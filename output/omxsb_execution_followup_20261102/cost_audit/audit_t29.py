"""Read-only T29 accounting/unit audit. No new return calculation or licensed raw export."""
from pathlib import Path
import argparse, hashlib, json, re
import numpy as np
import pandas as pd
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); p.add_argument('--out',required=True); a=p.parse_args()
R=Path(a.repo); O=Path(a.out); O.mkdir(parents=True,exist_ok=True)
I=R/'code/claude_checks/data'; T=R/'code/claude_checks/runda10_resultat'
inputs={}
def read(rel,**kwargs):
 f=R/rel; inputs[rel]=hashlib.sha256(f.read_bytes()).hexdigest(); return pd.read_csv(f,**kwargs)
e=read('code/claude_checks/runda10_resultat/T29_handelser.csv',parse_dates=['AD'])
ev=read('output/omxsb_replication_2007/events_car.csv',parse_dates=['AD','ED'])
rev=ev.groupby('review_cycle').agg(AD=('AD','first'),ED=('ED','first')).sort_values('AD').reset_index().rename(columns={'review_cycle':'review'})
e=e.merge(rev[['review','ED']],on='review',validate='many_to_one'); e['year_ED']=e.ED.dt.year
e['complete_calendar_year']=e.year_ED.between(2008,2025)
aum=read('code/claude_checks/data/shof/tracker_aum_shof_v2.csv'); aum['month']=pd.to_datetime(aum.manad+'-01'); aum=aum.set_index('manad')
checks=[]; original=[]; reviewrows=[]
for variant,col in [('primär','prem'),('sekundär','prem2')]:
 d=e.dropna(subset=['w',col]).copy(); d['contribution_bp']=d.w*d[col]*100
 z=d.groupby(['review','ar','year_ED','per'],observed=True).agg(linear_bp=('contribution_bp','sum'),turnover_pct=('w',lambda v:v.sum()*100),n=('event_id','size')).reset_index()
 z=z.merge(rev,on='review',validate='one_to_one'); z['variant']=variant
 z['aum_original_month']=[f'{y}-12' if f'{y}-12' in aum.index else aum.index[-1] for y in z.ar]
 z['aum_original_bn']=[aum.loc[m,'inkl_xact_omxsb_mdkr'] for m in z.aum_original_month]
 z['aum_original_fallback']=[f'{y}-12' not in aum.index for y in z.ar]
 prior=[]
 for ad in z.AD:
  eligible=aum[aum.month<ad.to_period('M').to_timestamp()]
  prior.append(eligible.index[-1] if len(eligible) else None)
 z['aum_prior_month']=prior; z['aum_prior_bn']=[aum.loc[m,'inkl_xact_omxsb_mdkr'] if m else np.nan for m in prior]
 z['million_SEK_original_scenario']=z.linear_bp*z.aum_original_bn/10
 z['million_SEK_prior_scenario']=z.linear_bp*z.aum_prior_bn/10
 z['complete_calendar_year']=z.year_ED.between(2008,2025)
 ref=read(f'code/claude_checks/runda10_resultat/T29_per_oversyn_{variant}.csv')
 j=z.merge(ref[['review','kostnad','mkr']],on='review',validate='one_to_one')
 checks.append({'test':variant+'_saved_review_arithmetic','max_abs_bp_difference':float((j.linear_bp-j.kostnad).abs().max()),'max_abs_SEKm_difference':float((j.million_SEK_original_scenario-j.mkr).abs().max())})
 for per,g in z.groupby('per',observed=True):
  original.append(dict(variant=variant,period=per,reviews=len(g),events=int(g.n.sum()),ADyears=g.ar.nunique(),bp_per_ADyear=g.linear_bp.sum()/g.ar.nunique(),SEKm_per_ADyear=g.million_SEK_original_scenario.sum()/g.ar.nunique()))
 reviewrows.append(z)
