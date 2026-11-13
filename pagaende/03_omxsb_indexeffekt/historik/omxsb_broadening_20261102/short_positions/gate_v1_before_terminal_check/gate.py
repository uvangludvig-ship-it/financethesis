from pathlib import Path
import pandas as pd,numpy as np,re,json,hashlib,datetime
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis')
d=pd.read_csv(O/'raw_positions.csv.gz',keep_default_na=False);d.position_numeric=pd.to_numeric(d.position_numeric,errors='coerce')
d=d[d.position_date.ge('2012-11-01')]
E=pd.read_csv(O/'issuer_preoutcome_coverage.csv');E=E[E.types.eq('addition')]
U=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv')
rows=[];coverage=[]
for e in E.itertuples():
 ids=set(e.issuer_isins.split(';'));yr=int(e.review[:4]);month=yr*100+10 if e.review.endswith('1') else (yr+1)*100+4
 nextids=set(U.loc[U.month.eq(month)&U.company_code.eq(e.company_code)&U.stock_type,'isin'])
 allowed=ids|nextids
 prior=d[d['isin'].isin(ids)&d.position_date.le(e.baseline)]
 allrows=d[d['isin'].isin(allowed)&d.position_date.le(e.post)].copy()
 holders=sorted(prior.holder_key.unique());ncohort=0
 for holder in holders:
  pre=prior[prior.holder_key.eq(holder)];lastdate=pre.position_date.max();base=pre[pre.position_date.eq(lastdate)]
  if not base.position_numeric.ge(.5).any():continue
  ncohort+=1;reasons=[]
  if base.position_raw.nunique()!=1:reasons.append('conflicting_baseline_rows')
  if base.comment.ne('').any():reasons.append('commented_baseline')
  future=allrows[allrows.holder_key.eq(holder)&allrows.position_date.gt(e.baseline)]
  if future.groupby('position_date').position_raw.nunique().gt(1).any():reasons.append('conflicting_followup_date')
  if future.comment.ne('').any():reasons.append('commented_followup')
  if (future.position_numeric.isna()&~future.below_public_threshold).any():reasons.append('unparsed_followup')
  compact=lambda x:re.sub(r'[^a-z0-9]','',x)
  variants={x for x in allrows.holder_key.unique() if compact(x)==compact(holder)}
  if len(variants)>1:reasons.append('holder_punctuation_identity_ambiguity')
  issuer_names=set(base.issuer)
  stray=d[d.holder_key.eq(holder)&d.issuer.isin(issuer_names)&d.position_date.gt(e.baseline)&d.position_date.le(e.post)&~d['isin'].isin(allowed)]
  if len(stray):reasons.append('unaccepted_ISIN_same_exact_issuer')
  rows.append(dict(event_id=e.event_ids,review=e.review,company_code=e.company_code,RIC=e.RICs,
                   holder_key=holder,holder=base.iloc[0].holder,baseline=e.baseline,end=e.end,post=e.post,
                   AD=e.AD,ED=e.ED,baseline_report_date=lastdate,baseline_position=base.iloc[0].position_raw,
                   baseline_source_rows=';'.join(map(str,base.source_row)),
                   baseline_isins=e.issuer_isins,accepted_followup_isins=';'.join(sorted(allowed)),
                   baseline_FI_issuer_names=';'.join(sorted(issuer_names)),
                   valid=not reasons,reasons=';'.join(reasons),followup_comment_rows=';'.join(map(str,future.loc[future.comment.ne(''),'source_row'])),
                   identity_stray_rows=';'.join(map(str,stray.source_row))))
 coverage.append(dict(event_id=e.event_ids,review=e.review,company_code=e.company_code,baseline_cohort=ncohort))
C=pd.DataFrame(rows);C.to_csv(O/'cohort_gate.csv',index=False)
V=pd.DataFrame(coverage);valid=C[C.valid].groupby('event_id').size();V['valid_cohort']=V.event_id.map(valid).fillna(0).astype(int);V.to_csv(O/'event_coverage_gate.csv',index=False)
files=[O/'DECLARATION.txt',Path(__file__),O/'inventory.py',O/'raw_positions.csv.gz',O/'cohort_gate.csv',O/'event_coverage_gate.csv',O/'issuer_preoutcome_coverage.csv']
lock=dict(frozen_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),new_followup_changes_computed=False,
          initial_addition_events=len(E),baseline_candidate_pairs=len(C),valid_pairs=int(C.valid.sum()),
          valid_issuer_events=int(C[C.valid].event_id.nunique()),valid_reviews=int(C[C.valid].review.nunique()),
          valid_companies=int(C[C.valid].company_code.nunique()),excluded=C[~C.valid].to_dict('records'),
          files={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in files})
(O/'COHORT_LOCK.json').write_text(json.dumps(lock,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in lock.items()if k!='files'},indent=2,ensure_ascii=False))
