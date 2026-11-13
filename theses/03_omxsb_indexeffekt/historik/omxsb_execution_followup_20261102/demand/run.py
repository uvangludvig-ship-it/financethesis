"""Exploratory measurement repair; no fresh price calculation and no guessed zeros."""
from pathlib import Path
import argparse, ast, datetime, hashlib, json, re, importlib.util
import numpy as np
import pandas as pd
from scipy.stats import t

ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--out',required=True);ap.add_argument('--freeze',action='store_true');a=ap.parse_args()
R=Path(a.repo).resolve();O=Path(a.out).resolve();O.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
paths={
 'lseg_raw':'code/claude_checks/data/runda8_fondagare.csv.gz',
 'original_code':'code/claude_checks/runda9.py',
 'original_events':'code/claude_checks/runda8_input.csv',
 'field_test':'code/claude_checks/data/runda8_falttest.txt',
 'fi_panel':'output/omxsb_followup_20261102/mandate_upgrade_20261102/classified_fund_event_panel.csv.gz',
 'fi_raw':'output/omxsb_open_questions_20261102/demand_quarter/quarter_raw_target_instruments.csv.gz',
 'fi_reports':'output/omxsb_open_questions_20261102/demand_quarter/raw_fund_report_metadata.csv',
 'fi_events':'output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv',
 'fi_evidence':'output/omxsb_followup_20261102/mandate_upgrade_20261102/upgraded_fund_review_evidence.csv',
 'price':'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',
 'price_code':'output/omxsb_open_questions_20261102/eligible_rematch/run.py',
 'price_panel_code':'code/build/robusthet_hela.py',
 'mandate_reading':'output/omxsb_followup_20261102/mandate_upgrade_20261102/PRIMARY_READING.txt',
}
if a.freeze:
 assert not (O/'ANALYSIS_LOCK.json').exists(),'Existing analysis lock cannot be overwritten'
 lock={'actual_utc_before_run':now(),'prior_outcomes_known':True,'exploratory':True,'files':{k:{'relative_path':p,'sha256':sha(R/p)} for k,p in paths.items()},'decisions_sha256':sha(O/'DECISIONS.txt'),'code_sha256':sha(Path(__file__))}
 (O/'ANALYSIS_LOCK.json').write_text(json.dumps(lock,indent=2));print('Frozen',lock['actual_utc_before_run']);raise SystemExit
lock=json.loads((O/'ANALYSIS_LOCK.json').read_text())
for k,p in paths.items():assert sha(R/p)==lock['files'][k]['sha256'],k+' changed'
assert sha(O/'DECISIONS.txt')==lock['decisions_sha256'];assert sha(Path(__file__))==lock['code_sha256']
started=now()

# Coverage diagnostic uses the original classifier exactly; it is not an approved mandate classification.
tree=ast.parse((R/paths['original_code']).read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='grupp')
env={'pd':pd,'re':re};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<original classifier>','exec'),env)
F=pd.read_csv(R/paths['lseg_raw'],low_memory=False).rename(columns={'Fund Name':'fond','Fund Type Description':'ftyp','Fund Shares Held (Adjusted)':'aktier','Fund Holdings Filing Date':'rapport','Fund Address Country':'land'})
F['rapport']=pd.to_datetime(F.rapport,errors='coerce');F['asofd']=pd.to_datetime(F['asof']);F['aktier']=pd.to_numeric(F.aktier,errors='coerce')
I=pd.read_csv(R/paths['original_events'],parse_dates=['AD','ED']);I=I[I.kind.eq('event')].copy()
F=F.merge(I[['event_id','AD','ED','review_cycle','type']],on='event_id',how='inner',validate='m:1')
F['old_group']=[env['grupp'](z)for z in F.itertuples()]
F['age_days']=(F.asofd-F.rapport).dt.days
F['old_keep']=F.age_days.le(120)&F.aktier.notna()
F['report_in_endpoint_window']=np.where(F.snap.eq('fore'),F.rapport.lt(F.AD),F.rapport.ge(F.ED))
bins=[2006,2011,2016,2021,2026];labels=['2007–2011','2012–2016','2017–2021','2022–2026']
I['period']=pd.cut(I.AD.dt.year,bins,labels=labels);F['period']=pd.cut(F.AD.dt.year,bins,labels=labels)
rd={name:np.sort(g.rapport.dropna().unique()) for name,g in F.groupby('fond')}
def reports(name,start,end):
 d=rd.get(name,np.array([],dtype='datetime64[ns]'));i=np.searchsorted(d,np.datetime64(start));return i<len(d)and d[i]<=np.datetime64(end)
