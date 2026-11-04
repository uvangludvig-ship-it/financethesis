# Updated: 2026-11-04 17:53:40 CET (from date)
"""Build journal-style Word tables from the thesis CSV sources.

Run with Python and the packages pandas and python-docx installed.
Paths are relative to the repository, independently of the working directory.
Reported values are computed from source data; literals in checks are only
the reference values requested for validation, never table inputs.
"""

from pathlib import Path
import hashlib
from html import escape
import subprocess

import re
import numpy as np
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
        ("With ten closing prices from AD−3 to ED+3", "With price data"),
        ("Price history 100 days before and after ED", "After filter"),
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
    normal.font.size = Pt(10)
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
        run.font.size = Pt(10)


def terminal_table(title, headers, rows):
    widths = [max(len(str(row[i])) for row in [headers, *rows])
              for i in range(len(headers))]
    lines = [title]
    for row in [headers, *rows]:
        lines.append("  ".join(str(value).ljust(widths[i]) if i == 0
                               else str(value).rjust(widths[i])
                               for i, value in enumerate(row)))
    return "\n".join(lines)


MEMBERS = ROOT / 'code/claude_checks/data/medlemskap_verifierad.csv'
PANEL = ROOT / 'runda2_indata/panel_full.csv.gz'
DATA = ROOT / 'code/claude_checks/data'
INDEX = ROOT / 'data/raw/lseg/panel_2005_2026/indices_daily (1).csv'
METRICS = ('mcap_pre', 'k_storlek', 'k_oms', 'volatility', 'k_ana', 'pre100')


