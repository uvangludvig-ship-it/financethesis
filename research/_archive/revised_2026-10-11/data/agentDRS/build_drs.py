"""Feasibility check: forced PPM inflows to FTN procurement winners as an exogenous
size shock (DRS design). Descriptive only.

Outputs (in this directory):
  treated_funds.csv        one row per winner (new + incumbent) with tranche months, dose, post months
  tranche_months.csv       long: fund x tranche month x handel_netto
  before_after.csv         fund-level mean excess return 12m before / after transfer
  before_after_groups.csv  group averages
  ppm_post_dynamics.csv    PPM capital & TNA after the transfer
  purge_2019.csv           2019 exits by month
  purge_2019_funds.csv     fund-level 2019 exit detail
  power.csv                power sketch
"""
import pandas as pd, numpy as np, json, os
OUT = os.path.dirname(os.path.abspath(__file__))
FTN = os.path.dirname(OUT)
SHOF = '/mnt/user-data/uploads/financethesis_ny/data/derived/shof_monthly'

# FX assumption (no FX file in the data set). Stated, crude.
FX = {'SEK': 1.0, 'EUR': 11.0, 'USD': 10.0, 'NOK': 0.97, 'DKK': 1.48, 'GBP': 13.0}

# ---------------------------------------------------------------- load
p = pd.read_csv(f'{FTN}/ppm_panel_2018_2026.csv', low_memory=False)
p['ym'] = pd.PeriodIndex(p.date.str[:7], freq='M')
p = p.drop_duplicates(['fondnr', 'ym'], keep='last').sort_values(['fondnr', 'ym'])
m = pd.read_csv(f'{FTN}/agentA/task1_round_membership.csv')
x = pd.read_csv(f'{FTN}/agentC/crosswalk_ppm_shof.csv')
x = x[x.match_method != 'none']
fm = pd.read_pickle(f'{FTN}/agentC/fundmaster.pkl')
v = pd.read_csv(f'{SHOF}/shof_valuations_monthly.csv')
r = pd.read_csv(f'{SHOF}/shof_rips_monthly.csv')
r = r[r.returntype == 1]

# fund-level TNA (median across classes) per fundid-ym
pid2fid = fm.drop_duplicates('performanceid').set_index('performanceid').fundid
v['fundid'] = v.performanceId.map(pid2fid)
v['tna_sek_row'] = v.tnafund * v.ccy_fund.map(FX)
fl = (v.dropna(subset=['tnafund']).groupby(['fundid', 'ym'])
      .agg(tnafund=('tnafund', 'median'), ccy_fund=('ccy_fund', lambda c: c.mode().iloc[0]),
           tna_sek=('tna_sek_row', 'median'), nf_fund=('nf_fund', 'median'))
      .reset_index())
fl['ym'] = pd.PeriodIndex(fl.ym, freq='M')
# fill gaps: carry last observed TNA forward up to 12 months (Swedbank Robur/Folksam report sparsely), flag staleness
grid = (fl.groupby('fundid').ym.agg(['min', 'max']).apply(lambda r: pd.period_range(r['min'], pd.Period('2026-09', 'M'), freq='M'), axis=1)
        .explode().rename('ym').reset_index())
fl = grid.merge(fl, on=['fundid', 'ym'], how='left').sort_values(['fundid', 'ym'])
fl['obs_ym'] = fl.ym.where(fl.tnafund.notna())
for c in ['tnafund', 'ccy_fund', 'tna_sek', 'obs_ym']:
    fl[c] = fl.groupby('fundid')[c].ffill(limit=18)
fl['tna_stale_m'] = [(a - b).n if pd.notna(b) else np.nan for a, b in zip(fl.ym, fl.obs_ym)]
TNA = fl.set_index(['fundid', 'ym'])

# returns: SEK TRI per performanceid -> monthly return; fund-level series = PPM class,
# fallback to the class of the same fund with the longest history
r['ym'] = pd.PeriodIndex(r.ym, freq='M')
r = r.sort_values(['performanceId', 'ym'])
r['ret'] = r.groupby('performanceId').tri_sek.pct_change(fill_method=None)
# drop returns where the gap is > 1 month
r['gap'] = r.groupby('performanceId').ym.diff().apply(lambda d: d.n if pd.notna(d) else np.nan)
r.loc[r.gap != 1, 'ret'] = np.nan
RET = r.set_index(['performanceId', 'ym']).ret
r['fundid'] = r.performanceId.map(pid2fid)
hist = r.dropna(subset=['ret']).groupby('performanceId').ret.count()