coverage=[]
for z in I.itertuples():
 f=F[F.event_id.eq(z.event_id)];g=f[f.old_group.eq('OMXSB-index')&f.old_keep]
 k=set(g.fond.dropna());balanced=[n for n in k if reports(n,z.AD-pd.Timedelta(days=120),z.AD-pd.Timedelta(days=1))and reports(n,z.ED,z.ED+pd.Timedelta(days=45))]
 pre=set(g.loc[g.snap.eq('fore'),'fond']);post=set(g.loc[g.snap.eq('efter'),'fond'])
 coverage.append(dict(event_id=z.event_id,type=z.type,review_cycle=z.review_cycle,period=str(z.period),n_raw_rows=len(f),raw_funds=f.fond.nunique(),old_index_funds=len(k),
   old_cross_stock_reporting_funds=len(balanced),old_zero_no_group=len(g)==0,old_zero_no_eligible_fund=len(balanced)==0,
   inferred_missing_target_fund_endpoints=sum((n not in pre)+(n not in post)for n in balanced),
   median_report_age_before=f.loc[f.snap.eq('fore'),'age_days'].median(),median_report_age_after=f.loc[f.snap.eq('efter'),'age_days'].median(),
   stale_rows=int(f.age_days.gt(120).sum()),future_report_rows=int(f.age_days.lt(0).sum()),rows_failing_before_after_date=int((~f.report_in_endpoint_window).sum())))
C=pd.DataFrame(coverage);C.to_csv(O/'lseg_event_coverage.csv',index=False)
cs=C.groupby(['period','type'],observed=True).agg(N=('event_id','size'),G=('review_cycle','nunique'),median_raw_funds=('raw_funds','median'),median_old_index_funds=('old_index_funds','median'),median_reporting_index_funds=('old_cross_stock_reporting_funds','median'),no_group_made_zero=('old_zero_no_group','sum'),no_eligible_fund_made_zero=('old_zero_no_eligible_fund','sum'),inferred_target_zeros=('inferred_missing_target_fund_endpoints','sum'),median_before_age=('median_report_age_before','median'),median_after_age=('median_report_age_after','median')).reset_index()
cs.to_csv(O/'lseg_coverage_by_period.csv',index=False)
fr=F[F.old_group.eq('OMXSB-index')].groupby(['period','fond'],observed=True).agg(rows=('snap','size'),events=('event_id','nunique'),first_report=('rapport','min'),last_report=('rapport','max')).reset_index();fr.to_csv(O/'old_classifier_roster.csv',index=False)

# Metadata selection is repeated mechanically, before the new outcome aggregation.
P=pd.read_csv(R/paths['fi_panel']);E=pd.read_csv(R/paths['fi_events']);assert E.event_id.nunique()==216
roster=P.groupby('fund_id').agg(reviews=('review_cycle','nunique'),pairs=('event_id','size'),valid=('valid_for_market_acquisition_description','sum'),historically_classified=('new_documented_continuity','sum'),transitions=('benchmark_transition','sum'),mergers=('fund_merger','sum'))
ids=roster.index[(roster.reviews.eq(14))&(roster.pairs.eq(216))&(roster.valid.eq(216))&(roster.historically_classified.eq(216))&(roster.transitions.eq(0))&(roster.mergers.eq(0))].tolist();assert ids==[51482,60824]
roster['selected_fixed_description']=roster.index.isin(ids);roster.to_csv(O/'fund_selection_metadata.csv')
P=P[P.fund_id.isin(ids)].copy();assert not P.duplicated(['fund_id','event_id']).any()
assert P.before_report_instrument_rows.gt(0).all()and P.after_report_instrument_rows.gt(0).all()
assert P.measurement_status.eq('valid_position_pair').all(),P.measurement_status.unique()
assert P.stable_family.all()and (~P.benchmark_transition).all()and (~P.fund_merger).all()
P[['fund_id','review_cycle','before_fund_name','after_fund_name','before_fund_isin','after_fund_isin','before_benchmark','after_benchmark','new_evidence_class','new_strategy_continuity_assumption','new_source_ids']].drop_duplicates().to_csv(O/'fixed_fund_mandate_roster.csv',index=False)

