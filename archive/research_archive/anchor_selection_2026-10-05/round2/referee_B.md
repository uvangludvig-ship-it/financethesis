# Referee report on candidate (B): Cookson, Jenkinson, Jones and Martinez (2021 RFS)

Role: examiner, hostile but fair. Target: `round1/cookson_dossier.md` and `round1/cookson_work/`. Written 5 Oct 2026.
My scripts: `round2/ref_b_work/` (`iv_placebo.py`, `iv_placebo2.py`, `iv10.py`, `removal_mechanics.py`, `selection_logit_se.py`). I reran `cookson_power.py`, `moments.py`, `ppm_pretransfer_power.py` and `post_transfer_power.py` unchanged; their output files are byte-identical to before.
Blindness: I never computed a winner-minus-loser estimate, a selection coefficient or a loser average over the (iv) windows. To diagnose the removal mechanics I did look at removed funds' month-by-month capital in months with outflows above 20%.

---

## 0. Verdict

- Most of the dossier's numbers reproduce. Its two new claims do not survive.
  - **Test (iv), voluntary exits between award and removal.** The a+1 window falls **before the saver letters in every round**. After the letters, the measure is mixed up with two mechanical effects: funds closed for new choices, and **staged transfers**. Those are 26 months with outflows of 20 to 60%, in 16 of 66 removed funds holding 63% of removed capital, and all of them pass the dossier's -60% filter. The MDE is understated by about 2x: event-level inference gives 1.6 to 2.2%, not 0.77 to 1.51%. The CJJM conversion has the wrong units. **Not a credible headline (FATAL as specified).**
  - **"Selection powered against a CJJM-sized gap."** The comparator is wrong. CJJM's Table 4 gap is a stock gap over fund-months. At the addition decision (Table 5), the 3-year percentile coefficient is 0.31 (z = 0.63). Our logit MDE is 1.9, about six times that. On top of this, the returns are dated 5.5 to 12 months after the bid deadline.
- (B) has no replication in the course's sense, and its question loses CJJM's core (conflicts of interest). After the fixes it is a bounded-null selection study plus a descriptive fee table.
- Rubric: B falls from 48/90 to **33/90 (37%)**, or **44/90 (49%)** in its best version, against A's audited 69/90.
- **(B) should not beat (A).** B's one usable piece, the selection test, belongs in A's Table VIII FTN column with my corrections.

---

## 1. Verification of the dossier's load-bearing claims

