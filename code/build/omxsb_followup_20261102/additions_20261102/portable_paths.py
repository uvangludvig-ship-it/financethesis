"""Path adapters only; no analytical rules or source classifications."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys


def analysis_paths(name):
    repo = Path(os.environ.get('OMXSB_REPO', Path(__file__).resolve().parents[4])).expanduser().resolve()
    code = repo / 'code/build/omxsb_followup_20261102'
    if not (code / '_paths.py').is_file():
        raise FileNotFoundError(f'First follow-up package missing under {repo}; use --repo or OMXSB_REPO.')
    sys.path.insert(0, str(code))
    from _paths import analysis_paths as existing_paths
    return existing_paths(name)


def first_output(repo):
    """Read old secondary inputs from the first package, never from a staging sibling."""
    return repo / 'output/omxsb_followup_20261102'


def comparison_function(repo, module, name):
    """Import the existing, main-guarded arithmetic without running its analysis."""
    source = repo / 'code/build/omxsb_followup_20261102/comparison_rebuild_20261102' / (module + '.py')
    key = '_omxsb_first_package_' + module
    previous = os.environ.get('OMXSB_FOLLOWUP_OUTPUT')
    try:
        # Existing helper imports call analysis_paths. Keep that benign directory check
        # in the already existing first package; do not create old groups in staging.
        os.environ['OMXSB_FOLLOWUP_OUTPUT'] = str(first_output(repo))
        spec = importlib.util.spec_from_file_location(key, source)
        imported = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported)
    finally:
        if previous is None:
            os.environ.pop('OMXSB_FOLLOWUP_OUTPUT', None)
        else:
            os.environ['OMXSB_FOLLOWUP_OUTPUT'] = previous
    return getattr(imported, name)


def repository_source(repo, original):
    """Resolve unchanged historical JSON provenance to this checkout."""
    old_root = Path('/Users/ludviguvang/dev/financethesis')
    path = Path(original)
    if path.is_absolute():
        return repo / path.relative_to(old_root)
    return repo / path


def verify_original_lock(output, manifest):
    """Preserve the original manifest, checking frozen data and archived original code."""
    archive = output.parent / 'additions_20261102/archived_original_work' / output.name
    for original, expected in json.loads((output / manifest).read_text()).items():
        name = Path(original)
        assert name.parent.name == output.name, ('Unexpected lock source', original)
        target = (archive if name.suffix == '.py' else output) / name.name
        assert hashlib.sha256(target.read_bytes()).hexdigest() == expected, ('Original lock failed', target)
