"""Read-only audit of seven frozen SHoF pilot originals. No returns or price sums.

Only schema, identity, timestamp, record counts, hashes and equality proof export.
Prices, quantities and participant identifiers never appear in public output.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import zipfile

NAMES = [
 'NASDAQ_2nd_level_orderbook_1793732319625.csv.zip',
 'NASDAQ_2nd_level_orderbook_1793732601269.csv.zip',
 'NASDAQ_2nd_level_orderbook_1793733524718.csv.zip',
 'NASDAQ_2nd_level_orderbook_1793733549086.csv.zip',
 'NASDAQ_2nd_level_orderbook_1793733618890.csv.zip',
 'NASDAQ_2nd_level_orderbook_1793733672616.csv.zip',
 'NASDAQ_micromeasures_1793733197232.zip']
MISSING = {'','n/a','na','null','none','nan'}


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def missing(value):
    return value.strip().lower() in MISSING


def read_csv(blob, separator):
    text = blob.decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text), delimiter=separator)
    rows = list(reader)
    assert reader.fieldnames and len(set(reader.fieldnames)) == len(reader.fieldnames)
    assert all(None not in r for r in rows)
    return reader.fieldnames, rows


def canonical_hash(rows, columns):
    # One-way equality fingerprint; never exports the original numeric cells.
    h=hashlib.sha256()
    for row in rows:
        h.update(json.dumps([row[c] for c in columns], separators=(',',':'), ensure_ascii=False).encode())
        h.update(b'\n')
    return h.hexdigest()


def book_metadata(columns, rows):
    tx=lambda r:not missing(r['txpx']) and not missing(r['txsz'])
    identity={c:sorted({r[c] for r in rows}) for c in ['symbol','isin','date','market','currency','instrumentid']}
    assert all(len(v)==1 for v in identity.values())
    status=[]
    for code in sorted({r['status'] for r in rows}):
        subset=[r for r in rows if r['status']==code]
        status.append(dict(code=code, rows=len(subset), first_time=min(r['time'] for r in subset),
            last_time=max(r['time'] for r in subset), transaction_field_rows=sum(tx(r) for r in subset)))
    times=[r['time'] for r in rows]
    txrows=[r for r in rows if tx(r)]
    tuple_cols=['date','time','instrumentid','txpx','txsz']
    txkeys=[tuple(r[c] for c in tuple_cols) for r in txrows]
    return dict(identity=identity,columns=columns,rows=len(rows),
        first_time=min(times),last_time=max(times), first_file_time=times[0],last_file_time=times[-1],
        nonmonotonic_transitions=sum(b<a for a,b in zip(times,times[1:])),
        exact_duplicate_extra_rows=len(rows)-len({tuple(r[c] for c in columns) for r in rows}),
        timestamp_instrument_duplicate_extra_rows=len(rows)-len({(r['date'],r['time'],r['instrumentid']) for r in rows}),
        missing_by_column={c:sum(missing(r[c]) for r in rows) for c in columns},
        transaction_field_rows=len(txrows), transaction_first_time=min(r['time'] for r in txrows) if txrows else None,
        transaction_last_time=max(r['time'] for r in txrows) if txrows else None,
        same_timestamp_tx_key_extra_rows=len(txkeys)-len(set(txkeys)),
        same_timestamp_tx_key_fields=tuple_cols,
        prior_audit_tx_tuple_fields=['txpx','txsz','buyer','seller'] if 'buyer' in columns else None,
        prior_audit_tx_tuple_extra_rows_total=(len(txrows)-len({tuple(r[c] for c in ['txpx','txsz','buyer','seller']) for r in txrows})) if 'buyer' in columns else None,
        status_coverage=status,
        rows_at_or_after_17_25_as_exported=sum(r['time']>='17:25:00' for r in rows),
        rows_at_or_after_17_29_30_as_exported=sum(r['time']>='17:29:30' for r in rows),
        closing_status_L_rows=sum(r['status']=='L' for r in rows),
        closing_cross_status_third_C_rows=sum(len(r['status'])==3 and r['status'][2]=='C' for r in rows),
        match_number_present=any('match' in c.lower() for c in columns),
        raw_message_type_present=any(c.lower()=='type' for c in columns),
        timezone='No timezone field in file. Displayed-clock metadata only; prior local-clock conclusion was documented phase inference.',
        no_price_volume_return_computation=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=Path('/Users/ludviguvang/dev/financethesis'))
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    assert not args.output.exists(),'Choose fresh output directory; keep source audit frozen'
    args.output.mkdir(parents=True)
    raw=args.repo_root/'data/raw/shof/Reinvestments/hft_pilot_20261103'
    paths=[raw/n for n in NAMES]
    initial={n:digest(p.read_bytes()) for n,p in zip(NAMES,paths)}
    (args.output/'INPUT_LOCK.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),
        scope='Seven pre-existing originals; fixed Bilia2019 and Camurus/AFRY2023 pilot identities; source only',
        originals=initial,script_sha256=digest(Path(__file__).read_bytes()),economic_outcomes=False),indent=2)+'\n')
    files=[];books={}
    for path in paths:
        blob=path.read_bytes()
        meta=dict(file=path.name,bytes=len(blob),sha256=digest(blob))
        if blob[:2]==b'\x1f\x8b':
            decompressed=gzip.decompress(blob)  # validates gzip CRC as well as decoding
            columns,rows=read_csv(decompressed,';')
            meta.update(compression='gzip, despite .zip suffix',uncompressed_bytes=len(decompressed),
                integrity_check='gzip decompression/CRC succeeded',product_schema='reconstructed orderbook',
                metadata=book_metadata(columns,rows))
            books[path.name]=(columns,rows)
        else:
            with zipfile.ZipFile(io.BytesIO(blob)) as archive:
                assert archive.testzip() is None
                members=[]
                for name in archive.namelist():
                    columns,rows=read_csv(archive.read(name),',')
                    assert 'Stock' in columns and 'Date' in columns
                    members.append(dict(member=name,uncompressed_bytes=archive.getinfo(name).file_size,
                        rows=len(rows),columns=columns,keys=[{k:r[k] for k in ['Stock','Date']} for r in rows],
                        intraday_timestamp_column_present=any(c.lower() in {'time','timestamp'} for c in columns),
                        explicitly_named_auction_field_present=any('auction' in c.lower() or 'cross' in c.lower() for c in columns)))
                meta.update(compression='ZIP',integrity_check='all ZIP CRCs succeeded',product_schema='daily micro-measure summaries',members=members)
        files.append(meta)
    fullcols,full=books[NAMES[0]];txcols,transactions=books[NAMES[1]]
    selected=[r for r in full if not missing(r['txpx']) and not missing(r['txsz'])]
    removed=[c for c in fullcols if c not in txcols]
    assert [c for c in fullcols if c not in removed]==txcols
    cells=sum(a[c]!=b[c] for a,b in zip(selected,transactions) for c in txcols)
    equal=len(selected)==len(transactions) and cells==0
    comparison=dict(full=NAMES[0],transactions=NAMES[1],full_rows=len(full),full_transaction_field_rows=len(selected),
        transaction_file_rows=len(transactions),shared_columns=len(txcols),removed_columns=removed,
        same_row_order_and_all_shared_cells=equal,different_shared_cells=cells,
        full_filtered_canonical_sha256=canonical_hash(selected,txcols),transaction_canonical_sha256=canonical_hash(transactions,txcols),
        implication='This Bilia instrument-day Transactions export is a strict row/column projection of Full Reconstruction; no additional late-session records.',
        scope_limit='Proves only this pair. Does not prove universal SHoF auction omission, one row per economic match, or buyer/seller matching legs.')
    assert equal and len(selected)==862
    final={n:digest(p.read_bytes()) for n,p in zip(NAMES,paths)}
    assert initial==final
    output=dict(created_utc=datetime.now(timezone.utc).isoformat(),source_only=True,files=files,
        bilia_pair_proof=comparison,all_original_hashes_unchanged=True,
        product_coverage=dict(full_reconstruction_instrument_days=5,transactions_instrument_days=1,
            trade_ticker_exports=0,order_book_view_exports=0,raw_full_day_timeserie_exports=0,
            minute_timeserie_exports=0,daily_micro_measure_archives=1),
        limitation='Inventory covers only the seven explicit original archives, not unacquired products or future new downloads.')
    (args.output/'RAW_INVENTORY.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    with (args.output/'BOOK_COVERAGE.csv').open('w',newline='') as handle:
        names=['file','symbol','isin','date','market','currency','rows','transaction_field_rows','first_time','last_time','transaction_last_time','rows_at_or_after_17_25_as_exported','closing_status_L_rows','closing_cross_status_third_C_rows']
        writer=csv.DictWriter(handle,fieldnames=names);writer.writeheader()
        for f in files:
            if 'metadata' not in f:continue
            m=f['metadata'];row={'file':f['file']}
            row.update({c:m['identity'][c][0] for c in ['symbol','isin','date','market','currency']})
            row.update({c:m[c] for c in names if c not in row})
            writer.writerow(row)
    (args.output/'BILIA_PAIR_PROOF.json').write_text(json.dumps(comparison,indent=2)+'\n')
    print(json.dumps({'archives':len(files),'book_rows':sum(f.get('metadata',{}).get('rows',0) for f in files),
        'all_original_hashes_unchanged':True,'bilia_pair_equal':equal,'shared_cells_compared':len(selected)*len(txcols)},indent=2))


if __name__=='__main__':main()
