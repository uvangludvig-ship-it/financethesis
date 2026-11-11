# Tabell 6 (G&S Table VI): M per period i en regression, utan och med kontroller.
# CAR_i = sum_k M_k * 1{period k} * D̄_k + b' kontroller + e (kontroller centrerade: omsättning, storlek, Wurgler-Zhuravskaya, analytiker).
# Ur results/fund_demand/omrakning_resultat.csv, tabell 6 (02), skikt D_C (huvudmåttet), fönster [AD−1, ED+1], utan split.
# Intervall: M per period = analytiskt (CR1 per översyn, t med G−1); skillnader = wild cluster bootstrap (testinversion), stjärnor därifrån.
# Körs från thesis_final efter 02: python3 code/output/12_table6_multiplier_controls.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

R = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv')
R6 = R[(R.tabell == 6) & (R.skikt == 'D_C') & (R.fonster == 'y_tot')].copy()
R6['kontroller'] = R6.kontroller.astype(str).str.lower().map({'true': True, 'false': False})
DIFFS = [('M 2007–11 − M 2022–26', '2007–11 − 2022–26'), ('M 2012–16 − M 2022–26', '2012–16 − 2022–26'),
         ('M 2017–21 − M 2022–26', '2017–21 − 2022–26')]
COLS = [(t, k) for t in ['addition', 'deletion'] for k in [False, True]]
for t, k in COLS:
    for p in PERS_KORT: assert one(R6, typ=t, kontroller=k, period=f'M {p}').ci_metod.startswith('95 % intervall: analytiskt')
    for d, _ in DIFFS: assert one(R6, typ=t, kontroller=k, period=d).ci_metod.startswith('95 % intervall: invertering')
# tabell 3 och tabell 4 utan kontroller ska ge samma M per period (kvoten och regressionen är samma skattning när D̄ per period används)
R5 = R[(R.tabell == 5) & (R.skikt == 'D_C') & (R.fonster == 'y_tot')]
for t in ['addition', 'deletion']:
    for p in PERS_KORT:
        a, b = one(R5, typ=t, period=p).M, one(R6, typ=t, kontroller=False, period=f'M {p}').b
        assert abs(a - b) < 1e-6, (t, p, a, b)


def build(doc):
    title(doc, 'tab_controls', 'The multiplier M with and without controls')
    rows, cis = [], []
    for p in PERS_KORT:
        rs = [one(R6, typ=t, kontroller=k, period=f'M {p}') for t, k in COLS]
        rows.append([f'M, {p}'] + [num(r.b) for r in rs]); cis.append(len(rows)); rows.append([''] + [ci(r.lo, r.hi) for r in rs])
    rows.append('Differences')
    for d, lab in DIFFS:
        rs = [one(R6, typ=t, kontroller=k, period=d) for t, k in COLS]
        rows.append([lab] + [num(r.b) + stars(r.p) for r in rs]); cis.append(len(rows)); rows.append([''] + [ci(r.lo, r.hi) for r in rs])
    rows.append(['Events'] + [str(int(R6[(R6.typ == t) & (R6.kontroller == k) & R6.period.isin([f'M {p}' for p in PERS_KORT])].n_period.sum())) for t, k in COLS])
    rows.append(['Reviews'] + [str(int(one(R6, typ=t, kontroller=k, period='M 2022–26').G)) for t, k in COLS])
    rows.append(['Controls', 'No', 'Yes', 'No', 'Yes'])
    table(doc, ['', 'No controls', 'Controls', 'No controls', 'Controls'], rows, [4.8, 3.05, 3.05, 3.05, 3.05], ci_rows=cis,
          group_header=[('Additions', 1, 2), ('Deletions', 3, 4)])
    note(doc, 'Following Greenwood and Sammon (2025, Table VI), we estimate CAR_i = Σ_k M_k · 1{period k} · D̄_k + b′X_i + e_i '
         'separately for additions and deletions, where CAR_i is the cumulative abnormal return over [AD−1, ED+1] in the direction '
         'of index trading, D̄_k is the mean net demand of OMXSB index trackers in period k (per cent of shares outstanding), and X_i '
         'holds turnover, size, the Wurgler–Zhuravskaya arbitrage-risk measure and analyst coverage, measured before the '
         'announcement and centred. Without controls M_k equals the ratio in ' + NUM['tab_multiplier'] + '. Brackets under M: 95 '
         f'per cent confidence intervals from {CR1}. Differences: {WCR}; brackets are {WCR_CI}; stars from the same draws: {STARS}. '
         'The 2007–11 period has few events with fund data, so its difference is imprecise.'
         + ' Deletions caused by a takeover, merger, distressed share issue or a large change in shares outstanding (19 events) are '
         'excluded from the fund demand sample.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: M per period = analytiskt (CR1, t med G-1); skillnader = wild cluster bootstrap (testinversion), stjärnor från samma bootstrap')
