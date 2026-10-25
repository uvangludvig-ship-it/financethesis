"""
2019 PPM purge as a replication sample: exits, renumberings, sibling/merger defaults,
voluntary-vs-default decomposition, destination (AP7 vs other), side-by-side with FTN.
Descriptives only.
"""
import pandas as pd, numpy as np, re, json
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 600); pd.set_option('display.max_columns', 50)
S = '/tmp/claude-0/-home-claude/5b447583-b5ae-51ff-a30e-274749b6d7af/scratchpad/'
O = S + 'ftn/agent2019/'
ME = pd.offsets.MonthEnd

d = pd.read_csv(S + 'ftn/ppm_panel_2018_2026.csv', parse_dates=['date'], low_memory=False)
d['fondnr'] = d.fondnr.astype(int)
d = d.sort_values(['fondnr', 'date']).reset_index(drop=True)
AP7 = [1, 2, 3, 4, 581371, 545541]
d['is_ap7'] = d.fondnr.isin(AP7) | d.fondnamn.str.contains('AP7', na=False)
d['mv_l'] = d.groupby('fondnr').mv_tot.shift(); d['val_l'] = d.groupby('fondnr').val_tot.shift()
d['hn_rel'] = d.handel_netto / d.mv_l; d['val_rel'] = d.val_tot / d.val_l - 1
d['dval'] = d.val_tot - d.val_l
months = sorted(d.date.unique()); END = months[-1]

# master list
l = pd.read_csv(S + 'xls/lista.csv'); l = l[l.FONDNAMN != '#REF!'].copy()
l['FONDNUMMER'] = l.FONDNUMMER.astype(int); l = l.set_index('FONDNUMMER')
l['AVSL'] = pd.to_datetime(l.AVSLUTSDATUM, errors='coerce')

# ---------- company key ----------
def ckey(s):
    s = re.sub(r'[^A-Za-z0-9ÅÄÖåäö ]', ' ', str(s)).lower()
    t = s.split()
    k = ' '.join(t[:2])
    alias = {'handelsbanken funds': 'handelsbanken fonder', 'xact kapitalförvaltning': 'handelsbanken fonder',
             'skagen as': 'storebrand', 'skagen fonder': 'storebrand', 'storebrand asset': 'storebrand', 'storebrand fonder': 'storebrand',
             'spp fonder': 'storebrand', 'odin forvaltning': 'odin fonder', 'blackrock luxembourg': 'blackrock', 'blackrock channel': 'blackrock',
             'seb funds': 'seb investment', 'aberdeen international': 'aberdeen', 'aberdeen standard': 'aberdeen', 'nn investment': 'nn asset',
             'lannebo kapitalförvaltning': 'lannebo fonder', 'atle fund': 'healthinvest partners', 'isec services': 'isec services',
             'fundrock management': 'fundrock', 'erste sparinvest': 'erste asset', 'franklin templeton': 'franklin', 'danske invest': 'danske invest',
             'alfred berg': 'alfred berg', 'swedbank robur': 'swedbank robur', 'nordic fund': 'nordic fund', 'fim kapitalförvaltning': 'fim',
             'c worldwide': 'c worldwide', 'amundi luxembourg': 'amundi', 'ubs fund': 'ubs', 'fil investment': 'fidelity', 'avanza fonder': 'avanza',
             'e öhman': 'öhman', 'pictet asset': 'pictet', 'allianz global': 'allianz', 'banque de': 'bl', 'morgan stanley': 'morgan stanley',
             'invl asset': 'invl', 'as trigon': 'trigon', 'dnb asset': 'dnb', 'j p': 'jpmorgan', 'jpmorgan asset': 'jpmorgan',
             'länsförsäkringar fondförvaltning': 'länsförsäkringar', 'axa rosenberg': 'axa', 'pinebridge investments': 'pinebridge',
             'baring international': 'baring', 'evli fondbolag': 'evli', 'aktia fondbolag': 'aktia', 'fondbolaget fondita': 'fondita',
             'ub fondbolag': 'ub', 'taaleri rahastoyhtiö': 'taaleri', 'sparinvest sa': 'sparinvest', 'east capital': 'east capital',
             'nordea funds': 'nordea', 'skandia fonder': 'skandia', 'carnegie fonder': 'carnegie', 'spiltan fonder': 'spiltan',
             'cicero fonder': 'cicero', 'ikc fonder': 'ikc', 'granit fonder': 'granit', 'tundra fonder': 'tundra', 'simplicity ab': 'simplicity',
             'enter fonder': 'enter', 'cliens kapitalförvaltning': 'cliens', 'didner gerge': 'didner', 'lemanik asset': 'solidar', 'solidar fonder': 'solidar',
             'bmo asset': 'bmo', 'first state': 'first state', 'credit suisse': 'credit suisse', 'aviva investors': 'aviva',
             'swedbank management': 'sef', 'luxcellence management': 'turkisfund', 'mdo management': 'coeli', 'valueinvest asset': 'valueinvest',
             'healthinvest partners': 'healthinvest partners', 'prior nilsson': 'prior nilsson', 'indecap fonder': 'indecap',
             'lundmark co': 'lundmark', 'zmartic fonder': 'zmartic', 'navigera ab': 'navigera', 'sensor fonder': 'sensor', 'insiderfonder ab': 'insiderfonder',
             'alfakraft fonder': 'alfakraft', 'aktie ansvar': 'aktie ansvar', 'tellus fonder': 'tellus', 'fcg fonder': 'fcg', 'erste asset': 'erste asset',
             'sentat asset': 'sentat', 'holberg fondsforvaltning': 'holberg', 'pareto asset': 'pareto', 'goldman sachs': 'goldman', 'invesco management': 'invesco',
             'atlant fonder': 'atlant', 'lantern structured': 'independent', 'seligson co': 'seligson', 'catella fondförvaltning': 'catella',
             'naventi fonder': 'naventi', 'aktieinvest fonder': 'aktieinvest', 'amf fonder': 'amf', 'monyx': 'nordic fund'}
    return alias.get(k, k)
