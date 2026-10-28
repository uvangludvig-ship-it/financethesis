# financethesis_fresh

Built 11 October 2026, from scratch: start from what Fondtorgsnämnden does, list the questions it raises, check each against the data on disk, search for anchors in both directions, read the 25 prize-winning SSE theses, and decide. Nothing in `financethesis_ny` or `financethesis_revised` was deleted or edited; those folders stay as they were.

Read in this order:

| file | what it is |
|---|---|
| `07_THESIS_PROPOSAL.md` | **The decision.** Question, anchor, exhibits, identification, power, data, risks, calendar, Klug email. Start here. |
| `01_FTN_QUESTION_MAP.md` | The institution step by step and fourteen questions scored on data, anchor, power, tutor fit and winner fit. |
| `02_WINNING_PATTERN.md` | What the 25 Per Hiller and Staffan Viotti winners 2011-2024 have in common, from the full texts. |
| `03_ANCHORS_flows_prices.md` | Anchor search, flows and prices: Greenwood-Sammon, Lou, Da et al., Jin et al., Pavlova-Sikorskaya, PST. Swedish swing-pricing law verified. |
| `04_ANCHORS_selection_fees.md` | Anchor search, selection, bidding, fees: Cookson et al., Goyal-Wahal-Yavuz, Hortacsu-Syverson, Cooper-Halling-Yang, Sun. |
| `05_ANCHORS_savers.md` | Anchor search, savers and defaults: SSZ, Keim-Mitchell, Choukhmane-De Silva, Kronlund et al., Barber-Odean, Dahlquist et al. |
| `06_NEW_FACTS.md` | Nine descriptive facts measured today, no returns used: appeal null, gender gap, share classes, fee savings, concentration, 94 per cent default, execution months, stock-level pressure, who-pays inputs. |
| `08_BLIND_REFEREE.md` | A referee with no context compared the SSZ plan and file 07; verdict and the Friday 17 Oct gate. |
| `thesis/` | The deep-research pass on thesis 2 (12 Oct): validation against the referee, full design with equations and power, data instructions, outline from the winners, verified literature, OMXSB and swing-pricing data, tranche days, code. Start at `thesis/design/00_VALIDATION.md`. |

`data/`:

- `facts/` scripts and CSVs behind facts 1 to 5 (`common.py` loads the panel).
- `measurements/` summaries and scripts behind facts 6 to 9: round membership and loser decomposition (`agentA_*`), the 2019 purge (`agent2019_*`), stock-level pressure from FI holdings (`fip_*`, `execution_windows_monthly.csv`, `parse_fi.py`, `fip.py`), winners' fee series, all 290 bids (`bids_long.csv`). The full FI holdings files (79 MB) are in `financethesis_revised/data/agentP/`.
- `panel/` the fund-month panel 2018-2026 and the script that builds it from Pensionsmyndigheten's monthly files.
- `winners/` the table of the 25 winners (anchor, data, method, pages) and the course introduction text.
- `agent_reports/` the raw reports from the savers-anchor search and the facts check, before editing.

Rules kept: no stock or fund return around any FTN date has been computed (blind rule); these are planning files, the thesis prose is the students' own (course rule); nothing old deleted.

Short version of the decision: the thesis is about the forced flow. Anchor Greenwood and Sammon (2025) JF, replicated on OMXS30 reconstitutions; extension on FTN's dated, uninformed, 20 to 44 per cent redemptions at the stock level (anticipation, execution, reversal) and at the fund level (who paid: stayers through dilution or movers through swing pricing); conclusion sets the transition cost against fee savings of 178 MSEK a year. Savers, defaults and gender are a second paper.