def fund_ret(pid, fundid):
    """monthly SEK return series for a fund: PPM class, filled with longest-history sibling class."""
    s = RET.loc[pid] if pid in RET.index.get_level_values(0) else pd.Series(dtype=float)
    sib = fm.loc[fm.fundid == fundid, 'performanceid'].unique()
    sib = [q for q in sib if q in hist.index and q != pid]
    if sib:
        best = max(sib, key=lambda q: hist[q])
        s2 = RET.loc[best]
        s = s2.copy() if s.empty else s.combine_first(s2)
    return s.sort_index()


# category mean return per kategori-month (SHoF SEK returns of PPM member funds; fallback rounded ret_1m)
pp = p[~p.fondnr.isin([1, 2, 3, 4])].merge(x[['fondnr', 'performanceid']], on='fondnr', how='left')
pp['ret_shof'] = [RET.get((a, b), np.nan) for a, b in zip(pp.performanceid, pp.ym)]
pp['ret_use'] = pp.ret_shof.fillna(pp.ret_1m / 100)
cat = pp.groupby(['kategori', 'ym']).agg(cat_ret=('ret_use', 'mean'), n_cat=('ret_use', 'count'),
                                          cat_ret_shof=('ret_shof', 'mean'), n_shof=('ret_shof', 'count')).reset_index()
cat.loc[cat.n_cat < 5, 'cat_ret'] = np.nan
CAT = cat.set_index(['kategori', 'ym']).cat_ret
# fixed-membership benchmark: funds in kategori at anchor month (PPM panel), SHoF SEK returns, leave-one-out
_RETW = {}
def bench(kat, anchor, self_fondnr):
    key = (kat, anchor)
    if key not in _RETW:
        mem = pp[(pp.ym == anchor) & (pp.kategori == kat)].dropna(subset=['performanceid'])
        cols = {}
        for fn, pid in zip(mem.fondnr, mem.performanceid):
            fid = x.loc[x.fondnr == fn, 'fundid'].iloc[0]
            cols[fn] = fund_ret(pid, fid)
        _RETW[key] = pd.DataFrame(cols)
    df = _RETW[key]
    df = df.drop(columns=[self_fondnr], errors='ignore')
    b = df.mean(axis=1); b[df.count(axis=1) < 5] = np.nan
    return b, df.shape[1]

# ---------------------------------------------------------------- transfer windows per round
# window = [earliest month of large loser outflow or loser exit month, latest loser exit month + 1]
m['award_ym'] = pd.PeriodIndex(m.award.str[:7], freq='M')
m['exit_ym'] = pd.PeriodIndex(m.avslutsdatum.fillna('2099-12').str[:7], freq='M')
PANEL_END = pd.Period('2026-08', 'M')
windows = {}
for rd, g in m[m.role == 'loser'].groupby('round'):
    ex = g.exit_ym[g.exit_ym < pd.Period('2099-01', 'M')]
    a = g.award_ym.iloc[0]
    # loser outflow months: month where losers' aggregate handel_netto < -5% of their mv_award
    lo = p[p.fondnr.isin(g.fondnr) & (p.ym > a)].groupby('ym').handel_netto.sum()
    big = lo[lo < -0.05 * g.mv_award.sum()].index
    start = min([ex.min() if len(ex) else PANEL_END] + ([big.min()] if len(big) else []))
    # SE_index: Avanza Zero (pending) still draining -> window open to panel end
    pending = g.exit_ym.eq(pd.Period('2099-12', 'M')).any()
    end = PANEL_END if pending else min(ex.max() + 1, PANEL_END)
    windows[rd] = (start, end, pending, len(ex), int(g.shape[0]))
W = pd.DataFrame(windows, index=['win_start', 'win_end', 'pending', 'n_exited', 'n_losers']).T
print('transfer windows:\n', W)

