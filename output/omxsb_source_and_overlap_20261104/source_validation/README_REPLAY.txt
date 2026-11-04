Current decision: FINAL_SOURCE_NOTE_SV.txt. Five fixed sampled/full-book days verified; no new economic outcomes. Two-day files are preserved chronological diagnostics.

Requires Python 3 with pandas/numpy for the existing predeclared validator. Independent compare_bins.py, inventory_delivery.py and compare_overlap.py use the standard library. Licensed original files are NOT distributed in this package.

To replay all final source checks into a new directory:
python replay_sources.py --repo-root /absolute/path/to/financethesis --output /absolute/path/to/a/NEW/replay_directory

The repo must retain the unchanged predeclared validator at output/omxsb_scaled_round_20261103/auction_design/validate_sampled_export.py (checked hash e0df3e1b512f15189422a4d0ec37d426ac7e2aad85804b54868434b26451bc24) and the original licensed files locally. The wrapper imports its original functions without running its hardcoded-path main block, supplying repo-relative raw paths. No economic estimator is added. Replay outputs have fresh timestamps and may have different absolute paths; substantive counts, flags, input hashes and per-day comparisons must match the frozen files.

Private/raw input map:
data/raw/shof/Reinvestments/hft_revisit_20261104/NASDAQ_2nd_level_orderbook_1793788245204.csv.zip: Bilia minute (main input).
data/raw/shof/Reinvestments/hft_revisit_20261104/NASDAQ_2nd_level_orderbook_1793790402104.csv.zip: combined CAMX/AFRY minute (main input).
data/raw/shof/Reinvestments/hft_revisit_20261104/NASDAQ_2nd_level_orderbook_1793789997030.csv.zip: CAMX mistaken date range, overlap equality only; never concatenate with main input.
data/raw/shof/Reinvestments/hft_pilot_20261103/NASDAQ_2nd_level_orderbook_1793732319625.csv.zip: Bilia full book.
data/raw/shof/Reinvestments/hft_pilot_20261103/NASDAQ_2nd_level_orderbook_1793733524718.csv.zip: CAMX 23 November full book.
data/raw/shof/Reinvestments/hft_pilot_20261103/NASDAQ_2nd_level_orderbook_1793733549086.csv.zip: CAMX 30 November full book.
data/raw/shof/Reinvestments/hft_pilot_20261103/NASDAQ_2nd_level_orderbook_1793733618890.csv.zip: AFRY 23 November full book.
data/raw/shof/Reinvestments/hft_pilot_20261103/NASDAQ_2nd_level_orderbook_1793733672616.csv.zip: AFRY 30 November full book.

Metadata inventory can be repeated without pandas. compare_bins.py also supports --repo-root, --input (Bilia + combined ONLY), --out NEW.json. compare_overlap.py takes --first CAMX-file --second combined-file --out NEW.json. Frozen outputs refuse overwrite.

Scope exclusions: no raw numeric bid/ask/size/transaction levels; no new returns or auction premiums; no network access; no credential or email content. Input/output chronology and receipt times are operator metadata, not an assertion of independent email inspection. PUBLICATION_SHA256.json does not hash itself.
