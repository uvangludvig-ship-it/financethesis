import os
from pathlib import Path
import pandas as pd,numpy as np,json
from scipy.stats import t
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO', str(Path(__file__).resolve().parents[3])))
E=pd.read_csv(O/'decomp_event_groups.csv');F=pd.read_csv(O/'family_combined_joint_uncertainty.csv');checks=[]
for f in F.itertuples():
 z=E[E.type==f.type].groupby(['review','group']).matched_change.mean().unstack()
 a=z[['OMXSB_index_named','OMXSB_other_named']].sum(axis=1);b=z['ALL'];g=len(z);mu=np.array([a.mean(),b.mean()]);V=np.cov(np.column_stack([a,b]),rowvar=False,ddof=1)/g;crit=t.ppf(.975,g-1)
 aa=mu[1]**2-crit**2*V[1,1];bb=-2*(mu[0]*mu[1]-crit**2*V[0,1]);cc=mu[0]**2-crit**2*V[0,0];disc=bb*bb-4*aa*cc
 roots=sorted([(-bb-np.sqrt(disc))/(2*aa),(-bb+np.sqrt(disc))/(2*aa)])
 own=dict(G=g,family_count=mu[0],total_count=mu[1],family_ci_low=mu[0]-crit*np.sqrt(V[0,0]),family_ci_high=mu[0]+crit*np.sqrt(V[0,0]),ratio_point=mu[0]/mu[1],fieller_low=roots[0],fieller_high=roots[1],fieller_bounded=bool(aa>0 and disc>=0))
 dif={k:float(v-getattr(f,k))for k,v in own.items()if k!='fieller_bounded'};passed=all(abs(x)<1e-10 for x in dif.values())and own['fieller_bounded']==f.fieller_bounded
 assert passed;checks.append(dict(type=f.type,independent=own,differences=dif,pass_all=passed,covariance_of_review_means=V.tolist(),ratio_is_signed_unclipped=True))
# Exact current H sample and dated-control role coverage.
Q=pd.read_csv(O/'event_ownership.csv');ids=set(Q[Q.support=='post'].event_id);S=pd.read_csv(O/'security_role_gate.csv');roles=S[S.event_id.isin(ids)&S.role.ne('event')].copy();assert len(roles)==3*len(ids)
m=pd.read_csv(R/'code/claude_checks/data/medlemskap_verifierad.csv');ev=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',usecols=['review_cycle','effective_date']);cycle=ev.groupby('review_cycle').effective_date.first().sort_values().index.tolist();pos={c:i for i,c in enumerate(cycle)};known=m.set_index(['review_after','ric']).status.to_dict()
roles['before_status']=[known.get((cycle[pos[c]-1],ric),'not_in_chain')if pos[c]>0 else'unknown_first_review'for c,ric in zip(roles.review,roles.ric)]
roles['after_status']=[known.get((c,ric),'not_in_chain')for c,ric in zip(roles.review,roles.ric)]
roles['incumbent_before_and_after']=roles.before_status.eq('medlem')&roles.after_status.eq('medlem');roles.to_csv(O/'independent_current_sample_membership.csv',index=False)
counts=[]
for typ,q in [('ALL',roles)]+list(roles.groupby('type')):
 counts.append(dict(type=typ,event_count=q.event_id.nunique(),control_roles=len(q),incumbent_control_roles=int(q.incumbent_before_and_after.sum()),incumbent_control_fraction=float(q.incumbent_before_and_after.mean()),member_before_roles=int(q.before_status.eq('medlem').sum()),member_after_roles=int(q.after_status.eq('medlem').sum()),uncertain_either_endpoint_roles=int((q.before_status.eq('osäker')|q.after_status.eq('osäker')).sum())))
G=pd.read_csv(O/'H_fund_review_gate.csv');C=pd.read_csv(O/'coverage.csv');X=pd.read_csv(O/'ambiguous_fund_exclusions.csv');post=C[C.eligible];T=pd.read_csv(O/'security_role_gate.csv');unsupported=T[~(T.q0_supported&T.q1_supported)]
countgate=dict(initial_matched_events=S.event_id.nunique(),initial_roles=len(S),events_all4_q0=int(S.groupby('event_id').q0_supported.all().sum()),events_all4_q0q1=int(S.groupby('event_id')[['q0_supported','q1_supported']].all().all(axis=1).sum()),unsupported_roles=unsupported[['event_id','role','ric','q0_supported','q1_supported']].to_dict('records'),H_fund_review_candidates=len(G),H_fund_review_eligible=int(G.eligible.sum()),H_fund_review_excluded=int((~G.eligible).sum()),H_eligible_unique_funds=G[G.eligible].fund_id.nunique(),post_events=int(C.eligible.sum()),post_additions=int(post.type.eq('addition').sum()),post_deletions=int(post.type.eq('deletion').sum()),post_reviews=post.review.nunique(),primary_unique_event_fund_exclusions=int((post.funds_before_quality-post.funds_after_quality).sum()),exclusion_role_fund_endpoint_rows=len(X),exclusions_unique_event_funds=X[['event_id','fund_id']].drop_duplicates().shape[0],post_funds_median=float(post.funds_after_quality.median()),post_funds_min=int(post.funds_after_quality.min()),post_funds_max=int(post.funds_after_quality.max()),three_quarter_events=int(post.pretrend_funds.gt(0).sum()),three_quarter_additions=int((post.pretrend_funds.gt(0)&post.type.eq('addition')).sum()),three_quarter_deletions=int((post.pretrend_funds.gt(0)&post.type.eq('deletion')).sum()))
# Confirm the stale note correction has reached both the script and current JSON.
v=json.loads((O/'independent_validation.json').read_text());assert 'Corrected nse' in v['declared_group_note'];assert 'Corrected nse' in (O/'independent_validation.py').read_text()
out=dict(family_joint_uncertainty_pass=True,Fieller=checks,current_sample_control_membership=counts,initial_and_retained_coverage=countgate,H_validation_stale_note_fixed=True,interpretation='Nominal exploratory joint uncertainty for ratio of signed mean owner-count contrasts; not causal mechanism share or share of capital. Membership counts use corrected event-chain membership, not independently dated constituent weights.')
(O/'independent_final_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
