# Main quantities and provenance

The complete input inventory is `replication/thesis_final/data/FILES.csv`. Original transformation code is retained unchanged under `replication/thesis_final/code/`. This dictionary describes the quantities used in the manuscript, including their units and interpretation boundaries.

| Quantity | Definition and units | Main provenance | Limitation |
|---|---|---|---|
| Event | Security entering or leaving OMXSB at one review | Nasdaq event inventory with historical security mapping | An issuer may contribute several events/classes |
| Review | Reconstitution cycle | `review_cycle` in event files | Primary cluster; not proof of independent cycles |
| AD | Recorded announcement trading date | Notice inventory and mapped trading calendar | Intraday timestamp not resolved by daily prices |
| ED | Effective trading date | Historical notice inventory | Earlier January/July dates are retained |
| Stock return | Reported daily total return; closing-price percentage-change fallback when missing | LSEG stock panel | Fallback may omit dividends; vendor observations not independently authenticated |
| Market return | Daily percentage change in OMXSBGI | LSEG index panel | Unit-beta market adjustment |
| CAR | Sum of daily stock minus market returns, percentage points | `returns.py`; independent reconstruction | Arithmetic, not compounded; not causal |
| Main CAR | CAR from AD-1 to ED+1, inclusive | Main event table | Complete-window requirement changes sample |
| Initial seven-day CAR | CAR from AD-1 through AD+5; seven daily returns, same complete events as main CAR | `return_definition_checks.py`; independently checked by `fixed_window_decomposition.py` | Exploratory; ends before ED for every event; not proof of equal responses across periods |
| Remaining CAR | CAR from AD+6 through ED+1; adds exactly to the initial seven-day CAR to give the main CAR | `fixed_window_decomposition.py` | Varying duration and composition; not a causal calendar decomposition |
| Announcement CAR | AD-1 to AD+1 | Main event table | Includes pre-announcement day |
| Implementation CAR | ED-1 to ED+1 | Main event table | Not an intraday execution measure |
| Extended CAR | AD-1 to ED+20 on fixed complete cases | Independent audit | Exploratory; finite horizon |
| Y | Main CAR multiplied by +1 for additions or -1 for deletions | Fund-demand calculation | Sign convention does not identify demand impact |
| B | Strict OMXSB follower group | Curated, dated fund classifications | Not a mechanically applied diagnostic threshold |
| V | B plus benchmark variants | Curated, dated fund classifications | Broader covered investor definition |
| C | V plus relevant mixed-fund exposure | Dated classifications; actual security holdings (benchmark weights apply only to the separate AUM measure) | Main measure; incomplete passive population |
| D | Sign-adjusted change in covered holdings divided by shares outstanding, multiplied by 100 | LSEG/Lipper reports; `02_fund_demand.py` | Report completeness, zero-position and share-adjustment assumptions |
| M | Mean Y divided by mean D on identical adjustment-screened complete cases | Fund-demand aggregates | Ratio of means; not structural elasticity |
| Adjustment screen | Ratio of market-cap/share-count/adjusted-price proxy at ED to the proxy at the last available price date; retain [1/1.4, 1.4] | Original `runda11.py`; independently checked by `share_adjustment_dd.py` | Not an event-window split screen; time-dependent attrition and vendor adjustment conventions matter |
| FI check | Holdings measure derived from quarterly FI data, on matched events | `03_fund_demand_fi_check.py` | Overlap comparison, not full historical coverage |
| Volume share | Daily volume divided by volume over ED±22, multiplied by 100 | Broad stock panel | Missing volume set to zero; not auction volume |
| Quoted spread | Closing ask minus bid divided by midpoint, percent | Broad stock panel | Not effective spread; >20% quotes excluded |
| Relative size | Capitalization relative to available universe | Composition controls | Historical denominator and class mapping matter |
| Comparison group | Available securities passing inherited size screens | Original `14_near_additions_control.py`; revised `comparison_repair.py` | Not Nasdaq threshold assignment; revised pre-return ends at AD-2, removing the inherited AD-1 overlap |
| MSCI overlap | Inherited matched OMXSB/MSCI event status | MSCI changes via LSEG | Exclusion changes population, not causal attribution |
| News exclusion | Flags from review of 24 extreme inherited events | Targeted source-based screen | Outcome-informed and incomplete |
| Twin return | Sign-adjusted relative log return of indexed and sibling class | Share-class panel and supplementary sources | Different outcome from main CAR; possible spillovers |
| Issuance | Share-count growth AD-5 to ED+60 after heuristic split adjustment | Original other-tests code | Corporate-action reconciliation incomplete |

Sources are differentiated in the reference ledger: publication metadata, retrieved primary documents, secondary republications, inherited records and computations are not interchangeable evidence levels.
