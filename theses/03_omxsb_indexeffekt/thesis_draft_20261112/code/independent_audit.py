"""Independent arithmetic and inferential audit. No licensed event data are exported.

Usage: python independent_audit.py /path/to/frozen/thesis_final /path/to/audit/output
This implementation does not import the inherited return or inference functions.
"""
from pathlib import Path
import sys, json, hashlib, platform, importlib.metadata
import numpy as np
import pandas as pd
from scipy import stats

SRC=Path(sys.argv[1]).resolve(); OUT=Path(sys.argv[2]).resolve(); OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name, passed, detail):
    checks.append({'check':name,'passed':bool(passed),'detail':detail})

def covariance_mean(y,g):
    y=np.asarray(y,float)
    if y.ndim==1: y=y[:,None]
    codes=pd.factorize(g)[0]; G=codes.max()+1; n=len(y)
    scores=np.zeros((G,y.shape[1])); np.add.at(scores,codes,y-y.mean(0))
    return (scores.T@scores)*G/(G-1)/n**2

def mean_inference(d,col):
    q=d.dropna(subset=[col]); y=q[col].to_numpy(); n=len(y); G=q.review_cycle.nunique()
    b=y.mean(); se=float(np.sqrt(covariance_mean(y,q.review_cycle)[0,0])); crit=stats.t.ppf(.975,G-1)
    loo=np.array([q.loc[q.review_cycle!=c,col].mean() for c in q.review_cycle.unique()])
    sj=np.sqrt((G-1)/G*np.sum((loo-b)**2))
    out=dict(n=n,G=G,b=b,se=se,lo=b-crit*se,hi=b+crit*se,p=2*stats.t.sf(abs(b/se),G-1),
        equal_review=q.groupby('review_cycle')[col].mean().mean(),loo_min=loo.min(),loo_max=loo.max(),
        jackknife_se=sj,jackknife_p=2*stats.t.sf(abs(b/sj),G-1),max_review_weight=q.groupby('review_cycle').size().max()/n)
    if 'RIC' in q:
        J=q.RIC.nunique(); pairs=q.review_cycle.astype(str)+'|'+q.RIC.astype(str)
        v=covariance_mean(y,q.review_cycle)[0,0]+covariance_mean(y,q.RIC)[0,0]-covariance_mean(y,pairs)[0,0]
        out.update(se_two_way=np.sqrt(v) if v>0 else np.nan, securities=J)
        if v>0:
            c=stats.t.ppf(.975,min(G,J)-1);out.update(lo_two_way=b-c*np.sqrt(v),hi_two_way=b+c*np.sqrt(v),p_two_way=2*stats.t.sf(abs(b/np.sqrt(v)),min(G,J)-1))
    return out

def holm(p):
    p=np.asarray(p); order=np.argsort(p); z=np.empty(len(p));z[order]=np.minimum(1,np.maximum.accumulate((len(p)-np.arange(len(p)))*p[order]));return z

def wcr_mean(y,g,B=49999,seed=20261112):
    y=np.asarray(y,float); codes=pd.factorize(g)[0]; G=codes.max()+1;n=len(y)
    totals=np.bincount(codes,weights=y); sizes=np.bincount(codes);b=y.mean()
    se=np.sqrt(G/(G-1)*np.sum((totals-sizes*b)**2)/n**2)
    support=np.array([-1.,1.]) if G>=12 else np.array([-np.sqrt(1.5),-1.,-np.sqrt(.5),np.sqrt(.5),1.,np.sqrt(1.5)])
    w=np.random.default_rng(seed).choice(support,size=(B,G));ys=w*totals
    bs=ys.sum(1)/n;ss=np.sqrt(G/(G-1)*((ys-bs[:,None]*sizes)**2).sum(1)/n**2)
    return (1+np.sum(np.abs(bs/ss)>=abs(b/se)))/(B+1)

idx=pd.read_csv(SRC/'data/prices/index_levels_daily_2004_2026.csv',parse_dates=['date'])
ix=idx.loc[(idx.ric=='.OMXSBGI')&idx.close.notna()].sort_values('date').set_index('date').close
cal=ix.index; market=100*(ix/ix.shift(1)-1); position={d:i for i,d in enumerate(cal)}
px=pd.read_csv(SRC/'data/prices/stock_prices_daily_2004_2026.csv.gz',parse_dates=['date'])
px=px[px.date.isin(cal)].sort_values(['ric','date'])
check('unique stock daily keys',not px.duplicated(['ric','date']).any(),int(px.duplicated(['ric','date']).sum()))
returns={}; fallback={}; strict={}
for ric,g in px.groupby('ric'):
    g=g.set_index('date'); previous=g.close.ffill().shift(1)
    r=g.totret.where(g.totret.notna(),100*(g.close.ffill()/previous-1))
    returns[ric]=r.reindex(cal).to_numpy()-market.to_numpy()
    strict[ric]=(g.totret.where(g.totret.notna(),100*(g.close/g.close.shift(1)-1)).reindex(cal)-market).to_numpy()
    fallback[ric]=(g.totret.isna()&r.notna()).reindex(cal,fill_value=False).to_numpy()
