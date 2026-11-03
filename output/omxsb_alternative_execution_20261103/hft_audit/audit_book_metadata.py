"""Source-only checks for a locked SHoF instrument-day; never computes a midpoint."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,gzip,hashlib,json
import pandas as pd

def audit(p, expected_isin, expected_date):
    with p.open('rb') as f:magic=f.read(2)
    op=gzip.open if magic==b'\x1f\x8b' else open
    with op(p,'rt') as f:x=pd.read_csv(f,sep=';',dtype=str,keep_default_na=False)
    required=['symbol','isin','date','time','askpx1','asksz1','bidpx1','bidsz1','txpx','txsz','status','market','currency','instrumentid']
    assert set(required)<=set(x.columns)
    assert set(x['isin'])=={expected_isin} and set(x['date'])=={expected_date}
    missing=x.apply(lambda c:c.str.strip().str.lower().isin(['','na','n/a','null','none','nan']))
    tm=pd.to_timedelta(x.time)
    q=x[['bidpx1','askpx1','bidsz1','asksz1']].apply(pd.to_numeric,errors='coerce')
    valid=q.notna().all(axis=1)&q.gt(0).all(axis=1)&q.bidpx1.le(q.askpx1)
    tx=~missing.txpx&~missing.txsz
    before=valid&tm.lt(pd.Timedelta(hours=17,minutes=25))
    last=x.loc[before,'time'].max() if before.any() else None
    lastrows=x.loc[before&x.time.eq(last)] if last else x.iloc[:0]
    statuses=[]
    for status,g in x.groupby('status',sort=False):
        statuses.append({'status':status,'rows':len(g),'first_time_as_exported':g.time.min(),
                        'last_time_as_exported':g.time.max(),'rows_with_tx_fields':int(tx.loc[g.index].sum())})
    return {'created_utc':datetime.now(timezone.utc).isoformat(),'private_source_path':str(p.resolve()),
      'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'rows':len(x),
      'source_only':True,'economic_outcomes_computed':False,'columns':x.columns.tolist(),
      'expected_isin':expected_isin,'expected_date':expected_date,
      'identity':{c:x[c].unique().tolist() for c in ['symbol','isin','date','market','currency','instrumentid']},
      'missing_by_column':{c:int(missing[c].sum()) for c in x},'phase_coverage':statuses,
      'exact_duplicate_extra_rows':int(x.duplicated().sum()),
      'timestamp_instrument_duplicate_extra_rows':int(x.duplicated(['date','time','instrumentid']).sum()),
      'nonmonotonic_time_transitions':int(tm.diff().lt(pd.Timedelta(0)).sum()),
      'rows_with_positive_uncrossed_quote_and_positive_sizes':int(valid.sum()),
      'rows_at_or_after_17_25_as_exported':int(tm.ge(pd.Timedelta(hours=17,minutes=25)).sum()),
      'candidate_last_pre_17_25_quote_if_export_clock_local':last,
      'candidate_quote_age_seconds_if_export_clock_local':float((pd.Timedelta(hours=17,minutes=25)-pd.to_timedelta(last)).total_seconds()) if last else None,
      'candidate_last_time_rows':len(lastrows),'distinct_top_quote_states_at_candidate_time':len(lastrows[['bidpx1','askpx1']].drop_duplicates()),
      'timezone_status':'NOT_DOCUMENTED: candidate clock diagnostic does not certify local time',
      'primary_gate_pass':False,'primary_gate_reason':'Await timezone/session provenance and separate genuine final-auction price/unit validation.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('--isin',required=True)
    ap.add_argument('--date',required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    if a.out.exists():raise FileExistsError('Use a new output filename to preserve source audit history')
    out=audit(a.input,a.isin,a.date)
    a.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['sha256','rows','expected_isin','expected_date','phase_coverage',
       'candidate_last_pre_17_25_quote_if_export_clock_local','candidate_quote_age_seconds_if_export_clock_local',
       'distinct_top_quote_states_at_candidate_time','primary_gate_pass']},indent=2))
