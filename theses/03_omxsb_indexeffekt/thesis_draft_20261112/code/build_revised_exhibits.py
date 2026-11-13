"""Build revised replication-paper exhibits from aggregate inputs only.
Run: python code/build_revised_exhibits.py replication/thesis_final
"""
from pathlib import Path
import runpy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
ns=runpy.run_path(str(ROOT/'code/build_exhibits.py'))
table,n,p,esc= (ns[k] for k in ['table','n','p','esc'])
R,A,OUT,FIG=(ns[k] for k in ['R','A','OUT','FIG'])
maps=pd.read_csv(ROOT/'audit/exhibit_map.csv').set_index('exhibit').to_dict('index')

def record(key,source,selector,kind='table'):
    maps[key]=dict(generated_file=f"manuscript/{'generated' if kind=='table' else 'figures'}/{key}.{'tex' if kind=='table' else 'pdf'}",source_files=source,selector=selector,source_commit='d2d41666ed213e4cc1f6cb382313f59c29e87ea0')

rows=[
 ['Return pattern',r'S\&P 500 additions/deletions; announcement, implementation and full windows','OMXSB; same event-window questions, explicitly defined daily-sum CAR'],
 ['Time comparison','Long US history and decade means','Four Swedish calendar blocks and two pooled decades; incomplete 2026'],
 ['Composition','Period indicators and four firm characteristics','Same regression structure; Swedish measurement proxies and common samples'],
 ['Index demand','Tracking-trade classification; quarterly holdings','Dated mandate groups; available pre/post reports; FI comparison'],
 ['Other index activity',r'Migrations within S\&P index families','Coincident MSCI changes; a distinct overlap diagnostic'],
 ['Anticipation','Pre-announcement returns and longer starting window','Pre-return windows and AD-20 to ED+1 ratio; historical eligibility not fully reconstructed'],
 ['Liquidity','Effective spreads and implementation costs','Closing quoted spreads and daily volume concentration'],
 ['Extensions','Anchor comparison provides the baseline','Fixed-duration timing, within-firm share classes and separate holdings reporting']]
table('replication_map','From Greenwood--Sammon to the Swedish implementation',['Component','Anchor study','Swedish analysis'],rows,
 r'The mapping distinguishes conceptual replication from exact numerical reproduction. Detailed source-version references and adaptations appear in Appendix~\ref{app:replication}. Differences in periods, sample selection, holdings dates and return conventions prevent interpreting raw cross-country differences as causal effects.',r'p{2.0cm}p{4.65cm}p{6.1cm}')
record('replication_map','sources/greenwood_sammon_replication_map.md','version-specific source/code mapping')

coverage=pd.read_csv(A/'sample_by_period.csv');rows=[]
for z in coverage.itertuples():rows.append([z.type.title(),esc(z.period),int(z.source_events),int(z.return_events),int(z.holdings_events),int(z.return_reviews)])
table('sample_by_period','Coverage across periods',['Type','Period','Source events','Return sample','Holdings sample','Reviews'],rows,
 r'The source inventory precedes security matching, exclusions and return requirements. Return sample requires complete AD-1 through ED+1 returns after the stated deletion exclusions. Holdings sample additionally requires the broad demand measure and retention under the share-adjustment screen, with a nonmissing matching return. Reviews counts distinct review cycles in the return sample. The figures describe coverage, not random attrition.','llrrrr')
record('sample_by_period','audit/results/sample_by_period.csv','four periods and both types; source/return/holdings counts')

of=pd.read_csv(A/'observed_fund_net_buying_2017_2026.csv');rows=[]
for z in of.itertuples():
 rows.append([esc(z.label),n(z.mean),f'[{n(z.analytical_lo)}, {n(z.analytical_hi)}]'])
