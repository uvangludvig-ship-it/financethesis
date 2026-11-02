"""Exploratory announcement-cohort timing comparison; no full-fund or causal claim.
Includes raw final changes plus source-verified known cancellations.
Decision history is retained under timing/; this v2 amendment follows observed v1.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import t
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'output/omxsb_execution_followup_20261102'
OUT = BASE/'timing/v2_announced'; OUT.mkdir(exist_ok=True)
PLAN = json.loads((BASE/'timing/PLAN_LOCK.json').read_text())
SEED = PLAN['seed']
E = pd.read_csv(ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
E=E.rename(columns={'announcement_date':'AD','effective_date':'ED','review_cycle':'review'})
E['AD']=pd.to_datetime(E.AD);E['ED']=pd.to_datetime(E.ED)
E=E[E.AD.dt.year.between(2017,2025)].copy()
E['cancelled']=False;E['cancellation_date']=pd.NaT
L=pd.read_csv(BASE/'sources/known_cancellations.csv')
L=L.rename(columns={'known_cancel_id':'event_id','scheduled_ED':'ED','initial_source_url':'source_url'})
L['cancelled']=True;L['verification']='source_verified_known_cancellation'
L['AD']=pd.to_datetime(L.AD);L['ED']=pd.to_datetime(L.ED);L['cancellation_date']=pd.to_datetime(L.cancellation_date)
E=pd.concat([E,L],ignore_index=True)
assert not E.event_id.duplicated().any()
assert not E.duplicated(['review','RIC','type']).any()
LEG=pd.read_csv(ROOT/'output/omxsb_replication_2007/events_car.csv')
E['in_legacy_replication']=E.event_id.isin(LEG.event_id)
IX=pd.read_csv(ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
GI=IX.loc[(IX.ric=='.OMXSBGI')&IX.close.notna(),['date','close']].set_index('date').sort_index().close
assert not GI.index.duplicated().any()
CAL=GI.index;POS={d:i for i,d in enumerate(CAL)};M=GI.pct_change(fill_method=None)
PX=pd.read_parquet(ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',
 columns=['ric','date','totret','close'],filters=[('ric','in',list(E.RIC.dropna().unique()))])
PX['date']=pd.to_datetime(PX.date)
assert not PX.duplicated(['ric','date']).any()
BY={r:g.set_index('date').sort_index().reindex(CAL) for r,g in PX.groupby('ric')}

def factor(x):
    v=np.asarray(x,float)
    if not np.isfinite(v).all() or (v<=-1).any():return np.nan
    return float(np.prod(1+v))  # empty segment is cash factor1

rows=[]
for e in E.itertuples():
    a,b=POS.get(e.AD),POS.get(e.ED)
    base=dict(event_id=e.event_id,review=e.review,RIC=e.RIC,company=e.company,type=e.type,
      AD=e.AD,ED=e.ED,year=e.AD.year,cancelled=e.cancelled,cancellation_date=e.cancellation_date,
      in_legacy_replication=e.in_legacy_replication,source_url=e.source_url,verification=e.verification)
    for delay in [1,2]:
        r=dict(**base,delay=delay)
        if a is None or b is None or e.RIC not in BY:
            rows.append(dict(**r,status='missing_calendar_or_RIC'));continue
        start=a+delay;end=b-1
        r.update(early_date=CAL[start],late_date=CAL[end],holding_days=end-start)
        if end<=start:
            rows.append(dict(**r,status='no_positive_tradable_interval'));continue
        p=BY[e.RIC];tr=p.totret/100.0
        u=min(int(CAL.searchsorted(e.cancellation_date,side='right')),end) if e.cancelled else end
        noentry=bool(e.cancelled and e.cancellation_date<=CAL[start])
        r.update(unwind_date=CAL[u] if e.cancelled else pd.NaT,no_entry_due_to_cancellation=noentry)
        if noentry:
            rows.append(dict(**r,status='ok',gross_pp=0.0,net_10bps_pp=0.0,net_25bps_pp=0.0,
                net_50bps_pp=0.0,large_daily_return_flag=False,max_absolute_path_pp=0.0,
                worst_path_pp=0.0,best_path_pp=0.0,trade_count=0));continue
        required_stock_end=end if e.type=='deletion' else u
        stock=tr.iloc[start+1:required_stock_end+1];bm=M.iloc[start+1:end+1]
        r.update(missing_stock_days=int(stock.isna().sum()),missing_index_days=int(bm.isna().sum()))
        if not (np.isfinite(factor(stock)) and np.isfinite(factor(bm))):
            rows.append(dict(**r,status='invalid_or_missing_total_return'));continue
        prices=p.close.iloc[[start,u]]
        if not (np.isfinite(prices).all() and (prices>0).all()):
            rows.append(dict(**r,status='missing_transaction_endpoint_price'));continue
        path=[]
        for k in range(start+1,end+1):
            x=min(k,u)
            stock_pre=factor(tr.iloc[start+1:x+1]);index_pre=factor(M.iloc[start+1:x+1])
            if e.type=='addition':
                early=stock_pre*factor(M.iloc[x+1:k+1]);late=factor(M.iloc[start+1:k+1])
            else:
                early=index_pre*factor(tr.iloc[x+1:k+1]);late=factor(tr.iloc[start+1:k+1])
            path.append((early-late)*100)
        gross=float(path[-1]);ntrade=2 if e.cancelled else 1
        r.update(status='ok',gross_pp=gross,early_terminal_factor=early,baseline_terminal_factor=late,
            trade_count=ntrade,max_absolute_path_pp=float(np.max(np.abs(path))),
            worst_path_pp=float(np.min(path)),best_path_pp=float(np.max(path)),
            large_daily_return_flag=bool((stock.abs()>.5).any()))
        for bp in [10,25,50]:r[f'net_{bp}bps_pp']=gross-ntrade*bp/100
        rows.append(r)
D=pd.DataFrame(rows)
D.to_csv(OUT/'event_comparisons.csv',index=False)
D.groupby(['type','delay','cancelled','status']).size().rename('N').reset_index().to_csv(OUT/'coverage.csv',index=False)
# Verify the common v1 completed-event outcomes; this population repair must not change them.
V=pd.read_csv(BASE/'timing/v1_completed_events/event_comparisons.csv')
common=D.loc[D.status.eq('ok')].merge(V.loc[V.status.eq('ok'),['event_id','delay','gross_pp']],
 on=['event_id','delay'],suffixes=('_v2','_v1'))
maxdiff=float((common.gross_pp_v2-common.gross_pp_v1).abs().max())
assert len(common)>0 and maxdiff<1e-9
def signflip(x):
    x=np.asarray(x,float);n=len(x);obs=abs(x.mean())
    if n<=20:
        count=0;size=1<<n
        for start in range(0,size,8192):
            k=np.arange(start,min(start+8192,size),dtype=np.uint32)
            signs=((k[:,None]>>np.arange(n,dtype=np.uint32))&1)*2.0-1
            count+=int((np.abs(signs@x/n)>=obs-1e-12).sum())
        return count/size
    rng=np.random.default_rng(SEED);count=0;size=99999
    for start in range(0,size,8192):
        k=min(8192,size-start);s=rng.choice([-1,1],size=(k,n))
        count+=int((np.abs(s@x/n)>=obs-1e-12).sum())
    return (count+1)/(size+1)

def summarize(d,label,metric='gross_pp'):
    d=d.dropna(subset=[metric]);v=d.groupby('review')[metric].mean()
    n=len(v)
    if n<2:return dict(sample=label,metric=metric,N=len(d),G=n)
    m=float(v.mean());se=float(v.std(ddof=1)/np.sqrt(n));q=float(t.ppf(.975,n-1))
    loo=(v.sum()-v)/(n-1)
    return dict(sample=label,metric=metric,N=len(d),G=n,issuers=d.RIC.nunique(),mean_review_pp=m,
        ci_low_pp=m-q*se,ci_high_pp=m+q*se,p_signflip=signflip(v.values),
        mean_event_pp=d[metric].mean(),median_event_pp=d[metric].median(),
        event_sd_pp=d[metric].std(ddof=1),negative_event_share=(d[metric]<0).mean(),
        worst_review_pp=v.min(),best_review_pp=v.max(),loo_review_min_pp=loo.min(),loo_review_max_pp=loo.max(),
        median_holding_days=d.holding_days.median(),median_peak_absolute_path_pp=d.max_absolute_path_pp.median(),
        max_peak_absolute_path_pp=d.max_absolute_path_pp.max(),large_daily_return_events=int(d.large_daily_return_flag.sum()))


ok=D[D.status.eq('ok')].copy();summ=[];rev=[]
for ty in ['addition','deletion']:
    for name,years in [('primary2017_2025',(2017,2025)),('exploratory2017_2020',(2017,2020)),('exploratory2021_2025',(2021,2025))]:
        g=ok[ok.type.eq(ty)&ok.year.between(*years)&ok.delay.eq(1)]
        label=f'{ty}_{name}_announced_ADplus1'
        if len(g):
            summ.append(summarize(g,label))
            rr=g.groupby('review').agg(N=('event_id','size'),cancelled_N=('cancelled','sum'),gross_pp=('gross_pp','mean'),mean_holding_days=('holding_days','mean')).reset_index()
            rr['sample']=label;rev.append(rr)
        if name=='primary2017_2025':
            for bp in [10,25,50]:summ.append(summarize(g,label,f'net_{bp}bps_pp'))
            summ.append(summarize(g[~g.cancelled],label+'_completed_only'))
            paired=set(g.event_id)&set(ok.loc[ok.type.eq(ty)&ok.delay.eq(2),'event_id'])
            for delay in [1,2]:summ.append(summarize(ok[ok.event_id.isin(paired)&ok.delay.eq(delay)],f'{ty}_primary2017_2025_paired_ADplus{delay}'))
S=pd.DataFrame(summ);S.to_csv(OUT/'summary.csv',index=False)
pd.concat(rev,ignore_index=True).to_csv(OUT/'review_comparisons.csv',index=False)
D[D.cancelled].to_csv(OUT/'cancellation_comparisons.csv',index=False)
D[~D.in_legacy_replication&~D.cancelled].to_csv(OUT/'previous_upstream_exclusions.csv',index=False)
inputs=[ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',BASE/'sources/known_cancellations.csv',
 BASE/'timing/PLAN_LOCK.json',BASE/'timing/ADDENDUM_CANCELLATIONS.json',BASE/'timing/ADDENDUM_RAW_COHORT.json']
run=dict(completed_at_utc=datetime.now(timezone.utc).isoformat(),new_results_exploratory=True,
 raw_plus_known_cancellations=int(len(E)),common_v1_cells=int(len(common)),max_abs_common_v1_difference_pp=maxdiff,
 exact_full_initial_notice_history_verified=False,full_fund_strategy_or_actual_execution=False,
 input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
 script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(OUT/'RUN.json').write_text(json.dumps(run,ensure_ascii=False,indent=2)+'\n')
print(S[['sample','metric','N','G','mean_review_pp','ci_low_pp','ci_high_pp','p_signflip','negative_event_share']].to_string(index=False))
print(json.dumps(run))
