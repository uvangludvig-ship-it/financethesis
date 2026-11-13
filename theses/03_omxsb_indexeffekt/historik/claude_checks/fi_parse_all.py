import zipfile, glob, re, xml.etree.ElementTree as ET, pandas as pd, sys
R='../..'
funds=[]; hold=[]
for z in sorted(glob.glob(f'{R}/data/raw/fi/Fondinnehav_*.zip')):
    q=re.search(r'(\d{4}Q\d)',z).group(1); Z=zipfile.ZipFile(z)
    for n in Z.namelist():
        if not n.lower().endswith('.xml'): continue
        try: root=ET.fromstring(Z.read(n))
        except Exception: continue
        NS=root.tag.split('}')[0]+'}'
        g=lambda p: (root.find('.//'+NS+p).text or '').strip() if root.find('.//'+NS+p) is not None and root.find('.//'+NS+p).text else ''
        fid=g('Fond_institutnummer'); qd=g('Kvartalsslut')
        bms=[ (e.text or '').strip() for e in root.iter(NS+'Jämförelseindex') if e.text and e.text.strip()]
        funds.append(dict(q=q,kvartal=qd,fund_id=fid,namn=g('Fond_namn'),bolag=g('Fondbolag_namn'),aum=g('Fondförmögenhet'),aktiv_risk=g('Aktiv_risk'),jmf=' | '.join(bms)))
        for it in root.iter(NS+'FinansielltInstrument'):
            f=lambda p: (it.find(NS+p).text or '').strip() if it.find(NS+p) is not None and it.find(NS+p).text else ''
            if f('Tillgångsslag_enligt_LVF_5_kap')!='ÖverlåtbartVärdepapper': continue
            isin=f('ISIN-kod_instrument')
            if not isin: continue
            hold.append((q,qd,fid,isin,f('Instrumentnamn'),f('Antal')))
    print(q,len(funds),len(hold),flush=True)
F=pd.DataFrame(funds); H=pd.DataFrame(hold,columns=['q','kvartal','fund_id','isin','instrument','antal'])
F=F.drop_duplicates(['q','fund_id'],keep='last')
F.to_csv('data/fi_all_funds.csv',index=False); H.to_pickle('data/fi_all_holdings.pkl')
print('klart',F.shape,H.shape)
