# Runda 4, T14: vilka fonder blir nya ägare. Deklarerat i runda4_deklaration.md (22:55 CET).
# Körs i tre steg: python3 runda4.py 0 | 1 | 2. Steg 2 körs bara om steg 1 godkänt.
import os, re, sys, json
import numpy as np, pandas as pd
from scipy.stats import t as tdist

STEP = int(sys.argv[1])
R = '../..'
OUT = 'runda4_resultat'; os.makedirs(OUT, exist_ok=True)

# ---------- underlag
ix = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/indices_daily (1).csv', parse_dates=['date'])
cal = pd.DatetimeIndex(ix.loc[(ix.ric == '.OMXSBGI') & ix.close.notna(), 'date'].sort_values().unique())
S5 = pd.read_csv('runda2_resultat/T5urval_T7_T8b_events.csv', parse_dates=['AD'])
S = S5[S5.AD >= '2019-01-01'].copy().reset_index(drop=True)
tu = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/td_universe.csv')
st = pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/stocks_static_2005.csv')
isin = dict(zip(tu.RIC, tu.IssueISIN)); isin.update({k: v for k, v in zip(st.ric, st.IssueISIN) if isinstance(v, str)})

H = pd.read_pickle('data/fi_all_holdings.pkl')
H['antal'] = pd.to_numeric(H.antal.astype(str).str.replace(',', '.').str.replace(' ', ''), errors='coerce')
H = H[H.antal > 0].copy(); H['fund_id'] = H.fund_id.astype(str); H['kv'] = pd.to_datetime(H.kvartal)
F = pd.read_csv('data/fi_all_funds_klass.csv'); F['fund_id'] = F.fund_id.astype(str); F['kv'] = pd.to_datetime(F.kvartal)
F = F.drop_duplicates(['kv', 'fund_id'], keep='last')
qs = sorted(H.kv.unique())
first_seen = H.groupby('isin')['kv'].min().to_dict()
HOLD = H.groupby(['isin', 'kv']).fund_id.agg(set).to_dict()

def quarters(r):
    pre = [q for q in qs if q < r.AD]; post = [q for q in qs if q >= cal[min(int(r.iE) + 20, len(cal) - 1)]]
    return (pre[-1] if pre else None), (post[0] if post else None)
S['isn'] = S.ric.map(isin)
QQ = [quarters(r) for r in S.itertuples()]
S['q0'] = [a for a, b in QQ]; S['q1'] = [b for a, b in QQ]
S['ok'] = [isinstance(i, str) and a is not None and b is not None and first_seen.get(i, pd.Timestamp('2100-01-01')) <= a for i, a, b in zip(S.isn, S.q0, S.q1)]

# ---------- inferens (samma som runda 2)
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
    b0, s0 = bse(y[None, :]); b0, s0 = b0[0], s0[0]; qq = tdist.ppf(.975, G - 1)
    p = np.nan
    if boot:
        Xr = np.delete(X, j, 1); fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]; er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = (np.abs(np.concatenate(ts)[:B]) >= abs(b0 / s0)).mean()
    return dict(b=b0, se=s0, lo=b0 - qq * s0, hi=b0 + qq * s0, p=p, n=n, G=G)
def reg(s, y, boot=True):
    FE = pd.get_dummies(s.review).astype(float).values
    X = np.column_stack([s.event.values.astype(float), s.ru.values, s.lm.values, FE])
    return wcr(X, np.asarray(y, float), s.review.values, 0, boot=boot)
def mde(r): return (tdist.ppf(.975, r['G'] - 1) + tdist.ppf(.80, r['G'] - 1)) * r['se']
fmt = lambda r: f"{r['b']:+.3f} ({r['lo']:+.3f} till {r['hi']:+.3f}), p {r['p']:.3f}, N {r['n']}, G {r['G']}"

