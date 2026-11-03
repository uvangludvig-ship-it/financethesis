"""Verify already-reported post-primary counts; no new tests or group choices."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
O=Path(__file__).resolve().parent;A=O.parent.parent/'ownership_capital'
d=pd.read_csv(A/'normalized_fund_role_contributions.csv.gz')
d['entry_count']=(d.component=='new').astype(int)
d['exit_count']=-(d.component=='exiting').astype(int)
d['count']=d.entry_count+d.exit_count
pieces=[d,d.assign(group='ALL'),d[d.group.str.startswith('OMXSB_')].assign(group='OMXSB_family')]
g=pd.concat(pieces).groupby(['event_id','review','type','group','role'])[['count','entry_count','exit_count','pp']].sum()
parts=[]
for metric in ['count','entry_count','exit_count','pp']:
    q=g[metric].unstack('role');q[metric]=q.event-(q.c1+q.c2+q.c3)/3
    parts.append(q[metric])
e=pd.concat(parts,axis=1).reset_index()
v=e.groupby(['type','group','review'])[['count','entry_count','exit_count','pp']].mean()
z=v.groupby(['type','group']).mean().reset_index()
s=pd.read_csv(A/'same_support_counts_capital.csv')
j=z.merge(s,on=['type','group'],suffixes=('_audit','_saved'),validate='1:1')
err=max(float((j[c+'_audit']-j[c+'_saved']).abs().max()) for c in ['count','entry_count','exit_count','pp'])
assert err<1e-12
z.to_csv(O/'independent_same_support_counts_capital.csv',index=False)
(O/'DESCRIPTIVE_COUNTS_CHECK.json').write_text(json.dumps({'all14_group_type_rows_match':True,'max_error':err,'no_new_hypothesis_test':True,'labels_are_name_and_benchmark_proxies_not_certified_passive_status':True},indent=2))
print(z[z.type.eq('addition')].to_string(index=False))
