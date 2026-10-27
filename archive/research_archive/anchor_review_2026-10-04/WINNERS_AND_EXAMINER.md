**What the awarded theses do, and what the examiner evidence supports**

Research date: 4 October 2026. This review separates observed features, my interpretation of their research value, and facts about the examiner. It does not identify the jury’s private reasons or predict a grade.

**The comparison is informative, but “winner versus non-winner” is an imperfect label**

The repository contains 25 awarded theses from 2011–2024 and 635 other full texts spanning 2009–2026. I audited the 660 catalogue records, reviewed the awarded-thesis abstracts and closely examined selected introductions, designs and conclusions on both sides. I have not closely read all 660 theses. The comparisons below are concrete qualitative cases, not a fully double-coded content analysis.

The folder name `non_winners` is not proof that every thesis in it failed to win an award. The repository itself flags *Leading the Wallet* (archive ID 6338, thesis year 2025) as a later award recipient outside the existing winner collection. Grades and nomination eligibility are not observed. To reduce cohort mismatch, the numerical comparison uses the 511 other theses from the same 2011–2024 years as the awarded set.

| Reproducible descriptive measure | Awarded collection | Same-year comparison |
|---|---:|---:|
| Theses | 25 | 511 |
| Median extracted word count | 13,446 | 13,088 |
| Detected contents heading | 12/25, 48.0% | 244/511, 47.7% |

These are text-extraction measures, not audited main-text word counts. Reweighting the comparison group to the winners’ year distribution changes its contents-heading rate to 53.3%; it still provides no compelling contents-page explanation of awards. A few long or old winning theses also differ substantially from today’s format rules. Follow the current course rules rather than copying their historical layout.

The pre-existing `thesis_metrics.py` is unsafe for several proposed comparisons: its case-insensitive `DiD` expression also matches ordinary “did,” and reference extraction can misread OCR text. The exploratory output CSVs are retained for transparency but are not evidence that winners use a particular estimator or have a particular number of references. The separate [audit script](audit_sources.py), [inventory](corpus_inventory.csv) and [summary](corpus_summary.json) reproduce the limited descriptive claims above.

**The useful difference is the structure of the research argument**

The strongest awarded examples make it easy to see why a setting, variable or extra test changes what one can learn. An extension is part of the argument, not simply another regression at the end. Here are the most transferable examples.

| Awarded thesis in the repository | Concrete feature | Why it strengthens research; implication for FTN |
|---|---|---|
| [The Smooth Transition, 2024](../../old_winners/2024_per_hiller_the_smooth_transition.pdf), ID 6053 | Builds on the board-quota literature, studies France, and examines board composition alongside firm value. The longer adjustment period and institutional differences motivate the setting. | The country changes an economic mechanism. The thesis can remain informative with a null value result. For FTN, public selection and outside-platform demand must motivate Sweden; country novelty alone does not. Cross-country institutional comparisons do not separately identify every institutional feature. |
| [Changing Patterns over the FOMC Cycle, 2023](../../old_winners/2023_per_hiller_changing_patterns_over_the_fomc_cycle.pdf), ID 5734 | Replicates the earlier cycle result, extends the sample, and investigates changes in meeting timing, monetary-policy conditions and uncertainty. | A disappearing result creates a question about mechanism rather than ending the paper. For FTN, ask why flows might be confined to PPM or extend outside it; do not make significance the success condition. |
| *Solving the Swedish Muni Puzzle*, 2017, ID 3519 | Uses the Swedish setting to reduce familiar credit and tax differences and studies maturity-matched municipal/Treasury bonds. | The setting removes rival explanations and focuses attention on liquidity. For FTN, the most valuable contrast is between investors subject to PPM transfers and investors outside that system. Remaining alternative channels still require discussion. |
| *Fund Flow Risk and Cross-Sectional Asset Prices*, 2015, ID 2552 | Puts competing flow-related mechanisms into hypotheses with distinguishable predictions. | A mechanism is something evidence can discriminate between. For FTN, announcement-period outside flows and implementation-period PPM flows imply different interpretations. |
| [Chasing Your Own Tail, 2020](../../old_winners/2020_per_hiller_chasing_your_own_tail.pdf), ID 4696 | Connects leveraged-ETF rebalancing to intraday timing and market conditions. | The observation frequency is chosen for the predicted mechanism. Monthly FTN data cannot identify a reaction within hours or disentangle events only days apart. |
| [Predicting Liquidity in the Cryptocurrency Market, 2022](../../old_winners/2022_per_hiller_predicting_liquidity_in_cryptocurrency_market.pdf), ID 5326 | Tests implications of a liquidity/invariance framework in a market with different trading arrangements. | A new asset class is useful when it tests a proposition. FTN should similarly test the reach of public selection, not merely document a new agency. |
| *The Drivers of Wealth Inequality*, 2023, ID 5727 | Extends a model with economically motivated heterogeneity and examines counterfactuals. | There is no universal winning estimator. The method serves the question. Adding a DiD label or extra controls to FTN does not create identification. |

For all source filenames and archive links, see the [award index](../../old_winners/INDEX.md). The interpretations in the last column are mine, not statements from the award juries.

**Direct comparisons are more useful than treating every other thesis as weak**

