> Reference evidence (1 October 2026). Sections 1-3 and the appendices remain valid. **Section 4 predates the anchor decision**: its design advice (DiD around award dates, staggered adoption) belongs to the dropped designs. For the current design, use `PLAN.md`.

# Winners versus non-winners: what separates the 25 awarded SSE finance theses from the other 635

Prepared 1 October 2026 from the full text of all 660 bachelor theses in finance in the SSE library catalogue (2009 to 2026): the 25 in the official awarded collection (`old_winners/`) and the 635 that are not (`non_winners/`). Two layers of evidence are used. Layer 1 is a set of structural metrics computed by script over every thesis (`metrics_all.csv`, produced by `../thesis_metrics.py`). Layer 2 is a close reading against a fixed rubric of all 25 winners and a stratified sample of 33 non-winners, 4 per year for 2018 to 2024, 4 from 2025 to 2026, plus 6338, which the catalogue flags as awarded in 2026 but which is not yet in the official collection.

Read the numbers with two caveats. There are only 25 winners, 13 of them from 2018 onward, so most differences cannot reach statistical significance even when they are real. And the script metrics are heuristics on extracted text (reference lists are counted by block, introductions are located by heading), so they describe tendencies, not exact counts.

## 1. The short version

On the surface, winners look like everyone else. They are not longer, they do not cite more papers, they do not cite more top-journal papers (if anything slightly fewer), they do not have more tables, and they are not more often Swedish. Nothing you can count on the page separates a winner from the median thesis.

What separates them is how the thesis is built:

1. One explicit research question, usually a single sentence set off in the introduction (recent winners 69%, recent non-winners 39%).
2. A named anchor paper whose design is transplanted and then compared to, number by number, rather than a paper borrowed for its variable list. Winners use "we follow", "replicate", "akin to" about twice as often, and the difference is significant for 2018 to 2024.
3. A credible source of identification. Six of the 25 winners exploit a reform, a regulatory threshold or an institutional quirk with a treatment and a control group. Zero of the 33 non-winners read have one; every "event" in the sample is a calendar dummy or a before/after split.
4. One headline result plus robustness, instead of a fan of hypotheses. Winners have formal numbered hypotheses in 20% of cases, non-winners in 34%, and the non-winner sample routinely multiplies two or three hypotheses into dozens or hundreds of reported tests.
5. Null results treated as findings and explained by the institutional setting. Non-winners report nulls honestly most of the time but then soften them ("tendencies" at p = 0.7, "significant at the 20% level") or let the conclusion contradict the tables.
6. Short, targeted literature sections and an introduction that carries the argument, with results previewed in numbers. Non-winners put 2,000 to 4,000 words of textbook exposition (EMH, CAPM to FF5, what a spin-off is) where the argument should be.
7. Clean inference and clean references. The recurring technical faults in the non-winner sample are iid t-tests on overlapping event windows, look-ahead bias in portfolio formation, unclustered standard errors on country-level regressors, outlier-dependent significance, and reference lists that omit the paper being replicated.

None of this is about ambition or polish. Several winners found nothing (2011 quota DiD, 2023 FOMC cycle, 2024 French quota), and several have real flaws. They won because the question was clear, the design could answer it, and the write-up said what was found.

## 2. Layer 1: what the script can and cannot see

Medians, winners (W) versus non-winners (N). "All" is 2009 to 2026 (25 vs 635). "Recent" is 2018 to 2024, the years with winners (13 vs 305). "Current" is the 2025 to 2026 non-winner cohort (99), which has no winners yet. p-values are Mann-Whitney (counts) or Fisher exact (rates).

### Things that do not differ

