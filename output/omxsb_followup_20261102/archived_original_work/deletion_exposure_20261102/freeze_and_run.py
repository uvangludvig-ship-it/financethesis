from pathlib import Path
import json,hashlib,sys,datetime
import pandas as pd,numpy as np
from scipy import stats
import statsmodels.api as sm
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis')
G=json.loads((O/'gate_summary.json').read_text());assert G['gate_pass'] and not G['new_price_outcomes_loaded']
D=pd.read_csv(O/'gate_event_ledger.csv');T=D[D.gate_included].copy().sort_values('event_id')
# Freeze exact sample and model before outcome file is read.
lock=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),gate_sha256=hashlib.sha256((O/'gate_event_ledger.csv').read_bytes()).hexdigest(),protocol_sha256=hashlib.sha256((O/'GATE_PROTOCOL.txt').read_bytes()).hexdigest(),event_ids=T.event_id.tolist(),main='equal-review WLS: diff3_1 ~ reviewFE + exposure/0.1 + log_mcap + precar + log_liquidity',sensitivity='same rows: diff3_1 ~ reviewFE + exposure/0.1',CI='CR1 reviewcluster t(G-1)',wild='restrictednull studentized Rademacher9999 fixedhashseed',unplanned_variants=[])
if (O/'ANALYSIS_LOCK.json').exists():
 old=json.loads((O/'ANALYSIS_LOCK.json').read_text())
 assert old['event_ids']==lock['event_ids'] and old['gate_sha256']==lock['gate_sha256'] and old['protocol_sha256']==lock['protocol_sha256']
 lock=old  # Preserve the actual first lock timestamp on a reproduction.
else:
 (O/'ANALYSIS_LOCK.json').write_text(json.dumps(lock,indent=2))
P=R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv'
y=pd.read_csv(P,usecols=['event_id','diff3_1'])
T=T.merge(y,on='event_id',how='left',validate='1:1');T['price_outcome_missing']=T.diff3_1.isna()
# Only declared short outcome; no horizon or outcome-based replacement.
T.to_csv(O/'analysis_event_ledger_all_frozen_rows.csv',index=False)
n_outcome_missing=int(T.price_outcome_missing.sum())
T=T[T.diff3_1.notna()].copy();assert T.review_cycle.nunique()>=10
sys.path.insert(0,str(R/'code/build'));import robusthet_hela as b
FE=pd.get_dummies(T.review_cycle,dtype=float)
w=1/T.groupby('review_cycle').event_id.transform('size').to_numpy()
x=(T.exposure_company_pp/.1).to_numpy()
y=T.diff3_1.to_numpy();groups=T.review_cycle.to_numpy();G=T.review_cycle.nunique()
rows=[];validation=[]
for name,controls in [('primary_size_preCAR_official_liquidity',['log_mcap','precar','log_liquidity']),('sensitivity_reviewFE_only',[])]:
 C=T[controls].copy()
 if controls:C=(C-C.mean())/C.std()
 X=np.column_stack([FE,x,C]);j=FE.shape[1]
 Xw=X*np.sqrt(w[:,None]);yw=y*np.sqrt(w)
 f=b.cluster_fit(Xw,yw,groups)
 z=sm.WLS(y,X,weights=w).fit(cov_type='cluster',cov_kwds={'groups':groups,'use_correction':True},use_t=True)
 assert np.allclose(f['coef'],z.params,atol=1e-8)
 assert np.allclose(f['se'],z.bse,atol=1e-8)
 beta=float(f['coef'][j]);se=float(f['se'][j]);crit=stats.t.ppf(.975,G-1)
 iqr=T.exposure_company_pp.quantile(.75)-T.exposure_company_pp.quantile(.25)
 row=dict(model=name,N=len(T),G_reviews=G,N_issuers=T.issuer.nunique(),exposure_unit='0.1 company percentagepoint preinventory',outcome='stock-minus-three-fixed-controls CARpp AD-1:ED+1',estimate=beta,se_CR1=se,ci_lo=beta-crit*se,ci_hi=beta+crit*se,p_cluster_t=2*stats.t.sf(abs(beta/se),G-1),p_wild=b.wild_cluster_p(Xw,yw,groups,j,B=9999,label='deletion_exposure20261102/'+name),exposure_iqr_pp=float(iqr),estimated_return_difference_IQR=beta*iqr/.1,ci_IQR_lo=(beta-crit*se)*iqr/.1,ci_IQR_hi=(beta+crit*se)*iqr/.1,weight='each review totalweight1',omitted_float='historical freefloat unavailable')
 rows.append(row);validation.append(dict(model=name,statsmodels_coef_maxdiff=float(np.max(abs(f['coef']-z.params))),statsmodels_se_maxdiff=float(np.max(abs(f['se']-z.bse))),rank=int(np.linalg.matrix_rank(Xw)),columns=Xw.shape[1]))
 pd.DataFrame({'column':list(FE.columns)+['exposure_per_0_1pp']+controls,'coef':f['coef'],'se_CR1':f['se']}).to_csv(O/(name+'_all_coefficients.csv'),index=False)
