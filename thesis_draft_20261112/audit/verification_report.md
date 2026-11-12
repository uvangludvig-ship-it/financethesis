# Verification report

The inherited empirical pipeline executes successfully and the independent audit reproduces the main return arithmetic. The substantive evidence remains observational. This report distinguishes computational checks from source authentication and statistical validity.

## Frozen version and completed checks

Source repository: `uvangludvig-ship-it/financethesis`.

Source commit: `d2d41666ed213e4cc1f6cb382313f59c29e87ea0`.

Source git tree: `1f14b80599d9b904fd90f735afb76975006b3058`.

- Downloaded 292 selected source files and checked their Git blob identities against the pinned manifest.
- Reran the complete `thesis_final/run_all.py` in an isolated copy. It ended with `0 FEL`. The original results were preserved.
- All 43 recorded input MD5 checks passed. MD5 is used here to match the inherited input inventory, not as an authenticity or security guarantee. The new package inventory uses SHA-256.
- Independently reconstructed announcement, implementation and main-window CARs for 487 imported candidates, without importing inherited return or inference functions.
- Recorded 73 independent arithmetic/sample/inference checks, all passing. These are software checks, not independent empirical replications.
- Reconstructed 536 source events, 487 imported candidates, ten deletion exclusions and 471 complete main-window outcomes: 256 additions and 215 deletions. Type-specific review counts are 38 each; their union is 39.
- Identified seven events with a price-return fallback, covering 104 event-day observations. Removing implicit forward filling did not change any main-window CAR in this frozen sample.
- Computed equal-review means, leave-one-review-out influence, review jackknife and review-by-security covariance sensitivity; joint Fieller sets; a declared ten-test Holm correction; and an explicitly chosen ±1 percentage point equivalence check.
- Cross-checked the actual audit estimator functions against statsmodels 0.14.2 and observation-level bootstrap OLS: 77 additional checks passed. These cover means, CR1, two-way covariance, jackknife, compressed bootstrap calculations, Holm and Fieller-set classification. The bootstrap comparison uses the same 997 draws to test the algorithm; the reported horizon estimates retain 49,999 draws.
- Added a fixed-cohort, non-overlapping ED+20 calculation. All periods and both event types are retained. Follow-up exclusions are disclosed as post-result exploration.

The original checks, full runner log, independent check rows and estimate files accompany this report. The original check script uses tolerances and checks selected expected values; its success alone does not establish that all original outputs are identical.

## Replication-focused revision: completed diligence and corrections

The revised manuscript keeps the original Swedish baseline and separates it from supplementary definition checks and corrections. The additional work is documented in [the revision report](replication_revision_report.md), the aggregate files under `results/`, and the corresponding scripts under `../code/`. No original empirical source file or frozen result is overwritten. The sequence of decisions is recorded in [the exploratory addendum](analysis_addendum.md).

### Changing announcement lead times and return-window accounting

All 39 supplied reviews have one common announcement date and one common effective date, with no trading-calendar remapping relative to the stored notice dates. Their announcement-to-effective gaps range from six to 18 trading days. Among reviews represented in the complete addition sample, the median gap is 14, 16, 15 and six days across the four periods. The primary event-defined window therefore covers fewer days recently.

After inspecting that calendar, and before inspecting the new fixed-window outcomes, a seven-daily-return diagnostic was chosen: AD−1 through AD+5. It ends before ED for every observed event. The original main results were already known, so this is exploratory rather than preregistered. The comparison uses exactly the same complete events as the primary CAR in each period. Addition means over this common interval are 1.185%, 1.264%, 1.227% and 1.804%, compared with 8.523%, 0.250%, 2.847% and 1.498% over the full AD−1-to-ED+1 window.

A subsequent follow-up, chosen after those fixed-window means were inspected, calculated the nonoverlapping remainder AD+6 through ED+1 and first-to-last contrasts. It independently reconstructs the initial fixed-window calculation and verifies the accounting identity for every event, mean and contrast. **All 419 recorded validation checks pass**, including original mean/count/standard-error comparisons and observation-level statsmodels checks of the restricted bootstrap calculations.