| Metric | W all | N all | p | W recent | N recent | p | N current |
|---|---:|---:|---:|---:|---:|---:|---:|
| Words (full text) | 13,446 | 13,024 | 0.24 | 12,601 | 12,716 | 0.99 | 12,741 |
| Pages | 44 | 40 | 0.42 | 38 | 39 | 0.76 | 37 |
| Reference-list entries | 25 | 30 | 0.77 | 25 | 30 | 0.40 | 25 |
| Top-journal references | 7 | 8 | 0.11 | 6 | 8 | 0.08 | 10 |
| Working papers cited | 1 | 1 | 0.93 | 1 | 1 | 0.93 | 1 |
| Web sources cited | 6 | 7 | 0.60 | 7 | 11 | 0.65 | 8 |
| Highest table number | 6 | 7 | 0.70 | 5 | 6 | 0.24 | 7 |
| Swedish-setting words (Sweden, Swedish, Stockholm, OMX, SEK) | 15 | 9 | 0.82 | 22 | 7 | 0.45 | 4 |
| Share with Swedish setting (20+ such words) | 48% | 45% | 0.84 | 54% | 43% | 0.57 | 36% |
| Share with DiD / IV / RD vocabulary | 40% | 37% | 0.83 | 38% | 36% | 1.00 | 32% |
| Share with an event-study design | 16% | 16% | 1.00 | 15% | 12% | 0.67 | 20% |
| "Robustness" mentions | 3 | 3 | 0.88 | 3 | 2 | 0.69 | 5 |
| Null-result language | 5 | 5 | 0.36 | 4 | 5 | 0.30 | 9 |

Two things are worth pausing on. Winners cite slightly fewer top-journal papers, not more, so "pad the reference list with JF and JFE" is not the lesson. And the share using DiD, IV or RD words is the same in both groups; what differs, as the close reading shows, is whether the words correspond to a real treatment and control.

### Things that do differ

| Metric | W all | N all | p | W recent | N recent | p | N current |
|---|---:|---:|---:|---:|---:|---:|---:|
| Explicit question in the introduction (a "?" sentence or "research question") | 44% | 40% | 0.68 | **69%** | 39% | **0.04** | 59% |
| Anchor language ("we follow", "replicat", "akin to", "methodology of") per thesis | 2 | 1 | 0.09 | **4** | 2 | **0.04** | 2 |
| Share with 2+ anchor phrases | 60% | 46% | 0.22 | **85%** | 53% | **0.04** | 66% |
| Contribution phrases ("to our knowledge", "we contribute") | 1 | 0 | **0.01** | 1 | 0 | 0.08 | 1 |
| Results previewed in the introduction ("we find") | 56% | 36% | 0.06 | 46% | 34% | 0.38 | 42% |
| Introduction length (words) | 1,046 | 849 | 0.15 | 1,082 | 872 | 0.17 | 977 |
| Any formally numbered hypotheses (H1, H2...) | 20% | 34% | 0.20 | 15% | 37% | 0.15 | 21% |
| Three or more numbered hypotheses | 8% | 18% | 0.29 | 8% | 20% | 0.48 | 13% |
| Policy / reform vocabulary (5+ mentions) | 32% | 18% | 0.11 | 31% | 18% | 0.27 | 17% |
| Figures (highest figure number) | 4 | 2 | **0.01** | 3 | 2 | 0.66 | 3 |

The pattern is consistent even where individual p-values are not small: winners state a question, name the paper they build on, say what they add, preview the result, and do not fan out into numbered hypotheses.

### The current cohort (2025 to 2026)

The 99 most recent non-winners show where the format is going, and most of it matches the current course rules: tables of contents have all but vanished (4% versus 29% in 2018 to 2024), top-journal density is up (37% of these theses have at least half their references in top journals, against 21% before), "robustness" and null-result language are both more frequent, and an AI-use appendix is standard (six of the eight 2024 to 2026 theses read have one, all of the formulaic "grammar, R debugging, LaTeX" kind). Explicit research questions are more common too (59%). In other words, the surface conventions of the winners have spread; the design problems in section 3 have not gone away.

## 3. Layer 2: what the close reading adds

### 3.1 The question

Winners: a single question, often italicised or set off, in the introduction. "Are board gender quotas unfavorable for firm value?" "Can liquidity premiums explain the Swedish Muni Puzzle?" "Does the pattern of higher US excess stock returns in even weeks of the FOMC cycle persist after 2016?" Of the 25, about 18 state a verbatim question and the rest state a single aim; the 2013 rumours thesis, with four hypotheses, is the one that sprawls.

