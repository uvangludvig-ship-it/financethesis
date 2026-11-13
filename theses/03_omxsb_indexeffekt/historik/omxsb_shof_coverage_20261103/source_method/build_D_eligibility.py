"""D source eligibility only: no returns, flows, covariance or risk calculations."""
from pathlib import Path
import pandas as pd,numpy as np,zipfile,io,json,datetime,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');C=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke')
VP=R/'data/raw/shof/Valuations/pilot_20261103/FUNDS_VALUATIONS_1793724895212.zip'
TP=R/'data/raw/shof/Reinvestments/pilot_20261103/FUNDS_RIPS_1793724775329.zip'
PP=R/'data/raw/shof/Reinvestments/coverage_20261103/Prices/FUNDS_PRICES_1793726853862.zip'
DP=R/'data/raw/shof/Reinvestments/coverage_20261103/Dividends/FUNDS_DIVIDENDS_1793726872989.zip'
FP=R/'data/raw/lseg/panel_eu/fx_sek_daily.csv'
MP=C/'work/shof_pilot_20261103/audit/ACQUISITION_PILOT_CLASSES.csv'
inputs=[VP,TP,PP,DP,FP,MP,O/'SOURCE_RULE_D.txt',Path(__file__)]
lock=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Source eligibility only. Numeric capital/FX used solely for reconciliation. TRI/NAV only positivity/presence. No return division or flow arithmetic.',rule='SOURCE_RULE_D.txt',same_date=True,month_end_max_gap_calendar_days=4,fx_weekend_previous_day_max_gap=3,cap_ratio_bounds=[.99,1.01],repeated_fund_cap_relative_spread_max=.001,inputs={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
(O/'D_IMPLEMENTATION_LOCK.json').write_text(json.dumps(lock,indent=2))
def readzip(p,cols):
 with zipfile.ZipFile(p) as z:
  ns=[n for n in z.namelist() if n.endswith('.csv')];assert len(ns)==1
  d=pd.read_csv(io.BytesIO(z.read(ns[0])),sep=';',usecols=lambda x:x.lower() in cols,dtype=str)
 d.columns=d.columns.str.lower()
 if 'date' in d:d['date']=pd.to_datetime(d.date.str[:10]);d=d[d.date.between('2017-01-01','2023-12-31')]
 return d
M=pd.read_csv(MP,dtype=str);M['inc']=pd.to_datetime(M.inceptiondate);M['obs']=pd.to_datetime(M.obsoletedate)
assert not M.secid.duplicated().any(), 'Multiple performance streams must not duplicate share classes'
V=readzip(VP,{'performanceid','secid','date','classcurrencyiso','fundcurrencyiso','tnaclass','tnafund'})
T=readzip(TP,{'performanceid','date','returntype','unit_sek'});T=T[T.returntype.isin(['1','1.0'])]
P=readzip(PP,{'performanceid','date','pretaxnav','unsplit'})
D=readzip(DP,{'performanceid','secid','excludingdate','reinvestdate','currencyiso','pretaxdividend'})
for z in [V,T,P]:assert not z.duplicated(['performanceid','date']).any()
for c in ['tnaclass','tnafund']:V[c]=pd.to_numeric(V[c],errors='coerce')
T['present']=pd.to_numeric(T.unit_sek,errors='coerce').gt(0);P['present']=pd.to_numeric(P.pretaxnav,errors='coerce').gt(0)
tri=set(map(tuple,T.loc[T.present,['performanceid','date']].to_numpy()))
nav=set(map(tuple,P.loc[P.present,['performanceid','date']].to_numpy()))
for c in ['excludingdate','reinvestdate']:D[c]=pd.to_datetime(D[c].str[:10],errors='coerce')
D['amount_present']=pd.to_numeric(D.pretaxdividend,errors='coerce').gt(0)
fx=pd.read_csv(FP,usecols=['pair','date','rate']);fx=fx[fx.pair.eq('NOKSEK=')].copy();fx.date=pd.to_datetime(fx.date.str[:10]);assert not fx.date.duplicated().any()
fx=fx.set_index('date').rate.to_dict()
def nokrate(date):
 if date in fx and pd.notna(fx[date]) and fx[date]>0:return fx[date],date
 if date.weekday()>=5:
  for lag in range(1,4):
   x=date-pd.Timedelta(days=lag)
   if x in fx and pd.notna(fx[x]) and fx[x]>0:return fx[x],x
 return None,None
