"""FACT 1: Global active round (award 24 Feb 2026, appealed, no default move by Aug 2026).
Monthly net trade as % of lagged MV and saver change for losers vs own pre-period vs winners vs other rounds' losers pre-move."""
from common import *
d = load_panel(); t1, t2 = load_rounds()
A = GA_AWARD_ME
inc = [f for f in GA_INCUMBENTS if f != 294322]  # AXA left Oct 2025
present = d[(d.date == A) & d.fondnr.isin(inc)].fondnr.tolist()
losers = [f for f in present if f not in GA_WINNERS_INC]
winners = [f for f in present if f in GA_WINNERS_INC]
print('GA incumbents present at award:', len(present), 'losers:', len(losers), 'winners_inc:', len(winners))
x = d[d.fondnr.isin(present)].copy()
x['role'] = np.where(x.fondnr.isin(losers), 'GA_loser', 'GA_winner_inc')
x['window'] = np.select([(x.date >= '2025-09-30') & (x.date <= '2026-01-31'), x.date == A, (x.date >= '2026-03-31') & (x.date <= '2026-08-31')],
                        ['pre_Sep25_Jan26', 'award_Feb26', 'post_Mar26_Aug26'], 'other')
x['dval'] = x.val_tot - x.val_lag

# --- fund-month table (pooled = sum hn / sum lagged mv) ---
mm = x[x.window != 'other'].groupby(['role', 'window', 'date']).agg(n=('fondnr', 'size'), hn=('handel_netto', 'sum'), mv_lag=('mv_lag', 'sum'),
                                                                     val=('val_tot', 'sum'), val_lag=('val_lag', 'sum'), is_dec=('is_dec', 'first')).reset_index()
mm['hn_pct_mv'] = 100 * mm.hn / mm.mv_lag
mm['dval_pct'] = 100 * (mm.val - mm.val_lag) / mm.val_lag
# fund-level median
fl = x[x.window != 'other'].assign(hn_pct=lambda z: 100 * z.handel_netto / z.mv_lag, dv_pct=lambda z: 100 * z.dval / z.val_lag)
med = fl.groupby(['role', 'window', 'date']).agg(med_hn_pct=('hn_pct', 'median'), med_dv_pct=('dv_pct', 'median')).reset_index()
mm = mm.merge(med, on=['role', 'window', 'date'])
mm.to_csv(O + 'fact1_GA_monthly.csv', index=False)
print(mm.round(3).to_string())

# window summary: mean monthly %, ex-December
summ = mm.groupby(['role', 'window']).apply(lambda g: pd.Series(dict(n_months=len(g), mean_hn_pct=g.hn_pct_mv.mean(), mean_hn_pct_exDec=g[~g.is_dec].hn_pct_mv.mean(),
                                                                       mean_dval_pct=g.dval_pct.mean(), med_fund_hn_pct=g.med_hn_pct.mean()))).reset_index()
print(summ.round(3).to_string())

# --- cumulative voluntary outflow by event month 1..6 after award: GA losers vs other rounds' losers (months before their move start M) ---
rows = []
# GA
ga_mv0 = x[(x.date == A) & (x.role == 'GA_loser')].mv_tot.sum(); ga_v0 = x[(x.date == A) & (x.role == 'GA_loser')].val_tot.sum()
post = x[(x.role == 'GA_loser') & (x.date > A)].groupby('date').agg(hn=('handel_netto', 'sum'), val=('val_tot', 'sum'), n=('fondnr', 'size')).reset_index()
post['m'] = range(1, len(post) + 1)
post['cum_hn_pct'] = 100 * post.hn.cumsum() / ga_mv0
post['cum_dval_pct'] = 100 * (post.val - ga_v0) / ga_v0
for _, r in post.iterrows():
    rows.append(dict(group='Global_active (appeal, no move)', m=int(r.m), n_funds=r.n, cum_hn_pct=r.cum_hn_pct, cum_hn_pct_exDec=r.cum_hn_pct, cum_dval_pct=r.cum_dval_pct, dec_in_window=False, all_losers_unmoved=True))
# clean: exclude Evli Global (merger receiver Aug 2026, +0.78bn into a 6.5m fund)
xc = x[(x.role == 'GA_loser') & (x.fondnr != 793109)]
c_mv0 = xc[xc.date == A].mv_tot.sum(); c_v0 = xc[xc.date == A].val_tot.sum()
pc = xc[xc.date > A].groupby('date').agg(hn=('handel_netto', 'sum'), val=('val_tot', 'sum'), n=('fondnr', 'size')).reset_index()
for i, r in pc.iterrows():
    rows.append(dict(group='Global_active ex Evli (merger receiver)', m=i + 1, n_funds=r.n, cum_hn_pct=100 * pc.hn[:i + 1].sum() / c_mv0, cum_hn_pct_exDec=100 * pc.hn[:i + 1].sum() / c_mv0, cum_dval_pct=100 * (r.val - c_v0) / c_v0, dec_in_window=False, all_losers_unmoved=True))
