# Stock panel: what is here and what the code needs

Licensed data (LSEG Datastream). Nothing in this folder goes to git (`.gitignore`); share it by hand.

## On disk (raw, 15 Oct 2026)

`raw/datastream_P.csv`, `raw/datastream_RI.csv`, `raw/datastream_VO.csv`: Datastream Excel export, wide format. First column `Name` holds the date (`M/D/YYYY`), one column per series. 1,467 series, of which 30 are `#ERROR` (codes Datastream could not resolve). Daily, 31 Dec 2004 to 14 Oct 2026, `NA` where no quote. `P` is the adjusted close in SEK (or the home currency for the Nordic lines), `RI` the total return index, `VO` the volume in thousands of shares. The header carries only the Datastream name (for example `ABB LTD N (OME)`, `KLOVERN A DEAD - DELIST.12/09/14`), not the RIC, ISIN or DSCD. The request list is `thesis2/data/lseg_input.csv` (152 RICs for OMXSB companies plus 2,749 ISINs from the losers' holdings; 1,467 resolved).

## Missing

1. A code row. Re-run the same list in the Datastream add-in with the row title set to show the code (or export the request list with `DSCD`, `RIC` and `ISIN` as static datatypes). Without it the mapping from the OMXSB event list to columns runs on names, which works for most but not all (renamed and delisted companies).
2. `MV` (market value) and `NOSH` (shares outstanding), daily, same list and dates. Needed for size and for the dose in shares.
3. Index series, daily `PI` and `RI`: OMXS30 (`SWEDOMX`), OMXSPI (`SWSEALI`), OMXSB and OMXSBGI (search the code), OMXSBCAPGI if it exists. Record the exact code used for each.
4. Swedish factors (market, SMB, HML, MOM, rf) from the SHoF Fama-French page, for the four-factor robustness. Market-only is enough for the main tables.

## Target format (what `code/eventstudy.py` and `code/replication_omxsb.py` read)

- `stocks_daily.csv`, long: `id, date, p, ri, volume_sek, mcap, nosh`. One row per series-date with a quote. `volume_sek = VO x 1000 x P`. `id` is the Datastream code once the code row exists; until then a slug of the name.
- `stocks_static.csv`: `id, name, ticker, isin, first_date, last_date, delisted (0/1), exchange`.
- `indices_daily.csv`: `date, omxs30_pi, omxs30_ri, omxspi, omxsgi, omxsb_pi, omxsb_ri`.
- `factors_daily.csv`: `date, mkt, smb, hml, mom, rf` (or `date, mkt` only).

Build script to write: `code/build_prices.py` (wide to long, the static table, the list of the 30 unresolved series, coverage of all 394 OMXSB events: a price within 5 trading days on both sides of every announcement and effective date).
