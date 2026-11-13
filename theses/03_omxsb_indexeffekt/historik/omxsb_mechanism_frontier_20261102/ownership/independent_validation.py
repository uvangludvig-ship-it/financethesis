from pathlib import Path
import pandas as pd,numpy as np,json,itertools,re,hashlib
from scipy.stats import t
import statsmodels.api as sm
O=Path(__file__).resolve().parent
F=pd.read_csv(O/'fund_event_role_ownership.csv.gz',dtype={'fund_id':str});H=pd.read_csv(O/'selected_full_fund_reports.csv.gz',dtype={'fund_id':str});S=pd.read_csv(O/'security_role_gate.csv');G=pd.read_csv(O/'H_fund_review_gate.csv',dtype={'fund_id':str});M=pd.read_csv(O/'fund_metadata_classification.csv',dtype={'fund_id':str});E=pd.read_csv(O/'event_ownership.csv');R=pd.read_csv(O/'results.csv')
assert F.groupby(['support','event_id','fund_id']).role.nunique().eq(4).all()
assert not F.duplicated(['support','event_id','fund_id','role']).any()
# Rebuild all binary ownership from the saved full reports using exact/accepted aliases, not producer outcomes.
lookup=S.set_index(['event_id','role']).to_dict('index');hg=H.groupby(['isin','fund_id','quarter']).qty.agg(list).to_dict()
rawbad=[];mistakes=[]
for x in F.itertuples():
 s=lookup[(x.event_id,x.role)]
 for col,dt in [('own_before',s['q0']),('own_after',s['q1'])]+([('own_minus',s['qminus'])]if x.support=='three_quarter_common'else[]):
  qs=[v for i in s['aliases'].split(';')for v in hg.get((i,x.fund_id,dt),[])]
  if any(not np.isfinite(v)or v<0 for v in qs):rawbad.append((x.event_id,x.role,x.fund_id,dt))
  got=int(sum(qs)>0)if qs else 0
  if got!=getattr(x,col):mistakes.append((x.event_id,x.role,x.fund_id,dt,got,getattr(x,col)))
assert not mistakes and not rawbad
# Independently reconstruct per-event matched ownership contrasts from fund rows.
T=F.groupby(['event_id','support','role'])[['own_minus','own_before','own_after']].mean()*100
rows=[]
for (eid,support),d in T.groupby(level=[0,1]):
 z=d.droplevel([0,1]);evt=z.loc['event'];c=z.loc[['c1','c2','c3']].mean();meta=E[(E.event_id==eid)&(E.support==support)].iloc[0]
 mp=(evt.own_after-evt.own_before)-(c.own_after-c.own_before);pr=(evt.own_before-evt.own_minus)-(c.own_before-c.own_minus)
 rows.append(dict(event_id=eid,support=support,type=meta.type,review=meta.review,issuer=meta.issuer,matched_post=mp,matched_pre=pr,acceleration=mp-pr,event_before=evt.own_before,control_before=c.own_before,event_after=evt.own_after,control_after=c.own_after))
A=pd.DataFrame(rows);merge=A.merge(E,on=['event_id','support'],suffixes=('_ind','_prod'),validate='one_to_one');fields=['matched_post','matched_pre','acceleration','event_before','control_before','event_after','control_after']
err={c:float((merge[c+'_ind']-merge[c+'_prod']).abs().max())for c in fields};assert max(err.values())<1e-10
cells=[]
for r in R.itertuples():
 q=A[(A.type==r.type)&(A.support==r.support)];v=q[r.metric];means=q.groupby('review')[r.metric].mean();n=len(means)
 fit=sm.OLS(means.to_numpy(),np.ones((n,1))).fit();ci=fit.conf_int()[0];mu=float(fit.params[0]);se=float(fit.bse[0]);signs=np.array(list(itertools.product([-1.,1.],repeat=n)));draw=signs*means.to_numpy();tv=draw.mean(1)/(draw.std(1,ddof=1)/np.sqrt(n));pv=float((abs(tv)>=abs(mu/se)-1e-12).mean())
 weights=1/q.groupby('review')[r.metric].transform('size');scores=pd.Series(weights.to_numpy()*(v.to_numpy()-mu)).groupby(q.issuer.to_numpy()).sum();K=len(scores);isig=np.sqrt(K/(K-1)*(scores*scores).sum())/weights.sum();ic=t.ppf(.975,K-1)*isig
 own=dict(N=len(q),G=n,issuers=K,estimate_pp=mu,ci_low=float(ci[0]),ci_high=float(ci[1]),p_exact_signflip=pv,issuer_cluster_ci_low=mu-ic,issuer_cluster_ci_high=mu+ic)
 dif={k:float(v-getattr(r,k))for k,v in own.items()};cells.append(dict(type=r.type,support=r.support,metric=r.metric,independent=own,differences=dif,passed=all(abs(v)<1e-10 for v in dif.values())))
assert all(x['passed']for x in cells)
# Metadata identity / complete-report check for every retained fund endpoint.
md=M.set_index(['quarter','fund_id']);fund_errors=[];isin_changes=[]
for x in G[G.eligible].itertuples():
 a,b=md.loc[(x.q0,x.fund_id)],md.loc[(x.q1,x.fund_id)]
 if not(a.n_instr>0 and b.n_instr>0 and a.label==b.label):fund_errors.append((x.review,x.fund_id))
 if a.fund_isin!=b.fund_isin:isin_changes.append(dict(review=x.review,fund_id=x.fund_id,pre=a.fund_isin,post=b.fund_isin))
assert not fund_errors
# Known latent invalidity rule: zero quantity with positive value; quantify it instead of guessing impact.
ids=set(S.aliases.str.split(';').explode());zeroq=H[H['isin'].isin(ids)&H.qty.eq(0)&H.value.gt(0)]
# Conservative same-name alias supplement: exact normalized instrument names across accepted aliases.
norm=lambda x:re.sub('[^a-z0-9]','',str(x).lower().replace('å','a').replace('ä','a').replace('ö','o'))
checks=dict(binary_records_reproduced=len(F),raw_negative_or_nonfinite_in_retained_ledger=len(rawbad),binary_discrepancies=len(mistakes),event_arithmetic_max_errors=err,all_8_inference_cells_pass=True,cells=cells,retained_fund_metadata_errors=fund_errors,fund_isin_changes=isin_changes,target_zero_quantity_positive_value_rows=len(zeroq),declared_group_note='Corrected nse is restricted to ordinary-stock ISINs in the historical Nasdaq roster; source code correction verified',identity_scope_note='Exact Nasdaq plus positive FI supports existence; first-token unknown-issuer screen is conservative but not exhaustive. This audit does not certify unobserved aliases.')
(O/'independent_validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps({k:v for k,v in checks.items()if k!='cells'},indent=2))