| # | Claim | Check | Status |
|---|---|---|---|
| 1 | Table 6 col (3): 0.16 (t 5.42), full sample | `t6-41.png`, p. 40 | CONFIRMED |
| 2 | Table 6 col (11): 0.06 (t 1.91), post-RDR | same | CONFIRMED |
| 3 | Text cites "column (4)" for 0.16 | txt L1175-1179 | CONFIRMED (manuscript slip) |
| 4 | Fn 22: platform share 15-20% gives 9.6-13.8% annualized | txt L1217-1219 | CONFIRMED as quoted. CJJM's own arithmetic is off: 1.92/0.15 = **12.8**, not 13.8. The 15-20% is a share of the **D2C platform market**, not of fund AUM (see 2.6) |
| 5 | Figure 1A: deletion outflows about 2 months; R+1 about -0.10 (CI includes 0), R+2 about -0.17 (significant), R+3/R+4 near 0 | `f1-45.png`, p. 44 | CONFIRMED (read from the figure) |
| 6 | Table 7B platform-only 0.34% (t 0.71); post-RDR 0.81 (2.17) | txt L2249-2275 | CONFIRMED |
| 7 | Table 4 percentile gaps 6.70 and 14.92 | txt L2113-2115 | CONFIRMED, but these are **stock** gaps over 20,461 vs 309,714 platform-fund-months. At addition (Table 5, L2165-2167) the coefficients are 1-year -0.54 (z -1.32) and 3-year 0.31 (z 0.63). Deletions load on 3-year performance at -0.93 (z -2.67), which inflates the stock gap |
| 8 | 290 bids, 75 winners, 11 rounds | `bids_long_final.csv` | CONFIRMED |
| 9 | 142 bids with 12-month returns (58 winners, 11 rounds); 139 with 36-month returns (57) | same | CONFIRMED. Of the 84 losers with returns, 65 are PPM incumbents |
| 10 | Three all-qualified Swedish rounds; 57 bids, 25 winners, 32 losers | Sverige Aktiv L714 "Alla inkomna anbud uppfyllde kraven"; Sverige Passiv L675-676 "Alla anbud uppfyllde kraven"; Sverige småbolag L1027-1028 "Samtliga 19 anbud uppfyllde de obligatoriska kraven" | CONFIRMED |
| 11 | Global index withdrawer counted as a qualified loser | Global index L713-715: withdrew because it "inte kommer att leva upp till ett obligatoriskt krav" | CORRECTED: the bid was effectively unqualified, so **141** qualified losers |
| 12 | Fees before → after: Europe active 0.48→0.21; Nordic small 0.515→0.244; technology 0.396→0.194; Europe small 0.398→0.321; global active 0.371→0.186 | report summaries (e.g. Europa L79-80; Nordisk småbolag L66-67; Teknologi L72-73) | CONFIRMED (5 rounds) |
| 13 | Sweden active fee "corrected" to 0.309 | Sverige Aktiv: 0.303 at L72, L549 (as of 31 Jul 2025) and L1593; 0.309 only at L1476 ("vid tidpunkten för upphandlingens annonsering") | CORRECTED: the report is internally inconsistent. Its headline is 0.303 (-14.9 bp). Before-fee reference dates also differ across rounds |
| 14 | Outside-PPM flows: sd 2.2-3.1% per month, within-fund AR(1) 0.10-0.16 | reran `moments.py` | CONFIRMED (3.12/0.149 all SEK funds; 2.25/0.155 bidders; 2.16/0.105 winners) |
| 15 | Selection MDE 15.0 (1-year) and 15.3 (3-year) points | reran `cookson_power.py` | CONFIRMED arithmetically. The comparison with CJJM is invalid (item 7; section 3.4) |
| 16 | Outside-flow MDE 3.5-3.6% (3-month DiD), 4.7% at real N; 6.3-7.3% and 9.0% (6 months) | same | CONFIRMED |
| 17 | Performance MDE 3.5% per year pooled; 3.0-9.1% for single rounds | same | CONFIRMED (3.54) |
| 18 | (iv) MDE 0.77 / 1.51% (k=1) and 1.32 / 2.23% (k=2), N 50 / 74 | reran `ppm_pretransfer_power.py` | CORRECTED. The saved script (1% winsorization) gives **1.45 / 2.54** (k=1) and 2.57 / 3.34 (k=2). The dossier's numbers reproduce only with an undisclosed 2.5% winsorization. Event-level inference gives **1.59-1.70 (≥ SEK 100m) and 2.15 (≥ SEK 10m)** (section 2.4) |
| 19 | (v) winners' MDE 0.67% per month, N 32 | reran `post_transfer_power.py` | CONFIRMED arithmetically. The design is contaminated (S6) |
| 20 | Removed classes: 38 bid and lost, 26 never bid, 2 won through another class | `ssz_cross_section_fundlevel.csv` | CONFIRMED. Two "removed" classes are misdated: Odin Europa C was last seen Feb 2024, before the R1 award; Öhman Marknad Europa A until Feb 2025, 11 months after it |
| 21 | 85-95% of savers follow the default (brief: NOT VERIFIED) | Dagens PS, 8 Oct 2025, quoting Pensionsmyndigheten | CONFIRMED at press level. **This undercuts the headline (S10)** |
| 22 | FCA OP30 "1% of AUM"; published RFS tables | not re-fetched; OUP paywall | UNVERIFIABLE here |

---

## 2. Test (iv), the voluntary-exit headline

### 2.1 How and when savers are informed (VERIFIED unless marked)

