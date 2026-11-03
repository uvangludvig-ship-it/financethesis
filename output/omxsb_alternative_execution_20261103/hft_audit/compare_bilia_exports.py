"""Compare raw source records without numerical trade/quote outcomes."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json
import pandas as pd

OUT=Path(__file__).resolve().parent
RAW=Path('/Users/ludviguvang/dev/financethesis/data/raw/shof/Reinvestments/hft_pilot_20261103')
paths={'full':RAW/'NASDAQ_2nd_level_orderbook_1793732319625.csv.zip',
       'transaction':RAW/'NASDAQ_2nd_level_orderbook_1793732601269.csv.zip'}
frames={}
for k,p in paths.items():
    with gzip.open(p,'rt') as f:frames[k]=pd.read_csv(f,sep=';',dtype=str,keep_default_na=False)
f,t=frames['full'],frames['transaction']
is_missing=lambda c:c.str.strip().str.lower().isin(['','na','n/a','null','none','nan'])
present=~is_missing(f.txpx)&~is_missing(f.txsz)
assert set(f.columns)-set(t.columns)=={'buyer','seller'}
assert set(t.columns)<=set(f.columns)
expected=f.loc[present,t.columns].reset_index(drop=True)
same_shape=expected.shape==t.shape
equal_cells=expected.eq(t) if same_shape else None
result={'created_utc':datetime.now(timezone.utc).isoformat(),'source_only':True,
 'inputs':{k:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in paths.items()},
 'full_rows':len(f),'full_rows_with_both_tx_fields':int(present.sum()),'transaction_rows':len(t),
 'removed_columns':['buyer','seller'],'same_shape':same_shape,
 'all_shared_cells_equal_in_original_row_order':bool(same_shape and equal_cells.all().all()),
 'different_shared_cells':int((~equal_cells).sum().sum()) if same_shape else None,
 'transaction_first_time_as_exported':t.time.min(),'transaction_last_time_as_exported':t.time.max(),
 'transaction_status_counts':t.status.value_counts().to_dict(),
 'transaction_rows_at_or_after_17_25_as_exported':int(pd.to_timedelta(t.time).ge(pd.Timedelta(hours=17,minutes=25)).sum()),
 'result':'The transaction option is exactly the existing full reconstruction restricted to nonmissing transaction fields, with participant columns removed. It provides no extra closing-auction records.',
 'limitation':'One instrument-day proves equality for this file pair only. It does not prove all other SHoF days omit auctions or establish why this day has no closing-auction row.',
 'numeric_price_volume_return_outcomes_computed':False}
assert result['all_shared_cells_equal_in_original_row_order']
(OUT/'BILIA_EXPORT_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='inputs'},indent=2))
