#!/usr/bin/env python3
"""Build the editable final Word document from the authoritative LaTeX sources.
Run with the Codex bundled Python. Unknown commands/unequal table rows fail loudly.
"""
from pathlib import Path
import re, subprocess, json, hashlib, shutil, unicodedata, argparse, os
from copy import deepcopy
from functools import lru_cache
from zipfile import ZipFile
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'manuscript'; TMP=ROOT/'tmp/word_build'; TMP.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'final/The_Index_Effect_in_Sweden.docx'; OUT.parent.mkdir(exist_ok=True)
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--template',type=Path,default=ROOT.parent/'tmp/thesis_draft_20261112/source/reference/course_context/source_materials/front_page.docx',help='Path to official SSE front_page.docx (not redistributed with this package)')
ap.add_argument('--pdftoppm',type=Path,default=None)
ap.add_argument('--pdflatex',type=Path,default=None)
args=ap.parse_args()
TEMPLATE=args.template
if not TEMPLATE.exists():ap.error('Supply the official cover template with --template PATH')
POP=Path('/Users/ludviguvang/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm')
PDFLATEX=args.pdflatex or Path(shutil.which('pdflatex') or '/Library/TeX/texbin/pdflatex')
if args.pdftoppm:POP=args.pdftoppm
elif not POP.exists():POP=Path(shutil.which('pdftoppm') or 'pdftoppm')
aux=(SRC/'main.aux').read_text()
LABELS=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}',aux))
bbl=(SRC/'main.bbl').read_text()
BIB={}; REFS=[]
for m in re.finditer(r'\\bibitem\[(.*?)\]\{([^}]+)\}\s*(.*?)(?=\\bibitem|\\end\{thebibliography\})',bbl,re.S):
    BIB[m[2]]=m[1]; REFS.append((m[2],m[3]))
COUNTS={'paragraphs':0,'tables':0,'figures':0,'equations':0,'footnotes':0,'references':len(REFS)}
SOURCE_PARAGRAPHS=[]

def brace(s,pos,op='{',cl='}'):
    while pos<len(s) and s[pos].isspace():pos+=1
    if pos>=len(s) or s[pos]!=op:raise ValueError('Expected '+op+' at '+s[max(0,pos-25):pos+40])
    depth=1; i=pos+1
    while i<len(s):
        if s[i]=='\\':i+=2;continue
        if s[i]==op:depth+=1
        elif s[i]==cl:
            depth-=1
            if not depth:return s[pos+1:i],i+1
        i+=1
    raise ValueError('Unbalanced group '+s[pos:pos+80])

def command(s,i):
    m=re.match(r'\\([A-Za-z]+\*?|.)',s[i:]);return m[1],i+len(m[0])

def strip_comments(s):return re.sub(r'(?<!\\)%[^\n]*','',s)
def cleanbasic(s):
    s=s.replace('~',' ').replace('---','—').replace('--','–').replace('``','“').replace("''",'”')
    return re.sub(r'\s+',' ',s)

