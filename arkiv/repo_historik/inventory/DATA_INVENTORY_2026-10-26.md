# Data and data-pull inventory, ~/dev/financethesis (26 Oct 2026)

Read-only inventory of every thesis dataset and every piece of LSEG/Refinitiv data-pulling code on this machine. Written so that a second analyst can plan (a) a new LSEG CodeBook pull that extends the stock panel back to 2005 and (b) the FTN extension, without opening the files. Nothing was modified, moved or created except this file. Machine: macOS, Python 3.12 (anaconda), pandas 2.2.3, pyarrow, openpyxl, xlrd 2.0.2, `maketables` 0.2.0 installed.

Sections 1 to 7 answer the seven questions in the brief. Appendix A prints the four LSEG pull scripts verbatim. Appendix B is the machine-generated profile of every tabular file (rows, dtypes, date ranges, id uniques, first 3 rows). Appendix C is the raw directory tree with sizes.

---

## 0. Executive summary for the planner

**Stock panel actually on disk (used by the OMXSB replication notebook).** `data/senastedata/stocks_daily.csv.gz`: 3,206,212 daily rows for 1,667 RICs, columns `ric, date, close, totret, volume, mcap, shares, turnover, source`, produced by `lseg_pull_v4` in LSEG Workspace CodeBook on 14-15 Oct 2026 with `START = "2012-01-01"` and `END = today` (last date 2026-10-14). It is a 2012-2026 panel: only 72 stray rows (one row each for 72 RICs, 69 of them dated 2011) fall before 2012. 646 of the 1,667 RICs are delisted (`^` suffix). 2.35 million rows are `.ST`; the rest are `.OL` (374k), `.HE` (271k), `.CO` (209k): Nordic home-exchange shares from the losers' holdings ISIN list (tier 1 of `isin_list_lseg_v2.csv`). 1,619 RICs came from the `TR.*` field request and 48 from the pricing-endpoint fallback (`source = "pricing"`). Companion files: `stocks_static.csv` (1,667 rows: `ric, first_date, last_date, n_days, DTSubjectName, IssueISIN, RetireDate, ExchangeCode`; 412 RICs have no Search metadata, presumably because they entered the download list through the ISIN resolution or the OMXSB map rather than the universe search), `indices_daily.csv` (6 indices, 2012-01-02 to 2026-10-14: .OMXS30, .OMXS30GI, .OMXSBCAPGI, .OMXSBGI, .OMXSGI, .OMXSPI; .SIXRX and .SIXPRX are absent, so they failed in CELL 6), `omxsb_events_with_ric.csv` (394 events with RIC and `days_with_price` 10 to 24, i.e. every event has prices in its window), `td_failures.csv` (48 rows, 34 unique RICs, all chain RICs `0#...`, `IPO-...` placeholders and one `STRANSNOK.ST^G14`).

**Datastream export (15 Oct 2026), still zipped.** `data/senastedata/LSEG DATOR-20261025T183134Z-1-001.zip` holds `LSEG DATOR/Codes.csv, P.csv, RI.csv, VO.csv` (111 MB unzipped). P, RI and VO are wide: 5,684 daily rows from 2004-12-31 to 2026-10-14, 1,467 series columns, 30 of them `#ERROR`, 1,437 with at least one value, 420 series named `... DEAD - DELIST.dd/mm/yy`. `Codes.csv` is the request list in column order: 1,467 rows, column 0 = the Datastream request code (1,104 ISINs, of which 1,051 Swedish; 363 RICs in angle brackets: 149 `.OL`, 100 `.HE`, 70 `.CO`, 44 `.ST`), columns 1 and 2 empty except six rows that repeat the request list in chunks. Column i of P/RI/VO is the code in row i of Codes.csv (verified: row 0 `SE0013358710` = `24STORAGE DEAD - DELIST.10/01/22`, row 9 `<ABB.ST>` = `ABB LTD N (OME)`). 1,104 of the 1,247 ISINs in `stocks_static.csv` and 362 of the bracketed RICs appear in the LSEG panel, so the two sources overlap almost completely. This zip is the only Datastream copy in the repo; `thesis2/data/prices/raw/` (where `thesis2/data/prices/README.md` says the files sit) does not exist. A second, byte-identical-content copy of the four files is `~/Downloads/drive-download-20261026T101706Z-1-001.zip` (flat, no `LSEG DATOR/` folder). No MV, NOSH, VA, UP, AF, PI or factor files exist anywhere on the machine.

**What is not on this machine.** (1) The executed CodeBook notebook with its printed output. Only the source of `lseg_pull_v3` and `lseg_pull_v4` exists (`thesis2/code/codebook/*.py` and `*.ipynb`, cells have no outputs; identical copies in `~/Desktop/KOD TILL THESIS/`). (2) The CodeBook intermediate files `td_cfg.csv, td_universe.csv, td_isin_resolved.csv, td_omxsb_map.csv, td_rics_final.csv, td_done.csv, td_daily_NNN.csv, td_pricing_NNN.csv`: none exists locally; only the six download files listed in CELL 8 were brought down (and `td_omxsb_map.csv` and `td_universe.csv` were not). (3) The raw Morningstar/SHoF daily files `data/Valuations/*.csv` and `data/Reinvestments/*.csv` (755 MB and 3.6 GB per `thesis2/03_DATA.md`): absent; only their derived monthly aggregates and the 78 losers' daily extract survive. (4) FI quarter 2026Q3 (not yet published). (5) `thesis2/data/prices/*.csv`, `factors_daily.csv`, `round_dates.csv`, `tracker_aum.csv`, `fund_nav_daily.csv`, `fund_benchmark_daily.csv`, `dose_stock_tranche.csv` that the thesis2 scripts expect: none exists.

**Request lists for a new pull.** `thesis2/data/lseg_input.csv` (2,901 rows: 152 guessed RICs for OMXSB companies with `group = omxsb`, 2,749 ISINs from the losers' holdings), `thesis2/code/codebook/isin_list_lseg_v2.csv` (7,395 ISINs: `isin, name, country, source, tier`; tier 1 = 4,460 Nordic, tier 2 = 2,935 other; source `old_list` 3,788 / `fi_loser_holdings` 3,607), `thesis2/data/isin_list_lseg.csv` (4,452 rows, `isin, name`, older version), `thesis2/code/codebook/omxsb_changes_2013_2026.csv` (394 events, identical to `thesis2/data/omxsb/omxsb_changes_2013_2026.csv`).

**FI holdings.** 31 quarterly zips 2018Q4 to 2026Q2 in `data/senastedata/` (FI's VPFO XML, one file per fund), plus 4 older-timestamp zips in `data/extra/` (2023Q4, 2024Q1, 2024Q2, 2026Q2). Parsed long file `data/senastedata/output/fi_holdings_long.csv.gz`: 3,064,860 rows, 17 columns, 886 funds, 31 quarters, 45,709 unique instrument ISINs.

**FTN/PPM.** Everything listed in section 6 exists: `exit_days_by_loser.csv` (78 losers), `bids_long.csv` (290 bids, 11 rounds, two identical copies), swing status for 78 losers and 60 funds of the 2019 purge, winner/loser round membership (131 fund-round rows), monthly PPM fund panels 2018-2026 (1,019 fondnr) and 2022-2026, winners' monthly fee series, daily TNA/flows for the 78 losers only, Pensionsmyndigheten monthly statistics workbooks 2001-2026 (308 files) and a 2024 daily NAV workbook, the FTN procurement reports (11 PDFs), the SHoF fund master (80,258 share classes) and fee table (347,401 rows).

---

## 1. Directory tree

Top level of the repo (sizes in bytes; directories show their inode size). The full `find . -maxdepth 4` listing with sizes is Appendix C. Folders holding data or code:

| folder | what it holds |
|---|---|
| `data/senastedata/` | the 25 Oct 2026 drop: LSEG CodeBook outputs, Datastream zip, 31 FI zips, the analysis notebook `code.ipynb` (1.1 MB, 51 cells, executed) and its `output/` (tables, figures, parsed FI holdings) |
| `data/senastedata/output/` | `fi_holdings_long.csv.gz`, `events_car.csv`, `nettrading_omxsb.csv`, `holdings_price_check.csv`, `index_funds.csv`, `numbers.json`, `exhibits_manifest.md`, `tables/` (tab_01..tab_06, tabA_01..tabA_06 as tex/docx/csv), `figures/` (fig_01, 03, 08, 09, 10, 11 as pdf/png/csv) |
| `data/raw/` | Pensionsmyndigheten monthly premium-pension statistics workbooks, 2001-01 to 2026-08, in `2001-2008/`, `2009-2014/`, `2015-2020/`, `2021-2026/` by year (xls to 2011-09, xlsm after); 308 files, git-tracked |
| `data/panel/` | `ppm_panel_2018_2026.csv` and its builder `build_ppm_2018.py` |
| `data/derived/ftn_2026-10-11/` | FTN round tables built 11 Oct 2026: `bids_long.csv`, `crosswalk_ppm_shof.csv`, `ftn_category_fees.csv`, `panel_nonppm_monthly.csv`, `ppm_panel_2022_2026.csv` (+ `build_ppm.py`), `reallocation_losers.csv`, `reallocation_summary_by_round.csv`, `unmatched_for_lseg.csv`, `winners_fee_series.csv` |
| `data/derived/shof_monthly/` | `shof_valuations_monthly.csv` (46 MB), `shof_rips_monthly.csv` (19 MB), `monthly.py`, `monthly.log` |
| `data/measurements/` | agent outputs from Oct 2026: `agentA_*` (round membership, loser decomposition, monthly flows), `agent2019_*` (2019 purge), `fip_*` (FI net-demand by company), `bids_long.csv`, `winners_fee_series.csv`, `fund_fi_mapping.csv`, `execution_windows_monthly.csv`, scripts `agentA_build.py`, `agent2019_build2019.py`, `analyze.py`, `fip.py`, `fip_allnames.py`, `parse_fi.py` |
| `data/facts/` | `fact1..fact5` CSVs and scripts (appeal, gender, share class, savings, concentration) |
| `data/extra/` | `fi_2023q4.zip, fi_2024q1.zip, fi_2024q2.zip, fi_2026q2.zip`, `ppm_2023_12.xlsm, ppm_2024_03.xlsm, ppm_2024_06.xlsm, ppm_2026_06.xlsm, ppm_2026_08.xlsm` (copies of monthly statistics), `ppm_nav_2024.xlsx` (daily NAV 2024), `shof_fundmaster.zip` (= `fundmaster.xlsx`), `shof_field_definitions.pdf/.txt`, `ftn_europe_active_2024.pdf/.txt` |
| `data/FTN/` | 11 FTN procurement report PDFs (upphandlingsrapporter) |
| `data/` root | `FEES.txt` (27 MB SHoF fee table), `fundmaster.xlsx` (22 MB SHoF fund master), `Lista alla fonder 2026.xls` (PPM fund list 2026-07-17) |
| `data/winners/`, `data/agent_reports/` | thesis-prize winners table and two agent reports (not fund data) |
| `thesis2/code/` | analysis scripts (`eventstudy.py`, `replication_omxsb.py`, `pressure.py`, `ftn_eventstudy.py`, `dilution.py`, `power.py`, `parse_fi.py`), the two early LSEG pull scripts, and `codebook/` with `lseg_pull_v3/v4` (.py and .ipynb), `isin_list_lseg.csv`, `isin_list_lseg_v2.csv`, `omxsb_changes_2013_2026.csv` |
| `thesis2/data/` | `exit_days/` (`exit_days_by_loser.csv`, `losers_daily_valuations.csv`, `detect_exit_days.py`), `omxsb/` (change lists, builders, notes), `swing/` (status files, builder, notes), `prices/` (README only), `lseg_input.csv`, `isin_list_lseg.csv` |
| `thesis2/output/tables/` | `NOTES.md` only (empty template) |
| `code.ipynb` (repo root) | 602-byte empty stub (one markdown header, one empty code cell), not the analysis notebook |
| `tmp/` | PDFs/images of anchor papers and lecture slides; no data |
| `research/`, `old_winners/`, `non_winners/`, `course_context/`, `synopsis/`, `thesis2/*.md` | text, PDFs, notes; no data pulls |

Git status: `data/senastedata/` is untracked (not in git; it is not in `.gitignore` either). `.gitignore` excludes `Reinvestments/`, `Valuations/`, `data/FUNDS_*.csv`, `thesis2/data/prices/raw/`, `thesis2/data/prices/*.csv`. 403 files under `data/` and 33 under `thesis2/data` + `thesis2/code` are tracked.

Copies outside the repo (found by searching `~`): `~/Downloads/stocks_daily.csv.gz`, `stocks_daily.csv (1).gz`, `(2).gz`, `stocks_static.csv`, `indices_daily.csv`, `td_failures.csv`, `omxsb_events_with_ric.csv`, `fundmaster.xlsx`, `fundmaster.zip` (all md5-identical to the repo copies), `~/Downloads/drive-download-20261026T101706Z-1-001.zip` (Datastream P/RI/VO/Codes, flat), `~/Downloads/Statistik-Premiepension-2026-01-31.xlsm`, `~/Desktop/KOD TILL THESIS/` (`lseg_pull_v3.ipynb`, `lseg_pull_v4.ipynb`, `isin_list_lseg_v2.csv`, `omxsb_changes_2013_2026.csv`, identical to repo), `~/dev/avanza-analyst/data/raw/fi/2026Q2/Fondinnehav_2026Q2_2026-08-20_11.07.zip` (another project). No `Valuations/`, `Reinvestments/`, `thesis_data/`, `financethesis_ny/` or `financethesis_fresh/` folder exists anywhere under `~`.

---

## 2. Data files: what each one is

Full per-file profile (rows, every column with dtype, date ranges, id uniques, first 3 rows) is in Appendix B. This section gives the facts a planner needs.

### 2.1 LSEG CodeBook outputs (`data/senastedata/`)

| file | size | rows | columns | notes |
|---|---|---|---|---|
| `stocks_daily.csv.gz` | 76.0 MB | 3,206,212 | `ric, date, close, totret, volume, mcap, shares, turnover, source` | 1,667 RICs; date 1991-11-01 (one stray row) to 2026-10-14; effectively 2012-01-02 onward (135,745 rows in 2012 rising to 281,128 in 2022; 197,377 in 2026 to 14 Oct). Non-null shares: close 99.7 %, totret 97.5 %, volume 99.0 %, mcap 96.3 %, shares 94.3 %, turnover 74.8 %. 1,606 RICs have some totret, 1,547 mcap, 1,546 shares, 1,134 turnover. `source`: tr 3,128,160 rows / 1,619 RICs; pricing 78,052 rows / 48 RICs. Suffix rows: ST 2,351,773; OL 374,059; HE 271,155; CO 209,221; STp 4. `totret` is daily total return in per cent; `close` is split-adjusted (see holdings_price_check: FI prices differ from LSEG close by integer split factors for 3 events). |
| `stocks_static.csv` | 118 kB | 1,667 | `ric, first_date, last_date, n_days, DTSubjectName, IssueISIN, RetireDate, ExchangeCode` | first_date 1991-11-01 to 2026-09-30; last_date to 2026-10-14; RetireDate set for 585; 646 RICs carry `^`; ExchangeCode = STO for 1,255, NaN for 412; 1,247 unique IssueISIN. |
| `indices_daily.csv` | 613 kB | 22,311 | `ric, date, close` | 6 indices, each 3,711 to 3,734 rows, 2012-01-02 to 2026-10-14: .OMXS30, .OMXS30GI, .OMXSBCAPGI, .OMXSBGI, .OMXSGI, .OMXSPI. |
| `omxsb_events_with_ric.csv` | 153 kB | 394 | `event_id, effective_date, announcement_date, company, ticker, isin, type, review_cycle, source_url, verification, notes, RIC, days_with_price` | = `omxsb_changes_2013_2026.csv` + RIC from CELL 7; 222 additions, 172 deletions; 27 review cycles 2013H1 to 2026H1; 147 unique RICs, 214 companies; `isin` all NaN; days_with_price 10 to 24 (no event below 10). |
| `td_failures.csv` | 6.8 kB | 48 | `ric, error` | 34 unique RICs; errors are "Unable to resolve all requested identifiers" from TR plus "No data to return" from pricing. |
| `drive-download-20261025T185638Z-1-001.zip` | 76.2 MB | | | the Google Drive bundle these five files came from (`stocks_daily.csv (2).gz`, `stocks_static.csv`, `omxsb_events_with_ric.csv`, `indices_daily.csv`, `td_failures.csv`, all dated 2026-10-15 00:09 to 00:15). |
| `LSEG DATOR-20261025T183134Z-1-001.zip` | 33.5 MB | | | Datastream export, see section 7. |

### 2.2 Analysis outputs (`data/senastedata/output/`)

| file | rows | columns (abridged) | notes |
|---|---|---|---|
| `fi_holdings_long.csv.gz` (106 MB) | 3,064,860 | `Tillgångsslag_enligt_LVF_5_kap, Instrumentnamn, ISIN-kod_instrument, Landkod_Emittent, Valuta, Antal, Kurs_som_använts_vid_värdering_av_instrumentet, Marknadsvärde_instrument, Andel_av_fondförmögenhet_instrument, Kvartalsslut, Fondbolag_namn, Fond_institutnummer, Fond_namn, Fond_ISIN-kod, Fondförmögenhet, Jämförelseindex, zip` | 31 quarters 2018-12-31 to 2026-06-30; 886 funds (Fond_institutnummer), 74 fund companies, 937 fund ISINs, 45,709 instrument ISINs (112,119 rows without ISIN). Asset class rows: ÖverlåtbartVärdepapper 2,811,248; Derivat 134,407; Fondandel 60,743; Penningmarknad 58,462. Latest FI publication per fund-quarter kept (14 duplicate earlier publications dropped). |
| `events_car.csv` | 380 | 54 cols: event fields + `AD, ED, first_date, last_date, IssueISIN, DTSubjectName, period, listed_100, delisted_100, ann, eff, tot, ann_gi, eff_gi, tot_gi, ndays_tot, ym_pre, turn, mcap_pre, size, vol, qb, qa, n_isin, f, shares_qa, idx_b, idx_a, all_b, all_a, act_b, act_a, nt, instbuy, activebuy, indexown, n_idx_funds_b, n_idx_funds_a, isins` | 394 minus 14 dropped by listing/delisting filter; CARs vs .OMXSBGI (`ann, eff, tot`) and vs .OMXSGI (`*_gi`); holdings variables for the 259 events after 2018Q4. |
| `nettrading_omxsb.csv` | 259 | 25 | per-event index-fund and all-fund net trading in % of shares. |
| `holdings_price_check.csv` | 259 | 20 | FI price vs LSEG close before/after, split factor `f`. |
| `index_funds.csv` | 14 | 12 | OMXSB tracker funds identified from trades (5 companies). |
| `tables/*.csv`, `figures/*.csv` | small | | data behind each exhibit; listed in `exhibits_manifest.md`. |
| `numbers.json` | | | 22 headline numbers (CARs by period, elasticities, event counts). |

### 2.3 FI zips: see section 5. 

### 2.4 PPM / FTN / SHoF files: see section 6.

### 2.5 Other data files

| file | rows x cols | notes |
|---|---|---|
| `data/fundmaster.xlsx` (22 MB; same file inside `data/extra/shof_fundmaster.zip`) | 80,258 x 57, sheet `fundmaster` | SHoF Morningstar fund master: `performanceid, secid, fundid, domicileid, company, companyname, fundname, securityname, legalstructure, ..., ISIN, currencyspecificISIN, ticker, ..., indexingapproach, ..., AUM, AUM_lastupdate, 1_month ... 5_year, returntype, lastupdate, availableforsale`. |
| `data/FEES.txt` (27 MB CSV) | 347,401 x 11 | `performanceid, secid, prospectusdate, position, feetypeid, feecurrencyid, feeunit, fee, breakpointunit, lowbreakpoint, highbreakpoint`; 52,461 performanceids; prospectusdate 2002-04-01 to 2026-01-14; feetypeid ManagementFee 51,478, PerformanceFee 51,361, OngoingCharge 48,522, FrontLoadFee 48,004, ActualManagementFee 45,332, RedemptionFee 41,704, ... |
| `data/Lista alla fonder 2026.xls` | 1,932 x 16, sheet `Alla fonder 2026-07-17` | PPM fund register: `FONDBOLAG, FONDNUMMER, UPPHANDLAD, FONDNAMN, NOTERINGS VALUTA, FONDAVGIFT, AVGIFT FÖRE RABATT, KATEGORI, ISIN/EXTERNT ID, FOND_I_FOND, RESULTATBEROENDE, SLOW, FÖRLÄNGD, STARTDATUM, AVSLUTSDATUM, FONDSTATUS`. |
| `thesis2/data/omxsb/omxsb_changes_2013_2026.csv` | 394 x 11 | source event list (built by `omxsb_build.py` from Nasdaq releases; notes in `omxsb_notes.md`). |
| `thesis2/data/omxsb/omxs30_changes_2005_2026.csv` | 48 x 13 | OMXS30 changes, effective 2006-07-03 to 2025-07-01. |
| `data/winners/winners_table.csv` | 25 x 17 | thesis-prize winners (not fund data). |

---

## 3. LSEG / Refinitiv data-pulling code

Search terms `get_history`, `get_data`, `discovery.search`, `open_session`, `lseg.data`, `refinitiv`, `TR.`, `td_` hit exactly six code files, all in `thesis2/code/`; nothing else in the repo (the hits in `non_winners/text/*.txt` are thesis PDFs mentioning Refinitiv). `data/senastedata/code.ipynb` contains no LSEG calls; it reads the downloaded CSVs.

| file | version | START / END | universe | FIELDS | chunking | fallback | outputs |
|---|---|---|---|---|---|---|---|
| `thesis2/code/lseg_codebook_pull.py` | v1 (Oct 2026, never produced data) | `"2005-01-01"` / today | `SCREEN(U(IN(Equity(active,inactive,public,primary))), IN(TR.ExchangeMarketIdCode,"XSTO","FNSE","SSME"), CURN=SEK)` via `ld.get_data` | `TR.PriceClose, TR.TotalReturn, TR.Volume, TR.TurnoverValue, TR.CompanyMarketCap, TR.SharesOutstanding` | `get_history` on batches of 25 RICs, 3 attempts, 10 s sleep, chunk files skipped if present | none | `thesis_data/universe.csv`, `chunks/prices_NNNN.csv`, `stocks_daily.csv`, `stocks_static.csv` (fields `TR.CommonName, TR.ISIN, TR.TickerSymbol, TR.ExchangeMarketIdCode, TR.TRBCEconomicSector, TR.TRBCIndustryGroup, TR.FirstTradeDate, TR.RetireDate, TR.FreeFloatPct`), `index_<name>.csv` for `.OMXS30 .OMXSPI .OMXSB .OMXSBGI .OMXSBCAPGI .SIXPRX .SIX30RX` |
| `thesis2/code/lseg_codebook_pull_v2.py` | v2 | `"2012-01-01"` / today | `lseg_input.csv` (ISIN rows resolved with `get_data` fields `TR.RIC, TR.CommonName, TR.ISIN, TR.InstrumentIsActive, TR.ExchangeMarketIdCode, TR.InstrumentType` in batches of 100; RIC rows checked; misses searched by name with `ld.discovery.search(query=name, top=3, filter="ExchangeCode eq 'STO' and AssetCategory eq 'ORD'", select="RIC,DTSubjectName,IssueISIN,ExchangeName,RetireDate")`); keep `.ST` only | `TR.PriceClose, TR.TotalReturn, TR.Volume, TR.CompanyMarketCap, TR.SharesOutstanding` | one RIC per call, 3 attempts, 0.25 s pause | none | `thesis_data/resolved.csv, omxsb_search_hits.csv, rics.json, daily/<ric>.csv, failures.csv, stocks_static.csv, index_<name>.csv` (`.OMXSPI .SIXRX .OMXSBGI .OMXSB .OMXS30`) |
| `thesis2/code/codebook/lseg_pull_v3.py` / `.ipynb` | v3 (uses `os`, `shutil`, blocked by CodeBook) | `"2012-01-01"` / today; `MAX_CALLS = 9000` | Search `view=EQUITY_QUOTES`, filter `"<base> and RCSAssetCategoryLeaf eq 'Ordinary Share'"` and `'Depository Receipt'`, base tried in order `RCSExchangeCountryLeaf eq 'Sweden'`, `ExchangeCountry eq 'SWE'`, `ExchangeCode eq 'STO'`; inactive clause tried `IsActive eq false` then `AssetState eq 'DC'`; select `RIC,DTSubjectName,IssueISIN,ExchangeCode,ExchangeName,RCSAssetCategoryLeaf,RetireDate,PrimaryRIC,TickerSymbol` (fallback `RIC,DTSubjectName,IssueISIN,ExchangeCode,RetireDate`); top 10,000; keep `\.ST(\^|$)`, drop RetireDate < 2012-01-01. Plus ISIN list (`isin_list_lseg_v2.csv`, tier 1) via `IssueISIN in (...)` in chunks of 50, home-exchange filter ST/CO/HE/OL. Plus OMXSB ticker to RIC map. | tested per field on VOLVb.ST: `TR.PriceClose, TR.TotalReturn, TR.Volume, TR.CompanyMarketCap, TR.SharesOutstanding, TR.Turnover` (+ `TR.TotalReturn1D` if TotalReturn fails) | one RIC per `get_history` call, resumable by file | `get_history(universe=r, start, end, interval="daily")` without fields (pricing endpoint: TRDPRC_1, ACVOL_UNS, TRNOVR_UNS) | `thesis_data/config.json, universe.csv, isin_resolved.csv, omxsb_ric_map.csv, rics_final.json, daily/<ric>.csv, failures.csv, index_<name>.csv, stocks_daily.csv, stocks_static.csv, thesis_data.zip` |
| `thesis2/code/codebook/lseg_pull_v4.py` / `.ipynb` | **v4, the version that produced the data on disk** (CodeBook-safe: pandas + lseg only, flat `td_` files) | `"2012-01-01"` / today; `MAX_CALLS = 9000`, 0.25 s pause | same as v3 | same as v3 (config persisted in `td_cfg.csv` as `FIELDS|...`) | one RIC per call; appended to `td_daily_NNN.csv` / `td_pricing_NNN.csv` with `CHUNK = 250` RICs per file; `td_done.csv` resume list | same pricing fallback; `source` column `tr`/`pricing` | `td_cfg.csv, td_universe.csv, td_isin_resolved.csv, td_omxsb_map.csv, td_rics_final.csv, td_done.csv, td_daily_NNN.csv, td_pricing_NNN.csv, td_failures.csv, indices_daily.csv` (`.OMXSPI .OMXSGI .OMXS30 .OMXS30GI .OMXSB .OMXSBGI .OMXSBCAPGI .SIXRX .SIXPRX`), CELL 7 writes `stocks_daily.csv.gz`, `stocks_static.csv` and prints OMXSB coverage |

The v3 and v4 `.ipynb` files are the `.py` files split at the `# %% CELL n` markers (10 cells each: one markdown header + CELL 0 to CELL 8); the code is identical to the `.py` apart from the module docstring. No cell has outputs, so the printed field test, universe counts, suffix list and coverage list from the real run are **not on this machine**. The `omxsb_events_with_ric.csv` in `senastedata` is the CELL 7 `ev` table with `RIC` and `days_with_price` saved to CSV (the script itself does not save it, so it was exported by hand or by an unsaved cell). The notebook that ran lives in LSEG Workspace CodeBook, not locally.

Appendix A prints all four scripts in full.

---

## 4. `code.ipynb` cell listing

**`~/dev/financethesis/code.ipynb`** (repo root, 602 bytes, kernel `my_clean_env`): 3 cells, no data. Cell 0 markdown `## FINANCE THESIS CODE`; cell 1 empty code cell; cell 2 empty markdown.

**`data/senastedata/code.ipynb`** (1.1 MB, 51 cells, executed in order with outputs, kernel python3). It runs from `os.getcwd()` = `data/senastedata/`, requires `omxsb_events_with_ric.csv, stocks_daily.csv.gz, stocks_static.csv, indices_daily.csv` and exactly 31 `Fondinnehav_*.zip`, and writes to `output/`, `output/tables/`, `output/figures/`. Helper `tab_save` writes `<name>.tex`, `<name>.docx`, `<name>.csv` via `maketables`; `fig_save` writes `<name>.pdf`, `<name>.png`.

| cell | type | first line | reads | writes |
|---|---|---|---|---|
| 0 | md | Setup | | |
| 1 | code | `import os, re, glob, json, zipfile, tempfile, warnings` | lists sizes of the 4 REQ files and 31 zips | creates `output/`, `output/tables`, `output/figures` |
| 2 | code | `ev = pd.read_csv(os.path.join(D, "omxsb_events_with_ric.csv"), ...)` | `omxsb_events_with_ric.csv`, `stocks_static.csv`, `stocks_daily.csv.gz`, `indices_daily.csv` (output: 394 / 1,667 / 3,206,212 / 22,311 rows) | |
| 3 | md | Sample | | |
| 4 | code | `cal = pd.DatetimeIndex(ix.loc[(ix.ric == ".OMXSBGI") ...` | | |
| 5 | code | `drop = ev[ev.listed_100 \| ev.delisted_100]` | | |
| 6 | code | `n0 = ev.groupby(["period", "type"]).size().unstack()` | | `tab_01_sample` (tex/docx/csv) |
| 7 | md | Returns | | |
| 8 | code | `px = px[px.date.isin(cal) & px.ric.str.contains(r"\.ST", ...)]` | | |
| 9 | md | Table 2 | | |
| 10 | code | `def ols(y, X, g):` | | `tab_02_car`, `tab_02_car_long.csv` |
| 11 | code | `rows = []` | | `tabA_01_car_omxsgi_long.csv` |
| 12 | md | Table 3 | | |
| 13 | code | `px["ym"] = px.date.dt.to_period("M")` | | |
| 14 | code | `def reg3(s, ctrl):` | | `tab_03_determinants`, `tab_03_determinants_long.csv` |
| 15 | md | Fund holdings | | |
| 16 | code | `BAD = re.compile(...)` (FI VPFO XML parser: extracts FUND and INS fields, `Jämförelseindex`, publication timestamp from filename) | all 31 `Fondinnehav_*.zip` (extracted to a temp dir) | |
| 17 | code | `h0 = len(h)` (keeps latest publication per fund-quarter) | | `output/fi_holdings_long.csv.gz` |
| 18 | code | `h.groupby("Kvartalsslut").agg(...)` | | |
| 19 | md | Event ISINs | | |
| 20 | code | `STOP = {...}` (ISIN bridging by normalised name) | | `tabA_02_isin_matches` |
| 21 | code | `e5["n_isin"] = e5.isins.map(len)` | | |
| 22 | md | Index funds | | |
| 23 | code | `alli = set().union(*e5.isins)` | | `output/index_funds.csv`, `tabA_03_index_funds` |
| 24 | code | `funds[funds.index_name & ~funds.index_trade]...` | | |
| 25 | code | `pd.crosstab(funds.index_trade, funds.index_name, margins=True)` | | |
| 26 | md | Net trading | | |
| 27 | code | `IDX = set(funds.index[funds.index_trade])` | | `output/holdings_price_check.csv`, `tabA_04_split_factors` |
| 28 | code | `e5 = e5.merge(chk[["event_id", "f"]], ...)` | | |
| 29 | code | `e5[e5.shares_qa.isna()][...]` | | |
| 30 | code | `out = ev.merge(e5[[...]], on="event_id", how="left")` | | `output/events_car.csv`, `output/nettrading_omxsb.csv` |
| 31 | md | Figure 1 | | |
| 32 | code | `f1 = e5.groupby(["year", "type"]).nt.agg(...)` | | `fig_01_nettrading` (pdf/png/csv) |
| 33 | md | Figure 3 | | |
| 34 | code | `fig, axs = plt.subplots(1, 2, ...)` | | `fig_03_scatter` |
| 35 | md | Table 4 | | |
| 36 | code | `t4 = e5.groupby(["type", "year"])[["nt", "instbuy", "activebuy"]].median()` | | `tab_04_institutions` |
| 37 | md | Table 5 | | |
| 38 | code | `def eta_boot(s, B=9999, seed=1):` | | `tab_05_elasticity`, `tab_05_elasticity_long.csv` |
| 39 | md | Figure 8 | | |
| 40 | code | `def cum_paths(A, idx, lo, hi, zero_at=None):` | | `fig_08_car_announcement` (via `car_fig`) |
| 41 | md | Figure 9 | | |
| 42 | code | `f9 = car_fig("iED", -1, 100, 0, "fig_09_car_effective", ...)` | | `fig_09_car_effective` |
| 43 | md | Figure 10 | | |
| 44 | code | `mcm = px.groupby(["ric", "ym"]).mcap.last().reset_index()` | | `fig_10_size_rank` |
| 45 | md | Figure 11 | | |
| 46 | code | `vo = px.pivot(index="date", columns="ric", values="volume").reindex(cal)` | | `fig_11_volume`, `tab_06_volume_share` |
| 47 | md | Checks | | |
| 48 | code | `chain = pd.DataFrame({"Step": [...]})` | | `tabA_06_event_chain` |
| 49 | code | `dr = drop[[...]].copy()` | | `tabA_05_dropped_events` |
| 50 | code | `with open(os.path.join(OUT, "numbers.json"), "w") as f:` | | `output/numbers.json`, `output/exhibits_manifest.md` |

Key recorded outputs: 394 events, 380 after the filter, 259 with holdings data, 253 with net trading; 14 OMXSB index funds; FI parse: 3,090,564 raw rows, 3,064,860 kept, 886 funds, 31 quarters, zero XML parse errors.

---

## 5. FI holdings (Fondinnehav)

`data/senastedata/Fondinnehav_<quarter>_<FI timestamp>.zip`, 31 files, 4.8 to 6.7 MB each, one consecutive quarter each from 2018Q4 to 2026Q2 (no gaps). Each zip holds one folder per fund company (`<Fondbolag>_<institutnr>_<timestamp>/`) with one XML per fund, named `<Fond_namn>_<Fond_institutnummer>_VPFO_<YYYYQn>_<publication timestamp>.xml`; namespace `http://schemas.fi.se/publika/vardepappersfonder/20200331`; elements `Rapportinformation/Kvartalsslut`, `Bolagsinformation` (name, institutnummer, LEI), `Fondinformation` (institutnummer, ISIN, name, Förvaltningsavgift with or without share classes, Fondförmögenhet, Likvida_medel, Aktiv_risk, Standardavvikelse_24_månader, Jämförelseindex), `FinansiellaInstrument/FinansielltInstrument` (Tillgångsslag_enligt_LVF_5_kap, Instrumentnamn, ISIN-kod_instrument, Landkod_Emittent, Valuta, Antal, Nominellt_belopp, Kurs_som_använts_vid_värdering_av_instrumentet, Valutakurs_instrument, Marknadsvärde_instrument, Andel_av_fondförmögenhet_instrument, Bransch). From 2025Q3 on the zip entries use backslash paths (Windows-style, no folder entries).

| zip | size | XML files | funds kept in long file |
|---|---|---|---|
| Fondinnehav_2018Q4_2022-11-16 17.05.zip | 4,916,094 | 626 | 571 |
| Fondinnehav_2019Q1_2022-11-16 17.35.zip | 4,841,204 | 607 | 562 |
| Fondinnehav_2019Q2_2022-11-16 15.35.zip | 4,790,083 | 596 | 551 |
| Fondinnehav_2019Q3_2022-11-11 15.05.zip | 4,897,170 | 601 | 556 |
| Fondinnehav_2019Q4_2022-10-28 14.04.zip | 4,947,171 | 606 | 556 |
| Fondinnehav_2020Q1_2022-10-28 14.34.zip | 5,077,514 | 621 | 559 |
| Fondinnehav_2020Q2_2022-10-28 14.34.zip | 5,128,810 | 623 | 572 |
| Fondinnehav_2020Q3_2022-10-31 15.06.zip | 5,147,926 | 629 | 579 |
| Fondinnehav_2020Q4_2022-10-28 14.34.zip | 5,185,203 | 633 | 586 |
| Fondinnehav_2021Q1_2022-10-31 17.36.zip | 5,336,201 | 636 | 593 |
| Fondinnehav_2021Q2_2022-10-28 15.04.zip | 5,259,707 | 632 | 592 |
| Fondinnehav_2021Q3_2022-10-28 15.04.zip | 5,302,501 | 643 | 600 |
| Fondinnehav_2021Q4_2022-10-28 15.04.zip | 5,523,642 | 648 | 608 |
| Fondinnehav_2022Q1_2023-02-22 14.30.zip | 5,537,738 | 657 | 613 |
| Fondinnehav_2022Q2_2023-02-22 14.30.zip | 5,557,653 | 668 | 626 |
| Fondinnehav_2022Q3_2023-02-22 14.30.zip | 5,391,662 | 670 | 632 |
| Fondinnehav_2022Q4_2023-02-28 09.36.zip | 5,792,909 | 676 | 637 |
| Fondinnehav_2023Q1_2023-05-08 11.33.zip | 5,880,418 | 682 | 647 |
| Fondinnehav_2023Q2_2023-09-08 11.02.zip | 5,886,629 | 692 | 658 |
| Fondinnehav_2023Q3_2023-12-21 10.32.zip | 5,885,808 | 701 | 661 |
| Fondinnehav_2023Q4_2026-10-14 08.07.zip | 6,201,649 | 714 | 678 |
| Fondinnehav_2024Q1_2026-10-14 08.07.zip | 6,416,719 | 711 | 674 |
| Fondinnehav_2024Q2_2026-10-14 08.07.zip | 6,291,417 | 700 | 660 |
| Fondinnehav_2024Q3_2026-10-14 08.07.zip | 6,294,418 | 699 | 658 |
| Fondinnehav_2024Q4_2026-10-14 08.12.zip | 6,255,739 | 707 | 667 |
| Fondinnehav_2025Q1_2026-10-14 08.12.zip | 6,248,940 | 698 | 659 |
| Fondinnehav_2025Q2_2026-10-14 08.12.zip | 6,298,824 | 705 | 658 |
| Fondinnehav_2025Q3_2026-10-14 08.12.zip | 6,102,850 | 706 | 663 |
| Fondinnehav_2025Q4_2026-10-14 08.12.zip | 6,235,990 | 706 | 666 |
| Fondinnehav_2026Q1_2026-10-14 08.12.zip | 6,439,375 | 711 | 675 |
| Fondinnehav_2026Q2_2026-10-14 08.12.zip | 6,693,565 | 726 | 677 |

("Funds kept" is the number of distinct Fond_institutnummer per quarter in `fi_holdings_long.csv.gz`, after keeping the latest FI publication per fund-quarter; rows per quarter run from 85,624 (2018Q4) to 122,248 (2026Q2); 886 distinct funds over the 31 quarters.) Also in `data/extra/`: `fi_2023q4.zip` (6.1 MB, 761 entries), `fi_2024q1.zip` (6.3 MB, 759), `fi_2024q2.zip` (6.2 MB, 749), `fi_2026q2.zip` (6.7 MB, 726; byte count identical to the senastedata 2026Q2 zip). These were FI downloads with earlier timestamps used by `data/measurements/parse_fi.py` (whose per-quarter outputs `fi_holdings_2024q2.csv`, `fi_funds_*.csv`, `netdemand_*.csv` are **not** on disk; only their downstream `fund_fi_mapping.csv` and `fip_*` tables are).

**Parsed long file:** `data/senastedata/output/fi_holdings_long.csv.gz`, 106 MB gz, 3,064,860 rows, 17 columns (listed in 2.2), quarters 2018-12-31 through 2026-06-30 (31), 886 funds, 937 fund ISINs, 74 fund companies, 45,709 instrument ISINs. No `fi_holdings_<q>.csv` per-quarter files exist.

---

## 6. FTN / PPM fund data

| requested item | exists? | where | rows x cols | columns | dates / funds |
|---|---|---|---|---|---|
| `exit_days_by_loser.csv` | yes | `thesis2/data/exit_days/` | 78 x 19 | `round, award, fondnr, fondnamn, kategori, performanceid, ccy, avslutsdatum, mv_award_msek, tna_at_award, last_obs, n_days_window, n_big_days, big_days, sum_flow_window_pct, sum_big_flow_pct, max_single_day_pct, pre_year_days_le_minus5, pre_year_sd_flow_pct` | 78 losers, 9 rounds, award 2024-03-25 to 2026-05-28, avslutsdatum 2024-06-14 to 2026-06-24, last_obs up to 2026-09-30; built by `detect_exit_days.py` from the (absent) `data/Valuations/*.csv` |
| `losers_daily_valuations.csv` | yes | same folder | 84,696 x 9 | `performanceId, date, classcurrencyiso, fundcurrencyiso, netflowclass, netflowfund, shares, tnaclass, tnafund` | 78 performanceIds, daily 2018-01-01 to 2026-09-30 (the only daily TNA/flow data on the machine) |
| `bids_long.csv` | yes, two identical copies | `data/derived/ftn_2026-10-11/` and `data/measurements/` | 290 x 53 | `round, category, announce_date, bid_deadline, award_date, n_bids_reported, n_qualified_reported, bid_no, manager, fund_name, winner, qualified, on_ppm_at_announce, incumbent_in_category, new_to_platform, ..., ppm_fondnr_at_announce, ppm_isin_at_announce, ppm_fondnr_any, ppm_isins, shof_fundid, shof_match, perfid, ret12_ann, ret36_ann, ret12_dl, ret36_dl, ppm_ret12, ppm_ret36, ..., tna_fund_msek, log_tna_msek, size_pct, ppm_fee_net, ppm_fee_gross, ppm_capital_msek, post_award_months, post_award_last_ym` | 11 rounds, 11 categories, announce 2023-06-30 to 2025-10-28, award 2024-03-25 to 2026-09-22; 290 bid fund names, 133 PPM fondnr, 258 SHoF fundids |
| swing status | yes | `thesis2/data/swing/swing_status_ftn_losers.csv` (78 x 20: `round, award, fondnr, fondnamn, isin, kategori, avslutsdatum, mv_award_msek, forvaltare_panel, svensk_panel, fund_company, domicile, swing_status_at_exit, swing_since, max_factor_pct, applied_disclosed, evidence_doc_date, source_url, verification, notes`) and `swing_status_2019_purge.csv` (60 x 16) | | | 78 losers / 60 purge funds; builder `build_outputs.py`, notes `swing_notes.md` |
| loser / winner fund lists | yes | `data/measurements/agentA_task1_round_membership.csv` (131 x 12: `round, award, fondnr, fondnamn, kategori, role, mv_award, val_award, first_month, last_month, avslutsdatum, fondstatus`; role winner/loser); `agentA_task2_loser_decomposition.csv` = `reallocation_losers.csv` (78 x 21); `fund_fi_mapping.csv` (91 x 15, FI names for 2024q2/2026q2); `winners_fee_series.csv` (2,370 x 11, 62 winner fondnr, monthly 2022-01-31 to 2026-08-31, two identical copies); `unmatched_for_lseg.csv` (144 bids without SEK TRI) | | | |
| daily NAV / TNA per fund | partial | daily TNA + flows only for the 78 losers (above). Monthly for all funds: `data/derived/shof_monthly/shof_valuations_monthly.csv` (457,842 x 12, 4,984 performanceIds, 2018-01 to 2026-09: `performanceId, ym, secid, ccy_class, ccy_fund, last_date, tnaclass, tnafund, nf_class, nf_fund, ndays, nf_class_n`) and `shof_rips_monthly.csv` (442,507 x 5, 4,761 performanceIds: `performanceId, returntype, ym, last_date, tri_sek`). Daily PPM NAV for 2024 only: `data/extra/ppm_nav_2024.xlsx` (4 quarterly sheets, ~26-28k rows each: `Fondbolag, Fondnummer, Fondnamn, Datum, Valutakurs sälj/köp, Fondkurs sälj/köp, Fondkurs i SEK köp/sälj`). | | | raw SHoF daily `Valuations/` and `Reinvestments/` folders are **absent** |
| Pensionsmyndigheten files | yes | `data/raw/<period>/<year>/` monthly statistics workbooks 2001-01-31 to 2026-08-31 (308 files; sheets incl. `Fondval & marknadsvärde`, `Fondstatistik`, `Fondstatistik - hållbarhet`); `data/extra/ppm_2023_12, 2024_03, 2024_06, 2026_06, 2026_08.xlsm` (copies); `data/Lista alla fonder 2026.xls`; `data/FTN/` 11 upphandlingsrapport PDFs | | | |
| monthly fund panels | yes | `data/panel/ppm_panel_2018_2026.csv` (53,062 x 25: `fondnr, fondnamn, val_k, val_m, val_tot, mv_k, mv_m, mv_tot, handel_netto, kategori, fondtyp, forvaltare, svensk, forvaltning, upphandlad, ret_ytd, ret_1m, ret_12m, ret_36m, fee_net, fee_gross, valuta, startdatum, isin, date`; 1,019 fondnr, 2018-01-31 to 2026-08-31, 104 month-ends); `data/derived/ftn_2026-10-11/ppm_panel_2022_2026.csv` (24,554 x 25, same columns, 520 fondnr, 2022-01-31 to 2026-08-31); `panel_nonppm_monthly.csv` (35,328 x 26, 512 fondnr, 2021-01 to 2026-09, PPM capital vs SHoF total TNA); `crosswalk_ppm_shof.csv` (514 fondnr to performanceid/fundid); `ftn_category_fees.csv` (11 rounds); `reallocation_summary_by_round.csv` (19 rows) | | | |

Scripts that built these carry absolute paths from other machines (`/mnt/user-data/uploads/financethesis_ny/...`, `/tmp/claude-0/.../scratchpad/...`, `~/mnt/financethesis_ny/data`), so they do not run as-is here; `detect_exit_days.py`, `build_outputs.py`, `pressure.py`, `replication_omxsb.py` use repo-relative paths.

---

## 7. Datastream exports

Only inside `data/senastedata/LSEG DATOR-20261025T183134Z-1-001.zip` (and the flat duplicate in `~/Downloads/drive-download-20261026T101706Z-1-001.zip`); not extracted anywhere in the repo.

| file | size | dimensions | content |
|---|---|---|---|
| `P.csv` | 36.2 MB | 5,685 lines = header + 5,684 daily rows x (1 date col `Name` + 1,467 series) | adjusted close; dates `M/D/YYYY` from 12/31/2004 to 10/14/2026; `NA` where no quote; the first data row carries `$$ER: E100,INVALID CODE OR EXPRESSION ENTERED` in the 30 `#ERROR` columns |
| `RI.csv` | 42.2 MB | same | total return index; headers `<NAME> - TOT RETURN IND` |
| `VO.csv` | 32.8 MB | same | turnover by volume (thousands of shares); headers `<NAME> - TURNOVER BY VOLUME` |
| `Codes.csv` | 60 kB | 1,467 rows x 3 cols | row i col 0 = request code of series i (1,104 ISINs: SE 1,051, FI 12, CA 9, DK 9, CH 5, GB 5, MT 4, US 3, NO 3, JE/ZA/IE 1; 363 `<RIC>`: OL 149, HE 100, CO 70, ST 44, incl. delisted like `<ACCA.OL^J25>`); col 1 empty; col 2 non-empty in 6 rows only (chunks of 300/267 codes and one full 1,467-code list, i.e. the request lists pasted into the add-in) |

Of the 1,467 series, 1,437 have at least one numeric value, 30 are `#ERROR`, and 420 names carry `DEAD - DELIST.<date>`. There are no `MV`, `NOSH`, `VA`, `UP`, `AF`, `PI`, index or factor exports on the machine; `thesis2/data/prices/README.md` lists exactly those as "Missing". Because `Codes.csv` exists, the README's item 1 (a code row) is in fact already satisfied: the mapping from P/RI/VO column position to ISIN/RIC is Codes.csv row order.

---

## Appendix A. LSEG pull scripts, verbatim

### thesis2/code/codebook/lseg_pull_v4.py

```python
"""
lseg_pull_v4.py  --  thesis 2 stock panel from LSEG Workspace CodeBook.

CodeBook blocks os, shutil, glob and other filesystem modules, so this version uses only pandas
and the LSEG library. All output is written as flat files in the notebook folder, prefixed td_.
Run one cell at a time, in order. After any kernel restart, rerun CELL 0 first.
Upload next to this notebook: omxsb_changes_2013_2026.csv, isin_list_lseg_v2.csv
"""

# %% CELL 0  --  session, helpers, smoke tests (rerun after every restart)
import pandas as pd
try:
    import lseg.data as ld
except Exception:
    import refinitiv.data as ld
try:
    import time
    def pause(s): time.sleep(s)
except Exception:
    def pause(s): pass

START = "2012-01-01"
END = pd.Timestamp.today().strftime("%Y-%m-%d")
MAX_CALLS = 9000                      # daily API quota is about 10,000 requests
CALLS = {"n": 0}

def api(fn, *a, **k):
    CALLS["n"] += 1
    if CALLS["n"] > MAX_CALLS:
        raise RuntimeError("budget: daily call budget reached, rerun tomorrow (everything resumes)")
    r = fn(*a, **k)
    pause(0.25)
    return r

def search(filter_, select, top=10000, query=None):
    kw = dict(view=ld.discovery.Views.EQUITY_QUOTES, filter=filter_, select=select, top=top)
    if query: kw["query"] = query
    return api(ld.discovery.search, **kw)

def exists(path):
    try:
        pd.read_csv(path, nrows=0); return True
    except Exception:
        return False

def save_cfg(d): pd.DataFrame([d]).to_csv("td_cfg.csv", index=False)
def load_cfg():
    c = pd.read_csv("td_cfg.csv").iloc[0].to_dict()
    c["FIELDS"] = str(c["FIELDS"]).split("|")
    c["INACTIVE_CLAUSE"] = None if pd.isna(c["INACTIVE_CLAUSE"]) else str(c["INACTIVE_CLAUSE"])
    return c

ld.open_session()

# 0a. which history fields work on this account? (tested on Volvo B, one week)
CANDIDATES = ["TR.PriceClose", "TR.TotalReturn", "TR.Volume", "TR.CompanyMarketCap",
              "TR.SharesOutstanding", "TR.Turnover"]
FIELDS = []
for f in CANDIDATES:
    try:
        t = api(ld.get_history, universe="VOLVb.ST", fields=[f],
                start="2024-06-03", end="2024-06-07", interval="daily")
        ok = t is not None and len(t) > 0 and t.notna().any().any()
        print(f + " " * (24 - len(f)), "OK" if ok else "EMPTY")
        if ok: FIELDS.append(f)
    except Exception as e:
        print(f + " " * (24 - len(f)), "FAIL:", str(e)[:100])
if "TR.TotalReturn" not in FIELDS:
    try:
        t = api(ld.get_history, universe="VOLVb.ST", fields=["TR.TotalReturn1D"],
                start="2024-06-03", end="2024-06-07", interval="daily")
        if len(t): FIELDS.append("TR.TotalReturn1D"); print("TR.TotalReturn1D       OK")
    except Exception as e:
        print("TR.TotalReturn1D FAIL:", str(e)[:100])
print("\nFIELDS to use:", FIELDS)
assert "TR.PriceClose" in FIELDS, "TR.PriceClose failed: stop and send Claude the output above"

# 0b. does Search accept the field list, and does it return delisted stocks?
SEL_FULL = "RIC,DTSubjectName,IssueISIN,ExchangeCode,ExchangeName,RCSAssetCategoryLeaf,RetireDate,PrimaryRIC,TickerSymbol"
SEL_MIN = "RIC,DTSubjectName,IssueISIN,ExchangeCode,RetireDate"
SEL = SEL_FULL
try:
    search("ExchangeCode eq 'STO'", SEL_FULL, top=3)
except Exception as e:
    print("full select failed, using minimal select:", str(e)[:100]); SEL = SEL_MIN

INACTIVE_CLAUSE = None
for clause in ["IsActive eq false", "AssetState eq 'DC'"]:
    try:
        s = search("ExchangeCode eq 'STO' and " + clause, SEL, top=5, query="Klovern")
        print("\ninactive clause '" + clause + "':", len(s), "rows"); print(s.to_string())
        if len(s): INACTIVE_CLAUSE = clause; break
    except Exception as e:
        print("clause '" + clause + "' FAIL:", str(e)[:100])
print("\nINACTIVE_CLAUSE =", INACTIVE_CLAUSE, "(None means Search could not return delisted stocks: tell Claude)")
save_cfg({"FIELDS": "|".join(FIELDS), "SEL": SEL, "INACTIVE_CLAUSE": INACTIVE_CLAUSE})
# SEND CLAUDE everything this cell printed.


# %% CELL 1  --  universe: every Swedish share, active and delisted, alive at some point since 2012
cfg = load_cfg(); SEL = cfg["SEL"]; INACTIVE_CLAUSE = cfg["INACTIVE_CLAUSE"]
CATS = ["RCSAssetCategoryLeaf eq 'Ordinary Share'", "RCSAssetCategoryLeaf eq 'Depository Receipt'"]
frames, used = [], None
for base in ["RCSExchangeCountryLeaf eq 'Sweden'", "ExchangeCountry eq 'SWE'", "ExchangeCode eq 'STO'"]:
    try:
        for cat in CATS:
            a = search(base + " and " + cat, SEL); frames.append(a.assign(active_flag=True))
            if len(a) >= 10000: print("WARNING: active search hit the 10,000 cap for", cat)
            n_i = "n/a"
            if INACTIVE_CLAUSE:
                i = search(base + " and " + cat + " and " + INACTIVE_CLAUSE, SEL); frames.append(i.assign(active_flag=False))
                n_i = len(i)
                if len(i) >= 10000: print("WARNING: inactive search hit the 10,000 cap for", cat)
            print(base, "|", cat[-20:], ": active", len(a), ", inactive", n_i)
        used = base; break
    except Exception as e:
        print("filter failed:", base, "->", str(e)[:120]); frames = []
assert frames, "no universe filter worked: send Claude the output"
uni = pd.concat(frames, ignore_index=True).drop_duplicates("RIC")
uni["RIC"] = uni["RIC"].astype(str)
print("\nRIC suffixes before filtering:", uni["RIC"].str.extract(r"\.([A-Za-z]+)")[0].value_counts().head(12).to_dict())
uni = uni[uni["RIC"].str.contains(r"\.ST(\^|$)", regex=True)]          # Nasdaq Stockholm and First North
if "RetireDate" in uni:
    rd_ = pd.to_datetime(uni["RetireDate"], errors="coerce")
    uni = uni[rd_.isna() | (rd_ >= "2012-01-01")]                       # drop stocks that died before our window
uni.to_csv("td_universe.csv", index=False)
n_del = int(uni["RIC"].str.contains(chr(94)).sum())
print("\nuniverse:", len(uni), "RICs, of which", n_del, "delisted (^). filter used:", used)
print(uni.head(8).to_string())
# SEND CLAUDE: the counts and the suffix list.


# %% CELL 2  --  resolve the fund-holdings ISIN list (safety net for stocks the losers own)
cfg = load_cfg(); SEL = cfg["SEL"]; INACTIVE_CLAUSE = cfg["INACTIVE_CLAUSE"]
INCLUDE_TIER2 = False   # True also pulls the non-Nordic stocks held by the European-round losers
L = pd.read_csv("isin_list_lseg_v2.csv")
if not INCLUDE_TIER2: L = L[L["tier"] == 1]
isins = L["isin"].astype(str).str.strip()
isins = sorted(set(isins[isins.str.match(r"^[A-Z]{2}[A-Z0-9]{10}$")]))
res = []
clauses = [""] + ([" and " + INACTIVE_CLAUSE] if INACTIVE_CLAUSE else [])
for k in range(0, len(isins), 50):
    chunk = ",".join("'" + x + "'" for x in isins[k:k + 50])
    for extra in clauses:
        try:
            res.append(search("IssueISIN in (" + chunk + ")" + extra, SEL, top=2000))
        except Exception as e:
            print("isin chunk", k, "FAIL:", str(e)[:100])
isin_res = pd.concat(res, ignore_index=True).drop_duplicates("RIC") if res else pd.DataFrame(columns=["RIC", "IssueISIN"])
if len(isin_res):
    home = pd.Series("", index=isin_res.index)
    pref = isin_res["IssueISIN"].astype(str).str[:2]
    pat = pref.map({"SE": r"\.ST(\^|$)", "DK": r"\.CO(\^|$)", "FI": r"\.HE(\^|$)", "NO": r"\.OL(\^|$)"})
    keep = pd.Series(True, index=isin_res.index)
    for p in pat.dropna().unique():
        m = pat == p
        keep[m] = isin_res.loc[m, "RIC"].astype(str).str.contains(p, regex=True)
    isin_res = isin_res[keep]
isin_res.to_csv("td_isin_resolved.csv", index=False)
found = set(isin_res["IssueISIN"]) if len(isin_res) else set()
print("ISINs in list:", len(isins), "| resolved to a home-exchange share:", len(found), "| unresolved:", len(set(isins) - found))
print("(unresolved ones are mostly bonds and fund units; that is expected)")


# %% CELL 3  --  map the 394 OMXSB events to RICs, delisted included
uni = pd.read_csv("td_universe.csv"); uni["RIC"] = uni["RIC"].astype(str)
ev = pd.read_csv("omxsb_changes_2013_2026.csv")
def ric_base(t):
    p = str(t).strip().split()
    return p[0] + "".join(x.lower() for x in p[1:])      # 'BALD B' -> 'BALDb', 'ALIV SDB' -> 'ALIVsdb'
def norm(s):
    s = pd.Series([str(s)]).str.replace(r"\(publ\)|\bAB\b|\bser\.?\b|\bSDB\b|\bplc\b|,|\.", " ", regex=True, case=False)
    return " ".join(s.iloc[0].lower().split())
def sim(a, b):
    A, B = set(a.split()), set(b.split())
    return len(A & B) / max(1, len(A | B))
uni["base"] = uni["RIC"].str.replace(r"\.ST(\^.*)?$", "", regex=True)
uni["nname"] = uni["DTSubjectName"].map(norm)
rows = []
for tk, grp in ev.groupby("ticker"):
    name, base = grp["company"].iloc[0], ric_base(tk)
    hit, how = uni[uni["base"] == base], "ticker"
    if hit.empty: hit = uni[uni["base"].str.lower() == base.lower()]
    if hit.empty:
        sc = uni["nname"].map(lambda x: sim(norm(name), x))
        hit, how = uni[sc >= 0.5].assign(score=sc[sc >= 0.5]).sort_values("score", ascending=False).head(3), "name"
    if len(hit) > 1:                                      # several listings: keep the one alive at the event
        ed = pd.to_datetime(grp["effective_date"], errors="coerce").max()
        rd_ = pd.to_datetime(hit["RetireDate"], errors="coerce") if "RetireDate" in hit else pd.Series(pd.NaT, index=hit.index)
        alive = hit[rd_.isna() | (rd_ >= ed)]
        hit = alive if len(alive) else hit
    rows.append({"ticker": tk, "company": name, "ric_base": base,
                 "RIC": hit["RIC"].iloc[0] if len(hit) else None,
                 "matched_name": hit["DTSubjectName"].iloc[0] if len(hit) else None,
                 "how": how if len(hit) else "UNMATCHED", "n_candidates": len(hit)})
omx = pd.DataFrame(rows); omx.to_csv("td_omxsb_map.csv", index=False)
print(omx["how"].value_counts().to_dict())
print("\nUNMATCHED: type the RIC by hand into td_omxsb_map.csv (Workspace search box: company name; delisted RICs end in ^):")
print(omx[omx["how"] == "UNMATCHED"][["ticker", "company"]].to_string())
print("\nMatched by NAME, check these:")
print(omx[omx["how"] == "name"][["ticker", "company", "RIC", "matched_name"]].to_string())
# SEND CLAUDE: this output.


# %% CELL 4  --  final download list
uni = pd.read_csv("td_universe.csv")
isin_res = pd.read_csv("td_isin_resolved.csv") if exists("td_isin_resolved.csv") else pd.DataFrame()
omx = pd.read_csv("td_omxsb_map.csv")
rics = set(uni["RIC"].dropna().astype(str)) | set(isin_res.get("RIC", pd.Series(dtype=str)).dropna().astype(str)) \
       | set(omx["RIC"].dropna().astype(str))
rics = sorted(r for r in rics if r and r != "nan")
pd.DataFrame({"ric": rics}).to_csv("td_rics_final.csv", index=False)
print(len(rics), "RICs to download;", sum("^" in r for r in rics), "delisted")


# %% CELL 5  --  daily history, one RIC per call, resumable (rerun until 'to download' is 0)
cfg = load_cfg(); FIELDS = cfg["FIELDS"]
rics = pd.read_csv("td_rics_final.csv")["ric"].astype(str).tolist()
done = set(pd.read_csv("td_done.csv")["ric"].astype(str)) if exists("td_done.csv") else set()
CHUNK = 250                                            # 250 stocks per output file
def pull(r):
    err = ""
    try:
        h = api(ld.get_history, universe=r, fields=FIELDS, start=START, end=END, interval="daily")
        if h is not None and len(h): return h.copy(), "tr"
        err = "tr empty"
    except Exception as e:
        err = "tr: " + str(e)[:120]
    try:                                               # fallback: pricing endpoint (close, volume, turnover)
        h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        if h is not None and len(h): return h.copy(), "pricing"
        err += " | pricing empty"
    except Exception as e:
        err += " | pricing: " + str(e)[:120]
    raise RuntimeError(err)

todo = [(k, r) for k, r in enumerate(rics) if r not in done]
print(len(todo), "to download,", len(done), "already on disk")
fails, n_ok = [], 0
for n, (k, r) in enumerate(todo, 1):
    try:
        h, src = pull(r)
        h.index.name = "date"; h = h.reset_index(); h.columns = [str(c) for c in h.columns]
        h["ric"] = r; h["source"] = src
        f = "td_%s_%03d.csv" % ("daily" if src == "tr" else "pricing", k // CHUNK)
        h.to_csv(f, mode="a", index=False, header=not exists(f))
        pd.DataFrame({"ric": [r]}).to_csv("td_done.csv", mode="a", index=False, header=not exists("td_done.csv"))
        n_ok += 1
    except RuntimeError as e:
        if "budget" in str(e): print("STOP:", e); break
        fails.append({"ric": r, "error": str(e)})
    if n % 100 == 0: print(n, "/", len(todo), "done,", len(fails), "failed,", CALLS["n"], "API calls this session")
if fails:
    pd.DataFrame(fails).to_csv("td_failures.csv", mode="a", index=False, header=not exists("td_failures.csv"))
print("finished this run:", n_ok, "downloaded,", len(fails), "failed (td_failures.csv)")


# %% CELL 6  --  indices
IDX = [".OMXSPI", ".OMXSGI", ".OMXS30", ".OMXS30GI", ".OMXSB", ".OMXSBGI", ".OMXSBCAPGI", ".SIXRX", ".SIXPRX"]
parts = []
for r in IDX:
    try:
        try:
            h = api(ld.get_history, universe=r, fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        except Exception:
            h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        h.index.name = "date"; h = h.reset_index(); h.columns = [str(c) for c in h.columns]
        col = [c for c in h.columns if c != "date"][0]
        parts.append(pd.DataFrame({"ric": r, "date": h["date"], "close": h[col]}))
        print(r + " " * (14 - len(r)), len(h), "rows ", str(h["date"].min())[:10], "to", str(h["date"].max())[:10])
    except Exception as e:
        print(r + " " * (14 - len(r)), "FAILED:", str(e)[:100])
if parts: pd.concat(parts).to_csv("indices_daily.csv", index=False)
# Must have: .OMXSGI (market total return) or .OMXSPI, and .OMXSBGI or .OMXSB. Tell Claude which failed.


# %% CELL 7  --  combine, static table, coverage check against the OMXSB events
def canon(c):
    cl = str(c).lower()
    if c == "TRDPRC_1" or "price close" in cl: return "close"
    if c == "ACVOL_UNS" or cl == "volume": return "volume"
    if "total return" in cl: return "totret"
    if "market cap" in cl: return "mcap"
    if "shares" in cl: return "shares"
    if c == "TRNOVR_UNS" or "turnover" in cl: return "turnover"
    return c
rics = pd.read_csv("td_rics_final.csv")["ric"].astype(str).tolist()
n_files = len(rics) // 250 + 1
parts = []
for kind in ["daily", "pricing"]:
    for k in range(n_files):
        f = "td_%s_%03d.csv" % (kind, k)
        if not exists(f): continue
        d = pd.read_csv(f, low_memory=False).rename(columns=canon)
        d = d.loc[:, ~d.columns.duplicated()]
        keep = [c for c in ["ric", "date", "close", "totret", "volume", "mcap", "shares", "turnover", "source"] if c in d]
        parts.append(d[keep])
daily = pd.concat(parts, ignore_index=True)
daily["date"] = pd.to_datetime(daily["date"], errors="coerce")
daily = daily.sort_values(["ric", "date"])
daily.to_csv("stocks_daily.csv.gz", index=False, compression="gzip")
uni = pd.read_csv("td_universe.csv").rename(columns={"RIC": "ric"})
static = (daily.groupby("ric").agg(first_date=("date", "min"), last_date=("date", "max"), n_days=("date", "size")).reset_index()
          .merge(uni[[c for c in ["ric", "DTSubjectName", "IssueISIN", "RetireDate", "ExchangeCode"] if c in uni]], on="ric", how="left"))
static.to_csv("stocks_static.csv", index=False)
print("stocks_daily:", daily.shape, "| columns:", list(daily.columns))
print("rows by source:", daily["source"].value_counts().to_dict() if "source" in daily else "n/a")
print("latest date in data:", daily["date"].max())

omx = pd.read_csv("td_omxsb_map.csv")
ev = pd.read_csv("omxsb_changes_2013_2026.csv").merge(omx[["ticker", "RIC"]], on="ticker", how="left")
ad = pd.to_datetime(ev["announcement_date"], errors="coerce"); ed = pd.to_datetime(ev["effective_date"], errors="coerce")
sub = daily[daily["ric"].isin(set(ev["RIC"].dropna()))]
cov = []
for k in range(len(ev)):
    d = sub[(sub["ric"] == ev.loc[k, "RIC"]) & (sub["date"] >= ad[k] - pd.Timedelta(days=3)) & (sub["date"] <= ed[k] + pd.Timedelta(days=3))]
    cov.append(int(d["close"].notna().sum()) if "close" in d else 0)
ev["days_with_price"] = cov
print("\nOMXSB coverage:", int((ev["days_with_price"] >= 10).sum()), "of", len(ev), "events have prices from announcement to effective day")
print(ev[ev["days_with_price"] < 10][["event_id", "company", "ticker", "RIC", "days_with_price"]].to_string())
# SEND CLAUDE: the coverage line and the list under it.


# %% CELL 8  --  files to download
print("Download these from the file browser (right-click -> Download) into")
print("~/Documents/financethesis_fresh/thesis2/data/prices/ :")
for f in ["stocks_daily.csv.gz", "stocks_static.csv", "indices_daily.csv", "td_omxsb_map.csv", "td_universe.csv", "td_failures.csv"]:
    print("  ", f, "(exists)" if exists(f) else "(missing)")
```

### thesis2/code/codebook/lseg_pull_v3.py

```python
"""
lseg_pull_v3.py  --  thesis 2 stock panel from LSEG Workspace CodeBook.

One notebook cell per '# %% CELL' block. Run them in order. After any kernel restart, rerun CELL 0 first.
Files to upload next to this notebook: omxsb_changes_2013_2026.csv, isin_list_lseg_v2.csv

Design choices (why this version should not fail like the last one):
  * Universe comes from LSEG Search with delisted instruments included (RICs ending in ^Xyy),
    not from a screen of active stocks.
  * One instrument per history call, resumable, every failure logged to failures.csv.
  * Field names and filter syntax are tested first; whatever fails is dropped or swapped, and printed.
  * Daily call budget so the API quota is never exceeded silently.
"""

# %% CELL 0  --  session, helpers, smoke tests (rerun after every restart)
import os, re, time, json, difflib, shutil
import pandas as pd
try:
    import lseg.data as ld
except ImportError:
    import refinitiv.data as ld

OUT = "thesis_data"
os.makedirs(f"{OUT}/daily", exist_ok=True)
START = "2012-01-01"
END = pd.Timestamp.today().strftime("%Y-%m-%d")
MAX_CALLS = 9000                      # daily API quota is about 10,000 requests
CALLS = {"n": 0}

def api(fn, *a, **k):
    CALLS["n"] += 1
    if CALLS["n"] > MAX_CALLS:
        raise RuntimeError("budget: daily call budget reached, rerun tomorrow (everything resumes)")
    r = fn(*a, **k)
    time.sleep(0.25)
    return r

def search(filter_, select, top=10000, query=None):
    kw = dict(view=ld.discovery.Views.EQUITY_QUOTES, filter=filter_, select=select, top=top)
    if query: kw["query"] = query
    return api(ld.discovery.search, **kw)

ld.open_session()

# 0a. which history fields work on this account? (tested on Volvo B, one week)
CANDIDATES = ["TR.PriceClose", "TR.TotalReturn", "TR.Volume", "TR.CompanyMarketCap",
              "TR.SharesOutstanding", "TR.Turnover"]
FIELDS = []
for f in CANDIDATES:
    try:
        t = api(ld.get_history, universe="VOLVb.ST", fields=[f],
                start="2024-06-03", end="2024-06-07", interval="daily")
        ok = t is not None and len(t) > 0 and t.notna().any().any()
        print(f"{f:24s}", "OK" if ok else "EMPTY")
        if ok: FIELDS.append(f)
    except Exception as e:
        print(f"{f:24s} FAIL: {str(e)[:100]}")
if "TR.TotalReturn" not in FIELDS:
    try:
        t = api(ld.get_history, universe="VOLVb.ST", fields=["TR.TotalReturn1D"],
                start="2024-06-03", end="2024-06-07", interval="daily")
        if len(t): FIELDS.append("TR.TotalReturn1D"); print("TR.TotalReturn1D       OK")
    except Exception as e:
        print("TR.TotalReturn1D FAIL:", str(e)[:100])
print("\nFIELDS to use:", FIELDS)
assert "TR.PriceClose" in FIELDS, "TR.PriceClose failed: stop and send Claude the output above"

# 0b. does Search accept the field list, and does it return delisted stocks?
SEL_FULL = "RIC,DTSubjectName,IssueISIN,ExchangeCode,ExchangeName,RCSAssetCategoryLeaf,RetireDate,PrimaryRIC,TickerSymbol"
SEL_MIN = "RIC,DTSubjectName,IssueISIN,ExchangeCode,RetireDate"
SEL = SEL_FULL
try:
    search("ExchangeCode eq 'STO'", SEL_FULL, top=3)
except Exception as e:
    print("full select failed, using minimal select:", str(e)[:100]); SEL = SEL_MIN

INACTIVE_CLAUSE = None
for clause in ["IsActive eq false", "AssetState eq 'DC'"]:
    try:
        s = search(f"ExchangeCode eq 'STO' and {clause}", SEL, top=5, query="Klovern")
        print(f"\ninactive clause '{clause}': {len(s)} rows"); print(s.to_string())
        if len(s): INACTIVE_CLAUSE = clause; break
    except Exception as e:
        print(f"clause '{clause}' FAIL:", str(e)[:100])
print("\nINACTIVE_CLAUSE =", INACTIVE_CLAUSE, "(None means Search could not return delisted stocks: tell Claude)")
json.dump({"FIELDS": FIELDS, "SEL": SEL, "INACTIVE_CLAUSE": INACTIVE_CLAUSE}, open(f"{OUT}/config.json", "w"))
# SEND CLAUDE everything this cell printed.


# %% CELL 1  --  universe: every Swedish share, active and delisted, alive at some point since 2012
cfg = json.load(open(f"{OUT}/config.json")); SEL = cfg["SEL"]; INACTIVE_CLAUSE = cfg["INACTIVE_CLAUSE"]
CATS = ["RCSAssetCategoryLeaf eq 'Ordinary Share'", "RCSAssetCategoryLeaf eq 'Depository Receipt'"]
frames, used = [], None
for base in ["RCSExchangeCountryLeaf eq 'Sweden'", "ExchangeCountry eq 'SWE'", "ExchangeCode eq 'STO'"]:
    try:
        for cat in CATS:
            a = search(f"{base} and {cat}", SEL); frames.append(a.assign(active_flag=True))
            if len(a) >= 10000: print("WARNING: active search hit the 10,000 cap for", cat)
            if INACTIVE_CLAUSE:
                i = search(f"{base} and {cat} and {INACTIVE_CLAUSE}", SEL); frames.append(i.assign(active_flag=False))
                if len(i) >= 10000: print("WARNING: inactive search hit the 10,000 cap for", cat)
            print(f"{base} | {cat[-20:]}: active {len(a)}, inactive {len(i) if INACTIVE_CLAUSE else 'n/a'}")
        used = base; break
    except Exception as e:
        print("filter failed:", base, "->", str(e)[:120]); frames = []
assert frames, "no universe filter worked: send Claude the output"
uni = pd.concat(frames, ignore_index=True).drop_duplicates("RIC")
uni["RIC"] = uni["RIC"].astype(str)
print("\nRIC suffixes before filtering:", uni["RIC"].str.extract(r"\.([A-Za-z]+)")[0].value_counts().head(12).to_dict())
uni = uni[uni["RIC"].str.contains(r"\.ST(\^|$)", regex=True)]          # Nasdaq Stockholm and First North
if "RetireDate" in uni:
    rd_ = pd.to_datetime(uni["RetireDate"], errors="coerce")
    uni = uni[rd_.isna() | (rd_ >= "2012-01-01")]                       # drop stocks that died before our window
uni.to_csv(f"{OUT}/universe.csv", index=False)
print(f"\nuniverse: {len(uni)} RICs, of which {uni['RIC'].str.contains(chr(94)).sum()} delisted (^). filter used: {used}")
print(uni.head(8).to_string())
# SEND CLAUDE: the counts and the suffix list.


# %% CELL 2  --  resolve the fund-holdings ISIN list (so stocks the losers own are covered even if CELL 1 missed them)
INCLUDE_TIER2 = False   # True also pulls the non-Nordic stocks held by the European-round losers
L = pd.read_csv("isin_list_lseg_v2.csv")
if not INCLUDE_TIER2: L = L[L["tier"] == 1]
isins = L["isin"].astype(str).str.strip()
isins = sorted({i for i in isins if re.fullmatch(r"[A-Z]{2}[A-Z0-9]{10}", i)})
res = []
for k in range(0, len(isins), 50):
    chunk = ",".join(f"'{x}'" for x in isins[k:k + 50])
    clauses = [""] + ([f" and {INACTIVE_CLAUSE}"] if INACTIVE_CLAUSE else [])
    for extra in clauses:
        try:
            res.append(search(f"IssueISIN in ({chunk}){extra}", SEL, top=2000))
        except Exception as e:
            print("isin chunk", k, "FAIL:", str(e)[:100])
isin_res = pd.concat(res, ignore_index=True).drop_duplicates("RIC") if res else pd.DataFrame(columns=["RIC", "IssueISIN"])
HOME = {"SE": r"\.ST(\^|$)", "DK": r"\.CO(\^|$)", "FI": r"\.HE(\^|$)", "NO": r"\.OL(\^|$)"}
def is_home(row):
    pat = HOME.get(str(row["IssueISIN"])[:2])
    return bool(re.search(pat, str(row["RIC"]))) if pat else True
if len(isin_res):
    isin_res = isin_res[isin_res.apply(is_home, axis=1)]
isin_res.to_csv(f"{OUT}/isin_resolved.csv", index=False)
found = set(isin_res["IssueISIN"]) if len(isin_res) else set()
print(f"ISINs in list: {len(isins)} | resolved to a home-exchange share: {len(found)} | unresolved: {len(set(isins) - found)}")
print("(unresolved ones are mostly bonds, fund units and foreign stocks; that is expected)")


# %% CELL 3  --  map the 394 OMXSB events to RICs, delisted included
uni = pd.read_csv(f"{OUT}/universe.csv"); uni["RIC"] = uni["RIC"].astype(str)
ev = pd.read_csv("omxsb_changes_2013_2026.csv")
def ric_base(t):
    p = str(t).strip().split()
    return p[0] + "".join(x.lower() for x in p[1:])      # 'BALD B' -> 'BALDb', 'ALIV SDB' -> 'ALIVsdb'
def norm(s):
    s = re.sub(r"\(publ\)|\bAB\b|\bser\.?\b|\bSDB\b|\bplc\b|,|\.", " ", str(s), flags=re.I)
    return re.sub(r"\s+", " ", s).strip().lower()
uni["base"] = uni["RIC"].str.replace(r"\.ST(\^.*)?$", "", regex=True)
uni["nname"] = uni["DTSubjectName"].map(norm)
rows = []
for tk, grp in ev.groupby("ticker"):
    name, base = grp["company"].iloc[0], ric_base(tk)
    hit, how = uni[uni["base"] == base], "ticker"
    if hit.empty: hit = uni[uni["base"].str.lower() == base.lower()]
    if hit.empty:
        cands = difflib.get_close_matches(norm(name), uni["nname"].tolist(), n=3, cutoff=0.75)
        hit, how = uni[uni["nname"].isin(cands)], "name"
    if len(hit) > 1:                                      # several listings: keep the one alive at the event
        ed = pd.to_datetime(grp["effective_date"], errors="coerce").max()
        rd_ = pd.to_datetime(hit["RetireDate"], errors="coerce") if "RetireDate" in hit else pd.Series(pd.NaT, index=hit.index)
        alive = hit[rd_.isna() | (rd_ >= ed)]
        hit = alive if len(alive) else hit
    rows.append({"ticker": tk, "company": name, "ric_base": base,
                 "RIC": hit["RIC"].iloc[0] if len(hit) else None,
                 "matched_name": hit["DTSubjectName"].iloc[0] if len(hit) else None,
                 "how": how if len(hit) else "UNMATCHED", "n_candidates": len(hit)})
omx = pd.DataFrame(rows); omx.to_csv(f"{OUT}/omxsb_ric_map.csv", index=False)
print(omx["how"].value_counts().to_dict())
print("\nUNMATCHED: type the RIC by hand into omxsb_ric_map.csv (Workspace search box: company name; delisted RICs end in ^):")
print(omx[omx["how"] == "UNMATCHED"][["ticker", "company"]].to_string())
print("\nMatched by NAME, check these:")
print(omx[omx["how"] == "name"][["ticker", "company", "RIC", "matched_name"]].to_string())
# SEND CLAUDE: this output. Fix UNMATCHED rows in the csv before CELL 4 (or leave them, they are listed again in CELL 7).


# %% CELL 4  --  final download list
uni = pd.read_csv(f"{OUT}/universe.csv")
isin_res = pd.read_csv(f"{OUT}/isin_resolved.csv") if os.path.exists(f"{OUT}/isin_resolved.csv") else pd.DataFrame()
omx = pd.read_csv(f"{OUT}/omxsb_ric_map.csv")
rics = set(uni["RIC"].dropna().astype(str)) | set(isin_res.get("RIC", pd.Series(dtype=str)).dropna().astype(str)) \
       | set(omx["RIC"].dropna().astype(str))
rics = sorted(r for r in rics if r and r != "nan")
json.dump(rics, open(f"{OUT}/rics_final.json", "w"))
print(len(rics), "RICs to download;", sum("^" in r for r in rics), "delisted")


# %% CELL 5  --  daily history, one RIC per call, resumable (rerun until 'to download' is 0)
cfg = json.load(open(f"{OUT}/config.json")); FIELDS = cfg["FIELDS"]
rics = json.load(open(f"{OUT}/rics_final.json"))
def fname(r): return f"{OUT}/daily/{re.sub(r'[^A-Za-z0-9.]', '_', r)}.csv"
def pull(r):
    err = ""
    try:
        h = api(ld.get_history, universe=r, fields=FIELDS, start=START, end=END, interval="daily")
        if h is not None and len(h): h = h.copy(); h["source"] = "tr"; return h
        err = "tr empty"
    except Exception as e:
        err = "tr: " + str(e)[:120]
    try:                                                   # fallback: pricing endpoint (close, volume, turnover)
        h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        if h is not None and len(h): h = h.copy(); h["source"] = "pricing"; return h
        err += " | pricing empty"
    except Exception as e:
        err += " | pricing: " + str(e)[:120]
    raise RuntimeError(err)

todo = [r for r in rics if not os.path.exists(fname(r))]
print(len(todo), "to download,", len(rics) - len(todo), "already on disk")
fails = []
for n, r in enumerate(todo, 1):
    try:
        h = pull(r); h["ric"] = r; h.to_csv(fname(r))
    except RuntimeError as e:
        if "budget" in str(e): print("STOP:", e); break
        fails.append({"RIC": r, "error": str(e)})
    if n % 100 == 0: print(f"{n}/{len(todo)} done, {len(fails)} failed, {CALLS['n']} API calls this session")
old = pd.read_csv(f"{OUT}/failures.csv") if os.path.exists(f"{OUT}/failures.csv") else pd.DataFrame()
pd.concat([old, pd.DataFrame(fails)]).drop_duplicates("RIC", keep="last").to_csv(f"{OUT}/failures.csv", index=False) if (len(old) or fails) else None
print("finished this run. failures so far:", len(fails), "(failures.csv)")


# %% CELL 6  --  indices
IDX = [".OMXSPI", ".OMXSGI", ".OMXS30", ".OMXS30GI", ".OMXSB", ".OMXSBGI", ".OMXSBCAPGI", ".SIXRX", ".SIXPRX"]
for r in IDX:
    try:
        try:
            h = api(ld.get_history, universe=r, fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        except Exception:
            h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        h["ric"] = r; h.to_csv(f"{OUT}/index_{r.strip('.')}.csv")
        print(f"{r:14s} {len(h):5d} rows  {str(h.index.min())[:10]} to {str(h.index.max())[:10]}")
    except Exception as e:
        print(f"{r:14s} FAILED: {str(e)[:100]}")
# Must have: .OMXSGI (market total return) or .OMXSPI, and .OMXSBGI or .OMXSB. Tell Claude which failed.


# %% CELL 7  --  combine, static table, coverage check against the OMXSB events
def canon(c):
    cl = str(c).lower()
    if c == "TRDPRC_1" or "price close" in cl: return "close"
    if c == "ACVOL_UNS" or cl == "volume": return "volume"
    if "total return" in cl: return "totret"
    if "market cap" in cl: return "mcap"
    if "shares" in cl: return "shares"
    if c == "TRNOVR_UNS" or "turnover" in cl: return "turnover"
    return c
parts = []
for f in sorted(os.listdir(f"{OUT}/daily")):
    d = pd.read_csv(f"{OUT}/daily/{f}", index_col=0, parse_dates=True); d.index.name = "date"
    d = d.rename(columns=canon); d = d.loc[:, ~d.columns.duplicated()]
    parts.append(d.reset_index())
daily = pd.concat(parts, ignore_index=True)
keep = [c for c in ["ric", "date", "close", "totret", "volume", "mcap", "shares", "turnover", "source"] if c in daily]
daily = daily[keep].sort_values(["ric", "date"]); daily.to_csv(f"{OUT}/stocks_daily.csv", index=False)
uni = pd.read_csv(f"{OUT}/universe.csv").rename(columns={"RIC": "ric"})
static = (daily.groupby("ric").agg(first_date=("date", "min"), last_date=("date", "max"), n_days=("date", "size"))
          .reset_index().merge(uni[[c for c in ["ric", "DTSubjectName", "IssueISIN", "RetireDate", "ExchangeCode"] if c in uni]], on="ric", how="left"))
static.to_csv(f"{OUT}/stocks_static.csv", index=False)
print("stocks_daily:", daily.shape, "| columns:", keep)
print("rows by source:", daily["source"].value_counts().to_dict() if "source" in daily else "n/a")
print("latest date in data:", daily["date"].max())

omx = pd.read_csv(f"{OUT}/omxsb_ric_map.csv")
ev = pd.read_csv("omxsb_changes_2013_2026.csv").merge(omx[["ticker", "RIC"]], on="ticker", how="left")
ad = pd.to_datetime(ev["announcement_date"], errors="coerce"); ed = pd.to_datetime(ev["effective_date"], errors="coerce")
cov = []
for k in range(len(ev)):
    d = daily[(daily["ric"] == ev.loc[k, "RIC"]) & (daily["date"] >= ad[k] - pd.Timedelta(days=3)) & (daily["date"] <= ed[k] + pd.Timedelta(days=3))]
    cov.append(int(d["close"].notna().sum()) if "close" in d else 0)
ev["days_with_price"] = cov
print(f"\nOMXSB coverage: {(ev['days_with_price'] >= 10).sum()} of {len(ev)} events have prices from announcement to effective day")
print(ev[ev["days_with_price"] < 10][["event_id", "company", "ticker", "RIC", "days_with_price"]].to_string())
# SEND CLAUDE: the coverage line and the list under it.


# %% CELL 8  --  zip everything for download
shutil.make_archive("thesis_data", "zip", OUT)
print("thesis_data.zip is ready. Right-click it in the CodeBook file browser -> Download,")
print("then unzip into ~/Documents/financethesis_fresh/thesis2/data/prices/")
```

### thesis2/code/lseg_codebook_pull_v2.py

```python
"""
lseg_codebook_pull_v2.py: targeted stock panel for thesis 2, run inside LSEG Workspace CodeBook.

Pulls ONE instrument per request (small requests do not hit API limits), resumes where it stopped,
and logs every failure to failures.csv instead of silently dropping it.

Upload lseg_input.csv into the same CodeBook folder as this file before running.
Run the steps one cell at a time, in order. Send Claude the printed output of each step.
"""
import os, time, json
import pandas as pd
try:
    import lseg.data as ld
except ImportError:                      # older CodeBook images
    import refinitiv.data as ld

OUT = "thesis_data"
os.makedirs(f"{OUT}/daily", exist_ok=True)
START, END = "2012-01-01", pd.Timestamp.today().strftime("%Y-%m-%d")
ld.open_session()

# ===================================================================== STEP 0: does anything work?
t = ld.get_history(universe="VOLVb.ST", fields=["TR.PriceClose", "TR.Volume"],
                   start="2024-06-03", end="2024-06-07", interval="daily")
print(t)
# Expect 5 rows with price and volume. If this fails, stop and send Claude the error.

# ===================================================================== STEP 1: resolve every id to a RIC
inp = pd.read_csv("lseg_input.csv")
rows = []
# 1a. ISINs -> RIC, name, status (one call per 100 ISINs)
isins = inp.loc[inp.id_type == "ISIN", "id"].tolist()
for k in range(0, len(isins), 100):
    try:
        d = ld.get_data(universe=isins[k:k+100],
                        fields=["TR.RIC", "TR.CommonName", "TR.ISIN", "TR.InstrumentIsActive",
                                "TR.ExchangeMarketIdCode", "TR.InstrumentType"])
        rows.append(d)
    except Exception as e:
        print("isin batch", k, e)
    time.sleep(0.5)
# 1b. guessed RICs for OMXSB names (delisted ones will fail here and are retried in 1c)
rics_guess = inp.loc[inp.id_type == "RIC", "id"].tolist()
try:
    d = ld.get_data(universe=rics_guess,
                    fields=["TR.RIC", "TR.CommonName", "TR.ISIN", "TR.InstrumentIsActive", "TR.ExchangeMarketIdCode"])
    rows.append(d)
except Exception as e:
    print("ric batch", e)
res = pd.concat(rows, ignore_index=True)
res.to_csv(f"{OUT}/resolved.csv", index=False)

# 1c. OMXSB names whose guessed RIC did not resolve: search by company name, active AND inactive
ok_names = set(res.get("Company Common Name", pd.Series(dtype=str)).dropna())
missing = inp[(inp.id_type == "RIC")]
missing = missing[~missing.id.isin(res.loc[res.get("RIC", pd.Series(dtype=str)).notna(), "Instrument"])]
found = []
for _, r in missing.iterrows():
    try:
        s = ld.discovery.search(query=r["name"], top=3,
                                filter="ExchangeCode eq 'STO' and AssetCategory eq 'ORD'",
                                select="RIC,DTSubjectName,IssueISIN,ExchangeName,RetireDate")
        if len(s):
            s["query"] = r["name"]; found.append(s.head(1))
    except Exception as e:
        print("search", r["name"], e)
    time.sleep(0.3)
if found:
    pd.concat(found).to_csv(f"{OUT}/omxsb_search_hits.csv", index=False)
print("resolved rows:", len(res), "| OMXSB searched:", len(missing), "| search hits:", sum(len(f) for f in found))
# Send Claude these three numbers and the first rows of omxsb_search_hits.csv.

# ===================================================================== STEP 2: build the final RIC list
ric_col = "RIC" if "RIC" in res.columns else res.columns[1]
rics = set(res[ric_col].dropna().astype(str))
if found:
    rics |= set(pd.concat(found)["RIC"].dropna().astype(str))
rics = sorted(r for r in rics if r.endswith(".ST") or ".ST^" in r)   # Stockholm listings only
json.dump(rics, open(f"{OUT}/rics.json", "w"))
print(len(rics), "Stockholm RICs to download")

# ===================================================================== STEP 3: daily history, one RIC per call
FIELDS = ["TR.PriceClose", "TR.TotalReturn", "TR.Volume", "TR.CompanyMarketCap", "TR.SharesOutstanding"]
fails = []
for n, r in enumerate(rics):
    path = f"{OUT}/daily/{r.replace('^', '_')}.csv"
    if os.path.exists(path):
        continue
    for attempt in range(3):
        try:
            h = ld.get_history(universe=r, fields=FIELDS, start=START, end=END, interval="daily")
            h.to_csv(path); break
        except Exception as e:
            if attempt == 2: fails.append({"ric": r, "error": str(e)[:200]})
            time.sleep(3)
    time.sleep(0.25)
    if n % 50 == 0: print("done", n, "of", len(rics))
pd.DataFrame(fails).to_csv(f"{OUT}/failures.csv", index=False)
print("finished; failures:", len(fails))

# ===================================================================== STEP 4: static fields (listing and delisting dates)
st = []
for k in range(0, len(rics), 100):
    try:
        st.append(ld.get_data(universe=rics[k:k+100],
                              fields=["TR.CommonName", "TR.ISIN", "TR.FirstTradeDate", "TR.RetireDate",
                                      "TR.TRBCEconomicSector", "TR.FreeFloatPct"]))
    except Exception as e:
        print("static", k, e)
pd.concat(st).to_csv(f"{OUT}/stocks_static.csv", index=False)

# ===================================================================== STEP 5: indices
for r in [".OMXSPI", ".SIXRX", ".OMXSBGI", ".OMXSB", ".OMXS30"]:
    try:
        h = ld.get_history(universe=r, fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        h.to_csv(f"{OUT}/index_{r.strip('.')}.csv"); print(r, len(h))
    except Exception as e:
        print(r, "failed:", str(e)[:120])

ld.close_session()
print("Download the folder", OUT)
```

### thesis2/code/lseg_codebook_pull.py

```python
"""
lseg_codebook_pull.py: pull the stock panel for thesis 2 inside LSEG Workspace CodeBook.

How to use
  1. Workspace -> search "CodeBook" -> open it -> New -> Python 3 notebook (or upload this file and open it).
  2. Run STEP 0 alone first. If it prints a small table for Investor B, the field names work.
     If it errors on a field, comment that field out in FIELDS and tell Claude the error text.
  3. Run STEP 1 (universe), then STEP 2 (prices; runs in chunks, can take 1 to 3 hours, safe to restart:
     finished chunks are skipped), then STEP 3 (static), STEP 4 (indices).
  4. Zip the folder 'thesis_data' (right-click in the CodeBook file browser -> Download) and put the files in
     ~/Documents/financethesis_fresh/thesis2/data/prices/

Nothing here touches returns around FTN dates; it only downloads raw data.
"""
import os, time
import pandas as pd
import lseg.data as ld          # in older CodeBook images: import refinitiv.data as ld

OUT = "thesis_data"; os.makedirs(OUT, exist_ok=True); os.makedirs(f"{OUT}/chunks", exist_ok=True)
START, END = "2005-01-01", pd.Timestamp.today().strftime("%Y-%m-%d")

FIELDS = [
    "TR.PriceClose",            # close price (adjusted for splits)
    "TR.TotalReturn",           # daily total return in % (dividends included)
    "TR.Volume",                # shares traded
    "TR.TurnoverValue",         # value traded in local currency (if this errors, drop it; we use price x volume)
    "TR.CompanyMarketCap",      # market cap
    "TR.SharesOutstanding",     # shares outstanding
]

ld.open_session()

# ---------------------------------------------------------------- STEP 0: test on one stock
test = ld.get_history(universe=["INVEb.ST"], fields=FIELDS, start="2024-05-01", end="2024-05-20", interval="daily")
print(test)

# ---------------------------------------------------------------- STEP 1: universe (active AND delisted)
# Stockholm main market (XSTO), First North Sweden (FNSE), Spotlight (SSME); delisted RICs carry a ^ suffix.
screen = ('SCREEN(U(IN(Equity(active,inactive,public,primary))), '
          'IN(TR.ExchangeMarketIdCode,"XSTO","FNSE","SSME"), CURN=SEK)')
uni = ld.get_data(universe=screen, fields=["TR.CommonName", "TR.ISIN", "TR.ExchangeMarketIdCode", "TR.InstrumentIsActive"])
uni.to_csv(f"{OUT}/universe.csv", index=False)
rics = uni["Instrument"].dropna().unique().tolist()
print(len(rics), "instruments;", uni["TR.InstrumentIsActive" if "TR.InstrumentIsActive" in uni else uni.columns[-1]].value_counts())
# Sanity check: expect well over 1,000 instruments, a large share of them inactive. If you get only a few hundred,
# the screen dropped delisted names; tell Claude.

# ---------------------------------------------------------------- STEP 2: daily history in chunks
def pull_chunk(batch, i):
    path = f"{OUT}/chunks/prices_{i:04d}.csv"
    if os.path.exists(path):
        return
    for attempt in range(3):
        try:
            df = ld.get_history(universe=batch, fields=FIELDS, start=START, end=END, interval="daily")
            df.to_csv(path)
            return
        except Exception as e:
            print("chunk", i, "attempt", attempt, e); time.sleep(10)

BATCH = 25
for i in range(0, len(rics), BATCH):
    pull_chunk(rics[i:i + BATCH], i // BATCH)
    if (i // BATCH) % 10 == 0:
        print("done chunk", i // BATCH, "of", len(rics) // BATCH)

# stack the wide chunks into one long file: id, date, field values
longs = []
for f in sorted(os.listdir(f"{OUT}/chunks")):
    w = pd.read_csv(f"{OUT}/chunks/{f}", header=[0, 1], index_col=0)
    l = w.stack(level=0).reset_index()
    l.columns = ["date", "id"] + list(l.columns[2:])
    longs.append(l)
pd.concat(longs).to_csv(f"{OUT}/stocks_daily.csv", index=False)

# ---------------------------------------------------------------- STEP 3: static fields
static = ld.get_data(universe=rics, fields=["TR.CommonName", "TR.ISIN", "TR.TickerSymbol", "TR.ExchangeMarketIdCode",
                                            "TR.TRBCEconomicSector", "TR.TRBCIndustryGroup", "TR.FirstTradeDate",
                                            "TR.RetireDate", "TR.FreeFloatPct"])
static.to_csv(f"{OUT}/stocks_static.csv", index=False)

# ---------------------------------------------------------------- STEP 4: indices
IDX = [".OMXS30", ".OMXSPI", ".OMXSB", ".OMXSBGI", ".OMXSBCAPGI", ".SIXPRX", ".SIX30RX"]
for r in IDX:
    try:
        h = ld.get_history(universe=[r], fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        h.to_csv(f"{OUT}/index_{r.strip('.')}.csv")
        print(r, len(h))
    except Exception as e:
        print(r, "not found:", e)   # tell Claude which ones fail; there are alternative codes

ld.close_session()
print("finished; download the folder", OUT)
```

The notebooks `thesis2/code/codebook/lseg_pull_v3.ipynb` and `lseg_pull_v4.ipynb` contain the same code split at the `# %% CELL n` markers: cell 0 is a markdown title, cells 1 to 9 are CELL 0 to CELL 8 above, with no saved outputs.

---

## Appendix B. Per-file profile of every tabular data file

Generated 26 Oct 2026 with pandas from the files as found. For each file: size, rows, every column with dtype, min and max of date-like columns, number of unique values of id-like columns, first 3 rows. Workbooks over 5 MB show sheet names and dimensions only.

### data/senastedata/indices_daily.csv  (613.1 kB)
- rows: 22,311  cols: 3
- columns (dtype):
    - `ric` (object)
    - `date` (object)
    - `close` (float64)
- date-like ranges:
    - `date`: 2012-01-02 00:00:00 → 2026-10-14 00:00:00
- id-like uniques:
    - `ric`: 6 unique (nulls 0)
- first 3 rows:
```
       ric        date   close
0  .OMXSPI  2012-01-02  311.29
1  .OMXSPI  2012-01-03  317.26
2  .OMXSPI  2012-01-04  313.98
```

### data/senastedata/omxsb_events_with_ric.csv  (152.7 kB)
- rows: 394  cols: 13
- columns (dtype):
    - `event_id` (object)
    - `effective_date` (object)
    - `announcement_date` (object)
    - `company` (object)
    - `ticker` (object)
    - `isin` (float64)
    - `type` (object)
    - `review_cycle` (object)
    - `source_url` (object)
    - `verification` (object)
    - `notes` (object)
    - `RIC` (object)
    - `days_with_price` (int64)
- date-like ranges:
    - `effective_date`: 2013-06-03 00:00:00 → 2026-06-01 00:00:00
    - `announcement_date`: 2013-05-08 00:00:00 → 2026-05-22 00:00:00
    - `days_with_price`: 10 → 24
- id-like uniques:
    - `event_id`: 394 unique (nulls 0)
    - `company`: 214 unique (nulls 0)
    - `ticker`: 152 unique (nulls 0)
    - `isin`: 0 unique (nulls 394)
    - `RIC`: 147 unique (nulls 0)
    - `days_with_price`: 11 unique (nulls 0)
- first 3 rows:
```
          event_id effective_date announcement_date                       company   ticker  isin      type review_cycle                                                                                                                               source_url verification                                                                                                                                 notes            RIC  days_with_price
0  OMXSB-2013H1-01     2013-06-03        2013-05-08   Fastighets AB Balder ser. B   BALD B   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)       BALDb.ST               22
1  OMXSB-2013H1-02     2013-06-03        2013-05-08                        SAS AB      SAS   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)     SAS.ST^H24               22
2  OMXSB-2013H1-03     2013-06-03        2013-05-08  Black Earth Farming Ltd. SDB  BEF SDB   NaN  deletion       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)  BEFsdb.ST^L17               22
```

### data/senastedata/stocks_static.csv  (118.4 kB)
- rows: 1,667  cols: 8
- columns (dtype):
    - `ric` (object)
    - `first_date` (object)
    - `last_date` (object)
    - `n_days` (int64)
    - `DTSubjectName` (object)
    - `IssueISIN` (object)
    - `RetireDate` (object)
    - `ExchangeCode` (object)
- date-like ranges:
    - `first_date`: 1991-11-01 00:00:00 → 2026-09-30 00:00:00
    - `last_date`: 1991-11-01 00:00:00 → 2026-10-14 00:00:00
    - `n_days`: 1 → 3712
    - `RetireDate`: 2011-02-23 00:00:00 → 2026-10-13 00:00:00
- id-like uniques:
    - `ric`: 1,667 unique (nulls 0)
    - `DTSubjectName`: 1,226 unique (nulls 412)
    - `IssueISIN`: 1,247 unique (nulls 412)
    - `ExchangeCode`: 1 unique (nulls 412)
- first 3 rows:
```
             ric  first_date   last_date  n_days      DTSubjectName     IssueISIN  RetireDate ExchangeCode
0     2020NOK.ST  2019-12-12  2026-10-14    1272                NaN           NaN         NaN          NaN
1  24STOR.ST^A22  2019-12-10  2022-01-07     520  24Storage Ord Shs  SE0013358710  2022-01-10          STO
2  2CUREX.ST^I26  2017-11-24  2026-08-31    2193     2cureX Ord Shs  SE0010468124  2026-09-01          STO
```

### data/senastedata/td_failures.csv  (6.8 kB)
- rows: 48  cols: 2
- columns (dtype):
    - `ric` (object)
    - `error` (object)
- id-like uniques:
    - `ric`: 34 unique (nulls 0)
- first 3 rows:
```
                  ric                                                                                                                                                                                                      error
0   0#GB00BG5YJD47.ST  tr: Unable to resolve all requested identifiers in ['0#GB00BG5YJD47.ST']. | pricing: No data to return, please check errors: ERROR: No successful response.\n(TS.Interday.UserRequestError.70005, The uni
1  0#GB00BG60JM08.STf  tr: Unable to resolve all requested identifiers in ['0#GB00BG60JM08.STf']. | pricing: No data to return, please check errors: ERROR: No successful response.\n(TS.Interday.UserRequestError.70005, The un
2   0#GB00BG62QK33.ST  tr: Unable to resolve all requested identifiers in ['0#GB00BG62QK33.ST']. | pricing: No data to return, please check errors: ERROR: No successful response.\n(TS.Interday.UserRequestError.70005, The uni
```

### data/senastedata/stocks_daily.csv.gz  (76.02 MB)
- rows: 3,206,212  cols: 9
- columns (dtype):
    - `ric` (object)
    - `date` (object)
    - `close` (float64)
    - `totret` (float64)
    - `volume` (float64)
    - `mcap` (float64)
    - `shares` (float64)
    - `turnover` (float64)
    - `source` (object)
- date-like ranges:
    - `date`: 1991-11-01 00:00:00 → 2026-10-14 00:00:00
- id-like uniques:
    - `ric`: 1,667 unique (nulls 0)
- first 3 rows:
```
          ric        date     close     totret   volume          mcap      shares  turnover source
0  2020NOK.ST  2019-12-12  1.312456        NaN  10000.0  1.849054e+09  22170906.0       NaN     tr
1  2020NOK.ST  2019-12-17  1.297016  -1.176471      NaN           NaN         NaN       NaN     tr
2  2020NOK.ST  2020-04-21  0.759681 -41.428571      2.0  1.130716e+09  22170906.0       NaN     tr
```

### data/senastedata/output/events_car.csv  (317.6 kB)
- rows: 380  cols: 54
- columns (dtype):
    - `event_id` (object)
    - `effective_date` (object)
    - `announcement_date` (object)
    - `company` (object)
    - `ticker` (object)
    - `isin` (float64)
    - `type` (object)
    - `review_cycle` (object)
    - `source_url` (object)
    - `verification` (object)
    - `notes` (object)
    - `RIC` (object)
    - `days_with_price` (int64)
    - `AD` (object)
    - `ED` (object)
    - `first_date` (object)
    - `last_date` (object)
    - `IssueISIN` (object)
    - `DTSubjectName` (object)
    - `period` (object)
    - `ad_moved` (bool)
    - `ed_moved` (bool)
    - `listed_100` (bool)
    - `delisted_100` (bool)
    - `ann` (float64)
    - `eff` (float64)
    - `tot` (float64)
    - `ann_gi` (float64)
    - `eff_gi` (float64)
    - `tot_gi` (float64)
    - `ndays_tot` (int64)
    - `ym_pre` (object)
    - `turn` (float64)
    - `mcap_pre` (float64)
    - `size` (float64)
    - `vol` (float64)
    - `qb` (object)
    - `qa` (object)
    - `n_isin` (float64)
    - `f` (float64)
    - `shares_qa` (float64)
    - `idx_b` (float64)
    - `idx_a` (float64)
    - `all_b` (float64)
    - `all_a` (float64)
    - `act_b` (float64)
    - `act_a` (float64)
    - `nt` (float64)
    - `instbuy` (float64)
    - `activebuy` (float64)
    - `indexown` (float64)
    - `n_idx_funds_b` (float64)
    - `n_idx_funds_a` (float64)
    - `isins` (object)
- date-like ranges:
    - `effective_date`: 2013-06-03 00:00:00 → 2026-06-01 00:00:00
    - `announcement_date`: 2013-05-08 00:00:00 → 2026-05-22 00:00:00
    - `days_with_price`: 10 → 24
    - `first_date`: 2012-01-02 00:00:00 → 2026-02-16 00:00:00
    - `last_date`: 2017-06-07 00:00:00 → 2026-10-14 00:00:00
    - `ann`: -42.735092709761446 → 47.30771713042523
    - `eff`: -26.61946357165339 → 45.79076442525202
    - `ann_gi`: -42.50144738945338 → 47.33948619024573
    - `eff_gi`: -26.606107022408143 → 46.16152589853351
    - `ndays_tot`: 9 → 20
    - `ym_pre`: 2013-05-01 00:00:00 → 2026-05-01 00:00:00
- id-like uniques:
    - `event_id`: 380 unique (nulls 0)
    - `company`: 209 unique (nulls 0)
    - `ticker`: 147 unique (nulls 0)
    - `isin`: 0 unique (nulls 380)
    - `RIC`: 143 unique (nulls 0)
    - `days_with_price`: 11 unique (nulls 0)
    - `IssueISIN`: 140 unique (nulls 5)
    - `DTSubjectName`: 138 unique (nulls 5)
    - `n_isin`: 7 unique (nulls 121)
    - `n_idx_funds_b`: 14 unique (nulls 121)
    - `n_idx_funds_a`: 15 unique (nulls 121)
    - `isins`: 112 unique (nulls 121)
- first 3 rows:
```
          event_id effective_date announcement_date                       company   ticker  isin      type review_cycle                                                                                                                               source_url verification                                                                                                                                 notes            RIC  days_with_price          AD          ED  first_date   last_date     IssueISIN            DTSubjectName     period  ad_moved  ed_moved  listed_100  delisted_100        ann       eff        tot     ann_gi    eff_gi     tot_gi  ndays_tot   ym_pre      turn      mcap_pre      size         vol   qb   qa  n_isin   f  shares_qa  idx_b  idx_a  all_b  all_a  act_b  act_a  nt  instbuy  activebuy  indexown  n_idx_funds_b  n_idx_funds_a isins
0  OMXSB-2013H1-01     2013-06-03        2013-05-08   Fastighets AB Balder ser. B   BALD B   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)       BALDb.ST               22  2013-05-08  2013-06-03  2012-01-02  2026-10-14  SE0017832488     Fastighets AB Balder  2013–2017     False     False       False         False   3.002066 -2.021547   6.486468   3.043559 -1.995580   6.362484         20  2013-05  0.214058  7.119985e+09  0.091372   33.562091  NaN  NaN     NaN NaN        NaN    NaN    NaN    NaN    NaN    NaN    NaN NaN      NaN        NaN       NaN            NaN            NaN   NaN
1  OMXSB-2013H1-02     2013-06-03        2013-05-08                        SAS AB      SAS   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)     SAS.ST^H24               22  2013-05-08  2013-06-03  2012-01-02  2024-08-13  SE0003366871              SAS Ord Shs  2013–2017     False     False       False         False   2.017722  1.422468   1.391262   2.059216  1.448435   1.267277         20  2013-05  0.072396  4.606000e+09  0.059109  312.173858  NaN  NaN     NaN NaN        NaN    NaN    NaN    NaN    NaN    NaN    NaN NaN      NaN        NaN       NaN            NaN            NaN   NaN
2  OMXSB-2013H1-03     2013-06-03        2013-05-08  Black Earth Farming Ltd. SDB  BEF SDB   NaN  deletion       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)  BEFsdb.ST^L17               22  2013-05-08  2013-06-03  2012-01-02  2017-12-13  SE0010219774  Black Earth Farming SDR  2013–2017     False     False       False         False -11.258586 -6.362620 -21.476344 -11.217093 -6.336653 -21.600328         20  2013-05 -0.041779  1.993627e+09  0.025584  167.633946  NaN  NaN     NaN NaN        NaN    NaN    NaN    NaN    NaN    NaN    NaN NaN      NaN        NaN       NaN            NaN            NaN   NaN
```

### data/senastedata/output/holdings_price_check.csv  (48.3 kB)
- rows: 259  cols: 20
- columns (dtype):
    - `event_id` (object)
    - `company` (object)
    - `qb` (object)
    - `qa` (object)
    - `n_rows_b` (int64)
    - `n_rows_a` (int64)
    - `fi_price_b` (float64)
    - `fi_kurs_b` (float64)
    - `lseg_price_b` (float64)
    - `fi_price_a` (float64)
    - `fi_kurs_a` (float64)
    - `lseg_price_a` (float64)
    - `adj_close_b` (float64)
    - `adj_close_a` (float64)
    - `f_raw` (float64)
    - `f` (float64)
    - `kurs_vs_mv_b` (float64)
    - `kurs_vs_mv_a` (float64)
    - `fi_vs_lseg_b` (float64)
    - `fi_vs_lseg_a` (float64)
- id-like uniques:
    - `event_id`: 259 unique (nulls 0)
    - `company`: 165 unique (nulls 0)
    - `fi_price_b`: 248 unique (nulls 0)
    - `lseg_price_b`: 253 unique (nulls 6)
    - `fi_price_a`: 250 unique (nulls 0)
    - `lseg_price_a`: 253 unique (nulls 6)
- first 3 rows:
```
          event_id                              company          qb          qa  n_rows_b  n_rows_a  fi_price_b  fi_kurs_b  lseg_price_b  fi_price_a  fi_kurs_a  lseg_price_a  adj_close_b  adj_close_a  f_raw    f  kurs_vs_mv_b  kurs_vs_mv_a  fi_vs_lseg_b  fi_vs_lseg_a
0  OMXSB-2019H1-01                      Bilia AB ser. A  2019-03-31  2019-06-30        33        47       79.35      79.35     80.803361        84.0       84.0     85.538529      79.3500    84.000000    1.0  1.0           1.0           1.0      0.982014      0.982014
1  OMXSB-2019H1-02  International Petroleum Corporation  2019-03-31  2019-06-30         7        13       43.80      43.80     29.161001        41.2       41.2     27.643404      43.8000    41.200000    1.0  1.0           1.0           1.0      1.502006      1.490410
2  OMXSB-2019H1-03                    Klovern AB Ser. B  2019-03-31  2019-06-30        36        55       12.75      12.75     22.895598        14.6       14.6     25.196163      11.8441    13.562655    1.0  1.0           1.0           1.0      0.556876      0.579453
```

### data/senastedata/output/index_funds.csv  (3.6 kB)
- rows: 14  cols: 12
- columns (dtype):
    - `Fond_institutnummer` (int64)
    - `Fondbolag_namn` (object)
    - `Fond_namn` (object)
    - `Fond_ISIN` (object)
    - `benchmark` (object)
    - `q_first` (object)
    - `q_last` (object)
    - `score` (float64)
    - `years` (float64)
    - `events` (float64)
    - `index_trade` (bool)
    - `index_name` (bool)
- date-like ranges:
    - `q_first`: 2018-12-31 00:00:00 → 2018-12-31 00:00:00
    - `q_last`: 2026-06-30 00:00:00 → 2026-06-30 00:00:00
    - `years`: 8.0 → 8.0
- id-like uniques:
    - `Fond_institutnummer`: 14 unique (nulls 0)
    - `Fondbolag_namn`: 5 unique (nulls 0)
    - `Fond_namn`: 14 unique (nulls 0)
    - `Fond_ISIN`: 14 unique (nulls 0)
    - `events`: 1 unique (nulls 0)
    - `index_name`: 1 unique (nulls 0)
- first 3 rows:
```
   Fond_institutnummer            Fondbolag_namn                  Fond_namn     Fond_ISIN                                                      benchmark     q_first      q_last     score  years  events  index_trade  index_name
0                60293           Nordea Funds Ab      Nordea Sverige Passiv  SE0002591016                               OMX Stockholm Benchmark Cap 100;  2018-12-31  2026-06-30  0.967079    8.0   259.0         True        True
1                60320         Nordnet Fonder AB      Nordnet Sverige Index  SE0002756973                                                     OMXSBESGGI  2018-12-31  2026-06-30  0.957740    8.0   259.0         True        True
2                52163  Swedbank Robur Fonder AB  Swedbank Robur Access Mix  SE0000434359  OMRX Bond All 50.00; OMX Stockholm Benchmark Cap Gross 50.00;  2018-12-31  2026-06-30  0.815516    8.0   259.0         True        True
```

### data/senastedata/output/nettrading_omxsb.csv  (75.9 kB)
- rows: 259  cols: 25
- columns (dtype):
    - `event_id` (object)
    - `company` (object)
    - `RIC` (object)
    - `type` (object)
    - `AD` (object)
    - `ED` (object)
    - `period` (object)
    - `qb` (object)
    - `qa` (object)
    - `isins` (object)
    - `f` (float64)
    - `shares_qa` (float64)
    - `idx_b` (float64)
    - `idx_a` (float64)
    - `all_b` (float64)
    - `all_a` (float64)
    - `act_b` (float64)
    - `act_a` (float64)
    - `nt` (float64)
    - `instbuy` (float64)
    - `activebuy` (float64)
    - `indexown` (float64)
    - `n_idx_funds_b` (int64)
    - `n_idx_funds_a` (int64)
    - `tot` (float64)
- id-like uniques:
    - `event_id`: 259 unique (nulls 0)
    - `company`: 165 unique (nulls 0)
    - `RIC`: 112 unique (nulls 0)
    - `isins`: 112 unique (nulls 0)
    - `n_idx_funds_b`: 14 unique (nulls 0)
    - `n_idx_funds_a`: 15 unique (nulls 0)
- first 3 rows:
```
          event_id                              company           RIC      type          AD          ED     period          qb          qa         isins    f    shares_qa     idx_b      idx_a        all_b        all_a        act_b        act_a        nt   instbuy  activebuy  indexown  n_idx_funds_b  n_idx_funds_a        tot
0  OMXSB-2019H1-01                      Bilia AB ser. A      BILIa.ST  addition  2019-05-13  2019-06-03  2018–2020  2019-03-31  2019-06-30  SE0009921588  1.0  100950952.0  138462.0  1355258.0    7842377.0    8974981.0    7703915.0    7619723.0  1.205334  1.121935  -0.083399  0.137158              3             14   2.567176
1  OMXSB-2019H1-02  International Petroleum Corporation      IPCOR.ST  addition  2019-05-13  2019-06-03  2018–2020  2019-03-31  2019-06-30  CA46016U1084  1.0  163720065.0       0.0   747567.0    2419310.0    3775252.0    2419310.0    3027685.0  0.456613  0.828208   0.371595  0.000000              0              4 -11.625967
2  OMXSB-2019H1-03                    Klovern AB Ser. B  KLOVb.ST^G21  addition  2019-05-13  2019-06-03  2018–2020  2019-03-31  2019-06-30  SE0006593919  1.0  751729436.0   51171.0  8564395.0  117795941.0  123244301.0  117744770.0  114679906.0  1.132485  0.724777  -0.407708  0.006807              1             14  11.034816
```

### data/senastedata/output/fi_holdings_long.csv.gz  (106.22 MB)
- rows: 3,064,860  cols: 17
- columns (dtype):
    - `Tillgångsslag_enligt_LVF_5_kap` (object)
    - `Instrumentnamn` (object)
    - `ISIN-kod_instrument` (object)
    - `Landkod_Emittent` (object)
    - `Valuta` (object)
    - `Antal` (float64)
    - `Kurs_som_använts_vid_värdering_av_instrumentet` (float64)
    - `Marknadsvärde_instrument` (float64)
    - `Andel_av_fondförmögenhet_instrument` (float64)
    - `Kvartalsslut` (object)
    - `Fondbolag_namn` (object)
    - `Fond_institutnummer` (int64)
    - `Fond_namn` (object)
    - `Fond_ISIN-kod` (object)
    - `Fondförmögenhet` (int64)
    - `Jämförelseindex` (object)
    - `zip` (object)
- id-like uniques:
    - `ISIN-kod_instrument`: 45,709 unique (nulls 112,119)
    - `Andel_av_fondförmögenhet_instrument`: 3,697 unique (nulls 0)
    - `Fondbolag_namn`: 74 unique (nulls 0)
    - `Fond_institutnummer`: 886 unique (nulls 0)
    - `Fond_namn`: 1,241 unique (nulls 0)
    - `Fond_ISIN-kod`: 937 unique (nulls 0)
    - `Fondförmögenhet`: 19,283 unique (nulls 0)
- first 3 rows:
```
  Tillgångsslag_enligt_LVF_5_kap                 Instrumentnamn ISIN-kod_instrument Landkod_Emittent Valuta      Antal  Kurs_som_använts_vid_värdering_av_instrumentet  Marknadsvärde_instrument  Andel_av_fondförmögenhet_instrument Kvartalsslut                Fondbolag_namn  Fond_institutnummer             Fond_namn Fond_ISIN-kod  Fondförmögenhet                 Jämförelseindex                                      zip
0         ÖverlåtbartVärdepapper           TRANSMISSORA ALIANCA        BRTAEECDAM10               BR    BRL   422600.0                                           23.60               22814276.93                                 2.99   2018-12-31  SEB Investment Management AB                51403  SEB Latinamerikafond  SE0000433138        762226815  MSCI Latin America 10/40 Index  Fondinnehav_2018Q4_2022-11-16 17.05.zip
1         ÖverlåtbartVärdepapper  Fibra Uno Administracion REIT        MXCFFU000001               MX    MXN  1823700.0                                           21.84               17930743.43                                 2.35   2018-12-31  SEB Investment Management AB                51403  SEB Latinamerikafond  SE0000433138        762226815  MSCI Latin America 10/40 Index  Fondinnehav_2018Q4_2022-11-16 17.05.zip
2         ÖverlåtbartVärdepapper                          Ambev        BRABEVACNOR1               BR    BRL    88041.0                                           15.38                3097465.77                                 0.41   2018-12-31  SEB Investment Management AB                51403  SEB Latinamerikafond  SE0000433138        762226815  MSCI Latin America 10/40 Index  Fondinnehav_2018Q4_2022-11-16 17.05.zip
```

### data/senastedata/output/numbers.json  (0.7 kB)
- JSON content (first 1500 chars):
```
{
  "car_tot_addition_2013–2017": 2.213,
  "car_tot_addition_2018–2020": 2.348,
  "car_tot_addition_2021–2023": 0.505,
  "car_tot_addition_2024–2026": 2.67,
  "car_tot_deletion_2013–2017": -5.485,
  "car_tot_deletion_2018–2020": 1.126,
  "car_tot_deletion_2021–2023": -1.454,
  "car_tot_deletion_2024–2026": -2.691,
  "eta_all_addition": -0.605,
  "eta_all_deletion": -0.974,
  "events_dropped": 14,
  "events_part5": 259,
  "events_raw": 394,
  "events_sample": 380,
  "events_with_nettrading": 253,
  "fig3_slope_addition": 1.72,
  "fig3_slope_deletion": 3.577,
  "indexown_median_additions": 0.0,
  "n_index_funds": 14,
  "t3_N_additions": 189,
  "t3_N_deletions": 155,
  "volume_share_EDm1_mean": 13.52
}
```

### data/senastedata/output/tables/tabA_01_car_omxsgi_long.csv  (4.5 kB)
- rows: 30  cols: 11
- columns (dtype):
    - `type` (object)
    - `window` (object)
    - `period` (object)
    - `mean` (float64)
    - `se_hc1` (float64)
    - `p_hc1` (float64)
    - `se_cr1` (float64)
    - `p_cr1` (float64)
    - `p_wcb` (float64)
    - `N` (int64)
    - `G` (int64)
- first 3 rows:
```
       type  window     period      mean    se_hc1     p_hc1    se_cr1     p_cr1     p_wcb   N   G
0  addition  ann_gi  2013–2017  1.850789  0.636157  0.003622  0.712495  0.028851  0.013701  57  10
1  addition  ann_gi  2018–2020 -1.205079  0.872056  0.167008  1.422805  0.435663  0.967497  51   6
2  addition  ann_gi  2021–2023  0.639015  0.853871  0.454234  0.882846  0.501616  0.440644  59   6
```

### data/senastedata/output/tables/tabA_02_isin_matches.csv  (11.7 kB)
- rows: 139  cols: 7
- columns (dtype):
    - `Event` (object)
    - `Company` (object)
    - `LSEG ISIN` (object)
    - `Matched name` (object)
    - `Added ISIN` (object)
    - `Dominant name of added ISIN` (object)
    - `Rows` (int64)
- id-like uniques:
    - `Event`: 88 unique (nulls 0)
    - `Company`: 57 unique (nulls 0)
    - `LSEG ISIN`: 38 unique (nulls 3)
    - `Matched name`: 43 unique (nulls 0)
    - `Added ISIN`: 65 unique (nulls 0)
    - `Dominant name of added ISIN`: 44 unique (nulls 0)
- first 3 rows:
```
             Event                     Company     LSEG ISIN      Matched name    Added ISIN Dominant name of added ISIN  Rows
0  OMXSB-2019H1-06                   Nyfosa AB           NaN            NYFOSA  SE0011426428                      NYFOSA  1883
1  OMXSB-2019H1-07  Atrium Ljungberg AB ser. B  SE0024320832  ATRIUM LJUNGBERG  SE0000191827          ATRIUM LJUNGBERG B   561
2  OMXSB-2019H1-11              Karo Pharma AB  SE0007464888          KARO BIO  SE0017767148                    KARO BIO     3
```

### data/senastedata/output/tables/tabA_03_index_funds.csv  (1.0 kB)
- rows: 14  cols: 5
- columns (dtype):
    - `Fund company` (object)
    - `Fund` (object)
    - `Match share` (float64)
    - `Years` (float64)
    - `Events` (float64)
- date-like ranges:
    - `Years`: 8.0 → 8.0
- id-like uniques:
    - `Fund company`: 5 unique (nulls 0)
    - `Fund`: 14 unique (nulls 0)
    - `Events`: 1 unique (nulls 0)
- first 3 rows:
```
               Fund company                       Fund  Match share  Years  Events
0           Nordea Funds Ab      Nordea Sverige Passiv        0.967    8.0   259.0
1         Nordnet Fonder AB      Nordnet Sverige Index        0.958    8.0   259.0
2  Swedbank Robur Fonder AB  Swedbank Robur Access Mix        0.816    8.0   259.0
```

### data/senastedata/output/tables/tabA_04_split_factors.csv  (0.4 kB)
- rows: 3  cols: 10
- columns (dtype):
    - `Event` (object)
    - `Company` (object)
    - `Quarter before` (object)
    - `Quarter after` (object)
    - `FI price before` (float64)
    - `FI price after` (float64)
    - `Adjusted close before` (float64)
    - `Adjusted close after` (float64)
    - `Raw factor` (float64)
    - `Factor used` (float64)
- date-like ranges:
    - `Quarter before`: 2020-09-30 00:00:00 → 2022-03-31 00:00:00
    - `Quarter after`: 2020-12-31 00:00:00 → 2022-06-30 00:00:00
- id-like uniques:
    - `Event`: 3 unique (nulls 0)
    - `Company`: 3 unique (nulls 0)
    - `FI price before`: 3 unique (nulls 0)
    - `FI price after`: 3 unique (nulls 0)
- first 3 rows:
```
             Event                    Company Quarter before Quarter after  FI price before  FI price after  Adjusted close before  Adjusted close after  Raw factor  Factor used
0  OMXSB-2020H2-10          Lagercrantz Group     2020-09-30    2020-12-31            181.0            76.0              60.333273                  76.0    3.000003          3.0
1  OMXSB-2022H1-01    Addnode Group AB ser. B     2022-03-31    2022-06-30            385.5            83.4              96.375000                  83.4    4.000000          4.0
2  OMXSB-2022H1-04  Heba Fastighets AB ser. B     2022-03-31    2022-06-30            151.6            41.8              75.800000                  41.8    2.000000          2.0
```

### data/senastedata/output/tables/tabA_05_dropped_events.csv  (1.6 kB)
- rows: 14  cols: 7
- columns (dtype):
    - `Event` (object)
    - `Company` (object)
    - `Type` (object)
    - `ED` (object)
    - `First trading day` (object)
    - `Last trading day` (object)
    - `Reason` (object)
- date-like ranges:
    - `First trading day`: 2012-01-02 00:00:00 → 2025-03-27 00:00:00
    - `Last trading day`: 2019-03-06 00:00:00 → 2026-10-14 00:00:00
- id-like uniques:
    - `Event`: 14 unique (nulls 0)
    - `Company`: 14 unique (nulls 0)
- first 3 rows:
```
             Event                 Company       Type          ED First trading day Last trading day                            Reason
0  OMXSB-2014H1-02  Hemfosa Fastigheter AB  Additions  2014-06-02        2014-03-21       2020-01-31  Listed within 100 days before ED
1  OMXSB-2016H2-01              Ahlsell AB  Additions  2016-12-01        2016-10-28       2019-03-06  Listed within 100 days before ED
2  OMXSB-2017H1-01                Ambea AB  Additions  2017-06-01        2017-03-31       2026-10-14  Listed within 100 days before ED
```

### data/senastedata/output/tables/tabA_06_event_chain.csv  (0.3 kB)
- rows: 8  cols: 2
- columns (dtype):
    - `Step` (object)
    - `N` (int64)
- first 3 rows:
```
                              Step    N
0            Events in source file  394
1   After listing/delisting filter  380
2  With cumulative abnormal return  380
```

### data/senastedata/output/tables/tab_01_sample.csv  (0.2 kB)
- rows: 7  cols: 5
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Before filter` (object)
    - `Before filter.1` (object)
    - `After filter` (object)
    - `After filter.1` (object)
- id-like uniques:
    - `Unnamed: 0`: 6 unique (nulls 1)
- first 3 rows:
```
  Unnamed: 0 Before filter Before filter.1 After filter After filter.1
0        NaN     Additions       Deletions    Additions      Deletions
1     Period           NaN             NaN          NaN            NaN
2  2013–2017            60              36           57             36
```

### data/senastedata/output/tables/tab_02_car.csv  (1.6 kB)
- rows: 10  cols: 8
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `2013–2017` (object)
    - `2018–2020` (object)
    - `2021–2023` (object)
    - `2024–2026` (object)
    - `Last − previous` (object)
    - `F, equal means` (object)
- id-like uniques:
    - `Unnamed: 0`: 2 unique (nulls 0)
    - `Unnamed: 1`: 5 unique (nulls 0)
- first 3 rows:
```
           Unnamed: 0                        Unnamed: 1                         2013–2017                         2018–2020                       2021–2023                        2024–2026                Last − previous F, equal means
0  Panel A: Additions  Announcement window [AD−1, AD+1]  1.78***\n(0.64)\n[0.75]\n{0.023}    -1.35\n(0.89)\n[1.57]\n{0.967}   0.55\n(0.86)\n[0.90]\n{0.562}  2.24**\n(1.09)\n[0.43]\n{0.065}  1.68\n(1.38)\n[0.96]\n{0.121}  2.67\n{0.068}
1  Panel A: Additions     Effective window [ED−1, ED+1]    -0.93\n(0.72)\n[0.96]\n{0.408}  1.73***\n(0.45)\n[0.30]\n{0.032}  -0.60\n(0.73)\n[0.55]\n{0.340}   -0.03\n(1.17)\n[0.83]\n{0.939}  0.57\n(1.38)\n[0.94]\n{0.629}  7.58\n{0.001}
2  Panel A: Additions         Total window [AD−1, ED+1]     2.21\n(1.43)\n[1.95]\n{0.288}     2.35\n(1.56)\n[0.88]\n{0.032}   0.51\n(1.01)\n[0.71]\n{0.535}    2.67\n(1.88)\n[0.68]\n{0.065}  2.16\n(2.13)\n[0.94]\n{0.058}  2.07\n{0.129}
```

### data/senastedata/output/tables/tab_02_car_long.csv  (4.9 kB)
- rows: 36  cols: 11
- columns (dtype):
    - `type` (object)
    - `window` (object)
    - `period` (object)
    - `mean` (float64)
    - `se_hc1` (float64)
    - `p_hc1` (float64)
    - `se_cr1` (float64)
    - `p_cr1` (float64)
    - `p_wcb` (float64)
    - `N` (int64)
    - `G` (int64)
- first 3 rows:
```
       type window     period      mean    se_hc1     p_hc1    se_cr1     p_cr1     p_wcb   N   G
0  addition    ann  2013–2017  1.782657  0.640621  0.005391  0.748973  0.041219  0.023302  57  10
1  addition    ann  2018–2020 -1.353202  0.887200  0.127196  1.567212  0.427360  0.967497  51   6
2  addition    ann  2021–2023  0.552052  0.855900  0.518930  0.901813  0.567198  0.562456  59   6
```

### data/senastedata/output/tables/tab_03_determinants_long.csv  (2.6 kB)
- rows: 22  cols: 9
- columns (dtype):
    - `model` (int64)
    - `var` (object)
    - `coef` (float64)
    - `se_hc1` (float64)
    - `p_hc1` (float64)
    - `se_cr1` (float64)
    - `N` (int64)
    - `G` (int64)
    - `r2` (float64)
- first 3 rows:
```
   model        var      coef    se_hc1     p_hc1    se_cr1    N   G        r2
0      1  2013–2017  2.213219  1.430445  0.121809  1.901836  212  27  0.006724
1      1  2018–2020  2.348216  1.559481  0.132127  0.822977  212  27  0.006724
2      1  2021–2023  0.505315  1.011795  0.617480  0.665291  212  27  0.006724
```

### data/senastedata/output/tables/tab_04_institutions.csv  (0.9 kB)
- rows: 18  cols: 6
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Index funds` (float64)
    - `All funds` (float64)
    - `Non-index funds` (float64)
    - `N` (int64)
- id-like uniques:
    - `Unnamed: 0`: 2 unique (nulls 0)
    - `Unnamed: 1`: 9 unique (nulls 0)
    - `Index funds`: 18 unique (nulls 0)
    - `All funds`: 18 unique (nulls 0)
    - `Non-index funds`: 18 unique (nulls 0)
- first 3 rows:
```
           Unnamed: 0 Unnamed: 1  Index funds  All funds  Non-index funds   N
0  Panel A: Additions       2019        0.927      0.885            0.118  10
1  Panel A: Additions       2020        1.120      1.718            0.507  25
2  Panel A: Additions       2021        0.818      1.007            0.001  17
```

### data/senastedata/output/tables/tab_05_elasticity.csv  (1.5 kB)
- rows: 16  cols: 10
- columns (dtype):
    - `Unnamed: 0` (int64)
    - `panel` (object)
    - `period` (object)
    - `N` (int64)
    - `G` (int64)
    - `mean_nt` (float64)
    - `mean_tot` (float64)
    - `eta` (float64)
    - `ci_lo` (float64)
    - `ci_hi` (float64)
- id-like uniques:
    - `Unnamed: 0`: 16 unique (nulls 0)
- first 3 rows:
```
   Unnamed: 0               panel     period   N  G  mean_nt  mean_tot     eta    ci_lo    ci_hi
0           0  Panel A: Additions  2018–2020  34  4   1.1002    2.3517 -0.4678  -1.5695  -0.2006
1           1  Panel A: Additions  2021–2023  58  6   0.8421    0.5750 -1.4646 -10.9523  15.1496
2           2  Panel A: Additions  2024–2026  45  5   1.2225    2.6702 -0.4578  -0.8211  -0.2951
```

### data/senastedata/output/tables/tab_05_elasticity_long.csv  (2.4 kB)
- rows: 16  cols: 9
- columns (dtype):
    - `panel` (object)
    - `period` (object)
    - `N` (int64)
    - `G` (int64)
    - `mean_nt` (float64)
    - `mean_tot` (float64)
    - `eta` (float64)
    - `ci_lo` (float64)
    - `ci_hi` (float64)
- first 3 rows:
```
                panel     period   N  G   mean_nt  mean_tot       eta      ci_lo      ci_hi
0  Panel A: Additions  2018–2020  34  4  1.100151  2.351692 -0.467813  -1.569496  -0.200621
1  Panel A: Additions  2021–2023  58  6  0.842107  0.574991 -1.464558 -10.952293  15.149555
2  Panel A: Additions  2024–2026  45  5  1.222547  2.670207 -0.457847  -0.821091  -0.295126
```

### data/senastedata/output/tables/tab_06_volume_share.csv  (0.5 kB)
- rows: 8  cols: 8
- columns (dtype):
    - `Unnamed: 0` (int64)
    - `type` (object)
    - `period` (object)
    - `N` (int64)
    - `share_EDm1` (float64)
    - `share_ED` (float64)
    - `share_EDp1` (float64)
    - `avg_other_day` (float64)
- date-like ranges:
    - `avg_other_day`: 1.8814 → 2.0208
- id-like uniques:
    - `Unnamed: 0`: 8 unique (nulls 0)
- first 3 rows:
```
   Unnamed: 0      type     period   N  share_EDm1  share_ED  share_EDp1  avg_other_day
0           0  addition  2013–2017  57     13.4911    2.3084      2.0412         1.9582
1           1  addition  2018–2020  51     12.2248    2.4476      2.1810         1.9844
2           2  addition  2021–2023  59     13.5669    2.6824      2.2324         1.9477
```

### data/senastedata/output/figures/fig_01_nettrading.csv  (0.3 kB)
- rows: 8  cols: 5
- columns (dtype):
    - `year` (int64)
    - `mean Additions` (float64)
    - `mean Deletions` (float64)
    - `size Additions` (int64)
    - `size Deletions` (int64)
- date-like ranges:
    - `year`: 2019 → 2026
- first 3 rows:
```
   year  mean Additions  mean Deletions  size Additions  size Deletions
0  2019           0.889          -0.646              10              14
1  2020           1.188          -0.671              25              13
2  2021           0.933          -0.894              17              16
```

### data/senastedata/output/figures/fig_03_scatter.csv  (0.2 kB)
- rows: 2  cols: 7
- columns (dtype):
    - `type` (object)
    - `a` (float64)
    - `c` (float64)
    - `se_c_hc1` (float64)
    - `p_c_hc1` (float64)
    - `r2` (float64)
    - `N` (int64)
- first 3 rows:
```
       type         a         c  se_c_hc1   p_c_hc1        r2    N
0  addition -0.069542  1.720163  1.253406  0.169942  0.008346  137
1  deletion  2.625883  3.576713  0.969060  0.000223  0.105322  116
```

### data/senastedata/output/figures/fig_08_car_announcement.csv  (17.4 kB)
- rows: 112  cols: 9
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `addition` (object)
    - `addition.1` (object)
    - `addition.2` (object)
    - `addition.3` (object)
    - `deletion` (object)
    - `deletion.1` (object)
    - `deletion.2` (object)
    - `deletion.3` (object)
- id-like uniques:
    - `Unnamed: 0`: 111 unique (nulls 1)
- first 3 rows:
```
   Unnamed: 0            addition          addition.1            addition.2          addition.3             deletion           deletion.1            deletion.2            deletion.3
0         NaN           2013–2017           2018–2020             2021–2023           2024–2026            2013–2017            2018–2020             2021–2023             2024–2026
1      -100.0  0.6363654062570995  0.7122202686089218  -0.24259473637386117  -0.057441043048921  -0.2944962815789146  -0.8784441645551478   -0.7811351136095046  0.038433256742131765
2       -99.0  0.7607530964095364  0.6213888487388153     0.680884668264405  0.5537467479916122  -0.8356607373134336  -1.1351906461126091  -0.16191809189446163   0.25776741074160686
```

### data/senastedata/output/figures/fig_09_car_effective.csv  (16.3 kB)
- rows: 103  cols: 9
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `addition` (object)
    - `addition.1` (object)
    - `addition.2` (object)
    - `addition.3` (object)
    - `deletion` (object)
    - `deletion.1` (object)
    - `deletion.2` (object)
    - `deletion.3` (object)
- id-like uniques:
    - `Unnamed: 0`: 102 unique (nulls 1)
- first 3 rows:
```
   Unnamed: 0             addition           addition.1            addition.2            addition.3              deletion           deletion.1           deletion.2           deletion.3
0         NaN            2013–2017            2018–2020             2021–2023             2024–2026             2013–2017            2018–2020            2021–2023            2024–2026
1        -1.0                  0.0                  0.0                   0.0                   0.0                   0.0                  0.0                  0.0                  0.0
2         0.0  -0.5777016256445827  0.34408820574176446  -0.06640979588321715  -0.28993836518582466  -0.05595426981947735  0.06897168771124927  0.14618786857339566  0.19332847626024605
```

### data/senastedata/output/figures/fig_10_size_rank.csv  (0.9 kB)
- rows: 14  cols: 5
- columns (dtype):
    - `year` (int64)
    - `mean` (float64)
    - `q25` (float64)
    - `q75` (float64)
    - `N` (int64)
- date-like ranges:
    - `year`: 2013 → 2026
- first 3 rows:
```
   year       mean        q25        q75   N
0  2013  77.059155  73.477930  85.502283   8
1  2014  74.459610  67.219917  85.892116   7
2  2015  85.408134  80.600740  90.937773  11
```

### data/senastedata/output/figures/fig_11_volume.csv  (7.0 kB)
- rows: 46  cols: 9
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `addition` (object)
    - `addition.1` (object)
    - `addition.2` (object)
    - `addition.3` (object)
    - `deletion` (object)
    - `deletion.1` (object)
    - `deletion.2` (object)
    - `deletion.3` (object)
- id-like uniques:
    - `Unnamed: 0`: 45 unique (nulls 1)
- first 3 rows:
```
   Unnamed: 0            addition          addition.1          addition.2          addition.3            deletion          deletion.1          deletion.2         deletion.3
0         NaN           2013–2017           2018–2020           2021–2023           2024–2026           2013–2017           2018–2020           2021–2023          2024–2026
1       -22.0  1.6257686989589277  1.6652911483744242  2.0924257371549864  2.3792595765828923  1.5143038756719434  1.6776565631412137  2.3486949595100266  2.485384237838481
2       -21.0   1.770803164629352  2.4376436408398328   2.136359860063478  1.5464928480510167  1.6089765346053475  2.5580624212056056  2.2197664681823137  1.713811599117045
```

### data/derived/ftn_2026-10-11/bids_long.csv  (111.2 kB)
- rows: 290  cols: 53
- columns (dtype):
    - `round` (object)
    - `category` (object)
    - `announce_date` (object)
    - `bid_deadline` (object)
    - `award_date` (object)
    - `n_bids_reported` (int64)
    - `n_qualified_reported` (int64)
    - `bid_no` (int64)
    - `manager` (object)
    - `fund_name` (object)
    - `winner` (int64)
    - `qualified` (float64)
    - `on_ppm_at_announce` (int64)
    - `incumbent_in_category` (int64)
    - `new_to_platform` (float64)
    - `report_marks_new` (float64)
    - `manager_swedish` (int64)
    - `ppm_fondnr_at_announce` (float64)
    - `ppm_isin_at_announce` (object)
    - `ppm_kategori_at_announce` (object)
    - `ppm_fondnr_any` (object)
    - `ppm_isins` (object)
    - `shof_fundid` (object)
    - `shof_match` (object)
    - `match_approx` (int64)
    - `perfid` (object)
    - `end_ym_announce` (object)
    - `end_ym_deadline` (object)
    - `ret12_ann` (float64)
    - `ret36_ann` (float64)
    - `ret12_dl` (float64)
    - `ret36_dl` (float64)
    - `ppm_ret12` (float64)
    - `ppm_ret36` (float64)
    - `ret12_src` (object)
    - `ret12_ann_filled` (float64)
    - `ret36_ann_filled` (float64)
    - `pct12_ann_filled` (float64)
    - `pct36_ann_filled` (float64)
    - `pct12_ann` (float64)
    - `pct36_ann` (float64)
    - `pct12_dl` (float64)
    - `pct36_dl` (float64)
    - `tna_fund_ccy` (float64)
    - `tna_ccy` (object)
    - `tna_fund_msek` (float64)
    - `log_tna_msek` (float64)
    - `size_pct` (float64)
    - `ppm_fee_net` (float64)
    - `ppm_fee_gross` (float64)
    - `ppm_capital_msek` (float64)
    - `post_award_months` (float64)
    - `post_award_last_ym` (object)
- date-like ranges:
    - `announce_date`: 2023-06-30 00:00:00 → 2025-10-28 00:00:00
    - `award_date`: 2024-03-25 00:00:00 → 2026-09-22 00:00:00
    - `on_ppm_at_announce`: 0 → 1
    - `ppm_fondnr_at_announce`: 103606.0 → 989491.0
    - `end_ym_announce`: 2023-06-01 00:00:00 → 2025-09-01 00:00:00
    - `end_ym_deadline`: 2023-09-01 00:00:00 → 2025-11-01 00:00:00
    - `ret12_ann`: -0.1574089160479012 → 0.3765192360451386
    - `ret36_ann`: -0.2382919346486802 → 1.2172408272141937
    - `ret12_dl`: -0.1303620051798349 → 0.4001382824795696
    - `ppm_ret12`: -0.16 → 0.38
    - `ret12_ann_filled`: -0.1574089160479012 → 0.3765192360451386
    - `ret36_ann_filled`: -0.2382919346486802 → 1.2172408272141937
    - `pct12_ann_filled`: 0.0303030303030303 → 1.0
    - `pct36_ann_filled`: 0.0303030303030303 → 1.0
    - `pct12_ann`: 0.0303030303030303 → 1.0
    - `pct36_ann`: 0.03125 → 1.0
    - `pct12_dl`: 0.0303030303030303 → 1.0
    - `post_award_months`: 0.0 → 30.0
    - `post_award_last_ym`: 2026-07-01 00:00:00 → 2026-09-01 00:00:00
- id-like uniques:
    - `fund_name`: 290 unique (nulls 0)
    - `ppm_fondnr_at_announce`: 113 unique (nulls 176)
    - `ppm_isin_at_announce`: 113 unique (nulls 176)
    - `ppm_fondnr_any`: 133 unique (nulls 156)
    - `ppm_isins`: 133 unique (nulls 156)
    - `shof_fundid`: 258 unique (nulls 31)
    - `perfid`: 147 unique (nulls 142)
    - `tna_fund_ccy`: 141 unique (nulls 149)
    - `tna_fund_msek`: 141 unique (nulls 149)
- first 3 rows:
```
           round       category announce_date bid_deadline  award_date  n_bids_reported  n_qualified_reported  bid_no                            manager                                        fund_name  winner  qualified  on_ppm_at_announce  incumbent_in_category  new_to_platform  report_marks_new  manager_swedish  ppm_fondnr_at_announce ppm_isin_at_announce ppm_kategori_at_announce ppm_fondnr_any                  ppm_isins shof_fundid shof_match  match_approx      perfid end_ym_announce end_ym_deadline  ret12_ann  ret36_ann  ret12_dl  ret36_dl  ppm_ret12  ppm_ret36 ret12_src  ret12_ann_filled  ret36_ann_filled  pct12_ann_filled  pct36_ann_filled  pct12_ann  pct36_ann  pct12_dl  pct36_dl  tna_fund_ccy tna_ccy  tna_fund_msek  log_tna_msek  size_pct  ppm_fee_net  ppm_fee_gross  ppm_capital_msek  post_award_months post_award_last_ym
0  R01_EU_active  Europe active    2023-06-30   2023-10-05  2024-03-25               35                    12       1      ABN AMRO Investment Solutions  ABN AMRO EdenTree European Sustainable Equities       0        NaN                   0                      0              NaN               NaN                0                     NaN                  NaN                      NaN            NaN                        NaN  FS0000D1XC      fuzzy             0         NaN         2023-06         2023-09        NaN        NaN       NaN       NaN        NaN        NaN       NaN               NaN               NaN               NaN               NaN        NaN        NaN       NaN       NaN           NaN     NaN            NaN           NaN       NaN          NaN            NaN               NaN                0.0                NaN
1  R01_EU_active  Europe active    2023-06-30   2023-10-05  2024-03-25               35                    12       2  abrdn Investments Luxembourg S.A.                 European Sustainable Equity Fund       1        1.0                   1                      1              0.0               NaN                0                367698.0         LU0094541447                   Europa  367698;952770  LU0094541447;LU0231472209  FSGBR05845   ppm_isin             0  0P00000B5S         2023-06         2023-09   0.295895   0.346807  0.196185  0.185013        0.3       0.35      shof          0.295895          0.346807          0.642857          0.142857   0.642857   0.142857  0.214286  0.214286  2.433067e+08     EUR    2793.160951      7.934929  0.214286         0.55           1.69         17.454651               30.0            2026-09
2  R01_EU_active  Europe active    2023-06-30   2023-10-05  2024-03-25               35                    12       3      Allianz Global Investors GmbH             Allianz Europe Equity Growth- AT EUR       0        NaN                   0                      0              NaN               NaN                0                     NaN                  NaN                      NaN            NaN                        NaN  FSUSA07KTU      fuzzy             0  0P00006SRJ         2023-06         2023-09   0.348960   0.416595  0.292058  0.184860        NaN        NaN      shof          0.348960          0.416595          0.857143          0.214286   0.857143   0.214286  0.857143  0.142857  4.925726e+09     EUR   56547.330572     10.942833  1.000000          NaN            NaN               NaN               30.0            2026-09
```

### data/derived/ftn_2026-10-11/crosswalk_ppm_shof.csv  (71.4 kB)
- rows: 514  cols: 12
- columns (dtype):
    - `fondnr` (int64)
    - `isin_used` (object)
    - `match_method` (object)
    - `performanceid` (object)
    - `fundid` (object)
    - `fundname_ms` (object)
    - `status` (object)
    - `obsoletedate` (float64)
    - `currencyid` (object)
    - `pid_in_val` (object)
    - `fondnamn` (object)
    - `fundid_in_val` (bool)
- date-like ranges:
    - `obsoletedate`: nan → nan
- id-like uniques:
    - `fondnr`: 514 unique (nulls 0)
    - `isin_used`: 511 unique (nulls 0)
    - `performanceid`: 509 unique (nulls 2)
    - `fundid`: 499 unique (nulls 2)
    - `fundname_ms`: 499 unique (nulls 2)
    - `currencyid`: 5 unique (nulls 2)
    - `fondnamn`: 511 unique (nulls 0)
    - `fundid_in_val`: 2 unique (nulls 0)
- first 3 rows:
```
   fondnr     isin_used          match_method performanceid      fundid                fundname_ms  status  obsoletedate currencyid pid_in_val                     fondnamn  fundid_in_val
0  283408  SE0000538944  currencyspecificISIN    0P00000LCG  FSGBR05CRO  Swedbank Robur Technology  Active           NaN        SEK       True  Swedbank Robur Technology A           True
1  681783  SE0000739195  currencyspecificISIN    0P00000K12  FSGBR0532Z      AMF Aktiefond Sverige  Active           NaN        SEK       True        AMF Aktiefond Sverige           True
2  291906  SE0000428336  currencyspecificISIN    0P00000F01  FSGBR05353   Didner & Gerge Aktiefond  Active           NaN        SEK       True                D&G Aktiefond           True
```

### data/derived/ftn_2026-10-11/ftn_category_fees.csv  (1.4 kB)
- rows: 11  cols: 16
- columns (dtype):
    - `round` (object)
    - `category` (object)
    - `award_date` (object)
    - `fee_before_ew_after_rebate_s42` (float64)
    - `before_reference_date` (object)
    - `before_median` (float64)
    - `before_min` (float64)
    - `before_max` (float64)
    - `before_capweighted` (float64)
    - `fee_before_at_announcement_s62` (float64)
    - `fee_after_avg_procured_s62` (float64)
    - `fee_after_capweighted` (float64)
    - `pct_change_reported` (int64)
    - `n_winners` (int64)
    - `n_new_on_platform` (int64)
    - `note` (object)
- date-like ranges:
    - `award_date`: 2024-03-25 00:00:00 → 2026-09-22 00:00:00
    - `fee_before_at_announcement_s62`: 0.129 → 0.515
- first 3 rows:
```
  round       category  award_date  fee_before_ew_after_rebate_s42 before_reference_date  before_median  before_min  before_max  before_capweighted  fee_before_at_announcement_s62  fee_after_avg_procured_s62  fee_after_capweighted  pct_change_reported  n_winners  n_new_on_platform                                                     note
0    R1  Europe active  2024-03-25                           0.480           2023 (year)          0.510       0.140       0.680                0.27                           0.480                       0.210                    NaN                  -56          6                  3                                                      NaN
1    R2   Global index  2024-10-31                           0.143             Sept 2024          0.136       0.070       0.221                 NaN                           0.143                       0.046                    NaN                  -68          6                  3  summary says 68%; later reports cite 58% (0.143->0.046)
2    R2   Europe index  2024-10-31                           0.135             Sept 2024          0.121       0.119       0.143                 NaN                           0.135                       0.046                    NaN                  -66          4                  0                                                      NaN
```

### data/derived/ftn_2026-10-11/panel_nonppm_monthly.csv  (7.70 MB)
- rows: 35,328  cols: 26
- columns (dtype):
    - `fondnr` (int64)
    - `ym` (object)
    - `fundid` (object)
    - `performanceid` (object)
    - `tnafund` (float64)
    - `ccy_fund` (object)
    - `last_date` (object)
    - `nf_fund` (float64)
    - `ncls` (float64)
    - `mv_tot` (float64)
    - `handel_netto` (float64)
    - `kategori` (object)
    - `upphandlad` (object)
    - `valuta` (object)
    - `tri_sek` (float64)
    - `R` (float64)
    - `in_ppm` (bool)
    - `mv0` (float64)
    - `first_ppm` (object)
    - `A_tot_sek` (float64)
    - `A_np` (float64)
    - `A_np_l` (float64)
    - `ym_l` (object)
    - `flow_np` (float64)
    - `flow_np_alt` (float64)
    - `ppm_share` (float64)
- date-like ranges:
    - `ym`: 2021-01-01 00:00:00 → 2026-09-01 00:00:00
    - `last_date`: 2021-01-29 00:00:00 → 2026-09-30 00:00:00
    - `first_ppm`: 2022-01-01 00:00:00 → 2026-08-01 00:00:00
    - `ym_l`: 2021-01-01 00:00:00 → 2026-08-01 00:00:00
- id-like uniques:
    - `fondnr`: 512 unique (nulls 0)
    - `fundid`: 499 unique (nulls 0)
    - `performanceid`: 509 unique (nulls 0)
    - `tnafund`: 31,346 unique (nulls 2,964)
    - `ccy_fund`: 13 unique (nulls 2,964)
    - `nf_fund`: 14,849 unique (nulls 2,964)
- first 3 rows:
```
   fondnr       ym      fundid performanceid       tnafund ccy_fund   last_date       nf_fund  ncls  mv_tot  handel_netto kategori upphandlad valuta     tri_sek         R  in_ppm  mv0 first_ppm     A_tot_sek  A_np  A_np_l     ym_l  flow_np  flow_np_alt  ppm_share
0  103606  2021-01  FSGBR05BQA    0P00000FYK  5.974146e+09      SEK  2021-01-29  2.800879e+07   1.0     NaN           NaN      NaN        NaN    NaN  1827.06670       NaN   False  NaN   2022-01  5.974146e+09   NaN     NaN      NaN      NaN          NaN        NaN
1  103606  2021-02  FSGBR05BQA    0P00000FYK  6.227616e+09      SEK  2021-02-26 -1.187573e+07   1.0     NaN           NaN      NaN        NaN    NaN  1908.20985  0.044412   False  NaN   2022-01  6.227616e+09   NaN     NaN  2021-01      NaN          NaN        NaN
2  103606  2021-03  FSGBR05BQA    0P00000FYK  6.515350e+09      SEK  2021-03-31  7.732163e+06   1.0     NaN           NaN      NaN        NaN    NaN  1993.94369  0.044929   False  NaN   2022-01  6.515350e+09   NaN     NaN  2021-02      NaN          NaN        NaN
```

### data/derived/ftn_2026-10-11/ppm_panel_2022_2026.csv  (6.22 MB)
- rows: 24,554  cols: 25
- columns (dtype):
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `val_k` (int64)
    - `val_m` (int64)
    - `val_tot` (int64)
    - `mv_k` (float64)
    - `mv_m` (float64)
    - `mv_tot` (float64)
    - `handel_netto` (float64)
    - `kategori` (object)
    - `fondtyp` (object)
    - `forvaltare` (object)
    - `svensk` (object)
    - `forvaltning` (object)
    - `upphandlad` (object)
    - `ret_ytd` (float64)
    - `ret_1m` (float64)
    - `ret_12m` (float64)
    - `ret_36m` (float64)
    - `fee_net` (float64)
    - `fee_gross` (float64)
    - `valuta` (object)
    - `startdatum` (object)
    - `isin` (object)
    - `date` (object)
- date-like ranges:
    - `startdatum`: 2000-07-05 → 2026-08-18
    - `date`: 2022-01-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `fondnr`: 520 unique (nulls 0)
    - `fondnamn`: 639 unique (nulls 0)
    - `fondtyp`: 7 unique (nulls 0)
    - `isin`: 518 unique (nulls 224)
- first 3 rows:
```
   fondnr                                           fondnamn    val_k    val_m  val_tot          mv_k          mv_m        mv_tot  handel_netto                        kategori              fondtyp                forvaltare  svensk forvaltning upphandlad  ret_ytd  ret_1m  ret_12m  ret_36m  fee_net  fee_gross valuta           startdatum          isin        date
0       1  AP7 Såfa - Statens årskullsförvaltningsalternativ  2516740  2785621  5302361  3.842721e+11  4.737519e+11  8.580240e+11           NaN  Statens förvaltningsalternativ    Generationsfonder          Sjunde AP-fonden  Svensk         NaN        NaN      NaN     NaN      NaN      NaN      NaN        NaN    NaN                  NaN           NaN  2022-12-31
1  283408                        Swedbank Robur Technology A   145732   171935   317667  2.284296e+10  3.232936e+10  5.517232e+10  3.795735e+08            IT och kommunikation        Branschfonder  Swedbank Robur Fonder AB  Svensk         NaN        NaN    -21.0    -5.0    -21.0     54.0     0.23       1.25    SEK  2000-07-05 00:00:00  SE0000538944  2022-12-31
2  681783                              AMF Aktiefond Sverige    93148    96798   189946  1.020117e+10  1.319114e+10  2.339231e+10  2.350652e+08                         Sverige  Svenska Aktiefonder             AMF Fonder AB  Svensk         NaN        NaN    -28.0    -3.0    -28.0     13.0     0.14       0.40    SEK  2000-07-05 00:00:00  SE0000739195  2022-12-31
```

### data/derived/ftn_2026-10-11/reallocation_losers.csv  (17.2 kB)
- rows: 78  cols: 21
- columns (dtype):
    - `round` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `exited` (bool)
    - `last_month` (object)
    - `avslutsdatum` (object)
    - `move_start` (object)
    - `n_tranche_months` (int64)
    - `months_award_to_move` (int64)
    - `mv_award` (float64)
    - `val_award` (int64)
    - `vol_out` (float64)
    - `vol_out_exDec` (float64)
    - `dec_hn_pre` (float64)
    - `default_mv` (float64)
    - `val_at_move` (int64)
    - `val_last` (int64)
    - `mv_last` (float64)
    - `hn_tranche_months` (float64)
    - `sav_vol` (int64)
    - `pct_vol_cap` (float64)
- date-like ranges:
    - `last_month`: 2024-05-31 00:00:00 → 2026-08-31 00:00:00
    - `avslutsdatum`: 2024-06-14 00:00:00 → 2026-06-24 00:00:00
    - `move_start`: 2024-06-30 00:00:00 → 2026-09-30 00:00:00
    - `n_tranche_months`: 0 → 10
    - `months_award_to_move`: 3 → 6
    - `val_last`: 1 → 95182
    - `mv_last`: 33161.45428288 → 3515294527.81479
    - `hn_tranche_months`: -20068538527.44 → 0.0
- id-like uniques:
    - `fondnr`: 78 unique (nulls 0)
    - `fondnamn`: 78 unique (nulls 0)
- first 3 rows:
```
       round  fondnr                       fondnamn  exited  last_month avslutsdatum  move_start  n_tranche_months  months_award_to_move      mv_award  val_award     vol_out  vol_out_exDec  dec_hn_pre    default_mv  val_at_move  val_last       mv_last  hn_tranche_months  sav_vol  pct_vol_cap
0  EU_active  336826         BL - Equities Europe B    True  2024-05-31   2024-06-27  2024-06-30                 0                     3  6.988530e+08       7437   767455.54      767455.54         0.0  6.896811e+08         7379      7379  6.896811e+08               0.00       58     0.111153
1  EU_active  916122    BlackRock - Euro Markets A2    True  2024-06-30   2024-07-08  2024-06-30                 1                     3  8.969697e+07        904  9046178.37     9046178.37         0.0  7.945514e+07          843         1  3.849661e+04       -77415243.18       61    10.221519
2  EU_active  696898  BlackRock - European Value A2    True  2024-05-31   2024-07-05  2024-06-30                 0                     3  3.892773e+07        379  2003418.39     2003418.39         0.0  3.784657e+07          360       360  3.784657e+07               0.00       19     5.027400
```

### data/derived/ftn_2026-10-11/reallocation_summary_by_round.csv  (3.3 kB)
- rows: 19  cols: 14
- columns (dtype):
    - `round` (object)
    - `sample` (object)
    - `n_los` (int64)
    - `mv_award_bn` (float64)
    - `vol_bn` (float64)
    - `default_bn` (float64)
    - `pct_vol_cap` (float64)
    - `pct_vol_cap_exDec` (float64)
    - `sav_award` (int64)
    - `sav_vol` (int64)
    - `sav_default` (int64)
    - `pct_vol_sav` (float64)
    - `med_months_award_to_move` (float64)
    - `max_tranche_months` (float64)
- date-like ranges:
    - `med_months_award_to_move`: 3.0 → 6.0
    - `max_tranche_months`: 0.0 → 10.0
- first 3 rows:
```
       round            sample  n_los  mv_award_bn    vol_bn  default_bn  pct_vol_cap  pct_vol_cap_exDec  sav_award  sav_vol  sav_default  pct_vol_sav  med_months_award_to_move  max_tranche_months
0  EU_active            exited     20     7.821017 -0.022810    7.967551    -0.287111          -0.287111      95310      689        94621     0.722904                       3.0                 1.0
1  EU_active  all_incl_pending     20     7.821017 -0.022810    7.967551    -0.287111          -0.287111      95310      689        94621     0.722904                       3.0                 1.0
2   EU_index            exited      3     0.688590  0.028812    0.697208     3.968457           4.834007       6999      465         6534     6.643806                       5.0                 0.0
```

### data/derived/ftn_2026-10-11/unmatched_for_lseg.csv  (27.3 kB)
- rows: 144  cols: 11
- columns (dtype):
    - `round` (object)
    - `bid_no` (int64)
    - `manager` (object)
    - `fund_name` (object)
    - `winner` (int64)
    - `on_ppm_at_announce` (int64)
    - `shof_fundid` (object)
    - `shof_fundname` (object)
    - `reason` (object)
    - `announce_date` (object)
    - `award_date` (object)
- date-like ranges:
    - `on_ppm_at_announce`: 0 → 0
    - `announce_date`: 2023-06-30 00:00:00 → 2025-10-28 00:00:00
    - `award_date`: 2024-03-25 00:00:00 → 2026-09-22 00:00:00
- id-like uniques:
    - `fund_name`: 144 unique (nulls 0)
    - `shof_fundid`: 113 unique (nulls 31)
    - `shof_fundname`: 113 unique (nulls 31)
- first 3 rows:
```
           round  bid_no                        manager                                        fund_name  winner  on_ppm_at_announce shof_fundid                        shof_fundname                                              reason announce_date  award_date
0  R01_EU_active       1  ABN AMRO Investment Solutions  ABN AMRO EdenTree European Sustainable Equities       0                   0  FS0000D1XC  ABN AMRO EdenTree European Sust Eqs  SHoF fund matched but no SEK TRI at announce month    2023-06-30  2024-03-25
1  R01_EU_active       6         Amundi Ireland Limited                       GIB AM European Focus Fund       0                   0  FS0000I5CQ           GIB AM European Focus Fund  SHoF fund matched but no SEK TRI at announce month    2023-06-30  2024-03-25
2  R01_EU_active       7  AXA Investment Managers Paris      AXA WF Framlington Sustainable Europe I EUR       0                   0         NaN                                  NaN                                  no SHoF fund match    2023-06-30  2024-03-25
```

### data/derived/ftn_2026-10-11/winners_fee_series.csv  (303.0 kB)
- rows: 2,370  cols: 11
- columns (dtype):
    - `round` (object)
    - `award` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `isin` (object)
    - `kategori` (object)
    - `date` (object)
    - `upphandlad` (object)
    - `fee_net` (float64)
    - `fee_gross` (float64)
    - `mv_tot` (float64)
- date-like ranges:
    - `date`: 2022-01-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `fondnr`: 62 unique (nulls 0)
    - `fondnamn`: 74 unique (nulls 0)
    - `isin`: 62 unique (nulls 0)
- first 3 rows:
```
              round       award  fondnr                                         fondnamn          isin kategori        date upphandlad  fee_net  fee_gross        mv_tot
0  R1 Europe active  2024-03-25  124438  JPMorgan Funds - Europe Sustainable Equity Fund  LU1529809227   Europa  2024-05-31        NaN      NaN        NaN  1.476252e+06
1  R1 Europe active  2024-03-25  124438  JPMorgan Funds - Europe Sustainable Equity Fund  LU1529809227   Europa  2024-06-30        NaN      NaN        NaN  6.842568e+08
2  R1 Europe active  2024-03-25  124438  JPMorgan Funds - Europe Sustainable Equity Fund  LU1529809227   Europa  2024-07-31        NaN      NaN        NaN  1.096025e+09
```

### data/derived/shof_monthly/shof_rips_monthly.csv  (18.86 MB)
- rows: 442,507  cols: 5
- columns (dtype):
    - `performanceId` (object)
    - `returntype` (int64)
    - `ym` (object)
    - `last_date` (object)
    - `tri_sek` (float64)
- date-like ranges:
    - `ym`: 2018-01-01 00:00:00 → 2026-09-01 00:00:00
    - `last_date`: 2018-01-23 00:00:00 → 2026-09-27 00:00:00
- id-like uniques:
    - `performanceId`: 4,761 unique (nulls 0)
- first 3 rows:
```
  performanceId  returntype       ym   last_date      tri_sek
0    0P00000ASZ           1  2018-01  2018-01-31  26584.11626
1    0P00000ASZ           1  2018-02  2018-02-28  26865.31109
2    0P00000ASZ           1  2018-03  2018-03-31  27045.48391
```

### data/derived/shof_monthly/shof_valuations_monthly.csv  (46.41 MB)
- rows: 457,842  cols: 12
- columns (dtype):
    - `performanceId` (object)
    - `ym` (object)
    - `secid` (object)
    - `ccy_class` (object)
    - `ccy_fund` (object)
    - `last_date` (object)
    - `tnaclass` (float64)
    - `tnafund` (float64)
    - `nf_class` (float64)
    - `nf_fund` (float64)
    - `ndays` (int64)
    - `nf_class_n` (int64)
- date-like ranges:
    - `ym`: 2018-01-01 00:00:00 → 2026-09-01 00:00:00
    - `last_date`: 2018-01-25 00:00:00 → 2026-09-30 00:00:00
    - `ndays`: 1 → 31
- id-like uniques:
    - `performanceId`: 4,984 unique (nulls 0)
    - `secid`: 4,334 unique (nulls 0)
    - `ccy_fund`: 22 unique (nulls 0)
    - `tnafund`: 71,614 unique (nulls 9,273)
    - `nf_fund`: 47,467 unique (nulls 0)
- first 3 rows:
```
  performanceId       ym       secid ccy_class ccy_fund   last_date    tnaclass      tnafund     nf_class       nf_fund  ndays  nf_class_n
0    0P00000ASZ  2018-01  F0GBR04AIO       EUR      EUR  2018-01-31  57944352.0  800748084.0 -2488731.994  1.462616e+07     22          22
1    0P00000ASZ  2018-02  F0GBR04AIO       EUR      EUR  2018-02-28  56936145.0  788272345.0   234679.040  4.755226e+06     20          20
2    0P00000ASZ  2018-03  F0GBR04AIO       EUR      EUR  2018-03-29  56691639.0  777948109.0   456572.789 -6.164773e+05     21          21
```

### data/measurements/agent2019_t2_decomposition_summary.csv  (15.6 kB)
- rows: 24  cols: 43
- columns (dtype):
    - `sample` (object)
    - `n` (int64)
    - `mv_pre_bn` (float64)
    - `savers_pre` (float64)
    - `w1_pct_vol_cap_churnadj` (float64)
    - `w1_n` (int64)
    - `w1_vol_bn` (float64)
    - `w1_pct_vol_cap` (float64)
    - `w1_pct_vol_cap_exDec` (float64)
    - `w1_pct_vol_sav` (float64)
    - `w1_median_pct_vol_fund` (float64)
    - `w2_pct_vol_cap_churnadj` (float64)
    - `w2_n` (int64)
    - `w2_vol_bn` (float64)
    - `w2_pct_vol_cap` (float64)
    - `w2_pct_vol_cap_exDec` (float64)
    - `w2_pct_vol_sav` (float64)
    - `w2_median_pct_vol_fund` (float64)
    - `w3_pct_vol_cap_churnadj` (float64)
    - `w3_n` (int64)
    - `w3_vol_bn` (float64)
    - `w3_pct_vol_cap` (float64)
    - `w3_pct_vol_cap_exDec` (float64)
    - `w3_pct_vol_sav` (float64)
    - `w3_median_pct_vol_fund` (float64)
    - `fix1901_pct_vol_cap_churnadj` (float64)
    - `fix1901_n` (int64)
    - `fix1901_vol_bn` (float64)
    - `fix1901_pct_vol_cap` (float64)
    - `fix1901_pct_vol_cap_exDec` (float64)
    - `fix1901_pct_vol_sav` (float64)
    - `fix1901_median_pct_vol_fund` (float64)
    - `fix1811_pct_vol_cap_churnadj` (float64)
    - `fix1811_n` (int64)
    - `fix1811_vol_bn` (float64)
    - `fix1811_pct_vol_cap` (float64)
    - `fix1811_pct_vol_cap_exDec` (float64)
    - `fix1811_pct_vol_sav` (float64)
    - `fix1811_median_pct_vol_fund` (float64)
    - `merger_n` (float64)
    - `merger_mv_bn` (float64)
    - `merger_pct_vol_in_M_recv` (float64)
    - `merger_pct_sav_vol_in_M_recv` (float64)
- id-like uniques:
    - `w1_median_pct_vol_fund`: 24 unique (nulls 0)
    - `w2_median_pct_vol_fund`: 23 unique (nulls 0)
    - `w3_median_pct_vol_fund`: 24 unique (nulls 0)
    - `fix1901_median_pct_vol_fund`: 22 unique (nulls 2)
    - `fix1811_median_pct_vol_fund`: 24 unique (nulls 0)
- first 3 rows:
```
                 sample    n  mv_pre_bn  savers_pre  w1_pct_vol_cap_churnadj  w1_n  w1_vol_bn  w1_pct_vol_cap  w1_pct_vol_cap_exDec  w1_pct_vol_sav  w1_median_pct_vol_fund  w2_pct_vol_cap_churnadj  w2_n  w2_vol_bn  w2_pct_vol_cap  w2_pct_vol_cap_exDec  w2_pct_vol_sav  w2_median_pct_vol_fund  w3_pct_vol_cap_churnadj  w3_n  w3_vol_bn  w3_pct_vol_cap  w3_pct_vol_cap_exDec  w3_pct_vol_sav  w3_median_pct_vol_fund  fix1901_pct_vol_cap_churnadj  fix1901_n  fix1901_vol_bn  fix1901_pct_vol_cap  fix1901_pct_vol_cap_exDec  fix1901_pct_vol_sav  fix1901_median_pct_vol_fund  fix1811_pct_vol_cap_churnadj  fix1811_n  fix1811_vol_bn  fix1811_pct_vol_cap  fix1811_pct_vol_cap_exDec  fix1811_pct_vol_sav  fix1811_median_pct_vol_fund  merger_n  merger_mv_bn  merger_pct_vol_in_M_recv  merger_pct_sav_vol_in_M_recv
0        purge_all_2019  313  80.358352    949066.0                 2.949169   313   2.028376        2.462018              2.471729        1.258066                3.703983                 4.134988   313   2.471011        2.983255              3.245862        1.978776                5.626845                 5.182659   313   2.687253        3.235876              3.855647        0.848216                6.136476                      6.891928        305        3.564415             4.260595                   4.260595             0.634693                     7.980843                      8.259497        313        2.312380             2.797096                   5.320930             2.078899                     4.516121      70.0     46.188096                  1.475177                       11.3499
1     purge_AP7_default  243  34.170256    393810.0                 3.135750   243   0.805322        2.302528              2.308581        0.187049                3.828569                 5.418344   243   1.335701        3.761906              3.789082        1.736167                6.771760                 7.638966   243   1.840297        5.110438              5.270472       -1.009557                7.692435                     11.445172        239        2.326803             6.380230                   6.380230            -0.340702                    10.013905                     13.788918        243        2.029133             5.605433                   8.298375             2.907762                     6.425369       NaN           NaN                       NaN                           NaN
2  purge_merger_default   70  46.188096    555256.0                 2.810672    70   1.223053        2.579675              2.592077        2.003847                3.011323                 3.162912    70   1.135310        2.399046              2.840020        2.150119                3.589431                 3.279698    70   0.846956        1.800691              2.781447        2.124937                2.776862                      3.193776         66        1.237612             2.622555                   2.622555             1.321779                     4.230184                      3.689582         70        0.283247             0.609509                   2.990702             1.482405                     2.038913      70.0     46.188096                  1.475177                       11.3499
```

### data/measurements/agent2019_t4_side_by_side_ftn.csv  (2.8 kB)
- rows: 13  cols: 8
- columns (dtype):
    - `sample` (object)
    - `n_funds` (int64)
    - `mv_at_event_bn` (float64)
    - `vol_bn` (float64)
    - `default_bn` (float64)
    - `pct_vol_cap` (float64)
    - `pct_vol_sav` (float64)
    - `note` (object)
- id-like uniques:
    - `n_funds`: 4 unique (nulls 0)
    - `mv_at_event_bn`: 4 unique (nulls 0)
- first 3 rows:
```
                                                     sample  n_funds  mv_at_event_bn    vol_bn  default_bn  pct_vol_cap  pct_vol_sav                                                                                           note
0                       FTN 2024-26 exited losers (agent A)       67       75.591064  4.566722   71.147269     6.031543     5.560941  announcement = award; voluntary = outflow award..M-1 (median 3-6 months); default = mv at M-1
1  2019 purge, all non-renum (w1: last observed month only)      313       80.358352  2.028376   80.358352     2.462018     1.258066                         letter typically mid/late M-1; voluntary in M unobserved at fund level
2                  2019 purge, all non-renum (w3: 3 months)      313       80.358352  3.222586   80.358352     3.855647     0.848216                                                                                          exDec
```

### data/measurements/agentA_summary_by_round.csv  (3.3 kB)
- rows: 19  cols: 14
- columns (dtype):
    - `round` (object)
    - `sample` (object)
    - `n_los` (int64)
    - `mv_award_bn` (float64)
    - `vol_bn` (float64)
    - `default_bn` (float64)
    - `pct_vol_cap` (float64)
    - `pct_vol_cap_exDec` (float64)
    - `sav_award` (int64)
    - `sav_vol` (int64)
    - `sav_default` (int64)
    - `pct_vol_sav` (float64)
    - `med_months_award_to_move` (float64)
    - `max_tranche_months` (float64)
- date-like ranges:
    - `med_months_award_to_move`: 3.0 → 6.0
    - `max_tranche_months`: 0.0 → 10.0
- first 3 rows:
```
       round            sample  n_los  mv_award_bn    vol_bn  default_bn  pct_vol_cap  pct_vol_cap_exDec  sav_award  sav_vol  sav_default  pct_vol_sav  med_months_award_to_move  max_tranche_months
0  EU_active            exited     20     7.821017 -0.022810    7.967551    -0.287111          -0.287111      95310      689        94621     0.722904                       3.0                 1.0
1  EU_active  all_incl_pending     20     7.821017 -0.022810    7.967551    -0.287111          -0.287111      95310      689        94621     0.722904                       3.0                 1.0
2   EU_index            exited      3     0.688590  0.028812    0.697208     3.968457           4.834007       6999      465         6534     6.643806                       5.0                 0.0
```

### data/measurements/agentA_task1_round_membership.csv  (17.1 kB)
- rows: 131  cols: 12
- columns (dtype):
    - `round` (object)
    - `award` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `kategori` (object)
    - `role` (object)
    - `mv_award` (float64)
    - `val_award` (float64)
    - `first_month` (object)
    - `last_month` (object)
    - `avslutsdatum` (object)
    - `fondstatus` (float64)
- date-like ranges:
    - `first_month`: 2022-01-31 00:00:00 → 2026-08-31 00:00:00
    - `last_month`: 2024-05-31 00:00:00 → 2026-08-31 00:00:00
    - `avslutsdatum`: 2024-06-14 00:00:00 → 2026-06-24 00:00:00
- id-like uniques:
    - `fondnr`: 131 unique (nulls 0)
    - `fondnamn`: 131 unique (nulls 0)
    - `fondstatus`: 3 unique (nulls 5)
- first 3 rows:
```
       round       award  fondnr                       fondnamn kategori   role      mv_award  val_award first_month  last_month avslutsdatum  fondstatus
0  EU_active  2024-03-25  336826         BL - Equities Europe B   Europa  loser  6.988530e+08     7437.0  2022-01-31  2024-05-31   2024-06-27         5.0
1  EU_active  2024-03-25  916122    BlackRock - Euro Markets A2   Europa  loser  8.969697e+07      904.0  2022-01-31  2024-06-30   2024-07-08         5.0
2  EU_active  2024-03-25  696898  BlackRock - European Value A2   Europa  loser  3.892773e+07      379.0  2022-01-31  2024-05-31   2024-07-05         5.0
```

### data/measurements/agentA_task2_loser_decomposition.csv  (17.2 kB)
- rows: 78  cols: 21
- columns (dtype):
    - `round` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `exited` (bool)
    - `last_month` (object)
    - `avslutsdatum` (object)
    - `move_start` (object)
    - `n_tranche_months` (int64)
    - `months_award_to_move` (int64)
    - `mv_award` (float64)
    - `val_award` (int64)
    - `vol_out` (float64)
    - `vol_out_exDec` (float64)
    - `dec_hn_pre` (float64)
    - `default_mv` (float64)
    - `val_at_move` (int64)
    - `val_last` (int64)
    - `mv_last` (float64)
    - `hn_tranche_months` (float64)
    - `sav_vol` (int64)
    - `pct_vol_cap` (float64)
- date-like ranges:
    - `last_month`: 2024-05-31 00:00:00 → 2026-08-31 00:00:00
    - `avslutsdatum`: 2024-06-14 00:00:00 → 2026-06-24 00:00:00
    - `move_start`: 2024-06-30 00:00:00 → 2026-09-30 00:00:00
    - `n_tranche_months`: 0 → 10
    - `months_award_to_move`: 3 → 6
    - `val_last`: 1 → 95182
    - `mv_last`: 33161.45428288 → 3515294527.81479
    - `hn_tranche_months`: -20068538527.44 → 0.0
- id-like uniques:
    - `fondnr`: 78 unique (nulls 0)
    - `fondnamn`: 78 unique (nulls 0)
- first 3 rows:
```
       round  fondnr                       fondnamn  exited  last_month avslutsdatum  move_start  n_tranche_months  months_award_to_move      mv_award  val_award     vol_out  vol_out_exDec  dec_hn_pre    default_mv  val_at_move  val_last       mv_last  hn_tranche_months  sav_vol  pct_vol_cap
0  EU_active  336826         BL - Equities Europe B    True  2024-05-31   2024-06-27  2024-06-30                 0                     3  6.988530e+08       7437   767455.54      767455.54         0.0  6.896811e+08         7379      7379  6.896811e+08               0.00       58     0.111153
1  EU_active  916122    BlackRock - Euro Markets A2    True  2024-06-30   2024-07-08  2024-06-30                 1                     3  8.969697e+07        904  9046178.37     9046178.37         0.0  7.945514e+07          843         1  3.849661e+04       -77415243.18       61    10.221519
2  EU_active  696898  BlackRock - European Value A2    True  2024-05-31   2024-07-05  2024-06-30                 0                     3  3.892773e+07        379  2003418.39     2003418.39         0.0  3.784657e+07          360       360  3.784657e+07               0.00       19     5.027400
```

### data/measurements/agentA_task3_monthly_flows_winners_losers.csv  (158.6 kB)
- rows: 1,433  cols: 9
- columns (dtype):
    - `round` (object)
    - `role` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `date` (object)
    - `mv_tot` (float64)
    - `val_tot` (int64)
    - `handel_netto` (float64)
    - `december_flag` (bool)
- date-like ranges:
    - `date`: 2023-12-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `fondnr`: 131 unique (nulls 0)
    - `fondnamn`: 136 unique (nulls 0)
- first 3 rows:
```
       round   role  fondnr                fondnamn        date        mv_tot  val_tot  handel_netto  december_flag
0  EU_active  loser  336826  BL - Equities Europe B  2023-12-31  6.499750e+08     7570    9571789.74           True
1  EU_active  loser  336826  BL - Equities Europe B  2024-01-31  6.648718e+08     7540   -3818842.98           True
2  EU_active  loser  336826  BL - Equities Europe B  2024-02-29  6.755937e+08     7494   -5324687.70          False
```

### data/measurements/bids_long.csv  (111.2 kB)
- rows: 290  cols: 53
- columns (dtype):
    - `round` (object)
    - `category` (object)
    - `announce_date` (object)
    - `bid_deadline` (object)
    - `award_date` (object)
    - `n_bids_reported` (int64)
    - `n_qualified_reported` (int64)
    - `bid_no` (int64)
    - `manager` (object)
    - `fund_name` (object)
    - `winner` (int64)
    - `qualified` (float64)
    - `on_ppm_at_announce` (int64)
    - `incumbent_in_category` (int64)
    - `new_to_platform` (float64)
    - `report_marks_new` (float64)
    - `manager_swedish` (int64)
    - `ppm_fondnr_at_announce` (float64)
    - `ppm_isin_at_announce` (object)
    - `ppm_kategori_at_announce` (object)
    - `ppm_fondnr_any` (object)
    - `ppm_isins` (object)
    - `shof_fundid` (object)
    - `shof_match` (object)
    - `match_approx` (int64)
    - `perfid` (object)
    - `end_ym_announce` (object)
    - `end_ym_deadline` (object)
    - `ret12_ann` (float64)
    - `ret36_ann` (float64)
    - `ret12_dl` (float64)
    - `ret36_dl` (float64)
    - `ppm_ret12` (float64)
    - `ppm_ret36` (float64)
    - `ret12_src` (object)
    - `ret12_ann_filled` (float64)
    - `ret36_ann_filled` (float64)
    - `pct12_ann_filled` (float64)
    - `pct36_ann_filled` (float64)
    - `pct12_ann` (float64)
    - `pct36_ann` (float64)
    - `pct12_dl` (float64)
    - `pct36_dl` (float64)
    - `tna_fund_ccy` (float64)
    - `tna_ccy` (object)
    - `tna_fund_msek` (float64)
    - `log_tna_msek` (float64)
    - `size_pct` (float64)
    - `ppm_fee_net` (float64)
    - `ppm_fee_gross` (float64)
    - `ppm_capital_msek` (float64)
    - `post_award_months` (float64)
    - `post_award_last_ym` (object)
- date-like ranges:
    - `announce_date`: 2023-06-30 00:00:00 → 2025-10-28 00:00:00
    - `award_date`: 2024-03-25 00:00:00 → 2026-09-22 00:00:00
    - `on_ppm_at_announce`: 0 → 1
    - `ppm_fondnr_at_announce`: 103606.0 → 989491.0
    - `end_ym_announce`: 2023-06-01 00:00:00 → 2025-09-01 00:00:00
    - `end_ym_deadline`: 2023-09-01 00:00:00 → 2025-11-01 00:00:00
    - `ret12_ann`: -0.1574089160479012 → 0.3765192360451386
    - `ret36_ann`: -0.2382919346486802 → 1.2172408272141937
    - `ret12_dl`: -0.1303620051798349 → 0.4001382824795696
    - `ppm_ret12`: -0.16 → 0.38
    - `ret12_ann_filled`: -0.1574089160479012 → 0.3765192360451386
    - `ret36_ann_filled`: -0.2382919346486802 → 1.2172408272141937
    - `pct12_ann_filled`: 0.0303030303030303 → 1.0
    - `pct36_ann_filled`: 0.0303030303030303 → 1.0
    - `pct12_ann`: 0.0303030303030303 → 1.0
    - `pct36_ann`: 0.03125 → 1.0
    - `pct12_dl`: 0.0303030303030303 → 1.0
    - `post_award_months`: 0.0 → 30.0
    - `post_award_last_ym`: 2026-07-01 00:00:00 → 2026-09-01 00:00:00
- id-like uniques:
    - `fund_name`: 290 unique (nulls 0)
    - `ppm_fondnr_at_announce`: 113 unique (nulls 176)
    - `ppm_isin_at_announce`: 113 unique (nulls 176)
    - `ppm_fondnr_any`: 133 unique (nulls 156)
    - `ppm_isins`: 133 unique (nulls 156)
    - `shof_fundid`: 258 unique (nulls 31)
    - `perfid`: 147 unique (nulls 142)
    - `tna_fund_ccy`: 141 unique (nulls 149)
    - `tna_fund_msek`: 141 unique (nulls 149)
- first 3 rows:
```
           round       category announce_date bid_deadline  award_date  n_bids_reported  n_qualified_reported  bid_no                            manager                                        fund_name  winner  qualified  on_ppm_at_announce  incumbent_in_category  new_to_platform  report_marks_new  manager_swedish  ppm_fondnr_at_announce ppm_isin_at_announce ppm_kategori_at_announce ppm_fondnr_any                  ppm_isins shof_fundid shof_match  match_approx      perfid end_ym_announce end_ym_deadline  ret12_ann  ret36_ann  ret12_dl  ret36_dl  ppm_ret12  ppm_ret36 ret12_src  ret12_ann_filled  ret36_ann_filled  pct12_ann_filled  pct36_ann_filled  pct12_ann  pct36_ann  pct12_dl  pct36_dl  tna_fund_ccy tna_ccy  tna_fund_msek  log_tna_msek  size_pct  ppm_fee_net  ppm_fee_gross  ppm_capital_msek  post_award_months post_award_last_ym
0  R01_EU_active  Europe active    2023-06-30   2023-10-05  2024-03-25               35                    12       1      ABN AMRO Investment Solutions  ABN AMRO EdenTree European Sustainable Equities       0        NaN                   0                      0              NaN               NaN                0                     NaN                  NaN                      NaN            NaN                        NaN  FS0000D1XC      fuzzy             0         NaN         2023-06         2023-09        NaN        NaN       NaN       NaN        NaN        NaN       NaN               NaN               NaN               NaN               NaN        NaN        NaN       NaN       NaN           NaN     NaN            NaN           NaN       NaN          NaN            NaN               NaN                0.0                NaN
1  R01_EU_active  Europe active    2023-06-30   2023-10-05  2024-03-25               35                    12       2  abrdn Investments Luxembourg S.A.                 European Sustainable Equity Fund       1        1.0                   1                      1              0.0               NaN                0                367698.0         LU0094541447                   Europa  367698;952770  LU0094541447;LU0231472209  FSGBR05845   ppm_isin             0  0P00000B5S         2023-06         2023-09   0.295895   0.346807  0.196185  0.185013        0.3       0.35      shof          0.295895          0.346807          0.642857          0.142857   0.642857   0.142857  0.214286  0.214286  2.433067e+08     EUR    2793.160951      7.934929  0.214286         0.55           1.69         17.454651               30.0            2026-09
2  R01_EU_active  Europe active    2023-06-30   2023-10-05  2024-03-25               35                    12       3      Allianz Global Investors GmbH             Allianz Europe Equity Growth- AT EUR       0        NaN                   0                      0              NaN               NaN                0                     NaN                  NaN                      NaN            NaN                        NaN  FSUSA07KTU      fuzzy             0  0P00006SRJ         2023-06         2023-09   0.348960   0.416595  0.292058  0.184860        NaN        NaN      shof          0.348960          0.416595          0.857143          0.214286   0.857143   0.214286  0.857143  0.142857  4.925726e+09     EUR   56547.330572     10.942833  1.000000          NaN            NaN               NaN               30.0            2026-09
```

### data/measurements/execution_windows_monthly.csv  (9.4 kB)
- rows: 102  cols: 9
- columns (dtype):
    - `round` (object)
    - `month` (object)
    - `rel_month` (int64)
    - `loser_handel_netto_bn` (float64)
    - `loser_residual_exit_bn` (float64)
    - `loser_total_out_pct_of_award_cap` (float64)
    - `winner_handel_netto_bn` (float64)
    - `winner_in_pct_of_award_cap` (float64)
    - `n_losers_in_panel` (int64)
- date-like ranges:
    - `month`: 2024-08-31 00:00:00 → 2027-07-31 00:00:00
    - `rel_month`: -2 → 14
    - `loser_residual_exit_bn`: -8.487854515649145 → 0.0
- first 3 rows:
```
       round       month  rel_month  loser_handel_netto_bn  loser_residual_exit_bn  loser_total_out_pct_of_award_cap  winner_handel_netto_bn  winner_in_pct_of_award_cap  n_losers_in_panel
0  SE_active  2025-06-30         -2              -0.167870                     0.0                         -0.792891               -0.312435                   -1.475706                 18
1  SE_active  2025-07-31         -1              -0.147484                     0.0                         -0.696604               -0.293894                   -1.388131                 18
2  SE_active  2025-08-31          0              -0.163544                     0.0                         -0.772458               -0.270057                   -1.275543                 18
```

### data/measurements/fip_allnames_summary.csv  (1.9 kB)
- rows: 5  cols: 14
- columns (dtype):
    - `tag` (object)
    - `n_names_with_cap` (int64)
    - `n_fetched` (int64)
    - `n_approx` (int64)
    - `sd_fip_pct` (float64)
    - `p90_abs_fip` (float64)
    - `p99_abs_fip` (float64)
    - `max_abs_fip` (float64)
    - `n_abs_fip_gt_0p25` (int64)
    - `n_abs_fip_gt_0p5` (int64)
    - `n_abs_fip_gt_1` (int64)
    - `sd_gross_pct` (float64)
    - `top5_neg` (object)
    - `top5_pos` (object)
- id-like uniques:
    - `n_names_with_cap`: 5 unique (nulls 0)
- first 3 rows:
```
                                          tag  n_names_with_cap  n_fetched  n_approx  sd_fip_pct  p90_abs_fip  p99_abs_fip  max_abs_fip  n_abs_fip_gt_0p25  n_abs_fip_gt_0p5  n_abs_fip_gt_1  sd_gross_pct                                                                                                 top5_neg                                                                                     top5_pos
0              SE_active_2026q2_2026q2_actual               167         56       111    0.242520     0.400825     0.820586     1.336152                 33                10               1      0.350994  FI0009007611 -1.34%, SE0012729366 -0.94%, SE0010323998 -0.76%, SE0013747870 -0.71%, SE0015812417 -0.66%  SE0007491303 0.52%, SE0009858152 0.46%, Lagercrantz 0.45%, Loomis 0.38%, SE0000101362 0.38%
1               SE_index_2026q2_2026q2_actual               341         57       284    0.060444     0.097577     0.238681     0.310618                  3                 0               0      0.196938                Evolution -0.21%, SE0029277987 -0.19%, Saab -0.17%, SE0021309614 -0.12%, Husqvarna -0.11%        SE0016589188 0.31%, Bilia 0.30%, CA5503721063 0.28%, FI0009007611 0.25%, Loomis 0.23%
2  SE_index_2026q2_2026q2_actual_exAvanzaZero               340         56       284    0.041076     0.068286     0.142217     0.217297                  0                 0               0      0.095063           Husqvarna -0.22%, Elekta -0.21%, SE0021309614 -0.19%, SE0009216278 -0.14%, SE0000806994 -0.13%        SE0016589188 0.14%, CA5503721063 0.11%, Bilia 0.11%, FI0009007611 0.09%, Loomis 0.09%
```

### data/measurements/fip_company_Nordic_active_2024q2_2024q2_actual.csv  (4.9 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
       company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0     Investor  1.373993e+08  4.345929e+08 -2.971936e+08  5.719922e+08  1220.0     0.0          1 -0.024360            -0.008120  2.971936e+08
1  Atlas Copco  6.983502e+07  3.194597e+08 -2.496247e+08  3.892947e+08   904.0     0.0          2 -0.027613            -0.009204  2.496247e+08
2        Sampo  0.000000e+00  1.819849e+08 -1.819849e+08  1.819849e+08   279.0     0.0          1 -0.065228            -0.021743  1.819849e+08
```

### data/measurements/fip_company_SE_active_2024q2_2024q2_actual.csv  (5.7 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
    company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0     Volvo  1.348127e+09  8.186901e+08  5.294372e+08  2.166818e+09   682.0     0.0          2  0.077630             0.038815  5.294372e+08
1  Ericsson  6.237110e+07  5.339604e+08 -4.715893e+08  5.963315e+08   322.0     0.0          1 -0.146456            -0.073228  4.715893e+08
2       ABB  5.778286e+08  1.516371e+08  4.261915e+08  7.294657e+08  1640.0     0.0          1  0.025987             0.012994  4.261915e+08
```

### data/measurements/fip_company_SE_active_2024q2_2024q2_equal_new.csv  (5.8 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
    company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0  Ericsson  4.097006e+07  5.339604e+08 -4.929904e+08  5.749305e+08   322.0     0.0          1 -0.153103            -0.076551  4.929904e+08
1       ABB  6.019789e+08  1.516371e+08  4.503418e+08  7.536161e+08  1640.0     0.0          1  0.027460             0.013730  4.503418e+08
2     Volvo  1.239763e+09  8.186901e+08  4.210730e+08  2.058453e+09   682.0     0.0          2  0.061741             0.030870  4.210730e+08
```

### data/measurements/fip_company_SE_active_2026q2_2026q2_actual.csv  (5.8 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
       company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0        Volvo  1.343811e+09  8.128881e+08  5.309227e+08  2.156699e+09   682.0     0.0          2  0.077848             0.038924  5.309227e+08
1      Sandvik  8.466170e+08  3.376946e+08  5.089224e+08  1.184312e+09   461.0     0.0          1  0.110395             0.055198  5.089224e+08
2  Atlas Copco  1.453873e+09  1.023979e+09  4.298937e+08  2.477852e+09   904.0     0.0          2  0.047555             0.023777  4.298937e+08
```

### data/measurements/fip_company_SE_index_2024q2_2026q2_actual.csv  (5.9 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
       company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0  Atlas Copco  3.616456e+09  4.486536e+09 -8.700804e+08  8.102991e+09   904.0     0.0          2 -0.096248            -0.010694  8.700804e+08
1    Evolution  0.000000e+00  8.271474e+08 -8.271474e+08  8.271474e+08   170.0     0.0          1 -0.486557            -0.054062  8.271474e+08
2     Investor  3.852446e+09  3.106141e+09  7.463050e+08  6.958587e+09  1220.0     0.0          2  0.061173             0.006797  7.463050e+08
```

### data/measurements/fip_company_SE_index_2026q2_2026q2_actual.csv  (5.9 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
    company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0  Investor  3.852446e+09  3.266352e+09  5.860943e+08  7.118798e+09  1220.0     0.0          2  0.048041             0.005338  5.860943e+08
1      Saab  2.223306e+08  7.565978e+08 -5.342672e+08  9.789284e+08   309.0     0.0          1 -0.172902            -0.019211  5.342672e+08
2       ABB  1.448475e+09  1.841018e+09 -3.925427e+08  3.289492e+09  1640.0     0.0          1 -0.023936            -0.002660  3.925427e+08
```

### data/measurements/fip_company_SE_index_2026q2_2026q2_actual_AvanzaZeroOnly.csv  (5.8 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
       company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0         Saab  1.271038e+08  7.262583e+08 -5.991545e+08  8.533621e+08   309.0     0.0          1 -0.193901            -0.019390  5.991545e+08
1  Atlas Copco  2.067485e+09  2.507070e+09 -4.395850e+08  4.574556e+09   904.0     0.0          2 -0.048627            -0.004863  4.395850e+08
2          ABB  8.280761e+08  1.241458e+09 -4.133819e+08  2.069534e+09  1640.0     0.0          1 -0.025206            -0.002521  4.133819e+08
```

### data/measurements/fip_company_SE_index_2026q2_2026q2_actual_exAvanzaZero.csv  (6.1 kB)
- rows: 40  cols: 11
- columns (dtype):
    - `company` (object)
    - `buy` (float64)
    - `sell` (float64)
    - `net` (float64)
    - `gross` (float64)
    - `cap_bn` (float64)
    - `approx` (float64)
    - `n_classes` (int64)
    - `fip_pct` (float64)
    - `fip_pct_per_tranche` (float64)
    - `abs_net` (float64)
- id-like uniques:
    - `company`: 40 unique (nulls 0)
- first 3 rows:
```
       company           buy          sell           net         gross  cap_bn  approx  n_classes   fip_pct  fip_pct_per_tranche       abs_net
0  Atlas Copco  1.548970e+09  1.157187e+09  3.917827e+08  2.706158e+09   904.0     0.0          2  0.043339             0.010835  3.917827e+08
1     Investor  1.650048e+09  1.281941e+09  3.681066e+08  2.931989e+09  1220.0     0.0          2  0.030173             0.007543  3.681066e+08
2        Volvo  1.053037e+09  8.464206e+08  2.066164e+08  1.899458e+09   682.0     0.0          2  0.030296             0.007574  2.066164e+08
```

### data/measurements/fip_summary.csv  (1.5 kB)
- rows: 8  cols: 13
- columns (dtype):
    - `tag` (object)
    - `n_companies` (int64)
    - `sd_net_isin_m` (float64)
    - `sd_net_company_m` (float64)
    - `top10_sq_share_company` (float64)
    - `n_company_abs_net_gt_100m` (int64)
    - `n_mapped` (int64)
    - `mapped_share_abs_net` (float64)
    - `sd_fip_pct_mapped` (float64)
    - `max_abs_fip_pct` (float64)
    - `n_abs_fip_gt_0p25` (int64)
    - `n_abs_fip_gt_0p10` (int64)
    - `months_assumed` (int64)
- date-like ranges:
    - `months_assumed`: 2 → 10
- id-like uniques:
    - `sd_net_isin_m`: 8 unique (nulls 0)
    - `sd_net_company_m`: 8 unique (nulls 0)
    - `top10_sq_share_company`: 8 unique (nulls 0)
    - `n_company_abs_net_gt_100m`: 7 unique (nulls 0)
- first 3 rows:
```
                                 tag  n_companies  sd_net_isin_m  sd_net_company_m  top10_sq_share_company  n_company_abs_net_gt_100m  n_mapped  mapped_share_abs_net  sd_fip_pct_mapped  max_abs_fip_pct  n_abs_fip_gt_0p25  n_abs_fip_gt_0p10  months_assumed
0  SE_active_2024q2_2024q2_equal_new          201     106.550088         98.782001                0.641613                         34        58              0.679193           0.151135         0.591278                  6                 19               2
1     SE_active_2024q2_2024q2_actual          224     100.459188         94.775353                0.688483                         30        58              0.666054           0.140443         0.489262                  6                 19               2
2     SE_active_2026q2_2026q2_actual          208     112.122252         99.954786                0.673431                         29        56              0.691769           0.150610         0.448320                  5                 17               2
```

### data/measurements/fund_fi_mapping.csv  (14.8 kB)
- rows: 91  cols: 15
- columns (dtype):
    - `round` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `role` (object)
    - `mv_award` (float64)
    - `fi_2024q2` (float64)
    - `fi_2026q2` (float64)
    - `in_fi` (bool)
    - `note` (object)
    - `fi_name_2024q2` (object)
    - `bench_2024q2` (object)
    - `bench_2026q2` (object)
    - `n_hold_2024q2` (float64)
    - `nav_2024q2_bn` (float64)
    - `ppm_share_of_fund_2024q2_pct` (float64)
- id-like uniques:
    - `fondnr`: 91 unique (nulls 0)
    - `fondnamn`: 91 unique (nulls 0)
    - `fi_name_2024q2`: 49 unique (nulls 42)
    - `ppm_share_of_fund_2024q2_pct`: 41 unique (nulls 50)
- first 3 rows:
```
          round  fondnr                                        fondnamn   role      mv_award  fi_2024q2  fi_2026q2  in_fi                                        note fi_name_2024q2            bench_2024q2                                                        bench_2026q2  n_hold_2024q2  nav_2024q2_bn  ppm_share_of_fund_2024q2_pct
0  Global_index  680124                                   Avanza Global  loser  3.692385e+09    61050.0    61050.0   True  SE (feeder: 1 holding = Amundi index fund)  Avanza Global  Jämförelseindex saknas  Morningstar Developed Markets TME PAB Sustainability Select NR SEK            1.0       30.97526                     11.920434
1  Global_index  252411           Danske Invest SICAV - Global Index SI  loser  2.353427e+09        NaN        NaN  False                                  LU: Danske            NaN                     NaN                                                                 NaN            NaN            NaN                           NaN
2  Global_index  613729  Danske Invest  SICAV - Global Index Restricted  loser  2.206320e+08        NaN        NaN  False                                  LU: Danske            NaN                     NaN                                                                 NaN            NaN            NaN                           NaN
```

### data/measurements/winners_fee_series.csv  (303.0 kB)
- rows: 2,370  cols: 11
- columns (dtype):
    - `round` (object)
    - `award` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `isin` (object)
    - `kategori` (object)
    - `date` (object)
    - `upphandlad` (object)
    - `fee_net` (float64)
    - `fee_gross` (float64)
    - `mv_tot` (float64)
- date-like ranges:
    - `date`: 2022-01-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `fondnr`: 62 unique (nulls 0)
    - `fondnamn`: 74 unique (nulls 0)
    - `isin`: 62 unique (nulls 0)
- first 3 rows:
```
              round       award  fondnr                                         fondnamn          isin kategori        date upphandlad  fee_net  fee_gross        mv_tot
0  R1 Europe active  2024-03-25  124438  JPMorgan Funds - Europe Sustainable Equity Fund  LU1529809227   Europa  2024-05-31        NaN      NaN        NaN  1.476252e+06
1  R1 Europe active  2024-03-25  124438  JPMorgan Funds - Europe Sustainable Equity Fund  LU1529809227   Europa  2024-06-30        NaN      NaN        NaN  6.842568e+08
2  R1 Europe active  2024-03-25  124438  JPMorgan Funds - Europe Sustainable Equity Fund  LU1529809227   Europa  2024-07-31        NaN      NaN        NaN  1.096025e+09
```

### data/measurements/agent2019_t3_totals_2019.json  (0.8 kB)
- JSON content (first 1500 chars):
```
{
 "mv_nonrenum": 80.358351693,
 "mv_ap7cls": 34.170255993,
 "mv_merger": 46.188095700000005,
 "ap7_raw": 35.675564958,
 "ap7_excess": 30.281996634999995,
 "recv_matched": 47.630044846669996,
 "recv_matched_capped": 45.50673955556999,
 "abn_inflow_nonap7": 65.0081596368,
 "safa_dsav_raw": 274191.0,
 "safa_dsav_excess": 289954.0,
 "savers_ap7cls": 393810.0,
 "savers_merger": 555256.0,
 "ap7_excess_base_med2018": 30.281996635000002,
 "ap7_capture_pct_base_med2018": 88.62092411951338,
 "ap7_excess_base_0": 35.675564958,
 "ap7_capture_pct_base_0": 104.40531954255297,
 "ap7_excess_base_1bn": 24.675564958000002,
 "ap7_capture_pct_base_1bn": 72.21357944481001,
 "safa_capture_pct_savers": 73.62789162286381,
 "ap7_base_bn": 0.490324393,
 "safa_base": -1433.0
}
```

### data/facts/fact1_GA_losers_fundlevel.csv  (4.6 kB)
- rows: 38  cols: 9
- columns (dtype):
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `hn` (float64)
    - `mv_tot` (float64)
    - `val_tot` (float64)
    - `fee_net` (float64)
    - `val_aug26` (float64)
    - `cum_hn_pct` (float64)
    - `dval_pct` (float64)
- id-like uniques:
    - `fondnr`: 38 unique (nulls 0)
    - `fondnamn`: 38 unique (nulls 0)
- first 3 rows:
```
   fondnr               fondnamn            hn        mv_tot   val_tot  fee_net  val_aug26  cum_hn_pct  dval_pct
0  271478      Indecap Guide 2 C -5.312040e+08  3.496857e+10   83571.0     0.34    81824.0   -1.519090 -2.090438
1  645952  AMF Aktiefond Världen -6.712992e+08  3.024503e+10  158667.0     0.14   156119.0   -2.219535 -1.605879
2  964767       Lannebo Global A -2.026150e+08  1.058022e+10   63196.0     0.27    62092.0   -1.915036 -1.746946
```

### data/facts/fact1_GA_monthly.csv  (4.4 kB)
- rows: 24  cols: 13
- columns (dtype):
    - `role` (object)
    - `window` (object)
    - `date` (object)
    - `n` (int64)
    - `hn` (float64)
    - `mv_lag` (float64)
    - `val` (float64)
    - `val_lag` (float64)
    - `is_dec` (bool)
    - `hn_pct_mv` (float64)
    - `dval_pct` (float64)
    - `med_hn_pct` (float64)
    - `med_dv_pct` (float64)
- date-like ranges:
    - `date`: 2025-09-30 00:00:00 → 2026-08-31 00:00:00
- first 3 rows:
```
       role            window        date   n            hn        mv_lag       val   val_lag  is_dec  hn_pct_mv  dval_pct  med_hn_pct  med_dv_pct
0  GA_loser       award_Feb26  2026-02-28  38 -1.021890e+09  1.226948e+11  606560.0  611352.0   False  -0.832872 -0.783836   -1.134947   -0.819901
1  GA_loser  post_Mar26_Aug26  2026-03-31  38 -9.801954e+08  1.255390e+11  602720.0  606560.0   False  -0.780790 -0.633078   -0.877823   -0.656239
2  GA_loser  post_Mar26_Aug26  2026-04-30  38 -5.965308e+08  1.186531e+11  600398.0  602720.0   False  -0.502752 -0.385254   -0.517926   -0.377710
```

### data/facts/fact1_GA_vs_control_Mar_Aug26.csv  (0.4 kB)
- rows: 3  cols: 6
- columns (dtype):
    - `group` (object)
    - `n` (int64)
    - `median_cum_hn_pct` (float64)
    - `pooled_cum_hn_pct` (float64)
    - `median_dval_pct` (float64)
    - `pooled_dval_pct` (float64)
- first 3 rows:
```
                        group    n  median_cum_hn_pct  pooled_cum_hn_pct  median_dval_pct  pooled_dval_pct
0                   GA_losers   38          -2.169055          -1.223396        -2.152336        -1.183395
1            GA_losers_exEvli   37          -2.219535          -1.845605        -2.154626        -1.915442
2  control_equity_nonprocured  135          -1.459351          -2.292630        -1.877934        -0.739324
```

### data/facts/fact1_cum_outflow_by_event_month.csv  (4.3 kB)
- rows: 45  cols: 8
- columns (dtype):
    - `group` (object)
    - `m` (int64)
    - `n_funds` (int64)
    - `cum_hn_pct` (float64)
    - `cum_hn_pct_exDec` (float64)
    - `cum_dval_pct` (float64)
    - `dec_in_window` (bool)
    - `all_losers_unmoved` (bool)
- id-like uniques:
    - `n_funds`: 12 unique (nulls 0)
- first 3 rows:
```
                             group  m  n_funds  cum_hn_pct  cum_hn_pct_exDec  cum_dval_pct  dec_in_window  all_losers_unmoved
0  Global_active (appeal, no move)  1       38   -0.780790         -0.780790     -0.633078          False                True
1  Global_active (appeal, no move)  2       38   -1.255966         -1.255966     -1.015893          False                True
2  Global_active (appeal, no move)  3       38   -0.924433         -0.924433     -1.347600          False                True
```

### data/facts/fact2_gender_baseline_other_equity.csv  (1.0 kB)
- rows: 9  cols: 7
- columns (dtype):
    - `round` (object)
    - `A` (object)
    - `E` (object)
    - `n_funds` (int64)
    - `base_optout_women_pct` (float64)
    - `base_optout_men_pct` (float64)
    - `base_gap_pp` (float64)
- id-like uniques:
    - `n_funds`: 9 unique (nulls 0)
- first 3 rows:
```
         round           A           E  n_funds  base_optout_women_pct  base_optout_men_pct  base_gap_pp
0    EU_active  2024-03-31  2024-05-31      288               0.242652             0.223027    -0.019624
1     EU_index  2024-10-31  2025-02-28      281               0.362887             0.144169    -0.218717
2  EU_smallcap  2026-05-31  2026-07-31      243               0.374057             0.496334     0.122277
```

### data/facts/fact2_gender_by_round.csv  (4.9 kB)
- rows: 16  cols: 20
- columns (dtype):
    - `sample` (object)
    - `round` (object)
    - `n_funds` (float64)
    - `savers_k` (float64)
    - `savers_m` (float64)
    - `share_women_pct` (float64)
    - `months_med` (float64)
    - `optout_women_pct` (float64)
    - `optout_men_pct` (float64)
    - `gap_m_minus_w_pp` (float64)
    - `ratio_m_over_w` (float64)
    - `cap_out_women_pct` (float64)
    - `cap_out_men_pct` (float64)
    - `cap_gap_pp` (float64)
    - `fund_mean_opt_w` (float64)
    - `fund_mean_opt_m` (float64)
    - `fund_median_gap` (float64)
    - `n_funds_men_higher` (float64)
    - `mv_per_saver_w` (float64)
    - `mv_per_saver_m` (float64)
- date-like ranges:
    - `months_med`: 2.0 → 5.0
- id-like uniques:
    - `n_funds`: 12 unique (nulls 0)
    - `fund_mean_opt_w`: 14 unique (nulls 0)
    - `fund_mean_opt_m`: 14 unique (nulls 0)
    - `fund_median_gap`: 14 unique (nulls 0)
    - `n_funds_men_higher`: 12 unique (nulls 0)
- first 3 rows:
```
  sample        round  n_funds  savers_k  savers_m  share_women_pct  months_med  optout_women_pct  optout_men_pct  gap_m_minus_w_pp  ratio_m_over_w  cap_out_women_pct  cap_out_men_pct  cap_gap_pp  fund_mean_opt_w  fund_mean_opt_m  fund_median_gap  n_funds_men_higher  mv_per_saver_w  mv_per_saver_m
0    FTN    EU_active     20.0   47464.0   47846.0        49.799601         2.0          0.657340        0.787945          0.130604        1.198686          -0.316577        -0.024073    0.292503         0.288526         2.272469         0.320179                14.0    75161.497582    88900.892961
1    FTN     EU_index      3.0    2943.0    4056.0        42.048864         4.0          6.082229        7.051282          0.969053        1.159325           2.938352         3.760475    0.822123         4.151026         5.918970         2.603113                 2.0    90885.855334   103824.592458
2    FTN  EU_smallcap      3.0     240.0     502.0        32.345013         2.0          1.666667        0.000000         -1.666667        0.000000           1.599852         2.151296    0.551444         3.675033         1.053056        -1.635686                 1.0   108746.494472   128432.888759
```

### data/facts/fact2_gender_fundlevel.csv  (170.3 kB)
- rows: 544  cols: 26
- columns (dtype):
    - `sample` (object)
    - `round` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `A` (object)
    - `E` (object)
    - `M` (object)
    - `exited` (bool)
    - `val_k_A` (float64)
    - `val_m_A` (float64)
    - `val_k_E` (float64)
    - `val_m_E` (float64)
    - `mv_k_A` (float64)
    - `mv_m_A` (float64)
    - `mv_k_E` (float64)
    - `mv_m_E` (float64)
    - `cumret` (float64)
    - `n_months` (int64)
    - `dec_in_window` (bool)
    - `opt_k` (float64)
    - `opt_m` (float64)
    - `cap_k` (float64)
    - `cap_m` (float64)
    - `share_k_A` (float64)
    - `mv_per_saver_k_A` (float64)
    - `mv_per_saver_m_A` (float64)
- date-like ranges:
    - `n_months`: 1 → 10
- id-like uniques:
    - `fondnr`: 312 unique (nulls 0)
    - `fondnamn`: 311 unique (nulls 0)
- first 3 rows:
```
  sample      round  fondnr                       fondnamn           A           E           M  exited  val_k_A  val_m_A  val_k_E  val_m_E        mv_k_A        mv_m_A        mv_k_E        mv_m_E  cumret  n_months  dec_in_window     opt_k     opt_m     cap_k      cap_m  share_k_A  mv_per_saver_k_A  mv_per_saver_m_A
0    FTN  EU_active  336826         BL - Equities Europe B  2024-03-31  2024-05-31  2024-06-30    True   3468.0   3969.0   3442.0   3937.0  3.005065e+08  3.983465e+08  2.970082e+08  3.926728e+08  0.9898         2          False  0.749712  0.806248  0.145624   0.408469  46.631706      86651.247651     100364.447607
1    FTN  EU_active  916122    BlackRock - Euro Markets A2  2024-03-31  2024-05-31  2024-06-30    True    343.0    561.0    328.0    515.0  3.013601e+07  5.956096e+07  2.765624e+07  5.179890e+07  0.9801         2          False  4.373178  8.199643  6.365271  11.266331  37.942478      87860.093734     106169.267421
2    FTN  EU_active  696898  BlackRock - European Value A2  2024-03-31  2024-05-31  2024-06-30    True    139.0    240.0    137.0    223.0  1.261140e+07  2.631634e+07  1.293767e+07  2.490890e+07  1.0201         2          False  1.438849  7.083333 -0.565781   7.213175  36.675462      90729.474096     109651.399694
```

### data/facts/fact3_summary.csv  (0.8 kB)
- rows: 11  cols: 14
- columns (dtype):
    - `round` (object)
    - `PPM-dedicated class` (float64)
    - `retail class with rebate` (float64)
    - `n` (int64)
    - `pct_dedicated` (float64)
    - `table` (object)
    - `class_type` (object)
    - `n_new` (float64)
    - `mean_gap` (float64)
    - `mean_fee_after` (float64)
    - `mean_ppm_share_pre` (float64)
    - `n_share_pre` (float64)
    - `mean_ppm_share_latest` (float64)
    - `n_share_latest` (float64)
- first 3 rows:
```
              round  PPM-dedicated class  retail class with rebate  n  pct_dedicated     table class_type  n_new  mean_gap  mean_fee_after  mean_ppm_share_pre  n_share_pre  mean_ppm_share_latest  n_share_latest
0  R1 Europe active                  1.0                       3.0  4      25.000000  by_round        NaN    NaN       NaN             NaN                 NaN          NaN                    NaN             NaN
1   R2 Europe index                  0.0                       4.0  4       0.000000  by_round        NaN    NaN       NaN             NaN                 NaN          NaN                    NaN             NaN
2   R2 Global index                  1.0                       5.0  6      16.666667  by_round        NaN    NaN       NaN             NaN                 NaN          NaN                    NaN             NaN
```

### data/facts/fact3_winners_shareclass.csv  (9.2 kB)
- rows: 49  cols: 20
- columns (dtype):
    - `round` (object)
    - `fondnr` (int64)
    - `name` (object)
    - `ny` (object)
    - `fee_awarded` (float64)
    - `contract_month` (object)
    - `fee_net_before` (float64)
    - `fee_gross_before` (float64)
    - `fee_net_after` (float64)
    - `fee_gross_after` (float64)
    - `isin_after` (object)
    - `gap_after` (float64)
    - `mv_award` (float64)
    - `val_award` (float64)
    - `ppm_share_pre_award_pct` (float64)
    - `ppm_share_pre_status` (object)
    - `ppm_share_latest_pct` (float64)
    - `ppm_share_latest_status` (object)
    - `class_type` (object)
    - `new_to_platform` (int64)
- date-like ranges:
    - `contract_month`: 2024-12-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `fondnr`: 49 unique (nulls 0)
    - `name`: 49 unique (nulls 0)
    - `isin_after`: 49 unique (nulls 0)
- first 3 rows:
```
              round  fondnr                                             name   ny  fee_awarded contract_month  fee_net_before  fee_gross_before  fee_net_after  fee_gross_after    isin_after  gap_after      mv_award  val_award  ppm_share_pre_award_pct ppm_share_pre_status  ppm_share_latest_pct ppm_share_latest_status                class_type  new_to_platform
0  R1 Europe active  538462                             AMF Aktiefond Europa  Nej         0.08     2024-12-31            0.14               0.4           0.08             0.40  SE0000739153       0.32  3.477181e+09    35788.0                40.986392                   ok             46.264807                      ok  retail class with rebate                0
1  R1 Europe active  124438  JPMorgan Funds – Europe Sustainable Equity Fund   Ja         0.38     2024-12-31             NaN               NaN           0.38             0.71  LU1529809227       0.33           NaN        NaN                      NaN          non_SEK:EUR                   NaN             non_SEK:EUR  retail class with rebate                1
2  R1 Europe active  196097            Nordea 1 – European Stars Equity Fund   Ja         0.20     2024-12-31             NaN               NaN           0.20             0.21  LU2700275808       0.01           NaN        NaN                      NaN          non_SEK:EUR                   NaN             non_SEK:EUR       PPM-dedicated class                1
```

### data/facts/fact4_losers_moved.csv  (10.4 kB)
- rows: 78  cols: 11
- columns (dtype):
    - `round` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `fee_before` (float64)
    - `default_mv` (float64)
    - `val_at_move` (int64)
    - `vol_out` (float64)
    - `sav_vol` (int64)
    - `exited` (bool)
    - `saving_b_sek_iw` (float64)
    - `saving_b_sek_ew` (float64)
- id-like uniques:
    - `fondnr`: 78 unique (nulls 0)
    - `fondnamn`: 78 unique (nulls 0)
- first 3 rows:
```
       round  fondnr                       fondnamn  fee_before    default_mv  val_at_move     vol_out  sav_vol  exited  saving_b_sek_iw  saving_b_sek_ew
0  EU_active  336826         BL - Equities Europe B        0.45  6.896811e+08         7379   767455.54       58    True     1.446130e+06     1.655235e+06
1  EU_active  916122    BlackRock - Euro Markets A2        0.42  7.945514e+07          843  9046178.37       61    True     1.427658e+05     1.668558e+05
2  EU_active  696898  BlackRock - European Value A2        0.42  3.784657e+07          360  2003418.39       19    True     6.800308e+04     7.947780e+04
```

### data/facts/fact4_savings_by_round.csv  (3.9 kB)
- rows: 9  cols: 29
- columns (dtype):
    - `round` (object)
    - `award` (object)
    - `n_win_inc` (int64)
    - `n_win_new` (int64)
    - `n_losers` (int64)
    - `cap_inc_winners_bn` (float64)
    - `fee_inc_before_cw` (float64)
    - `fee_inc_after_cw` (float64)
    - `saving_a_msek` (float64)
    - `savers_a` (float64)
    - `cap_moved_bn` (float64)
    - `fee_losers_before_cw` (float64)
    - `fee_winners_after_ew` (float64)
    - `fee_winners_after_iw` (float64)
    - `saving_b_msek_iw` (float64)
    - `saving_b_msek_ew` (float64)
    - `savers_b` (int64)
    - `cap_left_voluntarily_bn` (float64)
    - `savers_left_voluntarily` (int64)
    - `ftn_fee_before_ew` (float64)
    - `ftn_fee_after_avg` (float64)
    - `ftn_cap_category_bn` (float64)
    - `ftn_check_saving_msek` (float64)
    - `pending` (bool)
    - `saving_total_msek` (float64)
    - `savers_affected` (float64)
    - `sek_per_saver_a` (float64)
    - `sek_per_saver_b` (float64)
    - `sek_per_saver_total` (float64)
- first 3 rows:
```
          round       award  n_win_inc  n_win_new  n_losers  cap_inc_winners_bn  fee_inc_before_cw  fee_inc_after_cw  saving_a_msek  savers_a  cap_moved_bn  fee_losers_before_cw  fee_winners_after_ew  fee_winners_after_iw  saving_b_msek_iw  saving_b_msek_ew  savers_b  cap_left_voluntarily_bn  savers_left_voluntarily  ftn_fee_before_ew  ftn_fee_after_avg  ftn_cap_category_bn  ftn_check_saving_msek  pending  saving_total_msek  savers_affected  sek_per_saver_a  sek_per_saver_b  sek_per_saver_total
0     EU_active  2024-03-31          1          5        20            3.477181           0.140000          0.080000       2.086309   35788.0      7.967551              0.318807              0.210000              0.240319          6.253605          8.669289     94621                -0.022810                      689              0.480              0.210            11.298199              30.505137    False           8.339914         130409.0        58.296324        66.091092            63.951982
1      EU_index  2024-10-31          4          0         3           15.483092           0.120347          0.046346      11.457559  173207.0      0.697208              0.141470              0.047500              0.045553          0.668741          0.655166      6534                 0.028812                      465              0.135              0.046            16.171682              14.392797    False          12.126300         179741.0        66.149515       102.347921            67.465411
2  Global_index  2024-10-31          3          3         8           30.757826           0.124574          0.040000      26.013255  166374.0     18.516266              0.125312              0.043333              0.042908         15.258248         15.179476    127148                 2.733842                    18558              0.143              0.046            53.791286              52.177548    False          41.271502         293522.0       156.354087       120.003836           140.607867
```

### data/facts/fact4_winners_fees.csv  (7.1 kB)
- rows: 53  cols: 12
- columns (dtype):
    - `round` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `role` (object)
    - `flag_month` (object)
    - `contract_month` (object)
    - `fee_before` (float64)
    - `fee_after` (float64)
    - `mv_award` (float64)
    - `val_award` (float64)
    - `inflow_window` (float64)
    - `saving_a_sek` (float64)
- date-like ranges:
    - `flag_month`: 2024-11-30 00:00:00 → 2026-08-31 00:00:00
    - `contract_month`: 2024-12-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `fondnr`: 53 unique (nulls 0)
    - `fondnamn`: 53 unique (nulls 0)
- first 3 rows:
```
       round  fondnr                                         fondnamn              role  flag_month contract_month  fee_before  fee_after      mv_award  val_award  inflow_window  saving_a_sek
0  EU_active  538462                             AMF Aktiefond Europa  winner_incumbent  2024-11-30     2024-12-31        0.14       0.08  3.477181e+09    35788.0   0.000000e+00  2.086309e+06
1  EU_active  124438  JPMorgan Funds - Europe Sustainable Equity Fund        winner_new  2024-11-30     2024-12-31         NaN       0.38           NaN        NaN   1.065949e+09  0.000000e+00
2  EU_active  196097    Nordea European Sustainable Stars Equity Fund        winner_new  2024-11-30     2024-12-31         NaN       0.20           NaN        NaN   1.711064e+09  0.000000e+00
```

### data/facts/fact5_concentration.csv  (9.9 kB)
- rows: 35  cols: 13
- columns (dtype):
    - `round` (object)
    - `universe` (object)
    - `when` (object)
    - `date` (object)
    - `n_funds` (int64)
    - `n_companies` (int64)
    - `cap_bn` (float64)
    - `top1_pct` (float64)
    - `top1` (object)
    - `top5_pct` (float64)
    - `hhi` (float64)
    - `swedish_pct` (float64)
    - `top5` (object)
- date-like ranges:
    - `date`: 2024-03-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `n_funds`: 17 unique (nulls 0)
- first 3 rows:
```
       round               universe   when        date  n_funds  n_companies     cap_bn   top1_pct                      top1   top5_pct          hhi  swedish_pct                                                                                                                                    top5
0  EU_active   procured_subcategory  award  2024-03-31       21           17  11.298199  30.776422             AMF Fonder AB  91.409777  2238.621656    55.263836  AMF Fonder AB;Nordea Funds Ab;Länsförsäkringar Fondförvaltning AB (publ);SEB Investment Management AB;Banque de Luxembourg Investments
1  EU_active   procured_subcategory  after  2025-03-31        6            6  14.022348  37.409415             AMF Fonder AB  93.669395  2525.463427    49.085696         AMF Fonder AB;Nordea Investment Funds S.A.;Swedbank Robur Fonder AB;SEB Funds AB;J.P. Morgan Asset Management (Europe) S.à.r.l.
2  EU_active  panel_kategori:Europa  award  2024-03-31       28           23  27.310830  25.080450  Swedbank Robur Fonder AB  79.221835  1476.027358    81.403285                                     Swedbank Robur Fonder AB;Storebrand Fonder AB;AMF Fonder AB;Nordea Funds Ab;Handelsbanken Fonder AB
```

### data/panel/ppm_panel_2018_2026.csv  (12.90 MB)
- rows: 53,062  cols: 25
- columns (dtype):
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `val_k` (float64)
    - `val_m` (float64)
    - `val_tot` (float64)
    - `mv_k` (float64)
    - `mv_m` (float64)
    - `mv_tot` (float64)
    - `handel_netto` (float64)
    - `kategori` (object)
    - `fondtyp` (object)
    - `forvaltare` (object)
    - `svensk` (object)
    - `forvaltning` (object)
    - `upphandlad` (object)
    - `ret_ytd` (float64)
    - `ret_1m` (float64)
    - `ret_12m` (float64)
    - `ret_36m` (float64)
    - `fee_net` (float64)
    - `fee_gross` (float64)
    - `valuta` (object)
    - `startdatum` (object)
    - `isin` (object)
    - `date` (object)
- date-like ranges:
    - `date`: 2018-01-31 00:00:00 → 2026-08-31 00:00:00
- id-like uniques:
    - `fondnr`: 1,019 unique (nulls 0)
    - `fondnamn`: 1,783 unique (nulls 0)
    - `fondtyp`: 8 unique (nulls 0)
    - `isin`: 1,014 unique (nulls 416)
- first 3 rows:
```
   fondnr                                           fondnamn      val_k      val_m    val_tot          mv_k          mv_m        mv_tot  handel_netto                        kategori            fondtyp                forvaltare  svensk forvaltning upphandlad  ret_ytd  ret_1m  ret_12m  ret_36m  fee_net  fee_gross valuta startdatum          isin        date
0       1  AP7 Såfa - Statens årskullsförvaltningsalternativ  1793388.0  1918843.0  3712231.0  1.863637e+11  2.318511e+11  4.182148e+11           NaN  Statens förvaltningsalternativ  Generationsfonder          Sjunde AP-fonden  Svensk         NaN        NaN      NaN     NaN      NaN      NaN      NaN        NaN    NaN        NaN           NaN  2018-01-31
1  283408                          Swedbank Robur Technology   139492.0   151250.0   290742.0  9.575349e+09  1.313945e+10  2.271480e+10    22325510.0            IT och kommunikation        Aktiefonder  Swedbank Robur Fonder AB  Svensk         NaN        NaN      3.0     3.0     30.0     65.0     0.27       1.28    SEK       2000  SE0000538944  2018-01-31
2  291906                           Didner & Gerge Aktiefond   111214.0   123380.0   234594.0  1.104389e+10  1.460498e+10  2.564888e+10  -196349274.0                         Sverige        Aktiefonder  Didner & Gerge Fonder AB  Svensk         NaN        NaN      2.0     2.0     10.0     30.0     0.30       1.23    SEK       2000  SE0000428336  2018-01-31
```

### data/winners/winners_table.csv  (21.8 kB)
- rows: 25  cols: 17
- columns (dtype):
    - `year` (int64)
    - `prize` (object)
    - `title` (object)
    - `question` (object)
    - `field` (object)
    - `data_source_country` (object)
    - `sample_N_period` (object)
    - `identification` (object)
    - `anchor_paper` (object)
    - `replicates_published_table` (object)
    - `explicit_extension` (object)
    - `n_main_tables` (int64)
    - `n_figures` (int64)
    - `pages_main_text` (int64)
    - `power_or_MDE_statement` (object)
    - `result_direction` (object)
    - `conclusion_calibration_quote` (object)
- date-like ranges:
    - `year`: 2011 → 2024
- first 3 rows:
```
   year           prize                                                                                                                        title                                                                                                    question           field                                                                        data_source_country                                                                                     sample_N_period                                                                         identification                                                                          anchor_paper                             replicates_published_table                                                  explicit_extension  n_main_tables  n_figures  pages_main_text               power_or_MDE_statement                                                     result_direction                                                                                                                                                                                         conclusion_calibration_quote
0  2011      Per Hiller                                                        Gender quotas, firm performance and firm value: The Norwegian example  Did Norway's 2003 board gender quota change firm performance (ROA, ROE, margin, Tobin's q) and firm value?       corporate  NASDAQ OMX / Oslo Bors lists, accounting and price data; Norway treated vs Sweden control  N~1,521 firm-year obs after cleaning; 2001-2006 (lags to 2009); 2 event dates (Feb 2002, Dec 2003)           diff-in-diff (Norway vs Sweden) + event study with industry-index benchmarks                                             Ahern & Dittmar (2009 wp, later QJE 2012)  partly (announcement-day CAR comparable to A&D -2.6%)  yes: cross-country control, industry benchmarks, second event date              8         13               27                                   no  mixed (DiD null; CAR -2.7% at first announcement; Dec 2003 unclear)                                             we can conclude that there are no statistically significant changes in the financial measures for Norwegian firms after the introduction of the gender quota requirement
1  2011  Staffan Viotti  The Impact of Short Sale Bans on Option Trading Activity: Evidence from the Financial Crisis of 2007-2009 and its Aftermath                      Did short sellers migrate to option markets when 2008-11 short sale bans were imposed?  microstructure                  Thomson Datastream option and stock data; 10 countries (financial stocks)                                        171 option-class pairs, 116,528 daily obs; Jan 2008-Feb 2011       panel FE (stock and time FE) with ban dummies; naked vs covered bans; subsamples  Grundy, Lim & Verwijmeren (2010 wp, JFE 2012); Battalio & Schultz (2009 wp, JF 2011)                                 no (new specification)             yes: international panel, ban stringency, open interest             10          9               32                                   no                             positive but endogeneity-flagged (mixed)  graphical results and various subsample re-estimations indicate that the adoption of the bans is endogenous. Hence, it is hard to assign the observed effects to an attempt by short sellers to circumvent the bans
2  2012  Staffan Viotti                                                  Tick sizes and stock market volatility: A regression discontinuity approach              Does a larger tick size (0.05 to 0.10 SEK at 100 SEK) lower daily volatility of OMXS30 stocks?  microstructure                                NASDAQ OMX / SIX Telekurs daily data curated at SSE; Sweden                                    13 stocks, 2,029 stock-days within 90-110 SEK; Jan 2010-Dec 2011  RD at the 100 SEK tick threshold (local linear, bandwidth tests, McCrary-type checks)   Bessembinder (2000 JFI; 2003 JFQA); Ronen & Weaver (2001 JFM) (design, not a table)                                                     no                        yes: RD design, HFT era, Swedish tick regime             18         12               19  no (informal mention of test power)                             mixed (log range +10%; level range null)                             Though the null hypothesis of no change cannot be rejected when the level range is used, the log range specification implies a 10% increase in the range when the tick size is increased
```

### data/extra/ppm_nav_2024.xlsx  (6.12 MB)
- sheets (name, max_row, max_col): [('Kvartal 1', 27827, 10), ('Kvartal 2', 26070, 10), ('Kvartal 3', 27656, 10), ('Kvartal 4', 25817, 10)]
- first 3 rows of sheet 0:
```
('Fondbolag', 'Fondnummer', 'Fondnamn', 'Datum', 'Valutakurs sälj', 'Valutakurs köp', 'Fondkurs sälj', 'Fondkurs köp', 'Fondkurs i SEK köp', 'Fondkurs i SEK sälj')
(None, None, None, None, None, None, None, None, None, None)
('abrdn Investments Luxembourg S.A', '865063', 'abrdn SICAV I - Europe ex UK Sustainable Equity Fund A', datetime.datetime(2024, 1, 2, 0, 0), 11.1168, 11.1183, 20.0171, 20.0171, 222.55612293, 222.52609728)
```

### data/extra/ppm_2023_12.xlsm  (1.95 MB)
- sheets: ['Innehåll', 'Fondval & marknadsvärde', '10 fonder...', 'Fondstatistik', 'Fondstatistik - hållbarhet', 'Värdeutveckling - konto', 'Värdeutv. Premiepensionssystem', 'Värdeutv. fondrörelse per år', 'Marknadsv. & tillfört kapital', 'Värdeutveckling - fondrörelse', 'Värdeutv fondrörelse genomsnitt', 'Avkastning pp-systemet', 'Värdeutveckling per år', 'Index, fondrörelsen', 'Marknadsv. och tillfört kapital', 'Avkastning sedan 2000', 'Beskrivning av mått', 'Info Makro']
- **sheet `Innehåll`**
- rows: 23  cols: 2
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 23)
    - `Unnamed: 1`: 14 unique (nulls 9)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1
0         NaN        NaN
1         NaN        NaN
2         NaN        NaN
```
- **sheet `Fondval & marknadsvärde`**
- rows: 476  cols: 15
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (float64)
    - `Unnamed: 14` (object)
- id-like uniques:
    - `Unnamed: 0`: 462 unique (nulls 14)
    - `Unnamed: 1`: 455 unique (nulls 21)
    - `Unnamed: 2`: 422 unique (nulls 21)
    - `Unnamed: 3`: 437 unique (nulls 20)
    - `Unnamed: 4`: 450 unique (nulls 21)
    - `Unnamed: 5`: 454 unique (nulls 21)
    - `Unnamed: 6`: 456 unique (nulls 20)
    - `Unnamed: 7`: 455 unique (nulls 21)
    - `Unnamed: 8`: 451 unique (nulls 25)
    - `Unnamed: 9`: 36 unique (nulls 21)
    - `Unnamed: 10`: 8 unique (nulls 21)
    - `Unnamed: 11`: 63 unique (nulls 21)
    - `Unnamed: 12`: 3 unique (nulls 20)
    - `Unnamed: 13`: 0 unique (nulls 476)
    - `Unnamed: 14`: 3 unique (nulls 473)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12  Unnamed: 13             Unnamed: 14
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN                     NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN                     NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN  Totalt marknadsvärde  
```
- **sheet `10 fonder...`**
- rows: 51  cols: 10
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 51)
    - `Unnamed: 1`: 30 unique (nulls 12)
    - `Unnamed: 2`: 26 unique (nulls 16)
    - `Unnamed: 3`: 21 unique (nulls 18)
    - `Unnamed: 4`: 23 unique (nulls 18)
    - `Unnamed: 5`: 23 unique (nulls 16)
    - `Unnamed: 6`: 25 unique (nulls 18)
    - `Unnamed: 7`: 26 unique (nulls 18)
    - `Unnamed: 8`: 21 unique (nulls 18)
    - `Unnamed: 9`: 10 unique (nulls 40)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9
0         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN
1         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN
2         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN
```
- **sheet `Fondstatistik`**
- rows: 470  cols: 20
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
- id-like uniques:
    - `Unnamed: 0`: 456 unique (nulls 14)
    - `Unnamed: 1`: 451 unique (nulls 19)
    - `Unnamed: 2`: 61 unique (nulls 22)
    - `Unnamed: 3`: 26 unique (nulls 19)
    - `Unnamed: 4`: 43 unique (nulls 20)
    - `Unnamed: 5`: 35 unique (nulls 24)
    - `Unnamed: 6`: 60 unique (nulls 23)
    - `Unnamed: 7`: 106 unique (nulls 20)
    - `Unnamed: 8`: 138 unique (nulls 35)
    - `Unnamed: 9`: 181 unique (nulls 35)
    - `Unnamed: 10`: 63 unique (nulls 21)
    - `Unnamed: 11`: 149 unique (nulls 22)
    - `Unnamed: 12`: 200 unique (nulls 20)
    - `Unnamed: 13`: 28 unique (nulls 19)
    - `Unnamed: 14`: 7 unique (nulls 18)
    - `Unnamed: 15`: 201 unique (nulls 19)
    - `Unnamed: 16`: 3 unique (nulls 18)
    - `Unnamed: 17`: 451 unique (nulls 19)
    - `Unnamed: 18`: 63 unique (nulls 19)
    - `Unnamed: 19`: 35 unique (nulls 19)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik - hållbarhet`**
- rows: 469  cols: 30
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
    - `Unnamed: 20` (object)
    - `Unnamed: 21` (object)
    - `Unnamed: 22` (object)
    - `Unnamed: 23` (object)
    - `Unnamed: 24` (object)
    - `Unnamed: 25` (object)
    - `Unnamed: 26` (object)
    - `Unnamed: 27` (object)
    - `Unnamed: 28` (object)
    - `Unnamed: 29` (object)
- id-like uniques:
    - `Unnamed: 0`: 455 unique (nulls 14)
    - `Unnamed: 1`: 451 unique (nulls 18)
    - `Unnamed: 2`: 2 unique (nulls 439)
    - `Unnamed: 3`: 2 unique (nulls 152)
    - `Unnamed: 4`: 2 unique (nulls 443)
    - `Unnamed: 5`: 23 unique (nulls 25)
    - `Unnamed: 6`: 9 unique (nulls 25)
    - `Unnamed: 7`: 3 unique (nulls 19)
    - `Unnamed: 8`: 14 unique (nulls 19)
    - `Unnamed: 9`: 4 unique (nulls 18)
    - `Unnamed: 10`: 4 unique (nulls 18)
    - `Unnamed: 11`: 4 unique (nulls 18)
    - `Unnamed: 12`: 4 unique (nulls 18)
    - `Unnamed: 13`: 4 unique (nulls 18)
    - `Unnamed: 14`: 4 unique (nulls 18)
    - `Unnamed: 15`: 4 unique (nulls 18)
    - `Unnamed: 16`: 4 unique (nulls 18)
    - `Unnamed: 17`: 4 unique (nulls 18)
    - `Unnamed: 18`: 4 unique (nulls 18)
    - `Unnamed: 19`: 4 unique (nulls 18)
    - `Unnamed: 20`: 4 unique (nulls 18)
    - `Unnamed: 21`: 4 unique (nulls 18)
    - `Unnamed: 22`: 4 unique (nulls 18)
    - `Unnamed: 23`: 4 unique (nulls 18)
    - `Unnamed: 24`: 4 unique (nulls 18)
    - `Unnamed: 25`: 4 unique (nulls 18)
    - `Unnamed: 26`: 4 unique (nulls 18)
    - `Unnamed: 27`: 4 unique (nulls 18)
    - `Unnamed: 28`: 4 unique (nulls 18)
    - `Unnamed: 29`: 4 unique (nulls 18)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19 Unnamed: 20 Unnamed: 21 Unnamed: 22 Unnamed: 23 Unnamed: 24 Unnamed: 25 Unnamed: 26 Unnamed: 27 Unnamed: 28 Unnamed: 29
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Värdeutveckling - konto`**
- rows: 44  cols: 3
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (float64)
    - `Unnamed: 2` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 44)
    - `Unnamed: 1`: 0 unique (nulls 44)
    - `Unnamed: 2`: 5 unique (nulls 39)
- first 3 rows:
```
   Unnamed: 0  Unnamed: 1 Unnamed: 2
0         NaN         NaN        NaN
1         NaN         NaN        NaN
2         NaN         NaN        NaN
```

### data/extra/ppm_2024_03.xlsm  (1.73 MB)
- sheets: ['Innehåll', 'Fondval & marknadsvärde', '10 fonder...', 'Fondstatistik', 'Fondstatistik - hållbarhet', 'Värdeutveckling - konto', 'Värdeutv. Premiepensionssystem', 'Värdeutv. fondrörelse per år', 'Marknadsv. & tillfört kapital', 'Värdeutveckling - fondrörelse', 'Värdeutv fondrörelse genomsnitt', 'Avkastning pp-systemet', 'Värdeutveckling per år', 'Index, fondrörelsen', 'Marknadsv. och tillfört kapital', 'Avkastning sedan 2000', 'Beskrivning av mått', 'Info Makro']
- **sheet `Innehåll`**
- rows: 23  cols: 2
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 23)
    - `Unnamed: 1`: 14 unique (nulls 9)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1
0         NaN        NaN
1         NaN        NaN
2         NaN        NaN
```
- **sheet `Fondval & marknadsvärde`**
- rows: 471  cols: 15
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (float64)
    - `Unnamed: 14` (object)
- id-like uniques:
    - `Unnamed: 0`: 457 unique (nulls 14)
    - `Unnamed: 1`: 450 unique (nulls 21)
    - `Unnamed: 2`: 426 unique (nulls 21)
    - `Unnamed: 3`: 427 unique (nulls 20)
    - `Unnamed: 4`: 442 unique (nulls 21)
    - `Unnamed: 5`: 450 unique (nulls 21)
    - `Unnamed: 6`: 451 unique (nulls 20)
    - `Unnamed: 7`: 450 unique (nulls 21)
    - `Unnamed: 8`: 446 unique (nulls 25)
    - `Unnamed: 9`: 36 unique (nulls 21)
    - `Unnamed: 10`: 8 unique (nulls 21)
    - `Unnamed: 11`: 63 unique (nulls 21)
    - `Unnamed: 12`: 3 unique (nulls 20)
    - `Unnamed: 13`: 0 unique (nulls 471)
    - `Unnamed: 14`: 3 unique (nulls 468)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12  Unnamed: 13             Unnamed: 14
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN                     NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN                     NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN  Totalt marknadsvärde  
```
- **sheet `10 fonder...`**
- rows: 84  cols: 13
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 84)
    - `Unnamed: 1`: 28 unique (nulls 13)
    - `Unnamed: 2`: 22 unique (nulls 16)
    - `Unnamed: 3`: 20 unique (nulls 18)
    - `Unnamed: 4`: 21 unique (nulls 18)
    - `Unnamed: 5`: 25 unique (nulls 16)
    - `Unnamed: 6`: 25 unique (nulls 18)
    - `Unnamed: 7`: 24 unique (nulls 18)
    - `Unnamed: 8`: 21 unique (nulls 40)
    - `Unnamed: 9`: 10 unique (nulls 62)
    - `Unnamed: 10`: 11 unique (nulls 51)
    - `Unnamed: 11`: 31 unique (nulls 51)
    - `Unnamed: 12`: 24 unique (nulls 51)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12
0         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN
1         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN
2         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik`**
- rows: 465  cols: 20
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
- id-like uniques:
    - `Unnamed: 0`: 451 unique (nulls 14)
    - `Unnamed: 1`: 446 unique (nulls 19)
    - `Unnamed: 2`: 32 unique (nulls 19)
    - `Unnamed: 3`: 19 unique (nulls 26)
    - `Unnamed: 4`: 31 unique (nulls 20)
    - `Unnamed: 5`: 47 unique (nulls 20)
    - `Unnamed: 6`: 65 unique (nulls 24)
    - `Unnamed: 7`: 104 unique (nulls 20)
    - `Unnamed: 8`: 145 unique (nulls 32)
    - `Unnamed: 9`: 190 unique (nulls 32)
    - `Unnamed: 10`: 63 unique (nulls 18)
    - `Unnamed: 11`: 145 unique (nulls 19)
    - `Unnamed: 12`: 197 unique (nulls 20)
    - `Unnamed: 13`: 29 unique (nulls 19)
    - `Unnamed: 14`: 7 unique (nulls 18)
    - `Unnamed: 15`: 197 unique (nulls 19)
    - `Unnamed: 16`: 3 unique (nulls 18)
    - `Unnamed: 17`: 446 unique (nulls 19)
    - `Unnamed: 18`: 63 unique (nulls 19)
    - `Unnamed: 19`: 35 unique (nulls 19)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik - hållbarhet`**
- rows: 464  cols: 30
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
    - `Unnamed: 20` (object)
    - `Unnamed: 21` (object)
    - `Unnamed: 22` (object)
    - `Unnamed: 23` (object)
    - `Unnamed: 24` (object)
    - `Unnamed: 25` (object)
    - `Unnamed: 26` (object)
    - `Unnamed: 27` (object)
    - `Unnamed: 28` (object)
    - `Unnamed: 29` (object)
- id-like uniques:
    - `Unnamed: 0`: 450 unique (nulls 14)
    - `Unnamed: 1`: 446 unique (nulls 18)
    - `Unnamed: 2`: 2 unique (nulls 435)
    - `Unnamed: 3`: 2 unique (nulls 114)
    - `Unnamed: 4`: 2 unique (nulls 436)
    - `Unnamed: 5`: 23 unique (nulls 24)
    - `Unnamed: 6`: 7 unique (nulls 24)
    - `Unnamed: 7`: 3 unique (nulls 19)
    - `Unnamed: 8`: 15 unique (nulls 19)
    - `Unnamed: 9`: 4 unique (nulls 18)
    - `Unnamed: 10`: 4 unique (nulls 18)
    - `Unnamed: 11`: 4 unique (nulls 18)
    - `Unnamed: 12`: 4 unique (nulls 18)
    - `Unnamed: 13`: 4 unique (nulls 18)
    - `Unnamed: 14`: 4 unique (nulls 18)
    - `Unnamed: 15`: 4 unique (nulls 18)
    - `Unnamed: 16`: 4 unique (nulls 18)
    - `Unnamed: 17`: 4 unique (nulls 18)
    - `Unnamed: 18`: 4 unique (nulls 18)
    - `Unnamed: 19`: 4 unique (nulls 18)
    - `Unnamed: 20`: 4 unique (nulls 18)
    - `Unnamed: 21`: 4 unique (nulls 18)
    - `Unnamed: 22`: 4 unique (nulls 18)
    - `Unnamed: 23`: 4 unique (nulls 18)
    - `Unnamed: 24`: 4 unique (nulls 18)
    - `Unnamed: 25`: 4 unique (nulls 18)
    - `Unnamed: 26`: 4 unique (nulls 18)
    - `Unnamed: 27`: 4 unique (nulls 18)
    - `Unnamed: 28`: 4 unique (nulls 18)
    - `Unnamed: 29`: 4 unique (nulls 18)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19 Unnamed: 20 Unnamed: 21 Unnamed: 22 Unnamed: 23 Unnamed: 24 Unnamed: 25 Unnamed: 26 Unnamed: 27 Unnamed: 28 Unnamed: 29
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Värdeutveckling - konto`**
- rows: 44  cols: 3
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (float64)
    - `Unnamed: 2` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 44)
    - `Unnamed: 1`: 0 unique (nulls 44)
    - `Unnamed: 2`: 5 unique (nulls 39)
- first 3 rows:
```
   Unnamed: 0  Unnamed: 1 Unnamed: 2
0         NaN         NaN        NaN
1         NaN         NaN        NaN
2         NaN         NaN        NaN
```

### data/extra/ppm_2024_06.xlsm  (1.74 MB)
- sheets: ['Innehåll', 'Fondval & marknadsvärde', '10 fonder...', 'Fondstatistik', 'Fondstatistik - hållbarhet', 'Värdeutveckling - konto', 'Värdeutv. Premiepensionssystem', 'Värdeutv. fondrörelse per år', 'Marknadsv. & tillfört kapital', 'Värdeutveckling - fondrörelse', 'Värdeutv fondrörelse genomsnitt', 'Avkastning pp-systemet', 'Värdeutveckling per år', 'Index, fondrörelsen', 'Marknadsv. och tillfört kapital', 'Avkastning sedan 2000', 'Beskrivning av mått', 'Info Makro']
- **sheet `Innehåll`**
- rows: 23  cols: 2
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 23)
    - `Unnamed: 1`: 14 unique (nulls 9)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1
0         NaN        NaN
1         NaN        NaN
2         NaN        NaN
```
- **sheet `Fondval & marknadsvärde`**
- rows: 458  cols: 15
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (float64)
    - `Unnamed: 14` (object)
- id-like uniques:
    - `Unnamed: 0`: 444 unique (nulls 14)
    - `Unnamed: 1`: 438 unique (nulls 20)
    - `Unnamed: 2`: 417 unique (nulls 21)
    - `Unnamed: 3`: 419 unique (nulls 20)
    - `Unnamed: 4`: 431 unique (nulls 21)
    - `Unnamed: 5`: 437 unique (nulls 21)
    - `Unnamed: 6`: 438 unique (nulls 20)
    - `Unnamed: 7`: 437 unique (nulls 21)
    - `Unnamed: 8`: 429 unique (nulls 25)
    - `Unnamed: 9`: 36 unique (nulls 21)
    - `Unnamed: 10`: 8 unique (nulls 21)
    - `Unnamed: 11`: 63 unique (nulls 21)
    - `Unnamed: 12`: 3 unique (nulls 20)
    - `Unnamed: 13`: 0 unique (nulls 458)
    - `Unnamed: 14`: 3 unique (nulls 455)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12  Unnamed: 13             Unnamed: 14
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN                     NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN                     NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN          NaN  Totalt marknadsvärde  
```
- **sheet `10 fonder...`**
- rows: 84  cols: 14
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 84)
    - `Unnamed: 1`: 29 unique (nulls 13)
    - `Unnamed: 2`: 25 unique (nulls 16)
    - `Unnamed: 3`: 24 unique (nulls 18)
    - `Unnamed: 4`: 24 unique (nulls 18)
    - `Unnamed: 5`: 25 unique (nulls 16)
    - `Unnamed: 6`: 22 unique (nulls 18)
    - `Unnamed: 7`: 23 unique (nulls 18)
    - `Unnamed: 8`: 22 unique (nulls 40)
    - `Unnamed: 9`: 11 unique (nulls 62)
    - `Unnamed: 10`: 11 unique (nulls 51)
    - `Unnamed: 11`: 33 unique (nulls 51)
    - `Unnamed: 12`: 17 unique (nulls 51)
    - `Unnamed: 13`: 11 unique (nulls 73)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13
0         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
1         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
2         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik`**
- rows: 455  cols: 20
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
- id-like uniques:
    - `Unnamed: 0`: 441 unique (nulls 14)
    - `Unnamed: 1`: 436 unique (nulls 19)
    - `Unnamed: 2`: 39 unique (nulls 24)
    - `Unnamed: 3`: 21 unique (nulls 20)
    - `Unnamed: 4`: 27 unique (nulls 24)
    - `Unnamed: 5`: 38 unique (nulls 25)
    - `Unnamed: 6`: 53 unique (nulls 29)
    - `Unnamed: 7`: 102 unique (nulls 21)
    - `Unnamed: 8`: 139 unique (nulls 29)
    - `Unnamed: 9`: 188 unique (nulls 29)
    - `Unnamed: 10`: 63 unique (nulls 23)
    - `Unnamed: 11`: 145 unique (nulls 24)
    - `Unnamed: 12`: 195 unique (nulls 21)
    - `Unnamed: 13`: 28 unique (nulls 20)
    - `Unnamed: 14`: 7 unique (nulls 18)
    - `Unnamed: 15`: 191 unique (nulls 19)
    - `Unnamed: 16`: 3 unique (nulls 18)
    - `Unnamed: 17`: 436 unique (nulls 19)
    - `Unnamed: 18`: 63 unique (nulls 19)
    - `Unnamed: 19`: 35 unique (nulls 19)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik - hållbarhet`**
- rows: 454  cols: 30
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
    - `Unnamed: 20` (object)
    - `Unnamed: 21` (object)
    - `Unnamed: 22` (object)
    - `Unnamed: 23` (object)
    - `Unnamed: 24` (object)
    - `Unnamed: 25` (object)
    - `Unnamed: 26` (object)
    - `Unnamed: 27` (object)
    - `Unnamed: 28` (object)
    - `Unnamed: 29` (object)
- id-like uniques:
    - `Unnamed: 0`: 440 unique (nulls 14)
    - `Unnamed: 1`: 436 unique (nulls 18)
    - `Unnamed: 2`: 2 unique (nulls 423)
    - `Unnamed: 3`: 2 unique (nulls 96)
    - `Unnamed: 4`: 2 unique (nulls 418)
    - `Unnamed: 5`: 23 unique (nulls 23)
    - `Unnamed: 6`: 7 unique (nulls 23)
    - `Unnamed: 7`: 3 unique (nulls 18)
    - `Unnamed: 8`: 12 unique (nulls 18)
    - `Unnamed: 9`: 4 unique (nulls 18)
    - `Unnamed: 10`: 4 unique (nulls 18)
    - `Unnamed: 11`: 4 unique (nulls 18)
    - `Unnamed: 12`: 4 unique (nulls 18)
    - `Unnamed: 13`: 4 unique (nulls 18)
    - `Unnamed: 14`: 4 unique (nulls 18)
    - `Unnamed: 15`: 4 unique (nulls 18)
    - `Unnamed: 16`: 4 unique (nulls 18)
    - `Unnamed: 17`: 4 unique (nulls 18)
    - `Unnamed: 18`: 4 unique (nulls 18)
    - `Unnamed: 19`: 4 unique (nulls 18)
    - `Unnamed: 20`: 4 unique (nulls 18)
    - `Unnamed: 21`: 4 unique (nulls 18)
    - `Unnamed: 22`: 4 unique (nulls 18)
    - `Unnamed: 23`: 4 unique (nulls 18)
    - `Unnamed: 24`: 4 unique (nulls 18)
    - `Unnamed: 25`: 4 unique (nulls 18)
    - `Unnamed: 26`: 4 unique (nulls 18)
    - `Unnamed: 27`: 4 unique (nulls 18)
    - `Unnamed: 28`: 4 unique (nulls 18)
    - `Unnamed: 29`: 4 unique (nulls 18)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19 Unnamed: 20 Unnamed: 21 Unnamed: 22 Unnamed: 23 Unnamed: 24 Unnamed: 25 Unnamed: 26 Unnamed: 27 Unnamed: 28 Unnamed: 29
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Värdeutveckling - konto`**
- rows: 44  cols: 3
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (float64)
    - `Unnamed: 2` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 44)
    - `Unnamed: 1`: 0 unique (nulls 44)
    - `Unnamed: 2`: 5 unique (nulls 39)
- first 3 rows:
```
   Unnamed: 0  Unnamed: 1 Unnamed: 2
0         NaN         NaN        NaN
1         NaN         NaN        NaN
2         NaN         NaN        NaN
```

### data/extra/ppm_2026_06.xlsm  (1.76 MB)
- sheets: ['Innehåll', 'Fondval & marknadsvärde', '10 fonder...', 'Fondstatistik', 'Fondstatistik - hållbarhet', 'Värdeutveckling - konto', 'Värdeutv. Premiepensionssystem', 'Värdeutv. fondrörelse per år', 'Marknadsv. & tillfört kapital', 'Värdeutveckling - fondrörelse', 'Värdeutv fondrörelse genomsnitt', 'Avkastning pp-systemet', 'Värdeutveckling per år', 'Index, fondrörelsen', 'Marknadsv. och tillfört kapital', 'Avkastning sedan 2000', 'Beskrivning av mått', 'Info Makro']
- **sheet `Innehåll`**
- rows: 23  cols: 2
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 23)
    - `Unnamed: 1`: 15 unique (nulls 8)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1
0         NaN        NaN
1         NaN        NaN
2         NaN        NaN
```
- **sheet `Fondval & marknadsvärde`**
- rows: 400  cols: 17
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (float64)
    - `Unnamed: 16` (object)
- id-like uniques:
    - `Unnamed: 0`: 386 unique (nulls 14)
    - `Unnamed: 1`: 381 unique (nulls 19)
    - `Unnamed: 2`: 363 unique (nulls 20)
    - `Unnamed: 3`: 372 unique (nulls 19)
    - `Unnamed: 4`: 375 unique (nulls 20)
    - `Unnamed: 5`: 380 unique (nulls 20)
    - `Unnamed: 6`: 381 unique (nulls 19)
    - `Unnamed: 7`: 380 unique (nulls 20)
    - `Unnamed: 8`: 375 unique (nulls 25)
    - `Unnamed: 9`: 37 unique (nulls 21)
    - `Unnamed: 10`: 8 unique (nulls 21)
    - `Unnamed: 11`: 57 unique (nulls 21)
    - `Unnamed: 12`: 3 unique (nulls 20)
    - `Unnamed: 13`: 3 unique (nulls 20)
    - `Unnamed: 14`: 2 unique (nulls 359)
    - `Unnamed: 15`: 0 unique (nulls 400)
    - `Unnamed: 16`: 3 unique (nulls 397)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14  Unnamed: 15             Unnamed: 16
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN          NaN                     NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN          NaN                     NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN          NaN  Totalt marknadsvärde  
```
- **sheet `10 fonder...`**
- rows: 84  cols: 14
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 84)
    - `Unnamed: 1`: 29 unique (nulls 13)
    - `Unnamed: 2`: 27 unique (nulls 16)
    - `Unnamed: 3`: 26 unique (nulls 18)
    - `Unnamed: 4`: 26 unique (nulls 18)
    - `Unnamed: 5`: 27 unique (nulls 16)
    - `Unnamed: 6`: 26 unique (nulls 18)
    - `Unnamed: 7`: 26 unique (nulls 18)
    - `Unnamed: 8`: 26 unique (nulls 40)
    - `Unnamed: 9`: 11 unique (nulls 62)
    - `Unnamed: 10`: 11 unique (nulls 51)
    - `Unnamed: 11`: 33 unique (nulls 51)
    - `Unnamed: 12`: 17 unique (nulls 51)
    - `Unnamed: 13`: 11 unique (nulls 73)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13
0         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
1         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
2         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik`**
- rows: 394  cols: 22
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
    - `Unnamed: 20` (object)
    - `Unnamed: 21` (object)
- id-like uniques:
    - `Unnamed: 0`: 380 unique (nulls 14)
    - `Unnamed: 1`: 375 unique (nulls 19)
    - `Unnamed: 2`: 376 unique (nulls 18)
    - `Unnamed: 3`: 375 unique (nulls 19)
    - `Unnamed: 4`: 375 unique (nulls 19)
    - `Unnamed: 5`: 375 unique (nulls 19)
    - `Unnamed: 6`: 367 unique (nulls 27)
    - `Unnamed: 7`: 369 unique (nulls 25)
    - `Unnamed: 8`: 368 unique (nulls 26)
    - `Unnamed: 9`: 368 unique (nulls 26)
    - `Unnamed: 10`: 304 unique (nulls 18)
    - `Unnamed: 11`: 308 unique (nulls 19)
    - `Unnamed: 12`: 369 unique (nulls 25)
    - `Unnamed: 13`: 370 unique (nulls 24)
    - `Unnamed: 14`: 7 unique (nulls 18)
    - `Unnamed: 15`: 173 unique (nulls 19)
    - `Unnamed: 16`: 3 unique (nulls 18)
    - `Unnamed: 17`: 2 unique (nulls 353)
    - `Unnamed: 18`: 375 unique (nulls 19)
    - `Unnamed: 19`: 57 unique (nulls 19)
    - `Unnamed: 20`: 3 unique (nulls 18)
    - `Unnamed: 21`: 36 unique (nulls 19)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19 Unnamed: 20 Unnamed: 21
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik - hållbarhet`**
- rows: 452  cols: 28
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
    - `Unnamed: 20` (object)
    - `Unnamed: 21` (object)
    - `Unnamed: 22` (object)
    - `Unnamed: 23` (object)
    - `Unnamed: 24` (object)
    - `Unnamed: 25` (object)
    - `Unnamed: 26` (object)
    - `Unnamed: 27` (object)
- id-like uniques:
    - `Unnamed: 0`: 379 unique (nulls 14)
    - `Unnamed: 1`: 375 unique (nulls 18)
    - `Unnamed: 2`: 2 unique (nulls 422)
    - `Unnamed: 3`: 2 unique (nulls 81)
    - `Unnamed: 4`: 2 unique (nulls 417)
    - `Unnamed: 5`: 22 unique (nulls 22)
    - `Unnamed: 6`: 8 unique (nulls 22)
    - `Unnamed: 7`: 3 unique (nulls 18)
    - `Unnamed: 8`: 3 unique (nulls 18)
    - `Unnamed: 9`: 3 unique (nulls 18)
    - `Unnamed: 10`: 3 unique (nulls 18)
    - `Unnamed: 11`: 3 unique (nulls 18)
    - `Unnamed: 12`: 3 unique (nulls 18)
    - `Unnamed: 13`: 3 unique (nulls 18)
    - `Unnamed: 14`: 3 unique (nulls 18)
    - `Unnamed: 15`: 3 unique (nulls 18)
    - `Unnamed: 16`: 3 unique (nulls 18)
    - `Unnamed: 17`: 3 unique (nulls 18)
    - `Unnamed: 18`: 3 unique (nulls 18)
    - `Unnamed: 19`: 3 unique (nulls 18)
    - `Unnamed: 20`: 3 unique (nulls 18)
    - `Unnamed: 21`: 3 unique (nulls 18)
    - `Unnamed: 22`: 3 unique (nulls 18)
    - `Unnamed: 23`: 3 unique (nulls 18)
    - `Unnamed: 24`: 3 unique (nulls 18)
    - `Unnamed: 25`: 3 unique (nulls 18)
    - `Unnamed: 26`: 3 unique (nulls 18)
    - `Unnamed: 27`: 3 unique (nulls 18)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19 Unnamed: 20 Unnamed: 21 Unnamed: 22 Unnamed: 23 Unnamed: 24 Unnamed: 25 Unnamed: 26 Unnamed: 27
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Värdeutveckling - konto`**
- rows: 44  cols: 3
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (float64)
    - `Unnamed: 2` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 44)
    - `Unnamed: 1`: 0 unique (nulls 44)
    - `Unnamed: 2`: 5 unique (nulls 39)
- first 3 rows:
```
   Unnamed: 0  Unnamed: 1 Unnamed: 2
0         NaN         NaN        NaN
1         NaN         NaN        NaN
2         NaN         NaN        NaN
```

### data/extra/ppm_2026_08.xlsm  (1.77 MB)
- sheets: ['Innehåll', 'Fondval & marknadsvärde', '10 fonder...', 'Fondstatistik', 'Fondstatistik - hållbarhet', 'Värdeutveckling - konto', 'Värdeutv. Premiepensionssystem', 'Värdeutv. fondrörelse per år', 'Marknadsv. & tillfört kapital', 'Värdeutveckling - fondrörelse', 'Värdeutv fondrörelse genomsnitt', 'Avkastning pp-systemet', 'Värdeutveckling per år', 'Index, fondrörelsen', 'Marknadsv. och tillfört kapital', 'Avkastning sedan 2000', 'Beskrivning av mått', 'Info Makro']
- **sheet `Innehåll`**
- rows: 23  cols: 2
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 23)
    - `Unnamed: 1`: 15 unique (nulls 8)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1
0         NaN        NaN
1         NaN        NaN
2         NaN        NaN
```
- **sheet `Fondval & marknadsvärde`**
- rows: 403  cols: 17
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (float64)
    - `Unnamed: 16` (object)
- id-like uniques:
    - `Unnamed: 0`: 389 unique (nulls 14)
    - `Unnamed: 1`: 384 unique (nulls 19)
    - `Unnamed: 2`: 370 unique (nulls 20)
    - `Unnamed: 3`: 368 unique (nulls 19)
    - `Unnamed: 4`: 374 unique (nulls 20)
    - `Unnamed: 5`: 383 unique (nulls 20)
    - `Unnamed: 6`: 384 unique (nulls 19)
    - `Unnamed: 7`: 383 unique (nulls 20)
    - `Unnamed: 8`: 378 unique (nulls 25)
    - `Unnamed: 9`: 37 unique (nulls 21)
    - `Unnamed: 10`: 8 unique (nulls 21)
    - `Unnamed: 11`: 57 unique (nulls 21)
    - `Unnamed: 12`: 3 unique (nulls 20)
    - `Unnamed: 13`: 3 unique (nulls 20)
    - `Unnamed: 14`: 2 unique (nulls 348)
    - `Unnamed: 15`: 0 unique (nulls 403)
    - `Unnamed: 16`: 3 unique (nulls 400)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14  Unnamed: 15             Unnamed: 16
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN          NaN                     NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN          NaN                     NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN          NaN  Totalt marknadsvärde  
```
- **sheet `10 fonder...`**
- rows: 84  cols: 14
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 84)
    - `Unnamed: 1`: 29 unique (nulls 13)
    - `Unnamed: 2`: 27 unique (nulls 16)
    - `Unnamed: 3`: 26 unique (nulls 18)
    - `Unnamed: 4`: 26 unique (nulls 18)
    - `Unnamed: 5`: 27 unique (nulls 16)
    - `Unnamed: 6`: 26 unique (nulls 18)
    - `Unnamed: 7`: 26 unique (nulls 18)
    - `Unnamed: 8`: 26 unique (nulls 40)
    - `Unnamed: 9`: 11 unique (nulls 62)
    - `Unnamed: 10`: 11 unique (nulls 51)
    - `Unnamed: 11`: 33 unique (nulls 51)
    - `Unnamed: 12`: 17 unique (nulls 51)
    - `Unnamed: 13`: 11 unique (nulls 73)
- first 3 rows:
```
   Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13
0         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
1         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
2         NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik`**
- rows: 399  cols: 22
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
    - `Unnamed: 20` (object)
    - `Unnamed: 21` (object)
- id-like uniques:
    - `Unnamed: 0`: 385 unique (nulls 14)
    - `Unnamed: 1`: 380 unique (nulls 19)
    - `Unnamed: 2`: 374 unique (nulls 25)
    - `Unnamed: 3`: 380 unique (nulls 19)
    - `Unnamed: 4`: 373 unique (nulls 26)
    - `Unnamed: 5`: 373 unique (nulls 26)
    - `Unnamed: 6`: 365 unique (nulls 34)
    - `Unnamed: 7`: 373 unique (nulls 26)
    - `Unnamed: 8`: 372 unique (nulls 27)
    - `Unnamed: 9`: 372 unique (nulls 27)
    - `Unnamed: 10`: 300 unique (nulls 18)
    - `Unnamed: 11`: 318 unique (nulls 19)
    - `Unnamed: 12`: 373 unique (nulls 26)
    - `Unnamed: 13`: 374 unique (nulls 25)
    - `Unnamed: 14`: 7 unique (nulls 18)
    - `Unnamed: 15`: 174 unique (nulls 19)
    - `Unnamed: 16`: 3 unique (nulls 18)
    - `Unnamed: 17`: 2 unique (nulls 344)
    - `Unnamed: 18`: 380 unique (nulls 19)
    - `Unnamed: 19`: 57 unique (nulls 19)
    - `Unnamed: 20`: 3 unique (nulls 18)
    - `Unnamed: 21`: 36 unique (nulls 19)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19 Unnamed: 20 Unnamed: 21
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Fondstatistik - hållbarhet`**
- rows: 398  cols: 28
- columns (dtype):
    - `Unnamed: 0` (object)
    - `Unnamed: 1` (object)
    - `Unnamed: 2` (object)
    - `Unnamed: 3` (object)
    - `Unnamed: 4` (object)
    - `Unnamed: 5` (object)
    - `Unnamed: 6` (object)
    - `Unnamed: 7` (object)
    - `Unnamed: 8` (object)
    - `Unnamed: 9` (object)
    - `Unnamed: 10` (object)
    - `Unnamed: 11` (object)
    - `Unnamed: 12` (object)
    - `Unnamed: 13` (object)
    - `Unnamed: 14` (object)
    - `Unnamed: 15` (object)
    - `Unnamed: 16` (object)
    - `Unnamed: 17` (object)
    - `Unnamed: 18` (object)
    - `Unnamed: 19` (object)
    - `Unnamed: 20` (object)
    - `Unnamed: 21` (object)
    - `Unnamed: 22` (object)
    - `Unnamed: 23` (object)
    - `Unnamed: 24` (object)
    - `Unnamed: 25` (object)
    - `Unnamed: 26` (object)
    - `Unnamed: 27` (object)
- id-like uniques:
    - `Unnamed: 0`: 384 unique (nulls 14)
    - `Unnamed: 1`: 380 unique (nulls 18)
    - `Unnamed: 2`: 2 unique (nulls 373)
    - `Unnamed: 3`: 2 unique (nulls 70)
    - `Unnamed: 4`: 2 unique (nulls 369)
    - `Unnamed: 5`: 23 unique (nulls 22)
    - `Unnamed: 6`: 7 unique (nulls 22)
    - `Unnamed: 7`: 3 unique (nulls 18)
    - `Unnamed: 8`: 3 unique (nulls 18)
    - `Unnamed: 9`: 3 unique (nulls 18)
    - `Unnamed: 10`: 3 unique (nulls 18)
    - `Unnamed: 11`: 3 unique (nulls 18)
    - `Unnamed: 12`: 3 unique (nulls 18)
    - `Unnamed: 13`: 3 unique (nulls 18)
    - `Unnamed: 14`: 3 unique (nulls 18)
    - `Unnamed: 15`: 3 unique (nulls 18)
    - `Unnamed: 16`: 3 unique (nulls 18)
    - `Unnamed: 17`: 3 unique (nulls 18)
    - `Unnamed: 18`: 3 unique (nulls 18)
    - `Unnamed: 19`: 3 unique (nulls 18)
    - `Unnamed: 20`: 3 unique (nulls 18)
    - `Unnamed: 21`: 3 unique (nulls 18)
    - `Unnamed: 22`: 3 unique (nulls 18)
    - `Unnamed: 23`: 3 unique (nulls 18)
    - `Unnamed: 24`: 3 unique (nulls 18)
    - `Unnamed: 25`: 3 unique (nulls 18)
    - `Unnamed: 26`: 3 unique (nulls 18)
    - `Unnamed: 27`: 3 unique (nulls 18)
- first 3 rows:
```
  Unnamed: 0 Unnamed: 1 Unnamed: 2 Unnamed: 3 Unnamed: 4 Unnamed: 5 Unnamed: 6 Unnamed: 7 Unnamed: 8 Unnamed: 9 Unnamed: 10 Unnamed: 11 Unnamed: 12 Unnamed: 13 Unnamed: 14 Unnamed: 15 Unnamed: 16 Unnamed: 17 Unnamed: 18 Unnamed: 19 Unnamed: 20 Unnamed: 21 Unnamed: 22 Unnamed: 23 Unnamed: 24 Unnamed: 25 Unnamed: 26 Unnamed: 27
0        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
1        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
2        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN        NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
```
- **sheet `Värdeutveckling - konto`**
- rows: 44  cols: 3
- columns (dtype):
    - `Unnamed: 0` (float64)
    - `Unnamed: 1` (float64)
    - `Unnamed: 2` (object)
- id-like uniques:
    - `Unnamed: 0`: 0 unique (nulls 44)
    - `Unnamed: 1`: 0 unique (nulls 44)
    - `Unnamed: 2`: 5 unique (nulls 39)
- first 3 rows:
```
   Unnamed: 0  Unnamed: 1 Unnamed: 2
0         NaN         NaN        NaN
1         NaN         NaN        NaN
2         NaN         NaN        NaN
```

### data/fundmaster.xlsx  (22.06 MB)
- sheets (name, max_row, max_col): [('fundmaster', 80259, 57)]
- first 3 rows of sheet 0:
```
('performanceid', 'secid', 'fundid', 'domicileid', 'company', 'companyname', 'fundname', 'securityname', 'legalstructure', 'shareclasslegalname', 'UCITS', 'inceptiondate', 'status', 'obsoletedate', 'isbasecurrency', 'isoldestclass', 'currencyid', 'incomedistribution', 'accumulateddistribution', 'insurancefund', 'hedgefund', 'fundoffunds', 'exchangetradedshare', 'ISIN', 'currencyspecificISIN', 'ticker', 'olsobors', 'pricingfrequency', 'availableforpensionplan', 'exchangeid', 'institutionalonly', 'pencetraded', 'sociallyconscious', 'legalstructureid', 'moneymarketfund', 'availableforretirementpl
('0P00000AMR', 'F0GBR04ABX', 'FSGBR057UR', 'LUX', '0C0000AFFH', 'Invesco Management S.A.', 'Invesco Pan European Small Cap Equity Fd', 'Invesco Pan European Sm Cp Eq A EUR Acc', 'SICAV', 'Invesco Funds - Invesco Pan European Small Cap Equity Fund A Accumulation EUR', 1, datetime.datetime(1991, 1, 2, 0, 0), 'Active', None, 1, 1, 'EUR', 0, 1, 0, 0, 0, 0, 'LU0028119013', 'LU0028119013', '', 39180, 'D$', 0, 'EX$$$$CCLX', None, None, '', 9, 0, 0, 0, 'Equity', 5, '', None, '', None, datetime.datetime(2021, 5, 5, 0, 0), '', 'Open-end Fund (EU)', 1177156413.9280186, datetime.datetime(2026, 1, 9, 0, 0)
('0P00000AMS', 'F0GBR04ABY', 'FSGBR057US', 'LUX', '0C0000AFFH', 'Invesco Management S.A.', 'Invesco Pan European Equity Fund', 'Invesco Pan European Equity A EUR Acc', 'SICAV', 'Invesco Funds - Invesco Pan European Equity Fund A Accumulation EUR', 1, datetime.datetime(1991, 1, 1, 0, 0), 'Active', None, 1, 1, 'EUR', 0, 1, 0, 0, 0, 0, 'LU0028118809', 'LU0028118809', '', 39181, 'D$', 0, 'EX$$$$CCLX', None, None, '', 9, 0, 0, 0, 'Equity', 5, '', None, '', None, datetime.datetime(2021, 5, 5, 0, 0), '', 'Open-end Fund (EU)', 10922555213.528807, datetime.datetime(2026, 1, 9, 0, 0), 0.067, 0.1014, 0.1
```

### data/Lista alla fonder 2026.xls  (607.7 kB)
- sheets: ['Alla fonder 2026-07-17']
- **sheet `Alla fonder 2026-07-17`**
- rows: 1,932  cols: 16
- columns (dtype):
    - `FONDBOLAG` (object)
    - `FONDNUMMER` (float64)
    - `UPPHANDLAD` (object)
    - `FONDNAMN` (object)
    - `NOTERINGS VALUTA` (object)
    - `FONDAVGIFT` (float64)
    - ` AVGIFT FÖRE
 RABATT` (float64)
    - `KATEGORI` (object)
    - `ISIN/EXTERNT ID` (object)
    - `FOND_I_FOND` (object)
    - `RESULTATBEROENDE` (object)
    - `SLOW` (object)
    - `FÖRLÄNGD` (float64)
    - `STARTDATUM` (object)
    - `AVSLUTSDATUM` (object)
    - `FONDSTATUS` (float64)
- date-like ranges:
    - `STARTDATUM`: 2000-07-05 00:00:00 → 2026-07-07 00:00:00
    - `AVSLUTSDATUM`: 2002-04-11 00:00:00 → 2026-07-06 00:00:00
- id-like uniques:
    - `FONDBOLAG`: 172 unique (nulls 1)
    - `FONDNUMMER`: 1,931 unique (nulls 1)
    - `FONDNAMN`: 1,910 unique (nulls 0)
    - `FONDAVGIFT`: 195 unique (nulls 529)
    - `ISIN/EXTERNT ID`: 1,896 unique (nulls 1)
    - `FOND_I_FOND`: 2 unique (nulls 1)
    - `FONDSTATUS`: 3 unique (nulls 1)
- first 3 rows:
```
                                           FONDBOLAG  FONDNUMMER UPPHANDLAD                                             FONDNAMN NOTERINGS VALUTA  FONDAVGIFT   AVGIFT FÖRE\n RABATT KATEGORI ISIN/EXTERNT ID FOND_I_FOND RESULTATBEROENDE SLOW  FÖRLÄNGD  STARTDATUM AVSLUTSDATUM  FONDSTATUS
0                                                NaN         NaN        NaN                                                    0              NaN         NaN                    NaN      NaN             NaN         NaN              NaN  NaN       NaN         NaN          NaN         NaN
1  Aberdeen International Management Ireland Limited    967125.0        NaN             Aberdeen International Asia Pacific Fund              USD         NaN                   1.87    Asien    IE0004019489           N                N    N       0.0  2004-06-02   2006-04-18         5.0
2  Aberdeen International Management Ireland Limited    705988.0        NaN  Aberdeen International Asian Smaller Companies Fund              USD        1.53                   1.90    Asien    IE0034372742           N                N    N       0.0  2004-10-15   2006-04-18         5.0
```

### thesis2/data/isin_list_lseg.csv  (174.3 kB)
- rows: 4,452  cols: 2
- columns (dtype):
    - `isin` (object)
    - `name` (object)
- id-like uniques:
    - `isin`: 4,452 unique (nulls 0)
    - `name`: 4,383 unique (nulls 0)
- first 3 rows:
```
           isin           name
0  SE0000115446        VOLVO B
1  SE0015811963     Investor B
2  SE0017486889  ATLAS COPCO A
```

### thesis2/data/lseg_input.csv  (159.4 kB)
- rows: 2,901  cols: 4
- columns (dtype):
    - `id` (object)
    - `id_type` (object)
    - `name` (object)
    - `group` (object)
- id-like uniques:
    - `id`: 2,901 unique (nulls 0)
    - `name`: 2,871 unique (nulls 0)
- first 3 rows:
```
          id id_type                          name  group
0   BALDb.ST     RIC   Fastighets AB Balder ser. B  omxsb
1     SAS.ST     RIC                        SAS AB  omxsb
2  BEFSDB.ST     RIC  Black Earth Farming Ltd. SDB  omxsb
```

### thesis2/data/exit_days/exit_days_by_loser.csv  (14.3 kB)
- rows: 78  cols: 19
- columns (dtype):
    - `round` (object)
    - `award` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `kategori` (object)
    - `performanceid` (object)
    - `ccy` (object)
    - `avslutsdatum` (object)
    - `mv_award_msek` (float64)
    - `tna_at_award` (float64)
    - `last_obs` (object)
    - `n_days_window` (int64)
    - `n_big_days` (int64)
    - `big_days` (object)
    - `sum_flow_window_pct` (float64)
    - `sum_big_flow_pct` (float64)
    - `max_single_day_pct` (float64)
    - `pre_year_days_le_minus5` (int64)
    - `pre_year_sd_flow_pct` (float64)
- date-like ranges:
    - `avslutsdatum`: 2024-06-14 00:00:00 → 2026-06-24 00:00:00
    - `last_obs`: 2025-10-24 00:00:00 → 2026-09-30 00:00:00
    - `n_days_window`: 3 → 149
    - `n_big_days`: 0 → 3
    - `big_days`: 2024-06-19:-1.2%/-7.3% → 2026-09-24:-4.0%/-5.6%
    - `max_single_day_pct`: -21.54139933683529 → -0.280905621239607
    - `pre_year_days_le_minus5`: 0 → 2
    - `pre_year_sd_flow_pct`: 0.0435992538403179 → 6.3952446455326175
- id-like uniques:
    - `fondnr`: 78 unique (nulls 0)
    - `fondnamn`: 78 unique (nulls 0)
    - `performanceid`: 78 unique (nulls 0)
- first 3 rows:
```
       round       award  fondnr                       fondnamn kategori performanceid  ccy avslutsdatum  mv_award_msek  tna_at_award    last_obs  n_days_window  n_big_days                 big_days  sum_flow_window_pct  sum_big_flow_pct  max_single_day_pct  pre_year_days_le_minus5  pre_year_sd_flow_pct
0  EU_active  2024-03-25  336826         BL - Equities Europe B   Europa    0P00000KDB  EUR   2024-06-27          698.9  1.244226e+09  2026-09-29             95           1  2024-06-19:-4.9%/-20.2%            -9.753298         -4.937522           -4.937522                        1              0.515617
1  EU_active  2024-03-25  916122    BlackRock - Euro Markets A2   Europa    0P00000AXK  EUR   2024-07-08           89.7           NaN  2026-09-30            103           0                      NaN                  NaN          0.000000                 NaN                        0                   NaN
2  EU_active  2024-03-25  696898  BlackRock - European Value A2   Europa    0P00000X1Y  EUR   2024-07-05           38.9           NaN  2026-09-30            100           0                      NaN                  NaN          0.000000                 NaN                        0                   NaN
```

### thesis2/data/exit_days/losers_daily_valuations.csv  (7.05 MB)
- rows: 84,696  cols: 9
- columns (dtype):
    - `performanceId` (object)
    - `date` (object)
    - `classcurrencyiso` (object)
    - `fundcurrencyiso` (object)
    - `netflowclass` (float64)
    - `netflowfund` (float64)
    - `shares` (float64)
    - `tnaclass` (float64)
    - `tnafund` (float64)
- date-like ranges:
    - `date`: 2018-01-01 00:00:00 → 2026-09-30 00:00:00
- id-like uniques:
    - `performanceId`: 78 unique (nulls 0)
    - `fundcurrencyiso`: 4 unique (nulls 0)
    - `netflowfund`: 61,304 unique (nulls 23,392)
    - `tnafund`: 67,121 unique (nulls 17,445)
- first 3 rows:
```
  performanceId        date classcurrencyiso fundcurrencyiso  netflowclass  netflowfund  shares      tnaclass  tnafund
0    0P00000AXK  2018-01-02              EUR             EUR    974741.129          NaN     NaN  1.467140e+09      NaN
1    0P00000AXK  2018-01-03              EUR             EUR   -257143.286          NaN     NaN  1.476203e+09      NaN
2    0P00000AXK  2018-01-04              EUR             EUR   2025099.217          NaN     NaN  1.501769e+09      NaN
```

### thesis2/data/omxsb/omxs30_changes_2005_2026.csv  (20.0 kB)
- rows: 48  cols: 13
- columns (dtype):
    - `event_id` (object)
    - `effective_date` (object)
    - `announcement_date` (object)
    - `company` (object)
    - `ticker` (object)
    - `isin` (object)
    - `type` (object)
    - `reason` (object)
    - `review_cycle` (object)
    - `source_url` (object)
    - `source_type` (object)
    - `verification` (object)
    - `notes` (object)
- date-like ranges:
    - `effective_date`: 2006-07-03 00:00:00 → 2025-07-01 00:00:00
    - `announcement_date`: 2006-12-27 00:00:00 → 2025-06-23 00:00:00
- id-like uniques:
    - `event_id`: 48 unique (nulls 0)
    - `company`: 36 unique (nulls 0)
    - `ticker`: 34 unique (nulls 1)
    - `isin`: 27 unique (nulls 11)
- first 3 rows:
```
  event_id effective_date announcement_date                           company ticker          isin      type                                                                                             reason review_cycle                             source_url                                                                                                        source_type verification                                                                                                                                                                                                                                                                                                                                                                                                                  notes
0     E001            NaN               NaN  Skandia Forsakrings AB (Skandia)   SDIA           NaN  deletion  merger (acquired by Old Mutual plc; offer declared unconditional 26 Jan 2006, completed Feb 2006)    off-cycle  https://news.cision.com/se/old-mutual  company press releases (Old Mutual) + sv.wikipedia OMXS30 table (Old Mutual listed as member excluded 2006-07-03)   UNVERIFIED                                                                                Inferred: Old Mutual plc appears as an OMXS30 member removed at the July 2006 review, so it must have replaced Skandia under the take-over replacement rule, most likely Feb-Mar 2006. No Nasdaq/OMX notice or press report with the exact date was found; dates left blank. Treat as merger event (G&S-type samples normally exclude).
1     E002            NaN               NaN                    Old Mutual plc     OM  GB0007389926  addition                    merger replacement (acquirer of Skandia, secondary listing on Stockholmsborsen)    off-cycle  https://news.cision.com/se/old-mutual                                                    company press releases (Old Mutual) + sv.wikipedia OMXS30 table   UNVERIFIED                                                                                                                                                                                                                                                                                                      See E001. Old Mutual was then removed at the July 2006 review (E006). Exact inclusion date not found; left blank.
2     E003     2006-07-03               NaN                        Boliden AB    BOL           NaN  addition                                                                                 semi-annual review      2006-07   https://sv.wikipedia.org/wiki/OMXS30              sv.wikipedia (citing Dagens Industri 2006-06-30) + two thesis event lists (Gothenburg 2024, SSE 2013)    SECONDARY  Announcement date unresolved: Frantzich & Nilson (2024, Gothenburg) appendix gives 2006-06-03 (a Saturday, probably a keying error); sv.wikipedia cites DI market report of 2006-06-30. Lead time in 2006-07 appears to have been only days. Norin & Parksjo (2013, SSE) appendix lists Boliden and Vostok Nafta inclusions effective 03/07/2006 but Fabege exclusion effective 03/01/2006 (possible day/month slip).
```

### thesis2/data/omxsb/omxsb_changes_2013_2026.csv  (148.1 kB)
- rows: 394  cols: 11
- columns (dtype):
    - `event_id` (object)
    - `effective_date` (object)
    - `announcement_date` (object)
    - `company` (object)
    - `ticker` (object)
    - `isin` (float64)
    - `type` (object)
    - `review_cycle` (object)
    - `source_url` (object)
    - `verification` (object)
    - `notes` (object)
- date-like ranges:
    - `effective_date`: 2013-06-03 00:00:00 → 2026-06-01 00:00:00
    - `announcement_date`: 2013-05-08 00:00:00 → 2026-05-22 00:00:00
- id-like uniques:
    - `event_id`: 394 unique (nulls 0)
    - `company`: 214 unique (nulls 0)
    - `ticker`: 152 unique (nulls 0)
    - `isin`: 0 unique (nulls 394)
- first 3 rows:
```
          event_id effective_date announcement_date                       company   ticker  isin      type review_cycle                                                                                                                               source_url verification                                                                                                                                 notes
0  OMXSB-2013H1-01     2013-06-03        2013-05-08   Fastighets AB Balder ser. B   BALD B   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)
1  OMXSB-2013H1-02     2013-06-03        2013-05-08                        SAS AB      SAS   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)
2  OMXSB-2013H1-03     2013-06-03        2013-05-08  Black Earth Farming Ltd. SDB  BEF SDB   NaN  deletion       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)
```

### thesis2/data/swing/swing_status_2019_purge.csv  (17.7 kB)
- rows: 60  cols: 16
- columns (dtype):
    - `rank_by_max_mv` (int64)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `isin` (object)
    - `forvaltare_panel` (object)
    - `svensk_panel` (object)
    - `domicile` (object)
    - `kategori` (object)
    - `first_month_in_panel` (object)
    - `last_month_in_panel` (object)
    - `mv_max_2018_19_msek` (float64)
    - `mv_last_msek` (float64)
    - `swing_possible_2019` (object)
    - `swing_2019_status` (object)
    - `verification` (object)
    - `notes` (object)
- date-like ranges:
    - `first_month_in_panel`: 2018-01-31 00:00:00 → 2018-07-31 00:00:00
    - `last_month_in_panel`: 2018-11-30 00:00:00 → 2019-09-30 00:00:00
    - `mv_last_msek`: 0.0 → 9463.5
- id-like uniques:
    - `fondnr`: 60 unique (nulls 0)
    - `fondnamn`: 60 unique (nulls 0)
    - `isin`: 60 unique (nulls 0)
- first 3 rows:
```
   rank_by_max_mv  fondnr                                              fondnamn          isin           forvaltare_panel svensk_panel domicile kategori first_month_in_panel last_month_in_panel  mv_max_2018_19_msek  mv_last_msek                         swing_possible_2019 swing_2019_status      verification                                                                                                                                           notes
0               1  740274  Ålandsbanken Premium 100 Global Aktie Placeringsfond  FI4000252317  Ålandsbanken Fondbolag Ab     Utländsk  Finland   Global           2018-01-31          2018-11-30              10385.4        9463.5  YES (foreign UCITS; depends on prospectus)                NO         SECONDARY  Alandsbanken fund-specific rules of 2022 had no swing clause; swing pricing entered the common rules only 16.4.2026. No swing pricing in 2019.
1               2  789271                       Swedbank Robur Sverigefond MEGA  SE0000537771   Swedbank Robur Fonder AB       Svensk   Sweden  Sverige           2018-01-31          2019-03-31               7745.6        7024.9                                          NO                NO  VERIFIED (legal)                                Swedish UCITS: justerat fondandelsvarde not available in law before 1 July 2023 (LVF 4 kap. 10 b, SFS 2023:234).
2               3  753442                        Swedbank Robur Globalfond MEGA  SE0000542839   Swedbank Robur Fonder AB       Svensk   Sweden   Global           2018-01-31          2019-03-31               7566.1        7174.2                                          NO                NO  VERIFIED (legal)                                Swedish UCITS: justerat fondandelsvarde not available in law before 1 July 2023 (LVF 4 kap. 10 b, SFS 2023:234).
```

### thesis2/data/swing/swing_status_ftn_losers.csv  (42.4 kB)
- rows: 78  cols: 20
- columns (dtype):
    - `round` (object)
    - `award` (object)
    - `fondnr` (int64)
    - `fondnamn` (object)
    - `isin` (object)
    - `kategori` (object)
    - `avslutsdatum` (object)
    - `mv_award_msek` (float64)
    - `forvaltare_panel` (object)
    - `svensk_panel` (object)
    - `fund_company` (object)
    - `domicile` (object)
    - `swing_status_at_exit` (object)
    - `swing_since` (object)
    - `max_factor_pct` (object)
    - `applied_disclosed` (object)
    - `evidence_doc_date` (object)
    - `source_url` (object)
    - `verification` (object)
    - `notes` (object)
- date-like ranges:
    - `avslutsdatum`: 2024-06-14 00:00:00 → 2026-06-24 00:00:00
    - `evidence_doc_date`: 2008-06-25 00:00:00 → 2026-10-08 00:00:00
- id-like uniques:
    - `fondnr`: 78 unique (nulls 0)
    - `fondnamn`: 78 unique (nulls 0)
    - `isin`: 78 unique (nulls 0)
    - `fund_company`: 43 unique (nulls 0)
- first 3 rows:
```
       round       award  fondnr                       fondnamn          isin kategori avslutsdatum  mv_award_msek                  forvaltare_panel svensk_panel                                          fund_company    domicile swing_status_at_exit swing_since max_factor_pct applied_disclosed evidence_doc_date                                                       source_url verification                                                                                                                                                                                                                          notes
0  EU_active  2024-03-25  336826         BL - Equities Europe B  LU0093570330   Europa   2024-06-27          698.9  Banque de Luxembourg Investments     Utländsk      Banque de Luxembourg Investments S.A. (BL SICAV)  Luxembourg              UNKNOWN     UNKNOWN        UNKNOWN           UNKNOWN               NaN  https://www.banquedeluxembourginvestments.com/bank/bli/homepage      UNKNOWN                                                                                                                                                          BLI website gives no prospectus link without JS; prospectus not read.
1  EU_active  2024-03-25  916122    BlackRock - Euro Markets A2  LU0093502762   Europa   2024-07-08           89.7         BlackRock Luxembourg S.A.     Utländsk  BlackRock (Luxembourg) S.A. (BlackRock Global Funds)  Luxembourg              UNKNOWN     UNKNOWN        UNKNOWN           UNKNOWN               NaN                                                              NaN      UNKNOWN  BGF prospectus not reachable in this run (blackrock.com fetch failed). Unverified expectation: BGF prospectus permits NAV adjustment (swing pricing) for net flows; must be checked in the BGF prospectus in force June 2024.
2  EU_active  2024-03-25  696898  BlackRock - European Value A2  LU0072462186   Europa   2024-07-05           38.9         BlackRock Luxembourg S.A.     Utländsk  BlackRock (Luxembourg) S.A. (BlackRock Global Funds)  Luxembourg              UNKNOWN     UNKNOWN        UNKNOWN           UNKNOWN               NaN                                                              NaN      UNKNOWN                                                                                                                                                                                                 As for BlackRock Euro Markets.
```

### thesis2/code/codebook/isin_list_lseg.csv  (174.3 kB)
- rows: 4,452  cols: 2
- columns (dtype):
    - `isin` (object)
    - `name` (object)
- id-like uniques:
    - `isin`: 4,452 unique (nulls 0)
    - `name`: 4,383 unique (nulls 0)
- first 3 rows:
```
           isin           name
0  SE0000115446        VOLVO B
1  SE0015811963     Investor B
2  SE0017486889  ATLAS COPCO A
```

### thesis2/code/codebook/isin_list_lseg_v2.csv  (405.4 kB)
- rows: 7,395  cols: 5
- columns (dtype):
    - `isin` (object)
    - `name` (object)
    - `country` (object)
    - `source` (object)
    - `tier` (int64)
- id-like uniques:
    - `isin`: 7,395 unique (nulls 0)
    - `name`: 7,275 unique (nulls 0)
- first 3 rows:
```
           isin                                name country             source  tier
0  BMG0670A1099                      AUTOSTORE HLDS      NO  fi_loser_holdings     1
1  DK0002032978  Nordea Kredit 2% 10-01-2047 SDRO 2      DK           old_list     1
2  DK0004615986                RDKRE Float 10/01/24      DK           old_list     1
```

### thesis2/code/codebook/omxsb_changes_2013_2026.csv  (148.1 kB)
- rows: 394  cols: 11
- columns (dtype):
    - `event_id` (object)
    - `effective_date` (object)
    - `announcement_date` (object)
    - `company` (object)
    - `ticker` (object)
    - `isin` (float64)
    - `type` (object)
    - `review_cycle` (object)
    - `source_url` (object)
    - `verification` (object)
    - `notes` (object)
- date-like ranges:
    - `effective_date`: 2013-06-03 00:00:00 → 2026-06-01 00:00:00
    - `announcement_date`: 2013-05-08 00:00:00 → 2026-05-22 00:00:00
- id-like uniques:
    - `event_id`: 394 unique (nulls 0)
    - `company`: 214 unique (nulls 0)
    - `ticker`: 152 unique (nulls 0)
    - `isin`: 0 unique (nulls 394)
- first 3 rows:
```
          event_id effective_date announcement_date                       company   ticker  isin      type review_cycle                                                                                                                               source_url verification                                                                                                                                 notes
0  OMXSB-2013H1-01     2013-06-03        2013-05-08   Fastighets AB Balder ser. B   BALD B   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)
1  OMXSB-2013H1-02     2013-06-03        2013-05-08                        SAS AB      SAS   NaN  addition       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)
2  OMXSB-2013H1-03     2013-06-03        2013-05-08  Black Earth Farming Ltd. SDB  BEF SDB   NaN  deletion       2013H1  https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/     VERIFIED  Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy); announcement 08:30 CET (pre-open)
```
---

## Appendix C. Directory tree (`find . -maxdepth 4`, sizes in bytes, .git excluded)

```
         608  .
        8196  ./.DS_Store
         448  ./.git
         970  ./.gitignore
         602  ./code.ipynb
         320  ./course_context
        6148  ./course_context/.DS_Store
        3840  ./course_context/CHECKLIST.md
         448  ./course_context/econometrics
     1555737  ./course_context/econometrics/All_slides_Fall_2026.pdf
      151702  ./course_context/econometrics/Econometrics_Course.pdf
      494150  ./course_context/econometrics/Lecture_1_Introduction_and_Cross_section_I.pdf
     1321942  ./course_context/econometrics/Lecture_2_Codes.zip
      462669  ./course_context/econometrics/Lecture_2_Cross_section_and_IV.pdf
     8458777  ./course_context/econometrics/Lecture_3_Codes.zip
      829154  ./course_context/econometrics/Lecture_3_Panel_Methods_and_DID_I.pdf
     3174076  ./course_context/econometrics/Lecture_4_Codes.rar
      995550  ./course_context/econometrics/Lecture_4_DID_II_Portfolio_sorts_and_Event_Study.pdf
        2397  ./course_context/econometrics/MANIFEST.md
        6411  ./course_context/econometrics/README.md
         876  ./course_context/econometrics/SHA256SUMS
       17606  ./course_context/README.md
        2899  ./course_context/REPLICATION_README_TEMPLATE.md
         352  ./course_context/source_materials
       95586  ./course_context/source_materials/front_page.docx
      400153  ./course_context/source_materials/Introduction_to_research_in_finance_Fall_2026_RS.pdf
        1899  ./course_context/source_materials/MANIFEST.md
       54261  ./course_context/source_materials/Setting_up_a_WRDS_account_Fall_2026.pdf
         583  ./course_context/source_materials/SHA256SUMS
        3838  ./course_context/source_materials/SOURCE_NOTES.md
      304019  ./course_context/source_materials/Syllabus_Fall_2026.pdf
      147678  ./course_context/source_materials/Synopsis_Fall_2026.pdf
      288468  ./course_context/source_materials/Tutors_and_topics_Fall_2026.pdf
        2775  ./course_context/SYNOPSIS_TEMPLATE.md
        9941  ./course_context/TUTORS_AND_TOPICS.md
         512  ./data
      291207  ./DATA_INVENTORY_2026-10-26.md
        6148  ./data/.DS_Store
         128  ./data/agent_reports
        5489  ./data/agent_reports/agent_facts_report_raw.md
       11969  ./data/agent_reports/agent_L3_savers_report_raw.md
         128  ./data/derived
         384  ./data/derived/ftn_2026-10-11
      111179  ./data/derived/ftn_2026-10-11/bids_long.csv
        2566  ./data/derived/ftn_2026-10-11/build_ppm.py
       71353  ./data/derived/ftn_2026-10-11/crosswalk_ppm_shof.csv
        1443  ./data/derived/ftn_2026-10-11/ftn_category_fees.csv
     7695250  ./data/derived/ftn_2026-10-11/panel_nonppm_monthly.csv
     6222442  ./data/derived/ftn_2026-10-11/ppm_panel_2022_2026.csv
       17161  ./data/derived/ftn_2026-10-11/reallocation_losers.csv
        3262  ./data/derived/ftn_2026-10-11/reallocation_summary_by_round.csv
       27345  ./data/derived/ftn_2026-10-11/unmatched_for_lseg.csv
      303033  ./data/derived/ftn_2026-10-11/winners_fee_series.csv
         192  ./data/derived/shof_monthly
         335  ./data/derived/shof_monthly/monthly.log
        2560  ./data/derived/shof_monthly/monthly.py
    18862175  ./data/derived/shof_monthly/shof_rips_monthly.csv
    46412887  ./data/derived/shof_monthly/shof_valuations_monthly.csv
         544  ./data/extra
     6127598  ./data/extra/fi_2023q4.zip
     6343912  ./data/extra/fi_2024q1.zip
     6219422  ./data/extra/fi_2024q2.zip
     6693564  ./data/extra/fi_2026q2.zip
     7021934  ./data/extra/ftn_europe_active_2024.pdf
       95667  ./data/extra/ftn_europe_active_2024.txt
     1953942  ./data/extra/ppm_2023_12.xlsm
     1729371  ./data/extra/ppm_2024_03.xlsm
     1736202  ./data/extra/ppm_2024_06.xlsm
     1760199  ./data/extra/ppm_2026_06.xlsm
     1771331  ./data/extra/ppm_2026_08.xlsm
     6119743  ./data/extra/ppm_nav_2024.xlsx
     1496762  ./data/extra/shof_field_definitions.pdf
       46095  ./data/extra/shof_field_definitions.txt
    21924169  ./data/extra/shof_fundmaster.zip
         672  ./data/facts
        3411  ./data/facts/common.py
       10323  ./data/facts/fact1_appeal.py
        4316  ./data/facts/fact1_cum_outflow_by_event_month.csv
        4637  ./data/facts/fact1_GA_losers_fundlevel.csv
        4404  ./data/facts/fact1_GA_monthly.csv
         379  ./data/facts/fact1_GA_vs_control_Mar_Aug26.csv
         957  ./data/facts/fact2_gender_baseline_other_equity.csv
        4869  ./data/facts/fact2_gender_by_round.csv
      170265  ./data/facts/fact2_gender_fundlevel.csv
        6492  ./data/facts/fact2_gender.py
        4986  ./data/facts/fact3_shareclass.py
         845  ./data/facts/fact3_summary.csv
        9225  ./data/facts/fact3_winners_shareclass.csv
       10391  ./data/facts/fact4_losers_moved.csv
        3896  ./data/facts/fact4_savings_by_round.csv
        6238  ./data/facts/fact4_savings.py
        7080  ./data/facts/fact4_winners_fees.csv
        9903  ./data/facts/fact5_concentration.csv
        2807  ./data/facts/fact5_concentration.py
    27084129  ./data/FEES.txt
         416  ./data/FTN
     7021934  ./data/FTN/FTN upphandlingsrapport 25 mars 2024 sve.pdf
     3977096  ./data/FTN/FTN upphandlingsrapport Europa smabolag.pdf
     4620402  ./data/FTN/FTN upphandlingsrapport Global Aktiv SE.pdf
     7810567  ./data/FTN/FTN upphandlingsrapport nordiska aktiefonder SE_2.pdf
     7871125  ./data/FTN/FTN upphandlingsrapport nordiska smabolagsfonder SE.pdf
     5547763  ./data/FTN/FTN upphandlingsrapport Sverige Aktiv SE.pdf
     7143650  ./data/FTN/FTN upphandlingsrapport Sverige Passiv SE.pdf
     4535279  ./data/FTN/FTN upphandlingsrapport Sverige smabolag.pdf
     4071451  ./data/FTN/FTN upphandlingsrapport Teknologi.pdf
     5013313  ./data/FTN/FTN_Upphandlingsrapport_Europa index sv ny.pdf
     5248043  ./data/FTN/FTN_Upphandlingsrapport_Global index sv.pdf
    22063397  ./data/fundmaster.xlsx
      607744  ./data/Lista alla fonder 2026.xls
         928  ./data/measurements
       33241  ./data/measurements/agent2019_build2019.py
       15618  ./data/measurements/agent2019_t2_decomposition_summary.csv
         761  ./data/measurements/agent2019_t3_totals_2019.json
        2782  ./data/measurements/agent2019_t4_side_by_side_ftn.csv
       12119  ./data/measurements/agentA_build.py
        3262  ./data/measurements/agentA_summary_by_round.csv
       17080  ./data/measurements/agentA_task1_round_membership.csv
       17161  ./data/measurements/agentA_task2_loser_decomposition.csv
      158635  ./data/measurements/agentA_task3_monthly_flows_winners_losers.csv
       15936  ./data/measurements/analyze.py
      111179  ./data/measurements/bids_long.csv
        9377  ./data/measurements/execution_windows_monthly.csv
        1851  ./data/measurements/fip_allnames_summary.csv
        4323  ./data/measurements/fip_allnames.py
        4940  ./data/measurements/fip_company_Nordic_active_2024q2_2024q2_actual.csv
        5746  ./data/measurements/fip_company_SE_active_2024q2_2024q2_actual.csv
        5797  ./data/measurements/fip_company_SE_active_2024q2_2024q2_equal_new.csv
        5807  ./data/measurements/fip_company_SE_active_2026q2_2026q2_actual.csv
        5923  ./data/measurements/fip_company_SE_index_2024q2_2026q2_actual.csv
        5755  ./data/measurements/fip_company_SE_index_2026q2_2026q2_actual_AvanzaZeroOnly.csv
        6082  ./data/measurements/fip_company_SE_index_2026q2_2026q2_actual_exAvanzaZero.csv
        5947  ./data/measurements/fip_company_SE_index_2026q2_2026q2_actual.csv
        1530  ./data/measurements/fip_summary.csv
        6546  ./data/measurements/fip.py
       14766  ./data/measurements/fund_fi_mapping.csv
        4171  ./data/measurements/parse_fi.py
      303033  ./data/measurements/winners_fee_series.csv
         128  ./data/panel
        2564  ./data/panel/build_ppm_2018.py
    12899027  ./data/panel/ppm_panel_2018_2026.csv
         192  ./data/raw
         320  ./data/raw/2001-2008
         448  ./data/raw/2001-2008/2001
         448  ./data/raw/2001-2008/2002
         448  ./data/raw/2001-2008/2003
         448  ./data/raw/2001-2008/2004
         448  ./data/raw/2001-2008/2005
         416  ./data/raw/2001-2008/2006
         448  ./data/raw/2001-2008/2007
         448  ./data/raw/2001-2008/2008
         256  ./data/raw/2009-2014
         448  ./data/raw/2009-2014/2009
         448  ./data/raw/2009-2014/2010
         448  ./data/raw/2009-2014/2011
         448  ./data/raw/2009-2014/2012
         448  ./data/raw/2009-2014/2013
         448  ./data/raw/2009-2014/2014
         256  ./data/raw/2015-2020
         448  ./data/raw/2015-2020/2015
         448  ./data/raw/2015-2020/2016
         480  ./data/raw/2015-2020/2017
         448  ./data/raw/2015-2020/2018
         448  ./data/raw/2015-2020/2019
         448  ./data/raw/2015-2020/2020
         256  ./data/raw/2021-2026
         448  ./data/raw/2021-2026/2021
         448  ./data/raw/2021-2026/2022
         448  ./data/raw/2021-2026/2023
         448  ./data/raw/2021-2026/2024
         448  ./data/raw/2021-2026/2025
         320  ./data/raw/2021-2026/2026
        1376  ./data/senastedata
        6148  ./data/senastedata/.DS_Store
     1116770  ./data/senastedata/code.ipynb
    76225647  ./data/senastedata/drive-download-20261025T185638Z-1-001.zip
     4916094  ./data/senastedata/Fondinnehav_2018Q4_2022-11-16 17.05.zip
     4841204  ./data/senastedata/Fondinnehav_2019Q1_2022-11-16 17.35.zip
     4790083  ./data/senastedata/Fondinnehav_2019Q2_2022-11-16 15.35.zip
     4897170  ./data/senastedata/Fondinnehav_2019Q3_2022-11-11 15.05.zip
     4947171  ./data/senastedata/Fondinnehav_2019Q4_2022-10-28 14.04.zip
     5077514  ./data/senastedata/Fondinnehav_2020Q1_2022-10-28 14.34.zip
     5128810  ./data/senastedata/Fondinnehav_2020Q2_2022-10-28 14.34.zip
     5147926  ./data/senastedata/Fondinnehav_2020Q3_2022-10-31 15.06.zip
     5185203  ./data/senastedata/Fondinnehav_2020Q4_2022-10-28 14.34.zip
     5336201  ./data/senastedata/Fondinnehav_2021Q1_2022-10-31 17.36.zip
     5259707  ./data/senastedata/Fondinnehav_2021Q2_2022-10-28 15.04.zip
     5302501  ./data/senastedata/Fondinnehav_2021Q3_2022-10-28 15.04.zip
     5523642  ./data/senastedata/Fondinnehav_2021Q4_2022-10-28 15.04.zip
     5537738  ./data/senastedata/Fondinnehav_2022Q1_2023-02-22 14.30.zip
     5557653  ./data/senastedata/Fondinnehav_2022Q2_2023-02-22 14.30.zip
     5391662  ./data/senastedata/Fondinnehav_2022Q3_2023-02-22 14.30.zip
     5792909  ./data/senastedata/Fondinnehav_2022Q4_2023-02-28 09.36.zip
     5880418  ./data/senastedata/Fondinnehav_2023Q1_2023-05-08 11.33.zip
     5886629  ./data/senastedata/Fondinnehav_2023Q2_2023-09-08 11.02.zip
     5885808  ./data/senastedata/Fondinnehav_2023Q3_2023-12-21 10.32.zip
     6201649  ./data/senastedata/Fondinnehav_2023Q4_2026-10-14 08.07.zip
     6416719  ./data/senastedata/Fondinnehav_2024Q1_2026-10-14 08.07.zip
     6291417  ./data/senastedata/Fondinnehav_2024Q2_2026-10-14 08.07.zip
     6294418  ./data/senastedata/Fondinnehav_2024Q3_2026-10-14 08.07.zip
     6255739  ./data/senastedata/Fondinnehav_2024Q4_2026-10-14 08.12.zip
     6248940  ./data/senastedata/Fondinnehav_2025Q1_2026-10-14 08.12.zip
     6298824  ./data/senastedata/Fondinnehav_2025Q2_2026-10-14 08.12.zip
     6102850  ./data/senastedata/Fondinnehav_2025Q3_2026-10-14 08.12.zip
     6235990  ./data/senastedata/Fondinnehav_2025Q4_2026-10-14 08.12.zip
     6439375  ./data/senastedata/Fondinnehav_2026Q1_2026-10-14 08.12.zip
     6693565  ./data/senastedata/Fondinnehav_2026Q2_2026-10-14 08.12.zip
      613061  ./data/senastedata/indices_daily.csv
    33474381  ./data/senastedata/LSEG DATOR-20261025T183134Z-1-001.zip
      152663  ./data/senastedata/omxsb_events_with_ric.csv
         352  ./data/senastedata/output
      317624  ./data/senastedata/output/events_car.csv
        2377  ./data/senastedata/output/exhibits_manifest.md
   106222728  ./data/senastedata/output/fi_holdings_long.csv.gz
         640  ./data/senastedata/output/figures
       48309  ./data/senastedata/output/holdings_price_check.csv
        3616  ./data/senastedata/output/index_funds.csv
       75897  ./data/senastedata/output/nettrading_omxsb.csv
         724  ./data/senastedata/output/numbers.json
        1216  ./data/senastedata/output/tables
    76024714  ./data/senastedata/stocks_daily.csv.gz
      118427  ./data/senastedata/stocks_static.csv
        6781  ./data/senastedata/td_failures.csv
         128  ./data/winners
       16191  ./data/winners/course_intro.txt
       21830  ./data/winners/winners_table.csv
         224  ./non_winners
     1126194  ./non_winners/catalogue_index.json
       49293  ./non_winners/extraction_meta.json
      145917  ./non_winners/INDEX.md
       20384  ./non_winners/text
      205301  ./non_winners/text/1000.txt
      127954  ./non_winners/text/1002.txt
      113248  ./non_winners/text/1003.txt
      116707  ./non_winners/text/1004.txt
      164397  ./non_winners/text/1005.txt
      127876  ./non_winners/text/1006.txt
       91068  ./non_winners/text/1008.txt
      112316  ./non_winners/text/1009.txt
       96019  ./non_winners/text/1010.txt
       50666  ./non_winners/text/1011.txt
       43058  ./non_winners/text/1013.txt
      138073  ./non_winners/text/1014.txt
       49189  ./non_winners/text/1016.txt
      106805  ./non_winners/text/1019.txt
      109620  ./non_winners/text/1020.txt
      117914  ./non_winners/text/1025.txt
      123387  ./non_winners/text/1027.txt
      134807  ./non_winners/text/1028.txt
       52547  ./non_winners/text/1045.txt
      112538  ./non_winners/text/1112.txt
       70514  ./non_winners/text/1250.txt
       82221  ./non_winners/text/1252.txt
       61239  ./non_winners/text/1266.txt
       64960  ./non_winners/text/1267.txt
       72294  ./non_winners/text/1268.txt
      136152  ./non_winners/text/1269.txt
       69077  ./non_winners/text/1270.txt
       78204  ./non_winners/text/1280.txt
      143962  ./non_winners/text/1287.txt
      109249  ./non_winners/text/1288.txt
      126412  ./non_winners/text/1289.txt
      132656  ./non_winners/text/1297.txt
       92790  ./non_winners/text/1299.txt
      117434  ./non_winners/text/1300.txt
      106392  ./non_winners/text/1302.txt
      163654  ./non_winners/text/1303.txt
       85050  ./non_winners/text/1304.txt
      121745  ./non_winners/text/1305.txt
      114995  ./non_winners/text/1306.txt
       87698  ./non_winners/text/1307.txt
      169805  ./non_winners/text/1319.txt
       86029  ./non_winners/text/1457.txt
      122215  ./non_winners/text/1462.txt
      111937  ./non_winners/text/1463.txt
      166666  ./non_winners/text/1474.txt
       63308  ./non_winners/text/1482.txt
       91231  ./non_winners/text/1637.txt
       85689  ./non_winners/text/1643.txt
      160724  ./non_winners/text/1645.txt
      117132  ./non_winners/text/1646.txt
       83936  ./non_winners/text/1647.txt
      123013  ./non_winners/text/1648.txt
      126459  ./non_winners/text/1649.txt
       98003  ./non_winners/text/1650.txt
       63928  ./non_winners/text/1654.txt
      112108  ./non_winners/text/1655.txt
       93323  ./non_winners/text/1656.txt
       84086  ./non_winners/text/1657.txt
      140140  ./non_winners/text/1658.txt
      121668  ./non_winners/text/1659.txt
       56508  ./non_winners/text/1660.txt
      159531  ./non_winners/text/1661.txt
       59670  ./non_winners/text/1662.txt
      563975  ./non_winners/text/1663.txt
      178177  ./non_winners/text/1664.txt
      105193  ./non_winners/text/1665.txt
       89994  ./non_winners/text/1666.txt
      121287  ./non_winners/text/1667.txt
       95848  ./non_winners/text/1668.txt
      166344  ./non_winners/text/1669.txt
      101275  ./non_winners/text/1670.txt
      137908  ./non_winners/text/1671.txt
      135260  ./non_winners/text/1672.txt
      121035  ./non_winners/text/1673.txt
      134835  ./non_winners/text/1674.txt
       97735  ./non_winners/text/1675.txt
      125951  ./non_winners/text/1676.txt
      181478  ./non_winners/text/1718.txt
       67926  ./non_winners/text/1801.txt
      104156  ./non_winners/text/1807.txt
       85543  ./non_winners/text/1823.txt
       87242  ./non_winners/text/1835.txt
      108823  ./non_winners/text/1843.txt
       85060  ./non_winners/text/1844.txt
      175711  ./non_winners/text/1865.txt
      100942  ./non_winners/text/1873.txt
       99852  ./non_winners/text/1875.txt
       65962  ./non_winners/text/1878.txt
      156826  ./non_winners/text/1879.txt
       91713  ./non_winners/text/1895.txt
      168664  ./non_winners/text/1897.txt
       66577  ./non_winners/text/1899.txt
      103944  ./non_winners/text/1908.txt
       51656  ./non_winners/text/1911.txt
      124592  ./non_winners/text/1914.txt
      129616  ./non_winners/text/1929.txt
      129236  ./non_winners/text/1943.txt
      106457  ./non_winners/text/1955.txt
       43920  ./non_winners/text/1958.txt
       97073  ./non_winners/text/1967.txt
       76194  ./non_winners/text/1980.txt
      207669  ./non_winners/text/1985.txt
       89802  ./non_winners/text/2125.txt
      119527  ./non_winners/text/2238.txt
       87628  ./non_winners/text/2253.txt
       37941  ./non_winners/text/2258.txt
      144008  ./non_winners/text/2283.txt
      103420  ./non_winners/text/2289.txt
      173803  ./non_winners/text/2310.txt
       72881  ./non_winners/text/2312.txt
      119262  ./non_winners/text/2314.txt
       91928  ./non_winners/text/2317.txt
       90721  ./non_winners/text/2324.txt
       86655  ./non_winners/text/2326.txt
      134850  ./non_winners/text/2329.txt
      103828  ./non_winners/text/2335.txt
       72175  ./non_winners/text/2349.txt
      186451  ./non_winners/text/2350.txt
       74003  ./non_winners/text/2351.txt
       61206  ./non_winners/text/2352.txt
       80130  ./non_winners/text/2354.txt
      164579  ./non_winners/text/2355.txt
      123139  ./non_winners/text/2356.txt
      111036  ./non_winners/text/2357.txt
      100319  ./non_winners/text/2358.txt
      114259  ./non_winners/text/2359.txt
      185000  ./non_winners/text/2361.txt
      114800  ./non_winners/text/2362.txt
      103773  ./non_winners/text/2364.txt
       85816  ./non_winners/text/2507.txt
      136179  ./non_winners/text/2508.txt
      104130  ./non_winners/text/2513.txt
      103478  ./non_winners/text/2522.txt
      103884  ./non_winners/text/2529.txt
      121522  ./non_winners/text/2531.txt
      131604  ./non_winners/text/2539.txt
      124287  ./non_winners/text/2541.txt
      100972  ./non_winners/text/2544.txt
       76463  ./non_winners/text/2556.txt
       95052  ./non_winners/text/2560.txt
       99469  ./non_winners/text/2572.txt
      112154  ./non_winners/text/2576.txt
      126471  ./non_winners/text/2580.txt
       96585  ./non_winners/text/2618.txt
       79227  ./non_winners/text/2622.txt
      103034  ./non_winners/text/2637.txt
      111784  ./non_winners/text/2651.txt
      103345  ./non_winners/text/2657.txt
       79521  ./non_winners/text/2659.txt
      104196  ./non_winners/text/2660.txt
       87524  ./non_winners/text/2661.txt
      100784  ./non_winners/text/2664.txt
      102029  ./non_winners/text/2668.txt
      119350  ./non_winners/text/2673.txt
      111131  ./non_winners/text/2674.txt
       74720  ./non_winners/text/2679.txt
       66026  ./non_winners/text/2684.txt
      184184  ./non_winners/text/2702.txt
       59105  ./non_winners/text/2706.txt
      204252  ./non_winners/text/2848.txt
       86957  ./non_winners/text/2857.txt
      106159  ./non_winners/text/2858.txt
      132140  ./non_winners/text/2861.txt
       86547  ./non_winners/text/2868.txt
      108918  ./non_winners/text/2879.txt
      131839  ./non_winners/text/2883.txt
       62114  ./non_winners/text/2895.txt
      114128  ./non_winners/text/2897.txt
      101078  ./non_winners/text/2901.txt
      130071  ./non_winners/text/2902.txt
      115655  ./non_winners/text/2916.txt
      105393  ./non_winners/text/2919.txt
      145210  ./non_winners/text/2921.txt
       84460  ./non_winners/text/2927.txt
      177470  ./non_winners/text/2939.txt
       68251  ./non_winners/text/2945.txt
      144626  ./non_winners/text/2950.txt
      141134  ./non_winners/text/2977.txt
       59389  ./non_winners/text/2996.txt
      100466  ./non_winners/text/3007.txt
       67906  ./non_winners/text/3016.txt
       90692  ./non_winners/text/3018.txt
       94659  ./non_winners/text/3020.txt
       82432  ./non_winners/text/3026.txt
      106415  ./non_winners/text/3041.txt
      104225  ./non_winners/text/3047.txt
       74928  ./non_winners/text/3074.txt
       75915  ./non_winners/text/3083.txt
      103041  ./non_winners/text/3093.txt
       69045  ./non_winners/text/3103.txt
       95173  ./non_winners/text/3231.txt
      129448  ./non_winners/text/3247.txt
      118827  ./non_winners/text/3249.txt
      113438  ./non_winners/text/3255.txt
      103415  ./non_winners/text/3259.txt
       94916  ./non_winners/text/3263.txt
       82471  ./non_winners/text/3273.txt
       92805  ./non_winners/text/3324.txt
      116415  ./non_winners/text/3327.txt
      148118  ./non_winners/text/3329.txt
      102318  ./non_winners/text/3342.txt
      107413  ./non_winners/text/3343.txt
       80346  ./non_winners/text/3371.txt
      118178  ./non_winners/text/3393.txt
       86231  ./non_winners/text/3396.txt
       82918  ./non_winners/text/3399.txt
       75529  ./non_winners/text/3415.txt
       92288  ./non_winners/text/3416.txt
      124551  ./non_winners/text/3419.txt
      101395  ./non_winners/text/3435.txt
      163326  ./non_winners/text/3439.txt
       81177  ./non_winners/text/3445.txt
       97088  ./non_winners/text/3454.txt
       62216  ./non_winners/text/3455.txt
       72723  ./non_winners/text/3456.txt
      235812  ./non_winners/text/3470.txt
      131916  ./non_winners/text/3481.txt
      105833  ./non_winners/text/3483.txt
      132808  ./non_winners/text/3484.txt
       88183  ./non_winners/text/3494.txt
       96948  ./non_winners/text/3507.txt
      107490  ./non_winners/text/3514.txt
      116733  ./non_winners/text/3525.txt
      125146  ./non_winners/text/3529.txt
       90663  ./non_winners/text/3628.txt
      123939  ./non_winners/text/3787.txt
      120782  ./non_winners/text/3966.txt
       94460  ./non_winners/text/3975.txt
      138680  ./non_winners/text/3977.txt
       90054  ./non_winners/text/3999.txt
      100385  ./non_winners/text/4001.txt
      134552  ./non_winners/text/4023.txt
      105976  ./non_winners/text/4040.txt
      113353  ./non_winners/text/4088.txt
      136513  ./non_winners/text/4090.txt
      129378  ./non_winners/text/4091.txt
       69000  ./non_winners/text/4092.txt
      102029  ./non_winners/text/4094.txt
      116748  ./non_winners/text/4096.txt
      124777  ./non_winners/text/4097.txt
      115485  ./non_winners/text/4100.txt
      169901  ./non_winners/text/4101.txt
      102909  ./non_winners/text/4102.txt
      111183  ./non_winners/text/4103.txt
      128523  ./non_winners/text/4105.txt
       81275  ./non_winners/text/4107.txt
      124041  ./non_winners/text/4110.txt
       86624  ./non_winners/text/4113.txt
      151008  ./non_winners/text/4114.txt
      109000  ./non_winners/text/4118.txt
      134169  ./non_winners/text/4119.txt
      162389  ./non_winners/text/4121.txt
      112947  ./non_winners/text/4123.txt
      115436  ./non_winners/text/4125.txt
       75268  ./non_winners/text/4126.txt
      115248  ./non_winners/text/4128.txt
      122771  ./non_winners/text/4130.txt
      106736  ./non_winners/text/4131.txt
      111503  ./non_winners/text/4132.txt
       93276  ./non_winners/text/4136.txt
      112964  ./non_winners/text/4138.txt
      109151  ./non_winners/text/4141.txt
      140932  ./non_winners/text/4146.txt
      185632  ./non_winners/text/4147.txt
       86926  ./non_winners/text/4148.txt
       62882  ./non_winners/text/4149.txt
       72064  ./non_winners/text/4150.txt
      136473  ./non_winners/text/4237.txt
      131840  ./non_winners/text/4251.txt
       65367  ./non_winners/text/4413.txt
      107936  ./non_winners/text/4420.txt
       76091  ./non_winners/text/4425.txt
       68791  ./non_winners/text/4428.txt
       86547  ./non_winners/text/4429.txt
       49617  ./non_winners/text/4430.txt
      125307  ./non_winners/text/4431.txt
      105740  ./non_winners/text/4432.txt
       84562  ./non_winners/text/4433.txt
       90377  ./non_winners/text/4434.txt
       80631  ./non_winners/text/4435.txt
      106662  ./non_winners/text/4438.txt
       98275  ./non_winners/text/4439.txt
       69055  ./non_winners/text/4440.txt
       50155  ./non_winners/text/4441.txt
      109423  ./non_winners/text/4442.txt
       86182  ./non_winners/text/4443.txt
       95630  ./non_winners/text/4444.txt
       67624  ./non_winners/text/4445.txt
      118597  ./non_winners/text/4446.txt
      111871  ./non_winners/text/4447.txt
       97631  ./non_winners/text/4448.txt
      112649  ./non_winners/text/4449.txt
      122217  ./non_winners/text/4450.txt
      147379  ./non_winners/text/4451.txt
       84435  ./non_winners/text/4452.txt
       83354  ./non_winners/text/4453.txt
       94380  ./non_winners/text/4454.txt
      113451  ./non_winners/text/4455.txt
       95107  ./non_winners/text/4456.txt
       79241  ./non_winners/text/4457.txt
       64387  ./non_winners/text/4458.txt
      121389  ./non_winners/text/4459.txt
       97978  ./non_winners/text/4460.txt
      102765  ./non_winners/text/4461.txt
      117675  ./non_winners/text/4554.txt
       69978  ./non_winners/text/4566.txt
       61361  ./non_winners/text/4609.txt
       65017  ./non_winners/text/4627.txt
       62768  ./non_winners/text/4628.txt
      101950  ./non_winners/text/4630.txt
       91979  ./non_winners/text/4631.txt
       66603  ./non_winners/text/4632.txt
      103897  ./non_winners/text/4633.txt
       69021  ./non_winners/text/4634.txt
      122921  ./non_winners/text/4635.txt
       99814  ./non_winners/text/4636.txt
       56501  ./non_winners/text/4637.txt
      134737  ./non_winners/text/4640.txt
       72053  ./non_winners/text/4641.txt
      112088  ./non_winners/text/4642.txt
      106824  ./non_winners/text/4643.txt
       98445  ./non_winners/text/4644.txt
      136500  ./non_winners/text/4646.txt
       75822  ./non_winners/text/4654.txt
      107307  ./non_winners/text/4656.txt
      125161  ./non_winners/text/4657.txt
      113224  ./non_winners/text/4659.txt
       68847  ./non_winners/text/4665.txt
       88833  ./non_winners/text/4667.txt
       93440  ./non_winners/text/4668.txt
       86478  ./non_winners/text/4670.txt
       50640  ./non_winners/text/4673.txt
       87022  ./non_winners/text/4674.txt
       46582  ./non_winners/text/4679.txt
      109661  ./non_winners/text/4681.txt
       82299  ./non_winners/text/4682.txt
      144167  ./non_winners/text/4683.txt
      124876  ./non_winners/text/4684.txt
      121770  ./non_winners/text/4686.txt
       64425  ./non_winners/text/4690.txt
      130181  ./non_winners/text/4691.txt
       86440  ./non_winners/text/4693.txt
       68219  ./non_winners/text/4694.txt
       75071  ./non_winners/text/4695.txt
       67668  ./non_winners/text/4699.txt
       74156  ./non_winners/text/4700.txt
       59395  ./non_winners/text/4701.txt
       56407  ./non_winners/text/4705.txt
       74609  ./non_winners/text/4879.txt
       74274  ./non_winners/text/4882.txt
       63088  ./non_winners/text/4889.txt
       77402  ./non_winners/text/4892.txt
      152859  ./non_winners/text/4897.txt
       59536  ./non_winners/text/4900.txt
      117279  ./non_winners/text/4912.txt
      150858  ./non_winners/text/4924.txt
       78313  ./non_winners/text/4933.txt
      164449  ./non_winners/text/4940.txt
       89543  ./non_winners/text/4955.txt
      118075  ./non_winners/text/4957.txt
      121400  ./non_winners/text/4962.txt
       95533  ./non_winners/text/4968.txt
       98905  ./non_winners/text/4978.txt
      106784  ./non_winners/text/4981.txt
      125657  ./non_winners/text/4987.txt
       90397  ./non_winners/text/4994.txt
      115156  ./non_winners/text/4995.txt
       78081  ./non_winners/text/4998.txt
       70447  ./non_winners/text/5011.txt
      114043  ./non_winners/text/5014.txt
      126355  ./non_winners/text/5020.txt
       84142  ./non_winners/text/5021.txt
      113407  ./non_winners/text/5023.txt
       74963  ./non_winners/text/5027.txt
      252085  ./non_winners/text/5030.txt
       80641  ./non_winners/text/5033.txt
      114781  ./non_winners/text/5034.txt
       80710  ./non_winners/text/5063.txt
      116354  ./non_winners/text/5180.txt
       81272  ./non_winners/text/5201.txt
      100494  ./non_winners/text/5202.txt
       34144  ./non_winners/text/5205.txt
      124393  ./non_winners/text/5208.txt
       93924  ./non_winners/text/5211.txt
       72912  ./non_winners/text/5213.txt
      123457  ./non_winners/text/5214.txt
       97049  ./non_winners/text/5218.txt
      143676  ./non_winners/text/5226.txt
       64299  ./non_winners/text/5229.txt
       97081  ./non_winners/text/5230.txt
       72351  ./non_winners/text/5231.txt
       48183  ./non_winners/text/5232.txt
      119593  ./non_winners/text/5234.txt
       79847  ./non_winners/text/5236.txt
       82327  ./non_winners/text/5237.txt
       77859  ./non_winners/text/5244.txt
       84039  ./non_winners/text/5245.txt
      107539  ./non_winners/text/5246.txt
      102106  ./non_winners/text/5247.txt
       89654  ./non_winners/text/5248.txt
       87367  ./non_winners/text/5249.txt
      107211  ./non_winners/text/5250.txt
      101102  ./non_winners/text/5251.txt
       77585  ./non_winners/text/5253.txt
      126952  ./non_winners/text/5256.txt
       76395  ./non_winners/text/5262.txt
      116232  ./non_winners/text/5267.txt
      179031  ./non_winners/text/5269.txt
       94903  ./non_winners/text/5276.txt
      125032  ./non_winners/text/5277.txt
      115643  ./non_winners/text/5286.txt
      191428  ./non_winners/text/5288.txt
      188313  ./non_winners/text/5290.txt
       87521  ./non_winners/text/5294.txt
       77223  ./non_winners/text/5296.txt
       99837  ./non_winners/text/5297.txt
      132251  ./non_winners/text/5298.txt
       99480  ./non_winners/text/5299.txt
      101566  ./non_winners/text/5302.txt
       74663  ./non_winners/text/5313.txt
       91362  ./non_winners/text/5314.txt
       82424  ./non_winners/text/5315.txt
       72357  ./non_winners/text/5318.txt
      116826  ./non_winners/text/5322.txt
       50098  ./non_winners/text/5324.txt
       55014  ./non_winners/text/5325.txt
       87375  ./non_winners/text/5341.txt
      125198  ./non_winners/text/5474.txt
      149779  ./non_winners/text/5476.txt
       80825  ./non_winners/text/5488.txt
       68707  ./non_winners/text/5491.txt
       80235  ./non_winners/text/5492.txt
       83084  ./non_winners/text/5502.txt
       66552  ./non_winners/text/5503.txt
       93027  ./non_winners/text/5515.txt
       68353  ./non_winners/text/5517.txt
      115162  ./non_winners/text/5521.txt
       59771  ./non_winners/text/5522.txt
       84476  ./non_winners/text/5533.txt
       99472  ./non_winners/text/5568.txt
      135009  ./non_winners/text/5661.txt
       66472  ./non_winners/text/5662.txt
       83845  ./non_winners/text/5663.txt
       56441  ./non_winners/text/5666.txt
      107033  ./non_winners/text/5667.txt
      114230  ./non_winners/text/5674.txt
      111867  ./non_winners/text/5679.txt
       58035  ./non_winners/text/5682.txt
       81289  ./non_winners/text/5687.txt
       82365  ./non_winners/text/5704.txt
       68212  ./non_winners/text/5708.txt
       66666  ./non_winners/text/5709.txt
      110851  ./non_winners/text/5712.txt
       66484  ./non_winners/text/5713.txt
      143546  ./non_winners/text/5720.txt
       64438  ./non_winners/text/5722.txt
      122152  ./non_winners/text/5728.txt
       88308  ./non_winners/text/5731.txt
       48907  ./non_winners/text/5733.txt
      119423  ./non_winners/text/5737.txt
       93930  ./non_winners/text/5739.txt
       70385  ./non_winners/text/5740.txt
      117717  ./non_winners/text/5741.txt
       73690  ./non_winners/text/5871.txt
       98725  ./non_winners/text/5872.txt
      132058  ./non_winners/text/5873.txt
       76784  ./non_winners/text/5874.txt
      100690  ./non_winners/text/5875.txt
       90446  ./non_winners/text/5876.txt
       82941  ./non_winners/text/5877.txt
       50706  ./non_winners/text/5878.txt
       74449  ./non_winners/text/5879.txt
      114239  ./non_winners/text/5880.txt
      160108  ./non_winners/text/5881.txt
      163806  ./non_winners/text/5882.txt
       80506  ./non_winners/text/5883.txt
       88981  ./non_winners/text/5885.txt
       59555  ./non_winners/text/5886.txt
      295324  ./non_winners/text/5887.txt
       52388  ./non_winners/text/5888.txt
       78155  ./non_winners/text/5889.txt
       99338  ./non_winners/text/5890.txt
       85477  ./non_winners/text/5891.txt
       74026  ./non_winners/text/5893.txt
      195431  ./non_winners/text/6003.txt
      104599  ./non_winners/text/6005.txt
      106697  ./non_winners/text/6006.txt
      133989  ./non_winners/text/6010.txt
       60193  ./non_winners/text/6011.txt
       76480  ./non_winners/text/6012.txt
       87607  ./non_winners/text/6013.txt
       60600  ./non_winners/text/6016.txt
       90029  ./non_winners/text/6019.txt
       95424  ./non_winners/text/6020.txt
       90092  ./non_winners/text/6021.txt
       68496  ./non_winners/text/6027.txt
       53904  ./non_winners/text/6028.txt
       68639  ./non_winners/text/6031.txt
       68560  ./non_winners/text/6038.txt
       52730  ./non_winners/text/6039.txt
       81433  ./non_winners/text/6040.txt
       57223  ./non_winners/text/6042.txt
      108929  ./non_winners/text/6043.txt
       78150  ./non_winners/text/6045.txt
       55033  ./non_winners/text/6050.txt
       79739  ./non_winners/text/6051.txt
       99819  ./non_winners/text/6052.txt
      223786  ./non_winners/text/6054.txt
       83958  ./non_winners/text/6056.txt
       97710  ./non_winners/text/6058.txt
      125253  ./non_winners/text/6060.txt
      102557  ./non_winners/text/6073.txt
      104223  ./non_winners/text/6074.txt
       87272  ./non_winners/text/6076.txt
       66113  ./non_winners/text/6077.txt
       80794  ./non_winners/text/6078.txt
       77507  ./non_winners/text/6079.txt
       67448  ./non_winners/text/6082.txt
      139152  ./non_winners/text/6084.txt
       84016  ./non_winners/text/6206.txt
       67396  ./non_winners/text/6208.txt
       93992  ./non_winners/text/6209.txt
       84527  ./non_winners/text/6210.txt
       88560  ./non_winners/text/6211.txt
      138564  ./non_winners/text/6212.txt
       80073  ./non_winners/text/6218.txt
      130811  ./non_winners/text/6221.txt
      120544  ./non_winners/text/6222.txt
      124917  ./non_winners/text/6224.txt
       79824  ./non_winners/text/6226.txt
       53355  ./non_winners/text/6227.txt
       91011  ./non_winners/text/6228.txt
       96881  ./non_winners/text/6231.txt
      178622  ./non_winners/text/6232.txt
       94599  ./non_winners/text/6233.txt
      110694  ./non_winners/text/6234.txt
       96151  ./non_winners/text/6235.txt
       69563  ./non_winners/text/6237.txt
       71629  ./non_winners/text/6238.txt
      130336  ./non_winners/text/6239.txt
       71901  ./non_winners/text/6240.txt
      134530  ./non_winners/text/6242.txt
       57365  ./non_winners/text/6326.txt
       70287  ./non_winners/text/6327.txt
      115461  ./non_winners/text/6328.txt
       98284  ./non_winners/text/6329.txt
      102156  ./non_winners/text/6330.txt
       77423  ./non_winners/text/6331.txt
       81751  ./non_winners/text/6332.txt
      134650  ./non_winners/text/6333.txt
      142538  ./non_winners/text/6334.txt
       78622  ./non_winners/text/6335.txt
      151977  ./non_winners/text/6336.txt
       53726  ./non_winners/text/6337.txt
      244927  ./non_winners/text/6338.txt
      104759  ./non_winners/text/6339.txt
       79274  ./non_winners/text/6340.txt
       83113  ./non_winners/text/6341.txt
       79477  ./non_winners/text/6344.txt
       82393  ./non_winners/text/6345.txt
      116844  ./non_winners/text/6346.txt
      134621  ./non_winners/text/6347.txt
       98650  ./non_winners/text/6350.txt
       93241  ./non_winners/text/6351.txt
       83629  ./non_winners/text/6352.txt
       78417  ./non_winners/text/6354.txt
      126751  ./non_winners/text/6356.txt
      117558  ./non_winners/text/6362.txt
      100372  ./non_winners/text/6364.txt
       74505  ./non_winners/text/6365.txt
       80989  ./non_winners/text/6366.txt
       79430  ./non_winners/text/6372.txt
       72190  ./non_winners/text/6373.txt
       81402  ./non_winners/text/6385.txt
       80597  ./non_winners/text/6388.txt
       44684  ./non_winners/text/6390.txt
       96825  ./non_winners/text/6437.txt
       75973  ./non_winners/text/6442.txt
      104412  ./non_winners/text/6456.txt
      100962  ./non_winners/text/6538.txt
      128100  ./non_winners/text/6555.txt
      162991  ./non_winners/text/6558.txt
       64765  ./non_winners/text/6573.txt
      103763  ./non_winners/text/6575.txt
       83716  ./non_winners/text/6576.txt
       89233  ./non_winners/text/6577.txt
       88023  ./non_winners/text/6580.txt
      106819  ./non_winners/text/6581.txt
       88656  ./non_winners/text/6583.txt
      110630  ./non_winners/text/6584.txt
       89489  ./non_winners/text/6585.txt
      116736  ./non_winners/text/6586.txt
      138484  ./non_winners/text/6587.txt
       87005  ./non_winners/text/6589.txt
       69339  ./non_winners/text/6591.txt
      127445  ./non_winners/text/6593.txt
      264691  ./non_winners/text/6594.txt
      113956  ./non_winners/text/6595.txt
       88123  ./non_winners/text/6596.txt
      120376  ./non_winners/text/6597.txt
       58687  ./non_winners/text/6598.txt
       61041  ./non_winners/text/6600.txt
      104168  ./non_winners/text/6606.txt
       75732  ./non_winners/text/6618.txt
      101436  ./non_winners/text/6621.txt
       89826  ./non_winners/text/6686.txt
       91227  ./non_winners/text/6687.txt
      101340  ./non_winners/text/6689.txt
       66281  ./non_winners/text/6691.txt
       98727  ./non_winners/text/6692.txt
       97941  ./non_winners/text/6724.txt
      145123  ./non_winners/text/6733.txt
      114893  ./non_winners/text/6744.txt
      110930  ./non_winners/text/6775.txt
       93467  ./non_winners/text/6778.txt
      130237  ./non_winners/text/6782.txt
       87579  ./non_winners/text/6784.txt
      117426  ./non_winners/text/6785.txt
      278551  ./non_winners/text/6795.txt
      249376  ./non_winners/text/6799.txt
      111040  ./non_winners/text/6801.txt
       78692  ./non_winners/text/6803.txt
      116164  ./non_winners/text/6805.txt
       95076  ./non_winners/text/6810.txt
       73855  ./non_winners/text/6812.txt
       97796  ./non_winners/text/6816.txt
       94591  ./non_winners/text/6817.txt
       98190  ./non_winners/text/6821.txt
      119082  ./non_winners/text/6827.txt
      149803  ./non_winners/text/6828.txt
       80363  ./non_winners/text/834.txt
      105723  ./non_winners/text/839.txt
      155053  ./non_winners/text/841.txt
       81055  ./non_winners/text/846.txt
       60583  ./non_winners/text/901.txt
       13247  ./non_winners/thesis_metrics.py
         928  ./old_winners
      881827  ./old_winners/2011_per_hiller_gender_quotas_firm_performance_and_firm_value.pdf
      707765  ./old_winners/2011_staffan_viotti_impact_of_short_sale_bans.pdf
     4392099  ./old_winners/2012_staffan_viotti_tick_sizes_and_stock_market_volatility.pdf
    15644904  ./old_winners/2013_per_hiller_telling_true_from_false.pdf
      670362  ./old_winners/2013_staffan_viotti_a_blueprint_for_europe.pdf
     6247147  ./old_winners/2014_staffan_viotti_religious_frictions_on_the_capital_markets.pdf
      354513  ./old_winners/2015_per_hiller_fund_flow_risk_and_cross_sectional_asset_prices.pdf
      936386  ./old_winners/2015_staffan_viotti_commodities_as_a_diversification_instrument.pdf
      767158  ./old_winners/2016_per_hiller_intermediary_asset_pricing_and_swedish_equity_market.pdf
      342733  ./old_winners/2016_staffan_viotti_economic_policy_uncertainty_and_credit_risk.pdf
     1543674  ./old_winners/2017_per_hiller_solving_the_swedish_muni_puzzle.pdf
      420481  ./old_winners/2017_staffan_viotti_unbundled_costs_and_external_research.pdf
     1170066  ./old_winners/2018_per_hiller_battery_electric_vehicle_adoption_and_free_parking.pdf
     1764002  ./old_winners/2018_staffan_viotti_mirror_mirror_on_the_wall.pdf
     3184450  ./old_winners/2019_per_hiller_tobins_q_and_filing_lag.pdf
      466311  ./old_winners/2019_staffan_viotti_the_swedish_value_premium_and_disasters.pdf
    10739651  ./old_winners/2020_per_hiller_chasing_your_own_tail.pdf
      679759  ./old_winners/2020_staffan_viotti_bank_stock_returns_and_monetary_policy_surprises.pdf
     4288326  ./old_winners/2021_per_hiller_in_the_eye_of_a_pandemic.pdf
     2506208  ./old_winners/2021_staffan_viotti_market_microstructure_invariance.pdf
     2271468  ./old_winners/2022_per_hiller_predicting_liquidity_in_cryptocurrency_market.pdf
     1064626  ./old_winners/2022_staffan_viotti_owning_the_wave.pdf
      913060  ./old_winners/2023_per_hiller_changing_patterns_over_the_fomc_cycle.pdf
     1077652  ./old_winners/2023_staffan_viotti_the_drivers_of_wealth_inequality.pdf
      415307  ./old_winners/2024_per_hiller_the_smooth_transition.pdf
        7523  ./old_winners/INDEX.md
         864  ./old_winners/text
      129839  ./old_winners/text/2011_per_hiller_gender_quotas_firm_performance_and_firm_value.txt
      190835  ./old_winners/text/2011_staffan_viotti_impact_of_short_sale_bans.txt
      133614  ./old_winners/text/2012_staffan_viotti_tick_sizes_and_stock_market_volatility.txt
      181341  ./old_winners/text/2013_per_hiller_telling_true_from_false.txt
       84226  ./old_winners/text/2013_staffan_viotti_a_blueprint_for_europe.txt
      118069  ./old_winners/text/2014_staffan_viotti_religious_frictions_on_the_capital_markets.txt
       83502  ./old_winners/text/2015_per_hiller_fund_flow_risk_and_cross_sectional_asset_prices.txt
       88181  ./old_winners/text/2015_staffan_viotti_commodities_as_a_diversification_instrument.txt
       90010  ./old_winners/text/2016_per_hiller_intermediary_asset_pricing_and_swedish_equity_market.txt
      106554  ./old_winners/text/2016_staffan_viotti_economic_policy_uncertainty_and_credit_risk.txt
      141621  ./old_winners/text/2017_per_hiller_solving_the_swedish_muni_puzzle.txt
      108193  ./old_winners/text/2017_staffan_viotti_unbundled_costs_and_external_research.txt
      140928  ./old_winners/text/2018_per_hiller_battery_electric_vehicle_adoption_and_free_parking.txt
      108495  ./old_winners/text/2018_staffan_viotti_mirror_mirror_on_the_wall.txt
       89847  ./old_winners/text/2019_per_hiller_tobins_q_and_filing_lag.txt
       70487  ./old_winners/text/2019_staffan_viotti_the_swedish_value_premium_and_disasters.txt
       93339  ./old_winners/text/2020_per_hiller_chasing_your_own_tail.txt
       92074  ./old_winners/text/2020_staffan_viotti_bank_stock_returns_and_monetary_policy_surprises.txt
      118535  ./old_winners/text/2021_per_hiller_in_the_eye_of_a_pandemic.txt
      105161  ./old_winners/text/2021_staffan_viotti_market_microstructure_invariance.txt
       98371  ./old_winners/text/2022_per_hiller_predicting_liquidity_in_cryptocurrency_market.txt
       86218  ./old_winners/text/2022_staffan_viotti_owning_the_wave.txt
       72460  ./old_winners/text/2023_per_hiller_changing_patterns_over_the_fomc_cycle.txt
       70354  ./old_winners/text/2023_staffan_viotti_the_drivers_of_wealth_inequality.txt
       85155  ./old_winners/text/2024_per_hiller_the_smooth_transition.txt
       12608  ./PLAN.md
        3098  ./README.md
        1184  ./research
         384  ./research/_archive
         512  ./research/_archive/anchor_review_2026-10-04
       13331  ./research/_archive/anchor_review_2026-10-04/audit_sources.py
      162655  ./research/_archive/anchor_review_2026-10-04/comparison_metrics.csv
       84507  ./research/_archive/anchor_review_2026-10-04/corpus_inventory.csv
        1051  ./research/_archive/anchor_review_2026-10-04/corpus_summary.json
       11251  ./research/_archive/anchor_review_2026-10-04/DATA_AUDIT.md
        1973  ./research/_archive/anchor_review_2026-10-04/historical_public_probe.json
      101006  ./research/_archive/anchor_review_2026-10-04/public_data_audit.json
        4870  ./research/_archive/anchor_review_2026-10-04/README.md
       19886  ./research/_archive/anchor_review_2026-10-04/RECOMMENDATION.md
         575  ./research/_archive/anchor_review_2026-10-04/shof_master_probe.json
        1595  ./research/_archive/anchor_review_2026-10-04/source_sha256.json
        4439  ./research/_archive/anchor_review_2026-10-04/source_urls.json
        7289  ./research/_archive/anchor_review_2026-10-04/winner_metrics.csv
       12664  ./research/_archive/anchor_review_2026-10-04/WINNERS_AND_EXAMINER.md
         160  ./research/_archive/anchor_selection_2026-10-05
       11299  ./research/_archive/anchor_selection_2026-10-05/BRIEFING.md
         224  ./research/_archive/anchor_selection_2026-10-05/round1
         192  ./research/_archive/anchor_selection_2026-10-05/round2
         224  ./research/_archive/course_text_extracts
      252970  ./research/_archive/course_text_extracts/cookson_table6.png
       16191  ./research/_archive/course_text_extracts/course_intro.txt
      156271  ./research/_archive/course_text_extracts/replication_rule.png
       23437  ./research/_archive/course_text_extracts/syllabus.txt
        8972  ./research/_archive/course_text_extracts/synopsis.txt
       16982  ./research/_archive/PLAN_2026-10-01_sv.md
         128  ./research/_archive/plan_revisions_2026-10-05
        9938  ./research/_archive/plan_revisions_2026-10-05/REVISED_PLAN_2026-10-05.md
        7123  ./research/_archive/plan_revisions_2026-10-05/STEP_BY_STEP_2026-10-05.md
         192  ./research/_archive/project_docs
       22123  ./research/_archive/project_docs/2026-10-02_anchor_decision_cookson_vs_ssz.md
       17761  ./research/_archive/project_docs/2026-10-02_pressure_test_cookson_ssz_price_pressure.md
       12440  ./research/_archive/project_docs/2026-10-03_final_design_and_plan_PRICE_PRESSURE.md
       13920  ./research/_archive/project_docs/2026-10-05_FINAL_anchor_decision.md
        3155  ./research/_archive/README_2026-10-01_sv.md
        2187  ./research/_archive/README.md
         224  ./research/_archive/revised_2026-10-11
         288  ./research/_archive/revised_2026-10-11/data
        3532  ./research/_archive/revised_2026-10-11/DATA_TODO.md
         224  ./research/_archive/revised_2026-10-11/evidence
       18275  ./research/_archive/revised_2026-10-11/PLAN_REVISED.md
        2746  ./research/_archive/revised_2026-10-11/README.md
         160  ./research/_archive/thesis1_ssz_2026-10-06
       19369  ./research/_archive/thesis1_ssz_2026-10-06/PLAN.md
        4080  ./research/_archive/thesis1_ssz_2026-10-06/STATUS.md
        5262  ./research/_archive/thesis1_ssz_2026-10-06/STEPS.md
       28562  ./research/00_BESLUTSUNDERLAG.md
       20500  ./research/01_amnesval_shortlist.md
        4843  ./research/02_capiq_feasibility_2025_2026.md
       25068  ./research/03_synopsis_draft.md
       11043  ./research/03b_topic_D_reserve.md
       16063  ./research/03c_synopsis_draft_H_G.md
       13486  ./research/03d_synopsis_draft_A_B_short.md
        8339  ./research/03e_synopsis_topic_I.md
       15918  ./research/03f_synopsis_topic_5_tokenization.md
       12500  ./research/03g_synopsis_topic_1_fondtorg.md
        5292  ./research/04_fordelsanalys.md
       33154  ./research/05_fem_alternativ.md
       10238  ./research/06_idetratt.md
       18453  ./research/07_vinnarrubrik.md
        4726  ./research/08_skrivguide.md
        5242  ./research/09_blueprint_en.md
        6744  ./research/10_klose_alternativ.md
       15578  ./research/11_blind_rerank.md
       38861  ./research/11_oberoende_amnesgranskning_2026-09-07.md
       42393  ./research/12_bred_omprovning_2026-09-07.md
        2704  ./research/12_varfor_H.md
       29623  ./research/13_sjalvstandigt_amnesval_2026-09-08.md
      306742  ./research/14_soklogg_2026-09-08.json
       14085  ./research/15_vinnare_och_jamforelse_2026-09-08.md
        6395  ./research/16_metod_och_sakerhet_2026-09-08.md
        8311  ./research/17_synopsiskrav_och_fables_forslag_2026-09-08.md
       24885  ./research/18_ankare_fondtorg_2026-10-04.md
       16912  ./research/19_metodankare_fordjupning_2026-10-04.md
       25424  ./research/20_ankare_och_genomforbar_modell_2026-10-04.md
         800  ./research/agent_reports
        2229  ./research/agent_reports/01_private_target_discount.md
        1635  ./research/agent_reports/02_pe_vs_strategic.md
        2181  ./research/agent_reports/03_succession.md
        1797  ./research/agent_reports/04_advisors_process.md
        2228  ./research/agent_reports/05_ai_text_ma.md
        2417  ./research/agent_reports/06_nordic_natural_experiments.md
        2217  ./research/agent_reports/07_asset_pricing.md
        2033  ./research/agent_reports/08_corporate_household_registers.md
        1470  ./research/agent_reports/09_winning_formula.md
        2352  ./research/agent_reports/10_redteam_A.md
        2436  ./research/agent_reports/11_redteam_D.md
        2568  ./research/agent_reports/12_redteam_B.md
        2984  ./research/agent_reports/13_verify_G_H.md
        3143  ./research/agent_reports/14_verify_F.md
        3791  ./research/agent_reports/15_scan_econ_top5_jfqa_rof_jme.md
        3113  ./research/agent_reports/16_scan_nber_cepr_2024_2026.md
        3429  ./research/agent_reports/17_scan_jf_jfe_rfs_2023_2026.md
        1899  ./research/agent_reports/18_scan_swedish_reforms_2020_2026.md
        2988  ./research/agent_reports/19_redteam_K.md
       25615  ./research/agent_reports/20_sweep_2019_2022.md
       18819  ./research/agent_reports/21_sweep_markets.md
       17465  ./research/agent_reports/22_sweep_datafirst.md
       17340  ./research/agent_reports/23_sweep_nordic.md
         192  ./research/literature
        9185  ./research/literature/anchor_sweep_final_2026-10-06.md
        5644  ./research/literature/dahlquist_martinez_2015_notes.md
       16089  ./research/literature/literature_sweep_2026-10-05.md
         256  ./research/literature/papers
     1260334  ./research/literature/papers/cookson_et_al_accepted_2019.pdf
      142789  ./research/literature/papers/cookson_et_al_accepted_2019.txt
     1814519  ./research/literature/papers/cooper_halling_yang_2021.pdf
      139020  ./research/literature/papers/cooper_halling_yang_2021.txt
       29042  ./research/literature/papers/cooper_orbilu.html
      201133  ./research/literature/papers/dahlquist_martinez_2015_EFM.pdf
         160  ./research/reference
       16023  ./research/reference/conclusions_winners_vs_nonwinners.md
       46849  ./research/reference/winners_audit.md
       31791  ./research/reference/winners_vs_nonwinners_analysis.md
         352  ./research/synopsis
      104804  ./research/synopsis/BScThesis_IK_Surname1_Surname2.pdf
       16068  ./research/synopsis/BScThesis_IK_Surname1_Surname2.tex
       98855  ./research/synopsis/BScThesis_Surname1_Surname2.pdf
       13260  ./research/synopsis/BScThesis_Surname1_Surname2.tex
       15242  ./research/synopsis/BScThesis_v1_backup.tex
       13753  ./research/synopsis/BScThesis_v2_4pages_backup.tex
      138381  ./research/synopsis/page-1.png
      140151  ./research/synopsis/Synopsis_alternatives_all.pdf
       41512  ./research/synopsis/Synopsis_alternatives_all.tex
         928  ./research/winners_intros
       14088  ./research/winners_intros/2011_per_hiller_gender_quotas_firm_performance_and_firm_value.txt
       13354  ./research/winners_intros/2011_staffan_viotti_impact_of_short_sale_bans.txt
       12402  ./research/winners_intros/2012_staffan_viotti_tick_sizes_and_stock_market_volatility.txt
        9366  ./research/winners_intros/2013_per_hiller_telling_true_from_false.txt
       12534  ./research/winners_intros/2013_staffan_viotti_a_blueprint_for_europe.txt
       12162  ./research/winners_intros/2014_staffan_viotti_religious_frictions_on_the_capital_markets.txt
       10032  ./research/winners_intros/2015_per_hiller_fund_flow_risk_and_cross_sectional_asset_prices.txt
       11564  ./research/winners_intros/2015_staffan_viotti_commodities_as_a_diversification_instrument.txt
       13431  ./research/winners_intros/2016_per_hiller_intermediary_asset_pricing_and_swedish_equity_market.txt
        9094  ./research/winners_intros/2016_staffan_viotti_economic_policy_uncertainty_and_credit_risk.txt
       12019  ./research/winners_intros/2017_per_hiller_solving_the_swedish_muni_puzzle.txt
        8911  ./research/winners_intros/2017_staffan_viotti_unbundled_costs_and_external_research.txt
       10632  ./research/winners_intros/2018_per_hiller_battery_electric_vehicle_adoption_and_free_parking.txt
       13187  ./research/winners_intros/2018_staffan_viotti_mirror_mirror_on_the_wall.txt
       11785  ./research/winners_intros/2019_per_hiller_tobins_q_and_filing_lag.txt
       12023  ./research/winners_intros/2019_staffan_viotti_the_swedish_value_premium_and_disasters.txt
       11151  ./research/winners_intros/2020_per_hiller_chasing_your_own_tail.txt
       12630  ./research/winners_intros/2020_staffan_viotti_bank_stock_returns_and_monetary_policy_surprises.txt
       13608  ./research/winners_intros/2021_per_hiller_in_the_eye_of_a_pandemic.txt
        9573  ./research/winners_intros/2021_staffan_viotti_market_microstructure_invariance.txt
       12184  ./research/winners_intros/2022_per_hiller_predicting_liquidity_in_cryptocurrency_market.txt
       12425  ./research/winners_intros/2022_staffan_viotti_owning_the_wave.txt
       12043  ./research/winners_intros/2023_per_hiller_changing_patterns_over_the_fomc_cycle.txt
       10602  ./research/winners_intros/2023_staffan_viotti_the_drivers_of_wealth_inequality.txt
       14858  ./research/winners_intros/2024_per_hiller_the_smooth_transition.txt
      177145  ./research/winners_intros/tmp_2013_per_hiller_telling_true_from_false.txt
       90718  ./research/winners_intros/tmp_2020_per_hiller_chasing_your_own_tail.txt
        6033  ./STATUS.md
        6165  ./STEPS.md
         192  ./synopsis
         162  ./synopsis/~$pic1_Fondtorgsnamnden.docx
      141858  ./synopsis/BScThesis_Fox_Pauli_Uvang.pdf
        7951  ./synopsis/Topic1_Fondtorgsnamnden.docx
        5084  ./synopsis/Topic1_Fondtorgsnamnden.html
         704  ./thesis2
        7840  ./thesis2/00_VALIDATION.md
       18524  ./thesis2/01_DESIGN.md
        9361  ./thesis2/03_DATA.md
        1823  ./thesis2/AI_LOG.md
         416  ./thesis2/code
         288  ./thesis2/code/codebook
      405365  ./thesis2/code/codebook/isin_list_lseg_v2.csv
      174278  ./thesis2/code/codebook/isin_list_lseg.csv
       17227  ./thesis2/code/codebook/lseg_pull_v3.ipynb
       15569  ./thesis2/code/codebook/lseg_pull_v3.py
       19028  ./thesis2/code/codebook/lseg_pull_v4.ipynb
       16877  ./thesis2/code/codebook/lseg_pull_v4.py
      148124  ./thesis2/code/codebook/omxsb_changes_2013_2026.csv
        3636  ./thesis2/code/dilution.py
       12507  ./thesis2/code/eventstudy.py
        5209  ./thesis2/code/ftn_eventstudy.py
        5594  ./thesis2/code/lseg_codebook_pull_v2.py
        4757  ./thesis2/code/lseg_codebook_pull.py
        4171  ./thesis2/code/parse_fi.py
        3182  ./thesis2/code/power.py
        6231  ./thesis2/code/pressure.py
        1758  ./thesis2/code/README.md
        6870  ./thesis2/code/replication_omxsb.py
         256  ./thesis2/data
         160  ./thesis2/data/exit_days
        3060  ./thesis2/data/exit_days/detect_exit_days.py
       14304  ./thesis2/data/exit_days/exit_days_by_loser.csv
     7051949  ./thesis2/data/exit_days/losers_daily_valuations.csv
      174278  ./thesis2/data/isin_list_lseg.csv
      159388  ./thesis2/data/lseg_input.csv
         256  ./thesis2/data/omxsb
       17508  ./thesis2/data/omxsb/build_csv.py
       19962  ./thesis2/data/omxsb/omxs30_changes_2005_2026.csv
       26663  ./thesis2/data/omxsb/omxs30_notes.md
       34794  ./thesis2/data/omxsb/omxsb_build.py
      148124  ./thesis2/data/omxsb/omxsb_changes_2013_2026.csv
       16452  ./thesis2/data/omxsb/omxsb_notes.md
          96  ./thesis2/data/prices
        2538  ./thesis2/data/prices/README.md
         192  ./thesis2/data/swing
       37507  ./thesis2/data/swing/build_outputs.py
       19995  ./thesis2/data/swing/swing_notes.md
       17681  ./thesis2/data/swing/swing_status_2019_purge.csv
       42363  ./thesis2/data/swing/swing_status_ftn_losers.csv
         128  ./thesis2/literature
       53389  ./thesis2/literature/literature_verified.md
       23445  ./thesis2/literature/references.bib
         160  ./thesis2/outline
        9660  ./thesis2/outline/requirements_checklist.md
       30361  ./thesis2/outline/thesis2_outline.md
       31694  ./thesis2/outline/winners_structure.md
          96  ./thesis2/output
          96  ./thesis2/output/tables
         365  ./thesis2/output/tables/NOTES.md
        2778  ./thesis2/README.md
         352  ./thesis2/research
        7381  ./thesis2/research/01_FTN_QUESTION_MAP.md
        6107  ./thesis2/research/02_WINNING_PATTERN.md
       11410  ./thesis2/research/03_ANCHORS_flows_prices.md
        8870  ./thesis2/research/04_ANCHORS_selection_fees.md
       13472  ./thesis2/research/05_ANCHORS_savers.md
       11530  ./thesis2/research/06_NEW_FACTS.md
       20792  ./thesis2/research/07_THESIS_PROPOSAL.md
        6316  ./thesis2/research/08_BLIND_REFEREE.md
        3432  ./thesis2/research/README_deep_research_2026-10-11.md
         128  ./thesis2/text
        1081  ./thesis2/text/main.tex
         384  ./thesis2/text/sections
         148  ./thesis2/text/sections/00_abstract.tex
         166  ./thesis2/text/sections/01_introduction.tex
         143  ./thesis2/text/sections/02_institutional_background.tex
         154  ./thesis2/text/sections/03_theory_and_hypotheses.tex
         121  ./thesis2/text/sections/04_data.tex
         130  ./thesis2/text/sections/05_methodology.tex
         304  ./thesis2/text/sections/06_results.tex
         129  ./thesis2/text/sections/07_robustness.tex
         129  ./thesis2/text/sections/08_conclusion.tex
         251  ./thesis2/text/sections/09_appendix.tex
       37268  ./thesis2/Thesis_in_plain_words.docx
       57388  ./thesis2/THESIS_IN_PLAIN_WORDS.md
       15468  ./thesis2/Thesis_summary_by_section.docx
       73452  ./thesis2/Thesis_summary_by_section.pdf
      207500  ./thesis2/thesis2_method.pdf
       27216  ./thesis2/thesis2_method.tex
       15491  ./thesis2/Uppsatsen_i_sammandrag.docx
       74722  ./thesis2/Uppsatsen_i_sammandrag.pdf
         160  ./tmp
         384  ./tmp/anchor_audit
     1112013  ./tmp/anchor_audit/consultants2021.pdf
      235647  ./tmp/anchor_audit/jjm_equation.png
     1905314  ./tmp/anchor_audit/picking_winners.pdf
      153385  ./tmp/anchor_audit/picking_winners.txt
      296513  ./tmp/anchor_audit/ssz.pdf
      137824  ./tmp/anchor_audit/ssz.txt
       13640  ./tmp/anchor_audit/star_openalex.json
       24815  ./tmp/anchor_audit/star_page.html
      187963  ./tmp/anchor_audit/star_power_2001.pdf
      114636  ./tmp/anchor_audit/star_power_2001.txt
         160  ./tmp/pdfs
         416  ./tmp/pdfs/econometrics
         160  ./tmp/pdfs/econometrics/course
      288509  ./tmp/pdfs/econometrics/course_contact_1.jpg
        7582  ./tmp/pdfs/econometrics/Econometrics_Course.txt
       34684  ./tmp/pdfs/econometrics/Lecture_1.txt
        2720  ./tmp/pdfs/econometrics/lecture1
      309244  ./tmp/pdfs/econometrics/lecture1_contact_1.jpg
      306646  ./tmp/pdfs/econometrics/lecture1_contact_2.jpg
      374910  ./tmp/pdfs/econometrics/lecture1_contact_3.jpg
      402035  ./tmp/pdfs/econometrics/lecture1_contact_4.jpg
       57341  ./tmp/pdfs/econometrics/lecture1_contact_5.jpg
        2601  ./tmp/pdfs/econometrics/make_contact_sheets.swift
      264232  ./tmp/pdfs/synopsis_anchor-1.png
      211355  ./tmp/pdfs/synopsis_anchor-2.png
         864  ./tmp/winner_review
      148594  ./tmp/winner_review/2011_per_hiller_gender_quotas_firm_performance_and_firm_value.txt
      217555  ./tmp/winner_review/2011_staffan_viotti_impact_of_short_sale_bans.txt
      144565  ./tmp/winner_review/2012_staffan_viotti_tick_sizes_and_stock_market_volatility.txt
       10965  ./tmp/winner_review/2013_per_hiller_telling_true_from_false.txt
       87897  ./tmp/winner_review/2013_staffan_viotti_a_blueprint_for_europe.txt
      126806  ./tmp/winner_review/2014_staffan_viotti_religious_frictions_on_the_capital_markets.txt
       87301  ./tmp/winner_review/2015_per_hiller_fund_flow_risk_and_cross_sectional_asset_prices.txt
       90112  ./tmp/winner_review/2015_staffan_viotti_commodities_as_a_diversification_instrument.txt
      103629  ./tmp/winner_review/2016_per_hiller_intermediary_asset_pricing_and_swedish_equity_market.txt
      130054  ./tmp/winner_review/2016_staffan_viotti_economic_policy_uncertainty_and_credit_risk.txt
      144862  ./tmp/winner_review/2017_per_hiller_solving_the_swedish_muni_puzzle.txt
      122827  ./tmp/winner_review/2017_staffan_viotti_unbundled_costs_and_external_research.txt
      162737  ./tmp/winner_review/2018_per_hiller_battery_electric_vehicle_adoption_and_free_parking.txt
      115883  ./tmp/winner_review/2018_staffan_viotti_mirror_mirror_on_the_wall.txt
       92298  ./tmp/winner_review/2019_per_hiller_tobins_q_and_filing_lag.txt
       77350  ./tmp/winner_review/2019_staffan_viotti_the_swedish_value_premium_and_disasters.txt
          81  ./tmp/winner_review/2020_per_hiller_chasing_your_own_tail.txt
       95420  ./tmp/winner_review/2020_staffan_viotti_bank_stock_returns_and_monetary_policy_surprises.txt
      115289  ./tmp/winner_review/2021_per_hiller_in_the_eye_of_a_pandemic.txt
      103425  ./tmp/winner_review/2021_staffan_viotti_market_microstructure_invariance.txt
       94457  ./tmp/winner_review/2022_per_hiller_predicting_liquidity_in_cryptocurrency_market.txt
       84653  ./tmp/winner_review/2022_staffan_viotti_owning_the_wave.txt
       73721  ./tmp/winner_review/2023_per_hiller_changing_patterns_over_the_fomc_cycle.txt
       70571  ./tmp/winner_review/2023_staffan_viotti_the_drivers_of_wealth_inequality.txt
       91255  ./tmp/winner_review/2024_per_hiller_the_smooth_transition.txt
```

Entries deeper than four levels are not in this listing: `data/raw/<period>/<year>/*.xls|xlsm` (308 monthly workbooks, 2001-01-31 to 2026-08-31, see sections 1 and 6), `data/senastedata/output/tables/*` and `output/figures/*` (section 2.2), `research/_archive/*/*`, `tmp/pdfs/econometrics/*` and `course_context/*` subfolders.
