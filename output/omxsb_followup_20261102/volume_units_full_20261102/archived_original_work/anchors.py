from pathlib import Path
import pandas as pd,numpy as np,json,re,hashlib
O=Path(__file__).resolve().parent;C=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis');B=C/'work/open_questions_20261101';E=B/'eligibility'
norm=lambda s:re.sub('[^A-Z0-9]','',str(s).upper())
def num(v):
 try:return float(str(v).strip().replace(' ','').replace(',','.'))
 except:return np.nan
D=pd.read_csv(O/'unit_measurement_all216.csv');A=json.loads((R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json').read_text());roster=pd.read_csv(E/'dated_stockholm_instrument_roster.csv');p=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','volume','turnover','source']);p=p[p.ric.isin(D.RIC)];S={k:g.set_index('date').sort_index() for k,g in p.groupby('ric')};rows=[]
for ym,g in roster.groupby('month'):
 if ym<201810:continue
 f=list(E.glob(str(ym)+'.xls*'));assert len(f)==1;f=f[0];x=pd.read_excel(f,sheet_name='Instrument Trading Details',header=None)
 hh=[i for i,rr in x.iloc[:10].iterrows() if 'ISIN' in rr.values and 'Instrument' in rr.values];assert len(hh)==1;h=hh[0];cols={}
 for j,v in x.iloc[h].items():cols.setdefault(norm(v),[]).append(j)
 st=pd.Timestamp(str(ym)+'01');en=st+pd.offsets.MonthEnd(0)
 for ric in sorted(D.RIC.unique()):
  allowed=set(A.get(ric,[]))|set(D.loc[D.RIC.eq(ric),'nasdaq_isin']);gg=g[g['isin'].isin(allowed)&g.stock_type&g.listed_at_month_end&~g.preference_name_flag]
  r=dict(RIC=ric,month=ym,month_end=en,matched_rows=len(gg),source_file=str(f))
  if len(gg)!=1:rows.append(r);continue
  z=gg.iloc[0];rid=int(z.source_excel_row)-1;assert x.iloc[rid,cols['ISIN'][0]]==z['isin']
  pp=S[ric].loc[st:en];nv=num(x.iloc[rid,cols['TOTALNOOFTRADEDSHARES'][0]]);nt=num(x.iloc[rid,cols['TOTALTURNOVER'][0]]);pv=pp.volume.sum(min_count=1);pt=pp.turnover.sum(min_count=1);nd=num(x.iloc[rid,cols['LISTEDDAYS'][0]])
  r.update(isin=z['isin'],instrument=z.instrument,source_excel_row=rid+1,source_url=z.source_url,nasdaq_volume=nv,nasdaq_turnover=nt,nasdaq_listed_days=nd,panel_volume=pv,panel_turnover=pt,panel_volume_n=pp.volume.notna().sum(),panel_volume_positive_n=pp.volume.gt(0).sum(),negative_volume_n=pp.volume.lt(0).sum(),panel_source='|'.join(sorted(pp.source.dropna().unique())),factor=nv/pv if pv>0 else np.nan,turnover_relerror=pt/nt-1 if nt>0 else np.nan)
  r['anchor_basic_valid']=bool(nv>0 and pv>0 and nt>0 and np.isfinite(r['turnover_relerror']) and abs(r['turnover_relerror'])<=.001 and r['panel_source']=='tr' and r['panel_volume_n']>=nd and r['negative_volume_n']==0)
  rows.append(r)
d=pd.DataFrame(rows);d.to_csv(O/'all_available_exactISIN_month_anchors.csv',index=False)
# Blind unit diagnostics only.
a=[]
for z in D.itertuples():
 ym=int(z.month);yy=ym//100;mm=ym%100;nextym=(yy*100+10) if mm==4 else ((yy+1)*100+4);prevym=((yy-1)*100+10) if mm==4 else (yy*100+4)
 rr=dict(event_id=z.event_id,RIC=z.RIC,month=ym,ref_factor=z.month_volume_factor)
 for tag,m in [('previous',prevym),('next',nextym)]:
  zz=d[d.RIC.eq(z.RIC)&d.month.eq(m)];assert len(zz)==1,(z.RIC,m,len(zz));zz=zz.iloc[0]
  for c in ['month','isin','factor','anchor_basic_valid','turnover_relerror','source_url','matched_rows']:rr[tag+'_'+c]=zz.get(c)
 rr['next_vs_reference']=rr['next_factor']/rr['ref_factor']-1;a.append(rr)
y=pd.DataFrame(a);y.to_csv(O/'anchor_event_bridge_diagnostics.csv',index=False);print(y.to_string(index=False))
