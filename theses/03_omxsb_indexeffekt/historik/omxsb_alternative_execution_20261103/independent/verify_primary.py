"""Independent Decimal replay of the frozen individual auction contrasts.

Run only after the producer's source gate and first calculation exist. Reads
licensed private sources; emits only source hashes, gate flags and arithmetic
differences against permitted derived AP/contrast values. No raw price, size,
midpoint or participant record is exported. No alternative estimator or mean.
"""
from pathlib import Path
from decimal import Decimal, InvalidOperation, getcontext
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import argparse, json
from verify import BASE, OUT, records, sha, infer_repo_root, relocated_repo_path

getcontext().prec = 40
NS = 10**9
OPEN = 9 * 3600 * NS
PREOPEN = (8 * 3600 + 45 * 60) * NS
CUT = (17 * 3600 + 25 * 60) * NS
TOP = ['bidpx1', 'askpx1', 'bidsz1', 'asksz1']
AMENDMENT_SHA = 'd53064d43a6e90265f00369236d1d75a172411ec118e0bdc1dd206c8745c207e'


def ns(value):
    h, m, s = value.split(':')
    return (int(h) * 3600 + int(m) * 60) * NS + int(Decimal(s) * NS)


def mapped_lock_path(value, repo_root):
    path = relocated_repo_path(value, repo_root)
    if path != Path(value):
        return path
    parts = Path(value).parts
    for marker in ['hft_audit', 'auction_source']:
        if marker in parts:
            return BASE.joinpath(*parts[parts.index(marker):])
    return path


