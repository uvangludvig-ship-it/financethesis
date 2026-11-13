"""Replay three completed additions from frozen inputs; never fetch or rebuild gates."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
C=HERE.parent
P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--repo',type=Path,default=Path(os.environ.get('OMXSB_REPO',HERE.parents[3])))
P.add_argument('--output',type=Path)
A=P.parse_args()
R=A.repo.expanduser().resolve()
O=(A.output or Path(os.environ.get('OMXSB_FOLLOWUP_OUTPUT',R/'output/omxsb_followup_20261102'))).expanduser().resolve()
M=O/'additions_20261102'; ARC=M/'archived_original_work'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
archive=load(M/'ARCHIVE_SHA256.json'); locks=load(M/'LOCK_SHA256.json'); inputs=load(M/'INPUT_SHA256.json')

def assert_immutable():
    for name,h in archive.items():
        assert sha(ARC/name)==h,('Original archive changed',name)
    for name,h in locks.items():
        assert sha(O/name)==h,('Frozen active input changed',name)
        assert sha(ARC/name)==h,('Active lock differs from archived original',name)
    for name,h in inputs.items():
        assert sha(R/name)==h,('Required input changed; stop, do not silently rebuild',name)

assert_immutable()
steps=['mandate_upgrade_20261102/aggregate.py','mandate_upgrade_20261102/independent_audit.py',
       'owner_concentration_stability_20261102/run.py','owner_concentration_stability_20261102/independent_audit.py',
       'retention_scaling_feasibility_20261102/relative_retention.py','retention_scaling_feasibility_20261102/validate.py']
env=os.environ.copy();env['OMXSB_REPO']=str(R);env['OMXSB_FOLLOWUP_OUTPUT']=str(O)
env['PYTHONDONTWRITEBYTECODE']='1'  # Import existing helpers without writing caches into their package.
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
logs=M/'replay_logs';logs.mkdir(exist_ok=True);runs=[]
for n,step in enumerate(steps,1):
    log=logs/(f'{n:02d}_'+step.replace('/','_')+'.log')
    with log.open('w') as stream:
        proc=subprocess.run([sys.executable,str(C/step)],cwd=R,env=env,stdout=stream,stderr=subprocess.STDOUT)
    runs.append(dict(script=step,returncode=proc.returncode,log=str(log.relative_to(O))))
    (M/'replay_execution.json').write_text(json.dumps(dict(started_utc=started,repo=str(R),output=str(O),runs=runs,completed=False),indent=2))
    print(f'{n}/{len(steps)} {step}: returncode={proc.returncode}',flush=True)
    if proc.returncode:
        raise RuntimeError(f'Replay failed; inspect {log}')

csvs={
 'mandate_upgrade_20261102':['classified_fund_event_panel.csv.gz','event_demand_updated.csv','quantity_summary.csv','fixed_definition_ratios.csv'],
 'owner_concentration_stability_20261102':['all_omissions.csv','company_additive_contributions.csv','review_contributions.csv','event_company_contributions.csv','descriptive_ranges.csv'],
 'retention_scaling_feasibility_20261102':['core_ratios_all.csv','fund_review_factors.csv','relative_retention_all.csv','relative_retention_summary.csv','baseline_selection_audit.csv']}
checks=[]
for group,files in csvs.items():
    for file in files:
        old=ARC/group/file; new=O/group/file
        a=pd.read_csv(old);b=pd.read_csv(new)
        assert list(a)==list(b),(group,file,'columns')
        assert a.shape==b.shape,(group,file,'shape')
        errors={}
        for col in a:
            if pd.api.types.is_numeric_dtype(a[col]) and pd.api.types.is_numeric_dtype(b[col]):
                assert np.allclose(a[col],b[col],rtol=1e-10,atol=1e-10,equal_nan=True),(group,file,col)
                delta=(a[col].astype(float)-b[col].astype(float)).abs()
                errors[col]=float(delta.max()) if delta.notna().any() else 0.0
            else:
                assert a[col].fillna('__NA__').equals(b[col].fillna('__NA__')),(group,file,col)
        checks.append(dict(file=f'{group}/{file}',rows=len(a),all_values_equal=True,
                           max_numeric_absolute_error=max(errors.values(),default=0.0),byte_identical=sha(old)==sha(new)))

def canonical_science(value):
    if isinstance(value,dict):
        return {k:canonical_science(v)for k,v in value.items()if k!='input_hashes'}
    if isinstance(value,list):
        return [canonical_science(v)for v in value]
    if isinstance(value,str):
        for prefix in [str(R),'/Users/ludviguvang/dev/financethesis']:
            if value.startswith(prefix+'/'):
                return '<REPO>/'+value[len(prefix)+1:]
    return value

json_files=[('mandate_upgrade_20261102','independent_audit.json'),
            ('owner_concentration_stability_20261102','independent_audit.json'),
            ('retention_scaling_feasibility_20261102','independent_validation.json')]
for group,file in json_files:
    a=canonical_science(load(ARC/group/file));b=canonical_science(load(O/group/file))
    assert a==b,(group,file,'scientific JSON changed')
    checks.append(dict(file=f'{group}/{file}',scientific_json_exactly_equal=True,
                       ignored_metadata=['input_hashes'],normalized_paths='repo prefix only'))

assert_immutable()
codehashes={str(p.relative_to(C)):sha(p)for p in [HERE/'portable_paths.py',HERE/'replay.py']+[C/s for s in steps]}
report=dict(completed=True,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 python=sys.version,platform=platform.platform(),repo=str(R),output=str(O),scripts=runs,
 scientific_outputs_checked=checks,csv_tolerance=dict(rtol=1e-10,atol=1e-10),
 archived_original_file_count=len(archive),frozen_active_file_count=len(locks),repository_input_count=len(inputs),
 original_archive_intact=True,all_locks_byte_identical=True,all_existing_inputs_unchanged=True,
 no_gate_rebuild=True,no_fetching=True,no_new_economic_specification=True,code_sha256=codehashes,
 expected_provenance_changes=['Code/output absolute paths in generated hashes.json/outcome_hashes.json/input_hashes',
 'gzip header timestamp, while decompressed CSV values are compared',
 'PPM original source paths resolve relative to the current repo; original identity JSON stays byte-identical'])
(M/'replay_comparison.json').write_text(json.dumps(report,indent=2))
(M/'replay_execution.json').write_text(json.dumps(dict(completed=True,runs=runs),indent=2))
print('All 14 scientific tables and 3 independent-audit JSONs reproduced. Original archive and locks unchanged.',flush=True)
