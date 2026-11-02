# Runda 9 (deklarerad 17:45, tillägg 17:50): indexköp 2007-2026 ur LSEG, utländska fonder, migrationer, professionell bevakning.
# Körs från code/claude_checks: python3 runda9.py 0|1|2   (kräver data/runda8_fondagare.csv.gz, data/runda8_analytiker.csv.gz)
import os, re, sys, json
import numpy as np, pandas as pd
STEP = int(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__)); R = os.environ.get('REPO', os.path.join(HERE, '..', '..'))
D = os.environ.get('DATA', os.path.join(HERE, 'data')); OUT = os.path.join(HERE, 'runda9_resultat'); os.makedirs(OUT, exist_ok=True)
F = pd.read_csv(os.path.join(D, 'runda8_fondagare.csv.gz'), low_memory=False)
F = F.rename(columns={'Fund Name': 'fond', 'Fund Type Description': 'ftyp', 'Fund Shares Held (Adjusted)': 'aktier', 'Fund Holdings Filing Date': 'rapport', 'Fund Address Country': 'land'})
F['rapport'] = pd.to_datetime(F.rapport, errors='coerce'); F['asofd'] = pd.to_datetime(F['asof']); F['aktier'] = pd.to_numeric(F.aktier, errors='coerce')
I = pd.read_csv(os.path.join(HERE, 'runda8_input.csv')); I = I[I.kind == 'event'].copy(); I['AD'] = pd.to_datetime(I.AD); I['ED'] = pd.to_datetime(I.ED)
F = F.merge(I[['event_id', 'type', 'AD', 'ED', 'review_cycle']], on='event_id', how='left')
n = F.fond.fillna('').str.lower()
def grupp(r):
    s = r.fond.lower() if isinstance(r.fond, str) else ''
    if re.search(r'nordea sverige passiv|robur access sverige|robur access edge sweden|nordnet sverige index|nordnet indexfond sverige|nordnet superfonden sverige|^lannebo marknad sverige$|^öhman marknad sverige$|nordea inst aktief sverige|ishares omx stockholm', s): return 'OMXSB-index'
    if re.search(r'xact sverige|xact omxsb', s): return 'OMXSB-index' if r.rapport <= pd.Timestamp('2018-12-31') else 'övriga passiva'
    if re.search(r'lansforsakringar sverige index|länsförsäkringar sverige index', s): return 'OMXSB-index' if r.rapport >= pd.Timestamp('2025-06-16') else 'övriga passiva'
    if s == 'storebrand sverige': return 'OMXSB-index' if r.rapport >= pd.Timestamp('2025-10-01') else 'ej passiv'
    if re.search(r'nordea generationsfond|robur access mix|kpa blandfond|nordea donationsmedel', s): return 'OMXSB-blandfond'
    if re.search(r'lansforsakringar sparmal|länsförsäkringar sparmål', s): return 'OMXSB-blandfond' if r.rapport >= pd.Timestamp('2025-06-16') else 'ej passiv'
    if re.search(r'xact omxs30|avanza zero|aktiespararna topp sverige', s): return 'OMXS30' if not (('zero' in s) and r.rapport > pd.Timestamp('2025-06-30')) else 'övriga passiva'
    if re.search(r'(smabolag|småbolag|small ?cap|mikrobolag)', s) and re.search(r'index|indeks|xact|etf|plus ', s) and re.search(r'sverige|svenska|sweden', s): return 'småbolagsindex'
    if r.ftyp == 'Exchange-Traded Fund' or re.search(r'index|indeks|passiv|passive|tracker|exponering', s): return 'övriga passiva'
    return 'ej passiv'
F['grupp'] = [grupp(r) for r in F.itertuples()]
F['svensk'] = F.land.eq('Sweden')
F.loc[(F.grupp == 'övriga passiva') & ~F.svensk, 'grupp'] = 'övriga passiva, utländska'
F.loc[(F.grupp == 'övriga passiva') & F.svensk, 'grupp'] = 'övriga passiva, svenska'
F['gammal'] = (F.asofd - F.rapport).dt.days > 120
F['ok2'] = np.where(F.snap == 'fore', F.rapport < F.AD, F.rapport >= F.ED)
# aktier i aktieslaget vid ED (utdraget)
px = pd.read_csv(os.path.join(D, 'panel_utdrag.csv.gz'), usecols=['ric', 'date', 'shares'], parse_dates=['date']).dropna(subset=['shares'])
def sh(ric, d):
    s = px[(px.ric == ric) & (px.date <= d)].tail(1); return float(s.shares.iloc[0]) if len(s) and s.shares.iloc[0] > 0 else np.nan
