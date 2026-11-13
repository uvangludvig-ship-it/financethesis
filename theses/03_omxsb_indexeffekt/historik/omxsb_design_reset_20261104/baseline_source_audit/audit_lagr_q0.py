"""Source-only LAGR q0 identity/unit audit. Reads no q1/q2 quantities."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json
import pyarrow.dataset as ds

P=Path(__file__).resolve().parent
C=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke')
R=Path('/Users/ludviguvang/dev/financethesis')
G=C/'work/omxsb_scaled_round_20261103/independent_design/retention'
paths={'panel':R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',
 'old_scaling':G/'private/SCALING_INPUTS.csv','old_gate':G/'SECURITY_SOURCE_GATE.csv',
 'source_counts':P/'LAGR_PRIMARY_SOURCE_FACTS.json','code':Path(__file__)}
O=P/'LAGR_Q0_DIAGNOSTIC.json';assert not O.exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
start=datetime.now(timezone.utc).isoformat()
lock={k:{'path':str(p),'sha256':sha(p)} for k,p in paths.items()}
facts=json.loads(paths['source_counts'].read_text())
s=next(r for r in csv.DictReader(paths['old_scaling'].open()) if r['ric']=='LAGRb.ST' and r['review']=='2020H2')
sg=next(r for r in csv.DictReader(paths['old_gate'].open()) if r['ric']=='LAGRb.ST' and r['review']=='2020H2')
assert sg['reason']=='q0_class_capital_fraction_unverified'
dataset=ds.dataset(paths['panel'],format='parquet')
rows=dataset.to_table(columns=['ric','date','close','mcap','shares','source'],
 filter=(ds.field('ric')=='LAGRb.ST')&(ds.field('date')==datetime(2020,9,30))).to_pylist()
assert len(rows)==1 and rows[0]['source']=='tr'
x=rows[0];p0=float(s['q0_price']);m0=float(s['q0_mcap'])
A=facts['presplit_20200930']['class_A_issued']
B=facts['presplit_20200930']['class_B_issued']
T=facts['presplit_20200930']['class_B_treasury']
F=facts['physical_split_factor']
checks={'vendor_shares_over_split_adjusted_B_ex_treasury':x['shares']/(F*(B-T)),
 'adjusted_close_times_split_over_nominal_FI_price':x['close']*F/p0,
 'stored_mcap_over_original_q0_mcap':x['mcap']/m0,
 'stored_mcap_over_nominal_FI_price_times_B_issued':m0/(p0*B),
 'old_class_fraction':float(s['class_fraction_q0']),
 'class_fraction_using_dated_B_issued':B*p0/m0,
 'class_fraction_using_dated_B_ex_treasury':(B-T)*p0/m0,
 'stored_mcap_over_nominal_FI_price_times_AB_issued':m0/(p0*(A+B)),
 'stored_mcap_over_nominal_FI_price_times_AB_ex_treasury':m0/(p0*(A+B-T))}
assert abs(checks['vendor_shares_over_split_adjusted_B_ex_treasury']-1)<1e-10
assert abs(checks['adjusted_close_times_split_over_nominal_FI_price']-1)<2e-6
assert abs(checks['stored_mcap_over_nominal_FI_price_times_B_issued']-1)<1e-10
assert 0<checks['class_fraction_using_dated_B_issued']<=1.03
assert sg['q0_LSEG_close_date']==sg['q0_LSEG_mcap_date']=='2020-09-30'
result={'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),
 'ric':'LAGRb.ST','review':'2020H2','event_id':'OMXSB-2020H2-10','q0':'2020-09-30',
 'no_new_q2_quantities_or_outcomes_read':True,'no_new_q1_capital_weights_or_width_computed':True,
 'diagnostic_split_explanation_verified':True,
 'old_scale_changed':False,'old_q2_support_mask_changed':False,
 'companywide_denominator_semantics_certified':False,
 'status':'SPLIT_DIAGNOSTIC_RESOLVED_BUT_ALL70_PP_OUTCOME_BLOCKED_PENDING_DENOMINATOR_DEFINITION',
 'comparisons':checks,'inputs':lock}
assert all(sha(Path(z['path']))==z['sha256'] for z in lock.values())
O.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
