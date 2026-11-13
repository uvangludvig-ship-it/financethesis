import zipfile, glob, os, sys, re, collections
import xml.etree.ElementTree as ET
fi_dir=sys.argv[1]
NS='{http://schemas.fi.se/publika/vardepappersfonder/20200331}'
want={'2022Q3','2022Q4','2025Q1','2025Q2','2025Q3'}
pat=re.compile(r'(Länsförsäkringar Sverige Index|Lansforsakringar Sverige Index)',re.I)
res={}
for z in sorted(glob.glob(os.path.join(fi_dir,'Fondinnehav_*.zip'))):
    q=re.search(r'(\d{4}Q\d)',z).group(1)
    if q not in want: continue
    with zipfile.ZipFile(z) as zf:
        for n in zf.namelist():
            if not pat.search(n): continue
            root=ET.fromstring(zf.read(n))
            name=root.find('.//'+NS+'Fond_namn').text
            bm=' | '.join((b.text or '').strip() for b in root.iter(NS+'Jämförelseindex') if b.text and b.text.strip())
            aum=root.find('.//'+NS+'Fondförmögenhet').text
            h={}
            for it in root.iter(NS+'FinansielltInstrument'):
                isin=it.find(NS+'ISIN-kod_instrument'); mv=it.find(NS+'Marknadsvärde_instrument'); nm=it.find(NS+'Instrumentnamn')
                if isin is not None and isin.text and mv is not None and mv.text:
                    h[isin.text]=(float(mv.text),nm.text if nm is not None else '')
            res[(q,name)]=(bm,float(aum),h)
for (q,name),(bm,aum,h) in sorted(res.items()):
    print(q,'|',name,'| AUM %.1f bn'%(aum/1e9),'| n=',len(h),'|',bm[:70])
def turnover(q0,q1,name):
    a=res.get((q0,name)); b=res.get((q1,name))
    if not a or not b: return
    wa={k:v[0]/a[1] for k,v in a[2].items()}; wb={k:v[0]/b[1] for k,v in b[2].items()}
    keys=set(wa)|set(wb)
    to=0.5*sum(abs(wb.get(k,0)-wa.get(k,0)) for k in keys)
    out=[k for k in wa if k not in wb]; new=[k for k in wb if k not in wa]
    print(f'{name} {q0}->{q1}: one-way weight turnover {to:.0%} (~{to*b[1]/1e9:.1f} bn SEK), dropped {len(out)} holdings, added {len(new)}')
    big=sorted(keys,key=lambda k:-abs(wb.get(k,0)-wa.get(k,0)))[:8]
    for k in big:
        nm=(b[2].get(k) or a[2].get(k))[1]
        print(f'   {nm[:30]:30s} weight {wa.get(k,0):.2%} -> {wb.get(k,0):.2%}')
names={n for (_,n) in res}
for n in names:
    turnover('2022Q3','2022Q4',n); turnover('2025Q1','2025Q2',n); turnover('2025Q2','2025Q3',n)
