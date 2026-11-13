import pandas as pd, numpy as np
S = '/tmp/claude-0/-home-claude/5b447583-b5ae-51ff-a30e-274749b6d7af/scratchpad/'
O = S + 'ftn/agentA/'
d = pd.read_csv(S + 'ftn/ppm_panel_2022_2026.csv', parse_dates=['date'])
d = d[~d.fondnr.isin([1, 2, 3, 4]) & ~d.fondnamn.str.contains('AP7', na=False)]
l = pd.read_csv(S + 'xls/lista.csv'); l = l[l.FONDNAMN != '#REF!']
l['FONDNUMMER'] = l.FONDNUMMER.astype('Int64')
avsl = l.set_index('FONDNUMMER').AVSLUTSDATUM
stat = l.set_index('FONDNUMMER').FONDSTATUS
months = sorted(d.date.unique())
END = months[-1]

# incumbents per FTN report sec 4.1, W = incumbent awarded; new_w = winners new to PPM (or new share class/fund)
R = {
 'EU_active': dict(award='2024-03-31', inc={336826:0,916122:0,696898:0,309492:0,901181:0,764951:0,814947:0,566556:0,899773:0,899352:0,848770:0,
                    492306:0,564849:0,810465:0,755090:0,122432:0,666495:0,865063:0,367698:0,238832:0,538462:1},  # Odin Europa 280867 left Feb-24 (pre-award)
                   new_w=[124438,196097,988600,160267,952770]),
 'EU_index': dict(award='2024-10-31', inc={219170:0,629543:1,479840:0,654459:1,140673:1,755504:1,570630:0}, new_w=[]),
 'Global_index': dict(award='2024-10-31', inc={680124:0,252411:0,613729:0,362491:0,785907:1,199753:0,658997:0,114819:1,545426:1,407064:0,393488:0},
                    new_w=[491233,343665,527060]),
 'Nordic_active': dict(award='2025-02-28', inc={147512:0,811117:0,354290:0,861757:1,598557:0,484923:1,484980:0,388298:0,820852:0,521104:1},
                    new_w=[674630]),
 'Nordic_smallcap': dict(award='2025-02-28', inc={339473:0,785493:0,237834:1,751495:1,286294:1}, new_w=[710467]),
 'SE_active': dict(award='2025-08-31', inc={344739:0,681783:1,393314:1,291906:1,792697:0,973263:0,916189:0,106849:0,904904:0,146928:0,490292:0,
                    806869:0,528133:0,203067:0,450981:0,643700:0,328021:0,158261:0,846527:0,339184:0,272898:0,976928:1},
                    new_w=[423822,459652,495482,531310,567140,607226]),
 'SE_index': dict(award='2025-08-31', inc={734491:0,290072:1,528894:0,610410:0,465914:1,577833:0,587337:0,292193:0,212332:0,357658:0,719674:1},
                    new_w=[638809,602979]),
 'EU_smallcap': dict(award='2026-05-31', inc={538751:0,250167:0,182759:0,556589:1,896761:1}, new_w=[571399,535569]),
 'SE_smallcap': dict(award='2026-05-31', inc={269357:1,712299:0,721035:0,584912:0,140491:1,420463:0,952010:1,842690:1,694539:0,416867:0,515676:0,
                    103606:0,152181:0,856682:1}, new_w=[392241,356410,463901,428078,499731]),
}
award_day = {'EU_active':'2024-03-25','EU_index':'2024-10-31','Global_index':'2024-10-31','Nordic_active':'2025-02-19','Nordic_smallcap':'2025-02-19',
             'SE_active':'2025-08-27','SE_index':'2025-08-27','EU_smallcap':'2026-05-28','SE_smallcap':'2026-05-28'}

P = d.set_index(['fondnr', 'date']).sort_index()
rows1, rows2, rows3 = [], [], []
for r, c in R.items():
    A = pd.Timestamp(c['award'])
    for f, w in list(c['inc'].items()) + [(f, 2) for f in c['new_w']]:
        x = d[d.fondnr == f].sort_values('date')
        a = x[x.date == A]
        rows1.append(dict(round=r, award=award_day[r], fondnr=f, fondnamn=x.fondnamn.iloc[-1], kategori=x.kategori.iloc[-1],
                          role={0: 'loser', 1: 'winner_incumbent', 2: 'winner_new'}[w],
                          mv_award=a.mv_tot.iloc[0] if len(a) else np.nan, val_award=a.val_tot.iloc[0] if len(a) else np.nan,
                          first_month=x.date.min().date(), last_month=x.date.max().date(),
                          avslutsdatum=avsl.get(f, np.nan), fondstatus=stat.get(f, np.nan)))
        if w == 0:
            L = x.date.max()
            exited = L < END
            post = x[(x.date > A) & (x.date <= L)]
            pre_last = x[x.date == L].iloc[0]
            dec = post[post.date.dt.month.isin([12, 1])]
            rows2.append(dict(round=r, fondnr=f, fondnamn=pre_last.fondnamn, exited=exited,
                              last_month=L.date(), exit_month=(L + pd.offsets.MonthEnd(1)).date() if exited else None,
                              avslutsdatum=avsl.get(f, np.nan),
                              months_award_to_last=len(post),
                              mv_award=a.mv_tot.iloc[0], mv_last=pre_last.mv_tot,
                              hn_award_month=a.handel_netto.iloc[0],
                              hn_post_sum=post.handel_netto.sum(), hn_post_decjan=dec.handel_netto.sum(),
                              val_award=a.val_tot.iloc[0], val_last=pre_last.val_tot,
                              ret_component=pre_last.mv_tot - a.mv_tot.iloc[0] - post.handel_netto.sum()))
        # monthly series for winners (and losers) award-3 .. end
        for _, z in x[x.date >= A - pd.offsets.MonthEnd(3)].iterrows():
            rows3.append(dict(round=r, role={0: 'loser', 1: 'winner_incumbent', 2: 'winner_new'}[w], fondnr=f, fondnamn=z.fondnamn,
                              date=z.date.date(), mv_tot=z.mv_tot, val_tot=z.val_tot, handel_netto=z.handel_netto,
                              december_flag=z.date.month in (12, 1)))
