"""Availability-only minute-history check on the fixed 2023 pilot dates."""
from pathlib import Path
import datetime as dt
import json, hashlib, signal
import lseg.data as ld
import pandas as pd
ROOT=Path(__file__).resolve().parent
PRIVATE=ROOT/'private'
REQUESTS=[dict(universe=ric, start=day+'T00:00:00', end=day+'T23:59:59',
               interval='1min', adjustments=['unadjusted'])
          for ric in ['CAMX.ST','AFRY.ST'] for day in ['2023-11-23','2023-11-30']]
LOG=dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
         request_plan=REQUESTS, requests=[], economic_outcomes_computed=False,
         purpose='source availability for fixed 2023 events, no stock/date/window replacement')
def save():
    (ROOT/'MINUTE_2023_ATTEMPTS.json').write_text(json.dumps(LOG,indent=2)+'\n')
def timeout(signum,frame):
    raise TimeoutError('Source check exceeded 60 seconds')
signal.signal(signal.SIGALRM,timeout)
save()
signal.alarm(60)
s=ld.open_session()
signal.alarm(0)
assert 'desktop' in type(s).__module__.lower()
for n,request in enumerate(REQUESTS,1):
    r=dict(request=request,utc=dt.datetime.now(dt.timezone.utc).isoformat())
    try:
        signal.alarm(60)
        frame=ld.get_history(**request)
        signal.alarm(0)
        if frame is None: r['status']='no_dataframe'
        else:
            p=PRIVATE/f'minute_2023_{n}.csv'
            frame.to_csv(p,index=True)
            r.update(status='source_response_requires_validation', rows=len(frame),
                     columns=[str(c) for c in frame.columns],
                     numeric_nonmissing={str(c):int(pd.to_numeric(frame[c],errors='coerce').notna().sum()) for c in frame.columns},
                     first_index=str(frame.index[0]) if len(frame) else None,
                     last_index=str(frame.index[-1]) if len(frame) else None,
                     sha256=hashlib.sha256(p.read_bytes()).hexdigest(),private_file=p.name)
    except Exception as e:
        signal.alarm(0)
        r.update(status='error',error_type=type(e).__name__,error=str(e)[:650])
    LOG['requests'].append(r);save();print(json.dumps(r),flush=True)
LOG['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat();save()
