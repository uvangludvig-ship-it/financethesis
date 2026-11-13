# Robusthetstest T1-T4 enligt robusthet_deklaration.md (2026-11-01 19:06 CET)
from common import *
import re
rng=np.random.default_rng(20261101)
D_=D
ixe=pd.read_csv(f'{D_}/indices_daily_extra.csv',parse_dates=['date']).pivot_table(index='date',columns='ric',values='close').reindex(cal)
AR_mid=RET.sub(ixe['.OMXSMCGI'].pct_change()*100,axis=0)

def root(r):
    m=re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST',str(r)); return m.group(1) if m else str(r)

def signflip(y,g,B=20000):
    m=pd.Series(np.asarray(y,float),index=np.asarray(g)).dropna()
    m=m.groupby(level=0).mean(); t=m.mean()
    s=np.array([(m.values*rng.choice([-1,1],len(m))).mean() for _ in range(B)])
    return t,(np.abs(s)>=abs(t)).mean(),len(m)

WEBB=np.array([-np.sqrt(1.5),-1,-np.sqrt(.5),np.sqrt(.5),1,np.sqrt(1.5)])
def wdraw(G): return rng.choice([-1,1],G) if G>=12 else rng.choice(WEBB,G)

def wcb_mean(y,g,B=9999):
    d=pd.DataFrame({'y':np.asarray(y,float),'g':np.asarray(g)}).dropna(); G=d.g.nunique()
    codes=pd.factorize(d.g)[0]
    def tstat(v):
        mu=v.mean(); e=v-mu; sg=np.bincount(codes,weights=e)
        return mu/(np.sqrt((sg**2).sum())/len(v)*np.sqrt(G/(G-1)))
    t=tstat(d.y.values); ts=np.array([tstat(d.y.values*wdraw(G)[codes]) for _ in range(B)])
    return (np.abs(ts)>=abs(t)).mean()

def ols_cl(X,y,codes):
    XtX=np.linalg.inv(X.T@X); b=XtX@X.T@y; e=y-X@b; G=codes.max()+1
    S=np.zeros((X.shape[1],X.shape[1]))
    for g in range(G):
        s=X[codes==g].T@e[codes==g]; S+=np.outer(s,s)
    n,k=X.shape; V=XtX@S@XtX*G/(G-1)*(n-1)/(n-k)
    return b,np.sqrt(np.diag(V))

def wcr(X,y,g,j,B=9999):
    """wild cluster bootstrap, restriktiv (H0: beta_j=0). Returnerar coef, se, p."""
    ok=np.isfinite(y)&np.isfinite(X).all(1); X=X[ok]; y=y[ok]; codes=pd.factorize(np.asarray(g)[ok])[0]; G=codes.max()+1
    b,se=ols_cl(X,y,codes); t=b[j]/se[j]
    Xr=np.delete(X,j,1); br=np.linalg.lstsq(Xr,y,rcond=None)[0]; fr=Xr@br; er=y-fr
    ts=[]
    for _ in range(B):
        ys=fr+er*wdraw(G)[codes]; bs,ses=ols_cl(X,ys,codes); ts.append(bs[j]/ses[j])
    return b[j],se[j],(np.abs(ts)>=abs(t)).mean(),len(y),G

ev['post']=(ev.AD.dt.year>=2017).astype(int)
ev['sign']=np.where(ev.type=='addition',1,-1)
ev['car']=[wsum(r,a-1,e+1) for r,a,e in zip(ev.RIC,ev.iAD,ev.iED)]
ev['car_mid']=[wsum(r,a-1,e+1,AR_mid) for r,a,e in zip(ev.RIC,ev.iAD,ev.iED)]
ev['car_e20']=[wsum(r,e,e+20) for r,e in zip(ev.RIC,ev.iED)]
rev=ev.groupby('review_cycle').agg(AD=('AD','first'),iAD=('iAD','first'),iED=('iED','first')).sort_values('AD').reset_index()
rev['k']=np.arange(len(rev)); kmap=dict(zip(rev.review_cycle,rev.k))
ev['k']=ev.review_cycle.map(kmap)
has_ev=set(zip(ev.RIC,ev.k))
PER={'före':0,'efter':1}
out=[]
def rec(test,typ,per,variant,N,G,mean,p_sf,p_wcb,extra=''):
    out.append(dict(test=test,typ=typ,period=per,variant=variant,N=N,G=G,medel=round(mean,3),p_teckenbyte=None if p_sf is None else round(p_sf,4),p_wcb=None if p_wcb is None else round(p_wcb,4),not_=extra))

