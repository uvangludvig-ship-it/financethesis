# Runda 7: T22 hopptest mot urval, T23 asymmetri. Deklarerat i runda7_deklaration.md (2 nov 2026, 13:55 CET).
# Körs från code/claude_checks:
#   ROOT=../.. PANEL=data/panel_utdrag.csv.gz INDATA=code/claude_checks/data python3 runda7.py 1|2
# Steg 1: styrka för T22 (bara N, G, SE, MDE). Steg 2: skattningar.
import os, sys, json
STEP = int(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['OUT'] = os.path.join(HERE, 'runda7_resultat')
src = open(os.path.join(HERE, 'runda3.py')).read()
exec(src.split('# %%\nrng = np.random')[0])          # panel, kalender, överavkastning A, händelser ev (från runda 3)
OUT = os.environ['OUT']; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261102)
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
        Xr = np.delete(X, j, 1)
        fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0] if Xr.shape[1] else np.zeros_like(y); er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = (np.abs(np.concatenate(ts)[:B]) >= abs(b0 / s0)).mean()
    return dict(b=b0, se=s0, lo=b0 - qq * s0, hi=b0 + qq * s0, p=p, n=n, G=G)
def mde(r): return (tdist.ppf(.975, r['G'] - 1) + tdist.ppf(.80, r['G'] - 1)) * r['se']
fmt = lambda r: f"{r['b']:+.3f} ({r['lo']:+.3f} till {r['hi']:+.3f}), p {r['p']:.3f}, N {r['n']}, G {r['G']}"
def mean_test(s, y, boot=True):
    return wcr(np.ones((len(s), 1)), np.asarray(s[y], float), s.review_cycle.values, 0, boot=boot)

# ---------- T22: J per händelse
FL = pd.read_csv(P('output/omxsb_replication_2007/mechanisms/step1_deletion_flags.csv')); FLAGGED = set(FL[FL.flagged.astype(bool)].event_id)
E = ev[~ev.event_id.isin(FLAGGED)].dropna(subset=['iAD', 'iED']).copy()
rows, prof = [], []
for x in E.itertuples():
    if x.RIC not in CI: continue
    iA, iE = int(x.iAD), int(x.iED); lo, hi = iA - 20, iE + 20
    if lo < 0 or hi >= len(cal) or iE - 1 <= iA + 1: continue
    ar = A[lo:hi + 1, CI[x.RIC]]; days = np.arange(lo, hi + 1)
    H = np.isin(days, [iA, iA + 1, iE - 1]); O = ~H
    if np.isnan(ar[H]).any() or np.isfinite(ar[O]).mean() < 0.8: continue
    rows.append(dict(event_id=x.event_id, review_cycle=x.review_cycle, type=x.type, post=int(x.post), RIC=x.RIC, n_ovriga=int(np.isfinite(ar[O]).sum()),
                     H_medel=np.mean(ar[H]), O_medel=np.nanmean(ar[O]), J=np.mean(ar[H]) - np.nanmean(ar[O]),
                     J_AD=np.mean(ar[np.isin(days, [iA, iA + 1])]) - np.nanmean(ar[O]), J_ED=ar[days == iE - 1][0] - np.nanmean(ar[O])))
    for rel in range(-20, 6): prof.append(dict(type=x.type, post=int(x.post), ankare='AD', dag=rel, ar=A[iA + rel, CI[x.RIC]]))
    for rel in range(-5, 21): prof.append(dict(type=x.type, post=int(x.post), ankare='ED', dag=rel, ar=A[iE + rel, CI[x.RIC]]))
J = pd.DataFrame(rows); J.to_csv(os.path.join(OUT, 'T22_events.csv'), index=False)
prim = J[(J.type == 'addition') & (J.post == 1)]

