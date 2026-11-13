"""Baseline and data-support keys only. Never read post holdings or capital values."""
from pathlib import Path
import pandas as pd, json, datetime
O=Path(__file__).resolve().parent
R=Path('/Users/ludviguvang/dev/financethesis')
W=R/'output/omxsb_mechanism_frontier_20261102/ownership'
A=pd.read_csv(O/'fund_review_metadata_baseline.csv',dtype={'fund_id':str})
F=pd.read_csv(W/'decomp_fund_roles.csv.gz',usecols=['event_id','review','type','role','fund_id','own_before'],dtype={'fund_id':str})
F=F[F.role.eq('event')].drop(columns='role').merge(A,on=['review','fund_id'],validate='m:1')
F=F[F.full_both_reports & F.company.str.startswith('SEB')].copy()
owned=F.groupby(['event_id','company']).own_before.any().rename('company_pre_owned')
F=F.join(owned,on=['event_id','company'])
idsB={'51250','52265','56050','56054'};idsH={'51416','51718','56053'}
F=F[F.fund_id.isin(idsB|idsH) & F.pre_direct_Swedish_stock_support].copy()
F['candidate_group']=F.fund_id.map(lambda x:'B' if x in idsB else 'H')
F['baseline_nonowner']=F.own_before.eq(0)
F['benchmark_conflict']=F.fund_id.eq('56053')&F.review.str.startswith('2019')
# Fund-level position-pair availability, without reading any quantities/changes.
Q=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz',usecols=['event_id','fund_id'],dtype={'fund_id':str})
qkeys=set(map(tuple,Q.to_numpy()))
F['prior_quantity_pair_key']=[(e,f) in qkeys for e,f in zip(F.event_id,F.fund_id)]
# Old validated common event+fixed3control support. No component or pp loaded.
K=pd.read_csv(O.parents[1]/'contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz',usecols=['event_id','fund_id','role'],dtype={'fund_id':str}).drop_duplicates()
cnt=K.groupby(['event_id','fund_id']).role.nunique();vkeys=set(cnt[cnt.eq(4)].index)
F['old_common_four_stock_valid_support']=[(e,f) in vkeys for e,f in zip(F.event_id,F.fund_id)]
F[['event_id','review','type','company','fund_id','fund_isin','name','candidate_group','own_before','company_pre_owned','baseline_nonowner','benchmark_conflict','prior_quantity_pair_key','old_common_four_stock_valid_support']].to_csv(O/'seb_fund_event_baseline_keys.csv',index=False)
rows=[]
for label,dat in [('continuity_candidate_all7',F),('unresolved_2019_SIX60_removed',F[~F.benchmark_conflict])]:
 for (ev,rev,typ,co),z in dat.groupby(['event_id','review','type','company']):
  b=z[z.candidate_group.eq('B')];h=z[z.candidate_group.eq('H')]
  if len(b)==0 or len(h)==0:continue
  rb=b[b.baseline_nonowner];rh=h[h.baseline_nonowner]
  risk=bool(z.company_pre_owned.any() and len(rb)>0 and len(rh)>0)
  rows.append(dict(screen=label,event_id=ev,review=rev,type=typ,company=co,company_pre_owned=bool(z.company_pre_owned.any()),both_risk_sets_nonempty=risk,B_funds=len(b),H_funds=len(h),B_before_owners=int(b.own_before.sum()),H_before_owners=int(h.own_before.sum()),B_nonowners=len(rb),H_nonowners=len(rh),B_quantity_pair_keys=int(rb.prior_quantity_pair_key.sum()),H_quantity_pair_keys=int(rh.prior_quantity_pair_key.sum()),all_risk_funds_old_common_four_support=bool(risk and rb.old_common_four_stock_valid_support.all() and rh.old_common_four_stock_valid_support.all())))
E=pd.DataFrame(rows);E.to_csv(O/'seb_company_event_baseline.csv',index=False)
out=[]
for (s,t),z in E.groupby(['screen','type']):
 for rule,mask in [('all',pd.Series(True,index=z.index)),('company_old_owner',z.company_pre_owned),('both_nonowner_risk_sets',z.both_risk_sets_nonempty),('both_risk_sets_old_common4_support',z.all_risk_funds_old_common_four_support)]:
  a=z[mask];out.append(dict(screen=s,type=t,rule=rule,events=len(a),reviews=a.review.nunique(),legal_names=a.company.nunique(),B_fund_rows=int(a.B_funds.sum()),H_fund_rows=int(a.H_funds.sum()),B_pre_owners=int(a.B_before_owners.sum()),H_pre_owners=int(a.H_before_owners.sum()),B_nonowner_rows=int(a.B_nonowners.sum()),H_nonowner_rows=int(a.H_nonowners.sum()),B_quantity_keys=int(a.B_quantity_pair_keys.sum()),H_quantity_keys=int(a.H_quantity_pair_keys.sum())))
S=pd.DataFrame(out);S.to_csv(O/'seb_baseline_support_summary.csv',index=False)
E[E.type.eq('addition')&E.both_risk_sets_nonempty].groupby(['screen','review']).agg(events=('event_id','size'),B_risk_rows=('B_nonowners','sum'),H_risk_rows=('H_nonowners','sum'),common4_events=('all_risk_funds_old_common_four_support','sum')).reset_index().to_csv(O/'seb_baseline_by_review.csv',index=False)
print(S.to_string(index=False))
(O/'SEB_SUPPORT_RUN.json').write_text(json.dumps(dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),only_baseline_and_support_keys=True,new_outcomes_loaded=False,active_history_certified=False),indent=2))
