"""Coverage/variation only. No price/return columns, outcomes, or hypothesis tests."""
from pathlib import Path
import json,hashlib,re,argparse
import pandas as pd,numpy as np
pa=argparse.ArgumentParser();pa.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[4]);pa.add_argument('--out',type=Path);ar=pa.parse_args();R=ar.repo.resolve();O=(ar.out or R/'output/omxsb_broadening_20261102/frontier').resolve();O.mkdir(parents=True,exist_ok=True)
FI=R/'data/derived/fi/fi_holdings_long.csv.gz';RO=R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv';ME=R/'output/omxsb_mechanism_frontier_20261102/ownership/fund_metadata_classification.csv'
ro=pd.read_csv(RO);me=pd.read_csv(ME)
reviews={f'{y}H{h}':(f'{y}-03-31'if h==1 else f'{y}-09-30',y*100+(4 if h==1 else 10))for y in range(2019,2026)for h in [1,2]}
qs={v[0]for v in reviews.values()}
cols={'Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','ISIN-kod_instrument':'isin','Antal':'quantity','Marknadsvärde_instrument':'mv','Fond_ISIN-kod':'fund_isin','Fondbolag_namn':'company','Tillgångsslag_enligt_LVF_5_kap':'asset_type'}
selected=[];types=[]
for x in pd.read_csv(FI,usecols=list(cols),chunksize=150000):
 x=x.rename(columns=cols);x=x[x.quarter.isin(qs)]
 types.append(x.groupby(['quarter','asset_type']).size().rename('rows').reset_index())
 # This is a positive-position coverage screen, not a zero-filled ownership panel.
 selected.append(x[x.asset_type.eq('ÖverlåtbartVärdepapper')])
p=pd.concat(selected,ignore_index=True);pd.concat(types).groupby(['quarter','asset_type']).rows.sum().to_csv(O/'baseline_asset_type_coverage.csv')
summary=[];stockout=[];exclusions=[]
for review,(q,month)in reviews.items():
 u=ro[ro.month.eq(month)&ro.stock_type&ro.listed_at_month_end&~ro.preference_name_flag].copy()
 dupisin=set(u.loc[u.duplicated('isin',keep=False),'isin']);u=u[~u['isin'].isin(dupisin)].copy()
 # Choose one ordinary share class per issuer using only the dated roster and
 # maximum company-cap field, then ISIN. This does not use future price availability.
 u=u.sort_values(['company_code','market_cap','isin'],ascending=[True,False,True]).drop_duplicates('company_code')
 z=p[p.quarter.eq(q)].copy();meta=me[me.quarter.eq(q)].copy()
 badfund=set(meta.loc[meta.fund_isin.notna()&meta.duplicated('fund_isin',keep=False),'fund_id'])
 z=z[z['isin'].isin(u['isin'])&~z.fund_id.isin(badfund)]
 badkeys=z.loc[z.duplicated(['fund_id','isin'],keep=False)|z.quantity.isna()|z.mv.isna()|z.quantity.lt(0)|z.mv.lt(0),['fund_id','isin']].drop_duplicates()
 if len(badkeys):
  badkeys['exclude']=True;z=z.merge(badkeys,on=['fund_id','isin'],how='left');z=z[z.exclude.isna()].drop(columns='exclude')
 z=z[z.quantity.gt(0)&z.mv.gt(0)].copy()
 z=z.merge(meta[['fund_id','label','company']],on='fund_id',how='left',validate='m:1',suffixes=('_raw','_meta'))
 missingcompany=z.company_meta.isna()|z.company_meta.str.strip().eq('');z=z[~missingcompany].copy()
 z['manager']=z.company_meta.map(lambda v:re.sub(r'\s+',' ',v.strip().lower()))
 z['omxsb_label']=z.label.fillna('').str.contains('OMXSB',case=False,regex=False)
 ids=sorted(u['isin']);mat=pd.crosstab(z['isin'],z.fund_id).reindex(ids,fill_value=0).gt(0).astype(np.int32)
 man=pd.crosstab(z['isin'],z.manager).reindex(ids,fill_value=0).gt(0).astype(np.int32)
 net=mat.values@mat.values.T;netm=man.values@man.values.T;tri=np.triu_indices(len(ids),1)
 ind=u.set_index('isin').reindex(ids).industry.fillna('<missing>').to_numpy();diffind=ind[tri[0]]!=ind[tri[1]]
 samecompany=u.set_index('isin').reindex(ids).company_code.to_numpy();assert len(set(samecompany))==len(ids)
 for isin in ids:
  zz=z[z['isin'].eq(isin)];stockout.append(dict(review=review,quarter=q,isin=isin,observed_positive_fund_owners=zz.fund_id.nunique(),observed_positive_managers=zz.manager.nunique(),positive_OMXSB_label_funds=zz.loc[zz.omxsb_label,'fund_id'].nunique()))
 summary.append(dict(review=review,baseline_quarter=q,dated_stock_roster_month=month,issuer_distinct_stock_candidates=len(ids),stocks_with_observed_FI_position=int((mat.sum(axis=1)>0).sum()),funds_with_positions=mat.shape[1],managers_with_positions=man.shape[1],pair_count=len(tri[0]),pairs_shared_fund=int((net[tri]>0).sum()),pairs_shared_manager=int((netm[tri]>0).sum()),cross_industry_pairs=int(diffind.sum()),cross_industry_pairs_shared_at_least_5_managers=int(((netm[tri]>=5)&diffind).sum()),shared_manager_count_sd=float(netm[tri].std()),median_positive_fund_owners=float(mat.sum(axis=1).median()),median_positive_managers=float(man.sum(axis=1).median()),duplicate_legal_fund_ids_excluded=len(badfund),ambiguous_or_invalid_fund_stock_pairs_excluded=len(badkeys),missing_manager_position_rows_excluded=int(missingcompany.sum()),duplicated_roster_ISINs_excluded=len(dupisin)))
 exclusions.extend(dict(review=review,fund_id=int(x.fund_id),isin=x.isin,reason='duplicate_or_missing_or_negative_quantity_or_value')for x in badkeys.itertuples())
pd.DataFrame(summary).to_csv(O/'network_baseline_coverage.csv',index=False);pd.DataFrame(stockout).to_csv(O/'network_baseline_stock_coverage.csv',index=False);pd.DataFrame(exclusions).to_csv(O/'network_baseline_exclusions.csv',index=False)
(O/'network_feasibility.json').write_text(json.dumps(dict(scope='Baseline positive-position support only, not validated complete ownership or price study.',reviews=len(summary),price_or_return_fields_read=False,postquarter_holdings_used=False,financial_results_computed=False,metadata_only=True,dated_roster_next_month_limitation='April/October roster verifies the intended review population but is not baseline-quarter listing status or evidence of public availability before the event; a network-return design must freeze/publication-align separately.',legal_fund_duplicates_and_ambiguous_position_keys_excluded=True,absent_positions_not_claimed_zero=True,ordinary_share_screen='Nasdaq Stock, listed month end, no preference-name flag; issuer dedup deterministic. This does not certify every unflagged stock is ordinary.',summary=summary,source_sha256={str(a):hashlib.sha256(a.read_bytes()).hexdigest()for a in [FI,RO,ME]}),indent=2))
print(pd.DataFrame(summary).to_string(index=False))
