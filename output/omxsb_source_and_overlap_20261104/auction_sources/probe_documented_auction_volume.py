"""Two source-presence requests through an authorized default Desktop session.

Public LSEG support documents TR.ClosingAuctionVolume. No invented price field,
secret/config discovery, quote contrast, or inference. Raw output stays private.
"""
from pathlib import Path
import datetime as dt
import hashlib, importlib.metadata, inspect, json, signal
import lseg.data as ld
import pandas as pd

P=Path(__file__).resolve().parent
PRIVATE=P/'private';PRIVATE.mkdir(exist_ok=True)
Q=[('BILIa.ST','2019-05-31'),('CAMX.ST','2023-11-30')]
FIELDS=['TR.ClosingAuctionVolume.date','TR.ClosingAuctionVolume']
LOCK={'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'source':'https://community.developers.lseg.com/discussion/101276/how-can-i-pull-historical-ticker-level-closing-auction-volume-in-refinitiv-eikon-excel',
      'purpose':'Source presence only through documented historical auction-volume field, not price replacement.',
      'request_limit':2,'requests':[{'universe':[r],'fields':FIELDS,'parameters':{'SDate':d,'EDate':d,'Frq':'D'}} for r,d in Q],
      'no_economic_outcomes':True,'no_credentials_supplied_or_read':True,'no_other_endpoint_probe':True}
(P/'SOURCE_PILOT_LOCK.json').write_text(json.dumps(LOCK,indent=2)+'\n')
R={'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'sdk_version':importlib.metadata.version('lseg-data'),
   'sdk_source_path':inspect.getfile(ld),'session_method':'ld.open_session() default, no supplied key or credentials',
   'requests':[],'client_session_closed':False}
def save(): (P/'SOURCE_PILOT_RESULT.json').write_text(json.dumps(R,indent=2)+'\n')
def timeout(*a): raise TimeoutError('60-second source request limit')
signal.signal(signal.SIGALRM,timeout)
opened=False
try:
    save();signal.alarm(60);s=ld.open_session();signal.alarm(0);opened=True
    R['session_class']=type(s).__module__+'.'+type(s).__name__
    if 'desktop' not in R['session_class'].lower():
        R['session_status']='unexpected_nondesktop_no_requests';raise RuntimeError('Only default Desktop allowed')
    R['session_status']='open_desktop';save()
    print('Default Desktop session open; at most two documented-field source requests.',flush=True)
    for i,request in enumerate(LOCK['requests'],1):
        a={'request_number':i,'request':request,'started_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
        try:
            signal.alarm(60);f=ld.get_data(**request);signal.alarm(0)
            if f is None: a['status']='no_dataframe'
            else:
                path=PRIVATE/f'auction_volume_pilot_{i}.csv';f.to_csv(path,index=False)
                coverage={}
                for c in f.columns:
                    x=f[c];nonempty=x.notna()&x.astype(str).str.strip().ne('')
                    nums=pd.to_numeric(x.where(nonempty),errors='coerce')
                    # Datetime64 NaT may cast to a finite sentinel integer; do not
                    # classify dates/identifiers as numeric auction observations.
                    finite=int((nonempty&nums.notna()&nums.abs().lt(float('inf'))).sum()) if str(c)=='Closing Auction Volume' else None
                    coverage[str(c)]={'nonempty':int(nonempty.sum()),'finite_numeric':finite}
                date_columns=[c for c in f.columns if 'date' in str(c).lower()]
                dates=sorted({str(x) for c in date_columns for x in f[c].dropna().tolist()})
                a.update(status='response',rows=len(f),columns=[str(x) for x in f.columns],coverage=coverage,
                         dates_returned=dates,private_file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        except Exception as e:
            signal.alarm(0);a.update(status='request_error',error_type=type(e).__name__,error=str(e)[:600])
        R['requests'].append(a);save();print(json.dumps(a),flush=True)
except Exception as e:
    signal.alarm(0);R['session_status']=R.get('session_status','open_failed')
    R['outer_error_type']=type(e).__name__;R['outer_error']=str(e)[:600]
finally:
    signal.alarm(0)
    if opened:
        ld.close_session();R['client_session_closed']=True
    R['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat();save()
    print(json.dumps({'session_status':R['session_status'],'requests_attempted':len(R['requests']),'client_session_closed':R['client_session_closed']}),flush=True)
