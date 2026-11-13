# T18: tvillingaktier vid MSCI-ändringar, enligt msci_deklaration.md (2 november 09:30).
# python3 msci_t18.py 0  -> bara antal händelser efter varje uteslutning (ingen kurs i händelsefönster används för utfall)
# python3 msci_t18.py 1  -> första steget och styrka (inga skattningar av skillnaden mellan aktieslagen)
# python3 msci_t18.py 2  -> skattningar, bara om steg 1 är godkänt
import os, re, sys, json
import numpy as np, pandas as pd
from scipy.stats import t as tdist

STEG = int(sys.argv[1])
HER = os.path.dirname(os.path.abspath(__file__))
_r = os.path.abspath(os.path.join(HER, '../../..'))
REPO = os.environ.get('REPO', _r if os.path.exists(os.path.join(_r, 'data/raw/lseg')) else '/home/claude/uvangludvig-ship-it/financethesis')
UT = os.path.join(HER, 't18_resultat'); os.makedirs(UT, exist_ok=True)
rng = np.random.default_rng(20261102)

# ---------- kalender
ix = pd.read_csv(f'{REPO}/data/raw/lseg/panel_2005_2026/indices_daily (1).csv', parse_dates=['date'])
cal = pd.DatetimeIndex(ix.loc[(ix.ric == '.OMXSBGI') & ix.close.notna(), 'date'].sort_values().unique())
def pos_on_or_after(d):
    i = cal.searchsorted(pd.Timestamp(d)); return int(i) if i < len(cal) else None
def pos_after(d):
    i = cal.searchsorted(pd.Timestamp(d), side='right'); return int(i) if i < len(cal) else None

# ---------- kurser: första hämtningen (pris, volym, totalavkastning) och kompletteringar (TRDPRC_1, ACVOL_UNS)
P1 = pd.read_csv(os.path.join(HER, 'indata', 'msci_tvilling_priser.csv'), parse_dates=['Date'])
serier = {}
for r, g in P1.groupby('ric'):
    g = g.sort_values('Date').drop_duplicates('Date', keep='last').set_index('Date')
    if g['Price Close'].notna().sum() < 50: continue
    serier[r] = dict(close=g['Price Close'], vol=g['Volume'], tr=g['Daily Total Return'], kalla='forsta')
komp = [os.path.join(HER, 'indata', f) for f in ['msci_tvilling_priser_2.csv']]
komp.append(f'{REPO}/data/raw/lseg/twins/tvilling_priser_lseg_2.csv')
for f in komp:
    if not os.path.exists(f): continue
    K = pd.read_csv(f, parse_dates=['Date'])
    if 'TRDPRC_1' not in K.columns: continue
    if 'metod' in K.columns: K = K[(K.metod == 1) | K.metod.isna()]
    for r, g in K.groupby('ric'):
        if r in serier: continue
        g = g[g.TRDPRC_1.notna()].sort_values('Date').drop_duplicates('Date', keep='first').set_index('Date')
        if len(g) < 50: continue
        serier[r] = dict(close=g['TRDPRC_1'], vol=g.get('ACVOL_UNS', pd.Series(dtype=float)), tr=None, kalla='komplettering')
def on_cal(s): return s.reindex(cal) if s is not None else None
CL = {r: on_cal(v['close']) for r, v in serier.items()}
VO = {r: on_cal(v['vol']) for r, v in serier.items()}
TRI = {}
for r, v in serier.items():
    if v['tr'] is not None and v['tr'].notna().sum() > 50:
        t_ = on_cal(v['tr']); TRI[r] = (1 + t_.fillna(0) / 100).cumprod().where(CL[r].ffill().notna())

# ---------- händelser
C = pd.read_csv(os.path.join(HER, 'msci_sweden_changes_2007_2026.csv'))
Kd = pd.read_csv(os.path.join(HER, 'msci_tvilling_kandidater.csv'))
datum = C.groupby('review').agg(AD=('announcement_date', 'first'), asofdag=('effective_date', 'first'))
E = Kd.merge(datum, left_on='review', right_index=True, how='left')
E['iAD'] = E.AD.map(pos_on_or_after); E['iED'] = E['asofdag'].map(pos_after)
E['sign'] = np.where(E.typ.str.startswith('tillägg'), 1, -1)
stem = lambda r: re.sub(r'(sdb)?[abcrA]?\.ST.*$', '', str(r))
E['bolag_rot'] = E.ric.map(stem)

# andra indexhändelser för samma bolag: OMXSB (events_car) och OMXS30
ev = pd.read_csv(f'{REPO}/output/omxsb_replication_2007/events_car.csv', parse_dates=['AD', 'ED'])
andra = [(stem(r), pos_on_or_after(a), pos_on_or_after(e)) for r, a, e in zip(ev.RIC, ev.AD, ev.ED)]
try:
    o30 = pd.read_csv(f'{REPO}/data/input/omxsb/omxs30_changes_2005_2026.csv')
    for tk, a, e in zip(o30.ticker.astype(str), o30.announcement_date, o30.effective_date):
        if isinstance(a, str) and isinstance(e, str):
            andra.append((tk.split(' ')[0], pos_on_or_after(a), pos_on_or_after(e)))
