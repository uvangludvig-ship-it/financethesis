"""Independent frozen-window audit; no import of either production calculation."""
from pathlib import Path
import os
import hashlib, json, re
import numpy as np
import pandas as pd
from scipy import stats
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
S=Path(__file__).resolve().parent/'original_inputs'
O=Path(__file__).resolve().parent
D=pd.read_csv(S/'event_paths.csv',parse_dates=['AD','ED'])
P=D[(D.model=='market_adjusted')&(D.type=='addition')&(D.post==1)].copy()
roles=['event','c1','c2','c3']; H=[1,20,60,100]
rics=set(P[[x+'_ric' for x in roles]].to_numpy().ravel())
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
cal=pd.DatetimeIndex(sorted(ix[(ix.ric=='.OMXSBGI')&ix.close.notna()].date.unique()))
mr=ix[ix.ric=='.OMXSBGI'].set_index('date').close.reindex(cal).pct_change(fill_method=None)*100
px=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','totret','volume','shares','source'])
px=px[px.ric.isin(rics)].copy();px['date']=pd.to_datetime(px.date);px=px[px.date.isin(cal)].drop_duplicates()
assert not px.duplicated(['ric','date']).any()
series={};diag=[];large=[]
for ric,g in px.groupby('ric'):
 g=g.set_index('date').reindex(cal)
 g['fallback']=g.totret.isna()&g.close.notna()&g.close.shift().notna()
 g['ret']=g.totret.where(g.totret.notna(),g.close.pct_change(fill_method=None)*100)
 g.loc[(g.ret>1000)|(g.ret<-100),'ret']=np.nan
 g['abnormal']=g.ret-mr
 series[ric]=g
rows=[];mmdiffs=[]
for row in P.to_dict('records'):
 ia=cal.get_loc(row['AD']);ie=cal.get_loc(row['ED'])
 out={k:row[k] for k in ['event_id','review','issuer','AD','ED','ric','common3']}
 out['window_start']=cal[ie+21];out['window_end']=cal[ie+100]
 rolevals={};allgood=True
 for role in roles:
  ric=row[role+'_ric'];g=series[ric]
  full=g.iloc[ia-1:ie+101];late=g.iloc[ie+21:ie+101]
  valid=len(full)==ie+101-(ia-1) and full.ret.notna().all()
  rolevals[role]=late.ret.sum() if valid else np.nan
  allgood &= bool(valid)
  out[role+'_ric']=ric;out[role+'_raw_late']=rolevals[role]
  for h in H:
   a=g.abnormal.iloc[ia-1:ie+h+1]
   v=a.sum() if len(a)==ie+h+1-(ia-1) and a.notna().all() else np.nan
   saved=row[f'{role}_{h}'];diag.append({'event_id':row['event_id'],'role':role,'ric':ric,'h':h,'raw_value':v,'saved_value':saved,'abs_difference':abs(v-saved) if np.isfinite(v) and np.isfinite(saved) else np.nan,'same_missing':bool(pd.isna(v)==pd.isna(saved))})
  out[role+'_missing_full']=int(full.ret.isna().sum())
  out[role+'_fallback_full']=int(full.fallback.sum());out[role+'_zero_volume_full']=int(full.volume.eq(0).sum())
  out[role+'_first_missing']=str(full.index[full.ret.isna()][0].date()) if full.ret.isna().any() else ''
  # Fixed data-QA screen: all daily absolute returns >=20pp in the late window.
  for dt,z in late[late.ret.abs()>=20].iterrows():
   prev=g.loc[:dt].iloc[-2] if len(g.loc[:dt])>1 else None
   large.append({'event_id':row['event_id'],'review':row['review'],'role':role,'ric':ric,'date':dt,'ret':z.ret,'totret':z.totret,'fallback':z.fallback,'close':z.close,'previous_close':prev.close if prev is not None else None,'shares':z.shares,'previous_shares':prev.shares if prev is not None else None,'volume':z.volume,'source':z.source})
 out['recomputed_common']=allgood
 out['late_difference']=rolevals['event']-np.mean([rolevals[k] for k in ['c1','c2','c3']]) if allgood else np.nan
 out['saved_late_difference']=row['diff3_100']-row['diff3_20']
 rows.append(out)
V=pd.DataFrame(rows);V.to_csv(O/'raw_reproduction_events.csv',index=False)
C=pd.DataFrame(diag);C.to_csv(O/'raw_level_comparison.csv',index=False)
L=pd.DataFrame(large);L.to_csv(O/'large_daily_return_flags.csv',index=False)
assert V.recomputed_common.eq(V.common3).all()
assert C.same_missing.all()
assert C.abs_difference.max()<1e-8
Q=V[V.recomputed_common].copy()
Q['weight']=1/Q.groupby('review').event_id.transform('size')/Q.review.nunique()
Q['contribution_pp']=Q.late_difference*Q.weight
Q.sort_values('contribution_pp').to_csv(O/'event_influence_ranked.csv',index=False)
g=Q.groupby('review').late_difference.mean();G=len(g);mu=g.mean();se=g.std(ddof=1)/np.sqrt(G);ci=stats.t.interval(.95,G-1,loc=mu,scale=se)
# All 2^19 Rademacher draws; no dependence on production inference helper.
hits=0;n=2**G
for a in range(0,n,8192):
 bits=((np.arange(a,min(a+8192,n))[:,None]>>np.arange(G))&1)
 y=(2*bits-1)*g.to_numpy()
 hits+=np.sum(np.abs(y.mean(1))>=abs(mu)-1e-12)
