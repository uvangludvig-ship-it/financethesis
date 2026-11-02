"""Independent role join and intercept-mean inference; does not import production code."""
from pathlib import Path
import hashlib,json
import numpy as np,pandas as pd,statsmodels.api as sm
from scipy.stats import t,ttest_1samp
O=Path(__file__).resolve().parent
p=O.parent/'persistence_corrected/event_paths.csv';f=O/'review_RIC_status.csv';r=O/'historical_main_persistence_results.csv'
D=pd.read_csv(p);F=pd.read_csv(f);R=pd.read_csv(r)
assert len(R)==20 and not R.duplicated(['controls','model','contrast']).any()
assert not F.duplicated(['review','ric']).any()
# Independently reshape the REAL event roles, never use provenance event_id/role from the status registry.
D['audit_row']=np.arange(len(D));rolemap={q+'_ric':q for q in ['event','c1','c2','c3']}
L=D[['audit_row','event_id','review','model']+list(rolemap)].melt(id_vars=['audit_row','event_id','review','model'],value_vars=list(rolemap),var_name='role_column',value_name='ric')
L['role']=L.role_column.map(rolemap)
L=L.merge(F[['review','ric','status']],how='left',on=['review','ric'],validate='many_to_one');L['eligible']=L.status.eq('confirmed_main_stock')
P=L.pivot(index='audit_row',columns='role',values='eligible')
D=D.join(P.add_prefix('role_ok_'),on='audit_row')
base=(D.type=='addition')&(D.post==1)
pri=D[base&(D.model=='market_adjusted')&D.common3&D[[f'role_ok_{z}'for z in ['event','c1','c2','c3']]].all(axis=1)]
E=pd.read_csv(O/'primary_event_eligibility.csv');expected=set(E.loc[E.strict_all_four_confirmed,'event_id']);assert set(pri.event_id)==expected and len(pri)==69 and pri.review.nunique()==18
version='repair-20261101-v5'
def rng(kind,label):
 seed=int.from_bytes(hashlib.sha256((version+str((kind,label))).encode()).digest()[:8],'little');return np.random.default_rng(seed)
def pval(sim,obs):
 hit=(abs(sim)>=abs(obs)-1e-12*max(1.,abs(obs))).sum();return float((hit+1)/(len(sim)+1))
checks=[]
for x in R.itertuples():
 nc=int(x.controls);need=['event']+['c'+str(i)for i in range(1,nc+1)]
 q=D[base&(D.model==x.model)&D['common'+str(nc)]&D[['role_ok_'+z for z in need]].all(axis=1)].copy()
 if x.contrast.startswith('level_'):h=int(x.contrast.split('_')[-1]);v=q[f'diff{nc}_{h}']
 else:assert x.contrast=='change_20_100';v=q[f'diff{nc}_100']-q[f'diff{nc}_20']
 z=pd.DataFrame({'y':v,'review':q.review}).replace([np.inf,-np.inf],np.nan).dropna();m=z.groupby('review',sort=True).y.mean().to_numpy();g=len(m)
 fit=sm.OLS(m,np.ones((g,1))).fit();ci=fit.conf_int(alpha=.05)[0]
 label=f'historical_main/{x.model}/{nc}/{x.contrast}'
 # Independent direct-outcome bootstrap for an intercept with one observation per review.
 w=rng('wild',label).choice([-1.,1.],size=(9999,g));Y=w*m[None,:]
 tboot=Y.mean(axis=1)/(Y.std(axis=1,ddof=1)/np.sqrt(g));obs=float(ttest_1samp(m,0).statistic)
 ws=rng('sign',label).choice([-1.,1.],size=(19999,g));signmeans=(ws*m[None,:]).mean(axis=1)
 own=dict(N=len(z),G=g,estimate_pp=float(fit.params[0]),event_weighted_mean_pp=float(z.y.mean()),ci_lo=float(ci[0]),ci_hi=float(ci[1]),p_signflip=pval(signmeans,m.mean()),p_wild=pval(tboot,obs))
 delta={k:float(own[k]-getattr(x,k))for k in own};passes=all(abs(v)<1e-10 for v in delta.values())
 checks.append(dict(model=x.model,controls=nc,contrast=x.contrast,pass_all=passes,independent=own,production={k:getattr(x,k)for k in own},differences=delta,event_ids=sorted(q.event_id.tolist())))
V=dict(task='Independent check of all20historical Main Market persistence cells',joins='meltactualeventroles -> merge(review,ric) many_to_one; provenanceevent_id/role ignored',primary_count=len(pri),primary_reviews=pri.review.nunique(),primary_event_ids_equal_to_eligibility_file=set(pri.event_id)==expected,primary_event_ids=sorted(pri.event_id.tolist()),all_cells_pass=all(c['pass_all']for c in checks),cell_count=len(checks),max_abs_numeric_difference=max(abs(v)for c in checks for v in c['differences'].values()),inference='statsmodels OLS intercept on review means, SciPy t test; direct restricted-null studentized bootstrap with documented same seeds; no production function imported',checks=checks,input_sha256={str(z):hashlib.sha256(z.read_bytes()).hexdigest()for z in [p,f,r,O/'primary_event_eligibility.csv']})
(O/'validation.json').write_text(json.dumps(V,indent=2));print(json.dumps({k:v for k,v in V.items()if k not in ['checks','input_sha256','primary_event_ids']},indent=2));assert V['all_cells_pass']
