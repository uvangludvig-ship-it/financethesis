from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _paths import analysis_paths
_PORTABLE_REPO, _PORTABLE_OUT = analysis_paths('volume_measurement_20261102/unit_venue_audit')
import pandas as pd,numpy as np,json,re,hashlib
O=_PORTABLE_OUT;C=O.parents[2];R=_PORTABLE_REPO
E=R/'output/omxsb_open_questions_20261102/eligibility'
U=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv')
px=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','volume','turnover','source'])
choices=[('SAABb.ST',2022,.25),('ANODb.ST',2021,.25),('SINCH.ST',2020,.1),('BILIa.ST',2019,1),('LOOMIS.ST',2019,1)]
px=px[px.ric.isin([r for r,y,k in choices])].copy();assert not px.duplicated(['ric','date']).any()
norm=lambda s:re.sub('[^A-Z0-9]','',str(s).upper())
rows=[];notes=[]
for ric,year,k in choices:
 for month,half in [(4,1),(10,2)]:
  ym=f'{year}{month:02d}';rev=f'{year}H{half}'
  u=U[(U.review==rev)&(U.ric==ric)];assert len(u)==1,(ric,rev,len(u));u=u.iloc[0]
  f=list(E.glob(ym+'.xls*'));assert len(f)==1;f=f[0]
  x=pd.read_excel(f,sheet_name='Instrument Trading Details',header=None)
  h=[i for i,row in x.iloc[:10].iterrows() if 'ISIN' in row.values and 'Instrument' in row.values];assert len(h)==1;h=h[0]
  cols={};
  for j,v in x.iloc[h].items():cols.setdefault(norm(v),[]).append(j)
  rid=int(u.source_excel_row)-1;assert x.iloc[rid,cols['ISIN'][0]]==u.nasdaq_isin
  cvol=min(cols['TOTALNOOFTRADEDSHARES']);ct=min(cols['TOTALTURNOVER']);cp=cols['LATESTPAID'][0];cot=min(cols['OTCTURNOVER']);cd=min(cols['LISTEDDAYS'])
  top=' '.join(map(str,x.iloc[:h,min(cvol,ct)-2:min(cvol,ct)+4].to_numpy().ravel()))
  assert pd.Timestamp(year,month,1).strftime('%B %Y') in top
  nominalvol=float(x.iloc[rid,cvol]);nominalturn=float(x.iloc[rid,ct]);nominalprice=float(str(x.iloc[rid,cp]).strip().replace(',','.'));otc=pd.to_numeric(x.iloc[rid,cot],errors='coerce')
  p=px[(px.ric==ric)&px.date.dt.year.eq(year)&px.date.dt.month.eq(month)].sort_values('date')
  latest=p[p.close.notna()].iloc[-1]
  rows.append(dict(ric=ric,month=ym,isin=u.nasdaq_isin,nasdaq_instrument=x.iloc[rid,0],nasdaq_row=rid+1,nasdaq_volume_column=cvol+1,nasdaq_turnover_column=ct+1,nasdaq_month_volume=nominalvol,nasdaq_month_turnover=nominalturn,nasdaq_month_OTCturnover=otc,nasdaq_latest_paid=nominalprice,panel_month_volume=p.volume.sum(min_count=1),panel_month_turnover=p.turnover.sum(min_count=1),panel_last_close=latest.close,panel_last_date=latest.date,panel_days=len(p),nonmissing_volume=int(p.volume.notna().sum()),positive_volume_days=int(p.volume.gt(0).sum()),source='|'.join(sorted(p.source.unique())),volume_ratio=p.volume.sum(min_count=1)/nominalvol,turnover_ratio=p.turnover.sum(min_count=1)/nominalturn,close_ratio=latest.close/nominalprice,expected_price_factor=k,expected_split_volume_factor=1/k,implied_volume_price_product=(p.volume.sum(min_count=1)/nominalvol)*(latest.close/nominalprice),source_file=str(f),source_url=u.source_url,source_sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
  # Capture all notes/definitions, not whole instrument table.
  contents=pd.read_excel(f,sheet_name='Contents',header=None)
  texts=[' | '.join(str(v) for v in rr.values if pd.notna(v)) for _,rr in contents.iterrows()]
  extra=[]
  for sh in ['Instrument Trading Details','Main Market Trading Details','Company Trading per Exchange']:
   ss=pd.read_excel(f,sheet_name=sh,header=None,nrows=4)
   extra.extend(sh+': '+' | '.join(str(v) for v in rr.values if pd.notna(v)) for _,rr in ss.iterrows())
  rows[-1]['nasdaq_month_listed_days']=int(x.iloc[rid,cd])
  rows[-1]['volume_scaled_to_historical_share_units']=rows[-1]['panel_month_volume']*k
  rows[-1]['scaled_volume_minus_nasdaq']=rows[-1]['panel_month_volume']*k-nominalvol
  notes.append(dict(file=str(f),contents=texts,header_notes=extra))
d=pd.DataFrame(rows);d.to_csv(O/'monthly_comparison.csv',index=False)
(O/'original_workbook_notes.json').write_text(json.dumps(notes,indent=2,ensure_ascii=False))
print(d[['ric','month','nasdaq_month_volume','panel_month_volume','volume_ratio','close_ratio','turnover_ratio','source']].to_string(index=False))
(O/'validation.json').write_text(json.dumps(dict(stock_months=len(d),exact_datedISIN_rows=True,new_returns=False,new_volume_regressions=False,panel_sources=d.source.value_counts().to_dict(),inputs={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),O/'DECISIONS.txt',R/'code/lseg/lseg_pull_v4.py']}),indent=2))
