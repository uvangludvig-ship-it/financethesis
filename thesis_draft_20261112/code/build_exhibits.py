"""Build manuscript exhibits from frozen aggregate results and audit outputs."""
from pathlib import Path
import sys,json,re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; SRC=Path(sys.argv[1]).resolve(); R=SRC/'results'; A=ROOT/'audit/results'
OUT=ROOT/'manuscript/generated';OUT.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'manuscript/figures';FIG.mkdir(exist_ok=True)
claims=[]
def n(v,d=2):
    if pd.isna(v):return '--'
    if not np.isfinite(v):return r'$\infty$' if v>0 else r'$-\infty$'
    return f'{v:.{d}f}'
def p(v):return '$<0.001$' if v<.001 else n(v,3)
def esc(s):return re.sub(r'(?<=\d)-(?=\d)','--',str(s).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('–','--').replace('−','-'))
def ci(r):return f"[{n(r.lo)}, {n(r.hi)}]"
def table(name,title,headers,rows,note,align=None):
    align=align or ('l'+'r'*(len(headers)-1))
    s='\\begin{table}[!htbp]\n\\centering\n\\caption{'+title+'}\\label{tab:'+name+'}\n\\small\n\\setlength{\\tabcolsep}{5pt}\n\\begin{tabular}{'+align+'}\n\\toprule\n'
    s+=' & '.join(headers)+r' \\'+'\n\\midrule\n'
    s+='\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)
    s+='\n\\bottomrule\n\\end{tabular}\n\\begin{minipage}{\\linewidth}\\footnotesize\\vspace{5pt}\n'+note+'\n\\end{minipage}\n\\end{table}\n'
    (OUT/(name+'.tex')).write_text(s)

t=pd.read_csv(R/'effect/tabell1_lang.csv'); flow=pd.read_csv(A/'sample_flow.csv');rows=[]
for stage in flow.stage.unique():
    q=flow[flow.stage==stage].set_index('type');rows.append([{'source list':'Documented membership changes','imported return candidates':'Imported return candidates','after exclusions':'After deletion exclusions','complete main CAR':'Complete main return window'}[stage],int(q.loc['addition','n']),int(q.loc['deletion','n'])])
table('sample','Construction of the return sample',['Stage','Additions','Deletions'],rows,
 r'The source list contains 536 membership changes in 39 review cycles from 2007 through the first review of 2026. The imported return panel contains 487 candidates. Ten deletions flagged for offers or delisting are excluded; six remaining candidates lack a complete main window. The final sample contains 471 event observations. Each event type spans 38 review cycles; their union spans 39. Source: frozen event files and independent reconstruction, audit/results/sample\_flow.csv.')
rows=[]
for ty in ['addition','deletion']:
 for period in ['2007–2011','2012–2016','2017–2021','2022–2026']:
    q=t[(t.panel=='A/B')&(t.typ==ty)&(t.urval==period)].set_index('fönster');r=q.loc['tot']
    rows.append([ty.title(),esc(period),int(r.n),int(r.G),n(q.loc['ann','b']),n(q.loc['eff','b']),n(r.b),ci(r),p(r.p_wcb)])
table('returns','Market adjusted returns around index changes',['Type','Period','$N$','$G$','AD','ED','Total',r'95\% interval','$p$'],rows,
 r'Returns are percentages. AD denotes CAR $[AD-1,AD+1]$, ED denotes CAR $[ED-1,ED+1]$, and Total denotes CAR $[AD-1,ED+1]$, where AD is the recorded announcement trading date and ED the effective trading date. The benchmark is OMXSBGI. Means weight events equally. $N$ and $G$ are event and review counts for Total; AD and ED use their own complete cases. Intervals and two-sided $p$-values for Total use the inherited restricted wild cluster bootstrap with 9,999 draws, Webb weights below 12 clusters and Rademacher weights otherwise. These are pointwise, exploratory intervals. No stars are used. Source: effect/tabell1\_lang.csv, panel A/B.','llrrrrrlr')
