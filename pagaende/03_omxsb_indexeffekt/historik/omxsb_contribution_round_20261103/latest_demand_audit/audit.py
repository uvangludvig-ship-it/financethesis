"""Read-only reconstruction of Runda11 demand; all writes go beside this file.

Diagnostic only: not a corrected economic demand estimate.
"""
from pathlib import Path
import re, json, hashlib, datetime, sys
import numpy as np
import pandas as pd
from scipy.stats import t

O = Path(__file__).resolve().parent
R = Path('/Users/ludviguvang/dev/financethesis')
OLD = Path('/Users/ludviguvang/Documents/Codex/2026-10-30/oke/work/omxsb_execution_demand_20261102')
inputs = []
def read(path, **kwargs):
    inputs.append(path)
    return pd.read_csv(path, **kwargs)

E = read(R/'code/claude_checks/runda11_resultat/handelser.csv')
F = read(R/'code/claude_checks/data/runda8_fondagare.csv.gz', low_memory=False).rename(columns={
    'Fund Name':'fund','Fund Type Description':'fund_type','Fund Shares Held (Adjusted)':'q',
    'Fund Holdings Filing Date':'date','Fund Address Country':'country'})
I = read(R/'code/claude_checks/runda8_input.csv')
I = I[I.kind.eq('event')]
F = F.merge(I[['event_id','AD','ED']], on='event_id', validate='m:1')
for c in ['date','asof','AD','ED']: F[c] = pd.to_datetime(F[c], errors='coerce')
F.q = pd.to_numeric(F.q, errors='coerce')

def classify(row):
    n = row.fund.lower() if isinstance(row.fund, str) else ''
    if re.search(r'nordea sverige passiv|robur access sverige|robur access edge sweden|nordnet sverige index|nordnet indexfond sverige|nordnet superfonden sverige|^lannebo marknad sverige$|^öhman marknad sverige$|nordea inst aktief sverige|ishares omx stockholm', n): return 'OMXSB-index'
    if re.search(r'xact sverige|xact omxsb', n): return 'OMXSB-index' if row.date <= pd.Timestamp('2018-12-31') else 'other_passive'
    if re.search(r'lansforsakringar sverige index|länsförsäkringar sverige index', n): return 'OMXSB-index' if row.date >= pd.Timestamp('2025-06-16') else 'other_passive'
    if n == 'storebrand sverige': return 'OMXSB-index' if row.date >= pd.Timestamp('2025-10-01') else 'active'
    if re.search(r'nordea generationsfond|robur access mix|kpa blandfond|nordea donationsmedel', n): return 'OMXSB-blandfond'
    if re.search(r'lansforsakringar sparmal|länsförsäkringar sparmål', n): return 'OMXSB-blandfond' if row.date >= pd.Timestamp('2025-06-16') else 'active'
    if re.search(r'xact omxs30|avanza zero|aktiespararna topp sverige', n): return 'OMXS30' if not ('zero' in n and row.date > pd.Timestamp('2025-06-30')) else 'other_passive'
    if re.search(r'(smabolag|småbolag|small ?cap|mikrobolag)', n) and re.search(r'index|indeks|xact|etf|plus ', n) and re.search(r'sverige|svenska|sweden', n): return 'smallcap'
    if row.fund_type == 'Exchange-Traded Fund' or re.search(r'index|indeks|passiv|passive|tracker|exponering', n): return 'other_passive'
    return 'active'

F['group'] = [classify(r) for r in F.itertuples()]
F['stale'] = (F['asof'] - F.date).dt.days.gt(120)
F['wrong_side'] = np.where(F.snap.eq('fore'), F.date.ge(F.AD), F.date.lt(F.ED))
RD = {f: pd.DatetimeIndex(g.date.dropna().unique()).sort_values() for f,g in F.groupby('fund')}
def reports(f, a, b):
    d = RD[f]
    return bool(((d >= a) & (d <= b)).any())

