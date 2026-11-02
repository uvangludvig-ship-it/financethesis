"""Strict historical Main Market candidate pool, identification only; no prices/outcomes read."""
from pathlib import Path
import os
import pandas as pd,json,re,hashlib
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]));D=Path(__file__).parent;W=D.parent
ro=pd.read_csv(W/'eligibility/dated_stockholm_instrument_roster.csv')
static_path=R/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv';universe_path=R/'data/raw/lseg/panel_2005_2026/td_universe.csv';alias_path=R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json';panel_path=R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet'
st=pd.read_csv(static_path).fillna('');tu=pd.read_csv(universe_path).fillna('');aliases=json.load(open(alias_path))
# Read identifiers only. All quoted histories retained without using their returns/coverage.
panel_rics=set(pd.read_parquet(panel_path,columns=['ric']).ric.dropna().astype(str));stock_rics={r for r in panel_rics if re.search(r'\.ST(?:\^.*)?$',r)}
rows=[]
for df,riccol,source in [(st,'ric','stocks_static_2005.csv'),(tu,'RIC','td_universe.csv')]:
 for x in df.to_dict('records'):
  ric=x[riccol];isin=str(x.get('IssueISIN',''))
  if ric in stock_rics and len(isin)==12:rows.append(dict(ric=ric,isin=isin,evidence_type='exact_static_ISIN',evidence_source=source,vendor_name=x.get('DTSubjectName',''),vendor_ticker=x.get('TickerSymbol','')))
for ric,ss in aliases.items():
 if ric in stock_rics:
  for isin in ss:rows.append(dict(ric=ric,isin=isin,evidence_type='previously_validated_ordinary_historical_ISIN_chain',evidence_source=str(alias_path.relative_to(R)),vendor_name='',vendor_ticker=''))
manual=[('NYFO.ST','SE0011426428','https://view.news.eu.nasdaq.com/view?id=bf5badbacea6190ca2736e6094e4251c6&lang=en&src=rss'),('MAHAa.ST','SE0008374383','https://investors.keocapital.com/about-us/')]
for ric,isin,url in manual:
 if ric in stock_rics:rows.append(dict(ric=ric,isin=isin,evidence_type='primary_confirmed_unchanged_ISIN_rename',evidence_source=url,vendor_name='',vendor_ticker=''))
