"""Independent source and single-estimand audit; never imports producer code.

Requires pandas/numpy/scipy/pyarrow/xlrd and locally licensed original inputs.
Only audit counts, hashes, normalized differences and already locked results output.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(4*1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def compare(actual, expected, tol=1e-9):
    a, b = np.asarray(actual, float), np.asarray(expected, float)
    assert a.shape == b.shape
    same = np.isclose(a, b, rtol=1e-11, atol=tol, equal_nan=True)
    finite = np.isfinite(a) & np.isfinite(b)
    return dict(cells=int(a.size), mismatches=int((~same).sum()),
                max_absolute_difference=float(np.max(np.abs(a[finite]-b[finite]))) if finite.any() else 0.)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path('/Users/ludviguvang/dev/financethesis'))
    parser.add_argument('--work-root', type=Path, default=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work'))
    parser.add_argument('--design', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Use a fresh output JSON; frozen reviews are not overwritten'
    repo, work = args.repo_root.resolve(), args.work_root.resolve()
    design = args.design or work/'omxsb_followthrough_20261103/design'
    sys.path.insert(0, str(design/'.deps'))
    import xlrd
    def read(name):
        return pd.read_csv(design/name)
    source_lock = json.loads((design/'SOURCE_GATE_LOCK.json').read_text())
    outcome_lock = json.loads((design/'OUTCOME_LOCK.json').read_text())
    unit_lock = json.loads((design/'UNIT_RECONCILIATION_LOCK.json').read_text())
    units = json.loads((design/'UNIT_GATE_SUMMARY.json').read_text())
    headline = json.loads((design/'PRIMARY_RESULT.json').read_text())
    def source_path(key):
        original = Path(source_lock['inputs'][key]['path'])
        if original.exists():
            return original
        text = str(original)
        if '/financethesis/' in text:
            return repo/text.split('/financethesis/', 1)[1]
        return work/text.split('/work/', 1)[1]
    source_paths = {key: source_path(key) for key in source_lock['inputs']}
    audit_lock = dict(started_utc=datetime.now(timezone.utc).isoformat(),
        role='Independent replay after the producer released the locked result; not blinded',
        no_new_estimands=True, spec_sha256=sha(design/'PRIMARY_SPEC.txt'),
        source_lock_sha256=sha(design/'SOURCE_GATE_LOCK.json'), outcome_lock_sha256=sha(design/'OUTCOME_LOCK.json'),
        reviewer_script_sha256=sha(Path(__file__)))
    lock_file = args.output.with_name(args.output.stem+'_LOCK.json')
    assert not lock_file.exists()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    lock_file.write_text(json.dumps(audit_lock, indent=2)+'\n')
    check = {}
    check['source_hashes'] = {key: sha(path) == source_lock['inputs'][key]['sha256'] for key, path in source_paths.items()}
    check['spec_pre_outcome_hash'] = sha(design/'PRIMARY_SPEC.txt') == unit_lock['primary_spec_sha256'] == outcome_lock['inputs']['spec']['sha256']
    check['producer_code_hash'] = sha(design/'run_primary.py') == outcome_lock['script_sha256']
    check['chronology'] = source_lock['created_utc'] < unit_lock['created_utc'] < outcome_lock['created_utc'] < headline['created_utc']
    roles = pd.read_csv(source_paths['roles'], usecols=['event_id','review','role','type','ric','nasdaq_isin'])
    events = pd.read_csv(source_paths['events'], usecols=['event_id','AD','ED'], parse_dates=['AD','ED'])
    roles = roles.merge(events, on='event_id', validate='many_to_one')
    assert len(roles) == 280 and roles.event_id.nunique() == 70 and roles.type.eq('addition').all()
    assert roles.groupby('event_id').role.apply(set).map(lambda x:x == {'event','c1','c2','c3'}).all()
    assert roles.groupby('event_id').ric.nunique().eq(4).all()
    observed_roles = read('ROLE_FINAL_SOURCE_GATE.csv').set_index(['event_id','role'])
    pd.testing.assert_frame_equal(roles.set_index(['event_id','role'])[['review','ric','nasdaq_isin']].sort_index(),
        observed_roles[['review','ric','nasdaq_isin']].sort_index())
    panel = pd.read_parquet(source_paths['panel'], columns=['ric','date','turnover','source'], filters=[('ric','in',sorted(roles.ric.unique()))])
    panel.date = pd.to_datetime(panel.date)
    assert not panel.duplicated(['ric','date']).any()
    book = {ric: rows.set_index('date').sort_index() for ric, rows in panel.groupby('ric')}
    index = pd.read_csv(source_paths['index'], usecols=['ric','date','close'], parse_dates=['date'])
    calendar = pd.DatetimeIndex(sorted(index.loc[index.ric.isin(['.OMXSBGI','.OMXSPI']) & index.close.gt(0), 'date'].unique()))
    cancelled = pd.read_csv(source_paths['cancel'])
    observed_unit = read('MONTHLY_TURNOVER_UNIT_FLAGS.csv').set_index(['review','ric'])
    # Read original XLS, choose exact Stockholm Stock + ISIN independently of roster row pointers.
    unit_rows, monthly_books, monthly_infinite, monthly_missing_source = [], [], 0, 0
    clean = lambda value: re.sub('[^A-Z0-9]', '', str(value).upper())
    number = lambda value: float(str(value).replace(' ', '').replace(',', '.'))
    for review, group in roles.groupby('review'):
        year, month = int(review[:4]), 4 if review.endswith('H1') else 10
        record = next(row for row in units['raw_files'] if row['review'] == review)
        path = Path(record['file'])
        if not path.exists():
            path = work/'open_questions_20261101/eligibility'/f'{year}{month:02d}.xls'
        assert sha(path) == record['sha256']
        sheet = xlrd.open_workbook(path).sheet_by_name('Instrument Trading Details')
        header = [i for i in range(10) if 'ISIN' in sheet.row_values(i) and 'Instrument' in sheet.row_values(i)]
        assert len(header) == 1
        h = header[0]
        columns = {}
        for j, value in enumerate(sheet.row_values(h)):
            columns.setdefault(clean(value), []).append(j)
        cisin, ctype, cloc, ccur = [columns[x][0] for x in ['ISIN','INSTRUMENTTYPE','LOCATION','CURRENCY']]
        cturn, cdays = columns['TOTALTURNOVER'][0], columns['LISTEDDAYS'][0]
        assert cturn+1 == record['monthly_turnover_column'] and cdays+1 == record['monthly_listed_days_column']
        # Verify the enclosing header is current month/on-exchange, not YTD, trailing-year or OTC.
        month_label = 'April' if month == 4 else 'October'
        assert f'{month_label} {year}' in str(sheet.cell_value(h-2, cdays))
        assert ' - ' not in str(sheet.cell_value(h-2, cdays))
        assert 'On Exchange Turnover' in str(sheet.cell_value(h-1, cdays))
        monthly_books.append(dict(review=review, file_sha256=sha(path), header_row=h+1,
            current_month_column=cturn+1, listed_days_column=cdays+1, monthly_on_exchange_header_verified=True))
        for ric, isin in group[['ric','nasdaq_isin']].drop_duplicates().itertuples(index=False, name=None):
            hits = [i for i in range(h+1,sheet.nrows) if sheet.cell_value(i,cisin) == isin
                    and sheet.cell_value(i,ctype) == 'Stock' and sheet.cell_value(i,cloc) == 'STO']
            assert len(hits) == 1
            row = hits[0]
            amount, listed = number(sheet.cell_value(row,cturn)), number(sheet.cell_value(row,cdays))
            currency = str(sheet.cell_value(row,ccur))
            p = book[ric]
            q = p.loc[(p.index.year == year) & (p.index.month == month)]
            values = q.turnover.to_numpy(float)
            finite = np.isfinite(values)
            monthly_infinite += int(np.isinf(values).sum())
            monthly_missing_source += int(q.source.isna().sum())
            error = np.nansum(values)/amount-1 if amount > 0 else np.nan
            passed = (currency == 'SEK' and amount > 0 and np.isfinite(error) and abs(error) <= .001
                      and int(finite.sum()) >= listed and not np.any(values[finite] < 0)
                      and q.source.eq('tr').all() and not np.isinf(values).any())
            observed = observed_unit.loc[(review,ric)]
            assert row+1 == observed.source_excel_row and currency == observed.currency
            assert bool(observed.unit_pass) == passed
            assert np.isclose(error, observed.monthly_relative_error, rtol=1e-10, atol=1e-12, equal_nan=True)
            unit_rows.append(dict(review=review, ric=ric, unit_pass=passed, row_pointer_matches=True,
                                  currency=currency, monthly_numeric_finite_count=int(finite.sum())))
    monthly = pd.DataFrame(unit_rows).set_index(['review','ric'])
    check['monthly_original_source_reconstruction'] = dict(checks=len(monthly), passed=int(monthly.unit_pass.sum()),
        failures=int((~monthly.unit_pass).sum()), all_flags_and_errors_match=True, infinite_values=monthly_infinite,
        missing_source_rows=monthly_missing_source, original_header_checks=monthly_books)
    gate, windows, infinite95 = [], {}, 0
    for role in roles.itertuples():
        ai, ei = calendar.get_loc(role.AD), calendar.get_loc(role.ED)
        baseline_last = min(ai-12,ei-23)
        assert baseline_last >= 49 and ei >= 22 and ei+22 < len(calendar)
        bdays, wdays = calendar[baseline_last-49:baseline_last+1], calendar[ei-22:ei+23]
        target = calendar[ei-1]
        assert len(bdays)==50 and len(wdays)==45 and not set(bdays)&set(wdays) and bdays.max()<role.AD
        p = book[role.ric]
        b, w = p.reindex(bdays), p.reindex(wdays)
        bv, wv = b.turnover.to_numpy(float), w.turnover.to_numpy(float)
        infinite95 += int(np.isinf(bv).sum()+np.isinf(wv).sum())
        cancelled_control = role.role != 'event' and bool((cancelled.review.eq(role.review) & cancelled.RIC.eq(role.ric)).any())
        present = bool(np.isfinite(bv).all() and np.isfinite(wv).all() and (bv>=0).all() and (wv>=0).all()
                       and (bv>0).any() and b.source.eq('tr').all() and w.source.eq('tr').all() and not cancelled_control)
        monthly_ok = bool(monthly.loc[(role.review,role.ric),'unit_pass'])
        passed = present and monthly_ok
        stored = observed_roles.loc[(role.event_id,role.role)]
        assert present == stored.turnover_presence_pass and passed == stored.cash_gate_pass
        for col,value in [('baseline_start',bdays[0]),('baseline_end',bdays[-1]),('window_start',wdays[0]),('window_end',wdays[-1])]:
            assert pd.Timestamp(stored[col]) == value
        gate.append(dict(event_id=role.event_id, review=role.review, role=role.role, pass_source=passed))
        windows[(role.event_id,role.role)] = (bdays,wdays,target)
    gate = pd.DataFrame(gate)
    event_pass = gate.groupby('event_id').pass_source.all()
    saved_pass = read('EVENT_FINAL_SOURCE_GATE.csv').set_index('event_id').gate_pass
    assert event_pass.sort_index().equals(saved_pass.sort_index())
    selected = set(event_pass.index[event_pass])
    check['common_support_reconstruction'] = dict(original_roles=len(roles), role_checks=len(gate), events=len(event_pass),
        passed_events=len(selected), failed_events=sorted(set(event_pass.index)-selected), infinite_values_95day_roles=infinite95,
        all_four_role_gates_match=True, baseline_and_window_dates_match=True, no_baseline_window_overlap=True)
    raw_export = read('private/RAW_RELEVANT_TURNOVER.csv.gz')
    raw_export.date = pd.to_datetime(raw_export.date)
    assert not raw_export.duplicated(['event_id','role','date']).any()
    expected_rows, role_results = [], []
    for role in roles[roles.event_id.isin(selected)].itertuples():
        bd, wd, target = windows[(role.event_id,role.role)]
        bv = book[role.ric].loc[bd,'turnover'].to_numpy(float)
        wv = book[role.ric].loc[wd,'turnover'].to_numpy(float)
        base = np.sum(bv)/50
        normalized = wv/base-1
        target_index = list(wd).index(target)
        result = dict(event_id=role.event_id, review=role.review, role=role.role, ric=role.ric,
            total45=float(np.sum(normalized)), day_EDminus1=float(normalized[target_index]),
            other44=float(np.sum(np.delete(normalized,target_index))))
        role_results.append(result)
        for period, dates in [('baseline',bd),('window',wd)]:
            for date in dates:
                expected_rows.append(dict(event_id=role.event_id,review=role.review,role=role.role,ric=role.ric,date=date,
                    period=period,is_EDminus1=date==target,source=book[role.ric].loc[date,'source'],turnover=book[role.ric].loc[date,'turnover']))
    raw_keys = ['event_id','role','date']
    expected_raw = pd.DataFrame(expected_rows).set_index(raw_keys).sort_index()
    exported = raw_export.set_index(raw_keys).sort_index()
    pd.testing.assert_frame_equal(expected_raw.drop(columns='turnover'),exported.drop(columns='turnover'),check_like=True)
    check['private_export_matches_original_panel'] = compare(expected_raw.turnover,exported.turnover,tol=1e-7)
    components=['total45','day_EDminus1','other44']
    role_results=pd.DataFrame(role_results).set_index(['event_id','role']).sort_index()
    stored_roles=read('NORMALIZED_ROLE_COMPONENTS.csv').set_index(['event_id','role']).sort_index()
    check['normalized_role_components'] = compare(role_results[components],stored_roles[components])
    matched=[]
    for event_id,g in role_results.reset_index().groupby('event_id'):
        r=g.set_index('role')
        value=r.loc['event',components]-r.loc[['c1','c2','c3'],components].sum()/3
        matched.append(dict(event_id=event_id,review=r.review.iloc[0],**value.to_dict()))
    matched=pd.DataFrame(matched).set_index('event_id').sort_index()
    stored_events=read('EVENT_COMPONENTS.csv').set_index('event_id').sort_index()
    check['matched_event_components']=compare(matched[components],stored_events[components])
    review=matched.groupby('review')[components].mean().sort_index()
    stored_review=read('REVIEW_COMPONENTS.csv').set_index('review').sort_index()
    check['review_components']=compare(review,stored_review[components])
    assert matched.groupby('review').size().equals(stored_review.N_events)
    g=len(review)
    means=review.mean()
    centered=review.to_numpy()-means.to_numpy()
    cov=centered.T@centered/(g*(g-1))
    saved_cov=pd.read_csv(design/'JOINT_COVARIANCE_OF_MEANS.csv',index_col=0).loc[components,components]
    check['covariance_of_review_means']=compare(cov,saved_cov,tol=1e-10)
    se=np.sqrt(cov[0,0]); margin=t.ppf(.975,g-1)*se
    rebuilt=[means.total45,se,means.total45-margin,means.total45+margin,means.day_EDminus1,means.other44]
    published=[headline['primary_total45_mean'],headline['primary_SE_review_means'],*headline['primary_CI95'],headline['descriptive_day_EDminus1_mean'],headline['descriptive_other44_mean']]
    check['primary_result_and_descriptive_levels']=compare(rebuilt,published,tol=1e-10)
    check['additive_identity_max_error']=float(np.max(np.abs(role_results.total45-role_results.day_EDminus1-role_results.other44)))
    check['covariance_identity_error']=float(abs(cov[0,0]-cov[1,1]-cov[2,2]-2*cov[1,2]))
    check['N_G_df'] = dict(events=len(matched),reviews=g,df=g-1)
    check['no_component_intervals_or_pvalues'] = not headline['p_values_reported'] and not headline['component_intervals_reported']
    def good(value):
        if isinstance(value,dict):
            return value.get('mismatches',0)==0 and all(good(v) for k,v in value.items() if k!='mismatches')
        return bool(value) if isinstance(value,bool) else True
    report=dict(completed_utc=datetime.now(timezone.utc).isoformat(),status='PASS' if good(check) else 'FAIL',
        scope='Independent raw-panel and ten original monthly-XLS reconstruction of locked source gate and one released contrast',
        audit_lock=audit_lock,checks=check,
        result=dict(total45=float(means.total45),CI95=[float(means.total45-margin),float(means.total45+margin)],
                    descriptive_day=float(means.day_EDminus1),descriptive_other44=float(means.other44)),
        limitations=['Nominal exploratory interval after many prior analyses; lower bound is very near zero.',
            'Prior ownership-covered70 additions;65source-complete events, not all additions.',
            'Review-t conditional on independent reviews; repeated issuers/controls and common regimes remain.',
            'Gross SEK amount includes price changes and venue effects; not net demand, share quantity, or index causation.',
            'Monthly reconciliation and dated SEK identity do not prove daily field basis throughout every measurement window.',
            'Latent notna versus finite and dropna-source guard weaknesses checked against actual data; no frozen result changed.'])
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))
    assert report['status']=='PASS'


if __name__=='__main__':
    main()
