# %% [markdown]
# # Robusthet på hela panelen: T2-hela och T5 (nästan tillagda)
# Deklarerat 2026-11-01 19:23 CET i `robusthet_deklaration.md`.
#
# 1. Lägg notebooken i repo-mappen `financethesis/`.
# 2. Kör alla celler (Run All). Det tar några minuter.
# 3. Ladda upp `robusthet_hela_resultat.zip` till Claude.
#
# Ger första cellen fel om parquet: kör `pip install pyarrow`. Är parquet-filen bara 134 byte: kör `git lfs pull`.

# %%
import os, re, zipfile
import numpy as np, pandas as pd
try:
    from scipy.stats import t as tdist
except ImportError:  # utan scipy: t-kvantil via Cornish-Fisher-approximation
    from statistics import NormalDist
    class tdist:
        @staticmethod
        def ppf(p, df):
            z = NormalDist().inv_cdf(p)
            return z + (z**3 + z) / (4 * df) + (5 * z**5 + 16 * z**3 + 3 * z) / (96 * df**2) + (3 * z**7 + 19 * z**5 + 17 * z**3 - 15 * z) / (384 * df**3)
ROOT = os.environ.get('ROOT', '.')
PANEL = os.environ.get('PANEL', 'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet')
OUT = os.environ.get('OUT', 'robusthet_hela_resultat')
os.makedirs(OUT, exist_ok=True)
P = lambda *a: os.path.join(ROOT, *a)
COLS = ['ric', 'date', 'close', 'totret', 'volume', 'mcap']
if PANEL.endswith('.parquet'):
    px = pd.read_parquet(P(PANEL) if not os.path.isabs(PANEL) else PANEL, columns=COLS)
else:
    px = pd.read_csv(PANEL, usecols=COLS)
px['date'] = pd.to_datetime(px['date'])
px = px[px.ric.astype(str).str.contains(r'\.ST')]
print('panel:', len(px), 'rader,', px.ric.nunique(), 'aktier')

# %%
ix = pd.read_csv(P('data/raw/lseg/panel_2005_2026/indices_daily (1).csv'), parse_dates=['date'])
cal = pd.DatetimeIndex(ix.loc[(ix.ric == '.OMXSBGI') & ix.close.notna(), 'date'].sort_values().unique())
pos = pd.Series(np.arange(len(cal)), index=cal)
mkt = ix.pivot(index='date', columns='ric', values='close').reindex(cal).pct_change()['.OMXSBGI'] * 100
px = px[px.date.isin(cal)].drop_duplicates(['ric', 'date'], keep='last').sort_values(['ric', 'date'])
def rser(g):
    g = g.set_index('date'); r = g.totret.fillna(g.close.pct_change() * 100)
    return r.reindex(cal[(cal >= g.index.min()) & (cal <= g.index.max())])
RET = pd.DataFrame({r: rser(g) for r, g in px.groupby('ric')}).reindex(cal)
n_err = int((RET > 1000).sum().sum()); RET = RET.mask(RET > 1000)  # datafel (deklarerat 19:26): dagsavkastning över 1 000 %
print('dagsavkastningar över 1 000 % satta till saknad:', n_err)
AR = RET.sub(mkt, axis=0)
RICS = list(AR.columns); CI = {r: i for i, r in enumerate(RICS)}
A = AR.values
CS = np.vstack([np.zeros(A.shape[1]), np.nancumsum(A, axis=0)])
CN = np.vstack([np.zeros(A.shape[1]), np.cumsum(np.isnan(A), axis=0)])
def wsum(ric, a, b):
    if ric not in CI or pd.isna(a) or pd.isna(b): return np.nan
    a = int(a); b = int(b)
    if a < 0 or b >= len(cal): return np.nan
    j = CI[ric]
    return np.nan if CN[b + 1, j] - CN[a, j] > 0 else CS[b + 1, j] - CS[a, j]
