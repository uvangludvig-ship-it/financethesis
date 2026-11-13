from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,re
O=Path(__file__).resolve().parent;W=O.parent;R=Path('/Users/ludviguvang/dev/financethesis');L=R/'data/raw/lseg/panel_2005_2026'
F=json.load(open(O/'core_freeze_hashes.json'))
for p,h in F.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
C=pd.read_csv(O/'core_frozen.csv',parse_dates=['index_q','next_q']);B=pd.read_csv(O/'baseline_coverage.csv');dates=set(C.index_q)|set(C.next_q);isins=set(C["isin"])
T=pd.read_csv(W/'open_questions_20261101/retention/raw_tracker_transferable_securities.csv.gz',parse_dates=['Kvartalsslut'])
M=pd.read_csv(W/'claude_audit_20261101/holdings/corrected/latest_metadata_classification.csv',parse_dates=['quarter']).set_index(['fund_id','quarter'])
cols=['Tillgångsslag_enligt_LVF_5_kap','Instrumentnamn','ISIN-kod_instrument','Valuta','Antal','Marknadsvärde_instrument','Kvartalsslut','Fond_institutnummer','Fond_ISIN-kod']
parts=[]
for x in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=cols,chunksize=300000):
 x=x[x['ISIN-kod_instrument'].isin(isins)&x['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')].copy();x['Kvartalsslut']=pd.to_datetime(x.Kvartalsslut);parts.append(x[x.Kvartalsslut.isin(dates)])