- **FTN reports, §3.7 (every 2025-26 report; e.g. Sverige småbolag L740-784):**
  - The incumbents' contracts are terminated **when the procurement is announced**, 8 to 13 months before the award ("I samband med att en upphandling ... annonseras sägs fondavtalen upp").
  - The award becomes final after a 10-day standstill.
  - "Efter avslutad upphandling meddelar Pensionsmyndigheten de sparare ...", and "En sparare kan när som helst byta fond".
- **Press timeline (pensionsmyndigheten.se and ftn.se are blocked by the container proxy, 403 CONNECT):**

| Round | Announced | Bid deadline | Award | Losers closed / winners admitted | Letters | Saver deadline | Losers last in file |
|---|---|---|---|---|---|---|---|
| R1 Europe active | 30 Jun 2023 | 5 Oct 2023 (report timeline) | 25 Mar 2024 | Jun 2024 | after the award is final and the new funds are listed; transfer "till sommaren" (Placera, 25 Mar 2024) | n/v | May-Jun 2024 (gap 2-3 months) |
| R2 index | 29 Feb 2024 | n/v | 31 Oct 2024 | Feb/Mar 2025 | Mar 2025: "letters being sent" (Dagens PS, 21 Mar 2025) | 27 Mar 2025, 270,000 savers, "few have reacted so far" (Dagens PS, 27 Mar 2025; category not named, probably R2) | Feb-May 2025 (gap 4-7) |
| R3 Nordic | 29 Apr 2024 | n/v | 19 Feb 2025 | Apr 2025 | n/v | n/v | Apr-Jun 2025 (gap 2-4) |
| R4 Sweden | 9 Sep 2024 | 14 Nov 2024 (timeline graphic; label partly lost) | 27 Aug 2025 | Oct 2025 (passive), Dec 2025 (active) | active: "I månadsskiftet" Oct/Nov 2025, 149,000 savers (Dagens PS, 8 Oct 2025) | n/v | Oct 2025 to May 2026 (gap 2-9) |
| R6 Sweden small | 29 Apr 2025 | evaluation Jun-Dec 2025 | 28 May 2026 | **not selectable from 18 Aug 2026** (Dagens PS, 20 Aug 2026) | Aug-Sep 2026 | **25 Sep 2026** (EFN, 3 Sep 2026) | still listed Aug 2026 |

- **Implication.** Letters arrive around winners' admission, 2 to 5 months after the award, with a deadline about 3 to 6 weeks later. The dossier's a+1 month (Apr 2024, Nov 2024, Mar 2025, Sep 2025, Jun 2026) **precedes the letters in every round**. It can catch only savers who react to press coverage of the award, and the agency reports few acting even in the deadline week.

### 2.2 Can a saver switch before removal, and does it show in `nt`? (VERIFIED)

- Yes on both counts.
  - Switching is allowed "när som helst" (FTN §3.7.1).
  - `nt` is the month's net SEK flow, including switches (SSZ dossier §3.2, asset-identity gap 0.015-0.03%).
- But two mechanical effects enter the same series:
  - **Closure.** From closure (e.g. 18 Aug 2026), losers receive no new choices. Net flow then falls by the lost gross inflow, even with zero extra exits. Gross flows are not in the files.
  - **Staged transfers** (`removal_mechanics.py`). After the award, removed funds have **26 months with -60% < nt/mv_l < -20%, in 16 of 66 funds holding SEK 46.3bn of 74.0bn**, at event months 2 to 9. Examples:
    - Länsförsäkringar Global Index: capital ratios 0.44, then 0.34 in its last two months;
    - Spiltan Aktiefond Småland: drops Jan, Mar, Apr and May 2026;
    - Handelsbanken Sverige A1: 0.51.
  - Only 31% of last-observed months fall below -60%. The dossier's rule ("drop months with nt ≤ -60%") therefore keeps most transfer tranches as "voluntary exits".

### 2.3 Window length and comparability

- The award-to-last-seen gap ranges from 2-3 months (R1) to 2-9 months (R4 Sweden active).
- The treated period (letter to deadline) is about one month and falls in a different award-month in each round.
- So the window is neither long nor identical across rounds. In letter time it is short and sits next to the closure and the tranches.

