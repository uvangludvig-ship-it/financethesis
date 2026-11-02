"""Metadata/identity/coverage only. No price, return or holdings quantities loaded."""
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd,numpy as np,json,hashlib
R=Path('/Users/ludviguvang/dev/financethesis');O=Path(__file__).resolve().parent
p=R/'data/input/omxsb/omxs30_changes_2005_2026.csv';e=pd.read_csv(p,parse_dates=['effective_date','announcement_date'])
e['scheduled_review']=e.reason.str.startswith('semi-annual review');e['regime']=np.where(e.effective_date.ge('2025-07-01'),'2025_methodology_reset','old_methodology')
e['source_host']=e.source_url.map(lambda x:urlparse(x).hostname)
def source_class(x):
 if x.verification=='UNVERIFIED':return 'inferred_placeholder'
 if x.verification!='VERIFIED':return 'secondary_or_unverified_event_evidence'
 if x.source_host in ['mondovisione.com','www.mondovisione.com','www.finanznachrichten.de']:return 'claimed_read_verbatim_Nasdaq_reproduction'
 return 'claimed_read_primary_Nasdaq_release_or_wire'
e['source_evidence_class']=[source_class(x)for x in e.itertuples()]
e.to_csv(O/'all48_event_metadata.csv',index=False)
counts=[]
for name,sel in [('all48',e),('dated46',e[e.effective_date.notna()]),('scheduled42',e[e.scheduled_review]),
                 ('FI_2019_2025',e[e.effective_date.between('2019-01-01','2025-12-31')]),
                 ('FI_scheduled_old_regime',e[e.scheduled_review&e.effective_date.between('2019-01-01','2025-06-30')]),
                 ('reset2025',e[e.effective_date.eq('2025-07-01')])]:
 counts.append(dict(sample=name,N=len(sel),additions=int(sel.type.eq('addition').sum()),deletions=int(sel.type.eq('deletion').sum()),
                    effective_dates=int(sel.effective_date.nunique()),announcement_dates=int(sel.announcement_date.nunique()),
                    missing_AD=int(sel.announcement_date.isna().sum()),missing_ED=int(sel.effective_date.isna().sum()),
                    missing_ISIN=int(sel['isin'].isna().sum()),verification=sel.verification.value_counts().to_dict(),
                    source_classes=sel.source_evidence_class.value_counts().to_dict()))
bydate=e[e.effective_date.notna()].groupby('effective_date').agg(N=('event_id','size'),additions=('type',lambda x:x.eq('addition').sum()),deletions=('type',lambda x:x.eq('deletion').sum()),scheduled=('scheduled_review','all')).reset_index()
bydate['paired_slots_arithmetic_only']=bydate[['additions','deletions']].min(axis=1);bydate.to_csv(O/'changes_by_effective_date.csv',index=False)

# Exact historical Nasdaq ticker/ISIN and existing audited RIC mapping; no name guesses.
u=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligibility/dated_stockholm_instrument_roster.csv',parse_dates=['reference_date'])
rp=pd.read_csv(R/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv',parse_dates=['reference_date'])
st=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv',parse_dates=['first_date','last_date'])
idx=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',usecols=['ric','date'],parse_dates=['date']);cal=pd.DatetimeIndex(sorted(idx[idx.ric.eq('.OMXSBGI')].date.unique()))
fi=pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=['Fond_institutnummer','ISIN-kod_instrument','Kvartalsslut','Tillgångsslag_enligt_LVF_5_kap'],dtype={'Fond_institutnummer':str})
fi=fi[fi['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')]
fipos=fi.groupby(['Kvartalsslut','ISIN-kod_instrument'])['Fond_institutnummer'].nunique().to_dict()
fm=pd.read_csv(R/'output/omxsb_extension_20261031/ownership/fi_fund_quarter_metadata.csv',dtype={'Fond_institutnummer':str})
quarters=set(fm.Kvartalsslut)
alias=json.loads((R/'output/omxsb_extension_20261031/ownership/validated_isin_aliases.json').read_text())
current=e[e.effective_date.between('2019-01-01','2025-12-31')].copy();mapped=[]
for z in current.itertuples():
 period=u[u.reference_date.le(z.announcement_date)].reference_date.max();ru=u[u.reference_date.eq(period)&u.stock_type&u.listed_at_month_end]
 hit=ru[ru.ticker.eq(z.ticker)]
 record=dict(event_id=z.event_id,company=z.company,ticker=z.ticker,effective_date=str(z.effective_date.date()),announcement_date=str(z.announcement_date.date()),type=z.type,
             verification=z.verification,source_evidence_class=z.source_evidence_class,source_ISIN=z.isin,
             reference_date=str(period.date()),exact_ticker_rows=len(hit))
 if len(hit)!=1:record['identity_status']='needs_manual_historical_identity';mapped.append(record);continue
 h=hit.iloc[0];rr=rp[rp.reference_date.eq(period)&rp.nasdaq_isin.eq(h['isin'])]
 rics=sorted(rr.ric.unique());record.update(company_code=h.company_code,reference_ISIN=h['isin'],source_ISIN_matches_reference=bool(z.isin==h['isin']),
                  RIC_candidates=';'.join(rics),RIC_candidates_N=len(rics),Nasdaq_source=h.source_url,Nasdaq_source_row=int(h.source_excel_row))
 if len(rics)!=1:record['identity_status']='ambiguous_or_missing_RIC';mapped.append(record);continue
 ric=rics[0];ii=cal.get_loc(z.effective_date);trade=cal[ii-1];q1=trade.to_period('Q').end_time.normalize();q0=(trade.to_period('Q')-1).end_time.normalize()
 ids=set(alias.get(ric,[]))|{h['isin']};allobs=fi[fi['ISIN-kod_instrument'].isin(ids)&fi.Kvartalsslut.isin([str(q0.date()),str(q1.date())])]
 ss=st[st.ric.eq(ric)];spans=bool(len(ss)==1 and ss.iloc[0].first_date<=z.announcement_date and ss.iloc[0].last_date>=z.effective_date)
 record.update(identity_status='exact_dated_ticker_ISIN_existing_RIC_mapping',ric=ric,implementation_trade_day=str(trade.date()),FI_q0=str(q0.date()),FI_q1=str(q1.date()),
               FI_quarters_metadata_present=str(q0.date())in quarters and str(q1.date())in quarters,
               reference_ISIN_FI_funds_q0=fipos.get((str(q0.date()),h['isin']),0),reference_ISIN_FI_funds_q1=fipos.get((str(q1.date()),h['isin']),0),
               accepted_ISIN_candidates=';'.join(sorted(ids)),
               candidate_alias_FI_funds_q0=int(allobs.loc[allobs.Kvartalsslut.eq(str(q0.date())),'Fond_institutnummer'].nunique()),
               candidate_alias_FI_funds_q1=int(allobs.loc[allobs.Kvartalsslut.eq(str(q1.date())),'Fond_institutnummer'].nunique()),
               candidate_FI_ISINs_q0=';'.join(sorted(allobs.loc[allobs.Kvartalsslut.eq(str(q0.date())),'ISIN-kod_instrument'].unique())),
               candidate_FI_ISINs_q1=';'.join(sorted(allobs.loc[allobs.Kvartalsslut.eq(str(q1.date())),'ISIN-kod_instrument'].unique())),
               static_price_span_AD_ED=spans)
 mapped.append(record)