byevent = dict(tuple(F.groupby('event_id')))
rows=[];selected_rows=[]
for e in E.itertuples():
    raw=byevent.get(e.event_id,F.iloc[:0]); g=raw[raw.group.eq('OMXSB-index') & ~raw.stale & raw.q.notna()]
    funds=sorted(g.fund.dropna().unique()); AD=pd.Timestamp(e.AD);ED=pd.Timestamp(e.ED)
    eligible=[f for f in funds if reports(f,AD-pd.Timedelta(days=120),AD-pd.Timedelta(days=1)) and reports(f,ED,ED+pd.Timedelta(days=45))]
    sel=g[g.fund.isin(eligible)]
    q0=sel[sel.snap.eq('fore')].groupby('fund').q.sum().reindex(eligible,fill_value=0)
    q1=sel[sel.snap.eq('efter')].groupby('fund').q.sum().reindex(eligible,fill_value=0)
    net=float(q1.sum()-q0.sum())
    reconstructed=e.s*100*net/e.sh_ed if e.sh_ed>0 else np.nan
    inferred=2*len(eligible)-len(sel[['fund','snap']].drop_duplicates())
    primary=bool(e.fonddata and np.isfinite(e.D) and not e.split and np.isfinite(e.y_tot))
    rows.append(dict(event_id=e.event_id,type=e.type,period=e.per,review=e.review,RIC=e.RIC,
        primary_total=primary,controls_primary_total=primary and all(np.isfinite(getattr(e,k)) for k in ['k_oms','k_storlek','k_wz','k_ana']),
        split=e.split,kv=e.kv,eligible_funds=len(eligible),raw_index_funds=raw[raw.group.eq('OMXSB-index')].fund.nunique(),
        no_eligible_index_fund=len(eligible)==0,inferred_zero_endpoints=inferred,selected_wrong_side_rows=int(sel.wrong_side.sum()),
        selected_rows=len(sel),D_saved=e.D,D_reconstructed=reconstructed,D_abs_error=abs(e.D-reconstructed)))
    selected_rows.extend(sel.assign(primary_total=primary)[['event_id','fund','ric','date','snap','q','group','primary_total','wrong_side']].to_dict('records'))
C=pd.DataFrame(rows)
C.to_csv(O/'r11_event_coverage_audit.csv',index=False)
assert np.nanmax(C.D_abs_error)<1e-10
summ=[]
for scope, mask in [('all_r11',np.ones(len(C),dtype=bool)),('primary_total',C.primary_total),('controls_primary_total',C.controls_primary_total)]:
    q=C[mask].groupby(['period','type']).agg(N=('event_id','size'),G=('review','nunique'),
        zero_due_no_eligible_fund=('no_eligible_index_fund','sum'),inferred_zero_endpoints=('inferred_zero_endpoints','sum'),
        selected_wrong_side_rows=('selected_wrong_side_rows','sum'),median_eligible_funds=('eligible_funds','median')).reset_index()
    q['scope']=scope;summ.append(q)
S=pd.concat(summ,ignore_index=True);S.to_csv(O/'r11_coverage_summary.csv',index=False)

# R11 excludes large split-proxy changes; assess exact old FI/LSEG comparisons
# against actual retained event endpoints, not merely same security somewhere.
U=read(OLD/'LSEG_vs_FI_same_fund_date_units.csv')
U['date']=pd.to_datetime(U.rapport)
F['fund_id']=F.fund.map({'Storebrand Sverige':51482,'Swedbank Robur Access Sverige':60824})
MF=F[F.fund_id.notna() & F.q.notna()].merge(U[['fund_id','ric','date','FI_quantity','ratio_adjusted_to_raw','unique_LSEG_quantity']],on=['fund_id','ric','date'])
MF=MF.merge(C[['event_id','primary_total','split']],on='event_id',validate='m:1')
MF['unit_discrepancy']=(MF.ratio_adjusted_to_raw-1).abs().gt(.001)&MF.unique_LSEG_quantity
MF['positive_unique_match']=MF.FI_quantity.gt(0)&MF.unique_LSEG_quantity
unit=MF[['event_id','ric','fund_id','date','snap','group','primary_total','split','ratio_adjusted_to_raw','unit_discrepancy','positive_unique_match']].drop_duplicates()
unit.to_csv(O/'r11_split_screen_unit_diagnostic.csv',index=False)
us=[]
for scope,x in [('all_r11',unit),('primary_total_all_groups',unit[unit.primary_total]),('primary_total_D_group',unit[unit.primary_total&unit.group.eq('OMXSB-index')])]:
    x=x[x.positive_unique_match]
    z=x.drop_duplicates(['fund_id','ric','date'])
    us.append(dict(scope=scope,matched_endpoints=len(z),discrepant_endpoints=int(z.unit_discrepancy.sum()),
        events_with_discrepancy=x.loc[x.unit_discrepancy,'event_id'].nunique()))
pd.DataFrame(us).to_csv(O/'r11_unit_summary.csv',index=False)

