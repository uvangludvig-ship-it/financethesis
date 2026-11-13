# Steg 16: tvillingar. Port av code/claude_checks/twin_prices.py, twin_core.py, twin_run.py och ab_revision.py (1–2 nov 2026),
# metoden oförändrad. Deklarationer: code/claude_checks/twin_excl_beslut.md, ab_deklaration.md; flytten: declarations/step13_16_declaration.md.
#   Par: ett aktieslag läggs till eller tas bort ur OMXSB medan systerslaget i samma bolag inte ändras (data/twins/twin_pairs.csv).
#   Mått: spreaden = log-avkastning indexslag minus systerslag över fönstret, med eget tecken (borttag vänds), i procent.
#   Inferens: placebofördelning. För varje händelse dras startdagar samma tid på året (±45 dagar) andra år, utan bolagets egna
#   händelser i närheten; 5 000 dragningar av ett placebofönster per händelse ger nollfördelningen för medlet. Holm för de sekundära.
#   A/B-revisionen (ab_deklaration.md): pris i stället för totalavkastning när ett ben kommer från LSEG:s separata hämtning, och
#   händelser med spikar (R2), hopp (R3) eller stillastående systerslag (R4) tas bort; intervall ur placebofördelningen.
# Samma frön som då (11 för twin_run, 20261101 för ab_revision) och samma ordning på dragningarna, så siffrorna ska bli identiska.
# Kurspanelen, kalendern och marknaden kommer från 01:s huvud (returns.py); de är samma filer som common.py läste.
# Körs från thesis_final: python3 code/16_twins.py
import os, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'twins'

SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg16'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, px, cal, pos, mkt = g['np'], g['pd'], g['px'], g['cal'], g['pos'], g['mkt']
os.makedirs(OUT, exist_ok=True)
avvik = []
def jfr(namn, nytt, gammalt, tol=0):
    if pd.isna(nytt) and pd.isna(gammalt): return
    if not abs(float(nytt) - float(gammalt)) <= tol: avvik.append(f'{namn}: nu {float(nytt)}, då {float(gammalt)}')

# ---------- twin_prices.py
l1 = pd.read_csv(DATA / 'prices' / 'tvilling_priser_lseg.csv', parse_dates=['Date'])
l2 = pd.read_csv(DATA / 'prices' / 'tvilling_priser_lseg_2.csv', parse_dates=['Date'])
frames = []
for r in ['NCCa.ST', 'SWECa.ST']:
    gg = l1[(l1.ric == r) & l1['Price Close'].notna()].sort_values(['Date', 'Volume']).drop_duplicates('Date', keep='first')
    frames.append(pd.DataFrame({'ric': r, 'date': gg.Date, 'close': gg['Price Close'], 'volume': gg.Volume}))
for r in ['BONAVa.ST', 'RATOa.ST']:
    gg = l2[(l2.ric == r) & (l2.metod == 1) & l2.TRDPRC_1.notna()].drop_duplicates('Date')
    frames.append(pd.DataFrame({'ric': r, 'date': gg.Date, 'close': gg.TRDPRC_1, 'volume': gg.ACVOL_UNS}))
ext = pd.concat(frames)
P = pd.concat([px[['ric', 'date', 'close', 'volume']], ext])
P = P[P.date.isin(cal)]
CLOSE = P.pivot_table(index='date', columns='ric', values='close', aggfunc='last').reindex(cal)
VOL = P.pivot_table(index='date', columns='ric', values='volume', aggfunc='last').reindex(cal)

# ---------- twin_core.py
TR = {}
pr = px.pivot_table(index='date', columns='ric', values='totret', aggfunc='last').reindex(cal)
for c in pr.columns: TR[c] = (1 + pr[c].fillna(0) / 100).cumprod().where(CLOSE[c].ffill().notna() if c in CLOSE else True)
for r in ['NCCa.ST', 'SWECa.ST']:
    gg = l1[(l1.ric == r)].sort_values(['Date', 'Volume']).drop_duplicates('Date').set_index('Date')['Daily Total Return'].reindex(cal)
    TR[r] = (1 + gg.fillna(0) / 100).cumprod().where(CLOSE[r].ffill().notna())
PRICE = CLOSE.ffill()
def root(r):
    m = re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST', str(r)); return m.group(1) if m else str(r)
def legs(ix, sis):
    if ix in TR and sis in TR: return TR[ix], TR[sis], 'tr'
    return PRICE[ix], PRICE[sis], 'price'
