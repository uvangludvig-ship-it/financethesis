"""Executed-rounds feasibility: holdings coverage, net stock demand, execution windows.
Usage: python -I analyze.py <ftn_root> <agentP_root>
Reads: agentA/task1_round_membership.csv, ppm_panel_2018_2026.csv, agentP/out/fi_holdings_*.csv, fi_funds_*.csv
Writes CSVs into agentP/out/.
"""
import sys, os, numpy as np, pandas as pd
FTN, P = sys.argv[1], sys.argv[2]
OUT = os.path.join(P, "out")
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400); pd.set_option("display.max_colwidth", 60)

# ---------------------------------------------------------------- curated PPM fondnr -> FI institutnummer map
# value: (instnr_2024q2, instnr_2026q2, domicile/note). None = not in FI (not Swedish-registered or shell file).
MAP = {
 # SE_active losers
 528133: ("51682", "51682", "SE"), 916189: ("51541", "51541", "SE"), 203067: ("51540", "51540", "SE (Nordea Funds Ab Swedish-registered fund)"),
 450981: (None, None, "NO: ODIN Forvaltning AS, FI file is 'Ej aktiv fond' shell"), 158261: ("56053", "56053", "SE"),
 904904: ("60666", None, "SE (Öhman -> Lannebo 2024; fund gone by 2026Q2)"), 339184: ("51761", "51761", "SE"),
 806869: ("51669", "51669", "SE"), 272898: ("60279", "60279", "SE"), 490292: ("60311", "60311", "SE"),
 846527: (None, None, "LU: SEB SICAV (SEB Sweden Equity Fund C); converted into 'SEB 3 - SEB Sweden Equity Fund' Nov 2025"),
 344739: ("51172", "51172", "SE"), 328021: ("60588", "60588", "SE"), 973263: (None, None, "LU: Danske Invest SICAV"),
 792697: (None, None, "LU: C WorldWide"), 146928: ("60447", None, "SE (closed 2025)"), 106849: ("51781", "51781", "SE (named Indecap Guide Sverige in 2024Q2)"),
 643700: ("60204", "60204", "SE (named Enter Select in 2024Q2)"),
 # SE_active winners
 681783: ("51448", "51448", "SE"), 291906: ("51313", "51313", "SE (Didner & Gerge Aktiefond, now Carnegie Fonder)"), 976928: ("51496", "51496", "SE"), 393314: ("51272", "51272", "SE"),
 423822: ("60012", "60012", "SE"), 459652: ("60730", "60730", "SE"), 495482: ("51718", "51718", "SE"),
 531310: (None, None, "LU: SEB SICAV 3 (same portfolio family as SEB Sweden Equity Fund C)"), 567140: ("60351", "60351", "SE"), 607226: ("51776", "51776", "SE"),
 # SE_index
 734491: ("60097", "60097", "SE"), 212332: ("51482", "51482", "SE"), 610410: (None, None, "FI: Evli Fund Management (Finland)"),
 292193: ("60638", "60638", "SE"), 587337: ("60310", "60310", "SE"), 528894: ("60878", "60878", "SE"), 577833: ("60029", "60029", "SE (now Lannebo Marknad Sverige Bred)"),
 357658: ("60909", "60909", "SE"), 719674: ("60824", "60824", "SE"), 465914: ("60479", "60479", "SE"), 290072: ("51550", "51550", "SE"),
 638809: ("51734", "51734", "SE"), 602979: (None, "76299", "SE (launched 2025; 2024Q2 file is an 'Ej aktiv' shell)"),
 # Nordic_active
 820852: ("51455", "51455", "SE"), 484980: ("51758", "51758", "SE"), 811117: ("51200", "51200", "SE"), 598557: (None, None, "NO: ODIN"),
 388298: (None, None, "NO: Delphi/Storebrand"), 354290: (None, None, "NO: Holberg"), 147512: (None, None, "NO: DNB"),
 521104: (None, None, "FI: Ålandsbanken"), 484923: ("56051", "56051", "SE"), 861757: (None, None, "FI/LU: Nordea Nordic Fund (not in FI VPFO)"), 674630: ("60729", "60729", "SE"),
 # Nordic_smallcap
 785493: (None, None, "FI: Fondita"), 339473: (None, None, "FI: Aktia"), 286294: (None, None, "FI: Nordea Funds Ab (Finland-registered)"),
 751495: ("51449", "51449", "SE"), 237834: (None, None, "FI: Fondita"), 710467: (None, None, "LU: SEB SICAV"),
 # Global_index
 658997: ("60650", "60650", "SE"), 680124: ("61050", "61050", "SE (feeder: 1 holding = Amundi index fund)"), 252411: (None, None, "LU: Danske"), 393488: ("60869", "60869", "SE"),
 407064: ("51648", "51648", "SE"), 362491: (None, None, "NO: DNB"), 613729: (None, None, "LU: Danske"), 199753: ("60968", "60968", "SE"),
 114819: ("60800", "60800", "SE"), 785907: ("61032", "61032", "SE"), 545426: ("60667", "60667", "SE"), 491233: ("72144", "72144", "SE"),
 343665: (None, None, "IE: Mercer CCF"), 527060: (None, None, "NO: Storebrand Global Indeks"),
}