table('observed_funds','Reported fund trading around later additions',['Investor group','Mean purchase',r'95\% interval'],rows,
 r'Net purchases as a percentage of shares outstanding on identical 136 additions in 19 reviews, 2017--2026. The first three rows partition included holdings; the final row is their within-event sum. Mixed-fund security holdings are included at their reported amounts, without the benchmark weights used in the separate AUM measure. Intervals use analytical CR1 by review and $t_{G-1}$. These are covered fund positions, not the complete investor population or observed implementation-day orders.',r'p{8.2cm}rl')
record('observed_funds','audit/results/observed_fund_net_buying_2017_2026.csv','common 136 later additions; four disjoint/sum rows; analytical CR1 intervals')

f=pd.read_csv(R/'fund_demand/omrakning_resultat.csv');fi=pd.read_csv(A/'fieller_ratios.csv')
rows=[]
for ty in ['addition','deletion']:
 for period in ['2007–11','2012–16','2017–21','2022–26','2017–26']:
  z=f[(f.tabell==5)&(f.typ==ty)&(f.skikt=='D_C')&(f.fonster=='y_tot')&(f.period==period)].iloc[0]
  q=fi[(fi.type==ty)&(fi.tier=='D_C')&(fi.period==({'2017–26':'2017-2026'}.get(period,period)))].iloc[0]
  c='All real values' if q.set_type=='all_real' else f'[{n(q.lower)}, {n(q.upper)}]'
  rows.append([ty.title(),esc(period),int(z.n),n(z.car),n(z.D),n(z.M),c])
table('demand_main','Observed fund trading and return per unit of measured demand',['Type','Period','Events','Return','Demand','$M$',r'95\% ratio set'],rows,
 r'Return is sign-adjusted CAR from AD-1 through ED+1, in percent. Demand is the sign-adjusted broad benchmark-linked holdings change as a percentage of shares outstanding. For deletions, negative returns and sales have positive signs. Each ratio divides the two means on identical events retained after the share-adjustment screen. Joint ratio uncertainty is described in Appendix~\ref{app:inference}; it can be unbounded when the denominator is weak. These are descriptive ratios, not identified elasticities.','llrrrrl')
record('demand_main','replication/thesis_final/results/fund_demand/omrakning_resultat.csv; audit/results/fieller_ratios.csv','table5, C, y_tot, same-event ratio and joint covariance')

tim=pd.read_csv(A/'fixed_window_decomposition.csv');gap=pd.read_csv(A/'announcement_timing.csv');rows=[]
for ty in ['addition','deletion']:
 for period in ['2007-2011','2012-2016','2017-2021','2022-2026']:
  q=tim[(tim.type==ty)&(tim.period==period)&(tim.statistic=='mean')].set_index('measure')
  g=gap[(gap.type==ty)&(gap.period==period)].iloc[0]
  rows.append([ty.title(),esc(period),int(q.loc['whole','n']),int(g.gap_median),n(q.loc['whole','estimate']),n(q.loc['first_seven','estimate']),n(q.loc['remainder','estimate'])])
table('timing','The full event window and a common initial seven-day window',['Type','Period','Events','Gap','Full','Initial seven','Remainder'],rows,
 r'Returns are percentages. Gap is the median AD-to-ED distance in trading days across distinct reviews represented in the sample. Full includes AD-1 through ED+1; Initial seven includes AD-1 through AD+5; Remainder includes AD+6 through ED+1. Every row uses identical events and the two components sum to Full. The remainder has varying duration. This timing diagnostic is exploratory; uncertainty for period contrasts is reported in Appendix~\ref{app:inference}.','llrrrrr')
record('timing','audit/results/fixed_window_decomposition.csv; audit/results/announcement_timing.csv','four periods, both types, fixed identical cohorts; review-level median gap')
rows=[]
for z in tim[tim.statistic=='contrast'].itertuples():
 rows.append([z.type.title(),{'whole':'Full window','first_seven':'Initial seven days','remainder':'Remaining interval'}[z.measure],n(z.estimate),f'[{n(z.lower95_cr1)}, {n(z.upper95_cr1)}]',p(z.p_wcr)])
