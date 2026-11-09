# Tabell 2 (G&S Table I, perioddelen): överavkastning per femårsperiod och decennium med 95 % intervall.
# Allt läses ur results/effect/tabell1_lang.csv (01). Intervall och stjärnor = wild cluster bootstrap (intervall genom testinversion).
# Körs från thesis_final efter 01: python3 code/output/03_table2_effect_by_period.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

T = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
assert T[T.panel != 'D'].ci_metod.str.startswith('95 % intervall: invertering').all(), 'tabell1_lang.csv har inte bootstrapintervall'
assert [int(one(T, panel='A/B', typ='addition', fönster='tot', urval=p).n) for p in PERS] == [33, 54, 82, 87]
assert [int(one(T, panel='A/B', typ='deletion', fönster='tot', urval=p).n) for p in PERS] == [38, 47, 63, 77]
WIN = [('ann', 'Announcement [AD−1, AD+1]'), ('eff', 'Effective [ED−1, ED+1]'), ('tot', 'Total [AD−1, ED+1]')]


def est(r): return num(r.b) + stars(r.p_wcb)


def build(doc):
    title(doc, 'tab_by_period', 'Abnormal returns around OMXSB additions and deletions by period, 2007–2026')
    rows, cis = [], []
    for lab, typ in [('Panel A. Additions', 'addition'), ('Panel B. Deletions', 'deletion')]:
        rows.append(lab)
        for w, wl in WIN:
            rs = [one(T, panel='A/B', typ=typ, fönster=w, urval=p) for p in PERS]
            rows.append([wl] + [est(r) for r in rs]); cis.append(len(rows)); rows.append([''] + [ci(r.lo, r.hi) for r in rs])
        tot = [one(T, panel='A/B', typ=typ, fönster='tot', urval=p) for p in PERS]
        rows.append(['Events'] + [str(int(r.n)) for r in tot]); rows.append(['Reviews'] + [str(int(r.G)) for r in tot])
    table(doc, ['', '2007–11', '2012–16', '2017–21', '2022–26'], rows, [6.0, 2.65, 2.65, 2.65, 2.65], ci_rows=cis)

    subhead(doc, 'Panel C. Total window [AD−1, ED+1], by decade')
    rows, cis = [], []
    for lab, typ in [('Additions', 'addition'), ('Deletions', 'deletion')]:
        a, b = one(T, panel='C', typ=typ, urval='2007–16'), one(T, panel='C', typ=typ, urval='2017–26')
        d = one(T, panel='D', typ=typ, urval='2017–26 minus 2007–16 (decennier)')
        rows.append([lab, est(a), est(b), est(d)]); cis.append(len(rows)); rows.append(['', ci(a.lo, a.hi), ci(b.lo, b.hi), ci(d.lo, d.hi)])
        rows.append(['Events', str(int(a.n)), str(int(b.n)), ''])
    table(doc, ['', '2007–16', '2017–26', 'Difference'], rows, [6.0, 3.5, 3.5, 3.5], ci_rows=cis)
    note(doc, 'Cumulative abnormal return in per cent: the stock\'s total return minus the return on the OMX Stockholm Benchmark '
         'Gross Index (.OMXSBGI), summed over the window. AD is the announcement date and ED the effective date. Each cell gives the '
         f'mean across events. Inference: {WCR}. Brackets: {WCR_CI}. Stars come from the same bootstrap draws: {STARS}. '
         'Deletions keep their sign. Events are counted for the total window; the announcement and effective windows include up to '
         'three more events per period. Difference in Panel C: 2017–26 minus 2007–16, same inference. Sample: 481 changes in 39 '
         'semi-annual reviews with effective dates from 2 July 2007 to 1 June 2026 (Table A1).')


if __name__ == '__main__':
    run(build, '03_table2_effect_by_period')
    print('Metod: intervall och stjärnor = wild cluster bootstrap per översyn (intervall genom testinversion)')
