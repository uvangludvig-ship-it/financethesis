"""Read published source-support flags only; never reads NAV/TNA/return values."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib
P=Path(__file__).resolve().parent
R=Path('/Users/ludviguvang/dev/financethesis')
f=R/'output/omxsb_shof_coverage_20261103/audit/F_fund_review_source_eligibility.csv'
O=P/'TRACKER_SOURCE_SUPPORT.json';assert not O.exists()
with f.open() as stream:r=[x for x in csv.DictReader(stream) if x['fund_id'] in ('60293','60320')]
out=[]
for fid in ['60320','60293']:
 z=[x for x in r if x['fund_id']==fid]
 out.append({'fund_id':fid,'fundids':sorted({x['fundid'] for x in z}),
 'rows_present':len(z),'reviews_present':[x['review'] for x in z],
 'stable_exact_map_rows':sum(x['exact_stable_endpoint_map']=='True' for x in z),
 'rows_with_positive_month_count':sum(int(x['month_count'])>0 for x in z),
 'raw_batch_rows':sum(x['is_raw_batch']=='True' for x in z),
 'F_RIPS_pass_rows':sum(x['F_RIPS_allraw']=='True' for x in z),
 'F_NAV_conditional_pass_rows':sum(x['F_NAV_conditional_allraw']=='True' for x in z)})
result={'at_utc':datetime.now(timezone.utc).isoformat(),'trackers':out,
 'source_presence_only':True,'new_flows_returns_covariances_holdings_changes_computed':False,
 'limitation':'These flags describe the previous coverage study and its population. They do not establish absence from every SHoF product or exhaust newly possible direct requests.',
 'input':{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()},
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
assert len(r)==18
O.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