# Verify quantity endpoints directly against previously extracted raw FI records (ordinary transferable securities).
raw=pd.read_csv(R/paths['fi_raw'],dtype={'Fond_institutnummer':str});raw['Antal']=pd.to_numeric(raw.Antal,errors='coerce')
raw=raw[raw['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')&raw.Fond_institutnummer.isin([str(x)for x in ids])]
checks=[];endpoints=[]
for z in P.itertuples():
 for ep in ['before','after']:
  dt=getattr(z,ep);q=getattr(z,ep+'_quantity');ii=getattr(z,'ISIN_'+ep);isb=[] if pd.isna(ii)or not str(ii) else str(ii).split(';')
  rows=raw[raw.Fond_institutnummer.eq(str(z.fund_id))&raw.Kvartalsslut.eq(dt)&raw['ISIN-kod_instrument'].isin(isb)]
  rawq=rows.Antal.sum(min_count=1)if len(rows)else 0.0
  zero=getattr(z,ep+'_logical_zero')
  ok=bool(np.isclose(q,rawq,rtol=1e-10,atol=1e-7)and(len(rows)>0 or zero))
  checks.append(dict(event_id=z.event_id,fund_id=z.fund_id,endpoint=ep,date=dt,accepted_isins=';'.join(isb),raw_rows=len(rows),raw_quantity=rawq,ledger_quantity=q,logical_zero=zero,verified=ok))
  endpoints.append(dict(fund_id=z.fund_id,ric=z.RIC,rapport=dt,FI_quantity=q))
Q=pd.DataFrame(checks);Q.to_csv(O/'raw_FI_endpoint_checks.csv',index=False);assert Q.verified.all(),Q.loc[~Q.verified].to_dict('records')[:5]
P['delta_q_recomputed']=P.after_quantity-P.factor*P.before_quantity
P['normalized_change_pp']=100*P.delta_q_recomputed*P.fi_price_after/P.company_mcap_after
assert np.allclose(P.delta_q_recomputed,P.delta_q);assert np.allclose(P.normalized_change_pp,P.delta_company_pp)

# Fixed-period same-row ratio of price to measured net position change, not an impact elasticity.
prices=pd.read_csv(R/paths['price'],usecols=['event_id','event_1','diff3_1','AD','ED','issuer'])
prices=prices.dropna(subset=['event_1','diff3_1']);shared=E[['event_id']].merge(prices,on='event_id',validate='1:1');assert len(shared)==205
P=P.merge(shared,on='event_id',validate='m:1');assert len(P)==410
P['fund_label']=P.fund_id.astype(str)
detail=P[['event_id','RIC','review_cycle','type','fund_id','fund_label','before','after','AD','ED','issuer','before_quantity','after_quantity','factor','delta_q_recomputed','normalized_change_pp','event_1','new_evidence_class']].copy()
both=detail.groupby(['event_id','RIC','review_cycle','type','before','after','AD','ED','issuer'],as_index=False).agg(normalized_change_pp=('normalized_change_pp','sum'),event_1=('event_1','first'),n_funds=('fund_id','nunique'));assert both.n_funds.eq(2).all()
both['fund_label']='fixed_two_fund_sum';detail['n_funds']=1
D=pd.concat([detail,both],ignore_index=True);D['direction']=np.where(D.type.eq('addition'),1,-1)
D['directional_demand_pp']=D.direction*D.normalized_change_pp;D['directional_price_pp']=D.direction*D.event_1
D['block']=np.where(D.review_cycle.str[:4].astype(int).le(2021),'2019–2021','2022–2025');D.to_csv(O/'same_sample_event_fund_panel.csv',index=False)
rv=D.groupby(['fund_label','type','review_cycle','block'],as_index=False).agg(N=('event_id','size'),demand_pp=('directional_demand_pp','mean'),price_pp=('directional_price_pp','mean'));rv.to_csv(O/'review_means.csv',index=False)
def mean_ci(x):
 x=np.asarray(x,float);n=len(x);se=x.std(ddof=1)/np.sqrt(n);q=t.ppf(.975,n-1);return dict(mean=x.mean(),se=se,lo=x.mean()-q*se,hi=x.mean()+q*se)
def fieller(y,x):
 y=np.asarray(y,float);x=np.asarray(x,float);G=len(x);v=np.cov(np.vstack([y,x]),ddof=1)/G;ym=y.mean();xm=x.mean();tc=t.ppf(.975,G-1)**2
 A=xm*xm-tc*v[1,1];B=-2*(xm*ym-tc*v[0,1]);C=ym*ym-tc*v[0,0];disc=B*B-4*A*C
 ans={'ratio':ym/xm if xm!=0 else np.nan,'fieller_A':A,'fieller_B':B,'fieller_C':C,'den_se':np.sqrt(v[1,1]),'cov_means':v[0,1],'ratio_lo':np.nan,'ratio_hi':np.nan}
 if np.isclose(A,0,rtol=0,atol=1e-15):
  if np.isclose(B,0,rtol=0,atol=1e-15):kind='all_real'if C<=0 else'empty'
  elif B>0:kind='left_halfline';ans['ratio_hi']=-C/B
  else:kind='right_halfline';ans['ratio_lo']=-C/B
 elif disc<0:kind='all_real'if A<0 else'empty'
 else:
  lo,hi=sorted([(-B-np.sqrt(disc))/(2*A),(-B+np.sqrt(disc))/(2*A)]);ans['ratio_lo']=lo;ans['ratio_hi']=hi;kind='bounded'if A>0 else'two_unbounded_rays'
 ans['fieller_type']=kind;return ans
