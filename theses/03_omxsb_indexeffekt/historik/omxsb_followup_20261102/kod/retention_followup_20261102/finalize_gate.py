from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import analysis_paths
_PORTABLE_REPO, _PORTABLE_OUT = analysis_paths('retention_followup_20261102')
import pandas as pd,numpy as np,json,hashlib
O=_PORTABLE_OUT;R=_PORTABLE_REPO;SRC=R/'output/omxsb_open_questions_20261102/retention'
G=pd.read_csv(O/'unit_gate_initial.csv');T=pd.read_csv(SRC/'raw_tracker_transferable_securities.csv.gz');EP=pd.read_csv(SRC/'retention_endpoint_audit.csv');D=pd.read_csv(SRC/'retention_event_fund_status.csv');D=D[D.type.eq('addition')]
# Primary source decisions made before quantity ratios. No split factor is inferred from fund quantity changes.
actions={
 'OMXSB-2021H2-05':('directed_issue_ordinary_unit_unchanged','https://l.cdn.bequoted.com/1/prospectus-regarding-the-admission-to-trading-of-the-common--94648/Cibus_Prospectus.pdf'),
 'OMXSB-2021H2-06':('rights_issue_ordinary_unit_unchanged_BTA_excluded','https://www.stillfront.com/en/wp-content/uploads/sites/2/2024/05/stillfront-group-ab-publ-prospekt-25-februari-2022-1.pdf'),
 'OMXSB-2021H2-07':('acquisition_consideration_share_issue','https://investors.cint.com/sites/cint/files/pr/202201310568-1.pdf'),
 'OMXSB-2022H2-03':('rights_issue_ordinary_unit_unchanged','https://www.beijerref.com/pressrelease/beijer-ref-publishes-the-final-outcome-of-the-rights-issue'),
 'OMXSB-2022H2-08':('rights_issue_ordinary_unit_unchanged','https://ctekgroup.com/en/investors/rights-issue/')}
G['splitfactor']=1.;G['source_action']=[actions.get(e,('screened_no_unit_change',''))[0]for e in G.event_id];G['source_url']=[actions.get(e,('',''))[1]for e in G.event_id]
G['same_tracker_ordinary_ISINs']=G.index_tracker_ISINs.eq(G.next_tracker_ISINs)
G['units_gate_pass']=G.same_tracker_ordinary_ISINs&G.index_current_price&G.next_current_price&G.index_agreed_funds.ge(3)&G.next_agreed_funds.ge(3)&(G.close_diagnostic_one|G.event_id.isin(actions))
G['exclusion_reason']=np.where(G.units_gate_pass,'','unresolved_identity_or_unit_chain')
# BTA is never an ordinary alias; neither tracker holds it at the relevant endpoint.
bta=T[T['ISIN-kod_instrument'].eq('SE0017564024')&T.Kvartalsslut.eq('2022-03-31')];assert bta.empty
G['ordinary_identity_note']='same ordinary tracker ISIN both endpoints; no quantity-selected alias';G.loc[G.RIC.eq('SFRG.ST'),'ordinary_identity_note']='SE0015346135 ordinary; SE0017564024 BTA excluded; tracker positions unaffected'
# Check only exact, already held tracker ISINs for both relevant endpoints; compare source sum to previous endpoint audit.
checks=[]
for ev in D.itertuples():
 g=G.set_index('event_id').loc[ev.event_id];allowed=set(str(g.index_tracker_ISINs).split(';'))
 for dt in [ev.index_q,ev.next_q]:
  z=T[T.Fond_institutnummer.eq(ev.fund_id)&T.Kvartalsslut.eq(dt)&T['ISIN-kod_instrument'].isin(allowed)]
  ep=EP[EP.event_id.eq(ev.event_id)&EP.fund_id.eq(ev.fund_id)&EP.quarter.eq(dt)].iloc[0]
  invalid=z.Antal.isna()|z.Antal.lt(0)|(z.Antal.gt(0)&~z.Marknadsvärde_instrument.gt(0))|(z.Antal.eq(0)&z.Marknadsvärde_instrument.gt(0));assert not invalid.any();assert ep.status!='unknown'
  q=z.Antal.sum()if len(z)else 0.;original=ep.raw_quantity_unadjusted if pd.notna(ep.raw_quantity_unadjusted)else 0.;assert abs(q-original)<1e-6
  checks.append(dict(event_id=ev.event_id,fund_id=ev.fund_id,quarter=dt,ordinary_ISINs=';'.join(sorted(allowed)),matched_rows=len(z),invalid_rows=int(invalid.sum()),matches_prior_endpoint=True))
pd.DataFrame(checks).to_csv(O/'endpoint_source_gate.csv',index=False)
# Review-chain membership is recorded evidence, not exhaustive daily notice coverage.
M=pd.read_csv(R/'code/claude_checks/data/medlemskap_verifierad.csv');M=M.set_index(['review_after','ric']);A=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',parse_dates=['effective_date']);mem=[]
for x in G.itertuples():
 m=M.loc[(x.review,x.RIC)]if (x.review,x.RIC)in M.index else None
 ev=A[A.RIC.eq(x.RIC)&A.effective_date.gt(x.index_q)&A.effective_date.le(x.next_q)]
 mem.append(dict(event_id=x.event_id,RIC=x.RIC,review=x.review,chain_status=m.status if m is not None else 'missing',chain_source=m.kalla if m is not None else '',recorded_intermediate_events=len(ev),daily_membership_independently_certified=False))
pd.DataFrame(mem).to_csv(O/'membership_evidence.csv',index=False);G.to_csv(O/'quantity_gate_frozen.csv',index=False)
s=dict(events=len(G),passed=int(G.units_gate_pass.sum()),excluded=G.loc[~G.units_gate_pass,['event_id','exclusion_reason']].to_dict('records'),endpoint_source_checks=len(checks),new_ordinary_split_factors_other_than_one=0,verified_nonunit_share_issues=len(actions),BTA_in_relevant_tracker_rows=0,strict_daily_membership=False,gate_sha256=hashlib.sha256((O/'quantity_gate_frozen.csv').read_bytes()).hexdigest());(O/'gate_frozen_summary.json').write_text(json.dumps(s,indent=2));print(json.dumps(s,indent=2));print(pd.DataFrame(mem).chain_status.value_counts().to_dict());print('Recorded_intermediate_events',sum(x['recorded_intermediate_events']for x in mem))
