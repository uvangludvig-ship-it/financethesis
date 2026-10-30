# Check: does the 2007–2026 run reproduce the original 2013–2026 run?

Compared: `output/omxsb_replication/tables/tab_02_car_long.csv` (original run, `code/notebooks/replication_omxsb.ipynb`, LSEG panel `panel_2012_2026`, 25 Oct 2026) against `output/omxsb_replication_2007/tables/tab_02_car_long.csv` (new run, `code/notebooks/replication_omxsb_2007.ipynb`, LSEG panel `panel_2005_2026`, 28 Oct 2026) on the four shared periods 2013–2017, 2018–2020, 2021–2023, 2024–2026 and the "last − previous" row: mean, HC1 and CR1 standard error, wild-bootstrap p-value, N and G for every (type, window, period). The cell-by-cell comparison is in `check_2013_2026_vs_original.csv` (column `flag` marks |difference| > 0.01 percentage points in the mean or a standard error, or a different N or G).

## Result

- Sample: identical. The same 380 events of 2013–2026 survive the listing/delisting filter in both runs (the 14 dropped events are the same), N and the number of clusters G agree in all 30 cells.
- 28 of 30 cells agree to at least four decimals in mean, both standard errors and the bootstrap p-value.
- 2 cells differ, both in the period 2018–2020:

| type | window | period | mean, original | mean, new | difference (pp) |
|---|---|---|---|---|---|
| addition | eff | 2018–2020 | 1.7300 | 1.7457 | +0.0158 |
| deletion | tot | 2018–2020 | 1.1262 | 1.0754 | −0.0508 |

A third cell, addition tot 2018–2020, differs by +0.0055 pp (below the flag threshold); all other cells differ by zero.

## Cause: a few stock-days are missing in the 2005 pull, prices are otherwise identical

The two panels were compared row by row for the 394 RICs of the 2013–2026 events over the range of the 2012 panel (2012-01-02 to 2026-10-14):

- The index calendar is identical: .OMXSBGI has the same 3,711 trading days in both files and identical closes; .OMXSGI likewise. Windows therefore start and end on the same days in both runs. Not a calendar difference.
- The RICs are identical: all 394 RICs of `omxsb_events_with_ric.csv` are in the 2005 panel and were reused unchanged. Not a RIC difference.
- `close` and `totret` are identical (to 1e-6 relative) on every one of the 400,676 stock-days present in both panels. Not a revised-price difference.
- The 2005 pull lacks 136 stock-days that the 2012 pull has (0.03 percent of the rows), spread over 58 RICs; the largest gaps are MER.ST (22 days), LUMIsdb.ST^F17 (16), ETRN.ST^A22 (12), LUNG.ST (11), VNEsdb.ST^D22 (8), ENQ.ST^L23 (6), NOKIA.ST (4), and one or two days (mostly 2022-11-15 and 2025-07-28) for the rest. The 2005 pull has no stock-day that the 2012 pull lacks.
- `mcap` and `shares` differ on 1,443 and 162 stock-days (104 and 18 RICs). These do not enter Table 2 but do enter the Table 3 controls (size, excess turnover), Figure 10 and the net-trading denominators, so Table 3, Figure 10 and the 2013–2026 rows of Tables 4 and 5 may differ marginally from the original for that reason.

The notebook fills a missing stock-day inside the listing range with a zero return (`rser`), so a missing day enters the CAR as 0 − index return instead of the stock's actual return minus the index return. Exactly two event windows of 2013–2026 contain such a day:

| event | RIC | type | missing day(s) | window hit | effect on the cell |
|---|---|---|---|---|---|
| OMXSB-2018H1-07 Africa Oil | MER.ST | deletion | 2018-05-18 (total return +1.98 percent in the 2012 pull) | total window | −1.98 / 39 events = −0.051 pp on deletion tot 2018–2020 |
| OMXSB-2018H2-10 Veoneer SDB | VNEsdb.ST^D22 | addition | 2018-11-21 and 2018-12-04 (total returns summing to −0.28 percent) | total window (both days) and effective window (2018-12-04 only) | +0.28 / 51 = +0.0055 pp on addition tot 2018–2020; +0.80 / 51 = +0.016 pp on addition eff 2018–2020 |

