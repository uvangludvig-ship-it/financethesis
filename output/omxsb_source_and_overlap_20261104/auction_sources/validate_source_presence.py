"""Independent CSV-string presence audit; no new request or outcome calculation."""
from pathlib import Path
import csv, datetime, decimal, hashlib, json
P=Path(__file__).resolve().parent
attempt=json.loads((P/'SOURCE_PILOT_RESULT.json').read_text())
out=[]
for a in attempt['requests']:
    f=P/'private'/a['private_file']
    assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256']
    with f.open(newline='') as stream: rows=list(csv.DictReader(stream))
    valid=[]
    date=[]
    for row in rows:
        value=row.get('Closing Auction Volume','').strip()
        try: finite=bool(value) and decimal.Decimal(value).is_finite()
        except decimal.InvalidOperation: finite=False
        d=row.get('Date','').strip()
        exact_date=bool(d) and d[:10]==a['request']['parameters']['SDate']
        valid.append(bool(finite and exact_date))
        date.append(d)
    out.append({'instrument':a['request']['universe'][0], 'requested_date':a['request']['parameters']['SDate'],
                'response_rows':len(rows),'raw_sha256':a['sha256'],'date_present':any(date),
                'returned_dates':sorted(set(x for x in date if x)),
                'dated_finite_auction_volume_rows':sum(valid),'closing_auction_price_requested':False,
                'new_historical_price_coverage':False})
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'requests':out,'economic_outcomes_computed':False,
        'QA_correction':'Original diagnostic cast the Date column to numeric and classified NaT as finite. That irrelevant date-numeric count is invalid; source presence here uses CSV strings and only the auction-volume column. Original request log is preserved; no request was repeated.',
        'original_probe_sha256':hashlib.sha256((P/'private/probe_as_executed.py').read_bytes()).hexdigest()}
(P/'VALIDATED_SOURCE_PRESENCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
