"""Two bounded metadata searches after .OMXSB failed identifier resolution.
This is not a benchmark/estimand switch. No prices, weights or economic outcomes.
"""
from pathlib import Path
import lseg.data as ld
import json,datetime,signal,hashlib
O=Path(__file__).resolve().parent;P=O/'private';P.mkdir(exist_ok=True)
def timeout(a,b):raise TimeoutError('60 second metadata timeout')
signal.signal(signal.SIGALRM,timeout)
ld.open_session()
rows=[]
for query in ['OMX Stockholm Benchmark','OMXSB']:
 r={'query':query,'view':'IndexQuotes','select':'RIC,DocumentTitle','top':30,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  signal.alarm(60)
  d=ld.discovery.search(view=ld.discovery.Views.INDEX_QUOTES,query=query,select='RIC,DocumentTitle',top=30)
  signal.alarm(0)
  p=P/('identity_search_'+str(len(rows)+1)+'.csv');d.to_csv(p,index=False)
  r.update(status='response',rows=len(d),file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
  print(d.to_string(index=False),flush=True)
 except Exception as e:
  signal.alarm(0);r.update(status='error',type=type(e).__name__,error=str(e)[:500])
 rows.append(r);(O/'IDENTITY_REPAIR_ATTEMPT.json').write_text(json.dumps(rows,indent=2));print(r,flush=True)