# ---------- steg 0: T9 återskapat
if STEP == 0:
    IDX = F.namn.astype(str).str.contains('index|indexnära|exponering|etf|xact', case=False, regex=True)
    nonidx = set(zip(F.kv[~IDX], F.fund_id[~IDX]))
    v_all, v_act = [], []
    for r in S.itertuples():
        if not r.ok: v_all.append(np.nan); v_act.append(np.nan); continue
        h0 = HOLD.get((r.isn, r.q0), set()); h1 = HOLD.get((r.isn, r.q1), set())
        v_all.append(np.log1p(len(h1)) - np.log1p(len(h0)))
        v_act.append(np.log1p(sum((r.q1, f) in nonidx for f in h1)) - np.log1p(sum((r.q0, f) in nonidx for f in h0)))
    S['d_br_all'] = v_all; S['d_br_act'] = v_act
    res = {}
    for ty in ['addition', 'deletion']:
        for v in ['d_br_all', 'd_br_act']:
            q = S[(S.type == ty)].dropna(subset=[v]); r = reg(q, q[v]); res[f'{ty} {v}'] = r
            print('T9 återskapat', ty, v, fmt(r))
    known = {'addition d_br_all': 0.35, 'addition d_br_act': 0.38}
    passed = all(abs(res[k]['b'] - v) <= 0.03 for k, v in known.items())
    print('Steg 0', 'GODKÄNT' if passed else 'STOPP: avviker mer än 0,03 från runda 2')
    json.dump(dict(passed=bool(passed), **{k: {kk: float(vv) for kk, vv in r.items()} for k, r in res.items()}), open(f'{OUT}/steg0.json', 'w'), indent=1)
    sys.exit()

# ---------- fondgrupper
NAMEIDX = F.namn.astype(str).str.contains('index|indexnära|exponering|etf|xact|passiv|access', case=False, regex=True)
j = F.jmf.fillna('').str.lower()
F['B'] = j.str.contains(r'stockholm benchmark|omxsb|\bsbx')
F['Hh'] = j.str.contains(r'six ?(?:portfolio|prx|return|rx)|sixrx|sixprx|omxs ?gi|omxspi|all.?share') & ~F.B
F['ren'] = ~j.str.contains(r';|\|')
F['aktiv'] = ~F.bred.astype(bool) & ~NAMEIDX
SEN = H[H['isin'].str.startswith('SE')].groupby(['kv', 'fund_id'])['isin'].nunique()
F['nse'] = [SEN.get((a, b), 0) for a, b in zip(F.kv, F.fund_id)]
present = F.groupby('kv').fund_id.agg(set).to_dict()
def group(q0, q1, col, pure=False):
    f = F[(F.kv == q0) & F.aktiv & F[col] & (F.nse >= 10)]
    if pure: f = f[f.ren]
    return set(f.fund_id) & present.get(q1, set())
GC = {}
def G_(q0, q1, col, pure=False):
    k = (q0, q1, col, pure)
    if k not in GC: GC[k] = group(q0, q1, col, pure)
    return GC[k]
def dfrac(r, funds):
    if not funds: return np.nan
    h0 = HOLD.get((r.isn, r.q0), set()) & funds; h1 = HOLD.get((r.isn, r.q1), set()) & funds
    return 100 * (len(h1) - len(h0)) / len(funds)
def dlogn(r, funds):
    if not funds: return np.nan
    return np.log1p(len(HOLD.get((r.isn, r.q1), set()) & funds)) - np.log1p(len(HOLD.get((r.isn, r.q0), set()) & funds))
rows = []
for r in S.itertuples():
    d = {}
    if r.ok:
        for pure in (False, True):
            sfx = '_ren' if pure else ''
            B = G_(r.q0, r.q1, 'B', pure); Hh = G_(r.q0, r.q1, 'Hh', pure)
            d['dB' + sfx] = dfrac(r, B); d['dH' + sfx] = dfrac(r, Hh); d['dBH' + sfx] = dfrac(r, B | Hh)
            d['nB' + sfx] = len(B); d['nH' + sfx] = len(Hh)
            d['lB' + sfx] = dlogn(r, B); d['lH' + sfx] = dlogn(r, Hh)
    rows.append(d)
