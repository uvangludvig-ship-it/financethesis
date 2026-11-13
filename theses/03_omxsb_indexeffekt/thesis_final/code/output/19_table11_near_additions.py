# Tabell 11: tillägg och borttag mot nästan tillagda och nästan borttagna (T5v), före och från 2017.
# Ur results/near_additions/near_additions_results.csv (steg 14). Kontroll: antalet = händelser + nästan, och jämförelsen med
# runda 2 i results/near_additions/NEAR_ADDITIONS.md utan avvikelser.
# Körs från thesis_final efter 14: python3 code/output/19_table11_near_additions.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

R = pd.read_csv(RES / 'near_additions' / 'near_additions_results.csv')
assert 'Avvikelser' not in (RES / 'near_additions' / 'NEAR_ADDITIONS.md').read_text(encoding='utf-8')
assert (R.n == R.handelser + R.nastan).all()
assert R.ci_metod.str.startswith('95 % intervall: invertering').all()
COLS = [('addition', 'alla'), ('deletion', 'utan de 10 (G&S regel)'), ('deletion', 'alla')]
VAR = [('CAR [AD-1,ED+1] mot nästan', 'Panel A. All comparison stocks'), ('känslighet: bara huvudlistan (XSTO) bland nästan', 'Panel B. Comparison stocks on the main market only')]
PER = [('före', 'Announced before 2017'), ('efter', 'Announced 2017 or later')]


def build(doc):
    title(doc, 'tab_near', 'Index changes against stocks that were nearly added or nearly deleted')
    rows, cis = [], []
    for v, vlab in VAR:
        rows.append(vlab)
        for p, plab in PER:
            rs = [one(R, typ=t, urval=u, variant=v, period=p) for t, u in COLS]
            rows.append([plab] + [num(r.b) + stars(r.p_wcb) for r in rs]); cis.append(len(rows)); rows.append([''] + [ci(r.lo, r.hi) for r in rs])
            rows.append(['  Events / comparison stocks'] + [f'{int(r.handelser)} / {int(r.nastan)}' for r in rs])
    table(doc, ['', 'Additions', 'Deletions', 'All deletions'], rows, [6.2, 3.6, 3.6, 3.6], ci_rows=cis)
    # utkast: författarna formulerar om noten
    note(doc, 'Coefficient on an index-change dummy, in percentage points of CAR [AD−1, ED+1], from a regression of the CAR of index '
         'changes and comparison stocks on the dummy, the run-up over [AD−100, AD−1], the log market value and review fixed effects, '
         'separately for additions and deletions and for reviews announced before 2017 and from 2017. Comparison stocks for additions '
         'are stocks outside the OMXSB in the same review that were at least as large as the smallest addition (nearly added); for '
         'deletions, OMXSB members no larger than the largest deletion (nearly deleted). Panel B keeps only comparison stocks listed on '
         'the Nasdaq Stockholm main market. "Deletions" excludes the deletions that the sample rule of ' + NUM['tab_by_period'] + ' '
         'drops (8 of the 10 are in this sample); "All deletions" keeps them. Deletions keep their sign. Inference: '
         f'{WCR}. Brackets: {WCR_CI}. Stars from the same draws: {STARS}.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall och stjärnor = wild cluster bootstrap per översyn (intervall genom testinversion), fasta effekter per översyn')
