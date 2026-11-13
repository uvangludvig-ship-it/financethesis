"""Independent validation of the frozen volume-unit analysis; no new estimates."""
from pathlib import Path
import hashlib, json, re, sys
import numpy as np
import pandas as pd
from scipy.stats import t

O = Path(__file__).resolve().parent
R = Path('/Users/ludviguvang/dev/financethesis')
sys.path.insert(0, str(O.parent / 'comparison_rebuild_20261102'))
from independent_audit import independent_ratio

lock = json.loads((O / 'UNIT_GATE_LOCK.json').read_text())
run = json.loads((O / 'ANALYSIS_RUN.json').read_text())
for k, v in lock['files'].items():
    assert hashlib.sha256(Path(k).read_bytes()).hexdigest() == v, k
for k, v in run['input_hashes'].items():
    assert hashlib.sha256(Path(k).read_bytes()).hexdigest() == v, k
assert pd.Timestamp(lock['frozen_at_utc']) < pd.Timestamp(run['run_at_utc'])
gate = pd.read_csv(O / 'unit_gate_all216.csv', parse_dates=['AD','ED','after','before','reference_start','reference_end','baseline_start'])
anchors = pd.read_csv(O / 'all_available_exactISIN_month_anchors.csv')
saved_v = pd.read_csv(O / 'volume_input_all216.csv')
assert len(gate) == 216 and gate.event_id.is_unique and gate.unit_gate_pass.sum() == 205
assert int((gate.unit_gate_pass & gate.original172_pass).sum()) == 166
assert int((gate.unit_gate_pass & ~gate.original172_pass).sum()) == 39
assert int((~gate.unit_gate_pass & gate.original172_pass).sum()) == 6

pf = R / 'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet'
P = pd.read_parquet(pf, columns=['ric','date','close','volume','turnover','source'])
P = {k: x.set_index('date').sort_index() for k,x in P[P.ric.isin(gate.RIC)].groupby('ric')}
assert all(x.index.is_unique for x in P.values())
norm = lambda x: re.sub('[^A-Z0-9]', '', str(x).upper())
def number(x):
    return float(str(x).strip().replace(' ', '').replace(',', '.'))

# Reopen all 16 original Nasdaq workbooks; independently reproduce all 1412 exact rows.
anchor_checks = []
for file, aa in anchors[anchors.matched_rows.eq(1)].groupby('source_file'):
    sheet = pd.read_excel(file, sheet_name='Instrument Trading Details', header=None)
    hh = [i for i,row in sheet.iloc[:10].iterrows() if 'ISIN' in row.values and 'Instrument' in row.values]
    assert len(hh) == 1
    header = sheet.iloc[hh[0]].map(norm)
    col = {name: list(header[header.eq(name)].index) for name in ['ISIN','TOTALNOOFTRADEDSHARES','TOTALTURNOVER','LISTEDDAYS']}
    for z in aa.itertuples():
        rr = sheet.iloc[int(z.source_excel_row)-1]
        assert rr.iloc[col['ISIN'][0]] == z.isin
        nvol, nturn, ndays = [number(rr.iloc[col[c][0]]) for c in ['TOTALNOOFTRADEDSHARES','TOTALTURNOVER','LISTEDDAYS']]
        start = pd.Timestamp(str(z.month)+'01'); end = start + pd.offsets.MonthEnd(0)
        pp = P[z.RIC].loc[start:end]
        pv, pt = pp.volume.sum(min_count=1), pp.turnover.sum(min_count=1)
        vals = dict(nasdaq_volume=nvol,nasdaq_turnover=nturn,nasdaq_listed_days=ndays,
                    panel_volume=pv,panel_turnover=pt,panel_volume_n=pp.volume.notna().sum(),
                    negative_volume_n=pp.volume.lt(0).sum(),factor=nvol/pv if pv>0 else np.nan,
                    turnover_relerror=pt/nturn-1 if nturn>0 else np.nan)
        for k,v in vals.items():
            assert np.isclose(v,getattr(z,k),rtol=1e-11,atol=1e-7,equal_nan=True),(z.RIC,z.month,k)
        valid = bool(nvol>0 and pv>0 and nturn>0 and np.isfinite(vals['turnover_relerror'])
                     and abs(vals['turnover_relerror']) <= .001 and set(pp.source.dropna())=={'tr'}
                     and pp.volume.notna().sum()>=ndays and not pp.volume.lt(0).any())
        assert valid == z.anchor_basic_valid
        anchor_checks.append(dict(RIC=z.RIC,month=z.month,valid=valid,
                                  negative_turnover_days=int(pp.turnover.lt(0).sum())))