z=pd.concat(reviewrows,ignore_index=True); z.to_csv(O/'review_accounting.csv',index=False)
pd.DataFrame(original).to_csv(O/'original_arithmetic_reproduced.csv',index=False)
y=z.groupby(['variant','year_ED','complete_calendar_year']).agg(reviews=('review','size'),events=('n','sum'),linear_bp=('linear_bp','sum'),turnover_pct=('turnover_pct','sum'),million_SEK_original_scenario=('million_SEK_original_scenario','sum'),million_SEK_prior_scenario=('million_SEK_prior_scenario','sum')).reset_index(); y.to_csv(O/'calendar_year_accounting.csv',index=False)
sc=[]
for label,years,annual in [('2007_partial',[2007],False),('2008_2011_complete',list(range(2008,2012)),True),('2012_2016_complete',list(range(2012,2017)),True),('2017_2021_complete',list(range(2017,2022)),True),('2022_2025_complete',list(range(2022,2026)),True),('2026_H1_only',[2026],False),('2008_2025_complete',list(range(2008,2026)),True)]:
 g=y[(y.variant=='primär')&y.year_ED.isin(years)]; divisor=len(years) if annual else 1
 for fraction in [0.,.5,1.]:
  sc.append(dict(period=label,assumed_premium_fraction=fraction,years_divisor=divisor,annual_average=annual,reviews=int(g.reviews.sum()),events=int(g.events.sum()),scenario_bp=g.linear_bp.sum()/divisor*fraction,SEK_per_100000=g.linear_bp.sum()/divisor*fraction*10,SEKm_original_AUM=g.million_SEK_original_scenario.sum()/divisor*fraction,SEKm_prior_AUM=g.million_SEK_prior_scenario.sum()/divisor*fraction,actual_cost_identified=False,official_weights_verified=False))
pd.DataFrame(sc).to_csv(O/'conditional_scenarios.csv',index=False)
# Source and scale diagnostics only: no correction of fund values by an assumed factor.
fundrows=[]
for c in aum.columns:
 if not c.startswith('fond: '): continue
 name=c[6:]; src='källa: '+name
 for m,r in aum.iterrows():
  v=r[c]; fundrows.append(dict(month=m,fund=name,value_bn=v,source=r.get(src),positive_below_one_million_SEK=bool(pd.notna(v) and 0<v<.001),missing_source=r.get(src)=='saknas',zero_value=bool(v==0)))
f=pd.DataFrame(fundrows); f[f.positive_below_one_million_SEK|f.missing_source].to_csv(O/'aum_source_scale_flags.csv',index=False)
# Reproduce denominator construction from only required licensed input fields; export derived diagnostics.
raw=R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet'; inputs[str(raw.relative_to(R))]=hashlib.sha256(raw.read_bytes()).hexdigest()
px=pd.read_parquet(raw,columns=['ric','date','close','mcap','shares']); px.date=pd.to_datetime(px.date); px=px[px.ric.astype(str).str.contains(r'\.ST')]
s=read('code/claude_checks/data/lseg_saknade_aktier.csv')
adds=[]
for ric in ['NDASE.ST','TIETOS.ST']:
 d=s[(s.ric==ric)&s.Date.notna()].copy(); d['date']=pd.to_datetime(d.Date)
 m=s[(s.ric==ric)&(s.typ=='marknadsvarde_manad')].reset_index(drop=True); m['date']=pd.date_range('2006-01-31',periods=len(m),freq='ME')
 d=d.merge(m[['date','Outstanding Shares']].rename(columns={'Outstanding Shares':'shares'}),on='date',how='outer').sort_values('date'); d.shares=d.shares.ffill(); d=d[d.TRDPRC_1.notna()]
 adds.append(pd.DataFrame(dict(ric=ric,date=d.date,close=d.TRDPRC_1,mcap=d.TRDPRC_1*d.shares,shares=d.shares)))
px=pd.concat([px[~px.ric.isin(['NDASE.ST','TIETOS.ST'])]]+adds,ignore_index=True)
ix=read('data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date']); cal=pd.DatetimeIndex(ix.loc[(ix.ric=='.OMXSBGI')&ix.close.notna(),'date'].sort_values().unique()); pos=pd.Series(np.arange(len(cal)),index=cal)
px=px[px.date.isin(cal)].drop_duplicates(['ric','date'],keep='last').sort_values(['ric','date'])
pivot=lambda col:px.pivot_table(index='date',columns='ric',values=col).reindex(cal)
C=pivot('close'); M=pivot('mcap').ffill(limit=10); S=pivot('shares')
def root(ric):
 m=re.match(r'([A-Z0-9]+?)([a-z]|sdb[ab]?)?\.ST',str(ric)); return m.group(1) if m else str(ric)
