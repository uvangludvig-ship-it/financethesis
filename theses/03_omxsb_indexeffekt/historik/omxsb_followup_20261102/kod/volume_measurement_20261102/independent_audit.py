from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import analysis_paths
_PORTABLE_REPO, _PORTABLE_OUT = analysis_paths('volume_measurement_20261102')
import pandas as pd,numpy as np,json,hashlib,sys
from scipy.stats import t
O=_PORTABLE_OUT;R=_PORTABLE_REPO
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'comparison_rebuild_20261102'))
from independent_audit import independent_ratio
pfile=R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet';ifile=R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv';efile=R/'output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv';qfile=R/'output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz';dfile=R/'output/omxsb_mechanism_frontier_20261102/demand/event_demand_by_definition.csv'
A=pd.read_csv(O/'gate_and_volume.csv');J=pd.read_csv(O/'joined_all.csv');E=pd.read_csv(efile,parse_dates=['before','after']);C=pd.read_csv(ifile,parse_dates=['date']);C=C[C.ric.eq('.OMXSBGI')];cal=pd.DatetimeIndex(C.date.dropna().sort_values().unique());validcal=pd.DatetimeIndex(C.loc[C.close.notna(),'date'].dropna().sort_values().unique());assert cal.equals(validcal),'Calendar includes missing index closes'
D=pd.read_csv(R/'output/omxsb_replication_2007/events_car.csv',usecols=['event_id','AD','ED'],parse_dates=['AD','ED']);E=E.merge(D,on='event_id',validate='1:1');Q=pd.read_csv(qfile,usecols=['event_id','fi_price_after','company_mcap_after']).drop_duplicates();assert not Q.event_id.duplicated().any();E=E.merge(Q,on='event_id',validate='1:1')
P=pd.read_parquet(pfile,columns=['ric','date','close','volume']);P=P[P.ric.isin(E.RIC)];assert not P.duplicated(['ric','date']).any();P={r:g.set_index('date').sort_index() for r,g in P.groupby('ric')}
ca=pd.read_csv(R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',parse_dates=['action_date']);checks=[];rows=[];splitcheck=[]
for x in E.itertuples():
    assert x.AD in cal and x.ED in cal
    i=cal.get_loc(x.AD);j=cal.get_loc(x.ED)
    basedates=cal[[i+k for k in range(-61,-11)]];shortdates=cal[[j+k for k in range(-22,-1)]];ed=cal[j-1]
    assert len(basedates)==50 and len(shortdates)==21
    s=P[x.RIC];bv=s.reindex(basedates).volume;sv=s.reindex(shortdates).volume;bv=bv[bv.ge(0)];sv=sv[sv.ge(0)];v=s.reindex([ed]).volume.iloc[0];v=v if np.isfinite(v)and v>=0 else np.nan
    ps=s.loc[s.index<=x.after,'close'].dropna();dt=ps.index[-1];px=ps.iloc[-1];pr=px/x.fi_price_after;scale=100*x.fi_price_after/x.company_mcap_after;assert np.isfinite(scale)and scale>0
    reason=[]
    if abs(x.factor-1)>1e-10:reason.append('known_split_conversion')
    if (x.after-dt).days>5:reason.append('stale_quarter_price')
    if not np.isfinite(pr)or abs(pr-1)>.02:reason.append('cross_source_price_unit_gate')
    if len(bv)<40:reason.append('baseline_coverage')
    if not np.isfinite(v):reason.append('missing_event_volume')
    z=dict(event_id=x.event_id,rebalancing_day=str(ed.date()),after_panel_price=px,FI_price=x.fi_price_after,price_ratio=pr,price_date=str(dt.date()),baseline_N=len(bv),shortbaseline_N=len(sv),volume=v,baseline_volume=bv.mean(),shortbaseline_volume=sv.mean(),volume_pp=v*scale,baseline_pp=bv.mean()*scale,excess_pp=(v-bv.mean())*scale,short_excess_pp=(v-sv.mean())*scale if len(sv)>=17 else np.nan,unit_gate_pass=not reason,exclusions=';'.join(reason),scale=scale,company_mcap=x.company_mcap_after,baseline_first=str(basedates[0].date()),baseline_last=str(basedates[-1].date()),short_first=str(shortdates[0].date()),short_last=str(shortdates[-1].date()))
    rows.append(z)
    for c in ca[ca.RIC.eq(x.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.gt(basedates[0])&ca.action_date.le(x.after)].itertuples():
        splitcheck.append(dict(event_id=x.event_id,RIC=x.RIC,split_date=str(c.action_date.date()),factor=c.factor,passes_gate=not reason))
B=pd.DataFrame(rows);A.exclusions=A.exclusions.fillna('');Z=B.merge(A,on='event_id',suffixes=('_ind','_prod'),validate='1:1');num=['after_panel_price','FI_price','price_ratio','baseline_N','shortbaseline_N','volume','baseline_volume','shortbaseline_volume','volume_pp','baseline_pp','excess_pp','short_excess_pp'];errs={k:float((Z[k+'_ind']-Z[k+'_prod']).abs().max())for k in num};assert all(np.allclose(Z[k+'_ind'],Z[k+'_prod'],equal_nan=True,rtol=1e-11,atol=1e-8)for k in num)
for k in ['rebalancing_day','price_date','unit_gate_pass','exclusions']:assert Z[k+'_ind'].equals(Z[k+'_prod']),k
B.to_csv(O/'independent_window_and_unit_checks.csv',index=False)
d=pd.read_csv(dfile);d=d[d.definition.isin(['documented_stable_family_subset','all_stable_family_candidates_sensitivity'])];D=d.merge(B,on='event_id',validate='m:1');D['quantity_abs_pp']=D.net_company_pp.abs();assert len(D)==len(J)==432;assert set(zip(D.definition,D.event_id))==set(zip(J.definition,J.event_id));C=D[D.unit_gate_pass].dropna(subset=['quantity_abs_pp','excess_pp']);assert C.event_id.nunique()==172
rat=[]
for x in pd.read_csv(O/'volume_quantity_ratios.csv').itertuples():
    q=C[(C.definition==x.definition)&(C.type==x.type)].copy();assert q[x.outcome].notna().all(),'Potential different numerator/denominator event samples'
    vv=q.groupby('review_cycle')[[x.outcome,'quantity_abs_pp']].mean();a,cov=independent_ratio(vv[x.outcome],vv.quantity_abs_pp);a['N']=len(q);dif={k:float(a[k]-getattr(x,k))for k in ['ratio','den_mean','num_mean','G','lo','hi','N']};assert max(abs(z)for z in dif.values())<1e-10;assert a['fieller_type']==x.fieller_type;rat.append(dict(definition=x.definition,type=x.type,outcome=x.outcome,independent=a,differences=dif,covariance=cov))
models=[]
for x in pd.read_csv(O/'diagnostic_slopes.csv').itertuples():
    q=C[C.definition==x.definition].copy();q=q if x.type=='pooled'else q[q.type==x.type]
    names=['intercept','quantity'];xs=[np.ones(len(q)),q.quantity_abs_pp.to_numpy()]
    if x.type=='pooled':xs.append(q.type.eq('deletion').to_numpy().astype(float));names.append('deletion')
    if x.baseline_control:xs.append(q.baseline_pp.to_numpy());names.append('baseline')
    for r in sorted(q.review_cycle.unique())[1:]:xs.append(q.review_cycle.eq(r).to_numpy().astype(float));names.append(r)
    X=np.column_stack(xs);Y=q.excess_pp.to_numpy();W=(1/q.groupby('review_cycle').event_id.transform('count')).to_numpy();N,K=X.shape;G=q.review_cycle.nunique();assert np.linalg.matrix_rank(X)==K
    bread=np.linalg.inv(X.T@(W[:,None]*X));beta=bread@(X.T@(W*Y));u=Y-X@beta;scores=[]
    for rev in q.review_cycle.unique():
        ix=q.review_cycle.eq(rev).to_numpy();scores.append(X[ix].T@(W[ix]*u[ix]))
    scores=np.array(scores);V=bread@(scores.T@scores)@bread*(G/(G-1))*((N-1)/(N-K));se=np.sqrt(V[1,1]);half=t.ppf(.975,G-1)*se;rr=1-np.sum(W*u*u)/np.sum(W*(Y-np.average(Y,weights=W))**2)
    a=dict(N=N,G=G,slope=beta[1],lo=beta[1]-half,hi=beta[1]+half,p=2*t.sf(abs(beta[1]/se),G-1),r2=rr);dif={k:float(a[k]-getattr(x,k))for k in a};assert max(abs(z)for z in dif.values())<1e-8
    models.append(dict(definition=x.definition,type=x.type,baseline_control=bool(x.baseline_control),independent=a,cluster_small_sample_factor=(G/(G-1))*((N-1)/(N-K)),cluster_t_df=G-1,differences=dif))
# AFTER-RESULT VALIDATION DIAGNOSTIC, not a replacement regression or a p-value.
# Exact expected within-review covariance after random permutation of raw absolute Q among each review/type.
diag=[]
for (definition,typ),q in C.groupby(['definition','type']):
    q=q.copy();q['raw_abs_q']=q.quantity_abs_pp/q.scale;q['Y']=q.excess_pp;q['X']=q.quantity_abs_pp
    q['dy']=q.Y-q.groupby('review_cycle').Y.transform('mean');q['dx']=q.X-q.groupby('review_cycle').X.transform('mean');q['w']=1/q.groupby('review_cycle').event_id.transform('count');q['expected_shuffled_X']=q.scale*q.groupby('review_cycle').raw_abs_q.transform('mean')
    obs=float((q.w*q.dx*q.dy).sum()/q.review_cycle.nunique());exp=float((q.w*q.expected_shuffled_X*q.dy).sum()/q.review_cycle.nunique())
    diag.append(dict(definition=definition,type=typ,N=len(q),G=q.review_cycle.nunique(),observed_within_review_covariance_pp2=obs,expected_covariance_if_raw_Q_permuted_within_review_pp2=exp,expected_div_observed=exp/obs,interpretation='Exact permutation expectation as a shared-scale diagnostic, NOT estimated causal/bias fraction; raw Q exchangeability is illustrative, not asserted.'))
pd.DataFrame(diag).to_csv(O/'independent_shared_scale_diagnostic.csv',index=False)
out=dict(raw_windows_all216_pass=True,ED_AD_exact_calendar_dates=True,index_calendar_equals_nonmissing_close_calendar=True,gate_pass_events=172,gate_exclusions=A.exclusions.value_counts().to_dict(),raw_numeric_max_errors=errs,all12_ratio_cells_pass=True,all12_WLS_cluster_cells_pass=True,known_split_events_in_baseline_to_quarter=splitcheck,negative_excess_passed_event_count=int(B[B.unit_gate_pass].excess_pp.lt(0).sum()),shortbaseline_missing_passed_event_count=int(B[B.unit_gate_pass].short_excess_pp.isna().sum()),ratios=rat,regressions=models,shared_scale_diagnostic=diag,input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [pfile,ifile,efile,qfile,dfile,O/'gate_and_volume.csv',O/'joined_all.csv',O/'volume_quantity_ratios.csv',O/'diagnostic_slopes.csv']})
(O/'independent_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k not in ['ratios','regressions','input_hashes']},indent=2))
