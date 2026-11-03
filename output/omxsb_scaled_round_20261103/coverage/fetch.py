"""Execute frozen source requests. All licensed values stay in private/.

The output is field presence by stock/date, never an economic effect estimate.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,signal,csv
import pandas as pd
import lseg.data as ld
OUT=Path(__file__).resolve().parent
PRIVATE=OUT/'private';PRIVATE.mkdir(exist_ok=True)
lock=json.loads((OUT/'SOURCE_REQUEST_LOCK.json').read_text())
log={'started_utc':datetime.now(timezone.utc).isoformat(),
     'lock_sha256':hashlib.sha256((OUT/'SOURCE_REQUEST_LOCK.json').read_bytes()).hexdigest(),
     'economic_outcomes_computed':False,'requests':[]}
presence=[]
def save():
    (OUT/'FETCH_LOG.json').write_text(json.dumps(log,indent=2)+'\n')
    if presence:
        with (OUT/'SOURCE_PRESENCE.csv').open('w',newline='')as f:
            w=csv.DictWriter(f,fieldnames=list(presence[0]));w.writeheader();w.writerows(presence)
def timeout(signum,frame):raise TimeoutError('Source request exceeded60seconds')
signal.signal(signal.SIGALRM,timeout);save()
signal.alarm(60);session=ld.open_session();signal.alarm(0)
assert 'desktop' in type(session).__module__.lower()
for n,req in enumerate(lock['requests'],1):
    meta=dict(number=n,request=req,started_utc=datetime.now(timezone.utc).isoformat())
    frame=None
    try:
        signal.alarm(60)
        frame=ld.get_history(universe=req['universe'],fields=lock['fields_requested'],
                             start=req['date'],end=req['date'],interval='1D',adjustments=['unadjusted'])
        signal.alarm(0)
        if frame is None:meta['status']='no_dataframe'
        else:
            path=PRIVATE/f'request_{n:03d}.csv'
            frame.to_csv(path,index=True)
            meta.update(status='source_response',rows=len(frame),
                        columns=[list(c)if isinstance(c,tuple)else str(c)for c in frame.columns],
                        index=[str(i)for i in frame.index],
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),private_file=path.name)
    except Exception as e:
        signal.alarm(0);meta.update(status='source_error',error_type=type(e).__name__,error=str(e)[:700])
    for ric in req['universe']:
        row=dict(review=req['review'],date=req['date'],role=req['role'],RIC=ric,
                 response_status=meta['status'],exact_requested_date=False,
                 CLS_AUC_finite=0,CLS_AUCVOL_finite=0,TRDPRC_1_finite=0)
        if frame is not None and len(frame):
            dates=[pd.Timestamp(i).strftime('%Y-%m-%d') for i in frame.index]
            row['exact_requested_date']=len(dates)==1 and dates[0]==req['date']
            for field in lock['fields_requested']:
                if isinstance(frame.columns,pd.MultiIndex):
                    key=(ric,field)
                    values=frame[key] if key in frame.columns else pd.Series(dtype=float)
                else:
                    values=frame[field] if len(req['universe'])==1 and field in frame.columns else pd.Series(dtype=float)
                numeric=pd.to_numeric(values,errors='coerce')
                row[field+'_finite']=int(numeric.map(lambda x:pd.notna(x)and float('-inf')<x<float('inf')).sum())
        presence.append(row)
    log['requests'].append(meta);save()
    print(json.dumps({'request':n,'total':len(lock['requests']),'review':req['review'],
                      'date':req['date'],'status':meta['status'],
                      'securities':len(req['universe']),
                      'auction_fields_present':sum(r['CLS_AUC_finite']>0 for r in presence if r['review']==req['review']and r['date']==req['date'])}),flush=True)
log['finished_utc']=datetime.now(timezone.utc).isoformat();save()