mc = px.pivot_table(index='date', columns='ric', values='mcap').reindex(cal).ffill(limit=10)
tv = (px.assign(v=px.volume * px.close)).pivot_table(index='date', columns='ric', values='v').reindex(cal)
ev = pd.read_csv(P('output/omxsb_replication_2007/events_car.csv'), parse_dates=['AD', 'ED'])
ev['iAD'] = ev.AD.map(pos); ev['iED'] = ev.ED.map(pos)
ev['post'] = (ev.AD.dt.year >= 2017).astype(int)
ev['car'] = [wsum(r, a - 1, e + 1) for r, a, e in zip(ev.RIC, ev.iAD, ev.iED)]
rev = ev.groupby('review_cycle').agg(AD=('AD', 'first'), iAD=('iAD', 'first'), iED=('iED', 'first')).sort_values('AD').reset_index()
rev['k'] = np.arange(len(rev)); ev['k'] = ev.review_cycle.map(dict(zip(rev.review_cycle, rev.k)))
has_ev = set(zip(ev.RIC, ev.k))
print('kalender', cal.min().date(), cal.max().date(), '| händelser', len(ev), '| CAR saknas', int(ev.car.isna().sum()))

# %%
rng = np.random.default_rng(20261101)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
def ci_mean(y, g):
    m = pd.Series(np.asarray(y, float), index=np.asarray(g)).dropna().groupby(level=0).mean(); G = len(m)
    se = m.std(ddof=1) / np.sqrt(G); q = tdist.ppf(.975, G - 1)
    return m.mean(), m.mean() - q * se, m.mean() + q * se, G
def signflip(y, g, B=20000):
    m = pd.Series(np.asarray(y, float), index=np.asarray(g)).dropna().groupby(level=0).mean().values
    s = (m * rng.choice([-1, 1], (B, len(m)))).mean(1)
    return (np.abs(s) >= abs(m.mean())).mean()
