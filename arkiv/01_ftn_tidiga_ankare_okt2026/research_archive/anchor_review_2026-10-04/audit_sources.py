"""Reproduce the source-availability and descriptive corpus audit. No thesis estimates.

Run from the repository root with Python 3. Uses only the standard library.
Reads newly downloaded public files; deliberately never reads data/.
"""
import collections
import csv
import datetime
import hashlib
import io
import json
import re
import statistics
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SRC = OUT / "sources"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def workbook_rows(path):
    """Read cached values without executing macros or modifying the workbook."""
    with zipfile.ZipFile(path) as archive:
        strings = ["".join(el.itertext()) for el in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        rels = {x.get("Id"): x.get("Target") for x in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))}
        book = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets = {}
        for sheet in book.find("m:sheets", NS):
            rid = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = rels[rid]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            rows = []
            for row in ET.fromstring(archive.read(target)).findall(".//m:row", NS):
                cells = {}
                for cell in row:
                    value = cell.find("m:v", NS)
                    if value is None or value.text is None:
                        continue
                    col = re.sub(r"\d", "", cell.get("r"))
                    cells[col] = strings[int(value.text)] if cell.get("t") == "s" else value.text
                rows.append({"row": int(row.get("r")), "cells": cells})
            sheets[sheet.get("name")] = rows
        return sheets


