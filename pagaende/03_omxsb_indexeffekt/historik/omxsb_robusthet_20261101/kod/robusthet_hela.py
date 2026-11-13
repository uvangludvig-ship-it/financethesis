"""Repaired OMXSB control analysis. Post-result repair, not preregistration.

Run from any directory. Never edits raw data or the original replication exports.
Specification: thesis/design/ROBUSTHET_RATTELSE_20261101.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
VERSION = "repair-20261101-v5"
WEBB = np.array([-np.sqrt(1.5), -1., -np.sqrt(.5), np.sqrt(.5), 1., np.sqrt(1.5)])


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def rng_for(label):
    seed = int.from_bytes(hashlib.sha256((VERSION + str(label)).encode()).digest()[:8], 'little')
    return np.random.default_rng(seed)


def issuer_key(ric):
    """Conservative RIC-stem proxy, NOT a verified historical issuer identifier."""
    base = str(ric).split('.ST')[0]
    return re.sub(r'(?:sdb)?[a-z]+$', '', base)


def window_bounds(iad, ied):
    return dict(pre_start=iad - 101, pre_end=iad - 2, covariate_day=iad - 2,
                outcome_start=iad - 1, outcome_end=ied + 1)


def past_or_current_event(ric, review_k, event_keys):
    return any((ric, k) in event_keys for k in (review_k - 1, review_k))


def cluster_fit(X, y, groups):
    X, y = np.asarray(X, float), np.asarray(y, float)
    if not (np.isfinite(X).all() and np.isfinite(y).all()):
        raise ValueError('Regression inputs must be explicitly filtered, not silently dropped.')
    codes, names = pd.factorize(np.asarray(groups), sort=True)
    n, k = X.shape
    G = len(names)
    if G < 2 or n <= k or np.linalg.matrix_rank(X) < k:
        raise ValueError('Insufficient independent groups or rank-deficient regression.')
    inv = np.linalg.inv(X.T @ X)
    coef = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ coef
    scores = np.zeros((G, k))
    np.add.at(scores, codes, X * resid[:, None])
    adj = G / (G - 1) * (n - 1) / (n - k)
    cov = inv @ (scores.T @ scores) @ inv * adj
    return dict(coef=coef, se=np.sqrt(np.maximum(np.diag(cov), 0)), inv=inv,
                codes=codes, G=G, n=n, k=k, adj=adj)


def tail_p(simulated, observed, exact=False):
    a = np.asarray(simulated)
    if not np.isfinite(observed) or not np.isfinite(a).all():
        return np.nan
    hits = int((np.abs(a) >= abs(observed) - 1e-12 * max(1., abs(observed))).sum())
    return hits / len(a) if exact else (hits + 1) / (len(a) + 1)


def wild_cluster_p(X, y, groups, coefficient, B=9999, label=''):
    """Restricted-null, studentized wild cluster test; same OLS estimand as CI.

    Cluster-sufficient-statistic implementation, equivalent to explicitly
    generating every bootstrap outcome and refitting the model.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    f = cluster_fit(X, y, groups)
    j, G, codes = coefficient, f['G'], f['codes']
    if f['se'][j] <= np.finfo(float).eps:
        return np.nan
    Xr = np.delete(X, j, axis=1)
    fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0] if Xr.shape[1] else np.zeros(len(y))
    er = y - fr
    beta_fr = np.linalg.lstsq(X, fr, rcond=None)[0]
    q = X @ f['inv'][:, j]
    cluster_xer = np.zeros((G, X.shape[1]))
    cluster_qx = np.zeros_like(cluster_xer)
    np.add.at(cluster_xer, codes, X * er[:, None])
    np.add.at(cluster_qx, codes, X * q[:, None])
    cluster_qer = np.bincount(codes, weights=q * er, minlength=G)
    cluster_qefr = np.bincount(codes, weights=q * (fr - X @ beta_fr), minlength=G)
    coef_per_cluster = cluster_xer @ f['inv']
    rng = rng_for(('wild', label))
    ts = []
    for start in range(0, B, 1024):
        W = rng.choice([-1., 1.] if G >= 12 else WEBB, (min(1024, B - start), G))
        delta = W @ coef_per_cluster
        scores = cluster_qefr + W * cluster_qer - delta @ cluster_qx.T
        se = np.sqrt(np.sum(scores ** 2, axis=1) * f['adj'])
        numerator = beta_fr[j] + delta[:, j]
        with np.errstate(divide='ignore', invalid='ignore'):
            t = numerator / se
        # Degenerate draws should not be silently discarded.
        t = np.where((se == 0) & (numerator == 0), 0., t)
        ts.extend(t)
    observed = f['coef'][j] / f['se'][j]
    # Infinite t values from zero bootstrap variance are valid tail events.
    ts = np.asarray(ts)
    if np.isnan(ts).any():
        raise ValueError('Undefined bootstrap draw; inspect degenerate design.')
    hits = (np.abs(ts) >= abs(observed) - 1e-12 * max(1., abs(observed))).sum()
    return float((hits + 1) / (B + 1))


