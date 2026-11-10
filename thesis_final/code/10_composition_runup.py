# Metod 5.3 och 5.4: G&S tabell 2 (CAR på periodkonstanter, utan och med kontroller) och tabell 4 (uppgång före beskedet),
# kursbanan AD−100 till AD+14 (G&S figur 7), samt M-regressionen (5.5) utan kontroller på samma händelser som med kontroller.
# Deklarationer: declarations/step10_declaration.md (10 nov 2026, 17:11) och declarations/sample_rule_declaration.md (17:21).
# Urval: samma som tabell 1 (returns.py: alla händelser utom 10 borttag enligt G&S regel). Perioder efter ändringsåret, som 01.
# Kontrollerna k_oms (onormal omsättning [AD−21, AD−1]), k_storlek (andel av OMXSB:s börsvärde vid AD−1), k_wz (residualvarians
# mot OMXSBGI över [AD−250, AD−2]) och k_ana (prognoser månaden före AD) räknades i runda 11 och hämtas ur
# data/events/omxsb_changes_corrected_2007_2026.csv. De 9 borttag som bara har ändrat aktieantal finns inte i den filen och
# saknar därför kontroller; de är med i raden utan kontroller och faller bort i de andra. Fönstren före beskedet räknas här ur kurserna.
# Tre rader per typ: utan kontroller (= tabell 1), med kontroller, och utan kontroller på samma händelser som med.
# Inferens som tabell 1: klustrat per översyn, restriktiv wild cluster bootstrap (9 999 dragningar), intervall genom testinversion.
# Körs från thesis_final efter 02: python3 code/10_composition_runup.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'composition'

# lin(), händelserna och CAR från 01, så att urval och inferens är exakt desamma
SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg10'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, lin, stars, ev, wsum = g['np'], g['pd'], g['lin'], g['stars'], g['ev'], g['wsum']
os.makedirs(OUT, exist_ok=True)

PERS = ['2007–11', '2012–16', '2017–21', '2022–26']
KC = ['k_oms', 'k_storlek', 'k_wz', 'k_ana']
NAMN = {'k_oms': 'onormal omsättning', 'k_storlek': 'relativ storlek', 'k_wz': 'arbitragerisk', 'k_ana': 'analytiker'}
PRE = [10, 20, 50, 100]
K = pd.read_csv(DATA / 'events' / 'omxsb_changes_corrected_2007_2026.csv')[['event_id'] + KC]
E = ev.merge(K, on='event_id', how='left')
for n_ in PRE: E[f'pre{n_}'] = [wsum(r_, int(a) - n_, int(a) - 1) for r_, a in zip(E.RIC, E.iAD)]   # räknas här, samma urval som tabell 1
E['car_tot'] = E.tot; E['review'] = E.review_cycle; E['per'] = E.period.str[:5] + E.period.str[-2:]
assert set(E.per) == set(PERS), set(E.per)
rows = []
def rec(tabell, typ, variant, rad, r):
    rows.append(dict(tabell=tabell, typ=typ, variant=variant, rad=rad, **{k: r[k] for k in ['b', 'lo', 'hi', 'lo_cr1', 'hi_cr1', 'p_wcb', 'p_cr1', 'n', 'G', 'ci_metod', 'p_metod']}))

# tabell 2 (5.3)
for ty in ['addition', 'deletion']:
    alla = E[(E.type == ty) & E.car_tot.notna()]
    med_k = alla.dropna(subset=KC)
    for variant, s, kontroller in [('utan kontroller', alla, False), ('med kontroller', med_k, True),
                                   ('utan kontroller, samma händelser som med', med_k, False)]:
        s = s.copy()
        if kontroller:
            for c in KC: s[c] = s[c] - s[c].mean()
        X = np.column_stack([(s.per == p).astype(float).values for p in PERS] + ([s[c].values for c in KC] if kontroller else []))
        for j, p in enumerate(PERS):
            c = np.zeros(X.shape[1]); c[j] = 1; rec('tabell 2', ty, variant, p, lin(X, s.car_tot.values, s.review.values, c))
        c = np.zeros(X.shape[1]); c[0], c[3] = 1, -1; rec('tabell 2', ty, variant, '2007–11 minus 2022–26', lin(X, s.car_tot.values, s.review.values, c))
        if kontroller:
            for j, k in enumerate(KC):
                c = np.zeros(X.shape[1]); c[4 + j] = 1; rec('tabell 2', ty, variant, 'koefficient: ' + NAMN[k], lin(X, s.car_tot.values, s.review.values, c))

# tabell 4 (5.4)
for ty in ['addition', 'deletion']:
    for p in PERS:
        for n_ in PRE:
            s = E[(E.type == ty) & (E.per == p) & E[f'pre{n_}'].notna()]
            rec('tabell 4', ty, f'[AD−{n_}, AD−1]', p, lin(np.ones((len(s), 1)), s[f'pre{n_}'].values, s.review.values, [1.0]))

