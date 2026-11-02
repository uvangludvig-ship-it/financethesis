from pathlib import Path
import hashlib, json, sys
import numpy as np
import pandas as pd

O=Path(__file__).resolve().parent
R=Path('/Users/ludviguvang/dev/financethesis')
D=R/'output/omxsb_mechanism_frontier_20261102/demand'
sys.path.insert(0,str(O.parent/'comparison_rebuild_20261102'))
from run import fieller

p=pd.read_csv(D/'fund_event_demand_panel.csv.gz')
ev=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv')
u=pd.read_csv(O/'upgraded_fund_review_evidence.csv')
assert not u.duplicated(['fund_id','review_cycle']).any()
p=p.merge(u[['fund_id','review_cycle','upgrade_eligible']],on=['fund_id','review_cycle'],how='left',validate='m:1')
p['upgrade_eligible']=p.upgrade_eligible.eq(True)
p['new_documented_continuity']=p.documented_stable_family|p.upgrade_eligible
p['new_evidence_class']=p.mandate_evidence
p.loc[p.upgrade_eligible,'new_evidence_class']='historical_index_near_with_explicit_continuity_assumption'
p['new_strategy_continuity_assumption']=p.continuity_assumption|p.upgrade_eligible
p['new_source_ids']=p.source_ids
p.loc[p.upgrade_eligible&p.fund_id.eq(51482),'new_source_ids']='SPP2018;SPP2019;PPM2018;FI'
p.loc[p.upgrade_eligible&p.fund_id.eq(60310),'new_source_ids']='LF2018;LF2019;existing_later_regime_sources;PPM2018;FI'
p.loc[p.upgrade_eligible&p.fund_id.eq(60824),'new_source_ids']='PPM_catalog2016;PPM2018;FI'
assert (p.loc[p.new_documented_continuity,'stable_family']).all()
assert (p.loc[p.new_documented_continuity,'family_candidate_stable']).all()
p.to_csv(O/'classified_fund_event_panel.csv.gz',index=False,compression='gzip')
allrows=[]
for name,mask in [('old_documented',p.documented_stable_family),('updated_documented_continuity',p.new_documented_continuity),('broad_candidates',p.family_candidate_stable)]:
    g=p[mask&p.valid_for_market_acquisition_description].copy()
    g['pos']=g.delta_company_pp.clip(lower=0);g['neg']=g.delta_company_pp.clip(upper=0)
    a=g.groupby('event_id').agg(net_company_pp=('delta_company_pp','sum'),positive_company_pp=('pos','sum'),negative_company_pp=('neg','sum'),n_funds=('fund_id','nunique'))
    z=ev.merge(a,on='event_id',how='left',validate='1:1')
    z['definition']=name
    z['expected_fund_pairs']=z.event_id.map(p[mask].groupby('event_id').size()).fillna(0)
    z['excluded_fund_pairs']=z.expected_fund_pairs-z.n_funds.fillna(0)
    assert np.allclose(z.net_company_pp,z.positive_company_pp+z.negative_company_pp,equal_nan=True)
    allrows.append(z)
e=pd.concat(allrows,ignore_index=True)
e.to_csv(O/'event_demand_updated.csv',index=False)
summ=[]
for (name,typ),g in e.groupby(['definition','type']):
    rv=g.groupby('review_cycle')[['net_company_pp','n_funds','excluded_fund_pairs']].mean()
    summ.append(dict(definition=name,type=typ,N=g.net_company_pp.notna().sum(),G=len(rv),**rv.mean().to_dict()))
pd.DataFrame(summ).to_csv(O/'quantity_summary.csv',index=False)

# Previously known outcome definitions; no new windows or controls.
v=pd.read_csv(O.parent/'volume_measurement_20261102/gate_and_volume.csv')
prices=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv')
ratios=[]
for name,g in e.groupby('definition'):
    z=g.merge(v[['event_id','unit_gate_pass','excess_pp','short_excess_pp']],on='event_id',validate='1:1')
    z=z[z.unit_gate_pass].dropna(subset=['net_company_pp','excess_pp']).copy()
    z['quantity_abs_pp']=z.net_company_pp.abs()
    for typ,tg in z.groupby('type'):
        for y in ['excess_pp','short_excess_pp']:
            same=tg.dropna(subset=[y,'quantity_abs_pp'])
            rv=same.groupby('review_cycle')[[y,'quantity_abs_pp']].mean()
            a=fieller(rv[y],rv.quantity_abs_pp)
            ratios.append(dict(definition=name,type=typ,measure=y,N=len(same),**a))
    z=g.merge(prices[['event_id','event_1','diff3_1']],on='event_id',validate='1:1').dropna(subset=['net_company_pp','event_1','diff3_1'])
    for typ,tg in z.groupby('type'):
        for y in ['event_1','diff3_1']:
            rv=tg.groupby('review_cycle')[[y,'net_company_pp']].mean()
            a=fieller(rv[y],rv.net_company_pp)
            ratios.append(dict(definition=name,type=typ,measure=y,N=len(tg),**a))
pd.DataFrame(ratios).to_csv(O/'fixed_definition_ratios.csv',index=False)
files=[D/'fund_event_demand_panel.csv.gz',O/'DECISIONS.txt',O/'PRIMARY_READING.txt',O/'upgraded_fund_review_evidence.csv',Path(__file__)]
(O/'hashes.json').write_text(json.dumps({str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in files},indent=2))
print(pd.DataFrame(summ).to_string(index=False))
print(pd.DataFrame(ratios).query('definition == "updated_documented_continuity"').to_string(index=False))
