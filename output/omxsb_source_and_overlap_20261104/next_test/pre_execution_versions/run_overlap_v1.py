#!/usr/bin/env python3
"""Frozen event-only endpoint overlap; licensed quantities stay private."""
from pathlib import Path
import argparse, datetime, hashlib, json, os
import numpy as np
import pandas as pd


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bounds(weights, q1, q2, factors, supported):
    """Cap each fund before aggregation; unknown cells retain full weight."""
    w = np.asarray(weights, dtype=float)
    a, b, f = [np.asarray(x, dtype=float) for x in (q1, q2, factors)]
    known = np.asarray(supported, dtype=bool)
    assert len(w) == len(a) == len(b) == len(f) == len(known)
    assert np.isfinite(w).all() and (w > 0).all()
    assert np.isfinite(a[known]).all() and (a[known] > 0).all()
    assert np.isfinite(b[known]).all() and (b[known] >= 0).all()
    assert np.isfinite(f[known]).all() and (f[known] > 0).all()
    overlap = np.zeros(len(w))
    overlap[known] = np.minimum(1., b[known] / f[known] / a[known])
    low = float(np.dot(w, overlap) / w.sum())
    width = float(w[~known].sum() / w.sum())
    high = low + width
    assert -1e-12 <= low <= high <= 1 + 1e-12
    return low, high, overlap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', type=Path, default=Path(os.environ.get('FINANCETHESIS_REPO', '/Users/ludviguvang/dev/financethesis')))
    ap.add_argument('--gate-dir', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--design-lock', type=Path, required=True)
    a = ap.parse_args()
    O, G, R = a.output, a.gate_dir, a.repo_root
    if O.exists():
        raise RuntimeError('Use a new output directory; frozen files are never overwritten.')
    lock = json.loads(a.design_lock.read_text())
    for item in lock['inputs'].values():
        assert sha(item['path']) == item['sha256'], item['path']
    assert sha(__file__) == lock['script_sha256']
    O.mkdir(parents=True); (O/'private').mkdir()
    (O/'EXECUTION_LOCK.json').write_text(json.dumps({
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'design_lock_sha256': sha(a.design_lock),
        'script_sha256': sha(__file__),
        'new_q2_overlap_values_read_before_this_execution_lock': False,
        'source_width_known_before_decision_to_proceed': True,
    }, indent=2)+'\n')

    # Fixed q1 population/support is loaded before private q2 quantities.
    D = pd.read_csv(R/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz', dtype={'fund_id':str})
    D = D[D.type.eq('addition') & D.review.lt('2024')].copy()
    assert D.event_id.nunique() == 70 and D.review.nunique() == 10
    assert not D.duplicated(['event_id','role','fund_id']).any()
    assert D.groupby('event_id').role.apply(set).map(lambda v: v == {'event','c1','c2','c3'}).all()
    for eid, z in D.groupby('event_id'):
        base = set(z.loc[z.role.eq('event'),'fund_id'])
        assert all(set(g.fund_id) == base for _,g in z.groupby('role'))
    N = D[D.role.eq('event') & D.component.eq('new')].copy()
    assert len(N) == 737 and N.event_id.nunique() == 70
    assert np.isfinite(N.pp).all() and N.pp.gt(0).all()
    S = pd.read_csv(G/'FROZEN_ROLES.csv')
    assert len(S) == 280 and set(S.event_id) == set(N.event_id)
    S = S[S.role.eq('event')].set_index('event_id')
    E = pd.read_csv(G/'EVENT_SOURCE_GATE.csv')
    good_events = set(E.loc[E.gate_pass,'event_id']); assert len(good_events) == 59
    F = pd.read_csv(G/'ELIGIBLE_FUNDS.csv', dtype={'fund_id':str})
    assert not F.duplicated(['event_id','fund_id']).any()
    good_funds = set(zip(F.event_id,F.fund_id))
    SG = pd.read_csv(G/'SECURITY_SOURCE_GATE.csv').set_index(['review','ric'])
    N['source_supported'] = [e in good_events and (e,f) in good_funds for e,f in zip(N.event_id,N.fund_id)]
    assert int(N.source_supported.sum()) == 617
    source_width = pd.read_csv(Path(lock['inputs']['source_width']['path']))
    source_width = source_width[source_width.role.eq('event')].set_index('event_id')

    H = pd.read_csv(G/'private/RAW_RELEVANT_POSITIONS.csv.gz', dtype={'fund_id':str})
    C = pd.read_csv(G/'private/SCALING_INPUTS.csv').set_index(['review','ric'])
    assert not C.index.duplicated().any()
    rows, eventrows = [], []
    for eid, nn in N.groupby('event_id', sort=True):
        x = S.loc[eid]
        assert set(nn.review) == {x.review}
        aliases = set(x.aliases.split(';')); assert len(aliases) > 0
        hz = H[H['isin'].isin(aliases) & H.quarter.isin([x.q0,x.q1,x.q2])]
        sc = C.loc[(x.review,x.ric)]
        if eid in good_events:
            sg = SG.loc[(x.review,x.ric)]
            assert bool(sg.gate_pass) and bool(sg.q0_same_actual_LSEG_date)
            assert np.isfinite(sc.factor12) and sc.factor12 > 0
            assert abs(sc.factor12 - sg.factor12) <= 1e-12
        event_cells = []
        for z in nn.itertuples():
            known = bool(z.source_supported)
            reason = '' if known else ('old_event_source_gate_failed' if eid not in good_events else 'old_fund_report_or_unit_gate_failed')
            q0 = q1 = q2 = factor = np.nan
            n2 = 0; verified_absence = False
            if known:
                hf = hz[hz.fund_id.eq(z.fund_id)]
                def quantity(dt):
                    h = hf[hf.quarter.eq(dt)]
                    if len(h) == 0:
                        return 0., 0, False
                    # Duplicate payload rows are ambiguous, never silently removed.
                    duplicate = bool(h.duplicated().any())
                    if not np.isfinite(h.qty).all() or h.qty.lt(0).any():
                        return np.nan, len(h), duplicate
                    return float(h.qty.sum()), len(h), duplicate
                q0, n0, dup0 = quantity(x.q0)
                q1, n1, dup1 = quantity(x.q1)
                # Original cohort/denominator faults are fatal, not q2 missingness.
                assert not dup0 and not dup1, (eid,z.fund_id,'ambiguous_original_quantity_rows')
                assert np.isfinite(q0) and q0 == 0 and np.isfinite(q1) and q1 > 0, (eid,z.fund_id,'original_cohort_changed')
                q2, n2, dup2 = quantity(x.q2)
                factor = float(sc.factor12)
                if dup2 or not np.isfinite(q2) or q2 < 0:
                    known = False
                    reason = 'unexpected_q2_duplicate_or_invalid_quantity'
                verified_absence = bool(known and n2 == 0)
            event_cells.append(dict(event_id=eid,review=x.review,ric=x.ric,fund_id=z.fund_id,
                original_q1_weight_pp=float(z.pp),original_source_supported=bool(z.source_supported),
                supported=known,unknown_reason=reason,q0=q0,q1=q1,q2=q2,factor12=factor,
                q2_source_rows=n2,verified_complete_report_absence=verified_absence))
        cells = pd.DataFrame(event_cells)
        available = cells[cells.original_source_supported]
        # q1 weights must have one common positive valuation factor within stock.
        ratios = available.original_q1_weight_pp / available.q1
        if len(ratios):
            assert np.isfinite(ratios).all() and ratios.gt(0).all()
            assert (ratios/ratios.iloc[0]-1).abs().max() < 1e-9, (eid,'q1_weight_not_proportional')
        lo, hi, overlap = bounds(cells.original_q1_weight_pp,cells.q1,cells.q2,cells.factor12,cells.supported)
        cells['capped_endpoint_fraction'] = np.where(cells.supported,overlap,np.nan)
        rows.extend(cells.to_dict('records'))
        base_width = float(source_width.loc[eid,'unknown_weight_fraction'])
        assert hi-lo + 1e-12 >= base_width
        if cells.supported.equals(cells.original_source_supported):
            assert abs(hi-lo-base_width) < 1e-12
        eventrows.append(dict(event_id=eid,review=x.review,ric=x.ric,q0=x.q0,q1=x.q1,q2=x.q2,
            original_new_positions=len(cells),source_supported_positions=int(cells.original_source_supported.sum()),
            supported_positions=int(cells.supported.sum()),verified_report_absences=int(cells.verified_complete_report_absence.sum()),
            lower_fraction=lo,upper_fraction=hi,width_fraction=hi-lo,
            source_only_width_fraction=base_width))
    L = pd.DataFrame(rows); B = pd.DataFrame(eventrows)
    V = B.groupby('review').agg(events=('event_id','size'),original_new_positions=('original_new_positions','sum'),
        supported_positions=('supported_positions','sum'),lower_fraction=('lower_fraction','mean'),
        upper_fraction=('upper_fraction','mean'),width_fraction=('width_fraction','mean')).reset_index()
    assert len(B) == 70 and len(V) == 10 and len(L) == 737
    low, high = float(V.lower_fraction.mean()), float(V.upper_fraction.mean())
    assert abs(high-low-float(V.width_fraction.mean())) < 1e-12
    result = dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        measure='Overlap between two report dates in the frozen observed new-owner cohort',
        population='All original 70 pre-2024 additions; equal event weight within review, equal review weight',
        original_events=70,reviews=10,original_new_fund_positions=len(L),
        supported_positions=int(L.supported.sum()),source_supported_positions=int(L.original_source_supported.sum()),
        unexpected_q2_source_failures=int((L.original_source_supported & ~L.supported).sum()),
        lower_percent=100*low,upper_percent=100*high,width_percentage_points=100*(high-low),
        uncertainty='Conservative logical missing-source bounds, conditional on original cohort and valid measurements; not a confidence interval',
        continuous_retention_identified=False,trade_flows_identified=False,causal_index_effect=False,
        decomposition_of_previous_F35=False,exploratory=True,no_peer_outcome=True,no_pvalue_or_sampling_CI=True,
        invariants=dict(cap_per_fund_before_sum=True,full_original_q1_denominator=True,
            all_original_events_kept=True,unit='q2/factor12 expressed in q1 shares',
            old_four_role_source_gate_unchanged=True,unknown_never_imputed_zero=True))
    L.to_csv(O/'private/FUND_ENDPOINT_AUDIT.csv.gz',index=False,compression='gzip')
    B.to_csv(O/'EVENT_BOUNDS.csv',index=False); V.to_csv(O/'REVIEW_BOUNDS.csv',index=False)
    (O/'PRIMARY_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (O/'OUTPUT_HASHES.json').write_text(json.dumps({str(p.relative_to(O)):sha(p) for p in sorted(O.rglob('*')) if p.is_file()},indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