rows=[]
labels={'2022–26 minus 2007–11':'Latest minus earliest','2022–26 minus 2017–21':'Latest minus preceding','2017–26 minus 2007–16 (decennier)':'Later minus earlier decade','trend per år (ingen periodindelning)':'Linear trend per year'}
for ty in ['addition','deletion']:
 for k,l in labels.items():
  z=t[(t.panel=='D')&(t.typ==ty)&(t.urval==k)].iloc[0];rows.append([ty.title(),l,n(z.b),ci(z),p(z.p_wcb)])
table('contrasts','Changes in the event window return',['Type','Contrast','Estimate',r'95\% interval','$p$'],rows,
 r'The outcome is CAR $[AD-1,ED+1]$. Differences are percentage points; the linear trend is percentage points per calendar year. Earliest, preceding, and latest periods are 2007--2011, 2017--2021, and 2022--2026. Decades are 2007--2016 and 2017--2026. Restricted wild bootstrap inference clusters by review cycle, using 9,999 draws. A difference of significance levels across periods is not a test of a difference. Source: effect/tabell1\_lang.csv, panel D.','lllrr')
f=pd.read_csv(R/'fund_demand/omrakning_resultat.csv');fi=pd.read_csv(A/'fieller_ratios.csv');rows=[]
for ty in ['addition','deletion']:
 for per in ['2007–11','2012–16','2017–21','2022–26','2017–26']:
  z=f[(f.tabell==5)&(f.typ==ty)&(f.skikt=='D_C')&(f.fonster=='y_tot')&(f.period==per)].iloc[0]
  ff=fi[(fi.type==ty)&(fi.tier=='D_C')&(fi.period==({'2017–26':'2017-2026'}.get(per,per)))].iloc[0]
  fs='All real values' if ff.set_type=='all_real' else '['+n(ff.lower)+', '+n(ff.upper)+']'
  rows.append([ty.title(),esc(per),int(z.n),int(z.G),n(z.car),n(z.D),n(z.M),fs])
table('demand','Returns scaled by observed benchmark linked fund purchases',['Type','Period','$N$','$G$',r'$\bar Y$',r'$\bar D_C$',r'$\widehat M$','Fieller set'],rows,
 r'$Y=s_i CAR_i[AD-1,ED+1]$ and $D_C$ is the sign-adjusted change in covered benchmark-linked funds\textquotesingle{} holdings as a percentage of shares outstanding; $s_i=1$ for additions and $-1$ for deletions. Positive values therefore indicate movement in the index-directed direction for both event types. $\widehat M=\bar Y/\bar D_C$ uses the same non-split complete-case sample for both means. Group C includes strict followers, benchmark variants, and benchmark-linked mixed-fund holdings. The last column is a 95\% Fieller confidence set using the joint CR1 covariance of both means and $t_{G-1}$, an asymptotic sensitivity measure rather than exact small-sample inference. It differs from the inherited percentile bootstrap. Source: fund\_demand/omrakning\_resultat.csv, table 5, and audit/results/fieller\_ratios.csv.','llrrrrrl')
c=pd.read_csv(R/'composition/tabell2_tabell4.csv');rows=[]
for ty in ['addition','deletion']:
 for per in ['2007–11','2012–16','2017–21','2022–26']:
  q=c[(c.tabell=='tabell 2')&(c.typ==ty)&(c.rad==per)].set_index('variant');u=q.loc['utan kontroller, samma händelser som med'];v=q.loc['med kontroller']
  rows.append([ty.title(),esc(per),n(u.b),n(v.b),f'[{n(v.lo_cr1)}, {n(v.hi_cr1)}]'])
table('composition','Composition adjustment on a common event sample',['Type','Period','Unadjusted','Adjusted','Adjusted CR1 interval'],rows,
 r'Period intercepts from CAR $[AD-1,ED+1]$ regressions. Both columns use the same complete-case sample: 237 additions or 185 deletions. Adjusted estimates control for centered abnormal turnover, relative size, residual return variance and analyst coverage. The columns are not a causal decomposition. Intervals are analytical CR1 review-clustered intervals using $t_{G-1}$; unstable inverted bootstrap intervals from auxiliary sparse specifications are not used here. Source: composition/tabell2\_tabell4.csv, table 2.','llrrl')
