from pathlib import Path
import pandas as pd,numpy as np,json,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');SRC=R/'output/omxsb_open_questions_20261102/retention';OWN=R/'output/omxsb_extension_20261031/ownership'
D=pd.read_csv(SRC/'retention_event_fund_status.csv',parse_dates=['index_q','next_q']);D=D[D.type.eq('addition')];E=D.drop_duplicates('event_id');assert len(E)==119
EP=pd.read_csv(SRC/'retention_endpoint_audit.csv',parse_dates=['quarter']);EP=EP[EP.type.eq('addition')];H=pd.read_csv(SRC/'raw_accepted_instruments.csv.gz',parse_dates=['Kvartalsslut']);T=pd.read_csv(SRC/'raw_tracker_transferable_securities.csv.gz',parse_dates=['Kvartalsslut']);AL=json.loads((OWN/'validated_isin_aliases.json').read_text());CA=pd.read_csv(OWN/'corporate_action_sources.csv',parse_dates=['action_date'])
P=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','shares','source']);P=P[P.ric.isin(E.RIC)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date']);cal=pd.DatetimeIndex(ix.loc[ix.ric.eq('.OMXSBGI')&ix.close.notna(),'date'].sort_values().unique());rows=[]
for ev in E.itertuples():
 row=dict(event_id=ev.event_id,RIC=ev.RIC,review=ev.review,index_q=str(ev.index_q.date()),next_q=str(ev.next_q.date()))
 for name,dt in [('index',ev.index_q),('next',ev.next_q)]:
  p=P[P.ric.eq(ev.RIC)&P.date.le(dt)&P.close.gt(0)].tail(1);lastday=cal[cal<=dt][-1];date=p.date.iloc[0]if len(p)else pd.NaT;close=p.close.iloc[0]if len(p)else np.nan
  h=H[H.Kvartalsslut.eq(dt)&H['ISIN-kod_instrument'].isin(AL[ev.RIC])&H.Valuta.eq('SEK')&H.Antal.gt(0)&H.Marknadsvärde_instrument.gt(0)]
  ip=(h.Marknadsvärde_instrument/h.Antal).median();agree=h.loc[((h.Marknadsvärde_instrument/h.Antal)/ip-1).abs().le(.01),'Fond_institutnummer'].nunique()
  row.update({name+'_close_date':date,name+'_last_market_day':lastday,name+'_current_price':date==lastday,name+'_close':close,name+'_FI_price':ip,name+'_agreed_funds':agree,name+'_price_factor':close/ip if ip>0 else np.nan,name+'_ISINs':';'.join(sorted(h['ISIN-kod_instrument'].unique()))})
  tt=T[T.Kvartalsslut.eq(dt)&T['ISIN-kod_instrument'].isin(AL[ev.RIC])];row[name+'_tracker_ISINs']=';'.join(sorted(tt['ISIN-kod_instrument'].unique()))
 row['unit_factor_diagnostic']=row['next_price_factor']/row['index_price_factor'];acts=CA[CA.RIC.eq(ev.RIC)&CA.action_date.gt(ev.index_q)&CA.action_date.le(ev.next_q)]
 row['known_action']=';'.join(acts.kind);row['known_factor']=acts.factor.prod()if len(acts)else 1.;row['same_FI_ISINs']=row['index_ISINs']==row['next_ISINs'];row['close_diagnostic_one']=abs(row['unit_factor_diagnostic']/row['known_factor']-1)<=.03
 rows.append(row)
G=pd.DataFrame(rows);G.to_csv(O/'unit_gate_initial.csv',index=False)
print('Flagged',G[(~G.index_current_price)|(~G.next_current_price)|(~G.same_FI_ISINs)|(~G.close_diagnostic_one)|G.known_action.ne('')].to_string(index=False));print('COVERAGE',len(G),'sameISIN',G.same_FI_ISINs.sum(),'pricecurrent',(G.index_current_price&G.next_current_price).sum(),'unitdiag',G.close_diagnostic_one.sum())
(O/'input_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [SRC/'retention_endpoint_audit.csv',SRC/'raw_tracker_transferable_securities.csv.gz',SRC/'raw_accepted_instruments.csv.gz',OWN/'validated_isin_aliases.json',O/'DECLARATION.txt']},indent=2))
