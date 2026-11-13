"""Independent arithmetic audit only; no new outcomes or specifications."""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
import pandas as pd

O = Path(__file__).resolve().parent
D = Path('/Users/ludviguvang/dev/financethesis/output/omxsb_mechanism_frontier_20261102/ownership')
M = O.parent / 'mechanism_frontier_20261102/ownership/fund_metadata_classification.csv'
f = pd.read_csv(D / 'decomp_fund_roles.csv.gz', dtype={'fund_id': str})
g = pd.read_csv(D / 'decomp_fund_groups.csv', dtype={'fund_id': str})
metadata = pd.read_csv(M, dtype={'fund_id': str})
saved = pd.read_csv(O / 'all_omissions.csv')
assert len(f) == 446048 and f.event_id.nunique() == 219
assert not f.duplicated(['event_id', 'role', 'fund_id']).any()
assert not g.duplicated(['review', 'fund_id']).any()
assert g.company.notna().all() and g.company.str.strip().ne('').all()
assert f[['own_before', 'own_after']].isin([0, 1]).all().all()
assert set(f.role) == {'event', 'c1', 'c2', 'c3'}

# Full reports and legal identity are assessed before any zero filling.
metadata['label'] = metadata.label.fillna('<missing>')
meta = metadata.set_index(['quarter', 'fund_id'], verify_integrity=True)
for z in g.itertuples():
    p, q = meta.loc[(z.q0, z.fund_id)], meta.loc[(z.q1, z.fund_id)]
    assert p.n_instr > 0 and q.n_instr > 0
    assert pd.notna(p.fund_isin) and p.fund_isin == q.fund_isin
    assert p.label == q.label
    assert z.company == p.company
for quarter in set(g.q0) | set(g.q1):
    full = metadata[(metadata.quarter == quarter) & metadata.n_instr.gt(0)]
    bad = set(full.loc[full.fund_isin.notna() & full.duplicated('fund_isin', keep=False), 'fund_id'])
    active = set(g.loc[g.q0.eq(quarter) | g.q1.eq(quarter), 'fund_id'])
    assert not bad.intersection(active)

# An independent route: first form four-role contrasts separately for every fund.
joined = f.merge(g[['review', 'fund_id', 'group', 'company']], on=['review', 'fund_id'],
                 validate='many_to_one', suffixes=('', '_meta'))
assert joined.company.notna().all() and joined.group.eq(joined.group_meta).all()
wide = joined.pivot(index=['event_id', 'review', 'type', 'fund_id', 'group', 'company'],
                    columns='role', values=['own_before', 'own_after'])
assert wide.notna().all().all()  # No report/role absence becomes zero.
diff = wide['own_after'] - wide['own_before']
contrast = diff['event'] - diff[['c1', 'c2', 'c3']].mean(axis=1)
c = contrast.rename('total').reset_index()
family_labels = {'OMXSB_index_named', 'OMXSB_other_named'}
assert set(c.group) == family_labels | {'broad_H', 'other_broad_Sweden', 'other_or_unknown'}
c['family'] = c.total.where(c.group.isin(family_labels), 0.0)
c['manager'] = c.company.map(lambda x: re.sub(r'\s+', ' ', x.strip().lower()))
events = c[['event_id', 'review', 'type']].drop_duplicates().set_index('event_id', verify_integrity=True)
managers = sorted(c.manager.unique())
assert len(managers) == 69
cm = c.groupby(['event_id', 'manager'])[['total', 'family']].sum()
present = cm.index
# Additive zero means this manager has no included balanced funds for that event.
# It does not classify an absent fund report as a zero holding.
index = pd.MultiIndex.from_product([events.index, managers], names=['event_id', 'manager'])
cm = cm.reindex(index, fill_value=0.0)
both = cm.reset_index().merge(events.reset_index(), on='event_id', validate='many_to_one')

def estimate(x, selected_events):
    e = x.groupby('event_id')[['total', 'family']].sum().reindex(selected_events, fill_value=0.0)
    e = e.join(events[['review']])
    review = e.groupby('review')[['total', 'family']].mean()
    result = review.mean()
    ratio = float(result.family / result.total) if result.total != 0 else float('nan')
    return len(review), float(result.total), float(result.family), ratio

