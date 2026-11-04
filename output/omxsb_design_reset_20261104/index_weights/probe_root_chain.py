"""Four fixed source-only questions; no economic outcome or data-driven retry."""
from pathlib import Path
import datetime, hashlib, importlib.metadata, json, signal
import numpy as np
import pandas as pd
import lseg.data as ld

O=Path(__file__).resolve().parent;P=O/'private';P.mkdir(exist_ok=True)
OLD=Path('/Users/ludviguvang/dev/financethesis/output/omxsb_alternative_execution_20261103/index_sources')
OLDPRIVATE=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/alternative_execution_20261103/index_sources/private')
queries=[('FTSE_root_historical_control','0#.FTSE','2023-11-30'),
 ('SPX_root_historical_control','0#.SPX','2023-11-30'),
 ('OMXSBPI_root_before','0#.OMXSBPI','2023-11-30'),
 ('OMXSBPI_root_after','0#.OMXSBPI','2023-12-01')]
fields=['TR.IndexConstituentWeightPercent.date','TR.IndexConstituentWeightPercent','TR.IndexConstituentShares']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
prior_names=['DESKTOP_ATTEMPT.json','DESKTOP_REPAIRED_ATTEMPT.json','ALTERNATIVE_REQUEST_RESULTS.json','GI_DIRECT_SOURCE_DIAGNOSTIC.json','FIELD_CONTROL_RESULTS.json','IDENTITY_REPAIR_ATTEMPT.json']
prior=[]
for name in prior_names:
 z=json.loads((OLD/name).read_text())
 if name=='IDENTITY_REPAIR_ATTEMPT.json':
  prior.extend(dict(source_file=name,metadata_search=True,request=x)for x in z);continue
 if isinstance(z,list):rr=z;default=None
 elif 'requests' in z:rr=z['requests'];default=z.get('index')
 else:rr=[z];default=None
 for x in rr:prior.append(dict(source_file=name,universe=x.get('universe',default),fields=x.get('fields'),parameters=x.get('parameters',{})))
def fingerprint(universe,ff,params):
 return json.dumps([universe,sorted(ff),{k.lower():str(v).replace('-','') if k.lower()=='sdate' else str(v) for k,v in sorted(params.items())}],sort_keys=True)
oldkeys={fingerprint(x['universe'],x['fields'],x['parameters'])for x in prior if not x.get('metadata_search')}
assert all(fingerprint(u,fields,{'SDate':d}) not in oldkeys for _,u,d in queries)
(O/'PRIOR_REQUEST_BLOCKLIST.json').write_text(json.dumps({'prior_desktop_request_count':len(prior),'requests':prior},indent=2)+'\n')
membership={d:OLDPRIVATE/f'repaired_index_pilot_{d.replace("-", "")}_field1.csv'for d in ['2023-11-30','2023-12-01']}
lock={'created_utc':now(),'spec_sha256':sha(O/'SOURCE_SPEC.txt'),'code_sha256':sha(Path(__file__)),
 'prior_log_hashes':{n:sha(OLD/n)for n in prior_names},'blocklist_sha256':sha(O/'PRIOR_REQUEST_BLOCKLIST.json'),
 'historical_membership_reference_hashes':{d:sha(p)for d,p in membership.items()},
 'requests':[dict(label=l,universe=u,fields=fields,parameters={'SDate':d})for l,u,d in queries],
 'max_data_calls':4,'economic_outcomes_authorized':False,'raw_data_public':False,
 'documented_pattern':'https://community.developers.lseg.com/discussion/65797/constituent-list-and-weight-for-spx-using-python-api',
 'newness':'Previously untested exact undated PI root-chain and historical-control pattern, not a newly proven product/entitlement'}
