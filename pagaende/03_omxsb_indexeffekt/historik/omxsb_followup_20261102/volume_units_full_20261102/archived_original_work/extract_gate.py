from pathlib import Path
import pandas as pd,numpy as np,json,re,hashlib
O=Path(__file__).resolve().parent;C=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis');B=C/'work/open_questions_20261101';E=B/'eligibility'
norm=lambda s:re.sub('[^A-Z0-9]','',str(s).upper())
def num(v):
 try:return float(str(v).strip().replace(' ','').replace(',','.'))
 except:return np.nan
q=pd.read_csv(B/'demand_quarter/events_locked.csv',parse_dates=['before','after'])
u=pd.read_csv(B/'eligible_pool/review_RIC_control_pool.csv')
e=q.merge(u,left_on=['review_cycle','RIC'],right_on=['review','ric'],how='left',validate='1:1')
p=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','volume','turnover','source']);p=p[p.ric.isin(e.RIC)].copy();assert not p.duplicated(['ric','date']).any()
s={k:g.sort_values('date').set_index('date') for k,g in p.groupby('ric')}
cas=pd.read_csv(R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',parse_dates=['action_date'])
snap=pd.read_csv(B/'demand_quarter/quarter_security_snapshots.csv',parse_dates=['date'])
metadata=[];rows=[]
for rev,g in e.groupby('review_cycle'):
 yr=int(rev[:4]);mo=4 if rev[-1]=='1' else 10;ym=f'{yr}{mo:02d}';start=pd.Timestamp(yr,mo,1);end=start+pd.offsets.MonthEnd(0);start12=start-pd.DateOffset(months=11)
 f=list(E.glob(ym+'.xls*'));assert len(f)==1;f=f[0]
 x=pd.read_excel(f,sheet_name='Instrument Trading Details',header=None)
 hh=[i for i,row in x.iloc[:10].iterrows() if 'ISIN' in row.values and 'Instrument' in row.values];assert len(hh)==1;h=hh[0]
 cols={}
 for j,v in x.iloc[h].items():cols.setdefault(norm(v),[]).append(j)
 metadata.append(dict(review_cycle=rev,month=ym,source_file=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),header_row=h+1,columns=cols))
 for z in g.itertuples():
  row=z._asdict();row.update(month=ym,source_file=str(f),source_sha256=metadata[-1]['sha256'],reference_end=end,reference_start=start,reference_12m_start=start12)
  rid=int(z.source_excel_row)-1;assert x.iloc[rid,cols['ISIN'][0]]==z.nasdaq_isin
  row['instrument_type']=x.iloc[rid,cols['INSTRUMENTTYPE'][0]]
  row['latest_paid']=num(x.iloc[rid,cols['LATESTPAID'][0]])
  pp=s[z.RIC];aa=snap[(snap.event_id==z.event_id)&snap.date.eq(z.after)];assert len(aa)==1;aa=aa.iloc[0]
  row.update(fi_after_price=aa.fi_price,fi_after_isins=aa.ordinary_isins,fi_agreeing_funds=aa.agreeing_funds,after_panel_close=aa.close,after_close_age_days=aa.close_age_days)
  for tag,st,ci in [('month',start,0),('12m',start12,-1)]:
   vv=cols['TOTALNOOFTRADEDSHARES'][ci];tt=cols['TOTALTURNOVER'][ci];dd=cols['LISTEDDAYS'][ci]
   p0=pp.loc[st:end]
   nv=num(x.iloc[rid,vv]);nt=num(x.iloc[rid,tt]);nd=num(x.iloc[rid,dd]);pv=p0.volume.sum(min_count=1);pt=p0.turnover.sum(min_count=1)
   row.update({f'nasdaq_{tag}_volume':nv,f'nasdaq_{tag}_turnover':nt,f'nasdaq_{tag}_listed_days':nd,f'nasdaq_{tag}_volume_excel_column':vv+1,f'nasdaq_{tag}_turnover_excel_column':tt+1,f'panel_{tag}_volume':pv,f'panel_{tag}_turnover':pt,f'panel_{tag}_rows':len(p0),f'panel_{tag}_valid_volume_days':p0.volume.notna().sum(),f'panel_{tag}_positive_volume_days':p0.volume.gt(0).sum(),f'panel_{tag}_negative_volume_days':p0.volume.lt(0).sum(),f'panel_{tag}_negative_turnover_days':p0.turnover.lt(0).sum(),f'panel_{tag}_sources':'|'.join(sorted(p0.source.dropna().unique())),f'{tag}_volume_factor':nv/pv if pv>0 else np.nan,f'{tag}_turnover_relerror':pt/nt-1 if nt>0 else np.nan})
  rc=cas[cas.RIC.eq(z.RIC)&cas.action_date.gt(end)&cas.action_date.le(z.after)]
  ac=cas[cas.RIC.eq(z.RIC)&cas.action_date.ge(start12)&cas.action_date.le(z.after)]
  row['ca_in_bridge']='|'.join(rc.kind);row['ca_in_bridge_dates']='|'.join(rc.action_date.dt.strftime('%Y-%m-%d'));row['ca_in_bridge_sources']='|'.join(rc.source);row['ca_in_12m_through_after']='|'.join(ac.kind+'@'+ac.action_date.dt.strftime('%Y-%m-%d'));row['physical_ordinary_factor_ref_after']=rc.loc[rc.kind.eq('ordinary_split'),'factor'].prod();row['ca_date_precision']='|'.join(rc.date_precision)
  row['factor_month_vs12m_relative']=row['month_volume_factor']/row['12m_volume_factor']-1
  row['candidate_after_factor']=row['month_volume_factor']*row['physical_ordinary_factor_ref_after']
  row['after_price_ratio_for_diagnostic']=aa.close/aa.fi_price
  row['after_price_vs_volume_factor']=row['after_price_ratio_for_diagnostic']/row['candidate_after_factor']-1
  rows.append(row)
d=pd.DataFrame(rows);assert len(d)==216;d.to_csv(O/'unit_measurement_all216.csv',index=False)
(O/'workbook_columns_and_hashes.json').write_text(json.dumps(metadata,indent=2,default=str))
print(d[['event_id','RIC','month_volume_factor','12m_volume_factor','month_turnover_relerror','12m_turnover_relerror','physical_ordinary_factor_ref_after','after_price_vs_volume_factor','ca_in_bridge']].to_string(index=False))