t1 = pd.DataFrame(rows1); t2 = pd.DataFrame(rows2); t3 = pd.DataFrame(rows3)
t2['vol_out'] = -t2.hn_post_sum
t2['vol_out_exDecJan'] = -(t2.hn_post_sum - t2.hn_post_decjan)
t2['default_mv'] = np.where(t2.exited, t2.mv_last, np.nan)
t2['sav_vol'] = t2.val_award - t2.val_last
t2['sav_default'] = np.where(t2.exited, t2.val_last, np.nan)
t1.to_csv(O + 'task1_round_membership.csv', index=False)
t2.to_csv(O + 'task2_loser_decomposition.csv', index=False)
t3.to_csv(O + 'task3_monthly_flows_winners_losers.csv', index=False)

# round summary (exited losers only for shares)
g = []
for r, c in R.items():
    T1 = t1[t1['round'] == r]; T2 = t2[t2['round'] == r]; E = T2[T2.exited]
    vol, dfl = E.vol_out.sum(), E.default_mv.sum()
    vx = E.vol_out_exDecJan.sum()
    sv, sd = E.sav_vol.sum(), E.sav_default.sum()
    g.append(dict(round=r, award=award_day[r], n_inc=(T1.role != 'winner_new').sum(), n_win=(T1.role != 'loser').sum(),
                  n_win_inc=(T1.role == 'winner_incumbent').sum(), n_win_new=(T1.role == 'winner_new').sum(),
                  n_los=len(T2), n_los_exited=len(E),
                  mv_inc_bn=T1[T1.role != 'winner_new'].mv_award.sum() / 1e9, mv_los_bn=T2.mv_award.sum() / 1e9,
                  mv_los_exited_bn=E.mv_award.sum() / 1e9,
                  vol_bn=vol / 1e9, default_bn=dfl / 1e9, pct_vol_cap=100 * vol / (vol + dfl), pct_vol_cap_exDecJan=100 * vx / (vx + dfl),
                  sav_los_award=E.val_award.sum(), sav_vol=sv, sav_default=sd, pct_vol_sav=100 * sv / (sv + sd),
                  months_med=E.months_award_to_last.median(), months_min=E.months_award_to_last.min(), months_max=E.months_award_to_last.max()))
