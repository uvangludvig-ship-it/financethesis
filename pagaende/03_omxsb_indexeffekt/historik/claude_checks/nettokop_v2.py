# Nettoköp v2 (2 nov 2026): OMXSB-indexfonder definieras efter innehav per kvartal (agar_kontroll/indexfond_innehav.csv),
# och en fond räknas bara om den är OMXSB-indexfond både kvartalet före och kvartalet efter (fonder som byter index räknas inte som köp).
# Körs från code/claude_checks efter agar_kontroll/indexfond_innehav.py. Övriga familjer som i nettokop.py. Beskrivande, inga avkastningar används utom CAR för kvoten.
import os, re
import numpy as np, pandas as pd
R = os.environ.get('REPO', '../..')
D = os.environ.get('DATA', 'data')
K = pd.read_csv(os.environ.get('KLASS', 'agar_kontroll/indexfond_innehav.csv'), dtype={'fund_id': str})
H = pd.read_pickle(os.environ.get('HOLD', 'data/fi_all_holdings.pkl'))
H['antal'] = pd.to_numeric(H.antal.astype(str).str.replace(',', '.').str.replace(' ', ''), errors='coerce')
H = H[H.antal > 0].copy(); H['fund_id'] = H.fund_id.astype(str); H['kv'] = pd.to_datetime(H.kvartal)
F = pd.read_csv(os.path.join(D, 'fi_all_funds_klass.csv')); F['fund_id'] = F.fund_id.astype(str); F['kv'] = pd.to_datetime(F.kvartal)
j = F.jmf.fillna('').str.lower(); n = F.namn.fillna('').str.lower()
indexlik = F.bred.astype(bool) | n.str.contains(r'index|indexnära|passiv|xact|exponering|\betf\b')
def familj(s):
    if re.search(r'stockholm benchmark|omxsb|sbx', s): return 'OMXSB'
    if re.search(r'small ?cap|småbolag|carnegie|csrx|csxse|mikro|omxsse', s): return 'småbolag'
    if re.search(r'six|omxs ?gi|all ?share|omxspi|stockholm total return|stockholm gi', s): return 'hela börsen'
    return 'övriga'
F['familj'] = np.where(indexlik, j.map(familj), 'ej index')
qmap = dict(zip(F.q, F.kv)); K['kv'] = K.q.map(qmap)
OMX = K[K.omxsb_index].groupby('kv').fund_id.agg(set).to_dict()            # ny definition per kvartal
F.loc[[(f in OMX.get(k, set())) for k, f in zip(F.kv, F.fund_id)], 'familj'] = 'OMXSB_ny'
F.loc[(F.familj == 'OMXSB'), 'familj'] = 'OMXSB_gammal_ej_ny'             # gamla OMXSB-indexlika som inte följer enligt innehavet
FAM = F.set_index(['kv', 'fund_id']).familj.to_dict()
H['familj'] = [FAM.get((k, f), 'ej index') for k, f in zip(H.kv, H.fund_id)]
HF = H.groupby(['isin', 'kv', 'fund_id']).antal.sum()
G = H[H.familj != 'ej index'].groupby(['isin', 'kv', 'familj']).antal.sum()
qs = sorted(H.kv.unique()); first_seen = H.groupby('isin')['kv'].min().to_dict()
tu = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/td_universe.csv'); st = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/stocks_static_2005.csv')
isin = dict(zip(tu.RIC, tu.IssueISIN)); isin.update({k: v for k, v in zip(st.ric, st.IssueISIN) if isinstance(v, str)})
px = pd.read_csv(os.path.join(D, 'panel_utdrag.csv.gz'), usecols=['ric', 'date', 'shares'], parse_dates=['date'])
e = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'del1_events.csv'), parse_dates=['AD', 'ED'])
e = e[e.AD >= '2018-12-01'].copy()
car = pd.read_csv(f'{R}/output/omxsb_replication_2007/events_car.csv').set_index(['RIC', 'review_cycle']).tot_gi
def fundsum(i, q, funds): return sum(HF.get((i, q, f), 0.0) for f in funds)
rows = []
for x in e.itertuples():
    i = isin.get(x.RIC); pre = [q for q in qs if q < x.AD]; post = [q for q in qs if q >= x.ED]
    if not isinstance(i, str) or not pre or not post or first_seen.get(i, pd.Timestamp('2100-01-01')) > pre[-1]:
        rows.append(dict(RIC=x.RIC, review=x.review_cycle, type=x.type, status='ISIN eller kvartal saknas')); continue
    q0, q1 = pre[-1], post[0]
    s = px[(px.ric == x.RIC) & (px.date <= q1)].dropna(subset=['shares']).tail(1)
    if s.empty or not s.shares.iloc[0] > 0:
        rows.append(dict(RIC=x.RIC, review=x.review_cycle, type=x.type, status='antal aktier saknas')); continue
    sh = s.shares.iloc[0]; sign = 1 if x.type == 'addition' else -1
    stab = OMX.get(q0, set()) & OMX.get(q1, set()); bada_ena = OMX.get(q0, set()) | OMX.get(q1, set())
    d = dict(RIC=x.RIC, review=x.review_cycle, type=x.type, status='ok', q0=q0.date(), q1=q1.date(), n_omxsb_stabila=len(stab),
             netto_OMXSB_ny=sign * 100 * (fundsum(i, q1, stab) - fundsum(i, q0, stab)) / sh,
             netto_OMXSB_ny_inkl_bytare=sign * 100 * (fundsum(i, q1, OMX.get(q1, set())) - fundsum(i, q0, OMX.get(q0, set()))) / sh,
             fore_OMXSB_ny=100 * fundsum(i, q0, stab) / sh)
    for fam in ['OMXSB_gammal_ej_ny', 'småbolag', 'hela börsen', 'övriga']:
        b0 = G.get((i, q0, fam), 0.0); b1 = G.get((i, q1, fam), 0.0); d[f'netto_{fam}'] = sign * 100 * (b1 - b0) / sh
    d['netto_alla_index_ny'] = d['netto_OMXSB_ny'] + d['netto_småbolag'] + d['netto_hela börsen'] + d['netto_övriga']
    d['car'] = car.get((x.RIC, x.review_cycle), np.nan)
    rows.append(d)
N = pd.DataFrame(rows); N.to_csv('nettokop_v2_events.csv', index=False)
ok = N[N.status == 'ok']; v1 = pd.read_csv('nettokop_events.csv'); v1 = v1[v1.status == 'ok']
print('händelser:', len(N), '| ok:', len(ok))
cols = ['netto_OMXSB_ny', 'netto_OMXSB_ny_inkl_bytare', 'netto_OMXSB_gammal_ej_ny', 'netto_småbolag', 'netto_hela börsen', 'netto_övriga', 'netto_alla_index_ny']
for ty in ['addition', 'deletion']:
    q = ok[ok.type == ty]; a = v1[v1.type == ty]
    print(f'\n{ty}, N {len(q)} (v1: {len(a)}); procent av aktierna, tecken vänt för borttag')
    print(pd.DataFrame({'medel': q[cols].mean(), 'median': q[cols].median()}).round(2).to_string())
    print(f"v1: OMXSB {a.netto_OMXSB.mean():.2f}, alla index {a.netto_alla_index.mean():.2f} | v2 alla index {q.netto_alla_index_ny.mean():.2f}; CAR medel {q.car.mean():.2f}, kvot {q.car.mean() / q.netto_alla_index_ny.mean():.2f}")
