# How five prize-winning SSE theses are built

Source texts: plain-text extractions in `scratchpad/fresh/winners/`. Page counts are taken from the page markers in the extractions. "Main text" means from the first page of the introduction to the last page of the conclusion, including any tables and figures placed inside that span. Tables and figures parked in an appendix are counted separately.

Course limit (course_intro.txt, slide 19): "Total length: up to 40 pages, single-spaced equivalent (including tables)." Introduction 2 to 4 pages. Related literature under 1 page. No table of contents. Table captions must be self-contained.

Summary table

| Thesis | Main text pages | Total pages | Tables (main + appendix) | Figures (main + appendix) | Anchor | Hypotheses stated as | Theory presented as |
|---|---|---|---|---|---|---|---|
| 2015 PH, Fund flow risk | 30 | 32 | 5 + 0 | 5 + 0 | Literature (Coval-Stafford 2007, Lou 2012, Brennan 1993), no single table replicated | Hypothesis 1, Hypothesis 2 in the intro; Propositions 1 to 3 in section 4.2 | Modified Brennan (1993) utility, eqs (4) to (6), derivation delegated |
| 2016 PH, Intermediary asset pricing | 25 | 38 | 7 + 4 | 4 + 4 | Adrian, Etula, Muir (2014 JF) and He, Kelly, Manela (2016 wp) | One research question in its own two-sentence section | Verbal: debt-constraint versus equity-constraint frameworks, no equations |
| 2020 PH, Chasing your own tail | 27 | 53 | 13 + 0 (all 13 in appendix) | 11 + 0 (all 11 in appendix) | Tuzun (2014 Fed wp), plus Kyle-Obizhaeva (2012) impact formula | One research question in italics; expectations in prose | Rebalancing algebra eq (1), impact formula eq (3), derivation delegated by footnote |
| 2021 SV, Invariance and spreads | 38 | 45 | 9 + 2 | 3 + 1 | Kyle-Obizhaeva (2017 wp), Andersen et al. (2018 wp), Kyle-Obizhaeva (2019 wp) | Two block-quoted hypotheses; first formalised as H0: beta = 1, H1: beta not 1 | Full chain, eqs (1) to (15), dimensional analysis with intuition |
| 2024 PH, The smooth transition | 17 | 27 | 8 + 6 | 3 + 0 | Ahern and Dittmar (2012 QJE) | One research question in italics | None; eqs (1) to (3) are definitions and regression specs |

Across the five: median main text 27 pages, median 8 tables, median 4 figures. The two most recent winners are the shortest (17 and 27 pages of main text), which is where the course now wants you.

---

## 1. 2015 Per Hiller: "Fund Flow Risk and Cross-Sectional Asset Prices" (Bergenstrahle and Nordqvist)

Closest design to thesis 2: flows from open-end funds moving stock prices, with a mechanism test (hedging versus price pressure) and asymmetric reversals.

### Section list and pages

| Section | Pages | Content |
|---|---|---|
| Abstract | 0.5 | 12 lines, gives the result (0.5 percent monthly alpha) and the verdict on both hypotheses |
| 1 Introduction | 1 to 3 | Motivation (47 percent institutional ownership), method in one sentence, two named hypotheses, results, three-part contribution, roadmap |
| 2 Data and Methodology | 3 to 5 | 2.1 Data (ICI, CRSP, French, Thomson S12); 2.2 Beta estimation, eqs (1) and (2); 2.3 Fama-MacBeth, eq (3) |
| 3 Results | 5 to 7 | Table 1 (premium by sub-period), Figure 1 (cumulative premium) |
| 4 Hypotheses | 7 to 28 | 4.1 Hedging hypothesis: Brennan model, eqs (4) to (6), Table 2. 4.2 Price pressure: Propositions 1 to 3, Figure 2 (schematic), Figure 3 (flow distribution), unexpected flows eq (9), 4.2.1 to 4.2.3 one test per proposition (Tables 3, 4, Figure 4), 4.2.4 trading strategy (Table 5, Figure 5) |
| 5 Conclusions | 28 to 30 | What was found, what it means for asset pricing models, what it does not mean |
| References | 31 to 32 | 18 entries |

