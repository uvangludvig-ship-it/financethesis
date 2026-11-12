"""Exploratory timing repair of an inherited comparison regression.
Only remove AD-1 from the pre-return control, preserving samples, outcomes,
fixed effects, size control, and exclusion rules. All variants are retained.
Outputs are aggregate or validation metadata, never raw security observations.
"""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster

ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);ap.add_argument('--draws',type=int,default=49999);a=ap.parse_args();src=a.source;out=a.out;out.mkdir(exist_ok=True,parents=True)
data=src/'data'
S=pd.read_csv(data/'events/additions_and_near_additions_2007_2026.csv',parse_dates=['AD'])
idx=pd.read_csv(data/'prices/index_levels_daily_2004_2026.csv',parse_dates=['date'])
m=idx[(idx.ric=='.OMXSBGI')&idx.close.notna()].sort_values('date').drop_duplicates('date');cal=pd.DatetimeIndex(m.date);market=m.set_index('date').close.pct_change(fill_method=None)*100;pos=pd.Series(np.arange(len(cal)),index=cal)
assert np.array_equal(S.AD.map(pos).values,S.iA.values),'calendar mismatch'
rics=set(S.ric)
parts=[]
for name in ['all_stocks_daily_2004_2012.csv.gz','all_stocks_daily_2013_2019.csv.gz','all_stocks_daily_2020_2026.csv.gz']:
    p=pd.read_csv(data/'prices'/name,usecols=['ric','date','close','totret'],parse_dates=['date']);parts.append(p[p.ric.isin(rics)&p.date.isin(cal)])
p=pd.concat(parts,ignore_index=True)
# Match the inherited full-panel return treatment for Nordea and Tieto.
n=pd.read_csv(data/'prices/nordea_tieto_daily_lseg.csv',low_memory=False)
for ric in ['NDASE.ST','TIETOS.ST']:
    d=n[(n.ric==ric)&n.Date.notna()&n.TRDPRC_1.notna()].copy()
    extra=pd.DataFrame({'ric':ric,'date':pd.to_datetime(d.Date),'close':d.TRDPRC_1,'totret':np.nan})
    p=pd.concat([p[p.ric!=ric],extra[extra.date.isin(cal)]],ignore_index=True)
p=p.drop_duplicates(['ric','date'],keep='last').sort_values(['ric','date'])
ret={};changed_ffill=0
for ric,g in p.groupby('ric'):
    g=g.set_index('date');fallback=g.close.ffill().pct_change(fill_method=None)*100
    r=g.totret.fillna(fallback).reindex(cal);r=r.mask(r>1000)
    ret[ric]=(r-market).to_numpy()
checks=[]
def check(name,passed,detail):checks.append({'check':name,'passed':bool(passed),'detail':str(detail)})
def ar(ric,start,end):
    if ric not in ret or start<0 or end>=len(cal):return np.nan
    z=ret[ric][int(start):int(end)+1]
    return z.sum() if np.isfinite(z).all() else np.nan
S['rebuild_ru']=[ar(r,ia-100,ia-1) for r,ia in zip(S.ric,S.iA)]
S['rebuild_outcome']=[ar(r,ia-1,ie+1) for r,ia,ie in zip(S.ric,S.iA,S.iE)]
S['repair_ru']=[ar(r,ia-100,ia-2) for r,ia in zip(S.ric,S.iA)]
S['ar_adminus1']=[ar(r,ia-1,ia-1) for r,ia in zip(S.ric,S.iA)]
for key,old in [('rebuild_ru','ru'),('rebuild_outcome','car_ED+1')]:
    ok=np.isclose(S[key],S[old],atol=1e-7,rtol=1e-7,equal_nan=True)
    check(key,ok.all(),f'{ok.sum()}/{len(S)} rows; max absolute difference {np.nanmax(abs(S[key]-S[old]))}')
check('repair is removal of one overlapping day',np.allclose(S.repair_ru+S.ar_adminus1,S.rebuild_ru,atol=1e-9,rtol=1e-9,equal_nan=True),'AD-1 removed; remaining control has 99 daily returns')
if not all(x['passed'] for x in checks):
    pd.DataFrame(checks).to_csv(out/'comparison_repair_validation.csv',index=False)
    raise RuntimeError('Reconstruction did not match; inspect rather than silently change model')
flags=pd.read_csv(data/'events/omxsb_deletion_flags_2007_2026.csv')
ev=pd.read_csv(data/'events/omxsb_changes_with_car_2007_2026.csv')
excluded=set(flags.loc[flags.flag_offer.astype(bool)|flags.flag_delist.astype(bool),'event_id'])
pairs=set(zip(ev[ev.event_id.isin(excluded)].review_cycle,ev[ev.event_id.isin(excluded)].RIC))
S['excluded']=[(r,c) in pairs and e==1 and t=='deletion' for r,c,e,t in zip(S.review,S.ric,S.event,S.type)]
old_results=pd.read_csv(src/'results/near_additions/near_additions_results.csv')

