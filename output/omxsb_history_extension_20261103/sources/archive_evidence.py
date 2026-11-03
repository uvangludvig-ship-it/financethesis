"""Fetch only already-read public primary URLs; full bodies remain private."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, urllib.request

BASE = Path(__file__).resolve().parent
SOURCES = [
    dict(id='launch', url='https://news.cision.com/se/stockholmsborsen/r/xact-sbx---en-ny-borshandlad-fond-noteras,c80505',
         publisher='Stockholmsbörsen', publication_date='2003-06-02', role='historical_identity_only',
         evidence_quote='SBX-index lanserades den 12 april 2001',
         interpretation='Live launch 2001-04-12; base 1995-12-30; semiannual review stated. No specific 2003–2006 review AD/ED or names.'),
    dict(id='rename', url='https://news.cision.com/se/omx-exchanges/r/omx-harmoniserar-indexnamn,c161338',
         publisher='OMX Exchanges', publication_date='2005-08-22', role='historical_identity_only',
         evidence_quote='Benchmark indexen i Köpenhamn och Stockholm ändras till OMXCB respektive OMXSB',
         interpretation='Name structure changes effective 2005-10-03. Not a candidate constituent review announcement.'),
    dict(id='market_notice_service', url='https://news.cision.com/se/stockholmsborsen/r/ny-tjanst-for-press--och-borsmeddelanden-samt-statistikrapporter,c80760',
         publisher='Stockholmsbörsen', publication_date='2003-06-06', role='archive_locator_only',
         evidence_quote='Stockholmsbörsen lanserar tjänsten onsdagen den 18 juni 2003.',
         interpretation='Searchable press/market notice service under Förändringar och Nyheter; not an SBX review.'),
    dict(id='wrong_segment_jan2003', url='https://news.cision.com/se/stockholmsborsen/r/forandringar-pa-mest-omsatta-och-attract40-tm-,c71299',
         publisher='Stockholmsbörsen', publication_date='2002-12-19', role='rejected_wrong_segment',
         evidence_quote='Förändringar på Mest Omsatta och ATTRACT40(TM)',
         interpretation='January 2003 listing segments, not SBX. Its announcement date is not used.'),
    dict(id='wrong_segment_jul2003', url='https://news.cision.com/se/stockholmsborsen/r/forandringar-pa-mest-omsatta-och-attract40-tm-,c81148',
         publisher='Stockholmsbörsen', publication_date='2003-06-17', role='rejected_wrong_segment',
         evidence_quote='Mest Omsatta-segmentet på A-listan förändras inte.',
         interpretation='Attract40/Mest Omsatta July 2003; unrelated review, with an internal January wording inconsistency. No SBX verification.'),
    dict(id='july2007_control', url='https://www.globenewswire.com/news-release/2007/06/12/116558/0/sv/avista-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-175-07.html',
         publisher='Exchange market notice, now Nasdaq Stockholm AB archive', publication_date='2007-06-12', role='outside_scope_convention_control',
         evidence_quote='Den nya sammansättningen träder i kraft fr.o.m. måndagen den 2 juli 2007.',
         interpretation='Original notice 175/07; page shows 06:29 ET, i.e. 12:29 Europe/Stockholm on 2007-06-12. This July review is not evidence for any of the eight earlier dates.'),
]

def fetch(row):
    row = dict(row)
    row['retrieval_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    row['evidence_method'] = 'primary source read with web tool; HTTP body archive attempt below'
    row['full_source_publication'] = False
    try:
        with urllib.request.urlopen(row['url'], timeout=15) as r:
            body = r.read()
            row.update(http_status=r.status, final_url=r.url)
        (BASE / 'private' / (row['id'] + '.html')).write_bytes(body)
        row['raw_body_sha256'] = hashlib.sha256(body).hexdigest()
    except Exception as e:
        row['archive_error'] = f'{type(e).__name__}: {e}'
        row['raw_body_sha256'] = None
    return row

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(fetch, SOURCES))
    (BASE/'SOURCE_LEDGER.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps([{'id':r['id'],'archived':r['raw_body_sha256'] is not None} for r in rows]))
