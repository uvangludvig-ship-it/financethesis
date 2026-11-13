# Verified literature list: price pressure from pre-announced forced flows (FTN / OMXSB thesis)

Compiled 2026-10-12. Verification channels that worked: ideas.repec.org article pages (give publisher DOI handles), api.crossref.org per-DOI lookups (rate-limited, used sparingly), NBER working-paper pages and PDFs, BIS, IMF, arXiv, St Gallen WP server, Pensionsmyndigheten, the SHoF SSRN RSS feed. Blocked or exhausted: WebSearch (budget), Firecrawl (credits), Wiley, OUP, ScienceDirect, AEA, SSRN pages, OpenAlex, Semantic Scholar, Google Scholar, DiVA, fondtorgsnamnden.se, scholar.archive.org (rate limit).

Flags:
- [V] bibliographic record verified (journal, volume, issue, pages, DOI) from RePEc and/or Crossref.
- [V-abs] record verified and abstract read; magnitudes in the summary come from the abstract or a full-text working-paper version (table numbers refer to the version read, stated in each entry).
- [M] from memory: volume/pages/DOI NOT VERIFIED, or magnitudes recalled from memory. Treat every number marked [M] as "to be checked against the PDF before it goes in the thesis".
- Where a DOI is given for a [V] entry it was read off a publisher record. No DOI is invented; where unknown it is left out of references.bib.

Placement key: motivation / anchor / method / theory / incidence / Swedish context / calibration.

---

## A. Anchor and index-effect literature

### Greenwood and Sammon (2025) [V-abs, full text of NBER WP 30748 read]
Greenwood, Robin, and Marco Sammon. 2025. "The Disappearing Index Effect." Journal of Finance 80(2): 657-698. DOI 10.1111/jofi.13410. (NBER WP 30748, Dec 2022, DOI 10.3386/w30748; SSRN 4649650.)

Question: why has the S&P 500 index effect vanished while index-linked assets exploded? Data: S&P 500 additions and deletions 1980-2020 (Siblis; 755 additions, 750 deletions; after filters Table 2 uses 684 additions and 263 deletions), CRSP returns, S&P MidCap changes from 1995 for the migration analysis, pre-1990 announcement dates from Barberis, Shleifer and Wurgler (2005). Identification: event study of the announcement window, effective-day window and the total window (day before announcement to day after implementation), by decade.

Headline magnitudes (Table 2 of the NBER WP, percent; the JF abstract gives slightly revised figures, see below):

| Window | 1980s | 1990s | 2000s | 2010s |
|---|---|---|---|---|
| Additions, total | 3.42 | 7.59 | 5.21 | 0.80 |
| Additions, announcement | 3.36 | 5.15 | 4.13 | 1.05 |
| Additions, effective | 3.44 | 3.68 | 1.32 | 0.21 |
| Deletions, total | -4.64 | -16.6 | -12.3 | -0.60 |
| Deletions, announcement | -4.71 | -14.4 | -10.1 | -0.2 |
| Deletions, effective | -4.65 | -8.64 | -4.34 | 0.2 |

The 2010s totals (0.80 and -0.60) are not distinguishable from zero. The published JF abstract states: additions averaged 7.4% in the 1990s and less than 1% over the past decade; deletions averaged only 0.1% in 2010-2020 (so the JF version revised the WP numbers slightly; the table number in the JF version could not be checked because Wiley is blocked).

Explanations tested (NBER WP numbering): (1) composition of added firms, Table 3, explains only part; (2) liquidity, Figures 4-5, spreads fell about 10x but timing does not match and institutional implementation shortfall was flat, judged insufficient alone; (3) index migrations from the S&P MidCap, Figures 6-7, supported: migrations rose from about 40% of additions in the mid-1990s to over 80%, and migration returns fell as MidCap passive ownership grew; (4) predictability and pre-positioning, Figures 8-10, mixed: more of the run-up now occurs before the announcement and size-based selection is more consistent, but the specific names remain hard to predict; (5) event-day liquidity provision, Figure 11 and Table 4, supported: effective-day volume share rose from about 15% to nearly 30% and institutional ownership changes around events shrank while tracker buying grew, i.e. other institutions now absorb the demand. Conclusion names two primary drivers: migrations and an overall increase in the market's ability to supply liquidity; increased predictability "cannot be ruled out". No numbers for other index families in the text; it cites Chinco and Sammon for the Russell decline.

Placement: anchor. The OMXSB replication mirrors Table 2 (announcement, effective, total windows by sub-period) and the explanation list.

### Shleifer (1986) [V]
Shleifer, Andrei. 1986. "Do Demand Curves for Stocks Slope Down?" Journal of Finance 41(3): 579-590. DOI 10.1111/j.1540-6261.1986.tb04518.x.

The original index-inclusion test of downward-sloping demand: S&P 500 additions 1966-1983, with the post-1976 period (when S&P began announcing changes) as the clean sample. Headline [M magnitudes]: about +2.8 to 3% abnormal return around the announcement, persisting for at least ten to twenty trading days, interpreted as a permanent shift from inelastic demand rather than information. Placement: motivation (demand curves slope down; large uninformed demand moves prices).

### Harris and Gurel (1986) [V]
Harris, Lawrence, and Eitan Gurel. 1986. "Price and Volume Effects Associated with Changes in the S&P 500 List: New Evidence for the Existence of Price Pressures." Journal of Finance 41(4): 815-829. DOI 10.1111/j.1540-6261.1986.tb04550.x.

Same event, opposite reading: S&P 500 changes 1973-1983 [M dates]. Headline [M magnitudes]: about +3% on the inclusion day with a near-complete reversal within roughly two weeks, plus a volume spike, consistent with temporary price pressure from index-fund buying rather than a permanent demand shift. Placement: motivation and method (the pressure-plus-reversal template the FTN execution-day test follows).

### Kaul, Mehrotra and Morck (2000) [V-abs]
Kaul, Aditya, Vikas Mehrotra, and Randall Morck. 2000. "Demand Curves for Stocks Do Slope Down: New Evidence from an Index Weights Adjustment." Journal of Finance 55(2): 893-912. DOI 10.1111/0022-1082.00230.

TSE 300 public-float redefinition, November 1996, pre-announced, raised the float and index weights of 31 stocks with no information content and no change in shareholder rights. Excess return of 2.3% in the event week, statistically significant, no reversal as volume normalised. Cleanest pre-announced pure demand shock in the literature. Placement: anchor-adjacent; closest analogue to FTN's uninformed pre-announced flow.

### Wurgler and Zhuravskaya (2002) [V-abs]
Wurgler, Jeffrey, and Ekaterina Zhuravskaya. 2002. "Does Arbitrage Flatten Demand Curves for Stocks?" Journal of Business 75(4): 583-608. DOI 10.1086/341636.

