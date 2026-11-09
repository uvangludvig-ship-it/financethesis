# Minsta påvisbara effekt (MDE) för huvudtesterna. Ingen ny skattning: bara aritmetik på
# standardfel som 01_effect_table.py, 02_fund_demand.py och 05_msci_overlap_results.py redan skrivit.
# MDE = (t_0,975 + t_0,80) * SE med G-1 frihetsgrader (5 % test, 80 % styrka).
# Körs från thesis_final efter 01, 02 och 05: python3 code/06_mde.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import pandas as pd
from scipy.stats import t

T1 = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
R13 = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv')
R14 = pd.read_csv(RES / 'msci_overlap' / 'resultat_car.csv')


def mde(se, G):
    return (t.ppf(0.975, G - 1) + t.ppf(0.80, G - 1)) * se


rader = []
for typ, urval in [('addition', '2022–26 minus 2017–21'), ('addition', '2017–26 minus 2007–16 (decennier)')]:
    r = T1[(T1.panel == 'D') & (T1.typ == typ) & (T1.urval == urval)].iloc[0]
    rader.append(('tabell1 panel D', typ, urval, r.se, int(r.G), mde(r.se, int(r.G))))
for typ, urval in [('addition', '2017–26'), ('addition', '2022–26'), ('deletion', '2017–26')]:
    r = R14[(R14.typ == typ) & (R14.urval == urval) & (R14.variant == 'alla')].iloc[0]
    rader.append(('runda 14, alla', typ, urval, float('nan'), int(r.G), r.mde))
r = R13[(R13.tabell == 6) & (R13.typ == 'addition') & (R13.skikt == 'D_V') & (R13.fonster == 'y_tot')
        & (R13.period == 'M 2017–21 − M 2022–26')].iloc[0]          # första förekomsten: alla händelser utan split
rader.append(('runda 13 tabell 6', 'addition', 'M 2017–21 minus M 2022–26', r.se, int(r.G), mde(r.se, int(r.G))))

ut = pd.DataFrame(rader, columns=['källa', 'typ', 'test', 'se', 'G', 'mde'])
os.makedirs(RES / 'mde', exist_ok=True); ut.to_csv(RES / 'mde' / 'mde.csv', index=False)
print(ut.round(3).to_string(index=False))
