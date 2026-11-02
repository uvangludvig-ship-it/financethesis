<!-- ANALYSIS_DELIVERY_20261102 -->
> **2 november 2026, genomfört:** Rättelser, daterade kontroller, ägar- och mandatdekomposition, retention, köp/volym-normalisering, modelljämförelse, samma-aktie-kontroll och censurerad FI-blankningsprofil är sparade med kod och verifieringar.
> **Nästa:** Samla försvarbara bidrag från resultaten; välj inte fler varianter efter signifikans.
> **Öppet:** Kausal prisförklaring och varaktighet efter 20 dagar. FTN-utfall är fortsatt stängda. Senaste rapport: `output/omxsb_broadening_20261102/RESULTAT.txt`.

> **1 november 2026: kontrollanalys rättad.** Se `output/omxsb_robusthet_20261101/RESULTAT.md`, `code/build/robusthet_hela.py` och `thesis/design/ROBUSTHET_RATTELSE_20261101.md`. T2 har konsekvent reviewviktning och matchning före utfallet. T5:s historiska medlemsidentifierare är ofullständiga och inga verifierade nästan-kandidater har skapats. A/B-förstastegets gamla nollor och 0,74 är inte validerade; den nya valideringsrapporten anger saknade led explicit. Påståendena om tredelning, noll köptryck och permanent effekt har dragits tillbaka. Äldre status nedan är historik.

# STATUS: read this first

**As of Thu 29 October 2026.** Newest change on top. Each evening, three lines per person (done / next / blocked), initialled A or L.

## Where things stand