def member_observations(events):
    """Reproduce runda3/runda11 panel and measurement rules without executing them.

    Membership is the verified post-review snapshot. Size denominators follow
    runda11: previous snapshot, or current snapshot for the first review.
    Missing observations remain missing; no event-only proxy for membership.
    """
    cols = ['ric', 'date', 'close', 'totret', 'volume', 'mcap', 'shares']
    px = pd.read_csv(PANEL, usecols=cols, parse_dates=['date'])
    px = px[px.ric.str.contains(r'\.ST')]
    extra = pd.read_csv(DATA / 'lseg_saknade_aktier.csv')
    for ric in ['NDASE.ST', 'TIETOS.ST']:
        d = extra[(extra.ric == ric) & extra.Date.notna()].copy()
        d['date'] = pd.to_datetime(d.Date)
        m = extra[(extra.ric == ric) & (extra.typ == 'marknadsvarde_manad')].copy()
        m['date'] = pd.date_range('2006-01-31', periods=len(m), freq='ME')
        d = d.merge(m[['date', 'Outstanding Shares']].rename(columns={'Outstanding Shares': 'shares'}), on='date', how='outer').sort_values('date')
        d['shares'] = d.shares.ffill()
        d = d[d.TRDPRC_1.notna()]
        new = pd.DataFrame(dict(ric=ric, date=d.date, close=d.TRDPRC_1,
                               totret=np.nan, volume=d.ACVOL_UNS,
                               mcap=d.TRDPRC_1 * d.shares, shares=d.shares))
        px = pd.concat([px[px.ric != ric], new], ignore_index=True)
    ix = pd.read_csv(INDEX, parse_dates=['date'])
    market = ix[ix.ric.eq('.OMXSBGI')].set_index('date')['close'].dropna().sort_index()
    cal = pd.DatetimeIndex(market.index.unique())
    market = market.reindex(cal).pct_change(fill_method=None) * 100
    px = px[px.date.isin(cal)].drop_duplicates(['ric', 'date'], keep='last').sort_values(['ric', 'date'])
    def pivot(col):
        return px.pivot_table(index='date', columns='ric', values=col).reindex(cal)
    close, mc, sh = pivot('close'), pivot('mcap').ffill(limit=10), pivot('shares')
    tv = pivot('volume') * close
    returns = {}
    for ric, g in px.groupby('ric'):
        g = g.set_index('date')
        returns[ric] = g.totret.fillna(g.close.ffill().pct_change(fill_method=None) * 100)
    ret = pd.DataFrame(returns).reindex(cal)
    ret = ret.mask(ret > 1000)
    def root(ric):
        match = re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST', ric)
        return match.group(1) if match else ric
    families = {}
    for ric in close:
        families.setdefault(root(ric), []).append(ric)
    def has_price(c, i):
        return c in close and close[c].iloc[max(i-5, 0):i+1].notna().any()
    def shares(c, i):
        if c not in sh:
            return np.nan
        v = sh[c].iloc[max(i-60, 0):i+1].dropna()
        return v.iloc[-1] if len(v) and v.iloc[-1] > 0 else np.nan
    def value(c, i):
        if c not in mc or not has_price(c, i):
            return np.nan
        v = mc[c].iloc[i]
        if not v > 0:
            return np.nan
        siblings = [r for r in families[root(c)] if has_price(r, i)]
        if len(siblings) == 1:
            return v
        ns = [shares(r, i) for r in siblings]
        return v * shares(c, i) / sum(ns) if all(n > 0 for n in ns) else np.nan
    classification = pd.read_csv(DATA / 'lseg_klassificering.csv').set_index('ric').marknad.to_dict()
    main = [c for c in tv if classification.get(c) not in ('SSME', 'ONSE')]
    denominator = mc[[c for c in main if c in mc]].T.groupby(root).max().T.sum(axis=1, min_count=1)
    market_turn = tv[main].sum(axis=1, min_count=1) / denominator * 100
    analysts = pd.read_csv(DATA / 'runda8_analytiker.csv.gz', low_memory=False)
    field = next(c for c in analysts if 'Number of Included Estimates' in c)
    analysts['month'] = pd.to_datetime(analysts.Date, errors='coerce').dt.to_period('M')
    covered = set(analysts.loc[analysts[field].notna(), 'Instrument'])
    forecasts = analysts.dropna(subset=['month']).groupby(['Instrument', 'month'])[field].max()
    membership = pd.read_csv(MEMBERS)
    members = {r: set(g.loc[g.status.eq('medlem'), 'ric']) for r, g in membership.groupby('review_after')}
    reviews = events.groupby('review').agg(AD=('AD', 'first'), ED=('ED', 'first'), per=('per', 'first')).sort_values('AD')
    rows = []
    prior = None
    for review, r in reviews.iterrows():
        i = cal.get_loc(pd.Timestamp(r.AD))
        total = np.nansum([value(c, i-1) for c in members[prior or review]])
        for c in sorted(members[review]):
            v = value(c, i-1)
            row = dict(review=review, ric=c, per=r.per, mcap_pre=mc[c].iloc[i-1] if c in mc else np.nan,
                       k_storlek=100*v/total if v > 0 and total > 0 else np.nan,
                       k_oms=np.nan, k_wz=np.nan, k_ana=np.nan, pre100=np.nan)
            if v > 0 and c in tv:
                fraction = v / mc[c].iloc[i-1]
                t = tv[c].iloc[i-21:i] / (mc[c].iloc[i-21:i]*fraction) * 100
                m = market_turn.iloc[i-21:i]
                ok = t.notna() & m.notna()
                if ok.sum() >= 10:
                    row['k_oms'] = float((t[ok]-m[ok]).mean())
            if c in ret:
                y, x = ret[c].iloc[i-250:i-1], market.iloc[i-250:i-1]
                ok = y.notna() & x.notna()
                if ok.sum() >= 100:
                    fit = np.polyfit(x[ok], y[ok], 1)
                    row['k_wz'] = np.var(y[ok]-np.polyval(fit, x[ok]), ddof=2)
                pre = (ret[c]-market).iloc[i-100:i]
                if len(pre) == 100 and pre.notna().all():
                    row['pre100'] = pre.sum()
            if c in covered:
                n = forecasts.get((c, pd.Period(r.AD, 'M')-1), np.nan)
                row['k_ana'] = 0.0 if pd.isna(n) else n
            rows.append(row)
        prior = review
    result = pd.DataFrame(rows)
    assert not result.duplicated(['review', 'ric']).any()
    # Validate reconstructed measures against overlapping event observations.
    overlap = result.merge(events, left_on=['review', 'ric'], right_on=['review', 'RIC'], suffixes=('_c', '_e'))
    for col in ['k_storlek', 'k_oms', 'k_wz', 'k_ana', 'pre100']:
        ok = overlap[[col+'_c', col+'_e']].notna().all(axis=1)
        if not np.allclose(overlap.loc[ok, col+'_c'], overlap.loc[ok, col+'_e'], rtol=1e-6, atol=1e-8):
            raise ValueError(f'Panel C reproduction mismatch: {col}')
    print('Panel C: reproduced measures agree for overlapping event observations.')
    return result