d['ckey'] = d.forvaltare.map(ckey)

# ---------- fund-level summary ----------
g = d.groupby('fondnr').agg(name=('fondnamn', 'last'), isin_=('isin', 'last'), forv=('forvaltare', 'last'), ckey=('ckey', 'last'),
                            kat=('kategori', 'last'), typ=('fondtyp', 'last'), first=('date', 'min'), last=('date', 'max'), n=('date', 'size'))
P = d.set_index(['fondnr', 'date']).sort_index()
def prow(f, t):
    r = P.loc[(f, t)]
    return r.iloc[0] if isinstance(r, pd.DataFrame) else r

def forced_month(f, L):
    """first month (within last 4 observed) with forced-move signature; else None"""
    x = d[(d.fondnr == f)].set_index('date')
    x = x[x.index >= L - ME(1)]
    sig = ((x.hn_rel < -0.10) & (x.val_rel > 0.5 * x.hn_rel)) | (x.hn_rel < -0.80) | ((x.mv_tot < 0.25 * x.mv_l) & (x.hn_rel < -0.2))
    s = x[sig]
    return s.index.min() if len(s) else None

ex = g[(g['last'] >= '2018-10-31') & (g['last'] <= '2020-05-31')].copy()
rows = []
for f, r in ex.iterrows():
    L = r['last']; fm = forced_month(f, L)
    M = fm if fm is not None else L + ME(1)
    Mm1 = M - ME(1)
    if (f, Mm1) not in P.index:  # fund entered at M? use first available
        Mm1 = d[(d.fondnr == f) & (d.date < M)].date.max()
    pre = prow(f, Mm1) if pd.notna(Mm1) else None
    rows.append(dict(fondnr=f, name=r['name'], forv=r.forv, ckey=r.ckey, kat=r.kat, typ=r.typ, first=r['first'].date(), last=L.date(),
                     forced_in_panel=fm is not None, M=M.date(), Mm1=Mm1.date() if pd.notna(Mm1) else None,
                     mv_pre=pre.mv_tot if pre is not None else np.nan, val_pre=pre.val_tot if pre is not None else np.nan,
                     mv_last=prow(f, L).mv_tot, val_last=prow(f, L).val_tot,
                     hn_M_observed=prow(f, M).handel_netto if (f, M) in P.index else np.nan,
                     avsl=l.AVSL.get(f, pd.NaT), status=l.FONDSTATUS.get(f, np.nan)))
E = pd.DataFrame(rows); E['M'] = pd.to_datetime(E.M); E['Mm1'] = pd.to_datetime(E.Mm1)
E['Mper'] = E.M.dt.to_period('M')

# ---------- renumbering detection ----------
STOP = set('a b c d e p r h i 1a a1 a2 a12 acc ack cap dist sek usd eur jpy nok hedged class fund funds fonden fond placeringsfond si au c eacc pacc e-acc p-acc global'.split())
def core(name):
    s = re.sub(r'[^A-Za-z0-9ÅÄÖåäö ]', ' ', str(name)).lower().replace('healtcare', 'healthcare').replace('investement', 'investment')
    toks = [t for t in s.split() if t not in STOP]
    return set(toks)
en = g[(g['first'] >= '2018-10-31') & (g['first'] <= '2020-09-30')].copy()
firstrow = d.groupby('fondnr').head(1).set_index('fondnr')
en['mv_first'] = firstrow.mv_tot; en['val_first'] = firstrow.val_tot
E['renum_to'] = np.nan; E['renum_name'] = None; E['renum_rule'] = None
for i, r in E.iterrows():
    c = en[(en['first'] >= r.M - ME(1)) & (en['first'] <= r.M + ME(3)) & (en.index != r.fondnr)]
    best = None
    for f2, r2 in c.iterrows():
        samec = r2.ckey == r.ckey
        a, b = core(r['name']), core(r2['name'])
        jac = len(a & b) / max(1, len(a | b))
        size_ok = (0.5 <= r2.mv_first / max(r.mv_pre, 1) <= 1.6) and (0.5 <= r2.val_first / max(r.val_pre, 1) <= 1.6)
        if (samec and jac >= 0.6) or (samec and size_ok and r.mv_pre >= 5e6 and jac >= 0.4) or (jac >= 0.75 and size_ok):
            sc = 2 * jac + (1 if size_ok else 0) + (0.5 if samec else 0)
            if best is None or sc > best[0]:
                best = (sc, f2, r2['name'], f'jac={jac:.2f} samec={samec} size_ok={size_ok}')
    if best:
        E.loc[i, 'renum_to'] = best[1]; E.loc[i, 'renum_name'] = best[2]; E.loc[i, 'renum_rule'] = best[3]; E.loc[i, 'renum_score'] = best[0]
# one-to-one: keep the best-scoring exit per entry
E = E.sort_values('renum_score', ascending=False)
dup = E.renum_to.notna() & E.duplicated('renum_to', keep='first')
E.loc[dup, ['renum_to', 'renum_name', 'renum_rule']] = [np.nan, None, None]
E = E.sort_values('fondnr')
E['is_renum'] = E.renum_to.notna()

