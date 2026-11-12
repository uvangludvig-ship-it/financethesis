"""Read frozen authorized inputs; write aggregate checks only, never event rows."""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
from scipy.stats import t
import statsmodels.api as sm

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path, help='Authorized frozen thesis_final directory')
parser.add_argument('output', type=Path, help='Directory for aggregate-only output')
args = parser.parse_args()
SRC, OUT = args.source, args.output
OUT.mkdir(parents=True, exist_ok=True)
e = pd.read_csv(SRC / 'results/fund_demand/handelser_omraknade.csv')
reported = pd.read_csv(SRC / 'results/fund_demand/omrakning_resultat.csv')
base = e[e.fonddata & ~e.split.astype(bool) & e.D_C.notna()].copy()
scatter = base[base.y_tot.notna()].copy()
rows = []
for kind in ['addition', 'deletion']:
    for period, subset in [('all', scatter), ('2017–26', scatter[scatter.ar >= 2017])]:
        d = subset[subset.type == kind]
        x, y = (d.s * d.D_C).to_numpy(), d.car_tot.to_numpy()
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        residual = y - X @ beta
        rsq = 1 - np.sum(residual**2) / np.sum((y-y.mean())**2)
        model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': d.review})
        assert np.isclose(rsq, np.corrcoef(x, y)[0, 1]**2, atol=1e-12)
        assert np.isclose(rsq, model.rsquared, atol=1e-12)
        rows.append(dict(type=kind, period=period, n=len(d), reviews=d.review.nunique(),
                         r_squared=rsq, variation_percent=100*rsq, correlation=np.corrcoef(x,y)[0,1],
                         intercept=beta[0], slope=beta[1], slope_cluster_se=model.bse[1]))
pd.DataFrame(rows).to_csv(OUT / 'claude_demand_return_aggregate_check.csv', index=False)

rows = []
for kind in ['addition', 'deletion']:
    d = base[(base.type == kind) & (base.ar >= 2017)]
    for col in ['D_C', 'D_B', 'V_bara', 'C_bara', 'passiva_ovriga', 'aktiva', 'alla_fonder']:
        y = d[col].to_numpy()
        n, g = len(d), d.review.nunique()
        estimate = y.mean()
        sums = pd.Series(y-estimate).groupby(d.review.to_numpy()).sum().to_numpy()
        se = np.sqrt(g/(g-1) * np.sum(sums**2) / n**2)
        low, high = estimate + np.array([-1,1])*t.ppf(.975, g-1)*se
        check = reported[(reported.tabell == 7) & (reported.typ == kind) &
                         (reported.period == '2017–26') & (reported.grupp == col)].iloc[0]
        assert np.isclose(estimate, check.b, atol=1e-12)
        assert np.isclose(se, check.se, atol=1e-12)
        if col != 'aktiva':
            assert np.isclose(low, check.lo, atol=1e-12)
            assert np.isclose(high, check.hi, atol=1e-12)
        rows.append(dict(type=kind, period='2017–26', group=col, n=n, reviews=g,
                         mean=estimate, cr1_se=se, analytical_lo=low, analytical_hi=high,
                         frozen_lo=check.lo, frozen_hi=check.hi,
                         frozen_ci_method=check.ci_metod))
    assert np.allclose(d.alla_fonder, d.D_C+d.passiva_ovriga+d.aktiva)
pd.DataFrame(rows).to_csv(OUT / 'claude_who_buys_aggregate_check.csv', index=False)
table = pd.DataFrame(rows)
table = table[(table.type == 'addition') & table.group.isin(['D_C', 'passiva_ovriga', 'aktiva', 'alla_fonder'])].copy()
table['label'] = table.group.map({'D_C': 'Covered OMXSB-linked funds (C)',
                                'passiva_ovriga': 'Other funds classified as passive',
                                'aktiva': 'Funds classified as active',
                                'alla_fonder': 'All included funds'})
table['unit'] = 'Percent of shares outstanding; positive is net buying'
table['inference'] = 'Analytical CR1 by review with t(G-1), common to all four rows'
table[['period','group','label','n','reviews','mean','analytical_lo','analytical_hi','unit','inference']].to_csv(
    OUT / 'observed_fund_net_buying_2017_2026.csv', index=False)
definitions = {
    'sample': '136 addition events in 19 reviews, 2017–2026; funddata true, share-adjustment screen passed, C demand observed. All four rows use the same events.',
    'classification': 'One mutually exclusive production group for each included fund-event, determined by dated classification records and fallback fund type/name rules; pre/post reporting availability and unchanged group are required.',
    'partition': 'D_C + passiva_ovriga + aktiva = alla_fonder for each included event, checked numerically; subgroup D_B + V_bara + C_bara = D_C.',
    'D_C': 'Observed changes in event-security holdings of strict followers, variants, and classified balanced funds. Actual holdings of balanced funds are not multiplied by benchmark asset weights.',
    'passiva_ovriga': 'Sum of OMXS30, small-cap-index, other Swedish passive, and other foreign passive groups, using the source classification rules.',
    'aktiva': 'Residual production group ej passiv, rather than an independently certified census of active management.',
    'ownership_distinction': 'Benchmark weights scale balanced-fund assets in the separate ownership proxy, not these security-level holdings changes.',
    'interpretation': 'All included observed funds are net buyers on average. Counterparty identities are not observed; counterparties may include funds outside coverage, other investors, and issuer share supply. The result does not show that all fund-sector sellers are outside the fund sector.',
    'uncertainty': 'Analytical CR1 intervals use the same method for all four rows. The inherited active-fund row uses wild-bootstrap inversion instead; both are retained in the detailed aggregate audit CSV.',
}
(OUT / 'observed_fund_net_buying_definition.json').write_text(json.dumps(definitions, indent=2, ensure_ascii=False)+'\n')

fi = pd.read_csv(SRC / 'data/funds/fund_net_buying_fi_by_event_2019_2026.csv')
fi = fi[fi.status == 'ok']
fi = fi.merge(e[['event_id', 'RIC', 'review']], on=['RIC', 'review'])
matched = fi.merge(e[['event_id', 'D_C']], on='event_id').dropna(subset=['D_C', 'netto_OMXSB_ny'])
fi_check = dict(n=len(matched), correlation=float(matched[['D_C', 'netto_OMXSB_ny']].corr().iloc[0,1]),
                lseg_mean=float(matched.D_C.mean()), fi_mean=float(matched.netto_OMXSB_ny.mean()),
                caveat='Source step-0 merge; demand-signed values; not necessarily the same sample as the CAR-complete FI ratio table.')
assert len(matched) == 208
assert round(fi_check['correlation'], 3) == .842
(OUT / 'claude_fi_aggregate_check.json').write_text(json.dumps(fi_check, indent=2)+'\n')
print(json.dumps(dict(scatter_rows=4, who_buys_rows=14, fi=fi_check, checks='All numerical assertions passed.'), indent=2))
