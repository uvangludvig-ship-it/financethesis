from pathlib import Path
import pandas as pd, numpy as np, json, hashlib
from scipy.stats import t
O=Path(__file__).resolve().parent
R=Path('/Users/ludviguvang/dev/financethesis')
DEFS=['documented_stable_family_subset','all_stable_family_candidates_sensitivity']

def independent_ratio(y,x):
    xy=np.column_stack([np.asarray(x,float),np.asarray(y,float)])
    assert np.isfinite(xy).all()
    n=len(xy);mu=xy.mean(axis=0);V=np.cov(xy,rowvar=False,ddof=1)/n
    critical=t.ppf(.975,n-1)**2
    co=[mu[0]**2-critical*V[0,0],-2*mu[0]*mu[1]+2*critical*V[0,1],mu[1]**2-critical*V[1,1]]
    roots=np.roots(co)
    if np.iscomplex(roots).any():
        kind='all_real' if co[0]<0 else 'empty'; bounds=[np.nan,np.nan]
    else:
        bounds=sorted(roots.real.tolist());kind='bounded' if co[0]>0 else 'two_unbounded_rays'
    return dict(ratio=mu[1]/mu[0],den_mean=mu[0],num_mean=mu[1],G=n,lo=bounds[0],hi=bounds[1],fieller_type=kind),V.tolist()

def main():
    dp=R/'output/omxsb_mechanism_frontier_20261102/demand/event_demand_by_definition.csv'
    pp=R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv'
    D=pd.read_csv(dp);D=D[D.definition.isin(DEFS)]
    P=pd.read_csv(pp);assert not P.event_id.duplicated().any()
    Z=D.merge(P[['event_id','event_1','diff3_1','issuer']],on='event_id',validate='many_to_one')
    Z=Z.dropna(subset=['net_company_pp','event_1','diff3_1'])
    saved=pd.read_csv(O/'same_sample_events.csv');assert set(zip(Z.definition,Z.event_id))==set(zip(saved.definition,saved.event_id));assert len(Z)==len(saved)==410
    assert Z.groupby('definition').event_id.nunique().eq(205).all()
    c=[]
    for x in pd.read_csv(O/'ratios.csv').itertuples():
        d=Z[(Z.definition==x.definition)&(Z.type==x.type)]
        assert d[x.outcome].notna().all() and d.net_company_pp.notna().all()
        if x.weighting=='equal_review':
            r=d.groupby('review_cycle')[[x.outcome,'net_company_pp']].mean()
            a,v=independent_ratio(r[x.outcome],r.net_company_pp)
            keys=['ratio','den_mean','num_mean','G','lo','hi']; assert a['fieller_type']==x.fieller_type
        else:
            a=dict(ratio=d[x.outcome].mean()/d.net_company_pp.mean(),den_mean=d.net_company_pp.mean(),num_mean=d[x.outcome].mean(),G=d.review_cycle.nunique());keys=['ratio','den_mean','num_mean','G'];v=None
        a['N']=len(d);keys+=['N'];diff={k:float(a[k]-getattr(x,k)) for k in keys};assert max(abs(z) for z in diff.values())<1e-10
        c.append(dict(definition=x.definition,type=x.type,outcome=x.outcome,weighting=x.weighting,independent=a,covariance_of_review_means=v,differences=diff))
    U=pd.read_csv(O/'US_reference.csv');assert np.allclose(U.rounded_ratio,U.return_pp/U.demand_pp)
    missing=[]
    for definition,g in D.groupby('definition'):
        matched=Z[Z.definition==definition]
        missing.append(dict(definition=definition,quantity_events=len(g),price_available_events=len(matched),excluded_event_ids=sorted(set(g.event_id)-set(matched.event_id))))
    out=dict(all_16_cells_pass=True,same_sample_rows=len(Z),unique_events=Z.event_id.nunique(),groups=Z.groupby(['definition','type']).size().to_dict(),coverage=missing,cells=c,US_ratio_arithmetic=True,input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [dp,pp,O/'same_sample_events.csv',O/'ratios.csv',O/'US_reference.csv']})
    out['groups']={str(k):v for k,v in out['groups'].items()}
    (O/'independent_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['cells','input_hashes']},indent=2))
if __name__=='__main__':main()
