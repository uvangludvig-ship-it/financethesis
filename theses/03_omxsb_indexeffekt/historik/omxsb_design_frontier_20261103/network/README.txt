Research decision: do not select potential-clientele comovement as the main
contribution on current evidence. This folder contains a new baseline-only
design assessment, not an event-return test or a revision of the old gate.

Read RECOMMENDATION_SV.txt first; DESIGN_CANDIDATE.txt gives the exact proposed
estimand and the review required before any further execution. The new question
uses all eligible prior-quarter benchmark funds, so it can include potential new
buyers. Its 49/118 baseline support improves on the old target-holder question's
1/118 after repair. The old first 0/118 and repaired 1/118 remain unchanged.

The distinctive measurement is the dated capital-weighted portfolio of a
predetermined fund clientele, shared by an entrant and its frozen three controls.
It does not select actual later purchasers. Its incremental economic information
beyond index/style comovement and its actual statistical precision remain
unproved. Thus it is not selected as a main contribution. This is not a null
result about investor risk or index effects: no new returns were inspected.

Reproduction requires the original local inputs, not supplied here. Absolute
input paths and SHA256 values are in INPUT_SHA256.json. The old folder
work/contribution_round_20261103/network_consequence contains the frozen
baseline holdings cache, event metadata and repaired identity pool. Repository
metadata and FI inputs are separately required. No credentials are needed by
these scripts; they do not acquire restricted sources or call an API.

Python requirements: pandas, numpy, scipy. A working local interpreter used was:
/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/contribution_round_20261103/network_consequence/.venv/bin/python

Replay in this order using that interpreter or equivalent:
  potential_clientele_gate.py
  pre_nonholder_cohort.py
  precision_scenarios.py

The first and third scripts regenerate their outputs and runtime timestamps;
archive this folder before rerunning if the original declaration timestamps
must remain untouched. The nonholder script preserves the original declaration
and verifies its saved counts. It only counts potential fund cohorts; it does
not create a second peer portfolio. The analytic precision calculations use
assumed variances and dependence, not observed prices or actual test power.

Common-weight assertions in the baseline script verify normalization and the
exclusion of all four issuers and their union of historical industries. Complete
cases, all failed reasons and all weights remain in the local audit artifacts.
No controls were rematched and no windows were selected from return outcomes.

Publication is opt-in by PUBLICATION_ALLOWLIST.txt, not by copying this directory.
It excludes raw literature PDF/text, all instrument/fund-level holdings and
weight files, event-level source-derived data, and logs. The source manifest
retains primary-source URLs, retrieval timestamps and hashes without rehosting
the papers. The public aggregate summary omits absolute capital values. This is
internal research support, not thesis prose. No repo or FTN files were changed.
