# Tabell A6: fonderna i fondlistan, deras cirkel per period och förmögenhet, rangordnade efter förmögenheten december 2025.
# Ur results/fund_demand/fondtabell_aum.csv (02). Förmögenhet = hela fondens (SHoF, mdkr); "räknas" = den del som ingår i
# ägarandelen i figur 4 (bara inom följarperioden, blandfonder vägda med OMXSB-andelen i jämförelseindexet).
# Kontroll: summan av "räknas" december 2025 = C i results/fund_demand/shof_aum_skikt.csv.
# Skriver också results/tables/26_tableA6_fund_list.csv (samma tabell, för vidare bruk).
# Körs från thesis_final efter 02: python3 code/output/26_tableA6_fund_list.py
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

F = pd.read_csv(RES / 'fund_demand' / 'fondtabell_aum.csv')
S = pd.read_csv(RES / 'fund_demand' / 'shof_aum_skikt.csv')
SIST = F.sista_manad.iloc[0]
assert abs(F['raknas_2025-12'].sum() - one(S, manad='2025-12').C_mdkr) < 1e-6, 'räknad förmögenhet ska summera till C'
CIRKEL = {'B': 'B', 'V': 'V', 'C': 'C', 'X': 'X'}


def cirklar(s):   # "B 2008–2022; X 2022–2025; V 2025–" i startordning; odaterade X-rader = hela perioden
    d = []
    for x in s.split('; '):
        c, per = x.split(' ', 1); a, b = per.split('–')
        d.append((0 if a == '…' else int(a), c, 'not a tracker' if (c == 'X' and a == '…') else f'{"" if a == "…" else a}–{b}'))
    return '; '.join(f'{c} {p}' for _, c, p in sorted(d))


def kort(f): return re.split(r' \(| / ', f)[0]


def tillv(a, b): return 100 * (b / a - 1) if pd.notna(a) and pd.notna(b) and a > 0.05 else np.nan   # under 50 mnkr: fonden fanns knappt


F['Fund'] = F.fond.map(kort); F['Circles'] = F.cirklar.map(cirklar)
F['growth_2015_25'] = [tillv(a, b) for a, b in zip(F['aum_2015-12'], F['aum_2025-12'])]
F['growth_2020_25'] = [tillv(a, b) for a, b in zip(F['aum_2020-12'], F['aum_2025-12'])]
F = F.sort_values(['aum_2025-12', 'fond'], ascending=[False, True], na_position='last').reset_index(drop=True)
F['rank'] = np.where(F['aum_2025-12'].notna(), np.arange(1, len(F) + 1), np.nan)
UT = F[['rank', 'Fund', 'fond', 'Circles', 'cirkel_nu', 'aum_2015-12', 'aum_2020-12', 'aum_2025-12', f'aum_{SIST}', 'growth_2015_25',
        'growth_2020_25', 'raknas_2025-12', f'raknas_{SIST}', 'shof_namn', 'status']]
OUT.mkdir(parents=True, exist_ok=True); UT.to_csv(OUT / f'{Path(__file__).stem}.csv', index=False)


def build(doc):
    title(doc, 'tab_funds', 'The funds in the tracker list: circle, assets and growth')
    pc = lambda v: '' if pd.isna(v) else num(v, 0)
    rows = []
    for _, r in F.iterrows():
        rows.append([str(int(r['rank'])) if pd.notna(r['rank']) else '', r.Fund, r.Circles, num(r['aum_2015-12'], 1), num(r['aum_2020-12'], 1),
                     num(r['aum_2025-12'], 1), pc(r.growth_2020_25), num(r['raknas_2025-12'], 1)])
    rows.append(['', 'Total counted in the ownership share', '', '', '', '', '', num(F['raknas_2025-12'].sum(), 1)])
    table(doc, ['', 'Fund', 'Circle', '2015', '2020', '2025', 'Growth 2020–25 (%)', 'Counted, 2025'], rows,
          [0.8, 4.6, 3.3, 1.2, 1.2, 1.2, 1.8, 1.8], group_header=[('Assets, SEK bn (December)', 3, 5)], left=(0, 1, 2))
    # utkast: författarna formulerar om noten
    note(doc, 'All funds in the tracker list, ranked by total assets in December 2025 (SHoF fund database, SEK billion, all share '
         'classes). Circle: B = pure OMXSB index funds, V = B plus tracker variants, C = V plus the OMXSB share of balanced funds, '
         'X = indexed or close to the index but not a tracker, with the years the fund belongs to each circle. A fund counts as a '
         'tracker while its documents or its holdings (at least half of the index trades) show it tracking the OMXSB. '
         'Counted 2025: the part of the assets that enters the ownership share in ' + NUM['fig_ownership'] + ' (main measure C): '
         'zero outside the tracker period, and for balanced funds the assets times the OMXSB weight in their benchmark. Growth: '
         'change in total assets, not shown when the fund had less than SEK 50 million at the start. Funds without assets are '
         'foreign-domiciled and not in the SHoF database (they count in the net buying D from LSEG Lipper, but not in the '
         f'ownership share). Assets for the latest month ({SIST}) are in the CSV file next to this table.')


if __name__ == '__main__':
    run(build, Path(__file__).stem)
    print('Metod: beskrivande (förmögenhet per fond), ingen inferens')
