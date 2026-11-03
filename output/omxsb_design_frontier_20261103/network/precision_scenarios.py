"""Analytic sampling illustrations; no empirical returns or actual power estimate.
This is not a lower bound: correlation-estimator dependence can help or hurt.
"""
from pathlib import Path
import pandas as pd,numpy as np,json,datetime
from scipy.stats import t,norm,chi2
from scipy.integrate import quad
from scipy.optimize import brentq
O=Path(__file__).resolve().parent;D=pd.read_csv(O/'common_clientele_baseline_gate.csv')
G=D.review.nunique();crit=t.ppf(.975,G-1)
rows=[]
for label,z in [('all118_before_return_coverage',D),('baseline_eligible49',D[D.baseline_pass])]:
 counts=z.groupby('review').size().to_numpy();g=len(counts)
 # Fixed design minimum75days eachwindow;5market lead/concurrent/lag controls.
 # Near-zero correlation: Var(Fisher z)≈1/(T-k-3). Four independent terms in
 # each pre/post-family/other contrast; independent target+mean3controls adds4/3.
 n=75;k=5;v=4/(n-k-3)*4/3
 for icc in [0,.25,1]:
  varmean=v/g**2*np.sum(icc+(1-icc)/counts);se=np.sqrt(varmean);hw=t.ppf(.975,g-1)*se
  critical=t.ppf(.975,g-1)
  # Integrate the noncentral-t representation; installed scipy.nct returnedNaN
  # at extreme noncentrality. This numerical repair changes no design choice.
  def power(delta):
   lam=delta/se;df=g-1
   return quad(lambda v:(norm.sf(critical*np.sqrt(v/df)-lam)+norm.cdf(-critical*np.sqrt(v/df)-lam))*chi2.pdf(v,df),0,np.inf,epsabs=1e-8)[0]
  mde=brentq(lambda d:power(d)-.8,0,2)
  rows.append(dict(sample=label,N=len(z),G=g,T_per_window=n,linear_nuisance_controls=k,assumed_within_review_ICC=icc,assumed_between_review_independence=True,assumed_independent_two_group_correlation_estimators=True,SE_Fisher_z_approx=se,CI95_halfwidth_approx=hw,MDE80_two_sided_approx=mde,power_for_delta_0_10=power(.1),economic_precision_target_halfwidth=.05,precision_target_met_under_this_scenario=hw<=.05,effective_event_N_when_ICC0=g*g/np.sum(1/counts)))
S=pd.DataFrame(rows);S.to_csv(O/'ANALYTIC_PRECISION_SCENARIOS.csv',index=False)
(O/'PRECISION_LIMITS.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_returns_read=False,actual_power_estimated=False,interpretation='Assumption-dependent Fisher-z delta-method illustrations near zero, NOT lower bounds and NOT actual power. Same-stock correlations with two overlapping portfolios can be highly dependent, shrinking or inflating contrast variance. Serial correlation/fat tails/parameter estimation/fixed-weight missingness and repeated stocks can change it. Holdings-weight cosine is not a return-correlation parameter.',meaningful_tolerance='Chosen95%halfwidth0.05correlation units to distinguish a0.10selective correlation shift. Even such precision would not settle smaller network associations or prove nonfundamental causality.',review_dependence='14calendarreviews remain the broad shock units. Eachreview receives equal weight; unequaleventcounts reduce the effective cross-sectional sample belowN even in the independenceillustration.',required_next_gate='Only after rootreview, a separately locked preannouncement-only calibration could use earlier nonoverlapping placebo windows and calendar-block resampling to estimate attainable halfwidth. Preserveactual matchedstocks/peers and rerun fullresidual/correlation procedure. No eventpostdata; reportfailure without changingwindow/sample to chaseprecision. This stage has NOT been opened.'),indent=2))
print(S.to_string(index=False))