results=[];contrasts=[]
for (fund,typ),g in rv.groupby(['fund_label','type']):
 for block,z in [('all2019–2025',g)]+list(g.groupby('block')):
  out=dict(fund_label=fund,type=typ,block=block,G=len(z),N=int(z.N.sum()),weighting='equal_review',benchmark='OMXSBGI',window='AD-1 to ED+1 inclusive')
  for var in ['demand_pp','price_pp']:out.update({var+'_'+k:v for k,v in mean_ci(z[var]).items()})
  out.update(fieller(z.price_pp,z.demand_pp));results.append(out)
 early=g[g.block.eq('2019–2021')];late=g[g.block.eq('2022–2025')]
 for var in ['demand_pp','price_pp']:
  n0,n1=len(early),len(late);v0=early[var].var(ddof=1)/n0;v1=late[var].var(ddof=1)/n1;se=np.sqrt(v0+v1);df=(v0+v1)**2/(v0*v0/(n0-1)+v1*v1/(n1-1));delta=late[var].mean()-early[var].mean();q=t.ppf(.975,df)
  contrasts.append(dict(fund_label=fund,type=typ,measure=var,later_minus_earlier=delta,se=se,df=df,lo=delta-q*se,hi=delta+q*se,early_reviews=n0,late_reviews=n1))
T=pd.DataFrame(results);T.to_csv(O/'fixed_fund_period_results.csv',index=False);pd.DataFrame(contrasts).to_csv(O/'later_minus_earlier_descriptive.csv',index=False)

# Narrow exact same named fund/security/report-date measurement check, no inferred correction series.
end=pd.DataFrame(endpoints);assert end.groupby(['fund_id','ric','rapport']).FI_quantity.nunique().max()==1;end=end.drop_duplicates(['fund_id','ric','rapport']);end.rapport=pd.to_datetime(end.rapport)
lf=F[F.fond.isin(['Storebrand Sverige','Swedbank Robur Access Sverige'])].copy();lf['fund_id']=lf.fond.map({'Storebrand Sverige':51482,'Swedbank Robur Access Sverige':60824})
lf=lf.dropna(subset=['aktier','rapport']);ls=lf.groupby(['fund_id','ric','rapport'],as_index=False).agg(lseg_adjusted=('aktier','first'),unique_quantities=('aktier','nunique'),raw_occurrences=('aktier','size'))
unit=end.merge(ls,on=['fund_id','ric','rapport'],validate='1:1');unit['ratio_adjusted_to_raw']=unit.lseg_adjusted/unit.FI_quantity.replace(0,np.nan);unit['unique_LSEG_quantity']=unit.unique_quantities.eq(1)
unit.to_csv(O/'LSEG_vs_FI_same_fund_date_units.csv',index=False)
unit_summary=unit[unit.FI_quantity.gt(0)&unit.unique_LSEG_quantity].groupby('fund_id').agg(N=('ric','size'),ratio_min=('ratio_adjusted_to_raw','min'),ratio_median=('ratio_adjusted_to_raw','median'),ratio_max=('ratio_adjusted_to_raw','max'));unit_summary.to_csv(O/'LSEG_FI_unit_summary.csv')
name_meta=F[F.fond.isin(['Storebrand Sverige','Swedbank Robur Access Sverige'])].groupby('fond').agg(parent_names=('Investor Parent name','nunique'),country_names=('land','nunique'),first_report=('rapport','min'),last_report=('rapport','max'));name_meta.to_csv(O/'LSEG_name_metadata_diagnostic.csv')
try:lseg_installed=importlib.util.find_spec('lseg')is not None
except ModuleNotFoundError:lseg_installed=False
meta={'started_utc':started,'finished_utc':now(),'exploratory':True,'fixed_fund_ids':ids,'all_FI_events':216,'same_sample_events':205,'review_count':14,'raw_endpoint_checks':len(Q),'all_raw_endpoints_match':bool(Q.verified.all()),'LSEG_installed_in_replay_runtime':lseg_installed,'local_authenticated_session_used':False,'LSEG_raw_rows':len(F),'LSEG_name_fund_mapping_is_not_identity_proof':True,'price_benchmark':'OMXSBGI','no_FTN':True,'lock_sha256':sha(O/'ANALYSIS_LOCK.json')}
(O/'RUN_METADATA.json').write_text(json.dumps(meta,indent=2));print(cs.to_string(index=False));print(T[['fund_label','type','block','N','G','demand_pp_mean','price_pp_mean','ratio','fieller_type','ratio_lo','ratio_hi']].to_string(index=False));print(unit_summary.to_string());print(json.dumps(meta,indent=2))
