"""Trace known withdrawn announcements through published fixed-control support only."""
from pathlib import Path
from datetime import datetime,timezone
import pandas as pd,json,hashlib
R=Path('/Users/ludviguvang/dev/financethesis');O=Path(__file__).resolve().parent
paths={
 'cancellations':R/'output/omxsb_execution_followup_20261102/sources/known_cancellations.csv',
 'roles':R/'output/omxsb_mechanism_frontier_20261102/ownership/security_role_gate.csv',
 'gate':R/'output/omxsb_contribution_round_20261103/ownership_capital/event_feasibility_gate.csv',
 'components':R/'output/omxsb_contribution_round_20261103/ownership_capital/event_component_results.csv',
 'ledger':R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz',
 'events':R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',
 'listed_controls':R/'output/omxsb_open_questions_20261102/eligible_rematch/selected_controls.csv',
 'old_T2':R/'output/omxsb_robusthet_20261101/T2_matches.csv'}
K=pd.read_csv(paths['cancellations'],usecols=['known_cancel_id','review','RIC','type','scheduled_ED','cancellation_date','initial_source_url','cancellation_source_url']).rename(columns={'RIC':'control_RIC','type':'withdrawn_change_type'})
S=pd.read_csv(paths['roles'],usecols=['event_id','review','type','role','ric']).rename(columns={'ric':'control_RIC','type':'focal_event_type'})
G=pd.read_csv(paths['gate'],usecols=['event_id','gate_pass','reasons'])
C=pd.read_csv(paths['components'],usecols=['event_id','review','type','group'])
F=pd.read_csv(paths['ledger'],usecols=['event_id','review','type','role'])
E=pd.read_csv(paths['events'],usecols=['event_id','company','RIC','type']).rename(columns={'company':'focal_company','RIC':'focal_RIC','type':'focal_type_census'})
D=S.merge(K,on=['review','control_RIC'],validate='m:1').merge(E,on='event_id',validate='m:1').merge(G,on='event_id',how='left',validate='m:1')
D['in_published_component_results']=D.event_id.isin(C.event_id)
F=F.drop_duplicates(['event_id','role'])
keys=set(zip(F.event_id,F.role))
D['in_published_fund_role_ledger']=[(e,r) in keys for e,r in zip(D.event_id,D.role)]
D.to_csv(O/'CANCELLED_CONTROL_CAPITAL_SUPPORT_AUDIT.csv',index=False)
M=pd.read_csv(paths['listed_controls'],usecols=['event_id','review','role','ric']).rename(columns={'ric':'control_RIC'})
old=pd.read_csv(paths['old_T2'],usecols=['event_id','review','c1_ric','c2_ric','c3_ric'])
old=old.melt(id_vars=['event_id','review'],value_vars=['c1_ric','c2_ric','c3_ric'],var_name='role',value_name='control_RIC');old['role']=old.role.str.replace('_ric','',regex=False)
L=pd.concat([M.assign(control_set='dated_eligible_rematch'),old.assign(control_set='older_T2')],ignore_index=True).merge(K,on=['review','control_RIC'],validate='m:1').merge(E,on='event_id',validate='m:1')
L.to_csv(O/'CANCELLED_CONTROL_MATCH_HISTORY.csv',index=False)
allids=C[['event_id','type']].drop_duplicates();affected=set(D.loc[D.in_published_component_results,'event_id'])
result={'created_utc':datetime.now(timezone.utc).isoformat(),'source_metadata_only':True,
 'no_holdings_capital_or_price_outcome_values_read_or_recomputed':True,
 'published_counts':allids.type.value_counts().to_dict(),
 'known_withdrawn_announcements':len(K),
 'published_affected_event_ids':sorted(affected),
 'affected_counts_by_type':allids.loc[allids.event_id.isin(affected),'type'].value_counts().to_dict(),
 'all_addition_headline_observations_unchanged':not allids.loc[allids.event_id.isin(affected),'type'].eq('addition').any(),
 'inputs':{k:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in paths.items()},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'action':'No old outcome rerun. New designs must exclude whole affected sets before outcomes under no-announced-change rule. Existing deletion description requires explicit contamination note or separately declared one-set sensitivity, not a new discovery.'}
(O/'CANCELLED_CONTROL_AUDIT_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
print(D[['event_id','focal_company','focal_event_type','role','control_RIC','withdrawn_change_type','gate_pass','in_published_component_results']].to_string(index=False))
print(json.dumps({k:result[k] for k in ['published_counts','published_affected_event_ids','affected_counts_by_type','all_addition_headline_observations_unchanged']},indent=2))
