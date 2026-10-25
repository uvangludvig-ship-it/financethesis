# What makes a prize-winning SSE finance thesis (2011-2024, 25 primary texts)

## 1. The recurring structure

**Question type.** Nearly every winner asks one of two things: does a result from a recent top-journal paper survive where institutions differ, or what happened when a specific rule changed? Twelve of 25 are built around a dated policy or market event (quotas, short-sale bans, French FTT, Norwegian parking fees, Swedish unbundling, Covid press conferences, LETF rebalancing, FOMC cycles). The question fits one sentence and is interesting whatever the answer: three winners are outright nulls (2011 PH, 2023 PH, 2024 PH) and nine are mixed.

**Anchor.** From 2016 onward every winner names one anchor paper and reproduces its main regression before extending it: Adrian-Etula-Muir (2016 PH), Petkova-Zhang (2019 SV), Tuzun (2020 PH), English-Van den Heuvel-Zakrajsek (2020 SV), Busse-Green (2021 PH), Kyle-Obizhaeva (2021 SV, 2022 PH), Baek-Kang-Park (2022 SV), Cieslak-Morse-Vissing-Jorgensen (2023 PH), Gabaix et al. (2023 SV), Ahern-Dittmar (2024 PH). The anchor is recent, has one replicable table, and usually sits in the tutor's field (three Obizhaeva-tutored invariance theses). Pre-2016 winners anchored on a literature rather than a paper.

**Data.** Thirteen of 25 use Swedish or Norwegian data, chosen because an institutional feature removes a confound, not for convenience: KommunInvest bonds share credit risk and tax status with treasuries (2017 PH); XACT is the only LETF issuer, so rebalancing flows are known exactly (2020 PH); Sweden unbundled research costs two years before MiFID II (2017 SV). Winners build data themselves: SCB broker-dealer balance sheets, fund annual reports, 375 million Nasdaq ticks, hand-coded French board genders.

**Identification.** Modest and standard: panel FE, event study, diff-in-diff, pre-period exposure as instrument (2024 PH), one RD (2012 SV), one experiment (2018 SV). Nobody oversells it. Instead they test a mechanism: hedging versus price pressure (2015 PH), direct rebalancing versus anticipatory trading (2020 PH), board-skill channel (2024 PH), Board-of-Governors timing (2023 PH).

**Conclusions.** Calibrated to the point of self-undermining: "Our results do not prove the validity of the model, but rather bring into question the validity of the standard benchmarks" (2016 PH); "There is no claim to causality" (2017 SV); "daily stock data may not be suitable" (2020 SV). Recent winners run 17-28 pages of main text (2019-2024) with 2-9 main tables and self-contained captions.

## 2. What the grading criteria reward in practice

The slides list Useful, Correct, Relevant, Contribution, Independence, "do not chase significance", and "what and why". In the winners this cashes out as: (i) a replicated recent top-journal table as proof of correctness; (ii) an extension changing at least two of {data, period, setting, method}, justified by institutions; (iii) a mechanism test, not just an effect; (iv) data the students assembled; (v) a paper-shaped document: intro that summarises results, under a page of related literature, no textbook econometrics. Nulls win when the question was interesting ex ante. No winner reports a power or MDE calculation although the slides ask for one.

## 3. Winners versus non-winners

The 2010 non-winners skimmed (1000, 1002, 1003, 1004, 1005, 1009) show the opposite profile: 36-77 pages, two-part theses with separate questions (1002), textbook sections on OLS assumptions or legal definitions of insiders, classic rather than recent anchors (Amihud 2002, Fama-French 1992) transplanted to Sweden with no institutional reason, and over-reach in the conclusion (hedging data "can thus be used in arbitrage pricing", 1009). Several claim causality from correlations. Winners do one thing, say why the setting is special, and say what they cannot conclude.

## 4. Five rules for a 2026 thesis on the Fondtorgsnämnden procurement

1. **Anchor on one paper with a replicable flow-pressure table** and reproduce it on Swedish data first: Coval-Stafford (2007 JFE) or Lou (2012 RFS), or the index-reconstitution literature if the design is forced reallocation of known amounts on known dates.
2. **Turn the institution into the identification.** Map which funds were removed, when capital moved, and where it went (new fund or AP7 default); build a stock-level exposure variable equal to expected forced sales or purchases scaled by average daily volume, as 2020 PH did with LETF flows and 2015 PH with fund-flow betas. The regulator, not the market, decided; say so and test it (pre-trends, placebo dates).
3. **State power before results.** Compute flows relative to ADV and the minimum detectable price effect given the number of transfer dates and stocks. No prior winner did this and the course asks for it.
4. **Test the mechanism:** temporary pressure with reversal versus permanent revaluation; anticipatory trading between announcement and transfer (2020 PH); heterogeneity by liquidity and ownership concentration; volume and spreads alongside returns.
5. **Write it as a paper:** 20-28 pages, an intro that gives the numbers, 5-8 main tables with stand-alone captions, a conclusion that states the limits. A clean null on price pressure, with evidence on who absorbed the flows, would still win.

## 5. Closest winners

**2015 PH** (fund-flow risk): took the Coval-Stafford/Lou price-pressure literature, built a new exposure measure, ran Fama-MacBeth, then tested two competing mechanisms and found asymmetric reversals. **2020 PH** (LETF rebalancing): used a Swedish institutional monopoly to measure flows exactly, regressed scaled end-of-day returns and volatility on scaled flows in the Tuzun specification, separated direct from anticipatory trading, and quantified crisis-time impact. **2024 PH** (French quota): a regulator-imposed shock evaluated with a pre-period exposure instrument, a foreign placebo, and a null reported without apology. Also worth reading: 2017 SV (Swedish rule change, hand-collected fund data) and 2021 PH (intraday reaction to a public authority).
