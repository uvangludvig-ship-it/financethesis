"""Validate source-presence pilot using already saved membership controls only."""
from pathlib import Path
import csv,hashlib,json
O=Path(__file__).resolve().parent
OLD=O.parents[1]/'alternative_execution_20261103/index_sources/private'
paths={'old_20231130':OLD/'repaired_index_pilot_20231130_field1.csv',
       'old_20231201':OLD/'repaired_index_pilot_20231201_field1.csv',
       'previously_pulled_current':OLD/'PI_current_content_control.csv',
       'new_20231130_PI':O/'private/request_07.csv',
       'new_20231130_GI':O/'private/request_08.csv'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def members(p):
    with p.open() as f:return {r['Constituent RIC'].strip() for r in csv.DictReader(f)
                              if r.get('Constituent RIC','').strip()}
sets={k:members(p) for k,p in paths.items()}
r=json.loads((O/'PILOT_RESULTS.json').read_text())
assert len(r['requests'])==8
assert all(q['status']=='response' for q in r['requests'])
assert all(q['unique_member_RICs']==0 for q in r['requests'][:6])
assert sets['new_20231130_PI']==sets['old_20231130']==sets['new_20231130_GI']
assert sets['new_20231130_PI']!=sets['previously_pulled_current']
report={'status':'PASS_SOURCE_PILOT_QA_NOT_HISTORICAL_SAMPLE_CLEARANCE',
 'actual_requests':8,'economic_outcomes_computed':False,
 'historical_empty_response_count':6,'historical_API_error_count':0,
 'empty_response_meaning':'Instrument stub with blank constituent fields, not an index with zero members.',
 'payload_contains_returned_asof_date':False,
 'dates_are_request_parameters_not_vendor_echoed_dates':True,
 'new_positive_control_matches_previous_20231130_exactly':True,
 'new_positive_control_PI_GI_equal':True,
 'new_positive_control_differs_from_previously_pulled_current':True,
 'control_counts':{k:len(v) for k,v in sets.items()},
 'control_symdiff_vs_previously_pulled_current':len(sets['new_20231130_PI']^sets['previously_pulled_current']),
 'old_control_adjacent_day_adds':len(sets['old_20231201']-sets['old_20231130']),
 'old_control_adjacent_day_deletes':len(sets['old_20231130']-sets['old_20231201']),
 'date_validation_limit':'2023 control has prior independent release/set validation; no pre-2007 basket was returned or validated.',
 'historical_name_labels_not_proved_point_in_time':True,
 'raw_publication':False,'SDK_session_closed':r['local_library_session_closed'],
 'input_hashes':{k:{'path':str(p),'sha256':sha(p)}for k,p in paths.items()}}
(O/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='input_hashes'},indent=2))
