"""Replay the already declared follow-ups without rebuilding or overwriting locks."""
from pathlib import Path
import argparse,os,sys,subprocess,json,hashlib,datetime,platform
import pandas as pd,numpy as np
C=Path(__file__).resolve().parent
P=argparse.ArgumentParser()
P.add_argument('--repo',type=Path,default=Path(os.environ.get('OMXSB_REPO',C.parents[2])))
P.add_argument('--output',type=Path)
A=P.parse_args();R=A.repo.expanduser().resolve();O=(A.output or Path(os.environ.get('OMXSB_FOLLOWUP_OUTPUT',R/'output/omxsb_followup_20261102'))).expanduser().resolve()
ARC=O/'archived_original_work';assert (ARC/'ARCHIVE_SHA256.json').is_file(),'Copy the saved outputs and archive first.'
input_hashes=json.loads((O/'INPUT_SHA256.json').read_text())
for f,h in input_hashes.items():
    q=R/f
    assert q.is_file(), ('Missing required input',f)
    assert hashlib.sha256(q.read_bytes()).hexdigest()==h, ('Input differs from frozen source; stop before replay',f)
archive_hashes=json.loads((ARC/'ARCHIVE_SHA256.json').read_text())
for f,h in archive_hashes.items():assert hashlib.sha256((O/f).read_bytes()).hexdigest()==h,('Original archive changed',f)
locks=['deletion_exposure_20261102/ANALYSIS_LOCK.json','deletion_exposure_20261102/GATE_PROTOCOL.txt','deletion_exposure_20261102/gate_event_ledger.csv','retention_followup_20261102/DECLARATION.txt','retention_followup_20261102/quantity_gate_frozen.csv','retention_followup_20261102/gate_frozen_summary.json']
lock_before={f:hashlib.sha256((O/f).read_bytes()).hexdigest()for f in locks}
for f,h in lock_before.items():assert h==hashlib.sha256((ARC/f).read_bytes()).hexdigest(),('Frozen original differs',f)
steps=['comparison_rebuild_20261102/run.py','comparison_rebuild_20261102/independent_audit.py','volume_measurement_20261102/run.py','volume_measurement_20261102/independent_audit.py','volume_measurement_20261102/unit_venue_audit/audit.py','retention_followup_20261102/quantity.py','retention_followup_20261102/validate.py','deletion_exposure_20261102/freeze_and_run.py','deletion_exposure_20261102/verify_raw.py']
env=os.environ.copy();env['OMXSB_REPO']=str(R);env['OMXSB_FOLLOWUP_OUTPUT']=str(O)
started=datetime.datetime.now(datetime.timezone.utc).isoformat();logs=O/'replay_logs';logs.mkdir(exist_ok=True);runs=[]
for i,step in enumerate(steps,1):
    dest=logs/(f'{i:02d}_'+step.replace('/','_')+'.log')
    with dest.open('w')as stream:
        r=subprocess.run([sys.executable,str(C/step)],cwd=R,env=env,stdout=stream,stderr=subprocess.STDOUT)
    runs.append(dict(script=step,returncode=r.returncode,log=str(dest.relative_to(O))))
    print(f'{i}/{len(steps)} {step}: returncode={r.returncode}',flush=True)
    if r.returncode:
        (O/'replay_execution.json').write_text(json.dumps(dict(started=started,repo=str(R),output=str(O),runs=runs,completed=False),indent=2))
        raise RuntimeError(f'Replay failed; inspect {dest}')
files={
'comparison_rebuild_20261102':['ratios.csv','same_sample_events.csv','US_reference.csv'],
'volume_measurement_20261102':['gate_and_volume.csv','joined_all.csv','volume_quantity_ratios.csv','diagnostic_slopes.csv','independent_shared_scale_diagnostic.csv','independent_window_and_unit_checks.csv','unit_venue_audit/monthly_comparison.csv'],
'retention_followup_20261102':['position_quantities.csv','quantity_summary.csv','two_verified_class_denominator_cases.csv','existing_price_join.csv','previous_stale_share_snapshots.csv'],
'deletion_exposure_20261102':['analysis_event_ledger.csv','analysis_event_ledger_all_frozen_rows.csv','primary_size_preCAR_official_liquidity_all_coefficients.csv','sensitivity_reviewFE_only_all_coefficients.csv','results.csv','quarter_liquidation_review_description.csv','raw_position_reconciliation.csv']}
checks=[]
for group,ff in files.items():
    for f in ff:
        old=ARC/group/f;new=O/group/f
        a=pd.read_csv(old);b=pd.read_csv(new);assert list(a)==list(b),(group,f,'columns');assert a.shape==b.shape,(group,f,'shape')
        errors={};pathcols=[]
        for col in a:
            if pd.api.types.is_numeric_dtype(a[col])and pd.api.types.is_numeric_dtype(b[col]):
                assert np.allclose(a[col],b[col],equal_nan=True,rtol=1e-10,atol=1e-10),(group,f,col)
                d=(a[col].astype(float)-b[col].astype(float)).abs();errors[col]=float(d.max())if d.notna().any()else 0.
            elif group=='volume_measurement_20261102'and f=='unit_venue_audit/monthly_comparison.csv'and col=='source_file':
                assert a[col].map(lambda x:Path(x).name).equals(b[col].map(lambda x:Path(x).name));pathcols.append(col)
            else:assert a[col].fillna('__NA__').equals(b[col].fillna('__NA__')),(group,f,col)
        checks.append(dict(file=f'{group}/{f}',rows=len(a),all_values_equal_within_tolerance=True,numeric_max_abs_error=max(errors.values())if errors else 0.,expected_provenance_path_columns=pathcols,byte_identical=hashlib.sha256(old.read_bytes()).hexdigest()==hashlib.sha256(new.read_bytes()).hexdigest()))
# JSON scientific fields: exact equality where paths/hash metadata are absent.
for group,f in [('retention_followup_20261102','joint_existing_price_description.json'),('retention_followup_20261102','independent_quantity_validation.json'),('deletion_exposure_20261102','quarter_liquidation_summary.json'),('deletion_exposure_20261102','raw_position_validation.json')]:
    a=json.loads((ARC/group/f).read_text());b=json.loads((O/group/f).read_text());assert a==b,(group,f,'JSON changed')
    checks.append(dict(file=f'{group}/{f}',scientific_json_exactly_equal=True))
lock_after={f:hashlib.sha256((O/f).read_bytes()).hexdigest()for f in locks};assert lock_before==lock_after
for f,h in archive_hashes.items():assert hashlib.sha256((O/f).read_bytes()).hexdigest()==h,('Archive mutated',f)
result=dict(completed=True,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),repo=str(R),output=str(O),scripts=runs,csv_numeric_tolerance=dict(rtol=1e-10,atol=1e-10),scientific_outputs_checked=checks,original_frozen_hashes=lock_after,all_locks_byte_identical=True,original_archive_files=len(archive_hashes),original_archive_intact=True,no_gate_rebuild=True,no_economic_specification_change=True)
(O/'replay_comparison.json').write_text(json.dumps(result,indent=2));(O/'replay_execution.json').write_text(json.dumps(dict(completed=True,runs=runs),indent=2))
print('All scientific outputs reproduced; original locks and archives unchanged.',flush=True)