m=pd.DataFrame(mapped);m.to_csv(O/'FI_period_identity_and_report_coverage.csv',index=False)

# Date and identifier only; no return values accessed.
sbp=R/'data/input/omxsb/omxsb_changes_2007_2026.csv'
sb=pd.read_csv(sbp,usecols=['event_id','effective_date','announcement_date','ticker','isin','type'],parse_dates=['effective_date','announcement_date'])
ov=[]
for z in e[e.effective_date.notna()].itertuples():
 for y in sb.itertuples():
  same_ED=z.effective_date==y.effective_date;same_AD=pd.notna(z.announcement_date)and pd.notna(y.announcement_date)and z.announcement_date==y.announcement_date
  same_security=(pd.notna(z.isin)and pd.notna(y.isin)and z.isin==y.isin)or(pd.notna(z.ticker)and pd.notna(y.ticker)and z.ticker==y.ticker)
  windows_overlap=pd.notna(z.announcement_date)and pd.notna(y.announcement_date)and max(z.announcement_date,y.announcement_date)<=min(z.effective_date,y.effective_date)
  if same_ED or same_AD or (same_security and windows_overlap):ov.append(dict(omxs30_event=z.event_id,omxsb_event=y.event_id,omxs30_ED=str(z.effective_date.date()),omxsb_ED=str(y.effective_date.date()),same_ED=same_ED,same_AD=same_AD,same_security_lexical=same_security,AD_ED_windows_overlap=windows_overlap,omxs30_type=z.type,omxsb_type=y.type))
pd.DataFrame(ov,columns=['omxs30_event','omxsb_event','omxs30_ED','omxsb_ED','same_ED','same_AD','same_security_lexical','AD_ED_windows_overlap','omxs30_type','omxsb_type']).to_csv(O/'OMXSB_calendar_overlap.csv',index=False)
summary=dict(event_samples=counts,dated_effective_event_groups=len(bydate),paired_slots_arithmetic_only=int(bydate.paired_slots_arithmetic_only.sum()),
             FI_period_mapped_rows=len(m),FI_period_identity_status=m.identity_status.value_counts().to_dict(),
             FI_period_exact_reference_ISIN_bothquarters=int((m.reference_ISIN_FI_funds_q0.gt(0)&m.reference_ISIN_FI_funds_q1.gt(0)).sum()),
             FI_period_candidate_alias_bothquarters=int((m.candidate_alias_FI_funds_q0.gt(0)&m.candidate_alias_FI_funds_q1.gt(0)).sum()),
             FI_period_static_price_span=int(m.static_price_span_AD_ED.sum()),
             FI_source_ISIN_mismatches=m[m.source_ISIN.notna()&~m.source_ISIN_matches_reference][['event_id','company','source_ISIN','reference_ISIN','reference_date']].to_dict('records'),
             calendar_overlap_pairs=len(ov),
             source_hashes={str(x):hashlib.sha256(x.read_bytes()).hexdigest()for x in [p,sbp,R/'data/input/omxsb/omxs30_notes.md']},
             no_price_return_or_holding_quantity_loaded=True)
(O/'metadata_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary,indent=2,ensure_ascii=False))