# GA winners for reference
ga_wmv0 = x[(x.date == A) & (x.role == 'GA_winner_inc')].mv_tot.sum(); ga_wv0 = x[(x.date == A) & (x.role == 'GA_winner_inc')].val_tot.sum()
postw = x[(x.role == 'GA_winner_inc') & (x.date > A)].groupby('date').agg(hn=('handel_netto', 'sum'), val=('val_tot', 'sum'), n=('fondnr', 'size')).reset_index()
postw['m'] = range(1, len(postw) + 1)
for _, r in postw.iterrows():
    rows.append(dict(group='Global_active winners_inc', m=int(r.m), n_funds=r.n, cum_hn_pct=100 * postw.hn[:int(r.m)].sum() / ga_wmv0, cum_hn_pct_exDec=100 * postw.hn[:int(r.m)].sum() / ga_wmv0, all_losers_unmoved=True, cum_dval_pct=100 * (r.val - ga_wv0) / ga_wv0, dec_in_window=False))
# other rounds: losers, event months after award while date < move_start (fund-specific M)
for rd, Ame in AWARD_ME.items():
    Ame = pd.Timestamp(Ame)
    L = t2[t2['round'] == rd]
    y = d[d.fondnr.isin(L.fondnr)].merge(L[['fondnr', 'move_start', 'mv_award', 'val_award']], on='fondnr')
    y = y[(y.date > Ame) & (y.date < y.move_start)]
    if len(y) == 0: continue
    y['m'] = ((y.date.dt.year - Ame.year) * 12 + y.date.dt.month - Ame.month)
    mv0 = L.mv_award.sum(); v0 = L.val_award.sum()
    for m in sorted(y.m.unique()):
        z = y[y.m <= m]; nowf = y[y.m == m]
        # only count event-month m if all losers of the round are still unmoved (otherwise the sample changes)
        full = nowf.fondnr.nunique() == len(L)
        rows.append(dict(group=rd, m=int(m), n_funds=nowf.fondnr.nunique(), cum_hn_pct=100 * z.handel_netto.sum() / mv0, cum_hn_pct_exDec=100 * z[~z.is_dec].handel_netto.sum() / mv0,
                         cum_dval_pct=100 * (nowf.val_tot.sum() + L[~L.fondnr.isin(nowf.fondnr)].val_award.sum() - v0) / v0,
                         dec_in_window=bool(z.is_dec.any()), all_losers_unmoved=full))
cum = pd.DataFrame(rows)
cum.to_csv(O + 'fact1_cum_outflow_by_event_month.csv', index=False)
piv = cum.pivot(index='group', columns='m', values='cum_hn_pct').round(2)
print(piv.to_string())
other = cum[~cum.group.str.startswith('Global_active') & (cum.all_losers_unmoved == True)]
print('mean other rounds cum_hn_pct by m:\n', other.groupby('m').cum_hn_pct.agg(['mean', 'median', 'count']).round(2))
print('mean other rounds cum_hn_pct_exDec by m:\n', other.groupby('m').cum_hn_pct_exDec.agg(['mean', 'median', 'count']).round(2))
print(cum.pivot(index='group', columns='m', values='cum_hn_pct_exDec').round(2).to_string())
print('mean other rounds cum_dval_pct by m:\n', other.groupby('m').cum_dval_pct.agg(['mean', 'median', 'count']).round(2))
print(cum.pivot(index='group', columns='m', values='cum_dval_pct').round(2).to_string())
# fund-level for GA losers: cumulative % Mar-Aug 2026 by fund
fl2 = x[(x.role == 'GA_loser') & (x.date > A)].groupby(['fondnr', 'fondnamn']).agg(hn=('handel_netto', 'sum')).reset_index()
fl2 = fl2.merge(x[(x.date == A)][['fondnr', 'mv_tot', 'val_tot', 'fee_net']], on='fondnr')
fl2 = fl2.merge(x[(x.date == '2026-08-31')][['fondnr', 'val_tot']].rename(columns={'val_tot': 'val_aug26'}), on='fondnr', how='left')
fl2['cum_hn_pct'] = 100 * fl2.hn / fl2.mv_tot; fl2['dval_pct'] = 100 * (fl2.val_aug26 - fl2.val_tot) / fl2.val_tot
fl2.sort_values('mv_tot', ascending=False).to_csv(O + 'fact1_GA_losers_fundlevel.csv', index=False)
print(fl2.sort_values('mv_tot', ascending=False).round(2).to_string())
print('GA losers mv at award (bn):', ga_mv0 / 1e9, 'savers:', ga_v0, '| median fund cum_hn_pct:', fl2.cum_hn_pct.median(), 'capital-weighted:', 100 * fl2.hn.sum() / fl2.mv_tot.sum())
# same-calendar control: all other non-procured equity funds Mar-Aug 2026 (category not in procured set), pooled
proc_cats = ['Europa', 'Global', 'Norden', 'Norden småbolag', 'Sverige', 'Europa småbolag', 'Sverige småbolag', 'Global och Sverige', 'IT och kommunikation']
EQ = ['Aktiefonder','Regionala fonder','Branschfonder','Länderfonder','Svenska Aktiefonder']
ctrl = d[d.fondtyp.isin(EQ) & ~d.kategori.isin(proc_cats) & (d.date > A) & (d.date <= '2026-08-31')]
c = ctrl.groupby('date').agg(hn=('handel_netto', 'sum'), mv_lag=('mv_lag', 'sum'))
print('control (other equity categories) monthly hn % Mar-Aug26:', (100 * c.hn / c.mv_lag).round(3).tolist(), 'cum:', round(100 * c.hn.sum() / ctrl[ctrl.date == '2026-03-31'].mv_lag.sum(), 2))
cp = d[d.fondtyp.isin(EQ) & ~d.kategori.isin(proc_cats) & (d.date >= '2025-09-30') & (d.date <= '2026-01-31')]
c2 = cp.groupby('date').agg(hn=('handel_netto', 'sum'), mv_lag=('mv_lag', 'sum'))
print('control Sep25-Jan26 monthly hn %:', (100 * c2.hn / c2.mv_lag).round(3).tolist())