Model of risk-averse arbitrageurs who trade between imperfect substitutes; the demand curve is flatter the better the substitutes. S&P 500 additions (1976-1989 [M dates]): the price jump is larger for stocks without close substitutes (high idiosyncratic risk). Implied elasticities on the order of -5 to -11 [M, quoted via Da et al. 2018]. Placement: theory and cross-sectional prediction (impact should scale with idiosyncratic risk of the FTN-affected stocks).

### Greenwood (2005) [V]
Greenwood, Robin. 2005. "Short- and Long-term Demand Curves for Stocks: Theory and Evidence on the Dynamics of Arbitrage." Journal of Financial Economics 75(3): 607-649. DOI 10.1016/j.jfineco.2004.03.007.

Nikkei 225 redefinition of April 2000 (announced in advance): 30 stocks added, 30 deleted, and the 195 remaining stocks mechanically sold by index trackers because the index was re-weighted. Model: risk-averse arbitrageurs absorb an uninformed pre-announced demand shock; price impact at the event is proportional to the shock's covariance with arbitrageurs' portfolio, and the price reverts as the shock is absorbed. Headline [M magnitudes]: added stocks up roughly 19%, deleted stocks down roughly 32% between announcement and effective date, remaining index stocks fell in proportion to the trackers' selling, and the effects reversed substantially over the following weeks. Placement: theory (the model the thesis' theory section should follow) and anchor-adjacent (pre-announced flow, both sides of the trade, reversal).

### Petajisto (2011) [V-abs]
Petajisto, Antti. 2011. "The Index Premium and Its Hidden Cost for Index Funds." Journal of Empirical Finance 18(2): 271-288. DOI 10.1016/j.jempfin.2010.10.002.

Index premium 1990-2005: announcement-to-effective price impact of +8.8% for S&P 500 additions and +4.7% for Russell 2000 additions; -15.1% and -4.6% for deletions. The premium rose through 2000 and declined after. Implied demand elasticity rises with size and falls with idiosyncratic risk. Index turnover cost of 21-28 bp per year for the S&P 500 and 38-77 bp for the Russell 2000. Placement: motivation and calibration (who pays for pre-announced index turnover; the cost borne by passive holders is the index analogue of NAV dilution).

### Chang, Hong and Liskovich (2015) [V-abs]
Chang, Yen-Cheng, Harrison Hong, and Inessa Liskovich. 2015. "Regression Discontinuity and the Price Effects of Stock Market Indexing." Review of Financial Studies 28(1): 212-246. DOI 10.1093/rfs/hhu041 (NBER WP 19290).

Russell 1000/2000 cutoff as a regression discontinuity: additions to the Russell 2000 are followed by price increases, deletions by declines; the paper also examines which fund types supply the liquidity. Magnitudes [M]: about +5% for additions to the 2000 in the month after reconstitution, with partial reversal. Placement: method (identification when the forcing variable is a rank; useful if OMXSB membership rules are threshold-based).

### Pavlova and Sikorskaya (2023) [V-abs]
Pavlova, Anna, and Taisiya Sikorskaya. 2023. "Benchmarking Intensity." Review of Financial Studies 36(3): 859-903. DOI 10.1093/rfs/hhac055. (CEPR DP 16909.) Note: the RePEc record also lists Ralph Koijen, which is the handling editor, not an author.

Benchmarking intensity (BMI) = cumulative weight of a stock across all benchmarks weighted by assets tracking each. Using the Russell cutoff as instrument, changes in BMI track benchmarked-investor ownership; implied demand elasticities are low; both active and passive managers buy additions and sell deletions; higher BMI predicts lower future returns. Placement: motivation (benchmarked active managers amplify index flows; relevant because Swedish active funds are benchmarked to OMX indices).

### Chinco and Sammon (2024) [V-abs]
Chinco, Alex, and Marco Sammon. 2024. "The Passive Ownership Share Is Double What You Think It Is." Journal of Financial Economics 157: 103860. DOI 10.1016/j.jfineco.2024.103860. (SSRN 4188052.)

Infers passive ownership from rebalancing volume on reconstitution days: index funds held 16% of the US market in 2021, but the passive share including internally indexed institutions and closet indexers is 33.5%. Placement: method (the reconstitution-day volume approach is the way to measure OMXSB tracker demand when tracker AUM is only partially observed).

### Sammon (2025) [V-abs]
Sammon, Marco. 2025. "Passive Ownership and Price Informativeness." Management Science 71(6): 4582-4598. DOI 10.1287/mnsc.2023.00836. (Published online 9/2024; SSRN 3243910.)

Passive ownership reduces the degree to which prices anticipate earnings announcements; the rise in passive ownership over 30 years lowered pre-announcement information in prices by about one fourth of its mean and one sixth of its standard deviation. Placement: motivation (passive growth changes the price-formation environment; the thesis uses tracker growth SEK 15bn to 120bn as the time-series variation).

### Ben-David, Franzoni and Moussawi (2018) [V-abs]
Ben-David, Itzhak, Francesco Franzoni, and Rabih Moussawi. 2018. "Do ETFs Increase Volatility?" Journal of Finance 73(6): 2471-2535. DOI 10.1111/jofi.12727. (NBER WP 20071.)

Exogenous changes in index membership identify the effect of ETF ownership: higher ETF ownership raises stock volatility and negative autocorrelation (liquidity shocks propagated by arbitrage); the extra volatility carries a premium of up to 56 bp per month. Placement: motivation (arbitrage channel that transmits fund-level flows to stock prices).

