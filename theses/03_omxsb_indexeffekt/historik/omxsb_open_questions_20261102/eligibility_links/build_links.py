from pathlib import Path
import os
import pandas as pd,numpy as np,json,re,unicodedata
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]));D=Path(__file__).parent;W=D.parent
ro=pd.read_csv(W/'eligibility/dated_stockholm_instrument_roster.csv');tu=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/td_universe.csv').fillna('');st=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv').fillna('')
a=json.load(open(R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json'))
t=pd.read_csv(R/'output/omxsb_robusthet_20261101/T2_matches.csv',usecols=['event_id','review','ric','c1_ric','c2_ric','c3_ric']);t=t[t.review.str[:4].astype(int).ge(2017)]
clean=pd.read_csv(W/'persistence_validation/identity_corrected_primary_events.csv',usecols=['event_id','review','ric','c1_ric','c2_ric','c3_ric','AD','ED']);assert len(clean)==139
master=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',usecols=['event_id','announcement_date','effective_date']);t=t.merge(master,on='event_id',validate='one_to_one').rename(columns={'announcement_date':'AD','effective_date':'ED'})
# Two primary-source-confirmed unchanged-ISIN name/ticker aliases. No price similarity rule.
manual={'NYFO.ST':('SE0011426428','https://view.news.eu.nasdaq.com/view?id=bf5badbacea6190ca2736e6094e4251c6&lang=en'),'MAHAa.ST':('SE0008374383','https://view.news.eu.nasdaq.com/view?id=b52a78d490c9dabac52116c623c7199fd&lang=en')}
ids={};sources={};names={};symbols={}
for df,rcol in [(tu,'RIC'),(st,'ric')]:
 for x in df.to_dict('records'):
  ric=x[rcol];i=str(x.get('IssueISIN',''));n=str(x.get('DTSubjectName',''));sy=str(x.get('TickerSymbol',''))
  if i and len(i)==12:ids.setdefault(ric,set()).add(i);sources.setdefault((ric,i),set()).add('LSEG_static_exact_ISIN')
  if n:names.setdefault(ric,set()).add(n)
  if sy:symbols.setdefault(ric,set()).add(sy)
for ric,ss in a.items():
 for i in ss:ids.setdefault(ric,set()).add(i);sources.setdefault((ric,i),set()).add('previously_validated_ordinary_historical_ISIN_chain')
for ric,(i,url) in manual.items():ids.setdefault(ric,set()).add(i);sources.setdefault((ric,i),set()).add('primary_unchanged_ISIN_alias:'+url)
def ns(s):return re.sub('[^A-Z0-9]','',str(s).upper())
def nn(s):
 s=unicodedata.normalize('NFKD',str(s).upper());s=''.join(c for c in s if not unicodedata.combining(c));s=re.sub(r'\b(?:SER\.?|SERIE|SERIES|CLASS)\s+[A-Z]\b',' ',s);s=re.sub(r'\b(?:AKTIEBOLAG|AB|PUBL|PUBLIC|PLC|LTD|LIMITED|INC|OYJ|ASA|AG|CORPORATION)\b',' ',s);return ns(s)
# Reference date is April30/October31; use true release timestamps separately.
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',usecols=['ric','date','close']);cal=pd.DatetimeIndex(pd.to_datetime(ix.loc[ix.ric.eq('.OMXSBGI')&ix.close.notna(),'date']).sort_values().unique())
rows=[]
for x in t.itertuples():
 month=int(x.review[:4]+('04' if x.review.endswith('H1') else '10'));rr=ro[ro.month.eq(month)];AD=pd.Timestamp(x.AD);pos=cal.searchsorted(AD);asof=cal[pos-2] if pos>=2 else pd.NaT
 for role in ['ric','c1_ric','c2_ric','c3_ric']:
  ric=getattr(x,role);base=dict(event_id=x.event_id,review=x.review,role='event' if role=='ric' else role[:2],ric=ric,month=month,AD=x.AD,ED=x.ED,control_characteristics_date=str(asof.date()),clean_primary=x.event_id in set(clean.event_id),known_ISINs=';'.join(sorted(ids.get(ric,set()))),vendor_names=' | '.join(sorted(names.get(ric,set()))),vendor_symbols=' | '.join(sorted(symbols.get(ric,set()))))
  cand=rr[rr['isin'].isin(ids.get(ric,set()))];method='exact_ISIN';proof=''
  if len(cand)==0:
   sy={ns(s) for s in symbols.get(ric,set())};na={nn(n) for n in names.get(ric,set())}
   cand=rr[rr.ticker.map(ns).isin(sy)&rr.instrument.map(nn).isin(na)]
   method='exact_vendor_symbol_AND_normalized_full_issuer_name_class_preserved_by_symbol'
  if len(cand)!=1:
   base.update(status='unresolved',reason='no_unique_dated_security_identity_match',candidate_count=len(cand),mapping_method=method)
  else:
   z=cand.iloc[0];i=z['isin'];proof=' | '.join(sorted(sources.get((ric,i),set()))) if method=='exact_ISIN' else 'Exact dated Nasdaq ticker + normalized complete legal name against LSEG; no fuzzy similarity'
   special=bool(z.preference_name_flag) or bool(re.search(r'\b(?:PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)\b',str(z.instrument)+' '+str(z.ticker),re.I))
   eligible=bool(z.stock_type and z.listed_at_month_end and not special)
   pub=str(z.publication_timestamp);pdpub=pd.Timestamp(pub[:10])
   base.update(status='confirmed_main_stock' if eligible else 'confirmed_not_main_or_ineligible',reason='dated_Main_Market_ordinary_stock_identity_confirmed' if eligible else 'matched_security_delisted_by_month_end_or_nonordinary',candidate_count=1,mapping_method=method,identity_evidence=proof,nasdaq_isin=i,nasdaq_symbol=z.ticker,nasdaq_name=z.instrument,nasdaq_instrument_type=z.instrument_type,nasdaq_segment=z.segment,listed_at_month_end=z.listed_at_month_end,delisted=z.delisted,preference_or_other_nonordinary_flag=special,reference_date=z.reference_date,publication_timestamp=pub,publication_before_AD_date=bool(pdpub<AD),publication_on_or_before_control_characteristics_date=bool(pdpub<=asof),source_url=z.source_url,source_sheet=z.source_sheet,source_excel_row=int(z.source_excel_row),full_OMXSB_eligibility_verified=False)
  rows.append(base)
d=pd.DataFrame(rows)
# Exact ticker/name proves a promising dated issuer/class label but does not alone
# independently document a changed historical ISIN into the vendor's current chain.
d['candidate_listing_status']=d.status
d['historical_ISIN_chain_explicitly_verified']=d.mapping_method.eq('exact_ISIN')&d.status.eq('confirmed_main_stock')
weak=d.status.eq('confirmed_main_stock')&~d.mapping_method.eq('exact_ISIN')
d.loc[weak,'status']='unresolved'
d.loc[weak,'reason']='exact_dated_ticker_and_name_but_changed_historical_ISIN_chain_not_independently_verified'
# Independent exchange/issuer source, not inference from roster absence.
fn=d.ric.eq('FNOX.ST^G25')&d.month.lt(202204)
assert d.loc[fn,'status'].eq('unresolved').all()
d.loc[fn,'status']='confirmed_not_main_or_ineligible'
d.loc[fn,'reason']='issuer_and_exchange_confirm_NGM_Nordic_SME_before_2022_04_13_Main_Market_admission'
d.loc[fn,'mapping_method']='primary_source_historical_exchange_admission'
d.loc[fn,'identity_evidence']='Fortnox issuer notice13April2022: trading starts today on Main Market; previously NGM Nordic SME; unchanged ticker/ISIN at transfer'
d.loc[fn,'source_url']='https://news.cision.com/se/fortnox-ab/r/forsta-dag-for-handel-i-fortnox-aktier-pa-nasdaq-stockholm%2Cc3545654'
d.to_csv(D/'all_T2_post2017_role_links.csv',index=False);d[d.clean_primary].to_csv(D/'clean139_role_links.csv',index=False)
# Canonical per(review,RIC) mapping for parent's already-declared frozen sensitivity.
k=d.sort_values(['review','ric']).drop_duplicates(['review','ric']);k.to_csv(D/'review_RIC_status.csv',index=False)
summary=[]
for label,z in [('clean_primary139',d[d.clean_primary]),('all_T2_post2017',d)]:
 g=z.groupby('event_id').status.agg(list);summary.append(dict(sample=label,events=len(g),roles=len(z),confirmed_main_stock=int(z.status.eq('confirmed_main_stock').sum()),confirmed_not_main_or_ineligible=int(z.status.eq('confirmed_not_main_or_ineligible').sum()),unresolved=int(z.status.eq('unresolved').sum()),all_four_confirmed=int(g.map(lambda a:len(a)==4 and all(s=='confirmed_main_stock' for s in a)).sum()),event_has_confirmed_noneligible=int(g.map(lambda a:'confirmed_not_main_or_ineligible' in a).sum()),event_has_unresolved=int(g.map(lambda a:'unresolved' in a).sum())))
pd.DataFrame(summary).to_csv(D/'coverage_summary.csv',index=False);d[d.status.ne('confirmed_main_stock')].to_csv(D/'unresolved_or_ineligible.csv',index=False)
print(pd.DataFrame(summary).to_string(index=False));print('\nUNRESOLVED CLEAN\n',d[d.clean_primary&d.status.ne('confirmed_main_stock')][['event_id','role','ric','known_ISINs','vendor_names','vendor_symbols','status','reason']].to_string(index=False));print('\nmethods',d.mapping_method.value_counts().to_dict())
