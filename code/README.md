# code/

All code in one place. Python 3, numpy and pandas (the notebook also uses statsmodels, matplotlib, maketables, scipy). Every script addresses files from the repo root through `REPO = <this file>/..` (or `../..` in `build/`), so it runs from any working directory. Paths are listed in `data/MANIFEST.md`.

## Analysis scripts (`code/*.py`)

| File | What it does | Reads | Writes | Runs now? |
|---|---|---|---|---|
| `eventstudy.py` | The engine: factor-model abnormal returns, CARs, BMP and Kolari-Pynnonen tests, cluster-robust OLS with wild cluster bootstrap, randomisation inference. `python3 eventstudy.py` runs a synthetic self-test (recovers a planted 2 per cent effect). | nothing | nothing | yes (self-test passed 27 Oct) |
| `power.py` | Minimum detectable effects for every table; `--dose <file>` recomputes from the actual dose file | optional dose csv | prints | yes |
| `replication_omxsb.py` | Table 2, Figure 2: Greenwood-Sammon on OMXSB 2013-2026, script version | `data/input/omxsb/omxsb_changes_2013_2026.csv`, `data/raw/lseg/panel_2012_2026/` | `output/table2_*.csv`, `figure2_data.csv` | needs `factors_daily.csv` (not pulled yet) and `tracker_aum.csv` (to build by hand). **The notebook below has already produced Table 2.** |
| `pressure.py` | Equations 5 and 6 and the square-root prediction; no returns | `data/derived/exit_days/`, `data/derived/measurements/`, LSEG panel | `output/dose_stock_tranche.csv`, `tranches.csv` | needs per-quarter `fi_holdings_<q>.csv` from `parse_fi.py` |
| `parse_fi.py` | Parses FI holdings zips (VPFO XML) into long CSVs; takes paths as arguments | `data/raw/fi/` | per-quarter csv | yes |
| `ftn_eventstudy.py` | Tables 3 and 4, Figure 3 | dose file, LSEG panel, `data/input/round_dates.csv` | `output/table3_*`, `table4_*` | **gated**: `UNBLIND = True` and a tutor sign-off date in `thesis/design/03_DATA.md` section E |
| `dilution.py` | Table 5 (incidence on stayers) | exit days, `data/derived/shof/fund_nav_daily.csv` (to build from Reinvestments), swing status | `output/table5_incidence.csv` | **gated**, same switch |

## Build scripts (`code/build/`): `data/raw` to `data/input` and `data/derived`

| File | Builds | From | Note |
|---|---|---|---|
| `detect_exit_days.py` | `data/derived/exit_days/*.csv` (tranche days of the 78 losers, no returns) | `data/raw/shof/Valuations/` (shared by hand), round membership, crosswalk | re-run after each SHoF refresh (next: early November) |
| `omxsb_build.py` | `data/input/omxsb/omxsb_changes_2013_2026.csv` | Nasdaq notices, sources in `omxsb_notes.md` | hand-verified list; 394 events |
| `omxs30_build_csv.py` | `data/input/omxsb/omxs30_changes_2005_2026.csv` | sources in `omxs30_notes.md` | 48 events |
| `omxsb_map_ric_2007_2012.py` | `data/input/omxsb/omxsb_changes_2007_2026.csv` (536 events, both lists concatenated) and `omxsb_events_with_ric_2007_2026.csv` (RIC and coverage on `panel_2005_2026`) | the two change lists, `omxsb_events_with_ric.csv` (RICs reused), `td_universe.csv`, `stocks_static_2005.csv`, the 2005 parquet | mapping logic of `lseg_pull_v4` CELL 3 and coverage check of CELL 7; prints the name matches and the 16 unmatched tickers to `output/omxsb_replication_2007/mapping_review.txt`; unmatched RICs are left empty, never guessed |
| `swing_build_outputs.py` | `data/input/swing/*.csv` | round membership, PPM panel, fund documents (urls in the script) | reads `purge2019_candidates.json`, which is not in the repo |
| `build_ppm_panel_2018.py` | `data/derived/ppm/ppm_panel_2018_2026.csv` | `data/raw/ppm/` monthly files | |
| `build_ppm_panel_2022.py` | `data/derived/ftn/ppm_panel_2022_2026.csv` | `data/raw/ppm/2021-2026/` | |
| `shof_monthly.py` | `data/derived/shof_monthly/*.csv` | SHoF daily exports | paths inside are from the machine it ran on |
| `agent_runs/measurements_*.py`, `agent_runs/facts_*.py` | `data/derived/measurements/`, `data/derived/facts/` | | **Archival.** Written by agents in October with absolute scratchpad paths; kept so that every derived number can be traced to its code. They do not run as-is. |

