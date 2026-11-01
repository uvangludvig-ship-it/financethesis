# %% [markdown]
# # Runda 3: kontrollgruppens trovärdighet (T12 gemensam uppgång, T13 mot Nasdaq-regelns nästan valda)
# Deklarerat i `runda3_deklaration.md` (2026-11-01 22:12 CET).
#
# 1. Lägg notebooken i repo-mappen `financethesis/`. Mappen `runda2_indata/` från runda 2 ska redan ligga där.
# 2. Kör alla celler (Run All). Ladda upp `runda3_resultat.zip` till Claude.
# %%
import os, re, json, zipfile
import numpy as np, pandas as pd
try:
    from scipy.stats import t as tdist
except ImportError:
    from statistics import NormalDist
    class tdist:
        @staticmethod
        def ppf(p, df):
            z = NormalDist().inv_cdf(p)
            return z + (z**3 + z) / (4 * df) + (5 * z**5 + 16 * z**3 + 3 * z) / (96 * df**2) + (3 * z**7 + 19 * z**5 + 17 * z**3 - 15 * z) / (384 * df**3)
ROOT = os.environ.get('ROOT', '.')
PANEL = os.environ.get('PANEL', 'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet')
OUT = os.environ.get('OUT', 'runda3_resultat')
os.makedirs(OUT, exist_ok=True)
P = lambda *a: os.path.join(ROOT, *a)
COLS = ['ric', 'date', 'close', 'totret', 'volume', 'mcap', 'shares', 'bid', 'ask']
px = pd.read_parquet(P(PANEL), columns=COLS) if PANEL.endswith('.parquet') else pd.read_csv(PANEL, usecols=COLS)
px['date'] = pd.to_datetime(px['date']); px = px[px.ric.astype(str).str.contains(r'\.ST')]
IND = P(os.environ.get('INDATA', 'runda2_indata'))
for f in ['medlemskap_verifierad.csv', 'lseg_klassificering.csv', 'lseg_freefloat_hist.csv', 'lseg_saknade_aktier.csv']:
    assert os.path.exists(os.path.join(IND, f)), f'STOPP: {f} saknas i {IND}'
S_ = pd.read_csv(os.path.join(IND, 'lseg_saknade_aktier.csv'))
add = []
for r in ['NDASE.ST', 'TIETOS.ST']:
    d = S_[(S_.ric == r) & S_.Date.notna()].copy(); d['date'] = pd.to_datetime(d.Date)
    m = S_[(S_.ric == r) & (S_.typ == 'marknadsvarde_manad')].reset_index(drop=True)
    m['date'] = pd.date_range('2006-01-31', periods=len(m), freq='ME')   # antagande: jan 2006 till okt 2026 i ordning
    d = d.merge(m[['date', 'Outstanding Shares']].rename(columns={'Outstanding Shares': 'shares'}), on='date', how='outer').sort_values('date')
    d['shares'] = d.shares.ffill(); d = d[d.TRDPRC_1.notna()]
    add.append(pd.DataFrame(dict(ric=r, date=d.date, close=d.TRDPRC_1, totret=np.nan, volume=d.ACVOL_UNS, mcap=d.TRDPRC_1 * d.shares, shares=d.shares, bid=d.BID, ask=d.ASK)))
px = pd.concat([px[~px.ric.isin(['NDASE.ST', 'TIETOS.ST'])]] + add, ignore_index=True)
print('panel:', len(px), 'rader,', px.ric.nunique(), 'aktier (inkl. NDASE.ST och TIETOS.ST från LSEG)')

# %%
ix = pd.read_csv(P('data/raw/lseg/panel_2005_2026/indices_daily (1).csv'), parse_dates=['date'])
cal = pd.DatetimeIndex(ix.loc[(ix.ric == '.OMXSBGI') & ix.close.notna(), 'date'].sort_values().unique())
pos = pd.Series(np.arange(len(cal)), index=cal)
def nextpos(d):
    d = pd.Timestamp(d); i = cal.searchsorted(d); return int(i) if i < len(cal) else None
mkt = ix.pivot(index='date', columns='ric', values='close').reindex(cal).pct_change()['.OMXSBGI'] * 100
px = px[px.date.isin(cal)].drop_duplicates(['ric', 'date'], keep='last').sort_values(['ric', 'date'])
def rser(g):
    g = g.set_index('date'); r = g.totret.fillna(g.close.pct_change() * 100)
    return r.reindex(cal[(cal >= g.index.min()) & (cal <= g.index.max())])
