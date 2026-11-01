# Verifierad medlemstabell för OMXSB per översyn, med dokumenterade rättelser.
# Ut: medlemskap_verifierad.csv (review, ric, status = medlem | osäker), medlemskap_kontroll.txt
import pandas as pd, numpy as np, re, os, sys
R = os.environ.get('ROOT', '../..')
mem = pd.read_csv(f'{R}/output/omxsb_replication_2007/mechanisms/omxsb_membership_by_review.csv')
ch = pd.read_csv(f'{R}/data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
ev = pd.read_csv(f'{R}/output/omxsb_replication_2007/events_car.csv', parse_dates=['AD', 'ED'])
cyc = list(ev.groupby('review_cycle').AD.first().sort_values().index)
after = {r.review_cycle: set(str(r.members_after).split(';')) for r in mem.itertuples()}

# 1. Tickernycklar utan RIC i panelen
TICK = {'T:NDA SEK': 'NDASE.ST', 'T:TIEN': 'TIETOS.ST'}          # Stockholmsrader hämtade från LSEG 2026-11-01
SAKNAR_DATA = {'T:TRAD', 'T:OPCO', 'T:TAGR', 'T:NOCM B'}          # inga kurser i panelen eller LSEG

# 2. Rättelser av brott i medlemskedjan (gäller medlemmar EFTER översynen; 'osäker' = uteslut ur kontrollgrupper)
def span(a, b): return cyc[cyc.index(a):cyc.index(b) + 1]
RATT = []
RATT += [(c, 'NOKIA.ST', 'osäker', 'tillägg saknas mellan borttaget 2009H1 och borttaget 2011H1') for c in span('2009H1', '2011H1')[:-1]]
RATT += [(c, 'ENQ.ST^L23', 'osäker', 'avknoppad från Lundin Petroleum 2010, kom in utan granskning, borttagen 2011H2') for c in span('2010H1', '2011H2')[:-1]]
RATT += [(c, 'CDONAB.ST', 'osäker', 'avknoppad från MTG december 2010, borttagen 2011H1') for c in span('2010H2', '2011H1')[:-1]]
RATT += [(c, 'COREb.ST', 'medlem', 'kom in via Corems köp av Klövern 2021, borttagen 2022H2') for c in span('2021H1', '2022H2')[:-1]]
RATT += [(c, k, 'osäker', 'Collector/Norion: tillägg saknas i ändringslistan, borttagen 2026H1') for c in span('2015H2', '2026H1')[:-1] for k in ['NORION.ST', 'COLLAX.ST', 'COLLE.ST^H22']]
RATT += [(c, 'SAMPO.ST', 'medlem', 'samma bolag som medlemmen SAMPOsdb, direktnotering') for c in span('2023H1', '2026H1')[:-1]]
TA_BORT = [(c, k, 'avnoterad efter Corems köp 2021') for c in span('2021H1', '2026H1') for k in ['KLOVa.ST^G21', 'KLOVb.ST^G21']]

rows, log = [], []
for c in cyc:
    for k in after.get(c, set()):
        if k in SAKNAR_DATA: rows.append((c, k, 'saknar_data', 'ticker utan kurser')); continue
        r = TICK.get(k, k)
        if r.startswith('T:'): log.append(f'OLÖST {c} {k}'); continue
        rows.append((c, r, 'medlem', 'kedja' if r == k else 'tickerkoppling'))
for c, k, s, why in RATT: rows.append((c, k, s, why))
V = pd.DataFrame(rows, columns=['review_after', 'ric', 'status', 'kalla'])
V = V.drop_duplicates(['review_after', 'ric'], keep='last')
for c, k, why in TA_BORT: V = V[~((V.review_after == c) & (V.ric == k))]
V.to_csv('medlemskap_verifierad.csv', index=False)

# Kontroll: varje borttag ska vara medlem (eller osäker) före, varje tillägg icke-medlem före
def members_after(c, inkl_osaker=True):
    s = V[(V.review_after == c) & (V.status.isin(['medlem', 'osäker'] if inkl_osaker else ['medlem']))]
    return set(s.ric)
def key(r, t):
    if isinstance(r, str) and r:
        return 'NOKIA.ST' if r == 'NOKIsdb.ST^E07' else r
    return TICK.get('T:' + str(t).strip(), 'T:' + str(t).strip())
ch['key'] = [key(r, t) for r, t in zip(ch.RIC, ch.ticker)]
fel = []
for i, c in enumerate(cyc[1:], 1):
    before = members_after(cyc[i - 1])
    for _, e in ch[ch.review_cycle == c].iterrows():
        if e.key.startswith('T:') and e.key in SAKNAR_DATA | {'T:' + x for x in []}: continue
        if e.type == 'deletion' and e.key not in before: fel.append((c, 'borttagen men inte medlem', e.key))
        if e.type == 'addition' and e.key in before: fel.append((c, 'tillagd men redan medlem', e.key))
fel = [f for f in fel if not f[2].startswith('T:')]
with open('medlemskap_kontroll.txt', 'w') as f:
    f.write(f'översyner {len(cyc)}; rader {len(V)}; olösta nycklar {len(log)}\n')
    f.write('\n'.join(log) + '\n')
    f.write(f'brott i kedjan efter rättelser: {len(fel)}\n' + '\n'.join(map(str, fel)) + '\n')
    f.write(V.groupby('status').size().to_string() + '\n')
    f.write(V[V.status == 'medlem'].groupby('review_after').size().describe().to_string() + '\n')
print(open('medlemskap_kontroll.txt').read())
if log: sys.exit('STOPP: olösta medlemsnycklar')
