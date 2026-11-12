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

## Numerical discrepancies

Of 40 compared CSV outputs, 32 match numerically within 1e-7. Eight differ in bootstrap interval endpoints or simulated p-values. Point estimates, counts and standard errors agree within the audit tolerances. The comparison includes event-level files used locally; only suitable aggregate files are copied into this public package.

The main effect table's largest difference is 0.0042575. Several auxiliary differences are larger. In the sparse early addition composition ratio, one frozen interval is approximately [-52.0348, 417.9463], while the rerun gives [-25.2104, 96.3730]. A separate early long-window ratio changes from an unbounded interval to a bounded interval around [24.135, 84.286]. These auxiliary endpoints must not be treated as numerically certified.

The inherited inversion searches outward to a finite cap and returns a single interval. A weakly identified or irregular acceptance set need not have that form. The routine also compares floating-point bootstrap statistics without a tie tolerance. The audit environment differs from the inherited recorded environment. These are plausible sources of sensitivity; the present audit has not proven a unique cause for every discrepancy.

The manuscript uses frozen main return-bootstrap outputs, whose discrepancies are small and disclosed. It uses analytical CR1 intervals for the composition table and independently calculated joint Fieller sets for demand ratios. Its new horizon p-values use 49,999 restricted wild draws and `(k+1)/(B+1)`; their accompanying intervals are analytical CR1, not inverted bootstrap intervals. They are labeled separately.

## Corrections to interpretation

| Issue | Treatment in the draft |
|---|---|
| Published versus working-paper anchor | Cite Greenwood and Sammon's 2025 article. The published abstract's recent deletion mean is +0.1%; do not silently reuse the older -0.6% working-paper number. |
| Causality | CARs, comparison regressions and holdings ratios are associations. No identified causal effect or elasticity is claimed. |
| Disappearance | Failure to reject zero is not equivalence. Neither latest-period mean meets the disclosed ±1 pp equivalence criterion. |
| Historical sample | July 2007 to June 2026; 2026 is incomplete. No claim to complete 2007 or 2026 calendar years. |
| Timing | Historical notice dates determine events. Current Nasdaq June/December rules are not imposed on earlier January/July reviews. |
| Holdings population | Production uses dated mandate classifications. The separate index-trade diagnostic does not mechanically classify the production fund universe. |
| Ratio uncertainty | Same events in numerator and denominator; ratio of means; joint covariance and weak denominators shown. |
| Comparison controls | Size screens are not the actual Nasdaq assignment threshold. The pre-return control includes AD-1, overlapping the outcome. |
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
| Essential | Holdings completeness | Reconcile complete pre/post reports, dated mandates and actual zero positions. Missing vendor rows do not independently prove zero holdings. |
| Essential | Corporate actions and share classes | Validate split adjustments and the shares-outstanding denominator against original records for affected events. |
| Essential | Fragile auxiliary inference | Keep the unstable intervals out of claims; if retained in a final analysis, replace and validate the inversion procedure and frozen environment. |
| Important | Comparison design | Remove AD-1 overlap from pre-return controls and reconstruct historical Nasdaq eligibility before interpreting adjusted coefficients beyond description. |
| Important | Source availability selection | Account for source-to-return attrition and its possible relation to historical performance; missingness is not shown to be random. |
| Important | Benchmarks and fallback returns | Validate dividends and corporate actions in fallback observations and examine risk-adjusted alternatives under a declared specification. |
| Important | Prospective validation | Freeze a protocol for later reviews. Existing results and the new horizon extension are exploratory. |

The raw-data limitations cannot be repaired by more elaborate prose or a stronger model setting. The draft retains them explicitly rather than asserting that every source observation has been independently authenticated.

## Environment

Audit: Python 3.12.4; NumPy 1.26.4; pandas 2.2.3; SciPy 1.15.2; matplotlib 3.10.1; python-docx 1.2.0. PDF: TeX Live 2025, pdfLaTeX, newtx fonts. The inherited README records different package versions; those claims are preserved as historical metadata, not asserted to describe this rerun.

This is a complete working-draft audit package with material open issues, not a guarantee of prize outcomes, causal identification or error-free underlying data.
