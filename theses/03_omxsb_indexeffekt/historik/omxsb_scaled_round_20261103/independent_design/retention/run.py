#!/usr/bin/env python3
"""One locked q0-valued new-owner-cohort change, after the frozen source gate."""
from pathlib import Path
import argparse,datetime,hashlib,json,os
import numpy as np
import pandas as pd
from scipy.stats import t
ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis')));ap.add_argument('--gate-dir',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parent);a=ap.parse_args()
G=a.gate_dir;O=a.output;R=a.repo_root;O.mkdir(parents=True,exist_ok=True)
if (O/'OUTCOME_LOCK.json').exists():raise RuntimeError('Frozen outcome exists; use --output NEW_DIRECTORY for replay.')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[G/'DESIGN_LOCK.txt',G/'Q0_TIMESTAMP_GUARD_AMENDMENT.txt',G/'GATE_RESULT.json',G/'SECURITY_SOURCE_GATE.csv',G/'EVENT_SOURCE_GATE.csv',G/'FROZEN_ROLES.csv',G/'ELIGIBLE_FUNDS.csv',G/'private/RAW_RELEVANT_POSITIONS.csv.gz',G/'private/SCALING_INPUTS.csv',R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz']
gate=json.loads((G/'GATE_RESULT.json').read_text());assert gate['new_outcomes_computed'] is False
eg=pd.read_csv(G/'EVENT_SOURCE_GATE.csv');keep=set(eg.loc[eg.gate_pass,'event_id']);assert len(keep)==gate['passed_events']
S=pd.read_csv(G/'FROZEN_ROLES.csv');S=S[S.event_id.isin(keep)]
SG=pd.read_csv(G/'SECURITY_SOURCE_GATE.csv');assert SG.loc[SG.gate_pass,'q0_same_actual_LSEG_date'].all()
F=pd.read_csv(G/'ELIGIBLE_FUNDS.csv',dtype={'fund_id':str});F=F[F.event_id.isin(keep)]
D=pd.read_csv(inputs[-1],dtype={'fund_id':str});D=D[D.event_id.isin(keep)]
H=pd.read_csv(G/'private/RAW_RELEVANT_POSITIONS.csv.gz',dtype={'fund_id':str});C=pd.read_csv(G/'private/SCALING_INPUTS.csv').set_index(['review','ric'])
first=not any((Path(__file__).resolve().parent/x).exists() for x in ['PRIMARY_RESULT.json','REVIEW_LEVELS.csv'])
lock={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_execution':first,'exploratory_prior_capital_and_two_fund_retention_known':True,'source_gate_reviewed_by_root':True,'events':len(keep),'reviews':int(S.review.nunique()),'primary':'equal-review mean of matched new-cohort q1-to-q2 quantity-capital change, fixed q0 valuation','inputs':{str(p):sha(p) for p in inputs},'script_sha256':sha(Path(__file__))}
(O/'OUTCOME_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
rows=[];eventrows=[];rawstatuschecks=0
for eid,ss in S.groupby('event_id'):
 good=set(F.loc[F.event_id.eq(eid),'fund_id']);rolevals={}
 for x in ss.itertuples():
  z=D[D.event_id.eq(eid)&D.role.eq(x.role)&D.fund_id.isin(good)];assert set(z.fund_id)==good
  h=H[H['isin'].isin(x.aliases.split(';'))&H.quarter.isin([x.q0,x.q1,x.q2])&H.fund_id.isin(good)]
  qt=h.groupby(['fund_id','quarter']).qty.sum(min_count=1).to_dict();sc=C.loc[(x.review,x.ric)]
  scale=100*sc.q0_price/sc.q0_mcap;v1=v2=0.;newn=0
  for f in z.itertuples():
   q0=float(qt.get((f.fund_id,x.q0),0));q1=float(qt.get((f.fund_id,x.q1),0));q2=float(qt.get((f.fund_id,x.q2),0))
   assert np.isfinite(q0+q1+q2) and min(q0,q1,q2)>=0
   kind='new' if q0==0 and q1>0 else ('continuing' if q0>0 and q1>0 else ('exiting' if q0>0 and q1==0 else 'neither'))
   assert kind==f.component;rawstatuschecks+=1
   if kind!='new':continue
   x1=q1/sc.factor01*scale;x2=q2/(sc.factor01*sc.factor12)*scale
   rows.append(dict(event_id=eid,review=x.review,role=x.role,ric=x.ric,fund_id=f.fund_id,q1_capital_pp=x1,q2_capital_pp=x2,post_change_pp=x2-x1))
   v1+=x1;v2+=x2;newn+=1
  rolevals[x.role]=(v1,v2,newn)
 val={'event_id':eid,'review':ss.review.iloc[0],'event_ric':ss.loc[ss.role.eq('event'),'ric'].iloc[0]}
 for role in ['event','c1','c2','c3']:
  val[role+'_q1_pp']=rolevals[role][0];val[role+'_q2_pp']=rolevals[role][1];val[role+'_fixed_new_funds']=rolevals[role][2]
 for endpoint in ['q1','q2']:
  val['control_'+endpoint+'_pp']=sum(val[c+'_'+endpoint+'_pp']for c in ['c1','c2','c3'])/3
  val['matched_'+endpoint+'_pp']=val['event_'+endpoint+'_pp']-val['control_'+endpoint+'_pp']
 for role in ['event','control','matched']:val[role+'_post_change_pp']=val[role+'_q2_pp']-val[role+'_q1_pp']
 assert abs(val['matched_post_change_pp']-(val['event_post_change_pp']-val['control_post_change_pp']))<1e-10
 eventrows.append(val)
L=pd.DataFrame(rows);E=pd.DataFrame(eventrows);metrics=[r+'_'+t for r in ['event','control','matched'] for t in ['q1_pp','q2_pp','post_change_pp']]
V=E.groupby('review')[metrics].mean();V['N_events']=E.groupby('review').size();V=V.reset_index();y=V.matched_post_change_pp.to_numpy();n=len(y);mean=float(y.mean());se=float(y.std(ddof=1)/np.sqrt(n));half=float(t.ppf(.975,n-1)*se)
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'N_events':len(E),'G_reviews':n,'new_fund_role_rows':len(L),'old_component_checks':rawstatuschecks,'primary_mean_pp':mean,'standard_error_pp':se,'ci95_low_pp':mean-half,'ci95_high_pp':mean+half,'inference':'One nominal exploratory t interval, df G-1, conditional on sufficiently independent review means; not causal and not adjusted for project-wide search','descriptive_equal_review_levels':{c:float(V[c].mean()) for c in metrics},'no_ratios_no_subgroups_no_price_paths':True,'max_additive_identity_error':float((E.matched_post_change_pp-(E.matched_q2_pp-E.matched_q1_pp)).abs().max())}
L.to_csv(O/'NORMALIZED_NEW_COHORT_LEDGER.csv.gz',index=False,compression='gzip');E.to_csv(O/'EVENT_LEVELS.csv',index=False);V.to_csv(O/'REVIEW_LEVELS.csv',index=False)
V[['matched_q1_pp','matched_q2_pp','matched_post_change_pp']].cov().div(n).to_csv(O/'JOINT_COVARIANCE_OF_MEANS.csv')
(O/'PRIMARY_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
