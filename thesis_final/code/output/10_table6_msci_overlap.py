# Tabell 6 (jämför G&S Table VIII, andra index): indexeffekten och M med och utan händelser som sammanfaller med MSCI Sweden.
# Ur results/msci_overlap/resultat_car.csv och resultat_m.csv (05). Överlapp = samma bolag ändras i MSCI Sweden inom ±10 handelsdagar.
# CAR: wild cluster bootstrap (testinversion). M: parvis klusterbootstrap, percentil. Bara överlapp: beskrivande medel.
# Körs från thesis_final efter 05: python3 code/output/10_table6_msci_overlap.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

C = pd.read_csv(RES / 'msci_overlap' / 'resultat_car.csv')
M = pd.read_csv(RES / 'msci_overlap' / 'resultat_m.csv')
T1 = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
SAMPLES = PERS_KORT + ['2017–26']
assert C[C.variant != 'bara överlapp (beskrivande)'].ci_metod.str.startswith('95 % intervall: invertering').all()
for t in ['addition', 'deletion']:   # "alla" ska vara samma skattning som tabell 2
    for p, pl in zip(PERS_KORT, PERS):
        assert abs(one(C, typ=t, urval=p, variant='alla').b - one(T1, panel='A/B', typ=t, fönster='tot', urval=pl).b) < 1e-9, (t, p)
        assert int(one(C, typ=t, urval=p, variant='alla').n) == int(one(T1, panel='A/B', typ=t, fönster='tot', urval=pl).n)
for _, r in C[C.variant == 'utan överlapp'].iterrows():
    assert r.n == one(C, typ=r.typ, urval=r.urval, variant='alla').n - r.n_overlapp, (r.typ, r.urval)


def build(doc):
    title(doc, 'tab_msci', 'The index effect with and without overlapping MSCI Sweden changes')
    rows, cis = [], []
    for t, lab in [('addition', 'Panel A. Additions'), ('deletion', 'Panel B. Deletions')]:
        rows.append(lab)
        for p in SAMPLES:
            a, x = one(C, typ=t, urval=p, variant='alla'), one(C, typ=t, urval=p, variant='utan överlapp')
            o = C[(C.typ == t) & (C.urval == p) & (C.variant == 'bara överlapp (beskrivande)')]
            ob = num(o.iloc[0].b) if len(o) else ''
            rows.append([p, num(a.b) + stars(a.p), str(int(a.n)), num(x.b) + stars(x.p), str(int(x.n)), ob, str(int(a.n_overlapp))])
            cis.append(len(rows)); rows.append(['', ci(a.lo, a.hi), '', ci(x.lo, x.hi), '', '', ''])
    table(doc, ['Period', 'CAR', 'N', 'CAR', 'N', 'CAR', 'N'], rows, [2.4, 2.9, 1.3, 2.9, 1.3, 2.0, 1.3], ci_rows=cis,
          group_header=[('All events', 1, 2), ('Excluding overlap', 3, 4), ('Overlap only', 5, 6)])

    subhead(doc, 'Panel C. Multiplier M, baseline window')
    rows, cis = [], []
    for _, r in M.iterrows():
        lab = ('Additions' if r.typ == 'addition' else 'Deletions') + f', {r.urval}, ' + ('all events' if r.variant == 'alla' else 'excluding overlap')
        rows.append([lab, str(int(r.n)), num(r.car * (1 if r.typ == 'addition' else -1)), num(r.D_V * (1 if r.typ == 'addition' else -1)), num(r.M)])
        cis.append(len(rows)); rows.append(['', '', '', '', ci(r.lo, r.hi)])
    table(doc, ['', 'N', 'CAR (%)', 'D̄ (%)', 'M'], rows, [7.4, 1.6, 2.4, 2.4, 3.0], ci_rows=cis)
    note(doc, 'An event overlaps when the same company is added to or deleted from the MSCI Sweden index within ten trading days of '
         'the OMXSB effective date. Panels A and B: mean cumulative abnormal return over [AD−1, ED+1] in per cent; All events '
         f'equals {NUM["tab_by_period"]}. Inference: {WCR}; brackets are {WCR_CI}; {STARS}. Overlap only: descriptive mean, no '
         f'inference. Panel C: M as in {NUM["tab_multiplier"]}; brackets from a {PAIRS}. Deletions in 2017–21 and 2022–26 are shown '
         'only for all events because they have three overlapping events each.')


if __name__ == '__main__':
    run(build, '10_table6_msci_overlap')
    print('Metod: CAR = wild cluster bootstrap (testinversion); M = parvis klusterbootstrap, percentil; bara överlapp beskrivande')
