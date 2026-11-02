from pathlib import Path
import pandas as pd, numpy as np, json, hashlib
O=Path(__file__).resolve().parent
CHAT=O.parents[1]; R=Path('/Users/ludviguvang/dev/financethesis')
Q=CHAT/'work/open_questions_20261101/demand_quarter'
# Only preholdings and evidence fields; no new price outcomes.
D=pd.read_csv(CHAT/'work/mechanism_frontier_20261102/demand/fund_event_demand_panel.csv.gz')
D=D[D.fund_id.eq(60320)&D.type.eq('deletion')].copy()
P=R/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv'
M=pd.read_csv(P,usecols=['event_id','ric','review','issuer','AD','ED','precar','log_mcap','mcap','chosen_controls','c1_ric','c2_ric','c3_ric'])
D=D.merge(M,on='event_id',how='left',validate='1:1')
S=pd.read_csv(Q/'quarter_security_snapshots.csv',usecols=['event_id','date','fi_price','agreeing_funds','ordinary_isins'])
S=S.rename(columns={'date':'before','fi_price':'fi_price_before','agreeing_funds':'price_funds_before','ordinary_isins':'before_price_isins'})
D=D.merge(S,on=['event_id','before'],how='left',validate='1:1')
px=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','mcap','shares','source'])
px=px[px.ric.isin(D.RIC.unique())].drop_duplicates()
assert not px.duplicated(['ric','date']).any()
pre=[]
for r in D.itertuples():
 t=px[(px.ric==r.RIC)&(px.date<=pd.Timestamp(r.before))&px.mcap.gt(0)].sort_values('date')
 z=t.iloc[-1] if len(t) else None
 pre.append(dict(event_id=r.event_id,pre_mcap=np.nan if z is None else z.mcap,pre_shares=np.nan if z is None else z.shares,pre_mcap_date=None if z is None else str(z.date.date()),pre_mcap_age=np.nan if z is None else (pd.Timestamp(r.before)-z.date).days,pre_mcap_source=None if z is None else z.source))
D=D.merge(pd.DataFrame(pre),on='event_id',validate='1:1')
D['pre_class_fraction']=D.pre_shares*D.fi_price_before/D.pre_mcap
D['exposure_company_pp']=100*D.before_quantity*D.fi_price_before/D.pre_mcap
# Official preannouncement monthend turnover. Source row from verified datedISIN->RIC map.
E=CHAT/'work/open_questions_20261101/eligibility'
U=pd.read_csv(CHAT/'work/open_questions_20261101/eligible_pool/review_RIC_control_pool.csv')
U=U.rename(columns={'review':'review_cycle','ric':'RIC'})
u=['review_cycle','RIC','nasdaq_isin','source_excel_row','source_url','reference_date','publication_timestamp','company_code']
D=D.merge(U[u],on=['review_cycle','RIC'],how='left',validate='m:1',suffixes=('','_nasdaq'))
headers={str(z['month']):z for z in json.loads((E/'workbook_headers.json').read_text())}
rows=[]
for review,g in D[D.source_excel_row.notna()].groupby('review_cycle'):
 month=review[:4]+('04' if review[-1]=='1' else '10')
 fs=list(E.glob(month+'.xls*'));assert len(fs)==1
 x=pd.read_excel(fs[0],sheet_name='Instrument Trading Details',header=None)
 h=headers[month]
 # Rolling12month section is the last occurrence of TotalTurnover.
 turn=[int(k) for k,v in h['headers'].items() if ''.join(v.split()).upper()=='TOTALTURNOVER']
 assert len(turn)==3
 col=max(turn)
 top=' '.join(map(str,x.iloc[:h['header_excel_row']-1,col-2:col+4].to_numpy().ravel()))
 assert h['rolling_title'] in top,(month,top)
 for a in g.itertuples():
  row=int(a.source_excel_row)-1
  assert str(x.iloc[row,3])==str(a.nasdaq_isin)
  assert str(x.iloc[row,14])=='STO' and str(x.iloc[row,13])=='SEK'
  rows.append(dict(event_id=a.event_id,official_turnover_12m=pd.to_numeric(x.iloc[row,col],errors='coerce'),turnover_column_excel=col+1,turnover_header=h['headers'][str(col)],turnover_period=h['rolling_title'],turnover_source_file=str(fs[0])))
D=D.merge(pd.DataFrame(rows),on='event_id',how='left',validate='1:1')
D['log_liquidity']=np.log(D.official_turnover_12m/D.pre_mcap)
D['exclusion_reason']=''
def flag(mask,why):
 D.loc[mask,'exclusion_reason']=D.loc[mask,'exclusion_reason'].apply(lambda a:a+';'+why if a else why)
