"""Holdings measurement DD and predeclared availability-only fixed-universe sensitivity.
Uses inherited classifications and snapshots without changing primary estimators.
Fixed funds are selected only by verified mandate and reporting availability at
EVERY review in the interval, not by return or trading outcomes. Empty universes
are retained and reported. Missing positions cannot be authenticated as zeros
from this security-query extract.
"""
from pathlib import Path
import sys, argparse, json, io, contextlib, hashlib
import numpy as np
import pandas as pd
from scipy import stats
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args();src=a.source.resolve();out=a.out.resolve();out.mkdir(exist_ok=True,parents=True)
# Execute only classification/report-selection setup, redirecting ALL output to
# this DD directory. No source files or primary outputs are modified.
f=src/'code/02_fund_demand.py';code=f.read_text().split('# ---------- händelser från rättelserna 3 nov')[0]
ns={'__file__':str(f),'__name__':'holdings_dd_setup'}
oldargv=sys.argv[:];sys.argv=[str(f),str(src/'data/funds/index_fund_list_with_mandates.csv'),'unused',str(out/'holdings_setup')]
with contextlib.redirect_stdout(io.StringIO()):exec(compile(code,str(f),'exec'),ns)
sys.argv=oldargv
F=ns['F'];G0=ns['G0'];KAND=ns['KAND'];rapport_i=ns['rapport_i'];grupp=ns['grupp'];NY=ns['NY']
E=pd.read_csv(src/'results/fund_demand/handelser_omraknade.csv',parse_dates=['AD','ED']);E['split']=E.split.astype(bool)
# Report filing-date coverage/zero imputation audit in original grouping.
fundrows=[]
for eid,x in G0.groupby('event_id'):
 AD,ED=x.AD.iloc[0],x.ED.iloc[0]
 for fund,xf in x.groupby('fond'):
  d0=rapport_i(fund,AD-pd.Timedelta(days=120),AD-pd.Timedelta(days=1),sista=True);d1=rapport_i(fund,ED,ED+pd.Timedelta(days=45))
  if d0 is None or d1 is None:continue
  g0,g1=grupp(fund.lower(),d0),grupp(fund.lower(),d1)
  if g0!=g1 or not g0.startswith('OMXSB-'):continue
  pre=xf[xf.snap=='fore'];post=xf[(xf.snap=='efter')&(xf.rapport>=ED)]
  before=pre.aktier.sum();after=post.aktier.sum()
  fundrows.append(dict(event_id=eid,fund=fund,key=NY.get(fund.lower()),group=g0,pre=float(before),post=float(after),net=float(after-before),pre_missing=pre.empty,post_missing=post.empty,pre_date_diff=bool((pre.rapport!=d0).any()),post_date_diff=bool((post.rapport!=d1).any()),pre_after_AD=bool((pre.rapport>=AD).any()),pre_older120=bool((pre.rapport<AD-pd.Timedelta(days=120)).any()),post_later45=bool((post.rapport>ED+pd.Timedelta(days=45)).any()),stale_post=bool(((xf.snap=='efter')&(xf.rapport<ED)&(xf.aktier>0)).any()),pre_rows=len(pre),post_rows=len(post)))
P=pd.DataFrame(fundrows).merge(E[['event_id','type','per','review','s','sh_ed','split','fonddata','y_tot']],on='event_id',how='left')
# Primary complete holdings sample, matches main C ratio eligibility.
base=E[(~E.split)&E.fonddata.astype(bool)&E.D_C.notna()&E.y_tot.notna()&(E.sh_ed>0)].copy()
coverage=[]
for (ty,per),g in base.groupby(['type','per']):
 coverage.append(dict(type=ty,period=per,n=len(g),G=g.review.nunique(),D_B=g.D_B.mean(),D_V=g.D_V.mean(),D_C=g.D_C.mean(),nf_B=g.nf_B.mean(),nf_V=g.nf_V.mean(),nf_C=g.nf_C.mean(),zero_demand=int((g.D_C==0).sum()),negative_demand=int((g.D_C<0).sum()),Y=g.y_tot.mean()))
pd.DataFrame(coverage).to_csv(out/'holdings_coverage_summary.csv',index=False)
Q=P[P.event_id.isin(base.event_id)].copy()
rows=[]
for (ty,per),g in Q.groupby(['type','per']):
 rows.append(dict(type=ty,period=per,fund_event_records=len(g),observed_both_sides=int((~g.pre_missing&~g.post_missing).sum()),missing_pre_position=int(g.pre_missing.sum()),missing_post_position=int(g.post_missing.sum()),stale_post_zero=int(g.stale_post.sum()),pre_date_diff_from_availability_check=int(g.pre_date_diff.sum()),post_date_diff_from_availability_check=int(g.post_date_diff.sum()),pre_after_AD=int(g.pre_after_AD.sum()),pre_older120=int(g.pre_older120.sum()),post_later45=int(g.post_later45.sum()),multiple_pre_rows=int((g.pre_rows>1).sum()),multiple_post_rows=int((g.post_rows>1).sum())))
