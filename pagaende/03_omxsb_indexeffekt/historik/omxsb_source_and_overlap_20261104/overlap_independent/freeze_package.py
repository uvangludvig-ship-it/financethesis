"""Freeze exact public audit files; exclude all licensed raw rows."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
FILES=[
 'AUDIT_SPEC.txt','replay.py','check_baseline_reports.py',
 'BASELINE_REPORT_CHECK.json','REPORT_SV.txt','README.txt',
 'SOURCE_SEMANTICS.json','freeze_package.py',
 'independent_replay/INPUT_LOCK.json',
 'independent_replay/INDEPENDENT_EVENT_BOUNDS.csv',
 'independent_replay/INDEPENDENT_REVIEW_BOUNDS.csv',
 'independent_replay/INDEPENDENT_RESULT.json',
 'independent_replay/COMPARISON.json',
 'PUBLICATION_ALLOWLIST.json','PUBLICATION_SHA256.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
assert not (P/'PUBLICATION_SHA256.json').exists(),'Preserve frozen audit package.'
write(P/'PUBLICATION_ALLOWLIST.json',FILES)
hashes={f:sha(P/f) for f in FILES if f!='PUBLICATION_SHA256.json'}
write(P/'PUBLICATION_SHA256.json',hashes)
assert len(hashes)==len(FILES)-1
print(json.dumps({'files':len(FILES),'hashes':len(hashes),'manifest_sha256':sha(P/'PUBLICATION_SHA256.json')},indent=2))
