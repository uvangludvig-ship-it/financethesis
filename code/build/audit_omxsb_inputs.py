"""Read-only integrity and history inventory for inputs used in the OMXSB audit."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/omxsb_audit_20261031"
OUT.mkdir(parents=True, exist_ok=True)
paths = list((ROOT / "data/input/omxsb").glob("*"))
paths += list((ROOT / "data/raw/fi").glob("*.zip"))
paths += [ROOT / p for p in ["data/derived/fi/fi_holdings_long.csv.gz",
    "data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet",
    "data/raw/lseg/panel_2005_2026/stocks_daily_2005.csv.gz",
    "data/raw/lseg/panel_2005_2026/stocks_static_2005.csv",
    "data/raw/lseg/panel_2005_2026/indices_daily (1).csv",
    "data/raw/lseg/panel_2012_2026/stocks_static.csv"]]
rows = []
for p in paths:
    if not p.is_file():
        continue
    with p.open("rb") as f:
        pointer = f.read(128).startswith(b"version https://git-lfs.github.com/spec/v1")
        f.seek(0)
        digest = hashlib.file_digest(f, "sha256").hexdigest()
    r = dict(file=str(p.relative_to(ROOT)), bytes=p.stat().st_size, sha256=digest, lfs_pointer=pointer)
    blob = subprocess.run(["git", "show", "HEAD:"+r["file"]], cwd=ROOT, capture_output=True).stdout
    r["git_lfs_tracked"] = blob.startswith(b"version https://git-lfs.github.com/spec/v1")
    if r["git_lfs_tracked"]:
        r["lfs_hash_matches"] = f"oid sha256:{digest}" in blob.decode()
    try:
        if pointer:
            raise ValueError("LFS pointer, not data")
        if p.suffix == ".zip":
            with zipfile.ZipFile(p) as z:
                bad = z.testzip()
                if bad:
                    raise ValueError("CRC failed: "+bad)
                r["xml_files"] = sum(n.lower().endswith('.xml') for n in z.namelist())
        elif p.name == "stocks_daily_2005.csv.gz":
            with gzip.open(p, "rb") as f:
                while f.read(1024*1024):
                    pass
        elif p.suffix == ".parquet" or p.name.endswith((".csv", ".csv.gz")):
            d = pd.read_parquet(p) if p.suffix == ".parquet" else pd.read_csv(p, low_memory=False)
            r.update(rows=len(d), columns=";".join(d.columns))
            if "date" in d:
                r.update(date_min=str(d.date.min()), date_max=str(d.date.max()), rics=d.ric.nunique(),
                         duplicate_ric_dates=int(d.duplicated(["ric", "date"]).sum()))
                if p.suffix == ".parquet":
                    d.groupby(pd.to_datetime(d.date).dt.year).agg(rows=("ric", "size"), rics=("ric", "nunique"),
                        close=("close", "count"), shares=("shares", "count"), bid=("bid", "count"), ask=("ask", "count")).to_csv(OUT/"panel_coverage_by_year.csv")
            if "Kvartalsslut" in d:
                r.update(quarter_min=str(d.Kvartalsslut.min()), quarter_max=str(d.Kvartalsslut.max()),
                         quarters=d.Kvartalsslut.nunique(), funds=d.Fond_institutnummer.nunique())
                d.groupby("Kvartalsslut").agg(rows=("Antal", "size"), funds=("Fond_institutnummer", "nunique")).to_csv(OUT/"fi_coverage_by_quarter.csv")
            del d
        else:
            p.read_text()
        r["status"] = "readable_verified"
    except Exception as e:
        r["status"] = type(e).__name__+": "+str(e)
    rows.append(r)
pd.DataFrame(rows).to_csv(OUT/"input_inventory.csv", index=False)
print(pd.DataFrame(rows)[["file", "status"]].to_string(index=False))
