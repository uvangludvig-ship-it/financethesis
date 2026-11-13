# Exploratory audit specification

Recorded on 12 November 2026 before running the new audit calculations. This is not a preregistration: inherited results, several return paths, and earlier analysis decisions were already known.

Source commit: d2d41666ed213e4cc1f6cb382313f59c29e87ea0.

1. Independently rebuild market-adjusted daily returns from the frozen price files. Check all inherited announcement, implementation, and total-window CARs; sample attrition; date alignment; and return fallback use. Retain the original sample rules, with separate sensitivity to exclusions.
2. Independently reproduce the event-weighted mean and CR1 standard error, report equal-review weighting, leave-one-review-out estimates, security and review two-way clustering, and cluster jackknife standard errors. These are sensitivity analyses, not a selection procedure for the preferred p-value.
3. On a fixed complete-case cohort, compute non-overlapping CARs [AD-1, ED-1], [ED, ED+20], and their sum [AD-1, ED+20]. A residual cumulative return does not establish a causal or permanent price effect. Report all periods and both event types, not only significant cases.
4. For the demand-scaled return ratio, report Fieller confidence sets based on the joint review-clustered covariance of the numerator and denominator, alongside the inherited percentile intervals. Do not discard draws or parameter values because a denominator changes sign. Label these as asymptotic sensitivity calculations, especially for sparse early periods.
5. Report Holm-adjusted inherited p-values for a declared audit family: the eight five-year total-window means and the two earliest-versus-latest contrasts. This family does not account for all historical researcher choices; it is not a new confirmatory family.
6. Test practical equivalence using the two one-sided bounds implied by an audit margin of plus/minus 1 percentage point for the latest-period CAR. The margin is a transparent reporting benchmark chosen after seeing old results, not an external economic threshold or preregistered target.

No FTN outcomes are opened. No new causal design is claimed. All results, including failures and ambiguous intervals, remain in the audit output.

Follow-up recorded after inspecting the new horizon results: apply the inherited Sivers, MSCI-overlap and company-news exclusions separately to the cumulative horizon, for both event types and both later periods. These checks are post-result exploration. The independent horizon bootstrap uses 49,999 draws with a finite-simulation correction; its p-values are reported beside, not as the inversion of, analytical CR1 intervals.

## Replication-focused revision on 12 November 2026

The following entries record the revision's actual sequence of decisions. They were added after the original manuscript and inherited results had been read. They do not retroactively preregister any part of the study. Original primary estimates and exclusion rules are preserved; corrected or supplementary specifications are identified separately.

### Return definitions and the changing event calendar

1. Compare the existing arithmetic daily CAR with compounded stock return minus compounded benchmark return over exactly the same included days, and with a separately labeled closing-price-endpoint alternative. Preserve common events so that a difference is not attributed to aggregation when it comes from sample selection. The available author-paper wording does not establish every convention in unrecovered US code.
2. Inspect announcement/effective-date metadata across all reviews. The observed lead time ranges from six to 18 trading days and shortens in the later sample. After seeing these calendar facts, but **before inspecting the new fixed-window outcome estimates**, choose AD−1 through AD+5 as a common seven-daily-return diagnostic. The minimum gap ensures that it ends before ED for every event. The main return history was already known. Retain both event types and every period, on the same complete events as each primary CAR estimate.
3. **After inspecting those fixed-window means**, add the complementary interval AD+6 through ED+1 and latest-minus-earliest contrasts for the whole window and both components. Check the event-level accounting identity and retain every result, including imprecise contrasts. Use the original four-period indicator design for contrasts, review-cluster CR1 intervals and separately computed 49,999-draw restricted wild-bootstrap p-values with `(k+1)/(B+1)`. These intervals are not bootstrap inversions. The resulting 419 validation checks verify arithmetic and estimator implementation, not the causal interpretation of the calendar.
4. Keep the primary AD−1-to-ED+1 measure. Do not replace it because a fixed-window mean has a smaller p-value. Do not infer statistical equality from an imprecise first-seven contrast or claim that shorter announcement lead times caused the whole-window decline. The remainder changes duration and can contain different information across events.

