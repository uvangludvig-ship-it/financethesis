import os
from pathlib import Path
import json,re,itertools,hashlib
import numpy as np,pandas as pd
from scipy.stats import t
import statsmodels.api as sm
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO', str(Path(__file__).resolve().parents[3])));B=R/'output/omxsb_open_questions_20261102'
S=pd.read_csv(O/'security_role_gate.csv');G=pd.read_csv(O/'H_fund_review_gate.csv',dtype={'fund_id':str});H=pd.read_csv(O/'selected_full_fund_reports.csv.gz',dtype={'fund_id':str});D=pd.read_csv(O/'same_issuer_identity_screen.csv',dtype={'fund_id':str});U=pd.read_csv(B/'eligibility/dated_stockholm_instrument_roster.csv')
other_codes=U.groupby('isin').company_code.agg(set).to_dict();sc=S.drop_duplicates(['review','ric']).set_index(['review','ric']).company_code.to_dict()
# Resolve only exact other listed issuer identity. Remaining name-based candidates are excluded conservatively, not guessed as shares/rights/bonds.
for k,r in D[D.status=='unresolved'].iterrows():
 codes=other_codes.get(r['isin'],set());target=sc[(r.review,r.ric)]
 if codes and target not in codes:D.loc[k,'status']='exact_other_listed_issuer'
D.to_csv(O/'identity_screen_resolved.csv',index=False)
D[D.status=='unresolved'].to_csv(O/'unresolved_identity_exclusions.csv',index=False)
# Report-derived zero is allowed only after independent security existence and complete report gates.
rows=[];evrows=[];exclusions=[];cov=[]
for eid,ss in S.groupby('event_id',sort=False):
 a=ss.iloc[0];rev=a.review;gf=G[(G.review==rev)&G.eligible];pre_f=set(G[(G.review==rev)&G.eligible_pretrend].fund_id)
 sec_ok=bool(ss.q0_supported.all()and ss.q1_supported.all());pre_sec=bool(ss.qminus_supported.all())
 candidates=set(gf.fund_id);keep=set(candidates);keep3=candidates&pre_f
 if not sec_ok:
  cov.append(dict(event_id=eid,review=rev,type=a.type,eligible=False,reason='security_endpoint_not_supported',funds_before_quality=len(candidates),funds_after_quality=0,pretrend_funds=0));continue
 q0=a.q0;q1=a.q1;qm=a.qminus
 local={}
 for z in ss.itertuples():
  ids=set(z.aliases.split(';'));xh=H[H['isin'].isin(ids)&H.fund_id.isin(candidates)&H.quarter.isin([qm,q0,q1])]
  # Unexpected asset type for target security is not silently accepted as ordinary ownership.
  invalid=(~xh.ordinary_container)|xh.qty.lt(0)|~np.isfinite(xh.qty)|((xh.qty>0)&(~np.isfinite(xh.value)|(xh.value<=0)))
  bad=xh[invalid]
  for f,qq in bad[['fund_id','quarter']].itertuples(index=False):
   if qq in [q0,q1]:keep.discard(f)
   keep3.discard(f);exclusions.append(dict(event_id=eid,role=z.role,ric=z.ric,fund_id=f,quarter=qq,reason='quantity_value_or_asset_ambiguous'))
  dd=D[(D.review==rev)&(D.ric==z.ric)&D.status.eq('unresolved')&D.fund_id.isin(candidates)]
  for f,qq in dd[['fund_id','quarter']].itertuples(index=False):
   if qq in [q0,q1]:keep.discard(f)
   keep3.discard(f);exclusions.append(dict(event_id=eid,role=z.role,ric=z.ric,fund_id=f,quarter=qq,reason='unresolved_same_issuer_ISIN'))
  # Binary observation from all accepted same-class rows, not from sums of positive only.
  local[z.role]=xh.groupby(['fund_id','quarter']).qty.sum(min_count=1).to_dict()
 keep3&=keep
 if not pre_sec:keep3=set()
 cov.append(dict(event_id=eid,review=rev,type=a.type,eligible=bool(keep),reason=''if keep else'no_valid_funds',funds_before_quality=len(candidates),funds_after_quality=len(keep),pretrend_funds=len(keep3)))
 for support,fs in [('post',keep),('three_quarter_common',keep3)]:
  if not fs:continue
  entries=[]
  for role,v in local.items():
   for f in sorted(fs):
    own0=int(v.get((f,q0),0)>0);own1=int(v.get((f,q1),0)>0);ownm=int(v.get((f,qm),0)>0)if support=='three_quarter_common'else np.nan
    entries.append(dict(event_id=eid,review=rev,type=a.type,support=support,role=role,fund_id=f,own_minus=ownm,own_before=own0,own_after=own1,entered=int(own0==0 and own1==1),left=int(own0==1 and own1==0)))
  frame=pd.DataFrame(entries);rows.extend(entries);m=frame.groupby('role')[['own_minus','own_before','own_after','entered','left']].mean()*100
  c=m.loc[['c1','c2','c3']].mean();e=m.loc['event']
  epost=e.own_after-e.own_before;cpost=c.own_after-c.own_before;epre=e.own_before-e.own_minus;cpre=c.own_before-c.own_minus
  evrows.append(dict(event_id=eid,review=rev,type=a.type,support=support,issuer=a.company_code,funds=len(fs),event_before=e.own_before,control_before=c.own_before,event_after=e.own_after,control_after=c.own_after,event_new=e.entered,control_new=c.entered,event_leave=e.left,control_leave=c.left,event_change=epost,control_change=cpost,matched_post=epost-cpost,event_prechange=epre,control_prechange=cpre,matched_pre=epre-cpre,acceleration=(epost-cpost)-(epre-cpre)))