# ---------- T1 pseudohändelser
rows=[]
for _,e in ev.iterrows():
    for dirn,dk in [('pseudo-före',-1),('pseudo-efter',1)]:
        kk=e.k+dk
        if kk<0 or kk>=len(rev) or (e.RIC,kk) in has_ev: continue
        r=rev.iloc[kk]; c=wsum(e.RIC,r.iAD-1,r.iED+1)
        rows.append(dict(event_id=e.event_id,RIC=e.RIC,type=e.type,post=e.post,dir=dirn,pseudo_review=r.review_cycle,real_review=e.review_cycle,car_pseudo=c,car_real=e.car))
P=pd.DataFrame(rows)
for ty in ['addition','deletion']:
    for pn,pv in PER.items():
        s=ev[(ev.type==ty)&(ev.post==pv)]
        m,p1,G=signflip(s.car,s.review_cycle); rec('T1',ty,pn,'verklig',int(s.car.notna().sum()),G,m,p1,wcb_mean(s.car,s.review_cycle))
        for dirn in ['pseudo-före','pseudo-efter']:
            q=P[(P.type==ty)&(P.post==pv)&(P.dir==dirn)]
            m,p1,G=signflip(q.car_pseudo,q.pseudo_review); rec('T1',ty,pn,dirn,int(q.car_pseudo.notna().sum()),G,m,p1,wcb_mean(q.car_pseudo,q.pseudo_review))
        q=P[(P.type==ty)&(P.post==pv)&(P.dir=='pseudo-före')].dropna(subset=['car_pseudo','car_real'])
        d=q.car_real-q.car_pseudo; m,p1,G=signflip(d,q.real_review)
        rec('T1',ty,pn,'verklig minus pseudo-före',len(q),G,m,p1,wcb_mean(d,q.real_review))
P.to_csv('robusthet_T1_events.csv',index=False)

# ---------- T2 matchad kontroll
mc=px.pivot_table(index='date',columns='ric',values='mcap').reindex(cal).ffill(limit=10)
rics=list(RET.columns)
def runup(r,i): return wsum(r,i-100,i-1)
rows=[]
for k,r in rev.iterrows():
    iA,iE=int(r.iAD),int(r.iED)
    if iA-100<0 or iE+1>=len(cal): continue
    evs=ev[ev.k==k]
    ev_roots=set(root(x) for x in evs.RIC)
    cand=[]
    for c in rics:
        if any((c,kk) in has_ev for kk in (k-1,k,k+1)): continue
        ru=runup(c,iA); cr=wsum(c,iA-1,iE+1); m=mc[c].iloc[iA-1] if c in mc else np.nan
        if np.isnan(ru) or np.isnan(cr) or not (m>0): continue
        cand.append((c,root(c),ru,np.log(m),cr))
    if len(cand)<3: continue
    C=pd.DataFrame(cand,columns=['ric','root','ru','lm','car'])
    E=evs.assign(ru=[runup(x,iA) for x in evs.RIC],lm=[np.log(mc[x].iloc[iA-1]) if x in mc and mc[x].iloc[iA-1]>0 else np.nan for x in evs.RIC]).dropna(subset=['ru','lm','car'])
    allv=pd.concat([C[['ru','lm']],E[['ru','lm']]]); mu=allv.mean(); sd=allv.std()
    Cz=((C[['ru','lm']]-mu)/sd).values
    for _,e in E.iterrows():
        ez=((e[['ru','lm']].astype(float)-mu)/sd).values.astype(float)
        mask=(C.root!=root(e.RIC)).values
        dist=np.sqrt(((Cz-ez)**2).sum(1)); dist[~mask]=np.inf
        o=np.argsort(dist)[:3]
        rows.append(dict(event_id=e.event_id,RIC=e.RIC,type=e.type,post=e.post,review=e.review_cycle,car=e.car,ru=e.ru,lm=e.lm,
            c1=C.ric.iloc[o[0]],c1_car=C.car.iloc[o[0]],c1_ru=C.ru.iloc[o[0]],c1_lm=C.lm.iloc[o[0]],c3_car=C.car.iloc[o].mean(),n_cand=int(mask.sum()),d1=dist[o[0]]))