### Bonus, verified, directly relevant
- Sammon, Marco, and John J. Shim. 2026. "Index Rebalancing and Stock Market Composition: Do Indexes Time the Market?" Journal of Financial Economics 177: 104229. DOI 10.1016/j.jfineco.2025.104229. [V-abs] Value-weighted indexes must rebalance for issuance, buybacks and IPOs; the long-short rebalancing portfolio earns 4.61% a year and the drag on indexes is 46-69 bp a year. Placement: motivation (index trading is not confined to add/delete events).
- Sammon, Marco (with co-author, author list [M]: John J. Shim). 2026. "Who Clears the Market When Passive Investors Trade?" Review of Financial Studies, advance article, DOI 10.1093/rfs/hhag032 (from the author's website; SSRN 4777585). Title and DOI seen on marcosammon.com; content not read. Placement: motivation (liquidity providers on reconstitution days, the exact question the FTN execution-day analysis asks).

---

## B. Price pressure from fund flows

### Coval and Stafford (2007) [V-abs]
Coval, Joshua, and Erik Stafford. 2007. "Asset Fire Sales (and Purchases) in Equity Markets." Journal of Financial Economics 86(2): 479-512. DOI not verified (RePEc gives only the PII S0304-405X(07)00115-8 and Crossref was rate-limited; look it up before use). (NBER WP 11357.)

Mutual fund flow-driven trading 1980-2003: funds with extreme outflows sell existing holdings, inflow funds buy; commonly held stocks experience price pressure and subsequent reversal; liquidity providers earn significant returns; because flows are predictable, front-running is possible. Magnitudes [M]: stocks under extreme selling pressure lose on the order of 7-8% in the event quarter and recover over the following 12-18 months. Placement: motivation and method (the "pressure" measure, reversal horizon, front-running of predictable flows).

### Lou (2012) [V-abs]
Lou, Dong. 2012. "A Flow-Based Explanation for Return Predictability." Review of Financial Studies 25(12): 3457-3489. DOI 10.1093/rfs/hhs103.

Flow-induced trading (FIT) aggregated across funds is a stock-level demand shock with a significant but temporary price impact; expected FIT forecasts next-year stock and fund returns with reversal afterwards; fully accounts for performance persistence and the smart-money effect, partly for momentum. Placement: method (the FIT construction is the template for the stock-level FTN flow measure: fund redemption x portfolio weight / stock market cap).

### Wardlaw (2020) [V-abs]
Wardlaw, Malcolm. 2020. "Measuring Mutual Fund Flow Pressure as Shock to Stock Returns." Journal of Finance 75(6): 3221-3243. DOI 10.1111/jofi.12962.

Shows the standard flow-pressure measure is mechanically tied to the stock's own realised return in the outflow quarter; once removed, outflows produce only a "fairly negligible" quarterly decline with no reversal, and many downstream findings disappear. Placement: method (build the FTN pressure variable from pre-event holdings and pre-event prices, exactly to avoid this critique; FTN flows are fixed by the award, which is the thesis' advantage).

### Da, Larrain, Sialm and Tessada (2018) [V-abs, full text of NBER WP 22161 read]
Da, Zhi, Borja Larrain, Clemens Sialm, and Jose Tessada. 2018. "Destabilizing Financial Advice: Evidence from Pension Fund Reallocations." Review of Financial Studies 31(10): 3720-3755. DOI 10.1093/rfs/hhy011. (NBER WP 22161, April 2016, under the title "Coordinated Noise Trading: Evidence from Pension Fund Reallocations".)

Chilean DC pension system; an advisory firm (Felices y Forrados) issued 22 switch recommendations between funds A (equity) and E (bonds), July 2011 to March 2015; each switch moved USD 1-5bn, 10-20% of fund assets, forcing managers to trade about 10% of their equity book within days. A USD 2.5bn flow implies about USD 395m of Chilean equity trading against daily turnover of about USD 205m. Price pressure (WP numbering): Table 5 cumulative abnormal equity return of 1.06% (s.e. 0.29) on day 1, 1.22% by day 3, reverting to -0.42% (n.s.) by day 15; Figure 5 shows full reversal within 15 days; Table 6 daily regressions 1.05% (no controls) and 0.77% (controls); Table 7 subsamples (1.01% for recommendations 8-15, 1.06% for buy-equity); Table 8 cross-section: FIP coefficient on cumulative returns 1.87 (day 2) and 3.40 (day 3), turnover responds on days 4-5; Table 9 volatility: 1% higher FIP raises monthly volatility 0.6-1.8%; Table 10 cash holdings. Implied day-1 demand elasticity -0.45 (versus -1 in Shleifer 1986 and -5 to -11 in Wurgler and Zhuravskaya 2002).

NOTE on "Table 11": the NBER WP has only ten tables; the RFS version was not accessible (OUP blocked). If the thesis cites "Table 11" it must be checked against the RFS PDF; the WP's stock-level price-pressure tables are 5 to 8 and the elasticity statement is in the text of Section 4.

Placement: closest analogue to FTN (coordinated, uninformed, very large relative to daily volume, in a small market) and method (event-day CAR, reversal, FIP cross-section, elasticity computation).

### Hartzmark and Solomon (2025) [V-abs]
Hartzmark, Samuel M., and David H. Solomon. 2025. "Market-Wide Predictable Price Pressure." American Economic Review 115(9): 3171-3213. DOI 10.1257/aer.20231725. Published (September 2025 issue), replication data DOI 10.3886/E222561V1.

Predictable uninformed cash flows forecast aggregate market returns: dividend payment days (known weeks in advance) carry higher value-weighted market returns; returns on top-quintile payment days are about four times those on bottom-quintile days; implied market-level price multiplier of 1.9. Holds internationally, stronger with high reinvestment and low liquidity. Placement: motivation and calibration (a pre-announced flow moves prices even at the market level; the multiplier is a benchmark for the FTN stock-level estimate).

### Parker, Schoar and Sun (2023) [V-abs]
Parker, Jonathan A., Antoinette Schoar, and Yang Sun. 2023. "Retail Financial Innovation and Stock Market Dynamics: The Case of Target Date Funds." Journal of Finance 78(5): 2673-2723. DOI 10.1111/jofi.13258.

TDF rebalancing generates contrarian flows into the equity funds TDFs hold; this stabilises those funds' flows and lowers returns on stocks TDFs disproportionately hold after high market returns. Placement: motivation (mechanical pension-driven flows reach stock prices through fund holdings).

### Mitchell, Pulvino and Stafford (2004) [V]
Mitchell, Mark, Todd Pulvino, and Erik Stafford. 2004. "Price Pressure around Mergers." Journal of Finance 59(1): 31-63. DOI 10.1111/j.1540-6261.2004.00626.x.

Merger-arbitrage short selling of acquirers in stock-financed deals creates downward price pressure. Magnitudes [M]: nearly half of the negative acquirer announcement return in fixed-exchange-ratio stock deals is price pressure that reverses, implying a price impact that is temporary and attributable to uninformed arbitrage demand. Placement: motivation (uninformed, predictable demand from a known mechanism moves prices by a measurable amount and reverses).

### Sabbatucci, Tamoni and Xiao (2023, WP) [V via SHoF SSRN RSS feed]
Sabbatucci, Riccardo, Andrea Tamoni, and Song Xiao. 2023. "Shifting From Active to Passive: How Retirement Plans Impact Equity Prices." SSRN Working Paper 4322784, Swedish House of Finance Research Paper series, posted 12 January 2023. URL https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4322784.

Question: how does the shift of 401(k) plan assets from active to passive funds affect equity prices? Data: granular 401(k) fund-offering (menu) data; DC plans hold about USD 12 trillion (end-2024 figure in the current abstract, so the paper has been revised after 2023). Findings as given in the feed abstract (paraphrased by the fetch tool, SSRN page itself blocked): the move to passive is associated with aggregate price changes of roughly 35%; stocks overweighted by active funds decline through two channels, direct outflows from those funds and lower stock-level 401(k) ownership, which the authors identify as a key driver of investor demand. The exact wording of the "35%" claim and its table should be read off the PDF before citing. Placement: motivation and method (the grader's paper; menu-driven forced reallocation across funds is the US analogue of FTN's procurement; its holdings-weighted flow measure is the template for the stock-level FTN measure).

