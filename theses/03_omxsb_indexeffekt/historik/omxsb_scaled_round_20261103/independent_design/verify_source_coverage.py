#!/usr/bin/env python3
"""Independent count of source-presence flags only; never read financial values."""
import csv, hashlib, json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse

def main():
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,default=Path(__file__).resolve().parents[1]/'coverage');p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'COVERAGE_REVIEW.json');a=p.parse_args()
    if a.output.exists(): raise RuntimeError('Frozen coverage output exists; use --output NEW_FILE.')
    source=a.source_dir/'SOURCE_PRESENCE.csv';lock=a.source_dir/'SOURCE_REQUEST_LOCK.json'
    rows=list(csv.DictReader(source.open()));meta=json.loads(lock.read_text())
    allowed={'review','date','role','RIC','response_status','exact_requested_date','CLS_AUC_finite','CLS_AUCVOL_finite','TRDPRC_1_finite'}
    assert set(rows[0])==allowed
    groups=defaultdict(list)
    for r in rows:groups[(r['review'],r['RIC'])].append(r)
    reviews=defaultdict(lambda:{'event_ric_pairs':0,'auction_both_dates':0,'ordinary_price_both_dates':0})
    for (review,ric),rs in groups.items():
        assert len(rs)==2 and {r['role'] for r in rs}=={'comparison','rebalance'}
        q=reviews[review];q['event_ric_pairs']+=1
        q['auction_both_dates']+=all(r['CLS_AUC_finite']=='1' and r['exact_requested_date']=='True' for r in rs)
        q['ordinary_price_both_dates']+=all(r['TRDPRC_1_finite']=='1' and r['exact_requested_date']=='True' for r in rs)
    out={'created_utc':datetime.now(timezone.utc).isoformat(),'source_only':True,'new_outcomes_computed':False,'rows':len(rows),'event_ric_pairs':len(groups),'review_count':len(reviews),'request_count':len(meta['requests']),'source_hashes':{str(x.name):hashlib.sha256(x.read_bytes()).hexdigest() for x in(source,lock)},'by_review':dict(sorted(reviews.items())),'auction_supported_reviews':[r for r,v in sorted(reviews.items()) if v['auction_both_dates']>0],'control_sources_validated':False,'interpretation':'Event-source upper bound only. Two supported reviews cannot establish population auction inference. Missing auction fields are not zero premiums.'}
    assert len(rows)==meta['request_rows'] and len(groups)==meta['events'] and len(reviews)==meta['reviews']
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in['rows','event_ric_pairs','review_count','request_count','auction_supported_reviews','new_outcomes_computed']}))
if __name__=='__main__':main()
