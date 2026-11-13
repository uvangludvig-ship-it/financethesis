# T8a (likviditet, tvillingar) och T10 (aktiva fonder), enligt runda2_deklaration.md (20:09)
from common import *
from scipy.stats import t as tdist
rng=np.random.default_rng(20261101)
out=[]
def ci(v,g=None):
    v=pd.Series(np.asarray(v,float),index=None if g is None else np.asarray(g)).dropna()
    if g is not None: v=v.groupby(level=0).mean()
    G=len(v); m=v.mean(); se=v.std(ddof=1)/np.sqrt(G); q=tdist.ppf(.975,G-1)
    s=(v.values*rng.choice([-1,1],(20000,G))).mean(1); p=(np.abs(s)>=abs(m)).mean()
    return m,m-q*se,m+q*se,p,G

# ---------- T8a
pv=lambda col: px.pivot_table(index='date',columns='ric',values=col).reindex(cal)
BID,ASK,VOL,SH=pv('bid'),pv('ask'),pv('volume'),pv('shares')
SPR=(ASK-BID)/((ASK+BID)/2)*100; SPR=SPR.where((SPR>0)&(SPR<50))
TURN=(VOL/SH*100).where(SH>0)
def med(M,r,a,b):
    if r not in M: return np.nan
    s=M[r].iloc[max(a,0):min(b,len(cal)-1)+1].dropna()
    return s.median() if len(s)>=20 else np.nan
tw=pd.read_csv('twin_results_events.csv',parse_dates=['AD','ED'])
rows=[]
for _,e in tw.iterrows():
    a,d=int(e.iAD),int(e.iED); r={}
    for lab,M in [('spread',SPR),('omsättning',TURN)]:
        for leg,ric in [('ix',e.event_key),('sis',e.sister_ric)]:
            pre=med(M,ric,a-120,a-21); post=med(M,ric,d+20,d+120)
            r[f'{lab}_{leg}']=np.log(post/pre) if pre and post and pre>0 and post>0 else np.nan
    rows.append(dict(event_id=e.event_id,firm=e.firm,type=e.type,sign=e.sign,**r))
L=pd.DataFrame(rows)
for lab in ['spread','omsättning']:
    L[f'{lab}_diff']=L.sign*(L[f'{lab}_ix']-L[f'{lab}_sis'])
    for v,txt in [(f'{lab}_diff','indexslag minus systerslag (signerad)'),(f'{lab}_ix','indexslaget, signerad'),(f'{lab}_sis','systerslaget, signerad')]:
        y=L[v] if v.endswith('diff') else L.sign*L[v]
        m,lo,hi,p,G=ci(y,L.firm)
        out.append(dict(test='T8a',mått=lab,variant=txt,N=int(y.notna().sum()),G=G,skattning=round(m,3),ci_lo=round(lo,3),ci_hi=round(hi,3),p=round(p,4)))
L.to_csv('runda2_T8a_events.csv',index=False)

# ---------- T10
ev['car']=[wsum(r,a-1,e+1) for r,a,e in zip(ev.RIC,ev.iAD,ev.iED)]
def ols_cl(X,y,g):
    ok=np.isfinite(y)&np.isfinite(X).all(1); X=X[ok];y=y[ok]; codes=pd.factorize(np.asarray(g)[ok])[0]; G=codes.max()+1; n,k=X.shape
    XtXi=np.linalg.inv(X.T@X); b=XtXi@X.T@y; e=y-X@b
    S=sum(np.outer(X[codes==c].T@e[codes==c],X[codes==c].T@e[codes==c]) for c in range(G))
    V=XtXi@S@XtXi*G/(G-1)*(n-1)/(n-k); se=np.sqrt(np.diag(V)); q=tdist.ppf(.975,G-1)
    return b,b-q*se,b+q*se,2*(1-tdist.cdf(np.abs(b/se),G-1)),n,G
for ty in ['addition','deletion']:
    s=ev[(ev.type==ty)&ev.activebuy.notna()&ev.nt.notna()&ev.car.notna()]
    X=np.column_stack([np.ones(len(s)),s.activebuy.values,s.nt.values])
    b,lo,hi,p,n,G=ols_cl(X,s.car.values,s.review_cycle.values)
    for j,nm in [(1,'activebuy'),(2,'nt (indexfonder)')]:
        out.append(dict(test='T10',mått=ty,variant=nm,N=n,G=G,skattning=round(b[j],3),ci_lo=round(lo[j],3),ci_hi=round(hi[j],3),p=round(p[j],4)))
    out.append(dict(test='T10',mått=ty,variant='beskrivande: medel activebuy / nt',N=n,G=G,skattning=round(s.activebuy.mean(),3),ci_lo=round(s.nt.mean(),3),ci_hi=None,p=None))
O=pd.DataFrame(out); O.to_csv('runda2_har_results.csv',index=False)
pd.set_option('display.width',220); print(O.to_string(index=False))