table('timing_contrasts','First-to-last changes in the timing decomposition',['Type','Component','Difference',r'95\% CR1 interval','$p$'],rows,
 r'Differences are 2022--2026 minus 2007--2011, in percentage points, from a four-period indicator regression. Intervals are analytical CR1 using review clusters; two-sided tests use 49,999 restricted wild draws. These are pointwise exploratory tests, not adjusted for all prior specification choices. The component contrasts add to the full contrast.','lllrl')
record('timing_contrasts','audit/results/fixed_window_decomposition.csv','statistic contrast; latest-minus-earliest; all three measures and both types')

tw=pd.read_csv(A/'twin_leg_descriptive_summary.csv');rows=[]
for z in tw.itertuples():rows.append([z.type.title(),int(z.n),int(z.firms),n(z.signed_index),n(z.signed_sister),n(z.signed_difference)])
whole=np.average(tw[['signed_index','signed_sister','signed_difference']],axis=0,weights=tw.n)
rows.append(['Combined',int(tw.n.sum()),13,*[n(v) for v in whole]])
table('twins','The indexed and sister share classes on the same events',['Events','Count','Firms','Index class','Sister class','Difference'],rows,
 r'Sign-adjusted log market-excess returns in percent for AD-1 through ED+1. Deletion signs are reversed. Each difference subtracts the sister-class mean from the index-class mean on identical events. The combined sample contains 39 events from 13 distinct firms; firm counts by event type overlap. The combined relative-return placebo $p$-value is 0.407. These selected log-return observations cannot be subtracted from the main arithmetic-CAR sample to identify a causal component.','lrrrrr')
record('twins','audit/results/twin_leg_descriptive_summary.csv; replication/thesis_final/results/twins/twin_results_summary.csv','same-cohort leg means by type; count-weighted combined mean')

h=pd.read_csv(A/'paired_horizon.csv');rows=[]
for ty in ['addition','deletion']:
 for period in ['2017-2026','2022–2026']:
  q=h[(h.type==ty)&(h.period==period)].set_index('window');z=q.loc['cumulative20']
  rows.append([ty.title(),esc(period),int(z.n),n(q.loc['pre_ed','b']),n(q.loc['post20','b']),n(z.b),f'[{n(z.lo)}, {n(z.hi)}]'])
table('horizon_main','Returns before and after implementation on a fixed cohort',['Type','Period','Events','Before','After','Cumulative',r'95\% interval'],rows,
 r'Returns in percent. Before is AD-1 through ED-1; After is ED through ED+20; Cumulative is AD-1 through ED+20. Each row uses the same events throughout. Intervals are analytical CR1 with review clustering for the cumulative mean. Separate wild-bootstrap tests and post-result exclusions are in the appendix. The horizon is finite and the analysis exploratory.','llrrrrl')
record('horizon_main','audit/results/paired_horizon.csv','later decade and latest block; three nonoverlapping cumulative measures; CR1 intervals')

c=pd.read_csv(R/'composition/tabell2_tabell4.csv');rows=[]
for ty in ['addition','deletion']:
 for period in ['2007–11','2012–16','2017–21','2022–26']:
  q=c[(c.tabell=='tabell 4')&(c.typ==ty)&(c.rad==period)].set_index('variant')
  short=q.loc['[AD−20, AD−1]'];long=q.loc['[AD−100, AD−1]']
  rows.append([ty.title(),esc(period),int(short.n),n(short.b),int(long.n),n(long.b)])
table('anticipation','Pre-announcement returns',['Type','Period','$N_{20}$','AD-20 to AD-1','$N_{100}$','AD-100 to AD-1'],rows,
 r'Arithmetic market-adjusted returns in percent. Each window uses its own complete cases and includes AD-1, which also belongs to the primary event window. The columns cannot be added to the main-window mean. Positive prior performance is consistent with anticipation but also with selection on earlier returns; it does not distinguish these channels.','llrrrr')
