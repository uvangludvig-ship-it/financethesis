"""FACT 2: gender gap in opting out before the forced move. Losers of executed rounds: award month A -> M-1 (task2 move_start - 1).
Opt-out rate = net decline in savers (val) between A and M-1, women vs men. Capital version return-adjusted with ret_1m."""
from common import *
d = load_panel(); t1, t2 = load_rounds()
P = d.set_index(['fondnr', 'date']).sort_index()

def window_change(f, A, E):
    """A, E: month-ends (inclusive). returns dict with val/mv by gender at A and E, cumulative return A+1..E"""
    try:
        a = P.loc[(f, A)]; e = P.loc[(f, E)]
    except KeyError:
        return None
    seg = d[(d.fondnr == f) & (d.date > A) & (d.date <= E)]
    cumret = np.prod(1 + seg.ret_1m.fillna(0) / 100)
    return dict(val_k_A=a.val_k, val_m_A=a.val_m, val_k_E=e.val_k, val_m_E=e.val_m, mv_k_A=a.mv_k, mv_m_A=a.mv_m, mv_k_E=e.mv_k, mv_m_E=e.mv_m,
                cumret=cumret, n_months=len(seg), dec_in_window=bool(seg.is_dec.any()))

rows = []
for _, r in t2.iterrows():
    A = pd.Timestamp(AWARD_ME[r['round']]); M = r.move_start
    E = M - pd.offsets.MonthEnd(1)
    if E <= A:  # no pre-move month after award
        continue
    w = window_change(r.fondnr, A, E)
    if w is None: continue
    rows.append(dict(sample='FTN', round=r['round'], fondnr=r.fondnr, fondnamn=r.fondnamn, A=A.date(), E=E.date(), M=M.date(), exited=r.exited, **w))

# 2019 purge: AP7-default exits, baseline 2018-12-31 -> Mm1
p = pd.read_csv(F + 'agent2019/t2_purge_funds_decomposition.csv', parse_dates=['M', 'Mm1'])
p = p[p.purge_sample & (p.dest_class == 'default_to_AP7') & (p.Mm1 >= '2019-01-31') & (p.was_receiver_in_window != True)]
print('2019 AP7-default purge funds after excluding merger receivers in window:', len(p))
for _, r in p.iterrows():
    A = pd.Timestamp('2018-12-31'); E = r.Mm1
    w = window_change(r.fondnr, A, E)
    if w is None: continue
    rows.append(dict(sample='purge2019_AP7', round='purge2019', fondnr=r.fondnr, fondnamn=r['name'], A=A.date(), E=E.date(), M=r.M.date(), exited=True, **w))
# 2019 purge, fixed 3-month window before M (M-3 .. M-1), comparable to FTN median award-to-move lag
for _, r in p.iterrows():
    E = r.Mm1; A = E - pd.offsets.MonthEnd(3)
    if A < pd.Timestamp('2018-01-31'): continue
    w = window_change(r.fondnr, A, E)
    if w is None: continue
    rows.append(dict(sample='purge2019_AP7_3m', round='purge2019_3m', fondnr=r.fondnr, fondnamn=r['name'], A=A.date(), E=E.date(), M=r.M.date(), exited=True, **w))

X = pd.DataFrame(rows)
X = X[(X.val_k_A > 0) & (X.val_m_A > 0)]
X['opt_k'] = 100 * (X.val_k_A - X.val_k_E) / X.val_k_A
X['opt_m'] = 100 * (X.val_m_A - X.val_m_E) / X.val_m_A
X['cap_k'] = 100 * (X.mv_k_A - X.mv_k_E / X.cumret) / X.mv_k_A   # return-adjusted capital decline
X['cap_m'] = 100 * (X.mv_m_A - X.mv_m_E / X.cumret) / X.mv_m_A
X['share_k_A'] = 100 * X.val_k_A / (X.val_k_A + X.val_m_A)
X['mv_per_saver_k_A'] = X.mv_k_A / X.val_k_A; X['mv_per_saver_m_A'] = X.mv_m_A / X.val_m_A
X.to_csv(O + 'fact2_gender_fundlevel.csv', index=False)

