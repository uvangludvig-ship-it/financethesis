"""Diagnose source-gate failures; never constructs fund flows or returns."""
from pathlib import Path
import pandas as pd,numpy as np,json,datetime,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership';CAP=O.parents[1]/'contribution_round_20261103/ownership_capital'
(O/'DOMINANT_SOURCE_LOCK.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Source only: identify stage failures for allmappedfunds and known trackers51482/60824; largest owners ranked by mean within-event-stock capital share from same audited pre2024support, no returns/flows/new outcomes. Check representative shareclass alternative as an approximation only; no relaxed risk result.'},indent=2))
M=pd.read_excel(R/'data/raw/shof/fundmaster.xlsx',usecols=['performanceid','fundid','ISIN','currencyid','inceptiondate','obsoletedate','shareclasslegalname']).drop_duplicates('performanceid')
H=pd.read_csv(O/'monthly_source_fund_feasibility.csv',dtype={'fund_id':str})
V=pd.read_csv(R/'data/derived/shof_monthly/shof_valuations_monthly.csv',usecols=['performanceId','ym','last_date','tnaclass','tnafund','ccy_class','ccy_fund'])
V=V[V.ym.le('2023-12')].merge(M,left_on='performanceId',right_on='performanceid')
T=pd.read_csv(R/'data/derived/shof_monthly/shof_rips_monthly.csv',usecols=['performanceId','returntype','ym','last_date'])
T=T[T.returntype.eq(1)&T.ym.le('2023-12')].rename(columns={'last_date':'tri_date'}).drop(columns='returntype')
V=V.merge(T,on=['performanceId','ym'],how='left',validate='1:1')
V['tri_present']=V.tri_date.notna();V['date_gap']=(pd.to_datetime(V.last_date)-pd.to_datetime(V.tri_date)).abs().dt.days
rows=[]
for (fid,ym),d in V[V.fundid.isin(H.fundid)].groupby(['fundid','ym']):
 den=d.tnafund.median();ratio=d.tnaclass.sum(min_count=1)/den if den>0 else np.nan
 have=d.tri_present&d.ccy_class.eq('SEK')&d.date_gap.le(4)&d.tnaclass.gt(0)
 maxshare=d.loc[have,'tnaclass'].max()/den if den>0 and have.any() else np.nan
 rows.append(dict(fundid=fid,ym=ym,allpositive=bool(d.tnaclass.gt(0).all() and d.tnafund.gt(0).all()),allSEK=bool(d.ccy_class.eq('SEK').all() and d.ccy_fund.eq('SEK').all()),cap_reconcile=bool(.99<=ratio<=1.01),ratio=ratio,repeatcap=bool(den>0 and (d.tnafund.max()-d.tnafund.min())/den<.001),dates_same=d.last_date.nunique()==1,allTRI=bool(d.tri_present.all()),TRIdates=bool(d.date_gap.le(4).all()),oneSEKclassTRI=bool(have.any()),largest_covered_class_share=maxshare,observedclasses=d.performanceId.nunique()))
Q=pd.DataFrame(rows);flags=['allpositive','allSEK','cap_reconcile','repeatcap','dates_same','allTRI','TRIdates','oneSEKclassTRI']
G=pd.read_csv(OWN/'decomp_fund_groups.csv',dtype={'fund_id':str},usecols=['review','fund_id','q0']).drop_duplicates()
out=[]
for x in H.itertuples():
 q0=G.loc[G.review.eq(x.review)&G.fund_id.eq(x.fund_id),'q0'].iloc[0];end=pd.Period(q0,freq='M');months={str(a) for a in pd.period_range(end-24,end,freq='M')};d=Q[Q.fundid.eq(x.fundid)&Q.ym.isin(months)]
 r=dict(review=x.review,fund_id=x.fund_id,fundid=x.fundid,months=len(d),eligible=x.provisional25endpoint_pass)
 r.update({a+'_months':int(d[a].sum()) for a in flags});r['class_sum_to_fund_TNA_min']=d.ratio.min();r['class_sum_to_fund_TNA_max']=d.ratio.max();r['largest_covered_SEKclass_share_min']=d.largest_covered_class_share.min();r['largest_covered_SEKclass_share_max']=d.largest_covered_class_share.max();out.append(r)
