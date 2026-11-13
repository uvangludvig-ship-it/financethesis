"""Publish only the enumerated design evidence, never licensed raw data."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import shutil
import zipfile

W = Path(__file__).resolve().parent
R = Path('/Users/ludviguvang/dev/financethesis')
OUT = R / 'output/omxsb_design_frontier_20261103'
ART = W.parents[1] / 'outputs'

ownership = '''REPORT_SV.txt FRAGILITY_REDTEAM.txt README.txt baseline.py
seb_baseline_support.py fund_mandate_evidence.csv source_ledger.csv input_map.csv
BASELINE_LOCK.txt BASELINE_RUN.json SEB_SUPPORT_RUN.json baseline_overlap_summary.csv
baseline_overlap_by_company.csv seb_baseline_support_summary.csv seb_baseline_by_review.csv
FINAL_CHECK.json'''.split()
network = (W / 'network/PUBLICATION_ALLOWLIST.txt').read_text().splitlines()
independent = json.loads((W / 'independent/PUBLICATION_ALLOWLIST.json').read_text())['allowed_files']

# The parent independently reran the synthetic validator; refresh that diagnostic's
# hash in the local ledger without pretending it is the agent's earlier run.
ledger_path = W / 'independent/FILE_LEDGER.json'
ledger = json.loads(ledger_path.read_text())
p = W / 'independent/PILOT_VALIDATOR_SYNTHETIC_TESTS.json'
ledger['files'][p.name] = {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
ledger['root_repeated_synthetic_check_at_utc'] = json.loads(p.read_text())['at_utc']
ledger_path.write_text(json.dumps(ledger, indent=2))

files = [Path('BESLUT_SV.txt'), Path('ROOT_VALIDATION.json'), Path('publish.py')]
for folder, names in [('ownership', ownership), ('network', network), ('independent', independent)]:
    for name in names:
        if name.strip():
            files.append(Path(folder) / name.strip())
assert len(files) == len(set(files))
assert all(p.suffix in {'.txt', '.json', '.csv', '.py'} for p in files)
assert all((W / p).is_file() for p in files)
for p in files:
    if p.suffix == '.py':
        ast.parse((W / p).read_text())

OUT.mkdir(parents=True, exist_ok=True)
for p in files:
    dst = OUT / p
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(W / p, dst)

(OUT / 'README.txt').write_text('''Start with BESLUT_SV.txt (Swedish research decision note, not thesis prose).
This package contains source and baseline feasibility work, not new economic outcomes.
The conditional candidate is investor-flow exposure of the changed ownership composition.
The exact prior is Greenwood-Thesmar (2011), footnote 15, not a new international question.
Current-data source coverage is inadequate. New pilot acquisition awaits university login.

ownership/: dated-mandate within-company design, not selected; independent conceptual risk review.
network/: improved potential-clientele definition, not selected; no new return outcomes.
independent/: SHoF source checks, 20-class/five-fund request, source-only pilot validator.
ROOT_VALIDATION.json: parent recomputation of the headline availability counts.

Scripts preserve original local execution paths recorded in their locks. Licensed source
files and some intermediate audit tables are intentionally not included. A clean clone
alone cannot recreate all source probes. Input hashes and each subfolder's replay note
identify what is needed. Synthetic source validation needs no licensed inputs:
  python independent/test_pilot_validator.py
Future downloads stay private. The pilot validator accepts CSV/ZIP and reports dates,
presence and duplicate diagnostics; it does not compute economic outcomes.

No FTN event outcomes were opened. No original results or raw sources were overwritten.
The separate concurrently published runda12_deklaration.md belongs to another analysis;
this round neither reruns it nor endorses its economic assumptions.
OUTPUT_MANIFEST.json hashes this public subset. Earlier subfolder ledgers describe
their original local audit products, including products deliberately excluded here.
''')
manifest = {
    'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'new_economic_results': False,
    'new_raw_downloads_received': False,
    'files': {
        str(p.relative_to(OUT)): {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'OUTPUT_MANIFEST.json'
    }
}
(OUT / 'OUTPUT_MANIFEST.json').write_text(json.dumps(manifest, indent=2))
ART.mkdir(parents=True, exist_ok=True)
shutil.copy2(OUT / 'BESLUT_SV.txt', ART / 'OMXSB_nasta_pusselbit_20261103.txt')
zpath = ART / 'OMXSB_designprov_20261103.zip'
with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(OUT))
print(json.dumps({'published': str(OUT), 'files': len(manifest['files']) + 1,
                  'zip': str(zpath), 'bytes': zpath.stat().st_size}, indent=2))
