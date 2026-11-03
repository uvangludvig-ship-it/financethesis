from pathlib import Path
import os,json,hashlib,datetime
import pandas as pd,numpy as np
from scipy.stats import t
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis'));OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership';DQ=R/'output/omxsb_open_questions_20261102/demand_quarter'
G=pd.read_csv(O/'security_feasibility_gate.csv');EG=pd.read_csv(O/'event_feasibility_gate.csv');keep=set(EG.loc[EG.gate_pass,'event_id'])
S=pd.read_csv(OWN/'security_role_gate.csv');S=S[S.event_id.isin(keep)].merge(G[['review','ric','factor']],on=['review','ric'],validate='m:1')
F=pd.read_csv(OWN/'decomp_fund_roles.csv.gz',dtype={'fund_id':str});F=F[F.event_id.isin(keep)]
B=pd.read_csv(O/'invalid_fund_role_pairs.csv',dtype={'fund_id':str});MERGE='51437'
cols={'ISIN-kod_instrument':'isin','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','Antal':'qty','Marknadsvärde_instrument':'value','Valuta':'currency','Tillgångsslag_enligt_LVF_5_kap':'asset_type'}
ids=set(S.aliases.str.split(';').explode());dates=set(S.q0)|set(S.q1);parts=[]
for c in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=list(cols),chunksize=300000,dtype={'Fond_institutnummer':str}):
 c=c.rename(columns=cols);parts.append(c[c['isin'].isin(ids)&c.quarter.isin(dates)])
H=pd.concat(parts,ignore_index=True)
for c in ['qty','value']:H[c]=pd.to_numeric(H[c],errors='coerce')
P=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','mcap']);P=P[P.ric.isin(S.ric)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
REPORTS=pd.read_csv(DQ/'raw_fund_report_metadata.csv',dtype={'Fond_institutnummer':str});REPOK={date:set(z.loc[z.actual_instrument_rows.gt(0),'Fond_institutnummer']) for date,z in REPORTS.groupby('Kvartalsslut')}
canonical=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand/denominator_audit.csv').set_index('event_id');ledgerQ=pd.read_csv(DQ/'fund_event_quarter_changes.csv.gz',dtype={'fund_id':str}).set_index(['event_id','fund_id'])
cache={}
for (review,ric),ss in S.groupby(['review','ric']):
 x=ss.iloc[0];z=H[H['isin'].isin(x.aliases.split(';'))&H.quarter.isin([x.q0,x.q1])];qt=z.groupby(['fund_id','quarter']).qty.sum(min_count=1).to_dict()
 aft=z[z.quarter.eq(x.q1)&z.asset_type.eq('ÖverlåtbartVärdepapper')&z.currency.eq('SEK')&z.qty.gt(0)&z.value.gt(0)];price=float((aft.value/aft.qty).median());cap=float(P[P.ric.eq(ric)&P.date.le(pd.Timestamp(x.q1))&P.mcap.gt(0)].tail(1).mcap.iloc[0])
 invalid=set(B.loc[B.review.eq(review)&B.ric.eq(ric),'fund_id'])
 cache[(review,ric)]=(qt,price,cap,invalid)
