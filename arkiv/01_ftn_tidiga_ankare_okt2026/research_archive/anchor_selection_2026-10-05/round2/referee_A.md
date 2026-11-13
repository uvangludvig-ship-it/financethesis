# Referee report on candidate (A): Sialm, Starks and Zhang (2015) as anchor

Round 2, 5 October 2026. Role: hostile but fair examiner. Target: `round1/ssz_dossier.md` and `round1/ssz_work/`.
My scripts are in `scratchpad/anchor_final/round2/refA/` (`v_nt.py`, `v_nt2.py`, `v_samples.py`, `v_mde.py`, `v_exits.py`, `v_exits2.py`). They use my own OLS (numpy) and print standard errors only, never a replication or extension coefficient. Labels: CONFIRMED, CORRECTED (with the right number), UNVERIFIABLE; JUDGEMENT marks my reasoning.

---

## 0. Verdict in brief

- **The data work holds up.** "Handel, netto" is the monthly net SEK flow. The Table III sample counts, the PPM-ratio distribution and the main MDEs (0.110 per year, 0.0059 per month, 0.655, 0.436) all reproduce with independent code.
- **Several load-bearing numbers and inferences are wrong.**
  - The 2019 exit capital: SEK 87.7bn, not 60.9bn.
  - The December placement: about SEK 16 to 19bn into chosen funds, not 47 to 51bn. The larger figure includes AP7.
  - The "implied gap of -0.20": the OLS-equivalent is -0.17, and it is not an SSZ estimate.
  - The "6 rounds, 5 award dates": there are 4 award dates.
  - "About 80% power against an SSZ-sized sponsor": about 57% even on the dossier's own benchmark, and 10 to 20% against plausible selection.
- **The dossier's framing does not survive.** "What happens when a sponsor is introduced" is answered by the FTN column. That column is in effect a survival regression. It mixes fund companies' decisions to bid with FTN's choices, and it recovers the correlation of a published scoring rule with 12-month returns. It does not test SSZ's mechanism, and it is powered only against near-perfect return-based selection.
- **The replication core is sound.** Read as an out-of-sample test of SSZ's attribution ("is DC money performance-sensitive without a sponsor?"), it is the only powered, table-level component among the candidates.
- **Recommendation.** (A) stays the anchor only in the reframed form of section 5. If the team requires FTN to be the headline, (A) loses its advantage and the choice should be reopened.

---

## 1. Verification of load-bearing claims

