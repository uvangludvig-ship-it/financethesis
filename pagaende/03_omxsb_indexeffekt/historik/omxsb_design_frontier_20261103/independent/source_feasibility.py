"""Metadata and capital-coverage only: no flow, covariance or price outcome estimates."""
from pathlib import Path
import hashlib,json,datetime,zipfile
import pandas as pd
import numpy as np
R=Path('/Users/ludviguvang/dev/financethesis')
O=Path(__file__).resolve().parent
C=O.parents[1]/'contribution_round_20261103/ownership_capital'
OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership'
inputs=[R/'data/raw/shof/fundmaster.xlsx',R/'data/derived/shof_monthly/shof_valuations_monthly.csv',R/'data/derived/shof_monthly/shof_rips_monthly.csv',R/'code/claude_checks/data/shof/shof_valuations_2026-11-02.zip',OWN/'fund_metadata_classification.csv',OWN/'decomp_fund_groups.csv',OWN/'security_role_gate.csv',C/'normalized_fund_role_contributions.csv.gz',C/'security_feasibility_gate.csv',R/'data/derived/fi/fi_holdings_long.csv.gz']
lock={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Source feasibility only, through 2023. No numeric net flows, fund returns, covariance or stock returns computed. Numeric TRI read solely to test positive nonmissing presence.',
 'monthly_source_gate':'25 consecutive pre-quarter month endpoints; positive class and fund TNA; all observed classes and funds SEK; repeated fund TNA agrees within 0.1%; class sum reconciles to fund TNA within 1%; all classes have positive returntype1 TRI and dates at most4 calendar days from TNA within same month; stable set of observed classes throughout25months; every class inception<=firstendpoint, obsolete date absent or later than lastendpoint. Exact current master ISIN->uniqueFundId join and same mapping at q0/q1. Any duplicate FI mapping to oneFundId in same review excluded. This gate is provisional, current master dates not a certified merger history.',
 'capital_coverage':'Use exact fund/event/role support in previously audited normalized ledger. At q0 andq1 within a stock, quantity fraction equals capital fraction because one common price cancels; q0 split factor also cancels. Compute each event and original3controls separately; no deltas, price outcomes or covariance. Aggregate means are equal-event-weighted coverage ratios, never pooled SEKcapital.',
 'zip':'Read IDs/dates/currencies and NF presence flags only; report coverage not validity. Count allmissing/partial month fields, no numeric NF.'}
lock['inputs']={str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs}
(O/'SOURCE_FEASIBILITY_LOCK.json').write_text(json.dumps(lock,indent=2))
M=pd.read_excel(inputs[0],usecols=['performanceid','secid','fundid','ISIN','inceptiondate','obsoletedate'])
F=pd.read_csv(inputs[4],dtype={'fund_id':str},usecols=['quarter','fund_id','fund_isin'])
G=pd.read_csv(inputs[5],dtype={'fund_id':str},usecols=['review','fund_id','q0','q1']);G=G[G.q1.le('2023-12-31')]
links=F.merge(M[['ISIN','fundid']].dropna().drop_duplicates(),left_on='fund_isin',right_on='ISIN',how='left').groupby(['fund_id','quarter'],as_index=False).agg(nfunds=('fundid','nunique'),fundid=('fundid','first'))
links=links[links.nfunds.eq(1)]
G=G.merge(links[['fund_id','quarter','fundid']],left_on=['fund_id','q0'],right_on=['fund_id','quarter'],how='left').drop(columns='quarter').rename(columns={'fundid':'f0'})
G=G.merge(links[['fund_id','quarter','fundid']],left_on=['fund_id','q1'],right_on=['fund_id','quarter'],how='left').drop(columns='quarter').rename(columns={'fundid':'f1'})
G['same_id']=G.f0.notna()&G.f0.eq(G.f1)
G['duplicate']=G.same_id&G.groupby(['review','f0']).fund_id.transform('nunique').gt(1)
G['exact_map']=G.same_id&~G.duplicate
badpid=M.groupby('performanceid').fundid.nunique();badpid=set(badpid[badpid.ne(1)].index)
P=M[~M.performanceid.isin(badpid)].drop_duplicates('performanceid').rename(columns={'performanceid':'performanceId'})
V=pd.read_csv(inputs[1],usecols=['performanceId','ym','ccy_class','ccy_fund','last_date','tnaclass','tnafund'])
V=V[V.ym.le('2023-12')].merge(P[['performanceId','fundid','inceptiondate','obsoletedate']],on='performanceId',validate='m:1')
V=V[V.fundid.isin(G.loc[G.exact_map,'f0'])]
T=pd.read_csv(inputs[2],usecols=['performanceId','returntype','ym','last_date','tri_sek'])
T=T[T.returntype.eq(1)&T.ym.le('2023-12')].copy();T['tri_present']=T.tri_sek.gt(0)&np.isfinite(T.tri_sek)
T=T.drop(columns=['tri_sek','returntype']).rename(columns={'last_date':'tri_date'})
assert not T.duplicated(['performanceId','ym']).any()
V=V.merge(T,on=['performanceId','ym'],how='left',validate='1:1')
V['tri_present']=V.tri_present.fillna(False)
V['date_gap']=(pd.to_datetime(V.last_date)-pd.to_datetime(V.tri_date)).abs().dt.days
V['date_ok']=V.date_gap.le(4)&V.last_date.str.slice(0,7).eq(V.ym)&V.tri_date.str.slice(0,7).eq(V.ym)
V['TNA_present']=V.tnaclass.gt(0)&V.tnafund.gt(0)&np.isfinite(V.tnaclass)&np.isfinite(V.tnafund)
V['currency_ok']=V.ccy_class.eq('SEK')&V.ccy_fund.eq('SEK')
rec=[]
for (fid,ym),d in V.groupby(['fundid','ym']):
 den=d.tnafund.median();ratio=d.tnaclass.sum(min_count=1)/den if den>0 else np.nan
 spread=(d.tnafund.max()-d.tnafund.min())/den if den>0 else np.nan
 rec.append(dict(fundid=fid,ym=ym,base_ok=bool(d.TNA_present.all() and d.currency_ok.all() and d.last_date.nunique()==1 and spread<.001 and .99<=ratio<=1.01),tri_ok=bool(d.tri_present.all() and d.date_ok.all()),classes=';'.join(sorted(d.performanceId)),nclasses=len(d)))