These two events also show up in the coverage check as the only 2013–2026 events whose `days_with_price` fell (20 → 19 and 20 → 18) between the two pulls. The differences are a property of the LSEG pull, not of the code; the original run is reproduced exactly wherever the input rows are the same.

## Other differences between the two runs that are not differences in results

- `stocks_static_2005.csv` carries the pull range (2004-07-01 to 2026-10-26) as `first_date`/`last_date` for 1,609 of 2,117 RICs instead of the first and last trading day, so the notebook recomputes the three columns from the daily panel; with the recomputed dates the listing/delisting filter drops the same 14 events of 2013–2026 as the original.
- 169 RICs of the 2005 static table have no `IssueISIN`/`DTSubjectName` because they are not in `td_universe.csv` (mostly Norwegian-cross-listed `...NOK.ST` RICs, but also SAMPO.ST, NOKIA.ST, EPIRb.ST, LUNG.ST, COREb.ST, VOLVa.ST, STEr.ST, SSABb.ST among the event RICs); the notebook fills them from `panel_2012_2026/stocks_static.csv` so that the FI holdings ISIN bridge of the original run is unchanged. The chain "with a quarter-end before AD in FI data" (259), "with net trading" (253) and the 14 index trackers are the same as in the original.
- The 2005 parquet has `bid` and `ask` columns, so the new run also produces `tab_07_spread`, which the original run skipped.
- .OMXSGI starts 2008-01-02, so 13 events of 2007 (and events whose window reaches into 2007) have no CAR against .OMXSGI; they are excluded from the appendix table `tabA_01_car_omxsgi_long` (N in 2007–2012: 44 additions and 50 deletions against 49 and 58 in Table 2). All main tables use .OMXSBGI.

## Addendum, phase 2 (Greenwood–Sammon conventions, 28 Oct 2026)

The notebook was re-run with missing stock-days inside the listing range kept as NaN instead of filled with a zero return (the anchor paper's CRSP convention), so an event drops out of a window that contains such a day. `check_2013_2026_vs_original.csv` now holds this run. The two events above therefore no longer enter the affected windows and the differences against the original run are now in N as well as in the mean: addition eff 2018–2020 1.730 → 1.669 (N 51 → 50, Veoneer), addition tot 2018–2020 2.348 → 2.432 (N 51 → 50, Veoneer), deletion tot 2018–2020 1.126 → 0.884 (N 39 → 38, Africa Oil); the remaining 27 cells are unchanged. The phase-1 Table 2 (zero-filled, identical to the original convention) is kept as `tables/tab_02_car_long_phase1.csv`, and `table2_phase1_vs_gs.md` compares the two conventions cell by cell: of the 487 sample events, 6 lose the total window, 3 the effective window and 1 the announcement window (four of the six are 2007–2012 events: Tanganyika Oil 2007, SCA A 2008, Atrium Ljungberg 2008, Lundin Mining SDB 2010).

## Addendum, equal periods (30 Oct 2026)

Table 2 now uses four equal five-year periods (2007–2011, 2012–2016, 2017–2021, 2022–2026). The check against the original run is unaffected: the notebook also computes Table 2 on the original run's four periods from a separate `period_old` column (`tables/tab_02_car_long_oldperiods.csv`) and compares those cells, so `check_2013_2026_vs_original.csv` still shows the same 3 flagged cells of 30 (Africa Oil, Veoneer). The phase-1 (zero-filled) column of `table2_phase1_vs_gs.md` is recomputed in the notebook on the new periods from the zero-filled return series instead of being read from the frozen 28 Oct file.
