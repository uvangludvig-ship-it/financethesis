"""Lock a metadata-only source inventory before reading any new auction outcome."""
from pathlib import Path
from datetime import datetime, timezone
import csv,hashlib,json
ROOT=Path('/Users/ludviguvang/dev/financethesis')
OUT=Path(__file__).resolve().parent
FILES={'events':ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',
       'calendar':ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',
       'cancellations':ROOT/'output/omxsb_execution_followup_20261102/sources/known_cancellations.csv'}
with FILES['events'].open() as f:events=list(csv.DictReader(f))
with FILES['calendar'].open() as f:
    calendar=sorted({r['date'] for r in csv.DictReader(f) if r['ric']=='.OMXSBGI'})
with FILES['cancellations'].open() as f:
    cancelled={(r['review'],r['RIC']) for r in csv.DictReader(f)}
positions={d:i for i,d in enumerate(calendar)}
rows=[];excluded=[]
for event in events:
    review=event['review_cycle'];ric=event['RIC'];ed=event['effective_date']
    if not ('2010'<=review<'2024'):continue
    reason=[]
    if '.ST' not in ric:reason.append('no_Stockholm_RIC')
    if ed not in positions or positions.get(ed,0)<6:reason.append('calendar_gap')
    if (review,ric) in cancelled:reason.append('known_cancelled_change')
    if reason:
        excluded.append({'event_id':event['event_id'],'reason':';'.join(reason)});continue
    for role,offset in [('rebalance',1),('comparison',6)]:
        rows.append({k:event[k] for k in ['event_id','review_cycle','RIC','type','company']}|
                    {'date':calendar[positions[ed]-offset],'session_role':role,
                     'announcement_date':event['announcement_date'],'effective_date':ed})
assert len({(r['event_id'],r['session_role']) for r in rows})==len(rows)
with (OUT/'SOURCE_REQUEST_ROWS.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
groups={}
for row in rows:
    key=(row['review_cycle'],row['date'],row['session_role'])
    groups.setdefault(key,[]).append(row['RIC'])
requests=[dict(review=key[0],date=key[1],role=key[2],universe=sorted(set(universe)))
          for key,universe in sorted(groups.items())]
lock={'created_utc':datetime.now(timezone.utc).isoformat(),
      'purpose':'source presence only; no price, volume ratio, return or effect calculation',
      'outcome_fields_opened_for_analysis':[],
      'fields_requested':['CLS_AUC','CLS_AUCVOL','TRDPRC_1'],
      'adjustments':['unadjusted'],'interval':'1D',
      'universe_rule':'All mapped implemented Stockholm OMXSB event candidates 2010 through2023; no price or source-coverage selection.',
      'controls':'This is not the analytical control set. Event-source coverage is checked first; same-day fixed control sources are required before final outcome eligibility.',
      'source_missing_rule':'Missingness is retained and reported by review/type. No replacement security or date.',
      'post2023':'Metadata may be inventoried separately; no outcome retrieval in this script because of FTN holdout rules.',
      'input_sha256':{k:hashlib.sha256(p.read_bytes()).hexdigest()for k,p in FILES.items()},
      'request_rows':len(rows),'events':len({r['event_id']for r in rows}),
      'reviews':len({r['review_cycle']for r in rows}),
      'exclusions':excluded,'requests':requests}
(OUT/'SOURCE_REQUEST_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
print(json.dumps({k:lock[k]for k in ['events','reviews','request_rows']}))
