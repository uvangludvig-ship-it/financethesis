# Figur 3 (G&S Figure 3): indexfondernas nettoköp mot indexeffekten, en punkt per händelse.
# Ur results/fund_demand/handelser_omraknade.csv (02): händelser med fonddata, utan split, med D_C och y_tot.
# x = nettoköp i procent av aktierna (s*D_C: negativt vid borttag), y = CAR [AD−1, ED+1] med eget tecken (s*y_tot = car_tot).
# Körs från thesis_final efter 02: python3 code/output/05_figure3_demand_vs_effect.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

STEM = Path(__file__).stem
E = pd.read_csv(RES / 'fund_demand' / 'handelser_omraknade.csv')
E = E[E.fonddata & ~E.split.astype(bool) & E.D_C.notna() & E.y_tot.notna()].copy()
assert set(E.s.unique()) <= {1.0, -1.0} and (E.s == np.where(E.type == 'addition', 1.0, -1.0)).all()
assert np.allclose(E.s * E.y_tot, E.car_tot)
E['x'] = E.s * E.D_C; E['y'] = E.car_tot


def png():
    plt = fig_setup(); fig, ax = plt.subplots(figsize=(6.3, 3.8))
    for typ, col, lab in [('addition', ADD, 'Additions'), ('deletion', DEL, 'Deletions')]:
        d = E[E.type == typ]
        ax.scatter(d.x, d.y, s=16, color=col, alpha=0.75, edgecolor='white', linewidth=0.5, label=f'{lab} (N = {len(d)})', zorder=3)
    ax.axhline(0, color=GREY, lw=0.6); ax.axvline(0, color=GREY, lw=0.6)
    ax.set_xlabel('Net purchases by index trackers (% of shares)'); ax.set_ylabel('CAR [AD−1, ED+1] (%)')
    ax.grid(True, axis='both')
    ax.legend(loc='upper left', fontsize=8)
    p = OUT / f'{STEM}.png'; OUT.mkdir(parents=True, exist_ok=True); fig.savefig(p); plt.close(fig); return p


def build(doc):
    title(doc, 'fig_scatter', 'Net purchases by index trackers and the index effect')
    figure(doc, png())
    note(doc, 'Each point is one addition or deletion with fund holdings data and no share split between the fund reports '
         f'({len(E)} events, {int(E.ar.min())}–{int(E.ar.max())}). Horizontal axis: net purchases by ' + TRACKERS + ', in per cent of shares outstanding (negative for deletions). Vertical axis: cumulative abnormal return from the day '
         'before the announcement to the day after the effective date, in per cent. As in Greenwood and Sammon (2025, Figure 3). '
         'Descriptive; the multiplier estimates are in ' + NUM['tab_multiplier'] + '.'
         + ' Deletions caused by a takeover, merger, distressed share issue or a large change in shares outstanding (19 events) are '
         'excluded from the fund demand sample.')


if __name__ == '__main__':
    run(build, STEM)
    print('Metod: beskrivande (en punkt per händelse), ingen inferens')