*The Rise and Fall of the Pre-FOMC Announcement Drift* (2019, [ID 4441](../../non_winners/text/4441.txt)) also has a recognizable published anchor, an updated sample and an anomaly that fades. Those features alone therefore do not explain an award. Compared with the awarded FOMC-cycle thesis, the useful distinction in the passages reviewed is how extensively the empirical work investigates the proposed explanation, rather than leaving market learning principally as interpretation. The papers study related but different anomalies, so this is not a controlled matched comparison.

*Do Active Fund Managers Outperform Their Peers?* (2022, [ID 5277](../../non_winners/text/5277.txt)) contains useful active-share analysis and acknowledges the difficulty of making a causal claim about disclosure rules. It also pursues several questions and extensions. The lesson for the current FTN plan is to resist accumulating fees, survival, performance, supply, flows and welfare as parallel theses. Breadth is costly when the central mechanism needs careful measurement.

*Unpacking Performance* (2024, [ID 6043](../../non_winners/text/6043.txt)) provides another relevant Swedish fund comparison. A local market’s size, participation rate or institutional distinctiveness can motivate interest, but those facts must be translated into a testable prediction. Comparing alpha and manager value added also requires clarity that these are different economic objects. FTN needs the same discipline: outside asset growth, estimated outside flow, observed trading, fee savings and welfare are not interchangeable outcomes.

There are strong counterexamples to any sharp winner/non-winner dichotomy. *Unraveling the Impact of the Riksbank* (2023, [ID 5880](../../non_winners/text/5880.txt)) uses policy surprises and investigates heterogeneous effects. The Norwegian quota thesis (2014, [ID 2324](../../non_winners/text/2324.txt)) examines compliance strategies and performance. The comparison collection contains serious mechanisms and methods too. We cannot infer that absence from the prize list means superficial analysis.

The defensible conclusion is that **a coherent, discriminating research argument is a strong standard to emulate**. It is not a necessary-and-sufficient prize formula. Topic appeal, execution, cohort competition, eligibility and judgment can all influence awards, and those factors are incompletely observed here.

**What to copy into your research process**

1. State one question whose answer matters under either sign and under a precisely estimated small effect.
2. Identify what changes relative to the anchor: institution, mechanism, treatment, information or economic constraint.
3. Define the counterfactual and the limits of identification before estimating results.
4. Make the data frequency and unit of observation match the proposed mechanism.
5. Give each main exhibit a purpose: sample validity, baseline response, channel distinction, or a serious alternative explanation.
6. Explain magnitudes and uncertainty in economically interpretable units. A null with wide bounds is not evidence of no effect.
7. Keep replication and extension visibly connected. An unrelated second question weakens the contribution.

For FTN, a compact exhibit plan would cover the institutional timeline and sample; pre-award comparability; selection-associated PPM and outside responses; announcement-versus-implementation timing; and sensitivity to measurement, controls and procurement cohorts. Combine or split exhibits as necessary. This is a proposed narrative, not a rule about exactly how many tables win.

**Riccardo Sabbatucci: verified professional facts**

Sabbatucci is an Associate Professor of Finance at SSE and joined after his UC San Diego doctorate in 2016. [Official SHoF profile](https://www.houseoffinance.se/about/people/people-container/riccardo-sabbatucci/).

His research list includes *Cash Flow News and Stock Price Dynamics* (JF, 2020), *Geographic Lead-Lag Effects* (RFS, 2020), and *Tradable Risk Factors for Institutional and Retail Investors* (Review of Finance, 2025). The current retirement-menu working paper is titled **“Shifting From Active to Passive: How Retirement Plans Impact Equity Prices”**, with Andrea Tamoni and Song Xiao, dated April 2026. It studies retirement-plan reallocations and equity prices. It is listed as a working paper, not a published anchor. [Author’s current research page](https://sites.google.com/site/riccardosabbatucci/Research).

This is a particularly relevant neighboring research interest for FTN. Your contribution should remain distinct: selection-associated demand outside PPM, rather than pension reallocations’ stock-price impact. Cite his paper only where that intellectual connection is useful. His authorship does not make it the best main anchor or override the published-paper requirement.

**What this implies for how to present the thesis**

The strongest evidence about his expectations is the course material he supplies, not a guessed personality profile. The [original introduction](../../course_context/source_materials/Introduction_to_research_in_finance_Fall_2026_RS.pdf) emphasizes feasibility, correctness, relevance, independence, economic mechanisms and meaningful extension. It discourages statistical-significance hunting. The stated main-text limit is 40 pages, with concise writing and self-contained exhibits; older awarded theses do not override it.

My inference from his research interests is that he is likely to recognize the difference between an administrative reallocation and a voluntary demand response, and between a financial quantity as labelled and as actually measured. This is an inference, not a private grading rule. Prepare especially clear answers to:

- What precisely moves at announcement, and what moves at implementation?
- Why should the comparison funds represent a credible counterfactual?
- Whose capital is in the outside-PPM measure?
- Are the flow inputs observed transactions or estimates from asset changes?
- Can selection, fees, marketing or fund scale explain the result?
- How much information comes from independent procurement events, rather than repeated monthly observations?
- What can a small or imprecisely estimated effect establish?

Several recent awarded theses identify **Adrien d’Avernas**, rather than Sabbatucci, as examiner on their front pages. The prize collection therefore cannot be treated as a revealed-preference dataset for Sabbatucci. Your safest response to the examiner research is methodological clarity and compliance with his current written assignment, not imitation or flattery.
