"""Replay the additional baseline cohort count; never opens price outcomes.

The declaration saved before the original calculation is preserved. No second
peer portfolio or alternative return model is constructed from these counts.
"""
from pathlib import Path
import hashlib
import json
import pandas as pd

O = Path(__file__).resolve().parent
OLD = O.parents[1] / 'contribution_round_20261103/network_consequence'
R = Path('/Users/ludviguvang/dev/financethesis')
paths = {
    'cohort': O / 'baseline_fund_cohort.csv.gz',
    'holdings': OLD / 'baseline_transferable_rows.csv.gz',
    'roles': R / 'output/omxsb_mechanism_frontier_20261102/ownership/security_role_gate.csv',
}
assert (O / 'PRE_NONHOLDER_COHORT_DECLARATION.json').exists()
F = pd.read_csv(paths['cohort'], dtype={'fund_id': str})
F = F[F.group.eq('family')]
H = pd.read_csv(paths['holdings'], dtype={'fund_id': str})
S = pd.read_csv(paths['roles'], usecols=['event_id', 'role', 'aliases', 'q0'])
rows = []
for event_id, f in F.groupby('event_id'):
    s = S[S.event_id.eq(event_id)]
    assert len(s) == 4 and s.q0.nunique() == 1
    aliases_event = set(s.loc[s.role.eq('event'), 'aliases'].iloc[0].split(';'))
    aliases_all4 = set(';'.join(s.aliases).split(';'))
    h = H[H.quarter.eq(s.q0.iloc[0]) & H.fund_id.isin(f.fund_id)
          & H.qty.gt(0) & H.mv.gt(0)]
    event_holders = set(h.loc[h['isin'].isin(aliases_event), 'fund_id'])
    all4_holders = set(h.loc[h['isin'].isin(aliases_all4), 'fund_id'])
    n = f[~f.fund_id.isin(event_holders)]
    n4 = f[~f.fund_id.isin(all4_holders)]
    rows.append(dict(
        event_id=event_id, review=f.review.iloc[0], family_funds=len(f),
        no_observed_event_position_funds=len(n),
        no_observed_event_position_managers=n.company.nunique(),
        nonholder_AUM_fraction=n.aum.sum() / f.aum.sum(),
        no_observed_any4_position_funds=len(n4),
        no_observed_any4_position_managers=n4.company.nunique(),
    ))
D = pd.DataFrame(rows)
out = O / 'pre_nonholder_cohort_counts.csv'
if out.exists():
    original = pd.read_csv(out)
    pd.testing.assert_frame_equal(D, original, check_dtype=False, rtol=1e-12, atol=1e-12)
else:
    D.to_csv(out, index=False)
(O / 'PRE_NONHOLDER_INPUT_SHA256.json').write_text(json.dumps({
    k: {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    for k, p in paths.items()
}, indent=2))
print(json.dumps({
    'events': len(D),
    'minimum_no_observed_target_position_funds': int(D.no_observed_event_position_funds.min()),
    'maximum_no_observed_target_position_funds': int(D.no_observed_event_position_funds.max()),
    'median_no_observed_target_position_funds': float(D.no_observed_event_position_funds.median()),
    'minimum_managers': int(D.no_observed_event_position_managers.min()),
    'median_AUM_fraction_retained': float(D.nonholder_AUM_fraction.median()),
    'all4_nonholder_cohort_empty': int(D.no_observed_any4_position_funds.eq(0).sum()),
    'price_or_return_outcomes_opened': False,
}, indent=2))
