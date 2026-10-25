"""
power.py: minimum detectable effects for every table, from assumptions now and from the actual dose file later.

MDE for a slope at power 0.8, size 0.05 (two-sided): 2.8 * sigma_y / (sigma_x * sqrt(N)).
MDE for a mean: 2.8 * sigma_y / sqrt(N).
Run with no arguments for the assumption-based table in 01_DESIGN.md 5.4; run with --dose ../output/dose_stock_tranche.csv
once pressure.py has produced the actual doses (still no returns involved).
"""
import sys, argparse
import numpy as np
import pandas as pd


def mde_slope(sigma_y, sigma_x, n):
    return 2.8 * sigma_y / (sigma_x * np.sqrt(n))


def mde_mean(sigma_y, n):
    return 2.8 * sigma_y / np.sqrt(n)


def assumption_table():
    rows = [
        # name, sigma_CAR (%), sigma_x (days of ADV), N, predicted effect (% per day of ADV at x=1 from sqrt law)
        ("SE active, tranche-day [-1,+1], large caps", 3.0, 0.02, 2000, 1.0),
        ("SE active, round window [first-1,last+1]", 6.0, 0.6, 200, 1.0),
        ("SE small cap, tranche-day [-1,+1]", 5.0, 0.5, 750, 2.0),
        ("SE small cap, round window", 8.0, 3.0, 150, 2.0),
        ("Nordic active, round window", 6.0, 0.1, 150, 1.0),
        ("SE index, round window (low dose)", 5.0, 0.05, 400, 1.0),
        ("Pooled rounds, round window", 6.5, 1.2, 500, 1.3),
    ]
    out = []
    for name, sy, sx, n, pred in rows:
        out.append({"test": name, "sigma_CAR_pct": sy, "sigma_x_days": sx, "N": n,
                    "MDE_slope_pct_per_day": round(mde_slope(sy, sx, n), 2), "MDE_mean_pct": round(mde_mean(sy, n), 2),
                    "sqrt_law_prediction_pct": pred, "powered": mde_slope(sy, sx, n) <= pred})
    df = pd.DataFrame(out)
    # beta = 1 test on the square-root prediction scale, pooled
    n, sig_pi, sy = 2500, 0.5, 3.0
    se_beta = sy / (sig_pi * np.sqrt(n))
    print(df.to_string(index=False))
    print(f"\nEquation (9), pooled stock-days N={n}: s.e. of beta on pi_hat about {se_beta:.2f}; beta=1 vs 0 is {1/se_beta:.1f} s.e.")
    # replication
    for per, n_ev in [("2013-17", 90), ("2018-20", 80), ("2021-23", 100), ("2024-26", 85)]:
        print(f"Table 2 {per}: N={n_ev} events, sigma_CAR(ann->eff, ~8 days) 4.5%: MDE mean = {mde_mean(4.5, n_ev):.2f}%")
    # incidence
    print(f"Table 5 index losers: 8 funds x 10 tranche days, daily tracking error 4 bp: s.e. of mean = {4/np.sqrt(80):.2f} bp; predicted 2 to 3 bp per tranche")
    print(f"Table 5 active losers: 18 funds x 2.5 tranches, daily noise 40 bp: s.e. of mean = {40/np.sqrt(45):.1f} bp; predicted 5 to 8 bp per tranche")
    return df


def from_dose(path):
    d = pd.read_csv(path)
    for col in ["x_net", "x_sell", "pi_hat"]:
        if col in d:
            s = d[col].dropna()
            print(f"{col}: N={len(s)}, sd={s.std():.3f}, p90 |.|={s.abs().quantile(.9):.3f}")
    if "pi_hat" in d:
        s = d["pi_hat"].dropna() * 100
        for sy in (3.0, 5.0):
            print(f"sigma_CAR={sy}%: s.e.(beta on pi_hat) = {sy/(s.std()*np.sqrt(len(s))):.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--dose", default=None)
    a = ap.parse_args()
    assumption_table()
    if a.dose:
        from_dose(a.dose)
