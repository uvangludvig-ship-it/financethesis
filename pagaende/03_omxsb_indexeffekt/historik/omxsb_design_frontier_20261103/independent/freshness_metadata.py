from pathlib import Path
import pandas as pd,numpy as np,json,zipfile,datetime,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis')
paths=[R/'data/derived/shof_monthly/shof_valuations_monthly.csv',R/'code/claude_checks/data/shof/shof_valuations_2026-11-02.zip',R/'data/raw/shof/fundmaster.xlsx',O/'monthly_source_fund_feasibility.csv']
lock={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only metadata freshness: monthly equality of TNA and source last-nonmissing date. No flows/returns/covariance. Repeated capital is a diagnostic, not proof of staleness. Raw ZIP can verify subset only; absent records not treated as zero.','inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(O/'FRESHNESS_LOCK.json').write_text(json.dumps(lock,indent=2))
M=pd.read_excel(paths[2],usecols=['performanceid','fundid']).drop_duplicates('performanceid')
H=pd.read_csv(paths[3],dtype={'fund_id':str});eligible=set(H.loc[H.provisional25endpoint_pass,'fundid'])
V=pd.read_csv(paths[0],usecols=['performanceId','ym','last_date','tnaclass','tnafund'])
V=V[V.ym.le('2023-12')].merge(M,left_on='performanceId',right_on='performanceid').sort_values(['performanceId','ym'])
V=V[V.fundid.isin(eligible)]
V['monthnum']=pd.PeriodIndex(V.ym,freq='M').asi8
for c in ['tnaclass','tnafund']:
 prev=V.groupby('performanceId')[c].shift();prevmonth=V.groupby('performanceId').monthnum.shift()
 V[c+'_same_prior']=V[c].gt(0)&prev.gt(0)&V[c].eq(prev)&V.monthnum.sub(prevmonth).eq(1)
 V[c+'_same_prior2']=V[c+'_same_prior']&V.groupby('performanceId')[c+'_same_prior'].shift().fillna(False)
stale=V.groupby('fundid').agg(class_months=('ym','size'),same_class_TNA_as_prior=('tnaclass_same_prior','sum'),same_fund_TNA_as_prior=('tnafund_same_prior','sum'),three_month_constant_class=('tnaclass_same_prior2','sum'),three_month_constant_fund=('tnafund_same_prior2','sum')).reset_index()
stale.to_csv(O/'capital_repeat_metadata.csv',index=False)
with zipfile.ZipFile(paths[1]) as z:
 with z.open(z.namelist()[0]) as f:Z=pd.read_csv(f,sep=';',usecols=['performanceId','date','tnaclass','tnafund'])
Z=Z[Z.date.lt('2024-01-01')].copy();Z['ym']=Z.date.str.slice(0,7)
records=[]
for (pid,ym),d in Z.groupby(['performanceId','ym']):
 last=d.date.max();r=dict(performanceId=pid,ym=ym,last_record=last)
 for c in ['tnaclass','tnafund']:
  nums=pd.to_numeric(d[c],errors='coerce');mask=nums.notna()&np.isfinite(nums)
  non=d.loc[mask,'date'];r[c+'_observed_n']=int(mask.sum());r[c+'_latest_observation']=non.max() if len(non) else None
  r[c+'_last_date_lag_days']=(pd.Timestamp(last)-pd.Timestamp(non.max())).days if len(non) else np.nan
 records.append(r)
Q=pd.DataFrame(records);Q.to_csv(O/'zip_capital_observation_dates.csv',index=False)
summary={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'eligible_unique_funds_across_reviews':len(eligible),'eligible_fund_classmonths_pre2024':len(V),'monthly_same_positive_classTNA_as_prior':int(V.tnaclass_same_prior.sum()),'monthly_same_positive_fundTNA_as_prior':int(V.tnafund_same_prior.sum()),'monthly_same_positive_classTNA_three_endpoints':int(V.tnaclass_same_prior2.sum()),'monthly_same_positive_fundTNA_three_endpoints':int(V.tnafund_same_prior2.sum()),'raw_zip_classmonths':len(Q),'raw_zip_allmissing_classTNA_months':int(Q.tnaclass_observed_n.eq(0).sum()),'raw_zip_allmissing_fundTNA_months':int(Q.tnafund_observed_n.eq(0).sum()),'raw_zip_classTNA_lastdate_earlier_than_recordmax_months':int(Q.tnaclass_last_date_lag_days.gt(0).sum()),'raw_zip_fundTNA_lastdate_earlier_than_recordmax_months':int(Q.tnafund_last_date_lag_days.gt(0).sum()),'raw_zip_max_classTNA_lastdate_lag_days':float(Q.tnaclass_last_date_lag_days.max()),'raw_zip_max_fundTNA_lastdate_lag_days':float(Q.tnafund_last_date_lag_days.max()),'raw_zip_validation_is_subset_not_complete_source':True}
(O/'FRESHNESS_METADATA.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
