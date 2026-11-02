from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,sys
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'additions_20261102'))
from portable_paths import analysis_paths, first_output, comparison_function, repository_source, verify_original_lock
R,O=analysis_paths('mandate_upgrade_20261102')
independent_ratio=comparison_function(R,'independent_audit','independent_ratio')
D=R/'output/omxsb_mechanism_frontier_20261102/demand'
P=pd.read_csv(D/'fund_event_demand_panel.csv.gz');U=pd.read_csv(O/'upgraded_fund_review_evidence.csv');S=pd.read_csv(O/'classified_fund_event_panel.csv.gz');E=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv')
assert not P.duplicated(['event_id','fund_id']).any();assert not U.duplicated(['fund_id','review_cycle']).any();assert set(U.fund_id)=={51482,60310,60824}
ids={51482:'SE0000529992',60310:'SE0002656611',60824:'SE0007074075'}
assert U.before_fund_isin.eq(U.fund_id.map(ids)).all()and U.after_fund_isin.eq(U.fund_id.map(ids)).all()
eligible=U.stable_family&~U.benchmark_transition&~U.fund_merger
assert eligible.equals(U.upgrade_eligible)
lookup=set(zip(U.loc[eligible,'fund_id'],U.loc[eligible,'review_cycle']))
P['own_upgrade']=[(f,r)in lookup for f,r in zip(P.fund_id,P.review_cycle)]
P['own_new']=P.documented_stable_family|P.own_upgrade
S=S.set_index(['event_id','fund_id']);Q=P.set_index(['event_id','fund_id']);assert S.index.equals(Q.index)
assert Q.own_upgrade.equals(S.upgrade_eligible);assert Q.own_new.equals(S.new_documented_continuity)
assert S.loc[S.upgrade_eligible,'new_evidence_class'].eq('historical_index_near_with_explicit_continuity_assumption').all()
assert S.loc[S.upgrade_eligible,'new_strategy_continuity_assumption'].all()
assert S.loc[~S.upgrade_eligible,'new_evidence_class'].equals(S.loc[~S.upgrade_eligible,'mandate_evidence'])
assert S.loc[~S.upgrade_eligible,'new_strategy_continuity_assumption'].equals(S.loc[~S.upgrade_eligible,'continuity_assumption'])
assert S.loc[S.upgrade_eligible,'new_source_ids'].notna().all()
legacy_cols=[c for c in U if c in P and c!='upgrade_eligible']
legacy=P[P.fund_id.isin(ids)][legacy_cols].drop_duplicates().sort_values(['fund_id','review_cycle']).reset_index(drop=True)
assert len(legacy)==len(U)==42
pd.testing.assert_frame_equal(legacy,U[legacy_cols].sort_values(['fund_id','review_cycle']).reset_index(drop=True),check_dtype=False)
selected=P[P.own_new];added=P[P.own_new&~P.documented_stable_family]
assert selected.stable_family.all()and selected.family_candidate_stable.all();assert not selected.benchmark_transition.any();assert not selected.fund_merger.any()
assert selected.before_report_instrument_rows.gt(0).all()and selected.after_report_instrument_rows.gt(0).all()
assert selected.before_fund_isin.eq(selected.after_fund_isin).all();assert selected.valid_for_market_acquisition_description.all()
assert selected.before_quantity.notna().all()and selected.after_quantity.notna().all();assert selected.before_quantity.ge(0).all()and selected.after_quantity.ge(0).all()
assert np.allclose(selected.delta_company_pp,100*(selected.after_quantity-selected.factor*selected.before_quantity)*selected.fi_price_after/selected.company_mcap_after)
rows=[]
for name,mask in [('old_documented',P.documented_stable_family),('updated_documented_continuity',P.own_new),('broad_candidates',P.family_candidate_stable)]:
    valid=P[mask&P.valid_for_market_acquisition_description]
    for ev in E.itertuples():
        g=valid[valid.event_id==ev.event_id];expected=P[mask&P.event_id.eq(ev.event_id)]
        rows.append(dict(definition=name,event_id=ev.event_id,type=ev.type,review_cycle=ev.review_cycle,net_company_pp=g.delta_company_pp.sum()if len(g)else np.nan,positive_company_pp=g.loc[g.delta_company_pp>0,'delta_company_pp'].sum()if len(g)else np.nan,negative_company_pp=g.loc[g.delta_company_pp<0,'delta_company_pp'].sum()if len(g)else np.nan,n_funds=g.fund_id.nunique()if len(g)else np.nan,expected_fund_pairs=len(expected),excluded_fund_pairs=len(expected)-g.fund_id.nunique()))
