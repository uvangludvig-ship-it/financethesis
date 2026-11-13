from pathlib import Path
import os
import pandas as pd,numpy as np,json,re,unicodedata,hashlib
O=Path(__file__).resolve().parent;W=O.parent;R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]));OWN=R/'output/omxsb_extension_20261031/ownership'
ids=set(pd.read_csv(W/'demand/event_group_decomposition.csv').event_id)
e=pd.read_csv(OWN/'ownership_observations.csv');e=e[e.main_common_sample&e.event_id.isin(ids)].copy();assert len(e)==216 and e.event_id.nunique()==216
base=pd.read_csv(R/'output/omxsb_replication_2007/events_car.csv',parse_dates=['AD','ED']);e=e.merge(base[['event_id','AD','ED']],on='event_id',validate='one_to_one');e['index_q']=pd.to_datetime(e.after);e['next_q']=e.index_q+pd.offsets.QuarterEnd(1)
alias=json.load(open(OWN/'validated_isin_aliases.json'));target=set(e.RIC);all_isins=set().union(*(set(alias[r]) for r in target));dates=set(e.index_q)|set(e.next_q);trackers={60320:('Nordnet','SE0002756973'),60293:('Nordea','SE0002591016')}
fm=pd.read_csv(W.parent/'claude_audit_20261101/holdings/corrected/latest_metadata_classification.csv');fm['quarter']=pd.to_datetime(fm.quarter);fm=fm.set_index(['fund_id','quarter'])
cols=['Tillgångsslag_enligt_LVF_5_kap','Instrumentnamn','ISIN-kod_instrument','Valuta','Antal','Kurs_som_använts_vid_värdering_av_instrumentet','Marknadsvärde_instrument','Kvartalsslut','Fond_institutnummer','Fond_namn','Fond_ISIN-kod']
parts=[];track=[]
for c in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=cols,chunksize=300000):
 c['Kvartalsslut']=pd.to_datetime(c.Kvartalsslut);c=c[c.Kvartalsslut.isin(dates)]
 c=c[c['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')]
 parts.append(c[c['ISIN-kod_instrument'].isin(all_isins)])
 track.append(c[c.Fond_institutnummer.isin(trackers)])
H=pd.concat(parts,ignore_index=True);T=pd.concat(track,ignore_index=True)
H.to_csv(O/'raw_accepted_instruments.csv.gz',index=False,compression='gzip');T.to_csv(O/'raw_tracker_transferable_securities.csv.gz',index=False,compression='gzip')
def norm(s):
 s=unicodedata.normalize('NFKD',str(s).upper());s=''.join(c for c in s if not unicodedata.combining(c));return re.sub('[^A-Z0-9]','',s)
# Conservative same-name unknown-ISIN diagnostic; name match flags ambiguity, never approves a new alias.
names={}
old=pd.read_csv(W/'demand_quarter/quarter_raw_target_instruments.csv.gz')
for ric in target:
 for n in old.loc[old['ISIN-kod_instrument'].isin(alias[ric]),'Instrumentnamn'].dropna().unique():names.setdefault(norm(n),set()).add(ric)
