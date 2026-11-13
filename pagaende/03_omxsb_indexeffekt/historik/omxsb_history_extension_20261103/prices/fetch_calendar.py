from pathlib import Path
import os
from datetime import datetime,timezone
import pandas as pd,json,hashlib
import lseg.data as ld
O=Path(os.environ.get('OMXSB_PRICE_WORKDIR',Path(__file__).resolve().parent));P=O/'private';lp=O/'REQUEST_LOG.json';l=json.loads(lp.read_text());R=pd.read_csv(P/'REQUEST_UNIVERSE.csv')
assert len(l)==89 and not any(r['id']=='index_2_pricing'for r in l)
r={'id':'index_2_pricing','ric':'.OMXSPI','start':R.start.min(),'end':R.end.max(),'fields':['TRDPRC_1'],'source':'pricing_index_default_adjustment','started_utc':datetime.now(timezone.utc).isoformat(),'library_version':ld.__version__}
ld.open_session()
try:
 h=ld.get_history(universe=r['ric'],fields=r['fields'],start=r['start'],end=r['end'],interval='daily');f=P/'index_2_pricing.csv.gz';h.to_csv(f,compression='gzip')
 r.update(status='received',rows=len(h),headers=[str(x)for x in h.columns],numeric_nonmissing={str(c):int(pd.to_numeric(h[c],errors='coerce').notna().sum())for c in h},private_file=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size)
except Exception as e:r.update(status='error',error=str(e)[:2000])
finally:ld.close_session()
r['ended_utc']=datetime.now(timezone.utc).isoformat();l.append(r);lp.write_text(json.dumps(l,indent=2)+'\n');print(json.dumps({k:r.get(k)for k in ['id','ric','rows','numeric_nonmissing','error']},indent=2))
