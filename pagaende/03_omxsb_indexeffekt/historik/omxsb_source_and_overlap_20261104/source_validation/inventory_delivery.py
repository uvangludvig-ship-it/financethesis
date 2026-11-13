"""Read-only SHoF delivery metadata. Never exports quote/transaction values.

The requested identifiers/dates are operator metadata, not inferred from filename.
Gzip, ZIP/CSV and uncompressed CSV supported; actual content drives the inventory.
"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
from decimal import Decimal
import gzip
import hashlib
import io
import json
from pathlib import Path
import zipfile


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--requested-isin', nargs='+', required=True)
    p.add_argument('--date-from', required=True)
    p.add_argument('--date-to', required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    assert not a.out.exists(), 'Never overwrite a frozen inventory'
    blob = a.input.read_bytes()
    if blob[:2] == b'\x1f\x8b':
        compression = 'gzip despite zip suffix'
        members = [(a.input.name, gzip.decompress(blob))]
    elif blob[:2] == b'PK':
        compression = 'ZIP'
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            assert archive.testzip() is None
            members = [(n, archive.read(n)) for n in archive.namelist() if n.lower().endswith('.csv')]
    else:
        compression = 'uncompressed CSV'
        members = [(a.input.name, blob)]
    byday = defaultdict(list)
    schemas = []
    for name, data in members:
        reader = csv.DictReader(io.StringIO(data.decode('utf-8-sig')), delimiter=';')
        columns = reader.fieldnames
        assert {'symbol', 'isin', 'date', 'time', 'status', 'market', 'currency', 'instrumentid'} <= set(columns)
        count = 0
        for row in reader:
            assert None not in row
            byday[tuple(row[c] for c in ['symbol', 'isin', 'date', 'market', 'currency', 'instrumentid'])].append(row)
            count += 1
        schemas.append(dict(member=name, header=columns, rows=count))
    inventory = []
    for key, rows in sorted(byday.items(), key=lambda x: (x[0][1], x[0][2])):
        times = [row['time'] for row in rows]
        inventory.append(dict(zip(['symbol', 'ISIN', 'date', 'market', 'currency', 'instrumentid'], key),
            rows=len(rows), first_time=min(times), last_time=max(times), unique_times=len(set(times)),
            all_exact_minute_labels=all(Decimal(t.split(':')[2]) == 0 for t in times),
            nonmonotonic_time_transitions=sum(b < c for c, b in zip(times, times[1:])),
            status_counts=dict(Counter(row['status'] for row in rows)),
            requested_identifier=key[1] in a.requested_isin,
            within_requested_date_range=a.date_from <= key[2] <= a.date_to))
    result = dict(created_utc=datetime.now(timezone.utc).isoformat(), source_only=True,
        input=str(a.input), bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(), compression=compression,
        requested=dict(ISIN=a.requested_isin, date_from=a.date_from, date_to=a.date_to, setting='Every minute'),
        members=schemas, actual_instrument_days=inventory,
        actual_days_outside_requested_range=sum(not x['within_requested_date_range'] for x in inventory),
        nonrequested_identifiers=sorted({x['ISIN'] for x in inventory if not x['requested_identifier']}),
        no_quote_levels_transactions_returns_or_premiums_exported=True,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['sha256', 'bytes', 'compression', 'actual_days_outside_requested_range', 'nonrequested_identifiers']}))


if __name__ == '__main__':
    main()
