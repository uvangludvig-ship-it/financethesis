# Figur 5 (G&S Figure 7): kumulerad överavkastning i händelsetid, AD−100 till AD+14, per period, tillägg och borttag.
# Ur results/composition/figur7_kursbana.csv (steg 10): medel över händelserna av CAR från AD−100 till AD+k.
# Kontroll: värdet vid dag −1 = [AD−100, AD−1] i tabell 4 (results/composition/tabell2_tabell4.csv), samma antal händelser.
# Körs från thesis_final efter 10: python3 code/output/08_figure5_price_path.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = Path(__file__).stem
F = pd.read_csv(RES / 'composition' / 'figur7_kursbana.csv')
C = pd.read_csv(RES / 'composition' / 'tabell2_tabell4.csv'); C = C[(C.tabell == 'tabell 4') & (C.variant == '[AD−100, AD−1]')]
assert set(F.period) == set(PERS_KORT) and F.groupby(['typ', 'period']).dag.apply(lambda d: list(d) == list(range(-100, 15))).all()
assert np.isfinite(F.car).all()
for t in ['addition', 'deletion']:
    for p in PERS_KORT:
        a, b = one(F, typ=t, period=p, dag=-1), one(C, typ=t, rad=p)
        assert abs(a.car - b.b) < 1e-9 and int(a.n) == int(b.n), (t, p)


def png():
    plt = fig_setup(); fig, axs = plt.subplots(1, 2, figsize=(6.5, 3.2), sharex=True)
    for ax, (t, lab) in zip(axs, [('addition', 'Additions'), ('deletion', 'Deletions')]):
        for p, col in zip(PERS_KORT, SEQ):
            d = F[(F.typ == t) & (F.period == p)]
            ax.plot(d.dag, d.car, color=col, lw=2, label=p)
        ax.axhline(0, color=GREY, lw=0.6); ax.axvline(0, color=GREY, lw=0.6, ls=':')
        ax.set_title(lab, fontsize=9, loc='left'); ax.set_xlabel('Trading days relative to announcement')
        ax.set_xlim(-100, 14); ax.set_xticks([-100, -75, -50, -25, 0])
    axs[0].set_ylabel('Cumulative abnormal return (%)')
    axs[0].legend(loc='upper left', fontsize=8, title='Effective in', title_fontsize=8)
    fig.tight_layout()
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_price_path', 'Cumulative abnormal returns before and after the announcement')
    figure(doc, png())
    nmin, nmax = int(F.n.min()), int(F.n.max())
    # utkast: författarna formulerar om noten
    note(doc, 'Mean cumulative abnormal return (stock total return minus .OMXSBGI), in per cent, from 100 trading days before the '
         'announcement to day k, for k from −100 to +14, by five-year period of the effective date. Day 0 is the announcement '
         'date (dotted line). Deletions keep their sign. As in Greenwood and Sammon (2025, Figure 7), which pools by decade. '
         f'Between {nmin} and {nmax} events per line and day. The values at day −1 are the [AD−100, AD−1] row of '
         f'{NUM["tab_runup"]}. Descriptive; inference in {NUM["tab_runup"]}.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: beskrivande (medel per dag och period), ingen inferens; intervall i tabell 4')
