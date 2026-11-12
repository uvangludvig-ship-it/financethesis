# Tabell 4 (G&S Table IV): kumulerad överavkastning före beskedet, [AD−n, AD−1] för n = 10, 20, 50, 100, per period.
# Ur results/composition/tabell2_tabell4.csv, tabell 4 (steg 10). Kontroll: samma medel som kursbanan i figur 5 vid dag −1.
# Intervall och stjärnor: wild cluster bootstrap per översyn (intervall genom testinversion), som i källfilen.
# Körs från thesis_final efter 10: python3 code/output/09_table4_runup.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

C = pd.read_csv(RES / 'composition' / 'tabell2_tabell4.csv'); C = C[C.tabell == 'tabell 4']
F7 = pd.read_csv(RES / 'composition' / 'figur7_kursbana.csv')
assert C.ci_metod.str.startswith('95 % intervall: invertering').all()
WIN = [100, 50, 20, 10]
# [AD−100, AD−1] i tabellen = kursbanan vid dag −1 (samma händelser, samma CAR)
for t in ['addition', 'deletion']:
    for p in PERS_KORT:
        a, b = one(C, typ=t, variant='[AD−100, AD−1]', rad=p), one(F7, typ=t, period=p, dag=-1)
        assert abs(a.b - b.car) < 1e-9 and int(a.n) == int(b.n), (t, p, a.b, b.car, a.n, b.n)


def build(doc):
    title(doc, 'tab_runup', 'Cumulative abnormal returns over pre-announcement windows')
    rows, cis = [], []
    for lab, t in [('Panel A. Additions', 'addition'), ('Panel B. Deletions', 'deletion')]:
        rows.append(lab)
        for n in WIN:
            rs = [one(C, typ=t, variant=f'[AD−{n}, AD−1]', rad=p) for p in PERS_KORT]
            rows.append([f'[AD−{n}, AD−1]'] + [num(r.b) + stars(r.p_wcb) for r in rs]); cis.append(len(rows))
            rows.append([''] + [ci(r.lo, r.hi) for r in rs])
        rs = [one(C, typ=t, variant='[AD−10, AD−1]', rad=p) for p in PERS_KORT]
        rows.append(['Events'] + [str(int(r.n)) for r in rs]); rows.append(['Reviews'] + [str(int(r.G)) for r in rs])
    table(doc, ['', '2007–11', '2012–16', '2017–21', '2022–26'], rows, [5.0, 2.9, 2.9, 2.9, 2.9], ci_rows=cis)
    nmin, nmax = int(C.n.min()), int(C.n.max())
    # utkast: författarna formulerar om noten
    note(doc, 'Mean cumulative abnormal return in per cent (stock total return minus .OMXSBGI) from n trading days before the '
         'announcement to the day before it, by five-year period of the effective date, as in Greenwood and Sammon (2025, '
         'Table IV). Deletions keep their sign. Greenwood and Sammon also report windows ending ten days after the announcement; '
         'those overlap the announcement and effective-date windows of ' + NUM['tab_by_period'] + ' and are not shown. Events: '
         f'events with returns over [AD−10, AD−1]; longer windows lose stocks with a short price history ({nmin} to {nmax} events '
         f'per cell). The paths behind the table are in {NUM["fig_price_path"]}. Inference: {WCR}. Brackets: {WCR_CI}. Stars from '
         f'the same draws: {STARS}.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall och stjärnor = wild cluster bootstrap per översyn (intervall genom testinversion)')
