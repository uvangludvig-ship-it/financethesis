"""FACT 3: share-class strategy of winners. Dedicated PPM class if fee_gross - fee_net < 0.03 pp at contract start (flag month + 1), else retail class with rebate.
PPM share of fund TNA (mv_tot / Morningstar tnafund) for SEK funds."""
from common import *
d = load_panel()
wm = pd.read_csv(F + 'agentB/winners_master.csv')
wm = wm[wm.in_panel & wm.first_flag_month.notna() & ~wm.ny.str.startswith('(panel flag only')].copy()  # drop duplicate-ISIN rows
wm['fondnr'] = wm.fondnr.astype(int)
bids = pd.read_csv(F + 'agentD/bids_long.csv')
bw = bids[bids.winner == 1][['round', 'fund_name', 'manager', 'new_to_platform', 'incumbent_in_category', 'ppm_fondnr_at_announce', 'tna_fund_ccy', 'tna_ccy', 'tna_fund_msek']]
xw = pd.read_csv(F + 'agentC/crosswalk_ppm_shof.csv')
ms = pd.read_csv('/mnt/user-data/uploads/financethesis_ny/data/derived/shof_monthly/shof_valuations_monthly.csv', usecols=['performanceId', 'ym', 'ccy_fund', 'tnafund'])
ms['date'] = pd.to_datetime(ms.ym) + pd.offsets.MonthEnd(0)
P = d.set_index(['fondnr', 'date']).sort_index()
AW = {'R1 Europe active': '2024-03-31', 'R2 Global index': '2024-10-31', 'R2 Europe index': '2024-10-31', 'R3 Nordic active': '2025-02-28', 'R3 Nordic small': '2025-02-28',
      'R4 Swedish active': '2025-08-31', 'R4 Swedish index': '2025-08-31', 'R6 Europe small': '2026-05-31', 'R6 Swedish small': '2026-05-31'}

def ppm_share(f, dt):
    r = xw[xw.fondnr == f]
    if len(r) == 0: return np.nan, 'no_xwalk'
    pid = r.performanceid.iloc[0]
    m = ms[(ms.performanceId == pid) & (ms.date == dt)]
    if len(m) == 0 or pd.isna(m.tnafund.iloc[0]): return np.nan, 'no_tna'
    if m.ccy_fund.iloc[0] != 'SEK': return np.nan, 'non_SEK:' + str(m.ccy_fund.iloc[0])
    try: mv = P.loc[(f, dt), 'mv_tot']
    except KeyError: return np.nan, 'no_ppm_month'
    return 100 * mv / m.tnafund.iloc[0], 'ok'

rows = []
for _, r in wm.iterrows():
    f = r.fondnr; fm = pd.Timestamp(r.first_flag_month); A = pd.Timestamp(AW[r['round']])
    c1 = fm + pd.offsets.MonthEnd(1)
    try: z = P.loc[(f, c1)]
    except KeyError:
        try: z = P.loc[(f, fm)]; c1 = fm
        except KeyError: continue
    try: b = P.loc[(f, A)]; fee_before = b.fee_net; gross_before = b.fee_gross; mv_award = b.mv_tot; val_award = b.val_tot
    except KeyError: fee_before = gross_before = mv_award = val_award = np.nan
    pre = fm - pd.offsets.MonthEnd(1)
    sh_pre, st_pre = ppm_share(f, A - pd.offsets.MonthEnd(1))
    last = d[d.fondnr == f].date.max()
    sh_last, st_last = ppm_share(f, min(last, pd.Timestamp('2026-06-30')))
    rows.append(dict(round=r['round'], fondnr=f, name=r['name'], ny=r.ny, fee_awarded=r.fee_awarded, contract_month=c1.date(),
                     fee_net_before=fee_before, fee_gross_before=gross_before, fee_net_after=z.fee_net, fee_gross_after=z.fee_gross, isin_after=z['isin'],
                     gap_after=z.fee_gross - z.fee_net, mv_award=mv_award, val_award=val_award,
                     ppm_share_pre_award_pct=sh_pre, ppm_share_pre_status=st_pre, ppm_share_latest_pct=sh_last, ppm_share_latest_status=st_last))
W = pd.DataFrame(rows)
W['class_type'] = np.where(W.gap_after < 0.03, 'PPM-dedicated class', 'retail class with rebate')
W['new_to_platform'] = (W.ny == 'Ja').astype(int)
W.to_csv(O + 'fact3_winners_shareclass.csv', index=False)
print(W.round(3).to_string())
print('\nshare of winners by class type per round:')
t = W.groupby(['round', 'class_type']).size().unstack(fill_value=0)
t['n'] = t.sum(axis=1); t['pct_dedicated'] = 100 * t.get('PPM-dedicated class', 0) / t.n
print(t.to_string())
print('\nby new_to_platform:')
t2 = W.groupby(['new_to_platform', 'class_type']).size().unstack(fill_value=0); print(t2)
print('\nmean PPM share of TNA by class type (SEK funds only):')
for col in ['ppm_share_pre_award_pct', 'ppm_share_latest_pct']:
    print(col); print(W.groupby('class_type')[col].agg(['count', 'mean', 'median']).round(1))
print('\nincumbents only, pre-award PPM share by class type:')
inc = W[(W.new_to_platform == 0) & W.ppm_share_pre_award_pct.notna()]
print(inc.groupby('class_type').ppm_share_pre_award_pct.agg(['count', 'mean', 'median']).round(1))
inc = inc.assign(retail_base_large=inc.ppm_share_pre_award_pct < 50)
print(pd.crosstab(inc.retail_base_large, inc.class_type))
print(W.ppm_share_pre_status.value_counts(), W.ppm_share_latest_status.value_counts())
summ = pd.concat([t.reset_index().assign(table='by_round'),
                  W.groupby('class_type').agg(n=('fondnr', 'size'), n_new=('new_to_platform', 'sum'), mean_gap=('gap_after', 'mean'), mean_fee_after=('fee_net_after', 'mean'),
                                              mean_ppm_share_pre=('ppm_share_pre_award_pct', 'mean'), n_share_pre=('ppm_share_pre_award_pct', 'count'),
                                              mean_ppm_share_latest=('ppm_share_latest_pct', 'mean'), n_share_latest=('ppm_share_latest_pct', 'count')).reset_index().assign(table='by_class')])
summ.to_csv(O + 'fact3_summary.csv', index=False)
