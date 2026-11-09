# Figur 2 (G&S Figure 2): indexeffekten per år, totalt fönster [AD−1, ED+1].
# Punkter: årsmedel ur data/comparison/replication_effect_by_year.csv (samma som tabell 1).
# Linje: glidande medel över fem år av årsmedlen (G&S använder tio år på 40 år; vi har 20 år). Bara år med händelser räknas.
# Körs från thesis_final: python3 code/output/04_figure2_effect_by_year.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = '04_figure2_effect_by_year'
Y = pd.read_csv(DATA / 'comparison' / 'replication_effect_by_year.csv', header=[0, 1], index_col=0)
Y.columns = [f'{a}_{b}' for a, b in Y.columns]
Y = Y.loc[[i for i in Y.index if str(i).isdigit()]]; Y.index = Y.index.astype(int)
assert list(Y.index) == list(range(2007, 2027))
MA = 5


def png():
    plt = fig_setup(); fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for pre, col, lab in [('Additions', ADD, 'Additions'), ('Deletions', DEL, 'Deletions')]:
        s = Y[f'{pre}_Total'].where(Y[f'{pre}_N'] > 0)
        ma = s.rolling(MA, min_periods=MA).mean()
        ax.scatter(s.index, s.values, s=22, color=col, edgecolor='white', linewidth=0.8, zorder=3, label=lab)
        ax.plot(ma.index, ma.values, color=col, lw=2, zorder=2)
        last = ma.dropna()
        ax.annotate(f'{lab}, {MA}-year average', (last.index[-1], last.values[-1]), xytext=(6, 0), textcoords='offset points',
                    va='center', fontsize=8, color='#0b0b0b')
    ax.axhline(0, color=GREY, lw=0.6)
    ax.set_xlim(2006.5, 2031.5); ax.set_xticks(range(2007, 2027, 2))
    ax.set_ylabel('CAR [AD−1, ED+1] (%)')
    ax.legend(loc='upper right', fontsize=8)
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_by_year', 'Average index effect by year')
    figure(doc, png())
    note(doc, 'Points: mean cumulative abnormal return from the day before the announcement to the day after the effective date '
         '([AD−1, ED+1], in per cent, stock total return minus .OMXSBGI) by year of the effective date, as in '
         f'{NUM["tab_by_year"]}. Lines: trailing {MA}-year moving averages of the yearly means (Greenwood and Sammon, 2025, Figure 2, '
         'use ten years over a 40-year sample). Descriptive; for inference see ' + NUM['tab_by_period'] + '.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: beskrivande (årsmedel och glidande medel), ingen inferens')
