# Snabbkontroll 9 nov (INTE deklarerad i förväg): M för tillägg och borttag 2019–26 med FI:s bredare D (netto_OMXSB_ny) mot runda 13:s D_V.
# Körs från thesis_final efter 02: python3 code/03_fund_demand_fi_check.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import os, pandas as pd, numpy as np
E = pd.read_csv(RES / 'fund_demand' / 'handelser_omraknade.csv')
fi = pd.read_csv(DATA / 'funds' / 'fund_net_buying_fi_by_event_2019_2026.csv'); fi = fi[fi.status == 'ok']
m = fi.merge(E[['event_id', 'RIC', 'review', 'type', 'split', 'y_tot', 'D_V']], on=['RIC', 'review'], suffixes=('_fi', ''))
rng = np.random.default_rng(1)
def ratio(d, dc, B=4999):
    rv = d.review.values; u = np.unique(rv); idx = {k: np.where(rv == k)[0] for k in u}; ks = []
    for b in range(B):
        ii = np.concatenate([idx[k] for k in rng.choice(u, len(u))]); dm = d[dc].values[ii].mean(); cm = d.y_tot.values[ii].mean()
        ks.append(cm / dm if dm > 0 else (np.inf if cm >= 0 else -np.inf))   # som 02 och 05: dragningen behålls
    ks = np.array(ks); return d.y_tot.mean() / d[dc].mean(), np.quantile(ks, .025), np.quantile(ks, .975)
rows = []
for ty in ['addition', 'deletion']:
    for split_ok in [False, True]:
        d = m[(m['type'] == ty) & m.y_tot.notna() & m.netto_OMXSB_ny.notna()]
        if not split_ok: d = d[~d.split.astype(bool)].dropna(subset=['D_V'])
        r = ratio(d, 'netto_OMXSB_ny'); row = dict(typ=ty, splittade=split_ok, n=len(d), G=d.review.nunique(), car=d.y_tot.mean(), D_FI=d.netto_OMXSB_ny.mean(), M_FI=r[0], lo_FI=r[1], hi_FI=r[2])
        if not split_ok:
            v = ratio(d, 'D_V'); row.update(D_V=d.D_V.mean(), M_V=v[0], lo_V=v[1], hi_V=v[2])
        rows.append(row)
METOD = '95 % intervall för M (lo_FI/hi_FI, lo_V/hi_V): parvis klusterbootstrap per översyn, percentil, 4 999 dragningar'
for r_ in rows: r_['ci_metod'] = METOD
print('Metod: ' + METOD)
R = pd.DataFrame(rows); os.makedirs(RES / 'fi_check', exist_ok=True); R.to_csv(RES / 'fi_check' / 'fi_m_kontroll.csv', index=False); print(R.drop(columns=['ci_metod']).round(2).to_string(index=False))
