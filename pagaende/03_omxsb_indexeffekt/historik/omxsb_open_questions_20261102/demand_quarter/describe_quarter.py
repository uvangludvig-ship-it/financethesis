from pathlib import Path
import os
import pandas as pd,numpy as np,json,hashlib
from scipy.stats import t
D=Path(__file__).parent;P=D.parent/'demand';R=Path(os.environ.get('FINANCETHESIS_REPO', Path(__file__).resolve().parents[3]));O=R/'output/omxsb_extension_20261031/ownership'
e=pd.read_csv(D/'events_locked.csv');gate=pd.read_csv(D/'gate_event_checks_resolved.csv');assert gate.gate_reasons.isna().all();assert len(e)==216
h=pd.read_csv(D/'quarter_raw_target_instruments.csv.gz');m=pd.read_csv(D/'raw_fund_report_metadata.csv');b=pd.read_csv(D/'ambiguous_fund_pairs.csv');bad=set(zip(b.event_id,b.fund_id));alias=json.load(open(O/'validated_isin_aliases.json'))
den=pd.read_csv(P/'denominator_audit.csv').set_index('event_id');snap=pd.read_csv(D/'quarter_security_snapshots.csv');reports={dt:set(g.loc[g.actual_instrument_rows.gt(0),'Fond_institutnummer']) for dt,g in m.groupby('Kvartalsslut')};md=m.set_index(['Fond_institutnummer','Kvartalsslut'])
rows=[];coverage=[]
for x in e.itertuples():
 z=h[h['ISIN-kod_instrument'].isin(alias[x.RIC])&h.Kvartalsslut.isin([x.before,x.after])];q=z.groupby(['Fond_institutnummer','Kvartalsslut']).agg(quantity=('Antal','sum'),source_rows=('Antal','size'),ISINs=('ISIN-kod_instrument',lambda s:';'.join(sorted(set(s)))))
 avail=reports[x.before]&reports[x.after];invalid={f for ev,f in bad if ev==x.event_id}&avail;good=avail-invalid
 assert 60320 in good and 60293 in good
 coverage.append(dict(event_id=x.event_id,RIC=x.RIC,review_cycle=x.review_cycle,type=x.type,balanced_nonempty_reports=len(avail),excluded_ambiguous_fund_pairs=len(invalid),retained_fund_pairs=len(good),excluded_funds=';'.join(map(str,sorted(invalid)))))
 for fid in sorted(good):
  qb=q.loc[(fid,x.before),'quantity'] if (fid,x.before) in q.index else 0.;qa=q.loc[(fid,x.after),'quantity'] if (fid,x.after) in q.index else 0.
  assert np.isfinite(qb+qa) and min(qb,qa)>=0
  group='Nordnet_documented' if fid==60320 else ('Nordea_metadata' if fid==60293 else 'Other_FI_mixed')
  rows.append(dict(event_id=x.event_id,RIC=x.RIC,type=x.type,review_cycle=x.review_cycle,fund_id=fid,group=group,before=x.before,after=x.after,before_quantity=qb,after_quantity=qa,before_source_rows=int(q.loc[(fid,x.before),'source_rows']) if (fid,x.before) in q.index else 0,after_source_rows=int(q.loc[(fid,x.after),'source_rows']) if (fid,x.after) in q.index else 0,ISIN_before=q.loc[(fid,x.before),'ISINs'] if (fid,x.before) in q.index else '',ISIN_after=q.loc[(fid,x.after),'ISINs'] if (fid,x.after) in q.index else '',before_logical_zero=(fid,x.before) not in q.index,after_logical_zero=(fid,x.after) not in q.index,factor=x.factor,fi_price_after=den.loc[x.event_id,'fi_price'],company_mcap_after=den.loc[x.event_id,'mcap'],delta_q=qa-x.factor*qb,delta_company_pp=100*(qa-x.factor*qb)*den.loc[x.event_id,'fi_price']/den.loc[x.event_id,'mcap']))
