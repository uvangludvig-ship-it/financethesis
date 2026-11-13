# Figur 8 (G&S avsnitt 2.4.3): andel av omsättningen under ED−22 till ED+22 som handlas varje dag, per period.
# Ur results/liquidity/volume_share_by_day.csv (steg 11), urvalet i tabell 1. Siffrorna för ED−1 i noten ur liquidity_results.csv.
# Kontroll: varje kolumn summerar till 100, och dag −1 och dag 0 i figuren = raderna i liquidity_results.csv.
# Körs från thesis_final efter 11: python3 code/output/14_figure8_volume.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = Path(__file__).stem
V = pd.read_csv(RES / 'liquidity' / 'volume_share_by_day.csv').set_index('dag_relativt_ED')
L = pd.read_csv(RES / 'liquidity' / 'liquidity_results.csv'); L = L[(L.test == 'B volym') & (L.urval == 'tabell 1')]
assert list(V.index) == list(range(-22, 23)) and np.allclose(V.sum(), 100)
for t in ['addition', 'deletion']:
    for p in PERS:
        for dag, txt in [(-1, 'ED−1'), (0, 'ED')]:
            r = one(L, typ=t, rad=f'{p}: andel av omsättningen ED±22 som handlas {txt} (%)')
            assert abs(V.loc[dag, f'tabell 1|{t}|{p}'] - r.b) < 1e-9, (t, p, dag)
DIFF = {t: one(L, typ=t, rad='andel ED−1: 2022–2026 minus 2007–2011 (procentenheter)') for t in ['addition', 'deletion']}


def png():
    plt = fig_setup(); fig, axs = plt.subplots(1, 2, figsize=(6.5, 3.2), sharey=True)
    for ax, (t, lab) in zip(axs, [('addition', 'Additions'), ('deletion', 'Deletions')]):
        for p, pk, col in zip(PERS, PERS_KORT, SEQ):
            ax.plot(V.index, V[f'tabell 1|{t}|{p}'], color=col, lw=1.6, label=pk)
        ax.axvline(0, color=GREY, lw=0.6, ls=':')
        ax.set_title(lab, fontsize=9, loc='left'); ax.set_xlabel('Trading days relative to effective date')
        ax.set_xlim(-22, 22); ax.set_xticks([-20, -10, -1, 10, 20])
    axs[0].set_ylabel('Share of volume over [ED−22, ED+22] (%)'); axs[0].set_ylim(0, None)
    axs[0].legend(loc='upper left', fontsize=8, title='Effective in', title_fontsize=8)
    fig.tight_layout()
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_volume', 'Trading volume around the effective date')
    figure(doc, png())
    r = {(t, p): one(L, typ=t, rad=f'{p}: andel av omsättningen ED±22 som handlas ED−1 (%)') for t in ['addition', 'deletion'] for p in [PERS[0], PERS[-1]]}
    a, d = DIFF['addition'], DIFF['deletion']
    # utkast: författarna formulerar om noten
    note(doc, 'Share of the number of shares traded over the 45 trading days from ED−22 to ED+22 that trades on each day, mean over '
         'events by five-year period of the effective date, in per cent. ED is the effective date (dotted line); index funds '
         'trade at the close on ED−1, the last day before the change takes effect. Same events as ' + NUM['tab_by_period'] + '. '
         'As discussed in Greenwood and Sammon (2025, Section II.D). The share traded on ED−1 rises from '
         f'{num(r[("addition", PERS[0])].b)} to {num(r[("addition", PERS[-1])].b)} per cent for additions (difference '
         f'{num(a.b)}{stars(a.p_wcb)} {ci(a.lo, a.hi)} percentage points) and from {num(r[("deletion", PERS[0])].b)} to '
         f'{num(r[("deletion", PERS[-1])].b)} per cent for deletions ({num(d.b)}{stars(d.p_wcb)} {ci(d.lo, d.hi)}). Inference for '
         f'the differences: {WCR}; brackets are {WCR_CI}; stars from the same draws: {STARS}.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: figuren beskrivande; skillnaderna i noten = wild cluster bootstrap per översyn (intervall genom testinversion)')
