"""Small access/coverage probe, not an index-event outcome study."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import urllib.request
import urllib.parse
import urllib.error

ROOT = Path(__file__).resolve().parent
TITLES = ['Addnode Group', 'VBG Group', 'Loomis', 'Investor', 'Embracer Group', 'Volvo']
START, END = '20190101', '20190131'
UA = 'OMXSBResearchCoverageProbe/1.0 (https://github.com/uvangludvig-ship-it/financethesis) Python/urllib'
LOG = []

def get(url, filename):
    request = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    record = {'url': url, 'retrieved_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'file': filename}
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            body = response.read()
            record.update(status=response.status, content_type=response.headers.get('Content-Type'))
    except urllib.error.HTTPError as exc:
        body = exc.read()
        record.update(status=exc.code, content_type=exc.headers.get('Content-Type'))
    except Exception as exc:
        record.update(status=None, error=type(exc).__name__ + ': ' + str(exc))
        body = b''
    (ROOT/filename).write_bytes(body)
    record.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
    LOG.append(record)
    (ROOT/'download_log.json').write_text(json.dumps(LOG, ensure_ascii=False, indent=2)+'\n')
    if record['status'] != 200:
        return None
    try:
        return json.loads(body)
    except Exception:
        return None

spec = {
    'purpose': 'Verify public endpoint access and historical technical coverage, not event effects.',
    'chosen_before_requests': True,
    'selection': 'Six purposive technical sentinels spanning recognizable and less-known names; not representative or randomly selected.',
    'titles': TITLES, 'project': 'sv.wikipedia.org', 'fixed_calendar_window': [START, END],
    'prohibitions': ['No CAR or price data', 'No index-event attention estimates', 'No inference from this sample to whole-universe coverage'],
    'identity_limits': 'Current page identity and redirects are checked; historical title/page-move identity is not fully reconstructed.',
}
(ROOT/'probe_specification.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
params = {'action':'query','format':'json','titles':'|'.join(TITLES),'redirects':1,'prop':'info|pageprops','ppprop':'wikibase_item'}
result = get('https://sv.wikipedia.org/w/api.php?'+urllib.parse.urlencode(params),'page_identity.json')
coverage=[]
if result and 'query' in result:
    for page in result['query'].get('pages',{}).values():
        row={'title':page.get('title'),'pageid':page.get('pageid'),'missing_page':'missing' in page,'wikibase_item':page.get('pageprops',{}).get('wikibase_item')}
        if row['missing_page']:
            coverage.append(row)
            continue
        slug=urllib.parse.quote(row['title'].replace(' ','_'),safe='')
        url=f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/sv.wikipedia.org/all-access/user/{slug}/daily/{START}/{END}'
        data=get(url,f'views_{page["pageid"]}.json')
        if data is None:
            row['series_available']=False
        else:
            items=data.get('items',[])
            row.update(series_available=True,observed_days=len(items),expected_days=31,zero_days=sum(x.get('views')==0 for x in items),positive_days=sum(x.get('views',0)>0 for x in items))
        coverage.append(row)
else:
    coverage.append({'series_available':False,'reason':'Page identity endpoint could not be verified; no pageview queries attempted.'})
(ROOT/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'requests':len(LOG),'http_statuses':[x['status'] for x in LOG],'coverage':coverage},ensure_ascii=False))