rows = []
for typ in ['addition', 'deletion']:
    ee = events[events.type.eq(typ)]
    x = both[both.type.eq(typ)]
    for kind, omit in [('none', 'none')] + [('company', m) for m in managers] + [('review', r) for r in sorted(ee.review.unique())]:
        xx = x[x.manager.ne(omit)] if kind == 'company' else x
        ids = ee.index[ee.review.ne(omit)] if kind == 'review' else ee.index
        G, total, family, ratio = estimate(xx, ids)
        rows.append(dict(type=typ, omission_kind=kind, omitted=omit, G=G,
                         total=total, family=family, ratio=ratio))
calc = pd.DataFrame(rows)
keys = ['type', 'omission_kind', 'omitted']
j = calc.merge(saved, on=keys, how='outer', validate='one_to_one', suffixes=('_audit', '_saved'), indicator=True)
assert j._merge.eq('both').all() and len(j) == 168
assert j.G_audit.eq(j.G_saved).all()
errors = {}
for col in ['total', 'family', 'ratio']:
    errors[col] = float((j[col + '_audit'] - j[col + '_saved']).abs().max())
    assert errors[col] < 1e-11

# Check contribution tables separately, with each absent manager retaining zero contribution.
contrib = []
for typ in ['addition', 'deletion']:
    x = both[both.type.eq(typ)]
    for manager in managers:
        G, a, b, _ = estimate(x[x.manager.eq(manager)], events.index[events.type.eq(typ)])
        contrib.append(dict(type=typ, manager=manager, total=a, family=b))
z = pd.DataFrame(contrib).merge(pd.read_csv(O / 'company_additive_contributions.csv'),
                               on=['type', 'manager'], validate='one_to_one', suffixes=('_audit', '_saved'))
assert len(z) == 138
for col in ['total', 'family']:
    assert np.allclose(z[col + '_audit'], z[col + '_saved'], atol=1e-12, rtol=0)

summary = []
for (typ, kind), x in calc.groupby(['type', 'omission_kind']):
    summary.append(dict(type=typ, omission_kind=kind, n=len(x),
                        ratio_min=float(x.ratio.min()), ratio_max=float(x.ratio.max()),
                        min_omitted=x.loc[x.ratio.idxmin(), 'omitted'],
                        max_omitted=x.loc[x.ratio.idxmax(), 'omitted']))
inputs = [D / 'decomp_fund_roles.csv.gz', D / 'decomp_fund_groups.csv', M,
          O / 'run.py', O / 'DECISIONS.txt', O / 'all_omissions.csv',
          O / 'company_additive_contributions.csv']
declared = json.loads((O / 'hashes.json').read_text())
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest() == v for k, v in declared.items())
report = dict(all168_omission_rows_match=True, all138_additive_company_rows_match=True,
              max_abs_error=errors, ledger_rows=len(f), events=len(events),
              additions=int(events.type.eq('addition').sum()), deletions=int(events.type.eq('deletion').sum()),
              reviews=int(events.review.nunique()), companies=len(managers),
              event_company_combinations=len(cm), absent_company_event_additive_zeros=int(len(index) - len(present)),
              balanced_four_roles_per_fund_event=True, full_nonempty_reports_both_endpoints=True,
              stable_legal_fund_isin_and_benchmark_label=True, duplicate_legal_fund_ids_excluded=True,
              missing_company_labels=0, full_results=calc[calc.omission_kind.eq('none')].to_dict('records'),
              nordea=calc[calc.omitted.str.contains('nordea', case=False)].to_dict('records'), ranges=summary,
              limits=['Point influence diagnostics conditional on the existing balanced ledger, not inference.',
                      'Absent manager contribution is additive zero; absent reports are not holdings zeros.',
                      'Pre-quarter legal company labels, not constant post labels or independent decision makers.',
                      'Ratio of signed owner-count changes, not capital, passive activity, or causal share.'],
              input_hashes={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
(O / 'independent_audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
print(json.dumps(report, indent=2, ensure_ascii=False))
