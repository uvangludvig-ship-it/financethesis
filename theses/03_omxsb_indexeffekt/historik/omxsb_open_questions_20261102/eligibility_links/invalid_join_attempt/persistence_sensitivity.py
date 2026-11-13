"""Declared historical-list sensitivity; no rematching, no new horizons."""
from pathlib import Path
import sys,json
import pandas as pd
ROOT=Path('/Users/ludviguvang/dev/financethesis')
O=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code/build'))
from robusthet_hela import mean_inference
D=pd.read_csv(O.parent/'persistence_corrected/event_paths.csv')
F=pd.read_csv(O/'review_RIC_status.csv')
P=F.pivot(index='event_id',columns='role',values='status')
out=[];samples=[];selection=[]
for nc in [3,1]:
    required=['event']+[f'c{i}' for i in range(1,nc+1)]
    eligible=set(P.index[P[required].eq('confirmed_main_stock').all(axis=1)])
    for model in ['market_adjusted','market_model']:
        s=D[(D.type=='addition')&(D.post==1)&(D.model==model)&D[f'common{nc}']].copy()
        s['all_required_main_confirmed']=s.event_id.isin(eligible)
        samples.append(s.assign(controls=nc))
        for flag in [True,False]:
            q=s[s.all_required_main_confirmed==flag]
            for h in [1,20]:
                selection.append(dict(controls=nc,model=model,confirmed=flag,N=len(q),G=q.review.nunique(),horizon=h,
                                      estimate=q.groupby('review')[f'diff{nc}_{h}'].mean().mean()))
        q=s[s.all_required_main_confirmed]
        for label,ha,hb in [('level_1',1,None),('level_20',20,None),('level_60',60,None),('level_100',100,None),('change_20_100',100,20)]:
            y=q[f'diff{nc}_{ha}'] if hb is None else q[f'diff{nc}_{ha}']-q[f'diff{nc}_{hb}']
            r=mean_inference(y,q.review,9999,f'historical_main/{model}/{nc}/{label}')
            r.update(model=model,controls=nc,contrast=label,interpretation='exploratory_conditional_on_verified_identity_and_main_stock_screen')
            out.append(r)
R=pd.DataFrame(out);R.to_csv(O/'historical_main_persistence_results.csv',index=False)
pd.concat(samples).to_csv(O/'historical_main_persistence_samples.csv',index=False)
pd.DataFrame(selection).to_csv(O/'historical_main_selection_diagnostic.csv',index=False)
print(R[['model','controls','contrast','N','G','estimate_pp','ci_lo','ci_hi','p_wild']].to_string(index=False))
