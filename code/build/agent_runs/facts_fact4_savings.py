"""FACT 4: annual fee savings in SEK per round, split into (a) stayers in incumbent winners (fee cut on existing capital) and
(b) capital moved from losers to winners (loser fee before minus winner fee after). Fees = PPM fee_net (after rebate), % per year."""
from common import *
d = load_panel(); t1, t2 = load_rounds()
P = d.set_index(['fondnr', 'date']).sort_index()
cat = pd.read_csv(F + 'agentB/ftn_category_fees.csv')
CATMAP = {'EU_active': 'Europe active', 'EU_index': 'Europe index', 'Global_index': 'Global index', 'Nordic_active': 'Nordic active', 'Nordic_smallcap': 'Nordic small',
          'SE_active': 'Swedish active', 'SE_index': 'Swedish index', 'EU_smallcap': 'Europe small', 'SE_smallcap': 'Swedish small'}
winflow = pd.read_csv(F + 'agentA/task3_winner_inflows_window.csv'); winflow = winflow[winflow.role == 'winner']

def fee_at(f, dt):
    try: return P.loc[(f, dt), 'fee_net']
    except KeyError: return np.nan

rows_w, rows_l, out = [], [], []
for rd, Ame in AWARD_ME.items():
    A = pd.Timestamp(Ame)
    W = t1[(t1['round'] == rd) & (t1.role != 'loser')].copy()
    L = t2[t2['round'] == rd].copy()
    # winner fee after: first flagged month + 1 (or first flagged month if that is the last obs); fee before (incumbents): award month
    wr = []
    for _, w in W.iterrows():
        x = d[d.fondnr == w.fondnr]
        fl = x[x.upphandlad == 'Upphandlad'].date.min()
        if pd.isna(fl):
            continue
        c1 = fl + pd.offsets.MonthEnd(1)
        fa = fee_at(w.fondnr, c1)
        if pd.isna(fa): fa = fee_at(w.fondnr, fl); c1 = fl
        fb = fee_at(w.fondnr, A) if w.role == 'winner_incumbent' else np.nan
        mv_a = w.mv_award if w.role == 'winner_incumbent' else np.nan; val_a = w.val_award if w.role == 'winner_incumbent' else np.nan
        # stayers: savers still in fund at contract month (<= val at award) -- use val at award as 'affected' (fee cut applies to all who are there)
        inflow = winflow[(winflow['round'] == rd) & (winflow.fondnr == w.fondnr)].hn_sum_award_to_exit_plus1.sum()
        wr.append(dict(round=rd, fondnr=w.fondnr, fondnamn=w.fondnamn, role=w.role, flag_month=fl.date(), contract_month=c1.date(), fee_before=fb, fee_after=fa,
                       mv_award=mv_a, val_award=val_a, inflow_window=max(inflow, 0.0),
                       saving_a_sek=(mv_a * (fb - fa) / 100) if w.role == 'winner_incumbent' else 0.0))
    wr = pd.DataFrame(wr); rows_w.append(wr)
    fee_after_ew = wr.fee_after.mean()
    fee_after_iw = np.average(wr.fee_after, weights=wr.inflow_window) if wr.inflow_window.sum() > 0 else np.nan
    # losers: moved capital default_mv at loser fee before (award month) -> winner fee after (inflow-weighted)
    lr = []
    for _, l in L.iterrows():
        fb = fee_at(l.fondnr, A)
        lr.append(dict(round=rd, fondnr=l.fondnr, fondnamn=l.fondnamn, fee_before=fb, default_mv=l.default_mv, val_at_move=l.val_at_move, vol_out=l.vol_out, sav_vol=l.sav_vol,
                       exited=l.exited, saving_b_sek_iw=l.default_mv * (fb - fee_after_iw) / 100, saving_b_sek_ew=l.default_mv * (fb - fee_after_ew) / 100))
    lr = pd.DataFrame(lr); rows_l.append(lr)
    c = cat[cat.category == CATMAP[rd]].iloc[0]
    inc_mv = t1[(t1['round'] == rd) & (t1.role != 'winner_new')].mv_award.sum()
    out.append(dict(round=rd, award=Ame, n_win_inc=(wr.role == 'winner_incumbent').sum(), n_win_new=(wr.role == 'winner_new').sum(), n_losers=len(lr),
                    cap_inc_winners_bn=wr.mv_award.sum() / 1e9, fee_inc_before_cw=np.average(wr.fee_before.dropna(), weights=wr.mv_award.dropna()) if wr.mv_award.notna().any() else np.nan,
                    fee_inc_after_cw=np.average(wr[wr.role == 'winner_incumbent'].fee_after, weights=wr[wr.role == 'winner_incumbent'].mv_award) if (wr.role == 'winner_incumbent').any() else np.nan,
                    saving_a_msek=wr.saving_a_sek.sum() / 1e6, savers_a=wr.val_award.sum(),
                    cap_moved_bn=lr.default_mv.sum() / 1e9, fee_losers_before_cw=np.average(lr.fee_before, weights=lr.default_mv), fee_winners_after_ew=fee_after_ew, fee_winners_after_iw=fee_after_iw,
                    saving_b_msek_iw=lr.saving_b_sek_iw.sum() / 1e6, saving_b_msek_ew=lr.saving_b_sek_ew.sum() / 1e6, savers_b=lr.val_at_move.sum(),
                    cap_left_voluntarily_bn=lr.vol_out.sum() / 1e9, savers_left_voluntarily=lr.sav_vol.sum(),
                    ftn_fee_before_ew=c.fee_before_ew_after_rebate_s42, ftn_fee_after_avg=c.fee_after_avg_procured_s62, ftn_cap_category_bn=inc_mv / 1e9,
                    ftn_check_saving_msek=inc_mv * (c.fee_before_ew_after_rebate_s42 - c.fee_after_avg_procured_s62) / 100 / 1e6,
                    pending=rd in ('EU_smallcap', 'SE_smallcap')))
