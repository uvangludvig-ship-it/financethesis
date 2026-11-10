# Steg 12: två G&S-test som kräver hela kurspanelen. Flyttade hit från code/claude_checks/runda11.py (del F) och runda10.py (T28),
# båda körda 2 nov 2026, metoden oförändrad. Deklaration: declarations/step11_13_declaration.md (10 nov 2026, 21:46).
#   A. Nyemissioner (G&S avsnitt 2.4.3): förändring i log antal aktier i bolaget (alla noterade aktieslag) från AD−5 till ED+60,
#      i procent, för tillägg och för nästan tillagda aktier i samma översyn. Skillnaden skattas med fasta effekter per översyn.
#      Urvalet av nästan tillagda kommer från kontrollgruppsarbetet (data/events/additions_and_near_additions_2007_2026.csv).
#   B. OMXS30 (G&S tabell 8, andra index): CAR [AD−1, ED+1] vid ändringar i OMXS30, tecknet vänt för borttag. OMXS30-händelser
#      som överlappar en OMXSB-händelse i samma aktie utesluts. Styrkan räckte inte 2 nov för att testa skillnaden mot OMXSB
#      (MDE 3,66 mot gränsen 3), så bara medelvärden med intervall redovisas, som då.
# Panelen ställs upp som i runda 3: Nordea och Tieto från LSEG:s separata hämtning, dagsavkastningar över 1 000 % stryks,
# börsvärdet fylls framåt högst 10 dagar.
# Inferens: som tabell 1 (klustrat per översyn, restriktiv wild cluster bootstrap, 9 999 dragningar). OMXS30 klustras per beskedsdag.
# Körs från thesis_final: python3 code/12_issuance_and_omxs30.py
import os, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'other_tests'

SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg12'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, lin, stars, tdist, cal, pos, mkt, GS_UTE = g['np'], g['pd'], g['lin'], g['stars'], g['tdist'], g['cal'], g['pos'], g['mkt'], g['GS_UTE']
exec(open(ROOT / 'code' / 'panel_runda3.py', encoding='utf-8').read())   # px, RET, wsum3, CLOSE, mc, SH, root, nextpos
os.makedirs(OUT, exist_ok=True)
CMP = DATA / 'comparison'
PERS = ['2007–11', '2012–16', '2017–21', '2022–26']
PER = lambda y: PERS[0] if y <= 2011 else (PERS[1] if y <= 2016 else (PERS[2] if y <= 2021 else PERS[3]))
rows, avvik = [], []
def rec(test, rad, r, **kw):
    rows.append(dict(test=test, rad=rad, **{k: r.get(k, np.nan) for k in ['b', 'lo', 'hi', 'lo_cr1', 'hi_cr1', 'p_wcb', 'p_cr1', 'n', 'G']}, **kw))
def jfr(namn, nytt, gammalt, tol=1e-6):
    d = abs(float(nytt) - float(gammalt))
    if not d <= tol: avvik.append(f'{namn}: nu {float(nytt):.6f}, då {float(gammalt):.6f}')

# ---------- A. nyemissioner
ROOTS = {}
for c_ in CLOSE.columns: ROOTS.setdefault(root(c_), []).append(c_)
def har_kurs(o, i): return o in CLOSE and pd.notna(CLOSE[o].iloc[max(i - 5, 0):i + 1]).any()
def sh_at(o, i, lb=60):
    if o not in SH: return np.nan
    s = SH[o].iloc[max(i - lb, 0):i + 1].dropna(); return float(s.iloc[-1]) if len(s) and s.iloc[-1] > 0 else np.nan
def bolagsaktier(c, i):
    sy = [o for o in ROOTS.get(root(c), [c]) if har_kurs(o, i)]
    s = [sh_at(o, i, 60) for o in sy]; return sum(s) if sy and all(v > 0 for v in s) else np.nan
