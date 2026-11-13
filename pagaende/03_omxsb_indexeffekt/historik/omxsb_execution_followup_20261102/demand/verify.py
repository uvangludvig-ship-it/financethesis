"""Separate arithmetic implementation; does not import the analysis script."""
from pathlib import Path
import argparse,hashlib,json,datetime
import numpy as np,pandas as pd,statsmodels.api as sm
from scipy.stats import t
ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();R=Path(a.repo);O=Path(a.out)
p=pd.read_csv(R/'output/omxsb_followup_20261102/mandate_upgrade_20261102/classified_fund_event_panel.csv.gz');p=p[p.fund_id.isin([51482,60824])].copy()
p['q']=p.after_quantity-p.before_quantity*p.factor;p['d']=100*p.q*p.fi_price_after/p.company_mcap_after
prices=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',usecols=['event_id','event_1','diff3_1']);prices=prices.dropna(subset=['event_1','diff3_1']);p=p.merge(prices,on='event_id',validate='m:1');assert len(p)==410
saved=pd.read_csv(O/'same_sample_event_fund_panel.csv');r=pd.read_csv(O/'fixed_fund_period_results.csv');contr=pd.read_csv(O/'later_minus_earlier_descriptive.csv')
maxerr=0.;count=0;details=[]
for fund in ['51482','60824','fixed_two_fund_sum']:
 g=p if fund=='fixed_two_fund_sum'else p[p.fund_id.eq(int(fund))]
 ev=g.groupby(['event_id','type','review_cycle'],as_index=False).agg(x=('d','sum'),y=('event_1','first'))
 ev['sgn']=np.where(ev.type.eq('addition'),1,-1);ev.x*=ev.sgn;ev.y*=ev.sgn;ev['block']=np.where(ev.review_cycle.str[:4].astype(int).le(2021),'2019–2021','2022–2025')
 for typ in ['addition','deletion']:
  t_ev=ev[ev.type.eq(typ)];rv=t_ev.groupby(['review_cycle','block'])[['x','y']].mean().reset_index()
  for block in ['all2019–2025','2019–2021','2022–2025']:
   sub=rv if block.startswith('all')else rv[rv.block.eq(block)];s=r[(r.fund_label.astype(str)==fund)&r.type.eq(typ)&r.block.eq(block)].iloc[0];n=len(sub)
   for col,label in [('x','demand_pp'),('y','price_pp')]:
    fit=sm.OLS(sub[col].to_numpy(),np.ones((n,1))).fit();ci=fit.conf_int()[0]
    for key,v in [('mean',fit.params[0]),('se',fit.bse[0]),('lo',ci[0]),('hi',ci[1])]:maxerr=max(maxerr,abs(v-s[label+'_'+key]))
   xm,ym=sub.x.mean(),sub.y.mean();q=t.ppf(.975,n-1)**2
   sx=((sub.x-xm)**2).sum()/((n-1)*n);sy=((sub.y-ym)**2).sum()/((n-1)*n);c=((sub.x-xm)*(sub.y-ym)).sum()/((n-1)*n)
   A=xm*xm-q*sx;B=-2*xm*ym+2*q*c;C=ym*ym-q*sy
   for key,v in [('fieller_A',A),('fieller_B',B),('fieller_C',C),('cov_means',c),('ratio',ym/xm)]:maxerr=max(maxerr,abs(v-s[key]))
   # Independently classify quadratic sublevel set, including unbounded values.
   roots=np.roots([A,B,C]);real=bool(np.all(np.isreal(roots)))
   kind=('bounded'if A>0 else'two_unbounded_rays')if real else('empty'if A>0 else'all_real')
   assert kind==s.fieller_type
   if real:
    roots=np.sort(roots.real);maxerr=max(maxerr,abs(roots[0]-s.ratio_lo),abs(roots[1]-s.ratio_hi))
   if kind=='two_unbounded_rays':assert s.ratio<=s.ratio_lo or s.ratio>=s.ratio_hi
   details.append(dict(fund_label=fund,type=typ,block=block,N=len(t_ev)if block.startswith('all')else int(t_ev.block.eq(block).sum()),G=n,fieller_type=kind));count+=1
  early=rv[rv.block.eq('2019–2021')];late=rv[rv.block.eq('2022–2025')]
  for col,label in [('x','demand_pp'),('y','price_pp')]:
   z=contr[(contr.fund_label.astype(str)==fund)&contr.type.eq(typ)&contr.measure.eq(label)].iloc[0]
   delta=late[col].mean()-early[col].mean();v0=early[col].var(ddof=1)/len(early);v1=late[col].var(ddof=1)/len(late);se=np.sqrt(v0+v1);df=(v0+v1)**2/(v0*v0/(len(early)-1)+v1*v1/(len(late)-1));critical=t.ppf(.975,df)
   for key,v in [('later_minus_earlier',delta),('se',se),('df',df),('lo',delta-critical*se),('hi',delta+critical*se)]:maxerr=max(maxerr,abs(v-z[key]))
assert maxerr<1e-7,maxerr
assert saved.groupby('fund_label').event_id.nunique().eq(205).all()
q=pd.read_csv(O/'raw_FI_endpoint_checks.csv');assert len(q)==864 and q.verified.all()
report={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_cells':count,'max_absolute_numeric_error':maxerr,'all_passed':True,'raw_endpoint_checks':len(q),'fund_specific_and_sum_same_event_ids':True,'Fieller_unbounded_sets_preserved':True,'checks':details,'result_hashes':{f:hashlib.sha256((O/f).read_bytes()).hexdigest()for f in['fixed_fund_period_results.csv','review_means.csv','same_sample_event_fund_panel.csv','later_minus_earlier_descriptive.csv','ANALYSIS_LOCK.json']}}
(O/'independent_numeric_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k not in['checks','result_hashes']},indent=2))
