"""E replacement or final F allraw source coverage; no economic outcomes."""
from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime,argparse
O=Path(__file__).resolve().parent;W=O.parents[1];SM=W/'shof_coverage_20261103/source_method';CAP=W/'contribution_round_20261103/ownership_capital';OWN=Path('/Users/ludviguvang/dev/financethesis/output/omxsb_mechanism_frontier_20261102/ownership');RAWPATH=Path('/Users/ludviguvang/dev/financethesis/data/derived/fi/fi_holdings_long.csv.gz')
ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['E','F'],required=True);ap.add_argument('--old-a-source',type=Path);args=ap.parse_args();ST=args.stage
if ST=='F' and not args.old_a_source:ap.error('F requires allremaining oldA rawsource flags')
FIVE=SM/'D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv';TEN=SM/'next10_ECB/NEXT10_D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv';paths=[O/'PRE_E_PROPAGATION_SPEC.txt',FIVE,TEN,O/'event_role_endpoint_coverage.csv',O/'D_event_role_endpoint_coverage.csv',O/'fund_review_source_eligibility_ABC.csv',CAP/'normalized_fund_role_contributions.csv.gz',CAP/'security_feasibility_gate.csv',OWN/'security_role_gate.csv',RAWPATH,Path(__file__)]
if args.old_a_source:paths.append(args.old_a_source)
oldfiles={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.is_file() and (p.name.startswith(('D_','E_')) or p.name=='FILE_LEDGER_ABC.json') and not p.name.startswith(ST+'_')}
(O/f'{ST}_PROPAGATION_LOCK.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':ST,'scope':'Samepopulation sourcecoverage only; no return/flow/covariance/risk outcome.','E_replaces_all15_oldA_contributions':True,'F_uses_no_oldA_fallback':ST=='F','inputs':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths},'preserved_oldfiles':oldfiles},indent=2))
snapshot=json.loads((O/'FILE_LEDGER_ABC.json').read_text())
def checkold():
 for name,info in snapshot['files'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==info['sha256'],name
 for name,h in oldfiles.items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==h,name
checkold()
H=pd.read_csv(O/'fund_review_source_eligibility_ABC.csv',dtype={'fund_id':str});AOLD=pd.read_csv(O/'event_role_endpoint_coverage.csv');DOLD=pd.read_csv(O/'D_event_role_endpoint_coverage.csv')
F5=pd.read_csv(FIVE,dtype={'FI_fund_id':str}).rename(columns={'FI_fund_id':'fund_id'});S5=F5[['review','fund_id','fundid','D_RIPS_source_supported','D_NAV_conditional_source_supported']].rename(columns={'D_RIPS_source_supported':'native','D_NAV_conditional_source_supported':'nav_conditional'});S5['source_batch']='fivepilot'
F10=pd.read_csv(TEN,dtype={'FI_fund_id':str}).rename(columns={'FI_fund_id':'fund_id'});S10=F10[['review','fund_id','fundid','D_RIPS_ECB_source_supported']].rename(columns={'D_RIPS_ECB_source_supported':'native'});S10['nav_conditional']=S10.native;S10['source_batch']='next10_RIPS_ECB'
sources=[S5,S10]
if args.old_a_source:
 X=pd.read_csv(args.old_a_source,dtype={'FI_fund_id':str,'fund_id':str}).rename(columns={'FI_fund_id':'fund_id'})
 flag='D_RIPS_ECB_source_supported';assert flag in X
 Q=X[['review','fund_id','fundid',flag]].rename(columns={flag:'native'});Q['nav_conditional']=Q.native;Q['source_batch']='existing_A_rawvalidation';sources.append(Q)
SRC=pd.concat(sources,ignore_index=True);assert not SRC.duplicated(['review','fund_id']).any();rawfunds=set(SRC.fund_id);assert len(rawfunds)==(15 if ST=='E' else 178)
EL=H.merge(SRC,on=['review','fund_id'],how='left',validate='1:1',suffixes=('','_raw'));EL['is_raw_batch']=EL.fund_id.isin(rawfunds)
assert EL.loc[EL.is_raw_batch,'source_batch'].notna().all()
assert (EL.loc[EL.is_raw_batch,'fundid'].fillna('')==EL.loc[EL.is_raw_batch,'fundid_raw'].fillna('')).all()
EL['raw_native']=EL.is_raw_batch&EL.exact_stable_endpoint_map&EL.native.fillna(False)
EL['raw_nav_conditional']=EL.is_raw_batch&EL.exact_stable_endpoint_map&EL.nav_conditional.fillna(False)
if ST=='E':
 scenarios={'E_RIPS_newraw15':('raw_native',False),'E_RIPS_hybrid':('raw_native',True),'E_NAV_conditional_newraw15':('raw_nav_conditional',False),'E_NAV_conditional_hybrid':('raw_nav_conditional',True)}
else:scenarios={'F_RIPS_allraw':('raw_native',False),'F_NAV_conditional_allraw':('raw_nav_conditional',False)}
for sc,(col,hybrid) in scenarios.items():EL[sc]=EL[col]|(EL.A&~EL.is_raw_batch if hybrid else False)
EL.to_csv(O/f'{ST}_fund_review_source_eligibility.csv',index=False)
elig={sc:{rev:set(z.loc[z[sc],'fund_id']) for rev,z in EL.groupby('review')} for sc in scenarios}
Asets={rev:set(z.loc[z.A,'fund_id']) for rev,z in H.groupby('review')};Csets={rev:set(z.loc[z.C,'fund_id']) for rev,z in H.groupby('review')};fiveR={rev:set(z.loc[z.D_RIPS_source_supported,'fund_id']) for rev,z in F5.groupby('review')}
L=pd.read_csv(CAP/'normalized_fund_role_contributions.csv.gz',dtype={'fund_id':str},usecols=['event_id','review','role','fund_id']);L=L[L.review.le('2023H2')];pops={}
for eid,d in L.groupby('event_id'):
 sets=[set(g.fund_id) for _,g in d.groupby('role')];assert len(sets)==4 and all(x==sets[0] for x in sets);pops[eid]=sets[0]
S=pd.read_csv(OWN/'security_role_gate.csv');S=S[S.event_id.isin(L.event_id)].merge(pd.read_csv(CAP/'security_feasibility_gate.csv',usecols=['review','ric','factor']),on=['review','ric'],validate='m:1')
cols={'ISIN-kod_instrument':'isin','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','Antal':'qty','Marknadsvärde_instrument':'value','Valuta':'currency','Tillgångsslag_enligt_LVF_5_kap':'asset_type'};ids=set(S.aliases.str.split(';').explode());dates=set(S.q0)|set(S.q1);parts=[]
for d in pd.read_csv(RAWPATH,usecols=list(cols),dtype={'Fond_institutnummer':str},chunksize=500000):
 d=d.rename(columns=cols);parts.append(d[d['isin'].isin(ids)&d.quarter.isin(dates)])
R=pd.concat(parts,ignore_index=True)
for c in ['qty','value']:R[c]=pd.to_numeric(R[c],errors='coerce')
cache={}
for (rev,ric),ss in S.groupby(['review','ric']):
 a=ss.iloc[0];d=R[R['isin'].isin(a.aliases.split(';'))&R.quarter.isin([a.q0,a.q1])];aft=d[d.quarter.eq(a.q1)&d.currency.eq('SEK')&d.asset_type.eq('ÖverlåtbartVärdepapper')&d.qty.gt(0)&d.value.gt(0)];price=float((aft.value/aft.qty).median());assert np.isfinite(price) and price>0
 cache[(rev,ric)]=(d.groupby(['fund_id','quarter']).qty.sum(min_count=1),price)
base=AOLD[AOLD.scenario.eq('A')].set_index(['event_id','role','endpoint']);COLD=AOLD[AOLD.scenario.eq('C')].set_index(['event_id','role','endpoint']);DR=DOLD[DOLD.scenario.eq('D_RIPS_pilot')].set_index(['event_id','role','endpoint']);checks=[];rows=[];remove=[]
for a in S.itertuples():
 pop=pops[a.event_id];q,price=cache[(a.review,a.ric)]
 for endpoint,date,fac in [('q0',a.q0,a.factor),('q1',a.q1,1.)]:
  vals=pd.Series({fid:float(q.get((fid,date),0))*fac*price for fid in pop},dtype=float);assert vals.notna().all() and vals.ge(0).all();key=(a.event_id,a.role,endpoint);b=base.loc[key];den=float(vals.sum());assert abs(den-b.denominator_SEK_at_q1price)/max(1,den)<1e-12
  anum=float(vals[vals.index.isin(Asets[a.review])].sum());cnum=float(vals[vals.index.isin(Csets[a.review])].sum());drnum=float(vals[vals.index.isin(fiveR[a.review])].sum())
  checks.extend([abs(anum-b.covered_SEK_at_q1price)/max(1,den),abs(cnum-COLD.loc[key,'covered_SEK_at_q1price'])/max(1,den),abs(drnum-DR.loc[key,'covered_SEK_at_q1price'])/max(1,den)])
  oldraw=float(vals[vals.index.isin(rawfunds&Asets[a.review])].sum());oldother=anum-oldraw;assert oldother>=-1e-6
  remove.append(dict(event_id=a.event_id,review=a.review,role=a.role,endpoint=endpoint,oldA_rawbatch_contribution_SEK=oldraw,oldA_other_contribution_SEK=oldother))
  for sc,(col,hybrid) in scenarios.items():
   selected=pop&elig[sc].get(a.review,set());num=float(vals[vals.index.isin(selected)].sum());rawnum=float(vals[vals.index.isin(selected&rawfunds)].sum())
   assert abs(num-(rawnum+oldother if hybrid else rawnum))/max(1,den)<1e-12
   fraction=num/den if den>0 else np.nan;assert pd.isna(fraction) or -.000000000001<=fraction<=1.000000000001
   rows.append(dict(event_id=a.event_id,review=a.review,type=a.type,role=a.role,ric=a.ric,endpoint=endpoint,scenario=sc,population_funds=len(pop),eligible_funds=len(selected),coverage_fraction=fraction,denominator_SEK_at_q1price=den if den>0 else np.nan,covered_SEK_at_q1price=num if den>0 else np.nan,old_monthly_provisional_included=hybrid,conditional_NAV='NAV_conditional' in sc,historical_class_universe_fully_certified=False))
OUT=pd.DataFrame(rows);OUT.to_csv(O/f'{ST}_event_role_endpoint_coverage.csv',index=False);pd.DataFrame(remove).to_csv(O/f'{ST}_oldA_component_removal_check.csv',index=False);assert OUT.groupby(['scenario','event_id']).eligible_funds.nunique().eq(1).all();assert max(checks)<1e-12
def summarize(d,keys):
 out=[]
 for key,g in d.groupby(keys):
  if not isinstance(key,tuple):key=(key,)
  r=dict(zip(keys,key));r.update(cells=len(g),events=g.event_id.nunique(),missing_cells=int(g.coverage_fraction.isna().sum()),equal_cell_mean_fraction=g.coverage_fraction.mean(),pooled_SEK_coverage_fraction=g.covered_SEK_at_q1price.sum()/g.denominator_SEK_at_q1price.sum(),minimum_fraction=g.coverage_fraction.min(),maximum_fraction=g.coverage_fraction.max())
  for t in [.5,.75,.9]:r['cells_ge_'+str(int(t*100))]=int(g.coverage_fraction.ge(t).sum())
  out.append(r)
 return pd.DataFrame(out)
summarize(OUT,['scenario']).to_csv(O/f'{ST}_overall_coverage_summary.csv',index=False);summarize(OUT,['scenario','review','type','role','endpoint']).to_csv(O/f'{ST}_review_side_role_endpoint_summary.csv',index=False);summarize(OUT,['scenario','role','endpoint']).to_csv(O/f'{ST}_role_endpoint_summary.csv',index=False)
event=[]
for (sc,eid),g in OUT.groupby(['scenario','event_id']):
 assert len(g)==8;r=dict(scenario=sc,event_id=eid,review=g.review.iloc[0],type=g.type.iloc[0],missing_cells=int(g.coverage_fraction.isna().sum()),minimum_all8_fraction=g.coverage_fraction.min() if g.coverage_fraction.notna().all() else np.nan)
 for t in [.5,.75,.9]:r['all8_ge_'+str(int(t*100))]=bool(g.coverage_fraction.notna().all() and g.coverage_fraction.ge(t).all())
 event.append(r)
EV=pd.DataFrame(event);EV.to_csv(O/f'{ST}_event_all8cell_coverage.csv',index=False);EV.groupby(['scenario','review','type']).agg(events=('event_id','size'),all8_ge_50=('all8_ge_50','sum'),all8_ge_75=('all8_ge_75','sum'),all8_ge_90=('all8_ge_90','sum')).reset_index().to_csv(O/f'{ST}_review_side_all8_thresholds.csv',index=False)
EL.groupby('review')[list(scenarios)].sum().reset_index().to_csv(O/f'{ST}_source_eligible_funds_by_review.csv',index=False)
v={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':ST,'source_funds':len(rawfunds),'source_native_passes_before_population_intersection':int(SRC.native.sum()),'source_NAVinclusive_passes_before_population_intersection':int(SRC.nav_conditional.sum()),'fixedpopulation_raw_native_passes':int(EL.raw_native.sum()),'fixedpopulation_raw_NAVinclusive_passes':int(EL.raw_nav_conditional.sum()),'oldA_rawbatch_passes_correctly_replaced':int((EL.A&EL.is_raw_batch).sum()),'oldA_rawbatch_passes_no_longer_native_supported':int((EL.A&EL.is_raw_batch&~EL.raw_native).sum()),'A_C_D_independent_reconstruction_maxerror_as_capitalfraction':max(checks),'same_eligiblefundset_all8cells':True,'coverage_bounded_0_1':True,'events':OUT.event_id.nunique(),'no_oldA_fallback_in_F':ST=='F','no_returns_flows_covariances_risk_outcomes':True,'all8_threshold_counts':EV.groupby('scenario')[['all8_ge_50','all8_ge_75','all8_ge_90']].sum().to_dict('index')}
checkold();v['prior_artifacts_unchanged']=True;(O/f'{ST}_COVERAGE_VALIDATION.json').write_text(json.dumps(v,indent=2));print(json.dumps(v,indent=2));print(summarize(OUT,['scenario']).to_string(index=False))