- **30 Oct: equal periods.** Table 2 and every by-period exhibit now use four equal five-year periods of effective dates, 2007-2011, 2012-2016, 2017-2021, 2022-2026 (10, 10, 10 and 9 reviews; the anchor's four decades, as the deck already said), in place of the unequal cut 2007-2012 / 2013-2017 / 2018-2020 / 2021-2023 / 2024-2026. The underlying event data were checked and are right (39 reviews, announcement and effective dates consistent, leads match the regimes in `omxsb_notes.md`); the unequal bins were a hard-coded choice in the notebook with no common rationale, and they made the trend slope per period ill-defined. Changed in `replication_omxsb_2007.ipynb`, `mechanisms_2007.py`, `slides_tables.py`; notebook, mechanisms and deck re-run. The comparison against the 25 Oct run keeps the old bins through a separate `period_old` column (`tab_02_car_long_oldperiods.csv`; still the same 3 of 30 cells differ, Africa Oil and Veoneer). The phase-1 table is now recomputed inside the notebook rather than read from a frozen file. Headline: total-window CAR for additions 8.5 / 0.3 / 2.9 / 1.5 per cent, deletions -6.7 / -2.4 / -0.6 / -1.5; F-test of equal means p = 0.03 (additions) and 0.04 (deletions); trend slope per five years -1.3 (p = 0.09) and +1.5 (p = 0.06). Committed and pushed 30 Oct. **Period-length sensitivity:** `code/build/period_sensitivity.py` reruns Table 2 for every equidistant length that divides the 20 years (1, 2, 4, 5, 10, 20 years) into `output/omxsb_replication_2007/period_sensitivity/` (RESULTS.md, long csv, trend table, figure). The per-year trend in the total-window CAR is the same at every length: additions about -0.27 pp per year (p 0.09 to 0.12 for 1, 2, 4 and 5-year periods), deletions about +0.23 to +0.30 pp per year (p 0.06 to 0.26). The F-test rejects equal means at 2, 4 and 5 years and not at 10; at 1 year it is singular (2007, 2010 and 2026 have one announcement date each). **Trend tests** (`code/build/trend_tests.py` → `period_sensitivity/TREND_TESTS.md`, `.csv`): bin-free OLS on calendar time, review-level slope and Spearman, Mann-Kendall, and a sup-Wald single-break test with wild-cluster-bootstrap p (break found after the June 2010 review for both types: additions 11.4 → 1.7, p = 0.014; deletions -9.6 → -1.5, p = 0.030), plus the same tests per period length (OLS on period index, Jonckheere-Terpstra, Spearman on period means, break at period boundaries). Linear trend per year is about -0.28 (adds, p 0.08–0.10) and +0.22 (dels, p 0.24–0.30) at every length; the break test is the one that is significant.
- **29 Oct: new structure.** The thesis is an OMXSB replication of Greenwood and Sammon (2025) in which we run their tests of the five explanations for the disappearing index effect. FTN is no longer a separate study: it is a new setting where the same test (equations (5) and (6) in `slides/main.tex`) is run, and because the award comes months before the sale it separates predictability from event liquidity, which the index setting cannot. **Struck:** who paid, the SEK cost, swing pricing as a result, and the square-root law as the main test. `slides/main.tex` was rewritten to this structure with the real formulas, Table 2 and two figures from the 2007-2026 run. `PLAN.md`, `01_DESIGN.md` and the method note still describe the old structure and must be rewritten before any FTN return is opened.
- **29 Oct: Part 1 now runs 2007-2026** in `code/notebooks/replication_omxsb_2007.ipynb` (536 events, 39 reviews, 487 with prices, five periods, the anchor's conventions to the letter; 2013-2026 cells reproduce the 25 Oct run). The five explanations are run by `code/build/mechanisms_2007.py` into `output/omxsb_replication_2007/mechanisms/` (PLAN.md, RESULTS.md, numbers). The 225 deletions were checked for bids, bankruptcies, mergers and distressed issues (`data/input/omxsb/deletion_reasons_2007_2026.csv`, 20 flagged, no sign changes). The five reviews before July 2007 have no surviving release.
- **No FTN return has been computed, and none will be until the rewritten `thesis/design/01_DESIGN.md` (equations (5) and (6), the A and E windows, clustering by sale day) is committed and signed off.**
- **27 Oct: the repo was restructured.** Five folders by role: `thesis/`, `code/`, `data/` (raw, input, derived), `output/`, `reference/`, `archive/`. Map in `README.md`, every data file in `data/MANIFEST.md`. All 1,680 files were moved with `git mv`; hash-checked, nothing lost or changed. Nothing is deleted or gitignored any more; files over 50 MB go through Git LFS. Scripts were re-pointed to the new paths and compile; `eventstudy.py` self-test passes. **[A] after pulling: `brew install git-lfs && git lfs install`, then put Valuations and Reinvestments at `data/raw/shof/`, and re-run `code/build/detect_exit_days.py` once to confirm.**
- **25 Oct, 19:50: roles swapped. Ludvig: all code and data. Alexander: all text, literature, correspondence, the seminar deck.** `PLAN.md` section 6 and `STEPS.md` carry the new owners.
- **The map is `thesis/design/THESIS_IN_PLAIN_WORDS.md` (and `.docx`), version 2.4, Parts A to H.** Read it before anything else in `thesis/`.
- **Superseded 29 Oct (kept for the record):** the three-part structure (Part 1 replication 2013-2026, Part 2 FTN price pressure, Part 3 who paid) in `thesis/design/01_DESIGN.md` and `thesis/design/thesis2_method.tex` (14 Oct).
- **Part 1 has been run.** The notebook `code/notebooks/replication_omxsb.ipynb` (25 Oct) produced CARs for 380 OMXSB events, index-fund net trading from FI holdings, 36 tables and 6 figures in `output/omxsb_replication/`. These are the first unblinded numbers and are not FTN results. Table 2 for the text is built from `tables/tab_02_car_long.csv`.
- **No FTN return has been computed.** `UNBLIND = False` in `code/ftn_eventstudy.py` and `code/dilution.py` stays until Klug has signed off the specifications and the date is written in `thesis/design/03_DATA.md`, section E.
- **Thesis 1 (the SSZ replication) is dropped.** Archived in `archive/research_archive/thesis1_ssz_2026-10-06/`.
- **The GitHub repo is private** (verified 27 Oct).

## Data on disk (27 Oct; details in `data/MANIFEST.md`)

- **Stock panel:** complete. `data/raw/lseg/panel_2012_2026/` (1,667 RICs, daily 2012 to 14 Oct 2026, long format with close, total return, volume, mcap, shares: exactly what `eventstudy.py` reads). Extended back to 2005 in `panel_2005_2026/` (26 Oct; use the parquet, the csv.gz is corrupt as received) and to 670 European stocks plus SEK FX in `panel_eu/` (27 Oct). Daily fund NAV for 205 funds in `panel_2005_2026/fund_nav_tna_daily.csv`. Still missing: Swedish factors (`factors_daily.csv`) for the four-factor robustness; market-only runs without it.
- **FI holdings:** all 31 quarters 2018Q4 to 2026Q2 in `data/raw/fi/`, parsed to `data/derived/fi/fi_holdings_long.csv.gz`. 2026Q3 expected in November.
- **Tranche days:** `data/derived/exit_days/` for the 78 losers through 30 Sep. Re-run after the November SHoF refresh (small-cap round).
- **Unchanged and ready:** OMXSB and OMXS30 events (`data/input/omxsb/`), swing-pricing status (`data/input/swing/`), PPM monthly panel 2018-2026 (`data/derived/ppm/`), FTN bids, fees and crosswalk (`data/derived/ftn/`), round membership (`data/derived/measurements/`).
- **Shared by hand, not in git:** SHoF Valuations and Reinvestments (Alexander has them; Ludvig does not yet). Path: `data/raw/shof/`.

## Next actions, in order

1. [A] Pull the restructuring commit, install Git LFS, place Valuations and Reinvestments at `data/raw/shof/`, and give them to Ludvig by AirDrop or Drive. [L] The same setup, then run `python3 code/build/detect_exit_days.py` and confirm the two csv files in `data/derived/exit_days/` are reproduced.
2. [A] Klug. Nothing documents a meeting after 11 Oct. Confirm he has the method note and knows the synopsis question changed; book the sign-off meeting for the week of 2 Nov with the five decisions below on the agenda. Send `thesis/design/thesis2_method.pdf`.
3. [L] Part 2 inputs: `code/parse_fi.py` per quarter into `data/derived/measurements/fi_holdings_<q>.csv`, then `code/pressure.py`, then `code/power.py --dose output/dose_stock_tranche.csv`.
4. [L] Three data items the replication needs this week: `data/input/omxsb/tracker_aum.csv` (yearly OMXSB tracker assets 2013-2026, by hand from `omxsb_notes.md` section 5; the replication script reads it and it is missing), Appendix Table A1 (the procurement calendar with a source per date), and the 29 UNKNOWN swing-pricing rows. Decide with A whether `code/replication_omxsb.py` (script) should reproduce the notebook's Table 2 for the replication package. [A] `thesis/literature/cards.md` and the seminar deck (`slides/main.tex`).
5. [A] Send the Pensionsmyndigheten request for sale orders under offentlighetsprincipen (draft in `thesis/design/03_DATA.md`, C; rewrite it in your own words). Answers take one to three weeks.
6. [A] Keep `thesis/AI_LOG.md` current (course requirement). Fill the section files in `thesis/text/sections/` starting with institutional background and data.
7. [A+L] Before the sign-off meeting: rewrite `thesis/design/01_DESIGN.md` to the 29 Oct structure (Part 1 = the anchor's Table 2 and the five explanations on OMXSB 2007-2026; Part 2 = equations (5) and (6), the award window A and the sale window E, clustering by sale day, hypotheses H_A, H_E, H_0 as in the deck) and commit it. The four maths additions from `THESIS_IN_PLAIN_WORDS.md` Part F are struck with the old structure.
8. [L] First week of November: request the SHoF refresh of Valuations and Reinvestments to 31 Oct and re-run `code/build/detect_exit_days.py` for the small-cap tranches.

## Open decisions (for Klug; `thesis2_method.tex`, section 7)

1. Sign-off on the specifications in `01_DESIGN.md` and on the deviation from the synopsis.
2. Replication on OMXSB alone, or OMXSB plus OMXS30 (48 events; the 2005 panel now exists).
3. Market-adjusted returns as the main measure (as in the anchor) with the four-factor model as robustness, or the reverse.
4. Which FTN rounds enter the sale window E first (those with dated tranches).

## Watch list

- Small-cap round: first tranche 24 Sep 2026; the rest execute in October and are dated only after the SHoF refresh.
- FI 2026Q3 holdings: expected in November.
- Global active round frozen by the Indecap appeal (Förvaltningsrätten i Stockholm, 4909-26): one sentence in the text, no estimates.
- Riksrevisionen audit "Ett upphandlat fondtorg för premiepensionen": ongoing, no date. Re-check in November.
- Holdings gap: nine foreign-domiciled losers report no holdings to FI; weights from semi-annual reports or Morningstar via SHoF, otherwise state the downward bias.

## Rules for any agent working here

1. `PLAN.md` wins over every other file. `archive/` is history, not guidance.
2. Do not compute a stock or fund return around an FTN date before the sign-off date is written in `thesis/design/03_DATA.md`, section E.
3. Do not write thesis prose. The course forbids AI-written thesis text; anything drafted is marked *draft* for the authors to rewrite, and every use goes into `thesis/AI_LOG.md`.
4. `data/raw/` is never modified; every transformation is a script in `code/build/`. Nothing is deleted: superseded files go to `archive/`. Nothing new is gitignored.
5. A new data file gets a row in `data/MANIFEST.md` the same day.
6. Seven tables and four figures (`thesis/outline/thesis2_outline.md`). Something new replaces something; it is never added.
