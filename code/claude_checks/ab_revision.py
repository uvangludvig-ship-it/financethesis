# A/B-revision enligt ab_deklaration.md
from twin_core import *
rng = np.random.default_rng(20261101)
fin = pd.read_csv('twin_results_events.csv', parse_dates=['AD', 'ED'])
LSEG_SIS = {'NCCa.ST', 'SWECa.ST', 'BONAVa.ST', 'RATOa.ST'}
TRp = {}
def series(ix_, sis):
    if sis in LSEG_SIS or ix_ in LSEG_SIS or not (ix_ in TR and sis in TR): return PRICE[ix_], PRICE[sis], 'pris'
    return TR[ix_], TR[sis], 'tr'
def flags(ix_, sis):
    key = (ix_, sis)
    if key not in TRp:
        A_, B_, src = series(ix_, sis)
        r = np.log(A_ / B_).diff().values
        nxt = np.r_[r[1:], np.nan]
        big = np.abs(r) > 0.08
        spike = big & (np.abs(r + nxt) < 0.25 * np.abs(r))
        jump = (np.abs(r) > 0.15) & (np.abs(r + nxt) > 0.75 * np.abs(r))
        TRp[key] = (A_, B_, src, spike, jump)
    return TRp[key]
def spread_c(ix_, sis, a, b):
    A_, B_, src, spike, jump = flags(ix_, sis)
    if a - 1 < 0 or b >= len(cal): return np.nan, 'utanför'
    if spike[a - 1] or spike[b]: return np.nan, 'R2'
    if jump[a:b + 1].any(): return np.nan, 'R3'
    x = np.log(A_.iloc[b] / A_.iloc[a - 1]) - np.log(B_.iloc[b] / B_.iloc[a - 1])
    return (100 * x, 'ok') if np.isfinite(x) else (np.nan, 'saknas')
def stale_share(sis, a, b):
    p = CLOSE[sis].iloc[max(a, 0):b + 1].dropna() if sis in CLOSE else pd.Series(dtype=float)
    return float((p.diff().iloc[1:] == 0).mean()) if len(p) > 5 else np.nan
allev = t.copy(); doy = np.array(cal.dayofyear)
def starts(e, L):
    firm_ev = allev[allev.firm == e.firm][['iAD', 'iED']].values; ad = e.AD.dayofyear; out = []
    for s in range(61, len(cal) - L - 21):
        if cal[s].year == e.AD.year: continue
        dd = abs(doy[s] - ad); dd = min(dd, 365 - dd)
        if dd > 45: continue
        if any((s + L + 20 >= ia - 60) and (s - 60 <= ie + 20) for ia, ie in firm_ev): continue
        out.append(s)
    return out
rows = []; pools = {}
for _, e in fin.iterrows():
    a, b = int(e.iAD) - 1, int(e.iED) + 1
    st = stale_share(e.sister_ric, int(e.iAD) - 60, int(e.iED) + 20)
    v, why = spread_c(e.event_key, e.sister_ric, a, b)
    if st > 0.5: why = 'R4'; v = np.nan
    src = flags(e.event_key, e.sister_ric)[2]
    L = b - a + 1; pl = []
    for s in starts(e, L):
        x, w = spread_c(e.event_key, e.sister_ric, s, s + L - 1)
        if np.isfinite(x): pl.append(e.sign * x)
    pools[e.event_id] = np.array(pl)
    rows.append(dict(event_id=e.event_id, firm=e.firm, type=e.type, källa=src, stillastående=round(st, 2), status=why,
                     spread=e.sign * v if np.isfinite(v) else np.nan, spread_tidigare=e['primär [AD-1,ED+1]'], n_placebo=len(pl)))
D = pd.DataFrame(rows)
print('status per händelse:'); print(D.status.value_counts().to_string())
print(D[D.status != 'ok'][['event_id', 'firm', 'type', 'källa', 'stillastående', 'status', 'spread_tidigare']].to_string(index=False))
ok = D[(D.status == 'ok') & (D.n_placebo >= 20)]
def infer(sub):
    m = sub.spread.mean(); fr = sub.firm.values
    nm = np.array([np.mean([rng.choice(pools[k]) for k in sub.event_id]) for _ in range(5000)])
    c = nm - nm.mean(); p = (np.abs(c) >= abs(m - nm.mean())).mean()
    lo, hi = m - np.percentile(c, 97.5), m - np.percentile(c, 2.5)
    mf = pd.Series(sub.spread.values, index=fr).groupby(level=0).mean().mean()
    return m, lo, hi, p, len(sub), len(set(fr)), mf
res = []
for lab, sub in [('alla rensade', ok), ('tillägg', ok[ok.type == 'addition']), ('borttag', ok[ok.type == 'deletion']),
                 ('utan källbyte (bara panelens totalavkastning)', ok[ok.källa == 'tr'])]:
    if len(sub) >= 3:
        m, lo, hi, p, n, g, mf = infer(sub)
        res.append(dict(urval=lab, N=n, bolag=g, skattning=round(m, 2), ci_lo=round(lo, 2), ci_hi=round(hi, 2), p=round(p, 4), medel_per_bolag=round(mf, 2)))
R = pd.DataFrame(res); print(); print(R.to_string(index=False))
D.to_csv('ab_revision_events.csv', index=False); R.to_csv('ab_revision_results.csv', index=False)
print('\nsamma 39 med gamla serier, som jämförelse: %.2f' % fin['primär [AD-1,ED+1]'].mean())
