# 03. Data: what is on disk, what was found tonight, what you must get

> **Paths updated 25 Oct 2026.** The folders were merged into the repo: `financethesis_fresh/data/...` is now `data/...` at the repo root, `financethesis_ny/...` is the repo root, `financethesis_fresh/thesis/...` is `thesis/...`, and `financethesis_revised/` is `archive/research_archive/revised_2026-10-11/`. The Datastream pull of 15 Oct sits in `data/raw/lseg/datastream/` (see `data/raw/lseg/panel_2012_2026/README.md`).

Status 12 Oct 2026. "On disk" means in `~/Documents/financethesis_ny/data` or in this folder.

## On disk, ready

| item | where | use |
|---|---|---|
| PPM fund-month panel 2018-2026 (capital, savers by sex, net trade, fees) | `financethesis_fresh/data/derived/ppm/ppm_panel_2018_2026.csv` | Table 1, winners' monthly inflows (B in equation 5), fee savings |
| FTN reports, all eleven rounds, with award dates, winners, losers, bids | `financethesis_ny/data/raw/ftn/`, parsed in `financethesis_fresh/data/derived/measurements/` | Table 1, Appendix A1 |
| FI quarterly holdings 2023Q4, 2024Q1, 2024Q2, 2026Q2 | `financethesis_ny/data/extra/fi_*.zip`, parser `measurements/parse_fi.py` | weights $w_{ij}$ for the 2024 European round and for the small-cap round (2026Q2) |
| Morningstar daily valuations (TNA, units, estimated flows) 2018 to 30 Sep 2026 | `financethesis_ny/data/raw/shof/Valuations/` (755 MB) | tranche days and $\rho_{je}$; done for the 78 losers in `data/derived/exit_days/` |
| Morningstar daily reinvested prices (fund NAV total return) 2018 to 30 Sep 2026 | `financethesis_ny/data/raw/shof/Reinvestments/` (3.6 GB) | Table 5 (fund NAV on tranche days), after unblinding only |
| Fund master (domicile, benchmark, company) | `financethesis_ny/data/fundmaster.xlsx` | Table 5 benchmarks, 2019 domiciles |
| OMXSB change list 2013-2026 (394 events) and OMXS30 2005-2026 (48) | `data/input/omxsb/` | Table 2 |
| Swing-pricing status of 78 losers and 60 largest 2019 exits | `data/input/swing/` | Table 5 |
| Tranche days for losers with daily data | `data/derived/exit_days/exit_days_by_loser.csv`, `losers_daily_valuations.csv` | equation 5 |

## A. What you must pull: the stock panel (the Friday gate)

Preferred source: FinBas at the Swedish House of Finance, because it covers every Nasdaq Stockholm and First North stock including delisted ones, in SEK, with adjusted prices, volume and shares outstanding, from 1983. Ask the SHoF data desk (you already have Morningstar access through them) for daily FinBas equity data 2005-01-01 to 2026-10-31 for all Swedish listed stocks, plus the FinBas daily factor returns (market, SMB, HML, MOM) if they offer them.

If FinBas takes more than two days, use LSEG. Datastream (Excel add-in or Workspace Datastream tab), one request list, daily frequency, 01/01/2005 to today:

- Universe: the Datastream research list for Sweden (`FSWD`) plus the dead-stock lists for Sweden (`DEADSD`, and `DEADSD1`, `DEADSD2` if they exist in your version) so delisted names are included. Alternatively build the list in Workspace Screener: exchange = Stockholm Stock Exchange and First North, status = active and inactive, export RICs, then feed Datastream.
- Datatypes, all daily: `P` (price), `UP` (unadjusted price), `AF` (adjustment factor), `RI` (total return index), `VO` (volume, thousands of shares), `VA` (value traded, if available), `NOSH` (shares outstanding), `MV` (market value), `NOSHFF` (free-float shares) or `FF` (free-float percentage), `PTBV` or `MTBV` (market-to-book, for the book-to-market control), `TURN` if offered.
- Static fields once: `ISIN`, `SECD`, `DSCD`, `NAME`, `ENAME`, `BDATE` (first date), `TIME` (delisting date), `TYPE`, `EXMNEM` (exchange), `ICBSSN` (ICB supersector name), `ICBSSC` (code).
- Indices, daily `PI` and `RI`: OMXS30 (`SWEDOMX`), OMXSPI (`SWSEALI`), and search Datastream or Workspace for OMXSB (`.OMXSB`, `.OMXSBGI`, `.OMXSBCAPGI`), OMXSBESG, SIX30RX, SIXPRX, SIX Sweden SRI, Solactive ESG Sweden 100, Solactive ESG Select Sweden. Record the exact code you used for each.
- Export as CSV, long format (one row per stock-date) if the tool offers it; wide format is fine, `code/eventstudy.py` reshapes both.

