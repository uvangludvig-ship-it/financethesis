Replay requires Python with numpy and pandas and access to the original licensed
FI quantity extract/scaling inputs already produced by the frozen F35 source gate.
No API session or new download is required. Do not publish those private inputs.

The immutable DESIGN_LOCK.json records all original input hashes and original
machine paths. portable_replay.py replaces PATHS ONLY after verifying every file
against the original hash; it executes the unchanged run_overlap.py. The original
lock/spec/code/output are never overwritten.

All replays occur AFTER the original result is known. The unchanged estimator
writes an inherited EXECUTION_LOCK pre-read flag as false; that line is NOT
evidence that a replay was blind. The adapter explicitly records known prior
results in RELOCATED_DESIGN_LOCK.json and REPLAY_STATUS.json. The original
design itself was exploratory after known F35 results and a known source-width
assessment, not an overarching preregistration or a previously unseen dataset.

Check local input availability/hashes without parsing quantities or rerunning:
python portable_replay.py --repo-root /path/financethesis \
  --gate-dir /path/to/frozen_F35_retention_with_private_inputs --check-only

Run the exact locked statistic into a new directory:
python portable_replay.py --repo-root /path/financethesis \
  --gate-dir /path/to/frozen_F35_retention_with_private_inputs \
  --replay-root /path/NEW_REPLAY_DIRECTORY

Publicly available F35 source metadata normally lives in:
output/omxsb_scaled_round_20261103/independent_design/retention/
The same directory must also contain private/RAW_RELEVANT_POSITIONS.csv.gz and
private/SCALING_INPUTS.csv, obtained from the original licensed preparation.
Do not replace absent quantity rows with zero unless the frozen complete-report,
identity and unit support gates passed. Original input hashes are mandatory.

Synthetic accounting checks, requiring no licensed data:
python test_overlap_synthetic.py

Public results contain event/review endpoint fractions and aggregate counts.
Fund-level quantities, values and per-fund derived ledger remain private.
