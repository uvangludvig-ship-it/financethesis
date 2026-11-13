# Follow-up analysis of persistence — analysis decisions

Recorded 2026-11-01 22:38 UTC, before computing the new paired contrasts.
This is an exploratory follow-up after seeing earlier results, NOT a blind preregistration.
Known results: positive matched addition return through ED+20 and imprecise levels at ED+60/+100.

Question: does the control-adjusted advantage shrink between ED+20 and ED+100?
Do not infer persistence from a non-significant reversal, or reversal from a non-significant level.

1. Reuse the already repaired T2 matching identities without rematching. Matching used information through AD-2, not outcome data, and did not exclude future index events. Primary specification: three controls, equal weight per review. One control is a declared sensitivity, not a replacement selected for significance.
2. Primary follow-up contrast: additions announced from 2017, CAR(AD-1,ED+100) minus CAR(AD-1,ED+20), event minus its same three controls. Require complete data through ED+100 for each of the four securities. Never replace a missing control with another stock. Report attrition and compare shorter-window estimates on complete vs available samples.
3. Report levels at ED+1, +20, +60, +100 on this identical sample, as well as ED+1 to +20, +20 to +60, +60 to +100 changes. Primary confidence interval: review-mean t interval. Restricted-null studentized wild bootstrap and sign-flip inference are sensitivity checks, with their symmetry/independence assumptions disclosed.
4. Secondary: deletions, pre-2017 events, and one-control results. Report all cells. No pooling additions and deletions to manufacture precision. Show leave-one-review-out and leave-one-issuer-out ranges for the primary contrast.
5. Same-support market-model sensitivity: alpha and beta estimated using AD-250 through AD-121 (at least 100 valid days), then subtract each stock's predicted daily return. This is separate from the replication's market-adjusted model. Keep the original three controls and report losses. No model chosen by significance.
6. Recompute old saved T5 regression on one identical sample across four horizons, including direct post-20 changes. This is an arithmetic diagnostic ONLY: historical eligibility, outcome-overlapping covariates and outcome-based candidate selection in that old analysis remain invalidating limitations. It does not override repaired T2.
7. No claim of permanent effects, causal mechanism, or exogenous assignment. Historical main-list eligibility is not independently verified for broad T2 controls. Shared issuer dependence across reviews is a limitation; issuer sensitivity will be reported. CAR is cumulative daily abnormal return, not a compounded investment return.
8. Save all inputs' hashes, complete event-level outputs, exclusions, coefficients, code and interpretation. Stop after these declared analyses unless a concrete programming/data defect requires correction; retain an amendment log.
