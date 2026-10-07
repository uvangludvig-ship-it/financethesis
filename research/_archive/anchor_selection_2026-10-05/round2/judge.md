# Final judgement: anchor and design for the FTN thesis

Round 2 judge, 5 October 2026. Inputs read in the order set by the brief. My scripts are in `round2/judge/` (`j1_exits_dec.py`, `j1b.py`, `j1c.py`, `j2_tranches.py`, `j3_fip.py`, `j4_mde.py`). They print counts, SEs, MDEs and descriptive moments only, never a replication or extension coefficient. Labels: CONFIRMED / CORRECTED for the referees' claims; VERIFIED / JUDGEMENT / NOT VERIFIED elsewhere.

## 0. Decision

- **Anchor: Sialm, Starks and Zhang (2015), in referee A's reframed form (`referee_A.md` §5), with three changes of mine:**
  1. a scale-robust hypothesis;
  2. a pre-registered monthly precision check;
  3. the "did PPM need a sponsor?" framing, which puts FTN in the question without giving it the headline.
- **Rubric after all corrections:**
  - A reframed: 66/90 (73%).
  - A plus a C figure: 63 (70%).
  - C best version: 53 (59%), or 47 if the Chilean replication fails.
  - A as submitted: 53 (59%).
  - B best version: 44 (49%).
- **The top choice survives my attack**, on three conditions: Klug signs off on the narrowed scope; the non-PPM composition caveat is pre-registered; the SHoF pre-2018 request goes out this week.
- **No FTN-centred headline is powered under any candidate** (section 5). Reopening the choice because "FTN must be the headline" would not help: B's headline is the same bounded selection test that A already carries as a column.

## 1. Spot-checks of the referees (8 checks)

| # | Referee claim | Verdict | My evidence |
|---|---|---|---|
| A1 | 2019 exits hold SEK 87.7bn, not 60.9bn | **CONFIRMED.** I also found the source of the 60.9bn. | `j1b.py`: 348 funds are first absent in 2019. Their capital in the month before first absence sums to 60.9bn only because 53 of them have an empty placeholder row (NaN name, mv and nt) in their final month in `ssz_work/ppm_panel_all.csv`. Using the last non-missing mv gives 87.7bn. Example (`j1c.py`): Swedbank Robur Småbolagsfond Norden held SEK 2.57bn in Apr 2019 with nt of -23m, followed by an empty May row. The net figure of 84.1bn (16 renumberings) is per `referee_A.md` §1 item 14; I did not re-check it. The "about SEK 61bn" in `da_dossier.md` §3.3 is probably the same artifact (not checked). |
| A2 | December placement into non-AP7 funds is SEK 16 to 19bn | **CONFIRMED** | `j1_exits_dec.py`. Non-AP7 December nt: 29.4 (2018), then 17.6 / 18.9 / 16.7 / 16.7 / 16.7 / 16.2 / 16.3 (2019 to 2025). AP7: 22.2 to 35.0. Non-AP7 November nt runs from -2.9 to +0.3, so the December excess is the placement. As a share of non-AP7 December capital it is 2.2% (2019) falling to 1.2% (2025), so referee A's "1.3 to 2.5%" is slightly off at the low end (minor). |
| A3 | SSZ's OLS-equivalent DC-minus-non-DC slope is +0.185 | **CONFIRMED** | 0.104 x 0.866 + 0.792 x (-0.049) + 0.104 x 1.289 = 0.185, against a secant of 0.402. Other OLS-equivalents: sponsor 0.499, participant 0.143, non-DC 0.310; the spliced gap is -0.166 (`j4_mde.py`). |
| A4 | Uniform-rank weights 0.104 / 0.792 / 0.104 | **CONFIRMED** analytically | For r ~ U(0,1), the OLS slope of f(r) on r equals the integral of f'(r) x 6r(1-r). Integrating 3r²-2r³ over each segment gives 0.104 / 0.792 / 0.104. The weights assume uniform ranks. The integer-rounded file returns create ties (`referee_A.md` item 13), so ranks must come from SHoF returns. |
| B1 | Saver letters arrive after the award+1 window | **CONFIRMED where checkable**; NOT VERIFIED for R1 and R3 | Sweden active: Dagens PS, 8 Oct 2025 (fetched), letters "I månadsskiftet", i.e. award +2/+3. Sweden small cap: EFN, 3 Sep 2026 (fetched), switch deadline 25 Sep 2026, i.e. award +4. Dagens PS, 21 Mar 2025: letters "just nu", category not named, consistent with R2 at award +5. The FTN R1 report §3.7.1 (txt L427-436) says only "I samband med att en upphandling är avslutad". The 85 to 95% default share is confirmed at press level (Dagens PS, 8 Oct 2025). |
| B2 | Staged transfers of 20 to 60% pass the -60% filter | **CONFIRMED** on a different source panel | `j2_tranches.py` on `audit/pa_panel_2023_2026.csv` (referee B used `ppm_shof_panel.pkl`): 26 post-award months with -60% < nt/mv_{t-1} < -20%, in 16 of 66 removed funds holding SEK 46.3bn of 74.0bn, at event months 2 to 9 and none at month 1. These months carry SEK 23.0bn of outflow, against 21.3bn in months at -60% or below. Only 29% of last-observed months are at -60% or below (referee: 31%). So the a+1 window is free of tranches; a+2 and any letter-time window are not. |
| C1 | Meds Apotek / Edge leverage | **CONFIRMED** | `j3_fip.py`. Meds Apotek carries 41.4% of squared S1 net FIP, with simple leverage 0.415 (0.385 after partialling out log market cap). Edge buys 100%, 100% and 76% of three of the top four stocks. Edge's Q1 and Q2 weights correlate 0.39. With Edge buying nothing (S7), the residual sd is 0.490. |
| C2 | Residual net-FIP sd 0.509 on Q2 holdings (S6) | **CONFIRMED** with my own aggregation of `holdings_2026q2.csv` | 178 stocks matched, covering 96.1% of gross SEK. S1: residual 0.750, with Upsales at +6.79 pp as the tail stock. S6: residual **0.509**. |

