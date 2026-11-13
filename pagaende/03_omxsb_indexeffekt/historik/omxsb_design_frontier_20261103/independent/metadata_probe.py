"""Coverage/definition probe only. Never loads NF values, returns or stock outcomes."""
from pathlib import Path
import datetime,json,hashlib
import numpy as np
import pandas as pd
R=Path('/Users/ludviguvang/dev/financethesis');O=Path(__file__).resolve().parent
paths=[R/'data/raw/shof/fundmaster.xlsx',R/'data/derived/shof_monthly/shof_valuations_monthly.csv',R/'output/omxsb_mechanism_frontier_20261102/ownership/fund_metadata_classification.csv',R/'output/omxsb_mechanism_frontier_20261102/ownership/decomp_fund_groups.csv',R/'data/raw/shof/shof_field_definitions.txt',R/'code/build/shof_monthly.py']
lock={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only exact identity joins, dates, currencies, daily nonmissing counters and TNA coverage through2023; no NF values/returns/outcomes/covariances. Candidate feasibility, not analysis selection.',
      'metadata_gate':'SEK fund and every observed classSEK; classNF_n=recordedndays>0; common lastdate; repeatedfundTNA range/median<0.001; sumclassTNA/fundTNA0.99..1.01. These are provisional source gates, not economic thresholds.',
      'inputs':{str(p):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}}
(O/'METADATA_LOCK.json').write_text(json.dumps(lock,indent=2))
M=pd.read_excel(paths[0],usecols=['performanceid','secid','fundid','ISIN','currencyid','inceptiondate','obsoletedate','fundname'])
F=pd.read_csv(paths[2],dtype={'fund_id':str},usecols=['quarter','fund_id','fund_isin'])
F=F[F.quarter.le('2023-12-31')].dropna(subset=['fund_isin'])
G=pd.read_csv(paths[3],dtype={'fund_id':str},usecols=['review','fund_id','q0','q1'])
G=G[G.q1.le('2023-12-31')]
F=F.merge(G[['fund_id','q0']].drop_duplicates(),left_on=['fund_id','quarter'],right_on=['fund_id','q0'])
links=F.merge(M[['ISIN','fundid']].dropna().drop_duplicates(),left_on='fund_isin',right_on='ISIN',how='left')
links=links.groupby(['fund_id','quarter'],as_index=False).agg(n_fundids=('fundid','nunique'),fundid=('fundid','first'))
valid=links[links.n_fundids.eq(1)].copy()
badpids=set(M.loc[M.performanceid.duplicated(keep=False)&M.groupby('performanceid').fundid.transform('nunique').gt(1),'performanceid'])
pidmap=M[~M.performanceid.isin(badpids)][['performanceid','fundid']].drop_duplicates()
V=pd.read_csv(paths[1],usecols=['performanceId','ym','ccy_class','ccy_fund','last_date','tnaclass','tnafund','ndays','nf_class_n'])
V=V[V.ym.le('2023-12')].merge(pidmap,left_on='performanceId',right_on='performanceid',validate='m:1')
V=V[V.fundid.isin(valid.fundid)]
assert not V.duplicated(['performanceId','ym']).any()
V['recorded_class_NF_complete']=V.ndays.gt(0)&V.nf_class_n.eq(V.ndays)
V['all_missing_class_NF']=V.nf_class_n.eq(0)
records=[]
for (fid,ym),d in V.groupby(['fundid','ym']):
    den=float(d.tnafund.median());ratio=float(d.tnaclass.sum(min_count=1)/den) if den>0 else np.nan
    capspread=float((d.tnafund.max()-d.tnafund.min())/den) if den>0 else np.nan
    complete=bool(d.recorded_class_NF_complete.all());ccyok=bool(d.ccy_class.eq('SEK').all()&d.ccy_fund.eq('SEK').all());dateok=d.last_date.nunique()==1
    ok=complete and ccyok and dateok and capspread<.001 and .99<=ratio<=1.01
    records.append(dict(fundid=fid,ym=ym,n_observed_classes=len(d),class_TNA_to_fund_TNA=ratio,repeated_fund_TNA_spread=capspread,
                        all_recorded_class_NF_complete=complete,all_classes_SEK=ccyok,common_lastdate=dateok,provisional_gate_pass=ok))
Q=pd.DataFrame(records)
out=[]
for rev,d in G.groupby('review'):
    # Review metadata uses pre-quarter q0. Hold window ends there, not in an event month.
    end=pd.Period(d.q0.iloc[0],freq='M');months={str(x) for x in pd.period_range(end-23,end,freq='M')}
    lm=valid[valid.quarter.eq(d.q0.iloc[0])].set_index('fund_id')
    sub=Q[Q.ym.isin(months)]
    hist=sub[sub.provisional_gate_pass].groupby('fundid').ym.nunique()
    matched=set(d.fund_id)&set(lm.index)
    good=[f for f in matched if hist.get(lm.loc[f,'fundid'],0)==24]
    out.append(dict(review=rev,ownership_funds=d.fund_id.nunique(),exact_unique_master_matches=len(matched),funds_with24_complete_prequarter_months=len(good),history_start=min(months),history_end=max(months)))
P=pd.DataFrame(out);P.to_csv(O/'pre2024_mapping_history_coverage.csv',index=False)
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'not_an_economic_result':True,'no_NF_values_loaded':True,'no_return_values_loaded':True,
 'FI_fund_quarters':len(links),'exact_single_fundid_matches':int(links.n_fundids.eq(1).sum()),'unmatched':int(links.n_fundids.eq(0).sum()),'ambiguous':int(links.n_fundids.gt(1).sum()),
 'matched_distinct_FI_funds':valid.fund_id.nunique(),'matched_distinct_Morningstar_funds':valid.fundid.nunique(),
 'observed_matched_class_months_pre2024':len(V),'allmissing_classNF_months':int(V.all_missing_class_NF.sum()),'partiallymissing_classNF_months':int((~V.all_missing_class_NF&~V.recorded_class_NF_complete).sum()),
 'matched_fund_months':len(Q),'provisional_complete_fund_months':int(Q.provisional_gate_pass.sum()),
 'raw_daily_valuation_csvs_present':len(list((R/'data/raw/shof/Valuations').glob('*.csv'))),
 'limitation':'Current master exactISIN joins are not yet dated fund-identity certification. Observed-class TNA reconciliation is coverage evidence, not proof all historicclasses are represented. Recorded daily counters do not prove all calendar observations available. No capital-weighted coverage or covariance estimated.'}
(O/'METADATA_COVERAGE.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(P.to_string(index=False))