def descriptive_rows(frame):
    frame = frame.copy()
    frame['mcap_pre'] /= 1e9
    if (frame.k_wz.dropna() < 0).any():
        raise ValueError('Negative residual variance')
    frame['volatility'] = np.sqrt(frame.k_wz)
    rows = []
    for period in PERIODS:
        g = frame[frame.per.eq(period)]
        row = [period, str(g.k_storlek.count())]
        for col in METRICS:
            values = [g[col].mean(), g[col].median()]
            row.append('\n'.join('' if pd.isna(v) else decimal(v, (0 if v >= 10 else 1) if col == 'mcap_pre' else (1 if col == 'k_ana' else 2)) for v in values))
        rows.append(row)
    return rows


def copyable_html(doc, path):
    """Export actual table text as HTML, suitable for rich-text paste into Word."""
    table = doc.tables[0]
    title = escape(doc.paragraphs[0].text)
    notes = ''.join('<p>' + escape(p.text) + '</p>' for p in doc.paragraphs[1:] if p.text)
    rows = []
    for i, row in enumerate(table.rows):
        unique = []
        for cell in row.cells:
            if not any(cell._tc is previous._tc for previous in unique):
                unique.append(cell)
        panel = len(unique) == 1
        cells = []
        for j, cell in enumerate(unique):
            tag = 'th' if i == 0 or panel else 'td'
            borders = ('border-top:0.75pt solid black;border-bottom:0.75pt solid black;' if i == 0
                       else 'border-bottom:0.75pt solid black;' if i == len(table.rows)-1 else '')
            align = 'left' if j == 0 or panel else 'right'
            span = f' colspan="{len(row.cells)}"' if panel else ''
            content = escape(cell.text).replace('\n', '<br>')
            cells.append(f'<{tag}{span} style="padding:4pt 6pt;text-align:{align};vertical-align:middle;{borders}">{content}</{tag}>')
        rows.append('<tr>' + ''.join(cells) + '</tr>')
    fragment = (f'<div style="font-family:Times New Roman,serif;font-size:10pt;color:black">'
                f'<p><b>{title}</b></p><table style="border-collapse:collapse;width:100%;font-family:Times New Roman,serif;font-size:10pt">'
                + ''.join(rows) + '</table>' + notes + '</div>')
    page = '''<!doctype html><html lang="sv"><meta charset="utf-8">
<title>Tabell att kopiera till Word</title>
<style>body{max-width:1200px;margin:32px auto;padding:0 24px;background:white;color:black}
.tools{font:16px system-ui;margin-bottom:28px;padding:16px;background:#f1f4f6}
button{font:inherit;padding:9px 16px;cursor:pointer} #status{margin-left:14px}
@media print{.tools{display:none}}</style>
<div class="tools"><button id="copy">Kopiera tabellen till Word</button><span id="status" role="status"></span>
<p>Klicka på knappen och klistra in i ditt Word-dokument med ⌘V.
Välj <b>Behåll källformatering</b> om Word frågar. Tabell 2 passar på en liggande sida.</p></div>
<main id="content">''' + fragment + '''</main>
<script>
document.getElementById('copy').onclick = () => {
  const el = document.getElementById('content');
  const range = document.createRange(); range.selectNodeContents(el);
  const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
  let copied = false;
  try { copied = document.execCommand('copy'); } catch (_) {}
  document.getElementById('status').textContent = copied
    ? 'Kopierad. Klistra in i Word med ⌘V.'
    : 'Tabellen är markerad. Tryck ⌘C och sedan ⌘V i Word.';
};
</script></html>'''
    path.write_text(page, encoding='utf-8')


