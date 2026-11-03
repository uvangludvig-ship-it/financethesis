"""Frozen A/B/C source coverage on the same event/control/fund population."""
from pathlib import Path
import pandas as pd,numpy as np,json,datetime,hashlib
O=Path(__file__).resolve().parent;W=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis');OLD=W/'design_frontier_20261103/independent';PIL=W/'shof_pilot_20261103/audit';CAP=W/'contribution_round_20261103/ownership_capital';OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership'
paths=[O/'PRE_COVERAGE_UPDATE_SPEC.txt',O/'source_feasibility.py',O/'monthly_source_fund_feasibility.csv',OLD/'monthly_source_fund_feasibility.csv',O/'event_role_capital_coverage.csv',OLD/'event_role_capital_coverage.csv',PIL/'FUND_24MONTH_SOURCE_HISTORY_OLD_NEW.csv',PIL/'VENDOR_NF_PRESENCE_ONLY_24MONTH.csv',PIL/'VENDOR_NF_24MONTH_SOURCE_HISTORY.csv',CAP/'normalized_fund_role_contributions.csv.gz',CAP/'security_feasibility_gate.csv',OWN/'security_role_gate.csv',OWN/'fund_metadata_classification.csv',OLD/'source_stage_diagnostics.csv',R/'data/derived/fi/fi_holdings_long.csv.gz',Path(__file__)]
(O/'COVERAGE_UPDATE_LOCK.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Source-capital coverage only; no fundreturn/flow/covariance/risk outcome.','inputs':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}},indent=2))
# A is rerun byte-identically; verify every source and capitalcoverage field.
assert (O/'source_feasibility.py').read_bytes()==(OLD/'source_feasibility.py').read_bytes()
baseline={}
for name,keys in [('monthly_source_fund_feasibility.csv',['review','fund_id']),('event_role_capital_coverage.csv',['event_id','role','endpoint'])]:
 a=pd.read_csv(O/name,dtype={'fund_id':str});b=pd.read_csv(OLD/name,dtype={'fund_id':str});a=a.sort_values(keys).reset_index(drop=True);b=b.sort_values(keys).reset_index(drop=True);pd.testing.assert_frame_equal(a,b,check_exact=True);baseline[name]={'rows':len(a),'all_fields_exact':True}
H=pd.read_csv(O/'monthly_source_fund_feasibility.csv',dtype={'fund_id':str});J=pd.read_csv(PIL/'FUND_24MONTH_SOURCE_HISTORY_OLD_NEW.csv',dtype={'FI_fund_id':str}).rename(columns={'FI_fund_id':'fund_id'});pilot=set(J.fund_id)
E=H.merge(J[['review','fund_id','new_strict25endpoint_metadata_pass']],on=['review','fund_id'],how='left',validate='1:1');E['is_pilot']=E.fund_id.isin(pilot)
E['A']=E.provisional25endpoint_pass
E['C']=E.is_pilot&E.exact_stable_endpoint_map&E.new_strict25endpoint_metadata_pass.fillna(False)
E['B']=E.A.where(~E.is_pilot,E.C)
assert E.loc[~E.is_pilot,'A'].equals(E.loc[~E.is_pilot,'B'])
E.to_csv(O/'fund_review_source_eligibility_ABC.csv',index=False)
elig={s:{rev:set(d.loc[d[s],'fund_id']) for rev,d in E.groupby('review')} for s in ['A','B','C']}
# Keep vendor routes wholly separate. ClassNF presence is a conditional class-source coverage appendix.
VN=pd.read_csv(PIL/'VENDOR_NF_PRESENCE_ONLY_24MONTH.csv',dtype={'FI_fund_id':str});VC=pd.read_csv(PIL/'VENDOR_NF_24MONTH_SOURCE_HISTORY.csv',dtype={'FI_fund_id':str})
for route,df,col in [('V_fundNF',VN,'fund_NF_presence_complete24'),('V_classNF',VC,'class_NF_all_recorded_dates_complete_24month_pass')]:
 elig[route]={rev:set(d.loc[d[col],'FI_fund_id'])&set(E.loc[E.review.eq(rev)&E.exact_stable_endpoint_map,'fund_id']) for rev,d in df.groupby('review')}
