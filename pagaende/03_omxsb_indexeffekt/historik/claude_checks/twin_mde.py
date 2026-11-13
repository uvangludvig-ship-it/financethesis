from twin_core import *
rng=np.random.default_rng(7)
keep=t[~t.excl_mech].copy()
allev=t.copy()
md=pd.Series(cal.strftime('%m-%d'),index=range(len(cal)))
doy=np.array(cal.dayofyear)
def placebo_pool(e,L):
    # windows of length L starting within +-45 calendar days of AD's day-of-year, other years, away from this firm's events
    firm_ev=allev[allev.firm==e.firm][['iAD','iED']].values
    cand=[]
    ad_doy=e.AD.dayofyear
    for s in range(61,len(cal)-L-21):
        if cal[s].year==e.AD.year: continue
        dd=abs(doy[s]-ad_doy); dd=min(dd,365-dd)
        if dd>45: continue
        if any((s+L+20>=ia-60) and (s-60<=ie+20) for ia,ie in firm_ev): continue
        cand.append(s)
    return cand
res={}
for _,e in keep.iterrows():
    L=(e.iED+1)-(e.iAD-1)+1
    pool=placebo_pool(e,L)
    vals=[spread(e.event_key,e.sister_ric,s,s+L-1) for s in pool]
    vals=np.array([v for v in vals if np.isfinite(v)])*e.sign
    res[e.event_id]=vals
keep['n_placebo']=keep.event_id.map(lambda k:len(res[k])); keep['sd_placebo']=keep.event_id.map(lambda k:np.std(res[k]) if len(res[k]) else np.nan)
print(keep[['event_id','firm','type','n_placebo','sd_placebo']].round(2).to_string(index=False))
ok=keep[keep.n_placebo>=20]
B=10000
ev_means=[];firm_means=[]
for _ in range(B):
    draw=np.array([rng.choice(res[k]) for k in ok.event_id])
    ev_means.append(draw.mean())
    firm_means.append(pd.Series(draw,index=ok.firm.values).groupby(level=0).mean().mean())
se_ev=np.std(ev_means); se_f=np.std(firm_means)
print('\nhändelser med placebo:',len(ok),'bolag:',ok.firm.nunique())
print('primärt fönster [AD-1,ED+1]: SE händelsemedel %.2f -> MDE (80%% styrka, 5%%) %.2f procentenheter'%(se_ev,2.8*se_ev))
print('                              SE bolagsmedel %.2f -> MDE %.2f'%(se_f,2.8*se_f))
import pickle; pickle.dump(dict(res=res,keep=keep),open('twin_placebo.pkl','wb'))
