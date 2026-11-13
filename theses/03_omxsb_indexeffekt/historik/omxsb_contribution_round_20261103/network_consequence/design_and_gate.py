"""Baseline-only feasibility gate. Never opens price/return/value outcome columns.

Run with the adjacent .venv/bin/python. Inputs remain in the existing local repo.
"""
from pathlib import Path
import datetime as dt, hashlib, json, re
import numpy as np
import pandas as pd

R=Path('/Users/ludviguvang/dev/financethesis')
O=Path(__file__).resolve().parent
P={
 'fi':R/'data/derived/fi/fi_holdings_long.csv.gz',
 'metadata':R/'output/omxsb_mechanism_frontier_20261102/ownership/fund_metadata_classification.csv',
 'roles':R/'output/omxsb_mechanism_frontier_20261102/ownership/security_role_gate.csv',
 'existing_coverage':R/'output/omxsb_mechanism_frontier_20261102/ownership/coverage.csv',
 'matches':R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv',
 'pool':R/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv',
 'roster':R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv',
 'events':R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',
}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for z in iter(lambda:f.read(1024*1024),b''):h.update(z)
 return h.hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()

DESIGN={
 'recorded_utc':utc(),
 'status':'New exploratory consequence design, not a preregistration before all previous OMXSB work.',
 'previous_known_results':'Ownership increase and existing generic index comovement literature known. No new network-return contrasts inspected. While finding the input schema, three old 2017 event_paths CAR rows were accidentally printed; these are outside this 2019–25 design and are not network outcomes.',
 'question':'Does a stock become more correlated with its own pre-existing OMXSB-family owners\u2019 portfolios than with its pre-existing other broad-Sweden-benchmark owners\u2019 portfolios, relative to three already-fixed matched stocks?',
 'sample':'Exactly the 118 additions in the previously eligible 2019–25 ownership sample; no replacement controls. Deletions are not a second primary test. All four matched roles must pass baseline and return coverage gates.',
 'funds':'Nonempty, unique legal fund ISIN at baseline q0. Dated q0 benchmark, simple unmixed OMXSB family (regex stockholm benchmark|omxsb|\\bsbx) versus simple other broad Sweden benchmark (existing broad & simple flags). No restriction based on subsequent benchmark, ownership, fund survival, or name indicating passive strategy. Custom and ESG family labels retained and disclosed as broad family, not literal tracker mandates.',
 'holdings':'Only q0 March/September positive quantities and market values, ordinary transferable-security container. Fund excluded across all four roles if a duplicate, missing or negative ordinary-security quantity/value appears in relevant baseline ordinary universe or any target alias. Duplicated legal IDs excluded, never added. Baseline target owner requires exactly one positive supported ordinary ISIN alias.',
 'peer_identity':'Require exact RIC/ordinary-share mapping with one RIC per ISIN in existing review pool. All share classes of one issuer can contribute capital but effective issuer count aggregates classes. Require the identical ISIN to be in the latest Nasdaq roster strictly before q0 (previous October for H1; April for H2), ordinary and listed, with nonmissing industry/company; current review issuer must agree. This conservative intersection excludes recent IPOs, changed ISINs, and uncertain identities. Industry is frozen at this prior roster, not a later classification.',
 'portfolio':'For target i, group g, each baseline owner f weight a_if=MV_if/sum_f MV_if. Each owner peer portfolio p_fj=MV_fj/sum eligible cross-industry peer MV_fj. w_igj=sum_f a_if*p_fj, renormalized only when a fund is rejected by the fixed data gate. Exclude target issuer and same prior industry. No future owner identities. Freeze exactly these weights before and after.',
 'capital_coverage':'Each retained owner must map at least 90% of its valid positive prior-roster ordinary cross-industry capital after metadata event exclusions. The denominator includes peer ISINs without a safe return link. This is coverage of verified baseline domestic ordinary holdings, not all global assets or NAV. Unknown/invalid values cause entire owner exclusion instead of a zero. Report retained fraction of each group\u2019s original target capital.',
 'contrast_gate':'Per role, each group has positive target capital and effective issuer count >=10; each retained group covers >=90% of its original eligible owners\u2019 target capital; total variation distance between portfolio issuer weights >=0.15 and cosine similarity <=0.98. These practical measurement thresholds are not power guarantees.',
 'sample_gate':'Proceed to ONE network-return test only if >=70% of the 118 additions (83) and >=12 of 14 reviews survive all-four-role baseline gates. Otherwise STOP; no replacement exposure or window. Report all attrition.',
 'window':'ONE fixed 120-calendar-day window: AD-120 through AD-1 and ED+1 through ED+120. Exclude announcement-to-effective transition entirely. Minimum 75 common observed return days in each window, same assets/weights both windows. No alternative window search.',
 'overlap':'Symmetric metadata-only rule: exclude an entire matched event if any of its four issuers has another OMXSB announcement-to-effective interval intersecting either observation window; exclude peer issuers if they have such an interval in either window OR are a changed constituent in the focal review. Use exact ISIN and observed RIC-to-issuer chains. Events unidentifiable to peer issuers remain a limitation. Prior roster and current review pool are identity information, not claims of real-time trading availability.',
 'returns_if_gate_passes':'Daily total-return-index percentage change from the frozen local LSEG panel. For stock and each frozen weighted portfolio, compute residuals separately within each window by OLS on intercept and broad OMXSGI market return. Simple residual Pearson correlations. Primary per-role value=(rho_family_post-rho_family_pre)-(rho_other_post-rho_other_pre). Event contrast is role event minus arithmetic mean of the same three controls. This removes a linear market component but not changing industry/style/fundamental exposure. Same-industry peers already excluded; no extra model search.',
 'missing_returns':'Never substitute close-only or carry forward missing returns. Require both consecutive total-return observations. Fixed peers need >=95% frozen weight observed on every included day; observed weights are renormalized only within this small missing fraction and their minimum coverage is reported. The same 75-day minimum is imposed in both windows; all four roles required. Return-availability selection reported separately.',
 'inference':'Equal-weight events within review and equal-weight the 14 or retained reviews. Primary nominal t interval across review means, df=G-1. Report exact studentized sign-flip as an assumption-dependent description only, not randomization inference. Review dependence, repeated issuers, overlapping peers and nonrandom index selection prevent causal and many-independent-pair claims. Also show each review and leave-one-review-out point range without choosing a preferred estimate.',
 'interpretation':'Association in pre-existing owner network only; cannot identify risk effect caused by inclusion, new-owner channel, or price impact mechanism. Nominal CI is exploratory. Do not assert absence of economic effect from an imprecise null.',
 'publication_times':'FI latest archived reports can be revised after the event: historical quarter is the holdings reference date, not proof investors knew the data then. Report late archive filenames; this is retrospective measurement, never an implementable ex ante signal.',
}
lock=O/'DESIGN_LOCK.json'
if lock.exists():
 old=json.loads(lock.read_text());assert {k:v for k,v in old.items() if k!='recorded_utc'}=={k:v for k,v in DESIGN.items() if k!='recorded_utc'},'Design changed: write a dated amendment instead of replacing lock.'
