import os
from pathlib import Path
import pandas as pd,numpy as np,json,re,itertools,hashlib
from scipy.stats import t
import statsmodels.api as sm
O=Path(__file__).resolve().parent;R=Path(os.environ.get('FINANCETHESIS_REPO', str(Path(__file__).resolve().parents[3])))
paths=[O/x for x in ['decomp_fund_roles.csv.gz','decomp_event_groups.csv','decomp_results.csv','decomp_fund_groups.csv','fund_metadata_classification.csv','event_ownership.csv','security_role_gate.csv']];before={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
L=pd.read_csv(paths[0],dtype={'fund_id':str});E=pd.read_csv(paths[1]);V=pd.read_csv(paths[2]);G=pd.read_csv(paths[3],dtype={'fund_id':str});M=pd.read_csv(paths[4],dtype={'fund_id':str});Q=pd.read_csv(paths[5]);S=pd.read_csv(paths[6]);M['label']=M.label.fillna('<missing>');md=M.set_index(['quarter','fund_id'])
assert not L.duplicated(['event_id','role','fund_id']).any()
assert L.groupby(['event_id','fund_id']).role.nunique().eq(4).all()
assert L.groupby(['event_id','fund_id']).group.nunique().eq(1).all()
assert not G.duplicated(['review','fund_id']).any()
# Fixed prequarter classifier independently implements the text specification.
def classify(x):
 omx=any(z in x.label for z in ['stockholm benchmark','omxsb'])or bool(re.search(r'\bsbx',x.label))
 if omx:
  tokens=['index','indexnära','exponering','etf','xact','passiv','access'];return 'OMXSB_index_named'if any(z in str(x.fund_name).lower()for z in tokens)else 'OMXSB_other_named'
 if x.valid_H_pre:return 'broad_H'
 if x.broad:return 'other_broad_Sweden'
 return 'other_or_unknown'
meta_bad=[]
for x in G.itertuples():
 a,b=md.loc[(x.q0,x.fund_id)],md.loc[(x.q1,x.fund_id)]
 if not(a.n_instr>0 and b.n_instr>0 and a.label==b.label and pd.notna(a.fund_isin)and a.fund_isin==b.fund_isin and classify(a)==x.group):meta_bad.append((x.review,x.fund_id))
assert not meta_bad
# Independent collision check on ALL nonempty reports, before any benchmark/name selection.
collision_records=[]
for rev,g in G.groupby('review'):
 q0,q1=g.iloc[0].q0,g.iloc[0].q1
 badids=set()
 for q in [q0,q1]:
  mm=M[M.quarter.eq(q)&M.n_instr.gt(0)&M.fund_isin.notna()]
  dd=mm[mm.duplicated('fund_isin',keep=False)]
  badids|=set(dd.fund_id)
  for z in dd.itertuples():collision_records.append(dict(review=rev,quarter=q,fund_id=z.fund_id,fund_isin=z.fund_isin))
 assert not(set(g.fund_id)&badids),'A duplicate legal-fund identity survived.'
mg=G.set_index(['review','fund_id']).group.to_dict();assert all(mg[(r,f)]==g for r,f,g in L[['review','fund_id','group']].itertuples(index=False,name=None))
# Rebuild each binary from source FI rows, not the saved group totals.
ids=set(S.aliases.str.split(';').explode());raw=[]
cols=['ISIN-kod_instrument','Fond_institutnummer','Kvartalsslut','Antal','Marknadsvärde_instrument','Tillgångsslag_enligt_LVF_5_kap']
for c in pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=cols,dtype={'Fond_institutnummer':str},chunksize=300000):
 raw.append(c[c['ISIN-kod_instrument'].isin(ids)])
H=pd.concat(raw);hu=H.groupby(['ISIN-kod_instrument','Fond_institutnummer','Kvartalsslut']).Antal.sum(min_count=1).to_dict();hbad=H[H.Antal.isna()|H.Antal.lt(0)|~H['Tillgångsslag_enligt_LVF_5_kap'].eq('ÖverlåtbartVärdepapper')|(H.Antal.gt(0)&~H.Marknadsvärde_instrument.gt(0))];bk=set(hbad[['ISIN-kod_instrument','Fond_institutnummer','Kvartalsslut']].itertuples(index=False,name=None));sl=S.set_index(['event_id','role']).to_dict('index')
raw_mismatch=0;raw_invalid=0
for x in L.itertuples():
 s=sl[(x.event_id,x.role)]
 for col,dt in [('own_before',s['q0']),('own_after',s['q1'])]:
  keys=[(i,x.fund_id,dt)for i in s['aliases'].split(';')];raw_invalid+=int(any(k in bk for k in keys));raw_mismatch+=int(int(sum(hu.get(k,0)for k in keys)>0)!=getattr(x,col))
