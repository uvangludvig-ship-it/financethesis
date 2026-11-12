# Omräkning med daterad fondklassning (runda 13). Deklaration: fondklassning_omrakning_deklaration.md (4 nov 2026, 17:46:37).
# Läser data/funds/index_fund_list_with_mandates.csv och räknar om D, M (tabell 5 och 6), vem handlar (tabell 7), D per år (figur 1)
# och SHoF-ägarandelen med tre skikt: B (rena OMXSB-följare), V (B + varianter), C (V + blandfondsdelar).
# Urval: data/events/omxsb_changes_corrected_2007_2026.csv, 468 händelser. Den saknar 19 borttag som finns i effekttabellen (01):
# borttag flaggade för uppköp, fusion, nyemission i kris eller stor ändring i aktieantalet (step1_deletion_flags.csv i det gamla repot).
# 'ar' är här beskedsåret (AD), i 01 och 05 ändringsåret (ED). Ingen periodgräns påverkas; bara årsetiketterna i figur 1.
# Händelser, CAR, kontroller, urval och inferens är oförändrade från runda 11 och rättelserna 3 nov (handelser_rattade.csv).
# Körs från thesis_final: python3 code/02_fund_demand.py   (standard: fondlistan i data/funds, resultat i results/fund_demand)
#   eller: python3 code/02_fund_demand.py <mandatfil> <ignoreras> <utkatalog> [inkl_obelagda=0|1]
#   inkl_obelagda=1: rader med status "att belägga"/"att bedöma" eller skikt med ? räknas som följare (känslighet).
#   validera=1: använder runda 9:s grupp() i stället för mandatfilen; ska då reproducera handelser_rattade.csv
#               utom för fonder som byter grupp mellan rapporten före och efter (de utesluts nu enligt regel 1).
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import os, re, sys, json, zipfile, types
import numpy as np, pandas as pd
from scipy.stats import t as tdist
MAND = sys.argv[1] if len(sys.argv) > 1 else str(DATA / 'funds' / 'index_fund_list_with_mandates.csv')
OUT = sys.argv[3] if len(sys.argv) > 3 else str(RES / 'fund_demand')
INKL = len(sys.argv) > 4 and sys.argv[4] == '1'; VALID = False   # valideringsläget mot runda 9 körs bara i det gamla repot
os.makedirs(OUT, exist_ok=True)
PERS = ['2007–11', '2012–16', '2017–21', '2022–26']
LOG = []
def log(s): LOG.append(s); print(s)

# ---------- mandatfilen. nyckel = början av kolumnen fond; per nyckel: LSEG-regex, SHoF-namn, FI-regex (för blandfondernas OMXSB-andel)
ALIAS = {
    'XACT OMXSB': (r'xact sverige|xact omxsb', ['XACT Sverige (UCITS ETF)'], None),
    'Handelsbanken Sverige OMXSB Index': (r'handelsbanken sverige 100 index|handelsbanken sverige omxsb', ['Handelsbanken Sverige 100 Index Criteria'], None),
    'Länsförsäkringar Sverige Index': (r'lansforsakringar sverige index|länsförsäkringar sverige index', ['Länsförsäkringar Sverige Index'], None),
    'Nordnet': (r'nordnet sverige index|nordnet indexfond sverige|nordnet superfonden sverige', ['Nordnet Indexfond Sverige ESG'], None),
    'Nordea Indexfond Sverige': (r'nordea sverige passiv|nordea indexfond sverige', ['Nordea Indexfond Sverige'], None),
    'Swedbank Robur Access Sverige': (r'^swedbank robur access sverige', ['Swedbank Robur Access Sverige'], None),
    'iShares': (r'ishares omx stockholm', [], None),
    'Danske Invest SICAV Sverige Beta': (r'danske invest sicav sverige beta', [], None),
    'Danske Invest Index Sweden Restricted': (r'danske invest index sweden restricted', [], None),
    'Öhman Etisk Index Sverige': (r'lannebo marknad sverige bred|öhman marknad sverige bred|ohman marknad sverige bred|etisk index sverige', ['Öhman Marknad Sverige Bred'], None),
    'Öhman Marknad Sverige': (r'^lannebo marknad sverige$|^öhman marknad sverige$|^ohman marknad sverige$', ['Öhman Marknad Sverige'], None),
    'Nordea Institutionella': (r'nordea inst aktief sverige|institutionella aktiefonden sverige', ['Nordea Inst Aktie Sverige'], None),
    'SEB Sverige Indexfond': (r'^seb sverige indexfond', ['SEB Sverige Indexfond'], None),
    'SEB Sverige Indexnära': (r'seb sverige indexnara|seb sverige indexnära', ['SEB Sverige Indexnära'], None),
    'Skandia Sverige Exponering': (r'^skandia sverige exponering', ['Skandia Sverige Exponering'], None),
    'Swedbank Robur Access Mix': (r'robur access mix|robur mix indexfond sverige', ['Swedbank Robur Mix Indexfond Sverige'], r'^swedbank robur access mix$'),
    'Nordea Generationsfond': (r'nordea generationsfond', [f'Nordea Generationsfond {x}' for x in ['50-tal', '60-tal', '70-tal', '80-tal', '90-tal', 'Senior']], 'samma namn'),
    'Nordea Stiftelse': (r'nordea donationsmedel|nordea stiftelse', ['Nordea Donationsmedelsfond'], r'^nordea donationsmedelsfond$|^nordea stiftelse- och donationsmedelsfond$'),
    'KPA': (r'kpa blandfond|kpa etisk blandfond', ['KPA Blandfond'], r'^kpa etisk blandfond 2$|^kpa blandfond$'),
    'Länsförsäkringar Sparmål': (r'lansforsakringar sparmal|länsförsäkringar sparmål', [f'Länsförsäkringar Sparmål {y}' for y in range(2015, 2070, 5)], 'samma namn'),
    'Swedbank Robur Access Edge': (r'robur access edge sweden', ['Swedbank Robur Access Edge Sweden'], None),
    'SPP Aktiefond Sverige': (r'^storebrand sverige$|spp aktiefond sverige', ['Storebrand Sverige'], None),
    'GodFond': (r'godfond', [], None),
    'Nordea 2 SICAV BetaPlus': (r'betaplus.*swedish', [], None),
    'Handelsbanken Stiftelsefond': (r'^handelsbanken stiftelsefond$', [], None),
}
# grupp för fonder med mandatrad men utanför sin följarperiod (regel 5: aldrig OMXSB-följare). Övriga nycklar: namnreglerna från runda 9.
FALLBACK = {'Swedbank Robur Access Edge': 'övriga passiva', 'SPP Aktiefond Sverige': 'övriga passiva', 'GodFond': 'ej passiv',
            'Nordea 2 SICAV BetaPlus': 'övriga passiva', 'Handelsbanken Stiftelsefond': 'ej passiv',
            'Öhman Etisk Index Sverige': 'övriga passiva',   # SIXPRX-fond efter 2022-11 (FI: Öhman/Lannebo Marknad Sverige Bred)
            'Nordea Institutionella': 'ej passiv'}           # aktiv före 2022-04
