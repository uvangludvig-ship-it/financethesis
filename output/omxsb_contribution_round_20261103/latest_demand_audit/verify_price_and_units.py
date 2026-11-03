"""Independent raw-panel verification of Runda11 prices and split screen.

No new price estimates or sample choices. Raw holdings stay in licensed input.
"""
from pathlib import Path
import re, json, hashlib, datetime
import pandas as pd
import numpy as np

O=Path(__file__).resolve().parent
R=Path('/Users/ludviguvang/dev/financethesis')
paths=[R/'runda2_indata/panel_full.csv.gz',R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',R/'code/claude_checks/data/lseg_saknade_aktier.csv',R/'code/claude_checks/runda11_resultat/handelser.csv']
(O/'RAW_PANEL_CHECK_LOCK.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Verify already-declared price and screen outputs; no new economic test','inputs':{str(p):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths}},indent=2))
E=pd.read_csv(paths[3])
ix=pd.read_csv(paths[1],parse_dates=['date'])
market=ix[ix.ric.eq('.OMXSBGI')&ix.close.notna()].sort_values('date').set_index('date').close
cal=pd.DatetimeIndex(market.index.unique());market=market.reindex(cal).pct_change()*100
def root(r):
    m=re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST',str(r));return m.group(1) if m else str(r)
roots={root(r) for r in E.RIC}
chunks=[]
for chunk in pd.read_csv(paths[0],usecols=['ric','date','close','totret','mcap','shares'],chunksize=100000):
    keep=chunk.ric.str.contains(r'\.ST')&chunk.ric.map(root).isin(roots)
    chunks.append(chunk[keep])
px=pd.concat(chunks,ignore_index=True);px.date=pd.to_datetime(px.date)
supp=pd.read_csv(paths[2]);add=[]
for r in ['NDASE.ST','TIETOS.ST']:
    d=supp[(supp.ric==r)&supp.Date.notna()].copy();d['date']=pd.to_datetime(d.Date)
    m=supp[(supp.ric==r)&(supp.typ=='marknadsvarde_manad')].reset_index(drop=True)
    m['date']=pd.date_range('2006-01-31',periods=len(m),freq='ME')
    d=d.merge(m[['date','Outstanding Shares']].rename(columns={'Outstanding Shares':'shares'}),on='date',how='outer').sort_values('date')
    d['shares']=d.shares.ffill();d=d[d.TRDPRC_1.notna()]
    add.append(pd.DataFrame(dict(ric=r,date=d.date,close=d.TRDPRC_1,totret=np.nan,mcap=d.TRDPRC_1*d.shares,shares=d.shares)))
px=pd.concat([px[~px.ric.isin(['NDASE.ST','TIETOS.ST'])]]+add,ignore_index=True)
px=px[px.date.isin(cal)].drop_duplicates(['ric','date'],keep='last').sort_values(['ric','date'])
data={};ar={};root_members={}
for r,g in px.groupby('ric'):
    z=g.set_index('date')
    # Older pandas pct_change used forward-fill when close was missing.
    ret=z.totret.fillna(z.close.ffill().pct_change()*100).reindex(cal)
    ret=ret.mask(ret>1000);ar[r]=ret-market
    z=z.reindex(cal);z['mcap']=z.mcap.ffill(limit=10);data[r]=z
    root_members.setdefault(root(r),[]).append(r)
def hasclose(r,i):return r in data and data[r].close.iloc[max(i-5,0):i+1].notna().any()
def shares(r,i,lb):
    if r not in data:return np.nan
    s=data[r].shares.iloc[max(i-lb,0):i+1].dropna()
    return float(s.iloc[-1]) if len(s) and s.iloc[-1]>0 else np.nan
def factor(r,i):
    if not hasclose(r,i):return np.nan
    z=data[r];mc=z.mcap.iloc[max(i-10,0):i+1].dropna();close=z.close.iloc[max(i-10,0):i+1].dropna()
    siblings=[o for o in root_members[root(r)] if hasclose(o,i)]
    sh=[shares(o,i,10) for o in siblings]
    return float(mc.iloc[-1]/sum(sh)/close.iloc[-1]) if len(mc) and len(close) and all(v>0 for v in sh) else np.nan
pos={d:i for i,d in enumerate(cal)}
out=[]
for e in E.itertuples():
    iA=int(e.iA);iE=int(e.iE);r=e.RIC
    last=data[r].close.last_valid_index() if r in data else None
    f=factor(r,iE)/factor(r,pos[last]) if last is not None else np.nan
    sh=shares(r,iE,250)
    def car(a,b):
        if a<0 or b>=len(cal) or r not in ar:return np.nan
        s=ar[r].iloc[a:b+1]
        return float(s.sum()) if s.notna().all() else np.nan
    y=car(iA-1,iE+1);yl=car(iA-20,iE+1)
    out.append(dict(event_id=e.event_id,raw_car_total=y,saved_car_total=e.car_tot,
        raw_car_long=yl,saved_car_long=e.car_lang,car_total_abs_error=abs(y-e.car_tot),car_long_abs_error=abs(yl-e.car_lang),
        raw_factor_ratio=f,saved_factor_ratio=e.kv,ratio_abs_error=abs(f-e.kv),raw_sh_ed=sh,saved_sh_ed=e.sh_ed,sh_abs_error=abs(sh-e.sh_ed),
        raw_split=not(1/1.4<=f<=1.4),saved_split=e.split))
Q=pd.DataFrame(out);Q.to_csv(O/'r11_raw_price_split_checks.csv',index=False)
errors={c:float(Q[c].max()) for c in ['car_total_abs_error','car_long_abs_error','ratio_abs_error','sh_abs_error']}
missing_match={f'car_{w}':bool(Q[f'raw_car_{w}'].isna().equals(Q[f'saved_car_{w}'].isna())) for w in ['total','long']}
split_match=bool(Q.raw_split.eq(Q.saved_split).all())
assert errors['car_total_abs_error']<1e-8 and errors['car_long_abs_error']<1e-8
assert errors['ratio_abs_error']<1e-8 and errors['sh_abs_error']<1e-3
assert all(missing_match.values()) and split_match
meta=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),event_count=len(Q),errors=errors,missing_patterns_match=missing_match,all_split_flags_match=split_match,price_benchmark='OMXSBGI')
(O/'RAW_PANEL_VERIFICATION.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
