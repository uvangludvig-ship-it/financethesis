"""Approximate market caps for ALL Swedish names from a SIXPRX-tracking fund's weights (Storebrand Sverige Plus, 2026Q2),
calibrated to the fetched Oct-2026 caps: cap_i ~ w_i * T, T = median(cap_known / w) over mapped large names.
SIXPRX is free-float, cap-weighted with a 10% issuer cap -> approximation only (flagged). Then sd(FIP) over all names.
Also: PPM share of each loser fund's NAV (forced redemption as % of fund).
Usage: python -I fip_allnames.py <agentP_root> <ftn_root>
"""
import sys, os, re, numpy as np, pandas as pd
P, FTN = sys.argv[1], sys.argv[2]; OUT = os.path.join(P, "out")
sys.path.insert(0, os.path.join(P, "scripts"))
from fip import CAP
pd.set_option("display.width", 220); pd.set_option("display.max_rows", 200)

H26 = pd.read_csv(os.path.join(OUT, "fi_holdings_2026q2.csv"), dtype={"fund_instnr": str})
H26 = H26[H26.asset_class == "ÖverlåtbartVärdepapper"]
trk = H26[H26.fund_instnr == "60909"].copy()   # Storebrand Sverige Plus (SIXPRX), 409 holdings
trk["w"] = trk.mv_sek / trk.nav_sek
w = trk.groupby("isin").w.sum()
# issuer-level weight for calibration (sum share classes)
comp = pd.Series({i: CAP[i][0] for i in CAP})
wc = w.groupby(w.index.map(lambda i: comp.get(i, i))).sum()
known = pd.Series({CAP[i][0]: CAP[i][1] for i in CAP if CAP[i][2] == 0})
ratio = (known / wc.reindex(known.index)).dropna()
ratio = ratio[(wc.reindex(ratio.index) > 0.001)]           # calibrate on names with weight > 0.1%
T = ratio.median()
print(f"calibration: T = {T:.0f} bn SEK implied SIXPRX cap (median), IQR ratio {ratio.quantile(.25)/T:.2f}-{ratio.quantile(.75)/T:.2f}, n={len(ratio)}")

rows = []
for tag in ["SE_active_2026q2_2026q2_actual", "SE_index_2026q2_2026q2_actual", "SE_index_2026q2_2026q2_actual_exAvanzaZero",
            "SE_index_2026q2_2026q2_actual_AvanzaZeroOnly", "SE_active_2024q2_2024q2_equal_new"]:
    g = pd.read_csv(os.path.join(OUT, f"netdemand_{tag}.csv"), index_col=0)
    g["company"] = [comp.get(i, i) for i in g.index]
    c = g.groupby("company").agg(net=("net", "sum"), gross=("gross", "sum"), country=("country", "first"))
    cap_known = pd.Series({CAP[i][0]: CAP[i][1] for i in CAP})
    cap_c = (wc * T)   # SEK bn, issuer level
    c["cap_bn"] = cap_known.reindex(c.index).fillna(cap_c.reindex(c.index))
    c["cap_src"] = np.where(cap_known.reindex(c.index).notna(), "fetched", np.where(cap_c.reindex(c.index).notna(), "sixprx_approx", "none"))
    c = c[c.cap_bn.notna() & (c.cap_bn > 0.5)]
    c["fip_pct"] = 100 * c.net / (c.cap_bn * 1e9)
    c["gross_pct"] = 100 * c.gross / (c.cap_bn * 1e9)
    c = c.sort_values("fip_pct")
    c.to_csv(os.path.join(OUT, f"fip_allnames_{tag}.csv"))
    sw = c[c.cap_src == "sixprx_approx"]
    rows.append(dict(tag=tag, n_names_with_cap=len(c), n_fetched=int((c.cap_src == "fetched").sum()), n_approx=int((c.cap_src == "sixprx_approx").sum()),
                     sd_fip_pct=c.fip_pct.std(), p90_abs_fip=c.fip_pct.abs().quantile(.9), p99_abs_fip=c.fip_pct.abs().quantile(.99), max_abs_fip=c.fip_pct.abs().max(),
                     n_abs_fip_gt_0p25=int((c.fip_pct.abs() > .25).sum()), n_abs_fip_gt_0p5=int((c.fip_pct.abs() > .5).sum()), n_abs_fip_gt_1=int((c.fip_pct.abs() > 1).sum()),
                     sd_gross_pct=c.gross_pct.std(), top5_neg=", ".join(f"{i} {v:.2f}%" for i, v in c.fip_pct.head(5).items()),
                     top5_pos=", ".join(f"{i} {v:.2f}%" for i, v in c.fip_pct.tail(5)[::-1].items())))
R = pd.DataFrame(rows); R.to_csv(os.path.join(OUT, "fip_allnames_summary.csv"), index=False)
print(R.drop(columns=["top5_neg", "top5_pos"]).round(3).to_string())
for _, r in R.iterrows():
    print(f"\n{r.tag}\n  most negative: {r.top5_neg}\n  most positive: {r.top5_pos}")

# PPM share of loser fund NAV (2024Q2 NAV vs PPM capital at award)
m = pd.read_csv(os.path.join(OUT, "fund_fi_mapping.csv"))
m["ppm_share_of_fund_2024q2_pct"] = 100 * m.mv_award / (m.nav_2024q2_bn * 1e9)
m.to_csv(os.path.join(OUT, "fund_fi_mapping.csv"), index=False)
print("\nPPM capital as % of fund NAV (2024Q2 NAV), losers:")
print(m[(m.role == "loser") & m.in_fi][["round", "fondnamn", "mv_award", "nav_2024q2_bn", "ppm_share_of_fund_2024q2_pct", "bench_2024q2"]]
      .assign(mv_award=lambda d: (d.mv_award / 1e9).round(2)).round(1).sort_values(["round", "mv_award"], ascending=[True, False]).to_string(index=False))
