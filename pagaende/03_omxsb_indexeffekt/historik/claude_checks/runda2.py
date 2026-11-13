# %% [markdown]
# # Runda 2 på hela panelen, verifierad kontrollgrupp
# T5v (T5 med verifierad kontrollgrupp), T7 (tid), T8b (likviditet), T9 (ägarbredd), T6 steg 1 (träffsäkerhet för Nasdaqs regel), T11 (OMXS30-tvillingar).
# Deklarerat i `runda2_deklaration.md` (20:09, 20:11, 20:3x, 21:21 CET).
#
# 1. Packa upp `runda2_paket.zip` i repo-mappen `financethesis/`. Då finns notebooken och mappen `runda2_indata/`.
# 2. Kör alla celler (Run All). Ladda upp `runda2_resultat.zip` till Claude.

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
OUT = os.environ.get('OUT', 'runda2_resultat')
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
# ---------- T7: håller effekten över tid?
for ty in ['addition', 'deletion']:
    for pn, pv in PER.items():
        s = S5[(S5.type == ty) & (S5.post == pv)]
        for w in WIN:
            q = s.dropna(subset=['car_' + w])
            if q.event.sum() == 0: continue
            b, lo, hi, p, n, G = reg(q, q['car_' + w])
            rec('T5v' if w == 'ED+1' else 'T7', ty, pn, f'CAR [AD-1,{w}] mot nästan', b, lo, hi, p, n, G,
                f'händelser {int(q.event.sum())}, nästan {int((q.event == 0).sum())}; okänd marknadsplats bland nästan {(q[q.event == 0].mic == "okänd").mean():.2f}; uppgång {q[q.event == 1].ru.mean():.1f} mot {q[q.event == 0].ru.mean():.1f}')
            if w == 'ED+1':
                x = q[(q.event == 1) | (q.mic == 'XSTO')]
                b, lo, hi, p, n, G = reg(x, x['car_' + w])
                rec('T5v', ty, pn, 'känslighet: bara huvudlistan (XSTO) bland nästan', b, lo, hi, p, n, G, f'nästan {int((x.event == 0).sum())}')
print('T7 klar')

# %%
# ---------- T8b: likviditet, tillägg mot nästan tillagda
for ty in ['addition', 'deletion']:
    for pn, pv in PER.items():
        s = S5[(S5.type == ty) & (S5.post == pv)]
        for v, lab in [('d_spread', 'förändring log spread'), ('d_turn', 'förändring log omsättning')]:
            q = s.dropna(subset=[v])
            if q.event.sum() == 0: continue
            b, lo, hi, p, n, G = reg(q, q[v])
            rec('T8b', ty, pn, lab, b, lo, hi, p, n, G, f'händelser medel {q[q.event == 1][v].mean():.3f}, nästan medel {q[q.event == 0][v].mean():.3f}')
print('T8b klar')

# %%
# ---------- T9: ägarbredd från FI (antal svenska fonder som äger aktieslaget)
FI = P('data/derived/fi/fi_holdings_long.csv.gz')
try:
  if not (os.path.exists(FI) and os.path.getsize(FI) > 10000): raise FileNotFoundError('FI-filen saknas eller är en LFS-stubb')
  if True:
      fi = pd.read_csv(FI, usecols=['ISIN-kod_instrument', 'Antal', 'Kvartalsslut', 'Fond_institutnummer', 'Fond_namn'])
      fi = fi[pd.to_numeric(fi.Antal, errors='coerce') > 0]; fi['Kvartalsslut'] = pd.to_datetime(fi.Kvartalsslut)
      idxname = fi.Fond_namn.astype(str).str.contains('index|indexnära|exponering|etf|xact', case=False, regex=True)
      br_all = fi.groupby(['ISIN-kod_instrument', 'Kvartalsslut']).Fond_institutnummer.nunique()
      br_act = fi[~idxname].groupby(['ISIN-kod_instrument', 'Kvartalsslut']).Fond_institutnummer.nunique()
      qs = sorted(pd.to_datetime(fi.Kvartalsslut.unique()))
      first_seen = fi.groupby('ISIN-kod_instrument').Kvartalsslut.min().to_dict()
      br_all = br_all.to_dict(); br_act = br_act.to_dict()
      st = pd.read_csv(P('data/raw/lseg/panel_2005_2026/stocks_static_2005.csv'))
      isin = dict(zip(tu.RIC, tu.IssueISIN)); isin.update({k: v for k, v in zip(st.ric, st.IssueISIN) if isinstance(v, str)})
      def breadth(B, i, q):
          return B.get((i, q), 0)
      vals = []
      for _, r in S5[S5.AD >= '2019-01-01'].iterrows():
          i = isin.get(r.ric)
          pre = [q for q in qs if q < r.AD]; post = [q for q in qs if q >= cal[min(r.iE + 20, len(cal) - 1)]]
          if not isinstance(i, str) or not pre or not post or first_seen.get(i, pd.Timestamp('2100-01-01')) > pre[-1]: vals.append((np.nan, np.nan)); continue
          a0, a1 = breadth(br_all, i, pre[-1]), breadth(br_all, i, post[0]); c0, c1 = breadth(br_act, i, pre[-1]), breadth(br_act, i, post[0])
          vals.append((np.log1p(a1) - np.log1p(a0), np.log1p(c1) - np.log1p(c0)))
      S9 = S5[S5.AD >= '2019-01-01'].copy(); S9['d_br_all'] = [v[0] for v in vals]; S9['d_br_act'] = [v[1] for v in vals]
      for ty in ['addition', 'deletion']:
          s = S9[S9.type == ty]
          for v, lab in [('d_br_all', 'förändring log(1+antal fonder), alla'), ('d_br_act', 'förändring log(1+antal fonder), ej indexfonder')]:
              q = s.dropna(subset=[v])
              if q.event.sum() == 0: continue
              b, lo, hi, p, n, G = reg(q, q[v])
              rec('T9', ty, '2019-26', lab, b, lo, hi, p, n, G, f'händelser medel {q[q.event == 1][v].mean():.3f}, nästan medel {q[q.event == 0][v].mean():.3f}')
      S9.to_csv(os.path.join(OUT, 'T9_events.csv'), index=False)
      print('T9 klar')