RET = pd.DataFrame({r: rser(g) for r, g in px.groupby('ric')}).reindex(cal)
n_err = int((RET > 1000).sum().sum()); RET = RET.mask(RET > 1000)
print('dagsavkastningar över 1 000 % satta till saknad:', n_err)
AR = RET.sub(mkt, axis=0); RICS = list(AR.columns); CI = {r: i for i, r in enumerate(RICS)}; A = AR.values
CS = np.vstack([np.zeros(A.shape[1]), np.nancumsum(A, axis=0)]); CN = np.vstack([np.zeros(A.shape[1]), np.cumsum(np.isnan(A), axis=0)])
def wsum(ric, a, b):
    if ric not in CI or a is None or b is None or pd.isna(a) or pd.isna(b): return np.nan
    a = int(a); b = int(b)
    if a < 0 or b >= len(cal): return np.nan
    j = CI[ric]; return np.nan if CN[b + 1, j] - CN[a, j] > 0 else CS[b + 1, j] - CS[a, j]
piv = lambda c: px.pivot_table(index='date', columns='ric', values=c).reindex(cal)
CLOSE = piv('close'); mc = piv('mcap').ffill(limit=10); VOL = piv('volume'); SH = piv('shares')
TV = VOL * CLOSE
SPR = ((piv('ask') - piv('bid')) / ((piv('ask') + piv('bid')) / 2) * 100); SPR = SPR.where((SPR > 0) & (SPR < 50))
TURN = (VOL / SH * 100).where(SH > 0)
ev = pd.read_csv(P('output/omxsb_replication_2007/events_car.csv'), parse_dates=['AD', 'ED'])
ev['iAD'] = ev.AD.map(pos); ev['iED'] = ev.ED.map(pos); ev['post'] = (ev.AD.dt.year >= 2017).astype(int)
rev = ev.groupby('review_cycle').agg(AD=('AD', 'first'), iAD=('iAD', 'first'), iED=('iED', 'first'), ED=('ED', 'first')).sort_values('AD').reset_index()
rev['k'] = np.arange(len(rev)); ev['k'] = ev.review_cycle.map(dict(zip(rev.review_cycle, rev.k)))
has_ev = set(zip(ev.RIC, ev.k)); cyc = list(rev.review_cycle)
MV = pd.read_csv(os.path.join(IND, 'medlemskap_verifierad.csv'))
MED = {c: set(g[g.status == 'medlem'].ric) for c, g in MV.groupby('review_after')}
OSA = {c: set(g[g.status == 'osäker'].ric) for c, g in MV.groupby('review_after')}
tu = pd.read_csv(P('data/raw/lseg/panel_2005_2026/td_universe.csv'))
K = pd.read_csv(os.path.join(IND, 'lseg_klassificering.csv'))
MIC = dict(zip(K.ric, K.marknad.astype(str)))
def not_main(r): return MIC.get(r, 'nan') in ('SSME', 'ONSE')
def stem(r): return re.sub(r'(sdb)?[abcr]?\.ST.*$', '', str(r))
def root(r):
    m = re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST', str(r)); return m.group(1) if m else str(r)
print('kalender', cal.min().date(), cal.max().date(), '| översyner', len(rev))