No separate related-literature section. The relevant papers are cited inside the introduction (contribution paragraph) and at the top of each hypothesis subsection, three or four papers at a time.

### Where the anchor is introduced
Page 1, footnote 2 (Shleifer 1986 on index inclusion) and page 2, the contribution paragraph: "This result corroborates a number of recent papers that find evidence of a price impact from liquidity-based trading in open-end funds, most notably Coval and Stafford (2007) and Lou (2012)." Brennan (1993), the theory anchor, waits until section 4.1.

### Replication versus extension
No single published table is replicated. The baseline is a standard Fama-MacBeth test of a new factor (Table 1), then the thesis moves to mechanism tests. The ordering is the craft: headline fact first (section 3), then "we propose two hypotheses that try to explain" it (section 4), one test per proposition, then economic significance last (trading strategy).

### How hypotheses are stated
Named and numbered in the introduction, each with a two-sentence derivation from a literature:

> "Hypothesis 1 (the hedging hypothesis). Our first hypothesis is derived from the literature on agency-based asset pricing."

Then in section 4.2 the second hypothesis is broken into three testable propositions, each a short paragraph with the predicted sign, and each followed by a subsection named "Test of proposition k". The verdict is delivered in the intro: "Taking both hypotheses to the data, we reject the first but find strong support for the second hypothesis."

### Theory
A modified Brennan (1993) utility function (eqs 4 and 5), and the resulting pricing equation (6) with the sign prediction. The derivation itself is delegated: "Brennan shows that solving the maximization problem for fund managers provides the following asset pricing model." The intuition follows in six plain sentences. Figure 2 is a schematic drawing of the price path under symmetric and asymmetric pressure, with a two-paragraph caption that works as a stand-alone explanation of the hypothesis. This is the best single exhibit to imitate for thesis 2.

### Data section
By source, one paragraph each, with period and N inside the paragraph (374 months; 19,338 firms; 228,289 stock-quarters). Variable construction in numbered equations with "where" definitions. Footnotes hold the filters (at least 36 non-missing returns).

### Standard errors and robustness
Fama-MacBeth t-statistics for the premia; robust standard errors clustered by stock in the holdings panels, stated in every caption. Robustness is handled by footnote and by "In results not shown, we find that these results hold when we include the stock characteristics from (8)" and "these results hold when we control for firm fixed effects." Footnote 10: "The results are similar but somewhat less significant if we consider total (i.e., the sum of expected and unexpected) fund flows instead." The trading rules are kept deliberately crude: "The rules have deliberately been made very simple in order to increase the robustness of our results."

### Conclusion calibration
Claims: the premium exists, it comes from reversal of flow-induced pressure, reversals are larger after negative flows. Refuses: to call it a priced risk factor. "fund flow risk is not a priced risk factor in the sense that fund flows are partially correlated with the marginal utility of any market participant. Rather, it is an expression of market inefficiencies". Closing line: "we hope that this paper has not only introduced yet another risk factor but also offered a viable explanation for why it appears to be priced".

### Captions
Every table caption restates the full regression equation and defines every symbol. The caption of Table 4 is longer than the table.

---

## 2. 2016 Per Hiller: "Intermediary Asset Pricing and the Swedish Equity Market" (Barketorp Dirke and Ye)

Replication of a recent JF paper (Adrian, Etula, Muir 2014) and a then-working paper (He, Kelly, Manela) on hand-built Swedish data.

### Section list and pages

| Section | Pages | Content |
|---|---|---|
| Abstract | 0.5 | Result (MAPE 6.8 percent) and the calibrated verdict in the last sentence |
| I Introduction | 1 to 2 | Theory in one paragraph, the two papers, method (21 portfolios, two-pass), numbers, roadmap |
| II Research question | 2 | Two sentences |
| III Theory and Previous Literature | 2 to 5 | Debt-constraint versus equity-constraint frameworks, the two anchor papers with their published numbers, why Swedish bank structure matters |
| IV Data | 5 to 13 | 1 Leverage factor (Statistics Sweden, two spliced series), 2 Capital factor (Compustat, Riksgalden list), 3 Comparison (Tables III, IV), 4 Test assets and benchmark factors (self-built FF portfolios) |
| V Empirical Approach | 14 to 15 | Two-pass regression, MAPE definition, why MAPE not R2, Lewellen et al. critique |
| VI Empirical Results | 15 to 21 | Table V (main), Figures 3 and 4, Table VI (pricing errors), Table VII (time series) |
| VII Discussion and Further Research | 21 to 24 | What could not be done and why (no Swedish hedge fund leverage data, no bond portfolios, Shanken correction) |
| VIII Conclusion | 24 to 25 | Half a page |
| References | 26 to 27 | |
| Appendix I to V | 28 to 38 | Seasonal adjustment test, primary dealer list, cyclicality plots, test asset coverage, combined model |

