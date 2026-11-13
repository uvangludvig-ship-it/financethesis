from pathlib import Path
import zipfile,xml.etree.ElementTree as ET,re,json,hashlib
import pandas as pd
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis')
source=R/'data/raw/fi_short/HistoriskaPositioner_2026-10-31.ods'
T='urn:oasis:names:tc:opendocument:xmlns:table:1.0';F='urn:oasis:names:tc:opendocument:xmlns:office:1.0'
with zipfile.ZipFile(source) as z:root=ET.fromstring(z.read('content.xml'))
rows=[]
for table in root.findall('.//{'+T+'}table'):
 for rownum,row in enumerate(table.findall('{'+T+'}table-row'),1):
  cells=[]
  for c in list(row):
   if c.tag not in ['{'+T+'}table-cell','{'+T+'}covered-table-cell']:continue
   repeat=int(c.get('{'+T+'}number-columns-repeated','1'))
   cells.extend([c]*min(repeat,max(0,6-len(cells))))
   if len(cells)>=6:break
  if len(cells)<6:continue
  val=[' '.join(c.itertext()).strip() for c in cells]
  dt=cells[4].get('{'+F+'}date-value',val[4])[:10]
  if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',dt):continue
  holder,issuer,isin,pos,_,comment=val
  censored=bool(re.fullmatch(r'<\s*0[,.]5',pos))
  num=pd.to_numeric(pos.replace(',','.'),errors='coerce')
  rows.append(dict(source_row=rownum,holder=holder,holder_key=re.sub(r'\s+',' ',holder.strip().lower()),
                   issuer=issuer,isin=isin,position_raw=pos,position_numeric=num,
                   below_public_threshold=censored,position_date=dt,comment=comment))
d=pd.DataFrame(rows);assert len(d)==39061
d.to_csv(O/'raw_positions.csv.gz',index=False,compression='gzip')
comments=d[d.comment.ne('')];comments.to_csv(O/'commented_rows.csv',index=False)
key=['holder_key','isin','position_date'];dups=d[d.duplicated(key,keep=False)]
dups.to_csv(O/'duplicate_holder_isin_dates.csv',index=False)
meta=dict(rows=len(d),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
          source=str(source),min_date=d.position_date.min(),max_date=d.position_date.max(),
          unique_holders=d.holder_key.nunique(),unique_ISIN=d['isin'].nunique(),unique_issuer_names=d.issuer.nunique(),
          numeric_rows=int(d.position_numeric.notna().sum()),censored_rows=int(d.below_public_threshold.sum()),
          unparsed_rows=int((d.position_numeric.isna()&~d.below_public_threshold).sum()),
          numeric_below_half=int(d.position_numeric.lt(.5).sum()),commented_rows=len(comments),
          comment_counts=comments.comment.value_counts().to_dict(),duplicate_key_rows=len(dups),
          conflicting_duplicate_keys=int(dups.groupby(key).position_raw.nunique().gt(1).sum()),
          dates_before_20121101=int(d.position_date.lt('2012-11-01').sum()))
(O/'inventory.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False));print(json.dumps(meta,indent=2,ensure_ascii=False))

# Pre-outcome issuer mapping and retrospective baseline coverage only.
E=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv')
U=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv')
E=E.merge(U[['review','ric','company_code','nasdaq_isin','source_url','source_excel_row']],left_on=['review_cycle','RIC'],right_on=['review','ric'],how='left',validate='1:1')
dates=pd.read_csv(R/'output/omxsb_replication_2007/events_car.csv',usecols=['event_id','AD','ED'],parse_dates=['AD','ED'])
E=E.merge(dates,on='event_id',validate='1:1')
idx=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date']);cal=pd.DatetimeIndex(sorted(idx[idx.ric.eq('.OMXSBGI')].date.unique()))
roster=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv')
items=[]
for (review,company),ee in E.groupby(['review_cycle','company_code']):
 e=ee.iloc[0];month=int(review[:4])*100+(4 if review.endswith('1') else 10)
 ids=set(roster.loc[roster.month.eq(month)&roster.company_code.eq(company)&roster.stock_type,'isin'])
 hh=d[d['isin'].isin(ids)&d.position_date.ge('2012-11-01')].copy()
 a=cal.get_loc(e.AD);ed=cal.get_loc(e.ED);base=cal[a-1];end=cal[ed-1];post=cal[ed+20]
 pre=hh[hh.position_date.le(str(base.date()))].sort_values(['position_date','source_row']).groupby('holder_key').tail(1)
 public=pre[pre.position_numeric.ge(.5)]
 items.append(dict(review=review,company_code=company,event_ids=';'.join(ee.event_id),RICs=';'.join(ee.RIC),
                   types=';'.join(sorted(ee.type.unique())),N_security_events=len(ee),AD=str(e.AD.date()),ED=str(e.ED.date()),
                   baseline=str(base.date()),end=str(end.date()),post=str(post.date()),issuer_isins=';'.join(sorted(ids)),
                   baseline_visible_holders=len(public),historical_matched_rows=len(hh),
                   source_url=e.source_url,source_excel_row=int(e.source_excel_row)))
I=pd.DataFrame(items);I.to_csv(O/'issuer_preoutcome_coverage.csv',index=False)
print('PREOUTCOME',json.dumps(dict(security_events=len(E),issuer_events=len(I),
 duplicates=I[I.N_security_events.gt(1)].to_dict('records'),unmapped_security_events=int(E.company_code.isna().sum()),
 issuer_events_by_types=I.types.value_counts().to_dict(),
 baseline_cohort_issuer_events=I[I.baseline_visible_holders.gt(0)].groupby('types').size().to_dict(),
 baseline_cohort_holder_pairs=I.groupby('types').baseline_visible_holders.sum().to_dict()),indent=2))
