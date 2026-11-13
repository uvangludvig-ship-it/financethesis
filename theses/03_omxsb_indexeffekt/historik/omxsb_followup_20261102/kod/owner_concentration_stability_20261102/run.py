from pathlib import Path
import re, json, hashlib
import pandas as pd
import numpy as np
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'additions_20261102'))
from portable_paths import analysis_paths, first_output, comparison_function, repository_source, verify_original_lock
R,O=analysis_paths('owner_concentration_stability_20261102')
D=R/'output/omxsb_mechanism_frontier_20261102/ownership'
f=pd.read_csv(D/'decomp_fund_roles.csv.gz',dtype={'fund_id':str})
m=pd.read_csv(D/'decomp_fund_groups.csv',dtype={'fund_id':str})
m['manager']=m.company.map(lambda v:re.sub(r'\s+',' ',str(v).strip().lower()))
f=f.merge(m[['review','fund_id','manager']],on=['review','fund_id'],validate='m:1')
assert len(f)==446048 and f.event_id.nunique()==219
f['net']=f.own_after-f.own_before
f['family_net']=f.net*f.group.str.startswith('OMXSB')
f['role_weight']=np.where(f.role.eq('event'),1.,-1/3)
f['total_contribution']=f.net*f.role_weight
f['family_contribution']=f.family_net*f.role_weight
ev=f[['event_id','review','type']].drop_duplicates()
ev['event_weight']=1/ev.groupby(['review','type']).event_id.transform('count')
a=f.groupby(['event_id','manager'])[['total_contribution','family_contribution']].sum().reset_index().merge(ev,on='event_id',validate='m:1')
for col in ['total_contribution','family_contribution']:
    a[col]*=a.event_weight
rev=a.groupby(['review','type'])[['total_contribution','family_contribution']].sum().reset_index()
rvcheck=pd.read_csv(D/'decomp_event_groups.csv')
assert np.allclose(rev.set_index(['review','type']).total_contribution.sort_index(),rvcheck[rvcheck.group.eq('ALL')].groupby(['review','type']).matched_change.mean().sort_index())
rows=[]; mgr=[]
for typ,r in rev.groupby('type'):
    G=len(r);full=r[['total_contribution','family_contribution']].mean()
    rows.append(dict(type=typ,omission_kind='none',omitted='none',G=G,total=full.total_contribution,family=full.family_contribution,ratio=full.family_contribution/full.total_contribution))
    contributions=a[a.type.eq(typ)].groupby('manager')[['total_contribution','family_contribution']].sum()/G
    for manager,c in contributions.iterrows():
        left=full-c
        rows.append(dict(type=typ,omission_kind='company',omitted=manager,G=G,total=left.total_contribution,family=left.family_contribution,ratio=left.family_contribution/left.total_contribution if left.total_contribution!=0 else np.nan))
        mgr.append(dict(type=typ,manager=manager,total=c.total_contribution,family=c.family_contribution))
    for review in r.review:
        left=r[r.review.ne(review)][['total_contribution','family_contribution']].mean()
        rows.append(dict(type=typ,omission_kind='review',omitted=review,G=G-1,total=left.total_contribution,family=left.family_contribution,ratio=left.family_contribution/left.total_contribution if left.total_contribution!=0 else np.nan))
out=pd.DataFrame(rows)
out.to_csv(O/'all_omissions.csv',index=False)
pd.DataFrame(mgr).to_csv(O/'company_additive_contributions.csv',index=False)
rev.to_csv(O/'review_contributions.csv',index=False)
a.to_csv(O/'event_company_contributions.csv',index=False)
summary=out.groupby(['type','omission_kind'])[['total','family','ratio']].agg(['min','max'])
summary.to_csv(O/'descriptive_ranges.csv')
files=[D/'decomp_fund_roles.csv.gz',D/'decomp_fund_groups.csv',O/'DECISIONS.txt',Path(__file__)]
(O/'hashes.json').write_text(json.dumps({str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in files},indent=2))
print(summary.to_string())
print(out[out.omitted.str.contains('nordea')].to_string(index=False))
