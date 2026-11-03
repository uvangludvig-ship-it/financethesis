Runda 11 audit — 2026-11-03

Start with REPORT_SV.txt. This is a technical analysis package, not thesis prose.
Known historical results were read before specification; no blind-registration claim.
SPEC_20261103.txt and LOCK.json precede new numerical work.

Read-only repository: /Users/ludviguvang/dev/financethesis
Audited Runda 11 commit: 3ff0da7; its audited code/results are unchanged at current HEAD 48c6ad3.
All new writes are inside this directory. No repo edits, commit or push.

Reproduce from this directory:
  ./.venv/bin/python audit.py
  ./.venv/bin/python verify_price_and_units.py
  ./.venv/bin/python verify_endpoint_and_fieller.py

Python and package versions are recorded in requirements_versions.json.
Existing /tmp/omxsb-audit-venv was absent; a local isolated environment was created here.
The three scripts use only local data. No FTN outcome file is opened.

Main outputs:
  r11_coverage_summary.csv — new Runda11 sample counts, with/without controls
  r11_event_coverage_audit.csv — derived event-level coverage and exact D replay
  r11_split_screen_unit_diagnostic.csv — old exact FI/LSEG endpoint comparisons intersected with R11 screen
  r11_unit_summary.csv — positive, unique matches only; all_r11 includes 294 matching endpoints
  r11_historical_classification_diagnostic.csv — current-name history/classifier evidence
  r11_full_fieller_diagnostic.csv — all 16 inference-diagnostic confidence sets; unrepaired D
  r11_raw_price_split_checks.csv — raw-panel prices, denominator and split-screen verification
  fieller_inversion_checks.csv — scalar cluster-t inversion QA
  DATA_BLOCKERS.csv, SOURCE_FIELD_PILOT_CASES.csv — precise missing-evidence requirements and targeted cases

The existing source-field pilot, not rerun or claimed complete, is:
  /Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/omxsb_execution_demand_20261102/lseg_complement_pilot.py
Its candidate field provenance is documented in that directory's LSEG_SOURCE_NOTES.txt.
Successful extra quantity fields do not prove full portfolio completeness or historical mandates.

Confidentiality/publication:
No entire licensed raw file is copied into this folder. Derived audit tables are retained;
their permitted external distribution must follow the source license. Do not package .venv,
raw source paths as data files, or full LSEG/FI endpoint source tables. The scripts/derived
aggregate audit are separable from raw inputs. No copyrighted article text is present.