if STEP == 1:
    r = mean_test(prim, 'J', boot=False)
    res = dict(n=int(r['n']), G=int(r['G']), se=float(r['se']), mde=float(mde(r)), villkor=0.5, godkant=bool(mde(r) <= 0.5))
    print(f"T22: N {r['n']}, G {r['G']}, SE {r['se']:.4f}, MDE {mde(r):.3f} (villkor ≤ 0,5) ->", 'GODKÄNT' if res['godkant'] else 'STOPP')
    json.dump(res, open(os.path.join(OUT, 'steg1.json'), 'w'), indent=1); sys.exit()

if STEP == 2:
    st1 = json.load(open(os.path.join(OUT, 'steg1.json'))); out = []
    if st1['godkant']:
        def add(name, s, y, typ):
            r = mean_test(s, y); out.append(dict(test=name, typ=typ, utfall=y, **r, mde=mde(r))); print(f'{name}:', fmt(r))
        add('T22 tillägg efter 2017', prim, 'J', 'primär')
        add('T22 borttag efter 2017', J[(J.type == 'deletion') & (J.post == 1)], 'J', 'sekundär')
        add('T22 tillägg före 2017', J[(J.type == 'addition') & (J.post == 0)], 'J', 'sekundär')
        for ty in ['addition', 'deletion']:
            for y in ['J_AD', 'J_ED']: add(f'T22 {ty} efter 2017, {y}', J[(J.type == ty) & (J.post == 1)], y, 'sekundär')
        d = J.groupby(['type', 'post'])[['H_medel', 'O_medel', 'J']].agg(['mean', 'count']).round(3); print(d.to_string())
        PR = pd.DataFrame(prof).groupby(['type', 'post', 'ankare', 'dag']).ar.agg(['mean', 'count']).reset_index()
        PR.to_csv(os.path.join(OUT, 'T22_profil.csv'), index=False)
    else:
        print('T22 stoppad i steg 1')

    # ---------- T23a: summan b_tillägg + b_borttag (explorativt)
    S5 = pd.read_csv(os.path.join(HERE, 'runda2_resultat', 'T5urval_T7_T8b_events.csv'))
    s = S5[S5.post == 1].copy(); Ea = ((s.type == 'addition') & (s.event == 1)).astype(float); Ed = ((s.type == 'deletion') & (s.event == 1)).astype(float)
    ad = (s.type == 'addition').astype(float)
    FE = pd.get_dummies(s.review + '_' + s.type).astype(float).values
    for w in ['car_ED+1', 'car_ED+20']:
        X = np.column_stack([Ea, Ed - Ea, s.ru * ad, s.ru * (1 - ad), s.lm * ad, s.lm * (1 - ad), FE])   # koefficient på Ea = b_tillägg + b_borttag
        r = wcr(X, s[w].values.astype(float), s.review.values, 0)
        out.append(dict(test=f'T23a summa tillägg + borttag, {w}', typ='explorativ', utfall=w, **r)); print(f'T23a {w}:', fmt(r))
    # ---------- T23b: fondägare utanför OMXSB-fonderna
    a = pd.read_csv(os.path.join(HERE, 'agar_kontroll', 'agar_omxsb_results.csv')).set_index('utfall').loc['n ej B']
    d_ = pd.read_csv(os.path.join(HERE, 'agar_kontroll', 'T21_results.csv')).set_index('utfall').loc['n ej B']
    b = a.b + d_.b; se = np.sqrt(a.se ** 2 + d_.se ** 2); dfm = min(a.G, d_.G) - 1; qq = tdist.ppf(.975, dfm)
    out.append(dict(test='T23b summa fondägare utanför OMXSB, tillägg + borttag', typ='explorativ', utfall='n ej B', b=b, se=se, lo=b - qq * se, hi=b + qq * se, p=2 * tdist.sf(abs(b / se), dfm), n=int(a.n + d_.n), G=int(dfm + 1)))
    print(f'T23b: {b:+.2f} ({b - qq * se:+.2f} till {b + qq * se:+.2f}), t-fördelning med {dfm} frihetsgrader')
    pd.DataFrame(out).to_csv(os.path.join(OUT, 'runda7_results.csv'), index=False)
