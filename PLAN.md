# PLAN.md: the thesis in one document

**Single source of truth.** Last updated 6 October 2026 (final anchor sweep: SSZ confirmed, no design change). It replaces every earlier plan and memo; those are in `research/_archive/`. If anything here conflicts with an older file, this file wins. Gates and dates are in `STEPS.md`.

Authors: Alexander Fox and Ludvig Pauli Uväng. Tutor: Michael Klug. Course: BE451, autumn 2026.

> Course rule: AI may not write thesis text. Every sentence marked *draft* below is a placeholder for meaning only. Rewrite it in your own words before it goes into the thesis.

---

## 1. Course requirements and deadlines

| What | When |
|---|---|
| Mid-term meeting with Klug | November, on Klug's date |
| Thesis in Canvas **and** replication package (zip) to Anneli Sandbladh | **Mon 7 December, 10:00** |
| Presentation and opposition | Before 12 December |
| Final version in Publish Thesis | 18 December, 18:00 |

**Format** (syllabus and intro lecture):
- English; official front page; **no table of contents**.
- Main text at most 40 pages (about 25-40 including the key tables and figures); 12 pt, single spacing.
- Introduction 2-4 pages, self-contained, previewing the numbers.
- Related literature under about one page ("not a review of the literature").
- Detailed, self-contained table captions.
- No textbook explanations of standard methods.
- Every in-text source is in the references and vice versa.
- **AI appendix** required. Keep an AI log from today: tool, date, purpose, what changed.

**What the examiner grades:** useful, correct, relevant, contribution, independence. The standard is "replication and extension of a (recent) published paper in a top journal". The extension must be meaningful, and simply moving the question to a Nordic country does not count unless that is meaningful in itself. "Do not chase statistical significance." "Check the power of your test."

---

## 2. What the thesis is

**Question.** Before Fondtorgsnämnden (FTN) existed, was premium-pension money less responsive to fund performance than the other money invested in the same funds? And when FTN arrived as the system's first "sponsor", how strongly did its first fund selections depend on past returns?

**Working title.** "Did the Premium Pension Need a Sponsor? Sticky Money before Fondtorgsnämnden"

**The story in three steps:**
1. **Sialm, Starks and Zhang (2015, JF):** US pension (DC) money is *more* performance-sensitive than the other money in the same funds. They attribute this to plan sponsors, who remove bad funds from the menu.
2. **Dahlquist and Martinez (2015, EFM):** Swedish premium-pension money, with no sponsor, was *less* sensitive than retail money in the same funds in 2000-2008. The gap is significant in SEK terms but not once flows are scaled by market size.
3. **FTN (from 2024):** Sweden's premium pension got a sponsor. The thesis tests the gap in the last years before (2020-2023) with a powered design, reads it through SSZ's sponsor attribution, and bounds how return-based FTN's first selections were.

**What is new** (the direction of the gap is not, see D&M):
1. A test with enough power to separate the two groups, using SSZ's fund-level flows. D&M's market-share test could not.
2. The post-reform period (2020-2023, after the 2019-2022 fund-market reforms).
3. The sponsor interpretation (Sweden as the no-sponsor counterpart to SSZ).
4. The FTN "new sponsor" column.

*Draft contribution (rewrite):* Dahlquist and Martinez (2015) show that premium-pension money responded far less to past returns than retail money in the same funds in 2000-2008, although the gap is imprecise once flows are scaled by market size. We ask whether the gap survived the reforms of 2019-2022, estimate it with fund-level flows that can separate the two groups, and read it through Sialm, Starks and Zhang's sponsor attribution, in the last years before Fondtorgsnämnden became the system's sponsor.

---

## 3. Papers and their roles

All five exhibits come from **one** paper (SSZ). Everything else is benchmark, design input or literature. That is the winners' pattern: one anchor transplanted to new data, one extension inside the anchor's own table, the anchor's numbers printed alongside.

