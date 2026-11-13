"""Bounded source diagnostics after validated historical names but empty weights.
All TR field names were documented before use. No data/outcome-selected metric.
GI is a source-availability diagnostic in the same uncapped family, never a
silent replacement for the specified PI original-basket requirement.
"""
from pathlib import Path
import lseg.data as ld
import json,datetime,signal,hashlib
O=Path(__file__).resolve().parent;P=O/'private';P.mkdir(exist_ok=True)
fields=['TR.IndexConstituentRIC','TR.IndexConstituentWeightPercent','TR.IndexConstituentShares']
queries=[
 ('PI_weight_only','.OMXSBPI',['TR.IndexConstituentWeightPercent'],{'SDate':'2023-11-30'}),
 ('PI_shares_only','.OMXSBPI',['TR.IndexConstituentShares'],{'SDate':'2023-11-30'}),
 ('PI_dated_chain','0#.OMXSBPI(20231130)',fields,{'SDate':'2023-11-30'}),
 ('GI_verified_chain','0#.OMXSBGI',fields,{'SDate':'2023-11-30'}),
 ('PI_dated_fields','.OMXSBPI',['TR.IndexConstituentRIC(SDate=2023-11-30)','TR.IndexConstituentWeightPercent(SDate=2023-11-30)','TR.IndexConstituentShares(SDate=2023-11-30)'],{}),
 ('PI_current_content_control','.OMXSBPI',fields,{}),
]
spec={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'source-presence only; no returns or weight changes','requests':[dict(label=l,universe=u,fields=f,parameters=p)for l,u,f,p in queries],'historical_membership_observed':True,'previous_weight_values_were_all_blank':True,'source_fields':'LSEG discussion105781 and65797; dated-chain syntax in LSEG historical constituents guides','no_current_value_used_as_historical':True}
(O/'ALTERNATIVE_REQUEST_LOCK.json').write_text(json.dumps(spec,indent=2))
def timeout(a,b):raise TimeoutError('60-second bounded source timeout')
signal.signal(signal.SIGALRM,timeout);ld.open_session();rows=[]
for label,univ,ff,params in queries:
 r=dict(label=label,universe=univ,fields=ff,parameters=params,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  signal.alarm(60);d=ld.get_data(universe=[univ],fields=ff,parameters=params);signal.alarm(0)
  p=P/(label+'.csv');d.to_csv(p,index=False)
  nonempty={str(c):int((d[c].notna()&d[c].astype(str).str.strip().ne('')).sum())for c in d.columns}
  r.update(status='response',rows=len(d),columns=list(d.columns),nonempty_counts=nonempty,private_file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 except Exception as e:
  signal.alarm(0);r.update(status='error',error_type=type(e).__name__,error=str(e)[:700])
 rows.append(r);(O/'ALTERNATIVE_REQUEST_RESULTS.json').write_text(json.dumps(rows,indent=2));print(json.dumps(r),flush=True)