# ---------- receiver (sibling / merger) matching ----------
# receiver candidates: non-AP7 funds with excess inflow in month M
d['hn_base'] = d.groupby('fondnr').handel_netto.transform(lambda s: s.shift(1).rolling(6, min_periods=2).median())
d['x_hn'] = d.handel_netto - d.hn_base.fillna(0)
d['x_mv'] = d.mv_tot - d.mv_l * (1 + d.ret_1m.fillna(0) / 100) - d.hn_base.fillna(0)
d['x_in'] = np.where(d.mv_l.isna(), d.mv_tot, np.fmax(d.x_hn, d.x_mv.where(d.ret_1m.notna(), -np.inf)))
d['x_rel'] = d.x_in / d.mv_l
cand = d[(~d.is_ap7) & (d.date >= '2018-11-30') & (d.date <= '2020-07-31') & (d.x_in > 10e6) & ((d.x_in > 0.05 * d.mv_l) | d.mv_l.isna())].copy()
cand['cap_left'] = cand.x_in.values; cand['sav_left'] = cand.dval.fillna(cand.val_tot).values
cand = cand.set_index(['date', 'fondnr'])
# manual, letter-verified cross-company mergers (fondhändelsebrev 2019)
MANUAL = {374835: 959502, 339002: 959502, 172601: 959502,   # Navigera Strategi x3 -> Cicero World 0-100 (letter FHB001056, merger 27 Feb 2019)
          123968: 959502, 159798: 959502, 195628: 959502,   # Zmart Beta (FHB001062, verified: -> Cicero World 0-100, 27 Feb 2019), Optimal, Balanserad (FHB001063-64, same letter series)
          778589: 959502,                                   # Zmart Alfa (assumed same merger as the other Zmart funds; no letter fetched)
          738500: 959502, 855973: 959502,                   # Cicero Världen / Cicero World Wide -> Cicero World 0-100 (same company, Feb/Mar 2019; by size, letter not fetched)
          354704: 972901,                                   # Viking Fonder Sverige -> Cicero Focus (FHB001061, merger 28 Mar 2019)
          156315: 303701,                                   # Granit Basfonden -> Sensor Sverige Select (FHB001080, merger 1 Apr 2019)
          476895: 536276, 208439: 536276, 590463: 536276}   # Inside Sweden (FHB001165), IKC Global Brand (FHB001175), IKC 0-50 (FHB001173) -> East Capital Multi-Strategi, Apr 2019
# company pairs with at least one letter-verified cross-company merger: other funds of the same source company may match the same receiver company
PAIRS = {('navigera', 'cicero'), ('zmartic', 'cicero'), ('isec services', 'cicero'), ('granit', 'sensor'), ('insiderfonder', 'east capital'), ('ikc', 'east capital')}
E['recv_to'] = np.nan; E['recv_name'] = None; E['recv_rule'] = None; E['recv_x_in'] = np.nan; E['recv_dval'] = np.nan
# renumbering targets are not receivers
cand = cand[~cand.index.get_level_values(1).isin(E.renum_to.dropna().astype(int))]
E = E.sort_values('mv_pre', ascending=False)
def try_match(i, r, rule):
    if E.loc[i, 'is_renum'] or pd.notna(E.loc[i, 'recv_to']): return
    for Mx in [r.M]:
        if Mx not in cand.index.get_level_values(0): continue
        cc = cand.loc[Mx]
        cc = cc[cc.index != r.fondnr]
        if rule == 'manual':
            if r.fondnr in MANUAL and MANUAL[r.fondnr] in cc.index: cc = cc.loc[[MANUAL[r.fondnr]]]
            else: continue
        elif rule == 'same_company':
            cc = cc[(cc.ckey == r.ckey) & ((cc.cap_left >= 0.5 * r.mv_pre) | (cc.sav_left >= 0.5 * r.val_pre)) & (r.mv_pre >= 1e6)]
        elif rule == 'cross_company':
            ok = cc.ckey.map(lambda k: (r.ckey, k) in PAIRS)
            cc = cc[ok & (cc.cap_left >= 0.2 * r.mv_pre)]
        if len(cc) == 0: continue
        ctoks = set(r.ckey.split()) | {'fonder', 'fond', 'ab', 'funds', 'fund'}
        def stems(n): return {t[:5] for t in core(n) if t not in ctoks and len(t) > 3}
        nb = cc.fondnamn.map(lambda n: -0.5 * len(stems(n) & stems(r['name'])))
        cc = cc.assign(score=(np.log(np.maximum(cc.cap_left, 1) / max(r.mv_pre, 1))).abs() + nb).sort_values('score')
        f2 = cc.index[0]
        E.loc[i, 'recv_to'] = f2; E.loc[i, 'recv_name'] = cc.fondnamn.iloc[0]; E.loc[i, 'recv_rule'] = rule + ('' if Mx == r.M else '+1')
        E.loc[i, 'recv_x_in'] = cc.x_in.iloc[0]; E.loc[i, 'recv_dval'] = cc.dval.iloc[0]
        cand.loc[(Mx, f2), 'cap_left'] -= r.mv_pre; cand.loc[(Mx, f2), 'sav_left'] -= r.val_pre
        return
for rule in ['manual', 'same_company', 'cross_company']:
    for i, r in E.iterrows(): try_match(i, r, rule)
E = E.sort_values(['M', 'mv_pre'], ascending=[True, False])

