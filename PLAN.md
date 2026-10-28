# PLAN.md: thesis 2 in one document

**Single source of truth.** Written 25 October 2026 when the three thesis folders were merged. It replaces the SSZ plan (archived in `archive/research_archive/thesis1_ssz_2026-10-06/`). If anything here conflicts with an older file, this file wins. Dates and gates are in `STEPS.md`; the day-to-day state is in `STATUS.md`.

The detailed design is not repeated here. Read, in this order: `thesis/design/00_VALIDATION.md` (why this design), `thesis/design/01_DESIGN.md` (the pre-analysis plan), `thesis/design/thesis2_method.tex` (equations, data table, honest assessment), `thesis/outline/thesis2_outline.md` (section by section, page budget 33 of 40).

Authors: Alexander Fox and Ludvig Pauli Uväng. Tutor: Michael Klug. Examiner: Riccardo Sabbatucci. Course: BE451, autumn 2026.

> Course rule: AI may not write thesis text. Every use of an AI tool goes into `thesis/AI_LOG.md` the same day (tool, date, purpose, what changed).

---

## 1. Course requirements and deadlines

| What | When |
|---|---|
| Mid-term meeting with Klug | November, on Klug's date |
| Thesis in Canvas **and** replication package (zip) to Anneli Sandbladh | **Mon 7 December, 10:00** |
| Presentation and opposition | Before 12 December |
| Final version in Publish Thesis | 18 December, 18:00 |

Format: English; official front page; no table of contents; at most 40 pages single-spaced including tables, references and appendix; introduction 2-4 pages that previews the numbers; related literature under one page; self-contained captions; no textbook exposition of standard methods; every in-text source in the references and vice versa; AI appendix. Checklist: `thesis/outline/requirements_checklist.md`.

What the examiner grades: useful, correct, relevant, contribution, independence. Do not chase significance; state the power of every test.

---

## 2. What the thesis is

**Question.** When a pre-announced, uninformed and large flow hits Swedish stocks, who pays, how much, and does the market learn? Greenwood and Sammon (2025) show that the US index effect disappeared as arbitrageurs learned the flow. Fondtorgsnämnden's procurements created a new flow of the same kind: Pensionsmyndigheten empties the losing funds in a few tranche days, which sells their portfolios into the market with a dose per stock that reaches tens of per cent of daily volume in small caps.

**Working title.** "Pre-announced, uninformed, and large: the price of moving the premium pension"

**Three parts, four hypotheses, one table each** (`thesis/design/01_DESIGN.md`, 3.5):

| Part | Hypothesis | Exhibit |
|---|---|---|
| 1. Replication on OMXSB, 2013-2026 | H1: additions earn positive and deletions negative abnormal returns from announcement to effective date; the effect scales with expected tracker demand over ADV; whether it declined as tracker assets grew eightfold | Table 2, Figure 2 |
| 2. FTN forced sales, 2024-2026 | H2: on tranche days abnormal returns fall in the forced net sale over ADV, with beta of order one on the square-root prediction, and reverse within 20 days | Table 3, Figure 3 |
| 2. Anticipation | H3: part of the move happens between award, letter and first tranche; the pattern separates predation, slow-moving capital and sunshine trading | Table 4 |
| 3. Who paid | H4: losing funds without swing pricing show NAV below benchmark by about c r/(1 - r) on tranche days; funds with swing pricing do not | Table 5, Figure 4 |

Table 1 is summary statistics (rounds, money moved, fees before and after). Table 6 is the cost-benefit arithmetic on H2 and H4 (impact cost per round against the fee saving). Table 7 is robustness. Figure 1 is the procurement timeline with one fund's capital. Appendix: A1 procurement calendar, A2 variable definitions, A3 additional checks. Seven tables, four figures, eight numbered equations, nothing added without something removed.

**What it can conclude** (`thesis2_method.tex`, section 6): a price in SEK for the reform's transitions against its fee saving; who paid and whether swing pricing or slower execution fixes it; whether the agency's staggering belief is right; and, from Table 2 against Table 3, whether the index effect vanished because the market became liquid or because it learned one flow at a time.

**What it does not test.** Whether FTN picks better funds. That was thesis 1 and needs years of post-award returns.

---

## 3. Papers and their roles

