"""Read-only XLSX event-history reconciliation; publish aggregates/row references only."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json,re
from openpyxl import load_workbook
import pandas as pd

O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis')
X=Path('/Users/ludviguvang/Downloads/OMXSBGI_index leavers & joiners_03-Nov-2026.xlsx')
C=R/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv'
CAL=R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv'
K=R/'output/omxsb_execution_followup_20261102/sources/known_cancellations.csv'
IP=O.parents[1]/'alternative_execution_20261103/index_sources'
BEFORE=IP/'private/repaired_index_pilot_20231130_field3.csv'
AFTER=IP/'private/repaired_index_pilot_20231201_field3.csv'
RELEASE=IP/'sources/release_2023H2.html'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ric(s):return re.sub(r'\s*\(expired\)\s*$','',str(s).strip(),flags=re.I).strip()
initial_hash=sha(X)
w=load_workbook(X,read_only=True,data_only=True);assert w.sheetnames==['L&J'];s=w['L&J']
assert [c.value for c in s[4]]==['Status','Issuer','Code','Date']
records=[]
for row,vals in enumerate(s.iter_rows(min_row=5,max_row=705,values_only=True),5):
 status,issuer,code,date=vals
 assert status in ['Joiner','Leaver'] and isinstance(date,datetime) and code
 records.append({'row':row,'RIC':ric(code),'type':{'Joiner':'addition','Leaver':'deletion'}[status],'date':date.strftime('%Y-%m-%d'),'issuer':issuer})
caption=s['A3'].value;w.close();W=pd.DataFrame(records)
wf=load_workbook(X,read_only=True,data_only=False);formula_count=sum(c.data_type=='f' for rr in wf['L&J'].iter_rows() for c in rr);wf.close()
E=pd.read_csv(C,usecols=['event_id','effective_date','announcement_date','company','type','review_cycle','RIC'],dtype=str).fillna('');E['RIC']=E.RIC.map(lambda v:ric(v) if v else '')
cal=pd.read_csv(CAL,usecols=['ric','date'],dtype=str);days=sorted(cal.loc[cal.ric.eq('.OMXSBGI'),'date'].unique());pos={d:i for i,d in enumerate(days)}
keys={k:g.row.tolist() for k,g in W.groupby(['RIC','type','date'])}
out=[]
for e in E.itertuples():
 previous=days[pos[e.effective_date]-1] if e.effective_date in pos and pos[e.effective_date]>0 else ''
 exact=keys.get((e.RIC,e.type,e.effective_date),[]) if e.RIC else []
 prev=keys.get((e.RIC,e.type,previous),[]) if e.RIC else []
 ann=keys.get((e.RIC,e.type,e.announcement_date),[]) if e.RIC else []
 near=W.loc[W.RIC.eq(e.RIC)&W.type.eq(e.type)] if e.RIC else W.iloc[:0]
 near=near.loc[(pd.to_datetime(near.date)-pd.Timestamp(e.effective_date)).abs().dt.days.le(10)]
 out.append({'event_id':e.event_id,'review':e.review_cycle,'repo_RIC':e.RIC,'repo_type':e.type,'repo_ED':e.effective_date,
   'exact_ED_match':bool(exact),'workbook_exact_row_refs':';'.join(f'L&J!A{n}:D{n}' for n in exact),
   'previous_session_match':bool(prev),'announcement_date_match':bool(ann),
   'nearby_same_RIC_type_row_refs':';'.join(f'L&J!A{n}:D{n}' for n in near.row),
   'status':'exact' if exact else 'repo_RIC_missing' if not e.RIC else 'no_exact_vendor_row'})
D=pd.DataFrame(out)
D.loc[~D.exact_ED_match].to_csv(O/'REPO_MISMATCH_REFERENCES.csv',index=False)
review=D.groupby('review').agg(repo_events=('event_id','size'),mapped_repo_RIC=('repo_RIC',lambda x:int(x.ne('').sum())),exact_ED_matches=('exact_ED_match','sum'),previous_close_matches=('previous_session_match','sum'),announcement_date_matches=('announcement_date_match','sum'),ED=('repo_ED','first')).reset_index()
review['workbook_rows_on_ED']=[int(W.date.eq(d).sum()) for d in review.ED]
review.to_csv(O/'REVIEW_RECONCILIATION_COUNTS.csv',index=False)
known_dates=set(E.effective_date);exact_event_keys=set(zip(E.RIC,E.type,E.effective_date))
W['review_date']=W.date.isin(known_dates)
W['exact_repo_event']=[k in exact_event_keys for k in zip(W.RIC,W.type,W.date)]
W['period']=W.date.str[:4]
W.groupby('period').agg(rows=('row','size'),additions=('type',lambda x:int(x.eq('addition').sum())),deletions=('type',lambda x:int(x.eq('deletion').sum())),on_repo_review_date=('review_date','sum'),exact_repo_event=('exact_repo_event','sum')).to_csv(O/'WORKBOOK_YEAR_COUNTS.csv')
pre=W[W.date.lt('2007-01-01')].copy();pre['date']=pd.to_datetime(pre.date)
pre['initial_basket_candidate']=pre.date.eq(pd.Timestamp('2002-08-12'))
pre['Jan_July_review_candidate']=(pre.date.dt.year.between(2003,2006)&pre.date.dt.month.isin([1,7])&pre.date.dt.day.le(7))
pre.groupby('date').agg(rows=('row','size'),additions=('type',lambda x:int(x.eq('addition').sum())),deletions=('type',lambda x:int(x.eq('deletion').sum())),initial_basket_candidate=('initial_basket_candidate','first'),Jan_July_review_candidate=('Jan_July_review_candidate','first')).to_csv(O/'PRE2007_DATE_CLUSTER_COUNTS.csv')
vendor_refs=W.loc[~W.exact_repo_event,['row','review_date']].copy();vendor_refs['source_reference']=vendor_refs.row.map(lambda n:f'L&J!A{n}:D{n}');vendor_refs['classification']=vendor_refs.review_date.map({True:'on_known_review_date_but_no_exact_repo_key',False:'outside_repo_scheduled_review_dates_or_pre2007'})
vendor_refs[['source_reference','classification']].to_csv(O/'VENDOR_UNMATCHED_ROW_REFERENCES.csv',index=False)
k=pd.read_csv(K,usecols=['known_cancel_id','review','RIC','type','scheduled_ED','cancellation_date'])
canc=[]
for z in k.itertuples():
 rows=keys.get((z.RIC,z.type,z.scheduled_ED),[])
 canc.append({'known_cancel_id':z.known_cancel_id,'review':z.review,'originally_announced_type':z.type,'scheduled_ED':z.scheduled_ED,'cancelled_date':z.cancellation_date,'vendor_row_count_on_scheduled_ED':len(rows),'source_row_refs':';'.join(f'L&J!A{i}:D{i}' for i in rows)})
pd.DataFrame(canc).to_csv(O/'KNOWN_CANCELLATION_SCREEN.csv',index=False)
b=set(pd.read_csv(BEFORE,usecols=['Constituent RIC'])['Constituent RIC'].dropna().astype(str));a=set(pd.read_csv(AFTER,usecols=['Constituent RIC'])['Constituent RIC'].dropna().astype(str))
beij={'RIC':'BEIJb.ST','repo_event_id':'OMXSB-2023H2-12','repo_direction':'deletion','repo_ED':'2023-12-01',
 'workbook_2023H2_source_range':'L&J!A65:D76','workbook_2023H2_rows':int(W.date.eq('2023-12-01').sum()),
 'workbook_BEIJ_2023H2_rows':len(keys.get(('BEIJb.ST','deletion','2023-12-01'),[])),
 'before_API_members':len(b),'after_API_members':len(a),'BEIJ_present_before':('BEIJb.ST'in b),'BEIJ_present_after':('BEIJb.ST'in a),
 'API_addition_count':len(a-b),'API_deletion_count':len(b-a),
 'API_matches_final_repo_additions':a-b==set(E.loc[E.review_cycle.eq('2023H2')&E.type.eq('addition'),'RIC']),
 'API_matches_final_repo_deletions':b-a==set(E.loc[E.review_cycle.eq('2023H2')&E.type.eq('deletion'),'RIC']),
 'cached_Nasdaq_release_contains_BEIJ_B':'Beijer Ref AB ser. B (BEIJ B)' in RELEASE.read_text(),
 'conclusion':'Workbook L&J history omits a deletion present in both the final scheduled census and separately retrieved historical constituent sets. Not repaired by ED-vs-previous-close convention.',
 'source_hashes':{str(p):sha(p) for p in [BEFORE,AFTER,RELEASE]}}
(O/'BEIJER_2023_SOURCE_CONTRADICTION.json').write_text(json.dumps(beij,indent=2)+'\n')
post=W[W.date.ge('2007-01-01')]
result={'created_utc':datetime.now(timezone.utc).isoformat(),'readonly':True,'no_economic_outcomes':True,'workbook_unchanged':sha(X)==initial_hash,
 'workbook_path':str(X),'workbook_sha256':initial_hash,'sheet':'L&J','source_range':'A5:D705','caption':caption,'formula_cells':formula_count,
 'records':len(W),'first_actual_record_date':W.date.min(),'last_actual_record_date':W.date.max(),'workbook_status_counts':W.type.value_counts().to_dict(),
 'duplicate_RIC_type_date_extra_rows':int(W.duplicated(['RIC','type','date']).sum()),
 'repo_records':len(E),'repo_reviews':E.review_cycle.nunique(),'repo_mapped_RIC':int(E.RIC.ne('').sum()),
 'exact_ED_matches':int(D.exact_ED_match.sum()),'previous_session_matches':int(D.previous_session_match.sum()),'announcement_date_matches':int(D.announcement_date_match.sum()),
 'reviews_with_no_vendor_rows_on_ED':review.loc[review.workbook_rows_on_ED.eq(0),'review'].tolist(),
 'pre2007_records':len(pre),'initial2002basket_candidates':int(pre.initial_basket_candidate.sum()),'2003_2006_JanJuly_candidate_records':int(pre.Jan_July_review_candidate.sum()),'2003_2006_JanJuly_candidate_dates':int(pre.loc[pre.Jan_July_review_candidate,'date'].nunique()),'other_pre2007_records':int((~pre.initial_basket_candidate&~pre.Jan_July_review_candidate).sum()),
 'post2007_records':len(post),'post2007_outside_repo_review_date_records':int((~post.review_date).sum()),'post2007_outside_repo_review_dates':int(post.loc[~post.review_date,'date'].nunique()),
 'known_cancels_present_on_scheduled_ED':sum(z['vendor_row_count_on_scheduled_ED'] for z in canc),
 'inputs':{str(p):sha(p) for p in [X,C,CAL,K,BEFORE,AFTER,RELEASE]},'script_sha256':sha(Path(__file__)),'spec_sha256':sha(O/'AUDIT_SPEC.txt'),
 'restrictions':['No full workbook history exported','RIC expired annotation stripped; expiry suffix retained','Pre2007clusters not certified announcements','Off-review does not automatically mean corporate action','New history does not supply prices or earlier auction fields']}
(O/'WORKBOOK_AUDIT_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['inputs','restrictions','caption']},indent=2))
