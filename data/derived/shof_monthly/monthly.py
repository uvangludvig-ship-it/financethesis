import pandas as pd, glob, sys, os
D=os.path.expanduser("~/mnt/financethesis_ny/data"); O=os.path.expanduser("~/mnt/financethesis_ny/data/derived/shof_monthly")
# Valuations -> monthly per performanceId
parts=[]
for f in sorted(glob.glob(D+"/Valuations/*.csv")):
    for ch in pd.read_csv(f,sep=';',usecols=['performanceId','date','classcurrencyiso','fundcurrencyiso','netflowclass','netflowfund','secid','tnaclass','tnafund'],chunksize=1_000_000,dtype={'performanceId':str,'secid':str,'classcurrencyiso':str,'fundcurrencyiso':str}):
        ch['ym']=ch['date'].str[:7]
        ch=ch.sort_values(['performanceId','date'])
        g=ch.groupby(['performanceId','ym'])
        a=g.agg(secid=('secid','last'),ccy_class=('classcurrencyiso','last'),ccy_fund=('fundcurrencyiso','last'),
                last_date=('date','max'),tnaclass=('tnaclass','last'),tnafund=('tnafund','last'),
                nf_class=('netflowclass','sum'),nf_fund=('netflowfund','sum'),ndays=('date','count'),nf_class_n=('netflowclass','count'))
        parts.append(a.reset_index())
v=pd.concat(parts)
# chunk boundaries can split a month: re-aggregate
v=v.sort_values(['performanceId','ym','last_date'])
g=v.groupby(['performanceId','ym'])
v=g.agg(secid=('secid','last'),ccy_class=('ccy_class','last'),ccy_fund=('ccy_fund','last'),last_date=('last_date','max'),
        tnaclass=('tnaclass','last'),tnafund=('tnafund','last'),nf_class=('nf_class','sum'),nf_fund=('nf_fund','sum'),
        ndays=('ndays','sum'),nf_class_n=('nf_class_n','sum')).reset_index()
v.to_csv(O+"/shof_valuations_monthly.csv",index=False); print("valuations",v.shape,flush=True)
# RIPS -> month-end SEK total return index per performanceId x returntype
parts=[]
for f in sorted(glob.glob(D+"/Reinvestments/*.csv")):
    for ch in pd.read_csv(f,sep=';',usecols=['performanceId','date','returntype','unit_sek'],chunksize=2_000_000,dtype={'performanceId':str}):
        ch['ym']=ch['date'].str[:7]
        ch=ch.sort_values(['performanceId','returntype','date'])
        a=ch.groupby(['performanceId','returntype','ym']).agg(last_date=('date','max'),tri_sek=('unit_sek','last')).reset_index()
        parts.append(a); print("rips chunk",f[-20:],len(a),flush=True)
r=pd.concat(parts).sort_values(['performanceId','returntype','ym','last_date'])
r=r.groupby(['performanceId','returntype','ym']).agg(last_date=('last_date','max'),tri_sek=('tri_sek','last')).reset_index()
r.to_csv(O+"/shof_rips_monthly.csv",index=False); print("rips",r.shape, r.returntype.value_counts().to_dict(),flush=True)
print("DONE",flush=True)
