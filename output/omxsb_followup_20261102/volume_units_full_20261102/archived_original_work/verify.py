from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd
from scipy.stats import t
import xlrd,openpyxl
O=Path(__file__).resolve().parent;C=O.parents[1]
g=pd.read_csv(O/'unit_gate_all216.csv');m=pd.read_csv(O/'unit_measurement_all216.csv');v=pd.read_csv(O/'volume_input_all216.csv');rr=pd.read_csv(O/'review_level_means.csv');out=pd.read_csv(O/'volume_quantity_ratios.csv')
assert len(g)==len(v)==216 and g.unit_gate_pass.sum()==205 and v.volume_window_pass.all();assert sum(g.unit_gate_pass&g.original172_pass)==166
lock=json.loads((O/'UNIT_GATE_LOCK.json').read_text());assert hashlib.sha256((O/'unit_gate_all216.csv').read_bytes()).hexdigest()==lock['files'][str(O/'unit_gate_all216.csv')]
# Read every original monthly cell with independent low-level readers, not pandas/read_excel used in extract_gate.
maxdiff=0.;books={}
for f,gg in m.groupby('source_file'):
 p=Path(f)
 if p.suffix=='.xls':
  b=xlrd.open_workbook(p);s=b.sheet_by_name('Instrument Trading Details');get=lambda r,c:s.cell_value(r,c)
 else:
  b=openpyxl.load_workbook(p,read_only=True,data_only=True);s=b['Instrument Trading Details'];get=lambda r,c:s.cell(row=r+1,column=c+1).value
 for z in gg.itertuples():
  observed=float(get(int(z.source_excel_row)-1,int(z.nasdaq_month_volume_excel_column)-1));maxdiff=max(maxdiff,abs(observed-z.nasdaq_month_volume));assert observed==z.nasdaq_month_volume
 books[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
# Joint ratio confidence sets recomputed directly from covariance of 14 review means.
errs=[]
for z in out.itertuples():
 r=rr[(rr['sample']==z.sample)&rr.definition.eq(z.definition)&rr.type.eq(z.type)].dropna(subset=[z.outcome,'quantity_abs_pp']);N=r[z.outcome].to_numpy();D=r.quantity_abs_pp.to_numpy();G=len(N);cov=np.cov(np.array([N,D]),ddof=1)/G;k=t.ppf(.975,G-1)**2;A=D.mean()**2-k*cov[1,1];B=-2*(N.mean()*D.mean()-k*cov[0,1]);C0=N.mean()**2-k*cov[0,0];roots=np.sort(np.roots([A,B,C0]));assert A>0 and np.isreal(roots).all();err=max(abs(N.mean()/D.mean()-z.ratio),abs(roots[0]-z.lo),abs(roots[1]-z.hi));errs.append(err);assert err<1e-10
# Previous172 exactly reproduced for both old definitions, all three frozen outcomes.
old=pd.read_csv(C/'work/volume_measurement_20261102/volume_quantity_ratios.csv');new=out[out['sample'].eq('original172_legacy')];j=old.merge(new,on=['definition','type','outcome'],suffixes=('_old','_new'),validate='1:1');oldmax=max(np.abs(j[c+'_old']-j[c+'_new']).max() for c in ['ratio','lo','hi','den_mean','num_mean','N','G']);assert oldmax<1e-10
passed=v[v.unit_gate_pass];assert np.allclose(passed.corrected_excess_pp,(passed.volume_FI_after_units-passed.baseline_volume_FI_after_units)*100*passed.FI_price/passed.company_mcap_after);assert (passed.corrected_volume_factor_to_FI_after>0).all()
res=dict(original_monthly_cells_verified=len(m),monthly_cell_max_error=maxdiff,review_ratio_cells_verified=len(out),joint_Fieller_max_error=max(errs),original172_cells_reproduced=len(j),original172_max_error=float(oldmax),gate_hash_unchanged=True,N_unit_pass=205,common_original=166,newly_passed=39,previously_passed_now_unresolved=6,no_CAR_analysis=True,source_workbook_hashes=books)
(O/'INDEPENDENT_NUMERIC_VALIDATION.json').write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='source_workbook_hashes'},indent=2))
