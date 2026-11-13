"""Source-reference diagnostics for exact mismatches, never automatic identity repair."""
from pathlib import Path
from openpyxl import load_workbook
import pandas as pd,re,json
O=Path(__file__).resolve().parent
X=Path('/Users/ludviguvang/Downloads/OMXSBGI_index leavers & joiners_03-Nov-2026.xlsx')
w=load_workbook(X,read_only=True,data_only=True);rows=[]
for n,(status,name,code,date) in enumerate(w['L&J'].iter_rows(min_row=5,max_row=705,values_only=True),5):
 c=re.sub(r'\s*\(expired\)\s*$','',code.strip(),flags=re.I).strip()
 rows.append({'row':n,'ric':c,'base':c.split('^')[0],'type':'addition' if status=='Joiner' else 'deletion','date':date.strftime('%Y-%m-%d')})
w.close();W=pd.DataFrame(rows)
E=pd.read_csv(O/'REPO_MISMATCH_REFERENCES.csv').fillna('');out=[]
for e in E.itertuples():
 if not e.repo_RIC:label='repo_RIC_missing';z=W.iloc[:0]
 else:
  exact_security=W[W.ric.eq(e.repo_RIC)&W.type.eq(e.repo_type)]
  near=exact_security[(pd.to_datetime(exact_security.date)-pd.Timestamp(e.repo_ED)).abs().dt.days.le(10)]
  suffix=W[W.base.eq(e.repo_RIC.split('^')[0])&W.type.eq(e.repo_type)&W.date.eq(e.repo_ED)]
  if len(near):label='same_exact_RIC_type_within10calendar_days';z=near
  elif len(suffix):label='same_base_RIC_type_ED_different_expiry_suffix';z=suffix
  else:label='no_simple_date_or_expiry_suffix_match';z=W.iloc[:0]
 out.append({'event_id':e.event_id,'review':e.review,'diagnostic':label,'workbook_candidate_row_refs':';'.join(f'L&J!A{n}:D{n}' for n in z.row),'candidate_calendar_day_offsets':';'.join(str((pd.Timestamp(d)-pd.Timestamp(e.repo_ED)).days) for d in z.date),'automatic_repair':False})
D=pd.DataFrame(out);D.to_csv(O/'MISMATCH_DIAGNOSTICS.csv',index=False)
D.groupby(['review','diagnostic']).size().rename('events').to_csv(O/'MISMATCH_DIAGNOSTIC_COUNTS.csv')
summary={'exact_mismatch_rows':len(D),'diagnostic_counts':D.diagnostic.value_counts().to_dict(),'none_of_these_candidates_is_auto_accepted':True,
 'shifted_date_clusters':[{'review':'2008H1','repo_ED':'2008-01-02','vendor_date':'2008-01-03','vendor_rows':int(W.date.eq('2008-01-03').sum())},{'review':'2009JAN','repo_ED':'2009-01-02','vendor_date':'2009-01-05','vendor_rows':int(W.date.eq('2009-01-05').sum())},{'review':'2011H2','repo_ED':'2011-12-01','vendor_date':'2011-12-02','vendor_rows':int(W.date.eq('2011-12-02').sum())}],
 '2008_primary_notice_confirms_repo_ED':'Nasdaq Stockholm AB notice287/07 published2007-12-14 states effectiveness2008-01-02; https://www.globenewswire.com/news-release/2007/12/14/118048/0/sv/avista-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-287-07.html',
 'other_two_shifted_dates':'Repo carries VERIFIED primary-source references; fresh access failed in this bounded audit, so no new independent date certification here.'}
(O/'MISMATCH_DIAGNOSTIC_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary['diagnostic_counts'],indent=2))
