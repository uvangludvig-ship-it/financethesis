"""One predeclared descriptive FI decomposition. Never edits repo inputs.
Run: /tmp/omxsb-audit-venv/bin/python describe_fund_changes.py --repo /Users/ludviguvang/dev/financethesis
"""
from pathlib import Path
import os
import argparse,json,hashlib
import numpy as np,pandas as pd
from scipy.stats import t
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3])));args=p.parse_args()
R=args.repo;O=R/'output/omxsb_extension_20261031/ownership';OUT=Path(__file__).parent
obs=pd.read_csv(O/'ownership_observations.csv');obs=obs[obs.main_common_sample].copy()
assert len(obs)==217 and obs.review_cycle.nunique()==14
f=pd.read_csv(O/'fi_fund_event_observations.csv.gz');f=f[f.window.eq('event')&f.event_id.isin(obs.event_id)].copy()
assert not f.duplicated(['event_id','fund_id']).any()
f=f.merge(obs[['event_id','type','review_cycle','factor','denominator','company']],on='event_id',validate='many_to_one')
valid=f[~f.unit_invalid].copy()
valid['delta_q']=valid.quantity_after_raw-valid.factor*valid.quantity_before_raw
checks=[]
for col,mask in [('FI_all_matched_delta_pp',pd.Series(True,index=valid.index)),('FI_Nordnet_documented_delta_pp',valid.is_documented_Nordnet),('FI_Nordea_metadata_delta_pp',valid.is_metadata_Nordea),('FI_original14_delta_pp',valid.is_original14)]:
 x=(100*valid[mask].delta_q/valid[mask].denominator).groupby(valid.loc[mask,'event_id']).sum().reindex(obs.event_id,fill_value=0)
 y=obs.set_index('event_id')[col].reindex(x.index)
 assert np.allclose(x,y,rtol=1e-9,atol=1e-9),col
 checks.append({'check':col,'max_abs_error':float((x-y).abs().max())})
meta=pd.read_csv(O/'fi_fund_quarter_metadata.csv')
reported=set(zip(meta.Fond_institutnummer.astype(int),meta.Kvartalsslut))
assert all((int(x.fund_id),x.before) in reported and (int(x.fund_id),x.after) in reported for x in f.itertuples())
assert not ((valid.quantity_before_raw.gt(0)&valid.ISIN_before.isna())|(valid.quantity_after_raw.gt(0)&valid.ISIN_after.isna())).any()
flags=pd.read_csv(OUT/'new_quantity_flags.csv')
bad=set(zip(flags.event_id,flags.fund_id))
valid['extra_unit_exclusion']=[(e,fi) in bad for e,fi in zip(valid.event_id,valid.fund_id)]
removed=valid[valid.extra_unit_exclusion].copy();removed.to_csv(OUT/'additional_excluded_fund_pairs.csv',index=False)
valid=valid[~valid.extra_unit_exclusion].copy()
d=pd.read_csv(OUT/'denominator_audit.csv');d=d[d.new_unit_exclusion.isna()|d.new_unit_exclusion.eq('')].copy()
ids=set(d.event_id);assert len(ids)==216
valid=valid[valid.event_id.isin(ids)].copy();events=obs[obs.event_id.isin(ids)].copy()
valid=valid.merge(d[['event_id','fi_price','mcap','mcap_date','mcap_age_days','price_agreeing_funds','class_value_fraction']],on='event_id',validate='many_to_one')
valid['before_adjusted']=valid.factor*valid.quantity_before_raw
valid['delta_company_pp']=100*valid.delta_q*valid.fi_price/valid.mcap
valid['before_quantity_valued_after_company_pp']=100*valid.before_adjusted*valid.fi_price/valid.mcap
# Above is value of BEFORE shares at AFTER prices / AFTER capital, not historical before ownership.
valid['group']=np.select([valid.is_documented_Nordnet,valid.is_metadata_Nordea],['Nordnet_documented','Nordea_metadata'],'Other_FI_mixed')
tol=1e-8
valid['position_change']=np.select([valid.quantity_before_raw.eq(0)&valid.quantity_after_raw.gt(0),valid.quantity_before_raw.gt(0)&valid.quantity_after_raw.eq(0),valid.delta_q.gt(tol),valid.delta_q.lt(-tol)],['opened','closed','existing_increased','existing_decreased'],'unchanged')
valid.to_csv(OUT/'fund_event_changes_company_normalized.csv.gz',index=False,compression='gzip')
rows=[]
for ev in events.itertuples():
 for group in ['Nordnet_documented','Nordea_metadata','Other_FI_mixed','All_observed_FI']:
  z=valid[valid.event_id.eq(ev.event_id)]
  if group!='All_observed_FI':z=z[z.group.eq(group)]
  v=z.delta_company_pp
  row=dict(event_id=ev.event_id,RIC=ev.RIC,company=ev.company,type=ev.type,review_cycle=ev.review_cycle,before=ev.before,after=ev.after,group=group,net_pp=v.sum(),positive_fund_net_changes_pp=v.clip(lower=0).sum(),negative_fund_net_changes_pp=v.clip(upper=0).sum(),recorded_fund_pairs=len(z),funds_positive=int(v.gt(tol).sum()),funds_negative=int(v.lt(-tol).sum()),funds_preexisting=int(z.quantity_before_raw.gt(0).sum()),funds_opened=int(z.position_change.eq('opened').sum()),funds_closed=int(z.position_change.eq('closed').sum()))
  for part in ['opened','closed','existing_increased','existing_decreased','unchanged']:row[part+'_pp']=z.loc[z.position_change.eq(part),'delta_company_pp'].sum()
  assert np.isclose(row['net_pp'],row['positive_fund_net_changes_pp']+row['negative_fund_net_changes_pp'])
  assert np.isclose(row['net_pp'],sum(row[a+'_pp'] for a in ['opened','closed','existing_increased','existing_decreased','unchanged']))
  rows.append(row)
