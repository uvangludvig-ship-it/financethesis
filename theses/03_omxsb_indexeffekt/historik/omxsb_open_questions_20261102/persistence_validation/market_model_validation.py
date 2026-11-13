"""Independently reproduce the ALREADY DECLARED market-model sensitivity."""
from pathlib import Path
import os
import json
import pandas as pd
import numpy as np
from scipy.stats import linregress
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]));O=Path(__file__).resolve().parent
D=pd.read_csv(O/'original_inputs/event_paths.csv',parse_dates=['AD','ED'])
D=D[D.model.eq('market_model')&D.type.eq('addition')&D.post.eq(1)]
roles=['event','c1','c2','c3'];rics=set(D[[r+'_ric' for r in roles]].stack())
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
ix=ix[ix.ric.eq('.OMXSBGI')&ix.close.notna()].set_index('date').sort_index();cal=ix.index
mr=ix.close.pct_change(fill_method=None)*100
px=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','totret']);px.date=pd.to_datetime(px.date)
series={}
for r,g in px[px.ric.isin(rics)].groupby('ric'):
 g=g.set_index('date').reindex(cal);ret=g.totret.fillna(g.close.pct_change(fill_method=None)*100);ret[(ret>1000)|(ret<-100)]=np.nan;series[r]=ret
rows=[]
for e in D.to_dict('records'):
 a=cal.get_loc(e['AD']);z=cal.get_loc(e['ED'])
 for role in roles:
  r=e[role+'_ric'];y=series[r].iloc[a-250:a-120];x=mr.iloc[a-250:a-120];valid=y.notna()&x.notna()
  fit=linregress(x[valid],y[valid]) if valid.sum()>=100 else None
  for h in [1,20,60,100]:
   yy=series[r].iloc[a-1:z+h+1];xx=mr.iloc[a-1:z+h+1]
   v=(yy-fit.intercept-fit.slope*xx).sum() if fit is not None and yy.notna().all() and xx.notna().all() and len(yy)==z+h-a+2 else np.nan
   old=e[f'{role}_{h}']
   rows.append(dict(event_id=e['event_id'],role=role,ric=r,h=h,estimation_n=int(valid.sum()),alpha=fit.intercept if fit else np.nan,beta=fit.slope if fit else np.nan,raw_MM=v,saved_MM=old,same_missing=bool(pd.isna(v)==pd.isna(old)),absolute_difference=abs(v-old)))
F=pd.DataFrame(rows);F.to_csv(O/'market_model_reproduction.csv',index=False)
summary={'compared_cells':len(F),'all_missing_equal':bool(F.same_missing.all()),'max_absolute_difference':F.absolute_difference.max(),'fit_method':'scipy.stats.linregress on raw daily returns, independent of original least-squares/abnormal-return array','estimation_window':'AD-250 through AD-121 inclusive; at least100 observations'}
assert summary['all_missing_equal'];assert summary['max_absolute_difference']<1e-8
(O/'market_model_validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