S5 = pd.read_csv(DATA / 'events' / 'additions_and_near_additions_2007_2026.csv'); S5 = S5[S5.type == 'addition'].copy()
S5['dlog'] = [100 * np.log(bolagsaktier(c, b + 60) / bolagsaktier(c, a - 5)) if b + 60 < len(cal) else np.nan for c, a, b in zip(S5.ric, S5.iA, S5.iE)]
S5['per'] = pd.to_datetime(S5.AD).dt.year.map(PER); S5 = S5.dropna(subset=['dlog'])
S5[['review', 'AD', 'type', 'event', 'ric', 'dlog', 'per']].to_csv(OUT / 'issuance_sample.csv', index=False)
FE = pd.get_dummies(S5.review).astype(float).values; X = np.column_stack([S5.event.values, FE]); c = np.zeros(X.shape[1]); c[0] = 1
rec('A nyemissioner', 'tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter)', lin(X, S5.dlog.values, S5.review.values, c))
OLDF = pd.read_csv(CMP / 'previous_run_issuance.csv')
jfr('A skillnad', rows[-1]['b'], OLDF[OLDF.del_.str.startswith('tillägg minus')].b.iloc[0]); jfr('A antal', rows[-1]['n'], OLDF[OLDF.del_.str.startswith('tillägg minus')].n.iloc[0])
for p_ in PERS:
    for ev_, gr in S5[S5.per == p_].groupby('event'):
        namn = 'tillägg' if ev_ else 'nästan tillagda'
        rows.append(dict(test='A nyemissioner', rad=f'{p_}: {namn}, medel (%)', b=gr.dlog.mean(), n=len(gr), andel_over_1=(gr.dlog > 1).mean(), andel_over_5=(gr.dlog > 5).mean()))
        o = OLDF[(OLDF.del_ == p_) & (OLDF.grupp == namn)]; jfr(f'A {p_} {namn}', gr.dlog.mean(), o.b.iloc[0]); jfr(f'A {p_} {namn} antal', len(gr), o.n.iloc[0])

# ---------- B. OMXS30
ev_alla = g['ev_alla'].copy(); ev_alla['iAD'] = ev_alla.AD.map(pos); ev_alla['iED'] = ev_alla.ED.map(pos)
FL = pd.read_csv(DATA / 'events' / 'omxsb_deletion_flags_2007_2026.csv'); FLAGGED = set(FL[FL.flagged.astype(bool)].event_id)
I8 = pd.read_csv(DATA / 'funds' / 'fund_holdings_request_list.csv'); I8 = I8[I8.kind == 'event'].copy()
I8['AD'] = pd.to_datetime(I8.AD); I8['ED'] = pd.to_datetime(I8.ED); O = I8[I8.event_id.str.startswith('OMXS30')].copy()
def t28(ute):
    OB = ev_alla.dropna(subset=['iAD', 'iED']); OB = OB[~OB.event_id.isin(ute)]; logg, r_ = [], []
    for x in O.itertuples():
        if x.event_id == 'OMXS30-E040': logg.append((x.event_id, 'utesluten: fel aktieslag (Nasdaq anger A)')); continue
        iA, iE = nextpos(x.AD), nextpos(x.ED)
        if x.ric not in CI: logg.append((x.event_id, 'utesluten: RIC saknas i panelen')); continue
        ov = OB[(OB.RIC == x.ric) & (OB.iAD - 1 <= iE + 1) & (OB.iED + 1 >= iA - 1)]
        if len(ov): logg.append((x.event_id, 'utesluten: överlapp med ' + ','.join(ov.event_id))); continue
        car = wsum3(x.ric, iA - 1, iE + 1)
        if np.isnan(car): logg.append((x.event_id, 'utesluten: saknade kurser i fönstret')); continue
        r_.append(dict(event_id=x.event_id, index='OMXS30', typ=x.type, ric=x.ric, AD=x.AD, ED=x.ED, kluster='OMXS30 ' + str(x.AD.date()), car=car, y=(1 if x.type == 'addition' else -1) * car))
    for x in OB.itertuples():
        car = wsum3(x.RIC, int(x.iAD) - 1, int(x.iED) + 1)
        if np.isnan(car): continue
        r_.append(dict(event_id=x.event_id, index='OMXSB', typ=x.type, ric=x.RIC, AD=x.AD, ED=x.ED, kluster=x.review_cycle, car=car, y=(1 if x.type == 'addition' else -1) * car))
    return pd.DataFrame(r_), logg