else:lock.write_text(json.dumps(DESIGN,indent=2,ensure_ascii=False))
hashes={k:{'path':str(p),'sha256':sha(p)}for k,p in P.items()}
(O/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2))

M=pd.read_csv(P['metadata'],dtype={'fund_id':str})
S=pd.read_csv(P['roles']);C=pd.read_csv(P['existing_coverage'],usecols=['event_id','type','eligible'])
E=pd.read_csv(P['matches'],usecols=['event_id','review','type','AD','ED','ric','c1_ric','c2_ric','c3_ric'])
E=E[E.event_id.isin(C.loc[C.eligible & C.type.eq('addition'),'event_id'])].copy()
assert len(E)==118 and E.review.nunique()==14
S=S[S.event_id.isin(E.event_id)].copy()
U=pd.read_csv(P['pool']);RO=pd.read_csv(P['roster'])
A=pd.read_csv(P['events'],usecols=['event_id','announcement_date','effective_date','isin','RIC','review_cycle'])
A['AD']=pd.to_datetime(A.announcement_date);A['ED']=pd.to_datetime(A.effective_date)
for c in ['AD','ED']:E[c]=pd.to_datetime(E[c])
RO['ordinary']=RO.stock_type & RO.listed_at_month_end & ~RO.preference_name_flag & ~(RO.instrument.fillna('')+' '+RO.ticker.fillna('')).str.contains(r'\b(?:PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)\b',case=False,regex=True)
qs=set(S.q0);col={'Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','ISIN-kod_instrument':'isin','Antal':'qty','Marknadsvärde_instrument':'mv','Tillgångsslag_enligt_LVF_5_kap':'asset_type'}
parts=[]
for z in pd.read_csv(P['fi'],usecols=list(col),dtype={'Fond_institutnummer':str},chunksize=200000):
 z=z.rename(columns=col);z=z[z.quarter.isin(qs)&z.asset_type.eq('ÖverlåtbartVärdepapper')];parts.append(z)
