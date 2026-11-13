"""Run ONLY in an already authenticated LSEG/Refinitiv notebook session.
No session is opened; no configuration, credential or environment variable is read.
Usage in that notebook: from lseg_complement_pilot import run_pilot; run_pilot(ld, 'complement_pilot')
This is a field/identity diagnostic. It never computes demand or returns.
"""
from pathlib import Path
import datetime,json,hashlib

def run_pilot(ld,out):
    session=ld.session.get_default()
    if session is None:
        raise RuntimeError('No existing authenticated session; pilot stopped without opening one.')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    # Original three field-test securities; one predeclared date each.
    cases=[('VOLVa.ST','2015-05-29'),('BILIa.ST','2015-05-29'),('BOSS.ST^D08','2007-05-29'),('SINCH.ST','2020-12-31')]
    candidates=['TR.FundPortfolioName','TR.FundHoldingsDate','TR.FundAdjShrsHeld',
                'TR.FundAsRepShrsHeld','TR.FdAdjPctOfShrsOutHeld','TR.FdAdjSharesHeldValue',
                'TR.FundAdjShrsHeld.InvestorPermID']
    before={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':cases,'fields':candidates,
            'not_tested_here':True,'note':'Correct syntax does not establish complete fund portfolios, valid zero absence or historical mandate.'}
    lock=out/'REQUEST_LOCK.json'
    if lock.exists():raise RuntimeError('Existing pilot folder; do not overwrite raw requests.')
    lock.write_text(json.dumps(before,indent=2));rows=[]
    for ric,date in cases:
        successful=[]
        for field in candidates:
            rec={'ric':ric,'asof':date,'field':field,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
            try:
                df=ld.get_data(universe=[ric],fields=[field],parameters={'SDate':date,'EndNum':10000})
                fn=f'{ric.replace("^","_")}_{date}_{field.replace(".","_")}.csv'
                df.to_csv(out/fn,index=False);rec.update(status='returned',rows=len(df),file=fn,sha256=hashlib.sha256((out/fn).read_bytes()).hexdigest())
                cols=[c for c in df if c.lower()!='instrument']
                if cols and df[cols].notna().any(axis=1).any():successful.append(field)
            except Exception as exc:
                rec.update(status='error',error_type=type(exc).__name__) # no credential-bearing exception string
            rows.append(rec)
        if successful:
            try:
                df=ld.get_data(universe=[ric],fields=successful,parameters={'SDate':date,'EndNum':10000})
                fn=f'{ric.replace("^","_")}_{date}_combined.csv';df.to_csv(out/fn,index=False)
                rows.append({'ric':ric,'asof':date,'field':'combined_successful_fields','status':'returned','rows':len(df),'file':fn,'sha256':hashlib.sha256((out/fn).read_bytes()).hexdigest()})
            except Exception as exc:rows.append({'ric':ric,'asof':date,'field':'combined_successful_fields','status':'error','error_type':type(exc).__name__})
    (out/'REQUEST_RESULTS.json').write_text(json.dumps(rows,indent=2));return rows
