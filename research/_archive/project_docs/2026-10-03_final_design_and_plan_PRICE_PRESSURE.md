> ARCHIVED 5 October 2026. This was design C (price pressure from FTN's transfers, anchored on Da, Larrain, Sialm and Tessada 2018). It lost the anchor decision on 5 October and is NOT the thesis. Kept for the record only. The current plan is `PLAN.md`.

# Final design and plan: price pressure from Fondtorgsnämnden's mandated transfers

Prepared 2 October 2026, revised 3 October 2026 after an examiner-style audit of the anchor (full text of Da et al. 2018) and a first measurement of portfolio overlap from public 2026Q2 holdings. Supersedes the anchor label in `pressure_test_cookson_ssz_price_pressure.md`.

## Question

Fondtorgsnämnden ordered about SEK 8bn of default pension capital out of nine Swedish small-cap funds, announced it on 28 May 2026 and carried it out from late September 2026. How much does a known, informationless demand shock move the prices of the stocks involved, per unit of net demand, and how much of that arrives at the announcement versus the execution?

## Anchor

Da, Larrain, Sialm and Tessada (2018), "Destabilizing Financial Advice: Evidence from Pension Fund Reallocations", RFS 31(10), 3720 to 3755 (editor Goldstein). Chile: advisor emails move USD 1 to 4bn (up to 20% of fund assets) between equity and bond pension funds; funds trade up to 10% of domestic equity; the stock market rises 1.06% on day 1 (SE 0.29), 1.22% by day 3, back to 0.33% by day 10; elasticity minus 0.45; cross-section (Table 11, FIP = flow x weight / market cap): 3.61 on day 3 (SE 1.53), 0.71 on day 1 (insignificant); day minus 1 effect of 0.64% excluded; funds respond by holding more cash. The earlier figures "2.5% peaking on day 8" came from the 2015 working paper and are wrong.

Their Section 3 question (do uninformative pension flows move prices) is the thesis question; their title question (does advice destabilise) is not, and the thesis says so.

Supporting: Lou (2012 RFS) for flow-induced trading and partial scaling; Coval and Stafford (2007 JFE) event time; Chang, Hong and Liskovich (2015 RFS) elasticity; Wardlaw (2020 JF) frozen weights; Greenwood (2005 JFE) for the arbitrage model and the spillover prediction; Lynch and Mendenhall (1997) and Greenwood (2005) as precedents for announcement versus effective-date splits (so that split is not claimed as new in general, only for a pension reallocation by decree). Klug and Sabbatucci, Tamoni, Xiao cited once each as framing.

## Replication map (DLST table to thesis)

| DLST | Replicable | Swedish analogue | Deviation to state |
|---|---|---|---|
| T1 funds | Yes | Losers, new winners, incumbents: PPM and total AUM, fee, domicile | One risk class |
| F1 switches | Partly | Losers' daily TNA and flows | Flows, not people |
| T2 events | Yes | Award, closure, deadline, transfer per round; stock-level demand vector | Same-day rounds collapse to about three dates |
| T3 drivers | Partly | Logit of losing on fee and past return | Selection, not timing |
| T4 advice returns | No | None | Not applicable |
| F2 flows | Yes | Monthly PPM capital in losers, winners, incumbents | SEK |
| T5 young investors | Partly | First stage: realised outflow on allocation-rule outflow | No demographics |
| F3, T6 event time | Partly | Net-FIP-weighted long-short portfolio, days minus 10 to plus 20 around award and around each loser's TNA drop | Spread, not index; day 0 is the release day |
| T7 placebos | Yes | Frozen FIP vector on random dates; same-day Europe small-cap award with near-zero Swedish flow | Randomisation, not probit |
| T8 time series | Yes | Long-short portfolio 2018 to 2026 with SHoF factors | Few dates; not the headline |
| T9 subsamples | Partly | Buy vs sell side, liquidity terciles | Within event |
| T10 volume by broker | No | Total turnover only | No broker IDs on Nasdaq Stockholm |
| T11 cross-section | Yes (A, B), No (C) | Headline: CAR and turnover on net FIP, award and transfer side by side | Two-sided FIP |
| T12 volatility | Partly | Transfer months | Few treated months |
| T13, F4 fund response | Partly | Losers' and winners' cash and liquid holdings, FI Q1 vs Q2, incumbents as control | Quarterly |

## Overlap, first look (3 October 2026, top-10 holdings, 2026Q2)

- 53 distinct names in the 14 funds' top-10 lists; 26 shared, 18 losers only, 9 winners only.
- 55 to 62% of losers' top-10 exposure is matched by the five new winners; the overlap is in liquid names (Nordnet, Beijer Ref, Avanza, Addtech) where FIP is negligible.
- Losers-only names: Securitas, Gränges, Hoist Finance, Medicover, Puuilo, Castellum, Hiab, Lifco, Indutrade, Bergman & Beving, Lindab, Ambea, Attendo. The illiquid tail (XANO, Green Landscaping, Elanders, MedCap, Balco, Proact, Coor) is outside top-10 lists and is where the shock sits; winners largely do not hold it.
- Cross-check: Placera's SEK 125m sell pressure on Hoist equals Carnegie's PPM capital 2.14bn x 5.4%; MedCap's 144m equals Spiltan's 2.28bn x 5.2%.
- PPM capital known: Spiltan 2.28bn (48.7% of fund), Carnegie 2.14bn, Evli about 48.5% of fund (Placera). Others by request.
- Identification will rest on perhaps 20 to 40 stocks with net FIP above 0.5% of market cap: inference must be randomisation-based, with leave-one-stock-out and liquidity-scaled FIP.
- The go/no-go number still needs the full FI 2026Q1 lists.

## Mistakes to pre-empt (examiner's list)

- Sign: every Swedish event is two-sided; sign by each stock's net FIP, net same-day rounds before stacking.
- Flows: award test uses allocation-rule (ex-ante) flow; transfer test uses realised daily-TNA drops instrumented by the ex-ante flow.
- Holdings: Q2 is post-award; use Q1 share counts at pre-award prices; foreign-domiciled Danske, Evli, C WorldWide from factsheets with dates.
- Benchmark: not MSCI World, OMXS30 or the Carnegie Small Cap index (contains treated stocks); matched zero-FIP small caps or SHoF four-factor residuals over days minus 250 to minus 30.
- Standard errors: randomisation inference with the frozen FIP vector on historical dates; wild cluster bootstrap only when pooling 2025 rounds.
- Ask Pensionsmyndigheten whether transfers are cash or in kind.

## Expectations

Elasticity between about minus 0.5 and minus 2 in total, mostly at the award; transfer window near zero or reversing. A zero transfer effect is read as "priced at the award", with the award estimate as the measured mechanism.

## Claims

Can claim: price impact of a mandated, informationless, pre-announced reallocation on a two-sided demand vector, and its split between announcement and execution. Cannot claim: destabilisation, anything about advice, retail behaviour, generality beyond one sharp round, or novelty of the announcement/effective split in general.

## Timing (corrected)

Swedish small cap: award 28 May 2026; losers closed 18 Aug; letters late Aug; saver deadline 25 Sep (Carnegie letter); transfers late Sep to Oct 2026, per fund, dates not published. Detect transfer dates from daily fund capital: Avanza endpoint avanza.se/_api/fund-guide/guide/{orderbookId} returns fund capital and holdings (30 Sep 2026); poll daily from 6 Oct. Later confirm with SHoF Morningstar daily TNA and the Pensionsmyndigheten request. Europe small cap: three losers (Allianz Europe Small Cap, BL European Small & Mid Caps, Lannebo Europa Småbolag) closed 7 Jul 2026. Nordic small cap: two losers (Aktia Nordic Small Cap, Fondita Nordic Micro Cap) closed 16 Apr 2025, transfers about mid-May 2025.

## Data

| Need | Source | Status | Catch |
|---|---|---|---|
| Stock-level fund holdings | FI quarterly XML, 2018Q4 to 2026Q2 | Public | Swedish-domiciled only; Danske, Evli, C WorldWide from factsheets; confirm ISIN and share counts |
| Daily fund capital and holdings | Avanza fund-guide endpoint; SHoF Morningstar daily TNA | Public / SSE | Avanza needs orderbookId from each fund's URL |
| PPM capital per fund, demand vector | FTN award report (19 bids, 10 winners with fee, allocation rule); Placera for Spiltan, Carnegie, Evli; Pensionsmyndigheten by request | Partly | Per-fund PPM capital at 31 Mar 2026 by request |
| Transfer amounts and dates | Avanza/SHoF daily capital; Pensionsmyndigheten request (cash or in kind) | Partly | Request aggregates only |
| Daily prices, market cap, turnover | FinBas (SHoF) | SSE | Free float from LSEG |
| Daily Swedish factors | SHoF | SSE | Confirm end date |
| Bidder scores | FTN evaluation records | Request | Redaction likely |

## Plan

- Weekend to Mon 5 Oct: Avanza polling script; FI 2026Q1 download; factsheets for the three foreign funds; requests to Pensionsmyndigheten, FTN, SHoF; DiVA search for "Fondtorgsnämnden".
- Week 1 (5 to 9 Oct): demand vector from the allocation rule; net FIP per stock by market cap and ADV; go/no-go numbers (sd net/gross, residual sd after controls, top-ten share of squared FIP); pre-analysis plan with predicted spread written before any return is opened; Klug meeting with the number.
- Week 2 (12 to 16 Oct): headline Table 11 analogue at the award (days minus 10 to plus 5 around 28 May), randomisation inference, incumbents-only placebo, elasticity beside DLST's two numbers.
- Week 3 (19 to 23 Oct): stacked event-time replication of T6/F3 on Nordic small cap 2025, Europe small cap 2026, Swedish active 2025 (zero-FIP comparison); reversal to 120 days.
- Week 4 (26 to 30 Oct): pre-trading (T13 analogue, FI Q1 vs Q2, incumbents as control); leave-one-round-out P(win | bid) with AUC; surprise-weighted FIP column.
- Week 5 (2 to 6 Nov): transfer-window test on the detected transfer dates (realised flows instrumented by ex-ante); fee table and cost-vs-saving sentence; methods and deviations paragraph.
- Week 6 (9 to 13 Nov): robustness (float and ADV scaling, windows, winsorising, leave-one-stock-out, weights).
- Week 7 (16 to 20 Nov): introduction and conclusion with numbers; conclusion calibrated per `conclusions_winners_vs_nonwinners.md`.
- Week 8 (23 to 27 Nov): full draft to Klug.
- Week 9 (30 Nov to 4 Dec): references, AI-use appendix, no table of contents, 20 to 30 references. Submit 7 Dec.
- Fallback, decided 9 October only: if residual net FIP is under 0.5 pp of market cap, switch to fee spillover with the closet-indexing selection table; price pressure becomes one figure.

## Sources
- Da, Larrain, Sialm, Tessada (2018) RFS: https://academic.oup.com/rfs/article/31/10/3720/4835372
- Lou (2012) RFS 25(12), 3457 to 3489
- FTN Swedish small-cap report: https://mb.cision.com/Main/23067/4352002/4118846.pdf ; European: https://mb.cision.com/Main/23067/4351974/4118844.pdf ; Nordic: https://mb.cision.com/Main/23067/4106627/3270853.pdf
- FI holdings register: https://fi.se/sv/vara-register/fondinnehav-per-kvartal/
- Pensionsmyndigheten: nine small-cap funds closed 18 Aug 2026: https://www.pensionsmyndigheten.se/nyheter-och-press/nyheter-fondtorg/nio-svenska-smabolagsfonder-ar-inte-langre-valbara ; three Europe small-cap funds closed 7 Jul 2026: https://www.pensionsmyndigheten.se/nyheter-och-press/nyheter-fondtorg/tre-europeiska-smabolagsfonder-ar-inte-langre-valbara ; two Nordic funds closed 16 Apr 2025: https://www.pensionsmyndigheten.se/nyheter-och-press/nyheter-fondtorg/tva-norden-fonder-ar-inte-langre-valbara-pa-fondtorget ; timetable: https://www.pensionsmyndigheten.se/forsta-din-pension/valj-och-byt-fonder/upphandlat-fondtorg
- EFN 3 Sep 2026 (Carnegie letter, 25 Sep deadline): https://efn.se/nu-flyttas-ppm-pengarna-da-behover-du-agera
- Placera 26 May 2026: https://placera.se/nyheter/pensionsrisk-i-smabolagen-har-ager-svenska-fonder-mest-2026-05-26 ; 28 May 2026 (PPM capital per fund, days of volume): https://placera.se/nyheter/experten-aktierna-som-pressas-mest-av-ppm-beslutet-2026-05-28
- Holdings via Börskollen fund pages (FI 2026Q2 reports), Nordnet fund pages, Danske factsheet: https://danskeinvest.dk/docs/FACTSHEET_5879_77_sv.pdf
- SHoF FinBas: https://www.houseoffinance.se/data-center/finbas/ ; factors: https://www.houseoffinance.se/data-center/fama-french-factors ; fund data: https://www.houseoffinance.se/data-center/shof-fund-data-morningstar/
- Global round and court challenge: https://www.placera.se/nyheter/31-globalfonder-aker-ur-ppm--avgiften-halveras-2026-02-24
- Klug: https://research.hhs.se/esploro/outputs/doctoral/Essays-on-Index-Investment-index-inclusions/991001547399306056 ; Sabbatucci, Tamoni, Xiao: https://research.hhs.se/esploro/outputs/workingPaper/Stock-Demand-and-Price-Impact-of/991001524896506056
