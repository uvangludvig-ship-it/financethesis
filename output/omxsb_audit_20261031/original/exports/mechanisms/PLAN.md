# Plan: Greenwood & Sammon's five explanations on OMXSB 2007-2026

Written before running anything (28 Oct 2026). Script: `code/build/mechanisms_2007.py`. Outputs: this folder.

## Sources read

| Version | Where | What it says |
|---|---|---|
| NBER WP 30748 (Dec 2022) | scratchpad markdown (full text) | Abstract: 3.4% (1980s), 7.6% (1990s), 0.8% (2010s) for additions; deletions -0.6% in 2010-2020. Five explanations in sections 2.1-2.5: composition (Table 3, eq. 4), average liquidity (Fig. 4 effective spreads, Fig. 5 implementation shortfall), migrations (Fig. 6-7), predictability (Fig. 8, Fig. 10 rank, Fig. 9 post-event), event-specific liquidity (Fig. 11 volume share, Table 4 trackers vs 13F). Table 2 is "by decade" in its title while the text says "5-year periods". Fig. 3: event-level scatter of total return on net tracker buying, "negative slope, R² about 2% (additions) and 6% (deletions)". |
| HBS WP 23-025 (later version, fetched from hbs.edu, 59 pp.) | scratchpad `hbs/gs_hbs.md` | Abstract: 7.4% (1990s) to 0.3% (past decade); deletions 0.1% in 2010-2020. Sections renumbered: 2.1 composition (now Table 2, eq. 3, with **demeaned** controls, adds Wurgler-Zhuravskaya arbitrage risk and analyst coverage, and columns without controls); 2.2 migrations (Fig. 4-6, Table 3); 2.3 predictability (Fig. 7 = old Fig. 8 but to AD+14, Table 4 pre-announcement CARs, Fig. 8 = old Fig. 10 ranks; the old Fig. 9 post-event figure is gone); 2.4 "higher liquidity" with new multiplier/elasticity Tables 5-6, then 2.4.3 overall liquidity (Fig. 9 = old Fig. 4+5 combined) and accommodation (Table 7 = old Table 4, adds passive/active columns). NBER Table 3 turnover coefficient for additions -0.029 (0.44); HBS Table 2 -0.14 (0.49), size 19.08 (4.15), 1990s dummy 7.39, 2010s dummy 1.77 with controls. |
| JF 2025 (doi 10.1111/jofi.13465) | not accessible: onlinelibrary.wiley.com returns HTTP 403 to the fetch tool (paywalled/blocked) | assumed to follow the HBS version; not verified. |

Where the NBER and HBS versions differ, the authors' instructions follow the NBER numbering (five explanations, Table 3, Fig. 3-11); both conventions are noted per row below.

## Our data (fixed by earlier steps)

- 487 events 2007-2026 with CARs (`events_car.csv`), `tot` = CAR in percent over [AD-1, ED+1] against .OMXSBGI; five periods.
- Net trading by FI index funds only 2019-2026 (259 events).
- LSEG daily panel: OMXSB constituents 2013-2026 + FTN losers' holdings + mapped 2007-2012 constituents (1,526 .ST RICs; 270-800 .ST stocks with prices per year), **not** all of Nasdaq Stockholm. Quoted close bid/ask present for ~90% of stock-days; `shares` present for 2% of stock-days before 2007, 70% in 2007, >86% from 2009.
- Change lists 2007-2026 (39 reviews, 536 events) and the 81-name constituent table of 2009-05-11 (read from the GlobeNewswire release) for the membership reconstruction.
- Nasdaq "OMX Stockholm Benchmark Index Methodology" (© 2025, fetched): universe OMXSPI; rank by 12-month SEK turnover; top 10% of the turnover ranking (min. 25) selected, then free-float cap within ICB supersectors to 85%; bottom 30% by turnover removed; reference dates last trading day of April/October; announcement after the close on the sixth trading day before the effective date.

## Step 1: our cleaning (not G&S)

Deletions flagged if (i) last price date in the parquet < ED+100 trading days and < panel end; (ii) `deletion_reason` in {public_offer, merger_or_acquirer, delisting_application}; (iii) |shares(ED+100 td or last available) / shares(ED) - 1| > 10%. Every test is run on "all" and "clean" (flagged deletions removed; additions never flagged). G&S instead drop events listed/acquired/delisted/acquirer within 100 days (already partly done: listed/delisted within 100 calendar days).

## Tests