D=pd.DataFrame(out);D.to_csv(O/'source_stage_diagnostics.csv',index=False)
K=D[D.fund_id.isin(['51482','60824'])];K.to_csv(O/'known_trackers_source_diagnostics.csv',index=False)
knownfid=set(K.fundid);KCLASS=V[V.fundid.isin(knownfid)&V.ym.eq('2023-09')].copy();KCLASS['class_share_of_fund']=KCLASS.tnaclass/KCLASS.tnafund
KCLASS[['fundid','performanceId','ISIN','currencyid','shareclasslegalname','ccy_class','ccy_fund','class_share_of_fund','tri_present','date_gap']].to_csv(O/'known_tracker_class_metadata_202309.csv',index=False)
# Rank economically large owners by equal-event mean within-stock capital fraction, pre2024, eventrole only, both endpoints.
L=pd.read_csv(CAP/'normalized_fund_role_contributions.csv.gz',dtype={'fund_id':str},usecols=['event_id','review','role','fund_id']);L=L[L.role.eq('event')&L.review.le('2023H2')]
S=pd.read_csv(OWN/'security_role_gate.csv');S=S[S.event_id.isin(L.event_id)&S.role.eq('event')]
ids=set(S.aliases.str.split(';').explode());dates=set(S.q0)|set(S.q1);parts=[]
for c in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=['ISIN-kod_instrument','Kvartalsslut','Fond_institutnummer','Antal'],dtype={'Fond_institutnummer':str},chunksize=500000):
 parts.append(c[c['ISIN-kod_instrument'].isin(ids)&c.Kvartalsslut.isin(dates)])
raw=pd.concat(parts,ignore_index=True);raw.Antal=pd.to_numeric(raw.Antal,errors='coerce');rank=[]
for s in S.itertuples():
 pop=set(L.loc[L.event_id.eq(s.event_id),'fund_id']);d=raw[raw['ISIN-kod_instrument'].isin(s.aliases.split(';'))&raw.Fond_institutnummer.isin(pop)]
 for date in [s.q0,s.q1]:
  q=d[d.Kvartalsslut.eq(date)].groupby('Fond_institutnummer').Antal.sum(min_count=1);den=q.sum()
  if den>0:
   for fid,qty in q.items():rank.append(dict(fund_id=fid,review=s.review,event_id=s.event_id,date=date,stock_capital_fraction=qty/den))
A=pd.DataFrame(rank);N=2*S.event_id.nunique();ranked=A.groupby('fund_id').stock_capital_fraction.sum().div(N).sort_values(ascending=False).rename('mean_fraction_across135events2endpoints').reset_index()
ranked.to_csv(O/'owner_size_source_ranking.csv',index=False)
top=set(ranked.head(12).fund_id)|{'51482','60824'};D[D.fund_id.isin(top)].merge(ranked,on='fund_id').to_csv(O/'largest_owner_source_diagnostics.csv',index=False)
summary={'source_feasibility_not_risk_result':True,'top_owner_ids':ranked.head(12).fund_id.tolist(),'known_trackers_latest':K[K.review.eq('2023H2')].to_dict('records'),'allfunds_latest':D[D.review.eq('2023H2')][['months']+[a+'_months' for a in flags]].eq(25).sum().to_dict(),'single_class_alternative':'FundTNA plus one SEK shareclass return is only an approximation to aggregate fund net flow: shareclass fees/distributions/hedging and return timing differ. Largest covered class share documented; no flows calculated, no gate relaxed.'}
(O/'DOMINANT_SOURCE_DIAGNOSTIC.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(K.to_string(index=False));print(ranked.head(12).to_string(index=False))
