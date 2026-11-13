"""Compatibility entrypoint. Canonical code lives in code/build/robusthet_hela.py."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "code/build/robusthet_hela.py"), run_name="__main__")
