import os
from pathlib import Path
import re,json,hashlib,os
import numpy as np,pandas as pd
R=Path(os.environ.get('FINANCETHESIS_REPO', str(Path(__file__).resolve().parents[3])));B=R/'output/omxsb_open_questions_20261102';O=Path(__file__).resolve().parent
M=pd.read_csv(B/'independent/inputs/latest_metadata_classification.csv',dtype={'fund_id':str,'fund_isin':str});M['quarter']=pd.to_datetime(M.quarter)
assert not M.duplicated(['quarter','fund_id']).any()
cols=['Tillgångsslag_enligt_LVF_5_kap','Instrumentnamn','ISIN-kod_instrument','Antal','Marknadsvärde_instrument','Kvartalsslut','Fond_institutnummer','Fond_namn','Fondförmögenhet']
H=pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=cols,dtype={'Fond_institutnummer':str})
H=H.rename(columns={'Tillgångsslag_enligt_LVF_5_kap':'asset_type','Instrumentnamn':'name','ISIN-kod_instrument':'isin','Antal':'qty','Marknadsvärde_instrument':'value','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id'})
H['quarter']=pd.to_datetime(H.quarter)
for c in ['qty','value']:H[c]=pd.to_numeric(H[c],errors='coerce')
H['ordinary_container']=H.asset_type.eq('ÖverlåtbartVärdepapper')
H['valid_positive']=H.ordinary_container&H.qty.gt(0)&H.value.gt(0)&np.isfinite(H.qty)&np.isfinite(H.value)
ROSTER=pd.read_csv(B/'eligibility/dated_stockholm_instrument_roster.csv')
ORDINARY=set(ROSTER.loc[ROSTER.stock_type & ~ROSTER.preference_name_flag,'isin'])
SE=H[H.valid_positive&H['isin'].fillna('').str.startswith('SE')&H['isin'].isin(ORDINARY)].groupby(['quarter','fund_id']).isin.nunique()
M['nse']=[int(SE.get((q,f),0))for q,f in zip(M.quarter,M.fund_id)]
def norm(s):return re.sub(r'\s+',' ',str(s).strip().lower())
M['label']=M.benchmark.map(norm)
pat=r'six ?(?:portfolio|prx|return|rx)|sixrx|sixprx|omxs ?gi|omxspi|all.?share'
M['broad']=M.label.str.contains(pat,regex=True)&~M.label.str.contains(r'stockholm benchmark|omxsb|\bsbx')
M['simple']=~M.label.str.contains(r';|\||msci|omrx|solactive|bloomberg|\bex\b|procent|carnegie|hfrx|[0-9]+\s*%',regex=True)
M['not_index_named']=~M.fund_name.fillna('').str.contains(r'index|indexnära|exponering|etf|xact|passiv|access',case=False,regex=True)
M['valid_H_pre']=M.broad&M.simple&M.not_index_named&M.nse.ge(10)&M.n_instr.gt(0)
M.to_csv(O/'fund_metadata_classification.csv',index=False)
E=pd.read_csv(B/'eligible_rematch/event_paths.csv',usecols=['event_id','ric','review','type','AD','ED','issuer','c1_ric','c2_ric','c3_ric']);E=E[E.review.str[:4].astype(int).between(2019,2025)].copy()
U=pd.read_csv(B/'eligible_pool/review_RIC_control_pool.csv');ud=U.set_index(['review','ric']).to_dict('index')
AA=json.load(open(R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json'))
# An externally inspected alias chain is used only for matching share class, never a name guess.
G=[];S=[];J=[]
exists=set(zip(H.loc[H.valid_positive,'quarter'],H.loc[H.valid_positive,'isin']))
for rev,ee in E.groupby('review'):
 year=int(rev[:4]);q0=pd.Timestamp(f'{year}-03-31' if rev.endswith('H1')else f'{year}-09-30');q1=q0+pd.offsets.QuarterEnd(1);qm=q0-pd.offsets.QuarterEnd(1)
 pre=M[(M.quarter==q0)&M.valid_H_pre];post=M[M.quarter==q1].set_index('fund_id');prev=M[M.quarter==qm].set_index('fund_id')
 for x in pre.itertuples():
  y=post.loc[x.fund_id]if x.fund_id in post.index else None;z=prev.loc[x.fund_id]if x.fund_id in prev.index else None
  ok=bool(y is not None and y.n_instr>0 and y.label==x.label and pd.notna(x.fund_isin) and x.fund_isin==y.fund_isin)
  prior=bool(ok and z is not None and z.n_instr>0 and z.label==x.label and x.fund_isin==z.fund_isin)
  G.append(dict(review=rev,fund_id=x.fund_id,fund_name=x.fund_name,company=x.company,qminus=str(qm.date()),q0=str(q0.date()),q1=str(q1.date()),label=x.label,nse=x.nse,eligible=ok,eligible_pretrend=prior))
 for x in ee.itertuples():
  for role,ric in [('event',x.ric),('c1',x.c1_ric),('c2',x.c2_ric),('c3',x.c3_ric)]:
   a=ud[(rev,ric)];aliases=sorted(set([a['nasdaq_isin']]+AA.get(ric,[])))
   ev0=[s for s in aliases if (q0,s)in exists];evm=[s for s in aliases if(qm,s)in exists];ev1=[s for s in aliases if(q1,s)in exists]
   S.append(dict(event_id=x.event_id,review=rev,type=x.type,role=role,ric=ric,company_code=a['company_code'],instrument=a['instrument'],nasdaq_isin=a['nasdaq_isin'],aliases=';'.join(aliases),qminus=str(qm.date()),q0=str(q0.date()),q1=str(q1.date()),q0_supported=bool(ev0),qminus_supported=bool(evm),q1_supported=bool(ev1),q0_isins=';'.join(ev0),q1_isins=';'.join(ev1),source_url=a['source_url']))
G=pd.DataFrame(G);S=pd.DataFrame(S);G.to_csv(O/'H_fund_review_gate.csv',index=False);S.to_csv(O/'security_role_gate.csv',index=False)
ids=set(S.aliases.str.split(';').explode());qfund=set((pd.Timestamp(row.q0),row.fund_id)for row in G[G.eligible].itertuples())|set((pd.Timestamp(row.q1),row.fund_id)for row in G[G.eligible].itertuples())|set((pd.Timestamp(row.qminus),row.fund_id)for row in G[G.eligible_pretrend].itertuples())
Q=H.loc[[(q,f)in qfund for q,f in zip(H.quarter,H.fund_id)]].copy();Q.to_csv(O/'selected_full_fund_reports.csv.gz',index=False,compression='gzip')
Q[Q['isin'].isin(ids)].to_csv(O/'target_security_raw_rows.csv.gz',index=False,compression='gzip')
# Unknown same-issuer candidate screen: compare distinctive company tokens; known other listed classes and named rights are classified explicitly below.
roster=pd.read_csv(B/'eligibility/dated_stockholm_instrument_roster.csv');print('rostercolumns',roster.columns.tolist())
summary={'fund_review_candidates':len(G),'eligible_fund_review_rows':int(G.eligible.sum()),'eligible_unique_funds':int(G[G.eligible].fund_id.nunique()),'reviews':G.review.nunique(),'matched_events':S.event_id.nunique(),'supported_all4_before':int(S.groupby('event_id').q0_supported.all().sum()),'supported_all4_both':int(S.groupby('event_id')[['q0_supported','q1_supported']].all().all(axis=1).sum()),'target_isins':len(ids),'selected_full_rows':len(Q),'H_labels':G[G.eligible].label.value_counts().to_dict()}
(O/'gate_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(G[G.eligible].groupby(['fund_id','fund_name','company']).size().to_string());print('UNSUPPORTED',S[~S.q0_supported][['event_id','role','ric','nasdaq_isin']].to_string(index=False))
inputs=[Path(__file__),O/'ANALYSIS_DECISIONS.txt',B/'eligible_rematch/event_paths.csv',B/'eligible_pool/review_RIC_control_pool.csv',B/'independent/inputs/latest_metadata_classification.csv',R/'data/derived/fi/fi_holdings_long.csv.gz',R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json']
(O/'input_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2))
