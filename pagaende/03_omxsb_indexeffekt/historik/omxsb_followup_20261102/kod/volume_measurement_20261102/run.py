from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import analysis_paths
_PORTABLE_REPO, _PORTABLE_OUT = analysis_paths('volume_measurement_20261102')
import sys, json, hashlib
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import t
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'comparison_rebuild_20261102'))
from run import fieller

R=_PORTABLE_REPO; O=_PORTABLE_OUT
dpath=R/'output/omxsb_mechanism_frontier_20261102/demand/event_demand_by_definition.csv'
qpath=R/'output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz'
epath=R/'output/omxsb_replication_2007/events_car.csv'
ppath=R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet'
ipath=R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv'
ev=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv',parse_dates=['before','after'])
dated=pd.read_csv(epath,usecols=['event_id','AD','ED'],parse_dates=['AD','ED'])
ev=ev.merge(dated,on='event_id',validate='1:1')
q=pd.read_csv(qpath,usecols=['event_id','fi_price_after','company_mcap_after'])
q=q.drop_duplicates();assert not q.duplicated('event_id').any()
ev=ev.merge(q,on='event_id',validate='1:1')
p=pd.read_parquet(ppath,columns=['ric','date','close','volume'])
p=p[p.ric.isin(ev.RIC)].copy();p['date']=pd.to_datetime(p.date)
assert not p.duplicated(['ric','date']).any()
idx=pd.read_csv(ipath)
datecol='date' if 'date' in idx else 'Date'
riccol='ric' if 'ric' in idx else 'RIC'
cal=pd.DatetimeIndex(sorted(pd.to_datetime(idx.loc[idx[riccol].eq('.OMXSBGI'),datecol]).dropna().unique()))
series={k:g.set_index('date').sort_index() for k,g in p.groupby('ric')}
rows=[]
for x in ev.itertuples():
    a=int(cal.searchsorted(x.AD)); ed=int(cal.searchsorted(x.ED)); recon=cal[ed-1]
    z=series[x.RIC].reindex(cal)
    prior=z.loc[z.index<=x.after,'close'].dropna()
    lastd=prior.index[-1] if len(prior) else pd.NaT
    px=prior.iloc[-1] if len(prior) else np.nan
    v=z.volume.where(z.volume.ge(0))
    b=v.iloc[a-61:a-11]; short=v.iloc[ed-22:ed-1]
    vol=v.loc[recon]; price_ratio=px/x.fi_price_after
    reason=[]
    if abs(x.factor-1)>1e-10:reason.append('known_split_conversion')
    if pd.isna(lastd) or (x.after-lastd).days>5:reason.append('stale_quarter_price')
    if not np.isfinite(price_ratio) or abs(price_ratio-1)>.02:reason.append('cross_source_price_unit_gate')
    if b.count()<40:reason.append('baseline_coverage')
    if not np.isfinite(vol):reason.append('missing_event_volume')
    scale=100*x.fi_price_after/x.company_mcap_after
    rows.append(dict(event_id=x.event_id,RIC=x.RIC,type=x.type,review_cycle=x.review_cycle,AD=x.AD,ED=x.ED,rebalancing_day=recon,after=x.after,after_panel_price=px,FI_price=x.fi_price_after,price_ratio=price_ratio,price_date=lastd,baseline_N=b.count(),shortbaseline_N=short.count(),volume=vol,baseline_volume=b.mean(),shortbaseline_volume=short.mean(),volume_pp=vol*scale,baseline_pp=b.mean()*scale,excess_pp=(vol-b.mean())*scale,short_excess_pp=(vol-short.mean())*scale if short.count()>=17 else np.nan,unit_gate_pass=not reason,exclusions=';'.join(reason)))
audit=pd.DataFrame(rows);audit.to_csv(O/'gate_and_volume.csv',index=False)
d=pd.read_csv(dpath);d=d[d.definition.isin(['documented_stable_family_subset','all_stable_family_candidates_sensitivity'])]
z=d.merge(audit,on=['event_id','RIC','review_cycle','type'],validate='m:1',suffixes=('','_audit'))
z['quantity_abs_pp']=z.net_company_pp.abs();z.to_csv(O/'joined_all.csv',index=False)
passed=z[z.unit_gate_pass].dropna(subset=['quantity_abs_pp','excess_pp']).copy()
summ=[];models=[]
for (definition,typ),g in passed.groupby(['definition','type']):
    rv=g.groupby('review_cycle')[['quantity_abs_pp','excess_pp','short_excess_pp','volume_pp','baseline_pp']].mean()
    for outcome in ['excess_pp','short_excess_pp','volume_pp']:
        r=rv[[outcome,'quantity_abs_pp']].dropna(); ans=fieller(r[outcome],r.quantity_abs_pp)
        ans.update(definition=definition,type=typ,outcome=outcome,N=int(g[outcome].notna().sum()))
        summ.append(ans)
for definition,g0 in passed.groupby('definition'):
    for typ in ['addition','deletion','pooled']:
        g=g0.copy() if typ=='pooled' else g0[g0.type.eq(typ)].copy()
        for control in [False,True]:
            X=pd.DataFrame({'quantity_abs_pp':g.quantity_abs_pp},index=g.index)
            if typ=='pooled':X['deletion']=g.type.eq('deletion').astype(float)
            if control:X['baseline_pp']=g.baseline_pp
            X=pd.concat([X,pd.get_dummies(g.review_cycle,drop_first=True,dtype=float)],axis=1)
            X=sm.add_constant(X).astype(float)
            w=1/g.groupby('review_cycle').event_id.transform('count')
            fit=sm.WLS(g.excess_pp,X,weights=w).fit(cov_type='cluster',cov_kwds={'groups':g.review_cycle},use_t=True)
            ci=fit.conf_int().loc['quantity_abs_pp']
            models.append(dict(definition=definition,type=typ,baseline_control=control,N=len(g),G=g.review_cycle.nunique(),slope=fit.params['quantity_abs_pp'],lo=ci.iloc[0],hi=ci.iloc[1],p=fit.pvalues['quantity_abs_pp'],r2=fit.rsquared))
pd.DataFrame(summ).to_csv(O/'volume_quantity_ratios.csv',index=False)
pd.DataFrame(models).to_csv(O/'diagnostic_slopes.csv',index=False)
(O/'hashes.json').write_text(json.dumps({str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [dpath,qpath,epath,ipath,O/'DECISIONS.txt',Path(__file__)]},indent=2))
print('Unit gate',audit.unit_gate_pass.value_counts().to_dict(),audit.exclusions.value_counts().to_dict())
print(pd.DataFrame(summ).to_string(index=False));print(pd.DataFrame(models).to_string(index=False))
