from pathlib import Path
import zipfile,xml.etree.ElementTree as ET,re,json,hashlib,datetime
import pandas as pd
O=Path(__file__).resolve().parent
T='urn:oasis:names:tc:opendocument:xmlns:table:1.0';F='urn:oasis:names:tc:opendocument:xmlns:office:1.0'
def parse(source,kind):
 with zipfile.ZipFile(source) as z:root=ET.fromstring(z.read('content.xml'))
 rows=[]
 for table in root.findall('.//{'+T+'}table'):
  for rownum,row in enumerate(table.findall('{'+T+'}table-row'),1):
   cells=[]
   for c in list(row):
    if c.tag not in ['{'+T+'}table-cell','{'+T+'}covered-table-cell']:continue
    cells.extend([c]*min(int(c.get('{'+T+'}number-columns-repeated','1')),max(0,6-len(cells))))
    if len(cells)>=6:break
   if len(cells)<6:continue
   vals=[' '.join(c.itertext()).strip() for c in cells];dt=cells[4].get('{'+F+'}date-value',vals[4])[:10]
   if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',dt):continue
   holder,issuer,isin,pos,_,comment=vals
   rows.append(dict(source_row=f'{kind}:{rownum}',ods_row=rownum,source_file=source.name,source_kind=kind,
                    holder=holder,holder_key=re.sub(r'\s+',' ',holder.strip().lower()),issuer=issuer,isin=isin,
                    position_raw=pos,position_numeric=pd.to_numeric(pos.replace(',','.'),errors='coerce'),
                    below_public_threshold=bool(re.fullmatch(r'<\s*0[,.]5',pos)),position_date=dt,comment=comment))
 return pd.DataFrame(rows)
hist=O/'HistoriskaPositioner_2026-11-02.ods';current=O/'AktuellaPositioner_2026-11-02.ods'
h=parse(hist,'history_20261102');c=parse(current,'current_20261102');d=pd.concat([h,c],ignore_index=True)
h.to_csv(O/'history_20261102.csv.gz',index=False,compression='gzip');c.to_csv(O/'current_20261102.csv',index=False)
d.to_csv(O/'complete_positions_20261102.csv.gz',index=False,compression='gzip')
old=pd.read_csv(O/'raw_positions.csv.gz',keep_default_na=False)
keys=['holder_key','issuer','isin','position_raw','position_date','comment']
j=old[keys].drop_duplicates().merge(h[keys].drop_duplicates(),on=keys,how='outer',indicator=True)
j[j._merge.ne('both')].to_csv(O/'historical_snapshot_differences.csv',index=False)
meta=dict(retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_url='https://www.fi.se/sv/vara-register/blankningsregistret/',
          current_rows=len(c),historical_rows=len(h),combined_rows=len(d),
          historical_rows_removed=len(j[j._merge.eq('left_only')]),historical_rows_added=len(j[j._merge.eq('right_only')]),
          new_history_earliest_position_date=j.loc[j._merge.eq('right_only'),'position_date'].min(),
          current_min_position_date=c.position_date.min(),current_max_position_date=c.position_date.max(),
          input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [hist,current]},
          collection='Both FI public export buttons, same Chrome session; original31Oct history preserved; no position-return test yet.')
(O/'complete_sources.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False));print(json.dumps(meta,indent=2,ensure_ascii=False))
