"""Verify all FI XML report envelopes and reconcile latest fund-quarter row counts."""
import json
import re
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/omxsb_audit_20261031'
BAD=re.compile('[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd]')
rows=[];errors=[]
for p in sorted((ROOT/'data/raw/fi').glob('Fondinnehav_*.zip')):
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            if not name.lower().endswith('.xml'):continue
            try:
                raw=z.read(name)
                # Same XML hygiene as the replication parser, with no raw mutation.
                try:r=ET.fromstring(raw)
                except ET.ParseError:r=ET.fromstring(BAD.sub('',raw.decode('utf-8-sig')))
                for node in r.iter():node.tag=node.tag.split('}')[-1]
                def tx(tag):
                    x=next(r.iter(tag),None)
                    return x.text.strip() if x is not None and x.text else ''
                pub=re.search(r'_(\d{4}-\d{2}-\d{2} \d{2}\.\d{2})\.xml$',name)
                rows.append(dict(zip=p.name,file=name,fund=tx('Fond_institutnummer'),quarter=tx('Kvartalsslut'),
                    fund_name=tx('Fond_namn'),benchmark=' | '.join(x.text.strip() for x in r.iter('Jämförelseindex') if x.text),
                    published_file=pub.group(1) if pub else '',n_instruments=sum(1 for _ in r.iter('FinansielltInstrument'))))
            except Exception as exc:errors.append(dict(zip=p.name,file=name,error=str(exc)))
raw=pd.DataFrame(rows)
raw.to_csv(OUT/'fi_raw_report_inventory.csv',index=False)
pd.DataFrame(errors,columns=['zip','file','error']).to_csv(OUT/'fi_raw_parse_errors.csv',index=False)
latest=raw[raw.published_file.eq(raw.groupby(['fund','quarter']).published_file.transform('max'))]
counts=latest.groupby(['fund','quarter']).agg(raw_rows=('n_instruments','sum'),latest_files=('file','size'))
h=pd.read_csv(ROOT/'data/derived/fi/fi_holdings_long.csv.gz',usecols=['Fond_institutnummer','Kvartalsslut'],dtype=str)
hc=h.rename(columns={'Fond_institutnummer':'fund','Kvartalsslut':'quarter'}).groupby(['fund','quarter']).size().rename('derived_rows')
rec=counts.join(hc,how='outer').reset_index()
rec['row_count_matches']=rec.raw_rows.fillna(0).eq(rec.derived_rows.fillna(0))
rec.to_csv(OUT/'fi_raw_derived_reconciliation.csv',index=False)
summary=dict(xml_files=len(raw)+len(errors),parsed=len(raw),parse_errors=len(errors),
    latest_fund_quarters=len(rec),row_count_mismatches=int((~rec.row_count_matches).sum()),
    zero_instrument_reports=int(latest.n_instruments.eq(0).sum()),raw_latest_instrument_rows=int(latest.n_instruments.sum()),
    derived_rows=len(h),latest_multiple_reports=int(rec.latest_files.gt(1).sum()))
(OUT/'fi_raw_summary.json').write_text(json.dumps(summary,indent=2));print(summary)
