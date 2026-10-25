# DATA_TODO: what to download and pull, in order

All items are public or already licensed. Estimated time in brackets.

## 1. Finansinspektionen quarterly fund holdings (one click each) [1 hour]
Page: https://www.fi.se/sv/vara-register/fondinnehav-per-kvartal/
Download pattern: `https://www.fi.se/FondInnehavLista/download?filnamn=Fondinnehav_YYYYQn_<timestamp>.zip` (the timestamp is shown on the page next to each file).

Needed for the FTN rounds (pre- and post-transfer quarters):
- 2025Q4 `Fondinnehav_2025Q4_2026-08-16 17.37.zip` (before the Jan/Feb 2026 tranches, Swedish active and Swedish index)
- 2025Q3 `Fondinnehav_2025Q3_2026-06-10 14.33.zip` (post-award, pre-transfer)
- 2025Q2 `Fondinnehav_2025Q2_2026-06-10 14.28.zip` (pre-award)
- 2026Q1 `Fondinnehav_2026Q1_2026-08-16 17.42.zip` (post-transfer; also the small-cap pre-award quarter)
- 2024Q4 `Fondinnehav_2024Q4_2026-06-10 14.03.zip` and 2025Q1 `Fondinnehav_2025Q1_2026-06-10 14.23.zip` (Nordic and Global index rounds)
- 2024Q3 `Fondinnehav_2024Q3_2026-06-10 13.53.zip`
- 2026Q3 when posted (small-cap execution)

Needed for the Lou replication (2018Q1 to 2023Q3): 23 files, same page. Already on disk: 2023Q4, 2024Q1, 2024Q2, 2026Q2.

Save every zip untouched under `financethesis_revised/data/fi_raw/`. Parse with `data/agentP/scripts/parse_fi.py` (run `python -I`).

## 2. Stock data, Nasdaq Stockholm and First North, 2018-01-01 to today [half a day]
Source: FinBas via SHoF Data Center (ask the data centre for access if not already granted), otherwise LSEG Workspace.
Per stock and day: close price, total return (adjusted), volume (SEK and shares), shares outstanding, market cap, free float if available, ISIN, listing segment. Also OMXSPI, OMXS30, OMXSB and SIXPRX index levels.
From LSEG additionally: OMXS30 constituents and weights at each quarter-end 2018 to 2026 (for the index-round module and Pavlova-Sikorskaya BMI).

## 3. Redemption days per removed fund [1 day, code]
From the daily SHoF valuations CSVs (`financethesis_ny/data/Valuations/`): for each loser fundid, find the day(s) when tnafund drops by roughly the PPM stake (PPM capital from `ppm_panel_2018_2026.csv`, previous month). Save as `redemption_days.csv` (fondnr, fundid, date, drop in SEK and in % of NAV). Cross-check a few against Pensionsmyndigheten letters (search "fondhändelsebrev" + fund name).

## 4. Holdings for funds not in FI [half a day, LSEG]
Losers: Odin Sverige C (NO), Danske Invest SICAV Sverige SI (LU), C WorldWide Sweden 1A (LU), Evli Sverige Aktieindex B (FI), Odin Norden, Delphi Nordic, Holberg Norden, DNB Grönt Skifte Norden (NO).
Winners: SEB 3 Sweden Equity Fund (LU), Danske Invest SICAV Sverige Småbolag (LU), SEB Nordic Small Cap (LU), Ålandsbanken Norden Aktie (FI), Nordea Nordic Fund.
LSEG Workspace: fund holdings (Lipper) at the quarter-end before each transfer. If unavailable, use the fund's factsheet top-10 and bound the result with and without the fund.

## 5. Returns for the 144 bids without a return series (Table 1A only) [2 hours, LSEG]
List in `data/unmatched_for_lseg.csv`. Monthly total return 2019-01 to 2026-09 by fund name.

## 6. Requests to send this week
- Pensionsmyndigheten (registrator@pensionsmyndigheten.se): redemption dates per removed fund, FTN rounds and 2019; counts of own choice versus default per round. Swedish draft in `financethesis_ny` data guide, adapt.
- FTN: bid deadline per round; per-bid qualification status.
- SHoF Data Center: FinBas access; whether Morningstar holdings are in the licence.