## LSEG pulls (`code/lseg/`)

Run inside LSEG Workspace CodeBook, not locally. `lseg_pull_v4.py` / `.ipynb` is the version that produced `data/raw/lseg/panel_2012_2026/` (14 to 15 Oct) and, with the start date changed, `panel_2005_2026/` (26 Oct) and `panel_eu/` (27 Oct). `old/` holds v1 to v3. Request lists are in `data/input/lseg/`.

## Notebooks (`code/notebooks/replication_omxsb.ipynb`, `replication_omxsb_2007.ipynb`)

The OMXSB replication as actually run on 25 Oct: CARs for 380 events, index-fund net trading from FI holdings, 36 tables and 6 figures, all in `output/omxsb_replication/`. Start Jupyter in `code/notebooks/` (or the repo root); the first cell resolves the repo root and asserts the inputs exist. Inputs: `data/raw/lseg/panel_2012_2026/`, `data/input/omxsb/omxsb_events_with_ric.csv`, the 31 zips in `data/raw/fi/`. It also writes `data/derived/fi/fi_holdings_long.csv.gz`.

`replication_omxsb_2007.ipynb` is a copy of the notebook extended to 2007-2026: it reads `data/raw/lseg/panel_2005_2026/` (the parquet, `stocks_static_2005.csv`, `indices_daily (1).csv`), `data/input/omxsb/omxsb_events_with_ric_2007_2026.csv` and the same 31 zips, uses five periods with 2007–2012 first, adds a trend test and an old-versus-new comparison (`tab_02b_trend_long`, `tab_02c_ftest_old_vs_new`, `table2_old_vs_new.md`, `CHECK.md`) and writes everything to `output/omxsb_replication_2007/`. It loads `data/derived/fi/fi_holdings_long.csv.gz` instead of re-parsing the zips when the file exists, recomputes first/last trading day from the daily panel (the 2005 static table carries the pull range instead), and fills IssueISIN for RICs missing from `td_universe.csv` from the 2012 static table. Phase 2 (same day) makes it follow Greenwood & Sammon (2025) exactly where their text is explicit: missing stock-days are kept as NaN so the event drops out of that window (6 total-window CARs of 487), AD and ED are the next trading day on or after the calendar date, Table 3 uses uncentred controls with excess turnover as average daily turnover in the month before AD minus the cap-weighted market average, Figure 8 is normalised to zero at AD+10, and it adds the anchor's Table 1 by year (`tab_00_by_year`), Figure 2 (`fig_02_by_year`), the pre-announcement CAR table (`tab_08_preannouncement`) and the sample tables A1/A2 (`tabA_09_sample_selection`, `tabA_08_sample_sensitivity`); Table 5 (η) is labelled an extension. The phase-1 Table 2 is kept as `tab_02_car_long_phase1.csv` and compared in `table2_phase1_vs_gs.md`. Run 28 Oct, 61 s. The original notebook and `output/omxsb_replication/` are unchanged.

This notebook is the main track for Part 1; `replication_omxsb.py` is the script form of the same design and is kept for the replication package.

## Order of operations

1. Part 1: the notebook (done once; re-run when the panel or events change).
2. Part 2 inputs: `parse_fi.py` per quarter, then `pressure.py`, then `power.py --dose output/dose_stock_tranche.csv`.
3. Klug sign-off, date written in `03_DATA.md` section E, flip `UNBLIND`, run `ftn_eventstudy.py` and `dilution.py`.

Nothing in this folder reads a stock or fund return around an FTN date until the switch is flipped.