OLD30 = pd.read_csv(CMP / 'previous_run_omxs30.csv').set_index('test')
for urv, ute in [('tabell 1 (10 borttag ute)', GS_UTE), ('som 2 nov (19 flaggade borttag ute)', FLAGGED)]:
    T, logg = t28(ute)
    if urv.startswith('tabell 1'):
        T.to_csv(OUT / 'omxs30_events.csv', index=False); pd.DataFrame(logg, columns=['event_id', 'orsak']).to_csv(OUT / 'omxs30_excluded.csv', index=False)
    for ix_ in ['OMXS30', 'OMXSB']:
        for ty in ['addition', 'deletion', 'alla']:
            s = T[(T['index'] == ix_) & ((T.typ == ty) | (ty == 'alla'))]
            rec('B OMXS30', f'{ix_}, {ty}: CAR [AD−1, ED+1], tecken vänt för borttag (%)', lin(np.ones((len(s), 1)), s.y.values, s.kluster.values, [1.0]), urval=urv)
            if urv.startswith('som 2 nov'):
                o = OLD30.loc[f'medel {ix_} {ty}']; jfr(f'B {ix_} {ty}', rows[-1]['b'], o.b); jfr(f'B {ix_} {ty} antal', rows[-1]['n'], o.n); jfr(f'B {ix_} {ty} undre CR1', rows[-1]['lo_cr1'], o.lo, 1e-4)
    # styrkan för skillnaden OMXS30 minus OMXSB (bara SE och MDE, ingen skattning redovisas om MDE > 3)
    Xd = np.column_stack([(T['index'] == 'OMXS30').astype(float).values, np.ones(len(T))]); rd = lin(Xd, T.y.values, T.kluster.values, [1.0, 0.0])
    mde = (tdist.ppf(.975, rd['G'] - 1) + tdist.ppf(.80, rd['G'] - 1)) * rd['se']
    rows.append(dict(test='B OMXS30', rad='styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3', b=mde, n=rd['n'], G=rd['G'], urval=urv))
    if urv.startswith('som 2 nov'): jfr('B MDE', mde, 3.6641882791824054, 1e-3)

R = pd.DataFrame(rows); R.to_csv(OUT / 'issuance_omxs30_results.csv', index=False)
f = lambda v, d=2: '' if pd.isna(v) else f'{v:.{d}f}'.replace('-', '−')
with open(OUT / 'ISSUANCE_OMXS30.md', 'w', encoding='utf-8') as fh:
    fh.write('# Steg 12: nyemissioner och OMXS30\n\nFlyttat från `runda11.py` (del F) och `runda10.py` (T28), körda 2 nov 2026, metoden oförändrad.\n\n')
    fh.write('## Jämförelse med körningen 2 november\n\n' + ('Alla jämförda siffror är desamma.\n\n' if not avvik else 'Avvikelser:\n\n' + '\n'.join('- ' + a for a in avvik) + '\n\n'))
    fh.write('## A. Nyemissioner: förändring i log antal aktier, AD−5 till ED+60 (G&S avsnitt 2.4.3)\n\n| Rad | Medel (%) | 95 % intervall | p | N | Andel över 1 % | Andel över 5 % |\n|---|---|---|---|---|---|---|\n')
    for r in R[R.test == 'A nyemissioner'].itertuples():
        fh.write(f'| {r.rad} | {f(r.b)}{stars(r.p_wcb) if pd.notna(r.p_wcb) else ""} | {f(r.lo) + " till " + f(r.hi) if pd.notna(r.lo) else ""} | {f(r.p_wcb, 3)} | {int(r.n)} | {f(r.andel_over_1)} | {f(r.andel_over_5)} |\n')
    fh.write('\n## B. OMXS30 jämfört med OMXSB (G&S tabell 8)\n\n| Urval | Rad | Medel | 95 % intervall | N | Kluster |\n|---|---|---|---|---|---|\n')
    for r in R[R.test == 'B OMXS30'].itertuples():
        fh.write(f'| {r.urval} | {r.rad} | {f(r.b)} | {f(r.lo) + " till " + f(r.hi) if pd.notna(r.lo) else ""} | {int(r.n)} | {int(r.G)} |\n')
    fh.write('\nStyrkan räcker inte för att testa skillnaden mellan indexen (MDE över gränsen 3 procentenheter). Därför redovisas bara medelvärden.\n')
print('Metod: klustrat per översyn (OMXS30 per beskedsdag), restriktiv wild cluster bootstrap (9 999 dragningar)')
print('jämförelse med 2 nov:', 'inga avvikelser' if not avvik else avvik)
print(R.to_string())
