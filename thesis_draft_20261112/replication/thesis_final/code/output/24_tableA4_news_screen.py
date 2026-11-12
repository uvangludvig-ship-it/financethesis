# Tabell A4 (robusthet): alla händelser bredvid händelserna utan egen bolagsnyhet i fönstret, och det gamla urvalet av borttag.
# Panel A och B ur results/news_screen/news_screen_results.csv (steg 09). Panel C ur results/effect/tabell1_lang.csv (01): panel R
# (alla borttag, även de 10 som G&S regel utesluter) bredvid huvudurvalet (panel A/B, C och D).
# Kontroll: "Alla" i steg 09 = tabell 1 (samma medel och antal), och antalet borttagna = antalet i results/news_screen/REASONS.md.
# Körs från thesis_final efter 09: python3 code/output/24_tableA4_news_screen.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

N = pd.read_csv(RES / 'news_screen' / 'news_screen_results.csv')
T = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
import re
M = re.search(r'Genomgångna: (\d+) händelser .*?Borttagna: (\d+)\. Oklara \(behålls\): (\d+)', (RES / 'news_screen' / 'REASONS.md').read_text(encoding='utf-8'))
N_GENOM, N_JA, N_OKLART = (int(x) for x in M.groups())
ALLA, UTAN, RP = 'Alla (tabell 1)', 'Utan egen bolagsnyhet', 'R (gammalt urval, alla borttag)'
# samma perioder som tabell 2: de fyra femårsperioderna, decennierna och skillnaderna
TEST = ['2007–11', '2012–16', '2017–21', '2022–26', '2007–16', '2017–26', '2017–26 minus 2007–16', '2022–26 minus 2007–11',
        '2022–26 minus 2017–21']
LAB = {k: k.replace(' minus ', ' − ') for k in TEST}
assert N.ci_metod.str.startswith('95 % intervall: invertering').all()
FULL = {'2007–11': '2007–2011', '2012–16': '2012–2016', '2017–21': '2017–2021', '2022–26': '2022–2026'}


def main_row(t, test):
    """Huvudurvalet i tabell1_lang.csv för samma test (None om tabell 1 inte har testet)."""
    if test in FULL: return one(T, panel='A/B', typ=t, fönster='tot', urval=FULL[test])
    if test in ('2007–16', '2017–26'): return one(T, panel='C', typ=t, urval=test)
    if test == '2017–26 minus 2007–16': return one(T, panel='D', typ=t, urval='2017–26 minus 2007–16 (decennier)')
    m = T[(T.panel == 'D') & (T.typ == t) & (T.urval == test)]
    return m.iloc[0] if len(m) == 1 else None


# "Alla" i steg 09 ska vara tabell 1 och tabell 2: samma medel och antal
for t in ['addition', 'deletion']:
    for test in TEST:
        a, b = one(N, variant=ALLA, typ=t, test=test), main_row(t, test)
        if b is None: continue
        assert abs(a.b - b.b) < 1e-9 and int(a.n) == int(b.n), (t, test, a.b, b.b)
ut = sum(int(one(N, variant=ALLA, typ=t, test='2022–26 minus 2007–11').n) - int(one(N, variant=UTAN, typ=t, test='2022–26 minus 2007–11').n)
         for t in ['addition', 'deletion'])
assert ut == N_JA, (ut, N_JA)
NJA = ut
# panel C: huvudurvalet (tabell 2) bredvid alla borttag (panel R), samma rader som panel B
PC = [(LAB[k], k, {'2007–11': '2007–2011', '2012–16': '2012–2016', '2017–21': '2017–2021', '2022–26': '2022–2026',
                   '2017–26 minus 2007–16': '2017–26 minus 2007–16 (decennier)'}.get(k, k)) for k in TEST if k != '2022–26 minus 2017–21']
def pc_main(k):
    r = main_row('deletion', k); assert r is not None, k; return r


def build(doc):
    title(doc, 'tab_news', 'Robustness: events with company news in the window, and the full sample of deletions')
    rows, cis = [], []
    for lab, t in [('Panel A. Additions', 'addition'), ('Panel B. Deletions', 'deletion')]:
        rows.append(lab)
        for test in TEST:
            a, b = one(N, variant=ALLA, typ=t, test=test), one(N, variant=UTAN, typ=t, test=test)
            rows.append([LAB.get(test, test), num(a.b) + stars(a.p_wcb), str(int(a.n)), num(b.b) + stars(b.p_wcb), str(int(b.n))])
            cis.append(len(rows)); rows.append(['', ci(a.lo, a.hi), '', ci(b.lo, b.hi), ''])
    table(doc, ['', 'CAR (%)', 'N', 'CAR (%)', 'N'], rows, [4.6, 3.6, 1.6, 3.6, 1.6], ci_rows=cis,
          group_header=[('All events', 1, 2), ('Without company news', 3, 4)])
    subhead(doc, 'Panel C. Deletions: main sample and all deletions')
    rows, cis = [], []
    for lab, k, u in PC:
        a, b = pc_main(k), one(T, panel=RP, typ='deletion', fönster='tot', urval=u)
        rows.append([lab, num(a.b) + stars(a.p_wcb), str(int(a.n)), num(b.b) + stars(b.p_wcb), str(int(b.n))])
        cis.append(len(rows)); rows.append(['', ci(a.lo, a.hi), '', ci(b.lo, b.hi), ''])
    table(doc, ['', 'CAR (%)', 'N', 'CAR (%)', 'N'], rows, [4.6, 3.6, 1.6, 3.6, 1.6], ci_rows=cis,
          group_header=[('Main sample', 1, 2), ('All deletions', 3, 4)])
    # utkast: författarna formulerar om noten
    note(doc, 'Cumulative abnormal return over [AD−1, ED+1] in per cent (stock total return minus .OMXSBGI); deletions keep their '
         f'sign. Panels A and B: following a rule written down before the search, we read the company news of the {N_GENOM} events '
         f'with an absolute CAR above 20 per cent and drop the {NJA} with a company announcement dated from AD−1 to ED+1 (interim '
         'report, takeover or merger, share issue or other capital action, large contract, regulatory decision or trial result, or '
         f'a public short report); {N_OKLART} unclear event is kept. "All events" re-estimates the sample of ' + NUM['tab_by_period'] + ' with the same '
         'draws as the column next to it, so the brackets can differ slightly from that table. Panel C: the main sample excludes ten '
         'deletions that follow a takeover offer, a merger or acquisition by the firm, a delisting application or a delisting '
         'within 100 trading days, as in Greenwood and Sammon (2025); "All deletions" keeps them. Main-sample column as in '
         f'{NUM["tab_by_period"]}. Rows as in {NUM["tab_by_period"]}: five-year periods, decades and differences (later minus '
         f'earlier). Inference: {WCR}. Brackets: {WCR_CI}. Stars from the '
         f'same draws: {STARS}.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall och stjärnor = wild cluster bootstrap per översyn (intervall genom testinversion)')
