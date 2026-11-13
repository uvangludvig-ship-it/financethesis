"""Regression checks for the confirmed date, reporting and estimand defects."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from omxsb_audit_helpers import matched_fund_totals, yearly_median_inference

root=Path(__file__).resolve().parents[2]
nb=json.loads((root/'code/notebooks/replication_omxsb_2007.ipynb').read_text())
source='\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code')
assert 'MonthBegin(1)' not in source
dates=pd.Series(pd.to_datetime(['2020-05-01','2020-05-14','2020-01-02']))
assert (dates.dt.to_period('M')-1).astype(str).tolist()==['2020-04','2020-04','2019-12']
# A departing reporter and entering reporter must not be called a sale/purchase.
e=pd.DataFrame([dict(event_id='e',qb=1,qa=2,f=2)])
b={'e':pd.Series({10:5.,20:100.})};a={'e':pd.Series({10:12.,30:300.})}
r=matched_fund_totals(e,b,a,{1:{10,20},2:{10,30}},{10,20}).iloc[0]
assert r.all_a-r.all_b==2 and r.idx_a-r.idx_b==2
assert r.all_a-r.all_b == (r.idx_a-r.idx_b)+(r.act_a-r.act_b)
assert r.entry_holdings_a==300 and r.exit_holdings_b==200
# Median of pooled observations and EW annual medians are different estimands.
s=pd.DataFrame({'year':[1,1,1,2,2,2], 'adx':['a','a','b','c','d','d'], 'x':[0.,0.,100.,2.,2.,2.]})
r=yearly_median_inference(s,'x',B=9999)
assert r['mean']==1 and r['mean']!=s.x.mean()
assert np.isnan(r['se_cr1']) and r['ci_low']<=r['mean']<=r['ci_high']
assert r['G']==4 and r['N']==6
# Scalar rescaling should not change a wild-bootstrap tail probability.
cell=next(''.join(c['source']) for c in nb['cells'] if 'def wcb(' in ''.join(c['source']))
ns={'np':np,'pd':pd,'stats':stats,'PER':[]};exec(cell.split('rows = []')[0],ns)
y=np.array([1.,2.,2.,4.,4.]);g=np.array([0,0,1,1,1]);X=np.ones((5,1))
p=[ns['wcb'](y*k,X,g,[1.])[1] for k in [1,100,.01]]
assert max(p)-min(p)<1e-12,p
print('date, paired reporting, additive identity, median estimand and bootstrap tie tests passed')
