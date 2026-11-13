"""Second-agent independent review. No original functions imported or executed."""
from pathlib import Path
import datetime, json, hashlib, math
import numpy as np
import pandas as pd
from scipy.stats import t

O=Path(__file__).resolve().parent
A=O.parent.parent/'ownership_capital'
R=Path('/Users/ludviguvang/dev/financethesis')
OLD=R/'output/omxsb_mechanism_frontier_20261102/ownership'
DQ=R/'output/omxsb_open_questions_20261102/demand_quarter'
inputs=[]
def read(p,**kw):inputs.append(p);return pd.read_csv(p,**kw)

L=read(A/'normalized_fund_role_contributions.csv.gz',dtype={'fund_id':str})
assert not L.duplicated(['event_id','role','fund_id']).any()
K=read(A/'event_feasibility_gate.csv');K=K[K.gate_pass]
assert not K.event_id.duplicated().any() and set(L.event_id)==set(K.event_id)
S=read(OLD/'security_role_gate.csv');S=S[S.event_id.isin(K.event_id)]
assert not S.duplicated(['event_id','role']).any()
assert S.groupby('event_id').role.apply(lambda x:set(x)=={'event','c1','c2','c3'}).all()
assert S.groupby('event_id').ric.nunique().eq(4).all()
assert S.groupby('event_id').q0.nunique().eq(1).all() and S.groupby('event_id').q1.nunique().eq(1).all()
assert L.groupby('event_id').review.nunique().eq(1).all()
G=read(A/'security_feasibility_gate.csv').set_index(['review','ric'])
B=read(A/'invalid_fund_role_pairs.csv',dtype={'fund_id':str})
F=read(OLD/'decomp_fund_roles.csv.gz',dtype={'fund_id':str});F=F[F.event_id.isin(K.event_id)]
assert not F.duplicated(['event_id','role','fund_id']).any()
FM=read(OLD/'decomp_fund_groups.csv',dtype={'fund_id':str}).set_index(['review','fund_id'])
M=read(DQ/'raw_fund_report_metadata.csv',dtype={'Fond_institutnummer':str}).set_index(['Fond_institutnummer','Kvartalsslut'])
assert not M.index.duplicated().any()
saved_support=read(A/'fund_support.csv',dtype={'excluded_fund_ids':str}).set_index('event_id')
support=[];goodmap={};missing=0;merger=0;unitbad=0;zero_instruments_61031=0
for eid,rs in S.groupby('event_id'):
    orig=F[F.event_id.eq(eid)];roles={r:set(z.fund_id) for r,z in orig.groupby('role')}
    population=roles['event'];assert all(v==population for v in roles.values())
    review=rs.review.iloc[0];q0=rs.q0.iloc[0];q1=rs.q1.iloc[0]
    invalid=set()
    for x in rs.itertuples():
        assert bool(G.loc[(review,x.ric),'gate_pass'])
        invalid.update(B.loc[(B.review==review)&(B.ric==x.ric),'fund_id'])
    eligible=set()
    for f in population:
        reports_ok=all((f,q) in M.index and M.loc[(f,q),'actual_instrument_rows']>0 for q in [q0,q1])
        if not reports_ok:
            missing+=1
            if f=='61031' and review=='2020H2':zero_instruments_61031+=1
        merged=(f=='51437' and review=='2022H1')
        merger+=int(merged);unitbad+=int(f in invalid)
        if reports_ok and not merged and f not in invalid:eligible.add(f)
    actual={r:set(z.fund_id) for r,z in L[L.event_id.eq(eid)].groupby('role')}
    assert len(actual)==4 and all(v==eligible for v in actual.values())
    ex=population-eligible
    oldex=set(str(saved_support.loc[eid,'excluded_fund_ids']).split(';'))-{'nan',''}
    assert ex==oldex
    assert len(eligible)==saved_support.loc[eid,'retained_funds']
    assert len(population)==saved_support.loc[eid,'original_funds']
    goodmap[eid]=eligible
    support.append(dict(event_id=eid,review=review,original=len(population),retained=len(eligible),excluded=len(ex),four_roles_same_population=True))
pd.DataFrame(support).to_csv(O/'independent_support_checks.csv',index=False)

# Independent raw quantity-to-normalized ledger check. The source is read only;
# raw holdings amounts are not copied to this audit folder.
names={'Fond_institutnummer':'fund_id','Kvartalsslut':'quarter','ISIN-kod_instrument':'isin','Antal':'q','Marknadsvärde_instrument':'value','Valuta':'currency','Tillgångsslag_enligt_LVF_5_kap':'asset'}
rawpath=R/'data/derived/fi/fi_holdings_long.csv.gz';inputs.append(rawpath)
ids=set(S.aliases.str.split(';').explode());dates=set(S.q0)|set(S.q1);parts=[]
for d in pd.read_csv(rawpath,usecols=list(names),dtype={'Fond_institutnummer':str},chunksize=200000):
    d=d.rename(columns=names);parts.append(d[d['isin'].isin(ids)&d.quarter.isin(dates)])