# M-regressionen (5.5, tabell 6 i 02) utan kontroller på samma händelser som med kontroller. 02 rörs inte.
H = pd.read_csv(RES / 'fund_demand' / 'handelser_omraknade.csv'); H['split'] = H.split.astype(bool)
R6 = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv'); R6 = R6[(R6.tabell.astype(str) == '6') & (R6.skikt == 'D_V')]
for ty in ['addition', 'deletion']:
    for yc, fn in [('y_tot', '[AD−1, ED+1]'), ('y_lang', '[AD−20, ED+1]')]:
        s = H[(H.type == ty) & ~H.split & H.D_V.notna() & H[yc].notna()].dropna(subset=KC).copy()
        for kontroller in [True, False]:
            sk = s.copy()
            if kontroller:
                for c in KC: sk[c] = sk[c] - sk[c].mean()
            Db = sk.groupby('per').D_V.mean().reindex(PERS)
            X = np.column_stack([((sk.per == p).astype(float) * Db[p]).values for p in PERS] + ([sk[c].values for c in KC] if kontroller else []))
            v = 'med kontroller' if kontroller else 'utan kontroller, samma händelser som med'
            for j, p in enumerate(PERS):
                c = np.zeros(X.shape[1]); c[j] = 1; r = lin(X, sk[yc].values, sk.review.values, c)
                if kontroller:   # ska återskapa 02 exakt
                    b02 = R6[(R6.typ == ty) & (R6.fonster == yc) & (R6.kontroller.astype(str) == 'True') & (R6.period == f'M {p}')].b.iloc[0]
                    assert abs(r['b'] - b02) < 1e-8, (ty, yc, p, r['b'], b02)
                r['n'] = int((sk.per == p).sum()); rec('M ' + fn, ty, v, p, r)
            for a_, b_, lab in [(0, 3, '2007–11 minus 2022–26'), (2, 3, '2017–21 minus 2022–26')]:
                c = np.zeros(X.shape[1]); c[a_], c[b_] = 1, -1; rec('M ' + fn, ty, v, lab, lin(X, sk[yc].values, sk.review.values, c))

# kursbanan (G&S figur 7, runda 11 I): medel av kumulerad överavkastning från AD−100 till AD+k, k = −100 ... 14, per typ och period
f7 = []
for (ty, p), d in E.groupby(['type', 'per']):
    for kk in range(-100, 15):
        v = np.array([wsum(r_, int(a) - 100, int(a) + kk) for r_, a in zip(d.RIC, d.iAD)], float)
        f7.append(dict(typ=ty, period=p, dag=kk, car=np.nanmean(v), n=int(np.isfinite(v).sum())))
pd.DataFrame(f7).to_csv(OUT / 'figur7_kursbana.csv', index=False)

R = pd.DataFrame(rows); R.to_csv(OUT / 'tabell2_tabell4.csv', index=False)
cell = lambda r: f"{r.b:.2f}{stars(r.p_wcb)} ({r.lo:.2f} till {r.hi:.2f})"
L = ['# Metod 5.3, 5.4 och 5.5: G&S tabell 2 och tabell 4, och M på samma händelser', '',
     'CAR i procent mot OMXSBGI. 95 % intervall: invertering av restriktiv wild cluster bootstrap per översyn (9 999 dragningar); '
     'stjärnor från samma bootstrap. Analytiska CR1-intervall finns i tabell2_tabell4.csv.', '',
     '## Tabell 2: CAR [AD−1, ED+1] på periodkonstanter', '', '| Typ | Variant | N | ' + ' | '.join(PERS) + ' | 2007–11 minus 2022–26 | p |',
     '|---|---|---|' + '---|' * (len(PERS) + 2)]
for (ty, v), d in R[R.tabell == 'tabell 2'].groupby(['typ', 'variant'], sort=False):
    d = d.set_index('rad'); df = d.loc['2007–11 minus 2022–26']
    L.append(f'| {ty} | {v} | {int(df.n)} | ' + ' | '.join(cell(d.loc[p]) for p in PERS) + f' | {cell(df)} | {df.p_wcb:.3f} |')
L += ['', '## Tabell 2: kontrollernas koefficienter', '', '| Typ | ' + ' | '.join(NAMN.values()) + ' |', '|---|' + '---|' * 4]
for ty in ['addition', 'deletion']:
    d = R[(R.tabell == 'tabell 2') & (R.typ == ty) & R.rad.str.startswith('koefficient')].set_index('rad')
    L.append(f'| {ty} | ' + ' | '.join(f"{cell(d.loc['koefficient: ' + NAMN[k]])}, p {d.loc['koefficient: ' + NAMN[k]].p_wcb:.2f}" for k in KC) + ' |')
L += ['', '## Tabell 4: CAR [AD−n, AD−1], medel', '', '| Typ | Period | n = 10 | n = 20 | n = 50 | n = 100 |', '|---|---|---|---|---|---|']
for ty in ['addition', 'deletion']:
    for p in PERS:
        d = R[(R.tabell == 'tabell 4') & (R.typ == ty) & (R.rad == p)].set_index('variant')
        L.append(f'| {ty} | {p} | ' + ' | '.join(cell(d.loc[f'[AD−{n_}, AD−1]']) for n_ in PRE) + ' |')
L += ['', '## M (D_V) med kontroller och utan kontroller på samma händelser', '',
      '| Typ | Fönster | Variant | ' + ' | '.join(PERS) + ' | 2007–11 minus 2022–26 | 2017–21 minus 2022–26 |', '|---|---|---|' + '---|' * 6]
for (tb, ty, v), d in R[R.tabell.str.startswith('M ')].groupby(['tabell', 'typ', 'variant'], sort=False):
    d = d.set_index('rad')
    L.append(f'| {ty} | {tb[2:]} | {v} | ' + ' | '.join(f"{d.loc[p].b:.2f} (n {int(d.loc[p].n)})" for p in PERS) + ' | '
             + ' | '.join(f"{cell(d.loc[k])}, p {d.loc[k].p_wcb:.3f}" for k in ['2007–11 minus 2022–26', '2017–21 minus 2022–26']) + ' |')
(OUT / 'TABELL2_TABELL4.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('\n'.join(L))
