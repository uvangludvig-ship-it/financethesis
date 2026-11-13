"""Independent frozen-output audit: existing18 cells, fixed inputs, no new model/horizon."""
from pathlib import Path
import os
import hashlib,json,re
import numpy as np,pandas as pd,statsmodels.api as sm
from scipy import stats
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
D=pd.read_csv(O/'event_paths.csv',parse_dates=['AD','ED']);Z=pd.read_csv(O/'results.csv')
U=pd.read_csv(O.parent/'eligible_pool/review_RIC_control_pool.csv');C=pd.read_csv(O/'selected_controls.csv');Q=pd.read_csv(O/'quote_choices.csv')
L=pd.read_csv(O.parent/'eligibility/dated_stockholm_instrument_roster.csv',dtype={'month':str});L['review']=L.month.str[:4]+'H'+L.month.str[-2:].map({'04':'1','10':'2'})
E=pd.read_csv(R/'output/omxsb_replication_2007/events_car.csv',parse_dates=['AD','ED']);V=E.groupby('review_cycle').agg(AD=('AD','first')).sort_values('AD');km={v:i for i,v in enumerate(V.index)}
CE=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
keys={(e.RIC,km[e.review_cycle]) for e in CE.itertuples() if pd.notna(e.RIC) and e.review_cycle in km}|{(e.RIC,km[e.review_cycle]) for e in E.itertuples()}
errors=[];checks={}
def check(name,condition,detail=None):
 checks[name]=bool(condition)
 if not condition:errors.append({'check':name,'detail':detail})
check('all_results18',len(Z)==18);check('three_controls',D.chosen_controls.eq(3).all());check('event_ids_unique',D.event_id.is_unique)
join=C.merge(U,on=['review','ric'],suffixes=('','_pool'),how='left',indicator=True,validate='many_to_one')
check('all_selected_in_dated_pool',join._merge.eq('both').all());check('selected_isin_matches_pool',join['isin'].eq(join.isin_pool).all());check('selected_issuer_matches_pool',join.issuer.eq(join.company_code).all())
lj=join.merge(L[['review','isin','stock_type','listed_at_month_end','preference_name_flag','company_code','source_excel_row']],on=['review','isin'],suffixes=('','_ledger'),how='left',validate='many_to_one',indicator='ledger_match')
check('selected_in_official_stock_roster',lj.ledger_match.eq('both').all() and lj.stock_type.all() and lj.listed_at_month_end.all());check('no_preference_name_flag',not lj.preference_name_flag.any())
check('three_distinct_issuers',C.groupby('event_id').issuer.nunique().eq(3).all());check('no_own_issuer',C.merge(D[['event_id','issuer']],on='event_id',suffixes=('','_event')).eval('issuer != issuer_event').all())
check('all_selected_quotes_are_pre_canonical',C.merge(Q,on=['review','ric','isin'],validate='many_to_one').selected_quote.all())
# Independent extra screen: current/prior index events identified by dated ticker,
# including census rows with missing RIC (which do not enter the production keys).
def norm(s):return re.sub('[^A-Z0-9]','',str(s).upper())
collisions=[]
for rev,c in C.groupby('review'):
 k=km[rev];ledger=L[L.review.eq(rev)].copy();ledger['ticker_norm']=ledger.ticker.map(norm)
 for x in CE.itertuples():
  if x.review_cycle not in km or km[x.review_cycle] not in (k-1,k):continue
  q=ledger[ledger.ticker_norm.eq(norm(x.ticker))]
  if len(q)==1:
   hits=c[c.issuer.eq(q.iloc[0].company_code)]
   for _,h in hits.iterrows():collisions.append({'selected_for_event':h.event_id,'selected_ric':h.ric,'review':rev,'conflicting_census_event':x.event_id,'conflicting_ric':x.RIC,'conflicting_ticker':x.ticker})
check('no_dated_ticker_current_or_previous_event_issuer',not collisions,collisions)
# Numerical audit of ALL saved pair differences and common-support definitions.
for h in [1,20,60,100]:
 a=D[[f'event_{h}']+[f'c{j}_{h}' for j in [1,2,3]]];v=a.iloc[:,0]-a.iloc[:,1:].mean(axis=1,skipna=False)
 check(f'paired_arithmetic_{h}',np.allclose(v,D[f'diff3_{h}'],equal_nan=True,atol=1e-10))
