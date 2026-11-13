"""Independent baseline capital reconciliation and scope audit; no return input."""
from pathlib import Path
import json,hashlib,datetime,re
import pandas as pd,numpy as np
O=Path(__file__).resolve().parent
P={k:Path(v['path'])for k,v in json.loads((O/'INPUT_SHA256.json').read_text()).items()}
H=pd.read_csv(O/'baseline_transferable_rows.csv.gz',dtype={'fund_id':str})
F=pd.read_csv(O/'baseline_fund_portfolio_gate.csv.gz',dtype={'fund_id':str})
G=pd.read_csv(O/'role_baseline_gate.csv');S=pd.read_csv(P['roles']);E=pd.read_csv(O/'event_baseline_gate.csv')
M=pd.read_csv(P['metadata'],dtype={'fund_id':str});U=pd.read_csv(P['pool']);RO=pd.read_csv(P['roster'])
A=pd.read_csv(P['events'],usecols=['event_id','review_cycle','announcement_date','effective_date','isin','RIC'])
A['announcement_date']=pd.to_datetime(A.announcement_date);A['effective_date']=pd.to_datetime(A.effective_date)
RO['ordinary']=RO.stock_type&RO.listed_at_month_end&~RO.preference_name_flag&~(RO.instrument.fillna('')+' '+RO.ticker.fillna('')).str.contains(r'\b(?:PREF|PREFERENS|BTA|BTR|INL|IL|RTS|RIGHT|REDEMPTION|WARRANT)\b',case=False,regex=True)
X=pd.read_csv(O/'fund_exclusions.csv',dtype={'fund_id':str})
recon=[];missing=[];scope=[];invalid=[];reviewscope=[]
for review,ss in S[S.event_id.isin(E.event_id)].groupby('review'):
 y=int(review[:4]);q=ss.q0.iloc[0];pm=(y-1)*100+10 if review.endswith('H1')else y*100+4
 rr=RO[RO.month.eq(pm)&RO.ordinary].copy();rr=rr[~rr.duplicated('isin',keep=False)&rr.industry.notna()&rr.company_code.notna()].set_index('isin')
 cur=U[U.review.eq(review)].copy();unique=cur[cur.same_instrument_RIC_count.eq(1)].set_index('isin');ambiguous=set(cur.loc[cur.same_instrument_RIC_count.gt(1),'isin'])
 mm=M[M.quarter.eq(q)&M.n_instr.gt(0)].copy();badlegal=set(mm.loc[mm.fund_isin.notna()&mm.duplicated('fund_isin',keep=False),'fund_id'])
 mm=mm[mm.fund_isin.notna()&~mm.fund_id.isin(badlegal)&mm.company.notna()];b=mm.label.fillna('');mm['family_original_label']=b.str.contains(r'stockholm benchmark|omxsb|\bsbx',regex=True)
 mm['family_simple']=mm.family_original_label & ~b.str.contains(r';|\||msci|omrx|solactive|bloomberg|\bex\b|procent|carnegie|hfrx|[0-9]+\s*%',regex=True)
 reviewscope.append(dict(review=review,q0=q,original_family_label_funds=int(mm.family_original_label.sum()),simple_family_funds=int(mm.family_simple.sum()),compound_or_other_excluded=int((mm.family_original_label&~mm.family_simple).sum())))
 mm=mm.set_index('fund_id');zz=H[H.quarter.eq(q)].copy()
 zz['invalid']=zz.duplicated(['fund_id','isin'],keep=False)|zz.qty.isna()|zz.mv.isna()|zz.qty.lt(0)|zz.mv.lt(0)|~np.isfinite(zz.qty)|~np.isfinite(zz.mv)
 for e in E[E.review.eq(review)].itertuples():
  roles=ss[ss.event_id.eq(e.event_id)];targets=set(';'.join(roles.aliases).split(';'));badids=set(X.loc[X.event_id.eq(e.event_id),'fund_id'])
  badrows=zz[zz.fund_id.isin(badids)&zz.invalid&zz['isin'].isin(set(rr.index)|targets)]
  for row in badrows.itertuples():invalid.append(dict(review=review,event_id=e.event_id,fund_id=row.fund_id,isin=row.isin,quantity=row.qty,mv=row.mv,duplicate_pair=bool(len(zz[(zz.fund_id==row.fund_id)&(zz['isin']==row.isin)])>1)))
  intervals=((A.announcement_date.le(e.pre_end)&A.effective_date.ge(e.pre_start))|(A.announcement_date.le(e.post_end)&A.effective_date.ge(e.post_start)))&A.event_id.ne(e.event_id)
  changed=A[intervals|A.review_cycle.eq(review)];changedisin=set(changed['isin'].dropna());changedcompany=set(U.loc[U.ric.isin(changed.RIC.dropna()),'company_code'])|set(rr.loc[rr.index.isin(changedisin),'company_code'])
  for s in roles.itertuples():
   alias=s.aliases.split(';');rawown=zz[zz['isin'].isin(alias)&zz.qty.gt(0)&zz.mv.gt(0)&~zz.invalid].copy();rawown=rawown[~rawown.duplicated('fund_id',keep=False)]
   rawown=rawown.merge(mm[['family_original_label','family_simple']],left_on='fund_id',right_index=True)
   fam=rawown[rawown.family_original_label];simp=fam[fam.family_simple]
   scope.append(dict(event_id=e.event_id,review=review,role=s.role,original_label_baseline_owners=len(fam),simple_label_baseline_owners=len(simp),original_label_target_mv=fam.mv.sum(),simple_label_target_mv=simp.mv.sum(),simple_share_target_mv=simp.mv.sum()/fam.mv.sum()if fam.mv.sum()>0 else np.nan))
   gg=G[(G.event_id.eq(e.event_id))&G.role.eq(s.role)].iloc[0]
   ff=F[F.event_id.eq(e.event_id)&F.role.eq(s.role)]
   for f in ff.itertuples():
    z=zz[zz.fund_id.eq(f.fund_id)&zz.qty.gt(0)&zz.mv.gt(0)&~zz.invalid].copy()
    ordinary=z[z['isin'].isin(rr.index)].copy();ordinary=ordinary.merge(rr[['industry','company_code','instrument']],left_on='isin',right_index=True)
    sameissuer=ordinary.company_code.eq(s.company_code);sameindustry=ordinary.industry.eq(gg.industry)&~sameissuer
    change=(ordinary.company_code.isin(changedcompany)|ordinary['isin'].isin(changedisin))&~sameissuer&~sameindustry
    den=ordinary[~sameissuer&~sameindustry&~change].copy()
    def cause(row):
     if row['isin'] in ambiguous:return 'multiple_RICs_for_exact_ISIN'
     if row['isin'] not in unique.index:return 'no_unique_exact_link_in_current_review_pool'
     if unique.loc[row['isin'],'company_code']!=row.company_code:return 'dated_issuer_disagreement'
     return 'mapped'
    den['cause']=den.apply(cause,axis=1)if len(den)else pd.Series(dtype=str)
    dv=float(den.mv.sum());nv=float(den.loc[den.cause.eq('mapped'),'mv'].sum())
    rec=dict(event_id=e.event_id,review=review,role=s.role,group=f.group,fund_id=f.fund_id,all_positive_transferable_mv=float(z.mv.sum()),outside_verified_prior_Stockholm_ordinary_mv=float(z.loc[~z['isin'].isin(rr.index),'mv'].sum()),verified_prior_ordinary_mv=float(ordinary.mv.sum()),excluded_sameissuer_mv=float(ordinary.loc[sameissuer,'mv'].sum()),excluded_sameindustry_mv=float(ordinary.loc[sameindustry,'mv'].sum()),excluded_peer_indexevent_mv=float(ordinary.loc[change,'mv'].sum()),denominator_mv=dv,mapped_mv=nv,denominator_error=dv-f.peer_capital_denominator,mapped_error=nv-f.peer_capital_mapped,coverage=nv/dv if dv else 0)
    for c in ['multiple_RICs_for_exact_ISIN','no_unique_exact_link_in_current_review_pool','dated_issuer_disagreement']:rec[c+'_mv']=float(den.loc[den.cause.eq(c),'mv'].sum())
    recon.append(rec)
    for row in den[den.cause.ne('mapped')].itertuples():missing.append(dict(event_id=e.event_id,review=review,role=s.role,group=f.group,fund_id=f.fund_id,isin=row.isin,instrument=row.instrument,company_code=row.company_code,industry=row.industry,mv=row.mv,share_denominator=row.mv/dv,cause=row.cause))
