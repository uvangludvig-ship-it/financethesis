"""Eight locked index-membership requests; no weights, prices or returns.
Authorized local Workspace desktop session only. No credentials/config search.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, importlib.metadata, json, signal
import lseg.data as ld

O=Path(__file__).resolve().parent
P=O/'private';P.mkdir(exist_ok=True)
I=O.parents[1]/'alternative_execution_20261103/index_sources/private/identity_search_1.csv'
FIELDS=['TR.IndexConstituentRIC','TR.IndexConstituentName']
DATES=['2000-12-29','2003-12-30','2006-12-29','2023-11-30']
INDEXES=['.OMXSBPI','.OMXSBGI']
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj):(O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
with I.open() as f:identities=list(csv.DictReader(f))
for index in INDEXES:
    expected=f"OMX Stockholm Benchmark_{index[-2:]}, Equity Index, NASDAQ Stockholm AB"
    assert any(r['RIC']==index and r['DocumentTitle']==expected for r in identities)
queries=[{'index':idx,'date':date,'fields':FIELDS,'parameters':{'SDate':date.replace('-','')}}
         for date in DATES for idx in INDEXES]
lock={'created_utc':now(),'purpose':'source-presence and dated membership only',
 'queries':queries,'source_identity_sha256':sha(I),'script_sha256':sha(Path(__file__)),
 'fixed_positive_membership_control':'2023-11-30: prior verified .OMXSBPI 105 members',
 'membership_does_not_identify_announcement_or_live_launch':True,
 'no_new_aliases_no_query_grid':True,'raw_publication':False}
if (O/'PILOT_LOCK.json').exists():raise RuntimeError('Do not overwrite frozen pilot')
dump('PILOT_LOCK.json',lock)
result={'started_utc':now(),'library_version':importlib.metadata.version('lseg-data'),
        'session_method':'ld.open_session() without arguments','requests':[]}
def timeout(a,b):raise TimeoutError('45 second bounded source-pilot timeout')
signal.signal(signal.SIGALRM,timeout)
opened=False
try:
    signal.alarm(45);session=ld.open_session();signal.alarm(0);opened=True
    result['session_class']=type(session).__module__+'.'+type(session).__name__
    if 'desktop' not in result['session_class'].lower():raise RuntimeError('Not a DesktopSession; no data calls permitted')
    result['session_status']='open_desktop';dump('PILOT_RESULTS.json',result)
    for n,q in enumerate(queries,1):
        row=dict(q,started_utc=now(),request_number=n)
        try:
            signal.alarm(45)
            d=ld.get_data(universe=[q['index']],fields=q['fields'],parameters=q['parameters'])
            signal.alarm(0)
            if d is None:row['status']='no_dataframe'
            else:
                p=P/f'request_{n:02}.csv';d.to_csv(p,index=False)
                nonempty={str(c):int((d[c].notna()&d[c].astype(str).str.strip().ne('')).sum())for c in d.columns}
                candidates=[c for c in d.columns if 'constituent' in str(c).lower() and 'ric' in str(c).lower()]
                if len(candidates)!=1:
                    row.update(status='schema_requires_review',rows=len(d),columns=list(d.columns),nonempty_counts=nonempty)
                else:
                    c=candidates[0];values=d.loc[d[c].notna()&d[c].astype(str).str.strip().ne(''),c].astype(str).str.strip()
                    names=[c for c in d.columns if 'constituent' in str(c).lower() and 'name' in str(c).lower()]
                    row.update(status='response',rows=len(d),columns=list(d.columns),nonempty_counts=nonempty,
                      valid_member_rows=len(values),unique_member_RICs=values.nunique(),
                      duplicate_member_rows=len(values)-values.nunique(),
                      membership_sha256=hashlib.sha256('\n'.join(sorted(set(values))).encode()).hexdigest())
                row.update(private_file=str(p.relative_to(O)),sha256=sha(p))
        except Exception as e:
            signal.alarm(0);row.update(status='error',error_type=type(e).__name__,error=str(e)[:600])
        row['finished_utc']=now();result['requests'].append(row);dump('PILOT_RESULTS.json',result)
        print(json.dumps(row,ensure_ascii=False),flush=True)
except Exception as e:
    signal.alarm(0);result.update(session_status='failed',error_type=type(e).__name__,error=str(e)[:600])
finally:
    if opened:
        try:ld.close_session();result['local_library_session_closed']=True
        except Exception as e:result['local_close_error']=type(e).__name__
    result['finished_utc']=now();result['economic_outcomes_computed']=False
    result['user_desktop_logout_called']=False;dump('PILOT_RESULTS.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='requests'},ensure_ascii=False),flush=True)