# ---------------------------------------------------------------- treated set
w = m[m.role.str.startswith('winner')].merge(x[['fondnr', 'performanceid', 'fundid', 'fundname_ms']], on='fondnr', how='left')
rows, tr_rows = [], []
for _, f in w.iterrows():
    rd = f['round']; ws, we = W.loc[rd, 'win_start'], W.loc[rd, 'win_end']
    s = p[p.fondnr == f.fondnr].set_index('ym')
    mv = s.mv_tot; hn = s.handel_netto
    mv_prev = mv.shift(1)
    # baseline: median handel_netto in 6 months before window (0 for a fund not yet in PPM)
    pre6 = hn[(hn.index >= ws - 6) & (hn.index < ws)]
    base = pre6.median() if len(pre6) else 0.0
    base = 0.0 if pd.isna(base) else base
    win = hn[(hn.index >= ws) & (hn.index <= we)]
    mvp = mv_prev.reindex(win.index).fillna(0)
    thr = np.maximum(0.03 * mvp, 10e6)
    tranche = win[(win - base) > thr]
    tm = list(tranche.index)
    first, last = (tm[0], tm[-1]) if tm else (pd.NaT, pd.NaT)
    inflow = float((tranche - base).sum()) if tm else 0.0
    pre_m = first - 1 if tm else ws - 1
    pre_mv = mv.get(pre_m, 0.0); pre_mv = 0.0 if pd.isna(pre_mv) else pre_mv
    # voluntary inflow between award and window start (new winners: active choosers)
    vol = hn[(hn.index > f.award_ym) & (hn.index < ws)].sum()
    fid = f.fundid
    tna_pre = TNA.tna_sek.get((fid, pre_m), np.nan) if pd.notna(fid) else np.nan
    tna_pre_cc = TNA.tnafund.get((fid, pre_m), np.nan) if pd.notna(fid) else np.nan
    tna_stale = TNA.tna_stale_m.get((fid, pre_m), np.nan) if pd.notna(fid) else np.nan
    ccy = TNA.ccy_fund.get((fid, pre_m), np.nan) if pd.notna(fid) else np.nan
    tna_last = TNA.tna_sek.get((fid, last), np.nan) if (pd.notna(fid) and tm) else np.nan
    tna_end = TNA.tna_sek.get((fid, pd.Period('2026-09', 'M')), np.nan) if pd.notna(fid) else np.nan
    if pd.isna(tna_end) and pd.notna(fid):
        tna_end = TNA.tna_sek.get((fid, pd.Period('2026-08', 'M')), np.nan)
    rows.append(dict(round=rd, award=f.award, role=f.role, fondnr=f.fondnr, fondnamn=f.fondnamn, fundid=fid,
                     ccy_fund=ccy, win_start=str(ws), win_end=str(we), n_tranches=len(tm),
                     first_tranche=str(first) if tm else '', last_tranche=str(last) if tm else '',
                     pre_month=str(pre_m), pre_ppm_mv_msek=round(pre_mv / 1e6, 1),
                     pre_tna_fundccy_m=round(tna_pre_cc / 1e6, 1) if pd.notna(tna_pre_cc) else np.nan,
                     pre_tna_msek=round(tna_pre / 1e6, 1) if pd.notna(tna_pre) else np.nan, pre_tna_stale_months=tna_stale,
                     baseline_hn_msek=round(base / 1e6, 2), forced_inflow_msek=round(inflow / 1e6, 1),
                     voluntary_pre_window_msek=round(vol / 1e6, 1),
                     dose_tna=round(inflow / tna_pre, 3) if (pd.notna(tna_pre) and tna_pre > 0) else np.nan,
                     dose_ppm=round(inflow / pre_mv, 3) if pre_mv > 0 else np.nan,
                     tna_at_last_tranche_msek=round(tna_last / 1e6, 1) if pd.notna(tna_last) else np.nan,
                     tna_2026_09_msek=round(tna_end / 1e6, 1) if pd.notna(tna_end) else np.nan,
                     post_months_ppm=int((PANEL_END - last).n) if tm else np.nan,
                     post_months_shof=int((pd.Period('2026-09', 'M') - last).n) if tm else np.nan,
                     window_open=bool(W.loc[rd, 'pending'])))
    for t in tm:
        tr_rows.append(dict(round=rd, role=f.role, fondnr=f.fondnr, fondnamn=f.fondnamn, ym=str(t),
                            handel_netto_msek=round(hn[t] / 1e6, 1), mv_prev_msek=round(mv_prev.get(t, 0) / 1e6, 1)))