M = pd.read_csv(MAND, dtype=str).fillna('')
M = M[M.skikt != 'OMXS30'].copy()
M['nyckel'] = [next((k for k in ALIAS if f.startswith(k)), None) for f in M.fond]
assert M.nyckel.notna().all(), M[M.nyckel.isna()].fond.tolist()
def dat(s, slut=False):
    s = s.strip()
    if not s: return pd.NaT
    if re.fullmatch(r'\d{4}', s): return pd.Timestamp(f'{s}-12-31') if slut else pd.Timestamp(f'{s}-01-01')
    return pd.Timestamp(s)
M['start'] = [dat(s) for s in M.start]; M['slut'] = [dat(s, True) for s in M.slut]
M['skikt0'] = M.skikt.str.replace('?', '', regex=False)
M['belagd'] = M.status.str.startswith('verifierad') | M.status.str.startswith('ej följare')
M['obelagd'] = ~M.belagd | M.skikt.str.endswith('?')
if not INKL: M.loc[M.obelagd & M.skikt0.isin(['B', 'V', 'C']), 'skikt0'] = 'X'   # regel 6: obelagda följare räknas inte
M.to_csv(os.path.join(OUT, 'mandat_anvand.csv'), index=False)
log(f"mandatfil {os.path.basename(MAND)}: {len(M)} rader, följare (B/V/C) som används: {int(M.skikt0.isin(['B','V','C']).sum())}, obelagda som {'INGÅR' if INKL else 'INTE ingår'}: {int((M.obelagd & M.skikt.str.replace('?','',regex=False).isin(['B','V','C'])).sum())}")
MR = {k: g for k, g in M[M.skikt0.isin(['B', 'V', 'C'])].groupby('nyckel')}
MX = {k: g for k, g in M[(M.skikt == 'X') & (M.start.notna() | M.slut.notna())].groupby('nyckel')}   # bara rader som är X i filen, inte nedflyttade obelagda   # daterade X-rader: indexnära utan att följa = övriga passiva
def x_vid(nyckel, d):
    g = MX.get(nyckel)
    if g is None: return False
    return any((pd.isna(x.start) or x.start <= d) and (pd.isna(x.slut) or d <= x.slut) for x in g.itertuples())
def skikt_vid(nyckel, d):
    g = MR.get(nyckel)
    if g is None: return None
    for x in g.itertuples():
        if (pd.isna(x.start) or x.start <= d) and (pd.isna(x.slut) or d <= x.slut): return x.skikt0
    return None

# ---------- Lipper-raderna (runda 8 och 9)
F = pd.read_csv(DATA / 'funds' / 'fund_holdings_lipper_around_events_2007_2026.csv.gz', low_memory=False)
F = F.rename(columns={'Fund Name': 'fond', 'Fund Type Description': 'ftyp', 'Fund Shares Held (Adjusted)': 'aktier', 'Fund Holdings Filing Date': 'rapport', 'Fund Address Country': 'land'})
F['rapport'] = pd.to_datetime(F.rapport, errors='coerce'); F['asofd'] = pd.to_datetime(F['asof']); F['aktier'] = pd.to_numeric(F.aktier, errors='coerce')
I = pd.read_csv(DATA / 'funds' / 'fund_holdings_request_list.csv'); I = I[I.kind == 'event'].copy(); I['AD'] = pd.to_datetime(I.AD); I['ED'] = pd.to_datetime(I.ED)
F = F.merge(I[['event_id', 'type', 'AD', 'ED', 'review_cycle']], on='event_id', how='left')
F['fl'] = F.fond.fillna('').str.lower(); F['svensk'] = F.land.eq('Sweden')
def nyckel_for(s):
    for k, (rx, _, _) in ALIAS.items():
        if re.search(rx, s): return k
    return None