### Where the anchor is introduced
Page 1, second paragraph: "We have decided to base our research on intermediary asset pricing in Sweden on two papers: one by Adrian et al. (2014a) ... and the other one is by He et al. (2016)". The anchor papers' own results (adjusted R2 77 percent, yearly MAPE 1.3 percent) are quoted in section III so the reader can compare.

### Replication versus extension
Same method as the anchor (two-pass, free intercept, MAPE), adapted test assets (21 instead of 41 portfolios, all self-built), new factor series. The replication and the Swedish result share one table (Table V), with the two anchor models side by side with CAPM and FF3 benchmarks in matched sample periods. The anchor's US numbers are not in the table; they sit in the literature section text. Extension: the comparison of constraint frameworks (Table III) and the combined model (appendix Table AIV).

### How hypotheses are stated
No numbered hypotheses. Section II states the research question in two sentences. The theory section gives the sign prediction in prose: "if this framework holds, will correspond to a positive price of leverage risk".

### Theory
Verbal only. Two paragraphs contrast the frameworks and state what sign each predicts. Equations appear only for factor construction and the two-pass regression.

### Data section
By variable, not by source. Each factor gets its construction equation, its sources, its splice points, and its known defects (confidentiality, translation of "broker-dealer", Compustat exclusion bias with only about 28 firms early on). A correlation table follows each factor so the reader sees it is not a repackaged market factor. Table titles are declarative, JF style: "Broker-Dealer Leverage Growth is Uncorrelated with Other Explanatory Factors"; "Broker-Dealer Leverage is Pro-Cyclical, Primary Dealer Capital Ratio is not".

### Standard errors and robustness
Both White-corrected and Fama-MacBeth t-statistics reported in the same table. Seasonal adjustment tested and rejected in the appendix. Shanken (1992) correction named as a limitation, not done. The power motive is stated: "The objective of including different portfolio sorts other than size and book-to-market is to increase power".

### Conclusion calibration
The most quoted line of all 25 winners: "Our results do not prove the validity of the model, but rather bring into question the validity of the standard benchmarks." In the results: "we cannot infer that the AEM model performs well, but only that the benchmark models perform very poorly." On comparability: "It should be emphasized that the performance of the two intermediary asset pricing models cannot be compared with each other, since the sample periods do not match." And a line on priorities: the aim is "the first out-of-country sample test of intermediary asset pricing and not a well performed exercise in econometrics for its own sake."

---

## 3. 2020 Per Hiller: "Chasing Your Own Tail" (Gustafsson and Gerell)

Predictable LETF rebalancing flows in Sweden, with a split between direct and anticipatory price pressure. The institutional feature (XACT is the only issuer, execution window known) is the identification.

### Section list and pages

| Section | Pages | Content |
|---|---|---|
| Abstract | 1 | All headline numbers (SEK 89m per 1 percent move; 4.0 bps; 11.8 bps; 8.9 bps in crisis; anticipatory trading dominates) |
| 1 Introduction | 1 to 5 | 1.1 Background and relevance (results with numbers on pages 2 to 3); 1.2 Research question (one italic sentence); 1.3 Contribution (fourfold); 1.4 Scope; 1.5 Disposition |
| 2 Theory, Practice and Literature Review | 6 to 11 | 2.1 Rebalancing algebra, eq (1); 2.2 XACT institutional details, C&R flows eq (2); 2.3 Futures to stock propagation; 2.4 Literature (LETFs; invariance, impact formula eq (3)) |
| 3 Data | 12 | 3.1 Sources (one paragraph names every source); 3.2 Processing |
| 4 LETF Rebalancing and the Market | 13 to 15 | Descriptives: Tables I to III, Figures I to VI, tracking regression eq (4) |
| 5 Flow-Induced Market Impact | 16 to 21 | 5.1 Price impact, eq (5), Tables IV and V; 5.2 Volatility, eq (6), Table VI; 5.3 Anticipatory trading, eqs (7) and (8), Tables VII and VIII; 5.4 Mean reversion, eqs (9) and (10), Tables IX and X |
| 6 Case Study: the Corona Crisis | 22 to 23 | Same regressions on the crisis window, Tables XI and XII |
| 7 Price Impact and Invariance | 24 to 25 | Implied impact, eqs (11) and (12), Table XIII, Figures VII to XI |
| 8 Concluding Remarks | 26 to 27 | 8.1 Conclusion; 8.2 Future research |
| 9 References | 28 to 29 | |
| Appendix | 30 to 53 | All 13 tables and 11 figures, each on its own page with a full caption |

