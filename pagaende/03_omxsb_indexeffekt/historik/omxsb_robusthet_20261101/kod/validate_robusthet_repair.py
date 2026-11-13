"""Validate saved repaired results without recomputing returns or selecting specifications."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

REPO=Path(__file__).resolve().parents[2]
OUT=REPO/'output/omxsb_robusthet_20261101'


def main():
    checks={}
    R=pd.read_csv(OUT/'results.csv')
    M=pd.read_csv(OUT/'T2_matches.csv')
    numerical=[]
    for row in R[R.test=='T2_panel_match'].itertuples():
        pv=0 if row.period=='before2017' else 1
        q=M[(M.type==row.type)&(M.post==pv)].dropna(subset=[row.variant])
        g=q.groupby('review')[row.variant].mean()
        fit=sm.OLS(g.values,np.ones((len(g),1))).fit()
        ci=fit.conf_int(alpha=.05)[0]
        np.testing.assert_allclose([row.estimate_pp,row.ci_lo,row.ci_hi],[fit.params[0],ci[0],ci[1]],atol=1e-10)
        assert row.N==len(q) and row.G==len(g)
        assert 0<row.p_wild<=1 and 0<row.p_signflip<=1
        numerical.append(dict(type=row.type,period=row.period,variant=row.variant,
                              independently_recomputed_estimate=float(fit.params[0]),max_difference=float(np.max(np.abs(np.array([row.ci_lo,row.ci_hi])-ci)))))
    checks['T2_independent_statsmodels_checks']=numerical
    for row in M.itertuples():
        ids=[getattr(row,f'c{j}_issuer') for j in range(1,4) if pd.notna(getattr(row,f'c{j}_issuer',np.nan))]
        assert len(ids)==len(set(ids)) and row.issuer not in ids
        cc=np.array([getattr(row,f'c{j}_car',np.nan) for j in range(1,4)])
        if not np.isfinite(cc).all(): assert pd.isna(row.diff3)
    checks['control_issuer_and_missing_outcome_invariants']='passed'
    clocks=pd.read_csv(OUT/'window_clock.csv')
    assert (pd.to_datetime(clocks.pre_end)<pd.to_datetime(clocks.outcome_start)).all()
    assert (pd.to_datetime(clocks.covariate_day)<pd.to_datetime(clocks.outcome_start)).all()
    checks['nonoverlapping_predictor_and_outcome_dates']='passed'
    old=pd.read_csv(REPO/'archive/robusthet_repair_20261101/robusthet_hela_resultat/T2_hela_events.csv')
    comparison=M.merge(old[['event_id','car']],on='event_id',suffixes=('_new','_old')).dropna(subset=['car_new','car_old'])
    np.testing.assert_allclose(comparison.car_new,comparison.car_old,atol=1e-10)
    checks['unchanged_event_CAR_on_old_common_sample']=len(comparison)
    meta=json.loads((OUT/'run_metadata.json').read_text())
    if meta['T5_status']=='not_estimable_membership_unresolved':
        assert R.loc[R.test=='T5_exploratory_proxy','estimate_pp'].isna().all()
        assert pd.read_csv(OUT/'T5_proxy_preselected.csv').empty
        assert pd.read_csv(OUT/'T5_analysis_samples.csv').empty
    checks['T5_blocked_rows_are_missing_not_zero']='passed'
    gate=json.loads((OUT/'first_stage_validation/first_stage_validation.json').read_text())
    f=pd.read_csv(OUT/'first_stage_validation/first_stage_validation.csv')
    assert not gate['economic_computation_performed'] and not gate['legacy_0_74_pp_validated']
    assert f[['event_class_chg_pct','sister_chg_mn','sister_hold_before_mn']].isna().all().all()
    checks['first_stage_unknown_values_not_reported_as_zero']='passed'
    original=json.loads((REPO/'archive/robusthet_repair_20261101/original_sha256.json').read_text())
    for relative,digest in original.items():
        actual=hashlib.sha256((REPO/'archive/robusthet_repair_20261101'/relative).read_bytes()).hexdigest()
        assert actual==digest,relative
    checks['original_archived_hashes_unchanged']=len(original)
    testfiles=['code/build/test_robusthet_repair.py','code/claude_checks/test_twin_first_stage.py']
    for relative in testfiles:
        result=subprocess.run([sys.executable,str(REPO/relative)],capture_output=True,text=True)
        assert result.returncode==0,result.stdout+result.stderr
        checks[relative]=result.stderr.strip()
    for relative in ['robusthet_hela_panelen.ipynb','code/notebooks/robusthet_hela_panelen.ipynb']:
        notebook=json.loads((REPO/relative).read_text())
        for i,cell in enumerate(notebook['cells']):
            if cell['cell_type']=='code':compile(''.join(cell['source']),relative+str(i),'exec')
        assert not any(cell.get('outputs') for cell in notebook['cells'])
    checks['notebook_cells_compile_and_have_no_stale_outputs']='passed'
    checks['status']='passed'
    (OUT/'validation.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in checks.items() if isinstance(v,(str,int)) and not k.endswith('.py')},ensure_ascii=False))


if __name__=='__main__':main()
