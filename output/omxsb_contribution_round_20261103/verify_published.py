"""Standard-library replay of published normalized contributions, not raw data validation."""
from pathlib import Path
from collections import defaultdict
import csv
import gzip
import hashlib
import json
import math
import statistics

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'PUBLICATION_MANIFEST.json').read_text())
for item in manifest['files']:
    assert hashlib.sha256((ROOT / item['file']).read_bytes()).hexdigest() == item['sha256'], item['file']
for path in ROOT.rglob('*.py'):
    compile(path.read_text(), str(path), 'exec')

sums = defaultdict(float)
funds = defaultdict(set)
seen = set()
meta = {}
group_totals = defaultdict(float)
group_counts = defaultdict(float)
rows = 0
with gzip.open(ROOT / 'ownership_capital/normalized_fund_role_contributions.csv.gz', 'rt') as f:
    for x in csv.DictReader(f):
        eid, role, fund = x['event_id'], x['role'], x['fund_id']
        assert (eid, role, fund) not in seen
        seen.add((eid, role, fund))
        funds[eid, role].add(fund)
        info = (x['type'], x['review'])
        assert eid not in meta or meta[eid] == info
        meta[eid] = info
        component, value = x['component'], float(x['pp'])
        assert math.isfinite(value)
        sums[eid, role, component] += value
        group_totals[eid, role, x['group']] += value
        group_counts[eid, role, x['group']] += 1 if component == 'new' else -1 if component == 'exiting' else 0
        rows += 1

components = ['new', 'continuing', 'exiting']
by_review = defaultdict(list)
events = {}
for eid, (kind, review) in meta.items():
    assert all(funds[eid, role] == funds[eid, 'event'] for role in ['c1', 'c2', 'c3'])
    parts = {c: sums[eid, 'event', c] - sum(sums[eid, role, c] for role in ['c1', 'c2', 'c3']) / 3 for c in components}
    parts['preexisting'] = parts['continuing'] + parts['exiting']
    parts['total'] = sum(parts[c] for c in components)
    parts['new_minus_preexisting'] = parts['new'] - parts['preexisting']
    events[eid] = parts
    for component, value in parts.items():
        by_review[kind, component, review].append(value)

maximum_error = 0.0
with (ROOT / 'ownership_capital/event_component_results.csv').open() as f:
    for x in csv.DictReader(f):
        if x['group'] == 'ALL':
            for c, value in events[x['event_id']].items():
                error = abs(value - float(x['matched_' + c]))
                maximum_error = max(maximum_error, error)
                assert error < 1e-10

reviews = sorted({review for kind, review in meta.values() if kind == 'addition'})
primary = [statistics.mean(by_review['addition', 'new_minus_preexisting', review]) for review in reviews]
assert len(reviews) == 14
estimate = statistics.mean(primary)
se = statistics.stdev(primary) / math.sqrt(len(primary))
# Student t 0.975 quantile for 13 df; same fixed nominal interval as declared.
critical = 2.1603686564610127
ci = [estimate - critical * se, estimate + critical * se]
with (ROOT / 'ownership_capital/primary_contrast.csv').open() as f:
    published = next(csv.DictReader(f))
for name, value in [('mean_pp', estimate), ('se_pp', se), ('ci95_low', ci[0]), ('ci95_high', ci[1])]:
    assert abs(float(published[name]) - value) < 1e-10

with (ROOT / 'ownership_capital/same_support_counts_capital.csv').open() as f:
    for x in csv.DictReader(f):
        group = x['group']
        base_groups = sorted({k[2] for k in group_totals})
        members = base_groups if group == 'ALL' else [g for g in base_groups if g.startswith('OMXSB_')] if group == 'OMXSB_family' else [group]
        for field, source in [('count', group_counts), ('pp', group_totals)]:
            r = defaultdict(list)
            for eid, (kind, review) in meta.items():
                if kind != x['type']:
                    continue
                value = sum(source[eid, 'event', g] - sum(source[eid, role, g] for role in ['c1', 'c2', 'c3']) / 3 for g in members)
                r[review].append(value)
            mean = statistics.mean(statistics.mean(values) for values in r.values())
            assert abs(mean - float(x[field])) < 1e-10

report = {
    'all_checks_pass': True,
    'scope': 'Published derived-ledger arithmetic/hash/code-syntax check; raw-source and identity validation remains documented separately.',
    'manifest_files_checked': len(manifest['files']),
    'normalized_fund_role_rows': rows,
    'events': len(meta),
    'additions': sum(kind == 'addition' for kind, _ in meta.values()),
    'deletions': sum(kind == 'deletion' for kind, _ in meta.values()),
    'primary_reviews': len(reviews),
    'max_event_component_error_pp': maximum_error,
    'primary_mean_pp': estimate,
    'primary_se_pp': se,
    'primary_ci95': ci,
    'symmetric_fund_support_checked': True,
    'same_support_count_capital_table_checked': True,
}
(ROOT / 'PUBLICATION_VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
