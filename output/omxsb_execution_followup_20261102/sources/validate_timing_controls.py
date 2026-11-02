"""Independent arithmetic audit only: frozen AD+1 vs ED-1 comparison, no new design."""
from pathlib import Path
import hashlib, json, math
import numpy as np
import pandas as pd
import statsmodels.api as sm
ROOT=Path('/Users/ludviguvang/dev/financethesis')
OUT=Path(__file__).resolve().parent
BASE=ROOT/'output/omxsb_execution_followup_20261102/timing'
CP=ROOT/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv'
LOCK=json.loads((BASE/'ADDENDUM_FIXED_CONTROLS.json').read_text())
assert hashlib.sha256(CP.read_bytes()).hexdigest()==LOCK['control_file_sha256']
D=pd.read_csv(BASE/'fixed_controls/event_comparisons.csv',parse_dates=['early_date','late_date'])
C=pd.read_csv(CP,usecols=['event_id','ric','issuer','chosen_controls']+[f'c{k}_{field}' for k in (1,2,3) for field in ('ric','issuer')])
E=pd.read_csv(BASE/'v2_announced/event_comparisons.csv')
assert not D.event_id.duplicated().any()
assert set(D.event_id)==set(E.loc[E.delay.eq(1)&E.status.eq('ok'),'event_id'])
V=D[D.control_status.eq('ok')].copy()
assert not V.cancelled.any()
assert (V.chosen_controls==3).all()
CV=V.merge(C,on='event_id',suffixes=('','_frozen'),validate='one_to_one')
assert (CV.RIC==CV.ric).all()
assert all((CV[f'c{k}_ric']==CV[f'c{k}_ric_frozen']).all() for k in (1,2,3))
self_ric=[]; duplicate_ric=[]; self_issuer=[];duplicate_issuer=[]
for x in CV.to_dict('records'):
    controls=[x[f'c{k}_ric'] for k in (1,2,3)]
    issuers=[x[f'c{k}_issuer'] for k in (1,2,3)]
    if x['RIC'] in controls:self_ric.append(x['event_id'])
    if len(set(controls))!=3:duplicate_ric.append(x['event_id'])
    if x['issuer'] in issuers:self_issuer.append(x['event_id'])
    if len(set(issuers))!=3:duplicate_issuer.append(x['event_id'])
