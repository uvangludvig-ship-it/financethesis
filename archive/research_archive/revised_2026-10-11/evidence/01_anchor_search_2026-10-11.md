# Anchor search for an FTN-centred thesis (agent report, 11 Oct 2026)

Brief: find top-journal anchors not screened in the 5 October contest that make an FTN-centred thesis with a replicable table and a powered extension. Citations checked unless flagged.

## Verified about the Swedish index round
Award 27 Aug 2025; category ~65 bn SEK (31 Jul 2025), ~450k savers. Winners: Aktiespararna Topp Sverige (~30 stocks, OMXS30-type), Handelsbanken Sverige Index Criteria (SIX Sweden SRI GI), HB Sverige 100 Index Criteria (Solactive ISS ESG Screened Sweden 100), HB Sverige LM Index (Solactive ESG Screened Select Sweden), Swedbank Robur Access Sverige. Removed: Avanza Zero (OMXS30-type; savers' letters map it to HB Sverige Index Criteria), Aktiespararna Direktavkastning, Evli Sverige Aktieindex, Öhman Marknad Sverige Bred, LF Sverige Index, Skandia Sverige Exponering, Storebrand Sverige A/Plus (mapped to Topp Sverige). Capital moved 30-stock to broad ESG-screened in both directions. Sources: Handelsbanken release (mb.cision.com/Main/23067/4222848/3629551.pdf), EFN (efn.se/handelsbanken-fonder-dominerar-i-indexfonderna), saver thread (rikatillsammans.se/forum/t/avanza-zero-forsvinner-fran-fondtorget/113040). NOT VERIFIED: which winners counted as "new" for the allocation rule.

## Candidates

1. **Pavlova and Sikorskaya (2023), "Benchmarking Intensity", RFS 36(3), 859-903.** Benchmark-driven inelastic demand (BMI = sum of benchmark weight x AUM tracking it / market cap) moves ownership and prices. Replicate on Swedish data 2018-2025 (~330 stocks; OMXS30 weights public, other indices approximated). Extension: FTN as a government-induced change in BMI (index round 38 bn, small cap 8 bn). Power: 5-day CAR t about 2 to 3.5 with N 330 and elasticity -1; weaker if trading is spread over a month. Risks: non-OMX index weights approximated; one large event. Klug fit: highest.
2. **Lou (2012), "A Flow-Based Explanation for Return Predictability", RFS 25(12), 3457-3489; Wardlaw (2020), JF 75(6), 3221-3243.** Flow-induced trading predicts contemporaneous returns and later reversal. Replicate Lou's tables on Swedish stocks from FI quarterly holdings x Morningstar flows 2018-2025 (~27k stock-months). Extension: FTN flows as an instrument for FIT across executed rounds; 2019 purge as a pre-FTN sample. Risk: seen as Da et al. redux; quarterly holdings; foreign-domiciled funds missing. Klug fit high.
3. **Reuter and Zitzewitz (2021), RoF 25(5), 1395-1432**, with the panel table from Zhu (2018, JFE 130(1)) or Pastor, Stambaugh and Taylor (2015, JFE 116(1), 23-45). Exogenous inflows and performance. Replicate PST/Zhu on the Morningstar Swedish-sold panel. Extension: new winners vs incumbent winners vs losers. Power: MDE about 1.5 to 2 per cent per year alpha, underpowered; holdings outcomes (cash, number of holdings, turnover; Pollet and Wilson 2008 JF) better powered. Klug fit moderate.
4. **McLemore (2019), JFQA 54(4), 1683-1711.** Fund mergers as inflow shocks; FTN mapping is a forced merger. Replication needs Swedish merger events (NOT VERIFIED available).
5. **Charoenwong, Morck and Wiwattanakantang (2021), RoF 25(3).** BoJ ETF purchases into funds tracking different indices (Nikkei 225 vs TOPIX): the closest institutional twin of the index round. Replicable on Japanese data via LSEG only.
6. **Bessembinder, Carrion, Tuttle and Venkataraman (2016), JFE 121(1), 142-166.** Pre-announced predictable trades and anticipatory trading. FTN transfers are announced months ahead. A microstructure module inside 1 or 2, not an anchor.
7. Goyal and Wahal (2008), JF 63(4): sponsors hire on past returns. Too old, not replicable independent of FTN. Jiang, Vayanos and Zheng (2025, RFS 38(12)): passive flows inflate large caps, a testable prediction inside 1.

## No viable anchor found
Pension procurement/auctions (Hastings, Hortacsu and Syverson 2017 ECMA; Luco 2019 AEJ Micro; Chile auction papers) need Mexican/Chilean admin data. Defaults (Chetty et al. 2014 QJE) non-replicable. Gabaix-Koijen inelastic markets and van der Beck flow-driven ESG returns are working papers.

## Ranked table

| Rank | Anchor | Replicable table on Swedish data without FTN | FTN extension | Power (assumed N) | Biggest risk | Klug fit |
|---|---|---|---|---|---|---|
| 1 | Pavlova-Sikorskaya 2023 RFS | BMI ownership/return tables, ~330 stocks | Index-switch 38 bn + small cap 8 bn, day-level CARs | t about 2 to 3.5 | Index weights; one big event | Very high |
| 2 | Lou 2012 RFS + Wardlaw 2020 JF | FIT tables from FI holdings, ~27k stock-months | FTN flows as FIT instrument, all rounds, 2019 placebo | Same plus active rounds | Da et al. redux; quarterly holdings | High |
| 3 | Reuter-Zitzewitz 2021 RoF + Zhu/PST | PST/Zhu panel yes | New vs incumbent winners vs losers | MDE 1.5 to 2% p.a. | Underpowered for returns | Moderate |
| 4 | McLemore 2019 JFQA | Uncertain | As 3 | As 3 | Merger data | Moderate |
| 5 | Charoenwong et al. 2021 RoF | Japan only | Same regression on FTN | As 1 | Two markets | High |
| 6 | Bessembinder et al. 2016 JFE | No | Anticipatory trading | Intraday | No replication leg | High |

Agent's recommendation: 1 with 2's holdings-based measure for the active rounds and 6 as a microstructure robustness; 3 as fallback.

Editor's note (main session): PLAN_REVISED takes Lou/Wardlaw as the anchor and Pavlova-Sikorskaya for the index round, because the FIT replication needs only FI holdings and Morningstar flows (both in hand), whereas BMI needs proprietary index weights for SIX and Solactive indices.
