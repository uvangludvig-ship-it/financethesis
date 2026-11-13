from pathlib import Path
import sys,json,hashlib,datetime
import numpy as np,pandas as pd,statsmodels.api as sm
O=Path(__file__).resolve().parent;C=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis')
sys.path.insert(0,str(C/'work/comparison_rebuild_20261102'))
from run import fieller
lock=json.loads((O/'UNIT_GATE_LOCK.json').read_text());assert hashlib.sha256((O/'unit_gate_all216.csv').read_bytes()).hexdigest()==lock['files'][str(O/'unit_gate_all216.csv')]
gate=pd.read_csv(O/'unit_gate_all216.csv',parse_dates=['AD','ED','before','after'])
qpath=R/'output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz';q=pd.read_csv(qpath,usecols=['event_id','fi_price_after','company_mcap_after']).drop_duplicates();assert not q.event_id.duplicated().any();gate=gate.merge(q,on='event_id',validate='1:1')
p=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','volume']);p=p[p.ric.isin(gate.RIC)];assert not p.duplicated(['ric','date']).any();s={k:g.set_index('date').sort_index() for k,g in p.groupby('ric')}
idx=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv');cal=pd.DatetimeIndex(sorted(pd.to_datetime(idx.loc[idx.ric.eq('.OMXSBGI'),'date']).dropna().unique()));rows=[]
for z in gate.itertuples():
 a=int(cal.searchsorted(z.AD));e=int(cal.searchsorted(z.ED));recon=cal[e-1];v=s[z.RIC].reindex(cal).volume;v=v.where(v.ge(0));b=v.iloc[a-61:a-11];short=v.iloc[e-22:e-1];factor=z.corrected_volume_factor_to_FI_after;scale=100*z.fi_price_after/z.company_mcap_after
 reason=[]
 if b.count()<40:reason.append('baseline_coverage')
 if not np.isfinite(v.loc[recon]):reason.append('missing_event_volume')
 r=dict(event_id=z.event_id,RIC=z.RIC,type=z.type,review_cycle=z.review_cycle,AD=z.AD,ED=z.ED,rebalancing_day=recon,after=z.after,unit_gate_pass=z.unit_gate_pass,volume_window_pass=not reason,original172_pass=z.original172_pass,exclusions=z.exclusions,window_exclusions=';'.join(reason),corrected_volume_factor_to_FI_after=factor,baseline_N=b.count(),shortbaseline_N=short.count(),FI_price=z.fi_price_after,company_mcap_after=z.company_mcap_after,raw_panel_EDminus1_volume=v.loc[recon],raw_panel_baseline=b.mean(),raw_panel_shortbaseline=short.mean(),volume_FI_after_units=v.loc[recon]*factor,baseline_volume_FI_after_units=b.mean()*factor,shortbaseline_volume_FI_after_units=short.mean()*factor)
 for prefix,f in [('corrected',factor),('legacy',1)]:
  r[prefix+'_volume_pp']=v.loc[recon]*scale*f;r[prefix+'_baseline_pp']=b.mean()*scale*f;r[prefix+'_excess_pp']=(v.loc[recon]-b.mean())*scale*f;r[prefix+'_short_excess_pp']=(v.loc[recon]-short.mean())*scale*f if short.count()>=17 else np.nan
 rows.append(r)
