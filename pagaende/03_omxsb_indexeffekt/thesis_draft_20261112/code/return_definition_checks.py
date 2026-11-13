"""Check return conventions and fixed-cohort paths using authorized price inputs.

This is a disclosed post-result specification check, not a change to the frozen
primary estimator. Only aggregate results are written.
Usage: python return_definition_checks.py /path/to/thesis_final /path/to/output
"""
from pathlib import Path
import sys, json
import numpy as np
import pandas as pd
from scipy import stats

src, out = map(Path, sys.argv[1:3])
out.mkdir(parents=True, exist_ok=True)
ix = pd.read_csv(src/'data/prices/index_levels_daily_2004_2026.csv', parse_dates=['date'])
idx = ix[(ix.ric == '.OMXSBGI') & ix.close.notna()].sort_values('date').set_index('date').close
cal = idx.index
market = idx.div(idx.shift(1)).sub(1).to_numpy()
pos = {d: i for i, d in enumerate(cal)}
px = pd.read_csv(src/'data/prices/stock_prices_daily_2004_2026.csv.gz', parse_dates=['date'])
px = px[px.date.isin(cal)].sort_values(['ric', 'date'])
ret = {}
for ric, g in px.groupby('ric'):
    g = g.set_index('date')
    fallback = g.close.ffill().div(g.close.ffill().shift(1)).sub(1)
    ret[ric] = g.totret.div(100).where(g.totret.notna(), fallback).reindex(cal).to_numpy()
e = pd.read_csv(src/'data/events/omxsb_changes_with_car_2007_2026.csv', parse_dates=['AD','ED','effective_date'])
flags = pd.read_csv(src/'data/events/omxsb_deletion_flags_2007_2026.csv')
excluded = set(flags.loc[flags.flag_offer | flags.flag_delist, 'event_id'])
e = e[~e.event_id.isin(excluded)].copy()

def interval(y, groups):
    y = np.asarray(y, float)
    codes = pd.factorize(groups)[0]
    n, G = len(y), len(np.unique(codes))
    mean = y.mean()
    scores = np.bincount(codes, weights=y-mean)
    se = np.sqrt(G/(G-1)*np.dot(scores, scores)/n**2)
    crit = stats.t.ppf(.975, G-1)
    return dict(n=n, G=G, mean=mean, se=se, lower=mean-crit*se, upper=mean+crit*se)

def sample_groups(d):
    yield 'All', d
    for period in sorted(d.period.unique()):
        yield period.replace('–','-'), d[d.period == period]
    yield '2007-2016', d[d.effective_date.dt.year <= 2016]
    yield '2017-2026', d[d.effective_date.dt.year >= 2017]

checks = []
path_values = {}
for i, row in e.iterrows():
    a, b = pos[row.AD], pos[row.ED]
    e.loc[i, 'announcement_gap'] = b-a
    r = ret[row.RIC][a-1:b+2]
    m = market[a-1:b+2]
    if np.isfinite(r).all() and np.isfinite(m).all():
        e.loc[i, 'arithmetic'] = 100*np.sum(r-m)
        e.loc[i, 'compounded'] = 100*(np.prod(1+r)-np.prod(1+m))
        e.loc[i, 'close_before_AD_to_after_ED'] = 100*(np.prod(1+r[1:])-np.prod(1+m[1:]))
        # Same compound calculation through log returns is an independent check.
        assert np.all(r > -1) and np.all(m > -1)
        via_logs = 100*(np.exp(np.log1p(r).sum())-np.exp(np.log1p(m).sum()))
        assert np.isclose(via_logs, e.loc[i,'compounded'], atol=1e-9)
    fixed_r, fixed_m = ret[row.RIC][a-1:a+6], market[a-1:a+6]
    if np.isfinite(fixed_r).all() and np.isfinite(fixed_m).all():
        e.loc[i,'fixed_announcement_week'] = 100*np.sum(fixed_r-fixed_m)
    full_r = ret[row.RIC][a-1:b+21]
    full_m = market[a-1:b+21]
    if np.isfinite(full_r).all() and np.isfinite(full_m).all():
        # Every plotted day uses exactly this fixed complete cohort.
        path_values[i] = {
            k: 100*np.sum(ret[row.RIC][a-1:b+k+1]-market[a-1:b+k+1])
            for k in range(-1,21)
        }
        assert np.isclose(path_values[i][1], e.loc[i,'arithmetic'], atol=1e-9)