T = pd.DataFrame(rows)
T['topped_up'] = (T.role == 'winner_new') | ((T.forced_inflow_msek > 50) & (T.dose_ppm > 0.10))
NOTES = {495482: 'inflow includes same-manager merger of loser SEB Sverige Expanderad (1.9bn) + Oct-Dec 2025 flows',
         531310: 'Nov-2025 tranche (636m) = merger of loser SEB Sweden Equity Fund C',
         343665: 'no Morningstar match (CCF); no TNA',
         567140: 'tiny fund: 243m TNA got 3.4bn',
         114819: 'Swedbank Robur TNA reported sparsely; pre-TNA stale', 607226: 'Swedbank Robur TNA reported sparsely; pre-TNA stale',
         755504: 'Swedbank Robur TNA stale; Feb-Mar 2025 inflow confounded by Europe rotation (category net +5.1bn Mar-25 vs losers 0.69bn)',
         629543: 'Feb-Mar 2025 inflow confounded by Europe rotation wave', 654459: 'Feb-Mar 2025 inflow confounded by Europe rotation wave',
         140673: 'Feb-Mar 2025 inflow confounded by Europe rotation wave',
         638809: 'window open: Avanza Zero (21bn) still draining', 602979: 'window open: Avanza Zero still draining; fund grew 0.9->13bn pre-PPM',
         290072: 'window open: Avanza Zero still draining; largest incumbent top-up', 465914: 'window open: Avanza Zero still draining',
         527060: 'NOK fund; FX assumption', 674630: 'Morningstar reports fund TNA in EUR; FX assumption'}
T['notes'] = T.fondnr.map(NOTES).fillna('')
T.loc[T['round'].isin(['EU_smallcap', 'SE_smallcap']), 'notes'] = T.loc[T['round'].isin(['EU_smallcap', 'SE_smallcap']), 'notes'] + ' transfer not started/just started'
T.to_csv(f'{OUT}/treated_funds.csv', index=False)
pd.DataFrame(tr_rows).to_csv(f'{OUT}/tranche_months.csv', index=False)

# ---------------------------------------------------------------- before / after excess returns
ba = []
for _, f in T.iterrows():
    if not f.n_tranches or pd.isna(f.fundid):
        continue
    first, last = pd.Period(f.first_tranche, 'M'), pd.Period(f.last_tranche, 'M')
    kat = m.loc[m.fondnr == f.fondnr, 'kategori'].iloc[0]
    pid = w.loc[w.fondnr == f.fondnr, 'performanceid'].iloc[0]
    fr = fund_ret(pid, f.fundid)
    anchor = pd.Period(f.award[:7], 'M') - 1
    b, nb = bench(kat, anchor, f.fondnr)
    ex = (fr - b.reindex(fr.index))
    pre = ex[(ex.index >= first - 12) & (ex.index < first)].dropna()
    post = ex[(ex.index > last) & (ex.index <= last + 12)].dropna()
    raw_pre = fr[(fr.index >= first - 12) & (fr.index < first)].dropna()
    raw_post = fr[(fr.index > last) & (fr.index <= last + 12)].dropna()
    ba.append(dict(round=f['round'], role=f.role, topped_up=f.topped_up, fondnr=f.fondnr, fondnamn=f.fondnamn,
                   dose_tna=f.dose_tna, n_bench=nb, n_pre=len(pre), n_post=len(post),
                   raw_pre_pct=round(100 * raw_pre.mean(), 3), raw_post_pct=round(100 * raw_post.mean(), 3),
                   excess_pre_pct=round(100 * pre.mean(), 3), excess_post_pct=round(100 * post.mean(), 3),
                   excess_diff_pct=round(100 * (post.mean() - pre.mean()), 3),
                   sd_excess_pre_pct=round(100 * pre.std(), 3)))
BA = pd.DataFrame(ba)

# controls: (a) incumbents with no top-up (already in BA), (b) funds in not-yet-procured equity categories,
# evaluated on the same event window as each round
EQ = ['Global', 'Sverige', 'Nya marknader', 'Europa', 'USA och Nordamerika', 'Asien', 'Sverige småbolag', 'Norden',
      'Läkemedel och bioteknik', 'Råvaror och energi', 'Kina', 'Övriga länder', 'Japan', 'IT och kommunikation',
      'Övriga branscher', 'Fastighet', 'Indien', 'Europa småbolag', 'Latinamerika', 'Östeuropa', 'Ryssland',
      'Norden småbolag', 'Global och Sverige']
proc_cat = {'Europa': '2024-03', 'Global': '2024-10', 'Norden': '2025-02', 'Norden småbolag': '2025-02',
            'Sverige': '2025-08', 'Europa småbolag': '2026-05', 'Sverige småbolag': '2026-05'}
