Source-gated OMXSB new-owner-cohort follow-up. Read REPORT_SV.txt first.
The primary result is one exploratory quantity-capital change, not fund returns,
transactions, an auction result or a causal effect. No FTN outcome is used.

Dependencies: Python3, pandas, numpy, scipy, pyarrow. Original successful runtime:
work/contribution_round_20261103/ownership_capital/.venv/bin/python in the chat
workspace. This environment need not be distributed; install normal dependencies.

Never rerun into the frozen original output directory. Scripts deliberately stop
if their lock exists. Make a NEW output directory and copy DESIGN_LOCK.txt and
Q0_TIMESTAMP_GUARD_AMENDMENT.txt into it, then run:
  python gate.py --repo-root /path/to/financethesis --output /new/output
  python run.py --repo-root /path/to/financethesis --gate-dir /new/output --output /new/output
For numerical replay of the frozen gate without reacquiring sources:
  python run.py --repo-root /path/to/financethesis --gate-dir /licensed/frozen/retention --output /new/replay

GATE_START_LOCK.json gives exact raw/derived input paths and SHA256 values.
The gate writes raw quantity subsets and scaling values only under private/.
A public clone alone does not contain the licensed LSEG raw panel or these private
files. No browser/API/data acquisition is performed by the replay scripts.
The old normalized ownership ledger fixes q0/q1 cohort membership and support;
new fund reports/units are screened symmetrically before the outcome lock.

SOURCE stages do read q2 quantity/value pairs to validate units. They never
calculate q1-to-q2 holding changes. OUTCOME_LOCK explicitly separates those stages.
Source-checking future endpoints can nevertheless select on corporate survival;
the economic report makes this limitation explicit.

Historical directories are separate versions, not additional specifications:
failed_runtime/ = partial metadata before missing-runtime stop;
archive_before_q0_timestamp_guard/ = initial source gate, no new outcome;
DESIGN_LOCK_V1_OVERBROAD_DATE.txt = superseded date guard, corrected before data.
No later repair of the eleven failed eventsets is part of this execution.

Public outputs: normalized pp contributions, aggregate levels/difference,
support/identity/calendar flags, code, locks and narrative technical reports.
Exclude private/ everywhere, raw licensed values, cache environments and full texts.