L=pd.read_csv(CAP/'normalized_fund_role_contributions.csv.gz',dtype={'fund_id':str},usecols=['event_id','review','type','role','fund_id']);L=L[L.review.le('2023H2')]
assert not L.duplicated(['event_id','role','fund_id']).any()
S=pd.read_csv(OWN/'security_role_gate.csv');S=S[S.event_id.isin(L.event_id)];SG=pd.read_csv(CAP/'security_feasibility_gate.csv',usecols=['review','ric','factor']);S=S.merge(SG,on=['review','ric'],validate='m:1')
assert len(S)==4*L.event_id.nunique() and not S.duplicated(['event_id','role']).any()
pops={}
for eid,d in L.groupby('event_id'):
 sets={role:set(g.fund_id) for role,g in d.groupby('role')};assert set(sets)=={'event','c1','c2','c3'};assert len({tuple(sorted(v)) for v in sets.values()})==1;pops[eid]=sets['event']
cols={'ISIN-kod_instrument':'isin','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','Antal':'qty','Marknadsvärde_instrument':'value','Valuta':'currency','Tillgångsslag_enligt_LVF_5_kap':'asset_type'}
ids=set(S.aliases.str.split(';').explode());dates=set(S.q0)|set(S.q1);parts=[]
for d in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=list(cols),dtype={'Fond_institutnummer':str},chunksize=500000):
 d=d.rename(columns=cols);parts.append(d[d['isin'].isin(ids)&d.quarter.isin(dates)])
RAW=pd.concat(parts,ignore_index=True)
for c in ['qty','value']:RAW[c]=pd.to_numeric(RAW[c],errors='coerce')
cache={};pricecheck=[]
for (rev,ric),ss in S.groupby(['review','ric']):
 a=ss.iloc[0];d=RAW[RAW['isin'].isin(a.aliases.split(';'))&RAW.quarter.isin([a.q0,a.q1])]
 after=d[d.quarter.eq(a.q1)&d.currency.eq('SEK')&d.asset_type.eq('ÖverlåtbartVärdepapper')&d.qty.gt(0)&d.value.gt(0)]
 price=float((after.value/after.qty).median());assert np.isfinite(price) and price>0
 q=d.groupby(['fund_id','quarter']).qty.sum(min_count=1);cache[(rev,ric)]=(q,price)
 pricecheck.append(dict(review=rev,ric=ric,price_support_rows=len(after),price_positive_finite=True,splitfactor=a.factor))
pd.DataFrame(pricecheck).to_csv(O/'coverage_price_support_flags.csv',index=False)
cells=[];gaps=[];fundcontrib=[]
for a in S.itertuples():
 pop=pops[a.event_id];qt,price=cache[(a.review,a.ric)]
 for endpoint,date,factor in [('q0',a.q0,a.factor),('q1',a.q1,1.)]:
  # Logicalzeros come only from the existing validreport population and absent stockposition.
  q=qt.xs(date,level='quarter').reindex(sorted(pop),fill_value=0.) if date in qt.index.get_level_values('quarter') else pd.Series(0.,index=sorted(pop))
  assert q.notna().all() and q.ge(0).all();q=q*factor;capital=q*price;den=float(capital.sum());n_positive=int(q.gt(0).sum())
  for scenario in elig:
   selected=pop&elig[scenario].get(a.review,set());num=float(capital[capital.index.isin(selected)].sum());fraction=num/den if den>0 else np.nan
   cells.append(dict(event_id=a.event_id,review=a.review,type=a.type,role=a.role,ric=a.ric,endpoint=endpoint,scenario=scenario,population_funds=len(pop),eligible_funds=len(selected),positive_owners=n_positive,eligible_positive_owners=int(q[q.index.isin(selected)].gt(0).sum()),coverage_fraction=fraction,denominator_SEK_at_q1price=den if den>0 else np.nan,covered_SEK_at_q1price=num if den>0 else np.nan))
  bset=pop&elig['B'].get(a.review,set())
  for fid,val in capital[capital.gt(0)].items():
   if fid not in bset:gaps.append(dict(event_id=a.event_id,review=a.review,type=a.type,role=a.role,endpoint=endpoint,fund_id=fid,missing_SEK=val,missing_fraction_of_cell=val/den))
