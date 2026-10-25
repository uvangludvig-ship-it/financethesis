"""
eventstudy.py: a small, dependency-light event-study engine for the thesis.

Pure numpy/pandas. Functions:
  load_prices(path)            long or wide CSV -> long DataFrame [id, date, ret, volume_sek, mcap]
  factor_model_ar(...)         abnormal returns from a market or k-factor model estimated on a pre-window
  car(...)                     cumulative abnormal returns over [a, b] for a table of events
  bmp_test(...)                Boehmer, Musumeci and Poulsen (1991) standardised test
  kp_adjusted_t(...)           Kolari and Pynnonen (2010) cross-correlation adjustment
  ri_slope(...)                randomisation inference for a cross-sectional slope, permuting within a group
  cluster_ols(...)             OLS with cluster-robust standard errors (one-way) and a wild cluster bootstrap p-value

Conventions: dates are pandas Timestamps; returns are simple daily returns in decimal; event day 0 is the
trading day given in the event table (the caller handles announcement-timing conventions, see 01_DESIGN.md 4.2).
The engine never reads an FTN date on its own; it works on whatever event table it is given.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


# ----------------------------------------------------------------------------- prices

def load_prices(path: str, id_col: str = "id", date_col: str = "date",
                ri_col: str = "ri", vo_col: str | None = "volume_sek", mv_col: str | None = "mcap") -> pd.DataFrame:
    """Load a long CSV with at least [id, date, ri] (ri = total return index) and return
    [id, date, ret, volume_sek, mcap] sorted by id, date. Wide files: reshape before calling."""
    df = pd.read_csv(path, parse_dates=[date_col])
    df = df.rename(columns={id_col: "id", date_col: "date", ri_col: "ri"})
    if vo_col and vo_col in df.columns:
        df = df.rename(columns={vo_col: "volume_sek"})
    if mv_col and mv_col in df.columns:
        df = df.rename(columns={mv_col: "mcap"})
    df = df.sort_values(["id", "date"])
    df["ret"] = df.groupby("id")["ri"].pct_change()
    keep = ["id", "date", "ret"] + [c for c in ["volume_sek", "mcap"] if c in df.columns]
    return df[keep].dropna(subset=["ret"]).reset_index(drop=True)


def trading_calendar(prices: pd.DataFrame) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(sorted(prices["date"].unique()))


def shift_trading_days(cal: pd.DatetimeIndex, date: pd.Timestamp, k: int) -> pd.Timestamp:
    """Move k trading days from date (date snapped to the next trading day if not in cal)."""
    pos = cal.searchsorted(date)
    pos = min(max(pos + k, 0), len(cal) - 1)
    return cal[pos]


# ----------------------------------------------------------------------------- abnormal returns

def factor_model_ar(prices: pd.DataFrame, factors: pd.DataFrame, events: pd.DataFrame,
                    est_window=(-250, -31), min_obs: int = 120) -> pd.DataFrame:
    """
    For each event (rows with columns event_id, id, day0) estimate ret_it = a + b' f_t + e over the estimation
    window (trading days relative to day0) and return daily abnormal returns for days [-60, +60].
    factors: DataFrame indexed by date with factor columns (market model: one column of market excess return;
    include a column 'rf' to subtract from stock returns, else assume returns already excess or ignore rf).
    Output: long DataFrame [event_id, id, date, tau, ar, sigma_hat].
    """
    cal = trading_calendar(prices)
    px = prices.set_index(["id", "date"])["ret"]
    fcols = [c for c in factors.columns if c != "rf"]
    out = []
    for ev in events.itertuples(index=False):
        d0 = pd.Timestamp(ev.day0)
        if d0 not in cal:
            d0 = shift_trading_days(cal, d0, 0)
        pos0 = cal.get_loc(d0)
        lo, hi = pos0 + est_window[0], pos0 + est_window[1]
        if lo < 0:
            continue
        est_dates = cal[lo:hi + 1]
        ev_dates = cal[max(pos0 - 60, 0): min(pos0 + 61, len(cal))]
        try:
            r_est = px.loc[ev.id].reindex(est_dates)
        except KeyError:
            continue
        f_est = factors.reindex(est_dates)
        y = r_est.values - (f_est["rf"].values if "rf" in factors.columns else 0.0)
        X = np.column_stack([np.ones(len(est_dates))] + [f_est[c].values for c in fcols])
        ok = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
        if ok.sum() < min_obs:
            continue
        beta, *_ = np.linalg.lstsq(X[ok], y[ok], rcond=None)
        resid = y[ok] - X[ok] @ beta
        sigma = resid.std(ddof=X.shape[1])
        r_ev = px.loc[ev.id].reindex(ev_dates)
        f_ev = factors.reindex(ev_dates)
        yev = r_ev.values - (f_ev["rf"].values if "rf" in factors.columns else 0.0)
        Xev = np.column_stack([np.ones(len(ev_dates))] + [f_ev[c].values for c in fcols])
        ar = yev - Xev @ beta
        tau = np.arange(len(ev_dates)) - (pos0 - max(pos0 - 60, 0))
        out.append(pd.DataFrame({"event_id": ev.event_id, "id": ev.id, "date": ev_dates, "tau": tau,
                                 "ar": ar, "sigma_hat": sigma}))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(
        columns=["event_id", "id", "date", "tau", "ar", "sigma_hat"])


def car(ar_long: pd.DataFrame, a: int, b: int) -> pd.DataFrame:
    """CAR over tau in [a, b] per event, with standardised CAR (SCAR) for the BMP test."""
    w = ar_long[(ar_long.tau >= a) & (ar_long.tau <= b)]
    g = w.groupby("event_id")
    res = g["ar"].sum().rename("car").to_frame()
    res["n_days"] = g["ar"].count()
    res["sigma_hat"] = g["sigma_hat"].first()
    res["scar"] = res["car"] / (res["sigma_hat"] * np.sqrt(res["n_days"]))
    return res.reset_index()


# ----------------------------------------------------------------------------- tests

def bmp_test(scar: np.ndarray) -> tuple[float, float]:
    """Boehmer, Musumeci and Poulsen (1991): t = mean(SCAR) / (sd(SCAR)/sqrt(N)). Returns (t, two-sided p)."""
    s = np.asarray(scar, dtype=float)
    s = s[~np.isnan(s)]
    n = len(s)
    t = s.mean() / (s.std(ddof=1) / np.sqrt(n))
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / sqrt(2))))
    return float(t), float(p)


def kp_adjusted_t(scar: np.ndarray, ar_long: pd.DataFrame, est_window=(-250, -31)) -> tuple[float, float, float]:
    """
    Kolari and Pynnonen (2010) adjust the BMP statistic for the average cross-correlation of abnormal returns
    on common event days: t_adj = t_BMP * sqrt((1 - rbar) / (1 + (N - 1) rbar)).
    rbar is estimated from the estimation-window abnormal returns of the events (same calendar dates).
    Returns (t_adj, p_adj, rbar). If events do not overlap in calendar time, rbar is about zero and t_adj = t_BMP.
    """
    t, _ = bmp_test(scar)
    n = len(scar)
    est = ar_long[(ar_long.tau >= est_window[0]) & (ar_long.tau <= est_window[1])]
    wide = est.pivot_table(index="date", columns="event_id", values="ar")
    c = wide.corr(min_periods=30)
    vals = c.values[np.triu_indices_from(c.values, k=1)]
    rbar = float(np.nanmean(vals)) if np.isfinite(vals).any() else 0.0
    rbar = max(rbar, 0.0)
    t_adj = t * np.sqrt((1 - rbar) / (1 + (n - 1) * rbar))
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(t_adj) / sqrt(2))))
    return float(t_adj), float(p), rbar


def cluster_ols(y: np.ndarray, X: np.ndarray, cluster: np.ndarray, n_boot: int = 999, seed: int = 1,
                coef_index: int = 1) -> dict:
    """
    OLS with one-way cluster-robust SE (Liang-Zeger with small-sample G/(G-1) correction) and a wild cluster
    bootstrap p-value (Rademacher weights, restricted under H0: beta[coef_index] = 0), Cameron, Gelbach and
    Miller (2008). X must include the constant. Returns dict(beta, se, t, p_boot, G).
    """
    y = np.asarray(y, float); X = np.asarray(X, float); cluster = np.asarray(cluster)
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    groups = pd.unique(cluster); G = len(groups)
    meat = np.zeros((k, k))
    for g in groups:
        m = cluster == g
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
    se = np.sqrt(np.diag(V))
    t_obs = beta[coef_index] / se[coef_index]
    # restricted model for the wild bootstrap
    Xr = np.delete(X, coef_index, axis=1)
    br = np.linalg.lstsq(Xr, y, rcond=None)[0]
    ur = y - Xr @ br
    rng = np.random.default_rng(seed)
    gi = {g: i for i, g in enumerate(groups)}
    idx = np.array([gi[c] for c in cluster])
    count = 0
    for _ in range(n_boot):
        wts = rng.choice([-1.0, 1.0], size=G)[idx]
        yb = Xr @ br + ur * wts
        bb = XtX_inv @ X.T @ yb
        ub = yb - X @ bb
        meat = np.zeros((k, k))
        for g in groups:
            m = cluster == g
            s = X[m].T @ ub[m]
            meat += np.outer(s, s)
        Vb = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
        tb = bb[coef_index] / np.sqrt(Vb[coef_index, coef_index])
        if abs(tb) >= abs(t_obs):
            count += 1
    return {"beta": beta, "se": se, "t": float(t_obs), "p_boot": (count + 1) / (n_boot + 1), "G": G}


def ri_slope(y: np.ndarray, x: np.ndarray, group: np.ndarray, n_perm: int = 2000, seed: int = 1,
             controls: np.ndarray | None = None) -> dict:
    """
    Randomisation inference for the slope of y on x: permute x across observations WITHIN each group
    (e.g. within tranche day), re-estimate, and report the share of permuted |slope| >= observed |slope|.
    Controls (if any) are partialled out once (Frisch-Waugh) before permuting, which keeps the day fixed.
    """
    y = np.asarray(y, float); x = np.asarray(x, float); group = np.asarray(group)
    if controls is not None:
        C = np.column_stack([np.ones(len(y)), np.asarray(controls, float)])
        y = y - C @ np.linalg.lstsq(C, y, rcond=None)[0]
        x = x - C @ np.linalg.lstsq(C, x, rcond=None)[0]
    def slope(xx):
        xm = xx - xx.mean(); return float((xm @ (y - y.mean())) / (xm @ xm))
    b_obs = slope(x)
    rng = np.random.default_rng(seed)
    groups = pd.unique(group)
    members = {g: np.where(group == g)[0] for g in groups}
    count = 0
    for _ in range(n_perm):
        xp = x.copy()
        for g, m in members.items():
            xp[m] = x[m][rng.permutation(len(m))]
        if abs(slope(xp)) >= abs(b_obs):
            count += 1
    return {"slope": b_obs, "p_ri": (count + 1) / (n_perm + 1), "n_perm": n_perm}


# ----------------------------------------------------------------------------- self-test

if __name__ == "__main__":
    # synthetic check: 300 stocks, 1200 days, 40 events with a planted +2 per cent effect on days [0, 1]
    rng = np.random.default_rng(0)
    dates = pd.bdate_range("2019-01-01", periods=1200)
    mkt = rng.normal(0.0003, 0.01, len(dates))
    rows = []
    ids = [f"S{i:03d}" for i in range(300)]
    for s in ids:
        b = rng.normal(1, 0.3)
        r = b * mkt + rng.normal(0, 0.015, len(dates))
        ri = 100 * np.cumprod(1 + r)
        rows.append(pd.DataFrame({"id": s, "date": dates, "ri": ri}))
    px = pd.concat(rows)
    px.to_csv("/tmp/_synth_prices.csv", index=False)
    prices = load_prices("/tmp/_synth_prices.csv")
    factors = pd.DataFrame({"mkt": mkt}, index=dates)
    ev_days = rng.choice(np.arange(400, 1100), 40, replace=False)
    events = pd.DataFrame({"event_id": [f"E{i}" for i in range(40)], "id": rng.choice(ids, 40, replace=False),
                           "day0": dates[ev_days]})
    # plant the effect
    px2 = prices.copy()
    for ev in events.itertuples():
        for k in (0, 1):
            d = dates[list(dates).index(pd.Timestamp(ev.day0)) + k]
            px2.loc[(px2.id == ev.id) & (px2.date == d), "ret"] += 0.01
    arl = factor_model_ar(px2, factors, events)
    c = car(arl, 0, 1)
    t, p = bmp_test(c.scar.values)
    tadj, padj, rbar = kp_adjusted_t(c.scar.values, arl)
    print(f"mean CAR[0,1] = {100*c.car.mean():.2f}% (planted 2.00%), BMP t = {t:.2f}, KP t = {tadj:.2f}, rbar = {rbar:.3f}")
    dose = rng.normal(0, 1, len(c))
    y = c.car.values + 0.005 * dose
    X = np.column_stack([np.ones(len(y)), dose])
    res = cluster_ols(y, X, cluster=np.arange(len(y)) % 8, n_boot=299)
    ri = ri_slope(y, dose, group=np.arange(len(y)) % 8, n_perm=500)
    print(f"slope on dose = {res['beta'][1]:.4f} (planted 0.0050), cluster t = {res['t']:.2f}, wild p = {res['p_boot']:.3f}, RI p = {ri['p_ri']:.3f}")
