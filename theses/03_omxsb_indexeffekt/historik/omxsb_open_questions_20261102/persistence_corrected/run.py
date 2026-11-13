"""Exploratory, same-sample persistence analysis. See ANALYSIS_DECISIONS.md."""
from pathlib import Path
import os
import sys, json, hashlib, platform
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

ROOT=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code/build'))
import robusthet_hela as base

H=[1,20,60,100]
CONTRASTS={'level_1':(1,None),'level_20':(20,None),'level_60':(60,None),'level_100':(100,None),
           'change_1_20':(20,1),'change_20_60':(60,20),'change_60_100':(100,60),'change_20_100':(100,20)}
inputs=[ROOT/'output/omxsb_robusthet_20261101/T2_matches.csv',ROOT/'output/omxsb_replication_2007/events_car.csv',
        ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',
        ROOT/'runda2_resultat/T5urval_T7_T8b_events.csv',ROOT/'code/build/robusthet_hela.py',OUT/'ANALYSIS_DECISIONS.md',OUT/'IDENTITY_AMENDMENT.md',Path(__file__)]
M=pd.read_csv(inputs[0]); ev=pd.read_csv(inputs[1],parse_dates=['AD','ED'])
M=M.merge(ev[['event_id','AD','ED']],on='event_id',validate='one_to_one')
# Conservative identity repair; exclude whole event, never rematch on outcomes.
M=M[~M.event_id.isin(['OMXSB-2019H1-06','OMXSB-2026H1-07'])].copy()
panel=base.Panel(ROOT,inputs[2]);print('Loaded repaired return panel',flush=True)
# Reconstruct return array from its cumulative sums; restore all original missing values.
A=np.diff(panel.cs,axis=0); A[np.diff(panel.cn,axis=0)>0]=np.nan
ix=pd.read_csv(inputs[3],parse_dates=['date'])
market=ix[ix.ric=='.OMXSBGI'].set_index('date')['close'].reindex(panel.cal).pct_change(fill_method=None).to_numpy()*100
beta_cache={};beta_log=[]
def beta_fit(ric,iad,review):
    key=(ric,iad)
    if key in beta_cache:return beta_cache[key]
    if ric not in panel.columns or iad<250:return None
    j=panel.columns[ric]; xx=market[iad-250:iad-120];yy=A[iad-250:iad-120,j]+xx
    valid=np.isfinite(xx)&np.isfinite(yy)
    if valid.sum()<100 or np.std(xx[valid])<1e-12: fit=None
    else:
        X=np.column_stack([np.ones(valid.sum()),xx[valid]])
        fit=np.linalg.lstsq(X,yy[valid],rcond=None)[0]
    beta_cache[key]=fit
    beta_log.append(dict(review=review,ric=ric,n=int(valid.sum()),alpha=fit[0] if fit is not None else np.nan,beta=fit[1] if fit is not None else np.nan))
    return fit
def value(ric,iad,ied,h,model,review):
    v=panel.car(ric,iad-1,ied+h)
    if not np.isfinite(v):return np.nan
    if model=='market_adjusted':return v
    fit=beta_fit(ric,iad,review)
    if fit is None:return np.nan
    mm=market[iad-1:ied+h+1]
    return v-fit[0]*len(mm)-(fit[1]-1)*mm.sum()

rows=[]; validation=[]
for e in M.to_dict('records'):
    iad=int(panel.pos[e['AD']]);ied=int(panel.pos[e['ED']])
    recomputed=panel.car(e['ric'],iad-1,ied+1)
    if np.isfinite(e['car']) and np.isfinite(recomputed): validation.append(abs(e['car']-recomputed))
    for model in ['market_adjusted','market_model']:
        d={k:e[k] for k in ['event_id','ric','issuer','review','type','post','AD','ED']};d['model']=model
        for role,ric in [('event',e['ric'])]+[(f'c{j}',e[f'c{j}_ric']) for j in [1,2,3]]:
            d[role+'_ric']=ric
            for h in H:d[f'{role}_{h}']=value(ric,iad,ied,h,model,e['review'])
        for nc in [1,3]:
            for h in H:
                d[f'diff{nc}_{h}']=base.paired_difference(d[f'event_{h}'],[d[f'c{j}_{h}'] for j in range(1,nc+1)],nc)
            d[f'common{nc}']=all(np.isfinite(d[f'diff{nc}_{h}']) for h in H)
        rows.append(d)
D=pd.DataFrame(rows);D.to_csv(OUT/'event_paths.csv',index=False)
pd.DataFrame(beta_log).to_csv(OUT/'market_model_estimates.csv',index=False)
assert max(validation)<1e-8

