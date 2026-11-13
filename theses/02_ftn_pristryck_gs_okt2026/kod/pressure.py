"""
pressure.py: the exposure variable (equations 5 and 6) and the square-root prediction (equation 3). No returns.

Inputs
  ../data/exit_days/exit_days_by_loser.csv        tranche days per losing fund with flow_pct and dshares_pct
  ../data/exit_days/losers_daily_valuations.csv   daily TNA and units of the losers (to get A_j on the tranche day)
  FI holdings parsed to long form by data/derived/measurements/parse_fi.py:
      fi_holdings_<quarter>.csv with columns fund_name (or fund id), isin, name, market_value_sek, weight
  ../data/derived/measurements/fund_fi_mapping.csv       fondnr -> FI fund name (built earlier for 2024Q2/2026Q2)
  ../data/prices/stocks_daily.csv                 for ADV (volume_sek) and daily volatility (no event returns used:
                                                  ADV over [e-60, e-11], sigma over [e-250, e-11])
  winners' monthly inflows from the PPM panel (B in equation 5): data/derived/ppm/ppm_panel_2018_2026.csv

Output
  output/dose_stock_tranche.csv   one row per (stock, tranche day): S_ie, B_ie, F_ie, x_ie (net, days of ADV),
                                     x_sell, sigma_d, pi_hat (square-root prediction with Y = 0.7)
"""
import os, sys, glob
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
RAW = os.path.join(REPO, "data", "raw"); INP = os.path.join(REPO, "data", "input"); DER = os.path.join(REPO, "data", "derived")
PRICES = os.path.join(RAW, "lseg", "panel_2012_2026")  # LSEG panel 2012-2026; see data/MANIFEST.md
OUT = os.path.join(REPO, "output"); os.makedirs(OUT, exist_ok=True)
M = os.path.join(DER, "measurements")

Y_SQRT = 0.7


def parse_big_days(s: str):
    """'2026-01-15:-7.1%/-7.4%;2026-01-19:-6.4%/-7.1%' -> list of (date, flow_pct, dshares_pct)"""
    out = []
    if not isinstance(s, str) or not s:
        return out
    for part in s.split(";"):
        d, rest = part.split(":")
        f, sh = rest.split("/")
        f = float(f.replace("%", "")) if f != "nan%" else np.nan
        sh = float(sh.replace("%", "")) if sh != "nan%" else np.nan
        out.append((pd.Timestamp(d), f, sh))
    return out


def tranches() -> pd.DataFrame:
    ex = pd.read_csv(os.path.join(DER, "exit_days", "exit_days_by_loser.csv"))
    rows = []
    for r in ex.itertuples():
        for d, f, sh in parse_big_days(r.big_days):
            rho = abs(sh) / 100 if not np.isnan(sh) else abs(f) / 100   # redeemed share of the fund that day
            rows.append({"round": r.round, "fondnr": r.fondnr, "fondnamn": r.fondnamn, "performanceid": r.performanceid,
                         "tranche_date": d, "rho": rho, "flow_pct": f, "dshares_pct": sh})
    t = pd.DataFrame(rows)
    val = pd.read_csv(os.path.join(DER, "exit_days", "losers_daily_valuations.csv"), parse_dates=["date"],
                      dtype={"performanceId": str})
    # fund assets on the day before the tranche (fund currency; convert non-SEK with an FX series: TODO)
    val = val.sort_values(["performanceId", "date"])
    a_prev = val.groupby("performanceId").apply(lambda g: g.set_index("date")["tnafund"].shift(1)).reset_index()
    a_prev.columns = ["performanceid", "tranche_date", "A_prev"]
    t = t.merge(a_prev, on=["performanceid", "tranche_date"], how="left")
    t["S_fund_sek"] = t["rho"] * t["A_prev"]
    return t


def holdings_before(quarter_files: dict, fund_map: pd.DataFrame, fondnr: int, date: pd.Timestamp) -> pd.DataFrame:
    """Return the last FI holdings report dated before the saver letter (about 3 weeks before the first tranche)."""
    cutoff = date - pd.Timedelta(days=21)
    qs = sorted([q for q in quarter_files if quarter_end(q) < cutoff])
    if not qs:
        return pd.DataFrame()
    h = pd.read_csv(quarter_files[qs[-1]])
    fi_name = fund_map.loc[fund_map.fondnr == fondnr, "fi_fund_name"]
    if fi_name.empty:
        return pd.DataFrame()
    return h[h.fund_name == fi_name.iloc[0]]


def quarter_end(q: str) -> pd.Timestamp:
    y, n = int(q[:4]), int(q[-1])
    return pd.Timestamp(year=y, month=3 * n, day=1) + pd.offsets.MonthEnd(0)


def main():
    t = tranches()
    t.to_csv(os.path.join(OUT, "tranches.csv"), index=False)
    print(f"{len(t)} tranche days across {t.fondnr.nunique()} losers; median rho = {t.rho.median():.3f}")
    quarter_files = {os.path.basename(f)[12:18]: f for f in glob.glob(os.path.join(M, "fi_holdings_*.csv"))}
    if not quarter_files:
        print("no parsed FI holdings found in", M, "; run parse_fi.py on the FI zips first"); return
    fund_map = pd.read_csv(os.path.join(M, "fund_fi_mapping.csv"))
    rows = []
    for r in t.itertuples():
        h = holdings_before(quarter_files, fund_map, r.fondnr, r.tranche_date)
        if h.empty or np.isnan(r.S_fund_sek):
            continue
        w = h.set_index("isin")["weight"]
        for isin, wi in w.items():
            rows.append({"round": r.round, "tranche_date": r.tranche_date, "isin": isin, "fondnr": r.fondnr,
                         "S_sek": r.S_fund_sek * wi})
    S = pd.DataFrame(rows).groupby(["round", "tranche_date", "isin"], as_index=False)["S_sek"].sum()
    # TODO B_ie: winners' monthly inflow from the PPM panel x winners' FI weights, spread over the month's trading days
    S["B_sek"] = 0.0
    S["F_sek"] = S["B_sek"] - S["S_sek"]
    px_path = os.path.join(PRICES, "stocks_daily.csv.gz")
    if os.path.exists(px_path):
        px = pd.read_csv(px_path, parse_dates=["date"])
        st = pd.read_csv(os.path.join(PRICES, "stocks_static.csv"))
        px = px.merge(st[["id", "isin"]], on="id")
        px = px.sort_values(["isin", "date"])
        px["ret"] = px.groupby("isin")["ri"].pct_change()
        recs = []
        for r in S.itertuples():
            g = px[(px.isin == r.isin) & (px.date < r.tranche_date)]
            adv = g[g.date >= r.tranche_date - pd.Timedelta(days=90)].tail(50).head(40)["volume_sek"].mean()
            sig = g.tail(250).head(240)["ret"].std()
            recs.append({"adv_sek": adv, "sigma_d": sig})
        S = pd.concat([S.reset_index(drop=True), pd.DataFrame(recs)], axis=1)
        S["x_net"] = S["F_sek"] / S["adv_sek"]
        S["x_sell"] = -S["S_sek"] / S["adv_sek"]
        S["pi_hat"] = Y_SQRT * S["sigma_d"] * np.sqrt(S["x_net"].abs()) * np.sign(S["x_net"])
    S.to_csv(os.path.join(OUT, "dose_stock_tranche.csv"), index=False)
    print(S.describe().to_string())


if __name__ == "__main__":
    main()
