# Tabell 1 (G&S Table I): överavkastning år för år, med periodrader.
# Årsmedel ur results/effect/effect_by_year.csv (räknas i 01 ur händelserna, samma urval); periodrader och stjärnor ur results/effect/tabell1_lang.csv (01).
# Kontroll: N-viktat medel av årsraderna = periodmedlet i tabell1_lang.csv, och N stämmer.
# Körs från thesis_final efter 01: python3 code/output/02_table1_effect_by_year.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

T = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
Y = pd.read_csv(RES / 'effect' / 'effect_by_year.csv', header=[0, 1], index_col=0)
Y.columns = [f'{a}_{b}' for a, b in Y.columns]
YRS = [i for i in Y.index if str(i).isdigit()]
assert [int(y) for y in YRS] == list(range(2007, 2027)), YRS

for typ, pre in [('addition', 'Additions'), ('deletion', 'Deletions')]:
    for p in PERS:
        a, b = int(p[:4]), int(p[-4:]); q = Y.loc[[y for y in YRS if a <= int(y) <= b]]
        m = (q[f'{pre}_N'] * q[f'{pre}_Total']).sum() / q[f'{pre}_N'].sum()
        r = one(T, panel='A/B', typ=typ, fönster='tot', urval=p)
        assert abs(m - r.b) < 1e-6, (typ, p, m, r.b)
        assert int(q[f'{pre}_N'].sum()) == int(r.n), (typ, p)


def build(doc):
    title(doc, 'tab_by_year', 'Abnormal returns around OMXSB additions and deletions, by year, 2007–2026')
    rows = []
    for y in YRS:
        r = Y.loc[y]
        rows.append([str(y)] + [str(int(r[f'{pre}_N'])) if c == 'N' else num(r[f'{pre}_{c}'])
                                for pre in ['Additions', 'Deletions'] for c in ['N', 'Ann', 'Eff', 'Total']])
    rows.append('Period means')
    for p in PERS:
        rr = [p[:4] + '–' + p[-2:]]
        for typ in ['addition', 'deletion']:
            rr.append(str(int(one(T, panel='A/B', typ=typ, fönster='tot', urval=p).n)))
            for w in ['ann', 'eff', 'tot']:
                r = one(T, panel='A/B', typ=typ, fönster=w, urval=p); rr.append(num(r.b) + stars(r.p_wcb))
        rows.append(rr)
    for p in ['2007–16', '2017–26']:
        a, d = one(T, panel='C', typ='addition', urval=p), one(T, panel='C', typ='deletion', urval=p)
        rows.append([p, str(int(a.n)), '', '', num(a.b) + stars(a.p_wcb), str(int(d.n)), '', '', num(d.b) + stars(d.p_wcb)])
    table(doc, ['Year', 'N', 'Ann.', 'Eff.', 'Total', 'N', 'Ann.', 'Eff.', 'Total'], rows, [1.9] * 9,
          group_header=[('Additions', 1, 4), ('Deletions', 5, 8)])
    note(doc, 'Mean cumulative abnormal return in per cent (stock total return minus the OMX Stockholm Benchmark Gross Index, '
         '.OMXSBGI) by year of the effective date. Ann.: [AD−1, AD+1]; Eff.: [ED−1, ED+1]; Total: [AD−1, ED+1], where AD is the '
         'announcement date and ED the effective date. N counts events with a complete total window. Each year has at most two '
         'reviews, so yearly means carry no standard errors. Period rows: the same means pooled over five-year periods and '
         f'decades, with stars from a {WCR}: {STARS}. Confidence intervals in {NUM["tab_by_period"]}. 2007 contains only the July '
         'and December 2007 reviews, 2026 only the June review.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: årsrader beskrivande (inga standardfel); stjärnor på periodraderna = wild cluster bootstrap per översyn')
