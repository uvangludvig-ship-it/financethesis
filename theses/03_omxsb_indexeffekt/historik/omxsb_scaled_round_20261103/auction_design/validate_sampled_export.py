"""Compare fixed sampled SHoF exports to five full books; no price outcomes/export."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,gzip,zipfile,io,json,hashlib
import numpy as np
import pandas as pd

R=Path('/Users/ludviguvang/dev/financethesis/data/raw/shof/Reinvestments/hft_pilot_20261103')
FIXED=[('SE0009921588','2019-05-31','1793732319625'),
 ('SE0007692850','2023-11-23','1793733524718'),('SE0007692850','2023-11-30','1793733549086'),
 ('SE0005999836','2023-11-23','1793733618890'),('SE0005999836','2023-11-30','1793733672616')]
TOP=['bidpx1','askpx1','bidsz1','asksz1']
TOL=1e-10

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 b=p.read_bytes()
 if b[:2]==b'\x1f\x8b':parts=[(p.name,gzip.decompress(b))]
 elif b[:2]==b'PK':
  with zipfile.ZipFile(io.BytesIO(b)) as z:parts=[(n,z.read(n)) for n in z.namelist() if n.lower().endswith('.csv')]
 else:parts=[(p.name,b)]
 out=[]
 for name,raw in parts:
  x=pd.read_csv(io.BytesIO(raw),sep=';',dtype=str,keep_default_na=False)
  x.columns=x.columns.str.strip().str.lower()
  required=set(['isin','date','time','status','currency','market']+TOP)
  if not required.issubset(x.columns):raise ValueError(f'Missing schema fields: {sorted(required-set(x.columns))}')
  x['_source_member']=name;out.append(x)
 return pd.concat(out,ignore_index=True)

def equal(a,b):
 # Preserved missing fields are source-equivalent, never numeric zero.
 # The terminal quote is separately required to be positive and finite.
 both_missing=np.isnan(a)&np.isnan(b)
 numeric=np.isfinite(a)&np.isfinite(b)&np.isclose(a,b,atol=TOL,rtol=0,equal_nan=False)
 return bool(np.all(both_missing|numeric))
def terminal(x):
 t=pd.to_timedelta(x.time);q=x[TOP].apply(pd.to_numeric,errors='coerce');cut=pd.Timedelta(hours=17,minutes=25)
 good=x.status.eq('T')&np.isfinite(q).all(axis=1)&q.gt(0).all(axis=1)&q.bidpx1.le(q.askpx1)&t.ge(cut-pd.Timedelta(seconds=60))&t.lt(cut)
 if not good.any():return None,None
 tm=t[good].max();st=q.loc[good&t.eq(tm)].drop_duplicates()
 if len(st)!=1:raise ValueError('Full book final quote ambiguity')
 return tm,st.iloc[0].to_numpy(dtype=float)

def compare(full,sampled,seconds):
 freq=f'{seconds}s';step=pd.Timedelta(seconds=seconds)
 ft=pd.to_timedelta(full.time);st=pd.to_timedelta(sampled.time)
 fq=full[TOP].apply(pd.to_numeric,errors='coerce');sq=sampled[TOP].apply(pd.to_numeric,errors='coerce')
 fq['_bucket']=ft.dt.floor(freq);fq['_T']=full.status.eq('T')
 groups={k:g[TOP] for k,g in fq.loc[fq._T].groupby('_bucket')}
 cut=pd.Timedelta(hours=17,minutes=25);lo=pd.Timedelta(hours=9,minutes=1)
 fulltime,fullstate=terminal(full)
 candidates=[]
 for label,offset in [('start_or_original_timestamp',pd.Timedelta(0)),('end_label',step)]:
  bins=st.dt.floor(freq)-offset
  for method in ['first','last','arithmetic_snapshot_mean']:
   tested=matched=extra=0;endstates=[];endtimes=[]
   for idx in sampled.index[sampled.status.eq('T')&bins.ge(lo)&bins.lt(cut)]:
    k=bins[idx];g=groups.get(k)
    if g is None:extra+=1;continue
    if method=='first':expected=g.iloc[0].to_numpy(dtype=float)
    elif method=='last':expected=g.iloc[-1].to_numpy(dtype=float)
    else:expected=g.mean().to_numpy(dtype=float) if g.notna().all().all() else np.full(4,np.nan)
    actual=sq.loc[idx].to_numpy(dtype=float);tested+=1;matched+=int(equal(actual,expected))
    if k==cut-step:
     endstates.append(actual);endtimes.append(st[idx])
   terminal_unique=bool(len(endstates)==1)
   tm_match=bool(terminal_unique and fullstate is not None and equal(endstates[0],fullstate))
   candidates.append({'timestamp_interpretation':label,'aggregation':method,
      'compared_continuous_rows':tested,'four_field_equal_rows':matched,
      'sampled_rows_in_bins_without_full_T_updates':extra,
      'terminal_bin_rows':len(endstates),'terminal_quote_equal_to_full':tm_match,
      'terminal_original_timestamp_retained':bool(tm_match and endtimes[0]==fulltime),
      'all_compared_rows_match':bool(tested>0 and matched==tested),
      'terminal_bin_has_actual_full_update':bool(cut-step in groups)})
 last=[z for z in candidates if z['aggregation']=='last' and z['all_compared_rows_match'] and z['terminal_quote_equal_to_full']]
 return {'full_rows':len(full),'sampled_rows':len(sampled),'sampling_interval_seconds':seconds,
  'full_exact_terminal_time':str(fulltime),'sampled_first_time':sampled.time.min(),'sampled_last_time':sampled.time.max(),
  'sampled_nonmonotonic_transitions':int(st.diff().lt(pd.Timedelta(0)).sum()),
  'sampled_exact_duplicate_extra_rows':int(sampled.drop(columns=['_source_member']).duplicated().sum()),
  'sampled_duplicate_time_extra_rows':int(sampled.duplicated(['date','time']).sum()),
  'sampled_status_counts':sampled.status.value_counts().to_dict(),
  'sampled_nonzero_subsecond_timestamp_rows':int((st%pd.Timedelta(seconds=1)).ne(pd.Timedelta(0)).sum()),
  'candidates':candidates,'coherent_last_snapshot_terminal_equivalence':bool(last),
  'equivalent_last_rules':[(z['timestamp_interpretation']) for z in last],
  'source_supported_original_freshness':bool(last and any(z['terminal_original_timestamp_retained'] for z in last)),
  'requires_explicit_bin_label_or_carry_forward_assessment':bool(last and not any(z['terminal_original_timestamp_retained'] for z in last)),
  'no_economic_outcomes_computed':True}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,nargs='+',required=True)
 ap.add_argument('--interval',choices=['minute','second'],required=True);ap.add_argument('--out',type=Path,required=True)
 a=ap.parse_args()
 if a.out.exists():raise FileExistsError('Preserve every source-validation run')
 x=pd.concat([load(p) for p in a.input],ignore_index=True);checks=[]
 for isin,date,ident in FIXED:
  s=x.loc[x['isin'].eq(isin)&x.date.eq(date)].copy().reset_index(drop=True)
  p=R/f'NASDAQ_2nd_level_orderbook_{ident}.csv.zip';f=load(p)
  if s.empty:
   checks.append({'ISIN':isin,'date':date,'status':'missing_fixed_source_day'});continue
  assert set(s.currency)=={'SEK'} and set(s.market)=={'XSTO'}
  assert set(f['isin'])=={isin} and set(f.date)=={date}
  z=compare(f,s,60 if a.interval=='minute' else 1)
  checks.append({'ISIN':isin,'date':date,'full_source_sha256':sha(p),'status':'compared'}|z)
 selected={(i,d) for i,d,_ in FIXED}
 ignored=sorted({(i,d) for i,d in zip(x['isin'],x.date)}-selected)
 out={'created_utc':datetime.now(timezone.utc).isoformat(),'source_only':True,'no_new_auction_premiums':True,
  'interval':a.interval,'absolute_comparison_tolerance':TOL,
  'inputs':{str(p):sha(p) for p in a.input},'script_sha256':sha(Path(__file__)),
  'ignored_extra_instrument_days':ignored,'fixed_checks':checks,
  'all_five_terminal_last_snapshot_equivalent':all(c.get('coherent_last_snapshot_terminal_equivalence',False) for c in checks),
  'all_five_original_terminal_update_times_retained':all(c.get('source_supported_original_freshness',False) for c in checks),
  'broad_outcome_gate':'NOT_OPENED: source assessment, dated identities/overlaps and actual common support must be frozen first'}
 a.out.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
 print(json.dumps({k:out[k] for k in ['interval','all_five_terminal_last_snapshot_equivalent','all_five_original_terminal_update_times_retained','broad_outcome_gate']},indent=2))
