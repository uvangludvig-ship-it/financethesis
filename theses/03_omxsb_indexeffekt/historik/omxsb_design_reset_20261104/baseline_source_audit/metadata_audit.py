"""Read only old cohort labels and gate metadata; no quantities/outcomes."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import csv,gzip,hashlib,json
P=Path(__file__).resolve().parent
C=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke')
R=Path('/Users/ludviguvang/dev/financethesis')
G=C/'work/omxsb_scaled_round_20261103/independent_design/retention'
paths={'roles':G/'FROZEN_ROLES.csv','gate':G/'SECURITY_SOURCE_GATE.csv',
 'ledger':R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz',
 'code':Path(__file__)}
def read(p):
 op=gzip.open if p.suffix=='.gz' else open
 with op(p,'rt',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
out=P/'METADATA_AUDIT.json'
assert not out.exists()
hashes={k:{'path':str(p),'sha256':sha(p)} for k,p in paths.items()}
s=read(paths['roles']);sg={(r['review'],r['ric']):r for r in read(paths['gate'])}
n=Counter((r['event_id'],r['role']) for r in read(paths['ledger']) if r['type']=='addition' and r['review']<'2024' and r['component']=='new')
failed=[]
for x in s:
 if 'q0_' in sg[x['review'],x['ric']]['reason']:
  failed.append({**{k:x[k] for k in ['event_id','review','role','ric']},'new_positions':n[x['event_id'],x['role']],'reason':sg[x['review'],x['ric']]['reason']})
zeros=[x for x in s if x['role']!='event' and n[x['event_id'],x['role']]==0]
result={'at_utc':datetime.now(timezone.utc).isoformat(),'no_new_q2_quantities_or_outcomes_read':True,'no_new_capital_pp_computed':True,
 'events':len({r['event_id'] for r in s}),'reviews':len({r['review'] for r in s}),
 'entrant_counts_by_role':{role:sum(n[x['event_id'],role] for x in s if x['role']==role) for role in ['event','c1','c2','c3']},
 'zero_peer_cohorts':len(zeros),'events_with_zero_peer_cohort':len({x['event_id'] for x in zeros}),
 'q0_gate_failed_roles':failed,'inputs':hashes}
assert result['events']==70 and result['reviews']==10 and len(zeros)==44
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='inputs'},ensure_ascii=False,indent=2))