Note: the intro runs five pages, above the course guidance of two to four, because it carries a scope and a disposition subsection. The main text without exhibits is 27 pages; with the appendix exhibits it would be about 50. Under the current 40-page rule (tables included) this layout would not pass unless the exhibits were cut to the best eight.

### Where the anchor is introduced
Page 1, second paragraph, for the risks ("Tuzun, 2014") and page 1, third paragraph, for the method: "Tuzun (2014) implements a model of price impact developed in Kyle and Obizhaeva (2012) to show that the effects of rebalancing flows are notable". The replication sentence is on page 16: "We implement the following regression specification, as in Tuzun (2014), but include scaled creation and redemption flows as an additional control variable".

### Replication versus extension
Same table. Table IV column 1 is the Tuzun specification; column 2 adds the control. Tuzun's qualitative result is matched in the text: the Swedish results "do not differ markedly in kind or size from what has been presented in previous papers." The extensions are separate sections: anticipatory trading (5.3), crisis (6), implied impact (7). Each extension reuses the same scaled variables so coefficients are comparable across tables.

### How hypotheses are stated
Not numbered. One research question in italics: "What is the market stability impact of LETFs' rebalancing trades in the Swedish stock market?" Expectations appear in prose at the start of each subsection: "Due to the mathematically predictable nature of rebalancing flows, we expect some degree of anticipatory trading."

### Theory
Three equations. Eq (1) is simple algebra deriving the rebalancing amount, with a worked example (Black Thursday, XACT BEAR 2 rebalanced 63.42 percent of assets). Eq (3) is the Kyle-Obizhaeva impact formula, stated, not derived: "See Kyle and Obizhaeva (2012) for the derivation of the implied price impact equation." No model of liquidity provision.

### Data section
Shortest of the five (one page). Sources in one paragraph, processing in one paragraph, descriptives moved to their own section. A power statement of sorts opens it: "Due to being constrained to a relatively short sample period and the smaller relative size of the Swedish LETF market, we anticipate that results may have lower significance than those demonstrated in previous papers. Thus, we have resolved to minimise any unnecessary approximations by utilising the most granular data available."

### Standard errors and robustness
Standard errors clustered by date in every regression; all variables winsorised at 1 and 99 percent; returns scaled by stock volatility and flows by ADV to handle heteroskedasticity across stocks. Robustness: market ups versus downs (Table V), 40-day and 60-day estimation windows for ADV and volatility (Figures X and XI), crisis subsample.

### Null results
The reversal regressions (Tables IX and X) are insignificant, unlike Tuzun: "The lack of significance is likely a result of the short sample period, however, it may indulge the idea that the Swedish stock market is not as efficient as the US stock market. Further analysis is required to make confident statements regarding either proposition." The crisis volatility regression is also null and is explained the same way.

### Conclusion calibration
Claims a conditional result: "LETFs appear to have a negligible effect on 'normal' markets but may prove harmful to markets in crisis." On the key identification: "we do not claim to fully disentangle the effects, but rather to show the prevalence of anticipatory trading and its size relative to the direct price impact estimated earlier." The worst-case paragraph about a 1987-style crash is the one place the thesis over-reaches.

### Craft to copy
Every coefficient is converted to basis points for an average stock in the same sentence: "The price reaction for the average stock in the OMXS30 in response to a 1 % index move is therefore 4.0 basis points (1.499 x 1% x 2.7 %), all else equal."

