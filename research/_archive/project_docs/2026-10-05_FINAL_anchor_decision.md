> ARCHIVED 5 October 2026. Superseded by `PLAN.md` (root of the thesis folder), which carries over everything below that is still valid and adds the Dahlquist and Martinez (2015) changes. Kept for the record only.

# Final anchor decision: Sialm, Starks and Zhang (2015), "Did the premium pension need a sponsor?"

Decided 5 October 2026 after two adversarial rounds. Round 1: three dossiers (A, B, C), an outside search and a winners audit. Round 2: three hostile referees and an independent judge. This document supersedes the anchor choices in `final_design_and_plan.md` (Da et al.), `pressure_test_cookson_ssz_price_pressure.md` and `anchor_decision_cookson_vs_ssz.md`.

## 1. Decision

**Anchor:** Sialm, Starks and Zhang (2015), "Defined Contribution Pension Plans: Sticky or Discerning Money?", Journal of Finance 70(2), 805-838.

**Recency partners:** Tran and Wang (2023, JFE 148(1)); Kronlund, Pool, Sialm and Stefanescu (2021, JFE 141(2)).

**Framing:**
- SSZ credit plan sponsors with making US pension money performance-sensitive.
- Sweden's premium pension had no sponsor until Fondtorgsnämnden began removing and adding funds in 2024.
- The thesis tests whether premium-pension money was less performance-sensitive than the other money in the same funds before that.
- It then bounds how strongly the new sponsor's first selections loaded on past returns.

**Working title:** "Did the Premium Pension Need a Sponsor? Sticky Money before Fondtorgsnämnden".

**Rubric scores** (winners-audit rubric, after all corrections; judge §3):

| Candidate | Score |
|---|---|
| A reframed | 66/90 (73%) |
| A plus a price-pressure figure | 63 (70%) |
| C (Da et al.) at its best | 53 (59%); 47 if the Chilean replication is not feasible |
| A as first submitted | 53 (59%) |
| B (Cookson et al.) at its best | 44 (49%) |

No outside paper beat A, B or C (outside search §0).

## 2. Why A wins, on the evidence

- **Replication.** It is the only candidate whose replication is table-level and powered on data independent of the short FTN window.
  - Table III difference, linear rank, flow-years 2020-2023: N 512 (153 funds), MDE 0.101 per year.
  - SSZ's own OLS-equivalent gap is +0.185; the predicted no-sponsor gap is about -0.17. Both are separable from zero with power above 99%.
- **Extension.** It sits inside SSZ's own Table VIII as a "new sponsor" column.
  - SSZ's sponsor flow is mechanical by construction, so the FTN analogue is legitimate.
  - Footnote 6 (p. 807): "When a fund is replaced, the plan assets are typically transferred to the new fund."
- **Data.** Everything is in hand.
  - Pensionsmyndigheten files 2001-2026. "Handel, netto" is verified as the monthly net SEK flow (median identity gap 0.015-0.030% of assets).
  - SHoF Morningstar monthly TNA and returns from 2018, covering all 482 PPM funds with an ISIN.
  - All 11 FTN reports.
- **What winners do.**
  - 8 of the 11 winners in 2019-2024 replicated or transplanted an anchor's specification.
  - In the cleanest matched pair (the 2023 FOMC winner against non-winner 4441), the winner tested a measured mechanism inside the anchor's regression. The non-winner stopped at a new period.
  - Calibrated conclusions are the strongest discriminator: over-claiming in 4 of 25 winners against 19 of 33 sampled non-winners (Fisher p = 0.0025).
- **Why B lost on refereeing.**
  - No table can be replicated (the FCA data are confidential).
  - Its new headline (voluntary exits before removal) fails. Saver letters arrive 2-5 months after the award, after the measurement window, and transfers are staged in 20-60% tranches.
  - Its selection test has about 5% power against Cookson's decision-level coefficient.
  - Its one powered piece, selection at bid level, fits inside A's Table 3.
- **Why C lost on refereeing.**
  - Its only powered test (the award window) is not Da et al.'s test (execution).
  - It rests on one small fund: Meds Apotek, bought only by Aktiespararna Edge, carries 41% of squared net demand.
  - On Q2 holdings, net demand sits at the pre-registered bar (0.509 pp) rather than passing it.
  - Its replication is method-level only.

## 3. Final specification

**Question.** Before Fondtorgsnämnden, was sponsor-free premium-pension money less performance-sensitive than the other money in the same funds, as SSZ's sponsor attribution predicts?

**Headline test.** Pre-register it and timestamp it with Klug before running any coefficient.

| Element | Specification |
|---|---|
| Regression | SSZ Table III difference |
| Dependent variable | PPM flow minus non-PPM flow, both built with SSZ eqs. (1)-(2) from the same SHoF return |
| Sample | Annual, December to December, flow-years 2020-2023 (2019 dropped); SEK-currency equity funds; AP7 and merger-recipient fund-years dropped |
| Regressor | Linear percentile rank of prior-year SHoF return |
| Controls | SSZ's set without family size and turnover |
| Fixed effects and SEs | Year fixed effects; standard errors clustered by fund |