ctl = []
kat_last = p.dropna(subset=['kategori']).groupby('fondnr').kategori.last()
for rd, g in T[T.n_tranches > 0].groupby('round'):
    first = pd.Period(g.first_tranche.min(), 'M'); last = pd.Period(g.last_tranche.max(), 'M')
    members = p[(p.ym == first - 1)].fondnr.unique()
    for fn in members:
        kat = kat_last.get(fn)
        if kat not in EQ or (kat in proc_cat and pd.Period(proc_cat[kat], 'M') <= last + 12):
            continue
        xr = x[x.fondnr == fn]
        if xr.empty:
            continue
        fr = fund_ret(xr.performanceid.iloc[0], xr.fundid.iloc[0])
        if fr.empty:
            continue
        b, nb = bench(kat, first - 1, fn)
        ex = fr - b.reindex(fr.index)
        pre = ex[(ex.index >= first - 12) & (ex.index < first)].dropna()
        post = ex[(ex.index > last) & (ex.index <= last + 12)].dropna()
        if len(pre) < 6 or len(post) < 3:
            continue
        ctl.append(dict(round=rd, role='control_unprocured', topped_up=False, fondnr=fn, kategori=kat,
                        n_pre=len(pre), n_post=len(post), excess_pre_pct=100 * pre.mean(),
                        excess_post_pct=100 * post.mean(), excess_diff_pct=100 * (post.mean() - pre.mean())))
CT = pd.DataFrame(ctl)
BA.to_csv(f'{OUT}/before_after.csv', index=False)
CT.to_csv(f'{OUT}/before_after_controls.csv', index=False)
BA['grp'] = np.where(BA.role == 'winner_new', 'winner_new', np.where(BA.topped_up, 'incumbent_topped_up', 'incumbent_no_topup'))
CT['grp'] = 'control_unprocured'
allba = pd.concat([BA, CT])
G = (allba.groupby(['round', 'grp']).agg(n=('fondnr', 'count'), n_post_med=('n_post', 'median'),
                                          excess_pre=('excess_pre_pct', 'mean'), excess_post=('excess_post_pct', 'mean'),
                                          diff=('excess_diff_pct', 'mean'), diff_median=('excess_diff_pct', 'median'))
     .round(3).reset_index())
Gall = (allba.groupby('grp').agg(n=('fondnr', 'count'), n_post_med=('n_post', 'median'),
                                  excess_pre=('excess_pre_pct', 'mean'), excess_post=('excess_post_pct', 'mean'),
                                  diff=('excess_diff_pct', 'mean'), diff_median=('excess_diff_pct', 'median'))
        .round(3).reset_index().assign(round='ALL'))
pd.concat([G, Gall]).to_csv(f'{OUT}/before_after_groups.csv', index=False)

