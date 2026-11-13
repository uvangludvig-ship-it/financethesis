"""Formal tests of a time trend in the OMXSB index effect, bin-free and for every equidistant period length.

Bin-free (do not depend on how years are grouped):
  T1  OLS of the event CAR on calendar time (years since 2007, effective date), SE clustered on announcement
      date (CR1), p from t(G-1), and the wild cluster bootstrap p with the null imposed.
  T2  Review-level: mean CAR per review (38 reviews) regressed on time, HC1 p; and Spearman rank correlation
      between review date and review mean.
  T3  Mann-Kendall: Kendall's tau between event time and CAR, normal-approximation p (events treated as
      independent, so this ignores the clustering and is reported as a descriptive test).
  T4  Sup-Wald test for a single break in the mean at an unknown review boundary (at least 5 reviews on each
      side), Wald with CR1 variance, p from the wild cluster bootstrap under the no-break null (999 draws).
Per period length L in {1, 2, 4, 5, 10}:
  P1  OLS of the CAR on the period index (slope per period; also per year), CR1 and wild bootstrap p.
  P2  Jonckheere-Terpstra test for an ordered alternative across the periods (computed as Kendall's tau between
      the period index and the CAR; identical ordering statistic), normal-approximation p.
  P3  Spearman between the period index and the period mean (k points).
  P4  Sup-Wald break test with the break restricted to the period boundaries (at least 5 reviews on each side, as in T4), wild cluster bootstrap p.
Reads output/omxsb_replication_2007/events_car.csv; writes period_sensitivity/TREND_TESTS.md and .csv."""
import os, json
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT0 = os.path.join(REPO, "output", "omxsb_replication_2007")
OUT = os.path.join(OUT0, "period_sensitivity")
Y0, Y1 = 2007, 2026
LENGTHS = [1, 2, 4, 5, 10]
WIN = {"ann": "Announcement [AD−1, AD+1]", "eff": "Effective [ED−1, ED+1]", "tot": "Total [AD−1, ED+1]"}
B = 999
rng = np.random.default_rng(0)

nb = json.load(open(os.path.join(REPO, "code", "notebooks", "replication_omxsb_2007.ipynb")))
src = next("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code" and "def wcb(" in "".join(c["source"]))
ns = {"np": np, "pd": pd, "stats": stats, "PER": []}
exec(src.split("rows = []")[0], ns)
ols, wcb = ns["ols"], ns["wcb"]

ev = pd.read_csv(os.path.join(OUT0, "events_car.csv"), parse_dates=["AD", "ED"])
assert len(ev) == 487
ev["adx"] = ev.AD.dt.strftime("%Y-%m-%d")
ev["t"] = (ev.ED - pd.Timestamp("2007-01-01")).dt.days / 365.25
ev["year"] = ev.ED.dt.year

def ols_trend(s, x):
    y = s.values.astype(float) if hasattr(s, "values") else s
    X = np.column_stack([np.ones(len(y)), x])
    return X, y

