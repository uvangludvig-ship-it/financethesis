"""Read-only verification of19 public historical monthly source workbooks.
Uses audit Python because bundled Python lacks the xlrd reader for15 original XLS files.
No price returns, matching, index probabilities or outcome statistics.
"""
from pathlib import Path
import os
import json,re,hashlib,calendar
import pandas as pd
P=Path(__file__).resolve().parent
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
manifest=json.loads((P/'verified_archive_links.json').read_text())
rows=[];rosters=[];headers=[]
def norm(x):return re.sub('[^A-Z0-9]','',str(x).upper())
def parse_date(v):
 if pd.isna(v):return pd.NaT
 if isinstance(v,(int,float)):
  return pd.to_datetime(v,origin='1899-12-30',unit='D')
 return pd.to_datetime(v,errors='coerce')
for z in manifest:
 p=P/z['target_file'];month=z['month'];y=int(month[:4]);m=int(month[-2:]);month_end=pd.Timestamp(y,m,calendar.monthrange(y,m)[1]);name=calendar.month_name[m]+' '+str(y)
 x=pd.read_excel(p,sheet_name='Instrument Trading Details',header=None)
 candidates=[i for i,r in x.iloc[:12].iterrows() if 'ISIN' in r.values and 'Instrument' in r.values]
 assert len(candidates)==1,(month,candidates)
 h=candidates[0];he=x.iloc[h];hn={norm(v):j for j,v in he.items() if pd.notna(v)}
 assert hn['ISIN']==3 and hn['INSTRUMENT']==0
 assert name in str(x.iloc[0,3]),(month,x.iloc[0,3])
 assert 'Main Market Equity Instruments' in str(x.iloc[:h].values)
 # Dates are verified directly against each source notice, not inferred from report month.
 notice=(P/f'{month}_notice.html').read_text()
 assert z['attachment_url'] in notice,(month,'attachment link absent')
 assert z['published_display'] in notice,(month,'timestamp absent')
 publication_match=re.search(r'Published:.*?(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d).*?(CEST|CET)',notice,re.S)
 publication_tz=publication_match.group(2) if publication_match else 'not extracted'
 cols={'INSTRUMENT':'instrument','COMPANYCODE':'company_code','ORDERBOOKCODE':'ticker','ISIN':'isin','INSTRUMENTTYPE':'instrument_type','SEGMENT':'segment','INDUSTRY':'industry','SUPERSECTOR':'supersector','CURRENCY':'currency','LOCATION':'location','DELISTED':'delisted','NOOFSHARESLISTED':'shares_listed','MARKETCAP':'market_cap'}
 assert all(k in hn for k in cols),(month,hn)
 a=x.iloc[h+1:].rename(columns={hn[k]:v for k,v in cols.items()})[list(cols.values())].copy()
 a['source_excel_row']=a.index+1;a=a[a.location.eq('STO')&a["isin"].notna()].copy()
 a['delisted']=a.delisted.map(parse_date);a['listed_at_month_end']=a.delisted.isna()|(a.delisted>month_end)
 a['stock_type']=a.instrument_type.eq('Stock');a['month']=month;a['reference_date']=str(month_end.date());a['publication_timestamp']=z['published_display']+' '+publication_tz;a['source_url']=z['attachment_url'];a['source_sheet']='Instrument Trading Details'
 a['full_omxsb_eligibility_verified']=False;a['historical_ric_mapping_verified']=False
 a['preference_name_flag']=a.instrument.str.contains('pref',case=False,na=False)
 assert not a["isin"].duplicated().any(),(month,'duplicate Stockholm ISIN')
 assert a["isin"].astype(str).str.fullmatch(r'[A-Z]{2}[A-Z0-9]{9}[0-9]').all(),(month,'invalid ISIN syntax')
 expected_rolling=(('May '+str(y-1)+' - April '+str(y)) if m==4 else ('November '+str(y-1)+' - October '+str(y)))
 has_rolling=any(expected_rolling in str(v) for v in x.iloc[:h].to_numpy().ravel())
 assert has_rolling,(month,'rolling12month title absent')
 headers.append({'month':month,'header_excel_row':h+1,'source_notes':[str(v) for v in x.iloc[:h,0] if pd.notna(v)],'headers':{int(j):str(v) for j,v in he.items() if pd.notna(v)},'rolling_title':expected_rolling})
 rows.append(dict(month=month,source_file=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,month_title=name,source_note_confirms_main_market=True,header_excel_row=h+1,stockholm_instruments=len(a),stockholm_stock_rows=int(a.stock_type.sum()),stockholm_stocks_listed_month_end=int((a.stock_type&a.listed_at_month_end).sum()),preference_name_stocks=int((a.stock_type&a.preference_name_flag).sum()),isin_unique=True,isin_syntax_valid=True,rolling12month_title_verified=has_rolling,freefloat_column_present=any('FLOAT' in norm(v) for v in he),publication_timestamp=z['published_display'],publication_timezone=publication_tz,notice_links_downloaded_attachment=True,missing_industry=int(a[a.stock_type].industry.isna().sum()),missing_marketcap=int(a[a.stock_type].market_cap.isna().sum())))
 rosters.append(a)
S=pd.DataFrame(rows)
ev=pd.read_csv(R/'output/omxsb_replication_2007/events_car.csv',usecols=['review_cycle','AD']).drop_duplicates()
S['review_cycle']=S.month.str[:4]+'H'+S.month.str[-2:].map({'04':'1','10':'2'})
S=S.merge(ev,on='review_cycle',how='left',validate='one_to_one')
S['public_before_AD_calendar_day']=pd.to_datetime(S.publication_timestamp).dt.normalize()<pd.to_datetime(S.AD)
S.to_csv(P/'source_validation.csv',index=False)
pd.concat(rosters,ignore_index=True).to_csv(P/'dated_stockholm_instrument_roster.csv',index=False)
(P/'workbook_headers.json').write_text(json.dumps(headers,indent=2,ensure_ascii=False)+'\n')
print(S[['month','stockholm_instruments','stockholm_stocks_listed_month_end','header_excel_row','publication_timestamp','AD','public_before_AD_calendar_day']].to_string(index=False))
print('All19 historical source workbooks, original notice links, reportmonth and relevant headers verified. No returns or eligibility inference beyond source roster.')
