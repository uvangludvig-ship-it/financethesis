"""Source-only exact-RIC coverage; no return or event outcome calculations."""
from pathlib import Path
import os
import pandas as pd, json, hashlib
O=Path(os.environ.get('OMXSB_PRICE_WORKDIR',Path(__file__).resolve().parent))
P=Path(os.environ.get('OMXSB_REPO_ROOT','/Users/ludviguvang/dev/financethesis'))/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet'
I=P.parent/'indices_daily (1).csv'
E=pd.read_csv(O/'private/EARLY_CANDIDATES.csv'); E.candidate_ED=pd.to_datetime(E.candidate_ED)
fields=['close','totret','volume','bid','ask','mcap','shares']
S=pd.read_parquet(P,columns=['ric','date',*fields,'source'],filters=[('ric','in',sorted(E.ric.unique()))]);S.date=pd.to_datetime(S.date)
requests=[];parts=[];meta=[]
for ric,g in E.groupby('ric'):
 start=g.candidate_ED.min()-pd.Timedelta(days=400);end=g.candidate_ED.max()+pd.Timedelta(days=200)
 s=S.loc[S.ric.eq(ric)&S.date.between(start,end)].copy();parts.append(s)
 requests.append({'ric':ric,'start':str(start.date()),'end':str(min(end,pd.Timestamp('2006-12-31')).date()),'full_requested_end':str(end.date()),'candidate_count':len(g),'existing_rows':len(s),'existing_close':int(s.close.notna().sum())})
 for e in g.itertuples():
  x=s[s.date.between(e.candidate_ED-pd.Timedelta(days=400),e.candidate_ED+pd.Timedelta(days=200))]
  y=x[x.date.between(e.candidate_ED-pd.Timedelta(days=30),e.candidate_ED+pd.Timedelta(days=30))]
  meta.append({'candidate_id':e.candidate_id,'candidate_ED':str(e.candidate_ED.date()),'ric':ric,'rows_interval':len(x),'rows_close_near_ED_30calendar':int(y.close.notna().sum()),**{f'nonnull_{f}':int(x[f].notna().sum())for f in fields}})
R=pd.DataFrame(requests);R.to_csv(O/'private/REQUEST_UNIVERSE.csv',index=False)
F=pd.concat(parts,ignore_index=True);assert not F.duplicated(['ric','date']).any();F.to_csv(O/'private/EXISTING_PANEL_REUSE.csv.gz',index=False)
C=pd.DataFrame(meta);C.to_csv(O/'EXISTING_AVAILABILITY.csv',index=False)
idx=pd.read_csv(I,usecols=['ric','date','close']);idx.date=pd.to_datetime(idx.date);idx=idx[idx.ric.isin(['.OMXSBGI','.OMXSGI'])&idx.date.between(E.candidate_ED.min()-pd.Timedelta(days=400),E.candidate_ED.max()+pd.Timedelta(days=200))];idx.to_csv(O/'private/EXISTING_INDEX_REUSE.csv.gz',index=False)
a={'candidate_rows':len(E),'unique_RIC':len(R),'reviews':E.candidate_ED.nunique(),'exact_RIC_with_existing_rows':int(R.existing_rows.gt(0).sum()),'candidate_any_close_full_interval':int(C.nonnull_close.gt(0).sum()),'candidate_any_close_ED_plusminus30calendar':int(C.rows_close_near_ED_30calendar.gt(0).sum()),'by_review':C.groupby('candidate_ED').agg(candidates=('candidate_id','size'),any_close_near_ED=('rows_close_near_ED_30calendar',lambda x:int(x.gt(0).sum()))).reset_index().to_dict('records'),'existing_index':idx.groupby('ric').agg(rows=('date','size'),first=('date','min'),last=('date','max'),nonnull_close=('close','count')).astype(str).reset_index().to_dict('records'),'input_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [P,I,O/'private/EARLY_CANDIDATES.csv']},'notes':['Presence only; not complete estimation-window qualification','Existing totret naming merges Total Return and TotalReturn1D source headers; source-equivalence not certified by normalized name','No returns computed']}
(O/'EXISTING_AVAILABILITY_SUMMARY.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a,indent=2))
