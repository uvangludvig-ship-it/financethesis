# The 2019 purge as an independent replication sample (agent report, 11 Oct 2026)

Files in `data/agent2019/` (build2019.py; t0_letters_sample, t1_exits_classified, t1_exits_by_month_class, t1_exits_by_period_class, t2_purge_funds_decomposition, t2_decomposition_summary, t2_receiver_groups, t3_destination_by_month, t3_totals_2019.json, t4_side_by_side_ftn, t5_examples_monthly).

## Method
Exit month M = first month absent from the panel, or the last observed month if it shows a forced signature (net trade below -80% of prior market value, or market value collapsing to under 25% with a residual row; 10% of purge funds). Default base = market value at M-1. Renumbering = same company, name core match, new fondnr within M-1 to M+3 (one-to-one). Merger/sibling default = receiver fund with abnormal inflow in M (max of net trade and return-adjusted market-value jump), same company or letter-verified cross-company pairs (12 fondhandelsebrev fetched from pensionsmyndigheten.se: Navigera/Zmart to Cicero World 0-100, Viking to Cicero Focus, Granit to Sensor, Inside/IKC to East Capital Multi-Strategi). Rest = default to AP7 Safa.

## Counts
Exits with M in 2018-11 to 2020-06: 405 (SEK 114.9 bn at M-1): 23 renumberings, 92 merger/sibling defaults, 290 AP7 defaults. 2019 alone: 322 exits, 90.7 bn gross, 9 renumberings (10.4 bn, mostly C WorldWide 1A SEK to 1A, Sep 2019), 80.4 bn net; purge sample = 313 funds, 949k savers, split 243 AP7-default (34.2 bn, 394k savers) vs 70 merger-default (46.2 bn, 555k; Robur MEGA to Access 17 bn, Ohman, SEB Generationsfonder, Alandsbanken). Pre-deadline exits Nov-Dec 2018: 50 funds, 18.3 bn (mostly mergers). The old project's 87.7/84.1 bn used another valuation month and renumbering rule.

## Voluntary share, 2019 purge (capital, raw / churn-adjusted)
w1 (last observed month only) 2.5% / 3.0%; w2 3.3 / 4.1; w3 3.9 / 5.2; fixed window from Jan 2019 4.3 / 6.9; from Nov 2018 5.3 / 8.3. AP7-default subsample: w1 2.3, w3 5.3, fix-Jan 6.4 (churn-adjusted 11.5). Merger subsample: w1 2.6, w3 2.8, plus receiver-based voluntary inside the move month 1.5% of capital. Savers: w1 1.3% (AP7 class 0.2%). Fund-level medians, funds above 100m: AP7 class w1 1.8% (p75 4.4), merger class 2.4%. Large tercile 2.3-3.5%, small funds noisy (10-18%).

## Destination, 2019 (Jan-Nov)
AP7 Safa has no handel_netto; proxy = AP7 Aktiefond + Rantefond net trade. Raw 35.7 bn, excess over 2018 median baseline 0.49 bn/month = 30.3 bn = 89% of AP7-class capital (72% with 1 bn baseline, 104% with 0); monthly match tight in the big months (May 7.6 vs 7.7 bn, Jun 14.9 vs 15.9 bn). Safa saver gain 274k = 73% of AP7-class savers. Matched receivers took 45.5 bn (99% of merger-class capital). Roughly 38% of removed capital went to AP7, 57% to designated sibling/merger funds, about 6% unexplained (voluntary in the move month plus noise); destination-based voluntary upper bound for the AP7 class 13%.

## Side by side with FTN
FTN exited losers (agent A): 67 funds, 75.6 bn, voluntary 6.0% capital / 5.6% savers, award to move 3-6 months; with the same short windows FTN gives w1 6.4%, w3 6.5%. 2019: 313 funds, 80.4 bn, w1 2.5%, w3 3.9%, 1.3% savers. 2019 voluntary is roughly half FTN's even over comparable windows, with the timing caveat below.

## Data problems
(1) Letters: no index; 12 fetched show letter-to-deadline 15-31 days (median 21), move 0-2 weeks after deadline, letter month = M-1 in 10 of 12; so w1 covers about half a month post-letter and the opt-out weeks inside M are invisible at fund level. (2) December placement inflates flows. (3) Net trade understates merger transfers; AP7 flows only via the building-block proxy. (4) About 45 funds that were themselves merger receivers before exiting contaminate windows (cleaned by replacing receiver months with baseline). (5) Some letters say "sammanlaggning" for funds classified AP7 (e.g. KPA Etisk Rantefond) when no receiver is visible. (6) AVSLUTSDATUM in the master list has a bulk 2019-11-07 date for 449 rows, useless for dating.

## Verdict
2019 works as an independent descriptive replication of "who moves the money": large N (313 funds, 80 bn, 950k savers vs 67 / 76 bn), same structure (letter, about three-week opt-out, default to a designated fund), and two default regimes (AP7 vs equivalent sibling fund, the latter closest to FTN's winner-fund design). Less clean than FTN: short and partly unobserved opt-out window, no fund-level AP7 flow, many small funds and mergers mixed in, letter dates unknown for most funds. Use as a robustness sample with the w1/w2 windows and the destination-based bound, not as a like-for-like point estimate.