# ---------- classification ----------
def cls(r):
    if r.is_renum: return 'renumbering'
    if pd.notna(r.recv_to): return 'merger_default_to_fund'
    return 'default_to_AP7'
E['dest_class'] = E.apply(cls, axis=1)
def period(m):
    if m <= pd.Period('2018-12', 'M'): return 'pre_2018Q4'
    if m <= pd.Period('2019-07', 'M'): return 'purge_wave_2019H1'
    if m <= pd.Period('2019-12', 'M'): return 'purge_late_2019H2'
    return 'post_2020H1'
E['period'] = E.Mper.map(period)
E['purge_sample'] = (E.period.str.startswith('purge')) & (E.dest_class != 'renumbering')

# ---------- receiver groups (merger / sibling defaults) ----------
mg_ = E[E.dest_class == 'merger_default_to_fund']
RG = mg_.groupby(['M', 'recv_to']).agg(recv_name=('recv_name', 'first'), n_exits=('fondnr', 'size'), mv_sum=('mv_pre', 'sum'), val_sum=('val_pre', 'sum'),
                                        x_in=('recv_x_in', 'first'), dval=('recv_dval', 'first')).reset_index()
RG['default_cap'] = np.minimum(RG.x_in, RG.mv_sum); RG['vol_in_M_cap'] = RG.mv_sum - RG.default_cap
RG['default_sav'] = np.minimum(RG.dval.fillna(RG.val_sum), RG.val_sum); RG['vol_in_M_sav'] = RG.val_sum - RG.default_sav
RG.to_csv(O + 't2_receiver_groups.csv', index=False)
# allocate group split back to funds pro rata (for group-level sums only)
E = E.merge(RG[['M', 'recv_to', 'mv_sum', 'val_sum', 'default_cap', 'default_sav']], on=['M', 'recv_to'], how='left')
E['default_recv_cap'] = E.default_cap * E.mv_pre / E.mv_sum
E['vol_in_M_recv'] = E.mv_pre - E.default_recv_cap
E['sav_default_recv'] = E.default_sav * E.val_pre / E.val_sum
E = E.drop(columns=['mv_sum', 'val_sum', 'default_cap', 'default_sav'])

# ---------- decomposition windows ----------
RECV_MONTHS = set(zip(RG.recv_to.astype(int), RG.M))   # (fondnr, month) where the fund itself received a merger/sibling transfer
E['was_receiver_in_window'] = E.apply(lambda r: any((int(r.fondnr), m) in RECV_MONTHS for m in pd.date_range(r.M - ME(4), r.M - ME(1), freq='ME')), axis=1)
# fund-specific baseline churn: mean monthly net trade / mv in 2018-01..2018-10 (pre-rules, ex December)
b18 = d[(d.date >= '2018-01-31') & (d.date <= '2018-10-31')].groupby('fondnr').apply(lambda x: (x.handel_netto / x.mv_l).mean())
CHURN = b18.to_dict()
def window_vol(f, A, Mm1, exdec=False, adj=False):
    x = d[(d.fondnr == f) & (d.date >= A) & (d.date <= Mm1)].copy()
    if exdec: x = x[x.date.dt.month != 12]
    if adj and len(x):
        c = CHURN.get(f, np.nan)
        if pd.notna(c): x['handel_netto'] = x.handel_netto - c * x.mv_l.fillna(x.mv_tot)
    # months where the fund itself was a merger receiver: replace net trade with its rolling-median baseline
    rec = x.apply(lambda z: (int(z.fondnr), z.date) in RECV_MONTHS, axis=1) if len(x) else pd.Series([], dtype=bool)
    hn = np.where(rec, x.hn_base.fillna(0), x.handel_netto)
    return -np.nansum(hn), len(x)
def val_at(f, t):
    return prow(f, t).val_tot if (f, t) in P.index else np.nan
for lab, A_of in [('w1', lambda r: r.Mm1), ('w2', lambda r: r.Mm1 - ME(1)), ('w3', lambda r: r.Mm1 - ME(2)),
                  ('fix1901', lambda r: pd.Timestamp('2019-01-31')), ('fix1811', lambda r: pd.Timestamp('2018-11-30'))]:
    V, Vx, N, SV, VA = [], [], [], [], []
    for i, r in E.iterrows():
        A = A_of(r)
        A = max(A, pd.Timestamp(r['first']))
        if pd.isna(r.Mm1) or A > r.Mm1: V.append(np.nan); Vx.append(np.nan); N.append(0); SV.append(np.nan); VA.append(np.nan); continue
        v, n = window_vol(r.fondnr, A, r.Mm1); vx, _ = window_vol(r.fondnr, A, r.Mm1, exdec=True); va_, _ = window_vol(r.fondnr, A, r.Mm1, exdec=True, adj=True)
        V.append(v); Vx.append(vx); N.append(n); VA.append(va_)
        va = val_at(r.fondnr, A - ME(1))
        SV.append(va - r.val_pre if pd.notna(va) else np.nan)
    E[f'vol_{lab}'] = V; E[f'volx_{lab}'] = Vx; E[f'nmon_{lab}'] = N; E[f'sav_vol_{lab}'] = SV; E[f'vola_{lab}'] = VA
    E[f'pct_vol_{lab}'] = 100 * E[f'vol_{lab}'] / (E[f'vol_{lab}'] + E.mv_pre)
# receiver-based split for merger cases: default = receiver excess inflow (capped), voluntary_M = mv_pre - that

E.to_csv(O + 't1_exits_classified.csv', index=False)

