"""No q2 quantities read. Known q1 weights determine missing-support bound width."""
from pathlib import Path
from datetime import datetime,timezone
import pandas as pd,numpy as np,json,hashlib,os
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis'))
paths={'q1_ledger':R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz','event_gate':R/'output/omxsb_scaled_round_20261103/independent_design/retention/EVENT_SOURCE_GATE.csv','fund_support':R/'output/omxsb_scaled_round_20261103/independent_design/retention/ELIGIBLE_FUNDS.csv','roles':R/'output/omxsb_scaled_round_20261103/independent_design/retention/FROZEN_ROLES.csv'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(O/'SOURCE_SCREEN_LOCK.json').write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'q2_values_read':False,'source_spec_sha256':sha(O/'SOURCE_SCREEN_SPEC.txt'),'code_sha256':sha(Path(__file__)),'inputs':{k:{'path':str(p),'sha256':sha(p)}for k,p in paths.items()}},indent=2)+'\n')
D=pd.read_csv(paths['q1_ledger'],dtype={'fund_id':str});D=D[D.type.eq('addition')&D.review.lt('2024')].copy();assert D.event_id.nunique()==70;assert not D.duplicated(['event_id','role','fund_id']).any();assert D.groupby('event_id').role.apply(set).map(lambda s:s=={'event','c1','c2','c3'}).all()
S=pd.read_csv(paths['roles'],usecols=['event_id','review','role','ric']);assert len(S)==280 and S.event_id.nunique()==70;E=pd.read_csv(paths['event_gate']);F=pd.read_csv(paths['fund_support'],dtype={'fund_id':str});good=set(E.loc[E.gate_pass,'event_id']);funds=set(zip(F.event_id,F.fund_id))
N=D[D.component.eq('new')].copy();assert N.pp.gt(0).all();N['q2_supported']=[e in good and (e,f)in funds for e,f in zip(N.event_id,N.fund_id)];N['known_q1_weight']=N.pp.where(N.q2_supported,0);N['unknown_q1_weight']=N.pp.where(~N.q2_supported,0)
G=N.groupby(['event_id','review','role']).agg(new_positions=('fund_id','size'),supported_new_positions=('q2_supported','sum'),q1_weight=('pp','sum'),known_weight=('known_q1_weight','sum'),unknown_weight=('unknown_q1_weight','sum')).reset_index();G=S.merge(G,on=['event_id','review','role'],how='left',validate='1:1')
G['positive_initial_denominator']=G.q1_weight.gt(0);G['unknown_weight_fraction']=G.unknown_weight/G.q1_weight
# The fractions below use only source masks and OLD q1 weights, never q2 quantity.
public=G.drop(columns=['q1_weight','known_weight','unknown_weight']);public.to_csv(O/'ROLE_SOURCE_WIDTH.csv',index=False)
if not G.positive_initial_denominator.all():
 summary={'status':'denominator_design_blocker','roles_zero_or_missing_q1':G.loc[~G.positive_initial_denominator,['event_id','review','role']].to_dict('records'),'q2_values_read':False}
else:
 rv=G.groupby(['review','role']).unknown_weight_fraction.mean().unstack('role');rv['control_mean_width']=rv[['c1','c2','c3']].mean(axis=1);rv['matched_contrast_width']=rv['event']+rv.control_mean_width;rv.reset_index().to_csv(O/'REVIEW_IDENTIFICATION_WIDTH.csv',index=False)
 summary={'status':'all_initial_role_denominators_positive','original_events':70,'original_reviews':10,'original_stock_roles':280,'original_new_positions':len(N),'q2_source_supported_new_positions':int(N.q2_supported.sum()),'roles_with_supported_new_position':int(G.supported_new_positions.gt(0).sum()),'complete_event_source_sets':len(good),'equal_review_event_bound_width_pp':100*rv.event.mean(),'equal_review_control_bound_width_pp':100*rv.control_mean_width.mean(),'equal_review_matched_bound_width_pp':100*rv.matched_contrast_width.mean(),'event_initial_capital_pooled_source_coverage':float(G.loc[G.role.eq('event'),'known_weight'].sum()/G.loc[G.role.eq('event'),'q1_weight'].sum()),'q2_values_read':False,'economic_retention_overlap_computed':False,'bounds_are_finite_population_identification_not_confidence_intervals':True}
(O/'SOURCE_PRECISION_ASSESSMENT.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
