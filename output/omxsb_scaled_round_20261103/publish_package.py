"""Copy only explicit public deliverables; never publish raw market data.

Run after all subtask allowlists and the root README have been finalized.
Private inputs stay at their original locations; licensing is not inferred
from a filename. A package hash is a completeness check, not statistical QA.
"""
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
REPO = Path('/Users/ludviguvang/dev/financethesis')
DEST = REPO/'output/omxsb_scaled_round_20261103'

files = ['ROUND_LOG.txt', 'README_SV.txt', 'RUN.txt', 'publish_package.py']
coverage = ['build_requests.py','fetch.py','SOURCE_REQUEST_ROWS.csv',
            'SOURCE_REQUEST_LOCK.json','FETCH_LOG.json','SOURCE_PRESENCE.csv']
files += ['coverage/'+p for p in coverage]
auction = json.loads((HERE/'auction_design/PUBLICATION_ALLOWLIST.json').read_text())['files']
files += ['auction_design/'+p for p in auction]
files += ['auction_design/PUBLICATION_ALLOWLIST.json']
winner = (HERE/'winner_novelty/PUBLICATION_ALLOWLIST.txt').read_text().splitlines()
files += ['winner_novelty/'+p for p in winner if p.strip()]
for folder in ['independent_design', 'auction_design/retention_audit', 'historical_coverage', 'workbook_audit']:
    data = json.loads((HERE/folder/'PUBLICATION_ALLOWLIST.json').read_text())
    paths = data.get('files',data.get('allowed_files')) if isinstance(data,dict) else data
    assert isinstance(paths,list), folder
    files += [folder+'/'+p for p in paths]
    if folder+'/PUBLICATION_ALLOWLIST.json' not in files:
        files += [folder+'/PUBLICATION_ALLOWLIST.json']

assert len(files)==len(set(files)), 'Duplicate public file'
for rel in files:
    p = Path(rel)
    assert not p.is_absolute() and '..' not in p.parts
    assert not any(x.startswith('private') or x in ['.venv','__pycache__'] for x in p.parts)
    assert (HERE/p).is_file(), rel
DEST.mkdir(parents=True,exist_ok=True)
(DEST/'.gitignore').write_text('**/private/\n**/private_sources/\n**/private_reading/\n**/__pycache__/\n**/.venv/\n')
for rel in files:
    target=DEST/rel
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(HERE/rel,target)
manifest={p:hashlib.sha256((DEST/p).read_bytes()).hexdigest()
          for p in sorted(files+['.gitignore'])}
(DEST/'PACKAGE_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'destination':str(DEST),'public_hashed_files':len(manifest),
                  'licensed_raw_copied':False}))
