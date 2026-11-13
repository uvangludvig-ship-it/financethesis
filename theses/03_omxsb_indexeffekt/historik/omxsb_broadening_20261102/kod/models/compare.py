from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime,statsmodels.api as sm
import argparse
P=argparse.ArgumentParser();P.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[4]);P.add_argument('--out',type=Path);A=P.parse_args();R=A.repo.expanduser().resolve();O=(A.out or R/'output/omxsb_broadening_20261102/models').expanduser().resolve();O.mkdir(parents=True,exist_ok=True)
lock=json.loads((O/'DESIGN_LOCK.json').read_text());assert hashlib.sha256((O/'feature_gate_all216.csv').read_bytes()).hexdigest()==next(h for p,h in lock['files'].items() if Path(p).name=='feature_gate_all216.csv')
g=pd.read_csv(O/'feature_gate_all216.csv');y=pd.read_csv(O/'frozen_outcome_input.csv',usecols=['event_id','diff3_1']);g=g.merge(y,on='event_id',how='left',validate='1:1');g['analysis_pass']=g.design_pass & g.diff3_1.notna();g['outcome_missing']=g.diff3_1.isna();g.to_csv(O/'analysis_all216.csv',index=False);d=g[g.analysis_pass].copy().reset_index(drop=True);assert len(d)==194
base=['deletion','precar','log_mcap','pre_sigma','log_prevalued_ADV','notice_trading_days'];features={'M0_pre_characteristics':base,'ML_linear_prevalued_demand':base+['linear_prevalued_company_pp'],'MS_sqrt_volume_demand':base+['sqrt_proxy_pp']};modelnames=list(features);revs=sorted(d.review_cycle.unique());gid=pd.Categorical(d.review_cycle,categories=revs).codes;counts=np.bincount(gid);Y=d.diff3_1.to_numpy();X={m:d[f].to_numpy(float)for m,f in features.items()};G=len(revs)
def trainpredict(x,y,train,test,weights):
 xt=x[train];yt=y[train];w=weights[train];mu=np.average(xt,axis=0,weights=w);sd=np.sqrt(np.average((xt-mu)**2,axis=0,weights=w));
 if np.any(sd<=1e-14):raise ValueError('zero training feature variance')
 A=np.column_stack([np.ones(len(xt)),(xt-mu)/sd]);Aw=A*np.sqrt(w)[:,None];yw=yt*np.sqrt(w);coef,_,rank,singular=np.linalg.lstsq(Aw,yw,rcond=None)
 if rank<A.shape[1]:raise ValueError('training rank deficiency')
 B=np.column_stack([np.ones(test.sum()),(x[test]-mu)/sd]);return B@coef,float(singular.max()/singular.min())
def crossvalidate(multiplicities,detail=False):
 w=multiplicities[gid]/counts[gid];loss=np.full((G,len(modelnames)),np.nan);preds=np.full((len(d),len(modelnames)),np.nan);cond=0.
 for r in np.where(multiplicities>0)[0]:
  tr=(gid!=r)&(w>0);te=gid==r
  for j,m in enumerate(modelnames):
   pred,cc=trainpredict(X[m],Y,tr,te,w);cond=max(cond,cc);loss[r,j]=np.mean((Y[te]-pred)**2);preds[te,j]=pred
 risk=np.nansum(loss*multiplicities[:,None],axis=0)/multiplicities.sum();return risk,loss,preds,cond
