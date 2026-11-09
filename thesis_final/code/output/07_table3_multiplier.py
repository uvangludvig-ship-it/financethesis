# Tabell 3 (G&S Table V): multiplikatorn M = medel-CAR / medel-D och elasticiteten −1/M, per period.
# Ur results/fund_demand/omrakning_resultat.csv, tabell 5 (02), skikt D_V (OMXSB-följare inklusive varianter), utan split.
# Intervall för M: parvis klusterbootstrap per översyn, percentil (02, kvot_ci). CAR och D visas med eget tecken som hos G&S
# (negativa vid borttag); filen har dem i indexfondernas riktning (y = s*CAR, D > 0), så de multipliceras med s här.
# Körs från thesis_final efter 02: python3 code/output/07_table3_multiplier.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

R = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv')
R5 = R[(R.tabell == 5) & (R.skikt == 'D_V')]
assert R5.ci_metod.dropna().str.startswith('95 % intervall för M: parvis klusterbootstrap').all()
SAMPLES = PERS_KORT + ['2007–16', '2017–26']
WINS = [('y_tot', 'Baseline window [AD−1, ED+1]'), ('y_lang', 'Extended window [AD−20, ED+1]')]
for w, _ in WINS:
    for typ in ['addition', 'deletion']:
        for p in SAMPLES:
            r = one(R5, typ=typ, fonster=w, period=p)
            assert abs(r.M - r.car / r.D) < 1e-9 and r.D > 0, (w, typ, p)
            assert r.andel_oandliga == 0, (w, typ, p, 'bootstrapdragningar med D <= 0')
            assert r.lo <= r.M <= r.hi, (w, typ, p)


def build(doc):
    title(doc, 'tab_multiplier', 'Index effect decomposition: the multiplier M by period')
    rows, cis = [], []
    for w, wl in WINS:
        rows.append(wl)
        for p in SAMPLES:
            a, d = one(R5, typ='addition', fonster=w, period=p), one(R5, typ='deletion', fonster=w, period=p)
            rows.append([p, str(int(a.n)), num(a.car), num(a.D), num(a.M), str(int(d.n)), num(-d.car), num(-d.D), num(d.M)])
            cis.append(len(rows)); rows.append(['', '', '', '', ci(a.lo, a.hi), '', '', '', ci(d.lo, d.hi)])
    table(doc, ['Period', 'N', 'CAR', 'D̄', 'M', 'N', 'CAR', 'D̄', 'M'], rows, [1.7, 0.9, 1.3, 1.2, 3.4, 0.9, 1.3, 1.2, 3.4],
          ci_rows=cis, group_header=[('Additions', 1, 4), ('Deletions', 5, 8)])
    note(doc, 'Following Greenwood and Sammon (2025, Table V), M is the mean cumulative abnormal return divided by the mean net '
         'demand of index trackers, CAR = M × D̄, estimated separately for additions and deletions and by period; the implied demand elasticity is '
         'ε = −1/M. CAR in per cent. D̄: mean net purchases (negative: net sales) by OMXSB index trackers including variants, in per '
         'cent of shares outstanding, between the fund report before the announcement and the report after the effective date. '
         'CAR keeps its sign (negative for deletions), so M is positive when prices move with index demand. Events with fund '
         f'holdings data and no share split between the fund reports. Brackets: {PAIRS}. No draw had a mean D of zero or below. '
         'Extended window: from 20 trading days before the announcement to the day after the effective date, as in their Table V.'
         + ' Deletions caused by a takeover, merger, distressed share issue or a large change in shares outstanding (19 events) are '
         'excluded from the fund demand sample.')


if __name__ == '__main__':
    run(build, '07_table3_multiplier')
    print('Metod: intervall för M = parvis klusterbootstrap per översyn, percentil, 9 999 dragningar')