For additions, the latest-minus-earliest difference is −7.025 percentage points for the whole window, +0.619 for the first seven returns, and −7.644 for the remainder. The fixed-window contrast's analytical CR1 interval is [−1.795, 3.032], with restricted wild-bootstrap p=0.62454. This does not establish equality of announcement responses. The descriptive result is that the observed whole-window decline is concentrated after the common initial interval. Different securities, durations and intervening information remain possible explanations; the exercise does not identify the causal effect of shortening the calendar. Both event types and all period/component results are retained in `results/fixed_window_decomposition.csv`.

Return aggregation was also checked on matched events. For later additions, the arithmetic mean is 2.153%, compared with 2.180% for compounded stock return minus compounded benchmark return over the same included days. The latest-block means are 1.498% and 1.446%. Closing-price-endpoint alternatives and fixed-cohort paths through ED+20 are separately reported in `results/return_conventions.csv` and `results/fixed_cohort_path.csv`. These do not silently replace the primary daily-return convention or establish exact equivalence with unrecovered US source code.

### Comparison-control overlap repaired

The inherited auxiliary comparison regression uses a pre-return control over AD−100 through AD−1 while the outcome starts on AD−1. The revised sensitivity removes that one overlapping day, making the control AD−100 through AD−2. It preserves every model's observations, outcome, log-size control, review fixed effects, market filter and event-exclusion rules. The frozen specification remains available beside the correction.

All 4,087 comparison-panel outcomes and original pre-returns reconstruct from the daily inputs to numerical precision. **All 327 validation checks pass**, including inherited coefficients, counts and CR1 standard errors and explicit observation-level checks of bootstrap draws. The later addition coefficient changes from 1.525 to 1.652 percentage points, with a revised analytical CR1 interval [0.478, 2.826] and restricted wild-bootstrap p=0.01142. Restricting comparison securities to the main market changes 1.395 to 1.490 points, with interval [0.240, 2.741] and p=0.02876. Both deletion sets, both periods and both market filters are retained in `results/comparison_repair_results.csv`.

The one-day overlap is therefore repaired in the revised comparison results. The size screen still does not reconstruct the Nasdaq assignment boundary, and the corrected coefficients remain conditional associations rather than causal estimates.

### Holdings coverage, adjustment screen and denominator checks

The classified fund-event snapshots reconstruct C demand for all **311 complete primary holdings events**, with a maximum numerical discrepancy of 4.44e−16 percentage points. Across 3,231 contributing fund-event records, no observed pre-position falls on/after AD or more than 120 calendar days before it, no included post-position exceeds ED+45, and no included side contains duplicate rows for the same fund-event. Forty records use a pre-position date different from the latest report date that establishes the fund's availability elsewhere in the extract. Report availability is not proof of full report completeness. In particular, 1,630 of 1,739 contributing addition fund-event records have no observed pre-position row; interpreting those as zero remains an assumption that the security extracts alone cannot authenticate.

A fixed fund universe was selected only by verified mandate status and pre/post report availability at every review, without selecting on returns or purchases. The intersection is empty across 2007–2026 and contains three funds across all 19 reviews in 2017–2026. Within each later block, the same events are used for the fixed and broad fund measures. Fixed-universe addition demand is 0.488% in 2017–2021 and 0.378% in 2022–2026, compared with 1.107% and 0.973% for broad C. This is a narrower-population sensitivity, not a corrected total-demand estimate; the missing-position assumptions and changing event composition remain.

The original holdings adjustment screen was traced to its source calculation. It compares a price/share-adjustment proxy at ED with the proxy at the security's last available price observation. Ratios outside [1/1.4, 1.4], or missing ratios, are excluded. Thus it is not merely an exclusion of splits during the event window. Later adjustment changes can matter because vendor holdings are adjusted while the denominator is historical shares outstanding. Replacing that screen with an event-local rule would require the vendor's adjustment convention and corporate-action evidence.

