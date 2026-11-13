#!/usr/bin/env python3
"""Read-only pre-2007 source presence audit. No returns/effects are computed."""
import datetime,hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
R=Path('/Users/ludviguvang/dev/financethesis');O=Path(__file__).resolve().parent
files={'panel':R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet','index_main':R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv','index_extra':R/'data/raw/lseg/panel_2005_2026/indices_daily_extra.csv','static':R/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv','modern_census':R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv','baseline_events':R/'output/omxsb_replication_2007/events_car.csv','notebook':R/'code/notebooks/replication_omxsb_2007.ipynb','mechanisms':R/'code/build/mechanisms_2007.py','workbook_audit':R/'output/omxsb_scaled_round_20261103/workbook_audit/WORKBOOK_AUDIT_SUMMARY.json'}
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
assert not(O/'SOURCE_PRESENCE_LOCK.json').exists()
(O/'SOURCE_PRESENCE_LOCK.json').write_text(json.dumps({'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rule':'Only dates/identifiers and pre2007 finite-value presence flags. Never compute price changes or event outcomes. Baseline outcome file only hashed and event-ID/type/cycle columns read.','inputs':{k:{'path':str(v),'sha256':sha(v)}for k,v in files.items()}},indent=2)+'\n')
cols=['ric','date','close','totret','volume','mcap','shares','bid','ask','source']
P=pd.read_parquet(files['panel'],columns=cols,filters=[('date','<',pd.Timestamp('2007-01-01'))]);P['year']=P.date.dt.year
counts=[]
for y,z in P.groupby('year'):
 v={'year':int(y),'rows':len(z),'rics':z.ric.nunique(),'first_date':str(z.date.min().date()),'last_date':str(z.date.max().date())}
 for c in cols[2:-1]:v[c+'_finite_rows']=int(np.isfinite(pd.to_numeric(z[c],errors='coerce')).sum())
 counts.append(v)
I=[]
for key in ['index_main','index_extra']:
 f=pd.read_csv(files[key],usecols=['ric','date','close'],parse_dates=['date']);f=f[f.date.lt('2007-01-01')]
 for ric,z in f.groupby('ric'):
  good=z[np.isfinite(pd.to_numeric(z.close,errors='coerce'))]
  I.append({'source':key,'ric':ric,'pre2007_rows':len(z),'finite_rows':len(good),'first_date':str(good.date.min().date()) if len(good) else None,'last_date':str(good.date.max().date()) if len(good) else None})
S=pd.read_csv(files['static'],usecols=['ric','first_date','last_date'],parse_dates=['first_date','last_date'])
B=pd.read_csv(files['baseline_events'],usecols=['event_id','type','review_cycle'] if 'review_cycle' in pd.read_csv(files['baseline_events'],nrows=0).columns else ['event_id','type','cycle'])
E=pd.read_csv(files['modern_census'],usecols=['event_id','RIC','effective_date'],parse_dates=['effective_date'])
out={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_effects_computed':False,'pre2007_panel':counts,'pre2007_index_presence':I,'static_earliest_date':str(S.first_date.min().date()),'modern_census_rows':len(E),'modern_event_ids_unique':bool(E.event_id.is_unique),'baseline_event_rows':len(B),'baseline_event_ids_unique':bool(B.event_id.is_unique),'baseline_by_type':B.groupby('type').size().to_dict(),'baseline_review_count':int(B['review_cycle' if 'review_cycle'in B else 'cycle'].nunique())}
(O/'SOURCE_PRESENCE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