NY = {s: nyckel_for(s) for s in F.fl.unique()}
FT = F.groupby('fl').ftyp.first().to_dict(); SV = F.groupby('fl').svensk.first().to_dict()
def grupp9(s, ftyp, rapport):   # runda 9:s namnregler utan OMXSB-följare (de kommer från mandatfilen)
    if re.search(r'xact omxs30|avanza zero|aktiespararna topp sverige', s): return 'OMXS30' if not (('zero' in s) and rapport > pd.Timestamp('2025-06-30')) else 'övriga passiva'
    if re.search(r'(smabolag|småbolag|small ?cap|mikrobolag)', s) and re.search(r'index|indeks|xact|etf|plus ', s) and re.search(r'sverige|svenska|sweden', s): return 'småbolagsindex'
    if ftyp == 'Exchange-Traded Fund' or re.search(r'index|indeks|passiv|passive|tracker|exponering', s): return 'övriga passiva'
    return 'ej passiv'
if VALID:
    raise SystemExit('Valideringsläget mot runda 9 finns bara i det gamla repot.')
    ns = {}
    g9 = ns['grupp']
    def grupp(fl, d):
        g = g9(types.SimpleNamespace(fond=fl, rapport=d, ftyp=FT[fl]))
        if g == 'OMXSB-index': g = 'OMXSB-B'
        if g == 'OMXSB-blandfond': g = 'OMXSB-C'
        if g == 'övriga passiva': g = 'övriga passiva, svenska' if SV[fl] else 'övriga passiva, utländska'
        return g
else:
    def grupp(fl, d):
        """grupp för fonden med LSEG-namn fl på rapportdagen d."""
        k = NY[fl]
        if k is not None:
            sk = skikt_vid(k, d)
            if sk: return 'OMXSB-' + sk
            g = 'övriga passiva' if x_vid(k, d) else (FALLBACK.get(k) or grupp9(fl, FT[fl], d))
        else: g = grupp9(fl, FT[fl], d)
        if g == 'övriga passiva': g = 'övriga passiva, svenska' if SV[fl] else 'övriga passiva, utländska'
        return g
F['gammal'] = (F.asofd - F.rapport).dt.days > 120
RAPP = F.dropna(subset=['rapport'])[['fond', 'rapport']].drop_duplicates()
RD = RAPP.groupby('fond').rapport.apply(lambda s: np.sort(s.values)).to_dict()
def rapport_i(fond, a, b, sista=False):
    """rapportdatum för fonden i [a, b] (i någon aktie): första, eller sista om sista=True; None om ingen."""
    d = RD.get(fond)
    if d is None: return None
    i = np.searchsorted(d, np.datetime64(a)); j = np.searchsorted(d, np.datetime64(b), side='right')
    if i >= j: return None
    return pd.Timestamp(d[j - 1] if sista else d[i])
GR = ['OMXSB-B', 'OMXSB-V', 'OMXSB-C', 'OMXS30', 'småbolagsindex', 'övriga passiva, svenska', 'övriga passiva, utländska', 'ej passiv']
# ---------- nettoköp per händelse och grupp. regel 1: samma grupp vid rapporten före AD och efter ED, annars utesluts fonden ur händelsen.
# regel 2: fonden ska rapportera inom 120 dagar före AD och 45 dagar efter ED (i någon aktie); saknat innehav = 0.
G0 = F[~F.gammal & F.aktier.notna()]
out, byter, nf = {}, [], {}
GAMLA_EFTER = []   # fond-händelser där LSEG gav en rad från före beskedet som efter-rad
ALLA_FONDER = sorted(F.fond.dropna().unique())
for e, x in G0.groupby('event_id'):
    AD, ED = x.AD.iloc[0], x.ED.iloc[0]
    for f, xf in x.groupby('fond'):
        d0 = rapport_i(f, AD - pd.Timedelta(days=120), AD - pd.Timedelta(days=1), sista=True); d1 = rapport_i(f, ED, ED + pd.Timedelta(days=45))
        if d0 is None or d1 is None: continue
        g0, g1 = grupp(f.lower(), d0), grupp(f.lower(), d1)
        if g0 != g1: byter.append(dict(event_id=e, fond=f, fore=g0, efter=g1, d0=d0.date(), d1=d1.date())); continue
        # efter-raden räknas bara om den är rapporterad på eller efter ED: har fonden sålt hela innehavet ger LSEG annars den
        # senaste raden före beskedet, och då blev nettoförsäljningen 0 i stället för hela innehavet (rättat 9 nov 2026)
        efter = xf[(xf.snap == 'efter') & (xf.rapport >= ED)].aktier.sum()
        out[(e, g0)] = out.get((e, g0), 0.0) + efter - xf[xf.snap == 'fore'].aktier.sum()
        if ((xf.snap == 'efter') & (xf.rapport < ED) & (xf.aktier > 0)).any(): GAMLA_EFTER.append(dict(event_id=e, fond=f))
