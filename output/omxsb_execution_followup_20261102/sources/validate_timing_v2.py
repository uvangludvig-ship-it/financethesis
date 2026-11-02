"""Independent verification of frozen v2 accounting, without changing its strategy."""
from pathlib import Path
import json,hashlib,itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
R=Path('/Users/ludviguvang/dev/financethesis');H=Path(__file__).resolve().parent
B=R/'output/omxsb_execution_followup_20261102/timing/v2_announced'
D=pd.read_csv(B/'event_comparisons.csv',parse_dates=['AD','ED','early_date','late_date','unwind_date'])
I=pd.read_csv(R/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv',parse_dates=['date'])
I=I[I.ric.eq('.OMXSBGI')].set_index('date').close.dropna().sort_index()
raw=pd.read_parquet(R/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',
    columns=['ric','date','totret'],filters=[('ric','in',list(D.RIC.dropna().unique()))])
raw['date']=pd.to_datetime(raw.date)
by={r:g.set_index('date').totret for r,g in raw.groupby('ric')}
def sf(ric,start,end):
    dates=I.index[(I.index>start)&(I.index<=end)]
    a=by[ric].reindex(dates).to_numpy()/100
    assert np.isfinite(a).all() and (a>-1).all()
    return float(np.exp(np.log1p(a).sum()))
def ix(start,end):return float(I.loc[end]/I.loc[start])
errors=[];cancel=[]
ok=D[D.status.eq('ok')]
for row in ok.itertuples():
    if row.no_entry_due_to_cancellation:
        gross=0.0
    else:
        s,t=row.early_date,row.late_date
        u=row.unwind_date if row.cancelled else t
        if row.type=='addition':
            a=sf(row.RIC,s,u)*ix(u,t);b=ix(s,t)
        else:
            a=ix(s,u)*sf(row.RIC,u,t);b=sf(row.RIC,s,t)
        gross=(a-b)*100
        assert abs(a-row.early_terminal_factor)<1e-10
        assert abs(b-row.baseline_terminal_factor)<1e-10
    errors.append(gross-row.gross_pp)
    if row.cancelled:cancel.append({'id':row.event_id,'delay':row.delay,'max_difference_pp':abs(gross-row.gross_pp)})
res={'N_cells':len(errors),'max_abs_raw_accounting_difference_pp':float(np.max(np.abs(errors))),
     'cancellation_checks':cancel,'primary_inference':[],'hashes':{}}
for ty in ['addition','deletion']:
    a=ok[ok.type.eq(ty)&ok.delay.eq(1)];v=a.groupby('review').gross_pp.mean().values
    m=sm.OLS(v,np.ones((len(v),1))).fit();obs=abs(v.sum());count=0
    for bits in itertools.product((-1,1),repeat=len(v)):
        count+=abs(np.dot(bits,v))>=obs-1e-10
    res['primary_inference'].append({'type':ty,'N':len(a),'G':len(v),'mean':float(m.params[0]),
        'CI':m.conf_int()[0].tolist(),'p_signflip':float(count/(2**len(v)))})
res['coverage']=D.groupby(['type','delay','cancelled','status']).size().reset_index(name='N').to_dict('records')
res['limitations']=['Initial-notice history beyond known cancellations not exhaustively verified',
    'Missing return/transaction endpoint rows remain nonrandom potential selection',
    'Equal-review per-trade gross terminal wealth contrast, not measured auction execution or full fund return',
    'Review inference assumes independent review shocks/sign symmetry; repeat issuers and exploratory design remain']
for p in [R/'code/build/omxsb_execution_announced_20261102.py',B/'event_comparisons.csv',B/'summary.csv']:
    res['hashes'][str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
(H/'timing_v2_arithmetic_validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ['coverage','hashes','limitations']},indent=2))
