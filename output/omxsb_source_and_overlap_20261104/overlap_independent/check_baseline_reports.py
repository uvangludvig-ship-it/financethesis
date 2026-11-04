"""Post-replay metadata audit of every original q0/q1 entrant report.

No q2 quantity or outcome is read; no private fund rows are exported.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv, gzip, hashlib, json

P=Path(__file__).resolve().parent
CHAT=P.parents[2]
REPO=Path('/Users/ludviguvang/dev/financethesis')
paths={
 'ledger':REPO/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz',
 'roles':CHAT/'work/omxsb_scaled_round_20261103/independent_design/retention/FROZEN_ROLES.csv',
 'metadata':REPO/'output/omxsb_open_questions_20261102/demand_quarter/raw_fund_report_metadata.csv',
 'code':Path(__file__),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 op=gzip.open if p.suffix=='.gz' else open
 with op(p,'rt',newline='') as f:return list(csv.DictReader(f))
target=P/'BASELINE_REPORT_CHECK.json'
assert not target.exists(),'Preserve the first metadata audit.'
start=datetime.now(timezone.utc).isoformat()
hashes={k:{'path':str(v),'sha256':sha(v)} for k,v in paths.items()}
ledger=[r for r in read(paths['ledger']) if r['type']=='addition' and r['review']<'2024' and r['role']=='event' and r['component']=='new']
roles={r['event_id']:r for r in read(paths['roles']) if r['role']=='event'}
rows=read(paths['metadata'])
meta={(r['Fond_institutnummer'],r['Kvartalsslut']):r for r in rows}
assert len(meta)==len(rows)
good=changed=missing=0
for x in ledger:
 role=roles[x['event_id']]
 rr=[meta.get((x['fund_id'],role[q])) for q in ('q0','q1')]
 valid=all(r is not None and float(r['actual_instrument_rows'])>0 and r['fund_isin'].strip().lower() not in ('','nan','none') for r in rr)
 stable=valid and len({r['fund_isin'] for r in rr})==1
 good+=stable;missing+=not valid;changed+=valid and not stable
result={'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),
 'original_entrant_positions':len(ledger),'q0_q1_nonempty_reports_and_stable_fund_isin':good,
 'missing_or_empty_baseline_reports':missing,'changed_baseline_fund_isin':changed,
 'q2_quantity_read':False,'raw_fund_rows_exported':False,
 'meaning':'Nonempty report presence under the existing FI extraction; not external proof that every report is exhaustive.',
 'inputs':hashes}
assert len(ledger)==good==737 and missing==changed==0
assert all(sha(Path(v['path']))==v['sha256'] for v in hashes.values())
target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='inputs'},ensure_ascii=False,indent=2))