def sup_wald(y, g, order, cand):
    """Single break in the mean. y, g (cluster id), order (time) per observation; cand = list of boolean
    'post' masks (one per candidate break). Returns max Wald, its candidate index, and the wild cluster
    bootstrap p under the null of a constant mean. CR1 variance with the notebook's small-sample factor."""
    y = np.asarray(y, float); g = pd.factorize(g)[0]; G = g.max() + 1; n = len(y)
    mu = y.mean(); e = y - mu
    S = np.bincount(g, weights=e, minlength=G); ng = np.bincount(g, minlength=G)
    # cluster membership per candidate: clusters are whole announcement dates, so each cluster is pre or post
    post_c = np.array([np.bincount(g, weights=m.astype(float), minlength=G) > 0 for m in cand])  # (C, G)
    def wald_all(ystar_sum_g):  # ystar_sum_g: (D, G) cluster sums of y*
        W = np.empty((ystar_sum_g.shape[0], len(cand)))
        for ci, pc in enumerate(post_c):
            npre, npost = ng[~pc].sum(), ng[pc].sum()
            bpre = ystar_sum_g[:, ~pc].sum(1) / npre; bpost = ystar_sum_g[:, pc].sum(1) / npost
            # cluster residual sums: sum_i (y*_i - b_group) over the cluster
            R = ystar_sum_g - np.where(pc, bpost[:, None], bpre[:, None]) * ng
            corr = G / (G - 1) * (n - 1) / (n - 2)
            v = (R[:, ~pc] ** 2).sum(1) / npre ** 2 + (R[:, pc] ** 2).sum(1) / npost ** 2
            W[:, ci] = (bpost - bpre) ** 2 / (v * corr)
        return W
    W0 = wald_all((np.bincount(g, weights=y, minlength=G))[None, :])[0]
    w = rng.choice(np.array([-1.0, 1.0]), size=(B, G)) if G >= 12 else rng.choice(np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)]), size=(B, G))
    Wb = wald_all(ng[None, :] * mu + w * S[None, :]).max(1)
    k = int(np.argmax(W0))
    return W0[k], k, float(np.mean(Wb >= W0[k]))

