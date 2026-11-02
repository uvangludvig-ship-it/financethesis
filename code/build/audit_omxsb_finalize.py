"""Check preserved sources, register data artifacts, and finish audit provenance."""
import hashlib
import json
from pathlib import Path
import subprocess
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'output/omxsb_audit_20261031'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

# Fail rather than imply an incomplete or stale execution is current.
complete=json.loads((A/'corrected/run_complete.json').read_text())
assert complete['all_code_cells_executed']
assert complete['notebook_sha256']==sha(ROOT/'code/notebooks/replication_omxsb_2007.ipynb')
for name,digest in complete['scripts'].items():assert sha(ROOT/name)==digest,name
for r in json.loads((A/'original_sha256.json').read_text()):
    assert sha(A/'original'/r['file'])==r['sha256'],r['file']
inputs=pd.read_csv(A/'input_inventory.csv')
for r in inputs.itertuples():assert sha(ROOT/r.file)==r.sha256,r.file
assert subprocess.check_output(['git','diff','--name-only','--','data/raw','output/omxsb_replication_2007'],cwd=ROOT,text=True)==''

results=pd.read_csv(A/'result_table.csv')
assert not results[['question','type','period','window','unit','source','supports','does_not_support']].isna().any().any()
assert (results.N>=results.independent_reviews).all()
assert results.ci_low.le(results.ci_high).all()
raw=json.loads((A/'fi_raw_summary.json').read_text())
assert raw['parse_errors']==0 and raw['row_count_mismatches']==0

# Exhaustive path registry complements the human-facing A/B/C ledger.
records=[]
for p in sorted(A.rglob('*')):
    if not p.is_file() or p.name in ['artifact_inventory.csv','final_validation.json']:continue
    rel=p.relative_to(A)
    kind='frozen original' if rel.parts[0]=='original' else 'baseline rerun' if rel.parts[0]=='baseline' else 'corrected rerun' if rel.parts[0]=='corrected' else 'audit support/report'
    records.append(dict(file=str(p.relative_to(ROOT)),role=kind,bytes=p.stat().st_size,sha256=sha(p)))
inventory=pd.DataFrame(records)
inventory.to_csv(A/'artifact_inventory.csv',index=False)
marker='<!-- OMXSB_AUDIT_20261031 -->'
endmarker='<!-- END_OMXSB_AUDIT_20261031 -->'
manifest=ROOT/'data/MANIFEST.md'
existing=manifest.read_text()
text, found, rest=existing.partition(marker)
suffix=''
if found:
    if endmarker in rest:
        suffix=rest.split(endmarker,1)[1]
    else:
        # Preserve independently appended sections after the old generated table.
        oldlines=rest.splitlines(keepends=True)
        last=max(i for i,line in enumerate(oldlines) if line.startswith('| `output/omxsb_audit_20261031/'))
        suffix=''.join(oldlines[last+1:])
text=text.rstrip()
data=inventory[inventory.file.str.endswith(('.csv','.csv.gz','.json','.xls','.xlsx'))]
lines=[marker,'','## OMXSB verification audit 31 Oct 2026','',
       'Base commit: `b886f5b744f797a6c1252f0e41fe2b740591c8c3`. Raw inputs unchanged. '
       'The original `omxsb_replication_2007/` exports remain frozen; corrected exports are in the separate audit folder. '
       'The full artifact registry includes SHA256, byte size and role for every artifact. '
       'Scientific conclusions and unresolved history are in `output/omxsb_audit_20261031/GRANSKNING.md`.','',
       '| File | Role/source and generator | Bytes |','|---|---|---|',
       '| `output/omxsb_audit_20261031/artifact_inventory.csv` | Per-file SHA256 registry; `code/build/audit_omxsb_finalize.py` | generated |']
for z in data.itertuples():
    generator='audit_omxsb_run.py / preserved commit' if z.role!='audit support/report' else 'code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md'
    lines.append(f'| `{z.file}` | {z.role}; {generator} | {z.bytes} |')
manifest.write_text(text+'\n\n'+'\n'.join(lines)+'\n'+endmarker+'\n'+suffix)
log=ROOT/'thesis/AI_LOG.md'
entry='| 31 Oct 2026 | Codex | Verify OMXSB replication and data availability before choosing extension | Preserved b886f5b exports; reran all 2007 notebook cells, mechanisms, periods and trends; verified LFS/parquet/FI XML; corrected pre-month, E5b inference, paired reporting, bootstrap ties and coverage labels; audit report, result/gap ledgers and run scripts in output/omxsb_audit_20261031; manifest updated; no FTN returns | No |'
if entry not in log.read_text():log.write_text(log.read_text().rstrip()+'\n'+entry+'\n')
status=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)
(A/'final_validation.json').write_text(json.dumps(dict(
    base_commit='b886f5b744f797a6c1252f0e41fe2b740591c8c3',audited_inputs_and_original_exports_unchanged=True,
    input_hashes_rechecked=True,frozen_snapshot_hashes_rechecked=True,current_code_matches_completed_run=True,
    result_rows=len(results),registered_data_files=len(data)+1,git_status=status,
    source_code_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'code/build').glob('*omxsb*.py'))},
    note='No FTN return scripts run. Local modifications; no commit or push performed.'),indent=2))
print('Preservation, input hashes, executed source hashes, results and FI reconciliation passed.')
