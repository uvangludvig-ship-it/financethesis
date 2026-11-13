"""Recreate only the fixed candidate request inventory; source workbook read-only."""
from pathlib import Path
import os
from openpyxl import load_workbook
from datetime import datetime
import csv,re
O=Path(os.environ.get('OMXSB_PRICE_WORKDIR',Path(__file__).resolve().parent));P=O/'private';P.mkdir(exist_ok=True)
X=Path(os.environ.get('OMXSB_WORKBOOK','/Users/ludviguvang/Downloads/OMXSBGI_index leavers & joiners_03-Nov-2026.xlsx'))
w=load_workbook(X,read_only=True,data_only=True);rows=[]
for n,(status,issuer,code,date) in enumerate(w['L&J'].iter_rows(min_row=5,max_row=705,values_only=True),5):
 if isinstance(date,datetime) and 2003<=date.year<=2006 and date.month in [1,7] and date.day<=7:
  rows.append({'candidate_id':f'XLSXROW{n}','workbook_row':n,'ric':re.sub(r'\s*\(expired\)\s*$','',code.strip(),flags=re.I).strip(),'type':'addition'if status=='Joiner'else'deletion','candidate_ED':date.strftime('%Y-%m-%d')})
w.close();assert len(rows)==57 and len({r['ric']for r in rows})==43
with (P/'EARLY_CANDIDATES.csv').open('w')as f:
 z=csv.DictWriter(f,fieldnames=rows[0]);z.writeheader();z.writerows(rows)
