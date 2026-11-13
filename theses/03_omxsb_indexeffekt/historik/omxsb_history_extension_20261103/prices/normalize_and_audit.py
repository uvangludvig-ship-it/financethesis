"""Metadata-only validation, explicit field mapping and private long panel. No derived returns."""
from pathlib import Path
import os
from datetime import datetime,timezone
import json,hashlib
import pandas as pd,numpy as np
O=Path(os.environ.get('OMXSB_PRICE_WORKDIR',Path(__file__).resolve().parent));P=O/'private'
FIELDS=['close','totret','volume','bid','ask','mcap','shares']
MAP_TR={'Price Close':'close','Daily Total Return':'totret','Volume':'volume','Company Market Cap':'mcap','Outstanding Shares':'shares'}
MAP_PR={'TRDPRC_1':'close','ACVOL_UNS':'volume','BID':'bid','ASK':'ask'}
L=json.loads((O/'REQUEST_LOG.json').read_text());E=pd.read_csv(P/'EARLY_CANDIDATES.csv');E.candidate_ED=pd.to_datetime(E.candidate_ED)
assert len(L)<=90 and len({r['id']for r in L})==len(L)
meta=[];parts=[];same_return=[]
for r in L:
 if r['status']!='received':continue
 rawpath=Path(r['private_file']);rawpath=rawpath if rawpath.exists() else P/rawpath.name
 d=pd.read_csv(rawpath);datecol=d.columns[0];d['date']=pd.to_datetime(d[datecol],errors='coerce');assert d.date.notna().all()
 raw_duplicates=int(d.date.duplicated().sum())
 if raw_duplicates:
  for date,group in d.groupby('date'):
   assert all(group[c].dropna().nunique()<=1 for c in d.columns if c!='date'),(r['id'],str(date),'conflicting duplicate')
  d=d.groupby('date',as_index=False).first()
 assert not d.date.duplicated().any(),r['id']
 in_range=d.date.between(pd.Timestamp(r['start']),pd.Timestamp(r['end']));outside_rows=int((~in_range).sum());d=d[in_range].copy()
 mapping=MAP_TR if r['source'].startswith('TR')else MAP_PR
 known={k:v for k,v in mapping.items()if k in d}
 x=pd.DataFrame({'ric':r['ric'],'date':d.date,'request_id':r['id'],'source_kind':r['source']})
 for raw,f in known.items():x[f]=pd.to_numeric(d[raw],errors='coerce')
 parts.append(x)
 meta.append({'request_id':r['id'],'ric':r['ric'],'source_kind':r['source'],'rows':len(d),'first_date':str(d.date.min().date())if len(d)else None,'last_date':str(d.date.max().date())if len(d)else None,'outside_request_rows_excluded':outside_rows,'raw_duplicate_extra_rows':raw_duplicates,'normalized_duplicate_dates':int(d.date.duplicated().sum()),'source_header_mapping':json.dumps(known,sort_keys=True),**{f'nonnull_{f}':int(x[f].notna().sum())if f in x else 0 for f in FIELDS}})
 if {'Total Return','Daily Total Return'}<=set(d):
  a=pd.to_numeric(d['Total Return'],errors='coerce');b=pd.to_numeric(d['Daily Total Return'],errors='coerce');ok=a.notna()&b.notna()
  same_return.append({'ric':r['ric'],'both_numeric':int(ok.sum()),'same_to_absolute_tolerance1e_10':int(np.isclose(a[ok],b[ok],atol=1e-10,rtol=0).sum()),'equivalence_claim':False})
S=pd.concat(parts,ignore_index=True);S.to_csv(P/'NORMALIZED_BY_SOURCE.csv.gz',index=False)
stock=[]
for ric,g in S[~S.ric.str.startswith('.')].groupby('ric'):
 tr=g[g.source_kind.eq('TR')].set_index('date');pr=g[g.source_kind.eq('pricing_default_adjustment')].set_index('date');dates=tr.index.union(pr.index)
 x=pd.DataFrame(index=dates);x['ric']=ric
 for f in FIELDS:
  source=pr if f in ['bid','ask']else tr
  if f in source:x[f]=source[f].reindex(dates)
  else:x[f]=np.nan
  x[f+'_source']=np.where(x[f].notna(),('LSEG_pricing_default:'if f in ['bid','ask']else 'LSEG_TR:')+({'close':'TR.PriceClose','totret':'TR.TotalReturn1D','volume':'TR.Volume','mcap':'TR.CompanyMarketCap','shares':'TR.SharesOutstanding','bid':'BID','ask':'ASK'}[f]),'missing')
 stock.append(x.reset_index().rename(columns={'index':'date'}))
N=pd.concat(stock,ignore_index=True);assert not N.duplicated(['ric','date']).any()
N[['ric','date',*FIELDS]].to_csv(P/'FETCHED_NORMALIZED_LONG.csv.gz',index=False);N.to_csv(P/'FETCHED_NORMALIZED_WITH_PROVENANCE.csv.gz',index=False)
old=pd.read_csv(P/'EXISTING_PANEL_REUSE.csv.gz');old.date=pd.to_datetime(old.date);old=old.set_index(['ric','date']);new=N.set_index(['ric','date']);keys=old.index.union(new.index);C=pd.DataFrame(index=keys)
for f in FIELDS:
 a=old[f].reindex(keys);b=new[f].reindex(keys);C[f]=a.combine_first(b)
 C[f+'_source']=np.where(a.notna(),'existing_panel:'+f,new[f+'_source'].reindex(keys).fillna('missing'))
