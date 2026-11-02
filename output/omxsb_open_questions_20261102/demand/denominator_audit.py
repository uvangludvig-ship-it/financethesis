from pathlib import Path
import os
import pandas as pd, numpy as np,json
ROOT=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
OUT=Path(__file__).parent
O=ROOT/'output/omxsb_extension_20261031/ownership'
e=pd.read_csv(O/'ownership_observations.csv',parse_dates=['before','after']);e=e[e.main_common_sample].copy()
alias=json.load(open(O/'validated_isin_aliases.json'))
h=pd.read_csv(O/'fi_halfyear_instrument_rows.csv.gz',parse_dates=['Kvartalsslut'])
p=pd.read_parquet(ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','close','mcap','shares','source']);p=p[p.ric.isin(e.RIC)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
rows=[]
for x in e.itertuples():
 z=p[p.ric.eq(x.RIC)&p.date.le(x.after)&p.mcap.gt(0)].tail(1)
 q=h[h.Kvartalsslut.eq(x.after)&h['ISIN-kod_instrument'].isin(alias[x.RIC])&h.Valuta.eq('SEK')&h.Antal.gt(0)&h.Marknadsvärde_instrument.gt(0)].copy()
 v=(q.Marknadsvärde_instrument/q.Antal).dropna();median=v.median()
 # At least three independent fund reports agree within 1% around the median.
 agree=q.loc[(v/median-1).abs().le(.01),'Fond_institutnummer'].nunique()
 row=dict(event_id=x.event_id,RIC=x.RIC,type=x.type,review_cycle=x.review_cycle,after=x.after,fi_price=median,price_agreeing_funds=agree,price_funds=q.Fond_institutnummer.nunique(),price_q10=v.quantile(.1),price_q90=v.quantile(.9),class_shares_after=x.denominator)
 if len(z):
  z=z.iloc[0];row.update(mcap=z.mcap,mcap_date=z.date,mcap_age_days=(x.after-z.date).days,close=z.close,raw_shares=z.shares,source=z.source,class_value_fraction=x.denominator*median/z.mcap)
 reasons=[]
 if not len(z):reasons.append('missing_company_mcap')
 elif row['mcap_age_days']>7:reasons.append('stale_company_mcap')
 if not median>0 or agree<3:reasons.append('unverified_contemporaneous_SEK_price')
 if len(z) and np.isfinite(row.get('class_value_fraction',np.nan)) and row['class_value_fraction']>1.03:reasons.append('class_value_exceeds_company_cap_3pct')
 row['new_unit_exclusion']=';'.join(reasons);rows.append(row)
d=pd.DataFrame(rows);d.to_csv(OUT/'denominator_audit.csv',index=False)
print('N',len(d),'MCAPmissing',d.mcap.isna().sum(),'new_unit_exclusions',d.new_unit_exclusion.value_counts().to_dict())
print('fraction distribution',d.class_value_fraction.describe().to_string())
print(d[d.new_unit_exclusion.ne('')|d.class_value_fraction.lt(.20)][['event_id','RIC','fi_price','mcap','class_shares_after','class_value_fraction','new_unit_exclusion']].to_string(index=False))
print('A/B examples\n',d[d.RIC.str.contains('SSAB|VOLV|INDU|NCC|KINV|BETS|KLOV|CORE')][['event_id','RIC','fi_price','mcap','class_shares_after','class_value_fraction','new_unit_exclusion']].to_string(index=False))