except Exception as e:
    print('T9 hoppas över:', str(e)[:200])
S5.to_csv(os.path.join(OUT, 'T5urval_T7_T8b_events.csv'), index=False)

# %%
# ---------- T6 steg 1: Nasdaqs urvalsregel, bara träffsäkerhet
FFH = pd.read_csv(os.path.join(IND, 'lseg_freefloat_hist.csv'))
ffh = {(r.review, r.ric): r.ff for r in FFH.dropna(subset=['ff']).itertuples()}
ICB = {r: str(int(v)) for r, v in zip(K.ric, K.icb) if pd.notna(v)}
TRBC = {r: str(v) for r, v in zip(K.ric, K.trbc) if pd.notna(v)}
FFC = dict(zip(K.ric, pd.to_numeric(K.freefloat, errors='coerce')))
REFS = {'2007H2': '2007-05-31', '2008H1': '2007-11-30', '2008H2': '2008-05-30', '2009JAN': '2008-11-28'}
for c, e in zip(rev.review_cycle, rev.ED):
    if c not in REFS:
        m = {6: 4, 12: 10, 7: 5, 1: 11}[e.month]; y = e.year - (1 if e.month == 1 else 0)
        REFS[c] = str(cal[(cal.year == y) & (cal.month == m)].max().date())