| Paper | Role |
|---|---|
| **Sialm, Starks and Zhang (2015), JF 70(2), 805-838** | Anchor. Specification and Tables I, III, VIII, IX, Figure 1 |
| **Dahlquist and Martinez (2015), EFM 21(1), 1-19** | Swedish predecessor; robustness specification; conditional replication. Notes: `research/literature/dahlquist_martinez_2015_notes.md` |
| Fricke, Jank and Wilke (2026), RFS | Recency partner: clientele sensitivities within the same fund-quarter (sharpens risk S2) |
| Tran and Wang (2023), JFE 148(1); Kronlund, Pool, Sialm and Stefanescu (2021), JFE 141(2) | Recency partners |
| Evans and Fahlenbrach (2012), RFS 25(12); (2007) working paper | Mechanism: investors leaving ("market governance") vs a sponsor acting ("traditional governance") |
| Keim and Mitchell (2018), JPEF | What a sponsor's removal round does to savers |
| Cookson, Jenkinson, Jones and Martinez (2021), RFS; Jenkinson, Jones and Martinez (2016), JF | Gatekeeper selection; design input for Table 3 only |
| Koh and Mitchell (2010); Kavourakis and Tanewski (2026) | Public bodies curating or grading pension funds (Singapore, Australia) |
| Del Guercio and Tkac (2002), JFQA 37(4) | Pension vs retail flow-performance; ancestor of SSZ |
| Goyal and Wahal (2008), JF 63(4); Brown, Gredil, Kantak and Ramadorai (2023), RFS 36(8) | Does a selector pick better funds? Design ancestors for Table 3 |
| Barr and Diamond (2020), response to SOU 2019:44 | Hypothesis for Table 3: procurement screens out bad funds better than it picks winners |
| Engström and Westerberg (2004), SSE WP 555; Hagen, Malisa and Post (2023), RBF 15(5) | First PPM flow paper; recent published use of the same Pensionsmyndigheten data |
| Bjerksund, Døskeland, Sjuve and Ørpetveit (2026), MS 72(5) | Scandinavian authority intervening in fund quality (related literature) |
| FI (2025), *Avgifter och distribution på den svenska fondmarknaden*; RiR 2018:32; Riksrevisionen audit 2026; FTN results (European Pensions, 18 Mar 2026) | Institutional background and novelty |
| Berk and Green (2004); Sirri and Tufano (1998) | Flow-performance background |

Full literature sweep (about 9,500 records, four databases): `research/literature/literature_sweep_2026-10-05.md`. Final web sweep (six agents, 6 Oct): `research/literature/anchor_sweep_final_2026-10-06.md`. **Nothing beats SSZ; the anchor question is closed.** Aim for 20-30 references in total.

---

## 4. Specification (to be frozen in the pre-analysis plan)

### 4.1 Headline test (SSZ Table III difference)

| Element | Specification |
|---|---|
| Dependent variable | PPM flow minus non-PPM flow, both built with SSZ eqs. (1)-(2) from the same SHoF return |
| Sample | Annual, December to December, flow-years 2020-2023 (2019 dropped); SEK-currency equity funds; AP7 and merger-recipient fund-years dropped |
| Regressor | Linear percentile rank of prior-year SHoF return |
| Controls | SSZ's set without family size and turnover |
| Fixed effects and SEs | Year fixed effects; standard errors clustered by fund |
| Size and power | N 512 (153 funds); MDE 0.101 per year |

### 4.2 Hypotheses (Δ = β_PPM − β_nonPPM)

- **H_noSponsor:** Δ ≤ 0. Point prediction about −0.17 raw (about −0.07 scaled).
  - Cross-check against D&M: their market-share coefficients, converted to fund-level annual units (×230 funds, ×4 quarters), imply about −0.18 per year.
  - The conversion assumes equal-size funds, so it is a rough cross-check only. Write it and its caveat into the PAP.
