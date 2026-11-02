from pathlib import Path
import pandas as pd,numpy as np,json,re,hashlib
O=Path(__file__).resolve().parent; W=O.parent; R=Path('/Users/ludviguvang/dev/financethesis'); L=R/'data/raw/lseg/panel_2005_2026'
D=pd.read_csv(W/'retention_followup_20261102/position_quantities.csv',usecols=['event_id','review','fund_id','fund','index_q','next_q'],parse_dates=['index_q','next_q'])
T=pd.read_csv(W/'open_questions_20261101/retention/raw_tracker_transferable_securities.csv.gz',parse_dates=['Kvartalsslut'])
M=pd.read_csv(W/'claude_audit_20261101/holdings/corrected/latest_metadata_classification.csv',parse_dates=['quarter'])
RO=pd.read_csv(W/'open_questions_20261101/eligibility/dated_stockholm_instrument_roster.csv'); E=pd.read_csv(R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
AL=json.load(open(R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json'));AL['SFRG.ST']=[s for s in AL.get('SFRG.ST',[]) if s!='SE0017564024']
TU=pd.read_csv(L/'td_universe.csv').fillna(''); ST=pd.read_csv(L/'stocks_static_2005.csv').fillna('')
ids={}
for df,col in [(TU,'RIC'),(ST,'ric')]:
 for x in df.to_dict('records'):
  if len(str(x.get('IssueISIN','')))==12:ids.setdefault(x['IssueISIN'],set()).add(x[col])
for ric,ss in AL.items():
 for i in ss:ids.setdefault(i,set()).add(ric)
stat=ST.set_index('ric'); audit=[]; selected=[];cov=[]
for fr in D.drop_duplicates(['fund_id','review']).itertuples():
 rr=RO[RO.month.eq(int(fr.review[:4]+('04' if fr.review.endswith('H1') else '10')))].copy()
 assert not rr['isin'].duplicated().any()
 rm=rr.set_index('isin'); ex=set()
 for e in E[E.review_cycle.eq(fr.review)].itertuples():
  if pd.notna(e.isin):ex.add(e.isin)
  if pd.notna(e.RIC):ex.update(AL.get(e.RIC,[]))
 companies=set(rr.loc[rr['isin'].isin(ex),'company_code'].dropna())
 tt=T[T.Fond_institutnummer.eq(fr.fund_id)&T.Kvartalsslut.eq(fr.index_q)].copy()
 mm=M[M.fund_id.eq(fr.fund_id)&M.quarter.eq(fr.index_q)];assert len(mm)==1
 aum=mm.aum.iloc[0]
 cand=[]
 for isin,g in tt.groupby('ISIN-kod_instrument',dropna=False):
  q=g.Antal.sum(min_count=1);mv=g.Marknadsvärde_instrument.sum(min_count=1); reason=[];ric='';company='';name='';src=''
  if not np.isfinite(q) or q<=0 or not np.isfinite(mv) or mv<=0:reason.append('not_positive_start_ordinary_position')
  if not g.Valuta.eq('SEK').all():reason.append('non_SEK')
  if isin not in rm.index:reason.append('no_exact_dated_Main_stock_ISIN')
  else:
   r=rm.loc[isin];company=r.company_code;name=r.instrument;src=r.source_url
   if not r.stock_type or not r.listed_at_month_end or r.preference_name_flag or re.search(r'\b(PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)\b',str(r.instrument)+' '+str(r.ticker),re.I):reason.append('nonordinary_or_not_listed')
   if isin in ex or company in companies:reason.append('current_review_event_issuer')
  cr=[]
  for c in ids.get(isin,set()):
   if c in stat.index:
    z=stat.loc[c]
    if isinstance(z,pd.DataFrame):continue
    try:
     if pd.Timestamp(z.first_date)<=fr.index_q<=pd.Timestamp(z.last_date):cr.append(c)
    except Exception:pass
  if len(cr)!=1:reason.append('no_unique_date_supported_exact_ISIN_RIC')
  else:ric=cr[0]
  row=dict(review=fr.review,fund_id=fr.fund_id,fund=fr.fund,index_q=fr.index_q,next_q=fr.next_q,isin=isin,ric=ric,company_code=company,security_name=name,FI_name=';'.join(g.Instrumentnamn.dropna().unique()),q0=q,mv0=mv,aum0=aum,source_url=src,baseline_reason=';'.join(reason))
  audit.append(row)
  if not reason:cand.append(row)
 cc=pd.DataFrame(cand)
 if len(cc):
  cc=cc.sort_values(['mv0','isin'],ascending=[False,True]).drop_duplicates('company_code').head(20).copy();cc['rank']=range(1,len(cc)+1);selected.extend(cc.to_dict('records'))
  cv=cc.mv0.sum()/aum
 else:cv=np.nan
 cov.append(dict(review=fr.review,fund_id=fr.fund_id,fund=fr.fund,selected_N=len(cc),selected_start_AUM_share=cv,start_gate_pass=len(cc)==20 and cv>=.25))
pd.DataFrame(audit).to_csv(O/'baseline_candidate_ledger.csv',index=False);pd.DataFrame(selected).to_csv(O/'core_frozen.csv',index=False);pd.DataFrame(cov).to_csv(O/'baseline_coverage.csv',index=False)
(O/'core_freeze_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'ANALYSIS_DECISIONS.txt',O/'core_frozen.csv',O/'baseline_candidate_ledger.csv',Path(__file__)]},indent=2))
print(pd.DataFrame(cov).to_string(index=False));print('NO CORE ENDPOINT RATIOS COMPUTED')
