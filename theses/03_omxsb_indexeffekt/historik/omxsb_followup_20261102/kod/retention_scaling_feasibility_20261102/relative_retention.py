from pathlib import Path
import pandas as pd,numpy as np,json,hashlib
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'additions_20261102'))
from portable_paths import analysis_paths, first_output, comparison_function, repository_source, verify_original_lock
R,O=analysis_paths('retention_scaling_feasibility_20261102')
verify_original_lock(O,'gate_freeze_hashes.json')
G=pd.read_csv(O/'core_gate_frozen.csv');S=pd.read_csv(O/'core_gate_summary.csv');T=pd.read_csv(first_output(R)/'retention_followup_20261102/position_quantities.csv')
assert len(T)==238 and T.event_id.nunique()==119
G['core_quantity_ratio']=np.where(G.gate_pass,G.q1/(G.q0*G.splitfactor),np.nan)
factors=G[G.gate_pass].groupby(['fund_id','review']).agg(core_factor=('core_quantity_ratio','median'),core_zero_endpoints=('q1',lambda x:int(x.eq(0).sum()))).reset_index()
F=S.merge(factors,on=['fund_id','review'],validate='1:1');F['relative_gate_pass']=F.fund_review_gate_pass&F.core_factor.gt(0)
Z=T.merge(F[['fund_id','review','core_factor','relative_gate_pass']],on=['fund_id','review'],validate='m:1');Z['relative_quantity_ratio']=np.where(Z.q_index.gt(0)&Z.gate_pass&Z.relative_gate_pass,Z.quantity_retention_ratio/Z.core_factor,np.nan)
Z['relative_direction']=np.select([Z.relative_quantity_ratio.isna(),Z.relative_quantity_ratio.lt(1),Z.relative_quantity_ratio.gt(1)],['undefined','decreased','increased'],default='unchanged')
Z['estimand']='target_share_quantity_growth_divided_by_median_reference_basket_share_quantity_growth'
rows=[]
for (fid,fund),g in Z.groupby(['fund_id','fund']):
 v=g.dropna(subset=['relative_quantity_ratio']);r=v.groupby('review').relative_quantity_ratio.mean()
 rows.append(dict(fund_id=fid,fund=fund,all_events=len(g),defined_N=len(v),reviews=v.review.nunique(),initial_zero=int(g.q_index.eq(0).sum()),other_undefined=int(g.q_index.gt(0).sum()-len(v)),median_relative_ratio=v.relative_quantity_ratio.median(),equal_review_mean_relative_ratio=r.mean(),min_relative_ratio=v.relative_quantity_ratio.min(),max_relative_ratio=v.relative_quantity_ratio.max(),decreased=int(v.relative_quantity_ratio.lt(1).sum()),unchanged=int(v.relative_quantity_ratio.eq(1).sum()),increased=int(v.relative_quantity_ratio.gt(1).sum())))
G.to_csv(O/'core_ratios_all.csv',index=False);F.to_csv(O/'fund_review_factors.csv',index=False);Z.to_csv(O/'relative_retention_all.csv',index=False);pd.DataFrame(rows).to_csv(O/'relative_retention_summary.csv',index=False)
(O/'outcome_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'core_gate_frozen.csv',O/'fund_review_factors.csv',O/'relative_retention_all.csv',O/'relative_retention_summary.csv',Path(__file__)]},indent=2))
print(pd.DataFrame(rows).to_string(index=False));print(F.to_string(index=False));print('PREVIOUS SINGLE DECLINE',Z[Z.quantity_direction.eq('decreased')][['event_id','RIC','fund','quantity_retention_ratio','core_factor','relative_quantity_ratio']].to_string(index=False))
