"""Source-only replay to a NEW directory; never modifies frozen outputs/raw inputs.

Uses the original predeclared validator functions, then the independent Decimal
comparison. No network, price-level exports, midpoint or auction-return estimate.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists(), 'Use a new replay directory'
    a.output.mkdir(parents=True)
    here = Path(__file__).resolve().parent
    raw = a.repo_root/'data/raw/shof/Reinvestments/hft_revisit_20261104'
    files = {k:raw/f'NASDAQ_2nd_level_orderbook_{k}.csv.zip' for k in ['1793788245204','1793789997030','1793790402104']}
    expected = {'1793788245204':'262b1f9d09c3060f69b1999f27424c30f09dae3754e5f58e5ebc79e504a2919e',
        '1793789997030':'b6851383d3ef989ee9cb8e2fa89d7c56cea3148e9c50a1f28dc94ffd12b91d0b',
        '1793790402104':'d08dd0e219899d7959d261a67a3f7fce76697dbcb18addba0c84d65f0f7d8018'}
    for key, file in files.items():
        assert hashlib.sha256(file.read_bytes()).hexdigest()==expected[key]
    validator = a.repo_root/'output/omxsb_scaled_round_20261103/auction_design/validate_sampled_export.py'
    assert hashlib.sha256(validator.read_bytes()).hexdigest()=='e0df3e1b512f15189422a4d0ec37d426ac7e2aad85804b54868434b26451bc24'
    spec = importlib.util.spec_from_file_location('fixed_source_validator', validator)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    main_inputs=[files['1793788245204'],files['1793790402104']]
    data=module.pd.concat([module.load(x) for x in main_inputs],ignore_index=True)
    checks=[]
    for isin,date,ident in module.FIXED:
        sampled=data.loc[data['isin'].eq(isin)&data.date.eq(date)].copy().reset_index(drop=True)
        assert not sampled.empty
        fullpath=a.repo_root/'data/raw/shof/Reinvestments/hft_pilot_20261103'/f'NASDAQ_2nd_level_orderbook_{ident}.csv.zip'
        full=module.load(fullpath)
        assert set(sampled.currency)=={'SEK'} and set(sampled.market)=={'XSTO'}
        assert set(full['isin'])=={isin} and set(full.date)=={date}
        checks.append(dict(ISIN=isin,date=date,full_source_sha256=module.sha(fullpath),status='compared',**module.compare(full,sampled,60)))
    selected={(i,d) for i,d,_ in module.FIXED}
    result=dict(created_utc=datetime.now(timezone.utc).isoformat(),source_only=True,
        no_new_auction_premiums=True,interval='minute',absolute_comparison_tolerance=module.TOL,
        inputs={str(x):module.sha(x) for x in main_inputs},script_sha256=module.sha(validator),
        ignored_extra_instrument_days=sorted(set(zip(data['isin'],data.date))-selected),fixed_checks=checks,
        all_five_terminal_last_snapshot_equivalent=all(x['coherent_last_snapshot_terminal_equivalence'] for x in checks),
        all_five_original_terminal_update_times_retained=all(x['source_supported_original_freshness'] for x in checks),
        broad_outcome_gate='NOT_OPENED: source assessment, dated identities/overlaps and actual common support must be frozen first')
    (a.output/'FIVE_DAY_PREDECLARED_VALIDATOR.json').write_text(json.dumps(result,indent=2)+'\n')
    run=lambda script,args:subprocess.run([sys.executable,str(here/script),*map(str,args)],check=True)
    run('compare_bins.py',['--repo-root',a.repo_root,'--input',*main_inputs,'--out',a.output/'FIVE_DAY_BIN_ORDERING_CHECK.json'])
    run('compare_overlap.py',['--first',files['1793789997030'],'--second',files['1793790402104'],'--out',a.output/'CAMX_OVERLAP_EQUALITY.json'])
    run('inventory_delivery.py',['--input',files['1793790402104'],'--requested-isin','SE0007692850','SE0005999836','--date-from','2023-11-23','--date-to','2023-11-30','--out',a.output/'COMBINED_DELIVERY_INVENTORY.json'])
    run('inventory_delivery.py',['--input',files['1793789997030'],'--requested-isin','SE0007692850','--date-from','2023-11-23','--date-to','2023-11-23','--out',a.output/'CAMX_DELIVERY_INVENTORY_REPLAY.json'])
    print('Source-only replay complete; compare counts/flags/hashes, ignoring timestamps and relocated absolute paths.')


if __name__=='__main__':
    main()