months=list(pd.period_range('2017-01','2023-12',freq='M'));endpoints={};erows=[]
for fid,classes in M.groupby('FI_fund_id'):
 pids=set(classes.performanceid);vv=V[V.performanceid.isin(pids)]
 for mode in ['RIPS','NAV_conditional']:
  for mo in months:
   end=mo.end_time.normalize();active=classes[classes.inc.le(end)&(classes.obs.isna()|classes.obs.ge(end))]
   needed=set(active.performanceid);candidates=sorted(vv.loc[vv.date.between(end-pd.Timedelta(days=4),end),'date'].unique(),reverse=True)
   candidates=[pd.Timestamp(d) for d in candidates]
   found=None;lastwhy='no_common_TNA_and_return_source_within4days'
   for date in candidates:
    if (active.inc>date).any():continue
    z=vv[vv.date.eq(date)&vv.performanceid.isin(needed)].copy()
    if set(z.performanceid)!=needed or not z.tnaclass.gt(0).all():continue
    if not z.fundcurrencyiso.isin(['SEK','NOK']).all() or not z.classcurrencyiso.isin(['SEK','NOK']).all():lastwhy='unsupported_currency';continue
    if any((pid,date) not in tri and not(mode=='NAV_conditional' and pid in ['0P00016KI8','0P0000MWNE'] and (pid,date) in nav) for pid in needed):continue
    # First actual source-intersection date is fixed before capital reconciliation.
    found=(date,z);break
   rr=dict(FI_fund_id=fid,mode=mode,month=str(mo),active_class_ids=';'.join(sorted(needed)),active_classes=len(needed),source_date=None,fx_date=None,uses_NOK=False,uses_NAV=False,pass_source=False,reason=lastwhy)
   if found:
    date,z=found;rr['source_date']=str(date.date());rr['uses_NOK']=bool(z.classcurrencyiso.eq('NOK').any());rr['uses_NAV']=any((pid,date) not in tri for pid in needed)
    amounts=z.tnaclass.copy();ok=True
    if rr['uses_NOK']:
     rate,fd=nokrate(date);ok=rate is not None;rr['fx_date']=str(fd.date()) if fd is not None else None
     if ok:amounts.loc[z.classcurrencyiso.eq('NOK')]*=rate
    # Use directly quoted SEK fund TNA if available, once. Compare copies in
    # that currency; foreign-currency presentations are not extra fund capital.
    f=z.loc[z.tnafund.gt(0)&z.fundcurrencyiso.eq('SEK'),'tnafund']
    if f.empty:
     fn=z.loc[z.tnafund.gt(0)&z.fundcurrencyiso.eq('NOK'),'tnafund']
     rate,fd=nokrate(date)
     if len(fn) and rate is not None:f=fn*rate;rr['fx_date']=str(fd.date())
    if not ok:rr['reason']='missing_same_day_or_weekend_FX'
    elif f.empty:rr['reason']='no_contemporaneous_fund_TNA'
    else:
     den=f.median();reconcile=.99<=amounts.sum()/den<=1.01;copies=(f.max()-f.min())/den<.001
     rr['capital_reconciliation_pass']=bool(reconcile);rr['fund_TNA_copy_consistency']=bool(copies)
     rr['pass_source']=bool(reconcile and copies);rr['reason']='pass' if rr['pass_source'] else ('capital_reconciliation' if not reconcile else 'fund_TNA_copy_inconsistent')
    endpoints[(fid,mode,str(mo))]=dict(row=rr,date=date,pids=needed)
   else:endpoints[(fid,mode,str(mo))]=dict(row=rr,date=None,pids=needed)
   erows.append(rr)
