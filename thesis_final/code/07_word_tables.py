# Effekttabellen (G&S Table I för OMXSB) i Word, ur tabell1_resultat/tabell1_lang.csv.
# Inga nya skattningar: varje siffra läses ur tabell1.py:s utfil (3 nov 2026, 20:12). Panel A och B = G&S Table I;
# panel C = decennierna (G&S indelning) med skillnaden från panel D. Noten är ett utkast för författarna.
# Körs från thesis_final efter 01: python3 code/07_word_tables.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import sys, hashlib
from pathlib import Path
import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else RES / 'effect' / 'tabell1_lang.csv'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else RES / 'tables' / 'table_effect.docx'
T = pd.read_csv(SRC)
PERS = ['2007–2011', '2012–2016', '2017–2021', '2022–2026']
HEAD = ['', '2007–11', '2012–16', '2017–21', '2022–26']
WIN = [('ann', 'Announcement [AD−1, AD+1]'), ('eff', 'Effective [ED−1, ED+1]'), ('tot', 'Total [AD−1, ED+1]')]

def stars(p):
    return '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.10 else ''
def num(x, d=2):
    s = f'{x:.{d}f}'
    return s.replace('-', '−')
def cell(r):
    return f'{num(r.b)}{stars(r.p_wcb)}', f'[{num(r.lo)}, {num(r.hi)}]'
def get(panel, typ, win, urval):
    q = T[(T.panel == panel) & (T.typ == typ) & (T['fönster'] == win) & (T.urval == urval)]
    assert len(q) == 1, (panel, typ, win, urval, len(q))
    return q.iloc[0]

rows, panels = [], []
for lab, typ in [('Panel A. Additions', 'addition'), ('Panel B. Deletions', 'deletion')]:
    panels.append(len(rows) + 1); rows.append(lab)
    for w, wl in WIN:
        rs = [get('A/B', typ, w, p) for p in PERS]
        rows.append([wl] + [cell(r)[0] for r in rs]); rows.append([''] + [cell(r)[1] for r in rs])
    tot = [get('A/B', typ, 'tot', p) for p in PERS]
    rows.append(['Events'] + [str(int(r.n)) for r in tot])
    rows.append(['Reviews'] + [str(int(r.G)) for r in tot])
# kontroller mot TABELL1.md (3 nov)
assert [int(get('A/B', 'addition', 'tot', p).n) for p in PERS] == [33, 54, 82, 87]
assert [int(get('A/B', 'deletion', 'tot', p).n) for p in PERS] == [38, 47, 63, 77]
assert num(get('A/B', 'addition', 'tot', '2007–2011').b) == '8.52'

rowsC = []
for lab, typ in [('Additions', 'addition'), ('Deletions', 'deletion')]:
    a, b = get('C', typ, 'tot', '2007–16'), get('C', typ, 'tot', '2017–26')
    d = get('D', typ, 'tot', '2017–26 minus 2007–16 (decennier)')
    rowsC.append([lab, cell(a)[0], cell(b)[0], cell(d)[0]]); rowsC.append(['', cell(a)[1], cell(b)[1], cell(d)[1]])
    rowsC.append(['Events', str(int(a.n)), str(int(b.n)), ''])

def document(title):
    doc = Document(); s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7); s.top_margin = s.bottom_margin = Cm(2.5); s.left_margin = s.right_margin = Cm(2)
    n = doc.styles['Normal']; n.font.name = 'Times New Roman'; n.font.size = Pt(10); n.font.color.rgb = RGBColor(0, 0, 0)
    n.paragraph_format.space_after = Pt(0); n.paragraph_format.line_spacing = 1
    c = doc.add_paragraph(); c.paragraph_format.keep_with_next = True; c.paragraph_format.space_after = Pt(8); c.add_run(title).bold = True
    doc.core_properties.author = ''; doc.core_properties.title = title
    return doc