record('anticipation','replication/thesis_final/results/composition/tabell2_tabell4.csv','table4, two prewindows, all four blocks and both types')
rows=[]
for ty in ['addition','deletion']:
 for period in ['2007–11','2012–16','2017–21','2022–26']:
  q=f[(f.tabell==5)&(f.typ==ty)&(f.skikt=='D_C')&(f.period==period)].set_index('fonster');s=q.loc['y_tot'];l=q.loc['y_lang']
  rows.append([ty.title(),esc(period),int(s.n),n(s.M),int(l.n),n(l.M)])
table('long_demand','The earlier-start demand-ratio window',['Type','Period','Short $N$','Short $M$','Long $N$','Long $M$'],rows,
 r'Short is AD-1 to ED+1; Long is AD-20 to ED+1, the earlier-start counterpart in the anchor study. Each ratio uses identical events in its own numerator and denominator, but the short and long samples can differ. These are descriptive point estimates; the table does not claim well-identified early multipliers. The ED+20 analysis is a separate extension.','llrrrr')
record('long_demand','replication/thesis_final/results/fund_demand/omrakning_resultat.csv','table5, broad C, y_tot and y_lang, all four blocks')

conv=pd.read_csv(A/'return_conventions.csv');rows=[]
for ty in ['addition','deletion']:
 for period in ['2007-2011','2012-2016','2017-2021','2022-2026','2017-2026']:
  q=conv[(conv.type==ty)&(conv.period==period)].set_index('measure');z=q.loc['compounded']
  rows.append([ty.title(),esc(period),int(z.n),n(q.loc['arithmetic','mean']),n(z['mean']),n(q.loc['close_before_AD_to_after_ED','mean'])])
table('return_conventions','Return definitions on matched events',['Type','Period','Events','Daily sum','Compounded','Base at AD-1'],rows,
 r'Daily sum is the primary arithmetic CAR. Compounded is the stock buy-and-hold return minus the benchmark buy-and-hold return using the same included daily returns, AD-1 through ED+1. Base at AD-1 instead starts from the AD-1 close and includes daily returns AD through ED+1. Both latter columns compound stock and benchmark separately. These are sensitivity checks, not proof of the original US code\textquotesingle{}s convention.','llrrrr')
record('return_conventions','audit/results/return_conventions.csv','matched complete cohorts, three definitions, four blocks plus later decade')
cov=pd.read_csv(A/'holdings_coverage_summary.csv');rows=[]
for z in cov.itertuples():rows.append([z.type.title(),esc(z.period),int(z.n),n(z.D_B),n(z.D_V),n(z.D_C),n(z.nf_C,1)])
table('holdings_coverage','Fund definitions on the broad-measure event sample',['Type','Period','Events','Strict','+ variants','Broad','Mixed count'],rows,
 r'Demand is percent of shares outstanding, sign-adjusted for deletions. All three demand definitions in a row use the same retained event sample. Strict comprises exact benchmark followers; the next column adds related benchmark variants; Broad also includes the benchmark-linked mixed-fund category. Mixed count is the mean number of reporting mixed funds per event, not their ownership percentage. These data do not measure the complete investor universe.','llrrrrr')
record('holdings_coverage','audit/results/holdings_coverage_summary.csv','all common broad-complete cells; D_B,D_V,D_C and mean nf_C')

comp=pd.read_csv(A/'comparison_repair_results.csv');rows=[]
for ty,sample in [('addition','all'),('deletion','exclude_flagged')]:
 for period in ['2007-2016','2017-2026']:
  q=comp[(comp.type==ty)&(comp['sample']==sample)&(comp.period==period)&(comp.variant=='all_comparators')].set_index('control_window')
  if q.empty:raise ValueError(f'Unknown comparator sample label: {ty}, {sample}')
  old=q.loc['AD-100 to AD-1'];new=q.loc['AD-100 to AD-2']
  rows.append([ty.title(),esc(period),int(new.events),int(new.comparators),n(old.estimate),n(new.estimate),f'[{n(new.lower95_cr1)}, {n(new.upper95_cr1)}]'])
