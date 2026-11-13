"""Compare completed independent aggregates and frozen cohort keys to producer exports."""
from pathlib import Path
from datetime import datetime,timezone
import pandas as pd,numpy as np,json,hashlib
O=Path(__file__).resolve().parent;P=O.parents[1]/'independent_design/retention'
R=Path('/Users/ludviguvang/dev/financethesis')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
I=pd.read_csv(O/'INDEPENDENT_EVENT_AGGREGATES.csv').set_index('event_id')
E=pd.read_csv(P/'EVENT_LEVELS.csv').set_index('event_id')
assert set(I.index)==set(E.index) and len(I)==59
mapping={k:k for k in ['event_q1_pp','event_q2_pp','control_q1_pp','control_q2_pp','matched_q1_pp','matched_q2_pp']};mapping['D_pp']='matched_post_change_pp'
errors={k:float((I[k]-E.loc[I.index,v]).abs().max()) for k,v in mapping.items()}
T=pd.read_csv(O/'INDEPENDENT_REVIEW_AGGREGATES.csv').set_index('review')
V=pd.read_csv(P/'REVIEW_LEVELS.csv').set_index('review');assert set(T.index)==set(V.index) and len(T)==10
review_errors={k:float((T[k]-V.loc[T.index,v]).abs().max()) for k,v in mapping.items()}
Z=pd.read_csv(O/'INDEPENDENT_ROLE_AGGREGATES.csv')
role_errors=[];cohort_counts=[]
for x in Z.itertuples():
 prefix='event' if x.role=='event' else x.role
 role_errors += [abs(x.X_q1_pp-E.loc[x.event_id,prefix+'_q1_pp']),abs(x.X_q2_pp-E.loc[x.event_id,prefix+'_q2_pp'])]
 assert x.new_cohort_funds==E.loc[x.event_id,prefix+'_fixed_new_funds']
old=pd.read_csv(R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz',usecols=['event_id','role','fund_id','component'],dtype={'fund_id':str})
a=pd.read_csv(P/'ELIGIBLE_FUNDS.csv',usecols=['event_id','fund_id'],dtype={'fund_id':str})
expected=old.loc[old.event_id.isin(I.index)&old.component.eq('new')].merge(a,on=['event_id','fund_id'],validate='m:1')
new=pd.read_csv(P/'NORMALIZED_NEW_COHORT_LEDGER.csv.gz',usecols=['event_id','role','fund_id'],dtype={'fund_id':str})
assert not new.duplicated().any()
assert set(map(tuple,new[['event_id','role','fund_id']].to_numpy()))==set(map(tuple,expected[['event_id','role','fund_id']].to_numpy()))
maxerr=max(list(errors.values())+list(review_errors.values())+role_errors)
assert maxerr<1e-9
me=json.loads((O/'INDEPENDENT_RECONSTRUCTION.json').read_text());their=json.loads((P/'PRIMARY_RESULT.json').read_text())
headline_map={'equal_review_mean_D_pp':'primary_mean_pp','se_pp':'standard_error_pp','ci95_low':'ci95_low_pp','ci95_high':'ci95_high_pp'}
headline={k:abs(me[k]-their[v]) for k,v in headline_map.items()};assert max(headline.values())<1e-12
out={'created_utc':datetime.now(timezone.utc).isoformat(),'passed':True,'events':len(I),'reviews':len(T),'role_aggregates':len(Z),'cohort_key_rows':len(new),
 'max_absolute_aggregate_export_difference_pp':maxerr,'aggregate_tolerance_pp':1e-9,
 'note':'Independent aggregate CSVs intentionally round to12significantdigits; this bounds export comparison differences, not disagreement of the main fullprecision arithmetic.',
 'headline_absolute_differences':headline,'event_metric_max_errors':errors,'review_metric_max_errors':review_errors,
 'exact_frozen_new_cohort_keys_match':True,'three_controls_and_equal_review_weights_match':True,'primary_df':9,
 'what_was_reproduced':['Raw quantity sums under exact role-specific ISIN aliases','Every eligible fund set from original support, three complete reports and any-role unit exclusions','Every role-specific raw q0zero/q1positive cohort versus original labels','q0share-unit split conversion and fixed input q0valuation','236role levels,59event levels/changes,10review means','Mean,SE,t9CI and covariance subtraction identity','Recorded actual q0vendor date equality and source-age flags'],
 'what_was_not_newly_certified':['Vendor q0capitalization values independently sourced from another vendor','Exhaustive corporate-action/fund-merger or competing-index registers','Missing11event outcomes','Independence of review means','A causal effect or persistent gross trading demand'],
 'files':{str(p):sha(p) for p in [P/'OUTCOME_LOCK.json',P/'PRIMARY_RESULT.json',P/'EVENT_LEVELS.csv',P/'REVIEW_LEVELS.csv',P/'NORMALIZED_NEW_COHORT_LEDGER.csv.gz',O/'INDEPENDENT_RUN_LOCK.json',O/'INDEPENDENT_RECONSTRUCTION.json',Path(__file__)]}}
(O/'FINAL_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['passed','events','reviews','role_aggregates','cohort_key_rows','max_absolute_aggregate_export_difference_pp','headline_absolute_differences']},indent=2))
