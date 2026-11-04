"""Archive already-read public primary sources privately, without browser/auth."""
from pathlib import Path
from datetime import datetime, timezone
import concurrent.futures
import hashlib
import json
import urllib.request

HERE = Path(__file__).resolve().parent
sources = json.loads((HERE / 'SOURCE_LEDGER.json').read_text())
private = HERE / 'private'
private.mkdir(exist_ok=True)

def fetch(s):
    result = {'source_id': s['source_id'], 'url': s['url'],
              'attempt_utc': datetime.now(timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(s['url'], headers={'User-Agent': 'Mozilla/5.0 (academic source verification)'})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read()
            result.update(http_status=r.status, content_type=r.headers.get('Content-Type'), final_url=r.url)
        (private / (s['source_id'] + '.bin')).write_bytes(body)
        result.update(raw_body_sha256=hashlib.sha256(body).hexdigest(), bytes=len(body), status='ARCHIVED_PRIVATE')
    except Exception as exc:
        result.update(status='DIRECT_FETCH_FAILED_WEB_READ_SUCCEEDED', error=str(exc), raw_body_sha256=None)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, sources))
(HERE / 'ARCHIVE_LOG.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
for s, r in zip(sources, results):
    s['raw_body_sha256'] = r['raw_body_sha256']
    s['archive_status'] = r['status']
(HERE / 'SOURCE_LEDGER.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'archived_private': sum(r['status'] == 'ARCHIVED_PRIVATE' for r in results), 'attempted': len(results)}))
