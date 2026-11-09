# Gemensam stil för alla Word-tabeller och figurer. Ingen skattning här: bara formatering.
# Varje tabell- och figurfil i code/output/ har en funktion build(doc) som lägger in sin tabell i ett Word-dokument,
# och skriver en egen .docx när den körs. 99_all_tables.py lägger alla i ett dokument i samma ordning som Greenwood och Sammon.
# Numreringen bestäms bara här (NUM). Byt numret här så följer titlar och hänvisningar med.
from pathlib import Path
import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'tables'
FONT, SIZE = 'Times New Roman', 10

# G&S-ordningen: figur 1, tabell I, figur 2, figur 3, (figur 5), tabell V, VI, VII, VIII
NUM = {'fig_net_buying': 'Figure 1', 'tab_by_year': 'Table 1', 'tab_by_period': 'Table 2', 'fig_by_year': 'Figure 2',
       'fig_scatter': 'Figure 3', 'fig_ownership': 'Figure 4', 'tab_multiplier': 'Table 3', 'tab_controls': 'Table 4',
       'tab_who_buys': 'Table 5', 'tab_msci': 'Table 6', 'tab_mde': 'Table A2', 'tab_fi': 'Table A3'}

PERS = ['2007–2011', '2012–2016', '2017–2021', '2022–2026']      # som i tabell1_lang.csv
PERS_KORT = ['2007–11', '2012–16', '2017–21', '2022–26']         # som i omrakning_resultat.csv och resultat_car.csv

# Bootstrapmetod, ordagrant i noterna
WCR = ('restricted wild cluster bootstrap by review (Rademacher weights if G ≥ 12, Webb six-point weights otherwise; 9,999 draws), '
       'where G is the number of reviews')
WCR_CI = ('95 per cent confidence intervals obtained by inverting the bootstrap test: they contain every value not rejected at the '
          '5 per cent level; ∞ means that no value within 20 standard errors of the estimate is rejected')
PAIRS = ('pairs cluster bootstrap by review (reviews drawn with replacement; 9,999 draws), percentile 95 per cent confidence '
         'intervals')
CR1 = 'standard errors clustered by review and t critical values with G − 1 degrees of freedom (no bootstrap)'
STARS = '* p < 0.10, ** p < 0.05, *** p < 0.01'


def stars(p):
    if p is None or pd.isna(p): return ''
    return '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.10 else ''


def num(x, d=2):
    if x is None or pd.isna(x): return ''
    s = f'{x:.{d}f}'
    if s.lstrip('-').strip('0.') == '': s = s.lstrip('-')   # −0.00 skrivs 0.00
    return s.replace('-', '−')


def ci(lo, hi, d=2):
    if pd.isna(lo) or pd.isna(hi): return ''
    kant = lambda v: ('−∞' if v < 0 else '∞') if abs(v) == float('inf') else num(v, d)
    return f'[{kant(lo)}, {kant(hi)}]'


def one(df, **k):
    """Exakt en rad som matchar, annars stopp (så att en tabell aldrig tyst läser fel rad)."""
    m = df
    for a, b in k.items(): m = m[m[a] == b]
    assert len(m) == 1, (k, len(m))
    return m.iloc[0]


def new_document():
    doc = Document(); s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7); s.top_margin = s.bottom_margin = Cm(2.5); s.left_margin = s.right_margin = Cm(2)
    n = doc.styles['Normal']; n.font.name = FONT; n.font.size = Pt(SIZE); n.font.color.rgb = RGBColor(0, 0, 0)
    n.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    n.paragraph_format.space_after = Pt(0); n.paragraph_format.line_spacing = 1
    doc.core_properties.author = ''
    return doc


def title(doc, key, text):
    c = doc.add_paragraph(); c.paragraph_format.keep_with_next = True; c.paragraph_format.space_after = Pt(8)
    c.add_run(f'{NUM[key]}. ').bold = True; c.add_run(text).bold = True
    if not doc.core_properties.title: doc.core_properties.title = f'{NUM[key]}. {text}'