near=pd.read_csv(R/'near_additions/near_additions_results.csv');rows=[]
for ty in ['addition','deletion']:
 for per in ['före','efter']:
  z=near[(near.typ==ty)&(near.period==per)&(near.variant=='CAR [AD-1,ED+1] mot nästan')&(near.urval==('alla' if ty=='addition' else 'utan de 10 (G&S regel)'))].iloc[0]
  rows.append([ty.title(),'2007--2016' if per=='före' else '2017--2026',int(z.handelser),int(z.nastan),n(z.b),ci(z),p(z.p_wcb)])
table('comparators','Returns relative to size screened comparison securities',['Type','Period','Events','Controls','Coefficient',r'95\% interval','$p$'],rows,
 r'The coefficient is on an event indicator in a regression of CAR $[AD-1,ED+1]$ on that indicator, pre-announcement returns, log market capitalization and review fixed effects. Comparison observations are security-review observations, not unique firms. The inherited size screens do not reconstruct the Nasdaq inclusion threshold and are not a regression discontinuity design. The pre-return control includes AD-1, which also enters the outcome; this overlap is an additional reason to treat the coefficients as descriptive adjustments. Intervals and $p$-values use 9,999 restricted wild cluster draws by review. Source: near\_additions/near\_additions\_results.csv.','llrrrlr')
rows=[]
news=pd.read_csv(R/'news_screen/news_screen_results.csv');ext=pd.read_csv(R/'extreme_values/extreme_values_results.csv');msci=pd.read_csv(R/'msci_overlap/resultat_car.csv')
for per in ['2017–26','2022–26']:
 base=t[(t.panel=='C')&(t.typ=='addition')&(t.urval==per)] if per=='2017–26' else t[(t.panel=='A/B')&(t.typ=='addition')&(t.urval=='2022–2026')&(t['fönster']=='tot')]
 variants=[('Baseline',base.iloc[0]),('Without MSCI overlap',msci[(msci.typ=='addition')&(msci.urval==per)&(msci.variant=='utan överlapp')].iloc[0]),('Without screened company news',news[(news.typ=='addition')&(news.test==per)&(news.variant=='Utan egen bolagsnyhet')].iloc[0])]
 variants +=[(lab,ext[(ext.matt=='CAR')&(ext.typ=='addition')&(ext.test==per)&(ext.variant==v)].iloc[0]) for lab,v in [('Winsorized 1st and 99th percentiles','winsoriserad 1/99'),('Without Sivers','utan Sivers')]]
 for label,z in variants:rows.append([esc(per),label,int(z.n),n(z.b),ci(z)])
table('robustness','Sensitivity of addition returns',['Period','Specification','$N$','CAR',r'95\% interval'],rows,
 r'Event-weighted CAR $[AD-1,ED+1]$ in percent, with pointwise restricted wild cluster bootstrap intervals by review. Each exclusion is applied separately. The company-news screen examines the 24 most extreme inherited events, rather than the full event universe, and is outcome-informed. MSCI exclusion changes the target population. Winsorization changes the outcome. These are sensitivity descriptions, not independent replications or specification selection rules. Sources: effect, msci\_overlap, news\_screen and extreme\_values aggregate CSV files.','llrrl')
h=pd.read_csv(A/'paired_horizon.csv');rows=[]
for ty in ['addition','deletion']:
 for per in ['2017-2026','2022–2026']:
  z=h[(h.type==ty)&(h.period==per)].set_index('window');v=z.loc['cumulative20']
  rows.append([ty.title(),esc(per),int(v.n),n(z.loc['pre_ed','b']),n(z.loc['post20','b']),n(v.b),ci(v),p(v.p_wcr_49999)])
table('horizon','A fixed cohort decomposition through twenty days after implementation',['Type','Period','$N$','Before ED','After ED','Cumulative','CR1 interval','$p_{WCR}$'],rows,
 r'New exploratory audit. Before ED is CAR $[AD-1,ED-1]$; After ED is CAR $[ED,ED+20]$; Cumulative is their event-level sum, CAR $[AD-1,ED+20]$. Every entry in a row uses exactly the same complete-case events. All values are percentages. The interval is analytical CR1 with $t_{G-1}$; $p_{WCR}$ is a separately computed restricted wild cluster bootstrap $p$-value using 49,999 draws and the finite-simulation correction $(k+1)/(B+1)$. These are distinct inferential summaries. No claim of permanent or causal price impact follows from a nonzero finite-horizon cumulative return. Source: audit/results/paired\_horizon.csv.','llrrrrlr')
