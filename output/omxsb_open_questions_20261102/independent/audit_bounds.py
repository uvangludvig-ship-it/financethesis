from pathlib import Path
import os
import os, sys, json, hashlib
import numpy as np, pandas as pd
from scipy.stats import t, nct
from scipy.optimize import brentq
OUT=Path(__file__).resolve().parent
REPO=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
CC=REPO/'code/claude_checks'
# Imported modules read inputs only. Prevent bytecode writes to read-only repository.
sys.dont_write_bytecode=True
os.chdir(CC); sys.path.insert(0,str(CC))
import twin_core as tc
# Reuse only the original definitions before its event iteration; no file-writing statements executed.
src=(CC/'ab_revision.py').read_text().split('rows = []; pools = {}')[0]
ns={}; exec(compile(src,str(CC/'ab_revision.py'),'exec'),ns)
D=pd.read_csv(CC/'ab_revision_events.csv')
fin=pd.read_csv(CC/'twin_results_events.csv',parse_dates=['AD','ED'])
E=D[(D.status=='ok')&(D.n_placebo>=20)].merge(fin.drop(columns=['firm','type']),on='event_id',validate='one_to_one')
legs=[]
for e in E.itertuples():
 a,b=int(e.iAD)-1,int(e.iED)+1
 A,B,source=ns['series'](e.event_key,e.sister_ric)
 m=100*np.log((1+tc.mkt.iloc[a:b+1]/100).prod())
 ai=float(e.sign*(100*np.log(A.iloc[b]/A.iloc[a-1])-m))
 bi=float(e.sign*(100*np.log(B.iloc[b]/B.iloc[a-1])-m))
 legs.append({'event_id':e.event_id,'index_leg_consistent':ai,'sister_leg_consistent':bi,'spread_consistent':ai-bi,'source_consistent':source})
E=E.merge(pd.DataFrame(legs),on='event_id',validate='one_to_one')
assert np.allclose(E.spread,E.spread_consistent,atol=1e-8)
E['review']=E.event_id.str.rsplit('-',n=1).str[0]
E['old_index_leg']=E['primär [AD-1,ED+1] indexslag']
E['old_sister_leg']=E['primär [AD-1,ED+1] systerslag']
E['outside']=~E.sister_member_before & ~E.sister_member_after
E.to_csv(OUT/'ab_joint_event_ledger.csv',index=False)

def fieller(m,v,crit):
 # ratio mu_spread / mu_index: accept |S-rI| <= crit*se(S-rI)
 s,i=m[0],m[1]; a=i*i-crit*crit*v[1,1]; b=-2*(s*i-crit*crit*v[0,1]); c=s*s-crit*crit*v[0,0]
 dis=b*b-4*a*c
 if dis<0:
  return dict(kind='all_real' if a<0 else 'empty',lower=None,upper=None,A=a,discriminant=dis)
 r=sorted([(-b-np.sqrt(dis))/(2*a),(-b+np.sqrt(dis))/(2*a)])
 return dict(kind='bounded' if a>0 else 'two_unbounded_rays',lower=float(r[0]),upper=float(r[1]),A=float(a),discriminant=float(dis))
results=[]
for label,sub in [('all_clean39',E),('outside18',E[E.outside]),('outside_from2017_9',E[E.outside&(E.AD>='2017-01-01')])]:
 Y=sub[['spread_consistent','index_leg_consistent','sister_leg_consistent']].to_numpy(); m=Y.mean(0); n=len(Y)
 for cluster in ['firm','review']:
  labels=pd.factorize(sub[cluster])[0]; g=labels.max()+1
  scores=np.array([(Y-m)[labels==k].sum(0) for k in range(g)])
  cov=(scores.T@scores)*g/(g-1)/n**2
  crit=t.ppf(.975,g-1); se=np.sqrt(cov.diagonal()); ci=np.column_stack([m-crit*se,m+crit*se])
  f=fieller(m,cov,crit)
  results.append(dict(sample=label,cluster=cluster,N=n,G=int(g),spread_mean=m[0],index_mean=m[1],sister_mean=m[2],ratio=m[0]/m[1],spread_se=se[0],index_se=se[1],sister_se=se[2],spread_lo=ci[0,0],spread_hi=ci[0,1],index_lo=ci[1,0],index_hi=ci[1,1],sister_lo=ci[2,0],sister_hi=ci[2,1],spread_index_cov=cov[0,1],ratio_set=f['kind'],ratio_lower=f['lower'],ratio_upper=f['upper'],old_index_mean=sub.old_index_leg.mean(),old_sister_mean=sub.old_sister_leg.mean(),changed_index_legs=int((abs(sub.index_leg_consistent-sub.old_index_leg)>1e-8).sum())))
R=pd.DataFrame(results); R.to_csv(OUT/'ab_joint_uncertainty.csv',index=False)
print(R.to_string(index=False))
# Verify published MDE arithmetics and numerical noncentral-t power, without opening coefficient estimates.
s4=json.loads((CC/'runda4_resultat/steg1.json').read_text())
s5=json.loads((CC/'runda5_resultat/steg1.json').read_text())
rows=[]
for lab,g,se,reported,threshold in [('T14_H',15,s4['E_H']['se'],s4['E_H']['mde'],.5*s4['E_BH']['b']),('T14_D',15,s4['E_D']['se'],s4['E_D']['mde'],s4['E_BH']['b']),('T16',7,None,s5['T16']['mde'],1.5),('T17',19,None,s5['T17']['mde'],.92)]:
 # T16 G is not stored in steg1; derive from exact saved classified input and valid regression sample.
 if lab=='T16':
  cls=pd.read_csv(CC/'runda5_resultat/T16_klassning.csv')
  s5e=pd.read_csv(CC/'runda2_resultat/T5urval_T7_T8b_events.csv')
  q=cls[cls.grupp.isin(['utanför','inom'])].merge(s5e[s5e.event==1],on=['review','ric'])
  q=q.dropna(subset=['ru','lm','car_ED+1']); g=q.review.nunique()
 fac=t.ppf(.975,g-1)+t.ppf(.80,g-1)
 if se is None: se=reported/fac
 crit=t.ppf(.975,g-1)
 power=lambda nc:nct.cdf(-crit,g-1,nc)+nct.sf(crit,g-1,nc)
 nc=brentq(lambda x:power(x)-.8,.01,5)
 rows.append(dict(test=lab,G=g,SE=se,MDE_reported=reported,MDE_formula=fac*se,MDE_noncentral_t=nc*se,threshold=threshold,pass_published=reported<=threshold,pass_noncentral_t=nc*se<=threshold))
M=pd.DataFrame(rows); M.to_csv(OUT/'mde_check.csv',index=False); print('\nMDE\n',M.to_string(index=False))
(OUT/'input_provenance.json').write_text(json.dumps({str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [CC/'ab_revision.py',CC/'ab_revision_events.csv',CC/'twin_results_events.csv',CC/'runda4.py',CC/'runda4_resultat/steg1.json',CC/'runda5_t15.py',CC/'runda5_t16_t17.py',CC/'runda5_resultat/steg1.json']},indent=2))