T['candidate_RICs']=T.Instrumentnamn.map(lambda s:';'.join(sorted(names.get(norm(s),set()))))
unknown=T[(T.candidate_RICs!='')&~T['ISIN-kod_instrument'].isin(all_isins)].copy()
known_other={'SE0000115446':'VolvoB','SE0000107203':'IndustrivardenC','SE0010714279':'CoremA','SE0015961594':'CoremD','FI0009003305':'SampoFinnishUnderlyingA'}
unknown['known_other_class']=unknown['ISIN-kod_instrument'].map(known_other)
unknown.to_csv(O/'tracker_unknown_identifier_screen.csv',index=False)
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date']);cal=pd.DatetimeIndex(ix.loc[(ix.ric=='.OMXSBGI')&ix.close.notna(),'date'].sort_values().unique())
ca=pd.read_csv(OWN/'corporate_action_sources.csv',parse_dates=['action_date'])
rows=[];endpoints=[]
for ev in e.itertuples():
 q0,q1=ev.index_q,ev.next_q;iE=cal.get_indexer([ev.ED])[0];assert iE>=0
 td0=int(cal.searchsorted(q0,side='right')-1-iE);td1=int(cal.searchsorted(q1,side='right')-1-iE);ed100=cal[iE+100] if iE+100<len(cal)else pd.NaT
 for fid,(name,fundisin) in trackers.items():
  eps=[]
  for dt in [q0,q1]:
   reasons=[];meta=fm.loc[(fid,dt)] if (fid,dt)in fm.index else None
   if meta is None:reasons.append('missing_report')
   elif not meta.n_instr>0:reasons.append('empty_report')
   elif meta.fund_isin!=fundisin:reasons.append('fund_identity_unknown')
   # Any unresolved related-name identifier blocks an absence interpretation.
   u=unknown[unknown.Fond_institutnummer.eq(fid)&unknown.Kvartalsslut.eq(dt)&unknown.candidate_RICs.str.split(';').map(lambda rr:ev.RIC in rr)&unknown.known_other_class.isna()]
   if len(u):reasons.append('unresolved_related_ISIN')
   z=H[H.Kvartalsslut.eq(dt)&H['ISIN-kod_instrument'].isin(alias[ev.RIC])]
   s=z[z.Fond_institutnummer.eq(fid)]
   goodmarket=z[z.Antal.gt(0)&z.Marknadsvärde_instrument.gt(0)&z.Valuta.eq('SEK')]
   implied=goodmarket.Marknadsvärde_instrument/goodmarket.Antal;med=implied.median();agree=goodmarket.loc[(implied/med-1).abs().le(.01),'Fond_institutnummer'].nunique()
   if not med>0 or agree<3:reasons.append('security_alias_not_reconfirmed_by_3_funds')
   bad=s.Antal.isna()|s.Antal.lt(0)|(s.Antal.gt(0)&~s.Marknadsvärde_instrument.gt(0))|(s.Antal.eq(0)&s.Marknadsvärde_instrument.gt(0))
   rr=(s.Marknadsvärde_instrument/s.Antal)/med
   bad|=s.Valuta.eq('SEK')&s.Antal.gt(0)&s.Marknadsvärde_instrument.gt(10000)&(rr-1).abs().gt(.1)
   if bad.any():reasons.append('quantity_or_instrument_unit_ambiguous')
   state='unknown' if reasons else 'positive' if s.Antal.gt(0).any()else 'no_reported_position'
   eps.append(state)
   endpoints.append(dict(event_id=ev.event_id,RIC=ev.RIC,type=ev.type,fund_id=fid,fund=name,quarter=dt,status=state,reasons=';'.join(reasons),source_report=meta.source_file if meta is not None else '',report_n_instruments=meta.n_instr if meta is not None else np.nan,raw_quantity_unadjusted=s.Antal.sum(min_count=1),matched_position_rows=len(s),isin_observed=';'.join(sorted(set(s['ISIN-kod_instrument']))),FI_implied_price=med,price_agreeing_funds=agree))
  state=('unknown' if 'unknown'in eps else 'positive_both' if eps==['positive','positive']else 'positive_to_no_reported_position'if eps==['positive','no_reported_position']else 'no_position_to_positive'if eps==['no_reported_position','positive']else 'no_position_both')
  actions=ca[(ca.RIC==ev.RIC)&ca.action_date.gt(q0)&ca.action_date.le(q1)]
  rows.append(dict(event_id=ev.event_id,RIC=ev.RIC,type=ev.type,review=ev.review_cycle,fund_id=fid,fund=name,ED=ev.ED,index_q=q0,next_q=q1,index_q_trading_days_after_ED=td0,next_q_trading_days_after_ED=td1,ED100=ed100,next_q_before_ED100=bool(q1<ed100)if pd.notna(ed100)else None,index_status=eps[0],next_status=eps[1],retention_status=state,known_CA_in_interval=';'.join(actions.kind.astype(str)),quantity_change_estimated=False))