mem = pd.read_csv(os.path.join(FTN, "agentA/task1_round_membership.csv"))
ROUNDS = ["SE_active", "SE_index", "Nordic_active", "Nordic_smallcap", "Global_index", "SE_smallcap"]
mem = mem[mem["round"].isin(ROUNDS)].copy()
panel = pd.read_csv(os.path.join(FTN, "ppm_panel_2018_2026.csv"), usecols=["fondnr", "fondnamn", "mv_tot", "handel_netto", "date"], parse_dates=["date"])

H = {q: pd.read_csv(os.path.join(OUT, f"fi_holdings_{q}.csv"), dtype={"fund_instnr": str}) for q in ["2024q2", "2026q2"]}
F = {q: pd.read_csv(os.path.join(OUT, f"fi_funds_{q}.csv"), dtype={"fund_instnr": str}) for q in ["2024q2", "2026q2"]}
for q in H:
    H[q] = H[q][H[q].asset_class == "ÖverlåtbartVärdepapper"].copy()   # equities (+ a few listed non-equities), drops fund units/derivatives/MM
    H[q]["w"] = H[q].mv_sek / H[q].nav_sek                                # weight of fund NAV

# ---------------------------------------------------------------- coverage table
cov_rows = []
for _, r in mem.iterrows():
    a, b, note = MAP.get(r.fondnr, (None, None, "NOT MAPPED"))
    cov_rows.append(dict(round=r["round"], fondnr=r.fondnr, fondnamn=r.fondnamn, role=r.role, mv_award=r.mv_award,
                         fi_2024q2=a, fi_2026q2=b, in_fi=bool(a or b), note=note,
                         fi_name_2024q2=F["2024q2"].set_index("fund_instnr").fund_name.get(a, "") if a else "",
                         bench_2024q2=F["2024q2"].set_index("fund_instnr").benchmark.get(a, "") if a else "",
                         bench_2026q2=F["2026q2"].set_index("fund_instnr").benchmark.get(b, "") if b else "",
                         n_hold_2024q2=F["2024q2"].set_index("fund_instnr").n_holdings.get(a, np.nan) if a else np.nan,
                         nav_2024q2_bn=F["2024q2"].set_index("fund_instnr").nav_sek.get(a, np.nan) / 1e9 if a else np.nan))
cov = pd.DataFrame(cov_rows)
cov.to_csv(os.path.join(OUT, "fund_fi_mapping.csv"), index=False)

# ---------------------------------------------------------------- actual winner inflows per round (execution window from panel)
WINDOW = {"SE_active": ("2025-10-31", "2026-05-31"), "SE_index": ("2025-10-31", "2026-08-31"), "Nordic_active": ("2025-03-31", "2025-09-30"),
          "Nordic_smallcap": ("2025-03-31", "2025-09-30"), "Global_index": ("2024-11-30", "2025-07-31"), "SE_smallcap": ("2026-06-30", "2026-08-31")}
