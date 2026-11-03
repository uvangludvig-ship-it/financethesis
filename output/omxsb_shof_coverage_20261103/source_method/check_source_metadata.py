"""Identity, source-presence and dates only; no return/flow/risk arithmetic."""
from pathlib import Path
import pandas as pd, json, hashlib, datetime, zipfile, io
O=Path(__file__).resolve().parent
R=Path('/Users/ludviguvang/dev/financethesis')
CHAT=Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke')
M=R/'data/raw/shof/fundmaster.xlsx'
FX=R/'data/raw/lseg/panel_eu/fx_sek_daily.csv'
FLAGS=CHAT/'work/shof_pilot_20261103/audit/NEW_CLASS_MONTH_SOURCE_FLAGS.csv'
RIPS=CHAT/'work/shof_pilot_20261103/audit/PILOT_RIPS_CLASS_METADATA.csv'
P=R/'data/raw/shof/Reinvestments/coverage_20261103/Prices/FUNDS_PRICES_1793726853862.zip'
DEFS=R/'data/raw/shof/shof_field_definitions.txt'
want=['0P00016KI8','0P0000MWNE','0P0001PD6Z','0P0001P1OC','0P0001P1OD','0P0001P1OE']
cols=['performanceid','secid','fundid','shareclasslegalname','ISIN','inceptiondate','currencyid','incomedistribution','accumulateddistribution','trackrecordinheritedfrom']
m=pd.read_excel(M,usecols=cols);m=m[m.performanceid.isin(want)]
flags=pd.read_csv(FLAGS);rips=pd.read_csv(RIPS)
records=[]
for r in m.to_dict('records'):
 z=flags[flags.performanceid.eq(r['performanceid'])]
 inc=str(r['inceptiondate'])[:10];pre=z[z.ym.lt(inc[:7])]
 valid=z[z.tnaclass_present.fillna(False).astype(bool)]
 rr=rips[rips.performanceid.eq(r['performanceid'])]
 r.update(inceptiondate=inc,preinception_months_with_positive_classTNA=int(pre.tnaclass_present.fillna(False).astype(bool).sum()),first_audited_monthly_classTNA_date=valid.tnaclass_date.min() if len(valid) else None,first_raw_RIP_date=rr.first_date.iloc[0] if len(rr) else None,source='current master + previously audited source metadata',historical_no_distribution_proven=False)
 records.append(r)
pd.DataFrame(records).to_csv(O/'evidence.csv',index=False)
fx=pd.read_csv(FX,usecols=['pair','date']);fx=fx[fx.pair.eq('NOKSEK=')]
fxmeta=dict(pair='NOKSEK=',rows=len(fx),first_date=fx.date.min(),last_date=fx.date.max(),rates_loaded=False,quote_orientation_verified=False)
with zipfile.ZipFile(P) as z:
 names=[x for x in z.namelist() if x.lower().endswith('.csv')];assert len(names)==1
 d=pd.read_csv(io.BytesIO(z.read(names[0])),sep=';',usecols=lambda x:x.lower() in ['performanceid','date','pretaxnav','unsplit'],dtype=str)
d.columns=d.columns.str.lower();d.date=d.date.str.slice(0,10);d=d[d.date.between('2017-01-01','2023-12-31')]
pr=[]
for pid,g in d.groupby('performanceid'):
 a=dict(performanceid=pid,duplicate_dates=int(g.date.duplicated().sum()),first_date=g.date.min(),last_date=g.date.max())
 for c in ['pretaxnav','unsplit']:
  good=pd.to_numeric(g[c],errors='coerce').gt(0);a[c+'_positive_rows']=int(good.sum());a[c+'_positive_months']=g.loc[good,'date'].str.slice(0,7).nunique()
 pr.append(a)
meta=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Source metadata only; no return flow covariance or risk arithmetic',fx=fxmeta,prices=pr,nav_as_totalreturn_certified=False,dividend_and_split_completeness_pending=True,inputs={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [M,FX,FLAGS,RIPS,P,DEFS,O/'SOURCE_RULE_D.txt']})
(O/'METADATA_AUDIT.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'fx':fxmeta,'prices':pr,'no_returns_flows_or_risk_calculated':True},indent=2))
