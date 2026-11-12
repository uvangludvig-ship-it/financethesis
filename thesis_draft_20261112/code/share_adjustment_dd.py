"""Reconstruct inherited share-denominator and adjustment-screen provenance.
No corporate-action truth is inferred from the adjustment proxy. Event-local
proxy changes are diagnostics only and never replace the primary filter.
"""
from pathlib import Path
import argparse,json,re
import numpy as np
import pandas as pd
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args();src=a.source;out=a.out;out.mkdir(exist_ok=True,parents=True)
e=pd.read_csv(src/'results/fund_demand/handelser_omraknade.csv',parse_dates=['AD','ED'])
idx=pd.read_csv(src/'data/prices/index_levels_daily_2004_2026.csv',parse_dates=['date']);cal=pd.DatetimeIndex(idx.loc[(idx.ric=='.OMXSBGI')&idx.close.notna(),'date'].sort_values().unique());pos=pd.Series(np.arange(len(cal)),index=cal)
def root(r):
 m=re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST',str(r));return m.group(1) if m else str(r)
roots={root(r) for r in e.RIC};parts=[]
for name in ['all_stocks_daily_2004_2012.csv.gz','all_stocks_daily_2013_2019.csv.gz','all_stocks_daily_2020_2026.csv.gz']:
 p=pd.read_csv(src/'data/prices'/name,usecols=['ric','date','close','shares','mcap'],parse_dates=['date']);key={r:root(r) for r in p.ric.unique()};parts.append(p[p.ric.map(key).isin(roots)&p.date.isin(cal)])
p=pd.concat(parts,ignore_index=True).drop_duplicates(['ric','date'],keep='last').sort_values(['ric','date'])
def piv(c):return p.pivot_table(index='date',columns='ric',values=c).reindex(cal)
close=piv('close');shares=piv('shares');mcap=piv('mcap').ffill(limit=10)
related={}
for c in close:related.setdefault(root(c),[]).append(c)
def available(c,i):return c in close and close[c].iloc[max(0,i-5):i+1].notna().any()
def sh_at(c,i,lb):
 if c not in shares:return np.nan,np.nan
 z=shares[c].iloc[max(0,i-lb):i+1].dropna()
 if z.empty or z.iloc[-1]<=0:return np.nan,np.nan
 return float(z.iloc[-1]),int(i-pos[z.index[-1]])
def factor(c,i):
 if not available(c,i) or c not in mcap:return np.nan
 b=mcap[c].iloc[max(0,i-10):i+1].dropna();cl=close[c].iloc[max(0,i-10):i+1].dropna()
 sibling=[r for r in related.get(root(c),[c]) if available(r,i)]
 sh=[sh_at(r,i,10)[0] for r in sibling]
 if b.empty or cl.empty or not all(v>0 for v in sh):return np.nan
 return float(b.iloc[-1]/sum(sh)/cl.iloc[-1])
last={c:int(pos[close[c].last_valid_index()]) for c in set(e.RIC) if c in close and close[c].last_valid_index() is not None}
rows=[]
for x in e.itertuples():
 i=int(pos[x.ED]);aidx=int(pos[x.AD]);sh,age=sh_at(x.RIC,i,250)
 f0=factor(x.RIC,i);f1=factor(x.RIC,last[x.RIC]) if x.RIC in last else np.nan
 ratio=f0/f1 if f1 and np.isfinite(f1) else np.nan
 # Broad bounding window for snapshots: calendar120 days before AD through45 after ED.
 lo=max(0,cal.searchsorted(x.AD-pd.Timedelta(days=120)))
 hi=min(len(cal)-1,cal.searchsorted(x.ED+pd.Timedelta(days=45),side='right')-1)
 fl,fh=factor(x.RIC,lo),factor(x.RIC,hi);local=fl/fh if fh and np.isfinite(fh) else np.nan
 rows.append(dict(event_id=x.event_id,type=x.type,period=x.per,split=bool(x.split),stored_kv=x.kv,reconstructed_kv=ratio,stored_sh=x.sh_ed,reconstructed_sh=sh,denominator_age_trading_days=age,local_proxy_ratio=local,fonddata=bool(x.fonddata),D_C=x.D_C,y_tot=x.y_tot))
z=pd.DataFrame(rows);checks=[]
for c,old in [('reconstructed_sh','stored_sh'),('reconstructed_kv','stored_kv')]:
 ok=np.isclose(z[c],z[old],atol=1e-6,rtol=1e-8,equal_nan=True);checks.append({'check':c,'passed':bool(ok.all()),'matching':int(ok.sum()),'total':len(z),'max_abs_difference':float(np.nanmax(abs(z[c]-z[old])))})
z['unknown_factor']=z.stored_kv.isna();z['outside_global_band']=z.stored_kv.notna()&~z.stored_kv.between(1/1.4,1.4);z['outside_local_band']=z.local_proxy_ratio.notna()&~z.local_proxy_ratio.between(1/1.4,1.4)
z['retained_primary']=(~z.split)&z.fonddata&z.D_C.notna()&z.y_tot.notna()
agg=[]
for (ty,per),g in z.groupby(['type','period']):
 q=g[g.retained_primary]
 agg.append(dict(type=ty,period=per,candidates=len(g),excluded_adjustment_screen=int(g.split.sum()),missing_factor=int(g.unknown_factor.sum()),outside_global_factor_band=int(g.outside_global_band.sum()),excluded_global_but_local_within_band=int((g.outside_global_band&g.local_proxy_ratio.between(1/1.4,1.4)).sum()),primary_retained=len(q),retained_median_denominator_age=q.denominator_age_trading_days.median(),retained_max_denominator_age=q.denominator_age_trading_days.max(),retained_denominators_older21=int((q.denominator_age_trading_days>21).sum()),retained_outside_local_band=int(q.outside_local_band.sum())))
pd.DataFrame(agg).to_csv(out/'share_adjustment_screen_summary.csv',index=False)
pd.DataFrame(checks).to_csv(out/'share_adjustment_validation.csv',index=False)
(out/'share_adjustment_definition.json').write_text(json.dumps({'source_original':'https://github.com/uvangludvig-ship-it/financethesis/blob/d2d41666ed213e4cc1f6cb382313f59c29e87ea0/code/claude_checks/runda11.py','screen':'Exclude if proxy factor(ED)/factor(last available price date) is missing or outside [1/1.4,1.4]. Proxy factor is company market capitalization divided by total shares of locally quoted classes divided by class adjusted close.','denominator':'Last available shares outstanding at or before ED, lookback250 trading days.','local_diagnostic':'Compare same proxy factor at AD minus120 calendar days and ED plus45 calendar days (nearest available trade boundaries); this is a wide snapshot-bound diagnostic, not exact fund-specific reporting dates. Never substitutes for corporate-action verification.','interpretation':'A future-adjustment exclusion can be motivated by adjusted holdings vs historical shares units; it nevertheless causes historical attrition. Proxy is not an independently authenticated split record.'},indent=2))
print(pd.DataFrame(checks).to_string(index=False));print(pd.DataFrame(agg).to_string(index=False))
