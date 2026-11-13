#!/usr/bin/env python3
"""Three-quarter source/unit gate. Never calculates q1-to-q2 holding changes."""
from pathlib import Path
import argparse, datetime, hashlib, json, os
import numpy as np
import pandas as pd

ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis')));ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parent);args=ap.parse_args()
O=args.output;R=args.repo_root;O.mkdir(parents=True,exist_ok=True);(O/'private').mkdir(exist_ok=True)
if (O/'GATE_START_LOCK.json').exists():raise RuntimeError('Frozen gate already exists; use --output NEW_DIRECTORY and copy DESIGN_LOCK.txt there.')
CAP=R/'output/omxsb_contribution_round_20261103/ownership_capital'
OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership'
DQ=R/'output/omxsb_open_questions_20261102/demand_quarter'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths={'old_ledger':CAP/'normalized_fund_role_contributions.csv.gz','roles':OWN/'security_role_gate.csv','old_event_gate':DQ/'events_locked.csv','reports':DQ/'raw_fund_report_metadata.csv','ca':R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv','roster':R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv','holdings':R/'data/derived/fi/fi_holdings_long.csv.gz','panel':R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet','cancel':R/'output/omxsb_execution_followup_20261102/sources/known_cancellations.csv','events':R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv'}
start={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'source_and_unit_gate_before_new_changes','new_outcomes_computed':False,'inputs':{k:{'path':str(v),'sha256':sha(v)}for k,v in paths.items()},'design_sha256':sha(O/'DESIGN_LOCK.txt'),'code_sha256':sha(Path(__file__))}
(O/'GATE_START_LOCK.json').write_text(json.dumps(start,indent=2)+'\n')
D=pd.read_csv(paths['old_ledger'],dtype={'fund_id':str});D=D[D.type.eq('addition')&D.review.lt('2024')].copy()
assert D.event_id.nunique()==70
S=pd.read_csv(paths['roles']);S=S[S.event_id.isin(D.event_id)].copy();S['q2']=(pd.to_datetime(S.q1)+pd.offsets.QuarterEnd(1)).dt.strftime('%Y-%m-%d')
C=pd.read_csv(paths['cancel']);cancel_rows=[]
for x in S.itertuples():
 z=C[C.review.eq(x.review)&C.RIC.eq(x.ric)]
 if x.role!='event' and len(z):cancel_rows.append(dict(event_id=x.event_id,review=x.review,role=x.role,ric=x.ric,reason='known_cancelled_announcement_control',cancellation_ids=';'.join(z.known_cancel_id)))
cancel_ids={r['event_id'] for r in cancel_rows}
pd.DataFrame(cancel_rows,columns=['event_id','review','role','ric','reason','cancellation_ids']).to_csv(O/'CANCELLED_CONTROL_EXCLUSIONS.csv',index=False)
S=S[~S.event_id.isin(cancel_ids)].copy();D=D[D.event_id.isin(S.event_id)].copy()
CA=pd.read_csv(paths['ca'],parse_dates=['action_date']);G0=pd.read_csv(paths['old_event_gate']);prior={(x.review_cycle,x.RIC):float(x.factor) for x in G0.itertuples()}
S['factor01']=[prior.get((x.review,x.ric),float(CA.loc[CA.RIC.eq(x.ric)&CA.kind.eq('ordinary_split')&CA.action_date.gt(pd.Timestamp(x.q0))&CA.action_date.le(pd.Timestamp(x.q1)),'factor'].prod())) for x in S.itertuples()]
assert S.groupby('event_id').role.apply(set).map(lambda z:z=={'event','c1','c2','c3'}).all()
S.to_csv(O/'FROZEN_ROLES.csv',index=False)
F=pd.read_csv(paths['reports'],dtype={'Fond_institutnummer':str,'fund_isin':str}).rename(columns={'Fond_institutnummer':'fund_id','Kvartalsslut':'quarter'})
assert not F.duplicated(['fund_id','quarter']).any()
fm=F.set_index(['fund_id','quarter']); CA=pd.read_csv(paths['ca'],parse_dates=['action_date']); U=pd.read_csv(paths['roster'])
date_set=set(S.q0)|set(S.q1)|set(S.q2);isin_set=set(S.aliases.str.split(';').explode())
cols={'ISIN-kod_instrument':'isin','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','Antal':'qty','Marknadsvärde_instrument':'value','Valuta':'currency','Tillgångsslag_enligt_LVF_5_kap':'asset_type'}
parts=[]
for p in pd.read_csv(paths['holdings'],usecols=list(cols),chunksize=300000,dtype={'Fond_institutnummer':str}):
 p=p.rename(columns=cols);parts.append(p[p['isin'].isin(isin_set)&p.quarter.isin(date_set)])