---

## 4. 2021 Staffan Viotti: "Market Microstructure Invariance, Bid-Ask Spreads and Impact Costs" (Domeij and Krieg)

The most mathematical winner. Useful as a model for presenting a theory chain, and as a warning about length.

### Section list and pages

| Section | Pages | Content |
|---|---|---|
| Abstract | 0.5 | |
| Introduction (unnumbered) | 2 to 4 | HFT context, invariance in one paragraph, two research questions in italics, headline result with the confidence interval, roadmap |
| 1 Fundamental Concepts | 5 to 6 | Glossary: bets, business time, spread, illiquidity, tick size |
| 2 Literature Review | 7 to 8 | Three anchor papers, one subsection each, ending with what is taken from each |
| 3 Theoretical Background | 9 to 17 | 3.1 Dimensional analysis, leverage neutrality, invariance assumptions, eqs (1) to (9); 3.2 Crash impact: conventional wisdom eq (10), invariance eqs (11) and (12) |
| 4 Hypotheses and Research Design | 18 to 22 | 4.1 Two hypotheses, eqs (13) and (14), H0 and H1; 4.2 Design: cross-section, intraday, correlational, OLS, confidence intervals, non-statistical test |
| 5 Data | 23 to 29 | 5.1 Stock data (SHoF, 375 million rows), 5.1.1 limitations, 5.1.2 variable construction, 5.1.3 summary statistics (Table 1, Figure 1); 5.2 Futures data (Table 2) |
| 6 Empirical Findings | 30 to 37 | 6.1 Spread versus illiquidity: Table 3, Figure 2, Table 4, tick-size extension eq (15); 6.2 Crash: Figure 3, Tables 5 to 9 |
| 7 Concluding Remarks | 38 to 39 | |
| References | 40 to 41 | |
| Appendix A to C | 42 to 45 | Per-stock plots, yearly regressions, variable construction |

### Where the anchor is introduced
Page 2, fourth and fifth paragraphs: Kyle and Obizhaeva (2016) defined, then "Kyle and Obizhaeva (2017) confirm for Russian and US stocks that there exists a proportional relationship between relative bid-ask spread costs and an illiquidity measure".

### Replication versus extension
The replication (K-O 2017 regression of log spread on log illiquidity, slope predicted to be one) is Table 3 and Figure 2. The anchor's own fitted lines are quoted beside the Swedish line in the text: "For the Russian stocks, their fitted line is ln(S/P) = 2.093 + 0.998 ln(1/L). ... Hence, our results are similar to the results reported by Kyle and Obizhaeva (2017), in particular their fitted line for the Russian stocks." Extensions sit in the same subsection (intraday frequency, tick-size and lot-size variables from eq 15, which raise R2 from 0.7786 to 0.8110) and in a second subsection (the 2020 crash, where the model is applied, not tested).

### How hypotheses are stated
Two hypotheses, each a block-quoted italic sentence stating the relationship, the sample and the period. The first is then written as a regression with H0: beta = 1 and H1: beta not equal to 1, and the authors note that failure to reject confirms the theory. The second is openly declared untestable: "We are not able to statistically test this second set of hypotheses for two reasons. First, these are the same hypotheses as formulated in Kyle and Obizhaeva (2019) and they do not provide an appropriate test statistic. Second, we have only looked at one stock market crash".

### Theory
Fifteen numbered equations following Kyle and Obizhaeva (2017) step by step, with the G.I. Taylor atomic bomb story as the intuition for dimensional analysis. The authors are explicit about what they take as given: "we take this specification as exogenously given, provided by existing theory in the field of market microstructure invariance." Nine pages of theory for a one-coefficient test is more than thesis 2 should spend; the lesson is the discipline of tying each equation to the hypothesis it generates ("This relationship provides the theoretical foundation for our first hypothesis").

### Data section
Organised by hypothesis (stocks for H1, futures for H2), each with sources, cleaning, limitations and summary statistics. The limitations subsection says what was not available (realised spreads, futures before 2020) and why the substitute is acceptable under the theory. The aggregation procedure (volume-weighting then time-weighting) is moved to Appendix C.

