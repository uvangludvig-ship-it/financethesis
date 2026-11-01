import zipfile, glob, os, sys, re
import xml.etree.ElementTree as ET
fi_dir=sys.argv[1]; fid=sys.argv[2]
NS='{http://schemas.fi.se/publika/vardepappersfonder/20200331}'
want=['2021Q4','2022Q1','2022Q2','2022Q3','2022Q4','2024Q4','2025Q1','2025Q2','2025Q3']
res={}
for z in sorted(glob.glob(os.path.join(fi_dir,'Fondinnehav_*.zip'))):
    q=re.search(r'(\d{4}Q\d)',z).group(1)
    if q not in want: continue
    with zipfile.ZipFile(z) as zf:
        for n in zf.namelist():
            if f'_{fid}_' not in n: continue
            root=ET.fromstring(zf.read(n))
            aum=float(root.find('.//'+NS+'Fondförmögenhet').text)
            h={}
            for it in root.iter(NS+'FinansielltInstrument'):
                isin=it.find(NS+'ISIN-kod_instrument'); mv=it.find(NS+'Marknadsvärde_instrument'); nm=it.find(NS+'Instrumentnamn')
                if isin is not None and isin.text and mv is not None and mv.text:
                    h[isin.text]=(float(mv.text),(nm.text or '') if nm is not None else '')
            res[q]=(aum,h)
qs=[q for q in want if q in res]
for a,b in zip(qs,qs[1:]):
    A,B=res[a],res[b]
    wa={k:v[0]/A[0] for k,v in A[1].items()}; wb={k:v[0]/B[0] for k,v in B[1].items()}
    keys=set(wa)|set(wb); to=0.5*sum(abs(wb.get(k,0)-wa.get(k,0)) for k in keys)
    print(f'{a}->{b}: one-way turnover {to:.0%} (~{to*B[0]/1e9:.1f} bn SEK) | dropped {sum(1 for k in wa if k not in wb)}, added {sum(1 for k in wb if k not in wa)} | n {len(wa)}->{len(wb)}')
    big=sorted(keys,key=lambda k:-abs(wb.get(k,0)-wa.get(k,0)))[:6]
    for k in big:
        nm=(B[1].get(k) or A[1].get(k))[1]
        print(f'     {nm[:28]:28s} {wa.get(k,0):6.2%} -> {wb.get(k,0):6.2%}')
