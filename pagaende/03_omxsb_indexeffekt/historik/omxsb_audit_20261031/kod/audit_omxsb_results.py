"""Produce review-clustered result ledger and before/after audit, no specification search."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from omxsb_audit_helpers import yearly_median_inference
from omxsb_demand_labels import demand_labels

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'output/omxsb_audit_20261031'
C=A/'corrected'; B=A/'baseline'; O=A/'original/exports'
PER=['2007–2011','2012–2016','2017–2021','2022–2026']
nb=json.loads((ROOT/'code/notebooks/replication_omxsb_2007.ipynb').read_text())
src=next(''.join(c['source']) for c in nb['cells'] if 'def wcb(' in ''.join(c['source']))
ns={'np':np,'pd':pd,'stats':stats,'PER':PER};exec(src.split('rows = []')[0],ns)
cell,diffcell,ols,wcb=[ns[k] for k in ['cell','diffcell','ols','wcb']]

def compare(left,right,name):
    rows=[];details=[]
    for f in sorted(right.rglob('*.csv')):
        old=left/f.relative_to(right)
        if not old.exists(): continue
        a,b=pd.read_csv(old),pd.read_csv(f)
        # Unordered sets in the original membership code only permute rows.
        keys=next((k for k in [['event_id'],['review_cycle','key'],['review_cycle','problem','key']] if set(k)<=set(a) and not a.duplicated(k).any()),None)
        if keys:
            a=a.sort_values(keys).reset_index(drop=True);b=b.sort_values(keys).reset_index(drop=True)
        elif f.name=='membership_inconsistencies.csv':
            a=a.sort_values(list(a)).reset_index(drop=True);b=b.sort_values(list(b)).reset_index(drop=True)
        if a.shape!=b.shape or list(a)!=list(b):
            rows.append(dict(file=str(f.relative_to(right)),status='schema_changed',max_numeric_diff=np.nan));continue
        nums=a.select_dtypes('number').columns.intersection(b.select_dtypes('number').columns)
        changed=[];maxdiff=0.
        for col in nums:
            bad=~np.isclose(a[col],b[col],equal_nan=True,atol=1e-9,rtol=1e-9)
            if bad.any():
                changed.append(col)
                dd=(a[col]-b[col]).abs().max();maxdiff=max(maxdiff,dd if np.isfinite(dd) else 0)
                for j in np.flatnonzero(bad):
                    details.append(dict(file=str(f.relative_to(right)),row=int(j),variable=col,before=a.loc[j,col],after=b.loc[j,col]))
        textcols=[c for c in a if c not in nums]
        textmatch=a[textcols].fillna('').equals(b[textcols].fillna(''))
        rows.append(dict(file=str(f.relative_to(right)),status='match' if not changed and textmatch else 'difference',
                         changed_numeric_columns=';'.join(changed),text_match=textmatch,max_numeric_diff=maxdiff))
    pd.DataFrame(rows).to_csv(A/f'{name}.csv',index=False)
    pd.DataFrame(details).to_csv(A/f'{name}_details.csv',index=False)
    return pd.DataFrame(rows)

cmp=compare(O,B,'baseline_comparison')
compare(B,C,'correction_comparison')
e=pd.read_csv(C/'events_car.csv',parse_dates=['AD','ED'])
e['adx']=e.AD.astype(str)
m=pd.read_csv(C/'mechanisms/results_table_long.csv')
rows=[]
def put(question,typ,period,window,unit,r,source,can,cannot,method='CR1 t(G−1), 95%',stage='corrected rerun'):
    r=dict(r);est=r.get('coef',r.get('mean',np.nan));g=r.get('G',np.nan)
    lo,hi=r.get('ci_low',np.nan),r.get('ci_high',np.nan)
    if not np.isfinite(lo) and np.isfinite(r.get('se_cr1',np.nan)) and g>1:
        d=stats.t.ppf(.975,g-1)*r['se_cr1'];lo,hi=est-d,est+d
    rows.append(dict(question=question,type=typ,period=period,window=window,estimate=est,unit=unit,
                     ci_low=lo,ci_high=hi,ci_method=r.get('ci_method') if pd.notna(r.get('ci_method')) else method,N=r.get('N',np.nan),
                     independent_reviews=g,se_cr1=r.get('se_cr1',np.nan),p_wcb=r.get('p_wcb',np.nan),
                     source=source,execution=stage,supports=can,does_not_support=cannot))

t=pd.read_csv(C/'tables/tab_02_car_long.csv')
for r in t[t.period.isin(PER)].to_dict('records'):
    put('Indexeffekt',r['type'],r['period'],{'ann':'AD−1:AD+1','eff':'ED−1:ED+1','tot':'AD−1:ED+1'}[r['window']],
        '% marknadsjusterad avkastning, beta=1',r,'corrected/tables/tab_02_car_long.csv',
        'Genomsnittlig prisreaktion i fast fönster relativt OMXSBGI','Ingen identifierad kausal mekanism; utebliven signifikans bevisar inte noll')
for r in m[(m['sample']=='all')].to_dict('records'):
    test=r['test'];typ='addition' if 'additions' in test else 'deletion' if 'deletions' in test else 'all'
    if 'pre-announcement' in test:
        window='AD−100:AD−1' if '100' in test else 'AD−20:AD−1'
        put('Förbeskedsavkastning',typ,r['statistic'],window,'%',r,'corrected/mechanisms/results_table_long.csv',
            'Kursutveckling före besked','Inte evidens ensam för förhandspositionering; urval på omsättning/storlek och momentum')
    elif 'post-event CAR' in test:
        put('Efterföljande avkastning',typ,r['statistic'],'ED+2:ED+100','%',r,'corrected/mechanisms/results_table_long.csv',
            'Genomsnittlig senare relativ avkastning','Inte säker återgång eller kausal reversering')
    elif r['explanation']=='E1 composition' and 'demeaned' in test and r['statistic'] in PER:
        put('Kompositionsjusterad indexeffekt',typ,r['statistic'],'AD−1:ED+1; kontroller före AD','%',r,'corrected/mechanisms/e1_table3_long.csv',
            'Predikterad effekt vid gemensamma genomsnittliga kontroller inom typ','Ofullständigt medlemsuniversum; inte full JF-modell; komposition är inte kausalt identifierad')
    elif 'Fig. 11:' in test:
        put('Volymkoncentration',typ,r['statistic'],'ED−1 / ED±22' if 'ED−1' in test else 'ED / ED±22','% av 45-dagarsvolym',r,
            'corrected/mechanisms/results_table_long.csv','När handeln koncentreras','Varken orderriktning, motpart eller exekveringskostnad')
    elif test.startswith('Table 4:'):
        group='trackers' if 'OMXSB trackers' in test else 'all FI' if 'all FI' in test else 'non-trackers'
        put('Nettoinnehavsförändring, '+group,typ,'2019–2026','kvartalsslut före AD till första kvartalsslut efter ED',
            '% av LSEG-aktier vid efterkvartalet; medel av årsmedianer',r,'corrected/mechanisms/results_table_long.csv',
            'Förändring för fonder rapporterande vid båda ändpunkterna','Medianerna är inte additiva; mandat, split/ISIN och nämnare inte fullständigt verifierade')
    elif r['explanation'].startswith('E2'):
        put('Spread och indexeffekt',typ,'2007–2026','årsmedelspread mot AD−1:ED+1','pp CAR per procentenhet spread',r,
            'corrected/mechanisms/results_table_long.csv','Beskrivande samvariation','Ingen kausal likviditetseffekt; slutnoterad spread är inte effektiv spread')
    elif r['explanation'].startswith('Demand ('):
        labels=demand_labels(test)
        put(labels['question'],typ,labels['period'],labels['window'],labels['unit'],r,
            'corrected/mechanisms/results_table_long.csv',labels['supports'],labels['does_not_support'])

# Actual contrasts, not comparisons of separate significance levels.
contrast=[]
for typ in ['addition','deletion']:
    s=e[(e.type==typ)&e.period.isin([PER[0],PER[-1]])]
    r=diffcell(s.tot,s.adx,s.period.eq(PER[-1]))
    put('Förändring av indexeffekt, sista minus första period',typ,'2022–2026 minus 2007–2011','AD−1:ED+1','procentenheter',r,
        'contrast_tests.csv','Direkt skattad skillnad över tid','Ingen förklaring till skillnaden')
    contrast.append(dict(test='last_minus_first',type=typ,**r))
s=e[e.period==PER[-1]]
r=diffcell(s.tot,s.adx,s.type.eq('addition'))
contrast.append(dict(test='addition_minus_deletion_latest',type='both',**r))
put('Inval minus utträden', 'both',PER[-1],'AD−1:ED+1','procentenheter',r,'contrast_tests.csv',
    'Direkt prövad skillnad på gemensamma översynsdatum','Olika tecken är inte samma sak som olika absoluta effekter')
pd.DataFrame(contrast).to_csv(A/'contrast_tests.csv',index=False)

# Paired-reporting accounting on exactly the same event sample, both means and medians.
nt=pd.read_csv(C/'nettrading_omxsb.csv').dropna(subset=['nt','instbuy','activebuy'])
nt['adx']=nt.AD
account=[]
for typ,s in nt.groupby('type'):
    assert np.allclose(s.instbuy,s.nt+s.activebuy)
    for v in ['nt','instbuy','activebuy']:
        r=cell(s[v],s.adx);account.append(dict(type=typ,group=v,**r))
        put('Additiv ägarbokföring, '+v,typ,'2019–2026','kvartal före AD till kvartal efter ED',
            '% av LSEG-aktier; poolat händelsemedel',r,'ownership_common_sample.csv',
            'Alla FI = tracker + övriga, per händelse och i medel','Övriga FI är inte alla aktiva ägare och residual utanför FI saknar identitet')
pd.DataFrame(account).to_csv(A/'ownership_common_sample.csv',index=False)

# Isolate the E5b inference correction from the reporting-pair correction.
original_nt=pd.read_csv(B/'nettrading_omxsb.csv').dropna(subset=['nt','instbuy','activebuy'])
original_nt['year']=pd.to_datetime(original_nt.ED).dt.year
original_nt['adx']=original_nt.AD
paired_nt=nt.assign(year=pd.to_datetime(nt.ED).dt.year)
e5changes=[]
for typ in ['addition','deletion']:
    for v in ['nt','instbuy','activebuy']:
        old=original_nt[original_nt.type.eq(typ)]
        new=paired_nt[paired_nt.type.eq(typ)]
        old_median=yearly_median_inference(old,v)
        new_median=yearly_median_inference(new,v)
        invalid_se=cell(old[v],old.adx)['se_cr1']
        e5changes.append(dict(type=typ,group=v,original_yearly_median_mean=old_median['mean'],
            original_pooled_mean_se_misattached=invalid_se,
            corrected_inference_unpaired_ci_low=old_median['ci_low'],corrected_inference_unpaired_ci_high=old_median['ci_high'],
            paired_yearly_median_mean=new_median['mean'],paired_ci_low=new_median['ci_low'],paired_ci_high=new_median['ci_high'],
            N=len(new),G=new.adx.nunique(),
            note='First fix inference holding original estimand/data fixed; then separately restrict to paired nonempty reporters.'))
pd.DataFrame(e5changes).to_csv(A/'e5b_before_after.csv',index=False)

# Compare composition on a shared complete-case sample, with and without controls.
em=pd.read_csv(C/'mechanisms/events_mechanisms.csv')
composition=[]
for typ in ['addition','deletion']:
    s=em[em.type.eq(typ)].dropna(subset=['tot','turn','size','vol'])
    ctrl=s[['turn','size','vol']]-s[['turn','size','vol']].mean()
    d=pd.get_dummies(s.period).reindex(columns=PER).astype(float)
    for variant,X in [('raw_same_sample',d),('controlled_same_sample',pd.concat([ctrl,d],axis=1))]:
        X=X.to_numpy();y=s.tot.to_numpy();g=s.AD.to_numpy()
        b,res,Vh,Vc,G,*_=ols(y,X,g)
        r=np.zeros(X.shape[1]);r[-4]=-1;r[-1]=1
        _,pw,_=wcb(y,X,g,r)
        rr=dict(mean=r@b,se_cr1=np.sqrt(r@Vc@r),N=len(y),G=G,p_wcb=pw)
        composition.append(dict(type=typ,variant=variant,**rr))
        put('Komposition: sista minus första på samma urval, '+variant,typ,'2022–2026 minus 2007–2011','AD−1:ED+1','pp',rr,
            'composition_common_sample.csv','Tidsförändring med urvalet hållet konstant','Inga nya observerade konfunderare eller historiska medlemslänkar')
pd.DataFrame(composition).to_csv(A/'composition_common_sample.csv',index=False)

# Flag reconciliation: calendar days vs trading days and reason-based exclusions.
rs=pd.read_csv(ROOT/'data/input/omxsb/deletion_reasons_2007_2026.csv')
flags=pd.read_csv(C/'mechanisms/step1_deletion_flags.csv')
flags['reason_script_flag']=flags.deletion_reason.fillna('review_only').ne('review_only')
flags['missing_reason']=flags.deletion_reason.isna()
flags['rules_disagree']=flags.reason_script_flag.ne(flags.flagged)
flags.to_csv(A/'deletion_flag_reconciliation.csv',index=False)
src_events=pd.read_csv(ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv')
sample=src_events[['event_id','type','review_cycle','RIC','days_with_price']].copy()
sample['in_main']=sample.event_id.isin(e.event_id)
sample['has_total_window']=sample.event_id.isin(e.loc[e.tot.notna(),'event_id'])
sample['has_holdings_denominator']=sample.event_id.isin(nt.event_id)
sample.to_csv(A/'sample_by_event.csv',index=False)

res=pd.DataFrame(rows)
res.to_csv(A/'result_table.csv',index=False)
view=res[['question','type','period','window','estimate','ci_low','ci_high','N','independent_reviews','source']].copy()
for col in ['estimate','ci_low','ci_high']:view[col]=view[col].map(lambda v:f'{v:.3f}' if pd.notna(v) else 'ej skattat')
(A/'RESULTATTABELL.md').write_text('# OMXSB verifierade resultat\n\nAlla rader är omkörda. Fulla enheter, tolkningar och CI-metoder finns i `result_table.csv`. '
    'CAR betyder summa av daglig aktieavkastning minus OMXSBGI med beta ett. CR1-intervall använder t(G−1); '
    'årsmedianerna har i stället bootstrap av hela översyner inom år, med få översyner per år.\n\n'+view.to_markdown(index=False)+'\n')
summary={'baseline_comparison':cmp.status.value_counts().to_dict(),
         'source_events':len(src_events),'source_reviews':src_events.review_cycle.nunique(),
         'main_events':len(e),'main_reviews':e.AD.nunique(),'complete_total_events':int(e.tot.notna().sum()),
         'complete_total_reviews':e.loc[e.tot.notna(),'AD'].nunique(),
         'holdings_events_complete':len(nt),'holdings_reviews':nt.AD.nunique(),
         'missing_reason_events':flags.loc[flags.missing_reason,'event_id'].tolist(),
         'reason_flag_count':int(flags.reason_script_flag.sum()),'mechanism_flag_count':int(flags.flagged.sum()),
         'flag_disagreement_count':int(flags.rules_disagree.sum()),
         'not_in_main_reviews':sorted(set(src_events.review_cycle)-set(src_events.loc[src_events.event_id.isin(e.event_id),'review_cycle']))}
(A/'result_summary.json').write_text(json.dumps(summary,indent=2))
print(summary)
