import sys, zipfile, re, csv, os, io, glob
import xml.etree.ElementTree as ET
fi_dir, events_csv, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
ev = list(csv.DictReader(open(events_csv)))
isins = set()
for e in ev:
    for s in re.split(r'[;,| ]+', e['isins']):
        if s: isins.add(s.strip())
NS = '{http://schemas.fi.se/publika/vardepappersfonder/20200331}'
funds_out = open(os.path.join(out_dir,'funds.csv'),'w',newline='')
hold_out = open(os.path.join(out_dir,'holdings.csv'),'w',newline='')
fw = csv.writer(funds_out); hw = csv.writer(hold_out)
fw.writerow(['quarter','fund_id','fund_isin','fund_name','company','status','aum','active_risk','benchmark','n_instr'])
hw.writerow(['quarter','fund_id','isin','antal'])
def txt(el, tag):
    x = el.find('.//'+NS+tag)
    return x.text.strip() if x is not None and x.text else ''
for z in sorted(glob.glob(os.path.join(fi_dir,'Fondinnehav_*.zip'))):
    with zipfile.ZipFile(z) as zf:
        for name in zf.namelist():
            if not name.lower().endswith('.xml'): continue
            try:
                root = ET.fromstring(zf.read(name))
            except Exception as ex:
                continue
            q = txt(root,'Kvartalsslut')
            fid = txt(root,'Fond_institutnummer')
            bm = ' | '.join((b.text or '').strip() for b in root.iter(NS+'Jämförelseindex') if b.text and b.text.strip())
            instr = list(root.iter(NS+'FinansielltInstrument'))
            fw.writerow([q,fid,txt(root,'Fond_ISIN-kod'),txt(root,'Fond_namn'),txt(root,'Fondbolag_namn'),txt(root,'Fond_status'),
                         txt(root,'Fondförmögenhet'),txt(root,'Aktiv_risk'),bm,len(instr)])
            for it in instr:
                isin = txt(it,'ISIN-kod_instrument')
                if isin in isins:
                    hw.writerow([q,fid,isin,txt(it,'Antal')])
funds_out.close(); hold_out.close()
print('done')
