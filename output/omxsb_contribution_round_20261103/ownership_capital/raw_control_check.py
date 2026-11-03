from pathlib import Path
import pandas as pd,numpy as np,zipfile,xml.etree.ElementTree as ET,re,json,datetime,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership'
keep=set(pd.read_csv(O/'fund_support.csv').event_id);s=pd.read_csv(OWN/'security_role_gate.csv');s=s[s.event_id.isin(keep)&s.role.ne('event')].drop_duplicates(['review','ric']);dates=set(s.q0)|set(s.q1);funds={'51482','60824'}
I=pd.read_csv(R/'output/omxsb_audit_20261031/fi_raw_report_inventory.csv',dtype={'fund':str});I=I[I.fund.isin(funds)&I.quarter.isin(dates)];I=I[I.published_file.eq(I.groupby(['fund','quarter']).published_file.transform('max'))].drop_duplicates(['zip','file'])
raw={};reportrows={};source=[];BAD=re.compile('[^\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd]')
for x in I.itertuples():
 p=R/'data/raw/fi'/x.zip
 with zipfile.ZipFile(p) as zz:b=zz.read(x.file)
 try:r=ET.fromstring(b)
 except ET.ParseError:r=ET.fromstring(BAD.sub('',b.decode('utf-8-sig')))
 for node in r.iter():node.tag=node.tag.split('}')[-1]
 def tx(node,key):
  z=next(node.iter(key),None);return z.text.strip() if z is not None and z.text else ''
 assert tx(r,'Fond_institutnummer')==x.fund and tx(r,'Kvartalsslut')==x.quarter
 rows=list(r.iter('FinansielltInstrument'));assert len(rows)>0;reportrows[(x.fund,x.quarter)]=len(rows)
 for node in rows:
  isin=tx(node,'ISIN-kod_instrument');q=tx(node,'Antal')
  if not q:continue
  raw[(x.fund,x.quarter,isin)]=raw.get((x.fund,x.quarter,isin),0.)+float(q)
 source.append(dict(fund_id=x.fund,quarter=x.quarter,raw_zip=str(p),xml_member=x.file,xml_sha256=hashlib.sha256(b).hexdigest(),full_report_instrument_rows=len(rows)))
cols=['Fond_institutnummer','Kvartalsslut','ISIN-kod_instrument','Antal'];parts=[]
for d in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=cols,dtype={'Fond_institutnummer':str},chunksize=300000):parts.append(d[d.Fond_institutnummer.isin(funds)&d.Kvartalsslut.isin(dates)])
h=pd.concat(parts);qty=h.groupby(cols[:3]).Antal.sum().to_dict();res=[]
for x in s.itertuples():
 for f in sorted(funds):
  for dt in [x.q0,x.q1]:
   assert (f,dt) in reportrows
   expected=sum(raw.get((f,dt,isin),0.) for isin in x.aliases.split(';'));derived=sum(qty.get((f,dt,isin),0.) for isin in x.aliases.split(';'))
   res.append(dict(review=x.review,ric=x.ric,fund_id=f,quarter=dt,raw_full_report_present=True,raw_target_absent_or_zero=expected==0,quantity_matches=abs(expected-derived)<1e-8,abs_quantity_error=abs(expected-derived)))
d=pd.DataFrame(res);assert d.quantity_matches.all();d.to_csv(O/'raw_control_endpoint_checks.csv',index=False);pd.DataFrame(source).to_csv(O/'raw_control_report_map.csv',index=False)
z=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),raw_reports=len(source),distinct_control_security_quarters=len(s),endpoints=len(d),zero_endpoints=int(d.raw_target_absent_or_zero.sum()),max_raw_to_derived_quantity_error=float(d.abs_quantity_error.max()),all_pass=True,selection='Fixed two independently documented funds51482and60824; all retained distinct control security/review pairs; not a new economic subgroup test.')
(O/'raw_control_validation.json').write_text(json.dumps(z,indent=2));print(json.dumps(z,indent=2))
