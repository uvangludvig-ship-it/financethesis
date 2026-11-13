from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
files = ['README.txt', 'REPORT_SV.txt', 'SOURCE_LEDGER.json', 'TIMELINE.csv',
         'INVESTOR_EVIDENCE.csv', 'FEASIBILITY.json', 'INPUT_LEDGER.json',
         'DECISION_TABLE.json', 'SEARCH_LOG.json', 'ARCHIVE_LOG.json',
         'build_note.py', 'archive_sources.py', 'freeze_publication.py',
         'PUBLICATION_ALLOWLIST.json', 'PUBLICATION_SHA256.json']
(HERE / 'PUBLICATION_ALLOWLIST.json').write_text(json.dumps(files, indent=2) + '\n')
hashes = {}
for name in files:
    assert Path(name).name == name and name != 'private'
    if name == 'PUBLICATION_SHA256.json':
        continue
    hashes[name] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
(HERE / 'PUBLICATION_SHA256.json').write_text(json.dumps(hashes, indent=2) + '\n')
print(json.dumps({'allowlisted': len(files), 'hashed': len(hashes),
 'manifest_sha256': hashlib.sha256((HERE / 'PUBLICATION_SHA256.json').read_bytes()).hexdigest()}))
