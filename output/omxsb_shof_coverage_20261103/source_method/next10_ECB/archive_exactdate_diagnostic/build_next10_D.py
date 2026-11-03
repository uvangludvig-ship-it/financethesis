"""Next10 source gate using a fixed ECB conversion source. No economic outcomes."""
from pathlib import Path
import pandas as pd,numpy as np,zipfile,io,json,datetime,hashlib,argparse
O=Path(__file__).resolve().parent;C=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke')
ap=argparse.ArgumentParser();ap.add_argument('--valuations',type=Path,required=True);ap.add_argument('--rips',type=Path,required=True);args=ap.parse_args()
MP=C/'work/shof_coverage_20261103/audit/NEXT10_ACQUISITION_CLASSES.csv';FP=C/'work/shof_coverage_20261103/root/ECB_FX_SEK_201612_202312.csv';FS=C/'work/shof_coverage_20261103/root/ECB_FX_SOURCE.json'
inputs=[args.valuations,args.rips,MP,FP,FS,O/'RULE_LOCK.txt',Path(__file__)]
(O/'INPUT_LOCK.json').write_text(json.dumps(dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Sourcepresence and convertedcapitalreconciliation ONLY. No return/flow/covariance.',inputs={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}),indent=2))
def readzip(p,cols):
 with zipfile.ZipFile(p) as z:
  ns=[n for n in z.namelist() if n.lower().endswith('.csv')];assert len(ns)==1
  d=pd.read_csv(io.BytesIO(z.read(ns[0])),sep=';',usecols=lambda x:x.lower() in cols,dtype=str)
 d.columns=d.columns.str.lower();d.date=pd.to_datetime(d.date.str[:10]);return d[d.date.between('2017-01-01','2023-12-31')]
M=pd.read_csv(MP,dtype=str);M=M.rename(columns={'fund_id':'FI_fund_id'});M['inc']=pd.to_datetime(M.inceptiondate);M['obs']=pd.to_datetime(M.obsoletedate)
assert not M.secid.duplicated().any();assert not M.performanceid.duplicated().any()
V=readzip(args.valuations,{'performanceid','secid','date','classcurrencyiso','fundcurrencyiso','tnaclass','tnafund'})
T=readzip(args.rips,{'performanceid','secid','date','returntype','unit_sek'});T=T[T.returntype.isin(['1','1.0'])]
assert set(V.performanceid)<=set(M.performanceid);assert set(T.performanceid)<=set(M.performanceid)
assert not V.duplicated(['performanceid','date']).any();assert not T.duplicated(['performanceid','date']).any()
secmap=M.set_index('performanceid').secid.to_dict()
for z in [V,T]:
 assert z.secid.eq(z.performanceid.map(secmap)).all(),'SecId mismatch or missing identity'
for col in ['tnaclass','tnafund']:V[col]=pd.to_numeric(V[col],errors='coerce')
tri=set(map(tuple,T.loc[pd.to_numeric(T.unit_sek,errors='coerce').gt(0),['performanceid','date']].to_numpy()))
FX=pd.read_csv(FP);FX.date=pd.to_datetime(FX.date);assert not FX.date.duplicated().any();FX=FX.set_index('date')
def rate(ccy,date):
 if ccy=='SEK':return 1.
 col=ccy+'SEK'
 if col not in FX or date not in FX.index:return None
 x=FX.loc[date,col];return float(x) if pd.notna(x) and x>0 else None
V=V.merge(M[['performanceid','FI_fund_id','inc']],on='performanceid',validate='m:1')
contradictions=V[V.tnaclass.gt(0)&V.date.lt(V.inc)][['FI_fund_id','performanceid','date','inc']]
contradictions.to_csv(O/'PREINCEPTION_CLASS_CAPITAL_FLAGS.csv',index=False)
endpoints=[]
for fid,classes in M.groupby('FI_fund_id'):
 vv=V[V.FI_fund_id.eq(fid)]
 for mo in pd.period_range('2017-01','2023-12',freq='M'):
  end=mo.end_time.normalize();active=classes[classes.inc.le(end)&(classes.obs.isna()|classes.obs.ge(end))];needed=set(active.performanceid)
  row=dict(FI_fund_id=fid,month=str(mo),active_class_ids=';'.join(sorted(needed)),active_classes=len(needed),source_date=None,uses_reference_FX=False,capital_reconciliation_pass=False,fund_TNA_same_currency_copies_pass=False,pass_source=False,reason='no_common_TNA_RIP_FX_date_within4days')
  badinc=contradictions[contradictions.FI_fund_id.eq(fid)&contradictions.date.between(mo.start_time,mo.end_time)]
  if len(badinc):row['reason']='positive_class_capital_before_master_inception';endpoints.append(row);continue
  found=None
  for date in sorted(vv.loc[vv.date.between(end-pd.Timedelta(days=4),end),'date'].unique(),reverse=True):
   date=pd.Timestamp(date)
   if (active.inc>date).any():continue
   z=vv[vv.date.eq(date)&vv.performanceid.isin(needed)].copy()
   if not needed or set(z.performanceid)!=needed or not z.tnaclass.gt(0).all():continue
   if any((pid,date) not in tri for pid in needed):continue
   if any(rate(ccy,date) is None for ccy in z.classcurrencyiso):continue
   if not any(a.tnafund>0 and rate(a.fundcurrencyiso,date) is not None for a in z.itertuples()):continue
   # First joint source-date chosen before the capital reconciliation.
   found=(date,z);break
  if found:
   date,z=found;row['source_date']=str(date.date());row['uses_reference_FX']=not bool(z.classcurrencyiso.eq('SEK').all())
   converted=z.apply(lambda a:a.tnaclass*rate(a.classcurrencyiso,date),axis=1)
   f=None
   for ccy in ['SEK','EUR','NOK']:
    q=z.loc[z.tnafund.gt(0)&z.fundcurrencyiso.eq(ccy),'tnafund'];r=rate(ccy,date)
    if len(q) and r is not None:f=q*r;row['fund_TNA_reference_currency']=ccy;break
   if f is None:row['reason']='no_contemporaneous_fund_TNA_in_supported_currency'
   else:
    den=f.median();row['capital_reconciliation_pass']=bool(.99<=converted.sum()/den<=1.01);row['fund_TNA_same_currency_copies_pass']=bool((f.max()-f.min())/den<.001)
    row['pass_source']=row['capital_reconciliation_pass'] and row['fund_TNA_same_currency_copies_pass'];row['reason']='pass' if row['pass_source'] else ('capital_reconciliation' if not row['capital_reconciliation_pass'] else 'fund_TNA_duplicate_conflict')
  endpoints.append(row)
E=pd.DataFrame(endpoints);E.to_csv(O/'NEXT10_D_ENDPOINT_SOURCE_FLAGS.csv',index=False)
rows=[]
for year in range(2019,2024):
 for half,m in [('H1',3),('H2',9)]:
  last=pd.Period(f'{year}-{m:02d}',freq='M');first=last-24
  for fid,cl in M.groupby('FI_fund_id'):
   z=E[E.FI_fund_id.eq(fid)&E.month.between(str(first),str(last))];assert len(z)==25
   entrants=cl[cl.inc.gt(first.end_time)&cl.inc.le(last.end_time)]
   rows.append(dict(review=f'{year}{half}',FI_fund_id=fid,fundid=cl.fundid.iloc[0],first_endpoint_month=str(first),last_endpoint_month=str(last),D_RIPS_ECB_source_supported=bool(z.pass_source.all()),valid_endpoints=int(z.pass_source.sum()),uses_reference_FX=bool(z.uses_reference_FX.any()),new_entry_class_ids=';'.join(sorted(entrants.performanceid)),D_provisional_current_master=True,D_dated_lineage_verified=False,historical_class_universe_fully_certified=False,conditional_NAV_used=False,failure_reasons=';'.join(f'{r.month}:{r.reason}' for r in z[~z.pass_source].itertuples())))
S=pd.DataFrame(rows);S.to_csv(O/'NEXT10_D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv',index=False)
summary=S.groupby('FI_fund_id').D_RIPS_ECB_source_supported.sum().astype(int).to_dict()
(O/'SUMMARY.json').write_text(json.dumps(dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_only=True,classes_requested=len(M),funds_requested=M.FI_fund_id.nunique(),windows=len(S),passing_windows=int(S.D_RIPS_ECB_source_supported.sum()),byfund=summary,preinception_positive_class_capital_rows=len(contradictions),RIPS_present_classes=T.performanceid.nunique(),valuations_present_classes=V.performanceid.nunique(),ECB_referenceFX_not_NAVprovider_fixing=True,no_missing_FX_filled=True,no_returns_flows_covariances=True,eligibility_SHA256=hashlib.sha256((O/'NEXT10_D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv').read_bytes()).hexdigest()),indent=2))
print(json.dumps(summary,indent=2));print('Total',S.D_RIPS_ECB_source_supported.sum(),'of',len(S))
