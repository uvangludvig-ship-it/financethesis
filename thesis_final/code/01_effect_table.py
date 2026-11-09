# Tabell 1 rättad: stjärnor och 95 % intervall från wild cluster bootstrap (intervallet genom testinversion, 9 nov), panel C (decennier, G&S kalenderår, sedan 2010),
# panel D (har effekten minskat), panel E (varje startår). CAR från returns.py, som återskapar replikeringens tot exakt.
# Ingen ny data, inga nya regler. Körs från thesis_final: python3 code/01_effect_table.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import os, sys, numpy as np, pandas as pd
from math import lgamma, exp, log
# t- och F-fördelning utan scipy (regulariserad ofullständig betafunktion, Lentz kedjebråk, Numerical Recipes 6.4)
def _betacf(a, b, x, itmax=300, eps=3e-14):
    qab, qap, qam = a + b, a + 1, a - 1; c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300); h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m; aa = m * (b - m) * x / ((qam + m2) * (a + m2)); d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300); c = 1 + aa / (c if abs(c) > 1e-300 else 1e-300); h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2)); d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300); c = 1 + aa / (c if abs(c) > 1e-300 else 1e-300); de = d * c; h *= de
        if abs(de - 1) < eps: break
    return h
def betainc(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * log(x) + b * log(1 - x))
    return bt * _betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * _betacf(b, a, 1 - x) / b
class tdist:
    @staticmethod
    def sf(t, df): return 0.5 * betainc(df / 2, 0.5, df / (df + t * t))
    @staticmethod
    def ppf(q, df):
        lo, hi = 0.0, 200.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if 1 - tdist.sf(mid, df) < q: lo = mid
            else: hi = mid
        return (lo + hi) / 2
class fdist:
    @staticmethod
    def sf(x, d1, d2): return betainc(d2 / 2, d1 / 2, d2 / (d2 + d1 * x))
