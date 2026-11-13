"""Table 2 under every equidistant period length: 1, 2, 4, 5, 10 and 20 calendar years of effective dates
(the divisors of the 20-year sample 2007-2026, so that every period has the same length; 2026 holds only
the June review). Reads output/omxsb_replication_2007/events_car.csv, reuses the notebook's inference
functions (HC1, CR1 clustered on announcement date, wild cluster bootstrap) and writes
output/omxsb_replication_2007/period_sensitivity/ (long csv, one markdown table per length, a trend table
and a figure). No FTN return is computed."""
import os, json
import numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT0 = os.path.join(REPO, "output", "omxsb_replication_2007")
OUT = os.path.join(OUT0, "period_sensitivity")
os.makedirs(OUT, exist_ok=True)
Y0, Y1 = 2007, 2026
LENGTHS = [L for L in range(1, Y1 - Y0 + 2) if (Y1 - Y0 + 1) % L == 0]  # 1, 2, 4, 5, 10, 20
WIN = {"ann": "Announcement window [AD−1, AD+1]", "eff": "Effective window [ED−1, ED+1]", "tot": "Total window [AD−1, ED+1]"}

nb = json.load(open(os.path.join(REPO, "code", "notebooks", "replication_omxsb_2007.ipynb")))
src = next("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code" and "def wcb(" in "".join(c["source"]))
ns = {"np": np, "pd": pd, "stats": stats, "PER": []}
exec(src.split("rows = []")[0], ns)
ols, wcb, cell, ftest = ns["ols"], ns["wcb"], ns["cell"], ns["ftest"]

ev = pd.read_csv(os.path.join(OUT0, "events_car.csv"), parse_dates=["AD", "ED"])
assert len(ev) == 487, len(ev)
ev["adx"] = ev.AD.dt.strftime("%Y-%m-%d")
ev["year"] = ev.ED.dt.year
assert ev.year.between(Y0, Y1).all()

def periods(L):
    starts = list(range(Y0, Y1 + 1, L))
    labels = [f"{a}–{a + L - 1}" if L > 1 else str(a) for a in starts]
    return starts, labels, pd.cut(ev.year, [a - 1 for a in starts] + [Y1], labels=labels).astype(str)

def trend(s, col, pers):
    s = s.dropna(subset=[col])
    y = s[col].values.astype(float)
    X = np.column_stack([np.ones(len(y)), s.per.map({p: i for i, p in enumerate(pers)}).values.astype(float)])
    b, e, Vh, Vc, G, gs, _ = ols(y, X, s.adx.values)
    t, pw, G = wcb(y, X, s.adx.values, [0.0, 1.0])
    return dict(slope_per_period=b[1], se_cr1=np.sqrt(Vc[1, 1]), p_cr1=2 * stats.t.sf(abs(b[1] / np.sqrt(Vc[1, 1])), G - 1), p_wcb=pw, N=len(y), G=G)

rows, trows, md = [], [], ["# Table 2 under every equidistant period length", "",
    f"Sample: the {len(ev)} OMXSB events of `events_car.csv` (2007–2026), period = calendar year of the effective date. Lengths are the divisors of the 20-year window so every period has the same length; 2026 contains only the June review. Cells: mean CAR in percent against .OMXSBGI, stars from the HC1 p-value, HC1 SE in parentheses, SE clustered on announcement date in brackets, wild cluster bootstrap p in braces, N. F = cluster-robust F for equal means across the periods (p from F(k−1, G−1)). Trend = OLS of the CAR on the period index, slope per period and per year, CR1 SE, p from t(G−1) and the wild bootstrap. For one period the F-test and the trend do not exist; with one-year periods three periods (2007, 2010, 2026) contain a single announcement date, so their clustered SE and bootstrap p are n/a and the F-test is singular.", ""]