SYMBOLS={'mu':'μ','Delta':'Δ','pm':'±','sum':'∑','alpha':'α','beta':'β','varepsilon':'ε','in':'∈','leq':'≤','approx':'≈','qquad':'  ','left':'','right':''}
def math_nodes(s):
    """Small native OMML parser for all inline math used in this manuscript."""
    def mr(txt):
        e=OxmlElement('m:r');t=OxmlElement('m:t');t.text=txt;t.set(qn('xml:space'),'preserve');e.append(t);return e
    def atom(i):
        if s[i]=='{':
            a,j=brace(s,i);return math_nodes(a),j
        if s[i]=='\\':
            c,j=command(s,i)
            while j<len(s) and s[j].isspace():j+=1
            if c in ('widehat','overline','bar'):
                a,j=atom(j);e=OxmlElement('m:acc');pr=OxmlElement('m:accPr');ch=OxmlElement('m:chr');ch.set(qn('m:val'),'̂' if c=='widehat' else '̅');pr.append(ch);e.append(pr);v=OxmlElement('m:e');v.extend(a);e.append(v);return[e],j
            if c in ('mathbf','boldsymbol','mathrm','text'):return atom(j)
            if c=='frac':
                a,j=atom(j);b,j=atom(j);e=OxmlElement('m:f');n=OxmlElement('m:num');n.extend(a);d=OxmlElement('m:den');d.extend(b);e.extend([n,d]);return[e],j
            if c in SYMBOLS:return[mr(SYMBOLS[c])],j
            raise ValueError('Unsupported math command '+c)
        return[mr(s[i])],i+1
    out=[];i=0
    while i<len(s):
        if s[i].isspace():i+=1;continue
        a,i=atom(i)
        while i<len(s) and s[i] in '_^':
            kind=s[i];b,i=atom(i+1);e=OxmlElement('m:sSub' if kind=='_' else 'm:sSup');base=OxmlElement('m:e');base.extend(a);sub=OxmlElement('m:sub' if kind=='_' else 'm:sup');sub.extend(b);e.extend([base,sub]);a=[e]
        out.extend(a)
    merged=[]
    for e in out:
        if merged and e.tag==qn('m:r') and merged[-1].tag==qn('m:r'):
            merged[-1].find(qn('m:t')).text=(merged[-1].find(qn('m:t')).text or '')+(e.find(qn('m:t')).text or '')
        else:merged.append(e)
    return merged

def citation(keys,kind):
    vals=[]
    for key in keys.split(','):
        if key.strip() not in BIB:raise ValueError('Citation absent from bibliography: '+key)
        label=plain(BIB[key.strip()]);author,year=label.rsplit(', ',1)
        vals.append(author+' ('+year+')' if kind=='citet' else author+', '+year)
    return '; '.join(vals) if kind=='citet' else '('+'; '.join(vals)+')'

def inline(p,s,bold=False,italic=False,size=None,footnotes=None):
    s=cleanbasic(s);i=0;buf=''
    def add(txt):
        if not txt:return
        r=p.add_run(txt);r.bold=bold;r.italic=italic
        if size:r.font.size=Pt(size)
        r.font.color.rgb=RGBColor(0,0,0)
    def flush():
        nonlocal buf
        add(buf);buf=''
    while i<len(s):
        c=s[i]
        if c=='$':
            flush();j=i+1
            while j<len(s) and s[j]!='$':j+=1
            if j==len(s):raise ValueError('Unterminated math '+s)
            om=OxmlElement('m:oMath');om.extend(math_nodes(s[i+1:j]))
            if size:
                for mr in om.iter(qn('m:r')):
                    rp=OxmlElement('w:rPr');sz=OxmlElement('w:sz');sz.set(qn('w:val'),str(int(size*2)));rp.append(sz);mr.insert(0,rp)
            p._p.append(om);i=j+1;continue
        if c in '{}':i+=1;continue
        if c!='\\':buf+=c;i+=1;continue
        cmd,j=command(s,i)
        if cmd in ('%','&','_','#','$','{','}'):
            buf+=cmd;i=j;continue
        if cmd in ('textquotesingle',):buf+="'";i=j;continue
        if cmd in ('O','o','aa','AA','ae','AE','ss'):buf+={'O':'Ø','o':'ø','aa':'å','AA':'Å','ae':'æ','AE':'Æ','ss':'ß'}[cmd];i=j;continue
        if cmd in (',',';',':',' '):buf+=' ';i=j;continue
        if cmd in ('newblock','par'):buf+=' ';i=j;continue
        if cmd in ('em','bfseries','itshape','normalfont'):flush();italic=cmd=='em' or cmd=='itshape';bold=cmd=='bfseries';i=j;continue
        if cmd in ('"',"'",'`','^','~'):
            if s[j]=='{':a,j=brace(s,j)
            else:a=s[j];j+=1
            accent={'"':'\u0308',"'":'\u0301','`':'\u0300','^':'\u0302','~':'\u0303'}[cmd]
            buf+=unicodedata.normalize('NFC',a+accent);i=j;continue
        if cmd in ('textbf','emph','textit','texttt','textrm','url'):
            flush();a,j=brace(s,j);inline(p,a,bold=bold or cmd=='textbf',italic=italic or cmd in ('emph','textit'),size=size,footnotes=footnotes);i=j;continue
        if cmd in ('citep','citet'):
            a,j=brace(s,j);buf+=citation(a,cmd);i=j;continue
        if cmd in ('ref','eqref'):
            a,j=brace(s,j)
            if a not in LABELS:raise ValueError('Missing cross-reference '+a+'; compile LaTeX first')
            val=LABELS[a];buf+=('('+val+')') if cmd=='eqref' else val;i=j;continue
        if cmd=='label':a,i=brace(s,j);continue
        if cmd=='footnote':
            flush();a,j=brace(s,j);COUNTS['footnotes']+=1;num=COUNTS['footnotes'];r=p.add_run(str(num));r.font.superscript=True
            if footnotes is None:raise ValueError('Footnote outside body')
            footnotes.append((num,a));i=j;continue
        raise ValueError('Unsupported text command \\'+cmd+' near '+s[max(0,i-50):i+80])
    flush()

