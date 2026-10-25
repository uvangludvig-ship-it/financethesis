# The thesis in plain words

*Working title: Pre-announced, uninformed, and large: the price of moving the premium pension*

*Planning document, 25 October 2026, version 2.1. It replaces the 12 October version. For every part of the thesis it says what to write, what the prize winners did there, what the non-winners did that we must not do, and who writes it. No results exist yet; where a result of ours is mentioned, it is what we expect, not what we found. The thesis text is written by the two of us; this document is a map.*

*Sources for "what winners did" and "what losers did": the full text of all 660 bachelor theses in finance in the SSE catalogue 2009-2026, the 25 awarded ones read in full and a sample of 33 non-winners read against the same rubric (`research/reference/winners_vs_nonwinners_analysis.md`, `research/reference/conclusions_winners_vs_nonwinners.md`), and the five winners closest to our design read section by section (`outline/winners_structure.md`). The course rules are from Professor Sabbatucci's slides (`outline/requirements_checklist.md`).*

**Contents.** Part A: what the thesis is (question, anchor, what winners do). Part B: the three empirical parts, one card each. Part C: the thesis section by section, with what the winners did and what the losers did. Part D: the literature, strand by strand. Part E: the method in plain words and the harder maths. Part F: exhibits and data. Part G: outcomes, work plan, checklists.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part A. What the thesis is

## What the thesis is about

Since 2024 a new agency, Fondtorgsnämnden (FTN), decides by procurement which funds are allowed on the premium-pension platform. When a fund loses, Pensionsmyndigheten takes the savers' money out of it and puts it into a winner. Savers rarely act (about 94 per cent of the money moves without a choice), so the move is mechanical.

The money is large. Pensionsmyndigheten often owns 20 to 44 per cent of a losing fund. It does not take it out at once; it redeems in one to three chunks (tranches) of 5 to 11 per cent of the fund, spread over two or three weeks. To pay, the fund must sell stocks. So on dates known months in advance, for reasons that have nothing to do with the companies, specific Swedish stocks get sold in amounts that can reach tens of per cent of a normal day's trading.

The thesis asks three things:

- Do the prices of those stocks fall on the selling days, and bounce back afterwards?
- Does part of the move happen before the selling days, because traders see it coming?
- Who loses: the savers who are moved, or the investors who stay in the losing fund?

