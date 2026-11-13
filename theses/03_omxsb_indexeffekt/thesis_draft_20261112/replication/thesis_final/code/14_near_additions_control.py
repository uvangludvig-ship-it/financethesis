# Steg 14: tillägg och borttag mot nästan tillagda och nästan borttagna (T5v). Flyttat från code/claude_checks/runda2.py
# (T5v, deklarerat i runda2_deklaration.md), metoden oförändrad. Deklaration för flytten: declarations/step13_16_declaration.md.
#   Urvalet byggdes i runda 2 och ligger i data/events/additions_and_near_additions_2007_2026.csv: per översyn tilläggen (event = 1)
#   och de aktier utanför OMXSB som var minst lika stora som det minsta tillägget (nästan tillagda, event = 0); för borttag
#   borttagen och de medlemmar som var högst lika stora som det största borttaget. ru = uppgång [AD−100, AD−1], lm = log börsvärde.
#   Regression: car_ED+1 (CAR [AD−1, ED+1]) på event, ru, lm och fasta effekter per översyn, klustrat per översyn,
#   per typ och före (beskedet före 2017) eller efter. Skattningen är koefficienten för event.
#   Känslighet: bara nästan tillagda på huvudlistan (mic == XSTO).
#   Borttag på två urval: utan de 10 som G&S regel utesluter (matchas på översyn och RIC), och alla (som runda 2).
# Inferens: lin() från 01 (restriktiv wild cluster bootstrap per översyn, intervall genom testinversion). Runda 2 hade analytiska
# intervall och en annan dragning, så p och intervall kan skilja sig; skattning och antal ska vara desamma.
# Körs från thesis_final: python3 code/14_near_additions_control.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'near_additions'

SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg14'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, lin, stars, ev_alla, GS_UTE = g['np'], g['pd'], g['lin'], g['stars'], g['ev_alla'], g['GS_UTE']
os.makedirs(OUT, exist_ok=True)
rows, avvik = [], []
def jfr(namn, nytt, gammalt, tol=1e-4):
    if not abs(float(nytt) - float(gammalt)) <= tol: avvik.append(f'{namn}: nu {float(nytt):.6f}, då {float(gammalt):.6f}')

S5 = pd.read_csv(DATA / 'events' / 'additions_and_near_additions_2007_2026.csv', parse_dates=['AD'])
UT = set(zip(ev_alla[ev_alla.event_id.isin(GS_UTE)].review_cycle, ev_alla[ev_alla.event_id.isin(GS_UTE)].RIC))
S5['gs_ute'] = [(r, c) in UT and e == 1 and t == 'deletion' for r, c, e, t in zip(S5.review, S5.ric, S5.event, S5.type)]
assert S5.gs_ute.sum() <= len(GS_UTE)
def reg(s):
    """Som reg() i runda 2: X = [event, ru, lm, fasta effekter per översyn]; kolumner utan variation efter att saknade rader
    tagits bort faller bort (som wcr() i runda 2), så att antalet parametrar och därmed CR1-justeringen blir densamma."""
    y = s['car_ED+1'].values.astype(float)
    X = np.column_stack([s.event.values.astype(float), s.ru.values, s.lm.values, pd.get_dummies(s.review).astype(float).values])
    ok = np.isfinite(y) & np.isfinite(X).all(1); X, y, gr = X[ok], y[ok], s.review.values[ok]
    keep = X.std(0) > 0; keep[0] = True; X = X[:, keep]
    c = np.zeros(X.shape[1]); c[0] = 1
    return lin(X, y, gr, c), int((X[:, 0] == 1).sum()), int((X[:, 0] == 0).sum())
PER = {'före': 0, 'efter': 1}
for ty, urvalen in [('addition', ['alla']), ('deletion', ['utan de 10 (G&S regel)', 'alla'])]:
    for urv in urvalen:
        for pn, pv in PER.items():
            s = S5[(S5.type == ty) & (S5.post == pv)]
            if urv.startswith('utan'): s = s[~s.gs_ute]
            q = s.dropna(subset=['car_ED+1'])
            for variant, x in [('CAR [AD-1,ED+1] mot nästan', q), ('känslighet: bara huvudlistan (XSTO) bland nästan', q[(q.event == 1) | (q.mic == 'XSTO')])]:
                r, ne, nn = reg(x)
                rows.append(dict(typ=ty, urval=urv, period=pn, variant=variant, handelser=ne, nastan=nn, **r))
R = pd.DataFrame(rows); R.to_csv(OUT / 'near_additions_results.csv', index=False)

# jämförelse med runda 2 (alla borttag, som då)
PR = pd.read_csv(DATA / 'comparison' / 'previous_run_near_additions.csv')
for o in PR.itertuples():
    n = R[(R.typ == o.typ) & (R.urval == 'alla') & (R.period == o.period) & (R.variant == o.variant)].iloc[0]
    jfr(f'{o.typ} {o.period} {o.variant}: skattning', n.b, o.skattning); jfr(f'{o.typ} {o.period} {o.variant}: N', n.n, o.N, 0)
    jfr(f'{o.typ} {o.period} {o.variant}: översyner', n.G, o.G, 0)
    jfr(f'{o.typ} {o.period} {o.variant}: analytiskt intervall, undre', n.lo_cr1, o.ci_lo); jfr(f'{o.typ} {o.period} {o.variant}: analytiskt intervall, övre', n.hi_cr1, o.ci_hi)

f = lambda v, d=2: '' if pd.isna(v) else ('∞' if v == np.inf else '−∞' if v == -np.inf else f'{v:.{d}f}'.replace('-', '−'))
L = ['# Steg 14: tillägg och borttag mot nästan tillagda (T5v)', '', 'Flyttat från `runda2.py` (T5v), metoden oförändrad. Före = beskedet före 2017.', '',
     '## Jämförelse med runda 2 (alla borttag)', '', 'Alla jämförda siffror är desamma (skattning, antal, översyner och analytiskt intervall).' if not avvik else 'Avvikelser:\n\n' + '\n'.join('- ' + a for a in avvik), '',
     '## Resultat: koefficienten för händelse (procentenheter CAR [AD−1, ED+1])', '', '| Typ | Urval | Period | Variant | Skattning | 95 % intervall | p | N | Händelser | Nästan | Översyner |', '|---|---|---|---|---|---|---|---|---|---|---|']
for r in R.itertuples():
    L.append(f'| {r.typ} | {r.urval} | {r.period} | {r.variant} | {f(r.b)}{stars(r.p_wcb)} | {f(r.lo)} till {f(r.hi)} | {f(r.p_wcb, 3)} | {r.n} | {r.handelser} | {r.nastan} | {r.G} |')
(OUT / 'NEAR_ADDITIONS.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('\n'.join(L))
print('Metod: klustrat per översyn, restriktiv wild cluster bootstrap (intervall genom testinversion), fasta effekter per översyn')
print('jämförelse med runda 2:', 'inga avvikelser' if not avvik else avvik)