H=pd.concat(parts,ignore_index=True)
for c in ['qty','value']:H[c]=pd.to_numeric(H[c],errors='coerce')
P=pd.read_parquet(paths['panel'],columns=['ric','date','close','mcap','shares','source']);P=P[P.ric.isin(S.ric)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
source_rows=[];invalid=[];cache=[]
for (review,ric),ss in S.groupby(['review','ric']):
 x=ss.iloc[0];alias=x.aliases.split(';');z=H[H['isin'].isin(alias)&H.quarter.isin([x.q0,x.q1,x.q2])]
 reasons=[];prices={};closes={};observed={}
 f12=float(CA.loc[CA.RIC.eq(ric)&CA.kind.eq('ordinary_split')&CA.action_date.gt(pd.Timestamp(x.q1))&CA.action_date.le(pd.Timestamp(x.q2)),'factor'].prod())
 diagnostics={}
 for lab,dt in [('q0',x.q0),('q1',x.q1),('q2',x.q2)]:
  zz=z[z.quarter.eq(dt)];ok=zz.asset_type.eq('ÖverlåtbartVärdepapper')&zz.currency.eq('SEK')&zz.qty.gt(0)&zz.value.gt(0)
  implied=zz.loc[ok,'value']/zz.loc[ok,'qty'];price=float(implied.median()) if len(implied) else np.nan
  agree=zz.loc[ok&(zz.value/zz.qty/price-1).abs().le(.01),'fund_id'].nunique();prices[lab]=price
  snap=P[P.ric.eq(ric)&P.date.le(pd.Timestamp(dt))&P.close.gt(0)].tail(1)
  close=float(snap.close.iloc[0]) if len(snap) else np.nan;age=int((pd.Timestamp(dt)-snap.date.iloc[0]).days) if len(snap) else None;closes[lab]=close
  if not(price>0 and agree>=3):reasons.append(lab+'_FI_price_consensus_missing')
  if not(close>0 and age is not None and age<=7):reasons.append(lab+'_adjusted_close_missing_stale')
  observed[lab]=set(zz.loc[ok,'isin']);diagnostics.update({lab+'_price_support_funds':int(agree),lab+'_close_age_days':age,lab+'_observed_isins':';'.join(sorted(observed[lab]))})
  rr=zz.value/zz.qty/price
  bad=(~zz.asset_type.eq('ÖverlåtbartVärdepapper'))|~np.isfinite(zz.qty)|zz.qty.lt(0)|(zz.qty.eq(0)&zz.value.notna()&zz.value.ne(0))|(zz.qty.gt(0)&~zz.value.gt(0))|(zz.currency.eq('SEK')&zz.qty.gt(0)&zz.value.gt(10000)&(rr-1).abs().gt(.10))
  for fid in zz.loc[bad,'fund_id'].unique():invalid.append(dict(review=review,ric=ric,fund_id=fid,quarter=dt,reason='signed_missing_zero_value_or_price_unit'))
 # Do not silently treat an unresolved changed security as a missing zero.
 if observed['q1']!=observed['q2']:reasons.append('q1_q2_observed_ISIN_set_changed')
 roster_month=str(pd.Timestamp(x.q2).year)+('10' if pd.Timestamp(x.q2).month==9 else '04')
 ur=U[U.month.astype(str).eq(roster_month)&U.company_code.eq(x.company_code)&U['isin'].isin(alias)]
 if len(ur)==0:reasons.append('q2_adjacent_dated_roster_no_exact_ISIN_company')
 ratio=(prices['q1']/prices['q2'])/(closes['q1']/closes['q2']) if min(prices.values())>0 and min(closes.values())>0 else np.nan
 if not(np.isfinite(ratio) and abs(ratio/f12-1)<=.03):reasons.append('q1_q2_units_need_dated_CA_resolution')
 cap=P[P.ric.eq(ric)&P.date.le(pd.Timestamp(x.q0))&P.mcap.gt(0)].tail(1)
 capvalid=len(cap)>0 and (pd.Timestamp(x.q0)-cap.date.iloc[0]).days<=7 and cap.source.iloc[0]=='tr'
 if not capvalid:reasons.append('q0_company_mcap_missing_stale_nonTR')
 mcap=float(cap.mcap.iloc[0]) if len(cap) else np.nan
 cf=float(cap.shares.iloc[0]*prices['q0']/mcap) if len(cap) else np.nan
 if not(np.isfinite(cf) and 0<cf<=1.03):reasons.append('q0_class_capital_fraction_unverified')
 source_rows.append(dict(review=review,ric=ric,q0=x.q0,q1=x.q1,q2=x.q2,factor01=x.factor01,factor12=f12,gate_pass=not reasons,reason=';'.join(reasons),**diagnostics))
 cache.append(dict(review=review,ric=ric,q0_price=prices['q0'],q0_mcap=mcap,factor01=x.factor01,factor12=f12,unit_ratio12=ratio,class_fraction_q0=cf))
SG=pd.DataFrame(source_rows);SG.to_csv(O/'SECURITY_SOURCE_GATE.csv',index=False)
pd.DataFrame(cache).to_csv(O/'private/SCALING_INPUTS.csv',index=False)
B=pd.DataFrame(invalid,columns=['review','ric','fund_id','quarter','reason']).drop_duplicates();B.to_csv(O/'INVALID_FUND_UNITS.csv',index=False)
EG=[];support=[];kept_funds=[];coverage=[]
for eid,ss in S.groupby('event_id'):
 x=ss.iloc[0];z=D[D.event_id.eq(eid)];original=set(z[z.role.eq('event')].fund_id)
 for role,zr in z.groupby('role'):assert set(zr.fund_id)==original
 good=set();badunit=set(B[B.review.eq(x.review)&B.ric.isin(ss.ric)].fund_id)
 for fid in sorted(original):
  fr=[];why=[]
  for dt in [x.q0,x.q1,x.q2]:
   if (fid,dt) not in fm.index:why.append('report_absent_'+dt);continue
   r=fm.loc[(fid,dt)];fr.append(r)
   if not(r.actual_instrument_rows>0):why.append('empty_report_'+dt)
   if pd.isna(r.fund_isin) or not str(r.fund_isin).strip():why.append('missing_fund_ISIN_'+dt)
  if len(fr)==3 and len({str(r.fund_isin) for r in fr})!=1:why.append('fund_ISIN_changed')
  if fid in badunit:why.append('unit_invalid_in_any_role')
  if not why:good.add(fid);kept_funds.append(dict(event_id=eid,review=x.review,fund_id=fid))
  support.append(dict(event_id=eid,review=x.review,fund_id=fid,eligible=not why,reason=';'.join(why)))
 gs=SG[SG.review.eq(x.review)&SG.ric.isin(ss.ric)];assert len(gs)==4
 passed=bool(gs.gate_pass.all() and len(good)>0)
 EG.append(dict(event_id=eid,review=x.review,gate_pass=passed,original_funds=len(original),retained_funds=len(good),reason=' | '.join(r.ric+':'+r.reason for r in gs[~gs.gate_pass].itertuples())))
 for role,zr in z.groupby('role'):
  n=zr[zr.component.eq('new')];den=float(n.pp.sum());num=float(n[n.fund_id.isin(good)].pp.sum()) if passed else 0.
  coverage.append(dict(event_id=eid,review=x.review,role=role,source_pass=passed,baseline_known_new_pp=den,retained_known_new_pp=num,retained_fraction=num/den if den>0 else np.nan))
EG=pd.DataFrame(EG);EG.to_csv(O/'EVENT_SOURCE_GATE.csv',index=False)
pd.DataFrame(support).to_csv(O/'FUND_REPORT_SUPPORT.csv.gz',index=False,compression='gzip')
pd.DataFrame(kept_funds).to_csv(O/'ELIGIBLE_FUNDS.csv',index=False)
CV=pd.DataFrame(coverage);CV.to_csv(O/'BASELINE_KNOWN_CAPITAL_COVERAGE.csv',index=False)
# Metadata-only subsequent OMXSB event flags, not outcome-based exclusions.
EV=pd.read_csv(paths['events'],usecols=['event_id','RIC','effective_date','type']);EV['effective_date']=pd.to_datetime(EV.effective_date)
haz=[]
for x in S.itertuples():
 for a in EV[EV.RIC.eq(x.ric)&EV.effective_date.gt(pd.Timestamp(x.q1))&EV.effective_date.le(pd.Timestamp(x.q2))].itertuples():haz.append(dict(event_id=x.event_id,role=x.role,ric=x.ric,subsequent_event_id=a.event_id,subsequent_type=a.type,subsequent_ED=a.effective_date.strftime('%Y-%m-%d')))
pd.DataFrame(haz,columns=['event_id','role','ric','subsequent_event_id','subsequent_type','subsequent_ED']).to_csv(O/'SUBSEQUENT_OMXSB_FLAGS.csv',index=False)
passed=set(EG.loc[EG.gate_pass,'event_id'])
# Keep only position data for possible later execution; this script never subtracts q2−q1.
H.to_csv(O/'private/RAW_RELEVANT_POSITIONS.csv.gz',index=False,compression='gzip')
out={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_outcomes_computed':False,'original_additions':70,'known_cancelled_control_event_exclusions':sorted(cancel_ids),'remaining_before_units':len(EG),'passed_events':len(passed),'passed_reviews':int(EG[EG.gate_pass].review.nunique()),'by_review':EG.groupby('review').gate_pass.agg(['sum','size']).to_dict('index'),'security_pairs':len(SG),'security_passes':int(SG.gate_pass.sum()),'subsequent_OMXSB_role_flags':len(haz),'unit_failures':SG.loc[~SG.gate_pass,['review','ric','reason']].to_dict('records'),'capital_coverage_basis':'Already known q1-valued new-position contribution, for support only, not new retention. Final outcomes use q0 valuation.'}
for role in ['event','c1','c2','c3']:
 c=CV[CV.role.eq(role)];v=c.groupby('review')[['baseline_known_new_pp','retained_known_new_pp']].mean().mean();out['retained_known_capital_'+role]=float(v.retained_known_new_pp/v.baseline_known_new_pp)
(O/'GATE_RESULT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(O/'GATE_OUTPUT_HASHES.json').write_text(json.dumps({p.name:sha(p) for p in O.glob('*') if p.is_file() and p.name not in ['GATE_OUTPUT_HASHES.json']},indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
