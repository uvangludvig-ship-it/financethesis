# Exploratory audit specification

Recorded on 12 November 2026 before running the new audit calculations. This is not a preregistration: inherited results, several return paths, and earlier analysis decisions were already known.

Source commit: d2d41666ed213e4cc1f6cb382313f59c29e87ea0.

1. Independently rebuild market-adjusted daily returns from the frozen price files. Check all inherited announcement, implementation, and total-window CARs; sample attrition; date alignment; and return fallback use. Retain the original sample rules, with separate sensitivity to exclusions.
2. Independently reproduce the event-weighted mean and CR1 standard error, report equal-review weighting, leave-one-review-out estimates, security and review two-way clustering, and cluster jackknife standard errors. These are sensitivity analyses, not a selection procedure for the preferred p-value.
3. On a fixed complete-case cohort, compute non-overlapping CARs [AD-1, ED-1], [ED, ED+20], and their sum [AD-1, ED+20]. A residual cumulative return does not establish a causal or permanent price effect. Report all periods and both event types, not only significant cases.
4. For the demand-scaled return ratio, report Fieller confidence sets based on the joint review-clustered covariance of the numerator and denominator, alongside the inherited percentile intervals. Do not discard draws or parameter values because a denominator changes sign. Label these as asymptotic sensitivity calculations, especially for sparse early periods.
5. Report Holm-adjusted inherited p-values for a declared audit family: the eight five-year total-window means and the two earliest-versus-latest contrasts. This family does not account for all historical researcher choices; it is not a new confirmatory family.
6. Explicitly test the one-sided practical-equivalence question using a prespecified audit margin of plus/minus 1 percentage point for the latest-period CAR. The margin is a transparent reporting benchmark chosen after seeing old results, not an external economic threshold or preregistered target.

No FTN outcomes are opened. No new causal design is claimed. All results, including failures and ambiguous intervals, remain in the audit output.

Follow-up recorded after inspecting the new horizon results: apply the inherited Sivers, MSCI-overlap and company-news exclusions separately to the cumulative horizon, for both event types and both later periods. These checks are post-result exploration. The independent horizon bootstrap uses 49,999 draws with a finite-simulation correction; its p-values are reported beside, not as the inversion of, analytical CR1 intervals.
