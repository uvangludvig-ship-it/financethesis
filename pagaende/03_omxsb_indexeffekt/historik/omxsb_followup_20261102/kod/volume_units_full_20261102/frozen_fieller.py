"""Byte-identical Fieller function from the frozen original comparison script."""
import numpy as np
from scipy.stats import t

def fieller(y,x,alpha=.05):
    a=np.asarray(x,float); b=np.asarray(y,float); n=len(a)
    vx,vy,cov=np.var(a,ddof=1)/n,np.var(b,ddof=1)/n,np.cov(a,b,ddof=1)[0,1]/n
    xm,ym=a.mean(),b.mean(); c=t.ppf(1-alpha/2,n-1)**2
    A=xm*xm-c*vx; B=-2*(xm*ym-c*cov); C=ym*ym-c*vy
    disc=B*B-4*A*C
    ans=dict(ratio=ym/xm if xm!=0 else None,den_mean=xm,num_mean=ym,G=n,fieller_type='',lo=None,hi=None)
    if disc<0: ans['fieller_type']='all_real' if A<0 else 'empty'
    elif abs(A)<1e-14: ans['fieller_type']='linear_halfline'
    else:
        roots=sorted([(-B-np.sqrt(disc))/(2*A),(-B+np.sqrt(disc))/(2*A)])
        ans.update(fieller_type='bounded' if A>0 else 'two_unbounded_rays',lo=roots[0],hi=roots[1])
    return ans