| # | Dossier claim | Status | My result and source |
|---|---|---|---|
| 1 | Table III, 1-year: DC 1.194 / 0.236 / 1.776; non-DC 0.328 / 0.284 / 0.487; difference 0.866 / -0.049 / 1.289; N 3,851 | **CONFIRMED** | PDF p. 17 (journal p. 820), read as an image. The 5-year columns also match (DC 0.845 / 0.421 / 0.619; non-DC 0.096 / 0.281 / 0.102). |
| 2 | Table VIII, P&I sample: sponsor 1.050 / 0.310 / 1.389; participant -0.004 / 0.156 / 0.194; N 2,815. 11-K sample: sponsor 0.786 / 0.380 / 0.718; participant -0.013 / 0.135 / 0.026 | **CONFIRMED** | PDF p. 28 (journal p. 831, rotated table). |
| 3 | Footnote 6: "When a fund is replaced, the plan assets are typically transferred to the new fund" | **CONFIRMED** verbatim | PDF p. 4 (journal p. 807), with the Deloitte 43% sentence before it. |
| 4 | SSZ Table I DC ratio: 25.38 / 8.50 / 19.85 / 35.52 (mean, Q1, median, Q3) | **CONFIRMED** | PDF p. 10 (journal p. 813). |
| 5 | "Handel, netto" (`nt`) is the month's net SEK flow | **CONFIRMED** | `v_nt.py` uses the *other* agent's parse (`audit/pa_panel_2023_2026.csv`) and my own ISIN-to-performanceId link (95.7% linked). For holdings above SEK 200m, the median gap to the identity mv_t - mv_{t-1}(1+R) is 0.015 / 0.019 / 0.020% (2023 / 2024 / 2025) and 0.50% in 2026. `v_nt2.py` (2018 to 2023, own link): 0.017 to 0.032%. The median monthly flow is 0.6 to 0.9%, so the gap is about 3 to 5% of a typical flow. The dossier's upper bound of 0.030% is exceeded only in 2020 (0.032%), which is immaterial. |
| 6 | December placement is in `nt`, "aggregate +47 to +51bn every December" | **CORRECTED** | Those totals include AP7, whose `nt` fails the identity. Into non-AP7 funds, December `nt` is SEK 17.6 / 18.9 / 16.7 / 16.7 / 16.7 / 16.2 / 16.3bn for 2019 to 2025 (29.4bn in 2018). Against non-AP7 capital of about SEK 1.0 to 1.3tn, that is roughly 1.3 to 2.5% a year. AP7's own December `nt` is 22.8 to 35.0bn. |
| 7 | PPM ratio 25.3 / 8.2 / 18.1 / 37.9% | **CONFIRMED** | On the dossier's 651 fund-years (mv_t / tnafund_t, `t3_annual_sample.csv`). My own build from `ppm_shof_flows.csv` (669 fund-years, 166 funds) gives 24.8 / 7.8 / 17.2 / 37.6. |
| 8 | Table III samples: annual 635 fund-years over 160 funds; monthly 8,033 over 199 funds (59 months, Feb 2019 to Dec 2023) | **CONFIRMED** | `v_mde.py` regressions: N 635 with 160 clusters; N 8,033 with 199 clusters. The pre-regression files hold 651 / 163 and 8,241 / 201. The drop comes from singleton category-years in the style-flow control. |
| 9 | MDE 0.110 per year (linear Table III difference); 0.0059 per month | **CONFIRMED** | SE 0.0393, MDE 0.1101; monthly SE 0.0021, MDE 0.00589. The annual SE is robust to clustering by category (17 clusters: MDE 0.094) and by category-year (78: 0.098). Excluding 2019: MDE 0.101 (N 512). Excluding December months: MDE 0.0059. Piecewise annual MDEs: 1.033 / 0.179 / 0.652, as the dossier reports. |
| 10 | FTN sponsor-flow slope MDE 0.655, N 81 (62 removed, 19 incumbent winners); LPM MDE 0.436 | **CONFIRMED** (arithmetic) | HC1 SE 0.234 and 0.156. Clustering by round (6 clusters) gives 0.278 and 0.197; with so few clusters, randomization inference is needed. |
| 11 | "About 80% power only against an SSZ-sized sponsor" (0.655 against 0.674) | **CORRECTED** | 0.674 is the secant slope (weights 0.2 / 0.6 / 0.2). A coefficient on a uniform linear rank weights the segments 6r(1-r), that is 0.104 / 0.792 / 0.104. SSZ's sponsor column is then **0.499**, and power is Φ(0.499/0.234 - 1.96) ≈ **57%**. The benchmark also has the wrong units (section 2, issue F1). |
| 12 | Implied PPM gap "about -0.20" | **CORRECTED** | Reproduced as the secant: participant 0.132 minus non-DC 0.333. The OLS-equivalent, comparable with the 0.110 MDE, is 0.143 - 0.310 = **-0.167**. It splices Table VIII's participant column (11-K plans in the P&I sample, N 2,815) with Table III's non-DC column (N 3,851), so it is an extrapolation, not an SSZ estimate. SSZ's own DC-minus-non-DC difference in OLS-equivalent terms is **+0.185** (secant 0.402). |
| 13 | File returns are integer-rounded | **CONFIRMED** | 100% of 15,064 `r_1m` and 14,975 `r_12m` values in linked 2018 to 2023 rows are integers. The annual Table III ranks use these: only 27 to 54 distinct prior-year returns for 126 to 140 funds per year. |
| 14 | 2019 exits: 348 funds, SEK 60.9bn | **348 CONFIRMED; capital CORRECTED** | `v_exits.py`: 348 funds first absent in 2019, with **SEK 87.7bn** of capital at last appearance. 16 reappear under a new fund number (SEK 3.6bn), so genuine exits hold 84.1bn. Mar to Jul 2019: 267 funds, 64.6bn. 60.9bn is not reproducible from any script in `ssz_work/`. The 348 equal 42% of the 814 funds listed in Dec 2018. |
| 15 | "6 rounds, 5 award dates" (risk 7) | **CORRECTED** | The N = 81 sample excludes R6 (`ftn_power.py`, line 11), so its 6 categories share **4** award dates (25 Mar 2024, 31 Oct 2024, 19 Feb 2025, 27 Aug 2025). |
| 16 | Allocation rule: equal split; incumbents keep capital and receive "upp till samma nivå" | **CONFIRMED** | FTN report of 25 Mar 2024, txt lines 417-425. The same text appears in all 11 reports. |
| 17 | (Cookson critique) 26 of 66 removed classes never bid; 2 belong to funds that won | **CONFIRMED from file, and understated** | `cookson_work/ssz_cross_section_fundlevel.csv`. **Inside N = 81:** 24 of the 62 "removed" never bid, 36 bid and lost, and 2 belong to winning funds. Spot check: "Nordea European Stars" (Nordea Funds Ab, SEK 3.2bn, coded never-bid and removed) is the same strategy as the R1 winner "Nordea 1 - European Stars Equity Fund (BP-EUR)" (report lines 84-98). SEB Europafond (removed) sits beside the winner SEB Europe Equity Fund; I did not verify that it is the same strategy. Handelsbanken Sverige A1 (SEK 2.6bn, removed) belongs to a family that won with Sverige Selektiv. |
| 18 | Winner "dose" in the sponsor flow | **CONFIRMED (new descriptive)** | Incumbent winners' sponsor flow: median 0.059, p25 -0.002, max 3.0 (winsorized at 1.30). Half of them received about nothing, so the dependent variable is roughly a binary removed/kept. |
| 19 | 2019 non-choosers' capital went to AP7 Såfa (dossier: "not re-verified") | **CONFIRMED indirectly** | In Mar to Jul 2019, `nt` was +26.1bn for AP7 Aktiefond and +3.0bn for AP7 Räntefond. Same-family mappings also appear: Swedbank Robur Access Global +7.8bn, Access Sverige +7.2bn, Access Europa +2.8bn. Pensionsmyndigheten (2020) gives the rule: at least SEK 500m of capital outside PPM, at least 3 years of return history, PRI signatory, and about 200 funds removed under the capital rule alone. |
| 20 | Course recency: "Read recent papers (<15 years)" | **CONFIRMED** | `course_intro.txt` line 165. The Nordic warning is at line 147. SSZ will be 11 years old at submission. |

