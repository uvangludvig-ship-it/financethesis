# Runda 6: T19 förutsägbarhet och T20 dos-respons. Deklarerat i runda6_deklaration.md (2 nov 2026, 10:40 CET).
# Körs från code/claude_checks med repo-roten som ROOT. Två lägen:
#   utdrag (T19a/c/d, T20):  UTDRAG=1 ROOT=../.. PANEL=data/panel_utdrag.csv.gz INDATA=code/claude_checks/data python3 runda6.py 0|1|2
#   hela panelen (T19b):     ROOT=../.. PANEL=../../runda2_indata/panel_full.csv.gz INDATA=code/claude_checks/data python3 runda6.py 0|1|2
#   (panel_full.csv.gz = stocks_daily_2005.parquet sparad som csv; csv.gz-filen i data/raw är trasig)
# Steg 0: datakedjan (T13 återskapat). Steg 1: styrka (bara N, G, SE, MDE). Steg 2: skattningar för test som klarat steg 1.
import os, sys, json
STEP = int(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['OUT'] = os.environ.get('R6OUT', os.path.join(HERE, 'runda6_resultat'))
src = open(os.path.join(HERE, 'runda3.py')).read()
exec(src.split('# %%\nrng = np.random')[0])          # gemensam uppsättning från runda 3: panel, kalender, regel, medlemmar
OUT = os.environ['OUT']; os.makedirs(OUT, exist_ok=True)

# ---------- inferens (som runda 2-4)
rng = np.random.default_rng(20261102)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
def wcr(X, y, g, j=0, B=9999, boot=True):
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    keep = X.std(0) > 0; keep[j] = True; X = X[:, keep]; j = int(keep[:j].sum())
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    if G < 3 or n <= k: return dict(b=np.nan, se=np.nan, lo=np.nan, hi=np.nan, p=np.nan, n=n, G=G)
    XtXi = np.linalg.pinv(X.T @ X); q = X @ XtXi[j]; adj = G / (G - 1) * (n - 1) / (n - k); Am = XtXi @ X.T
    def bse(Y):
        Bm = Y @ Am.T; E = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in E * q])
        return Bm[:, j], np.sqrt((sg ** 2).sum(1) * adj)
    b0, s0 = bse(y[None, :]); b0, s0 = b0[0], s0[0]; qq = tdist.ppf(.975, G - 1); p = np.nan
    if boot:
        Xr = np.delete(X, j, 1); fr = Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]; er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, G); bs, ss = bse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = (np.abs(np.concatenate(ts)[:B]) >= abs(b0 / s0)).mean()
    return dict(b=b0, se=s0, lo=b0 - qq * s0, hi=b0 + qq * s0, p=p, n=n, G=G)
def reg(s, x, y, ctrl, fe='review', boot=True):
    FE = pd.get_dummies(s[fe]).astype(float).values
    X = np.column_stack([np.asarray(s[x], float)] + [np.asarray(s[c], float) for c in ctrl] + [FE])
    return wcr(X, np.asarray(s[y], float), s.review.values, 0, boot=boot)
def mde(r): return (tdist.ppf(.975, r['G'] - 1) + tdist.ppf(.80, r['G'] - 1)) * r['se']
fmt = lambda r: f"{r['b']:+.3f} ({r['lo']:+.3f} till {r['hi']:+.3f}), p {r['p']:.3f}, N {r['n']}, G {r['G']}"
LV = np.log(VOL.where(VOL > 0)).values
def ablogvol(c, iA):
    if c not in CI or iA - 120 < 0: return np.nan
    j = CI[c]; pre = LV[iA - 10:iA, j]; base = LV[iA - 120:iA - 20, j]
    if np.isfinite(pre).sum() < 5 or np.isfinite(base).sum() < 50: return np.nan
    return np.nanmean(pre) - np.nanmean(base)