S = pd.concat([S, pd.DataFrame(rows)], axis=1)
S['dD'] = S.dB - S.dH; S['dD_ren'] = S.dB_ren - S.dH_ren; S['lD'] = S.lB - S.lH

# ---------- steg 1: styrkekontroll, inga skattningar för E_H, E_B, E_D
if STEP == 1:
    q = S[S.type == 'addition']
    print('grupp B per händelse, median antal fonder:', q.nB.median(), '| grupp H:', q.nH.median())
    out = {}
    for v, lab in [('dBH', 'E_BH'), ('dH', 'E_H'), ('dD', 'E_D')]:
        qq = q.dropna(subset=[v]); rr = reg(qq, qq[v], boot=(lab == 'E_BH'))
        out[lab] = dict(se=float(rr['se']), mde=float(mde(rr)), n=int(rr['n']), G=int(rr['G']))
        if lab == 'E_BH': out[lab].update(b=float(rr['b']), lo=float(rr['lo']), hi=float(rr['hi']), p=float(rr['p']))
    E = out['E_BH']['b']
    c1 = out['E_D']['mde'] <= E; c2 = out['E_H']['mde'] <= 0.5 * E
    print(f"E_BH (skala, motsvarar T9): {E:+.3f} pe ({out['E_BH']['lo']:+.3f} till {out['E_BH']['hi']:+.3f}), N {out['E_BH']['n']}, G {out['E_BH']['G']}")
    print(f"MDE E_D: {out['E_D']['mde']:.3f}  (gräns {E:.3f})  -> {'ok' if c1 else 'för stort'}")
    print(f"MDE E_H: {out['E_H']['mde']:.3f}  (gräns {0.5 * E:.3f})  -> {'ok' if c2 else 'för stort'}")
    passed = bool(c1 and c2)
    print('Steg 1', 'GODKÄNT: testet är informativt' if passed else 'STOPP: testet är inte informativt')
    json.dump(dict(passed=passed, **out), open(f'{OUT}/steg1.json', 'w'), indent=1)
    sys.exit()

# ---------- steg 2: skattningar, bara om steg 1 godkänt
s1 = json.load(open(f'{OUT}/steg1.json'))
if not s1['passed']: sys.exit('STOPP: steg 1 inte godkänt, skattningarna visas inte.')
res = []
for ty in ['addition', 'deletion']:
    q = S[S.type == ty]
    for v, lab in [('dH', 'E_H (primär)'), ('dD', 'E_D (primär)'), ('dB', 'E_B'), ('dBH', 'E_BH'),
                   ('dH_ren', 'känslighet E_H, rena fonder'), ('dD_ren', 'känslighet E_D, rena fonder'),
                   ('lH', 'känslighet E_H, log(1+antal)'), ('lD', 'känslighet E_D, log(1+antal)')]:
        qq = q.dropna(subset=[v]); rr = reg(qq, qq[v])
        ev_m = qq[qq.event == 1][v].mean(); nm_m = qq[qq.event == 0][v].mean()
        res.append(dict(typ=ty, mått=lab, skattning=rr['b'], ci_lo=rr['lo'], ci_hi=rr['hi'], p_wcb=rr['p'], N=rr['n'], G=rr['G'],
                        händelser_medel=ev_m, nästan_medel=nm_m, händelser=int(qq.event.sum())))
        print(ty, lab, fmt(rr), f'| medel händelser {ev_m:+.2f}, nästan {nm_m:+.2f}')
pd.DataFrame(res).to_csv(f'{OUT}/T14_results.csv', index=False)
S.to_csv(f'{OUT}/T14_events.csv', index=False)