# ---------------------------------------------------------------- PPM capital & TNA dynamics after the transfer
dyn = []
for _, f in T[T.n_tranches > 0].iterrows():
    last = pd.Period(f.last_tranche, 'M')
    s = p[p.fondnr == f.fondnr].set_index('ym')
    post = s[s.index > last]
    mv_last = s.mv_tot.get(last, np.nan); mv_end = s.mv_tot.get(PANEL_END, np.nan)
    hn_post = post.handel_netto.sum(); n_post = len(post)
    hn_post_pct_mo = 100 * (post.handel_netto / s.mv_tot.shift(1).reindex(post.index)).mean() if n_post else np.nan
    fid = f.fundid
    tna_last = TNA.tna_sek.get((fid, last), np.nan); tna_end = TNA.tna_sek.get((fid, PANEL_END), np.nan)
    d_tna = tna_end - tna_last; d_mv = mv_end - mv_last
    # cumulative fund return last tranche -> 2026-08, est. non-PPM net flow = dTNA - TNA*R - (dPPM - PPM*R)
    pid = w.loc[w.fondnr == f.fondnr, 'performanceid'].iloc[0]
    fr = fund_ret(pid, fid) if pd.notna(fid) else pd.Series(dtype=float)
    frw = fr[(fr.index > last) & (fr.index <= PANEL_END)] if not fr.empty else fr
    Rc = float(np.prod(1 + frw.dropna())) - 1 if (len(frw.dropna()) == n_post and n_post > 0) else np.nan
    nonppm = (tna_end - tna_last * (1 + Rc)) - (mv_end - mv_last * (1 + Rc)) if pd.notna(Rc) and pd.notna(tna_end) else np.nan
    dyn.append(dict(round=f['round'], role=f.role, fondnr=f.fondnr, fondnamn=f.fondnamn, last_tranche=f.last_tranche,
                    n_post=n_post, ppm_mv_at_last_msek=round(mv_last / 1e6, 1), ppm_mv_2026_08_msek=round(mv_end / 1e6, 1),
                    post_hn_sum_msek=round(hn_post / 1e6, 1), post_hn_pct_of_mv_per_month=round(hn_post_pct_mo, 2),
                    post_hn_over_forced=round(hn_post / (f.forced_inflow_msek * 1e6), 3) if f.forced_inflow_msek else np.nan,
                    tna_at_last_msek=round(tna_last / 1e6, 1) if pd.notna(tna_last) else np.nan,
                    tna_2026_08_msek=round(tna_end / 1e6, 1) if pd.notna(tna_end) else np.nan,
                    d_tna_msek=round(d_tna / 1e6, 1) if pd.notna(d_tna) else np.nan, d_ppm_msek=round(d_mv / 1e6, 1),
                    ppm_share_of_dTNA=round(d_mv / d_tna, 2) if (pd.notna(d_tna) and abs(d_tna) > 1e6) else np.nan,
                    cum_ret_post_pct=round(100 * Rc, 1) if pd.notna(Rc) else np.nan,
                    est_nonppm_netflow_msek=round(nonppm / 1e6, 1) if pd.notna(nonppm) else np.nan,
                    est_nonppm_netflow_pct_of_tna=round(100 * nonppm / tna_last, 1) if (pd.notna(nonppm) and tna_last > 0) else np.nan,
                    ppm_share_of_tna_end=round(mv_end / tna_end, 2) if pd.notna(tna_end) else np.nan))
pd.DataFrame(dyn).to_csv(f'{OUT}/ppm_post_dynamics.csv', index=False)

# ---------------------------------------------------------------- 2019 purge
q = p[~p.fondnr.isin([1, 2, 3, 4])]
lastm = q.groupby('fondnr').ym.max()
firstm = q.groupby('fondnr').ym.min()
ex19 = lastm[(lastm >= pd.Period('2018-06', 'M')) & (lastm <= pd.Period('2020-12', 'M'))]
pf = []
for fn, lm in ex19.items():
    s = q[q.fondnr == fn].set_index('ym')
    mv_exit = s.mv_tot.get(lm, np.nan)
    mv_dec18 = s.mv_tot.get(pd.Period('2018-12', 'M'), np.nan)
    pre = s.handel_netto[(s.index >= pd.Period('2019-01', 'M')) & (s.index < lm)]
    hn_pre = pre.sum() if len(pre) else 0.0
    hn_exit = s.handel_netto.get(lm, np.nan)
    pf.append(dict(fondnr=fn, fondnamn=s.fondnamn.iloc[-1], kategori=s.kategori.iloc[-1], fondtyp=s.fondtyp.iloc[-1],
                   last_month=str(lm), mv_dec2018_msek=round(mv_dec18 / 1e6, 1) if pd.notna(mv_dec18) else np.nan,
                   mv_exit_msek=round(mv_exit / 1e6, 1), hn_jan19_to_preexit_msek=round(hn_pre / 1e6, 1),
                   hn_exit_month_msek=round(hn_exit / 1e6, 1) if pd.notna(hn_exit) else np.nan,
                   vol_out_share=round(-hn_pre / mv_dec18, 3) if (pd.notna(mv_dec18) and mv_dec18 > 0) else np.nan,
                   val_exit=s.val_tot.get(lm, np.nan)))
PF = pd.DataFrame(pf)
PF.to_csv(f'{OUT}/purge_2019_funds.csv', index=False)
PM = (PF.groupby('last_month').agg(n_exits=('fondnr', 'count'), cap_exit_bn=('mv_exit_msek', lambda s: round(s.sum() / 1e3, 2)),
                                   cap_dec18_bn=('mv_dec2018_msek', lambda s: round(s.sum() / 1e3, 2)),
                                   vol_out_bn=('hn_jan19_to_preexit_msek', lambda s: round(-s.sum() / 1e3, 2)),
                                   savers_exit=('val_exit', 'sum')).reset_index())