IX=pd.read_csv(ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
GI=IX.loc[IX.ric.eq('.OMXSBGI')&IX.close.notna()].set_index('date').sort_index().close
assert not GI.index.duplicated().any()
rics=sorted(set(V.RIC)|set(V[['c1_ric','c2_ric','c3_ric']].to_numpy().ravel()))
PX=pd.read_parquet(ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','totret','close'],filters=[('ric','in',rics)])
PX['date']=pd.to_datetime(PX.date)
assert not PX.duplicated(['ric','date']).any()
BY={r:g.set_index('date').sort_index() for r,g in PX.groupby('ric')}
records=[]
for x in V.to_dict('records'):
    a,b=x['early_date'],x['late_date']
    days=GI.index[(GI.index>a)&(GI.index<=b)]
    factors=[]
    for ric in [x['RIC']]+[x[f'c{k}_ric'] for k in (1,2,3)]:
        g=BY[ric]
        rets=g.totret.reindex(days).to_numpy()/100
        close=g.close.reindex([a,b]).to_numpy()
        assert np.isfinite(rets).all() and (rets>-1).all()
        assert np.isfinite(close).all() and (close>0).all()
        factors.append(math.exp(math.fsum(math.log1p(float(r)) for r in rets)))
    market=float(GI.loc[b]/GI.loc[a])
    sign={'addition':1,'deletion':-1}[x['type']]
    own_fixed=sign*(factors[0]-math.fsum(factors[1:])/3)*100
    own_gross=sign*(factors[0]-market)*100
    assert len(days)==x['holding_days']
    records.append({'event_id':x['event_id'],'review':x['review'],'type':x['type'],'year':x['year'],
        'fixed_control_pp':own_fixed,'gross_pp':own_gross,
        'control_error_pp':own_fixed-x['fixed_control_pp'],'market_error_pp':own_gross-x['gross_pp'],
        'basket_factor_error':math.fsum(factors[1:])/3-x['control_terminal_factor']})
R=pd.DataFrame(records)
S=pd.read_csv(BASE/'fixed_controls/summary.csv')
checks=[]
for row in S.to_dict('records'):
    ty=row['sample'].split('_',1)[0]
    start=2021 if 'descriptive2021' in row['sample'] else 2017
    z=R[R.type.eq(ty)&R.year.between(start,2025)]
    v=z.groupby('review')[row['metric']].mean().to_numpy()
    model=sm.OLS(v,np.ones((len(v),1))).fit()
    mean=float(model.params[0]);lo,hi=map(float,model.conf_int(alpha=.05)[0])
    # Independent bit-mask signs, counted in vector batches; exact 2**G reference.
    n=len(v);total=1<<n;extreme=0
    for j in range(0,total,4096):
        bits=np.arange(j,min(j+4096,total),dtype=np.uint32)
        sg=np.where(((bits[:,None]>>np.arange(n,dtype=np.uint32))&1)==0,-1,1)
        vals=np.abs((sg*v).sum(axis=1)/n)
        extreme+=int((vals>=abs(mean)-1e-12).sum())
    p=extreme/total
    diffs={k:float(val-row[k]) for k,val in [('mean_review_pp',mean),('ci_low_pp',lo),('ci_high_pp',hi),('p_signflip',p)]}
    assert len(z)==row['N'] and n==row['G']
    assert max(abs(w) for w in diffs.values())<1e-9
    checks.append({'sample':row['sample'],'metric':row['metric'],'N':len(z),'G':n,'mean_review_pp':mean,
        'ci_low_pp':lo,'ci_high_pp':hi,'p_signflip':p,'difference_from_report':diffs})
assert R.control_error_pp.abs().max()<1e-9
assert R.market_error_pp.abs().max()<1e-9
assert not (self_ric or duplicate_ric or self_issuer or duplicate_issuer)
result={'purpose':'Independent reproduction of exactly the frozen matched-control timing diagnostic; no rematching or new windows.',
    'valid_event_rows':len(V),'raw_stock_and_control_legs':4*len(V),'raw_return_unit':'percent daily, divided by 100 before compounding',
    'interval':'early close excluded, late close included; identical trading dates for stock and all 3 controls',
    'basket':'Three fixed controls, equal initial notional, buy-and-hold; arithmetic average of terminal wealth factors',
    'max_abs_control_error_pp':float(R.control_error_pp.abs().max()),'max_abs_market_error_pp':float(R.market_error_pp.abs().max()),
    'max_abs_basket_factor_error':float(R.basket_factor_error.abs().max()),
    'identity_checks':{'event_RIC_matches_frozen_file':True,'all_control_RICs_unchanged':True,
        'self_RIC_events':self_ric,'duplicate_control_RIC_events':duplicate_ric,
        'self_issuer_events':self_issuer,'duplicate_control_issuer_events':duplicate_issuer,
        'cancelled_events_in_control_sample':int(V.cancelled.sum())},
    'coverage':D.groupby(['type','control_status']).size().rename('N').reset_index().to_dict('records'),
    'summary_checks':checks,
    'limitation':'Inherited frozen matching, eligibility and return data are not newly revalidated against all original source documents. Market-relative path diagnostics in summary are not control-adjusted path diagnostics.',
    'control_file_sha256':hashlib.sha256(CP.read_bytes()).hexdigest(),
    'reviewed_script_sha256':hashlib.sha256((ROOT/'code/build/omxsb_execution_controls_20261102.py').read_bytes()).hexdigest()}
(OUT/'timing_controls_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('valid_event_rows','raw_stock_and_control_legs','max_abs_control_error_pp','max_abs_market_error_pp','identity_checks')},indent=2))
print(pd.DataFrame(checks).drop(columns='difference_from_report').to_string(index=False))