Q=pd.DataFrame(rec);Q['endpoint_ok']=Q.base_ok&Q.tri_ok
good={};rows=[]
for rev,d in G.groupby('review'):
 end=pd.Period(d.q0.iloc[0],freq='M');months={str(x) for x in pd.period_range(end-24,end,freq='M')};good[rev]=set()
 hist=Q[Q.ym.isin(months)];s=hist.groupby('fundid').agg(n=('ym','nunique'),nbase=('base_ok','sum'),nok=('endpoint_ok','sum'),classsets=('classes','nunique'))
 for f in d.itertuples():
  h=s.loc[f.f0] if f.exact_map and f.f0 in s.index else None
  endpoint_pass=h is not None and h.n==25 and h.nok==25
  stable=endpoint_pass and h.classsets==1
  x=V[V.fundid.eq(f.f0)&V.ym.isin(months)] if stable else V.iloc[:0]
  # Data master is current: dates establish only provisional continuity, not certified merger history.
  inc=pd.to_datetime(x.inceptiondate,errors='coerce');obs=pd.to_datetime(x.obsoletedate,errors='coerce')
  dates=bool(stable and inc.notna().all() and inc.le(pd.Period(min(months)).end_time).all() and (obs.isna()|obs.gt(pd.Period(max(months)).end_time)).all())
  ok=bool(endpoint_pass and stable and dates)
  if ok:good[rev].add(f.fund_id)
  rows.append(dict(review=rev,fund_id=f.fund_id,fundid=f.f0,exact_stable_endpoint_map=f.exact_map,month_count=0 if h is None else int(h.n),capital_reconciled_endpoints=0 if h is None else int(h.nbase),complete_TNA_TRI_endpoints=0 if h is None else int(h.nok),stable_classes=bool(stable),class_life_dates_ok=dates,provisional25endpoint_pass=ok))
H=pd.DataFrame(rows);H.to_csv(O/'monthly_source_fund_feasibility.csv',index=False)
# Independently use the exact audited event-fund-role support, then raw FI quantities as coverage weights.
L=pd.read_csv(inputs[7],dtype={'fund_id':str},usecols=['event_id','review','type','role','fund_id']);L=L[L.review.le('2023H2')]
S=pd.read_csv(inputs[6]);S=S[S.event_id.isin(L.event_id)]
ids=set(S.aliases.str.split(';').explode());dates=set(S.q0)|set(S.q1);parts=[]
cols=['ISIN-kod_instrument','Kvartalsslut','Fond_institutnummer','Antal']
for c in pd.read_csv(inputs[9],usecols=cols,dtype={'Fond_institutnummer':str},chunksize=500000):
 parts.append(c[c['ISIN-kod_instrument'].isin(ids)&c.Kvartalsslut.isin(dates)])