All **468 stored share denominators and adjustment ratios reconstruct** from the supplied panel (the largest ratio discrepancy is 8.9e−16). Every retained complete holdings event has its share-count field available in the daily vendor panel on ED; none requires the permitted 250-trading-day fallback. This verifies availability, not the freshness of the underlying issuer filing. The adjustment screen excludes 26/37, 27/54, 25/83 and 9/87 addition candidates across the four periods, including respectively four, four, four and one missing-factor cases. The analogous deletion counts are 21/31, 20/45, 18/59 and 4/72. Historical selection is consequently important for the early multiplier comparison. `results/share_adjustment_screen_summary.csv` distinguishes adjustment exclusions from other reasons a holdings candidate does not enter the complete sample.

### Same-cohort share-class summaries

The existing 39-event, 13-firm share-class sample contains both return legs. Its mean sign-adjusted log market-excess returns are 3.181% for the index class and 2.850% for the sister class; their difference is 0.331%. The leg identity holds to less than 2e−10. For the 19 additions, the respective means are 2.135%, 2.479% and −0.344%; for 20 deletions, with signs reversed, they are 4.174%, 3.203% and 0.971%. These are clearer summaries of existing results, not new causal estimates. The source-consistent 29-event/nine-firm subset has a relative mean of 0.04%, with an inherited interval [−0.59%, 0.65%]. Spillovers, repeated firms, liquidity differences and non-joint placebo draws prevent treating this selected sample as a causal decomposition of the main CAR.

The additional validation counts describe numerical software checks. They are not independent financial observations, full source authentication, or independent confirmations of the economic hypotheses.

## Numerical discrepancies

Of 40 compared CSV outputs, 32 match numerically within 1e-7. Eight differ in bootstrap interval endpoints or simulated p-values. Point estimates, counts and standard errors agree within the audit tolerances. The comparison includes event-level files used locally; only suitable aggregate files are copied into this public package.

The main effect table's largest difference is 0.0042575. Several auxiliary differences are larger. In the sparse early addition composition ratio, one frozen interval is approximately [-52.0348, 417.9463], while the rerun gives [-25.2104, 96.3730]. A separate early long-window ratio changes from an unbounded interval to a bounded interval around [24.135, 84.286]. These auxiliary endpoints must not be treated as numerically certified.

The inherited inversion searches outward to a finite cap and returns a single interval. A weakly identified or irregular acceptance set need not have that form. The routine also compares floating-point bootstrap statistics without a tie tolerance. The audit environment differs from the inherited recorded environment. These are plausible sources of sensitivity; the present audit has not proven a unique cause for every discrepancy.

The manuscript uses frozen main return-bootstrap outputs, whose discrepancies are small and disclosed. It uses analytical CR1 intervals for the composition table and independently calculated joint Fieller sets for demand ratios. New horizon, fixed-window and comparison-correction p-values use 49,999 restricted wild draws and `(k+1)/(B+1)`; their accompanying intervals are analytical CR1, not inverted bootstrap intervals. They are labeled separately. The new routines do not repair or certify every endpoint produced by the inherited auxiliary inversion.

## Corrections to interpretation

