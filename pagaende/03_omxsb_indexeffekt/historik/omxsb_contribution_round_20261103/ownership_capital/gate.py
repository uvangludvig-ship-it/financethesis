from pathlib import Path
import os,json,hashlib,datetime
import numpy as np,pandas as pd
O=Path(__file__).resolve().parent
R=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis'))
OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership';DQ=R/'output/omxsb_open_questions_20261102/demand_quarter'
S=pd.read_csv(OWN/'security_role_gate.csv');C=pd.read_csv(OWN/'decomp_coverage.csv');S=S[S.event_id.isin(C.loc[C.kept,'event_id'])].copy()
E=pd.read_csv(DQ/'events_locked.csv');CANON=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand/denominator_audit.csv').set_index('event_id');S=S[S.event_id.isin(E.event_id)].copy();prior={(x.review_cycle,x.RIC):x for x in E.itertuples()}
CA=pd.read_csv(R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',parse_dates=['action_date'])
U=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv')
cols={'ISIN-kod_instrument':'isin','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','Antal':'qty','Marknadsvärde_instrument':'value','Valuta':'currency','Tillgångsslag_enligt_LVF_5_kap':'asset_type'}
ids=set(S.aliases.str.split(';').explode());dates=set(S.q0)|set(S.q1);parts=[]
for c in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=list(cols),chunksize=300000,dtype={'Fond_institutnummer':str}):
 c=c.rename(columns=cols);c=c[c['isin'].isin(ids)&c.quarter.isin(dates)]
 parts.append(c)
H=pd.concat(parts,ignore_index=True)
for c in ['qty','value']:H[c]=pd.to_numeric(H[c],errors='coerce')
P=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','mcap','shares','source']);P=P[P.ric.isin(S.ric)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
# Do not compute holdings changes in this file.
records=[];bad=[]
for (rev,ric),ss in S.groupby(['review','ric']):
 x=ss.iloc[0];aliases=set(x.aliases.split(';'));q0=pd.Timestamp(x.q0);q1=pd.Timestamp(x.q1)
 z=H[H['isin'].isin(aliases)&H.quarter.isin([x.q0,x.q1])].copy();prices={};closes={};snapshot={}
 reasons=[];changed=[]
 factor=float(CA.loc[CA.RIC.eq(ric)&CA.kind.eq('ordinary_split')&CA.action_date.gt(q0)&CA.action_date.le(q1),'factor'].prod())
 known_factor='dated_corporate_action_register' if factor!=1 else 'no_dated_split_in_register'
 if (rev,ric) in prior:factor=float(prior[(rev,ric)].factor);known_factor='inherited_validated_event_quarter_gate'
 for lab,dt in [('before',x.q0),('after',x.q1)]:
  zz=z[z.quarter.eq(dt)];ok=zz.asset_type.eq('ÖverlåtbartVärdepapper')&zz.currency.eq('SEK')&zz.qty.gt(0)&zz.value.gt(0)
  v=(zz.loc[ok,'value']/zz.loc[ok,'qty']);med=float(v.median()) if len(v) else np.nan
  agree=zz.loc[ok&(zz.value/zz.qty/med-1).abs().le(.01),'fund_id'].nunique();prices[lab]=med
  snap=P[P.ric.eq(ric)&P.date.le(pd.Timestamp(dt))&P.close.gt(0)].tail(1)
  close=float(snap.close.iloc[0]) if len(snap) else np.nan;age=int((pd.Timestamp(dt)-snap.date.iloc[0]).days) if len(snap) else np.nan;closes[lab]=close
  snapshot.update({lab+'_agreeing_funds':agree,lab+'_price_valid':bool(med>0 and agree>=3),lab+'_close_valid':bool(close>0 and age<=7),lab+'_observed_isins':';'.join(sorted(zz.loc[ok,'isin'].unique())),lab+'_close_age':age})
  if not(med>0 and agree>=3):reasons.append('unverified_'+lab+'_raw_SEK_price')
  if not(close>0 and age<=7):reasons.append('missing_or_stale_'+lab+'_adjusted_price')
  # Per-fund units/values exclude all event roles symmetrically later.
  rr=zz.value/zz.qty/med
  invalid=(~zz.asset_type.eq('ÖverlåtbartVärdepapper'))|~np.isfinite(zz.qty)|zz.qty.lt(0)|(zz.qty.eq(0)&zz.value.notna()&zz.value.ne(0))|(zz.qty.gt(0)&~zz.value.gt(0))|(zz.currency.eq('SEK')&zz.qty.gt(0)&zz.value.gt(10000)&(rr-1).abs().gt(.10))
  for f in zz.loc[invalid,'fund_id'].unique():bad.append(dict(review=rev,ric=ric,fund_id=f,side=lab,reason='signed_missing_zero_value_or_price_unit'))
 cap=P[P.ric.eq(ric)&P.date.le(q1)&P.mcap.gt(0)].tail(1)
 capvalid=len(cap)>0 and (q1-cap.date.iloc[0]).days<=7 and cap.source.iloc[0]=='tr'
 if not capvalid:reasons.append('missing_stale_or_nonTR_company_mcap')
 # Same historical shares/mcap fields as earlier quantity work. Ratio only diagnoses impossible class capital.
 cf=float(cap.shares.iloc[0]*prices['after']/cap.mcap.iloc[0]) if len(cap) else np.nan
 if (rev,ric) in prior:
  cc=CANON.loc[prior[(rev,ric)].event_id];assert np.isclose(prices['after'],cc.fi_price,rtol=1e-10);assert np.isclose(float(cap.mcap.iloc[0]),cc.mcap,rtol=1e-10);cf=float(cc.class_value_fraction)
 if not(np.isfinite(cf) and 0<cf<=1.03):reasons.append('class_value_vs_company_mcap_unverified')
 ratio=(prices['before']/prices['after'])/(closes['before']/closes['after']) if min(prices.values())>0 and min(closes.values())>0 else np.nan
 unitvalid=np.isfinite(ratio) and abs(ratio/factor-1)<=.03
 if (rev,ric) in prior:unitvalid=True # already resolved primary CA/quarter gate, not a price-derived factor
 if not unitvalid:reasons.append('quarter_unit_change_requires_dated_CA_resolution')
 # An identifier switch not covered by a validated event gate or dated physical split also blocks fresh controls.
 isin_changed=snapshot['before_observed_isins']!=snapshot['after_observed_isins']
 if isin_changed and (rev,ric) not in prior and factor==1:reasons.append('changing_ISIN_requires_dated_identity_CA_resolution')
 records.append(dict(review=rev,ric=ric,q0=x.q0,q1=x.q1,roles=';'.join(sorted(set(ss.role))),event_role_count=len(ss),inherited_event_validation=(rev,ric) in prior,factor=factor,factor_basis=known_factor,quarter_unit_ratio=ratio,unit_ratio_vs_factor=ratio/factor-1,class_value_fraction=cf,mcap_source=cap.source.iloc[0] if len(cap) else '',mcap_age=int((q1-cap.date.iloc[0]).days) if len(cap) else np.nan,gate_pass=not reasons,gate_reasons=';'.join(reasons),**snapshot))