e=pd.DataFrame(rows);e.to_csv(OUT/'event_group_decomposition.csv',index=False)
# Net decomposition from exhaustive, non-overlapping groups exactly reproduces observed FI totals.
a=e[e.group.ne('All_observed_FI')].groupby('event_id').net_pp.sum();b=e[e.group.eq('All_observed_FI')].set_index('event_id').net_pp
assert np.allclose(a.sort_index(),b.sort_index())
metrics=['net_pp','positive_fund_net_changes_pp','negative_fund_net_changes_pp','opened_pp','existing_increased_pp','existing_decreased_pp','closed_pp']
rev=e.groupby(['type','group','review_cycle'])[metrics].mean().reset_index();rev.to_csv(OUT/'review_group_decomposition.csv',index=False)
summary=[]
for (ty,g),z in e.groupby(['type','group']):
 for m in metrics:
  x=rev[rev.type.eq(ty)&rev.group.eq(g)][m].to_numpy();G=len(x);mean=x.mean();se=x.std(ddof=1)/np.sqrt(G);h=t.ppf(.975,G-1)*se
  summary.append(dict(type=ty,group=g,metric=m,review_weighted_mean=mean,ci95_low=mean-h,ci95_high=mean+h,event_weighted_mean=z[m].mean(),N=len(z),G=G,distinct_RIC=z.RIC.nunique()))
