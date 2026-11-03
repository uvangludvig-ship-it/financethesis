"""Public documentation/archive checks only. No login/session/credentials."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
import json,datetime,hashlib
O=Path(__file__).resolve().parent;(O/'sources').mkdir(exist_ok=True)
targets={
'current_document':'https://www.houseoffinance.se/SHoF_NASDAQ_Documentation.pdf',
'legacy_hhs_root':'https://www.hhs.se/SHoF_NASDAQ_Documentation.pdf',
'legacy_hhs_prefixed':'https://www.hhs.se/en/houseoffinance/SHoF_NASDAQ_Documentation.pdf',
'archive_https':'https://archive.org/wayback/available?'+urlencode({'url':'https://www.houseoffinance.se/SHoF_NASDAQ_Documentation.pdf','timestamp':'20200101'}),
'archive_http':'https://archive.org/wayback/available?'+urlencode({'url':'http://www.houseoffinance.se/SHoF_NASDAQ_Documentation.pdf','timestamp':'20190101'}),
'archive_legacy_hhs':'https://archive.org/wayback/available?'+urlencode({'url':'https://www.hhs.se/SHoF_NASDAQ_Documentation.pdf','timestamp':'20200101'}),
'public_repo_search':'https://api.github.com/search/repositories?'+urlencode({'q':'houseoffinance','per_page':10}),
'public_repo_search_shof':'https://api.github.com/search/repositories?'+urlencode({'q':'SHoF Nasdaq','per_page':10}),
}
def fetch(kv):
 key,url=kv;r={'key':key,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  try:f=urlopen(Request(url,headers={'User-Agent':'Academic-source-check'}),timeout=20)
  except HTTPError as e:f=e
  b=f.read();r.update(status=f.status,final_url=f.url,content_type=f.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest());(O/'sources'/(key+'.bin')).write_bytes(b)
  if 'json'in(f.headers.get('Content-Type')or''):
   d=json.loads(b)
   if key.startswith('archive'):r['response']=d
   else:r['response']={'total_count':d.get('total_count'),'repositories':[{'name':v['full_name'],'url':v['html_url'],'description':v['description']}for v in d.get('items',[])]}
 except Exception as e:r.update(error_type=type(e).__name__,error=str(e))
 return r
with ThreadPoolExecutor(max_workers=4)as ex:res=list(ex.map(fetch,targets.items()))
(O/'PUBLIC_ATTEMPTS.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
