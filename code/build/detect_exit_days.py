# Detect Pensionsmyndigheten's redemption days in losing funds from daily Morningstar valuations.
# Uses only units outstanding (shares), TNA and estimated net flow. No returns are computed or read.
import pandas as pd, numpy as np, glob, os, json
# Paths are relative to the repo root (financethesis). Raw Morningstar files are gitignored; get them from SHoF.
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
D=REPO+'/data/raw/shof/Valuations'  # SHoF daily exports, shared by hand (see data/MANIFEST.md)
O=REPO+'/data/derived/exit_days'; os.makedirs(O,exist_ok=True)
m=pd.read_csv(REPO+'/data/derived/measurements/agentA_task1_round_membership.csv')
cw=pd.read_csv(REPO+'/data/derived/ftn/crosswalk_ppm_shof.csv')
los=m[m.role=='loser'].merge(cw[['fondnr','performanceid','fundid']],on='fondnr',how='left')
pids=set(los.performanceid.dropna())
parts=[]
for f in sorted(glob.glob(D+'/*.csv')):
    for ch in pd.read_csv(f,sep=';',usecols=['performanceId','date','netflowclass','netflowfund','shares','tnaclass','tnafund','classcurrencyiso','fundcurrencyiso'],chunksize=1_000_000,dtype={'performanceId':str}):
        parts.append(ch[ch.performanceId.isin(pids)])
v=pd.concat(parts).sort_values(['performanceId','date'])
v['date']=pd.to_datetime(v['date'])
v.to_csv(O+'/losers_daily_valuations.csv',index=False)
rows=[]
for _,r in los.iterrows():
    d=v[v.performanceId==r.performanceid].copy()
    if d.empty: continue
    d['tna_lag']=d.tnafund.shift(1); d['sh_lag']=d.shares.shift(1)
    d['flow_pct']=100*d.netflowfund/d.tna_lag
    d['dshares_pct']=100*(d.shares/d.sh_lag-1)
    award=pd.to_datetime(r.award)
    end=pd.to_datetime(r.avslutsdatum) if pd.notna(r.avslutsdatum) else d.date.max()
    end=end+pd.Timedelta(days=45)
    w=d[(d.date>=award)&(d.date<=end)]
    pre=d[(d.date<award)&(d.date>=award-pd.Timedelta(days=365))]
    big=w[(w.flow_pct<=-5)|(w.dshares_pct<=-5)]
    rows.append(dict(round=r['round'],award=r.award,fondnr=r.fondnr,fondnamn=r.fondnamn,kategori=r.kategori,
        performanceid=r.performanceid,ccy=d.fundcurrencyiso.iloc[-1],avslutsdatum=r.avslutsdatum,
        mv_award_msek=r.mv_award/1e6,
        tna_at_award=float(d[d.date<=award].tnafund.iloc[-1]) if (d.date<=award).any() else np.nan,
        last_obs=str(d.date.max().date()),
        n_days_window=len(w),
        n_big_days=len(big),
        big_days=';'.join(f"{x.date.date()}:{x.flow_pct:.1f}%/{x.dshares_pct:.1f}%" for x in big.itertuples()),
        sum_flow_window_pct=float(100*w.netflowfund.sum()/w.tna_lag.iloc[0]) if len(w) and w.tna_lag.iloc[0]>0 else np.nan,
        sum_big_flow_pct=float(big.flow_pct.sum()),
        max_single_day_pct=float(w.flow_pct.min()) if len(w) else np.nan,
        pre_year_days_le_minus5=int(((pre.flow_pct<=-5)|(pre.dshares_pct<=-5)).sum()),
        pre_year_sd_flow_pct=float(pre.flow_pct.std()) if len(pre)>5 else np.nan))
out=pd.DataFrame(rows)
out.to_csv(O+'/exit_days_by_loser.csv',index=False)
print(out[['round','fondnamn','n_big_days','max_single_day_pct','sum_big_flow_pct','sum_flow_window_pct','pre_year_days_le_minus5']].to_string())
print('DONE')
