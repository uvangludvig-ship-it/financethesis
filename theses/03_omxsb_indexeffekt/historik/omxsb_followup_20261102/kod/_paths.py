"""Portable paths only; no analytical settings are changed."""
from pathlib import Path
import os

def analysis_paths(name):
    repo = Path(os.environ.get('OMXSB_REPO', Path(__file__).resolve().parents[3])).expanduser().resolve()
    out_root = Path(os.environ.get('OMXSB_FOLLOWUP_OUTPUT', repo / 'output/omxsb_followup_20261102')).expanduser().resolve()
    out = out_root / name
    if not (repo / 'data').is_dir():
        raise FileNotFoundError(f'Input repo not found: {repo}; set OMXSB_REPO.')
    out.mkdir(parents=True, exist_ok=True)
    return repo, out
