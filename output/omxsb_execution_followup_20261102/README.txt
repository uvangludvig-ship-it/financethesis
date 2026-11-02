OMXSB execution/demand follow-up, 2 November2026. Technical outputs only.
Read REPORT.txt for results, limitations and what changed.

Code from repo root:
python code/build/omxsb_execution_timing_20261102.py
python code/build/omxsb_execution_announced_20261102.py
python code/build/omxsb_execution_controls_20261102.py

The first script reproduces the preserved completed-event v1, not the corrected headline population. v2_announced is the corrected raw-final-list-plus-known-reversals population. fixed_controls is a smaller conditional diagnostic; compare its market and control metrics on exactly its same rows. Never join different Ns as if they were the same strategy.

Requirements: pandas,numpy,scipy,pyarrow; independent audit uses statsmodels. Existing local environment /tmp/omxsb-audit-venv/bin/python was used, not a dependency on that absolute path. Licensed stock/index inputs are required locally and not shipped. All analysis paths resolve from the repo code location.

Demand: demand/README.txt and REPORT.txt. The unchanged executable is also copied to code/build/omxsb_execution_demand_20261102.py; its frozen byte hash is preserved. To replay into a NEW directory, copy DECISIONS.txt and ANALYSIS_LOCK.json first and pass --repo and --out. Do not refreeze the original. verify.py and coverage_scope.py are in demand/. PUBLIC_EXPORT_NOTE.txt lists locally regenerable vendor-valued diagnostics excluded from publication.

Cost: cost_audit/audit_t29.py --repo REPO --out NEW_OUTPUT. cost_audit/verify_audit.py provides independent accounting checks. This reproduces a conditional scenario and audit, not official weights or actual fund cost. Read cost_audit/REPORT.txt.

Sources: sources/SOURCE_AND_METHOD_AUDIT.txt, source_ledger.json, known_cancellations.csv, announcement_date_checks.json, 2020H2_primary_update.json. The later2020H2 update resolves its primary-text gap without changing the date. Initial18-review notice-history coverage remains explicitly incomplete. Copyright fulltexts are kept outside the repo.

Chronology: PLAN_LOCK.json precededv1. ADDENDUM_CANCELLATIONS.json followedv1 and precededcancellation outcomes. ADDENDUM_RAW_COHORT.json removes upstream future-delisting/history selection. ADDENDUM_FIXED_CONTROLS.json followedv2 and preceded this new control horizon. All are exploratory; actual timestamps and commits do not make already-seen evidence blind.

No original analysis or raw input was overwritten. User edits outside this new tree are separate. No FTN outcome or thesis prose was generated.