except FileNotFoundError:
    pass

def overlap(a1, b1, a2, b2): return a1 is not None and a2 is not None and b1 is not None and b2 is not None and a1 <= b2 and a2 <= b1

def stale_share(r, a, b):
    if r not in CL: return np.nan
    p = CL[r].iloc[max(a, 0):b + 1].dropna()
    return float((p.diff().iloc[1:] == 0).mean()) if len(p) > 5 else np.nan

def series_pair(x, y):
    if x in TRI and y in TRI: return TRI[x], TRI[y], 'tr'
    return CL[x], CL[y], 'pris'
FL = {}
def flags(x, y):
    if (x, y) not in FL:
        A_, B_, src = series_pair(x, y)
        r = np.log(A_.ffill() / B_.ffill()).diff().values; nxt = np.r_[r[1:], np.nan]
        spike = (np.abs(r) > 0.08) & (np.abs(r + nxt) < 0.25 * np.abs(r))
        jump = (np.abs(r) > 0.15) & (np.abs(r + nxt) > 0.75 * np.abs(r))
        FL[(x, y)] = (A_, B_, src, np.nan_to_num(spike).astype(bool), np.nan_to_num(jump).astype(bool))
    return FL[(x, y)]
def spread(x, y, a, b):
    A_, B_, src, spike, jump = flags(x, y)
    if a - 1 < 0 or b >= len(cal): return np.nan, 'utanför'
    if spike[a - 1] or spike[b]: return np.nan, 'R2'
    if jump[a:b + 1].any(): return np.nan, 'R3'
    if pd.isna(A_.iloc[a - 1]) or pd.isna(A_.iloc[b]) or pd.isna(B_.iloc[a - 1]) or pd.isna(B_.iloc[b]): return np.nan, 'saknas'
    v = np.log(A_.iloc[b] / A_.iloc[a - 1]) - np.log(B_.iloc[b] / B_.iloc[a - 1])
    return (100 * v, 'ok') if np.isfinite(v) else (np.nan, 'saknas')

doy = np.array(cal.dayofyear)
rows, pools = [], {}
for i, e in E.iterrows():
    status = 'ok'
    if e.systerslaget == 'kontrolleras': status = 'U1 systerstatus okänd'
    elif e.iAD is None or e.iED is None or pd.isna(e.iAD) or pd.isna(e.iED): status = 'datum saknas'
    elif e.ric not in CL or e.syster_ric not in CL: status = 'kurs saknas'
    a, b = (int(e.iAD) - 1, int(e.iED) + 1) if status == 'ok' else (None, None)
    egna = [(int(x.iAD), int(x.iED)) for x in E[(E.bolag_rot == e.bolag_rot)].itertuples() if pd.notna(x.iAD) and pd.notna(x.iED)]
    egna += [(p, q) for rr, p, q in andra if rr == e.bolag_rot and p is not None and q is not None]
    if status == 'ok' and any(overlap(a, b, p - 1, q + 1) for rr, p, q in andra if rr == e.bolag_rot):
        status = 'U2 överlapp med OMXSB/OMXS30'
    st = stale_share(e.syster_ric, int(e.iAD) - 60, int(e.iED) + 20) if status == 'ok' else np.nan
    v = np.nan
    if status == 'ok':
        if st > 0.5: status = 'R4 stillastående systerslag'
        else:
            v, why = spread(e.ric, e.syster_ric, a, b)
            if why != 'ok': status = why
    pl = []
    if status == 'ok':
        L = b - a + 1; ad = cal[int(e.iAD)].dayofyear
        for s in range(61, len(cal) - L - 21):
            if cal[s].year == cal[int(e.iAD)].year: continue
            dd = abs(doy[s] - ad); dd = min(dd, 365 - dd)
            if dd > 45 or any((s + L + 20 >= p - 60) and (s - 60 <= q + 20) for p, q in egna): continue
            x, w = spread(e.ric, e.syster_ric, s, s + L - 1)
            if np.isfinite(x): pl.append(e.sign * x)
        if len(pl) < 20: status = 'färre än 20 placebofönster'
    pools[i] = np.array(pl)
    # första steget: onormal log-omsättning dagen före ED, ändrat slag minus systerslag
    fs = np.nan
    if status == 'ok':
        def avol(r):
            vv = VO[r]; d = vv.iloc[int(e.iED) - 1]; base = vv.iloc[int(e.iED) - 60:int(e.iED) - 20].median()
            return np.log1p(d) - np.log1p(base) if pd.notna(d) and pd.notna(base) else np.nan
        fs = avol(e.ric) - avol(e.syster_ric)
    rows.append(dict(idx=i, review=e.review, typ=e.typ, bolag=e.bolag, slag=e.slag, index=e['index'], systerslaget=e.systerslaget,
                     status=status, stillastaende=st, n_placebo=len(pl), _spread=e.sign * v if np.isfinite(v) else np.nan, forsta_steget=fs,
                     kalla=series_pair(e.ric, e.syster_ric)[2] if status == 'ok' else ''))
