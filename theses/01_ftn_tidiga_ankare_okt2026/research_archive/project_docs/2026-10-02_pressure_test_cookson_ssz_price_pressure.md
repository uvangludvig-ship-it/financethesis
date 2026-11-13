> ARCHIVED 5 October 2026. An intermediate memo from 2 October. Its verdicts (Cookson as anchor; stock-level price pressure as headline) were overturned by the 5 October anchor decision. Some numbers here were later corrected (see `PLAN.md`). Kept for the record only.

# Pressure test: Cookson versus SSZ, and the design that survives

Prepared 2 October 2026. Inputs: the Cookson et al. (2021 RFS) PDF, the SSZ (2013 NBER WP / 2015 JF) text, Michael Klug's dissertation record (SSE 2023), Fondtorgsnämnden and Pensionsmyndigheten sources on the 2024 to 2026 procurements, and four independent referee reports (one per candidate design) each with its own minimum-detectable-effect arithmetic. This document supersedes `anchor_decision_cookson_vs_ssz.md` on the points listed in section 1.

## Verdict

Cookson is the better anchor than SSZ, but neither gives a headline test with power: every fund-level test on the 2024 to 2026 procurements (non-PPM flows, flow-performance sensitivity, post-award alpha) has 5 to 14% power against the published effect sizes. The identification is where the power is not; the power (the 2001 to 2023 panel) is where there is no recommendation to identify. The one design that is both identified and powered is stock level: the procurements are mandated demand shocks to the stocks the funds hold, and the cross-section of about 300 Swedish small caps gives an MDE inside the literature's range. This is Klug's question (announcement versus effective date, front-running, elasticity, predictability of inclusion) and Sabbatucci's (pension menu reallocations repricing stocks). The Berk and Green interest survives as the mechanism, not as a fund-level regression.

Whether it works turns on one number computable this week without looking at returns: how much of the gross flow-induced trading nets out because winners and losers hold the same stocks.

## 1. Corrections to the 2 October memo

- Cookson's listing effect is 0.16% of AUM per month (1.92% per year, t = 5.42) over the full sample and 0.06% per month (t = 1.91) after the 2014 ban, not "about 1% per year".
- Cookson does not show three-year outflows after deletion; Figure 1 follows four months after removal.
- Cookson's performance split is by agreement with Morningstar analysts (Table 7 panel B), not by affiliation; platform-only picks lean own-brand and high-commission and show no outperformance before the ban.
- Table numbers: 5 (listing logit), 6 (flows, fund-by-platform and year FE), 7 (performance), 8 (fees). There are no Tables IX or X.
- Dahlquist, Martinez and Söderlind (2017) is in the Review of Financial Studies, not JFQA.
- In the Swedish small-cap round, SEK 34bn is the whole category; about SEK 8bn moves from nine losers to five uncapped winners; five incumbents are capacity-capped and receive nothing.
- The three-regime extension (open registration 2001 to 2018, screened 2019 to 2023, procured 2024 onward, with the 2019 purge as placebo) does not survive refereeing. Registration before 2024 was the fund's own choice, so within-fund variation is launches, mergers and liquidations with their own mechanical flow patterns; the 2019 purge removed small, young funds whose percentage flows mean-revert on their own. Drop it. Keep 2001 to 2023 only as a flow-sensitivity benchmark and pre-period.
- The memo chose by question fit and replicability and never did the power calculation. That was the wrong order.

## 2. Cookson versus SSZ