D=pd.DataFrame(rows);EP=pd.DataFrame(endpoints);D.to_csv(O/'retention_event_fund_status.csv',index=False);EP.to_csv(O/'retention_endpoint_audit.csv',index=False)
D.groupby(['type','fund','retention_status']).agg(N=('event_id','size'),reviews=('review','nunique')).reset_index().to_csv(O/'retention_summary.csv',index=False)
# Already-computed, identity-corrected 20->100 same-event price match. No new returns or regressions.
p=pd.read_csv(W/'persistence_corrected/event_paths.csv');p=p[(p.model=='market_adjusted')&p.common3].copy();p['late20_100_existing']=p.diff3_100-p.diff3_20
A=D[D.type=='addition'];M=A.merge(p[['event_id','diff3_20','diff3_100','late20_100_existing']],on='event_id',how='left',validate='many_to_one');M.to_csv(O/'retention_existing_price_join.csv',index=False)
# Use the fixed positive-both status only; descriptive paired price average is not a causal effect.
sumrows=[]
for f,g in M.groupby('fund'):
 for status,z in g.groupby('retention_status'):
  zz=z.dropna(subset=['late20_100_existing']);rev=zz.groupby('review').late20_100_existing.mean()
  sumrows.append(dict(fund=f,status=status,all_additions=len(z),price_matched_additions=len(zz),reviews=len(rev),late20_100_event_mean=zz.late20_100_existing.mean(),late20_100_review_mean=rev.mean(),post_q_min_days=z.next_q_trading_days_after_ED.min(),post_q_max_days=z.next_q_trading_days_after_ED.max()))
P=pd.DataFrame(sumrows);P.to_csv(O/'retention_existing_price_descriptive.csv',index=False)
summary=dict(events=len(e),additions=int(e.type.eq('addition').sum()),deletions=int(e.type.eq('deletion').sum()),fund_event_status_rows=len(D),unknown_endpoints=int(EP.status.eq('unknown').sum()),unknown_addition_endpoints=int(EP[EP.type.eq('addition')].status.eq('unknown').sum()),unresolved_unknown_ISIN_rows=int(unknown.known_other_class.isna().sum()),addition_nextq_min_trading_days=int(A.next_q_trading_days_after_ED.min()),addition_nextq_max_trading_days=int(A.next_q_trading_days_after_ED.max()),addition_nextq_before_ED100_fundevents=int(A.next_q_before_ED100.sum()))
(O/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(D.groupby(['type','fund','retention_status']).size().to_string());print(P.to_string(index=False));print('UNKNOWN ENDPOINTS',EP[EP.status=='unknown'][['event_id','RIC','fund','quarter','reasons']].to_string(index=False))
(O/'source_hashes.json').write_text(json.dumps({str(x):hashlib.sha256(x.read_bytes()).hexdigest()for x in [OWN/'validated_isin_aliases.json',OWN/'corporate_action_sources.csv',W/'demand/event_group_decomposition.csv',W/'persistence_corrected/event_paths.csv']},indent=2))
# Joint two-fund descriptive match and independent reconciliation at the known index endpoint.
both=D[(D.type=='addition')&D.retention_status.eq('positive_both')].groupby('event_id').fund.nunique();bothids=set(both[both==2].index)
J=M[M.event_id.isin(bothids)&M.late20_100_existing.notna()].drop_duplicates('event_id');J.to_csv(O/'both_trackers_retained_existing_price_match.csv',index=False)
y=D.merge(EP,left_on=['event_id','fund_id','index_q'],right_on=['event_id','fund_id','quarter'],validate='one_to_one');ei=e.set_index('event_id')
y['old_quantity']=[ei.loc[r.event_id,'FI_Nordnet_documented_after_raw'if r.fund_id==60320 else 'FI_Nordea_metadata_after_raw']for r in y.itertuples()];y['difference']=y.raw_quantity_unadjusted.fillna(0)-y.old_quantity
# fillna(0) here only reconciles valid no-position rows; every status was already validated before this step.
assert not y.difference.abs().gt(1e-6).any()
y[['event_id','fund_id','index_q','raw_quantity_unadjusted','old_quantity','difference']].to_csv(O/'index_quarter_old_ledger_reconciliation.csv',index=False)
(O/'joint_retention_summary.json').write_text(json.dumps(dict(both_trackers_retained_additions=len(bothids),price_matched_additions=len(J),reviews=J.review.nunique(),late20_100_event_mean=J.late20_100_existing.mean(),late20_100_review_mean=J.groupby('review').late20_100_existing.mean().mean(),index_quantity_reconciled_rows=len(y),index_quantity_mismatches=int(y.difference.abs().gt(1e-6).sum())),indent=2))
D[['event_id','review','ED','index_q','next_q','index_q_trading_days_after_ED','next_q_trading_days_after_ED','ED100','next_q_before_ED100']].drop_duplicates().to_csv(O/'timing.csv',index=False)
