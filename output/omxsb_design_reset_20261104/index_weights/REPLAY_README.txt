The four-query pilot has completed. Do not rerun it as a source-availability
search without a newly documented reason. REQUEST_LOCK.json freezes the exact
four requests and source hashes; SOURCE_RESULTS.json retains every response.

probe_root_chain.py requires pandas, numpy and lseg-data and the already
authorized local Workspace DesktopSession. It supplies no credentials or key.
It refuses to overwrite REQUEST_LOCK.json. To reproduce an acquisition, copy
code/spec to a new directory, retain access to the hash-identified previous
source references, and explicitly record that this is a replay after known
blank responses. Four queries only; no retry/field-fishing loop.

verify_source_results.py uses only standard-library CSV parsing and local
private response files, not the SDK. It verifies empty fields, hashes, row
counts and alignment with independently verified historical/current member
references. Adapt the reference ROOT paths when replaying elsewhere, retaining
the original hashes. No price or economic statistic is computed.

capture_primary_sources.py saves already-read public provider documents into
private/source_documents. The public ledger has URLs/status/hashes; original
third-party text is excluded from redistribution.

All private raw membership lists, weights/shares payloads, full source documents
and SDK environment remain outside the publication allowlist. No thesis prose.
