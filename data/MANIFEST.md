# data/MANIFEST.md: every data file, what it is and where it came from

Updated 27 Oct 2026 at the restructuring. **Rule: a new data file gets a row here the same day.** The per-file tables at the bottom are generated (`sizes, rows, columns`); the prose is maintained by hand.

## The four layers

| Folder | Meaning | Who writes it |
|---|---|---|
| `data/raw/` | Inputs exactly as received. Never edited. | nobody; files are dropped in |
| `data/input/` | Lists built or verified by hand (event lists, swing status, LSEG request lists). | the authors, with the build script named in each `*_notes.md` |
| `data/derived/` | What `code/build/` produces from raw and input, and what the analysis scripts read. | scripts only |
| `output/` | What the analysis produces for the text. | scripts only |

## What is in git and what is shared by hand

Everything is in git, including the LSEG panels and the FI holdings. Files over 50 MB are stored through **Git LFS** (patterns in `.gitattributes`: `data/raw/lseg/**/*.gz`, `*.parquet`, `data/derived/fi/*.gz`, the zips). Run `brew install git-lfs && git lfs install` once per machine; after that `git clone` and `git pull` fetch them like any file.

Two folders are **not** in git because they are several GB and licensed to SHoF: `data/raw/shof/Valuations/` (daily fund TNA, units and net flow per share class) and `data/raw/shof/Reinvestments/` (daily reinvested prices). Alexander holds them; Ludvig gets them by AirDrop or Drive and puts them at exactly those paths. `code/build/detect_exit_days.py` and `code/build/shof_monthly.py` read them.

## data/raw: sources