# Compact roster only: raw-name classifier and actual first/last report.
roster=F[F.group.eq('OMXSB-index')].groupby('fund').agg(first_report=('date','min'),last_report=('date','max'),event_count=('event_id','nunique'))
roster.to_csv(O/'r11_index_name_roster.csv')
M=F[F.fund.isin(['Storebrand Sverige','Swedbank Robur Access Sverige'])].groupby(['fund','group']).agg(first_report=('date','min'),last_report=('date','max'),rows=('event_id','size'),parent_names=('Investor Parent name','nunique'))
M.to_csv(O/'r11_historical_classification_diagnostic.csv')

# Full Fieller inversion, event-weighted means, review-cluster CR1 covariance.
# This changes inferential treatment only; it cannot validate the demand measure.
def fieller(d,ycol):
    y=d[ycol].to_numpy(float);x=d.D.to_numpy(float); n=len(x);g=d.review.to_numpy();G=d.review.nunique()
    mu=np.array([y.mean(),x.mean()]);err=np.column_stack([y,x])-mu
    score=np.array([err[g==k].sum(axis=0) for k in np.unique(g)])
    V=G/(G-1)*(score.T@score)/(n*n)
    crit=t.ppf(.975,G-1)**2
    A=mu[1]**2-crit*V[1,1];B=-2*(mu[0]*mu[1]-crit*V[0,1]);CC=mu[0]**2-crit*V[0,0]
    disc=B*B-4*A*CC;lo=hi=np.nan
    if abs(A)<1e-15:
        if abs(B)<1e-15: kind='all_real' if CC<=0 else 'empty'
        else:kind='left_halfline' if B>0 else 'right_halfline';lo=hi=-CC/B
    elif disc<0: kind='all_real' if A<0 else 'empty'
    else:
        lo,hi=sorted([(-B-np.sqrt(disc))/(2*A),(-B+np.sqrt(disc))/(2*A)])
        kind='bounded' if A>0 else 'two_unbounded_rays'
    rng=np.random.default_rng(20261103);idx={k:np.where(g==k)[0] for k in np.unique(g)}
    nonpositive=0
    for _ in range(9999):
        ii=np.concatenate([idx[k] for k in rng.choice(list(idx),G)])
        nonpositive+=int(x[ii].mean()<=0)
    return dict(n=n,G=G,car=mu[0],D=mu[1],ratio=mu[0]/mu[1],D_se=np.sqrt(V[1,1]),
        D_lo=mu[1]-np.sqrt(crit*V[1,1]),D_hi=mu[1]+np.sqrt(crit*V[1,1]),
        A=A,B=B,C=CC,cov_y_D=V[0,1],fieller_type=kind,lo=lo,hi=hi,
        bootstrap_nonpositive_denominators=nonpositive,bootstrap_draws=9999)
rr=[]
for (typ,per),d in E[E.fonddata & E.D.notna() & ~E.split].groupby(['type','per']):
    for y in ['y_tot','y_lang']:
        rr.append(dict(type=typ,period=per,window=y,**fieller(d.dropna(subset=[y]),y)))
FF=pd.DataFrame(rr);FF.to_csv(O/'r11_full_fieller_diagnostic.csv',index=False)
saved=read(R/'code/claude_checks/runda11_resultat/runda11_resultat.csv')
tab=saved[(saved.test=='C tabell 5') & (saved.primar=='True')]
if tab.empty: tab=saved[(saved.test=='C tabell 5') & (saved.primar==True)]
cmp=FF.merge(tab[['typ','del_','fonster','M','n','G','car','D']],left_on=['type','period','window'],right_on=['typ','del_','fonster'],suffixes=('_audit','_saved'),validate='1:1')
assert len(cmp)==16
errs={c:float((cmp[c+'_audit']-cmp[c+'_saved']).abs().max()) for c in ['n','G','car','D']}
errs['M']=float((cmp.ratio-cmp.M).abs().max())
assert max(errs.values())<1e-9
meta=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),event_count=len(E),raw_holding_rows=len(F),
    D_max_abs_reconstruction_error=float(C.D_abs_error.max()),table5_reconstruction_errors=errs,
    raw_to_saved_demand_verified=True,fieller_is_measurement_diagnostic_not_corrected_economic_result=True,
    no_FTN=True,no_repo_edits=True,python=sys.version,
    inputs={str(p):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in set(inputs)})
(O/'RUN_METADATA.json').write_text(json.dumps(meta,indent=2))
print(S[S.scope.eq('primary_total')].to_string(index=False))
print(pd.DataFrame(us).to_string(index=False))
print(FF[(FF.type=='addition')&(FF.window=='y_tot')].to_string(index=False))
print(json.dumps(meta['table5_reconstruction_errors']))
