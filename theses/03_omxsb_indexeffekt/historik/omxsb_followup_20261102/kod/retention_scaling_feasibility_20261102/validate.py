from pathlib import Path
from fractions import Fraction
import csv,json,statistics,hashlib,math
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'additions_20261102'))
from portable_paths import analysis_paths, first_output, comparison_function, repository_source, verify_original_lock
R,O=analysis_paths('retention_scaling_feasibility_20261102')
read=lambda p:list(csv.DictReader(open(p)))
g=read(O/'core_gate_frozen.csv'); f=read(O/'fund_review_factors.csv'); z=read(O/'relative_retention_all.csv'); t=read(first_output(R)/'retention_followup_20261102/position_quantities.csv')
T={(x['event_id'],x['fund_id']):x for x in t}; factors={}; buckets={}
for x in g:
 k=(x['fund_id'],x['review']);buckets.setdefault(k,[]).append(x)
for k,gg in buckets.items():
 assert len(gg)==20 and len({x['company_code'] for x in gg})==20
 good=[x for x in gg if x['gate_pass']=='True']
 assert len(good)>=15
 assert sum(float(x['mv0']) for x in good)/sum(float(x['mv0']) for x in gg)>=.8
 factors[k]=statistics.median([Fraction(x['q1'])/(Fraction(x['q0'])*Fraction(x['splitfactor'])) for x in good])
maxfactor=0
for x in f:
 k=(x['fund_id'],x['review']);maxfactor=max(maxfactor,abs(float(factors[k])-float(x['core_factor'])))
errs=[];maxerr=0;directions=[]
for x in z:
 orig=T[(x['event_id'],x['fund_id'])]
 if Fraction(orig['q_index'])==0:
  assert x['relative_quantity_ratio']=='' and x['relative_direction']=='undefined';continue
 ex=Fraction(orig['q_next'])/(Fraction(orig['q_index'])*Fraction(orig['splitfactor']))/factors[(x['fund_id'],x['review'])]
 maxerr=max(maxerr,abs(float(ex)-float(x['relative_quantity_ratio'])))
 dr='decreased' if ex<1 else 'increased' if ex>1 else 'unchanged'
 if dr!=x['relative_direction']:directions.append(dict(event_id=x['event_id'],fund_id=x['fund_id'],stored=x['relative_direction'],exact=dr,exact_float=float(ex),stored_float=float(x['relative_quantity_ratio'])))
 assert maxerr<1e-12
assert len(z)==238 and len(T)==238
result=dict(target_rows=len(z),fund_review_factors=len(factors),core_rows=len(g),valid_core_rows=sum(x['gate_pass']=='True' for x in g),target_defined=sum(bool(x['relative_quantity_ratio']) for x in z),max_factor_error=maxfactor,max_relative_error=maxerr,exact_direction_mismatches=directions,pvalues_computed=False,new_price_outcomes_computed=False)
# Reproducible metadata-only selection audit and independent issuer exclusion check.
import pandas as pd
# R is the portable repository root defined above.
a=pd.read_csv(O/'baseline_candidate_ledger.csv');c=pd.read_csv(O/'core_frozen.csv');sel=set(zip(c.fund_id,c.review,c['isin']))
a['selected_core']=[(x.fund_id,x.review,x.isin) in sel for x in a.itertuples()]
a['selection_status']=a.baseline_reason.fillna('')
a.loc[a.selected_core,'selection_status']='selected_before_endpoints'
a.loc[a.selection_status.eq(''),'selection_status']='eligible_but_other_class_or_below_fixed_top20'
a.to_csv(O/'baseline_selection_audit.csv',index=False)
E=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv');RO=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv');AL=json.load(open(R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json'))
clash=[]
for rev,cc in c.groupby('review'):
 ids=set(E.loc[E.review_cycle.eq(rev),'isin'].dropna())
 for ric in E.loc[E.review_cycle.eq(rev),'RIC'].dropna():ids.update(AL.get(ric,[]))
 codes=set(RO.loc[RO['isin'].isin(ids),'company_code'].dropna())
 for x in cc[cc.company_code.isin(codes)].itertuples():clash.append(dict(review=rev,isin=x.isin,company=x.company_code))
assert not clash
result['global_dated_identity_issuer_overlap']=clash
result['selection_audit_file']='baseline_selection_audit.csv'
(O/'independent_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