# ---------- task 1 tables ----------
t1 = E.groupby(['Mper', 'dest_class']).agg(n=('fondnr', 'size'), mv_pre_bn=('mv_pre', lambda s: s.sum() / 1e9), savers=('val_pre', 'sum')).reset_index()
t1.to_csv(O + 't1_exits_by_month_class.csv', index=False)
t1p = E.groupby(['period', 'dest_class']).agg(n=('fondnr', 'size'), mv_pre_bn=('mv_pre', lambda s: s.sum() / 1e9), savers=('val_pre', 'sum')).reset_index()
t1p.to_csv(O + 't1_exits_by_period_class.csv', index=False)
print('=== exits by period x class ==='); print(t1p.round(2).to_string())
print('=== exits by month (all classes) ===')
print(E.groupby('Mper').agg(n=('fondnr', 'size'), mv_bn=('mv_pre', lambda s: s.sum() / 1e9), n_renum=('is_renum', 'sum'),
                            n_merger=('dest_class', lambda s: (s == 'merger_default_to_fund').sum()), n_ap7=('dest_class', lambda s: (s == 'default_to_AP7').sum())).round(2).to_string())
print('renumberings:'); print(E[E.is_renum][['fondnr', 'name', 'M', 'mv_pre', 'renum_to', 'renum_name', 'renum_rule']].assign(mv_pre=lambda z: (z.mv_pre / 1e6).round(0)).to_string(index=False))
print('mergers/sibling defaults:'); print(E[E.dest_class == 'merger_default_to_fund'][['fondnr', 'name', 'ckey', 'M', 'mv_pre', 'val_pre', 'recv_to', 'recv_name', 'recv_rule', 'recv_x_in', 'recv_dval']]
                                           .assign(mv_pre=lambda z: (z.mv_pre / 1e6).round(0), recv_x_in=lambda z: (z.recv_x_in / 1e6).round(0)).to_string(index=False))

# ---------- task 2: decomposition ----------
def summ(df, label):
    out = dict(sample=label, n=len(df), mv_pre_bn=df.mv_pre.sum() / 1e9, savers_pre=df.val_pre.sum())
    for w in ['w1', 'w2', 'w3', 'fix1901', 'fix1811']:
        s = df[df[f'nmon_{w}'] > 0]
        v, vx, dflt, va_ = s[f'vol_{w}'].sum(), s[f'volx_{w}'].sum(), s.mv_pre.sum(), s[f'vola_{w}'].sum()
        out[f'{w}_pct_vol_cap_churnadj'] = 100 * va_ / (va_ + dflt)
        sv, sd = s[f'sav_vol_{w}'].sum(), s.val_pre.sum()
        out[f'{w}_n'] = len(s); out[f'{w}_vol_bn'] = v / 1e9; out[f'{w}_pct_vol_cap'] = 100 * v / (v + dflt)
        out[f'{w}_pct_vol_cap_exDec'] = 100 * vx / (vx + dflt); out[f'{w}_pct_vol_sav'] = 100 * sv / (sv + sd)
        out[f'{w}_median_pct_vol_fund'] = s[f'pct_vol_{w}'].median()
    m = df[df.dest_class == 'merger_default_to_fund']
    if len(m):
        out['merger_n'] = len(m); out['merger_mv_bn'] = m.mv_pre.sum() / 1e9
        out['merger_pct_vol_in_M_recv'] = 100 * m.vol_in_M_recv.sum() / m.mv_pre.sum()
        out['merger_pct_sav_vol_in_M_recv'] = 100 * (m.val_pre.sum() - m.sav_default_recv.sum()) / m.val_pre.sum()
    return out
PS = E[E.purge_sample]
res = [summ(PS, 'purge_all_2019'), summ(PS[PS.dest_class == 'default_to_AP7'], 'purge_AP7_default'),
       summ(PS[PS.dest_class == 'merger_default_to_fund'], 'purge_merger_default'),
       summ(PS[PS.period == 'purge_wave_2019H1'], 'wave_2019H1'), summ(PS[PS.period == 'purge_late_2019H2'], 'late_2019H2'),
       summ(E[(E.period == 'pre_2018Q4') & ~E.is_renum], 'pre_2018Q4_nonrenum'), summ(E[(E.period == 'post_2020H1') & ~E.is_renum], 'post_2020H1_nonrenum')]
for m, s in PS.groupby('Mper'): res.append(summ(s, f'month_{m}'))
PS = PS.copy(); PS['tercile'] = pd.qcut(PS.mv_pre.rank(method='first'), 3, labels=['small', 'mid', 'large'])
for t, s in PS.groupby('tercile', observed=True): res.append(summ(s, f'size_{t}'))
for t, s in PS.groupby('typ'): res.append(summ(s, f'type_{t}'))
T2 = pd.DataFrame(res); T2.to_csv(O + 't2_decomposition_summary.csv', index=False)
print('=== decomposition summary ===')
print(T2[['sample', 'n', 'mv_pre_bn', 'savers_pre', 'w1_pct_vol_cap', 'w1_pct_vol_cap_churnadj', 'w1_pct_vol_sav', 'w2_pct_vol_cap_exDec', 'w2_pct_vol_cap_churnadj', 'w3_pct_vol_cap_exDec', 'w3_pct_vol_cap_churnadj',
          'fix1901_n', 'fix1901_pct_vol_cap_exDec', 'fix1901_pct_vol_cap_churnadj', 'fix1811_pct_vol_cap_exDec', 'fix1811_pct_vol_cap_churnadj', 'w1_median_pct_vol_fund', 'merger_pct_vol_in_M_recv', 'merger_pct_sav_vol_in_M_recv']].round(2).to_string())