| Paper | Role |
|---|---|
| **Greenwood and Sammon (2025), JF 80(2), 657-698** | Anchor. Windows, return measure, Table 2 structure, the learning question |
| Da, Larrain, Sialm and Tessada (2018); Lou (2012); Jin, Kacperczyk, Kahraman and Suntheim (2022) | Method references for forced flows, dose and dilution. Not second anchors |
| Hartzmark and Solomon (2025, AER); Kyle and Obizhaeva (2016); Brunnermeier and Pedersen (2005); Duffie (2010) | Theory: price impact, predation, slow-moving capital |
| Sabbatucci's working paper on retirement-plan menu shifts | The examiner's own question; cited in the motivation |
| Dahlquist and Martinez (2015, EFM); Hagen, Malisa and Post (2023); Engström and Westerberg (2004) | PPM background and the Swedish flow literature |
| FI (2025); RiR 2018:32; SOU 2019:44; Lag (2022:759) and (2022:760); the 2026 Riksrevisionen audit | Institutional chain and novelty |

Full list with verification status and magnitudes: `thesis/literature/literature_verified.md` (66 references, 52 verified) and `references.bib`. Target in the thesis: 25-30 references.

---

## 4. Specification: pre-committed and open

Pre-committed in `thesis/design/01_DESIGN.md` (section 8): the windows, the dose definitions (gross and net, equation 6), Y = 0.7 in the square-root benchmark, the factor model, the clustering unit, the four hypotheses with their tables, the 20-day reversal window for the small-cap round, and the index round reported as a low-dose treated group. Power is in `01_DESIGN.md` 5.4 and is recomputed from the actual ADV by `code/power.py --dose` before unblinding.

Open, to be settled with Klug before unblinding: OMXSB alone or with OMXS30; the 2019 purge in Table 5 or the appendix; market-adjusted or four-factor as the main measure; cost-benefit as table or paragraph.

**The unblinding rule.** `code/replication_omxsb.py` runs now; it touches no FTN date. `ftn_eventstudy.py` and `dilution.py` carry `UNBLIND = False`. The switch is flipped only after the sign-off meeting, and the date goes into `thesis/design/03_DATA.md`, section E, in the same commit.

---

## 5. Data

| Variable | Used in | Source and file | Status 25 Oct |
|---|---|---|---|
| Daily close, total return, volume | AR, CAR, ADV, dose | Datastream pull of 15 Oct, `data/raw/lseg/datastream/` (gitignored) | On disk, wide, names only. Needs the long format, a code row, MV and NOSH (`data/raw/lseg/panel_2012_2026/README.md`) |
| Index levels (OMXSPI, OMXSGI, OMXSB, OMXSBGI, OMXS30) | Market return, figures | Datastream, `indices_daily.csv` | Not pulled |
| Swedish factors | Four-factor robustness | SHoF Fama-French page | Not pulled; not on the critical path |
| OMXSB additions and deletions | Part 1 events | Nasdaq releases, `data/input/omxsb/` | Done: 394 events, mapped to LSEG codes |
| Tranche days, redeemed share, fund assets | Dose, Table 5 | Morningstar daily via SHoF, `data/derived/exit_days/` | Done for about 30 losers to 30 Sep; refresh to 31 Oct in week 2 |
| Sale orders for the largest Swedish losers | Dose, Swedish rounds | Pensionsmyndigheten, offentlighetsprincipen | Request not sent |
| Fund holdings | Dose, staleness check | FI quarterly holdings, `data/extra/fi_YYYYqN.zip` | 4 of 12 quarters; 8 plus 5 to download |
| Winners' inflows, fee savings | Table 1, Table 6 | `data/derived/ppm/ppm_panel_2018_2026.csv` | Done |
| Award and letter dates, winners, losers, bids | Rounds, windows | `data/derived/ftn/bids_long.csv` | Done, 11 rounds |
| Swing-pricing status | Table 5 | `data/input/swing/` | Done: 11 yes, 38 no, 29 unknown |
| Fund NAV and benchmark | Table 5 | `data/raw/shof/Reinvestments/` (not in git), `data/fundmaster.xlsx` | Done; opened only after unblinding |

Data rules: raw files untouched, with download dates; every transformation in code; one script per exhibit; the whole chain runs from raw data on a clean machine before the draft goes to Klug. Licensed data (LSEG, Morningstar) never enters git; the replication package for the course ships the code and the derived tables, and names the licensed inputs.

