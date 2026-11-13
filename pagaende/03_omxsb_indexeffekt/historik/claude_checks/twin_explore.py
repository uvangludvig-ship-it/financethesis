from twin_core import *
rng=np.random.default_rng(5)
excl=set(open('twin_excl_screen.txt').read().split())
ev=t[(~t.excl_mech)&(~t.event_id.isin(excl))].copy()
allev=t.copy(); doy=np.array(cal.dayofyear)
def starts(e,L):
    firm_ev=allev[allev.firm==e.firm][['iAD','iED']].values; ad=e.AD.dayofyear; out=[]
    for s in range(61,len(cal)-L-21):
        if cal[s].year==e.AD.year: continue
        dd=abs(doy[s]-ad); dd=min(dd,365-dd)
        if dd>45 or any((s+L+20>=ia-60) and (s-60<=ie+20) for ia,ie in firm_ev): continue
        out.append(s)
    return out
obs=[];pools=[]
for _,e in ev.iterrows():
    a,b=int(e.iAD)-1,int(e.iED)+1; L=b-a+1
    obs.append(e.sign*spread(e.event_key,e.sister_ric,a,b))
    p=np.array([e.sign*spread(e.event_key,e.sister_ric,s,s+L-1) for s in starts(e,L)]); pools.append(p[np.isfinite(p)])
ev['obs']=obs; ev['pool']=pools
conv={'HUSQ','SCA','VOLV','NCC','BONAV','RATO','KLOV','INDU','SWEC','CORE'}
def test(sub,lab):
    o=sub.obs.values; pl=list(sub.pool); nm=np.array([np.mean([rng.choice(p) for p in pl]) for _ in range(5000)])
    se=nm.std(); p=(np.abs(nm-nm.mean())>=abs(o.mean()-nm.mean())).mean()
    print(f'{lab:32s} N {len(o):2d} medel {o.mean():+.2f}  p {p:.3f}  95%-gräns ±{1.96*se:.2f}  MDE {2.8*se:.2f}')
test(ev,'alla (primärt)')
test(ev[ev.type=='addition'],'tillägg')
test(ev[ev.type=='deletion'],'borttag')
test(ev[ev.firm.isin(conv)],'omvandlingsbara')
test(ev[~ev.firm.isin(conv)],'ej omvandlingsbara')
test(ev[ev.sister_member_before&ev.sister_member_after],'systerslag i index')
test(ev[~(ev.sister_member_before&ev.sister_member_after)],'systerslag utanför index')
test(ev[ev.AD>='2017-01-01'],'2017-2026')
