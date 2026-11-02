from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime
O=Path(__file__).resolve().parent;C=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis');B=C/'work/open_questions_20261101'
d=pd.read_csv(O/'unit_measurement_all216.csv',parse_dates=['before','after','reference_end','reference_start']);a=pd.read_csv(O/'anchor_event_bridge_diagnostics.csv');d=d.merge(a.drop(columns=['RIC','month']),on='event_id',validate='1:1');anchors=pd.read_csv(O/'all_available_exactISIN_month_anchors.csv');old=pd.read_csv(C/'work/volume_measurement_20261102/gate_and_volume.csv',usecols=['event_id','unit_gate_pass']);d=d.merge(old.rename(columns={'unit_gate_pass':'original172_pass'}),on='event_id',validate='1:1')
ca=pd.read_csv(R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',parse_dates=['action_date'])
# Evidence rules written before any new volume/quantity join. Nonstandard entries do not derive a volume factor from prices.
source=[
 dict(RIC='LAGRb.ST',date='2020-10',precision='month',kind='ordinary_split',factor=3,url='https://www.lagercrantz.com/media/press-archive/2020/change-in-number-of-shares-and-votes-in-lagercrantz-group-ab/',read='Company notice confirms October2020 3:1, new B ISIN SE0014990966; exact ex-date not claimed'),
 dict(RIC='ANODb.ST',date='2022-05-17',precision='first_split_trading_day',kind='ordinary_split',factor=4,url='https://www.addnodegroup.com/release/share-split-in-addnode-group/',read='First split-adjusted trading17May; record18May; both classes4:1'),
 dict(RIC='HEBAb.ST',date='2022-05-18',precision='first_split_trading_day',kind='ordinary_split',factor=2,url='https://ir.hebafast.se/aktien/',read='First split-adjusted trading18May; record19May;2:1'),
 dict(RIC='KARO.ST^K22',date='2019-09-30',precision='ex_rights_day',kind='rights_after_target_quarter',factor=np.nan,url='https://www.karohealthcare.com/karo-pharma-resolves-on-a-fully-guaranteed-rights-issue-of-approximately-sek-2-billion-4/',read='Ex-rights30September2019 after June target. Does not authorize changing June ordinary units.'),
 dict(RIC='SFRG.ST',date='2022-03-01',precision='record_date',kind='rights_after_target_quarter',factor=np.nan,url='https://www.stillfront.com/en/wp-content/uploads/sites/2/2022/02/stillfront-announcement-from-the-extraordinary-general-meeting-in-stillfront-group-on-23-february-220223.pdf',read='Record1March2022 after December2021 target; primary approved EGM. Missing independent preceding same-unit anchor remains flagged.'),
 dict(RIC='BEIJb.ST',date='2023-02-27',precision='ex_rights_day',kind='rights_after_target_quarter',factor=np.nan,url='https://www.beijerref.com/investors/the-share/rights-issue-2023',read='Public search extraction: ex-rights27February2023; record28February; after December2022 target.'),
 dict(RIC='CTEK.ST',date='2023-03-08',precision='ex_rights_day_in_existing_CA_register',kind='rights',factor=np.nan,url='https://ctekgroup.com/en/investors/rights-issue/',read='March2023 rights, ordinary shares do not physically split. Target2022H2 unaffected;2023H1 baseline overlaps and remains unresolved.'),
 dict(RIC='AXFO.ST',date='2022-05-03',precision='record_date',kind='rights_in_target_quarter',factor=np.nan,url='https://www.axfood.com/newsroom/press-releases/2022/06/change-in-number-of-shares-and-votes-in-axfood-ab-publ/',read='Completed rights shares registered by June30. Supplementary issuer calendar in2021annual records May3; unable to bridge raw shares with scalar referencefactor.'),
 dict(RIC='SHOTE.ST',date='2020-06-01',precision='record_date',kind='rights_in_target_quarter',factor=np.nan,url='https://www.scandichotelsgroup.com/media/press-releases/2020/scandic-announces-the-final-terms-of-its-fully-underwritten-rights-issue/',read='6newfor7old, recordJune1, subscriptionJune3–17. Nonphysical CCH, scalar factor unresolved.'),
 dict(RIC='PEABb.ST',date='2020-12-08',precision='ex_distribution_day',kind='different_stock_distribution',factor=1,url='https://www.peab.com/financial-info/financial-summary/distribution-annehem/',read='Annehem distribution1for5, Peab ordinary unit unchanged. Independent reference and next-month volume anchors agree1; price-only diagnostic need not equal volume factor.'),
 dict(RIC='VOLVa.ST',date='2021-07',precision='payment_month',kind='extraordinary_cash_dividend',factor=1,url='https://www.volvogroup.com/en/news-and-media/events/2021/jun/extraordinary-general-meeting-2021.html',read='Extraordinary cash9.50 following UD sale, no physical share multiplier; volume anchors agree1. Exact vendor RPO metadata not retrieved.'),
 dict(RIC='VOLCARb.ST',date='2024-04-11',precision='first_ex_redemption_trading_day',kind='ordinary_plus_distinct_redemption',factor=1,url='https://www.volvocars.com/intl/media/press-releases/80B61AA5C3FC175F/',read='One surviving ordinary plus separately traded redemption share; Polestar distributed in2024. Target2022 units unchanged; volume anchors agree1. Exact vendor RPO metadata not retrieved.'),
 dict(RIC='BETSb.ST',date='2021-05-17',precision='record_date',kind='ordinary_plus_distinct_redemption',factor=1,url='https://www.betssonab.com/sites/default/files/pr/202105054773-1.pdf',read='Existing audited original confirms ordinary+redemption, latter redeemed. Reference/next-month volume anchors agree. No price-ratio factor used.'),
 dict(RIC='CATME.ST',date='2020-07-10',precision='warrant_first_trading_day',kind='hybrid_and_warrants',factor=np.nan,url='https://www.catenamedia.com/release/first-day-of-trading-in-catena-medias-warrants-and-capital-securities-and-first-day-to-exercise-warrants-for-subscription-of-shares/',read='Separate warrants/hybrid securities identified; exact reason for2019 historical price-only discrepancy not conclusively established, remains unresolved.'),
]
pd.DataFrame(source).to_csv(O/'primary_CA_evidence.csv',index=False)
# Pre-specified alternate baseline is the same frozen date range; use dates only to locate CAs.
idx=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv');cal=pd.DatetimeIndex(sorted(pd.to_datetime(idx.loc[idx.ric.eq('.OMXSBGI'),'date']).dropna().unique()));dates=pd.read_csv(R/'output/omxsb_replication_2007/events_car.csv',usecols=['event_id','AD','ED'],parse_dates=['AD','ED']);d=d.merge(dates,on='event_id',validate='1:1')
rows=[]
for z in d.itertuples():
 r=dict(zip(d.columns,z[1:]));reason=[];notes=[];evidence=[]
 mr=np.isfinite(z.month_turnover_relerror) and abs(z.month_turnover_relerror)<=.001 and z.nasdaq_month_volume>0 and z.panel_month_volume>0 and z.panel_month_sources=='tr' and z.panel_month_valid_volume_days>=z.nasdaq_month_listed_days and z.panel_month_negative_volume_days==0
 if not mr:reason.append('reference_month_nominal_turnover_or_coverage_unverified')
 factor=z.candidate_after_factor;unitmethod='reference_month_times_documented_ordinary_split'
 # Mixing raw quantities within reference month makes its aggregate factor unusable.
 mix=ca[ca.RIC.eq(z.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.ge(z.reference_start)&ca.action_date.le(z.reference_end)]
 if len(mix):
  if z.previous_anchor_basic_valid==True and z.next_anchor_basic_valid==True:
   st=pd.Timestamp(str(int(z.previous_month))+'01')+pd.offsets.MonthEnd(0);spl=ca[ca.RIC.eq(z.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.gt(st)&ca.action_date.le(z.after)];factor=z.previous_factor*spl.factor.prod();unitmethod='previous_month_anchor_plus_dated_split_reference_month_mixed';evidence.extend(spl.source);notes.append('reference_month_mixed_raw_share_units')
  else:reason.append('reference_month_mixed_units_without_valid_adjacent_anchors')
 # Standard second anchor must agree after ordinary physical splits through next anchor.
 endnext=pd.Timestamp(str(int(z.next_month))+'01')+pd.offsets.MonthEnd(0)
 afterspl=ca[ca.RIC.eq(z.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.gt(z.after)&ca.action_date.le(endnext)]
 agree_next=z.next_anchor_basic_valid==True and np.isfinite(z.next_factor) and abs(z.next_factor/(factor*afterspl.factor.prod())-1)<=.001
 if not agree_next:
  # Same-unit previous anchor independently verifies the reference factor; source dates locate next-period rights entirely AFTER target quarter.
  postrights={'OMXSB-2019H1-11':'KARO.ST^K22','OMXSB-2022H2-03':'BEIJb.ST','OMXSB-2022H2-08':'CTEK.ST'}
  agree_prev=z.previous_anchor_basic_valid==True and np.isfinite(z.previous_factor) and abs(z.previous_factor/z.month_volume_factor-1)<=.001
  if z.event_id in postrights and agree_prev and z.next_anchor_basic_valid==True:
   notes.append('next_anchor_CCH_after_target_quarter_previous_anchor_confirms_reference');evidence.extend(t['url'] for t in source if t['RIC']==z.RIC)
  else:reason.append('independent_adjacent_month_volume_factor_not_reconciled')
 # Nonphysical rights within frozen baseline to target quarter must have daily conversion, not a single global factor.
 a=int(cal.searchsorted(z.AD));bstart=cal[a-61];r['baseline_start']=bstart
 for t in source:
  if t['RIC']!=z.RIC:continue
  td=pd.Timestamp(t['date']);
  if t['kind'] in ['rights','rights_in_target_quarter'] and bstart<=td<=z.after:
   reason.append('nonphysical_rights_CCH_overlaps_measurement_interval');evidence.append(t['url'])
 # Read-only FI price consistency; never create factor from this ratio.
 pricediff=z.after_price_ratio_for_diagnostic/factor-1;r['final_after_price_factor_diagnostic_error']=pricediff
 rpo={'OMXSB-2019H2-11':'PEABb.ST','OMXSB-2020H2-27':'VOLVa.ST','OMXSB-2022H1-11':'VOLCARb.ST','OMXSB-2021H1-12':'BETSb.ST'}
 if not np.isfinite(pricediff) or abs(pricediff)>.02:
  if z.event_id in rpo and agree_next:
   notes.append('documented_nonphysical_distribution_price_volume_factors_differ');evidence.extend(t['url'] for t in source if t['RIC']==z.RIC)
  else:reason.append('FI_price_vs_month_volume_factor_discrepancy_unresolved')
 if z.after_close_age_days>5:reason.append('FI_quarter_price_date_stale')
 r['strict_initial_12m_gate_pass']=bool(mr and np.isfinite(r['12m_turnover_relerror']) and abs(r['12m_turnover_relerror'])<=.001 and np.isfinite(z.factor_month_vs12m_relative) and abs(z.factor_month_vs12m_relative)<=.001 and abs(pricediff)<=.02 and not ('nonphysical_rights_CCH_overlaps_measurement_interval' in reason))
 r['corrected_volume_factor_to_FI_after']=factor if not reason else np.nan;r['candidate_volume_factor_even_if_fail']=factor;r['factor_method']=unitmethod;r['unit_gate_pass']=not reason;r['exclusions']=';'.join(sorted(set(reason)));r['unit_notes']=';'.join(notes);r['additional_primary_sources']='|'.join(sorted(set(evidence)));r['adjacent_anchor_agreement']=agree_next
 rows.append(r)
x=pd.DataFrame(rows);assert len(x)==216 and not x.event_id.duplicated().any();x.to_csv(O/'unit_gate_all216.csv',index=False)
# Do not load fund-demand outcomes in the gate script.
lock=dict(frozen_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),N=216,unit_pass=int(x.unit_gate_pass.sum()),reviews=int(x[x.unit_gate_pass].review_cycle.nunique()),files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'DECISIONS.txt',O/'QA_AMENDMENT_BEFORE_ASSOCIATIONS.txt',Path(__file__),O/'primary_CA_evidence.csv',O/'unit_gate_all216.csv',O/'unit_measurement_all216.csv',O/'all_available_exactISIN_month_anchors.csv']},new_volume_quantity_associations_loaded=False)
(O/'UNIT_GATE_LOCK.json').write_text(json.dumps(lock,indent=2));print('PASS',x.unit_gate_pass.value_counts().to_dict());print(pd.crosstab(x.original172_pass,x.unit_gate_pass));print(x[~x.unit_gate_pass][['event_id','RIC','exclusions']].to_string(index=False))
