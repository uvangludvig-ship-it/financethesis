"""Bounded sequential LSEG source acquisition, private payloads; no return calculations."""
from pathlib import Path
import os
from datetime import datetime,timezone
import json,hashlib,time,argparse
import pandas as pd
import lseg.data as ld
O=Path(os.environ.get('OMXSB_PRICE_WORKDIR',Path(__file__).resolve().parent));P=O/'private';P.mkdir(exist_ok=True)
now=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=90);args=p.parse_args()
R=pd.read_csv(P/'REQUEST_UNIVERSE.csv')
TR=['TR.PriceClose','TR.TotalReturn','TR.TotalReturn1D','TR.Volume','TR.CompanyMarketCap','TR.SharesOutstanding']
PR=['TRDPRC_1','ACVOL_UNS','BID','ASK']
req=[]
for i,r in enumerate(R.itertuples()):
 req.append({'id':f'stock_{i:02d}_TR','ric':r.ric,'start':r.start,'end':r.end,'fields':TR,'source':'TR'})
for i,r in enumerate(R.itertuples()):
 req.append({'id':f'stock_{i:02d}_pricing','ric':r.ric,'start':r.start,'end':r.end,'fields':PR,'source':'pricing_default_adjustment'})
for i,r in enumerate(['.OMXSBGI','.OMXSGI']):
 req.append({'id':f'index_{i}_TR','ric':r,'start':R.start.min(),'end':R.end.max(),'fields':['TR.PriceClose'],'source':'TR_index'})
manifest=O/'REQUEST_LOCK.json'
if not manifest.exists():
 manifest.write_text(json.dumps({'locked_utc':now(),'requests':req,'conditional_index_fallback':'If no numeric TR.PriceClose, one TRDPRC_1 request per index, same date bounds','max_calls':90,'default_adjustment':'No explicit adjustment parameter, matching old pull API; adjustment equivalence is not certified automatically','no_RIC_alias_fallback':True,'script_sha256':sha(Path(__file__)),'source_spec_sha256':sha(O/'SOURCE_SPEC.json')},indent=2)+'\n')
logpath=O/'REQUEST_LOG.json';log=json.loads(logpath.read_text()) if logpath.exists()else []
done={r['id']for r in log}
def perform(q):
 if len(log)>=90:raise RuntimeError('90-call ceiling')
 rec={**q,'started_utc':now(),'library_version':ld.__version__}
 try:
  h=ld.get_history(universe=q['ric'],fields=q['fields'],start=q['start'],end=q['end'],interval='daily')
  if h is None:rec.update(status='none',rows=0)
  else:
   rec.update(status='received',rows=len(h),headers=[str(c)for c in h.columns],index_name=str(h.index.name),index_min=str(h.index.min()),index_max=str(h.index.max()),numeric_nonmissing={str(c):int(pd.to_numeric(h[c],errors='coerce').notna().sum())for c in h.columns})
   dest=P/(q['id']+'.csv.gz');h.to_csv(dest,index=True,compression='gzip');rec.update(private_file=str(dest),sha256=sha(dest),bytes=dest.stat().st_size)
 except Exception as e:rec.update(status='error',error=str(e)[:2000])
 rec['ended_utc']=now();log.append(rec);logpath.write_text(json.dumps(log,indent=2)+'\n');print(json.dumps({k:rec.get(k)for k in ['id','ric','status','rows','headers','numeric_nonmissing','error']}),flush=True);time.sleep(.3)
ld.open_session()
try:
 n=0
 for q in req:
  if q['id']in done:continue
  if n>=args.limit:break
  perform(q);n+=1
 if args.limit>1:
  for i,r in enumerate(['.OMXSBGI','.OMXSGI']):
   source=next((x for x in log if x['id']==f'index_{i}_TR'),None)
   if source and not any(source.get('numeric_nonmissing',{}).values()) and f'index_{i}_pricing'not in done:
    perform({'id':f'index_{i}_pricing','ric':r,'start':R.start.min(),'end':R.end.max(),'fields':['TRDPRC_1'],'source':'pricing_index_default_adjustment'})
finally:ld.close_session()
