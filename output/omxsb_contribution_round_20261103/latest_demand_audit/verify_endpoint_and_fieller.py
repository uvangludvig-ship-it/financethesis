"""Independent endpoint check and confidence-set inversion verification."""
from pathlib import Path
import json, hashlib, datetime
import pandas as pd
import numpy as np
from scipy.stats import t

O=Path(__file__).resolve().parent
R=Path('/Users/ludviguvang/dev/financethesis')
paths=[R/'output/omxsb_open_questions_20261102/demand_quarter/quarter_raw_target_instruments.csv.gz',
       R/'code/claude_checks/data/runda8_fondagare.csv.gz',R/'code/claude_checks/runda11_resultat/handelser.csv']
raw=pd.read_csv(paths[0],low_memory=False)
fi=raw[(raw.Fond_institutnummer==60824)&(raw.Kvartalsslut=='2023-06-30')&(raw['ISIN-kod_instrument']=='SE0017769995')]
lseg=pd.read_csv(paths[1],low_memory=False)
ls=lseg[(lseg['Fund Name']=='Swedbank Robur Access Sverige')&(lseg.event_id=='OMXSB-2023H1-02')&(lseg.snap=='efter')&(lseg['Fund Holdings Filing Date']=='2023-06-30')]
assert len(fi)==1 and len(ls)==1
ratio=ls['Fund Shares Held (Adjusted)'].astype(float).iloc[0]/fi.Antal.iloc[0]
assert np.isclose(ratio,1.10518654870449)
E=pd.read_csv(paths[2]);Q=pd.read_csv(O/'r11_full_fieller_diagnostic.csv')
records=[]
for z in Q.itertuples():
    d=E[(E.type==z.type)&(E.per==z.period)&E.fonddata&~E.split&E.D.notna()].dropna(subset=[z.window])
    # Reconstruct the scalar cluster t-statistic for H0: mean(Y-mD)=0.
    # This checks Fieller-set membership directly, independently of its quadratic roots.
    grid=[-1e6,-1e4,-2000,-1000,-100,-10,0,1,10,100,1000,10000,1e6,z.ratio]
    for b in [z.lo,z.hi]:
        if np.isfinite(b):grid.extend([b,b-1e-5*max(1,abs(b)),b+1e-5*max(1,abs(b))])
    for m in grid:
        v=d[z.window]-m*d.D;mean=v.mean();score=(v-mean).groupby(d.review).sum()
        var=(len(score)/(len(score)-1))*np.sum(score.to_numpy()**2)/(len(d)**2)
        stat=mean*mean-t.ppf(.975,len(score)-1)**2*var
        quad=z.A*m*m+z.B*m+z.C
        error=abs(stat-quad)/max(1,abs(stat),abs(quad))
        assert error<1e-9
        if abs(stat)>1e-7:assert (stat<=0)==(quad<=0)
        records.append(dict(type=z.type,period=z.period,window=z.window,test_ratio=m,relative_inversion_error=error))
pd.DataFrame(records).to_csv(O/'fieller_inversion_checks.csv',index=False)
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),BIOG_endpoint=dict(event='OMXSB-2023H1-02',fund_id=60824,date='2023-06-30',raw_FI_matching_rows=len(fi),raw_LSEG_matching_rows=len(ls),LSEG_over_FI_ratio=float(ratio),cause_not_established=True),
    scalar_inversion_checks=len(records),max_relative_inversion_error=max(r['relative_inversion_error'] for r in records),
    inputs={str(p):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths})
(O/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