Not verified by me: the Tran and Wang (2023) quote, the 158-citation search, and Table IX units.

---

## 2. Issues, classified, with fixes

### F1. FATAL for the dossier's framing (not for the anchor): the FTN column does not test SSZ's mechanism and is not powered against plausible effects

1. **The dependent variable is almost a survival dummy.** 62 of 81 values are -1, and the median kept fund's dose is 0.059. The "sponsor-flow slope" is therefore close to the LPM of being kept, with formula noise added.
2. **The units do not match SSZ.** SSZ's sponsor slope is an *annual* fund-level flow, aggregated over many independent plans in which most funds face no menu change in a given year (Table I: sponsor flow mean 9.68%, sd 74). FTN is a one-off review of a whole category.
   - The right yardstick is the slope under *perfect* return-based selection: **1.155** (`v_mde.py`, within-round step function with winners at the median dose).
   - The MDE of 0.655 is 57% of that.
   - Simulated with FTN's actual winner counts per round: a score-to-rank correlation of 0.5 gives a mean slope of 0.48 (power about 55 to 60%); a correlation of 0.25 gives 0.24 (power about 10 to 20%).
   - FTN's rule makes "Investeringsresultat" one of five quality subcriteria (75%), next to cost (25%). A low correlation is the plausible case.
3. **It mixes incumbency with bidding.**
   - 24 of 62 deletions are fund companies that chose not to bid, so the estimand is P(bid) × P(win | bid).
   - At least 3 deletions are strategy-level winners, families that bid with a sibling vehicle (Nordea, plus the 2 class-level cases). Coding their sponsor flow as -1 is wrong at fund level and mechanically biases the slope toward zero.
4. **It recovers a rule FTN published.** The quality and cost weights and the subcriteria are in every report, and FTN prints winners' 3-year Sharpe and information ratios. The regression measures how the output of a known, multi-criteria, interview-based rule correlates with returns. It cannot separate "rewards past returns" from "rewards process or fees that correlate with returns", and losers' bid fees are unobserved. SSZ's sponsors are discretionary fiduciaries with an unknown rule, which is what made their revealed loading informative.
5. **The dose is arithmetic.** Equal split plus the incumbent cap means the dose falls with the winner's prior PPM capital by construction. Regressing it on rank tests the formula, not FTN.
6. **The timing does not match FTN's information set.** The 12-month return is taken at the pre-award month. Bids are evaluated earlier, on 3-year history.
7. **Inference.** HC1 treats 81 decisions as independent across 6 categories and 4 award dates.

