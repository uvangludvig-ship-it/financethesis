# Steg 15: återgång efter ändringen. Port av code/claude_checks/del1.py med lin(). Deklaration för flytten:
# declarations/step13_16_declaration.md.
#   car_e10 = CAR [ED, ED+10], car_e20 = CAR [ED, ED+20], runup = uppgången [AD, ED−1], alla och per period (period som i tabell 1).
#   Återgångsandel över 20 dagar = −medel(car_e20) / medel(runup) på händelser med båda.
#   Tillägg på ev_alla (tilläggen påverkas inte av urvalsregeln). Borttag på två urval: utan de 10 (G&S regel, som tabell 1) och
#   alla (det gamla urvalet, som del1.py).
# Inferens: lin() från 01 (medel, klustrat per översyn, restriktiv wild cluster bootstrap, intervall genom testinversion).
# del1.py hade teckenbyte per beskedsdag och en egen wild bootstrap; skattning och antal ska vara desamma, p kan skilja sig.
# Körs från thesis_final: python3 code/15_reversal.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'reversal'

SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg15'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, lin, stars, ev_alla, GS_UTE, wsum, pos = g['np'], g['pd'], g['lin'], g['stars'], g['ev_alla'], g['GS_UTE'], g['wsum'], g['pos']
os.makedirs(OUT, exist_ok=True)
rows, avvik = [], []
def jfr(namn, nytt, gammalt, tol=5e-4):
    if not abs(float(nytt) - float(gammalt)) <= tol: avvik.append(f'{namn}: nu {float(nytt):.6f}, då {float(gammalt):.6f}')

E = ev_alla.copy(); E['iAD'] = E.AD.map(pos); E['iED'] = E.ED.map(pos)
E['car_e10'] = [wsum(r, e, e + 10) for r, e in zip(E.RIC, E.iED)]
E['car_e20'] = [wsum(r, e, e + 20) for r, e in zip(E.RIC, E.iED)]
E['runup'] = [wsum(r, a, e - 1) for r, a, e in zip(E.RIC, E.iAD, E.iED)]
E['gs_ute'] = E.event_id.isin(GS_UTE)
MATT = ['car_e10', 'car_e20', 'runup']
PERS = ['all'] + sorted(E.period.dropna().unique())
URVAL = [('addition', 'alla', E[E.type == 'addition']), ('deletion', 'utan de 10 (G&S regel)', E[(E.type == 'deletion') & ~E.gs_ute]),
         ('deletion', 'alla', E[E.type == 'deletion'])]
for ty, urv, s0 in URVAL:
    for p in PERS:
        s = s0 if p == 'all' else s0[s0.period == p]
        for v in MATT:
            x = s[s[v].notna()]
            rows.append(dict(typ=ty, urval=urv, period=p, matt=v, review_mean=float(x.groupby('review_cycle')[v].mean().mean()),
                             **lin(np.ones((len(x), 1)), x[v].values, x.review_cycle.values, [1.])))
    ok = s0.car_e20.notna() & s0.runup.notna()
    rows.append(dict(typ=ty, urval=urv, period='all', matt='återgångsandel 20 dagar', b=float(-s0[ok].car_e20.mean() / s0[ok].runup.mean()), n=int(ok.sum()),
                     ci_metod='beskrivande, ingen inferens', p_metod='inget p'))
R = pd.DataFrame(rows); R.to_csv(OUT / 'reversal_results.csv', index=False)
E.to_csv(OUT / 'reversal_events.csv', index=False)

# jämförelse med del1.py (tillägg och alla borttag, som då)
PR = pd.read_csv(DATA / 'comparison' / 'previous_run_reversal.csv')
for o in PR.itertuples():
    n = R[(R.typ == o.type) & (R.urval == 'alla') & (R.period == o.period) & (R.matt == o.measure)].iloc[0]
    jfr(f'{o.type} {o.period} {o.measure}: händelsemedel', n.b, o.event_mean); jfr(f'{o.type} {o.period} {o.measure}: medel per översyn', n.review_mean, o.review_mean)
    jfr(f'{o.type} {o.period} {o.measure}: N', n.n, o.N, 0); jfr(f'{o.type} {o.period} {o.measure}: kluster', n.G, o.G, 0)

f = lambda v, d=2: '' if pd.isna(v) else ('∞' if v == np.inf else '−∞' if v == -np.inf else f'{v:.{d}f}'.replace('-', '−'))
NAMN = {'car_e10': 'CAR [ED, ED+10]', 'car_e20': 'CAR [ED, ED+20]', 'runup': 'Uppgång [AD, ED−1]'}
L = ['# Steg 15: återgång efter ändringen', '', 'Port av `del1.py` med `lin()`. Medel i procent; borttag med eget tecken.', '',
     '## Jämförelse med del1.py (tillägg och alla borttag)', '', 'Alla jämförda siffror är desamma (händelsemedel, medel per översyn, N och kluster).' if not avvik else 'Avvikelser:\n\n' + '\n'.join('- ' + a for a in avvik), '',
     '## Resultat', '', '| Typ | Urval | Period | Mått | Medel | 95 % intervall | p | N | Översyner |', '|---|---|---|---|---|---|---|---|---|']
for r in R[R.matt.isin(MATT)].itertuples():
    L.append(f'| {r.typ} | {r.urval} | {r.period} | {NAMN[r.matt]} | {f(r.b)}{stars(r.p_wcb)} | {f(r.lo)} till {f(r.hi)} | {f(r.p_wcb, 3)} | {int(r.n)} | {int(r.G)} |')
L += ['', '## Återgångsandel över 20 dagar (−CAR [ED, ED+20] / uppgång [AD, ED−1])', '']
for r in R[R.matt == 'återgångsandel 20 dagar'].itertuples():
    L.append(f'- {r.typ}, {r.urval}: {100 * r.b:.0f} % (N {int(r.n)})')
(OUT / 'REVERSAL.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('\n'.join(L))
print('Metod: medel klustrat per översyn, restriktiv wild cluster bootstrap (intervall genom testinversion); återgångsandelen beskrivande')
print('jämförelse med del1.py:', 'inga avvikelser' if not avvik else avvik)