| | Cookson et al. (2021 RFS) | Sialm, Starks, Zhang (2015 JF) |
|---|---|---|
| Their question | Does a gatekeeper's list move money and pick well | Who drives pension flows, sponsors or participants |
| What FTN is, in their terms | A curated list with additions and deletions | A sponsor added to a participant-only plan in 2024 |
| What their flow outcome measures | Investor response to a recommendation | DC versus non-DC money reacting to performance |
| What it measures in PPM after 2024 | Inside PPM: the agency's transfers (mechanical). Outside PPM: the behavioural analog, but noisy | The agency's scoring rule read back (quality 75% includes track record, then capital is moved) |
| Table-by-table replication | Tables 5, 7, 8 map cleanly; Table 6 maps only to non-PPM flows | Tables II, III, IX map on 2001 to 2023; Table VIII has no Swedish counterpart unless Pensionsmyndigheten supplies transferred capital per fund and date |
| Pre-2024 use | Baseline for visibility, not certification | Replicates PPM inertia already in Cronqvist and Thaler (2004) and DMS (2017 RFS) |
| Powered test on FTN | Fees (27 bp fall in Europe active against their 33 bp) and the selection logit. Flows and returns: no | None without the sponsor split, and marginal even then |
| Measurement trap | Non-PPM flow = Morningstar imputed flow minus PPM net trading; Morningstar's TNA-and-NAV imputation puts timing error into the subtraction with the same sign as treatment, in the transfer months (a 2% mismatch on a transfer worth 30% of AUM is 0.6% of AUM of fake flow, four times Cookson's effect) | Same trap; the December placement (about SEK 35bn in one month, above the monthly flow sd) contaminates every monthly moment; SSZ's annual autocorrelations are not comparable to monthly ones (monthly AR(1) 0.3 aggregates to annual 0.03) |
| Cookson's own analog to an outside certifier | Morningstar analyst rating has no significant direct effect on platform flows (Table 6) | |
| Fit to tutor and examiner | Index-inclusion logic for funds; fees and quality outcomes | Sticky-money motivation: why an agency can move SEK 100bn with 85 to 95% default acceptance |
| What to take | Selection logit with lagged stars, ratings, fees; the "picks Morningstar does not endorse" test as a certification benchmark; the fee table; the framing that a list mostly avoids losers | Flow decomposition; Table II as one condensed benchmark; the Berk and Green link in Table IX |

Cookson for the frame, SSZ for measurement and one paragraph of motivation. Neither as the source of the headline.

## 3. Power arithmetic

MDE = 2.8 standard errors (5% two-sided, 80% power). Assumptions stated; the referees ran these in code.

| Design and test | Assumptions | SE | MDE | Published effect | Power |
|---|---|---|---|---|---|
| A: non-PPM flow DiD, winners vs losers | sd 3 to 5% of AUM, AR(1) 0.3, 60 vs 100 funds, 14 post and 36 pre months, cluster by fund | 0.21 to 0.34% per month | 0.58 to 0.97% per month (7 to 12% per year) | Cookson 0.16 (full), 0.06 (post-ban) | 8 to 12%; 5 to 6% |
| A: calendar-time winners minus losers, pooled rounds | TE 0.5% per month, 27 months | 1.15% per year | 3.2% per year | Cookson 0.60 to 0.94 | 6 to 13% |
| A: same, one category | TE 1%, 14 months | 3.2% per year | 9.0% per year | | about 5% |
| A: pre-2024 panel | 400 funds, 276 months, about 59,000 effective obs | 0.025 to 0.041 | 0.07 to 0.12% per month | | sufficient, but no recommendation to test |
| B: regime difference in top-quintile Sirri-Tufano slope | once transfers (minus 100% months) enter PPM flow, sd rises from 2% to about 9% | | 0.106 to 0.22 per month | SSZ gap 0.1075 | marginal, and mechanical in any case |
| C: post minus pre alpha on inflow/AUM | sd 1.5 to 2% per month, 15 post months, 38 winners, dose sd 0.4 | 2.3 to 3.0 pp per doubling | 6.5 to 8.5% per year per doubling | at most about 2% per year (Zhu 2018, units to verify); CHHK 0.2 to 0.25; Reuter and Zitzewitz null | 5 to 14% |
| D: announcement CAR on net FIT, 300 stocks | daily idiosyncratic sd 2.5%, 7-day CAR sd 6.6%, FIT sd 1 pp of market cap | 0.38 clean; 0.75 after controls absorb half of FIT and a fat micro-cap tail | 1.1 to 2.1% CAR per 1 pp of market cap | multiplier 1.4 (Koijen-Yogo type, elasticity about minus 0.7) to 2.9 (median elasticity minus 0.34, Escobar, Pandolfi, Pedraza and Williams; Chang, Hong and Liskovich minus 0.46 to minus 1.5) | 46 to 97% on gross FIT |
| D: if net FIT is one third of gross | | 2.25 | 6.3 | | 9 to 25% |
| D: transfer window (42 days, CAR sd 16%) | | | 2.6 gross, 7.9 net | | weak |
| D: six-month reversal | | | 4.5 gross, 13.6 net | | weak |

Shrinkage does not rescue C: with posterior weight 0.06 to 0.16 on the data, shrinking the outcome scales slope and SE together; the t-statistic is unchanged. Shrinkage belongs on the pre-period baseline, where the winner's curse lives: high-dose winners are small and young, so their pre-period alpha is noisiest and most overstated (expected overstatement about 4.4% per year with a 24-month record versus 2.6% with 60 months, for true-alpha sd 1.5% and top-tercile selection), and that gap lines up with dose.

## 4. Design D: one question, stock level

