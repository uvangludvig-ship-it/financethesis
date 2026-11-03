from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,datetime
O=Path(__file__).resolve().parent;(O/'private_sources').mkdir(exist_ok=True)
targets={'BM2020':'https://www.aeaweb.org/conference/2021/preliminary/paper/H9T4hef7','PS2022':'https://www.sikorskaya.net/files/Pavlova_and_Sikorskaya_2022.pdf','HLR2024':'https://www.dimensional.com/chmedia/383623/source/measuring-the-costs-of-index-reconstitution-a-10-year-perspective.pdf','VDB2022':'https://memento.epfl.ch/public/upload/files/VanderBeckPaper.pdf'}
def run(kv):
 k,u=kv;r={'key':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  try:f=urlopen(Request(u,headers={'User-Agent':'Academic-source-review'}),timeout=25)
  except HTTPError as e:f=e
  b=f.read();r.update(status=f.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),content_type=f.headers.get('Content-Type'));(O/'private_sources'/(k+'.bin')).write_bytes(b)
 except Exception as e:r.update(error_type=type(e).__name__,error=str(e))
 return r
with ThreadPoolExecutor(max_workers=4) as ex:r=list(ex.map(run,targets.items()))
(O/'PUBLIC_SOURCE_HASHES.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
