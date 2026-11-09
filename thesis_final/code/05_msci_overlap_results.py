# Runda 14, steg 2: CAR och M med och utan MSCI-överlapp. Inferens som tabell1 (klustring per översyn, wild bootstrap 9 999, intervall genom testinversion)
# och runda 13 (kvotbootstrap per översyn, 9 999). Kräver att 02 körts (results/fund_demand/handelser_omraknade.csv).
# Körs från thesis_final efter 02 och 04: python3 code/05_msci_overlap_results.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import os, pandas as pd, numpy as np
from scipy.stats import t as tdist
HERE = RES / 'msci_overlap'
ev = pd.read_csv(DATA / 'events' / 'omxsb_changes_with_car_2007_2026.csv', parse_dates=['AD', 'ED'])
OV = set(pd.read_csv(os.path.join(HERE, 'overlapp_handelser.csv')).event_id)
ev['ovl'] = ev.event_id.isin(OV); ev['ar'] = ev.ED.dt.year
ev['per'] = pd.cut(ev.ar, [2006, 2011, 2016, 2021, 2026], labels=['2007–11', '2012–16', '2017–21', '2022–26']).astype(str)
rng = np.random.default_rng(20261109)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
CI_METOD = '95 % intervall: invertering av restriktiv wild cluster bootstrap per översyn (9 999 dragningar)'
P_METOD = 'p: restriktiv wild cluster bootstrap per översyn (Rademacher om G>=12, annars Webb; 9 999 dragningar)'
M_METOD = '95 % intervall för M: parvis klusterbootstrap (översyner dras med återläggning), percentil, 9 999 dragningar'
def medel(y, g, B=9999):
    # Medel, klustrat SE (CR1) och restriktiv wild cluster bootstrap. Samma dragningar ger p (H0: medel = 0) och intervallet
    # (alla th som H0: medel = th inte förkastar på 5 %). mde bygger på det analytiska SE.
    y = np.asarray(y, float); ok = np.isfinite(y); y = y[ok]; codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n = len(y)
    H = np.zeros((n, G)); H[np.arange(n), codes] = 1.0 / n
    def tse(Y):
        b = Y.mean(1); e = Y - b[:, None]; s = e @ H
        return b, np.sqrt((s ** 2).sum(1) * G / (G - 1))
    b0, s0 = tse(y[None, :]); b0, s0 = b0[0], s0[0]
    Wc = np.concatenate([rng.choice([-1., 1.], (1000, G)) if G >= 12 else rng.choice(WEBB, (1000, G)) for _ in range(B // 1000 + 1)])[:B][:, codes]
    def pw(th):
        bs, ss = tse((y - th)[None, :] * Wc); return float((np.abs(bs / ss) >= abs((b0 - th) / s0)).mean())
    q = tdist.ppf(.975, G - 1)
    def kant(sgn):
        inne, ute = b0, b0 + sgn * q * s0
        while pw(ute) > .05:   # obegränsat om testet inte förkastar inom 20 standardfel (få kluster bakom kontrasten)
            if abs(ute - b0) >= 20 * s0 * (1 - 1e-9): return sgn * np.inf
            ute = b0 + sgn * min(2 * abs(ute - b0), 20 * s0)
        while abs(ute - inne) > 1e-4 * s0:
            m = (inne + ute) / 2
            if pw(m) > .05: inne = m
            else: ute = m
        return (inne + ute) / 2
    return dict(b=b0, lo=kant(-1), hi=kant(1), lo_cr1=b0 - q * s0, hi_cr1=b0 + q * s0, p=pw(0.0), n=n, G=G, mde=(q + tdist.ppf(.80, G - 1)) * s0,
                ci_metod=CI_METOD, p_metod=P_METOD, mde_metod='analytiskt: (t_0,975 + t_0,80) * CR1-SE, G-1 frihetsgrader')
rows = []
for ty in ['addition', 'deletion']:
    s = ev[(ev.type == ty) & ev.tot.notna()]
    for lab, sub in [(p, s[s.per == p]) for p in ['2007–11', '2012–16', '2017–21', '2022–26']] + [('2017–26', s[s.ar >= 2017])]:
        n_ov = int(sub.ovl.sum())
        rows.append(dict(typ=ty, urval=lab, variant='alla', n_overlapp=n_ov, **medel(sub.tot, sub.review_cycle)))
        ex = sub[~sub.ovl]; rows.append(dict(typ=ty, urval=lab, variant='utan överlapp', n_overlapp=n_ov, **medel(ex.tot, ex.review_cycle)))
        if n_ov: rows.append(dict(typ=ty, urval=lab, variant='bara överlapp (beskrivande)', n_overlapp=n_ov, b=sub[sub.ovl].tot.mean(), n=n_ov, ci_metod='beskrivande medel, ingen inferens'))
T = pd.DataFrame(rows)
H = pd.read_csv(RES / 'fund_demand' / 'handelser_omraknade.csv'); H['ovl'] = H.event_id.isin(OV)
def kvot(d, B=9999):
    rv = d.review.values; u = np.unique(rv); idx = {k: np.where(rv == k)[0] for k in u}; ks = np.empty(B)
    for b in range(B):
        ii = np.concatenate([idx[k] for k in rng.choice(u, len(u))]); dm = d.D_V.values[ii].mean(); cm = d.y_tot.values[ii].mean()
        ks[b] = cm / dm if dm > 0 else (np.inf if cm >= 0 else -np.inf)
    return d.y_tot.mean() / d.D_V.mean(), np.quantile(ks, .025), np.quantile(ks, .975)
mr = []
for ty in ['addition', 'deletion']:
    s0 = H[(H.type == ty) & ~H.split.astype(bool) & H.D_V.notna() & H.y_tot.notna()]
    for lab, sub in [('2017–21', s0[s0.per == '2017–21']), ('2022–26', s0[s0.per == '2022–26']), ('2017–26', s0[s0.ar >= 2017])]:
        for var, d in [('alla', sub), ('utan överlapp', sub[~sub.ovl])]:
            if ty == 'deletion' and var != 'alla' and lab != '2017–26': continue
            m, lo, hi = kvot(d)
            mr.append(dict(typ=ty, urval=lab, variant=var, n=len(d), n_overlapp=int(sub.ovl.sum()), car=d.y_tot.mean(), D_V=d.D_V.mean(), M=m, lo=lo, hi=hi, ci_metod=M_METOD))
MR = pd.DataFrame(mr)
T.to_csv(os.path.join(HERE, 'resultat_car.csv'), index=False); MR.to_csv(os.path.join(HERE, 'resultat_m.csv'), index=False)
pd.set_option('display.width', 250)
print('Metod CAR: ' + CI_METOD + '; ' + P_METOD + '. lo_cr1/hi_cr1 = analytiskt CR1-intervall (jämförelse); mde analytiskt.')
print(T.drop(columns=['ci_metod', 'p_metod', 'mde_metod']).round(2).to_string(index=False))
print('Metod M: ' + M_METOD + '.')
print(MR.drop(columns=['ci_metod']).round(2).to_string(index=False))