### 2.4 Inference (`iv_placebo.py`, `iv_placebo2.py`, `iv10.py`)

- **The dossier's SE assumes independent funds.** It uses placebo sd / √N, with fund-level draws at -24, -36 and -48 months. But all losers in a round share one award date, and there are only 5 award dates.
- **Event-level randomization** (one common placebo month per award group; N-weighted pool; 20,000 draws; months adjacent to December and the year 2019 excluded):

| Sample | Dossier-style SE / MDE | Event-level SE / MDE | Power for a 1% effect |
|---|---|---|---|
| ≥ SEK 100m, N 50 | 0.276 / 0.77 | **0.609 / 1.70** (0.567 / 1.59 with all months) | 95% → **about 37%** |
| ≥ SEK 10m, N 74 | 0.538 / 1.51 | **0.768 / 2.15** | about 46% → about 13% |

- Group-level placebo sd exceeds the iid value by a factor of up to 1.9; the largest gap is the R4 group of 21 funds (0.84 against 0.45).

### 2.5 December placement and month-median adjustment

- The December placement is large and dispersed. Its median is 1.0 to 2.7% of PPM capital in 2018-2025, with a p10-p90 span of about 2.5 to 4 points (≥ SEK 100m funds).
- **k=1 windows avoid December.** The R2 k=2 window includes Dec 2024; the placebo absorbs the noise but not a fund-specific mean shift.
- **R4 Sweden active** has December 2025, the admission month, inside its award-to-removal window. If closed losers' placements went to the replacement fund (NOT VERIFIED), the median adjustment books about **-1 to -2.7%** of capital as "voluntary exit". That is larger than any claimed MDE.
- The cross-sectional median removes the market-wide month effect, but not category shocks. Event-level inference or a matched control category is needed.

### 2.6 Churn placebo and pre-award baseline (no treatment effects inspected)

- **Placebo on funds not removed:** all non-FTN funds at the five real award dates, same k=1 statistic.
  - Means are +0.61, +0.03, +0.17, +0.44 and -0.56; fund-level sd is 3.5 to 5.3.
  - Date-level common shocks are therefore as large as the claimed MDE. Any (iv) estimate must be differenced against such a control, and inference must be event-level.
- **Pre-award baseline for losers.** Month-adjusted PPM flow is -0.02 (a-12 to a-7) and +0.14 (a-6 to a-1) % per month, with medians 0.00 and 0.05. The same windows two years earlier give +0.34 and +0.10.
  - So there is **no pre-trend**: losers are not already bleeding.
  - This holds even though both windows come after the announcement, when contracts are terminated. This part of the design is sound.

### 2.7 CJJM equivalence (fn 22)

The conversion is not defensible.
1. **Wrong units.** The dossier takes -0.10 - 0.17 = -0.27% of fund AUM and divides by 0.15-0.20 to get "-1.4 to -1.8% of platform capital". But 15-20% is the platform's share of the D2C market. Dividing by it gives the fund-AUM flow if all D2C platforms acted, which is still in fund-AUM units.
   - Converting to "% of capital held through the platform" needs the platform's holding of each fund relative to that fund's AUM, which CJJM do not report.
   - If that holding is a few percent, CJJM's deletion effect is roughly 5 to 30% of platform-held capital, an order of magnitude above the dossier's benchmark (JUDGEMENT).
2. **Wrong object.** A CJJM deletion leaves the fund purchasable. An FTN loser is about to be force-moved. Pre-removal exits have no CJJM counterpart.
3. **The same error inflates (v)'s "1.0-1.3% of platform capital".**

### 2.8 Decision on test (iv)

- **Not a credible headline.** As specified, (iv) measures a month with no letters, and that month is not powered against plausible press-driven exits.
- In the month that carries the letters, voluntary exits cannot be separated from closure and tranches without the transaction-type ledger.
- Even if the ledger arrives, the answer to the headline question is already public in saver terms (85-95% default).
- It can survive only as a descriptive, capital-weighted, round-by-round share, built from Pensionsmyndigheten records.

