"""Date/identifier-only FTN screening. Does not clear outcome access.

No returns, prices, holdings, flows, or flow magnitudes are inspected/computed.
The compound big_days cell is projected to its date prefix only; existing
detector-selected dates are NOT assumed to be a complete order calendar.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import re

ROOT = Path('/Users/ludviguvang/dev/financethesis')
OUT = Path(__file__).resolve().parent
FILES = {
    'index_events': ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',
    'trading_dates': ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',
    'ftn_bids': ROOT/'data/derived/ftn/bids_long.csv',
    'ftn_detected_dates': ROOT/'data/derived/exit_days/exit_days_by_loser.csv',
    'ftn_membership': ROOT/'data/derived/measurements/agentA_task1_round_membership.csv',
    'design': ROOT/'thesis/design/03_DATA.md',
    'detector_code': ROOT/'code/build/detect_exit_days.py',
    'plan': ROOT/'PLAN.md',
}
SELECT = {
    'index_events': ['review_cycle','effective_date'],
    'trading_dates': ['ric','date'],
    'ftn_bids': ['round','announce_date','bid_deadline','award_date'],
    'ftn_detected_dates': ['round','fondnr','award','last_obs','avslutsdatum','big_days'],
    'ftn_membership': ['round','fondnr','role','award','avslutsdatum'],
}
headers = {}
def project(key):
    with FILES[key].open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers[key] = reader.fieldnames
        assert set(SELECT[key]).issubset(reader.fieldnames)
        for row in reader:
            yield {k: row[k] for k in SELECT[key]}

calendar = sorted({r['date'] for r in project('trading_dates') if r['ric']=='.OMXSBGI'})
positions = {d:i for i,d in enumerate(calendar)}
reviews = sorted({(r['review_cycle'],r['effective_date']) for r in project('index_events')
                  if '2024' <= r['review_cycle'] < '2027'})
bid_dates = list(project('ftn_bids'))
awards = {(r['round'],r['award_date']) for r in bid_dates if r['award_date']}
detected_rows = list(project('ftn_detected_dates'))
detected = set()
for row in detected_rows:
    for entry in row['big_days'].split(';'):
        date = entry.partition(':')[0]
        if date:
            assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', date), 'Unexpected date syntax'
            detected.add((row['round'],row['fondnr'],date))
    del row['big_days']
members = [r for r in project('ftn_membership') if r['role']=='loser']
member_ids = {(r['round'],r['fondnr']) for r in members}
detector_ids = {(r['round'],r['fondnr']) for r in detected_rows}
closing = {(r['round'],r['fondnr'],r['avslutsdatum']) for r in members if r['avslutsdatum']}
compared = []
for review,ed in reviews:
    for role,offset in [('ED-1',1),('ED-6',6)]:
        d = calendar[positions[ed]-offset] if ed in positions and positions[ed]>=offset else None
        compared.append({'review':review,'effective_date':ed,'relative_trading_day':role,'date':d,
          'award_rounds_on_date':sorted(r for r,date in awards if date==d),
          'detected_loser_fund_days_on_date':sum(date==d for _,_,date in detected),
          'registered_fund_closures_on_date':sum(date==d for _,_,date in closing),
          'clearance':'NOT_CLEARED_INCOMPLETE_TRANCHE_CALENDAR'})
result = {
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Metadata-only; existing date prefixes and identifiers. No new source retrieval.',
 'status':'NO_COMPLETE_FTN_NONOVERLAP_CERTIFICATION',
 'columns_projected':SELECT,
 'headers_inspected':headers,
 'index_reviews_present':len(reviews),
 'index_reviews_absent':['2026H2'] if not any(r=='2026H2' for r,_ in reviews) else [],
 'calendar_date_min':min(calendar),'calendar_date_max':max(calendar),
 'bid_award_rounds':len(awards),
 'loser_membership_rows':len(members),'loser_membership_unique_round_funds':len(member_ids),
 'detector_rows':len(detected_rows),'detector_unique_round_funds':len(detector_ids),
 'membership_round_funds_absent_from_detector':len(member_ids-detector_ids),
 'detector_latest_observation_date':max(r['last_obs'] for r in detected_rows),
 'detector_rounds':sorted({r['round'] for r in detected_rows}),
 'detector_selected_unique_fund_days':len(detected),
 'comparisons':compared,
 'limitations':[
  'The detector dates flag existing <=-5 percent estimated flows OR units changes; not an official transaction calendar.',
  '03_DATA section C explicitly documents monthly-only observations and missing exact tranche dates for multiple funds.',
  'Absence of detector flags, awards or registered closure dates is not proof of absence of FTN trading.',
  'No per-instrument FTN holdings or sale exposure was inspected; fund-level dates do not establish stock-level overlap.',
  '03_DATA section D documents a 2026-09-30 data endpoint and later small-cap execution.',
  'Only exact dates were compared. This is not clearance of any wider FTN outcome window.',
  'Pre-2024 restriction is a conservative operational rule, not a blanket PLAN ban on all 2024+ quotes.',
 ],
 'input_sha256':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in FILES.items()},
}
(OUT/'FTN_CALENDAR_METADATA_AUDIT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:result[k] for k in ['status','index_reviews_present','bid_award_rounds',
 'loser_membership_unique_round_funds','detector_unique_round_funds',
 'membership_round_funds_absent_from_detector','detector_latest_observation_date','comparisons']},indent=2))
