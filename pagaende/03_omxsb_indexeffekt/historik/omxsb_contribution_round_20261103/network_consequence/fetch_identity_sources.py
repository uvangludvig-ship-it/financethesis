"""Replay downloads to this folder; original file hashes remain in manifest.json."""
from pathlib import Path
import urllib.request,hashlib,json,datetime,subprocess
D=Path(__file__).resolve().parent/'identity_sources'
saved=json.loads((D/'manifest.json').read_text());results=[]
for s in saved:
 p=D/s['file']
 if p.exists():
  results.append(dict(file=s['file'],status='already_present',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),matches_original=hashlib.sha256(p.read_bytes()).hexdigest()==s.get('sha256')));continue
 try:
  b=urllib.request.urlopen(urllib.request.Request(s['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read();p.write_bytes(b)
  if p.suffix=='.pdf':subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  results.append(dict(file=s['file'],status='downloaded',sha256=hashlib.sha256(b).hexdigest(),matches_original=hashlib.sha256(b).hexdigest()==s.get('sha256')))
 except Exception as e:results.append(dict(file=s['file'],status=str(e)))
(D/'retrieval_replay.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),results=results),indent=2))