exec(open(Path(__file__).resolve().parent / 'returns.py', encoding='utf-8').read())
OUT = RES / 'effect'; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261103)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, Gn): return rng.choice([-1., 1.], (B, Gn)) if Gn >= 12 else rng.choice(WEBB, (B, Gn))
def lin(X, y, g, c, B=9999):
    # Skattning c'b, klustrat SE (CR1) och restriktiv wild cluster bootstrap (WCR) med samma 9 999 dragningar för p-värdet och
    # intervallet. Intervallet = alla värden th där WCR-testet av H0: c'b = th inte förkastar på 5 % (testinversion, som boottest).
    X = np.asarray(X, float); y = np.asarray(y, float); c = np.asarray(c, float)
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    codes = pd.factorize(np.asarray(g)[ok])[0]; Gn = codes.max() + 1; n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X); Am = XtXi @ X.T; q = X @ (XtXi @ c); adj = Gn / (Gn - 1) * (n - 1) / max(n - k, 1)
    Hq = np.zeros((n, Gn)); Hq[np.arange(n), codes] = q   # summerar residual*q per kluster
    def tse(Y):
        Bm = Y @ Am.T; Ee = Y - Bm @ X.T; sg = Ee @ Hq; return Bm @ c, np.sqrt((sg ** 2).sum(1) * adj)
    t0, s0 = tse(y[None, :]); t0, s0 = t0[0], s0[0]; qq = tdist.ppf(.975, Gn - 1)
    Wc = np.concatenate([wdraw(1000, Gn) for _ in range(B // 1000 + 1)])[:B][:, codes]
    v = XtXi @ c / (c @ XtXi @ c)   # förskjutning så att c'b(y - th*Xv) = c'b - th; residualerna och SE är oförändrade
    def pw(th):
        ys = y - th * (X @ v); b = Am @ ys; br = b - XtXi @ c * (c @ b) / (c @ XtXi @ c); fr = X @ br; er = ys - fr
        bs, ss = tse(fr[None, :] + er[None, :] * Wc); return float((np.abs(bs / ss) >= abs((t0 - th) / s0)).mean())
    def kant(sgn):
        inne, ute = t0, t0 + sgn * qq * s0
        while pw(ute) > .05:   # obegränsat om testet inte förkastar inom 20 standardfel (få kluster bakom kontrasten)
            if abs(ute - t0) >= 20 * s0 * (1 - 1e-9): return sgn * np.inf
            ute = t0 + sgn * min(2 * abs(ute - t0), 20 * s0)
        while abs(ute - inne) > 1e-4 * max(s0, 1e-12):
            m = (inne + ute) / 2
            if pw(m) > .05: inne = m
            else: ute = m
        return (inne + ute) / 2
    p = pw(0.0)
    e = y - X @ (Am @ y); se_hc1 = float(np.sqrt((XtXi @ (X.T * (e ** 2)) @ X @ XtXi)[np.ix_(c != 0, c != 0)].sum() * n / (n - k))) if (c != 0).sum() == 1 else np.nan
    return dict(b=float(t0), se=float(s0), lo=kant(-1), hi=kant(1), lo_cr1=float(t0 - qq * s0), hi_cr1=float(t0 + qq * s0),
                p_cr1=float(2 * tdist.sf(abs(t0 / s0), Gn - 1)), p_wcb=p, se_hc1=se_hc1, n=int(n), G=int(Gn),
                vikter='Rademacher' if Gn >= 12 else 'Webb', ci_metod=CI_METOD, p_metod=P_METOD)
CI_METOD = '95 % intervall: invertering av restriktiv wild cluster bootstrap per översyn (9 999 dragningar)'
P_METOD = 'p och stjärnor: restriktiv wild cluster bootstrap per översyn (Rademacher om G>=12, annars Webb; 9 999 dragningar)'
def stars(p): return '***' if p < .01 else '**' if p < .05 else '*' if p < .10 else ''
def cell(r): return f"{r['b']:.2f}{stars(r['p_wcb'])} ({r['lo']:.2f} till {r['hi']:.2f})"
ev['ann'] = [wsum(r, a - 1, a + 1) for r, a in zip(ev.RIC, ev.iAD)]
ev['eff'] = [wsum(r, e - 1, e + 1) for r, e in zip(ev.RIC, ev.iED)]
ev['tot'] = [wsum(r, a - 1, e + 1) for r, a, e in zip(ev.RIC, ev.iAD, ev.iED)]
ev['effective_date'] = pd.to_datetime(ev.effective_date); ev['ar'] = ev.effective_date.dt.year
PERS = ['2007–2011', '2012–2016', '2017–2021', '2022–2026']; WIN = {'ann': 'Besked [AD−1, AD+1]', 'eff': 'Ändring [ED−1, ED+1]', 'tot': 'Totalt [AD−1, ED+1]'}
rows = []
def medel(d, y, lab, panel, ty, win):
    d = d[d[y].notna()]
    if len(d) < 3: return
    r = lin(np.ones((len(d), 1)), d[y].values, d.review_cycle.values, [1.]); rows.append(dict(panel=panel, typ=ty, fönster=win, urval=lab, **r))
for ty in ['addition', 'deletion']:
    s = ev[ev.type == ty]
    for w in WIN:
        for p in PERS: medel(s[s.period == p], w, p, 'A/B', ty, w)
    for lab, q in [('2007–16', s.ar <= 2016), ('2017–26', s.ar >= 2017), ('2010–20 (G&S kalenderår)', (s.ar >= 2010) & (s.ar <= 2020)), ('2011–20', (s.ar >= 2011) & (s.ar <= 2020)),
                   ('efter brottet juni 2010', s.effective_date > '2010-06-01'), ('2007 till juni 2010', s.effective_date <= '2010-06-01')]:
        medel(s[q], 'tot', lab, 'C', ty, 'tot')
    if ty == 'addition':
        for y0 in range(2008, 2024): medel(s[s.ar >= y0], 'tot', f'från {y0}', 'E', ty, 'tot')
    # panel D: har effekten minskat (totalt fönster)
    d = s[s.tot.notna()]
    X = np.column_stack([(d.period == p).astype(float).values for p in PERS]); y = d.tot.values; g = d.review_cycle.values
    r = lin(X, y, g, [-1, 0, 0, 1]); rows.append(dict(panel='D', typ=ty, fönster='tot', urval='2022–26 minus 2007–11', **r))
    r = lin(X, y, g, [0, 0, -1, 1]); rows.append(dict(panel='D', typ=ty, fönster='tot', urval='2022–26 minus 2017–21', **r))
    Xd = np.column_stack([np.ones(len(d)), (d.ar >= 2017).astype(float).values]); r = lin(Xd, y, g, [0, 1]); rows.append(dict(panel='D', typ=ty, fönster='tot', urval='2017–26 minus 2007–16 (decennier)', **r))
    Xt = np.column_stack([np.ones(len(d)), (d.ar - 2007).values.astype(float)]); r = lin(Xt, y, g, [0, 1]); rows.append(dict(panel='D', typ=ty, fönster='tot', urval='trend per år (ingen periodindelning)', **r))
    Xb = np.column_stack([np.ones(len(d)), (d.effective_date > '2010-06-01').astype(float).values]); r = lin(Xb, y, g, [0, 1]); rows.append(dict(panel='D', typ=ty, fönster='tot', urval='efter minus före brottet juni 2010 (brottet från Luddes T4, inte sökt här)', **r))
    # F-test lika medel: Wald med CR1, p från F(3, G-1)
    codes = pd.factorize(g)[0]; G = codes.max() + 1; XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; e = y - X @ b
    S = sum(np.outer(X[codes == k].T @ e[codes == k], X[codes == k].T @ e[codes == k]) for k in range(G)); V = XtXi @ S @ XtXi * G / (G - 1) * (len(y) - 1) / (len(y) - 4)
    Rm = np.array([[1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, -1]], float); W = (Rm @ b) @ np.linalg.inv(Rm @ V @ Rm.T) @ (Rm @ b) / 3
    rows.append(dict(panel='D', typ=ty, fönster='tot', urval='F-test lika medel i fyra perioder', b=float(W), p_cr1=float(fdist.sf(W, 3, G - 1)), n=len(y), G=int(G), ci_metod='inget intervall (F-test)', p_metod='analytiskt: Wald med CR1, p från F(3, G-1), ingen bootstrap'))
T = pd.DataFrame(rows); T.to_csv(f'{OUT}/tabell1_lang.csv', index=False)
# läsbara tabeller
with open(f'{OUT}/TABELL1.md', 'w') as f:
    f.write('# Tabell 1, rättad: intervall och stjärnor från wild cluster bootstrap per översyn\n\nCAR i procent mot OMXSBGI, totalavkastning. **BOOTSTRAP:** 95 % intervall i parentes = alla värden som restriktiv wild cluster bootstrap per översyn inte förkastar på 5 % (testinversion). Stjärnor: * p<0,10, ** p<0,05, *** p<0,01 från samma bootstrap och samma dragningar (Rademacher om G≥12, annars Webb; 9 999 dragningar), så intervall och stjärnor stämmer alltid överens. **ANALYTISKT (jämförelse):** raderna märkta klustrat = CR1-standardfel per översyn, t med G−1. Källa: 01_effect_table.py, CAR från returns.py som återskapar replikeringens tot exakt.\n\n')
    for ty, nm in [('addition', 'Panel A: Tillägg'), ('deletion', 'Panel B: Borttag')]:
        f.write(f'## {nm}\n\n| Fönster | ' + ' | '.join(PERS) + ' |\n|---|---|---|---|---|\n')
        for w, wl in WIN.items():
            f.write(f'| {wl} | ' + ' | '.join(cell(T[(T.panel == 'A/B') & (T.typ == ty) & (T.fönster == w) & (T.urval == p)].iloc[0]) for p in PERS) + ' |\n')
        a = T[(T.panel == 'A/B') & (T.typ == ty) & (T.fönster == 'tot')].set_index('urval')
        f.write('| Händelser | ' + ' | '.join(str(a.loc[p, 'n']) for p in PERS) + ' |\n| Översyner | ' + ' | '.join(str(a.loc[p, 'G']) for p in PERS) + ' |\n')
        f.write('| Intervall totalt, klustrat (analytiskt) | ' + ' | '.join(f"{a.loc[p, 'lo_cr1']:.2f} till {a.loc[p, 'hi_cr1']:.2f}" for p in PERS) + ' |\n')
        f.write('| p totalt, klustrat (analytiskt) | ' + ' | '.join(f"{a.loc[p, 'p_cr1']:.3f}" for p in PERS) + ' |\n| p totalt, wild bootstrap | ' + ' | '.join(f"{a.loc[p, 'p_wcb']:.3f}" for p in PERS) + ' |\n\n')
    f.write('## Panel C: sammanslagna perioder, totalt fönster\n\n| Typ | Urval | Händelser | Översyner | Effekt (bootstrapintervall) | Intervall, klustrat (analytiskt) | p, wild bootstrap |\n|---|---|---|---|---|---|---|\n')
    for r in T[T.panel == 'C'].itertuples(): f.write(f'| {r.typ} | {r.urval} | {r.n} | {r.G} | {cell(r._asdict())} | {r.lo_cr1:.2f} till {r.hi_cr1:.2f} | {r.p_wcb:.3f} |\n')
    f.write('\nG&S, USA: tillägg 1990-talet 7,4 %; tillägg 2010-talet under 1 %, inte skild från noll; borttag 2010–2020 −0,6 %.\n\n')
    f.write('## Panel D: har effekten minskat? Totalt fönster\n\n| Typ | Test | Skattning | Intervall, bootstrap | Intervall, klustrat (analytiskt) | p, klustrat (analytiskt) | p, wild bootstrap | Översyner |\n|---|---|---|---|---|---|---|---|\n')
    for r in T[T.panel == 'D'].itertuples():
        iv = '' if pd.isna(r.lo) else f'{r.lo:.2f} till {r.hi:.2f}'; ia = '' if pd.isna(r.lo_cr1) else f'{r.lo_cr1:.2f} till {r.hi_cr1:.2f}'; pw = '' if pd.isna(r.p_wcb) else f'{r.p_wcb:.3f}'
        f.write(f'| {r.typ} | {r.urval} | {r.b:.2f} | {iv} | {ia} | {r.p_cr1:.3f} | {pw} | {r.G} |\n')
    f.write('\n## Panel E: tillägg från varje startår till 2026, totalt fönster\n\n| Från | Händelser | Översyner | Effekt (bootstrapintervall) | p, wild bootstrap |\n|---|---|---|---|---|\n')
    for r in T[T.panel == 'E'].itertuples(): f.write(f'| {r.urval} | {r.n} | {r.G} | {cell(r._asdict())} | {r.p_wcb:.3f} |\n')
    f.write('\nF-testet i panel D (lika medel i fyra perioder) är analytiskt: Wald med CR1, p från F(3, G−1), ingen bootstrap.\n')
print('Metod: ' + CI_METOD); print('Metod: ' + P_METOD); print('Metod: analytiska jämförelseintervall (lo_cr1, hi_cr1, p_cr1) = CR1 per översyn, t med G-1; F-testet i panel D är analytiskt')
print(open(f'{OUT}/TABELL1.md').read())
