"""
replication_omxsb.py: Table 2 and Figure 2 of the thesis (H1), the Greenwood-Sammon replication on OMXSB.

Runs as soon as the stock panel exists. Uses no FTN date.

Inputs
  ../data/omxsb/omxsb_changes_2013_2026.csv   events (effective_date, announcement_date, company, ticker, type)
  ../data/prices/stocks_daily.csv             long: id, date, ri, volume_sek, mcap   (from LSEG or FinBas)
  ../data/prices/stocks_static.csv            id, name, ticker, isin (to map tickers in the event file to ids)
  ../data/prices/factors_daily.csv            date, mkt, smb, hml, mom, rf  (FinBas factors; or mkt only)
  ../data/omxsb/tracker_aum.csv               year, tracker_aum_sek (from omxsb_notes.md; built by hand)

Outputs (output/)
  table2_omxsb_car.csv      mean CAR by type x sub-period for [ann, eff] and [eff+1, eff+20], with BMP and KP tests
  table2_regression.csv     equation (8): CAR on Add, Add x expected demand / ADV, sub-period dummies
  figure2_data.csv          yearly mean CAR and tracker AUM for the "disappearing" picture

Announcement timing convention (01_DESIGN.md 4.2): releases before May 2021 came pre-open at 08:30, so day 0 of the
announcement window is the announcement date itself; from May 2021 releases came after the close, so day 0 is the
next trading day. The effective date is the first day the new composition applies; trackers trade at the close of the
day before, so the effective window ends at eff - 1 for the demand and eff for the price (we report both).
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from eventstudy import load_prices, trading_calendar, shift_trading_days, factor_model_ar, car, bmp_test, kp_adjusted_t, cluster_ols

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))  # repo-roten; filen flyttades 13 nov 2026 från code/ till arkiv/02_ftn_pristryck_gs_okt2026/kod/
RAW = os.path.join(REPO, "data", "raw"); INP = os.path.join(REPO, "data", "input"); DER = os.path.join(REPO, "data", "derived")
PRICES = os.path.join(RAW, "lseg", "panel_2012_2026")  # LSEG panel 2012-2026; see data/MANIFEST.md
OUT = os.path.join(HERE, "..", "output"); os.makedirs(OUT, exist_ok=True)  # 13 nov 2026: utdata i uppsatsmappen, inte i rotens output/



def map_events_to_ids(events: pd.DataFrame, static: pd.DataFrame) -> pd.DataFrame:
    """Join on ticker first, then on a normalised company name. Unmatched rows are written out for hand-matching."""
    st = static.copy()
    st["ticker_n"] = st["ticker"].astype(str).str.upper().str.replace(" ", "")
    ev = events.copy()
    ev["ticker_n"] = ev["ticker"].astype(str).str.upper().str.replace(" ", "")
    m = ev.merge(st[["id", "ticker_n"]], on="ticker_n", how="left")
    un = m[m.id.isna()]
    if len(un):
        un.to_csv(os.path.join(OUT, "omxsb_unmatched_for_hand_matching.csv"), index=False)
        print(f"{len(un)} events unmatched on ticker; see output/omxsb_unmatched_for_hand_matching.csv")
    return m.dropna(subset=["id"])


def main():
    events = pd.read_csv(os.path.join(INP, "omxsb", "omxsb_changes_2013_2026.csv"),
                         parse_dates=["effective_date", "announcement_date"])
    static = pd.read_csv(os.path.join(PRICES, "stocks_static.csv"))
    prices = load_prices(os.path.join(PRICES, "stocks_daily.csv.gz"))
    factors = pd.read_csv(os.path.join(PRICES, "factors_daily.csv"), parse_dates=["date"]).set_index("date")
    cal = trading_calendar(prices)

    ev = map_events_to_ids(events, static)
    # day0 = announcement reaction day
    ev["day0"] = [shift_trading_days(cal, a, 1 if a >= pd.Timestamp("2021-05-01") else 0)
                  for a in ev.announcement_date]
    ev["eff_tau"] = [cal.get_loc(shift_trading_days(cal, e, 0)) - cal.get_loc(d0) for e, d0 in zip(ev.effective_date, ev.day0)]
    ev["add"] = (ev["type"] == "addition").astype(int)
    ev["period"] = pd.cut(ev.effective_date.dt.year, [2012, 2017, 2020, 2023, 2026],
                          labels=["2013-17", "2018-20", "2021-23", "2024-26"])

    arl = factor_model_ar(prices, factors, ev[["event_id", "id", "day0"]])
    rows = []
    for name, (a, b_fn) in {"ann_to_eff": (0, lambda r: r.eff_tau), "post_eff_20": (None, None)}.items():
        pass
    # announcement-to-effective CAR is event-specific in length: compute per event
    recs = []
    for r in ev.itertuples():
        w = arl[arl.event_id == r.event_id]
        if w.empty:
            continue
        c_ae = w[(w.tau >= 0) & (w.tau <= r.eff_tau)]["ar"].sum()
        c_post = w[(w.tau > r.eff_tau) & (w.tau <= r.eff_tau + 20)]["ar"].sum()
        sig = w.sigma_hat.iloc[0]
        recs.append({"event_id": r.event_id, "id": r.id, "add": r.add, "period": r.period, "year": r.effective_date.year,
                     "n_ae": r.eff_tau + 1, "car_ae": c_ae, "scar_ae": c_ae / (sig * np.sqrt(r.eff_tau + 1)),
                     "car_post20": c_post, "scar_post20": c_post / (sig * np.sqrt(20))})
    res = pd.DataFrame(recs)

    # Table 2: means by type and sub-period with BMP and KP tests
    t2 = []
    for (add, per), g in res.groupby(["add", "period"], observed=True):
        for win in ["ae", "post20"]:
            t, p = bmp_test(g[f"scar_{win}"].values)
            tadj, padj, rbar = kp_adjusted_t(g[f"scar_{win}"].values, arl[arl.event_id.isin(g.event_id)])
            t2.append({"type": "addition" if add else "deletion", "period": per, "window": win, "n": len(g),
                       "mean_car_pct": 100 * g[f"car_{win}"].mean(), "bmp_t": t, "kp_t": tadj, "kp_p": padj, "rbar": rbar})
    pd.DataFrame(t2).to_csv(os.path.join(OUT, "table2_omxsb_car.csv"), index=False)
    print(pd.DataFrame(t2).round(3).to_string())

    # Figure 2 data: yearly means and tracker AUM
    fig = res.groupby(["year", "add"])["car_ae"].mean().unstack().rename(columns={0: "deletion", 1: "addition"}) * 100
    aum_path = os.path.join(INP, "omxsb", "tracker_aum.csv")
    if os.path.exists(aum_path):
        aum = pd.read_csv(aum_path).set_index("year")
        fig = fig.join(aum, how="left")
    fig.to_csv(os.path.join(OUT, "figure2_data.csv"))

    # Equation (8): CAR on Add and Add x expected demand / ADV (expected demand needs tracker AUM and weights;
    # until weights exist, use tracker AUM / total OMXSB cap as the year-level demand proxy)
    if os.path.exists(aum_path):
        res = res.merge(aum.reset_index(), on="year", how="left")
        res["demand_proxy"] = res["tracker_aum_sek"] / res["tracker_aum_sek"].max()
        y = res.car_ae.values
        X = np.column_stack([np.ones(len(res)), res["add"].values, res["add"].values * res["demand_proxy"].values,
                             (1 - res["add"].values) * res["demand_proxy"].values])
        fit = cluster_ols(y, X, cluster=res["year"].values, n_boot=999)
        pd.DataFrame({"coef": ["const", "add", "add_x_demand", "del_x_demand"], "beta": fit["beta"], "se": fit["se"]}
                     ).to_csv(os.path.join(OUT, "table2_regression.csv"), index=False)
        print("equation (8):", dict(zip(["const", "add", "add_x_demand", "del_x_demand"], np.round(fit["beta"], 4))),
              "wild-cluster p for add_x_demand:", round(fit["p_boot"], 3))


if __name__ == "__main__":
    main()