D = pd.DataFrame(rows)
ok = D[D.status == 'ok']; okST = ok[ok['index'] == 'ST']

if STEG == 0:
    print('status per händelse:'); print(D.groupby(['index', 'status']).size().to_string())
    print('kvar: Standard', len(okST), '| Small Cap', int((ok['index'] == 'SC').sum()))
    D.drop(columns=['_spread', 'forsta_steget']).to_csv(os.path.join(UT, 'steg0_urval.csv'), index=False)
    sys.exit()

def null_means(sub, B=5000):
    return np.array([np.mean([rng.choice(pools[k]) for k in sub.idx]) for _ in range(B)])

if STEG == 1:
    n = len(okST); fsv = okST.forsta_steget.dropna(); m = fsv.mean(); se = fsv.std(ddof=1) / np.sqrt(len(fsv))
    lo, hi = m - tdist.ppf(.975, len(fsv) - 1) * se, m + tdist.ppf(.975, len(fsv) - 1) * se
    nm = null_means(okST); mde = 2.8 * nm.std()
    villkor = dict(minst_15=n >= 15, forsta_steget_over_0=bool(lo > 0), mde_hogst_2=bool(mde <= 2.0))
    ok1 = all(villkor.values())
    print(f'Standard-händelser kvar: {n} (gräns 15)')
    print(f'Första steget, onormal log-omsättning dagen före ED, ändrat slag minus systerslag: {m:+.2f} ({lo:+.2f} till {hi:+.2f}), N {len(fsv)}')
    print(f'Minsta upptäckbara effekt: {mde:.2f} procentenheter (gräns 2,0)')
    print('Steg 1', 'GODKÄNT' if ok1 else 'STOPP', villkor)
    json.dump(dict(passed=ok1, n=n, forsta_steget=[m, lo, hi], mde=mde, villkor=villkor), open(os.path.join(UT, 'steg1.json'), 'w'), indent=1)
    D.drop(columns=['_spread']).to_csv(os.path.join(UT, 'steg1_urval.csv'), index=False)
    sys.exit()

s1 = json.load(open(os.path.join(UT, 'steg1.json')))
if not s1['passed']: sys.exit('STOPP: steg 1 inte godkänt, skattningarna visas inte.')
res = []
for lab, sub in [('Standard (primär)', okST), ('Standard, systerslaget utanför MSCI', okST[okST.systerslaget == 'utanför']),
                 ('Small Cap', ok[ok['index'] == 'SC']), ('Alla', ok)]:
    if len(sub) < 3: continue
    m = sub._spread.mean(); nm = null_means(sub); c = nm - nm.mean()
    p = (np.abs(c) >= abs(m - nm.mean())).mean()
    res.append(dict(urval=lab, N=len(sub), bolag=sub.bolag.nunique(), skattning=round(m, 2), ci_lo=round(m - np.percentile(c, 97.5), 2),
                    ci_hi=round(m - np.percentile(c, 2.5), 2), p=round(p, 3)))
R = pd.DataFrame(res); print(R.to_string(index=False))
# båda slagens rörelse mot marknaden, [AD-1, ED+1], tecken vänt för borttag
mkt = ix.pivot(index='date', columns='ric', values='close').reindex(cal)['.OMXSBGI']
def car(r, a, b):
    s_ = TRI.get(r, CL[r]); return 100 * (np.log(s_.iloc[b] / s_.iloc[a - 1]) - np.log(mkt.iloc[b] / mkt.iloc[a - 1]))
E2 = E.loc[okST.idx]
okST = okST.assign(andrat_mot_marknad=[x.sign * car(x.ric, int(x.iAD) - 1, int(x.iED) + 1) for x in E2.itertuples()],
                   syster_mot_marknad=[x.sign * car(x.syster_ric, int(x.iAD) - 1, int(x.iED) + 1) for x in E2.itertuples()])
print(f"Standard: ändrat slag mot marknaden {okST.andrat_mot_marknad.mean():+.2f}, systerslaget {okST.syster_mot_marknad.mean():+.2f} (medel, tecken vänt för borttag)")
okST.to_csv(os.path.join(UT, 'T18_standard_events.csv'), index=False)
R.to_csv(os.path.join(UT, 'T18_results.csv'), index=False); D.to_csv(os.path.join(UT, 'T18_events.csv'), index=False)