pd.DataFrame(rows).to_csv(out/'holdings_position_observability.csv',index=False)
# Exact numerator reconstruction, using every fund-event original classified as B,V,C.
allnets=P.groupby('event_id').net.sum()
rebuild=np.array([100*s*allnets.get(e,0)/sh for e,s,sh in zip(base.event_id,base.s,base.sh_ed)])
err=np.max(abs(rebuild-base.D_C));assert err<1e-10
# Availability by every review, independent of event return/trade outcome.
reviews=E.groupby('review').agg(AD=('AD','first'),ED=('ED','first')).sort_values('ED')
availability={}
for review,x in reviews.iterrows():
 fs=set()
 for fund in KAND:
  d0=rapport_i(fund,x.AD-pd.Timedelta(days=120),x.AD-pd.Timedelta(days=1),sista=True);d1=rapport_i(fund,x.ED,x.ED+pd.Timedelta(days=45))
  if d0 is None or d1 is None:continue
  g0,g1=grupp(fund.lower(),d0),grupp(fund.lower(),d1)
  if g0==g1 and g0.startswith('OMXSB-'):fs.add(fund)
 availability[review]=fs
fixed_summaries=[];fixed_rows=[]
for label,start,end in [('full_2007_2026',2007,2026),('later_2017_2026',2017,2026)]:
 revs=reviews[(reviews.ED.dt.year>=start)&(reviews.ED.dt.year<=end)].index.tolist()
 common=set.intersection(*(availability[r] for r in revs))
 keysets=[{NY.get(f.lower()) for f in availability[r] if NY.get(f.lower()) is not None} for r in revs]
 commonkeys=set.intersection(*keysets)
 fixed_summaries.append(dict(interval=label,reviews=len(revs),constant_fund_names=len(common),constant_mandate_keys=len(commonkeys),fund_names=sorted(common),mandate_keys=sorted(commonkeys),selection='Intersection of verified mandate and pre/post report availability at every review; no selection on returns/purchases. Keys can pool changing fund families and are not a constant-portfolio panel.'))
 for unit,keep in [('fund_name',common),('mandate_key',commonkeys)]:
  if not keep:continue
  selected=P[P.fund.isin(keep)] if unit=='fund_name' else P[P.key.isin(keep)]
  net=selected.groupby('event_id').net.sum()
  z=base[base.review.isin(revs)].copy();z['D_fixed']=[100*s*net.get(e,0)/sh for e,s,sh in zip(z.event_id,z.s,z.sh_ed)]
  for (ty,per),g in z.groupby(['type','per']):
   fixed_rows.append(dict(interval=label,unit=unit,type=ty,period=per,fixed_entities=len(keep),events=len(g),reviews=g.review.nunique(),mean_primary_D_C=g.D_C.mean(),mean_fixed_D=g.D_fixed.mean(),mean_sign_adjusted_CAR=g.y_tot.mean(),primary_ratio=g.y_tot.mean()/g.D_C.mean(),fixed_ratio=g.y_tot.mean()/g.D_fixed.mean() if g.D_fixed.mean()!=0 else np.nan))
  # Compare 2017-21 vs 2022-26 demand on identical fixed portfolio set, event-weighted.
  if label=='later_2017_2026':
   for ty in ['addition','deletion']:
    g=z[z.type==ty];g=g[g.per.isin(['2017–21','2022–26'])]
    # Only report simple period means here: changing events and unknown zero coverage
    # mean this is not a causal time comparison or authenticated coverage test.
 pd.DataFrame(fixed_rows).to_csv(out/'holdings_fixed_universe_sensitivity.csv',index=False)
(out/'holdings_fixed_universe_definition.json').write_text(json.dumps(fixed_summaries,ensure_ascii=False,indent=2))
meta={'primary_complete_events':len(base),'fund_event_records_in_primary_sample':len(Q),'max_D_C_reconstruction_error':float(err),'source_commit':'d2d41666ed213e4cc1f6cb382313f59c29e87ea0','important_limit':'Report availability is inferred across securities in the query extract. It does not establish full report completeness or authenticate an absent security position as zero. Both fixed-universe variants retain original zero assumptions.','outputs':'Only aggregate CSVs and public fund names/mandate classification metadata. Raw fund-event P not saved.'}
(out/'holdings_dd_metadata.json').write_text(json.dumps(meta,indent=2))
print(pd.DataFrame(rows).to_string(index=False));print(json.dumps(fixed_summaries,ensure_ascii=False,indent=2));print(pd.DataFrame(fixed_rows).to_string(index=False));print(meta)
