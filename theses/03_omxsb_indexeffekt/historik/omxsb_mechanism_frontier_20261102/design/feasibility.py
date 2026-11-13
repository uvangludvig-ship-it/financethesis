import os
from pathlib import Path
import pandas as pd,numpy as np,json
R=Path(os.environ.get('FINANCETHESIS_REPO', str(Path(__file__).resolve().parents[3])));O=Path(__file__).resolve().parent;W=R/'output/omxsb_open_questions_20261102'
allcols=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',nrows=0).columns
meta=['event_id','RIC','type','review_cycle','announcement_date','effective_date','company','ticker','isin']
A=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',usecols=[c for c in meta if c in allcols])
A['AD']=pd.to_datetime(A.announcement_date);A['ED']=pd.to_datetime(A.effective_date);A=A.sort_values(['AD','event_id'])
P=pd.read_csv(R/'output/omxsb_replication_2007/events_car.csv',usecols=['event_id','RIC','AD','ED','type','review_cycle'],parse_dates=['AD','ED'])
fiids=set(pd.read_csv(W/'demand/event_group_decomposition.csv',usecols=['event_id']).event_id)
F=A[A.event_id.isin(fiids)].copy();assert len(F)==216
summaries=[];pairs=[];triples=[];security=[]
for name,d in [('full_source_mapped',A[A.RIC.notna()]),('priced487_metadata',P),('locked_FI216',F)]:
 groups=d.groupby('RIC');repeated=groups.size();both=groups.type.nunique();repkeys=set(repeated[repeated>=2].index);bothkeys=set(both[both==2].index)
 pp=[];tt=[]
 for ric,g in groups:
  g=g.sort_values(['AD','event_id']).reset_index(drop=True)
  security.append(dict(population=name,RIC=ric,N=len(g),additions=int(g.type.eq('addition').sum()),deletions=int(g.type.eq('deletion').sum()),reviews=g.review_cycle.nunique(),first_AD=str(g.AD.iloc[0].date()),last_AD=str(g.AD.iloc[-1].date()),directions=' '.join('A'if t=='addition'else'D'for t in g.type)))
  for i in range(1,len(g)):
   a,b=g.iloc[i-1],g.iloc[i]
   z=dict(population=name,RIC=ric,first_id=a.event_id,second_id=b.event_id,first_type=a.type,second_type=b.type,first_review=a.review_cycle,second_review=b.review_cycle,days=int((b.AD-a.AD).days),opposite=bool(a.type!=b.type))
   pairs.append(z);pp.append(z)
  for i in range(2,len(g)):
   a,b,c=g.iloc[i-2],g.iloc[i-1],g.iloc[i]
   if a.type!=b.type and b.type!=c.type:
    z=dict(population=name,RIC=ric,first_id=a.event_id,middle_id=b.event_id,last_id=c.event_id,first_review=a.review_cycle,middle_review=b.review_cycle,last_review=c.review_cycle,pattern='ADA'if a.type=='addition'else'DAD',days=int((c.AD-a.AD).days))
    triples.append(z);tt.append(z)
 summaries.append(dict(population=name,N=len(d),unique_RIC=d.RIC.nunique(),reviews=d.review_cycle.nunique(),repeated_RIC=len(repkeys),events_in_repeated_RIC=int(d.RIC.isin(repkeys).sum()),both_direction_RIC=len(bothkeys),events_in_both_direction_RIC=int(d.RIC.isin(bothkeys).sum()),opposite_adjacent_pairs=sum(x['opposite']for x in pp),same_direction_adjacent_pairs=sum(not x['opposite']for x in pp),complete_ADA_triples=sum(x['pattern']=='ADA'for x in tt),complete_DAD_triples=sum(x['pattern']=='DAD'for x in tt),unique_RIC_with_triples=len({x['RIC']for x in tt})))
S=pd.DataFrame(summaries);S.to_csv(O/'repeated_switcher_counts.csv',index=False);pd.DataFrame(pairs).to_csv(O/'successive_events.csv',index=False);pd.DataFrame(triples).to_csv(O/'complete_triples.csv',index=False);pd.DataFrame(security).to_csv(O/'security_metadata_counts.csv',index=False)
# Descriptive sequence since the start of observed history, never first-ever membership.
seen={};history=[]
for x in A.itertuples():
 if not isinstance(x.RIC,str):continue
 prior=seen.get(x.RIC,[]);history.append(dict(event_id=x.event_id,RIC=x.RIC,type=x.type,review=x.review_cycle,prior_observed_events=len(prior),prior_observed_additions=sum(t=='addition'for t in prior),prior_observed_deletions=sum(t=='deletion'for t in prior),observed_reentry=x.type=='addition'and'deletion'in prior,FI_locked=x.event_id in fiids));seen.setdefault(x.RIC,[]).append(x.type)
hist=pd.DataFrame(history);hist.to_csv(O/'observed_event_history.csv',index=False)
# Existing corrected membership chain. A chain correction is not an independent original membership file.
M=pd.read_csv(R/'code/claude_checks/data/medlemskap_verifierad.csv');cycle=A.groupby('review_cycle').ED.first().sort_values().index.tolist();mi={c:M[M.review_after==c].set_index('ric').status.to_dict()for c in cycle}
fullroster=[]
for k,c in enumerate(cycle):
 if k==0:continue
 pre=mi.get(cycle[k-1],{});post=mi.get(c,{})
 inc=sorted(set(r for r,s in pre.items()if s=='medlem')&set(r for r,s in post.items()if s=='medlem'))
 for r in inc:fullroster.append(dict(review=c,RIC=r,previous_review=cycle[k-1],continuing_member=True))
I=pd.DataFrame(fullroster);I.to_csv(O/'incumbent_member_candidates.csv',index=False)
# Fixed new dated control roles; membership diagnostic, no rematching or returns.
C=pd.read_csv(W/'eligible_rematch/selected_controls.csv');C=C.merge(hist[['event_id','FI_locked']],on='event_id',how='left');C['previous_review']=C.review.map(lambda c:cycle[cycle.index(c)-1]if c in cycle and cycle.index(c)>0 else None)
C['membership_before']= [mi.get(p,{}).get(r,'not_in_chain')for p,r in zip(C.previous_review,C.ric)]
C['membership_after']= [mi.get(c,{}).get(r,'not_in_chain')for c,r in zip(C.review,C.ric)]
C['continuing_member']=C.membership_before.eq('medlem')&C.membership_after.eq('medlem')
C.to_csv(O/'fixed_control_membership_diagnostic.csv',index=False)
extra=dict(full_event_source_N=len(A),mapped_RIC=int(A.RIC.notna().sum()),missing_RIC=int(A.RIC.isna().sum()),FI_first_addition_since_sample=int((hist.FI_locked&hist.type.eq('addition')&hist.prior_observed_additions.eq(0)).sum()),FI_observed_reentries=int((hist.FI_locked&hist.observed_reentry).sum()),FI_controls_rows=int(C.FI_locked.fillna(False).sum()),FI_current_member_control_rows=int(C.loc[C.FI_locked.fillna(False),'continuing_member'].sum()),membership_status_counts=M.status.value_counts().to_dict(),incumbents_min=int(I.groupby('review').size().min()),incumbents_max=int(I.groupby('review').size().max()),incumbents_FI_review_counts=I[I.review.isin(F.review_cycle)].groupby('review').size().to_dict())
(O/'summary.json').write_text(json.dumps(extra,indent=2));print(S.to_string(index=False));print(json.dumps(extra,indent=2));print(pd.DataFrame(security).query("population=='locked_FI216'").sort_values('N',ascending=False).head(15).to_string(index=False))
