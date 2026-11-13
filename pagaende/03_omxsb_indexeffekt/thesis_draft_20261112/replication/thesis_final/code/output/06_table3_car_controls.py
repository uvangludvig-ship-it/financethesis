# Tabell 3 (G&S Table II): CAR [AD−1, ED+1] på periodkonstanter, utan och med kontroller.
# Ur results/composition/tabell2_tabell4.csv, tabell 2 (steg 10). Kontroll: utan kontroller = tabell 1 (results/effect/tabell1_lang.csv).
# Intervall och stjärnor: wild cluster bootstrap per översyn (intervall genom testinversion), som i källfilen.
# Körs från thesis_final efter 10: python3 code/output/06_table3_car_controls.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

C = pd.read_csv(RES / 'composition' / 'tabell2_tabell4.csv'); C = C[C.tabell == 'tabell 2']
T = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
assert C.ci_metod.str.startswith('95 % intervall: invertering').all()
VAR = ['utan kontroller', 'med kontroller', 'utan kontroller, samma händelser som med']
COLS = [(t, v) for t in ['addition', 'deletion'] for v in VAR]
KOEF = [('koefficient: onormal omsättning', 'Turnover'), ('koefficient: relativ storlek', 'Size'),
        ('koefficient: arbitragerisk', 'Arbitrage risk (WZ)'), ('koefficient: analytiker', 'Analyst coverage')]
DIFF = '2007–11 minus 2022–26'
# utan kontroller ska vara tabell 1: samma medel per period och samma antal händelser
for t in ['addition', 'deletion']:
    for p, pl in zip(PERS_KORT, PERS):
        a, b = one(C, typ=t, variant='utan kontroller', rad=p).b, one(T, panel='A/B', typ=t, fönster='tot', urval=pl).b
        assert abs(a - b) < 1e-9, (t, p, a, b)
    n1 = int(T[(T.panel == 'A/B') & (T.typ == t) & (T.fönster == 'tot')].n.sum())
    assert int(one(C, typ=t, variant='utan kontroller', rad=PERS_KORT[0]).n) == n1, (t, n1)
    # samma händelser: lika många som med kontroller
    assert int(one(C, typ=t, variant=VAR[1], rad=DIFF).n) == int(one(C, typ=t, variant=VAR[2], rad=DIFF).n)


def build(doc):
    title(doc, 'tab_car_controls', 'Cumulative abnormal returns, controlling for characteristics')
    rows, cis = [], []
    for k, lab in KOEF:
        cells = []
        for t, v in COLS:
            m = C[(C.typ == t) & (C.variant == v) & (C.rad == k)]
            cells.append((num(m.iloc[0].b) + stars(m.iloc[0].p_wcb), ci(m.iloc[0].lo, m.iloc[0].hi)) if len(m) else ('', ''))
        rows.append([lab] + [c[0] for c in cells]); cis.append(len(rows)); rows.append([''] + [c[1] for c in cells])
    for p in PERS_KORT + [DIFF]:
        rs = [one(C, typ=t, variant=v, rad=p) for t, v in COLS]
        lab = '2007–11 − 2022–26' if p == DIFF else p
        rows.append([lab] + [num(r.b) + stars(r.p_wcb) for r in rs]); cis.append(len(rows)); rows.append([''] + [ci(r.lo, r.hi) for r in rs])
    rows.append(['Events'] + [str(int(one(C, typ=t, variant=v, rad=DIFF).n)) for t, v in COLS])
    rows.append(['Reviews'] + [str(int(one(C, typ=t, variant=v, rad=DIFF).G)) for t, v in COLS])
    rows.append(['Controls'] + ['No', 'Yes', 'No'] * 2)
    table(doc, ['', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)'], rows, [3.8, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2], ci_rows=cis,
          group_header=[('CAR additions (%)', 1, 3), ('CAR deletions (%)', 4, 6)])
    # utkast: författarna formulerar om noten
    note(doc, 'Following Greenwood and Sammon (2025, Table II), we regress the cumulative abnormal return over [AD−1, ED+1], in '
         'per cent, on dummies for the four five-year periods (by effective date), without and with controls, separately for '
         'additions and deletions. Deletions keep their sign. Controls, all measured before the announcement and demeaned: '
         'turnover is the stock\'s mean daily turnover (per cent of market value) over [AD−21, AD−1] minus the same measure for '
         'the whole main market; size is the stock\'s market value in per cent of the total market value of OMXSB members on the '
         'day before AD; arbitrage risk is the residual variance from a regression of daily returns on .OMXSBGI over '
         '[AD−250, AD−2] (Wurgler and Zhuravskaya, 2002); analyst coverage is the number of earnings forecasts in the consensus '
         'the month before AD. Columns (1) and (4) equal ' + NUM['tab_by_period'] + '; columns (3) and (6) drop controls but keep '
         'only the events with all four controls, so that (2) and (3), and (5) and (6), compare the same events. Row '
         '"2007–11 − 2022–26": difference between the first and the last period coefficient. Inference: '
         f'{WCR}. Brackets: {WCR_CI}. Stars from the same draws: {STARS}. Greenwood and Sammon report White standard errors and '
         'R²; we report the bootstrap instead.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall och stjärnor = wild cluster bootstrap per översyn (intervall genom testinversion)')
