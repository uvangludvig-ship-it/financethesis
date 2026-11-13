"""QA scope clarification only: original Runda8 input also includes OMXS30 events."""
from pathlib import Path
import pandas as pd,hashlib,json,datetime,argparse
a=argparse.ArgumentParser();a.add_argument('--repo',required=True);a.add_argument('--out',required=True);a=a.parse_args();R=Path(a.repo);O=Path(a.out)
P=R/'code/claude_checks/runda9_resultat/nettokop_lseg_events.csv';C=R/'output/omxsb_replication_2007/events_car.csv';D=R/'output/omxsb_open_questions_20261102/demand/denominator_audit.csv'
lock={'actual_utc_before_scope_counts':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'Clarify original all-event metadata vs OMXSB-only T24 sample; does not alter any FI economic result; metadata-only denominator context for already declared unit diagnostic','hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in[P,C,D,O/'lseg_event_coverage.csv']}}
(O/'COVERAGE_SCOPE_LOCK.json').write_text(json.dumps(lock,indent=2))
x=pd.read_csv(O/'lseg_event_coverage.csv');p=pd.read_csv(P,usecols=['event_id','shares']);c=pd.read_csv(C,usecols=['event_id','tot_gi'])
eligible=set(p.loc[p.shares.notna(),'event_id'])&set(c.loc[c.tot_gi.notna(),'event_id'])
z=x[x.event_id.str.startswith('OMXSB')].copy();z['in_original_T24_same_price_share_sample']=z.event_id.isin(eligible);z.to_csv(O/'lseg_OMXSB_event_coverage.csv',index=False)
out=[]
for scope,s in [('all_OMXSB_raw_events',z),('original_T24_price_share_sample',z[z.in_original_T24_same_price_share_sample])]:
 q=s.groupby(['period','type']).agg(N=('event_id','size'),G=('review_cycle','nunique'),median_reporting_funds=('old_cross_stock_reporting_funds','median'),no_eligible_fund_made_zero=('old_zero_no_eligible_fund','sum'),no_group_made_zero=('old_zero_no_group','sum'),inferred_target_zeros=('inferred_missing_target_fund_endpoints','sum'),median_before_age=('median_report_age_before','median'),median_after_age=('median_report_age_after','median')).reset_index();q['scope']=scope;out.append(q)
y=pd.concat(out,ignore_index=True);y.to_csv(O/'lseg_T24_scoped_coverage.csv',index=False);print(y.to_string(index=False))
d=pd.read_csv(D);u=p.merge(d,on='event_id',validate='1:1');u=u[u.RIC.isin(['SINCH.ST','FINGb.ST^G26','NOBI.ST','SWECb.ST','ANODb.ST','ATRLJb.ST'])]
u[['event_id','RIC','shares','raw_shares','class_shares_after','fi_price','close','mcap','class_value_fraction']].to_csv(O/'T24_denominator_unit_context.csv',index=False)