# Quantity validation uses same frozen analysis sample, not a sample chosen for liquidation.
T['quarter_delta_prevalue_pp']=100*(T.after_quantity/T.factor-T.before_quantity)*T.fi_price_before/T.pre_mcap
T['quarter_residual_prevalue_pp']=100*(T.after_quantity/T.factor)*T.fi_price_before/T.pre_mcap
assert np.allclose(T.quarter_delta_prevalue_pp+T.exposure_company_pp,T.quarter_residual_prevalue_pp)
T['after_zero']=T.after_quantity.eq(0);T['before_zero']=T.before_quantity.eq(0)
T['after_equal_before']=np.isclose(T.after_quantity/T.factor,T.before_quantity)
T['observed_reduction']=T.quarter_delta_prevalue_pp.lt(0)
T.to_csv(O/'analysis_event_ledger.csv',index=False)
q=T.groupby('review_cycle').agg(N=('event_id','size'),pre_inventory_pp=('exposure_company_pp','mean'),net_change_prevalue_pp=('quarter_delta_prevalue_pp','mean'),remaining_inventory_prevalue_pp=('quarter_residual_prevalue_pp','mean'),before_zero_count=('before_zero','sum'),after_zero_count=('after_zero','sum'),reductions=('observed_reduction','sum'))
q.to_csv(O/'quarter_liquidation_review_description.csv')
summ=dict(N=len(T),G=G,prezero=int(T.before_zero.sum()),afterzero=int(T.after_zero.sum()),positive_before=int(T.before_quantity.gt(0).sum()),positive_before_afterzero=int((T.before_quantity.gt(0)&T.after_zero).sum()),observed_reduction=int(T.observed_reduction.sum()),positive_after=int(T.after_quantity.gt(0).sum()),review_mean_pre_inventory_pp=float(q.pre_inventory_pp.mean()),review_mean_net_change_prevalue_pp=float(q.net_change_prevalue_pp.mean()),review_mean_remaining_inventory_prevalue_pp=float(q.remaining_inventory_prevalue_pp.mean()),afterto_pre_inventory_ratio_of_review_means=float(q.remaining_inventory_prevalue_pp.mean()/q.pre_inventory_pp.mean()),not_transaction_volume=True)
(O/'quarter_liquidation_summary.json').write_text(json.dumps(summ,indent=2));pd.DataFrame(rows).to_csv(O/'results.csv',index=False)
(O/'validation.json').write_text(json.dumps(dict(models=validation,N_frozen=lock['event_ids'].__len__(),N_outcome_missing=n_outcome_missing,normalization_identity=True,source_prices_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),lock_sha256=hashlib.sha256((O/'ANALYSIS_LOCK.json').read_bytes()).hexdigest(),no_horizon_search=True),indent=2))
print(pd.DataFrame(rows).to_string(index=False));print(json.dumps(summ,indent=2))