dep=pd.read_csv(A/'dependence_sensitivity.csv');rows=[]
for ty in ['addition','deletion']:
 for per in ['2017-2026','2022–2026']:
  z=dep[(dep.type==ty)&(dep.period==per)].iloc[0]
  rows.append([ty.title(),esc(per),n(z.b),n(z.equal_review),f'[{n(z.loo_min)}, {n(z.loo_max)}]',n(z.se),n(z.jackknife_se),n(z.se_two_way)])
table('dependence','Weighting and dependence sensitivity',['Type','Period','Event','Review','Leave one out','CR1','CV3','Two way'],rows,
 r'CAR $[AD-1,ED+1]$ in percent. Review mean gives each review equal weight. Leave one out is the range of event-weighted estimates after removing one review at a time, not a confidence interval. CR1, CV3 and Two way report standard errors. CV3 is the cluster jackknife centered on the full-sample estimate. Two way combines review and security clustering with subtraction of the review-security intersection. It does not solve dependence between different securities across different reviews. Source: audit/results/dependence\_sensitivity.csv.','llrrlrrr')
mu=pd.read_csv(A/'multiplicity.csv');rows=[]
for z in mu.itertuples():rows.append([z.typ.title(),esc(z.urval),p(z.p_wcb),p(z.p_holm_10)])
table('multiplicity','Multiplicity in a declared ten test audit family',['Type','Test','Raw $p$','Holm $p$'],rows,
 r'The audit family contains eight five-year total-window means and two latest-minus-earliest contrasts. It was declared after the inherited results were known. Holm adjustment controls familywise error for this family under valid marginal tests; it cannot correct unrecorded historical specification search. It does not turn the thesis into a preregistered study. Source: audit/results/multiplicity.csv.','llrr')
hs=pd.read_csv(A/'horizon_sensitivity.csv');rows=[]
for z in hs[hs.type=='addition'].itertuples():rows.append([esc(z.period),esc(z.variant),z.n,n(z.b),f'[{n(z.lo)}, {n(z.hi)}]',p(z.p_wcr_49999)])
table('horizon_checks','Exclusions in the exploratory cumulative return extension',['Period','Sample','$N$','CAR','CR1 interval','$p_{WCR}$'],rows,
 r'CAR $[AD-1,ED+20]$ in percent, constructed on complete non-overlapping before/after cohorts. Each exclusion is separate. These follow-up diagnostics were added after inspecting the new cumulative estimates, and inherit the limitations of the original screens. Analytical intervals and 49,999-draw wild-bootstrap $p$-values have the same definitions as Table \ref{tab:horizon}. Source: audit/results/horizon\_sensitivity.csv.','llrrlr')

plt.rcParams.update({'font.family':'serif','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelsize':10,'figure.dpi':150,'savefig.bbox':'tight'})
navy='#153b57';red='#993e3d'
annual=pd.read_csv(R/'effect/effect_by_year.csv',header=[0,1],index_col=0)
fig,ax=plt.subplots(figsize=(6.5,3.6))
for ty,color in [('Additions',navy),('Deletions',red)]:ax.plot(annual.index,annual[(ty,'Total')],marker='o',ms=3,lw=1.25,color=color,label=ty)
ax.axhline(0,color='0.5',lw=.6);ax.set(xlabel='Effective year',ylabel='Mean market adjusted CAR (%)',xticks=[2007,2010,2015,2020,2025]);ax.legend(frameon=False,ncol=2);fig.tight_layout();fig.savefig(FIG/'annual_returns.pdf');plt.close(fig)
dd=pd.read_csv(R/'fund_demand/figur1_skikt.csv');fig,ax=plt.subplots(figsize=(6.5,3.6))
for ty,color in [('addition',navy),('deletion',red)]:ax.plot(dd.ar,dd['D_C_'+ty],marker='o',ms=3,lw=1.25,color=color,label=ty.title())
ax.set(xlabel='Announcement year',ylabel='Sign adjusted net holdings change (%)',xticks=[2007,2010,2015,2020,2025]);ax.axhline(0,color='0.5',lw=.6);ax.legend(frameon=False);fig.tight_layout();fig.savefig(FIG/'fund_demand.pdf');plt.close(fig)
v=pd.read_csv(R/'liquidity/volume_share_by_day.csv',index_col=0);fig,axs=plt.subplots(1,2,figsize=(6.5,3.1),sharey=True)
for ax,ty in zip(axs,['addition','deletion']):
 for per,color in [('2007–2011','0.55'),('2022–2026',navy)]:ax.plot(v.index,v[f'tabell 1|{ty}|{per}'],color=color,lw=1.5,label=per)
 ax.axvline(-1,color=red,lw=.7,ls=':');ax.set(title=ty.title()+'s',xlabel='Trading days from ED',xlim=(-12,12))