hit, rows6 = [], []
for k, r in rev.iterrows():
    if k == 0: continue
    iA, iE = int(r.iAD), int(r.iED); ref = pd.Timestamp(REFS[r.review_cycle]); ir = int(pos[ref]) if ref in pos.index else nextpos(ref)
    start = nextpos(ref - pd.DateOffset(months=6))
    cl = CLOSE.iloc[ir]; U = [c for c in RICS if pd.notna(cl.get(c)) and not not_main(c)]
    if len(U) < 50: continue
    tvv = pd.Series({c: (np.nansum(TV[c].values[start:ir + 1]) if c in TV else np.nan) for c in U})
    shr = SH.iloc[max(ir - 5, 0):ir + 1].ffill().iloc[-1]
    # Rättelse 2 nov cirka 18:20: kursen i panelen är justerad för senare splittar, aktieantalet är historiskt, så kurs × aktier blir fel.
    # Nu: bolagets mcap (ojusterat) × aktieslagets andel av aktierna i bolagets noterade aktieslag samma dag. Gamla raden:
    # cm = pd.Series({c: (cl[c] * shr[c]) if pd.notna(shr.get(c)) and shr.get(c) > 0 else (mc[c].iloc[ir] if c in mc else np.nan) for c in U})
    ROOTS_ = {}
    for c_ in U: ROOTS_.setdefault(root(c_), []).append(c_)
    def klassvarde(c):
        b_ = mc[c].iloc[ir] if c in mc else np.nan
        if not (b_ > 0): return np.nan
        sy = ROOTS_[root(c)]
        if len(sy) == 1: return b_
        s_ = [shr.get(o) for o in sy]
        return b_ * shr.get(c) / sum(s_) if all(pd.notna(v) and v > 0 for v in s_) else np.nan
    cm = pd.Series({c: klassvarde(c) for c in U})
    ffsrc = pd.Series({c: ('historik' if (r.review_cycle, c) in ffh else ('aktuell' if pd.notna(FFC.get(c)) else 'ingen')) for c in U})
    ff = pd.Series({c: ffh.get((r.review_cycle, c), FFC.get(c, np.nan)) for c in U}); ff = ff.where((ff > 0) & (ff <= 100))
    D = pd.DataFrame(dict(tv=tvv, ffm=cm * (ff.fillna(100) / 100), ffsrc=ffsrc)).dropna(subset=['tv', 'ffm']); D = D[D.ffm > 0]
    D['sect'] = [ICB.get(c, 'trbc:' + TRBC[c] if c in TRBC else 'okänd') for c in D.index]
    D['mic'] = [MIC.get(c, 'okänd') for c in D.index]
    ntop = max(int(np.ceil(0.10 * len(D))), 25)
    D['top'] = D.tv.rank(ascending=False) <= ntop; D['bottom'] = D.tv.rank(ascending=False, pct=True) > 0.70
    D = D.sort_values('ffm', ascending=False)
    D['w'] = D.ffm / D.groupby('sect').ffm.transform('sum'); D['cum'] = D.groupby('sect').ffm.cumsum() / D.groupby('sect').ffm.transform('sum')
    D['sel'] = (D.top | ((D.cum - D.w) < 0.85)) & ~D.bottom
    before = MED.get(cyc[k - 1], set()); after = MED.get(cyc[k], set())
    evs = ev[ev.k == k]; adds = set(evs[evs.type == 'addition'].RIC) & set(D.index); mem_in = after & set(D.index)
    tot = D.ffm.sum()
    hit.append(dict(review=r.review_cycle, post=int(r.AD.year >= 2017), universum=len(D), regel_valda=int(D.sel.sum()), tillägg=len(adds),
                    tillägg_träffade=int(D.loc[list(adds), 'sel'].sum()) if adds else 0, medlemmar_efter=len(mem_in),
                    medlemmar_träffade=int(D.loc[list(mem_in), 'sel'].sum()) if mem_in else 0,
                    regel_nya_ej_tillagda=int((D.sel & ~D.index.isin(list(before)) & ~D.index.isin(list(adds))).sum()),
                    tillägg_ej_i_universum=len(set(evs[evs.type == 'addition'].RIC) - set(D.index)),
                    andel_utan_sektor=round(float(D[D.sect == 'okänd'].ffm.sum() / tot), 3),
                    andel_okänd_marknadsplats=round(float(D[D.mic == 'okänd'].ffm.sum() / tot), 3),
                    andel_ff_historik=round(float(D[D.ffsrc == 'historik'].ffm.sum() / tot), 3)))
    D.assign(review=r.review_cycle, medlem_före=D.index.isin(list(before)), tillagd=D.index.isin(list(adds))).to_csv(os.path.join(OUT, f'T6_regel_{r.review_cycle}.csv'))
H = pd.DataFrame(hit); H.to_csv(os.path.join(OUT, 'T6_traffsakerhet.csv'), index=False)
for pn, pv in PER.items():
    h = H[H.post == pv]
    rec('T6 steg 1', 'träffsäkerhet', pn, 'andel tillägg som regeln väljer', h.tillägg_träffade.sum() / max(h.tillägg.sum(), 1), None, None, None, int(h.tillägg.sum()), len(h),
        f'medlemmar efter som regeln väljer {h.medlemmar_träffade.sum() / max(h.medlemmar_efter.sum(), 1):.2f}; regelns nya som inte lades till per översyn {h.regel_nya_ej_tillagda.mean():.1f}; '
        f'utan sektor {h.andel_utan_sektor.mean():.2f}, okänd marknadsplats {h.andel_okänd_marknadsplats.mean():.2f}, ff-historik {h.andel_ff_historik.mean():.2f} (andel av ff-börsvärde)')
print('T6 steg 1 klar (jämförelsen körs inte i detta steg)'); print(H.to_string(index=False))