# AP7 Såfa / default inflows by month 2019 (fondnr 1 handel_netto)
ap7 = p[p.fondnr == 1].set_index('ym')[['mv_tot', 'handel_netto', 'val_tot']]
ap7 = ap7[(ap7.index >= pd.Period('2018-06', 'M')) & (ap7.index <= pd.Period('2020-12', 'M'))]
PM = PM.merge(ap7.reset_index().assign(last_month=lambda d: d.ym.astype(str))[['last_month', 'mv_tot', 'handel_netto', 'val_tot']]
              .rename(columns={'mv_tot': 'ap7_mv_bn', 'handel_netto': 'ap7_hn_bn', 'val_tot': 'ap7_savers'}), on='last_month', how='left')
PM['ap7_mv_bn'] = (PM.ap7_mv_bn / 1e9).round(1); PM['ap7_hn_bn'] = (PM.ap7_hn_bn / 1e9).round(2)
PM.to_csv(f'{OUT}/purge_2019.csv', index=False)
# total number of funds on platform by month
nf = q.groupby('ym').fondnr.nunique()
nf[(nf.index >= pd.Period('2018-06', 'M')) & (nf.index <= pd.Period('2020-12', 'M'))].rename('n_funds').to_csv(f'{OUT}/n_funds_by_month_2018_2020.csv')

# ---------------------------------------------------------------- idiosyncratic sd and power sketch
# residual sd: SEK equity funds in PPM, SHoF return minus category mean, 2022-01..2026-08
pp2 = pp[(pp.ym >= pd.Period('2022-01', 'M')) & pp.kategori.isin(EQ) & (pp.valuta == 'SEK')].copy()
pp2['cat'] = [CAT.get((a, b), np.nan) for a, b in zip(pp2.kategori, pp2.ym)]
pp2['res'] = pp2.ret_shof - pp2.cat
sdf = pp2.dropna(subset=['res']).groupby('fondnr').res.agg(['std', 'count'])
sdf = sdf[sdf['count'] >= 24]
idx_names = pp2.groupby('fondnr').fondnamn.last().str.lower()
is_index = idx_names.str.contains('index|indeks|exponering|access|zero|criteria', regex=True)
sd_all = 100 * sdf['std'].median(); sd_act = 100 * sdf.loc[~is_index.reindex(sdf.index).fillna(False)]['std'].median()
sd_idx = 100 * sdf.loc[is_index.reindex(sdf.index).fillna(False)]['std'].median()
# index funds vs mean of index funds in same kategori (tighter benchmark)
pp3 = pp2[pp2.fondnr.isin(is_index[is_index].index)].copy()
pp3['ibench'] = pp3.groupby(['kategori', 'ym']).ret_shof.transform('mean'); pp3['n_i'] = pp3.groupby(['kategori', 'ym']).ret_shof.transform('count')
pp3 = pp3[pp3.n_i >= 3]; pp3['res_i'] = pp3.ret_shof - pp3.ibench
sdi = pp3.dropna(subset=['res_i']).groupby('fondnr').res_i.agg(['std', 'count']); sdi = sdi[sdi['count'] >= 24]
sd_idx_tight = 100 * sdi['std'].median()
# treated set for power: new winners with dose & >= 5 post months
tp = T[(T.role == 'winner_new') & T.dose_tna.notna() & (T.post_months_shof >= 5)]
tp12 = T[(T.role == 'winner_new') & T.dose_tna.notna() & (T.post_months_shof >= 12)]
tpall = T[T.topped_up & T.dose_tna.notna() & (T.post_months_shof >= 5)]
tpn_all = T[(T.role == 'winner_new') & T.dose_tna.notna() & (T.n_tranches > 0) & ~T['round'].isin(['EU_smallcap', 'SE_smallcap'])]
tp_all = T[T.topped_up & T.dose_tna.notna() & (T.n_tranches > 0) & ~T['round'].isin(['EU_smallcap', 'SE_smallcap'])]
sd_pre = 100 * BA.sd_excess_pre_pct.div(100).median() if 'sd_excess_pre_pct' in BA else np.nan
pw = []
for lab, S, sd, cap in [('new winners, >=5 post m, active sd, dose cap 5', tp, sd_act, 5), ('new winners, >=5 post m, all-fund sd, cap 5', tp, sd_all, 5),
                   ('new winners, >=5 post m, active sd, dose cap 1', tp, sd_act, 1),
                   ('new winners, >=12 post m, active sd, cap 5', tp12, sd_act, 5), ('new+topped incumbents, >=5 post m, active sd, cap 5', tpall, sd_act, 5),
                   ('new+topped incumbents, >=5 post m, active sd, cap 1', tpall, sd_act, 1),
                   ('new winners, >=5 post m, index sd, cap 5', tp, sd_idx, 5),
                   ('PROSPECTIVE all new winners (transfer done), active sd, cap 5', tpn_all, sd_act, 5),
                   ('PROSPECTIVE all new winners (transfer done), active sd, cap 1', tpn_all, sd_act, 1),
                   ('PROSPECTIVE all new+topped incumbents, active sd, cap 5', tp_all, sd_act, 5),
                   ('PROSPECTIVE all new+topped incumbents, active sd, cap 1', tp_all, sd_act, 1),
                   ('PROSPECTIVE all new+topped incumbents, treated-fund pre-period sd, cap 1', tp_all, sd_pre, 1),
                   ('PROSPECTIVE all new+topped incumbents, index-vs-index sd, cap 1', tp_all, None, 1)]:
    if sd is None: sd = sd_idx_tight
    n = len(S); d = S.dose_tna.clip(upper=cap)
    sdd = d.std(ddof=1) if n > 1 else np.nan
    Tm = 12
    se_cs = sd / np.sqrt(Tm) / (sdd * np.sqrt(n)) if n > 1 else np.nan   # cross-sectional slope on dose, 12-m avg excess ret
    mde_cs = 2.8 * se_cs                                                  # monthly % per 100% dose (alpha=5% two-sided, 80% power)
    # alternative: pooled treated-vs-category mean (no dose variation): se = sd / sqrt(n*T)
    se_lvl = sd / np.sqrt(n * Tm); mde_lvl = 2.8 * se_lvl
    pw.append(dict(spec=lab, n=n, dose_mean=round(d.mean(), 2), dose_sd=round(sdd, 2), dose_min=round(d.min(), 2), dose_max=round(d.max(), 2),
                   sd_month_pct=round(sd, 2), mde_per_100pct_dose_month_pct=round(mde_cs, 2), mde_per_100pct_dose_year_pct=round(12 * mde_cs, 1),
                   mde_level_month_pct=round(mde_lvl, 2), mde_level_year_pct=round(12 * mde_lvl, 1)))
