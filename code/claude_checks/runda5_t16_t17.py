# T16 (ESG-bytet) och T17 (kortare väntetid) enligt runda5_deklaration.md (23:22). Steg 1: styrka. Steg 2: skattning om godkänt.
import os, sys, json, re
import numpy as np, pandas as pd
from scipy.stats import t as tdist
STEP = int(sys.argv[1]); OUT = 'runda5_resultat'; os.makedirs(OUT, exist_ok=True)
R = '../..'
ix = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/indices_daily (1).csv', parse_dates=['date'])
cal = pd.DatetimeIndex(ix.loc[(ix.ric == '.OMXSBGI') & ix.close.notna(), 'date'].sort_values().unique())
S5 = pd.read_csv('runda2_resultat/T5urval_T7_T8b_events.csv', parse_dates=['AD'])
rng = np.random.default_rng(20261101)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
def wcr(X, y, g, j=0, B=9999, boot=True):
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    keep = X.std(0) > 0; keep[j] = True; X = X[:, keep]; j = int(keep[:j].sum())
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    if G < 3 or n <= k: return dict(b=np.nan, se=np.nan, lo=np.nan, hi=np.nan, p=np.nan, n=n, G=G)
    XtXi = np.linalg.pinv(X.T @ X); q = X @ XtXi[j]; adj = G / (G - 1) * (n - 1) / (n - k); Am = XtXi @ X.T
    def bse(Y):
        Bm = Y @ Am.T; E = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in E * q])
        return Bm[:, j], np.sqrt((sg ** 2).sum(1) * adj)
    b0, s0 = bse(y[None, :]); b0, s0 = b0[0], s0[0]; qq = tdist.ppf(.975, G - 1); p = np.nan
    if boot:
        Xr = np.delete(X, j, 1); fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]; er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = (np.abs(np.concatenate(ts)[:B]) >= abs(b0 / s0)).mean()
    return dict(b=b0, se=s0, lo=b0 - qq * s0, hi=b0 + qq * s0, p=p, n=n, G=G)
def mde(r): return (tdist.ppf(.975, r['G'] - 1) + tdist.ppf(.80, r['G'] - 1)) * r['se']
FE = lambda s: pd.get_dummies(s.review).astype(float).values

# ---------- T16: klassning med FI
tu = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/td_universe.csv'); st = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/stocks_static_2005.csv')
isin = dict(zip(tu.RIC, tu.IssueISIN)); isin.update({k: v for k, v in zip(st.ric, st.IssueISIN) if isinstance(v, str)})
H = pd.read_pickle('data/fi_all_holdings.pkl')
H['antal'] = pd.to_numeric(H.antal.astype(str).str.replace(',', '.').str.replace(' ', ''), errors='coerce')
H = H[H.antal > 0].copy(); H['fund_id'] = H.fund_id.astype(str); H['kv'] = pd.to_datetime(H.kvartal)
HOLD = H.groupby(['isin', 'kv']).fund_id.agg(set).to_dict(); qs = sorted(H.kv.unique())
F = pd.read_csv('data/fi_all_funds_klass.csv'); F['fund_id'] = F.fund_id.astype(str); F['kv'] = pd.to_datetime(F.kvartal)
j_ = F.jmf.fillna('').str.lower()
F['esg'] = F.bred.astype(bool) & j_.str.contains(r'stockholm benchmark|omxsb|\bsbx') & j_.str.contains(r'esg|responsible|sustainab|hållbar|custom|paris|climate')
ESG = F[F.esg].groupby('kv').fund_id.agg(set).to_dict()
A = S5[(S5.event == 1) & (S5.type == 'addition') & (S5.AD >= '2022-11-01')].copy()
def post_q(iE):
    c = [q for q in qs if q >= cal[min(int(iE) + 20, len(cal) - 1)]]; return c[0] if c else None
A['q1'] = A.iE.map(post_q); A['isn'] = A.ric.map(isin)
A['andel_esg'] = [len(HOLD.get((i, q), set()) & ESG.get(q, set())) / len(ESG[q]) if (q is not None and isinstance(i, str) and ESG.get(q)) else np.nan for i, q in zip(A.isn, A.q1)]
A['grupp'] = np.where(A.andel_esg < 0.2, 'utanför', np.where(A.andel_esg >= 0.5, 'inom', np.where(A.andel_esg.notna(), 'mellan', 'saknas')))
A16 = A[A.grupp.isin(['utanför', 'inom'])].copy(); A16['ut'] = (A16.grupp == 'utanför').astype(float)
def r16(boot):
    X = np.column_stack([A16.ut.values, A16.ru.values, A16.lm.values, FE(A16)]); return wcr(X, A16['car_ED+1'].values.astype(float), A16.review.values, 0, boot=boot)
# ---------- T17
T = S5[(S5.type == 'addition') & (S5.post == 1)].copy(); T['kort'] = (T.AD >= '2021-05-01').astype(float)
def r17(boot):
    X = np.column_stack([(T.event * T.kort).values, T.event.values.astype(float), T.ru.values, T.lm.values, FE(T)]); return wcr(X, T['car_ED+1'].values.astype(float), T.review.values, 0, boot=boot)

if STEP == 1:
    print('T16 klassning:', A.grupp.value_counts().to_dict())
    u = A16[A16.ut == 1]; n_u, g_u = len(u), u.review.nunique()
    r = r16(False); m16 = mde(r)
    ok16 = bool(n_u >= 8 and g_u >= 4 and m16 <= 1.5)
    print(f'T16: utanför {n_u} tillägg i {g_u} översyner, inom {int((A16.ut == 0).sum())}; G {r["G"]}; MDE {m16:.2f} (gräns 1,5) -> {"GODKÄNT" if ok16 else "STOPP"}')
    r = r17(False); m17 = mde(r)
    ok17 = bool(m17 <= 0.92)
    print(f'T17: tillägg kort väntetid {int(T[(T.event == 1) & (T.kort == 1)].shape[0])}, lång {int(T[(T.event == 1) & (T.kort == 0)].shape[0])}; G {r["G"]}; MDE {m17:.2f} (gräns 0,92) -> {"GODKÄNT" if ok17 else "STOPP"}')
    json.dump(dict(T16=dict(passed=ok16, n_ut=n_u, g_ut=g_u, mde=float(m16)), T17=dict(passed=ok17, mde=float(m17))), open(f'{OUT}/steg1.json', 'w'), indent=1)
    A[['review', 'ric', 'isn', 'q1', 'andel_esg', 'grupp']].to_csv(f'{OUT}/T16_klassning.csv', index=False)
    sys.exit()
s1 = json.load(open(f'{OUT}/steg1.json'))
for k, f in [('T16', r16), ('T17', r17)]:
    if not s1[k]['passed']: print(k, 'stoppat i steg 1, ingen skattning'); continue
    r = f(True); print(k, {kk: round(float(v), 3) for kk, v in r.items()})