Non-winners: about 10 of the 33 pose one crisp question. The rest have none (5888, 5713, 6003, 6052), a list of aims (6013), five numbered questions (6365), or one umbrella question that fans out into four or five hypotheses (4554, 4897, 5314). Vague questions and multiplied hypotheses go together: 6365 reports several hundred cumulative abnormal returns; 4455 reports about 60 alphas; 6338 has roughly 150 coefficients on its key variable across 44 tables.

### 3.2 The anchor paper

Winners: 24 of 25 name one or two published papers whose design they transplant, say so bluntly ("the methodology is a replication of Baek et al (2004)", "we follow as closely as possible the methodology and data sources of Cieslak et al. (2019)"), and compare their numbers to the anchor's ("their 3.56% vs our 0.83%", "0.20% compared to Baek's 0.28%"). The anchors are in JF, JFE, QJE, RoF, JME, Econometrica, or, for the microstructure theses, the tutor's own working papers.

Non-winners: about two thirds of the sample name an anchor, which is not far below the winners. The difference is in what the anchor is for. In the sample it is often a lower-tier journal or working paper (Boulton et al. in JIBS, Nofsinger and Varma in JBF, Salaber unpublished, Adams et al. in a management journal, Tunaru et al. in Review of Financial Economics), or a practitioner book (O'Shaughnessy's *What Works on Wall Street*). And it is used for the variable list or the data cleaning rather than the design: Lowry et al. supplies sample filters for 5888, Chambers and Dimson supplies a regression that 6013 then strips of nine of its regressors, Butler et al. supplies control variables for 4554, Beck et al. supplies an econometric template for an unrelated question in 4130. One thesis (5314) cites its anchor, discards its method as "a flaw", and omits it from the reference list.

The theses in the sample that stay inside the anchor's design (6812 with Parise and Rubin 2025 JF, 6208 with Yung, Colak and Wang 2008 JFE, 4694 with Campbell et al. 2008 JF, 4670 with Reeb et al. 2001 JFQA) are the ones that read most like winners. Where they go wrong is in the add-on: an untested trading strategy bolted onto an anchored logit (6581), subsample mining after an anchored null (6365), a "loss aversion" split that is mechanically related to the sorting variable (4994).

### 3.3 Identification

This is the sharpest difference. Six winners exploit a reform or a regulatory discontinuity with a dated event, a named control group and a pre-trend check: the Norwegian quota with Swedish firms as control (2011), crisis short-sale bans across ten countries (2011), the OMXS30 tick-size threshold with a regression discontinuity (2012), the French transaction tax with Eurozone controls (2013), Norwegian parking fees for electric cars (2018), the French quota with Ahern and Dittmar's instrument (2024). A seventh (2017 muni) uses an institutional quirk (KommunInvest and Riksgälden have identical credit risk and tax treatment) to remove the usual confounders.

None of the 33 non-winners has exogenous variation. The only one that uses DiD vocabulary (4130) applies it to self-selected treatment with a 13-firm control group and a parallel-trends plot for one firm; its own placebo falsifies the claim. Everything else is pooled OLS, a cross-sectional logit, portfolio sorts, matched pairs with a Wilcoxon test, or an event study. Covid, Brexit, the STOCK Act, the EU Taxonomy, SFDR, ETS phases and crises all appear, and in every case as a calendar dummy, a before/after split or a sample definition, so the headline effect is indistinguishable from a period effect (5201's "work-from-home effect" on insider returns is a 16-month dummy over the post-crash rebound; 6208's hot-market comparison has the 2022 bear market inside its holding window).

### 3.4 Results and how nulls are handled