def rule(cell, edge):
    b = cell._tc.get_or_add_tcPr().find(qn('w:tcBorders'))
    if b is None: b = OxmlElement('w:tcBorders'); cell._tc.get_or_add_tcPr().append(b)
    line = OxmlElement(f'w:{edge}')
    for k, v in (('val', 'single'), ('sz', '6'), ('color', '000000')): line.set(qn(f'w:{k}'), v)
    b.append(line)
def make_table(doc, headers, rows, widths, panels=(), ci_rows=()):
    t = doc.add_table(rows=1, cols=len(headers)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for col, w in zip(t.columns, widths): col.width = Cm(w)
    bs = OxmlElement('w:tblBorders')
    for e in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV'):
        l = OxmlElement(f'w:{e}'); l.set(qn('w:val'), 'nil'); bs.append(l)
    t._tbl.tblPr.append(bs)
    for c, h in zip(t.rows[0].cells, headers): c.text = h; rule(c, 'top'); rule(c, 'bottom')
    for v in rows:
        cs = t.add_row().cells
        if isinstance(v, str): cs[0].merge(cs[-1]).text = v
        else:
            for c, x in zip(cs, v): c.text = x
    for c in t.rows[-1].cells: rule(c, 'bottom')
    for i, row in enumerate(t.rows):
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit')); isp = i in panels; isci = i in ci_rows
        for j, c in enumerate(row.cells):
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if not isp: c.width = Cm(widths[j])
            for p in c.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 or isp else WD_ALIGN_PARAGRAPH.RIGHT
                p.paragraph_format.space_before = Pt(0 if isci else 4); p.paragraph_format.space_after = Pt(4 if isci else 0)
                p.paragraph_format.keep_with_next = i < len(t.rows) - 1
                for r in p.runs:
                    r.bold = i == 0 or isp; r.font.size = Pt(9 if isci else 10)
    return t
def note(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8)
    p.add_run('Note. ').italic = True; p.add_run(text)
    for r in p.runs: r.font.size = Pt(9)

doc = document('Table 2. Abnormal returns around OMXSB additions and deletions, 2007–2026')
ci = [i + 1 for i, r in enumerate(rows) if not isinstance(r, str) and r[0] == '']
make_table(doc, HEAD, rows, [5.4, 2.7, 2.7, 2.7, 2.7], panels=panels, ci_rows=ci)
doc.add_paragraph().paragraph_format.space_after = Pt(6)
p = doc.add_paragraph(); p.add_run('Panel C. Total window [AD−1, ED+1], by decade').bold = True; p.paragraph_format.space_after = Pt(4)
ciC = [i + 1 for i, r in enumerate(rowsC) if r[0] == '']
make_table(doc, ['', '2007–16', '2017–26', 'Difference'], rowsC, [5.4, 3.6, 3.6, 3.6], ci_rows=ciC)
note(doc, 'DRAFT, to be rewritten by the authors. Cumulative abnormal return in per cent: the stock\'s total return minus the '
     'return on the OMX Stockholm Benchmark Gross Index (.OMXSBGI), summed over the window. AD is the announcement date and ED '
     'the effective date. Each cell gives the mean across events; 95 per cent confidence intervals in brackets, from standard errors '
     'clustered by review and t critical values with G − 1 degrees of freedom, where G is the number of reviews. Stars from a '
     'restricted wild cluster bootstrap by review (Rademacher weights if G ≥ 12, Webb six-point weights otherwise; 9,999 draws): '
     '* p < 0.10, ** p < 0.05, *** p < 0.01. Deletions keep their sign. Events are counted for the total window; the announcement '
     'and effective windows include up to three more events per period. Difference in Panel C: 2017–26 minus 2007–16, same '
     'inference. Sample: 481 changes in 39 semi-annual reviews with effective dates from 2 July 2007 to 1 June 2026 (Table A1).')
OUT.parent.mkdir(parents=True, exist_ok=True); doc.save(OUT)
print('skrev', OUT, 'från', SRC, 'sha256', hashlib.sha256(SRC.read_bytes()).hexdigest()[:16])
for r in rows: print(r if isinstance(r, str) else '  '.join(f'{x:>16}' for x in r))
for r in rowsC: print('  '.join(f'{x:>16}' for x in r))

# ---------- år för år (G&S Table I): medel per år ur Luddes tab_00_by_year.csv, periodrader med stjärnor ur tabell1
BY = Path(sys.argv[3]) if len(sys.argv) > 3 else DATA / 'comparison' / 'replication_effect_by_year.csv'
Y = pd.read_csv(BY, header=[0, 1], index_col=0)
Y.columns = [f'{a}_{b}' for a, b in Y.columns]
yrs = [i for i in Y.index if str(i).isdigit()]
# kontroll: N-viktat medel per period ur årsraderna = tabell1:s totala fönster
for typ, pre in [('addition', 'Additions'), ('deletion', 'Deletions')]:
    for p in PERS:
        a, b = int(p[:4]), int(p[-4:]); q = Y.loc[[y for y in yrs if a <= int(y) <= b]]
        m = (q[f'{pre}_N'] * q[f'{pre}_Total']).sum() / q[f'{pre}_N'].sum()
        assert abs(m - get('A/B', typ, 'tot', p).b) < 1e-6, (typ, p, m)
        assert int(q[f'{pre}_N'].sum()) == int(get('A/B', typ, 'tot', p).n)
rowsY = []
for y in yrs:
    r = Y.loc[y]; rowsY.append([str(y)] + [str(int(r[f'{pre}_N'])) if c == 'N' else num(r[f'{pre}_{c}']) for pre in ['Additions', 'Deletions'] for c in ['N', 'Ann', 'Eff', 'Total']])
panY = [len(rowsY) + 1]; rowsY.append('Period means')
for p in PERS:
    rr = [p[:4] + '–' + p[-2:]]
    for typ in ['addition', 'deletion']:
        rr.append(str(int(get('A/B', typ, 'tot', p).n)))
        for w in ['ann', 'eff', 'tot']: rr.append(cell(get('A/B', typ, w, p))[0])
    rowsY.append(rr)
for p in ['2007–16', '2017–26']:
    a, d = get('C', 'addition', 'tot', p), get('C', 'deletion', 'tot', p)
    rowsY.append([p, str(int(a.n)), '', '', cell(a)[0], str(int(d.n)), '', '', cell(d)[0]])
doc2 = document('Table 2. Abnormal returns around OMXSB additions and deletions, by year, 2007–2026')
rowsY = [['Year', 'N', 'Ann.', 'Eff.', 'Total', 'N', 'Ann.', 'Eff.', 'Total']] + rowsY
panY = [i + 1 for i in panY]
t = make_table(doc2, ['', 'Additions', '', '', '', 'Deletions', '', '', ''], rowsY, [1.9] + [1.9] * 8, panels=panY)
for a, b in [(1, 4), (5, 8)]:
    m = t.rows[0].cells[a].merge(t.rows[0].cells[b]); m.text = 'Additions' if a == 1 else 'Deletions'
    for p in m.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: r.bold = True; r.font.size = Pt(10)
for c in t.rows[1].cells:
    rule(c, 'bottom')
    for p in c.paragraphs:
        for r in p.runs: r.bold = True
note(doc2, 'DRAFT, to be rewritten by the authors. Columns 2–5: additions; columns 6–9: deletions. Mean cumulative abnormal '
     'return in per cent (stock total return minus .OMXSBGI) by year of the effective date. Ann.: [AD−1, AD+1]; Eff.: [ED−1, ED+1]; '
     'Total: [AD−1, ED+1]. N counts events with a complete total window. Each year has at most two reviews, so yearly means carry '
     'no standard errors. Period rows: same means pooled over five-year periods and decades, with stars from a restricted wild '
     'cluster bootstrap by review (* p < 0.10, ** p < 0.05, *** p < 0.01); confidence intervals in Table 3. 2007 contains only '
     'the July and December 2007 reviews, 2026 only the June review.')
OUT2 = OUT.with_name('table_effect_by_year.docx'); doc2.save(OUT2); print('skrev', OUT2)
