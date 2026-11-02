from pathlib import Path
import os
import pandas as pd, numpy as np, json,re
O=Path(__file__).resolve().parent; W=O.parents[1]; R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3])); C=R/'code/claude_checks'
F=pd.read_csv(C/'data/fi_all_funds_klass.csv',dtype={'fund_id':str});F['kv']=pd.to_datetime(F.kvartal)
H=pd.read_pickle(C/'data/fi_all_holdings.pkl');H['fund_id']=H.fund_id.astype(str);H['kv']=pd.to_datetime(H.kvartal);H['qty']=pd.to_numeric(H.antal.astype(str).str.replace(',','.').str.replace(' ',''),errors='coerce')
HP=H[H.qty>0]; SEN=HP[HP['isin'].str.startswith('SE')].groupby(['kv','fund_id'])['isin'].nunique()
j=F.jmf.fillna('').str.lower();B=j.str.contains(r'stockholm benchmark|omxsb|\bsbx');F['H']=j.str.contains(r'six ?(?:portfolio|prx|return|rx)|sixrx|sixprx|omxs ?gi|omxspi|all.?share')&~B
ni=F.namn.astype(str).str.contains('index|indexnära|exponering|etf|xact|passiv|access',case=False);F['active_proxy']=~F.bred.astype(bool)&~ni
F['nse']=[SEN.get((a,b),0)for a,b in zip(F.kv,F.fund_id)]
FM=pd.read_csv(O/'inputs/latest_metadata_classification.csv',dtype={'fund_id':str});FM['kv']=pd.to_datetime(FM.quarter);FM=FM.set_index(['kv','fund_id']);fm=FM.to_dict('index')
ix=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date']);cal=pd.DatetimeIndex(ix.loc[(ix.ric=='.OMXSBGI')&ix.close.notna(),'date'].sort_values().unique())
S=pd.read_csv(C/'runda2_resultat/T5urval_T7_T8b_events.csv',parse_dates=['AD']);S=S[(S.AD>='2019-01-01')&(S.type=='addition')].copy();qs=sorted(HP.kv.unique())
periods=[]
for rev,s in S.groupby('review',sort=False):
 r=s.iloc[0];pre=[q for q in qs if q<r.AD];post=[q for q in qs if q>=cal[min(int(r.iE)+20,len(cal)-1)]]
 if pre and post:periods.append((rev,pre[-1],post[0]))
rows=[]
for rev,q0,q1 in periods:
 pre=F[(F.kv==q0)&F.H&F.active_proxy&(F.nse>=10)]
 post=F[F.kv==q1].set_index('fund_id')
 for x in pre.itertuples():
  if x.fund_id not in post.index:continue
  a=fm.get((q0,x.fund_id),{});b=fm.get((q1,x.fund_id),{})
  jb=str(post.loc[x.fund_id,'jmf'])
  norm=lambda z:re.sub(r'\s+',' ',str(z).strip().lower())
  rows.append(dict(review=rev,q0=str(q0.date()),q1=str(q1.date()),fund_id=x.fund_id,fund_name=x.namn,pre_benchmark=x.jmf,post_benchmark=jb,pre_n_instr=a.get('n_instr'),post_n_instr=b.get('n_instr'),pre_status=a.get('status'),post_status=b.get('status'),same_label=norm(x.jmf)==norm(jb),separator=bool(re.search(r'[;|]',str(x.jmf))),special_or_composite=bool(re.search(r';|\||msci|omrx|solactive|bloomberg|\bex\b|procent|carnegie|hfrx',str(x.jmf),re.I))))