- **H_US:** Δ = +0.185 (SSZ's OLS-equivalent).
- **H_US scaled:** Δ = +0.075 (Swedish flows are about 40% as volatile as SSZ's, 0.179/0.444).
- **Power:** above 99% against +0.185 and −0.17. Against +0.075 it is 55% on annual data and 81% with the pre-registered monthly precision check (MDE 0.073 per year).

### 4.3 Pre-committed reading

- If the CI upper bound is below 0.075: reject the US pattern at Swedish scale.
- If the CI lower bound is above 0: a sponsor is not necessary for performance-sensitive pension money.
- Otherwise: report the bound.
- A negative Δ is "consistent with SSZ's participants and with D&M's 2000-2008 evidence, not unique to the sponsor channel".
- A Δ near zero or positive means the 2000-2008 gap has closed. That is reported as a change since D&M, not as a failure.

### 4.4 Exhibits (five, fixed)

| Exhibit | Source | Content |
|---|---|---|
| **Table 1** | SSZ Table I | PPM ratio and flow moments beside SSZ (25.38 / 8.50 / 19.85 / 35.52; DC 32.00, sd 119.34; non-DC 6.65, sd 44.37) and beside D&M's 2008 shares. Panel B: the FTN rounds (bids, winners, removals, capital, category fees before and after) |
| **Figure 1** | SSZ Figure 1 | Flows by prior-return percentile, PPM vs non-PPM, SSZ values overlaid (middle 10%: +23.7 vs +2.1) |
| **Table 2 (headline)** | SSZ Table III | Piecewise rows with tail MDEs plus the linear headline row; SSZ's 1-year panel alongside (DC 1.194 / 0.236 / 1.776; non-DC 0.328 / 0.284 / 0.487; difference 0.866 / −0.049 / 1.289; N 3,851; OLS-equivalents 0.496 / 0.310 / 0.185). Robustness rows: monthly; 2019 included; December excluded; within-category rank; category clustering; funds-of-funds families excluded; **D&M rows** (4.5) |
| **Table 3 (new sponsor)** | SSZ Table VIII, one new column | Stage 1: P(bid given incumbent), N 87. Stage 2: P(win given bid) on 36- and 12-month category percentiles at the bid deadline (N 110; N 142 with the appealed global active round). Strategy-level fund identity, round fixed effects, randomisation inference within round. Reported as a fraction of the perfect-selection slope, beside SSZ's sponsor column (1.050 / 0.310 / 1.389; OLS-equivalent 0.499) and participant column (−0.004 / 0.156 / 0.194; OLS-equivalent 0.143). The equal-split dose rule is described, not estimated |
| **Table 4** | SSZ Table IX | Next-year raw and category-adjusted performance on lagged PPM and non-PPM flows; SSZ beside (DC −0.262 (0.163); non-DC −1.567 (0.455); F-test p 0.009). Verify the unit on SSZ p. 833 |

**Secondary test:** the tail contrast, (Low + High)/2 − Mid.

**Table 3 reading (pre-register in the PAP):** Barr and Diamond (2020) predict that procurement screens out bad funds better than it picks good ones. State in advance how stage 1 (incumbents bidding or leaving) and stage 2 (winning given a bid) bear on that prediction. Framing only, no new estimate.

### 4.5 D&M robustness rows (pre-registered, inside Table 2)

- Quarterly, 2020Q1-2023Q4.
- Absolute SEK flow and market-share flow (D&M eqs. 1-3).
- Return rank, new-pension-money term (log TNA × contribution-quarter dummy), log TNA, one-year volatility, quarter intercepts.
- PPM and non-PPM equations estimated jointly as a system, with pairwise bootstrap standard errors (1,000 replications).
- Print D&M's 2000-2008 Systems I and III alongside (Table 2, p. 11): retail 0.064 / 0.023, pension 0.007 / 0.003; Wald p < 0.001 and 0.123.
- Inputs: PPM quarterly flow = summed monthly "Handel, netto"; non-PPM = SHoF TNA minus PPM capital.

### 4.6 Appendix

- Descriptive: SSZ Table II; 2019 as a rule-change year; PPM-only panel 2012-2023.
- **Conditional:** replicate D&M Table 2 (Systems I-IV) for 2001-2008. Only if quarterly non-PPM fund assets for 2000-2008 arrive by the data freeze; otherwise drop it with one sentence.

### 4.7 Dropped (do not reopen)

- The regime column, the FTN-period Table IX, the dose regression, FTN-period non-PPM spillovers.
- All Cookson-style flow tests (old design B).
- The price-pressure design (old design C), including the Chilean replication.
- The PPM-ratio match used as an argument.
- Causal "introduction of a sponsor" language.
- The "80% power" claim.

---

## 5. Data

### 5.1 In the folder now

| Data | Where |
|---|---|
| Pensionsmyndigheten monthly fund files 2001-2026 ("Handel, netto", market value, fund choices, fees, returns) | `data/raw/` (2001-2008, 2009-2014, 2015-2020, 2021-2026, pensionsmyndigheten) |
| SHoF Morningstar valuations and reinvestments (raw) | `data/Valuations/`, `data/Reinvestments/` |
| SHoF monthly series built from them (valuations, reinvestments) and the script | `data/derived/shof_monthly/` |
| SHoF fund master and fees | `data/fundmaster.xlsx`, `data/FEES.txt`; `data/extra/shof_fundmaster.zip`, `data/extra/shof_field_definitions.*` |
| All 11 FTN procurement reports | `data/FTN/` |
| FI holdings (2023Q4, 2024Q1, 2024Q2, 2026Q2), selected PPM monthly workbooks, PPM NAV 2024 | `data/extra/` |

### 5.2 Not on disk: rebuild in week 1

The derived files used in the anchor reports were built in earlier cloud sessions and are **not in the folder**. Rebuild them from raw data with code saved in the repo:
- the fund panel (`pa_panel`), with fee_net and fee_gross;
- the bid file (`bids_long`: 290 bids, 75 winners, 108 incumbents; 147 matched to SHoF);
- the power scripts (standard errors and MDEs only, no treatment coefficients).

### 5.3 Requests (send Tue 6 Oct)

- **SHoF:**
  - monthly TNA and returns before 2018 for PPM-linked fund ids;
  - quarterly fund assets for 2000-2008 (for the D&M replication);
  - series for the 82 matched non-PPM loser fund ids.
- **Fondbolagens Förening / Svensk Fondstatistik:**
  - quarterly fund assets by fund, 2000-2008 (D&M's own source);
  - fund capital by holder type, if it exists.
- **FTN** (offentlighetsprincipen): per-bid qualification status and quality scores.
- **Pensionsmyndigheten:** per-round counts of active versus default choices; the 2019 deregistration mapping.

### 5.4 Data rules (corrections confirmed by the referees)

- Raw data untouched, with download dates; every transformation in code; winsorise flows at 2.5% as in SSZ.
- Drop empty placeholder rows before dating exits. The 2019 exits hold SEK 87.7bn gross (84.1bn net of 16 renumberings), not 60.9bn.
- December placement into chosen (non-AP7) funds is SEK 16-19bn a year (2019-2025), not 47-51bn (that figure included AP7).
- Pensionsmyndigheten returns are integer-rounded: **rank on SHoF returns**.
- Linear-rank benchmarks are +0.185 (difference), 0.499 (sponsor) and 0.143 (participant), not the secant values 0.402 and 0.674.
- FTN column:
  - 24 of the 62 "removed" funds never bid, and at least 3 are winners at strategy level, hence the two-stage bid-level design;
  - the N = 81 sample spans 4 award dates, not 5;
  - power is about 57% against SSZ's sponsor column (10-20% at a plausible score-rank correlation).
- Fees: Sweden active before procurement is 0.303%. The withdrawer in the global index round was not qualified.
- **Definitional difference to state:** D&M's retail money is Swedish investors only (their footnote 4). Our non-PPM money is everyone else, including funds of funds.

---

## 6. Risks (S = could sink the thesis)

| # | Risk | Solution | Effect |
|---|---|---|---|
| **S1** | Read as "SSZ on Swedish data", off Klug's FTN topic | Build on D&M as the Swedish predecessor; FTN in the title, Table 1 panel B and Table 3; Klug's written yes | Reduces strongly |
| **S2** | Non-PPM money is not non-DC (unit-linked, occupational, foreign investors, funds of funds, which FJW show are the most sensitive clientele) | Asymmetric pre-registration; compare with SSZ's participant (0.143) and non-DC (0.310) columns; funds-of-funds exclusion row; holder-type data if available | Reduces |
| **S3** | Power depends on scale (55% against +0.075 annually) | Pre-registered monthly check (81%); SHoF data before 2018 | Solves if SHoF delivers |
| S4 | Novelty | The direction is published (D&M). Contribution = power, period, sponsor reading, FTN column. Checked 6 Oct: no academic work on FTN; FTN's own before/after numbers have no counterfactual; the Riksrevisionen audit (opened June 2026) covers transition efficiency, not flows or selection. Re-check the audit page in November | Reduces |
| S5 | Specification search (adding D&M rows after seeing results) | D&M rows are in the PAP before any coefficient is opened | Solves |
| 6 | 2019 re-registration and AP7 mapping | Drop flow-year 2019 | Solves |
| 7 | Robot switching before December 2011; advisers | Appendix panel from 2012; call flows "participant or adviser" | Solves / reduces |
| 8 | Mergers and family mappings | Flag same-company exits with a net-trading spike; drop those fund-years | Reduces |
| 9 | December placement | Year fixed effects; December-excluded row | Solves |
| 10 | FTN column misread or underpowered | Two-stage bid-level design; perfect-selection units; randomisation inference | Solves the misreading; power stays low |
| 11 | Missing FTN covariates (returns for 19 of 149 non-PPM losers; qualification status) | Re-date at bid deadlines; SHoF series for 82 losers; FTN request; three all-qualified rounds | Reduces |
| 12 | Fan-out | Five exhibits, the drop list | Solves if enforced |
| 13 | Over-claiming | Each claim gives our number, the benchmark (SSZ and/or D&M) and the bound in one sentence | Solves |
| 14 | Synopsis promises (fees, supply, active vs default) | Table 1 panel B; one cited sentence on the 85-95% default share; Klug's sign-off | Reduces |
| 15 | Lost derived data (5.2) | Rebuild in week 1 with saved code | Solves |
| 16 | AI-text rule | Write all thesis text yourselves; keep the AI log; AI appendix | Solves |

---

## 7. Message to Klug (send Tue 6 Oct; edit freely, it is an email)

> Hi Michael,
>
> Before we freeze our pre-analysis plan we'd like your view on two things.
>
> First, the A/B choice. A: test Sialm, Starks and Zhang's sponsor attribution on premium-pension data for 2020-2023 (MDE about 0.10 per year against their +0.185), with FTN's first selections as a bounded "new sponsor" column. B: a pure FTN selection study without a replication, whose main test only detects near-perfect return-based selection. We lean towards A. Are you fine with narrowing the synopsis's fee and supply promises to descriptive statistics?
>
> Second, we found Dahlquist and Martinez (2015, EFM), which compares PPM and retail flows in the same funds for 2000-2008. We plan to treat it as our direct predecessor: their specification goes in as a robustness row on our period, and we replicate their main table for 2001-2008 if SHoF can give us pre-2018 fund assets. Our contribution would then be a powered test after the reforms, read through the sponsor lens, just before FTN. Does that framing work for you? Do you think Magnus Dahlquist would be open to a short comment on the plan?
>
> We'll send the timestamped plan as soon as it's frozen.
>
> Best,
> Alexander and Ludvig

---

## 8. Rules for the whole project

1. No coefficient is opened before the PAP is frozen and timestamped. Anything added later is labelled exploratory.
2. One sentence per claim: our estimate, the benchmark, the bound.
3. Never "the sponsor caused". Say "consistent with" and name the alternative (participants; D&M's inattention; clientele mix).
4. Five exhibits. Something new replaces something; it is never added.
5. Write each table's sentence the day the table is finished.
6. Every evening: commit code, three lines of status. Every Friday: three-line status to Klug.
