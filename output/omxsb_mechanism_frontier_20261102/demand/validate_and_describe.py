from pathlib import Path
import pandas as pd,numpy as np,json
D=Path(__file__).parent
p=pd.read_csv(D/'fund_event_demand_panel.csv.gz')
e=pd.read_csv(D/'event_demand_by_definition.csv')
s=pd.read_csv(D/'summary_review_weighted_NO_PVALUES.csv')
assert not p.duplicated(['event_id','fund_id']).any()
assert not p.loc[p.fund_merger,'valid_for_market_acquisition_description'].any()
assert not p.loc[p.mandate_evidence.eq('documented_active_mixed'),'documented_stable_family'].any()
assert not p.loc[p.measurement_status.str.startswith('no_nonempty'),'delta_company_pp'].notna().any()
assert p.predicted_mechanical_company_pp.isna().all()
assert not p.real_time_forecast_valid.any()
# Metadata continuity evidence, not behavior-based strategy classification.
p['same_legal_fund_isin']=p.before_fund_isin.eq(p.after_fund_isin)&p.before_fund_isin.notna()
rows=[]
for f,g in p[p.candidate].groupby('fund_id'):
 z=g[g.in_frozen_matched_price_sample&g.family_candidate_stable&g.valid_for_market_acquisition_description]
 a=z[z.type.eq('addition')];d=z[z.type.eq('deletion')]
 rows.append(dict(fund_id=f,name=g.fund_name_canonical.iloc[0],stable_family_event_pairs=len(z),reviews=z.review_cycle.nunique(),documented_pairs=int(z.documented_stable_family.sum()),metadata_only_pairs=int((~z.documented_stable_family).sum()),before_zero_additions=int(a.before_quantity.eq(0).sum()),addition_pairs=len(a),after_zero_deletions=int(d.after_quantity.eq(0).sum()),deletion_pairs=len(d),has_prior_AUM_pairs=int(z.before_fund_aum.gt(0).sum()),same_legal_fund_isin_pairs=int(z.same_legal_fund_isin.sum())))
pd.DataFrame(rows).to_csv(D/'fund_coverage_preownership_diagnostics.csv',index=False)
for name,mask in [('documented',p.documented_stable_family),('all_candidates',p.family_candidate_stable)]:
 z=p[mask&p.in_frozen_matched_price_sample&p.valid_for_market_acquisition_description]
 print(name,'fundeventpairs',len(z),'funds',z.fund_id.nunique(),'withAUM',z.before_fund_aum.gt(0).sum(),'nonemptyBeforezeros',z.before_logical_zero.sum(),'nonemptyAfterzeros',z.after_logical_zero.sum())
 for ty,g in z.groupby('type'):
  print(ty,'pairs',len(g),'prezero',g.before_quantity.eq(0).sum(),'postzero',g.after_quantity.eq(0).sum(),'prepositive',g.before_quantity.gt(0).sum(),'maxpremcappp',g.preholding_at_after_prices_company_pp.max())
print(pd.DataFrame(rows).to_string(index=False))
print('all identities passed')