EV = I.copy(); EV['shares'] = [sh(r, d) for r, d in zip(EV.ric, EV.ED)]
# rapporterande fonder: fond som har någon rapport (i någon hämtad aktie) med rapportdatum i fönstret före AD respektive efter ED
RAPP = F.dropna(subset=['rapport'])[['fond', 'rapport']].drop_duplicates()
RD = RAPP.groupby('fond').rapport.apply(lambda s: np.sort(s.values)).to_dict()
def rapporterar(fond, a, b):
    d = RD.get(fond); 
    if d is None: return False
    i = np.searchsorted(d, np.datetime64(a)); return i < len(d) and d[i] <= np.datetime64(b)
def netto(G, stabil=True, krav2=False):
    G = G[~G.gammal & G.aktier.notna()]
    if krav2: G = G[G.ok2]
    out = {}
    for (e, g), x in G.groupby(['event_id', 'grupp']):
        f0 = x[x.snap == 'fore'].groupby('fond').aktier.sum(); f1 = x[x.snap == 'efter'].groupby('fond').aktier.sum()
        k = f0.index.union(f1.index)
        if stabil:   # rättelse 17:58: fonden ska rapportera före AD och efter ED (i någon aktie); saknat innehav = 0
            AD, ED = x.AD.iloc[0], x.ED.iloc[0]
            k = [f for f in k if rapporterar(f, AD - pd.Timedelta(days=120), AD - pd.Timedelta(days=1)) and rapporterar(f, ED, ED + pd.Timedelta(days=45))]
        out[(e, g)] = f1.reindex(k).fillna(0).sum() - f0.reindex(k).fillna(0).sum()
    s = pd.Series(out).unstack().fillna(0.0)
    return s
NT = netto(F); NT2 = netto(F, krav2=True); NTa = netto(F, stabil=False)
def pct(NTx):
    X = EV.set_index('event_id')[['type', 'shares', 'review_cycle', 'AD']].join(NTx, how='left')
    sign = np.where(X.type == 'addition', 1, -1)
    for c in NTx.columns: X[c] = sign * 100 * X[c].fillna(0.0) / X.shares
    return X
P, P2, Pa = pct(NT), pct(NT2), pct(NTa)
P.to_csv(os.path.join(OUT, 'nettokop_lseg_events.csv')); P2.to_csv(os.path.join(OUT, 'nettokop_lseg_events_krav2.csv')); Pa.to_csv(os.path.join(OUT, 'nettokop_lseg_events_alla.csv'))
F.groupby(['grupp', 'fond']).size().rename('rader').to_csv(os.path.join(OUT, 'fondgrupper.csv'))

if STEP == 0:
    fi = pd.read_csv(os.path.join(HERE, 'nettokop_v2_events.csv')); fi = fi[fi.status == 'ok']
    ids = EV[['event_id', 'ric', 'review_cycle']].rename(columns={'ric': 'RIC', 'review_cycle': 'review'})
    fi = fi.merge(ids, on=['RIC', 'review'])
    res = {}
    for namn, X in [('primärt', P), ('krav på rapportdatum', P2)]:
        m = fi.merge(X[['OMXSB-index']].rename(columns={'OMXSB-index': 'lseg'}), left_on='event_id', right_index=True).dropna(subset=['lseg', 'netto_OMXSB_ny'])
        m = m[np.isfinite(m.lseg)]
        r = float(np.corrcoef(m.lseg, m.netto_OMXSB_ny)[0, 1]); d = float((m.lseg - m.netto_OMXSB_ny).mean())
        res[namn] = dict(n=len(m), korrelation=r, medel_lseg=float(m.lseg.mean()), medel_fi=float(m.netto_OMXSB_ny.mean()), medelskillnad=d, godkant=bool(r >= 0.6 and abs(d) <= 0.3))
        print(f"{namn}: N {len(m)}, korrelation {r:.2f}, LSEG {m.lseg.mean():.2f} mot FI {m.netto_OMXSB_ny.mean():.2f}, skillnad {d:+.2f} ->", 'GODKÄNT' if res[namn]['godkant'] else 'EJ GODKÄNT')
        for ty in ['addition', 'deletion']:
            q = m[m.type == ty]; print(f'   {ty}: N {len(q)}, LSEG {q.lseg.mean():.2f}, FI {q.netto_OMXSB_ny.mean():.2f}, korr {np.corrcoef(q.lseg, q.netto_OMXSB_ny)[0, 1]:.2f}')
    print('\nfonder per grupp (rader):'); print(F.groupby('grupp').fond.nunique().to_string())
    print('\nOMXSB-indexfonder som hittades:'); print(F[F.grupp == 'OMXSB-index'].groupby('fond').rapport.agg(['min', 'max', 'count']).to_string())
    json.dump(res, open(os.path.join(OUT, 'steg0.json'), 'w'), indent=1, ensure_ascii=False)

