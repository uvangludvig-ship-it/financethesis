# Figur 1 (G&S Figure 1): indexfondernas nettoköp och nettoförsäljning per år, i procent av aktierna.
# Ur results/fund_demand/figur1_skikt.csv (02): D_V = OMXSB-följare inklusive varianter, likaviktat medel per år, utan split.
# D_V är positivt i indexfondernas riktning, så nettoförsäljning vid borttag ritas som −D_V. Linje: LOWESS, bandbredd 0,8 (som G&S).
# Körs från thesis_final efter 02: python3 code/output/01_figure1_net_buying.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = Path(__file__).stem
F = pd.read_csv(RES / 'fund_demand' / 'figur1_skikt.csv')
assert F.ar.is_unique and F.ar.min() == 2007


def png():
    plt = fig_setup(); fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for typ, col, sign, lab in [('addition', ADD, 1, 'Additions: net buying'), ('deletion', DEL, -1, 'Deletions: net selling')]:
        d = F[F[f'n_D_V_{typ}'] > 0]; x, y = d.ar.values.astype(float), sign * d[f'D_V_{typ}'].values
        ax.plot(x, lowess(x, y), color=col, lw=2, zorder=2)
        ax.scatter(x, y, s=22, color=col, edgecolor='white', linewidth=0.8, zorder=3, label=lab)
        ax.annotate(lab, (x[-1], lowess(x, y)[-1]), xytext=(6, 0), textcoords='offset points', va='center', fontsize=8, color='#0b0b0b')
    ax.axhline(0, color=GREY, lw=0.6)
    ax.set_xlim(2006.5, 2030.5); ax.set_xticks(range(2007, 2027, 2))
    ax.set_ylabel('Net trade by index trackers (% of shares)')
    ax.legend(loc='upper left', fontsize=8)
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_net_buying', 'Net buying and selling by OMXSB index trackers, by year')
    figure(doc, png())
    n = int(F.n_D_V_addition.sum() + F.n_D_V_deletion.sum())
    note(doc, 'Net buying (additions) and net selling (deletions) by funds that track the OMXSB index, including tracker variants: '
         'the change in shares held between the last fund report before the announcement and the first report after the effective '
         'date, divided by shares outstanding (multiplied by 100). Fund holdings from LSEG Lipper; events with a share split '
         'between the two reports are excluded. Each point is the equal-weighted mean across events by year of the announcement; years without '
         f'fund data are left out ({n} events in total). The line is a LOWESS fit with bandwidth 0.8, as in Greenwood and Sammon '
         '(2025, Figure 1). Descriptive; no inference.'
         + ' Deletions caused by a takeover, merger, distressed share issue or a large change in shares outstanding (19 events) are '
         'excluded from the fund demand sample.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: beskrivande (medel per år och LOWESS), ingen inferens')
