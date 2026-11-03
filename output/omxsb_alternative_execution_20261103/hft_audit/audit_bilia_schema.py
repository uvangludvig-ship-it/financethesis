"""Frozen one-day source semantics audit: no prices/volumes/returns summarized."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json
import pandas as pd

OUT=Path(__file__).resolve().parent
RAW=Path('/Users/ludviguvang/dev/financethesis/data/raw/shof/Reinvestments/hft_pilot_20261103/NASDAQ_2nd_level_orderbook_1793732319625.csv.zip')
assert hashlib.sha256(RAW.read_bytes()).hexdigest()=='b965282b2d3e4f07c5e7cc144761fbf8cda944caec9f297662a86fa1a0e95564'
with gzip.open(RAW,'rt') as f:x=pd.read_csv(f,sep=';',dtype=str,keep_default_na=False)
missing=x.apply(lambda c:c.str.strip().str.lower().isin(['','na','n/a','null','none','nan']))
time=pd.to_timedelta(x.time)
tx=(~missing.txpx)&(~missing.txsz)
txpartial=missing.txpx.ne(missing.txsz)
book=['askpx1','asksz1','bidpx1','bidsz1','askpx2','asksz2','bidpx2','bidsz2']
txfields=['txpx','txsz','buyer','seller']
same_tx=x[txfields].eq(x[txfields].shift()).all(axis=1)&tx&tx.shift(fill_value=False)
bookchange=~x[book].eq(x[book].shift()).all(axis=1)
px=x[['bidpx1','askpx1']].apply(pd.to_numeric,errors='coerce')
validquote=px.notna().all(axis=1)&px.gt(0).all(axis=1)&px.bidpx1.le(px.askpx1)
pre_if_local=validquote&time.lt(pd.Timedelta(hours=17,minutes=25))
last_quote_time=x.loc[pre_if_local,'time'].max()
last_quote_rows=x.loc[pre_if_local&x.time.eq(last_quote_time)]
phase=[]
for status,g in x.groupby('status',sort=False):
    ii=g.index
    phase.append({'status':status,'rows':len(g),'first_time_as_exported':g.time.min(),
      'last_time_as_exported':g.time.max(),'rows_with_transaction_fields':int(tx.loc[ii].sum()),
      'rows_with_valid_uncrossed_positive_top_quote':int(validquote.loc[ii].sum())})
timestampkey=['date','time','instrumentid']
result={'created_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest(),
 'source_only':True,'outcome_contrasts_computed':False,'rows':len(x),
 'identity':{c:x[c].unique().tolist() for c in ['symbol','isin','date','market','currency','instrumentid']},
 'gzip_magic_despite_zip_suffix':True,'nonmonotonic_timestamp_transitions':int(time.diff().lt(pd.Timedelta(0)).sum()),
 'duplicate_date_time_instrument_extra_rows':int(x.duplicated(timestampkey).sum()),
 'exact_duplicate_extra_rows':int(x.duplicated().sum()),
 'missing_by_column':{c:int(missing[c].sum()) for c in x},
 'transaction_field_present_rows':int(tx.sum()),'partial_transaction_field_rows':int(txpartial.sum()),
 'adjacent_rows_same_nonmissing_tx_fields':int(same_tx.sum()),
 'adjacent_same_tx_fields_with_changed_book':int((same_tx&bookchange).sum()),
 'reused_tx_tuple_extra_rows_total':int(x.loc[tx].duplicated(txfields).sum()),
 'last_valid_pre_17_25_quote_time_if_clock_local':last_quote_time,
 'rows_at_last_valid_pre_17_25_quote_time':len(last_quote_rows),
 'distinct_top_quote_states_at_that_time':len(last_quote_rows[['bidpx1','askpx1']].drop_duplicates()),
 'rows_after_or_at_17_25_as_exported':int(time.ge(pd.Timedelta(hours=17,minutes=25)).sum()),
 'phase_coverage':phase,
 'stop_reasons':['Closing-auction execution is not explicitly identified in this schema.',
                 'No rows at/after 17:25 in the exported clock; full reconstruction does not contain the expected local closing-auction period.',
                 'Source timezone is not yet documented; raw ITCH UTC cannot be silently assigned to this transformed export.',
                 'No execution/match ID or correction/cancellation links; exact-row uniqueness does not prove unique trades.'],
 'interpretation_notes':['Repeated identical transaction tuples may represent separate genuine trades or repeated snapshots; counts alone do not license deduplication.',
                         'N/A tokens are missing, never zeros. BILIA_SCHEMA_INVENTORY_v2.json supersedes initial missingness counts, which omitted N/A.',
                         'QTA is observed at five dispersed intraday times, so it must not be labelled closing auction from its name alone.',
                         'No raw price/quantity/participant values are exported by this script.']}
(OUT/'BILIA_SOURCE_SEMANTICS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['rows','transaction_field_present_rows','partial_transaction_field_rows',
 'adjacent_rows_same_nonmissing_tx_fields','adjacent_same_tx_fields_with_changed_book',
 'reused_tx_tuple_extra_rows_total','duplicate_date_time_instrument_extra_rows','phase_coverage']},indent=2))