G=pd.DataFrame(records);G.to_csv(O/'security_feasibility_gate.csv',index=False)
B=pd.DataFrame(bad).drop_duplicates();B.to_csv(O/'invalid_fund_role_pairs.csv',index=False)
SG=S.merge(G[['review','ric','gate_pass','gate_reasons']],on=['review','ric'],validate='m:1');out=[]
for eid,ss in SG.groupby('event_id'):
 out.append(dict(event_id=eid,review=ss.review.iloc[0],type=ss.type.iloc[0],gate_pass=bool(ss.gate_pass.all()),reasons=' | '.join(x.role+':'+x.ric+':'+x.gate_reasons for x in ss.loc[~ss.gate_pass].itertuples())))
EG=pd.DataFrame(out);EG.to_csv(O/'event_feasibility_gate.csv',index=False)
meta=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),no_holdings_changes_calculated=True,source_ownership_events=len(EG),security_review_pairs=len(G),inherited_event_validations=int(G.inherited_event_validation.sum()),new_control_security_review_pairs=int((~G.inherited_event_validation).sum()),technical_security_gate_pass=int(G.gate_pass.sum()),allfour_technical_gate_pass=int(EG.gate_pass.sum()),by_type=EG.groupby('type').gate_pass.agg(['sum','size']).to_dict(),note='Technical feasibility only; final analyst review of control unit evidence and selection required before capital outcomes.')
(O/'FEASIBILITY_RUN.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2));print(G.loc[~G.gate_pass,['review','ric','roles','quarter_unit_ratio','factor','class_value_fraction','gate_reasons']].to_string(index=False))
inputs=[R/'data/derived/fi/fi_holdings_long.csv.gz',R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',OWN/'security_role_gate.csv',OWN/'decomp_coverage.csv',OWN/'decomp_fund_roles.csv.gz',OWN/'decomp_fund_groups.csv',DQ/'events_locked.csv',DQ/'raw_fund_report_metadata.csv',R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv']
(O/'input_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2))