axs[0].set_ylabel('Share of 45 day volume (%)');axs[1].legend(frameon=False);fig.tight_layout();fig.savefig(FIG/'volume_concentration.pdf');plt.close(fig)
s=pd.read_csv(R/'liquidity/spread_by_year.csv');fig,ax=plt.subplots(figsize=(6.5,3.1));ax.plot(s.year,s.vw_spread_omxsb_members,color=navy,marker='o',ms=3)
ax.set(xlabel='Calendar year',ylabel='Value weighted quoted closing spread (%)',xticks=[2007,2010,2015,2020,2025]);fig.tight_layout();fig.savefig(FIG/'quoted_spread.pdf');plt.close(fig)

# Explicit source paths and selectors accompany the self-contained captions.
mapping={
 'sample':('audit/results/sample_flow.csv','stages by event type'),
 'returns':('replication/thesis_final/results/effect/tabell1_lang.csv','panel A/B; ann, eff, tot; four periods and both types'),
 'contrasts':('replication/thesis_final/results/effect/tabell1_lang.csv','panel D; endpoint, last-two, decades and annual-trend contrasts'),
 'composition':('replication/thesis_final/results/composition/tabell2_tabell4.csv','tabell 2; common-sample variants; lo_cr1 and hi_cr1'),
 'comparators':('replication/thesis_final/results/near_additions/near_additions_results.csv','CAR [AD-1,ED+1] mot nastan; original main samples; fore/efter'),
 'demand':('replication/thesis_final/results/fund_demand/omrakning_resultat.csv; audit/results/fieller_ratios.csv','tabell 5; D_C; y_tot; non-split common cases; joint Fieller sets'),
 'robustness':('replication/thesis_final/results/effect/tabell1_lang.csv; replication/thesis_final/results/msci_overlap/resultat_car.csv; replication/thesis_final/results/news_screen/news_screen_results.csv; replication/thesis_final/results/extreme_values/extreme_values_results.csv','addition; later decade and latest block; each exclusion separately'),
 'horizon':('audit/results/paired_horizon.csv','2017-2026 and 2022-2026; pre_ed, post20, cumulative20'),
 'dependence':('audit/results/dependence_sensitivity.csv','later decade and latest block; event/review means, LOO range and three SEs'),
 'multiplicity':('audit/results/multiplicity.csv','all ten declared family rows'),
 'horizon_checks':('audit/results/horizon_sensitivity.csv','all addition exclusions; full deletion results remain in CSV'),
 'annual_returns':('replication/thesis_final/results/effect/effect_by_year.csv','two-header CSV; Total columns by type'),
 'fund_demand':('replication/thesis_final/results/fund_demand/figur1_skikt.csv','ar and D_C_addition/D_C_deletion'),
 'volume_concentration':('replication/thesis_final/results/liquidity/volume_share_by_day.csv','tabell 1; early and latest; plotted ED +/-12 with ED +/-22 denominator'),
 'quoted_spread':('replication/thesis_final/results/liquidity/spread_by_year.csv','year and vw_spread_omxsb_members')}
for key,(source,selector) in mapping.items():
 path=OUT/(key+'.tex') if (OUT/(key+'.tex')).exists() else FIG/(key+'.pdf')
 claims.append({'exhibit':key,'generated_file':str(path.relative_to(ROOT)),'source_files':source,'selector':selector,'source_commit':'d2d41666ed213e4cc1f6cb382313f59c29e87ea0'})
pd.DataFrame(claims).to_csv(ROOT/'audit/exhibit_map.csv',index=False)
print('Generated 11 tables and 4 figures')