G = pd.DataFrame(g)
G.to_csv(O + 'summary_by_round.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 300)
print(G.round(2).to_string())
print(t2[['round', 'fondnr', 'fondnamn', 'exited', 'last_month', 'avslutsdatum', 'months_award_to_last', 'mv_award', 'mv_last', 'hn_award_month', 'vol_out', 'hn_post_decjan', 'val_award', 'val_last']]
      .assign(mv_award=lambda z: (z.mv_award / 1e6).round(0), mv_last=lambda z: (z.mv_last / 1e6).round(0), vol_out=lambda z: (z.vol_out / 1e6).round(0),
              hn_award_month=lambda z: (z.hn_award_month / 1e6).round(0), hn_post_decjan=lambda z: (z.hn_post_decjan / 1e6).round(0)).to_string())

# ---------- refined decomposition: detect forced-tranche months ----------
rows = []
for r, c in R.items():
    A = pd.Timestamp(c['award'])
    for f, w in c['inc'].items():
        if w: continue
        x = d[d.fondnr == f].sort_values('date').set_index('date')
        L = x.index.max(); exited = L < END
        x['mv_l'] = x.mv_tot.shift(); x['val_l'] = x.val_tot.shift()
        x['hn_rel'] = x.handel_netto / x.mv_l; x['val_rel'] = x.val_tot / x.val_l - 1
        post = x[x.index > A]
        forced = post[((post.hn_rel < -0.10) & (post.val_rel > 0.5 * post.hn_rel)) | (post.hn_rel < -0.80)]
        M = forced.index.min() if len(forced) else L + pd.offsets.MonthEnd(1)
        pre = post[post.index < M]
        Mm1 = x[x.index < M].index.max()
        vol = -pre.handel_netto.sum(); vol_exdec = -pre[pre.index.month != 12].handel_netto.sum()
        dflt = x.loc[Mm1, 'mv_tot']
        rows.append(dict(round=r, fondnr=f, fondnamn=x.fondnamn.iloc[-1], exited=exited, last_month=L.date(),
                         avslutsdatum=avsl.get(f, np.nan),
                         move_start=M.date(), n_tranche_months=len(post[post.index >= M]),
                         months_award_to_move=len(pre) + 1,
                         mv_award=x.loc[A, 'mv_tot'], val_award=x.loc[A, 'val_tot'],
                         vol_out=vol, vol_out_exDec=vol_exdec, dec_hn_pre=pre[pre.index.month == 12].handel_netto.sum(),
                         default_mv=dflt, val_at_move=x.loc[Mm1, 'val_tot'], val_last=x.loc[L, 'val_tot'], mv_last=x.loc[L, 'mv_tot'],
                         hn_tranche_months=post[post.index >= M].handel_netto.sum()))
t2b = pd.DataFrame(rows)
t2b['sav_vol'] = t2b.val_award - t2b.val_at_move
t2b['pct_vol_cap'] = 100 * t2b.vol_out / (t2b.vol_out + t2b.default_mv)
t2b.to_csv(O + 'task2_loser_decomposition.csv', index=False)
g = []
for r in R:
    E = t2b[(t2b['round'] == r)]
    for lab, EE in [('exited', E[E.exited]), ('all_incl_pending', E)]:
        if len(EE) == 0: continue
        v, df_, vx = EE.vol_out.sum(), EE.default_mv.sum(), EE.vol_out_exDec.sum()
        sv, sd = EE.sav_vol.sum(), EE.val_at_move.sum()
        g.append(dict(round=r, sample=lab, n_los=len(EE), mv_award_bn=EE.mv_award.sum()/1e9, vol_bn=v/1e9, default_bn=df_/1e9,
                      pct_vol_cap=100*v/(v+df_), pct_vol_cap_exDec=100*vx/(vx+df_), sav_award=EE.val_award.sum(), sav_vol=sv, sav_default=sd,
                      pct_vol_sav=100*sv/(sv+sd), med_months_award_to_move=EE.months_award_to_move.median(),
                      max_tranche_months=EE.n_tranche_months.max()))
G2 = pd.DataFrame(g)
tot = []
for lab, EE in [('TOTAL exited (rounds to Aug-25 + EU smallcap)', t2b[t2b.exited]), ('TOTAL incl Avanza Zero/pending', t2b[t2b['round'] != 'SE_smallcap'])]:
    v, df_, vx = EE.vol_out.sum(), EE.default_mv.sum(), EE.vol_out_exDec.sum(); sv, sd = EE.sav_vol.sum(), EE.val_at_move.sum()
    tot.append(dict(round=lab, sample='', n_los=len(EE), mv_award_bn=EE.mv_award.sum()/1e9, vol_bn=v/1e9, default_bn=df_/1e9,
                    pct_vol_cap=100*v/(v+df_), pct_vol_cap_exDec=100*vx/(vx+df_), sav_award=EE.val_award.sum(), sav_vol=sv, sav_default=sd, pct_vol_sav=100*sv/(sv+sd)))
G2 = pd.concat([G2, pd.DataFrame(tot)])
G2.to_csv(O + 'summary_by_round.csv', index=False)
print(G2.round(2).to_string())
print(t2b[['round','fondnamn','exited','move_start','n_tranche_months','months_award_to_move','pct_vol_cap','sav_vol','val_at_move']].round(1).to_string())

# ---------- task 3: winners' flows around loser move window ----------
W = []
for r, c in R.items():
    E = t2b[(t2b['round'] == r)]
    if len(E) == 0: continue
    win = [f for f, w in c['inc'].items() if w] + c['new_w']
    A = pd.Timestamp(c['award'])
    los = [f for f, w in c['inc'].items() if not w]
    end = min(pd.Timestamp(max(E.last_month)) + pd.offsets.MonthEnd(1), END)
    for f in win + los:
        x = d[(d.fondnr == f) & (d.date > A) & (d.date <= end)]
        W.append(dict(round=r, role='winner' if f in win else 'loser', fondnr=f, fondnamn=d[d.fondnr == f].fondnamn.iloc[-1],
                      hn_sum_award_to_exit_plus1=x.handel_netto.sum(), hn_dec=x[x.date.dt.month == 12].handel_netto.sum(),
                      window=f'{(A + pd.offsets.MonthEnd(1)).date()}..{end.date()}'))
W = pd.DataFrame(W)
W.to_csv(O + 'task3_winner_inflows_window.csv', index=False)
s = W.groupby(['round', 'role']).hn_sum_award_to_exit_plus1.sum().unstack() / 1e9
s['winner_capture_pct'] = -100 * s.winner / s.loser
print(s.round(2))
print(W[W.role == 'winner'].assign(bn=lambda z: (z.hn_sum_award_to_exit_plus1/1e9).round(2))[['round','fondnamn','bn','window']].to_string())