ev=pd.DataFrame(rows);ev.to_csv(D/'RIC_ISIN_evidence.csv',index=False)
link=ev.groupby(['ric','isin'],as_index=False).agg(evidence_type=('evidence_type',lambda x:' | '.join(sorted(set(x)))),evidence_source=('evidence_source',lambda x:' | '.join(sorted(set(x)))),vendor_names=('vendor_name',lambda x:' | '.join(sorted(set(x)-{''}))),vendor_tickers=('vendor_ticker',lambda x:' | '.join(sorted(set(x)-{''}))))
ro['review']=ro.month.astype(str).str[:4]+ro.month.astype(str).str[4:].map({'04':'H1','10':'H2'})
ro['other_nonordinary_name_flag']=(ro.instrument.fillna('')+' '+ro.ticker.fillna('')).str.contains(r'\b(?:PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)\b',case=False,regex=True)
ro['strict_instrument_screen']=ro.stock_type&ro.listed_at_month_end&~ro.preference_name_flag&~ro.other_nonordinary_name_flag
joined=ro.merge(link,on='isin',how='inner',validate='many_to_many')
# More than one matched historical ISIN for the same RIC/review indicates an unresolved
# instrument chain, not permission to select a convenient share class or return series.
cnt=joined.groupby(['review','ric']).isin.nunique().rename('matched_distinct_ISINs_for_RIC_review');joined=joined.merge(cnt,on=['review','ric']);joined['mapping_unambiguous']=joined.matched_distinct_ISINs_for_RIC_review.eq(1)
joined['strict_eligible_pool']=joined.strict_instrument_screen&joined.mapping_unambiguous
joined['status']=joined.apply(lambda x:'confirmed_main_stock' if x.strict_eligible_pool else ('unresolved_multiple_instruments_for_RIC_review' if not x.mapping_unambiguous else 'confirmed_not_main_or_ineligible'),axis=1)
# Nasdaq's dated company_code identifies the issuer grouping. No RIC-stem guess.
joined['nasdaq_isin']=joined['isin']
joined['issuer_key']=joined.review+':'+joined.company_code.astype(str)
joined['instrument_alias_key']=joined.review+':'+joined['isin']
joined['same_instrument_RIC_count']=joined.groupby(['review','isin']).ric.transform('nunique')
joined['same_instrument_RIC_alternatives']=joined.groupby(['review','isin']).ric.transform(lambda x:';'.join(sorted(set(x))))
joined['RIC_quote_selected']=False;joined['full_OMXSB_eligibility_verified']=False
joined=joined.sort_values(['review','company_code','isin','ric']);joined.to_csv(D/'all_exact_links_including_excluded.csv',index=False)
pool=joined[joined.strict_eligible_pool].copy();pool.to_csv(D/'strict_historical_main_stock_pool.csv',index=False)
pool[['review','ric','company_code','issuer_key','nasdaq_isin','isin','ticker','instrument','reference_date','publication_timestamp','source_url','source_sheet','source_excel_row','evidence_type','evidence_source','same_instrument_RIC_count','same_instrument_RIC_alternatives']].to_csv(D/'review_RIC_control_pool.csv',index=False)
ali=pool[pool.same_instrument_RIC_count.gt(1)].copy();ali.to_csv(D/'same_instrument_quote_alternatives.csv',index=False)
matched=set(link.ric);pd.DataFrame({'ric':sorted(stock_rics-matched),'status':'unresolved_no_static_or_validated_historical_ISIN'}).to_csv(D/'panel_RIC_without_identifier_evidence.csv',index=False)
records=[]
for review,z in ro.groupby('review'):
 j=joined[joined.review.eq(review)];p=pool[pool.review.eq(review)];records.append(dict(review=review,source_stockholm_rows=len(z),source_screened_main_stock_ISINs=z[z.strict_instrument_screen]['isin'].nunique(),strict_pool_RICs=p.ric.nunique(),strict_pool_instruments=p['isin'].nunique(),strict_pool_company_codes=p.company_code.nunique(),instruments_with_multiple_RICs=p.loc[p.same_instrument_RIC_count.gt(1),'isin'].nunique(),excluded_ambiguous_RICs=j.loc[~j.mapping_unambiguous,'ric'].nunique(),source_eligible_ISINs_without_safe_panel_link=len(set(z.loc[z.strict_instrument_screen,'isin'])-set(p['isin']))))
s=pd.DataFrame(records);s.to_csv(D/'coverage_by_review.csv',index=False)
assert not pool.duplicated(['review','ric']).any()
assert pool.groupby(['review','ric'])['isin'].nunique().max()==1
assert pool.strict_instrument_screen.all()
# NYFO/ALTRA and MAHA/KEOC should remain alternatives where both histories exist.
audit=dict(all_panel_RICs=len(panel_rics),Stockholm_panel_RICs=len(stock_rics),Stockholm_RICs_with_any_exact_identity=len(matched),strict_pool_rows=len(pool),reviews=pool.review.nunique(),unique_pool_RICs=pool.ric.nunique(),selected_quote_count=int(pool.RIC_quote_selected.sum()),identification_only=True,no_price_or_return_columns_read=True)
(D/'validation.json').write_text(json.dumps(audit,indent=2));paths=[Path(__file__),W/'eligibility/dated_stockholm_instrument_roster.csv',static_path,universe_path,alias_path];(D/'source_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2))
print(json.dumps(audit,indent=2));print(s.to_string(index=False));print('\nALIAS EXAMPLES\n',ali[ali.ric.isin(['NYFO.ST','ALTRAF.ST','MAHAa.ST','KEOC.ST'])][['review','ric','isin','company_code','same_instrument_RIC_alternatives']].tail(12).to_string(index=False))