# distribution across funds
dist = PS[['fondnr', 'name', 'dest_class', 'M', 'mv_pre', 'val_pre', 'pct_vol_w1', 'pct_vol_w2', 'pct_vol_w3', 'pct_vol_fix1901']].copy()
print('=== distribution of fund-level % voluntary (w1 = letter month only; w3 = 3 months) ===')
print(PS[['pct_vol_w1', 'pct_vol_w2', 'pct_vol_w3', 'pct_vol_fix1901']].describe(percentiles=[.1, .25, .5, .75, .9]).round(2).to_string())
wq = PS[PS.mv_pre > 100e6]
print('funds > 100m:'); print(wq[['pct_vol_w1', 'pct_vol_w2', 'pct_vol_w3']].describe(percentiles=[.1, .25, .5, .75, .9]).round(2).to_string())
PS.to_csv(O + 't2_purge_funds_decomposition.csv', index=False)

# ---------- task 3: destination by month ----------
ap = d[d.fondnr.isin([581371, 545541])].groupby('date').handel_netto.sum()
safa = d[d.fondnr == 1].set_index('date').val_tot.diff()
base_months = [m for m in months if m >= pd.Timestamp('2018-02-28') and m <= pd.Timestamp('2018-11-30') and m.month not in (6, 12)]  # Jun-18: one-off 15bn AP7 inflow (non-purge event)
ap_base = ap.loc[base_months].median(); safa_base = safa.loc[base_months].median()
AP_BASES = {'base_med2018': ap_base, 'base_0': 0.0, 'base_1bn': 1.0e9}
nonap7 = d[~d.is_ap7].groupby('date').handel_netto.sum()
allhn = d.groupby('date').handel_netto.sum()
rows = []
for m in [x for x in months if pd.Timestamp('2018-10-31') <= x <= pd.Timestamp('2020-07-31')]:
    mp = m.to_period('M')
    ex_m = E[(E.Mper == mp)]
    ex_np = ex_m[~ex_m.is_renum]
    rec = cand.loc[m] if m in cand.index.get_level_values(0) else pd.DataFrame()
    matched_recv = RG[RG.M.dt.to_period('M') == mp]
    rows.append(dict(month=str(mp), n_exits=len(ex_m), n_renum=int(ex_m.is_renum.sum()), n_ap7_default=int((ex_m.dest_class == 'default_to_AP7').sum()),
                     n_merger=int((ex_m.dest_class == 'merger_default_to_fund').sum()),
                     mv_pre_exits_nonrenum_bn=ex_np.mv_pre.sum() / 1e9,
                     mv_pre_ap7_default_bn=ex_m[ex_m.dest_class == 'default_to_AP7'].mv_pre.sum() / 1e9,
                     mv_pre_merger_bn=ex_m[ex_m.dest_class == 'merger_default_to_fund'].mv_pre.sum() / 1e9,
                     mv_pre_renum_bn=ex_m[ex_m.is_renum].mv_pre.sum() / 1e9,
                     ap7_hn_bn=ap.get(m, np.nan) / 1e9, ap7_excess_bn=(ap.get(m, np.nan) - ap_base) / 1e9,
                     safa_dsavers=safa.get(m, np.nan), safa_dsavers_excess=safa.get(m, np.nan) - safa_base,
                     recv_matched_inflow_bn=matched_recv.x_in.sum() / 1e9 if len(matched_recv) else 0.0,
                     recv_matched_capped_bn=matched_recv.default_cap.sum() / 1e9 if len(matched_recv) else 0.0,
                     abn_inflow_nonap7_bn=(rec.x_in.sum() / 1e9) if len(rec) else 0.0,
                     allfunds_hn_bn=allhn.get(m, np.nan) / 1e9, nonap7_hn_bn=nonap7.get(m, np.nan) / 1e9,
                     savers_ap7_default_exits=ex_m[ex_m.dest_class == 'default_to_AP7'].val_pre.sum()))
T3 = pd.DataFrame(rows); T3.to_csv(O + 't3_destination_by_month.csv', index=False)
print('=== destination by month (bn SEK) ===  AP7 proxy = handel_netto(AP7 Aktiefond)+handel_netto(AP7 Räntefond); base = 2018 Jan-Nov mean = %.2f bn' % (ap_base / 1e9))
print(T3.round(2).to_string())
w = T3[(T3.month >= '2019-01') & (T3.month <= '2019-11')]
tot = dict(mv_nonrenum=w.mv_pre_exits_nonrenum_bn.sum(), mv_ap7cls=w.mv_pre_ap7_default_bn.sum(), mv_merger=w.mv_pre_merger_bn.sum(),
           ap7_raw=w.ap7_hn_bn.sum(), ap7_excess=w.ap7_excess_bn.sum(), recv_matched=w.recv_matched_inflow_bn.sum(), recv_matched_capped=w.recv_matched_capped_bn.sum(),
           abn_inflow_nonap7=w.abn_inflow_nonap7_bn.sum(), safa_dsav_raw=w.safa_dsavers.sum(), safa_dsav_excess=w.safa_dsavers_excess.sum(),
           savers_ap7cls=w.savers_ap7_default_exits.sum(), savers_merger=E[(E.Mper >= pd.Period('2019-01', 'M')) & (E.Mper <= pd.Period('2019-11', 'M')) & (E.dest_class == 'merger_default_to_fund')].val_pre.sum())
