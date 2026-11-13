# Runda 10: T28 OMXS30 mot OMXSB och T29 kostnaden för indexsparare. Deklarerat i runda10_deklaration.md (2 nov 2026, 17:58).
# Körs från code/claude_checks:
#   ROOT=../.. PANEL=../../runda2_indata/panel_full.csv.gz INDATA=code/claude_checks/data python3 runda10.py 0|1|2
# Steg 0: urval och datakedja (inga utfall). Steg 1: styrka för T28 (bara N, G, SE, MDE). Steg 2: skattningar och beskrivande tabeller.
import os, sys, json
STEP = int(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'runda3.py')).read()
os.environ['OUT'] = os.path.join(HERE, 'runda10_resultat')
exec(src.split('# %%\nrng = np.random')[0])          # panel, kalender, wsum, medlemmar, händelser (runda 3)
OUT = os.path.join(HERE, 'runda10_resultat'); os.makedirs(OUT, exist_ok=True)

# ---------- inferens (som runda 6, men en konstant får vara med)
rng = np.random.default_rng(20261102)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
def wcr(X, y, g, j=0, B=9999, boot=True):
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X); q = X @ XtXi[j]; adj = G / (G - 1) * (n - 1) / (n - k); Am = XtXi @ X.T
    def bse(Y):
        Bm = Y @ Am.T; E = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in E * q])
        return Bm[:, j], np.sqrt((sg ** 2).sum(1) * adj)
    b0, s0 = bse(y[None, :]); b0, s0 = b0[0], s0[0]; qq = tdist.ppf(.975, G - 1); p = np.nan
    if boot and k > 1:
        Xr = np.delete(X, j, 1); fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]; er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = (np.abs(np.concatenate(ts)[:B]) >= abs(b0 / s0)).mean()
    return dict(b=b0, se=s0, lo=b0 - qq * s0, hi=b0 + qq * s0, p=p, n=n, G=G)
def mde(r): return (tdist.ppf(.975, r['G'] - 1) + tdist.ppf(.80, r['G'] - 1)) * r['se']
def medel(s):   # medel med klustrat intervall (konstant som enda regressor)
    return wcr(np.ones((len(s), 1)), s.y.values.astype(float), s.kluster.values, 0, boot=False)

FL = pd.read_csv(P('output/omxsb_replication_2007/mechanisms/step1_deletion_flags.csv'))
FLAGGED = set(FL[FL.flagged.astype(bool)].event_id)

# ---------- T28-urvalet
I8 = pd.read_csv(os.path.join(HERE, 'runda8_input.csv')); I8 = I8[I8.kind == 'event'].copy()
I8['AD'] = pd.to_datetime(I8.AD); I8['ED'] = pd.to_datetime(I8.ED)
O = I8[I8.event_id.str.startswith('OMXS30')].copy()
OB = ev.dropna(subset=['iAD', 'iED']).copy(); OB = OB[~OB.event_id.isin(FLAGGED)]
logg = []
rows = []
for x in O.itertuples():
    if x.event_id == 'OMXS30-E040': logg.append((x.event_id, 'utesluten: fel aktieslag (Nasdaq anger A)')); continue
    iA, iE = nextpos(x.AD), nextpos(x.ED)
    if x.ric not in CI: logg.append((x.event_id, 'utesluten: RIC saknas i panelen')); continue
    ov = OB[(OB.RIC == x.ric) & (OB.iAD - 1 <= iE + 1) & (OB.iED + 1 >= iA - 1)]
    if len(ov): logg.append((x.event_id, 'utesluten: överlapp med ' + ','.join(ov.event_id))); continue
    c = wsum(x.ric, iA - 1, iE + 1)
    if np.isnan(c): logg.append((x.event_id, 'utesluten: saknade kurser i fönstret')); continue
    s = 1 if x.type == 'addition' else -1
    rows.append(dict(event_id=x.event_id, index='OMXS30', typ=x.type, ric=x.ric, AD=x.AD, ED=x.ED, iA=iA, iE=iE, kluster='OMXS30 ' + str(x.AD.date()), car=c, y=s * c))
for x in OB.itertuples():
    c = wsum(x.RIC, int(x.iAD) - 1, int(x.iED) + 1)
    if np.isnan(c): continue
    s = 1 if x.type == 'addition' else -1
    rows.append(dict(event_id=x.event_id, index='OMXSB', typ=x.type, ric=x.RIC, AD=x.AD, ED=x.ED, iA=int(x.iAD), iE=int(x.iED), kluster=x.review_cycle, car=c, y=s * c))
