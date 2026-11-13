# Empirical diligence for the Greenwood–Sammon Swedish replication

Prepared 12 November 2026. Source calculations are pinned to commit `d2d41666ed213e4cc1f6cb382313f59c29e87ea0`. These checks were undertaken after the inherited results were known. They are corrections and exploratory diagnostics, not preregistered discoveries. Original files and results have not been changed.

## Executive findings

1. The clearest economic result remains positive later-period addition returns: 2.15% in 2017–2026, with the inherited review-bootstrap interval [1.01%, 3.39%]. Latest-period returns are less precisely resolved. These are existing results, independently reproduced previously, not new findings of this revision.
2. One auxiliary comparison regression had a pre-return control that included the first day of its outcome. Removing that day preserves every model's sample and strengthens, rather than eliminates, the later addition association. It does not create a causal design.
3. Fund-demand arithmetic reconstructs exactly, but a constant observed fund universe cannot be formed across all 39 reviews. A later-period constant universe exists and supports neither a claim of continuously rising purchases nor identification of a structural demand curve.
4. The holdings adjustment screen concerns changes between the event and the final available price observation, not merely stock splits during the event window. This can be motivated by adjusted holdings versus historical share counts, but its actual definition and historical attrition must be disclosed accurately.
5. The existing share-class analysis provides an economically intelligible Swedish extension: the event class and sister class both move, while the same-firm difference is imprecise. This helps assess interpretation but does not prove that all observed returns are firm news or that demand effects are absent.

## 1. Actual repair: remove the overlapping day from the comparison control

In `thesis_final/code/14_near_additions_control.py`, the outcome is CAR [AD−1, ED+1], while `ru` is CAR [AD−100, AD−1]. The shared AD−1 creates mechanical overlap between outcome and control. This is the auxiliary size-screened comparison design, not a blanket claim that every Greenwood–Sammon control is incorrectly timed.

`comparison_repair.py` reconstructs every inherited comparison outcome and pre-return from the full daily panel, preserving the original treatment of return fallbacks and the special Nordea/Tieto series. It then removes AD−1 only, so the revised control is [AD−100, AD−2]. No outcome, event exclusion, size control, review fixed effect or comparison security is changed. Both event types, both periods, both market filters and both deletion exclusion sets are retained.

| Later-period model | Inherited coefficient | Repaired coefficient | Repaired analytical 95% interval | Restricted wild p |
|---|---:|---:|---:|---:|
| Additions, all comparison securities | 1.525 | 1.652 | [0.478, 2.826] | 0.01142 |
| Additions, main-market comparison securities | 1.395 | 1.490 | [0.240, 2.741] | 0.02876 |
| Deletions, flagged events excluded, all comparisons | −1.399 | −1.569 | [−3.037, −0.101] | 0.04320 |
| Deletions, flagged events excluded, main-market comparisons | −1.381 | −1.544 | [−3.149, 0.062] | 0.06570 |

All estimates are percentage-point conditional return differences. The addition models retain 159 events and, respectively, 1,609 or 1,379 comparison security-review observations over 19 reviews. The corresponding early-period addition coefficient changes from 3.900 to 4.013 percentage points with all comparisons. See the complete CSV rather than selectively reporting only the significant cases.

Intervals use analytical CR1 standard errors with t(G−1). The separately reported restricted wild-bootstrap p-values use 49,999 draws, Rademacher weights when G≥12, Webb otherwise, a fixed seed and the finite-simulation correction (k+1)/(B+1). They are not inversions of these analytical intervals. A cluster-compressed general-regression implementation was checked against observation-level statsmodels OLS and covariance calculations. All 327 recorded checks pass, including original coefficients, standard errors and counts and five explicit bootstrap draws per model.

This repair does not make the size screen a Nasdaq assignment threshold. There is still no regression-discontinuity design, and selecting comparison securities by size does not establish that their unobserved return determinants match those of additions or deletions. The revised coefficient belongs in a sensitivity section or appendix, not in a causal headline.

## 2. Fund-demand arithmetic, dates and zero positions

`holdings_dd.py` uses the inherited dated mandate definitions and reconstructs the aggregate C demand numerator from the actual classified fund-event snapshots. The maximum discrepancy across all 311 complete primary holdings events is 4.44e−16 percentage points.

