"""Final declared listing repair. No outcome-driven matching or replacement."""
from pathlib import Path
import os
import sys,json
import pandas as pd,numpy as np
ROOT=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
O=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code/build'))
import robusthet_hela as b
P=b.Panel(ROOT,ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet')
E=pd.read_csv(ROOT/'output/omxsb_replication_2007/events_car.csv',parse_dates=['AD','ED'])
V=E.groupby('review_cycle').agg(AD=('AD','first'),ED=('ED','first')).sort_values('AD').reset_index()
V['k']=np.arange(len(V));km=dict(zip(V.review_cycle,V.k));E['k']=E.review_cycle.map(km)
CENSUS=pd.read_csv(ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
keys={(x.RIC,km[x.review_cycle]) for x in CENSUS.itertuples() if pd.notna(x.RIC) and x.review_cycle in km}
keys|=set(zip(E.RIC,E.k))
U=pd.read_csv(O.parent/'eligible_pool/review_RIC_control_pool.csv')
assert not U.duplicated(['review','ric']).any()
rows=[];coverage=[];selections=[];quote_log=[]
for r in V.itertuples():
    if r.AD.year<2017:continue
    iad=int(P.pos[r.AD]);ied=int(P.pos[r.ED]);u=U[U.review==r.review_cycle].copy()
    lookup=u.set_index('ric').to_dict('index')
    current_rics={ric for ric,k in keys if k==r.k}
    current_issuers={lookup[ric]['company_code'] for ric in current_rics if ric in lookup}
    past_issuers={lookup[ric]['company_code'] for ric,k in keys if k==r.k-1 and ric in lookup}
    ce=[]
    for ric,info in lookup.items():
        c=P.covariates(ric,iad)
        if c is None:continue
        j=P.columns[ric]
        c.update(issuer=str(info['company_code']),isin=info['isin'],source_url=info['source_url'],
                 pre_observed=int(100-(P.cn[iad-1,j]-P.cn[iad-101,j])))
        ce.append(c)
    A=pd.DataFrame(ce)
    if A.empty:raise ValueError('No covariate-valid main stocks '+r.review_cycle)
    # Canonical quote picked by pre-outcome data only, before reading any event outcome.
    A=A.sort_values(['isin','pre_observed','ric'],ascending=[True,False,True],kind='stable')
    canon=A.drop_duplicates('isin').copy()
    for x in A.itertuples():quote_log.append(dict(review=r.review_cycle,ric=x.ric,isin=x.isin,pre_observed=x.pre_observed,selected_quote=x.ric in set(canon.ric)))
    candidates=canon[~canon.issuer.isin(current_issuers|past_issuers)&~canon.ric.map(lambda ric:b.past_or_current_event(ric,r.k,keys))].copy()
    ee=[]
    for e in E[E.k==r.k].itertuples():
        cov=P.covariates(e.RIC,iad)
        status='ok' if (e.RIC in lookup and cov is not None) else ('unresolved_dated_identity_or_listing' if e.RIC not in lookup else 'missing_pre_covariates')
        coverage.append(dict(event_id=e.event_id,review=r.review_cycle,type=e.type,ric=e.RIC,status=status,eligible_pool_RIC=len(u),candidate_instruments=len(candidates)))
        if status!='ok':continue
        cov.update(issuer=str(lookup[e.RIC]['company_code']),event_id=e.event_id,type=e.type,review=r.review_cycle,AD=e.AD,ED=e.ED)
        ee.append(cov)
    if not ee:continue
    ee=pd.DataFrame(ee);scale=pd.concat([candidates[['precar','log_mcap']],ee[['precar','log_mcap']]])
    mu,sd=scale.mean(),scale.std()
    for e in ee.to_dict('records'):
        chosen=b.choose_matches(candidates,e,mu,sd,3)
        row=e.copy();row['chosen_controls']=len(chosen)
        for j,c in enumerate(chosen.to_dict('records'),1):
            assert c['issuer']!=e['issuer']
            row.update({f'c{j}_ric':c['ric'],f'c{j}_issuer':c['issuer'],f'c{j}_distance':c['distance'],f'c{j}_precar':c['precar'],f'c{j}_log_mcap':c['log_mcap']})
            selections.append(dict(event_id=e['event_id'],review=r.review_cycle,role=f'c{j}',ric=c['ric'],issuer=c['issuer'],isin=c['isin'],distance=c['distance'],source_url=c['source_url']))
        assert chosen.issuer.nunique()==len(chosen)
        # Outcomes are first accessed here, AFTER all identities and ranks are frozen.
        for h in [1,20,60,100]:
            row[f'event_{h}']=P.car(e['ric'],iad-1,ied+h)
            vals=[]
            for j,c in enumerate(chosen.to_dict('records'),1):
                row[f'c{j}_{h}']=P.car(c['ric'],iad-1,ied+h);vals.append(row[f'c{j}_{h}'])
            row[f'diff3_{h}']=b.paired_difference(row[f'event_{h}'],vals,3)
        row['common100']=all(np.isfinite(row[f'diff3_{h}']) for h in [1,20,60,100])
        rows.append(row)
    print(r.review_cycle,'events',len(ee),'candidates',len(candidates),flush=True)
D=pd.DataFrame(rows);D.to_csv(O/'event_paths.csv',index=False)
pd.DataFrame(coverage).to_csv(O/'coverage.csv',index=False)
pd.DataFrame(selections).to_csv(O/'selected_controls.csv',index=False)
pd.DataFrame(quote_log).to_csv(O/'quote_choices.csv',index=False)
out=[];balance=[]
for typ in ['addition','deletion']:
    for support in ['available','common100']:
        q=D[D.type==typ].copy()
        if support=='common100':q=q[q.common100]
        for label,ha,hb in [('level_1',1,None),('level_20',20,None),('level_60',60,None),('level_100',100,None),('change_20_100',100,20)]:
            if support=='available' and hb is not None:continue
            y=q[f'diff3_{ha}'] if hb is None else q[f'diff3_{ha}']-q[f'diff3_{hb}']
            f=b.mean_inference(y,q.review,9999,f'eligible_rematch/{typ}/{support}/{label}');f.update(type=typ,support=support,contrast=label);out.append(f)
        for feature in ['precar','log_mcap']:
            good=q[q.diff3_1.notna()];x=good[feature];y=good[[f'c{i}_{feature}' for i in [1,2,3]]].mean(axis=1)
            balance.append(dict(type=typ,support=support,feature=feature,N=len(good),event_mean=x.mean(),control_mean=y.mean(),event_median=x.median(),control_median=y.median(),standardized_difference=(x.mean()-y.mean())/np.sqrt((x.var()+y.var())/2)))
R=pd.DataFrame(out);R.to_csv(O/'results.csv',index=False);pd.DataFrame(balance).to_csv(O/'balance.csv',index=False)
inputs=[O/'ANALYSIS_DECISIONS.txt',Path(__file__),O.parent/'eligible_pool/review_RIC_control_pool.csv',ROOT/'output/omxsb_replication_2007/events_car.csv',ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',ROOT/'code/build/robusthet_hela.py']
(O/'metadata.json').write_text(json.dumps(dict(exploratory=True,no_future_events_excluded=True,no_outcome_replacement=True,main_list_only_not_full_index_eligibility=True,hashes={str(p):b.file_hash(p) for p in inputs}),indent=2))
print(R[['type','support','contrast','N','G','estimate_pp','ci_lo','ci_hi','p_wild']].to_string(index=False))
