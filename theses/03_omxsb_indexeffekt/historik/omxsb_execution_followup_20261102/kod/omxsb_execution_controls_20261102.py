"""Fixed-control diagnostic for the already observed exploratory timing comparison.
No matching is estimated here; all controls come from the previously frozen file.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'output/omxsb_execution_followup_20261102/timing'
OUT=BASE/'fixed_controls';OUT.mkdir(exist_ok=True)
PLAN=json.loads((BASE/'PLAN_LOCK.json').read_text());SEED=PLAN['seed']
LOCK=json.loads((BASE/'ADDENDUM_FIXED_CONTROLS.json').read_text())
CP=ROOT/LOCK['control_file'];assert hashlib.sha256(CP.read_bytes()).hexdigest()==LOCK['control_file_sha256']
E=pd.read_csv(BASE/'v2_announced/event_comparisons.csv',parse_dates=['early_date','late_date'])
E=E[E.delay.eq(1)&E.status.eq('ok')].copy()
C=pd.read_csv(CP,usecols=['event_id','chosen_controls','c1_ric','c2_ric','c3_ric'])
E=E.merge(C,on='event_id',how='left',validate='one_to_one')
IX=pd.read_csv(ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
GI=IX[(IX.ric=='.OMXSBGI')&IX.close.notna()].set_index('date').sort_index().close
CAL=GI.index;POS={d:i for i,d in enumerate(CAL)};M=GI.pct_change(fill_method=None)
rics=list(pd.unique(E[['c1_ric','c2_ric','c3_ric']].to_numpy().ravel()));rics=[x for x in rics if pd.notna(x)]
PX=pd.read_parquet(ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','totret','close'],filters=[('ric','in',rics)])
PX['date']=pd.to_datetime(PX.date);assert not PX.duplicated(['ric','date']).any()
BY={r:g.set_index('date').sort_index().reindex(CAL) for r,g in PX.groupby('ric')}
rows=[]
for e in E.to_dict('records'):
    if e['chosen_controls']!=3:
        rows.append(dict(**e,control_status='no_frozen_three_controls'));continue
    a,b=POS[e['early_date']],POS[e['late_date']];factors=[];reason=None
    for k in [1,2,3]:
        ric=e[f'c{k}_ric'];p=BY.get(ric)
        if p is None:reason='missing_control_RIC';break
        v=p.totret.iloc[a+1:b+1]/100.0;price=p.close.iloc[[a,b]]
        if not (np.isfinite(v).all() and (v>-1).all() and np.isfinite(price).all() and (price>0).all()):
            reason='missing_control_totalreturn_or_endpoint';break
        factors.append(float(np.prod(1+v)))
    if reason:rows.append(dict(**e,control_status=reason));continue
    sign=1 if e['type']=='addition' else -1
    stockfactor=e['early_terminal_factor'] if sign==1 else e['baseline_terminal_factor']
    y=sign*(stockfactor-np.mean(factors))*100
    rows.append(dict(**e,control_status='ok',fixed_control_pp=y,control_terminal_factor=float(np.mean(factors))))
D=pd.DataFrame(rows);D.to_csv(OUT/'event_comparisons.csv',index=False)
D.groupby(['type','control_status']).size().rename('N').reset_index().to_csv(OUT/'coverage.csv',index=False)
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



summ=[]
for ty in ['addition','deletion']:
    for label,years in [('2017_2025',(2017,2025)),('descriptive2021_2025',(2021,2025))]:
        g=D[D.type.eq(ty)&D.year.between(*years)&D.control_status.eq('ok')]
        for metric in ['gross_pp','fixed_control_pp']:summ.append(summarize(g,f'{ty}_{label}_fixed_common_sample',metric))
S=pd.DataFrame(summ).rename(columns={'median_peak_absolute_path_pp':'median_market_relative_peak_path_pp','max_peak_absolute_path_pp':'max_market_relative_peak_path_pp'});S.to_csv(OUT/'summary.csv',index=False)
D[D.control_status.eq('ok')].groupby(['type','review'])[['gross_pp','fixed_control_pp']].mean().reset_index().to_csv(OUT/'review_comparisons.csv',index=False)
run=dict(completed_at_utc=datetime.now(timezone.utc).isoformat(),exploratory_after_v2=True,
 control_sha256=hashlib.sha256(CP.read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 lock_sha256=hashlib.sha256((BASE/'ADDENDUM_FIXED_CONTROLS.json').read_bytes()).hexdigest(),full_portfolio_or_causal_effect=False)
(OUT/'RUN.json').write_text(json.dumps(run,indent=2)+'\n')
print(S[['sample','metric','N','G','mean_review_pp','ci_low_pp','ci_high_pp','p_signflip']].to_string(index=False))
