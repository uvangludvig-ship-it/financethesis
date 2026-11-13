import os
from pathlib import Path
import pandas as pd, numpy as np, re, json, hashlib
BASE=Path(__file__).resolve().parent
CHAT=BASE.parents[1]
REPO=Path(os.environ.get('FINANCETHESIS_REPO', str(Path(__file__).resolve().parents[3])))
Q=REPO/'output/omxsb_open_questions_20261102/demand_quarter'
# Documents classify strategies independently of event position changes.
CAND={51482:'SPP/Storebrand Sverige',56020:'KPA Etisk Blandfond2 / KPA Blandfond',60330:'GodFond Sverige och Världen',51080:'Swedbank Robur Access Edge Sweden',51437:'Institutionella Aktiefonden Sverige',52163:'Swedbank Robur Access Mix',60029:'Öhman Etisk Index Sverige / Marknad Sverige Bred',60293:'Nordea Sverige Passiv',60310:'Länsförsäkringar Sverige Index',60320:'Nordnet Sverige Index',60479:'Handelsbanken Sverige OMXSB Index / Sverige100',60824:'Swedbank Robur Access Sverige',60967:'Öhman/Lannebo Marknad Sverige'}
ORIG={60293,60320,52163,60824,60967,51437,60718,51615,51617,51613,51619,51621,60310,51128}
SOURCES=[
('S1','Nordnet2019ENF','2019-04-29','2019 onward subject toS2','https://www.fondbolagen.se/globalassets/aktuellt/nyheter/2019/190429-uttalande-om-e.-ohman-jor-fonder-abs-marknadforing-av-fond.pdf','PDFp1–2; actual2019fundfact-sheet OMXSBGI index mandate; read local saved source'),
('S2','Nordnet annual2022','2023','2014-07-01/2022-06-01 changes explicitly historical','https://nordnetab.com/wp-content/uploads/2023/05/Arsberattelse-Nordnet-Indexfond-Sverige-ESG-2022.pdf','PDFp4; OMXSBGI until2022-06-01 thenOMXSBESGGI; managertransfer2022-10-01 samefund; local source'),
('S3','Nordea historical changes','2019-03-12;2022-04-01','index-near process2019-03-01; merger2022-06-17','https://www.nordea.se/privat/produkter/spara-investera/fonder/andringar-fonder-arkiv.html','Relevant2019and2022paragraphs read; publishedbefore events; no proof exact target weights. Stableprocess carriedforward subject toFIbenchmarkregime'),
('S4','Öhman index objective history and switch','2022;2026-03-20','2006–2022-11-30 historical indexfund objective','https://www.folksam.se/media/ohman.sverige2022_tcm5-64570.pdf','Bothpages read; companion primarybrochure https://cms-media.lannebo.se/sv/fonder/informationsbroschyr-ohman-marknad-sverige-bred.pdf p15 explicitlystart2006,indexswitch30Nov2022. Historicalreconstruction, notthenpublicforecastdata.'),
('S5','Handelsbanken2017semiannual','2017','2017observed; carryforwardto2019Q3 usingFI','https://www.handelsbanken.se/tron/public/info/contents/v1/document/35-47806','PDFp89investmentfocus/portfolio read: holdsallOMXSBstocks. 2019Q4FIbenchmarkSolactive; exactswitchdaynotsecured.'),
('S6','LF2021semiannual','2021','2021 firsthalf documented, carryforwarduntil12May2022','https://mb.cision.com/Main/152/3400491/1456826.pdf','PDFp52 read: indexnear OMXSBcap withexclusions; derivativesused; nohistoricalweightmap.'),
('S7','LFdatedbenchmarktimeline','current; dateshistorical','2022-05-12and2025-06-16','https://fund-performance.auxality-portal.com/sv/Lansforsakringar/past?currency=SEK&id=SE0002656611','Previously audited timeline; primaryissuerannouncement11May2022 https://news.cision.com/se/lansforsakringar/r/lansforsakringar-startar-egen-forvaltning-av-indexfonder---nytt-index-ger-halverat-co2-utslapp,c3565138 ; metadata confirmsquarterregimes. Customweightsunknown.'),
('S8','AccessEdgeParisclimate strategy','2020-09-24','2020-09-24forward withcontinuityassumption','https://mb.cision.com/Main/67/3201573/1310060.pdf','PrimarySwedbankpressrelease:climatefilter,notexactreplication; https://news.cision.com/se/swedbank/r/swedbank-robur-klassificerar-flera-fonder-i-linje-med-parisavtalet%2Cc3201573'),
('S9','OhmanMarknad2025annual','2026','2025only','https://cms-media.lannebo.se/sv/fonder/arsberattelse-ohman-marknad-sverige.pdf','PDFp2–4read currentfile is2025NOT2024 despitecachedsearchsnippet. Indexnear,ESGtiltandrelativeoverweights. Neverbackcaststrategyfromthis.'),
('S10','Nordea2025annual under2024URL','2026','2025only; historicalbenchmarktable separate','https://www.nordea.se/Images/154-495669/Nordea%20Hela%CC%8Arsrapport%202024%201.pdf','LocalPDFprintedp474–475and567–568read: bothpassivemandates in2025; historicalbenchmark/passive-name/active-sharetable2016–25 supportsbenchmarkhistory but not historicaleverytargetweight. MutableURLisNOT2024document.'),
('S11','SwedbankAccessSverige currentannual','current','pendingread','https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE37492932','Web403; currentfundpageindexnear https://swedbankrobur.fondlista.se/sv/details/SE0007074075 ; doNOTbackcast.'),
('S12','SwedbankAccessMix currentdescription','current','currentonly','https://swedbankrobur.fondlista.se/sv/details/SE0000434359','Indexnear50/50equitybondportfolio. FIhistoricalmixedbenchmark available; strategyhistorynotfullyverified.'),
('S13','Storebrand2024semiannual','2024','2024documented; forwardcontinuityusingFI','https://www.storebrandfonder.se/globalassets/dokument/finansiell-information/halvarsredogorelse-2024-storebrand-fonder-ab.pdf','PDFp83printed81StorebrandSverigereadindexnearSBXCAPwithexclusions; GodFondprinted139 descriptionindexnear globalwithSwedishsleeve; source searchexcerptplusFIbenchmark. Earlierstrategyhistoryunverified.'),
('S14','KPAcurrentprimarydescription','2026current','currentonly','https://swedbankrobur.fondlista.se/sv/details/SE0000885089','Explicitpassiveindexnearquantitative1/3Swedish,1/3global,1/3bonds. Cannotbackcast. KPAAktiefond separatelyexplicitactive https://swedbankrobur.fondlista.se/sv/details/SE0000885105 soNOTadded.'),
('FI','FI contemporaneous originalreports','quarterend','2018Q4–2026Q2','repo/data/derived/fi/fi_holdings_long.csv.gz','Actualbenchmark,name,fundISINandpositions; benchmarkaloneNOTpassivemandate.')]
pd.DataFrame(SOURCES,columns=['source_id','title','publication_date_or_precision','historical_scope','url','read_scope_and_limit']).to_csv(BASE/'source_ledger.csv',index=False)
meta=pd.read_csv(REPO/'code/claude_checks/data/fi_all_funds_klass.csv')
meta['fund_id']=meta.fund_id.astype(int)
meta['family_screen']=meta.jmf.fillna('').str.contains(r'OMX.?S.?B|OMX Stockholm Benchmark|OMX SBX|Stockholm Benchmark|SBX INDEX',case=False,regex=True)
census=[]
for f,g in meta[meta.family_screen].groupby('fund_id'):
 census.append(dict(fund_id=f,last_name=g.namn.iloc[-1],first_quarter=g.q.min(),last_quarter=g.q.max(),quarters=len(g),candidate=f in CAND,original14=f in ORIG,review_status='candidate_detailed' if f in CAND else 'mixed_or_active_or_unknown_NOT_proven_tracker',benchmarks=' | '.join(g.jmf.dropna().unique())))