NT = pd.Series(out).unstack().reindex(columns=GR).fillna(0.0) if out else pd.DataFrame(columns=GR)
BY = pd.DataFrame(byter); BY.to_csv(os.path.join(OUT, 'uteslutna_mandatbyte.csv'), index=False)
log(f'efter-rader från före ED som räknats som 0 (fonden har sålt allt): {len(GAMLA_EFTER)} fond-händelser {GAMLA_EFTER[:10]}')
log(f'fond-händelser uteslutna för grupp-byte mellan rapporterna: {len(BY)}' + (f" ({BY.fond.nunique()} fonder: {', '.join(sorted(BY.fond.unique())[:12])})" if len(BY) else ''))
# regel 3: antal fonder per skikt som rapporterar runt händelsen (oavsett innehav), med samma skikt vid båda rapporterna
KAND = sorted({f for f in ALLA_FONDER if NY.get(f.lower()) in MR}) if not VALID else sorted({f for f in ALLA_FONDER if grupp(f.lower(), pd.Timestamp('2015-01-01')).startswith('OMXSB') or grupp(f.lower(), pd.Timestamp('2025-12-01')).startswith('OMXSB')})
def n_rapp(AD, ED):
    n = dict(B=0, V=0, C=0)
    for f in KAND:
        d0 = rapport_i(f, AD - pd.Timedelta(days=120), AD - pd.Timedelta(days=1), sista=True); d1 = rapport_i(f, ED, ED + pd.Timedelta(days=45))
        if d0 is None or d1 is None: continue
        g0, g1 = grupp(f.lower(), d0), grupp(f.lower(), d1)
        if g0 == g1 and g0.startswith('OMXSB-'): n[g0[-1]] += 1
    return n
# fondtabell: grupp per fond och år (för granskning)
rows = []
for f in ALLA_FONDER:
    for ar in range(2007, 2027):
        d = pd.Timestamp(f'{ar}-06-30'); g = grupp(f.lower(), d)
        if g.startswith('OMXSB') or NY.get(f.lower()) is not None: rows.append(dict(fond=f, ar=ar, grupp=g))
FT_ = pd.DataFrame(rows).pivot(index='fond', columns='ar', values='grupp') if rows else pd.DataFrame()
FT_.to_csv(os.path.join(OUT, 'fondgrupp_per_ar.csv'))

# ---------- händelser från rättelserna 3 nov; bara fondkolumnerna byts
E = pd.read_csv(DATA / 'events' / 'omxsb_changes_corrected_2007_2026.csv', parse_dates=['AD', 'ED']); E['split'] = E.split.astype(bool)
GAMLA = [c for c in E.columns if c.startswith('n_')] + ['D', 'passiva_ovriga', 'aktiva', 'alla_fonder', 'n_indexfonder', 'D_ny']
E = E.rename(columns={c: 'r11_' + c for c in GAMLA})
for g_ in GR:
    v = NT[g_] if g_ in NT else pd.Series(dtype=float)
    E['n_' + g_] = [s_ * 100 * v.get(e_, 0.0) / sh if sh > 0 else np.nan for s_, e_, sh in zip(E.s, E.event_id, E.sh_ed)]
NR = [n_rapp(a, d) for a, d in zip(E.AD, E.ED)]
for sk in ['B', 'V', 'C']: E['nf_' + sk] = [r[sk] for r in NR]
E['D_B'] = np.where(E.nf_B > 0, E['n_OMXSB-B'], np.nan)
E['D_V'] = np.where(E.nf_B + E.nf_V > 0, E['n_OMXSB-B'] + E['n_OMXSB-V'], np.nan)
E['D_C'] = np.where(E.nf_B + E.nf_V + E.nf_C > 0, E['n_OMXSB-B'] + E['n_OMXSB-V'] + E['n_OMXSB-C'], np.nan)
E['B_bara'] = E['n_OMXSB-B']; E['V_bara'] = E['n_OMXSB-V']; E['C_bara'] = E['n_OMXSB-C']
E['passiva_ovriga'] = E[['n_OMXS30', 'n_småbolagsindex', 'n_övriga passiva, svenska', 'n_övriga passiva, utländska']].sum(1, min_count=1)
E['aktiva'] = E['n_ej passiv']; E['alla_fonder'] = E[['n_' + g for g in GR]].sum(1, min_count=1)
E.loc[~E.fonddata, ['D_B', 'D_V', 'D_C']] = np.nan
E.to_csv(os.path.join(OUT, 'handelser_omraknade.csv'), index=False)
if VALID:
    for a, b in [('n_OMXSB-B', 'r11_n_OMXSB-index'), ('n_OMXSB-C', 'r11_n_OMXSB-blandfond'), ('n_OMXS30', 'r11_n_OMXS30'), ('n_ej passiv', 'r11_n_ej passiv'), ('n_övriga passiva, svenska', 'r11_n_övriga passiva, svenska')]:
        d = (E[a] - E[b]).abs(); ev = E[d > 1e-9].event_id.tolist()
        log(f'validering {a}: händelser som skiljer sig från runda 11: {len(ev)} {ev[:10]}; max skillnad {d.max():.4f}')
    log(f"validering nf_B mot n_indexfonder: lika i {(E.nf_B == E.r11_n_indexfonder).sum()} av {len(E)} händelser")

