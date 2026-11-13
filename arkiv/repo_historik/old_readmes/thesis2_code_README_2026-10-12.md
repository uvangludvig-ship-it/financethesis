# code/

Analysis code for thesis 2. Python 3, numpy and pandas only. Written 12 Oct 2026 as infrastructure; the students must understand every line before it produces a number that goes into the thesis, and the analysis choices remain theirs.

| file | what it does | runs now? |
|---|---|---|
| `eventstudy.py` | the engine: factor-model abnormal returns, CARs, BMP and Kolari-Pynnonen tests, cluster-robust OLS with wild cluster bootstrap, randomisation inference within a group. `python3 eventstudy.py` runs a synthetic self-test (recovers a planted 2 per cent effect) | yes |
| `power.py` | minimum detectable effects for every table from stated assumptions; `--dose` recomputes from the actual dose file | yes |
| `parse_fi.py` | parses FI's quarterly holdings zips (VPFO XML) into long CSVs | yes, on the zips in `financethesis_ny/data/extra/` |
| `replication_omxsb.py` | Table 2, Figure 2: Greenwood-Sammon on OMXSB 2013-2026 | once `data/prices/` exists |
| `pressure.py` | equations 5 and 6 and the square-root prediction; builds `output/dose_stock_tranche.csv`; no returns | once FI quarters and prices exist |
| `ftn_eventstudy.py` | Tables 3 and 4, Figure 3 | gated: `UNBLIND = True` and a tutor-agreement date required |
| `dilution.py` | Table 5 | gated, same switch |
| `../data/exit_days/detect_exit_days.py` | reads tranche days from daily fund units and flows | yes; re-run after the November SHoF refresh |

Order of operations: (1) stock panel into `data/prices/` and run `replication_omxsb.py`; (2) FI zips, `parse_fi.py`, `pressure.py`, then `power.py --dose`; (3) Klug sign-off, flip the switch, `ftn_eventstudy.py`, `dilution.py`.

Nothing in this folder reads a stock or fund return around an FTN date until the switch is flipped.