re=pd.DataFrame(recon);mi=pd.DataFrame(missing);sc=pd.DataFrame(scope);rs=pd.DataFrame(reviewscope);iv=pd.DataFrame(invalid).drop_duplicates()
re.to_csv(O/'independent_capital_reconciliation.csv.gz',index=False,compression='gzip');mi.to_csv(O/'unmapped_peer_capital_ledger.csv.gz',index=False,compression='gzip');sc.to_csv(O/'benchmark_scope_by_role.csv',index=False);rs.to_csv(O/'benchmark_scope_by_review.csv',index=False);iv.to_csv(O/'invalid_baseline_position_ledger.csv',index=False)
# The same fund/position can recur across many focal stocks. Deduplicate here for a
# descriptive missing-name list; never claim these records are independent evidence.
top=mi.drop_duplicates(['review','fund_id','isin']).groupby(['review','group','isin','instrument','cause']).agg(mv_across_funds=('mv','sum'),funds=('fund_id','nunique')).reset_index().sort_values('mv_across_funds',ascending=False)
top.to_csv(O/'largest_unmapped_peer_positions.csv',index=False)
W=pd.read_csv(O/'frozen_peer_weights.csv.gz');ws=W.groupby(['event_id','role','group']).weight.sum()
targets=G.set_index(['event_id','role'])
own_issuer=sum(row.peer_company==targets.loc[(row.event_id,row.role),'company_code']for row in W.itertuples())
sameindustry=sum(row.peer_industry==targets.loc[(row.event_id,row.role),'industry']for row in W.itertuples())
assert re.denominator_error.abs().max()<1e-3 and re.mapped_error.abs().max()<1e-3
assert abs(ws-1).max()<1e-12 and own_issuer==0 and sameindustry==0
assert not E.baseline_pass.any()
out=dict(audited_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),denominator_max_error=float(re.denominator_error.abs().max()),mapped_max_error=float(re.mapped_error.abs().max()),weight_sum_max_error=float(abs(ws-1).max()),own_issuer_peer_rows=int(own_issuer),same_industry_peer_rows=int(sameindustry),return_data_read=False,all_checks_pass=True,denominator_definition='Valid positive baseline transferable rows on prior dated Stockholm ordinary-share roster, excluding target issuer, same industry, and fixed peer indexevent exclusions. No global fund NAV denominator. Foreign-incorporated Stockholm-listed ordinary shares remain part of Swedish-market portfolios.',outside_universe_caution='Outside-verified-ordinary rows may include foreign listings, bonds or other securities; they are NOT denominator capital. The data screen does not relabel them all foreign.',scope='Original ownership-family label includes mixed benchmark mandates. Current simple-family design is narrower and target-specific. This baseline audit does not estimate change in ownership.',repeat_caution='Fund-role records overlap heavily; their sums and quantiles are coverage diagnostics only, not independent observations.',coverage_quantiles_by_group=re.groupby('group').coverage.quantile([0,.25,.5,.75,1]).unstack().to_dict('index'),simple_family_funds_range=[int(rs.simple_family_funds.min()),int(rs.simple_family_funds.max())],original_family_label_funds_range=[int(rs.original_family_label_funds.min()),int(rs.original_family_label_funds.max())],role_family_zero_by_role=G.groupby('role').family_target_capital.apply(lambda x:int(x.eq(0).sum())).to_dict(),scope_addition_zero_original=int(sc[sc.role.eq('event')].original_label_baseline_owners.eq(0).sum()),scope_addition_zero_simple=int(sc[sc.role.eq('event')].simple_label_baseline_owners.eq(0).sum()),invalid_ordinary_position_unique_records=len(iv.drop_duplicates(['review','fund_id','isin'])))
(O/'INDEPENDENT_AUDIT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out,indent=2,ensure_ascii=False))
