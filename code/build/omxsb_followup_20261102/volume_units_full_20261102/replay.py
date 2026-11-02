"""Replay associations only, using byte-preserved frozen gate and input data."""
from pathlib import Path
import argparse,os,sys,subprocess,json,hashlib,datetime
import pandas as pd,numpy as np
C=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(os.environ.get('OMXSB_REPO',C.parents[3])));p.add_argument('--output',type=Path);a=p.parse_args();R=a.repo.expanduser().resolve();B=(a.output or R/'output/omxsb_followup_20261102').expanduser().resolve();O=B/'volume_units_full_20261102';A=O/'archived_original_work'
m=json.loads((O/'PORTABLE_INPUT_MANIFEST.json').read_text());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name,h in m['repo_inputs'].items():assert sha(R/name)==h,('Input differs; stop before replay',name)
for name,h in m['local_inputs'].items():assert sha(O/name)==h,('Frozen local input differs',name)
for name,h in m['archive'].items():assert sha(A/name)==h,('Archive differs',name)
started=datetime.datetime.now(datetime.timezone.utc).isoformat();env=os.environ.copy();env.update(OMXSB_REPO=str(R),OMXSB_FOLLOWUP_OUTPUT=str(B))
with (O/'portable_replay.log').open('w')as stream:r=subprocess.run([sys.executable,str(C/'run_frozen_volume.py')],cwd=R,env=env,stdout=stream,stderr=subprocess.STDOUT)
assert r.returncode==0,('Replay failed; inspect portable_replay.log',r.returncode)
checks=[]
for name in ['volume_input_all216.csv','joined_quantities_volume_all216.csv','volume_quantity_ratios.csv','diagnostic_slopes.csv','review_level_means.csv']:
 x=pd.read_csv(A/name);y=pd.read_csv(O/name);assert list(x)==list(y) and x.shape==y.shape,('Shape/schema differs',name);maxerr=0.
 for c in x:
  if pd.api.types.is_numeric_dtype(x[c])and pd.api.types.is_numeric_dtype(y[c]):
   assert np.allclose(x[c],y[c],equal_nan=True,atol=1e-10,rtol=1e-10),(name,c)
   v=(x[c].astype(float)-y[c].astype(float)).abs();maxerr=max(maxerr,float(v.max())if v.notna().any()else 0.)
  else:assert x[c].fillna('__NA__').equals(y[c].fillna('__NA__')),(name,c)
 checks.append(dict(file=name,rows=len(x),max_abs_error=maxerr,byte_identical=sha(A/name)==sha(O/name)))
for name,h in m['local_inputs'].items():assert sha(O/name)==h,('Frozen input modified',name)
for name,h in m['archive'].items():assert sha(A/name)==h,('Original archive modified',name)
result=dict(completed=True,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),no_gate_rebuild=True,no_specification_change=True,all_locks_and_original_archive_unchanged=True,repo=str(R),output=str(O),checks=checks)
(O/'PORTABLE_REPLAY_VALIDATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