def wcb_mean(y, g, B=9999):
    d = pd.DataFrame({'y': np.asarray(y, float), 'g': np.asarray(g)}).dropna()
    codes = pd.factorize(d.g)[0]; G = codes.max() + 1; v = d.y.values; n = len(v)
    def tst(V):
        mu = V.mean(1, keepdims=True); e = V - mu
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in e])
        return mu[:, 0] / (np.sqrt((sg ** 2).sum(1)) / n * np.sqrt(G / (G - 1)))
    t0 = tst(v[None, :])[0]; ts = []
    for _ in range(B // 1000 + 1):
        W = wdraw(1000, G); ts.append(tst(v[None, :] * W[:, codes]))
    ts = np.concatenate(ts)[:B]
    return (np.abs(ts) >= abs(t0)).mean()
def wcr(X, y, g, j, B=9999):
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    keep = X.std(0) > 0; keep[j] = True
    X = X[:, keep]; j = int(keep[:j].sum())
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X); h = XtXi[j]; q = X @ h; adj = G / (G - 1) * (n - 1) / (n - k)
    Am = XtXi @ X.T
    def bse(Y):
        Bm = Y @ Am.T; E = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in E * q])
        return Bm[:, j], np.sqrt((sg ** 2).sum(1) * adj)
    b0, s0 = bse(y[None, :]); b0 = b0[0]; s0 = s0[0]
    Xr = np.delete(X, j, 1); fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]; er = y - fr
    ts = []
    for _ in range(B // 1000 + 1):
        W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
    ts = np.concatenate(ts)[:B]; qq = tdist.ppf(.975, G - 1)
    return b0, b0 - qq * s0, b0 + qq * s0, (np.abs(ts) >= abs(b0 / s0)).mean(), n, G
out = []
def rec(test, typ, per, variant, N, G, m, lo, hi, p_sf, p_wcb, note=''):
    out.append(dict(test=test, typ=typ, period=per, variant=variant, N=N, G=G, skattning=round(m, 3), ci_lo=round(lo, 3), ci_hi=round(hi, 3),
                    p_teckenbyte=None if p_sf is None else round(p_sf, 4), p_wcb=None if p_wcb is None else round(p_wcb, 4), not_=note))
PER = {'före': 0, 'efter': 1}
def root(r):
    m = re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST', str(r)); return m.group(1) if m else str(r)

# %%
# ---------- T2-hela: matchad kontroll, identisk med T2 men med hela panelen som pool
rows = []
for k, r in rev.iterrows():
    iA, iE = int(r.iAD), int(r.iED)
    if iA - 100 < 0 or iE + 1 >= len(cal): continue
    evs = ev[ev.k == k]; cand = []
    for c in RICS:
        if any((c, kk) in has_ev for kk in (k - 1, k, k + 1)): continue
        ru = wsum(c, iA - 100, iA - 1); cr = wsum(c, iA - 1, iE + 1); m = mc[c].iloc[iA - 1] if c in mc else np.nan
        if np.isnan(ru) or np.isnan(cr) or not (m > 0): continue
        cand.append((c, root(c), ru, np.log(m), cr))
    if len(cand) < 3: continue
    C = pd.DataFrame(cand, columns=['ric', 'root', 'ru', 'lm', 'car'])
    E = evs.assign(ru=[wsum(x, iA - 100, iA - 1) for x in evs.RIC],
                   lm=[np.log(mc[x].iloc[iA - 1]) if x in mc and mc[x].iloc[iA - 1] > 0 else np.nan for x in evs.RIC]).dropna(subset=['ru', 'lm', 'car'])
    allv = pd.concat([C[['ru', 'lm']], E[['ru', 'lm']]]); mu = allv.mean(); sd = allv.std()
    Cz = ((C[['ru', 'lm']] - mu) / sd).values
    for _, e in E.iterrows():
        ez = ((e[['ru', 'lm']].astype(float) - mu) / sd).values.astype(float)
        mask = (C.root != root(e.RIC)).values
        dist = np.sqrt(((Cz - ez) ** 2).sum(1)); dist[~mask] = np.inf; o = np.argsort(dist)[:3]
        rows.append(dict(event_id=e.event_id, RIC=e.RIC, type=e.type, post=e.post, review=e.review_cycle, car=e.car, ru=e.ru, lm=e.lm,
                         c1=C.ric.iloc[o[0]], c1_car=C.car.iloc[o[0]], c1_ru=C.ru.iloc[o[0]], c1_lm=C.lm.iloc[o[0]], c3_car=C.car.iloc[o].mean(), n_cand=int(mask.sum())))
M = pd.DataFrame(rows); M['diff1'] = M.car - M.c1_car; M['diff3'] = M.car - M.c3_car
for ty in ['addition', 'deletion']:
    for pn, pv in PER.items():
        q = M[(M.type == ty) & (M.post == pv)]
        for v, lab in [('diff1', 'händelse minus 1 kontroll'), ('diff3', 'händelse minus 3 kontroller'), ('c1_car', 'kontrollens CAR')]:
            m, lo, hi, G = ci_mean(q[v], q.review)
            note = f'balans: uppgång {q.ru.mean():.2f} mot {q.c1_ru.mean():.2f}; log mcap {q.lm.mean():.2f} mot {q.c1_lm.mean():.2f}; kandidater median {q.n_cand.median():.0f}' if v == 'diff1' else ''
            rec('T2-hela', ty, pn, lab, int(q[v].notna().sum()), G, m, lo, hi, signflip(q[v], q.review), wcb_mean(q[v], q.review), note)
M.to_csv(os.path.join(OUT, 'T2_hela_events.csv'), index=False)
print('T2-hela klar:', len(M), 'händelser matchade')

# %%
# ---------- T5: nästan tillagda (och nästan borttagna)
mem = pd.read_csv(P('output/omxsb_replication_2007/mechanisms/omxsb_membership_by_review.csv'))
mem_after = {r.review_cycle: set(str(r.members_after).split(';')) for r in mem.itertuples()}
tu = pd.read_csv(P('data/raw/lseg/panel_2005_2026/td_universe.csv'))
tick2ric = tu.dropna(subset=['TickerSymbol']).groupby('TickerSymbol').RIC.apply(list).to_dict()
def resolve(keys, iA):
    out_, miss = set(), 0
    for kk in keys:
        if not kk.startswith('T:'): out_.add(kk); continue
        cands = [x for x in tick2ric.get(kk[2:], []) if x in CI and not np.isnan(A[max(iA - 5, 0):iA, CI[x]]).all()]
        if cands: out_.update(cands)
        else: miss += 1
    return out_, miss
def stem(r): return re.sub(r'(sdb)?[abcr]?\.ST.*$', '', str(r))
cyc = list(rev.review_cycle); rows = []; miss_log = []
for k, r in rev.iterrows():
    iA, iE = int(r.iAD), int(r.iED)
    if iA - 120 < 0 or iE + 1 >= len(cal) or k == 0: continue
    before, nmiss = resolve(mem_after.get(cyc[k - 1], set()), iA)
    miss_log.append(dict(review=cyc[k], members_before=len(before), unresolved_tickers=nmiss))
    evs = ev[ev.k == k]; adds = set(evs[evs.type == 'addition'].RIC); dels = set(evs[evs.type == 'deletion'].RIC)
    ev_stems = set(stem(x) for x in evs.RIC)
    def stats(c):
        return wsum(c, iA - 100, iA - 1), wsum(c, iA - 1, iE + 1), (mc[c].iloc[iA - 1] if c in mc else np.nan)
    pool = []
    for c in RICS:
        if any((c, kk) in has_ev for kk in (k - 1, k, k + 1)) or stem(c) in ev_stems: continue
        ru, cr, m = stats(c)
        if np.isnan(ru) or np.isnan(cr) or not (m > 0): continue
        tvv = np.nansum(tv[c].values[iA - 120:iA]) if c in tv else 0
        pool.append(dict(ric=c, stem=stem(c), member=c in before, ru=ru, car=cr, mcap=m, tval=tvv))
    Pq = pd.DataFrame(pool)
    if Pq.empty: continue
    Pq = Pq.sort_values('tval', ascending=False).drop_duplicates('stem')
    for ty, S in [('addition', adds), ('deletion', dels)]:
        E = []
        for c in S:
            ru, cr, m = stats(c)
            if not (np.isnan(ru) or np.isnan(cr) or not (m > 0)): E.append(dict(ric=c, ru=ru, car=cr, mcap=m))
        if not E: continue
        E = pd.DataFrame(E)
        if ty == 'addition': N = Pq[(~Pq.member) & (Pq.mcap >= E.mcap.min())]
        else: N = Pq[(Pq.member) & (Pq.mcap <= E.mcap.max())]
        for _, e in E.iterrows():
            rows.append(dict(review=cyc[k], k=k, post=int(r.AD.year >= 2017), type=ty, event=1, ric=e.ric, ru=e.ru, car=e.car, lm=np.log(e.mcap)))
        for _, e in N.iterrows():
            rows.append(dict(review=cyc[k], k=k, post=int(r.AD.year >= 2017), type=ty, event=0, ric=e.ric, ru=e.ru, car=e.car, lm=np.log(e.mcap)))
N5 = pd.DataFrame(rows)
N5.to_csv(os.path.join(OUT, 'T5_events.csv'), index=False)
pd.DataFrame(miss_log).to_csv(os.path.join(OUT, 'T5_membership_log.csv'), index=False)
for ty in ['addition', 'deletion']:
    for pn, pv in PER.items():
        s = N5[(N5.type == ty) & (N5.post == pv)]
        if s.empty or s.event.sum() == 0 or (s.event == 0).sum() == 0: continue
        FE = pd.get_dummies(s.review).astype(float).values
        X = np.column_stack([s.event.values.astype(float), s.ru.values, s.lm.values, FE])
        b, lo, hi, p, n, G = wcr(X, s.car.values.astype(float), s.review.values, 0)
        rec('T5', ty, pn, 'regression b (uppgång, storlek, fasta effekter per översyn)', n, G, b, lo, hi, None, p,
            f'händelser {int(s.event.sum())}, nästan {int((s.event == 0).sum())}; median nästan per översyn {s[s.event == 0].groupby("review").size().median():.0f}')
        d = s.groupby(['review', 'event']).car.mean().unstack().dropna()
        if len(d) >= 3:
            dd = d[1] - d[0]; m, lo, hi, G = ci_mean(dd.values, dd.index)
            rec('T5', ty, pn, 'skillnad per översyn (händelse minus nästan)', len(dd), G, m, lo, hi, signflip(dd.values, dd.index), wcb_mean(dd.values, dd.index),
                f'händelser CAR {s[s.event == 1].car.mean():.2f}, nästan CAR {s[s.event == 0].car.mean():.2f}; uppgång {s[s.event == 1].ru.mean():.1f} mot {s[s.event == 0].ru.mean():.1f}')
print('T5 klar:', int(N5.event.sum()) if len(N5) else 0, 'händelser,', int((N5.event == 0).sum()) if len(N5) else 0, 'nästan-observationer')

# %%
O = pd.DataFrame(out); O.to_csv(os.path.join(OUT, 'robusthet_hela_results.csv'), index=False)
with zipfile.ZipFile('robusthet_hela_resultat.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(OUT): z.write(os.path.join(OUT, f), f)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 140)
print(O.to_string(index=False))
print('\nKlart. Ladda upp robusthet_hela_resultat.zip till Claude.')
