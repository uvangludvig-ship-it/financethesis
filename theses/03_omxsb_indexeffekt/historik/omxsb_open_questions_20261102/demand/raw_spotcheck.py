from pathlib import Path
import os
import pandas as pd,json,numpy as np
R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]));O=R/'output/omxsb_extension_20261031/ownership';D=Path(__file__).parent
obs=pd.read_csv(O/'ownership_observations.csv');obs=obs[obs.main_common_sample]
# Chosen for chronology, an ordinary split and a dual class; not based on outcome sizes.
rics=['BILIa.ST','KLOVb.ST^G21','ANODb.ST','SSABa.ST']
chosen=obs[obs.RIC.isin(rics)].sort_values(['RIC','before']).groupby('RIC').head(1)
alias=json.load(open(O/'validated_isin_aliases.json'));isin=set().union(*(set(alias[r]) for r in chosen.RIC));funds={60320,60293,51542,51434}
ledger=pd.read_csv(O/'fi_fund_event_observations.csv.gz');rows=[];reports=[]
for chunk in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',chunksize=300000):
 c=chunk[chunk.Fond_institutnummer.isin(funds)]
 reports.append(c[['Fond_institutnummer','Kvartalsslut']].value_counts().rename('raw_report_rows').reset_index())
 z=c[c['ISIN-kod_instrument'].isin(isin)].copy();rows.append(z)
h=pd.concat(rows);rep=pd.concat(reports).groupby(['Fond_institutnummer','Kvartalsslut']).raw_report_rows.sum().to_dict()
h.to_csv(D/'raw_spotcheck_security_rows.csv',index=False)
out=[]
for e in chosen.itertuples():
 for fund in funds:
  ll=ledger[ledger.event_id.eq(e.event_id)&ledger.window.eq('event')&ledger.fund_id.eq(fund)]
  if len(ll) and ll.unit_invalid.iloc[0]:continue
  for side,date in [('before',e.before),('after',e.after)]:
   x=h[h.Fond_institutnummer.eq(fund)&h.Kvartalsslut.eq(date)&h['ISIN-kod_instrument'].isin(alias[e.RIC])&h['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')]
   n=rep.get((fund,date),0)
   if not n:continue
   q=x.Antal.sum();expected=ll['quantity_'+side+'_raw'].iloc[0] if len(ll) else 0
   assert np.isclose(q,expected)
   out.append(dict(event_id=e.event_id,RIC=e.RIC,side=side,date=date,fund_id=fund,raw_report_rows=n,raw_matching_rows=len(x),raw_quantity=q,ledger_quantity=expected,zero_supported_by_report_absence=(len(x)==0),passed=True))
pd.DataFrame(out).to_csv(D/'raw_spotcheck_reconciliation.csv',index=False)
print('Raw spot checks passed:',len(out),'source-missing quantity rows inside present report:',sum(x['zero_supported_by_report_absence'] for x in out))
