"""Exploratory same-security price association; does not identify causality."""
from pathlib import Path
import argparse, hashlib, json, datetime
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster, cov_cluster_2groups

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--repo',default='/Users/ludviguvang/dev/financethesis')
    pa.add_argument('--out',default=str(Path(__file__).resolve().parent))
    ar=pa.parse_args(); root=Path(ar.repo); out=Path(ar.out); out.mkdir(parents=True,exist_ok=True)
    src=root/'output/omxsb_open_questions_20261102/eligible_rematch/event_paths.csv'
    dec=Path(__file__).with_name('ANALYSIS_DECISIONS.txt')
    record={'source':str(src.relative_to(root)),'sha256':sha(src),'decisions_sha256':sha(dec),
            'script_sha256':sha(Path(__file__)),'run_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    # Publish decision/input record before accessing outcome values.
    (out/'run_input_record.json').write_text(json.dumps(record,indent=2))
    d=pd.read_csv(src)
    assert len(d)==287 and d.event_id.is_unique
    d['pre_balance']=d.precar-d[[f'c{i}_precar' for i in range(1,4)]].mean(axis=1)
    d['size_balance']=d.log_mcap-d[[f'c{i}_log_mcap' for i in range(1,4)]].mean(axis=1)
    cols=['diff3_1','pre_balance','size_balance']
    d['complete']=np.isfinite(d[cols]).all(axis=1)
    two=d.loc[d.complete].groupby('ric').type.nunique()
    d['both_directions']=d.ric.isin(two[two==2].index)
    d[['event_id','ric','issuer','review','type','complete','both_directions']].to_csv(out/'eligibility.csv',index=False)
    q=d[d.complete&d.both_directions].copy()
    q['add']=q.type.eq('addition').astype(float)
    # Panel.car already returns percentage points (see robusthet_hela.py).
    q['y_pp']=q.diff3_1
    q['pre_balance_pp']=q.pre_balance
    # Exact dated Nasdaq ISIN continuity verifies these company-code renamings.
    roster=pd.read_csv(root/'output/omxsb_open_questions_20261102/eligible_pool/review_RIC_control_pool.csv')
    aliases={'HMED':'HNSA','AF':'AFRY','CLNK':'BICO'}
    identity=[]
    for old,new in aliases.items():
        z=roster[roster.company_code.isin([old,new])]
        assert z['isin'].nunique()==1 and z.company_code.nunique()==2
        identity.append(dict(old=old,new=new,isin=z['isin'].iloc[0],source='dated Nasdaq roster',n=len(z)))
    pd.DataFrame(identity).to_csv(out/'issuer_alias_evidence.csv',index=False)
    q['issuer_cluster']=q.issuer.replace(aliases)
    q['w']=1/q.groupby('review').event_id.transform('size')
    q.to_csv(out/'analysis_events.csv',index=False)
    dummies=pd.get_dummies(q[['ric','review']],drop_first=True,dtype=float)
    review=pd.Categorical(q.review).codes; issuer=pd.Categorical(q.issuer_cluster).codes
    G=len(np.unique(review)); J=len(np.unique(issuer)); n=len(q)
    rs=[]; leverages=[]
    for name,controls in [('same_security_review',[]),('primary_pre_balance',['pre_balance_pp','size_balance'])]:
        x=pd.concat([q[['add']+controls],dummies],axis=1)
        x=sm.add_constant(x,has_constant='add')
        sw=np.sqrt(q.w.to_numpy()); X=x.to_numpy()*sw[:,None]; Y=q.y_pp.to_numpy()*sw
        k=X.shape[1]; assert np.linalg.matrix_rank(X)==k
        f=sm.WLS(q.y_pp,x,weights=q.w).fit()
        j=list(x.columns).index('add'); bhat=float(f.params['add'])
        bread=np.linalg.inv(X.T@X); a=(bread@X.T)[j]
        H=X@bread@X.T; h=np.diag(H)
        for eid,hv in zip(q.event_id,h):leverages.append(dict(model=name,event_id=eid,leverage=hv))
        cov_r=cov_cluster(f,review,use_correction=True)
        cov_i=cov_cluster(f,issuer,use_correction=True)
        cov_both,_,_=cov_cluster_2groups(f,review,issuer,use_correction=True)
        se_r=np.sqrt(cov_r[j,j]); t_obs=bhat/se_r
        # Restricted bootstrap under null coefficient=0, same nuisance model.
        X0=np.delete(X,j,axis=1); f0=X0@np.linalg.lstsq(X0,Y,rcond=None)[0]; u0=Y-f0
        gen=np.random.default_rng(20261102)
        signs=gen.choice([-1.,1.],size=(G,9999))
        U=u0[:,None]*signs[review,:]
        bs=a@U; er=U-H@U
        score=np.vstack([(a[review==g,None]*er[review==g]).sum(axis=0) for g in range(G)])
        correction=G/(G-1)*(n-1)/(n-k)
        bse=np.sqrt(correction*np.sum(score**2,axis=0))
        bt=bs/bse
        p_wild=(1+np.sum(np.abs(bt)>=abs(t_obs)))/(len(bt)+1)
        row=dict(model=name,N=n,securities=q.ric.nunique(),issuers=J,reviews=G,rank=k,
                 adds=int(q['add'].sum()),dels=int((1-q['add']).sum()),estimate_pp=bhat,
                 max_leverage=float(h.max()),median_leverage=float(np.median(h)),condition=float(np.linalg.cond(X)),
                 p_wild_review=float(p_wild),wild_draws=len(bt),seed=20261102)
        for lab,cov,df in [('review',cov_r,G-1),('issuer',cov_i,J-1),('two_way',cov_both,min(G,J)-1)]:
            var=float(cov[j,j]); se=np.sqrt(var) if var>=0 else np.nan
            c=stats.t.ppf(.975,df)
            row.update({f'{lab}_variance':var,f'{lab}_se':se,f'{lab}_ci_low':bhat-c*se,
                        f'{lab}_ci_high':bhat+c*se,f'{lab}_p':2*stats.t.sf(abs(bhat/se),df),f'{lab}_df':df})
        rs.append(row)
    pd.DataFrame(rs).to_csv(out/'results.csv',index=False)
    pd.DataFrame(leverages).to_csv(out/'leverage.csv',index=False)
    q.groupby(['ric','issuer','type']).agg(n=('event_id','size'),reviews=('review','nunique')).reset_index().to_csv(out/'security_counts.csv',index=False)
    print(pd.DataFrame(rs)[['model','N','securities','issuers','reviews','estimate_pp','review_ci_low','review_ci_high','p_wild_review','two_way_ci_low','two_way_ci_high','max_leverage']].to_string(index=False))
    print('Excluded:',d.loc[~(d.complete&d.both_directions),['complete','both_directions']].value_counts().to_dict())

if __name__=='__main__':main()
