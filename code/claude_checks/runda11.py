# Runda 11: Greenwood och Sammon (2025) fullt ut, med multiplikatorn M. Deklarerat i runda11_deklaration.md (2 nov 2026, 19:23).
# Körs från code/claude_checks:
#   ROOT=../.. PANEL=../../runda2_indata/panel_full.csv.gz INDATA=code/claude_checks/data python3 runda11.py 0|1|2
# Steg 0: datakedja (inga utfall visas). Steg 1: styrka (N, G, SE, MDE). Steg 2: alla skattningar och tabeller.
import os, sys, json
STEP = int(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['OUT'] = os.path.join(HERE, 'runda11_resultat')
exec(open(os.path.join(HERE, 'runda3.py')).read().split('# %%\nrng = np.random')[0])   # panel, kalender, wsum, medlemmar, händelser
OUT = os.path.join(HERE, 'runda11_resultat'); os.makedirs(OUT, exist_ok=True)
PER = lambda y: '2007–11' if y <= 2011 else ('2012–16' if y <= 2016 else ('2017–21' if y <= 2021 else '2022–26'))
PERS = ['2007–11', '2012–16', '2017–21', '2022–26']

# ---------- inferens: linjär kombination c'b, klustrat, restriktiv wild cluster bootstrap
rng = np.random.default_rng(20261102)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
def lin(X, y, g, c, B=9999, boot=True):
    X = np.asarray(X, float); y = np.asarray(y, float); c = np.asarray(c, float)
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    if G < 3 or n <= k: return dict(b=np.nan, se=np.nan, lo=np.nan, hi=np.nan, p=np.nan, n=n, G=G)
    XtXi = np.linalg.pinv(X.T @ X); Am = XtXi @ X.T; q = X @ (XtXi @ c); adj = G / (G - 1) * (n - 1) / max(n - k, 1)
    def tse(Y):
        Bm = Y @ Am.T; E = Y - Bm @ X.T
        sg = np.stack([np.bincount(codes, weights=row, minlength=G) for row in E * q])
        return Bm @ c, np.sqrt((sg ** 2).sum(1) * adj)
    t0, s0 = tse(y[None, :]); t0, s0 = t0[0], s0[0]; qq = tdist.ppf(.975, G - 1); p = np.nan
    if boot:
        b = Am @ y; br = b - XtXi @ c * (c @ b) / (c @ XtXi @ c); fr = X @ br; er = y - fr; ts = []
        for _ in range(B // 1000 + 1):
            W = wdraw(1000, G); bs, ss = tse(fr[None, :] + er[None, :] * W[:, codes]); ts.append(bs / ss)
        p = float((np.abs(np.concatenate(ts)[:B]) >= abs(t0 / s0)).mean())
    return dict(b=float(t0), se=float(s0), lo=float(t0 - qq * s0), hi=float(t0 + qq * s0), p=p, n=int(n), G=int(G))
def mde(r): return (tdist.ppf(.975, r['G'] - 1) + tdist.ppf(.80, r['G'] - 1)) * r['se']
def medel(s, col, boot=False): return lin(np.ones((len(s), 1)), s[col].values, s.review.values, [1.0], boot=boot)

# ---------- hjälp: aktieslagets börsvärde (6c), senare splittar
ROOTS = {}
for c_ in CLOSE.columns: ROOTS.setdefault(root(c_), []).append(c_)
def har_kurs(o, i): return o in CLOSE and pd.notna(CLOSE[o].iloc[max(i - 5, 0):i + 1]).any()
def sh_at(o, i, lb=60):
    if o not in SH: return np.nan
    s = SH[o].iloc[max(i - lb, 0):i + 1].dropna(); return float(s.iloc[-1]) if len(s) and s.iloc[-1] > 0 else np.nan
def klassvarde(c, i):
    if not har_kurs(c, i): return np.nan
    b = mc[c].iloc[i] if c in mc else np.nan
    if not (b > 0): return np.nan
    sy = [o for o in ROOTS.get(root(c), [c]) if har_kurs(o, i)]
    if len(sy) == 1: return float(b)
    s = [sh_at(o, i) for o in sy]
    return float(b * sh_at(c, i) / sum(s)) if all(v > 0 for v in s) else np.nan
def faktor(c, i):   # ojusterat pris / justerat pris
    if not har_kurs(c, i) or c not in mc: return np.nan
    b = mc[c].iloc[max(i - 10, 0):i + 1].dropna()
    if b.empty: return np.nan
    sy = [o for o in ROOTS.get(root(c), [c]) if har_kurs(o, i)]
    s = [sh_at(o, i, 10) for o in sy]
    cl = CLOSE[c].iloc[max(i - 10, 0):i + 1].dropna()
    if not all(v > 0 for v in s) or cl.empty: return np.nan
    return float(b.iloc[-1] / sum(s) / cl.iloc[-1])

# ---------- händelser
FL = pd.read_csv(P('output/omxsb_replication_2007/mechanisms/step1_deletion_flags.csv')); FLAGGED = set(FL[FL.flagged.astype(bool)].event_id)
E = ev.dropna(subset=['iAD', 'iED']).copy(); E = E[~E.event_id.isin(FLAGGED)].copy()
E['iA'] = E.iAD.astype(int); E['iE'] = E.iED.astype(int); E['ar'] = E.AD.dt.year; E['per'] = E.ar.map(PER); E['review'] = E.review_cycle
E['s'] = np.where(E.type == 'addition', 1.0, -1.0)
E['car_tot'] = [wsum(r, a - 1, b + 1) for r, a, b in zip(E.RIC, E.iA, E.iE)]
E['car_lang'] = [wsum(r, a - 20, b + 1) for r, a, b in zip(E.RIC, E.iA, E.iE)]
for n_ in [10, 20, 50, 100]: E[f'pre{n_}'] = [wsum(r, a - n_, a - 1) for r, a in zip(E.RIC, E.iA)]
E['y_tot'] = E.s * E.car_tot; E['y_lang'] = E.s * E.car_lang
# senare splittar
last_i = {c: int(pos[CLOSE[c].last_valid_index()]) for c in set(E.RIC) if c in CLOSE and CLOSE[c].last_valid_index() is not None}
E['kv'] = [faktor(r, e) / faktor(r, last_i[r]) if r in last_i else np.nan for r, e in zip(E.RIC, E.iE)]
E['split'] = ~E.kv.between(1 / 1.4, 1.4)   # NaN räknas som flaggad
# D och fondgrupper ur LSEG (regeln från runda 9)
ns = {'__file__': os.path.join(HERE, 'runda9.py')}; os.environ.setdefault('DATA', os.path.join(HERE, 'data'))
argv0 = sys.argv[:]; sys.argv = ['runda9.py', '9']
exec(open(os.path.join(HERE, 'runda9.py')).read().split('NT = netto(F)')[0], ns); sys.argv = argv0
F9 = ns['F']; NT = ns['netto'](F9)
GR = ['OMXSB-index', 'OMXSB-blandfond', 'OMXS30', 'småbolagsindex', 'övriga passiva, svenska', 'övriga passiva, utländska', 'ej passiv']
E['sh_ed'] = [sh_at(r, e, 250) for r, e in zip(E.RIC, E.iE)]
E['fonddata'] = E.event_id.isin(set(F9.event_id))
for g_ in GR:
    v = NT[g_] if g_ in NT else pd.Series(dtype=float)
    E['n_' + g_] = [s_ * 100 * v.get(e_, 0.0) / sh if sh > 0 else np.nan for s_, e_, sh in zip(E.s, E.event_id, E.sh_ed)]
E['D'] = E['n_OMXSB-index']; E['passiva_ovriga'] = E[['n_' + g for g in GR[1:6]]].sum(1, min_count=1); E['aktiva'] = E['n_ej passiv']
E['alla_fonder'] = E[['n_' + g for g in GR]].sum(1, min_count=1)
# kontroller (G&S tabell 2)
MAIN = [c for c in TV.columns if not not_main(c)]
mcr = mc[[c for c in MAIN if c in mc]].T.groupby(lambda c: root(c)).max().T   # ett mcap per bolag
mkt_turn = TV[MAIN].sum(1, min_count=1) / mcr.sum(1, min_count=1) * 100
def abn_turn(c, i):
    v = klassvarde(c, i - 1)
    if not (v > 0) or c not in TV: return np.nan
    frac = v / mc[c].iloc[i - 1]
    t = TV[c].iloc[i - 21:i] / (mc[c].iloc[i - 21:i] * frac) * 100
    m = mkt_turn.iloc[i - 21:i]; ok = t.notna() & m.notna()
    return float(t[ok].mean() - m[ok].mean()) if ok.sum() >= 10 else np.nan
def wz(c, i):
    if c not in RET: return np.nan
    r = RET[c].iloc[i - 250:i - 1]; m = mkt.iloc[i - 250:i - 1]; ok = r.notna() & m.notna()
    if ok.sum() < 100: return np.nan
    b = np.polyfit(m[ok].values, r[ok].values, 1); return float(np.var(r[ok].values - np.polyval(b, m[ok].values), ddof=2))
A8 = pd.read_csv(os.path.join(HERE, 'data', 'runda8_analytiker.csv.gz'), low_memory=False)
va = [c for c in A8.columns if 'Number of Included Estimates' in c][0]
A8['m'] = pd.to_datetime(A8.Date, errors='coerce').dt.to_period('M'); har_a = set(A8[A8[va].notna()].Instrument)
NA = A8.dropna(subset=['m']).groupby(['Instrument', 'm'])[va].max()
def analytiker(c, d):
    if c not in har_a: return np.nan
    v = NA.get((c, pd.Period(d, 'M') - 1), np.nan); return 0.0 if pd.isna(v) else float(v)
storlek = []
for x in E.itertuples():
    k = int(x.k); mem = MED.get(cyc[k - 1], set()) if k > 0 else MED.get(cyc[k], set())
    tot = np.nansum([klassvarde(c, x.iA - 1) for c in mem]); v = klassvarde(x.RIC, x.iA - 1)
    storlek.append(100 * v / tot if tot > 0 and v > 0 else np.nan)
E['k_oms'] = [abn_turn(r, a) for r, a in zip(E.RIC, E.iA)]; E['k_storlek'] = storlek
E['k_wz'] = [wz(r, a) for r, a in zip(E.RIC, E.iA)]; E['k_ana'] = [analytiker(r, d) for r, d in zip(E.RIC, E.AD)]
KC = ['k_oms', 'k_storlek', 'k_wz', 'k_ana']
E.to_csv(os.path.join(OUT, 'handelser.csv'), index=False)

def urval(ty, prim=True, krav_D=True):
    s = E[E.type == ty].copy()
    if krav_D: s = s[s.D.notna() & s.fonddata]
    if prim: s = s[~s.split]
    return s
def demean(s, cols):
    s = s.dropna(subset=cols).copy()
    for c in cols: s[c] = s[c] - s[c].mean()
    return s

if STEP == 0:
    print('händelser:', len(E), E.type.value_counts().to_dict(), '| flaggade borttag uteslutna:', len(FLAGGED))
    print('CAR saknas: totalt', int(E.car_tot.isna().sum()), 'långt', int(E.car_lang.isna().sum()))
    print('med fonddata:', int(E.fonddata.sum()), '| D saknas (aktieantal):', int(E.D.isna().sum()))
    print('senare split eller okänd faktor:', E.groupby('type').split.sum().to_dict(), 'av', E.type.value_counts().to_dict(), '| okänd faktor:', int(E.kv.isna().sum()))
    for c in KC: print(f'  kontroll {c}: {int(E[c].notna().sum())} av {len(E)}')
    # spärr: T24:s medel-D per period (medel per översyn), tillägg, alla händelser, samma urval som runda 9
    T24 = pd.read_csv(os.path.join(HERE, 'runda9_resultat', 'T24_resultat.csv')); T24 = T24[(T24.typ == 'addition') & (T24['mått'] == 'OMXSB-index')].set_index('period').nettokop
    a = E[(E.type == 'addition') & E.D.notna() & E.car_tot.notna()]
    ny = a.groupby(['per', 'review']).D.mean().groupby('per').mean()
    dd = (ny.reindex(T24.index) - T24).abs()
    print('T24 medel-D per period:', T24.round(3).to_dict()); print('ny kedja:            ', ny.round(3).to_dict()); print('största avvikelse:', round(dd.max(), 4))
    ok = bool(dd.max() <= 0.03); print('Steg 0', 'GODKÄNT' if ok else 'STOPP')
    json.dump(dict(passed=ok, maxdiff=float(dd.max()), t24=T24.to_dict(), ny=ny.to_dict()), open(os.path.join(OUT, 'steg0.json'), 'w'), indent=1, ensure_ascii=False)
    sys.exit()

def tab6(ty, yc, kontroller, prim=True):
    s = urval(ty, prim); s = s[s[yc].notna()]
    if kontroller: s = demean(s, KC)
    Db = s.groupby('per').D.mean().reindex(PERS)
    X = np.column_stack([((s.per == p_).astype(float) * Db[p_]).values for p_ in PERS] + ([s[c].values for c in KC] if kontroller else []))
    return s, Db, X

if STEP == 1:
    res = {}
    for namn, yc in [('H11a', 'y_tot'), ('H11b', 'y_lang')]:
        s, Db, X = tab6('addition', yc, True); c = np.zeros(X.shape[1]); c[0], c[3] = 1, -1
        r = lin(X, s[yc].values, s.review.values, c, boot=False); res[namn] = dict(n=r['n'], G=r['G'], se=r['se'], mde=float(mde(r)), D_per=Db.round(3).to_dict())
        print(f"{namn} (M_2007–11 − M_2022–26, tillägg, kontroller): N {r['n']}, G {r['G']}, SE {r['se']:.2f}, MDE {mde(r):.2f}")
    s = urval('addition'); s = s[s.ar >= 2017]; r = medel(s, 'aktiva'); res['H11c'] = dict(n=r['n'], G=r['G'], se=r['se'], mde=float(mde(r)))
    print(f"H11c (aktiva fonder, tillägg 2017–26): N {r['n']}, G {r['G']}, SE {r['se']:.3f}, MDE {mde(r):.3f}")
    for ty in ['addition', 'deletion']:
        for fr in [2007, 2017]:
            s = demean(urval(ty), KC); s = s[(s.ar >= fr) & s.y_tot.notna()]
            FE = pd.get_dummies(s.review).astype(float).values
            X = np.column_stack([s.D.values] + [s[c].values for c in KC] + [FE]); c = np.zeros(X.shape[1]); c[0] = 1
            r = lin(X, s.y_tot.values, s.review.values, c, boot=False)
            res[f'T30 {ty} från {fr}'] = dict(n=r['n'], G=r['G'], se=r['se'], mde=float(mde(r)), villkor=2.0, godkant=bool(mde(r) <= 2.0))
            print(f"T30 {ty} från {fr}: N {r['n']}, G {r['G']}, SE {r['se']:.2f}, MDE {mde(r):.2f} (villkor ≤ 2) ->", 'GODKÄNT' if mde(r) <= 2 else 'bara lutning')
    json.dump(res, open(os.path.join(OUT, 'steg1.json'), 'w'), indent=1, ensure_ascii=False)
    sys.exit()

if STEP == 2:
    st1 = json.load(open(os.path.join(OUT, 'steg1.json'))); rader = []
    def rec(test, **kw): rader.append(dict(test=test, **kw))
    # A. Tabell 2
    for ty in ['addition', 'deletion']:
        for kontroller in [False, True]:
            s = E[(E.type == ty) & E.car_tot.notna()]
            if kontroller: s = demean(s, KC)
            X = np.column_stack([(s.per == p_).astype(float).values for p_ in PERS] + ([s[c].values for c in KC] if kontroller else []))
            for j, p_ in enumerate(PERS):
                c = np.zeros(X.shape[1]); c[j] = 1; r = lin(X, s.car_tot.values, s.review.values, c, boot=False); rec('A tabell 2', typ=ty, kontroller=kontroller, del_=p_, **r)
            c = np.zeros(X.shape[1]); c[0], c[3] = 1, -1; r = lin(X, s.car_tot.values, s.review.values, c); rec('A tabell 2', typ=ty, kontroller=kontroller, del_='2007–11 minus 2022–26', **r)
            if kontroller:
                for j, kc in enumerate(KC):
                    c = np.zeros(X.shape[1]); c[4 + j] = 1; r = lin(X, s.car_tot.values, s.review.values, c); rec('A tabell 2', typ=ty, kontroller=True, del_=kc, **r)
    # B. Tabell 4
    for ty in ['addition', 'deletion']:
        for p_ in PERS:
            for n_ in [10, 20, 50, 100]:
                s = E[(E.type == ty) & (E.per == p_) & E[f'pre{n_}'].notna()]; r = medel(s, f'pre{n_}'); rec('B tabell 4', typ=ty, del_=f'{p_} [AD−{n_}, AD−1]', **r)
    # C. Tabell 5
    for prim in [True, False]:
        for ty in ['addition', 'deletion']:
            for yc in ['y_tot', 'y_lang']:
                s0 = urval(ty, prim)
                for p_ in PERS:
                    d = s0[(s0.per == p_) & s0[yc].notna()]
                    if d.empty: continue
                    M = d[yc].mean() / d.D.mean() if d.D.mean() > 0 else np.nan
                    rv = d.review.values; u = np.unique(rv); idx = {k: np.where(rv == k)[0] for k in u}; ks = []
                    for _ in range(9999):
                        ii = np.concatenate([idx[k] for k in rng.choice(u, len(u))]); dm = d.D.values[ii].mean(); ks.append(d[yc].values[ii].mean() / dm if dm > 0 else np.nan)
                    rec('C tabell 5', typ=ty, primar=prim, fonster=yc, del_=p_, n=len(d), G=len(u), car=d[yc].mean(), D=d.D.mean(), M=M,
                        lo=np.nanpercentile(ks, 2.5), hi=np.nanpercentile(ks, 97.5), elasticitet=-1 / M if M and M != 0 else np.nan)
    # D. Tabell 6 och H11a, H11b
    for ty in ['addition', 'deletion']:
        for yc in ['y_tot', 'y_lang']:
            for kontroller in [False, True]:
                s, Db, X = tab6(ty, yc, kontroller)
                for j, p_ in enumerate(PERS):
                    c = np.zeros(X.shape[1]); c[j] = 1; r = lin(X, s[yc].values, s.review.values, c, boot=False)
                    rec('D tabell 6', typ=ty, fonster=yc, kontroller=kontroller, del_=f'M {p_}', D_medel=Db[p_], **r)
                for (a_, b_, lab) in [(0, 3, 'M 2007–11 − M 2022–26'), (2, 3, 'M 2017–21 − M 2022–26')]:
                    c = np.zeros(X.shape[1]); c[a_], c[b_] = 1, -1; r = lin(X, s[yc].values, s.review.values, c)
                    hyp = {('addition', 'y_tot', True, 0): 'H11a', ('addition', 'y_lang', True, 0): 'H11b'}.get((ty, yc, kontroller, a_), '')
                    rec('D tabell 6', typ=ty, fonster=yc, kontroller=kontroller, del_=lab, hypotes=hyp, mde=float(mde(r)), **r)
    # E. Tabell 7 och H11c
    for prim in [True, False]:
        for ty in ['addition', 'deletion']:
            s0 = urval(ty, prim)
            for p_ in PERS + ['2017–26']:
                s = s0[s0.ar >= 2017] if p_ == '2017–26' else s0[s0.per == p_]
                for col in ['D', 'passiva_ovriga', 'aktiva', 'alla_fonder']:
                    boot = (p_ == '2017–26' and col == 'aktiva' and ty == 'addition' and prim)
                    r = medel(s, col, boot=boot); rec('E tabell 7', typ=ty, primar=prim, del_=p_, grupp=col, hypotes='H11c' if boot else '', **r)
    # F. Nyemissioner
    S5 = pd.read_csv(os.path.join(HERE, 'runda2_resultat_v2', 'T5urval_T7_T8b_events.csv')); S5 = S5[S5.type == 'addition'].copy()
    def bolagsaktier(c, i):
        sy = [o for o in ROOTS.get(root(c), [c]) if har_kurs(o, i)]
        s = [sh_at(o, i, 60) for o in sy]; return sum(s) if sy and all(v > 0 for v in s) else np.nan
    S5['dlog'] = [100 * np.log(bolagsaktier(c, b + 60) / bolagsaktier(c, a - 5)) if b + 60 < len(cal) else np.nan for c, a, b in zip(S5.ric, S5.iA, S5.iE)]
    S5['per'] = pd.to_datetime(S5.AD).dt.year.map(PER); S5 = S5.dropna(subset=['dlog'])
    S5.to_csv(os.path.join(OUT, 'F_nyemissioner_urval.csv'), index=False)
    FE = pd.get_dummies(S5.review).astype(float).values; X = np.column_stack([S5.event.values, FE]); c = np.zeros(X.shape[1]); c[0] = 1
    r = lin(X, S5.dlog.values, S5.review.values, c); rec('F nyemissioner', del_='tillägg minus nästan tillagda, 2007–26', **r)
    for p_ in PERS:
        for ev_, g in S5[S5.per == p_].groupby('event'):
            rec('F nyemissioner', del_=p_, grupp='tillägg' if ev_ else 'nästan tillagda', n=len(g), b=g.dlog.mean(), andel_over_1=(g.dlog > 1).mean(), andel_over_5=(g.dlog > 5).mean())
    # G. Figur 1 och G&S figur 5
    AUM = pd.read_csv(os.path.join(HERE, 'data', 'shof', 'tracker_aum_shof_v2.csv')).set_index('manad').inkl_xact_omxsb_mdkr
    f1 = []
    for ar, g in E[E.D.notna() & E.fonddata & ~E.split].groupby('ar'):
        rr = dict(ar=ar)
        for ty in ['addition', 'deletion']: q = g[g.type == ty]; rr[f'D_{ty}'] = q.D.mean(); rr[f'n_{ty}'] = len(q)
        sista = rev[rev.AD.dt.year == ar].iloc[-1]; mem = MED.get(sista.review_cycle, set())
        tot = np.nansum([klassvarde(c, int(sista.iAD) - 1) for c in mem]) / 1e9
        a_ = AUM.get(f'{ar}-12', AUM.iloc[-1]); rr.update(omxsb_mdkr=tot, fonder_mdkr=a_, agarandel_pct=100 * a_ / tot if tot > 0 else np.nan)
        f1.append(rr)
    pd.DataFrame(f1).to_csv(os.path.join(OUT, 'G_figur1_figur5.csv'), index=False)
    # H. Figur 3 och T30
    for ty in ['addition', 'deletion']:
        s = urval(ty); s = s[s.y_tot.notna()]
        X = np.column_stack([s.D.values, np.ones(len(s))]); r = lin(X, s.y_tot.values, s.review.values, [1, 0])
        r2 = np.corrcoef(s.D, s.y_tot)[0, 1] ** 2; rec('H figur 3', typ=ty, del_='utan kontroller, 2007–26', r2=r2, **r)
        for fr in [2007, 2017]:
            q = demean(urval(ty), KC); q = q[(q.ar >= fr) & q.y_tot.notna()]
            FE = pd.get_dummies(q.review).astype(float).values
            X = np.column_stack([q.D.values] + [q[c].values for c in KC] + [FE]); c = np.zeros(X.shape[1]); c[0] = 1
            ok = st1[f'T30 {ty} från {fr}']['godkant']; r = lin(X, q.y_tot.values, q.review.values, c, boot=ok)
            if not ok: r['p'] = np.nan
            rec('H T30', typ=ty, del_=f'fasta effekter per översyn och kontroller, från {fr}', godkant_styrka=ok, mde=float(mde(r)), **r)
    # I. Figur 7
    f7 = []
    for (ty, p_), g in E.groupby(['type', 'per']):
        for kk in range(-100, 15):
            v = [wsum(r_, a - 100, a + kk) for r_, a in zip(g.RIC, g.iA)]; f7.append(dict(typ=ty, period=p_, dag=kk, car=np.nanmean(v), n=int(np.isfinite(v).sum())))
    pd.DataFrame(f7).to_csv(os.path.join(OUT, 'I_figur7.csv'), index=False)
    R = pd.DataFrame(rader); R.to_csv(os.path.join(OUT, 'runda11_resultat.csv'), index=False)
    pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
    for t_, g in R.groupby('test', sort=False):
        print('\n==', t_); print(g.drop(columns=['test']).dropna(axis=1, how='all').round(3).to_string(index=False))
    print(pd.DataFrame(f1).round(2).to_string(index=False))
