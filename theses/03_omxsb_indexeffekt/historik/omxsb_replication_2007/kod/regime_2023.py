"""Announcement-timing regimes: did the index effect change after Nov 2023, when the announcement lead became
exactly six trading days under the rulebook? Regimes (from omxsb_notes.md section 4): intraday releases 2007-2012
(lead 7-17); pre-open 08:30 releases 2013-2020 (lead 14-17); after-close releases May 2021-May 2023 (lead 7-8);
after-close, exactly six trading days, Nov 2023-2026. Mean CAR per regime and the difference between the last two,
with HC1, CR1 (clustered on announcement date) and wild cluster bootstrap p. Writes period_sensitivity/REGIMES.md."""
import os, json
import numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT0 = os.path.join(REPO, "output", "omxsb_replication_2007"); OUT = os.path.join(OUT0, "period_sensitivity")
nb = json.load(open(os.path.join(REPO, "code", "notebooks", "replication_omxsb_2007.ipynb")))
src = next("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code" and "def wcb(" in "".join(c["source"]))
ns = {"np": np, "pd": pd, "stats": stats, "PER": []}; exec(src.split("rows = []")[0], ns)
cell, diffcell = ns["cell"], ns["diffcell"]
ev = pd.read_csv(os.path.join(OUT0, "events_car.csv"), parse_dates=["AD", "ED", "announcement_date"])
ev["adx"] = ev.AD.dt.strftime("%Y-%m-%d")
cuts = [("2007-01-01", "2012-12-31", "R1 intraday release, lead 7–17 (2007–2012)"), ("2013-01-01", "2020-12-31", "R2 pre-open 08:30, lead 14–17 (2013–2020)"),
        ("2021-01-01", "2023-10-31", "R3 after close, lead 7–8 (May 2021–May 2023)"), ("2023-11-01", "2026-12-31", "R4 after close, exactly 6 (Nov 2023–2026)")]
ev["regime"] = None
for a, b, lab in cuts: ev.loc[ev.announcement_date.between(a, b), "regime"] = lab
assert ev.regime.notna().all()
def star(p): return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
def fmt(r): return f"{r['mean']:.2f}{star(r['p_hc1'])} ({r['se_hc1']:.2f}) [{r['se_cr1']:.2f}] {{{r['p_wcb']:.3f}}} N={int(r['N'])} G={int(r['G'])}"
md = ["# Announcement-timing regimes and the Nov 2023 change to an exact six-day lead", "", __doc__.strip(), "", "Cell: mean CAR % against .OMXSBGI, stars HC1 p, (HC1 SE) [CR1 SE] {wild cluster bootstrap p} N events G reviews.", ""]
rows = []
for typ in ["addition", "deletion"]:
    md += [f"## {typ.capitalize()}s", "", "| Window | " + " | ".join(l for _, _, l in cuts) + " | R4 − R3 | R4 − R2 |", "|---|---|---|---|---|---|---|"]
    s = ev[ev.type == typ]
    for w, wl in [("ann", "Announcement [AD−1, AD+1]"), ("eff", "Effective [ED−1, ED+1]"), ("tot", "Total [AD−1, ED+1]")]:
        line = [wl]
        for _, _, lab in cuts:
            c = s[s.regime == lab]; r = cell(c[w], c.adx); rows.append(dict(type=typ, window=w, regime=lab, **r)); line.append(fmt(r))
        for base in [cuts[2][2], cuts[1][2]]:
            c = s[s.regime.isin([base, cuts[3][2]])]; r = diffcell(c[w], c.adx, (c.regime == cuts[3][2]).values.astype(float))
            rows.append(dict(type=typ, window=w, regime=f"R4 − {base[:2]}", **r)); line.append(fmt(r))
        md.append("| " + " | ".join(line) + " |")
    md.append("")
pd.DataFrame(rows).to_csv(os.path.join(OUT, "regimes.csv"), index=False)
open(os.path.join(OUT, "REGIMES.md"), "w").write("\n".join(md) + "\n"); print("\n".join(md))