f=pd.DataFrame(rows);f.to_csv(D/'fund_event_quarter_changes.csv.gz',index=False,compression='gzip');cov=pd.DataFrame(coverage);cov.to_csv(D/'coverage.csv',index=False)
rows=[]
for x in e.itertuples():
 for group in ['Nordnet_documented','Nordea_metadata','Other_FI_mixed','All_observed_FI']:
  z=f[f.event_id.eq(x.event_id)];z=z if group=='All_observed_FI' else z[z.group.eq(group)];v=z.delta_company_pp
  rows.append(dict(event_id=x.event_id,RIC=x.RIC,review_cycle=x.review_cycle,type=x.type,group=group,before=x.before,after=x.after,N_fund_pairs=len(z),net_pp=v.sum(),positive_fund_net_changes_pp=v.clip(lower=0).sum(),negative_fund_net_changes_pp=v.clip(upper=0).sum(),positive_funds=int(v.gt(1e-8).sum()),negative_funds=int(v.lt(-1e-8).sum()),zero_funds=int(v.abs().le(1e-8).sum())))
a=pd.DataFrame(rows);assert np.allclose(a.net_pp,a.positive_fund_net_changes_pp+a.negative_fund_net_changes_pp)
g=a[a.group.ne('All_observed_FI')].groupby('event_id').net_pp.sum();allg=a[a.group.eq('All_observed_FI')].set_index('event_id').net_pp;assert np.allclose(g.sort_index(),allg.sort_index())
a.to_csv(D/'event_group_decomposition.csv',index=False)
metrics=['net_pp','positive_fund_net_changes_pp','negative_fund_net_changes_pp'];rev=a.groupby(['type','group','review_cycle'])[metrics].mean().reset_index();rev.to_csv(D/'review_group_decomposition.csv',index=False)
summary=[]
for (ty,group),z in a.groupby(['type','group']):
 r=rev[rev.type.eq(ty)&rev.group.eq(group)]
 for metric in metrics:
  vals=r[metric];G=len(vals);mean=vals.mean();half=t.ppf(.975,G-1)*vals.std(ddof=1)/np.sqrt(G)
  summary.append(dict(type=ty,group=group,metric=metric,review_weighted_mean=mean,ci95_low=mean-half,ci95_high=mean+half,event_weighted_mean=z[metric].mean(),N=len(z),G=G,distinct_RIC=z.RIC.nunique()))
s=pd.DataFrame(summary);s.to_csv(D/'summary_review_weighted.csv',index=False)
check=dict(events=len(e),additions=int(e.type.eq('addition').sum()),deletions=int(e.type.eq('deletion').sum()),reviews=e.review_cycle.nunique(),all_fund_event_pairs=len(f),excluded_pairs=int(cov.excluded_ambiguous_fund_pairs.sum()),balanced_reports_min=int(cov.balanced_nonempty_reports.min()),balanced_reports_max=int(cov.balanced_nonempty_reports.max()),retained_reports_min=int(cov.retained_fund_pairs.min()),retained_reports_max=int(cov.retained_fund_pairs.max()),logical_zero_before=int(f.before_logical_zero.sum()),logical_zero_after=int(f.after_logical_zero.sum()),fund_report_date_pairs=m[m.actual_instrument_rows.gt(0)].shape[0],original_216_sample_unchanged=set(e.event_id)==set(pd.read_csv(P/'event_group_decomposition.csv').event_id),accounting_identities='passed',both_tracker_funds_present_valid_all216=True)
(D/'validation.json').write_text(json.dumps(check,indent=2))
paths=[D/'ANALYSBESLUT.txt',D/'quarter_raw_target_instruments.csv.gz',D/'raw_fund_report_metadata.csv',D/'events_locked.csv',D/'gate_event_checks_resolved.csv',O/'validated_isin_aliases.json',P/'denominator_audit.csv'];(D/'source_hashes.json').write_text(json.dumps({str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},indent=2))
print(json.dumps(check,indent=2));print(s.to_string(index=False));
for ty,z in a[a.group.eq('Other_FI_mixed')].groupby('type'):print(ty,'events_with_both_positive_negative_fund_nets',int((z.positive_funds.gt(0)&z.negative_funds.gt(0)).sum()),'of',len(z))
