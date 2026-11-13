"""Independent locked-result audit. No alternative estimands or raw-value exports.

Run with Python + pandas/numpy/scipy/pyarrow. Requires licensed local inputs.
--output must name a fresh JSON file; frozen audit files are never overwritten.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for part in iter(lambda: handle.read(4 * 1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def compare(a, b, atol=1e-8):
    a, b = np.asarray(a, float), np.asarray(b, float)
    assert a.shape == b.shape
    valid = np.isfinite(a) & np.isfinite(b)
    same = np.isclose(a, b, rtol=1e-10, atol=atol, equal_nan=True)
    return dict(cells=int(a.size), mismatches=int((~same).sum()),
                max_absolute_difference=float(np.max(np.abs(a[valid]-b[valid]))) if valid.any() else 0.)


def joined(old, extra, fields):
    """Reconstruct cell precedence and per-security source agreement independently."""
    old = old.set_index(['ric', 'date'])[fields]
    extra = extra.set_index(['ric', 'date'])[fields]
    assert old.index.is_unique and extra.index.is_unique
    keys = old.index.union(extra.index)
    result = old.reindex(keys).copy()
    source = pd.DataFrame(index=keys, columns=fields, dtype=object)
    for field in fields:
        source.loc[old.index, field] = np.where(old[field].notna(), 'old', None)
        for ric, sub in extra.groupby(level='ric', sort=False):
            common = old.index.intersection(sub.index)
            both = old.loc[common, field].notna() & sub.loc[common, field].notna()
            compatible = (int(both.sum()) >= 20 and np.allclose(
                old.loc[common[both], field], sub.loc[common[both], field], rtol=1e-8, atol=1e-10))
            missing_keys = sub.index[result.loc[sub.index, field].isna() & sub[field].notna()]
            result.loc[missing_keys, field] = sub.loc[missing_keys, field]
            source.loc[missing_keys, field] = 'old' if compatible else 'new'
    for field in fields:
        result[field + '_src'] = source[field]
    return result.reset_index()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path('/Users/ludviguvang/dev/financethesis'))
    parser.add_argument('--results', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Choose a new audit output file'
    repo = args.repo_root.resolve()
    out = args.results or repo/'output/omxsb_history_extension_20261103'
    lock = json.loads((out/'RUN_LOCK.json').read_text())
    manifest = json.loads((out/'RUN_MANIFEST.json').read_text())
    def local(name):
        p = Path(name)
        if not p.is_absolute():
            return repo/p
        if p.exists():
            return p
        if name.endswith('.xlsx'):
            return repo/'output/omxsb_scaled_round_20261103/private/user_source'/p.name
        return p
    inputs_ok = {name: digest(local(name)) == value for name, value in lock['inputs'].items()}
    code = repo/'code/build/omxsb_history_extension/extend.py'
    checks = dict(input_hashes=inputs_ok,
                  locked_script_unchanged=digest(code) == lock['script_sha256'],
                  locked_specification_unchanged=digest(out/'SPECIFICATION.txt') == lock['specification_sha256'],
                  lock_precedes_manifest=lock['locked_utc'] < manifest['created_utc'])
    original = pd.read_csv(repo/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv', dtype=str).fillna('')
    catalog = pd.read_csv(out/'private/omxsb_history_catalog_2002_2026.csv', dtype=str).fillna('')
    pd.testing.assert_frame_equal(original, catalog.iloc[:len(original)][original.columns].reset_index(drop=True))
    old = pd.read_csv(repo/'output/omxsb_replication_2007/events_car.csv')
    metrics = pd.read_csv(out/'EVENT_METRICS.csv')
    early = pd.read_csv(out/'private/early_source_ledger.csv')
    candidate = early.loc[early.category.eq('scheduled_candidate') & ~early.source_conflict].copy()
    measured_early = metrics[metrics.source_group.ne('legacy')].set_index('event_id')
    modern = metrics[metrics.source_group.eq('legacy')].set_index('event_id')
    assert set(modern.index) == set(old.event_id)
    assert set(measured_early.index) == set(candidate.event_id)
    checks['original_input_rows_preserved'] = len(original)
    checks['modern_result_rows_preserved'] = len(old)
    checks['modern_ann_eff_tot_exact'] = compare(
        modern.loc[old.event_id, ['ann', 'eff', 'tot']], old[['ann', 'eff', 'tot']], atol=0.)
    checks['early_selection'] = dict(source_rows=len(early), initial_basket=int(early.category.eq('initial_basket').sum()),
        other_changes=int(early.category.eq('other_change').sum()), candidates=len(candidate), reviews=int(candidate.review_cycle.nunique()),
        verified_primary=int(measured_early.source_group.eq('primary_verified').sum()),
        announcement_results=int(measured_early.ann.notna().sum()), total_results=int(measured_early.tot.notna().sum()))

    fields = ['close', 'totret', 'volume', 'bid', 'ask']
    rics = sorted(set(old.RIC) | set(candidate.RIC))
    panel_path = repo/'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet'
    raw = pd.read_parquet(panel_path, columns=['ric', 'date']+fields, filters=[('ric', 'in', rics)])
    raw['date'] = pd.to_datetime(raw.date).dt.normalize()
    index = pd.read_csv(repo/'data/raw/lseg/panel_2005_2026/indices_daily (1).csv', usecols=['ric', 'date', 'close'], parse_dates=['date'])

    # Exact legacy convention: observed-stock-row price fallback, original GI calendar.
    gi = index[index.ric.eq('.OMXSBGI') & index.close.notna()].set_index('date').close.sort_index()
    gi_ar = (gi/gi.shift()-1)*100
    legacy_ar = {}
    for ric, group in raw[raw.ric.isin(old.RIC) & raw.date.isin(gi.index)].groupby('ric'):
        group = group.sort_values('date').set_index('date')
        daily = group.totret.where(group.totret.notna(), (group.close/group.close.shift()-1)*100)
        legacy_ar[ric] = daily.reindex(gi.index) - gi_ar
    original_reconstructed = []
    original_reference = []
    def window(values, lo, hi):
        return float(np.sum(values[lo:hi+1])) if 0 <= lo <= hi < len(values) and np.isfinite(values[lo:hi+1]).all() else np.nan
    for event in old.itertuples():
        a, e = gi.index.get_loc(pd.Timestamp(event.AD)), gi.index.get_loc(pd.Timestamp(event.ED))
        values = legacy_ar[event.RIC].to_numpy(float)
        for metric, lo, hi in [('ann', a-1, a+1), ('eff', e-1, e+1), ('tot', a-1, e+1)]:
            original_reconstructed.append(window(values, lo, hi))
            original_reference.append(getattr(event, metric))
    checks['independent_legacy_raw_replay'] = compare(original_reconstructed, original_reference, atol=1e-9)

    extra = pd.read_csv(out/'private/FETCHED_NORMALIZED_LONG.csv.gz', parse_dates=['date'])
    extra_index = pd.read_csv(out/'private/FETCHED_INDICES_LONG.csv.gz', parse_dates=['date'])
    panel = joined(raw[raw.ric.isin(candidate.RIC)], extra, fields)
    index = joined(index, extra_index, ['close'])
    cal = pd.DatetimeIndex(sorted(index.loc[index.ric.isin(['.OMXSBGI', '.OMXSPI']) & index.close.notna(), 'date'].unique()))
    market = index[index.ric.eq('.OMXSBGI')].set_index('date').reindex(cal)
    market_return = ((market.close/market.close.shift()-1)*100).where(market.close_src.eq(market.close_src.shift()))
    securities = {ric: group.set_index('date').reindex(cal) for ric, group in panel.groupby('ric')}
    names = ['eff', 'post10', 'post20', 'post60', 'post100', 'volume_share_edm1', 'spread_edm1']
    comparisons, actual, gates, paths = [], [], [], []
    for event in candidate.itertuples():
        s = securities.get(event.RIC)
        values = {name: np.nan for name in names}
        p = cal.get_loc(pd.Timestamp(event.effective_date)) if pd.Timestamp(event.effective_date) in cal else None
        valid = s.close.gt(0) if s is not None else pd.Series(dtype=bool)
        dates = cal[valid.to_numpy()] if s is not None else pd.DatetimeIndex([])
        span = len(dates) > 0 and dates.min() <= pd.Timestamp(event.effective_date)-pd.Timedelta(days=100) and dates.max() >= pd.Timestamp(event.effective_date)+pd.Timedelta(days=100)
        row = measured_early.loc[event.event_id]
        gates.append(bool(row.price_series == (s is not None) and row.exact_calendar_date == (p is not None) and row.coverage_100_calendar == span))
        if p is not None and span:
            close = s.close.where(s.close.gt(0))
            price_ret = ((close/close.shift()-1)*100).where(s.close_src.eq(s.close_src.shift()))
            total = s.totret.where(s.totret.notna(), price_ret).where(close.notna() & close.shift().notna())
            ar = (total - market_return).to_numpy(float)
            for metric, lo, hi in [('eff', -1, 1), ('post10', 0, 10), ('post20', 0, 20), ('post60', 0, 60), ('post100', 0, 100)]:
                values[metric] = window(ar, p+lo, p+hi)
            if p >= 22 and p+22 < len(cal):
                vol = s.volume.iloc[p-22:p+23]
                if np.isfinite(vol).all() and vol.ge(0).all() and vol.sum() > 0 and s.volume_src.iloc[p-22:p+23].nunique(dropna=False) == 1:
                    values['volume_share_edm1'] = float(100*vol.iloc[21]/vol.sum())
            if p >= 1:
                b, a = s.bid.iloc[p-1], s.ask.iloc[p-1]
                if np.isfinite(b) and np.isfinite(a) and a >= b > 0 and s.bid_src.iloc[p-1] == s.ask_src.iloc[p-1]:
                    spread = 200*(a-b)/(a+b)
                    if spread <= 20:
                        values['spread_edm1'] = spread
            if np.isfinite(values['post100']):
                paths.append((event.event_id, np.r_[0., np.cumsum(ar[p:p+101])]))
        comparisons.extend(values.values())
        actual.extend(row[names].to_numpy(float))
    checks['early_source_support_flags'] = dict(rows=len(gates), all_equal=all(gates))
    checks['independent_early_raw_metrics'] = compare(comparisons, actual)
    checks['early_finite_windows'] = {name: int(measured_early[name].notna().sum()) for name in names}
    checks['early_benchmark_missing_sessions'] = [str(x.date()) for x in cal[(market.close.isna()) & (cal.year < 2007)]]

    all_metrics = ['eff', 'post10', 'post20', 'post60', 'post100', 'ann', 'tot', 'volume_share_edm1', 'spread_edm1']
    samples = {'BASELINE': metrics.source_group.eq('legacy'), 'VERIFIED_EXTENDED': metrics.source_group.ne('vendor_provisional'),
               'PROVISIONAL_EARLY_ONLY': metrics.source_group.eq('vendor_provisional'), 'VERIFIED_EARLY_ONLY': metrics.source_group.eq('primary_verified'),
               'PROVISIONAL_COMBINED': pd.Series(True, index=metrics.index)}
    summary_checks = {}
    for label, selected in samples.items():
        frame = metrics[selected]
        output = pd.read_csv(out/f'{label}_SUMMARY.csv')
        expected, observed = [], []
        for row in output.itertuples():
            sub = frame if row.period == 'All' else frame[frame.period.eq(row.period)]
            sub = sub[sub.type.eq(row.type) & sub[row.metric].notna()]
            review = sub.groupby('review_cycle')[row.metric].mean().to_numpy(float)
            n = len(review)
            center = review.mean() if n else np.nan
            se = np.sqrt(np.sum((review-center)**2)/(n*(n-1))) if n >= 2 else np.nan
            margin = t.ppf(.975, n-1)*se if n >= 2 else np.nan
            expected.extend([len(sub), n, sub[row.metric].mean(), center, se, center-margin, center+margin])
            observed.extend([row.events, row.reviews, row.mean_event, row.mean_review, row.se_review, row.ci_low, row.ci_high])
        summary_checks[label] = compare(expected, observed)
    checks['independent_summary_arithmetic'] = summary_checks
    path_frame = pd.read_csv(out/'BALANCED_ED_PATHS.csv')
    assert not path_frame.duplicated(['event_id', 'tau']).any()
    assert path_frame.groupby('event_id').size().eq(102).all()
    assert set(path_frame.event_id) == set(metrics.loc[metrics.post100.notna(), 'event_id'])
    checks['balanced_paths'] = dict(events=int(path_frame.event_id.nunique()), rows=len(path_frame),
        initial_zero=bool(path_frame.loc[path_frame.tau.eq(-1), 'car'].eq(0).all()),
        terminal=compare(path_frame[path_frame.tau.eq(100)].set_index('event_id').car.sort_index(), metrics.set_index('event_id').post100.dropna().sort_index()))
    for event_id, curve in paths:
        result = compare(curve, path_frame[path_frame.event_id.eq(event_id)].sort_values('tau').car)
        assert result['mismatches'] == 0
    expected, observed = [], []
    for row in pd.read_csv(out/'BALANCED_ED_PATH_SUMMARY.csv').itertuples():
        subset = path_frame[path_frame.source_group.eq(row.source_group) & path_frame.period.eq(row.period) & path_frame.type.eq(row.type) & path_frame.tau.eq(row.tau)]
        expected.extend([subset.car.mean(), subset.event_id.nunique(), subset.review_cycle.nunique(), subset.groupby('review_cycle').car.mean().mean()])
        observed.extend([row.mean_car_event, row.events, row.reviews, row.mean_car_review])
    checks['balanced_path_summary'] = compare(expected, observed)
    def passed(value):
        if isinstance(value, dict):
            return (value.get('mismatches', 0) == 0 and all(passed(v) for k, v in value.items() if k != 'mismatches'))
        if isinstance(value, bool):
            return value
        return True
    report = dict(created_utc=datetime.now(timezone.utc).isoformat(), status='PASS' if passed(checks) else 'FAIL',
        scope='Independent locked-result arithmetic and eligibility replay; no new contrast, no raw numeric prices exported',
        reviewer_script_sha256=digest(Path(__file__)), result_lock_sha256=digest(out/'RUN_LOCK.json'),
        checks=checks,
        limitations=['No primary-source certification of early vendor dates, identities, currencies or corporate actions.',
                     'Source-date union is not independently certified full historical exchange calendar.',
                     'Legacy arithmetic retains the original missing-date convention; new metrics use strict session rules.',
                     'Source addendum was not itself included in RUN_LOCK hash; core code and base specification were.',
                     'Review-t intervals are nominal exploratory and condition on review independence; issuer reuse and calendar dependence remain.'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    assert report['status'] == 'PASS'


if __name__ == '__main__':
    main()
