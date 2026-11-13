"""Two user-authorized discovery searches; no additional constituent requests."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,signal
import lseg.data as ld
O=Path(__file__).resolve().parent;P=O/'private'
queries=['Stockholm Benchmark','Stockholmsbörsens Benchmark']
def now():return datetime.now(timezone.utc).isoformat()
def dump(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
assert not (O/'METADATA_FOLLOWUP_LOCK.json').exists()
dump('METADATA_FOLLOWUP_LOCK.json',{'created_utc':now(),'queries':queries,
 'view':'IndexQuotes','select':'RIC,DocumentTitle','top':30,
 'inactive_inclusion_parameter':None,
 'inactive_coverage_not_claimed':'No documented inactive switch was established; no invented filter was supplied.',
 'additional_constituent_queries_permitted':False,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
def timeout(a,b):raise TimeoutError('45 second metadata timeout')
signal.signal(signal.SIGALRM,timeout);rows=[];opened=False
try:
 signal.alarm(45);s=ld.open_session();signal.alarm(0);opened=True
 assert 'desktop' in (type(s).__module__+'.'+type(s).__name__).lower()
 for n,q in enumerate(queries,1):
  row={'query':q,'started_utc':now()}
  try:
   signal.alarm(45)
   d=ld.discovery.search(view=ld.discovery.Views.INDEX_QUOTES,query=q,select='RIC,DocumentTitle',top=30)
   signal.alarm(0)
   p=P/f'metadata_followup_{n:02}.csv';d.to_csv(p,index=False)
   row.update(status='response',rows=len(d),columns=list(d.columns),private_file=str(p.relative_to(O)),
     sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
     exact_verified_uncapped_identities=[dict(RIC=str(r.RIC),DocumentTitle=str(r.DocumentTitle))for r in d.itertuples() if str(r.RIC) in ['.OMXSBPI','.OMXSBGI']],
     SBX_or_SAXB_label_rows=int(d.astype(str).apply(lambda c:c.str.contains(r'\b(?:SBX|SAXB)\b',regex=True,case=False)).any(axis=1).sum()))
  except Exception as e:
   signal.alarm(0);row.update(status='error',error_type=type(e).__name__,error=str(e)[:500])
  row['finished_utc']=now();rows.append(row);dump('METADATA_FOLLOWUP_RESULTS.json',{'requests':rows,'finished':False});print(json.dumps(row,ensure_ascii=False),flush=True)
finally:
 if opened:ld.close_session()
 dump('METADATA_FOLLOWUP_RESULTS.json',{'requests':rows,'finished':True,'finished_utc':now(),
  'local_library_session_closed':opened,'no_historical_alias_verified_by_absence':True,
  'additional_constituent_requests':0})