---

## 3. Anchor fit

1. **What is left of CJJM's question without conflict variables?**
   - CJJM's abstract is about conflicts (txt L4-15): platforms favour own-brand and high-commission funds, and a ban on commission sharing improved recommendations.
   - FTN has no affiliation, no revenue share and no RDR-type ban. It is also **not a recommendation**: it is a menu restriction with default reassignment, which is closer to SSZ, Pool-Sialm-Stefanescu and Cronqvist-Thaler.
   - What remains is generic: the determinants, influence and value of a list. The "incumbency or bank-group falsification" is not CJJM's variable.
   - The closest surviving CJJM object is Table 7B and IA.4, the unconflicted Morningstar benchmark. Its Medalist history is not in hand.
2. **Is "adaptation" a replication in the course's sense? No.**
   - The course sets "replication and extension" as the standard (course_intro L142).
   - It wants replication of "the main quantitative exercise" (L272) as "a guarantee of solid foundations such that we can trust your results" (L428). The syllabus allows "(partially) replicate" (L143).
   - "Same method but different question" is listed as an **extension** type (L148). An adaptation with no anchor number to reproduce does not validate the code or the method.
   - This is "departing from the suggested format", which the course calls risky (L152).
3. **One question or several? Several.**
   - The dossier states one question (§4.1) but runs seven tables answering five: selection, voluntary flows, outside flows, performance and fees.
   - The briefing's version has two (outside flows and selection).
   - This is the SFDR 6045 pattern (four outcomes, did not win).
4. **Is the bid-level selection test confounded?**
   - **(a) Qualification screen.** 63 of 290 bids (22%) failed it, on administrative completeness, a 3-year strategy record, active-risk bands and ESG minimums (Europa report L268-282). P(win | bid) mixes this rule-based screen with FTN's quality evaluation. Active-risk and ESG screens correlate with tail returns, for example the energy exclusions in 2022.
   - **(b) Sample.** Returns exist for 84 of 215 losers, 65 of them PPM incumbents. The test is effectively winners against incumbent losers.
   - **(c) Selection into bidding.** The pool is truncated on expected quality, so within-pool percentile gaps are attenuated relative to CJJM's category-universe percentiles. The two are not comparable.
   - **(d) Appealed round.** Global active is 34% of bids and 23% of the returns sample, and its award is not final.
   - **(e) Timing.** Returns end at award-1, which is 5.5 months (R1) to about 12 months (R6) after the bid deadline. The 12-month window is mostly outside FTN's information set.
   - **(f) Comparator.** Logit MDE on our data is 1.82 (1-year) and 1.91 (3-year), on a 0-1 percentile scale (`selection_logit_se.py`). CJJM's addition coefficients are -0.54 and 0.31, so power against them is about 5%.

---

## 4. Issues, classified, with fixes

