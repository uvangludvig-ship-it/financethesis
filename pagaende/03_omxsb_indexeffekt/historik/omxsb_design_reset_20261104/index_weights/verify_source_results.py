"""Independent CSV/header/presence validation; no API call and no economic data."""
from pathlib import Path
import csv,datetime,hashlib,json
O=Path(__file__).resolve().parent
P=O/'private'
OLD=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/alternative_execution_20261103/index_sources/private')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
R=json.loads((O/'SOURCE_RESULTS.json').read_text())
assert R['actual_data_queries']==4 and R['session_opened'] and R['session_closed']
lock=json.loads((O/'REQUEST_LOCK.json').read_text());assert len(lock['requests'])==4
assert sha(O/'probe_root_chain.py')==lock['code_sha256']
assert sha(O/'SOURCE_SPEC.txt')==lock['spec_sha256']
assert json.loads((O/'PRIOR_REQUEST_BLOCKLIST.json').read_text())['prior_desktop_request_count']==29
current=list(csv.DictReader((OLD/'PI_current_content_control.csv').open()))
cur={x['Constituent RIC'].strip() for x in current if x['Constituent RIC'].strip()}
out=[];target_sets=[]
for rec in R['requests']:
 p=P/rec['private_file'];assert sha(p)==rec['sha256']
 with p.open() as f:
  reader=csv.DictReader(f);assert reader.fieldnames==['Instrument','Date','Weight percent','Index Shares'];rows=list(reader)
 assert len(rows)==rec['rows']
 for k in ['Date','Weight percent','Index Shares']:
  assert all(not x[k].strip() for x in rows),(rec['label'],k)
 ids={x['Instrument'].strip() for x in rows if x['Instrument'].strip()}
 item={'label':rec['label'],'rows':len(rows),'all_weight_share_date_cells_blank':True,'no_numeric_zero_imputation':True}
 if rec['universe']=='0#.OMXSBPI':
  target_sets.append(ids)
  d=rec['requested_date'];refpath=OLD/f'repaired_index_pilot_{d.replace("-", "")}_field1.csv'
  with refpath.open() as f:rr=list(csv.DictReader(f))
  ref={x['Constituent RIC'].strip()for x in rr if x['Constituent RIC'].strip()}
  cmp=rec['historical_member_alignment']
  assert len(ref)==cmp['reference_members'] and len(ids)==cmp['returned_unique_instruments']
  assert len(ref-ids)==cmp['reference_missing'] and len(ids-ref)==cmp['extra_returned']
  item.update(exact_previous_current_member_set_match=ids==cur,previous_current_members=len(cur),historical_reference_match=ids==ref,missing_historical_members=len(ref-ids),extra_members=len(ids-ref))
 out.append(item)
assert target_sets[0]==target_sets[1]
v={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_responses_checked':4,'private_rows_checked':sum(x['rows']for x in out),'all_numeric_weight_share_and_date_fields_empty':True,'valid_historical_official_weight_baskets':0,'target_returned_same_members_both_dates':True,'only_source_metadata_computed':True,'checks':out,'source_results_sha256':sha(O/'SOURCE_RESULTS.json'),'old_current_reference_sha256':sha(OLD/'PI_current_content_control.csv')}
(O/'VALIDATION.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v,indent=2))
