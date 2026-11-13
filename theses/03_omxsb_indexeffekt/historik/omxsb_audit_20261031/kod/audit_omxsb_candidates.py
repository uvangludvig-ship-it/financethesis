"""Read-only Nasdaq sample and bounded October pilot linkage inventory; no returns."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/omxsb_audit_20261031'
path=OUT/'nasdaq_202002.xls'
x=pd.read_excel(path,sheet_name='Instrument Trading Details',header=None)
cols={0:'name',1:'company_code',2:'orderbook_code',3:'isin',4:'instrument_type',5:'segment',
      6:'industry',7:'supersector',13:'currency',14:'location',15:'delisted',17:'listed_shares',
      18:'market_cap',22:'turnover_month',56:'turnover_12m'}
s=x.iloc[6:].rename(columns=cols)[list(cols.values())]
s=s[s.location.eq('STO') & s['isin'].notna()].copy()
s['is_preference_name']=s.name.str.contains('pref',case=False,na=False)
s['reference_date']='2020-02-28'
s['published_at']='2020-03-23 13:08:10 CET'
s['source']='https://attachment.news.eu.nasdaq.com/a8cb43b3dac4a07770fd3957b8858b42a'
static=pd.read_csv(ROOT/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv')
static12=pd.read_csv(ROOT/'data/raw/lseg/panel_2012_2026/stocks_static.csv')
mapping=pd.concat([static[['ric','IssueISIN']],static12[['ric','IssueISIN']]]).dropna().drop_duplicates()
mm=mapping.groupby('IssueISIN').ric.agg(lambda z:';'.join(sorted(set(z))))
s['static_isin_rics']=s['isin'].map(mm)
s['historical_link_verified']=False
s.to_csv(OUT/'nasdaq_202002_instrument_sample.csv',index=False)
ev=pd.read_csv(ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
pilot=ev[ev.review_cycle.isin(['2019H2','2024H2'])].copy()
pilot['reference_month']=pilot.effective_date.str[:4]+'-10'
pilot['official_candidate_file_verified']=False
pilot['historical_identifier_link_verified']=False
pilot['status']='Event target verified locally; October candidate XLS not retrieved; no prediction or return test'
pilot.to_csv(OUT/'candidate_pilot_targets.csv',index=False)
summary={'sample_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'sample_sheet':'Instrument Trading Details','stockholm_instruments':len(s),
         'instrument_types':s.instrument_type.value_counts().to_dict(),
         'preference_names_labeled_stock':int((s.is_preference_name & s.instrument_type.eq('Stock')).sum()),
         'static_isin_matched':int(s.static_isin_rics.notna().sum()),
         'free_float_present':False,'historical_links_verified':0,
         'pilot_targets':pilot.groupby(['review_cycle','type']).size().to_dict()}
summary['pilot_targets']={str(k):int(v) for k,v in summary['pilot_targets'].items()}
(OUT/'candidate_sample_summary.json').write_text(json.dumps(summary,indent=2))
print(summary)