**Fix:**
- Demote the FTN column to a secondary, descriptive "new sponsor" column in Table VIII format, estimated at bid level in two stages:
  - P(bid | incumbent), N 87 (R1 to R4);
  - P(win | bid) on 36-month returns measured at the bid deadline: the 142 bids with returns from Cookson's file, plus the 3 all-qualified Swedish rounds as robustness.
- Code fund identity at strategy level.
- Use randomization inference within round.
- Report the result as a bound in the "perfect selection = 1.155" metric.
- Describe the dose rule; do not estimate it.

**Does the fix solve it?** It fully solves the misinterpretation, but not the power: the column remains a bounded description.

### S1. SERIOUS: "a sponsor is introduced" is two papers in one

- Paper 1 is a 2019 to 2023 within-fund comparison of PPM and non-PPM flow sensitivity (about 160 funds).
- Paper 2 is a 2024 to 2026 cross-section of 81 procurement decisions.
- They have different estimands, samples and identification. The only test of "introduction" itself is the regime column. That column re-expresses the same 81 decisions, with unwinsorized -1 rows making up 2.2% of rows, and its pre/post MDE is about 5 times the pre-period MDE (0.042 to 0.046 against 0.008 per month).

**Fix:** one question, the pre-2024 attribution test of section 5. FTN becomes one column (F1). Drop the regime column and the FTN Table IX as estimates; describe them in one paragraph. This fully solves the problem if enforced.

### S2. SERIOUS: PPM before 2024 is not participant-only

1. **2019 re-registration.**
   - 348 funds left (42% of the menu, SEK 84 to 88bn).
   - Non-choosers' capital went to AP7 (+29bn into AP7 Aktiefond and Räntefond, Mar to Jul 2019), and fund families mapped capital into sibling funds (+17.8bn into the Robur Access funds).
   - 2019 is one of the 5 joint annual cross-sections. 4.0% of its fund-years sit at the upper winsorization bound, against 2.3% in other years.
   - The survival rule required at least SEK 500m *outside* PPM, so the joint sample is selected on the comparison group's assets.
2. **Advice-driven switching.**
   - Robot "mass fund switches" were 75% of all 2011 fund switches; about 700,000 savers used management services; about 13,500 switches a day. All of this ended on 1 Dec 2011 (Pensionsmyndigheten, "Effekter av massfondbytesstoppet", 2012).
   - Advisory services continued: about 1 in 5 savers report using an adviser, and 4.6% of savers switched in 2021 (Pensionsmyndigheten 2022 situation report).
   - This matters most for the PPM-only panel B (2008 to 2023), and as a caveat on "participant" in 2019 to 2023.
3. **Mergers and family mappings** are sponsor-like flows initiated by fund companies, in every year. No merger link exists in the Morningstar master (briefing).
4. **The AP7 default.** Excluding AP7 is right. The default does select who the active choosers are, which affects interpretation only.

**Fix:**
- Drop flow-year 2019 from the joint sample. The cost is nil: MDE 0.101 at N 512. Report 2019 as a separate rule-change year.
- Start panel B in 2012, or split it at Dec 2011.
- Flag merger recipients: a same-company exit plus a `nt` spike in the same month. Drop those fund-years.
- Define "participant flow" as "participant or adviser", in the spirit of SSZ fn 18.

**Does the fix solve it?** It fully solves 2019 and reduces the rest.

### S3. SERIOUS: the non-PPM control is not "non-DC", and a negative gap does not discriminate between explanations

1. **What non-PPM money is.** In SEK-currency equity funds (137 of 166 funds Swedish-domiciled in my build), non-PPM money includes:
   - unit-linked occupational and private pension money (fondförsäkring, tjänstepension), whose fund menus are curated by insurers or procured, which is sponsor-like;
   - same-family fund-of-funds and allocation funds, which rebalance mechanically;
   - institutional mandates;
   - retail money.

   So PPM minus non-PPM is "participant-only DC minus a mix that contains sponsored DC". The composition of this capital is **NOT VERIFIED**.
2. **The asymmetry.** Under SSZ's mechanism the gap should be ≤ 0. Generic participant inertia or choice overload on an 800-fund menu (Cronqvist and Thaler; Dahlquist, Martinez and Söderlind) predicts ≤ 0 as well. Only a non-negative gap is diagnostic: it would mean a sponsor is not necessary.
3. **Direction of the contamination.** If non-PPM contains sponsored DC, a negative gap overstates the "no sponsor" effect.

