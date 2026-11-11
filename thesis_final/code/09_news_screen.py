# Robusthet: tabell 1 utan händelser med egen bolagsnyhet i fönstret [AD−1, ED+1].
# Regeln är deklarerad i declarations/news_screen_declaration.md innan genomgången gjordes.
# Läser data/events/news_screen_extreme_events.csv (en rad per händelse med |CAR| > 20 %, kolumnen contaminated = ja/nej/oklart).
# Skriver results/news_screen/news_screen_results.csv och results/news_screen/REASONS.md.
# Körs från thesis_final: python3 code/09_news_screen.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'news_screen'; os.makedirs(OUT, exist_ok=True)

# samma inferens som 01_effect_table.py: kör filens första del (funktionerna och händelserna), inte tabellerna
SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'news_screen'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, lin, stars, ev = g['np'], g['pd'], g['lin'], g['stars'], g['ev']
ev = ev[ev.tot.notna()].copy()

N = pd.read_csv(DATA / 'events' / 'news_screen_extreme_events.csv', dtype=str).fillna('')
N['contaminated'] = N.contaminated.str.strip().str.lower()
assert N.contaminated.isin(['ja', 'nej', 'oklart']).all(), 'contaminated måste vara ja, nej eller oklart'
assert N.event_id.isin(ev.event_id).all(), 'okänt event_id i news_screen_extreme_events.csv'
ut = set(N.loc[N.contaminated == 'ja', 'event_id'])

PERS = ['2007–2011', '2012–2016', '2017–2021', '2022–2026']
rows = []
for v, d0 in {'Alla (tabell 1)': ev, 'Utan egen bolagsnyhet': ev[~ev.event_id.isin(ut)]}.items():
    for ty in ['addition', 'deletion']:
        d = d0[d0.type == ty]
        for lab, q in [('2007–11', d.period == '2007–2011'), ('2017–21', d.period == '2017–2021'),
                       ('2022–26', d.period == '2022–2026'), ('2017–26', d.ar >= 2017)]:
            x = d[q]
            rows.append(dict(variant=v, typ=ty, test=lab, **lin(np.ones((len(x), 1)), x.tot.values, x.review_cycle.values, [1.])))
        X = np.column_stack([(d.period == p).astype(float).values for p in PERS])
        for lab, c in [('2022–26 minus 2007–11', [-1, 0, 0, 1]), ('2022–26 minus 2017–21', [0, 0, -1, 1])]:
            rows.append(dict(variant=v, typ=ty, test=lab, **lin(X, d.tot.values, d.review_cycle.values, c)))
# samma perioder som tabell 2 (11 nov 2026): 2012–16, 2007–16 och decennieskillnaden. Läggs efter de deklarerade testerna så att
# deras dragningar inte flyttas. Se tillägget i declarations/news_screen_declaration.md.
for v, d0 in {'Alla (tabell 1)': ev, 'Utan egen bolagsnyhet': ev[~ev.event_id.isin(ut)]}.items():
    for ty in ['addition', 'deletion']:
        d = d0[d0.type == ty]
        for lab, q in [('2012–16', d.period == '2012–2016'), ('2007–16', d.ar <= 2016)]:
            x = d[q]
            rows.append(dict(variant=v, typ=ty, test=lab, **lin(np.ones((len(x), 1)), x.tot.values, x.review_cycle.values, [1.])))
        X = np.column_stack([np.ones(len(d)), (d.ar >= 2017).astype(float).values])
        rows.append(dict(variant=v, typ=ty, test='2017–26 minus 2007–16', **lin(X, d.tot.values, d.review_cycle.values, [0, 1])))
R = pd.DataFrame(rows); R['stars'] = R.p_wcb.map(stars)
R.to_csv(OUT / 'news_screen_results.csv', index=False)

# REASONS.md: vilka som togs bort och varför, sedan resultaten sida vid sida
L = ['# Händelser med egen bolagsnyhet i fönstret', '',
     f'Genomgångna: {len(N)} händelser med |CAR| > 20 %. Borttagna: {len(ut)}. Oklara (behålls): {(N.contaminated == "oklart").sum()}.', '',
     '| Händelse | Bolag | Typ | CAR % | Bedömning | Nyhetens datum | Kategori | Nyhet eller vad som kontrollerades | Källa |', '|---|---|---|---|---|---|---|---|---|']
for r in N.sort_values('contaminated').itertuples():
    car = ev.loc[ev.event_id == r.event_id, 'tot'].iloc[0]
    L.append(f'| {r.event_id} | {r.company} | {r.type} | {car:.1f} | {r.contaminated} | {r.news_date} | {r.category} | {r.headline} | {r.source_url} |')
L += ['', '## Resultat', '', 'Effekt i procent, p från wild cluster bootstrap.', '']
for ty in ['addition', 'deletion']:
    t = R[R.typ == ty].assign(cell=lambda d: d.apply(lambda r: f'{r.b:.2f}{r.stars} (p {r.p_wcb:.3f}, n {r.n})', axis=1))
    p = t.pivot(index='test', columns='variant', values='cell').reindex(
        ['2007–11', '2012–16', '2017–21', '2022–26', '2007–16', '2017–26', '2017–26 minus 2007–16', '2022–26 minus 2007–11', '2022–26 minus 2017–21'])
    L += [f'**{"Tillägg" if ty == "addition" else "Borttag"}**', '', '| Test | ' + ' | '.join(p.columns) + ' |', '|---' * (len(p.columns) + 1) + '|']
    L += [f'| {i} | ' + ' | '.join(p.loc[i]) + ' |' for i in p.index] + ['']
(OUT / 'REASONS.md').write_text('\n'.join(L), encoding='utf-8')
print('\n'.join(L))
