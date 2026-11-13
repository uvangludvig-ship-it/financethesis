"""Exact publication allowlist; exclude private vendor records and source bodies."""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
FILES=[
    'REPORT_SV.txt','REVIEW_VERIFICATION.csv','EVENT_VERIFICATION_OVERLAY.csv',
    'SOURCE_LEDGER.json','SEARCH_LOG.json','INPUT_LEDGER.json','SCOPE_LOCK.json',
    'VALIDATION.json','REQUEST_SPEC.txt','build_verification.py',
    'archive_evidence.py','freeze_publication.py',
    'PUBLICATION_ALLOWLIST.json','PUBLICATION_SHA256.json'
]
def write(name,obj):
    (BASE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
    assert all('/' not in x and x!='private' for x in FILES)
    write('PUBLICATION_ALLOWLIST.json',FILES)
    hashes={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest()
            for name in FILES if name!='PUBLICATION_SHA256.json'}
    write('PUBLICATION_SHA256.json',hashes)
    assert all(hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h for n,h in hashes.items())
    print(json.dumps({'allowlist_files':len(FILES),'verified_hashes':len(hashes),
       'manifest_sha256':hashlib.sha256((BASE/'PUBLICATION_SHA256.json').read_bytes()).hexdigest()}))
