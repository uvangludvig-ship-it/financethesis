"""Separate vendor-estimated NF source audit: presence and replication equality only.
No flow sums, flow rates, returns, covariances or economic outcomes.
"""
from pathlib import Path
import argparse,zipfile,io,datetime,hashlib,json
import pandas as pd
import numpy as np
O=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--valuations',required=True,type=Path);args=ap.parse_args()
paths=[args.valuations,O/'ACQUISITION_PILOT_CLASSES.csv',Path(__file__)]
lock={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Separate direct vendor-estimated NF metadata audit. Compare nonmissing numeric fields across duplicate fund-date copies but never add or report their values. No economic calculations.','rules':['Only requested20classes,2017..2023.','Restrict class-copy eligibility to current-master inception<=source date<=obsolete date when known; metadata is provisional lineage.','For fundNF eachFundId/date gets at most one presence flag; conflicting repeated numerical values fail, never sum copies.','ClassNF alternative requires every current-master active class to have a same-day numeric field, no conflicting duplicate classdate and all classcurrencySEK; this is source presence, not yet capital-reconciled totalfundflow.','Monthly completeness compared both against all observedfunddates and dateswithpositivefundTNA. Missing fields do not become numerical zero.','Fixed24monthhistory endsatq0; compare recorded-day completeness separately from TRI25endpoint route. Complete recorded dates are not proof of complete expected businesscalendar.'],'files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}}
(O/'VENDOR_NF_SOURCE_LOCK.json').write_text(json.dumps(lock,indent=2))
M=pd.read_csv(paths[1],dtype=str);M['inc']=pd.to_datetime(M.inceptiondate,errors='coerce');M['obs']=pd.to_datetime(M.obsoletedate,errors='coerce')
with zipfile.ZipFile(args.valuations) as z:
 names=[n for n in z.namelist() if n.lower().endswith('.csv')];assert len(names)==1
 D=pd.read_csv(io.BytesIO(z.read(names[0])),sep=';',dtype=str)
D.columns=[c.lower() for c in D];D.date=D.date.str.slice(0,10);D=D[D.performanceid.isin(M.performanceid)&D.date.between('2017-01-01','2023-12-31')].merge(M[['performanceid','fundid','FI_fund_id','inc','obs']],on='performanceid',validate='m:1');D['dt']=pd.to_datetime(D.date)
D['active']=D.inc.notna()&D.inc.le(D.dt)&(D.obs.isna()|D.obs.ge(D.dt))
for field in ['netflowclass','netflowfund','tnaclass','tnafund']:
 D[field]=pd.to_numeric(D[field],errors='coerce');D.loc[~np.isfinite(D[field]),field]=np.nan
rows=[]
for (fid,date),g0 in D.groupby(['FI_fund_id','date']):
 g=g0[g0.active];cl=M[M.FI_fund_id.eq(fid)];dt=pd.Timestamp(date);expected=set(cl.loc[cl.inc.notna()&cl.inc.le(dt)&(cl.obs.isna()|cl.obs.ge(dt)),'performanceid'])
 nff=g.netflowfund.dropna();fieldcopies=len(nff);conflict=nff.nunique()>1;nfccy=set(g.loc[g.netflowfund.notna(),'fundcurrencyiso'].dropna())
 byclass=g.groupby('performanceid').agg(nf_present=('netflowclass',lambda a:a.notna().any()),nf_distinct=('netflowclass','nunique'),ccy=('classcurrencyiso',lambda a:';'.join(sorted(a.dropna().unique()))))
 nfclasses=set(byclass.index[byclass.nf_present]);classok=bool(expected and expected<=nfclasses and byclass.loc[list(expected),'nf_distinct'].eq(1).all() and byclass.loc[list(expected),'ccy'].eq('SEK').all()) if expected<=set(byclass.index) else False
 rows.append(dict(FI_fund_id=fid,date=date,ym=date[:7],active_class_rows=len(g),expected_active_classes=len(expected),positive_fund_TNA=bool(g.tnafund.gt(0).any()),fund_NF_any=bool(len(nff)),fund_NF_copies=fieldcopies,fund_NF_conflict=bool(conflict),fund_NF_all_present_ccy_SEK=bool(nfccy=={'SEK'}),fund_NF_source_usable=bool(len(nff) and not conflict and nfccy=={'SEK'}),allactive_class_NF_source_usable=classok))
