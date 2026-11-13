"""Exploratory matched-cohort accounting for a changing event-window length.
Written after the fixed-window estimates and timing metadata were inspected.
Preserves both event types, every four-period cell, and first-to-last contrasts.
The fixed seven-return window is AD-1..AD+5; the nonoverlapping remainder is
AD+6..ED+1. Neither component identifies a causal timing effect.
"""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);ap.add_argument('--reference',type=Path);ap.add_argument('--draws',type=int,default=49999);a=ap.parse_args();src=a.source;out=a.out;out.mkdir(parents=True,exist_ok=True)
ix=pd.read_csv(src/'data/prices/index_levels_daily_2004_2026.csv',parse_dates=['date']);m=ix[(ix.ric=='.OMXSBGI')&ix.close.notna()].sort_values('date').set_index('date').close
assert not m.index.duplicated().any();cal=m.index;pos=pd.Series(np.arange(len(cal)),index=cal);market=m.pct_change(fill_method=None)*100
p=pd.read_csv(src/'data/prices/stock_prices_daily_2004_2026.csv.gz',parse_dates=['date']);p=p[p.date.isin(cal)].sort_values(['ric','date']);assert not p.duplicated(['ric','date']).any()
AR={}
for ric,g in p.groupby('ric'):
 g=g.set_index('date');r=g.totret.fillna(g.close.ffill().pct_change(fill_method=None)*100);AR[ric]=(r.reindex(cal)-market).to_numpy()
def car(ric,l,h):
 z=AR[ric][int(l):int(h)+1];return float(z.sum()) if len(z)==h-l+1 and np.isfinite(z).all() else np.nan
E=pd.read_csv(src/'data/events/omxsb_changes_with_car_2007_2026.csv',parse_dates=['AD','ED','effective_date']);fl=pd.read_csv(src/'data/events/omxsb_deletion_flags_2007_2026.csv');assert str(fl.flag_offer.dtype)=='bool' and str(fl.flag_delist.dtype)=='bool'
E=E[~E.event_id.isin(fl.loc[fl.flag_offer|fl.flag_delist,'event_id'])].copy();E['a']=E.AD.map(pos);E['b']=E.ED.map(pos);assert (E.b-E.a).min()>=6
for col,l,h in [('whole',-1,None),('first_seven',-1,5),('remainder',6,None)]:
 E[col]=[car(r,aa+l,bb+1 if h is None else aa+h) for r,aa,bb in zip(E.RIC,E.a,E.b)]
checks=[]
def check(name,passed,detail):checks.append(dict(check=name,passed=bool(passed),detail=str(detail)))
check('whole matches frozen CAR',np.allclose(E.whole,E.tot,atol=1e-8,equal_nan=True),len(E))
D=E.dropna(subset=['whole','first_seven','remainder']).copy();check('primary sample retained',len(D)==E.tot.notna().sum(),len(D))
check('event-level decomposition',np.allclose(D.whole,D.first_seven+D.remainder,atol=1e-10),np.max(abs(D.whole-D.first_seven-D.remainder)))

def estimate(X,y,g,c,label):
 X=np.asarray(X,float);y=np.asarray(y,float);c=np.asarray(c,float);codes,uniq=pd.factorize(g);G=len(uniq);n,k=X.shape
 pinv=np.linalg.pinv(X);inv=pinv@pinv.T;bh=pinv@y;e=y-X@bh;q=pinv.T@c;adj=G/(G-1)*(n-1)/(n-k);scores=np.bincount(codes,weights=e*q,minlength=G);coef=float(c@bh);se=np.sqrt(adj*(scores**2).sum());crit=stats.t.ppf(.975,G-1)
 ref=sm.OLS(y,X).fit();refse=float(np.sqrt(c@cov_cluster(ref,codes)@c));check(label+' OLS',abs(c@ref.params-coef)<1e-10,coef);check(label+' CR1',abs(se-refse)<1e-9,se)
 br=bh-(inv@c)*(c@bh)/(c@inv@c);fr=X@br;er=y-fr;sx=np.zeros((G,k));cx=np.zeros((G,k));ag=np.zeros(G)
 np.add.at(sx,codes,X*er[:,None]);np.add.at(cx,codes,X*q[:,None]);np.add.at(ag,codes,er*q)
 atoms=np.array([-1.,1.]) if G>=12 else np.array([-np.sqrt(1.5),-1.,-np.sqrt(.5),np.sqrt(.5),1.,np.sqrt(1.5)])
 W=np.random.default_rng(20261112).choice(atoms,size=(a.draws,G));db=W@sx@inv;bs=db@c;sg=W*ag-db@cx.T;ss=np.sqrt(adj*np.sum(sg**2,axis=1));pw=(1+np.count_nonzero(abs(bs/ss)>=abs(coef/se)-1e-12))/(a.draws+1)
 for j in range(3):
  yb=fr+er*W[j,codes];z=sm.OLS(yb,X).fit();seb=np.sqrt(c@cov_cluster(z,codes)@c)
  check(label+f' pseudo OLS {j}',abs(c@z.params-bs[j])<1e-9,bs[j]);check(label+f' pseudo CR1 {j}',abs(seb-ss[j])<1e-9,ss[j])
 return dict(n=n,reviews=G,estimate=coef,se_cr1=se,lower95_cr1=coef-crit*se,upper95_cr1=coef+crit*se,p_cr1=2*stats.t.sf(abs(coef/se),G-1),p_wcr=pw,draws=a.draws)
