REPLAY / SAVED ANALYSIS
Use the project's Python environment with pandas, numpy, scipy, statsmodels.
Run from repository root. These depend on existing project data and frozen inputs;
they are not fresh downloads or a new blind pre-analysis plan.

python code/build/omxsb_broadening_20261102/switchers/run.py --repo . --out output/omxsb_broadening_20261102/switchers
python code/build/omxsb_broadening_20261102/switchers/validate.py --out output/omxsb_broadening_20261102/switchers
python code/build/omxsb_broadening_20261102/models/compare.py --repo . --out output/omxsb_broadening_20261102/models
python code/build/omxsb_broadening_20261102/models/verify.py --repo . --out output/omxsb_broadening_20261102/models
python code/build/omxsb_broadening_20261102/frontier/network_feasibility.py --repo . --out output/omxsb_broadening_20261102/frontier

For short positions, use its module-specific replay instructions. Do not rebuild
the source or cohort gate over a frozen version. All earlier invalid attempts
are provenance only, not additional specifications to select from.
