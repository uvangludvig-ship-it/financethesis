# archive/

History. Nothing here guides current work; `PLAN.md` and `thesis/` do. Nothing here is deleted, so that every earlier decision can be traced.

| Folder | What it is | Period |
|---|---|---|
| `topic_selection_2026-09/` | Shortlists, CapIQ feasibility, seven synopsis drafts, blind rerank, anchor notes (the former `research/` root) | 7 Sep to 4 Oct |
| `agent_reports/` | Agent sweeps over literature and topics, red-team reports, the two raw fact reports | Sep to Oct |
| `literature_sweeps_2026-10/` | Two literature sweeps of 5 to 6 Oct and Dahlquist-Martinez notes (superseded by `thesis/literature/`) | Oct |
| `synopsis_source/` | LaTeX sources and backups of the submitted synopsis | Sep |
| `research_archive/` | The former `research/_archive/`: thesis 1 (the SSZ plan, never executed), the 11 Oct transition folder (87 files), anchor review and selection, course text extracts, old plans | Oct |
| `summaries_2026-10/` | `Thesis_summary_by_section`, `Uppsatsen_i_sammandrag` (replaced by `thesis/design/THESIS_IN_PLAIN_WORDS.md` v2) | Oct |
| `old_readmes/` | The READMEs of `thesis2/`, `thesis2/code/` and `thesis2/data/prices/` as they were on 25 Oct, before the restructuring | Oct |
| `inventory/` | `DATA_INVENTORY_2026-10-26.md` (machine-generated profile of every data file as of 26 Oct) and `STRUKTUR_2026-10-27.md` (the inventory and proposal behind the restructuring) | Oct |
| `duplicates/` | Byte-identical copies that existed in two places. The live copy is named in the file name or below. | |
| `tmp/` | anchor_audit, pdfs, winner_review: scratch from the topic selection | Sep to Oct |

## duplicates/

| File here | Identical to (the live copy) |
|---|---|
| `codebook_isin_list_lseg.csv` | `data/input/lseg/isin_list_lseg.csv` |
| `codebook_omxsb_changes_2013_2026.csv` | `data/input/omxsb/omxsb_changes_2013_2026.csv` |
| `drive-download-20261025T185638Z-1-001_same_as_panel_2012_2026.zip` | the five files in `data/raw/lseg/panel_2012_2026/` |
| `extra_ppm_2023_12.xlsm`, `extra_ppm_2024_03.xlsm`, `extra_ppm_2024_06.xlsm`, `extra_ppm_2026_06.xlsm`, `extra_ppm_2026_08.xlsm` | the same months in `data/raw/ppm/2021-2026/` |
| `root_code_ipynb_empty_placeholder.ipynb` | a 602-byte empty notebook that sat in the repo root; the real one is `code/notebooks/replication_omxsb.ipynb` |

Duplicates that were left in place because both copies are read by code or sit inside a coherent set: `data/derived/measurements/` shares four files with `data/derived/ftn/` (bids_long, winners_fee_series, reallocation_losers = agentA_task2_loser_decomposition, reallocation_summary_by_round = agentA_summary_by_round), and 20 files in `data/derived/measurements/` also exist under `archive/research_archive/revised_2026-10-11/data/`.
