from common import *
rng=np.random.default_rng(3)
ixe=pd.read_csv(f'{D}/indices_daily_extra.csv',parse_dates=['date']).pivot_table(index='date',columns='ric',values='close').reindex(cal)
mid=ixe['.OMXSMCGI'].pct_change()*100
AR_mid=RET.sub(mid,axis=0)
def beta_ar(ric,iAD):
    a,b=iAD-250,iAD-101
    if a<0 or ric not in RET: return None
    y=RET[ric].iloc[a:b+1]; x=mkt.iloc[a:b+1]; ok=y.notna()&x.notna()
    if ok.sum()<150: return None
    bt=np.cov(y[ok],x[ok])[0,1]/np.var(x[ok],ddof=1); al=y[ok].mean()-bt*x[ok].mean()
    return RET[ric]-bt*mkt  # alpha excluded (common choice for event windows)
def csum(series,a,b):
    if series is None or b>=len(cal): return np.nan
    s=series.iloc[a:b+1]; return np.nan if s.isna().any() else s.sum()
def sf(y,g,B=20000):
    m=y.groupby(g).mean().dropna(); t=m.mean()
    s=np.array([(m.values*rng.choice([-1,1],len(m))).mean() for _ in range(B)])
    return t,(np.abs(s)>=abs(t)).mean(),len(m)
rows=[]
for _,e in ev.iterrows():
    if pd.isna(e.iED): continue
    iA,iE=int(e.iAD),int(e.iED); bser=beta_ar(e.RIC,iA)
    r=dict(event_id=e.event_id,type=e.type,AD=e.AD,period=e.period)
    for h in [20,60,100]:
        r[f'mkt_{h}']=csum(AR[e.RIC] if e.RIC in AR else None,iE,iE+h)
        r[f'mid_{h}']=csum(AR_mid[e.RIC] if e.RIC in AR_mid else None,iE,iE+h)
        r[f'beta_{h}']=csum(bser,iE,iE+h)
    rows.append(r)
X=pd.DataFrame(rows); X.to_csv('tillagg_A_events.csv',index=False)
out=[]
for ty in ['addition','deletion']:
    for per,c in [('2007-2026',X.AD>='2007-01-01'),('2017-2026',X.AD>='2017-01-01')]:
        s=X[(X.type==ty)&c]
        for bm in ['mkt','mid','beta']:
            for h in [20,60,100]:
                y=s[f'{bm}_{h}']; m,p,G=sf(y,s.AD)
                out.append(dict(typ=ty,period=per,benchmark=bm,fönster=f'[ED,ED+{h}]',N=int(y.notna().sum()),G=G,medel_översyn=round(m,2),p=round(p,4)))
O=pd.DataFrame(out); O.to_csv('tillagg_A_results.csv',index=False)
pd.set_option('display.width',200); print(O.to_string(index=False))
