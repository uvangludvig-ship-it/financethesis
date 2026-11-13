"""Prepare auditable OMXSB half-year AP/FI observations, without estimating effects.
All inputs read-only. Writes exclusively to the new ownership output directory.
"""
from pathlib import Path
import argparse,json,hashlib,re,unicodedata
import pandas as pd
import numpy as np

def norm(s):
 s=unicodedata.normalize('NFKD',str(s).upper());s=''.join(c for c in s if not unicodedata.combining(c))
 s=re.sub(r'\([^)]*\)',' ',s)
 stop={'AB','PUBL','SER','SERIE','SERIES','SHS','SHARE','SHARES','ORD','CLASS','CL','AKTIEBOLAG','THE','INC','CORP','CORPORATION','LTD','PLC','OYJ','ASA','SA','SDB','SDR','REG','REGISTERED','NPV','STK','AKTIE','AKTIER','ORDINARY','COMMON','STOCK','VPL','BEARER'}
 return ' '.join(x for x in re.sub('[^A-Z0-9 ]',' ',s).split() if x not in stop)
def prev_half(d):
 return pd.Timestamp(d.year,6,30) if d.month==12 else pd.Timestamp(d.year-1,12,31)
def after_half(d):return pd.Timestamp(d.year,6,30) if d.month<=6 else pd.Timestamp(d.year,12,31)
def serial(x):
 if isinstance(x,set):return sorted(x)
 if isinstance(x,(np.integer,np.floating)):return x.item()
 return str(x)

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--out',type=Path);args=p.parse_args()
 root=args.repo;out=args.out or root/'output/omxsb_extension_20261031/ownership';out.mkdir(parents=True,exist_ok=True)
 paths={'ap':root/'data/derived/ap/ap_svenska_aktier_med_ric.csv','events':root/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv','fi':root/'data/derived/fi/fi_holdings_long.csv.gz','price':root/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet','net':root/'output/omxsb_audit_20261031/corrected/nettrading_omxsb.csv'}
 # net is used only for the frozen event universe / identifier candidates, not outcomes.
 net=pd.read_csv(paths['net'],usecols=['event_id','isins','shares_qa']);net['original_quantity_available']=net.shares_qa.notna();net=net.drop(columns='shares_qa')
 ev=pd.read_csv(paths['events'],parse_dates=['announcement_date','effective_date']).rename(columns={'announcement_date':'AD','effective_date':'ED'})
 ev=ev.merge(net,on='event_id');ev=ev[ev.AD.ge('2019-01-01')].copy();ev['after']=ev.ED.map(after_half);ev['before']=ev.after.map(prev_half);ev['prior']=ev.before.map(prev_half)
 ev['main_period']=ev.ED.lt('2026-01-01')&ev.original_quantity_available
 ap=pd.read_csv(paths['ap'],parse_dates=['datum']).fillna({'RIC':'','ISIN':'','RIC_kandidater':'','datakvalitetsflaggor':'','bolagsnamn':''})
 static=pd.read_csv(root/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv').set_index('ric')
 oldflags=pd.read_csv(root/'output/omxsb_audit_20261031/historical_isin_name_flags.csv')
 ev['old_name_class_flag']=ev.event_id.isin(oldflags.loc[oldflags.flag,'event_id'])
 aset={r:set(g.ISIN[g.ISIN.ne('')]) for r,g in ap.loc[ap.RIC.ne('')&~ap.osaker_matchning].groupby('RIC')}
 isinmap={}
 for r,g in ev.groupby('RIC'):
  v=set(';'.join(g.isins.fillna('')).split(';'))|set(g['isin'].dropna())|aset.get(r,set());v.discard('')
  if r in static.index and pd.notna(static.loc[r,'IssueISIN']):v.add(static.loc[r,'IssueISIN'])
  isinmap[r]=v
 all_isins=set().union(*isinmap.values())
 half_dates=set(ev[['before','after','prior']].stack())
 cols=['Tillgångsslag_enligt_LVF_5_kap','Instrumentnamn','ISIN-kod_instrument','Valuta','Antal','Kurs_som_använts_vid_värdering_av_instrumentet','Marknadsvärde_instrument','Kvartalsslut','Fond_institutnummer','Fond_namn','Fondbolag_namn','Fond_ISIN-kod','Jämförelseindex']
 metadata=[];holdings=[]
 for chunk in pd.read_csv(paths['fi'],usecols=cols,chunksize=200000):
  chunk['Kvartalsslut']=pd.to_datetime(chunk.Kvartalsslut)
  metadata.append(chunk[['Kvartalsslut','Fond_institutnummer','Fond_namn','Fondbolag_namn','Fond_ISIN-kod','Jämförelseindex']].drop_duplicates())
  q=chunk[chunk.Kvartalsslut.isin(half_dates)&chunk['ISIN-kod_instrument'].isin(all_isins)&chunk['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')].copy()
  holdings.append(q)
 meta=pd.concat(metadata).drop_duplicates().sort_values(['Fond_institutnummer','Kvartalsslut'])
 meta.to_csv(out/'fi_fund_quarter_metadata.csv',index=False)
 h=pd.concat(holdings,ignore_index=True)
 for col in ['Antal','Marknadsvärde_instrument','Kurs_som_använts_vid_värdering_av_instrumentet']:h[col]=pd.to_numeric(h[col],errors='coerce')
 h['invalid_instrument_name']=h.Instrumentnamn.fillna('').str.contains(r'\b(?:BTA|BTR|BTU|TR|TO\d*|WARRANT|RIGHTS?|REDEMPTION|INLOSEN|INLÖSEN)\b',case=False,regex=True)
 # An ISIN can be rejected if its observed names identify rights / redemption instruments.
 names=h.groupby('ISIN-kod_instrument').agg(names=('Instrumentnamn',lambda s:' | '.join(sorted(set(s.dropna())))),n=('Antal','size'),invalid_name=('invalid_instrument_name','any'))
 names.to_csv(out/'fi_isin_name_inventory.csv')
 for r,s in isinmap.items():isinmap[r]={i for i in s if i not in names.index or not names.loc[i,'invalid_name']}
 h[~h.invalid_instrument_name & (h.Antal.isna()|h.Antal.lt(0))].to_csv(out/'fi_halfyear_ambiguous_quantity_rows.csv',index=False)
 h=h[~h.invalid_instrument_name&h.Antal.notna()&h.Antal.ge(0)].copy()
 h.to_csv(out/'fi_halfyear_instrument_rows.csv.gz',index=False,compression='gzip')
 name_records=[]
 for ric,g in ev.groupby('RIC'):
  a=ap[(ap.RIC.eq(ric)) | ap.RIC_kandidater.map(lambda s:ric in s.split('|'))]
  for r in a[['bolagsnamn','ISIN','RIC','matchningsmetod','osaker_matchning','samlat_aktieslag']].drop_duplicates().itertuples(index=False):
   name_records.append(dict(target_RIC=ric,event_company=g.company.iloc[0],source_name=r.bolagsnamn,source_ISIN=r.ISIN,assigned_RIC=r.RIC,method=r.matchningsmetod,uncertain=r.osaker_matchning,combined=r.samlat_aktieslag,exact_norm=norm(r.bolagsnamn)==norm(g.company.iloc[0])))
 pd.DataFrame(name_records).to_csv(out/'ap_identity_review.csv',index=False)
 px=pd.read_parquet(paths['price'],columns=['ric','date','close','shares'])
 px=px[px.ric.isin(isinmap)].copy();px['date']=pd.to_datetime(px.date);px=px.sort_values('date')
 bypx={r:g.set_index('date') for r,g in px.groupby('ric')}
 snaps=[]
 for ric,isins in isinmap.items():
  for date in sorted(half_dates):
   q=h[h.Kvartalsslut.eq(date)&h['ISIN-kod_instrument'].isin(isins)]
   prices=q[q.Valuta.eq('SEK')&q.Antal.gt(0)&q.Marknadsvärde_instrument.gt(0)]
   pr=(prices.Marknadsvärde_instrument/prices.Antal).median() if len(prices) else np.nan
   x=bypx.get(ric,pd.DataFrame()).loc[:date] if ric in bypx else pd.DataFrame()
   sh=x.shares.dropna() if len(x) else pd.Series(dtype=float);cl=x.close.dropna() if len(x) else pd.Series(dtype=float)
   snaps.append(dict(RIC=ric,date=date,fi_isins=';'.join(sorted(set(q['ISIN-kod_instrument']))),allowed_isins=';'.join(sorted(isins)),fi_names=' | '.join(sorted(set(q.Instrumentnamn.dropna()))),fi_price=pr,fi_rows=len(q),close=cl.iloc[-1] if len(cl) else np.nan,shares=sh.iloc[-1] if len(sh) else np.nan,shares_date=sh.index[-1] if len(sh) else pd.NaT,close_date=cl.index[-1] if len(cl) else pd.NaT))
 sn=pd.DataFrame(snaps);sn.to_csv(out/'security_halfyear_snapshots.csv',index=False)
 ix=sn.set_index(['RIC','date']);ca=[]
 for r in ev.itertuples():
  for window,b,a in [('event',r.before,r.after),('prior',r.prior,r.before)]:
   sb=ix.loc[(r.RIC,b)];sa=ix.loc[(r.RIC,a)];raw=(sb.fi_price/sa.fi_price)/(sb.close/sa.close) if sb.close>0 and sa.close>0 and sa.fi_price>0 else np.nan
   candidates=np.array([1.]+list(range(2,51))+[1/n for n in range(2,51)])
   idx=np.argmin(abs(raw/candidates-1)) if np.isfinite(raw) else 0;factor=float(candidates[idx]) if np.isfinite(raw) and abs(raw/candidates[idx]-1)<.03 else np.nan
   ca.append(dict(event_id=r.event_id,RIC=r.RIC,company=r.company,review_cycle=r.review_cycle,type=r.type,window=window,before=b,after=a,raw_price_factor=raw,candidate_factor=factor,shares_before=sb.shares,shares_after=sa.shares,shares_ratio=sa.shares/sb.shares if sb.shares>0 else np.nan,before_fi_isins=sb.fi_isins,after_fi_isins=sa.fi_isins,before_fi_names=sb.fi_names,after_fi_names=sa.fi_names,old_name_class_flag=r.old_name_class_flag,main_period=r.main_period))
 pd.DataFrame(ca).to_csv(out/'halfyear_CA_review.csv',index=False)
 ev.to_csv(out/'events_locked.csv',index=False)
 (out/'allowed_isins.json').write_text(json.dumps({k:sorted(v) for k,v in isinmap.items()},indent=2))
 hashes={k:dict(path=str(v.relative_to(root)),sha256=hashlib.sha256(v.read_bytes()).hexdigest()) for k,v in paths.items()}
 (out/'input_hashes.json').write_text(json.dumps(hashes,indent=2))
 print(json.dumps(dict(events=len(ev),main_events=int(ev.main_period.sum()),fi_rows=len(h),fund_quarter_meta=len(meta),snapshots=len(sn),CA_cases=sum(1 for x in ca if x['candidate_factor']!=1)),indent=2))

if __name__=='__main__':main()
