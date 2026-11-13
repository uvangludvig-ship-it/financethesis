"""Metadata-only operational auction-source decision. No raw prices/effects read.

Builds a prospective per-review acquisition size, not a new economic sample.
Never submits a request. Fresh --output directory required.
"""
import argparse
from collections import defaultdict
import csv
from datetime import date,datetime,timezone
import hashlib,json,math
from pathlib import Path


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(path):return list(csv.DictReader(path.open()))
def truth(value):return str(value).lower() in {'true','1'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=Path('/Users/ludviguvang/dev/financethesis'))
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert not args.output.exists();args.output.mkdir(parents=True)
    base=args.repo_root/'output/omxsb_scaled_round_20261103'
    revisit=args.repo_root/'output/omxsb_shof_revisit_20261104'
    inputs={'events':base/'auction_design/EVENT_METADATA_INVENTORY.csv',
      'roles':base/'auction_design/FIXED_ROLE_METADATA_INVENTORY.csv',
      'auction_presence':base/'coverage/SOURCE_PRESENCE.csv',
      'primary_design':base/'auction_design/PRIMARY_DESIGN_SPEC.txt',
      'source_stop':base/'auction_design/SOURCE_COVERAGE_STOP_ADDENDUM.txt',
      'current_access':revisit/'ACCESS_STATUS.json','job_ledger':revisit/'ACQUISITION_LEDGER.json',
      'minute_pilot':revisit/'minute_validation/BILIA_BIN_ORDERING_CHECK.json'}
    lock=dict(created_utc=datetime.now(timezone.utc).isoformat(),scope='Source flags and frozen metadata only; no economics',
        inputs={k:{'path':str(p),'sha256':sha(p)} for k,p in inputs.items()},script_sha256=sha(Path(__file__)))
    (args.output/'INPUT_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
    E=rows(inputs['events']);R=rows(inputs['roles']);S=rows(inputs['auction_presence'])
    ledger=json.loads(inputs['job_ledger'].read_text());access=json.loads(inputs['current_access'].read_text())
    pilot=json.loads(inputs['minute_pilot'].read_text())
    byevent=defaultdict(list)
    for row in R:byevent[row['event_id']].append(row)
    candidates=[e for e in E if 2017<=int(e['review'][:4])<=2023]
    accepted=[];excluded=[]
    for e in candidates:
        rr=byevent[e['event_id']];reasons=[]
        if len(rr)!=4 or {r['role'] for r in rr}!={'event','c1','c2','c3'}:reasons.append('no_existing_three_control_set')
        if any(r['role']!='event' and r['control_origin']!='dated_eligible_rematch' for r in rr):reasons.append('older_control_match_not_dated_verified')
        if any(r['identity_quality']!='dated_listing' or not r['ric'] or not r['isin'] for r in rr):reasons.append('dated_role_identity_incomplete')
        if any(r['role']!='event' and (truth(r['known_cancelled_announcement_same_review']) or truth(r['recorded_current_OMXSB_event'])) for r in rr):reasons.append('control_known_announced_component_change')
        if reasons:excluded.append(dict(event_id=e['event_id'],review=e['review'],reasons=';'.join(reasons)))
        else:accepted.append((e,rr))
    byreview=defaultdict(list)
    for e,rr in accepted:byreview[e['review']].append((e,rr))
    coverage=defaultdict(list)
    for row in S:coverage[(row['review'],row['RIC'])].append(row)
    aucbyreview=defaultdict(int)
    for (review,ric),rr in coverage.items():
        if len(rr)==2 and all(truth(r['exact_requested_date']) and truth(r['CLS_AUC_finite']) for r in rr):aucbyreview[review]+=1
    plan=[];request_roles=[]
    for review,events in sorted(byreview.items()):
        d0s={e['comparison_date'] for e,rr in events};d1s={e['auction_date'] for e,rr in events};assert len(d0s)==len(d1s)==1
        d0,d1=next(iter(d0s)),next(iter(d1s));days=(date.fromisoformat(d1)-date.fromisoformat(d0)).days+1
        allroles=[r for e,rr in events for r in rr]
        identifiers=sorted({r['isin'] for r in allroles})
        max_instruments=1999//days
        plan.append(dict(review=review,metadata_candidate_events=sum(e['review']==review for e in candidates),
            role_sets_after_limited_metadata_screen=len(events),comparison_date=d0,auction_date=d1,
            unique_ISINs=len(identifiers),exact_stock_date_cells=2*len(identifiers),
            calendar_days_in_range=days,instrument_calendar_days=len(identifiers)*days,
            simple_per_review_minute_query_batches=math.ceil(len(identifiers)/max_instruments),
            event_RIC_pairs_with_existing_auction_numeric_presence=aucbyreview[review],
            other_index_gate='UNRESOLVED_not_an_accepted_analysis_sample'))
        for r in allroles:
            for session,d in [('comparison',d0),('implementation',d1)]:
                request_roles.append(dict(review=review,event_id=r['event_id'],role=r['role'],RIC=r['ric'],ISIN=r['isin'],session=session,date=d))
    for name,data in [('PROSPECTIVE_REVIEW_JOB_SIZES.csv',plan),('METADATA_EXCLUSIONS.csv',excluded),('PROSPECTIVE_ROLE_CELLS.csv',request_roles)]:
        with (args.output/name).open('w',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    completed=[c for c in pilot['fixed_checks'] if c['status']=='source_compared']
    pending=[{'ISIN':c['ISIN'],'date':c['date']} for c in pilot['fixed_checks'] if c['status']!='source_compared']
    remaining=ledger['source_job_budget']-ledger['maximum_backend_jobs_conservatively_budgeted']
    decision=dict(created_utc=datetime.now(timezone.utc).isoformat(),new_outcomes=False,
        current_broad_auction_decision='STOP: only two event-source-supported reviews; complete matched auction/quote source panel not built',
        minute_source_pilot=dict(compared_days=len(completed),pending_days=pending,
            completed_terminal_state_match=all(c['terminal_four_field_state_reproduced'] for c in completed),
            all_five_complete=len(completed)==5,global_sampling_or_freshness_certified=False),
        binding_missing_source='Genuine final closing-auction price before2023 for event AND three frozen controls on both dates',
        event_only_existing_auction_reviews=sorted(k for k,v in aucbyreview.items() if v),
        event_only_existing_auction_review_count=sum(v>0 for v in aucbyreview.values()),
        raw_trade_ticker_route_verified=access['raw_trade_ticker_live_access_verified'],
        raw_full_day_route_verified=access['raw_full_day_live_access_verified'],
        current_source_job_budget=dict(total=ledger['source_job_budget'],conservatively_reserved=ledger['maximum_backend_jobs_conservatively_budgeted'],remaining=remaining),
        prospective_metadata_scope=dict(years='2017–2023 because existing dated eligible controls begin2017',
            candidate_events=len(candidates),role_sets_after_limited_screen=len(accepted),reviews=len(plan),
            all_role_cell_rows=len(request_roles),unique_stock_date_cells=sum(p['exact_stock_date_cells'] for p in plan),
            simple_per_review_minute_query_batches=sum(p['simple_per_review_minute_query_batches'] for p in plan),
            excludes_other_index_source_gate=False,accepted_economic_sample=False,
            raw_message_batch_size_or_cost_known=False),
        next_actions=['Process already pending four fixed2023 minute days when delivered; no replacement query based on silence.',
            'Only if an actual raw TradeTicker/FullDay route is accessible, use at most two new source prototypes: Bilia2019-05-31 and CAMX2023-11-30.',
            'Do not order broad quote panel until a genuine historical closing source and its batching are established.',
            'A successful source prototype is not a multi-review outcome GO; all8cells/set, overlaps and review support must be frozen first.'],
        economic_bound={'informative_bound_from_current_inputs':False,
            'reason':'Missing AP cells have no established finite upper bound; paired/control contrast has positive and negative coefficients, so missingness cannot bound the review-population effect.',
            'no_new_numerical_bound_calculated':True},
        chronology='This is a new source feasibility note after known prior pilot outcomes; not blind preregistration or an amendment to the fixed estimand')
    (args.output/'DECISION.json').write_text(json.dumps(decision,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(decision,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
