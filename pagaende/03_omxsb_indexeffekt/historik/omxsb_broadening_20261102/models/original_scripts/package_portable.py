from pathlib import Path
import shutil,json,hashlib,difflib
C=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;S=C/'work/broadening_models_portable_20261102';code=S/'code/build/omxsb_broadening_20261102/models';out=S/'output/omxsb_broadening_20261102/models';code.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
for p in O.iterdir():
 if p.is_file() and p.suffix!='.py':shutil.copy2(p,out/p.name)
archive=out/'original_scripts';archive.mkdir(exist_ok=True)
for p in O.glob('*.py'):shutil.copy2(p,archive/p.name)
R=Path('/Users/ludviguvang/dev/financethesis')
import pandas as pd
pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',usecols=['event_id','diff3_1']).to_csv(out/'frozen_outcome_input.csv',index=False)
prefix="""import argparse
P=argparse.ArgumentParser();P.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[4]);P.add_argument('--out',type=Path);A=P.parse_args();R=A.repo.expanduser().resolve();O=(A.out or R/'output/omxsb_broadening_20261102/models').expanduser().resolve();O.mkdir(parents=True,exist_ok=True)
"""
changes=[]
for name in ['compare.py','verify.py']:
 src=(O/name).read_text();ported=src.replace("O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');",prefix)
 ported=ported.replace("lock['files'][str(O/'feature_gate_all216.csv')]","next(h for p,h in lock['files'].items() if Path(p).name=='feature_gate_all216.csv')")
 ported=ported.replace("R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv'","O/'frozen_outcome_input.csv'")
 if name=='verify.py':
  i=ported.index('# Sanity masking:');j=ported.index('# Unit algebra,')
  ported=ported[:i]+"# Prior raw-source sanity audit is frozen; this replay verifies its saved counts only.\nmasked=pd.read_csv(O/'pre_returns_sanity_masked_values.csv').to_dict('records');counts=pd.read_csv(O/'pre_returns_sanity_counts_all216.csv');assert len(counts)==216 and counts.newly_masked.sum()==len(masked)\n"+ported[j:]
  ported=ported.replace("'gate_hash_unchanged':True","'gate_hash_unchanged':True")
 (code/name).write_text(ported);changes.append('\n'.join(difflib.unified_diff(src.splitlines(),ported.splitlines(),fromfile='original/'+name,tofile='portable/'+name)))
(out/'PORTABLE_PATH_CHANGES.diff').write_text('\n\n'.join(changes)+'\n')
inputs=['feature_gate_all216.csv','DESIGN_LOCK.json','DECISIONS.txt','frozen_outcome_input.csv','pre_returns_sanity_counts_all216.csv','pre_returns_sanity_masked_values.csv'];(out/'FROZEN_PORTABLE_INPUT_HASHES.json').write_text(json.dumps({n:hashlib.sha256((out/n).read_bytes()).hexdigest()for n in inputs},indent=2))
(out/'PORTABLE_README.txt').write_text('''Kopiera code/build/omxsb_broadening_20261102/models och output/omxsb_broadening_20261102/models till repo med samma relativa paths.
Kör python REPO/code/build/omxsb_broadening_20261102/models/compare.py --repo REPO [--out OUTPUTFOLDER]
Kör sedan python REPO/code/build/omxsb_broadening_20261102/models/verify.py --repo REPO [--out OUTPUTFOLDER]
Defaultoutput är REPO/output/omxsb_broadening_20261102/models. Med --out ska den sparade katalogens innehåll redan finnas där.
Replay läser frysta feature_gate_all216 och frozen_outcome_input; ingen ny primärdatagrind eller råpanel behöver läsas. Tidigare raw-source sanitycheck bevaras som fryst räknelogg; portableverify räknar inte om råkällans värden. DESIGN_LOCK och DECISIONS är byteidentiska, gamla absoluta paths inne i proveniens-JSON är historiska och används inte för filåtkomst. Originalets prepare/compare/verify ligger i original_scripts. Inga ekonomiska specifikationer ändrades. Numpy,pandas,scipy,statsmodels behövs. Resultatjämförelse finns i PORTABLE_REPLAY_VALIDATION.json efter den verifierade stagingkörningen.
''')
print(S)