# ---------- T19-urvalet: samma konstruktion som T13 (runda3.py), fler fönster
UTDRAG = bool(os.environ.get('UTDRAG'))   # utdraget (186 aktier) täcker alla tillägg men bara 35 % av de icke tillagda: då körs T19a/c/d och T20, inte T19b
SUF = '_utdrag' if UTDRAG else ''
CACHE = os.path.join(OUT, f'T19_urval{SUF}.csv')
if UTDRAG and (STEP == 0 or not os.path.exists(CACHE)):
    # tilläggen med regelflagga, uppgång och storlek exakt som i T13 (runda3_resultat/T13_events.csv), fönstren räknas om här
    T13e = pd.read_csv(os.path.join(HERE, 'runda3_resultat', 'T13_events.csv')); T13e = T13e[T13e.event == 1]
    evk = ev[ev.type == 'addition'].drop_duplicates(['RIC', 'review_cycle']).set_index(['RIC', 'review_cycle'])
    rows = []
    for x in T13e.itertuples():
        e = evk.loc[(x.ric, x.review)]; iA, iE = int(e.iAD), int(e.iED)
        rows.append(dict(review=x.review, post=x.post, event=1, ric=x.ric, ru=x.ru, lm=x.lm, ltv=x.ltv, regel_vald=int(x.regel_vald), cum=x.cum,
                         car_c1=wsum(x.ric, iA - 1, iE + 1), car_c1_runda3=x._8, ann=wsum(x.ric, iA, iA + 1), annED=wsum(x.ric, iA, iE + 1),
                         pre20=wsum(x.ric, iA - 20, iA - 1), ru_lag=wsum(x.ric, iA - 100, iA - 21), abvol=ablogvol(x.ric, iA)))
    pd.DataFrame(rows).to_csv(CACHE, index=False)
