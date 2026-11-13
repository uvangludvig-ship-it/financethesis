"""Metadata only: complete event census, fixed controls, exact source-request dates."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,unicodedata
import pandas as pd

R=Path('/Users/ludviguvang/dev/financethesis'); O=Path(__file__).resolve().parent
P={
 'events':R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',
 'calendar':R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',
 'dated_roles':R/'output/omxsb_mechanism_frontier_20261102/ownership/security_role_gate.csv',
 'listed_pool':R/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv',
 'controls':R/'output/omxsb_open_questions_20261102/eligible_rematch/selected_controls.csv',
 'older_controls':R/'output/omxsb_robusthet_20261101/T2_matches.csv',
 'control_membership':R/'output/omxsb_mechanism_frontier_20261102/design/fixed_control_membership_diagnostic.csv',
 'cancellations':R/'output/omxsb_execution_followup_20261102/sources/known_cancellations.csv',
 'actions':R/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',
 'omxs30':R/'data/input/omxsb/omxs30_changes_2005_2026.csv',
 'omxs30_membership':R/'output/omxsb_replication_2007/mechanisms/e3_omxsb_events_vs_omxs30_membership.csv',
 'msci_candidates':R/'code/claude_checks/msci/msci_sweden_changes_2007_2026.csv',
 'solactive_candidates':R/'output/omxsb_extension_20261031/migration/results/omxsb_solactive_event_screen.csv'}
READ={}
def read(key,cols):
 READ[key]=cols
 return pd.read_csv(P[key],usecols=cols,dtype=str).fillna('')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def issuer_name(s):
 s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
 s=re.sub(r'\b(AB|PUBL|SER|SERIE|CLASS|A|B|C)\b',' ',s)
 return re.sub(r'[^A-Z0-9]','',s)

E=read('events',['event_id','effective_date','announcement_date','company','ticker','isin','type','review_cycle','source_url','verification','notes','RIC'])
assert E.event_id.is_unique
C=read('calendar',['ric','date']);cal=sorted(C.loc[C.ric.eq('.OMXSBGI'),'date'].unique());pos={d:i for i,d in enumerate(cal)}
G=read('dated_roles',['event_id','role','ric','company_code','nasdaq_isin','source_url'])
G=G.loc[G.role.eq('event')].set_index('event_id');assert G.index.is_unique
U=read('listed_pool',['review','ric','company_code','isin','ticker','instrument','reference_date','source_url'])
assert not U.duplicated(['review','ric']).any();u=U.set_index(['review','ric']).to_dict('index')
S=read('controls',['event_id','review','role','ric','issuer','isin','source_url'])
old=read('older_controls',['event_id','review','c1_ric','c1_issuer','c2_ric','c2_issuer','c3_ric','c3_issuer'])
assert old.event_id.is_unique
for z in old.itertuples():
 if z.event_id not in set(S.event_id):
  for j in [1,2,3]:
   S=pd.concat([S,pd.DataFrame([{'event_id':z.event_id,'review':z.review,'role':f'c{j}','ric':getattr(z,f'c{j}_ric'),'issuer':getattr(z,f'c{j}_issuer'),'isin':'','source_url':''}])],ignore_index=True)
M=read('control_membership',['event_id','role','ric','membership_before','membership_after','continuing_member'])
m=M.set_index(['event_id','role','ric']).to_dict('index')
K=read('cancellations',['known_cancel_id','review','RIC','type','scheduled_ED','cancellation_date','initial_source_url','cancellation_source_url'])
cancel=set(zip(K.review,K.RIC))
A=read('actions',['RIC','action_date','kind','source','date_precision'])
X=read('omxs30',['event_id','effective_date','announcement_date','company','ticker','isin','type','source_url','verification'])
XM=read('omxs30_membership',['event_id','omxs30_member_at_AD']).set_index('event_id')
MS=read('msci_candidates',['review','segment','change','security','announcement_date','effective_date','status','note'])
MS['name_key']=MS.security.map(issuer_name)
SO=read('solactive_candidates',['event_id','solactive_change_candidate','same_share_class_screen','opposed_candidate'])
so=SO.groupby('event_id').agg(lambda v:';'.join(sorted(set(v)))).to_dict('index')
roles=[];events=[];hazards=[]
for z in E.itertuples():
 p=pos.get(z.effective_date)
 d0=cal[p-6] if p is not None and p>=6 else ''
 d1=cal[p-1] if p is not None and p>=1 else ''
 allowed=bool(z.effective_date<'2024-01-01')
 source_range=bool(d0 and d0>='2010-02-08')
 cancelled=(z.review_cycle,z.RIC) in cancel
 info=u.get((z.review_cycle,z.RIC),{})
 g=G.loc[z.event_id].to_dict() if z.event_id in G.index else {}
 dated_isins={v for v in [info.get('isin',''),g.get('nasdaq_isin','')] if len(v)==12}
 isin=next(iter(dated_isins)) if len(dated_isins)==1 else ''
 conflict=len(dated_isins)>1
 candidate_isin=isin or z.isin
 source=info.get('source_url','') or g.get('source_url','')
 quality='dated_listing' if isin and not conflict else ('conflict' if conflict else 'census_ISIN_unverified' if candidate_isin else 'missing')
 cs=S.loc[S.event_id.eq(z.event_id)]
 row={'event_id':z.event_id,'review':z.review_cycle,'type':z.type,'direction':1 if z.type=='addition' else -1,
  'company':z.company,'ticker':z.ticker,'RIC':z.RIC,'ISIN':candidate_isin,
  'identity_quality':quality,'identity_source_url':source,'event_source_url':z.source_url,
  'AD':z.announcement_date,'ED':z.effective_date,'comparison_date':d0,'auction_date':d1,
  'comparison_next_date':cal[p-5] if p is not None and p>=5 else '',
  'next_date':z.effective_date,'comparison_vs_AD':('before' if d0<z.announcement_date else 'same_date' if d0==z.announcement_date else 'after') if d0 and z.announcement_date else 'unknown',
  'allowed_pre2024':allowed,'within_SHoF_possible_date_range':source_range,'known_cancelled':cancelled,
  'mapped_RIC':bool(z.RIC),'calendar_mapped':p is not None,'fixed_control_count':len(cs),
  'existing_primary_pilot_review':z.review_cycle=='2023H2',
  'omxs30_member_at_AD_existing_metadata':XM.loc[z.event_id,'omxs30_member_at_AD'] if z.event_id in XM.index else 'unknown',
  'solactive_candidate_metadata':json.dumps(so.get(z.event_id,{})),
  'event_verification':z.verification,'notes':z.notes}
 events.append(row)
 rr=[{'role':'event','ric':z.RIC,'isin':candidate_isin,'issuer':info.get('company_code','') or g.get('company_code',''),
      'instrument':z.company,'identity_quality':quality,'source_url':source,'control_origin':'event'}]
 for c in cs.itertuples():
  ci=u.get((z.review_cycle,c.ric),{}); mi=m.get((z.event_id,c.role,c.ric),{})
  rr.append({'role':c.role,'ric':c.ric,'isin':ci.get('isin','') or c.isin,'issuer':ci.get('company_code','') or c.issuer,
       'instrument':ci.get('instrument',''),'identity_quality':'dated_listing' if ci or c.isin else 'provisional_old_match',
       'source_url':ci.get('source_url','') or c.source_url,'control_origin':'dated_eligible_rematch' if c.source_url else 'older_T2_provisional',
       'membership_before':mi.get('membership_before','unknown'),'membership_after':mi.get('membership_after','unknown')})
 for r in rr:
  r.update(event_id=z.event_id,review=z.review_cycle,type=z.type,AD=z.announcement_date,ED=z.effective_date,
           comparison_date=d0,auction_date=d1,allowed_pre2024=allowed,within_SHoF_possible_date_range=source_range)
  r['known_cancelled_announcement_same_review']=(z.review_cycle,r['ric']) in cancel
  r['recorded_current_OMXSB_event']=bool(((E.review_cycle==z.review_cycle)&(E.RIC==r['ric'])).any())
  roles.append(r)
  for a in A.loc[A.RIC.eq(r['ric'])].itertuples():
   if d0 and d0[:7]<=a.action_date[:7]<=z.effective_date[:7]:
    hazards.append({'event_id':z.event_id,'role':r['role'],'RIC':r['ric'],'hazard':'corporate_action_in_month_span','candidate':a.kind,'date':a.action_date,'source':a.source,'status':a.date_precision+'; incomplete_register_not_negative_certificate'})
  for x in X.itertuples():
   match=(bool(r['isin']) and x.isin==r['isin']) or (r['role']=='event' and x.ticker==z.ticker)
   if match and x.effective_date and d0 and d0<=x.effective_date<=z.effective_date:
    hazards.append({'event_id':z.event_id,'role':r['role'],'RIC':r['ric'],'hazard':'OMXS30_change_candidate','candidate':x.company+' '+x.type,'date':x.effective_date,'source':x.source_url,'status':x.verification+'; effective_vs_execution_date_requires_check'})
  candidates=MS.loc[MS.name_key.eq(issuer_name(r['instrument']))&MS.change.isin(['addition','deletion'])]
  for x in candidates.itertuples():
   if x.effective_date and d0 and d0<=x.effective_date<=z.effective_date:
    hazards.append({'event_id':z.event_id,'role':r['role'],'RIC':r['ric'],'hazard':'MSCI_name_candidate_unverified','candidate':x.security+' '+x.segment+' '+x.change,'date':x.effective_date,'source':str(P['msci_candidates']),'status':x.status+'; issuer_name_candidate_only_no_automatic_exclusion'})

D=pd.DataFrame(events); F=pd.DataFrame(roles)
D['security_event_count_full_census']=D.groupby('RIC').event_id.transform('size').where(D.RIC.ne(''))
D['same_review_RIC_duplicate']=D.duplicated(['review','RIC'],keep=False)&D.RIC.ne('')
F['security_distinct_reviews']=F.groupby('ric').review.transform('nunique').where(F.ric.ne(''))
F['same_review_role_reuse_count']=F.groupby(['review','ric']).event_id.transform('size').where(F.ric.ne(''))
F['issuer_distinct_reviews']=F.groupby('issuer').review.transform('nunique').where(F.issuer.ne(''))
D.to_csv(O/'EVENT_METADATA_INVENTORY.csv',index=False)
F.to_csv(O/'FIXED_ROLE_METADATA_INVENTORY.csv',index=False)
pd.DataFrame(hazards,columns=['event_id','role','RIC','hazard','candidate','date','source','status']).to_csv(O/'KNOWN_HAZARDS_AND_UNVERIFIED_CANDIDATES.csv',index=False)
K.to_csv(O/'KNOWN_CANCELLED_ANNOUNCEMENTS.csv',index=False)
rev=D.groupby('review',sort=True).agg(events=('event_id','size'),AD=('AD','first'),ED=('ED','first'),comparison_date=('comparison_date','first'),auction_date=('auction_date','first'),within_SHoF_possible_date_range=('within_SHoF_possible_date_range','first'),allowed_pre2024=('allowed_pre2024','first'),dated_event_identities=('identity_quality',lambda s:int(s.eq('dated_listing').sum())),three_control_sets=('fixed_control_count',lambda s:int(s.eq(3).sum())),comparison_vs_AD=('comparison_vs_AD','first')).reset_index()
rev.to_csv(O/'REVIEW_METADATA_COUNTS.csv',index=False)
Q=F.loc[F.allowed_pre2024&F.within_SHoF_possible_date_range&F.ric.ne('')].copy()
requests=[]
for z in Q.to_dict('records'):
 for session,col in [('comparison','comparison_date'),('implementation','auction_date')]:
  requests.append({k:z[k] for k in ['event_id','review','role','ric','isin','identity_quality','control_origin']}|{'session':session,'date':z[col],
    'LSEG_fields':'CLS_AUC;CLS_AUCVOL','LSEG_adjustments':'unadjusted','HFT_source_gate':'minute_or_second_only_after_same_terminal_quote_validation',
    'source_request_only_not_sample_acceptance':True})
Q=pd.DataFrame(requests);Q.to_csv(O/'SOURCE_COVERAGE_REQUESTS_LONG.csv',index=False)
Q.groupby(['ric','date'],sort=True).agg(ISIN_candidates=('isin',lambda s:';'.join(sorted(set(s)-{''}))),event_roles=('event_id','size')).reset_index().to_csv(O/'LSEG_DEDUPLICATED_COVERAGE_REQUESTS.csv',index=False)
out={'created_utc':datetime.now(timezone.utc).isoformat(),'source_only':True,'new_outcomes_computed':False,
 'all_events':len(D),'all_reviews':D.review.nunique(),
 'pre2024_possible_SHoF_events':int((D.allowed_pre2024&D.within_SHoF_possible_date_range&~D.known_cancelled).sum()),
 'pre2024_possible_SHoF_reviews':D.loc[D.allowed_pre2024&D.within_SHoF_possible_date_range&~D.known_cancelled,'review'].nunique(),
 '2020_2023_events':int(D.ED.between('2020-01-01','2023-12-31').sum()),
 '2020_2023_reviews':D.loc[D.ED.between('2020-01-01','2023-12-31'),'review'].nunique(),
 'known_cancelled_census_rows':int(D.known_cancelled.sum()),'known_cancelled_separate_announcements':len(K),
 'unique_ric_date_source_requests':len(Q[['ric','date']].drop_duplicates()),
 'potential_source_dates_not_observed_coverage':True,
 'repeated_RICs_full_census':int(D.loc[D.RIC.ne('')].groupby('RIC').size().gt(1).sum()),
 'same_review_RIC_duplicates':int(D.same_review_RIC_duplicate.sum()),
 'primary_population_dated_identity_counts':D.loc[D.allowed_pre2024&D.within_SHoF_possible_date_range,'identity_quality'].value_counts().to_dict(),
 'new_outcome_columns_read':[], 'read_columns':READ,
 'inputs':{k:{'path':str(p),'sha256':sha(p)} for k,p in P.items()},
 'script_sha256':sha(Path(__file__)),'metadata_spec_sha256':sha(O/'METADATA_INVENTORY_SPEC.txt')}
(O/'INVENTORY_LOCK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['inputs','read_columns']},indent=2))
