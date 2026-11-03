"""Independent source-only verification; no returns, flows or covariance estimates."""
from pathlib import Path
import csv, io, zipfile, hashlib, json, math, os
from collections import defaultdict
from datetime import datetime, timezone

REPO = Path(os.environ.get('FINANCETHESIS_REPO', '/Users/ludviguvang/dev/financethesis'))
HERE = Path(__file__).resolve().parent
CLASSES = REPO / 'output/omxsb_design_frontier_20261103/independent/ACQUISITION_PILOT_CLASSES.csv'
SOURCES = {
    'rips': REPO / 'data/raw/shof/Reinvestments/pilot_20261103/FUNDS_RIPS_1793724775329.zip',
    'valuations': REPO / 'data/raw/shof/Valuations/pilot_20261103/FUNDS_VALUATIONS_1793724895212.zip',
}

def finite(s):
    try:
        v = float(s)
        return v if math.isfinite(v) else None
    except (ValueError, TypeError):
        return None

def read(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == 1 and names[0].endswith('.csv')
        with z.open(names[0]) as f:
            return [{k.lower(): v for k, v in row.items()} for row in csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig'), delimiter=';')]

def main():
    classes = list(csv.DictReader(CLASSES.open()))
    ids = {r['performanceid'] for r in classes}
    results = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Source presence and consistency only; no economic outcome calculated.', 'sources': {}}
    for kind, p in SOURCES.items():
        rows = read(p)
        assert all(r['performanceid'] in ids and '2017-01-01' <= r['date'][:10] <= '2023-12-31' for r in rows)
        keys = [(r['performanceid'], r['date'][:10], r.get('returntype', '')) for r in rows]
        result = {
            'relative_path': str(p.relative_to(REPO)), 'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'zip_crc_ok': True,
            'rows': len(rows), 'unique_classes': len({r['performanceid'] for r in rows}),
            'duplicate_class_date_type_rows': len(keys) - len(set(keys)),
        }
        byclass = []
        for pid in sorted(ids):
            rs = [r for r in rows if r['performanceid'] == pid]
            ds = [r['date'][:10] for r in rs]
            item = {'performanceid': pid, 'rows': len(rs), 'first_date': min(ds) if ds else None, 'last_date': max(ds) if ds else None}
            fields = ['unit_sek'] if kind == 'rips' else ['tnaclass', 'tnafund', 'netflowclass', 'netflowfund']
            for field in fields:
                present = [r for r in rs if finite(r.get(field)) is not None and (field.startswith('netflow') or finite(r[field]) > 0)]
                item[field + '_present_rows'] = len(present)
                item[field + '_present_months'] = len({r['date'][:7] for r in present})
            byclass.append(item)
        result['class_presence'] = byclass
        if kind == 'rips':
            result['returntypes'] = sorted({r['returntype'] for r in rows})
            assert result['returntypes'] == ['1']
        results['sources'][kind] = result
    (HERE / 'ROOT_SOURCE_VERIFICATION.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({k: {x:v for x,v in d.items() if x != 'class_presence'} for k,d in results['sources'].items()}, indent=2))

if __name__ == '__main__':
    main()
