from pathlib import Path
import os
import pandas as pd,numpy as np,json,unicodedata,re
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]));D=Path(__file__).parent;O=R/'output/omxsb_extension_20261031/ownership';P=D.parent/'demand'
e=pd.read_csv(O/'ownership_observations.csv');valid_ids=set(pd.read_csv(P/'event_group_decomposition.csv').event_id);e=e[e.main_common_sample&e.event_id.isin(valid_ids)].copy();assert len(e)==216
e['halfyear_before']=e.before;e['before']=pd.to_datetime(e.after).map(lambda d:pd.Timestamp(d.year,3,31) if d.month==6 else pd.Timestamp(d.year,9,30));e['after']=pd.to_datetime(e.after)
ca=pd.read_csv(O/'corporate_action_sources.csv',parse_dates=['action_date']);e['halfyear_factor']=e.factor
e['factor']=[ca.loc[ca.RIC.eq(x.RIC)&ca.kind.eq('ordinary_split')&ca.action_date.gt(x.before)&ca.action_date.le(x.after),'factor'].prod() for x in e.itertuples()]
e[['event_id','RIC','review_cycle','type','before','after','factor','halfyear_factor','halfyear_before']].to_csv(D/'events_locked.csv',index=False)
alias=json.load(open(O/'validated_isin_aliases.json'));targets=set(e.RIC);all_isins=set().union(*(set(alias[r]) for r in targets));dates=set(e.before)|set(e.after)
cols=['Tillgångsslag_enligt_LVF_5_kap','Instrumentnamn','ISIN-kod_instrument','Valuta','Antal','Kurs_som_använts_vid_värdering_av_instrumentet','Marknadsvärde_instrument','Kvartalsslut','Fond_institutnummer','Fond_namn','Fondbolag_namn','Fond_ISIN-kod','Jämförelseindex']
parts=[];meta=[];allstock=[]
for c in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=cols,chunksize=300000):
 c['Kvartalsslut']=pd.to_datetime(c.Kvartalsslut);c=c[c.Kvartalsslut.isin(dates)].copy()
 c['has_actual_instrument']=c['ISIN-kod_instrument'].notna()&c['Instrumentnamn'].notna()&c['Tillgångsslag_enligt_LVF_5_kap'].notna()
 m=c.groupby(['Fond_institutnummer','Kvartalsslut'],dropna=False).agg(raw_rows=('has_actual_instrument','size'),actual_instrument_rows=('has_actual_instrument','sum'),name=('Fond_namn','first'),fund_isin=('Fond_ISIN-kod','first'),benchmark=('Jämförelseindex','first'))
 meta.append(m.reset_index());s=c[c['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')];allstock.append(s)
 parts.append(s[s['ISIN-kod_instrument'].isin(all_isins)])
m=pd.concat(meta).groupby(['Fond_institutnummer','Kvartalsslut'],as_index=False).agg(raw_rows=('raw_rows','sum'),actual_instrument_rows=('actual_instrument_rows','sum'),name=('name','first'),fund_isin=('fund_isin','first'),benchmark=('benchmark','first'))
m.to_csv(D/'raw_fund_report_metadata.csv',index=False)
h=pd.concat(parts);h.to_csv(D/'quarter_raw_target_instruments.csv.gz',index=False,compression='gzip');allh=pd.concat(allstock)
# Unknown identifier screen: same normalized instrument label as already accepted ordinary target security.
def norm(s):
 s=unicodedata.normalize('NFKD',str(s).upper());s=''.join(c for c in s if not unicodedata.combining(c));return re.sub('[^A-Z0-9]','',s)
old=pd.read_csv(O/'fi_halfyear_instrument_rows.csv.gz')
name_to_ric={}
for ric in targets:
 for name in old.loc[old['ISIN-kod_instrument'].isin(alias[ric]),'Instrumentnamn'].dropna().unique():name_to_ric.setdefault(norm(name),set()).add(ric)