@lru_cache(maxsize=4096)
def plain(s):
    p=Document().add_paragraph();inline(p,s)
    # For table-width measurement, native math text is included.
    return ''.join(p._p.itertext()) if not p.text else p.text

DOC=Document(TEMPLATE)
# Adapt copied official cover in its own anchored components.
for pnode in DOC._element.xpath('.//w:txbxContent/w:p'):
    p=Paragraph(pnode,DOC._body);t=p.text.lower()
    replacement=None
    if 'eye of the beholder' in t:replacement='The Index Effect in Sweden';p.style='Title'
    elif 'constructs' in t:replacement='A Replication and Extension of\nGreenwood and Sammon (2025)'
    elif 'anna adams' in t:replacement='Alexander Fox'
    elif 'benny berger' in t:replacement='Ludvig Pauli Uväng'
    elif t=='2019':replacement='2026'
    elif t=='bachelor thesis':replacement='Bachelor Thesis Research Draft'
    if replacement is not None:
        p.clear();p.add_run(replacement)
    p.paragraph_format.first_line_indent=Cm(0)
# All title/header text black; preserve source cover positions and SSE seal.
for st in DOC.styles:
    if hasattr(st,'font'):
        st.font.color.rgb=RGBColor(0,0,0)
    for x in list(st.element.xpath('.//w:pBdr')):x.getparent().remove(x)
for x in list(DOC._element.xpath('.//w:pBdr')):x.getparent().remove(x)
for x in DOC._element.xpath('.//w:color'):
    x.attrib.clear();x.set(qn('w:val'),'000000')
# Official cover has an independent black line shape, removed for plain title treatment.
for x in list(DOC._element.xpath('//*[local-name()="line"]')):x.getparent().remove(x)
for x in DOC._element.xpath('//*[local-name()="prstGeom" and @prst="line"]'):
    for line in x.getparent().xpath('./*[local-name()="ln"]'):
        for child in list(line):line.remove(child)
        line.append(OxmlElement('a:noFill'))
for stn in ('Title','Subtitle'):
    st=DOC.styles[stn];st.font.all_caps=False;st.font.name='Arial';st.font.bold=True
DOC.styles['Title'].font.size=Pt(26)
DOC.styles['Subtitle'].font.size=Pt(14)
# Front matter follows the official colophon field order, with verified facts only.
main=(SRC/'main.tex').read_text();MAIN_BREAK_SECTIONS={int(n) for n in re.findall(r'\\clearpage\s*\\input\{sections/(\d+)_',main)};abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',main,re.S)[1].strip()
front={2:'The Index Effect in Sweden',4:abstract,6:'index effect; replication; passive investing; reconstitution; fund holdings.',8:'Alexander Fox\nLudvig Pauli Uväng',10:'Michael Klug',12:'Riccardo Sabbatucci',13:'Bachelor Thesis Research Draft',14:'BE451 Degree Project in Finance\nStockholm School of Economics',15:'© Alexander Fox and Ludvig Pauli Uväng, 2026'}
for idx,txt in front.items():
    p=DOC.paragraphs[idx];p.clear()
    if idx==2:p.style='Title';p.paragraph_format.space_after=Pt(10)
    for n,line in enumerate(txt.split('\n')):
        if n:p.add_run().add_break()
        inline(p,line)
    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(14 if idx==2 else 11);r.font.color.rgb=RGBColor(0,0,0)
    if idx!=2:p.paragraph_format.space_after=Pt(5);p.paragraph_format.space_before=Pt(0);p.paragraph_format.first_line_indent=Cm(0)
