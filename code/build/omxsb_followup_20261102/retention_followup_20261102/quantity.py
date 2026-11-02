from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import analysis_paths
_PORTABLE_REPO, _PORTABLE_OUT = analysis_paths('retention_followup_20261102')
import pandas as pd,numpy as np,json,hashlib
O=_PORTABLE_OUT;R=_PORTABLE_REPO;SRC=R/'output/omxsb_open_questions_20261102/retention'
gatefile=O/'quantity_gate_frozen.csv';hh=hashlib.sha256(gatefile.read_bytes()).hexdigest();frozen=json.loads((O/'gate_frozen_summary.json').read_text());assert hh==frozen['gate_sha256']
G=pd.read_csv(gatefile);D=pd.read_csv(SRC/'retention_event_fund_status.csv');D=D[D.type.eq('addition')];EP=pd.read_csv(SRC/'retention_endpoint_audit.csv');EP=EP[EP.type.eq('addition')].set_index(['event_id','fund_id','quarter']);E=pd.read_csv(R/'output/omxsb_extension_20261031/ownership/ownership_observations.csv');E=E[E.main_common_sample].set_index('event_id')
rows=[]
for x in D.merge(G[['event_id','units_gate_pass','splitfactor','source_action']],on='event_id',validate='m:1').itertuples():
 a=EP.loc[(x.event_id,x.fund_id,x.index_q)];b=EP.loc[(x.event_id,x.fund_id,x.next_q)];assert a.status!='unknown'and b.status!='unknown'
 q0=float(a.raw_quantity_unadjusted)if a.status=='positive'else 0.;q1=float(b.raw_quantity_unadjusted)if b.status=='positive'else 0.;den=q0*x.splitfactor
 beforecol='FI_Nordnet_documented_before_raw'if x.fund_id==60320 else 'FI_Nordea_metadata_before_raw';before=E.loc[x.event_id,beforecol];assert before==0
 ratio=q1/den if x.units_gate_pass and den>0 else np.nan
 rows.append(dict(event_id=x.event_id,RIC=x.RIC,review=x.review,fund=x.fund,fund_id=x.fund_id,index_q=x.index_q,next_q=x.next_q,q_pre_index=before,q_pre_index_date=E.loc[x.event_id,'before'],q_index=q0,q_next=q1,splitfactor=x.splitfactor,quantity_retention_ratio=ratio,quantity_direction='not_defined_initial_zero'if np.isnan(ratio)else 'decreased'if q1<den else 'increased'if q1>den else 'unchanged',source_action=x.source_action,next_q_trading_days_after_ED=x.next_q_trading_days_after_ED,next_q_before_ED100=x.next_q_before_ED100,gate_pass=x.units_gate_pass))
Q=pd.DataFrame(rows);Q.to_csv(O/'position_quantities.csv',index=False);summ=[]
for fund,z in Q.groupby('fund'):
 a=z[z.quantity_retention_ratio.notna()];y=a.groupby('review').quantity_retention_ratio.mean()
 summ.append(dict(fund=fund,all_additions=len(z),initial_positive=len(a),initial_zero=int(z.q_index.eq(0).sum()),reviews=a.review.nunique(),median_ratio=a.quantity_retention_ratio.median(),review_equal_mean_ratio=y.mean(),event_equal_mean_ratio=a.quantity_retention_ratio.mean(),decreased=int(a.quantity_direction.eq('decreased').sum()),unchanged=int(a.quantity_direction.eq('unchanged').sum()),increased=int(a.quantity_direction.eq('increased').sum()),full_exit=int(a.q_next.eq(0).sum())))
S=pd.DataFrame(summ);S.to_csv(O/'quantity_summary.csv',index=False);print(S.to_string(index=False))
# Exactly the two preidentified denominator corrections, not an outcome-selected ownership subsample.
denoms={'OMXSB-2024H1-07':295966330.,'OMXSB-2024H2-03':122833491.};C=Q[Q.event_id.isin(denoms)].copy();C['validated_class_shares_index']=C.event_id.map(denoms);C['validated_class_shares_next']=C.event_id.map(denoms);C['class_ownership_pct_index']=100*C.q_index/C.validated_class_shares_index;C['class_ownership_pct_next']=100*C.q_next/C.validated_class_shares_next;C.to_csv(O/'two_verified_class_denominator_cases.csv',index=False);print('TWOCASES',C[['event_id','fund','q_index','q_next','class_ownership_pct_index','class_ownership_pct_next']].to_string(index=False))
# Membership and flow claims are never inferred from these outcomes.
P=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv');P=P[P.type.eq('addition')&P.common100].copy();P['existing_direct_event_20to100']=P.event_100-P.event_20;P['existing_matched_20to100']=P.diff3_100-P.diff3_20
J=Q.merge(P[['event_id','existing_direct_event_20to100','existing_matched_20to100']],on='event_id',how='left',validate='m:1');J.to_csv(O/'existing_price_join.csv',index=False)
# Single joint descriptive intersection: both trackers have a defined ratio and the pre-existing common100 price path.
ids=Q[Q.quantity_retention_ratio.notna()].groupby('event_id').fund_id.nunique();valid=set(ids[ids==2].index);B=J[J.event_id.isin(valid)&J.existing_matched_20to100.notna()];V=B.drop_duplicates('event_id');js=dict(both_initially_positive_events=len(valid),joint_price_events=len(V),reviews=V.review.nunique(),existing_direct_late_event_mean=V.existing_direct_event_20to100.mean(),existing_direct_late_review_mean=V.groupby('review').existing_direct_event_20to100.mean().mean(),existing_matched_late_event_mean=V.existing_matched_20to100.mean(),existing_matched_late_review_mean=V.groupby('review').existing_matched_20to100.mean().mean(),funds={f:dict(N=len(z),median_quantity_ratio=z.quantity_retention_ratio.median(),review_equal_mean_quantity_ratio=z.groupby('review').quantity_retention_ratio.mean().mean())for f,z in B.groupby('fund')},statement='Descriptive intersection, no new price calculation beyond subtraction of saved horizons, no inference or causal price/retention effect; retention endpoint precedes100 for all.')
(O/'joint_existing_price_description.json').write_text(json.dumps(js,indent=2));print(json.dumps(js,indent=2));assert hashlib.sha256(gatefile.read_bytes()).hexdigest()==hh
(O/'quantity_run_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [gatefile,O/'DECLARATION.txt',SRC/'retention_endpoint_audit.csv',R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',O/'position_quantities.csv',O/'quantity_summary.csv']},indent=2))
