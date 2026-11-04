"""Archive only already-read public primary docs, privately; no data/auth calls."""
from pathlib import Path
import datetime,hashlib,json,urllib.request,concurrent.futures
O=Path(__file__).resolve().parent;P=O/'private/source_documents';P.mkdir(exist_ok=True)
sources=[
 ('lseg_root_chain','https://community.developers.lseg.com/discussion/65797/constituent-list-and-weight-for-spx-using-python-api','Documented root chain plus SDate and field date; no guarantee for every index'),
 ('lseg_dsws_fields','https://community.developers.lseg.com/discussion/106460/how-to-retrieve-msci-index-constituents-weights-index-shares-weights-in-datastream/p1','Provider documents WTIDX and FNSIDX; not company NOSH/NOSHFF; OMXSB not certified'),
 ('lseg_dsws_auth','https://developers.lseg.com/en/api-catalog/eikon/datastream-web-service/Quickstart','DSWS requires a Datastream child account/password; desktop session is not evidence of DSWS access'),
 ('lseg_separate_weight_entitlement','https://community.developers.lseg.com/discussion/72579/eikon-data-api-error-requesting-tr-indexconstituentweightpercent/p1','For SPX provider distinguishes membership from fee-liable weights; does not determine our OMXSB cause'),
 ('nasdaq_giffd','https://www.nasdaqtrader.com/content/technicalSupport/specifications/dataproducts/Nasdaq-GIFFD-Global-Index-FlexFile-Delivery.pdf','v3.1 Feb2025, sections2/4/5/7.1: authorized SFTP/IP setup, versioned files and weight/index-share definitions'),
 ('nasdaq_public_samples','https://emi.nasdaq.com/index/GIW_Webservices/','Public directory lists other-index samples; no OMXSB sample is listed'),
 ('nasdaq_sftp_samples','https://emi.nasdaq.com/index/GIFFD_SFTP/','Public directory lists one NDX CAUFF example; not OMXSB archive')]
def fetch(x):
 key,url,meaning=x;r={'key':key,'url':url,'meaning_and_limit':meaning,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_type':'primary provider documentation','authenticated':False,'raw_fulltext_public':False}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30)as h:
   raw=h.read();p=P/(key+('.pdf' if 'pdf' in h.headers.get('Content-Type','').lower() else '.html'));p.write_bytes(raw)
   r.update(http_status=h.status,final_url=h.url,content_type=h.headers.get('Content-Type'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),private_file=str(p.relative_to(O)))
 except Exception as e:r.update(error_type=type(e).__name__,error=str(e)[:300],web_tool_primary_page_read_successfully=True)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rows=list(ex.map(fetch,sources))
(O/'PRIMARY_SOURCE_LEDGER.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([{'key':x['key'],'status':x.get('http_status',x.get('error_type'))}for x in rows],indent=2))
