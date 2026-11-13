from pathlib import Path
import re,json,hashlib
import pandas as pd,numpy as np
from scipy.stats import t
O=Path(__file__).resolve().parent
F=pd.read_csv(O/'decomp_fund_roles.csv.gz',dtype={'fund_id':str});M=pd.read_csv(O/'decomp_fund_groups.csv',dtype={'fund_id':str});Z=pd.read_csv(O/'fund_metadata_classification.csv',dtype={'fund_id':str})
M=M.merge(Z[['quarter','fund_id','company']].rename(columns={'quarter':'q1','company':'company_post'}),on=['q1','fund_id'],validate='m:1')
def norm(x):return re.sub(r'\s+',' ',str(x).strip().lower())
M['manager']=M.company.map(norm);M['same_manager']=M.manager==M.company_post.map(norm)
A=F.merge(M[['review','fund_id','manager','same_manager']],on=['review','fund_id'],validate='m:1')
rows=[]
for scope in ['fixed_before_company','stable_company_label']:
 a=A if scope=='fixed_before_company'else A[A.same_manager]
 for (ev,rev,ty),x in a.groupby(['event_id','review','type']):
  q=x.groupby(['role','manager'])[['own_before','own_after']].max().reset_index();q['new_company']=(q.own_before==0)&(q.own_after==1)
  x=x.merge(q[['role','manager','own_before']].rename(columns={'own_before':'company_before_owner'}),on=['role','manager'],validate='m:1');x['net']=x.own_after-x.own_before;x['within_old_company_net']=x.net*x.company_before_owner;x['new_company_fund_net']=x.net*(1-x.company_before_owner)
  counts=q.groupby('role')[['own_before','own_after','new_company']].sum();changes=x.groupby('role')[['net','within_old_company_net','new_company_fund_net']].sum()
  allm=pd.concat([counts,changes],axis=1).reindex(['event','c1','c2','c3'],fill_value=0);e=allm.loc['event'];c=allm.loc[['c1','c2','c3']].mean()
  rows.append(dict(event_id=ev,review=rev,type=ty,scope=scope,event_company_before=e.own_before,control_company_before=c.own_before,event_company_after=e.own_after,control_company_after=c.own_after,matched_company_net=(e.own_after-e.own_before)-(c.own_after-c.own_before),matched_new_companies=e.new_company-c.new_company,matched_fund_net=e.net-c.net,matched_within_old_company_net=e.within_old_company_net-c.within_old_company_net,matched_new_company_fund_net=e.new_company_fund_net-c.new_company_fund_net,N_funds=int(x[x.role=='event'].shape[0])))
E=pd.DataFrame(rows);E.to_csv(O/'manager_event_counts.csv',index=False);assert np.allclose(E.matched_fund_net,E.matched_within_old_company_net+E.matched_new_company_fund_net)
results=[]
for (ty,scope),q in E.groupby(['type','scope']):
 g=q.groupby('review');G=g.ngroups
 for metric in ['matched_company_net','matched_new_companies','matched_fund_net','matched_within_old_company_net','matched_new_company_fund_net']:
  z=g[metric].mean();mu=z.mean();half=t.ppf(.975,G-1)*z.std(ddof=1)/np.sqrt(G);results.append(dict(type=ty,scope=scope,metric=metric,N=len(q),G=G,estimate=mu,ci_low=mu-half,ci_high=mu+half))
R=pd.DataFrame(results);R.to_csv(O/'manager_results.csv',index=False)
base=pd.read_csv(O/'decomp_event_groups.csv');j=E[E.scope=='fixed_before_company'].merge(base[base.group=='ALL'][['event_id','matched_change']],on='event_id',validate='1:1');err=float((j.matched_fund_net-j.matched_change).abs().max());assert err<1e-12
check=dict(additive_partition=True,original_all_fund_max_error=err,manager_stability_excluded_fund_review_pairs=int((~M.same_manager).sum()),distinct_pre_company_labels=M.manager.nunique(),decision_sha256=hashlib.sha256((O/'MANAGER_COUNT_DECISIONS.txt').read_bytes()).hexdigest())
(O/'manager_validation.json').write_text(json.dumps(check,indent=2));print(R.to_string(index=False));print(json.dumps(check,indent=2))