# %%
# ---------- T11: tvillingar i OMXS30
try:
    o30 = pd.read_csv(P('data/input/omxsb/omxs30_changes_2005_2026.csv'))
    KAND = [('HOLM B', '2007-01-02'), ('SSAB A', '2007-07-02'), ('MTG B', '2009-07-01'), ('KINV B', '2014-07-01'), ('MTG B', '2016-01-04'), ('SSAB A', '2021-01-04'),
            ('EPI A', '2025-07-01'), ('INDU C', '2025-07-01'), ('ATCO B', '2025-07-01'), ('ELUX B', '2025-07-01'), ('KINV B', '2025-07-01')]
    ROOTS = {'HOLM': 'HOLM', 'SSAB': 'SSAB', 'MTG': 'MTG', 'KINV': 'KINV', 'EPI': 'EPIR', 'INDU': 'INDU', 'ATCO': 'ATCO', 'ELUX': 'ELUX'}
    SIS = {'A': ['b', 'c'], 'B': ['a'], 'C': ['a']}
    TR = {}
    def trser(c):
        if c not in TR:
            t = RET[c] if c in RET else None
            TR[c] = None if t is None else (1 + t.fillna(0) / 100).cumprod().where(CLOSE[c].ffill().notna())
        return TR[c]
    def find_ric(rt, cl, i):
        c = [x for x in RICS if re.match(rf'^{rt}{cl}\.ST', x) and pd.notna(CLOSE[x].iloc[max(i - 5, 0):i + 5]).any()]
        return c[0] if c else None
    def spread(ix_, sis, a, b):
        A_, B_ = trser(ix_), trser(sis)
        if A_ is None or B_ is None or a - 1 < 0 or b >= len(cal): return np.nan
        x = np.log(A_.iloc[b] / A_.iloc[a - 1]) - np.log(B_.iloc[b] / B_.iloc[a - 1]); return 100 * x if np.isfinite(x) else np.nan
    doy = np.array(cal.dayofyear); rows11, pools = [], {}
    for tick, eff in KAND:
        r = o30[(o30.ticker == tick) & (o30.effective_date == eff)]
        if r.empty: print('saknas i listan:', tick, eff); continue
        r = r.iloc[0]; iE = nextpos(r.effective_date); iA = nextpos(r.announcement_date)
        base, cls = tick.split(' '); rt = ROOTS[base]
        ixr = find_ric(rt, cls.lower(), iE)
        sis = next((s for s in (find_ric(rt, x, iE) for x in SIS[cls]) if s), None)
        if ixr is None or sis is None: print('RIC saknas:', tick, eff, ixr, sis); continue
        v = VOL[sis].iloc[iA - 60:iE + 21] if sis in VOL else pd.Series(dtype=float); share = float((v.fillna(0) > 0).mean()) if len(v) else 0
        sign = 1 if r.type == 'addition' else -1
        obs = sign * spread(ixr, sis, iA - 1, iE + 1)
        firm_ev = [(nextpos(x.announcement_date), nextpos(x.effective_date)) for x in o30[o30.ticker.astype(str).str.startswith(base)].itertuples() if isinstance(x.announcement_date, str)]
        firm_ev += [(int(a), int(e)) for a, e in zip(ev[ev.RIC.map(stem) == stem(ixr)].iAD, ev[ev.RIC.map(stem) == stem(ixr)].iED)]
        L = (iE + 1) - (iA - 1) + 1; ad = cal[iA].dayofyear; pl = []
        for s in range(61, len(cal) - L - 21):
            if cal[s].year == cal[iA].year: continue
            dd = abs(doy[s] - ad); dd = min(dd, 365 - dd)
            if dd > 45 or any((s + L + 20 >= a - 60) and (s - 60 <= e + 20) for a, e in firm_ev): continue
            v_ = sign * spread(ixr, sis, s, s + L - 1)
            if np.isfinite(v_): pl.append(v_)
        key = f'{tick} {eff}'; pools[key] = pl
        rows11.append(dict(händelse=key, typ=r.type, index_ric=ixr, syster_ric=sis, syster_handelsandel=round(share, 3), spread=obs, n_placebo=len(pl), placebo_sd=np.std(pl) if pl else np.nan))
    T11 = pd.DataFrame(rows11); T11['med'] = (T11.syster_handelsandel >= 0.90) & T11.spread.notna() & (T11.n_placebo >= 20)
    ok = T11[T11.med]
    if len(ok):
        m = ok.spread.mean(); nm = np.array([np.mean([rng.choice(pools[k_]) for k_ in ok.händelse]) for _ in range(5000)])
        p = (np.abs(nm - nm.mean()) >= abs(m - nm.mean())).mean(); lo, hi = np.percentile(m - (nm - nm.mean()), [2.5, 97.5])
        rec('T11', 'OMXS30-tvillingar', 'alla', 'spread [AD-1,ED+1], indexslag minus systerslag (signerad)', m, lo, hi, p, len(ok), ok.syster_ric.map(root).nunique(), 'p och intervall från placebofönster')
    T11.to_csv(os.path.join(OUT, 'T11_events.csv'), index=False); json.dump(pools, open(os.path.join(OUT, 'T11_placebo.json'), 'w'))
    print(T11.to_string(index=False))
except Exception as e:
    print('T11 avbröts:', str(e)[:200])

# %%
O = pd.DataFrame(out); O.to_csv(os.path.join(OUT, 'runda2_results.csv'), index=False)
with zipfile.ZipFile('runda2_resultat.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(OUT): z.write(os.path.join(OUT, f), f)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 120)
print(O.to_string(index=False)); print('\nKlart. Ladda upp runda2_resultat.zip till Claude.')
