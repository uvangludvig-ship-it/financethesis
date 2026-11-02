"""Isolated, logged execution of every OMXSB notebook code cell and mechanism script.

No analytical expressions are rewritten. Only output paths are redirected for the
frozen baseline, whose sources are read from the preserved snapshot.
"""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "output/omxsb_audit_20261031"
ORIGINAL = AUDIT / "original"
BASE_COMMIT = "b886f5b744f797a6c1252f0e41fe2b740591c8c3"
NB = Path("code/notebooks/replication_omxsb_2007.ipynb")
SCRIPTS = [Path("code/build") / f for f in
           ["mechanisms_2007.py", "period_sensitivity.py", "trend_tests.py"]]

def sha(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def snapshot():
    if ORIGINAL.exists():
        return
    ORIGINAL.mkdir(parents=True)
    exports = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE_COMMIT,
                                      "output/omxsb_replication_2007"], cwd=REPO, text=True).splitlines()
    for path in [NB] + SCRIPTS + list(map(Path,exports)):
        dest = (ORIGINAL / "exports" / path.relative_to("output/omxsb_replication_2007")) if str(path).startswith("output/") else ORIGINAL / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{path}"],cwd=REPO))
    records = [{"file": str(p.relative_to(ORIGINAL)), "sha256": sha(p)}
               for p in sorted(ORIGINAL.rglob("*")) if p.is_file()]
    (AUDIT / "original_sha256.json").write_text(json.dumps(records, indent=2))
    (AUDIT / "starting_git.json").write_text(json.dumps({
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "status_at_snapshot": subprocess.check_output(["git", "status", "--short"], cwd=REPO, text=True),
        "initial_status_before_audit": "clean (verified before creating audit files)",
        "origin_HEAD_verified": "b886f5b744f797a6c1252f0e41fe2b740591c8c3"
    }, indent=2))

def run(stage, periods):
    from IPython.display import display
    snapshot()
    os.chdir(REPO)
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/omxsb-audit-matplotlib")
    root = ORIGINAL if stage == "baseline" else REPO
    dest = AUDIT / stage
    dest.mkdir(parents=True, exist_ok=True)
    nb = json.loads((root / NB).read_text())
    ns = {"__name__": "__main__", "display": display}
    log = AUDIT / f"{stage}.log"
    start = time.time()
    with log.open("w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] != "code":
                continue
            src = "".join(c["source"])
            if i == 1:
                src = src.replace('OUT = os.path.join(REPO, "output", "omxsb_replication_2007")',
                                  f'OUT = {str(dest)!r}')
                src = src.replace('PHASE1 = os.path.join(REPO, "output", "omxsb_replication_2007", "tables", "tab_02_car_long_phase1.csv")',
                                  'PHASE1 = os.path.join(OUT, "tables", "tab_02_car_long_phase1.csv")')
            print(f"CELL {i} START", flush=True)
            exec(compile(src, f"{root / NB}:cell_{i}", "exec"), ns)
            print(f"CELL {i} DONE", flush=True)
            # Later plot cells reuse h for legend handles; inspect before that.
            if stage == "corrected" and i == 42:
                import audit_omxsb_holdings
                audit_omxsb_holdings.run(ns, AUDIT)
    del ns
    for path in SCRIPTS if periods else SCRIPTS[:1]:
        src = (root / path).read_text()
        src = src.replace('OUT0 = os.path.join(REPO, "output", "omxsb_replication_2007")',
                          f'OUT0 = {str(dest)!r}')
        if stage == "baseline":
            src = src.replace('os.path.join(REPO, "code", "notebooks", "replication_omxsb_2007.ipynb")',
                              repr(str(ORIGINAL / NB)))
        with log.open("a") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
            print(f"SCRIPT {path} START", flush=True)
            exec(compile(src, str(root / path), "exec"), {"__name__": "__main__", "__file__": str(REPO / path)})
            print(f"SCRIPT {path} DONE", flush=True)
    (dest / "run_complete.json").write_text(json.dumps({"stage": stage, "seconds": time.time()-start,
        "notebook_sha256": sha(root / NB), "scripts": {str(p): sha(root / p) for p in SCRIPTS if periods or p == SCRIPTS[0]},
        "python": sys.version, "all_code_cells_executed": True}, indent=2))
    print(f"{stage} complete in {time.time()-start:.1f}s: {dest}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("stage", choices=["baseline", "corrected", "snapshot"])
    p.add_argument("--periods", action="store_true")
    args = p.parse_args()
    snapshot() if args.stage == "snapshot" else run(args.stage, args.periods)
