#!/usr/bin/env python3
"""Relocate hashed inputs only; execute the unchanged, locked estimator."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

ap=argparse.ArgumentParser()
ap.add_argument('--repo-root',type=Path,required=True)
ap.add_argument('--gate-dir',type=Path,required=True)
ap.add_argument('--package',type=Path,default=Path(__file__).resolve().parent)
ap.add_argument('--replay-root',type=Path)
ap.add_argument('--check-only',action='store_true')
a=ap.parse_args();R=a.repo_root.resolve();G=a.gate_dir.resolve();P=a.package.resolve()
orig=P/'DESIGN_LOCK.json';lock=json.loads(orig.read_text())
assert sha(P/'run_overlap.py')==lock['script_sha256']
mapping={'spec':P/'PROPOSED_TEST.txt','source_width':P/'ROLE_SOURCE_WIDTH.csv',
 'source_precision':P/'EVENT_ONLY_SOURCE_PRECISION.json',
 'q1_ledger':R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz',
 'raw_positions':G/'private/RAW_RELEVANT_POSITIONS.csv.gz','scaling_inputs':G/'private/SCALING_INPUTS.csv'}
for n in ['EVENT_SOURCE_GATE.csv','ELIGIBLE_FUNDS.csv','FROZEN_ROLES.csv','SECURITY_SOURCE_GATE.csv','GATE_RESULT.json']:
 mapping[n]=G/n
assert set(mapping)==set(lock['inputs'])
for k,p in mapping.items():
 assert sha(p)==lock['inputs'][k]['sha256'], ('input_hash_mismatch',k)
 lock['inputs'][k]['path']=str(p)
lock['portable_replay_original_design_lock_sha256']=sha(orig)
lock['portable_replay_path_changes_only']=True
lock['portable_replay_prior_results_known']=True
lock['inherited_execution_lock_false_pre_read_flag_is_not_evidence_of_replay_blindness']=True
if a.check_only:
 print(json.dumps({'all_input_hashes_match':True,'inputs':len(mapping),'locked_estimator_hash_matches':True,'q2_values_parsed':False,'outcomes_recomputed':False},indent=2))
else:
 if a.replay_root is None:ap.error('--replay-root NEW_DIRECTORY required')
 if a.replay_root.exists():raise RuntimeError('Replay root must be new')
 O=a.replay_root.resolve();O.mkdir(parents=True)
 lp=O/'RELOCATED_DESIGN_LOCK.json';lp.write_text(json.dumps(lock,indent=2)+'\n')
 (O/'REPLAY_STATUS.json').write_text(json.dumps({'replay_after_known_results':True,'original_study_exploratory_after_F35':True,'unchanged_estimator_execution_lock_pre_read_flag_is_inherited_not_blindness_evidence':True,'original_design_lock_sha256':sha(orig)},indent=2)+'\n')
 subprocess.run([sys.executable,str(P/'run_overlap.py'),'--repo-root',str(R),'--gate-dir',str(G),'--output',str(O/'outcomes'),'--design-lock',str(lp)],check=True)
