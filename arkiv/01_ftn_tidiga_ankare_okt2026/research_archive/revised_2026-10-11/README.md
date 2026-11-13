# financethesis_revised

Created 11 October 2026. A revised thesis design with Fondtorgsnämnden at the centre, plus the data and evidence it rests on. Nothing in `financethesis_ny` was changed or deleted; this folder sits beside it.

| File | What it is |
|---|---|
| `PLAN_REVISED.md` | **Read first.** The design: question, anchor (Lou 2012 RFS, Wardlaw 2020 JF), replication, FTN extension, five exhibits, power, data, risks, eight-week calendar, Klug email |
| `DATA_TODO.md` | What to download and pull this week, with URLs |
| `evidence/00_ftn_feasibility_round1_2026-10-11.md` | Four feasibility runs on the synopsis questions: default vs own choice (94% default), fees, non-PPM flows, the bid file |
| `evidence/01_anchor_search_2026-10-11.md` | Literature search for anchors not screened on 5 October; ranked table |
| `evidence/02_price_pressure_executed_rounds_2026-10-11.md` | Net stock demand per executed round from FI holdings; index benchmarks; execution windows; FI files to get |
| `evidence/03_forced_inflows_DRS_2026-10-11.md` | Winners' forced inflows: doses, before/after, power (secondary only) |
| `evidence/04_purge_2019_replication_sample_2026-10-11.md` | The 2019 purge: 313 funds, 80 bn, 97% default; a replication sample for "who moves the money" |
| `data/ppm_panel_2018_2026.csv` | PPM fund-month panel, Jan 2018 to Aug 2026 (104 months), built by `data/build_ppm_2018.py` from the raw Pensionsmyndigheten files |
| `data/bids_long.csv` | All 290 FTN bids, 11 rounds, winners, incumbents, dates |
| `data/unmatched_for_lseg.csv` | 144 bids without a return series: the LSEG pull list |
| `data/crosswalk_ppm_shof.csv` | PPM ISIN to Morningstar fundid |
| `data/ftn_category_fees.csv`, `data/winners_fee_series.csv` | Category fees before/after; winners' monthly fee series |
| `data/agentA/` | Round membership and loser decomposition (default vs voluntary), with code |
| `data/agent2019/` | 2019 purge exits, decomposition, destinations, with code |
| `data/agentDRS/` | Forced inflows per winner, power sketch, with code |
| `data/agentP/` | FI holdings parser (`scripts/parse_fi.py`), per-stock net demand and FIP by round (`out/`), fund-to-FI mapping, index benchmarks, execution windows |

Blind-analysis rule: no stock return or fund return around any FTN date has been looked at. Everything here is built from holdings, capital, flows, fees and bid lists.

Relation to the old folder: `financethesis_ny/PLAN.md` (SSZ 2015 as anchor, FTN as a side table) is the design the 5 October anchor contest chose. `PLAN_REVISED.md` section 3 explains what has changed since then and why the price-pressure design that lost that contest is now viable. The choice between the two belongs to the authors and the tutor.