T28 = pd.DataFrame(rows); T28['d30'] = (T28['index'] == 'OMXS30').astype(float)

# ---------- T29-urvalet: vikter och premier per händelse
FFH = pd.read_csv(os.path.join(IND, 'lseg_freefloat_hist.csv'))
ffh = {(r.review, r.ric): r.ff for r in FFH.dropna(subset=['ff']).itertuples()}
FFC = dict(zip(K.ric, pd.to_numeric(K.freefloat, errors='coerce')))
ROOTS = {}
for c_ in CLOSE.columns: ROOTS.setdefault(root(c_), []).append(c_)
def ffm(c, cy, i):   # aktieslagets fritt flytande börsvärde dag i
    # Rättelse cirka 18:16: panelens kurs är justerad för senare splittar och sammanläggningar, men aktieantalet är historiskt.
    # Kurs × aktier blir då fel (Investor 2018: en fjärdedel av rätt värde; Eniro 2013: 750 gånger för stort).
    # Nu: bolagets mcap (ojusterat) × aktieslagets andel av aktierna i de noterade aktieslagen samma dag.
    if c not in CLOSE or not pd.notna(CLOSE[c].iloc[max(i - 5, 0):i + 1]).any(): return np.nan
    bolag = mc[c].iloc[i] if c in mc else np.nan
    if not (bolag > 0): return np.nan
    sys_ = [o for o in ROOTS.get(root(c), [c]) if pd.notna(CLOSE[o].iloc[max(i - 5, 0):i + 1]).any()]
    if len(sys_) == 1: m = bolag
    else:
        sh = {o: (SH[o].iloc[max(i - 60, 0):i + 1].ffill().iloc[-1] if o in SH else np.nan) for o in sys_}
        m = bolag * sh[c] / sum(sh.values()) if all(v > 0 for v in sh.values()) else np.nan
    if not (m > 0): return np.nan
    f = ffh.get((cy, c), FFC.get(c, np.nan)); f = f if (pd.notna(f) and 0 < f <= 100) else 100.0
    return m * f / 100
T13 = pd.read_csv(os.path.join(HERE, 'runda3_resultat_v2', 'T13_events.csv')); kA = T13[T13.event == 0].groupby('review')['car_ED+1'].mean()   # v2: regeln med rättat börsvärde (cirka 18:20)
T5 = pd.read_csv(os.path.join(HERE, 'runda2_resultat', 'T5urval_T7_T8b_events.csv')); kD = T5[(T5.type == 'deletion') & (T5.event == 0)].groupby('review')['car_ED+1'].mean()
rows = []; saknade_vikter = []
for k, r in rev.iterrows():
    cy = r.review_cycle; iA, iE = int(r.iAD), int(r.iED); evs = ev[ev.k == k]
    adds = set(evs[evs.type == 'addition'].RIC); dels_all = set(evs[evs.type == 'deletion'].RIC)
    after = MED.get(cy, set()); before = MED.get(cyc[k - 1], set()) if k > 0 else (after - adds) | dels_all
    tot_a = np.nansum([ffm(c, cy, iA - 1) for c in after]); tot_b = np.nansum([ffm(c, cy, iA - 1) for c in before])
    levande = [c for c in after if c in CLOSE and pd.notna(CLOSE[c].iloc[max(iA - 6, 0):iA]).any()]
    utan = [c for c in levande if np.isnan(ffm(c, cy, iA - 1))]
    saknade_vikter.append(dict(review=cy, medlemmar_med_kurs=len(levande), utan_varde=len(utan), vilka=' '.join(utan)))
    for x in evs.itertuples():
        if x.event_id in FLAGGED: continue
        add = x.type == 'addition'; s = 1 if add else -1
        w = ffm(x.RIC, cy, iA - 1) / (tot_a if add else tot_b)
        prem = s * wsum(x.RIC, iA - 1, iE - 1)
        c1 = wsum(x.RIC, iA - 1, iE + 1); kk = (kA if add else kD).get(cy, np.nan)
        rows.append(dict(review=cy, AD=r.AD, ar=r.AD.year, event_id=x.event_id, typ=x.type, ric=x.RIC, w=w, prem=prem, prem2=s * (c1 - kk)))