def spread(ix, sis, a, b):
    A, B, _ = legs(ix, sis)
    if a - 1 < 0 or b >= len(cal): return np.nan
    x = np.log(A.iloc[b] / A.iloc[a - 1]) - np.log(B.iloc[b] / B.iloc[a - 1])
    return 100 * x if np.isfinite(x) else np.nan
t = pd.read_csv(DATA / 'twins' / 'twin_pairs.csv', parse_dates=['AD', 'ED'])
t['iAD'] = t.AD.map(pos).astype(int); t['iED'] = t.ED.map(pos).astype(int)
t['firm'] = t.event_key.map(root); t['sign'] = np.where(t.type == 'addition', 1, -1)
scr = pd.read_csv(DATA / 'twins' / 'twin_mech_screen.csv'); t = t.merge(scr[['event_id', 'excl_mech']], on='event_id')

# ---------- twin_run.py (twin_placebo.pkl lästes men användes inte; utelämnad)
rng = np.random.default_rng(11)
excl_extra = set(open(DATA / 'twins' / 'twin_excl_screen.txt').read().split())
ev = t[(~t.excl_mech) & (~t.event_id.isin(excl_extra))].copy()
W = {'primär [AD-1,ED+1]': lambda e: (e.iAD - 1, e.iED + 1),
     'medprimär återgång [ED,ED+20]': lambda e: (e.iED, e.iED + 20),
     'sek [AD-1,AD+1]': lambda e: (e.iAD - 1, e.iAD + 1),
     'sek [AD+2,ED-2]': lambda e: (e.iAD + 2, e.iED - 2),
     'sek [ED-1,ED+1]': lambda e: (e.iED - 1, e.iED + 1),
     'placebo [AD-60,AD-21]': lambda e: (e.iAD - 60, e.iAD - 21),
     'placebo [AD-20,AD-2]': lambda e: (e.iAD - 20, e.iAD - 2)}
allev = t.copy(); doy = np.array(cal.dayofyear)
def starts(e, L):
    firm_ev = allev[allev.firm == e.firm][['iAD', 'iED']].values; ad = e.AD.dayofyear; out = []
    for s in range(61, len(cal) - L - 21):
        if cal[s].year == e.AD.year: continue
        dd = abs(doy[s] - ad); dd = min(dd, 365 - dd)
        if dd > 45: continue
        if any((s + L + 20 >= ia - 60) and (s - 60 <= ie + 20) for ia, ie in firm_ev): continue
        out.append(s)
    return out
rows = []
for name, fw in W.items():
    obs = []; pools = []
    for _, e in ev.iterrows():
        a, b = fw(e); a, b = int(a), int(b)
        if b < a: obs.append(np.nan); pools.append(np.array([])); continue
        obs.append(e.sign * spread(e.event_key, e.sister_ric, a, b))
        L = b - a + 1; st = starts(e, L)
        pools.append(np.array([e.sign * spread(e.event_key, e.sister_ric, s, s + L - 1) for s in st]))
    ev[name] = obs
    ok = [i for i, (o, p) in enumerate(zip(obs, pools)) if np.isfinite(o) and len(p[np.isfinite(p)]) >= 20]
    o = np.array([obs[i] for i in ok]); fr = ev.firm.values[ok]; pl = [pools[i][np.isfinite(pools[i])] for i in ok]
    m_ev = o.mean(); m_f = pd.Series(o, index=fr).groupby(level=0).mean().mean()
    nm_ev = []; nm_f = []
    for _ in range(5000):
        d = np.array([rng.choice(p) for p in pl]); nm_ev.append(d.mean()); nm_f.append(pd.Series(d, index=fr).groupby(level=0).mean().mean())
    nm_ev = np.array(nm_ev); nm_f = np.array(nm_f)
    p_ev = (np.abs(nm_ev - nm_ev.mean()) >= abs(m_ev - nm_ev.mean())).mean(); p_f = (np.abs(nm_f - nm_f.mean()) >= abs(m_f - nm_f.mean())).mean()
    rows.append(dict(fönster=name, N=len(o), bolag=len(set(fr)), medel_händelse=round(m_ev, 2), p_händelse=round(p_ev, 4), medel_bolag=round(m_f, 2), p_bolag=round(p_f, 4)))