def signflip_means(means, label='', B=19999):
    m = np.asarray(means, float)
    G = len(m)
    if G < 2:
        return np.nan
    if G <= 16:
        bits = ((np.arange(2 ** G)[:, None] >> np.arange(G)) & 1)
        samples = ((2 * bits - 1) * m).mean(axis=1)
        return tail_p(samples, m.mean(), exact=True)
    weights = rng_for(('sign', label)).choice([-1., 1.], (B, G))
    return tail_p(weights @ m / G, m.mean())


def mean_inference(values, groups, B=9999, label=''):
    d = pd.DataFrame({'value': values, 'review': groups}).replace([np.inf, -np.inf], np.nan).dropna()
    m = d.groupby('review', sort=True).value.mean()
    result = dict(N=len(d), G=len(m), estimate_pp=float(m.mean()),
                  event_weighted_mean_pp=float(d.value.mean()), ci_lo=np.nan, ci_hi=np.nan,
                  p_signflip=np.nan, p_wild=np.nan, estimand='equal_review_mean', status='ok')
    if len(m) < 2:
        result['status'] = 'insufficient_reviews'
        return result
    se = m.std(ddof=1) / np.sqrt(len(m))
    margin = stats.t.ppf(.975, len(m) - 1) * se
    result.update(ci_lo=float(m.mean() - margin), ci_hi=float(m.mean() + margin),
                  p_signflip=signflip_means(m.values, label),
                  p_wild=wild_cluster_p(np.ones((len(m), 1)), m.values, m.index, 0, B, label))
    return result


def choose_matches(pool, event, mu, sd, number=3):
    """Only covariates and identifiers enter this function. Outcomes are ignored."""
    c = pool[pool.issuer != event['issuer']].copy()
    scale = sd[['precar', 'log_mcap']].replace(0, np.nan)
    if not np.isfinite(scale).all():
        return c.iloc[:0]
    ez = (pd.Series({k: float(event[k]) for k in scale.index}) - mu[scale.index]) / scale
    cz = (c[scale.index] - mu[scale.index]) / scale
    c['distance'] = np.sqrt(((cz - ez) ** 2).sum(axis=1))
    c = c[np.isfinite(c.distance)].sort_values(['distance', 'ric'], kind='stable')
    return c.drop_duplicates('issuer').head(number)


def paired_difference(event_car, control_cars, required):
    a = np.asarray(control_cars, float)
    if len(a) < required or not np.isfinite(event_car) or not np.isfinite(a[:required]).all():
        return np.nan
    return float(event_car - a[:required].mean())


def supported_reviews(d):
    if d.empty:
        return d.copy()
    g = d.groupby('review').event.agg(['min', 'max'])
    return d[d.review.isin(g.index[(g['min'] == 0) & (g['max'] == 1)])].copy()


def common_support(d):
    parts = []
    for _, g in d.groupby('review', sort=True):
        if g.event.nunique() != 2:
            continue
        keep = np.ones(len(g), dtype=bool)
        for v in ['precar', 'log_mcap']:
            lo = max(g.loc[g.event == j, v].min() for j in [0, 1])
            hi = min(g.loc[g.event == j, v].max() for j in [0, 1])
            keep &= g[v].between(lo, hi).values
        parts.append(g.loc[keep])
    return supported_reviews(pd.concat(parts, ignore_index=True) if parts else d.iloc[:0])


