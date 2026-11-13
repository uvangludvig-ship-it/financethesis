from pathlib import Path
import ast,shutil,json,hashlib,difflib,datetime
C=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');S=C/'work/volume_full_package_staging_20261102';code=S/'code/build/omxsb_followup_20261102/volume_units_full_20261102';out=S/'output/omxsb_followup_20261102/volume_units_full_20261102';code.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
archive=out/'archived_original_work';archive.mkdir(exist_ok=True)
for f in O.iterdir():
 if not f.is_file() or f.name=='build_portable_staging.py':continue
 shutil.copy2(f,archive/f.name)
 if f.suffix!='.py':shutil.copy2(f,out/f.name)
# Also preserve this packaging script separately; never part of the scientific replay.
shutil.copy2(Path(__file__),archive/Path(__file__).name)
src=(O/'run_frozen_volume.py').read_text()
old="O=Path(__file__).resolve().parent;C=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis')\nsys.path.insert(0,str(C/'work/comparison_rebuild_20261102'))\nfrom run import fieller"
new="import os\nR=Path(os.environ.get('OMXSB_REPO',Path(__file__).resolve().parents[4])).expanduser().resolve()\nBASE=Path(os.environ.get('OMXSB_FOLLOWUP_OUTPUT',R/'output/omxsb_followup_20261102')).expanduser().resolve()\nO=BASE/'volume_units_full_20261102';O.mkdir(parents=True,exist_ok=True)\nfrom frozen_fieller import fieller"
assert old in src;ported=src.replace(old,new)
ported=ported.replace("lock['files'][str(O/'unit_gate_all216.csv')]","next(h for p,h in lock['files'].items() if Path(p).name=='unit_gate_all216.csv')")
ported=ported.replace("newpath=C/'work/mandate_upgrade_20261102/event_demand_updated.csv'","newpath=O/'inputs/event_demand_updated.csv'")
(code/'run_frozen_volume.py').write_text(ported)
fs=(C/'work/comparison_rebuild_20261102/run.py').read_text();fnode=next(n for n in ast.parse(fs).body if isinstance(n,ast.FunctionDef) and n.name=='fieller');func=ast.get_source_segment(fs,fnode);(code/'frozen_fieller.py').write_text('"""Byte-identical Fieller function from the frozen original comparison script."""\nimport numpy as np\nfrom scipy.stats import t\n\n'+func+'\n')
(out/'inputs').mkdir(exist_ok=True);shutil.copy2(C/'work/mandate_upgrade_20261102/event_demand_updated.csv',out/'inputs/event_demand_updated.csv')
files=['data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet','data/raw/lseg/panel_2005_2026/indices_daily (1).csv','output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz','output/omxsb_mechanism_frontier_20261102/demand/event_demand_by_definition.csv']
manifest=dict(repo_inputs={p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in files},local_inputs={p:hashlib.sha256((out/p).read_bytes()).hexdigest()for p in ['unit_gate_all216.csv','UNIT_GATE_LOCK.json','DECISIONS.txt','QA_AMENDMENT_BEFORE_ASSOCIATIONS.txt','inputs/event_demand_updated.csv']},archive={str(f.relative_to(archive)):hashlib.sha256(f.read_bytes()).hexdigest()for f in archive.rglob('*')if f.is_file()},frozen_fieller_function_sha256=hashlib.sha256(func.encode()).hexdigest())
(out/'PORTABLE_INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2));(out/'path_only_code_changes.diff').write_text('\n'.join(difflib.unified_diff(src.splitlines(),ported.splitlines(),fromfile='original/run_frozen_volume.py',tofile='portable/run_frozen_volume.py'))+'\n');(out/'PORTABILITY_LOG.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),original_directory=str(O),staging=str(S),only_operational_paths_and_import_changed=True,fieller_function_identical=True,unit_gate_rebuild=False,scientific_specification_change=False,original_scripts_preserved_in='archived_original_work',frozen_inputs_byte_identical=True),indent=2))
print(S)
