"""Independent accounting, zero-source and inference checks of ownership outputs."""
from pathlib import Path
import argparse,json,re,subprocess,hashlib,sys
import numpy as np
import pandas as pd
from scipy.stats import t
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--out',type=Path);args=p.parse_args();root=args.repo;out=args.out or root/'output/omxsb_extension_20261031/ownership'
a=pd.read_csv(out/'ap_snapshot_resolution.csv').fillna({'source_file':''});o=pd.read_csv(out/'ownership_observations.csv');r=pd.read_csv(out/'ownership_results.csv');aliases=json.load(open(out/'validated_isin_aliases.json'));bad=pd.read_csv(out/'fi_halfyear_ambiguous_quantity_rows.csv');f=pd.read_csv(out/'fi_fund_event_observations.csv.gz')
assert len(o)==460 and o.event_id.nunique()==230
assert not o.duplicated(['event_id','window']).any()
q=o[o.main_common_sample];assert q.valid.all() and q.review_cycle.nunique()==14
for suffix in ['before_raw','after_raw','delta_pp']:
 assert np.allclose(q['AP3_AP4_sum_'+suffix],q['AP3_'+suffix]+q['AP4_'+suffix])
 assert np.allclose(q['FI_all_matched_'+suffix],q['FI_Nordnet_documented_'+suffix]+q['FI_other_than_Nordnet_'+suffix])
assert (q.AP3_after_raw+q.AP4_after_raw<=q.denominator).all()
assert (q.FI_all_matched_after_raw<=q.denominator).all()
assert (q.FI_original14_available==14).all()
assert len(bad)==198 and bad.Antal.lt(0).all()
assert not bad.Fond_institutnummer.isin([60320,60293]).any()
assert f.ambiguous_signed_or_missing_quantity.sum()>0
# Recompute primary APsum event-weighted CR1 interval independently.
for direction in ['addition','deletion']:
 z=q[q.type.eq(direction)];x=z.AP3_AP4_sum_delta_pp;mu=x.mean();sc=(x-mu).groupby(z.review_cycle).sum();G=len(sc);se=np.sqrt(G/(G-1)*(sc**2).sum()/len(x)**2)
 rr=r[(r['sample']=='main_common')&(r.direction==direction)&(r.group=='AP3_AP4_sum')].iloc[0]
 assert np.allclose([mu,se,mu-t.ppf(.975,G-1)*se,mu+t.ppf(.975,G-1)*se],[rr.mean_pp,rr.se_review_cluster,rr.ci95_low,rr.ci95_high])
# Original full list: a logical zero cannot coexist with its ordinary ISIN in source text.
texts={};checks=[]
for row in a[a.logical_zero].itertuples():
 hits=[]
 for file in str(row.source_file).split(' | '):
  if file not in texts:
   result=subprocess.run(['pdftotext','-layout',str(root/file),'-'],capture_output=True,text=True,check=True)
   texts[file]=re.sub(r'\s+','',result.stdout.upper())
  hits.extend(i for i in aliases[row.RIC] if i in texts[file])
 checks.append(dict(fund=row.fund,RIC=row.RIC,date=row.date,ordinary_ISIN_found_in_original_text=';'.join(sorted(set(hits))),source_file=row.source_file,scope='Exact ISIN negative check; does not by itself prove absence in older no-ISIN lists'))
checks=pd.DataFrame(checks);checks.to_csv(out/'logical_zero_original_PDF_checks.csv',index=False)
hit=checks.ordinary_ISIN_found_in_original_text.ne('')
summary=dict(accounting_and_ci_checks='passed',logical_zero_rows=len(checks),original_PDFs_checked=len(texts),zero_ISIN_conflicts=int(hit.sum()),negative_FI_rows=len(bad),excluded_negative_FI_fund_event_windows=int(f.ambiguous_signed_or_missing_quantity.sum()),main_events=len(q),main_reviews=q.review_cycle.nunique())
# Store provenance for both code and exact original data supporting this run.
paths=[root/'code/build/omxsb_ap_prepare.py',root/'code/build/omxsb_ap_ownership.py',root/'code/build/omxsb_ap_validate.py',root/'data/derived/ap/excluded_rows.csv',root/'data/derived/ap/source_checks.csv',root/'data/derived/ap/parse_rejections.csv']+[root/file for file in texts]
checksums={str(v.relative_to(root)):hashlib.sha256(v.read_bytes()).hexdigest() for v in paths};(out/'execution_source_hashes.json').write_text(json.dumps(checksums,indent=2))
(out/'validation_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if hit.any():print(checks[hit].to_string(index=False));sys.exit(2)