elif STEP == 0 or not os.path.exists(CACHE):
    FL = pd.read_csv(P('output/omxsb_replication_2007/mechanisms/step1_deletion_flags.csv'))
    FLAGGED = set(FL[FL.flagged.astype(bool)].RIC)
    FFH = pd.read_csv(os.path.join(IND, 'lseg_freefloat_hist.csv'))
    ffh = {(r.review, r.ric): r.ff for r in FFH.dropna(subset=['ff']).itertuples()}
    ICB = {r: str(int(v)) for r, v in zip(K.ric, K.icb) if pd.notna(v)}
    TRBC = {r: str(v) for r, v in zip(K.ric, K.trbc) if pd.notna(v)}
    FFC = dict(zip(K.ric, pd.to_numeric(K.freefloat, errors='coerce')))
    REFS = {'2007H2': '2007-05-31', '2008H1': '2007-11-30', '2008H2': '2008-05-30', '2009JAN': '2008-11-28'}
    for c, e in zip(rev.review_cycle, rev.ED):
        if c not in REFS:
            m_ = {6: 4, 12: 10, 7: 5, 1: 11}[e.month]; y_ = e.year - (1 if e.month == 1 else 0)
            REFS[c] = str(cal[(cal.year == y_) & (cal.month == m_)].max().date())
    rows = []
    for k, r in rev.iterrows():
        if k == 0: continue
        iA, iE = int(r.iAD), int(r.iED); ref = pd.Timestamp(REFS[r.review_cycle]); ir = int(pos[ref]) if ref in pos.index else nextpos(ref)
        start = nextpos(ref - pd.DateOffset(months=6))
        cl = CLOSE.iloc[ir]; U = [c for c in RICS if pd.notna(cl.get(c)) and not not_main(c)]
        if len(U) < 50: continue
        tvv = pd.Series({c: (np.nansum(TV[c].values[start:ir + 1]) if c in TV else np.nan) for c in U})
        shr = SH.iloc[max(ir - 5, 0):ir + 1].ffill().iloc[-1]
        # Rättelse 2 nov cirka 18:20: kursen i panelen är justerad för senare splittar, aktieantalet är historiskt, så kurs × aktier blir fel.
        # Nu: bolagets mcap (ojusterat) × aktieslagets andel av aktierna i bolagets noterade aktieslag samma dag. Gamla raden:
        # cm = pd.Series({c: (cl[c] * shr[c]) if pd.notna(shr.get(c)) and shr.get(c) > 0 else (mc[c].iloc[ir] if c in mc else np.nan) for c in U})
        ROOTS_ = {}
        for c_ in U: ROOTS_.setdefault(root(c_), []).append(c_)
        def klassvarde(c):
            b_ = mc[c].iloc[ir] if c in mc else np.nan
            if not (b_ > 0): return np.nan
            sy = ROOTS_[root(c)]
            if len(sy) == 1: return b_
            s_ = [shr.get(o) for o in sy]
            return b_ * shr.get(c) / sum(s_) if all(pd.notna(v) and v > 0 for v in s_) else np.nan
        cm = pd.Series({c: klassvarde(c) for c in U})
        ff = pd.Series({c: ffh.get((r.review_cycle, c), FFC.get(c, np.nan)) for c in U}); ff = ff.where((ff > 0) & (ff <= 100))
        D = pd.DataFrame(dict(tv=tvv, ffm=cm * (ff.fillna(100) / 100))).dropna(); D = D[D.ffm > 0]
        D['sect'] = [ICB.get(c, 'trbc:' + TRBC[c] if c in TRBC else 'okänd') for c in D.index]
        ntop = max(int(np.ceil(0.10 * len(D))), 25)
        D['top'] = D.tv.rank(ascending=False) <= ntop; D['bottom'] = D.tv.rank(ascending=False, pct=True) > 0.70
        D = D.sort_values('ffm', ascending=False)
        D['w'] = D.ffm / D.groupby('sect').ffm.transform('sum'); D['cum'] = D.groupby('sect').ffm.cumsum() / D.groupby('sect').ffm.transform('sum')
        D['sel'] = (D.top | ((D.cum - D.w) < 0.85)) & ~D.bottom
        before = MED.get(cyc[k - 1], set()); unsure = OSA.get(cyc[k - 1], set())
        evs = ev[ev.k == k]; adds = set(evs[evs.type == 'addition'].RIC); ev_stems = set(stem(x) for x in evs.RIC)
        near = D[(~D.index.isin(list(before))) & (~D.index.isin(list(adds))) & (~D.bottom) & (D.sel | (D.cum <= 0.95))]
        dels = [d_ for d_ in set(evs[evs.type == 'deletion'].RIC) if d_ in D.index and d_ not in FLAGGED]
        for d_ in dels:   # T19e: borttag, förutsägbart om regeln inte valde aktien
            ru = wsum(d_, iA - 100, iA - 1); m = mc[d_].iloc[iA - 1] if d_ in mc else np.nan
            if np.isnan(ru) or not (m > 0): continue
            rows.append(dict(review=r.review_cycle, post=int(r.AD.year >= 2017), event=1, typ='deletion', ric=d_, ru=ru, lm=np.log(m), ltv=np.log1p(D.loc[d_, 'tv']),
                             regel_vald=int(bool(D.loc[d_, 'sel'])), cum=float(D.loc[d_, 'cum']), car_c1=wsum(d_, iA - 1, iE + 1), ann=wsum(d_, iA, iA + 1)))
        for flag, idx in [(1, [a for a in adds if a in D.index]), (0, list(near.index))]:
            for c in idx:
                if flag == 0 and (any((c, kk) in has_ev for kk in (k - 1, k, k + 1)) or stem(c) in ev_stems or c in unsure): continue
                ru = wsum(c, iA - 100, iA - 1); m = mc[c].iloc[iA - 1] if c in mc else np.nan
                c1 = wsum(c, iA - 1, iE + 1)
                if np.isnan(ru) or np.isnan(c1) or not (m > 0): continue
                rows.append(dict(review=r.review_cycle, post=int(r.AD.year >= 2017), event=flag, typ='addition' if flag else 'near', ric=c, ru=ru, lm=np.log(m), ltv=np.log1p(D.loc[c, 'tv']),
                                 regel_vald=int(bool(D.loc[c, 'sel'])), cum=float(D.loc[c, 'cum']),
                                 car_c1=c1, ann=wsum(c, iA, iA + 1), annED=wsum(c, iA, iE + 1),
                                 pre20=wsum(c, iA - 20, iA - 1), ru_lag=wsum(c, iA - 100, iA - 21), abvol=ablogvol(c, iA)))
    T = pd.DataFrame(rows); T.to_csv(CACHE, index=False)
T = pd.read_csv(CACHE)
if 'typ' in T:
    TE = T[T.typ != 'near'].copy(); sg = np.where(TE.typ == 'deletion', -1, 1)
    TE['ann_s'] = sg * TE.ann; TE['ru_s'] = sg * TE.ru
    TE['forutsagbar'] = np.where(TE.typ == 'deletion', 1 - TE.regel_vald, TE.regel_vald); TE['rt'] = TE.review + '_' + TE.typ
    T = T[T.typ != 'deletion'].copy()