Then it puts a SEK figure on the cost of a round and sets it against what the round saves in fees (the agency's platform-wide figure is SEK 178m a year; cite the source document when writing).

The replication half measures the same thing on a flow the market has had years to learn: OMXSB index reconstitutions, following Greenwood and Sammon (2025).

**What the thesis does not do.** It does not judge whether FTN picks good funds. That needs years of returns after the awards and stays out of the hypotheses. Table 1 may describe what FTN chose (fee cut per round, winners' versus losers' trailing returns), labelled as descriptive.


## Why these flows are a clean experiment, and what is new

Three properties, each proven in section 2 of the thesis:

1. **Uninformed.** FTN selects on fees, quality and sustainability. Nothing in an award depends on the stocks a fund holds.
2. **Pre-announced.** The award is public months before the money moves; the saver letter gives a second public date.
3. **Large.** The redeemed share is 20 to 44 per cent of a fund; the dose per stock (forced sale over average daily volume) reaches tens of per cent in small caps.

New: nobody has measured FTN's executions. The flow has three dated steps (award, letter, tranche), which separates "the market positions early" from "the market absorbs on the day". No index reconstitution offers that, and none has a fund-level side (who paid).

This matches what the winners did with Swedish data: they chose a setting because an institutional feature removes a confound, not because the data were nearby. KommunInvest bonds share credit risk and tax status with treasuries (2017); XACT is the only LETF issuer, so its flows are known exactly (2020); Sweden unbundled research costs before MiFID II (2017). Thirteen of the 25 winners use Swedish or Norwegian data for a reason like that. In the 33 non-winners read, Covid, Brexit, the EU Taxonomy, SFDR and the crises all appear as calendar dummies or before/after splits, so the "effect" is indistinguishable from a period effect. Our treatment is a dated administrative act with a dose that varies across stocks within the same day.


## The anchor paper and how we copy it

**Greenwood and Sammon (2025), "The Disappearing Index Effect", Journal of Finance 80(2), 657-698.**

What they ask: why did the S&P 500 index effect vanish while index assets exploded? What they do: an event study of every S&P 500 addition and deletion 1980-2020 in three windows (announcement day, effective day, announcement to effective) by decade. Their numbers (NBER WP 30748, Table 2, per cent; the JF abstract revises slightly: additions 7.4 per cent in the 1990s, under 1 per cent in the last decade; deletions 0.1 per cent in 2010-2020. Check the published table before printing):

| Window | 1980s | 1990s | 2000s | 2010s |
| --- | --- | --- | --- | --- |
| Additions, announcement to effective | 3.42 | 7.59 | 5.21 | 0.80 |
| Additions, announcement day | 3.36 | 5.15 | 4.13 | 1.05 |
| Additions, effective day | 3.44 | 3.68 | 1.32 | 0.21 |
| Deletions, announcement to effective | -4.64 | -16.6 | -12.3 | -0.60 |

They test five explanations and keep two: index migrations from the MidCap (where passive money already held the stock), and a general rise in the market's capacity to supply liquidity on the day (other institutions now sell to the trackers). Increased predictability of additions "cannot be ruled out".

What we copy, and say so in one sentence in the method section: the three windows; market-adjusted returns as the main measure (a four-factor version is one robustness row); a table with additions and deletions in rows and sub-periods in columns with N per cell; a regression of the announcement-to-effective return on expected tracker demand scaled by average daily volume; a figure of tracker assets against the yearly effect.

Our version: OMXSB, about 100 stocks, reviewed twice a year; 394 events over 27 reviews, June 2013 to June 2026 (222 additions, 172 deletions; 325 read from Nasdaq's releases, 69 from newswires); tracker assets from about SEK 15bn to 120bn inside the sample; the announcement lead fell from 14-17 trading days to 6 from November 2023. Sub-periods: 2013-17, 2018-20, 2021-23, 2024-26.

What the replication can show: whether a small market with rising tracker demand shows the same disappearance. Either answer is a finding. If the Swedish effect did not disappear, that goes in the abstract, and we say which of their explanations does not apply here, using only what Table 2 shows.

Why this anchor for an FTN thesis: their open question is whether the effect died because markets got liquid in general or because arbitrageurs learned this one flow. FTN is the same kind of flow, in the same market and the same years, that nobody has learned yet. If the index effect is gone (Table 2) and the FTN effect is there (Table 3), general liquidity cannot be the whole story. That contrast is the sentence for the abstract.

How the winners used their anchors, which we imitate: the 2024 winner wrote "this paper employs a methodology akin to Ahern and Dittmar (2012)" on page 2 and quoted the anchor's 3.56 and 1.9 per cent next to its own numbers in the discussion; the 2020 winner put the anchor's specification in column 1 and its own in column 2 of the same table; the 2021 winner printed Kyle and Obizhaeva's fitted line beside its own. The comparison is a sentence in the text, not a column, and it comes before any extension. The non-winners also name anchors (two thirds of the 33), but use them for the variable list or the data cleaning rather than the design, or pick them from lower-tier journals, practitioner books, or working papers nobody cites; one discarded its anchor's method as "a flaw" and left the paper out of the reference list.


## What winners do and losers do not: the pattern in numbers

On the page, winners look like everyone else. Median length 13,446 words against 13,024; 25 references against 30; 7 top-journal references against 8; the same share with DiD, IV or RD vocabulary (40 against 37 per cent). Nothing you can count separates them. What does:

| | Winners (25) | Non-winners (635 or the 33 read) |
| --- | --- | --- |
| One explicit research question in the introduction (2018-24) | 69 % | 39 % |
| Two or more "we follow / replicate / akin to" phrases (2018-24) | 85 % | 53 % |
| Results previewed with numbers in the introduction | 56 % | 36 % |
| Formally numbered hypotheses (H1, H2, ...) | 20 % | 34 % |
| A reform, threshold or institutional quirk with treatment and control | 6 of 25 | 0 of 33 |
| Headline result with numbers in the conclusion | 48 % | 24 % |
| Mechanism or institutional explanation offered in the conclusion | 80 % | 58 % |
| Clear over-claiming in the conclusion | 16 % | 58 % |
| Policy implication directed at a regulator or a model (not investor advice) | most of 52 % | most of 48 % are investor advice |

Three winners are outright nulls (2011 quota, 2023 FOMC, 2024 French quota) and nine are mixed. Nulls win when the question was interesting before the data arrived.

The seven things a winner has: one question in one sentence; one top-journal anchor used for the design and benchmarked number by number; a credible source of identification; one headline result plus robustness instead of a fan of hypotheses; nulls treated as findings and explained by the institution; an introduction that carries the argument with numbers and a literature section under a page; clean inference and clean references.

The recurring faults a referee stops on in the non-winners, none of which may appear in ours: look-ahead bias (a 2019 ESG score sorting portfolios from 2004; 2018 labels applied to 2000-2016); survivorship bias acknowledged and left alone; iid t-tests on overlapping event windows with hundreds of subsamples and no multiple-testing correction; degrees of freedom taken from trading days instead of events; country-level regressors with unclustered firm-level standard errors; stars that do not match the standard errors; outcomes mismeasured by construction (underpricing as close over open); tautological tests; a headline that exists only after dropping one outlier; results tables pasted as images; 2,000 to 4,000 words of textbook (CAPM to FF5, the EMH, what a spin-off is, 2,500 words on logit and ROC curves); Bodie-Kane-Marcus and Wooldridge cited as sources of method; an anchor absent from the reference list; anchor authors misspelled throughout; 104 references of which 40 are web pages; Investopedia, Forbes, LinkedIn and blogs as sources.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part B. The three empirical parts

## Part 1 of the thesis: the OMXSB replication (Greenwood and Sammon on Swedish data)

| | |
| --- | --- |
| Question | Did the index effect on Nasdaq Stockholm's benchmark index shrink as tracker money grew, as it did in the US? |
| Hypothesis | H1. Additions earn positive and deletions negative abnormal returns from announcement to effective date; the effect scales with expected tracker demand over ADV; whether it fell over 2013-2026 is the sub-question. |
| Data | 394 OMXSB events 2013-2026 (done), daily prices and volume (Datastream, on disk, needs the long format), tracker assets by year (hand-built from fund reports), index levels (to pull). No FTN data. |
| Method | Market-adjusted returns in the anchor's three windows; equation (4): CAR on expected demand over ADV and sub-period dummies. Cluster by review date. |
| Exhibits | Table 2 (two panels), Figure 2. |
| Benchmark | The anchor's decade numbers: additions 3.4, 7.6, 5.2, 0.8 per cent; deletions -4.6, -16.6, -12.3, -0.6. Quoted in a sentence beside ours. |
| Expected | A small effect, weaker in recent sub-periods, with a volume spike on the effective day. If it did not fall, that is the abstract's first sentence. |
| Runs | Now. `code/replication_omxsb.py`. No unblinding needed. Gate 3, Sun 1 Nov. Owner: Alexander. |
| Role in the thesis | Proof of competence and the calibration for Part 2: what a learned flow does in this market. Two pages of results. |

## Part 2 of the thesis: FTN forced sales, price pressure and anticipation (the contribution)

| | |
| --- | --- |
| Question | When Pensionsmyndigheten redeems 5 to 11 per cent of a losing fund on a known day, do the fund's stocks fall, by how much per unit of forced sale, how much of the move comes before the day, and how fast does it reverse? |
| Hypotheses | H2. On tranche days abnormal returns fall in the forced net sale over ADV, with beta on the square-root prediction of order one, and reverse within 20 trading days. H3. Part of the move happens between award, letter and first tranche; the pattern separates predation, slow capital and sunshine trading. |
| Data | Tranche days and redeemed shares from daily fund units (done for about 30 losers; refresh in week 2; sale orders for the largest Swedish funds requested from Pensionsmyndigheten); fund holdings from FI (4 of 12 quarters, 13 zips to download); winners' monthly inflows (done); prices and volume (Datastream). |
| Method | The dose, equation (3), built before any price is seen. Equation (5): window CAR scaled by the stock's volatility on the dose, windows fixed in advance (award, anticipation, execution per tranche, reversal 2 to 20 and 21 to 60). Cluster by tranche day, wild-cluster bootstrap, randomisation within round, Kolari-Pynnönen. MDE printed before the result. |
| Exhibits | Table 3, Figure 3 (H2); Table 4 (H3). |
| Benchmarks | The square-root prediction (Y = 0.7); Da et al.'s 1.06 per cent on day 1 and full reversal within 15 days; the index-effect magnitude from Table 2 at equal dose. |
| Expected | Little in large caps (doses of 0.5 to 2 per cent of ADV are below the MDE); a visible drop and recovery in small caps; some early selling by the managers between letter and tranche. |
| Runs | Only after Klug's sign-off is dated in `03_DATA.md` E and `UNBLIND = True` is committed. Gate 4, Fri 6 Nov. Owner: Alexander. |
| Role in the thesis | The headline. Five pages of results, the abstract's numbers, the cost figure's input. |

## Part 3 of the thesis: who paid, and what it cost (incidence and cost-benefit)

| | |
| --- | --- |
| Question | Did the savers who were moved pay the impact cost, or the investors who stayed in the losing fund; and how many months of fee saving did a round's transition consume? |
| Hypothesis | H4. On tranche days, losing funds without swing pricing show NAV returns below benchmark by about c times r over (1 minus r); funds with swing pricing do not. Table 6 is arithmetic on H2 and H4. |
| Data | Fund NAV total return (Morningstar reinvested prices, on disk, opened only after unblinding), benchmark from the fund master, swing-pricing status (11 yes, 38 no, 29 unknown), redeemed share per tranche, the 2019 purge as a no-swing pooled sample (open decision). |
| Method | Equation (6): NAV minus benchmark on r over (1 minus r), split by swing status; the coefficient for funds without swing pricing is the realised dilution rate, compared with the stock-level cost applied to the fund's sold portfolio. Equation (8): cost per round, predicted (Y = 0.5 and 1) and realised, against the fee saving. |
| Exhibits | Table 5, Figure 4 (H4); Table 6 (cost-benefit). |
| Benchmarks | Jin et al.'s 33 bp swing adjustment; SEK 178m a year of fee saving. |
| Expected | A few basis points lost per tranche day in funds without swing pricing, none in funds with it; the worked example is SEB Sverige Expanderad against Öhman, Lannebo and Prior & Nilsson in January 2026. A round's price cost in months of fee saving. |
| Runs | After sign-off, `code/dilution.py`. Gate 5, Fri 13 Nov. Owner: Alexander. |
| Role in the thesis | The second result that stands on its own and the policy sentence (staggering, swing pricing, in-kind transfers). Three and a half pages of results. |

How the three parts talk to each other: Part 1 says what a learned flow does; Part 2 says what an unlearned flow of the same kind does in the same market; Part 3 says who carried the difference and what it was worth. The abstract's last sentence is the contrast between Part 1 and Part 2.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part C. The thesis section by section

## Section by section

Page budget 33 of 40; everything after the title page counts. The five closest winners run 17 to 38 pages of main text with 5 to 13 tables; the two most recent are 17 and 27 pages. We aim at 26 pages of main text, 7 tables, 4 figures, 8 numbered equations.

### 0. Title and abstract (1 page). Owner: Ludvig, written last

**What to write.** The title with a subtitle naming the two settings ("Index reconstitutions and Fondtorgsnämnden's fund procurements on Nasdaq Stockholm"). An abstract of at most 180 words with five numbers: the OMXSB effect by sub-period, the FTN pressure coefficient in basis points and the share reversed, the incidence result, the cost of a round in months of fee saving. Last sentence: the calibration.

**Winners did.** Four of five use a colon title. Abstracts are 120 to 200 words and carry the headline numbers (2016: "a total mean absolute pricing error of 6.8% per annum"; 2020: five numbers in basis points) and end with the limit ("Our results do not prove the validity of the model, but rather bring into question the validity of the standard benchmarks"). The 2024 winner stated its null in the fourth sentence and the mechanism in the sixth.

**Losers did.** Abstracts that describe what the thesis does ("we examine", "we investigate") with no number; abstracts that end with "we hope this contributes".

**Our rule.** If a number cannot go in the abstract, the thesis is not finished.

### 1. Introduction (3 pages) plus related literature (under 1 page). Owner: Ludvig, week 3

**What to write, paragraph by paragraph.** (1) The fact: a state agency redeems a fifth to almost half of each losing fund on dates it announced months earlier, for reasons unrelated to the stocks the funds hold. Total money moved, the largest single redemption as a share of the fund and as days of volume in the most exposed stock. (2) The anchor and the replication in two sentences, with our number. (3) Why the extension is not "the same thing in Sweden": larger relative to holdings than any reconstitution, three dated steps, a fund-level incidence side. (4) Results with numbers: the pressure coefficient, the share of the move before execution, the reversal horizon, the dilution estimate for funds without swing pricing, the cost against SEK 178m a year. (5) What we do not claim, one sentence each: causality for anticipatory trading; welfare (price pressure is partly a transfer to liquidity providers); generalisation to larger procurements. (6) Contribution in three numbered points, then the roadmap. Then the run-in paragraph "Related literature", three strands, one sentence per strand on how we differ (section 6 below).

**Winners did.** Every one of the five gives the point estimates and the verdict on each hypothesis before the data section: 0.23 percentage points per month (2015); MAPE 6.8 against 22.0 per cent (2016); 4.0, 11.8, 5.5, 16.4 and 8.9 basis points (2020); slope 0.9881 with interval 0.9707 to 1.0054 (2021); 0.83 per cent insignificant, -0.279 per cent insignificant (2024). The 2020 winner states its question in italics. The 2024 winner closes the intro with a run-in paragraph headed "Related literature" of exactly one page. 2015 names its hypotheses in the intro and writes "Taking both hypotheses to the data, we reject the first but find strong support for the second". All end with a roadmap. Introductions run 900 to 1,800 words.

**Losers did.** No question (4 of 33), a list of aims, five numbered questions, or one umbrella question fanning into four or five hypotheses that multiply into dozens of tests (several hundred CARs in one thesis, 60 alphas in another, 150 coefficients across 44 tables in a third). Only 7 of 33 preview results with numbers. The literature and theory sections balloon into textbook exposition where the argument should be.

**Our rule.** One question in one sentence, set off. Numbers by page 3. The FTN part is the contribution and the replication is the proof of competence; the intro says so in that order.

### 2. Institutional background (2.5 pages). Owner: Ludvig, week 1

**What to write.** 2.1 OMXSB: the review cycle, the announcement notice, the effective date, which funds track it and their assets over time, one sentence on what a tracker must do on the effective day. 2.2 FTN step by step, with a date source for each step: the procurement notice; bids and evaluation; the award (tilldelningsbeslut), its standstill and appeals (record delays; the global active round is frozen by the Indecap appeal, Förvaltningsrätten i Stockholm 4909-26, one sentence); fund agreements; the saver letter and the choice deadline; what happens to non-choosers (name the destination fund or the default, with the source); execution by Pensionsmyndigheten in tranches, cash or in kind; the fee saving as the authority reports it. 2.3 Why the flow is uninformed, pre-announced and large, one paragraph each, with the award criteria, the award-to-execution lag in days with its range, and the redeemed shares with the implied days of volume in the most exposed stocks. Figure 1: one round (Swedish active: award 27 August 2025, tranches in January 2026) with one losing fund's capital dropping on its tranche days. Appendix Table A1: every round with category, award date, letter date, execution dates, number of losers, money moved, destination, and the source document for each date.

**Winners did.** 2020 gave XACT's monopoly and the exact rebalancing window in one page and a worked numerical example ("XACT BEAR 2 rebalanced 63.42 % of its total net assets"). 2024 gave the law in one paragraph, the dates of first reading, enactment and both deadlines, and a paragraph on why the control group is valid. Six of the 25 winners exploit a reform or threshold with a dated event, a named control and a pre-trend check, and each spent its background section proving the three properties, not narrating history.

**Losers did.** Three pages on the history of the premium pension since 2000, or a bond-pricing primer, or the legal definition of an insider. Vagueness about where the money went.

**Our rule.** The reader must finish this section convinced that the flow is decided by a regulator, dated to the day, and large relative to the holdings it hits. Without the destination of the money the net dose is wrong by construction.

### 3. Theory and hypotheses (3 pages). Owner: Ludvig, week 2, equations from `01_DESIGN.md`

**What to write.** 3.1 A pre-announced uninformed flow with risk-averse liquidity providers (Greenwood 2005; Duffie 2010), stated as a reduced form, equation (1): the price concedes when the flow is announced, again when it executes because capital is slow, and recovers as more capital arrives. Three predictions: announcement effect, execution effect, reversal. 3.2 Predatory trading (Brunnermeier and Pedersen 2005), one paragraph: traders who know the date and size sell ahead and buy back after, so the price overshoots on the day and the recovery exceeds the day's move. Sunshine trading (Admati and Pfleiderer 1991) in one sentence: a pre-announced uninformed trade attracts liquidity, so the day's move is smaller than an unannounced one. 3.3 The square-root benchmark, equation (2): expected impact equals Y times daily volatility times the square root of order size over daily volume, Y about 0.5 to 1 (Kyle and Obizhaeva 2016; Toth et al. 2011; Bouchaud et al. 2018). Used twice: before the data, to say what size of effect to expect for a typical dose, and after, as the benchmark in the cost-benefit table. 3.4 Four hypotheses as indented numbered blocks, each with the sign, the test and the table:

- H1 (replication). Around OMXSB reconstitutions, additions earn positive and deletions negative abnormal returns from announcement to effective date; the effect increases in expected tracker demand over ADV; whether it declined over 2013-2026 as tracker assets grew eightfold is the sub-question. Table 2.
- H2 (pressure and reversal). On tranche days, abnormal returns are decreasing in the forced net sale over ADV, with beta on the square-root prediction of order one, and the move reverses within 20 trading days. Table 3, Figure 3.
- H3 (anticipation). Part of the move happens between award, letter and first tranche; the pattern separates predation, slow capital and sunshine trading. Table 4.
- H4 (incidence). On tranche days, losing funds without swing pricing show NAV returns below benchmark by about c times r over (1 minus r); funds with swing pricing do not. Table 5, Figure 4.

Table 6 (cost-benefit) is arithmetic on H2 and H4, not a hypothesis.

**Winners did.** 2015 took one published utility function, changed one argument, stated the pricing equation and delegated the derivation ("Brennan shows that solving the maximization problem ... provides the following asset pricing model"), then drew the predicted price path as a schematic figure whose two-paragraph caption explains the hypothesis on its own. That figure is the single exhibit to imitate (our Figure 3, panel A). 2020 wrote the rebalancing identity in four lines and stated the impact formula with a footnote to the derivation. 2016 did the theory in words. 2021 derived fifteen equations over nine pages; that is the ceiling, and it also contains a glossary and a paragraph explaining OLS, which the slides forbid; it won in spite of that.

**Losers did.** Hypotheses that no single table can refute; hypotheses true by construction (an index correlated 0.994 with its own inputs); a "loss aversion" split mechanically related to the sorting variable; CAPM-to-FF5 history as theory.

**Our rule.** One equation per idea, intuition in plain sentences, derivation cited. If a hypothesis needs two tables, split it or drop it. Eight numbered equations in the whole thesis.

### 4. Data (3 pages). Owner: Ludvig writes, Alexander supplies every count

**What to write.** Source by source with period and N inside the paragraph: OMXSB events (Nasdaq notices); FTN rounds and losers (procurement reports, award decisions, appeal rulings); PPM capital and savers by fund-month (Pensionsmyndigheten); tranche days from daily fund units (Morningstar via SHoF); holdings of each losing fund (FI quarterly holdings, the last report before the letter and the first after execution); swing-pricing status with adoption date (fund rules, "justerat fondandelsvärde"); fund NAV and benchmark (Morningstar, prospectus); prices, total return and volume (Datastream). State every filter with counts and every known defect (month-end-only data for the largest Swedish funds; nine foreign-domiciled losers without FI holdings; the 30 unresolved Datastream series). 4.3 The dose, equation (3): minus the sum over losers of redeemed share times fund assets times portfolio weight, plus the money arriving in destination funds times their weights, scaled by the stock's average daily volume, in days of volume. Report its distribution and the top ten stock-events; build the gross (sales only) version for robustness. Table 1 in three panels: A rounds; B the dose (mean, median, p90, max, share above 0.1 days of ADV); C stock characteristics by dose tercile. Figure 2: tracker assets and the yearly OMXSB effect ("the disappearing picture"), and the dose distribution.

**Winners did.** 2015 and 2020 went source by source with N and period in each paragraph (374 months; 19,338 firms; 228,289 stock-quarters). 2016 went variable by variable with a correlation table after each factor and declarative table titles ("Broker-Dealer Leverage is Pro-Cyclical, Primary Dealer Capital Ratio is not"). 2024 described its hand-coding so it could be repeated ("When no pronouns were used, we visually determined the gender"). 2020 opened its data section with a power statement: a short Swedish sample means lower significance, so use the most granular data available. Winners get data from institutions and say so: broker-dealer balance sheets from Statistics Sweden, fund annual reports by hand, KommunInvest bonds, car registrations, Nasdaq ticks via SHoF.

**Losers did.** Pulled everything from a terminal (Eikon, Datastream, Morningstar Direct) or scraped it (Transfermarkt, Excel's STOCKHISTORY), inherited a dataset from another bachelor thesis, built a classification from a blog. Applied a 2019 score to 2004 portfolios. Acknowledged survivorship bias and left it alone. Defined the outcome so that it could not measure what the question asked.

**Our rule.** Every number has a source and a date. Holdings are measured twice (before the letter, after execution) and the difference is evidence on H3, not noise. An OMXSB review within 30 days of a tranche contaminates both samples: flag it, exclude it in robustness.

### 5. Methodology (2.5 pages). Owner: Ludvig writes, Alexander checks every line against the code

**What to write.** 5.1 The replication regression, equation (4): announcement-to-effective abnormal return on expected tracker demand over ADV and sub-period dummies; copy the anchor's layout and say so. 5.2 The FTN windows, fixed here and used nowhere else: award [a-1, a+1]; anticipation [letter, exec-1]; execution [exec-1, exec+1] per tranche; reversal [exec+2, exec+20] and [exec+21, exec+60]. The pressure regression, equation (5): the window CAR scaled by the stock's own daily volatility on the dose, with and without controls, gross and net dose; the coefficient reads as volatility units per day of ADV and is converted to basis points for the median stock in every paragraph. 5.3 The incidence regression, equation (6): fund NAV return minus benchmark on r over (1 minus r), separately for funds with and without swing pricing; the coefficient for funds without is the realised dilution rate, to be compared with the stock-level cost applied to the fund's sold portfolio. 5.4 Inference, once in the text and once in each caption: the shock is by date, so cluster by tranche day, not by stock; with few dates, wild-cluster bootstrap p-values beside the clustered t-statistics, a randomisation test that reshuffles doses within a round, and the Kolari-Pynnönen correction for many stocks reacting on the same day. 5.5 Power, equation (7): the minimum detectable effect at 5 per cent size and 80 per cent power from the spread of window CARs among unexposed stocks and the effective number of independent observations after clustering, printed next to the square-root prediction for the median and the p90 dose; if the MDE exceeds the median prediction, say so and make the headline test the high-dose stock-events. 5.6 The cost arithmetic, equation (8).

**Winners did.** 2020 wrote the anchor's specification, said what it added and why ("but include scaled creation and redemption flows as an additional control variable"), scaled returns by volatility and flows by ADV, winsorised at 1 and 99 per cent, clustered by date, and converted every coefficient in the same sentence: "The price reaction for the average stock in the OMXS30 in response to a 1 % index move is therefore 4.0 basis points (1.499 x 1% x 2.7 %)". 2024 clustered by firm and cited Bertrand, Duflo and Mullainathan (2004) for the reason. 2016 reported two kinds of t-statistics in the same table. Nobody explained OLS. None of the 25 computed a minimum detectable effect, although the slides ask for one; we will be the first.

**Losers did.** iid t-tests on overlapping 255-day windows with hundreds of subsamples; t-statistics of 5 to 14 from calendar-clustered events; degrees of freedom from trading days instead of 28 events; 18 country-level regressors with unclustered firm-level standard errors; 23 clusters with stars that do not match the standard errors; 2,500 words on the logit, likelihood-ratio tests and permutation tests; Wooldridge as a source of method.

**Our rule.** Windows fixed in section 3, used in section 5, never a fifth one in section 6. Clustering by tranche day; with 200 stock-events on five dates, clustering by stock would make the t-statistics two to three times too large.

### 6. Results (9 pages). Owner: Alexander runs each table and writes its one sentence in `output/tables/NOTES.md`; Ludvig writes the prose

**What to write.** One table per hypothesis, in the order of the hypotheses, each introduced by what it tests, read in two paragraphs in economic magnitudes, and benchmarked against the anchor's numbers in the text.

- 6.1 Replication (2 pages). Table 2 panel A: abnormal return by window and sub-period, additions and deletions, N per cell; panel B: equation (4). Compare the Swedish magnitude and trend with the anchor's decade numbers sentence by sentence. Say whether the effect scales with demand over ADV and whether it fell as tracker assets rose eightfold.
- 6.2 FTN price pressure and reversal (3.5 pages). Table 3: equation (5) for the execution window and the two reversal windows, columns with and without controls, gross and net. Figure 3: panel A the schematic path; panel B the average cumulative abnormal return from award to exec+60 for the top dose tercile against the bottom, 90 per cent bands, tranche days marked. Text: the coefficient in basis points for the median and the p90 stock-event; the fraction reversed by day 20 and day 60; beta against the square-root prediction; the index-effect magnitude from Table 2 at equal dose.
- 6.3 Anticipation (1.5 pages, inside 6.2 if space is short). Table 4: the share of the total move in each window for high-dose stock-events, and the holdings change between the pre-letter and post-execution reports as direct evidence of early selling by the losing fund. Which of the three stories the pattern fits, with the 2020 winner's sentence adapted: we do not claim to disentangle predatory from slow-capital trading, only to measure the pre-execution share and its size relative to the day's move.
- 6.4 Incidence (2 pages). Table 5: equation (6), the realised dilution rate for funds without swing pricing, the coefficient for funds with it, and a column with the stock-level prediction applied to the fund's sold portfolio. Figure 4: the tranche-day NAV excess return against r over (1 minus r), marker by swing status. Text: who paid, in basis points of the fund and in SEK per remaining saver. Worked example: SEB Sverige Expanderad (swing pricing) was redeemed on 15 and 19 January 2026, the same weeks as Öhman Sverige, Lannebo Sverige and Prior & Nilsson (none).
- 6.5 Cost-benefit (1.5 pages). Table 6: per round, money moved, predicted impact cost (Y = 0.5 and 1), realised cost with confidence bands, the split between stayers and movers, the cumulative cost, and the break-even number of years against the fee saving. One paragraph on what the comparison means and does not: a transfer to liquidity providers is a cost to savers but not a deadweight loss; the fee saving recurs, the impact cost does not.

**Winners did.** 2015 read each table with "Three things are of note here" and numbered them. 2016 used table titles that state the finding. 2020 and 2024 quoted the anchor's numbers in the paragraph reading each table. 2021 reported that its slope held pooled but failed in ten of eleven years rather than hiding it. The 2020 winner reported its null reversal regressions and said why ("likely a result of the short sample period").

**Losers did.** Read t-statistics instead of magnitudes. Called odds ratios with p = 0.74 "tendencies supporting the glass cliff". Called a coefficient "significant at the 20% level". Reported a 20 per cent annual alpha from 25 microcaps with no cost or liquidity check. Pasted results tables as images. Withheld results that did not fit.

**Our rule.** Every coefficient becomes basis points, SEK or days in the same sentence. If the Swedish index effect did not disappear, that is a finding for the abstract, not a footnote.

### 7. Robustness (1.5 pages). Owner: Alexander

**What to write.** Table 7, one row per named threat, columns for the key coefficient from Table 3 and from Table 5: (1) placebo tranche dates, shifted one quarter and random; (2) exclusion of stock-events within 30 days of an OMXSB review; (3) dose from the pre-letter versus the post-execution holdings report; (4) ADV window 20, 60 and 120 days, and market-adjusted versus market-model versus four-factor returns; (5) drop the largest round, drop the largest stock-event, winsorise at 1 and 99 per cent. Everything else (gross versus net, clustering alternatives, index excluding the event stock) in one sentence pointing to Appendix Table A3.

**Winners did.** 2020 re-ran with 40- and 60-day windows and split market ups from downs. 2024 used a placebo country, an alternative outcome and a year-by-year reduced form. 2015 put minor checks in footnotes and "in results not shown". None ran a page of unmotivated alternatives.

**Losers did.** "Robustness" meaning VIF and Durbin-Watson. Sign consistency of insignificant coefficients called robust. A laundry list of alternatives with no threat named.

**Our rule.** Each row of Table 7 answers an objection that can be stated in one clause; otherwise the row goes.

### 8. Conclusion (1.5 pages). Owner: Ludvig, last, with `conclusions_winners_vs_nonwinners.md` open

**What to write.** Paragraph 1: the three numbers (index effect trend, FTN pressure and reversal, incidence) and the cost against the fee saving. Paragraph 2: what it says about pre-announced uninformed flows in a small market, against the anchor. Paragraph 3: the limits before the examiner writes them: anticipation cannot be attributed to a trader type; the concession is partly a transfer, so the cost-benefit is from the savers' side; the number of tranche dates is small, so clustered inference is the binding constraint; the result may not scale to the larger procurements to come. Paragraph 4, only if the stock-level result is null: the minimum detectable effect, what sizes of impact the data rule out, and what the fund-level and anticipation evidence still shows. Paragraph 5: two next steps (intraday execution data; the next rounds as an out-of-sample test).

**Winners did.** Put the coefficient and the anchor's coefficient in the same sentence (2011: "-2.71 percent ... in line with ... Ahern and Dittmar (2009) who obtained ... -2.6 percent"). Put the identification problem inside the claim (2011 short-sale bans: "associated with ... However, graphical results and various subsample re-estimations indicate that the adoption of the bans is endogenous. Hence, it is hard to assign the observed effects"). Said what the result does not mean (2016: the benchmark models are questionable, not the model proven). Ranked candidate explanations and reported having tested one (2011 quota: tested three-year lagged effects, found none). Gave a counterfactual magnitude (2018: a 2.85 per cent reduction in BEV sales). Derived a directional policy statement from the sign (2012: a larger tick size "would thus not be recommended"). Named the next experiment (2013: the Italian STT of March 2013). Nulls: the 2024 winner said it first and plainly, reported point estimate and standard error every time, showed the design had bite (strong first stage, null placebo), looked for the effect in alternative outcomes and timing, turned to the mechanism, and explained with institutions (six-year transition against two). Its one gap: no power calculation, so "no effect" and "could not have seen it" were not separated. We separate them.

**Losers did.** Narrated an insignificant coefficient as a tendency and then acted on it ("Issuers ... should not fear underpricing as much during crises" after a null). Used causal verbs on group comparisons and OLS ("differs between countries due to differences in welfare"). Handed the explanation to future research ("more research is needed in this field of study"). Presented an untested claim as a finding (IFRS and a spinning ban "have increased trust", never tested). Ended with investment advice as the payoff. Muddled the hypothesis logic ("cannot be rejected" for a positive claim after stating no causality can be identified). Closed with a flourish ("what norms and values are going to influence the stock market of tomorrow?"). Or disclaimed the whole result in 87 words. One well-built non-winner (6812) read a low-powered null as evidence that regulation works; the winners' nulls rest on something measured.

**Our rule.** A winning conclusion is the tables rewritten as prose; a losing conclusion is the introduction rewritten as if the tables had cooperated. "Associated with", never "caused", unless the design earns it. The recommendation stays with execution mechanics (staggering, in-kind transfers, swing pricing), where the evidence bears; the thesis does not evaluate the procurement regime.

### Appendix (3 pages)

A1 the procurement calendar with a source per date (a contribution on its own). A2 variable definitions, one row per variable with source and construction. A3 the remaining checks. A4 the AI disclosure, two sentences as the 2024 winner wrote them, from `AI_LOG.md`. Trap: parking the main tables in the appendix, as the 2020 winner did (53 pages with the appendix; under today's rule it would not pass).

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part D. The literature

## The literature: what we read, what we take, how we differ

### How to do the literature work (Ludvig, weeks 1 to 2)

1. Read the anchor twice: once for the story, once with a pen for the windows, filters, table layout and the numbers to print beside ours.
2. For each paper to be cited (25 to 30 of the 66 in `literature/literature_verified.md`), write a four-line card in `literature/cards.md`: the question; the data and identification; the one magnitude we may quote; how we use it or how we differ. No fourth line, no citation.
3. Verify every record against the publisher's page before it enters `references.bib`. The entries flagged [M] (Almgren et al. 2005; Frazzini, Israel and Moskowitz 2018; the Coval-Stafford DOI; Christoffersen et al.) are not cited until checked. A magnitude recalled from memory is never printed.
4. The related-literature text is one run-in paragraph under one page at the end of the introduction: three strands, two or three papers each, one sentence per strand on how we differ.
5. If we borrow a table layout or the exposure measure from an SSE winner (the 2020 thesis for volatility scaling and date clustering; the 2021 thesis for the Kyle-Obizhaeva form), we cite it; the slides treat uncited borrowing of table formats as plagiarism.
6. Every quoted magnitude carries its table or page, so the number audit in week 5 can trace it.
7. Every in-text source is in the list and every list entry is cited; author names are spelled as on the paper. The course asks for 2 to 3 top-journal papers closely related; the winners' lists have a median of 25 entries.

**What the losers did with literature, and we will not:** anchors in lower-tier journals or practitioner books (*What Works on Wall Street*); anchors used for the variable list or the sample filters rather than the design; an anchor discarded as "a flaw" and dropped from the references; "Lowery" for Lowry, "Young" for Yung; listed papers never cited; 40 web pages among 104 references; Investopedia, Forbes, CNN, LinkedIn; a 5,000-word review (one older winner did this too; the recent winners never exceed a page).

### Strand A: the index effect and its decline (the anchor strand)

- **Shleifer (1986, JF)** and **Harris and Gurel (1986, JF)**: about +3 per cent at S&P 500 inclusion; Shleifer reads a permanent shift (demand curves slope down), Harris and Gurel temporary pressure reversing within about two weeks. These are the two readings Table 3 chooses between. Magnitudes [M]; check.
- **Kaul, Mehrotra and Morck (2000, JF)**: the 1996 TSE 300 float redefinition, pre-announced, no information, no change in rights: +2.3 per cent in the event week, no reversal. The cleanest pre-announced pure demand shock in the literature and the closest analogue to FTN's flow.
- **Greenwood (2005, JFE)**: the Nikkei 225 redefinition; risk-averse arbitrageurs absorb a known flow; the price moves at announcement, again at execution, then reverses. Our equation (1). Cite, do not derive.
- **Chang, Hong and Liskovich (2015, RFS)**: Russell cutoffs as a discontinuity; index demand moves prices.
- **Greenwood and Sammon (2025, JF)**: the anchor.
- We differ: a larger flow relative to holdings, three dated steps, a fund-level incidence side, and no learning yet.

### Strand B: price pressure from fund flows (the method strand)

- **Coval and Stafford (2007, JFE)**: funds with extreme outflows sell their holdings; commonly held stocks drop and recover over 12 to 18 months; because flows are predictable, front-running is possible. Cite for the pressure-and-reversal template and the front-running idea behind H3.
- **Lou (2012, RFS)**: flow-induced trading built as fund flow times portfolio weight, aggregated to the stock. Our dose is this construction with the agency's redemption as the flow.
- **Wardlaw (2020, JF)**: the standard measure is mechanically tied to the stock's own return in the flow quarter. We avoid the critique by construction: holdings from the report before the letter, prices from before the event, a flow fixed by the award. One sentence in the method.
- **Da, Larrain, Sialm and Tessada (2018, RFS)**: Chilean pension savers following an adviser's switch calls moved USD 1-5bn at a time, 10 to 20 per cent of fund assets, forcing managers to trade about 10 per cent of their equity book within days in a market with about USD 205m of daily turnover; about 1.06 per cent on day 1, 1.22 by day 3, fully reversed within 15 days (NBER WP tables 5 to 7; check against the RFS version). The closest published analogue: coordinated, uninformed, huge relative to volume, small market. Table 3 and Figure 3 follow its event-day CAR, reversal and cross-section. We differ: administrative dates, state execution.
- **Hartzmark and Solomon (2025, AER)**: predictable dividend cash flows move the whole market; multiplier about 1.9. Motivation and benchmark.
- **Sabbatucci, Tamoni and Xiao (2023, SSRN 4322784)**: the examiner's working paper on 401(k) shifts moving stock prices through fund holdings. Cite in the motivation; read the current version before quoting anything.

### Strand C: theory, four ideas

- **Duffie (2010, JF)**: slow-moving capital; equation (1) with Greenwood (2005).
- **Brunnermeier and Pedersen (2005, JF)**: predatory trading; the competing story in H3.
- **Grossman and Miller (1988, JF)** and **Admati and Pfleiderer (1991, RFS)**: liquidity provision and sunshine trading; the third story, one sentence.
- **Wurgler and Zhuravskaya (2002, J. Business)**: larger drops for stocks without close substitutes; one cross-sectional check (dose effect rising in idiosyncratic volatility), in Table 7 or the controls, not a hypothesis.
- Koijen and Yogo (2019) and Gabaix and Koijen (2021) on inelastic markets: one sentence of motivation if space allows, otherwise out.

### Strand D: how big the drop should be (the square-root law)

- **Kyle and Obizhaeva (2016, Econometrica)**, **Toth et al. (2011, Physical Review X)**, **Bouchaud et al. (2018, CUP textbook)**: impact equals Y times daily volatility times the square root of order over daily volume, Y about 0.5 to 1. Equation (2), our pre-committed Y = 0.7, a predicted drop for every stock and tranche day before any price is seen.
- **Zarinelli et al. (2015)**: for very large orders impact flattens below the square root; our biggest doses sit there, so the square-root prediction is an upper bound.
- **Almgren and Chriss (2001, Journal of Risk)**: optimal liquidation trades off expected cost against variance; tranches lower temporary impact. The theory behind the agency's own staggering and the frame for the policy sentence.
- Almgren et al. (2005) and Frazzini, Israel and Moskowitz (2018): [M], cite only after checking.
- Use: beta in Table 3 is the realised drop over the square-root prediction. Near 1, the market treated the state's sale like any other big order; near 0, it absorbed the sale at no price cost; above 1, something extra. Beta not equal to 1 is a finding, with the MDE stated.

### Strand E: who pays (incidence)

- **Edelen (1999, JFE)**: flow-driven trading costs a fund about 1.5 to 2 per cent of assets a year [M], paid by all holders. The baseline "stayers pay".
- **Greene and Hodges (2002, JFE)**: the NAV-dilution accounting; equation (6) on one day.
- **Chen, Goldstein and Jiang (2010, JFE)**: in illiquid funds redemptions hurt stayers more, which creates a first-mover advantage; why swing pricing exists.
- **Jin, Kacperczyk, Kahraman and Suntheim (2022, RFS)**: UK bond funds; swing pricing's dilution adjustment averages about 33 bp and offsets stress outflows almost one for one. Table 5 is their design on Swedish equity funds. We differ: the redemption is executed by the state, so the first-mover game is between the agency and the stayers.
- **Capponi, Glasserman and Weber (2020, Management Science)** and **Lewrick and Schanz (2017, BIS)**: what a swing factor must do for a 20 to 44 per cent redemption; swing funds' returns hold up in stress. One sentence each.
- **Dahlquist, Martinez and Söderlind (2017, RFS)**: PPM daily data; flows hitting fund NAVs. Method for Table 5 and the Swedish strand.
- We differ: a dated, state-executed redemption of a known share; swing pricing legal in Sweden only from July 2023, so a before-and-after inside one country (the 2019 purge had none by law).

### Strand F: the statistics we lean on

Boehmer, Musumeci and Poulsen (1991) for the standardised event test; Kolari and Pynnönen (2010, RFS) for many stocks reacting on the same day; Petersen (2009, RFS) for clustering by date; Young (2019, QJE) for randomisation inference with few clusters; Kothari and Warner (2007) and MacKinlay (1997) as references. One sentence in the method and one line in each caption. No paragraph explaining OLS.

### Strand G: the Swedish premium pension (context, short)

Cronqvist and Thaler (2004, AER P&P) and Cronqvist, Thaler and Yu (2018, AEA P&P): the 2000 launch and the inertia since; the menu, not the saver, decides where money sits, which is why only the state can move these positions and why the move is uninformed. Dahlquist and Martinez (2015, EFM): PPM money responds less to performance than retail money in the same funds. Kinnerud and Lorentzon (2026, AEJ: Applied): letters do not move most savers even when search costs are removed; the state's rationale for procuring the menu. Sialm, Starks and Zhang (2015, JF), Pool, Sialm and Stefanescu (2016, JF), Keim and Mitchell (2018, JPEF): sponsors' menu changes, not participants, drive large flows; removals are not information about the stocks. Institutional sources: SOU 2019:44, prop. 2021/22:179, lag (2022:759) and (2022:760), FTN's reports and award decisions, Pensionsmyndigheten's avslutsprocess document and fee figure, FI (2025), RiR 2018:32, the Riksrevisionen audit opened June 2026 (check in November). Every date in the thesis has one of these as its source.

### The related-literature paragraph itself

(i) The index effect and its decline: Shleifer; Harris and Gurel; Chang, Hong and Liskovich; Greenwood and Sammon. We differ by a new, larger, three-step flow in the same market. (ii) Flow-induced pressure and slow capital: Coval and Stafford; Lou; Da et al.; Greenwood; Duffie; Brunnermeier and Pedersen. We differ by administrative dates and a dose built before any price is seen. (iii) The premium pension and who pays: Cronqvist and Thaler; Dahlquist, Martinez and Söderlind; Jin et al. We differ by the first measurement of the reform's executions and their incidence.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part E. Method and maths

## The method in plain words

**Abnormal return.** The stock's return minus the market's (OMXSPI or OMXSGI) that day, as the anchor does. A four-factor version with Swedish factors is one robustness row.

**The dose.** For each stock and tranche day: how much the losing funds had to sell in that stock (redeemed share times fund assets times the fund's weight in the stock) minus what the winners bought (spread over the month's trading days), divided by the stock's average daily volume. A dose of 0.5 means the forced net sale equals half a normal day's trading. Built from holdings before the letter and prices before the event, so it is fixed before anything happens.

**The main regression.** The tranche-day abnormal return, scaled by the stock's own volatility, on the dose. Read two ways: in basis points for the median and the p90 stock-event, and as beta, the realised move divided by the square-root prediction. Then the same for the reversal windows and for the award and anticipation windows.

**Who paid.** On a tranche day the fund's NAV return minus its benchmark, on r over (1 minus r), separately for funds with and without swing pricing. The coefficient for funds without is the realised dilution rate and should match the stock-level cost applied to the fund's sold portfolio.

**Inference.** The shock is by date, so we cluster by tranche day, not by stock. With few dates we also report wild-cluster bootstrap p-values and a randomisation test that reshuffles doses within a round. The Kolari-Pynnönen correction handles many stocks reacting on the same day. Stated once in the text and once in each caption.

**Power.** Before any FTN result, the minimum detectable effect at the 5 per cent level and 80 per cent power, printed next to the square-root prediction for the median and p90 dose. If the MDE exceeds the median prediction, the headline test is on high-dose stock-events, and we say so.

**Unblinding.** `replication_omxsb.py` runs now and touches no FTN date. `ftn_eventstudy.py` and `dilution.py` stay switched off until Klug has agreed the specifications and the date is written into `03_DATA.md`, section E. Anything run afterwards that is not in `01_DESIGN.md` is labelled exploratory.


## Harder maths that fit inside the existing tables

We want the maths harder than a BSc thesis usually carries, without adding an exhibit or opening a test after the data are seen. The rule: each addition is written into `01_DESIGN.md` section 8 and the method note before the sign-off, lands in an existing table, figure or caption, and its derivation goes to Appendix A3. The main text keeps eight numbered equations; the 2021 winner's fifteen equations over nine pages is the ceiling, and it also carried a glossary and an OLS paragraph that the slides forbid. Four additions, in order of value:

**1. The impact exponent, not only beta (one extra column in Table 3).** The square-root law says the move grows with the dose to the power one half; Kyle's (1985) linear model says power one; the latent-order-book model (Toth et al. 2011) gives one half and explains why. Estimate the exponent directly: regress the log of the absolute volatility-scaled tranche-day CAR on the log of the dose for high-dose stock-events, and report a Wald test of the exponent equal to 0.5 against 1 (the 2021 winner's H0: slope = 1 format). Measurement error in the dose pulls the estimate toward zero; the pre-letter and post-execution holdings give two noisy measures of the same dose, so use one as an instrument for the other (classical errors-in-variables) and report the IV estimate as a robustness row. Owner: Alexander (code), Ludvig (two paragraphs in section 3.3 and the appendix derivation).

**2. The reversal half-life from the slow-moving capital model (one parameter in the Figure 3 caption).** Under Greenwood (2005) and Duffie (2010) the concession after the tranche decays as capital arrives at a constant rate: CAR at event time tau equals minus kappa times the dose times exp(minus lambda times tau), plus a constant. Fit kappa and lambda by nonlinear least squares on the average event-time CAR of the top dose tercile, with a bootstrap band by tranche day, and report the half-life ln 2 over lambda in trading days. Compare it with the pre-committed 20-day window, with Da et al.'s 15 days, and with the reversal after the OMXSB effective day in Table 2. The fixed windows stay the primary test; the half-life is the economic reading of the picture. Owner: Alexander (fit), Ludvig (one paragraph in 6.2).

**3. The optimal-execution counterfactual (two extra columns in Table 6).** With square-root impact, a sale of Q split into n equal tranches on separate days costs Q times Y sigma times the square root of Q over V, times n to the power minus one half: the cost falls with the square root of the number of tranches, while the variance of the execution price rises with n. That is Almgren and Chriss (2001) with concave impact, and it is the trade-off the agency faces when it "staggers large funds so that sales do not move prices". For each round compute the predicted cost at the actual schedule (one to three tranches), at ten and at twenty tranches, and the schedule that equates marginal cost and marginal variance for a stated risk aversion. The policy sentence then has a number: spreading the Swedish active round over ten days would have cut the predicted impact cost by a stated share. Derivation in Appendix A3; one paragraph in 6.5. Owner: Alexander (table), Ludvig (derivation and text, checked with Klug).

**4. The implied demand elasticity (one sentence in 6.2).** Translate the pressure coefficient into a daily demand elasticity: the forced sale as a share of shares outstanding, divided by the abnormal return, for the median and the p90 stock-event, beside the elasticities in Chang, Hong and Liskovich (2015), Da et al. (2018) and Koijen and Yogo (2019). Needs shares outstanding (the NOSH pull). Owner: Alexander.

What we do not add: a structural model of liquidity provision, a second anchor, or any new table. If space runs short, additions 4 and 2 go first, then 1; the counterfactual in Table 6 stays, because it is the sentence Pensionsmyndigheten can act on.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part F. Exhibits and data

## The tables and figures: how each is built

| Exhibit | What it shows | Script | Expect | Benchmark in the text |
| --- | --- | --- | --- | --- |
| Table 1 | Rounds, money moved, dose distribution, stock characteristics by dose tercile | `pressure.py` plus a table script | Descriptive | Da et al.'s 10 % of the equity book |
| Table 2 | OMXSB abnormal return by window and sub-period; regression on demand over ADV | `replication_omxsb.py` | Small, weaker recently; a volume spike on the effective day | Greenwood and Sammon's decade numbers |
| Figure 2 | Tracker assets against the yearly effect; dose distribution | same | The disappearing picture, Swedish version | their Figure 1 |
| Table 3 | Tranche-day abnormal return against the dose; reversal windows; gross and net | `ftn_eventstudy.py` (gated) | Little in large caps (tiny doses); a drop and recovery in small caps | square-root prediction; Da et al. 1.06 % |
| Figure 3 | Schematic path; average CAR award to exec+60, top versus bottom tercile, 90 % bands | same | A dip at the tranche, recovery after | the 2015 winner's Figure 2 (format) |
| Table 4 | Share of the move per window; holdings change pre-letter to post-execution | same | Little at award; some early selling by managers | the 2020 winner's anticipatory split (format) |
| Table 5 | Fund NAV minus benchmark on tranche days, with and without swing pricing | `dilution.py` (gated) | A few bp lost without swing pricing, none with it | Jin et al.'s 33 bp adjustment |
| Figure 4 | NAV excess return against r/(1 - r), marker by swing status | same | Two clouds | |
| Table 6 | Per round: money moved, predicted and realised cost, stayers versus movers, break-even months | small script | A number the policy debate lacks | SEK 178m a year |
| Table 7 | Robustness rows for Table 3 and Table 5 | gated scripts with flags | Nothing on placebo dates | |
| Figure 1 | One round's timeline with one losing fund's capital | small script | Illustration | |

Every table is written by its script as a `.tex` fragment into `output/tables/` and `\input` into the text. Nobody types a number. Every caption restates the estimated equation, defines each variable, names the sample and period, and states the standard-error treatment; the 2015 winner's Table 4 caption is longer than the table, and that is the standard. Table titles may state the finding, as the 2016 winner's did.


## The data, item by item (status 25 October)

| What | Source | Status | Who |
| --- | --- | --- | --- |
| 394 OMXSB events 2013-2026; 48 OMXS30 events 2005-2026 | Nasdaq releases, newswires | Done, verified against prices | A |
| FTN rounds, dates, winners, losers, bids, fees | 11 FTN reports | Done (`data/derived/ftn_2026-10-11/`) | A |
| PPM capital, savers, net trade, fees per fund-month 2018-2026 | Pensionsmyndigheten monthly files | Done (`data/panel/`) | A |
| Tranche days and redeemed share per losing fund | Morningstar daily units via SHoF | Done for about 30 of the 78 entries to 30 Sep (the method note counts 73 funds; reconcile); refresh to 31 Oct in week 2 | A; L requests the refresh |
| Sale orders for the largest Swedish losers (Avanza Zero, Storebrand Sverige, LF Sverige Vision, Handelsbanken Sverige, Nordea Swedish Stars and others with month-end-only data) | Pensionsmyndigheten, offentlighetsprincipen | Request not sent | L |
| Holdings of each losing fund | FI quarterly holdings | 4 of 12 quarters; 13 zips to download (links in `03_DATA.md` B) | A |
| Swing-pricing status and adoption date | Fund rules, annual reports | 11 yes, 38 no, 29 unknown (mostly Luxembourg) | L fills gaps if time |
| Daily price, total return, volume | Datastream pull of 15 Oct | On disk, wide, names only, 30 unresolved series; MV, NOSH, the index series and a code row to pull; then the long format (`data/prices/README.md`) | A |
| Swedish factors | SHoF Fama-French page | Not pulled; robustness only | A |
| Fund NAV and benchmark | Morningstar reinvested prices, fund master | Done; opened only after unblinding | A |

Holdings gap to state in the text: only Swedish-domiciled funds report to FI; nine foreign-domiciled losers need semi-annual reports or Morningstar holdings via SHoF; until then they are out of the dose, which biases it down, not up.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part G. Outcomes, work plan, checklists

## What we expect, and how the conclusion reads in each case

1. **Most likely.** Prices drop and recover in small caps; large caps show nothing visible because their doses are tiny; stayers in funds without swing pricing pay a few basis points per tranche day; the OMXSB effect is small and has fallen. The conclusion gives the SEK cost per round against the fee saving and recommends execution mechanics: staggering, swing pricing, in-kind transfers.
2. **Effect only in small caps.** The same, with the large-cap null stated with its MDE.
3. **Nothing anywhere.** The conclusion states the MDE, what sizes of impact the data rule out, and what the fund-level and anticipation evidence still shows. Three of the 25 winners are outright nulls; the 2024 winner won with a null on every outcome, explained by the institution.

In all three: one sentence per claim with our number, the benchmark and the bound.


## Order of work and who does what

Dates and gates in `STEPS.md`; division of labour and working rules in `PLAN.md`, sections 6 and 7.

- **Alexander:** repo private and pushed; the stock panel into the code's format; Table 2; the FI zips, the dose, the power calculation; after sign-off Tables 3 to 7 and the figures; one script per exhibit; the clean-machine run; the replication package.
- **Ludvig:** Klug (method note, sign-off meeting in the week of 2 November, three lines every Friday); the Pensionsmyndigheten request; the SHoF refresh request; literature cards and the related-literature paragraph; sections 2, 3, 4 and 5 in that order, then 6 from Alexander's table sentences, then 1, 8 and the abstract; the AI log and appendix; references and format.
- **Both:** the Friday swap (Alexander reads the text for claims without a table cell; Ludvig reads the code for a choice not in the design file); three lines in `STATUS.md` each evening.

Full draft to Klug Friday 20 November. Submission-ready Friday 4 December. Hard deadline Monday 7 December, 10:00.


## Two checklists

### Must have (what the winners have)

- [ ] One research question in one sentence, set off in the introduction.
- [ ] The anchor named on page 1 or 2 with "we follow" or "akin to", its specification reproduced, its numbers quoted beside ours in a sentence.
- [ ] Every headline number in the introduction and the abstract.
- [ ] The three institutional properties (uninformed, pre-announced, large) proven with dates and shares, and a dose that varies across stocks within a day.
- [ ] Four hypotheses, one table each, windows fixed before the data.
- [ ] A mechanism test (anticipation; swing pricing) after the headline result.
- [ ] The minimum detectable effect stated before the FTN results. No winner did this; the course asks for it.
- [ ] Clustering by tranche day, with bootstrap and randomisation p-values where dates are few.
- [ ] Every coefficient converted to basis points, SEK or days in the same sentence.
- [ ] Captions that restate the equation and define every symbol.
- [ ] A conclusion that states the numbers, the benchmark, the limits, and what the design cannot show.
- [ ] 25 to 30 references, every one verified, every one cited, at least ten in top journals.
- [ ] An AI appendix of two sentences, from the log.
- [ ] 33 pages or fewer, no table of contents, official front page.

### Must not have (what the losers have)

- [ ] A fan of hypotheses or hundreds of reported tests.
- [ ] Textbook exposition of OLS, event studies, the CAPM or the EMH.
- [ ] A literature review longer than a page.
- [ ] An anchor used for the variable list rather than the design, or missing from the references.
- [ ] A window, split or test chosen after seeing the data.
- [ ] A dose built from post-event holdings or prices (the Wardlaw critique).
- [ ] iid t-tests on overlapping windows; clustering by stock when the shock is by date.
- [ ] "Tendencies", "seems", "significant at the 20% level", or advice built on a null.
- [ ] "Caused" for a correlational design; a claim in the conclusion that no table tested.
- [ ] "More research is needed" in place of an explanation.
- [ ] Investment advice as the payoff; a policy sentence about the regime rather than the execution.
- [ ] Results tables pasted as images; numbers typed by hand.
- [ ] Web pages, blogs or news sites as sources of method or fact where a document exists.
- [ ] Licensed data in a public repository.