roots={}
for ric in C: roots.setdefault(root(ric),[]).append(ric)
h=read('code/claude_checks/data/lseg_freefloat_hist.csv'); hd={(r.review,r.ric):r.ff for r in h.dropna(subset=['ff']).itertuples()}; refs=h.groupby('review').refdag.first().to_dict()
k=read('code/claude_checks/data/lseg_klassificering.csv'); cd=dict(zip(k.ric,pd.to_numeric(k.freefloat,errors='coerce')))
mem=read('code/claude_checks/data/medlemskap_verifierad.csv'); med={cy:set(g[g.status=='medlem'].ric) for cy,g in mem.groupby('review_after')}; unsure={cy:set(g[g.status=='osäker'].ric) for cy,g in mem.groupby('review_after')}
cache={}
def measure(ric,cy,i):
 key=(ric,cy,i)
 if key in cache:return cache[key].copy()
 quote=bool(ric in C and C[ric].iloc[max(i-5,0):i+1].notna().any()); cap=M[ric].iloc[i] if ric in M else np.nan
 siblings=[o for o in roots.get(root(ric),[ric]) if o in C and C[o].iloc[max(i-5,0):i+1].notna().any()]
 m=np.nan; sh={}
 if quote and cap>0:
  if len(siblings)==1:m=cap
  else:
   sh={o:S[o].iloc[max(i-60,0):i+1].ffill().iloc[-1] if o in S else np.nan for o in siblings}
   if all(v>0 for v in sh.values()):m=cap*sh[ric]/sum(sh.values())
 hist=hd.get((cy,ric),np.nan); current=cd.get(ric,np.nan); used=hist if (cy,ric) in hd else current; provenance='historical' if (cy,ric) in hd else 'current_fallback'
 if not(pd.notna(used) and 0<used<=100):used=100.; provenance='assumed_100_fallback'
 val=m*used/100 if m>0 else np.nan
 r=dict(ric=ric,review=cy,valuation_date=str(cal[i].date()),quote_available=quote,root=root(ric),n_live_root_RICs=len(siblings),live_root_RICs='|'.join(siblings),shares_all_positive=bool(sh and all(v>0 for v in sh.values())),float_source=provenance,float_reference_date=refs.get(cy),float_used_pct=used,ffm_reproduced=val,ffm_available=bool(np.isfinite(val)),classcap_reproduced=m,companycap=cap,supplement_constructed_cap=ric in ['NDASE.ST','TIETOS.ST'])
 cache[key]=r;return r.copy()
ledger=[]; reviewcov=[]; recweights=[]
for j,r in rev.iterrows():
 cy=r.review;i=int(pos[r.AD])-1; events=ev[ev.review_cycle==cy]; aset=set(events.loc[events.type=='addition','RIC']); dset=set(events.loc[events.type=='deletion','RIC']); after=med.get(cy,set()); before=med.get(rev.iloc[j-1].review,set()) if j>0 else (after-aset)|dset
 totals={}
 for side,universe in [('before',before),('after',after)]:
  vals=[]
  for ric in sorted(universe):
   row=measure(ric,cy,i); row['side']=side; ledger.append(row); vals.append(row)
  v=pd.DataFrame(vals); totals[side]=v.ffm_reproduced.sum()
  reviewcov.append(dict(review=cy,side=side,members=len(v),without_recent_quote=int((~v.quote_available).sum()),without_ffm=int((~v.ffm_available).sum()),historical_float=int((v.float_source=='historical').sum()),current_float_fallback=int((v.float_source=='current_fallback').sum()),assumed_100_float=int((v.float_source=='assumed_100_fallback').sum()),denominator_ffm=totals[side],denominator_complete=bool(v.ffm_available.all()),current_review_uncertain_members=len(unsure.get(cy,set())),live_multiple_root=int((v.n_live_root_RICs>1).sum())))
 for x in e[e.review==cy].itertuples():
  q=measure(x.ric,cy,i); denom=totals['after' if x.typ=='addition' else 'before']; w=q['ffm_reproduced']/denom if denom>0 else np.nan
  recweights.append(dict(event_id=x.event_id,review=cy,ric=x.ric,w_saved=x.w,w_reproduced=w,float_source=q['float_source'],n_live_root_RICs=q['n_live_root_RICs'],denominator_complete=next(v['denominator_complete'] for v in reviewcov[-2:] if v['side']==('after' if x.typ=='addition' else 'before'))))