# ---------- T20-urvalet: nettoköp per händelse 2019-2026
NK = pd.read_csv(os.path.join(HERE, 'nettokop_events.csv')); NK = NK[NK.status == 'ok'].copy()
evm = ev.set_index(['RIC', 'review_cycle'])
def t20row(x):
    e = evm.loc[(x.RIC, x.review)]; e = e.iloc[0] if isinstance(e, pd.DataFrame) else e
    iA = int(e.iAD); sign = 1 if x.type == 'addition' else -1
    m = mc[x.RIC].iloc[iA - 1] if x.RIC in mc else np.nan
    sh = SH[x.RIC].iloc[max(iA - 5, 0):iA].ffill().iloc[-1] if x.RIC in SH else np.nan
    adv = np.nanmean(VOL[x.RIC].values[iA - 120:iA - 20]) if x.RIC in VOL else np.nan
    d = sign * x.netto_alla_index
    return dict(car=e.tot_gi, ru=wsum(x.RIC, iA - 100, iA - 1), lm=np.log(m) if m > 0 else np.nan, d=d,
                d_omxsb=sign * x.netto_OMXSB, d_dagar=d / 100 * sh / adv if (adv > 0 and sh > 0) else np.nan)
T20 = pd.concat([NK.reset_index(drop=True), pd.DataFrame([t20row(x) for x in NK.itertuples()])], axis=1)
T20['rt'] = T20.review + '_' + T20.type
T20.to_csv(os.path.join(OUT, f'T20_urval{SUF}.csv'), index=False)

C19 = ['ru', 'lm']
TESTS = {   # namn: (urval, testvariabel, utfall, kontroller, fe, villkor för MDE)
    'T19a': (lambda t: t[t.event == 1], 'regel_vald', 'ann', C19, 'review', 1.5),
    'T19b': (lambda t: t[t.event == 0], 'regel_vald', 'ann', C19, 'review', 0.5),
    'T20': (lambda t: t, 'd', 'car', C19, 'rt', 1.8),
}
SEC = {
    'T19a före 2017': (lambda t: t[(t.event == 1) & (t.post == 0)], 'regel_vald', 'ann', C19, 'review'),
    'T19a efter 2017': (lambda t: t[(t.event == 1) & (t.post == 1)], 'regel_vald', 'ann', C19, 'review'),
    'T19b före 2017': (lambda t: t[(t.event == 0) & (t.post == 0)], 'regel_vald', 'ann', C19, 'review'),
    'T19b efter 2017': (lambda t: t[(t.event == 0) & (t.post == 1)], 'regel_vald', 'ann', C19, 'review'),
    'T19a [AD, ED+1]': (lambda t: t[t.event == 1], 'regel_vald', 'annED', C19, 'review'),
    'T19c [AD-20, AD-1]': (lambda t: t[t.event == 1], 'regel_vald', 'pre20', ['ru_lag', 'lm'], 'review'),
    'T19d volym [AD-10, AD-1]': (lambda t: t[t.event == 1], 'regel_vald', 'abvol', C19, 'review'),
    'T20 dagars omsättning': (lambda t: t, 'd_dagar', 'car', C19, 'rt'),
    'T20 bara OMXSB-familjen': (lambda t: t, 'd_omxsb', 'car', C19, 'rt'),
    'T20 bara tillägg': (lambda t: t[t.type == 'addition'], 'd', 'car', C19, 'rt'),
    'T20 bara borttag': (lambda t: t[t.type == 'deletion'], 'd', 'car', C19, 'rt'),
}
if not UTDRAG: TESTS['T19e'] = (lambda t: t, 'forutsagbar', 'ann_s', ['ru_s', 'lm'], 'rt', 1.5)
DATA = lambda name: T20 if name.startswith('T20') else (TE if name.startswith('T19e') else T)

if UTDRAG:
    for k in [k for k in TESTS if k == 'T19b']: TESTS.pop(k)
    for k in [k for k in SEC if k.startswith('T19b')]: SEC.pop(k)