pd.DataFrame(erows).to_csv(O/'D_ENDPOINT_SOURCE_FLAGS.csv',index=False)
rows=[];checks=[]
for year in range(2019,2024):
 for half,month in [('H1',3),('H2',9)]:
  review=f'{year}{half}';last=pd.Period(f'{year}-{month:02d}',freq='M');window=list(pd.period_range(last-24,last,freq='M'))
  for fid,cl in M.groupby('FI_fund_id'):
   row=dict(review=review,FI_fund_id=fid,fundid=cl.fundid.iloc[0],first_endpoint_month=str(window[0]),last_endpoint_month=str(window[-1]),historical_class_universe_fully_certified=False)
   ent=cl[cl.inc.gt(window[0].end_time)&cl.inc.le(window[-1].end_time)]
   row['new_entry_class_ids']=';'.join(sorted(ent.performanceid));row['new_entry_current_master_only']=bool(len(ent) and fid!='51482');row['new_entry_issuer_verified']=bool(len(ent) and fid=='51482')
   for mode in ['RIPS','NAV_conditional']:
    es=[endpoints[(fid,mode,str(m))] for m in window];bad=[f'{m}:{e["row"]["reason"]}' for m,e in zip(window,es) if not e['row']['pass_source']]
    ok=not bad
    # Endpoint rows require own source for all active classes; no pre-inception endpoint is demanded.
    # This is sufficient for every positive-lag-capital interval; new class has a structural zero lag.
    use_nav=any(e['row']['uses_NAV'] for e in es);uses_fx=any(e['row']['uses_NOK'] for e in es)
    if ok and mode=='NAV_conditional':
     start=es[0]['date'];finish=es[-1]['date'];div=D[D.performanceid.isin(cl.performanceid)&D.excludingdate.between(start,finish,inclusive='right')]
     for d in div.itertuples():
      if not(d.currencyiso=='SEK' and d.amount_present and pd.notna(d.reinvestdate) and d.excludingdate==d.reinvestdate and (d.performanceid,d.excludingdate) in nav):
       bad.append('dividend_event_source_alignment');ok=False
    row[f'D_{mode}_source_supported']=bool(ok)
    row[f'D_{mode}_valid_endpoints']=sum(e['row']['pass_source'] for e in es)
    row[f'D_{mode}_requires_NAV_assumption']=bool(use_nav)
    row[f'D_{mode}_uses_FX']=bool(uses_fx)
    row[f'D_{mode}_failure_reasons']=';'.join(bad)
   row['D_provisional_current_master']=row['D_RIPS_source_supported'] and row['new_entry_current_master_only']
   row['D_dated_lineage_verified_entry_only']=row['D_RIPS_source_supported'] and row['new_entry_issuer_verified']
   rows.append(row)
S=pd.DataFrame(rows);S.to_csv(O/'D_FUND_REVIEW_SOURCE_ELIGIBILITY.csv',index=False)
summary=S.groupby('FI_fund_id')[['D_RIPS_source_supported','D_NAV_conditional_source_supported']].sum().astype(int)
(O/'D_SUMMARY.json').write_text(json.dumps(dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_windows_only=True,no_returns_flows_covariances=True,N_windows=len(S),counts=summary.to_dict('index'),fund_history_fully_certified=False,FX_quote_orientation='NOKSEK= is SEK per NOK; Nordea primary final terms PDF p11',conditional_NAV_not_delivered_TRI=True),indent=2))
print(summary.to_string());print(S[['review','FI_fund_id','D_RIPS_source_supported','D_NAV_conditional_source_supported','new_entry_class_ids']].to_string(index=False))