def car(ric,a,b,arrays=returns):
    if ric not in arrays or a<0 or b>=len(cal) or b<a: return np.nan
    s=arrays[ric][a:b+1]
    return float(s.sum()) if np.isfinite(s).all() else np.nan

e=pd.read_csv(SRC/'data/events/omxsb_changes_with_car_2007_2026.csv',parse_dates=['AD','ED','effective_date'])
fl=pd.read_csv(SRC/'data/events/omxsb_deletion_flags_2007_2026.csv')
check('deletion flags are boolean',str(fl.flag_offer.dtype)=='bool' and str(fl.flag_delist.dtype)=='bool',str(fl[['flag_offer','flag_delist']].dtypes.to_dict()))
excluded=set(fl.loc[fl.flag_offer|fl.flag_delist,'event_id'])
for c in ['ann','eff','tot']: e['original_'+c]=e[c]
fallback_events=0;fallback_observations=0;strict_changes=0
for j,r in e.iterrows():
    a=position[r.AD]; b=position[r.ED]
    for c,l,h in [('ann',a-1,a+1),('eff',b-1,b+1),('tot',a-1,b+1),('pre_ed',a-1,b-1),('post20',b,b+20),('cumulative20',a-1,b+20)]:
        e.loc[j,c]=car(r.RIC,l,h)
    nf=int(fallback[r.RIC][a-1:b+2].sum());fallback_events+=nf>0;fallback_observations+=nf
    st=car(r.RIC,a-1,b+1,strict)
    strict_changes+=not (np.isclose(st,e.loc[j,'tot'],atol=1e-10,equal_nan=True))
for c in ['ann','eff','tot']:
    v=e[[c,'original_'+c]];err=(v[c]-v['original_'+c]).abs().max()
    check('independent '+c+' reconstruction',np.allclose(v[c],v['original_'+c],atol=1e-8,equal_nan=True),{'max_abs_error':float(err),'events':len(v)})
e=e[~e.event_id.isin(excluded)].copy()
raw=pd.read_csv(SRC/'data/events/omxsb_changes_nasdaq_2007_2026.csv',parse_dates=['effective_date'])
flow=[]
for ty in ['addition','deletion']:
    for label,d in [('source list',raw),('imported return candidates',pd.read_csv(SRC/'data/events/omxsb_changes_with_car_2007_2026.csv')),('after exclusions',e),('complete main CAR',e[e.tot.notna()])]:
        q=d[d.type==ty];flow.append(dict(type=ty,stage=label,n=len(q),reviews=q.review_cycle.nunique()))
pd.DataFrame(flow).to_csv(OUT/'sample_flow.csv',index=False)
check('no future source effective dates',raw.effective_date.max()<=pd.Timestamp('2026-11-12'),str(raw.effective_date.max().date()))

base=pd.read_csv(SRC/'results/effect/tabell1_lang.csv');sens=[];paired=[]
for ty in ['addition','deletion']:
    q=e[e.type==ty]
    for label, d in [('all',q),('2007-2016',q[q.effective_date.dt.year<=2016]),('2017-2026',q[q.effective_date.dt.year>=2017])]+[(p,q[q.period==p]) for p in sorted(q.period.unique())]:
        r=mean_inference(d,'tot');sens.append(dict(type=ty,period=label,**r))
        if label in q.period.unique():
            ref=base[(base.panel=='A/B')&(base.typ==ty)&(base['fönster']=='tot')&(base.urval==label)].iloc[0]
            check('independent mean and CR1 '+ty+' '+label,abs(r['b']-ref.b)<1e-8 and abs(r['se']-ref.se)<1e-8,{'mean_error':r['b']-ref.b,'se_error':r['se']-ref.se})
        d=d.dropna(subset=['pre_ed','post20','cumulative20'])
        check('nonoverlapping window identity '+ty+' '+label,np.allclose(d.pre_ed+d.post20,d.cumulative20,atol=1e-9),len(d))
        for col in ['pre_ed','post20','cumulative20']:
            paired.append(dict(type=ty,period=label,window=col,p_wcr_49999=wcr_mean(d[col],d.review_cycle),**mean_inference(d,col)))