# Explicit restricted-null intercept-only bootstrap, matching the declared seed.
label='market_adjusted/3/addition/1/common100/change_20_100'
seed=int.from_bytes(hashlib.sha256(('repair-20261101-v5'+str(('wild',label))).encode()).digest()[:8],'little')
w=np.random.default_rng(seed).choice([-1.,1.],(9999,G));b=w*g.to_numpy()
t=b.mean(1)/(b.std(1,ddof=1)/np.sqrt(G));wild=(np.sum(abs(t)>=abs(mu/se)-1e-12)+1)/10000
# Data dependencies: repeated control issuer is not removed by omitting event issuer.
def issuer(ric):return re.sub(r'(?:sdb)?[a-z]+$','',str(ric).split('.ST')[0])
influ=[]
allissuers=sorted(set(issuer(x) for x in Q[[r+'_ric' for r in roles]].to_numpy().ravel()))
for name in allissuers:
 keep=~Q[[r+'_ric' for r in roles]].apply(lambda c:c.map(issuer)).eq(name).any(axis=1)
 q=Q[keep]
 influ.append({'omitted_any_role_issuer':name,'events_removed':len(Q)-len(q),'reviews_retained':q.review.nunique(),'estimate':q.groupby('review').late_difference.mean().mean()})
I=pd.DataFrame(influ);I.to_csv(O/'all_role_issuer_influence.csv',index=False)
# Individual security contributes once for each reused role; expose concentration.
security=[]
for _,e in Q.iterrows():
 for role in roles:
  security.append({'event_id':e.event_id,'review':e.review,'role':role,'ric':e[role+'_ric'],'issuer':issuer(e[role+'_ric']),'weighted_contribution':e.weight*e[role+'_raw_late']*(1 if role=='event' else -1/3)})
U=pd.DataFrame(security);U.groupby(['issuer','ric']).agg(contribution=('weighted_contribution','sum'),uses=('event_id','size'),reviews=('review','nunique')).sort_values('contribution').to_csv(O/'security_contributions.csv')
# On the declared market-model sample, compare MA and MM on identical events;
# this changes no horizon/model and isolates support from model differences.
MM=D[(D.model=='market_model')&(D.type=='addition')&(D.post==1)&D.common3]
same=Q[Q.event_id.isin(MM.event_id)].copy()
model_bridge={'N':len(same),'market_adjusted_same_support':same.groupby('review').late_difference.mean().mean(),'market_model_saved':(MM.assign(y=MM.diff3_100-MM.diff3_20)).groupby('review').y.mean().mean()}
# Exposure-time overlap and repeated controls across distinct review clusters.
reviewdates=Q.groupby('review').agg(start=('window_start','min'),end=('window_end','max'))
overlaps=[]
for i,(r1,z1) in enumerate(reviewdates.iterrows()):
 for r2,z2 in list(reviewdates.iterrows())[i+1:]:
  if max(z1.start,z2.start)<=min(z1.end,z2.end):overlaps.append([r1,r2])
summary={'primary_N':len(Q),'G':G,'independent_raw_mean_pp':mu,'ci':list(ci),'t':mu/se,'t_p':2*stats.t.sf(abs(mu/se),G-1),'exact_sign_flip_p':hits/n,'explicit_wild_p':wild,'max_level_discrepancy':C.abs_difference.max(),'max_primary_discrepancy':(Q.late_difference-Q.saved_late_difference).abs().max(),'all_missing_flags_agree':bool(C.same_missing.all()),'late_window':'ED+21 through ED+100 inclusive; 80 trading daily returns','preselected':len(P),'lost':int((~V.recomputed_common).sum()),'full_window_fallback_cells':int(Q[[r+'_fallback_full' for r in roles]].sum().sum()),'zero_volume_full_cells':int(Q[[r+'_zero_volume_full' for r in roles]].sum().sum()),'same_support_model_bridge':model_bridge,'overlapping_late_review_windows':overlaps,'leave_any_role_issuer_range':list(I.estimate.agg(['min','max'])),'new_return_horizons_or_models':False}
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('Largest event contributions:');print(Q.sort_values('contribution_pp')[['event_id','ric','review','late_difference','contribution_pp']].head(10).to_string(index=False))
print('Largest security contributions:');print(pd.read_csv(O/'security_contributions.csv').head(12).to_string(index=False))
