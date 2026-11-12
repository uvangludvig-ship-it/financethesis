"""Aggregate existing share-class legs and public review dates for the DD.

Usage: python summarize_twins_and_timing.py PATH_TO_THESIS_FINAL OUTPUT_DIRECTORY
No security- or fund-level observations are exported.
"""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
src,out=map(Path,sys.argv[1:3]);out.mkdir(parents=True,exist_ok=True)
t=pd.read_csv(src/'results/twins/twin_results_events.csv')
w='primär [AD-1,ED+1]'
assert np.allclose(t[w],t[w+' indexslag']-t[w+' systerslag'],atol=1e-8)
rows=[]
for ty,g in t.groupby('type'):
 rows.append(dict(type=ty,n=len(g),firms=g.firm.nunique(),signed_index=g[w+' indexslag'].mean(),signed_sister=g[w+' systerslag'].mean(),signed_difference=g[w].mean()))
pd.DataFrame(rows).to_csv(out/'twin_leg_descriptive_summary.csv',index=False)
e=pd.read_csv(src/'data/events/omxsb_changes_with_car_2007_2026.csv',parse_dates=['AD','ED','announcement_date','effective_date'])
r=e.groupby('review_cycle').agg(AD=('AD','first'),ED=('ED','first'),announcement=('announcement_date','first'),effective=('effective_date','first'),n=('event_id','size'),AD_unique=('AD','nunique'),ED_unique=('ED','nunique'))
idx=pd.read_csv(src/'data/prices/index_levels_daily_2004_2026.csv',parse_dates=['date']);cal=pd.DatetimeIndex(idx.loc[(idx.ric=='.OMXSBGI')&idx.close.notna(),'date'].sort_values().unique());pos=pd.Series(range(len(cal)),index=cal)
r['lag_trading_days']=r.ED.map(pos)-r.AD.map(pos)
assert (r.AD_unique==1).all() and (r.ED_unique==1).all()
r.reset_index().to_csv(out/'review_timing_summary.csv',index=False)
(out/'twins_timing_summary_validation.json').write_text(json.dumps({'share_class_event_count':len(t),'share_class_firm_count':int(t.firm.nunique()),'max_leg_difference_discrepancy':float(abs(t[w]-t[w+' indexslag']+t[w+' systerslag']).max()),'reviews':len(r),'min_announcement_gap_trading_days':int(r.lag_trading_days.min()),'max_announcement_gap_trading_days':int(r.lag_trading_days.max()),'one_AD_and_ED_per_review':True},indent=2))
print('Aggregate twin leg identity and review-date uniqueness verified.')
