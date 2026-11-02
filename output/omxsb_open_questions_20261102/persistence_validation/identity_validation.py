"""Fixed-match identity QA, using static IDs and PRE-outcome histories only.
Does not rematch. Confirmed alias event is excluded as a conservative data repair.
"""
from pathlib import Path
import os
from itertools import combinations
import hashlib,json
import numpy as np
import pandas as pd
from scipy import stats
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3])); O=Path(__file__).resolve().parent
S=O/'original_inputs'
d=pd.read_csv(S/'event_paths.csv',parse_dates=['AD','ED']); d=d[d.model.eq('market_adjusted')].copy()
roles=['event','c1','c2','c3'];rics=set(d[[r+'_ric' for r in roles]].stack())
px=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','totret','volume','shares'])
px=px[px.ric.isin(rics)].copy();px.date=pd.to_datetime(px.date)
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
cal=pd.DatetimeIndex(sorted(ix[ix.ric.eq('.OMXSBGI')&ix.close.notna()].date.unique()))
series={r:g.set_index('date').reindex(cal) for r,g in px.groupby('ric')}
st=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv');print(st.columns.tolist())
ids=st.set_index('ric').IssueISIN.to_dict()
rows=[]
for e in d.to_dict('records'):
 iad=cal.get_loc(e['AD']);pre=cal[max(0,iad-101):iad-1]
 for r1,r2 in combinations(roles,2):
  a,b=e[r1+'_ric'],e[r2+'_ric'];ga,gb=series[a].reindex(pre),series[b].reindex(pre)
  z=dict(event_id=e['event_id'],review=e['review'],type=e['type'],post=e['post'],role1=r1,role2=r2,ric1=a,ric2=b,isin1=ids.get(a),isin2=ids.get(b),pre_start=pre[0],pre_end=pre[-1])
  z['same_static_isin']=pd.notna(ids.get(a)) and pd.notna(ids.get(b)) and ids.get(a)==ids.get(b)
  for v in ['close','totret','volume','shares']:
   mask=ga[v].notna()&gb[v].notna();n=int(mask.sum())
   z[v+'_joint_n']=n;z[v+'_equal_n']=int(np.isclose(ga.loc[mask,v],gb.loc[mask,v],rtol=1e-10,atol=1e-10).sum());z[v+'_unique1']=ga.loc[mask,v].nunique()
  z['pre_identical_price_candidate']=z['close_joint_n']>=50 and z['close_equal_n']==z['close_joint_n'] and z['close_unique1']>=10
  z['pre_identical_price_return_volume']=bool(z['pre_identical_price_candidate'] and z['totret_joint_n']>=50 and z['totret_equal_n']==z['totret_joint_n'] and z['volume_joint_n']>=50 and z['volume_equal_n']==z['volume_joint_n'])
  rows.append(z)
f=pd.DataFrame(rows);f.to_csv(O/'fixed_match_pre_identity_screen.csv',index=False)
flags=f[f.same_static_isin|f.pre_identical_price_candidate];flags.to_csv(O/'identity_flags.csv',index=False)
print(flags.to_string(index=False))
# Only aliases confirmed by primary issuer/exchange notices enter repair below.
source='https://view.news.eu.nasdaq.com/view?id=b52a78d490c9dabac52116c623c7199fd&lang=en'
confirmed=[{'MAHAa.ST','KEOC.ST'},{'NYFO.ST','ALTRAF.ST'}]
source=[source,'https://view.news.eu.nasdaq.com/view?id=bf5badbacea6190ca2736e6094e4251c6&lang=en&src=rss']
bad=sorted(set(f[f.apply(lambda x: any({x.ric1,x.ric2}==c for c in confirmed),axis=1)].event_id))
# Affected event IDs are determined only from fixed roles and confirmed identity.
p=pd.read_csv(O/'raw_reproduction_events.csv');p=p[p.recomputed_common].copy();q=p[~p.event_id.isin(bad)].copy()
def calc(q,label):
 g=q.groupby('review').late_difference.mean();G=len(g);mu=g.mean();se=g.std(ddof=1)/np.sqrt(G);lo,hi=stats.t.interval(.95,G-1,loc=mu,scale=se)
 seed=int.from_bytes(hashlib.sha256(('repair-20261101-v5'+str(('wild',label))).encode()).digest()[:8],'little')
 b=np.random.default_rng(seed).choice([-1.,1.],(9999,G))*g.to_numpy();tb=b.mean(1)/(b.std(1,ddof=1)/np.sqrt(G))
 wild=(np.sum(abs(tb)>=abs(mu/se)-1e-12)+1)/10000
 hits=0
 for a in range(0,2**G,8192):
  bits=(np.arange(a,min(a+8192,2**G))[:,None]>>np.arange(G))&1
  hits+=np.sum(np.abs(((2*bits-1)*g.to_numpy()).mean(1))>=abs(mu)-1e-12)
 return dict(N=len(q),G=G,estimate_pp=mu,ci_lo=lo,ci_hi=hi,t_p=2*stats.t.sf(abs(mu/se),G-1),p_wild=wild,exact_sign_flip_p=hits/2**G)
label='market_adjusted/3/addition/1/common100/change_20_100'
summary=dict(screened_events=len(d),screened_pairs=len(f),flagged_pairs=flags[['event_id','ric1','ric2']].to_dict('records'),confirmed_alias_pairs=[sorted(c) for c in confirmed],source=source,removed_event_ids_all_fixed_matches=bad,removed_event_ids_primary=sorted(set(p.event_id)&set(bad)),original=calc(p,label),conservative_identity_corrected=calc(q,label),repair='Exclude whole affected event; no replacement control or changed horizon/model',remaining_identity_limit='Current static ISIN is not a historical mapping. Exact prehistory flags can identify aliases but a negative screen cannot validate all historical issuer affiliations.')
q.to_csv(O/'identity_corrected_primary_events.csv',index=False)
q.groupby('review').agg(y=('late_difference','mean'),N=('event_id','size')).to_csv(O/'identity_corrected_review_means.csv')
# Decomposition of the existing contrast only, not a new test.
q['control_average']=q[['c1_raw_late','c2_raw_late','c3_raw_late']].mean(axis=1)
summary['same_corrected_sample_raw_late_decomposition']={'event_daily_return_sum':q.groupby('review').event_raw_late.mean().mean(),'control_daily_return_sum':q.groupby('review').control_average.mean().mean()}
(O/'identity_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