Winners: nulls are the finding. The 2011 quota thesis found no effect in its DiD and listed six candidate explanations. The 2023 FOMC thesis found the anomaly had vanished and explained why. *The Smooth Transition* found nothing on every outcome and attributed it to France's six-year phase-in and softer sanctions. The 2011 short-sale thesis concluded its own effects were probably endogenous and still won. Winners are not spotless: the 2019 value-premium thesis calls t = 1.47 "significant" and the 2012 tick-size thesis draws a policy conclusion from p between 0.05 and 0.08. But the general pattern is to state the result and explain it.

Non-winners: nulls and wrong-signed results are more common than positive ones (4088, 4440, 5232, 5888, 6013 null; 4251, 4451, 4455, 5201 contrary to hypothesis), and are usually reported, then softened. Odds ratios with p = 0.74 and 0.98 are "tendencies supporting the glass cliff" (4088). Coefficients are "significant at the 20% level" (5232). A null is "confirmation of our prediction" of a null (5888). Sign consistency of insignificant coefficients makes a result "robust" (4130). A conclusion asserts causal effects of IFRS and a spinning ban that were never tested (6013). Positive results are over-claimed in the other direction: a 20%-a-year alpha from 25 microcaps with no cost or liquidity check becomes evidence of "investor biases" (5885); one football player valued within 8% of Transfermarkt becomes "a significant finding" (5713); 43% from a backtest with no costs and no test "challenges the strong EMH" (6581).

### 3.5 Technical faults a referee would stop on

These recur in the non-winner sample and are almost absent from the winners:

- Look-ahead bias: a 2019 ESG score used to sort portfolios from 2004 (4251); 2018 SRI labels applied to 2000 to 2016 (4455); a static country classification over 19 years (4110).
- Survivorship bias acknowledged and left alone (4455, 5232, 6372).
- Inference: iid t-tests on overlapping 255-day windows with hundreds of subsamples and no multiple-testing correction (6365); t-statistics of 5 to 14 from cross-sectional tests on calendar-clustered repurchase events (6372); degrees of freedom taken from trading days instead of the 28 events (4609); country-level regressors on 18 countries with unclustered firm-level standard errors (4131); 23 clusters with stars that do not match the standard errors (6338).
- Mismeasured outcomes: "underpricing" defined as close over open, giving a mean of minus 0.6% that is rationalised instead of questioned (4554); issue price relative to par when the coupon is reset to par by construction (4440); a "return" that is a mechanical transform of the portfolio weight (6338).
- Tautological tests: reclassifying R&D-heavy firms out of the top quintile mechanically raises its bankruptcy share, then a McNemar test on 141,000 observations "confirms" it (4912); an index that correlates 0.994 with its own inputs (5889).
- Fragile headlines: significance that exists only after dropping one outlier, sold as SEK 82 million "left on the table" (4451).

### 3.6 Writing and structure

Winners: introductions of 900 to 1,800 words (two to four pages) that motivate, state the question, name the method, preview the results with numbers, and state the contribution, often as a numbered "threefold" list. Literature sections of 450 to 1,300 words that name the two or three closest papers and the difference. The exceptions (the 2017 muni thesis with a 5,000-word review and a philosophy-of-science section) are the older ones.

Non-winners: introductions are often as long, but the literature and theory sections balloon into textbook exposition. 2,000 to 4,000 words on the history from CAPM to FF5 (4110, 4251, 4455, 5885), EMH primers (4251, 4609, 5202), a bond-pricing primer (4440), 2,500 words on logit, likelihood-ratio tests, ROC curves and permutation tests (6581), formulas for Sharpe, skewness and kurtosis (6052). Bodie-Kane-Marcus, Berk-DeMarzo, Newbold and Wooldridge are cited as sources of method. Only seven of the 33 preview results with numbers in the introduction. Results tables are images that did not survive text extraction in at least four (4994, 5202, 5888, 6013, 6365), which is a sign they were pasted from statistical output.

### 3.7 Data

