from pathlib import Path
import pandas as pd,numpy as np,json,re,hashlib
import statsmodels.api as sm
O=Path(__file__).resolve().parent
paths=[O/x for x in ['decomp_fund_roles.csv.gz','decomp_fund_groups.csv','fund_metadata_classification.csv','manager_event_counts.csv','manager_results.csv','decomp_event_groups.csv']];hash0={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
F=pd.read_csv(paths[0],dtype={'fund_id':str});M=pd.read_csv(paths[1],dtype={'fund_id':str});Z=pd.read_csv(paths[2],dtype={'fund_id':str});E=pd.read_csv(paths[3]);R=pd.read_csv(paths[4]);D=pd.read_csv(paths[5]);assert len(R)==20
norm=lambda x:re.sub(r'\s+',' ',str(x).strip().lower())
md=Z.set_index(['quarter','fund_id']).company.to_dict();M['manager_before']=M.company.map(norm);M['manager_after']=[norm(md[(q,f)])for q,f in zip(M.q1,M.fund_id)];M['stable']=M.manager_before.eq(M.manager_after)
missing=M.company.isna()|M.manager_before.isin(['','nan','none']);assert not missing.any(),'Missing labels cannot be grouped as one company.'
F=F.merge(M[['review','fund_id','manager_before','stable']],on=['review','fund_id'],validate='many_to_one');assert not F.manager_before.isna().any()
rec=[]
for scope in ['fixed_before_company','stable_company_label']:
 a=F if scope=='fixed_before_company'else F[F.stable]
 assert a.groupby(['event_id','fund_id']).role.nunique().eq(4).all()
 for (eid,review,typ),q in a.groupby(['event_id','review','type']):
  role={}
  for r,ss in q.groupby('role'):
   bm=set(ss.loc[ss.own_before.eq(1),'manager_before']);am=set(ss.loc[ss.own_after.eq(1),'manager_before']);dv=ss.own_after.to_numpy()-ss.own_before.to_numpy();old=ss.manager_before.isin(bm).to_numpy()
   role[r]=dict(event_company_before=len(bm),event_company_after=len(am),matched_company_net=len(am)-len(bm),matched_new_companies=len(am-bm),matched_fund_net=int(dv.sum()),matched_within_old_company_net=int(dv[old].sum()),matched_new_company_fund_net=int(dv[~old].sum()),N_funds=len(ss))
  assert set(role)=={'event','c1','c2','c3'};r=dict(event_id=eid,review=review,type=typ,scope=scope)
  for k in ['matched_company_net','matched_new_companies','matched_fund_net','matched_within_old_company_net','matched_new_company_fund_net']:r[k]=role['event'][k]-sum(role[c][k]for c in ['c1','c2','c3'])/3
  r['event_company_before']=role['event']['event_company_before'];r['event_company_after']=role['event']['event_company_after'];r['control_company_before']=sum(role[c]['event_company_before']for c in ['c1','c2','c3'])/3;r['control_company_after']=sum(role[c]['event_company_after']for c in ['c1','c2','c3'])/3;r['N_funds']=role['event']['N_funds'];rec.append(r)
A=pd.DataFrame(rec);J=A.merge(E,on=['event_id','scope'],suffixes=('_ind','_prod'),validate='one_to_one');cols=[c for c in A if c not in ['event_id','review','type','scope']];err={c:float((J[c+'_ind']-J[c+'_prod']).abs().max())for c in cols};assert max(err.values())<1e-10
partition_error=float((A.matched_fund_net-A.matched_within_old_company_net-A.matched_new_company_fund_net).abs().max());assert partition_error<1e-10
j=A[A.scope=='fixed_before_company'].merge(D[D.group=='ALL'][['event_id','matched_change']],on='event_id',validate='one_to_one');baseerr=float((j.matched_fund_net-j.matched_change).abs().max());assert baseerr<1e-10
cells=[]
for x in R.itertuples():
 q=A[(A.type==x.type)&(A.scope==x.scope)];y=q.groupby('review')[x.metric].mean();fit=sm.OLS(y.to_numpy(),np.ones((len(y),1))).fit();ci=fit.conf_int()[0];own=dict(N=len(q),G=len(y),estimate=float(fit.params[0]),ci_low=float(ci[0]),ci_high=float(ci[1]));diff={k:float(v-getattr(x,k))for k,v in own.items()};cells.append(dict(type=x.type,scope=x.scope,metric=x.metric,independent=own,differences=diff,passed=all(abs(v)<1e-10 for v in diff.values())))
assert all(c['passed']for c in cells)
hash1={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths};assert hash0==hash1,'Inputs changed during audit.'
out=dict(all20_cells_pass=True,source_fund_role_rows=len(F),event_scope_rows=len(A),event_count=A.event_id.nunique(),missing_company_labels=int(missing.sum()),distinct_before_labels=M.manager_before.nunique(),unstable_company_fund_review_pairs=int((~M.stable).sum()),event_arithmetic_max_errors=err,partition_max_error=partition_error,fixed_scope_reconciles_ALL_max_error=baseerr,cells=cells,input_hashes=hash1,interpretation='Counts of fixed reported company labels, not independent investors/teams; within-old and new-company fund components are NET changes, not gross entries. New means absent in the included balanced fund panel at q0.')
(O/'independent_manager_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k not in ['cells','input_hashes']},indent=2))
