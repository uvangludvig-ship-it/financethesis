# Winners audit: what the 25 awarded SSE finance theses share, and which design (A, B, C) looks most like one

Prepared 5 October 2026 (round 1). An independent, evidence-first re-test of the earlier winners/non-winners conclusions, used to choose between (A) Sialm, Starks and Zhang (2015) reframed, (B) Cookson et al. (2021) selection and outside flows, and (C) Da et al. (2018) price pressure.

Labels: **VERIFIED** means I checked it in the thesis text, file or script cited. **JUDGEMENT** is my reasoning. **NOT VERIFIED** means I could not confirm it. Facts about designs A, B and C that I did not check myself are marked "per SSZ dossier" (`round1/ssz_dossier.md`) or "per briefing" (`BRIEFING.md`).

Paths. Winners: `/home/claude/uvangludvig-ship-it/financethesis/old_winners/text/<file>.txt` (cited below by year and prize, e.g. "2023 Hiller"). Non-winners: `.../non_winners/text/<MediumId>.txt` (cited by id). "Line" means a line in that .txt file. Scripts and outputs: `scratchpad/anchor_final/round1/audit_work/`.

---

## 0. Bottom line

1. **Of the six earlier claims, two hold as stated, three hold only in part and one is wrong in its second half.**
   - (1) "15 of 25 have an anchor whose question equals the thesis question." This depends on the coding. 12 do strictly (one or two named papers asked the same question). 17 do if prior literatures without a single anchor count. 15 sits inside that range. Since 2019 the count is 8 of 11.
   - (2) "9 table-level replications" is VERIFIED. "All from 2016 onward" is contestable, because the 2011 Hiller quota thesis reproduces Ahern and Dittmar's announcement CAR on the same event (-2.71% against their -2.6%). "7 of 12 since 2019" cannot be reproduced: there are 11 winners from 2019 onward, and 8 of them replicate or transplant an anchor's specification.
   - (3) "Six winners exploit a reform or threshold with a control" is VERIFIED (five dated reforms plus one regression-discontinuity threshold). But four of the six date from 2011 to 2013, and only one of the 11 winners since 2019 has such a design. The rider "none of the non-winners do" is FALSE at corpus level. At least 10 non-winners use a dated reform or threshold with a control group, including topical twins of two winners: 1305 (tick-size cut) and 1955 (short-sale ban).
   - (4) "The extension sits inside the anchor's tables" is VERIFIED for 8 of the 9 replicators. It does not discriminate: non-winners 4441, 5277, 5522 and 6812 do the same.
   - (5) "Winners compare their numbers to the anchor's" holds strictly (anchor's estimate and own estimate in the same passage) for 6 of 25. Counting qualitative "similar to" or "in line with" comparisons it is 11 of 25. Non-winners do it too (4441, 5522).
   - (6) Over-claiming, 16% of winners against 58% of sampled non-winners: every quote I checked exists (4 winners, 10 non-winners). The rates themselves come from one unblinded coder and were not re-coded. If accepted, the gap is significant (Fisher p = 0.0025) and is still the strongest discriminator in the corpus.
   - "Method-only anchors have not won the Hiller since 2021" is true only for the 2022 to 2024 prizes (three in a row). The 2021 Hiller winner itself is method-anchored (Busse and Green). The Viotti prize went to a model-anchored thesis in 2023. Under the 2011 to 2021 Hiller base rate, a streak of three has about a 17% chance, so it is not evidence.
2. **The "winner package" (same-question top anchor, replication, extension inside the anchor's table, numbers compared) is close to necessary in recent years but not sufficient.** Non-winners 4441 (2019, Lucca and Moench), 5277 (2022, Cremers and Petajisto), 5522 (2022, Liu, Tsyvinski and Wu) and 6812 (2026, Parise and Rubin) have all of it. In the cleanest matched pair, the 2023 Hiller winner (Cieslak et al.) and non-winner 4441 (Lucca and Moench) both replicate a pre-FOMC anomaly and show it vanishing afterwards. The winner explains the change with measured variables inside the anchor's regression. 4441 attributes it to the efficient-market hypothesis without testing that.
3. **Examiners and tutors (VERIFIED from `roles_all.csv` and grep):**
   - Sabbatucci never examined a thesis in the corpus. He tutored 20 non-winners (2018: 5, 2022: 5, 2023: 10) and no winner.
   - Klug formally tutored one thesis (6238, 2024) and co-tutored one (5522, 2022, "A Replicative Reassessment"). Neither won.
   - D'Avernas examined 9 of the 11 winners from 2019 to 2024 and about 222 non-winners. Baghai examines the 2025 and 2026 cohorts.
   - So the corpus contains no revealed-preference data on Sabbatucci as an examiner.
4. **Rubric result (section 5).** A scores 77% of the weighted maximum, B 53% and C 46%. A also wins under equal weights (76 / 58 / 49%) and under a weighting that stresses identification (72 / 58%). B overtakes A only if informative-null power and replication carry almost no weight, which is the opposite of what the evidence supports.
5. **Why A (section 6).** A is the only design that meets the course's stated standard (replication plus a meaningful extension) at table level, with a powered replication test. Its extension tests a mechanism inside the anchor's table, which is the feature that separates the 2023 FOMC winner from 4441. A null result in A is still informative.
   - The strongest counter-argument is that A has exactly the package that 4441, 5277 and 5522 had when they lost. It must therefore lead with the sponsor switch, not with "SSZ on Swedish data".

---

## 1. Method, and what was reused from the earlier runs

**Partial work inspected and reused (VERIFIED):**
- `roles.py` and `roles_all.csv` extract tutor and examiner lines from the first 160 lines of all 660 texts: 589 have a tutor line and 350 an examiner line. No examiner lines exist before 2019, which is a format change.
  - Checked against a raw grep of all texts. "Sabbatucci" appears in exactly the 20 files the CSV lists. "Klug" appears in 8 files: 2 as tutor (6238, 5522), 5 in acknowledgements (4631, 5299, 5474, 5517, 5533), and 1 false positive in garbled text (5741).
  - `examiners_nonwinners.json` agrees within a few theses: d'Avernas 224 plus 2 variant spellings, against 222 by my year tabulation; Baghai 106 against 105.
- `did.py` and `did_counts.csv` count identification vocabulary ("difference-in-difference(s)", "diff-in-diff", case-sensitive `\bDiD\b`, "regression discontinuity", RDD, "synthetic control", "triple difference", DDD), with reference lists cut. Because the match is case-sensitive, `\bDiD\b` cannot match "did". This fixes the fault the rival review found in the old script.
- `cmp.py` and `cmp2.py` find anchor-name sentences that contain numbers. They are noisy and were used only as pointers, then read by hand.
- `peek.py` prints anchor phrases and the conclusion of a non-winner.
- New in this run:
  - `intro.py`: abstract, introduction and conclusion, flattened.
  - `q.py`: phrase search on flattened text, for quotes broken across lines.
  - `rep.py` and `rep_counts.csv`: explicit "replicat* + study/method/et al." statements, references cut.

**Coding rules (JUDGEMENT, fixed before counting):**
- *Same-question anchor (Q1).* One or two named papers asked the same economic question (same outcome, same treatment or explanatory variable), and the thesis re-asks it in a new sample, period or setting.
  - *Q1-lit:* the question belongs to a named prior literature, but no single paper is replicated.
  - *Q2:* the anchor's question is adjacent (same design, a different treatment or outcome).
  - *Q3:* the anchor supplies only a method, or there is no anchor.
- *Table-level replication.* The thesis estimates the anchor's own specification and says so.
  - *R1:* on the anchor's original sample, then extended.
  - *R2 (transplant):* the anchor's specification on new data.
- *Numeric comparison.* The anchor's estimate and the thesis's estimate in the same passage.
- *Reform design.* A dated policy change, or a sharp regulatory threshold, with an explicit control group.

**Reading depth.**
- Winners: abstract, full introduction, conclusion, and every passage naming the anchor, for all 25.
- Non-winners: abstracts for all 37 theses discussed here, plus targeted passages for 4441, 4439, 5737, 6045, 6591, 6687, 4448, 5277, 4092, 4962, 5522 and 3966.
- Non-winners were therefore coded more shallowly than winners. Where that biases a comparison, I say so.

---

## 2. Claim-by-claim verification

### 2.1 The 25 winners as coded (VERIFIED unless marked)

| Year, prize | Thesis | Anchor as cited | Q | Replication | Extension inside anchor spec | Numeric compare to anchor | Reform design |
|---|---|---|---|---|---|---|---|
| 2011 Hiller | Norwegian gender quota | Ahern & Dittmar (2009) | Q1 | Partial: same-event CAR | No (main DiD is their own design) | **Yes**: "-2.71 percent ... in line with ... Ahern and Dittmar (2009) who obtained ... -2.6 percent" (line 1173) | **Yes**: DiD, Norway vs Sweden |
| 2011 Viotti | Short-sale bans and options | Grundy et al. (2010); Battalio & Schultz (2009) | Q1 | No | n/a | Qualitative: "In contrast to previous empirical work" | **Yes**: staggered bans in 10 countries, ban-removal DiD |
| 2012 Viotti | Tick size and volatility | Hau; Bessembinder (cited by number) | Q1-lit | No | n/a | Qualitative ("corroborated by earlier panel studies") | **Yes**: RDD at the 100 SEK threshold |
| 2013 Hiller | Takeover rumours | Pound & Zeckhauser (1990); Zivney et al. (1996) | Q1-lit | No | n/a | Qualitative | No |
| 2013 Viotti | French FTT | Umlauf (1993); Jones & Seguin (1997); Liu & Zhu (2009) | Q1-lit | No (measures follow Jones & Seguin, line 593) | n/a | No | **Yes**: DiD with Eurozone controls, 1 Aug 2012 |
| 2014 Viotti | Sukuk | Nelson-Siegel; Diebold-Li; Chen et al. (2007) | Q3 | No | n/a | No | No |
| 2015 Hiller | Fund-flow risk | Coval & Stafford (2007); Lou (2012) as mechanism (line 122) | Q3 | No | n/a | No | No |
| 2015 Viotti | Commodities | Daskalaki & Skiadopoulos (2011); Tang & Xiong (2012) | Q1-lit | No | n/a | No | No |
| 2016 Hiller | Intermediary asset pricing | Adrian et al. (2014a); He et al. (2016) | Q1 | R2 ("we follow the original approach", line 588) | No (new market only) | No ("we do not have any previous research to directly compare") | No |
| 2016 Viotti | EPU and CDS | Wisniewski (2015) | Q1 | No (FE panel, not their VAR) | n/a | No (anchor gave no magnitude) | No |
| 2017 Hiller | Swedish muni puzzle | Goldreich et al. (2005); Liu et al. (2003) | Q1-lit | No ("Analogous to that of Goldreich et al.", line 1113) | n/a | No (sample size only) | No (institutional quirk) |
| 2017 Viotti | Unbundled fund costs | None ("to our knowledge, been studied before") | Q3 | No | n/a | No | No |
| 2018 Hiller | EV free parking | BLP; Verboven (methods) | Q3 | No | n/a | No | **Yes**: 2017 policy, 38 municipalities charging |
| 2018 Viotti | Intergroup bias | Brooks et al. (2014) | Q2 | No | n/a | Qualitative (70/30 split) | No |
| 2019 Hiller | Filing lag | Lindenberg & Ross tradition | Q3 | No | n/a | No | No |
| 2019 Viotti | Swedish value premium | Petkova & Zhang (2005) | Q1 | R2 ("Replicating Petkova and Zhang's framework", line 91) | **Yes**: iTraxx added | Qualitative: "similar to the results of Petkova and Zhang" (line 727) | No |
| 2020 Hiller | Leveraged ETFs | Tuzun (2014); Kyle & Obizhaeva | Q1 | R2 ("specifications, similar to Tuzun (2014)", line 885) | **Yes**: anticipatory flows, Corona period | Qualitative (line 678) | No |
| 2020 Viotti | Bank stocks and FOMC | English et al. (2018) | Q1 | **R1** ("replicating, with modifications", line 57; "replicating the baseline regression", line 103) | **Yes**: 2012-2019 sample | **Yes**: R² 0.099-0.103 vs 1.6-7% (lines 573-575, 1041) | No |
| 2021 Hiller | Covid press conferences | Busse & Green (2002) | Q2 | Method only ("We follow the methodology used by Busse and Green", line 456) | n/a | No | No (DiD only as a robustness check) |
| 2021 Viotti | Microstructure invariance | Kyle & Obizhaeva (2017, 2019) | Q1 | R2 | Partly (intraday, after Andersen et al.) | Qualitative ("we confirm the specific scaling laws") | No |
| 2022 Hiller | Crypto liquidity | Kyle & Obizhaeva (2017) | Q1 | R2 ("replicating the Kyle and Obizhaeva (2017)", line 1131) | **Yes**: time-series and intraday dimensions | **Yes**: R² vs K&O's 0.450 and 0.876 (line 1039) | No |
| 2022 Viotti | Ownership in the Covid crash | Baek et al. (2004) | Q1 | R2 ("The methodology is a replication of Baek et al (2004)", line 448) | **Yes**: identity × concentration | **Yes**: "0.20% compared to Baek's 0.28%" (line 512) | No |
| 2023 Hiller | FOMC cycle | Cieslak et al. (2019) | Q1 | **R1** ("we also replicate the results by Cieslak et al. (2019) for the original sample period", line 467) | **Yes**: post-sample, plus Board-meeting timing and hike-share controls | **Yes**: original sample +14 and +11 bp; post-sample -17 and -5 bp (lines 467-475) | No |
| 2023 Viotti | Wealth inequality | Gabaix et al. (2016) model | Q2 | Model extension | Yes (type dependency) | Parameters only (θ 5.51% vs 6.81%) | No |
| 2024 Hiller | French board quota | Ahern & Dittmar (2012) | Q1 | R2 ("methodology akin to Ahern and Dittmar (2012)", line 75) | **Yes**: board size and tenure | **Yes**: A&D's 3.56% and 1.9% vs own insignificant (lines 809, 842) | **Yes**: event study with US control, IV panel |

### 2.2 Claim (1): anchor question equals thesis question

**PARTLY VERIFIED: 12 strict, 17 broad.**
- Q1, 12 theses: 2011 Hiller, 2011 Viotti, 2016 Hiller, 2016 Viotti, 2019 Viotti, 2020 Hiller, 2020 Viotti, 2021 Viotti, 2022 Hiller, 2022 Viotti, 2023 Hiller, 2024 Hiller.
- Q1-lit, 5 more: 2012 Viotti, 2013 Hiller, 2013 Viotti, 2015 Viotti, 2017 Hiller.
- Q2, 3 theses: 2018 Viotti, 2021 Hiller, 2023 Viotti.
- Q3, 5 theses: 2014 Viotti, 2015 Hiller, 2017 Viotti, 2018 Hiller, 2019 Hiller.

The earlier figure of 15 needs three of the five Q1-lit cases to count; the list behind it was never published. The trend is the useful part: **from 2019 to 2024, 8 of 11 winners are strict Q1**, against 4 of 14 from 2011 to 2018.

Evidence quotes:
- 2016 Viotti: "the only published work on corporate credit risk is to our knowledge the study by Wisniewski (2015) ... we confirm that a positive relationship between economic policy uncertainty and CDS spreads exist, thus making the findings by Wisniewski et al. more robust" (lines 106-135).
- 2011 Viotti: "Our study has many similarities with the papers by Grundy et al. and Battalio and Schultz ... Grundy et al. (2010) and Battalio and Schultz (2009) focus on the U.S. event exclusively. This study, on the other hand, uses an international panel" (lines 183-190).

### 2.3 Claim (2): 9 of 25 are table-level replications

**COUNT VERIFIED; THE TWO RIDERS ARE NOT.**
- The 9 replicators: 2016 Hiller, 2019 Viotti, 2020 Hiller, 2020 Viotti, 2021 Viotti, 2022 Hiller, 2022 Viotti, 2023 Hiller, 2024 Hiller.
- Only two are R1, re-estimated on the anchor's own sample: 2020 Viotti (English et al.) and 2023 Hiller (Cieslak et al.). The other seven are transplants (R2). **Transplants win as often as strict replications.**
- "All from 2016 onward": the 2011 Hiller thesis reproduces Ahern and Dittmar's three-day CAR on the same announcement (22 Feb 2002) and states both numbers. It is a one-number replication, not a table, so the rider survives only under a narrow reading.
- "7 of 12 since 2019": the collection has 11 winners from 2019 to 2024 (one in 2024). By my coding 8 of the 11 replicate or transplant, and 5 of the 11 compare numbers strictly. I cannot reproduce 7 of 12 under any year cut.
- **Base rate of replication language** (`rep.py`; vocabulary only, reference lists cut; ETF "physical replication" false positives were checked and excluded, e.g. 3966). For 2019 to 2024, 5 of 11 winners against 89 of 264 non-winners (34%) state that they replicate a study or method (Fisher p = 0.52). Replication language does not discriminate. The non-winners that replicate a top-journal paper explicitly include:
  - 4441 ("we are going to replicate this study of the SPX", line 90);
  - 5277 ("we carry through a replication on the study of Cremers and Petajisto (2009)", line 205);
  - 5522 ("We replicate the methods used in the article 'Common Risk Factors In Cryptocurrency'", abstract);
  - 6812 ("Building on the methodology of Parise and Rubin (2025)", abstract).

### 2.4 Claim (3): six winners exploit a reform or threshold with a dated treatment and a control

**VERIFIED AS SIX; THE NON-WINNER RIDER IS FALSE.**
- The six:
  - 2011 Hiller: DiD, Norwegian firms against Swedish firms.
  - 2011 Viotti: staggered bans; "we rely solely on the removal of the bans in our difference-in-difference re-estimation".
  - 2012 Viotti: sharp RDD at the 100 SEK tick threshold.
  - 2013 Viotti: French FTT, 1 Aug 2012, comparable European securities as controls.
  - 2018 Hiller: the 2017 parking change, adopted by 38 municipalities.
  - 2024 Hiller: event study with "our control group of US firms" (line 809), plus IV.
- Only five are dated reforms; the 2012 RDD is a cross-sectional threshold. The 2017 muni thesis (institutional quirk) is close but has no control group.
- **Timing:** four of the six are 2011 to 2013. Since 2014 there are 2 of 19; since 2019, 1 of 11 (2024 Hiller).
- **Non-winners with dated reform or threshold designs.** A screen (≥3 identification terms; 58 of 635 non-winners against 5 of 25 winners, Fisher p = 0.08) followed by reading the abstracts confirms at least 10:
  - 1305: FESE tick-size cut on 7 Jun 2010, Wilcoxon and DiD.
  - 1661: round lot one on 13 Oct 2008, 223 treated and 115 control stocks.
  - 1955: Spanish covered short-sale ban, matched European controls.
  - 3454: green buses, RDD.
  - 3787: Covered Bond Issuance Act, DiD at five dates.
  - 4138: wind turbines, hedonic DiD.
  - 4701: MiFID II on 3 Jan 2018, DiD on analyst coverage.
  - 5286: mandatory sustainability reporting, DiD.
  - 6045: SFDR on 10 Mar 2021, Article 6/8/9 intensity.
  - 6821: CSRD 500-employee threshold, DiD.
  - At least five more are likely but NOT VERIFIED: 1462, 1482, 1650, 1875, 4420.
- 1305 and 1955 are topical twins of the 2012 and 2011 Viotti winners, and lost.
- The winner rate (6/25) is still far above this floor (≥10/635). But winners were coded by reading and non-winners by a screen, which inflates the gap. In the recent period it vanishes: 1 of 11 winners against at least 4 of 264 non-winners (4420, 4701, 5286, 6045).
- **JUDGEMENT:** a reform design was the winning archetype of 2011 to 2013. Since 2019 it has been neither necessary (10 of 11 winners lack one) nor sufficient.

### 2.5 Claim (4): the extension sits inside the anchor's tables

**VERIFIED FOR 8 OF THE 9 REPLICATORS, AND NOT DISCRIMINATING.**
- Inside the anchor's specification:
  - 2019 Viotti: iTraxx added to Petkova and Zhang's conditional regression.
  - 2020 Hiller: "we implement the regression specification for volatility in Tuzun (2014) and allow for C&R-flows as an additional control variable".
  - 2020 Viotti: post-crisis sample in English et al.'s regression.
  - 2022 Hiller: time-series and intraday dimensions.
  - 2022 Viotti: identity × concentration.
  - 2023 Hiller: Board-meeting timing and rate-hike share as controls.
  - 2024 Hiller: board size and tenure as outcomes.
  - 2021 Viotti: partly inside (a high-frequency version).
- The exception is 2016 Hiller, whose only extension is the market (Sweden).
- Non-winners that also extend inside the anchor's table: 5522 (adds a volatility factor to Liu, Tsyvinski and Wu's model, abstract), 4441 (post-publication period and OMX30 inside Lucca and Moench's design, line 90), 5277 (quantile regressions inside Cremers and Petajisto), 6812 (inside Parise and Rubin).

**The paired contrast** (2023 Hiller against 4441, both with d'Avernas as examiner). Both replicate a pre-FOMC return pattern on the original period and find it gone afterwards.
- 2023 Hiller tests a measured explanation inside the anchor's regression: "When controlling for both ... we find that the effect on daily excess return is consistent over both sample periods".
- 4441 compares pre- and post-publication means ("dropped from 0,323 to 0,055 for the SPX") and then offers an untested reading: "This is in line with the efficient market hypothesis ... investors should have taken advantage of the information made available by Lucca & Moench".
- **JUDGEMENT:** the extension that matters is one that tests a mechanism. Extending the period or country inside the anchor's table is common to winners and non-winners.

### 2.6 Claim (5): winners compare their numbers to the anchor's

**PARTLY VERIFIED.**
- Strict numeric comparisons, 6 of 25: 2011 Hiller, 2020 Viotti, 2022 Hiller, 2022 Viotti, 2023 Hiller, 2024 Hiller (quotes in the table in 2.1).
- Qualitative "similar to" or "in line with", 5 more: 2011 Viotti, 2012 Viotti, 2019 Viotti, 2020 Hiller, 2021 Viotti.
- Since 2019: 5 of 11 strict, 8 of 11 with the qualitative cases.
- Non-winners also compare: 4441 compares with Lucca and Moench's indices ("remarkably strong compared to other international indices studied by Lucca & Moench", line 729), and 5522 states "Liu, Tsyvinski, and Wu (2022) show significance for ten out of 24".
- **JUDGEMENT:** comparing numbers is good practice. This corpus cannot show that it discriminates.

### 2.7 Claim (6): over-claiming, 16% against 58%

**QUOTES VERIFIED; RATES NOT RE-CODED.**
- The four winner over-claims exist verbatim:
  - 2019 Viotti: "Although both alphas are statistically insignificant ... we see that the inclusion of our disaster risk proxy goes in the right direction".
  - 2021 Hiller: "the renowned Swedish Covid-19 strategy has been beneficial for some Swedish stocks".
  - 2022 Viotti: "it is the joint effect of ownership concentration and equity identity that impacts firm value".
  - 2018 Viotti: "predictor of access to venture funding" (line 1079).
- So do the milder winner cases: 2012 Viotti ("an increased tick size would thus not be recommended" on weak p-values) and 2024 Hiller ("a gender quota does not need to negatively affect", line 947).
- All 10 non-winner quotes checked exist: 4088, 5888, 6581, 4110, 5885, 4251, 6003, 6812, 5202, and the COBS reference in 6013 (only its existence was checked).
- One more non-winner of the same "tendency" type found in this run: 5737, "although not statistically significant, the pre-treatment difference in gross alpha ... was negative. Using conventional measures of skill, the results thus point to the conclusion that brown funds are more skilled".
- Taking the earlier counts as given, 4/25 against 19/33 gives Fisher p = 0.0025.
- Limits: one coder, unblinded to winner status; the 33-thesis sample includes 6338, which is flagged as awarded in 2026 (see 3.4).
- **JUDGEMENT:** this is still the strongest discriminator in the corpus, but it is about execution, not about which anchor to pick. For the anchor choice it translates into one question: does the design make the most likely result, a small or null effect, an informative finding?

### 2.8 Claim: "method-only anchors have not won the Hiller prize since 2021"

**TRUE ONLY FOR 2022 TO 2024.**
- The Hiller winners since 2021: 2021 (Q2, method-anchored: "We use the event study methodology suggested by Busse and Green"), then 2022, 2023 and 2024, all Q1.
- Hiller method-only or no-anchor winners from 2011 to 2021: 2015, 2018, 2019 and 2021, so 4 of 9. A run of three non-method winners then has probability (5/9)³ ≈ 0.17.
- The Viotti prize went to a model extension in 2023.
- **JUDGEMENT:** this is not evidence.

---

## 3. Examiners and tutors (from `roles_all.csv`, verified as in section 1)

### 3.1 Verified facts
- **Sabbatucci examined no thesis in the corpus.**
  - He tutored 20 theses, all non-winners: 3966, 4113, 4119, 4132, 4148 (2018); 5237, 5245, 5251, 5277, 5315 (2022); 5661, 5667, 5704, 5708, 5728, 5871, 5872, 5879, 5883, 5887 (2023).
  - The 2022 and 2023 tutees were examined by d'Avernas.
- **What his tutees' theses were like** (abstracts, plus `did_counts.csv` and `rep_counts.csv`):
  - Single-question empirical studies on Swedish, Nordic, EU or US equities. Topics: ETFs (3966, 5237), sustainable funds or ESG (4119, 5667, 5708), insider trading (5315, 5661), index revisions (4132), dividends (4113), earnings manipulation (4148), hedge funds in bubbles (5245), Google Trends (5251), active share (5277), policy uncertainty (5704), crash risk (5728), stocks against T-bills (5871), profit warnings (5872), geopolitical risk and inflation (5879, VAR), cash-flow distributions around recessions (5883, which cites "Sabbatucci (2022)"), herding (5887).
  - None uses DiD or RDD vocabulary: the identification count is 0 for all 20.
  - One explicit top-journal replication: 5277, Cremers and Petajisto (2009).
  - Most are correlational or event-study designs. None has a reform-plus-control design.
- **Klug:**
  - Tutor of 6238 (2024, transfer-learning CNN return prediction across 22 countries; examiner Baghai).
  - Co-tutor as a PhD student of 5522 (2022, "Cryptocurrency Return Predictors - A Replicative Reassessment", which replicates Liu, Tsyvinski and Wu (2022) and adds a volatility factor; examiner d'Avernas).
  - Thanked for econometrics or data help in 4631, 5299, 5474, 5517 and 5533. No winner.
- **Who examined the winners:**
  - D'Avernas examined 9 of the 11 winners from 2019 to 2024 (2019 Viotti and 2020 Viotti have no examiner line). He also examined about 222 non-winners from 2019 to 2024, so about 9 of 231 of his examinees won (≈4%).
  - Baghai examined 11 of the 2024 non-winners and all named examiners in 2025 to 2026, including 6338.
- **Who tutored the winners, 2019 to 2024** (crude name match):
  - Ebrahimian: 4 winners, 10 non-winners (Fisher p ≈ 0.001 against all other tutees).
  - Obizhaeva: 3 winners, 22 non-winners.
  - Sabbatucci: 0 winners, 15 non-winners (p = 1.0).

### 3.2 What this implies (JUDGEMENT)
- The prize corpus says nothing about Sabbatucci's preferences as an examiner. He is out of sample. Tailoring the design to "what wins" means tailoring it to d'Avernas-era juries and examiners.
- Winners and non-winners within a year shared the same examiner. So examiner identity cannot explain winning inside the corpus; tutor and cohort vary more. Ebrahimian's record (4 of 14) is consistent with tutor effects, or with strong students choosing him. These cannot be separated.
- What he values can only be inferred from the course material he wrote ("replication and extension", "do not chase statistical significance", "check the power", "simpler is better") and from his research. Per the briefing, his current working paper is on retirement plans shifting from active to passive and the effect on equity prices. That suggests he will notice whether a "flow" is mechanical or voluntary, and how it is measured. This is an inference, not evidence.

### 3.3 What it does not imply
- That a design close to his own working paper (C) is favoured. No thesis he examined exists to test this, and the briefing records no award rule that favours the examiner's topic.
- That his tutees' failure to win reflects his standards. Tutors are partly allocated, and prizes are decided by a jury whose membership I could not verify (NOT VERIFIED).
- That Klug prefers replication designs. One co-tutored replication is n = 1.

### 3.4 Label problems that limit every comparison
- 6338 (2025) is flagged in `non_winners/INDEX.md` as awarded in 2026. The catalogue record I printed has no award field, so this is NOT VERIFIED beyond the INDEX flag.
- The award status of the 2025 and 2026 cohorts is otherwise unknown. 6591, 6687, 6812 and 6821 are "non-winners" only by default.

---

## 4. Closest analogues for each design

Facts about the designs come from the SSZ dossier (A) and the briefing (B, C). Thesis facts are VERIFIED unless marked.

### 4.1 (A) SSZ replication on PPM before 2024, plus an FTN sponsor column

**Winners whose moves A can copy:**
- **2023 Hiller (FOMC):** "we follow as closely as possible the methodology and data sources of Cieslak et al. (2019)". It replicates on the original period, then extends with a regime change and tests the mechanism inside the same regression.
  - A's equivalent: SSZ Tables II, III and IX on pre-2024 PPM as the "no-sponsor regime". The FTN column of Table VIII (removal = -1, winners' transfers) is the regime change.
  - What A cannot copy: re-estimation on SSZ's own US data (R1). A is a transplant (R2), like 7 of the 9 replicating winners.
- **2020 Viotti (bank stocks):** puts the anchor's statistics next to its own and explains the gap ("weaker effect ... with roughly one quarter of the explanatory power ... relatively unsurprising, as we use daily returns").
  - A's equivalent: print SSZ's Table III coefficients beside the PPM ones. The dossier's PPM-ratio match makes this natural (mean / Q1 / median / Q3: 25.3 / 8.2 / 18.1 / 37.9 against SSZ's 25.38 / 8.50 / 19.85 / 35.52, per dossier).
- **2022 Viotti (ownership):** a transplanted replication with one added interaction and one side-by-side number ("0.20% compared to Baek's 0.28%").
- **2017 Viotti (Swedish fund costs):** a Swedish institutional first ("Sweden as early as 2015 being the first country to unbundle") made an otherwise unobservable fund characteristic measurable. Data were hand-collected from annual reports ("over 4000 datapoints").
  - A's equivalent: PPM's participant-only design before 2024 is the institutional fact that makes the sponsor switch observable. This is the answer to the course's "avoid the Nordic default".
- **2015 Hiller (fund-flow risk):** two hypotheses with distinguishable predictions; one rejected, one supported.
  - A's equivalent: the dossier's pre-registered signs (dossier §4.4). For example, a positive DC indicator for flow volatility after size controls would mean a sponsor is not necessary for DC volatility.

**Non-winners whose moves A must avoid:**
- **4439 (2019, d'Avernas tutor and examiner):** literally SSZ-type objects (flow-performance sensitivity, flow volatility) for Swedish sustainable against conventional funds, with three parallel purposes reported as a list. A must keep one question; Tables II and IX serve it and are not separate aims.
- **5277 (2022, Sabbatucci tutor):** a top-journal replication on Swedish funds plus quantile regressions; no new mechanism.
- **4441 (2019):** replication plus a new period and an untested explanation.
- **5522 (2022, Klug co-tutor):** replication plus an added factor.
- These three are the "SSZ on Swedish data" trap. The FTN column must be the headline, and the replication its control regime.
- **5737 (2023):** PPM data and a "difference-in-difference" around Covid, a period effect, with insignificant differences read as skill rankings. A must not call the pre/post comparison a DiD and must not read insignificant coefficients directionally.
- **1463, 4092, 2289 (PPM theses, 2012 to 2018):** descriptive group comparisons ("activity has a negative effect on the investor returns", 4092 abstract), "inconclusive" results (1463), and 16 strategies compared against the default (2289). PPM data alone do not make a winner.

**Most winner-like features of A (JUDGEMENT):**
- A same-question top-journal anchor (JF).
- Table-level transplant replication with a powered headline test: MDE 0.110 per year against an implied gap of about -0.20 (per dossier §0).
- The extension sits inside Table VIII.
- Numbers come in the anchor's units.

**Least winner-like features:**
- The policy part rests on 81 decisions in 6 rounds, with MDE 0.655 against SSZ's 0.674 (per dossier §0). That is the 4441-type risk of a new regime with a weak test.
- Many tables invite fan-out.
- The "participant-only before 2024" premise is contestable: the briefing says the 2019 platform tightening removed several hundred funds and moved non-choosers' capital to AP7 Såfa, which is itself sponsor-like.

### 4.2 (B) Cookson-style selection and outside-PPM flows

**Winners whose moves B can copy:**
- **2024 Hiller (French quota):** a reform, the anchor's own methods, a control group, and a null on every outcome explained by measured institutional differences ("French firms had six years ... softer punishment").
- **2018 Hiller (EV parking):** a policy change adopted by a subset of units, with the effect translated into a counterfactual magnitude ("led to a 2.85% reduction in total BEV sales").
- **2013 Viotti (French FTT):** splits one policy into components (STT against HFTT) with separate control sets. B's equivalent is separating announcement (selection news) from implementation (transfer).

**Non-winners whose moves B must avoid:**
- **6045 (2024, SFDR):** a dated reform with treatment intensity (Article 6/8/9), but four outcomes (demand, size growth, performance, value added). This is B's twin, and it lost.
- **6812 (2026):** a JF anchor, then a low-powered null turned into a regulatory claim ("depends on regulatory pressure and the ESG maturity of the market"). With 8 to 12% power on outside flows (per briefing), B's likely null is the same trap.
- **1305, 1955, 4701:** reform designs that did not win; the design archetype is not enough.
- **6687 (2026):** flows regressed on strategy adherence with IV ("suggestive evidence"). This is the calibrated version, award status unknown.

**Most winner-like features of B (JUDGEMENT):**
- A dated, staggered treatment with natural control groups (losing bidders, not-yet-procured categories), like the 2011, 2013, 2018 and 2024 reform winners.
- A close fit with Klug's prompt ("exact policy/selection design").
- A powered selection logit (per briefing).

**Least winner-like features:**
- No table-level replication is possible (no UK platform data; NOT VERIFIED beyond the briefing).
- The headline outside-flow test is badly underpowered.
- Swedish-fund flows must be imputed from TNA: per the briefing, only 32% of Swedish fund-months show a nonzero SHoF net flow.
- Two questions unless one is dropped.
- The "own brands" half of Cookson has no FTN analogue.

### 4.3 (C) Da et al. price pressure

**Winners whose moves C can copy:**
- **2020 Hiller (leveraged ETFs):** the closest winner of the three designs. Mechanical, predictable flows; stock-level price and volatility impact on OMXS30 stocks; an anticipatory-trading extension; "Standard errors are clustered by date".
  - It won on a short intraday sample ("September 19, 2019 through April 20, 2020") with SHoF intraday data. A short post-period is therefore not fatal when the observations are many and the mechanism is sharp.
- **2015 Hiller (fund-flow risk):** flow-induced price pressure with a reversal test (Coval and Stafford; Lou).

**Non-winners whose moves C must avoid:**
- **6591 (2026, 24 pages):** fund flows and Swedish stock returns, fire-sale exposure, a reversal, then a bolted-on backtest that underperformed. It concludes with "direct evidence of non-fundamental pricing dynamics".
- **5202 (from the earlier analysis, not re-read):** three shared event dates and window fishing. C has three events (per briefing).
- **4132 and 5237 (Sabbatucci tutees):** an index-revision event study and ETF price informativeness. These are adjacent topics and were not winners.

**Most winner-like features of C:**
- One question.
- A mechanism matching the 2020 Hiller winner.
- An anchor question equal to the thesis question (pension reallocations moving prices).

**Least winner-like features:**
- No replication independent of FTN.
- Three events.
- Within-category netting never computed: removed funds sell what winners may buy.
- Doses are small: a median inflow of 6% of AUM, per briefing.
- Holdings data cover only four FI quarters.
- No power analysis.

---

## 5. Evidence-weighted rubric

Weights: **3** = backed by the course rules and by verified corpus patterns, or the strongest tested discriminator; **2** = common among (recent) winners or course-backed, but shown not to discriminate or shown only in one matched pair; **1** = plausible, little corpus evidence. Scores run from 0 to 5.

| # | Criterion | Weight | Evidence basis | A | B | C |
|---|---|---:|---|---:|---:|---:|
| 1 | Same-question anchor from a top journal | 2 | 8 of 11 winners 2019-2024 (2.2); common in non-winners too | 4 | 3 | 4 |
| 2 | Table-level replication with the anchor's numbers alongside | 3 | Course rule ("replication and extension"); 8 of 11 recent winners; not discriminating (2.3, 2.6) | 5 | 2 | 1 |
| 3 | The extension tests a mechanism inside the anchor's specification, not just a new country or period | 2 | 2023 Hiller against 4441 (2.5); course: "extension needs to be meaningful", avoid the Nordic default | 4 | 2 | 2 |
| 4 | One headline question | 2 | Earlier script metric (69% against 39%, p = 0.04, not re-verified); course "Simpler is better"; counter-examples 2013 Hiller, 2017 Viotti | 3 | 3 | 4 |
| 5 | The likely result is informative (powered, or bounded against an anchor-sized effect), so the conclusion can be calibrated | 3 | Strongest discriminator (2.7); course: "interesting independently of the results", "check the power" | 4 | 2 | 1 |
| 6 | Identification from the institution (dated reform or threshold with control, or an institutional quirk) | 2 | 6/25 winners against ≥10/635 non-winners, but 1/11 since 2019 (2.4) | 3 | 4 | 3 |
| 7 | Avoids documented non-winner failure modes (fan-out, period dummies as "treatment", bolted-on strategies, underpowered nulls over-read) | 2 | Non-winner twins in section 4 | 3 | 2 | 2 |
| 8 | Institutional or unique data named | 1 | Earlier analysis §3.7; 2017 Viotti, 2020 Hiller; but PPM non-winners 4092, 5737 | 5 | 4 | 2 |
| 9 | Fit with the tutor's topic prompt | 1 | No corpus evidence; practical | 3 | 4 | 3 |

**Justifications (JUDGEMENT; design facts per dossier or briefing):**

1. A asks SSZ's sponsor question with the sponsor switched on. That is a reframing, since SSZ compare DC and non-DC money cross-sectionally; hence 4, not 5. B re-asks Cookson's "does a gatekeeper's selection move money, and on what does it select", minus own brands: 3. C asks Da et al.'s pension-reallocation price-pressure question almost exactly: 4.
2. A can replicate SSZ Tables I, II, III and IX (dossier §7), and its PPM ratio reproduces SSZ's distribution. B has no independent replication sample; its selection logit is a Cookson-style table on new data, so 2. C has none: 1.
3. A's FTN column in Table VIII tests a sponsor's loading on past returns, a mechanism. B's and C's "extension" is the whole thesis.
4. A has one question but many tables (risk). B has two questions. C has one.
5. A's replication is powered (MDE 0.110 against about -0.20), and its FTN column at least excludes SSZ-sized sponsor sensitivity (MDE 0.655 against 0.674): 4. B's headline has 8 to 12% power, so only the selection logit is informative: 2. C: no power analysis, three events, netting unknown: 1.
6. B has dated staggered awards with natural controls: 4. A's extension is a cross-section of 81 dated decisions, with pre-2024 PPM and non-procured categories as controls: 3. C is dated but confounded by netting: 3.
7. A risks fan-out and the 4441/5277/5522 reading. B risks the 6812/6045 pattern. C risks the 6591/5202 pattern.
8. A: Pensionsmyndigheten files 2001-2026 and FTN reports, already parsed. B: the same, but outside flows must be imputed. C: four FI holdings quarters.
9. Klug's prompt lists "fund supply, quality, fees, investor behaviour or market efficiency" and "exact policy/selection design". B hits selection; A hits investor behaviour; C hits market efficiency and Klug's own index-price-pressure research. The prompt's emphasis (selection design) tips B.

**Totals:**

| Weighting | A | B | C |
|---|---:|---:|---:|
| Evidence-weighted (max 90) | 69 (77%) | 48 (53%) | 41 (46%) |
| Equal weights (max 45) | 34 (76%) | 26 (58%) | 22 (49%) |
| Identification-heavy (c6 weight 4, c2 weight 1) | 65 (72%) | 52 (58%) | not computed |

B overtakes A only if criteria 2 and 5 are weighted near zero and criteria 6 and 9 dominate. That contradicts the two best-supported criteria.

**What the evidence cannot show:**
- **Causation.** The features correlate with winning in 25 cases. Copying them does not cause a prize; cohort competition, execution and jury taste are unobserved.
- **Grades.** The corpus records prizes, not grades. A non-winner can be a top grade.
- **The examiner.** No thesis examined by Sabbatucci exists in the corpus (3.1). The prize jury's composition is NOT VERIFIED.
- **Labels.** 6338 is probably awarded, and 2025 to 2026 award status is unknown (3.4).
- **Coding asymmetry.** Winners were read in depth; non-winners mostly through screens and abstracts. Single coder, unblinded. Reform-design and replication rates for non-winners are floors.
- **The designs themselves.** The power, data and replicability facts behind the A, B and C scores come from other agents' work (SSZ dossier; briefing). If those change, the scores change.
- **Small n.** With 2 prizes a year, any year-specific pattern (such as the "since 2021" streak) is noise-level.

---

## 6. Why the winner is the winner

**The argument for A (JUDGEMENT, built on the verified patterns above):**
1. **It meets the stated standard in the form recent winners did.** The course defines the BSc standard as "replication and extension of a (recent) published paper in a top journal". From 2019 to 2024, 8 of 11 winners replicated or transplanted an anchor's specification (2.3), 6 of them as transplants on new data, as A would. Of the three designs, only A can do this at table level, and the dossier shows the headline replication test is powered.
2. **Its extension is the kind that separates winners from look-alikes.** In the one clean matched pair, the 2023 FOMC winner tested a measured mechanism inside the anchor's regression, while 4441 stopped at a new period and an untested story. A's extension (the FTN column of Table VIII) tests a mechanism, sponsor presence, inside SSZ's own table. It is not "SSZ on Swedish data".
3. **Its most likely result is still a finding.** Calibration is the strongest discriminator in the corpus (2.7). A's replication is powered against the effect SSZ's estimates imply. Its FTN column, if null, still excludes SSZ-sized sponsor sensitivity and is written as a bound. The signs are pre-registered (dossier §4.4). The 2024 and 2023 Hiller winners show that a null explained with measured institutional facts wins.
4. **It absorbs B's best part.** The powered half of B, the selection regression of winning on past rank, sits inside A's Table VIII (dossier §0, §4.3). B's unpowered half (outside-PPM flows) does not need to be the headline.
5. **Its data exist and are parsed.**

**The strongest counter-argument (for B, against A):**
- A carries exactly the package that lost in 4441 (2019), 5277 (2022, a Sabbatucci tutee), 5522 (2022, a Klug co-tutee) and 6812 (2026): a top anchor, replication on new data, an extension inside the table, and numbers compared.
- The corpus therefore shows that package is not sufficient. The course explicitly warns against "applying the question to Nordic countries unless meaningful".
- A's policy-relevant part rests on 81 decisions in 6 rounds and is powered only against effects at least as large as SSZ's US sponsors.
- B, by contrast, is the winners' identification archetype (2011 Hiller, 2011 and 2013 Viotti, 2018 and 2024 Hiller). It answers Klug's prompt directly ("exact policy/selection design"), and its selection test is powered.

**Why the counter-argument does not overturn A (JUDGEMENT):**
- B's headline test has 8 to 12% power, so B's most likely result is an uninformative null. That fails criterion 5, the best-supported criterion, and is the 6812 failure mode.
- The reform archetype has won once in the last 11 prizes, and at least 10 non-winners used it.
- B's selection test can be housed in A. So the real choice is "A with B's selection test" against "B without a replication".

**What would flip the decision to B:**
- If outside-PPM flows can be measured with at least 50% power, for example from Luxembourg share classes with daily flows (90% nonzero per briefing). Not verified.
- If the pre-2024 "no sponsor" premise collapses: the 2019 removals cannot be separated.

**Risks of A, with mitigations:**

| Risk | Mitigation | Effect |
|---|---|---|
| Read as "SSZ on Swedish data" (the 4441/5277/5522 pattern) | Make the one-sentence question the sponsor switch. Put the FTN Table VIII column and the regime column in the first results table, with the pre-2024 replication as the control regime. Justify Sweden by the participant-only institution, not by novelty. | Reduces |
| FTN column null and marginally powered (n = 81, MDE ≈ SSZ size) | Pre-register sign and MDE. Report the confidence bound in SSZ's units. Phrase as "excludes sponsor sensitivity of SSZ's size". Add the R6 transfers when published (dossier: about 100 decisions; NOT VERIFIED). | Reduces (n cannot be raised) |
| Fan-out across Tables I, II, III, VIII and IX and the regime column | One pre-specified headline test (dossier: the linear-rank difference). Table II and the Table IX FTN rows as secondary exhibits, with no separate aims. | Solves, if enforced |
| The 2019 platform tightening was sponsor-like before 2024 | Exclude the 2019 removal months and funds from the "no sponsor" regime. As robustness, treat 2019 as a second sponsor episode (removals to AP7 Såfa). | Reduces |
| Over-claiming in the conclusion (the strongest discriminator) | Write the conclusion from the tables: coefficient, SSZ's coefficient and the identification limit in the same sentence (the earlier conclusions document, pattern (a)/(b)). | Solves (under the authors' control) |
| Examiner preferences unknown (out of sample) | Write to his course rules: power, no significance chasing, simplicity, a meaningful extension. | Solves what can be solved |
| Cohort competition in 2026 unknown | None | Not mitigable |

---

## Appendix: files

All in `scratchpad/anchor_final/round1/audit_work/` unless noted.

- `roles.py`, `roles_all.csv`: tutor and examiner roles; verified against a raw grep.
- `did.py`, `did_counts.csv`: identification vocabulary (case-sensitive, so it does not match "did").
- `rep.py`, `rep_counts.csv`: explicit replication statements (new in this run).
- `intro.py` (abstract, introduction and conclusion extractor) and `q.py` (phrase search on flattened text), both new in this run.
- `cmp.py`, `cmp2.py`, `peek.py`: earlier pointers, reused.
- `../examiners_nonwinners.json`: earlier examiner extraction; agrees with `roles_all.csv` within 4 theses.
