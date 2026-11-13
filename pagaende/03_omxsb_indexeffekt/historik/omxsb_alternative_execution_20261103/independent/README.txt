Independent replay, finalized 2026-11-03.

Requires Python 3.9+ with the standard library (zoneinfo/Decimal included), original licensed SHoF files under REPO/data/raw/shof/Reinvestments/hft_pilot_20261103 and the ignored index_sources/private and auction_source/private source CSVs. No network or authenticated API is called by the two verification scripts. No private numeric source observations are written to their outputs.

Run from any working directory, using the actual path to the scripts:
python independent/verify.py --repo-root /path/to/financethesis --include-auction --output /path/to/new_source_verification.json
python independent/verify_primary.py --repo-root /path/to/financethesis --output /path/to/new_arithmetic_verification.json

When scripts are packaged below the repository, the repository is inferred from its ancestor data/input/omxsb directory. Otherwise the original workstation repository is the fallback. --repo-root overrides that fallback and remaps recorded original repository paths. LSEG private files are resolved relative to the package's sibling folders. Omit --output to create a uniquely timestamped replay JSON beside the script. Existing output paths are rejected; frozen audit files are never overwritten.

Frozen final evidence:
- PRIMARY_ARITHMETIC_VERIFICATION.json: independent Decimal/source-gate reconstruction of the four daily AP values and two signed contrasts. Four original events remain, two 2019 NA. Differences only, no raw prices/midpoints/sizes.
- SOURCE_AND_PUBLICATION_VERIFICATION.json: final source hashes/counts, index controls, five books, eight daily/five minute queries, NMQ CRC/schema and final producer allowlist/hash checks.
- REPORT_SV.txt: final interpretation, limitations and publication boundary.

Historical evidence retained:
- SOURCE_VERIFICATION_PRE_AP.json: source-only replay before independent AP reconstruction; its pending publication flags are historical and superseded by SOURCE_AND_PUBLICATION_VERIFICATION.json.

PUBLICATION_ALLOWLIST.json has eight exact relative paths. Its own hash is omitted to avoid a circular definition. All unlisted files are excluded, including the older provisional VERIFICATION.json, intermediate replay logs and __pycache__. Original/private licensed data and full third-party texts are never included. The reader needs their own authorized source access to replay numerical checks.
