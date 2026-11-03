"""Independent arithmetic rebuild: aggregate raw FI quantities by component first,
then value with one price; compare every matched component and review statistic.
Does not import run.py or use its calculated quantities/outcomes as inputs."""
from pathlib import Path
import os,json,math,datetime
import pandas as pd,numpy as np
from scipy.stats import t
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO','/Users/ludviguvang/dev/financethesis'));OWN=R/'output/omxsb_mechanism_frontier_20261102/ownership';DQ=R/'output/omxsb_open_questions_20261102/demand_quarter'
support=pd.read_csv(O/'fund_support.csv',dtype={'excluded_fund_ids':str}).set_index('event_id');s=pd.read_csv(OWN/'security_role_gate.csv');s=s[s.event_id.isin(support.index)]
f=pd.read_csv(OWN/'decomp_fund_roles.csv.gz',dtype={'fund_id':str});f=f[f.event_id.isin(support.index)]
g=pd.read_csv(O/'security_feasibility_gate.csv').set_index(['review','ric']);ids=set(s.aliases.str.split(';').explode());dates=set(s.q0)|set(s.q1)
rename={'ISIN-kod_instrument':'isin','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id','Antal':'qty','Marknadsvärde_instrument':'value','Valuta':'currency','Tillgångsslag_enligt_LVF_5_kap':'asset_type'}
parts=[]
for z in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=list(rename),dtype={'Fond_institutnummer':str},chunksize=250000):
 z=z.rename(columns=rename);parts.append(z[z['isin'].isin(ids)&z.quarter.isin(dates)])
h=pd.concat(parts);h.qty=pd.to_numeric(h.qty,errors='coerce');h.value=pd.to_numeric(h.value,errors='coerce')
p=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',columns=['ric','date','mcap']);p=p.sort_values(['ric','date']).drop_duplicates(['ric','date'],keep='last')
meta=pd.read_csv(DQ/'raw_fund_report_metadata.csv',dtype={'Fond_institutnummer':str}).set_index(['Fond_institutnummer','Kvartalsslut'])
cache={};role_results=[];zero_checks=0;fund_group_identity=pd.read_csv(OWN/'decomp_fund_groups.csv',dtype={'fund_id':str}).set_index(['review','fund_id'])
for (review,ric),z in s.groupby(['review','ric']):
 x=z.iloc[0];raw=h[h['isin'].isin(x.aliases.split(';'))&h.quarter.isin([x.q0,x.q1])]
 quantities=raw.groupby(['fund_id','quarter']).qty.agg(lambda x: math.fsum(x)).unstack(fill_value=0)
 vals=raw[raw.quarter.eq(x.q1)&raw.currency.eq('SEK')&raw.qty.gt(0)&raw.value.gt(0)&raw.asset_type.eq('ÖverlåtbartVärdepapper')]
 price=float(np.median((vals.value/vals.qty).to_numpy()));cap=float(p[p.ric.eq(ric)&p.date.le(pd.Timestamp(x.q1))&p.mcap.gt(0)].iloc[-1].mcap)
 cache[(review,ric)]=(quantities,price,cap)