flag(D.review_cycle.eq('2022H1'),'simultaneous_Nordnet_ESG_switch')
flag(D.ric.isna(),'no_frozen_strict_matched_row')
flag(D.RIC.str.contains('SAMPO',case=False),'crosslisted_instrument_conversion')
flag(~D.measurement_status.eq('valid_position_pair'),'canonical_quantity_pair_unresolved')
flag(D.before_fund_isin.ne('SE0002756973')|D.after_fund_isin.ne('SE0002756973'),'legal_fund_ID_unresolved')
flag(D.before_quantity.isna()|D.before_quantity.lt(0),'invalid_pre_quantity')
flag(D.fi_price_before.isna()|D.fi_price_before.le(0)|D.price_funds_before.lt(3),'invalid_pre_nominal_price')
flag(D.pre_mcap.isna()|D.pre_mcap.le(0)|D.pre_mcap_age.gt(7),'pre_company_cap_missing_or_stale')
flag(D.pre_class_fraction.isna()|D.pre_class_fraction.gt(1.03)|D.pre_class_fraction.le(0),'pre_class_to_company_unit_failure')
flag(~np.isfinite(D.log_liquidity),'official_liquidity_unavailable')
flag(D.precar.isna()|D.log_mcap.isna(),'missing_frozen_pre_covariate')
D['gate_included']=D.exclusion_reason.eq('')
D.to_csv(O/'gate_event_ledger.csv',index=False)
T=D[D.gate_included].copy();r=T.groupby('review_cycle').exposure_company_pp.agg(['size','mean','std','min','max'])
r['range']=r['max']-r['min'];r.to_csv(O/'exposure_review_variation.csv')
FE=pd.get_dummies(T.review_cycle,dtype=float)
C=T[['log_mcap','precar','log_liquidity']].copy();C=(C-C.mean())/C.std()
X=np.column_stack([FE,C]);x=T.exposure_company_pp.to_numpy();w=1/T.groupby('review_cycle').event_id.transform('size').to_numpy()
Z=X*np.sqrt(w[:,None]);xx=x*np.sqrt(w)
res=xx-Z@np.linalg.lstsq(Z,xx,rcond=None)[0]
resfe=xx-(FE.to_numpy()*np.sqrt(w[:,None]))@np.linalg.lstsq(FE.to_numpy()*np.sqrt(w[:,None]),xx,rcond=None)[0]
T['residual_exposure_pp']=res/np.sqrt(w);T['residual_exposure_sq_weight']=res**2
rg=T.groupby('review_cycle').residual_exposure_sq_weight.sum();rg=rg/rg.sum();rg.to_csv(O/'review_exposure_information_share.csv')
T[['event_id','review_cycle','RIC','exposure_company_pp','residual_exposure_pp','residual_exposure_sq_weight']].to_csv(O/'exposure_residuals_NO_OUTCOMES.csv',index=False)
Xall=np.column_stack([X,x/.1]);Xw=Xall*np.sqrt(w[:,None]);rank=np.linalg.matrix_rank(Xw)
rankok=rank==Xw.shape[1];lev=np.sum(Xw*(Xw@np.linalg.inv(Xw.T@Xw)),axis=1) if rankok else np.full(len(T),np.nan)
T[['exposure_company_pp','log_mcap','precar','log_liquidity','pre_class_fraction']].corr().to_csv(O/'pre_covariate_correlations.csv')
checks=dict(N_canonical_deletions=len(D),N_included=len(T),G=T.review_cycle.nunique(),issuers=T.issuer.nunique(),zeros=int(T.before_quantity.eq(0).sum()),positive=int(T.before_quantity.gt(0).sum()),reviews_nonconstant=int(r['range'].gt(1e-10).sum()),exposure_median=float(T.exposure_company_pp.median()),exposure_iqr=float(T.exposure_company_pp.quantile(.75)-T.exposure_company_pp.quantile(.25)),exposure_min=float(x.min()),exposure_max=float(x.max()),within_review_sd_pp=float(np.sqrt(np.sum(resfe**2)/np.sum(w))),controlled_residual_sd_pp=float(np.sqrt(np.sum(res**2)/np.sum(w))),remaining_within_variance_fraction=float(np.sum(res**2)/np.sum(resfe**2)),rank=int(rank),columns=Xw.shape[1],max_leverage=float(np.nanmax(lev)),max_review_residual_exposure_share=float(rg.max()),review_with_max_share=str(rg.idxmax()),new_price_outcomes_loaded=False,strict_pool='Nordnet60320 only',rule='N>=30,G>=10,nonconstant_reviews>=8,fullrank',gate_pass=bool(len(T)>=30 and T.review_cycle.nunique()>=10 and r['range'].gt(1e-10).sum()>=8 and rankok))
(O/'gate_summary.json').write_text(json.dumps(checks,indent=2))
(O/'source_hashes_gate.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),O/'GATE_PROTOCOL.txt',P,Q/'quarter_security_snapshots.csv',CHAT/'work/mechanism_frontier_20261102/demand/fund_event_demand_panel.csv.gz']},indent=2))
print(json.dumps(checks,indent=2));print(D.exclusion_reason.value_counts().to_string())