# ---------- inferens (samma som runda 11 och rättelserna 3 nov)
rng = np.random.default_rng(20261102)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
def wdraw(B, G): return rng.choice([-1., 1.], (B, G)) if G >= 12 else rng.choice(WEBB, (B, G))
CI_BOOT = '95 % intervall: invertering av restriktiv wild cluster bootstrap per översyn (9 999 dragningar)'
P_BOOT = 'p: restriktiv wild cluster bootstrap per översyn (Rademacher om G>=12, annars Webb; 9 999 dragningar)'
CI_ANAL = '95 % intervall: analytiskt, CR1 per översyn, t med G-1 (ingen bootstrap)'
M_BOOT = '95 % intervall för M: parvis klusterbootstrap (översyner dras med återläggning), percentil, 9 999 dragningar'
def lin(X, y, g, c, B=9999, boot=True):
    # boot=True: p och 95 % intervall från samma restriktiva wild cluster bootstrap (intervallet genom testinversion).
    # boot=False: bara analytiskt CR1-intervall, inget p. lo_cr1/hi_cr1 finns alltid som jämförelse.
    X = np.asarray(X, float); y = np.asarray(y, float); c = np.asarray(c, float)
    ok = np.isfinite(y) & np.isfinite(X).all(1); X = X[ok]; y = y[ok]
    codes = pd.factorize(np.asarray(g)[ok])[0]; G = codes.max() + 1; n, k = X.shape
    if G < 3 or n <= k: return dict(b=np.nan, se=np.nan, lo=np.nan, hi=np.nan, p=np.nan, n=n, G=G, ci_metod='för få kluster, ingen inferens')
    XtXi = np.linalg.pinv(X.T @ X); Am = XtXi @ X.T; q = X @ (XtXi @ c); adj = G / (G - 1) * (n - 1) / max(n - k, 1)
    Hq = np.zeros((n, G)); Hq[np.arange(n), codes] = q
    def tse(Y):
        Bm = Y @ Am.T; Ee = Y - Bm @ X.T; sg = Ee @ Hq; return Bm @ c, np.sqrt((sg ** 2).sum(1) * adj)
    t0, s0 = tse(y[None, :]); t0, s0 = t0[0], s0[0]; qq = tdist.ppf(.975, G - 1)
    ut = dict(b=float(t0), se=float(s0), lo=float(t0 - qq * s0), hi=float(t0 + qq * s0), lo_cr1=float(t0 - qq * s0), hi_cr1=float(t0 + qq * s0),
              p=np.nan, n=int(n), G=int(G), ci_metod=CI_ANAL, p_metod='inget p')
    if not boot: return ut
    Wc = np.concatenate([wdraw(1000, G) for _ in range(B // 1000 + 1)])[:B][:, codes]
    v = XtXi @ c / (c @ XtXi @ c)
    def pw(th):
        ys = y - th * (X @ v); b = Am @ ys; br = b - XtXi @ c * (c @ b) / (c @ XtXi @ c); fr = X @ br; er = ys - fr
        bs, ss = tse(fr[None, :] + er[None, :] * Wc); return float((np.abs(bs / ss) >= abs((t0 - th) / s0)).mean())
    def kant(sgn):
        inne, ute = t0, t0 + sgn * qq * s0
        while pw(ute) > .05:   # obegränsat om testet inte förkastar inom 20 standardfel (få kluster bakom kontrasten)
            if abs(ute - t0) >= 20 * s0 * (1 - 1e-9): return sgn * np.inf
            ute = t0 + sgn * min(2 * abs(ute - t0), 20 * s0)
        while abs(ute - inne) > 1e-4 * max(s0, 1e-12):
            m = (inne + ute) / 2
            if pw(m) > .05: inne = m
            else: ute = m
        return (inne + ute) / 2
    ut.update(p=pw(0.0), lo=kant(-1), hi=kant(1), ci_metod=CI_BOOT, p_metod=P_BOOT); return ut
def medel(s, col, boot=False): return lin(np.ones((len(s), 1)), s[col].values, s.review.values, [1.0], boot=boot)
KC = ['k_oms', 'k_storlek', 'k_wz', 'k_ana']
def kvot_ci(d, yc, dc, B=9999):   # alla dragningar med; medel-D <= 0 ger ±oändligt (som rättelserna 3 nov)
    rv = d.review.values; u = np.unique(rv); idx = {k: np.where(rv == k)[0] for k in u}; ks = np.empty(B)
    for b in range(B):
        ii = np.concatenate([idx[k] for k in rng.choice(u, len(u))]); dm = d[dc].values[ii].mean(); cm = d[yc].values[ii].mean()
        ks[b] = cm / dm if dm > 0 else (np.inf if cm >= 0 else -np.inf)
    return np.quantile(ks, .025), np.quantile(ks, .975), float(np.mean(~np.isfinite(ks)))
rows = []
# tabell 5: M per period, tre skikt, utan split; plus decennier
PER2 = {'2007–16': lambda s: s.ar <= 2016, '2017–26': lambda s: s.ar >= 2017}
for ty in ['addition', 'deletion']:
    for dc in ['D_B', 'D_V', 'D_C']:
        s0 = E[(E.type == ty) & ~E.split & E[dc].notna()]
        for yc in ['y_tot', 'y_lang']:
            for p_ in PERS + list(PER2):
                d = s0[(s0.per == p_) if p_ in PERS else PER2[p_](s0)]; d = d[d[yc].notna()]
                if len(d) < 3: rows.append(dict(tabell='5', typ=ty, skikt=dc, fonster=yc, period=p_, n=len(d), ci_metod='för få händelser, ingen inferens')); continue
                lo, hi, inf = kvot_ci(d, yc, dc)
                rows.append(dict(tabell='5', typ=ty, skikt=dc, fonster=yc, period=p_, n=len(d), G=d.review.nunique(), car=d[yc].mean(), D=d[dc].mean(),
                                 M=d[yc].mean() / d[dc].mean() if d[dc].mean() > 0 else np.nan, lo=lo, hi=hi, andel_oandliga=inf, D_noll=int((d[dc] == 0).sum()), ci_metod=M_BOOT, p_metod='inget p'))
# tabell 6: M med och utan kontroller, H11a (2007–11 mot 2022–26) och H11b (2017–21 mot 2022–26), tre skikt
for ty in ['addition', 'deletion']:
    for dc in ['D_B', 'D_V', 'D_C']:
        for yc in ['y_tot', 'y_lang']:
            for kontroller in [False, True]:
                s = E[(E.type == ty) & ~E.split & E[dc].notna() & E[yc].notna()].copy()
                if kontroller:
                    s = s.dropna(subset=KC)
                    for c in KC: s[c] = s[c] - s[c].mean()
                Db = s.groupby('per')[dc].mean().reindex(PERS)
                X = np.column_stack([((s.per == p_).astype(float) * Db[p_]).values for p_ in PERS] + ([s[c].values for c in KC] if kontroller else []))
                for j, p_ in enumerate(PERS):
                    c = np.zeros(X.shape[1]); c[j] = 1; r = lin(X, s[yc].values, s.review.values, c, boot=False)
                    rows.append(dict(tabell='6', typ=ty, skikt=dc, fonster=yc, kontroller=kontroller, period=f'M {p_}', n_period=int((s.per == p_).sum()), D_medel=Db[p_], **r))
                for a_, b_, lab in [(0, 3, 'M 2007–11 − M 2022–26'), (2, 3, 'M 2017–21 − M 2022–26'), (1, 3, 'M 2012–16 − M 2022–26')]:
                    c = np.zeros(X.shape[1]); c[a_], c[b_] = 1, -1; r = lin(X, s[yc].values, s.review.values, c)
                    rows.append(dict(tabell='6', typ=ty, skikt=dc, fonster=yc, kontroller=kontroller, period=lab, **r))
# tabell 7: vem handlar, utan split, per period och 2017–26 (tecken: positivt = i indexfondernas riktning, som runda 11)
for ty in ['addition', 'deletion']:
    s0 = E[(E.type == ty) & ~E.split & E.fonddata & E.D_C.notna()]   # huvudmåttet C (11 nov); samma händelser som D_V
    for p_ in PERS + ['2017–26']:
        s = s0[s0.ar >= 2017] if p_ == '2017–26' else s0[s0.per == p_]
        if len(s) < 3: continue
        for col in ['B_bara', 'V_bara', 'C_bara', 'D_B', 'D_V', 'D_C', 'n_OMXS30', 'n_småbolagsindex', 'n_övriga passiva, svenska', 'n_övriga passiva, utländska', 'passiva_ovriga', 'aktiva', 'alla_fonder']:
            r = medel(s, col, boot=(p_ == '2017–26' and col == 'aktiva')); rows.append(dict(tabell='7', typ=ty, period=p_, grupp=col, **r))
T = pd.DataFrame(rows); T.to_csv(os.path.join(OUT, 'omrakning_resultat.csv'), index=False)
# figur 1: D per år och skikt (utan split, som runda 11)
f1 = []
for ar, g in E[E.fonddata & ~E.split].groupby('ar'):
    rr = dict(ar=ar)
    for ty in ['addition', 'deletion']:
        q = g[g.type == ty]
        for dc in ['D_B', 'D_V', 'D_C']: rr[f'{dc}_{ty}'] = q[dc].mean(); rr[f'n_{dc}_{ty}'] = int(q[dc].notna().sum())
    f1.append(rr)
F1 = pd.DataFrame(f1)

# ---------- SHoF: fondförmögenhet per skikt med daterat medlemskap; blandfonder (C) vägda med OMXSB-andelen i FI:s jämförelseindex
L = pd.read_csv(DATA / 'funds' / 'fund_ids_shof.csv')
with zipfile.ZipFile(DATA / 'funds' / 'fund_aum_shof_monthly.zip') as z:
    V = pd.read_csv(z.open(z.namelist()[0]), sep=';', parse_dates=['date'], usecols=['performanceId', 'date', 'tnaclass', 'tnafund'])
V = V.merge(L[['performanceid', 'fundid', 'fundname']].drop_duplicates(), left_on='performanceId', right_on='performanceid'); V['m'] = V.date.dt.to_period('M')
idx = pd.period_range('2006-01', V.m.max(), freq='M'); MSLUT = {m: m.to_timestamp(how='end') for m in idx}
SHOF_UNDANTAG = {'Öhman Marknad Sverige Bred': pd.Timestamp('2012-12-31')}   # tnafund 14,6 gånger andelsklassernas summa alla månader 2006–2012, försvinner 2013: fel i källan, klassumman används
def fond_manad(x, fn=None):   # som shof_aum.py: dagsvärde = tnafund (om > 0), annars summa tnaclass; månadsvärde = senaste dagsvärde inom 92 dagar
    x = x.copy(); x.loc[x.tnafund <= 0, 'tnafund'] = np.nan
    if fn in SHOF_UNDANTAG: x.loc[x.date <= SHOF_UNDANTAG[fn], 'tnafund'] = np.nan
    f = x.dropna(subset=['tnafund']).groupby('date').tnafund.last(); c = x.dropna(subset=['tnaclass']).groupby('date').tnaclass.sum()
    dag = pd.concat([f.rename('v'), c[~c.index.isin(f.index)].rename('v')]).sort_index(); out = {}
    for m in idx:
        slut = MSLUT[m]; d = dag[(dag.index <= slut) & (dag.index > slut - pd.Timedelta(days=92))]
        out[m] = d.iloc[-1] if len(d) else np.nan
    return pd.Series(out)
AUM = {}
for fn in L.fundname.unique():
    parts = [fond_manad(x, fn) for _, x in V[V.fundname == fn].groupby('fundid')]
    if parts: AUM[fn] = sum(p.reindex(idx).fillna(0) for p in parts) / 1e9
AUM = pd.DataFrame(AUM, index=idx)
fa = pd.read_csv(DATA / 'funds' / 'fund_list_fi_quarterly_2018_2026.csv', low_memory=False); fa['kvartal'] = pd.to_datetime(fa.kvartal); fa['nl'] = fa.namn.str.lower()
def omxsb_andel(jmf):   # OMXSB-delens vikt i jämförelseindexet, 0–1
    if not isinstance(jmf, str): return np.nan
    for del_ in jmf.split(';'):
        if re.search(r'omx ?s(?:tockholm)? ?b(?:enchmark)?|omxsb|sbx', del_, re.I):
            m = re.search(r'(\d+(?:[.,]\d+)?)\s*%?\s*$', del_.strip())
            return float(m.group(1).replace(',', '.')) / 100 if m else 1.0
    return np.nan
fa['andel'] = fa.jmf.map(omxsb_andel)
def fi_andel_serie(key, fn):
    _, names, firx = ALIAS[key]
    q = fa[fa.namn == fn] if firx == 'samma namn' else fa[fa.nl.str.contains(firx, regex=True)]
    s = q.dropna(subset=['andel']).groupby('kvartal').andel.first().sort_index()
    if not len(s): return None
    out = {}
    for m in idx:
        s2 = s[s.index <= MSLUT[m]]; out[m] = float(s2.iloc[-1]) if len(s2) else float(s.iloc[0])   # före FI-perioden: första kända värdet
    return pd.Series(out)
ser = {sk: pd.Series(0.0, index=idx) for sk in ['B', 'V', 'C']}; sk_log = []; vikt_log = []
for r in M[M.skikt0.isin(['B', 'V', 'C'])].itertuples():
    for fn in ALIAS[r.nyckel][1]:
        if fn not in AUM: sk_log.append(f'{r.fond}: SHoF-serie saknas för {fn}'); continue
        galler = pd.Series([(pd.isna(r.start) or r.start <= MSLUT[m]) and (pd.isna(r.slut) or m.to_timestamp() <= r.slut) for m in idx], index=idx)
        if r.skikt0 == 'C':
            w = fi_andel_serie(r.nyckel, fn)
            if w is None: sk_log.append(f'{r.fond}: ingen OMXSB-andel i FI för {fn}, vikt 0'); continue
            vikt_log.append(dict(fond=fn, vikt_2019=w.get(pd.Period('2019-12', 'M')), vikt_2022=w.get(pd.Period('2022-12', 'M')), vikt_2025=w.get(pd.Period('2025-12', 'M'))))
            ser['C'] += AUM[fn].where(galler, 0.0) * w
        else: ser[r.skikt0] += AUM[fn].where(galler, 0.0)
# fondtabell (tabell A6, 11 nov 2026): varje fond i fondlistan, cirkel per period, hela fondens förmögenhet och den del som räknas i
# ägarandelen (blandfonder vägda med OMXSB-andelen, bara inom följarperioden). Ändrar inga andra siffror.
ALLA_M = pd.read_csv(MAND, dtype=str).fillna(''); ALLA_M = ALLA_M[ALLA_M.skikt != 'OMXS30']
SIST = idx[-1]; DAGAR = [pd.Period(x, 'M') for x in ['2015-12', '2020-12', '2025-12']] + [SIST]
ft = []
for k in dict.fromkeys(M.nyckel):
    rr = M[M.nyckel == k]; namn = [fn for fn in ALIAS[k][1] if fn in AUM]
    hel = sum((AUM[fn] for fn in namn), pd.Series(0.0, index=idx)) if namn else None
    rakn = pd.Series(0.0, index=idx)
    for r in rr[rr.skikt0.isin(['B', 'V', 'C'])].itertuples():
        for fn in namn:
            galler = pd.Series([(pd.isna(r.start) or r.start <= MSLUT[m]) and (pd.isna(r.slut) or m.to_timestamp() <= r.slut) for m in idx], index=idx)
            w = fi_andel_serie(r.nyckel, fn) if r.skikt0 == 'C' else pd.Series(1.0, index=idx)
            if w is not None: rakn += AUM[fn].where(galler, 0.0) * w
    per_ = [f"{x.skikt0} {x.start.year if pd.notna(x.start) else '…'}–{x.slut.year if pd.notna(x.slut) else ''}" for x in rr.itertuples()]
    rad = dict(nyckel=k, fond=rr.fond.iloc[0], cirklar='; '.join(per_), cirkel_nu=next((x.skikt0 for x in rr.itertuples() if pd.isna(x.slut)), 'ingen'),
               shof_namn='; '.join(namn), i_shof=bool(namn), status=rr.status.iloc[0])
    for d_ in DAGAR:
        rad[f'aum_{d_}'] = float(hel[d_]) if hel is not None else np.nan; rad[f'raknas_{d_}'] = float(rakn[d_]) if namn else np.nan
    ft.append(rad)
FT6 = pd.DataFrame(ft); FT6['sista_manad'] = str(SIST)
FT6.to_csv(os.path.join(OUT, 'fondtabell_aum.csv'), index=False)
S = pd.DataFrame({'manad': idx.astype(str), 'B_mdkr': ser['B'].values, 'V_mdkr': (ser['B'] + ser['V']).values, 'C_mdkr': (ser['B'] + ser['V'] + ser['C']).values})
S.to_csv(os.path.join(OUT, 'shof_aum_skikt.csv'), index=False); pd.DataFrame(vikt_log).to_csv(os.path.join(OUT, 'blandfond_vikter.csv'), index=False)
G = pd.read_csv(DATA / 'comparison' / 'previous_run_demand_and_ownership_by_year.csv')[['ar', 'D_addition', 'D_deletion', 'omxsb_mdkr', 'fonder_mdkr', 'agarandel_pct']].rename(columns={'D_addition': 'r11_D_addition', 'D_deletion': 'r11_D_deletion', 'fonder_mdkr': 'r11_fonder_mdkr', 'agarandel_pct': 'r11_agarandel_pct'})
Sd = S[S.manad.str.endswith('-12')].copy(); Sd['ar'] = Sd.manad.str[:4].astype(int)
F1 = F1.merge(G, on='ar', how='left').merge(Sd[['ar', 'B_mdkr', 'V_mdkr', 'C_mdkr']], on='ar', how='left')
for sk in ['B', 'V', 'C']: F1[f'agarandel_{sk}_pct'] = 100 * F1[f'{sk}_mdkr'] / F1.omxsb_mdkr
F1.to_csv(os.path.join(OUT, 'figur1_skikt.csv'), index=False)
# steg 0: jämförelse mot FI (nettokop_v2) per skikt
fi = pd.read_csv(DATA / 'funds' / 'fund_net_buying_fi_by_event_2019_2026.csv'); fi = fi[fi.status == 'ok']
fi = fi.merge(E[['event_id', 'RIC', 'review']], on=['RIC', 'review'])
chk = {}
for dc in ['D_B', 'D_V', 'D_C', 'r11_D_ny']:
    m_ = fi.merge(E[['event_id', dc]], on='event_id').dropna(subset=[dc, 'netto_OMXSB_ny'])
    chk[dc] = dict(n=len(m_), korr=round(float(np.corrcoef(m_[dc], m_.netto_OMXSB_ny)[0, 1]), 3), lseg=round(float(m_[dc].mean()), 3), fi=round(float(m_.netto_OMXSB_ny.mean()), 3))
json.dump(dict(fi_jamforelse=chk, shof_saknas=sk_log, inkl_obelagda=INKL, validering=VALID, uteslutna_mandatbyten=int(len(BY)), logg=LOG), open(os.path.join(OUT, 'kontroller.json'), 'w'), indent=1, ensure_ascii=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 400)
print('SHoF saknas:', sk_log); print('FI-jämförelse:', chk)
print('Metod tabell 5 (M per period): ' + M_BOOT + '.')
print(T[(T.tabell == '5') & (T.fonster == 'y_tot')][['typ', 'skikt', 'period', 'n', 'G', 'car', 'D', 'M', 'lo', 'hi', 'D_noll']].round(2).to_string(index=False))
print('Metod tabell 6: M per period (rader "M 20xx") = ' + CI_ANAL + '; skillnader mellan perioder = ' + CI_BOOT + ', ' + P_BOOT + '.')
print('Metod tabell 7 (vem köper): ' + CI_ANAL + ', utom aktiva fonder 2017–26: ' + CI_BOOT + ', ' + P_BOOT + '.')
t7 = T[(T.tabell == '7') & (T.period == '2017–26')].copy(); t7['metod'] = np.where(t7.ci_metod == CI_BOOT, 'bootstrap', 'analytiskt')
print(t7[['typ', 'grupp', 'b', 'lo', 'hi', 'p', 'n', 'G', 'metod']].round(3).to_string(index=False))
for m_ in sorted(T.ci_metod.dropna().unique()): print(f'Metod: {m_}: {int((T.ci_metod == m_).sum())} rader i omrakning_resultat.csv')
print(F1[['ar', 'r11_D_addition', 'D_B_addition', 'D_V_addition', 'D_C_addition', 'n_D_V_addition', 'r11_agarandel_pct', 'agarandel_B_pct', 'agarandel_V_pct', 'agarandel_C_pct']].round(3).to_string(index=False))