| Expl. | G&S exhibit | G&S measure | Our measure | Same / deviates |
|---|---|---|---|---|
| Step 1 | A1 sample filter | drop listed, acquired, delisted, acquirer within 100 days | flags (i)-(iii) above, run with and without | deviates (our cleaning; reasons file + share jump instead of CRSP ACPERM) |
| E1 | Table 3, eq. (4) (HBS Table 2) | total return on turnover_{t-1}, size_{t-1}, vol_{t-12,t-1} + decade dummies, no constant, adds/dels separately, HC1 | `tot` on turn, size, vol + five era dummies, no constant, HC1 + CR1 (announcement date) + wild cluster bootstrap p per coefficient; adds/dels separately | same spec (uncentred, NBER eq. 4); eras are our five periods; HBS demeans and adds WZ/coverage (demeaned variant reported as a sensitivity row, WZ/coverage not available) |
| E1 turn | volume/shares over the month before the change minus VW (mcap) average over all CRSP ordinary common shares | monthly volume / shares outstanding in the calendar month before AD, minus the mcap-weighted average over all .ST stocks in the panel that month; in percent of shares | deviates: universe is the panel, not Nasdaq Stockholm; volume and shares are LSEG-adjusted series (notebook phase 2 used mean daily turnover; here monthly volume/shares as specified) |
| E1 size | mcap day before announcement / total S&P 500 mcap | mcap on AD-1 / total OMXSB mcap on AD-1 (reconstructed constituents, company-level mcap summed once per company), in percent; fallback: top-100 .ST sum | same if reconstruction works; deviates where constituents are missing from the panel (coverage reported per review) |
| E1 vol | 12-month MA of monthly sum of squared daily market-adjusted returns | same, AR against .OMXSBGI, percent² | same |
| E2 | Fig. 4 (HBS Fig. 9): VW effective spread (TAQ, Holden-Jacobsen) by year, all common shares | VW (mcap) relative quoted spread (ask-bid)/midpoint from closing quotes, daily, averaged by year, across reconstructed OMXSB constituents and across all .ST stocks in the panel; plotted with the yearly mean `tot` of additions | deviates: quoted closing spread, not effective spread; constituents/panel, not all listed shares |
| E2 | Fig. 5: implementation shortfall (Virtu/ITG) | not available | not replicated |
| E3 | Fig. 6-7, (HBS Table 3): migrations S&P MidCap <-> S&P 500 | no Swedish index pair with dedicated passive money on both sides; check OMXSB additions against the OMXS30 change list; no proxy built | not replicated (reasoning in RESULTS) |
| E4a | Fig. 8 (HBS Fig. 7 to AD+14, Table 4): cumulative market-adjusted return AD-100 to AD+10, normalised at AD+10 | same, by five periods, both samples; rows: mean CAR [AD-100, AD-1] and [AD-20, AD-1] per period | same (window AD+10 as NBER) |
| E4b | Fig. 9: cumulative return from the day before the announcement to 100 days after inclusion, normalised at the day before the change | cumulative AR from ED-1 to ED+100, normalised at ED-1 (anchored at ED as the notebook); rows: mean CAR [ED+2, ED+100] per period | deviates: anchored at ED-1, not AD-1 (said so) |
| E4c | Fig. 10 (HBS Fig. 8): monthly mcap rank of all non-index common shares; mean, p25, p75 of added stocks' rank by year | at each review, rank all non-constituents in the panel (reconstructed membership) by 6-month SEK turnover (price x volume) ending at the reference date (last trading day of the month before the announcement month); mean, p25, p75 of the added stocks' rank by year; second version with mcap; percentile ranks as well because the panel universe grows; our addition: before vs after Nov 2023 (6-day lead) | deviates: selection variable is turnover (Nasdaq rule), universe is the panel |
| E5a | Fig. 11: share of volume on each day of ED±22 by period | same | same |
| E5b | Table 4 (HBS Table 7): yearly medians of net trading by trackers vs all 13F institutions, EW mean of yearly medians | yearly medians of nt (OMXSB trackers), instbuy (all FI funds), activebuy (non-trackers), 2019-2026 only; EW mean | deviates: FI funds (mutual funds) instead of 13F; 2007-2018 missing |
| Demand | Fig. 3: event-level total return on net tracker buying | 2019-2026: `tot` on `nt` without controls, adds/dels separately, HC1 + CR1 (+ WCB). 2007-2018: expected demand = tracker AUM x index weight / mcap (= AUM / total OMXSB mcap, identical within a review) and / ADV (mean price x volume over 50 trading days ending 11 days before AD); AUM from `tracker_aum.csv` (hand-built from omxsb_notes.md section 5, linear interpolation between documented points, held flat before the first point) | same for 2019-2026; deviates for 2007-2018 (expected, not realised, demand) |

Inference everywhere: HC1 (as G&S) plus CR1 clustered on announcement date and wild cluster bootstrap (Webb weights if G < 12, Rademacher otherwise, 9,999 draws, null imposed) from the notebook's `ols`/`wcb`/`cell`/`diffcell`.

## Known problems to be flagged in RESULTS.md

- Membership chain: Nokia deleted twice (Jun 2009, Jun 2011) without a recorded re-addition; Loomis deleted Jan 2009 without a recorded addition (spin-off entry); corporate-action entries/exits outside reviews (e.g. Essity 2017) are not in the lists; the five reviews Jan 2005 to Jan 2007 are missing, so the chain starts at the July 2007 review.
- Several 2007-2012 constituents have no RIC in the panel (Nordea, Tieto, TradeDoubler, Kaupthing, Cybercom, Rederi Transatlantic, ...): coverage per review is reported; total OMXSB mcap is understated accordingly.
- `shares` is sparse before 2009, so turn and the share-jump flag are missing for part of 2007-2008.