H=pd.concat(parts,ignore_index=True)
H.to_csv(O/'baseline_transferable_rows.csv.gz',index=False,compression='gzip')
role_records=[];peer_records=[];fund_records=[];event_records=[];review_records=[];excluded=[]
for rev,ee in E.groupby('review'):
 y=int(rev[:4]);h=int(rev[-1]);q=f'{y}-03-31' if h==1 else f'{y}-09-30';prior=(y-1)*100+10 if h==1 else y*100+4
 rr=RO[RO.month.eq(prior)&RO.ordinary].copy();rr=rr[~rr.duplicated('isin',keep=False)]
 rr=rr[rr.industry.notna()&rr.company_code.notna()].set_index('isin')
 current=U[U.review.eq(rev)].copy();curunique=current[current.same_instrument_RIC_count.eq(1)].copy()
 peer=curunique.merge(rr[['company_code','industry']],left_on='isin',right_index=True,suffixes=('_current','_prior'))
 peer=peer[peer.company_code_current.eq(peer.company_code_prior)].copy().rename(columns={'company_code_current':'company_code'})
 peer=peer.drop_duplicates('isin').set_index('isin')
 m=M[M.quarter.eq(q)].copy();m=m[m.n_instr.gt(0)]
 badlegal=set(m.loc[m.fund_isin.notna()&m.duplicated('fund_isin',keep=False),'fund_id'])
 b=m.label.fillna('');simple=~b.str.contains(r';|\||msci|omrx|solactive|bloomberg|\bex\b|procent|carnegie|hfrx|[0-9]+\s*%',regex=True)
 family=b.str.contains(r'stockholm benchmark|omxsb|\bsbx',regex=True)&simple
 other=m.broad & m.simple
 m['network_group']=np.where(family,'family',np.where(other,'other','excluded'))
 m=m[m.network_group.ne('excluded')&m.fund_isin.notna()&~m.fund_id.isin(badlegal)].copy()
 m['manager']=m.company.fillna('').map(lambda z:re.sub(r'\s+',' ',z.strip().lower()))
 m=m[m.manager.ne('')].set_index('fund_id')
 z=H[H.quarter.eq(q)&H.fund_id.isin(m.index)].copy()
 z['invalid']=z.duplicated(['fund_id','isin'],keep=False)|~np.isfinite(z.qty)|~np.isfinite(z.mv)|z.qty.lt(0)|z.mv.lt(0)
 # Exact known issuer map may span renamed RICs; no fuzzy issuer or ticker inference.
 rel=U[['ric','company_code','isin']].drop_duplicates()
 issuerlinks={k:set(v.company_code)for k,v in rel.groupby('ric')}
 allreviewroles=S[S.review.eq(rev)]
 review_records.append(dict(review=rev,q0=q,prior_roster_month=prior,ordinary_prior_isins=len(rr),exact_peer_candidates=len(peer),family_funds=int(m.network_group.eq('family').sum()),other_funds=int(m.network_group.eq('other').sum()),duplicate_legal_ids=len(badlegal)))
 for e in ee.itertuples():
  pre0=e.AD-pd.Timedelta(days=120);pre1=e.AD-pd.Timedelta(days=1);post0=e.ED+pd.Timedelta(days=1);post1=e.ED+pd.Timedelta(days=120)
  overlap=((A.AD.le(pre1)&A.ED.ge(pre0))|(A.AD.le(post1)&A.ED.ge(post0)))&A.event_id.ne(e.event_id)
  peerchange=overlap|A.review_cycle.eq(rev)
  def changed(mask):
   aa=A[mask];isins=set(aa['isin'].dropna());companies=set()
   for ric in aa.RIC.dropna():companies.update(issuerlinks.get(ric,set()))
   companies.update(rr.loc[rr.index.isin(isins),'company_code'])
   return isins,companies
  overlap_isin,overlap_company=changed(overlap);changed_isin,changed_company=changed(peerchange)
  ss=allreviewroles[allreviewroles.event_id.eq(e.event_id)]
  alias_universe=set(';'.join(ss.aliases).split(';'))
  relevant=set(rr.index)|alias_universe
  badfund=set(z.loc[z.invalid&z['isin'].isin(relevant),'fund_id'])
  good=z[~z.fund_id.isin(badfund)&z.qty.gt(0)&z.mv.gt(0)&~z.invalid].copy()
  excluded.extend(dict(event_id=e.event_id,fund_id=f,reason='ambiguous_or_invalid_baseline_ordinary_position')for f in sorted(badfund))
  event_overlap=any(x.company_code in overlap_company or bool(set(x.aliases.split(';'))&overlap_isin)for x in ss.itertuples())
  er=dict(event_id=e.event_id,review=rev,AD=str(e.AD.date()),ED=str(e.ED.date()),pre_start=str(pre0.date()),pre_end=str(pre1.date()),post_start=str(post0.date()),post_end=str(post1.date()),overlap_exclusion=event_overlap)
  rolepass=[]
  for s in ss.itertuples():
   reasons=[];aliases=s.aliases.split(';');priorids=[a for a in aliases if a in rr.index]
   baselineid=priorids[0]if len(priorids)==1 else None
   industry=rr.loc[baselineid,'industry']if baselineid else None
   if baselineid is None:reasons.append('no_unique_prior_roster_industry_class')
   elif rr.loc[baselineid,'company_code']!=s.company_code:reasons.append('prior_issuer_disagreement')
   owns=good[good['isin'].isin(aliases)].copy();duptarget=set(owns.loc[owns.duplicated('fund_id',keep=False),'fund_id']);owns=owns[~owns.fund_id.isin(duptarget)]
   owns=owns.merge(m[['network_group','manager','label','published_file']],left_on='fund_id',right_index=True,validate='m:1')
   w_bygroup={};gr={}
   for group in ['family','other']:
    og=owns[owns.network_group.eq(group)];alltarget=float(og.mv.sum());accepted=[];fundport=[]
    if industry is not None:
     den_ids=set(rr.index[(rr.industry.ne(industry))&rr.company_code.ne(s.company_code)&~rr.company_code.isin(changed_company)])-changed_isin
     pp=peer[peer.industry.ne(industry)&peer.company_code.ne(s.company_code)&~peer.company_code.isin(changed_company)]
     pp=pp[~pp.index.isin(changed_isin)]
     for f in og.itertuples():
      fh=good[good.fund_id.eq(f.fund_id)];den=float(fh.loc[fh['isin'].isin(den_ids),'mv'].sum())
      use=fh[fh['isin'].isin(pp.index)].set_index('isin').mv
      num=float(use.sum());cov=num/den if den>0 else 0.
      ok=den>0 and cov>=.9
      fund_records.append(dict(event_id=e.event_id,review=rev,role=s.role,ric=s.ric,group=group,fund_id=f.fund_id,manager=f.manager,label=f.label,archive_timestamp=f.published_file,target_mv=f.mv,peer_capital_denominator=den,peer_capital_mapped=num,coverage=cov,accepted=ok))
      if ok:accepted.append(f);fundport.append(use/num)
    kept=sum(f.mv for f in accepted);retain=kept/alltarget if alltarget>0 else 0.
    w=pd.Series(0.,index=peer.index)
    for f,p in zip(accepted,fundport):w=w.add(p*(f.mv/kept),fill_value=0)
    w=w[w.gt(0)];wi=w.groupby(peer.reindex(w.index).company_code).sum()if len(w)else pd.Series(dtype=float)
    eff=1/float((wi**2).sum())if len(wi)else 0.
    gr[group]=dict(funds=len(accepted),managers=len(set(f.manager for f in accepted)),target_capital=alltarget,retained_target_capital_fraction=retain,peers=len(w),issuers=len(wi),effective_issuers=eff)
    w_bygroup[group]=wi
    if alltarget<=0:reasons.append(group+'_no_positive_baseline_owner')
    if retain<.9:reasons.append(group+'_insufficient_target_capital_retained')
    if eff<10:reasons.append(group+'_effective_issuers_below_10')
    for isin,v in w.items():
     p=peer.loc[isin];peer_records.append(dict(event_id=e.event_id,review=rev,role=s.role,target_ric=s.ric,group=group,peer_ric=p.ric,peer_isin=isin,peer_company=p.company_code,peer_industry=p.industry,weight=v))
   joined=pd.concat(w_bygroup,axis=1).fillna(0)
   if len(joined) and (joined**2).sum().gt(0).all():
    tv=float((joined.family-joined.other).abs().sum()/2);cos=float(joined.family.dot(joined.other)/np.sqrt(joined.family.dot(joined.family)*joined.other.dot(joined.other)))
   else:tv=np.nan;cos=np.nan
   if not(np.isfinite(tv)and tv>=.15):reasons.append('portfolio_TV_below_0.15_or_undefined')
   if not(np.isfinite(cos)and cos<=.98):reasons.append('portfolio_cosine_above_0.98_or_undefined')
   rolepass.append(not reasons)
   role_records.append(dict(event_id=e.event_id,review=rev,role=s.role,ric=s.ric,company_code=s.company_code,industry=industry,baseline_isin=baselineid,portfolio_TV=tv,portfolio_cosine=cos,role_pass=not reasons,reasons=';'.join(reasons),**{g+'_'+k:v for g,d in gr.items()for k,v in d.items()}))
  er['four_roles_pass']=all(rolepass);er['baseline_pass']=all(rolepass)and not event_overlap;event_records.append(er)