for k, b in AP_BASES.items(): tot[f'ap7_excess_{k}'] = tot['ap7_raw'] - 11 * b / 1e9; tot[f'ap7_capture_pct_{k}'] = 100 * tot[f'ap7_excess_{k}'] / tot['mv_ap7cls']
tot['safa_capture_pct_savers'] = 100 * tot['safa_dsav_excess'] / tot['savers_ap7cls']
print('2019 (Jan-Nov) totals:', {k: round(v, 2) for k, v in tot.items()})
json.dump({k: float(v) for k, v in tot.items()} | dict(ap7_base_bn=ap_base / 1e9, safa_base=safa_base), open(O + 't3_totals_2019.json', 'w'), indent=1)
# monthly AP7-class vs AP7 excess check
chk = w[['month', 'n_ap7_default', 'mv_pre_ap7_default_bn', 'ap7_excess_bn', 'savers_ap7_default_exits', 'safa_dsavers_excess']].copy()
chk['ratio_cap'] = chk.ap7_excess_bn / chk.mv_pre_ap7_default_bn
print(chk.round(2).to_string())

# ---------- task 4: side by side with FTN ----------
A = pd.read_csv(S + 'ftn/agentA/summary_by_round.csv')
ftn = A[A['round'].str.startswith('TOTAL exited')].iloc[0]
L2 = pd.read_csv(S + 'ftn/agentA/task2_loser_decomposition.csv')
L2e = L2[L2.exited]
ap7s = PS[PS.dest_class == 'default_to_AP7']; mg = PS[PS.dest_class == 'merger_default_to_fund']
def row(label, n, mv, vol, dflt, sv, sd, note):
    return dict(sample=label, n_funds=n, mv_at_event_bn=mv / 1e9, vol_bn=vol / 1e9, default_bn=dflt / 1e9, pct_vol_cap=100 * vol / (vol + dflt),
                pct_vol_sav=100 * sv / (sv + sd) if sd else np.nan, note=note)
sb = [row('FTN 2024-26 exited losers (agent A)', int(ftn.n_los), ftn.mv_award_bn * 1e9, ftn.vol_bn * 1e9, ftn.default_bn * 1e9, ftn.sav_vol, ftn.sav_default,
          'announcement = award; voluntary = outflow award..M-1 (median 3-6 months); default = mv at M-1'),
      row('2019 purge, all non-renum (w1: last observed month only)', len(PS), PS.mv_pre.sum(), PS.vol_w1.sum(), PS.mv_pre.sum(), PS.sav_vol_w1.sum(), PS.val_pre.sum(),
          'letter typically mid/late M-1; voluntary in M unobserved at fund level'),
      row('2019 purge, all non-renum (w3: 3 months)', len(PS), PS.mv_pre.sum(), PS.volx_w3.sum(), PS.mv_pre.sum(), PS.sav_vol_w3.sum(), PS.val_pre.sum(), 'exDec'),
      row('2019 purge, AP7-default only (w1)', len(ap7s), ap7s.mv_pre.sum(), ap7s.vol_w1.sum(), ap7s.mv_pre.sum(), ap7s.sav_vol_w1.sum(), ap7s.val_pre.sum(), ''),
      row('2019 purge, AP7-default only (w3 exDec)', len(ap7s), ap7s.mv_pre.sum(), ap7s.volx_w3.sum(), ap7s.mv_pre.sum(), ap7s.sav_vol_w3.sum(), ap7s.val_pre.sum(), ''),
      row('2019 purge, merger-default only (w1)', len(mg), mg.mv_pre.sum(), mg.vol_w1.sum(), mg.mv_pre.sum(), mg.sav_vol_w1.sum(), mg.val_pre.sum(), ''),
      row('2019 merger-default, receiver-based incl. move month', len(mg), mg.mv_pre.sum(), mg.vol_w1.sum() + mg.vol_in_M_recv.sum(), mg.default_recv_cap.sum(),
          mg.sav_vol_w1.sum() + (mg.val_pre.sum() - mg.sav_default_recv.sum()), mg.sav_default_recv.sum(), 'default = receiver excess inflow in M; voluntary adds mv_pre - receiver inflow'),
      ]
# AP7-default, destination-based (aggregate): default = AP7 excess inflow in 2019 months; voluntary = rest of mv_pre
mv_ap7 = ap7s.mv_pre.sum()
for k in AP_BASES:
    ap7_def = tot[f'ap7_excess_{k}'] * 1e9
    sb.append(row(f'2019 AP7-default, destination-based ({k}: AP7 excess inflow Jan-Nov 2019)', len(ap7s), mv_ap7, ap7s.vol_w1.sum() + max(mv_ap7 - ap7_def, 0), min(ap7_def, mv_ap7),
                  ap7s.sav_vol_w1.sum() + max(ap7s.val_pre.sum() - tot['safa_dsav_excess'], 0), min(tot['safa_dsav_excess'], ap7s.val_pre.sum()),
                  'default = excess AP7 Aktie+Räntefond net trade; voluntary = w1 + (mv_pre - AP7 excess); noisy upper bound'))