H=pd.concat(parts,ignore_index=True)
H.q=pd.to_numeric(H.q,errors='coerce');H.value=pd.to_numeric(H.value,errors='coerce')
ppath=R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet';inputs.append(ppath)
P=pd.read_parquet(ppath,columns=['ric','date','mcap','source']);P=P[P.ric.isin(S.ric)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
CA=read(R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',parse_dates=['action_date'])
prior=read(DQ/'events_locked.csv').set_index(['review_cycle','RIC'])
cache={};split_checks=[]
for (review,ric),ss in S.groupby(['review','ric']):
    x=ss.iloc[0];z=H[H['isin'].isin(x.aliases.split(';'))&H.quarter.isin([x.q0,x.q1])]
    q=z.groupby(['fund_id','quarter']).q.sum(min_count=1)
    zv=z[z.quarter.eq(x.q1)&z.currency.eq('SEK')&z.asset.eq('ÖverlåtbartVärdepapper')&z.q.gt(0)&z.value.gt(0)]
    price=np.median((zv.value/zv.q).to_numpy())
    cap=P[P.ric.eq(ric)&P.date.le(pd.Timestamp(x.q1))&P.mcap.gt(0)].iloc[-1]
    assert cap.source=='tr' and (pd.Timestamp(x.q1)-cap.date).days<=7
    factor=float(G.loc[(review,ric),'factor'])
    acts=CA[CA.RIC.eq(ric)&CA.kind.eq('ordinary_split')&CA.action_date.gt(pd.Timestamp(x.q0))&CA.action_date.le(pd.Timestamp(x.q1))]
    registered=float(acts.factor.prod())
    inherited=(review,ric) in prior.index
    expected=float(prior.loc[(review,ric),'factor']) if inherited else registered
    assert factor==expected
    split_checks.append(dict(review=review,ric=ric,factor=factor,registered_same_quarter_factor=registered,inherited_gate=inherited,source_rows=len(acts),factor_matches_declared_source=True))
    cache[(review,ric)]=(q,float(price),float(cap.mcap),factor)
pd.DataFrame(split_checks).to_csv(O/'independent_split_checks.csv',index=False)

raw_errors=[];raw_units=[];zero_endpoints=0;group_consistency=0;metadata_isin_variation=[]
lookup=L.set_index(['event_id','role','fund_id'])
origlookup=F.set_index(['event_id','role','fund_id'])
for x in S.itertuples():
    q,price,cap,factor=cache[(x.review,x.ric)]
    raw_total=0.;component_total=0.
    for f in sorted(goodmap[x.event_id]):
        qb=float(q.get((f,x.q0),0));qa=float(q.get((f,x.q1),0))
        assert np.isfinite(qb+qa) and qb>=0 and qa>=0
        zero_endpoints+=int(qb==0)+int(qa==0)
        status=('new' if qb==0 and qa>0 else 'exiting' if qb>0 and qa==0 else 'continuing' if qb>0 and qa>0 else 'neither')
        saved=lookup.loc[(x.event_id,x.role,f)];old=origlookup.loc[(x.event_id,x.role,f)]
        assert old.own_before==int(qb>0) and old.own_after==int(qa>0)
        assert saved.component==status
        assert saved.group==FM.loc[(x.review,f),'group']==old.group
        group_consistency+=1
        val=100*price/cap*(qa-factor*qb)
        raw_errors.append(abs(val-saved.pp));raw_total+=val
        if status!='neither':component_total+=val
        before_id=M.loc[(f,x.q0),'fund_isin'];after_id=M.loc[(f,x.q1),'fund_isin']
        if str(before_id)!=str(after_id):metadata_isin_variation.append((x.event_id,f,str(before_id),str(after_id)))
    raw_units.append(dict(event_id=x.event_id,role=x.role,raw_normalized_total=raw_total,raw_components_total=component_total,component_identity_error=abs(raw_total-component_total)))
assert max(raw_errors)<1e-10
pd.DataFrame(raw_units).to_csv(O/'independent_role_totals.csv',index=False)
pd.DataFrame(metadata_isin_variation,columns=['event_id','fund_id','before_isin_metadata','after_isin_metadata']).drop_duplicates().to_csv(O/'raw_metadata_fund_isin_variation.csv',index=False)

# Rebuild every summary from the normalized fund-role checkpoint; it has just
# been verified against the raw quantities with independently reconstructed support.
base_groups=sorted(L.group.unique());rows=[]
for eid,ds in L.groupby('event_id'):
    for group in base_groups+['ALL','OMXSB_family']:
        d=ds if group=='ALL' else ds[ds.group.str.startswith('OMXSB_')] if group=='OMXSB_family' else ds[ds.group==group]
        roles={}
        for role in ['event','c1','c2','c3']:
            r=d[d.role==role]
            v={c:math.fsum(r.loc[r.component.eq(c),'pp']) for c in ['new','continuing','exiting']}
            v['total']=math.fsum(r.pp);v['preexisting']=v['continuing']+v['exiting'];v['new_minus_preexisting']=v['new']-v['preexisting']
            assert abs(v['total']-(v['new']+v['continuing']+v['exiting']))<1e-10
            roles[role]=v
        row=dict(event_id=eid,review=ds.review.iloc[0],type=ds.type.iloc[0],group=group)
        for metric in roles['event']:
            row['event_'+metric]=roles['event'][metric]
            row['control_'+metric]=math.fsum(roles[r][metric] for r in ['c1','c2','c3'])/3
            row['matched_'+metric]=row['event_'+metric]-row['control_'+metric]
        rows.append(row)
EC=pd.DataFrame(rows);savedEC=read(A/'event_component_results.csv')
metrics=[c for c in EC if c not in ['event_id','review','type','group']]
jj=EC.merge(savedEC,on=['event_id','review','type','group'],suffixes=('_ind','_saved'),validate='1:1')
assert len(jj)==len(savedEC)==185*7
eventerr=max(float((jj[c+'_ind']-jj[c+'_saved']).abs().max()) for c in metrics)
assert eventerr<1e-10
rev=EC.groupby(['type','group','review'])[metrics].mean().reset_index()
rev.to_csv(O/'independent_review_components.csv',index=False)
ss=[]
for (typ,group),z in rev.groupby(['type','group']):
    for metric in metrics:
        y=z[metric].to_numpy();n=len(y);mean=math.fsum(y)/n
        variance=math.fsum((y-mean)**2)/(n*(n-1));se=math.sqrt(variance);c=t.ppf(.975,n-1)
        ss.append(dict(type=typ,group=group,metric=metric,mean_pp=mean,se_pp=se,ci95_low=mean-c*se,ci95_high=mean+c*se,G_reviews=n,N_events=EC[(EC.type==typ)&(EC.group==group)].shape[0]))
SU=pd.DataFrame(ss);savedSU=read(A/'summary.csv')
su=SU.merge(savedSU,on=['type','group','metric'],suffixes=('_ind','_saved'),validate='1:1')
summaryerr=max(float((su[c+'_ind']-su[c+'_saved']).abs().max()) for c in ['mean_pp','se_pp','ci95_low','ci95_high','G_reviews','N_events'])
assert summaryerr<1e-10
SU[(SU.group=='ALL')&SU.metric.str.startswith('matched')].to_csv(O/'independent_headline_summary.csv',index=False)
covs=[]
for typ,z in rev[rev.group.eq('ALL')].groupby('type'):
    Y=z[['matched_new','matched_continuing','matched_exiting']].to_numpy();n=len(Y);dev=Y-Y.mean(axis=0)
    V=(dev.T@dev)/(n*(n-1))
    for i,a in enumerate(['matched_new','matched_continuing','matched_exiting']):
        for j,b in enumerate(['matched_new','matched_continuing','matched_exiting']):covs.append(dict(type=typ,row=a,column=b,covariance_of_mean=V[i,j]))
    if typ=='addition':
        weight=np.array([1.,-1.,-1.]);primaryse=float(np.sqrt(weight@V@weight))
        primary=SU[(SU.type=='addition')&(SU.group=='ALL')&(SU.metric=='matched_new_minus_preexisting')].iloc[0]
        assert abs(primaryse-primary.se_pp)<1e-12
CV=pd.DataFrame(covs);savedCV=read(A/'component_covariance.csv');cc=CV.merge(savedCV,on=['type','row','column'],suffixes=('_ind','_saved'),validate='1:1')
coverr=float((cc.covariance_of_mean_ind-cc.covariance_of_mean_saved).abs().max());assert coverr<1e-12
CV.to_csv(O/'independent_covariance.csv',index=False)
results=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),all_numeric_checks_pass=True,
    events=len(K),additions=int((K.type=='addition').sum()),deletions=int((K.type=='deletion').sum()),reviews=K.review.nunique(),
    unique_normalized_fund_role_rows=len(L),zero_endpoints_in_verified_report_support=zero_endpoints,
    no_report_or_empty_report_fund_event_exclusions=missing,excluded61031_2020H2_event_count=zero_instruments_61031,
    known_merger_51437_2022H1_event_count=merger,unit_invalid_fund_event_count=unitbad,
    max_raw_fund_pp_error=max(raw_errors),event_component_cells=len(jj)*len(metrics),max_event_component_error=eventerr,
    summary_cells=len(su)*6,max_summary_error=summaryerr,max_covariance_error=coverr,primary_se_from_covariance=primaryse,
    primary_estimate=float(primary.mean_pp),primary_low=float(primary.ci95_low),primary_high=float(primary.ci95_high),
    raw_fund_isin_metadata_variation_rows=len(metadata_isin_variation),
    nonunit_samequarter_security_factors=sum(z['factor']!=1 for z in split_checks),
    inherited_measurement_limits='Original alias/identity/source-completeness gates are inherited; this audit verifies their actual use and raw amounts, not independently collects all original XML reports.',
    source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in set(inputs)})
(O/'VERIFICATION.json').write_text(json.dumps(results,indent=2));print(json.dumps({k:v for k,v in results.items() if k!='source_hashes'},indent=2))