if STEP == 2:
    car = pd.read_csv(os.path.join(R, 'output/omxsb_replication_2007/events_car.csv')).set_index('event_id').tot_gi
    X = P.copy(); X['car'] = car.reindex(X.index).values; X = X[X.index.str.startswith('OMXSB')].dropna(subset=['shares'])
    X['per'] = pd.cut(pd.to_datetime(X.AD).dt.year, [2006, 2011, 2016, 2021, 2026], labels=['2007–11', '2012–16', '2017–21', '2022–26'])
    X['index_bland'] = X.get('OMXSB-index', 0) + X.get('OMXSB-blandfond', 0)
    rng = np.random.default_rng(20261102)
    from scipy.stats import t as tdist
    def per_review_ci(s, rv):
        m = s.groupby(rv).mean(); G = len(m); se = m.std(ddof=1) / np.sqrt(G); q = tdist.ppf(.975, G - 1)
        return m.mean(), m.mean() - q * se, m.mean() + q * se, G
    def kvot_ci(d, B=9999):
        rv = d.review_cycle.values; u = np.unique(rv); idx = {k: np.where(rv == k)[0] for k in u}; ks = []
        for _ in range(B):
            s = rng.choice(u, len(u)); ii = np.concatenate([idx[k] for k in s]); den = d.index_val.values[ii].mean()
            ks.append(d.car.values[ii].mean() / den if den > 0 else np.nan)
        ks = np.array(ks); return np.nanpercentile(ks, 2.5), np.nanpercentile(ks, 97.5)
    rows = []
    for ty in ['addition', 'deletion']:
        for per, d in X[X.type == ty].groupby('per', observed=True):
            d = d.dropna(subset=['car']).copy()
            for mått in ['OMXSB-index', 'index_bland']:
                d['index_val'] = d[mått]
                m, lo, hi, G = per_review_ci(d[mått], d.review_cycle); cm, clo, chi, _ = per_review_ci(d.car, d.review_cycle)
                k = d.car.mean() / d[mått].mean() if d[mått].mean() > 0 else np.nan; klo, khi = kvot_ci(d)
                rows.append(dict(typ=ty, period=per, mått=mått, N=len(d), G=G, nettokop=m, nk_lo=lo, nk_hi=hi, car=cm, car_lo=clo, car_hi=chi, kvot=k, kvot_lo=klo, kvot_hi=khi))
    T24 = pd.DataFrame(rows); T24.to_csv(os.path.join(OUT, 'T24_resultat.csv'), index=False)
    print(T24.round(2).to_string(index=False))
    # T25 och T26: andra grupper per period, medel per översyn
    grp = [c for c in ['OMXS30', 'småbolagsindex', 'övriga passiva, svenska', 'övriga passiva, utländska'] if c in X.columns]
    ish = F[F.fond.str.contains('iShares OMX Stockholm', na=False)].event_id.unique()
    rows = []
    for ty in ['addition', 'deletion']:
        for per, d in X[X.type == ty].groupby('per', observed=True):
            r = dict(typ=ty, period=per, N=len(d))
            for c in grp: m, lo, hi, G = per_review_ci(d[c], d.review_cycle); r[c] = f'{m:+.2f} ({lo:+.2f} till {hi:+.2f})'
            rows.append(r)
    T25 = pd.DataFrame(rows); T25.to_csv(os.path.join(OUT, 'T25_T26_resultat.csv'), index=False); print(T25.to_string(index=False))
    # utländska OMXSB-fonder (iShares) separat, 2017-2026
    G2 = F[F.fond.str.contains('iShares OMX Stockholm', na=False)].copy(); G2['grupp'] = 'iShares'
    NI = netto(G2); PI = pct(NI); PI = PI[PI.index.str.startswith('OMXSB')].dropna(subset=['shares'])
    PI = PI[pd.to_datetime(PI.AD) >= '2017-06-01']
    for ty in ['addition', 'deletion']:
        q = PI[PI.type == ty]
        if 'iShares' in q: print(f'iShares OMX Stockholm Capped, {ty} 2017-26: medel {q.iShares.mean():.3f} % av aktierna, N {len(q)}')
