"""Deterministic source-only HFT pilot. No price, return or volume columns read."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import pandas as pd

ROOT = Path('/Users/ludviguvang/dev/financethesis')
OUT = Path(__file__).resolve().parent
PATHS = {
    'events': ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',
    'identities': ROOT/'output/omxsb_mechanism_frontier_20261102/ownership/security_role_gate.csv',
    'calendar': ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',
    'cancellations': ROOT/'output/omxsb_execution_followup_20261102/sources/known_cancellations.csv',
}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

ec = ['event_id','effective_date','announcement_date','company','ticker','type',
      'review_cycle','source_url','verification','notes','RIC']
E = pd.read_csv(PATHS['events'], usecols=ec, dtype=str)
G = pd.read_csv(PATHS['identities'], usecols=['event_id','role','ric','instrument',
        'nasdaq_isin','q0_isins','q1_isins','source_url'], dtype=str)
G = G.loc[G.role.eq('event')].rename(columns={'source_url':'identity_source_url'})
assert not G.event_id.duplicated().any()
C = pd.read_csv(PATHS['calendar'], usecols=['ric','date'], dtype=str)
cal = sorted(C.loc[C.ric.eq('.OMXSBGI'),'date'].dropna().unique())
pos = {d:i for i,d in enumerate(cal)}
K = pd.read_csv(PATHS['cancellations'], usecols=['review','RIC'], dtype=str)
cancelled = set(zip(K.review,K.RIC))
selected=[]; checked=[]
for review in ['2019H1','2023H2']:
    for ty in ['addition','deletion']:
        rows=E.loc[E.review_cycle.eq(review)&E.type.eq(ty)].sort_values('event_id')
        assert len(rows)>0
        for _,e in rows.iterrows():
            reasons=[]; ident=G.loc[G.event_id.eq(e.event_id)]
            if not isinstance(e.RIC,str) or '.ST' not in e.RIC: reasons.append('no_stockholm_RIC')
            if e.effective_date not in pos: reasons.append('no_effective_calendar_date')
            if (review,e.RIC) in cancelled: reasons.append('known_cancelled_event')
            if len(ident)!=1: reasons.append('no_unique_dated_identity')
            else:
                g=ident.iloc[0]
                if g.ric!=e.RIC: reasons.append('RIC_disagreement')
                if pd.isna(g.nasdaq_isin) or len(g.nasdaq_isin)!=12: reasons.append('no_exact_ISIN')
                if not any(str(g.nasdaq_isin) in str(g[k]).split(';') for k in ['q0_isins','q1_isins']):
                    reasons.append('no_quarter_identity_crosscheck')
            checked.append({'event_id':e.event_id,'review':review,'type':ty,
                            'selected':not reasons,'rejection_reason':';'.join(reasons)})
            if reasons: continue
            p=pos[e.effective_date]
            selected.append(dict(event_id=e.event_id,review=review,type=ty,direction=1 if ty=='addition' else -1,
                company=e.company,ticker=e.ticker,RIC=e.RIC,ISIN=g.nasdaq_isin,
                AD=e.announcement_date,ED=e.effective_date,comparison_date=cal[p-6],
                comparison_next_date=cal[p-5],auction_date=cal[p-1],next_date=cal[p],
                event_source_url=e.source_url,identity_source_url=g.identity_source_url,
                metadata_notes=e.notes))
            break
        else: raise ValueError(f'No metadata-valid event in {review}/{ty}')
S=pd.DataFrame(selected)
assert len(S)==4 and S.event_id.is_unique
S.to_csv(OUT/'PILOT_EVENTS.csv',index=False)
pd.DataFrame(checked).to_csv(OUT/'PILOT_SELECTION_LOG.csv',index=False)
sessions=[]
for e in selected:
    for role,col in [('comparison','comparison_date'),('comparison_next','comparison_next_date'),
                     ('rebalance','auction_date'),('rebalance_next','next_date')]:
        sessions.append({k:e[k] for k in ['event_id','review','type','ticker','RIC','ISIN']}|
                        {'session_role':role,'date':e[col],'AD':e['AD'],
                         'comparison_session_is_announcement_date':e['comparison_date']==e['AD']})
pd.DataFrame(sessions).to_csv(OUT/'PILOT_REQUEST_SESSIONS.csv',index=False)
lock={'created_utc':datetime.now(timezone.utc).isoformat(),'source_only':True,
      'outcome_columns_read':[], 'inputs':{k:{'path':str(p),'sha256':sha(p)} for k,p in PATHS.items()},
      'spec_sha256':sha(OUT/'PRE_ACQUISITION_SPEC.txt'),'selection_script_sha256':sha(Path(__file__)),
      'selected_event_ids':S.event_id.tolist(),
      'notes':['No CAR, volume, return or price level fields read.',
               'Calendar uses source rows for OMXSBGI, not values or individual-stock availability.',
               '2023H2 comparison session is AD, with announcement after closing auction; next-day baseline is contaminated by announcement news and is not a neutral reversal comparator.']}
(OUT/'PILOT_SELECTION_LOCK.json').write_text(json.dumps(lock,indent=2,ensure_ascii=False)+'\n')
print(S[['event_id','ticker','ISIN','comparison_date','comparison_next_date','auction_date','next_date']].to_string(index=False))