### Standard errors and robustness
The test is a 95 percent confidence interval around the slope (0.9707 to 1.0054). Robustness: per-stock slopes (Table 4, Appendix A), per-year regressions (Appendix B, where the slope is rejected in every year except 2017), three calibration windows for the impact model, three sub-periods of the crash. No clustering is reported, which is a weakness given 3535 pooled stock-interval points.

### Conclusion calibration
"Kyle and Obizhaeva (2017) do not investigate causality between the two variables, and neither do we." On the crash: "we as Kyle and Obizhaeva (2019), are not able to statistically validate the general applicability of this model due to a small sample size." On the yearly rejections the authors neither hide nor explain them away: they report that the slope holds pooled but fails year by year and point to the MiFID II tick-size change in 2018 as a candidate reason.

### Warning
This thesis contains a glossary section and a paragraph explaining what OLS is, which the course slides explicitly forbid. It won in spite of that, not because of it. It is also 38 pages of main text, which with the current 40-page limit including tables leaves no room.

---

## 5. 2024 Per Hiller: "The Smooth Transition" (Fager and Ohman Tunklint)

A regulator-imposed shock (French board quota), replicated from Ahern and Dittmar (2012), with a null result on firm value handled well. Shortest winner.

### Section list and pages

| Section | Pages | Content |
|---|---|---|
| Abstract | 1 | Result stated as a null in sentence four, mechanism in sentence six |
| 1 Introduction | 2 to 4 | Policy context, the anchor, research question in italics, the law in one paragraph, France versus Norway, results with numbers, data in one paragraph, method in two paragraphs, mechanism, then a run-in paragraph headed "Related literature" (one page) |
| 2 Data and Methodology | 4 to 11 | 2.1 Data gathering (Refinitiv, CapitalIQ, hand-coded annual reports, Namsor name database); 2.2 Summary statistics (Tables 1, 2, Figures 1, 2); 2.3 Corporate governance in France, Europe and the US (institutional background, control group choice); 2.4 Methodology: 2.4.1 Event study (Tables 3, 4 balance tests), 2.4.2 Long-term IV, eq (2), board skills eq (3) |
| 3 Results | 11 to 14 | 3.1 Event study (Tables 5, 6); 3.2 Tobin's Q (Table 7), board skills (Table 8), appendix tables referenced |
| 4 Discussion | 15 to 18 | Result by result against Ahern and Dittmar's numbers; the mechanism (skills, size, tenure unchanged); institutional explanation (six years versus two, fee suspension versus dissolution); Figure 3 reproduced from the anchor |
| 5 Conclusion | 18 | Half a page |
| Appendix A | 19 to 24 | Tables 9 to 14: reduced forms, first stage, ROE robustness, board size, board tenure |
| Appendix B | 25 | AI disclosure, two sentences |
| References | 26 to 27 | |

### Where the anchor is introduced
Page 2, paragraph one, sentence eight: "A prominent study by Ahern and Dittmar (2012) on the Norwegian gender quota from 2003 found significant costs to shareholders and a decrease in board skills. As such, this paper employs a methodology akin to Ahern and Dittmar (2012)".

### Replication versus extension
The thesis reproduces both of the anchor's designs (announcement event study with a high versus low diversity split; IV on pre-quota female share interacted with year dummies) on French data. Tables 5 to 7 mirror the anchor's tables. The anchor's own estimates are not placed in the tables; they are quoted in the Discussion text, result by result: "Ahern and Dittmar (2012) found that Low board gender diversity firms had, on average, a 3.56% worse return than the High diversity group"; "Our results differ from the paper by Ahern and Dittmar (2012), who found that firm value decreased by 1.9% as a result of the quota." The extension is the mechanism (Table 8 on board skills; Tables 13 and 14 on board size and tenure) and the institutional contrast that explains the different result.

### How hypotheses are stated
One research question in italics: "Are board gender quotas unfavorable for firm value?" No numbered hypotheses; the expected signs come from the anchor.

### Theory
None. Equation (1) defines Tobin's Q, equations (2) and (3) are the IV specifications. The causal story is institutional, not formal.