def agg(g):
    vk, vm = g.val_k_A.sum(), g.val_m_A.sum()
    ok = 100 * (vk - g.val_k_E.sum()) / vk; om = 100 * (vm - g.val_m_E.sum()) / vm
    ck = 100 * (g.mv_k_A.sum() - (g.mv_k_E / g.cumret).sum()) / g.mv_k_A.sum(); cm = 100 * (g.mv_m_A.sum() - (g.mv_m_E / g.cumret).sum()) / g.mv_m_A.sum()
    return pd.Series(dict(n_funds=len(g), savers_k=vk, savers_m=vm, share_women_pct=100 * vk / (vk + vm), months_med=g.n_months.median(),
                          optout_women_pct=ok, optout_men_pct=om, gap_m_minus_w_pp=om - ok, ratio_m_over_w=om / ok if ok != 0 else np.nan,
                          cap_out_women_pct=ck, cap_out_men_pct=cm, cap_gap_pp=cm - ck,
                          fund_mean_opt_w=g.opt_k.mean(), fund_mean_opt_m=g.opt_m.mean(), fund_median_gap=(g.opt_m - g.opt_k).median(),
                          n_funds_men_higher=int((g.opt_m > g.opt_k).sum()),
                          mv_per_saver_w=g.mv_k_A.sum() / vk, mv_per_saver_m=g.mv_m_A.sum() / vm))

T = X.groupby(['sample', 'round']).apply(agg).reset_index()
pooled = []
for s_, g in X.groupby('sample'):
    a = agg(g); a['sample'] = s_; a['round'] = 'POOLED'; pooled.append(a)
# FTN pooled excluding windows containing December (new pension rights inflate saver counts? no: Dec adds capital not savers; keep both)
g = X[(X['sample'] == 'FTN') & (~X.dec_in_window)]
a = agg(g); a['sample'] = 'FTN'; a['round'] = 'POOLED_exDecWindows'; pooled.append(a)
# FTN pooled, large losers only (>= 1bn at award)
g = X[(X['sample'] == 'FTN') & ((X.mv_k_A + X.mv_m_A) >= 1e9)]
a = agg(g); a['sample'] = 'FTN'; a['round'] = 'POOLED_losers_ge_1bn'; pooled.append(a)
T = pd.concat([T, pd.DataFrame(pooled)], ignore_index=True)
T.to_csv(O + 'fact2_gender_by_round.csv', index=False)
print(T.round(2).to_string())

# saver-weighted vs capital-weighted pooled is above; also fund-level: distribution of gap
ftn = X[X['sample'] == 'FTN']
print('FTN fund-level gap (men - women opt-out pp): mean', round((ftn.opt_m - ftn.opt_k).mean(), 2), 'median', round((ftn.opt_m - ftn.opt_k).median(), 2),
      'share funds men>women', round((ftn.opt_m > ftn.opt_k).mean(), 2), 'n', len(ftn))
pg = X[X['sample'] == 'purge2019_AP7']
print('2019 fund-level gap: mean', round((pg.opt_m - pg.opt_k).mean(), 2), 'median', round((pg.opt_m - pg.opt_k).median(), 2), 'share men>women', round((pg.opt_m > pg.opt_k).mean(), 2), 'n', len(pg))
# baseline attrition by gender in NON-treated equity funds over same calendar windows (FTN rounds): same window lengths, all other equity funds in the panel
EQ = ['Aktiefonder', 'Regionala fonder', 'Branschfonder', 'Länderfonder', 'Svenska Aktiefonder']
base = []
for rd, g in ftn.groupby('round'):
    A = pd.Timestamp(g.A.iloc[0]); E = pd.Timestamp(g.E.mode().iloc[0])
    treated = set(t1[t1['round'] == rd].fondnr)
    a = d[(d.date == A) & d.fondtyp.isin(EQ) & ~d.fondnr.isin(treated)][['fondnr', 'val_k', 'val_m']]
    e = d[(d.date == E) & d.fondtyp.isin(EQ)][['fondnr', 'val_k', 'val_m']]
    z = a.merge(e, on='fondnr', suffixes=('_A', '_E'))
    base.append(dict(round=rd, A=A.date(), E=E.date(), n_funds=len(z), base_optout_women_pct=100 * (z.val_k_A.sum() - z.val_k_E.sum()) / z.val_k_A.sum(),
                     base_optout_men_pct=100 * (z.val_m_A.sum() - z.val_m_E.sum()) / z.val_m_A.sum()))
B = pd.DataFrame(base); B['base_gap_pp'] = B.base_optout_men_pct - B.base_optout_women_pct
B.to_csv(O + 'fact2_gender_baseline_other_equity.csv', index=False)
print(B.round(2).to_string())
