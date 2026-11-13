# Första steget v2 enligt forsta_steget_deklaration.md
import pandas as pd, numpy as np
F=pd.read_csv('data/fi_all_funds_klass.csv'); H=pd.read_pickle('data/fi_all_holdings.pkl')
ALL=set(x for v in [['SE0006593901'],['SE0006593919'],['SE0008091581'],['SE0000489098','SE0014960373'],['SE0000171100'],['SE0000120669'],['SE0000115420'],['SE0000115446'],['SE0000190126'],['SE0000107203'],['SE0010714279'],['SE0010714287'],['SE0000118952'],['SE0000117970'],['SE0014684510','SE0015810239','SE0022060513'],['SE0008373906','SE0013256682','SE0014684528','SE0015810247','SE0022060521']] for x in v)
H=H[H['isin'].isin(ALL)].copy()
H['fid']=H.fund_id.astype(str)
H['antal']=pd.to_numeric(H.antal.astype(str).str.replace(',','.'),errors='coerce'); H['kvartal']=pd.to_datetime(H.kvartal)
ISIN={('KLOV','A'):['SE0006593901'],('KLOV','B'):['SE0006593919'],('BONAV','A'):[],('BONAV','B'):['SE0008091581'],
      ('SWEC','A'):[],('SWEC','B'):['SE0000489098','SE0014960373'],('SSAB','A'):['SE0000171100'],('SSAB','B'):['SE0000120669'],
      ('VOLV','A'):['SE0000115420'],('VOLV','B'):['SE0000115446'],('INDU','A'):['SE0000190126'],('INDU','C'):['SE0000107203'],
      ('CORE','A'):['SE0010714279'],('CORE','B'):['SE0010714287'],('NCC','A'):['SE0000118952'],('NCC','B'):['SE0000117970'],
      ('KINV','A'):['SE0014684510','SE0015810239','SE0022060513'],('KINV','B'):['SE0008373906','SE0013256682','SE0014684528','SE0015810247','SE0022060521']}
for (f,c),v in ISIN.items():
    o=[x for (g,d),w in ISIN.items() if g==f and d!=c for x in w]; assert not set(v)&set(o), (f,c)
tw=pd.read_csv('twin_events.csv'); tw=tw[tw.usable_pair==True]; tw['AD']=pd.to_datetime(tw.AD); tw['ED']=pd.to_datetime(tw.ED); tw=tw[tw.AD>='2019-01-01']
fin=set(pd.read_csv('twin_results_events.csv').event_id)
px=pd.read_csv('data/panel_utdrag.csv.gz',usecols=['ric','date','shares'],parse_dates=['date'])
def shares(ric,d):
    s=px[(px.ric==ric)&(px.date<=d)&px.shares.notna()]; return s.shares.iloc[-1] if len(s) else np.nan
import re
root=lambda r: re.match(r'([A-Z]+?)[a-z]?\.ST',str(r)).group(1)
qs=sorted(H.kvartal.unique())
rows=[]; detail=[]
for _,e in tw.iterrows():
    f=root(e.event_key)
    if (f,e.class_changed) not in ISIN: continue
    qb=max(q for q in qs if q<e.AD); qa=min(q for q in qs if q>=e.ED)
    sign=1 if e.type=='addition' else -1
    r=dict(event_id=e.event_id,review=e.review_cycle,bolag=f,typ=e.type,indexslag=e.class_changed,systerslag=e.sister_class,i_slutligt_urval=e.event_id in fin,
           qb=qb.date(),qa=qa.date(),dagar_qb_till_AD=(e.AD-qb).days,dagar_ED_till_qa=(qa-e.ED).days)
    for defn in ['strikt','bred']:
        ids={q:set(F[(F.kvartal==str(pd.Timestamp(q).date()))&F[defn]].fund_id.astype(str)) for q in [qb,qa]}
        for leg,cls,ric in [('index',e.class_changed,e.event_key),('syster',e.sister_class,e.sister_ric)]:
            isins=ISIN[(f,cls)]
            hb=H[(H.kvartal==qb)&H.fid.isin(ids[qb])&H['isin'].isin(isins)].antal.sum()
            ha=H[(H.kvartal==qa)&H.fid.isin(ids[qa])&H['isin'].isin(isins)].antal.sum()
            sh=shares(ric,pd.Timestamp(qa))
            r[f'{defn}_{leg}_före_mn']=hb/1e6; r[f'{defn}_{leg}_efter_mn']=ha/1e6
            r[f'{defn}_{leg}_förändring_pct']=sign*100*(ha-hb)/sh if sh==sh and sh>0 else np.nan
            if defn=='strikt':
                for fid in ids[qb]|ids[qa]:
                    b=H[(H.kvartal==qb)&(H.fid==fid)&H['isin'].isin(isins)].antal.sum(); a=H[(H.kvartal==qa)&(H.fid==fid)&H['isin'].isin(isins)].antal.sum()
                    if a or b: detail.append(dict(event_id=e.event_id,ben=leg,fond=F[F.fund_id.astype(str)==fid].namn.iloc[-1],före=b,efter=a))
    rows.append(r)
R=pd.DataFrame(rows); R.to_csv('forsta_steget_v2_events.csv',index=False); pd.DataFrame(detail).to_csv('forsta_steget_v2_fonder.csv',index=False)
pd.set_option('display.width',260)
print(R[['review','bolag','typ','indexslag','i_slutligt_urval','dagar_qb_till_AD','dagar_ED_till_qa','strikt_index_förändring_pct','strikt_syster_förändring_pct','bred_index_förändring_pct','bred_syster_förändring_pct']].round(3).to_string(index=False))
for defn in ['strikt','bred']:
    for sub,lab in [(R,'alla'),(R[R.i_slutligt_urval],'slutligt urval')]:
        x=sub[f'{defn}_index_förändring_pct'].dropna(); y=sub[f'{defn}_syster_förändring_pct'].dropna()
        print(f'{defn}, {lab}: indexslag N {len(x)} medel {x.mean():.3f} median {x.median():.3f} | fel tecken {int((x<0).sum())} | systerslag N {len(y)} medel {y.mean():.3f} median {y.median():.3f}')