**Fix:**
- Pre-register the asymmetric interpretation.
- Benchmark against SSZ's +0.185 (DC minus non-DC) and against SSZ's participant column, not against a spliced -0.17.
- Add a Table I row on the composition of Swedish fund capital by holder type, sourced from Fondbolagen or SCB (availability **NOT VERIFIED**).
- As robustness, drop funds of families with large in-house fund-of-funds.

**Does the fix solve it?** It reduces the problem only; it is the main residual risk.

### S4. SERIOUS: the powered headline test is not SSZ's test

- The linear rank coefficient puts 79% of its weight on the middle segment, where SSZ's DC-minus-non-DC difference is -0.049 and insignificant. SSZ's result (p. 807, p. 820) is in the tails.
- The SSZ-faithful tails are underpowered annually: Low MDE 1.03 exceeds SSZ's own 0.866, and High MDE 0.65 can detect SSZ's 1.289 but not the predicted -0.29.
- Monthly tails: Low 0.37 and High 0.47 per year (×12). These detect SSZ-sized tails but not the predicted PPM gaps.

**Fix:**
- Keep the linear coefficient as the pre-registered headline, stating openly that it is a summary measure.
- Print the piecewise table in SSZ's format with tail MDEs.
- Add one pre-registered tail contrast, (Low + High)/2 minus Mid.

**Does the fix solve it?** It fully solves the transparency problem; tail power stays limited.

### S5. SERIOUS: blind analysis is partial, and the "pre-registered" signs are an AI agent's, not the students'

- No coefficient was printed. I checked every `print` in `ssz_work/*.py`.
- Seen before §4.4 was written:
  - the raw annual flow sd (PPM 0.321 against non-PPM 0.179), which is Table II's object;
  - the winners' dose distribution;
  - the transfer-month non-PPM residuals for 19 winners (`reconcile.py`), which are point estimates of outside-PPM spillovers.
- Other agents have worked on the same data (`cookson_work/moments.py`, `da_work/`).

**Fix:**
- The students freeze and timestamp a pre-analysis plan (question, specifications, MDEs, signs, the asymmetric reading in S3) and send it to Klug before any coefficient is run.
- Treat Table II as descriptive.

**Does the fix solve it?** It fully solves the problem going forward; Table II cannot be un-seen.

### S6. SERIOUS: the "SSZ on Swedish data" trap (4441, 5277, 5522) and fit with the topic

- The powered part *is* SSZ on Swedish data. The dossier's defense, the FTN sponsor switch, is the weakest part (F1).
- Demoting FTN weakens fit with Klug's topic prompt and with the synopsis (FTN effects).
- 5277, a top-journal replication on Swedish funds, was tutored by Sabbatucci and did not win (winners audit §4.1).

**Fix:**
- Make the Swedish institution the test: a DC system without the mechanism that SSZ credit. State the predicted sign flip (SSZ: +0.185) and compare numbers in the same sentence.
- Present FTN as the policy that ended the participant-only regime, with its realized selection in one column.
- Clear the narrowed scope with Klug early.

**Does the fix solve it?** It reduces the risk; the outcome depends on the examiner's judgement.

### MINOR issues

| # | Issue | Fix | Solves? |
|---|---|---|---|
| M1 | December placement is mandated and allocated by savers' chosen weights (allocation rule **NOT VERIFIED**). At about 1.3 to 2.5% of capital, the mechanical return loading is of order 0.01 per unit of rank, well below the MDE. | Time FE; a monthly robustness check without December (MDE unchanged at 0.0059). | Fully |
| M2 | Wrong 2019 capital (60.9bn) and December totals (47 to 51bn). | Use 84.1 to 87.7bn and 16 to 19bn. | Fully |
| M3 | "5 award dates". | 4. | Fully |
| M4 | Annual ranks use integer-rounded file returns although SHoF `tri_sek` covers 2018 onward. | Rank on SHoF returns. | Fully |
| M5 | Monthly denominators differ: PPM `nt`/mv_{t-1} against non-PPM flow/[NP_{t-1}(1+R)]. | Use one definition. | Fully |
| M6 | FTN inference with 6 categories and 4 dates. | Within-round permutation. | Fully (validity); power falls |
| M7 | The PPM-ratio match with SSZ is a coincidence, helped by the SEK 500m external-capital floor. It carries no identifying weight. | Do not use it as an argument. | Fully |
| M8 | Recency: 2015 meets "<15 years". | Pair with Tran and Wang (2023 JFE) and Kronlund et al. (2021 JFE) in the literature section. | Fully (rule) |
| M9 | SEK-only sample, mostly Swedish-domiciled funds: external validity. | State it; add EUR funds once FX is available. | Reduces |
| M10 | Table II is thin: 96 funds, AR(1) MDE 0.174 against SSZ's 0.138. | Descriptive appendix. | Fully (by demotion) |
| M11 | Fan-out: Tables I, II, III, IV, VI, VII, VIII, IX, a regime column and an FTN Table IX. | Four exhibits (section 5). | Fully if enforced |

