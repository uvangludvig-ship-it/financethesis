"""Exploratory public-announcement execution comparison, not an executable fund backtest.

Run with an environment containing pandas, numpy, scipy and pyarrow.
Outputs only event-derived summaries; raw licensed daily prices are not exported.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/omxsb_execution_followup_20261102/timing'
PLAN = json.loads((OUT / 'PLAN_LOCK.json').read_text())
SEED = PLAN['seed']
E = pd.read_csv(ROOT/'output/omxsb_replication_2007/events_car.csv', parse_dates=['AD','ED'])
IX = pd.read_csv(ROOT/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv', parse_dates=['date'])
CAL = pd.DatetimeIndex(IX.loc[(IX.ric=='.OMXSBGI') & IX.close.notna(),'date'].sort_values().unique())
POS = {d:i for i,d in enumerate(CAL)}
M = IX.pivot(index='date',columns='ric',values='close').reindex(CAL).pct_change(fill_method=None)
PX = pd.read_parquet(ROOT/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet',
    columns=['ric','date','totret','close','bid','ask'], filters=[('ric','in',list(E.RIC.dropna().unique()))])
PX['date'] = pd.to_datetime(PX.date)
assert not PX.duplicated(['ric','date']).any(), 'Ambiguous daily price rows'
BY = {ric:g.set_index('date').sort_index().reindex(CAL) for ric,g in PX.groupby('ric')}
FLAGS = pd.read_csv(ROOT/'output/omxsb_replication_2007/mechanisms/step1_deletion_flags.csv')
FLAGGED = set(FLAGS.loc[FLAGS.flagged.astype(str).str.lower().eq('true'),'event_id'])

def compound(r):
    r=np.asarray(r,float)
    if not len(r) or not np.isfinite(r).all() or (r<=-1).any():return np.nan
    return float(np.prod(1+r)-1)

def halfspread(row):
    b,a=row.get('bid',np.nan),row.get('ask',np.nan)
    if not (np.isfinite(b) and np.isfinite(a) and 0<b<=a):return np.nan
    return (a-b)/(a+b)*10000

rows=[]; checks=[]
for e in E.itertuples():
    a,b=POS.get(e.AD),POS.get(e.ED)
    base=dict(event_id=e.event_id,review=e.review_cycle,RIC=e.RIC,company=e.company,
        type=e.type,AD=e.AD,ED=e.ED,year=e.AD.year,flagged_deletion=e.event_id in FLAGGED,
        source_url=e.source_url,verification=e.verification)
    if a is None or b is None or e.RIC not in BY:
        for delay in [1,2]:rows.append(dict(**base,delay=delay,status='missing_calendar_or_RIC'))
        continue
    p=BY[e.RIC]; tr=p.totret/100.0
    # Reproduce the legacy additive return without filling any missing observation.
    for index,col in [('.OMXSBGI','tot'),('.OMXSGI','tot_gi')]:
        rr=tr.iloc[a-1:b+2]; mm=M[index].iloc[a-1:b+2]
        valid=(a>=1 and b+1<len(CAL) and rr.notna().all() and mm.notna().all())
        calc=float((rr-mm).sum()*100) if valid else np.nan
        old=getattr(e,col,np.nan)
        checks.append(dict(event_id=e.event_id,benchmark=index,legacy_column=col,
            recomputed=calc,legacy=old,difference=calc-old if np.isfinite(calc) and pd.notna(old) else np.nan))
    for delay in [1,2]:
        start=a+delay; end=b-1
        r=dict(**base,delay=delay,early_date=CAL[start] if start<len(CAL) else pd.NaT,
            late_date=CAL[end],holding_days=end-start)
        if end<=start:
            rows.append(dict(**r,status='no_positive_tradable_interval'));continue
        stock=tr.iloc[start+1:end+1]; bm=M['.OMXSBGI'].iloc[start+1:end+1]
        sr,br=compound(stock),compound(bm)
        r['missing_stock_days']=int(stock.isna().sum());r['missing_index_days']=int(bm.isna().sum())
        if not (np.isfinite(sr) and np.isfinite(br)):
            rows.append(dict(**r,status='invalid_or_missing_total_return'));continue
        sign=1.0 if e.type=='addition' else -1.0
        path=sign*(np.cumprod(1+stock.to_numpy())-np.cumprod(1+bm.to_numpy()))*100
        gross=sign*(sr-br)*100
        h0,h1=halfspread(p.iloc[start]),halfspread(p.iloc[end])
        quotediff=h0-h1
        # 1SEK at the early close: early stock vs benchmark for additions; reversed for deletions.
        rows.append(dict(**r,status='ok',gross_pp=gross,stock_total_return_pct=sr*100,
            benchmark_total_return_pct=br*100,additive_signed_car_pp=sign*float((stock-bm).sum())*100,
            signed_price_change_pct=sign*(p.close.iloc[end]/p.close.iloc[start]-1)*100
                if p.close.iloc[start]>0 and p.close.iloc[end]>0 else np.nan,
            max_absolute_path_pp=float(np.max(np.abs(path))),worst_path_pp=float(np.min(path)),
            best_path_pp=float(np.max(path)),large_daily_return_flag=bool((np.abs(stock)>0.5).any()),
            early_halfspread_bps=h0,late_halfspread_bps=h1,incremental_halfspread_bps=quotediff,
            quote_adjusted_pp=gross-quotediff/100 if np.isfinite(quotediff) else np.nan,
            net_10bps_pp=gross-.10,net_25bps_pp=gross-.25,net_50bps_pp=gross-.50))

D=pd.DataFrame(rows)
D.to_csv(OUT/'event_comparisons.csv',index=False)
C=pd.DataFrame(checks);C.to_csv(OUT/'replication_checks.csv',index=False)
dif=C.difference.dropna()
assert len(dif)>0 and float(dif.abs().max())<1e-7, 'Legacy CAR mismatch needs investigation'
D.groupby(['type','delay','status']).size().rename('N').reset_index().to_csv(OUT/'coverage.csv',index=False)

def signflip(x):
    x=np.asarray(x,float);n=len(x);obs=abs(x.mean())
    if n<=20:
        count=0;size=1<<n
        for start in range(0,size,8192):
            k=np.arange(start,min(start+8192,size),dtype=np.uint32)
            signs=((k[:,None]>>np.arange(n,dtype=np.uint32))&1)*2.0-1
            count+=int((np.abs(signs@x/n)>=obs-1e-12).sum())
        return count/size
    rng=np.random.default_rng(SEED);count=0;size=99999
    for start in range(0,size,8192):
        k=min(8192,size-start);s=rng.choice([-1,1],size=(k,n))
        count+=int((np.abs(s@x/n)>=obs-1e-12).sum())
    return (count+1)/(size+1)

def summarize(d,label,metric='gross_pp'):
    d=d.dropna(subset=[metric]);v=d.groupby('review')[metric].mean()
    n=len(v)
    if n<2:return dict(sample=label,metric=metric,N=len(d),G=n)
    m=float(v.mean());se=float(v.std(ddof=1)/np.sqrt(n));q=float(t.ppf(.975,n-1))
    loo=(v.sum()-v)/(n-1)
    return dict(sample=label,metric=metric,N=len(d),G=n,issuers=d.RIC.nunique(),mean_review_pp=m,
        ci_low_pp=m-q*se,ci_high_pp=m+q*se,p_signflip=signflip(v.values),
        mean_event_pp=d[metric].mean(),median_event_pp=d[metric].median(),
        event_sd_pp=d[metric].std(ddof=1),negative_event_share=(d[metric]<0).mean(),
        worst_review_pp=v.min(),best_review_pp=v.max(),loo_review_min_pp=loo.min(),loo_review_max_pp=loo.max(),
        median_holding_days=d.holding_days.median(),median_peak_absolute_path_pp=d.max_absolute_path_pp.median(),
        max_peak_absolute_path_pp=d.max_absolute_path_pp.max(),large_daily_return_events=int(d.large_daily_return_flag.sum()))

ok=D[D.status.eq('ok')].copy();summary=[];rev_rows=[]
for ty in ['addition','deletion']:
    for name,years in [('primary2017_2025',(2017,2025)),('earlier2007_2016',(2007,2016)),('partial2026',(2026,2026))]:
        g=ok[ok.type.eq(ty)&ok.year.between(*years)&ok.delay.eq(1)]
        label=f'{ty}_{name}_ADplus1'
        if len(g):
            summary.append(summarize(g,label))
            rr=g.groupby('review').agg(N=('event_id','size'),gross_pp=('gross_pp','mean'),mean_holding_days=('holding_days','mean')).reset_index();rr['sample']=label;rev_rows.append(rr)
        if name=='primary2017_2025':
            for penalty in [10,25,50]:summary.append(summarize(g,label,f'net_{penalty}bps_pp'))
            summary.append(summarize(g,label+'_quotes_subset','quote_adjusted_pp'))
            if ty=='deletion':summary.append(summarize(g[~g.flagged_deletion],label+'_exclude_legacy_flags'))
            paired=set(g.event_id)&set(ok.loc[ok.type.eq(ty)&ok.year.between(*years)&ok.delay.eq(2),'event_id'])
            for de in [1,2]:
                z=ok[ok.event_id.isin(paired)&ok.delay.eq(de)]
                summary.append(summarize(z,f'{ty}_{name}_paired_ADplus{de}'))

S=pd.DataFrame(summary);S.to_csv(OUT/'summary.csv',index=False)
pd.concat(rev_rows,ignore_index=True).to_csv(OUT/'review_comparisons.csv',index=False)
stats=dict(completed_at_utc=datetime.now(timezone.utc).isoformat(),plan_recorded_at_utc=PLAN['recorded_at_utc'],
    plan_sha256=hashlib.sha256((OUT/'PLAN_LOCK.json').read_bytes()).hexdigest(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    legacy_cells_checked=len(dif),max_abs_legacy_difference_pp=float(dif.abs().max()),
    new_effects_exploratory=True,full_portfolio_or_actual_execution=False,
    outputs=[p.name for p in OUT.glob('*.csv')])
(OUT/'RUN.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
print(S[['sample','metric','N','G','mean_review_pp','ci_low_pp','ci_high_pp','p_signflip']].to_string(index=False))
print(json.dumps(stats,ensure_ascii=False))
