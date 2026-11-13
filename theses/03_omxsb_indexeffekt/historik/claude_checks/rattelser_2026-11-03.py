# Rättelser 3 november (plan: rattelser_2026-11-03_plan.md, skriven 15:21:30). Explorativt.
# D saknas (inte 0) när ingen OMXSB-indexfond rapporterar runt händelsen; M räknas om; intervall som tar med alla dragningar;
# kontroll med förväntat D från SHoF. Körs från code/claude_checks: python3 rattelser_2026-11-03.py
import os, sys, types
import numpy as np, pandas as pd
from scipy.stats import t as tdist
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'rattelser_2026-11-03_resultat'); os.makedirs(OUT, exist_ok=True)
PERS = ['2007–11', '2012–16', '2017–21', '2022–26']
E = pd.read_csv(os.path.join(HERE, 'runda11_resultat', 'handelser.csv'), parse_dates=['AD', 'ED'])
E['split'] = E.split.astype(bool)
# ---------- OMXSB-indexfonder som rapporterar runt händelsen (regeln och klassningen från runda 9)
ns = {'__file__': os.path.join(HERE, 'runda9.py')}; os.environ.setdefault('DATA', os.path.join(HERE, 'data'))
argv0 = sys.argv[:]; sys.argv = ['runda9.py', '9']
exec(open(os.path.join(HERE, 'runda9.py')).read().split('NT = netto(F)')[0], ns); sys.argv = argv0
F9 = ns['F']; rapporterar = ns['rapporterar']; grupp = ns['grupp']
kand = F9[F9.grupp == 'OMXSB-index'].groupby('fond').ftyp.first().to_dict()
def n_rapporterande(AD, ED):
    n = 0
    for f, ft in kand.items():
        if grupp(types.SimpleNamespace(fond=f, rapport=AD, ftyp=ft)) != 'OMXSB-index': continue
        if rapporterar(f, AD - pd.Timedelta(days=120), AD - pd.Timedelta(days=1)) and rapporterar(f, ED, ED + pd.Timedelta(days=45)): n += 1
    return n
E['n_indexfonder'] = [n_rapporterande(a, e) for a, e in zip(E.AD, E.ED)]
E['D_ny'] = np.where(E.n_indexfonder > 0, E.D, np.nan)
# ---------- förväntat D från SHoF (fri flytande andel × fondernas ägarandel av indexet)
G = pd.read_csv(os.path.join(HERE, 'runda11_resultat', 'G_figur1_figur5.csv')).set_index('ar').agarandel_pct
FFH = pd.read_csv(os.path.join(HERE, 'data', 'lseg_freefloat_hist.csv')); ffh = {(r.review, r.ric): r.ff for r in FFH.dropna(subset=['ff']).itertuples()}
K = pd.read_csv(os.path.join(HERE, 'data', 'lseg_klassificering.csv')); FFC = dict(zip(K.ric, pd.to_numeric(K.freefloat, errors='coerce')))
def ff(rv, c):
    v = ffh.get((rv, c), FFC.get(c, np.nan)); return v if pd.notna(v) and 0 < v <= 100 else 100.0
E['D_shof'] = [ff(rv, c) / 100 * G.get(a, np.nan) for rv, c, a in zip(E.review, E.RIC, E.ar)]
E.to_csv(os.path.join(OUT, 'handelser_rattade.csv'), index=False)

# ---------- inferens (samma som runda 11)
rng = np.random.default_rng(20261103)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, Gn): return rng.choice([-1., 1.], (B, Gn)) if Gn >= 12 else rng.choice(WEBB, (B, Gn))
def lin(X, y, g, c, B=9999, boot=True):
    X = np.asarray(X, float); y = np.asarray(y, float); c = np.asarray(c, float)
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    codes = pd.factorize(np.asarray(g)[ok])[0]; Gn = codes.max() + 1; n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X); Am = XtXi @ X.T; q = X @ (XtXi @ c); adj = Gn / (Gn - 1) * (n - 1) / max(n - k, 1)
    def tse(Y):
        Bm = Y @ Am.T; Ee = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=Gn) for row in Ee * q]); return Bm @ c, np.sqrt((sg ** 2).sum(1) * adj)
    t0, s0 = tse(y[None, :]); t0, s0 = t0[0], s0[0]; qq = tdist.ppf(.975, Gn - 1); p = np.nan
    if boot:
        b = Am @ y; br = b - XtXi @ c * (c @ b) / (c @ XtXi @ c); fr = X @ br; er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, Gn); bs, ss = tse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = float((np.abs(np.concatenate(ts)[:B]) >= abs(t0 / s0)).mean())
    return dict(b=float(t0), se=float(s0), lo=float(t0 - qq * s0), hi=float(t0 + qq * s0), p=p, n=int(n), G=int(Gn))
