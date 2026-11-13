from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime
R=Path('/Users/ludviguvang/dev/financethesis');O=Path(__file__).resolve().parent;W=R/'output/omxsb_mechanism_frontier_20261102/ownership'
# Explicit usecols prohibit loading new post-event economic outcomes.
F=pd.read_csv(W/'decomp_fund_roles.csv.gz',usecols=['event_id','review','type','role','fund_id','group','own_before'],dtype={'fund_id':str});F=F[F.role.eq('event')].drop(columns='role')
G=pd.read_csv(W/'decomp_fund_groups.csv',dtype={'fund_id':str});M=pd.read_csv(W/'fund_metadata_classification.csv',dtype={'fund_id':str},usecols=['fund_id','quarter','fund_name','company','fund_isin','nse','n_instr','benchmark']);REPORT=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/raw_fund_report_metadata.csv',dtype={'Fond_institutnummer':str},usecols=['Fond_institutnummer','Kvartalsslut','actual_instrument_rows'])
A=G.merge(M[['fund_id','quarter','fund_isin','nse','n_instr']],left_on=['fund_id','q0'],right_on=['fund_id','quarter'],validate='m:1').drop(columns='quarter')
for lab in ['q0','q1']:
 mm=REPORT.rename(columns={'Fond_institutnummer':'fund_id','Kvartalsslut':lab,'actual_instrument_rows':lab+'_actual_rows'});A=A.merge(mm,on=['fund_id',lab],how='left',validate='m:1')
A['full_both_reports']=A.q0_actual_rows.gt(0)&A.q1_actual_rows.gt(0);A['B_screen']=A.group.str.startswith('OMXSB_');A['H_screen']=A.group.eq('broad_H');A['pre_direct_Swedish_stock_support']=A.nse.ge(10)
A['style_not_active_certified']=True
# Evidence in at least one period; continuity across 2019-25 is NOT certified.
index_near={51482,60330,60320,60967,60029,60909}
A['ID_with_indexnear_evidence_in_some_period']=A.fund_id.astype(int).isin(index_near)
A.to_csv(O/'fund_review_metadata_baseline.csv',index=False)
D=F.merge(A.drop(columns=['group']),on=['review','fund_id'],validate='m:1');D=D[D.full_both_reports].copy()
D['family_cluster_for_description']=D.company.replace({'SEB Investment Management AB':'SEB','SEB Funds AB':'SEB','SPP Fonder AB':'SPP/Storebrand','Storebrand Fonder AB':'SPP/Storebrand','E. Öhman J:or Fonder AB':'Öhman/Lannebo','Lannebo Kapitalförvaltning AB':'Öhman/Lannebo','Lannebo Fonder AB':'Öhman/Lannebo'})
# One row per company/security/event. Common-company ownership based on all included reporting funds, not just candidates.
rows=[]
for (eid,rev,typ,co),z in D.groupby(['event_id','review','type','company']):
 for screen in ['raw_benchmark_metadata','nonindex_named_with_direct_stock_support','conditional_continuity_screen_NOT_certification']:
  bb=z[z.B_screen];hh=z[z.H_screen]
  if screen!='raw_benchmark_metadata':bb=bb[bb.group.eq('OMXSB_other_named')&bb.pre_direct_Swedish_stock_support];hh=hh[hh.pre_direct_Swedish_stock_support]
  if screen=='conditional_continuity_screen_NOT_certification':bb=bb[~bb.ID_with_indexnear_evidence_in_some_period];hh=hh[~hh.ID_with_indexnear_evidence_in_some_period]
  if len(bb)==0 or len(hh)==0:continue
  rows.append(dict(event_id=eid,review=rev,type=typ,company=co,family_cluster=z.family_cluster_for_description.iloc[0],screen=screen,N_B_funds=len(bb),N_H_funds=len(hh),B_pre_owners=int(bb.own_before.sum()),H_pre_owners=int(hh.own_before.sum()),B_pre_nonowners=int((1-bb.own_before).sum()),H_pre_nonowners=int((1-hh.own_before).sum()),company_pre_owners=int(z.own_before.sum()),company_already_owned=bool(z.own_before.any()),both_groups_have_pre_nonowner=bool((bb.own_before==0).any() and (hh.own_before==0).any()),both_group_nonowners_company_owned=bool(z.own_before.any() and (bb.own_before==0).any() and (hh.own_before==0).any()),B_ids=';'.join(sorted(bb.fund_id.unique())),H_ids=';'.join(sorted(hh.fund_id.unique()))))