roles=pd.DataFrame(role_records);events=pd.DataFrame(event_records);peers=pd.DataFrame(peer_records);funds=pd.DataFrame(fund_records)
roles.to_csv(O/'role_baseline_gate.csv',index=False);events.to_csv(O/'event_baseline_gate.csv',index=False);peers.to_csv(O/'frozen_peer_weights.csv.gz',index=False,compression='gzip');funds.to_csv(O/'baseline_fund_portfolio_gate.csv.gz',index=False,compression='gzip');pd.DataFrame(review_records).to_csv(O/'review_baseline_coverage.csv',index=False);pd.DataFrame(excluded).to_csv(O/'fund_exclusions.csv',index=False)
passing=events[events.baseline_pass];reason_counts=roles.reasons.str.split(';').explode();reason_counts=reason_counts[reason_counts.ne('')].value_counts().to_dict()
summary=dict(finished_utc=utc(),design_locked_utc=json.loads(lock.read_text())['recorded_utc'],sample_additions=len(events),sample_roles=len(roles),roles_pass=int(roles.role_pass.sum()),all_four_role_pass=int(events.four_roles_pass.sum()),events_overlap_excluded=int(events.overlap_exclusion.sum()),events_pass=len(passing),reviews_pass=passing.review.nunique(),sample_fraction=len(passing)/118,gate_pass=bool(len(passing)>=83 and passing.review.nunique()>=12),role_reason_counts=reason_counts,returns_read=False,new_return_contrasts_computed=False,portfolio_TV_quantiles=roles.portfolio_TV.quantile([0,.25,.5,.75,1]).to_dict(),portfolio_cosine_quantiles=roles.portfolio_cosine.quantile([0,.25,.5,.75,1]).to_dict(),input_hashes=hashes)
(O/'BASELINE_GATE.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in summary.items()if k!='input_hashes'},indent=2))
