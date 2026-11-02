OMXSB mechanism/ownership follow-up, 2 November2026
Technical local data/code/audit material, not thesis text. Start with RESULTAT.txt.

Inputs: existing repository data/derived/fi/fi_holdings_long.csv.gz, FI latest-report metadata, old immutable output/omxsb_open_questions_20261102 bundle, event files, and reviewed ISIN aliases. Neither original inputs nor older outputs are overwritten. Set FINANCETHESIS_REPO only if using another checkout location.
Python environment: /tmp/omxsb-audit-venv/bin/python ; dependencies in requirements.lock.
Run ownership scripts in this order: build_gate.py, screen_identity.py, run.py, decompose.py, manager_check.py, make_figure.py. Then run the independent_*validation/check scripts listed in ownership/. All write only their own directory. Archived earlier attempts are retained for provenance, not intended as current entry points.
Demand: run demand/build_panel.py then demand/validate_and_describe.py; owner_contributors.py reads final ownership outputs. Design feasibility: design/feasibility.py. These are not additional price regressions.
Look at ANALYSIS_DECISIONS and later separately timestamped decisions before outcomes. This is exploratory follow-up after earlier known results, not a blinded preregistration. Old failed T14 remains stopped.
Source URLs/read scopes are in demand/source_ledger.csv and literature/. A downloaded Nordea file has2024 in filename/URL but actual2025content; never treat it as2024evidence. Nordnetblogredirect and unavailable historical lists are recorded as missing sources.
The final fund-count table uses219eventsets118additions101deletions,14reviews. Quantity panel is a different205price-overlap sample: never combine means as though samples/units were equal.
No causal price mechanism or long-run permanence is claimed. No FTN returns, email or publication. All prior phases retained.
