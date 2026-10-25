# STATUS: read this first

**As of Sun 25 October 2026.** Newest change on top. Each evening, three lines per person (done / next / blocked), initialled A or L.

## Where things stand

- **Thesis 2 is the thesis.** Working title: "Pre-announced, uninformed, and large: the price of moving the premium pension". Anchor: Greenwood and Sammon (2025, JF). Part 1 replicates their index-effect result on OMXSB (394 events, 2013-2026). Part 2 measures the price pressure of Pensionsmyndigheten's forced sales after Fondtorgsnämnden's rounds (2024-2026). Part 3 asks who paid (dilution of the stayers, swing pricing). Pre-analysis plan: `thesis2/01_DESIGN.md`. Method note with equations, data table and work plan: `thesis2/thesis2_method.tex` (14 Oct).
- **Thesis 1 (the SSZ replication) is dropped.** Its plan is archived in `research/_archive/thesis1_ssz_2026-10-06/`. Nothing in it was executed.
- **25 Oct, evening: the map is `thesis2/THESIS_IN_PLAIN_WORDS.md` (and `.docx`), version 2.1, Parts A to G.** Read it before anything else in `thesis2/`.
- **25 Oct: folders merged.** `financethesis_fresh` and `financethesis_revised` were folded into this repo (`thesis2/`, `data/`, `research/_archive/revised_2026-10-11/`). The empty shells and byte-identical duplicates sit in `~/Documents/_to_delete/`; Alexander empties it by hand after checking.
- **No FTN return has been computed.** `UNBLIND = False` in `thesis2/code/ftn_eventstudy.py` and `dilution.py` stays until Klug has signed off the specifications and the date is written in `thesis2/03_DATA.md`, section E.
- **The GitHub repo is public.** It holds SHoF/Morningstar-derived data (`data/derived/`, `thesis2/data/exit_days/`), course slides and the SSE thesis corpus. Make it private before the next push (GitHub: Settings, Danger zone, Change visibility).

## Data on disk (what changed since 14 Oct)

- **Stock panel, raw:** `thesis2/data/prices/raw/datastream_{P,RI,VO}.csv` (Datastream, 15 Oct). Wide format, 1,467 series of which 30 are `#ERROR`, daily 31 Dec 2004 to 14 Oct 2026, names only in the header (no RIC or ISIN). Gitignored (licensed). Not yet in the long format the code reads. Missing: market value, shares outstanding, the index series, Swedish factors, and a code row to map names to the OMXSB event list. Details and target format: `thesis2/data/prices/README.md`.
- Unchanged and ready: OMXSB and OMXS30 events (`thesis2/data/omxsb/`), tranche days for about 30 losers through 30 Sep (`thesis2/data/exit_days/`), swing-pricing status (`thesis2/data/swing/`), PPM monthly panel 2018-2026 (`data/panel/`), FTN bids, fees and crosswalk (`data/derived/ftn_2026-10-11/`), FI holdings 4 of 12 quarters (`data/extra/`), Morningstar daily valuations and reinvested prices to 30 Sep (`data/Valuations/`, `data/Reinvestments/`, not in git).

## Next actions, in order

1. [A] Make the repo private. Push this cleanup. [L] Clone it (`git clone git@github.com:uvangludvig-ship-it/financethesis.git`) and get `data/Valuations`, `data/Reinvestments` and `thesis2/data/prices/raw` from Alexander by AirDrop or Drive, not through git.
2. [L] Klug. Nothing here documents a meeting after 11 Oct. Confirm he has the method note and knows the synopsis question changed; book the sign-off meeting for the week of 2 Nov with the five decisions below on the agenda. Send `thesis2/thesis2_method.pdf`.
3. [A] Stock panel into the code's format: `stocks_daily.csv`, `stocks_static.csv`, `factors_daily.csv`, `indices_daily.csv` (see `thesis2/data/prices/README.md`). Re-run the same Datastream list for `MV`, `NOSH` and a code row. Then `python3 thesis2/code/replication_omxsb.py`: Table 2, the first unblinded result, and not an FTN result.
4. [A] Download the 8 FI zips for 2024Q3-2026Q1 and the 5 for 2018Q4-2019Q4 (links in `thesis2/03_DATA.md`, B). Run `parse_fi.py`, `pressure.py`, `power.py --dose`.
5. [L] Send the Pensionsmyndigheten request for sale orders under offentlighetsprincipen (draft in `thesis2/03_DATA.md`, C; rewrite it in your own words). Answers take one to three weeks.
6. [L] Keep `thesis2/AI_LOG.md` current (course requirement). Fill the section files in `thesis2/text/sections/` starting with institutional background and data.
7. [A+L] Before the sign-off meeting: write the four maths additions from `thesis2/THESIS_IN_PLAIN_WORDS.md` Part E (impact exponent with EIV-IV, reversal half-life, optimal-execution counterfactual, implied elasticity) into `thesis2/01_DESIGN.md` section 8 and the method note, so they are pre-committed and land inside Tables 3 and 6 and the Figure 3 caption. Nothing else is added.
8. [L] First week of November: request the SHoF refresh of Valuations and Reinvestments to 31 Oct. [A] Re-run `thesis2/data/exit_days/detect_exit_days.py` for the small-cap tranches.

## Open decisions (for Klug; `thesis2_method.tex`, section 7)

1. Sign-off on the specifications in `01_DESIGN.md` and on the deviation from the synopsis.
2. Replication on OMXSB alone, or OMXSB plus OMXS30 (48 events, needs a 2005-2011 pull).
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

1. `PLAN.md` wins over every other file. `research/_archive/` is history, not guidance.
2. Do not compute a stock or fund return around an FTN date before the sign-off date is written in `thesis2/03_DATA.md`, section E.
3. Do not write thesis prose. The course forbids AI-written thesis text; anything drafted is marked *draft* for the authors to rewrite, and every use goes into `thesis2/AI_LOG.md`.
4. Raw data in `data/raw/`, `data/Valuations/`, `data/Reinvestments/` and `thesis2/data/prices/raw/` is never modified; every transformation lives in code.
5. Seven tables and four figures (`thesis2/outline/thesis2_outline.md`). Something new replaces something; it is never added.