assert raw_invalid==0 and raw_mismatch==0
# From disjoint fund roles reconstruct groups and ALL, including empty group cells.
metrics=['own_before','own_after','new','left'];B=L.groupby(['event_id','group','role'])[metrics].sum();All=L.groupby(['event_id','role'])[metrics].sum();rec=[]
for x in E.itertuples():
 if x.group=='ALL':z=All.loc[x.event_id]
 else:
  try:z=B.loc[(x.event_id,x.group)]
  except KeyError:z=pd.DataFrame(0,index=['event','c1','c2','c3'],columns=metrics)
 z=z.reindex(['event','c1','c2','c3'],fill_value=0);ev=z.loc['event'];co=z.loc[['c1','c2','c3']].sum()/3
 event_change=ev.own_after-ev.own_before;control_change=co.own_after-co.own_before
 counts=L[(L.event_id==x.event_id)&L.role.eq('event')];n=len(counts)if x.group=='ALL'else int(counts.group.eq(x.group).sum())
 d=dict(event_id=x.event_id,type=x.type,review=x.review,group=x.group,N_funds=n,event_pre=ev.own_before,event_post=ev.own_after,control_pre=co.own_before,control_post=co.own_after,event_new=ev.new,control_new=co.new,event_left=ev.left,control_left=co.left,event_change=event_change,control_change=control_change,matched_change=event_change-control_change,matched_rate=100*(event_change-control_change)/n if n else np.nan);rec.append(d)
A=pd.DataFrame(rec);J=A.merge(E,on=['event_id','group'],suffixes=('_ind','_prod'),validate='one_to_one');cs=[x for x in A.columns if x not in ['event_id','type','review','group']];errors={x:float((J[x+'_ind']-J[x+'_prod']).abs().max())for x in cs};assert max(errors.values())<1e-10
T=A[A.group=='ALL'].set_index('event_id').matched_change;Z=A[A.group!='ALL'].groupby('event_id').matched_change.sum();identity_error=float((T-Z).abs().max());assert identity_error<1e-10
cells=[]
for v in V.itertuples():
 q=A[(A.type==v.type)&(A.group==v.group)];m=q.groupby('review').matched_change.mean();g=len(m);fit=sm.OLS(m.to_numpy(),np.ones((g,1))).fit();ci=fit.conf_int()[0];mu=float(fit.params[0]);sg=np.array(list(itertools.product([-1.,1.],repeat=g)));draw=sg*m.to_numpy();ts=draw.mean(1)/(draw.std(1,ddof=1)/np.sqrt(g));pv=float((abs(ts)>=abs(mu/fit.bse[0])-1e-12).mean())
 own=dict(N=len(q),G=g,mean_owner_count_difference=mu,ci_low=float(ci[0]),ci_high=float(ci[1]),p_exact_signflip=pv,median_funds=float(q.N_funds.median()),min_funds=int(q.N_funds.min()),max_funds=int(q.N_funds.max()))
 for c in ['event_pre','control_pre','event_change','control_change']:own[c]=float(q.groupby('review')[c].mean().mean())
 dif={k:float(z-getattr(v,k))for k,z in own.items()};cells.append(dict(type=v.type,group=v.group,passed=all(abs(z)<1e-10 for z in dif.values()),independent=own,differences=dif))
assert all(c['passed']for c in cells)
hr=A[A.group=='broad_H'].merge(Q[Q.support=='post'][['event_id','matched_post']],on='event_id',validate='one_to_one');herr=float((hr.matched_rate-hr.matched_post).abs().max());assert herr<1e-10
ratio={}
for ty in ['addition','deletion']:
 v=V[V.type==ty].set_index('group');den=v.loc['ALL','mean_owner_count_difference'];num=v.loc[['OMXSB_index_named','OMXSB_other_named'],'mean_owner_count_difference'].sum();ratio[ty]=dict(numerator=float(num),denominator=float(den),point_ratio=float(num/den),interpretation='descriptive ratio of signed mean owner-count differences; not confidence bound or causal share')
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths};assert before==after,'Inputs changed during audit; rerun.'
out=dict(all_12_cells_pass=True,ledger_rows=len(L),events=L.event_id.nunique(),binary_source_mismatches=raw_mismatch,invalid_source_quantities_retained=raw_invalid,metadata_or_group_failures=meta_bad,full_report_collision_rows=collision_records,retained_duplicate_fund_ISIN_pairs=0,event_group_numeric_max_errors=errors,additivity_max_error=identity_error,H_event_rate_max_error=herr,cells=cells,benchmark_family_point_concentration=ratio,input_hashes=after)
(O/'independent_decomp_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k not in ['cells','input_hashes']},indent=2))