def public_data_audit():
    funds = []
    with zipfile.ZipFile(SRC / "fi_2026q2.zip") as archive:
        for name in archive.namelist():
            if not name.endswith(".xml"):
                continue
            root = ET.fromstring(archive.read(name))
            def value(tag):
                node = root.find(".//{*}" + tag)
                return node.text if node is not None else None
            funds.append({"file": name, "name": value("Fond_namn"), "isin": value("Fond_ISIN-kod"),
                          "aum": value("Fondförmögenhet"), "date": value("Kvartalsslut"),
                          "fi_id": value("Fond_institutnummer"),
                          "single_class_flag": root.find(".//{*}UtanAndelsklasser") is not None})
    book = workbook_rows(SRC / "ppm_2026_06.xlsm")
    stats = {r["cells"]["A"]: r for r in book["Fondstatistik"]
             if r["cells"].get("A", "").isdigit() and len(r["cells"]["A"]) == 6}
    amounts = {r["cells"]["A"]: r for r in book["Fondval & marknadsvärde"]
               if r["cells"].get("A", "").isdigit() and len(r["cells"]["A"]) == 6}
    fi_by_isin = collections.defaultdict(list)
    for row in funds:
        fi_by_isin[row["isin"]].append(row)
    matches = []
    for fid, row in stats.items():
        cells = row["cells"]
        hit = fi_by_isin.get(cells.get("S"), [])
        if len(hit) != 1 or fid not in amounts:
            continue
        fi = hit[0]
        ppm = amounts[fid]
        matches.append({"ppm_id": fid, "isin": cells.get("S"), "ppm_name": cells.get("B"),
                        "fi_name": fi["name"], "date": fi["date"], "fi_total_aum": fi["aum"],
                        "ppm_aum": ppm["cells"].get("H"), "ppm_net_trade": ppm["cells"].get("I"),
                        "ppm_stat_row": row["row"], "ppm_amount_row": ppm["row"],
                        "procured": ppm["cells"].get("O", ""), "fi_file": fi["file"],
                        "single_class_flag": fi["single_class_flag"]})
    selected = [r for r in matches if "AMF Aktiefond Europa" in r["ppm_name"] or "Swedbank Robur Europafond" in r["ppm_name"]]
    result = {
        "checked_on": "2026-10-04", "fi_xml_files": len(funds), "fi_dates": sorted(set(f["date"] for f in funds)),
        "fi_with_aum": sum(bool(f["aum"]) for f in funds), "ppm_six_digit_fund_records": len(stats),
        "exact_unique_isin_matches": len(matches), "matched_procured_funds": sum(bool(m["procured"]) for m in matches),
        "single_class_matches": sum(m["single_class_flag"] for m in matches),
        "single_class_procured_matches": sum(m["single_class_flag"] and bool(m["procured"]) for m in matches),
        "examples": selected, "all_matches": matches,
        "limitations": ["One quarter and exact ISIN matches only; not historical coverage or a complete parent-fund mapping.",
                        "FI covers Swedish UCITS only, excluding foreign funds and special funds.",
                        "No direct outside-PPM flow is supplied by these two public files.",
                        "AUM subtraction is a stock of outside-PPM assets, not a flow.",
                        "FI fee fields and PPM TER are not automatically the same fee definition."]}
    (OUT / "public_data_audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "all_matches"}, indent=2, ensure_ascii=False))


def historical_probe():
    """Verify one known winner across the announcement, without estimating effects."""
    observations = []
    for quarter, month in [("2023q4", "2023_12"), ("2024q1", "2024_03"), ("2024q2", "2024_06")]:
        with zipfile.ZipFile(SRC / ("fi_" + quarter + ".zip")) as archive:
            hits = []
            for name in archive.namelist():
                if not name.endswith(".xml"):
                    continue
                root = ET.fromstring(archive.read(name))
                isin = root.find(".//{*}Fond_ISIN-kod")
                if isin is not None and isin.text == "SE0000739153":
                    hits.append((name, root))
            assert len(hits) == 1, (quarter, len(hits))
            filename, root = hits[0]
            book = workbook_rows(SRC / ("ppm_" + month + ".xlsm"))
            ppm = next(r for r in book["Fondval & marknadsvärde"] if r["cells"].get("A") == "538462")
            stats = next(r for r in book["Fondstatistik"] if r["cells"].get("A") == "538462")
            header = next(r for r in book["Fondstatistik"] if r["cells"].get("A") == "Fondnummer")
            isin_col = next(col for col, value in header["cells"].items() if value == "ISIN-kod")
            assert stats["cells"][isin_col] == "SE0000739153"
            observations.append({"quarter": quarter, "date": root.find(".//{*}Kvartalsslut").text,
                                 "fi_aum_sek": root.find(".//{*}Fondförmögenhet").text,
                                 "ppm_aum_sek": ppm["cells"]["H"], "ppm_row": ppm["row"],
                                 "fi_file": filename, "ppm_isin_column": isin_col,
                                 "single_class_flag": root.find(".//{*}UtanAndelsklasser") is not None})
    prices = []
    for sheet, rows in workbook_rows(SRC / "ppm_nav_2024.xlsx").items():
        for row in rows:
            c = row["cells"]
            if c.get("B") == "538462":
                date = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(c["D"])))
                prices.append({"date": date.isoformat(), "nav_sek_sell": c["J"], "sheet": sheet, "row": row["row"]})
    quarter_ends = [max((r for r in prices if r["date"] <= end), key=lambda r: r["date"])
                    for end in ["2024-03-31", "2024-06-30"]]
    result = {"fund": "AMF Aktiefond Europa", "isin": "SE0000739153", "ppm_id": "538462",
              "observations": observations, "nav_2024_observations": len(prices),
              "nav_quarter_end_examples": quarter_ends,
              "conclusion": "Historical matching and NAV availability verified for one fund; no flow or treatment effect estimated.",
              "limitations": ["NAV is not distribution-adjusted; check distributions and fund events before computing returns.",
                              "One fund does not establish panel-wide historical coverage or statistical power.",
                              "Quarter-end PPM and FI valuation dates must be reconciled with actual NAV dates.",
                              "ISIN and other columns change between workbook vintages; use headers, not fixed positions."]}
    (OUT / "historical_public_probe.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def master_probe():
    with zipfile.ZipFile(SRC / "shof_fundmaster.zip") as archive:
        rows = workbook_rows(io.BytesIO(archive.read("fundmaster.xlsx")))["fundmaster"]
    fields = rows[0]["cells"]
    records = [{fields[k]: v for k, v in row["cells"].items() if k in fields}
               for row in rows[1:] if row["cells"].get("A")]
    matches = [r for r in records if r.get("ISIN") == "SE0000739153"]
    result = {"downloaded_on": "2026-10-04", "records": len(records),
              "distinct_fundids": len({r.get("fundid") for r in records if r.get("fundid")}),
              "amf_europe_identity": [{k: r.get(k) for k in
                  ["ISIN", "performanceid", "secid", "fundid", "currencyid", "fundname", "AUM_lastupdate", "lastupdate"]} for r in matches],
              "limitation": "Public identity master verified; its snapshot assets/returns do not supply historical monthly valuations. Row count is not fund count. Date fields are Excel serial dates."}
    (OUT / "shof_master_probe.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


def corpus_audit():
    catalogue = json.loads((ROOT / "non_winners/catalogue_index.json").read_text())["records"]
    meta = json.loads((ROOT / "non_winners/extraction_meta.json").read_text())
    index = (ROOT / "old_winners/INDEX.md").read_text()
    winner_paths = dict(re.findall(r"\[PDF\]\(([^)]+)\.pdf\).*?MediumId=(\d+)", index))
    winner_ids = set(winner_paths.values())
    path_by_id = {fid: ROOT / "old_winners/text" / (stem + ".txt") for stem, fid in winner_paths.items()}
    records = []
    for row in catalogue:
        fid = str(row["mediumid"])
        path = path_by_id.get(fid, ROOT / "non_winners/text" / (fid + ".txt"))
        text = path.read_text(errors="replace")
        pages = meta.get(fid, {}).get("pages")
        record = {"id": fid, "year": int(row["year"]), "title": row["title"],
                  "winner_collection": fid in winner_ids, "flagged_other_award": fid == "6338",
                  "words": len(text.split()), "pages": pages,
                  "contents_heading": bool(re.search(r"^\s*(?:table of )?contents\s*$", text[:15000], re.I | re.M))}
        records.append(record)
    winners = [r for r in records if r["winner_collection"]]
    comparison = [r for r in records if not r["winner_collection"] and 2011 <= r["year"] <= 2024]
    weights = collections.Counter(r["year"] for r in winners)
    def stats(rows):
        pp = [r["pages"] for r in rows if r["pages"] is not None]
        return {"n": len(rows), "median_words": statistics.median(r["words"] for r in rows),
                "median_pdf_pages": statistics.median(pp), "known_pdf_page_counts": len(pp),
                "contents_heading_n": sum(r["contents_heading"] for r in rows),
                "contents_heading_pct": 100 * statistics.mean(r["contents_heading"] for r in rows)}
    weighted_toc = sum(n * statistics.mean(r["contents_heading"] for r in comparison if r["year"] == year)
                       for year, n in weights.items()) / len(winners)
    result = {"catalogue_n": len(records), "winner": stats(winners), "same_year_comparison": stats(comparison),
              "comparison_contents_pct_reweighted_to_winner_years": 100 * weighted_toc,
              "excluded_2009_2010": sum(r["year"] < 2011 for r in records),
              "excluded_2025_2026": sum(r["year"] > 2024 for r in records),
              "limitations": ["Absence from the awarded collection is not verified non-winning status or a low grade.",
                              "Prize years, examiners and eligibility differ. No causal explanation of awards is estimated.",
                              "Existing thesis_metrics.py has fragile reference extraction and its case-insensitive DiD pattern matches the ordinary word 'did'. Those measures are not used for conclusions.",
                              "Contents detection is a text heuristic, and PDF pages include appendices and front matter."]}
    (OUT / "corpus_summary.json").write_text(json.dumps(result, indent=2) + "\n")
    with (OUT / "corpus_inventory.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    public_data_audit()
    historical_probe()
    master_probe()
    corpus_audit()
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SRC.iterdir()) if p.is_file()}
    (OUT / "source_sha256.json").write_text(json.dumps(hashes, indent=2) + "\n")
