"""Independent CSV-header/raw-presence verification; never export source price values."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,math,hashlib
import pandas as pd
O=Path(__file__).resolve().parent;P=O.parent/'coverage'
log=json.loads((P/'FETCH_LOG.json').read_text());provided=pd.read_csv(P/'SOURCE_PRESENCE.csv')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def finite(s):
 try:return int(math.isfinite(float(s)))
 except (TypeError,ValueError):return 0
out=[];sources=[]
for l in log['requests']:
 q=l['request'];p=P/'private'/l['private_file'];assert sha(p)==l['sha256']
 with p.open() as f:raw=list(csv.reader(f))
 assert len(raw)>=4 and raw[2][0]=='Date'
 keys=list(zip(raw[0][1:],raw[1][1:]));assert len(keys)==len(set(keys))
 data=raw[3:];assert len(data)==1
 date=pd.Timestamp(data[0][0]).strftime('%Y-%m-%d');assert date==q['date']
 vals=dict(zip(keys,data[0][1:]));missingcolumns=[]
 for ric in q['universe']:
  row={'review':q['review'],'date':date,'role':q['role'],'RIC':ric,'exact_requested_date':True}
  for field in ['CLS_AUC','CLS_AUCVOL','TRDPRC_1']:
   if (ric,field) not in vals:missingcolumns.append([ric,field])
   row[field+'_finite']=finite(vals.get((ric,field)))
  out.append(row)
 assert not missingcolumns, 'Requested field omitted, cannot equate to numeric NA'
 sources.append({'request_number':l['number'],'sha256':sha(p),'requested_RICs':len(q['universe']),
                 'unique_RIC_field_columns':len(keys),'exact_date':True,'all_requested_fields_have_columns':True})
D=pd.DataFrame(out);keys=['review','date','role','RIC'];assert not D.duplicated(keys).any()
joined=D.merge(provided,on=keys,validate='one_to_one',suffixes=('_ind','_provided'));assert len(joined)==len(D)==len(provided)
for field in ['CLS_AUC_finite','CLS_AUCVOL_finite','TRDPRC_1_finite','exact_requested_date']:
 assert (joined[field+'_ind']==joined[field+'_provided']).all(),field
review=D.groupby('review').agg(requested_stock_dates=('RIC','size'),auction_present_stock_dates=('CLS_AUC_finite','sum'),auctionvolume_present_stock_dates=('CLS_AUCVOL_finite','sum'),lasttrade_present_stock_dates=('TRDPRC_1_finite','sum')).reset_index()
review.to_csv(O/'INDEPENDENT_SOURCE_COUNTS_BY_REVIEW.csv',index=False)
pre=D[D.review.lt('2023H1')];post=D[D.review.ge('2023H1')]
result={'created_utc':datetime.now(timezone.utc).isoformat(),'source_only':True,'no_premiums_returns_or_price_values_exported':True,
 'requests_verified':len(sources),'stock_date_presence_rows':len(D),'all_provided_presence_flags_reproduced':True,
 'independent_method':'csv.reader multirow headers + original data cells, not producer extraction code',
 'pre2023_stock_dates':len(pre),'pre2023_CLS_AUC_present':int(pre.CLS_AUC_finite.sum()),
 'pre2023_TRDPRC_1_present':int(pre.TRDPRC_1_finite.sum()),'2023_stock_dates':len(post),'2023_CLS_AUC_present':int(post.CLS_AUC_finite.sum()),
 'reviews_with_auction_presence':review.loc[review.auction_present_stock_dates.gt(0),'review'].tolist(),
 'interpretation':'Only two pre2024 reviews have auction fields in these exact daily get_history queries. This is not proof that no other legitimate LSEG product or raw Nasdaq source has earlier auctions.',
 'inference_gate':'NO broader review-population inferential analysis from only two reviews; source-stage restriction before new broad AP outcomes.',
 'inputs':{'FETCH_LOG_sha256':sha(P/'FETCH_LOG.json'),'SOURCE_PRESENCE_sha256':sha(P/'SOURCE_PRESENCE.csv')},
 'source_checks':sources,'script_sha256':sha(Path(__file__))}
(O/'INDEPENDENT_SOURCE_PRESENCE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['source_checks','inputs']},indent=2))
