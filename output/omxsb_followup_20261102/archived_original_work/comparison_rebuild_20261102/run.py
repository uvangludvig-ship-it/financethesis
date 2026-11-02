from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
from scipy.stats import t

ROOT=Path('/Users/ludviguvang/dev/financethesis')
OUT=Path(__file__).parent

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

def main():
    dp=ROOT/'output/omxsb_mechanism_frontier_20261102/demand/event_demand_by_definition.csv'
    pp=ROOT/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv'
    d=pd.read_csv(dp); p=pd.read_csv(pp)
    defs=['documented_stable_family_subset','all_stable_family_candidates_sensitivity']
    d=d[d.definition.isin(defs)].merge(p[['event_id','event_1','diff3_1','issuer']],on='event_id',validate='m:1')
    d=d.dropna(subset=['net_company_pp','event_1','diff3_1'])
    d.to_csv(OUT/'same_sample_events.csv',index=False)
    rows=[]
    for (definition,typ),g in d.groupby(['definition','type']):
        rv=g.groupby('review_cycle')[['net_company_pp','event_1','diff3_1']].mean()
        for outcome in ['event_1','diff3_1']:
            a=fieller(rv[outcome],rv.net_company_pp)
            a.update(definition=definition,type=typ,outcome=outcome,N=len(g),issuer_N=g.issuer.nunique(),weighting='equal_review',excluded_or_unavailable_fund_event_pairs=int(g.n_excluded_or_unavailable_pairs.sum()))
            rows.append(a)
            ev=dict(definition=definition,type=typ,outcome=outcome,N=len(g),G=g.review_cycle.nunique(),weighting='equal_event_descriptive',num_mean=g[outcome].mean(),den_mean=g.net_company_pp.mean(),ratio=g[outcome].mean()/g.net_company_pp.mean())
            rows.append(ev)
    pd.DataFrame(rows).to_csv(OUT/'ratios.csv',index=False)
    # Transcribed published rounded values, not estimated anew from US microdata.
    us=pd.DataFrame([
        dict(type='addition',event_type='direct',return_pp=5.40,demand_pp=5.61),
        dict(type='addition',event_type='migration',return_pp=-1.82,demand_pp=.31),
        dict(type='addition',event_type='all',return_pp=.83,demand_pp=2.25),
        dict(type='deletion',event_type='direct',return_pp=-6.86,demand_pp=-5.53),
        dict(type='deletion',event_type='migration',return_pp=.06,demand_pp=-.22),
        dict(type='deletion',event_type='all',return_pp=-.62,demand_pp=-.89)])
    us['rounded_ratio']=us.return_pp/us.demand_pp
    us.to_csv(OUT/'US_reference.csv',index=False)
    (OUT/'hashes.json').write_text(json.dumps({str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [dp,pp,OUT/'DECISIONS.txt',Path(__file__)]},indent=2))
    print(pd.DataFrame(rows).to_string(index=False)); print(us.to_string(index=False))
if __name__=='__main__':main()
