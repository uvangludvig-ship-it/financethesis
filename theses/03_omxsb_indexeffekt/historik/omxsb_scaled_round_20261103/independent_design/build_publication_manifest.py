#!/usr/bin/env python3
"""Explicit public subset. No licensed raw/scaling/position input is copied."""
from pathlib import Path
import datetime,hashlib,json
P=Path(__file__).resolve().parent
FILES='''LOCK.json
README.txt
REPORT_SV.txt
REPORT_PRE_SOURCE_GATE_SV.txt
build_inventory.py
ANALYSIS_FAMILY_MATRIX.json
ANALYSIS_FAMILY_MATRIX.txt
SOURCE_READ_LEDGER.json
verify_source_coverage.py
COVERAGE_REVIEW.json
build_publication_manifest.py
archive_before_current_round/build_inventory.py
archive_before_current_round/ANALYSIS_FAMILY_MATRIX.json
archive_before_current_round/ANALYSIS_FAMILY_MATRIX.txt
archive_before_current_round/SOURCE_READ_LEDGER.json
retention/DESIGN_LOCK.txt
retention/DESIGN_LOCK_V1_OVERBROAD_DATE.txt
retention/Q0_TIMESTAMP_GUARD_AMENDMENT.txt
retention/RUNTIME_CORRECTION.txt
retention/gate.py
retention/run.py
retention/GATE_START_LOCK.json
retention/GATE_RESULT.json
retention/GATE_OUTPUT_HASHES.json
retention/SECURITY_SOURCE_GATE.csv
retention/EVENT_SOURCE_GATE.csv
retention/FROZEN_ROLES.csv
retention/ELIGIBLE_FUNDS.csv
retention/FUND_REPORT_SUPPORT.csv.gz
retention/INVALID_FUND_UNITS.csv
retention/CANCELLED_CONTROL_EXCLUSIONS.csv
retention/BASELINE_KNOWN_CAPITAL_COVERAGE.csv
retention/SUBSEQUENT_OMXSB_FLAGS.csv
retention/OUTCOME_LOCK.json
retention/PRIMARY_RESULT.json
retention/NORMALIZED_NEW_COHORT_LEDGER.csv.gz
retention/EVENT_LEVELS.csv
retention/REVIEW_LEVELS.csv
retention/JOINT_COVARIANCE_OF_MEANS.csv
retention/REPORT_SV.txt
retention/README_REPLAY.txt
retention/INDEPENDENT_VALIDATION_POINTER.json
retention/archive_before_q0_timestamp_guard/gate.py
retention/archive_before_q0_timestamp_guard/GATE_START_LOCK.json
retention/archive_before_q0_timestamp_guard/GATE_RESULT.json
retention/failed_runtime/GATE_START_LOCK.json'''.splitlines()
def main():
 out=P/'PUBLICATION_ALLOWLIST.json'
 if out.exists():raise RuntimeError('Publication list is frozen; do not overwrite it. Explicitly version an amendment if needed.')
 hashes={}
 for n in FILES:
  f=P/n
  if not f.is_file():raise FileNotFoundError(f)
  if any(x in f.relative_to(P).parts for x in ['private','.venv','__pycache__']):raise ValueError(n)
  hashes[n]=hashlib.sha256(f.read_bytes()).hexdigest()
 obj={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Public technical design inventory plus one source-gated retention outcome; originals preserved','files':FILES+['PUBLICATION_ALLOWLIST.json'],'sha256':hashes,'manifest_self_hash':'Intentionally omitted to avoid recursive self hash','excluded':['Every private/ subtree, including archived ones','RAW_RELEVANT_POSITIONS.csv.gz and SCALING_INPUTS.csv','Licensed raw prices, NAV, TRI, TNA, dividend amounts, fund quantities and market capitalizations','Credentials, email bodies, full source texts, runtime environments, caches','Any file not explicitly listed'],'interpretation':'Derived normalized pp ledger/aggregates are allowed; source quantities and prices are not. Historical gate/inventory versions are not independent economic tests.'}
 out.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'files':len(obj['files']),'hashes':len(hashes),'allowlist_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
