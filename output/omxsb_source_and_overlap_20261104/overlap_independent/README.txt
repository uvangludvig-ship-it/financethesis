Independent replay of the frozen, event-only q1-to-q2 endpoint-overlap bounds.

Read REPORT_SV.txt first. Authoritative machine outputs are in independent_replay/.
COMPARISON.json reports equality with producer aggregates after independent
reconstruction. BASELINE_REPORT_CHECK.json separately checks all original
q0/q1 report-presence/fund-identity cells without reading new q2 quantities.

replay.py uses the Python standard library. It imports no producer functions.
It reads the original ownership-capital ledger and older F35 quantity/scaling
files at the local absolute paths listed in independent_replay/INPUT_LOCK.json.
The licensed/private inputs are deliberately not included. Local reproduction
requires lawful access to those exact hash-matched input files. The hardcoded
repository/work paths must resolve to the original local inputs.

This frozen audit script is NOT portable from a copied repo/output/ directory:
it resolves the original chat root relative to its own file location. Execute
the original script at
/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/omxsb_shof_continue_20261104/overlap_independent/replay.py
inside the original workspace. No relocated execution has been tested or
promised. A published copy documents the audit; it does not bundle its inputs.

Execution example from the original chat root:
python3 work/omxsb_shof_continue_20261104/overlap_independent/replay.py --output NEW_DIRECTORY

The script rejects existing output directories. Do not replace the original
independent_replay/ files. check_baseline_reports.py is a separate metadata
audit and likewise rejects replacement of its first output.

PUBLICATION_ALLOWLIST.json is the exact list of distributable relative file
paths. PUBLICATION_SHA256.json hashes every allowlisted file except itself.
Only code, audit text, source hashes and event/review/overall aggregates are
included. No FI fund-level quantity/value rows, copied private sources, full
source documents, API credentials or peer economic statistics are included.

Terminology: complete in one frozen JSON field means the existing nonempty-
report support rule, not independently proven exhaustive reporting. See
REPORT_SV.txt. This clarification does not revise the first calculation.
