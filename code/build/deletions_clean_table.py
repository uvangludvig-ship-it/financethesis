import os, json
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "output", "omxsb_replication_2007")
TAB = os.path.join(OUT, "tables")
PER = ["2007–2012", "2013–2017", "2018–2020", "2021–2023", "2024–2026"]

nb = json.load(open(os.path.join(REPO, "code", "notebooks", "replication_omxsb_2007.ipynb")))
src = next(''.join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code" and "def wcb(" in ''.join(c["source"]))
ns = {"np": np, "pd": pd, "stats": stats, "PER": PER}
exec(src.split("rows = []")[0], ns)
cell = ns["cell"]

ev = pd.read_csv(os.path.join(OUT, "events_car.csv"))
rs = pd.read_csv(os.path.join(REPO, "data", "input", "omxsb", "deletion_reasons_2007_2026.csv"))
d = ev[ev.type == "deletion"].merge(rs[["event_id", "deletion_reason"]], on="event_id", how="left")
d["adx"] = d.AD.astype(str)
flag = d.deletion_reason.fillna("review_only") != "review_only"
rows = []
for win in ["ann", "eff", "tot"]:
    for p in PER:
        for lab, s in [("all", d[d.period == p]), ("clean", d[(d.period == p) & ~flag])]:
            s = s.dropna(subset=[win])
            rows.append(dict(window=win, period=p, sample=lab, n_flagged=int(flag[(d.period == p)].sum()) if lab == "all" else 0, **cell(s[win], s.adx)))
t = pd.DataFrame(rows)
t.to_csv(os.path.join(TAB, "tabA_10_deletions_clean_long.csv"), index=False)

def fmt(r):
    st = "***" if r.p_hc1 < 0.01 else "**" if r.p_hc1 < 0.05 else "*" if r.p_hc1 < 0.1 else ""
    return f"{r['mean']:.2f}{st} ({r.se_hc1:.2f}) [{r.se_cr1:.2f}] {{{r.p_wcb:.3f}}} N={int(r.N)}"
lines = ["# Deletions: Table 2 with and without events flagged for a corporate event in the window", "",
         "Flagged = public offer, bankruptcy or reconstruction, merger or acquirer, delisting application, or distressed equity issue between AD−30 and ED+100 calendar days (`data/input/omxsb/deletion_reasons_2007_2026.csv`, 20 of 225 deletions). Cells: mean CAR in percent against .OMXSBGI, stars from HC1 p, HC1 SE in parentheses, CR1 SE (clustered on announcement date) in brackets, wild cluster bootstrap p in braces.", ""]
for win, nm in [("ann", "Announcement window [AD−1, AD+1]"), ("eff", "Effective window [ED−1, ED+1]"), ("tot", "Total window [AD−1, ED+1]")]:
    lines += [f"## {nm}", "", "| Period | All deletions | Flagged | Without flagged |", "|---|---|---|---|"]
    for p in PER:
        a = t[(t.window == win) & (t.period == p) & (t["sample"] == "all")].iloc[0]
        c = t[(t.window == win) & (t.period == p) & (t["sample"] == "clean")].iloc[0]
        lines.append(f"| {p} | {fmt(a)} | {int(a.n_flagged)} | {fmt(c)} |")
    lines.append("")
open(os.path.join(OUT, "table2_deletions_clean.md"), "w").write("\n".join(lines))
print("\n".join(lines))