**Hypotheses** (Δ = β_PPM − β_nonPPM):
- H_noSponsor: Δ ≤ 0. Point prediction about -0.17 raw, about -0.07 scaled.
- H_US: Δ = +0.185, SSZ's OLS-equivalent.
- H_US scaled: Δ = +0.075. Swedish flows are about 40% as volatile as SSZ's (0.179/0.444).

**Power.**
- Above 99% against +0.185 and against -0.17.
- Against +0.075: 55% on annual data. A pre-registered monthly precision check (MDE 0.073 per year) raises this to 81%.

**Pre-committed reading.**
- If the CI upper bound is below 0.075: reject the US pattern at Swedish scale.
- If the CI lower bound is above 0: a sponsor is not necessary.
- Otherwise: report the bound.
- A negative Δ is "consistent with SSZ's participants, not unique to the sponsor channel".

**Secondary test:** the tail contrast, (Low + High)/2 − Mid.

**Exhibits (five):**
1. **Table 1 (SSZ Table I).**
   - PPM ratio beside SSZ's 25.38 / 8.50 / 19.85 / 35.52.
   - Flows beside SSZ's DC 32.00 (sd 119.34) and non-DC 6.65 (sd 44.37).
   - Panel B: the FTN rounds descriptively (bids, winners, removals, capital, exact category fees before and after).
2. **Figure 1 (SSZ Figure 1).** Flows by prior-return percentile, PPM against non-PPM, with SSZ's values (middle 10%: +23.7 against +2.1).
3. **Table 2, the headline (SSZ Table III).**
   - Piecewise rows with tail MDEs, plus the linear headline row.
   - SSZ's 1-year panel alongside: DC 1.194 / 0.236 / 1.776; non-DC 0.328 / 0.284 / 0.487; difference 0.866 / -0.049 / 1.289; N 3,851. OLS-equivalents 0.496 / 0.310 / 0.185.
   - Robustness rows: monthly; 2019 included; December excluded; within-category rank; clustering by category.
4. **Table 3, the new sponsor (SSZ Table VIII column).**
   - Stage 1: P(bid | incumbent), N 87.
   - Stage 2: P(win | bid) on 36- and 12-month category percentiles, dated at the bid deadline. N 110 without the appealed global active round; N 142 with it.
   - Strategy-level fund identity, round fixed effects, randomisation inference within round.
   - Reported as a fraction of the perfect-selection slope, beside SSZ's sponsor column (1.050 / 0.310 / 1.389; OLS-equivalent 0.499) and participant column (-0.004 / 0.156 / 0.194; OLS-equivalent 0.143).
   - The equal-split dose rule is described, not estimated.
5. **Table 4 (SSZ Table IX).**
   - Next-year raw and category-adjusted performance on lagged PPM and non-PPM flows.
   - SSZ alongside: DC -0.262 (0.163); non-DC -1.567 (0.455); F-test p 0.009.
   - The performance unit on SSZ p. 833 is still to be verified.

**Appendix (descriptive):** Table II; 2019 as a rule-change year; a PPM-only panel for 2012-2023.

**Dropped:**
- the regime column, the FTN-period Table IX, the dose regression and the FTN-period non-PPM spillovers;
- all of B's flow tests;
- all of C, including the Chilean replication;
- the PPM-ratio match used as an argument;
- causal "introduction of a sponsor" language;
- the "80% power" claim.

## 4. Corrections made by the referees (confirmed by the judge)

- **2019 exits** hold SEK 87.7bn gross (84.1bn net of 16 renumberings), not 60.9bn. The lower figure came from empty placeholder rows; drop those rows before dating any exit.
- **December placement** into chosen (non-AP7) funds is SEK 16-19bn a year (2019-2025). The earlier 47-51bn included AP7.
- **Benchmarks.** A linear rank weights SSZ's segments 0.104 / 0.792 / 0.104. The correct benchmarks are therefore +0.185 (difference), 0.499 (sponsor) and 0.143 (participant), not the secant values 0.402 and 0.674.
- **FTN sponsor column.**
  - Power is about 57% against SSZ's sponsor column, and 10-20% at a plausible correlation between score and rank.
  - 24 of the 62 "removed" funds never bid, and at least 3 are winners at strategy level. Hence the two-stage, bid-level design.
  - The N = 81 sample spans 4 award dates, not 5.
- **Pensionsmyndigheten file returns** are integer-rounded. Rank on SHoF returns instead.
- **Fees.** The Sweden active fee before procurement is 0.303% (the report says 0.309 once). The withdrawer in the global index round was not qualified.

## 5. Risks and solutions (S = could still sink the thesis)