def winner_inflows(rnd):
    ids = mem[(mem["round"] == rnd) & mem.role.str.startswith("winner")].fondnr
    d0, d1 = WINDOW[rnd]
    x = panel[panel.fondnr.isin(ids) & (panel.date >= d0) & (panel.date <= d1)]
    return x.groupby("fondnr").handel_netto.sum().clip(lower=0)

# ---------------------------------------------------------------- demand model
def demand(rnd, q_loser="2024q2", q_winner="2024q2", winner_alloc="equal_new", include=None, exclude=()):
    """sell_i = sum_l w_li * C_l ; buy_i = sum_w w_wi * B_w with B_w = share_w * sum(C_l covered+uncovered)."""
    sub = mem[mem["round"] == rnd]
    losers = sub[(sub.role == "loser") & ~sub.fondnr.isin(exclude)]
    if include is not None:
        losers = losers[losers.fondnr.isin(include)]
    winners = sub[sub.role.str.startswith("winner")]
    tot_C = losers.mv_award.sum()
    rows = []
    cov_C = 0.0
    for _, l in losers.iterrows():
        inst = MAP.get(l.fondnr, (None, None, ""))[0 if q_loser == "2024q2" else 1]
        if not inst:
            continue
        h = H[q_loser][H[q_loser].fund_instnr == inst]
        if h.empty:
            continue
        cov_C += l.mv_award
        for _, s in h.iterrows():
            rows.append(dict(isin=s["isin"], name=s["name"], country=s.country, side="sell", fund=l.fondnamn, sek=s.w * l.mv_award, price=s.price))
    # winner allocation shares
    if winner_alloc == "equal_new":
        wn = winners[winners.role == "winner_new"]
        shares = pd.Series(1 / len(wn), index=wn.fondnr)
    else:  # actual panel inflows
        inf = winner_inflows(rnd); shares = inf / inf.sum()
    cov_B = 0.0
    for fn, sh in shares.items():
        inst = MAP.get(fn, (None, None, ""))[0 if q_winner == "2024q2" else 1]
        wname = winners.set_index("fondnr").fondnamn.get(fn, str(fn))
        if not inst:
            continue
        h = H[q_winner][H[q_winner].fund_instnr == inst]
        if h.empty:
            continue
        cov_B += sh
        for _, s in h.iterrows():
            rows.append(dict(isin=s["isin"], name=s["name"], country=s.country, side="buy", fund=wname, sek=s.w * sh * tot_C, price=s.price))
    df = pd.DataFrame(rows)
    if df.empty or "isin" not in df:
        raise ValueError("no covered holdings")
    df = df[df["isin"].astype(str).str.len() == 12]
    g = df.pivot_table(index="isin", columns="side", values="sek", aggfunc="sum").fillna(0.0)
    for c in ["buy", "sell"]:
        if c not in g: g[c] = 0.0
    names = df.groupby("isin")["name"].agg(lambda s: s.value_counts().index[0])
    ctry = df.groupby("isin")["country"].agg(lambda s: s.value_counts().index[0])
    price = df.groupby("isin")["price"].median()
    g["name"] = names; g["country"] = ctry; g["price_fi"] = price
    g["net"] = g.buy - g.sell; g["gross"] = g.buy + g.sell
    g = g.sort_values("net")
    meta = dict(round=rnd, q_loser=q_loser, q_winner=q_winner, alloc=winner_alloc, total_loser_capital_bn=tot_C / 1e9,
                loser_capital_covered_pct=100 * cov_C / tot_C if tot_C else np.nan, winner_alloc_covered_pct=100 * cov_B,
                n_stocks=len(g), corr_buy_sell=g.buy.corr(g.sell), sd_net_m=g.net.std() / 1e6, sd_gross_m=g.gross.std() / 1e6,
                sd_net_over_sd_gross=g.net.std() / g.gross.std(), sum_abs_net_over_sum_gross=g.net.abs().sum() / g.gross.sum(),
                top10_share_sq_net=(g.net ** 2).sort_values(ascending=False).head(10).sum() / (g.net ** 2).sum(),
                n_abs_net_gt_100m=int((g.net.abs() > 1e8).sum()), n_abs_net_gt_50m=int((g.net.abs() > 5e7).sum()),
                sum_buy_bn=g.buy.sum() / 1e9, sum_sell_bn=g.sell.sum() / 1e9, sum_abs_net_bn=g.net.abs().sum() / 1e9,
                largest_sells="; ".join(f"{n} {v/1e6:.0f}m" for n, v in g.head(8)[["name", "net"]].values),
                largest_buys="; ".join(f"{n} {v/1e6:.0f}m" for n, v in g.tail(8)[::-1][["name", "net"]].values))
    return g, meta