allh['name_norm']=allh.Instrumentnamn.map(norm);allh['ric_candidate']=allh.name_norm.map(lambda n:';'.join(sorted(name_to_ric.get(n,set()))))
unknown=allh[allh.ric_candidate.ne('')&~allh['ISIN-kod_instrument'].isin(all_isins)].copy();unknown.to_csv(D/'unknown_ISIN_same_name_candidates.csv.gz',index=False,compression='gzip')
# Price/unit checks before calculating any changes.
px=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','shares']);px=px[px.ric.isin(targets)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last');source_den=pd.read_csv(P/'denominator_audit.csv').set_index('event_id')
report_dates={d:set(g.loc[g.actual_instrument_rows.gt(0),'Fond_institutnummer']) for d,g in m.groupby('Kvartalsslut')};rm=m.set_index(['Fond_institutnummer','Kvartalsslut'])
checks=[];snap=[];badfund=[]
for x in e.itertuples():
 prices={};closes={};reasons=[]
 both=report_dates.get(x.before,set())&report_dates.get(x.after,set())
 for date in [x.before,x.after]:
  z=h[h.Kvartalsslut.eq(date)&h['ISIN-kod_instrument'].isin(alias[x.RIC])].copy()
  zz=z[z.Valuta.eq('SEK')&z.Antal.gt(0)&z.Marknadsvärde_instrument.gt(0)];v=zz.Marknadsvärde_instrument/zz.Antal;med=v.median();agree=zz.loc[(v/med-1).abs().le(.01),'Fond_institutnummer'].nunique();prices[date]=med
  p=px[px.ric.eq(x.RIC)&px.date.le(date)&px.close.notna()].tail(1);close=p.close.iloc[0] if len(p) else np.nan;age=(date-p.date.iloc[0]).days if len(p) else np.nan;closes[date]=close
  if not med>0 or agree<3:reasons.append('price_not_verified_'+str(date.date()))
  if not close>0 or age>7:reasons.append('close_missing_or_stale_'+str(date.date()))
  snap.append(dict(event_id=x.event_id,RIC=x.RIC,date=date,fi_price=med,agreeing_funds=agree,close=close,close_age_days=age,ordinary_isins=';'.join(sorted(set(z['ISIN-kod_instrument'])))))
  # An ambiguous target quantity invalidates this FUND pair at both endpoints.
  rr=z.Marknadsvärde_instrument/z.Antal/med
  bad=z.Antal.isna()|z.Antal.lt(0)|(z.Antal.eq(0)&z.Marknadsvärde_instrument.notna()&z.Marknadsvärde_instrument.ne(0))|(z.Antal.gt(0)&~z.Marknadsvärde_instrument.gt(0))|(z.Valuta.eq('SEK')&z.Antal.gt(0)&z.Marknadsvärde_instrument.gt(10000)&(rr-1).abs().gt(.10))
  for b in z[bad&z.Fond_institutnummer.isin(both)].itertuples():badfund.append(dict(event_id=x.event_id,RIC=x.RIC,date=date,fund_id=b.Fond_institutnummer,instrument_name=b.Instrumentnamn,quantity=b.Antal,value=b.Marknadsvärde_instrument,reason='signed_missing_zero_value_or_price_unit'))
 ratio=(prices[x.before]/prices[x.after])/(closes[x.before]/closes[x.after]);reldiff=ratio/x.factor-1
 if not np.isfinite(reldiff) or abs(reldiff)>.03:reasons.append('unresolved_unit_change_against_dated_factor')
 for fund in [60320,60293]:
  if fund not in both:reasons.append('missing_actual_report_'+str(fund))
 if 60320 in both and any(rm.loc[(60320,dt),'fund_isin']!='SE0002756973' for dt in [x.before,x.after]):reasons.append('Nordnet_identity_not_constant')
 checks.append(dict(event_id=x.event_id,RIC=x.RIC,type=x.type,review_cycle=x.review_cycle,before=x.before,after=x.after,dated_factor=x.factor,halfyear_factor=x.halfyear_factor,price_unit_ratio=ratio,ratio_vs_dated_factor=reldiff,balanced_nonempty_fund_reports=len(both),gate_reasons=';'.join(reasons)))
pd.DataFrame(snap).to_csv(D/'quarter_security_snapshots.csv',index=False);bf=pd.DataFrame(badfund);bf.to_csv(D/'ambiguous_fund_pairs.csv',index=False);c=pd.DataFrame(checks)
if len(bf):
 for i,r in c.iterrows():
  bad=set(bf.loc[bf.event_id.eq(r.event_id),'fund_id'])&{60320,60293}
  if bad:c.loc[i,'gate_reasons']+=';tracker_quantity_invalid_'+','.join(map(str,bad))
c.to_csv(D/'gate_event_checks.csv',index=False)
print('event gate',c.gate_reasons.value_counts().to_dict());print('unknown same-name ISIN',len(unknown),unknown['ISIN-kod_instrument'].nunique());print(unknown[['ric_candidate','Instrumentnamn','ISIN-kod_instrument']].drop_duplicates().head(50).to_string(index=False));print('ambiguous fund pairs',len(bf[['event_id','fund_id']].drop_duplicates()) if len(bf) else 0);print(c[c.gate_reasons.ne('')].to_string(index=False));print('factor changes\n',c[c.dated_factor.ne(c.halfyear_factor)].to_string(index=False))