---

## 3. Re-score on the winners-audit rubric (section 5 of `winners_audit.md`)

| # | Criterion (weight) | Audit score for A | A as submitted, facts corrected | A, best version (section 5) | Justification |
|---|---|---:|---:|---:|---|
| 1 | Same-question anchor (2) | 4 | 4 | 4 | SSZ's sticky-or-discerning question, with the sponsor absent by institution. |
| 2 | Table-level replication (3) | 5 | 4 | 4 | Tables I, III and IX replicate. Table II is thin, the tails are underpowered annually, family size and turnover are missing, and 2019 must be dropped. Still the best of the three candidates. |
| 3 | Mechanism tested inside the specification (2) | 4 | 2 | 3 | The FTN column does not test SSZ's mechanism (F1). In the best version the mechanism test is the no-sponsor sign flip. |
| 4 | One headline question (2) | 3 | 2 | 4 | As submitted, two papers (S1). Best version: one question with secondary columns. |
| 5 | Informative likely result (3) | 4 | 3 | 4 | As submitted, the headline FTN test has about 57% power at best and 10 to 20% realistically. Best version: powered against SSZ's own +0.185 with MDE about 0.10. |
| 6 | Identification from the institution (2) | 3 | 2 | 3 | 2019, advisers and the non-PPM composition (S2, S3). Partly fixed. |
| 7 | Avoids non-winner failure modes (2) | 3 | 2 | 3 | Fan-out and the 4441 trap as submitted; reduced in the best version. |
| 8 | Institutional data (1) | 5 | 5 | 5 | `nt` validated independently. |
| 9 | Tutor-prompt fit (1) | 3 | 3 | 2 | FTN demoted, so further from Klug's prompt. |
| | **Weighted total (max 90)** | 69 (77%) | **53 (59%)** | **65 (72%)** | |
| | Equal weights (max 45) | 34 (76%) | 27 (60%) | 32 (71%) | |

The audit scored B at 48 (53%) and C at 41 (46%). The best version of A stays ahead, but by less than the audit claimed, and B's score must be revisited by its own referee. If the team insists on an FTN headline, A as submitted (59%) is close enough to B that the ranking should be redone with B's bid-level selection test scored as its headline.

---

## 4. Answers to the specific prompts (short)

- **Participant-only before 2024?** Not in 2019, and not before Dec 2011 (robot switching). It is approximately true for 2020 to 2023, after flagging mergers, with "participant" meaning "participant or adviser". See S2.
- **PPM against non-PPM confounded?** Yes. Non-PPM contains sponsored unit-linked pension money and fund-of-funds money, and survivors were selected on non-PPM size by the 2019 rule. The December placement is real but small for funds other than AP7 (M1). See S3.
- **One question or two papers?** Two as written. See S1.
- **Does the 81-decision column test SSZ?** No. See F1: equal split, incumbent cap, incumbency against bidding, a published rule, units, power.
- **Would the examiner see "SSZ on Swedish data"?** Likely, unless the headline is the no-sponsor sign-flip test with numbers compared to SSZ. See S6.
- **Recency and the Nordic default.** Recency is fine (11 years). The Nordic default is answered only by making the absence of a sponsor the test.
- **Power and blindness.** The MDEs reproduce. The 0.674 and -0.20 benchmarks are mis-specified (0.499 and -0.167; and the FTN units differ). No coefficients were seen, but Table II's raw object and spillover residuals were. See S5.

---

## 5. Best version of (A), at most one page

