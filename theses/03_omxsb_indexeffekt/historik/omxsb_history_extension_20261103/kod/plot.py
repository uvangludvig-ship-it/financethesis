"""Render the already computed historical volume summaries; no new estimates."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

p = argparse.ArgumentParser()
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
d = pd.read_csv(a.output/"PROVISIONAL_COMBINED_SUMMARY.csv")
d = d[d.metric.eq("volume_share_edm1") & d.period.ne("All")]
fig, ax = plt.subplots(figsize=(8.2, 4.8))
ax.axvspan(-.4, .4, color="#eeeeee", zorder=0)
for typ, name, color, offset in [("addition", "Tillägg", "#275b96", -.07),
                                  ("deletion", "Borttag", "#ba5736", .07)]:
    x = d[d.type.eq(typ)].reset_index(drop=True)
    pos = np.arange(len(x)) + offset
    ax.errorbar(pos, x.mean_review, yerr=[x.mean_review-x.ci_low, x.ci_high-x.mean_review],
                fmt="o-", color=color, label=name, capsize=4, linewidth=1.5)
ax.set_xticks(range(5), ["2003–06*", "2007–11", "2012–16", "2017–21", "2022–26"])
ax.set_ylim(0, 20)
ax.set_ylabel("Handelsdagens andel av 45 dagars volym (%)")
ax.set_title("Mer handel koncentreras till dagen före indexbytet", loc="left", fontsize=13, pad=16)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=.2)
ax.legend(frameon=False, loc="upper left")
fig.text(.12, .015, "Lika vikt per översyn; nominella 95 % intervall. *Äldre datum är preliminära.\n"
         "Kompletta volymfönster; olika bolag över tid. Diagrammet identifierar ingen prismekanism.", fontsize=8)
fig.tight_layout(rect=(0, .08, 1, 1))
fig.savefig(a.output/"VOLUME_HISTORY.png", dpi=180)
fig.savefig(a.output/"VOLUME_HISTORY.pdf")
