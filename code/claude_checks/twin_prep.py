from twin_prices import *
t=pd.read_csv('twin_pairs.csv',parse_dates=['AD','ED'])
t['iAD']=t.AD.map(pos); t['iED']=t.ED.map(pos)
o30=pd.read_csv(f'{R}/data/input/omxsb/omxs30_changes_2005_2026.csv',parse_dates=['effective_date','announcement_date'])
def root(r):
    import re; m=re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST',str(r)); return m.group(1) if m else ''
o30['tick_root']=o30.ticker.astype(str).str.split().str[0].str.upper()
rows=[]
for _,e in t.iterrows():
    a,b=int(e.iAD)-60,int(e.iED)+20
    s=e.sister_ric
    if s in CLOSE:
        c=CLOSE[s].iloc[a:b+1]; v=VOL[s].iloc[a:b+1]
        share=((c.notna())&(v.fillna(0)>0)).mean()
    else: share=0.0
    rt=root(e.event_key)
    lo,hi=cal[max(a,0)],cal[min(b,len(cal)-1)]
    o=o30[(o30.tick_root==rt)&(((o30.effective_date>=lo)&(o30.effective_date<=hi))|((o30.announcement_date>=lo)&(o30.announcement_date<=hi)))]
    rows.append(dict(event_id=e.event_id,company=e.company,type=e.type,sister=s,sister_trade_share=round(share,3),
                     stora_enso=('Stora Enso' in e.company),omxs30_overlap=len(o)>0,omxs30_note='; '.join(o.company.astype(str)+' '+o.type.astype(str))))
d=pd.DataFrame(rows)
d['excl_mech']=d.stora_enso|(d.sister_trade_share<0.90)|d.omxs30_overlap
d.to_csv('twin_mech_screen.csv',index=False)
print(d.to_string(index=False))
print('\nkvar efter mekaniska uteslutningar:',(~d.excl_mech).sum(),'av',len(d),'| Stora Enso',d.stora_enso.sum(),'| likviditet<90%',((d.sister_trade_share<0.9)&~d.stora_enso).sum(),'| OMXS30',d.omxs30_overlap.sum())
