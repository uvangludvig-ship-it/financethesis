from pathlib import Path
import pandas as pd,numpy as np,json
D=Path(__file__).parent;O=D.parent/'ownership'
a=pd.read_csv(O/'decomp_fund_roles.csv.gz');m=pd.read_csv(O/'decomp_fund_groups.csv');summary=pd.read_csv(O/'decomp_results.csv');ev=pd.read_csv(O/'decomp_event_groups.csv')
assert not a.duplicated(['event_id','fund_id','role']).any()
assert a.groupby(['event_id','fund_id']).role.nunique().eq(4).all()
a['change']=a.own_after-a.own_before
f=a.pivot(index=['event_id','fund_id','review','type','group'],columns='role',values='change').reset_index()
f['contribution']=f.event-f[['c1','c2','c3']].mean(axis=1)
f=f.merge(m[['review','fund_id','name','company','pre_benchmark']],on=['review','fund_id'],validate='m:1')
cols=[];man=[]
for ty,z in f[f.group.eq('OMXSB_other_named')].groupby('type'):
 den=ev[ev.type.eq(ty)&ev.group.eq('OMXSB_other_named')].groupby('review').size();G=len(den)
 # firstaddcontributionmeansreview, preservingfullreviewdenominators.
 r=z.groupby(['review','fund_id']).contribution.sum().reset_index();r['weighted_contribution']=r.contribution/r.review.map(den)/G
 v=r.groupby('fund_id').weighted_contribution.sum().rename('owner_count_difference_contribution').reset_index()
 nam=z.sort_values('review').groupby('fund_id').agg(name=('name','last'),company=('company','last'),valid_event_pairs=('event_id','size'),reviews=('review','nunique'),benchmarks=('pre_benchmark',lambda x:' | '.join(x.dropna().unique())))
 v=v.merge(nam,on='fund_id');v['type']=ty
 total=summary.loc[summary.type.eq(ty)&summary.group.eq('OMXSB_other_named'),'mean_owner_count_difference'].iloc[0]
 assert np.isclose(v.owner_count_difference_contribution.sum(),total,atol=1e-12)
 v['share_of_group_net']=v.owner_count_difference_contribution/total
 def cls(fid):
  if fid==60320:return 'documented_Nordnet_index_mandate;Superfonden_name_not_caught'
  if fid==51482:return 'documented_index_near2024;historical_OMXSB_metadata'
  if fid==56020:return 'current_explicitly_passive_index_near_mixed;history_incomplete'
  if fid==60330:return 'documented_index_near2024_mixed_regions;history_incomplete'
  if fid==51437:return 'historically_index_near_2019;documented_passive2025;mergerJune2022'
  if fid==60967:return 'index_near2025;historical_OMXSB_FI;not_exacttracker'
  if fid in {51128,51613,51615,51617,51619,51621,60718}:return 'mixed_benchmark;documented_ACTIVE2025;historical_style_incomplete'
  if fid in {51544,51776,51496,51498,51682}:return 'prior_active_fund_candidate;historical_active_evidence_pointwise_only'
  return 'not_independently_historically_classified'
 v['independent_mandate_assessment']=v.fund_id.map(cls)
 cols.append(v.sort_values('owner_count_difference_contribution',ascending=ty!='addition'))
 # manager labelsmaychange:allocateatcontemporaneousreviewidentity.
 z['event_review_weighted_contribution']=z.contribution/z.review.map(den)/G
 mg=z.groupby('company').event_review_weighted_contribution.sum().reset_index().rename(columns={'event_review_weighted_contribution':'owner_count_difference_contribution'});mg['type']=ty;mg['share_of_group_net']=mg.owner_count_difference_contribution/total
 man.append(mg.sort_values('share_of_group_net',ascending=False))
C=pd.concat(cols);C.to_csv(D/'OMXSB_other_named_fund_contributors.csv',index=False)
M=pd.concat(man);M.to_csv(D/'OMXSB_other_named_manager_concentration.csv',index=False)
# InspectsamelegalfundISINduplicateIDs amongacceptedfunds perreview. SinglefundID=onevote regardlessofmultipleunderlyingshareclasses.
md=pd.read_csv(O/'fund_metadata_classification.csv');print('metadata fields',md.columns.tolist())
mm=m.merge(md[['quarter','fund_id','fund_isin']].rename(columns={'quarter':'q0'}),on=['q0','fund_id'],how='left',validate='m:1')
dup=mm[mm.fund_isin.notna()&mm.duplicated(['review','fund_isin'],keep=False)].sort_values(['review','fund_isin','fund_id']);dup.to_csv(D/'same_fundISIN_multiple_ID_audit.csv',index=False)
print('duplicatefundISINIDrows',len(dup))
print(C[C.type.eq('addition')][['fund_id','name','company','owner_count_difference_contribution','share_of_group_net','independent_mandate_assessment']].head(18).to_string(index=False))
print(M[M.type.eq('addition')].head(10).to_string(index=False))
(D/'owner_contributor_validation.json').write_text(json.dumps(dict(reproduces_existing_group_sum=True,no_new_models=True,duplicate_fundISIN_ID_rows=len(dup),fundIDs_additions=int(C[C.type.eq('addition')].fund_id.nunique())),indent=2))
