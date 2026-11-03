from pathlib import Path
import pandas as pd,numpy as np,json,datetime
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');D=pd.read_csv(O/'normalized_fund_role_contributions.csv.gz',dtype={'fund_id':str});D['count']=D.component.map({'new':1,'exiting':-1,'continuing':0,'neither':0});D['entry_count']=D.component.eq('new').astype(int);D['exit_count']=-D.component.eq('exiting').astype(int)
G=pd.read_csv(R/'output/omxsb_mechanism_frontier_20261102/ownership/decomp_fund_groups.csv',dtype={'fund_id':str});D=D.merge(G[['review','fund_id','company']],on=['review','fund_id'],validate='m:1');D.company=D.company.fillna('<missing>')
def contrast(tab,values,keys):
 x=tab.groupby(keys+['role'])[values].sum();x=x.unstack('role').fillna(0)
 for v in values:x[(v,'matched')]=x[(v,'event')]-sum(x[(v,k)] for k in ['c1','c2','c3'])/3
 return x.loc[:,[(v,'matched') for v in values]].set_axis(values,axis=1).reset_index()
rows=[]
for grp in list(sorted(D.group.unique()))+['ALL','OMXSB_family']:
 z=D if grp=='ALL' else (D[D.group.str.startswith('OMXSB_')] if grp=='OMXSB_family' else D[D.group.eq(grp)])
 x=contrast(z,['count','entry_count','exit_count','pp'],['event_id','review','type']);x['group']=grp;rows.append(x)
e=pd.concat(rows);e.to_csv(O/'same_support_event_counts_capital.csv',index=False);v=e.groupby(['type','group','review'])[['count','entry_count','exit_count','pp']].mean().reset_index();a=v.groupby(['type','group'])[['count','entry_count','exit_count','pp']].mean().reset_index();a['N_events']=[e[e.type.eq(x.type)&e.group.eq(x.group)].event_id.nunique() for x in a.itertuples()];a['G_reviews']=[v[v.type.eq(x.type)&v.group.eq(x.group)].review.nunique() for x in a.itertuples()];a.to_csv(O/'same_support_counts_capital.csv',index=False)
# Every legal pre-quarter company on every retained event; absent contribution is zero in observed fixed support.
base=D[['event_id','review','type']].drop_duplicates().merge(pd.DataFrame({'company':sorted(D.company.unique())}),how='cross')
cm=contrast(D,['count','pp'],['event_id','review','type','company']);cm=base.merge(cm,on=['event_id','review','type','company'],how='left');cm[['count','pp']]=cm[['count','pp']].fillna(0)
rv=cm.groupby(['type','review','company'])[['count','pp']].mean().reset_index();cs=rv.groupby(['type','company'])[['count','pp']].mean().reset_index();cs.to_csv(O/'all_company_contributions.csv',index=False)
# Both accounting decompositions must equal the original primary totals.
primary=pd.read_csv(O/'summary.csv');errs=[]
for typ in a.type.unique():
 target=float(primary[primary.type.eq(typ)&primary.group.eq('ALL')&primary.metric.eq('matched_total')].mean_pp.iloc[0]);gval=float(a[a.type.eq(typ)&a.group.eq('ALL')].pp.iloc[0]);cval=float(cs[cs.type.eq(typ)].pp.sum());errs.extend([abs(target-gval),abs(target-cval)]);assert abs(target-gval)<1e-12 and abs(target-cval)<1e-12
result=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),post_primary_descriptive_only=True,company_names=int(cs.company.nunique()),max_capital_accounting_error=max(errs),no_omission_tests=True)
(O/'descriptive_validation.json').write_text(json.dumps(result,indent=2));print(a.to_string(index=False));print(cs[cs.type.eq('addition')].sort_values('pp',ascending=False).head(8).to_string(index=False));print(result)