| Folder | Source | Period | Pulled | Notes |
|---|---|---|---|---|
| `raw/ppm/` | Pensionsmyndigheten monthly fund statistics (xls/xlsm), plus the 2026 fund list, `FEES.txt`, `ppm_nav_2024.xlsx` | 2001-01 to 2026-08 | Sep to Oct 2026 | 310 files in year folders. `build_ppm_panel_2018.py` reads 2018 onward. |
| `raw/ftn/` | Fondtorgsnämnden procurement reports, 11 pdf + the Europe active report as pdf and txt | 2024 to 2026 | Oct 2026 | |
| `raw/fi/` | Finansinspektionen quarterly fund holdings (`Fondinnehav_<quarter>_<FI publication date>.zip`), one zip per quarter | 2018Q4 to 2026Q2, 31 quarters | 25 Oct 2026 (Alexander) | Read by the notebook into `derived/fi/fi_holdings_long.csv.gz`. `earlier_download_2026-10/` holds four quarters downloaded earlier under other names; they differ byte-wise from the 31 (different FI packaging) and are kept. |
| `raw/shof/` | SHoF (Swedish House of Finance) Morningstar fund master (`fundmaster.xlsx`, zip) and field definitions | | Oct 2026 | Valuations and Reinvestments: see above. |
| `raw/lseg/panel_2012_2026/` | LSEG Workspace CodeBook, `code/lseg/lseg_pull_v4`: daily close, total return, volume, market cap, shares, turnover for 1,667 RICs (OMXSB companies and the losers' holdings), indices, static table, failures | 2012-01 to 2026-10-14 | 14 to 15 Oct 2026 | The panel the notebook and `replication_omxsb.py` read. |
| `raw/lseg/panel_2005_2026/` | Same pull with start 2005, 2,117 RICs, plus `fund_nav_tna_daily.csv` (daily NAV for the 205 funds in `input/lseg/funds_input.csv`), extra indices, resolved universe | 2005 to 2026-10 | 26 Oct 2026 | **`stocks_daily_2005.csv.gz` is corrupt (gzip CRC error), as received. `stocks_daily_2005.parquet` holds the same 4,340,104 rows intact; use it.** |
| `raw/lseg/panel_eu/` | Same pull for 670 European stocks held by the losers, plus `fx_sek_daily.csv` (daily SEK rates) | to 2026-10 | 27 Oct 2026 | |
| `raw/lseg/datastream/` | Datastream Excel add-in export (P, RI, VO wide, 1,467 series, 2004-12-31 to 2026-10-14) with `Codes.csv` | | 15 Oct 2026 | Superseded by the CodeBook panels but kept. |

## data/input: hand-built lists

| File | What | Built by |
|---|---|---|
| `omxsb/omxsb_changes_2013_2026.csv` | 394 OMXSB index changes with announcement and effective dates, 325 verified | `code/build/omxsb_build.py`, sources in `omxsb_notes.md` |
| `omxsb/omxsb_changes_2005_2012.csv` | 142 OMXSB index changes 2007-2012 (12 of the 17 reviews with effective dates in 2005-2012; the five reviews Jan 2005 to Jan 2007 not found), all verified from OMX/Nasdaq OMX release text; January/July schedule until Jan 2009 (cycle `2009JAN`), June/December from Jun 2009 | `code/build/omxsb_build_2005_2012.py`, sources in `omxsb_notes_2005_2012.md` |
| `omxsb/omxsb_notes_2005_2012.md` | Sources, schedule correction, the five missing reviews and what was tried, caveats (Nokia chain gap, reversed Sigma/Stora Enso A, ticker spellings) for the 2005-2012 list | agent run 27 Oct 2026 |
| `omxsb/deletion_reasons_2007_2026.csv` | Corporate events behind the 225 OMXSB deletions in the 2007-2026 sample: public offer, bankruptcy or reconstruction, merger or acquirer, delisting application, distressed issue, or review_only, with event date, source and confidence (20 flagged, AD−30 to ED+100 days) | three agent runs 28 Oct 2026 (web sources per row); used by `code/build/deletions_clean_table.py` |
| `omxsb/omxsb_events_with_ric.csv` | The same 394 events matched to LSEG RICs | LSEG pull v4 |
| `omxsb/omxsb_changes_2007_2026.csv` | The two lists above concatenated: 536 events, 39 reviews, 2007-07 to 2026-06, sorted by effective date then event_id, nothing dropped | `code/build/omxsb_map_ric_2007_2012.py` |
| `omxsb/omxsb_events_with_ric_2007_2026.csv` | The 536 events with RIC and days_with_price on `panel_2005_2026`: the 394 RICs of `omxsb_events_with_ric.csv` reused, the 2007-2012 tickers mapped with the CELL 3 logic of `lseg_pull_v4` (33 by ticker, 6 by name, 16 unmatched and left empty); 505 events pass the coverage check (111 of 142 in 2007-2012), the 31 failures are in `output/omxsb_replication_2007/coverage_failures.csv` | `code/build/omxsb_map_ric_2007_2012.py`, review in `output/omxsb_replication_2007/mapping_review.txt` |
| `omxsb/omxs30_changes_2005_2026.csv` | 48 OMXS30 changes | `code/build/omxs30_build_csv.py`, `omxs30_notes.md` |
| `omxsb/omxsb_constituents_2009_06_01.csv` | The 81 OMXSB constituents after the May 2009 review (effective 2009-06-01) as printed in the Nasdaq OMX release of 2009-05-11, with ticker and the LSEG RIC chain in `panel_2005_2026` (3 without a RIC: Nordea, Tieto, TradeDoubler); anchor for the membership reconstruction | hand-built 28 Oct 2026 from the GlobeNewswire release (url in the file); used by `code/build/mechanisms_2007.py` |
| `omxsb/tracker_aum.csv` | AUM of the OMXSB-tracking funds (Robur Access Sverige, Nordnet Sverige Index, LF Sverige Index) at documented dates, the notes' summary points (15/60/120 bn), the Nov 2010 release figure (other concept, unused) and XACT OMXSB (missing), with kind and source per row | hand-built 28 Oct 2026 from `omxsb_notes.md` section 5 and `omxsb_notes_2005_2012.md`; used by `code/build/mechanisms_2007.py` |
| `swing/swing_status_ftn_losers.csv`, `swing_status_2019_purge.csv` | Swing-pricing status at exit for the 78 FTN losers and the 60 largest 2019 exits | `code/build/swing_build_outputs.py`, `swing_notes.md` |
| `lseg/funds_input.csv` | 205 funds (winners and losers) with round, award and exit dates: input to the 26 Oct NAV pull | by hand from round membership |
| `lseg/lseg_input.csv`, `isin_list_lseg.csv`, `isin_list_lseg_v2.csv` | Request lists for the LSEG and Datastream pulls | |
| `swing/swing_status_fill_2026-10-27.csv` | Swing-pricing status at exit for the 47 funds that were unverified in the two files above (29 losers, 18 from the 2019 purge), with verbatim quote, document date and url. yes 19, partial 10, levy 1, no 17. Three inference cases flagged in document_title (Monyx x7, CB European Quality, East Capital). | agent run 27 Oct 2026 from fondbestämmelser and prospectuses |
| `holdings_external/holdings_external.csv` (+ `README.md`) | Full portfolio holdings for the 11 losers that do not report to FI, at the month-end before award and before the move (753 rows, 22 fund-dates). Full on both dates for 9 funds (4 of them from one document before both dates), Holberg top 20 on the second date, SEB Sweden Equity top 25 only from a distributor page. No instrument ISINs in any source. Per-fund sources and gaps in the README. | agent run 27 Oct 2026 from annual, semi-annual and monthly reports |

## data/derived: what scripts produced

| Folder | What | Script | Read by |
|---|---|---|---|
| `ppm/ppm_panel_2018_2026.csv` | Monthly PPM fund panel 2018 to 2026 (53,062 rows) | `build_ppm_panel_2018.py` | pressure, swing build |
| `ftn/` | PPM to SHoF crosswalk, FTN bids (290), category fees, winners' fee series, reallocation of the losers, panel 2022 to 2026, non-PPM monthly panel | `build_ppm_panel_2022.py` and agent runs of 11 Oct | exit days (crosswalk), facts |
| `exit_days/` | Daily TNA and flows of the 78 losers (84,696 rows, 2018 to 2026-09-30) and one row per loser with its tranche days | `detect_exit_days.py` | pressure, dilution |
| `measurements/` | Round membership (131 fund-rounds, the key file), loser decomposition, monthly flows, FI net demand by company (fip_*), 2019 comparison | `code/build/agent_runs/measurements_*.py` (archival) | exit days, pressure, swing build |
| `facts/` | Four institutional facts from the sticky-money design (appeal, gender, share class, savings, concentration) | `agent_runs/facts_*.py` (archival) | thesis text, maybe |
| `fi/fi_holdings_long.csv.gz` | All FI holdings in long form, 3,064,860 rows, 31 quarters, 886 funds (LFS) | the notebook, cell 16 to 17 | the notebook |
| `shof_monthly/` | SHoF valuations and reinvested prices aggregated to month-end | `shof_monthly.py` | facts |

## output

| Folder | What | Script |
|---|---|---|
| `omxsb_replication/` | `events_car.csv` (380 events with CARs vs OMXSBGI and OMXSGI), `nettrading_omxsb.csv` (index-fund and all-fund net trading, 259 events after 2018Q4), `index_funds.csv` (14 OMXSB trackers), `holdings_price_check.csv`, `numbers.json`, `exhibits_manifest.md`, `tables/` (36), `figures/` (6 as csv, pdf, png) | `code/notebooks/replication_omxsb.ipynb`, 25 Oct |
| `omxsb_replication_2007/` | The same replication extended to 2007-2026 (536 events in the list, 505 with prices, 487 in the sample, 39 reviews, five periods with 2007–2012 first) on `panel_2005_2026`: `mapping_review.txt` and `coverage_failures.csv` (RIC mapping of the 2007-2012 events, 31 events without prices), `CHECK.md` and `check_2013_2026_vs_original.csv` (2013-2026 reproduces the original run in 28 of 30 Table 2 cells; the two differences come from 136 stock-days missing in the 2005 pull), `table2_old_vs_new.md` (Table 2, F-test and trend test, 27 vs 39 reviews), `events_car.csv`, `nettrading_omxsb.csv`, `numbers.json`, `exhibits_manifest.md`, `table2_phase1_vs_gs.md` (zero-filled vs G&S missing-day convention), `tables/` (61 files: adds tab_00_by_year, tab_07_spread, tab_08_preannouncement, tab_02b_trend, tab_02c_ftest, tabA_08_sample_sensitivity, tabA_09_sample_selection, tab_02_car_long_phase1), `figures/` (21, adds fig_02_by_year). Phase 2 of the notebook follows Greenwood–Sammon exactly where their text is explicit: missing stock-days kept as NaN (event drops from the window), AD/ED moved to the next trading day, Table 3 with uncentred controls and daily-turnover excess turnover, Figure 8 normalised at AD+10, Table 5 marked as an extension | `code/notebooks/replication_omxsb_2007.ipynb`, 28 Oct |
| `omxsb_replication_2007/mechanisms/` | Greenwood–Sammon's five explanations (sections 2.1-2.5, Fig. 3) on OMXSB 2007-2026: `PLAN.md` (test-by-test plan and NBER/HBS/JF differences), `RESULTS.md` (table with HC1/CR1/wild-bootstrap inference, flagged problems), `numbers_mechanisms.json`, `results_table_long.csv`, E1 Table 3 (`e1_table3_long.csv`, `e1_table3_size_top100.csv`), E2 spreads (`e2_spread_by_year.csv`, `fig_e2_*`), E3 check (`e3_omxsb_events_vs_omxs30_membership.csv`), E4 figures 8/9/10 (`fig_e4a_*`, `fig_e4b_*`, `fig_e4c_*`, `e4c_rank_of_additions.csv`), E5 figure 11 and Table 4 (`fig_e5a_*`, `e5b_table4_medians_by_year.csv`), demand (`fig_d_*`), step-1 flags (`step1_deletion_flags.csv`), membership reconstruction (`omxsb_membership_by_review.csv`, `membership_coverage_by_review.csv`, `membership_missing_mcap_by_review.csv`, `membership_inconsistencies.csv`), `tracker_aum_daily_interpolated.csv`, `events_mechanisms.csv` | `code/build/mechanisms_2007.py`, 28 Oct |
| `tables/NOTES.md` | One sentence per thesis table, written when the table is done | by hand |

---

# Generated file tables (27 Oct 2026)

Sizes, row counts and the first columns of every file. Regenerate with the snippet in `archive/inventory/STRUKTUR_2026-10-27.md` or by hand.

### `data/raw/fi/`

31 filer, 168 MB. Första: `Fondinnehav_2018Q4_2022-11-16 17.05.zip`, sista: `Fondinnehav_2026Q2_2026-10-14 08.12.zip`.

### `data/raw/fi/earlier_download_2026-10/`

| fil | storlek | innehåll |
|---|---|---|
| `fi_2023q4.zip` | 5.8 MB | 761 filer i zip |
| `fi_2024q1.zip` | 6.1 MB | 759 filer i zip |
| `fi_2024q2.zip` | 5.9 MB | 749 filer i zip |
| `fi_2026q2.zip` | 6.4 MB | 726 filer i zip |

### `data/raw/ftn/`

| fil | storlek | innehåll |
|---|---|---|
| `FTN upphandlingsrapport 25 mars 2024 sve.pdf` | 6.7 MB |  |
| `FTN upphandlingsrapport Europa smabolag.pdf` | 3.8 MB |  |
| `FTN upphandlingsrapport Global Aktiv SE.pdf` | 4.4 MB |  |
| `FTN upphandlingsrapport Sverige Aktiv SE.pdf` | 5.3 MB |  |
| `FTN upphandlingsrapport Sverige Passiv SE.pdf` | 6.8 MB |  |
| `FTN upphandlingsrapport Sverige smabolag.pdf` | 4.3 MB |  |
| `FTN upphandlingsrapport Teknologi.pdf` | 3.9 MB |  |
| `FTN upphandlingsrapport nordiska aktiefonder SE_2.pdf` | 7.4 MB |  |
| `FTN upphandlingsrapport nordiska smabolagsfonder SE.pdf` | 7.5 MB |  |
| `FTN_Upphandlingsrapport_Europa index sv ny.pdf` | 4.8 MB |  |
| `FTN_Upphandlingsrapport_Global index sv.pdf` | 5.0 MB |  |
| `ftn_europe_active_2024.pdf` | 6.7 MB |  |
| `ftn_europe_active_2024.txt` | 93 kB |  |

### `data/raw/lseg/datastream/`

| fil | storlek | innehåll |
|---|---|---|
| `LSEG_DATOR_2026-10-15.zip` | 31.9 MB | 4 filer i zip |

### `data/raw/lseg/panel_2005_2026/`

| fil | storlek | innehåll |
|---|---|---|
| `fund_nav_tna_daily.csv` | 10.1 MB | 162,803 rader, 5 kol: date, NAV, lipper_ric, fund_name, group |
| `indices_daily (1).csv` | 875 kB | 32,775 rader, 3 kol: ric, date, close |
| `indices_daily_extra.csv` | 1.8 MB | 64,171 rader, 3 kol: ric, date, close |
| `stocks_daily_2005.csv.gz` | 105.1 MB | (kunde inte läsa: BadGzipFile) |
| `stocks_daily_2005.parquet` | 136.8 MB | 4,340,104 rader, 11 kol: ric, date, close, totret, volume, mcap, shares, turnover |
| `stocks_static_2005.csv` | 137 kB | 2,117 rader, 8 kol: ric, first_date, last_date, n_days, DTSubjectName, IssueISIN, RetireDate, ExchangeCode |
| `td_failures (1).csv` | 2 kB | 21 rader, 2 kol: ric, error |
| `td_funds_resolved.csv` | 29 kB | 205 rader, 11 kol: group, fondnr, name, isin, round, award_date, exit_date, lipper_ric … |
| `td_rics_final.csv` | 23 kB | 2,135 rader, 1 kol: ric |
| `td_universe.csv` | 127 kB | 1,291 rader, 9 kol: RIC, DTSubjectName, IssueISIN, ExchangeCode, ExchangeName, RCSAssetCategoryLeaf, PrimaryRIC, TickerSymbol … |

### `data/raw/lseg/panel_2012_2026/`

| fil | storlek | innehåll |
|---|---|---|
| `indices_daily.csv` | 599 kB | 22,311 rader, 3 kol: ric, date, close |
| `stocks_daily.csv.gz` | 72.5 MB | 3,206,212 rader, 9 kol: ric, date, close, totret, volume, mcap, shares, turnover … |
| `stocks_static.csv` | 116 kB | 1,667 rader, 8 kol: ric, first_date, last_date, n_days, DTSubjectName, IssueISIN, RetireDate, ExchangeCode |
| `td_failures.csv` | 7 kB | 68 rader, 2 kol: ric, error |

### `data/raw/lseg/panel_eu/`

| fil | storlek | innehåll |
|---|---|---|
| `fx_sek_daily.csv` | 1.4 MB | 42,725 rader, 3 kol: pair, date, rate |
| `stocks_daily_eu.csv.gz` | 28.0 MB | 762,161 rader, 11 kol: ric, date, close, totret, volume, mcap, shares, turnover … |
| `stocks_daily_eu.parquet` | 27.8 MB | 762,161 rader, 11 kol: ric, date, close, totret, volume, mcap, shares, turnover |
| `stocks_static_eu.csv` | 57 kB | 670 rader, 10 kol: ric, first_date, last_date, n_days, DTSubjectName, IssueISIN, RetireDate, ExchangeCode … |
| `td_isin_resolved.csv` | 81 kB | 630 rader, 16 kol: RIC, DTSubjectName, IssueISIN, ExchangeCode, ExchangeName, RCSAssetCategoryLeaf, PrimaryRIC, TickerSymbol … |
| `td_rics_final.csv` | 5 kB | 630 rader, 1 kol: ric |

### `data/raw/ppm/`

| fil | storlek | innehåll |
|---|---|---|
| `FEES.txt` | 25.8 MB |  |
| `Lista alla fonder 2026.xls` | 594 kB |  |
| `ppm_nav_2024.xlsx` | 5.8 MB |  |

### `data/raw/ppm/2001-2008/2001/`

12 filer, 2 MB. Första: `PPM 010131.xls`, sista: `PPM 011231.xls`.

### `data/raw/ppm/2001-2008/2002/`

12 filer, 2 MB. Första: `PPM 020131.xls`, sista: `PPM 021231.xls`.

### `data/raw/ppm/2001-2008/2003/`

12 filer, 2 MB. Första: `PPM 030131.xls`, sista: `PPM 031231.xls`.

### `data/raw/ppm/2001-2008/2004/`

12 filer, 2 MB. Första: `PPM 040131.xls`, sista: `PPM 041231.xls`.

### `data/raw/ppm/2001-2008/2005/`

12 filer, 2 MB. Första: `PPM 050131.xls`, sista: `PPM 051231.xls`.

### `data/raw/ppm/2001-2008/2006/`

11 filer, 7 MB. Första: `Kopia av PPM 060930.xls`, sista: `PPM 061231.xls`.

### `data/raw/ppm/2001-2008/2007/`

12 filer, 8 MB. Första: `Kopia av PPM 070831.xls`, sista: `PPM 071231.xls`.

### `data/raw/ppm/2001-2008/2008/`

12 filer, 8 MB. Första: `PPM 080131.xls`, sista: `PPM 081231.xls`.

### `data/raw/ppm/2009-2014/2009/`

12 filer, 10 MB. Första: `PPM 090131.xls`, sista: `PPM 091231.xls`.

### `data/raw/ppm/2009-2014/2010/`

12 filer, 15 MB. Första: `PM 100131.xls`, sista: `PM 101231.xls`.

### `data/raw/ppm/2009-2014/2011/`

12 filer, 16 MB. Första: `PM 110131.xls`, sista: `PM 111231.xlsm`.

### `data/raw/ppm/2009-2014/2012/`

12 filer, 10 MB. Första: `PM 120131.xlsm`, sista: `PM 121231.xlsm`.

### `data/raw/ppm/2009-2014/2013/`

12 filer, 16 MB. Första: `PM 130131.xlsm`, sista: `PM 131231.xlsm`.

### `data/raw/ppm/2009-2014/2014/`

12 filer, 17 MB. Första: `PM 140131.xlsm`, sista: `PM 141231.xlsm`.

### `data/raw/ppm/2015-2020/2015/`

12 filer, 11 MB. Första: `PM 150131.xlsm`, sista: `PM 151231.xlsm`.

### `data/raw/ppm/2015-2020/2016/`

12 filer, 11 MB. Första: `M_nadsstatistik fonder och fondsparande 160731.xlsm`, sista: `Statistik premiepension 2016-12-31.xlsm`.

### `data/raw/ppm/2015-2020/2017/`

13 filer, 10 MB. Första: `Lista av tidigare fondkategorier och de nya som f_rekommer i m_nadsstatistiken.xlsx`, sista: `Statistik premiepension 2017-08-31.xlsm`.

### `data/raw/ppm/2015-2020/2018/`

12 filer, 10 MB. Första: `Statistik Premiepension 2018-01-31.xlsm`, sista: `Statistik Premiepension 2018-12-31.xlsm`.

### `data/raw/ppm/2015-2020/2019/`

12 filer, 10 MB. Första: `Statistik Premiepension 2019-01-31.xlsm`, sista: `Statistik Premiepension 2019-12-31.xlsm`.

### `data/raw/ppm/2015-2020/2020/`

12 filer, 11 MB. Första: `Kopia av Statistik Premiepension 2020-02-29.xlsm`, sista: `Statistik-Premiepension-2020-11-30.xlsm`.

### `data/raw/ppm/2021-2026/2021/`

12 filer, 14 MB. Första: `Statistik-Premiepension-2021-01-31.xlsm`, sista: `Statistik-premiepension-2021-12-31.xlsm`.

### `data/raw/ppm/2021-2026/2022/`

12 filer, 21 MB. Första: `Statistik premiepension 2022-12-31.xlsm`, sista: `Statistik-premiepension-2022-09-30.xlsm`.

### `data/raw/ppm/2021-2026/2023/`

12 filer, 22 MB. Första: `Statistik-Premiepension-2023-02-28.xlsm`, sista: `Statistik-premiepension-2023-03-31.xlsm`.

### `data/raw/ppm/2021-2026/2024/`

12 filer, 20 MB. Första: `Statistik premiepension 2024-03-31.xlsm`, sista: `statistik-premiepension-2024-11-30.xlsm`.

### `data/raw/ppm/2021-2026/2025/`

12 filer, 20 MB. Första: `Statistik-Premiepension-2025-01-31.xlsm`, sista: `Statistik-Premiepension-2025-12-31.xlsm`.

### `data/raw/ppm/2021-2026/2026/`

8 filer, 13 MB. Första: `Statistik-Premiepension-2026-01-31.xlsm`, sista: `Statistik-Premiepension-2026-08-31.xlsm`.

### `data/raw/shof/`

| fil | storlek | innehåll |
|---|---|---|
| `fundmaster.xlsx` | 21.0 MB |  |
| `shof_field_definitions.pdf` | 1.4 MB |  |
| `shof_field_definitions.txt` | 45 kB |  |
| `shof_fundmaster.zip` | 20.9 MB | 1 filer i zip |

### `data/input/lseg/`

| fil | storlek | innehåll |
|---|---|---|
| `funds_input.csv` | 16 kB | 205 rader, 7 kol: group, fondnr, name, isin, round, award_date, exit_date |
| `isin_list_lseg.csv` | 170 kB | 4,452 rader, 2 kol: isin, name |
| `isin_list_lseg_v2.csv` | 396 kB | 7,395 rader, 5 kol: isin, name, country, source, tier |
| `lseg_input.csv` | 156 kB | 2,901 rader, 4 kol: id, id_type, name, group |

### `data/input/omxsb/`

| fil | storlek | innehåll |
|---|---|---|
| `omxs30_changes_2005_2026.csv` | 19 kB | 48 rader, 13 kol: event_id, effective_date, announcement_date, company, ticker, isin, type, reason … |
| `omxs30_notes.md` | 26 kB |  |
| `omxsb_changes_2013_2026.csv` | 145 kB | 394 rader, 11 kol: event_id, effective_date, announcement_date, company, ticker, isin, type, review_cycle … |
| `omxsb_changes_2007_2026.csv` | 223 kB | 536 rader, 11 kol: event_id, effective_date, announcement_date, company, ticker, isin, type, review_cycle … |
| `omxsb_events_with_ric.csv` | 149 kB | 394 rader, 13 kol: event_id, effective_date, announcement_date, company, ticker, isin, type, review_cycle … |
| `omxsb_events_with_ric_2007_2026.csv` | 229 kB | 536 rader, 13 kol: event_id, effective_date, announcement_date, company, ticker, isin, type, review_cycle … |
| `omxsb_notes.md` | 16 kB |  |

### `data/input/swing/`

| fil | storlek | innehåll |
|---|---|---|
| `swing_notes.md` | 20 kB |  |
| `swing_status_2019_purge.csv` | 17 kB | 60 rader, 16 kol: rank_by_max_mv, fondnr, fondnamn, isin, forvaltare_panel, svensk_panel, domicile, kategori … |
| `swing_status_ftn_losers.csv` | 41 kB | 78 rader, 20 kol: round, award, fondnr, fondnamn, isin, kategori, avslutsdatum, mv_award_msek … |

### `data/derived/exit_days/`

| fil | storlek | innehåll |
|---|---|---|
| `exit_days_by_loser.csv` | 14 kB | 78 rader, 19 kol: round, award, fondnr, fondnamn, kategori, performanceid, ccy, avslutsdatum … |
| `losers_daily_valuations.csv` | 6.7 MB | 84,696 rader, 9 kol: performanceId, date, classcurrencyiso, fundcurrencyiso, netflowclass, netflowfund, shares, tnaclass … |

### `data/derived/facts/`

| fil | storlek | innehåll |
|---|---|---|
| `fact1_GA_losers_fundlevel.csv` | 5 kB | 38 rader, 9 kol: fondnr, fondnamn, hn, mv_tot, val_tot, fee_net, val_aug26, cum_hn_pct … |
| `fact1_GA_monthly.csv` | 4 kB | 24 rader, 13 kol: role, window, date, n, hn, mv_lag, val, val_lag … |
| `fact1_GA_vs_control_Mar_Aug26.csv` | 0 kB | 3 rader, 6 kol: group, n, median_cum_hn_pct, pooled_cum_hn_pct, median_dval_pct, pooled_dval_pct |
| `fact1_cum_outflow_by_event_month.csv` | 4 kB | 45 rader, 8 kol: group, m, n_funds, cum_hn_pct, cum_hn_pct_exDec, cum_dval_pct, dec_in_window, all_losers_unmoved |
| `fact2_gender_baseline_other_equity.csv` | 1 kB | 9 rader, 7 kol: round, A, E, n_funds, base_optout_women_pct, base_optout_men_pct, base_gap_pp |
| `fact2_gender_by_round.csv` | 5 kB | 16 rader, 20 kol: sample, round, n_funds, savers_k, savers_m, share_women_pct, months_med, optout_women_pct … |
| `fact2_gender_fundlevel.csv` | 166 kB | 544 rader, 26 kol: sample, round, fondnr, fondnamn, A, E, M, exited … |
| `fact3_summary.csv` | 1 kB | 11 rader, 14 kol: round, PPM-dedicated class, retail class with rebate, n, pct_dedicated, table, class_type, n_new … |
| `fact3_winners_shareclass.csv` | 9 kB | 49 rader, 20 kol: round, fondnr, name, ny, fee_awarded, contract_month, fee_net_before, fee_gross_before … |
| `fact4_losers_moved.csv` | 10 kB | 78 rader, 11 kol: round, fondnr, fondnamn, fee_before, default_mv, val_at_move, vol_out, sav_vol … |
| `fact4_savings_by_round.csv` | 4 kB | 9 rader, 29 kol: round, award, n_win_inc, n_win_new, n_losers, cap_inc_winners_bn, fee_inc_before_cw, fee_inc_after_cw … |
| `fact4_winners_fees.csv` | 7 kB | 53 rader, 12 kol: round, fondnr, fondnamn, role, flag_month, contract_month, fee_before, fee_after … |
| `fact5_concentration.csv` | 10 kB | 35 rader, 13 kol: round, universe, when, date, n_funds, n_companies, cap_bn, top1_pct … |

### `data/derived/fi/`

| fil | storlek | innehåll |
|---|---|---|
| `fi_holdings_long.csv.gz` | 101.3 MB | 3,064,860 rader, 17 kol: Tillgångsslag_enligt_LVF_5_kap, Instrumentnamn, ISIN-kod_instrument, Landkod_Emittent, Valuta, Antal, Kurs_som_använts_vid_värdering_av_instrumentet, Marknadsvärde_instrument … |

### `data/derived/ftn/`

| fil | storlek | innehåll |
|---|---|---|
| `bids_long.csv` | 109 kB | 290 rader, 53 kol: round, category, announce_date, bid_deadline, award_date, n_bids_reported, n_qualified_reported, bid_no … |
| `crosswalk_ppm_shof.csv` | 70 kB | 514 rader, 12 kol: fondnr, isin_used, match_method, performanceid, fundid, fundname_ms, status, obsoletedate … |
| `ftn_category_fees.csv` | 1 kB | 11 rader, 16 kol: round, category, award_date, fee_before_ew_after_rebate_s42, before_reference_date, before_median, before_min, before_max … |
| `panel_nonppm_monthly.csv` | 7.3 MB | 35,328 rader, 26 kol: fondnr, ym, fundid, performanceid, tnafund, ccy_fund, last_date, nf_fund … |
| `ppm_panel_2022_2026.csv` | 5.9 MB | 24,554 rader, 25 kol: fondnr, fondnamn, val_k, val_m, val_tot, mv_k, mv_m, mv_tot … |
| `reallocation_losers.csv` | 17 kB | 78 rader, 21 kol: round, fondnr, fondnamn, exited, last_month, avslutsdatum, move_start, n_tranche_months … |
| `reallocation_summary_by_round.csv` | 3 kB | 19 rader, 14 kol: round, sample, n_los, mv_award_bn, vol_bn, default_bn, pct_vol_cap, pct_vol_cap_exDec … |
| `unmatched_for_lseg.csv` | 27 kB | 144 rader, 11 kol: round, bid_no, manager, fund_name, winner, on_ppm_at_announce, shof_fundid, shof_fundname … |
| `winners_fee_series.csv` | 296 kB | 2,370 rader, 11 kol: round, award, fondnr, fondnamn, isin, kategori, date, upphandlad … |

### `data/derived/measurements/`

| fil | storlek | innehåll |
|---|---|---|
| `agent2019_t2_decomposition_summary.csv` | 15 kB | 24 rader, 43 kol: sample, n, mv_pre_bn, savers_pre, w1_pct_vol_cap_churnadj, w1_n, w1_vol_bn, w1_pct_vol_cap … |
| `agent2019_t3_totals_2019.json` | 1 kB |  |
| `agent2019_t4_side_by_side_ftn.csv` | 3 kB | 13 rader, 8 kol: sample, n_funds, mv_at_event_bn, vol_bn, default_bn, pct_vol_cap, pct_vol_sav, note |
| `agentA_summary_by_round.csv` | 3 kB | 19 rader, 14 kol: round, sample, n_los, mv_award_bn, vol_bn, default_bn, pct_vol_cap, pct_vol_cap_exDec … |
| `agentA_task1_round_membership.csv` | 17 kB | 131 rader, 12 kol: round, award, fondnr, fondnamn, kategori, role, mv_award, val_award … |
| `agentA_task2_loser_decomposition.csv` | 17 kB | 78 rader, 21 kol: round, fondnr, fondnamn, exited, last_month, avslutsdatum, move_start, n_tranche_months … |
| `agentA_task3_monthly_flows_winners_losers.csv` | 155 kB | 1,433 rader, 9 kol: round, role, fondnr, fondnamn, date, mv_tot, val_tot, handel_netto … |
| `bids_long.csv` | 109 kB | 290 rader, 53 kol: round, category, announce_date, bid_deadline, award_date, n_bids_reported, n_qualified_reported, bid_no … |
| `execution_windows_monthly.csv` | 9 kB | 102 rader, 9 kol: round, month, rel_month, loser_handel_netto_bn, loser_residual_exit_bn, loser_total_out_pct_of_award_cap, winner_handel_netto_bn, winner_in_pct_of_award_cap … |
| `fip_allnames_summary.csv` | 2 kB | 5 rader, 14 kol: tag, n_names_with_cap, n_fetched, n_approx, sd_fip_pct, p90_abs_fip, p99_abs_fip, max_abs_fip … |
| `fip_company_Nordic_active_2024q2_2024q2_actual.csv` | 5 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_company_SE_active_2024q2_2024q2_actual.csv` | 6 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_company_SE_active_2024q2_2024q2_equal_new.csv` | 6 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_company_SE_active_2026q2_2026q2_actual.csv` | 6 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_company_SE_index_2024q2_2026q2_actual.csv` | 6 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_company_SE_index_2026q2_2026q2_actual.csv` | 6 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_company_SE_index_2026q2_2026q2_actual_AvanzaZeroOnly.csv` | 6 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_company_SE_index_2026q2_2026q2_actual_exAvanzaZero.csv` | 6 kB | 40 rader, 11 kol: company, buy, sell, net, gross, cap_bn, approx, n_classes … |
| `fip_summary.csv` | 1 kB | 8 rader, 13 kol: tag, n_companies, sd_net_isin_m, sd_net_company_m, top10_sq_share_company, n_company_abs_net_gt_100m, n_mapped, mapped_share_abs_net … |
| `fund_fi_mapping.csv` | 14 kB | 91 rader, 15 kol: round, fondnr, fondnamn, role, mv_award, fi_2024q2, fi_2026q2, in_fi … |
| `winners_fee_series.csv` | 296 kB | 2,370 rader, 11 kol: round, award, fondnr, fondnamn, isin, kategori, date, upphandlad … |

### `data/derived/ppm/`

| fil | storlek | innehåll |
|---|---|---|
| `ppm_panel_2018_2026.csv` | 12.3 MB | 53,062 rader, 25 kol: fondnr, fondnamn, val_k, val_m, val_tot, mv_k, mv_m, mv_tot … |

### `data/derived/shof_monthly/`

| fil | storlek | innehåll |
|---|---|---|
| `monthly.log` | 0 kB |  |
| `monthly.py` | 2 kB |  |
| `shof_rips_monthly.csv` | 18.0 MB | 442,507 rader, 5 kol: performanceId, returntype, ym, last_date, tri_sek |
| `shof_valuations_monthly.csv` | 44.3 MB | 457,842 rader, 12 kol: performanceId, ym, secid, ccy_class, ccy_fund, last_date, tnaclass, tnafund … |

### `output/omxsb_replication/`

| fil | storlek | innehåll |
|---|---|---|
| `events_car.csv` | 310 kB | 380 rader, 54 kol: event_id, effective_date, announcement_date, company, ticker, isin, type, review_cycle … |
| `exhibits_manifest.md` | 2 kB |  |
| `holdings_price_check.csv` | 47 kB | 259 rader, 20 kol: event_id, company, qb, qa, n_rows_b, n_rows_a, fi_price_b, fi_kurs_b … |
| `index_funds.csv` | 4 kB | 14 rader, 12 kol: Fond_institutnummer, Fondbolag_namn, Fond_namn, Fond_ISIN, benchmark, q_first, q_last, score … |
| `nettrading_omxsb.csv` | 74 kB | 259 rader, 25 kol: event_id, company, RIC, type, AD, ED, period, qb … |
| `numbers.json` | 1 kB |  |

### `output/omxsb_replication/figures/`

18 filer, 1 MB. Första: `fig_01_nettrading.csv`, sista: `fig_11_volume.png`.

### `output/omxsb_replication/tables/`

36 filer, 0 MB. Första: `tabA_01_car_omxsgi_long.csv`, sista: `tab_06_volume_share.tex`.

### `output/omxsb_replication_2007/`

| fil | storlek | innehåll |
|---|---|---|
| `CHECK.md` | 6 kB | reproduktionskontroll 2013-2026 mot originalkörningen |
| `check_2013_2026_vs_original.csv` | 7 kB | 30 rader, 20 kol: type, window, period, mean_orig, mean_new, d_mean, se_hc1_orig, se_hc1_new … |
| `coverage_failures.csv` | 2 kB | 31 rader, 6 kol: event_id, company, ticker, RIC, effective_date, days_with_price |
| `events_car.csv` | 409 kB | 487 rader, 55 kol: event_id, effective_date, announcement_date, company, ticker, isin, type, review_cycle … |
| `exhibits_manifest.md` | 3 kB |  |
| `holdings_price_check.csv` | 48 kB | 259 rader, 20 kol |
| `index_funds.csv` | 4 kB | 14 rader, 12 kol |
| `mapping_review.txt` | 15 kB | RIC-mappning av 2007-2012-händelserna: återanvända, ticker, namn, omatchade, täckning |
| `nettrading_omxsb.csv` | 76 kB | 259 rader, 25 kol |
| `numbers.json` | 1 kB |  |
| `table2_old_vs_new.md` | 7 kB | Tabell 2 ny (5 perioder) och original (4), F-test och trendtest |
| `table2_phase1_vs_gs.md` | 10 kB | Tabell 2 fas 1 (nollfyllda saknade dagar) mot G&S-konventionen (NaN), och 2013-2026 mot originalet |
| `table2_phase1_vs_gs.csv` | 4 kB | 36 rader, 11 kol: type, window, period, mean_phase1, mean_gs, d_mean, se_hc1_phase1, se_hc1_gs … |

### `output/omxsb_replication_2007/figures/`

21 filer, 1 MB. Första: `fig_01_nettrading.csv`, sista: `fig_11_volume.png`.

### `output/omxsb_replication_2007/tables/`

61 filer, 0 MB. Första: `tabA_01_car_omxsgi_long.csv`, sista: `tab_08_preannouncement.tex`.

### `output/tables/`

| fil | storlek | innehåll |
|---|---|---|
| `NOTES.md` | 0 kB |  |

<!-- OMXSB_AUDIT_20261031 -->

## OMXSB verification audit 31 Oct 2026

Base commit: `b886f5b744f797a6c1252f0e41fe2b740591c8c3`. Raw inputs unchanged. The original `omxsb_replication_2007/` exports remain frozen; corrected exports are in the separate audit folder. The full artifact registry includes SHA256, byte size and role for every artifact. Scientific conclusions and unresolved history are in `output/omxsb_audit_20261031/GRANSKNING.md`.

| File | Role/source and generator | Bytes |
|---|---|---|
| `output/omxsb_audit_20261031/artifact_inventory.csv` | Per-file SHA256 registry; `code/build/audit_omxsb_finalize.py` | generated |
| `output/omxsb_audit_20261031/baseline/check_2013_2026_vs_original.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 7204 |
| `output/omxsb_audit_20261031/baseline/events_car.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 442285 |
| `output/omxsb_audit_20261031/baseline/figures/fig_01_nettrading.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 257 |
| `output/omxsb_audit_20261031/baseline/figures/fig_02_by_year.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 1868 |
| `output/omxsb_audit_20261031/baseline/figures/fig_03_scatter.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 254 |
| `output/omxsb_audit_20261031/baseline/figures/fig_08_car_announcement.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 17265 |
| `output/omxsb_audit_20261031/baseline/figures/fig_09_car_effective.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 16167 |
| `output/omxsb_audit_20261031/baseline/figures/fig_10_size_rank.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 1239 |
| `output/omxsb_audit_20261031/baseline/figures/fig_11_volume.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 7018 |
| `output/omxsb_audit_20261031/baseline/holdings_price_check.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 48310 |
| `output/omxsb_audit_20261031/baseline/index_funds.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 3616 |
| `output/omxsb_audit_20261031/baseline/mechanisms/e1_table3_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 9932 |
| `output/omxsb_audit_20261031/baseline/mechanisms/e1_table3_size_top100.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2329 |
| `output/omxsb_audit_20261031/baseline/mechanisms/e2_spread_by_year.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2613 |
| `output/omxsb_audit_20261031/baseline/mechanisms/e3_omxsb_events_vs_omxs30_membership.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 3845 |
| `output/omxsb_audit_20261031/baseline/mechanisms/e4c_rank_of_additions.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 33571 |
| `output/omxsb_audit_20261031/baseline/mechanisms/e5b_table4_medians_by_year.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 3013 |
| `output/omxsb_audit_20261031/baseline/mechanisms/events_mechanisms.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 126729 |
| `output/omxsb_audit_20261031/baseline/mechanisms/fig_d_expected_demand_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2290 |
| `output/omxsb_audit_20261031/baseline/mechanisms/fig_d_fig3_nettrading.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 19065 |
| `output/omxsb_audit_20261031/baseline/mechanisms/fig_e4a_car_announcement.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 34218 |
| `output/omxsb_audit_20261031/baseline/mechanisms/fig_e4b_car_effective.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 32127 |
| `output/omxsb_audit_20261031/baseline/mechanisms/fig_e4c_rank.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2225 |
| `output/omxsb_audit_20261031/baseline/mechanisms/fig_e5a_volume.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 13971 |
| `output/omxsb_audit_20261031/baseline/mechanisms/membership_coverage_by_review.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 3983 |
| `output/omxsb_audit_20261031/baseline/mechanisms/membership_inconsistencies.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 275 |
| `output/omxsb_audit_20261031/baseline/mechanisms/membership_missing_mcap_by_review.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 5775 |
| `output/omxsb_audit_20261031/baseline/mechanisms/numbers_mechanisms.json` | baseline rerun; audit_omxsb_run.py / preserved commit | 22952 |
| `output/omxsb_audit_20261031/baseline/mechanisms/omxsb_membership_by_review.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 36674 |
| `output/omxsb_audit_20261031/baseline/mechanisms/results_table_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 55736 |
| `output/omxsb_audit_20261031/baseline/mechanisms/step1_deletion_flags.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 34975 |
| `output/omxsb_audit_20261031/baseline/mechanisms/tracker_aum_daily_interpolated.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 122979 |
| `output/omxsb_audit_20261031/baseline/nettrading_omxsb.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 75897 |
| `output/omxsb_audit_20261031/baseline/numbers.json` | baseline rerun; audit_omxsb_run.py / preserved commit | 961 |
| `output/omxsb_audit_20261031/baseline/period_sensitivity/table2_by_period_length_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 38382 |
| `output/omxsb_audit_20261031/baseline/period_sensitivity/trend_by_period_length.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 3784 |
| `output/omxsb_audit_20261031/baseline/period_sensitivity/trend_tests.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 19496 |
| `output/omxsb_audit_20261031/baseline/run_complete.json` | baseline rerun; audit_omxsb_run.py / preserved commit | 601 |
| `output/omxsb_audit_20261031/baseline/table2_phase1_vs_gs.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 3632 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_01_car_omxsgi_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 4525 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_02_isin_matches.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 11708 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_02_isin_matches_check.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 15258 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_03_index_funds.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 963 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_04_split_factors.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 431 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_05_dropped_events.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2029 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_06_event_chain.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 319 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_07_car_robustness.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 4625 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_07_car_robustness_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 14874 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_08_sample_sensitivity.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 1172 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_08_sample_sensitivity_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 1591 |
| `output/omxsb_audit_20261031/baseline/tables/tabA_09_sample_selection.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 472 |
| `output/omxsb_audit_20261031/baseline/tables/tab_00_by_year.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2765 |
| `output/omxsb_audit_20261031/baseline/tables/tab_01_sample.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 311 |
| `output/omxsb_audit_20261031/baseline/tables/tab_02_car.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 1598 |
| `output/omxsb_audit_20261031/baseline/tables/tab_02_car_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 4848 |
| `output/omxsb_audit_20261031/baseline/tables/tab_02_car_long_oldperiods.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 4438 |
| `output/omxsb_audit_20261031/baseline/tables/tab_02_car_long_phase1.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 4423 |
| `output/omxsb_audit_20261031/baseline/tables/tab_02b_trend_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 751 |
| `output/omxsb_audit_20261031/baseline/tables/tab_02c_ftest_old_vs_new.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 957 |
| `output/omxsb_audit_20261031/baseline/tables/tab_03_determinants_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2607 |
| `output/omxsb_audit_20261031/baseline/tables/tab_04_institutions.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 902 |
| `output/omxsb_audit_20261031/baseline/tables/tab_05_elasticity.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 1557 |
| `output/omxsb_audit_20261031/baseline/tables/tab_05_elasticity_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 2783 |
| `output/omxsb_audit_20261031/baseline/tables/tab_06_volume_share.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 498 |
| `output/omxsb_audit_20261031/baseline/tables/tab_07_spread.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 391 |
| `output/omxsb_audit_20261031/baseline/tables/tab_08_preannouncement.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 5401 |
| `output/omxsb_audit_20261031/baseline/tables/tab_08_preannouncement_long.csv` | baseline rerun; audit_omxsb_run.py / preserved commit | 5434 |
| `output/omxsb_audit_20261031/baseline_comparison.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 3486 |
| `output/omxsb_audit_20261031/baseline_comparison_details.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 11655 |
| `output/omxsb_audit_20261031/candidate_pilot_targets.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 14222 |
| `output/omxsb_audit_20261031/candidate_sample_summary.json` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 560 |
| `output/omxsb_audit_20261031/composition_common_sample.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 408 |
| `output/omxsb_audit_20261031/contrast_tests.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 514 |
| `output/omxsb_audit_20261031/corrected/check_2013_2026_vs_original.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 7204 |
| `output/omxsb_audit_20261031/corrected/events_car.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 442460 |
| `output/omxsb_audit_20261031/corrected/figures/fig_01_nettrading.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 257 |
| `output/omxsb_audit_20261031/corrected/figures/fig_02_by_year.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 1868 |
| `output/omxsb_audit_20261031/corrected/figures/fig_03_scatter.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 254 |
| `output/omxsb_audit_20261031/corrected/figures/fig_08_car_announcement.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 17265 |
| `output/omxsb_audit_20261031/corrected/figures/fig_09_car_effective.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 16167 |
| `output/omxsb_audit_20261031/corrected/figures/fig_10_size_rank.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 1247 |
| `output/omxsb_audit_20261031/corrected/figures/fig_11_volume.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 7018 |
| `output/omxsb_audit_20261031/corrected/holdings_price_check.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 48310 |
| `output/omxsb_audit_20261031/corrected/index_funds.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 3616 |
| `output/omxsb_audit_20261031/corrected/mechanisms/e1_table3_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 9949 |
| `output/omxsb_audit_20261031/corrected/mechanisms/e1_table3_size_top100.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2321 |
| `output/omxsb_audit_20261031/corrected/mechanisms/e2_spread_by_year.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2617 |
| `output/omxsb_audit_20261031/corrected/mechanisms/e3_omxsb_events_vs_omxs30_membership.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 3845 |
| `output/omxsb_audit_20261031/corrected/mechanisms/e4c_rank_of_additions.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 33571 |
| `output/omxsb_audit_20261031/corrected/mechanisms/e5b_table4_medians_by_year.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 3011 |
| `output/omxsb_audit_20261031/corrected/mechanisms/events_mechanisms.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 126817 |
| `output/omxsb_audit_20261031/corrected/mechanisms/fig_d_expected_demand_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2290 |
| `output/omxsb_audit_20261031/corrected/mechanisms/fig_d_fig3_nettrading.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 19065 |
| `output/omxsb_audit_20261031/corrected/mechanisms/fig_e4a_car_announcement.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 34218 |
| `output/omxsb_audit_20261031/corrected/mechanisms/fig_e4b_car_effective.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 32127 |
| `output/omxsb_audit_20261031/corrected/mechanisms/fig_e4c_rank.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2225 |
| `output/omxsb_audit_20261031/corrected/mechanisms/fig_e5a_volume.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 13971 |
| `output/omxsb_audit_20261031/corrected/mechanisms/membership_coverage_by_review.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 3987 |
| `output/omxsb_audit_20261031/corrected/mechanisms/membership_inconsistencies.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 275 |
| `output/omxsb_audit_20261031/corrected/mechanisms/membership_missing_mcap_by_review.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 5775 |
| `output/omxsb_audit_20261031/corrected/mechanisms/numbers_mechanisms.json` | corrected rerun; audit_omxsb_run.py / preserved commit | 22946 |
| `output/omxsb_audit_20261031/corrected/mechanisms/omxsb_membership_by_review.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 36674 |
| `output/omxsb_audit_20261031/corrected/mechanisms/results_table_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 58494 |
| `output/omxsb_audit_20261031/corrected/mechanisms/step1_deletion_flags.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 34975 |
| `output/omxsb_audit_20261031/corrected/mechanisms/tracker_aum_daily_interpolated.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 122979 |
| `output/omxsb_audit_20261031/corrected/nettrading_omxsb.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 75906 |
| `output/omxsb_audit_20261031/corrected/numbers.json` | corrected rerun; audit_omxsb_run.py / preserved commit | 961 |
| `output/omxsb_audit_20261031/corrected/period_sensitivity/table2_by_period_length_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 38395 |
| `output/omxsb_audit_20261031/corrected/period_sensitivity/trend_by_period_length.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 3784 |
| `output/omxsb_audit_20261031/corrected/period_sensitivity/trend_tests.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 19496 |
| `output/omxsb_audit_20261031/corrected/reporting_pair_diagnostics.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 22872 |
| `output/omxsb_audit_20261031/corrected/run_complete.json` | corrected rerun; audit_omxsb_run.py / preserved commit | 601 |
| `output/omxsb_audit_20261031/corrected/table2_phase1_vs_gs.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 3632 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_01_car_omxsgi_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 4526 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_02_isin_matches.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 11708 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_02_isin_matches_check.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 15258 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_03_index_funds.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 963 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_04_split_factors.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 431 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_05_dropped_events.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2029 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_06_event_chain.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 319 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_07_car_robustness.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 4625 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_07_car_robustness_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 14875 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_08_sample_sensitivity.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 1172 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_08_sample_sensitivity_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 1591 |
| `output/omxsb_audit_20261031/corrected/tables/tabA_09_sample_selection.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 472 |
| `output/omxsb_audit_20261031/corrected/tables/tab_00_by_year.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2765 |
| `output/omxsb_audit_20261031/corrected/tables/tab_01_sample.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 311 |
| `output/omxsb_audit_20261031/corrected/tables/tab_02_car.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 1598 |
| `output/omxsb_audit_20261031/corrected/tables/tab_02_car_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 4848 |
| `output/omxsb_audit_20261031/corrected/tables/tab_02_car_long_oldperiods.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 4438 |
| `output/omxsb_audit_20261031/corrected/tables/tab_02_car_long_phase1.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 4423 |
| `output/omxsb_audit_20261031/corrected/tables/tab_02b_trend_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 751 |
| `output/omxsb_audit_20261031/corrected/tables/tab_02c_ftest_old_vs_new.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 957 |
| `output/omxsb_audit_20261031/corrected/tables/tab_03_determinants_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2602 |
| `output/omxsb_audit_20261031/corrected/tables/tab_04_institutions.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 901 |
| `output/omxsb_audit_20261031/corrected/tables/tab_05_elasticity.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 1557 |
| `output/omxsb_audit_20261031/corrected/tables/tab_05_elasticity_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 2783 |
| `output/omxsb_audit_20261031/corrected/tables/tab_06_volume_share.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 498 |
| `output/omxsb_audit_20261031/corrected/tables/tab_07_spread.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 391 |
| `output/omxsb_audit_20261031/corrected/tables/tab_08_preannouncement.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 5401 |
| `output/omxsb_audit_20261031/corrected/tables/tab_08_preannouncement_long.csv` | corrected rerun; audit_omxsb_run.py / preserved commit | 5434 |
| `output/omxsb_audit_20261031/correction_comparison.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 3868 |
| `output/omxsb_audit_20261031/correction_comparison_details.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 207099 |
| `output/omxsb_audit_20261031/data_gaps.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 10351 |
| `output/omxsb_audit_20261031/deletion_flag_reconciliation.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 38905 |
| `output/omxsb_audit_20261031/e5b_before_after.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 1856 |
| `output/omxsb_audit_20261031/event_fund_reporting.csv.gz` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 184243 |
| `output/omxsb_audit_20261031/fi_coverage_by_quarter.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 690 |
| `output/omxsb_audit_20261031/fi_raw_derived_reconciliation.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 664026 |
| `output/omxsb_audit_20261031/fi_raw_parse_errors.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 15 |
| `output/omxsb_audit_20261031/fi_raw_report_inventory.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 5444657 |
| `output/omxsb_audit_20261031/fi_raw_summary.json` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 261 |
| `output/omxsb_audit_20261031/historical_isin_name_flags.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 15258 |
| `output/omxsb_audit_20261031/holdings_audit_summary.json` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 379 |
| `output/omxsb_audit_20261031/holdings_measurement_audit.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 75594 |
| `output/omxsb_audit_20261031/input_inventory.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 10172 |
| `output/omxsb_audit_20261031/nasdaq_202002.xls` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 1784832 |
| `output/omxsb_audit_20261031/nasdaq_202002_instrument_sample.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 100619 |
| `output/omxsb_audit_20261031/original/exports/check_2013_2026_vs_original.csv` | frozen original; audit_omxsb_run.py / preserved commit | 6814 |
| `output/omxsb_audit_20261031/original/exports/coverage_failures.csv` | frozen original; audit_omxsb_run.py / preserved commit | 1822 |
| `output/omxsb_audit_20261031/original/exports/events_car.csv` | frozen original; audit_omxsb_run.py / preserved commit | 442284 |
| `output/omxsb_audit_20261031/original/exports/figures/fig_01_nettrading.csv` | frozen original; audit_omxsb_run.py / preserved commit | 257 |
| `output/omxsb_audit_20261031/original/exports/figures/fig_02_by_year.csv` | frozen original; audit_omxsb_run.py / preserved commit | 1868 |
| `output/omxsb_audit_20261031/original/exports/figures/fig_03_scatter.csv` | frozen original; audit_omxsb_run.py / preserved commit | 250 |
| `output/omxsb_audit_20261031/original/exports/figures/fig_08_car_announcement.csv` | frozen original; audit_omxsb_run.py / preserved commit | 17265 |
| `output/omxsb_audit_20261031/original/exports/figures/fig_09_car_effective.csv` | frozen original; audit_omxsb_run.py / preserved commit | 16167 |
| `output/omxsb_audit_20261031/original/exports/figures/fig_10_size_rank.csv` | frozen original; audit_omxsb_run.py / preserved commit | 1239 |
| `output/omxsb_audit_20261031/original/exports/figures/fig_11_volume.csv` | frozen original; audit_omxsb_run.py / preserved commit | 7018 |
| `output/omxsb_audit_20261031/original/exports/holdings_price_check.csv` | frozen original; audit_omxsb_run.py / preserved commit | 48310 |
| `output/omxsb_audit_20261031/original/exports/index_funds.csv` | frozen original; audit_omxsb_run.py / preserved commit | 3616 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/e1_table3_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 9929 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/e1_table3_size_top100.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2320 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/e2_spread_by_year.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2613 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/e3_omxsb_additions_in_omxs30_list.csv` | frozen original; audit_omxsb_run.py / preserved commit | 4723 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/e3_omxsb_events_vs_omxs30_membership.csv` | frozen original; audit_omxsb_run.py / preserved commit | 3845 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/e4c_rank_of_additions.csv` | frozen original; audit_omxsb_run.py / preserved commit | 33571 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/e5b_table4_medians_by_year.csv` | frozen original; audit_omxsb_run.py / preserved commit | 3013 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/events_mechanisms.csv` | frozen original; audit_omxsb_run.py / preserved commit | 126729 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/fig_d_expected_demand_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2290 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/fig_d_fig3_nettrading.csv` | frozen original; audit_omxsb_run.py / preserved commit | 19065 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/fig_e4a_car_announcement.csv` | frozen original; audit_omxsb_run.py / preserved commit | 34218 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/fig_e4b_car_effective.csv` | frozen original; audit_omxsb_run.py / preserved commit | 32127 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/fig_e4c_rank.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2225 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/fig_e5a_volume.csv` | frozen original; audit_omxsb_run.py / preserved commit | 13971 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/membership_coverage_by_review.csv` | frozen original; audit_omxsb_run.py / preserved commit | 3983 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/membership_inconsistencies.csv` | frozen original; audit_omxsb_run.py / preserved commit | 275 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/membership_missing_mcap_by_review.csv` | frozen original; audit_omxsb_run.py / preserved commit | 5775 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/numbers_mechanisms.json` | frozen original; audit_omxsb_run.py / preserved commit | 22952 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/omxsb_membership_by_review.csv` | frozen original; audit_omxsb_run.py / preserved commit | 36674 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/results_table_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 55749 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/step1_deletion_flags.csv` | frozen original; audit_omxsb_run.py / preserved commit | 34975 |
| `output/omxsb_audit_20261031/original/exports/mechanisms/tracker_aum_daily_interpolated.csv` | frozen original; audit_omxsb_run.py / preserved commit | 123001 |
| `output/omxsb_audit_20261031/original/exports/nettrading_omxsb.csv` | frozen original; audit_omxsb_run.py / preserved commit | 75897 |
| `output/omxsb_audit_20261031/original/exports/numbers.json` | frozen original; audit_omxsb_run.py / preserved commit | 961 |
| `output/omxsb_audit_20261031/original/exports/period_sensitivity/regimes.csv` | frozen original; audit_omxsb_run.py / preserved commit | 6210 |
| `output/omxsb_audit_20261031/original/exports/period_sensitivity/table2_by_period_length_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 38423 |
| `output/omxsb_audit_20261031/original/exports/period_sensitivity/tables_by_length.xlsx` | frozen original; audit_omxsb_run.py / preserved commit | 44777 |
| `output/omxsb_audit_20261031/original/exports/period_sensitivity/trend_by_period_length.csv` | frozen original; audit_omxsb_run.py / preserved commit | 3801 |
| `output/omxsb_audit_20261031/original/exports/period_sensitivity/trend_tests.csv` | frozen original; audit_omxsb_run.py / preserved commit | 19508 |
| `output/omxsb_audit_20261031/original/exports/table2_phase1_vs_gs.csv` | frozen original; audit_omxsb_run.py / preserved commit | 3638 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_01_car_omxsgi_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 4511 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_02_isin_matches.csv` | frozen original; audit_omxsb_run.py / preserved commit | 11708 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_02_isin_matches_check.csv` | frozen original; audit_omxsb_run.py / preserved commit | 15258 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_03_index_funds.csv` | frozen original; audit_omxsb_run.py / preserved commit | 963 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_04_split_factors.csv` | frozen original; audit_omxsb_run.py / preserved commit | 431 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_05_dropped_events.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2029 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_06_event_chain.csv` | frozen original; audit_omxsb_run.py / preserved commit | 319 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_07_car_robustness.csv` | frozen original; audit_omxsb_run.py / preserved commit | 4625 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_07_car_robustness_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 14901 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_08_sample_sensitivity.csv` | frozen original; audit_omxsb_run.py / preserved commit | 1172 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_08_sample_sensitivity_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 1591 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_09_sample_selection.csv` | frozen original; audit_omxsb_run.py / preserved commit | 472 |
| `output/omxsb_audit_20261031/original/exports/tables/tabA_10_deletions_clean_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 3566 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_00_by_year.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2765 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_01_sample.csv` | frozen original; audit_omxsb_run.py / preserved commit | 311 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_02_car.csv` | frozen original; audit_omxsb_run.py / preserved commit | 1598 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_02_car_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 4861 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_02_car_long_oldperiods.csv` | frozen original; audit_omxsb_run.py / preserved commit | 4433 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_02_car_long_phase1.csv` | frozen original; audit_omxsb_run.py / preserved commit | 4430 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_02b_trend_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 753 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_02c_ftest_old_vs_new.csv` | frozen original; audit_omxsb_run.py / preserved commit | 961 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_03_determinants_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2608 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_04_institutions.csv` | frozen original; audit_omxsb_run.py / preserved commit | 902 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_05_elasticity.csv` | frozen original; audit_omxsb_run.py / preserved commit | 1557 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_05_elasticity_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 2783 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_06_volume_share.csv` | frozen original; audit_omxsb_run.py / preserved commit | 498 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_07_spread.csv` | frozen original; audit_omxsb_run.py / preserved commit | 391 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_08_preannouncement.csv` | frozen original; audit_omxsb_run.py / preserved commit | 5401 |
| `output/omxsb_audit_20261031/original/exports/tables/tab_08_preannouncement_long.csv` | frozen original; audit_omxsb_run.py / preserved commit | 5434 |
| `output/omxsb_audit_20261031/original_sha256.json` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 21652 |
| `output/omxsb_audit_20261031/ownership_common_sample.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 882 |
| `output/omxsb_audit_20261031/panel_coverage_by_year.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 1183 |
| `output/omxsb_audit_20261031/possible_fund_id_transfers.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 3795 |
| `output/omxsb_audit_20261031/result_summary.json` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 462 |
| `output/omxsb_audit_20261031/result_table.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 39741 |
| `output/omxsb_audit_20261031/sample_by_event.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 32265 |
| `output/omxsb_audit_20261031/shareclass_denominator_diagnostics.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 175 |
| `output/omxsb_audit_20261031/split_denominator_checks.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 51423 |
| `output/omxsb_audit_20261031/split_source_verification.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 643 |
| `output/omxsb_audit_20261031/starting_git.json` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 304 |
| `output/omxsb_audit_20261031/tracker_quarter_metadata.csv` | audit support/report; code/build/audit_omxsb_*.py; external XLS/source-verification exceptions documented in KORNING.md | 95698 |
<!-- END_OMXSB_AUDIT_20261031 -->

<!-- OMXSB_EXTENSION_20261031 -->

## OMXSB extension execution, 31 October 2026

Local analysis only. Original sources and earlier numerical exports preserved. No FTN returns. Full file hashes: `output/omxsb_extension_20261031/artifact_manifest.json`.

| Location | Provenance / purpose |
|---|---|
| `output/omxsb_extension_20261031/ownership/` | New AP2/AP3/AP4 and FI half-year ownership analysis; source/exclusion ledgers and report; code/build/omxsb_ap_prepare.py and omxsb_ap_ownership.py |
| `output/omxsb_extension_20261031/candidate/` | Nasdaq October2019/2024 original files and notices; two-review data pilot; source_manifest.json and source_reading_notes.json; code/build/omxsb_candidate_pilot.py |
| `output/omxsb_extension_20261031/migration/` | Saved cached primary Solactive extracts plus original FI XML; bounded transition screen; source_register.csv; code/build/omxsb_migration_screen.py |
| `output/omxsb_extension_20261031/labels/` | Eight corrected labels; original numerical results unchanged; code/build/omxsb_relabel_results.py |
| `data/raw/omxsb_extension_20261031/support/` | Four official original PDFs and layout text extracts: government AP2019/2024, Nordnet2022, contemporaneous ENF2019 mandate statement; source_ledger.json |
| `output/omxsb_extension_20261031/independent_validation.json` | Independent numerical/accounting checks; code/build/omxsb_extension_validate.py |

<!-- END_OMXSB_EXTENSION_20261031 -->

<!-- OMXSB_ROBUSTHET_REPAIR_20261101 -->
## OMXSB control-analysis repair, 1 November 2026

Post-result code/method repair. Original exports archived, raw sources unchanged. Source hashes in output/omxsb_robusthet_20261101/input_sha256.json; artifact hashes in artifact_manifest.json. No FTN return calculations.

| File | Provenance/status |
|---|---|
| `output/omxsb_robusthet_20261101/KORNING.md` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/RESULTAT.md` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/T2_matches.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/T5_analysis_samples.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/T5_proxy_preselected.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/artifact_manifest.json` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/covariate_balance.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/event_coverage.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/first_stage_validation/first_stage_validation.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/first_stage_validation/first_stage_validation.json` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/input_sha256.json` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/membership_quality.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/requirements.lock` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/results.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/run_metadata.json` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/unresolved_event_identifiers.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/validation.json` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `output/omxsb_robusthet_20261101/window_clock.csv` | Repaired control analysis / validation; code/build/robusthet_hela.py and companion validation scripts. Blocked outputs are not economic estimates. |
| `robusthet_hela_resultat.zip` | Current code, specification, results, provenance and tests; supersedes archived original ZIP. |
<!-- END_OMXSB_ROBUSTHET_REPAIR_20261101 -->

<!-- OMXSB_OPEN_QUESTIONS_20261102 -->
## OMXSB follow-up data, 1–2 November2026

New local reproducibility bundle: `output/omxsb_open_questions_20261102/`. Dated Nasdaq sources, source URLs, publication timestamps, retrieval hashes and complete file manifest are stored inside the bundle.19 workbook/notice pairs cover April/October2017–2025 and April2026. These establish a retrospective Main Market Stock screen, not full OMXSB eligibility or availability for prediction. Strict exact-ISIN/reviewed-alias pool:5765 review×RIC rows; unresolved identities are retained separately. New quarterly FI decomposition:216 locked events,132621 valid fund/event pairs; observed changes are not actual gross transactions. Original data untouched. See `RESULTAT.txt`, `ANALYSIS_LEDGER.txt` and `MANIFEST_SHA256.json` for results, limitations, all variants and provenance.


<!-- OMXSB_MECHANISM_FRONTIER_20261102 -->
## OMXSB ownership/mandate follow-up, 2 November 2026

New local bundle `output/omxsb_mechanism_frontier_20261102/`: exploratory owner-count decomposition on219 fixed matched event sets (118additions,101deletions),14reviews2019–25;446048fund/event/security-role rows with balanced full reports, stable fundISIN/benchmark and explicit ambiguity/collision exclusions. H-group, benchmark-group counts, management-company counts and joint Fieller ratios separately validated. Broader13-candidate quantity ledger has205price-overlap events and incomplete historical mandate/target-weight evidence; not all-market mechanical demand. Source URLs, read scopes, declarations, failed data gates, previous versions, source/file hashes and numerical replay validation are included. No new price regressions or FTN returns.


<!-- OMXSB_MEASUREMENT_FOLLOWUP_20261102 -->
## OMXSB measurement and ownership follow-up, 2 November 2026

Eight additive, exploratory analysis modules; original data and prior results preserved. Code is in `code/build/omxsb_followup_20261102/`. Frozen gates, previous versions, exact source URLs/read scopes, failures and complete SHA256 manifest are included. Replay validates numeric outputs without reopening selection rules. Downloaded primary reports are unchanged; subset continuity assumptions remain explicit. See `output/omxsb_followup_20261102/START_HERE.txt` and `RESULTAT.txt`.

| New file | Role / provenance |
|---|---|
| `output/omxsb_followup_20261102/INPUT_SHA256.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/PORTABILITY_LOG.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/ARCHIVE_SHA256.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/ENVIRONMENT.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/EXISTING_ARCHIVE_CHECK.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/INPUT_SHA256.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/LOCK_SHA256.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/PACKAGE_BUILD.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/PATH_ONLY_CHANGES.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/SECONDARY_PATH_EQUIVALENCE.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/replay_comparison.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/additions_20261102/replay_execution.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/comparison_rebuild_20261102/US_reference.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/comparison_rebuild_20261102/hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/comparison_rebuild_20261102/independent_audit.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/comparison_rebuild_20261102/ratios.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/comparison_rebuild_20261102/same_sample_events.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/ANALYSIS_LOCK.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/analysis_event_ledger.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/analysis_event_ledger_all_frozen_rows.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/exposure_residuals_NO_OUTCOMES.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/exposure_review_variation.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/gate_event_ledger.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/gate_summary.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/pre_covariate_correlations.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/primary_size_preCAR_official_liquidity_all_coefficients.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/quarter_liquidation_review_description.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/quarter_liquidation_summary.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/raw_position_reconciliation.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/raw_position_validation.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/results.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/review_exposure_information_share.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/sensitivity_reviewFE_only_all_coefficients.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/source_hashes_gate.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/source_ledger.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/deletion_exposure_20261102/validation.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/figures/OMXSB_tva_agarresultat_20261102.pdf` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_catalog_20261102/Access_Sverige_FI2019_2025_metadata.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_catalog_20261102/Access_Sverige_PPM2016_identity_raw.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_catalog_20261102/Access_Sverige_PPM2018_identity_raw.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_catalog_20261102/Access_Sverige_recommended_classification.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_catalog_20261102/Fondkatalog2016.pdf` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_catalog_20261102/source.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/LF_2018.pdf` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/LF_2019.pdf` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/PPM2018_identity.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/classified_fund_event_panel.csv.gz` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/event_demand_updated.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/fixed_definition_ratios.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/independent_audit.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/quantity_summary.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/source_manifest.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/mandate_upgrade_20261102/upgraded_fund_review_evidence.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/owner_concentration_stability_20261102/all_omissions.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/owner_concentration_stability_20261102/company_additive_contributions.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/owner_concentration_stability_20261102/descriptive_ranges.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/owner_concentration_stability_20261102/event_company_contributions.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/owner_concentration_stability_20261102/hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/owner_concentration_stability_20261102/independent_audit.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/owner_concentration_stability_20261102/review_contributions.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/path_only_code_changes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/replay_comparison.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/replay_execution.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/before_BTA_correction_unit_gate_initial.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/endpoint_source_gate.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/existing_price_join.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/final_file_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/fund_flow_field_check.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/gate_frozen_summary.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/independent_quantity_validation.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/input_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/joint_existing_price_description.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/membership_evidence.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/position_quantities.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/previous_stale_share_snapshots.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/quantity_gate_frozen.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/quantity_run_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/quantity_summary.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/source_ledger.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/two_verified_class_denominator_cases.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_followup_20261102/unit_gate_initial.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/baseline_candidate_ledger.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/baseline_coverage.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/baseline_selection_audit.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/core_FI_evidence.csv.gz` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/core_freeze_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/core_frozen.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/core_gate_frozen.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/core_gate_summary.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/core_ratios_all.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/endpoint_evidence.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/file_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/fund_review_factors.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/gate_freeze_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/independent_validation.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/input_source_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/outcome_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/relative_retention_all.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/retention_scaling_feasibility_20261102/relative_retention_summary.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/diagnostic_slopes.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/gate_and_volume.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/independent_audit.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/independent_shared_scale_diagnostic.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/independent_window_and_unit_checks.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/joined_all.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/unit_venue_audit/canonical216_RIC_source_provenance.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/unit_venue_audit/monthly_comparison.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/unit_venue_audit/original_workbook_notes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/unit_venue_audit/validation.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_measurement_20261102/volume_quantity_ratios.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/ANALYSIS_RUN.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/INDEPENDENT_NUMERIC_VALIDATION.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/PORTABILITY_LOG.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/PORTABLE_CODE_SHA256.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/PORTABLE_INPUT_MANIFEST.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/PORTABLE_REPLAY_VALIDATION.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/UNIT_GATE_LOCK.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/all_available_exactISIN_month_anchors.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/anchor_event_bridge_diagnostics.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/coverage_by_review_direction.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/diagnostic_slopes.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/exclusions_by_reason.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/independent_audit.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/inputs/event_demand_updated.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/joined_quantities_volume_all216.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/primary_CA_evidence.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/review_level_means.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/unit_gate_all216.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/unit_measurement_all216.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/volume_input_all216.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/volume_quantity_ratios.csv` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/volume_units_full_20261102/workbook_columns_and_hashes.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |
| `output/omxsb_followup_20261102/winner_structures_20261102/reading_ledger.json` | Audited follow-up artifact; source, estimand, coverage, limitations and code identified in its module report/README and SHA256 manifest. |

Archived original duplicates and code snapshots are listed individually in module ARCHIVE_SHA256 manifests; they are preserved provenance, not additional independent data.


<!-- OMXSB_BROADENING_20261102 -->

## OMXSB bounded additional analyses, 2 November 2026

Public FI snapshots were downloaded together from https://www.fi.se/sv/vara-register/blankningsregistret/. Exact source/download timestamps, actions and raw hashes are in output/omxsb_broadening_20261102/short_positions/download_log.csv, current_download.json and complete_sources.json. The 31 October source is preserved.

| Artifact | Source / limitations |
|---|---|
| `data/raw/fi_short/AktuellaPositioner_2026-11-02.ods` | Official FI export; 599093 bytes; SHA256 `0423857cd62af91caae83595615938f2ca962d259f0765b659342e90dc6bed1f`. Original file added unchanged. |
| `data/raw/fi_short/HistoriskaPositioner_2026-11-02.ods` | Official FI export; 1736665 bytes; SHA256 `0f42d256a02cd985243c6dc30d7d46a29b40e4db76e94050f815b2538796b597`. Original file added unchanged. |
| `output/omxsb_broadening_20261102/switchers/` | Fixed existing matches, same-RIC/ review comparison; no new raw returns, no rematching. Exploratory directional association, not identified causality. All saved files listed and hashed in `PACKAGE_SHA256.json`; module reports and code record transformations. |
| `output/omxsb_broadening_20261102/models/` | Frozen quantity/volume gate and existing matched CAR; three fixed functional-proxy models, common sample, held-out reviews. Realized quarterly positions are endogenous; no structural metaorder interpretation. All saved files listed and hashed in `PACKAGE_SHA256.json`; module reports and code record transformations. |
| `output/omxsb_broadening_20261102/short_positions/` | Paired public FI source snapshots, identities, archived gate versions and final47 holder-event/28 issuer-event cohort. Positive part of net short exposure, censoring bounds; no price outcome, no representative whole-market claim. All saved files listed and hashed in `PACKAGE_SHA256.json`; module reports and code record transformations. |
| `output/omxsb_broadening_20261102/frontier/` | Baseline-only positive-holding network coverage from existing FI/Nasdaq inputs; no return outcomes. Financing and incumbent designs remain data-gated. All saved files listed and hashed in `PACKAGE_SHA256.json`; module reports and code record transformations. |

Code and original provenance snapshots are preserved separately from executed numerical outputs. Package checks do not mean all economic mechanisms have been identified, all literature exhausted, or results preregistered blindly.


<!-- OMXSB_ATTENTION_COVERAGE_20261102 -->
### Public attention coverage probe, 2 November 2026

Technical-only fixed January2019 Wikimedia pageview probe for six purposive company names, preserved in `output/omxsb_attention_dd_20261102/public_data_probe/`. Source URLs, access status, hashes and pre-probe specification are included. Four current pages yielded31 daily user-pageview rows; two current pages returned404 and require historical-title research. Missing is not zero. This is not population coverage or an event-effect estimate. Google Trends first browser attempt returned429; no series received. Current SSE catalogue reports Factiva discontinued2021 and an on-campus Nexis Uni trial19Oct–19Nov2026; no archive entitlement/export validated. Raw licensed inputs unchanged.