Additional checks (`j4_mde.py`, SEs only):
- Headline annual MDE excluding 2019: 0.101 (N 512, 153 fund clusters). CONFIRMED.
- Monthly MDE excluding 2019: 0.0733 per year (N 6,559, 169 funds). New.

## 2. Disagreements that matter, and rulings

| # | Disagreement | Ruling and reason |
|---|---|---|
| 1 | 2019 exit capital: 60.9bn (`ssz_dossier.md` §3.1) against 87.7bn (`referee_A.md` item 14) | **87.7bn gross, 84.1bn net.** The 60.9bn is a placeholder-row artifact (A1). Drop the empty rows before dating any exit. |
| 2 | December placement: 40 to 52bn (`da_dossier.md` §3.3; `ssz_dossier.md` §3.2) against 16 to 19bn | **Both are true for different scopes.** Use 16 to 19bn for chosen (non-AP7) funds. C's conclusion that December gives no powered replication only gets stronger. |
| 3 | Benchmarks: implied gap -0.20 and FTN target 0.674 (dossier) against -0.167, +0.185 and 0.499 (referee A) | **Referee A.** The linear-rank coefficient weights the segments 0.104 / 0.792 / 0.104, not 0.2 / 0.6 / 0.2 (A3, A4). |
| 4 | Power of the FTN column: "about 80%" (dossier §5) against 57% against SSZ, and 10 to 20% at a score-rank correlation of 0.25 (`referee_A.md` F1) | **Referee A.** The dependent variable is close to a survival dummy (62 of 81 values are -1), and the perfect-selection slope is 1.155. |
| 5 | "6 rounds, 5 award dates" | **4 award dates** for N = 81 (`referee_A.md` item 15). |
| 6 | The FTN selection sample conditions on incumbency, not on bidding | **Cookson dossier §7.1 and referee A F1.** 24 of the 62 removed funds never bid. Use a two-stage design: P(bid \| incumbent), then P(win \| bid), with strategy-level identity. |
| 7 | Test (iv) as B's headline: MDE 0.77 to 1.51% (`cookson_dossier.md` §5) against 1.59 to 2.15% at event level, with the window before the letters (`referee_B.md` §2) | **Referee B** (B1 and B2 confirmed). Drop (iv). |
| 8 | Selection benchmark: 77% power against CJJM's Table 4 gap (Cookson dossier) against about 5% against CJJM's Table 5 addition coefficients (`referee_B.md` §3.4f) | **Neither benchmark fits.** Table 4 is a stock gap. CJJM's addition logit belongs to conflicted platforms with star controls, while FTN's rule puts track record inside a 75% quality score (`ssz_dossier.md` §3.5). Benchmark against perfect within-round return selection, computed on the bid sample (referee A's method), and report the result as a bound. |
| 9 | Sweden active fee: 0.309 (Cookson dossier) against 0.303 (`referee_B.md` item 13) | **Print both.** Headline 0.303 (report L72); note 0.309 at L1476. |
| 10 | Global index withdrawer counted as a qualified loser | **Unqualified**, so there are 141 qualified losers (`referee_B.md` item 11). |
| 11 | C's netting: "passes narrowly" (`da_dossier.md` §0) against "sits at the bar" (`referee_C.md` §0.3) | **Referee C** (C1 and C2). |
| 12 | C's MDE: 2.1 / 2.7 against 2.5 to 3.5 under size-dependent volatility | **Referee C directionally.** Both rest on assumed volatility (NOT VERIFIED until σ_i is estimated). Moot for the decision. |
| 13 | C's replication: none feasible (DA dossier §3.3) against Chilean Tables 6 and 8 through LSEG (`referee_C.md` S1) | **Plausible, but LSEG coverage is NOT VERIFIED.** Moot, since C is not chosen. |
| 14 | Whether to put a C figure inside A (`da_dossier.md` §6; `referee_C.md` §4) | **No.** It adds a second question (price efficiency), costs about 2 to 5 weeks, has 43 to 68% power at b = 2.2, and its execution half depends on an unobserved transfer date. The score falls from 66 to 63 (section 3). |
| 15 | Fee and fund-supply material from the synopsis: CHY fee panel (`outside_search.md` §0.4) | **Keep only the exact category fee rows and removal counts in Table 1, panel B.** No fee-dispersion regressions. |
| 16 | PPM-ratio match with SSZ as an argument (audit §4.1; dossier §0) against "coincidence" (`referee_A.md` M7) | **Referee A.** Print it as a descriptive and argue nothing from it. |
| 17 | Headline frequency: annual (referee A §5) against annual plus monthly (dossier) | **Annual headline, monthly as the pre-registered precision check.** Reason: scale (row 18). |
| 18 | **New (mine):** "MDE 0.10, so the hypotheses are separable" (referee A §5) | **True only in SSZ's raw units.** Swedish annual flow sds are PPM 0.321 and non-PPM 0.179, against SSZ's DC 1.193 and non-DC 0.444 (`ssz_dossier.md` §3.6; `j4_mde.py`). Scaling SSZ's +0.185 by the non-DC sd ratio (0.40) gives +0.075. Power against +0.075 is **55% annually and 81% monthly**. Against SSZ's raw +0.185, and against the predicted -0.166, power is above 99% in both. |
| 19 | Klug fit of A reframed: 2 (referee A §3) against 3 (audit) | **3,** but only with the section 5 framing and Klug's written sign-off. |
| 20 | Referee A: "if FTN must be the headline, reopen" | **Moot.** The only alternative FTN headline is B's selection test, which is equally bounded (rows 4 and 8). |

## 3. Ranking on the winners-audit rubric (`winners_audit.md` §5; weights 2, 3, 2, 2, 3, 2, 2, 1, 1)

| Criterion (weight) | A reframed | A + C figure | C best (anchor) | B best | A as submitted |
|---|---:|---:|---:|---:|---:|
| 1 Same-question anchor (2) | 4 | 4 | 3 | 2 | 4 |
| 2 Table-level replication (3) | 4 | 4 | 3* | 1 | 4 |
| 3 Mechanism inside the anchor's specification (2) | 3 | 3 | 3 | 2 | 2 |
| 4 One headline question (2) | 4 | 3 | 4 | 4 | 2 |
| 5 Informative likely result (3) | 4** | 4 | 2 | 2 | 3 |
| 6 Identification from the institution (2) | 3 | 3 | 3 | 3 | 2 |
| 7 Avoids failure modes (2) | 3 | 2 | 3 | 3 | 2 |
| 8 Institutional data (1) | 5 | 5 | 3 | 3 | 5 |
| 9 Tutor fit (1) | 3 | 4 | 3 | 4 | 3 |
| **Total (max 90)** | **66 (73%)** | 63 (70%) | 53 (59%) | 44 (49%) | 53 (59%) |

\* C scores 3 on criterion 2 only if LSEG supports the Chilean Table 6/8 replication; otherwise 1, for a total of 47.
\** A scores 4 on criterion 5 only with the monthly precision check pre-registered; annual-only it scores 3, for a total of 63.

Sources for the scores: referee A §3, referee B §5 and referee C §3, adjusted as in rows 14, 18 and 19 of section 2. No hybrid beats A reframed, because every addition costs on criteria 4 and 7 more than it gains.

## 4. Trying to break A

**The strongest examiner case against A:**
1. *"This is SSZ on Swedish data."* The powered estimate uses 2020 to 2023 data and measures no effect of FTN, which is the synopsis topic and Klug's prompt. The course warns against "applying the question to Nordic countries unless meaningful" (`course_intro.txt` L147). Non-winner 5277, a Sabbatucci tutee, replicated a top-journal paper on Swedish funds and lost (`winners_audit.md` §4.1).
2. *"Your test is not diagnostic."* Non-PPM money is not non-DC. It contains insurer-curated unit-linked and occupational pension money and fund-of-funds flows (`referee_A.md` S3). PPM inertia (Cronqvist-Thaler; Dahlquist, Martinez and Söderlind) predicts a negative gap with or without SSZ's mechanism, so the likely result confirms something already known. Only a gap of zero or more is informative, and that is the unlikely outcome.
3. *"Your power is borrowed from US units."* Swedish flows are about 40% as volatile as SSZ's. Against a volatility-scaled US gap (+0.075), the annual test has 55% power (row 18).
4. *"Your FTN column is a survival regression on a rule FTN published."* Its power is 10 to 20% at plausible selection (`referee_A.md` F1).
5. *"Four annual cross-sections, Table II thin, signs pre-registered by an AI after seeing moments"* (`referee_A.md` S5, M10).

**Steelman of the runner-up, C (best version, `referee_C.md` §4).**
- It is the only candidate whose headline is an FTN effect with non-trivial power: 43 to 68% at b = 2.2, and higher against DLST's day-3 slope of 3.6.
- The shock is dated, information-free and rule-determined, and the rule held ex post: new Sweden-active winners received SEK 3.05 to 3.36bn against a predicted 3.42bn (`referee_C.md` item 7).
- Netting does not destroy the shock in market-cap units (`da_dossier.md` §2.2).
- It sits on Klug's dissertation (index-inclusion elasticities) and on the examiner's working paper (`BRIEFING.md` §1).
- A zero slope and a positive slope are both interesting.

(B's steelman: the closest fit to Klug's "selection design" prompt. But it has no replication, and its powered pieces collapsed under refereeing: `referee_B.md` §0.)

**Does A survive? Yes.**
- C's weaknesses are structural:
  - its powered half (the announcement) is not DLST's test;
  - it rests on one SEK 0.5bn fund's micro-cap book (C1, C2);
  - its DLST-matched half (execution) depends on a transfer date not yet observed.
- A's weaknesses respond to design:
  - Attack 1: the framing in section 5 plus Klug's sign-off. This only reduces the risk.
  - Attack 2: the asymmetric pre-registration plus a direct benchmark against SSZ's participant column (0.143) and non-DC column (0.310). Then "PPM behaves like SSZ's participants" is a quantitative claim, not a restatement of inertia. This reduces the risk.
  - Attack 3: the monthly check (81%) and the SHoF history request. Fully solved if the history arrives.
  - Attack 4: demote the column and report it as a bound. Fully solves the misreading.
  - Attack 5: the students freeze the pre-analysis plan before running anything. Fully solves it going forward.
- A loses only if Klug rejects the scope narrowing. The fallback is then B's best version (bid-level selection plus exact fees), not C, which drifts further from the synopsis (`referee_C.md` S7).

## 5. The FTN-headline tension

**Is the reframed A still on Klug's topic?** Partly.
- Klug's prompt is "effects of FTN ... on ... investor behaviour", and its stated main risk is the "short post-period and exact policy/selection design" (`BRIEFING.md` §1).
- A's powered estimate is not an FTN effect. It is the sponsor-free baseline that any claim about FTN's effect on how pension money responds to performance would need.
- A puts the powered test where the data are (before 2024) and confines FTN to what the short post-period can bound. That answers Klug's own risk, and it is the pitch to make to him.
- It is on-topic only with his written agreement.

**Is the proposed framing honest?** The proposal: "does Sweden's new public sponsor make PPM money discerning, as SSZ claim US sponsors do?", with FTN's realised selection reported as the answer, as a bound. **Not as a headline.**
- The literal answer to that question is the FTN column. Its power is 57% even against SSZ's sponsor column, 10 to 20% at a plausible score-rank correlation (`referee_A.md` F1), and about 5% against CJJM's decision-level loading (`referee_B.md` §3.4f).
- The post-2024 version of Table III, the regime column, has an MDE about 5 times the pre-period's (0.042 to 0.046 against 0.008 per month; `ssz_dossier.md` §5).
- The FTN column's main input is a rule FTN publishes (75% quality, 25% cost, with Sharpe and information ratios printed in each report; `ssz_dossier.md` §3.5). Its result is therefore partly known in advance, and its interest depends on the result. That breaks "interesting independently of the results" (`course_intro.txt`, research-question slide).
- Advertising the bound as the answer invites the 6812 failure mode (`winners_audit.md` §4.2).

**An honest framing that keeps FTN central.** Ask whether the premium pension *needed* a sponsor. FTN stays in the title, the motivation and the last table. The powered replication answers the question, and FTN's realised selection is the bounded epilogue.

**The framing in one sentence:** *Sialm, Starks and Zhang credit plan sponsors for making US pension money performance-sensitive; Sweden's premium pension had no sponsor until Fondtorgsnämnden began removing and adding funds in 2024, so we test whether premium-pension money was less performance-sensitive than the other money in the same funds before that, and bound how strongly the new sponsor's first selections loaded on past returns.*

## 6. Final specification

**Question.** Before Fondtorgsnämnden, was sponsor-free premium-pension money less performance-sensitive than the other money in the same funds, as Sialm, Starks and Zhang's sponsor attribution predicts?

Suggested title: "Did the Premium Pension Need a Sponsor? Sticky Money before Fondtorgsnämnden".

**Headline test (pre-registered and timestamped with Klug before any coefficient is run).**
- **Specification:** SSZ Table III difference regression.
  - Dependent variable: PPM flow minus non-PPM flow. Both are built with SSZ eqs. (1) and (2) from the same SHoF fund return (fixes `referee_A.md` M5); the `nt`-based PPM flow is a robustness check.
  - Sample: annual, December to December, flow-years 2020 to 2023 (2019 dropped). SEK-currency equity funds; AP7 and merger-recipient fund-years dropped.
  - Regressor: linear percentile rank of prior-year SHoF return.
  - Controls: SSZ's set minus family size and turnover (log PPM size, log non-PPM size, log age, expense ratio, volatility, style flow).
  - Year fixed effects; standard errors clustered by fund.
  - N 512, 153 funds. **MDE 0.101.**
- **Hypotheses, with Δ = β_PPM − β_nonPPM:**
  - H_noSponsor: Δ ≤ 0. Point prediction from SSZ's participant minus non-DC columns: -0.166 in raw units, about -0.07 scaled.
  - H_US: Δ = +0.185, SSZ's OLS-equivalent. Scaled version: **+0.075** (factor 0.179/0.444).
- **Pre-committed reading:**
  - If the upper end of the 95% CI is below 0.075, reject the US pattern at Swedish scale.
  - If the lower end is above 0, a sponsor is not necessary for DC money to be the more performance-sensitive money. This rejects SSZ's attribution as a necessary condition.
  - Otherwise, report the bound.
  - A negative Δ is described as "consistent with SSZ's participants, not unique to the sponsor channel".
- **Power:**
  - more than 99% against +0.185 and against -0.166;
  - against +0.075: 55% annually.
  - The pre-registered monthly precision check (same specification, 2020 to 2023, MDE 0.073 per year) has 81%.
- **Secondary, pre-registered:** the tail contrast (Low + High)/2 − Mid (`referee_A.md` S4).

**Replication tables, with SSZ's numbers printed alongside.**
- **Table 1** (SSZ Table I):
  - PPM ratio beside SSZ's 25.38 / 8.50 / 19.85 / 35.52.
  - Flows: SSZ's DC 32.00 (sd 119.34) and non-DC 6.65 (sd 44.37).
  - Sizes and fees.
  - Panel B gives FTN rounds descriptively: bids, winners, removed funds and capital, and exact category fees before and after (Sweden active 0.303, with 0.309 noted).
- **Table 2, the headline** (SSZ Table III):
  - PPM, non-PPM and difference columns, in piecewise format with tail MDEs, plus the linear headline row and its OLS-equivalent.
  - SSZ's 1-year panel alongside: DC 1.194 (0.377) / 0.236 (0.086) / 1.776 (0.497); non-DC 0.328 (0.142) / 0.284 (0.037) / 0.487 (0.180); difference 0.866 (0.374) / -0.049 (0.090) / 1.289 (0.476); N 3,851. OLS-equivalents: 0.496 / 0.310 / 0.185.
  - Robustness rows: monthly; 2019 included; December excluded; within-category rank (Table IV analog); clustering by category.
- **Table 4** (SSZ Table IX):
  - Next-year raw and category-adjusted performance on lagged PPM and non-PPM flows.
  - SSZ alongside: DC -0.262 (0.163) and -0.260 (0.160); non-DC -1.567 (0.455) and -1.102 (0.436); F-test p-values 0.009 and 0.074.
  - The unit (percent per month) is still to be verified on p. 833 (`ssz_dossier.md` §1.2: NOT VERIFIED).
- **Figure 1** (SSZ Figure 1): flows by prior-return percentile group, PPM against non-PPM, beside SSZ's values (middle 10%: +23.7 against +2.1).

**The extension, inside the anchor's tables.**
- **Table 3, an SSZ Table VIII column titled "The new sponsor":**
  - Stage 1: P(bid | incumbent), N 87 (R1 to R4).
  - Stage 2: P(win | bid) on 36-month and 12-month category percentiles dated at each round's bid deadline. Main sample N 110 (10 rounds), which excludes the appealed global active round; N 142 with it, as robustness (`cookson_dossier.md` §2.4). The three all-qualified Swedish rounds serve as a P(win | qualified) check.
  - Strategy-level fund identity, round fixed effects, and randomisation inference within round.
  - The slope is reported as a fraction of the perfect-selection slope computed on the same sample. For the incumbent sponsor-flow version (perfect-selection slope 1.155), it is also set beside SSZ's sponsor column: 1.050 (0.376) / 0.310 (0.083) / 1.389 (0.427), OLS-equivalent 0.499. Participant column: -0.004 / 0.156 / 0.194, OLS-equivalent 0.143.
  - The equal-split dose rule is described, not estimated.
  - This column depends only on award decisions, not transfers, so R6 and the 2026 rounds enter without waiting for the data calendar.

**What to drop:**
- the regime column;
- the FTN-period Table IX;
- the dose regression;
- the FTN-period non-PPM spillovers;
- all of B's flow tests ((ii) to (v));
- all of C, including the Chilean replication;
- Tables IV to VII as separate exhibits;
- the PPM-ratio match as an argument;
- causal "introduction of a sponsor" language;
- the "80% power" claim.

Table II, 2019 as a rule-change year (SEK 500m external-capital rule), and a PPM-only panel for 2012 to 2023 go to the appendix as descriptives.

**Exhibits (5):** Table 1, Figure 1, Table 2 (headline), Table 3 (new sponsor), Table 4.

## 7. Consolidated risk register (**S** = could still sink the thesis)

| # | Risk | Solution | Effect |
|---|---|---|---|
| **S1** | Read as "SSZ on Swedish data", off Klug's FTN topic (5277/4441 pattern) | Section 5 framing; FTN in the title and Table 3; a written answer from Klug on the A/B question by 9 October | Reduces |
| **S2** | Non-PPM is not non-DC (unit-linked, occupational, fund-of-funds money), so a negative gap is not diagnostic | Asymmetric pre-registration; compare with SSZ's participant column (0.143) and non-DC column (0.310), not only the difference; holder-composition row from Fondbolagen or SCB (NOT VERIFIED that it exists); drop families with large in-house fund-of-funds as robustness | Reduces |
| **S3** | Headline power depends on scale (55% annually against +0.075) with only 4 cross-sections | Pre-registered monthly check (81%); request SHoF pre-2018 TNA and returns, which would roughly double or triple the annual N | Fully solves if SHoF delivers; otherwise reduces |
| 4 | 2019 re-registration, mapping into AP7 and fund families | Drop flow-year 2019 (MDE 0.101) | Fully solves |
| 5 | Robot switching before Dec 2011; advisers | Appendix panel starts in 2012; "participant" defined as "participant or adviser" | Fully (panel); reduces (definition) |
| 6 | Mergers and family mappings in all years | Flag a same-company exit plus an nt spike; drop those fund-years | Reduces (no merger link in the Morningstar master) |
| 7 | Placeholder rows distort exit dating (A1) | Drop rows with NaN name and mv before any exit or survival coding | Fully solves |
| 8 | Integer-rounded file returns; differing flow denominators | SHoF ranks; SSZ eqs. (1) and (2) for both flow types | Fully solves |
| 9 | December placement | Year FE; December-excluded robustness (MDE unchanged) | Fully solves |
| 10 | FTN column misread as a test of SSZ; low power | Two stages at bid level, strategy identity, randomisation inference, bound in perfect-selection units | Fully solves the misreading; does not solve the power |
| 11 | FTN covariates dated after the bid deadline; non-PPM losers' returns missing (19 of 149); qualification status unknown | Re-date at bid deadlines; SHoF series for 82 matched loser fundids; FTN records request; three all-qualified rounds | Fully solves the dating; reduces the rest (fully if FTN releases status) |
| 12 | Fan-out | Cap at 5 exhibits; the drop list above | Fully solves, if enforced |
| 13 | Over-claiming in the conclusion | Each claim states the coefficient, SSZ's coefficient and the bound in one sentence | Fully solves |
| 14 | Pre-registration credibility (AI-written signs; Table II moments already seen) | Students freeze and timestamp the plan and send it to Klug; Table II descriptive only | Fully solves going forward |
| 15 | Synopsis promises (fees, supply, active vs default, performance after inflows) | Table 1 panel B (exact fees, removal counts); one cited sentence on the 85-95% default share; Table 4 covers performance after inflows; Klug signs off on the narrowed scope | Reduces |
| 16 | Recency (2015) | Pair with Tran and Wang (2023 JFE) and Kronlund et al. (2021 JFE) | Fully solves the rule |
| 17 | SEK-only, mostly Swedish-domiciled sample | State it; add EUR funds if FX is added | Reduces |
| 18 | Novelty (DiVA theses; Riksrevisionen FTN audit, per `outside_search.md` §0.4) | Search both before writing the novelty sentence | Reduces |
| 19 | Examiner out of sample | Write to the course rules: power, simplicity, no significance chasing | Reduces |
| 20 | Nine-week calendar | The headline needs no 2026 data; freeze the data on 1 November | Reduces |

## 8. Week-one actions, in order

1. **Day 1. Send the data requests:**
   - SHoF: pre-2018 TNA and returns for PPM-linked ids, plus series for the 82 matched non-PPM loser fundids.
   - FTN (offentlighetsprincipen): per-bid qualification status and quality scores.
   - Pensionsmyndigheten: per-round counts of active versus default choices, and the 2019 deregistration mapping.
   - Fondbolagen or SCB: fund capital by holder type.
2. **Days 1 to 2. Hygiene (no coefficients):**
   - drop the placeholder rows;
   - flag merger recipients;
   - rank on SHoF returns;
   - unify the flow definitions;
   - re-date the FTN covariates at bid deadlines;
   - code strategy-level identity (Nordea European Stars, SEB, Handelsbanken cases);
   - read the Fondstatistik fee headers;
   - check the Table IX unit on SSZ p. 833.
3. **Days 2 to 3. Freeze the pre-analysis plan:**
   - the question;
   - the headline specification;
   - H_noSponsor, H_US and H_US-scaled;
   - the MDEs (0.101 annual, 0.073 monthly);
   - the asymmetric reading;
   - the five exhibits;
   - the drop list;
   - the perfect-selection benchmark for Table 3.

   Timestamp it and email it to Klug.
4. **Klug meeting (9 October, per `da_dossier.md` §5). The A/B question:** "Should we do A: test Sialm, Starks and Zhang's sponsor attribution on 2020-2023 premium-pension data (MDE 0.10 per year, against SSZ's +0.185), with FTN's realised selection as a bounded Table VIII column? Or B: an FTN selection study with no replication, whose main test detects only near-perfect return-based selection? And do you accept narrowing the synopsis's fee and supply promises to Table 1?"
5. **Days 4 to 5:**
   - DiVA and Riksrevisionen novelty check;
   - recompute the SE-only power table under the frozen specification;
   - only then open the coefficients, Table 1 and Figure 1 first.
