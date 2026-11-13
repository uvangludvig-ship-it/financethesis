Bounded methodological and source review, no new q2 outcomes.

Read LAGR_SOURCE_REVIEW_SV.txt for the latest source decision, then
DESIGN_REVIEW_SV.txt and FORMAL_SPEC.txt for the proposed incremental question.
The latter files preserve the initial proposal before the subsequent q0 audit.
METADATA_AUDIT.json confirms fixed cohorts and old source failure flags.
LAGR_Q0_DIAGNOSTIC.json documents the q0-only split and denominator checks.

Current status: source-based split explanation found; all70 bounds in the
proposed companywide q0-capital unit remain blocked on denominator semantics.
No q2 support upgraded, no source threshold relaxed, no new outcome computed.

Reproduction needs original licensed local sources at paths in the input
hash records. metadata_audit.py uses standard Python; audit_lagr_q0.py uses
pyarrow (local audit version 26.0.1) and an exact RIC/date parquet filter.
The scripts refuse to replace their first output. They are audit records
with explicit original-workspace paths, not a portable data bundle.

PUBLICATION_ALLOWLIST.json is an exact relative file list.
PUBLICATION_SHA256.json hashes each listed file except itself.
Exclude .venv/, private/ and all copied full-text sources, raw market values,
prices, quantities and source snapshots. Only code, metadata, source URLs and
hashes, diagnostic ratios and written design/source findings are public.
