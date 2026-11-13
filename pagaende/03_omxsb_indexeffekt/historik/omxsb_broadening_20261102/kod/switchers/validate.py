"""Separate FWL and cluster-score numerical check of the frozen two models."""
from pathlib import Path
import numpy as np, pandas as pd, json, argparse
pa=argparse.ArgumentParser();pa.add_argument('--out',default=str(Path(__file__).resolve().parent))
O=Path(pa.parse_args().out)
d=pd.read_csv(O/'analysis_events.csv'); saved=pd.read_csv(O/'results.csv')
fe=pd.get_dummies(d[['ric','review']],drop_first=True,dtype=float).to_numpy()
sw=np.sqrt(d.w.to_numpy()); Y=d.y_pp.to_numpy()*sw; t=d['add'].to_numpy()*sw
out=[]
for name,controls in [('same_security_review',[]),('primary_pre_balance',['pre_balance_pp','size_balance'])]:
    Z=np.column_stack([np.ones(len(d)),fe,d[controls].to_numpy()])*sw[:,None]
    tr=t-Z@np.linalg.lstsq(Z,t,rcond=None)[0]
    yr=Y-Z@np.linalg.lstsq(Z,Y,rcond=None)[0]
    beta=(tr@yr)/(tr@tr)
    e=yr-beta*tr; a=tr/(tr@tr); k=Z.shape[1]+1; n=len(d)
    covs={}
    for key,g in [('review',d.review),('issuer',d.issuer_cluster),('pair',d.review.astype(str)+'/'+d.issuer_cluster)]:
        score=pd.Series(a*e).groupby(g).sum(); G=len(score)
        covs[key]=G/(G-1)*(n-1)/(n-k)*(score@score)
    covs['two_way']=covs['review']+covs['issuer']-covs['pair']
    s=saved.set_index('model').loc[name]
    errors={'beta':abs(beta-s.estimate_pp)}
    for key in ['review','issuer','two_way']:errors[key]=abs(covs[key]-s[f'{key}_variance'])
    assert max(errors.values())<1e-9,errors
    out.append(dict(model=name,beta_fwl=beta,errors=errors))
assert d.groupby('ric').type.nunique().eq(2).all()
assert d.groupby('review').w.sum().sub(1).abs().max()<1e-12
assert len(d)==244 and d.ric.nunique()==75 and d.issuer_cluster.nunique()==74
report={'passed':True,'models':out,'no_new_selection_or_outcomes':True}
(O/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