v=pd.DataFrame(rows);v.to_csv(O/'volume_input_all216.csv',index=False)
oldpath=R/'output/omxsb_mechanism_frontier_20261102/demand/event_demand_by_definition.csv';newpath=C/'work/mandate_upgrade_20261102/event_demand_updated.csv';d=pd.read_csv(oldpath);d=d[d.definition.isin(['documented_stable_family_subset','all_stable_family_candidates_sensitivity'])];newd=pd.read_csv(newpath);newd=newd[newd.definition.eq('updated_documented_continuity')];d=pd.concat([d,newd],ignore_index=True);assert not d.duplicated(['event_id','definition']).any();assert len(d)==216*3
z=d.merge(v,on=['event_id','RIC','review_cycle','type'],validate='m:1',suffixes=('','_volume'));z['quantity_abs_pp']=z.net_company_pp.abs();z.to_csv(O/'joined_quantities_volume_all216.csv',index=False)
summary=[];models=[];reviews=[]
samples={'original172_legacy':(z.original172_pass,'legacy'),'common166_legacy':(z.original172_pass&z.unit_gate_pass,'legacy'),'common166_corrected':(z.original172_pass&z.unit_gate_pass,'corrected'),'corrected205':(z.unit_gate_pass,'corrected')}
for sample,(mask,prefix) in samples.items():
 passed=z[mask&z.volume_window_pass].copy()
 for c in ['excess_pp','short_excess_pp','volume_pp','baseline_pp']:passed[c]=passed[prefix+'_'+c]
 for (definition,typ),g in passed.groupby(['definition','type']):
  rv=g.groupby('review_cycle')[['quantity_abs_pp','excess_pp','short_excess_pp','volume_pp','baseline_pp']].mean();rr=rv.reset_index();rr['sample']=sample;rr['definition']=definition;rr['type']=typ;reviews.append(rr)
  for outcome in ['excess_pp','short_excess_pp','volume_pp']:
   r=rv[[outcome,'quantity_abs_pp']].dropna();ans=fieller(r[outcome],r.quantity_abs_pp);ans.update(sample=sample,definition=definition,type=typ,outcome=outcome,N=int(g[outcome].notna().sum()));summary.append(ans)
 if sample!='corrected205':continue
 for definition,g0 in passed.groupby('definition'):
  for typ in ['addition','deletion','pooled']:
   g=g0.copy() if typ=='pooled' else g0[g0.type.eq(typ)].copy()
   for control in [False,True]:
    X=pd.DataFrame({'quantity_abs_pp':g.quantity_abs_pp},index=g.index)
    if typ=='pooled':X['deletion']=g.type.eq('deletion').astype(float)
    if control:X['baseline_pp']=g.baseline_pp
    X=pd.concat([X,pd.get_dummies(g.review_cycle,drop_first=True,dtype=float)],axis=1);X=sm.add_constant(X).astype(float);w=1/g.groupby('review_cycle').event_id.transform('count');fit=sm.WLS(g.excess_pp,X,weights=w).fit(cov_type='cluster',cov_kwds={'groups':g.review_cycle},use_t=True);ci=fit.conf_int().loc['quantity_abs_pp'];models.append(dict(sample=sample,definition=definition,type=typ,baseline_control=control,N=len(g),G=g.review_cycle.nunique(),slope=fit.params['quantity_abs_pp'],lo=ci.iloc[0],hi=ci.iloc[1],p=fit.pvalues['quantity_abs_pp'],r2=fit.rsquared))
pd.DataFrame(summary).to_csv(O/'volume_quantity_ratios.csv',index=False);pd.DataFrame(models).to_csv(O/'diagnostic_slopes.csv',index=False);pd.concat(reviews).to_csv(O/'review_level_means.csv',index=False)
(O/'ANALYSIS_RUN.json').write_text(json.dumps(dict(run_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit_gate_frozen_at=lock['frozen_at_utc'],unit_gate_hash=lock['files'][str(O/'unit_gate_all216.csv')],N_unit_pass=int(v.unit_gate_pass.sum()),N_analysis=int((v.unit_gate_pass&v.volume_window_pass).sum()),sample_sizes={k:int(m.sum()/3) for k,(m,p) in samples.items()},input_hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [oldpath,newpath,qpath,Path(__file__)]},no_CAR_loaded=True),indent=2))
print('window check',v.volume_window_pass.value_counts().to_dict());print(pd.DataFrame(summary).query("sample=='corrected205' and outcome=='excess_pp'").to_string(index=False));print(pd.DataFrame(models).to_string(index=False))
