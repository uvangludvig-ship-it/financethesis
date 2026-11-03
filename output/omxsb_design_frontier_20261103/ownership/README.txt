Baseline-only design audit, 2026-11-03

Start with REPORT_SV.txt. FRAGILITY_REDTEAM.txt is the separately assigned conceptual follow-up. Neither is thesis prose. No new post-event economic outcomes were loaded/calculated by these scripts. Repository inputs are read only; all outputs remain here.

Run from any directory, in order:
  python /absolute/path/to/ownership/baseline.py
  python /absolute/path/to/ownership/seb_baseline_support.py
Dependencies: pandas and numpy. The scripts use absolute local input locations listed in input_map.csv. On this machine a compatible existing executable is:
/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/contribution_round_20261103/ownership_capital/.venv/bin/python
Do not run both scripts simultaneously: the second reads the first's generated metadata.

Key tables:
baseline_overlap_summary.csv / baseline_overlap_by_company.csv: metadata screens, not active certification.
seb_baseline_support_summary.csv / seb_baseline_by_review.csv: narrowly mapped SEB support and preholdings.
fund_mandate_evidence.csv: seven candidate funds, FI ID/ISIN, dated primary source, manager/sleeve and historical limits.
source_ledger.csv: exact URLs, dates and selective read scope; no full texts copied.
input_map.csv: existing derived inputs, precise columns opened, SHA256.

Other tables are baseline or availability-key ledgers to replay the aggregates. They contain no post holdings, position changes, raw stock prices, company market caps or fund flow amounts. The old common-support availability flag was obtained from keys only in an earlier validated derived ledger; it does not recalculate or improve those economic outcomes.

Uncertainty labels matter. conditional_continuity_screen_NOT_certification removes IDs with index-near evidence in at least one period; it does not certify full-history active labels. Seven SEB candidates have 2019 active descriptions, not complete 2019–25 dated certification. unresolved_2019_SIX60_removed is the defensible current SEB baseline, excluding FI/issuer benchmark disagreement. No final analysis sample is approved.

Archival relation: baseline_initial_1615.py and BASELINE_RUN_initial_1615.json preserve the first run before an overstrong screen label was corrected. Main baseline aggregate numbers did not change; label/interpretation did. The seven-ID exploratory roster in seb_baseline_support.py also reports the unresolved conflict-inclusive screen, but the report uses the conflict-removed screen only. This is a baseline evidence correction, not outcome-based subset choice.

Publication allowlist if root elects to publish: REPORT_SV.txt, FRAGILITY_REDTEAM.txt, README.txt, baseline.py, seb_baseline_support.py, fund_mandate_evidence.csv, source_ledger.csv, input_map.csv, BASELINE_LOCK.txt, BASELINE_RUN.json, SEB_SUPPORT_RUN.json, baseline_overlap_summary.csv, baseline_overlap_by_company.csv, seb_baseline_support_summary.csv, seb_baseline_by_review.csv. Local absolute paths may be generalized for portability while preserving relative input identity/hash.
Do not copy underlying licensed LSEG/Morningstar/vendor data, raw prices/market caps/flows or full copyrighted PDFs. No source full texts are stored in this folder. The larger baseline-key tables are local audit material, not necessary for a public report.

AI log: root must record the same-day design audit in its authorized log location. This subtask did not edit repo/PLAN/AI_LOG, commit, push, or touch FTN outcomes.