The C measure combines strict followers, benchmark variants and funds with an OMXSB-linked component. It is the actual change in covered holdings of the event security. The production classification comes from dated mandates. `02b_indexaffarer.py` produces a separate index-trade diagnostic; its ≥50% rule does not mechanically determine the production C universe. This distinction matters for fidelity to the original study.

Among 3,231 classified fund-event records contributing to the primary sample:

- No observed pre-position date is on/after AD or more than 120 calendar days before it.
- No included post-position date is later than ED+45 calendar days.
- No fund-event has multiple included rows on the same side in this sample.
- Forty records use a pre-position report date different from the latest fund report used in the availability check (39 addition records and one deletion record). This does not itself show the position is wrong, but means that evidence of another security's report is not the same as observing this security on that exact date.
- Missing position rows are interpreted as zero conditional on report availability elsewhere in the extract. For additions, 1,630 of 1,739 contributing fund-event records have no observed pre-position row. This is economically plausible for new index holdings but cannot be authenticated as a true zero from a security-query extract alone.

Do not describe these checks as full report reconciliation. Full original holdings reports, or a documented vendor completeness flag, are needed to distinguish an absent position from an incomplete security-level response. The audit has verified arithmetic and available timestamps, not the economic truth of every imputed zero.

### Fixed observed fund-universe sensitivity

The rule was written into the new script before its results were inspected: take the intersection of verified mandate status and both-side report availability at every review, without selecting on purchases or returns. Run it for 2007–2026 and 2017–2026. Preserve an empty intersection rather than relax the rule after seeing results. Both exact fund names and mandate alias keys were examined; their later-period sets coincide.

- **2007–2026:** no constant fund or mandate-key universe across all 39 reviews.
- **2017–2026:** three funds across all 19 reviews: Swedbank Robur Access Mix, Swedbank Robur Access Sverige, and iShares OMX Stockholm Capped UCITS ETF.

On the same complete addition events, the three-fund mean purchase measure is 0.488% of shares in 2017–2021 and 0.378% in 2022–2026. The primary broad C means are 1.107% and 0.973%. The ratios of mean signed CAR to this narrower three-fund denominator are 6.74 and 6.05, versus 2.97 and 2.35 using broad C. The corresponding deletion numbers are retained in `holdings_fixed_universe_sensitivity.csv`.

These are narrower-universe descriptive sensitivity measures, not corrected estimates of total index demand. They retain the same missing-position assumptions and changing event composition. The subset excludes relevant funds and therefore should not replace C mechanically. It demonstrates that the later data do not support a simple claim that covered purchases rise continuously, even when the observed fund universe is fixed.

Across all four periods, mean primary addition purchases are approximately 0.15%, 0.52%, 1.11% and 0.97%. Average reporting mixed-fund count rises from zero in the first period to 8.83 in the last. Part of the historical difference may be changing investor mandates and part may be coverage; the current data do not separate them.

## 3. Adjustment-screen provenance and denominator freshness

