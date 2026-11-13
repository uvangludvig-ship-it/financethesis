"""Check the public manifest and private-path exclusion; no network request."""
from pathlib import Path
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parent
expected=json.loads((ROOT/'PACKAGE_SHA256.json').read_text())
assert expected
for name,digest in expected.items():
    p=Path(name)
    assert not p.is_absolute() and '..' not in p.parts
    assert not set(p.parts)&{'private','sources','.venv','__pycache__'}
    assert p.suffix not in {'.pdf','.html','.zip','.gz','.png','.log'}
    assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest,name
try:
    repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
except subprocess.CalledProcessError:
    repo=None
if repo:
    for private in ROOT.glob('*/private'):
        for p in private.iterdir():
            if p.is_file():
                assert subprocess.run(['git','check-ignore','-q',str(p)],cwd=repo).returncode==0,p
print(json.dumps({'public_file_hashes_verified':len(expected),'no_raw_or_fulltext_paths_in_manifest':True,'local_private_paths_ignored':bool(repo)}))
