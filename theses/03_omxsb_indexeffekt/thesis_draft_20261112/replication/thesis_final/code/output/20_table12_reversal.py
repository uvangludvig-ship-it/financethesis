# Tabell 12: uppgång före ändringen och återgång efter, per period, tillägg och borttag (urvalet i tabell 2).
# Ur results/reversal/reversal_results.csv (steg 15). Kontroll: jämförelsen med del1.py i results/reversal/REVERSAL.md utan
# avvikelser, och återgångsandelen = −medel CAR [ED, ED+20] / medel uppgång på samma händelser (results/reversal/reversal_events.csv).
# Körs från thesis_final efter 15: python3 code/output/20_table12_reversal.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from _style import *

R = pd.read_csv(RES / 'reversal' / 'reversal_results.csv')
E = pd.read_csv(RES / 'reversal' / 'reversal_events.csv')
assert 'Avvikelser' not in (RES / 'reversal' / 'REVERSAL.md').read_text(encoding='utf-8')
COLS = [('addition', 'alla'), ('deletion', 'utan de 10 (G&S regel)')]
MATT = [('runup', 'Run-up [AD, ED−1]'), ('car_e10', 'CAR [ED, ED+10]'), ('car_e20', 'CAR [ED, ED+20]')]
PER = [('all', '2007–26'), ('2007–2011', '2007–11'), ('2012–2016', '2012–16'), ('2017–2021', '2017–21'), ('2022–2026', '2022–26')]
AND = {}
for t, u in COLS:
    s = E[(E.type == t) & (~E.gs_ute if u.startswith('utan') else True)]; ok = s.car_e20.notna() & s.runup.notna()
    a = -s[ok].car_e20.mean() / s[ok].runup.mean(); r = one(R, typ=t, urval=u, matt='återgångsandel 20 dagar')
    assert abs(a - r.b) < 1e-12 and int(ok.sum()) == int(r.n); AND[t] = r


def build(doc):
    title(doc, 'tab_reversal', 'Run-up before and reversal after the effective date')
    rows, cis = [], []
    for p, plab in PER:
        rs = [one(R, typ=t, urval=u, matt=m, period=p) for t, u in COLS for m, _ in MATT]
        rows.append([plab] + [num(r.b) + stars(r.p_wcb) for r in rs]); cis.append(len(rows)); rows.append([''] + [ci(r.lo, r.hi) for r in rs])
    n = [one(R, typ=t, urval=u, matt=m, period='all') for t, u in COLS for m, _ in MATT]
    rows.append(['Events'] + [str(int(r.n)) for r in n])
    rows.append(['Reversal over 20 days'] + ['', '', f'{100 * AND["addition"].b:.0f} %', '', '', f'{100 * AND["deletion"].b:.0f} %'])
    table(doc, [''] + [lab.replace(' [', '\n[') for _, lab in MATT] * 2, rows, [2.6] + [2.4] * 6, ci_rows=cis,
          group_header=[('Additions', 1, 3), ('Deletions', 4, 6)])
    # utkast: författarna formulerar om noten
    note(doc, 'Mean cumulative abnormal return in per cent (stock total return minus .OMXSBGI): the run-up from the announcement to '
         'the day before the effective date, and the return over the 10 and 20 trading days from the effective date, by five-year '
         'period of the effective date. Deletions keep their sign, so a reversal shows as a positive number for deletions and a '
         'negative number for additions. Same events as ' + NUM['tab_by_period'] + '. Events: events with returns over the whole '
         'window, 2007–26. Reversal over 20 days: −CAR [ED, ED+20] divided by the run-up, on events with both. Inference: '
         f'{WCR}. Brackets: {WCR_CI}. Stars from the same draws: {STARS}.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall och stjärnor = wild cluster bootstrap per översyn (intervall genom testinversion); återgångsandelen beskrivande')
