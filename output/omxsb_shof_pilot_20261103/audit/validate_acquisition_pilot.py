"""Validate downloaded five-fund sources by metadata only; no flow/return estimates.
Usage: python validate_acquisition_pilot.py --valuations FILE --rips FILE
FILE may be CSV or a ZIP containing exactly one CSV. Writes only this script folder.
"""
from pathlib import Path
import argparse,zipfile,io,hashlib,datetime,json
import pandas as pd
import numpy as np

O=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--valuations',type=Path);ap.add_argument('--rips',type=Path);args=ap.parse_args()
if not args.valuations and not args.rips:ap.error('Provide at least one downloaded source.')
M=pd.read_csv(O/'ACQUISITION_PILOT_CLASSES.csv',dtype=str);want=set(M.performanceid)
paths=[p for p in [args.valuations,args.rips] if p]
lock={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Presence/dates/currencies/duplicate metadata only. No flow arithmetic, returns, covariance or economic analysis. Exact20class pilot,2017..2023 only.','files':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(O/'PILOT_ACQUISITION_VALIDATION_LOCK.json').write_text(json.dumps(lock,indent=2))

def read_source(p):
    if zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z:
            names=[n for n in z.namelist() if n.lower().endswith('.csv')]
            if len(names)!=1:raise ValueError(f'Expected one CSV, got {names}')
            b=z.read(names[0])
    else:b=p.read_bytes()
    first=b.decode('utf-8-sig').splitlines()[0]
    sep=';' if first.count(';')>first.count(',') else ','
    d=pd.read_csv(io.BytesIO(b),sep=sep,dtype=str,encoding='utf-8-sig')
    d.columns=[str(c).strip().lower() for c in d.columns]
    if not {'performanceid','date'}<=set(d):raise ValueError('Missing performanceid/date')
    d.date=d.date.str.slice(0,10)
    outside_ids=int((~d.performanceid.isin(want)).sum())
    outside_dates=int((~d.date.between('2017-01-01','2023-12-31')).sum())
    d=d[d.performanceid.isin(want)&d.date.between('2017-01-01','2023-12-31')].copy()
    d['ym']=d.date.str.slice(0,7)
    return d,{'unexpected_id_rows_ignored':outside_ids,'outside_2017_2023_rows_ignored':outside_dates,'columns':list(d.columns)}

results={}
for kind,p in [('valuations',args.valuations),('rips',args.rips)]:
    if not p:continue
    d,meta=read_source(p)
    fields=['tnaclass','tnafund','netflowclass','netflowfund','shares'] if kind=='valuations' else ['unit_sek','unit_bas']
    if kind=='rips':
        if 'returntype' not in d:raise ValueError('RIPS needs returntype; cannot assume total return')
        meta['returntypes_in_filtered_source']=d.returntype.value_counts().to_dict()
        d=d[d.returntype.isin(['1','1.0'])].copy()
    missing=[c for c in fields if c not in d]
    rows=[]
    for (pid,ym),g in d.groupby(['performanceid','ym']):
        r={'performanceid':pid,'ym':ym,'rows':len(g),'distinct_dates':g.date.nunique(),'first_record':g.date.min(),'last_record':g.date.max(),'duplicate_id_date_rows':int(g.duplicated(['performanceid','date'],keep=False).sum())}
        for field in fields:
            if field not in g:
                r[field+'_observations']=None;r[field+'_first_date']=None;r[field+'_last_date']=None;continue
            if field.startswith('netflow'):
                present=g[field].notna()&~g[field].isin(['','NULL','NaN','nan','NA'])
            else:
                num=pd.to_numeric(g[field],errors='coerce');present=num.notna()&np.isfinite(num)&num.gt(0)
            dates=g.loc[present,'date'];r[field+'_observations']=int(present.sum());r[field+'_first_date']=dates.min() if len(dates) else None;r[field+'_last_date']=dates.max() if len(dates) else None
        if kind=='valuations':
            for field in ['classcurrencyiso','fundcurrencyiso']:
                r[field]=';'.join(sorted(g[field].dropna().unique())) if field in g else None
        rows.append(r)
    q=pd.DataFrame(rows);q.to_csv(O/f'PILOT_{kind.upper()}_MONTH_METADATA.csv',index=False)
    cls=d.groupby('performanceid').agg(rows=('date','size'),first_date=('date','min'),last_date=('date','max'),months=('ym','nunique')).reset_index()
    cls=M[['FI_fund_id','fundid','performanceid','ISIN','inceptiondate','obsoletedate']].merge(cls,on='performanceid',how='left')
    cls['rows']=cls.rows.fillna(0).astype(int);cls['months']=cls.months.fillna(0).astype(int)
    cls.to_csv(O/f'PILOT_{kind.upper()}_CLASS_METADATA.csv',index=False)
    meta.update({'rows':len(d),'classes_present':d.performanceid.nunique(),'requested_classes':len(want),'classes_without_pre2024_records':cls.loc[cls.rows.eq(0),'performanceid'].tolist(),'missing_expected_columns':missing,'no_numeric_netflows_or_returns_computed':True})
    results[kind]=meta
results['limitation']='This checks source presence only. Positive capital and TRI at dates are not proof of clean fund identity, complete capital reconciliation, same NAV date, merger treatment or usable flows. A class formed after2023 appropriately has no pilot records.'
(O/'PILOT_ACQUISITION_VALIDATION.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
