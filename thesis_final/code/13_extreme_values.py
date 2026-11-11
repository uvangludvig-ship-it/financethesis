# Steg 13: robusthet för extremvärden. Deklaration: declarations/step13_16_declaration.md (11 nov 2026, 13:36).
#   Tabell 1 i fyra varianter, samma nio rader som tabell A4 (perioder, decennier, skillnader), totalt fönster [AD−1, ED+1]:
#     alla            = tabell 1 (urvalet efter G&S regel för borttag)
#     winsoriserad    = CAR winsoriserad vid 1:a och 99:e percentilen, gränserna räknade på alla 481 händelser med CAR (ev_alla)
#     utan |CAR| > 20 = händelser med |CAR| över 20 % borttagna
#     utan Sivers     = utan OMXSB-2026H1-10 (CAR +77 %)
#   Median per period och variant (beskrivande, ingen inferens).
#   M för tillägg (D_V, [AD−1, ED+1], utan split) 2017–21, 2022–26 och 2017–26: alla, och utan de 12 händelserna med "ja" i
#   data/events/news_screen_extreme_events.csv. Kvoten och den parvisa klusterbootstrapen som i steg 02 (tabell 5).
# Inferens för CAR: som tabell 1 (lin(): klustrat per översyn, restriktiv wild cluster bootstrap, intervall genom testinversion).
# Körs från thesis_final efter 02: python3 code/13_extreme_values.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'extreme_values'

SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg13'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, lin, stars, ev, ev_alla, wsum, pos = g['np'], g['pd'], g['lin'], g['stars'], g['ev'], g['ev_alla'], g['wsum'], g['pos']
os.makedirs(OUT, exist_ok=True)
rows, avvik = [], []
def jfr(namn, nytt, gammalt, tol):
    if not abs(float(nytt) - float(gammalt)) <= tol: avvik.append(f'{namn}: nu {float(nytt):.6f}, då {float(gammalt):.6f}')

# ---------- CAR: fyra varianter
ev = ev[ev.tot.notna()].copy()
ea = ev_alla.copy(); ea['tot'] = [wsum(r, pos.get(a, np.nan) - 1, pos.get(e, np.nan) + 1) for r, a, e in zip(ea.RIC, ea.AD, ea.ED)]
ea = ea[ea.tot.notna()]
assert len(ea) == 481, len(ea)
LO, HI = np.percentile(ea.tot.values, [1, 99])
SIVERS = 'OMXSB-2026H1-10'
VAR = {'alla': ev,
       'winsoriserad 1/99': ev.assign(tot=ev.tot.clip(LO, HI)),
       'utan |CAR| > 20': ev[ev.tot.abs() <= 20],
       'utan Sivers': ev[ev.event_id != SIVERS]}
PERS = ['2007–2011', '2012–2016', '2017–2021', '2022–2026']
TEST = ['2007–11', '2012–16', '2017–21', '2022–26', '2007–16', '2017–26', '2017–26 minus 2007–16', '2022–26 minus 2007–11', '2022–26 minus 2017–21']
for v, d0 in VAR.items():
    for ty in ['addition', 'deletion']:
        d = d0[d0.type == ty]
        sel = {'2007–11': d.period == '2007–2011', '2012–16': d.period == '2012–2016', '2017–21': d.period == '2017–2021',
               '2022–26': d.period == '2022–2026', '2007–16': d.ar <= 2016, '2017–26': d.ar >= 2017}
        for lab, q in sel.items():
            x = d[q]
            rows.append(dict(matt='CAR', variant=v, typ=ty, test=lab, median=float(x.tot.median()),
                             **lin(np.ones((len(x), 1)), x.tot.values, x.review_cycle.values, [1.])))
        X = np.column_stack([np.ones(len(d)), (d.ar >= 2017).astype(float).values])
        rows.append(dict(matt='CAR', variant=v, typ=ty, test='2017–26 minus 2007–16', **lin(X, d.tot.values, d.review_cycle.values, [0, 1])))
        X = np.column_stack([(d.period == p).astype(float).values for p in PERS])
        for lab, c in [('2022–26 minus 2007–11', [-1, 0, 0, 1]), ('2022–26 minus 2017–21', [0, 0, -1, 1])]:
            rows.append(dict(matt='CAR', variant=v, typ=ty, test=lab, **lin(X, d.tot.values, d.review_cycle.values, c)))

# ---------- M för tillägg, med och utan de 12 med egen bolagsnyhet (som tabell 5 i steg 02)
rng2 = np.random.default_rng(20261102)
M_BOOT = '95 % intervall för M: parvis klusterbootstrap (översyner dras med återläggning), percentil, 9 999 dragningar'
def kvot_ci(d, yc, dc, B=9999):   # samma som 02: alla dragningar med; medel-D <= 0 ger ±oändligt
    rv = d.review.values; u = np.unique(rv); idx = {k: np.where(rv == k)[0] for k in u}; ks = np.empty(B)
    for b in range(B):
        ii = np.concatenate([idx[k] for k in rng2.choice(u, len(u))]); dm = d[dc].values[ii].mean(); cm = d[yc].values[ii].mean()
        ks[b] = cm / dm if dm > 0 else (np.inf if cm >= 0 else -np.inf)
    return np.quantile(ks, .025), np.quantile(ks, .975)
