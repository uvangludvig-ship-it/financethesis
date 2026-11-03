"""Independent output/source-consistency checks; never computes returns or flows."""
from pathlib import Path
import pandas as pd,json,hashlib,zipfile,io,datetime
O=Path(__file__).resolve().parent
C=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke')
M=pd.read_csv(C/'work/shof_coverage_20261103/audit/EXISTING_A_RAW_VALIDATION_CLASSES.csv',dtype=str)
P=pd.read_csv(C/'work/shof_coverage_20261103/audit/EXISTING_A_RAW_VALIDATION_FUND_REVIEWS.csv',dtype=str)
S=pd.read_csv(O/'EXISTING_A_RAW_FUND_REVIEW_SOURCE_ELIGIBILITY.csv',dtype={'FI_fund_id':str})
E=pd.read_csv(O/'EXISTING_A_RAW_ENDPOINT_SOURCE_FLAGS.csv',dtype={'FI_fund_id':str})
L=json.loads((O/'INPUT_LOCK.json').read_text())
assert len(S)==1630 and len(E)==163*85
assert not S.duplicated(['review','FI_fund_id']).any()
assert S.groupby('FI_fund_id').size().eq(10).all()
assert S.in_frozen_old_A_pair.sum()==925
assert set(zip(S.loc[S.in_frozen_old_A_pair,'review'],S.loc[S.in_frozen_old_A_pair,'FI_fund_id']))==set(zip(P.review,P.fund_id))
assert not S.conditional_NAV_used.any() and not S.historical_class_universe_fully_certified.any()
for r in S.itertuples():
 year=int(r.review[:4]);month=3 if r.review.endswith('H1') else 9
 last=pd.Period(year=year,month=month,freq='M');first=last-24
 assert r.first_endpoint_month==str(first) and r.last_endpoint_month==str(last)
 z=E[E.FI_fund_id.eq(r.FI_fund_id)&E.month.between(str(first),str(last))]
 assert len(z)==25 and int(z.pass_source.sum())==r.valid_endpoints
 assert bool(z.pass_source.all())==r.D_RIPS_ECB_source_supported==r.D_provisional_current_master
for r in E[E.source_date.notna()].itertuples():
 date=pd.Timestamp(r.source_date);end=pd.Period(r.month,freq='M').end_time.normalize()
 assert 0<=(end-date).days<=4
 if pd.notna(r.FX_reference_dates):
  for fx in str(r.FX_reference_dates).split(';'):
   lag=(date-pd.Timestamp(fx)).days
   assert lag==0 or (date.weekday()>=5 and 0<lag<=4)
active=E[E.pass_source]
assert active.capital_reconciliation_pass.all() and active.fund_TNA_same_currency_copies_pass.all()
assert not active.uses_reference_FX.any(), 'Frozen master has no non-SEK pre-2024 classes; investigate discrepancy'
raws={}
for path,sha in L['inputs'].items():
 p=Path(path);assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
 if p.suffix.lower()=='.zip':
  with zipfile.ZipFile(p) as z:
   assert z.testzip() is None
   ns=[n for n in z.namelist() if n.lower().endswith('.csv')];assert len(ns)==1
   d=pd.read_csv(io.BytesIO(z.read(ns[0])),sep=';',dtype=str,usecols=lambda c:c.lower() in {'performanceid','date','returntype','unit_sek','tnaclass','tnafund','classcurrencyiso','fundcurrencyiso'})
   d.columns=d.columns.str.lower();d['date']=pd.to_datetime(d.date.str[:10])
  raws['RIPS' if 'returntype' in d.columns else 'Valuations']=d
V=raws['Valuations'];T=raws['RIPS'];T=T[T.returntype.isin(['1','1.0'])]
V['tnaclass']=pd.to_numeric(V.tnaclass,errors='coerce');V['tnafund']=pd.to_numeric(V.tnafund,errors='coerce')
V=V.set_index(['performanceid','date']);T=T.set_index(['performanceid','date']);M=M.set_index('performanceid')
checks=0
for r in active.itertuples():
 pids=str(r.active_class_ids).split(';');date=pd.Timestamp(r.source_date)
 z=V.loc[[(pid,date) for pid in pids]]
 tr=T.loc[[(pid,date) for pid in pids]]
 assert z.tnaclass.gt(0).all() and pd.to_numeric(tr.unit_sek,errors='coerce').gt(0).all()
 assert z.classcurrencyiso.eq('SEK').all()
 f=z.loc[z.fundcurrencyiso.eq('SEK')&z.tnafund.gt(0),'tnafund'];assert len(f)
 assert .99<=z.tnaclass.sum()/f.median()<=1.01
 assert (f.max()-f.min())/f.median()<.001
 assert pd.to_datetime(M.loc[pids,'inceptiondate']).le(date).all()
 checks+=1
out=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),review_window_aggregation_checks=len(S),passing_endpoint_raw_presence_and_capital_checks=checks,input_hashes_and_ZIP_CRC_pass=True,all_checks_pass=True,no_returns_flows_or_risk=True,eligibility_SHA256=hashlib.sha256((O/'EXISTING_A_RAW_FUND_REVIEW_SOURCE_ELIGIBILITY.csv').read_bytes()).hexdigest())
(O/'FINAL_CHECK.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
