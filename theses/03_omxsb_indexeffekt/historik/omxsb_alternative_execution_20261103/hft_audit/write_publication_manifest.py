"""Explicit metadata/code allowlist; raw licensed observations are excluded."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

OUT=Path(__file__).resolve().parent
BASE=[
 'PRE_ACQUISITION_SPEC.txt','PRIMARY_CONTRAST_LOCK.txt','PRE_HFT_SOURCE_LOCK.json',
 'PILOT_SELECTION_LOCK.json','PILOT_EVENTS.csv','PILOT_SELECTION_LOG.csv','PILOT_REQUEST_SESSIONS.csv',
 'select_pilot.py','inspect_hft_source.py','test_source_inventory.py','SOURCE_TEST_LOG.txt',
 'audit_bilia_schema.py','compare_bilia_exports.py','audit_book_metadata.py','audit_nmq_schema.py',
 'summarize_lseg_source_presence.py','write_publication_manifest.py',
 'BILIA_SCHEMA_INVENTORY_v2.json','BILIA_TRANSACTION_INVENTORY.json','BILIA_SOURCE_SEMANTICS.json',
 'BILIA_EXPORT_COMPARISON.json','BILIA_BOOK_METADATA.json','NMQ_SCHEMA_INVENTORY.json','NMQ_SOURCE_NOTE.json',
 'LSEG_AUCTION_SOURCE_REQUEST.json','LSEG_LOCKED_PRIMARY_SOURCE_COVERAGE.csv','LSEG_SOURCE_PRESENCE_SUMMARY.json',
 'SOURCE_READ_LOG.txt','SOURCE_REPORT_STAGE1_SV.txt','CROSS_SOURCE_PRICE_GATE_CLARIFICATION.txt',
 'MINIMUM_PROVIDER_CLARIFICATION.txt']
CANDIDATES=['CAMX_20231123_BOOK_METADATA.json','CAMX_20231130_BOOK_METADATA.json',
 'AFRY_20231123_BOOK_METADATA.json','AFRY_20231130_BOOK_METADATA.json',
 'SOURCE_REPORT_FINAL_SV.txt','FINAL_SOURCE_GATE_SUMMARY.json',
 'NASDAQ_2023_SESSION_EVIDENCE.txt','RECOVERED_SHOF_DOCUMENT_NOTE.txt',
 'FINAL_EXECUTION_SPEC.txt','FINAL_EXECUTION_LOCK.json','CLOCK_METHOD_AMENDMENT.json',
 'CLOCK_VALIDATION.json','execute_locked_auction_pilot.py','test_locked_auction_pilot.py',
 'FINAL_EXECUTION_TEST_LOG.txt','INDIVIDUAL_AUCTION_CONTRASTS.csv',
 'INDEPENDENT_VALIDATION_POINTER.json']
assert all((OUT/f).is_file() for f in BASE)
files=BASE+[f for f in CANDIDATES if (OUT/f).is_file()]
manifest={'created_utc':datetime.now(timezone.utc).isoformat(),
 'stage':'final_two_individual_descriptive_2023_contrasts' if (OUT/'SOURCE_REPORT_FINAL_SV.txt').exists() else 'source_only_pending_locked_2023_book_metadata',
 'files':files,'count':len(files),'excluded':['BILIA_SCHEMA_INVENTORY.json','__pycache__/',
 'all private raw CSV/GZIP/ZIP files','all licensed numeric execution/quote/market-quality source values',
 'all participant/order-level identifiers','all full third-party PDFs/texts'],
 'rules':['Explicit filenames only; no recursive directory publication.',
          'Metadata JSON contains counts, missingness, clocks, hashes and instrument identifiers; no trade/quote prices or sizes.',
          'INDIVIDUAL_AUCTION_CONTRASTS.csv contains only derived individual premiums/contrasts; 2019 missingness retained; no two-event mean.',
          'Historical source-only closed gates are superseded explicitly by the final clock amendment and four2023 price-gate checks.',
          'NMQ numerical quality metrics have not been used to compute any new outcome.',
          'PILOT CSV files contain source requests/event metadata, not economic observations.',
          'Initial N/A-missingness bug is retained privately; only v2 inventory is approved.']}
(OUT/'PUBLICATION_ALLOWLIST.json').write_text(json.dumps(manifest,indent=2)+'\n')
ledger={f:{'bytes':(OUT/f).stat().st_size,'sha256':hashlib.sha256((OUT/f).read_bytes()).hexdigest()} for f in files}
(OUT/'FILE_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps({'stage':manifest['stage'],'count':len(files)}))
