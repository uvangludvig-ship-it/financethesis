from pathlib import Path
import pandas as pd,numpy as np,json
O=Path(__file__).resolve().parent;C=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis')
d=pd.read_csv(O/'analysis_event_ledger.csv')
a=json.loads((R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json').read_text())
r=pd.read_csv(C/'work/open_questions_20261101/demand_quarter/quarter_raw_target_instruments.csv.gz')
r=r[r.Fond_institutnummer.eq(60320)].copy();r['Antal']=pd.to_numeric(r.Antal,errors='coerce')
checks=[]
for x in d.itertuples():
 for side in ['before','after']:
  g=r[r.Kvartalsslut.eq(getattr(x,side))&r['ISIN-kod_instrument'].isin(a[x.RIC])]
  assert g.Antal.notna().all() and g.Antal.ge(0).all()
  rawq=g.Antal.sum()
  q=getattr(x,side+'_quantity')
  assert np.isclose(q,rawq),(x.event_id,side,q,rawq)
  checks.append(dict(event_id=x.event_id,RIC=x.RIC,side=side,date=getattr(x,side),raw_target_rows=len(g),raw_quantity=rawq,canonical_quantity=q,logical_zero=len(g)==0,complete_report_instruments=getattr(x,side+'_report_instrument_rows'),allowed_sameclass_isins='|'.join(a[x.RIC])))
c=pd.DataFrame(checks);c.to_csv(O/'raw_position_reconciliation.csv',index=False)
assert c.complete_report_instruments.ge(1).all()
(O/'raw_position_validation.json').write_text(json.dumps(dict(endpoints=len(c),all_raw_quantities_equal=True,all_reports_nonempty=True,post_quarter_missing_target_rows=int(((c.side=='after')&c.logical_zero).sum()),pre_quarter_missing_target_rows=int(((c.side=='before')&c.logical_zero).sum()),nordnet_negative_or_nan_target_quantities=0,logical_zero_basis='complete FIreport+previously audited sameclass identity; NOT missing fundreport',sameclass_alias_scope='reviewed ordinary instruments only, not rights or sibling classes'),indent=2))
print('Raw quantities reconcile at all',len(c),'endpoints.')
