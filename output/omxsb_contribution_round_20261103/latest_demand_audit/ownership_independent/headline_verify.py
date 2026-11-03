"""Direct independent primary and covariance calculation from final fund-role ledger."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from scipy.stats import t
O=Path(__file__).resolve().parent;A=O.parent.parent/'ownership_capital'
L=pd.read_csv(A/'normalized_fund_role_contributions.csv.gz',dtype={'fund_id':str})
assert not L.duplicated(['event_id','role','fund_id']).any()
g=L.groupby(['event_id','review','type','role','component']).pp.sum().unstack('role',fill_value=0)
g['difference']=g.event-(g.c1+g.c2+g.c3)/3
e=g.difference.unstack('component',fill_value=0).reset_index()
e['total']=e[['new','continuing','exiting','neither']].sum(axis=1)
e['contrast']=e.new-e.continuing-e.exiting
v=e.groupby(['type','review'])[['new','continuing','exiting','total','contrast']].mean()
rows=[]
for typ,d in v.groupby('type'):
    z=d[['new','continuing','exiting']].to_numpy();G=len(z);centered=z-z.mean(axis=0);cov=centered.T@centered/(G*(G-1))
    w=np.array([1.,-1.,-1.]);se_cov=float(np.sqrt(w@cov@w))
    for metric in ['new','continuing','exiting','total','contrast']:
        mu=float(d[metric].mean());se=float(d[metric].std(ddof=1)/np.sqrt(G));half=t.ppf(.975,G-1)*se
        if metric=='contrast':assert abs(se-se_cov)<1e-12
        rows.append(dict(type=typ,metric=metric,N=int((e.type==typ).sum()),G=G,mean=mu,se=se,lo=mu-half,hi=mu+half))
T=pd.DataFrame(rows);T.to_csv(O/'HEADLINE_FROM_FINAL_LEDGER.csv',index=False)
target=pd.read_csv(A/'primary_contrast.csv').iloc[0];p=T[(T.type=='addition')&(T.metric=='contrast')].iloc[0]
errors=[abs(target.mean_pp-p['mean']),abs(target.se_pp-p.se),abs(target.ci95_low-p.lo),abs(target.ci95_high-p.hi)]
assert max(errors)<1e-12
(O/'HEADLINE_CHECK.json').write_text(json.dumps({'primary_reproduced':True,'max_error':max(errors),'N_additions':int(p.N),'reviews':int(p.G),'component_covariance_retained':True,'primary':p.to_dict()},indent=2))
print(T.to_string(index=False))
