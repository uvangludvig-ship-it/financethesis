from pathlib import Path
import pandas as pd,numpy as np,re,json,itertools,hashlib
from scipy.stats import t
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');B=R/'output/omxsb_open_questions_20261102'
S=pd.read_csv(O/'security_role_gate.csv');M=pd.read_csv(O/'fund_metadata_classification.csv',dtype={'fund_id':str});U=pd.read_csv(B/'eligibility/dated_stockholm_instrument_roster.csv')
M['label']=M.label.fillna('<missing>')
H=pd.read_csv(R/'data/derived/fi/fi_holdings_long.csv.gz',usecols=['Tillgångsslag_enligt_LVF_5_kap','Instrumentnamn','ISIN-kod_instrument','Antal','Marknadsvärde_instrument','Kvartalsslut','Fond_institutnummer'],dtype={'Fond_institutnummer':str}).rename(columns={'Tillgångsslag_enligt_LVF_5_kap':'asset_type','Instrumentnamn':'name','ISIN-kod_instrument':'isin','Antal':'qty','Marknadsvärde_instrument':'value','Kvartalsslut':'quarter','Fond_institutnummer':'fund_id'})
for c in ['qty','value']:H[c]=pd.to_numeric(H[c],errors='coerce')
def norm(x):return re.sub(r'[^a-z0-9]','',str(x).lower().replace('å','a').replace('ä','a').replace('ö','o'))
H['name_norm']=H['name'].map(norm);H['ordinary_container']=H.asset_type.eq('ÖverlåtbartVärdepapper')
known_codes=U.groupby('isin').company_code.agg(set).to_dict();known_class=U.groupby('company_code')['isin'].agg(set).to_dict()
def group(x):
 if bool(re.search(r'stockholm benchmark|omxsb|\bsbx',x.label)):
  ni=bool(re.search(r'index|indexnära|exponering|etf|xact|passiv|access',str(x.fund_name),re.I));return'OMXSB_index_named'if ni else'OMXSB_other_named'
 if x.valid_H_pre:return'broad_H'
 if x.broad:return'other_broad_Sweden'
 return'other_or_unknown'
M['decomp_group']=[group(x)for x in M.itertuples()]
GROUPS=['OMXSB_index_named','OMXSB_other_named','broad_H','other_broad_Sweden','other_or_unknown']
meta=[];events=[];ledger=[];screen=[];coverage=[]
for rev,sg in S.groupby('review'):
 a=sg.iloc[0];q0=a.q0;q1=a.q1
 pre=M[(M.quarter==q0)&M.n_instr.gt(0)];post=M[(M.quarter==q1)&M.n_instr.gt(0)].set_index('fund_id')
 fs={x.fund_id:x for x in pre.itertuples()if x.fund_id in post.index and x.label==post.loc[x.fund_id,'label']};funds=set(fs)
 for f,x in fs.items():meta.append(dict(review=rev,fund_id=f,group=x.decomp_group,name=x.fund_name,company=x.company,pre_benchmark=x.benchmark,post_benchmark=post.loc[f,'benchmark'],q0=q0,q1=q1))
 hh=H[H.quarter.isin([q0,q1])&H.fund_id.isin(funds)]
 cache={}
 for ric,zs in sg.groupby('ric'):
  z=zs.iloc[0];ids=set(z.aliases.split(';'));token=norm(re.split(r'\s+',str(z.instrument))[0]);cl=known_class.get(z.company_code,set())-ids
  target=hh[hh['isin'].isin(ids)];bad=target[(~target.ordinary_container)|target.qty.lt(0)|~np.isfinite(target.qty)|((target.qty>0)&(~np.isfinite(target.value)|(target.value<=0)))]
  invalid=set(bad.fund_id)
  for k in bad.itertuples():screen.append(dict(review=rev,ric=ric,fund_id=k.fund_id,quarter=k.quarter,isin=k.isin,instrument=k.name,status='target_quantity_value_or_type_invalid'))
  unknown=hh[hh.ordinary_container&hh.name_norm.str.startswith(token)&~hh['isin'].isin(ids|cl)]if len(token)>=3 else hh.iloc[:0]
  for k in unknown.itertuples():
   codes=known_codes.get(k.isin,set());status='exact_other_issuer'if codes and z.company_code not in codes else'unresolved_same_issuer'
   if status=='unresolved_same_issuer':invalid.add(k.fund_id)
   screen.append(dict(review=rev,ric=ric,fund_id=k.fund_id,quarter=k.quarter,isin=k.isin,instrument=k.name,status=status))
  qty=target.groupby(['fund_id','quarter']).qty.sum(min_count=1).to_dict();cache[ric]=(invalid,qty)
 for eid,ss in sg.groupby('event_id'):
  a=ss.iloc[0]
  if not(ss.q0_supported.all()and ss.q1_supported.all()):coverage.append(dict(event_id=eid,reason='unknown_security_endpoint',kept=False));continue
  valid=funds-set().union(*(cache[x.ric][0]for x in ss.itertuples()))
  if not valid:coverage.append(dict(event_id=eid,reason='no_valid_funds',kept=False));continue
  coverage.append(dict(event_id=eid,reason='',kept=True,funds=len(valid),funds_before_quality=len(funds)))
  obs=[]
  for x in ss.itertuples():
   qt=cache[x.ric][1]
   for f in valid:
    p=int(qt.get((f,q0),0)>0);n=int(qt.get((f,q1),0)>0);obs.append(dict(event_id=eid,review=rev,type=a.type,role=x.role,fund_id=f,group=fs[f].decomp_group,own_before=p,own_after=n,new=int(n==1 and p==0),left=int(n==0 and p==1)))
  df=pd.DataFrame(obs);ledger.extend(obs)
  for grp in GROUPS+['ALL']:
   z=df if grp=='ALL'else df[df.group==grp];cnt=z.groupby('role')[['own_before','own_after','new','left']].sum().reindex(['event','c1','c2','c3'],fill_value=0);cc=cnt.loc[['c1','c2','c3']].mean();ee=cnt.loc['event'];N=z[z.role=='event'].shape[0]
   ec=ee.own_after-ee.own_before;dc=cc.own_after-cc.own_before
   events.append(dict(event_id=eid,review=rev,type=a.type,group=grp,N_funds=N,event_pre=ee.own_before,event_post=ee.own_after,control_pre=cc.own_before,control_post=cc.own_after,event_new=ee.new,control_new=cc.new,event_left=ee.left,control_left=cc.left,event_change=ec,control_change=dc,matched_change=ec-dc,matched_rate=100*(ec-dc)/N if N else np.nan))
 print(rev,'balanced stable funds',len(fs),flush=True)