The original derivation is in [`code/claude_checks/runda11.py`](https://github.com/uvangludvig-ship-it/financethesis/blob/d2d41666ed213e4cc1f6cb382313f59c29e87ea0/code/claude_checks/runda11.py), retrieved at the frozen commit.

Its adjustment factor is company market capitalization divided by total shares of locally quoted classes, divided by the event class's adjusted closing price. It compares that proxy at ED with its value at the last available price date for the security. A missing ratio or ratio outside [1/1.4, 1.4] sets `split=True`.

Thus the retained holdings sample is **after a share-adjustment consistency screen**, not simply a sample without splits during the event window. The rule can exclude a 2007 event because of a later adjustment before the dataset endpoint. This can be a deliberate safeguard because the numerator is `Fund Shares Held (Adjusted)` while the denominator is historical shares outstanding. Removing the future screen without knowing the vendor's adjustment convention would not be a justified correction.

The share denominator is the last available positive share count at or before ED, with a search back as far as 250 trading days. `share_adjustment_dd.py` independently reconstructs the denominator and proxy-factor calculation and records their differences from the frozen input. It also reports an explicitly diagnostic wide snapshot-bound proxy comparison, AD−120 calendar days through ED+45 calendar days. That is not an exact fund-specific report interval or an authenticated split record. See the aggregate validation and screen-summary CSVs for the actual reconciliation outcome.

All 468 stored denominators reconstruct exactly and all 468 adjustment ratios agree to numerical precision (maximum absolute discrepancy 8.9e−16). In every one of the 311 retained complete holdings events, the denominator is available in the daily vendor panel on ED itself; the code does not use its 250-day stale-value fallback for this sample. This establishes panel availability, not the freshness of the underlying issuer filing, because a provider may repeat a share count across days.

| Type | Period | Candidates in holdings input | Excluded by adjustment screen | Of these, missing factor | Complete primary holdings sample |
|---|---|---:|---:|---:|---:|
| Addition | 2007–2011 | 37 | 26 | 4 | 8 |
| Addition | 2012–2016 | 54 | 27 | 4 | 27 |
| Addition | 2017–2021 | 83 | 25 | 4 | 58 |
| Addition | 2022–2026 | 87 | 9 | 1 | 78 |
| Deletion | 2007–2011 | 31 | 21 | 4 | 7 |
| Deletion | 2012–2016 | 45 | 20 | 4 | 25 |
| Deletion | 2017–2021 | 59 | 18 | 3 | 40 |
| Deletion | 2022–2026 | 72 | 4 | 0 | 68 |

The final column also requires usable CAR and holdings data, so it need not equal candidates minus the adjustment exclusions. Most nonmissing global-band exclusions fall inside the wide event-local proxy band: for additions, 21/22, 21/23, 20/21 and 8/8 across the four periods; for deletions, 15/17, 14/16, 15/15 and 4/4. This is consistent with the screen being driven mainly by later adjustment differences rather than changes local to the event. It is not proof of the underlying corporate-action dates, and it is not a reason to switch the main filter mechanically.

## 4. Share classes and FI: existing Swedish extensions worth explaining

The existing share-class output contains the market-adjusted return of each leg on the same 39-event cohort. The mean sign-adjusted log returns are 3.181% for the index class and 2.850% for its sister class, giving a 0.331% paired difference. The arithmetic identity holds to less than 2e−10.

For the 19 additions, the corresponding means are 2.135%, 2.479%, and −0.344%. For the 20 deletions they are 4.174%, 3.203%, and 0.971%, with deletion signs reversed in all three columns. These are descriptive summaries of existing outputs, not newly discovered causal estimates. In the source-consistent 29-event/9-firm subset, the relative estimate is 0.04% with an inherited interval [−0.59%, 0.65%].

The comparison is useful because share classes belong to the same issuer. However, classes differ in liquidity, voting rights and investor clientele; demand can spill over or substitute between them. Repeated firms and common review shocks remain. The inherited placebo simulation draws by event rather than simulating those shocks jointly. A small or insignificant relative estimate neither proves no demand effect nor establishes that all raw CAR is firm news. It is also a selected small subset, not a decomposition of the main 471-event estimate.

The FI cross-check is a second reporting channel for the holdings scale, not independent return data. On 106 matched additions in 2019–2026, the common CAR is 2.43%, FI mean demand 1.14% and matched C demand 1.05%; their ratios are 2.12 and 2.30. This supports the order of magnitude in a later matched sample, while leaving early coverage, imputed zeros and exogeneity unresolved.

## 5. Claim priorities for a readable revised paper

### Institutional timing matters to period comparisons

The supplied event list has exactly one AD and one ED per review, with no trading-calendar remapping relative to its stored announcement/effective dates. The lag from announcement to effectiveness ranges from 6 to 18 trading days (median 15). It is generally 14–18 days during 2010–2019, falls to 7 and 6 in the two 2021 reviews, and is 6–8 throughout 2022–2026. Therefore the primary G&S-style [AD−1, ED+1] window becomes shorter in recent years. This does not make the event-defined window incorrect, but a comparison of its means changes both the period and the amount of calendar time included. The original fixed three-day announcement and implementation windows should remain visible; do not describe their difference as a pure change in elasticity. A figure aligned on AD and a separate figure aligned on ED must not imply a constant AD-to-ED distance. The aggregate dates and lags are in `review_timing_summary.csv`.

### New fixed-window decomposition: a measurement result, not a timing experiment

The main agent specified a common seven-return window AD−1 through AD+5 after inspecting the announcement calendar, before inspecting its outcome estimates. Because the minimum announcement-to-effective gap is six trading days, this window ends before ED for every event. The main agent's `return_definition_checks.py` implements those endpoints correctly and uses the same complete primary cohorts when comparing it to the whole event window.

After seeing the initial fixed-window means, this DD independently rebuilt daily returns and added the complementary nonoverlapping remainder AD+6 through ED+1. `fixed_window_decomposition.py` retains both event types and all periods. It checks that first-seven plus remainder equals the whole CAR for every event and every mean/contrast, and verifies every earlier fixed-window mean, count and CR1 standard error. All 419 validation checks pass, including observation-level statsmodels checks of restricted bootstrap draws.

| Addition period | First seven returns | Remaining returns | Whole window |
|---|---:|---:|---:|
| 2007–2011 | 1.185% | 7.338% | 8.523% |
| 2012–2016 | 1.264% | −1.015% | 0.250% |
| 2017–2021 | 1.227% | 1.620% | 2.847% |
| 2022–2026 | 1.804% | −0.306% | 1.498% |

For additions, the latest-minus-earliest difference decomposes exactly into +0.619 percentage points in the first seven returns and −7.644 in the remainder, totaling −7.025. The first-seven contrast has an analytical CR1 interval [−1.795, 3.032] and restricted wild p=0.62454. The remainder contrast has interval [−11.913, −3.374] and p=0.00930. These contrasts use the same four-period indicator regression and review clusters as the primary period contrast, with 49,999 bootstrap draws and finite-simulation correction. Their analytical intervals are not bootstrap-inverted intervals.

The corresponding deletion contrasts are +2.780 in the first seven returns (p=0.08814) and +1.843 in the remainder (p=0.40432), totaling +4.623 (p=0.03960). They are reported regardless of significance.

The defensible wording is: **the observed first-to-last decline in addition CAR is concentrated in the portion after the common first seven daily returns; the first-seven point estimate rises slightly, but its change is imprecise.** Do not say that first-week effects are equal, or that shorter announcement lead time explains or causes the whole-window decline. The remainder combines different durations, different securities and possibly unrelated information. These are pointwise, exploratory follow-up tests selected after existing results were known, not a newly confirmatory primary endpoint. The latest first-seven mean's pointwise p=0.03184 must not be used to replace the original window solely because it crosses a conventional significance cutoff.

| Claim | Status | Placement |
|---|---|---|
| Later-period index additions have positive average market-adjusted returns | Supported descriptive finding, existing baseline and exclusions | Abstract, introduction, first results subsection |
| Latest-period index effect has disappeared | Not established; interval too wide and equivalence not shown | Explain concisely in main results |
| Returns steadily decline over time | Not supported by period path or trend tests | Do not use as headline |
| More concentrated trading coexists with positive event-window returns | Supported descriptive joint pattern; volume is share of a fixed window | Main interpretation |
| Covered index-linked funds buy additions and sell deletions | Supported by measured signed holdings changes, conditional on snapshot assumptions | Demand section with simple definitions |
| The ratio M identifies a causal price multiplier or elasticity | Not established by this design | Explicit boundary, without adding unnecessary structural notation |
| Early-to-late M comparison is precise | Not supported; sparse early denominator and strong adjustment attrition | Appendix uncertainty check plus short main caveat |
| Within-issuer classes isolate pure firm information | Not established; small subset and spillovers | Swedish extension, careful descriptive reading |
| Positive cumulative CAR through ED+20 establishes permanent impact | Not established | Exploratory appendix or focused horizon sensitivity |

## Reproduction

Run each script with the frozen `thesis_final` directory and a separate output directory:

```text
python comparison_repair.py PATH_TO_THESIS_FINAL OUTPUT_DIRECTORY
python holdings_dd.py PATH_TO_THESIS_FINAL OUTPUT_DIRECTORY
python share_adjustment_dd.py PATH_TO_THESIS_FINAL OUTPUT_DIRECTORY
python fixed_window_decomposition.py PATH_TO_THESIS_FINAL OUTPUT_DIRECTORY --reference PATH_TO_FIXED_WINDOW_SENSITIVITY_CSV
```

The scripts require authorized source data. The comparison repair uses NumPy, pandas, SciPy and statsmodels. The holdings script reads the inherited classification setup with output redirected to its own `holdings_setup/` folder. Do not publish raw security or fund-event observations; only the aggregate summaries, code, public classification metadata and this report are intended as shareable outputs.
