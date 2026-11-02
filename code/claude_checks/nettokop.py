# Indexfondernas nettoköp vid OMXSB-ändringar 2019-2026, per fondfamilj (beskrivande, för jämförelsen med G&S).
# Samma kvartal och ISIN-regel som första steget v2 och T9. Inga avkastningar används.
import os, re
import numpy as np, pandas as pd
R = os.environ.get('REPO', '/home/claude/uvangludvig-ship-it/financethesis')
D = os.environ.get('DATA', '/home/claude/kodpaket/data')
H = pd.read_pickle(os.environ.get('HOLD', '/home/claude/fi_all_holdings.pkl'))
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
FAM = F.set_index(['kv', 'fund_id']).familj.to_dict()
H['familj'] = [FAM.get((k, f), 'ej index') for k, f in zip(H.kv, H.fund_id)]
G = H[H.familj != 'ej index'].groupby(['isin', 'kv', 'familj']).antal.sum()
qs = sorted(H.kv.unique()); first_seen = H.groupby('isin')['kv'].min().to_dict()

tu = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/td_universe.csv'); st = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/stocks_static_2005.csv')
isin = dict(zip(tu.RIC, tu.IssueISIN)); isin.update({k: v for k, v in zip(st.ric, st.IssueISIN) if isinstance(v, str)})
px = pd.read_csv(os.path.join(D, 'panel_utdrag.csv.gz'), usecols=['ric', 'date', 'shares'], parse_dates=['date'])
e = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'del1_events.csv'), parse_dates=['AD', 'ED'])
e = e[e.AD >= '2018-12-01'].copy()
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
    d = dict(RIC=x.RIC, review=x.review_cycle, type=x.type, status='ok', q0=q0.date(), q1=q1.date(),
             dagar_fore_AD=(x.AD - q0).days, dagar_efter_ED=(q1 - x.ED).days)
    tot = 0
    for fam in ['OMXSB', 'småbolag', 'hela börsen', 'övriga']:
        b0 = G.get((i, q0, fam), 0.0); b1 = G.get((i, q1, fam), 0.0)
        d[f'fore_{fam}'] = 100 * b0 / sh; d[f'netto_{fam}'] = sign * 100 * (b1 - b0) / sh; tot += d[f'netto_{fam}']
    d['netto_alla_index'] = tot
    rows.append(d)
N = pd.DataFrame(rows); N.to_csv('nettokop_events.csv', index=False)
ok = N[N.status == 'ok']
print('händelser 2019-2026:', len(N), '| ok:', len(ok), '|', N.status.value_counts().to_dict())
cols = ['netto_OMXSB', 'netto_småbolag', 'netto_hela börsen', 'netto_övriga', 'netto_alla_index']
for ty in ['addition', 'deletion']:
    q = ok[ok.type == ty]
    print(f'\n{ty}, N {len(q)}, i procent av aktierna, tecken vänt för borttag:')
    print(pd.DataFrame({'medel': q[cols].mean(), 'median': q[cols].median(), 'andel < -0,05': (q[cols] < -0.05).mean()}).round(2).to_string())
    print('ägande före, medel:', q[[c for c in q.columns if c.startswith('fore_')]].mean().round(2).to_dict())
