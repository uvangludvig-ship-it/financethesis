from twin_core import *
import pickle, sys
rng=np.random.default_rng(11)
P=pickle.load(open('twin_placebo.pkl','rb'))
excl_extra=set(open('twin_excl_screen.txt').read().split()) if __import__('os').path.exists('twin_excl_screen.txt') else set()
ev=t[(~t.excl_mech)&(~t.event_id.isin(excl_extra))].copy()
W={'primär [AD-1,ED+1]':lambda e:(e.iAD-1,e.iED+1),
   'medprimär återgång [ED,ED+20]':lambda e:(e.iED,e.iED+20),
   'sek [AD-1,AD+1]':lambda e:(e.iAD-1,e.iAD+1),
   'sek [AD+2,ED-2]':lambda e:(e.iAD+2,e.iED-2),
   'sek [ED-1,ED+1]':lambda e:(e.iED-1,e.iED+1),
   'placebo [AD-60,AD-21]':lambda e:(e.iAD-60,e.iAD-21),
   'placebo [AD-20,AD-2]':lambda e:(e.iAD-20,e.iAD-2)}
allev=t.copy(); doy=np.array(cal.dayofyear)
def starts(e,L):
    firm_ev=allev[allev.firm==e.firm][['iAD','iED']].values; ad=e.AD.dayofyear; out=[]
    for s in range(61,len(cal)-L-21):
        if cal[s].year==e.AD.year: continue
        dd=abs(doy[s]-ad); dd=min(dd,365-dd)
        if dd>45: continue
        if any((s+L+20>=ia-60) and (s-60<=ie+20) for ia,ie in firm_ev): continue
        out.append(s)
    return out
rows=[]; null={}
for name,f in W.items():
    obs=[];pools=[]
    for _,e in ev.iterrows():
        a,b=f(e); a,b=int(a),int(b)
        if b<a: obs.append(np.nan); pools.append(np.array([])); continue
        obs.append(e.sign*spread(e.event_key,e.sister_ric,a,b))
        L=b-a+1; st=starts(e,L)
        pools.append(np.array([e.sign*spread(e.event_key,e.sister_ric,s,s+L-1) for s in st]))
    ev[name]=obs
    ok=[i for i,(o,p) in enumerate(zip(obs,pools)) if np.isfinite(o) and len(p[np.isfinite(p)])>=20]
    o=np.array([obs[i] for i in ok]); fr=ev.firm.values[ok]; pl=[pools[i][np.isfinite(pools[i])] for i in ok]
    m_ev=o.mean(); m_f=pd.Series(o,index=fr).groupby(level=0).mean().mean()
    nm_ev=[];nm_f=[]
    for _ in range(5000):
        d=np.array([rng.choice(p) for p in pl]); nm_ev.append(d.mean()); nm_f.append(pd.Series(d,index=fr).groupby(level=0).mean().mean())
    nm_ev=np.array(nm_ev); nm_f=np.array(nm_f)
    p_ev=(np.abs(nm_ev-nm_ev.mean())>=abs(m_ev-nm_ev.mean())).mean(); p_f=(np.abs(nm_f-nm_f.mean())>=abs(m_f-nm_f.mean())).mean()
    rows.append(dict(fönster=name,N=len(o),bolag=len(set(fr)),medel_händelse=round(m_ev,2),p_händelse=round(p_ev,4),medel_bolag=round(m_f,2),p_bolag=round(p_f,4)))
res=pd.DataFrame(rows)
sec=res[res.fönster.str.startswith('sek')].sort_values('p_händelse')
k=len(sec); holm=[min(1,max((k-i)*p for i,p in enumerate(sec.p_händelse.values[:j+1]))) for j in range(k)]
res.loc[sec.index,'p_holm']=np.round(holm,4)
pd.set_option('display.width',220)
print(res.to_string(index=False))
# legs: index class and sister CAR vs market, primary and reversal windows
def legcar(ric,a,b):
    A=TR[ric] if ric in TR else PRICE[ric]
    if a-1<0 or b>=len(cal): return np.nan
    r=100*np.log(A.iloc[b]/A.iloc[a-1]); m=100*np.log((1+mkt.iloc[a:b+1]/100).prod())
    return r-m
for name in ['primär [AD-1,ED+1]','medprimär återgång [ED,ED+20]']:
    f=W[name]
    ev[name+' indexslag']=[e.sign*legcar(e.event_key,*map(int,f(e))) for _,e in ev.iterrows()]
    ev[name+' systerslag']=[e.sign*legcar(e.sister_ric,*map(int,f(e))) for _,e in ev.iterrows()]
    print(name,'| indexslag (signerad, mot marknaden) %.2f | systerslag %.2f'%(ev[name+' indexslag'].mean(),ev[name+' systerslag'].mean()))
# leave one firm out (primary, event mean)
pm='primär [AD-1,ED+1]'
print('utan ett bolag i taget (primär, händelsemedel):',{f:round(ev[ev.firm!=f][pm].mean(),2) for f in sorted(ev.firm.unique())})
print('utan Volvo: %.2f (N %d)'%(ev[ev.firm!='VOLV'][pm].mean(),(ev.firm!='VOLV').sum()))
print('tillägg %.2f (N %d) | borttag %.2f (N %d)'%(ev[ev.type=='addition'][pm].mean(),(ev.type=='addition').sum(),ev[ev.type=='deletion'][pm].mean(),(ev.type=='deletion').sum()))
ev.to_csv('twin_results_events.csv',index=False); res.to_csv('twin_results_summary.csv',index=False)