### Schmickler and Tremacoldi-Rossi (WP) [M]
Schmickler, Simon N. M., and Pedro Tremacoldi-Rossi. "Spillover Effects of Payouts on Asset Prices and Real Investment." Working paper (SSRN), year and status NOT VERIFIED. Not found in the RePEc listings of JFE (2023-2026), RFS (2023-2026) or Review of Finance (2018-2026), so treat as unpublished unless the authors' pages say otherwise.

Dividend and buyback proceeds are reinvested by funds into the rest of their portfolios, producing predictable buying pressure on non-paying stocks, with price and real-investment spillovers. Placement: motivation (pre-announced reinvestment flows as price pressure); cite only after checking the current version.

---

## C. Demand elasticity and theory

### Koijen and Yogo (2019) [V-abs]
Koijen, Ralph S. J., and Motohiro Yogo. 2019. "A Demand System Approach to Asset Pricing." Journal of Political Economy 127(4): 1475-1515. DOI 10.1086/701683.

Characteristics-based demand system for institutions and households, estimated by IV on 13F holdings; low micro demand elasticities; used to decompose price movements into institutional demand components. Placement: theory and calibration (inelastic demand as the quantitative frame; the thesis' implied elasticity is comparable to the KY estimates).

### Gabaix and Koijen (2021, WP) [V as NBER WP; publication status not verified]
Gabaix, Xavier, and Ralph S. J. Koijen. 2021 (revised). "In Search of the Origins of Financial Fluctuations: The Inelastic Markets Hypothesis." NBER Working Paper 28967. DOI 10.3386/w28967. The NBER page (read 2026-10-12) lists no published version; cite as a working paper unless a 2026 journal version is found.

Households invest through mandate-constrained institutions, so aggregate stock demand is inelastic; granular IV estimates a multiplier of about 5 (USD 1 of inflow raises aggregate market value by about USD 5). Placement: theory and calibration (the market-level multiplier against which Hartzmark-Solomon's 1.9 and the thesis' stock-level number can be placed).

### Haddad, Huebner and Loualiche (2025) [V-abs]
Haddad, Valentin, Paul Huebner, and Erik Loualiche. 2025. "How Competitive Is the Stock Market? Theory, Evidence from Portfolios, and Implications for the Rise of Passive Investing." American Economic Review 115(3): 975-1018. DOI 10.1257/aer.20230505.

Demand system with strategic responses: when surrounding investors become less aggressive an investor trades more aggressively, but the offset is only about two thirds; the rise of passive investing over 20 years made demand for individual stocks 11% more inelastic. Placement: theory (why growing tracker share need not make the index effect larger: other investors partially fill the gap, consistent with Greenwood-Sammon explanation 5).

### Duffie (2010) [V-abs]
Duffie, Darrell. 2010. "Presidential Address: Asset Price Dynamics with Slow-Moving Capital." Journal of Finance 65(4): 1237-1267. DOI 10.1111/j.1540-6261.2010.01569.x.

After a supply or demand shock, prices react sharply and then reverse over an extended period; the size of the initial impact and the speed of recovery depend on frictions (search, time to raise capital, inattention); gives a simple model with inattentive investors that produces a closed-form price path after a supply shock. Placement: theory (the shape of the expected FTN price path: overshoot on the execution day, decay as slow capital arrives).

### Grossman and Miller (1988) [V]
Grossman, Sanford J., and Merton H. Miller. 1988. "Liquidity and Market Structure." Journal of Finance 43(3): 617-633. DOI 10.1111/j.1540-6261.1988.tb04594.x.

Market makers with finite risk-bearing capacity absorb an order imbalance; the temporary price concession is the compensation for holding the position until outside buyers arrive; immediacy is priced. Placement: theory (the baseline risk-averse liquidity-provider model; the thesis' theory section is a Grossman-Miller economy with a pre-announced imbalance).

### Brunnermeier and Pedersen (2005) [V-abs]
Brunnermeier, Markus K., and Lasse Heje Pedersen. 2005. "Predatory Trading." Journal of Finance 60(4): 1825-1863. DOI 10.1111/j.1540-6261.2005.00781.x.

When a trader must liquidate, others sell first and buy back later, pushing the price beyond its fundamental overshoot and lowering the distressed trader's proceeds; liquidity is lowest when most needed; predation can spread across traders and markets. Placement: theory (the FTN award and letter dates make the forced seller's position public weeks in advance: the predatory versus sunshine-trading distinction is the thesis' anticipation test).

### Admati and Pfleiderer (1991) [V-abs]
Admati, Anat R., and Paul Pfleiderer. 1991. "Sunshine Trading and Financial Market Equilibrium." Review of Financial Studies 4(3): 443-481. DOI 10.1093/rfs/4.3.443.

Pre-announcing an uninformed order identifies it as liquidity-motivated and coordinates liquidity supply; it generally lowers the announcer's trading cost but has ambiguous effects on others' welfare and on price informativeness. Placement: theory (the benign reading of pre-announcement; predicts smaller execution-day impact than an unannounced trade of the same size).

### Bessembinder, Carrion, Tuttle and Venkataraman (2016) [V-abs]
Bessembinder, Hendrik, Allen Carrion, Laura Tuttle, and Kumar Venkataraman. 2016. "Liquidity, Resiliency and Market Quality around Predictable Trades: Theory and Evidence." Journal of Financial Economics 121(1): 142-166. DOI 10.1016/j.jfineco.2016.02.011.

Theory with resiliency: a single strategic trader can improve market quality and raise the liquidator's proceeds when temporary impact reverts quickly; competition helps further. Evidence from the USO ETF's pre-announced futures rolls: spreads narrow, depth rises, resiliency improves, more accounts supply liquidity, no systematic predatory trading. Placement: theory and motivation (the empirical counterpart of sunshine trading; the benchmark against which FTN execution-day spreads and depth should be compared).

### Vayanos and Woolley (2013) [V-abs]
Vayanos, Dimitri, and Paul Woolley. 2013. "An Institutional Theory of Momentum and Reversal." Review of Financial Studies 26(5): 1087-1145. DOI 10.1093/rfs/hht014.

Flows between funds, driven by inferred manager efficiency, generate momentum (prices under-react to expected future flows when flows are persistent) and reversal (flows push prices from fundamentals); stronger for high-idiosyncratic-risk assets; calibrated to fund flows. Placement: theory (fund-level flows as the origin of stock-level momentum and reversal; predicts larger FTN effects in high-idiosyncratic-risk names).

### Kyle (1985) [V]
Kyle, Albert S. 1985. "Continuous Auctions and Insider Trading." Econometrica 53(6): 1315-1335. DOI 10.2307/1913210.

Market maker sets price linearly in order flow (lambda) to break even against an informed trader; uninformed order flow moves prices because it cannot be distinguished from informed flow. Placement: theory (lambda as the linear-impact benchmark; FTN flows are identified as uninformed by construction, which is why sunshine trading applies).

---

## D. Market impact and execution-cost calibration (square-root law)

### Almgren, Thum, Hauptmann and Li (2005) [M]
Almgren, Robert, Chee Thum, Emmanuel Hauptmann, and Hong Li. 2005. "Direct Estimation of Equity Market Impact." Risk 18(7): 58-62. NOT VERIFIED (practitioner journal, no DOI located).

Citigroup execution data: temporary impact is concave in the participation rate (fitted exponent about 0.6), permanent impact roughly linear; impact scales with daily volatility and with (order size / ADV). Placement: calibration (the industry square-root functional form: impact ≈ Y · sigma_daily · sqrt(Q/ADV), Y around 0.5 to 1).

### Bouchaud, Bonart, Donier and Gould (2018) [V]
Bouchaud, Jean-Philippe, Julius Bonart, Jonathan Donier, and Martin Gould. 2018. Trades, Quotes and Prices: Financial Markets Under the Microscope. Cambridge: Cambridge University Press. DOI 10.1017/9781316659335. ISBN 9781107156050. Part V "Price Impact", Chapter 12 "The Impact of Metaorders" (pp. 229-244) covers the square-root law (chapter content inferred from the table of contents and a reviewer's description; the chapter was not read).

Textbook statement of the square-root law for metaorders: peak impact ≈ Y · sigma · sqrt(Q/V) with Y of order 1, independent of execution speed over a wide range; impact decays after completion to a permanent level of about two thirds of the peak. Placement: calibration (the benchmark expected impact of an FTN redemption equal to a given multiple of ADV).

### Frazzini, Israel and Moskowitz (2018) [M]
Frazzini, Andrea, Ronen Israel, and Tobias J. Moskowitz. 2018. "Trading Costs." Working paper (AQR / SSRN), NOT VERIFIED; not found in the Review of Finance RePEc listing 2018-2026, so treat as unpublished.

Live trade data from a large asset manager (about USD 1.7 trillion traded, 1998-2016 [M]): realised price impact is well described by a square-root-like concave function of the fraction of daily volume, with impact around 10-20 bp for trades of 1% of ADV [M]; costs are an order of magnitude smaller than earlier TAQ-based estimates. Placement: calibration (realised-cost parameters for the square-root benchmark).

### Almgren and Chriss (2000/2001) [V]
Almgren, Robert, and Neil Chriss. 2001. "Optimal Execution of Portfolio Transactions." Journal of Risk 3(2): 5-39. DOI 10.21314/JOR.2001.041. (Crossref dates the issue Winter 2000/2001; most citations say 2000.)

Mean-variance optimal liquidation with linear temporary and permanent impact; efficient frontier of expected cost versus variance; the Pensionsmyndigheten's choice between one-day and staggered redemptions is exactly this trade-off. Placement: method and calibration (frames why staggered execution lowers temporary impact and why one-day execution is the worst case).

### Toth, Lemperiere, Deremble, de Lataillade, Kockelkoren and Bouchaud (2011) [V-abs via arXiv]
Toth, Bence, Yves Lemperiere, Cyril Deremble, Joachim de Lataillade, Julien Kockelkoren, and Jean-Philippe Bouchaud. 2011. "Anomalous Price Impact and the Critical Nature of Liquidity in Financial Markets." Physical Review X 1(2): 021006. DOI 10.1103/PhysRevX.1.021006. (arXiv 1105.1694.)

Latent order book theory: the supply/demand profile is V-shaped and vanishes near the current price, so small orders have disproportionate impact and metaorder impact is concave (square root); supported by CFM proprietary data. Placement: calibration and theory (why impact is concave rather than Kyle-linear).

### Zarinelli, Treccani, Farmer and Lillo (2015) [V-abs]
Zarinelli, Elia, Michele Treccani, J. Doyne Farmer, and Fabrizio Lillo. 2015. "Beyond the Square Root: Evidence for Logarithmic Dependence of Market Impact on Size and Participation Rate." Market Microstructure and Liquidity 1(2): 1550004. DOI 10.1142/S2382626615500045. (arXiv 1412.2152.)

US equity metaorders 2007-2009 (Ancerno-type data): the square root fits over about two orders of magnitude of size; a logarithmic form fits over nearly five; impact surface in duration and participation rate; impact decays to about two thirds of peak after execution, and prices sometimes start reverting before execution ends. Placement: calibration (very large FTN orders are at the extreme of the size range where impact is flatter than the square root; use both as bounds).

---

## E. Incidence: who pays for flows

### Edelen (1999) [V]
Edelen, Roger M. 1999. "Investor Flows and the Assessed Performance of Open-End Mutual Funds." Journal of Financial Economics 53(3): 439-466. DOI 10.1016/S0304-405X(99)00028-8.

Flow-driven (liquidity-motivated) trading by open-end funds has a negative marginal effect on performance; on the order of 1.5 to 2% of assets per year for the average fund [M magnitude], a cost borne by all shareholders, i.e. an externality from flows. Placement: incidence (the baseline statement that stayers pay for others' flows).

### Greene and Hodges (2002) [V]
Greene, Jason T., and Charles W. Hodges. 2002. "The Dilution Impact of Daily Fund Flows on Open-End Mutual Funds." Journal of Financial Economics 65(1): 131-158. DOI 10.1016/S0304-405X(02)00137-X.

Daily flows into international funds priced with stale NAVs dilute non-transacting shareholders; dilution on the order of 0.5% of assets per year for international funds [M magnitude]. Placement: incidence (the NAV-dilution mechanism, and the accounting of who bears it).

### Chen, Goldstein and Jiang (2010) [V-abs]
Chen, Qi, Itay Goldstein, and Wei Jiang. 2010. "Payoff Complementarities and Financial Fragility: Evidence from Mutual Fund Outflows." Journal of Financial Economics 97(2): 239-262. DOI 10.1016/j.jfineco.2010.03.016.

Strategic complementarities: in illiquid funds, where redemptions impose larger costs on stayers, outflows are more sensitive to bad performance; the pattern disappears when shareholders are mostly large (internalising) investors. Placement: incidence and theory (first-mover advantage; the reason swing pricing exists; the Dahlquist-Martinez-Soderlind regression follows this paper's design).

### Jin, Kacperczyk, Kahraman and Suntheim (2022) [V-abs, full text of IMF WP 19/227 read]
Jin, Dunhong, Marcin Kacperczyk, Bige Kahraman, and Felix Suntheim. 2022. "Swing Pricing and Fragility in Open-End Mutual Funds." Review of Financial Studies 35(1): 1-50. DOI 10.1093/rfs/hhab022. (IMF WP 2019/227; CEPR DP 13929.)

FCA data on 224 UK-managed open-end corporate bond funds in 22 families, Jan 2006 to Dec 2016, with investor-level transactions for 230 funds; 22% traditional pricing, 22% full swing, 57% partial swing, 21% dual pricing; 34 funds switched to swing. Tables (WP numbering, the RFS version may renumber): Table 2 and Figure 2 dilution adjustment factors (full swing and dual average about 33 bp; partial swing 57 bp on days triggered; 18-25 bp outside crises, roughly quadrupled in 2008; thresholds mostly 1% and 3%, caps around 2%); Table 3 outflows in stress: Alternative x Stress about +1.04 against Stress about -0.99, so swing pricing offsets stress outflows almost one for one; Tables 5-6 switcher triple-difference; Table 7 flow-performance asymmetry: NegAlpha 5.82, NegAlpha x Alternative -4.07 (both 1%); Table 10 dilution: outflows lower future performance for traditional funds, an effect that "almost completely dissipates" under swing pricing (about twice as large for illiquid funds); Tables 11-12 costs (higher tracking error, fewer new investors in calm periods). Stress-period capital loss about GBP 8.9m per month (6.3% of assets) for traditional funds versus GBP 0.2m for swing funds. Placement: incidence (swing pricing as the alternative to NAV dilution; magnitudes of the dilution that swing pricing removes).

### Capponi, Glasserman and Weber (2020) [V-abs]
Capponi, Agostino, Paul Glasserman, and Marko Weber. 2020. "Swing Pricing for Mutual Funds: Breaking the Feedback Loop Between Fire Sales and Fund Redemptions." Management Science 66(8): 3581-3602. DOI 10.1287/mnsc.2019.3353.

Model of the redemption-fire-sale feedback loop with a first-mover advantage; the redemption impact is nonlinear with a critical shock size beyond which the fund fails; a well-designed swing factor, increasing in outflows, removes the nonlinearity and the failure region; one fund's optimal swing factor depends on others' policies. Placement: incidence and theory (what a swing factor must look like for a 20-44% redemption; note the FTN redemption is state-executed, so the first-mover game is between the state and the stayers).

### Lewrick and Schanz (2017) [V-abs, full text read]
Lewrick, Ulf, and Jochen Schanz. 2017. "Is the Price Right? Swing Pricing and Investor Redemptions." BIS Working Paper 664, Bank for International Settlements, October 2017. No published journal version listed on the BIS page.

1,719 actively managed bond funds (1,000 US, 719 Luxembourg), monthly, Jan 2012 to May 2016, taper tantrum analysed separately. Table 2: a -10% prior-month return produces outflows of about 0.52% of TNA for US funds versus 0.25% for Luxembourg (swing-eligible) funds; the dampening is about 0.04% of TNA per point of negative return (0.08 and 0.16 over 3- and 6-month returns). Table 4: swing funds' market-adjusted returns 17-52 bp per year higher in the taper tantrum, but daily NAV volatility about 1.5 pp higher (2.4-3.1 pp in the tightest matches). Table 5: swing funds hold about 0.98 pp less cash (sample mean 3.3%). Swing factors: industry caps around 2% of NAV; stylised example 1% factor triggered at 2% net outflow. Placement: incidence (the European swing-pricing regime that Swedish UCITS may apply; magnitudes of the protection and its cost).

### Dahlquist, Martinez and Soderlind (2017) [V-abs, full text of St Gallen WP 1408 (rev. Sept 2016) read]
Dahlquist, Magnus, Jose Vicente Martinez, and Paul Soderlind. 2017. "Individual Investor Activity and Performance." Review of Financial Studies 30(3): 866-899. DOI 10.1093/rfs/hhw093. (St Gallen School of Finance WP 1408; CEPR DP 8744.)

Swedish Premium Pension System, daily data from the Swedish Pensions Agency: random sample of 100,000 of 6m+ participants, 70,755 in the system from Sept 2000 to May 2010 (62,640 non-coordinated, 8,115 coordinated), 1,229 funds. Headline: inactive investors (93.5%) earn 3.82% a year versus 12.57% for the top activity decile; FFCH alphas -0.70%, 2.09% (active) and 7.56% (highly active); about 45% of the highly-active outperformance is performance chasing. Fund-level flow impact, Table XII in the WP (the published table number may differ, "Table X" in the thesis note should be checked): Panel A equity funds 2000-2010, daily abnormal fund returns on ten return lags plus outflow and inflow indicators (Chen-Goldstein-Jiang design), fund fixed effects, Driscoll-Kraay errors. Outflows at 10x the fund's average (1.24% of fund-days) lower the day's abnormal return by about 6 bp; at 30x (0.28% of fund-days) by about 9.5 bp; two-day clusters roughly double it to about 19 bp, three- and four-day clusters triple and quadruple it; inflows have no effect; Panel B VAR shows cumulative responses at 10 and 20 days similar in size to the contemporaneous one, read as persistent (no reversal), i.e. NAV dilution borne by stayers; the introduction puts the cost of a single extreme outflow at up to 0.10% of AUM. Advisors are behind more than 90% of flows above 30x average. The exact coefficient and standard-error columns were not legible in the extract; read them off the PDF (http://ux-tauri.unisg.ch/RePEc/usg/sfwpfi/WPF-1408.pdf). Placement: Swedish context and incidence (the direct PPM precedent for fund-level dilution from coordinated redemptions; the thesis' fund-level test is the same regression with FTN redemptions of 20-44% instead of 10-30x average flow).

### Christoffersen, Keim and Musto (2007) [M] and Christoffersen, Keim, Musto and Rzeznik (2022) [V from RePEc listing; DOI not verified]
Christoffersen, Susan E. K., Donald B. Keim, and David K. Musto. 2007. "Valuable Information and Costly Liquidity: Evidence from Individual Mutual Fund Trades." Working paper (University of Toronto / Wharton). NOT VERIFIED; unpublished as such. The later published version: Christoffersen, Susan K., Donald B. Keim, David K. Musto, and Aleksandra Rzeznik. 2022. "Passive-Aggressive Trading: The Supply and Demand of Liquidity by Mutual Funds." Review of Finance 26(5): 1145-1177 (volume and pages from the RePEc listing; DOI not located).

Canadian fund trade data: trades motivated by flows (liquidity-demanding) underperform, trades that absorb others' flows (liquidity-supplying) earn a premium; the cost of flow-driven trading is a tax on stayers. Placement: incidence (flow-driven trades are costly to the fund; stayers pay unless swing pricing reallocates the cost).

---

## F. Event-study econometrics

### Kolari and Pynnonen (2010) [V-abs]
Kolari, James W., and Seppo Pynnonen. 2010. "Event Study Testing with Cross-sectional Correlation of Abnormal Returns." Review of Financial Studies 23(11): 3996-4025. DOI 10.1093/rfs/hhq072.

With event-date clustering even modest cross-correlation causes severe over-rejection; proposes an adjusted BMP statistic that corrects for average cross-correlation and extends to multi-day CARs; dominates the portfolio approach in power. Placement: method (FTN events hit many stocks on the same day; OMXSB reconstitutions cluster on semi-annual dates).

### Boehmer, Musumeci and Poulsen (1991) [V]
Boehmer, Ekkehart, Jim Musumeci, and Annette B. Poulsen. 1991. "Event-Study Methodology under Conditions of Event-Induced Variance." Journal of Financial Economics 30(2): 253-272. DOI 10.1016/0304-405X(91)90032-F.

Standardised cross-sectional test robust to event-induced variance increases. Placement: method (the base statistic that Kolari-Pynnonen adjusts; volatility rises on reconstitution and execution days).

### Kothari and Warner (2007) [V]
Kothari, S. P., and Jerold B. Warner. 2007. "Econometrics of Event Studies." In Handbook of Empirical Corporate Finance, Vol. 1, ed. B. Espen Eckbo, 3-36. Amsterdam: Elsevier. DOI 10.1016/B978-0-444-53265-7.50015-9.

Survey of short- and long-horizon event-study properties, specification and power. Placement: method.

### MacKinlay (1997) [V-abs]
MacKinlay, A. Craig. 1997. "Event Studies in Economics and Finance." Journal of Economic Literature 35(1): 13-39. DOI not verified (RePEc does not list one; JSTOR stable 2729691 [M]).

Canonical exposition of the market-model event study, estimation and event windows, test statistics. Placement: method.

### Young (2019) [V-abs]
Young, Alwyn. 2019. "Channeling Fisher: Randomization Tests and the Statistical Insignificance of Seemingly Significant Experimental Results." Quarterly Journal of Economics 134(2): 557-598. DOI 10.1093/qje/qjy029.

Randomisation inference applied to 53 AEA experimental papers finds 13-22% fewer significant individual coefficients and 33-49% fewer significant joint tests than the authors' methods. Placement: method (reference for the placebo-date and permutation tests on FTN execution days; with 394 OMXSB events and a handful of FTN dates, randomisation inference is the honest test).

### Petersen (2009) [V-abs]
Petersen, Mitchell A. 2009. "Estimating Standard Errors in Finance Panel Data Sets: Comparing Approaches." Review of Financial Studies 22(1): 435-480. DOI 10.1093/rfs/hhn053. (NBER WP 11280.)

When and why firm- and time-clustered standard errors differ; guidance on two-way clustering. Placement: method (clustering by event date and by stock in the pooled regressions).

---

## G. Swedish and pension context

### Sialm, Starks and Zhang (2015) [V-abs]
Sialm, Clemens, Laura T. Starks, and Hanjiang Zhang. 2015. "Defined Contribution Pension Plans: Sticky or Discerning Money?" Journal of Finance 70(2): 805-838. DOI 10.1111/jofi.12232. (NBER WP 19569.)

DC-plan flows into mutual funds are more volatile and more performance-sensitive than non-DC flows, mainly because plan sponsors change menus; DC money is "less sticky and more discerning". Placement: Swedish context and motivation (menu changes by a sponsor, not participants, drive large flows; FTN is the sponsor for 6m+ savers).

### Cronqvist and Thaler (2004) [V]
Cronqvist, Henrik, and Richard H. Thaler. 2004. "Design Choices in Privatized Social-Security Systems: Learning from the Swedish Experience." American Economic Review 94(2): 424-428. DOI 10.1257/0002828041301632.

The 2000 PPM launch: active choice encouraged, 456 funds, two thirds chose actively, concentrated and home-biased portfolios, the default outperformed. Placement: Swedish context.

### Cronqvist, Thaler and Yu (2018) [V]
Cronqvist, Henrik, Richard H. Thaler, and Frank Yu. 2018. "When Nudges Are Forever: Inertia in the Swedish Premium Pension Plan." AEA Papers and Proceedings 108: 153-158. DOI 10.1257/pandp.20181096.

Initial 2000 choices persist for well over a decade; inertia means the fund menu, not saver choice, determines where money sits. Placement: Swedish context (why forced reallocation by the state is the only way large positions move; why the flows are uninformed).

### Dahlquist, Setty and Vestman (2018) [V-abs]
Dahlquist, Magnus, Ofer Setty, and Roine Vestman. 2018. "On the Asset Allocation of a Default Pension Fund." Journal of Finance 73(4): 1893-1936. DOI 10.1111/jofi.12697.

Swedish registry data inside and outside the pension system; life-cycle model of a DC account with opt-out; the optimal default allocation gives a welfare gain of 1.5% in retirement over an age-based rule. Placement: Swedish context (PPM data description; heterogeneity of active versus passive savers).

### Kinnerud and Lorentzon (2026) [V-abs]
Kinnerud, Karin, and Louise Lorentzon. 2026. "Dominated Pension Investments: The Role of Search Frictions and Unawareness." American Economic Journal: Applied Economics 18(3): 115-144. DOI 10.1257/app.20240153. (Replication deposit DOI 10.3886/E215982V1.)

Large field experiment in the Swedish pension system: letters raising awareness of a dominated (high-fee index) fund and lowering search cost improve choices on average, but most savers do not respond even when search cost is removed; unawareness and search cost explain at most 45% of dominated choices; rejects fixed-adjustment-cost models. The RePEc abstract says "the Swedish pension system" without naming the premium pension; confirm in the PDF. Placement: Swedish context (saver inertia on the PPM platform; the state's rationale for procuring the menu).

### Choukhmane and De Silva (2026) [V-abs]
Choukhmane, Taha, and Tim De Silva. 2026. "What Drives Investors' Portfolio Choices? Separating Risk Preferences from Frictions." Journal of Finance 81(1): 5-48. DOI 10.1111/jofi.70013.

Variation in 401(k) default funds as a quasi-experiment: absent participation frictions 94% of investors would hold stocks; life-cycle estimates of RRA about 2.5, EIS about 0.25, a portfolio adjustment cost of about USD 160; low participation reflects frictions, not loss aversion. Placement: Swedish context and motivation (frictions, not preferences, keep savers where the menu puts them; forced reallocation is therefore not informative about preferences or fundamentals).

### Keim and Mitchell (2018) [V; DOI inferred from the CUP identifier S1474747217000336]
Keim, Donald B., and Olivia S. Mitchell. 2018. "Simplifying Choices in Defined Contribution Retirement Plan Design: A Case Study." Journal of Pension Economics and Finance 17(3): 363-384. DOI 10.1017/S1474747217000336 (inferred; not independently checked). (CFS WP 573, 2017.)

A large employer deleted nearly half of its DC fund menu; streamlined participants ended with lower expense ratios and turnover (aggregate savings about USD 20.2m over 20 years, more than USD 9,400 per participant) and lower equity and factor exposure. Placement: Swedish context (menu streamlining precedent; what happens to money when funds are removed).

### Pool, Sialm and Stefanescu (2016) [V-abs]
Pool, Veronika K., Clemens Sialm, and Irina Stefanescu. 2016. "It Pays to Set the Menu: Mutual Fund Investment Options in 401(k) Plans." Journal of Finance 71(4): 1779-1812. DOI 10.1111/jofi.12411. (NBER WP 18764.)

Trustee families favour their own funds: poorly performing affiliated funds are less likely to be deleted and more likely to be added; participants do not undo it; subsequent performance shows the decisions are not information-driven and are costly. Placement: Swedish context and motivation (menu decisions are not informative about fund quality; supports the "uninformed" label on FTN removals, with the caveat that FTN removals are quality-screened on fees and track record).

---

## Search for 2024-2026 work on Sweden's fondtorg procurement, Fondtorgsnamnden, or the 2019 PPM purge

What was searched (within the tool limits): the SHoF Research Paper Series SSRN RSS feed (50 most recent papers, through Dec 2025): nothing on fondtorget, FTN, PPM procurement or the 2019 purge. RePEc listings of JF 2024-2026, JFE 2023-2026, RFS 2023-2026, RoF 2018-2026, AER 2025-2026, AEJ Applied 2022-2026, Management Science 2024-2026: no title mentioning the Swedish premium pension fund platform, procurement or fund removals, other than Kinnerud and Lorentzon (2026, dominated funds, field experiment, not about forced flows). Pensionsmyndigheten press room and "Nyheter i fondtorget" (229 entries, 31 read): institutional notices only. Could not reach: SSRN search, DiVA (student theses), fondtorgsnamnden.se, Google Scholar, Semantic Scholar, OpenAlex, CORE, scholar.archive.org (all blocked or rate-limited), and WebSearch was exhausted before this task started. Riksbank WP listing is JavaScript-rendered and returned nothing.

Conclusion: no academic paper on FTN forced flows or the 2019 purge was found. This is weak evidence of absence given the blocked channels; a follow-up with WebSearch/SSRN on "Fondtorgsnamnden", "upphandlat fondtorg", "premiepension upphandling", "PPM 2019 reform fund removal" is recommended. The closest existing academic precedents are Dahlquist, Martinez and Soderlind (2017, PPM coordinated outflows and NAV impact), Da, Larrain, Sialm and Tessada (2018, Chile), and Sabbatucci, Tamoni and Xiao (2023 WP, 401(k) menu shifts).

Institutional sources found (verified pages, for the Swedish-context section):
- Pensionsmyndigheten, "Vad hander med dina fonder nar fondtorget upphandlas?" (undated, read 2026-10-12), https://www.pensionsmyndigheten.se/nyheter-och-press/nyheter-fondtorg/Ett-upphandlat-fondtorg. Key statements: AP7 Safa savers unaffected; a fund that is not procured is deregistered and holdings are moved automatically to a procured fund in the same category with similar risk and lower fee; savers get a letter and about two weeks to choose otherwise; about 12 months from procurement documents to availability of procured funds (example: award 28 May 2026, selectable July 2026); "Det kan ta flera manader att avregistrera stora fonder" because managers need time to sell large holdings and sales must not move market prices; switches that cannot be processed within a week are queued to the next week.
  IMPORTANT for the thesis premise: this page says deregistration of large funds is staggered over months and explicitly aims not to move prices, which sits uneasily with "the state redeems 20-44% of each losing fund on one day". The thesis must document, event by event, the actual redemption schedule (one day versus staggered) from Pensionsmyndigheten data or fund-company NAV/AUM series before the execution-day design is fixed.
- Pensionsmyndigheten, "Nio svenska smabolagsfonder ar inte langre valbara" (18 Aug 2026): nine Swedish small-cap funds not procured and no longer selectable from 18 August 2026 (Carnegie Smabolagsfond A, C WorldWide Sweden Small Cap 1A, Evli Sverige Smabolag, Humle Smabolagsfond A, Lannebo Small Cap Opportunities A, Lannebo Sweden Micro Cap, Lansforsakringar Smabolag Sverige Vision A, Skandia Smabolag Sverige, Spiltan Smabolagsfond); ten procured replacements (Aktiespararna Smabolag Edge, AMF Aktiefond Smabolag, Cliens Smabolag, Danske Invest SICAV Sverige Smabolag SI, D&G Smabolag, Handelsbanken Svenska Smabolag A1, Lannebo Smabolag, Nordea Smabolagsfond Sverige, SEB Sverigefond Smabolag, Swedbank Robur Smabolagsfond Sverige A). Procurement of Sverige smabolag completed 12 June 2026; European small caps completed 12 June 2026 and three funds removed 7 July 2026; global technology completed 5 Oct 2026; the global equity award was appealed to Forvaltningsratten (10 Mar 2026). These are the live FTN events for the stock-level analysis (Swedish small caps are the OMXSB-adjacent universe where impact should be largest).

---

## Verification tally

Verified bibliographic records [V] or [V-abs]: 52 entries (A: 11 + 2 bonus; B: 7; C: 9; D: 4; E: 8; F: 6; G: 8), counting Gabaix-Koijen and Lewrick-Schanz as verified working papers and Sabbatucci-Tamoni-Xiao as verified via the SHoF SSRN feed.

[M] entries (bibliographic data from memory, not verified): Almgren, Thum, Hauptmann and Li (2005); Frazzini, Israel and Moskowitz (2018); Schmickler and Tremacoldi-Rossi (WP); Christoffersen, Keim and Musto (2007 WP). Partially unverified: Christoffersen et al. (2022) DOI not located; Keim and Mitchell DOI (inferred from the CUP identifier); Coval-Stafford DOI not located; MacKinlay DOI not located; the "Who Clears the Market" author list.

Magnitudes flagged [M] inside otherwise verified entries: Shleifer, Harris-Gurel, Greenwood 2005, Chang-Hong-Liskovich, Coval-Stafford, Mitchell-Pulvino-Stafford, Edelen, Greene-Hodges, Frazzini et al.
