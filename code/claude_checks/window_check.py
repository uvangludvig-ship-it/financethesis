"""Equal-length windows vs G&S total window, OMXSB 2007-2026.

Usage:
  python3 window_check.py <repo>/output/omxsb_replication_2007

Part A uses figures/fig_08_car_announcement.csv (mean CAR path from AD-100 to
AD+10, normalised to 0 at AD+10). The value at day -1 therefore equals
-CAR[AD, AD+10]. These are plain event means by period, no clustered test.

Part B uses events_car.csv (ann = [AD-1, AD+1], eff = [ED-1, ED+1],
tot = [AD-1, ED+1]); mid = tot - ann - eff is the drift between the two
windows. Split by Nasdaq lead-time regime (AD before / from May 2021) and
tested with review-mean sign-flip randomisation (review = AD).
"""
import sys, os
import numpy as np
import pandas as pd

base = sys.argv[1]
rng = np.random.default_rng(1)

# ---------- Part A: fixed window [AD, AD+10] from figure data ----------
a = pd.read_csv(os.path.join(base, "figures", "fig_08_car_announcement.csv"),
                header=[0, 1], index_col=0)
a.index = a.index.astype(float).astype(int)
fixed = (-a.loc[-1]).round(2)
print("A. Mean CAR[AD, AD+10] by period (event means, untested)")
print(fixed.to_string())

# ---------- Part B: regime split with sign-flip test ----------
e = pd.read_csv(os.path.join(base, "events_car.csv"), parse_dates=["AD", "ED"])
e["mid"] = e.tot - e.ann - e.eff
e["gap"] = np.busday_count(e.AD.values.astype("datetime64[D]"),
                           e.ED.values.astype("datetime64[D]"))

def signflip(s, g, n=20000):
    m = s.groupby(g).mean().dropna()
    t = m.mean()
    sims = np.array([(m * rng.choice([-1, 1], len(m))).mean() for _ in range(n)])
    return f"{t:+.2f} (p {(np.abs(sims) >= abs(t)).mean():.3f}, G {len(m)})"

print("\nTrading days AD->ED by year (min/max)")
print(e.groupby(e.AD.dt.year).gap.agg(["min", "max"]).T.to_string())

print("\nB. Windows by lead-time regime, review-mean sign-flip")
regimes = [("2007-2016", e.AD < "2017-01-01"),
           ("2017-Apr2021 (15 days)", (e.AD >= "2017-01-01") & (e.AD < "2021-05-01")),
           ("May2021-2026 (6-7 days)", e.AD >= "2021-05-01")]
for ty in ["addition", "deletion"]:
    for lab, c in regimes:
        x = e[(e.type == ty) & c]
        print(f"{ty:8s} {lab:24s} gap {int(x.gap.median()):2d} | "
              f"ann {signflip(x.ann, x.AD)} | mid {signflip(x.mid, x.AD)} | "
              f"eff {signflip(x.eff, x.AD)} | tot {signflip(x.tot, x.AD)}")
