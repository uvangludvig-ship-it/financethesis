# Step by step to submission (5 October to 7 December 2026)

Goal: a thesis an examiner cannot fault on design, honesty or execution. No thesis is flawless. But almost every failure we saw in the winners/non-winners audit comes from one of five things: an unclear question, an untested anchor, results chosen after the fact, over-claiming, and sloppy finishing. Each step below closes one of those. Tick the boxes as you go.

Fixed dates: **PAP frozen Fri 9 Oct**, **data freeze Sun 1 Nov**, **full draft to Klug Mon 23 Nov**, **submission Mon 7 Dec**. Check the course page for any interim deadline (mid-term seminar, opposition) and slot it in.

---

## Week 1 (Mon 5 to Fri 9 Oct): lock the design

**Mon-Tue: requests out (everything else waits on these)**
- [ ] SHoF:
  - monthly TNA and returns before 2018 for all PPM-linked fund ids;
  - quarterly fund assets for 2000-2008, for the D&M replication;
  - series for the 82 matched non-PPM loser fund ids.
- [ ] Fondbolagens Förening / Svensk Fondstatistik:
  - quarterly fund assets by fund, 2000-2008 (D&M's own source);
  - fund capital by holder type, if it exists.
- [ ] FTN (offentlighetsprincipen): per-bid qualification status and quality scores.
- [ ] Pensionsmyndigheten:
  - per-round counts of active versus default choices;
  - the 2019 deregistration mapping.
- [ ] Send Klug the message in `REVISED_PLAN_2026-10-05.md` §6: the A/B question plus D&M. Ask for a short meeting this week.

**Tue-Wed: novelty and literature**
- [ ] Search DiVA directly for "Fondtorgsnämnden", "upphandlat fondtorg", "premiepension flöden".
- [ ] Check the status of Riksrevisionen's audit "Ett upphandlat fondtorg för premiepensionen".
- [ ] Read in full and take one page of notes each:
  - Keim and Mitchell (2018);
  - Fricke, Jank and Wilke (2026);
  - Evans and Fahlenbrach (2012).
- [ ] Get the D&M published PDF into the reference manager (done: `round3/dahlquist_martinez_2015_EFM.pdf`).

**Wed-Thu: data hygiene (no coefficients)**
- [ ] Drop placeholder rows, flag mergers, unify flow definitions (SSZ eqs. (1)-(2) for both groups).
- [ ] Build the quarterly PPM flow from monthly "Handel, netto" for the D&M rows.
- [ ] Rank on SHoF returns. Code FTN covariates at bid deadlines and strategy-level fund identity.
- [ ] Read the Fondstatistik fee headers. Verify the Table IX performance unit on SSZ p. 833.

**Thu-Fri: freeze the pre-analysis plan (PAP)**
- [ ] One document covering:
  - question, specification, hypotheses with the D&M cross-check (about −0.18), MDEs, pre-committed reading;
  - the five exhibits including the D&M rows, the drop list and the conditional-appendix rule.
- [ ] Recompute the power table under the frozen spec (standard errors and MDEs only).
- [ ] Timestamp it (email to Klug and to yourselves, plus a git commit) and **do not open coefficients before this**.

## Week 2 (12 to 16 Oct): headline

- [ ] Table 1 (descriptives, SSZ Table I with D&M benchmark; panel B: FTN rounds).
- [ ] Figure 1 (flows by prior-return percentile, PPM vs non-PPM, SSZ values overlaid).
- [ ] **Table 2 headline row**: run exactly as pre-registered. Write the one-sentence result (our Δ, SSZ's +0.185, D&M's gap, the CI) the same day, before any robustness.
- [ ] Meet Klug with the headline number.

## Week 3 (19 to 23 Oct): Table 2 complete

- [ ] Piecewise rows and tail MDEs; the secondary tail contrast.
- [ ] Robustness rows:
  - monthly; 2019 included; December excluded; within-category rank; category clustering;
  - **D&M quarterly system rows**; funds-of-funds families excluded.
- [ ] Anything not pre-registered goes in a clearly labelled "exploratory" paragraph or not at all.

## Week 4 (26 to 30 Oct): Table 3, the new sponsor

- [ ] Stage 1: P(bid | incumbent), N 87. Stage 2: P(win | bid) on 36- and 12-month category percentiles at bid deadlines (N 110; N 142 with the appealed round).
- [ ] Randomisation inference within round. Report as a fraction of the perfect-selection slope, beside SSZ's sponsor and participant columns.
- [ ] Describe the equal-split dose rule; do not estimate it.

**Sun 1 Nov: data freeze.** Nothing new enters after this. If pre-2008 quarterly assets have not arrived, drop the D&M replication and note it in one sentence.

## Week 5 (2 to 6 Nov): Table 4 and the conditional appendix

- [ ] Table 4 (SSZ Table IX): next-year raw and category-adjusted performance on lagged PPM and non-PPM flows, SSZ beside.
- [ ] If data arrived: replicate D&M Table 2, Systems I-IV, 2001-2008. Compare coefficient by coefficient with p. 11 and explain every gap larger than one standard error.
- [ ] Appendix: Table II; 2019 as a rule-change year; PPM-only panel 2012-2023.

## Week 6 (9 to 13 Nov): write the solid parts

- [ ] Institutional background:
  - PPM, the 2019-2022 reforms, FTN;
  - Table 1 panel B facts, each with a source;
  - the 85-95% default-share sentence.
- [ ] Data section: every source, every filter, every count (the referees' corrections in §4 of the final decision).
- [ ] Method section: SSZ spec, D&M spec, deviations from both stated in a table.
- [ ] Code: one script per exhibit, run end to end from raw files on a clean machine.

## Week 7 (16 to 20 Nov): write the hard parts

- [ ] Results: each paragraph opens with the number, the benchmark (SSZ and/or D&M) and the bound, in one sentence.
- [ ] Literature review: SSZ, D&M, clienteles (FJW, Jank, Keswani-Stolin), sponsors and governance (Evans-Fahlenbrach, Tang et al., Keim-Mitchell), public curation (Koh-Mitchell, Kavourakis-Tanewski), gatekeepers (Cookson et al., JJM).
- [ ] Introduction last but one; conclusion last. Calibrate the conclusion with `conclusions_winners_vs_nonwinners.md`: no claim stronger than the CI.

## Week 8 (23 to 27 Nov): review

- [ ] **Mon 23 Nov: full draft to Klug.**
- [ ] Independent referee pass: someone (or a fresh AI agent) who has not seen the work reads only the PDF and lists every claim not backed by a table. Fix each one.
- [ ] Number audit: every number in the text traced to a table cell or a cited page.
- [ ] Reproduce all exhibits from the frozen data one more time.

## Week 9 (30 Nov to 4 Dec): finish

- [ ] Incorporate Klug's comments.
- [ ] References: 20-30, every one cited and every citation listed. Check years, volumes and pages (D&M: EFM 21(1), 1-19).
- [ ] AI-use appendix: what was used, for what, and what you verified yourselves.
- [ ] Format rules (no table of contents, length, fonts). Proofread twice, once on paper.
- [ ] **Submit Mon 7 Dec.**

---

## Rules that hold the whole way

1. **No coefficient before the PAP is frozen.** Every later change is labelled exploratory.
2. **One sentence per claim:** our estimate, the benchmark, the bound.
3. **Never say "the sponsor caused".** Say "consistent with" and name the alternative (participants; D&M's inattention).
4. **Five exhibits.** If something new seems essential, it replaces something; it is not added.
5. **Write as you go.** A table without its sentence written the same day is not finished.
6. **Every Friday:** commit code, update the plan file, send Klug a three-line status.