M=pd.DataFrame(rows); M['diff1']=M.car-M.c1_car; M['diff3']=M.car-M.c3_car
for ty in ['addition','deletion']:
    for pn,pv in PER.items():
        q=M[(M.type==ty)&(M.post==pv)]
        for v,lab in [('diff1','händelse minus 1 kontroll'),('diff3','händelse minus 3 kontroller'),('c1_car','kontrollens CAR')]:
            m,p1,G=signflip(q[v],q.review); rec('T2',ty,pn,lab,int(q[v].notna().sum()),G,m,p1,wcb_mean(q[v],q.review),
               extra=f'balans: uppgång {q.ru.mean():.2f} mot {q.c1_ru.mean():.2f}; log mcap {q.lm.mean():.2f} mot {q.c1_lm.mean():.2f}; kandidater median {q.n_cand.median():.0f}' if v=='diff1' else '')
M.to_csv('robusthet_T2_events.csv',index=False)

# ---------- T3 asymmetri
for col,lab in [('car','[AD-1,ED+1]'),('car_e20','[ED,ED+20]'),('car_mid','[AD-1,ED+1] Mid Cap')]:
    s=ev[['review_cycle','type','post','sign',col]].dropna()
    y=(s.sign*s[col]).values; add=(s.type=='addition').astype(float).values; post=s.post.astype(float).values
    for pn,pv in PER.items():
        w=post==pv; X=np.column_stack([np.ones(w.sum()),add[w]])
        b,se,p,N,G=wcr(X,y[w],s.review_cycle.values[w],1)
        a_=y[w][add[w]==0].mean(); rec('T3','b: tillägg minus borttag (signerad)',pn,lab,N,G,b,None,p,extra=f'signerad borttag {a_:.2f}, signerad tillägg {a_+b:.2f}, se {se:.2f}')
    X=np.column_stack([np.ones(len(y)),add,post,add*post])
    b,se,p,N,G=wcr(X,y,s.review_cycle.values,3)
    rec('T3','d: ändring i asymmetri (tillägg×efter)','hela',lab,N,G,b,None,p,extra=f'se {se:.2f}')

# ---------- T4 multiplikator
fs=pd.read_csv('twin_first_stage_output.csv'); te=pd.read_csv('twin_results_events.csv')
T=fs.merge(te,left_on=['review','company','type'],right_on=['review_cycle','company','type'])
T['d']=T.sign*T.event_class_chg_pct; T['y']=T['primär [AD-1,ED+1]']; T['leg']=T['primär [AD-1,ED+1] indexslag']
T=T.dropna(subset=['d','y'])
firms=T.firm.unique(); Mhat=T.y.mean()/T.d.mean()
bs=[]
for _ in range(10000):
    f=rng.choice(firms,len(firms)); S=pd.concat([T[T.firm==x] for x in f])
    if S.d.mean()!=0: bs.append(S.y.mean()/S.d.mean())
lo,hi=np.percentile(bs,[2.5,97.5])
rec('T4','M = medel(y)/medel(d)','2019-26','primärt',len(T),len(firms),Mhat,None,None,extra=f'95% [{lo:.2f}, {hi:.2f}]; medel y {T.y.mean():.2f}, medel d {T.d.mean():.2f}')
X=np.column_stack([np.ones(len(T)),T.d.values])
b,se,p,N,G=wcr(X,T.y.values,T.firm.values,1)
rec('T4','beta: y på d','2019-26','sekundärt',N,G,b,None,p,extra=f'se {se:.2f}')
rec('T4','indexslagets CAR / d','2019-26','beskrivande',len(T),len(firms),T.leg.mean()/T.d.mean(),None,None,extra=f'medel CAR indexslag {T.leg.mean():.2f}')
T[['event_id','review','company','type','firm','d','y','leg']].to_csv('robusthet_T4_events.csv',index=False)

O=pd.DataFrame(out); O.to_csv('robusthet_results.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',120)
print(O.to_string(index=False))