def phase_check(rows, offset_seconds):
    ts = [(ns(r['time']) + offset_seconds * NS, r['status']) for r in rows]
    cont = [t for t, status in ts if status == 'T']
    opening = [t for t, status in ts if status == 'IOO']
    bad_t = sum(not OPEN <= t < CUT for t in cont)
    bad_i = sum(not PREOPEN <= t <= OPEN + 5 * NS for t in opening)
    transition = bool(cont and opening and OPEN <= max(opening) <= OPEN + 5 * NS and min(cont) > max(opening))
    return {'T_outside_regular_continuous_session': bad_t,
            'IOO_outside_opening_window': bad_i,
            'documented_opening_transition_conforms': transition,
            'passes': bool(cont and opening and not bad_t and not bad_i and transition)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', type=Path, default=infer_repo_root())
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    dest = args.output or OUT / ('PRIMARY_REPLAY_' + stamp + '.json')
    if dest.exists():
        raise FileExistsError('Choose a new output; frozen audit is preserved.')
    repo_root = args.repo_root.resolve()
    hft = BASE / 'hft_audit'
    auction = BASE / 'auction_source'
    amendment = auction / 'CLOCK_METHOD_AMENDMENT.json'
    assert sha(amendment) == AMENDMENT_SHA
    lock = json.loads((hft / 'FINAL_EXECUTION_LOCK.json').read_text())
    for value, metadata in lock['inputs'].items():
        path = mapped_lock_path(value, repo_root)
        assert sha(path) == metadata['sha256'], ('locked file changed', path.name)
    summary = json.loads((hft / 'FINAL_SOURCE_GATE_SUMMARY.json').read_text())
    assert summary['passed_events'] == 2 and summary['original_events'] == 4
    assert summary['no_two_event_mean'] and summary['2019_missing_retained']
    clock = json.loads((hft / 'CLOCK_VALIDATION.json').read_text())
    assert clock['primary_metadata_gate_all_four_pass']
    result_path = hft / 'INDIVIDUAL_AUCTION_CONTRASTS.csv'
    assert sha(result_path) == summary['result_sha256']
    assert json.loads(amendment.read_text())['locked_utc'] < summary['created_utc']
    _, events = records(hft / 'PILOT_EVENTS.csv')
    _, reported = records(result_path)
    reports = {r['event_id']: r for r in reported}
    assert set(reports) == {e['event_id'] for e in events}
    source_requests = json.loads((auction / 'REMAINING_ATTEMPTS.json').read_text())['requests']
    request_by_key = {(r['request']['universe'], r['request']['start']): r for r in source_requests
                      if r['request']['interval'] == '1D'}
    aps = {}; day_checks = []
    for metadata_path in sorted(hft.glob('*_2023*_BOOK_METADATA.json')):
        metadata = json.loads(metadata_path.read_text())
        raw_path = relocated_repo_path(metadata['private_source_path'], repo_root)
        assert sha(raw_path) == metadata['sha256']
        _, rows = records(raw_path, compressed=True)
        date = metadata['expected_date']
        event = next(e for e in events if e['ISIN'] == metadata['expected_isin'])
        ric = event['RIC']
        assert date in [event['comparison_date'], event['auction_date']]
        expected = {'date': date, 'isin': event['ISIN'], 'symbol': event['ticker'], 'market': 'XSTO', 'currency': 'SEK'}
        assert all(all(r[k] == v for k, v in expected.items()) for r in rows)
        times = [ns(r['time']) for r in rows]
        assert all(a <= b for a, b in zip(times, times[1:]))
        offset = int(datetime.fromisoformat(date + 'T12:00:00').replace(tzinfo=timezone.utc)
                     .astimezone(ZoneInfo('Europe/Stockholm')).utcoffset().total_seconds())
        local = phase_check(rows, 0)
        utc = phase_check(rows, offset)
        assert local['passes'] and not utc['passes']
        producer_clock = next(c for c in clock['checks'] if c['RIC'] == ric and c['date'] == date)
        for candidate, own in [('exchange_local', local), ('UTC', utc)]:
            producer = next(c for c in producer_clock['clock_candidates'] if c['candidate'] == candidate)
            assert all(producer[k] == v for k, v in own.items())
        quotes = []
        for time_ns, row in zip(times, rows):
            if row['status'] != 'T' or not CUT - 60 * NS <= time_ns < CUT:
                continue
            try:
                q = tuple(Decimal(row[k]) for k in TOP)
                valid = all(v.is_finite() and v > 0 for v in q) and q[0] <= q[1]
            except InvalidOperation:
                valid = False
            if valid:
                quotes.append((time_ns, q))
        assert quotes
        final_ns = max(t for t, _ in quotes)
        states = {q for t, q in quotes if t == final_ns}
        assert len(states) == 1
        bid, ask, _, _ = states.pop()
        request = request_by_key[(ric, date)]
        assert request['request']['adjustments'] == ['unadjusted']
        raw_auction = auction / 'private' / request['private_file']
        assert sha(raw_auction) == request['sha256']
        columns, auction_rows = records(raw_auction)
        assert len(auction_rows) == 1 and auction_rows[0][columns[0]][:10] == date
        price = Decimal(auction_rows[0]['CLS_AUC'])
        volume_confirmation = Decimal(auction_rows[0]['CLS_AUCVOL'])
        assert price.is_finite() and price > 0 and volume_confirmation.is_finite() and volume_confirmation > 0
        midpoint = (bid + ask) / 2
        ap = Decimal(10000) * (price / midpoint - 1)
        aps[(ric, date)] = ap
        column = 'AP_comparison_bp' if date == event['comparison_date'] else 'AP_rebalance_bp'
        difference = abs(ap - Decimal(reports[event['event_id']][column]))
        assert difference < Decimal('0.00000001')
        day_checks.append({'RIC': ric, 'date': date, 'book_sha256': sha(raw_path),
                           'auction_sha256': sha(raw_auction), 'gate_reproduced': True,
                           'source_clock_candidates_reproduced': True,
                           'AP_absolute_difference_bp': float(difference)})
    assert len(aps) == 4
    contrasts = []
    for event in events:
        report = reports[event['event_id']]
        if event['review'] == '2019H1':
            assert report['source_gate_pass'] == 'False'
            assert all(report[c] == 'NA' for c in ['AP_comparison_bp', 'AP_rebalance_bp', 'signed_contrast_bp'])
            continue
        value = int(event['direction']) * (aps[(event['RIC'], event['auction_date'])] - aps[(event['RIC'], event['comparison_date'])])
        difference = abs(value - Decimal(report['signed_contrast_bp']))
        assert difference < Decimal('0.00000001')
        contrasts.append({'event_id': event['event_id'], 'RIC': event['RIC'],
                          'sign_and_subtraction_reproduced': True,
                          'contrast_absolute_difference_bp': float(difference)})
    result = {'created_utc': datetime.now(timezone.utc).isoformat(),
              'independent_decimal_reconstruction': True,
              'producer_calculation_imported_or_executed': False,
              'same_locked_estimand_only': True,
              'raw_prices_midpoints_sizes_or_participants_published': False,
              'source_gate_and_day_checks': day_checks, 'contrast_checks': contrasts,
              'all_four_original_events_retained': True, 'two_2019_rows_remain_NA': True,
              'no_two_event_mean_or_other_estimator': True,
              'clock_amendment_sha256': sha(amendment), 'execution_lock_sha256': sha(hft / 'FINAL_EXECUTION_LOCK.json'),
              'derived_result_sha256': sha(result_path),
              'arithmetic_tolerance_bp': 1e-8,
              'limitation': 'Arithmetic and recorded source rules pass; inferred local clock is not an explicit vendor timezone declaration. Two 2023 cases are not causal or population evidence.'}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: four daily AP values and two signed contrasts independently reproduced; two 2019 NA rows retained.')
    print('Largest absolute arithmetic difference (bp):', max(float(r['AP_absolute_difference_bp']) for r in day_checks))


if __name__ == '__main__':
    main()