**Question (one sentence).** Sialm, Starks and Zhang attribute the high flow-performance sensitivity of US DC money to plan sponsors. Is DC money in Sweden's premium pension, which had no sponsor before 2024, less performance-sensitive than the non-PPM money in the same funds?

**Headline test (pre-registered, timestamped with Klug).**
- Specification: the Table III difference regression, PPM flow minus non-PPM flow, annual December-to-December, flow-years 2020 to 2023.
  - Ranks from SHoF returns.
  - Merger recipients dropped.
  - SSZ's controls minus family size and turnover.
  - Time FE; standard errors clustered by fund.
- Statistic: the linear-rank coefficient (summary measure).
- Hypotheses:
  - H_US: equal to SSZ's own DC-minus-non-DC difference, +0.185 (OLS-equivalent of Table III).
  - H_noSponsor: ≤ 0.
- MDE about 0.10, so the two hypotheses are separable.
- Interpretation, pre-committed: a gap ≥ 0 rejects "a sponsor is necessary"; a gap ≤ 0 is consistent with SSZ but also with generic inertia (S3).

**Tables (four exhibits).**
1. Summary statistics beside SSZ's Table I: PPM ratio, flows, sizes, fees. Add one row on who holds Swedish fund capital, if a source is found.
2. Table III replication: PPM, non-PPM and difference, in SSZ's piecewise format with tail MDEs, plus the linear headline and the tail contrast. Columns: annual 2020 to 2023 and monthly 2019 to 2023. SSZ's coefficients in a side panel. Robustness: December excluded; 2019 included; category-clustered SEs.
3. Table VIII analog, "the new sponsor": FTN's realized selection at bid level.
   - P(bid | incumbent) and P(win | bid) on 36-month and 12-month returns at the bid deadline; strategy-level identity; round FE; randomization inference.
   - Reported as a bound against perfect return-based selection (slope 1.155) and against SSZ's sponsor column (0.499 OLS-equivalent).
   - The equal-split dose rule described in the text.
4. Table IX replication: next-year raw and category-adjusted performance on lagged PPM and non-PPM flows.
5. Appendix: Table II (descriptive); 2019 as a rule-change year (SEK 500m external-capital rule; 348 exits); PPM-only panel 2012 to 2023.

**Residual risk.**
1. A negative headline gap is consistent with SSZ but not unique to SSZ's mechanism.
2. Non-PPM money contains some sponsored DC money.
3. The examiner may still read the thesis as a transplant.
4. The FTN column is a low-powered description: about 57% power against SSZ's sponsor column, much less against realistic selection.
5. "Participant" flows include adviser-driven switching.
6. Scope drift from the FTN topic in the synopsis, which needs Klug's agreement.

**Should (A) remain the anchor?** Yes, but only in this form. Its replication core survives independent verification, is powered against the anchor's own effect, and sits in SSZ's tables. The FTN extension, re-estimated at bid level, also contains (B)'s one powered test. The dossier's own framing ("a sponsor is introduced", with the FTN column as headline and "80% power") should not go forward. If the team or Klug insists that FTN must be the headline, (A) loses its rubric advantage and the decision should be reopened, since that headline is (B)'s selection test.

---

### Sources used beyond the dossier
- Pensionsmyndigheten (2012), "Effekter av massfondbytesstoppet": https://www.pensionsmyndigheten.se/content/dam/pensionsmyndigheten/blanketter---broschyrer---faktablad/publikationer/svar-p%C3%A5-regeringsuppdrag/2012/Effekter%2Bav%2Bmassfondbytesstoppet%2B120919.pdf
- Pensionsmyndigheten (2020), "Utvärdering skärpta krav fondtorget": https://www.pensionsmyndigheten.se/content/dam/pensionsmyndigheten/blanketter---broschyrer---faktablad/publikationer/svar-p%C3%A5-regeringsuppdrag/2020/Utvardering-skarpta-krav-fondtorget.pdf
- Pensionsmyndigheten (2022), "Dyra råd är inte alltid goda" (situation report on the sale of advice): https://www.pensionsmyndigheten.se/content/dam/pensionsmyndigheten/blanketter---broschyrer---faktablad/publikationer/rapporter/2022/Lagesrapport-om-forsaljning-av-rad-inom-premiepensionen.pdf
- SSZ PDF pp. 4, 10, 17, 28 (journal pp. 807, 813, 820, 831), read as images.
- FTN report of 25 Mar 2024 (`scratchpad/ftn_txt/`), lines 84-98 and 417-425.
