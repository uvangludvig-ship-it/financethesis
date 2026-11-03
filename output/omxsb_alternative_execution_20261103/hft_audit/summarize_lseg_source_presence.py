"""Join parent-owned request metadata to the frozen pilot; no licensed values read."""
from pathlib import Path
import json,hashlib
import pandas as pd

OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'auction_source'
paths=[SRC/'ATTEMPTS.json',SRC/'REMAINING_ATTEMPTS.json',SRC/'MINUTE_2023_ATTEMPTS.json']
logs=[json.loads(p.read_text()) for p in paths]
rows=[]
for r in logs[0]['requests']:
    rows.append(dict(RIC=logs[0]['instrument'],date=r['date_requested'],interval='1D',rows=r['rows'],
        returned_date=r['dates_returned'][0][:10] if r['rows'] else None,
        CLS_AUC_nonmissing=r['numeric_nonmissing'].get('CLS_AUC',0),
        CLS_AUCVOL_nonmissing=r['numeric_nonmissing'].get('CLS_AUCVOL',0),
        OFF_CLOSE_column_present='OFF_CLOSE' in r['columns'],raw_sha256=r['sha256']))
for log in logs[1:]:
    for r in log['requests']:
        q=r['request']
        rows.append(dict(RIC=q['universe'],date=q['start'][:10],interval=q['interval'],rows=r['rows'],
           returned_date=r['first_index'][:10] if r['rows'] else None,
           CLS_AUC_nonmissing=r['numeric_nonmissing'].get('CLS_AUC',0),
           CLS_AUCVOL_nonmissing=r['numeric_nonmissing'].get('CLS_AUCVOL',0),
           OFF_CLOSE_column_present='OFF_CLOSE' in r['columns'],raw_sha256=r['sha256']))
allrequests=pd.DataFrame(rows)
daily=allrequests.loc[allrequests.interval.eq('1D')].copy()
assert not daily.duplicated(['RIC','date']).any()
expected=pd.read_csv(OUT/'PILOT_REQUEST_SESSIONS.csv',dtype=str)
expected=expected.loc[expected.session_role.isin(['comparison','rebalance'])]
joined=expected.merge(daily,on=['RIC','date'],how='left',validate='one_to_one')
assert len(joined)==8 and joined.rows.eq(1).all() and joined.date.eq(joined.returned_date).all()
joined['documented_auction_field_present']=joined.CLS_AUC_nonmissing.eq(1)
joined['primary_source_gate_pass']=False
joined['reason']='Await quote clock/session and price units; presence alone is not source certification.'
joined.loc[~joined.documented_auction_field_present,'reason']='Final auction price missing; no ordinary-close substitution.'
joined.to_csv(OUT/'LSEG_LOCKED_PRIMARY_SOURCE_COVERAGE.csv',index=False)
summary={'source_only':True,'price_values_read':False,'fixed_primary_cells':8,
 'final_auction_price_field_nonmissing_cells':int(joined.documented_auction_field_present.sum()),
 'final_auction_price_missing_cells':int((~joined.documented_auction_field_present).sum()),
 'native_intraday_requests':int(allrequests.interval.eq('1min').sum()),
 'native_intraday_total_rows':int(allrequests.loc[allrequests.interval.eq('1min'),'rows'].sum()),
 'underlying_source_response_hashes':joined.raw_sha256.tolist(),
 'input_metadata_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
 'interpretation':'Four2023 daily auction-price fields are present; all four2019 cells are missing. Presence is not proof of validated price/time/unit alignment. No new economic outcome computed.'}
(OUT/'LSEG_SOURCE_PRESENCE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['fixed_primary_cells','final_auction_price_field_nonmissing_cells',
 'final_auction_price_missing_cells','native_intraday_requests','native_intraday_total_rows']},indent=2))