# %%
rng = np.random.default_rng(20261101)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
def wcr(X, y, g, j=0, B=9999):
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    keep = X.std(0) > 0; keep[j] = True; X = X[:, keep]; j = int(keep[:j].sum())
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    if G < 3 or n <= k: return (np.nan,) * 4 + (n, G)
    XtXi = np.linalg.pinv(X.T @ X); q = X @ XtXi[j]; adj = G / (G - 1) * (n - 1) / (n - k); Am = XtXi @ X.T
    def bse(Y):
        Bm = Y @ Am.T; E = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in E * q])
        return Bm[:, j], np.sqrt((sg ** 2).sum(1) * adj)
    b0, s0 = bse(y[None, :]); b0, s0 = b0[0], s0[0]
    Xr = np.delete(X, j, 1); fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]; er = y - fr; ts = []
    for _ in range(B // 1000 + 1):
        W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
    ts = np.concatenate(ts)[:B]; qq = tdist.ppf(.975, G - 1)
    return b0, b0 - qq * s0, b0 + qq * s0, (np.abs(ts) >= abs(b0 / s0)).mean(), n, G
out = []
def rec(test, typ, per, variant, b, lo, hi, p, n, G, note=''):
    r = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
    out.append(dict(test=test, typ=typ, period=per, variant=variant, N=n, G=G, skattning=r(b), ci_lo=r(lo), ci_hi=r(hi), p_wcb=r(p), not_=note))
def reg(s, y, extra=()):
    FE = pd.get_dummies(s.review).astype(float).values
    X = np.column_stack([s.event.values.astype(float), s.ru.values, s.lm.values] + [s[c].values for c in extra] + [FE])
    return wcr(X, np.asarray(y, float), s.review.values, 0)
PER = {'före': 0, 'efter': 1}

# %%
# ---------- Urval som T5: tillägg/borttag och nästan tillagda/borttagna, med flera mått per aktie
WIN = {'ED+1': 1, 'ED+20': 20, 'ED+60': 60, 'ED+100': 100}
def liq(M, c, a, b):
    if c not in M: return np.nan
    s = M[c].iloc[max(a, 0):min(b, len(cal) - 1) + 1].dropna(); return s.median() if len(s) >= 20 else np.nan
def dlog(M, c, iA, iE):
    pre = liq(M, c, iA - 120, iA - 21); post = liq(M, c, iE + 20, iE + 120)
    return np.log(post / pre) if pre and post and pre > 0 and post > 0 else np.nan
rows = []
for k, r in rev.iterrows():
    iA, iE = int(r.iAD), int(r.iED)
    if iA - 120 < 0 or iE + 1 >= len(cal) or k == 0: continue
    before = MED.get(cyc[k - 1], set()); unsure = OSA.get(cyc[k - 1], set())
    evs = ev[ev.k == k]; adds = set(evs[evs.type == 'addition'].RIC); dels = set(evs[evs.type == 'deletion'].RIC)
    ev_stems = set(stem(x) for x in evs.RIC)
    def stats(c):
        return wsum(c, iA - 100, iA - 1), wsum(c, iA - 1, iE + 1), (mc[c].iloc[iA - 1] if c in mc else np.nan)
    pool = []
    for c in RICS:
        if any((c, kk) in has_ev for kk in (k - 1, k, k + 1)) or stem(c) in ev_stems or c in unsure or not_main(c): continue
        ru, cr, m = stats(c)
        if np.isnan(ru) or np.isnan(cr) or not (m > 0): continue
        pool.append(dict(ric=c, stem=stem(c), member=c in before, ru=ru, car=cr, mcap=m, tval=np.nansum(TV[c].values[iA - 120:iA]) if c in TV else 0))
    Pq = pd.DataFrame(pool)
    if Pq.empty: continue
    Pq = Pq.sort_values('tval', ascending=False).drop_duplicates('stem')
    for ty, S in [('addition', adds), ('deletion', dels)]:
        E = []
        for c in S:
            ru, cr, m = stats(c)
            if not (np.isnan(ru) or np.isnan(cr) or not (m > 0)): E.append(dict(ric=c, ru=ru, car=cr, mcap=m, tval=np.nansum(TV[c].values[iA - 120:iA]) if c in TV else 0))
        if not E: continue
        E = pd.DataFrame(E)
        N = Pq[(~Pq.member) & (Pq.mcap >= E.mcap.min())] if ty == 'addition' else Pq[(Pq.member) & (Pq.mcap <= E.mcap.max())]
        for flag, D in [(1, E), (0, N)]:
            for _, e in D.iterrows():
                d = dict(review=cyc[k], k=k, AD=r.AD, iA=iA, iE=iE, post=int(r.AD.year >= 2017), type=ty, event=flag, ric=e.ric, mic=MIC.get(e.ric, 'okänd'), ru=e.ru, lm=np.log(e.mcap), ltv=np.log(1 + e.tval))
                for w, h in WIN.items(): d['car_' + w] = wsum(e.ric, iA - 1, iE + h)
                d['d_spread'] = dlog(SPR, e.ric, iA, iE); d['d_turn'] = dlog(TURN, e.ric, iA, iE)
                rows.append(d)
S5 = pd.DataFrame(rows)
print('urval som T5:', int(S5.event.sum()), 'händelser,', int((S5.event == 0).sum()), 'nästan')

# %%
# ---------- hjälp: regression med egna kolumner
def reg_cols(s, y, cols):
    FE = pd.get_dummies(s.review).astype(float).values
    X = np.column_stack([s.event.values.astype(float)] + [np.asarray(s[c], float) for c in cols] + [FE])
    return wcr(X, np.asarray(y, float), s.review.values, 0)
def quint(s, ev_ru):
    edges = np.quantile(ev_ru, [.2, .4, .6, .8]); qd = np.digitize(s.ru.values, edges)
    D_ = pd.get_dummies(qd, prefix='q').astype(float); D_.index = s.index
    return D_.drop(columns=[c for c in D_.columns if c == 'q_0'], errors='ignore')
def bal(s):
    e, n = s[s.event == 1], s[s.event == 0]
    return f'uppgång median {e.ru.median():.1f} mot {n.ru.median():.1f}; log börsvärde {e.lm.mean():.2f} mot {n.lm.mean():.2f}; log omsättning {e.ltv.mean():.2f} mot {n.ltv.mean():.2f}; nästan {len(n)}'
def common_support(s):
    ev_ru = s[s.event == 1].ru; lo_, hi_ = ev_ru.quantile([.1, .9])
    q = s[(s.event == 1) | ((s.event == 0) & s.ru.between(lo_, hi_))].copy()
    Q = quint(q, ev_ru.values); q = pd.concat([q, Q], axis=1)
    return q, list(Q.columns)

# ---------- T12: gemensam uppgång
for ty in ['addition', 'deletion']:
    for pn, pv in PER.items():
        s = S5[(S5.type == ty) & (S5.post == pv)]
        if s.event.sum() == 0: continue
        q, qc = common_support(s)
        for w in ['ED+1', 'ED+20']:
            x = q.dropna(subset=['car_' + w])
            b, lo, hi, p, n, G = reg_cols(x, x['car_' + w], qc + ['lm'])
            lab = 'T12' if (ty == 'addition' and pv == 1 and w == 'ED+1') else 'T12 sekundärt'
            rec(lab, ty, pn, f'CAR [AD-1,{w}], nästan inom 10-90-percentilen av uppgång, kvintiler', b, lo, hi, p, n, G,
                f'före begränsning: {bal(s)} | efter: {bal(q)}')
print('T12 klar')

# %%
# ---------- T13: Nasdaq-regelns nästan valda (T6 steg 2)
FFH = pd.read_csv(os.path.join(IND, 'lseg_freefloat_hist.csv'))
ffh = {(r.review, r.ric): r.ff for r in FFH.dropna(subset=['ff']).itertuples()}
ICB = {r: str(int(v)) for r, v in zip(K.ric, K.icb) if pd.notna(v)}
TRBC = {r: str(v) for r, v in zip(K.ric, K.trbc) if pd.notna(v)}
FFC = dict(zip(K.ric, pd.to_numeric(K.freefloat, errors='coerce')))
REFS = {'2007H2': '2007-05-31', '2008H1': '2007-11-30', '2008H2': '2008-05-30', '2009JAN': '2008-11-28'}
for c, e in zip(rev.review_cycle, rev.ED):
    if c not in REFS:
        m_ = {6: 4, 12: 10, 7: 5, 1: 11}[e.month]; y_ = e.year - (1 if e.month == 1 else 0)
        REFS[c] = str(cal[(cal.year == y_) & (cal.month == m_)].max().date())
rows13 = []
for k, r in rev.iterrows():
    if k == 0: continue
    iA, iE = int(r.iAD), int(r.iED); ref = pd.Timestamp(REFS[r.review_cycle]); ir = int(pos[ref]) if ref in pos.index else nextpos(ref)
    start = nextpos(ref - pd.DateOffset(months=6))
    cl = CLOSE.iloc[ir]; U = [c for c in RICS if pd.notna(cl.get(c)) and not not_main(c)]
    if len(U) < 50: continue
    tvv = pd.Series({c: (np.nansum(TV[c].values[start:ir + 1]) if c in TV else np.nan) for c in U})
    shr = SH.iloc[max(ir - 5, 0):ir + 1].ffill().iloc[-1]
    cm = pd.Series({c: (cl[c] * shr[c]) if pd.notna(shr.get(c)) and shr.get(c) > 0 else (mc[c].iloc[ir] if c in mc else np.nan) for c in U})
    ff = pd.Series({c: ffh.get((r.review_cycle, c), FFC.get(c, np.nan)) for c in U}); ff = ff.where((ff > 0) & (ff <= 100))
    D = pd.DataFrame(dict(tv=tvv, ffm=cm * (ff.fillna(100) / 100))).dropna(); D = D[D.ffm > 0]
    D['sect'] = [ICB.get(c, 'trbc:' + TRBC[c] if c in TRBC else 'okänd') for c in D.index]
    ntop = max(int(np.ceil(0.10 * len(D))), 25)
    D['top'] = D.tv.rank(ascending=False) <= ntop; D['bottom'] = D.tv.rank(ascending=False, pct=True) > 0.70
    D = D.sort_values('ffm', ascending=False)
    D['w'] = D.ffm / D.groupby('sect').ffm.transform('sum'); D['cum'] = D.groupby('sect').ffm.cumsum() / D.groupby('sect').ffm.transform('sum')
    D['sel'] = (D.top | ((D.cum - D.w) < 0.85)) & ~D.bottom
    before = MED.get(cyc[k - 1], set()); unsure = OSA.get(cyc[k - 1], set())
    evs = ev[ev.k == k]; adds = set(evs[evs.type == 'addition'].RIC); ev_stems = set(stem(x) for x in evs.RIC)
    near = D[(~D.index.isin(list(before))) & (~D.index.isin(list(adds))) & (~D.bottom) & (D.sel | (D.cum <= 0.95))]
    for flag, idx in [(1, [a for a in adds if a in D.index]), (0, list(near.index))]:
        for c in idx:
            if flag == 0 and (any((c, kk) in has_ev for kk in (k - 1, k, k + 1)) or stem(c) in ev_stems or c in unsure): continue
            ru = wsum(c, iA - 100, iA - 1); m = mc[c].iloc[iA - 1] if c in mc else np.nan
            c1 = wsum(c, iA - 1, iE + 1); c20 = wsum(c, iA - 1, iE + 20)
            if np.isnan(ru) or np.isnan(c1) or not (m > 0): continue
            rows13.append(dict(review=r.review_cycle, post=int(r.AD.year >= 2017), event=flag, ric=c, ru=ru, lm=np.log(m), ltv=np.log1p(D.loc[c, 'tv']),
                               **{'car_ED+1': c1, 'car_ED+20': c20}, regel_vald=bool(D.loc[c, 'sel']), cum=float(D.loc[c, 'cum'])))
S13 = pd.DataFrame(rows13); S13.to_csv(os.path.join(OUT, 'T13_events.csv'), index=False)
for pn, pv in PER.items():
    s = S13[S13.post == pv]
    if s.event.sum() == 0 or (s.event == 0).sum() == 0: continue
    for w in ['ED+1', 'ED+20']:
        x = s.dropna(subset=['car_' + w]); b, lo, hi, p, n, G = reg_cols(x, x['car_' + w], ['ru', 'lm', 'ltv'])
        rec('T13' if (pv == 1 and w == 'ED+1') else 'T13 sekundärt', 'addition', pn, f'CAR [AD-1,{w}] mot regelns nästan valda', b, lo, hi, p, n, G, bal(x))
    x = s[(s.event == 1) | s.regel_vald].dropna(subset=['car_ED+1'])
    if (x.event == 0).sum():
        b, lo, hi, p, n, G = reg_cols(x, x['car_ED+1'], ['ru', 'lm', 'ltv'])
        rec('T13 sekundärt', 'addition', pn, 'CAR [AD-1,ED+1] mot "regeln valde, Nasdaq lade inte till"', b, lo, hi, p, n, G, bal(x))
    q, qc = common_support(s.dropna(subset=['car_ED+1']))
    b, lo, hi, p, n, G = reg_cols(q, q['car_ED+1'], qc + ['lm', 'ltv'])
    rec('T13 sekundärt', 'addition', pn, 'CAR [AD-1,ED+1] mot regelns nästan valda, gemensam uppgång', b, lo, hi, p, n, G, bal(q))
print('T13 klar')

# %%
O = pd.DataFrame(out); O.to_csv(os.path.join(OUT, 'runda3_results.csv'), index=False)
S5.to_csv(os.path.join(OUT, 'T12_urval.csv'), index=False)
with zipfile.ZipFile('runda3_resultat.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(OUT): z.write(os.path.join(OUT, f), f)
    z.write(os.path.join(IND, 'runda2_deklaration.md'), 'runda2_deklaration.md') if os.path.exists(os.path.join(IND, 'runda2_deklaration.md')) else None
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 160)
print(O.to_string(index=False)); print('\nKlart. Ladda upp runda3_resultat.zip till Claude.')