if STEP == 0 and UTDRAG:
    dd = (T.car_c1 - T.car_c1_runda3).abs()
    print('Utdraget: CAR [AD-1, ED+1] för tilläggen mot runda 3:', len(T), 'tillägg, saknas', int(T.car_c1.isna().sum()), ', största avvikelse', round(dd.max(), 4))
    ok = (dd.max() < 0.01) and T.car_c1.notna().all()
    for c in ['ann', 'pre20', 'ru_lag', 'abvol']: print(f'  {c}: {int(T[c].notna().sum())} av {len(T)} med värde')
    print('Steg 0 (utdrag)', 'GODKÄNT' if ok else 'STOPP')
    json.dump(dict(passed=bool(ok), n=len(T), maxdiff=float(dd.max())), open(os.path.join(OUT, 'steg0_utdrag.json'), 'w'), indent=1)
    sys.exit()
if not UTDRAG:
    for k in ['T19a', 'T20']: TESTS.pop(k)   # stoppade i steg 1 i utdragsläget (steg1_utdrag.json)
    for k in [k for k in SEC if not k.startswith('T19b')]: SEC.pop(k)
if STEP == 0:
    s = T[T.post == 1]; r = reg(s, 'event', 'car_c1', ['ru', 'lm', 'ltv'])
    print('T13 återskapat (efter 2017):', fmt(r), '| känt: +1,701, N 985, G 19')
    ok = abs(r['b'] - 1.7013) <= 0.05 and r['n'] == 985
    print('Steg 0', 'GODKÄNT' if ok else 'STOPP')
    json.dump(dict(passed=bool(ok), **{k: float(v) for k, v in r.items()}), open(os.path.join(OUT, 'steg0.json'), 'w'), indent=1)
    sys.exit()

if STEP == 1:
    res = {}
    for name, (f, x, y, c, fe, lim) in TESTS.items():
        s = f(DATA(name)).dropna(subset=[x, y] + c); r = reg(s, x, y, c, fe, boot=False)
        res[name] = dict(n=int(r['n']), G=int(r['G']), se=float(r['se']), mde=float(mde(r)), villkor=lim, godkant=bool(mde(r) <= lim),
                         n_testvariabel_1=int((s[x] == 1).sum()) if name.startswith('T19') else None)
        print(f"{name}: N {r['n']}, G {r['G']}, SE {r['se']:.3f}, MDE {mde(r):.3f} (villkor ≤ {lim}) ->", 'GODKÄNT' if mde(r) <= lim else 'STOPP')
    json.dump(res, open(os.path.join(OUT, f'steg1{SUF}.json'), 'w'), indent=1, ensure_ascii=False)
    sys.exit()

if STEP == 2:
    st1 = json.load(open(os.path.join(OUT, f'steg1{SUF}.json'))); out = []
    for name, (f, x, y, c, fe, lim) in TESTS.items():
        if not st1[name]['godkant']: print(name, 'stoppad i steg 1, skattas inte'); continue
        s = f(DATA(name)).dropna(subset=[x, y] + c); r = reg(s, x, y, c, fe)
        out.append(dict(test=name, typ='primär', **r, mde=mde(r))); print(f'{name} (primär):', fmt(r), f'MDE {mde(r):.2f}')
    for name, (f, x, y, c, fe) in SEC.items():
        base = 'T19b' if name.startswith('T19b') else ('T20' if name.startswith('T20') else 'T19a')   # sekundära följer sitt primära test
        if base in st1 and not st1[base]['godkant']: continue
        s = f(DATA(name)).dropna(subset=[x, y] + c); r = reg(s, x, y, c, fe)
        out.append(dict(test=name, typ='sekundär', **r, mde=mde(r))); print(f'{name}:', fmt(r), f'MDE {mde(r):.2f}')
    # beskrivande medel, ingen inferens
    d = []
    for (pv, ev_, rv), g in T.groupby(['post', 'event', 'regel_vald']):
        d.append(dict(period='efter 2017' if pv else 'före 2017', grupp='tillägg' if ev_ else 'ej tillagd', regel_vald=rv, n=len(g),
                      ann=g.ann.mean(), pre20=g.pre20.mean(), annED=g.annED.mean()))
    D_ = pd.DataFrame(d); D_.to_csv(os.path.join(OUT, f'T19_medel{SUF}.csv'), index=False); print(D_.round(2).to_string(index=False))
    pd.DataFrame(out).to_csv(os.path.join(OUT, f'runda6_results{SUF}.csv'), index=False)