for x in s.itertuples():
 original=f[f.event_id.eq(x.event_id)&f.role.eq(x.role)];excluded=set(str(support.loc[x.event_id,'excluded_fund_ids']).split(';'));z=original[~original.fund_id.isin(excluded)]
 assert len(z)==support.loc[x.event_id,'retained_funds'];qt,price,cap=cache[(x.review,x.ric)];factor=float(g.loc[(x.review,x.ric),'factor'])
 for fid in z.fund_id:
  assert meta.loc[(fid,x.q0),'actual_instrument_rows']>0 and meta.loc[(fid,x.q1),'actual_instrument_rows']>0
  assert fund_group_identity.loc[(x.review,fid),'q0']==x.q0
 def quantity(fid,date):return float(qt.loc[fid,date]) if fid in qt.index and date in qt.columns else 0.
 z=z.copy();z['qb']=[quantity(a,x.q0) for a in z.fund_id];z['qa']=[quantity(a,x.q1) for a in z.fund_id]
 assert np.array_equal(z.qb.gt(0),z.own_before.eq(1));assert np.array_equal(z.qa.gt(0),z.own_after.eq(1));zero_checks+=int(z.qb.eq(0).sum()+z.qa.eq(0).sum())
 for grp in list(sorted(f.group.unique()))+['ALL','OMXSB_family']:
  zz=z if grp=='ALL' else (z[z.group.str.startswith('OMXSB_')] if grp=='OMXSB_family' else z[z.group.eq(grp)])
  # Different algebra to primary: separate aggregate after and split-adjusted before capital.
  masks={'new':zz.qb.eq(0)&zz.qa.gt(0),'continuing':zz.qb.gt(0)&zz.qa.gt(0),'exiting':zz.qb.gt(0)&zz.qa.eq(0)}
  for comp,mask in masks.items():
   v=zz[mask];dq=math.fsum(v.qa)-factor*math.fsum(v.qb);role_results.append(dict(event_id=x.event_id,review=x.review,type=x.type,role=x.role,group=grp,component=comp,value=100*price*dq/cap))
v=pd.DataFrame(role_results);wide=v.pivot(index=['event_id','review','type','group','component'],columns='role',values='value');wide['matched']=wide['event']-(wide['c1']+wide['c2']+wide['c3'])/3
out=wide.reset_index().pivot(index=['event_id','review','type','group'],columns='component',values='matched').reset_index();out['total']=out['new']+out['continuing']+out['exiting'];out['preexisting']=out['continuing']+out['exiting'];out['new_minus_preexisting']=out['new']-out['preexisting']
main=pd.read_csv(O/'event_component_results.csv');j=out.merge(main,on=['event_id','review','type','group'],validate='1:1');errors={c:float((j[c]-j['matched_'+c]).abs().max()) for c in ['new','continuing','exiting','total','preexisting','new_minus_preexisting']};assert max(errors.values())<1e-10
review=out.groupby(['type','group','review'])[['new','continuing','exiting','total','preexisting','new_minus_preexisting']].mean().reset_index();summ=pd.read_csv(O/'summary.csv');max_summary_err=0.
for (ty,grp),zz in review.groupby(['type','group']):
 for c in ['new','continuing','exiting','total','preexisting','new_minus_preexisting']:
  a=summ[summ.type.eq(ty)&summ.group.eq(grp)&summ.metric.eq('matched_'+c)].iloc[0];y=zz[c].to_numpy();mean=math.fsum(y)/len(y);se=math.sqrt(math.fsum((y-mean)**2)/(len(y)-1)/len(y));half=t.ppf(.975,len(y)-1)*se
  max_summary_err=max(max_summary_err,abs(a.mean_pp-mean),abs(a.se_pp-se),abs(a.ci95_low-(mean-half)),abs(a.ci95_high-(mean+half)))
assert max_summary_err<1e-10
cov=pd.read_csv(O/'component_covariance.csv');z=cov[cov.type.eq('addition')].pivot(index='row',columns='column',values='covariance_of_mean').reindex(index=['matched_new','matched_continuing','matched_exiting'],columns=['matched_new','matched_continuing','matched_exiting']);w=np.array([1,-1,-1]);se_cov=math.sqrt(w@z.to_numpy()@w);a=summ[summ.is_primary].iloc[0];assert abs(a.se_pp-se_cov)<1e-12
res=dict(verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),event_component_rows_checked=len(j),zero_endpoint_checks_in_nonempty_reports=zero_checks,max_event_component_error_pp=errors,max_summary_error_pp=max_summary_err,primary_SE_reproduced_from_joint_covariance=se_cov,all_checks_pass=True,scope='Independent code and aggregate-first arithmetic on same underlying sources, not an independent data collection or second analyst.')
(O/'independent_validation.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