raw=pd.concat(parts,ignore_index=True);raw['Antal']=pd.to_numeric(raw.Antal,errors='coerce')
coverage=[]
for a in S.itertuples():
 pop=set(L.loc[L.event_id.eq(a.event_id)&L.role.eq(a.role),'fund_id']);mapped=set(G.loc[G.review.eq(a.review)&G.exact_map,'fund_id']);eligible=good[a.review]
 d=raw[raw['ISIN-kod_instrument'].isin(a.aliases.split(';'))&raw.Fond_institutnummer.isin(pop)]
 for endpoint,date in [('q0',a.q0),('q1',a.q1)]:
  q=d[d.Kvartalsslut.eq(date)].groupby('Fond_institutnummer').Antal.sum(min_count=1);assert q.ge(0).all()
  den=q.sum();coverage.append(dict(event_id=a.event_id,review=a.review,type=a.type,role=a.role,endpoint=endpoint,population_funds=len(pop),exact_mapped_funds=len(pop&mapped),history_eligible_funds=len(pop&eligible),positive_owners=int(q.gt(0).sum()),mapped_positive_owners=int(q[q.index.isin(mapped)].gt(0).sum()),history_positive_owners=int(q[q.index.isin(eligible)].gt(0).sum()),mapped_capital_fraction=q[q.index.isin(mapped)].sum()/den if den>0 else np.nan,history_capital_fraction=q[q.index.isin(eligible)].sum()/den if den>0 else np.nan))
COV=pd.DataFrame(coverage);COV.to_csv(O/'event_role_capital_coverage.csv',index=False)
aggreg=COV.groupby(['review','type','role','endpoint']).agg(events=('event_id','size'),mapped_mean=('mapped_capital_fraction','mean'),mapped_min=('mapped_capital_fraction','min'),history_mean=('history_capital_fraction','mean'),history_min=('history_capital_fraction','min'),history_median=('history_capital_fraction','median')).reset_index();aggreg.to_csv(O/'capital_coverage_summary.csv',index=False)
# Raw new download: field presence only. Keep pre2024 and aggregate daily flags byclass/month.
with zipfile.ZipFile(inputs[3]) as z:
 with z.open(z.namelist()[0]) as f:
  Z=pd.read_csv(f,sep=';',usecols=['performanceId','date','classcurrencyiso','fundcurrencyiso','netflowclass','netflowfund','tnaclass','tnafund'],dtype=str)
Z=Z[Z.date.lt('2024-01-01')].copy();Z['ym']=Z.date.str.slice(0,7)
for col in ['netflowclass','netflowfund','tnaclass','tnafund']:
 Z[col+'_present']=Z[col].notna()&~Z[col].isin(['','NULL','NaN','nan','NA']);Z=Z.drop(columns=col)
Z=Z.merge(P[['performanceId','fundid']],on='performanceId',how='left',validate='m:1')
ZM=Z.groupby(['fundid','performanceId','ym'],dropna=False).agg(ndays=('date','nunique'),nfclass_n=('netflowclass_present','sum'),nffund_n=('netflowfund_present','sum'),tnaclass_n=('tnaclass_present','sum'),tnafund_n=('tnafund_present','sum')).reset_index()
ZM.to_csv(O/'zip_month_field_presence.csv',index=False)
ZQ=[]
for rev,d in G.groupby('review'):
 end=pd.Period(d.q0.iloc[0],freq='M');months={str(x) for x in pd.period_range(end-23,end,freq='M')};z=ZM[ZM.ym.isin(months)]
 zs=z.groupby('fundid').agg(months=('ym','nunique'),months_with_any_fund_nf=('nffund_n',lambda a:int((a>0).sum())))
 fullclass=z[z.ndays.eq(z.nffund_n)&z.ndays.gt(0)].groupby(['fundid','performanceId']).ym.nunique();fids=set(fullclass[fullclass.eq(24)].index.get_level_values('fundid'))
 ZQ.append(dict(review=rev,exact_mapped_funds_in_raw_zip=int((d.exact_map&d.f0.isin(set(Z.fundid))).sum()),funds_with_one_class_complete_recorded_fund_NF24months=int((d.exact_map&d.f0.isin(fids)).sum())))
SUMMARY={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fund_source_coverage':H.groupby('review')[['exact_stable_endpoint_map','provisional25endpoint_pass']].sum().to_dict('index'),'source25_endpoints_not_final_identity_validation':True,'positive_TRI_values_not_used_as_outcomes':True,'no_flows_or_covariance_computed':True,'zip_pre2024_rows':len(Z),'zip_distinct_classes':Z.performanceId.nunique(),'zip_distinct_funds':Z.fundid.nunique(),'zip_dates':[Z.date.min(),Z.date.max()],'zip_allmissing_nf_class_months':int(ZM.nfclass_n.eq(0).sum()),'zip_allmissing_nf_fund_months':int(ZM.nffund_n.eq(0).sum()),'zip_class_months':len(ZM),'zip_review_coverage':ZQ,'capital_coverage_quantities_use_exact_audited_4role_support':True,'ownership_events':L.event_id.nunique(),'limitation':'Metadata only. Class dates and same ISIN at endpoints do not certify historic identity, shareclass migrations, mergers or complete calendar reports. Four-day tolerance is provisional; monthly endpoint return must represent the matching NAV date. Coverage is within observed Swedish FI funds only, not full stock ownership.'}
(O/'SOURCE_FEASIBILITY.json').write_text(json.dumps(SUMMARY,indent=2));print(json.dumps(SUMMARY,indent=2));print(aggreg[aggreg.role.eq('event')].to_string(index=False))