D=pd.DataFrame(cells);D.to_csv(O/'event_role_endpoint_coverage.csv',index=False)
assert D.groupby(['event_id','scenario']).eligible_funds.nunique().eq(1).all()
# Independently reconstructed A agrees with original quantityfraction to floating precision.
prior=pd.read_csv(O/'event_role_capital_coverage.csv');a=D[D.scenario.eq('A')].merge(prior[['event_id','role','endpoint','history_capital_fraction']],on=['event_id','role','endpoint'],validate='1:1');maxerr=float((a.coverage_fraction-a.history_capital_fraction).abs().max());assert maxerr<1e-12

def summarize(d,keys):
 out=[]
 for key,g in d.groupby(keys,dropna=False):
  if not isinstance(key,tuple):key=(key,)
  r=dict(zip(keys,key));valid=g.coverage_fraction.notna();z=g[valid];den=z.denominator_SEK_at_q1price.sum()
  r.update(cells=len(g),events=g.event_id.nunique(),missing_cells=int((~valid).sum()),equal_cell_mean_fraction=z.coverage_fraction.mean(),median_fraction=z.coverage_fraction.median(),minimum_fraction=z.coverage_fraction.min(),pooled_SEK_coverage_fraction=z.covered_SEK_at_q1price.sum()/den if den>0 else np.nan)
  for threshold in [.5,.75,.9]:r['cells_ge_'+str(int(threshold*100))]=int(z.coverage_fraction.ge(threshold).sum())
  out.append(r)
 return pd.DataFrame(out)
summarize(D,['scenario','review','type','role','endpoint']).to_csv(O/'review_side_role_endpoint_summary.csv',index=False)
summarize(D,['scenario','type','role','endpoint']).to_csv(O/'side_role_endpoint_summary.csv',index=False)
summarize(D,['scenario','role','endpoint']).to_csv(O/'overall_role_endpoint_summary.csv',index=False)
event=[]
for (sc,eid),g in D.groupby(['scenario','event_id']):
 assert len(g)==8;r=dict(scenario=sc,event_id=eid,review=g.review.iloc[0],type=g.type.iloc[0],cells=len(g),missing_cells=int(g.coverage_fraction.isna().sum()),minimum_all8_fraction=g.coverage_fraction.min() if g.coverage_fraction.notna().all() else np.nan)
 for t in [.5,.75,.9]:r['all8_ge_'+str(int(t*100))]=bool(g.coverage_fraction.notna().all() and g.coverage_fraction.ge(t).all())
 event.append(r)