KC = ['k_oms', 'k_storlek', 'k_wz', 'k_ana']
def kvot_ci(d, yc, dc, B=9999):   # alla dragningar med; medel-D <= 0 ger M = ±oändligt
    rv = d.review.values; u = np.unique(rv); idx = {k: np.where(rv == k)[0] for k in u}; ks = np.empty(B)
    for b in range(B):
        ii = np.concatenate([idx[k] for k in rng.choice(u, len(u))]); dm = d[dc].values[ii].mean(); cm = d[yc].values[ii].mean()
        ks[b] = cm / dm if dm > 0 else (np.inf if cm >= 0 else -np.inf)
    return np.quantile(ks, .025), np.quantile(ks, .975), float(np.mean(~np.isfinite(ks)))
rows = []
for ty in ['addition', 'deletion']:
    for dc, lab, prim in [('D_ny', 'LSEG, rättat D', True), ('D', 'LSEG, som runda 11', True), ('D_shof', 'förväntat D (SHoF)', False)]:
        s0 = E[E.type == ty]
        s0 = s0[~s0.split & s0[dc].notna()] if prim else s0[s0[dc].notna()]
        for yc in ['y_tot', 'y_lang']:
            for p_ in PERS:
                d = s0[(s0.per == p_) & s0[yc].notna()]
                if len(d) < 3: rows.append(dict(typ=ty, mått=lab, fönster=yc, period=p_, n=len(d))); continue
                lo, hi, andel_inf = kvot_ci(d, yc, dc)
                rows.append(dict(typ=ty, mått=lab, fönster=yc, period=p_, n=len(d), G=d.review.nunique(), car=d[yc].mean(), D=d[dc].mean(),
                                 M=d[yc].mean() / d[dc].mean() if d[dc].mean() > 0 else np.nan, lo=lo, hi=hi, andel_oandliga=andel_inf,
                                 D_noll=int((d[dc] == 0).sum())))
T5 = pd.DataFrame(rows); T5.to_csv(os.path.join(OUT, 'M_per_period.csv'), index=False)
# tabell 6 med rättat D, H11a och H11b igen
r6 = []
for ty in ['addition', 'deletion']:
    for yc in ['y_tot', 'y_lang']:
        for kontroller in [False, True]:
            s = E[(E.type == ty) & ~E.split & E.D_ny.notna() & E[yc].notna()].copy()
            if kontroller:
                s = s.dropna(subset=KC)
                for c in KC: s[c] = s[c] - s[c].mean()
            Db = s.groupby('per').D_ny.mean().reindex(PERS)
            X = np.column_stack([((s.per == p_).astype(float) * Db[p_]).values for p_ in PERS] + ([s[c].values for c in KC] if kontroller else []))
            for j, p_ in enumerate(PERS):
                c = np.zeros(X.shape[1]); c[j] = 1; r = lin(X, s[yc].values, s.review.values, c, boot=False)
                r6.append(dict(typ=ty, fönster=yc, kontroller=kontroller, del_=f'M {p_}', n_period=int((s.per == p_).sum()), D_medel=Db[p_], **r))
            for a_, b_, lab in [(0, 3, 'M 2007–11 − M 2022–26'), (2, 3, 'M 2017–21 − M 2022–26')]:
                c = np.zeros(X.shape[1]); c[a_], c[b_] = 1, -1; r = lin(X, s[yc].values, s.review.values, c); r6.append(dict(typ=ty, fönster=yc, kontroller=kontroller, del_=lab, **r))
T6 = pd.DataFrame(r6); T6.to_csv(os.path.join(OUT, 'tabell6_rattad.csv'), index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
print('tillägg utan split där ingen OMXSB-indexfond rapporterar (D blir saknat):', E[(E.type == 'addition') & ~E.split & E.D.notna() & (E.n_indexfonder == 0)].groupby('per').size().to_dict())
print('borttag utan split där ingen OMXSB-indexfond rapporterar:', E[(E.type == 'deletion') & ~E.split & E.D.notna() & (E.n_indexfonder == 0)].groupby('per').size().to_dict())
print(T5.round(3).to_string(index=False)); print(T6.round(3).to_string(index=False))