risk,loss,pred,condition=crossvalidate(np.ones(G,dtype=int));oos=d[['event_id','RIC','type','review_cycle','diff3_1']].copy();oos.columns=list(oos.columns[:-1])+['observed_matched_CAR_pp']
for j,m in enumerate(modelnames):oos[m+'_prediction']=pred[:,j];oos[m+'_squared_error']=(Y-pred[:,j])**2
oos.to_csv(O/'heldout_event_predictions.csv',index=False);fold=pd.DataFrame(loss,columns=modelnames);fold.insert(0,'review_cycle',revs);fold['N']=counts;fold.to_csv(O/'heldout_review_losses.csv',index=False)
rng=np.random.default_rng(20261102);B=1999;br=[]
for b in range(B):
 mult=np.bincount(rng.integers(0,G,G),minlength=G)
 try:riskb,_,_,cond=crossvalidate(mult);r=dict(draw=b,status='ok',unique_reviews=int((mult>0).sum()),max_standardized_design_condition=cond,**dict(zip(modelnames,riskb)))
 except ValueError as e:r=dict(draw=b,status=str(e),unique_reviews=int((mult>0).sum()))
 br.append(r)
boot=pd.DataFrame(br);boot.to_csv(O/'review_bootstrap_all1999.csv',index=False);valid=boot[boot.status.eq('ok')];comparisons=[]
for ma,mb in [('ML_linear_prevalued_demand','M0_pre_characteristics'),('MS_sqrt_volume_demand','M0_pre_characteristics'),('MS_sqrt_volume_demand','ML_linear_prevalued_demand')]:
 da=risk[modelnames.index(ma)]-risk[modelnames.index(mb)];dd=valid[ma]-valid[mb];lo,hi=np.quantile(dd,[.025,.975]);blo,bhi=np.quantile(dd,[.05/(2*3),1-.05/(2*3)]);comparisons.append(dict(model_a=ma,model_b=mb,meaning='negative difference favors model_a',delta_MSE_pp_squared=da,bootstrap95_lo=lo,bootstrap95_hi=hi,bonferroni98_333_lo=blo,bonferroni98_333_hi=bhi,valid_bootstrap=len(valid),attempted_bootstrap=B,G=G,N=len(d)))
pd.DataFrame(comparisons).to_csv(O/'formal_model_comparisons.csv',index=False)
fits=[];coefrows=[];w=1/counts[gid]
for j,m in enumerate(modelnames):
 xx=sm.add_constant(d[features[m]]).astype(float);fit=sm.WLS(Y,xx,weights=w).fit(cov_type='cluster',cov_kwds={'groups':gid},use_t=True);ci=fit.conf_int()
 for term in xx:coefrows.append(dict(model=m,term=term,coefficient=fit.params[term],SE_CR1=fit.bse[term],lo=ci.loc[term,0],hi=ci.loc[term,1],p_CR1=fit.pvalues[term],N=len(d),G=G))
 fits.append(dict(model=m,N=len(d),G=G,parameters=xx.shape[1],in_sample_weighted_R2=fit.rsquared,leave_review_out_MSE=risk[j],leave_review_out_RMSE=np.sqrt(risk[j]),improvement_MSE_vs_M0_percent=100*(1-risk[j]/risk[0])))
pd.DataFrame(fits).to_csv(O/'model_scores.csv',index=False);pd.DataFrame(coefrows).to_csv(O/'in_sample_coefficients.csv',index=False)
metadata=dict(started_from_design_lock=lock['timestamp_utc'],finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),G=G,N=len(d),valid_bootstrap=len(valid),B=B,seed=20261102,max_original_fold_condition=condition,model_labels=modelnames,no_new_windows=True,not_structural_theory_test=True,not_ex_ante_forecast=True,feature_gate_hash_unchanged=True,input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [O/'DECISIONS.txt',O/'DESIGN_LOCK.json',O/'feature_gate_all216.csv',Path(__file__),O/'frozen_outcome_input.csv']});(O/'RESULTS_METADATA.json').write_text(json.dumps(metadata,indent=2));print(pd.DataFrame(fits).to_string(index=False));print(pd.DataFrame(comparisons).to_string(index=False));print('bootstrap',boot.status.value_counts().to_dict());print(pd.DataFrame(coefrows).query("term in ['linear_prevalued_company_pp','sqrt_proxy_pp']").to_string(index=False))
