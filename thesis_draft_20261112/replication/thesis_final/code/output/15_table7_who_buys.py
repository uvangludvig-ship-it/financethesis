# Tabell 7 (G&S Table VII): vem handlar vid tillägg och borttag. Nettoköp per fondgrupp i procent av aktierna, per period.
# Ur results/fund_demand/omrakning_resultat.csv, tabell 7 (02), utan split, händelser med fonddata.
# Tecken: positivt = i indexfondernas riktning (köp vid tillägg, försäljning vid borttag), som i 02.
# Intervall: analytiskt (CR1 per översyn), utom aktiva fonder 2017–26 som är wild cluster bootstrap (testinversion); markeras med †.
# Körs från thesis_final efter 02: python3 code/output/15_table7_who_buys.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

R = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv')
R7 = R[R.tabell == 7]
SAMPLES = PERS_KORT + ['2017–26']
GROUPS = [('D_C', 'OMXSB index trackers (C)'), ('D_B', '  Pure index funds (B)'), ('V_bara', '  Tracker variants'),
          ('C_bara', '  Balanced funds, OMXSB share'), ('passiva_ovriga', 'Other passive funds'),
          ('aktiva', 'Active funds'), ('alla_fonder', 'All funds')]
SUB = ['B_bara', 'n_övriga passiva, svenska', 'n_övriga passiva, utländska', 'n_OMXS30', 'n_småbolagsindex']   # i CSV, inte i tabellen
BOOT = R7.ci_metod.str.startswith('95 % intervall: invertering')
assert set(map(tuple, R7[BOOT][['period', 'grupp']].values)) == {('2017–26', 'aktiva')}, 'bootstrap bara för aktiva 2017–26'
for t in ['addition', 'deletion']:
    for p in SAMPLES:
        g = {k: one(R7, typ=t, period=p, grupp=k).b for k in [k for k, _ in GROUPS] + SUB}
        assert abs(g['D_C'] - g['B_bara'] - g['V_bara'] - g['C_bara']) < 1e-9 and abs(g['D_B'] - g['B_bara']) < 1e-9, (t, p, 'D_C = B + V + C')
        assert abs(g['passiva_ovriga'] - g['n_övriga passiva, svenska'] - g['n_övriga passiva, utländska']
                   - one(R7, typ=t, period=p, grupp='n_OMXS30').b - one(R7, typ=t, period=p, grupp='n_småbolagsindex').b) < 1e-9, (t, p)
        assert abs(g['alla_fonder'] - g['D_C'] - g['passiva_ovriga'] - g['aktiva']) < 1e-6, (t, p, 'summan')


def build(doc):
    title(doc, 'tab_who_buys', 'Net buying and selling by fund group around OMXSB index changes')
    rows, cis = [], []
    for t, lab in [('addition', 'Panel A. Additions: net buying'), ('deletion', 'Panel B. Deletions: net selling')]:
        rows.append(lab)
        for k, kl in GROUPS:
            rs = [one(R7, typ=t, period=p, grupp=k) for p in SAMPLES]
            rows.append([kl] + [num(r.b) + ('†' if r.ci_metod.startswith('95 % intervall: invertering') else '') for r in rs])
            cis.append(len(rows)); rows.append([''] + [ci(r.lo, r.hi) for r in rs])
        rows.append(['Events'] + [str(int(one(R7, typ=t, period=p, grupp='D_C').n)) for p in SAMPLES])
        rows.append(['Reviews'] + [str(int(one(R7, typ=t, period=p, grupp='D_C').G)) for p in SAMPLES])
    table(doc, [''] + SAMPLES, rows, [5.5, 2.25, 2.25, 2.25, 2.25, 2.25], ci_rows=cis)
    note(doc, 'Mean change in shares held by each fund group between the fund report before the announcement and the report after '
         'the effective date, in per cent of shares outstanding, signed in the direction of index trading: positive numbers are '
         'purchases at additions and sales at deletions. Fund holdings from LSEG Lipper; events with a share split between the '
         f'reports are excluded. {TRACKERS[0].upper() + TRACKERS[1:]}; the indented rows split them into their three parts. Balanced funds count with the OMXSB '
         'weight in their benchmark. Other passive funds are index funds that do not track the OMXSB, Swedish and foreign-domiciled. '
         'All funds is '
         f'the sum of the groups. Brackets: 95 per cent confidence intervals from {CR1}, except † where the interval is from a '
         f'{WCR} ({WCR_CI}). Comparable to Greenwood and Sammon (2025, Table VII), who compare index trackers with all 13F institutions.'
         + ' Deletions caused by a takeover, merger, distressed share issue or a large change in shares outstanding (19 events) are '
         'excluded from the fund demand sample.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: intervall analytiska (CR1, t med G-1), utom aktiva fonder 2017–26 (†) = wild cluster bootstrap med testinversion')
