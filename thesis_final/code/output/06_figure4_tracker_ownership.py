# Figur 4 (G&S Figure 5): hur stor del av OMXSB som ägs av indexfonder, per år (december).
# Ur results/fund_demand/figur1_skikt.csv (02): fondförmögenhet från SHoF per skikt delat med OMXSB:s börsvärde.
# Skikten är kumulativa: B = rena OMXSB-följare, V = B + varianter, C = V + OMXSB-andelen i blandfonder.
# Körs från thesis_final efter 02: python3 code/output/06_figure4_tracker_ownership.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = '06_figure4_tracker_ownership'
F = pd.read_csv(RES / 'fund_demand' / 'figur1_skikt.csv')
D = F.dropna(subset=['agarandel_B_pct', 'agarandel_V_pct', 'agarandel_C_pct'])
assert (D.agarandel_B_pct <= D.agarandel_V_pct + 1e-9).all() and (D.agarandel_V_pct <= D.agarandel_C_pct + 1e-9).all(), 'skikten ska vara kumulativa'
SER = [('agarandel_C_pct', THIRD, 'C: V plus OMXSB share of balanced funds'), ('agarandel_V_pct', DEL, 'V: B plus tracker variants'),
       ('agarandel_B_pct', ADD, 'B: pure OMXSB index funds')]


def png():
    plt = fig_setup(); fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for col, c, lab in SER:
        ax.plot(D.ar, D[col], color=c, lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.8, label=lab)
    ax.set_ylim(0, None); ax.set_xticks(range(2007, int(D.ar.max()) + 1, 2))
    ax.set_ylabel('Share of OMXSB market value (%)')
    ax.legend(loc='upper left', fontsize=8)
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_ownership', 'Share of the OMXSB index owned by index trackers, by year')
    figure(doc, png())
    note(doc, 'Assets of funds that track the OMXSB index at the end of each year (SHoF fund database), divided by the market value '
         'of the OMXSB index. The three lines are cumulative: B counts pure OMXSB index funds, V adds tracker variants, and C adds '
         'the OMXSB share of balanced funds, weighted by the OMXSB weight in their benchmark (Finansinspektionen). A fund counts '
         'only while its mandate documents show it tracking the index. Comparable to Greenwood and Sammon (2025, Figure 5). '
         f'{int(D.ar.min())}–{int(D.ar.max())}. Descriptive; no inference.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: beskrivande (andel per år), ingen inferens')