EV=pd.DataFrame(event);EV.to_csv(O/'event_all8cell_coverage.csv',index=False)
evsum=EV.groupby(['scenario','review','type']).agg(events=('event_id','size'),events_missing_any=('missing_cells',lambda x:int(x.gt(0).sum())),all8_ge_50=('all8_ge_50','sum'),all8_ge_75=('all8_ge_75','sum'),all8_ge_90=('all8_ge_90','sum'),mean_minimum_all8=('minimum_all8_fraction','mean')).reset_index();evsum.to_csv(O/'review_side_all8_thresholds.csv',index=False)
GAP=pd.DataFrame(gaps);names=pd.read_csv(OWN/'fund_metadata_classification.csv',dtype={'fund_id':str},usecols=['fund_id','quarter','fund_name','company']);qmap=S[['review','q0']].drop_duplicates();names=names.merge(qmap,left_on='quarter',right_on='q0').drop_duplicates(['review','fund_id'])
stage=pd.read_csv(OLD/'source_stage_diagnostics.csv',dtype={'fund_id':str})
ranking=[];reviewranking=[]
for scope,g in [('event_role',GAP[GAP.role.eq('event')]),('all4roles',GAP)]:
 den=D[D.scenario.eq('B')&(D.role.eq('event') if scope=='event_role' else True)].denominator_SEK_at_q1price.sum();ncells=int(D[D.scenario.eq('B')&(D.role.eq('event') if scope=='event_role' else True)].shape[0])
 z=g.groupby('fund_id').agg(missing_SEK=('missing_SEK','sum'),missing_fraction_sum=('missing_fraction_of_cell','sum'),affected_cells=('event_id','size'),affected_events=('event_id','nunique'),reviews=('review','nunique')).reset_index();z['scope']=scope;z['share_of_total_fixed_population_SEK']=z.missing_SEK/den;z['mean_missing_fraction_across_all_cells']=z.missing_fraction_sum/ncells;z['share_of_all_missing_SEK']=z.missing_SEK/z.missing_SEK.sum();z=z.sort_values('missing_SEK',ascending=False);z['rank']=range(1,len(z)+1)
 latest=names.sort_values('quarter').drop_duplicates('fund_id',keep='last')[['fund_id','fund_name','company']];z=z.merge(latest,on='fund_id',how='left',validate='1:1');ranking.append(z)
 rr=g.groupby(['review','fund_id']).agg(missing_SEK=('missing_SEK','sum'),affected_cells=('event_id','size'),affected_events=('event_id','nunique'),missing_fraction_sum=('missing_fraction_of_cell','sum')).reset_index();rr=rr.merge(E[['review','fund_id','fundid','exact_stable_endpoint_map','A','B','C','is_pilot','month_count','capital_reconciled_endpoints','complete_TNA_TRI_endpoints','stable_classes','class_life_dates_ok','new_strict25endpoint_metadata_pass']],on=['review','fund_id'],how='left',validate='1:1').merge(names[['review','fund_id','fund_name','company']],on=['review','fund_id'],how='left',validate='1:1');rr['scope']=scope;rr=rr.merge(stage.drop(columns=['fundid','eligible']),on=['review','fund_id'],how='left',validate='1:1');reviewranking.append(rr)
RANK=pd.concat(ranking,ignore_index=True);RANK.to_csv(O/'remaining_fund_gap_ranking_B.csv',index=False)
RR=pd.concat(reviewranking,ignore_index=True);RR.to_csv(O/'remaining_fund_review_gaps_B.csv',index=False)
topids=set(RANK[RANK['rank'].le(15)].fund_id);RR[RR.fund_id.isin(topids)].to_csv(O/'top15_remaining_source_diagnostics.csv',index=False)
sumoverall=summarize(D,['scenario']);sumoverall.to_csv(O/'overall_allcell_summary.csv',index=False)
sourcecounts=E.groupby('review')[['A','B','C']].sum().reset_index();sourcecounts.to_csv(O/'source_eligible_funds_by_review.csv',index=False)
validation={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_exact_reproduction':baseline,'original_script_byte_identical':True,'A_independent_capital_fraction_maxerror':maxerr,'events':L.event_id.nunique(),'additions':S.loc[S.role.eq('event')&S.type.eq('addition'),'event_id'].nunique(),'deletions':S.loc[S.role.eq('event')&S.type.eq('deletion'),'event_id'].nunique(),'reviews':S.review.nunique(),'same_fund_population_all4roles':True,'same_eligible_fund_set_all8cells':True,'nonpilot_eligibility_unchanged':True,'missing_coverage_cells':int(D.coverage_fraction.isna().sum()),'no_economic_outcomes':True,'source_windows_updated':int((E.A!=E.B).sum()),'thresholds_are_descriptive_not_power_or_GO':True,'all8_threshold_counts':EV.groupby('scenario')[['all8_ge_50','all8_ge_75','all8_ge_90']].sum().to_dict('index')}
(O/'COVERAGE_VALIDATION.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2));print(sumoverall.to_string(index=False));print(RANK[RANK.scope.eq('event_role')].head(15).to_string(index=False))
