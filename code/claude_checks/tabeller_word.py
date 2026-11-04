# Created: 2026-11-04 17:06:54 CET (from date)
"""Build journal-style Word tables from the thesis CSV sources.

Run with Python and the packages pandas and python-docx installed.
Paths are relative to the repository, independently of the working directory.
Reported values are computed from source data; literals in checks are only
the reference values requested for validation, never table inputs.
"""

from pathlib import Path
import hashlib
import subprocess

import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/tabeller"
EVENTS = ROOT / "code/claude_checks/rattelser_2026-11-03_resultat/handelser_rattade.csv"
SAMPLE = ROOT / "output/omxsb_replication_2007/tables/tab_01_sample.csv"
CAR = ROOT / "output/omxsb_replication_2007/events_car.csv"
PERIODS = ("2007–11", "2012–16", "2017–21", "2022–26")
MEASURES = ("k_oms", "k_storlek", "k_wz", "k_ana")
TABLE2_NOTE = (
    "Means by period of the effective date. Abnormal turnover: the security's "
    "SEK turnover over market value, averaged over the 21 trading days before "
    "AD, less the value-weighted mean for the main list. Size: market value "
    "the day before AD as a share of OMXSB's total, in percent. Arbitrage risk: "
    "residual variance of daily returns on OMXSBGI over [AD−250, AD−2] "
    "(Wurgler and Zhuravskaya, 2002). Analysts: number of FY1 EPS forecasts "
    "in the month before AD. Source: LSEG; authors' calculations."
)


def decimal(value, places):
    """Use decimal points and suppress the sign of rounded negative zero."""
    if pd.isna(value):
        return "—"
    rounded = round(float(value), places)
    return f"{0.0 if rounded == 0 else rounded:.{places}f}"


def load_tables():
    events = pd.read_csv(EVENTS)
    for col in (*MEASURES, "D_ny"):
        events[col] = pd.to_numeric(events[col], errors="raise")
    if events["per"].isna().any() or not set(events["per"]).issubset(PERIODS):
        raise ValueError("Unexpected or missing period in corrected events")
    if not set(events["type"]).issubset({"addition", "deletion"}):
        raise ValueError("Unexpected event type")
    additions = events.loc[events["type"].eq("addition")]
    grouped = additions.groupby("per")
    means = grouped[list(MEASURES)].mean().reindex(PERIODS)
    counts = grouped["k_oms"].count().reindex(PERIODS)
    table2 = [
        [period, str(int(counts.loc[period]))]
        + [decimal(means.loc[period, col], places)
           for col, places in zip(MEASURES, (2, 2, 1, 1))]
        for period in PERIODS
    ]

    sample = pd.read_csv(SAMPLE, header=[0, 1], index_col=0)
    total = sample.loc["Total"]
    labels = (
        ("Changes in Nasdaq's index lists", "In event list"),
        ("With ten closing prices around the change", "With price data"),
        ("Listed 100 days before and after", "After filter"),
    )
    panel_a = []
    for label, group in labels:
        n_add = int(total[(group, "Additions")])
        n_del = int(total[(group, "Deletions")])
        panel_a.append([label, str(n_add), str(n_del), str(n_add + n_del)])
    car = pd.read_csv(CAR)
    car["tot"] = pd.to_numeric(car["tot"], errors="raise")
    complete = car.loc[car["tot"].notna()].groupby("type").size()
    n_add = int(complete.get("addition", 0))
    n_del = int(complete.get("deletion", 0))
    panel_a.append([
        "Complete window AD−1 to ED+1", str(n_add), str(n_del), str(n_add + n_del)
    ])

    # Normalize bool/string representations explicitly; missing flags are not False.
    split = events["split"].astype("string").str.lower()
    if not split.dropna().isin(["true", "false"]).all():
        raise ValueError("Unexpected split flag")
    eligible = events.loc[events["D_ny"].notna() & split.eq("false").fillna(False)]
    by_period = eligible.groupby(["per", "type"]).size().unstack(fill_value=0)
    by_period = by_period.reindex(index=PERIODS, columns=["addition", "deletion"])
    by_period = by_period.fillna(0).astype(int)
    panel_b = [
        [period, str(row["addition"]), str(row["deletion"]), str(row.sum())]
        for period, row in by_period.iterrows()
    ]

    # Requested checks: reference literals never supply document values.
    assert table2[0][2:] == ["0.00", "0.17", "6.0", "4.0"], table2[0]
    assert panel_a[0][1:] == ["284", "252", "536"], panel_a[0]
    assert panel_a[-1][1:3] == ["256", "225"], panel_a[-1]
    return table2, panel_a, panel_b


def document(title):
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(2.5)
    section.left_margin = section.right_margin = Cm(2)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1
    caption = doc.add_paragraph()
    caption.paragraph_format.keep_with_next = True
    caption.paragraph_format.space_after = Pt(8)
    caption.add_run(title).bold = True
    doc.core_properties.author = ""
    doc.core_properties.title = title
    return doc


def rule(cell, edge):
    borders = cell._tc.get_or_add_tcPr().find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        cell._tc.get_or_add_tcPr().append(borders)
    line = OxmlElement(f"w:{edge}")
    for name, value in (("val", "single"), ("sz", "6"), ("color", "000000")):
        line.set(qn(f"w:{name}"), value)
    borders.append(line)


