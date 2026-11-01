# Klassar fonder i FI-data som indexfonder enligt forsta_steget_deklaration.md (22:35, förtydligande 22:41).
# In: data/fi_all_funds.csv (från fi_parse_all.py). Ut: data/fi_all_funds_klass.csv med kolumnerna ar, strikt, bred.
import re, pandas as pd, numpy as np
F = pd.read_csv('data/fi_all_funds.csv')
F['ar'] = pd.to_numeric(F.aktiv_risk.astype(str).str.replace(',', '.'), errors='coerce')
j = F.jmf.fillna('').str.lower(); n = F.namn.fillna('').str.lower()
fam = j.str.contains(r'stockholm benchmark|omxsb|sbx')
special = j.str.contains(r'esg|custom|responsible|sustainability')
namn_index = n.str.contains(r'index|indexnära|passiv|access') & ~n.str.contains('edge')
def en_komponent(s):
    delar = [p.strip() for p in re.split(r'[;|]', s) if p.strip()]
    if len(delar) == 1: return True
    return False
ensam = j.map(en_komponent) | j.str.contains(r'\b100(?:\.0+)?\s*;?\s*$')
F['strikt'] = fam & ~special & ((F.ar <= 0.5) | namn_index) & ensam
# Obs: körningen 1 november tog med fonder som saknar uppgift om aktiv risk (NaN) i den breda definitionen.
# Det avviker från deklarationens ordalydelse (aktiv risk <= 1,5) och redovisas i README_KOD.md.
F['bred'] = fam & ~(F.ar > 1.5)
F.to_csv('data/fi_all_funds_klass.csv', index=False)
print('strikt', int(F.strikt.sum()), 'bred', int(F.bred.sum()))