T29 = pd.DataFrame(rows)
T29['per'] = pd.cut(T29.ar, [2006, 2011, 2016, 2021, 2026], labels=['2007–11', '2012–16', '2017–21', '2022–26'])
AUM = pd.read_csv(os.path.join(HERE, 'data', 'shof', 'tracker_aum_shof_v2.csv')).set_index('manad').inkl_xact_omxsb_mdkr
def aum_dec(y): return AUM.get(f'{y}-12', AUM.iloc[-1])

if STEP == 0:
    print('T28: OMXS30-händelser', len(O), '| med i urvalet', int((T28['index'] == 'OMXS30').sum()), '| OMXSB', int((T28['index'] == 'OMXSB').sum()))
    for e, m in logg: print('  ', e, m)
    print('  OMXS30 per typ:', T28[T28['index'] == 'OMXS30'].typ.value_counts().to_dict(), '| kluster', T28[T28['index'] == 'OMXS30'].kluster.nunique())
    print('T29: händelser', len(T29), '| saknar vikt', int(T29.w.isna().sum()), '| saknar premie', int(T29.prem.isna().sum()), '| saknar sekundär premie', int(T29.prem2.isna().sum()))
    SV = pd.DataFrame(saknade_vikter); print('  medlemmar med kurs men utan börsvärde dagen före AD: max', int(SV.utan_varde.max()), 'per översyn av median', int(SV.medlemmar_med_kurs.median()), 'medlemmar med kurs')
    print(SV[SV.utan_varde > 0][['review', 'utan_varde', 'vilka']].to_string(index=False))
    print('  vikt per tillägg, median', round(T29[T29.typ == 'addition'].w.median() * 100, 3), '%; summa per översyn, median', round(T29.groupby('review').w.sum().median() * 100, 2), '%')
    SV.to_csv(os.path.join(OUT, 'T29_medlemmar_utan_varde.csv'), index=False)
    T29[['review', 'event_id', 'typ', 'ric', 'w']].to_csv(os.path.join(OUT, 'T29_vikter.csv'), index=False)   # bara vikter, inga premier
    pd.DataFrame(logg, columns=['event_id', 'orsak']).to_csv(os.path.join(OUT, 'T28_uteslutna.csv'), index=False)
    sys.exit()

if STEP == 1:
    X = np.column_stack([T28.d30.values, np.ones(len(T28))]); r = wcr(X, T28.y.values, T28.kluster.values, 0, boot=False)
    res = dict(n=int(r['n']), G=int(r['G']), se=float(r['se']), mde=float(mde(r)), villkor=3.0, godkant=bool(mde(r) <= 3.0),
               n_omxs30=int(T28.d30.sum()), G_omxs30=int(T28[T28.d30 == 1].kluster.nunique()))
    print(f"T28: N {res['n']} (OMXS30 {res['n_omxs30']}), G {res['G']} (OMXS30 {res['G_omxs30']}), SE {res['se']:.3f}, MDE {res['mde']:.2f} (villkor ≤ 3) ->", 'GODKÄNT' if res['godkant'] else 'STOPP')
    json.dump(dict(T28=res), open(os.path.join(OUT, 'steg1.json'), 'w'), indent=1, ensure_ascii=False)
    sys.exit()

