"""Reproducible supplementary source metadata; no economic outcomes."""
from pathlib import Path
import pandas as pd,zipfile,io,json,datetime
O=Path(__file__).resolve().parent
raw=Path('/Users/ludviguvang/dev/financethesis/data/raw/shof/Valuations/pilot_20261103/FUNDS_VALUATIONS_1793724895212.zip')
M=pd.read_csv(O/'ACQUISITION_PILOT_CLASSES.csv',dtype=str)
with zipfile.ZipFile(raw) as z:
 d=pd.read_csv(io.BytesIO(z.read(z.namelist()[0])),sep=';',usecols=['performanceId','date','netflowfund','tnafund'])
d=d[d.performanceId.isin(M.loc[M.FI_fund_id.eq('51331'),'performanceid'])&d.date.between('2017-01-01','2023-12-31')].merge(M[['performanceid','inceptiondate']],left_on='performanceId',right_on='performanceid');d=d[pd.to_datetime(d.date).ge(pd.to_datetime(d.inceptiondate))]
rows=[]
for date,g in d.groupby('date'):
 x=pd.to_numeric(g.netflowfund,errors='coerce').dropna()
 if len(x)>1:
  span=x.max()-x.min();scale=max(1.,x.abs().max());rows.append(dict(conflict_exact=span>0,conflict_rel1e8=span>1e-8*scale,conflict_rel1e6=span>1e-6*scale,conflict_rel1e4=span>1e-4*scale,fund_TNA_exact_equal=pd.to_numeric(g.tnafund,errors='coerce').dropna().nunique()<=1))
x=pd.DataFrame(rows);rep={c:int(x[c].sum()) for c in x};rep.update(replicated_dates=len(x),scope='Source replication consistency only. Tolerances diagnose floating precision. Exact gate retained; no economic values reported.')
(O/'VENDOR_NF_REPLICATION_TOLERANCE_DIAGNOSTIC.json').write_text(json.dumps(rep,indent=2))
DAY=pd.read_csv(O/'VENDOR_NF_FUND_DATE_FLAGS.csv',dtype={'FI_fund_id':str});bad=DAY[~DAY.fund_NF_any].copy();bad['weekday']=pd.to_datetime(bad.date).dt.day_name();bad[['FI_fund_id','date','weekday','positive_fund_TNA']].to_csv(O/'FUND_NF_MISSING_SOURCE_DATES.csv',index=False)
MON=pd.read_csv(O/'VENDOR_NF_FUND_MONTH_COMPLETENESS.csv',dtype={'FI_fund_id':str});H=pd.read_csv(O/'VENDOR_NF_24MONTH_SOURCE_HISTORY.csv',dtype={'FI_fund_id':str});rows=[]
for r in H.itertuples():
 q=MON[MON.FI_fund_id.eq(r.FI_fund_id)&MON.ym.between(r.first_month,r.last_month)];n=int(q.fund_NF_present_dates.eq(q.recorded_dates).sum());rows.append(dict(review=r.review,FI_fund_id=r.FI_fund_id,first_month=r.first_month,last_month=r.last_month,recorded_months=len(q),fund_NF_presence_complete_months=n,fund_NF_presence_complete24=bool(len(q)==24 and n==24)))
P=pd.DataFrame(rows);P.to_csv(O/'VENDOR_NF_PRESENCE_ONLY_24MONTH.csv',index=False)
J=pd.read_csv(O/'FUND_24MONTH_SOURCE_HISTORY_OLD_NEW.csv',dtype={'FI_fund_id':str})
perfund=[]
for fid,g in J.groupby('FI_fund_id'):
 p=P[P.FI_fund_id.eq(fid)];h=H[H.FI_fund_id.eq(fid)];r=dict(FI_fund_id=fid,old_representative25_windows=int(g.old_representative_SEK_pair_classes25.gt(0).sum()),new_representative25_windows=int(g.new_representative_SEK_pair_classes25.gt(0).sum()),new_strict_allactive25_windows=int(g.new_strict25endpoint_metadata_pass.sum()),vendor_fundNF_presence24_reviews=p.loc[p.fund_NF_presence_complete24,'review'].tolist(),vendor_allactiveclassNF24_reviews=h.loc[h.class_NF_all_recorded_dates_complete_24month_pass,'review'].tolist());perfund.append(r)
summary={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'metadata_only_no_returns_flows_or_covariance':True,'funds':perfund,'replicatedNF_51331_exact_differences_are_all_within_relative1e8':rep['conflict_rel1e8']==0,'interpretation':'Preserved exact-equality gate flags on51331 are floating-precision differences, not substantive source inconsistency. Presence-only vendorNF completeness is reported separately. No duplicate fundNF values summed. Complete source presence is not a final economic usability decision.','actual_fundNF_missing_dates_60087':int(((bad.FI_fund_id=='60087')).sum()),'actual_fundNF_missing_dates_60302':int(((bad.FI_fund_id=='60302')).sum()),'missing_days_imputed_zero':False,'limitations':['Onlyfivefundpilot; no universecapitalcoverage recomputed.','60087 B is an explicit representativeclass alternative, not silent replacement for complete aggregatefundreturn.','Storebrand foreigncurrencyclasses/inceptions require a newsource rule before outcomes.','Vendor NF estimated fromcapitalandreturn; not cash transfers or stock orders.','Delivered source dates need not equal original NAV valuation timestamp.','Exactallactive classliststability is conservative; entry handling is unresolved, not permanently impossible.']}
(O/'FINAL_SOURCE_AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