assert not (O/'REQUEST_LOCK.json').exists()
(O/'REQUEST_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
print(json.dumps({'request_lock_sha256':sha(O/'REQUEST_LOCK.json'),'created_utc':lock['created_utc'],'data_queries_planned':4}),flush=True)

def timeout(a,b):raise TimeoutError('50 second bounded source request limit')
signal.signal(signal.SIGALRM,timeout)
out={'started_utc':now(),'library_version':importlib.metadata.version('lseg-data'),'session_opened':False,'session_closed':False,'requests':[],'economic_outcomes_computed':False}
def save():(O/'SOURCE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
save()
try:
 signal.alarm(50);session=ld.open_session();signal.alarm(0)
 out['session_type']=type(session).__module__+'.'+type(session).__name__
 if 'desktop' not in out['session_type'].lower():raise RuntimeError('Non-desktop session; no data request permitted')
 out['session_opened']=True;save()
 for label,u,day in queries:
  row={'label':label,'universe':u,'requested_date':day,'fields':fields,'started_utc':now()}
  try:
   signal.alarm(50);df=ld.get_data(universe=[u],fields=fields,parameters={'SDate':day});signal.alarm(0)
   p=P/(label+'.csv');df.to_csv(p,index=False)
   coverage={}
   for col in df.columns:
    s=df[col];nonempty=s.notna()&s.astype(str).str.strip().ne('')
    c={'nonempty':int(nonempty.sum())}
    if str(col).lower() in ['weight percent','index shares']:
     nums=pd.to_numeric(s.where(nonempty),errors='coerce');valid=nums.notna()&np.isfinite(nums.astype(float))
     c.update(numeric_finite=int(valid.sum()),positive=int((valid&nums.gt(0)).sum()),zero=int((valid&nums.eq(0)).sum()))
    coverage[str(col)]=c
   datecols=[c for c in df if str(c).lower()=='date' or str(c).lower().endswith('.date')]
   weightcols=[c for c in df if str(c).lower()=='weight percent']
   dateinfo={'date_columns':list(map(str,datecols)),'requested_date_matches':0,'positive_weights_with_requested_actual_date':0}
   if len(datecols)==1:
    dd=pd.to_datetime(df[datecols[0]],errors='coerce',utc=True).dt.strftime('%Y-%m-%d')
    dateinfo.update(actual_nonmissing_dates=sorted(dd.dropna().unique().tolist()),requested_date_matches=int(dd.eq(day).sum()))
    if len(weightcols)==1:
     vv=pd.to_numeric(df[weightcols[0]],errors='coerce');dateinfo['positive_weights_with_requested_actual_date']=int((dd.eq(day)&vv.gt(0)&np.isfinite(vv.astype(float))).sum())
   row.update(status='response',rows=len(df),columns=list(map(str,df.columns)),field_coverage=coverage,date_validation=dateinfo,private_file=p.name,sha256=sha(p))
   if u=='0#.OMXSBPI':
    old=pd.read_csv(membership[day],keep_default_na=False)
    ref=set(old.loc[old['Constituent RIC'].astype(str).str.strip().ne(''),'Constituent RIC'])
    actual=set(df.loc[df['Instrument'].notna()&df['Instrument'].astype(str).str.strip().ne(''),'Instrument'])
    row['historical_member_alignment']={'reference_members':len(ref),'returned_unique_instruments':len(actual),'common_members':len(ref&actual),'reference_missing':len(ref-actual),'extra_returned':len(actual-ref),'exact_set_match':ref==actual,'instrument_duplicate_rows':int(df['Instrument'].duplicated().sum())}
  except Exception as exc:
   signal.alarm(0);row.update(status='error',error_type=type(exc).__name__,error=str(exc)[:700])
  out['requests'].append(row);save();print(json.dumps(row),flush=True)
except Exception as exc:
 signal.alarm(0);out['session_error']={'type':type(exc).__name__,'message':str(exc)[:700]}
finally:
 signal.alarm(0)
 if out['session_opened']:
  ld.close_session();out['session_closed']=True
 out['completed_utc']=now();out['actual_data_queries']=len(out['requests']);save()
