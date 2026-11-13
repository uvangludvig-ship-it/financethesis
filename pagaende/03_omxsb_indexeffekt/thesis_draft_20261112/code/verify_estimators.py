"""Cross-check the actual audit functions against alternative implementations.

Usage: python verify_estimators.py /authorized/thesis_final /audit/output
Requires statsmodels in addition to the audit requirements. No event data exported.
"""
from pathlib import Path
import ast
import sys
import json
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster, cov_cluster_2groups
from statsmodels.stats.multitest import multipletests
import statsmodels

source = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

# Load only the named pure functions; the audit's top-level data processing is not run.
tree = ast.parse(Path(__file__).with_name('independent_audit.py').read_text())
names = {'covariance_mean', 'mean_inference', 'holm', 'wcr_mean', 'fieller'}
nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
assert {node.name for node in nodes} == names
namespace = {'np': np, 'pd': pd, 'stats': stats}
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<audit functions>', 'exec'), namespace)

events = pd.read_csv(source/'data/events/omxsb_changes_with_car_2007_2026.csv')
flags = pd.read_csv(source/'data/events/omxsb_deletion_flags_2007_2026.csv')
excluded = set(flags.loc[flags.flag_offer | flags.flag_delist, 'event_id'])
events = events[~events.event_id.isin(excluded)].dropna(subset=['tot'])
checks = []

def check(label, actual, expected, tol=1e-9):
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    checks.append({'check': label, 'passed': bool(error <= tol), 'max_error': error})

for event_type in ['addition', 'deletion']:
    for period, data in events[events.type == event_type].groupby('period'):
        label = event_type+' '+period
        y = data.tot.to_numpy()
        g = pd.factorize(data.review_cycle)[0]
        sec = pd.factorize(data.RIC)[0]
        fitted = sm.OLS(y, np.ones((len(y), 1))).fit()
        result = namespace['mean_inference'](data, 'tot')
        check('mean '+label, result['b'], fitted.params[0])
        check('CR1 '+label, result['se']**2, cov_cluster(fitted, g)[0, 0])
        check('two way '+label, result['se_two_way']**2,
              cov_cluster_2groups(fitted, g, sec)[0][0, 0])
        estimates = [sm.OLS(y[g != k], np.ones((sum(g != k), 1))).fit().params[0]
                     for k in np.unique(g)]
        jack = (len(estimates)-1)/len(estimates)*sum((b-fitted.params[0])**2 for b in estimates)
        check('CV3 '+label, result['jackknife_se']**2, jack)

        # Independently materialize every bootstrap pseudo-observation and fit OLS.
        # This checks the compressed cluster-score algorithm with the same draws.
        B = 997
        G = len(np.unique(g))
        support = [-1., 1.] if G >= 12 else [-np.sqrt(1.5), -1., -np.sqrt(.5),
                                            np.sqrt(.5), 1., np.sqrt(1.5)]
        weights = np.random.default_rng(20261112).choice(support, size=(B, G))
        observed = abs(fitted.params[0]/np.sqrt(cov_cluster(fitted, g)[0, 0]))
        exceeded = 0
        for weight in weights:
            boot = sm.OLS(y*weight[g], np.ones((len(y), 1))).fit()
            statistic = abs(boot.params[0]/np.sqrt(cov_cluster(boot, g)[0, 0]))
            exceeded += statistic >= observed
        check('WCR versus observation-level OLS '+label,
              namespace['wcr_mean'](y, g, B=B), (exceeded+1)/(B+1), tol=1e-12)

family = pd.read_csv(out/'multiplicity.csv')
check('Holm versus statsmodels', namespace['holm'](family.p_wcb),
      multipletests(family.p_wcb, method='holm')[1])

ratios = pd.read_csv(out/'fieller_ratios.csv')
for row in ratios.itertuples():
    # A candidate m is accepted exactly where A*m^2+B*m+C <= 0.
    grid = np.r_[np.linspace(-1000, 1000, 4001), row.ratio]
    actual = row.A*grid**2 + row.B*grid + row.C <= 0
    if row.set_type == 'bounded':
        expected = (grid >= row.lower) & (grid <= row.upper)
    elif row.set_type == 'two_unbounded_rays':
        expected = (grid <= row.lower) | (grid >= row.upper)
    elif row.set_type == 'all_real':
        expected = np.ones(len(grid), dtype=bool)
    else:
        expected = np.zeros(len(grid), dtype=bool)
    check('Fieller set '+row.type+' '+row.tier+' '+row.period,
          actual.astype(int), expected.astype(int), tol=0)

pd.DataFrame(checks).to_csv(out/'estimator_validation.csv', index=False)
summary = {'statsmodels': statsmodels.__version__, 'checks': len(checks),
           'passed': sum(c['passed'] for c in checks),
           'failed': [c for c in checks if not c['passed']]}
(out/'estimator_validation.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
if summary['failed']:
    raise SystemExit(1)
