# 06. What the data say before any hypothesis test (measured 11 Oct 2026)

Everything here is descriptive: counts, shares, sums. No treatment coefficient, no stock or fund return around an FTN date has been looked at (blind rule). Scripts and CSVs for facts 1 to 5 are in `data/facts/` (run from `common.py`; the panel is `ppm_panel_2018_2026.csv`, 53,062 fund-months, Jan 2018 to Aug 2026, built from Pensionsmyndigheten's monthly files; 22 duplicate fund-months in June 2018 dropped; AP7 excluded). Facts 6 to 9 were measured earlier the same day from the same panel plus FI holdings and the FTN reports; their scripts and outputs are in `data/measurements/` with pointers to the full files.

## Fact 1. The appeal round: information without a default move does nothing

Global active, awarded 24 Feb 2026, frozen by Indecap's appeal, nothing moved through Aug 2026. Losers = the 45 funds in FTN report section 4.1 minus 6 incumbent winners minus AXA (left Oct 2025) = 38 funds, 125.5 bn SEK, 606,560 savers at Feb 2026.

Pooled monthly net trade, per cent of lagged market value:

| window | losers (38) | incumbent winners (6) |
|---|---|---|
| Sep 2025 to Jan 2026, ex Dec | -0.49 | -0.29 |
| award month, Feb 2026 | -0.83 | -0.38 |
| Mar to Aug 2026, mean | -0.21 | -0.14 |

Cumulative after award, event months 1 to 6, losers: capital -0.78, -1.26, -0.92, -1.35, -1.47, -1.22 per cent (ex Evli Global, a merger receiver in Aug 2026: -1.85 at month 6); savers -0.63, -1.02, -1.35, -1.64, -1.69, -1.18 per cent. Median fund: capital -2.2, savers -2.2 per cent over six months. Control (135 equity funds in categories not yet procured, same window): median -1.5 per cent capital, -1.9 per cent savers. For comparison, losers in executed rounds in the months before their move: month 1 mean -0.34, month 2 -1.82 per cent (ex Dec -2.21); beyond month 2 most rounds had already moved.

Reading: being told that the fund will leave the platform, with nothing forced, releases 1 to 2 per cent of capital and savers in six months, no faster than ordinary attrition; winners do not gain. This is the cleanest statement in the whole setting that the forced flow is not a saver decision.

## Fact 2. Men opt out 1.5 times more than women, in both episodes

Opt-out = decline in saver count from award month to the month before the move, by sex.

| sample | funds | savers (w / m) | women | men | gap, pp | ratio |
|---|---|---|---|---|---|---|
| FTN pooled, 9 rounds | 78 | 335k / 435k | 4.85 % | 7.11 % | 2.26 | 1.47 |
| FTN, losers of 1 bn or more | 25 | 278k / 367k | 5.07 | 7.32 | 2.25 | 1.44 |
| 2019 purge, AP7-default exits | 234 | 167k / 203k | 5.10 | 8.29 | 3.19 | 1.63 |

Capital-weighted (return-adjusted): FTN women 5.8 versus men 8.6 per cent; 2019: 6.4 versus 9.4. Men higher in 63 of 78 FTN funds and 176 of 234 purge funds, and in every FTN round except two tiny ones (European small cap, 3 funds; Nordic active, net inflows). Baseline attrition in untreated equity funds over the same windows: 0.2 to 0.4 per cent for both sexes, gap about zero. Women are 43.5 per cent of loser savers and hold 125k versus 147k SEK per saver. Problems: net saver change understates gross exits; December windows add capital but not savers. The strongest of the five facts: two independent episodes, 770k plus 370k savers, same direction.

## Fact 3. Winners did not create PPM share classes; the fee cut is a rebate on the same ISIN

49 winners with an observed contract (Global active and Tech not implemented). Only 4 of 49 (8 per cent) use a PPM-dedicated class where gross equals net: Nordea 1 European Stars, Mercer Passive Global, SEB Nordic Small Cap, Cliens Sverige; all four are new to the platform (4 of 22 new, 0 of 27 incumbents). 19 use a cheap or institutional class with a small rebate (gap 0.03 to 0.5 pp), 26 a retail class with a large rebate (gap above 0.5 pp). Incumbent winners all kept their ISIN; mean fee cut 0.086 pp (capital-weighted 0.074). PPM share of fund TNA for SEK incumbents (18 observed): mean 33, median 32 per cent; 14 of 18 have PPM below half of TNA and all use a rebate class, so there is no variation to test a "retail base" story. Coverage gaps: 10 EUR and 2 NOK funds (no FX), 8 without TNA, 11 not on the platform before award. Consequence: the price-discrimination question (Q9 in file 01) is dropped.

## Fact 4. Fee savings are 178 MSEK a year, 102 SEK per affected saver, and FTN's category averages overstate them 1.8 times

Panel `fee_net`; moved capital priced at the inflow-weighted winner fee. Executed rounds through Swedish index:

- stayers in 28 incumbent winners: 160 bn x cut = 118 MSEK a year, 1.07 m fund-savers, 110 SEK per saver;
- 92 bn moved from losers: 60 MSEK a year (68 at equal-weighted winner fee), 668k savers, 90 SEK per saver;
- total 178 MSEK a year, 102 SEK per affected saver per year; 222 MSEK including the pending small-cap rounds.

By round, MSEK a year: European active 8, European index 12, Global index 41, Nordic active 10, Nordic small cap -3 (Nordea Smabolag Norden rose 0.27 to 0.35 on 7 bn), Swedish active 79, Swedish index 30 (Avanza Zero 0.00 to 0.04 costs -8), European small cap 4, Swedish small cap 40.

Check against FTN's own framing: FTN's equal-weighted before-fee category averages times the same capital give 328 MSEK a year, 1.8 times higher, because the capital sat in the cheap incumbents (capital-weighted before-fee 0.12 to 0.32 versus FTN equal-weighted 0.13 to 0.52). Savers are fund-saver pairs (one person can be counted in several funds). This is the benefit side of the cost-benefit in file 07.

## Fact 5. Concentration: top-5 companies 90 to 97 per cent of procured capital

Procured sub-category universe, award versus latest, capital-weighted and pooled: top-5 company share 90.2 to 96.5 per cent; HHI 2,548 to 2,997; funds 106 to 64; companies 88 to 55 (with overlap); Swedish-managed share 91.7 to 90.3 per cent. By round (top-5 / Swedish share): European active 91 to 94 / 55 to 49; Global index 94 to 100 / 95 to 86; Nordic active 81 to 100 / 64 to 50; Swedish active 85 to 93 / 97 to 96; Swedish index 92 to 100 / 97 to 100; small caps unchanged (moves pending). Mostly mechanical from fewer funds: a table at most.

## Fact 6. 94 per cent of the capital moves by default (97 per cent in 2019)

FTN rounds with completed exits (to Aug 2026): 67 losers, 75.6 bn SEK, 580k saver-funds. Voluntary outflow between award and the month before the move: 4.6 bn (6.0 per cent of capital, 5.6 per cent of savers); 71.1 bn (94 per cent) moved on the agency's order. Including Avanza Zero's pending tranches: 69 losers, 97.2 bn, 7.0 per cent voluntary. 2019 purge: 313 funds, 80.4 bn; voluntary 2.5 per cent (one-month window) to 3.9 per cent (three months); 243 funds (34 bn) defaulted to AP7 Safa, 70 funds (46 bn) to a sibling fund of the same company. Sources: `data/measurements/agentA_summary_by_round.csv`, `data/measurements/agent2019_t4_side_by_side_ftn.csv`.

## Fact 7. The executed transfers are dated to the month and are large relative to the funds

From the panel's "Handel, netto" and residual exits (`data/measurements/execution_windows_monthly.csv`):

- Swedish active (18 losers, 21.2 bn at award): 51 per cent of award capital left in Jan 2026, 34 per cent in Feb, 11 per cent in Mar; 6 new winners received 45, 36 and 6 per cent of that capital in the same months.
- Swedish index (8 losers, 37.6 bn incl. Avanza Zero): about ten monthly tranches Oct 2025 to Aug 2026 (8, 28, 7, 19, 18, 5, 6, 8, 3, 2 per cent). Avanza Zero drained from 22.1 to 2.7 bn.
- Nordic active (7 losers, 6.7 bn): May 2025 14, Jun 68, Jul 15 per cent.
- Global index (8 losers, 23 bn): Mar 2025 17, Apr 59, May 14 per cent.
- Swedish small cap (9 losers, 8.9 bn): closed to new choices 18 Aug 2026, choice deadline 25 Sep 2026, execution Oct 2026 (in progress during the thesis).
- European active (20 losers, 7.8 bn) and European index (3 losers, 0.7 bn): 2024, before the panel's `upphandlad` flag starts.

Pensionsmyndigheten's own process document ("Avslutsprocess", for fund companies) states that the exit order is 100 per cent of the holding on one day ("Vi har tyvarr inte mojlighet att dela upp var avslutsorder") and that letters go out about two weeks before. Exact days are not published; they can be read off daily TNA and units outstanding in the SHoF Morningstar files, or requested from Pensionsmyndigheten.

## Fact 8. Stock-level pressure: Swedish small cap and Swedish active carry the design; the index round is placebo-strength

FI quarterly holdings (VPFO) on disk for 2023Q4, 2024Q1, 2024Q2, 2026Q2, matched to 77 to 95 per cent of loser capital. Pressure per stock = net SEK bought minus sold across losers and winners, divided by company market cap (FIP, per cent). No returns used.

| round | sd of FIP across names | notes |
|---|---|---|
| Swedish active (21 bn) | large caps 0.15 pp; all names with approximate caps 0.25 to 0.35 pp; 33 to 47 names above 0.25 per cent, 10 to 18 above 0.5, max 1.2 | buy and sell legs correlate 0.82 to 0.89, so net is 30 to 34 per cent of gross; top-10 names hold 62 to 72 per cent of squared net |
| Swedish small cap (8.9 bn) | 0.56 to 0.73 pp (earlier evaluation on 2024Q2 holdings) | highest dose; executing Oct 2026 |
| Swedish index (38 bn) | 0.05 to 0.09 pp, max 0.3 | losers track OMXS30, SBX, SIXPRX; winners track SIX 30 SRI, Solactive ESG Sweden 100, SIX Sweden SRI, Solactive ESG Select, SBX; signs predictable (Evolution -0.21, Saab -0.17, H&M -0.09; Investor B, Industrivarden, Epiroc, Indutrade, SSAB +0.13 to +0.16), dose about 0.02 per cent per tranche |
| Nordic active (6.7 bn) | 0.04 pp, max 0.17 | low |
| Global index (23 bn) | negligible, 3,017 names | diffuse |

Full per-name files: `financethesis_revised/data/agentP/` (79 MB, not duplicated here); summaries in `data/measurements/fip_summary.csv` and `fip_allnames_summary.csv`.

## Fact 9. Fund-level facts that matter for "who pays"

- Pensionsmyndigheten's stake in the large losers at award: Avanza Zero 41, Storebrand Sverige 41, Ohman Sverige 44 per cent of NAV; typical range 20 to 44 per cent (`data/measurements/agentA_task2_loser_decomposition.csv`).
- Swedish swing pricing (justerat fondandelsvarde) has been legal since 1 July 2023 (prop. 2022/23:65; FFFS 2013:9 ch. 31 s. 48b requires the annual and half-year report to state the factor actually applied). SEB adopted it for 41 funds from 14 Mar 2025 with a maximum factor of 1 per cent. Pensionsmyndigheten asked in its 2022 consultation response that the tool be made mandatory. Other companies' adoption: NOT VERIFIED, to be read fund by fund in fondbestammelser and annual reports (file 03).
- Fund TER (gross fee) is unchanged for every winner; only the PPM rebate changes (`data/measurements/winners_fee_series.csv`; Morningstar FEES.txt has no history).

## Data problems to carry into the design

- The `upphandlad` flag starts Nov 2024, so round 1 contract fees are observed only from then.
- Move-start detection from monthly data misses staggered moves (Avanza Zero still held 2.7 bn and 95k savers in Aug 2026).
- December rows carry new pension rights (+1.2 to 1.6 per cent in all funds); exclude December from flow windows.
- Merger receivers contaminate pooled flows (Evli Global 2026, Monyx 2019); handled by exclusion.
- Morningstar TNA is unusable for non-SEK funds without an FX series.
- Exact redemption days are not in any public file; needed for the exit-day dilution table and for the event-day CARs.
