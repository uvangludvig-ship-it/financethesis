from common import *
l1=pd.read_csv('../../data/raw/lseg/twins/tvilling_priser_lseg.csv',parse_dates=['Date'])
l2=pd.read_csv('../../data/raw/lseg/twins/tvilling_priser_lseg_2.csv',parse_dates=['Date'])
frames=[]
for r in ['NCCa.ST','SWECa.ST']:
    g=l1[(l1.ric==r)&l1['Price Close'].notna()].sort_values(['Date','Volume']).drop_duplicates('Date',keep='first')
    frames.append(pd.DataFrame({'ric':r,'date':g.Date,'close':g['Price Close'],'volume':g.Volume}))
for r in ['BONAVa.ST','RATOa.ST']:
    g=l2[(l2.ric==r)&(l2.metod==1)&l2.TRDPRC_1.notna()].drop_duplicates('Date')
    frames.append(pd.DataFrame({'ric':r,'date':g.Date,'close':g.TRDPRC_1,'volume':g.ACVOL_UNS}))
ext=pd.concat(frames)
P=pd.concat([px[['ric','date','close','volume']],ext])
P=P[P.date.isin(cal)]
CLOSE=P.pivot_table(index='date',columns='ric',values='close',aggfunc='last').reindex(cal)
VOL=P.pivot_table(index='date',columns='ric',values='volume',aggfunc='last').reindex(cal)
# price return only on days with a price; days without trade -> NaN (stale), handled by cumulating log prices between valid points
