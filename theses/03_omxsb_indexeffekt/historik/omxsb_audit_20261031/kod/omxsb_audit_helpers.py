"""Small, tested measurement helpers shared by the OMXSB replication and audit."""
import numpy as np
import pandas as pd

def yearly_median_inference(s, value, B=9999, seed=20261031):
    """Equal-year mean of medians; pairs bootstrap whole reviews within each year.

    Conditions on the observed years. With only 1--2 reviews/year intervals have
    limited support; no pooled-mean SE or p-value is attached to this estimand.
    """
    s = s.dropna(subset=[value, "adx", "year"])
    rng = np.random.default_rng(seed)
    boot = np.zeros(B)
    years = list(s.groupby("year"))
    for _, y in years:
        groups = [g[value].to_numpy() for _, g in y.groupby("adx")]
        picks = rng.integers(0, len(groups), size=(B, len(groups)))
        # At most two scheduled OMXSB reviews/year: cache repeated selections.
        choices, inv = np.unique(picks, axis=0, return_inverse=True)
        med = np.array([np.median(np.concatenate([groups[j] for j in ii])) for ii in choices])
        boot += med[inv] / len(years)
    lo, hi = np.quantile(boot, [.025, .975])
    return dict(mean=float(s.groupby("year")[value].median().mean()), N=len(s), G=s.adx.nunique(),
                ci_low=float(lo), ci_high=float(hi), se_cluster_boot=float(boot.std(ddof=1)),
                ci_method="95% review-pairs bootstrap within year, 9999 draws; fixed years; few reviews/year",
                se_hc1=np.nan, se_cr1=np.nan, p_hc1=np.nan, p_cr1=np.nan, p_wcb=np.nan)

def matched_fund_totals(e, own_b, own_a, presence, idx):
    """Same reporting funds at both endpoints; missing whole report is never zero."""
    out = []
    for r in e.itertuples():
        both = presence[r.qb] & presence[r.qa]
        b, a = own_b[r.event_id], own_a[r.event_id]
        rec = dict(event_id=r.event_id, n_reporting_both=len(both))
        for prefix, ids in [("idx", both & idx), ("act", both - idx), ("all", both)]:
            rec[prefix+"_b"] = float(b[b.index.isin(ids)].sum()) * r.f
            rec[prefix+"_a"] = float(a[a.index.isin(ids)].sum())
        rec["entry_holdings_a"] = float(a[~a.index.isin(presence[r.qb])].sum())
        rec["exit_holdings_b"] = float(b[~b.index.isin(presence[r.qa])].sum()) * r.f
        out.append(rec)
    return pd.DataFrame(out).set_index("event_id")
