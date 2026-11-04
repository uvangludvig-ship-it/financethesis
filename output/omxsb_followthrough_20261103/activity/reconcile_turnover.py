"""Fixed reference-month unit QA only; not event-window activity estimates."""
from pathlib import Path
from datetime import datetime,timezone
import sys,re,json,hashlib
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O/'.deps'))
import pandas as pd,numpy as np
BASE=O.parents[1];R=Path('/Users/ludviguvang/dev/financethesis');PVT=O/'private';PVT.mkdir(exist_ok=True)
S=pd.read_csv(O/'ROLE_SOURCE_PRESENCE.csv');roster=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv')
panel=R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet';P=pd.read_parquet(panel,columns=['ric','date','turnover','source'],filters=[('ric','in',sorted(S.ric.unique()))]);P.date=pd.to_datetime(P.date)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lock={'created_utc':datetime.now(timezone.utc).isoformat(),'stage':'reference_month_source_units_before_event_outcomes','primary_spec_sha256':sha(O/'PRIMARY_SPEC.txt'),'presence_sha256':sha(O/'ROLE_SOURCE_PRESENCE.csv'),'script_sha256':sha(Path(__file__))};(O/'UNIT_RECONCILIATION_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
norm=lambda s:re.sub('[^A-Z0-9]','',str(s).upper())
def number(x):
 try:return float(str(x).replace(' ','').replace(',','.'))
 except:return np.nan
rows=[];inputs=[]
for rev,g in S.groupby('review'):
 y=int(rev[:4]);m=4 if rev.endswith('H1')else 10;ym=y*100+m;f=BASE/'open_questions_20261101/eligibility'/f'{ym}.xls';assert f.exists();x=pd.read_excel(f,sheet_name='Instrument Trading Details',header=None,engine='xlrd');hh=[i for i,z in x.iloc[:10].iterrows()if 'ISIN'in z.values and 'Instrument'in z.values];assert len(hh)==1;h=hh[0];cols={}
 for j,v in x.iloc[h].items():cols.setdefault(norm(v),[]).append(j)
 inputs.append({'review':rev,'file':str(f),'sha256':sha(f),'header_row':h+1,'monthly_turnover_column':cols['TOTALTURNOVER'][0]+1,'monthly_listed_days_column':cols['LISTEDDAYS'][0]+1})
 st=pd.Timestamp(y,m,1);end=st+pd.offsets.MonthEnd(0)
 for (ric,isin),z in g.groupby(['ric','nasdaq_isin']):
  u=roster[roster.month.eq(ym)&roster['isin'].eq(isin)];reason=[];r={'review':rev,'ric':ric,'nasdaq_isin':isin,'reference_month':ym,'source_file':str(f),'source_sha256':sha(f),'matched_roster_rows':len(u)}
  if len(u)!=1:reason.append('nonunique_exact_ISIN_reference')
  else:
   u=u.iloc[0];row=int(u.source_excel_row)-1;assert x.iloc[row,cols['ISIN'][0]]==isin
   amount=number(x.iloc[row,cols['TOTALTURNOVER'][0]]);days=number(x.iloc[row,cols['LISTEDDAYS'][0]])
   q=P[P.ric.eq(ric)&P.date.between(st,end)];vals=pd.to_numeric(q.turnover,errors='coerce');got=vals.sum(min_count=1);error=got/amount-1 if amount>0 else np.nan
   r.update(currency=str(u.currency),source_url=u.source_url,source_excel_row=row+1,original_month_turnover=amount,panel_month_turnover=got,monthly_relative_error=error,original_listed_days=days,panel_nonmissing_days=int(vals.notna().sum()),panel_negative_days=int(vals.lt(0).sum()),panel_sources=';'.join(sorted(q.source.dropna().unique())))
   if str(u.currency)!='SEK':reason.append('reference_currency_not_SEK')
   if not(amount>0 and np.isfinite(error)and abs(error)<=.001):reason.append('monthly_turnover_mismatch_or_missing')
   if vals.notna().sum()<days:reason.append('month_insufficient_reported_days')
   if vals.lt(0).any():reason.append('negative_turnover')
   if set(q.source.dropna())!={'tr'}:reason.append('nonTR_or_missing_source')
  r['unit_pass']=not reason;r['unit_reasons']=';'.join(reason);rows.append(r)
Q=pd.DataFrame(rows);assert not Q.duplicated(['review','ric']).any();Q.to_csv(PVT/'MONTHLY_TURNOVER_RECONCILIATION_NUMERIC.csv',index=False)
public=Q.drop(columns=['original_month_turnover','panel_month_turnover']);public.to_csv(O/'MONTHLY_TURNOVER_UNIT_FLAGS.csv',index=False)
G=S.merge(public[['review','ric','unit_pass','unit_reasons']],on=['review','ric'],validate='m:1');G['cash_gate_pass']=G.turnover_presence_pass&G.dated_currency_unique_SEK&G.unit_pass;G.to_csv(O/'ROLE_FINAL_SOURCE_GATE.csv',index=False)
F=G.groupby(['event_id','review']).agg(gate_pass=('cash_gate_pass','all')).reset_index();F.to_csv(O/'EVENT_FINAL_SOURCE_GATE.csv',index=False)
summary={'created_utc':datetime.now(timezone.utc).isoformat(),'monthly_security_checks':len(Q),'unit_pass_security_checks':int(Q.unit_pass.sum()),'raw_files':inputs,'source_presence_events':65,'final_pass_events':int(F.gate_pass.sum()),'final_pass_reviews':int(F[F.gate_pass].review.nunique()),'by_review':F.groupby('review').gate_pass.agg(['sum','size']).reset_index().to_dict('records'),'unit_failure_rows':public.loc[~public.unit_pass,['review','ric','unit_reasons']].to_dict('records'),'no_event_window_totals_ratios_or_economic_outcomes':True,'limits':['Monthly vendor amount reconciliation, not daily trade-level audit','Dated reference currency; no generic all-venues or share-quantity interpretation','Future window coverage conditions sample']}
(O/'UNIT_GATE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items()if k!='raw_files'},indent=2))
