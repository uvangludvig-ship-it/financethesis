"""Public documentation/archive checks only. No login/session/credentials."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
import json,datetime,hashlib
O=Path(__file__).resolve().parent;(O/'sources').mkdir(exist_ok=True)
targets={
'archive_document':'https://web.archive.org/web/20230107102616id_/https://www.houseoffinance.se/SHoF_NASDAQ_Documentation.pdf',
'parser_source':'https://raw.githubusercontent.com/SwedishHouseofFinance/SHoF-Nasdaq-JSON-Parser/master/Main.java',
'parser_readme':'https://raw.githubusercontent.com/SwedishHouseofFinance/SHoF-Nasdaq-JSON-Parser/master/README.md',
'org_repositories':'https://api.github.com/orgs/SwedishHouseofFinance/repos?per_page=100',
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
   elif isinstance(d,list):r['response']=[{'name':v.get('full_name'),'description':v.get('description'),'url':v.get('html_url')} for v in d]
   else:r['response']={'total_count':d.get('total_count'),'repositories':[{'name':v['full_name'],'url':v['html_url'],'description':v['description']}for v in d.get('items',[])]}
 except Exception as e:r.update(error_type=type(e).__name__,error=str(e))
 return r
with ThreadPoolExecutor(max_workers=4)as ex:res=list(ex.map(fetch,targets.items()))
(O/'PRIMARY_FOLLOWUP_ATTEMPTS.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
