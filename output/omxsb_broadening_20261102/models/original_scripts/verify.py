from pathlib import Path
import pandas as pd,numpy as np,statsmodels.api as sm,json,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');g=pd.read_csv(O/'analysis_all216.csv',parse_dates=['AD']);d=g[g.analysis_pass].copy();pred=pd.read_csv(O/'heldout_event_predictions.csv');models={'M0_pre_characteristics':['deletion','precar','log_mcap','pre_sigma','log_prevalued_ADV','notice_trading_days'],'ML_linear_prevalued_demand':['deletion','precar','log_mcap','pre_sigma','log_prevalued_ADV','notice_trading_days','linear_prevalued_company_pp'],'MS_sqrt_volume_demand':['deletion','precar','log_mcap','pre_sigma','log_prevalued_ADV','notice_trading_days','sqrt_proxy_pp']};errs=[];checks=[]
for review in sorted(d.review_cycle.unique()):
 train=d[d.review_cycle.ne(review)];test=d[d.review_cycle.eq(review)];w=1/train.groupby('review_cycle').event_id.transform('count')
 for m,cols in models.items():
  # Independent implementation: statsmodels on unstandardized predictors.
  X=sm.add_constant(train[cols],has_constant='add').astype(float);fit=sm.WLS(train.diff3_1,X,weights=w).fit();pp=fit.predict(sm.add_constant(test[cols],has_constant='add').astype(float));saved=pred.set_index('event_id').loc[test.event_id,m+'_prediction'].to_numpy();err=float(np.max(np.abs(pp.to_numpy()-saved)));assert err<1e-8,(review,m,err);errs.append(err);checks.append(dict(review=review,model=m,N_train=len(train),N_test=len(test),max_prediction_error=err,train_reviews=train.review_cycle.nunique(),test_review_absent_from_training=review not in set(train.review_cycle)))
pd.DataFrame(checks).to_csv(O/'independent_fold_reproduction.csv',index=False)
# Sanity masking: log every impossible return removed by the fixed upstream(-100%,1000%) bound; do not silently call it no filter.
p=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','totret']);p=p[p.ric.isin(g.RIC)];S={r:a.set_index('date').sort_index()for r,a in p.groupby('ric')};ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv');cal=pd.DatetimeIndex(sorted(pd.to_datetime(ix.loc[ix.ric.eq('.OMXSBGI')&ix.close.notna(),'date']).unique()));masked=[];counts=[]
for z in g.itertuples():
 i=int(cal.searchsorted(z.AD));rr=S[z.RIC].reindex(cal).totret.iloc[i-61:i-11];bad=rr[(rr<-100)|(rr>1000)];counts.append(dict(event_id=z.event_id,RIC=z.RIC,N_window=len(rr),already_missing=int(rr.isna().sum()),newly_masked=len(bad),analysis_pass=z.analysis_pass))
 for date,value in bad.items():masked.append(dict(event_id=z.event_id,RIC=z.RIC,date=date,raw_return_percent=value))
pd.DataFrame(masked,columns=['event_id','RIC','date','raw_return_percent']).to_csv(O/'pre_returns_sanity_masked_values.csv',index=False);pd.DataFrame(counts).to_csv(O/'pre_returns_sanity_counts_all216.csv',index=False)
# Unit algebra, common sample, score weights, and review risk definition.
assert d.event_id.nunique()==194 and d.review_cycle.nunique()==14;assert np.allclose(d.linear_prevalued_company_pp,100*d.Q_after_units/d.factor*d.prequarter_class_price/d.prequarter_company_cap);assert np.allclose(d.sqrt_proxy_pp,100*d.pre_sigma*np.sign(d.signed_Q_over_ADV)*np.sqrt(abs(d.signed_Q_over_ADV)))
sc=pd.read_csv(O/'model_scores.csv');fold=pd.read_csv(O/'heldout_review_losses.csv')
for z in sc.itertuples():assert abs(fold[z.model].mean()-z.leave_review_out_MSE)<1e-10
boot=pd.read_csv(O/'review_bootstrap_all1999.csv');assert len(boot)==1999;invalid=boot[boot.status.ne('ok')];invalid.to_csv(O/'invalid_bootstrap_draws.csv',index=False)
repeated=d.groupby('issuer').agg(events=('event_id','size'),reviews=('review_cycle','nunique'));repeated.to_csv(O/'issuer_repeat_counts.csv');lock=json.loads((O/'DESIGN_LOCK.json').read_text());assert hashlib.sha256((O/'feature_gate_all216.csv').read_bytes()).hexdigest()==lock['files'][str(O/'feature_gate_all216.csv')]
res=dict(N=194,G=14,independent_training_and_holdout_fits=42,max_prediction_error=max(errs),all_models_same_sample=True,review_equal_loss_means_verified=True,pre_return_sanity_newly_masked_event_day_rows=len(masked),no_newly_masked_outlier_values=len(masked)==0,unique_issuers=len(repeated),issuers_repeated_across_reviews=int(repeated.reviews.gt(1).sum()),max_issuer_reviews=int(repeated.reviews.max()),bootstrap_attempted=1999,bootstrap_valid=int(boot.status.eq('ok').sum()),invalid_bootstrap_reasons=invalid.status.value_counts().to_dict(),gate_hash_unchanged=True)
(O/'VALIDATION.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
