from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import analysis_paths
_PORTABLE_REPO, _PORTABLE_OUT = analysis_paths('retention_followup_20261102')
import pandas as pd, json, hashlib, numpy as np
O=_PORTABLE_OUT
R=_PORTABLE_REPO
S=R/'output/omxsb_open_questions_20261102/retention'
T=pd.read_csv(S/'raw_tracker_transferable_securities.csv.gz')
Q=pd.read_csv(O/'position_quantities.csv')
C=pd.read_csv(O/'endpoint_source_gate.csv')
I={(r.event_id,r.fund_id,r.quarter):r.ordinary_ISINs.split(';') for r in C.itertuples()}
diff=[]
ratios=[]
for r in Q.itertuples():
    vals=[]
    for dt in [r.index_q,r.next_q]:
        z=T[T.Fond_institutnummer.eq(r.fund_id)&T.Kvartalsslut.eq(dt)&T['ISIN-kod_instrument'].isin(I[(r.event_id,r.fund_id,dt)])]
        vals.append(float(z.Antal.sum()) if len(z) else 0.)
    diff.extend([vals[0]-r.q_index,vals[1]-r.q_next])
    ratios.append(vals[1]/vals[0] if vals[0]>0 else np.nan)
assert max(abs(x) for x in diff)<1e-6
assert np.allclose(ratios,Q.quantity_retention_ratio,equal_nan=True)
print('ONLYDECREASE',Q[Q.quantity_direction.eq('decreased')].to_string(index=False))
sg=pd.read_csv(S/'share_data_gate.csv')
st=sg[~sg.passes_date_gate]
st.to_csv(O/'previous_stale_share_snapshots.csv',index=False)
print('STALE',st[['event_id','RIC','quarter','shares_date','age_days']].to_string(index=False))
assert hashlib.sha256((O/'quantity_gate_frozen.csv').read_bytes()).hexdigest()==json.loads((O/'gate_frozen_summary.json').read_text())['gate_sha256']
(O/'independent_quantity_validation.json').write_text(json.dumps(dict(raw_endpoint_comparisons=len(diff),max_absolute_quantity_error=max(abs(x) for x in diff),ratios_all_equal=True,previous_stale_share_snapshots=len(st),decreased_rows=Q[Q.quantity_direction.eq('decreased')].to_dict('records')),indent=2))
