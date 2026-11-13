"""Verify duplicate CAMX 2023-11-23 delivery without adding an observation."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from compare_bins import load, sha


def canonical(columns, rows):
    return hashlib.sha256(json.dumps([[r[c] for c in columns] for r in rows],
        ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--first', type=Path, required=True)
    p.add_argument('--second', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    assert not a.out.exists()
    columns1, all1 = load(a.first)
    columns2, all2 = load(a.second)
    assert columns1 == columns2
    select = lambda rows: [r for r in rows if r['isin']=='SE0007692850' and r['date']=='2023-11-23']
    rows1, rows2 = select(all1), select(all2)
    assert rows1 and rows2
    mismatched = Counter()
    for x, y in zip(rows1, rows2):
        for c in columns1:
            if x[c] != y[c]:
                mismatched[c] += 1
    equal = rows1 == rows2
    result = dict(created_utc=datetime.now(timezone.utc).isoformat(), source_only=True,
        ISIN='SE0007692850', date='2023-11-23',
        files=[dict(path=str(a.first), sha256=sha(a.first)), dict(path=str(a.second), sha256=sha(a.second))],
        columns=columns1, rows_first=len(rows1), rows_second=len(rows2),
        cells_compared_in_same_row_order=min(len(rows1),len(rows2))*len(columns1),
        exact_same_cells_and_order=equal, mismatched_cell_counts=dict(mismatched),
        canonical_ordered_rows_sha256_first=canonical(columns1, rows1),
        canonical_ordered_rows_sha256_second=canonical(columns1, rows2),
        duplicate_source_is_not_an_additional_observation=True,
        no_raw_numeric_values_or_economic_outcomes_exported=True,
        script_sha256=sha(Path(__file__)), comparison_dependency_sha256=sha(Path(__file__).with_name('compare_bins.py')))
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['rows_first','rows_second','cells_compared_in_same_row_order','exact_same_cells_and_order']}))
    assert equal, 'Conflicting duplicate source; stop before any combined validation'


if __name__ == '__main__':
    main()