A=pd.DataFrame(rows);Z=pd.read_csv(O/'event_demand_updated.csv');J=A.merge(Z,on=['definition','event_id','type','review_cycle'],suffixes=('_ind','_prod'),validate='1:1');err={c:float((J[c+'_ind']-J[c+'_prod']).abs().max())for c in ['net_company_pp','positive_company_pp','negative_company_pp','n_funds','expected_fund_pairs','excluded_fund_pairs']};assert max(err.values())<1e-10
summ=[]
for x in pd.read_csv(O/'quantity_summary.csv').itertuples():
    a=A[(A.definition==x.definition)&(A.type==x.type)];m=a.groupby('review_cycle')[['net_company_pp','n_funds','excluded_fund_pairs']].mean().mean();assert len(a)==x.N and a.review_cycle.nunique()==x.G
    assert all(abs(m[k]-getattr(x,k))<1e-10 for k in m.index);summ.append(dict(definition=x.definition,type=x.type,N=len(a),G=a.review_cycle.nunique(),**m.to_dict()))
V=pd.read_csv(first_output(R)/'volume_measurement_20261102/gate_and_volume.csv');B=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv');cells=[]
for x in pd.read_csv(O/'fixed_definition_ratios.csv').itertuples():
    a=A[(A.definition==x.definition)&(A.type==x.type)].copy()
    if x.measure in ['excess_pp','short_excess_pp']:
        a=a.merge(V[['event_id','unit_gate_pass',x.measure]],on='event_id',validate='1:1');a=a[a.unit_gate_pass].dropna(subset=['net_company_pp',x.measure]);a['den']=a.net_company_pp.abs()
    else:
        a=a.merge(B[['event_id','event_1','diff3_1']],on='event_id',validate='1:1').dropna(subset=['net_company_pp','event_1','diff3_1']);a['den']=a.net_company_pp
    v=a.groupby('review_cycle')[[x.measure,'den']].mean();ans,cov=independent_ratio(v[x.measure],v.den);ans['N']=len(a);diff={k:float(ans[k]-getattr(x,k))for k in ['N','G','ratio','num_mean','den_mean','lo','hi']};assert max(abs(t)for t in diff.values())<1e-10;assert ans['fieller_type']==x.fieller_type
    cells.append(dict(definition=x.definition,type=x.type,measure=x.measure,independent=ans,differences=diff,covariance=cov,same_events_both_sides=True))
assert len(cells)==24
# Verify exact 2018 PPM number/ISIN rows from actual original workbook, no name approximation.
proof=json.loads((O/'PPM2018_identity.json').read_text())+json.loads((first_output(R)/'mandate_catalog_20261102/Access_Sverige_PPM2018_identity_raw.json').read_text());identity=[]
for z in proof:
    f=repository_source(R,z.get('file',z.get('source_file')));book=pd.read_excel(f,sheet_name=z['sheet'],header=None,dtype=str);row=book.iloc[z['excel_row']-1]
    assert str(row.iloc[0])==z['cells']['0'];assert str(row.iloc[17])==z['cells']['17'];assert str(row.iloc[1])==z['cells']['1']
    if 'sha256'in z:assert hashlib.sha256(f.read_bytes()).hexdigest()==z['sha256']
    identity.append(dict(PPM_number=str(row.iloc[0]),name=str(row.iloc[1]),ISIN=str(row.iloc[17]),excel_row=z['excel_row'],source=str(f),source_sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
assert {z['ISIN']for z in identity}==set(ids.values())
counts=U.groupby('fund_id')[['upgrade_eligible','documented_stable_family']].sum().reset_index().to_dict('records')
newreviews=added[['fund_id','review_cycle']].drop_duplicates();out=dict(all648_event_definition_rows_pass=True,all6_quantity_summary_rows_pass=True,all24_ratio_cells_pass=True,exact_PPM2018_identities=identity,upgraded_review_counts=counts,incremental_fund_reviews=len(newreviews),incremental_fund_event_rows=len(added),invalid_selected_rows=int((selected.valid_for_market_acquisition_description==False).sum()),new_selected_identity_failures=0,old_documented_preserved=True,source_join_uses_exact_fund_id_review=True,aggregation_max_errors=err,quantity_summary=summ,ratio_cells=cells,legacy_continuity_false_on_new_rows=int((~added.continuity_assumption).sum()),new_evidence_fields_explicit_and_valid=True,legacy_evidence_preserved_exactly=True,interpretation='Historical index-near evidence plus explicit continuity assumption, not full replication, complete passive demand or causal instrument; original legacy evidence columns retained unchanged.',input_hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest()for f in [D/'fund_event_demand_panel.csv.gz',O/'upgraded_fund_review_evidence.csv',O/'classified_fund_event_panel.csv.gz',O/'event_demand_updated.csv',O/'fixed_definition_ratios.csv',O/'PRIMARY_READING.txt',Path(__file__).with_name('aggregate.py'),O/'PPM2018_identity.json']})
(O/'independent_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k not in ['ratio_cells','input_hashes','exact_PPM2018_identities']},indent=2))
