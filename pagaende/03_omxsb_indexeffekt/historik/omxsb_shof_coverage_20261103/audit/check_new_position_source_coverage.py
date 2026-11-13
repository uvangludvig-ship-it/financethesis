from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime
O=Path(__file__).resolve().parent;W=O.parents[1];LED=W/'contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz';FP=O/'F_fund_review_source_eligibility.csv'
paths=[O/'POST_F_NEW_POSITION_COVERAGE_SPEC.txt',LED,FP,Path(__file__)]
(O/'NEW_POSITION_COVERAGE_LOCK.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'declared_after_F':True,'no_risk_outcome_or_new_ownership_estimate':True,'inputs':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}},indent=2))
L=pd.read_csv(LED,dtype={'fund_id':str},usecols=['event_id','review','type','role','fund_id','component','pp']);L=L[L.review.le('2023H2')&L.type.eq('addition')];assert L.event_id.nunique()==70;assert not L.duplicated(['event_id','role','fund_id']).any()
H=pd.read_csv(FP,dtype={'fund_id':str},usecols=['review','fund_id','F_RIPS_allraw','F_NAV_conditional_allraw']);L=L.merge(H,on=['review','fund_id'],how='left',validate='m:1');assert L[['F_RIPS_allraw','F_NAV_conditional_allraw']].notna().all().all()
N=L[L.component.eq('new')].copy();assert N.pp.ge(0).all() and np.isfinite(N.pp).all()
rows=[]
for (eid,rev,role),g in L.groupby(['event_id','review','role']):
 n=g[g.component.eq('new')];den=float(n.pp.sum())
 for sc in ['F_RIPS_allraw','F_NAV_conditional_allraw']:
  covered=n[n[sc]];num=float(covered.pp.sum());fraction=num/den if den>0 else np.nan;assert pd.isna(fraction) or 0<=fraction<=1+1e-12
  rows.append(dict(event_id=eid,review=rev,role=role,scenario=sc,gross_new_pp=den,covered_new_pp=num,coverage_fraction=fraction,new_positive_fund_positions=int(n.pp.gt(0).sum()),covered_new_positive_fund_positions=int(covered.pp.gt(0).sum())))
D=pd.DataFrame(rows);controls=[]
for (eid,rev,sc),g in D[D.role.isin(['c1','c2','c3'])].groupby(['event_id','review','scenario']):
 assert len(g)==3;den=float(g.gross_new_pp.mean());num=float(g.covered_new_pp.mean());controls.append(dict(event_id=eid,review=rev,role='control_mean',scenario=sc,gross_new_pp=den,covered_new_pp=num,coverage_fraction=num/den if den>0 else np.nan,new_positive_fund_positions=int(g.new_positive_fund_positions.sum()),covered_new_positive_fund_positions=int(g.covered_new_positive_fund_positions.sum())))
D=pd.concat([D,pd.DataFrame(controls)],ignore_index=True);D.to_csv(O/'NEW_POSITION_event_role_coverage.csv',index=False)
R=D.groupby(['scenario','role','review']).agg(events=('event_id','size'),missing_or_zero_new_denominator=('coverage_fraction',lambda x:int(x.isna().sum())),mean_gross_new_pp=('gross_new_pp','mean'),mean_covered_new_pp=('covered_new_pp','mean'),mean_event_coverage_fraction=('coverage_fraction','mean'),positive_new_positions=('new_positive_fund_positions','sum'),covered_positive_new_positions=('covered_new_positive_fund_positions','sum')).reset_index();R['ratio_of_review_gross_pp']=R.mean_covered_new_pp/R.mean_gross_new_pp;R.loc[R.mean_gross_new_pp.le(0),'ratio_of_review_gross_pp']=np.nan;R.to_csv(O/'NEW_POSITION_review_role_summary.csv',index=False)
out=[]
for (sc,role),g in R.groupby(['scenario','role']):
 den=float(g.mean_gross_new_pp.mean());num=float(g.mean_covered_new_pp.mean());out.append(dict(scenario=sc,role=role,events=int(g.events.sum()),reviews=len(g),mean_gross_new_pp_equal_review=den,mean_covered_new_pp_equal_review=num,coverage_of_equal_review_gross_new_pp=num/den if den>0 else np.nan,mean_event_coverage_equal_review=float(g.mean_event_coverage_fraction.mean()),missing_or_zero_new_denominators=int(g.missing_or_zero_new_denominator.sum()),positive_new_positions=int(g.positive_new_positions.sum()),covered_positive_new_positions=int(g.covered_positive_new_positions.sum())))
S=pd.DataFrame(out);S.to_csv(O/'NEW_POSITION_equal_review_summary.csv',index=False)
validation={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':L.event_id.nunique(),'reviews':L.review.nunique(),'input_new_component_nonnegative':True,'no_netmatched_denominators':True,'fraction_bounds_pass':bool(D.coverage_fraction.dropna().between(-1e-12,1+1e-12).all()),'missing_or_zero_denominator_cells':int(D.coverage_fraction.isna().sum()),'units':'marketcap-normalized grossnew positions; not pooledSEKcash','declared_after_F_before_riskoutcomes':True,'risk_outcomes_computed':False,'prior_ownership_results_unchanged':True}
(O/'NEW_POSITION_COVERAGE_VALIDATION.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2));print(S.to_string(index=False))
