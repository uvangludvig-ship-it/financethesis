"""Authorized desktop-session execution of the unchanged nine-request pilot.
No supplied app key or platform credentials. No secret/config discovery.
Raw responses stay in private/. Only request status and counts are printed.
"""
from pathlib import Path
import datetime, json, signal, importlib.metadata, hashlib, argparse
import lseg.data as ld

O = Path(__file__).resolve().parent
P = O / 'private'
P.mkdir(exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument('--verified-index-repair', action='store_true')
args = parser.parse_args()
INDEX = '.OMXSBPI' if args.verified_index_repair else '.OMXSB'
LOGFILE = 'DESKTOP_REPAIRED_ATTEMPT.json' if args.verified_index_repair else 'DESKTOP_ATTEMPT.json'
PREFIX = 'repaired_' if args.verified_index_repair else ''
if args.verified_index_repair:
    import pandas as pd
    identities = pd.read_csv(P / 'identity_search_1.csv')
    assert identities.loc[identities.RIC.eq(INDEX),'DocumentTitle'].eq(
        'OMX Stockholm Benchmark_PI, Equity Index, NASDAQ Stockholm AB').any()
R = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'library_version': importlib.metadata.version('lseg-data'),
     'session_method': 'ld.open_session() with no supplied arguments',
     'supplied_app_key': False, 'credential_search': False,
     'index': INDEX, 'dates': ['2023-11-30', '2023-12-01'], 'requests': [],
     'verified_identifier_repair': args.verified_index_repair}

def save():
    (O / LOGFILE).write_text(json.dumps(R, indent=2))

def timeout(signum, frame):
    raise TimeoutError('Bounded source-pilot call exceeded 60 seconds')

signal.signal(signal.SIGALRM, timeout)
save()
try:
    signal.alarm(60)
    session = ld.open_session()
    signal.alarm(0)
    R['session_class'] = type(session).__module__ + '.' + type(session).__name__
    if 'desktop' not in R['session_class'].lower():
        raise RuntimeError('Returned session is not identified as Desktop; no data call executed')
    R['session_status'] = 'open_desktop'
except Exception as e:
    signal.alarm(0)
    R.update(session_status='failed', error_type=type(e).__name__, error=str(e)[:700])
    save()
    print(json.dumps({k:v for k,v in R.items() if k!='requests'}, indent=2))
    raise SystemExit(0)
save()
print('Desktop session opened:', R['session_class'], flush=True)

def fetch(label, fields, parameters):
    row = {'label': label, 'fields': fields, 'parameters': parameters,
           'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        signal.alarm(60)
        df = ld.get_data(universe=[INDEX], fields=fields, parameters=parameters)
        signal.alarm(0)
        if df is None:
            row['status'] = 'no_dataframe'
        else:
            path = P / (PREFIX + 'index_pilot_' + label + '.csv')
            df.to_csv(path, index=False)
            row.update(status='response_requires_validation', private_file=path.name,
                       rows=len(df), columns=[str(c) for c in df.columns],
                       nonnull_counts={str(c):int(df[c].notna().sum())for c in df.columns},
                       nonempty_counts={str(c):int((df[c].notna()&df[c].astype(str).str.strip().ne('')).sum())for c in df.columns},
                       sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    except Exception as e:
        signal.alarm(0)
        row.update(status='field_or_content_error', error_type=type(e).__name__, error=str(e)[:500])
    R['requests'].append(row)
    save()
    print(json.dumps(row), flush=True)

fetch('index_identity', ['TR.InstrumentName'], {})
fields = ['TR.IndexConstituentName', 'TR.IndexConstituentWeightPercent',
          'TR.IndexConstituentShares', 'TR.IndexConstituentWeightPercent.date']
for day in R['dates']:
    for number, field in enumerate(fields, 1):
        fetch(day.replace('-', '') + '_field' + str(number),
              ['TR.IndexConstituentRIC', field], {'SDate':day.replace('-', '')})
R['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
R['economic_outcomes_computed'] = False
save()
# Do not close or log out the user's desktop/platform session.