def star(p): return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
def fmt(r): return f"{r['mean']:.2f}{star(r.p_hc1)} ({r.se_hc1:.2f}) " + (f"[{r.se_cr1:.2f}] {{{r.p_wcb:.3f}}}" if np.isfinite(r.se_cr1) else "[n/a] {n/a}") + f" N={int(r.N)}"
for L in LENGTHS:
    starts, pers, ev["per"] = periods(L)
    md += [f"## Period length {L} year{'s' if L > 1 else ''}: {len(pers)} period{'s' if len(pers) > 1 else ''}", ""]
    for typ in ["addition", "deletion"]:
        s = ev[ev.type == typ]
        tab = []
        for w in ["ann", "eff", "tot"]:
            line = {"Window": WIN[w]}
            for p in pers:
                c = s[s.per == p]
                r = dict(length=L, n_periods=len(pers), type=typ, window=w, period=p, **cell(c[w], c.adx))
                if r["G"] < 2:  # one announcement date in the period: no clustered SE and no bootstrap
                    r["se_cr1"] = r["p_cr1"] = r["p_wcb"] = np.nan
                rows.append(r); line[p] = fmt(pd.Series(r))
            if len(pers) > 1:
                gmin = min(int(s[(s.per == p) & s[w].notna()].adx.nunique()) for p in pers)
                if gmin >= 2:
                    F, pF, G = ftest(s[w], s.adx, s.per, pers)
                else:  # a period with a single cluster makes the clustered covariance singular
                    F, pF, G = np.nan, np.nan, int(s[s[w].notna()].adx.nunique())
                rows.append(dict(length=L, n_periods=len(pers), type=typ, window=w, period="F_equal", mean=F, p_cr1=pF, N=int(s[w].notna().sum()), G=G))
                line["F, equal means"] = f"{F:.2f} (p = {pF:.3f})" if np.isfinite(F) else "n/a (a period has one cluster)"
                tr = trend(s, w, pers)
                trows.append(dict(length=L, n_periods=len(pers), type=typ, window=w, **tr, slope_per_year=tr["slope_per_period"] / L))
                line["Trend per year"] = f"{tr['slope_per_period'] / L:.2f} (p = {tr['p_cr1']:.3f}; wcb {tr['p_wcb']:.3f})"
            tab.append(line)
        df = pd.DataFrame(tab)
        md += [f"**{typ.capitalize()}s**", "", "| " + " | ".join(df.columns) + " |", "|" + "---|" * len(df.columns)]
        md += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.values.tolist()]
        md.append("")
long = pd.DataFrame(rows); long.to_csv(os.path.join(OUT, "table2_by_period_length_long.csv"), index=False)
tr = pd.DataFrame(trows); tr.to_csv(os.path.join(OUT, "trend_by_period_length.csv"), index=False)
md += ["## Trend slope per year by period length (total window)", "", "| Length | Periods | Additions: slope/yr (CR1 SE) p, wcb p | Deletions: slope/yr (CR1 SE) p, wcb p | F adds (p) | F dels (p) |", "|---|---|---|---|---|---|"]
for L in [L for L in LENGTHS if L < Y1 - Y0 + 1]:
    a = tr[(tr.length == L) & (tr.type == "addition") & (tr.window == "tot")].iloc[0]
    d = tr[(tr.length == L) & (tr.type == "deletion") & (tr.window == "tot")].iloc[0]
    Fa = long[(long.length == L) & (long.type == "addition") & (long.window == "tot") & (long.period == "F_equal")].iloc[0]
    Fd = long[(long.length == L) & (long.type == "deletion") & (long.window == "tot") & (long.period == "F_equal")].iloc[0]
    fF = lambda r: f"{r['mean']:.2f} ({r.p_cr1:.3f})" if np.isfinite(r["mean"]) else "n/a"
    md.append(f"| {L} | {int(a.n_periods)} | {a.slope_per_year:.3f} ({a.se_cr1 / L:.3f}) {a.p_cr1:.3f}, {a.p_wcb:.3f} | {d.slope_per_year:.3f} ({d.se_cr1 / L:.3f}) {d.p_cr1:.3f}, {d.p_wcb:.3f} | {fF(Fa)} | {fF(Fd)} |")
open(os.path.join(OUT, "RESULTS.md"), "w").write("\n".join(md) + "\n")

# figure: mean total-window CAR as a step function of time for each length
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
cols = plt.cm.viridis(np.linspace(0, 0.9, len(LENGTHS)))
for ax, typ in zip(axs, ["addition", "deletion"]):
    for L, c in zip(LENGTHS, cols):
        starts, pers, _ = periods(L)
        m = long[(long.length == L) & (long.type == typ) & (long.window == "tot") & long.period.isin(pers)].set_index("period").reindex(pers)["mean"].values
        xs = np.repeat(np.array(starts + [Y1 + 1]), 2)[1:-1]
        ax.plot(xs, np.repeat(m, 2), color=c, lw=1.2 if L > 1 else 0.8, label=f"{L} yr")
    ax.axhline(0, color="k", lw=0.5); ax.set_title(f"{typ.capitalize()}s: mean CAR [AD−1, ED+1] (%)"); ax.set_xlabel("Year of effective date")
axs[0].legend(title="Period length", fontsize=8, ncol=2)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_car_by_period_length.png"), dpi=200); fig.savefig(os.path.join(OUT, "fig_car_by_period_length.pdf"))
print(open(os.path.join(OUT, "RESULTS.md")).read())