E=pd.DataFrame(rows);E.to_csv(O/'baseline_company_event_overlap.csv',index=False)
res=[]
for (screen,typ),z in E.groupby(['screen','type']):
 for rule,mask in [('A_both_metadata_groups',pd.Series(True,index=z.index)),('B_company_already_owned',z.company_already_owned),('C_nonowners_both_groups_company_owned',z.both_group_nonowners_company_owned)]:
  zz=z[mask];res.append(dict(screen=screen,type=typ,rule=rule,company_event_cells=len(zz),events=zz.event_id.nunique(),reviews=zz.review.nunique(),legal_company_names=zz.company.nunique(),descriptive_brand_clusters=zz.family_cluster.nunique(),B_fund_rows=int(zz.N_B_funds.sum()),H_fund_rows=int(zz.N_H_funds.sum()),B_pre_owner_rate=float(zz.B_pre_owners.sum()/zz.N_B_funds.sum()) if len(zz) else None,H_pre_owner_rate=float(zz.H_pre_owners.sum()/zz.N_H_funds.sum()) if len(zz) else None))
S=pd.DataFrame(res);S.to_csv(O/'baseline_overlap_summary.csv',index=False)
C=E.groupby(['screen','type','company','family_cluster']).agg(company_event_cells=('event_id','size'),events=('event_id','nunique'),reviews=('review','nunique'),already_owned_cells=('company_already_owned','sum'),both_nonowners_and_old_company_cells=('both_group_nonowners_company_owned','sum'),B_fund_rows=('N_B_funds','sum'),H_fund_rows=('N_H_funds','sum'),B_pre_owners=('B_pre_owners','sum'),H_pre_owners=('H_pre_owners','sum')).reset_index();C.to_csv(O/'baseline_overlap_by_company.csv',index=False)
# Availability only: row keys, never amounts or own_after.
Q=pd.read_csv(R/'output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz',usecols=['event_id','fund_id'],dtype={'fund_id':str});support=set(map(tuple,Q.to_numpy()));K=D[D.B_screen|D.H_screen][['event_id','review','type','company','fund_id','group']].copy();K['prior_quantity_pair_available']=[(ev,f) in support for ev,f in zip(K.event_id,K.fund_id)];K=K[K.company.isin(E.company.unique())];K.to_csv(O/'quarter_quantity_support_keys.csv',index=False)
# Fund roster for actual shared-company/review pairs only; posterior outcomes prohibited.
pairs=E[['review','company']].drop_duplicates();roster=A.merge(pairs,on=['review','company']);roster=roster[roster.B_screen|roster.H_screen];roster.to_csv(O/'overlap_fund_review_roster.csv',index=False)
meta=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),loaded_post_ownership=False,loaded_post_quantities=False,new_economic_changes_calculated=False,baseline_event_stock_rows=len(D),events=D.event_id.nunique(),reviews=D.review.nunique(),max_candidate_group_certified_active=False,interpretation='Metadata/direct-stock screens are possible support, never proof of active management; the final ID-exclusion screen assumes temporal continuity and is not a certified historical upper bound. All economic amounts/outcomes are unopened.',input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [W/'decomp_fund_roles.csv.gz',W/'decomp_fund_groups.csv',W/'fund_metadata_classification.csv',R/'output/omxsb_open_questions_20261102/demand_quarter/raw_fund_report_metadata.csv',O/'BASELINE_LOCK.txt']})
(O/'BASELINE_RUN.json').write_text(json.dumps(meta,indent=2));print(S.to_string(index=False));print(C[C.type.eq('addition')].to_string(index=False));print(roster[['company','fund_id','name','group','nse']].drop_duplicates().sort_values(['company','fund_id']).to_string(index=False))
