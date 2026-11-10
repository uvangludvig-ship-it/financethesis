# Tabell 8 (G&S avsnitt II.D, nyemissioner): förändring i antal aktier från AD−5 till ED+60, tillägg och nästan tillagda.
# Ur results/other_tests/issuance_omxs30_results.csv, test "A nyemissioner" (steg 12).
# Kontroll: antalet i skillnaden = summan av antalen per period och grupp; andelarna ligger mellan 0 och 1.
# Körs från thesis_final efter 12: python3 code/output/16_table8_issuance.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

O = pd.read_csv(RES / 'other_tests' / 'issuance_omxs30_results.csv'); O = O[O.test == 'A nyemissioner']
GR = [('tillägg', 'Additions'), ('nästan tillagda', 'Near-additions')]
D = one(O, rad='tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter)')
cells = {(g, p): one(O, rad=f'{p}: {g}, medel (%)') for g, _ in GR for p in PERS_KORT}
assert sum(int(r.n) for r in cells.values()) == int(D.n), 'antalet i skillnaden ska vara summan av cellerna'
assert all(0 <= r.andel_over_5 <= r.andel_over_1 <= 1 for r in cells.values())


def build(doc):
    title(doc, 'tab_issuance', 'Share issuance around OMXSB additions')
    rows = []
    for p in PERS_KORT:
        rr = [p]
        for g, _ in GR:
            r = cells[(g, p)]; rr += [num(r.b), num(100 * r.andel_over_1, 1), num(100 * r.andel_over_5, 1), str(int(r.n))]
        rows.append(rr)
    table(doc, ['', 'Mean (%)', '> 1 %', '> 5 %', 'N', 'Mean (%)', '> 1 %', '> 5 %', 'N'], rows,
          [1.8] + [1.9, 1.5, 1.5, 1.2] * 2, group_header=[('Additions', 1, 4), ('Near-additions', 5, 8)])
    subhead(doc, 'Additions minus near-additions, 2007–26, review fixed effects')
    table(doc, ['', 'Difference (pp)', '95 % interval', 'p', 'N', 'Reviews'],
          [['Change in shares outstanding', num(D.b) + stars(D.p_wcb), ci(D.lo, D.hi), num(D.p_wcb, 3), str(int(D.n)), str(int(D.G))]],
          [5.2, 2.6, 3.4, 1.6, 1.6, 1.6])
    # utkast: författarna formulerar om noten
    note(doc, 'Change in the log number of shares outstanding of the company (all listed share classes) from five trading days '
         'before the announcement to 60 trading days after the effective date, in per cent, by five-year period of the effective '
         'date. Near-additions are stocks that were close to being added in the same review but were not. "> 1 %" and "> 5 %": '
         'share of stocks whose number of shares rose by more than 1 or 5 per cent. Greenwood and Sammon (2025, Section II.D) ask '
         'whether firms issue shares into the index rebalance. The difference row regresses the change on an addition dummy with '
         f'review fixed effects. Inference: {WCR}. Brackets: {WCR_CI}. Stars and p from the same draws: {STARS}.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: periodceller beskrivande; skillnaden = wild cluster bootstrap per översyn (intervall genom testinversion)')