results=[];attrition=[];review_paths=[]
for model in ['market_adjusted','market_model']:
 for nc in [3,1]:
  for typ in ['addition','deletion']:
   for post in [1,0]:
    q=D[(D.model==model)&(D.type==typ)&(D.post==post)].copy()
    common=q[q[f'common{nc}']].copy()
    for h in H:
        attrition.append(dict(model=model,controls=nc,type=typ,post=post,horizon=h,preselected=len(q),
                              available=int(q[f'diff{nc}_{h}'].notna().sum()),common=len(common)))
    for support,frame in [('common100',common),('available',q)]:
     for label,(ha,hb) in CONTRASTS.items():
        y=frame[f'diff{nc}_{ha}'] if hb is None else frame[f'diff{nc}_{ha}']-frame[f'diff{nc}_{hb}']
        if support=='available' and hb is not None:continue
        identity=f'{model}/{nc}/{typ}/{post}/{support}/{label}'
        res=base.mean_inference(y,frame.review,B=9999,label=identity)
        res.update(model=model,controls=nc,type=typ,post=post,support=support,contrast=label)
        results.append(res)
        if support=='common100':
            for review,v in pd.DataFrame({'review':frame.review,'y':y}).groupby('review').y.mean().items():
                review_paths.append(dict(model=model,controls=nc,type=typ,post=post,contrast=label,review=review,value=v))

R=pd.DataFrame(results);R.to_csv(OUT/'results_all.csv',index=False)
pd.DataFrame(attrition).to_csv(OUT/'attrition.csv',index=False)
pd.DataFrame(review_paths).to_csv(OUT/'review_paths.csv',index=False)
primary=D[(D.model=='market_adjusted')&(D.type=='addition')&(D.post==1)&D.common3].copy()
primary['delta']=primary.diff3_100-primary.diff3_20
influence=[]
for col in ['review','issuer']:
 for omitted in sorted(primary[col].unique()):
    q=primary[primary[col]!=omitted]
    influence.append(dict(unit=col,omitted=omitted,estimate=q.groupby('review').delta.mean().mean(),N=len(q),G=q.review.nunique()))
pd.DataFrame(influence).to_csv(OUT/'primary_influence.csv',index=False)
# Independent statsmodels check of review-mean intercept inference.
gm=primary.groupby('review').delta.mean()
fit=sm.OLS(gm.to_numpy(),np.ones((len(gm),1))).fit()
pr=R[(R.model=='market_adjusted')&(R.controls==3)&(R.type=='addition')&(R.post==1)&(R.support=='common100')&(R.contrast=='change_20_100')].iloc[0]
assert abs(fit.params[0]-pr.estimate_pp)<1e-10
assert np.max(np.abs(fit.conf_int()[0]-[pr.ci_lo,pr.ci_hi]))<1e-9

# Independent common-support arithmetic diagnostic of Claude's old T5 sample.
S=pd.read_csv(inputs[4]);diag=[]
for typ in ['addition','deletion']:
 for post in [1,0]:
    s=S[(S.type==typ)&(S.post==post)].dropna(subset=[f'car_ED+{h}' for h in H]+['ru','lm']).copy()
    s=base.supported_reviews(s)
    if s.empty:continue
    X=np.column_stack([s.event,s.ru,s.lm,pd.get_dummies(s.review,dtype=float).values])
    for label,(ha,hb) in CONTRASTS.items():
        y=s[f'car_ED+{ha}'].to_numpy()
        if hb is not None:y=y-s[f'car_ED+{hb}'].to_numpy()
        f=sm.OLS(y,X).fit(cov_type='cluster',cov_kwds={'groups':s.review},use_t=True)
        diag.append(dict(type=typ,post=post,contrast=label,estimate_pp=f.params[0],ci_lo=f.conf_int()[0,0],ci_hi=f.conf_int()[0,1],p=f.pvalues[0],N=len(s),events=int(s.event.sum()),G=s.review.nunique(),status='old_sample_arithmetic_only_known_selection_defects'))
pd.DataFrame(diag).to_csv(OUT/'old_T5_common_support_diagnostic.csv',index=False)

meta=dict(generated_at=datetime.now(timezone.utc).isoformat(),exploratory=True,preregistered=False,
          panel_qa=panel.qa,baseline_reproduced=len(validation),max_baseline_difference=max(validation),
          primary_statsmodels_check=True,python=platform.python_version(),inputs={str(p):base.file_hash(p) for p in inputs},
          limitations=['historical eligibility unverified','long-horizon complete-case survival selection','cluster independence across reviews and issuer reuse','not causal identification','old T5 diagnostic retains known defects'])
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
print('PRIMARY and common-sample levels:',flush=True)
print(R[(R.model=='market_adjusted')&(R.controls==3)&(R.type=='addition')&(R.post==1)&(R.support=='common100')][['contrast','N','G','estimate_pp','ci_lo','ci_hi','p_wild']].to_string(index=False))
print('All declared outputs saved',flush=True)
