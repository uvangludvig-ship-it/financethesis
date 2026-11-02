Frozen short-position profile replay

This directory contains one exploratory economic test, plus its source collection and quality-gate history. No thesis prose, return regression, FTN outcome or repository file was changed.

Portable replay (Python3.14.7, pandas2.3.3, numpy2.5.4):
  python /path/to/run.py --input /path/to/frozen_input_directory --out /path/to/new_output_directory
  python /path/to/verify.py --input /path/to/frozen_input_directory --out /path/to/new_output_directory

No repository path is needed for this frozen replay: the final paired official exports and cohort are self-contained in the input directory. Keep the files listed in COHORT_LOCK.json together; the portable reader resolves their historical paths by unique basenames and verifies their unchanged original hashes. It does not download data or rebuild the gate. It reproduces holder_position_intervals.csv, issuer_position_intervals.csv, review_position_intervals.csv and RESULTS.json; verifier checks original ODS cells and aggregation independently.

REPLAY_COMPARISON.json records that the three scientific tables are byteidentical. RESULTS.json includes runtime/source metadata, so the replay copy differs in time/path plus an explicit positive-part-estimand label. archived_original_run/ retains exact original run.py and result metadata. A first portable replay had a local variable/path-name collision; this was corrected before the successful run and did not change scientific table values. No old gate or lock was rewritten during portability adaptation.

Source files for repository collection:
  AktuellaPositioner_2026-11-02.ods
  HistoriskaPositioner_2026-11-02.ods
  current_download.json, complete_sources.json, download_log.csv
The original31October ODS stays unchanged in the repository. Original parsed history is raw_positions.csv.gz; completed contemporaneous history/current data are complete_positions_20261102.csv.gz. Source references in tables identify export kind and one-based ODS row.

Upstream inventory.py, complete_sources.py and gate.py document collection/transformation and require their recorded local inputs. Do not rerun gate.py as a routine result replay: it creates a new lock timestamp. The original gate variants remain in gate_v1_before_terminal_check/ and gate_v2_history_only_terminal_check/. No economic output was calculated for those variants. The sole analysed final cohort is47 holder-event pairs/28 issuer events/13 reviews.

DECLARATION.txt, QA_TERMINAL_AMENDMENT.txt and QA_COMPLETE_EXPORTS_BEFORE_OUTCOMES.txt record the sequence before results. CLARIFICATION_MEASURE.txt clarifies that unchanged[0;0.5) bounds refer to max(net short,0), not signed exposure. REPORT.txt is an audit/research note, not thesis text.
