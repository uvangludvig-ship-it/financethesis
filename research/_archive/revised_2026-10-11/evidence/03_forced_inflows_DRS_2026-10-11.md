# Forced inflows to winners: decreasing returns to scale feasibility (agent report, 11 Oct 2026)

Files in `data/agentDRS/` (build_drs.py; treated_funds, treated_summary, tranche_months, before_after*, ppm_post_dynamics, purge_2019*, power, meta.json, run.log). Dose = forced PPM inflow / fund-level Morningstar TNA the month before the first tranche (FX fixed: EUR 11.0, USD 10.0, NOK 0.97).

## Treated funds

| Round | Fund (role) | Tranches | Pre-TNA bn | Inflow bn | Dose | Post months (SHoF) |
|---|---|---|---|---|---|---|
| EU_active | JPM Europe Sustainable (new) | 24-06..07 | 11.2 | 1.06 | 10% | 26 |
| | Nordea European Stars (new) | 24-06 | 20.9 | 1.72 | 8% | 27 |
| | SEB Europe Equity (new) | 24-06..07 | 7.2 | 0.73 | 10% | 26 |
| | Swedbank Robur Europafond (new) | 24-06..07 | 11.2 | 1.07 | 10% | 26 |
| | abrdn European Sustainable (new) | 24-06..07 | 3.1 | 1.05 | 34% | 26 |
| EU_index | HB Europa Index / Skandia Europa / Storebrand Europa / Robur Access Europa (incumbents) | 25-02..03 | 13.9 / 6.2 / 19.6 / 15.4 | 0.99 / 0.88 / 0.47 / 0.97 | 7 / 14 / 2 / 6% | 18 |
| Global_index | HB Developed Markets (new) | 25-03..06 | 36.5 | 8.08 | 22% | 15 |
| | Storebrand Global Indeks (new) | 25-03..05 | 44.8 | 3.98 | 9% | 16 |
| | Mercer CCF (new) | 25-04..06 | n/a | 4.26 | n/a | 15 |
| | Robur Access Global / Skandia Global (incumbents) | 25-03..06 | 50.1 / 26.0 | 5.84 / 5.66 | 12 / 22% | 15 |
| Nordic_active | HB Norden Selektiv (new) | 25-05..07 | 13.6 | 1.96 | 14% | 14 |
| | Nordea Nordic / SEB Norden / Alandsbanken (incumbents) | 25-05..07 | 8.8 / 15.0 / 2.3 | 2.01 / 0.81 / 0.98 | 23 / 5 / 42% | 14 |
| Nordic_sc | SEB Nordic Small Cap (new) | 25-05..06 | 4.6 | 0.07 | 1% | 15 |
| SE_active | Cliens / HB Sverige Selektiv / SEB Sverigefond / SEB Sweden Equity / Simplicity / Robur Sverige (new) | 25-11..26-03 | 5.0 / 27.0 / 25.8 / 17.1 / 0.28 / 54.9 | 3.2 / 3.3 / 4.6 / 2.3 / 3.3 / 3.3 | 64 / 12 / 18 / 13 / 1182 / 6% | 6-7 |
| | Carnegie Sverigefond (incumbent) | 26-01..02 | 36.0 | 0.62 | 2% | 7 |
| SE_index (open) | HB Sverige Index Criteria / HB Sverige LM Index (new) | 25-10..26-06+ | 61.4 / 11.2 | 9.9 / 10.5 | 16 / 94% | 3 |
| | Aktiespararna Topp / HB Sverige 100 (incumbents) | 25-10..26-06+ | 5.5 / 15.0 | 12.4 / 6.0 | 227 / 40% | 3-5 |

Counts: 18 new winners with completed or ongoing transfer (17 with dose; median 13%, IQR 10-22%), 11 incumbents topped up by more than 10% of PPM capital (median 14%). Only 4 funds exceed 50%. The rule looks like "equalise all winners to a common PPM level" (Nordic: all four ended at about 2.35 bn). At least 12 post months: 19 funds; SE rounds 3-7 months; small-cap rounds not started. The "20-290% of AUM" premise holds only relative to PPM capital, not to fund TNA.

## Before and after (monthly SEK return minus fixed-membership category mean, leave-one-out; 12 months pre, up to 12 post, % per month)

| Group | n | pre | post | diff (median) |
|---|---|---|---|---|
| new winners | 19 | 0.00 | +0.23 | +0.22 (+0.15) |
| incumbents topped up | 11 | +0.12 | +0.41 | +0.28 (+0.10) |
| controls, unprocured equity categories | ~150 per round | 0.00 | +0.01 | about 0 |

No deterioration visible; positives are benchmark artefacts (Global index winners vs an active-heavy Global category; Norden category included small caps until mid-2025). Only abrdn (dose 34%: -0.15 to -0.72) and Carnegie fall.

PPM capital after transfer is sticky: cumulative post-window PPM net trade / forced inflow from -21% (Mercer) to +29%, median about +3%; EU_index incumbents +69 to 81% (Europe rotation). PPM share of end-TNA 7-41% (Simplicity 91%, Aktiespararna 84%). TNA growth is not PPM-only: estimated non-PPM net flow after the window +37% / +48% of TNA (JPM, Nordea), -11% (HB DM), -18% (HB Norden).

## 2019 purge (from this agent)
Platform 797 funds (Dec-18) to 478 (Dec-19). 316 exits Jan-Oct 2019 (Feb 75, Mar 79, Apr 36, May 53), capital at exit 73.7 bn (Dec-18 80.6 bn), plus 86 exits H2-2018 (21 bn). Voluntary pre-exit outflow Jan-19 to exit: net 0.2 bn (median 4% of Dec-18 capital; 32% of funds above 10%). AP7 Safa savers 4.20 to 4.48 m during 2019.

## Power (alpha 5%, 80%, 12 post months)
Idiosyncratic sd vs category mean: 1.31%/month active, 0.91 index, 0.63 index-vs-index, 0.87 treated pre-period. Cross-sectional dose slope, n = 25 treated, dose capped at 1 (sd 0.27): MDE 0.78%/month per 100% dose (9%/yr); n = 28 prospective: 0.69%/month (8%/yr; 0.33-0.46 with tighter sd). Level test treated vs benchmark: 0.20-0.27%/month (2.4-3.2%/yr). Literature (rough): PST 2015 industry-level; Zhu 2018 a few bp/month per log-size unit; Reuter-Zitzewitz about 1-3%/yr per doubling. A 13% median dose implies effects of 0.1-0.4%/yr: MDE 10-30x too large.

## Data problems
No FX (7 of 18 new winners have EUR/NOK fund TNA); Swedbank Robur/Folksam TNA reported only 2024-10 and 2026-09 (stale 3-14 months for 4 funds); Mercer unmatched; SHoF TNA gaps Feb/Mar/Jul-26; PPM ret_1m integer-rounded before 2026-03; EU_index top-ups confounded by the Mar-25 Europe rotation; SEB Sverigefond / SEB Sweden Equity inflows include same-manager mergers of losers; transfers are multi-month (SE_index 11+ months); daily RIPS not at the stated path.

## Verdict
Secondary analysis only. Doses are mostly 5-35% of fund size with 15-30 funds and at most 12 post months; MDE is an order of magnitude above plausible DRS. Use as a descriptive paragraph plus case studies (Simplicity x12, Aktiespararna x2.3, HB LM x0.9, Cliens x0.6).