rows = []
for typ in ["addition", "deletion"]:
    for win in ["ann", "eff", "tot"]:
        s = ev[(ev.type == typ)].dropna(subset=[win]).sort_values("ED")
        y = s[win].values.astype(float); g = s.adx.values
        # T1 continuous trend
        X = np.column_stack([np.ones(len(y)), s.t.values])
        b, e, Vh, Vc, G, gs, _ = ols(y, X, g)
        t_, pw, G = wcb(y, X, g, [0.0, 1.0])
        rows.append(dict(type=typ, window=win, length="bin-free", test="T1 OLS on calendar time (per year)", stat=b[1], se=np.sqrt(Vc[1, 1]), p=2 * stats.t.sf(abs(b[1] / np.sqrt(Vc[1, 1])), G - 1), p_boot=pw, N=len(y), G=G))
        # T2 review-level
        r = s.groupby("adx").agg(m=(win, "mean"), t=("t", "first"), n=(win, "size"))
        Xr = np.column_stack([np.ones(len(r)), r.t.values]); br, er, Vhr, _, _, _, _ = ols(r.m.values, Xr, np.arange(len(r)))
        rows.append(dict(type=typ, window=win, length="bin-free", test="T2a review means on time (per year), HC1", stat=br[1], se=np.sqrt(Vhr[1, 1]), p=2 * stats.norm.sf(abs(br[1] / np.sqrt(Vhr[1, 1]))), p_boot=np.nan, N=len(r), G=len(r)))
        rho, prho = stats.spearmanr(r.t, r.m)
        rows.append(dict(type=typ, window=win, length="bin-free", test="T2b Spearman, review date vs review mean", stat=rho, se=np.nan, p=prho, p_boot=np.nan, N=len(r), G=len(r)))
        # T3 Mann-Kendall
        tau, ptau = stats.kendalltau(s.t, y)
        rows.append(dict(type=typ, window=win, length="bin-free", test="T3 Mann-Kendall tau, event time vs CAR (no clustering)", stat=tau, se=np.nan, p=ptau, p_boot=np.nan, N=len(y), G=G))
        # T4 sup-Wald at review boundaries
        revs = sorted(s.adx.unique()); cand = [(s.adx.values > revs[i]).astype(bool) for i in range(4, len(revs) - 5)]
        Wmax, k, pb = sup_wald(y, g, s.t.values, cand)
        brk = s[s.adx == revs[k + 4]].ED.iloc[0]; post = cand[k]
        rows.append(dict(type=typ, window=win, length="bin-free", test=f"T4 sup-Wald single break (break after {brk.date()} review; pre {y[~post].mean():.2f}, post {y[post].mean():.2f})", stat=Wmax, se=np.nan, p=np.nan, p_boot=pb, N=len(y), G=G))
        # per length
        for L in LENGTHS:
            starts = list(range(Y0, Y1 + 1, L)); idx = ((s.year - Y0) // L).values.astype(float)
            X = np.column_stack([np.ones(len(y)), idx]); b, e, Vh, Vc, G, gs, _ = ols(y, X, g); t_, pw, G = wcb(y, X, g, [0.0, 1.0])
            rows.append(dict(type=typ, window=win, length=L, test="P1 OLS on period index (slope per period)", stat=b[1], se=np.sqrt(Vc[1, 1]), p=2 * stats.t.sf(abs(b[1] / np.sqrt(Vc[1, 1])), G - 1), p_boot=pw, N=len(y), G=G, per_year=b[1] / L))
            tau, ptau = stats.kendalltau(idx, y)
            rows.append(dict(type=typ, window=win, length=L, test="P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR)", stat=tau, se=np.nan, p=ptau, p_boot=np.nan, N=len(y), G=G))
            pm = pd.Series(y).groupby(idx).mean()
            if len(pm) > 2:
                rho, prho = stats.spearmanr(pm.index, pm.values)
                rows.append(dict(type=typ, window=win, length=L, test="P3 Spearman, period index vs period mean", stat=rho, se=np.nan, p=prho, p_boot=np.nan, N=len(pm), G=len(pm)))
            thr = [i for i in range(int(idx.max())) if s.adx[idx <= i].nunique() >= 5 and s.adx[idx > i].nunique() >= 5]  # same trimming as T4: at least 5 reviews on each side
            cand = [(idx > i).astype(bool) for i in thr]
            if cand:
                Wmax, k, pb = sup_wald(y, g, s.t.values, cand); post = cand[k]
                yr = Y0 + L * (thr[k] + 1)
                rows.append(dict(type=typ, window=win, length=L, test=f"P4 sup-Wald break at a period boundary (break before {yr}; pre {y[~post].mean():.2f}, post {y[post].mean():.2f})", stat=Wmax, se=np.nan, p=np.nan, p_boot=pb, N=len(y), G=G))
res = pd.DataFrame(rows); res.to_csv(os.path.join(OUT, "trend_tests.csv"), index=False)

def f(v, d=3): return "" if pd.isna(v) else f"{v:.{d}f}"
md = ["# Trend tests: bin-free and for every equidistant period length", "", __doc__.split("\n", 1)[1].strip(), "", "Sample: 487 OMXSB events 2007–2026 (`events_car.csv`), CAR in percent against .OMXSBGI. Stat = slope, tau, rho or sup-Wald; p = analytical p (CR1 t for OLS, normal for tau and HC1, exact/approx for Spearman); p_boot = wild cluster bootstrap with the null imposed. A negative slope for additions and a positive one for deletions means the effect shrinks.", ""]
for win in ["tot", "ann", "eff"]:
    md += [f"## {WIN[win]}", ""]
    for typ in ["addition", "deletion"]:
        u = res[(res.type == typ) & (res.window == win)]
        md += [f"**{typ.capitalize()}s**", "", "| Length | Test | Stat | SE | p | p_boot | per year | N | G |", "|---|---|---|---|---|---|---|---|---|"]
        for _, r in u.iterrows():
            md.append(f"| {r.length} | {r.test} | {f(r.stat)} | {f(r.se)} | {f(r.p)} | {f(r.p_boot)} | {f(r.get('per_year'))} | {int(r.N)} | {int(r.G)} |")
        md.append("")
open(os.path.join(OUT, "TREND_TESTS.md"), "w").write("\n".join(md) + "\n")
pd.set_option("display.width", 250, "display.max_colwidth", 90)
print(res[res.window == "tot"][["type", "length", "test", "stat", "se", "p", "p_boot", "per_year"]].to_string(index=False))