assert len(anchor_checks)==1412
assert not any(x['negative_turnover_days'] for x in anchor_checks)

# Confirm each accepted scalar's data origin and the documented physical-share bridge.
ca = pd.read_csv(R / 'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',parse_dates=['action_date'])
aa = anchors.set_index(['RIC','month'],verify_integrity=True)
factor_checks = []
for z in gate[gate.unit_gate_pass].itertuples():
    ref = aa.loc[(z.RIC,z.month)]
    assert ref.anchor_basic_valid and np.isclose(ref.factor,z.month_volume_factor,rtol=1e-11)
    aftersplits = ca[ca.RIC.eq(z.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.gt(z.reference_end)&ca.action_date.le(z.after)]
    factor = ref.factor * aftersplits.factor.prod()
    if z.factor_method == 'previous_month_anchor_plus_dated_split_reference_month_mixed':
        prior = aa.loc[(z.RIC,int(z.previous_month))]
        st = pd.Timestamp(str(int(z.previous_month))+'01')+pd.offsets.MonthEnd(0)
        sp = ca[ca.RIC.eq(z.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.gt(st)&ca.action_date.le(z.after)]
        assert prior.anchor_basic_valid and z.RIC=='LAGRb.ST' and sp.factor.prod()==3
        factor = prior.factor*sp.factor.prod()
    assert np.isclose(factor,z.corrected_volume_factor_to_FI_after,rtol=1e-12,atol=1e-12)
    nxt = aa.loc[(z.RIC,int(z.next_month))]
    en = pd.Timestamp(str(int(z.next_month))+'01')+pd.offsets.MonthEnd(0)
    sp = ca[ca.RIC.eq(z.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.gt(z.after)&ca.action_date.le(en)]
    next_ok = bool(nxt.anchor_basic_valid and abs(nxt.factor/(factor*sp.factor.prod())-1)<=.001)
    if not next_ok:
        assert z.event_id in ['OMXSB-2019H1-11','OMXSB-2022H2-03','OMXSB-2022H2-08']
        prior = aa.loc[(z.RIC,int(z.previous_month))]
        assert prior.anchor_basic_valid and abs(prior.factor/ref.factor-1)<=.001
        assert nxt.anchor_basic_valid
    factor_checks.append(dict(event_id=z.event_id,RIC=z.RIC,factor=float(factor),next_agrees=next_ok,
                              method=z.factor_method))

idx = pd.read_csv(R / 'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
idx=idx[idx.ric.eq('.OMXSBGI')]
cal = pd.DatetimeIndex(idx.date.dropna().sort_values().unique())
assert cal.equals(pd.DatetimeIndex(idx.loc[idx.close.notna(),'date'].dropna().sort_values().unique()))
qpath = R / 'output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz'
qs = pd.read_csv(qpath,usecols=['event_id','fi_price_after','company_mcap_after']).drop_duplicates().set_index('event_id',verify_integrity=True)
rows=[]
for z in gate.itertuples():
    assert z.AD in cal and z.ED in cal
    i,j=cal.get_loc(z.AD),cal.get_loc(z.ED)
    bd=cal[[i+k for k in range(-61,-11)]]; sd=cal[[j+k for k in range(-22,-1)]]; ed=cal[j-1]
    assert len(bd)==50 and len(sd)==21 and bd[0]==z.baseline_start
    pp=P[z.RIC]; bv=pp.reindex(bd).volume; bv=bv[bv.ge(0)]
    sv=pp.reindex(sd).volume; sv=sv[sv.ge(0)]
    v=pp.reindex([ed]).volume.iloc[0]; assert np.isfinite(v) and v>=0
    if z.unit_gate_pass:
        window_rows=pp.reindex(bd.union(sd).union(pd.DatetimeIndex([ed])))
        assert window_rows.loc[window_rows.volume.notna(),'source'].eq('tr').all()
    scale=100*qs.loc[z.event_id,'fi_price_after']/qs.loc[z.event_id,'company_mcap_after']
    factor=z.corrected_volume_factor_to_FI_after
    row=dict(event_id=z.event_id,baseline_N=len(bv),shortbaseline_N=len(sv),rebalancing_day=str(ed.date()),
             raw_panel_EDminus1_volume=v,raw_panel_baseline=bv.mean(),raw_panel_shortbaseline=sv.mean(),
             volume_FI_after_units=v*factor,baseline_volume_FI_after_units=bv.mean()*factor,
             shortbaseline_volume_FI_after_units=sv.mean()*factor,volume_window_pass=len(bv)>=40)
    for prefix,fac in [('corrected',factor),('legacy',1)]:
        row[prefix+'_volume_pp']=v*scale*fac
        row[prefix+'_baseline_pp']=bv.mean()*scale*fac
        row[prefix+'_excess_pp']=(v-bv.mean())*scale*fac
        row[prefix+'_short_excess_pp']=(v-sv.mean())*scale*fac if len(sv)>=17 else np.nan
    rows.append(row)
v=pd.DataFrame(rows)
check=v.merge(saved_v,on='event_id',validate='1:1',suffixes=('_audit','_saved'))
for k in v.columns.difference(['event_id','rebalancing_day']):
    assert np.allclose(check[k+'_audit'],check[k+'_saved'],rtol=1e-11,atol=1e-7,equal_nan=True),k
assert check.rebalancing_day_audit.eq(check.rebalancing_day_saved).all()
assert v.volume_window_pass.all() and v.shortbaseline_N.ge(17).all()

old=pd.read_csv(O.parent/'volume_measurement_20261102/gate_and_volume.csv').set_index('event_id',verify_integrity=True)
vc=v.set_index('event_id')
for k in ['volume_pp','baseline_pp','excess_pp','short_excess_pp']:
    assert np.allclose(vc.loc[old.index,'legacy_'+k],old[k],rtol=1e-11,atol=1e-10,equal_nan=True),k

oldpath=R/'output/omxsb_mechanism_frontier_20261102/demand/event_demand_by_definition.csv'
newpath=O.parent/'mandate_upgrade_20261102/event_demand_updated.csv'
d=pd.read_csv(oldpath);d=d[d.definition.isin(['documented_stable_family_subset','all_stable_family_candidates_sensitivity'])]
new=pd.read_csv(newpath);new=new[new.definition.eq('updated_documented_continuity')]
d=pd.concat([d,new],ignore_index=True)
d=d.merge(v,on='event_id',validate='m:1').merge(gate[['event_id','unit_gate_pass','original172_pass']],on='event_id',validate='m:1')
d['quantity_abs_pp']=d.net_company_pp.abs()
savedj=pd.read_csv(O/'joined_quantities_volume_all216.csv')
assert len(d)==len(savedj)==648 and set(zip(d.definition,d.event_id))==set(zip(savedj.definition,savedj.event_id))
numcheck=d.merge(savedj,on=['event_id','definition'],validate='1:1',suffixes=('_audit','_saved'))
assert np.allclose(numcheck.quantity_abs_pp_audit,numcheck.quantity_abs_pp_saved)
samples={'original172_legacy':(d.original172_pass,'legacy'),
         'common166_legacy':(d.original172_pass&d.unit_gate_pass,'legacy'),
         'common166_corrected':(d.original172_pass&d.unit_gate_pass,'corrected'),
         'corrected205':(d.unit_gate_pass,'corrected')}
ratios=[]
for z in pd.read_csv(O/'volume_quantity_ratios.csv').itertuples():
    mask,prefix=samples[z.sample]
    x=d[mask&d.definition.eq(z.definition)&d.type.eq(z.type)].copy()
    y=x[prefix+'_'+z.outcome]
    assert y.notna().all() and x.quantity_abs_pp.notna().all()
    rv=pd.DataFrame({'review':x.review_cycle,'y':y,'x':x.quantity_abs_pp}).groupby('review')[['y','x']].mean()
    ans,cov=independent_ratio(rv.y,rv.x);ans['N']=len(x)
    err={k:float(ans[k]-getattr(z,k)) for k in ['ratio','den_mean','num_mean','G','lo','hi','N']}
    assert max(abs(x) for x in err.values())<1e-9 and ans['fieller_type']==z.fieller_type
    ratios.append(dict(sample=z.sample,definition=z.definition,type=z.type,outcome=z.outcome,values=ans,covariance=cov))
assert len(ratios)==72
old_ratios=pd.read_csv(O.parent/'volume_measurement_20261102/volume_quantity_ratios.csv')
current_ratios=pd.read_csv(O/'volume_quantity_ratios.csv')
old_compare=old_ratios.merge(current_ratios[current_ratios['sample'].eq('original172_legacy')],
                            on=['definition','type','outcome'],validate='1:1',suffixes=('_old','_new'))
assert len(old_compare)==12
for k in ['num_mean','den_mean','ratio','lo','hi']:
    assert old_compare[k+'_old'].eq(old_compare[k+'_new']).all()

models=[]
for z in pd.read_csv(O/'diagnostic_slopes.csv').itertuples():
    x=d[d.unit_gate_pass&d.definition.eq(z.definition)].copy()
    if z.type!='pooled':x=x[x.type.eq(z.type)]
    xs=[np.ones(len(x)),x.quantity_abs_pp.to_numpy()]
    if z.type=='pooled':xs.append(x.type.eq('deletion').to_numpy().astype(float))
    if z.baseline_control:xs.append(x.corrected_baseline_pp.to_numpy())
    xs.extend(x.review_cycle.eq(r).to_numpy().astype(float) for r in sorted(x.review_cycle.unique())[1:])
    X=np.column_stack(xs);Y=x.corrected_excess_pp.to_numpy();W=(1/x.groupby('review_cycle').event_id.transform('count')).to_numpy()
    N,K=X.shape;G=x.review_cycle.nunique();assert np.linalg.matrix_rank(X)==K
    bread=np.linalg.inv(X.T@(W[:,None]*X));beta=bread@(X.T@(W*Y));u=Y-X@beta
    scores=[]
    for rev in x.review_cycle.unique():
        ii=x.review_cycle.eq(rev).to_numpy();scores.append(X[ii].T@(W[ii]*u[ii]))
    scores=np.array(scores);V=bread@(scores.T@scores)@bread*(G/(G-1))*((N-1)/(N-K))
    se=np.sqrt(V[1,1]);half=t.ppf(.975,G-1)*se
    ans=dict(N=N,G=G,slope=beta[1],lo=beta[1]-half,hi=beta[1]+half,
             p=2*t.sf(abs(beta[1]/se),G-1),r2=1-np.sum(W*u*u)/np.sum(W*(Y-np.average(Y,weights=W))**2))
    assert max(abs(ans[k]-getattr(z,k)) for k in ans)<1e-8
    models.append(dict(definition=z.definition,type=z.type,baseline_control=bool(z.baseline_control),values=ans))
assert len(models)==18

common=gate[gate.unit_gate_pass&gate.original172_pass]
known_interval_ca=[]
for z in gate[gate.unit_gate_pass].itertuples():
    for k in ca[ca.RIC.eq(z.RIC)&ca.action_date.ge(z.baseline_start)&ca.action_date.le(z.after)].itertuples():
        known_interval_ca.append(dict(event_id=z.event_id,RIC=z.RIC,kind=k.kind,
                                      date=str(k.action_date.date()),factor=float(k.factor)))
source_files=[Path(x) for x in anchors.source_file.unique()]
paths=[O/'UNIT_GATE_LOCK.json',O/'unit_gate_all216.csv',O/'volume_input_all216.csv',O/'run_frozen_volume.py',
       O/'volume_quantity_ratios.csv',O/'diagnostic_slopes.csv',O/'ANALYSIS_RUN.json']+source_files
report=dict(locked_hashes_current=True,lock_precedes_association_run=True,raw_nasdaq_workbooks=len(source_files),
            all1412_exact_month_anchor_rows_reproduced=True,all216_frozen_windows_reproduced=True,
            all205_scalar_formulas_reproduced=True,all72_Fieller_cells_reproduced=True,all18_WLS_cluster_models_reproduced=True,
            original172_legacy_matches_old_outputs=True,all12_original_ratio_cells_match_exactly=True,
            all_observed_passed_window_volume_rows_source_tr=True,
            known_corporate_actions_baseline_to_after=known_interval_ca,
            same_event_numerator_denominator_all72_cells=True,
            accepted_event_types=gate[gate.unit_gate_pass].type.value_counts().to_dict(),
            common166_factor_range=[float(common.corrected_volume_factor_to_FI_after.min()),float(common.corrected_volume_factor_to_FI_after.max())],
            common166_factors_materially_not_one=common[(common.corrected_volume_factor_to_FI_after-1).abs()>.0001][['event_id','RIC','corrected_volume_factor_to_FI_after']].to_dict('records'),
            exclusions=gate[~gate.unit_gate_pass][['event_id','RIC','exclusions']].to_dict('records'),
            factors=factor_checks,ratios=ratios,models=models,
            limits=['Monthly anchors validate aggregate units, not every vendor daily adjustment.',
                    'A constant factor over baseline and ED-1 remains conditional on a stable adjusted-volume unit within those windows and known CA completeness.',
                    'No price-derived conversion factor; FI prices are checks and common nominal scaling only.',
                    'Same-company market-cap denominator remains a possible common-scale association source.',
                    'Nasdaq Stockholm matched scope is not all venues; quarter net quantity is not ED-1 trading.',
                    'The gate amendment is after unit diagnostics but before new associations, and is exploratory.'],
            input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
(O/'independent_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k not in ['ratios','models','factors','input_hashes']},indent=2,ensure_ascii=False))