E = pd.read_csv(RES / 'fund_demand' / 'handelser_omraknade.csv'); E['split'] = E.split.astype(bool)
NS = pd.read_csv(DATA / 'events' / 'news_screen_extreme_events.csv', dtype=str).fillna('')
JA = set(NS.loc[NS.contaminated.str.strip().str.lower() == 'ja', 'event_id']); assert len(JA) == 12, len(JA)
s0 = E[(E.type == 'addition') & ~E.split & E.D_V.notna() & E.y_tot.notna()]
for v, s in [('alla', s0), ('utan egen bolagsnyhet', s0[~s0.event_id.isin(JA)])]:
    for lab, q in [('2017–21', s.per == '2017–21'), ('2022–26', s.per == '2022–26'), ('2017–26', s.ar >= 2017)]:   # som PER2 i 02
        d = s[q]; lo, hi = kvot_ci(d, 'y_tot', 'D_V')
        rows.append(dict(matt='M', variant=v, typ='addition', test=lab, b=d.y_tot.mean() / d.D_V.mean(), lo=lo, hi=hi, n=len(d), G=d.review.nunique(),
                         car=d.y_tot.mean(), D=d.D_V.mean(), ci_metod=M_BOOT, p_metod='inget p'))
R = pd.DataFrame(rows)
R.to_csv(OUT / 'extreme_values_results.csv', index=False)

# ---------- kontroller: "alla" = tabell 1 och tabell 5, och jämförelse med de gamla siffrorna
T1 = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
for ty in ['addition', 'deletion']:
    for lab, full in zip(TEST[:4], PERS):
        a = R[(R.matt == 'CAR') & (R.variant == 'alla') & (R.typ == ty) & (R.test == lab)].iloc[0]
        b = T1[(T1.panel == 'A/B') & (T1.typ == ty) & (T1.fönster == 'tot') & (T1.urval == full)].iloc[0]
        jfr(f'alla = tabell 1, {ty} {lab}', a.b, b.b, 1e-9); jfr(f'alla = tabell 1, {ty} {lab}, antal', a.n, b.n, 0)
R5 = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv'); R5 = R5[(R5.tabell.astype(str) == '5') & (R5.skikt == 'D_V') & (R5.fonster == 'y_tot') & (R5.typ == 'addition')]
for lab in ['2017–21', '2022–26', '2017–26']:
    a = R[(R.matt == 'M') & (R.variant == 'alla') & (R.test == lab)].iloc[0]; b = R5[R5.period == lab].iloc[0]
    jfr(f'M alla = tabell 5, {lab}', a.b, b.M, 1e-9); jfr(f'M alla = tabell 5, {lab}, antal', a.n, b.n, 0)
PR = pd.read_csv(DATA / 'comparison' / 'previous_run_extreme_values.csv')
for r in PR.itertuples():
    tol = 0.5 * 10 ** -r.decimaler
    if r.variant == 'gränser': nytt = LO if r.test.startswith('1:a') else HI
    else: nytt = R[(R.matt == r.matt) & (R.variant == r.variant) & (R.typ == r.typ) & (R.test == r.test)].iloc[0].b
    jfr(f'{r.variant}, {r.typ}, {r.test}, {r.matt} ({r.kalla})', nytt, r.varde, tol + 1e-12)

# ---------- läsbar text
f = lambda v, d=2: '' if pd.isna(v) else ('∞' if v == np.inf else '−∞' if v == -np.inf else f'{v:.{d}f}'.replace('-', '−'))
cellt = lambda r: f'{f(r.b)}{stars(r.p_wcb) if pd.notna(r.get("p_wcb", np.nan)) else ""} ({f(r.lo)} till {f(r.hi)}), n {int(r.n)}'
L = ['# Steg 13: extremvärden', '', f'Winsoriseringsgränser (1:a och 99:e percentilen av CAR [AD−1, ED+1] över alla {len(ea)} händelser med CAR): '
     f'{f(LO)} och {f(HI)} procent. Inferens för CAR som tabell 1; M med parvis klusterbootstrap som tabell 5.', '',
     '## Jämförelse med de gamla siffrorna och med tabell 1 och 5', '', 'Alla jämförda siffror är desamma.' if not avvik else 'Avvikelser:\n\n' + '\n'.join('- ' + a for a in avvik), '']
for ty, namn in [('addition', 'Tillägg'), ('deletion', 'Borttag')]:
    L += [f'## CAR, {namn.lower()}', '', '| Test | ' + ' | '.join(VAR) + ' |', '|---' * (len(VAR) + 1) + '|']
    for t in TEST:
        L.append(f'| {t} | ' + ' | '.join(cellt(R[(R.matt == "CAR") & (R.variant == v) & (R.typ == ty) & (R.test == t)].iloc[0]) for v in VAR) + ' |')
    L += ['', f'Median, {namn.lower()}:', '', '| Period | ' + ' | '.join(VAR) + ' |', '|---' * (len(VAR) + 1) + '|']
    for t in TEST[:6]:
        L.append(f'| {t} | ' + ' | '.join(f(R[(R.matt == "CAR") & (R.variant == v) & (R.typ == ty) & (R.test == t)].iloc[0]['median']) for v in VAR) + ' |')
    L.append('')
L += ['## M för tillägg (D_V, [AD−1, ED+1], utan split)', '', '| Period | alla | utan egen bolagsnyhet |', '|---|---|---|']
for t in ['2017–21', '2022–26', '2017–26']:
    L.append(f'| {t} | ' + ' | '.join(cellt(R[(R.matt == "M") & (R.variant == v) & (R.test == t)].iloc[0]) for v in ['alla', 'utan egen bolagsnyhet']) + ' |')
(OUT / 'EXTREME_VALUES.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('\n'.join(L))
print('Metod: CAR = wild cluster bootstrap per översyn (intervall genom testinversion); M = parvis klusterbootstrap per översyn, percentil')
print('jämförelse:', 'inga avvikelser' if not avvik else avvik)