def subhead(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True; p.add_run(text).bold = True


def _rule(cell, edge):
    b = cell._tc.get_or_add_tcPr().find(qn('w:tcBorders'))
    if b is None: b = OxmlElement('w:tcBorders'); cell._tc.get_or_add_tcPr().append(b)
    line = OxmlElement(f'w:{edge}')
    for k, v in (('val', 'single'), ('sz', '6'), ('color', '000000')): line.set(qn(f'w:{k}'), v)
    b.append(line)


def table(doc, headers, rows, widths, panels=(), ci_rows=(), header_rows=1, group_header=None):
    """rows: lista av listor (en cell per kolumn) eller en sträng (panelrubrik över hela bredden).
    ci_rows: index i rows för intervallrader (mindre text). group_header: [(text, första kolumn, sista kolumn), ...] ovanför headers."""
    extra = 1 if group_header else 0
    t = doc.add_table(rows=1 + extra, cols=len(headers)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    bs = OxmlElement('w:tblBorders')
    for e in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV'):
        l = OxmlElement(f'w:{e}'); l.set(qn('w:val'), 'nil'); bs.append(l)
    t._tbl.tblPr.append(bs)
    if group_header:
        for c in t.rows[0].cells: _rule(c, 'top')
        for txt, a, b in group_header:
            m = t.rows[0].cells[a].merge(t.rows[0].cells[b]); m.text = txt; _rule(m, 'bottom')
    for c, h in zip(t.rows[extra].cells, headers):
        c.text = h; _rule(c, 'bottom')
        if not group_header: _rule(c, 'top')
    panel_idx, ci_idx = set(), set()
    for i, v in enumerate(rows):
        cs = t.add_row().cells; ti = len(t.rows) - 1
        if isinstance(v, str): cs[0].merge(cs[-1]).text = v; panel_idx.add(ti)
        else:
            assert len(v) == len(headers), (v, headers)
            for c, x in zip(cs, v): c.text = x
        if i in ci_rows: ci_idx.add(ti)
    for c in t.rows[-1].cells: _rule(c, 'bottom')
    for i, row in enumerate(t.rows):
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        isp, isci, ishead = i in panel_idx, i in ci_idx, i <= extra
        for j, c in enumerate(row.cells):
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if not isp: c.width = Cm(widths[j])
            for p in c.paragraphs:
                if ishead and i < extra: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else: p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 or isp else WD_ALIGN_PARAGRAPH.RIGHT
                p.paragraph_format.space_before = Pt(0 if isci else 3); p.paragraph_format.space_after = Pt(3 if isci else 0)
                # håll ihop: rubrikrader, panelrubrik med första raden, skattning med sitt intervall. Annars får tabellen brytas.
                p.paragraph_format.keep_with_next = i < len(t.rows) - 1 and (i <= extra or isp or (i + 1) in ci_idx)
                for r in p.runs: r.bold = ishead or isp; r.font.size = Pt(SIZE - 1 if isci else SIZE)
    return t


def note(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
    p.add_run('Note. ').italic = True; p.add_run(text)
    for r in p.runs: r.font.size = Pt(SIZE - 1)


def figure(doc, png, width_cm=16):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(png), width=Cm(width_cm))


def save(doc, stem):
    OUT.mkdir(parents=True, exist_ok=True); path = OUT / f'{stem}.docx'; doc.save(path); print('skrev', path); return path


def run(build, stem):
    """Kör en tabellfil fristående: nytt dokument, build(doc), spara som results/tables/<stem>.docx."""
    doc = new_document(); build(doc); return save(doc, stem)


# ---------- figurer (matplotlib), samma typsnitt som tabellerna. Färger kontrollerade för färgblindhet (dataviz-validatorn).
ADD, DEL, GREY = '#2a78d6', '#eb6834', '#52514e'
THIRD = '#1baf7a'


def fig_setup():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'serif', 'font.serif': [FONT, 'Times', 'DejaVu Serif'], 'font.size': 9,
                         'axes.spines.top': False, 'axes.spines.right': False, 'axes.linewidth': 0.6,
                         'axes.edgecolor': GREY, 'xtick.color': GREY, 'ytick.color': GREY, 'axes.labelcolor': '#0b0b0b',
                         'axes.grid': True, 'axes.grid.axis': 'y', 'grid.color': '#e4e3df', 'grid.linewidth': 0.6,
                         'legend.frameon': False, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})
    return plt


def lowess(x, y, frac=0.8):
    """Lokal linjär regression med tricube-vikter (LOWESS utan robusthetsiterationer), bandbredd frac som G&S figur 1."""
    import numpy as np
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x); r = max(int(np.ceil(frac * n)), 2); out = np.empty(n)
    for i in range(n):
        d = np.abs(x - x[i]); h = np.sort(d)[r - 1] or 1.0; w = np.clip(1 - (d / h) ** 3, 0, None) ** 3
        W = np.sum(w); xm = np.sum(w * x) / W; ym = np.sum(w * y) / W
        b = np.sum(w * (x - xm) * (y - ym)) / max(np.sum(w * (x - xm) ** 2), 1e-12); out[i] = ym + b * (x[i] - xm)
    return out
