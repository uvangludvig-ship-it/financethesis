"""Metadata-only acquisition selector; source rule in NEXT_ACQUISITION_SOURCE_SPEC.txt."""
from pathlib import Path
import pandas as pd,json,datetime,hashlib
O=Path(__file__).resolve().parent
M=pd.read_csv(O/'PRIORITY_REPAIR_CLASS_IDENTIFIERS.csv',dtype=str);R=pd.read_csv(O/'PRIORITY_REPAIR_TARGETS.csv',dtype={'fund_id':str});exclude={'51331','51482','60087','60302','60824'}
M['inc']=pd.to_datetime(M.inceptiondate,errors='coerce');old=M.groupby('fund_id').inc.min();eligible=set(old[old.le(pd.Timestamp('2017-01-01'))].index)-exclude
T=R[R.fund_id.isin(eligible)].sort_values('rank').head(10)
C=M[M.fund_id.isin(T.fund_id)].drop(columns='inc').sort_values(['rank','fund_id','performanceid']).drop_duplicates(['fund_id','performanceid']);C['request_start']='2017-01-01';C['request_end']='2023-12-31'
C.to_csv(O/'NEXT10_ACQUISITION_CLASSES.csv',index=False);T.to_csv(O/'NEXT10_ACQUISITION_FUNDS.csv',index=False);ids=list(dict.fromkeys(C.performanceid));(O/'NEXT10_ACQUISITION_IDS.txt').write_text(','.join(ids)+'\n')
manifest={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'funds':len(T),'classes':len(ids),'fund_ids_in_priority_order':T.fund_id.tolist(),'selector':'Top remaining B eventrole pooledfixedcapitalgap, excluding five pilotfunds; allchosenfunds have an established class before2017. Diagnosed FX/date/reconciliation/missingexport gaps.','date_start':'2017-01-01','date_end':'2023-12-31','raw_queries':['RIPS daily:performanceId,SecId,date,lastupdate,returntype,unit_SEK,unit_BAS','Valuations daily:performanceId,SecId,date,lastupdate,classcurrencyiso,fundcurrencyiso,tnaclass,tnafund,netflowclass,netflowfund,shares'],'metadata_only':True,'no_new_economic_outcomes_authorized':True,'no_source_availability_guarantee':True,'old_nonpilot_flags_remain_provisional':True,'files':{n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['NEXT_ACQUISITION_SOURCE_SPEC.txt','NEXT10_ACQUISITION_CLASSES.csv','NEXT10_ACQUISITION_FUNDS.csv','NEXT10_ACQUISITION_IDS.txt']}}
(O/'NEXT10_ACQUISITION_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
