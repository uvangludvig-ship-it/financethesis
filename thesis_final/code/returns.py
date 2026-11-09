# Dagliga överavkastningar mot OMXSBGI och summering över fönster. Läses av 01_effect_table.py med exec (DATA definieras där).
import pandas as pd, numpy as np
ix=pd.read_csv(DATA/'prices'/'index_levels_daily_2004_2026.csv',parse_dates=['date'])
cal=pd.DatetimeIndex(ix.loc[(ix.ric=='.OMXSBGI')&ix.close.notna(),'date'].sort_values().unique())
pos=pd.Series(np.arange(len(cal)),index=cal)
rm=ix.pivot(index='date',columns='ric',values='close').reindex(cal).pct_change()*100
mkt=rm['.OMXSBGI']
px=pd.read_csv(DATA/'prices'/'stock_prices_daily_2004_2026.csv.gz',parse_dates=['date'])
px=px[px.date.isin(cal)].sort_values(['ric','date'])
def rser(g):
    g=g.set_index('date'); r=g.totret.fillna(g.close.pct_change()*100)
    return r.reindex(cal[(cal>=g.index.min())&(cal<=g.index.max())])
RET=pd.DataFrame({r:rser(g) for r,g in px.groupby('ric')}).reindex(cal)
AR=RET.sub(mkt,axis=0)
ev=pd.read_csv(DATA/'events'/'omxsb_changes_with_car_2007_2026.csv',parse_dates=['AD','ED'])
ev['iAD']=ev.AD.map(pos); ev['iED']=ev.ED.map(pos)
def wsum(ric,a,b,M=AR):
    if ric not in M or pd.isna(a) or pd.isna(b): return np.nan
    a=int(a); b=int(b)
    if a<0 or b>=len(M): return np.nan
    s=M[ric].iloc[a:b+1]
    return np.nan if s.isna().any() else s.sum()