| Issue | Treatment in the draft |
|---|---|
| Published versus working-paper anchor | Cite Greenwood and Sammon's 2025 article. The published abstract's recent deletion mean is +0.1%; do not silently reuse the older -0.6% working-paper number. |
| Causality | CARs, comparison regressions and holdings ratios are associations. No identified causal effect or elasticity is claimed. |
| Disappearance | Failure to reject zero is not equivalence. Neither latest-period mean meets the disclosed ±1 pp equivalence criterion. |
| Historical sample | July 2007 to June 2026; 2026 is incomplete. No claim to complete 2007 or 2026 calendar years. |
| Timing | Historical notice dates determine events. Current Nasdaq June/December rules are not imposed on earlier January/July reviews. The shortened announcement lead time changes the duration of the primary window; the fixed-window decomposition is exploratory and not a causal timing experiment. |
| Holdings population | Production uses dated mandate classifications. The separate index-trade diagnostic does not mechanically classify the production fund universe. |
| Ratio uncertainty | Same events in numerator and denominator; ratio of means; joint covariance and weak denominators shown. |
| Comparison controls | The inherited AD-1 overlap has been removed in the revised auxiliary comparison, preserving the original specification beside it. Size screens still do not reconstruct the actual Nasdaq assignment threshold. |
| Holdings adjustment screen | The screen compares ED with the final available adjustment proxy; it is not simply an event-window split exclusion. Historical attrition and zero-position assumptions remain material. |
| News screen | Only 24 extreme inherited events screened. Remaining events are not certified news-free. |
| Volume | Daily share of a 45-day volume denominator; not auction volume, total turnover growth or execution cost. |
| Spread | Quoted closing spread; not effective spread or the slope of residual supply. |
| Multiplicity | Ten-test adjustment is limited and retrospective; unrecorded historical selection remains. |
| Longer horizon | Identical non-overlapping cohorts; exploratory finite-horizon association, not permanent impact. |
| Twins | Log relative returns, small repeated-firm sample, potential spillovers and non-joint placebo draws. |

## Unresolved issues before a defensible submission

| Priority | Issue | Required evidence or action |
|---|---|---|
| Essential | Course AI rule | Authors write the submitted text and make a truthful permitted-assistance disclosure; use the mandatory cover template and verified student details. |
| Essential | Event notices | Initial retrieval recovered 23/39 notices; follow-up opened 12 more, found indexed text only for three, and left the 2008 second-half notice unresolved. Recover originals/attachments and reconcile identities and timestamps field by field. The December 2008 correction also has an inconsistent printed effective year and requires the first announcement's timing to be checked. A recovered webpage alone does not complete this work. |
| Essential | Holdings completeness | Reconcile complete pre/post reports, dated mandates and actual zero positions. Arithmetic and available timestamps now reconcile, but missing vendor rows do not independently prove zero holdings. The constant-fund sensitivity retains that assumption. |
| Essential | Corporate actions and share classes | Validate the vendor's adjusted-holdings convention and share-count consistency against original records. All stored screen ratios and denominators now reconstruct, and retained denominators are available in the panel on ED, but those facts do not authenticate corporate actions or issuer-filing freshness. |
| Essential | Fragile auxiliary inference | Keep the unstable intervals out of claims; if retained in a final analysis, replace and validate the inversion procedure and frozen environment. |
| Important | Comparison design | The AD-1 overlap is repaired. Reconstruct historical Nasdaq eligibility and establish a credible comparison design before interpreting the adjusted coefficients causally. |
| Important | Source availability selection | Account for source-to-return attrition and its possible relation to historical performance; missingness is not shown to be random. |
| Important | Benchmarks and fallback returns | Validate dividends and corporate actions in fallback observations and examine risk-adjusted alternatives under a declared specification. |
| Important | Prospective validation | Freeze a protocol for later reviews. Existing results, the horizon extension, timing decomposition and fixed-fund sensitivity are exploratory; the correction does not create independent confirmation. |

The raw-data limitations cannot be repaired by more elaborate prose or a stronger model setting. The draft retains them explicitly rather than asserting that every source observation has been independently authenticated.

## Environment

Audit: Python 3.12.4; NumPy 1.26.4; pandas 2.2.3; SciPy 1.15.2; matplotlib 3.10.1; python-docx 1.2.0. PDF: TeX Live 2025, pdfLaTeX, newtx fonts. The inherited README records different package versions; those claims are preserved as historical metadata, not asserted to describe this rerun.

This is a complete working-draft audit package with material open issues, not a guarantee of prize outcomes, causal identification or error-free underlying data.
