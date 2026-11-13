"""Source metadata only. Run copied validator first, then this script with same paths.
No numerical fund returns, flows, covariance or stock outcomes are calculated.
"""
from pathlib import Path
import argparse,datetime,json,hashlib,zipfile,io
import pandas as pd
import numpy as np

O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis')
ap=argparse.ArgumentParser();ap.add_argument('--valuations',required=True,type=Path);ap.add_argument('--rips',required=True,type=Path);args=ap.parse_args()
oldv=R/'data/derived/shof_monthly/shof_valuations_monthly.csv';oldr=R/'data/derived/shof_monthly/shof_rips_monthly.csv'
paths=[args.valuations,args.rips,oldv,oldr,O/'ACQUISITION_PILOT_CLASSES.csv',O/'PRE_DOWNLOAD_AUDIT_SPEC.txt',Path(__file__)]
(O/'SOURCE_COMPARISON_LOCK.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Metadata comparison only; no flows or return calculations.','files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}},indent=2))
M=pd.read_csv(O/'ACQUISITION_PILOT_CLASSES.csv',dtype=str);want=set(M.performanceid);M['inc']=pd.to_datetime(M.inceptiondate,errors='coerce');M['obs']=pd.to_datetime(M.obsoletedate,errors='coerce')

def raw_read(p):
    if zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z:
            names=[n for n in z.namelist() if n.lower().endswith('.csv')];assert len(names)==1
            b=z.read(names[0])
    else:b=p.read_bytes()
    first=b.decode('utf-8-sig').splitlines()[0];sep=';' if first.count(';')>first.count(',') else ','
    d=pd.read_csv(io.BytesIO(b),sep=sep,dtype=str,encoding='utf-8-sig');d.columns=[str(c).strip().lower() for c in d.columns]
    d.date=d.date.str.slice(0,10);d=d[d.performanceid.isin(want)&d.date.between('2017-01-01','2023-12-31')].copy();d['ym']=d.date.str.slice(0,7)
    return d

V=raw_read(args.valuations);T=raw_read(args.rips);assert 'returntype' in T;T=T[T.returntype.isin(['1','1.0'])].copy()
dups=[]
for source,d in [('valuations',V),('rips',T)]:
    for (pid,date),g in d[d.duplicated(['performanceid','date'],keep=False)].groupby(['performanceid','date']):
        cols=[c for c in g if c not in ['performanceid','date','ym']]
        conflict=[c for c in cols if g[c].fillna('<MISSING>').nunique()>1]
        dups.append(dict(source=source,performanceid=pid,date=date,rows=len(g),conflicting_columns=';'.join(conflict)))
pd.DataFrame(dups,columns=['source','performanceid','date','rows','conflicting_columns']).to_csv(O/'DUPLICATE_SOURCE_KEYS.csv',index=False)
new=[]
for (pid,ym),d in V.groupby(['performanceid','ym']):
    r=dict(performanceid=pid,ym=ym,valuation_rows=len(d),valuation_dates=d.date.nunique(),valuation_last_record=d.date.max(),valuation_duplicate=bool(d.duplicated(['performanceid','date']).any()))
    for f in ['tnaclass','tnafund']:
        nums=pd.to_numeric(d[f],errors='coerce');z=d[nums.gt(0)&np.isfinite(nums)].sort_values('date')
        r[f+'_present']=len(z)>0;r[f+'_date']=z.date.iloc[-1] if len(z) else None;r[f+'_value']=float(z[f].iloc[-1]) if len(z) else np.nan
    for f in ['classcurrencyiso','fundcurrencyiso']:
        r[f]=';'.join(sorted(d[f].dropna().unique())) if f in d else None
    for f in ['netflowclass','netflowfund']:
        mask=d[f].notna()&~d[f].isin(['','NULL','NaN','nan','NA']) if f in d else pd.Series(False,index=d.index)
        r[f+'_recorded_complete']=bool(len(d)>0 and mask.all() and not r['valuation_duplicate']);r[f+'_any_present']=bool(mask.any())
    new.append(r)
NV=pd.DataFrame(new)
rt=[]
for (pid,ym),d in T.groupby(['performanceid','ym']):
    num=pd.to_numeric(d.unit_sek,errors='coerce');z=d[num.gt(0)&np.isfinite(num)].sort_values('date')
    rt.append(dict(performanceid=pid,ym=ym,tri_present=len(z)>0,tri_date=z.date.iloc[-1] if len(z) else None,tri_duplicate=bool(d.duplicated(['performanceid','date']).any())))
NT=pd.DataFrame(rt)
N=NV.merge(NT,on=['performanceid','ym'],how='outer',validate='1:1')
N['date_gap']=(pd.to_datetime(N.tnaclass_date)-pd.to_datetime(N.tri_date)).abs().dt.days
N['pair_present']=N.tnaclass_present.fillna(False)&N.tri_present.fillna(False)
N['pair_date0']=N.pair_present&N.date_gap.eq(0)
N['pair_date4']=N.pair_present&N.date_gap.le(4)
N['representative_SEK_pair']=N.pair_date4&N.classcurrencyiso.eq('SEK')&~N.valuation_duplicate.fillna(False)&~N.tri_duplicate.fillna(False)
N=N.merge(M[['performanceid','fundid','FI_fund_id']],on='performanceid',validate='m:1')
# Save flags and dates only, never downloaded numeric capital or totalreturn levels.
N.drop(columns=['tnaclass_value','tnafund_value']).to_csv(O/'NEW_CLASS_MONTH_SOURCE_FLAGS.csv',index=False)

A=pd.read_csv(oldv,usecols=['performanceId','ym','last_date','ccy_class','tnaclass','tnafund']);A=A[A.performanceId.isin(want)&A.ym.between('2017-01','2023-12')].rename(columns={'performanceId':'performanceid','last_date':'tna_date'})
B=pd.read_csv(oldr,usecols=['performanceId','returntype','ym','last_date','tri_sek']);B=B[B.performanceId.isin(want)&B.ym.between('2017-01','2023-12')&B.returntype.eq(1)].rename(columns={'performanceId':'performanceid','last_date':'tri_date'})
OLD=A.merge(B[['performanceid','ym','tri_date','tri_sek']],on=['performanceid','ym'],how='outer',validate='1:1')
OLD['tnaclass_present']=OLD.tnaclass.gt(0)&np.isfinite(OLD.tnaclass);OLD['tnafund_present']=OLD.tnafund.gt(0)&np.isfinite(OLD.tnafund);OLD['tri_present']=OLD.tri_sek.gt(0)&np.isfinite(OLD.tri_sek)
OLD['date_gap']=(pd.to_datetime(OLD.tna_date)-pd.to_datetime(OLD.tri_date)).abs().dt.days
OLD['representative_SEK_pair']=OLD.tnaclass_present&OLD.tri_present&OLD.ccy_class.eq('SEK')&OLD.date_gap.le(4)
class_rows=[]
for m in M.itertuples():
    for source,d in [('old',OLD[OLD.performanceid.eq(m.performanceid)]),('new',N[N.performanceid.eq(m.performanceid)])]:
        r=dict(FI_fund_id=m.FI_fund_id,fundid=m.fundid,performanceid=m.performanceid,ISIN=m.ISIN,source=source,inceptiondate=m.inceptiondate,obsoletedate=m.obsoletedate)
        for f in ['tnaclass_present','tnafund_present','tri_present','representative_SEK_pair']:
            z=d.loc[d[f].fillna(False).astype(bool)];r[f+'_months']=z.ym.nunique();r[f+'_first_month']=z.ym.min() if len(z) else None;r[f+'_last_month']=z.ym.max() if len(z) else None
        class_rows.append(r)
pd.DataFrame(class_rows).to_csv(O/'CLASS_SOURCE_OLD_NEW_COMPARISON.csv',index=False)

fund_month=[]
for fid,classes in M.groupby('FI_fund_id'):
    for per in pd.period_range('2017-01','2023-12',freq='M'):
        active=classes[classes.inc.notna()&classes.inc.le(per.end_time)&(classes.obs.isna()|classes.obs.ge(per.end_time))]
        z=N[N.FI_fund_id.eq(fid)&N.ym.eq(str(per))&N.performanceid.isin(active.performanceid)]
        complete=len(active)>0 and set(z.performanceid)==set(active.performanceid)
        positive=complete and bool(z.tnaclass_present.fillna(False).all()&z.tnafund_present.fillna(False).all())
        same_ccy=complete and bool(z.classcurrencyiso.eq('SEK').all()&z.fundcurrencyiso.eq('SEK').all())
        dates=positive and z.tnaclass_date.nunique()==1 and z.tnafund_date.nunique()==1 and z.tnaclass_date.iloc[0]==z.tnafund_date.iloc[0]
        den=z.tnafund_value.median() if positive else np.nan
        ratio=float(z.tnaclass_value.sum()/den) if positive and same_ccy and dates and den>0 else np.nan
        spread=float((z.tnafund_value.max()-z.tnafund_value.min())/den) if positive and same_ccy and dates and den>0 else np.nan
        pair=complete and bool(z.representative_SEK_pair.fillna(False).all())
        rawok=bool(complete and positive and same_ccy and dates and pair and .99<=ratio<=1.01 and spread<.001)
        fund_month.append(dict(FI_fund_id=fid,ym=str(per),expected_active_classes=len(active),observed_active_classes=len(z),active_class_ids=';'.join(sorted(active.performanceid)),all_active_present=complete,positive_capital=positive,allSEK=same_ccy,common_actual_capital_date=bool(dates),all_class_TNA_TRI_pairs=pair,capital_reconciliation_pass=bool(np.isfinite(ratio) and .99<=ratio<=1.01),repeated_fund_TNA_pass=bool(np.isfinite(spread) and spread<.001),provisional_source_month_pass=rawok))
FM=pd.DataFrame(fund_month);FM.to_csv(O/'FUND_MONTH_SOURCE_FLAGS.csv',index=False)
history=[]
for year in range(2019,2024):
    for half,end in [('H1',f'{year}-03'),('H2',f'{year}-09')]:
        review=f'{year}{half}';months=set(map(str,pd.period_range(pd.Period(end)-24,pd.Period(end),freq='M')))
        for fid,cl in M.groupby('FI_fund_id'):
            row=dict(review=review,FI_fund_id=fid,fundid=cl.fundid.iloc[0],first_month=min(months),last_month=max(months))
            for source,d in [('old',OLD),('new',N)]:
                s=d[d.performanceid.isin(cl.performanceid)&d.ym.isin(months)]
                for f in ['tnaclass_present','tnafund_present','tri_present','representative_SEK_pair']:
                    count=s.loc[s[f].fillna(False).astype(bool)].groupby('performanceid').ym.nunique()
                    row[source+'_'+f+'_classes25']=int(count.eq(25).sum())
            q=FM[FM.FI_fund_id.eq(fid)&FM.ym.isin(months)]
            row['new_all_active_months_pass']=int(q.provisional_source_month_pass.sum());row['new_active_class_set_stable']=q.active_class_ids.nunique()==1
            row['new_strict25endpoint_metadata_pass']=bool(len(q)==25 and q.provisional_source_month_pass.all() and row['new_active_class_set_stable'])
            row['new_one_class_repaired']=row['old_representative_SEK_pair_classes25']==0 and row['new_representative_SEK_pair_classes25']>0
            history.append(row)
H=pd.DataFrame(history);H.to_csv(O/'FUND_24MONTH_SOURCE_HISTORY_OLD_NEW.csv',index=False)
summary={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'metadata_only':True,'no_returns_flows_or_covariance_computed':True,'download_paths':[str(args.valuations),str(args.rips)],'duplicate_class_date_groups':len(dups),'conflicting_duplicate_groups':sum(bool(x['conflicting_columns']) for x in dups),'classes_requested':len(M),'new_classes_with_any_positive_TNA':int(N[N.tnaclass_present.fillna(False)].performanceid.nunique()),'new_classes_with_any_positive_TRI':int(N[N.tri_present.fillna(False)].performanceid.nunique()),'fund_review_rows':len(H),'old_one_representative_SEKclass25_rows':int(H.old_representative_SEK_pair_classes25.gt(0).sum()),'new_one_representative_SEKclass25_rows':int(H.new_representative_SEK_pair_classes25.gt(0).sum()),'new_strict_allactive25_rows':int(H.new_strict25endpoint_metadata_pass.sum()),'limitations':['Five selected funds only; not universecapitalcoverage.','Representative shareclassTNA+TRI is not exact aggregatefundflow.','Master inception/obsolete dates do not certify mergerhistory or exhaustive historicclasslist.','Fourday gap is preliminary metadata tolerance, not verifiedsameNAVdate.','Complete recorded NF does not prove complete calendarcoverage.','Strict allactive gate remains provisional and has not been relaxed to obtain economicresults.']}
(O/'SOURCE_HISTORY_COMPARISON.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(H.to_string(index=False))