| ID | Issue | Fix | Solves? |
|---|---|---|---|
| **F1** | **(iv) is unidentified as specified:** a pre-letter month, then closure and tranche contamination, a -60% filter that keeps tranches, no ledger (2.1-2.3) | Event time in letter dates. Obtain per-fund active-switch and default counts and capital per round from Pensionsmyndigheten (begäran om allmän handling); they already publish the 85-95%. Or obtain the ledger. Drop (iv) as a test | Fully solves measurement **if granted**. The result is then a descriptive share, not a CJJM test, so it does not rescue (iv) as a headline |
| S1 | (iv) SE ignores the common award date; MDE understated about 2x; winsorization undisclosed (2.4; item 18) | Event-level randomization inference; disclose the specification | Fully solves the inference; power does not recover |
| S2 | CJJM conversion has the wrong units and object; the same error affects (v) (2.7) | Delete it; state that no CJJM benchmark exists | Fully (by deletion) |
| S3 | Selection benchmark is a stock gap; the decision-level CJJM effect is near zero; logit MDE about 6x CJJM | Estimate CJJM Table 5's logit and print CJJM's addition coefficients beside it as a bounded result. Request FTN's per-bid **quality scores** (the 2026 reports already print anonymous score dots), giving a continuous outcome | Fixes the claim fully. Power improves only if scores are released (NOT VERIFIED) |
| S4 | Return covariates dated after the bid deadline | Date at each round's bid deadline | Fully |
| S5 | Screen, incumbency-tilted sample, appealed round, truncated pool (3.4) | Headline P(win \| qualified) once FTN releases status; exclude global active from the main table; Lee bounds otherwise; SHoF series for non-PPM losers | Reduces (fully if FTN releases status) |
| S6 | (v) contaminated. For 14 of 54 winners (all 9 Sweden active), the t+2 to t+7 window overlaps same-round loser tranches. The max-inflow rule picks wrong months (Nordic small 2025-12, Europe active 2024-04). Menu effect | Start the window after each round's last loser tranche (taken from loser capital paths); compare with non-procured categories; check the allocation formula | Reduces |
| S7 | No replication in the course's sense (3.2) | Partial replication of CJJM Table 4/7A on a public UK best-buy list (HL Wealth 50/150 archives) with UK fund returns. SHoF UK coverage NOT VERIFIED; costly with 9 weeks left | Reduces at best |
| S8 | Anchor question loses CJJM's core (conflicts); FTN is a menu, not a recommendation (3.1) | Reframe as "certification without conflicts" against CJJM Table 7B/IA.4; needs Medalist history | Reduces |
| S9 | Fan-out: five questions in seven tables | One question, at most two exhibits | Fully, if enforced |
| S10 | The headline's answer (default share) is already public | Capital-weighted, round-level shares and timing from records; do not claim it as a finding | Reduces |
| S11 | Window heterogeneity: letters at a+2 to a+5, gaps 2-9 months | Letter-date event time (press and fondhändelsebrev; agency sites blocked here) | Reduces |
| S12 | December placement and closure in R4 Sweden active; Dec 2024 in R2's k=2 window | Seasonal (December-on-December) baseline; drop December; verify the placement rule for closed funds | Fully if the rule is verified, otherwise reduces |
| M1 | Sweden active fee 0.303 vs 0.309; inconsistent reference dates | Report both; one convention across rounds | Fully |
| M2 | Misdated losers (Odin Europa C; Öhman Marknad Europa A) | Hand-check the last-seen month against the award | Fully |
| M3 | CJJM fn 22 arithmetic slip (12.8 vs 13.8) | Note it | Fully |
| M4 | Outside-PPM "CJJM-implied 0.48%" is an inside-platform effect; CJJM have no outside benchmark | Relabel. "Unpowered" holds even more strongly | Fully |
| M5 | "Morningstar ratings have no direct effect (col 3)" | Text p. 21: five-star has a significant direct effect (cols 1-2, 0.07, t 2.74). Cite accurately | Fully |
| M6 | Returns from the most-observed share class, not the bid class (fee-class noise) | Use the PPM or bid class, or fund-level returns | Fully |
| M7 | Coarse within-round ranks (5-9 bids with returns in 4 rounds); CJJM rank within the whole category | Category-universe percentiles from SHoF | Fully if universe returns are obtained |
| M8 | Published RFS version unchecked (dossier flags it) | SSE network | Fully |

---

## 5. Re-score on the winners-audit rubric

Weights as in `winners_audit.md` §5; scores run from 0 to 5.