res = pd.DataFrame(rows)
sec = res[res.fönster.str.startswith('sek')].sort_values('p_händelse')
k = len(sec); holm = [min(1, max((k - i) * p for i, p in enumerate(sec.p_händelse.values[:j + 1]))) for j in range(k)]
res.loc[sec.index, 'p_holm'] = np.round(holm, 4)
def legcar(ric, a, b):
    A = TR[ric] if ric in TR else PRICE[ric]
    if a - 1 < 0 or b >= len(cal): return np.nan
    r = 100 * np.log(A.iloc[b] / A.iloc[a - 1]); m = 100 * np.log((1 + mkt.iloc[a:b + 1] / 100).prod())
    return r - m
for name in ['primär [AD-1,ED+1]', 'medprimär återgång [ED,ED+20]']:
    fw = W[name]
    ev[name + ' indexslag'] = [e.sign * legcar(e.event_key, *map(int, fw(e))) for _, e in ev.iterrows()]
    ev[name + ' systerslag'] = [e.sign * legcar(e.sister_ric, *map(int, fw(e))) for _, e in ev.iterrows()]
ev.to_csv(OUT / 'twin_results_events.csv', index=False); res.to_csv(OUT / 'twin_results_summary.csv', index=False)

# ---------- ab_revision.py
rng = np.random.default_rng(20261101)
fin = pd.read_csv(OUT / 'twin_results_events.csv', parse_dates=['AD', 'ED'])
LSEG_SIS = {'NCCa.ST', 'SWECa.ST', 'BONAVa.ST', 'RATOa.ST'}
TRp = {}
def series(ix_, sis):
    if sis in LSEG_SIS or ix_ in LSEG_SIS or not (ix_ in TR and sis in TR): return PRICE[ix_], PRICE[sis], 'pris'
    return TR[ix_], TR[sis], 'tr'
def flags(ix_, sis):
    key = (ix_, sis)
    if key not in TRp:
        A_, B_, src = series(ix_, sis)
        r = np.log(A_ / B_).diff().values
        nxt = np.r_[r[1:], np.nan]
        big = np.abs(r) > 0.08
        spike = big & (np.abs(r + nxt) < 0.25 * np.abs(r))
        jump = (np.abs(r) > 0.15) & (np.abs(r + nxt) > 0.75 * np.abs(r))
        TRp[key] = (A_, B_, src, spike, jump)
    return TRp[key]
def spread_c(ix_, sis, a, b):
    A_, B_, src, spike, jump = flags(ix_, sis)
    if a - 1 < 0 or b >= len(cal): return np.nan, 'utanför'
    if spike[a - 1] or spike[b]: return np.nan, 'R2'
    if jump[a:b + 1].any(): return np.nan, 'R3'
    x = np.log(A_.iloc[b] / A_.iloc[a - 1]) - np.log(B_.iloc[b] / B_.iloc[a - 1])
    return (100 * x, 'ok') if np.isfinite(x) else (np.nan, 'saknas')
def stale_share(sis, a, b):
    p = CLOSE[sis].iloc[max(a, 0):b + 1].dropna() if sis in CLOSE else pd.Series(dtype=float)
    return float((p.diff().iloc[1:] == 0).mean()) if len(p) > 5 else np.nan
rows = []; pools = {}
for _, e in fin.iterrows():
    a, b = int(e.iAD) - 1, int(e.iED) + 1
    st = stale_share(e.sister_ric, int(e.iAD) - 60, int(e.iED) + 20)
    v, why = spread_c(e.event_key, e.sister_ric, a, b)
    if st > 0.5: why = 'R4'; v = np.nan
    src = flags(e.event_key, e.sister_ric)[2]
    L = b - a + 1; pl = []
    for s in starts(e, L):
        x, w = spread_c(e.event_key, e.sister_ric, s, s + L - 1)
        if np.isfinite(x): pl.append(e.sign * x)
    pools[e.event_id] = np.array(pl)
    rows.append(dict(event_id=e.event_id, firm=e.firm, type=e.type, källa=src, stillastående=round(st, 2), status=why,
                     spread=e.sign * v if np.isfinite(v) else np.nan, spread_tidigare=e['primär [AD-1,ED+1]'], n_placebo=len(pl)))