E=pd.DataFrame(events);E.to_csv(O/'decomp_event_groups.csv',index=False);pd.DataFrame(ledger).to_csv(O/'decomp_fund_roles.csv.gz',index=False,compression='gzip');pd.DataFrame(meta).to_csv(O/'decomp_fund_groups.csv',index=False);pd.DataFrame(screen).drop_duplicates().to_csv(O/'decomp_identity_screen.csv.gz',index=False,compression='gzip');pd.DataFrame(coverage).to_csv(O/'decomp_coverage.csv',index=False)
T=E[E.group=='ALL'].set_index('event_id').matched_change;Z=E[E.group!='ALL'].groupby('event_id').matched_change.sum();assert np.allclose(T.sort_index(),Z.sort_index(),atol=1e-12)
res=[]
for (ty,grp),s in E.groupby(['type','group']):
 y=s.groupby('review').matched_change.mean();G=len(y);mean=y.mean();se=y.std(ddof=1)/np.sqrt(G);half=t.ppf(.975,G-1)*se;obs=abs(mean/se)
 signs=np.array(list(itertools.product([-1.,1.],repeat=G)));D=signs*y.to_numpy();tv=D.mean(1)/(D.std(1,ddof=1)/np.sqrt(G));p=np.mean(abs(tv)>=obs-1e-12)
 lev=s.groupby('review')[['event_pre','control_pre','event_change','control_change']].mean().mean()
 res.append(dict(type=ty,group=grp,N=len(s),G=G,mean_owner_count_difference=mean,ci_low=mean-half,ci_high=mean+half,p_exact_signflip=p,median_funds=s.N_funds.median(),min_funds=s.N_funds.min(),max_funds=s.N_funds.max(),**lev.to_dict()))
A=pd.DataFrame(res);A.to_csv(O/'decomp_results.csv',index=False)
# H percentages must reproduce the separately run H estimate event by event.
Q=pd.read_csv(O/'event_ownership.csv');Q=Q[Q.support=='post'];h=E[E.group=='broad_H'];jj=Q.merge(h,on='event_id');err=float((jj.matched_post-jj.matched_rate).abs().max());assert err<1e-10,err
check={'group_sums_exact':True,'H_event_rate_max_difference':err,'events':len(T),'all_fund_role_rows':len(ledger),'decision_hash':hashlib.sha256((O/'DECOMPOSITION_DECISIONS.txt').read_bytes()).hexdigest()};(O/'decomp_validation.json').write_text(json.dumps(check,indent=2));print(A.to_string(index=False));print(json.dumps(check,indent=2))
