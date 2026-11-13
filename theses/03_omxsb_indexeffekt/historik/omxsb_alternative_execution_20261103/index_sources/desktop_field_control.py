"""Two current source-presence controls requested after the frozen index pilot.
No historical substitute, no returns, and no index-demand calculation.
Private raw rows; public output is field coverage and input/output hashes only.
"""
from pathlib import Path
import datetime,hashlib,json,signal
import pandas as pd
import lseg.data as ld
O=Path(__file__).resolve().parent
P=O/'private';P.mkdir(exist_ok=True)
fields=['TR.IndexConstituentRIC','TR.IndexConstituentWeightPercent','TR.IndexConstituentShares']
queries=[('current_SPX_field_control','.SPX'),('current_OMXSBCAPGI_field_control','.OMXSBCAPGI')]
identity=P/'identity_search_1.csv'
idf=pd.read_csv(identity,keep_default_na=False)
cap=idf.loc[idf['RIC'].eq('.OMXSBCAPGI'),'DocumentTitle'].tolist()
assert cap==['OMX Stockholm Benchmark Cap_GI, Equity Index, NASDAQ Stockholm AB'],cap
lock={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'current field-presence diagnostic only; preserve frozen uncapped OMXSB historical pilot','queries':[{'label':l,'universe':u,'fields':fields,'parameters':{}} for l,u in queries],'CAPGI_identity_source_sha256':hashlib.sha256(identity.read_bytes()).hexdigest(),'CAPGI_identity_verified':True,'raw_rows_public':False,'session':'default authenticated desktop; no appkey or credentials read; close_session in finally'}
(O/'FIELD_CONTROL_LOCK.json').write_text(json.dumps(lock,indent=2))
def timeout(a,b): raise TimeoutError('60-second source request limit')
signal.signal(signal.SIGALRM,timeout)
results=[]
session_open=False
try:
 signal.alarm(60);ld.open_session();signal.alarm(0);session_open=True
 for label,ric in queries:
  result={'label':label,'universe':ric,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fields':fields,'parameters':{}}
  try:
   signal.alarm(60);d=ld.get_data(universe=[ric],fields=fields,parameters={});signal.alarm(0)
   f=P/(label+'.csv');d.to_csv(f,index=False)
   counts={}
   for c in d.columns:
    s=d[c];valid=s.notna()&s.astype(str).str.strip().ne('')
    num=pd.to_numeric(s.where(valid),errors='coerce')
    counts[str(c)]={'nonempty':int(valid.sum()),'numeric_finite':int((num.notna()&num.abs().lt(float('inf'))).sum()),'positive':int(num.gt(0).sum()),'zero':int(num.eq(0).sum())}
   result.update(status='response',rows=len(d),columns=list(d.columns),coverage=counts,private_file=f.name,raw_sha256=hashlib.sha256(f.read_bytes()).hexdigest())
  except Exception as exc:
   signal.alarm(0);result.update(status='error',error_type=type(exc).__name__,error=str(exc)[:700])
  results.append(result)
  (O/'FIELD_CONTROL_RESULTS.json').write_text(json.dumps({'session_opened':session_open,'session_closed':False,'requests':results},indent=2))
  print(json.dumps(result),flush=True)
finally:
 signal.alarm(0)
 if session_open: ld.close_session()
 (O/'FIELD_CONTROL_RESULTS.json').write_text(json.dumps({'session_opened':session_open,'session_closed':session_open,'requests':results,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
