"""Read-only HTTP collection; creates new files exclusively, never overwrites sources."""
import csv, datetime as dt, hashlib, json, pathlib, re, sys, urllib.request, urllib.parse
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[2]
AP = ROOT / 'data/raw/ap'
FI = ROOT / 'data/raw/fi_short'
META = AP / '_collection_20261031'
for p in (AP, FI, META):
    p.mkdir(parents=True, exist_ok=True)

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.current=None; self.parts=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a': self.current=a.get('href'); self.parts=[]
    def handle_data(self, data):
        if self.current is not None: self.parts.append(data)
    def handle_endtag(self, tag):
        if tag=='a' and self.current is not None:
            self.links.append((self.current,' '.join(' '.join(self.parts).split())))
            self.current=None

def fetch(url, dest=None, kind='discovery'):
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    rec=dict(url=url,downloaded_at_utc=stamp,kind=kind)
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research data collection)'})
        with urllib.request.urlopen(req,timeout=45) as r:
            body=r.read(); rec.update(final_url=r.url,status=r.status,content_type=r.headers.get('Content-Type',''))
        rec.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
        if dest:
            dest=pathlib.Path(dest); dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():
                if hashlib.sha256(dest.read_bytes()).hexdigest()!=rec['sha256']:
                    raise ValueError('Refusing to overwrite existing different file: '+str(dest))
                rec['file_status']='already_identical'
            else:
                with dest.open('xb') as f: f.write(body)
                rec['file_status']='created'
            rec['local_path']=str(dest.relative_to(ROOT))
        return body
    except Exception as e:
        rec.update(status='error',error=str(e)); return None
    finally:
        with (META/'requests.jsonl').open('a') as f: f.write(json.dumps(rec,ensure_ascii=False)+'\n')

def discover(url, label):
    body=fetch(url,META/(label+'.html'))
    if body is None: return []
    p=Links(); p.feed(body.decode('utf-8',errors='replace'))
    links=[{'url':urllib.parse.urljoin(url,u),'text':t,'page':url,'label':label} for u,t in p.links]
    with (META/(label+'_links.json')).open('x') as f: json.dump(links,f,ensure_ascii=False,indent=2)
    for x in links:
        if re.search(r'\.pdf|\.xlsx?|aktie|innehav|position|histor|vardepapp|värdepapp|201[3-9]|202[0-6]',x['url']+' '+x['text'],re.I):
            print(json.dumps(x,ensure_ascii=False))
    return links

if __name__=='__main__':
    if sys.argv[1]=='discover': discover(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=='download': fetch(sys.argv[2],ROOT/sys.argv[3],'original')
    elif sys.argv[1]=='batch':
        from concurrent.futures import ThreadPoolExecutor
        jobs=[]
        for label in ('ap1','ap2','ap3','ap4'):
            links=json.loads((META/(label+'_links.json')).read_text())
            seen=set()
            for x in links:
                t=x['text'].lower(); u=x['url']
                wanted=(t.startswith('noterade') if label in ('ap1','ap4') else bool(re.search('svenska aktier|utländska aktier',t)))
                if wanted and u.lower().endswith('.pdf') and u not in seen:
                    seen.add(u); x['fund']=label.upper()
                    x['local_path']=str((AP/label.upper()/urllib.parse.unquote(u.split('/')[-1])).relative_to(ROOT))
                    jobs.append(x)
        with (META/'download_manifest.json').open('x') as f: json.dump(jobs,f,ensure_ascii=False,indent=2)
        def work(x):
            b=fetch(x['url'],ROOT/x['local_path'],'original')
            return (x['fund'],x['local_path'],len(b) if b else 'FAILED')
        with ThreadPoolExecutor(max_workers=4) as pool:
            for result in pool.map(work,jobs): print(*result,flush=True)
