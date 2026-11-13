"""Independent raw-cell, interval, aggregation and frozen-sample verification."""
from pathlib import Path
import argparse,zipfile,xml.etree.ElementTree as ET,json,hashlib,itertools
import pandas as pd,numpy as np
parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,default=Path(__file__).resolve().parent)
parser.add_argument('--out',type=Path);args=parser.parse_args();I=args.input.resolve();O=(args.out or I).resolve()
T='urn:oasis:names:tc:opendocument:xmlns:table:1.0';F='urn:oasis:names:tc:opendocument:xmlns:office:1.0'
source={}
for name,kind in [('HistoriskaPositioner_2026-11-02.ods','history_20261102'),('AktuellaPositioner_2026-11-02.ods','current_20261102')]:
 with zipfile.ZipFile(I/name) as z:root=ET.fromstring(z.read('content.xml'))
 for table in root.findall('.//{'+T+'}table'):
  for n,row in enumerate(table.findall('{'+T+'}table-row'),1):
   cols=[]
   for c in row:
    if c.tag not in ['{'+T+'}table-cell','{'+T+'}covered-table-cell']:continue
    repeat=int(c.get('{'+T+'}number-columns-repeated','1'))
    for _ in range(min(repeat,6-len(cols))):cols.append(c)
    if len(cols)==6:break
   if len(cols)<6:continue
   values=[' '.join(c.itertext()).strip()for c in cols]
   dt=cols[4].get('{'+F+'}date-value',values[4])[:10]
   source[f'{kind}:{n}']=dict(holder=values[0],isin=values[2],position=values[3],date=dt,comment=values[5])
H=pd.read_csv(O/'holder_position_intervals.csv');E=pd.read_csv(O/'issuer_position_intervals.csv');V=pd.read_csv(O/'review_position_intervals.csv');S=json.loads((O/'RESULTS.json').read_text())
G=pd.read_csv(I/'cohort_gate.csv');G=G[G.valid]
assert len(H)==len(G)==47 and set(zip(H.event_id,H.holder_key))==set(zip(G.event_id,G.holder_key))
for z in H.itertuples():
 for tag in ['base','end','post']:
  refs=getattr(z,tag+'_source_rows').split(';');raw=getattr(z,tag+'_position_raw')
  for ref in refs:
   r=source[ref];assert r['position']==raw and r['date']==getattr(z,tag+'_report_date') and r['comment']==''
  if raw.startswith('<') or float(raw.replace(',','.'))<.5:lo,hi=0,5
  else:
   s=raw.replace(',','.').split('.');lo=int(s[0])*10+(int(s[1][0]) if len(s)>1 and s[1] else 0);hi=lo+1
  assert lo==getattr(z,tag+'_L10') and hi==getattr(z,tag+'_U10')
 assert z.base_L10>=5
columns=[t+'_'+b+'10'for t in ['base','end','post']for b in ['L','U']]
for table in [H,E]:
 for z in table.itertuples():
  vertices=[]
  for a,b,c in itertools.product([z.base_L10,z.base_U10],[z.end_L10,z.end_U10],[z.post_L10,z.post_U10]):vertices.append((b-max(a,c))/10)
  assert np.isclose(min(vertices),z.hump_lower_pp) and np.isclose(max(vertices),z.hump_upper_pp)
  status='certain_positive'if z.hump_lower_pp>0 else ('strict_positive_impossible'if z.hump_upper_pp<=0 else 'undetermined')
  assert status==z.hump_status
  assert np.isclose((z.end_L10-z.base_U10)/10,z.build_lower_pp)
  assert np.isclose((z.end_U10-z.base_L10)/10,z.build_upper_pp)
  assert np.isclose((z.post_L10-z.end_U10)/10,z.after_change_lower_pp)
  assert np.isclose((z.post_U10-z.end_L10)/10,z.after_change_upper_pp)
a=H.groupby('event_id')[columns].sum();b=E.set_index('event_id')[columns];assert a.sort_index().equals(b.sort_index())
metrics=[k for k in E.columns if k.endswith('_pp')]
v=E.groupby('review')[metrics].mean();saved=V.set_index('review')[metrics]
assert np.allclose(v.sort_index(),saved.sort_index(),atol=1e-12)
for k in metrics:
 assert np.isclose(v[k].mean(),S['equal_review_mean_identification_bounds'][k])
 assert np.isclose(E[k].mean(),S['equal_event_mean_identification_bounds'][k])
assert S['issuer_hump_status']==E.hump_status.value_counts().to_dict()
lock=json.loads((I/'COHORT_LOCK.json').read_text());assert pd.Timestamp(lock['frozen_at_utc'])<pd.Timestamp(S['run_at_utc'])
for k,h in lock['files'].items():assert hashlib.sha256((I/Path(k).name).read_bytes()).hexdigest()==h
out=dict(raw_endpoint_checks=3*len(H),all_checks_passed=True,holder_events=len(H),issuer_events=len(E),reviews=len(V),
         current_terminal_or_closed_marker_for_all_pairs=H.terminal_verification_method.isin(['current_export_exact_identity','last_historical_report_below_public_threshold']).all().item(),
         terminal_unknown_pairs_in_analysis=0,locked_before_outcomes=True,
         input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [I/'COHORT_LOCK.json',O/'holder_position_intervals.csv',O/'issuer_position_intervals.csv',O/'review_position_intervals.csv',O/'RESULTS.json']})
(O/'verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