results, metas = {}, []
specs = [
    ("SE_active", dict()), ("SE_active", dict(winner_alloc="actual")), ("SE_active", dict(q_winner="2026q2", winner_alloc="actual")),
    ("SE_index", dict(winner_alloc="actual")), ("SE_index", dict(winner_alloc="actual", exclude=(734491,))),
    ("SE_index", dict(winner_alloc="actual", include=[734491])), ("SE_index", dict(winner_alloc="actual", q_winner="2026q2")),
    ("SE_index", dict(winner_alloc="equal_new")),
    ("SE_index", dict(winner_alloc="actual", q_loser="2026q2", q_winner="2026q2")),
    ("SE_index", dict(winner_alloc="actual", q_loser="2026q2", q_winner="2026q2", exclude=(734491,))),
    ("SE_index", dict(winner_alloc="actual", q_loser="2026q2", q_winner="2026q2", include=[734491])),
    ("SE_active", dict(winner_alloc="actual", q_loser="2026q2", q_winner="2026q2")),
    ("Nordic_active", dict()), ("Nordic_active", dict(winner_alloc="actual")),
    ("Nordic_smallcap", dict()), ("Global_index", dict(winner_alloc="actual")), ("SE_smallcap", dict(q_loser="2026q2", q_winner="2026q2")),
]
for rnd, kw in specs:
    try:
        g, m = demand(rnd, **kw)
    except Exception as e:
        print("FAIL", rnd, kw, e); continue
    tag = f"{rnd}_{m['q_loser']}_{m['q_winner']}_{m['alloc']}" + ("_exAvanzaZero" if kw.get("exclude") else "") + ("_AvanzaZeroOnly" if kw.get("include") else "")
    g.to_csv(os.path.join(OUT, f"netdemand_{tag}.csv"))
    results[tag] = g; metas.append(dict(tag=tag, **m))
M = pd.DataFrame(metas)
M.to_csv(os.path.join(OUT, "netdemand_summary.csv"), index=False)
print(M.drop(columns=["largest_sells", "largest_buys"]).round(3).to_string())
for t in results:
    print("\n====", t); print("  SELL:", M.set_index("tag").largest_sells[t]); print("  BUY :", M.set_index("tag").largest_buys[t])

# ---------------------------------------------------------------- SE_index: pairwise overlap between index funds (2024Q2 weights)
idx_funds = {"Avanza Zero": "60097", "Storebrand Sverige": "51482", "Storebrand Sverige Plus": "60909", "Skandia Sverige Exponering": "60638",
             "LF Sverige Index": "60310", "Aktiesp Direktavkastning": "60878", "Öhman Marknad Sverige Bred": "60029",
             "Robur Access Sverige": "60824", "HB Sverige 100 Index Crit": "60479", "HB Sverige Index Crit": "51734", "Aktiesp Topp Sverige": "51550"}
def wvec(q, inst):
    h = H[q][H[q].fund_instnr == inst]; return h.groupby("isin").w.sum()
