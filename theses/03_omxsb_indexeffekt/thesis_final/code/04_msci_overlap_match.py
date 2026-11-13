# Runda 14, steg 1: OMXSB-händelser x MSCI Sweden-ändringar i samma bolag, MSCI-genomförande inom ±10 handelsdagar från OMXSB:s ED.
# Ingen avkastning läses. Handgranskningen (3 felmatchningar) är inskriven nedan så att körningen är reproducerbar.
# Körs från thesis_final: python3 code/04_msci_overlap_match.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import os, re, unicodedata, pandas as pd, numpy as np
HERE = RES / 'msci_overlap'; os.makedirs(HERE, exist_ok=True)
M = pd.read_csv(DATA / 'msci' / 'msci_sweden_changes_2007_2026.csv', parse_dates=['effective_date'])
E = pd.read_csv(DATA / 'events' / 'omxsb_changes_nasdaq_2007_2026.csv', parse_dates=['effective_date'])
ix = pd.read_csv(DATA / 'prices' / 'index_levels_daily_2004_2026.csv', parse_dates=['date'])
cal = pd.DatetimeIndex(sorted(ix.loc[(ix.ric == '.OMXSBGI') & ix.close.notna(), 'date'].unique()))
pos = lambda d: int(np.searchsorted(cal.values, np.datetime64(d)))
STOP = {'ab','publ','ser','serie','series','sdb','class','a','b','c','d','r','the','ltd','plc','oyj','asa','sa','corp','corporation','inc','group','holding',
        'holdings','co','och','aktiebolag','aktiebolaget','international','int','intl','svenska','fastighets','fastigheter','invest','investment','investmentab','l','e'}
def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    return [w for w in re.sub(r'[^a-z0-9 ]', ' ', s).split() if w not in STOP and len(w) > 1]
key = lambda s: (norm(s) or [''])[0]
E['k'] = E.company.map(key); M['k'] = M.security.map(key); E['p'] = E.effective_date.map(pos); M['p'] = M.effective_date.map(pos)
rows = []
for e in E.itertuples():
    for m in M[(M.k == e.k) & (M.k != '') & ((M.p - e.p).abs() <= 10)].itertuples():
        rows.append(dict(event_id=e.event_id, omxsb_bolag=e.company, ticker=e.ticker, omxsb_typ=e.type, omxsb_ED=e.effective_date.date(),
                         msci_namn=m.security, msci_segment=m.segment, msci_typ=m.change, msci_ED=m.effective_date.date(),
                         handelsdagar=m.p - e.p, samma_riktning=(e.type == m.change)))
C = pd.DataFrame(rows)
FEL = {('OMXSB-2009H1-02', 'NET INSIGHT B'): 'fel bolag (Net Insight, inte Net Entertainment)',
       ('OMXSB-2010H1-07', 'LUNDIN PETROLEUM'): 'fel bolag (Lundin Petroleum, inte Lundin Mining)',
       ('OMXSB-2019H2-02', 'CATENA MEDIA'): 'fel bolag (Catena Media, inte Catena)'}
C['granskning'] = [FEL.get((e, n), 'samma bolag') for e, n in zip(C.event_id, C.msci_namn)]
C.to_csv(os.path.join(HERE, 'matchning.csv'), index=False)
ok = C[C.granskning == 'samma bolag']
ev = ok.groupby('event_id').agg(omxsb_typ=('omxsb_typ', 'first'), ED=('omxsb_ED', 'first'), samma=('samma_riktning', 'max'),
                                motsatt=('samma_riktning', lambda s: (~s).any()), msci=('msci_namn', lambda s: '; '.join(s)))
ev['riktning'] = ['samma' if s and not m else ('motsatt' if m and not s else 'blandat (migration inom MSCI)') for s, m in zip(ev.samma, ev.motsatt)]
ev.to_csv(os.path.join(HERE, 'overlapp_handelser.csv'))
print(len(C), 'kandidatpar;', len(ev), 'överlappande OMXSB-händelser')
