Source-method audit only. Read SOURCE_RULE_D.txt and then SOURCE_STATUS_UPDATE.txt. Keep older strict23/50source gate unchanged; report anyDgate separately with its provisional/verified labels.

D implemented: D_RESULTAT_KORT.txt and D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv. Replay with the same runtime: python build_D_eligibility.py. This reads numeric capital and FX only for source reconciliation, and uses TRI/NAV only for presence/positivity; no return, flow or covariance is calculated. D_ENDPOINT_SOURCE_FLAGS.csv gives dates/flags only. D_FINAL_CHECK.json records an independent reaggregation and final eligibility CSV hash. NativeRIP29/50 and conditionalNAVinclusive46/50 must remain separately labelled. The initial overly restrictive fund-currency implementation is archived with its source-only outputs.

evidence.csv contains six relevant class identities, currencies, inception and distribution flags plus prior source-presence dates. METADATA_AUDIT.json independently verifies NAV/FX source extent without calculating returns/flows/risk. Exact source hashes are included there.

Replay metadata only:
/Users/ludviguvang/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 check_source_metadata.py
Requirespandas/openpyxl. Reads existing files at fixedlocalpaths; writes only thisfolder. Doesnotdownload anything. No flow/return/covariance arithmetic.

Primary dated inception source: https://www.storebrand.se/am/fonder/fondhandelser/ (2022-05-12 section, exactthreeISINs recorded in rule).
Current Access distribution support: https://swedbankrobur.fondlista.se/sv/details/SE0007074075 . Not historical proof.
Definitions: /Users/ludviguvang/dev/financethesis/data/raw/shof/shof_field_definitions.txt and pairedPDF, especiallypp4–5,19,21,23–24,27; not republished.

All files in thisfolder are derivedmetadata/code/technicalnotes, with no rawlicensed numerical series or copiedfulltexts. No repoedits, commits, pushes, FTNoutcomes, or thesistext.
