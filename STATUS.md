# STATUS: read this first

**As of Tue 27 October 2026.** Newest change on top. Each evening, three lines per person (done / next / blocked), initialled A or L.

## Where things stand

- **27 Oct: the repo was restructured.** Five folders by role: `thesis/`, `code/`, `data/` (raw, input, derived), `output/`, `reference/`, `archive/`. Map in `README.md`, every data file in `data/MANIFEST.md`. All 1,680 files were moved with `git mv`; hash-checked, nothing lost or changed. Nothing is deleted or gitignored any more; files over 50 MB go through Git LFS. Scripts were re-pointed to the new paths and compile; `eventstudy.py` self-test passes. **[A] after pulling: `brew install git-lfs && git lfs install`, then put Valuations and Reinvestments at `data/raw/shof/`, and re-run `code/build/detect_exit_days.py` once to confirm.**
- **Thesis 2 is the thesis.** Working title: "Pre-announced, uninformed, and large: the price of moving the premium pension". Anchor: Greenwood and Sammon (2025, JF). Part 1 replicates their index-effect result on OMXSB (394 events, 2013-2026). Part 2 measures the price pressure of Pensionsmyndigheten's forced sales after Fondtorgsnämnden's rounds (2024-2026). Part 3 asks who paid (dilution of the stayers, swing pricing). Pre-analysis plan: `thesis/design/01_DESIGN.md`. Method note: `thesis/design/thesis2_method.tex` (14 Oct).
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

1. [A] Pull the restructuring commit, install Git LFS, place Valuations and Reinvestments, run `python3 code/build/detect_exit_days.py` and confirm the two csv files in `data/derived/exit_days/` are reproduced. [L] Get Valuations and Reinvestments from Alexander by AirDrop or Drive.
2. [L] Klug. Nothing documents a meeting after 11 Oct. Confirm he has the method note and knows the synopsis question changed; book the sign-off meeting for the week of 2 Nov with the five decisions below on the agenda. Send `thesis/design/thesis2_method.pdf`.
3. [A] Part 2 inputs: `code/parse_fi.py` per quarter into `data/derived/measurements/fi_holdings_<q>.csv`, then `code/pressure.py`, then `code/power.py --dose output/dose_stock_tranche.csv`.
4. [A] Decide with L whether `code/replication_omxsb.py` (script) should reproduce the notebook's Table 2 for the replication package, and build `data/input/omxsb/tracker_aum.csv` by hand from `omxsb_notes.md`.
5. [L] Send the Pensionsmyndigheten request for sale orders under offentlighetsprincipen (draft in `thesis/design/03_DATA.md`, C; rewrite it in your own words). Answers take one to three weeks.
6. [L] Keep `thesis/AI_LOG.md` current (course requirement). Fill the section files in `thesis/text/sections/` starting with institutional background and data.
7. [L] First week of November: request the SHoF refresh of Valuations and Reinvestments to 31 Oct. [A] Re-run `detect_exit_days.py` for the small-cap tranches.

## Open decisions (for Klug; `thesis2_method.tex`, section 7)

1. Sign-off on the specifications in `01_DESIGN.md` and on the deviation from the synopsis.
2. Replication on OMXSB alone, or OMXSB plus OMXS30 (48 events; the 2005 panel now exists).
3. The 2019 purge in Table 5 as a pooled sample, or in the appendix.
4. Market-adjusted returns as the main measure (as in the anchor) with the four-factor model as robustness, or the reverse.
5. Cost-benefit as a table or a paragraph.

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