Wd = pd.concat(rows_w); Ld = pd.concat(rows_l); S_ = pd.DataFrame(out)
S_['saving_total_msek'] = S_.saving_a_msek + S_.saving_b_msek_iw
S_['savers_affected'] = S_.savers_a + S_.savers_b
S_['sek_per_saver_a'] = 1e6 * S_.saving_a_msek / S_.savers_a
S_['sek_per_saver_b'] = 1e6 * S_.saving_b_msek_iw / S_.savers_b
S_['sek_per_saver_total'] = 1e6 * S_.saving_total_msek / S_.savers_affected
Wd.to_csv(O + 'fact4_winners_fees.csv', index=False); Ld.to_csv(O + 'fact4_losers_moved.csv', index=False); S_.to_csv(O + 'fact4_savings_by_round.csv', index=False)
print(Wd.round(3).to_string()); print(Ld.round(2).to_string())
print(S_.round(2).T.to_string())
exe = S_[~S_.pending]
for lab, Z in [('executed rounds (to SE_index)', exe), ('all incl. pending smallcap', S_)]:
    print(lab, '| saving a (stayers) MSEK/yr:', round(Z.saving_a_msek.sum(), 1), 'savers', int(Z.savers_a.sum()), '| saving b (moved) MSEK/yr:', round(Z.saving_b_msek_iw.sum(), 1),
          '(ew:', round(Z.saving_b_msek_ew.sum(), 1), ') savers', int(Z.savers_b.sum()), '| total MSEK/yr', round(Z.saving_total_msek.sum(), 1),
          '| SEK/saver/yr: a', round(1e6 * Z.saving_a_msek.sum() / Z.savers_a.sum()), 'b', round(1e6 * Z.saving_b_msek_iw.sum() / Z.savers_b.sum()), 'all', round(1e6 * Z.saving_total_msek.sum() / Z.savers_affected.sum()),
          '| FTN-category check MSEK/yr', round(Z.ftn_check_saving_msek.sum(), 1), '| cap moved bn', round(Z.cap_moved_bn.sum(), 1), 'cap inc winners bn', round(Z.cap_inc_winners_bn.sum(), 1))