def fit(s,control,label):
    X=np.column_stack([s.event.to_numpy(float),s[control].to_numpy(float),s.lm.to_numpy(float),pd.get_dummies(s.review).to_numpy(float)])
    y=s['car_ED+1'].to_numpy(float)
    ok=np.isfinite(y)&np.isfinite(X).all(1);X=X[ok];y=y[ok];gr=s.review.to_numpy()[ok]
    keep=X.std(0)>0;keep[0]=True;X=X[:,keep]
    codes,uniq=pd.factorize(gr);G=len(uniq);n,k=X.shape
    pinv=np.linalg.pinv(X);inv=pinv@pinv.T;bh=pinv@y;e=y-X@bh
    c=np.zeros(k);c[0]=1;q=pinv.T@c
    adj=G/(G-1)*(n-1)/(n-k)
    scores=np.bincount(codes,weights=e*q,minlength=G);se=np.sqrt(adj*(scores**2).sum());coef=bh[0];crit=stats.t.ppf(.975,G-1)
    ref=sm.OLS(y,X).fit();refse=np.sqrt(cov_cluster(ref,codes)[0,0])
    check(label+' OLS coefficient',abs(coef-ref.params[0])<1e-10,coef)
    check(label+' CR1 standard error',abs(se-refse)<1e-9,se)
    # Restricted bootstrap of H0: coefficient on event == 0, compressed at review level.
    br=bh-(inv@c)*(c@bh)/(c@inv@c);fr=X@br;er=y-fr
    sx=np.zeros((G,k));cx=np.zeros((G,k));ag=np.zeros(G)
    np.add.at(sx,codes,X*er[:,None]);np.add.at(cx,codes,X*q[:,None]);np.add.at(ag,codes,er*q)
    rng=np.random.default_rng(20261112)
    atoms=np.array([-1.,1.]) if G>=12 else np.array([-np.sqrt(1.5),-1.,-np.sqrt(.5),np.sqrt(.5),1.,np.sqrt(1.5)])
    W=rng.choice(atoms,size=(a.draws,G));db=W@sx@inv
    bs=db@c;sg=W*ag-db@cx.T;ss=np.sqrt(adj*np.sum(sg**2,axis=1));ts=bs/ss
    pw=(1+np.count_nonzero(abs(ts)>=abs(coef/se)-1e-12))/(a.draws+1)
    for j in range(min(5,a.draws)):
        yb=fr+er*W[j,codes];frb=sm.OLS(yb,X).fit();seb=np.sqrt(cov_cluster(frb,codes)[0,0])
        check(label+f' bootstrap draw {j} coefficient',abs(frb.params[0]-bs[j])<1e-8,bs[j])
        check(label+f' bootstrap draw {j} SE',abs(seb-ss[j])<1e-8,ss[j])
    return dict(estimate=coef,se_cr1=se,lower95_cr1=coef-crit*se,upper95_cr1=coef+crit*se,p_cr1=2*stats.t.sf(abs(coef/se),G-1),p_wcr=pw,draws=a.draws,n=n,events=int(X[:,0].sum()),comparators=int((X[:,0]==0).sum()),reviews=G)
rows=[]
for ty,groups in [('addition',['all']),('deletion',['exclude_flagged','all'])]:
    for group in groups:
        for post in [0,1]:
            s=S[(S.type==ty)&(S.post==post)].copy()
            if group=='exclude_flagged':s=s[~s.excluded]
            for variant in ['all_comparators','main_market_comparators']:
                q=s if variant=='all_comparators' else s[(s.event==1)|(s.mic=='XSTO')]
                for control in ['ru','repair_ru']:
                    tag=f'{ty}/{group}/{post}/{variant}/{control}'
                    r=fit(q,control,tag);rows.append(dict(type=ty,sample=group,period='2017-2026' if post else '2007-2016',variant=variant,control_window='AD-100 to AD-1' if control=='ru' else 'AD-100 to AD-2',**r))
                    if control=='ru':
                        old=old_results[(old_results.typ==ty)&(old_results.urval==('utan de 10 (G&S regel)' if group=='exclude_flagged' else 'alla'))&(old_results.period==('efter' if post else 'före'))&(old_results.variant==('CAR [AD-1,ED+1] mot nästan' if variant=='all_comparators' else 'känslighet: bara huvudlistan (XSTO) bland nästan'))].iloc[0]
                        check(tag+' frozen coefficient',abs(r['estimate']-old.b)<1e-8,r['estimate']-old.b)
                        check(tag+' frozen standard error',abs(r['se_cr1']-old.se)<1e-8,r['se_cr1']-old.se)
                        check(tag+' frozen counts',r['n']==old.n and r['events']==old.handelser and r['comparators']==old.nastan and r['reviews']==old.G,f"{r['n']}/{r['events']}/{r['comparators']}/{r['reviews']}")
R=pd.DataFrame(rows);R.to_csv(out/'comparison_repair_results.csv',index=False)
C=pd.DataFrame(checks);C.to_csv(out/'comparison_repair_validation.csv',index=False)
(out/'comparison_repair_metadata.json').write_text(json.dumps({'source_commit':'d2d41666ed213e4cc1f6cb382313f59c29e87ea0','change':'Remove AD-1 only from pre-return control; preserve outcomes, sample rules, fixed effects and size control.','status':'Exploratory correction after inherited results were known. Not a new causal design.','interval':'Analytical CR1 t(G-1); not inversion of WCR test.','bootstrap':'Restricted wild null bootstrap, review clusters, Rademacher if G>=12, Webb otherwise, finite simulation correction (k+1)/(B+1).','draws':a.draws,'checks':len(C),'passed':int(C.passed.sum()),'input_rows':len(S),'daily_reconstruction_max_error':float(max(abs(S.rebuild_ru-S.ru).max(),abs(S.rebuild_outcome-S['car_ED+1']).max()))},indent=2))
assert C.passed.all()
print(R.to_string(index=False));print(f'{len(C)} checks passed.')
