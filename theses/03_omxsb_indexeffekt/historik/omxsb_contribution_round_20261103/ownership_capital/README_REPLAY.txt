Ownership/capital contribution round, 3November2026. Read REPORT.txt first.
Root directory: /Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/contribution_round_20261103/ownership_capital
Repo read-only inputs: /Users/ludviguvang/dev/financethesis
Python used: .venv/bin/python inside this working directory; requirements.txt records pandas/numpy/scipy/pyarrow versions. The parent's supplied /tmp venv did not exist; the bundled runtime lacked scipy. Environment is local only, do not publish .venv.

Replay from this working folder after obtaining lawful access to the named source files:
1. python gate.py
2. python run.py
3. python verify.py
4. python raw_control_check.py
5. python descriptive.py
6. python write_report.py
No downloads, network calls, repository writes or FTN outcomes are needed.
FINANCETHESIS_REPO overrides repo path in gate/run/verify. Other helper scripts contain the explicit documented local repo path at top; change that one Path for another computer. The derived canonical FI long file and previous gate/identity ledgers are dependencies, not rebuilt from raw in this small package. raw_input_map.csv explains their provenance; raw_control_check.py independently parses selected original full XML reports. This package is a bounded extension, not a claim to rebuild the entire thesis from scratch.

Reading outputs:
primary_contrast.csv: sole primary additioncontrast, newminuspreexisting, reviewtCI.
addition_reading_table.csv: event/control/additive accounting.
addition_benchmark_components.csv: descriptive benchmark decomposition.
same_support_counts_capital.csv: requested post-primary same-support count/capital comparison.
normalized_fund_role_contributions.csv.gz: derived normalized percentage-point contributions; no raw quantity,price,marketcap.
all_company_contributions.csv: all69legalcompanynames; descriptive,noomissions.
event_component_results.csv and review_component_results.csv: complete arithmetic inputs to means.
summary.csv: complete descriptive/support summaries; is_primary=True identifies sole primary. No p-values or search over specifications.
fund_support.csv and event_feasibility_gate.csv: symmetrical support/exclusions; no rematching.

Audit:
DESIGN_LOCK, GATE_AMENDMENT, QA_REPORT_SUPPORT_CORRECTION, POST_PRIMARY_DESCRIPTIVE_ADDENDUM document actual chronology.
GATE_HISTORY records exact184-to185change and harmless reasons-column correction.
ANALYSIS_LOCK is retained from before main economic aggregates. run_before_ledger_export.py has its original code. Current run.py adds only fund_id/ledger export and writes REPLAY_LOCK without replacing firstlock.
independent_validation.json: different arithmetic/code pathway by same agent.
raw_control_validation.json: direct rawXML-to-derived checks for fixedtwofunds.
A separately delegated analyst also audited every fundrole/component; its report is outside this folder and delivered to parent.
failed_first_run.log and failed_verifier_id_parse.log record caught issues. No unsuccessful economic variants were discarded.

Publishing:
Use publication_allowlist.json. It explicitly excludes .venv, original raw/licensed data, raw price/quantity/mcap diagnostics, fulltexts, and the local diagnostic GATE_HISTORY.txt containing one licensed rawshares example. REPORT.txt records the same gate explanation without the licensed raw counts. raw_input_map.csv contains only input locations/field names/hashes. Original XML map is source metadata, not full text. Licensed sources are required independently for reproduction and are never bundled.

All results exploratory. Fixed controls can already be indexmembers; entry/exit means quarterly observed statuses. No causal priceeffect or trade-level identification, no first-ever methodological claim, no AI-written thesis text. Repo owner handles the required AI-log entry.
