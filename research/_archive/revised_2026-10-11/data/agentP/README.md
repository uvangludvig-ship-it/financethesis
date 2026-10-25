# agentP: executed FTN rounds as a multi-event FIP design (feasibility, 2026-10-11)

Blind rule respected: no stock returns downloaded or used. Holdings, PPM capital, market caps only.

## Folder
- `data/fi_<q>/`      unzipped FI VPFO XML (untrusted data; scripts run with `python -I` from `scripts/`)
- `scripts/parse_fi.py`     XML -> `out/fi_funds_<q>.csv` (fund, ISIN, NAV, benchmark field `Jämförelseindex`) and `out/fi_holdings_<q>.csv`
- `scripts/analyze.py`      fund mapping, net demand per round/scenario, SE_index overlap matrices, execution windows
- `scripts/fip.py`          company-level FIP (= net SEK / market cap) for the top names; caps from stockanalysis.com Nasdaq Stockholm list (Oct 2026)
- `scripts/fip_allnames.py` approximate caps for all names via SIXPRX-tracker weights (Storebrand Sverige Plus 2026Q2, T = 13.2 trn SEK calibrated); PPM share of loser NAV

## Outputs (out/)
- `fund_fi_mapping.csv`         PPM fondnr -> FI institutnummer (2024Q2, 2026Q2), domicile note, benchmark, NAV, PPM share of fund NAV
- `netdemand_<round>_<qL>_<qW>_<alloc>[...].csv`   per-ISIN buy/sell/net/gross SEK; `netdemand_summary.csv` = corr(buy,sell), sd(net)/sd(gross), top-10 share, counts
- `se_index_overlap_2024q2.csv`, `se_index_overlap_2026q2.csv`   pairwise sum-of-min-weights overlap among SE index funds
- `fip_company_<tag>.csv`, `fip_summary.csv`           company-level FIP, fetched caps only
- `fip_allnames_<tag>.csv`, `fip_allnames_summary.csv` FIP with approximated caps for mid/small names (flag `cap_src`)
- `execution_windows_monthly.csv`  per round and month: loser handel_netto, residual exit (fund vanishes from panel), winner inflows, % of award capital

## Model
sell_i = sum over losers l of w_li * C_l (C_l = PPM capital at award, from panel).
buy_i  = sum over winners w of w_wi * s_w * sum(C_l); s_w = equal split over new winners ("equal_new") or actual panel inflow shares in the execution window ("actual").
Weights from FI quarter qL (losers) and qW (winners). 2024Q2 = pre-event proxy; 2026Q2 = post-event (same-quarter runs avoid weight-drift artefacts).
Equities only (Tillgångsslag = ÖverlåtbartVärdepapper). ISIN level; company level sums share classes (A/B substitution caveat).

## VERIFIED vs APPROXIMATED
VERIFIED: FI holdings and benchmark fields; PPM capital/flows from the monthly panel; FI download URLs; fund domiciles.
APPROXIMATED: (i) holdings quarter != transfer date (2025Q3/2025Q4 files not on disk); (ii) market caps are Oct-2026 company caps, not event-date;
(iii) `cap_src = sixprx_approx` caps derive from a tracker's weights (free-float, 10% cap rule); (iv) winner allocation rule inferred from panel inflows.
