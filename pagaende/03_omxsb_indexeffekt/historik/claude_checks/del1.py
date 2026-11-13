from common import *
rng=np.random.default_rng(20261101)
ev['car_e10']=[wsum(r,e,e+10) for r,e in zip(ev.RIC,ev.iED)]
ev['car_e20']=[wsum(r,e,e+20) for r,e in zip(ev.RIC,ev.iED)]
ev['runup']=[wsum(r,a,e-1) for r,a,e in zip(ev.RIC,ev.iAD,ev.iED)]
def signflip(y,g,B=20000):
    m=y.groupby(g).mean().dropna(); t=m.mean()
    s=np.array([(m.values*rng.choice([-1,1],len(m))).mean() for _ in range(B)])
    return t,(np.abs(s)>=abs(t)).mean(),len(m)
def wcb(y,g,B=9999):
    d=pd.DataFrame({'y':y,'g':g}).dropna(); G=d.g.nunique()
    def tstat(v):
        mu=v.mean(); e=v-mu; sg=e.groupby(d.g.values).sum()
        n=len(v); se=np.sqrt((sg**2).sum())/n*np.sqrt(G/(G-1))
        return mu/se
    t=tstat(d.y)
    codes=pd.factorize(d.g)[0]
    ts=[]
    for _ in range(B):
        if G>=12: w=rng.choice([-1,1],G)
        else: w=rng.choice([-np.sqrt(1.5),-1,-np.sqrt(.5),np.sqrt(.5),1,np.sqrt(1.5)],G)
        ts.append(tstat(pd.Series(d.y.values*w[codes])))
    return (np.abs(ts)>=abs(t)).mean()
rows=[]
PER=['all']+sorted(ev.period.dropna().unique())
for ty in ['addition','deletion']:
    for p in PER:
        s=ev[(ev.type==ty)&((ev.period==p) if p!='all' else True)]
        for v in ['car_e10','car_e20','runup']:
            y=s[v]; m,p_sf,G=signflip(y,s.AD)
            rows.append(dict(type=ty,period=p,measure=v,N=int(y.notna().sum()),G=G,event_mean=round(y.mean(),3),review_mean=round(m,3),p_signflip=round(p_sf,4),p_wcb=round(wcb(y,s.AD),4)))
out=pd.DataFrame(rows); out.to_csv('del1_results.csv',index=False)
pd.set_option('display.width',200)
print(out[out.period=='all'].to_string(index=False))
print(out[out.period!='all'].to_string(index=False))
for ty in ['addition','deletion']:
    s=ev[ev.type==ty]; ok=s.car_e20.notna()&s.runup.notna()
    print(ty,'återgångsandel [ED,ED+20] av [AD,ED-1]: ', round(-s[ok].car_e20.mean()/s[ok].runup.mean(),3), '(medel runup',round(s[ok].runup.mean(),3),', medel e20',round(s[ok].car_e20.mean(),3),', N',ok.sum(),')')
ev.to_csv('del1_events.csv',index=False)