for p in DOC.paragraphs[3:]:
    p.paragraph_format.line_spacing=1
    if 'heading' in p.style.name.lower():
        p.paragraph_format.space_before=Pt(8);p.paragraph_format.space_after=Pt(2)
        for r in p.runs:r.font.size=Pt(11);r.bold=True
p=DOC.add_paragraph();inline(p,'Research working draft revised 12 November 2026. This AI-generated research text is for author review and is not a submission version. The course prohibits AI directly writing the submitted thesis. Appendix~\\ref{app:audit} gives the disclosure and verification status.',size=9.5);p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.space_before=Pt(10)
# Keep template's original cover and colophon section geometry; user-specified main body follows.
sec=DOC.add_section(WD_SECTION_START.NEW_PAGE)
sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2.5)
sec.header_distance=sec.footer_distance=Cm(1.25);sec.different_first_page_header_footer=False
sec.header.is_linked_to_previous=False;sec.footer.is_linked_to_previous=False
for x in list(sec._sectPr.xpath('./w:pgNumType')):sec._sectPr.remove(x)
pn=OxmlElement('w:pgNumType');pn.set(qn('w:start'),'1');sec._sectPr.append(pn)
p=sec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');p._p.append(f)
normal=DOC.styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(12)
normal.paragraph_format.line_spacing=1;normal.paragraph_format.space_after=Pt(6);normal.paragraph_format.first_line_indent=Cm(.5);normal.paragraph_format.widow_control=True
for name,sz in [('Heading 1',14),('Heading 2',12),('Heading 3',12)]:
    st=DOC.styles[name];st.font.name='Times New Roman';st.font.size=Pt(sz);st.font.bold=True;st.font.color.rgb=RGBColor(0,0,0)
    st.paragraph_format.space_before=Pt(12);st.paragraph_format.space_after=Pt(6);st.paragraph_format.first_line_indent=Cm(0);st.paragraph_format.left_indent=Cm(0);st.paragraph_format.keep_with_next=True;st.paragraph_format.page_break_before=False
    for x in list(st.element.xpath('.//w:numPr | .//w:position')):x.getparent().remove(x)
    for x in st.element.xpath('.//w:rFonts'):
        for a in list(x.attrib):
            if 'theme' in a.lower():del x.attrib[a]
    np=OxmlElement('w:numPr');ni=OxmlElement('w:numId');ni.set(qn('w:val'),'0');np.append(ni);st.element.get_or_add_pPr().append(np)
for name,sz in [('Caption',10),('Body Text',12),('Table Text',9.5),('Table Note',9.5)]:
    if name not in DOC.styles:DOC.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
    st=DOC.styles[name];st.font.name='Times New Roman';st.font.size=Pt(sz);st.font.color.rgb=RGBColor(0,0,0)
    st.paragraph_format.line_spacing=1;st.paragraph_format.first_line_indent=Cm(0);st.paragraph_format.space_after=Pt(5)
DOC.styles['Caption'].font.italic=False
DOC.core_properties.title='The Index Effect in Sweden';DOC.core_properties.subject='Research working draft for author review';DOC.core_properties.author='Alexander Fox; Ludvig Pauli Uväng';DOC.core_properties.keywords='OMXSB; index effect; replication; research working draft'


def bodypara(s):
    s=s.strip()
    if not s:return
    p=DOC.add_paragraph();notes=[];inline(p,s,footnotes=notes);COUNTS['paragraphs']+=1;SOURCE_PARAGRAPHS.append(cleanbasic(s))
    for n,t in notes:
        np=DOC.add_paragraph();np.paragraph_format.first_line_indent=Cm(0);np.paragraph_format.space_after=Pt(6);inline(np,str(n)+'. '+t,size=9.5)
    return p

