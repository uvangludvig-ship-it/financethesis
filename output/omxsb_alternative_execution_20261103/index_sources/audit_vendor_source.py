"""Audit delivered index source alignment; no stock returns or demand outcomes."""
from pathlib import Path
import pandas as pd,json,datetime
O=Path(__file__).resolve().parent;P=O/'private';res={};SETS={}
for date in ['20231130','20231201']:
 f={i:pd.read_csv(P/f'repaired_index_pilot_{date}_field{i}.csv')for i in range(1,5)}
 sets={i:set(v['Constituent RIC'].dropna())for i,v in f.items()};SETS[date]=sets
 names=f[1].set_index('Constituent RIC')['Constituent Name'].to_dict()
 weights=pd.to_numeric(f[2]['Weight percent'],errors='coerce')
 res[date]={'rows':{str(i):len(v)for i,v in f.items()},'valid_RIC_count':{str(i):int(v['Constituent RIC'].notna().sum())for i,v in f.items()},'duplicated_RIC':{str(i):int(v['Constituent RIC'].duplicated().sum())for i,v in f.items()},'name_only':[{k:names.get(k)}for k in sorted(sets[1]-sets[2])],'weight_only':sorted(sets[2]-sets[1]),'shares_vs_weights_same_RIC':sets[3]==sets[2],'weights_sum':float(weights.sum())if weights.notna().any()else None,'weight_finite':int(weights.notna().sum()),'shares_positive':int(f[3]['Index Shares'].gt(0).sum()),'returned_date_values':f[4]['Date'].dropna().astype(str).unique().tolist()}
res['observed_name_membership_changes']={'added':sorted(SETS['20231201'][1]-SETS['20231130'][1]),'deleted':sorted(SETS['20231130'][1]-SETS['20231201'][1])}
res['observed_weight_membership_changes']={'added':sorted(SETS['20231201'][2]-SETS['20231130'][2]),'deleted':sorted(SETS['20231130'][2]-SETS['20231201'][2])}
E=pd.read_csv('/Users/ludviguvang/dev/financethesis/data/input/omxsb/omxsb_events_with_ric_2007_2026.csv',usecols=['review_cycle','RIC','type']);E=E[E.review_cycle.eq('2023H2')]
res['frozen_release_changes']=E.to_dict('records')
res['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(P/'source_alignment_audit.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
