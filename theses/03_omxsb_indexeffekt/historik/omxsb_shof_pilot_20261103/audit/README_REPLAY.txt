Source metadata pilot only, no thesis prose or economic outcomes.
Runtime:/Users/ludviguvang/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
Requires pandas,numpy. Raw files remain private, unchanged:
Valuations:/Users/ludviguvang/dev/financethesis/data/raw/shof/Valuations/pilot_20261103/FUNDS_VALUATIONS_1793724895212.zip
RIPS:/Users/ludviguvang/dev/financethesis/data/raw/shof/Reinvestments/pilot_20261103/FUNDS_RIPS_1793724775329.zip

Run in this folder, in order:
1.validate_acquisition_pilot.py --valuations [pathabove] --rips [pathabove]
2.compare_source_histories.py --valuations [pathabove] --rips [pathabove]
3.audit_vendor_nf_presence.py --valuations [pathabove]
4.finalize_metadata.py

Input ID/class metadata copied from the prior frozen20classpilot manifest. Old source comparison reads repository monthly Valuations/RIPS, dates restricted2017..2023. Scripts save metadata/flags only; downloaded numerical NF/TNA/TRI series never leave private raw files in publication output.

ExactNFreplication flags are deliberately retained, but all1651SEB51331differences are belowrelative1e-8; finalsummary distinguishes floatingprecision from substantive conflict. Presence-only24monthcounts are separate from exactduplication-gatecounts. No copiedfundNFvalues are summed.

Supplementary RIPS_OLD_NEW files are preliminary metadata counts. Final25endpoint results are reproduced bycompare_source_histories.py. Source flags/private month-level metadata and failed-run archive are excluded from public package by default. Do not overwrite the older design-frontier audit; this is a newsourceversion.
