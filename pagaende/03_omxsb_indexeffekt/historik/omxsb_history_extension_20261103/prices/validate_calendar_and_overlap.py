"""Source-unit/calendar checks only: no financial return calculation."""
from pathlib import Path
import os
from datetime import date,timedelta
from dateutil.easter import easter
import pandas as pd,numpy as np,json
O=Path(os.environ.get('OMXSB_PRICE_WORKDIR',Path(__file__).resolve().parent));P=O/'private'
old=pd.read_csv(P/'EXISTING_PANEL_REUSE.csv.gz');new=pd.read_csv(P/'FETCHED_NORMALIZED_LONG.csv.gz')
x=old.merge(new,on=['ric','date'],suffixes=('_old','_new'));out=[]
for ric,g in x.groupby('ric'):
 a=pd.to_numeric(g.close_old,errors='coerce');b=pd.to_numeric(g.close_new,errors='coerce');ok=a.notna()&b.notna()&a.gt(0)&b.gt(0);ratio=a[ok]/b[ok];scale=float(ratio.median())if len(ratio)else None
 equal=np.isclose(a[ok],b[ok],rtol=1e-8,atol=1e-10);constant=bool(np.isclose(ratio,scale,rtol=1e-6,atol=1e-10).all())if len(ratio)else False
 oa=pd.to_numeric(g.totret_old,errors='coerce');nb=pd.to_numeric(g.totret_new,errors='coerce');rr=oa.notna()&nb.notna()
 out.append({'ric':ric,'overlap_rows':len(g),'positive_close_overlap':int(ok.sum()),'close_equal_rtol1e_8':int(equal.sum()),'close_all_equal':bool(equal.all())if len(equal)else False,'old_over_new_close_median_scale':scale,'old_over_new_close_min_scale':float(ratio.min())if len(ratio)else None,'old_over_new_close_max_scale':float(ratio.max())if len(ratio)else None,'constant_scale_rtol1e_6':constant,'legacy_totret_vs_new_dailyreturn_common_numeric':int(rr.sum()),'legacy_totret_vs_new_dailyreturn_equal_rtol1e_8':int(np.isclose(oa[rr],nb[rr],rtol=1e-8,atol=1e-10).sum())})
Q=pd.DataFrame(out);Q.to_csv(O/'OVERLAP_EQUIVALENCE_METADATA.csv',index=False)
I=pd.read_csv(P/'FETCHED_INDICES_LONG.csv.gz');I.date=pd.to_datetime(I.date);sets={k:set(g.loc[g.close.notna(),'date'].dt.date)for k,g in I.groupby('ric')}
gi=sets.get('.OMXSBGI',set());spi=sets.get('.OMXSPI',set());a=min(gi|spi);b=max(gi|spi)
# Transparent fixed-date probes; this is not claimed to certify all historical exchange closures.
holidays={}
for year in range(a.year,b.year+1):
 fixed=[(1,1,'NewYear'),(1,6,'Epiphany'),(5,1,'MayDay'),(12,24,'ChristmasEve'),(12,25,'Christmas'),(12,26,'BoxingDay'),(12,31,'NewYearEve')]
 for m,d,label in fixed:holidays[date(year,m,d)]=label
 e=easter(year)
 for delta,label in [(-2,'GoodFriday'),(1,'EasterMonday'),(39,'Ascension')]:holidays[e+timedelta(days=delta)]=label
 midsummer=date(year,6,19)
 while midsummer.weekday()!=4:midsummer+=timedelta(days=1)
 holidays[midsummer]='MidsummerEve'
 # Change in Swedish statutory holidays is separated from full exchange-calendar certification.
 if year>=2005:holidays[date(year,6,6)]='NationalDay_from2005'
 else:holidays[e+timedelta(days=50)]='WhitMonday_before2005'
cal={'period_start':str(a),'period_end':str(b),'native_GI_numeric_dates':len(gi),'pricing_SPI_numeric_dates':len(spi),'GI_only_dates':[str(d)for d in sorted(gi-spi)],'SPI_only_dates':[str(d)for d in sorted(spi-gi)],'union_dates':len(gi|spi),'weekend_numeric_dates':{k:[str(d)for d in sorted(v)if d.weekday()>=5]for k,v in sets.items()},'holiday_probe_numeric_dates':{k:[{'date':str(d),'label':holidays[d]}for d in sorted(v)if d in holidays]for k,v in sets.items()},'holiday_probe_scope':'Transparent recurring full-closure probes, not an independently verified2001–2006 historical exchange calendar; half-days are retained. Native/pricing source-date union can reveal gaps; no GI fill or imputed zero.', 'date_lists':[{'date':str(d),'GI_present':d in gi,'SPI_present':d in spi}for d in sorted(gi|spi)]}
pd.DataFrame(cal.pop('date_lists')).to_csv(O/'BENCHMARK_DATE_PRESENCE.csv',index=False)
(O/'CALENDAR_CHECK.json').write_text(json.dumps(cal,indent=2)+'\n')
s={'overlap_RICs':len(Q),'RICs_with_positive_overlap':int(Q.positive_close_overlap.gt(0).sum()),'RICs_all_close_equal':int(Q.close_all_equal.sum()),'RICs_constant_scale':int(Q.constant_scale_rtol1e_6.sum()),'RICs_nonconstant_scale':Q.loc[Q.positive_close_overlap.gt(0)&~Q.constant_scale_rtol1e_6,'ric'].tolist(),'price_source_boundary_rule':'Do not compute price-only returns across old/new source boundaries unless overlap adjustment/identity is separately certified. Matching daily numeric values on overlap is a source consistency check, not a guarantee for nonoverlap historical corp actions.','calendar':cal}
(O/'SOURCE_EQUIVALENCE_SUMMARY.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