table('comparators_repaired','Removing overlap from the comparison control',['Type','Period','Events','Controls','Before','After',r'After 95\% interval'],rows,
 r'Coefficients are percentage points on the event indicator in the same review-fixed-effect, log-size and pre-return regression. Before includes AD-1 in the pre-return control; After removes only that day. Outcomes, sample and other regressors are unchanged. Intervals are analytical CR1 clustered by review; separate 49,999-draw wild tests and the main-market restriction are provided in the machine-readable results. Size screens are not reconstructed Nasdaq assignment thresholds.','llrrrrl')
record('comparators_repaired','audit/results/comparison_repair_results.csv','all_comparators; addition all/deletion excluded10; before/after control timing')

t=pd.read_csv(R/'effect/tabell1_lang.csv')
fig,axs=plt.subplots(1,2,figsize=(6.4,3.2),sharey=True)
for ax,ty,color in zip(axs,['addition','deletion'],['#153b57','#993e3d']):
 q=t[(t.panel=='A/B')&(t.typ==ty)&(t['fönster']=='tot')].set_index('urval').loc[['2007–2011','2012–2016','2017–2021','2022–2026']]
 ax.errorbar(np.arange(4),q.b,yerr=np.vstack([q.b-q.lo,q.hi-q.b]),fmt='o',color=color,capsize=4,lw=1.2)
 ax.axhline(0,color='0.45',lw=.7);ax.set(title=ty.title()+'s',xticks=np.arange(4),xticklabels=['2007–11','2012–16','2017–21','2022–26'])
 ax.tick_params(axis='x',labelsize=8)
axs[0].set_ylabel('Market-adjusted CAR (%)');fig.tight_layout();fig.savefig(FIG/'period_returns.pdf');plt.close(fig)
record('period_returns','replication/thesis_final/results/effect/tabell1_lang.csv','panel A/B total; frozen WCR intervals','figure')
paths=pd.read_csv(A/'fixed_cohort_path.csv');fig,axs=plt.subplots(1,2,figsize=(6.4,3.3),sharey=True)
for ax,ty,color in zip(axs,['addition','deletion'],['#153b57','#993e3d']):
 q=paths[(paths.type==ty)&(paths.period=='2017-2026')].sort_values('day_from_ED')
 ax.fill_between(q.day_from_ED.to_numpy(),q.lower.to_numpy(),q.upper.to_numpy(),color=color,alpha=.16)
 ax.plot(q.day_from_ED,q['mean'],color=color,lw=1.6);ax.axhline(0,color='0.45',lw=.7);ax.axvline(0,color='0.45',lw=.7,ls=':')
 ax.set(title=ty.title()+f's (N={int(q.n.iloc[0])})',xlabel='Ending day relative to ED',xticks=[0,5,10,15,20])
 ax.tick_params(axis='x',labelsize=8)
axs[0].set_ylabel('CAR accumulated since AD−1 (%)');fig.tight_layout();fig.savefig(FIG/'fixed_cohort_path.pdf');plt.close(fig)
record('fixed_cohort_path','audit/results/fixed_cohort_path.csv','later-decade both types, fixed complete cohort, pointwise CR1','figure')

# Keep main captions readable; exact input paths remain in the exhibit map.
for file in OUT.glob('*.tex'):
 text=file.read_text().replace(r'\ref{tab:horizon}',r'\ref{tab:horizon_main}').replace('inherited ','').replace('New exploratory audit.','Exploratory extension.').replace('non-split complete-case','adjustment-screened complete-case').replace('same non-split complete-case','same adjustment-screened complete-case')
 if file.stem=='replication_map':text=text.replace(r'\begin{table}[!htbp]',r'\begin{table}[H]')
 import re
 text=re.sub(r' Source[s]?: [^\n]+(?=\n\\end\{minipage\})',' Source: Authors\' calculations; exact inputs are listed in the replication package.',text)
 file.write_text(text)
pd.DataFrame([dict(exhibit=k,**v) for k,v in maps.items()]).to_csv(ROOT/'audit/exhibit_map.csv',index=False)
print('Built revised replication tables and two additional figures.')