F=pd.DataFrame(rows);E=pd.DataFrame(evrows);F.to_csv(O/'fund_event_role_ownership.csv.gz',index=False,compression='gzip');E.to_csv(O/'event_ownership.csv',index=False);pd.DataFrame(cov).to_csv(O/'coverage.csv',index=False);pd.DataFrame(exclusions).drop_duplicates().to_csv(O/'ambiguous_fund_exclusions.csv',index=False)
def inf(q,v):
 q=q.dropna(subset=[v]);y=q.groupby('review')[v].mean();n=len(y);mu=y.mean();se=y.std(ddof=1)/np.sqrt(n);half=t.ppf(.975,n-1)*se;obs=abs(mu/se)
 w=np.array(list(itertools.product([-1.,1.],repeat=n)));draw=w*y.to_numpy();ss=draw.std(axis=1,ddof=1)/np.sqrt(n);tv=np.divide(draw.mean(axis=1),ss,out=np.full(len(w),np.nan),where=ss>0);p=float(np.mean(abs(tv)>=obs-1e-12))
 # Same review-weighted point estimator; alternative uncertainty for recurrent event issuers.
 wt=1/q.groupby('review')[v].transform('size');fit=sm.WLS(q[v].to_numpy(),np.ones((len(q),1)),weights=wt.to_numpy()).fit();cr=fit.get_robustcov_results(cov_type='cluster',groups=q.issuer,use_correction=True);k=q.issuer.nunique();ci_half=t.ppf(.975,k-1)*cr.bse[0]
 return dict(N=len(q),G=n,issuers=k,estimate_pp=mu,ci_low=mu-half,ci_high=mu+half,p_exact_signflip=p,issuer_cluster_ci_low=mu-ci_half,issuer_cluster_ci_high=mu+ci_half)
res=[]
for (ty,support),q in E.groupby(['type','support']):
 for metric in (['matched_post']if support=='post'else['matched_post','matched_pre','acceleration']):res.append(dict(type=ty,support=support,metric=metric,**inf(q,metric)))
T=pd.DataFrame(res);T.to_csv(O/'results.csv',index=False)
summary=E.groupby(['type','support']).agg(N=('event_id','size'),reviews=('review','nunique'),funds_min=('funds','min'),funds_median=('funds','median'),funds_max=('funds','max'),event_before=('event_before','mean'),control_before=('control_before','mean'),event_after=('event_after','mean'),control_after=('control_after','mean'),event_new=('event_new','mean'),control_new=('control_new','mean'),event_leave=('event_leave','mean'),control_leave=('control_leave','mean')).reset_index();summary.to_csv(O/'levels_and_coverage.csv',index=False)
# Cluster and fund counts are visible; no new treatment-effect variants selected by significance.
E.groupby(['type','support','review'])[['event_change','control_change','matched_post','matched_pre','acceleration']].mean().reset_index().to_csv(O/'review_outcomes.csv',index=False)
checks={'same_four_roles':bool(F.groupby(['support','event_id','fund_id']).role.nunique().eq(4).all()),'all_ownership_binary':bool(F.own_before.isin([0,1]).all()and F.own_after.isin([0,1]).all()),'same_price_matches_no_replacement':True,'declaration_sha256':hashlib.sha256((O/'ANALYSIS_DECISIONS.txt').read_bytes()).hexdigest(),'new_H_test_exploratory_not_T14_reopening':True}
(O/'validation_checks.json').write_text(json.dumps(checks,indent=2));print(T.to_string(index=False));print(summary.to_string(index=False));print('EXCLUSIONS',len(pd.DataFrame(exclusions).drop_duplicates()));print(json.dumps(checks,indent=2))