# control: fund-level median cumulative Mar-Aug 2026 for equity funds in non-procured categories present at Feb 2026 and Aug 2026
cf = ctrl.groupby('fondnr').agg(hn=('handel_netto', 'sum'), n=('date', 'size')).reset_index()
cf = cf.merge(d[d.date == A][['fondnr', 'mv_tot', 'val_tot']], on='fondnr').merge(d[d.date == '2026-08-31'][['fondnr', 'val_tot']].rename(columns={'val_tot': 'val_aug'}), on='fondnr')
cf = cf[cf.n == 6]
cf['cum_hn_pct'] = 100 * cf.hn / cf.mv_tot; cf['dval_pct'] = 100 * (cf.val_aug - cf.val_tot) / cf.val_tot
print('control equity funds (non-procured categories, present whole window): n=', len(cf), 'median cum_hn_pct', round(cf.cum_hn_pct.median(), 2), 'median dval_pct', round(cf.dval_pct.median(), 2),
      'pooled cum_hn_pct', round(100 * cf.hn.sum() / cf.mv_tot.sum(), 2), 'pooled dval', round(100 * (cf.val_aug.sum() - cf.val_tot.sum()) / cf.val_tot.sum(), 2))
pd.DataFrame([dict(group='GA_losers', n=len(fl2), median_cum_hn_pct=fl2.cum_hn_pct.median(), pooled_cum_hn_pct=100 * fl2.hn.sum() / fl2.mv_tot.sum(), median_dval_pct=fl2.dval_pct.median(), pooled_dval_pct=100 * (fl2.val_aug26.sum() - fl2.val_tot.sum()) / fl2.val_tot.sum()),
              dict(group='GA_losers_exEvli', n=len(fl2) - 1, median_cum_hn_pct=fl2[fl2.fondnr != 793109].cum_hn_pct.median(), pooled_cum_hn_pct=100 * fl2[fl2.fondnr != 793109].hn.sum() / fl2[fl2.fondnr != 793109].mv_tot.sum(), median_dval_pct=fl2[fl2.fondnr != 793109].dval_pct.median(), pooled_dval_pct=100 * (fl2[fl2.fondnr != 793109].val_aug26.sum() - fl2[fl2.fondnr != 793109].val_tot.sum()) / fl2[fl2.fondnr != 793109].val_tot.sum()),
              dict(group='control_equity_nonprocured', n=len(cf), median_cum_hn_pct=cf.cum_hn_pct.median(), pooled_cum_hn_pct=100 * cf.hn.sum() / cf.mv_tot.sum(), median_dval_pct=cf.dval_pct.median(), pooled_dval_pct=100 * (cf.val_aug.sum() - cf.val_tot.sum()) / cf.val_tot.sum())]
             ).to_csv(O + 'fact1_GA_vs_control_Mar_Aug26.csv', index=False)