C=C.reset_index();assert not C.duplicated(['ric','date']).any();C[['ric','date',*FIELDS]].to_csv(P/'COMBINED_PREFER_EXISTING_LONG.csv.gz',index=False);C.to_csv(P/'COMBINED_WITH_PROVENANCE.csv.gz',index=False)
# Existing normalized totret is preserved, not certified as the same return definition.
checks=[]
for e in E.itertuples():
 start=e.candidate_ED-pd.Timedelta(days=400);end=e.candidate_ED+pd.Timedelta(days=200)
 for label,t in [('fetched',N),('combined',C)]:
  g=t[t.ric.eq(e.ric)&t.date.between(start,end)];z=g[g.date.between(e.candidate_ED-pd.Timedelta(days=30),e.candidate_ED+pd.Timedelta(days=30))]
  checks.append({'candidate_id':e.candidate_id,'candidate_ED':str(e.candidate_ED.date()),'ric':e.ric,'panel':label,'rows_full_interval':len(g),'nonnull_close_ED_plusminus30calendar':int(z.close.notna().sum()),'nonnull_dailyreturn_ED_plusminus30calendar':int(z.totret.notna().sum()),'first_close_date':str(g.loc[g.close.notna(),'date'].min().date())if g.close.notna().any()else '', 'last_close_date':str(g.loc[g.close.notna(),'date'].max().date())if g.close.notna().any()else '',**{f'nonnull_{f}':int(g[f].notna().sum())for f in FIELDS}})
A=pd.DataFrame(checks);A.to_csv(O/'SOURCE_AVAILABILITY_BY_CANDIDATE.csv',index=False)
pd.DataFrame(meta).to_csv(O/'RESPONSE_METADATA.csv',index=False);pd.DataFrame(same_return).to_csv(O/'RETURN_FIELD_EQUALITY_METADATA.csv',index=False)
# Index levels remain prices of GI indices, never the stock Daily Total Return field.
idx=[]
for ric,g in S[S.ric.str.startswith('.')].groupby('ric'):
 tr=g[g.source_kind.eq('TR_index')];pr=g[g.source_kind.eq('pricing_index_default_adjustment')]
 chosen=tr if 'close'in tr and tr.close.notna().any()else pr
 idx.append(chosen[['ric','date','close','source_kind','request_id']])
I=pd.concat(idx,ignore_index=True);assert not I.duplicated(['ric','date']).any();I.to_csv(P/'FETCHED_INDICES_LONG.csv.gz',index=False)
oldI=pd.read_csv(P/'EXISTING_INDEX_REUSE.csv.gz');oldI.date=pd.to_datetime(oldI.date)
merged=oldI.set_index(['ric','date'])['close'].combine_first(I.set_index(['ric','date'])['close']).rename('close').reset_index();merged.to_csv(P/'COMBINED_INDICES_LONG.csv.gz',index=False)
summary={'created_utc':datetime.now(timezone.utc).isoformat(),'requests':len(L),'request_errors':sum(r['status']=='error'for r in L),'candidate_count':len(E),'unique_RIC':E.ric.nunique(),'reviews':E.candidate_ED.nunique(),'all_date_keys_unique':True,'no_numeric_outcomes_computed':True,'long_schema':['ric','date',*FIELDS], 'totret':'Raw Daily Total Return (TR.TotalReturn1D) for newly fetched data; existing totret retains ambiguous legacy field lineage. No division, accumulation or return calculation.', 'normalized_close_policy':'TR.PriceClose only for stocks. Pricing TRDPRC_1 retained separately, never silently mixed into stock close. For index, documented price field fallback only when TR close absent.', 'reuse_policy':'Existing nonmissing cells retained; missing cells complemented from new source. Exact field provenance in private COMBINED_WITH_PROVENANCE.csv.gz.', 'no_full_return_panel_certification':'Source date subfields, fill/staleness, historic currency, corporate-action basis and share units not certified. Availability does not qualify estimation windows.', 'per_review':A.groupby(['panel','candidate_ED']).agg(candidates=('candidate_id','size'),any_close_near_ED=('nonnull_close_ED_plusminus30calendar',lambda x:int(x.gt(0).sum())),any_dailyreturn_near_ED=('nonnull_dailyreturn_ED_plusminus30calendar',lambda x:int(x.gt(0).sum()))).reset_index().to_dict('records'),'index_availability':merged.groupby('ric').agg(rows=('date','size'),first=('date','min'),last=('date','max'),nonnull_close=('close','count')).astype(str).reset_index().to_dict('records'),'price_missing_near_ED_candidates':A.loc[A.panel.eq('combined')&A.nonnull_close_ED_plusminus30calendar.eq(0),['candidate_id','candidate_ED','ric']].to_dict('records')}
(O/'AVAILABILITY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
