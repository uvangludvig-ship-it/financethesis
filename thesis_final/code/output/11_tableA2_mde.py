# Tabell A2: minsta påvisbara effekt (MDE) för huvudtesterna. Ur results/mde/mde.csv (06).
# MDE = (t_0,975 + t_0,80) * SE med G−1 frihetsgrader: 5 % test, 80 % styrka. Analytiskt, ingen bootstrap.
# Körs från thesis_final efter 06: python3 code/output/11_tableA2_mde.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from _style import *

D = pd.read_csv(RES / 'mde' / 'mde.csv')
assert (D.metod.str.startswith('analytiskt')).all() and len(D) == 6
LAB = {('addition', '2022–26 minus 2017–21'): ('Fall in the addition effect, 2022–26 minus 2017–21', NUM['tab_by_period']),
       ('addition', '2017–26 minus 2007–16 (decennier)'): ('Fall in the addition effect, 2017–26 minus 2007–16', NUM['tab_by_period']),
       ('addition', '2017–26'): ('Addition effect, 2017–26', NUM['tab_by_period']),
       ('addition', '2022–26'): ('Addition effect, 2022–26', NUM['tab_by_period']),
       ('deletion', '2017–26'): ('Deletion effect, 2017–26', NUM['tab_by_period']),
       ('addition', 'M 2017–21 minus M 2022–26'): ('Change in M for additions, 2017–21 minus 2022–26', NUM['tab_controls'])}


def build(doc):
    title(doc, 'tab_mde', 'Minimum detectable effects')
    rows = []
    for _, r in D.iterrows():
        lab, src = LAB[(r.typ, r.test)]
        rows.append([lab, src, num(r.se, 3), str(int(r.G)), num(r.mde)])
    table(doc, ['Test', 'Estimate in', 'SE', 'Reviews', 'MDE'], rows, [7.2, 2.4, 1.8, 1.8, 1.8])
    note(doc, 'Minimum detectable effect for a two-sided 5 per cent test with 80 per cent power: MDE = (t_0.975 + t_0.80) × SE, '
         'with G − 1 degrees of freedom, where SE is the standard error clustered by review and G the number of reviews. Analytic, '
         'no bootstrap. Units: per cent abnormal return, except the change in M (per cent return per per cent of shares). SE is '
         'left blank where the MDE was computed directly from the estimate\'s file.')


if __name__ == '__main__':
    run(build, '11_tableA2_mde')
    print('Metod: MDE analytiskt, (t_0,975 + t_0,80) * CR1-SE, G-1 frihetsgrader')
