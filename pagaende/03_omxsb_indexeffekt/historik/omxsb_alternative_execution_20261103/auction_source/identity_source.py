"""Current instrument metadata as corroboration, not proof of historical units."""
from pathlib import Path
import datetime as dt
import hashlib,json,signal
import lseg.data as ld
ROOT=Path(__file__).resolve().parent
P=ROOT/'private'/'instrument_identity.csv'
REQUEST=dict(universe=['BILIa.ST','ATRLJb.ST','CAMX.ST','AFRY.ST'],
             fields=['DSPLY_NAME','CURRENCY','ISIN_CODE','TRD_UNITS'])
LOG=dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),request=REQUEST,
         limitation='Current metadata corroborates identity only; it is not a dated historical currency/ISIN certificate. TRD_UNITS is price precision, not a currency scaling factor.')
def save():
    (ROOT/'IDENTITY_ATTEMPT.json').write_text(json.dumps(LOG,indent=2)+'\n')
def timeout(signum,frame):
    raise TimeoutError('Identity request exceeded60seconds')
signal.signal(signal.SIGALRM,timeout);save()
try:
    signal.alarm(60);s=ld.open_session();signal.alarm(0)
    assert 'desktop' in type(s).__module__.lower()
    signal.alarm(60);df=ld.get_data(**REQUEST);signal.alarm(0)
    df.to_csv(P,index=False)
    LOG.update(status='response',rows=len(df),columns=list(df.columns),
               sha256=hashlib.sha256(P.read_bytes()).hexdigest(),private_file=P.name,
               metadata=df.astype(object).where(df.notna(),None).to_dict(orient='records'))
except Exception as exc:
    signal.alarm(0)
    LOG.update(status='error',error_type=type(exc).__name__,error=str(exc)[:650])
save();print(json.dumps(LOG))
