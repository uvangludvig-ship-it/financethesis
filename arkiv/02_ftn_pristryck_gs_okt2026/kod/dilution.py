"""
dilution.py: Table 5 (H4), who paid on the tranche days. GATED, same switch as ftn_eventstudy.py.

Fund NAV total return on tranche day e minus benchmark return, for losing fund j:
    d_je = r_je^NAV - r_e^bench
Regression (equation in 01_DESIGN.md 3.4):
    d_je = a + b1 * [rho_je / (1 - rho_je)] * NoSwing_j + b2 * [rho_je / (1 - rho_je)] * Swing_j + fund FE + e
b1 estimates the realised cost c for funds that did not swing (prediction: b1 = -c, with c about the square-root
cost of the sold basket); b2 is predicted to be about zero or positive.

Inputs: ../data/exit_days/exit_days_by_loser.csv (tranches), SHoF Reinvestments daily (fund NAV total return in SEK,
        performanceId x date; convert to returns), ../data/prices/indices_daily.csv (benchmarks), fund master benchmark
        names, ../data/swing/swing_status_ftn_losers.csv (YES / NO / UNKNOWN at exit).
Index losers: benchmark = their own index (OMXS30 GI for Avanza Zero, SIXPRX / SBX for the others, per the fund rules).
Active losers: benchmark = the fund's stated benchmark; second column against the mean of same-category PPM peers.
Output: output/table5_incidence.csv
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from eventstudy import cluster_ols
from pressure import tranches

UNBLIND = False
AGREED_WITH_TUTOR_ON = None

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))  # repo-roten; filen flyttades 13 nov 2026 från code/ till arkiv/02_ftn_pristryck_gs_okt2026/kod/
RAW = os.path.join(REPO, "data", "raw"); INP = os.path.join(REPO, "data", "input"); DER = os.path.join(REPO, "data", "derived")
PRICES = os.path.join(RAW, "lseg", "panel_2012_2026")  # LSEG panel 2012-2026; see data/MANIFEST.md
OUT = os.path.join(HERE, "..", "output"); os.makedirs(OUT, exist_ok=True)  # 13 nov 2026: utdata i uppsatsmappen, inte i rotens output/



def main():
    if not UNBLIND or AGREED_WITH_TUTOR_ON is None:
        raise SystemExit("Blind rule: set UNBLIND = True and AGREED_WITH_TUTOR_ON = 'YYYY-MM-DD' after the Klug meeting.")
    t = tranches()
    sw = pd.read_csv(os.path.join(INP, "swing", "swing_status_ftn_losers.csv"))[["fondnr", "swing_status_at_exit", "domicile"]]
    t = t.merge(sw, on="fondnr", how="left")
    nav = pd.read_csv(os.path.join(DER, "shof", "fund_nav_daily.csv"), parse_dates=["date"], dtype={"performanceid": str})  # built from Reinvestments
    bench = pd.read_csv(os.path.join(DER, "shof", "fund_benchmark_daily.csv"), parse_dates=["date"], dtype={"performanceid": str})
    nav = nav.sort_values(["performanceid", "date"]); nav["r_nav"] = nav.groupby("performanceid")["tri_sek"].pct_change()
    bench = bench.sort_values(["performanceid", "date"]); bench["r_b"] = bench.groupby("performanceid")["bench_tri"].pct_change()
    panel = nav.merge(bench[["performanceid", "date", "r_b"]], on=["performanceid", "date"])
    panel["d"] = panel["r_nav"] - panel["r_b"]
    # tranche-day observations plus non-event days as controls (fund FE absorb the mean tracking difference)
    panel = panel.merge(t[["performanceid", "tranche_date", "rho", "swing_status_at_exit"]].rename(columns={"tranche_date": "date"}),
                        on=["performanceid", "date"], how="left")
    panel["rho"] = panel["rho"].fillna(0.0)
    panel["swing"] = (panel["swing_status_at_exit"] == "YES").astype(float)
    panel["noswing"] = (panel["swing_status_at_exit"] == "NO").astype(float)
    lev = panel["rho"] / (1 - panel["rho"])
    F = pd.get_dummies(panel["performanceid"]).astype(float).values
    X = np.column_stack([F, lev * panel["noswing"], lev * panel["swing"]])
    fit = cluster_ols(panel["d"].values * 1e4, X, cluster=panel["date"].values, n_boot=999, coef_index=X.shape[1] - 2)
    res = pd.DataFrame({"coef": ["lev x NoSwing (bp per unit rho/(1-rho))", "lev x Swing"],
                        "beta": fit["beta"][-2:], "se": fit["se"][-2:]})
    res.to_csv(os.path.join(OUT, "table5_incidence.csv"), index=False); print(res.round(2).to_string())


if __name__ == "__main__":
    main()
