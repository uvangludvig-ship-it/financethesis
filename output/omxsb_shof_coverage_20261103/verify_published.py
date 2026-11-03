"""Independent standard-library arithmetic checks; no licensed fund series needed.

Run from the published package. Optional --package PATH during staging.
This verifies coverage arithmetic, not source validity or causal identification.
"""
import argparse
import csv
import gzip
import json
import math
from collections import defaultdict
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
P = args.package.resolve()
A = P / 'audit'

def read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12), (a, b)

def mean(xs):
    return math.fsum(xs) / len(xs)

rows = read(A / 'F_event_role_endpoint_coverage.csv')
by_scenario = defaultdict(list)
for r in rows:
    by_scenario[r['scenario']].append(r)
    assert r['old_monthly_provisional_included'] == 'False'
    den, num, share = (float(r[x]) for x in [
        'denominator_SEK_at_q1price', 'covered_SEK_at_q1price', 'coverage_fraction'])
    assert den > 0 and -1e-12 <= num <= den * (1 + 1e-12)
    close(num / den, share)

published = {r['scenario']: r for r in read(A / 'F_overall_coverage_summary.csv')}
checks = {}
for scenario, group in by_scenario.items():
    events = defaultdict(list)
    for r in group:
        events[r['event_id']].append(r)
    assert len(group) == 1080 and len(events) == 135
    for event in events.values():
        assert len(event) == 8
        assert len({(r['role'], r['endpoint']) for r in event}) == 8
        assert len({r['eligible_funds'] for r in event}) == 1
    avg = mean([float(r['coverage_fraction']) for r in group])
    pooled = (math.fsum(float(r['covered_SEK_at_q1price']) for r in group)
              / math.fsum(float(r['denominator_SEK_at_q1price']) for r in group))
    close(avg, float(published[scenario]['equal_cell_mean_fraction']))
    close(pooled, float(published[scenario]['pooled_SEK_coverage_fraction']))
    thresholds = {str(t): sum(all(float(r['coverage_fraction']) >= t for r in e)
                             for e in events.values()) for t in [.5, .75, .9]}
    checks[scenario] = {'mean': avg, 'pooled': pooled, 'all8_thresholds': thresholds}

eligibility = read(A / 'F_fund_review_source_eligibility.csv')
eligible = {scenario: defaultdict(set) for scenario in by_scenario}
for r in eligibility:
    for scenario in eligible:
        if r[scenario] == 'True':
            eligible[scenario][r['review']].add(r['fund_id'])

# Rebuild new-position coverage from the separately published original ledger.
ledger = P.parent / 'omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz'
new = defaultdict(lambda: defaultdict(float))
support = set()
with gzip.open(ledger, 'rt', newline='') as f:
    for r in csv.DictReader(f):
        if r['type'] != 'addition' or r['review'] > '2023H2':
            continue
        key = (r['event_id'], r['review'], r['role'])
        support.add(key)
        if r['component'] == 'new':
            assert float(r['pp']) >= 0
            new[key][r['fund_id']] += float(r['pp'])

published_new = {(r['event_id'], r['review'], r['role'], r['scenario']): r
                 for r in read(A / 'NEW_POSITION_event_role_coverage.csv')
                 if r['role'] != 'control_mean'}
review = defaultdict(list)
for key in support:
    event_id, rev, role = key
    den = math.fsum(new[key].values())
    for scenario in eligible:
        num = math.fsum(v for fid, v in new[key].items() if fid in eligible[scenario][rev])
        row = published_new[(*key, scenario)]
        close(den, float(row['gross_new_pp']))
        close(num, float(row['covered_new_pp']))
        if den > 0:
            close(num / den, float(row['coverage_fraction']))
        else:
            assert row['coverage_fraction'] == ''
        if role == 'event':
            assert den > 0
            review[(scenario, rev)].append((den, num, num / den))

summary = {r['scenario']: r for r in read(A / 'NEW_POSITION_equal_review_summary.csv')
           if r['role'] == 'event'}
new_checks = {}
for scenario in eligible:
    groups = [g for (sc, _), g in review.items() if sc == scenario]
    assert len(groups) == 10 and sum(map(len, groups)) == 70
    den = mean([mean([x[0] for x in g]) for g in groups])
    num = mean([mean([x[1] for x in g]) for g in groups])
    avgshare = mean([mean([x[2] for x in g]) for g in groups])
    close(den, float(summary[scenario]['mean_gross_new_pp_equal_review']))
    close(num, float(summary[scenario]['mean_covered_new_pp_equal_review']))
    close(num / den, float(summary[scenario]['coverage_of_equal_review_gross_new_pp']))
    close(avgshare, float(summary[scenario]['mean_event_coverage_equal_review']))
    new_checks[scenario] = {'gross_new_coverage': num / den, 'mean_event_coverage': avgshare}

print(json.dumps({'verified': True, 'F_capital_coverage': checks,
                  'new_position_coverage': new_checks,
                  'scope': 'Derived arithmetic only; no economic risk outcomes.'}, indent=2))