PW = pd.DataFrame(pw)
PW.to_csv(f'{OUT}/power.csv', index=False)
json.dump(dict(sd_all=sd_all, sd_active=sd_act, sd_index=sd_idx, sd_index_tight=sd_idx_tight, sd_treated_pre=sd_pre, n_funds_sd=len(sdf), n_index_tight=len(sdi),
               windows={k: [str(a), str(b), bool(c), int(d), int(e)] for k, (a, b, c, d, e) in windows.items()}, FX=FX),
          open(f'{OUT}/meta.json', 'w'), indent=1)

pd.set_option('display.width', 300); pd.set_option('display.max_rows', 300); pd.set_option('display.max_columns', 40)
print(T[['round', 'role', 'fondnamn', 'ccy_fund', 'n_tranches', 'first_tranche', 'last_tranche', 'pre_ppm_mv_msek', 'pre_tna_msek',
         'forced_inflow_msek', 'voluntary_pre_window_msek', 'dose_tna', 'dose_ppm', 'post_months_shof', 'topped_up']].to_string())
print(pd.read_csv(f'{OUT}/before_after_groups.csv').to_string())
print(BA[['round', 'role', 'fondnamn', 'dose_tna', 'n_pre', 'n_post', 'excess_pre_pct', 'excess_post_pct', 'excess_diff_pct']].to_string())
print(pd.DataFrame(dyn)[['round', 'role', 'fondnamn', 'n_post', 'ppm_mv_at_last_msek', 'ppm_mv_2026_08_msek', 'post_hn_sum_msek', 'post_hn_pct_of_mv_per_month',
                         'tna_at_last_msek', 'tna_2026_08_msek', 'd_tna_msek', 'd_ppm_msek', 'ppm_share_of_dTNA', 'ppm_share_of_tna_end']].to_string())
print(PM.to_string())
print('sd all/active/index/index_tight/treated_pre', round(sd_all, 2), round(sd_act, 2), round(sd_idx, 2), round(sd_idx_tight, 2), round(sd_pre, 2), 'n', len(sdf), len(sdi))
print(PW.to_string())
