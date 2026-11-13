"""One locked gross-value accounting contrast after completed common-source gate."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os
import pandas as pd,numpy as np
from scipy.stats import t
O=Path(os.environ.get('OMXSB_ACTIVITY_WORKDIR',Path(__file__).resolve().parent));R=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis'));PVT=O/'private';PVT.mkdir(exist_ok=True)
assert not (O/'OUTCOME_LOCK.json').exists(),'Do not overwrite frozen first outcome run'
paths={'spec':O/'PRIMARY_SPEC.txt','roles':O/'ROLE_FINAL_SOURCE_GATE.csv','event_gate':O/'EVENT_FINAL_SOURCE_GATE.csv','unit_gate':O/'UNIT_GATE_SUMMARY.json','panel':R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet','calendar':R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lock={'created_utc':datetime.now(timezone.utc).isoformat(),'stage':'fixed_single_primary_before_first_arithmetic','inputs':{k:{'path':str(p),'sha256':sha(p)}for k,p in paths.items()},'script_sha256':sha(Path(__file__)),'no_new_price_or_FTN_outcomes':True};(O/'OUTCOME_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
F=pd.read_csv(paths['event_gate']);E=F[F.gate_pass];S=pd.read_csv(paths['roles']);S=S[S.event_id.isin(E.event_id)].copy();assert len(E)==65 and E.review.nunique()==10 and len(S)==260 and S.cash_gate_pass.all();assert S.groupby('event_id').role.apply(set).map(lambda x:x=={'event','c1','c2','c3'}).all()
I=pd.read_csv(paths['calendar'],usecols=['ric','date','close']);I.date=pd.to_datetime(I.date);cal=pd.DatetimeIndex(sorted(I.loc[I.ric.isin(['.OMXSBGI','.OMXSPI'])&I.close.gt(0),'date'].unique()));ix={d:i for i,d in enumerate(cal)}
P=pd.read_parquet(paths['panel'],columns=['ric','date','turnover','source'],filters=[('ric','in',sorted(S.ric.unique()))]);P.date=pd.to_datetime(P.date);assert not P.duplicated(['ric','date']).any();book={ric:g.set_index('date')for ric,g in P.groupby('ric')}
roles=[];raw=[];amount=[]
for z in S.itertuples():
 bdates=cal[(cal>=pd.Timestamp(z.baseline_start))&(cal<=pd.Timestamp(z.baseline_end))];wdates=cal[(cal>=pd.Timestamp(z.window_start))&(cal<=pd.Timestamp(z.window_end))];assert len(bdates)==50 and len(wdates)==45 and bdates.max()<wdates.min()
 a=ix[pd.Timestamp(z.AD)];e=ix[pd.Timestamp(z.ED)];be=min(a-12,e-23);assert bdates.equals(cal[be-49:be+1]) and wdates.equals(cal[e-22:e+23]);target=cal[e-1]
 d=book[z.ric];b=d.reindex(bdates);w=d.reindex(wdates);assert b.source.eq('tr').all()and w.source.eq('tr').all();bv=b.turnover.to_numpy(dtype=float);wv=w.turnover.to_numpy(dtype=float);assert np.isfinite(bv).all()and np.isfinite(wv).all()and(bv>=0).all()and(wv>=0).all();base=float(bv.mean());assert base>0
 norm=wv/base-1;D=float(w.loc[target,'turnover']/base-1);T=float(norm.sum());other=float(norm[wdates!=target].sum());assert np.isclose(T,D+other,rtol=1e-12,atol=1e-10)
 roles.append({'event_id':z.event_id,'review':z.review,'role':z.role,'ric':z.ric,'total45':T,'day_EDminus1':D,'other44':other})
 amount.append({'event_id':z.event_id,'review':z.review,'role':z.role,'ric':z.ric,'baseline_mean_SEK':base,'target_SEK':float(w.loc[target,'turnover']),'window_total_SEK':float(wv.sum()),'baseline_N':50,'window_N':45})
 for period,frame in [('baseline',b),('window',w)]:
  for date,row in frame.iterrows():raw.append({'event_id':z.event_id,'review':z.review,'role':z.role,'ric':z.ric,'date':date.strftime('%Y-%m-%d'),'period':period,'is_EDminus1':date==target,'turnover':row.turnover,'source':row.source})
Q=pd.DataFrame(roles);Q.to_csv(O/'NORMALIZED_ROLE_COMPONENTS.csv',index=False);pd.DataFrame(amount).to_csv(PVT/'ROLE_SEK_INPUTS.csv',index=False);pd.DataFrame(raw).to_csv(PVT/'RAW_RELEVANT_TURNOVER.csv.gz',index=False)
cols=['total45','day_EDminus1','other44'];matched=[]
for event_id,g in Q.groupby('event_id'):
 ev=g[g.role.eq('event')].iloc[0];c=g[~g.role.eq('event')];assert len(c)==3
 z={'event_id':event_id,'review':ev.review,'event_ric':ev.ric}
 for f in cols:z[f]=float(ev[f]-c[f].mean())
 assert np.isclose(z['total45'],z['day_EDminus1']+z['other44'],rtol=1e-12,atol=1e-10);matched.append(z)
M=pd.DataFrame(matched);M.to_csv(O/'EVENT_COMPONENTS.csv',index=False)
V=M.groupby('review')[cols].mean();V['N_events']=M.groupby('review').size();V.reset_index().to_csv(O/'REVIEW_COMPONENTS.csv',index=False)
G=len(V);n=len(M);mean=float(V.total45.mean());se=float(V.total45.std(ddof=1)/np.sqrt(G));crit=float(t.ppf(.975,G-1));cov=V[cols].cov()/G;cov.to_csv(O/'JOINT_COVARIANCE_OF_MEANS.csv');identity_error=float((V.total45-V.day_EDminus1-V.other44).abs().max());variance_error=float(abs(cov.loc['total45','total45']-cov.loc['day_EDminus1','day_EDminus1']-cov.loc['other44','other44']-2*cov.loc['day_EDminus1','other44']));assert identity_error<1e-10 and variance_error<1e-10
result={'created_utc':datetime.now(timezone.utc).isoformat(),'N_events':n,'G_reviews':G,'df':G-1,'unit':'baseline daily gross SEK trading-value equivalents; event-minus-mean3fixedpeers','primary_total45_mean':mean,'primary_SE_review_means':se,'primary_CI95':[mean-crit*se,mean+crit*se],'descriptive_day_EDminus1_mean':float(V.day_EDminus1.mean()),'descriptive_other44_mean':float(V.other44.mean()),'weighting':'Within-review equal events; across-review equal weights','p_values_reported':False,'component_intervals_reported':False,'exploratory_nominal_inference':True,'all_review_means_retained':True,'outcome_based_exclusions':False,'private_raw_rows':len(raw),'QA':{'role_component_rows':len(Q),'matched_component_rows':len(M),'review_additive_identity_max_error':identity_error,'variance_covariance_identity_error':variance_error,'constant_baseline_N_all_roles':50,'constant_window_N_all_roles':45},'limitations':['Prior ownership-covered70 additions, not full universe;65source-complete selected','Gross SEK amount reflects both quantity and price, and is venue-specific','Fixed peers may be affected by other indices/rebalancing','Shared issuers/controls and market regimes limit independent-review t approximation','Positive total does not establish index causation or exclude displacement beyond45days','No offset fraction or inventory/forced-flow interpretation']}
(O/'PRIMARY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
