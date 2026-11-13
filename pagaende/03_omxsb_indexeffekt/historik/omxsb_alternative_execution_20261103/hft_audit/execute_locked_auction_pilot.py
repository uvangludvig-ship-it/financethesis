"""Frozen HFT source gates and two individual AP contrasts; never export raw prices."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, gzip, hashlib, json
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
PARENT = OUT.parent / 'auction_source'
RAW = Path('/Users/ludviguvang/dev/financethesis/data/raw/shof/Reinvestments/hft_pilot_20261103')
BOOKS = [
 ('BILIa.ST','2019-05-31','1793732319625','b965282b2d3e4f07c5e7cc144761fbf8cda944caec9f297662a86fa1a0e95564',None,None),
 ('CAMX.ST','2023-11-23','1793733524718','b559e19b8c445bba9fcbb5a43726e3a991c9199eb7a5f6af007846fe7d44ffec','remaining_3.csv','c72fc493a5ebbcf0bfaf5889cc21e77935bc747e957165d6eb16ebea6c2de70f'),
 ('CAMX.ST','2023-11-30','1793733549086','71c3a114075e238da37441113a6ed2b3235b8bfecc8f211243a80eac1ff9f91b','remaining_4.csv','0aaec103138b31b2b46da45f7547227399761b973f0d960777f1a83270b91523'),
 ('AFRY.ST','2023-11-23','1793733618890','f288da767226b4c1450503dfcc1a50c5c1550e7a8747eed7fffaeba259cd1447','remaining_5.csv','c1dd5c8b8940811f54ae79fc222d8e62203df5231b56f7ec5e36781f8a83469f'),
 ('AFRY.ST','2023-11-30','1793733672616','1829722e3e4c6e25a7c56ed9a75f1cdaa4c9d3e3c7f9140ccfc0d389c8b93c80','remaining_6.csv','d0fe504f2260c92836addcfe76974d069133fc4dae0fcece35e1ad74fefc1fbd'),
]
TOP = ['bidpx1','askpx1','bidsz1','asksz1']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save_new(name, obj):
    p=OUT/name
    if p.exists(): raise FileExistsError(f'Preserve prior run: {p}')
    p.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')

def frame(p):
    with gzip.open(p,'rt') as f:
        return pd.read_csv(f,sep=';',dtype=str,keep_default_na=False)

def clock_check(x, candidate):
    naive=pd.to_datetime(x['date']+' '+x['time'])
    if candidate=='exchange_local':
        local=naive.dt.tz_localize('Europe/Stockholm',ambiguous='raise',nonexistent='raise')
    elif candidate=='UTC':
        local=naive.dt.tz_localize('UTC').dt.tz_convert('Europe/Stockholm')
    else: raise ValueError(candidate)
    t=local.dt.tz_localize(None)-local.dt.tz_localize(None).dt.normalize()
    T=x['status'].eq('T'); I=x['status'].eq('IOO')
    a=pd.Timedelta(hours=8,minutes=45); b=pd.Timedelta(hours=9)
    c=b+pd.Timedelta(seconds=5); d=pd.Timedelta(hours=17,minutes=25)
    wrong_day=int((local.dt.strftime('%Y-%m-%d')!=x['date']).sum())
    lateT=int((T&~(t.ge(b)&t.lt(d))).sum())
    badI=int((I&~(t.ge(a)&t.le(c))).sum())
    lastI=t[I].max() if I.any() else None
    firstT=t[T].min() if T.any() else None
    transition=bool(lastI is not None and firstT is not None and b<=lastI<=c and firstT>lastI)
    return {'candidate':candidate,'T_rows':int(T.sum()),'IOO_rows':int(I.sum()),
            'T_outside_regular_continuous_session':lateT,'IOO_outside_opening_window':badI,
            'changed_calendar_date_rows':wrong_day,'documented_opening_transition_conforms':transition,
            'first_T_local':str(firstT),'last_IOO_local':str(lastI),
            'passes':bool(T.any() and I.any() and not lateT and not badI and not wrong_day and transition)}

def select_quote(x):
    tm=pd.to_timedelta(x['time']); cut=pd.Timedelta(hours=17,minutes=25)
    q=x[TOP].apply(pd.to_numeric,errors='coerce')
    good=(np.isfinite(q).all(axis=1)&q.gt(0).all(axis=1)&q.bidpx1.le(q.askpx1)
          &x['status'].eq('T')&tm.lt(cut)&tm.ge(cut-pd.Timedelta(seconds=60)))
    if not good.any(): raise ValueError('no_valid_quote_in_locked_final_60_seconds')
    last=tm[good].max(); at=good&tm.eq(last)
    states=q.loc[at,TOP].drop_duplicates()
    if len(states)!=1: raise ValueError('ambiguous_distinct_quote_states_at_last_timestamp')
    if tm.diff().lt(pd.Timedelta(0)).any(): raise ValueError('nonmonotonic_source_timestamp')
    info={'quote_time_as_inferred_local':str(last).replace('0 days ',''),
          'quote_age_seconds':float((cut-last)/pd.Timedelta(seconds=1)),
          'rows_at_final_timestamp':int(at.sum()),'distinct_top_states':len(states),
          'valid_quotes_in_final_60_seconds':int(good.sum())}
    z=states.iloc[0]
    return info, (float(z.bidpx1)+float(z.askpx1))/2

def auction_price(x, date):
    # No fallback: a last-trade field cannot substitute for missing auction data.
    if len(x)!=1 or pd.to_datetime(x.iloc[:,0]).dt.strftime('%Y-%m-%d').tolist()!=[date]:
        raise ValueError('auction_date_or_row_count_mismatch')
    vals=[]
    for field in ['CLS_AUC','CLS_AUCVOL']:
        if field not in x: raise ValueError('required_auction_field_missing')
        v=pd.to_numeric(x[field],errors='coerce').iloc[0]
        if not np.isfinite(v) or v<=0: raise ValueError('auction_field_not_positive_finite')
        vals.append(float(v))
    return vals[0]

def premium(auction, midpoint):
    if not (np.isfinite(auction) and np.isfinite(midpoint) and auction>0 and midpoint>0):
        raise ValueError('invalid_price')
    return 10000*(auction/midpoint-1)

def signed_contrast(sign, comparison, rebalance):
    if sign not in [-1,1]: raise ValueError('invalid_direction')
    return sign*(rebalance-comparison)

def inputs():
    paths=[OUT/'FINAL_EXECUTION_SPEC.txt',OUT/'execute_locked_auction_pilot.py',
           OUT/'PRIMARY_CONTRAST_LOCK.txt',OUT/'PILOT_EVENTS.csv',
           OUT/'NASDAQ_2023_SESSION_EVIDENCE.txt',OUT/'RECOVERED_SHOF_DOCUMENT_NOTE.txt',
           PARENT/'CLOCK_METHOD_AMENDMENT.json',PARENT/'IDENTITY_ATTEMPT.json',
           PARENT/'REMAINING_ATTEMPTS.json']
    for ric,date,ident,digest,auc,ah in BOOKS:
        p=RAW/f'NASDAQ_2nd_level_orderbook_{ident}.csv.zip'
        assert sha(p)==digest
        paths.append(p)
        if auc:
            p=PARENT/'private'/auc
            assert sha(p)==ah
            paths.append(p)
    return {str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in paths}

def lock():
    save_new('FINAL_EXECUTION_LOCK.json',{'created_utc':datetime.now(timezone.utc).isoformat(),
      'auction_values_not_read':True,'economic_outcomes_not_computed':True,
      'inputs':inputs(),'modes':'source first; calculate only after the source-gate file passes'})

def verify_lock():
    frozen=json.loads((OUT/'FINAL_EXECUTION_LOCK.json').read_text())
    assert frozen['inputs']==inputs(), 'Locked input/code changed'

def source():
    verify_lock()
    events=pd.read_csv(OUT/'PILOT_EVENTS.csv').set_index('RIC')
    identity=json.loads((PARENT/'IDENTITY_ATTEMPT.json').read_text())
    current={z['Instrument']:z for z in identity['metadata']}
    attempts=json.loads((PARENT/'REMAINING_ATTEMPTS.json').read_text())
    request_map={z['private_file']:z for z in attempts['requests']}
    checks=[]
    for ric,date,ident,digest,auc,ah in BOOKS:
        x=frame(RAW/f'NASDAQ_2nd_level_orderbook_{ident}.csv.zip')
        e=events.loc[ric]
        expected={'isin':e.ISIN,'symbol':e.ticker,'date':date,'market':'XSTO','currency':'SEK'}
        for key,value in expected.items():
            assert set(x[key])=={value},f'identity/unit mismatch {ric} {date} {key}'
        cl=[clock_check(x,c) for c in ['exchange_local','UTC']]
        inferred=cl[0]['passes'] and not cl[1]['passes']
        q,_=select_quote(x)
        meta=current[ric]
        assert meta['ISIN_CODE']==e.ISIN and meta['CURRENCY']=='SEK'
        if auc:
            log=request_map[auc]; req=log['request']
            assert req['universe']==ric and req['start']==date and req['end']==date
            assert req['interval']=='1D' and req['adjustments']==['unadjusted']
            assert log['sha256']==ah and log['rows']==1
            assert log['numeric_nonmissing']['CLS_AUC']==1
            assert log['numeric_nonmissing']['CLS_AUCVOL']==1
        unknown={k:int(v) for k,v in x.status.value_counts().items() if k not in ['IOO','T']}
        checks.append({'RIC':ric,'date':date,'sha256':digest,'rows':len(x),
          'primary_2023':date.startswith('2023'), 'identity_and_dated_SHoF_SEK_pass':True,
          'current_LSEG_metadata_corroborates_only':True,'dated_identity_source':e.identity_source_url,
          'clock_candidates':cl,'local_clock_uniquely_conforms':bool(inferred),
          'unknown_status_counts_excluded_from_quote_selection':unknown,'quote':q,
          'primary_source_metadata_pass':bool(inferred and date.startswith('2023')),
          'book_auction_rows_after_17_25':int(pd.to_timedelta(x.time).ge(pd.Timedelta(hours=17,minutes=25)).sum())})
    primary=[c for c in checks if c['primary_2023']]
    assert len(primary)==4 and all(c['primary_source_metadata_pass'] for c in primary)
    save_new('CLOCK_VALIDATION.json',{'created_utc':datetime.now(timezone.utc).isoformat(),
       'economic_premiums_computed':False,
       'clock_label':'local exchange clock inferred from documented phase metadata; not explicitly declared by SHoF',
       'dated_schedule':'Nasdaq Nordic Market Model 2023_08 chapters3.3/4.2.1/4.2.4; primary November2023 only',
       'Bilia_2019_role':'summer-clock consistency check; no historical2019 schedule certification from2023document',
       'auction_value_gate':'not yet opened; run calculation mode only after this source check',
       'primary_metadata_gate_all_four_pass':True,'checks':checks})

def calculate():
    verify_lock()
    cpath=OUT/'CLOCK_VALIDATION.json'
    clock=json.loads(cpath.read_text())
    assert clock['primary_metadata_gate_all_four_pass']
    events=pd.read_csv(OUT/'PILOT_EVENTS.csv')
    sourcechecks=[]; aps={}
    for ric,date,ident,digest,auc,ah in BOOKS:
        if auc is None: continue
        x=frame(RAW/f'NASDAQ_2nd_level_orderbook_{ident}.csv.zip')
        q,mid=select_quote(x)
        p=PARENT/'private'/auc
        a=pd.read_csv(p)
        pa=auction_price(a,date)
        aps[(ric,date)]=premium(pa,mid)
        sourcechecks.append({'RIC':ric,'date':date,'auction_sha256':sha(p),
          'quote_source_sha256':digest,'exact_date_one_auction_row':True,
          'CLS_AUC_positive_finite':True,'CLS_AUCVOL_positive_finite_confirmation_only':True,
          'unadjusted_request':True,'raw_SEK_price_unit_conversion_factor':1,
          'source_gate_pass':True,'quote':q})
    rows=[]
    for e in events.itertuples():
        passed=(e.RIC,e.comparison_date) in aps and (e.RIC,e.auction_date) in aps
        r={'event_id':e.event_id,'review':e.review,'company':e.company,'RIC':e.RIC,
           'type':e.type,'direction':e.direction,'comparison_date':e.comparison_date,
           'rebalance_date':e.auction_date,'source_gate_pass':passed,
           'AP_comparison_bp':None,'AP_rebalance_bp':None,'signed_contrast_bp':None,
           'missing_reason':'' if passed else 'CLS_AUC_missing_on_both_locked_2019_dates; no_substitution',
           'clock_basis':'inferred_exchange_local_from_documented_phase_metadata' if passed else 'not_used',
           'economic_interpretation':'individual descriptive contrast; not causal index demand or execution cost'}
        if passed:
            ac=aps[(e.RIC,e.comparison_date)]; ar=aps[(e.RIC,e.auction_date)]
            r.update(AP_comparison_bp=ac,AP_rebalance_bp=ar,
                     signed_contrast_bp=signed_contrast(e.direction,ac,ar))
        rows.append(r)
    assert sum(r['source_gate_pass'] for r in rows)==2
    out=OUT/'INDIVIDUAL_AUCTION_CONTRASTS.csv'
    if out.exists(): raise FileExistsError('Preserve first calculation')
    pd.DataFrame(rows).to_csv(out,index=False,float_format='%.12f',na_rep='NA')
    save_new('FINAL_SOURCE_GATE_SUMMARY.json',{
      'created_utc':datetime.now(timezone.utc).isoformat(),'status':'completed_two_individual_2023_contrasts',
      'original_events':4,'passed_events':2,'passed_reviews':1,'missing_events':2,
      'clock_validation_sha256':sha(cpath),'execution_lock_sha256':sha(OUT/'FINAL_EXECUTION_LOCK.json'),
      'result_sha256':sha(out),'source_checks':sourcechecks,
      'clock_is_inference_not_vendor_timezone_declaration':True,
      '2019_missing_retained':True,'no_two_event_mean':True,'no_inference_or_causal_claim':True,
      'no_next_session_outcome_computed':True,'no_FTN_data':True,
      'price_gate_separate_from_unresolved_transaction_correction_or_volume_semantics':True,
      'historical_stage_files_superseded_only_for_the_four2023_primary_price_checks':True})
    print(pd.DataFrame(rows)[['event_id','source_gate_pass','AP_comparison_bp','AP_rebalance_bp','signed_contrast_bp']].to_string(index=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['lock','source','calculate'])
    {'lock':lock,'source':source,'calculate':calculate}[p.parse_args().mode]()
