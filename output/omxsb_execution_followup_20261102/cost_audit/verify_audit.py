from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();o=Path(a.out)
e=pd.read_csv(o/'saved_event_accounting_inputs.csv');z=pd.read_csv(o/'review_accounting.csv');s=pd.read_csv(o/'conditional_scenarios.csv');w=pd.read_csv(o/'event_weight_audit.csv');v=pd.read_csv(o/'review_weight_coverage.csv')
checks={}
for variant,col in [('primär','prem'),('sekundär','prem2')]:
 q=e.dropna(subset=['w',col]); expected=float(np.dot(q.w,q[col])*100);got=z[z.variant==variant].linear_bp.sum();checks['sum_'+variant]=bool(np.isclose(expected,got,atol=1e-10))
checks['weights_reproduce']=bool(np.allclose(w.w_saved,w.w_reproduced,equal_nan=True,atol=1e-13))
checks['78_denominator_endpoints']=len(v)==78
checks['all_scenarios_retained']=len(s)==21 and set(s.assumed_premium_fraction)=={0,.5,1}
checks['2026_not_annualized']=bool(~s[s.period=='2026_H1_only'].annual_average.any())
checks['per100000_conversion']=bool(np.allclose(s.SEK_per_100000,10*s.scenario_bp))
checks['half_and_zero_scenarios']=all(np.isclose(g.loc[g.assumed_premium_fraction==.5,'scenario_bp'].iloc[0],.5*g.loc[g.assumed_premium_fraction==1,'scenario_bp'].iloc[0]) and g.loc[g.assumed_premium_fraction==0,'scenario_bp'].iloc[0]==0 for _,g in s.groupby('period'))
checks['pre_AD_AUM_month']=bool((pd.to_datetime(z.aum_prior_month+'-01')<pd.to_datetime(z.AD).dt.to_period('M').dt.to_timestamp()).all())
checks['negative_reviews_retained']=bool((z.linear_bp<0).any())
(o/'validation.json').write_text(json.dumps(checks,indent=2));assert all(checks.values()),checks;print(json.dumps(checks,indent=2))
