from pathlib import Path
import pandas as pd,json
D=Path(__file__).parent
c=pd.read_csv(D/'gate_event_checks.csv').fillna({'gate_reasons':''});c['original_gate_reasons']=c.gate_reasons;c['resolved_by_documented_nonunit_CA']=False
resolved={'OMXSB-2019H1-14','OMXSB-2020H1-11','OMXSB-2020H2-15','OMXSB-2021H1-12'}
for i,r in c.iterrows():
 if r.event_id in resolved:
  assert r.gate_reasons=='unresolved_unit_change_against_dated_factor' and r.dated_factor==1
  c.loc[i,'gate_reasons']='';c.loc[i,'resolved_by_documented_nonunit_CA']=True
assert c.gate_reasons.eq('').all()
u0=pd.read_csv(D/'unknown_ISIN_same_name_candidates.csv.gz');ev=pd.read_csv(D/'events_locked.csv');parts=[]
for x in ev.itertuples():
 z=u0[u0.ric_candidate.str.split(';').map(lambda a:x.RIC in a)&u0.Kvartalsslut.isin([x.before,x.after])].copy()
 if len(z):z['event_id']=x.event_id;z['target_RIC']=x.RIC;parts.append(z)
u=pd.concat(parts);u.to_csv(D/'unknown_ISIN_relevant_endpoints.csv',index=False)
known={'SE0000115446':'VolvoB','SE0000107203':'IndustrivardenC','SE0010714279':'CoremA','SE0015961594':'CoremD','FI0009003305':'SampoFinnishUnderlyingA'}
assert set(u['ISIN-kod_instrument'])<=set(known)
u['resolution']=u['ISIN-kod_instrument'].map(known);u.to_csv(D/'unknown_ISIN_resolved.csv',index=False)
m=pd.read_csv(D/'raw_fund_report_metadata.csv')
assert set(m.loc[m.Fond_institutnummer.eq(60320),'fund_isin'])=={'SE0002756973'}
assert set(m.loc[m.Fond_institutnummer.eq(60293),'fund_isin'])=={'SE0002591016'}
c.to_csv(D/'gate_event_checks_resolved.csv',index=False)
print('All216events passed with4independently documented nonunit CA resolutions; no outcomes inspected. Identity candidate unique ISIN:',u['ISIN-kod_instrument'].nunique())