def main():
    timestamp = subprocess.check_output(['date', '+%Y-%m-%d %H:%M:%S %Z'], text=True).strip()
    _, panel_a, panel_b = load_tables()
    assert panel_a[-1][1:] == ['256', '225', '481']
    assert [r[1] for r in panel_b] == ['6', '27', '58', '78']
    events = pd.read_csv(EVENTS)
    check = events[events.type.eq('addition') & events.per.eq(PERIODS[0])]
    assert check.k_storlek.count() == 36
    members = member_observations(events)
    panels = [descriptive_rows(events[events.type.eq(ty)]) for ty in ('addition', 'deletion')]
    panels.append(descriptive_rows(members))
    OUT.mkdir(parents=True, exist_ok=True)
    headers = ['Period', 'N', 'Market value,\nSEK bn', 'Size, %\nof OMXSB', 'Turnover\nvs market', 'Residual volatility,\n% per day', 'Analysts', 'Run-up, %\nAD−100 to AD−1']
    doc = document('Table 2. Securities added to and deleted from OMXSB, by period')
    section = doc.sections[0]
    from docx.enum.section import WD_ORIENT
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width, section.page_height = Cm(29.7), Cm(21)
    section.top_margin = section.bottom_margin = Cm(1.2)
    labels = ['Panel A. Additions', 'Panel B. Deletions', 'Panel C. OMXSB members at the review']
    rows = []
    panel_positions = []
    for label, data in zip(labels, panels):
        panel_positions.append(len(rows)+1)
        rows.extend([label, *data])
    table = make_table(doc, headers, rows, [1.8, 1.0, 3.0, 3.2, 3.2, 4.8, 2.5, 6.2], panels=panel_positions)
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
    note(doc, 'Each cell reports the mean above the median, using available observations. N counts observations with size (k_storlek). Period follows per in the event source. AD is the announcement date; ED is the effective date. Market value: mcap_pre in SEK billion, measured before AD; this source field is company market value, whereas Size uses share-class value at AD−1 as a percentage of pre-review OMXSB value. Turnover: mean daily SEK turnover divided by share-class value over the 21 trading days before AD, less the value-weighted main-list mean, in percentage points. Residual volatility: square root of residual variance from daily percentage returns on OMXSBGI over AD−250 to AD−2 (at least 100 observations; Wurgler and Zhuravskaya, 2002), in percent per day. Analysts: FY1 EPS forecast count in the month before AD. Run-up: summed daily excess returns over OMXSBGI over AD−100 to AD−1, in percent. Panel C uses verified post-review members (status medlem), once per member and review, measured relative to that review’s AD; blank cells denote unavailable data. Source: Nasdaq, LSEG; authors’ calculations.')
    doc.save(OUT / 'table_2.docx')
    copyable_html(doc, OUT / 'table_2_kopiera.html')
    doc = document('Table A1. Sample construction')
    a_headers = ['', 'Additions', 'Deletions', 'Total']
    make_table(doc, a_headers, ['Panel A. Sample construction', *panel_a, 'Panel B. Events with D by period', *panel_b], [10.1, 2.3, 2.3, 2.3], panels=(1, 6))
    note(doc, "Additions and Deletions count securities added to and removed from OMXSB; Total is their sum. AD and ED denote announcement and effective dates. Panel A uses tab_01_sample.csv for the first three filters and non-missing tot in events_car.csv for the complete window. Panel B counts events with non-missing D_ny and split = False by period (per) in handelser_rattade.csv. D is index funds’ net buying between the report before AD and after ED, as a percentage of the share class’s shares. Panel B rests on the fund classification in data/input/omxsb/tracker_mandates.csv and is rerun when that file is final. Source: Nasdaq, LSEG; authors’ calculations.")
    doc.save(OUT / 'table_A1.docx')
    copyable_html(doc, OUT / 'table_A1_kopiera.html')
    reports = []
    for label, rows in zip(labels, panels):
        reports.append(terminal_table(label + ' (mean / median)', [h.replace('\n', ' ') for h in headers], [[v.replace('\n', ' / ') for v in row] for row in rows]))
    reports.extend([terminal_table('A1 Panel A', a_headers, panel_a), terminal_table('A1 Panel B', ['Period', *a_headers[1:]], panel_b)])
    sources = [EVENTS, SAMPLE, CAR, MEMBERS, PANEL, INDEX, DATA/'lseg_saknade_aktier.csv', DATA/'lseg_klassificering.csv', DATA/'runda8_analytiker.csv.gz']
    log = f'Run: {timestamp} (date)\n{Path(__file__).read_text().splitlines()[0]}\n'
    log += 'Units: declaration specifies residual variance; runda3.py constructs returns in percent and runda11.py takes residual variance (ddof=2). sqrt(k_wz) applied observation by observation before aggregation, yielding % per day. Raw variance check remains 6.0.\n'
    log += 'Panel C: status medlem = verified; uncertain/missing statuses excluded; post-review members, prior-review size denominator (current for first review), same panel and missing-data rules as runda11.\n'
    log += 'PASS: reference values; Panel C overlapping measures reproduced.\n'
    log += 'Copyable HTML companions generated from the same editable Word table cells. DOCX files have no document protection or table images.\n'
    log += '\n'.join(f'SHA256 {p.relative_to(ROOT)}: {hashlib.sha256(p.read_bytes()).hexdigest()}' for p in sources)
    log += '\n\n' + '\n\n'.join(reports) + '\n\nPanel C non-missing counts:\n' + members.groupby('per')[['mcap_pre', 'k_storlek', 'k_oms', 'k_wz', 'k_ana', 'pre100']].count().to_string() + '\n'
    log = '\n'.join(line.rstrip() for line in log.splitlines()) + '\n'
    (OUT/'LOGG.txt').write_text(log)
    print(log)


if __name__ == '__main__':
    main()