D = pd.DataFrame(rows)
okd = D[(D.status == 'ok') & (D.n_placebo >= 20)]
def infer(sub):
    m = sub.spread.mean(); fr = sub.firm.values
    nm = np.array([np.mean([rng.choice(pools[k]) for k in sub.event_id]) for _ in range(5000)])
    c = nm - nm.mean(); p = (np.abs(c) >= abs(m - nm.mean())).mean()
    lo, hi = m - np.percentile(c, 97.5), m - np.percentile(c, 2.5)
    mf = pd.Series(sub.spread.values, index=fr).groupby(level=0).mean().mean()
    return m, lo, hi, p, len(sub), len(set(fr)), mf
res2 = []
for lab, sub in [('alla rensade', okd), ('tillägg', okd[okd.type == 'addition']), ('borttag', okd[okd.type == 'deletion']),
                 ('utan källbyte (bara panelens totalavkastning)', okd[okd.källa == 'tr'])]:
    if len(sub) >= 3:
        m, lo, hi, p, n, gn, mf = infer(sub)
        res2.append(dict(urval=lab, N=n, bolag=gn, skattning=round(m, 2), ci_lo=round(lo, 2), ci_hi=round(hi, 2), p=round(p, 4), medel_per_bolag=round(mf, 2)))
R2 = pd.DataFrame(res2)
D.to_csv(OUT / 'ab_revision_events.csv', index=False); R2.to_csv(OUT / 'ab_revision_results.csv', index=False)

# ---------- jämförelse: identiskt med körningen 1–2 nov
P1 = pd.read_csv(DATA / 'comparison' / 'previous_run_twins_summary.csv'); P2 = pd.read_csv(DATA / 'comparison' / 'previous_run_twins_ab_revision.csv')
for o, n in zip(P1.itertuples(index=False), res.itertuples(index=False)):
    assert o.fönster == n.fönster
    for c in ['N', 'bolag', 'medel_händelse', 'p_händelse', 'medel_bolag', 'p_bolag', 'p_holm']: jfr(f'{o.fönster} {c}', getattr(n, c), getattr(o, c))
for o, n in zip(P2.itertuples(index=False), R2.itertuples(index=False)):
    assert o.urval == n.urval
    for c in ['N', 'bolag', 'skattning', 'ci_lo', 'ci_hi', 'p', 'medel_per_bolag']: jfr(f'A/B {o.urval} {c}', getattr(n, c), getattr(o, c))
if len(P1) != len(res) or len(P2) != len(R2): avvik.append(f'antal rader: nu {len(res)} och {len(R2)}, då {len(P1)} och {len(P2)}')

f = lambda v, d=2: '' if pd.isna(v) else f'{v:.{d}f}'.replace('-', '−')
L = ['# Steg 16: tvillingar', '', 'Port av `twin_prices.py`, `twin_core.py`, `twin_run.py` och `ab_revision.py`, samma frön och ordning.', '',
     '## Jämförelse med körningen 1–2 november', '', 'Alla jämförda siffror är identiska.' if not avvik else 'Avvikelser:\n\n' + '\n'.join('- ' + a for a in avvik), '',
     '## Spread indexslag minus systerslag (procent, eget tecken), placeboinferens', '', '| Fönster | N | Bolag | Medel | p | Medel per bolag | p | p (Holm) |', '|---|---|---|---|---|---|---|---|']
for r in res.itertuples(index=False):
    L.append(f'| {r.fönster} | {r.N} | {r.bolag} | {f(r.medel_händelse)} | {f(r.p_händelse, 4)} | {f(r.medel_bolag)} | {f(r.p_bolag, 4)} | {f(r.p_holm, 4)} |')
L += ['', '## A/B-revisionen, primärt fönster [AD−1, ED+1]', '', '| Urval | N | Bolag | Skattning | 95 % intervall | p | Medel per bolag |', '|---|---|---|---|---|---|---|']
for r in R2.itertuples(index=False):
    L.append(f'| {r.urval} | {r.N} | {r.bolag} | {f(r.skattning)} | {f(r.ci_lo)} till {f(r.ci_hi)} | {f(r.p, 4)} | {f(r.medel_per_bolag)} |')
L += ['', 'Status per händelse i revisionen: ' + ', '.join(f'{k} {v}' for k, v in D.status.value_counts().items()) + '.']
(OUT / 'TWINS.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('\n'.join(L))
print('Metod: placebofördelning (5 000 dragningar av placebofönster samma tid på året andra år); Holm för de sekundära fönstren')
print('jämförelse med 1–2 nov:', 'inga avvikelser' if not avvik else avvik)
