"""Independent arithmetic check of the already locked v1; no additional strategies."""
from pathlib import Path
import hashlib, json, itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT=Path('/Users/ludviguvang/dev/financethesis')
HERE=Path(__file__).resolve().parent
BASE=ROOT/'output/omxsb_execution_followup_20261102/timing'
D=pd.read_csv(BASE/'event_comparisons.csv',parse_dates=['early_date','late_date'])
S=pd.read_csv(BASE/'summary.csv')
IX=pd.read_csv(ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
I=IX[IX.ric.eq('.OMXSBGI')].set_index('date')['close'].dropna()
P=D[D.year.between(2017,2025)&D.delay.eq(1)&D.status.eq('ok')]
raw=pd.read_parquet(ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',
    columns=['ric','date','totret'],filters=[('ric','in',list(P.RIC.unique()))])
raw['date']=pd.to_datetime(raw.date)
by={k:g.set_index('date').totret for k,g in raw.groupby('ric')}
errors=[]
for r in P.itertuples():
    dates=I.index[(I.index>r.early_date)&(I.index<=r.late_date)]
    x=by[r.RIC].reindex(dates).to_numpy()/100
    assert np.isfinite(x).all() and (x>-1).all()
    stock=np.expm1(np.log1p(x).sum())
    benchmark=I.loc[r.late_date]/I.loc[r.early_date]-1
    independent=(1 if r.type=='addition' else -1)*(stock-benchmark)*100
    errors.append(independent-r.gross_pp)
res={'status':'v1 arithmetic and exact locked comparisons independently checked; not causal/execution validation',
     'N_raw_recomputed':len(errors),'max_abs_gross_difference_pp':float(np.max(np.abs(errors))),
     'samples':[],'input_hashes':{}}
for ty in ['addition','deletion']:
    a=P[P.type.eq(ty)];v=a.groupby('review').gross_pp.mean().values
    model=sm.OLS(v,np.ones((len(v),1))).fit()
    obs=abs(v.sum());count=0
    for bits in itertools.product((-1,1),repeat=len(v)):
        count+=abs(np.dot(bits,v))>=obs-1e-10
    pval=count/(2**len(v))
    original=S[S['sample'].eq(ty+'_primary2017_2025_ADplus1')&S.metric.eq('gross_pp')].iloc[0]
    res['samples'].append(dict(type=ty,N=len(a),reviews=len(v),mean_pp=float(model.params[0]),
        ci95=model.conf_int()[0].tolist(),exact_signflip=float(pval),
        mean_difference=float(model.params[0]-original.mean_review_pp),
        p_difference=float(pval-original.p_signflip)))
for p in [BASE/'PLAN_LOCK.json',BASE/'event_comparisons.csv',BASE/'summary.csv',ROOT/'code/build/omxsb_execution_timing_20261102.py']:
    res['input_hashes'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
res['primary_missing_rows']=D[D.year.between(2017,2025)&D.delay.eq(1)&D.status.ne('ok')][['event_id','company','RIC','status']].to_dict('records')
(HERE/'timing_v1_arithmetic_validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ['input_hashes','primary_missing_rows']},indent=2))
