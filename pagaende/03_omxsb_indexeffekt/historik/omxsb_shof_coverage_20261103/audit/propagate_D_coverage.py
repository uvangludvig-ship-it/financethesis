from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime
O=Path(__file__).resolve().parent;W=O.parents[1];SM=W/'shof_coverage_20261103/source_method';CAP=W/'contribution_round_20261103/ownership_capital';OWN=Path('/Users/ludviguvang/dev/financethesis/output/omxsb_mechanism_frontier_20261102/ownership');RAWPATH=Path('/Users/ludviguvang/dev/financethesis/data/derived/fi/fi_holdings_long.csv.gz')
paths=[O/'PRE_D_PROPAGATION_SPEC.txt',SM/'SOURCE_RULE_D.txt',SM/'D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv',SM/'D_IMPLEMENTATION_LOCK.json',O/'event_role_endpoint_coverage.csv',O/'fund_review_source_eligibility_ABC.csv',CAP/'normalized_fund_role_contributions.csv.gz',CAP/'security_feasibility_gate.csv',OWN/'security_role_gate.csv',RAWPATH,Path(__file__)]
(O/'D_PROPAGATION_LOCK.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Metadata sourceflags and fixedpopulation capitalcoverage only. ConditionalNAV separate.','inputs':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}},indent=2))
snapshot=json.loads((O/'FILE_LEDGER_ABC.json').read_text())
def check_ABC():
 for name,info in snapshot['files'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==info['sha256'],name
check_ABC()
OLD=pd.read_csv(O/'event_role_endpoint_coverage.csv');H=pd.read_csv(O/'fund_review_source_eligibility_ABC.csv',dtype={'fund_id':str});F=pd.read_csv(SM/'D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv',dtype={'FI_fund_id':str}).rename(columns={'FI_fund_id':'fund_id'});pilot=set(F.fund_id)
E=H.merge(F,on=['review','fund_id'],how='left',validate='1:1',suffixes=('','_D'))
E['D_RIPS_pilot']=E.is_pilot&E.exact_stable_endpoint_map&E.D_RIPS_source_supported.fillna(False)
E['D_NAV_conditional_pilot']=E.is_pilot&E.exact_stable_endpoint_map&E.D_NAV_conditional_source_supported.fillna(False)
E['D_RIPS_hybrid']=E.A.where(~E.is_pilot,E.D_RIPS_pilot);E['D_NAV_conditional_hybrid']=E.A.where(~E.is_pilot,E.D_NAV_conditional_pilot)
assert not E.loc[E.is_pilot,'A'].any();assert (E.loc[E.C,'D_RIPS_pilot']).all();assert (E.loc[E.D_RIPS_pilot,'D_NAV_conditional_pilot']).all()
E.to_csv(O/'D_fund_review_source_eligibility.csv',index=False)
scenarios=['D_RIPS_pilot','D_RIPS_hybrid','D_NAV_conditional_pilot','D_NAV_conditional_hybrid']
elig={sc:{rev:set(z.loc[z[sc],'fund_id']) for rev,z in E.groupby('review')} for sc in scenarios}
L=pd.read_csv(CAP/'normalized_fund_role_contributions.csv.gz',dtype={'fund_id':str},usecols=['event_id','review','role','fund_id']);L=L[L.review.le('2023H2')]
pops={}
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
 q=d[d.fund_id.isin(pilot)].groupby(['fund_id','quarter']).qty.sum(min_count=1);cache[(rev,ric)]=(q,price)
base=OLD[OLD.scenario.eq('A')].set_index(['event_id','role','endpoint']);oldc=OLD[OLD.scenario.eq('C')].set_index(['event_id','role','endpoint']);ccheck=[];rows=[]
for a in S.itertuples():
 pop=pops[a.event_id];q,price=cache[(a.review,a.ric)];cpop=set(E.loc[E.review.eq(a.review)&E.C,'fund_id'])&pop
 for end,date,fac in [('q0',a.q0,a.factor),('q1',a.q1,1.)]:
  vals=pd.Series({fid:float(q.get((fid,date),0))*fac*price for fid in pop&pilot});assert vals.ge(0).all() and vals.notna().all()
  key=(a.event_id,a.role,end);old=base.loc[key];cnum=float(vals[vals.index.isin(cpop)].sum());ccheck.append(abs(cnum-oldc.loc[key,'covered_SEK_at_q1price'])/max(1.,old.denominator_SEK_at_q1price))
  for sc in scenarios:
   selected=pop&elig[sc].get(a.review,set());num=float(vals[vals.index.isin(selected)].sum())+(float(old.covered_SEK_at_q1price) if sc.endswith('_hybrid') else 0.);den=float(old.denominator_SEK_at_q1price)
   rows.append(dict(event_id=a.event_id,review=a.review,type=a.type,role=a.role,ric=a.ric,endpoint=end,scenario=sc,population_funds=len(pop),eligible_funds=len(selected),coverage_fraction=num/den if den>0 else np.nan,denominator_SEK_at_q1price=den,covered_SEK_at_q1price=num,conditional_NAV='NAV_conditional' in sc,historical_class_universe_fully_certified=False))
D=pd.DataFrame(rows);assert max(ccheck)<1e-12;assert D.groupby(['scenario','event_id']).eligible_funds.nunique().eq(1).all();D.to_csv(O/'D_event_role_endpoint_coverage.csv',index=False)
def summary(d,keys):
 out=[]
 for key,g in d.groupby(keys):
  if not isinstance(key,tuple):key=(key,)
  r=dict(zip(keys,key));r.update(cells=len(g),events=g.event_id.nunique(),missing_cells=int(g.coverage_fraction.isna().sum()),equal_cell_mean_fraction=g.coverage_fraction.mean(),pooled_SEK_coverage_fraction=g.covered_SEK_at_q1price.sum()/g.denominator_SEK_at_q1price.sum(),minimum_fraction=g.coverage_fraction.min())
  for t in [.5,.75,.9]:r['cells_ge_'+str(int(t*100))]=int(g.coverage_fraction.ge(t).sum())
  out.append(r)
 return pd.DataFrame(out)
summary(D,['scenario']).to_csv(O/'D_overall_coverage_summary.csv',index=False);summary(D,['scenario','review','type','role','endpoint']).to_csv(O/'D_review_side_role_endpoint_summary.csv',index=False);summary(D,['scenario','role','endpoint']).to_csv(O/'D_role_endpoint_summary.csv',index=False)
ev=[]
for (sc,eid),g in D.groupby(['scenario','event_id']):
 assert len(g)==8;r=dict(scenario=sc,event_id=eid,review=g.review.iloc[0],type=g.type.iloc[0],missing_cells=int(g.coverage_fraction.isna().sum()),minimum_all8_fraction=g.coverage_fraction.min() if g.coverage_fraction.notna().all() else np.nan)
 for t in [.5,.75,.9]:r['all8_ge_'+str(int(t*100))]=bool(g.coverage_fraction.notna().all() and g.coverage_fraction.ge(t).all())
 ev.append(r)
EV=pd.DataFrame(ev);EV.to_csv(O/'D_event_all8cell_coverage.csv',index=False);EV.groupby(['scenario','review','type']).agg(events=('event_id','size'),all8_ge_50=('all8_ge_50','sum'),all8_ge_75=('all8_ge_75','sum'),all8_ge_90=('all8_ge_90','sum')).reset_index().to_csv(O/'D_review_side_all8_thresholds.csv',index=False)
sourcecounts=E.groupby('review')[scenarios].sum().reset_index();sourcecounts.to_csv(O/'D_source_eligible_funds_by_review.csv',index=False)
check_ABC();v={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ABC_snapshot_unchanged':True,'C_independent_pilot_numerator_error_as_denominator_fraction':max(ccheck),'events':D.event_id.nunique(),'same_fixed_fundpopulation':True,'same_eligible_fundset_all8cells':True,'fixedpopulation_RIPS_pilot_passes':int(E.D_RIPS_pilot.sum()),'fixedpopulation_conditionalNAVinclusive_pilot_passes':int(E.D_NAV_conditional_pilot.sum()),'source_agent_RIPS_passes':int(F.D_RIPS_source_supported.sum()),'source_agent_conditionalNAVinclusive_passes':int(F.D_NAV_conditional_source_supported.sum()),'thresholds_descriptive_not_powerGO':True,'no_returns_flows_covariances_risk_outcomes':True,'all8_threshold_counts':EV.groupby('scenario')[['all8_ge_50','all8_ge_75','all8_ge_90']].sum().to_dict('index')}
(O/'D_COVERAGE_VALIDATION.json').write_text(json.dumps(v,indent=2));print(json.dumps(v,indent=2));print(summary(D,['scenario']).to_string(index=False))
