# Tabell 8 (G&S avsnitt II.D, nyemissioner): förändring i antal aktier från AD−5 till ED+60, tillägg och nästan tillagda.
# Ur results/other_tests/issuance_omxs30_results.csv, test "A nyemissioner" (steg 12). Splitjusterat aktieantal (11 nov 2026,
# declarations/issuance_split_declaration.md); raden utan splitjustering visas som jämförelse.
# Kontroll: antalet i skillnaden = summan av antalen per period och grupp; andelarna ligger mellan 0 och 1.
# Körs från thesis_final efter 12: python3 code/output/16_table8_issuance.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

O = pd.read_csv(RES / 'other_tests' / 'issuance_omxs30_results.csv'); O = O[O.test == 'A nyemissioner']
GR = [('tillägg', 'Additions'), ('nästan tillagda', 'Near-additions')]
HUV = 'tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter)'
D = one(O, rad=HUV)
DIFF = [(D, 'Change in shares outstanding'),
        (one(O, rad='andel med ökning över 1 %: tillägg minus nästan tillagda, fasta effekter per översyn (procentenheter)'), 'Share with increase > 1 %'),
        (one(O, rad='andel med ökning över 5 %: tillägg minus nästan tillagda, fasta effekter per översyn (procentenheter)'), 'Share with increase > 5 %'),
        (one(O, rad=HUV + ', gräns 1,4 utan matchning'), 'Change in shares, factor rule only'),
        (one(O, rad=HUV + ', utan splitjustering'), 'Change in shares, not split-adjusted')]
assert all(int(r.n) == int(D.n) for r, _ in DIFF)
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
          [[lab, num(r.b) + stars(r.p_wcb), ci(r.lo, r.hi), num(r.p_wcb, 3), str(int(r.n)), str(int(r.G))] for r, lab in DIFF],
          [5.6, 2.4, 3.4, 1.4, 1.6, 1.6])
    # utkast: författarna formulerar om noten
    note(doc, 'Change in the log number of shares outstanding of the company (all listed share classes) from five trading days '
         'before the announcement to 60 trading days after the effective date, in per cent, by five-year period of the effective '
         'date. Near-additions are stocks that were close to being added in the same review but were not. "> 1 %" and "> 5 %": '
         'share of stocks whose number of shares rose by more than 1 or 5 per cent. Greenwood and Sammon (2025, Section II.D) ask '
         'whether firms issue shares into the index rebalance. The number of shares is adjusted for splits and reverse splits: when '
         'the ratio of the unadjusted to the adjusted share price moves by more than a factor 1.4 between the two dates and explains the '
         'change in shares within 10 per cent, the change in that ratio is removed from the change in shares (48 stocks). The '
         'difference rows regress the change, and indicators (× 100) for an increase above 1 and 5 per cent, on an addition dummy '
         'with review fixed effects. Factor rule only: every change in the price ratio above 1.4 is removed, which also removes part '
         'of rights issues and adjusts stocks whose number of shares did not change. Not split-adjusted: the raw change. All three '
         f'rules were reported regardless of outcome. Inference: {WCR}. Brackets: {WCR_CI}. Stars and p from the same draws: {STARS}.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: periodceller beskrivande; skillnaden = wild cluster bootstrap per översyn (intervall genom testinversion)')