l=pd.DataFrame(ledger); cov=pd.DataFrame(reviewcov); w=pd.DataFrame(recweights)
checks.append({'test':'saved_weights','max_abs_difference':float((w.w_saved-w.w_reproduced).abs().max()),'missing_pattern_equal':bool(w.w_saved.isna().equals(w.w_reproduced.isna()))})
# Available official monthly data are Stockholm instrument capitalization, not official index shares/weights.
pool=read('output/omxsb_open_questions_20261102/eligible_pool/strict_historical_main_stock_pool.csv')
fields=['review','ric','nasdaq_isin','company_code','market_cap','shares_listed','reference_date','source_url','source_excel_row','same_instrument_RIC_count','same_instrument_RIC_alternatives']
pool=pool[fields].drop_duplicates(['review','ric'])
l=l.merge(pool,on=['review','ric'],how='left',validate='many_to_one'); l['official_monthly_identity_available']=l.nasdaq_isin.notna(); l['official_index_weight_available']=False
# Diagnostic same-reference-date comparison. Ratio is NOT a universal error because issuer/global and listed-venue scope differ.
refrows=[]
for r in l[['review','ric','reference_date','market_cap','nasdaq_isin']].drop_duplicates().itertuples(index=False):
 if pd.isna(r.reference_date):continue
 dt=pd.Timestamp(r.reference_date);i=cal.searchsorted(dt,side='right')-1;q=measure(r.ric,r.review,int(i));refrows.append(dict(review=r.review,ric=r.ric,nasdaq_isin=r.nasdaq_isin,nasdaq_monthly_listed_cap=r.market_cap,reproduced_classcap_same_ref=q['classcap_reproduced'],proxy_to_monthly_ratio=q['classcap_reproduced']/r.market_cap if r.market_cap>0 else np.nan,not_interpreted_as_universal_error=True))
pd.DataFrame(refrows).drop(columns=['reproduced_classcap_same_ref']).to_csv(O/'monthly_cap_scope_diagnostic.csv',index=False)
l.drop(columns=['companycap','float_used_pct','classcap_reproduced','ffm_reproduced']).to_csv(O/'membership_weight_coverage.csv',index=False);cov.to_csv(O/'review_weight_coverage.csv',index=False);w.to_csv(O/'event_weight_audit.csv',index=False)
e.to_csv(O/'saved_event_accounting_inputs.csv',index=False)
summary={'saved_events':len(e),'primary_complete_events':int(e[['w','prem']].notna().all(axis=1).sum()),'reviews':len(rev),'complete_denominators_out_of_78':int(cov.denominator_complete.sum()),'missing_ffm_min':int(cov.without_ffm.min()),'missing_ffm_max':int(cov.without_ffm.max()),'event_float_provenance':w.float_source.value_counts().to_dict(),'member_endpoint_float_provenance':l.float_source.value_counts().to_dict(),'valid_member_float_provenance':l[l.ffm_available].float_source.value_counts().to_dict(),'valid_nondated_float_denominator_share_aggregate':float(l.loc[l.ffm_available & l.float_source.ne('historical'),'ffm_reproduced'].sum()/l.ffm_reproduced.sum()),'event_multi_live_RIC_roots':int((w.n_live_root_RICs>1).sum()),'AUM_tiny_positive_rows':int(f.positive_below_one_million_SEK.sum()),'tiny_positive_funds':sorted(f.loc[f.positive_below_one_million_SEK,'fund'].unique()),'prior_AUM_missing_reviews':int(z[z.variant=='primär'].aum_prior_bn.isna().sum()),'official_monthly_covered_member_endpoints':int(l.official_monthly_identity_available.sum()),'official_index_weights_verified':0,'checks':checks}
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
for rel in ['code/claude_checks/runda10.py','code/claude_checks/runda3.py','code/claude_checks/shof_aum.py','output/omxsb_extension_20261031/candidate/sources/methodology_nordic_2018.txt']:
 inputs[rel]=hashlib.sha256((R/rel).read_bytes()).hexdigest()
(O/'input_hashes.json').write_text(json.dumps(inputs,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2));print(pd.DataFrame(sc).query('assumed_premium_fraction==1').to_string(index=False))