common=D[[f'diff3_{h}' for h in [1,20,60,100]]].notna().all(axis=1)
check('common100_identical_support',common.eq(D.common100).all())
num=[]
for x in Z.itertuples():
 q=D[D.type.eq(x.type)]
 if x.support=='common100':q=q[q.common100]
 y=q.diff3_100-q.diff3_20 if x.contrast=='change_20_100' else q['diff3_'+x.contrast.split('_')[-1]]
 a=pd.DataFrame({'y':y,'review':q.review}).dropna();g=a.groupby('review',sort=True).y.mean();f=sm.OLS(g.to_numpy(),np.ones((len(g),1))).fit();ci=f.conf_int()[0]
 label=f'eligible_rematch/{x.type}/{x.support}/{x.contrast}'
 def rng(t):return np.random.default_rng(int.from_bytes(hashlib.sha256(('repair-20261101-v5'+str((t,label))).encode()).digest()[:8],'little'))
 w=rng('wild').choice([-1.,1.],(9999,len(g)));b=w*g.to_numpy();ts=b.mean(1)/(b.std(1,ddof=1)/np.sqrt(len(g)));pw=(np.sum(abs(ts)>=abs(f.tvalues[0])-1e-12*max(1,abs(f.tvalues[0])))+1)/10000
 s=rng('sign').choice([-1.,1.],(19999,len(g)))@g.to_numpy()/len(g);ps=(np.sum(abs(s)>=abs(g.mean())-1e-12*max(1,abs(g.mean())))+1)/20000
 delta=max(abs(f.params[0]-x.estimate_pp),abs(ci[0]-x.ci_lo),abs(ci[1]-x.ci_hi),abs(a.y.mean()-x.event_weighted_mean_pp))
 ok=delta<1e-9 and len(a)==x.N and len(g)==x.G and abs(pw-x.p_wild)<1e-10 and abs(ps-x.p_signflip)<1e-10
 check('inference_'+label,ok);num.append(dict(type=x.type,support=x.support,contrast=x.contrast,N=len(a),G=len(g),estimate_pp=f.params[0],ci_lo=ci[0],ci_hi=ci[1],p_wild=pw,p_signflip=ps,max_difference=delta))
# Rebuild predata/ranks independently from the raw panel; no outcome enters this block.
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date']);ix=ix[ix.ric.eq('.OMXSBGI')&ix.close.notna()].set_index('date').sort_index();cal=ix.index;mr=ix.close.pct_change(fill_method=None)*100
raw=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','totret','mcap']);raw.date=pd.to_datetime(raw.date);series={}
for ric,g in raw[raw.ric.isin(U.ric)].groupby('ric'):
 g=g.set_index('date').reindex(cal);a=g.totret.fillna(g.close.pct_change(fill_method=None)*100);a[(a>1000)|(a<-100)]=np.nan
 series[ric]=(a-mr,g.mcap.ffill(limit=10))
rank_errors=[];covdiff=[]
for rev,ed in D.groupby('review'):
 ad=ed.AD.iloc[0];ia=cal.get_loc(ad);k=km[rev];u=U[U.review.eq(rev)];lookup=u.set_index('ric');ce=[]
 for z in u.itertuples():
  if z.ric not in series:continue
  a,m=series[z.ric];p=a.iloc[ia-101:ia-1];cap=m.iloc[ia-2]
  if len(p)!=100 or p.isna().any() or not np.isfinite(cap) or cap<=0:continue
  ce.append(dict(ric=z.ric,isin=z.isin,issuer=z.company_code,pre_observed=int(p.notna().sum()),precar=p.sum(),log_mcap=np.log(cap)))
 a=pd.DataFrame(ce);canon=a.sort_values(['isin','pre_observed','ric'],ascending=[True,False,True],kind='stable').drop_duplicates('isin')
 banned={lookup.loc[ric,'company_code'] for ric,kk in keys if kk in (k-1,k) and ric in lookup.index}
 pool=canon[~canon.issuer.isin(banned)&~canon.ric.map(lambda ric:any((ric,kk) in keys for kk in (k-1,k)))].copy()
 ev=a[a.ric.isin(ed.ric)].set_index('ric').reindex(ed.ric)
 check('raw_event_covariates_'+rev,np.allclose(ev[['precar','log_mcap']],ed[['precar','log_mcap']],atol=1e-8))
 scale=pd.concat([pool[['precar','log_mcap']],ev[['precar','log_mcap']]]);mu=scale.mean();sd=scale.std()
 for z in ed.itertuples():
  eligible=pool[pool.issuer.ne(z.issuer)].copy();ez=(pd.Series({'precar':z.precar,'log_mcap':z.log_mcap})-mu)/sd
  eligible['distance']=np.sqrt((((eligible[['precar','log_mcap']]-mu)/sd-ez)**2).sum(axis=1));chosen=eligible.sort_values(['distance','ric'],kind='stable').drop_duplicates('issuer').head(3)
  want=[getattr(z,f'c{j}_ric') for j in [1,2,3]]
  if chosen.ric.tolist()!=want:rank_errors.append({'event_id':z.event_id,'expected':chosen.ric.tolist(),'saved':want})
check('all_predata_control_rankings_reproduced',not rank_errors,rank_errors)
pd.DataFrame(num).to_csv(O/'validation_inference.csv',index=False)
report={'passed':not errors,'checks':checks,'errors':errors,'raw_pre_rank_events':len(D),'selected_control_rows':len(C),'numerical_cells':len(num),'max_numerical_difference':max(z['max_difference'] for z in num),'limitations':['Only source roster and exact provided identity links are validated; not all OMXSB rules.','Exploratory nominal inference; no causal interpretation.','Later source publication validates earlier historical listing state retrospectively, not ex ante file availability.'],'input_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'run.py',O/'ANALYSIS_DECISIONS.txt',O/'event_paths.csv',O/'results.csv',O/'selected_controls.csv',O.parent/'eligible_pool/review_RIC_control_pool.csv']}}
(O/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2,ensure_ascii=False))