s=pd.DataFrame(summary);s.to_csv(OUT/'summary_review_weighted.csv',index=False)
# Pre-existing position counts for independently defined tracker series.
counts=[];ratios=[];rng=np.random.default_rng(20261101)
for (ty,g),z in e[e.group.isin(['Nordnet_documented','Nordea_metadata'])].groupby(['type','group']):
 vz=valid[valid.type.eq(ty)&valid.group.eq(g)]
 counts.append(dict(type=ty,group=g,N=len(z),prezero_events=int(vz.quantity_before_raw.eq(0).sum()),prepositive_events=int(vz.quantity_before_raw.gt(0).sum()),opened=int(vz.position_change.eq('opened').sum()),closed=int(vz.position_change.eq('closed').sum()),positive_delta=int(vz.delta_q.gt(tol).sum()),negative_delta=int(vz.delta_q.lt(-tol).sum()),zero_delta=int(vz.delta_q.abs().le(tol).sum())))
 r=rev[rev.type.eq(ty)&rev.group.eq(g)];num=r.opened_pp.to_numpy();den=r.positive_fund_net_changes_pp.to_numpy();idx=rng.integers(0,len(r),(19999,len(r)));bd=den[idx].mean(axis=1);bn=num[idx].mean(axis=1)
 br=np.divide(bn,bd,out=np.full_like(bn,np.nan),where=bd>0);ratio=num.mean()/den.mean() if den.mean()>0 else np.nan
 ratios.append(dict(type=ty,group=g,ratio_opened_share_of_positive_changes=ratio,ci95_low=np.nanquantile(br,.025) if np.isfinite(br).any() else np.nan,ci95_high=np.nanquantile(br,.975) if np.isfinite(br).any() else np.nan,bootstrap_draws=19999,nonpositive_bootstrap_denominator=int((bd<=0).sum()),G=len(r),note='Ratio of equal-review average opened increments to all positive fund net increments; no mechanical demand attribution.'))
pd.DataFrame(counts).to_csv(OUT/'tracker_preownership_counts.csv',index=False);pd.DataFrame(ratios).to_csv(OUT/'tracker_opened_share_ratios.csv',index=False)
# Same-event alignment; simultaneous net sums do not establish transactions between groups.
align=[]
for ty,z in e.groupby('type'):
 wide=z.pivot(index='event_id',columns='group',values='net_pp')
 for x,y in [('Nordnet_documented','Nordea_metadata'),('Nordnet_documented','Other_FI_mixed')]:
  a,b=wide[x],wide[y]
  align.append(dict(type=ty,group_1=x,group_2=y,N=len(wide),both_positive=int((a.gt(tol)&b.gt(tol)).sum()),both_negative=int((a.lt(-tol)&b.lt(-tol)).sum()),opposite=int(((a.gt(tol)&b.lt(-tol))|(a.lt(-tol)&b.gt(tol))).sum()),at_least_one_zero=int((a.abs().le(tol)|b.abs().le(tol)).sum())))
pd.DataFrame(align).to_csv(OUT/'same_event_alignment.csv',index=False)
validation=dict(locked_events=217,company_unit_valid_events=len(events),additions=int(events.type.eq('addition').sum()),deletions=int(events.type.eq('deletion').sum()),reviews=events.review_cycle.nunique(),unique_RIC=events.RIC.nunique(),retained_explicit_fund_event_rows=len(valid),additional_excluded_fund_pairs=len(removed),source_invalid_main_pairs=int(f.unit_invalid.sum()),source_agreement=checks,group_accounting='passed',balanced_reports='passed',positive_rows_have_ISIN='passed',source_panel_observed_funds_range=[int(events.FI_valid_unit_funds.min()),int(events.FI_valid_unit_funds.max())],zero_before_explicit_rows=int(valid.quantity_before_raw.eq(0).sum()),zero_after_explicit_rows=int(valid.quantity_after_raw.eq(0).sum()),all_zero_implicit_rows_note='Both-zero non-tracker rows omitted from source ledger. All sums include their exact zero contribution; denominators never count only rows in the sparse ledger.')
(OUT/'validation.json').write_text(json.dumps(validation,indent=2))
paths=[O/'ownership_observations.csv',O/'fi_fund_event_observations.csv.gz',O/'fi_fund_quarter_metadata.csv',O/'validated_isin_aliases.json',O/'fi_halfyear_instrument_rows.csv.gz',R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet']
(OUT/'source_hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2))
print(json.dumps(validation,indent=2))
print('\nNET\n'+s[s.metric.eq('net_pp')].to_string(index=False))
print('\nDECOMPOSITION OTHER\n'+s[s.group.eq('Other_FI_mixed')].to_string(index=False))
print('\nPREOWNERSHIP\n'+pd.DataFrame(counts).to_string(index=False))
print('\nOPENED RATIOS\n'+pd.DataFrame(ratios).to_string(index=False))
print('\nALIGNMENT\n'+pd.DataFrame(align).to_string(index=False))
