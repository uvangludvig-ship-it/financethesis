"""Coverage only: complete missing price-map cases without reading price values."""
from pathlib import Path
import pandas as pd,json
R=Path('/Users/ludviguvang/dev/financethesis');O=Path(__file__).resolve().parent
m=pd.read_csv(O/'FI_period_identity_and_report_coverage.csv')
fi=pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=['Fond_institutnummer','ISIN-kod_instrument','Kvartalsslut','Tillgångsslag_enligt_LVF_5_kap'],dtype={'Fond_institutnummer':str})
fi=fi[fi['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')]
counts=fi.groupby(['Kvartalsslut','ISIN-kod_instrument']).Fond_institutnummer.nunique().to_dict()
idx=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',usecols=['ric','date'],parse_dates=['date'])
cal=pd.DatetimeIndex(sorted(idx[idx.ric.eq('.OMXSBGI')].date.unique()))
st=pd.read_csv(R/'data/raw/lseg/panel_2012_2026/stocks_static.csv')
candidates={'ALIV SDB':'ALIVsdb.ST','INDU C':'INDUc.ST','ATCO B':'ATCOb.ST'}
for i,z in m.iterrows():
 t=cal[cal.get_loc(pd.Timestamp(z.effective_date))-1]
 q1=t.to_period('Q').end_time.normalize();q0=(t.to_period('Q')-1).end_time.normalize()
 m.loc[i,'implementation_trade_day']=str(t.date());m.loc[i,'FI_q0']=str(q0.date());m.loc[i,'FI_q1']=str(q1.date())
 m.loc[i,'reference_ISIN_FI_funds_q0']=counts.get((str(q0.date()),z.reference_ISIN),0)
 m.loc[i,'reference_ISIN_FI_funds_q1']=counts.get((str(q1.date()),z.reference_ISIN),0)
 if z.ticker in candidates:
  ric=candidates[z.ticker];s=st[st.ric.eq(ric)];assert len(s)==1
  m.loc[i,'secondary_panel_unverified_RIC_candidate']=ric
  m.loc[i,'secondary_panel_first_date']=s.iloc[0].first_date;m.loc[i,'secondary_panel_last_date']=s.iloc[0].last_date
  m.loc[i,'secondary_panel_ISIN']=s.iloc[0].IssueISIN
  m.loc[i,'secondary_panel_identity_status']='candidate RIC exists; missing vendor ISIN/name; exact dated bridge still required'
m.to_csv(O/'FI_period_expanded_metadata_coverage.csv',index=False)
summary={'exact_reference_ISIN_reportrows_both_quarters':int((m.reference_ISIN_FI_funds_q0.gt(0)&m.reference_ISIN_FI_funds_q1.gt(0)).sum()),
 'reference_ISIN_missing_one_endpoint':m.loc[m.reference_ISIN_FI_funds_q0.eq(0)|m.reference_ISIN_FI_funds_q1.eq(0),['event_id','ticker','FI_q0','FI_q1','reference_ISIN_FI_funds_q0','reference_ISIN_FI_funds_q1']].to_dict('records'),
 'candidate_alias_bridge_additional_two': ['E029 SINCH 2021 split','E035 SAAB B 2024 split'],
 'secondary_price_candidates':candidates,
 'note':'Report-row metadata only, not positive holdings, balanced funds, clean quantities or a proven zero. Candidate alias chains are not revalidated here.'}
(O/'additional_metadata_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))

# Keep valid empty-file schema: no matching same-security events within 90 calendar days.
cols=['omxs30_event','omxs30_ticker','omxs30_type','omxs30_ED','omxsb_event','omxsb_type','omxsb_ED','calendar_gap','match']
a=m.copy();a['effective_date']=pd.to_datetime(a.effective_date)
s=pd.read_csv(R/'data/input/omxsb/omxsb_changes_2007_2026.csv',usecols=['event_id','effective_date','ticker','isin','type'],parse_dates=['effective_date'])
x=[]
for z in a.itertuples():
 for y in s.itertuples():
  same=(z.ticker==y.ticker)or(pd.notna(z.reference_ISIN)and z.reference_ISIN==y.isin)
  gap=(z.effective_date-y.effective_date).days
  if same and abs(gap)<=90:x.append(dict(zip(cols,[z.event_id,z.ticker,z.type,str(z.effective_date.date()),y.event_id,y.type,str(y.effective_date.date()),gap,'exact ticker or dated ISIN'])))
pd.DataFrame(x,columns=cols).to_csv(O/'FI_period_same_security_nearby_dates.csv',index=False)