pd.DataFrame(sens).to_csv(OUT/'dependence_sensitivity.csv',index=False)
pd.DataFrame(paired).to_csv(OUT/'paired_horizon.csv',index=False)
news=pd.read_csv(SRC/'data/events/news_screen_extreme_events.csv')
newsids=set(news.loc[news.contaminated=='ja','event_id'])
msci=pd.read_csv(SRC/'results/msci_overlap/overlapp_handelser.csv')
overlapids=set(msci.event_id)
rob=[]
for ty in ['addition','deletion']:
    for label,start in [('2017-2026',2017),('2022-2026',2022)]:
        q=e[(e.type==ty)&(e.effective_date.dt.year>=start)].dropna(subset=['pre_ed','post20','cumulative20'])
        for variant,ss in [('full',q),('without Sivers',q[~q.company.str.contains('Sivers',case=False)]),('without MSCI overlap',q[~q.event_id.isin(overlapids)]),('without screened company news',q[~q.event_id.isin(newsids)])]:
            rob.append(dict(type=ty,period=label,variant=variant,p_wcr_49999=wcr_mean(ss.cumulative20,ss.review_cycle),**mean_inference(ss,'cumulative20')))
pd.DataFrame(rob).to_csv(OUT/'horizon_sensitivity.csv',index=False)
family=base[((base.panel=='A/B')&(base['fönster']=='tot'))|((base.panel=='D')&(base.urval=='2022–26 minus 2007–11'))][['typ','urval','b','p_wcb']].copy()
family['p_holm_10']=holm(family.p_wcb);family.to_csv(OUT/'multiplicity.csv',index=False)
equiv=[]
for r in sens:
    if r['period']=='2022–2026':
        t=stats.t.ppf(.95,r['G']-1);lo=r['b']-t*r['se'];hi=r['b']+t*r['se']
        equiv.append(dict(type=r['type'],margin_pp=1,lower90=lo,upper90=hi,equivalent=(lo>-1 and hi<1)))
pd.DataFrame(equiv).to_csv(OUT/'equivalence.csv',index=False)

def fieller(d,yc,dc):
    y=d[yc].to_numpy();x=d[dc].to_numpy(); G=d.review.nunique(); ym=y.mean();xm=x.mean()
    cov=covariance_mean(np.column_stack([y,x]),d.review);t=stats.t.ppf(.975,G-1)
    A=xm*xm-t*t*cov[1,1];B=-2*ym*xm+2*t*t*cov[0,1];C=ym*ym-t*t*cov[0,0];disc=B*B-4*A*C
    lo=hi=np.nan
    if disc>=0:
        lo,hi=sorted(((-B-np.sqrt(disc))/(2*A),(-B+np.sqrt(disc))/(2*A)))
        kind='bounded' if A>0 else 'two_unbounded_rays'
    else:kind='all_real' if A<0 else 'empty'
    return dict(n=len(d),G=G,numerator=ym,denominator=xm,ratio=ym/xm,denominator_se=np.sqrt(cov[1,1]),set_type=kind,lower=lo,upper=hi,A=A,B=B,C=C)
f=pd.read_csv(SRC/'results/fund_demand/handelser_omraknade.csv');ratios=[]
for ty in ['addition','deletion']:
    for tier in ['D_B','D_V','D_C']:
        q=f[(f.type==ty)&~f.split].dropna(subset=['y_tot',tier])
        for label,d in [(p,q[q.per==p]) for p in sorted(q.per.unique())]+[('2007-2016',q[q.ar<=2016]),('2017-2026',q[q.ar>=2017])]:
            if len(d)>=3 and d.review.nunique()>1:ratios.append(dict(type=ty,tier=tier,period=label,**fieller(d,'y_tot',tier)))
pd.DataFrame(ratios).to_csv(OUT/'fieller_ratios.csv',index=False)
check('demand C equals components',np.allclose(f.D_C.dropna(),(f.B_bara+f.V_bara+f.C_bara)[f.D_C.notna()],atol=1e-9),int(f.D_C.notna().sum()))
check('demand return matches independent CAR',np.allclose(f.y_tot,f.s*f.event_id.map(e.set_index('event_id').tot),atol=1e-8,equal_nan=True),'Comparison includes inherited missing outcomes')
manifest=pd.read_csv(SRC/'data/FILES.csv')
for r in manifest.itertuples():check('input checksum '+r.file,hashlib.md5((SRC/'data'/r.file).read_bytes()).hexdigest()==r.md5,r.md5)
pd.DataFrame(checks).to_csv(OUT/'arithmetic_checks.csv',index=False)
meta={'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy']},'source':str(SRC),'source_commit':'d2d41666ed213e4cc1f6cb382313f59c29e87ea0','passed':sum(x['passed'] for x in checks),'failed':[x for x in checks if not x['passed']],'fallback_events':fallback_events,'fallback_event_day_observations':fallback_observations,'strict_no_fill_main_CAR_changes':strict_changes}
(OUT/'audit_summary.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False))
print(json.dumps(meta,indent=2,ensure_ascii=False))
