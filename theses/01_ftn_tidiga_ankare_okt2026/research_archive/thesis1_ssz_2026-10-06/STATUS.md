# STATUS: read this first

**As of Tue 6 October 2026.** Update this file whenever something below changes (date at the top, one line per change).

## Where things stand

- **Phase:** design settled, nothing executed yet. No gate in `STEPS.md` is passed.
- **Anchor decided:** Sialm, Starks and Zhang (2015, JF). Dahlquist and Martinez (2015, EFM) is the Swedish predecessor and was integrated into the plan on 5 Oct. Details: `PLAN.md`.
- **No regression coefficient has been opened.** Only standard errors, counts and MDEs have been computed. Keep it that way until the pre-analysis plan (PAP) is frozen (Gate 3).

## Done

- [x] Anchor contest (two adversarial rounds) and decision (archived in `research/_archive/anchor_selection_2026-10-05/`).
- [x] Literature sweep across OpenAlex, Scopus, EconLit and Semantic Scholar (`research/literature/literature_sweep_2026-10-05.md`).
- [x] D&M read in full; notes with page numbers (`research/literature/dahlquist_martinez_2015_notes.md`).
- [x] D&M cross-check of the no-sponsor prediction: about −0.18 per year vs the frozen −0.17 (rough, equal-size approximation).
- [x] **Final anchor sweep (6 Oct):** six web-research agents, about 300 queries, citation trails of all 207 papers citing SSZ. Nothing beats SSZ (best: Bjerksund et al. 2026 MS at 12/18, wrong question). No academic work on FTN exists. No design change; new references added to `PLAN.md` §3. Report: `research/literature/anchor_sweep_final_2026-10-06.md`. **The anchor question is closed.**
- [x] Folder and project tidied. One plan (`PLAN.md`), one step list (`STEPS.md`), everything superseded in `research/_archive/`.

## Not done yet (next actions, in order)

1. [ ] **Send the Klug email** (`PLAN.md` §7): the A/B question plus the D&M framing. Not sent.
2. [ ] **Send the data requests** (`PLAN.md` §5.3: SHoF, Fondbolagen/Svensk Fondstatistik, FTN, Pensionsmyndigheten). None sent.
3. [ ] **Rebuild the processed data.** The fund panel (`pa_panel`), the bid file (`bids_long`: 290 bids, 75 winners) and the power scripts were built in earlier cloud sessions and **do not exist on disk**. Rebuild them from `data/` with code saved in the repo. The numbers in `PLAN.md` (N 512, 153 funds, MDE 0.101; 290 bids; N 87/110/142) come from those earlier builds; the rebuild must reproduce them or explain any difference.
4. [ ] Freeze and timestamp the PAP (Gate 3), then run the headline (Gate 4).
5. [ ] Start the AI log (required for the AI appendix).

## Watch list

- **Riksrevisionen audit** "Ett upphandlat fondtorg för premiepensionen" (opened June 2026, no report date). Re-check in November; if it publishes before 7 Dec, cite it.

## Open decisions

- **Klug's answer to A vs B.** Everything assumes A. If he chooses B, re-plan before doing anything else.
- **The D&M 2001-2008 replication** happens only if quarterly non-PPM fund assets for 2000-2008 arrive by Fri 30 Oct.
- **Holder-type data** (Fondbolagen/SCB): unknown whether it exists. It decides how strongly risk S2 can be addressed.

## Housekeeping

- **Git:** the tidy-up is **not committed**. `research/` is untracked; `PLAN.md` and `README.md` were replaced; `STEPS.md` and `STATUS.md` are new. Two SHoF CSVs show as deleted from `data/` (they predate this session and are in `data/Valuations/`). Commit only when the authors ask.
- **claude.ai project "thesis"** mirrors `PLAN.md`, `STEPS.md`, `STATUS.md`, the literature sweep, the D&M notes and the two winners references.
- **People:** authors Alexander Fox (data and code) and Ludvig Pauli Uväng (literature and writing); tutor Michael Klug.

## Rules for any agent working here

1. `PLAN.md` wins over every other file. Do not use anything in `research/_archive/` for decisions.
2. Do not open treatment or replication coefficients before Gate 3.
3. Do not write thesis prose. The course forbids AI-written thesis text; anything drafted is marked *draft* for the authors to rewrite.
4. Raw data in `data/raw/` is never modified; every transformation lives in code.
5. Do not add exhibits beyond the five in `PLAN.md` §4.4.