| # | Criterion (weight) | B, audit | B, corrected | Reason | B, best version |
|---|---|---:|---:|---|---:|
| 1 | Same-question top anchor (2) | 3 | 2 | Conflicts gone; menu, not recommendation | 2 |
| 2 | Table-level replication (3) | 2 | 1 | None possible; adaptation is an extension | 1 |
| 3 | Mechanism inside the anchor's specification (2) | 2 | 2 | Table 5 bid margin and Table 8 A/B/C rows stay | 2 |
| 4 | One headline question (2) | 3 | 2 | Five questions | 4 |
| 5 | Informative result / power (3) | 2 | 1 | Selection about 5% power against CJJM's decision effect; (iv) MDE x2 and pre-letter; (ii) and (iii) unpowered; fees exact but descriptive | 2 |
| 6 | Identification from the institution (2) | 4 | 3 | Dated awards, but letters staggered, closure and tranches | 3 |
| 7 | Avoids failure modes (2) | 2 | 1 | 6045 fan-out plus a headline that cannot be measured | 3 |
| 8 | Institutional data (1) | 4 | 3 | Ledger, letter dates, non-PPM loser returns and scores missing | 3 |
| 9 | Tutor fit (1) | 4 | 4 | Selection design | 4 |
| | **Weighted (max 90)** | **48 (53%)** | **33 (37%)** | | **44 (49%)** |
| | Equal weights (max 45) | 26 | 19 (42%) | | 24 (53%) |

A's audited score is 69/90 (77%). I did not referee A, so that number is not mine.

---

## 6. The best version of (B), and B against A (at most one page)

**Question.** What does an unconflicted public gatekeeper select on? This is CJJM's Table 5, with FTN in the role of CJJM's unconflicted Morningstar benchmark (Table 7B, IA.4).

**Design.**
1. Round table (T1), with qualification counts and the Sweden active fee at 0.303 and 0.309.
2. Logit and LPM of win on covariates **dated at each bid deadline**:
   - covariates: fee, 1- and 3-year **category-universe** percentiles, log size, age, active risk, incumbency;
   - sample: P(win | qualified) where status is known (the three Swedish rounds now, all rounds if FTN releases status), excluding the appealed global round;
   - CJJM's addition coefficients (-0.54, 0.31) printed beside it;
   - inference by randomization within round.
   - With FTN per-bid quality scores (records request), the outcome becomes continuous; that is the only route to real power.
3. Table 8 analog: category, same-fund and replacement fee rows (exact).
4. Voluntary versus default: a descriptive, capital-weighted, round-by-round share from Pensionsmyndigheten records, explicitly **not** a CJJM test.
   - Outside-PPM flows and performance are dropped, or kept as one bounded-null appendix line each.

**What it delivers.**
- One question, honest bounds, exact fees and good tutor fit.
- Still no replication. The selection test detects only strong selection unless scores arrive, and part of its answer (75% quality, 25% price) is published by FTN.

**B against A.** **B should not beat A.**
- Even at its best, B scores 44/90 against A's audited 69/90.
- It fails the course's stated standard (replication), and its new headline does not survive scrutiny.
- B's one durable contribution is the corrected bid-level selection test: bid-deadline dating, P(win | qualified), the appealed round excluded, event-level inference. It fits inside A's Table VIII FTN column, so the real choice is A with B's corrected selection test.
- What would reopen the question: FTN releases per-bid scores and status, **and** Pensionsmyndigheten releases per-fund active-choice data. Even then B gains power and description, not a replication.

---

### Sources (web, fetched 5 Oct 2026)
- Dagens PS, 20 Aug 2026: https://www.dagensps.se/privatekonomi/har-du-nagon-av-de-har-fonderna-da-flyttas-dina-pengar/
- EFN, 3 Sep 2026: https://efn.se/nu-flyttas-ppm-pengarna-da-behover-du-agera
- Dagens PS, 8 Oct 2025: https://www.dagensps.se/privatekonomi/149-000-pensionssparare-berors-fonder-forsvann-fick-du-brevet/
- Dagens PS, 27 Mar 2025: https://www.dagensps.se/fonder/tvingas-byta-fonder-nu-far-hundratusentals-pensionssparare-brev/
- Dagens PS, 21 Mar 2025: https://www.dagensps.se/privatekonomi/pension/nu-far-tiotusentals-svenskar-brev-tvingas-byta-fonder/
- Placera, 25 Mar 2024: https://placera.se/kommentar/forsta-kategorin-ppm-fonder-klar-2024-03-25
- FTN reports (local `scratchpad/ftn_txt/`; Cision copies at mb.cision.com/Main/23067/...)
- pensionsmyndigheten.se and ftn.se: blocked by the container proxy (403), not consulted directly.
