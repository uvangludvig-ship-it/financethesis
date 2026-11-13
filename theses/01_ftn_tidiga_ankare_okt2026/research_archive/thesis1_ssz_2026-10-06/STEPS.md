# STEPS.md: gates, steps and dates

Companion to `PLAN.md`. Aggressive schedule: **full draft to Klug Mon 2 Nov, submission-ready Fri 20 Nov**, then a buffer up to the hard deadline (Mon 7 Dec, 10:00). The headline needs no new data, so nothing on the critical path waits for a request.

**Two tracks.** The person who builds the panel does not write the introduction.
- **Alexander:** data, code, exhibits, replication package.
- **Ludvig:** literature, institutional background, writing, references.

Swap and review every Friday.

---

## The nine gates

Each gate must be passed before the work behind it counts. Gates 1, 3 and 4 decide the thesis; the rest is execution.

| # | Gate | Passed when | Target |
|---|---|---|---|
| 1 | **Klug says yes to A** and to the D&M framing | Written answer | Fri 9 Oct (if he prefers B, stop and re-plan) |
| 2 | **Data passes identity checks** | Flows reconcile with fund sizes (gap about 0.015-0.030%); placeholder rows dropped; mergers flagged; bid file and panel rebuilt with code; Table 1 plausible next to SSZ | Wed 7 Oct |
| 3 | **PAP frozen and timestamped** (incl. D&M rows and the −0.18 cross-check) | Emailed to Klug and yourselves, plus a git commit | Thu 8 Oct |
| 4 | **Headline result** | Table 2 headline row run exactly as registered; one-sentence reading written the same day | Fri 9 Oct to Sun 11 Oct |
| 5 | **FTN column** | Table 3 reported in perfect-selection units with randomisation inference | Fri 16 Oct |
| 6 | **Data freeze** | Nothing new enters; D&M 2001-2008 data either in hand (cutoff Fri 30 Oct) or that appendix dropped | Sun 25 Oct |
| 7 | **Full draft** | Every claim traces to a table cell or a cited page | Mon 2 Nov |
| 8 | **Outside referee read** | Someone who has not seen the work lists unsupported claims; all fixed | Fri 13 Nov |
| 9 | **Klug's sign-off and submission** | Canvas plus replication zip to Anneli Sandbladh | Ready Fri 20 Nov; deadline Mon 7 Dec 10:00 |

---

## Steps, in order

### Week 1 (Tue 6 to Sun 11 Oct): design locked, headline run
- [ ] **Tue 6 (both):** send all requests (`PLAN.md` §5.3) and the Klug message (§7). Start the AI log.
- [ ] **Tue 6 to Wed 7 (Alexander):**
  - rebuild the panel and bid file from raw data with saved code (§5.2);
  - drop placeholders, flag mergers, unify flow definitions (SSZ eqs. 1-2);
  - build the quarterly PPM flow for the D&M rows;
  - rank on SHoF returns;
  - code FTN covariates at bid deadlines and strategy-level identity. **Gate 2.**
- [ ] **Tue 6 to Wed 7 (Ludvig):**
  - read Fricke-Jank-Wilke, Keim-Mitchell and Evans-Fahlenbrach (one page of notes each);
  - ~~DiVA search and Riksrevisionen audit status~~ done 6 Oct (`research/literature/anchor_sweep_final_2026-10-06.md`); re-check the Riksrevisionen page in November;
  - verify the Table IX unit on SSZ p. 833.
- [ ] **Wed 7 (both):** recompute the power table under the frozen spec (standard errors and MDEs only). Write the PAP.
- [ ] **Thu 8:** freeze and timestamp the PAP; send to Klug. **Gate 3.**
- [ ] **Fri 9 to Sun 11 (Alexander):** Table 1, Figure 1, then the **Table 2 headline row**. Write its sentence the same day. **Gate 4.**
- [ ] **Fri 9 to Sun 11 (Ludvig):** draft the institutional background (PPM, reforms 2019-2022, FTN, every fact sourced).

### Week 2 (12 to 18 Oct): all main results
- [ ] Table 2 complete: piecewise rows, tail contrast, all robustness rows including D&M and the funds-of-funds exclusion.
- [ ] Table 3: two stages, randomisation inference within round. **Gate 5.**
- [ ] Meet Klug with the headline number.
- [ ] Ludvig: related literature (under one page) and the data section.

### Week 3 (19 to 25 Oct): finish the analysis
- [ ] Table 4 and the descriptive appendix.
- [ ] One script per exhibit; full run from raw data on a clean machine.
- [ ] Ludvig: method section with a deviations table (from SSZ and from D&M).
- [ ] **Sun 25 Oct: data freeze. Gate 6.** (D&M 2001-2008 data has its own cutoff, Fri 30 Oct.)

### Week 4 (26 Oct to 1 Nov): write everything
- [ ] Results: every paragraph opens with our number, the benchmark and the bound.
- [ ] Introduction (2-4 pages, numbers previewed); conclusion last, calibrated with `research/reference/conclusions_winners_vs_nonwinners.md`.
- [ ] D&M appendix if its data arrived.
- [ ] **Mon 2 Nov: full draft to Klug. Gate 7.**

### Weeks 5-6 (2 to 20 Nov): attack the draft, then finish
- [ ] Outside referee read; fix every unsupported claim. **Gate 8.**
- [ ] Number audit: every figure in the text traced to a table cell or a cited page.
- [ ] Mid-term meeting (Klug's date): bring Tables 2 and 3, nothing else.
- [ ] Klug's comments; 20-30 references, all cross-checked (D&M: EFM 21(1), 1-19).
- [ ] AI appendix from the log; replication package (raw data, code per exhibit, data dictionary, README with run order).
- [ ] Format: English, official front page, no table of contents, 12 pt single spacing, at most 40 pages of main text. Two proofreads, one on paper.
- [ ] **Fri 20 Nov: submission-ready.**

### Buffer (21 Nov to 7 Dec)
- [ ] Second Klug round if needed; prepare the presentation and opposition.
- [ ] **Submit by Mon 7 Dec, 10:00 (Gate 9).** Presentation and opposition before 12 Dec; Publish Thesis by 18 Dec, 18:00.
