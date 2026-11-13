Portable replay added4 November2026. Frozen first-run code, source gates, outcomes and OUTCOME_LOCK are unchanged.

The new portable_replay.py uses the public repository paths for the fixed role file and monthly unit anchors. Both source steps write to the explicitly selected new output directory. The primary script is copied byte-for-byte and uses its existing FINANCETHESIS_REPO/OMXSB_ACTIVITY_WORKDIR settings. Exact path substitutions are listed in PORTABLE_PATH_DIFF.json and recorded verbatim in each new PORTABLE_REPLAY_LOCK.json. No population, field, date, gate, calculation or inference rule changes.

Required inputs after pulling the repository:
1. The licensed original stock panel and index CSV at their documented data/raw/lseg/panel_2005_2026 paths. These are not supplied by this publication package.
2. Published metadata in repo/output, including output/omxsb_scaled_round_20261103/independent_design/retention/FROZEN_ROLES.csv and output/omxsb_followup_20261102/volume_units_full_20261102/all_available_exactISIN_month_anchors.csv.
3. The ten original Nasdaq monthly XLS files in one directory. NASDAQ_ORIGINAL_REQUESTS.csv gives exact filenames, public source URLs and SHA256. Reuse the originals or retrieve those exact files; do not substitute a current workbook. The runner verifies every workbook hash before proceeding.
4. Install requirements.txt in a Python environment. xlrd reads the original XLS format. The optional unpublished local .deps is unnecessary when dependencies are installed normally.

From the published producer directory, run source-only validation:
python portable_replay.py --repo-root /path/to/financethesis --nasdaq-dir /path/to/nasdaq-originals --output /path/to/new-source-check --source-only

Run the complete frozen source→unit→primary chain in another NEW empty directory:
python portable_replay.py --repo-root /path/to/financethesis --nasdaq-dir /path/to/nasdaq-originals --output /path/to/new-full-replay

--compare-to defaults to the directory containing portable_replay.py and the published frozen outputs. It can explicitly point to another copy of the frozen producer package. The runner refuses to overwrite a nonempty output directory, verifies original script hashes and records generated path-only copies. Licensed intermediate amounts remain in the new output/private directory.

Actual verification performed for this portability change: source-only execution against current public-repo metadata. All nonpath cells matched exactly in280 role-presence rows,70 event-presence rows,250 month-unit rows,280 final-role rows and70 final-event rows. All flags unchanged:65 final events/10reviews. Original scripts remained unchanged; the generated primary copy is byte-identical. No second primary arithmetic was necessary or performed. The full primary calculation had already passed independent raw replay; see INDEPENDENT_VALIDATION_POINTER.json.
