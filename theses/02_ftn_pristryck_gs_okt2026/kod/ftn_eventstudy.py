"""
ftn_eventstudy.py: Tables 3 and 4 and Figure 3 (H2, H3). GATED.

UNBLIND must be set to True by hand, after the specifications in 01_DESIGN.md have been agreed with the tutor
and the agreement date has been written into 03_DATA.md section E. Until then the script refuses to run.

Inputs: output/dose_stock_tranche.csv (from pressure.py), ../data/prices/*.csv, ../data/prices/factors_daily.csv,
        award and letter dates per round (Appendix A1 table, ../data/round_dates.csv: round, award_date, letter_date)
Outputs: output/table3_pressure.csv, table4_anticipation.csv, figure3_eventtime.csv
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from eventstudy import load_prices, trading_calendar, shift_trading_days, factor_model_ar, car, bmp_test, kp_adjusted_t, cluster_ols, ri_slope

UNBLIND = False
AGREED_WITH_TUTOR_ON = None   # e.g. "2026-10-17"

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
RAW = os.path.join(REPO, "data", "raw"); INP = os.path.join(REPO, "data", "input"); DER = os.path.join(REPO, "data", "derived")
PRICES = os.path.join(RAW, "lseg", "panel_2012_2026")  # LSEG panel 2012-2026; see data/MANIFEST.md
OUT = os.path.join(REPO, "output"); os.makedirs(OUT, exist_ok=True)



def main():
    if not UNBLIND or AGREED_WITH_TUTOR_ON is None:
        raise SystemExit("Blind rule: set UNBLIND = True and AGREED_WITH_TUTOR_ON = 'YYYY-MM-DD' after the Klug meeting.")
    dose = pd.read_csv(os.path.join(OUT, "dose_stock_tranche.csv"), parse_dates=["tranche_date"])
    st = pd.read_csv(os.path.join(PRICES, "stocks_static.csv"))
    dose = dose.merge(st[["id", "isin"]], on="isin")
    prices = load_prices(os.path.join(PRICES, "stocks_daily.csv.gz"))
    factors = pd.read_csv(os.path.join(PRICES, "factors_daily.csv"), parse_dates=["date"]).set_index("date")
    dose["event_id"] = dose["id"] + "_" + dose["tranche_date"].dt.strftime("%Y%m%d")
    ev = dose.rename(columns={"tranche_date": "day0"})[["event_id", "id", "day0"]].drop_duplicates()
    arl = factor_model_ar(prices, factors, ev)

    # Table 3: CAR[-1,+1] on pi_hat (col 1), on x_net (col 2), on x_sell (col 3); round FE; cluster by tranche day; RI within day
    c = car(arl, -1, 1).merge(dose, on="event_id")
    rounds = pd.get_dummies(c["round"], drop_first=False).astype(float).values
    rows = []
    for reg in ["pi_hat", "x_net", "x_sell"]:
        X = np.column_stack([rounds, c[reg].values])
        fit = cluster_ols(c["car"].values, X, cluster=c["tranche_date"].values, n_boot=999, coef_index=X.shape[1] - 1)
        ri = ri_slope(c["car"].values, c[reg].values, group=c["tranche_date"].values, n_perm=2000, controls=rounds[:, 1:])
        rows.append({"regressor": reg, "beta": fit["beta"][-1], "se_cluster": fit["se"][-1], "t": fit["t"],
                     "p_wild": fit["p_boot"], "p_ri": ri["p_ri"], "N": len(c), "clusters": fit["G"],
                     "test_beta_eq_1_t": (fit["beta"][-1] - 1) / fit["se"][-1] if reg == "pi_hat" else np.nan})
    # reversal: CAR[+2, +20] after the last tranche of the stock's round (approximation: per tranche)
    crev = car(arl, 2, 20).merge(dose, on="event_id")
    X = np.column_stack([rounds, crev["pi_hat"].values])
    fit = cluster_ols(crev["car"].values, X, cluster=crev["tranche_date"].values, n_boot=999, coef_index=X.shape[1] - 1)
    rows.append({"regressor": "pi_hat, reversal [+2,+20]", "beta": fit["beta"][-1], "se_cluster": fit["se"][-1], "t": fit["t"],
                 "p_wild": fit["p_boot"], "p_ri": np.nan, "N": len(crev), "clusters": fit["G"], "test_beta_eq_1_t": np.nan})
    t3 = pd.DataFrame(rows); t3.to_csv(os.path.join(OUT, "table3_pressure.csv"), index=False); print(t3.round(4).to_string())

    # Figure 3: mean AR by tau, dose terciles
    c["tercile"] = pd.qcut(c["pi_hat"].abs(), 3, labels=["low", "mid", "high"])
    f3 = arl.merge(c[["event_id", "tercile"]], on="event_id").groupby(["tercile", "tau"], observed=True)["ar"].mean().unstack(0).cumsum()
    f3.to_csv(os.path.join(OUT, "figure3_eventtime.csv"))

    # Table 4: anticipation windows around award and letter, same regressors (dose = round-level cumulative dose)
    rd = pd.read_csv(os.path.join(INP, "round_dates.csv"), parse_dates=["award_date", "letter_date"])
    cum = dose.groupby(["round", "id"], as_index=False)[["x_net", "x_sell", "pi_hat"]].sum()
    out4 = []
    for win_name, col in [("award", "award_date"), ("letter", "letter_date")]:
        evw = cum.merge(rd[["round", col]], on="round").rename(columns={col: "day0"})
        evw["event_id"] = evw["id"] + "_" + win_name + "_" + evw["round"]
        arw = factor_model_ar(prices, factors, evw[["event_id", "id", "day0"]])
        cw = car(arw, -1, 5).merge(evw, on="event_id")
        R = pd.get_dummies(cw["round"]).astype(float).values
        X = np.column_stack([R, cw["pi_hat"].values])
        fit = cluster_ols(cw["car"].values, X, cluster=cw["round"].values, n_boot=999, coef_index=X.shape[1] - 1)
        ri = ri_slope(cw["car"].values, cw["pi_hat"].values, group=cw["round"].values, n_perm=2000, controls=R[:, 1:])
        out4.append({"window": f"{win_name} [-1,+5]", "beta": fit["beta"][-1], "se": fit["se"][-1], "p_wild": fit["p_boot"], "p_ri": ri["p_ri"], "N": len(cw)})
    t4 = pd.DataFrame(out4); t4.to_csv(os.path.join(OUT, "table4_anticipation.csv"), index=False); print(t4.round(4).to_string())


if __name__ == "__main__":
    main()
