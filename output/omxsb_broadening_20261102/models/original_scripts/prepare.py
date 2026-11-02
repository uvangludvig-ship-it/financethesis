from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime
O=Path(__file__).resolve().parent;C=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis')
v=pd.read_csv(C/'work/volume_units_full_20261102/volume_input_all216.csv',parse_dates=['AD','ED','after']);e=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv',parse_dates=['before','after']);d=pd.read_csv(C/'work/mandate_upgrade_20261102/event_demand_updated.csv');d=d[d.definition.eq('updated_documented_continuity')][['event_id','net_company_pp','n_funds','expected_fund_pairs','excluded_fund_pairs']]
a=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',usecols=['event_id','precar','log_mcap','issuer'])
snap=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/quarter_security_snapshots.csv',parse_dates=['date']);p=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','totret','mcap']);p=p[p.ric.isin(v.RIC)];assert not p.duplicated(['ric','date']).any();S={k:g.set_index('date').sort_index()for k,g in p.groupby('ric')};ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv');cal=pd.DatetimeIndex(sorted(pd.to_datetime(ix.loc[ix.ric.eq('.OMXSBGI')&ix.close.notna(),'date']).unique()))
z=v.merge(e[['event_id','before','factor']],on='event_id',validate='1:1').merge(d,on='event_id',validate='1:1').merge(a,on='event_id',how='left',validate='1:1');rows=[]
for t in z.itertuples():
 r=t._asdict();reason=[]
 if not t.unit_gate_pass:reason.append('previous_unit_gate_unresolved')
 if pd.isna(t.issuer):reason.append('no_locked_historical_listing_match')
 pp=S[t.RIC];b=snap[(snap.event_id==t.event_id)&snap.date.eq(t.before)];assert len(b)==1;b=b.iloc[0];mb=pp.loc[:t.before,'mcap'].dropna();mc=mb.iloc[-1]if len(mb)else np.nan;age=(t.before-mb.index[-1]).days if len(mb)else np.nan
 if not np.isfinite(mc)or mc<=0 or age>5:reason.append('prequarter_company_cap_missing_or_stale')
 if not np.isfinite(b.fi_price)or b.fi_price<=0:reason.append('prequarter_class_price_missing')
 iad=int(cal.searchsorted(t.AD));ied=int(cal.searchsorted(t.ED));rr=pp.reindex(cal).totret.iloc[iad-61:iad-11]/100;rr=rr.where(rr.ge(-1)&rr.le(10));sig=rr.std(ddof=1)
 if rr.count()<40 or not np.isfinite(sig)or sig<=0:reason.append('pre_sigma_coverage')
 qa=t.net_company_pp/100*t.company_mcap_after/t.FI_price;dose=qa/t.baseline_volume_FI_after_units;ql=qa/t.factor*b.fi_price/mc*100;adv=t.baseline_volume_FI_after_units/t.factor*b.fi_price;qs=100*sig*np.sign(dose)*np.sqrt(abs(dose))
 r.update(prequarter_class_price=b.fi_price,prequarter_company_cap=mc,prequarter_company_cap_age_days=age,pre_sigma=sig,sigma_N=int(rr.count()),sigma_first=cal[iad-61],sigma_last=cal[iad-12],Q_after_units=qa,signed_Q_over_ADV=dose,linear_prevalued_company_pp=ql,sqrt_proxy_pp=qs,log_prevalued_ADV=np.log(adv)if adv>0 else np.nan,notice_trading_days=ied-iad,deletion=int(t.type=='deletion'))
 for c in ['precar','log_mcap','pre_sigma','linear_prevalued_company_pp','sqrt_proxy_pp','log_prevalued_ADV']:
  if not np.isfinite(r[c]):reason.append('missing_'+c)
 r['design_pass']=not reason;r['design_exclusions']=';'.join(reason);rows.append(r)
x=pd.DataFrame(rows);x.to_csv(O/'feature_gate_all216.csv',index=False);g=x[x.design_pass];g[['linear_prevalued_company_pp','sqrt_proxy_pp','precar','log_mcap','pre_sigma','log_prevalued_ADV','notice_trading_days']].corr().to_csv(O/'feature_correlations_NO_OUTCOME.csv');g[['linear_prevalued_company_pp','sqrt_proxy_pp','signed_Q_over_ADV','pre_sigma']].describe().to_csv(O/'feature_support_NO_OUTCOME.csv')
lock=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),N_input=216,N_gate=int(x.design_pass.sum()),G=int(g.review_cycle.nunique()),by_direction=g.type.value_counts().to_dict(),new_price_outcomes_loaded=False,files={str(f):hashlib.sha256(f.read_bytes()).hexdigest()for f in [O/'DECISIONS.txt',O/'feature_gate_all216.csv',Path(__file__)]})
(O/'DESIGN_LOCK.json').write_text(json.dumps(lock,indent=2));print(json.dumps(lock,indent=2));print(g[['linear_prevalued_company_pp','sqrt_proxy_pp','signed_Q_over_ADV','pre_sigma']].describe().to_string());print(g[['linear_prevalued_company_pp','sqrt_proxy_pp']].corr())
