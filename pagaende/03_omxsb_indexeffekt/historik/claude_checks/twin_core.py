from twin_prices import *
import re
l1=pd.read_csv('../../data/raw/lseg/twins/tvilling_priser_lseg.csv',parse_dates=['Date'])
TR={}
# total-return indices where available
pr=px.pivot_table(index='date',columns='ric',values='totret',aggfunc='last').reindex(cal)
for c in pr.columns: TR[c]=(1+pr[c].fillna(0)/100).cumprod().where(CLOSE[c].ffill().notna() if c in CLOSE else True)
for r in ['NCCa.ST','SWECa.ST']:
    g=l1[(l1.ric==r)].sort_values(['Date','Volume']).drop_duplicates('Date').set_index('Date')['Daily Total Return'].reindex(cal)
    TR[r]=(1+g.fillna(0)/100).cumprod().where(CLOSE[r].ffill().notna())
PRICE=CLOSE.ffill()
def root(r):
    m=re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST',str(r)); return m.group(1) if m else str(r)
def legs(ix,sis):
    if ix in TR and sis in TR: return TR[ix],TR[sis],'tr'
    return PRICE[ix],PRICE[sis],'price'
def spread(ix,sis,a,b):
    A,B,_=legs(ix,sis)
    if a-1<0 or b>=len(cal): return np.nan
    x=np.log(A.iloc[b]/A.iloc[a-1])-np.log(B.iloc[b]/B.iloc[a-1])
    return 100*x if np.isfinite(x) else np.nan
def leg_ret(ric_series,a,b):
    return 100*np.log(ric_series.iloc[b]/ric_series.iloc[a-1])
t=pd.read_csv('twin_pairs.csv',parse_dates=['AD','ED'])
t['iAD']=t.AD.map(pos).astype(int); t['iED']=t.ED.map(pos).astype(int)
t['firm']=t.event_key.map(root); t['sign']=np.where(t.type=='addition',1,-1)
scr=pd.read_csv('twin_mech_screen.csv'); t=t.merge(scr[['event_id','excl_mech']],on='event_id')