periods=['2007–2011','2012–2016','2017–2021','2022–2026'];rows=[]
for ty in ['addition','deletion']:
 s=D[D.type==ty].copy()
 groups=[('All',s)]+[(per.replace('–','-'),s[s.period==per]) for per in periods]+[('2007-2016',s[s.effective_date.dt.year<=2016]),('2017-2026',s[s.effective_date.dt.year>=2017])]
 for per,g in groups:
  for col in ['whole','first_seven','remainder']:
   r=estimate(np.ones((len(g),1)),g[col],g.review_cycle,[1.],f'{ty}/{per}/{col}');rows.append(dict(type=ty,period=per,measure=col,statistic='mean',**r))
 X=np.column_stack([(s.period==per).astype(float) for per in periods])
 for col in ['whole','first_seven','remainder']:
  r=estimate(X,s[col],s.review_cycle,[-1.,0.,0.,1.],f'{ty}/latest_minus_earliest/{col}');rows.append(dict(type=ty,period='2022-2026 minus 2007-2011',measure=col,statistic='contrast',**r))
R=pd.DataFrame(rows)
for ty in ['addition','deletion']:
 z=R[(R.type==ty)&(R.statistic=='contrast')].set_index('measure').estimate;check(ty+' contrast decomposition',abs(z.whole-z.first_seven-z.remainder)<1e-9,z.to_dict())
if a.reference:
 ref=pd.read_csv(a.reference)
 for rr in ref.itertuples():
  z=R[(R.type==rr.type)&(R.period==rr.period)&(R.measure==('whole' if rr.measure=='arithmetic' else 'first_seven'))&(R.statistic=='mean')].iloc[0]
  check(f'parent fixed-window result {rr.type}/{rr.period}/{rr.measure}',z.n==rr.n and z.reviews==rr.G and abs(z.estimate-rr.mean)<1e-9 and abs(z.se_cr1-rr.se)<1e-9,'Counts, mean and SE agree')
old=pd.read_csv(src/'results/effect/tabell1_lang.csv')
for ty in ['addition','deletion']:
 o=old[(old.panel=='D')&(old.typ==ty)&(old.urval=='2022–26 minus 2007–11')].iloc[0];z=R[(R.type==ty)&(R.measure=='whole')&(R.statistic=='contrast')].iloc[0]
 check(ty+' frozen period contrast',abs(z.estimate-o.b)<1e-9 and abs(z.se_cr1-o.se)<1e-9,'Same all-four-period regression and contrast; new seed/draw count only for p-value')
R.to_csv(out/'fixed_window_decomposition.csv',index=False);C=pd.DataFrame(checks);C.to_csv(out/'fixed_window_decomposition_validation.csv',index=False)
meta={'status':'Exploratory follow-up after the first fixed-window outcomes were inspected; all types/periods/components retained.','definition':'whole AD-1..ED+1 = first_seven AD-1..AD+5 + remainder AD+6..ED+1; identical primary complete events.','contrasts':'OLS four period dummies on all complete events; c=(-1,0,0,1), review clustered.','inference':'CR1 t(G-1) intervals and separate restricted wild null bootstrap p-values; 49999 draws; finite simulation correction; intervals are not WCR inversions.','checks':len(C),'passed':int(C.passed.sum()),'source_commit':'d2d41666ed213e4cc1f6cb382313f59c29e87ea0'}
(out/'fixed_window_decomposition_metadata.json').write_text(json.dumps(meta,indent=2));assert C.passed.all();print(R[R.statistic=='contrast'].to_string(index=False));print(R[(R.type=='addition')&(R.period.isin([p.replace('–','-') for p in periods]))].to_string(index=False));print(meta)