DAY=pd.DataFrame(rows);DAY.to_csv(O/'VENDOR_NF_FUND_DATE_FLAGS.csv',index=False)
month=[]
for (fid,ym),d in DAY.groupby(['FI_fund_id','ym']):
 a=d[d.positive_fund_TNA];r=dict(FI_fund_id=fid,ym=ym,recorded_dates=len(d),fund_TNA_dates=len(a),fund_NF_present_dates=int(d.fund_NF_any.sum()),fund_NF_usable_dates=int(d.fund_NF_source_usable.sum()),allactive_class_NF_usable_dates=int(d.allactive_class_NF_source_usable.sum()),fund_NF_conflict_dates=int(d.fund_NF_conflict.sum()),replicated_fundNF_dates=int(d.fund_NF_copies.gt(1).sum()),fund_NF_all_recorded_dates_complete=bool(len(d)>0 and d.fund_NF_source_usable.all()),fund_NF_all_TNA_dates_complete=bool(len(a)>0 and a.fund_NF_source_usable.all()),class_NF_all_recorded_dates_complete=bool(len(d)>0 and d.allactive_class_NF_source_usable.all()),class_NF_all_TNA_dates_complete=bool(len(a)>0 and a.allactive_class_NF_source_usable.all()))
 month.append(r)
MON=pd.DataFrame(month);MON.to_csv(O/'VENDOR_NF_FUND_MONTH_COMPLETENESS.csv',index=False)
history=[]
fields=['fund_NF_all_recorded_dates_complete','fund_NF_all_TNA_dates_complete','class_NF_all_recorded_dates_complete','class_NF_all_TNA_dates_complete']
for year in range(2019,2024):
 for half,end in [('H1',f'{year}-03'),('H2',f'{year}-09')]:
  months=set(map(str,pd.period_range(pd.Period(end)-23,pd.Period(end),freq='M')))
  for fid in sorted(M.FI_fund_id.unique()):
   d=MON[MON.FI_fund_id.eq(fid)&MON.ym.isin(months)];r=dict(review=f'{year}{half}',FI_fund_id=fid,first_month=min(months),last_month=max(months),months_recorded=len(d))
   for f in fields:r[f+'_months']=int(d[f].sum());r[f+'_24month_pass']=bool(len(d)==24 and d[f].all())
   history.append(r)
H=pd.DataFrame(history);H.to_csv(O/'VENDOR_NF_24MONTH_SOURCE_HISTORY.csv',index=False)
SUM=DAY.groupby('FI_fund_id').agg(recorded_dates=('date','size'),positive_fund_TNA_dates=('positive_fund_TNA','sum'),fund_NF_present_dates=('fund_NF_any','sum'),fund_NF_usable_dates=('fund_NF_source_usable','sum'),fund_NF_conflict_dates=('fund_NF_conflict','sum'),allactive_class_NF_usable_dates=('allactive_class_NF_source_usable','sum'),replicated_fundNF_dates=('fund_NF_copies',lambda a:int(a.gt(1).sum()))).reset_index()
SUM.to_csv(O/'VENDOR_NF_FUND_SOURCE_SUMMARY.csv',index=False)
summary={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'metadata_only':True,'no_flow_values_summed_or_reported':True,'perfund':SUM.to_dict('records'),'complete_fundNF24_windows':int(H.fund_NF_all_recorded_dates_complete_24month_pass.sum()),'complete_allclassNF24_windows':int(H.class_NF_all_recorded_dates_complete_24month_pass.sum()),'on_positive_fundTNA_dates_complete_fundNF24_windows':int(H.fund_NF_all_TNA_dates_complete_24month_pass.sum()),'on_positive_fundTNA_dates_complete_allclassNF24_windows':int(H.class_NF_all_TNA_dates_complete_24month_pass.sum()),'limitations':'Vendor-estimated NF is not observed cash or exchange orders. Source presence/completeness is separate from source accuracy, fiscalcalendar completeness, currency interpretation, fund continuity and capital reconciliation. Repeated fund NF copies must never be summed. Class aggregate is a candidate only, not calculated.'}
(O/'VENDOR_NF_SOURCE_SUMMARY.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(H.to_string(index=False))
