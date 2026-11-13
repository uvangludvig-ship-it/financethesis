"""Download only official URLs observed in Nasdaq's public historical report UI.
No authentication, bypasses, guessed endpoints or returns. Existing files preserved.
Run: python fetch_verified_sources.py
"""
from pathlib import Path
import concurrent.futures, hashlib,json,urllib.request
P=Path(__file__).resolve().parent
rows=json.loads((P/'verified_archive_links.json').read_text())
tasks=[]
for x in rows:
 tasks.extend([(x['target_file'],x['attachment_url']),(x['month']+'_notice.html',x['notice_url'])])
def fetch(t):
 name,url=t;p=P/name
 try:
  existed=p.exists()
  if not existed:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=25) as r:b=r.read()
   if not b:raise ValueError('Empty response')
   p.write_bytes(b)
  b=p.read_bytes()
  if name.endswith('.xls') and not b.startswith(bytes.fromhex('D0CF11E0A1B11AE1')):raise ValueError('Not an XLS binary workbook')
  if name.endswith('.xlsx') and not b.startswith(b'PK'):raise ValueError('Not a ZIP-based XLSX workbook')
  return dict(file=name,url=url,ok=True,already_present=existed,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:return dict(file=name,url=url,ok=False,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(fetch,tasks))
(P/'retrieval_recheck.json').write_text(json.dumps(out,indent=2)+'\n')
print(sum(r['ok'] for r in out),'of',len(out),'sources available')
if not all(r['ok'] for r in out):raise SystemExit(2)