# Freeze final input/code hashes immediately before first outcome arithmetic.
lock={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'no_new_capital_outcomes_read_yet':True,'events':len(keep),'files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'DESIGN_LOCK.txt',O/'GATE_AMENDMENT_BEFORE_OUTCOMES.txt',O/'security_feasibility_gate.csv',O/'event_feasibility_gate.csv',O/'gate.py',O/'QA_REPORT_SUPPORT_CORRECTION.txt',Path(__file__)]}}
lockpath=O/'ANALYSIS_LOCK.json'
if lockpath.exists():lockpath=O/'REPLAY_LOCK.json';lock['no_new_capital_outcomes_read_yet']=False;lock['prior_results_known']=True
lockpath.write_text(json.dumps(lock,indent=2))
rows=[];coverage=[];checks={'raw_ownership_status_checks':0,'prior_event_quantity_checks':0,'max_prior_event_quantity_error':0.,'max_prior_event_pp_error':0.};private=[]
for eid,ss in S.groupby('event_id'):
 f=F[F.event_id.eq(eid)];original=set(f.loc[f.role.eq('event'),'fund_id']);bad=set().union(*(cache[(x.review,x.ric)][3] for x in ss.itertuples()));bad|={MERGE} if ss.review.iloc[0]=='2022H1' else set();good=(original-bad)&REPOK[ss.q0.iloc[0]]&REPOK[ss.q1.iloc[0]];bad=original-good
 assert len(good)>0
 for role,z in f.groupby('role'):assert set(z.fund_id)==original
 coverage.append(dict(event_id=eid,review=ss.review.iloc[0],type=ss.type.iloc[0],original_funds=len(original),retained_funds=len(good),excluded_fund_ids=';'.join(sorted(original&bad)),known_merger_excluded=bool(MERGE in original and ss.review.iloc[0]=='2022H1')))
 for x in ss.itertuples():
  qt,price,cap,_=cache[(x.review,x.ric)];z=f[f.role.eq(x.role)&f.fund_id.isin(good)]
  for a in z.itertuples():
   q0=float(qt.get((a.fund_id,x.q0),0));q1=float(qt.get((a.fund_id,x.q1),0));assert q0>=0 and q1>=0 and np.isfinite(q0+q1)
   assert int(q0>0)==a.own_before and int(q1>0)==a.own_after;checks['raw_ownership_status_checks']+=2
   kind='new' if q0==0 and q1>0 else ('continuing' if q0>0 and q1>0 else ('exiting' if q0>0 and q1==0 else 'neither'))
   delta=q1-x.factor*q0;pp=100*delta*price/cap
   if x.role=='event':
    cq=ledgerQ.loc[(eid,a.fund_id)];checks['prior_event_quantity_checks']+=1;err=max(abs(q0-cq.before_quantity),abs(q1-cq.after_quantity));checks['max_prior_event_quantity_error']=max(checks['max_prior_event_quantity_error'],err);checks['max_prior_event_pp_error']=max(checks['max_prior_event_pp_error'],abs(pp-cq.delta_company_pp));assert err<1e-8 and abs(pp-cq.delta_company_pp)<1e-10
   rows.append(dict(event_id=eid,review=x.review,type=x.type,role=x.role,fund_id=a.fund_id,group=a.group,component=kind,pp=pp))
   # A minimal private checkpoint is omitted from delivery; raw public FI quantities never shipped with results.
D=pd.DataFrame(rows);D.to_csv(O/'normalized_fund_role_contributions.csv.gz',index=False,compression='gzip');groups=sorted(D.group.unique());components=['new','continuing','exiting'];eventrows=[]
for (eid,review,typ),d in D.groupby(['event_id','review','type']):
 for group in groups+['ALL','OMXSB_family']:
  dd=d if group=='ALL' else (d[d.group.str.startswith('OMXSB_')] if group=='OMXSB_family' else d[d.group.eq(group)])
  tab=dd.groupby(['role','component']).pp.sum().unstack(fill_value=0).reindex(index=['event','c1','c2','c3'],columns=components,fill_value=0).fillna(0)
  val=dict(event_id=eid,review=review,type=typ,group=group)
  for component in components:
   val['event_'+component]=float(tab.loc['event',component]);val['control_'+component]=float(tab.loc[['c1','c2','c3'],component].mean());val['matched_'+component]=val['event_'+component]-val['control_'+component]
  for prefix in ['event','control','matched']:
   val[prefix+'_total']=sum(val[prefix+'_'+c] for c in components);val[prefix+'_preexisting']=val[prefix+'_continuing']+val[prefix+'_exiting'];val[prefix+'_new_minus_preexisting']=val[prefix+'_new']-val[prefix+'_preexisting']
  eventrows.append(val)
E=pd.DataFrame(eventrows);E.to_csv(O/'event_component_results.csv',index=False)
metrics=[c for c in E if c not in ['event_id','review','type','group']]
V=E.groupby(['type','group','review'])[metrics].mean().reset_index();V.to_csv(O/'review_component_results.csv',index=False)
summary=[]
for (typ,group),z in V.groupby(['type','group']):
 for metric in metrics:
  y=z[metric].to_numpy();N=int(E[E.type.eq(typ)&E.group.eq(group)].shape[0]);G=len(y);mean=float(y.mean());se=float(y.std(ddof=1)/np.sqrt(G));half=float(t.ppf(.975,G-1)*se)
  summary.append(dict(type=typ,group=group,metric=metric,N_events=N,G_reviews=G,mean_pp=mean,se_pp=se,ci95_low=mean-half,ci95_high=mean+half,is_primary=typ=='addition' and group=='ALL' and metric=='matched_new_minus_preexisting'))
A=pd.DataFrame(summary);A.to_csv(O/'summary.csv',index=False)
primary=A[A.is_primary];primary.to_csv(O/'primary_contrast.csv',index=False)
# Covariance of review-weighted means preserves subtraction identities.
covs=[]
for typ,z in V[V.group.eq('ALL')].groupby('type'):
 vals=z[['matched_new','matched_continuing','matched_exiting']];cv=vals.cov()/len(z)
 for i in cv.index:
  for j in cv.columns:covs.append(dict(type=typ,row=i,column=j,covariance_of_mean=float(cv.loc[i,j])))
pd.DataFrame(covs).to_csv(O/'component_covariance.csv',index=False)
pd.DataFrame(coverage).to_csv(O/'fund_support.csv',index=False)
checks.update(events=len(keep),additions=int(E[E.group.eq('ALL')&E.type.eq('addition')].shape[0]),deletions=int(E[E.group.eq('ALL')&E.type.eq('deletion')].shape[0]),reviews=int(E.review.nunique()),fund_role_rows=len(D),inference='t intervals over equal-weight review means; exploratory nominal',completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
for prefix in ['event','control','matched']:
 assert np.allclose(E[prefix+'_total'],sum(E[prefix+'_'+c] for c in components),atol=1e-12)
 base=E[E.group.isin(groups)].groupby('event_id')[prefix+'_total'].sum();total=E[E.group.eq('ALL')].set_index('event_id')[prefix+'_total'];assert np.allclose(base.sort_index(),total.sort_index(),atol=1e-12)
checks['component_and_benchmark_identities_pass']=True
(O/'validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2));print(A[A.group.eq('ALL')&A.metric.str.startswith('matched')].to_string(index=False))
