from pathlib import Path
import urllib.request,json,hashlib,datetime,io
from pypdf import PdfReader
O=Path(__file__).resolve().parent
sources={
'SEB_dividends_2019.pdf':'https://sebgroup.com/siteassets/documents/om-seb-documents/fondbolaget/fondbolaget_bilagor/sve_fond_utd_2019-05.pdf',
'SEB_dividends_2020.pdf':'https://seb.se/contentassets/a01cdb165e404685835c8e95d552be06/fondutdelningar-29-maj-2020.pdf',
'SEB_dividends_2021.pdf':'https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/33E31499051976B3C12586D800401CF6/$FILE/Fondutdelningarmaj2021.pdf',
'SEB_dividends_2022.pdf':'https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/982B8031EB6B50EFC125883F002E28E3/$FILE/Fondutdelningar_maj2022.pdf',
'SEB_dividends_2023.pdf':'https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/D49CABC544B2AE2FC12589A300273250/$FILE/Dividends_May_2023_Swe.pdf',
'SEB_halfyear_2019.pdf':'https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/F83C1127642FB952C12586CD00482D52/$FILE/Halvarsredogorelser_2019.pdf',
'Robur_Access_current_annual.pdf':'https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE37492932',
'Robur_class_letter_2019.pdf':'https://online.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE25346071'
}
rows=[]
for name,url in sources.items():
 row=dict(file=name,source_url=url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),public_document=True,fulltext_republication_allowed=False)
 try:
  with urllib.request.urlopen(url,timeout=25) as r:raw=r.read();row.update(status=r.status,final_url=r.url)
  assert raw.startswith(b'%PDF'), 'Not PDF'
  (O/name).write_bytes(raw);reader=PdfReader(io.BytesIO(raw));row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pages=len(reader.pages))
  matches=[]
  for i,p in enumerate(reader.pages):
   s=p.extract_text()
   if 'SE0001696857' in s or 'Access Sverige' in s or ('Hållbarhetsfond Sverige Index' in s and 'Utveckling' in s):
    matches.append(i+1)
  row['relevant_pdf_pages']=matches
  print(name,row['status'],row['bytes'],'relevant pages',matches)
 except Exception as e:row['error']=str(e);print(name,row['error'])
 rows.append(row)
(O/'PUBLIC_DOCUMENTS.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
