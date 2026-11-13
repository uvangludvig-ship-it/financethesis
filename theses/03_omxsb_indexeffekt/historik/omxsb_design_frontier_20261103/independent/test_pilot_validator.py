"""Synthetic source-bug checks. No licensed numerical data used."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json,datetime
import pandas as pd

O=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='synthetic_source_test_',dir=O) as tmp:
    t=Path(tmp);shutil.copy2(O/'validate_acquisition_pilot.py',t/'validate_acquisition_pilot.py')
    pd.DataFrame([dict(FI_fund_id='TEST',fundid='TESTFUND',performanceid='TESTCLASS',ISIN='SYNTHETIC',inceptiondate='2010-01-01',obsoletedate=None)]).to_csv(t/'ACQUISITION_PILOT_CLASSES.csv',index=False)
    # Last record exists but TNA/NF are missing. Prior actual TNA row is duplicated.
    base=dict(performanceId='TESTCLASS',classcurrencyiso='SEK',fundcurrencyiso='SEK',netflowclass=None,netflowfund=None,shares=10)
    v=pd.DataFrame([dict(base,date='2019-01-29',tnaclass=100,tnafund=100),dict(base,date='2019-01-29',tnaclass=100,tnafund=100),dict(base,date='2019-01-31',tnaclass=None,tnafund=None),dict(base,date='2024-01-31',tnaclass=999,tnafund=999)])
    v.to_csv(t/'synthetic_valuations.csv',sep=';',index=False)
    r=pd.DataFrame([dict(performanceId='TESTCLASS',date='2019-01-29',returntype=1,unit_SEK=100,unit_BAS=100),dict(performanceId='TESTCLASS',date='2019-01-31',returntype=1,unit_SEK=None,unit_BAS=None),dict(performanceId='TESTCLASS',date='2019-01-31',returntype=18,unit_SEK=999,unit_BAS=999),dict(performanceId='TESTCLASS',date='2024-01-31',returntype=1,unit_SEK=888,unit_BAS=888)])
    r.to_csv(t/'synthetic_rips.csv',sep=';',index=False)
    proc=subprocess.run([sys.executable,str(t/'validate_acquisition_pilot.py'),'--valuations',str(t/'synthetic_valuations.csv'),'--rips',str(t/'synthetic_rips.csv')],text=True,capture_output=True,check=True)
    a=pd.read_csv(t/'PILOT_VALUATIONS_MONTH_METADATA.csv').iloc[0];b=pd.read_csv(t/'PILOT_RIPS_MONTH_METADATA.csv').iloc[0];s=json.loads((t/'PILOT_ACQUISITION_VALIDATION.json').read_text())
    checks={
      'TNA_actual_last_observation_not_recordmax':a.last_record=='2019-01-31' and a.tnaclass_last_date=='2019-01-29' and a.tnafund_last_date=='2019-01-29',
      'duplicate_class_date_detected':a.duplicate_id_date_rows==2 and a.rows==3 and a.distinct_dates==2,
      'allmissing_NF_has_zero_observationcount_and_missing_dates':a.netflowclass_observations==0 and a.netflowfund_observations==0 and pd.isna(a.netflowclass_first_date) and pd.isna(a.netflowclass_last_date) and pd.isna(a.netflowfund_last_date),
      'no_flow_value_column_or_numeric_flow_result':not any(c in ['netflowclass','netflowfund','flow','flow_rate'] for c in a.index),
      'TRI_actual_last_observation_not_recordmax':b.last_record=='2019-01-31' and b.unit_sek_last_date=='2019-01-29' and b.unit_sek_observations==1,
      'taxadjusted_type_not_substituted_for_totalreturn':b.rows==2 and s['rips']['returntypes_in_filtered_source'].get('18')==1,
      'post2023_observations_excluded':s['valuations']['outside_2017_2023_rows_ignored']==1 and s['rips']['outside_2017_2023_rows_ignored']==1,
    }
    checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
    out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'synthetic_only':True,'licensed_numerical_data_used':False,'checks':checks,'all_pass':True,'fixtures':'Generated in temporary subfolder by this script, then deleted. Values are invented.'}
    (O/'PILOT_VALIDATOR_SYNTHETIC_TESTS.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