assert np.allclose(e.arithmetic, e.tot, atol=1e-8, equal_nan=True)
checks.append({'check':'primary arithmetic CAR matches frozen outcomes','passed':True,'events':len(e)})
checks.append({'check':'compound product agrees with log implementation','passed':True,'events':int(e.compounded.notna().sum())})
checks.append({'check':'path at ED+1 equals primary return on fixed cohort','passed':True,'events':len(path_values)})
rows = []
for ty in ['addition','deletion']:
    for label, d in sample_groups(e[e.type == ty]):
        d = d.dropna(subset=['arithmetic','compounded','close_before_AD_to_after_ED'])
        for measure in ['arithmetic','compounded','close_before_AD_to_after_ED']:
            rows.append({'type':ty,'period':label,'measure':measure,**interval(d[measure],d.review_cycle)})
pd.DataFrame(rows).to_csv(out/'return_conventions.csv', index=False)

# Added after inspecting timing metadata, before inspecting these fixed-window
# outcomes: seven daily returns AD-1..AD+5, ending before ED for every event.
# It is a diagnostic of a changing measurement horizon, not a replacement window.
assert e.announcement_gap.min() >= 6
timing, fixed_rows = [], []
for ty in ['addition','deletion']:
    for label, d in sample_groups(e[e.type==ty]):
        d = d.dropna(subset=['arithmetic','fixed_announcement_week'])
        reviews = d.drop_duplicates('review_cycle')
        timing.append(dict(type=ty,period=label,n=len(d),reviews=len(reviews),
            gap_min=reviews.announcement_gap.min(),gap_median=reviews.announcement_gap.median(),
            gap_max=reviews.announcement_gap.max()))
        for measure in ['arithmetic','fixed_announcement_week']:
            fixed_rows.append(dict(type=ty,period=label,measure=measure,**interval(d[measure],d.review_cycle)))
pd.DataFrame(timing).to_csv(out/'announcement_timing.csv',index=False)
pd.DataFrame(fixed_rows).to_csv(out/'fixed_window_sensitivity.csv',index=False)
checks.append({'check':'fixed announcement window ends before ED for every event','passed':True,'events':len(e)})
raw = pd.read_csv(src/'data/events/omxsb_changes_nasdaq_2007_2026.csv',parse_dates=['effective_date'])
hold = pd.read_csv(src/'results/fund_demand/handelser_omraknade.csv')
hold = hold[(~hold.split)&hold.D_C.notna()&hold.y_tot.notna()]
coverage=[]
for ty in ['addition','deletion']:
    for start, stop in [(2007,2011),(2012,2016),(2017,2021),(2022,2026)]:
        label=f'{start}-{stop}'
        r=raw[(raw.type==ty)&raw.effective_date.dt.year.between(start,stop)]
        q=e[(e.type==ty)&e.effective_date.dt.year.between(start,stop)&e.arithmetic.notna()]
        h=hold[(hold.type==ty)&(hold.per == f'{start}–{str(stop)[-2:]}')]
        coverage.append(dict(type=ty,period=label,source_events=len(r),return_events=len(q),holdings_events=len(h),return_reviews=q.review_cycle.nunique()))
pd.DataFrame(coverage).to_csv(out/'sample_by_period.csv',index=False)

paths = []
pe = e.loc[list(path_values)].copy()
for ty in ['addition','deletion']:
    for label, d in sample_groups(pe[pe.type == ty]):
        for k in range(-1,21):
            vals = [path_values[i][k] for i in d.index]
            paths.append({'type':ty,'period':label,'day_from_ED':k,**interval(vals,d.review_cycle)})
pd.DataFrame(paths).to_csv(out/'fixed_cohort_path.csv', index=False)
old = pd.read_csv(out/'paired_horizon.csv')
for ty in ['addition','deletion']:
    for label in ['2017-2026','2022-2026']:
        p = next(x for x in paths if x['type']==ty and x['period']==label and x['day_from_ED']==20)
        q = old[(old.type==ty)&(old.period.str.replace('–','-',regex=False)==label)&(old.window=='cumulative20')].iloc[0]
        assert p['n']==q.n and abs(p['mean']-q.b)<1e-8 and abs(p['se']-q.se)<1e-8
        checks.append({'check':f'ED+20 endpoint matches previous independent calculation: {ty} {label}','passed':True,'events':p['n']})
(out/'return_definition_validation.json').write_text(json.dumps(checks,indent=2))
print(pd.DataFrame(rows).query("type=='addition' and period in ['2017-2026','2022-2026']").to_string(index=False))
print(f'{len(checks)} checks passed; no event-level observations exported.')