def caption(kind,label,text):
    if label not in LABELS:raise ValueError('Unresolved exhibit '+label)
    p=DOC.add_paragraph(style='Caption');p.paragraph_format.keep_with_next=True;p.paragraph_format.keep_together=True;p.paragraph_format.space_before=Pt(8)
    r=p.add_run(kind+' '+LABELS[label]+'. ');r.bold=True;inline(p,text);return p

def render_pdf(pdf,prefix,dpi=300):
    out=TMP/(prefix+'.png')
    if not out.exists() or out.stat().st_mtime<pdf.stat().st_mtime:
        subprocess.run([str(POP),'-f','1','-singlefile','-png','-r',str(dpi),str(pdf),str(TMP/prefix)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return out

def figure(s):
    path=re.search(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',s)[1]
    label=re.search(r'\\label\{([^}]+)\}',s)[1]
    m=re.search(r'\\caption',s);cap,_=brace(s,m.end())
    # Full original caption stays intact and follows the image.
    p=DOC.add_paragraph();p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.keep_with_next=True;p.paragraph_format.space_before=Pt(8);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    img=render_pdf(SRC/path,Path(path).stem);p.add_run().add_picture(str(img),width=Cm(15.8))
    cp=caption('Figure',label,cap);cp.paragraph_format.keep_with_next=False;cp.paragraph_format.space_before=Pt(3);cp.paragraph_format.space_after=Pt(9)
    COUNTS['figures']+=1

def border(cell,edge,sz=6):
    tcPr=cell._tc.get_or_add_tcPr();b=tcPr.find(qn('w:tcBorders'))
    if b is None:b=OxmlElement('w:tcBorders');tcPr.append(b)
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),str(sz));e.set(qn('w:color'),'000000');b.append(e)

def table(s):
    label=re.search(r'\\label\{([^}]+)\}',s)[1];m=re.search(r'\\caption',s);cap,_=brace(s,m.end());caption('Table',label,cap)
    m=re.search(r'\\begin\{tabular\}',s);spec,pos=brace(s,m.end());end=s.index(r'\end{tabular}',pos);data=s[pos:end]
    data=re.sub(r'\\(?:toprule|midrule|bottomrule)','',data)
    rows=[]
    for row in re.split(r'\\\\',data):
        if row.strip():rows.append([x.strip() for x in re.split(r'(?<!\\)&',row)])
    cols=len(rows[0]);assert all(len(row)==cols for row in rows),(label,rows)
    widths=[]
    pwidth=re.findall(r'p\{([\d.]+)cm\}',spec)
    if len(pwidth)==cols:widths=[float(x) for x in pwidth]
    else:
        for c in range(cols):
            vals=[plain(r[c]) for r in rows];body=vals[1:];v=max(body,key=len,default='')
            if all(re.fullmatch(r'[-\d.,]+',x) for x in body):w=max(.9,len(v)*.17+.23)
            elif all(re.fullmatch(r'\d{4}[–-]\d{2,4}',x) for x in body):w=2.2
            elif any(x.startswith('[') for x in body):w=max(2.25,len(v)*.145+.25)
            else:w=max(1.55,min(5.3,len(v)*.115+.4))
            w=max(w,min(2.0,len(vals[0])*.13+.35));widths.append(w)
    if pwidth and len(pwidth)!=cols:
        specs=re.findall(r'p\{[\d.]+cm\}|[lrc]',spec)
        for j,sp in enumerate(specs):
            if sp.startswith('p'):widths[j]=float(re.search(r'[\d.]+',sp)[0])
    widths=[x*16/sum(widths) for x in widths]
    tb=DOC.add_table(rows=len(rows),cols=cols);tb.autofit=False
    pr=tb._tbl.tblPr
    # Minimal booktabs styling: no vertical lines or shading.
    borders=OxmlElement('w:tblBorders')
    for edge in ('top','left','bottom','right','insideH','insideV'):
        x=OxmlElement('w:'+edge);x.set(qn('w:val'),'nil');borders.append(x)
    pr.append(borders)
    mar=OxmlElement('w:tblCellMar')
    for edge,val in [('top',55),('bottom',55),('left',55),('right',55)]:
        x=OxmlElement('w:'+edge);x.set(qn('w:w'),str(val));x.set(qn('w:type'),'dxa');mar.append(x)
    pr.append(mar)
    for j,w in enumerate(widths):tb.columns[j].width=Cm(w)
    # Keep short exhibits intact; long tables can continue with repeating headers.
    keep=len(rows)<=16
    for i,row in enumerate(rows):
        tr=tb.rows[i]._tr;trPr=tr.get_or_add_trPr();trPr.append(OxmlElement('w:cantSplit'))
        if i==0:trPr.append(OxmlElement('w:tblHeader'))
        for j,txt in enumerate(row):
            cell=tb.cell(i,j);cell.width=Cm(widths[j]);p=cell.paragraphs[0];p.style='Table Text';p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1;p.paragraph_format.keep_with_next=keep
            numeric=all(re.match(r'^(?:-?\d|\[|All real)',plain(rr[j])) for rr in rows[1:])
            period=all(re.fullmatch(r'\d{4}[–-]\d{2,4}',plain(rr[j])) for rr in rows[1:])
            p.alignment=WD_ALIGN_PARAGRAPH.RIGHT if numeric and not period else WD_ALIGN_PARAGRAPH.LEFT
            inline(p,txt,size=9.5,bold=i==0)
            for r in p.runs:r.font.name='Times New Roman'
            if i==0:border(cell,'top',8);border(cell,'bottom',5)
            if i==len(rows)-1:border(cell,'bottom',8)
    # End the keep chain in the notes, so the complete exhibit stays together.
    nt=s[end+len(r'\end{tabular}'):]
    nm=re.search(r'\\begin\{minipage\}',nt)
    if nm:
        _,np=brace(nt,nm.end());note=nt[np:nt.index(r'\end{minipage}')];note=re.sub(r'\\(?:footnotesize|small)','',note);note=re.sub(r'\\vspace\{[^}]+\}','',note).strip()
        p=DOC.add_paragraph(style='Table Note');p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(8);p.paragraph_format.keep_with_next=False;p.paragraph_format.keep_together=True;inline(p,note,size=9.5)
    else:
        for p in tb.rows[-1].cells[-1].paragraphs:p.paragraph_format.keep_with_next=False
    COUNTS['tables']+=1

EQINDEX=0
def equation(s):
    global EQINDEX
    if DOC.paragraphs:DOC.paragraphs[-1].paragraph_format.keep_with_next=True
    EQINDEX+=1
    # Render with the same TeX math fonts as the manuscript; no transcription.
    content=re.sub(r'\\label\{[^}]+\}','',s).strip();stem='equation_'+str(EQINDEX);tex=TMP/(stem+'.tex')
    tex.write_text(r'\documentclass[12pt]{article}\usepackage{newtxtext,newtxmath,amsmath}\usepackage[paperwidth=164mm,paperheight=45mm,margin=2mm]{geometry}\pagestyle{empty}\begin{document}\begin{equation}'+content+r'\tag{'+str(EQINDEX)+r'}\end{equation}\end{document}',encoding='utf-8')
    subprocess.run([str(PDFLATEX),'-interaction=nonstopmode','-halt-on-error','-output-directory',str(TMP),str(tex)],check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    img=render_pdf(TMP/(stem+'.pdf'),stem,400)
    im=Image.open(img).convert('RGB');bbox=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
    if not bbox:raise ValueError('Empty equation '+str(EQINDEX))
    margin_px=round(2/25.4*400)
    bbox=(margin_px,max(0,bbox[1]-12),im.width-margin_px,min(im.height,bbox[3]+12));im=im.crop(bbox);im.save(img)
    # Actual TeX sizing retained, capped at the text area.
    cm=min(16,im.width/400*2.54);p=DOC.add_paragraph();p.paragraph_format.first_line_indent=Cm(0);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(6);p.paragraph_format.space_after=Pt(8);p.paragraph_format.keep_with_next=True
    p.add_run().add_picture(str(img),width=Cm(cm));COUNTS['equations']+=1

SECNUM=0;SUBNUM=0;APP=False

def parse(s):
    global SECNUM,SUBNUM
    s=strip_comments(s);i=0;buf=''
    def flush():
        nonlocal buf
        for para in re.split(r'\n\s*\n',buf):bodypara(para)
        buf=''
    while i<len(s):
        if s[i]!='\\':buf+=s[i];i+=1;continue
        cmd,j=command(s,i)
        if cmd in ('section','subsection'):
            flush();title,j=brace(s,j)
            if cmd=='section':SECNUM+=1;SUBNUM=0;num=chr(64+SECNUM) if APP else str(SECNUM)
            else:SUBNUM+=1;num=(chr(64+SECNUM) if APP else str(SECNUM))+'.'+str(SUBNUM)
            p=DOC.add_paragraph(num+' '+plain(title),style='Heading 1' if cmd=='section' else 'Heading 2')
            if cmd=='section' and ((APP and SECNUM==1) or (not APP and SECNUM in MAIN_BREAK_SECTIONS)):p.paragraph_format.page_break_before=True
            i=j;continue
        if cmd=='input':
            flush();path,j=brace(s,j);parse((SRC/(path+'.tex')).read_text());i=j;continue
        if cmd=='begin':
            env,k=brace(s,j)
            if env in ('figure','table','equation'):
                flush();end=s.index('\\end{'+env+'}',k);inside=s[k:end]
                if env=='figure':figure(inside)
                elif env=='table':table(inside)
                else:equation(inside)
                i=end+len('\\end{'+env+'}');continue
            if env=='samepage':i=k;continue
            raise ValueError('Unsupported block '+env)
        if cmd=='end':
            env,k=brace(s,j)
            if env=='samepage':i=k;continue
            raise ValueError('Unexpected end '+env)
        if cmd=='label':_,i=brace(s,j);continue
        if cmd in ('FloatBarrier','clearpage','newpage'):
            flush();i=j;continue
        # Leave inline commands and their balanced contents for the inline parser.
        buf+=s[i:j];i=j
    flush()

for n in range(1,7):parse(next((SRC/'sections').glob(f'{n:02d}_*.tex')).read_text())
p=DOC.add_paragraph('References',style='Heading 1');p.paragraph_format.page_break_before=True
for key,txt in REFS:
    p=DOC.add_paragraph();p.paragraph_format.first_line_indent=Cm(-.6);p.paragraph_format.left_indent=Cm(.6);p.paragraph_format.space_after=Pt(6);inline(p,txt)
APP=True;SECNUM=0;SUBNUM=0
parse((SRC/'sections/07_appendix.tex').read_text())
# Every main/appendix body paragraph must be editable and no source controls survive.
DOC.settings.element.append(OxmlElement('w:updateFields'));DOC.settings.element[-1].set(qn('w:val'),'true')
DOC.save(OUT)
with ZipFile(OUT) as z:
    xml=z.read('word/document.xml').decode()
    visible=' '.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>',xml))
    leaked=re.findall(r'\\[A-Za-z]+|\$(?!\s)',visible)
    if leaked:raise ValueError('Raw LaTeX in Word '+str(leaked[:20]))
report={'output':str(OUT),'source_main_sha256':hashlib.sha256(main.encode()).hexdigest(),'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SRC.rglob('*')) if p.suffix in ('.tex','.bbl','.aux','.pdf') and p.name!='main.pdf'},'counts':COUNTS,'template_sha256':hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),'tables_editable':True,'inline_math':'native OMML','display_equations':'400 dpi TeX-rendered raster','footnotes':'numbered small notes immediately after source paragraph','source_paragraph_count':len(SOURCE_PARAGRAPHS)}
(TMP/'build_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(TMP/'source_paragraphs.json').write_text(json.dumps(SOURCE_PARAGRAPHS,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