if STEP == 2:
    st1 = json.load(open(os.path.join(OUT, 'steg1.json')))['T28']; out = []
    if st1['godkant']:
        X = np.column_stack([T28.d30.values, np.ones(len(T28))]); r = wcr(X, T28.y.values, T28.kluster.values, 0)
        out.append(dict(test='T28 skillnad OMXS30 − OMXSB', **r, mde=mde(r)))
        print(f"T28 skillnad: {r['b']:+.2f} ({r['lo']:+.2f} till {r['hi']:+.2f}), p {r['p']:.3f}, N {r['n']}, G {r['G']}, MDE {mde(r):.2f}")
    else: print('T28 skillnad: stoppad i steg 1, skattas inte')
    # beskrivande medel
    for (ix, ty), s in T28.groupby(['index', 'typ']):
        r = medel(s); out.append(dict(test=f'medel {ix} {ty}', **r))
        print(f"  {ix} {ty}: CAR med vänt tecken för borttag {r['b']:+.2f} ({r['lo']:+.2f} till {r['hi']:+.2f}), N {r['n']}, G {r['G']}")
    for ix in ['OMXS30', 'OMXSB']:
        r = medel(T28[T28['index'] == ix]); out.append(dict(test=f'medel {ix} alla', **r)); print(f"  {ix} alla: {r['b']:+.2f} ({r['lo']:+.2f} till {r['hi']:+.2f}), N {r['n']}, G {r['G']}")
    pd.DataFrame(out).to_csv(os.path.join(OUT, 'T28_resultat.csv'), index=False)
    T28.to_csv(os.path.join(OUT, 'T28_urval.csv'), index=False)
    # OMXS30-fondernas nettoköp (LSEG, regeln från runda 9) i procent av aktierna vid ED
    ns = {'__file__': os.path.join(HERE, 'runda9.py')}; os.environ.setdefault('DATA', os.path.join(HERE, 'data'))
    sys_argv = sys.argv[:]; sys.argv = ['runda9.py', '9']
    exec(open(os.path.join(HERE, 'runda9.py')).read().split('NT = netto(F)')[0], ns); sys.argv = sys_argv
    F9 = ns['F']; NT = ns['netto'](F9[F9.event_id.str.startswith('OMXS30') & (F9.grupp == 'OMXS30')])
    def shares_ed(ric, iE):
        if ric not in SH: return np.nan
        v = SH[ric].iloc[max(iE - 10, 0):iE + 1].ffill().iloc[-1]; return v if v > 0 else np.nan
    O30 = T28[T28['index'] == 'OMXS30'].copy()
    O30['nettokop'] = [np.sign(1 if t == 'addition' else -1) * 100 * (NT['OMXS30'].get(e, 0.0) if 'OMXS30' in NT else 0.0) / shares_ed(ric, iE)
                       for e, t, ric, iE in zip(O30.event_id, O30.typ, O30.ric, O30.iE)]
    O30['har_fonddata'] = O30.event_id.isin(F9.event_id.unique())
    O30.to_csv(os.path.join(OUT, 'T28_omxs30_nettokop.csv'), index=False)
    for ty, s in O30.groupby('typ'):
        s2 = s[s.har_fonddata]
        print(f"  OMXS30 {ty}: nettoköp OMXS30-fonder {s2.nettokop.mean():.3f} % av aktierna (N {len(s2)} med fonddata av {len(s)}), CAR {s2.y.mean():+.2f}, pris per köpt % {s2.y.mean() / s2.nettokop.mean() if s2.nettokop.mean() > 0 else float('nan'):.1f}")
    # T29: kostnad per översyn, år och period
    for namn, col in [('primär', 'prem'), ('sekundär', 'prem2')]:
        d = T29.dropna(subset=['w', col]).copy(); d['bidrag'] = d.w * d[col] * 100   # punkter av fondförmögenheten
        R = d.groupby(['review', 'ar', 'per'], observed=True).agg(kostnad=('bidrag', 'sum'), omsattning=('w', 'sum'), n=('bidrag', 'size')).reset_index()
        R['mkr'] = R.kostnad / 1e4 * np.array([aum_dec(y) for y in R.ar]) * 1000
        rows = []
        for per, g in R.groupby('per', observed=True):
            ar_n = g.ar.nunique(); rpy = len(g) / ar_n; v = g.kostnad.values; mk = g.mkr.values; om = g.omsattning.values
            bs = rng.integers(0, len(g), (9999, len(g)))
            rows.append(dict(premie=namn, period=per, oversyner=len(g), handelser=int(g.n.sum()), ar=ar_n,
                             kostnad_pkt_per_ar=v.mean() * rpy, lo=np.percentile(v[bs].mean(1) * rpy, 2.5), hi=np.percentile(v[bs].mean(1) * rpy, 97.5),
                             mkr_per_ar=mk.mean() * rpy, mkr_lo=np.percentile(mk[bs].mean(1) * rpy, 2.5), mkr_hi=np.percentile(mk[bs].mean(1) * rpy, 97.5),
                             omsattning_pct_per_ar=om.mean() * rpy * 100))
        Y = pd.DataFrame(rows); Y.to_csv(os.path.join(OUT, f'T29_{namn}.csv'), index=False); R.to_csv(os.path.join(OUT, f'T29_per_oversyn_{namn}.csv'), index=False)
        print(f'\nT29 {namn}:'); print(Y.round(2).to_string(index=False))
    T29.to_csv(os.path.join(OUT, 'T29_handelser.csv'), index=False)
