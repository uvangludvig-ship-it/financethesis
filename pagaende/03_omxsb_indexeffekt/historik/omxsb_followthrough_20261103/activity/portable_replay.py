"""Replay frozen calculations with explicit paths; never edits first-run scripts."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument('--repo-root', type=Path, required=True)
parser.add_argument('--nasdaq-dir', type=Path, required=True,
                    help='Folder containing the ten original YYYYMM.xls files')
parser.add_argument('--output', type=Path, required=True,
                    help='New output directory; existing files are never overwritten')
parser.add_argument('--source-only', action='store_true')
parser.add_argument('--compare-to', type=Path,
                    help='Frozen producer directory; defaults to this package directory')
args = parser.parse_args()
package = Path(__file__).resolve().parent
reference = (args.compare_to or package).resolve()
repo, nasdaq, out = args.repo_root.resolve(), args.nasdaq_dir.resolve(), args.output.resolve()
if out.exists() and any(out.iterdir()):
    raise SystemExit('Use a new empty output directory; frozen outputs will not be overwritten.')
for p in [repo, nasdaq, reference]:
    if not p.is_dir(): raise SystemExit(f'Missing required directory: {p}')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
path_spec = json.loads((package/'PORTABLE_PATH_DIFF.json').read_text())
for filename, expected in path_spec['original_script_sha256'].items():
    if sha(package/filename) != expected:
        raise SystemExit(f'Frozen original script hash changed: {filename}')
# Ensure all ten fixed source originals are available and identical before execution.
for source in json.loads((reference/'UNIT_GATE_SUMMARY.json').read_text())['raw_files']:
    p = nasdaq/Path(source['file']).name
    if not p.is_file() or sha(p) != source['sha256']:
        raise SystemExit(f'Missing or different original Nasdaq workbook: {p}')
out.mkdir(parents=True, exist_ok=True)
code = out/'replay_code'; code.mkdir()
for filename in ['SOURCE_GATE_SPEC.txt', 'PRIMARY_SPEC.txt']:
    shutil.copyfile(package/filename, out/filename)
transforms = {
    'check_source_presence.py': [
        ("O=Path(__file__).resolve().parent;BASE=O.parents[1];R=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis'))",
         "O=Path(os.environ['OMXSB_ACTIVITY_WORKDIR']);R=Path(os.environ['FINANCETHESIS_REPO'])"),
        ("BASE/'omxsb_scaled_round_20261103/independent_design/retention/FROZEN_ROLES.csv'",
         "R/'output/omxsb_scaled_round_20261103/independent_design/retention/FROZEN_ROLES.csv'"),
        ("BASE/'volume_units_full_20261102/all_available_exactISIN_month_anchors.csv'",
         "R/'output/omxsb_followup_20261102/volume_units_full_20261102/all_available_exactISIN_month_anchors.csv'")],
    'reconcile_turnover.py': [
        ('import sys,re,json,hashlib', 'import sys,re,json,hashlib,os'),
        ("O=Path(__file__).resolve().parent;sys.path.insert(0,str(O/'.deps'))",
         "O=Path(os.environ['OMXSB_ACTIVITY_WORKDIR']);sys.path.insert(0,str(O/'.deps'))"),
        ("BASE=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis');PVT=O/'private';PVT.mkdir(exist_ok=True)",
         "R=Path(os.environ['FINANCETHESIS_REPO']);N=Path(os.environ['OMXSB_NASDAQ_DIR']);PVT=O/'private';PVT.mkdir(exist_ok=True)"),
        ("BASE/'open_questions_20261101/eligibility'/f'{ym}.xls'", "N/f'{ym}.xls'")],
    'run_primary.py': []
}
changes = []
for filename, pairs in transforms.items():
    text = (package/filename).read_text()
    for old, new in pairs:
        if text.count(old) != 1: raise SystemExit(f'Path-only transform not unique: {filename}: {old}')
        text = text.replace(old, new)
        changes.append({'file': filename, 'from': old, 'to': new})
    (code/filename).write_text(text)
env = os.environ.copy()
env.update(FINANCETHESIS_REPO=str(repo), OMXSB_ACTIVITY_WORKDIR=str(out), OMXSB_NASDAQ_DIR=str(nasdaq))
# The original workdir's optional local dependency installation is not required on clean installations.
if (package/'.deps').is_dir():
    env['PYTHONPATH'] = str(package/'.deps') + (os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
lock = {'started_utc': datetime.now(timezone.utc).isoformat(), 'source_only': args.source_only,
        'repo_root': str(repo), 'nasdaq_dir': str(nasdaq), 'output': str(out),
        'original_script_sha256': path_spec['original_script_sha256'], 'exact_path_substitutions': changes,
        'generated_script_sha256': {p.name: sha(p) for p in code.iterdir()}}
(out/'PORTABLE_REPLAY_LOCK.json').write_text(json.dumps(lock, indent=2)+'\n')
steps = ['check_source_presence.py', 'reconcile_turnover.py']
if not args.source_only: steps.append('run_primary.py')
for filename in steps:
    with (out/(filename+'.log')).open('w') as log:
        subprocess.run([sys.executable, str(code/filename)], env=env, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
# Compare actual source flags/metadata, not locks whose paths/timestamps necessarily differ.
import pandas as pd
comparisons = []
for filename in ['ROLE_SOURCE_PRESENCE.csv','EVENT_SOURCE_PRESENCE.csv',
                 'MONTHLY_TURNOVER_UNIT_FLAGS.csv','ROLE_FINAL_SOURCE_GATE.csv','EVENT_FINAL_SOURCE_GATE.csv']:
    actual, expected = pd.read_csv(out/filename), pd.read_csv(reference/filename)
    ignore = [c for c in ['source_file'] if c in actual.columns]
    pd.testing.assert_frame_equal(actual.drop(columns=ignore), expected.drop(columns=ignore),
                                  check_exact=True)
    comparisons.append({'file':filename, 'rows':len(actual), 'all_nonpath_cells_identical':True})
validation = {'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
              'source_only':args.source_only,'new_outcomes_computed':not args.source_only,
              'source_comparisons':comparisons,
              'primary_script_byte_identical':sha(code/'run_primary.py')==path_spec['original_script_sha256']['run_primary.py'],
              'originals_unchanged':all(sha(package/n)==v for n,v in path_spec['original_script_sha256'].items())}
if not args.source_only:
    expected = json.loads((reference/'PRIMARY_RESULT.json').read_text())
    actual = json.loads((out/'PRIMARY_RESULT.json').read_text())
    for key in ['N_events','G_reviews','df','primary_total45_mean','primary_SE_review_means',
                'primary_CI95','descriptive_day_EDminus1_mean','descriptive_other44_mean']:
        if actual[key] != expected[key]: raise AssertionError(f'Primary replay mismatch: {key}')
    validation['primary_headlines_identical'] = True
(out/'PORTABLE_REPLAY_VALIDATION.json').write_text(json.dumps(validation, indent=2)+'\n')
print(json.dumps(validation, indent=2))