H=pd.concat(parts,ignore_index=True);H.to_csv(O/'core_FI_evidence.csv.gz',index=False,compression='gzip')
P=pd.read_parquet(L/'stocks_daily_2005.parquet',columns=['ric','date','close','source']);P=P[P.ric.isin(C.ric)].copy();P['date']=pd.to_datetime(P.date);P=P.sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
ix=pd.read_csv(L/'indices_daily (1).csv',usecols=['ric','date','close']);cal=pd.DatetimeIndex(pd.to_datetime(ix.loc[ix.ric.eq('.OMXSBGI')&ix.close.notna(),'date']).sort_values().unique())
CA=pd.read_csv(R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',parse_dates=['action_date'])
fundisin={60320:'SE0002756973',60293:'SE0002591016'};rows=[];eps=[]
def norm(s):return re.sub('[^A-Z0-9]','',str(s).upper())
for c in C.itertuples():
 reason=[];ep=[]
 actions=CA[CA.RIC.eq(c.ric)&CA.action_date.gt(c.index_q)&CA.action_date.le(c.next_q)]
 badact=actions[actions.factor.ne(1)|actions.kind.str.contains('split|conversion|redenom|redemption|inlösen|class',case=False,na=False)]
 if len(badact):reason.append('known_unit_or_class_action')
 for label,dt in [('start',c.index_q),('end',c.next_q)]:
  rr=[];meta=M.loc[(c.fund_id,dt)] if (c.fund_id,dt)in M.index else None
  if meta is None:rr.append('missing_report')
  elif meta.n_instr<=0 or meta.fund_isin!=fundisin[c.fund_id]:rr.append('invalid_or_different_fund_report')
  z=H[H.Kvartalsslut.eq(dt)&H['ISIN-kod_instrument'].eq(c.isin)&H.Valuta.eq('SEK')&H.Antal.gt(0)&H.Marknadsvärde_instrument.gt(0)]
  ip=(z.Marknadsvärde_instrument/z.Antal).median();agree=z.loc[((z.Marknadsvärde_instrument/z.Antal)/ip-1).abs().le(.01),'Fond_institutnummer'].nunique()
  if not ip>0 or agree<3:rr.append('security_unit_not_confirmed_by_3_funds')
  ss=T[T.Fond_institutnummer.eq(c.fund_id)&T.Kvartalsslut.eq(dt)&T['ISIN-kod_instrument'].eq(c.isin)]
  if ss.Antal.isna().any() or ss.Antal.lt(0).any() or (ss.Antal.gt(0)&~ss.Marknadsvärde_instrument.gt(0)).any():rr.append('invalid_quantity')
  names={norm(n) for n in str(c.FI_name).split(';')}
  alt=T[T.Fond_institutnummer.eq(c.fund_id)&T.Kvartalsslut.eq(dt)&~T['ISIN-kod_instrument'].eq(c.isin)&T.Instrumentnamn.map(norm).isin(names)]
  if len(alt):rr.append('same_full_name_other_ISIN_unresolved')
  q=ss.Antal.sum() if len(ss) else 0.
  if len(ss):
   implied=ss.Marknadsvärde_instrument/ss.Antal
   if (ss.Antal.gt(0)&ss.Marknadsvärde_instrument.gt(10000)&(implied/ip-1).abs().gt(.03)).any():rr.append('fund_unit_inconsistent_with_3_fund_price')
  pp=P[P.ric.eq(c.ric)&P.date.le(dt)&P.close.gt(0)].tail(1);last=cal[cal<=dt][-1]
  px=pp.close.iloc[0] if len(pp) else np.nan;pdte=pp.date.iloc[0] if len(pp) else pd.NaT
  if pdte!=last:rr.append('no_current_LSEG_price')
  factor=px/ip if ip>0 else np.nan
  ep.append(dict(label=label,date=dt,q=q,FI_price=ip,agreeing_funds=agree,panel_close=px,panel_date=pdte,price_factor=factor,own_rows=len(ss),endpoint_reason=';'.join(rr)))
  reason += [label+':'+r for r in rr]
  eps.append(dict(review=c.review,fund_id=c.fund_id,isin=c.isin,ric=c.ric,**ep[-1]))
 unit=ep[1]['price_factor']/ep[0]['price_factor']
 if not np.isfinite(unit) or abs(unit-1)>.03:reason.append('cross_source_unit_change_not_one')
 assert np.isclose(ep[0]['q'],c.q0)
 rows.append(dict(review=c.review,fund_id=c.fund_id,fund=c.fund,isin=c.isin,ric=c.ric,company_code=c.company_code,rank=c.rank,index_q=c.index_q,next_q=c.next_q,mv0=c.mv0,aum0=c.aum0,q0=c.q0,q1=ep[1]['q'],splitfactor=1.,unit_factor_diagnostic=unit,known_actions=';'.join(actions.kind.astype(str)),gate_pass=not reason,gate_reason=';'.join(reason)))
G=pd.DataFrame(rows);G.to_csv(O/'core_gate_frozen.csv',index=False);pd.DataFrame(eps).to_csv(O/'endpoint_evidence.csv',index=False)
s=[]
for (fid,rev),g in G.groupby(['fund_id','review']):
 b=B[B.fund_id.eq(fid)&B.review.eq(rev)].iloc[0];ok=g[g.gate_pass];cover=ok.mv0.sum()/g.mv0.sum();pas=bool(b.start_gate_pass and len(ok)>=15 and cover>=.8)
 s.append(dict(fund_id=fid,review=rev,fund=g.fund.iloc[0],selected_N=len(g),valid_N=len(ok),validated_core_start_value_share=cover,selected_start_AUM_share=b.selected_start_AUM_share,fund_review_gate_pass=pas))
S=pd.DataFrame(s);S.to_csv(O/'core_gate_summary.csv',index=False)
(O/'gate_freeze_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'ANALYSIS_DECISIONS.txt',O/'core_frozen.csv',O/'core_gate_frozen.csv',O/'core_gate_summary.csv',Path(__file__)]},indent=2))
print(S.to_string(index=False));print('EXCLUSIONS',G.loc[~G.gate_pass,'gate_reason'].value_counts().to_dict());print('NO CORE RATIOS OR RELATIVE OUTCOMES COMPUTED')
