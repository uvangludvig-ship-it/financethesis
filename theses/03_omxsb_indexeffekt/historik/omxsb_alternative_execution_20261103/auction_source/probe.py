"""Bounded LSEG auction-source pilot. Licensed values stay in private/.

This checks the existing fixed Bilia source pilot; it does not estimate returns.
The two dates, auction field, and unadjusted units are locked before requests.
"""
from pathlib import Path
import datetime as dt
import hashlib
import importlib.metadata
import json
import signal

import lseg.data as ld
import pandas as pd

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / 'private'
PRIVATE.mkdir(exist_ok=True)
DATES = ['2019-05-23', '2019-05-31']
RIC = 'BILIa.ST'
FIELDS = ['CLS_AUC', 'CLS_AUCVOL', 'OFF_CLOSE', 'TRDPRC_1']
LOG = {
    'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'purpose': 'auction field availability, exact date and raw-price source check only',
    'instrument': RIC,
    'dates': DATES,
    'fields': FIELDS,
    'adjustments': ['unadjusted'],
    'interval': '1D',
    'primary_price_field': 'CLS_AUC',
    'no_fallback': 'OFF_CLOSE and TRDPRC_1 never replace an absent CLS_AUC',
    'economic_outcomes_computed': False,
    'library_version': importlib.metadata.version('lseg-data'),
    'requests': [],
    'sources': [
        'https://community.developers.lseg.com/discussion/30335/how-to-get-closing-trade-price-for-european-markets',
        'https://cdn.refinitiv.com/public/lseg-lib-python-doc/2.0.0.2/book/en/sections/access-layer/access/get-history-function.html',
        'https://community.developers.lseg.com/discussion/132407/issue-with-query',
    ],
}


def save():
    (ROOT / 'ATTEMPTS.json').write_text(json.dumps(LOG, indent=2) + '\n')


def timed_out(signum, frame):
    raise TimeoutError('Source-pilot request exceeded 60 seconds')


signal.signal(signal.SIGALRM, timed_out)
save()  # Persist the whole request plan before opening the session.
signal.alarm(60)
session = ld.open_session()
signal.alarm(0)
LOG['session_class'] = type(session).__module__ + '.' + type(session).__name__
if 'desktop' not in LOG['session_class'].lower():
    raise RuntimeError('Only the authorized local desktop session is allowed')
save()

for date in DATES:
    row = {'date_requested': date, 'started_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        signal.alarm(60)
        frame = ld.get_history(
            universe=RIC, fields=FIELDS, interval='1D',
            start=date, end=date, adjustments=['unadjusted'],
        )
        signal.alarm(0)
        if frame is None:
            row['status'] = 'no_dataframe'
        else:
            path = PRIVATE / (date + '.csv')
            frame.to_csv(path, index=True)
            row.update(
                status='source_response_requires_validation',
                rows=len(frame), columns=[str(c) for c in frame.columns],
                dates_returned=[str(v) for v in frame.index],
                numeric_nonmissing={str(c): int(pd.to_numeric(frame[c], errors='coerce').notna().sum())
                                    for c in frame.columns},
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                private_file=path.name,
            )
    except Exception as exc:
        signal.alarm(0)
        row.update(status='request_error', error_type=type(exc).__name__, error=str(exc)[:650])
    LOG['requests'].append(row)
    save()
    print(json.dumps(row), flush=True)

LOG['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
save()
# End this local client process without logging the user out of Workspace.