def regression_inference(d, B, label):
    d = supported_reviews(d)
    result = dict(N=len(d), G=d.review.nunique(), events=int(d.event.sum()),
                  estimate_pp=np.nan, ci_lo=np.nan, ci_hi=np.nan, p_wild=np.nan,
                  p_signflip=np.nan, estimand='pooled_OLS_review_FE', status='insufficient_support')
    if d.empty or result['G'] < 2:
        return result
    FE = pd.get_dummies(d.review, dtype=float).values
    X = np.column_stack([d.event.values, d.precar.values, d.log_mcap.values, FE])
    try:
        f = cluster_fit(X, d.car.values, d.review.values)
        b, se = f['coef'][0], f['se'][0]
        margin = stats.t.ppf(.975, f['G'] - 1) * se
        result.update(estimate_pp=float(b), ci_lo=float(b-margin), ci_hi=float(b+margin),
                      p_wild=wild_cluster_p(X, d.car.values, d.review, 0, B, label), status='ok')
    except ValueError as e:
        result['status'] = str(e)
    return result


class Panel:
    def __init__(self, repo, panel_file):
        self.inputs = [panel_file, repo/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv']
        cols = ['ric', 'date', 'close', 'totret', 'volume', 'mcap']
        px = pd.read_parquet(panel_file, columns=cols) if panel_file.suffix == '.parquet' else pd.read_csv(panel_file, usecols=cols)
        px['date'] = pd.to_datetime(px.date)
        px = px[px.ric.astype(str).str.contains(r'\.ST(?:\^|$)', regex=True)].copy()
        ix = pd.read_csv(self.inputs[1], parse_dates=['date'])
        self.cal = pd.DatetimeIndex(ix.loc[(ix.ric == '.OMXSBGI') & ix.close.notna(), 'date'].sort_values().unique())
        self.pos = pd.Series(np.arange(len(self.cal)), index=self.cal)
        mkt = ix.pivot(index='date', columns='ric', values='close').reindex(self.cal).pct_change(fill_method=None)['.OMXSBGI'] * 100
        px = px[px.date.isin(self.cal)].copy()
        exact_duplicates = int(px.duplicated().sum())
        px = px.drop_duplicates()
        if px.duplicated(['ric', 'date']).any():
            raise ValueError('Conflicting duplicate stock-days. Resolve sources before calculating returns.')
        px = px.sort_values(['ric', 'date'])
        ret = {}
        fallback = 0
        for ric, g in px.groupby('ric', sort=True):
            g = g.set_index('date').reindex(self.cal[(self.cal >= g.date.min()) & (self.cal <= g.date.max())])
            fallback += int((g.totret.isna() & g.close.notna() & g.close.shift().notna()).sum())
            ret[ric] = g.totret.fillna(g.close.pct_change(fill_method=None) * 100)
        R = pd.DataFrame(ret).reindex(self.cal)
        invalid = (R > 1000) | (R < -100)
        self.qa = dict(panel_rows=len(px), ric_count=px.ric.nunique(), exact_duplicate_rows=exact_duplicates,
                       invalid_daily_returns=int(invalid.sum().sum()), price_return_fallback_rows=fallback,
                       historical_main_market_eligibility_verified=False)
        A = R.mask(invalid).sub(mkt, axis=0).values
        self.rics = list(R.columns)
        self.columns = {r: j for j, r in enumerate(self.rics)}
        self.cs = np.vstack([np.zeros(A.shape[1]), np.nancumsum(A, axis=0)])
        self.cn = np.vstack([np.zeros(A.shape[1]), np.cumsum(~np.isfinite(A), axis=0)])
        self.mcap = px.pivot(index='date', columns='ric', values='mcap').reindex(self.cal).ffill(limit=10)
        self.tv = px.assign(tvalue=px.volume * px.close).pivot(index='date', columns='ric', values='tvalue').reindex(self.cal)

    def car(self, ric, a, b):
        if ric not in self.columns or a < 0 or b >= len(self.cal) or b < a:
            return np.nan
        j = self.columns[ric]
        if self.cn[b+1, j] != self.cn[a, j]:
            return np.nan
        return float(self.cs[b+1, j] - self.cs[a, j])

    def covariates(self, ric, iad):
        w = window_bounds(iad, iad)
        if w['pre_start'] < 0:
            return None
        pre = self.car(ric, w['pre_start'], w['pre_end'])
        m = self.mcap[ric].iloc[w['covariate_day']] if ric in self.mcap else np.nan
        if not np.isfinite(pre) or not np.isfinite(m) or m <= 0:
            return None
        vol = self.tv[ric].iloc[max(0, iad-121):iad-1].sum(min_count=1) if ric in self.tv else np.nan
        return dict(ric=ric, issuer=issuer_key(ric), precar=pre, log_mcap=float(np.log(m)),
                    mcap=float(m), lagged_turnover=float(vol) if np.isfinite(vol) else 0.)


def run_analysis(repo, panel_file, outdir, B):
    outdir.mkdir(parents=True, exist_ok=True)
    panel = Panel(repo, panel_file)
    print(f"Panel loaded: {panel.qa['ric_count']} RICs", flush=True)
    evpath = repo/'output/omxsb_replication_2007/events_car.csv'
    censuspath = repo/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv'
    mempath = repo/'output/omxsb_replication_2007/mechanisms/omxsb_membership_by_review.csv'
    unipath = repo/'data/raw/lseg/panel_2005_2026/td_universe.csv'
    inputs = panel.inputs + [evpath, censuspath, mempath, unipath,
                            repo/'thesis/design/ROBUSTHET_RATTELSE_20261101.md', Path(__file__)]
    ev = pd.read_csv(evpath, parse_dates=['AD', 'ED'])
    if ev.groupby('review_cycle')[['AD', 'ED']].nunique().gt(1).any().any():
        raise ValueError('Different event clocks in one review; requires event-specific windows.')
    reviews = ev.groupby('review_cycle').agg(AD=('AD','first'), ED=('ED','first')).sort_values('AD').reset_index()
    reviews['k'] = np.arange(len(reviews))
    kmap = dict(zip(reviews.review_cycle, reviews.k))
    ev['k'] = ev.review_cycle.map(kmap)
    universe = pd.read_csv(unipath)
    tickmap = universe.dropna(subset=['TickerSymbol']).groupby('TickerSymbol').RIC.apply(list).to_dict()
    census = pd.read_csv(censuspath)
    event_keys, unresolved = set(), []
    for e in census.itertuples():
        if e.review_cycle not in kmap:
            continue
        rics = [e.RIC] if pd.notna(e.RIC) else tickmap.get(str(e.ticker), [])
        if not rics:
            unresolved.append(dict(event_id=e.event_id, review=e.review_cycle, ticker=e.ticker))
        event_keys.update((r, kmap[e.review_cycle]) for r in rics)
    for e in ev.itertuples():
        event_keys.add((e.RIC, e.k))
    pd.DataFrame(unresolved, columns=['event_id','review','ticker']).to_csv(outdir/'unresolved_event_identifiers.csv', index=False)
    mem = pd.read_csv(mempath)
    mem_after = dict(zip(mem.review_cycle, mem.members_after.fillna('').map(lambda s: set(s.split(';')))))
    matches, proxy_rows, clocks, coverage, membership_log = [], [], [], [], []
    for r in reviews.itertuples():
        iad, ied = int(panel.pos[r.AD]), int(panel.pos[r.ED])
        w = window_bounds(iad, ied)
        if w['pre_start'] < 0 or w['outcome_end'] >= len(panel.cal):
            continue
        clocks.append(dict(review=r.review_cycle, **{k: str(panel.cal[v].date()) for k,v in w.items()}))
        event_rows = ev[ev.k == r.k]
        event_issuers = {issuer_key(x) for x, k in event_keys if k == r.k}
        candidates = []
        for ric in panel.rics:
            if past_or_current_event(ric, r.k, event_keys) or issuer_key(ric) in event_issuers:
                continue
            c = panel.covariates(ric, iad)
            if c is not None:
                candidates.append(c)
        C = pd.DataFrame(candidates)
        E = []
        for e in event_rows.itertuples():
            c = panel.covariates(e.RIC, iad)
            coverage.append(dict(event_id=e.event_id, review=r.review_cycle, covariates_available=c is not None,
                                 car_available=np.isfinite(panel.car(e.RIC, w['outcome_start'], w['outcome_end']))))
            if c is not None:
                c.update(event_id=e.event_id, type=e.type, post=int(r.AD.year >= 2017), review=r.review_cycle)
                E.append(c)
        E = pd.DataFrame(E)
        if C.empty or E.empty:
            continue
        scale_frame = pd.concat([C[['precar','log_mcap']], E[['precar','log_mcap']]])
        mu, sd = scale_frame.mean(), scale_frame.std()
        for _, e in E.iterrows():
            chosen = choose_matches(C, e, mu, sd, 3)
            row = e.to_dict()
            row['car'] = panel.car(e.ric, w['outcome_start'], w['outcome_end'])
            row['n_candidates'] = C[C.issuer != e.issuer].issuer.nunique()
            cc = []
            for j, c in enumerate(chosen.itertuples(), 1):
                outcome = panel.car(c.ric, w['outcome_start'], w['outcome_end'])
                cc.append(outcome)
                row.update({f'c{j}_ric': c.ric, f'c{j}_issuer': c.issuer, f'c{j}_distance': c.distance,
                            f'c{j}_precar': c.precar, f'c{j}_log_mcap': c.log_mcap, f'c{j}_car': outcome})
            row['diff1'] = paired_difference(row['car'], cc, 1)
            row['diff3'] = paired_difference(row['car'], cc, 3)
            row['chosen_controls'] = len(chosen)
            matches.append(row)
        # T5 remains a descriptive proxy; reconstructed membership is explicitly uncertain.
        if r.k == 0:
            continue
        prev = reviews.loc[reviews.k == r.k-1, 'review_cycle'].iloc[0]
        keys = mem_after.get(prev)
        if keys is None:
            membership_log.append(dict(review=r.review_cycle, status='missing_previous_membership', unresolved=0))
            continue
        before, unknown_keys = set(), []
        for key in keys:
            if key.startswith('T:'):
                possible = [x for x in tickmap.get(key[2:], []) if panel.covariates(x, iad) is not None]
                if len(possible) == 1:
                    before.add(possible[0])
                else:
                    unknown_keys.append(key)
            elif key:
                before.add(key)
        membership_log.append(dict(review=r.review_cycle, status='reconstructed_unverified', unresolved=len(unknown_keys),
                                   unresolved_keys=';'.join(unknown_keys), reconstructed_members=len(before)))
        # A single unresolved member could otherwise become a false nonmember: skip this proxy review.
        if unknown_keys:
            continue
        P = C.sort_values(['lagged_turnover','ric'], ascending=[False,True], kind='stable').drop_duplicates('issuer').copy()
        P['reconstructed_member'] = P.ric.isin(before)
        for typ, Eg in E.groupby('type'):
            size_cut = Eg.mcap.min() if typ == 'addition' else Eg.mcap.max()
            N = P[(~P.reconstructed_member) & (P.mcap >= size_cut)] if typ == 'addition' else P[P.reconstructed_member & (P.mcap <= size_cut)]
            for flag, frame in [(1, Eg), (0, N)]:
                for q in frame.itertuples():
                    proxy_rows.append(dict(review=r.review_cycle, type=typ, post=int(r.AD.year >= 2017), event=flag,
                        ric=q.ric, issuer=q.issuer, precar=q.precar, log_mcap=q.log_mcap,
                        car=panel.car(q.ric, w['outcome_start'], w['outcome_end']),
                        membership_status='reconstructed_not_verified', main_market_eligibility='unknown',
                        ex_ante_candidate=False, size_cut=size_cut))
        print(f"Prepared {r.review_cycle}", flush=True)
    proxy_columns=['review','type','post','event','ric','issuer','precar','log_mcap','car',
                   'membership_status','main_market_eligibility','ex_ante_candidate','size_cut']
    M, N = pd.DataFrame(matches), pd.DataFrame(proxy_rows, columns=proxy_columns)
    M.to_csv(outdir/'T2_matches.csv', index=False)
    N.to_csv(outdir/'T5_proxy_preselected.csv', index=False)
    pd.DataFrame(clocks).to_csv(outdir/'window_clock.csv', index=False)
    pd.DataFrame(coverage).to_csv(outdir/'event_coverage.csv', index=False)
    pd.DataFrame(membership_log).to_csv(outdir/'membership_quality.csv', index=False)
    results, samples, balances = [], [], []
    for typ in ['addition', 'deletion']:
        for period, pv in [('before2017',0), ('since2017',1)]:
            q = M[(M.type == typ) & (M.post == pv)]
            for v in ['diff1', 'diff3']:
                label = f'T2/{typ}/{period}/{v}'
                result = mean_inference(q[v].values, q.review.values, B, label)
                result.update(test='T2_panel_match', type=typ, period=period, variant=v,
                              preselected_events=len(q), events_missing_outcome=int(q[v].isna().sum()))
                results.append(result)
                good = q[q[v].notna()]
                count = 1 if v == 'diff1' else 3
                for feature in ['precar','log_mcap']:
                    cv = good[[f'c{j}_{feature}' for j in range(1,count+1)]].mean(axis=1)
                    evv = good[feature]
                    pooled_sd = np.sqrt((evv.var(ddof=1)+cv.var(ddof=1))/2)
                    balances.append(dict(test='T2', type=typ, period=period, variant=v, feature=feature,
                                         event_mean=evv.mean(), control_mean=cv.mean(),
                                         standardized_difference=(evv.mean()-cv.mean())/pooled_sd if pooled_sd>0 else np.nan,
                                         N=len(good)))
            if N.empty:
                for variant in ['proxy_all','proxy_common_support']:
                    results.append(dict(test='T5_exploratory_proxy',type=typ,period=period,variant=variant,
                        N=0,G=0,estimate_pp=np.nan,ci_lo=np.nan,ci_hi=np.nan,p_wild=np.nan,p_signflip=np.nan,
                        estimand='pooled_OLS_review_FE',status='blocked_unresolved_historical_membership'))
                continue
            n = N[(N.type==typ) & (N.post==pv)].copy()
            n = n[np.isfinite(n[['precar','log_mcap','car']]).all(axis=1)]
            n = supported_reviews(n)
            for variant, s in [('proxy_all',n), ('proxy_common_support',common_support(n))]:
                s = supported_reviews(s)
                samples.append(s.assign(variant=variant))
                label=f'T5/{typ}/{period}/{variant}'
                result=regression_inference(s, B, label)
                result.update(test='T5_exploratory_proxy',type=typ,period=period,variant=variant)
                results.append(result)
                for feature in ['precar','log_mcap']:
                    a,b=s.loc[s.event==1,feature],s.loc[s.event==0,feature]
                    pooled=np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
                    balances.append(dict(test='T5',type=typ,period=period,variant=variant,feature=feature,
                                         event_mean=a.mean(),control_mean=b.mean(),
                                         standardized_difference=(a.mean()-b.mean())/pooled if pooled>0 else np.nan,N=len(s)))
                if not s.empty:
                    means=s.groupby(['review','event']).car.mean().unstack()
                    delta=means[1]-means[0]
                    extra=mean_inference(delta.values,delta.index.values,B,label+'/review_difference')
                    extra.update(test='T5_exploratory_proxy',type=typ,period=period,variant=variant+'_review_difference')
                    results.append(extra)
    R=pd.DataFrame(results)
    R.to_csv(outdir/'results.csv',index=False)
    pd.DataFrame(balances).to_csv(outdir/'covariate_balance.csv',index=False)
    (pd.concat(samples,ignore_index=True) if samples else pd.DataFrame(columns=proxy_columns+['variant'])).to_csv(outdir/'T5_analysis_samples.csv',index=False)
    panel.qa.update(event_census_rows=len(census),unresolved_event_identifiers=len(unresolved),bootstrap_draws=B,
                    T5_reviews_checked=len(membership_log),
                    T5_reviews_blocked=sum(x.get('unresolved',0)>0 or x['status']=='missing_previous_membership' for x in membership_log),
                    T5_status='not_estimable_membership_unresolved' if N.empty else 'exploratory_unverified_membership_proxy',
                    previous_result_known=True, preregistered=False, version=VERSION,
                    generated_at=datetime.now(ZoneInfo('Europe/Stockholm')).isoformat(),
                    python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__)
    (outdir/'run_metadata.json').write_text(json.dumps(panel.qa,indent=2,ensure_ascii=False)+'\n')
    (outdir/'input_sha256.json').write_text(json.dumps({str(p.relative_to(repo)):file_hash(p) for p in inputs},indent=2)+'\n')
    write_report(R,outdir,panel.qa)
    return R


def write_report(results,outdir,qa):
    def num(x):return 'saknas' if pd.isna(x) else f'{float(x):.3f}'
    lines=['# OMXSB: korrigerad kontrollanalys, version 5', '',
           'Teknisk resultatrapport, inte uppsatstext. Genererad '+qa['generated_at'], '',
           '## Vad denna körning kan säga', '',
           'T2 är bred panelmatchning på tidigare avkastning och storlek. T5 är en explorativ storleks-/medlemsproxy, inte verifierade nästan tillagda aktier. Historisk huvudlistebehörighet och fullständig medlemskedja är inte säkrade. Alla skattningar är associationer under respektive jämförelse, inte en kausal uppdelning av indexeffekten.', '',
           'Tidigare resultat var kända före rättelsen. Alla varianter nedan redovisas; ingen väljs för sitt p-värde. T-intervall och wild-bootstrap-p kommer från olika inferensmetoder men avser samma skattning. P-värden är nominella och explorativa.', '',
           f"T5-status: {qa['T5_status']}. {qa['T5_reviews_blocked']} av {qa['T5_reviews_checked']} granskade översyner spärras av olösta medlemsuppgifter. Om inga återstår kan ingen T5-regression skattas; detta är ett datastopp, INTE ett nollresultat. Den tidigare +1,68-regressionen kan återskapas från gamla sparade rader, men dess kontrollgrupp är inte här validerad som historiskt behöriga icke-medlemmar.", '',
           '## Resultat (procentenheter)', '',
           '| Test | Typ | Period | Variant | Skattning | 95% t-intervall | p teckenbyte | p wild | N | Översyner | Status |',
           '|---|---|---|---|---:|---|---:|---:|---:|---:|---|']
    for r in results.itertuples():
        lines.append(f'| {r.test} | {r.type} | {r.period} | {r.variant} | {num(r.estimate_pp)} | [{num(r.ci_lo)}, {num(r.ci_hi)}] | {num(r.p_signflip)} | {num(r.p_wild)} | {r.N} | {r.G} | {r.status} |')
    lines += ['', 'T2 och rader med review_difference väger varje översyn lika. T5-regressionen är pooled OLS med översynsfasta effekter och klustrad inferens. Dessa estimand ska inte blandas. N i review_difference är antal översynsskillnader; se sparade analysrader för aktieantal.', '',
              '## Rättelser som genomförts', '',
              '- Matchningsdata slutar AD−2; utfallet börjar AD−1. Tidigare avkastning omfattar fortfarande 100 handelsdagar.',
              '- Samma reviewviktning i T2:s skattning, intervall, teckenbyte och bootstrap.',
              '- Kontrollval görs innan kontrollens framtida avkastning läses. Saknade utfall ersätts inte med nästa kontroll.',
              '- Nästa översyns händelser används inte för att välja kontrollpoolen. Full händelsecensus används för samma och föregående översyn; olösta identifierare exporteras.',
              '- Tre kontroller betyder tre olika emittentproxyer. Alla matchningar, distanser och balansfält sparas.',
              '- T5 redovisas som proxy. Översyner med olösta medlems-tickers hoppas över i denna proxy; övrig kedjeosäkerhet kvarstår. Båda jämförelsegrupper måste finnas i en översyn.',
              '- Samma T5-urval används i regression och reviewdifferens. Gemensamt stöd redovisas separat och ersätter inte huvudvarianten.',
              '- Simuleringstest hanterar numeriska likheter och ger inte p=0 genom ett begränsat antal dragningar.', '',
              '## Vad som inte är visat', '',
              '- Skillnaden mellan rå och justerad avkastning är inte en identifierad andel orsakad av urval.',
              '- Lika A/B-avkastning utesluter inte köptryck som sprids mellan aktieslagen. Relativ A/B-multiplikator är inte total efterfrågeelasticitet.',
              '- Uppgifterna 0,57 och den senare korta återgångskörningen har inte källverifierats i detta paket. A/B-kodens äldre förstasteg har identifierar- och rapporttäckningsproblem; 0,74 ska inte användas som validerat förstasteg.',
              '- Ingen säkerställd återgång under ett ändligt fönster bevisar inte permanent effekt.',
              '- Frånvaro av migration, uppmärksamhet som mekanism och varför Sverige skiljer sig från USA identifieras inte här.', '',
              '## Kvarstående begränsningar', '',
              'Panelen är det tillgängliga prisunderlaget, inte en historiskt verifierad census av behöriga OMXSB-kandidater. RIC-stammar är emittentproxyer. Medlemskedjan har kända luckor. Prisavkastning används där totalavkastning saknas, enligt den tidigare replikationen; bolagshändelser måste därför fortsatt beaktas. Komplett utfallsfönster krävs och bortfall kan vara selektivt. Förhandsuppgång kan själv innehålla förväntad indexefterfrågan, så matchning på den skattar inte nödvändigtvis hela effekten av kommande indexmedlemskap. En gemensam stödrange bevisar inte balans eller kausalitet.', '',
              'Balans, valda kontroller, utfallsbortfall och exakta tidsgränser finns i CSV-filerna. Avkastningar runt FTN har inte beräknats. Originalfiler finns i archive/robusthet_repair_20261101/.', '',
              '## Körning', '',
              'python code/build/robusthet_hela.py', '',
              'Beroenden: numpy, pandas, scipy, pyarrow. Notebooken anropar samma källkod; inga kopierade regressionsfunktioner.', '']
    (outdir/'RESULTAT.md').write_text('\n'.join(lines))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=REPO)
    parser.add_argument('--panel',type=Path,default=Path('data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet'))
    parser.add_argument('--out',type=Path,default=Path('output/omxsb_robusthet_20261101'))
    parser.add_argument('--bootstrap',type=int,default=9999)
    args=parser.parse_args(argv)
    repo=args.repo.resolve(); panel=args.panel if args.panel.is_absolute() else repo/args.panel
    out=args.out if args.out.is_absolute() else repo/args.out
    run_analysis(repo,panel,out,args.bootstrap)
    # Current convenience package includes the actual code, specification and provenance.
    with zipfile.ZipFile(repo/'robusthet_hela_resultat.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file(): z.write(p,'results/'+str(p.relative_to(out)))
        for relative in ['code/build/robusthet_hela.py','code/build/test_robusthet_repair.py',
                         'code/notebooks/robusthet_hela_panelen.ipynb',
                         'code/claude_checks/twin_first_stage.py','code/claude_checks/test_twin_first_stage.py',
                         'thesis/design/OMXSB_TOLKNINGSREGLER.md','thesis/design/OMXSB_struktur.md']:
            z.write(repo/relative,relative)
        z.write(repo/'thesis/design/ROBUSTHET_RATTELSE_20261101.md','specification.md')
    shutil.copy2(out/'RESULTAT.md',repo/'RESULTAT_2026-11-01.md')
    print('Completed:',out,flush=True)


if __name__=='__main__':
    main()