Winners get data from institutions and say so in the introduction: broker-dealer balance sheets from Statistics Sweden, fund annual reports collected by hand, KommunInvest bond data, OFVAS car registrations, Nasdaq tick data via SHoF, English et al.'s own bank sample. Non-winners mostly pull from a terminal (Eikon, Datastream, SDC, Capital IQ, Morningstar Direct), scrape (Sofascore, Transfermarkt, football-data.co.uk, Excel's STOCKHISTORY), inherit a dataset from another bachelor thesis (4088), or build a classification from a blog and a commodity website (6052). Hand-collection appears in a minority (4451 prospectuses, 5889 CDP questionnaires, 6013 Companies House) and helps those theses.

### 3.8 Reference hygiene

Winners' lists are short (median 25) and clean. In the non-winner sample: an anchor cited in the text but absent from the list (5314, three papers); anchor authors misspelled throughout ("Lowery" for Lowry, "Young" for Yung, "Alon Bravan" for Gompers and Brav); 104 entries of which 40 are web pages (6003); listed papers never cited (5885); Investopedia, Forbes, CNN, LinkedIn and blogs as sources.

### 3.9 The one flagged for 2026 (6338, *Leading the Wallet*)

It has the ingredients the winners share: a JFE anchor (Guiso and Zaccaria 2023) extended with a written-out model, 135,000 harmonised households across 23 countries, a cross-country norms dimension, a full alternative-measure robustness section, and journal-style presentation. It also has the non-winner weaknesses at scale: three broad questions, no exogenous variation, a model whose own prediction the data reject, a mechanical return measure, and about 150 coefficients across 44 tables with signs that flip when country fixed effects are swapped for a dummy. If it does win, it will be for scope and execution rather than for a single credible result; it is the mirror image of 6812 (*Green Window Dressing*), which has one question, one JF anchor with replication code, bootstrapped double-clustered standard errors and an honest but low-powered null.

## 4. What this means for a thesis on Fondtorgsnämnden

> Superseded on design (see note at top). Points 1, 2, 4, 5, 6 (clustering, no iid tests on overlapping windows), 8 and 9 still apply. Point 3 (DiD around award dates as the centrepiece) does not: the current design is a transplant of SSZ Table III with FTN as one bounded column.

The procurement of the premium pension platform gives you the one thing that none of the 33 non-winners had and six of the winners built on: a dated treatment with a named control group. Build the thesis around it.