| # | Risk | Solution | Effect |
|---|---|---|---|
| **S1** | Read as "SSZ on Swedish data", off Klug's FTN topic (the 5277 / 4441 pattern) | "Did PPM need a sponsor?" framing. FTN in the title, Table 1 panel B and Table 3. Get Klug's written answer to the A/B question | Reduces |
| **S2** | Non-PPM money is not non-DC (it includes unit-linked, occupational and fund-of-funds money), so a negative gap is not diagnostic | Asymmetric pre-registration. Compare with SSZ's participant (0.143) and non-DC (0.310) columns, not only the difference. Holder-composition row from Fondbolagen or SCB (existence not verified). Robustness check dropping families with large in-house fund-of-funds | Reduces |
| **S3** | Power depends on scale (55% annual against +0.075), with only four cross-sections | Pre-registered monthly check (81%). Request SHoF TNA and returns before 2018 | Fully solves if SHoF delivers; otherwise reduces |
| 4 | 2019 re-registration and mapping into AP7 or sibling funds | Drop flow-year 2019 | Fully solves |
| 5 | Robot switching before December 2011; advisers | Start the appendix panel in 2012. Call the flows "participant or adviser" (as in SSZ footnote 18) | Fully solves the first; reduces the second |
| 6 | Mergers and family mappings | Flag same-company exits with a net-trading spike; drop those fund-years | Reduces |
| 7 | Placeholder rows; rounded returns; different flow denominators | Drop empty rows. Use SHoF ranks. Use SSZ eqs. (1)-(2) for both flows | Fully solves |
| 8 | December placement | Year fixed effects; December-excluded robustness | Fully solves |
| 9 | FTN column misread, and low power | Two-stage bid-level design; bound in perfect-selection units; randomisation inference | Fully solves the misreading; power remains low |
| 10 | Missing FTN covariates: returns for non-PPM losers (19 of 149) and qualification status | Re-date at bid deadlines. Get SHoF series for the 82 matched loser fund ids. FTN records request. Use the three all-qualified rounds | Reduces (fully if FTN releases status) |
| 11 | Fan-out | Five exhibits and the drop list | Fully solves if enforced |
| 12 | Over-claiming | Each claim states our coefficient, SSZ's coefficient and the bound in one sentence | Fully solves |
| 13 | Pre-registration credibility | The students freeze and timestamp the plan and send it to Klug | Fully solves from now on |
| 14 | Synopsis promises (fees, supply, active vs default, performance after inflows) | Table 1 panel B; one cited sentence on the 85-95% default share; Table 4; Klug's sign-off | Reduces |
| 15 | Recency (2015) | Pair with Tran and Wang (2023) and Kronlund et al. (2021) | Fully solves |
| 16 | Novelty (DiVA theses; Riksrevisionen's ongoing FTN audit) | Search both before writing the contribution sentence | Reduces |
| 17 | Nine-week calendar | The headline needs no 2026 data; freeze the data on 1 November | Reduces |

## 6. Week-one actions

1. **Send the data requests.**
   - SHoF: TNA and returns before 2018 for PPM-linked ids, plus series for the 82 matched non-PPM loser fund ids.
   - FTN (offentlighetsprincipen): per-bid qualification status and quality scores.
   - Pensionsmyndigheten: per-round counts of active versus default choices, and the 2019 deregistration mapping.
   - Fondbolagen or SCB: fund capital by holder type.
2. **Data hygiene (no coefficients).**
   - Drop placeholder rows; flag mergers; rank on SHoF returns; unify the flow definitions.
   - Re-date FTN covariates at bid deadlines; code strategy-level identity.
   - Read the fee headers; verify the Table IX unit on SSZ p. 833.
3. **Freeze the pre-analysis plan:** question, specification, hypotheses, MDEs, reading, exhibits, drop list. Timestamp it and send it to Klug.
4. **Put the A/B question to Klug:**
   > "Should we do A: test SSZ's sponsor attribution on 2020-2023 premium-pension data (MDE 0.10 per year against SSZ's +0.185), with FTN's realised selection as a bounded Table VIII column? Or B: an FTN selection study with no replication, whose main test detects only near-perfect return-based selection? And do you accept narrowing the synopsis's fee and supply promises to Table 1?"
5. **Then:** the novelty check; recompute the power table under the frozen specification; only then open the coefficients.

## 7. Record

The nine supporting reports, plus the shared briefing, were copied on 5 October 2026 into the local folder `~/Documents/financethesis_ny/research/anchor_final/`:
- `BRIEFING.md`
- `round1/`: `ssz_dossier.md`, `cookson_dossier.md`, `da_dossier.md`, `outside_search.md`, `winners_audit.md`
- `round2/`: `referee_A.md`, `referee_B.md`, `referee_C.md`, `judge.md`

All power work was blind: only standard errors, counts and MDEs were computed, and no treatment or replication coefficient was printed.