# FTN losers with the same short windows (w1 = month before move only, w3 = 3 months before move), from agent A's move_start
d2 = pd.read_csv(S + 'ftn/ppm_panel_2022_2026.csv', parse_dates=['date'], low_memory=False)
P2 = d2.set_index(['fondnr', 'date']).sort_index()
L2e = L2e.copy(); L2e['move_start'] = pd.to_datetime(L2e.move_start)
for k in [1, 2, 3]:
    V, SV, D, SD = [], [], [], []
    for _, r in L2e.iterrows():
        M = r.move_start; Mm1 = M - ME(1); A = M - ME(k)
        x = d2[(d2.fondnr == r.fondnr) & (d2.date >= A) & (d2.date <= Mm1)]
        xx = x[x.date.dt.month != 12]
        V.append(-xx.handel_netto.sum()); D.append(x[x.date == Mm1].mv_tot.sum())
        va = d2[(d2.fondnr == r.fondnr) & (d2.date == A - ME(1))].val_tot
        SV.append((va.iloc[0] - x[x.date == Mm1].val_tot.iloc[0]) if len(va) and len(x) else np.nan); SD.append(x[x.date == Mm1].val_tot.sum())
    L2e[f'vol_w{k}'] = V; L2e[f'def_w{k}'] = D; L2e[f'sv_w{k}'] = SV; L2e[f'sd_w{k}'] = SD
    sb.append(row(f'FTN exited losers, short window w{k} (exDec)', len(L2e), L2e.mv_award.sum(), L2e[f'vol_w{k}'].sum(), L2e[f'def_w{k}'].sum(), L2e[f'sv_w{k}'].sum(), L2e[f'sd_w{k}'].sum(),
                  f'like-for-like with 2019 w{k}: voluntary = -net trade in the {k} month(s) before move_start; default = mv at M-1'))
T4 = pd.DataFrame(sb); T4.to_csv(O + 't4_side_by_side_ftn.csv', index=False)
print('=== side by side ==='); print(T4.round(2).to_string())

# ---------- letters fetched (fondhändelsebrev, pensionsmyndigheten.se) ----------
LET = [(920074, 'Cliens Mixfond', '2019-05-17', '2019-06-10', 'avregistrering avslag', 'AP7 Såfa'),
       (762880, 'Monyx Strategi Offensiv', '2019-05-28', '2019-06-20', 'avregistrering (förändringar inom premiepensionen)', 'AP7 Såfa'),
       (889386, 'Evli Ryssland', '2019-03-19', '2019-04-09', 'avregistrering (förändrad lagstiftning)', 'AP7 Såfa'),
       (273300, 'Swedbank Robur Företagsobligationsfond', '2019-01-17', '2019-02-05', 'avregistrering (fondbolagets begäran)', 'AP7 Såfa'),
       (964171, 'Swedbank Robur Europafond MEGA', '2019-04-03', '2019-04-23', 'avregistrering (fondbolagets begäran)', 'Swedbank Robur Access Europa (755504)'),
       (296152, 'KPA Etisk Aktiefond', '2019-04-30', '2019-05-31', 'avregistrering (fondbolagets begäran)', 'Swedbank Robur Aktiefond Pension (785022)'),
       (339002, 'Navigera Strategi Världen', '2019-02-01', '2019-02-21', 'sammanläggning 2019-02-27', 'Cicero World 0-100 (959502)'),
       (123968, 'Zmart Beta', '2019-02-01', '2019-02-21', 'sammanläggning 2019-02-27', 'Cicero World 0-100 (959502)'),
       (354704, 'Viking Fonder Sverige', '2019-03-04', '2019-03-21', 'sammanläggning 2019-03-28', 'Cicero Focus (972901)'),
       (156315, 'Granit Basfonden', '2019-03-06', '2019-03-27', 'sammanläggning 2019-04-01', 'Sensor Sverige Select (303701)'),
       (476895, 'Inside Sweden', '2019-03-06', '2019-03-21', 'sammanläggning 2019-04-01', 'East Capital Multi-Strategi (536276)'),
       (208439, 'IKC Global Brand', '2019-03-07', '2019-03-28', 'sammanläggning 2019-04-08', 'East Capital Multi-Strategi (536276)')]
LT = pd.DataFrame(LET, columns=['fondnr', 'fund', 'letter_date', 'deadline', 'type', 'default_destination'])
LT['letter_date'] = pd.to_datetime(LT.letter_date); LT['deadline'] = pd.to_datetime(LT.deadline)
LT['days_letter_to_deadline'] = (LT.deadline - LT.letter_date).dt.days
LT = LT.merge(E[['fondnr', 'M', 'Mm1', 'forced_in_panel', 'dest_class', 'mv_pre']], on='fondnr', how='left')
LT['letter_month_is_Mm1'] = LT.letter_date.dt.to_period('M') == LT.Mm1.dt.to_period('M')
LT['days_letter_to_Mm1_monthend'] = (LT.Mm1 - LT.letter_date).dt.days
LT.to_csv(O + 't0_letters_sample.csv', index=False)
print('=== letters ==='); print(LT.to_string())

# ---------- task 5: examples ----------
EX = [889386, 920074, 762880, 964171, 755504, 296152, 785022, 119776, 912287, 313155, 443895, 374835, 959502, 753442, 114819, 749788, 964767, 581371, 545541, 1]
rows = []
for f in EX:
    x = d[(d.fondnr == f) & (d.date >= '2018-11-30') & (d.date <= '2019-10-31')]
    for _, z in x.iterrows():
        rows.append(dict(fondnr=f, fondnamn=z.fondnamn, date=z.date.date(), mv_m=round(z.mv_tot / 1e6, 1), val_tot=z.val_tot, hn_m=round(z.handel_netto / 1e6, 1) if pd.notna(z.handel_netto) else None,
                         hn_rel=round(z.hn_rel, 3) if pd.notna(z.hn_rel) else None, val_rel=round(z.val_rel, 3) if pd.notna(z.val_rel) else None))
T5 = pd.DataFrame(rows); T5.to_csv(O + 't5_examples_monthly.csv', index=False)
print('done')
