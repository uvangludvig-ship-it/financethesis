"""Independent source-only replay. No price/quantity values are emitted.

Reads original private exports but writes only hashes, counts and equality flags.
Auction sources are included only when --include-auction is explicitly supplied.
Uses the Python standard library; no producer audit script is imported or run.
"""
from pathlib import Path
from collections import Counter
import argparse, csv, datetime, gzip, hashlib, io, json, math, zipfile
from decimal import Decimal, InvalidOperation

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
ORIGINAL_REPO = Path('/Users/ludviguvang/dev/financethesis')
MISSING = {'', 'na', 'n/a', 'none', 'null', 'nan'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def infer_repo_root():
    for parent in OUT.parents:
        if (parent / 'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv').is_file():
            return parent
    return ORIGINAL_REPO


def relocated_repo_path(value, repo_root):
    original = Path(value)
    try:
        return repo_root / original.relative_to(ORIGINAL_REPO)
    except ValueError:
        return original


def missing(value):
    return value.strip().lower() in MISSING


def records(path, compressed=False):
    opener = gzip.open if compressed else open
    with opener(path, 'rt', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle, delimiter=';' if compressed else ',')
        rows = list(reader)
        assert all(None not in row and all(v is not None for v in row.values()) for row in rows)
        return reader.fieldnames, rows


def finite_count(rows, col):
    count = zeros = 0
    for row in rows:
        value = row.get(col, '')
        if missing(value):
            continue
        try:
            number = float(value)
        except ValueError:
            continue
        if math.isfinite(number):
            count += 1
            zeros += number == 0
    return {'finite_numeric': count, 'numeric_zero': zeros,
            'missing_tokens': sum(missing(row.get(col, '')) for row in rows),
            'empty_text': sum(row.get(col, '').strip() == '' for row in rows)}


def publication_manifest(directory):
    allow = directory / 'PUBLICATION_ALLOWLIST.txt'
    hashes = directory / 'PUBLICATION_SHA256.json'
    inline_hashes = {}
    if not allow.exists():
        allow = directory / 'PUBLICATION_ALLOWLIST.json'
        hashes = directory / 'FILE_LEDGER.json'
        if not allow.exists():
            return {'status': 'awaiting final allowlist'}
        manifest = json.loads(allow.read_text())
        names = manifest['files']
        assert len(names) == manifest.get('count', len(names))
        inline_hashes = manifest.get('sha256', {})
        if 'pending' in manifest.get('stage', ''):
            return {'status': 'producer manifest explicitly pending; final hash audit deferred',
                    'listed_files': len(names), 'manifest_sha256': sha(allow)}
    else:
        names = [line.strip() for line in allow.read_text().splitlines() if line.strip()]
    assert len(names) == len(set(names))
    for name in names:
        relative = Path(name)
        assert not relative.is_absolute() and '..' not in relative.parts
        assert not set(relative.parts) & {'private', 'sources', '.venv', '__pycache__', 'tmp'}
        assert relative.suffix not in {'.pdf', '.html', '.zip', '.gz', '.png', '.log'}
        assert (directory / relative).is_file()
    expected = json.loads(hashes.read_text()) if hashes.exists() else inline_hashes
    for name, value in expected.items():
        target_hash = value['sha256'] if isinstance(value, dict) else value
        assert sha(directory / name) == target_hash, ('publication hash changed', name)
    return {'status': 'paths checked; contents separately reviewed', 'listed_files': len(names),
            'exact_allowlist_sha256': sha(allow), 'hashes_checked': len(expected),
            'hash_key_set_matches_allowlist': set(expected) == set(names) if expected else None,
            'unhashed_allowed_paths': sorted(set(names) - set(expected)),
            'private_raw_fulltext_log_paths_in_allowlist': False}


def verify_book_metadata(metadata_path, repo_root):
    metadata = json.loads(metadata_path.read_text())
    raw_path = relocated_repo_path(metadata['private_source_path'], repo_root)
    assert sha(raw_path) == metadata['sha256']
    columns, rows = records(raw_path, compressed=True)
    assert len(rows) == metadata['rows']
    assert all(r['isin'] == metadata['expected_isin'] and r['date'] == metadata['expected_date'] for r in rows)
    def valid_quote(row):
        try:
            bid, ask, bidsize, asksize = [Decimal(row[c]) for c in ['bidpx1', 'askpx1', 'bidsz1', 'asksz1']]
            return all(q.is_finite() and q > 0 for q in [bid, ask, bidsize, asksize]) and bid <= ask
        except InvalidOperation:
            return False
    candidates = [r for r in rows if r['time'] < '17:25:00' and valid_quote(r)]
    last = max(r['time'] for r in candidates) if candidates else None
    terminal = [r for r in candidates if r['time'] == last]
    distinct = len({(r['bidpx1'], r['askpx1']) for r in terminal})
    assert last == metadata['candidate_last_pre_17_25_quote_if_export_clock_local']
    assert distinct == metadata['distinct_top_quote_states_at_candidate_time']
    assert len(terminal) == metadata['candidate_last_time_rows']
    assert sum(valid_quote(r) for r in rows) == metadata['rows_with_positive_uncrossed_quote_and_positive_sizes']
    for col in columns:
        assert sum(missing(r[col]) for r in rows) == metadata['missing_by_column'][col]
    return {'source_sha256': sha(raw_path), 'metadata_sha256': sha(metadata_path),
            'rows': len(rows), 'identity_and_missingness_reproduced': True,
            'candidate_time_as_exported': last, 'candidate_time_rows': len(terminal),
            'candidate_distinct_top_quote_states': distinct,
            'rows_from_17_25_exported_clock': sum(r['time'] >= '17:25:00' for r in rows),
            'phase_counts': dict(Counter(r['status'] for r in rows)),
            'midpoints_prices_returns_or_premia_computed': False}


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--include-auction', action='store_true')
    args.add_argument('--repo-root', type=Path, default=infer_repo_root())
    args.add_argument('--output', type=Path, help='New audit JSON path; existing files are never overwritten.')
    opts = args.parse_args()
    repo_root = opts.repo_root.resolve()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output_path = opts.output if opts.output else OUT / ('VERIFICATION_REPLAY_' + stamp + '.json')
    if output_path.exists():
        raise FileExistsError('Choose a new --output path; frozen verification is preserved.')
    result = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'source_only': True, 'economic_outcomes_computed': False,
              'raw_numeric_values_published': False}

    hf = BASE / 'hft_audit'
    input_log = json.loads((hf / 'BILIA_EXPORT_COMPARISON.json').read_text())
    paths = {k: relocated_repo_path(v['path'], repo_root) for k, v in input_log['inputs'].items()}
    for key, path in paths.items():
        assert sha(path) == input_log['inputs'][key]['sha256']
        assert path.read_bytes()[:2] == b'\x1f\x8b'
    full_columns, full = records(paths['full'], compressed=True)
    tx_columns, tx = records(paths['transaction'], compressed=True)
    selected = [row for row in full if not missing(row['txpx']) and not missing(row['txsz'])]
    projected = [tuple(row[col] for col in tx_columns) for row in selected]
    actual = [tuple(row[col] for col in tx_columns) for row in tx]
    assert projected == actual
    assert len(full) == 5483 and len(tx) == len(selected) == 862
    assert set(full_columns) - set(tx_columns) == {'buyer', 'seller'}
    assert set(tx_columns) <= set(full_columns)
    assert len(set(tuple(row[c] for c in full_columns) for row in full)) == len(full)
    assert all(row['date'] == '2019-05-31' and row['isin'] == 'SE0009921588'
               and row['market'] == 'XSTO' and row['currency'] == 'SEK' for row in full)
    assert not any(row['time'] >= '17:25:00' for row in full)
    result['hft'] = {
        'input_sha256': {key: sha(path) for key, path in paths.items()},
        'full_rows': len(full), 'transaction_rows': len(tx),
        'transaction_subset_equal_all_shared_cells_in_order': projected == actual,
        'missing_both_transaction_fields': sum(missing(r['txpx']) and missing(r['txsz']) for r in full),
        'partial_transaction_fields': sum(missing(r['txpx']) != missing(r['txsz']) for r in full),
        'rows_at_or_after_17_25_exported_clock': sum(r['time'] >= '17:25:00' for r in full),
        'status_counts': dict(Counter(r['status'] for r in full)),
        'exact_duplicate_extra_rows': len(full) - len(set(tuple(r[c] for c in full_columns) for r in full)),
        'timestamp_key_duplicate_extra_rows': len(full) - len(set((r['date'], r['time'], r['instrumentid']) for r in full)),
        'timezone_independently_verified': False,
        'auction_semantics_independently_verified': False,
        'reused_tx_tuple_extra_rows_total': len(selected) - len(set(
            tuple(row[c] for c in ['txpx', 'txsz', 'buyer', 'seller']) for row in selected)),
    }

    ix = BASE / 'index_sources'
    raw = ix / 'private'
    index = {}; sets = {}; per_date_hashes = {}
    delivered_hashes = {row['private_file']: row['sha256'] for row in
                       json.loads((ix / 'DESKTOP_REPAIRED_ATTEMPT.json').read_text())['requests']}
    for day, expected in [('20231130', 105), ('20231201', 104)]:
        frames = {}
        for field in range(1, 5):
            path = raw / f'repaired_index_pilot_{day}_field{field}.csv'
            _, frames[field] = records(path)
            per_date_hashes[path.name] = sha(path)
            assert sha(path) == delivered_hashes[path.name]
        ricsets = {f: {r['Constituent RIC'] for r in rows if not missing(r['Constituent RIC'])}
                   for f, rows in frames.items()}
        sets[day] = ricsets[2]
        assert len(ricsets[2]) == expected and ricsets[2] == ricsets[3] == ricsets[4]
        assert len(frames[2]) == expected
        weights = finite_count(frames[2], 'Weight percent')
        shares = finite_count(frames[3], 'Index Shares')
        assert weights['finite_numeric'] == shares['finite_numeric'] == 0
        assert weights['missing_tokens'] == shares['missing_tokens'] == expected
        assert all(missing(r['Date']) for r in frames[4])
        assert ricsets[1] == ricsets[2]
        # The combined name request has one extra row without a valid RIC.
        # It is not an additional identified historical member.
        index[day] = {
            'rows_by_request': {str(f): len(rows) for f, rows in frames.items()},
            'unique_nonmissing_ric_by_request': {str(f): len(s) for f, s in ricsets.items()},
            'name_request_extra_rics_count': len(ricsets[1] - ricsets[2]),
            'names_request_only_rows_count': len(frames[1]) - len(frames[2]),
            'name_rows_without_valid_ric': sum(missing(r['Constituent RIC']) for r in frames[1]),
            'weights_shares_dates_membership_identical': ricsets[2] == ricsets[3] == ricsets[4],
            'weights': weights, 'index_shares': shares,
            'returned_date_nonmissing': sum(not missing(r['Date']) for r in frames[4]),
        }
    _, events = records(repo_root / 'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
    expected_add = {r['RIC'] for r in events if r['review_cycle'] == '2023H2' and r['type'] == 'addition'}
    expected_del = {r['RIC'] for r in events if r['review_cycle'] == '2023H2' and r['type'] == 'deletion'}
    final_events = [r for r in events if r['review_cycle'] == '2023H2']
    assert all('UPDATE 29 Nov 2023' in r['notes'] for r in final_events)
    assert all('JM.ST' in members and 'KARNO.ST' not in members for members in sets.values())
    added = sets['20231201'] - sets['20231130']
    deleted = sets['20231130'] - sets['20231201']
    result['index'] = {'dated_membership': index, 'input_sha256': per_date_hashes,
                       'observed_additions_count': len(added), 'observed_deletions_count': len(deleted),
                       'frozen_release_additions_count': len(expected_add),
                       'frozen_release_deletions_count': len(expected_del),
                       'all_additions_match_frozen_release': added == expected_add,
                       'all_deletions_match_frozen_release': deleted == expected_del,
                       'release_version': 'final implemented list after 2023-11-29 update, not initial 2023-11-23 announcement',
                       'JM_present_on_both_dates': all('JM.ST' in members for members in sets.values()),
                       'KARNO_absent_on_both_dates': all('KARNO.ST' not in members for members in sets.values()),
                       'native_nasdaq_basket_received': False,
                       'quantitative_reweighting_available': False}
    field_log = ix / 'FIELD_CONTROL_RESULTS.json'
    if field_log.exists():
        controls = []
        for request in json.loads(field_log.read_text())['requests']:
            path = raw / request['private_file']
            assert sha(path) == request['raw_sha256']
            _, rows = records(path)
            assert len(rows) == request['rows']
            counts = {c: finite_count(rows, c) for c in ['Weight percent', 'Index Shares']}
            assert all(c['finite_numeric'] == c['numeric_zero'] == 0 for c in counts.values())
            assert all(c['empty_text'] == len(rows) for c in counts.values())
            controls.append({'universe': request['universe'], 'rows': len(rows),
                             'nonmissing_RIC_rows': sum(not missing(r['Constituent RIC']) for r in rows),
                             'counts': counts, 'source_sha256': sha(path)})
        assert len(controls) == 2
        result['index_field_controls'] = {'positive_field_control_obtained': False, 'requests': controls}

    if opts.include_auction:
        auction = BASE / 'auction_source'
        checked = []
        for logname in ['ATTEMPTS.json', 'REMAINING_ATTEMPTS.json', 'MINUTE_2023_ATTEMPTS.json']:
            attempts = json.loads((auction / logname).read_text())
            assert attempts['economic_outcomes_computed'] is False
            for request in attempts['requests']:
                path = auction / 'private' / request['private_file']
                assert sha(path) == request['sha256']
                columns, rows = records(path)
                assert len(rows) == request['rows']
                spec = request.get('request', {
                    'universe': attempts.get('instrument'),
                    'start': request.get('date_requested'),
                    'interval': attempts.get('interval'),
                    'fields': attempts.get('fields', []),
                })
                checks = {c: finite_count(rows, c) for c in spec.get('fields', [])}
                for col, count in request.get('numeric_nonmissing', {}).items():
                    assert finite_count(rows, col)['finite_numeric'] == count
                if rows:
                    assert all(row[columns[0]][:10] == spec['start'][:10] for row in rows)
                item = {'log': logname, 'requested_instrument': spec['universe'],
                        'requested_date': spec['start'], 'interval': spec['interval'],
                        'sha256': sha(path), 'rows': len(rows),
                        'returned_field_columns': [c for c in columns if c],
                        'field_presence': checks,
                        'OFF_CLOSE_column_present': 'OFF_CLOSE' in columns}
                checked.append(item)
        result['auction'] = {'independent_raw_presence_replayed': True, 'requests': checked,
                             'no_prices_volumes_or_returns_reported': True}
        result['book_sources'] = {p.name: verify_book_metadata(p, repo_root) for p in
                                  sorted((BASE / 'hft_audit').glob('*_BOOK_METADATA.json'))}
        nmq = json.loads((hf / 'NMQ_SCHEMA_INVENTORY.json').read_text())
        nmq_path = relocated_repo_path(nmq['path'], repo_root)
        assert sha(nmq_path) == nmq['sha256']
        nmq_checks = []
        with zipfile.ZipFile(nmq_path) as archive:
            assert archive.testzip() is None
            for member in nmq['members']:
                with archive.open(member['member']) as handle:
                    reader = csv.DictReader(io.TextIOWrapper(handle, encoding='utf-8-sig'))
                    count = sum(1 for _ in reader)
                    assert reader.fieldnames == member['columns']
                    assert count == member['row_count']
                    nmq_checks.append({'member': member['member'], 'rows': count,
                                       'schema_matches_inventory': True})
        result['nmq'] = {'source_sha256': sha(nmq_path), 'CRC_pass': True,
                         'numeric_metrics_used': False, 'members': nmq_checks}
    else:
        result['auction'] = {'independent_raw_presence_replayed': False,
                             'status': 'Awaiting root final source handoff; not final-audited.'}
    result['publication'] = {name: publication_manifest(BASE / name)
                             for name in ['index_sources', 'index_sources/timezone_source', 'hft_audit', 'auction_source']}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: result[k] for k in ['source_only', 'economic_outcomes_computed', 'raw_numeric_values_published']}))
    print('HFT: 5483 full rows, 862 shared transaction rows exactly equal. Index: 105 to 104; weights and shares all missing.')
    print('Release membership equality:', added == expected_add, deleted == expected_del)


if __name__ == '__main__':
    main()
