"""Freeze a source-only audit; no API request and no licensed values published."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
P=Path(__file__).resolve().parent
CHAT=P.parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,o): (P/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
sources=[
 {'id':'documented_TR_volume','url':'https://community.developers.lseg.com/discussion/101276/how-can-i-pull-historical-ticker-level-closing-auction-volume-in-refinitiv-eikon-excel','read':'Accepted/vendor answer and all comments; explicitly named TR.ClosingAuctionVolume','role':'Only new data field used in the two source requests'},
 {'id':'Tick_History_current_quickstart','url':'https://developers.lseg.com/en/api-catalog/refinitiv-tick-history/refinitiv-tick-history-rth-rest-api/quick-start','revision':'Jan2026','read':'Prerequisites; relation to DSS; authentication; service URI; standard extractions vs on-demand','role':'Separate DSS identity required; no desktop entitlement inference'},
 {'id':'Tick_History_python','url':'https://developers.lseg.com/en/article-catalog/article/tick-history-jupyter-notebook-quick-start','revision':'Jan2026','read':'Prerequisites and product scope','role':'Permissioned DSS login; broad history statement not instrument/date guarantee'},
 {'id':'CFS_desktop_boundary','url':'https://community.developers.lseg.com/discussion/107346/isins-cusips-full-list','revision':'July2023','read':'Accepted and follow-up vendor answers','role':'Explicit Workspace desktop exclusion for CFS; no speculative desktop call made'},
 {'id':'CFS_current_workflow','url':'https://developers.lseg.com/en/article-catalog/article/a-step-by-step-workflow-guide-for-rdp-client-file-store--cfs--ap','revision':'September2026','read':'Introduction and platform authentication/bucket workflow','role':'Tick History file store exists; permissioned service/content, not desktop access'},
 {'id':'Historical_Pricing_tick_limit','url':'https://community.developers.lseg.com/discussion/110733/tick-history-eikon-premium-user','revision':'November2023','read':'Accepted vendor answer','role':'90-day tick history; not an explanation of daily CLS_AUC start date'},
 {'id':'Tick_History_field_dictionary','url':'https://developers.lseg.com/content/dam/devportal/articles/how-expand-chain-ric-using-tick-history-rest-api-python/Thomson%20Reuters%20Tick%20History%2011.0%20REST%20API%20Use%20Cases%20Reference%20v1.0.pdf','read':'Search-returned primary excerpt Chapter19 p113 with auction content fields; earlier full-primary field guide locators in input source_access_note','role':'Documented fields, not certified Stockholm coverage'},
 {'id':'Nasdaq_EOD_cross_file','url':'https://www.nasdaq.com/docs/eod-for-nasdaq-nordic-1.70.1.pdf','revision':'2015-01-19 version1.70.1','read':'Entire10-page PDF text; printedpp1–2 and revisionhistoryp4','role':'Separate individual-cross/reveal file; current access and2019/2023 schema unverified'},
 {'id':'Nasdaq_delivery_migration','url':'https://view.news.eu.nasdaq.com/view?id=b8cce52d889b395d9030aa9b4d07a929a&lang=en&src=rss','revision':'2026-04-01','read':'Full announcement','role':'Historical ITCH among products migrated FDS→Nasdaq Data Link Files; no archive entitlement established'},
 {'id':'Nasdaq_current_catalog','url':'https://www.nasdaq.com/products/data/market-data-catalog','read':'Nordic Equity HistoricalView and End-of-Day descriptions','role':'Product existence and rolling30-day subscription; no current free historical endpoint'},
 {'id':'Nasdaq_2019_HistoricalView','url':'https://www.nasdaq.com/docs/2019/12/09/European%20GIS%20Pricelist%201_4.pdf','revision':'2019-12-01','read':'Historical Data Fees p27','role':'Continuous-trading wording cannot resolve SHoF aggregate-cross retention; no prices/fees used in recommendation'}]
write('SOURCE_LEDGER.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'sources':sources,'original_web_bytes_saved':False,'original_web_hashes':None,'hash_note':'Public primary pages read through web tool; no original PDF/HTML bytes obtained or hash invented.'})
inputs=[
 'work/omxsb_shof_revisit_20261104/documentation/REPORT_SV.txt',
 'work/omxsb_shof_revisit_20261104/documentation/SOURCE_LEDGER.json',
 'work/omxsb_shof_revisit_20261104/documentation/DATA_REQUEST_NOT_SENT.txt',
 'work/omxsb_shof_revisit_20261104/raw_audit/REPORT_SV.txt',
 'work/omxsb_scaled_round_20261103/winner_novelty/source_access_note.txt',
 'work/omxsb_scaled_round_20261103/auction_design/SOURCE_COVERAGE_STOP_ADDENDUM.txt',
 'work/alternative_execution_20261103/auction_source/probe.py',
 'work/alternative_execution_20261103/auction_source/remaining_fixed_pilot.py',
 'work/alternative_execution_20261103/auction_source/minute_2023_source.py']
write('INPUT_HASHES.json',[{'path':str(CHAT/x),'sha256':sha(CHAT/x)} for x in inputs])
write('ATTEMPT_REGISTER.json',{'source_request_limit':2,'new_data_requests':2,'request_errors':0,
 'failed_content_presence':[{'instrument':'BILIa.ST','date':'2019-05-31','kind':'Successful table response containing placeholder instrument row, empty date and auction-volume cells; not numeric zero.'}],
 'positive_control':{'instrument':'CAMX.ST','date':'2023-11-30','kind':'One dated finite auction-volume observation; no new price coverage'},
 'known_failed_requests_repeated':False,'forgone_requests':[{'route':'CFS through Desktop','reason':'Vendor explicitly says unavailable through Workspace; not attempted'}, {'route':'DSS Tick History extraction','reason':'No authorized separate DSS authentication established; not attempted; not proof institution lacks subscription'}, {'route':'Nasdaq historical EOD/ITCH files','reason':'No observed entitled download endpoint/account established; not attempted'}, {'route':'SHoF raw products','reason':'No verified direct endpoint; UI remains with root; no endpoint guessing'}],
 'SDK_inspection':'Installed lseg-data2.1.1 package module/signature introspection only; no secrets/config or environment variables read. Actual default Desktop session opened and local client closed.',
 'price_returns_or_other_economic_outcomes_computed':False,'no_FTN_outcomes':True,'ui_actions':0,'emails':0,'paid_or_trial_registration':0,
 'QA':'Original Date numeric diagnostic issue repaired in public script and independently validated from private CSV without repeating requests; immutable original log preserved.'})
files=['README.txt','REPORT_SV.txt','READY_SOURCE_REQUEST.txt','SOURCE_LEDGER.json','INPUT_HASHES.json','ATTEMPT_REGISTER.json','SOURCE_PILOT_LOCK.json','SOURCE_PILOT_RESULT.json','VALIDATED_SOURCE_PRESENCE.json','probe_documented_auction_volume.py','validate_source_presence.py','freeze_package.py','PUBLICATION_ALLOWLIST.json','PUBLICATION_SHA256.json']
write('PUBLICATION_ALLOWLIST.json',files)
write('PUBLICATION_SHA256.json',{f:sha(P/f) for f in files if f!='PUBLICATION_SHA256.json'})
assert all('/' not in f and (P/f).is_file() for f in files)
assert len(files)==len(set(files))
print(json.dumps({'public_files':len(files),'hashed_files':len(files)-1,'manifest_sha256':sha(P/'PUBLICATION_SHA256.json')}))
