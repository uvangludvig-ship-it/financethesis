# Tabell A3: M med Finansinspektionens bredare mått på indexfondernas köp, som kontroll av D från LSEG Lipper.
# Ur results/fi_check/fi_m_kontroll.csv (03). Inte deklarerad i förväg. Intervall: parvis klusterbootstrap, percentil, 4 999 dragningar.
# Körs från thesis_final efter 03: python3 code/output/23_tableA3_fi_check.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

F = pd.read_csv(RES / 'fi_check' / 'fi_m_kontroll.csv')
F['splittade'] = F.splittade.astype(str).str.lower().map({'true': True, 'false': False})
assert F.ci_metod.str.contains('4 999').all() and len(F) == 4
PAIRS_4999 = PAIRS.replace('9,999', '4,999')


def build(doc):
    title(doc, 'tab_fi', 'The multiplier M with net demand from Finansinspektionen fund data, 2019–2026')
    rows, cis = [], []
    for t, tl in [('addition', 'Additions'), ('deletion', 'Deletions')]:
        s = 1 if t == 'addition' else -1
        for sp in [False, True]:
            r = one(F, typ=t, splittade=sp)
            rows.append([f'{tl}, ' + ('incl. split events' if sp else 'excl. split events'), str(int(r.n)), str(int(r.G)), num(s * r.car),
                         num(s * r.D_FI), num(r.M_FI), num(s * r.D_C) if not sp else '', num(r.M_C) if not sp else ''])
            cis.append(len(rows)); rows.append(['', '', '', '', '', ci(r.lo_FI, r.hi_FI), '', ci(r.lo_C, r.hi_C) if not sp else ''])
    table(doc, ['Sample', 'N', 'Reviews', 'CAR (%)', 'D̄ (%)', 'M', 'D̄ (%)', 'M'], rows, [4.6, 1.2, 1.6, 1.8, 1.8, 2.6, 1.8, 2.6],
          ci_rows=cis, group_header=[('Finansinspektionen', 4, 5), ('LSEG Lipper', 6, 7)])
    note(doc, 'Not declared in advance; a check on the fund demand measure. Finansinspektionen: net purchases by funds classified '
         'as OMXSB index funds from their quarterly holdings in Finansinspektionen\'s fund data, counted only when classified so in '
         'both the quarter before and the quarter after the change, 2019–2026. LSEG Lipper: the measure used in '
         f'{NUM["tab_multiplier"]}, on the same events. CAR over [AD−1, ED+1], keeping its sign. M = mean CAR / mean D̄. Brackets: '
         f'{PAIRS_4999}. The LSEG measure is not available for events with a share split between the fund reports.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall för M = parvis klusterbootstrap per översyn, percentil, 4 999 dragningar')