D=pd.DataFrame(rows);D.to_csv(O/'h_group_report_gate.csv',index=False)
summary={'review_count':len(periods),'fund_review_rows':len(D),'unique_funds':D.fund_id.nunique(),'median_funds_per_review':D.groupby('review').fund_id.nunique().median(),'empty_pre_report_rows':int(D.pre_n_instr.fillna(0).eq(0).sum()),'empty_post_report_rows':int(D.post_n_instr.fillna(0).eq(0).sum()),'label_changed_rows':int((~D.same_label).sum()),'composite_special_rows':int(D.special_or_composite.sum()),'pure_unspecial_same_label_nonempty_rows':int((~D.special_or_composite&D.same_label&(D.pre_n_instr>0)&(D.post_n_instr>0)).sum())}
D[D.special_or_composite].groupby('pre_benchmark').agg(rows=('fund_id','size'),funds=('fund_id','nunique')).to_csv(O/'h_composite_labels.csv')
# Data-quality counts at selected H fund-quarter combinations only; no owner changes computed.
qfund=set(zip(pd.to_datetime(D.q0),D.fund_id))|set(zip(pd.to_datetime(D.q1),D.fund_id))
HH=H[[k in qfund for k in zip(H.kv,H.fund_id)]]
summary['H_raw_rows']=len(HH);summary['negative_quantity_rows']=int(HH.qty.lt(0).sum());summary['missing_quantity_rows']=int(HH.qty.isna().sum());summary['duplicate_fund_isin_quarter_rows']=int(HH.duplicated(['kv','fund_id','isin'],keep=False).sum())
# Static ISIN availability / first-seen coverage, not a dated security validation.
tu=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/td_universe.csv');st=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv');im=dict(zip(tu.RIC,tu.IssueISIN));im.update({k:v for k,v in zip(st.ric,st.IssueISIN)if isinstance(v,str)})
first=HP.groupby('isin').kv.min().to_dict();pq={r:(a,b)for r,a,b in periods}
S['isin_static']=S.ric.map(im);S['q0']=S.review.map(lambda r:pq.get(r,(None,None))[0]);S['static_isin_seen_pre']=[isinstance(i,str)and q is not None and first.get(i,pd.Timestamp('2100-01-01'))<=q for i,q in zip(S.isin_static,S.q0)]
S[['review','ric','event','isin_static','q0','static_isin_seen_pre']].to_csv(O/'h_security_gate.csv',index=False)
summary['candidate_rows']=len(S);summary['candidate_first_seen_pass']=int(S.static_isin_seen_pre.sum());summary['first_seen_failed_treated']=int(((S.event==1)&~S.static_isin_seen_pre).sum());summary['first_seen_failed_controls']=int(((S.event==0)&~S.static_isin_seen_pre).sum())
# Restrict data-quality diagnostics to the T14 target securities and the selected H fund-quarter pairs.
target_isins=set(S.loc[S.static_isin_seen_pre,'isin_static'])
HT=HH[HH['isin'].isin(target_isins)]
summary['target_isin_H_rows']=len(HT)
summary['target_negative_rows']=int(HT.qty.lt(0).sum())
summary['target_missing_rows']=int(HT.qty.isna().sum())
HT[(HT.qty<0)|HT.qty.isna()][['kv','fund_id','isin','instrument','antal']].to_csv(O/'h_target_invalid_rows.csv',index=False)
cleanD=D[~D.special_or_composite&D.same_label&(D.pre_n_instr>0)&(D.post_n_instr>0)]
summary['clean_metadata_unique_funds']=cleanD.fund_id.nunique()
summary['clean_metadata_min_funds_per_review']=int(cleanD.groupby('review').fund_id.nunique().min())
summary['clean_metadata_max_funds_per_review']=int(cleanD.groupby('review').fund_id.nunique().max())
summary['clean_metadata_median_funds_per_review']=float(cleanD.groupby('review').fund_id.nunique().median())
# Exact event/review/endpoint intersection: distinguish broad diagnostics from relevant cells.
J=S[S.static_isin_seen_pre][['review','ric','event','isin_static']].merge(D[['review','fund_id','q0','q1','special_or_composite','same_label','pre_n_instr','post_n_instr']],on='review')
JJ=pd.concat([J.assign(kv=pd.to_datetime(J.q0),endpoint='pre'),J.assign(kv=pd.to_datetime(J.q1),endpoint='post')],ignore_index=True)
JH=JJ.merge(H[['kv','fund_id','isin','qty','instrument','antal']],left_on=['kv','fund_id','isin_static'],right_on=['kv','fund_id','isin'],how='inner')
BAD=JH[JH.qty.lt(0)|JH.qty.isna()].copy()
BAD.to_csv(O/'h_exact_ambiguous_fund_security_endpoints.csv',index=False)
summary['exact_negative_endpoint_rows']=int(BAD.qty.lt(0).sum())
summary['exact_missing_endpoint_rows']=int(BAD.qty.isna().sum())
summary['exact_ambiguous_fund_security_reviews']=len(BAD[['review','ric','fund_id']].drop_duplicates())
summary['quarter_pairs']=D[['review','q0','q1']].drop_duplicates().to_dict('records')
(O/'h_data_gate_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print('EMPTYPOST',D[D.post_n_instr.fillna(0)==0][['review','fund_id','fund_name','post_status']].to_string(index=False))