### Data section
Sources first, then exclusions with counts (69 firms from Refinitiv, topped up to 93 by hand), then the hand-coding protocol in full: "We first checked if pronouns were mentioned in the description of the director. When no pronouns were used, we visually determined the gender." Then the Namsor name-frequency check. Summary statistics by year for both countries, and two figures with the three legal dates as vertical lines. Then the institutional background subsection, placed inside Data and Methodology rather than as its own section.

### Standard errors and robustness
Standard errors clustered by firm in all firm-fixed-effects regressions, citing Bertrand, Duflo and Mullainathan (2004). Balance tests on characteristics (Table 3) and sectors (Table 4) with Fisher's exact test (p = 0.78). US placebo on every IV regression. Alternative outcome (ROE, Table 12). Reduced form year by year (Table 9) to check for lagged effects to 2021. First stage reported (Table 11).

### What the 2024 winner did with a null result
1. Said it first and plainly, in the abstract and the first sentence of the conclusion: "we find no support for the French board gender quota impacting firm value negatively."
2. Reported the point estimate and standard error every time, so the reader can judge the confidence interval: "the point estimate -0.279% was insignificant"; board skills "0.161%, which was insignificant".
3. Showed that the design had bite where it should: the first stage is strong (Table 11), and the US placebo is also null, so the null is not a failed instrument.
4. Looked for the effect in alternative outcomes (ROE), alternative timing (reduced form by year, lags to three years after the deadline), and found nothing there either.
5. Turned to mechanism: the channel that produced the anchor's negative result (fall in board skills) is absent in France (board skills, size and tenure unchanged), which makes the null plausible rather than suspicious.
6. Explained why with institutions: six-year transition versus two, suspension of fees versus dissolution, and showed the smooth path in Figure 1 against the anchor's spike in Figure 3.
7. Did not apologise, and did not compute power. With 93 firms the minimum detectable effect on Tobin's Q is probably larger than the anchor's 1.9 percent, so "no effect" and "could not have seen the effect" are not separated. This is the one thing thesis 2 must do better.

Two places where the prose slides from "insignificant" to "no effect" should be read as traps: "This means that the mandated board changes did, in fact, not decrease board skills, as the regression result shows a positive although insignificant result", and the conclusion's "a gender quota does not need to negatively affect firm value".

### Conclusion calibration
Claims: no evidence of a negative effect; smooth transition; board skills maintained. Refuses: to claim the quota helped, or that the French result generalises beyond the institutional conditions named. The policy sentence is kept conditional on "the longer transition period and possibly the more lenient penalty".

### AI disclosure
Appendix B, two sentences: "We have utilized both Gemini and ChatGPT to assist us in the coding process. The AI tools have been used to spot coding errors and propose different methods for completing programming operations." The course slides do not require this, but the most recent winner did it.

---

## What all five do that most theses do not

1. **The introduction gives the numbers.** Each intro contains the point estimates and the verdict on each hypothesis before the reader reaches the data section: 0.23 percentage points per month (2015); MAPE 6.8 versus 22.0 percent (2016); 4.0, 11.8, 5.5, 16.4 and 8.9 basis points (2020); slope 0.9881 with interval 0.9707 to 1.0054 (2021); 0.83 percent insignificant, -0.279 percent insignificant (2024). A reader who stops after page 3 knows the answer and how big it is.

2. **One anchor specification is reproduced and then benchmarked against the anchor's published numbers in the text.** Tuzun's pattern (2020), Kyle-Obizhaeva's fitted lines for Russia and the US (2021), Adrian et al.'s R2 and MAPE (2016), Ahern-Dittmar's 3.56 and 1.9 percent (2024). The comparison is a sentence, not a table column, and it comes before any extension.

3. **A mechanism test follows the headline result, and the conclusion states exactly what the design cannot show.** Hedging versus price pressure (2015); debt versus equity constraint (2016); direct versus anticipatory trading (2020); tick-size regime (2021); board-skills channel (2024). Then: "There is no claim to causality"-type sentences in every conclusion, written by the authors before an examiner can write them.

Two further habits worth copying: table captions that restate the equation and define every symbol (2015, 2016, 2020, 2021), and coefficients converted into economic units in the same sentence they are reported (basis points per 1 percent move, percent per annum, monthly alpha).

What none of the five did: compute a minimum detectable effect. The course slides ask for it ("Minimum detectable effect: check the power of your test"). Thesis 2 should be the first.