---

## 6. Division of labour

Two tracks, one repo, one branch. Ludvig: code and data. Alexander: text, literature, correspondence. Each person owns folders; the other asks before touching them.

| | Ludvig (L) | Alexander (A) |
|---|---|---|
| Owns | `code/`, `data/`, `output/` | `thesis/text/`, `thesis/literature/`, `thesis/AI_LOG.md`, `thesis/research_2026-10-11/` |
| Does | Stock panel, FI holdings, tracker assets, procurement calendar data, swing-pricing gaps, dose, every table and figure, power, robustness, SHoF refresh request, clean-machine run, replication package | Klug and Pensionsmyndigheten correspondence, institutional background, data and method prose, theory section (four of the eight equations), literature cards and the related-literature paragraph, introduction and conclusion, AI log and appendix, format checklist, the seminar deck |
| Writes | The one-sentence reading of each table the day it is finished, in `output/tables/NOTES.md` | Everything in `thesis/text/`, from those sentences and the design files |
| Reviews | A's data and method sections against the code | L's tables against `01_DESIGN.md` and the captions rule |

Swap roles for one afternoon each Friday: L reads the text for claims without a table cell; A reads the code for a choice not in the PAP.

---

## 7. Working rules

1. **Git.** `git pull` before you start, `git push` when you stop, and at the latest every evening. Small commits with messages that say what changed ("Table 2: first run, 394 events"). Both work on `main`; folder ownership prevents conflicts. Shared root files (`STATUS.md`, `README.md`) are edited in one sitting: pull, edit, commit, push within minutes.
2. **Never in git:** `data/raw/shof/Valuations/`, `data/raw/shof/Reinvestments/`, `data/raw/lseg/panel_2012_2026/` (licensed), build files. They are in `.gitignore`; if git refuses a file over 100 MB, ignore it, never force it. Share those folders by AirDrop or Drive.
3. **Numbers.** Every table in the text is `\input` from a `.tex` fragment that the script writes to `output/tables/`. No number is typed by hand; the number audit before submission then checks scripts, not sentences.
4. **Text.** One file per section in `thesis/text/sections/`; `thesis/text/main.tex` includes them. Two people never edit the same section file on the same day.
5. **Claims.** One sentence per claim: our estimate, the benchmark (the anchor's number or the square-root prediction), the bound. "Associated with", never "caused", unless the design earns it.
6. **Unblinding.** See section 4. Anything run after the sign-off that is not in `01_DESIGN.md` is labelled exploratory.
7. **AI.** No AI-written thesis text. Log every use in `thesis/AI_LOG.md` the same day.
8. **Status.** Three lines each evening in `STATUS.md` (done, next, blocked). Three lines to Klug every Friday.

---

## 8. Risks (S = could sink the thesis)

| # | Risk | Mitigation |
|---|---|---|
| S1 | Klug has not signed off the change from the synopsis question | Meeting in the week of 2 Nov with the method note; written yes before unblinding |
| S2 | Stock panel cannot be mapped to the event list (names only, 30 `#ERROR` series) | Re-run the same Datastream list with a code row, MV and NOSH; match by ticker, then name; hand-resolve the rest (`replication_omxsb.py` writes the unmatched file) |
| S3 | Large-cap power is low; small-cap tranches slip to November | Write on Swedish active, Nordic active and the 2024 European round; add small cap last; state the MDE |
| S4 | Sale dates for the five largest Swedish losers never arrive | Index round month-dated as a low-dose group; Swedish active loses 3 of 18 funds; say so |
| S5 | Nine foreign-domiciled losers have no FI holdings | Semi-annual reports or Morningstar holdings via SHoF; otherwise state the downward bias in the dose |
| 6 | Square-root law fails for a fund that must deliver cash | beta not equal to one is the finding, with the MDE |
| 7 | Fan-out | Seven tables, four figures, eight equations; Table 4 and Table 6 are the first to cut |
| 8 | Over-claiming | Rule 5 above; `reference/winners_analysis/conclusions_winners_vs_nonwinners.md` when writing the conclusion |
| 9 | Licensed data on a public repo | Repo goes private before the next push |
| 10 | AI-text rule | Rule 7; AI appendix from the log |
