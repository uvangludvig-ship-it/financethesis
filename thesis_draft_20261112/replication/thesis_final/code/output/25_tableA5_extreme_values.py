# Tabell A5 (robusthet): extremvärden. Tabell 2:s rader i fyra varianter (alla, winsoriserad 1/99, utan |CAR| > 20, utan Sivers),
# medianen per period, och M för tillägg med och utan de 12 händelserna med egen bolagsnyhet.
# Ur results/extreme_values/extreme_values_results.csv (steg 13). Kontroll: "alla" = tabell 2 (results/effect/tabell1_lang.csv) och
# M "alla" = tabell 5 (results/fund_demand/omrakning_resultat.csv), och jämförelsen i EXTREME_VALUES.md utan avvikelser.
# Körs från thesis_final efter 13: python3 code/output/25_tableA5_extreme_values.py
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

R = pd.read_csv(RES / 'extreme_values' / 'extreme_values_results.csv')
T = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
R5 = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv')
MD = (RES / 'extreme_values' / 'EXTREME_VALUES.md').read_text(encoding='utf-8')
assert 'Avvikelser' not in MD
LO, HI = (float(x.replace('−', '-')) for x in re.search(r'\): (\S+) och (\S+) procent', MD).groups())
VAR = [('alla', 'All'), ('winsoriserad 1/99', 'Winsorized'), ('utan |CAR| > 20', '|CAR| ≤ 20 %'), ('utan Sivers', 'Without Sivers')]
TEST = ['2007–11', '2012–16', '2017–21', '2022–26', '2007–16', '2017–26', '2017–26 minus 2007–16', '2022–26 minus 2007–11', '2022–26 minus 2017–21']
FULL = {'2007–11': '2007–2011', '2012–16': '2012–2016', '2017–21': '2017–2021', '2022–26': '2022–2026'}
C = R[R.matt == 'CAR']; M = R[R.matt == 'M']
for t in ['addition', 'deletion']:
    for k, full in FULL.items():
        a, b = one(C, variant='alla', typ=t, test=k), one(T, panel='A/B', typ=t, fönster='tot', urval=full)
        assert abs(a.b - b.b) < 1e-9 and int(a.n) == int(b.n), (t, k)
R5 = R5[(R5.tabell.astype(str) == '5') & (R5.skikt == 'D_C') & (R5.fonster == 'y_tot') & (R5.typ == 'addition')]
for k in ['2017–21', '2022–26', '2017–26']:
    assert abs(one(M, variant='alla', test=k).b - one(R5, period=k).M) < 1e-9


def build(doc):
    title(doc, 'tab_extreme', 'Robustness: extreme values')
    rows, cis = [], []
    for lab, t in [('Panel A. Additions, mean CAR (%)', 'addition'), ('Panel B. Deletions, mean CAR (%)', 'deletion')]:
        rows.append(lab)
        for k in TEST:
            rs = [one(C, variant=v, typ=t, test=k) for v, _ in VAR]
            rows.append([k.replace(' minus ', ' − ')] + [num(r.b) + stars(r.p_wcb) for r in rs]); cis.append(len(rows))
            rows.append([''] + [ci(r.lo, r.hi) for r in rs])
        rows.append(['Events, 2007–26'] + [str(int(one(C, variant=v, typ=t, test='2022–26 minus 2007–11').n)) for v, _ in VAR])
    for lab, t in [('Panel C. Median CAR (%), additions', 'addition'), ('Panel D. Median CAR (%), deletions', 'deletion')]:
        rows.append(lab)
        for k in TEST[:6]:
            rows.append([k] + [num(one(C, variant=v, typ=t, test=k)['median']) for v, _ in VAR])
    table(doc, [''] + [h for _, h in VAR], rows, [4.4, 3.1, 3.1, 3.1, 3.1], ci_rows=cis)
    subhead(doc, 'Panel E. The multiplier M for additions, with and without the events with company news')
    rows, cis = [], []
    for k in ['2017–21', '2022–26', '2017–26']:
        a, b = one(M, variant='alla', test=k), one(M, variant='utan egen bolagsnyhet', test=k)
        rows.append([k, num(a.b), str(int(a.n)), num(b.b), str(int(b.n))]); cis.append(len(rows)); rows.append(['', ci(a.lo, a.hi), '', ci(b.lo, b.hi), ''])
    table(doc, ['', 'M', 'N', 'M', 'N'], rows, [4.4, 3.4, 1.6, 3.4, 1.6], ci_rows=cis,
          group_header=[('All events', 1, 2), ('Without company news', 3, 4)])
    # utkast: författarna formulerar om noten
    note(doc, 'Panels A and B: the rows of ' + NUM['tab_by_period'] + ' for the total window [AD−1, ED+1] with four treatments of '
         'extreme returns. All: as in ' + NUM['tab_by_period'] + '. Winsorized: CAR set to the 1st or 99th percentile when beyond it, '
         f'with the percentiles ({num(LO, 1)} and {num(HI, 1)} per cent) taken over all events with a CAR, including the ten deletions '
         'excluded by the sample rule. |CAR| ≤ 20 %: events with an absolute CAR above 20 per cent dropped. Without Sivers: the '
         'Sivers Semiconductors addition in June 2026 (CAR +77 per cent) dropped. Inference: ' + WCR + '. Brackets: ' + WCR_CI + '. '
         f'Stars from the same draws: {STARS}. Panels C and D: median CAR, descriptive. Panel E: M as in {NUM["tab_multiplier"]} '
         f'(net demand by {TRACKERS}, total window, events without a share split), with and without the twelve '
         f'events with company news in the window ({NUM["tab_news"]}). Brackets in Panel E: {PAIRS}.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: CAR = wild cluster bootstrap per översyn (intervall genom testinversion); median beskrivande; M = parvis klusterbootstrap, percentil')