W = pd.DataFrame({k: wvec("2024q2", v) for k, v in idx_funds.items()}).fillna(0.0)
W26 = pd.DataFrame({**{k: wvec("2026q2", v) for k, v in idx_funds.items()}, "HB Sverige LM Index": wvec("2026q2", "76299")}).fillna(0.0)
ov = pd.DataFrame({a: {b: 100 * np.minimum(W[a], W[b]).sum() for b in W} for a in W})
ov26 = pd.DataFrame({a: {b: 100 * np.minimum(W26[a], W26[b]).sum() for b in W26} for a in W26})
ov.round(1).to_csv(os.path.join(OUT, "se_index_overlap_2024q2.csv")); ov26.round(1).to_csv(os.path.join(OUT, "se_index_overlap_2026q2.csv"))
print("\n==== SE_index pairwise overlap (sum of min weights, %), 2024Q2 holdings"); print(ov.round(0).astype(int).to_string())
print("\n==== 2026Q2 (incl. LM Index)"); print(ov26.round(0).astype(int).to_string())
print("\nn holdings 2024Q2:", (W > 0).sum().to_dict()); print("n holdings 2026Q2:", (W26 > 0).sum().to_dict())
print("top-10 weight share 2024Q2:", {k: round(100 * W[k].sort_values(ascending=False).head(10).sum(), 1) for k in W})

# ---------------------------------------------------------------- Task 4: execution windows from monthly panel
AWARD = {"SE_active": "2025-08-27", "SE_index": "2025-08-27", "Nordic_active": "2025-02-19", "Nordic_smallcap": "2025-02-19",
         "Global_index": "2024-10-31", "SE_smallcap": "2026-05-28"}
rows = []
for rnd in ROUNDS:
    sub = mem[mem["round"] == rnd]
    los = sub[sub.role == "loser"]; win = sub[sub.role.str.startswith("winner")]
    A = pd.Timestamp(AWARD[rnd]) + pd.offsets.MonthEnd(0)
    months = pd.date_range(A - pd.offsets.MonthEnd(2), A + pd.offsets.MonthEnd(14), freq="ME")
    totC = los.mv_award.sum()
    x = panel[panel.fondnr.isin(los.fondnr)]
    # residual exit: a loser that disappears from the panel is treated as fully redeemed in the month after its last observation
    last = x.sort_values("date").groupby("fondnr").last()
    resid = {}
    for fn, r in last.iterrows():
        if r.date < panel.date.max():
            resid[(r.date + pd.offsets.MonthEnd(1))] = resid.get(r.date + pd.offsets.MonthEnd(1), 0) + r.mv_tot
    y = panel[panel.fondnr.isin(win.fondnr)]
    for mth in months:
        hl = x[x.date == mth].handel_netto.sum(); hw = y[y.date == mth].handel_netto.sum()
        rows.append(dict(round=rnd, month=mth.date(), rel_month=(mth.year - A.year) * 12 + mth.month - A.month,
                         loser_handel_netto_bn=hl / 1e9, loser_residual_exit_bn=-resid.get(mth, 0) / 1e9,
                         loser_total_out_pct_of_award_cap=100 * (hl - resid.get(mth, 0)) / totC,
                         winner_handel_netto_bn=hw / 1e9, winner_in_pct_of_award_cap=100 * hw / totC,
                         n_losers_in_panel=int((x.date == mth).sum())))
EX = pd.DataFrame(rows)
EX.to_csv(os.path.join(OUT, "execution_windows_monthly.csv"), index=False)
for rnd in ROUNDS:
    e = EX[EX["round"] == rnd]
    print(f"\n==== {rnd}: award {AWARD[rnd]}, loser capital {mem[(mem['round']==rnd)&(mem.role=='loser')].mv_award.sum()/1e9:.2f} bn")
    print(e[["month", "rel_month", "loser_handel_netto_bn", "loser_residual_exit_bn", "loser_total_out_pct_of_award_cap", "winner_handel_netto_bn", "winner_in_pct_of_award_cap", "n_losers_in_panel"]].round(2).to_string(index=False))