Question content: when a pension gatekeeper moves capital between funds by decree, do the stocks those funds hold reprice, by how much per unit of demand, and does the market price it at the award or at the transfer.

Anchor and literature: Lou (2012 RFS) for flow-induced trading; Coval and Stafford (2007 JFE) for the event-time decile table and reversal; Chang, Hong and Liskovich (2015 RFS) for turning CAR into elasticity; Wardlaw (2020 JF) for measurement discipline; Klug's three essays and Sabbatucci, Tamoni and Xiao as framing; Cookson once (selection logit); SSZ once (why the money moves).

Construction: FIT_ie = sum over funds j of (expected change in fund j's PPM capital from event e) times w_ij divided by market cap_i; second versions scaled by average daily SEK volume and by free float (sum A and B shares; controlled small caps often float about half). Losers' outflow from the April 2026 Pensionsmyndigheten file; uncapped winners' inflow under the default mapping (pro rata across the five if not released). Frozen before the award: weights from 31 March 2026 FI holdings (Morningstar for foreign-domiciled C Worldwide, Evli, Danske), capitalisation at day minus 10. Using Q2 holdings or post-event capitalisation produces a spurious slope (Wardlaw's mechanism).

Tables:
1. The procurement as a demand shock: capital, funds, dates, gross and net FIT by decile, overlap ratio.
2. Headline: announcement-window CAR (open at day minus 5; Placera published a 25-stock at-risk list on 26 May 2026) on net FIT with size, value, momentum, Amihud controls, Swedish factors from SHoF; randomisation inference by rerunning with the frozen FIT vector on every non-overlapping 7-day window 2015 to 2025 (about 400) and ranking the event slope.
3. Falsification: the five capped incumbents' holdings as pseudo-FIT (same stocks, zero flow) must give zero.
4. Implied multiplier with interval, beside Chang, Hong and Liskovich, Koijen and Yogo, Klug.
5. Predictability: leave-one-round-out regularised logit and gradient boosting of P(win | bid) on fees, 1, 3 and 5-year ranks, size, age, stars, incumbency, bank affiliation; out-of-sample AUC against the simple rule FTN publishes (fee rank plus track record); a surprise-weighted FIT column in table 2 (Klug chapter 3 transplanted).
6. The 2025 Nordic small-cap cycle as the completed replication (announcement, transfer, six-month reversal); three of four winners were incumbents, so check moved capital first.
7. Berk and Green link: fund-level liquidity dose sum of w_fs times NetDemand_s / ADV_s against the Kacperczyk, Sialm and Zheng return gap over transfer months; the alpha-on-dose regression reported once with its MDE as an explained null.

Quant and ML elements, each tied to an objection: randomisation inference (one date, dependent CARs); Wardlaw-frozen FIT and free-float scaling; elasticity translation; leave-one-round-out ML with honest AUC used for surprise weighting; empirical Bayes on pre-period alphas against the winner's curse; stacked design with permutation of winner labels within round for anything pooling rounds. Six tests over four events is the ceiling; no more.

Referee objections and fixes: overlap (section 6); anticipation (losers sell over the summer; measure pre-trading from FI Q1 versus Q2 weights and June to September PPM net trading; recast the transfer test as "was anything left"); cross-sectional dependence (randomisation inference); scaling (free float); the global round's court challenge is irrelevant (SEK 96bn across global large caps is FIT near 0.001%), but confirm the small-cap award was not challenged.

## 5. Klug's findings

SSE PhD 2023, "Essays on Index Investment: index inclusions, managerial skill, and the rise of passive management", main supervisor Magnus Dahlquist. (1) With Felix Wilke: an index inclusion premium of 84 to 208 bps around Russell constituent changes (the 2023 EFMA working-paper version reports 1.8 to 3.9%), a subset of active funds that trade on constituent changes, and the cost imposed on passive investors. (2) Price elasticities measured around quarterly IPO inclusions: downward-sloping demand confirmed; passive growth has not changed efficiency. (3) Machine learning prediction of index inclusions: a simple rule replicating the index methodology forecasts as well as ML; ML-based portfolios are more profitable. A procurement is an index reconstitution where the index is a pension menu and the passive investor is the saver who accepts the default. Sabbatucci, Tamoni and Xiao estimate a demand system for 401(k) menus and find aggregate repricing of about 10% from active-to-passive shifts; Design D is the reduced-form version of that object on a Swedish shock.

## 6. Go/no-go this week, and timeline

