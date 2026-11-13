"""The single declared three-date exposure profile, after the frozen gate."""
from pathlib import Path
from decimal import Decimal,ROUND_FLOOR
import json,hashlib,datetime
import pandas as pd,numpy as np
O=Path(__file__).resolve().parent
lock=json.loads((O/'COHORT_LOCK.json').read_text())
for k,v in lock['files'].items():assert hashlib.sha256(Path(k).read_bytes()).hexdigest()==v,k
g=pd.read_csv(O/'cohort_gate.csv',keep_default_na=False);g=g[g.valid]
d=pd.read_csv(O/'complete_positions_20261102.csv.gz',keep_default_na=False)
assert len(g)==47 and g.event_id.nunique()==28
def interval(raw):
 if '<' in raw or Decimal(raw.replace(',','.'))<Decimal('.5'):return 0,5,'below_0.5_censored'
 lo=int((Decimal(raw.replace(',','.'))*10).to_integral_value(rounding=ROUND_FLOOR))
 return lo,lo+1,'threshold_bin'
rows=[]
for z in g.itertuples():
 p=d[d.holder_key.eq(z.holder_key)&d['isin'].isin(z.accepted_followup_isins.split(';'))&d.position_date.ge('2012-11-01')]
 rr=dict(event_id=z.event_id,review=z.review,company_code=z.company_code,RIC=z.RIC,holder=z.holder,holder_key=z.holder_key,
         terminal_verification_method=z.terminal_verification_method)
 for label,target in [('base',z.baseline),('end',z.end),('post',z.post)]:
  s=p[p.position_date.le(target)];lastdate=s.position_date.max();last=s[s.position_date.eq(lastdate)]
  assert last.position_raw.nunique()==1 and last.comment.eq('').all()
  raw=last.position_raw.iloc[0];lo,hi,status=interval(raw)
  rr.update({label+'_date':target,label+'_report_date':lastdate,label+'_source_rows':';'.join(last.source_row),
             label+'_position_raw':raw,label+'_L10':lo,label+'_U10':hi,label+'_status':status,
             label+'_report_age_calendar_days':(pd.Timestamp(target)-pd.Timestamp(lastdate)).days})
 assert rr['base_L10']>=5
 rows.append(rr)
H=pd.DataFrame(rows)
def contrasts(x):
 x=x.copy()
 x['build_lower_pp']=(x.end_L10-x.base_U10)/10
 x['build_upper_pp']=(x.end_U10-x.base_L10)/10
 x['after_change_lower_pp']=(x.post_L10-x.end_U10)/10
 x['after_change_upper_pp']=(x.post_U10-x.end_L10)/10
 x['hump_lower_pp']=(x.end_L10-x[['base_U10','post_U10']].max(axis=1))/10
 x['hump_upper_pp']=(x.end_U10-x[['base_L10','post_L10']].max(axis=1))/10
 x['hump_status']=np.select([x.hump_lower_pp.gt(0),x.hump_upper_pp.le(0)],['certain_positive','strict_positive_impossible'],default='undetermined')
 for t in ['base','end','post']:
  x[t+'_lower_pp']=x[t+'_L10']/10;x[t+'_upper_pp']=x[t+'_U10']/10
 return x
H=contrasts(H);H.to_csv(O/'holder_position_intervals.csv',index=False)
keys=['event_id','review','company_code','RIC'];ivals=[t+'_'+b+'10' for t in ['base','end','post'] for b in ['L','U']]
I=H.groupby(keys)[ivals].sum().reset_index();I['cohort_holders']=I.event_id.map(H.groupby('event_id').size());I=contrasts(I)
I.to_csv(O/'issuer_position_intervals.csv',index=False)
metrics=[c for c in I if c.endswith('_pp')]
V=I.groupby('review')[metrics].mean();V['N_issuer_events']=I.groupby('review').size();V.to_csv(O/'review_position_intervals.csv')
summary=dict(run_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),cohort_frozen_at_utc=lock['frozen_at_utc'],
             pair_count=len(H),issuer_event_count=len(I),reviews=int(I.review.nunique()),companies=int(I.company_code.nunique()),
             issuer_hump_status=I.hump_status.value_counts().to_dict(),holder_hump_status=H.hump_status.value_counts().to_dict(),
             equal_review_mean_identification_bounds={k:float(V[k].mean())for k in metrics},
             equal_event_mean_identification_bounds={k:float(I[k].mean())for k in metrics},
             baseline_report_age_days=H.base_report_age_calendar_days.describe().to_dict(),
             end_censored_pairs=int(H.end_status.eq('below_0.5_censored').sum()),
             post_censored_pairs=int(H.post_status.eq('below_0.5_censored').sum()),
             terminal_method_counts=H.terminal_verification_method.value_counts().to_dict(),
             no_confidence_interval_or_pvalue=True,no_return_data_loaded=True,
             intervals_are_closed_conservative_outer_bounds=True,
             source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [O/'COHORT_LOCK.json',Path(__file__),O/'complete_positions_20261102.csv.gz']})
(O/'RESULTS.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary,indent=2,ensure_ascii=False))
print(I[['event_id','company_code','cohort_holders','build_lower_pp','build_upper_pp','after_change_lower_pp','after_change_upper_pp','hump_lower_pp','hump_upper_pp','hump_status']].to_string(index=False))