### Repair of the auxiliary comparison-control overlap

The inherited size-screened comparison uses outcome CAR [AD−1, ED+1] and pre-return control [AD−100, AD−1]. After detecting their one-day overlap, remove only AD−1 from that control. Preserve outcome, observations, log-size control, review fixed effects, market filters and deletion exclusion sets. Report original and corrected results for additions and deletions, before and after 2017, with all comparison securities and main-market comparison securities. No variant is selected by its p-value.

The correction reconstructs all 4,087 comparison-panel outcomes and old pre-returns from daily inputs and passes 327 validation checks, including original coefficients/counts/standard errors and observation-level checks of restricted bootstrap draws. New inference uses analytical CR1 intervals and separate 49,999-draw restricted wild p-values. This is a timing repair of an existing auxiliary model, not a reconstructed Nasdaq cutoff or a new causal design. The original result files are retained.

### Holdings availability, fixed investor universe and share adjustment

The production definition of the broad benchmark-linked fund group is retained. Reconstruct its aggregate numerator from the dated classifications and actual snapshots; inspect observed position dates, missing-side assumptions and duplicate records. Reconcile stored shares-outstanding denominators and adjustment factors with their source-panel construction. These checks establish numerical consistency and available fields, not the truth of every underlying position or corporate action.

Before inspecting the new fixed-universe outcome summaries, specify an availability-only selection rule: retain funds with verified benchmark mandate status and pre/post report availability at **every** review in the chosen interval. Apply it to 2007–2026 and 2017–2026, using exact fund names and mandate alias keys. Do not select funds based on purchases or returns, and report an empty intersection without relaxing the rule. Compare fixed and broad measures on identical events **within each period**; the event sets themselves differ between periods. Retain both event types. Do not reinterpret the narrower denominator as corrected total demand.

The full-period intersection is empty; the later-period intersection contains three funds. All 311 complete primary-event C numerators reconstruct, as do all 468 stored share denominators and adjustment ratios. The adjustment rule compares ED with the final available price/share proxy and can exclude events because of later adjustment changes. No event-local replacement is introduced, because adjusted holdings versus historical shares may require that safeguard. Missing position rows remain assumed zeros conditional on report availability elsewhere; full reports were not recovered by these calculations.

### Share-class presentation and retained inferential limits

Summarize the existing index-class and sister-class return legs on the identical 39-event cohort, verify their paired identity, and show additions and deletions separately with the inherited sign convention. This changes presentation, not the sample, return definition or original placebo procedure. Retain the existing source-consistent 29-event subset. Do not subtract this small selected log-return sample from the main arithmetic CAR as a causal decomposition; potential spillovers, repeated firms, liquidity differences and non-joint placebo draws remain.

The newly validated routines do not resolve the documented instability of some sparse inherited bootstrap intervals. Those limitations, all original audit facts and the incomplete external source reconciliation remain in the verification report. No new causal identification or independent confirmatory sample is claimed.


## Final narrative review against the supplied draft

After the earlier empirical audits, the authors supplied a Claude-prepared narrative draft. Its claims were reviewed individually. No primary return estimator or sample was changed for the narrative revision. The additional fund-flow table reorganizes existing production means on the same 136 later additions and reports a common analytical CR1 interval method. The simple event-level demand/return R-squared values were verified with residual sums of squares, squared correlation and statsmodels; both event types and both full/later samples are retained. These checks followed inspection of the supplied draft and are retrospective, not confirmatory discoveries.

The revision retains the useful economic sequence while removing unsupported claims of a sevenfold Swedish-US causal multiplier, universal absence of Swedish migrations, demand as a mathematical lower bound, and a causal upper bound inferred from the sister-class placebo interval. The production classification and mixed-fund weighting descriptions were corrected to match the code. See `claude_claim_audit.md` and `anchor_story_review.md`. `criteria_audit.md` distinguishes documented course requirements from inferred winner craft and unavailable detailed prize criteria.