1. One question, one sentence, set off in the introduction. Every other test is a sub-test of it or a robustness check.
2. One top-journal anchor used for the design, not the variable list. Write out the deviations and compare your coefficients to the anchor's.
3. Make identification the centrepiece: award dates, winners against losing bidders and not-yet-procured categories, pre-trend plot, placebo on untreated categories, staggered-adoption estimator (Callaway and Sant'Anna) since categories were procured at different times. "Robustness" means threats to identification, not VIF and Durbin-Watson.
4. One headline table. Fix the outcomes before you see the data and resist adding splits after.
5. If the result is null, say so in the first paragraph and explain it with the institutional detail (short post-period, index versus active categories, size of the default inflow relative to AUM), with a power calculation so the reader knows what you could have detected.
6. Inference: cluster by fund and by category-month; use calendar-time portfolios for performance; never run iid t-tests on overlapping windows.
7. Data from institutions, named in the introduction: Pensionsmyndigheten, Fondtorgsnämnden award decisions, Morningstar via SHoF.
8. Introduction of two to four pages that previews the numbers; related literature under a page naming the two or three closest papers; no textbook exposition of OLS, DiD or CAPM; no table of contents; an AI-use appendix.
9. Twenty to thirty references, ten or more in top journals, every cited work in the list, authors spelled correctly, no Investopedia.

## Appendix A. Winners read against the rubric

| Year | Thesis | Anchor (journal) | Question | Design | Setting | Result |
|---|---|---|---|---|---|---|
| 2011 | Gender quotas, Norway | Ahern & Dittmar (then WP, later QJE) | One | DiD Norway vs Sweden + event study | Nordic reform | DiD null, explained |
| 2011 | Short-sale bans and options | Grundy et al.; Battalio & Schultz; Beber & Pagano (WPs, later JFE/JF) | Two | FE panel, staggered bans, 10 countries | Policy event | Significant; authors conclude likely endogenous |
| 2012 | Tick sizes and volatility | Hau (JEEA); Bessembinder (JFI); Imbens & Lemieux (J Econometrics) | One | Sharp RDD at 100 SEK threshold | Swedish regulatory threshold | Weak (p 0.05 to 0.08) |
| 2013 | Takeover rumours | Pound & Zeckhauser (J. Business); Dietrich & Sorensen; MacKinlay | Title question + four hypotheses | Event study, cross-section, logit with out-of-sample validation, matching | US, hand-screened Zephyr rumours | True rumours +4.95pp; trading strategies null, as predicted |
| 2013 | French transaction tax | Jones & Seguin (AER); Liu & Zhu | One (three experiments) | DiD with Eurozone controls | Policy event | Volume/volatility effects; STT null |
| 2014 | Religious frictions, sukuk | Chen, Lesmond & Wei (JF); Diebold & Li | Two hypotheses | Yield curves + pooled OLS | Malaysia | Spread significant, liquidity channel weak |
| 2015 | Fund-flow risk | Fama-MacBeth; Warther (JFE); Falkenstein (JF) | One | Two-pass regressions, sorts | US | New factor, significant |
| 2015 | Commodities diversification | Tang & Xiong (FAJ); Huberman-Kandel | One | Mean-variance, spanning tests | US indices | Mixed |
| 2016 | Intermediary asset pricing | Adrian, Etula & Muir (JF); He, Kelly & Manela (later JFE) | One aim | Two-pass FM on Swedish portfolios | Swedish, hand-collected SCB data | Largely insignificant, framed as benchmark failure |
| 2016 | Policy uncertainty and CDS | Wisniewski & Lambe (SSRN); Longstaff et al. | Two | Firm FE panel | US | Significant |
| 2017 | Swedish muni puzzle | Goldreich, Hanke & Nath (RoF) | One | Panel FGLS on matched bond pairs | Swedish institutional quirk | Significant |
| 2017 | Unbundled fund costs | Dahlquist et al. (JFQA) tradition; Carhart | Seven hypotheses | RE/FE panel on hand-collected annual reports | Swedish, hand-collected | Core null, "suggestive" interaction |
| 2018 | EV adoption and free parking | Berry (RAND); BLP (Econometrica); Li et al. | One | Nested logit with IV, policy dummy | Norwegian reform | Significant in preferred spec |
| 2018 | Intergroup bias, venture funding | Brooks et al. (PNAS); Gino et al. | Three hypotheses | Survey experiment, Mann-Whitney | Swedish investors | Partly null |
| 2019 | Filing lag and Tobin's q | Lindenberg & Ross tradition | One | Pooled OLS with industry/year FE | US | Significant |
| 2019 | Swedish value premium | Petkova & Zhang (JFE) | Two | Conditional CAPM replication | Swedish factors | Weak, over-read |
| 2020 | Leveraged ETFs | Tuzun (Fed WP); Kyle & Obizhaeva (Econometrica + WP) | One | Stock-day OLS on rebalancing flow, date-clustered; anticipatory split | Swedish OMXS30, single issuer, SHoF minute data | Significant but thin (R² 0.02); reversal tests null |
| 2020 | Bank returns and policy surprises | English, Van den Heuvel & Zakrajšek (JME) | Two | FOMC-day event regressions, same bank sample | US | Sign flips pre/post crisis |
| 2021 | Covid press conferences | Busse & Green (JFE) | Two | Intraday event study, t-tests, OLS | Swedish | Mixed, signs opposite to anchor |
| 2021 | Microstructure invariance | Kyle & Obizhaeva (Econometrica + WPs) | One main | Log-log OLS, slope = 1 test | Swedish tick data | Confirms aggregate, rejects by year |
| 2022 | Crypto liquidity | Kyle & Obizhaeva (WPs) | One | Log-log OLS | Kraken | Rejected statistically, "economically close" |
| 2022 | Ownership and Covid returns | Baek, Kang & Park (JFE) | Aim | Cross-sectional OLS | Swedish crash | Concentration significant, identity null |
| 2023 | FOMC cycle | Cieslak, Morse & Vissing-Jorgensen (JF) | One | Out-of-sample replication | US | Null is the finding |
| 2023 | Wealth inequality | Gabaix et al. (Econometrica) | Aim | Structural model, calibrated to Swedish data | Swedish | Counterfactuals |
| 2024 | French board quota | Ahern & Dittmar (QJE) | One | Event study + IV panel | French reform | Null on every outcome, explained |

## Appendix B. The 33 non-winners read against the rubric

| Id | Year | Thesis | Anchor | Question | Design | Biggest weakness |
|---|---|---|---|---|---|---|
| 4131 | 2018 | Institutions and IPO underpricing | Boulton et al. (JIBS); Engelen & van Essen (JBF) | Two hypotheses, 16 regressors singly | Pooled OLS, 18 countries, unclustered | Country regressors with firm-level SEs; internally inconsistent |
| 4110 | 2018 | Sin stocks and investor traits | Salaber (WP); Hong & Kacperczyk (JFE) | Three hypotheses | FF5 on country-group portfolios | 4 of 5 long-short alphas insignificant, concluded as support |
| 4088 | 2018 | Glass cliff in Sweden | Adams et al. (BJM) | One | Logit of CEO gender on CAR, 25 treated | p = 0.7 narrated as tendencies; no finance anchor |
| 4130 | 2018 | Exclusions and dialogues, emissions | Beck et al. (JF) as template only | Two | "DiD" on self-selected treatment | No design; placebo falsifies own claim |
| 4440 | 2019 | Green bond issue prices | Gabbi & Sironi (EJF) | One | 20 matched pairs, Wilcoxon | Outcome cannot measure the premium; n = 20 |
| 4451 | 2019 | Banking relationships and IPOs | Schenone (JF) | One, three hypotheses | Cross-sectional OLS | Significance exists only after dropping one outlier, sold as SEK 82m |
| 4251 | 2019 | ESG portfolios | None | Several | FF5 + UMD sorts, trading rules | Look-ahead bias; all portfolios have positive alpha |
| 4455 | 2019 | Swedish SRI funds in crises | Nofsinger & Varma (JBF) | Three hypotheses, ~60 alphas | Matched-fund portfolios with crisis dummies | Survivorship and label look-ahead; 2 of 3 hypotheses rejected, tone promotional |
| 4609 | 2020 | Swedish spin-offs | Cusatis et al. (JFE) | Two, 10 sub-tests | Market-adjusted event study, 28 events | Degrees of freedom from trading days; results partly withheld |
| 4554 | 2020 | Governance and IPO underpricing | Butler et al. (JCF) for controls | Four hypotheses | Cross-sectional OLS, n = 115 | DV is close/open; mean underpricing minus 0.6% rationalised |
| 4670 | 2020 | Internationalisation and debt cost | Reeb, Mansi & Allee (JFQA), explicit replication | Two | Pooled OLS, ordered logit, firm FE | Defective dataset; honest FE null under-exploited |
| 4694 | 2020 | Distress anomaly | Campbell et al. (JF); Gao et al. (RFS) | One | Decile sorts, FF5 alphas | Thin increment; 20 to 30% alphas not stress-tested |
| 4912 | 2021 | R&D and bankruptcy prediction | Franzen et al. (JF) | One, two hypotheses | Quintile sorts, McNemar, logit | Near-tautological tests; no out-of-sample |
| 4897 | 2021 | VC vs PE and IPO underpricing | Barry et al. (JFE) | One, five hypotheses | t-tests, univariate OLS | Broken econometrics; null over-read |
| 4998 | 2021 | CSR and Covid returns, Sweden | Lins, Servaes & Tamayo (JF) | Vague | Cross-section n = 162, panel | Home-made CSR index; unfalsifiable cultural story |
| 4994 | 2021 | Contrast effects | Hartzmark & Shue (JF), explicit replication | Aim | Anchored OLS + splits | Mechanism tests over-claimed; tables are images |
| 5202 | 2022 | EU Taxonomy announcements | None (textbook event study) | One, 5 samples x 3 events x 6 windows | Event study on 3 shared dates | No identification; window fishing; conclusion contradicts signs |
| 5232 | 2022 | Passive share and active performance | Grossman & Stiglitz (theory only) | One | Bivariate OLS on 11 annual values | Design cannot learn anything; 20% significance |
| 5201 | 2022 | Insider trading under WFH | Cohen, Malloy & Pomorski (JF) | Two-part | Trade-level OLS with 16-month dummy | Period effect indistinguishable from "WFH effect" |
| 5314 | 2022 | IPOs and listed peers | Hsu, Reed & Rocholl (JF), discarded | Two, four hypotheses | Raw returns vs index, Welch tests | Non-independent observations; anchor missing from reference list |
| 5889 | 2023 | Social profitability index | Oehmke & Opp (WP) | One (design question) | Index construction, n = 24 | Nothing tested; H1 true by construction |
| 5888 | 2023 | IPO underpricing in crises | Lowry et al. (JF) for data cleaning | None | Monthly OLS on crisis dummies | No question; lone positive rests on six months |
| 5713 | 2023 | Option pricing of footballers | Tunaru et al. (RFE) | None | One-player valuation | No hypothesis, no test |
| 5885 | 2023 | Trending value in the Nordics | O'Shaughnessy (book); LSV (JF) | Two | Sorts + FF3, own factors | 20%+ alpha from 25 microcaps with no cost or liquidity check |
| 6013 | 2024 | IPO underpricing on the LSE | Chambers & Dimson (JF), 9 regressors dropped | List of aims | Cross-sectional OLS, Brexit split | Untested IFRS/spinning claims in conclusion |
| 6208 | 2024 | IPO underpricing in the Covid hot market | Yung, Colak & Wang (JFE); Carter & Manaster (JF) | Two | Distribution tests, OLS | Hot/non-hot split confounded by 2022 bear market |
| 6003 | 2024 | Sports betting as investment | Strumbelj (IJF); Kaunitz et al. (arXiv) | None | Backtests, simulated asset | Nothing falsifiable; 104 references, 40 web |
| 6052 | 2024 | Carbon credit betas | None | Several loose | Univariate betas, eyeballed group means | No anchor, no test, ad hoc classifications |
| 6365 | 2025 | Congressional stock trades | Ziobrowski et al. (JFQA) | Five questions | Event study, hundreds of CAARs | Multiple testing on overlapping windows |
| 6581 | 2025 | Oil futures overreactions | Jeon, McCurdy & Zhao (JFE) | Two loosely linked | Jump detection + logit; unanchored backtest | Two halves do not connect; wrong benchmark for win rate |
| 6372 | 2025 | Swedish share repurchases | Ikenberry et al. (JFE) | One, three hypotheses | Short- and long-run event study | Long-run t-stats from overlapping, clustered events |
| 6812 | 2026 | Green window dressing, EU | Parise & Rubin (JF), with replication code | One | Counterfactual return gap, bootstrapped double-clustered SEs | Low-powered null; closest to a winner in form |
| 6338 | 2025 | Female headship and portfolios (flagged 2026) | Guiso & Zaccaria (JFE) + model | Three broad | LPM/OLS with country and wave FE, 23 clusters | Scale without identification; model prediction rejected |

## Appendix C. Reproduction

- `metrics_all.csv`: one row per thesis (660), produced by `python3 ../thesis_metrics.py <text_dir> metrics_all.csv --index ../catalogue_index.json --winners ../../old_winners/INDEX.md` on the text files in `../text/` and `../../old_winners/text/`.
- `comparison.json`: the medians, rates and p-values in section 2.
- Text extraction: pdf.js text items re-flowed into lines with indentation, run inside the browser against the archive originals; identical for winners and non-winners. 1801 and 2258 (non-winners) and the 2013 and 2020 Per Hiller winners are OCR (Tesseract, 200 dpi).
- Close reading: all 25 winners and the 33 non-winners listed in Appendix B, each read in full against the same nine-point rubric by independent readers.
