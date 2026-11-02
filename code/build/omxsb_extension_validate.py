"""Independent checks of the new OMXSB outputs; never changes source data.

Re-estimates reported main means/CIs with statsmodels rather than the analysis
script's hand-coded formula, and verifies measurement/accounting identities.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.repo
    base = root / 'output/omxsb_extension_20261031'
    own = base / 'ownership'
    observations = pd.read_csv(own / 'ownership_observations.csv')
    results = pd.read_csv(own / 'ownership_results.csv')
    main_obs = observations[observations.main_common_sample].copy()
    assert main_obs.event_id.is_unique
    assert main_obs.window.eq('event').all()
    assert main_obs.valid.all()
    assert main_obs.exclusion.isna().all()
    assert main_obs.denominator.gt(0).all()
    assert main_obs.review_cycle.nunique() <= 14
    for group in ['AP3', 'AP4', 'AP3_AP4_sum', 'FI_Nordnet_documented']:
        calculated = 100 * (main_obs[group + '_after_raw'] -
                           main_obs.factor * main_obs[group + '_before_raw']) / main_obs.denominator
        np.testing.assert_allclose(calculated, main_obs[group + '_delta_pp'], rtol=1e-11, atol=1e-11)
    np.testing.assert_allclose(main_obs.AP3_delta_pp + main_obs.AP4_delta_pp,
                               main_obs.AP3_AP4_sum_delta_pp, rtol=1e-11, atol=1e-11)
    np.testing.assert_allclose(main_obs.FI_Nordnet_documented_delta_pp +
                               main_obs.FI_other_than_Nordnet_delta_pp,
                               main_obs.FI_all_matched_delta_pp, rtol=1e-11, atol=1e-11)
    checked = []
    for row in results[results['sample'].eq('main_common')].itertuples():
        sub = main_obs.copy() if row.direction == 'direction_aligned_pooled' else main_obs[main_obs.type.eq(row.direction)].copy()
        col = row.group + '_delta_pp'
        sub = sub.dropna(subset=[col])
        y = sub[col] * (sub.direction if row.direction == 'direction_aligned_pooled' else 1)
        fit = sm.OLS(y.to_numpy(), np.ones((len(y), 1))).fit(
            cov_type='cluster', cov_kwds={'groups': sub.review_cycle.to_numpy(), 'use_correction': True}, use_t=True)
        ci = fit.conf_int(alpha=.05)[0]
        assert row.N == len(sub) and row.G == sub.review_cycle.nunique()
        np.testing.assert_allclose([row.mean_pp, row.se_review_cluster, row.ci95_low, row.ci95_high],
                                   [fit.params[0], fit.bse[0], ci[0], ci[1]], rtol=1e-10, atol=1e-10)
        checked.append({'direction': row.direction, 'group': row.group, 'N': int(row.N), 'G': int(row.G)})
    snapshots = pd.read_csv(own / 'ap_snapshot_resolution.csv')
    zeros = snapshots[snapshots.logical_zero]
    assert zeros.quantity.eq(0).all()
    assert zeros.status.eq('absent_from_complete_parsed_list').all()
    assert zeros.source_file.notna().all()
    assert not snapshots.duplicated(['fund', 'RIC', 'date']).any()
    fi_ledger = pd.read_csv(own / 'fi_fund_event_observations.csv.gz')
    ambiguous_rows = pd.read_csv(own / 'fi_halfyear_ambiguous_quantity_rows.csv')
    aliases = json.loads((own / 'validated_isin_aliases.json').read_text())
    ambiguity_keys = {
        ric: set(zip(z.Kvartalsslut, z.Fond_institutnummer))
        for ric, isins in aliases.items()
        for z in [ambiguous_rows[ambiguous_rows['ISIN-kod_instrument'].isin(isins)]]
    }
    for entry in fi_ledger.itertuples():
        expected_bad = ((entry.before, entry.fund_id) in ambiguity_keys.get(entry.RIC, set()) or
                        (entry.after, entry.fund_id) in ambiguity_keys.get(entry.RIC, set()))
        assert bool(entry.ambiguous_signed_or_missing_quantity) == expected_bad
        if expected_bad:
            assert entry.unit_invalid
    for event in main_obs.itertuples():
        good = fi_ledger[fi_ledger.event_id.eq(event.event_id) & fi_ledger.window.eq('event') & ~fi_ledger.unit_invalid]
        for group, mask in [('FI_all_matched', np.ones(len(good), dtype=bool)),
                            ('FI_Nordnet_documented', good.is_documented_Nordnet),
                            ('FI_original14', good.is_original14)]:
            for side in ['before', 'after']:
                total = good.loc[mask, 'quantity_' + side + '_raw'].sum()
                np.testing.assert_allclose(total, getattr(event, group + '_' + side + '_raw'), rtol=1e-11, atol=1e-9)
    for key, record in json.loads((own / 'input_hashes.json').read_text()).items():
        assert sha(root / record['path']) == record['sha256'], key
    # These two pre-existing audit outputs are explicitly protected, including
    # the original numbers beneath the label-only correction.
    protected = {
        'output/omxsb_audit_20261031/result_table.csv': '0754a129c57a3af212307784d2e14edc36ace200ea35ccc78b2e9cacfa4d3be3',
        'output/omxsb_audit_20261031/corrected/mechanisms/results_table_long.csv': '746c6b173ed69a01bb19d867b70a66a36950ec179f0c21a3ade950e8719d7adc',
    }
    for path, expected in protected.items():
        assert sha(root / path) == expected, path
    labels = json.loads((base / 'labels/validation.json').read_text())
    candidate = json.loads((base / 'candidate/pilot_summary.json').read_text())
    assert candidate['target_total'] == candidate['target_dated_nasdaq_identity_matches'] == 29
    assert candidate['original_inputs_unchanged']
    for path, expected in candidate['source_input_hashes'].items():
        assert sha(root / path) == expected
    for entry in json.loads((base / 'candidate/source_manifest.json').read_text()):
        assert sha(base / 'candidate' / entry['file']) == entry['sha256']
    migration = pd.read_csv(base / 'migration/results/migration_candidate_measurement.csv')
    assert len(migration) == 2
    assert not migration.strict_migration_verified.any()
    assert migration.raw_xml_tracker_reconciles.all()
    np.testing.assert_array_equal(migration.xact_change_shares, [117686, 14915])
    report = {'status': 'passed', 'main_events': len(main_obs), 'main_reviews': main_obs.review_cycle.nunique(),
              'main_result_cells_independently_reestimated': len(checked), 'checked_cells': checked,
              'method': 'statsmodels intercept-only OLS with CR1 review-cluster correction and t(G-1)',
              'measurement_and_accounting_identities': 'passed', 'logical_zero_status_checks': 'passed',
              'ambiguous_FI_quantities_excluded_at_both_endpoints': 'passed',
              'protected_original_audit_files_unchanged': True,
              'label_validation': labels, 'candidate_targets_verified': 29,
              'migration_candidates': 2, 'migration_candidates_are_not_finally_dated': True,
              'limits': 'Validates calculations and declared status; does not certify every historical identifier, complete corporate-action coverage or causal identification.'}
    (base / 'independent_validation.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['checked_cells', 'label_validation']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
