from pathlib import Path
import os
import pandas as pd,numpy as np,json
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]))
e=pd.read_csv(O/'retention_event_fund_status.csv',parse_dates=['index_q','next_q']);e=e[e.type=='addition'].drop_duplicates('event_id');assert len(e)==119
v=pd.read_csv(O.parent/'demand/denominator_audit.csv').set_index('event_id')
p=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','shares','close','source']);p=p[p.ric.isin(e.RIC)].sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
rows=[]
for x in e.itertuples():
 for endpoint,dt in [('index',x.index_q),('next',x.next_q)]:
  z=p[p.ric.eq(x.RIC)&p.date.le(dt)&p.shares.gt(0)].tail(1)
  sh=z.shares.iloc[0]if len(z)else np.nan;sd=z.date.iloc[0]if len(z)else pd.NaT;age=(dt-sd).days if pd.notna(sd)else np.nan
  old=v.loc[x.event_id,'class_shares_after']if endpoint=='index'else np.nan
  rows.append(dict(event_id=x.event_id,RIC=x.RIC,endpoint=endpoint,quarter=dt,shares_date=sd,age_days=age,raw_shares=sh,source=z.source.iloc[0]if len(z)else None,validated_index_class_shares=old,index_exact_match=bool(abs(sh-old)<1e-6)if endpoint=='index'else None,passes_date_gate=bool(age<=2)if pd.notna(age)else False))
d=pd.DataFrame(rows);d.to_csv(O/'share_data_gate.csv',index=False);s=dict(events=len(e),index_old_denominator_mismatches=int((d[d.endpoint=='index'].index_exact_match==False).sum()),date_gate_failures_by_endpoint=d[~d.passes_date_gate].groupby('endpoint').size().to_dict(),qnext_independent_class_denominator_available=False)
(O/'share_data_gate_summary.json').write_text(json.dumps(s,indent=2));print(json.dumps(s,indent=2));print(d[(~d.passes_date_gate)|d.index_exact_match.eq(False)].to_string(index=False))