pd.DataFrame(census).to_csv(BASE/'all_FI_family_benchmark_census.csv',index=False)
rawmeta=pd.read_csv(Q/'raw_fund_report_metadata.csv').rename(columns={'Fond_institutnummer':'fund_id','Kvartalsslut':'date'})
events=pd.read_csv(Q/'events_locked.csv')
# No return columns loaded.
prices=pd.read_csv(REPO/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',usecols=['event_id','ric','review','AD','ED','common100'])
priceids=set(prices.event_id)
events['in_frozen_matched_price_sample']=events.event_id.isin(priceids)
# Starting canonical quarter ledger; 216 events, explicitly balanced reports and validated zeroes.
ledger=pd.read_csv(Q/'fund_event_quarter_changes.csv.gz')
assert ledger.event_id.nunique()==216 and not ledger.duplicated(['event_id','fund_id']).any()
assert np.allclose(ledger.delta_company_pp,100*(ledger.after_quantity-ledger.factor*ledger.before_quantity)*ledger.fi_price_after/ledger.company_mcap_after)
# Universe of fund/event candidate rows includes missing/ambiguous rows rather than disappearing them.
panel=events.merge(pd.DataFrame({'fund_id':sorted(set(CAND)|ORIG)}),how='cross')
shared=['event_id','fund_id']
new=[c for c in ledger if c not in panel or c in shared]
panel=panel.merge(ledger[new],on=shared,how='left',validate='1:1')
for side in ['before','after']:
 m=rawmeta.rename(columns={'date':side,'name':f'{side}_fund_name','fund_isin':f'{side}_fund_isin','benchmark':f'{side}_benchmark','actual_instrument_rows':f'{side}_report_instrument_rows','raw_rows':f'{side}_raw_rows'})
 panel=panel.merge(m,on=['fund_id',side],how='left',validate='m:1')
 a=meta[['fund_id','kvartal','aum']].rename(columns={'kvartal':side,'aum':f'{side}_fund_aum'})
 assert not a.duplicated(['fund_id',side]).any()
 panel=panel.merge(a,on=['fund_id',side],how='left',validate='m:1')

def family(x):
 s=str(x).upper()
 if 'MORNINGSTAR' in s:return 'other_Morningstar'
 if 'SOLACTIVE' in s:return 'other_Solactive'
 if 'SIXPRX' in s:return 'other_SIXPRX'
 if not any(z in s for z in ['OMXSB','SBX','STOCKHOLM BENCHMARK','STOCKHOLM CAPPED BENCHMARK']):return 'unknown_or_other'
 if 'CUSTOM' in s:return 'OMXSB_custom'
 if 'ESG' in s:return 'OMXSB_ESG'
 if 'OMRX' in s:return 'OMXSB_cap_mixed_sleeve' if 'CAP' in s else 'OMXSB_standard_mixed_sleeve'
 if 'CAP' in s:return 'OMXSB_cap'
 return 'OMXSB_standard'

def classify(r):
 f=int(r.fund_id); b=r.before; a=r.after
 bef=family(r.before_benchmark); aft=family(r.after_benchmark)
 candidate=f in CAND
 tier='mixed_or_strategy_unverified'; src='FI'; style='unknown'; continuity=False
 if candidate:
  tier='FI_candidate_strategy_history_unverified'; style='index_or_near_candidate'
 if f in {51482,60330}:
  src='S13;FI';style='index_near_history_incomplete'
  if b>='2024-01-01':tier='documented_index_near';style='index_near';continuity=True
 if f==56020:src='S14;FI';style='passive_mixed_current_history_unverified'
 if f==60320:tier='documented_index_family';src='S1;S2;FI';style='index';continuity=True
 if f==51437:tier='documented_index_near';src='S3;FI';style='index_near';continuity=True
 if f==60029 and a<'2022-11-30':tier='documented_index_near';src='S4;FI';style='index_near';continuity=True
 if f==60479 and a<='2019-09-30':tier='documented_index_family';src='S5;FI';style='index';continuity=True
 if f==60310 and b>='2021-01-01' and a<'2022-05-12':tier='documented_index_near';src='S6;S7;FI';style='index_near';continuity=True
 if f==60310 and b>='2025-06-16':tier='documented_index_family';src='S7;FI';style='index';continuity=True
 if f==51080 and b>='2020-09-24':tier='FI_candidate_strategy_history_unverified';src='S8;FI';style='climate_strategy_documented_index_objective_history_unverified';continuity=False
 if f==60293 and b>='2025-01-01':tier='documented_index_family';src='S10;FI';style='index';continuity=False
 if f==60967 and b>='2025-01-01':tier='documented_index_near';src='S9;FI';style='index_near';continuity=False
 # Explicit benchmarks can disqualify family membership regardless of fund name.
 transition=bef!=aft
 if candidate and bef.startswith('other_') and aft.startswith('other_'):tier='different_benchmark'
 if f in {51128,51613,51615,51617,51619,51621,60718} and b>='2025-01-01':tier='documented_active_mixed';src='S10;FI';style='active_mixed'
 # Changes of labels CAP wording not genuine benchmark change? AccessMix documentedGross→CAP within2019Q2 is actualregimechange.
 if f==60320 and b<'2022-06-01'<=a:transition=True
 if f==60310 and any(b<x<=a for x in ['2022-05-12','2025-06-16']):transition=True
 if f==60029 and b<'2022-11-30'<=a:transition=True
 merger=f==51437 and b<'2022-06-17'<=a
 valid=pd.notna(r.delta_company_pp)
 status='valid_position_pair' if valid else 'missing_or_ambiguous_pair'
 if not(pd.notna(r.before_report_instrument_rows) and r.before_report_instrument_rows>0):status='no_nonempty_before_report'
 elif not(pd.notna(r.after_report_instrument_rows) and r.after_report_instrument_rows>0):status='no_nonempty_after_report'
 if merger:status='fund_merger_not_market_purchase'
 stablefamily=bef.startswith('OMXSB') and aft.startswith('OMXSB') and not transition
 return pd.Series(dict(candidate=candidate,original14=f in ORIG,benchmark_before_regime=bef,benchmark_after_regime=aft,mandate_evidence=tier,strategy=style,source_ids=src,continuity_assumption=continuity,benchmark_transition=transition,fund_merger=merger,measurement_status=status,stable_family=stablefamily,documented_stable_family=stablefamily and tier in {'documented_index_family','documented_index_near'},family_candidate_stable=stablefamily and candidate,stock_specific_ESG_target_known=False,target_weight_before_known=False,target_weight_after_known=False))
panel=pd.concat([panel,panel.apply(classify,axis=1)],axis=1)
panel['benchmark_raw_text_changed']=panel.before_benchmark.fillna('').ne(panel.after_benchmark.fillna(''))
panel['fund_name_canonical']=panel.fund_id.map(CAND).fillna(panel.before_fund_name)
panel['valid_for_market_acquisition_description']=panel.delta_company_pp.notna() & ~panel.fund_merger
panel['preholding_at_after_prices_company_pp']=100*panel.before_quantity*panel.factor*panel.fi_price_after/panel.company_mcap_after
panel['conditional_liquidation_company_pp']=np.where(panel.type.eq('deletion'),-panel.preholding_at_after_prices_company_pp,np.nan)
panel['mechanical_prediction_status']='unidentified_target_weights_and_stock_eligibility'
panel.loc[panel.type.eq('deletion')&panel.documented_stable_family,'mechanical_prediction_status']='conditional_prior_position_liquidation_only_not_proven_target'
panel['predicted_mechanical_company_pp']=np.nan
panel['public_availability_before_event_audited']=False
panel['real_time_forecast_valid']=False
panel['after_zero_observed']=np.where(panel.delta_company_pp.notna(),panel.after_quantity.eq(0),np.nan)
panel['before_zero_observed']=np.where(panel.delta_company_pp.notna(),panel.before_quantity.eq(0),np.nan)
panel.to_csv(BASE/'fund_event_demand_panel.csv.gz',index=False,compression='gzip')
# Keep classifications/coverage separate before opening group outcomes.
periodcols=['fund_id','review_cycle','before','after','fund_name_canonical','before_fund_name','after_fund_name','before_fund_isin','after_fund_isin','before_benchmark','after_benchmark','before_fund_aum','after_fund_aum','benchmark_before_regime','benchmark_after_regime','mandate_evidence','strategy','source_ids','continuity_assumption','benchmark_transition','fund_merger','stable_family','documented_stable_family','family_candidate_stable']
periods=panel[periodcols].drop_duplicates()
assert not periods.duplicated(['fund_id','review_cycle']).any()
periods.to_csv(BASE/'fund_review_mandate_manifest.csv',index=False)
# Fixed definitions, zero all other funds, but exclusions are explicitly recorded; not lower/upperbounds.
defs={
 'documented_stable_family_subset':panel.documented_stable_family,
 'additional_FI_family_candidates':panel.family_candidate_stable & ~panel.documented_stable_family,
 'all_stable_family_candidates_sensitivity':panel.family_candidate_stable,
 'candidate_transition_quarters_separate':panel.candidate & panel.benchmark_transition,
 'original14_audit_comparator':panel.original14,
}
outs=[]
for gn,mask in defs.items():
 g=panel[mask & panel.valid_for_market_acquisition_description].copy()
 g['positive_net_change']=g.delta_company_pp.clip(lower=0)
 g['negative_net_change']=g.delta_company_pp.clip(upper=0)
 g['positive_net_from_zero_preposition']=g.positive_net_change.where(g.before_quantity.eq(0),0)
 g['positive_net_from_existing_preposition']=g.positive_net_change.where(g.before_quantity.gt(0),0)
 sums=g.groupby('event_id').agg(net_company_pp=('delta_company_pp','sum'),positive_company_pp=('positive_net_change','sum'),negative_company_pp=('negative_net_change','sum'),positive_from_zero_pp=('positive_net_from_zero_preposition','sum'),positive_from_existing_pp=('positive_net_from_existing_preposition','sum'),preholding_pp=('preholding_at_after_prices_company_pp','sum'),n_funds=('fund_id','nunique'),n_zero_before=('before_quantity',lambda v:(v==0).sum()),n_zero_after=('after_quantity',lambda v:(v==0).sum()))
 e=events.merge(sums,on='event_id',how='left');e['definition']=gn
 # A review with no qualifying mandate is unavailable, not demand0.
 expected=panel[mask].groupby('event_id').size(); e['n_expected_candidates']=e.event_id.map(expected).fillna(0).astype(int)
 e['n_excluded_or_unavailable_pairs']=e.n_expected_candidates-e.n_funds.fillna(0)
 outs.append(e)
res=pd.concat(outs,ignore_index=True)
assert np.allclose(res.net_company_pp.dropna(),(res.positive_company_pp+res.negative_company_pp).dropna())
parts=res.pivot(index='event_id',columns='definition',values='net_company_pp')
assert np.allclose(parts.documented_stable_family_subset+parts.additional_FI_family_candidates,parts.all_stable_family_candidates_sensitivity,equal_nan=True)
res.to_csv(BASE/'event_demand_by_definition.csv',index=False)
reviews=[];summaries=[]
cols=['net_company_pp','positive_company_pp','negative_company_pp','positive_from_zero_pp','positive_from_existing_pp','preholding_pp','n_funds','n_excluded_or_unavailable_pairs']
for sample,mask in [('all216',res.event_id.notna()),('frozen_matched_price_sample',res.in_frozen_matched_price_sample)]:
 t=res[mask]
 r=t.groupby(['definition','type','review_cycle'])[cols].mean().reset_index();r['sample']=sample
 reviews.append(r)
 for (definition,typ),g in r.groupby(['definition','type']):
  e=t[t.definition.eq(definition)&t.type.eq(typ)]
  d=dict(sample=sample,definition=definition,type=typ,N_events=int(e.net_company_pp.notna().sum()),G_reviews=int(g.net_company_pp.notna().sum()))
  for c in cols:d[c]=g[c].mean()
  d['zero_preposition_share_of_positive_net']=d['positive_from_zero_pp']/d['positive_company_pp'] if d['positive_company_pp']>0 else np.nan
  summaries.append(d)
pd.concat(reviews).to_csv(BASE/'review_demand_by_definition.csv',index=False)
s=pd.DataFrame(summaries);s.to_csv(BASE/'summary_review_weighted_NO_PVALUES.csv',index=False)
coverage=panel.groupby(['fund_id','fund_name_canonical','mandate_evidence','measurement_status']).agg(N=('event_id','size'),events_in_price_sample=('in_frozen_matched_price_sample','sum')).reset_index()
coverage.to_csv(BASE/'coverage_and_exclusions.csv',index=False)
# No merger/invalid pairs allowed in acquisition summaries, retainquantitiesrawpanel withflag.
checks=dict(events=events.shape[0],additions=int(events.type.eq('addition').sum()),deletions=int(events.type.eq('deletion').sum()),reviews=events.review_cycle.nunique(),fund_candidate_count=len(CAND),FI_ever_family_benchmark_IDs=len(census),audited_fund_event_panel_rows=len(panel),matched_price_events=int(events.in_frozen_matched_price_sample.sum()),matched_price_additions=int((events.in_frozen_matched_price_sample&events.type.eq('addition')).sum()),matched_price_deletions=int((events.in_frozen_matched_price_sample&events.type.eq('deletion')).sum()),merger_rows=int(panel.fund_merger.sum()),fund_merger_source='S3',price_outcomes_loaded=False,mechanical_predictions_available=int(panel.predicted_mechanical_company_pp.notna().sum()),all_quantity_identity_pass=True)
(BASE/'validation.json').write_text(json.dumps(checks,indent=2))
inputs=[Q/'fund_event_quarter_changes.csv.gz',Q/'events_locked.csv',Q/'raw_fund_report_metadata.csv',REPO/'code/claude_checks/data/fi_all_funds_klass.csv',REPO/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',Path(__file__),BASE/'ANALYSIS_DECISIONS.txt']
(BASE/'source_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2))
print(json.dumps(checks,indent=2))
print(s[s['sample'].eq('frozen_matched_price_sample')][['definition','type','N_events','G_reviews','net_company_pp','positive_company_pp','negative_company_pp','zero_preposition_share_of_positive_net']].to_string(index=False))
