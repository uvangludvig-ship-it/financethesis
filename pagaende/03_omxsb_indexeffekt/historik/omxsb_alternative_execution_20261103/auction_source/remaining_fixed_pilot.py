"""Check source coverage for the remaining fixed events; never replace a stock.

Daily fields are a source check only. The extra minute request tests availability
for the same Bilia event day, not another outcome or window. No contrast is run.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import signal
import lseg.data as ld
import pandas as pd

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / 'private'
PRIVATE.mkdir(exist_ok=True)
REQUESTS = []
for ric, dates in [
    ('ATRLJb.ST', ['2019-05-23', '2019-05-31']),
    ('CAMX.ST', ['2023-11-23', '2023-11-30']),
    ('AFRY.ST', ['2023-11-23', '2023-11-30']),
]:
    for day in dates:
        REQUESTS.append(dict(universe=ric, start=day, end=day, interval='1D',
                             fields=['CLS_AUC', 'CLS_AUCVOL', 'OFF_CLOSE', 'TRDPRC_1'],
                             adjustments=['unadjusted']))
REQUESTS.append(dict(universe='BILIa.ST', start='2019-05-31T00:00:00',
                     end='2019-05-31T23:59:59', interval='1min',
                     adjustments=['unadjusted']))
LOG = dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
           purpose='fixed-pilot source availability, no outcome replacement or estimates',
           requests_locked=REQUESTS, requests=[], economic_outcomes_computed=False)

def save():
    (ROOT/'REMAINING_ATTEMPTS.json').write_text(json.dumps(LOG, indent=2)+'\n')

def timeout(signum, frame):
    raise TimeoutError('Source request exceeded 60 seconds')

signal.signal(signal.SIGALRM, timeout)
save()
signal.alarm(60)
session=ld.open_session()
signal.alarm(0)
if 'desktop' not in type(session).__module__.lower():
    raise RuntimeError('Only authorized desktop session allowed')
for number, kwargs in enumerate(REQUESTS, 1):
    row=dict(request=kwargs, started_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    try:
        signal.alarm(60)
        frame=ld.get_history(**kwargs)
        signal.alarm(0)
        if frame is None:
            row['status']='no_dataframe'
        else:
            path=PRIVATE/f'remaining_{number}.csv'
            frame.to_csv(path, index=True)
            row.update(status='response_requires_validation', rows=len(frame),
                       columns=[str(c) for c in frame.columns],
                       numeric_nonmissing={str(c):int(pd.to_numeric(frame[c], errors='coerce').notna().sum()) for c in frame.columns},
                       first_index=str(frame.index[0]) if len(frame) else None,
                       last_index=str(frame.index[-1]) if len(frame) else None,
                       sha256=hashlib.sha256(path.read_bytes()).hexdigest(), private_file=path.name)
    except Exception as e:
        signal.alarm(0)
        row.update(status='request_error', error_type=type(e).__name__, error=str(e)[:650])
    LOG['requests'].append(row)
    save()
    print(json.dumps(row), flush=True)
LOG['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
save()
