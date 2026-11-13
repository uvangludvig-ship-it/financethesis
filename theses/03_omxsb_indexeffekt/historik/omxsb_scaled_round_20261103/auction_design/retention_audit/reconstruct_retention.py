"""Independent raw-position reconstruction; no producer functions or raw-value exports."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import t

O=Path(__file__).resolve().parent
P=O.parents[1]/'independent_design/retention'
R=Path('/Users/ludviguvang/dev/financethesis')
OLD=R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz'
REPORTS=R/'output/omxsb_open_questions_20261102/demand_quarter/raw_fund_report_metadata.csv'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def level(quantity, factor, price0, cap0):
 if not(np.isfinite(quantity) and quantity>=0 and np.isfinite(factor) and factor>0 and np.isfinite(price0) and price0>0 and np.isfinite(cap0) and cap0>0):raise ValueError('invalid quantity or scaling')
 return 100*quantity/factor*price0/cap0
def paired(rolevals):
 if set(rolevals)!={'event','c1','c2','c3'}:raise ValueError('exact three fixed controls required')
 return rolevals['event']-(rolevals['c1']+rolevals['c2']+rolevals['c3'])/3

def main():
 assert (P/'OUTCOME_LOCK.json').exists(),'Producer outcome release missing'
 assert sha(P/'GATE_RESULT.json')=='d28c68caba6730ad7987cdad5c65ce636ca02db0b5e720d29ebd9f6ddac83114'
 assert sha(P/'SECURITY_SOURCE_GATE.csv')=='37caef46e9c343247e969f72525eba256458310055fee31ef8a945e3f3646e9c'
 paths=[P/'DESIGN_LOCK.txt',P/'OUTCOME_LOCK.json',P/'GATE_RESULT.json',P/'SECURITY_SOURCE_GATE.csv',P/'EVENT_SOURCE_GATE.csv',P/'FROZEN_ROLES.csv',P/'ELIGIBLE_FUNDS.csv',P/'FUND_REPORT_SUPPORT.csv.gz',P/'INVALID_FUND_UNITS.csv',P/'private/RAW_RELEVANT_POSITIONS.csv.gz',P/'private/SCALING_INPUTS.csv',OLD,REPORTS,Path(__file__),O/'AUDIT_SPEC.txt']
 lock=O/'INDEPENDENT_RUN_LOCK.json'
 if lock.exists():raise FileExistsError('Preserve first independent run')
 lock.write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'producer_functions_used':False,'inputs':{str(p):sha(p) for p in paths}},indent=2)+'\n')
 E=pd.read_csv(P/'EVENT_SOURCE_GATE.csv');keep=set(E.loc[E.gate_pass,'event_id'])
 assert len(keep)==59 and E.loc[E.gate_pass,'review'].nunique()==10
 S=pd.read_csv(P/'FROZEN_ROLES.csv');S=S[S.event_id.isin(keep)]
 assert S.groupby('event_id').role.apply(set).map(lambda a:a=={'event','c1','c2','c3'}).all()
 assert not S.duplicated(['event_id','role']).any()
 SG=pd.read_csv(P/'SECURITY_SOURCE_GATE.csv')
 joined=S.merge(SG,on=['review','ric'],validate='m:1',suffixes=('','_gate'))
 assert joined.gate_pass.all() and joined.q0_same_actual_LSEG_date.all()
 assert joined.q0_LSEG_close_date.eq(joined.q0_LSEG_mcap_date).all()
 assert joined.q0_close_age_days.le(7).all()
 assert (pd.to_datetime(joined.q0)-pd.to_datetime(joined.q0_LSEG_mcap_date)).dt.days.between(0,7).all()
 A=pd.read_csv(P/'ELIGIBLE_FUNDS.csv',dtype={'fund_id':str});assert not A.duplicated(['event_id','fund_id']).any()
 support=pd.read_csv(P/'FUND_REPORT_SUPPORT.csv.gz',dtype={'fund_id':str})
 B=pd.read_csv(P/'INVALID_FUND_UNITS.csv',dtype={'fund_id':str})
 D=pd.read_csv(OLD,usecols=['event_id','review','type','role','fund_id','component'],dtype={'fund_id':str});D=D[D.event_id.isin(keep)]
 F=pd.read_csv(REPORTS,usecols=['Fond_institutnummer','Kvartalsslut','actual_instrument_rows','fund_isin'],dtype={'Fond_institutnummer':str,'fund_isin':str}).rename(columns={'Fond_institutnummer':'fund_id','Kvartalsslut':'quarter'})
 assert not F.duplicated(['fund_id','quarter']).any();fm=F.set_index(['fund_id','quarter'])
 H=pd.read_csv(P/'private/RAW_RELEVANT_POSITIONS.csv.gz',usecols=['isin','quarter','fund_id','qty'],dtype={'fund_id':str,'isin':str})
 H['qty']=pd.to_numeric(H.qty,errors='coerce')
 scale=pd.read_csv(P/'private/SCALING_INPUTS.csv').set_index(['review','ric']);assert scale.index.is_unique
 role_rows=[];event_rows=[];checks={'original_fund_role_sets_checked':0,'report_cells_checked':0,'new_cohort_membership_checks':0,'eligible_funds_sum':0,'new_cohort_q2_zero_positions':0,'source_missing_report_zero_imputations':0}
 for eid,ss in S.groupby('event_id',sort=True):
  first=ss.iloc[0];old=D[D.event_id.eq(eid)];base=set(old.loc[old.role.eq('event'),'fund_id'])
  for role,g in old.groupby('role'):
   assert set(g.fund_id)==base;checks['original_fund_role_sets_checked']+=1
  expected=set()
  bad=set(B.loc[B.review.eq(first.review)&B.ric.isin(ss.ric),'fund_id'])
  for fid in base:
   rows=[fm.loc[(fid,q)] if (fid,q) in fm.index else None for q in [first.q0,first.q1,first.q2]]
   ok=all(r is not None and r.actual_instrument_rows>0 and pd.notna(r.fund_isin) and str(r.fund_isin).strip() for r in rows)
   if ok:ok=len({str(r.fund_isin) for r in rows})==1
   if ok and fid not in bad:expected.add(fid)
  actual=set(A.loc[A.event_id.eq(eid),'fund_id'])
  assert actual==expected and actual
  assert set(support.loc[support.event_id.eq(eid)&support.eligible,'fund_id'])==actual
  checks['eligible_funds_sum']+=len(actual);checks['report_cells_checked']+=3*len(actual)
  vals1={};vals2={}
  for s in ss.itertuples():
   alias=set(s.aliases.split(';'));zz=H[H['isin'].isin(alias)&H.fund_id.isin(actual)&H.quarter.isin([s.q0,s.q1,s.q2])]
   assert zz.qty.notna().all() and np.isfinite(zz.qty).all() and zz.qty.ge(0).all()
   qty=zz.groupby(['fund_id','quarter']).qty.sum(min_count=1)
   # Absent instrument is zero only after complete report/stable-identity checks above.
   q={q:qty.reindex(pd.MultiIndex.from_product([sorted(actual),[q]],names=['fund_id','quarter']),fill_value=0).droplevel('quarter') for q in [s.q0,s.q1,s.q2]}
   cohort=set(q[s.q0].index[q[s.q0].eq(0)&q[s.q1].gt(0)])
   frozen=set(old.loc[old.role.eq(s.role)&old.fund_id.isin(actual)&old.component.eq('new'),'fund_id'])
   assert cohort==frozen;checks['new_cohort_membership_checks']+=len(actual)
   checks['new_cohort_q2_zero_positions']+=int(q[s.q2].reindex(sorted(cohort)).eq(0).sum())
   sc=scale.loc[(s.review,s.ric)]
   assert sc.factor01==s.factor01
   sg=SG.loc[SG.review.eq(s.review)&SG.ric.eq(s.ric)].iloc[0]
   assert sc.factor12==sg.factor12
   x1=level(float(q[s.q1].reindex(sorted(cohort)).sum()),float(sc.factor01),float(sc.q0_price),float(sc.q0_mcap))
   x2=level(float(q[s.q2].reindex(sorted(cohort)).sum()),float(sc.factor01*sc.factor12),float(sc.q0_price),float(sc.q0_mcap))
   vals1[s.role]=x1;vals2[s.role]=x2
   role_rows.append({'event_id':eid,'review':s.review,'role':s.role,'X_q1_pp':x1,'X_q2_pp':x2,'change_pp':x2-x1,'eligible_funds':len(actual),'new_cohort_funds':len(cohort)})
  event_rows.append({'event_id':eid,'review':first.review,'event_q1_pp':vals1['event'],'event_q2_pp':vals2['event'],
    'control_q1_pp':sum(vals1[c] for c in ['c1','c2','c3'])/3,'control_q2_pp':sum(vals2[c] for c in ['c1','c2','c3'])/3,
    'matched_q1_pp':paired(vals1),'matched_q2_pp':paired(vals2),'D_pp':paired({k:vals2[k]-vals1[k] for k in vals1})})
 V=pd.DataFrame(event_rows);T=V.groupby('review').mean(numeric_only=True)
 assert np.allclose(V.D_pp,V.matched_q2_pp-V.matched_q1_pp,atol=1e-10,rtol=0)
 y=T.D_pp;G=len(y);mean=float(y.mean());se=float(y.std(ddof=1)/np.sqrt(G));half=float(t.ppf(.975,G-1)*se)
 cov=T[['matched_q1_pp','matched_q2_pp']].cov()/G
 variance_difference=float(cov.iloc[0,0]+cov.iloc[1,1]-2*cov.iloc[0,1])
 assert abs(se*se-variance_difference)<1e-10
 V.to_csv(O/'INDEPENDENT_EVENT_AGGREGATES.csv',index=False,float_format='%.12g')
 T.to_csv(O/'INDEPENDENT_REVIEW_AGGREGATES.csv',float_format='%.12g')
 pd.DataFrame(role_rows).to_csv(O/'INDEPENDENT_ROLE_AGGREGATES.csv',index=False,float_format='%.12g')
 result={'created_utc':datetime.now(timezone.utc).isoformat(),'events':len(V),'reviews':G,'df':G-1,'equal_review_mean_D_pp':mean,'se_pp':se,'ci95_low':mean-half,'ci95_high':mean+half,'level_means':T.mean().to_dict(),'covariance_identity_pass':True,'all_cohort_labels_reproduced':True,'all_eligible_fund_sets_reproduced':True,'q0_actual_date_guard_pass':True,'no_raw_source_values_published':True,'producer_functions_called':False,'checks':checks,'input_lock_sha256':sha(lock)}
 (O/'INDEPENDENT_RECONSTRUCTION.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 print(json.dumps({k:result[k] for k in ['events','reviews','df','equal_review_mean_D_pp','ci95_low','ci95_high']},indent=2))

if __name__=='__main__':main()