def make_table(doc, headers, rows, widths, panels=()):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for col, width in zip(table.columns, widths):
        col.width = Cm(width)
    # Override all style borders: only the three explicit horizontal rules remain.
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "bottom", "left", "right", "insideH", "insideV"):
        line = OxmlElement(f"w:{edge}")
        line.set(qn("w:val"), "nil")
        borders.append(line)
    table._tbl.tblPr.append(borders)
    for cell, header in zip(table.rows[0].cells, headers):
        cell.text = header
        rule(cell, "top")
        rule(cell, "bottom")
    repeat = OxmlElement("w:tblHeader")
    table.rows[0]._tr.get_or_add_trPr().append(repeat)
    for values in rows:
        cells = table.add_row().cells
        if isinstance(values, str):
            cells[0].merge(cells[-1]).text = values
        else:
            for cell, value in zip(cells, values):
                cell.text = value
    for cell in table.rows[-1].cells:
        rule(cell, "bottom")
    for i, row in enumerate(table.rows):
        props = row._tr.get_or_add_trPr()
        props.append(OxmlElement("w:cantSplit"))
        is_panel = i in panels
        for j, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if not is_panel:
                cell.width = Cm(widths[j])
            for paragraph in cell.paragraphs:
                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.LEFT if j == 0 or is_panel
                    else WD_ALIGN_PARAGRAPH.RIGHT
                )
                paragraph.paragraph_format.space_before = Pt(5)
                paragraph.paragraph_format.space_after = Pt(5)
                paragraph.paragraph_format.keep_with_next = i < len(table.rows) - 1
                for run in paragraph.runs:
                    run.bold = i == 0 or is_panel
                    run.font.size = Pt(10)
    return table


def note(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(8)
    paragraph.add_run("Note. ").italic = True
    paragraph.add_run(text)
    for run in paragraph.runs:
        run.font.size = Pt(9)


def terminal_table(title, headers, rows):
    widths = [max(len(str(row[i])) for row in [headers, *rows])
              for i in range(len(headers))]
    lines = [title]
    for row in [headers, *rows]:
        lines.append("  ".join(str(value).ljust(widths[i]) if i == 0
                               else str(value).rjust(widths[i])
                               for i, value in enumerate(row)))
    return "\n".join(lines)


def main():
    timestamp = subprocess.check_output(
        ["date", "+%Y-%m-%d %H:%M:%S %Z"], text=True
    ).strip()
    table2, panel_a, panel_b = load_tables()
    OUT.mkdir(parents=True, exist_ok=True)
    headers2 = ["Period", "N", "Abnormal turnover", "Size (% of OMXSB)",
                "Arbitrage risk", "Analysts"]
    headers_a = ["", "Additions", "Deletions", "Total"]
    doc = document("Table 2. Added securities by period")
    make_table(doc, headers2, table2, [2, 0.8, 3.5, 4, 3.8, 2.9])
    note(doc, TABLE2_NOTE + " N: number of additions with non-missing abnormal "
         "turnover. Each mean uses the available observations for that column. "
         "AD denotes the announcement date.")
    doc.save(OUT / "table_2.docx")

    doc = document("Table A1. Sample selection")
    rows = ["Panel A. Sample selection", *panel_a,
            "Panel B. Events with D by period", *panel_b]
    make_table(doc, headers_a, rows, [10.1, 2.3, 2.3, 2.3],
               panels=(1, len(panel_a) + 2))
    note(doc, "Additions and Deletions count securities added to and removed "
         "from OMXSB; Total is their sum. Panel A reports successive sample "
         "filters. Complete window: non-missing tot in events_car.csv, covering "
         "AD−1 to ED+1; AD and ED denote announcement and effective dates. "
         "Panel B counts events by effective-date period with non-missing D_ny "
         "and split = False; preliminary, fund classification under revision. "
         "Source: output/omxsb_replication_2007/tables/tab_01_sample.csv "
         "(first three rows); output/omxsb_replication_2007/events_car.csv "
         "(complete window); code/claude_checks/rattelser_2026-11-03_resultat/"
         "handelser_rattade.csv (Panel B); authors' calculations.")
    doc.save(OUT / "table_A1.docx")
    report = "\n\n".join([
        terminal_table("Table 2. Added securities by period", headers2, table2),
        terminal_table("Table A1. Panel A", headers_a, panel_a),
        terminal_table("Table A1. Panel B (preliminary)", ["Period", *headers_a[1:]], panel_b),
    ])
    provenance = "\n".join(
        f"SHA256 {path.relative_to(ROOT)}: {hashlib.sha256(path.read_bytes()).hexdigest()}"
        for path in (EVENTS, SAMPLE, CAR)
    )
    log = (f"Run: {timestamp} (from date)\n"
           f"Script created: {Path(__file__).read_text().splitlines()[0]}\n"
           f"{provenance}\n\n{report}\n\n"
           "PASS: requested reference values agree with source calculations.\n"
           "Created: table_2.docx, table_A1.docx\n")
    (OUT / "LOGG.txt").write_text(log, encoding="utf-8")
    print(log)


if __name__ == "__main__":
    main()
