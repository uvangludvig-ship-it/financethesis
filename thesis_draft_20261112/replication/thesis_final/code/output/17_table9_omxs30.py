# Tabell 9 (G&S Table VIII, andra index): CAR [AD−1, ED+1] vid ändringar i OMXS30 och i OMXSB, tecknet vänt för borttag.
# Ur results/other_tests/issuance_omxs30_results.csv, test "B OMXS30", urvalet som i tabell 1 (steg 12).
# Kontroll: antalet OMXSB-händelser = tabell 1 (results/effect/tabell1_lang.csv), och alla = tillägg + borttag.
# Körs från thesis_final efter 12: python3 code/output/17_table9_omxs30.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

O = pd.read_csv(RES / 'other_tests' / 'issuance_omxs30_results.csv')
O = O[(O.test == 'B OMXS30') & (O.urval == 'tabell 1 (10 borttag ute)')]
T = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
TYP = [('addition', 'Additions'), ('deletion', 'Deletions'), ('alla', 'All changes')]
R = {(ix, t): one(O, rad=f'{ix}, {t}: CAR [AD−1, ED+1], tecken vänt för borttag (%)') for ix in ['OMXS30', 'OMXSB'] for t, _ in TYP}
MDE = one(O, rad='styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3')
for t in ['addition', 'deletion']:
    n1 = int(T[(T.panel == 'A/B') & (T.typ == t) & (T.fönster == 'tot')].n.sum())
    assert int(R[('OMXSB', t)].n) == n1, (t, R[('OMXSB', t)].n, n1)
for ix in ['OMXS30', 'OMXSB']:
    assert int(R[(ix, 'alla')].n) == int(R[(ix, 'addition')].n) + int(R[(ix, 'deletion')].n), ix
assert int(MDE.n) == int(R[('OMXS30', 'alla')].n) + int(R[('OMXSB', 'alla')].n)


def build(doc):
    title(doc, 'tab_omxs30', 'Index effects for the OMXS30 and the OMXSB')
    rows, cis = [], []
    for t, lab in TYP:
        a, b = R[('OMXS30', t)], R[('OMXSB', t)]
        rows.append([lab, num(a.b) + stars(a.p_wcb), str(int(a.n)), str(int(a.G)), num(b.b) + stars(b.p_wcb), str(int(b.n)), str(int(b.G))])
        cis.append(len(rows)); rows.append(['', ci(a.lo, a.hi), '', '', ci(b.lo, b.hi), '', ''])
    table(doc, ['', 'CAR (%)', 'Events', 'Clusters', 'CAR (%)', 'Events', 'Reviews'], rows, [3.0, 3.0, 1.7, 1.7, 3.0, 1.7, 1.7],
          ci_rows=cis, group_header=[('OMXS30', 1, 3), ('OMXSB', 4, 6)])
    # utkast: författarna formulerar om noten
    note(doc, 'Mean cumulative abnormal return over [AD−1, ED+1] in per cent (stock total return minus .OMXSBGI) for changes in '
         'the OMXS30 index (the 30 most traded stocks) and in the OMXSB index, 2007–2026, with the sign reversed for deletions so '
         'that a positive number is an index effect in the expected direction. Comparable to Greenwood and Sammon (2025, '
         'Table VIII), which compares indices with different tracker ownership. OMXS30 changes that overlap an OMXSB change in the '
         'same stock are excluded. OMXSB: the events of ' + NUM['tab_by_period'] + ', with returns from the same price panel as the '
         'OMXS30 events. Inference: ' + WCR + '; for the OMXS30 the clusters are announcement dates. Brackets: ' + WCR_CI + '. Stars '
         f'from the same draws: {STARS}. We do not test the difference between the two indices: its minimum detectable effect is '
         f'{num(MDE.b)} percentage points ({int(MDE.n)} events), above the limit of 3 percentage points used for this test.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall och stjärnor = wild cluster bootstrap (OMXSB per översyn, OMXS30 per beskedsdag), intervall genom testinversion')
