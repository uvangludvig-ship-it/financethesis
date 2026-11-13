# Runda 9, T27: professionell bevakning (antal vinstprognoser i konsensus, FY1). Deklarerat i runda9_deklaration.md.
# Körs från code/claude_checks: python3 runda9_t27.py 1|2
import os, sys, json
import numpy as np, pandas as pd
from scipy.stats import t as tdist
STEP = int(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__)); R = os.environ.get('REPO', os.path.join(HERE, '..', '..'))
D = os.environ.get('DATA', os.path.join(HERE, 'data')); OUT = os.path.join(HERE, 'runda9_resultat'); os.makedirs(OUT, exist_ok=True)
A = pd.read_csv(os.path.join(D, 'runda8_analytiker.csv.gz'), low_memory=False)
v = [c for c in A.columns if 'Number of Included Estimates' in c][0]
A['m'] = pd.to_datetime(A.Date, errors='coerce').dt.to_period('M'); A = A.dropna(subset=['m'])
har = set(A[A[v].notna()].Instrument)
N = A.groupby(['Instrument', 'm'])[v].max()
S = pd.read_csv(os.path.join(HERE, 'runda2_resultat', 'T5urval_T7_T8b_events.csv'), parse_dates=['AD'])
ev = pd.read_csv(os.path.join(R, 'output/omxsb_replication_2007/events_car.csv'), parse_dates=['ED'])
EDr = ev.groupby('review_cycle').ED.first().to_dict(); S['ED'] = S.review.map(EDr)
def utfall(r):
    if r.ric not in har: return np.nan
    a = pd.Period(r.AD, 'M'); e = pd.Period(r.ED, 'M')
    fore = [N.get((r.ric, a - k), np.nan) for k in range(1, 7)]; efter = [N.get((r.ric, e + k), np.nan) for k in range(3, 7)]
    fore = np.nan_to_num(np.array(fore, float), nan=0.0); efter = np.nan_to_num(np.array(efter, float), nan=0.0)
    return np.log1p(efter).mean() - np.log1p(fore).mean()
S['d_ana'] = [utfall(r) for r in S.itertuples()]
S['n_fore'] = [np.nanmean([N.get((r.ric, pd.Period(r.AD, 'M') - k), np.nan) for k in range(1, 7)]) if r.ric in har else np.nan for r in S.itertuples()]
rng = np.random.default_rng(20261102)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
def wcr(X, y, g, j=0, B=9999, boot=True):
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    keep = X.std(0) > 0; keep[j] = True; X = X[:, keep]; j = int(keep[:j].sum())
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X); q = X @ XtXi[j]; adj = G / (G - 1) * (n - 1) / (n - k); Am = XtXi @ X.T
    def bse(Y):
        Bm = Y @ Am.T; E = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in E * q]); return Bm[:, j], np.sqrt((sg ** 2).sum(1) * adj)
    b0, s0 = bse(y[None, :]); b0, s0 = b0[0], s0[0]; qq = tdist.ppf(.975, G - 1); p = np.nan
    if boot:
        Xr = np.delete(X, j, 1); fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]; er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = (np.abs(np.concatenate(ts)[:B]) >= abs(b0 / s0)).mean()
    return dict(b=b0, se=s0, lo=b0 - qq * s0, hi=b0 + qq * s0, p=p, n=n, G=G)
def reg(s, boot=True):
    FE = pd.get_dummies(s.review).astype(float).values
    X = np.column_stack([s.event.values.astype(float), s.ru.values, s.lm.values, FE])
    return wcr(X, s.d_ana.values.astype(float), s.review.values, 0, boot=boot)
mde = lambda r: (tdist.ppf(.975, r['G'] - 1) + tdist.ppf(.80, r['G'] - 1)) * r['se']
prim = S[(S.type == 'addition') & (S.post == 1)].dropna(subset=['d_ana'])
S.to_csv(os.path.join(OUT, 'T27_urval.csv'), index=False)
if STEP == 1:
    r = reg(prim, boot=False); res = dict(n=int(r['n']), G=int(r['G']), se=float(r['se']), mde=float(mde(r)), villkor=0.15, godkant=bool(mde(r) <= 0.15),
          andel_med_data=float(S[(S.type == 'addition') & (S.post == 1)].d_ana.notna().mean()))
    print(f"T27: N {r['n']}, G {r['G']}, SE {r['se']:.3f}, MDE {mde(r):.3f} (villkor ≤ 0,15) ->", 'GODKÄNT' if res['godkant'] else 'STOPP', '| andel med data', round(res['andel_med_data'], 2))
    json.dump(res, open(os.path.join(OUT, 'T27_steg1.json'), 'w'), indent=1); sys.exit()
if STEP == 2:
    st = json.load(open(os.path.join(OUT, 'T27_steg1.json'))); out = []
    if not st['godkant']: print('T27 stoppad i steg 1'); sys.exit()
    for name, s in [('tillägg efter 2017 (primär)', prim), ('borttag efter 2017', S[(S.type == 'deletion') & (S.post == 1)]), ('tillägg före 2017', S[(S.type == 'addition') & (S.post == 0)])]:
        s = s.dropna(subset=['d_ana']); r = reg(s); out.append(dict(test=name, **r)); print(f"{name}: {r['b']:+.3f} ({r['lo']:+.3f} till {r['hi']:+.3f}), p {r['p']:.3f}, N {r['n']}, G {r['G']}")
    e = prim[prim.event == 1]; c = prim[prim.event == 0]
    print(f'beskrivande, tillägg efter 2017: prognoser före i median {e.n_fore.median():.1f} (kontroller {c.n_fore.median():.1f})')
    pd.DataFrame(out).to_csv(os.path.join(OUT, 'T27_resultat.csv'), index=False)