Deliver to `~/Documents/financethesis_fresh/data/raw/lseg/panel_2012_2026/` as `stocks_daily.csv` (or several files) and `indices_daily.csv`, plus the static table `stocks_static.csv`. Tell me when it is there; `code/replication_omxsb.py` runs on it the same day. That is the first unblinded result and it is not an FTN result.

## B. What you must download: FI holdings, ten files, two minutes each

The listing page is https://www.fi.se/sv/vara-register/fondinnehav-per-kvartal/. Save each zip in `~/Documents/financethesis_ny/data/extra/` with the name `fi_YYYYqN.zip` (same pattern as the four you already have). The parser handles them.

For the FTN rounds (weights before the letter and after execution):

- 2024Q3: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2024Q3_2026-06-10%2013.53.zip
- 2024Q4: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2024Q4_2026-06-10%2014.03.zip
- 2025Q1: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2025Q1_2026-06-10%2014.23.zip
- 2025Q2: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2025Q2_2026-06-10%2014.28.zip
- 2025Q3: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2025Q3_2026-06-10%2014.33.zip
- 2025Q4: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2025Q4_2026-08-16%2017.37.zip
- 2026Q1: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2026Q1_2026-08-16%2017.42.zip
- 2026Q3: not published yet (expected November); check the listing page in week 5.

For the 2019 purge (Table 5 pooled sample and a 2019 pressure placebo if time allows):

- 2018Q4: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2018Q4_2022-11-16%2017.05.zip
- 2019Q1: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2019Q1_2022-11-16%2017.35.zip
- 2019Q2: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2019Q2_2022-11-16%2015.35.zip
- 2019Q3: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2019Q3_2022-11-11%2015.05.zip
- 2019Q4: https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_2019Q4_2022-10-28%2014.04.zip

If a link has expired (FI re-timestamps files), take the same quarter from the listing page.

## C. What you must ask for: execution days for the big Swedish losers

The Morningstar daily file has only month-end observations for most Swedish-domiciled funds, so the tranche days of Avanza Zero (21.5 bn), Storebrand Sverige (10.1 bn), LF Sverige Vision (3.9 bn), LF Global Index (12.8 bn), Avanza Global (3.7 bn), Handelsbanken Sverige (2.6 bn), Nordea Swedish Stars (2.1 bn), Nordea European Stars (3.4 bn), Robur Nordenfond (3.2 bn), Simplicity Norden, Evli Sverige Aktieindex, Aktiespararna Direktavkastning and the Storebrand global funds are not observed. Two routes, do both:

1. Email Pensionsmyndigheten (registrator@pensionsmyndigheten.se, and the fondtorg contact in the Avslutsprocess document), under offentlighetsprincipen, for a list of the sale orders placed in each deregistered fund since 2024: fund, date, amount (SEK) and share of the fund's units. Draft, in your own words:

   "Hej, vi skriver kandidatuppsats på Handelshögskolan om effekterna av fondtorgets upphandling. Vi önskar ta del av uppgifter om Pensionsmyndighetens avslutsorder i de fonder som avregistrerats efter Fondtorgsnämndens upphandlingar 2024 till 2026: fond, datum för varje order, belopp i kronor och andel av fondens andelar, samt motsvarande uppgifter för avregistreringarna 2019 om de finns. Uppgifterna avser myndighetens egna transaktioner och bör vara allmänna handlingar. Tacksamma för digitalt utlämnande."

2. Fund companies' own daily AUM: Avanza publishes daily fund size for Avanza Zero and Avanza Global on its fund pages (history via the fund's factsheet archive or by request to Avanza Fonder); Storebrand and Länsförsäkringar publish daily NAV but not daily AUM, so a unit-count series would need a request.

## D. What you must refresh in November

The Morningstar valuations and reinvested prices end 30 Sep 2026. The small-cap round executes in October. Re-download the same two SHoF datasets in the first week of November (same request as before, dates to 31 Oct 2026), then re-run `data/days/detect_exit_days.py` to date the small-cap tranches.

## E. What exists only as a plan until unblinding

Nothing in this folder computes a stock or fund return around an FTN date. `code/replication_omxsb.py` runs on index events only. `code/pressure.py` builds the dose and the square-root prediction without returns. `code/ftn_eventstudy.py` and `code/dilution.py` have an `UNBLIND = False` switch; it is turned to `True` only after the specifications in `01_DESIGN.md` have been agreed with Klug, and the agreement is dated in this file.

## F. Pause points, in order

1. Stock panel (A). Needed by Fri 17 Oct for the gate; everything else waits on it.
2. FI zips (B). Ten clicks; needed by week 2.
3. Pensionsmyndigheten email (C). Send Monday; answers take one to three weeks.
4. Klug meeting (Fri 17 Oct): sign-off on the specifications, on the synopsis drift, and on whether the replication uses OMXSB alone.
5. SHoF refresh (D), first week of November.