Compute before any return is downloaded: sd(net FIT)/sd(gross FIT) across stocks; residual sd of net FIT after partialling out size, book-to-market, momentum and Amihud; the share of the sum of squared FIT carried by the top ten stocks. Pre-committed rule: residual net-FIT sd of at least 0.5 pp of market cap (1 pp if the multiplier is believed nearer 1.4) means D is the thesis; below that, D is one figure inside the fallback. Intuition for the tail from Placera's 26 May list: Exsitec and Micro Systemation at about 30% Swedish fund ownership on SEK 1.4 to 1.5bn market caps; 25 stocks between 11% and 31%; the PPM share of the losers' holdings in those names is the quantity of interest.

Runnable today: the 28 May announcement test, pre-trading diagnostics, the Nordic 2025 cycle, the ML prediction if bidder lists are obtained under offentlighetsprincipen. October to November: the transfer window, but the October Pensionsmyndigheten file lands around mid-November and the November file after 7 December. Design so the announcement is the headline and the transfer window a labelled first look against the published schedule. Reversal and the fund-level dose test run only on 2025. The 2019 purge moved non-choosers' capital to AP7 Såfa (confirmed in Pensionsmyndigheten deregistration letters): a one-sided sell shock from several hundred funds; check scale in the 2019 files.

## 7. Fallback if the diagnostic fails

Design A with the headline moved to the Cookson Table 5 selection logit (with bidder scores) and the Table 8 fee comparison (27 bp against Cookson's 33), flows and returns demoted to a stacked, permutation-tested bounded null, the pre-2024 panel kept only as the flow-sensitivity benchmark, and D as one figure. Prize-capable but modest; fails gracefully. Precedent for D: the 2020 leveraged-ETF winner (single issuer, Swedish tick data, R-squared 0.02).

## Data requests to send now

- Pensionsmyndigheten: monthly fund files 2018 to 2026 with net trading by transaction type (placement, switch, transfer); transferred capital per losing fund, per receiving fund and date for each completed round; the default mapping rule.
- Fondtorgsnämnden (offentlighetsprincipen): bidder lists and evaluation scores per round.
- Finansinspektionen: quarterly holdings Q4 2024 to Q3 2026 for the Swedish-domiciled funds in the small-cap, Nordic small-cap and Europe small-cap rounds.
- SHoF: daily Swedish factors through mid-2026; Morningstar holdings for the foreign-domiciled losers.

## Sources

- Cookson, Jenkinson, Jones, Martinez (2021), RFS 34(1), 227 to 263.
- Sialm, Starks, Zhang (2013 NBER WP 19569; 2015 JF 70(2), 805 to 838): https://www.nber.org/system/files/working_papers/w19569/w19569.pdf
- Klug (2023), Essays on Index Investment, SSE: https://research.hhs.se/esploro/outputs/doctoral/Essays-on-Index-Investment-index-inclusions/991001547399306056
- Klug and Wilke, Trading on Index Constituent Changes (EFMA 2023): https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2023-UK/klug.pdf
- Sabbatucci, Tamoni, Xiao, Stock Demand and Price Impact of 401(k) Plans: https://research.hhs.se/esploro/outputs/workingPaper/Stock-Demand-and-Price-Impact-of/991001524896506056
- Escobar, Pandolfi, Pedraza, Williams, Who Trades Index Rebalancings? (CSEF WP 621): https://www.csef.it/WP/wp621.pdf
- Reuter and Zitzewitz (2021), Review of Finance 25(5): https://www.nber.org/papers/w16329
- Pensionsmyndigheten, procurement schedule: https://www.pensionsmyndigheten.se/forsta-din-pension/valj-och-byt-fonder/upphandlat-fondtorg
- Fondtorgsnämnden, Swedish small-cap award 28 May 2026: https://news.cision.com/se/fondtorgsnamnden/r/fondtorgsnamnden-meddelar-tilldelningsbeslut-i-upphandlingen-av-svenska-smabolagsfonder,c4352002
- Placera, 26 May 2026, at-risk small caps: https://www.placera.se/nyheter/pensionsrisk-i-smabolagen-har-ager-svenska-fonder-mest-2026-05-26
- EFN, 3 September 2026, transfers and 25 September deadline: https://efn.se/nu-flyttas-ppm-pengarna-da-behover-du-agera
- Pensionsmyndigheten 2019 deregistration letter (capital to AP7 Såfa): https://www.pensionsmyndigheten.se/content/dam/pensionsmyndigheten/blanketter---broschyrer---faktablad/fondh%C3%A4ndelsebrev/2019/FHB0010575%20Alfred%20Berg%20Nordic%20Equity%20Momentum%20avregistrering%20.pdf
