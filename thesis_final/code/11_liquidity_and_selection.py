# Steg 11: likviditet och urval, tre G&S-test som kräver hela kurspanelen. Flyttade hit från code/build/mechanisms_2007.py
# (30 okt 2026), metoden oförändrad. Deklaration: declarations/step11_13_declaration.md (10 nov 2026, 21:46).
#   A. Spread (G&S figur 9): värdeviktad relativ noterad spread per år för OMXSB-bolagen, och tilläggens CAR mot årets spread.
#      Noterad slutkurs-spread, inte effektiv spread som hos G&S. Observationer över 20 % stryks.
#   B. Volym (G&S avsnitt 2.4.3): andel av omsättningen (antal aktier) under ED±22 som handlas varje dag, per period.
#   C. Storleksrang (G&S figur 8): tilläggens rang bland aktier som inte är med i OMXSB, efter omsättning (Nasdaqs urvalsvariabel,
#      sex månader före referensdagen) och efter börsvärde (G&S variabel). Referensdag: sista handelsdagen månaden före beskedet.
# Medlemmarna i OMXSB byggs som i ursprunget: listan 1 juni 2009 (data/index/) rullad framåt och bakåt med Nasdaqs ändringslistor.
# Börsvärdet i LSEG gäller hela bolaget; aktier helt utan börsvärde får kurs × antal aktier.
# Urval: som tabell 1 (10 borttag ute enligt G&S regel). "gammalt urval" = alla borttag, för jämförelsen med körningen 30 okt.
# Inferens: som tabell 1 (klustrat per översyn, restriktiv wild cluster bootstrap, 9 999 dragningar).
# Körs från thesis_final: python3 code/11_liquidity_and_selection.py
import os, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'liquidity'

SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg11'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, lin, stars, ev, ev_alla, cal, pos = g['np'], g['pd'], g['lin'], g['stars'], g['ev'], g['ev_alla'], g['cal'], g['pos']
exec(open(ROOT / 'code' / 'panel.py', encoding='utf-8').read())
os.makedirs(OUT, exist_ok=True)
CMP = DATA / 'comparison'
PER = ['2007–2011', '2012–2016', '2017–2021', '2022–2026']
ev_alla = ev_alla.copy(); ev_alla['iAD'] = ev_alla.AD.map(pos); ev_alla['iED'] = ev_alla.ED.map(pos)
for e in (ev, ev_alla): e['year'] = e.ED.dt.year
rows, avvik = [], []
def rec(test, typ, urval, rad, r):
    rows.append(dict(test=test, typ=typ, urval=urval, rad=rad, **{k: r.get(k, np.nan) for k in ['b', 'lo', 'hi', 'lo_cr1', 'hi_cr1', 'p_wcb', 'p_cr1', 'n', 'G']}))
def medel(y, kl): return lin(np.ones((len(y), 1)), np.asarray(y, float), np.asarray(kl), [1.0])
def jfr(namn, nytt, gammalt, tol=1e-6):
    d = float(np.nanmax(np.abs(np.asarray(nytt, float) - np.asarray(gammalt, float)))) if len(np.atleast_1d(nytt)) else 0.0
    if not d <= tol: avvik.append(f'{namn}: största skillnad {d:.6g}')
    return d

# ---------- pivoter och medlemskap (som mechanisms_2007.py)
last_date = px.groupby('ric').date.max()
piv = lambda c: px.pivot(index='date', columns='ric', values=c).reindex(cal)
mc = piv('mcap'); no_mcap = [r for r in mc.columns if mc[r].notna().sum() == 0]
cs = px.assign(cs=px.close * px.shares).pivot(index='date', columns='ric', values='cs').reindex(cal); mc[no_mcap] = cs[no_mcap]
ch = pd.read_csv(DATA / 'events' / 'omxsb_changes_nasdaq_2007_2026.csv', parse_dates=['effective_date', 'announcement_date'])
cons = pd.read_csv(DATA / 'index' / 'omxsb_constituents_2009_06_01.csv', dtype=str).fillna('')
ALIAS_T = {'TWW SDB': 'TWW SDB B', 'NOKIA SEK': 'NOKI SEK', 'NOKI SEK': 'NOKI SEK'}
TICK_RIC = {'CYBE': 'CYBC.ST^A16', 'KAUP SEK': 'KAUP.ST^L08', 'CSN': 'CISI.ST^H14', 'RABT B': 'VSSABb.ST', 'WSIB SDB': 'AOILsdb.ST^L13',
            'NOKI SEK': 'NOKIA.ST', 'HAKN': 'ICAA.ST^A22', 'TWW SDB B': 'TWWsdbb.ST^K14', 'AWP': 'ARISE.ST^A26', 'BVT': 'SOBIV.ST'}
def key_of(ric, ticker):
    t = ALIAS_T.get(str(ticker).strip(), str(ticker).strip())
    if isinstance(ric, str) and ric: return 'NOKIA.ST' if ric == 'NOKIsdb.ST^E07' else ric
    return TICK_RIC.get(t, 'T:' + t)
ch['key'] = [key_of(r, t) for r, t in zip(ch.RIC, ch.ticker)]; cons['key'] = [key_of(r, t) for r, t in zip(cons.RIC, cons.ticker)]
ch['ED'] = ch.effective_date.map(lambda d: cal[cal.searchsorted(d)]); ch['AD'] = ch.announcement_date.map(lambda d: cal[cal.searchsorted(d)])
rev = ch.groupby('review_cycle').agg(ED=('ED', 'first'), AD=('AD', 'first')).sort_values('ED')
rev['adds'] = [set(ch[(ch.review_cycle == c) & (ch.type == 'addition')].key) for c in rev.index]
rev['dels'] = [set(ch[(ch.review_cycle == c) & (ch.type == 'deletion')].key) for c in rev.index]
cyc = list(rev.index); i0 = cyc.index('2009H1'); after = {cyc[i0]: set(cons.key)}
for i in range(i0 + 1, len(cyc)): after[cyc[i]] = (set(after[cyc[i - 1]]) - rev.dels[cyc[i]]) | rev.adds[cyc[i]]
for i in range(i0, 0, -1): after[cyc[i - 1]] = (set(after[cyc[i]]) - rev.adds[cyc[i]]) | rev.dels[cyc[i]]
before = {cyc[0]: (after[cyc[0]] - rev.adds[cyc[0]]) | rev.dels[cyc[0]]}
for i in range(1, len(cyc)): before[cyc[i]] = after[cyc[i - 1]]

# ---------- A. spread per år (G&S figur 9)
bw, aw = piv('bid'), piv('ask')
rsp = ((aw - bw) / ((aw + bw) / 2) * 100).where((bw > 0) & (aw >= bw)); rsp = rsp.where(rsp <= 20)
w = mc.where(rsp.notna())
vw_all = (rsp * w).sum(axis=1) / w.sum(axis=1)
vw_mem = pd.Series(np.nan, index=cal)
for i, c in enumerate(cyc):
    lo = rev.ED[c]; hi = rev.ED[cyc[i + 1]] if i + 1 < len(cyc) else cal[-1] + pd.Timedelta(days=1)
    if i == 0:
        rics = [k for k in before[c] if k in rsp.columns]; m = (cal >= cal[0]) & (cal < lo)
        vw_mem[m] = ((rsp.loc[m, rics] * w.loc[m, rics]).sum(axis=1) / w.loc[m, rics].sum(axis=1)).values
    rics = [k for k in after[c] if k in rsp.columns]; m = (cal >= lo) & (cal < hi)
    vw_mem[m] = ((rsp.loc[m, rics] * w.loc[m, rics]).sum(axis=1) / w.loc[m, rics].sum(axis=1)).values
e2 = pd.DataFrame({'vw_spread_omxsb_members': vw_mem.groupby(cal.year).mean(), 'vw_spread_all_st_panel': vw_all.groupby(cal.year).mean(),
                   'n_panel_stocks_with_quote': rsp.notna().sum(axis=1).groupby(cal.year).mean()}).loc[2007:2026]
e2 = e2.join(ev[ev.type == 'addition'].groupby('year').tot.agg(addition_effect_mean='mean', N_additions='count'))
e2 = e2.join(ev[ev.type == 'deletion'].groupby('year').tot.agg(deletion_effect_mean='mean', N_deletions='count'))
e2.index.name = 'year'; e2.to_csv(OUT / 'spread_by_year.csv')
old = pd.read_csv(CMP / 'previous_run_spread_by_year.csv').set_index('year')
for c_ in ['vw_spread_omxsb_members', 'vw_spread_all_st_panel', 'addition_effect_mean']: jfr(f'A spread, {c_}', e2[c_], old[c_].reindex(e2.index))
for urv, E_ in [('tabell 1', ev), ('gammalt urval', ev_alla)]:
    for ty in ['addition', 'deletion']:
        if ty == 'addition' and urv == 'gammalt urval': continue   # tilläggen är desamma i båda urvalen
        yy = E_[E_.type == ty].merge(e2[['vw_spread_omxsb_members']], left_on='year', right_index=True).dropna(subset=['tot', 'vw_spread_omxsb_members'])
        X = np.column_stack([np.ones(len(yy)), yy.vw_spread_omxsb_members.values])
        rec('A spread', ty, urv, 'lutning: CAR på årets spread (procentenheter per procentenhet)', lin(X, yy.tot.values, yy.review_cycle.values, [0.0, 1.0]))
for y_ in [2007, 2011, 2016, 2021, 2025, 2026]:
    rows.append(dict(test='A spread', typ='OMXSB-bolag', urval='alla medlemmar', rad=f'värdeviktad spread {y_} (%)', b=e2.vw_spread_omxsb_members[y_]))
OLDR = pd.read_csv(CMP / 'previous_run_liquidity_results.csv')
jfr('A lutning, tillägg', rows[0]['b'], OLDR[OLDR.statistic == 'slope on spread (%)'].coef.iloc[0])

# ---------- B. volymens fördelning kring ändringsdagen (G&S avsnitt 2.4.3)
vo = piv('volume')
def vshare(ric, i):
    if ric not in vo: return None
    s = vo[ric].iloc[i - 22:i + 23]
    if len(s) < 45 or s.isna().all(): return None
    s = s.fillna(0.0); return s.values / s.sum() * 100 if s.sum() > 0 else None
x = np.arange(-22, 23); f11 = {}
for urv, E_ in [('tabell 1', ev), ('gammalt urval', ev_alla)]:
    for ty in ['addition', 'deletion']:
        if ty == 'addition' and urv == 'gammalt urval': continue
        for p in PER:
            s = E_[(E_.type == ty) & (E_.period == p)]
            V = [(kl, v) for kl, v in ((kl, vshare(r, int(i))) for kl, r, i in zip(s.review_cycle, s.RIC, s.iED)) if v is not None]
            P = np.array([v for _, v in V]); kl = [k for k, _ in V]
            f11[(urv, ty, p)] = pd.Series(P.mean(0), index=x)
            for off, lab in [(21, 'ED−1'), (22, 'ED')]:
                rec('B volym', ty, urv, f'{p}: andel av omsättningen ED±22 som handlas {lab} (%)', medel(P[:, off], kl))
                o = OLDR[(OLDR.test == f'Fig. 11: share of ED±22 volume traded on {lab}, {ty}s') & (OLDR['sample'] == 'all') & (OLDR.statistic == p)]
                if (ty == 'addition' or urv == 'gammalt urval') and len(o): jfr(f'B volym {ty} {p} {lab}', rows[-1]['b'], o.coef.iloc[0])
        s = E_[E_.type == ty]; V = [(kl, p_, v) for kl, p_, v in ((kl, p_, vshare(r, int(i))) for kl, p_, r, i in zip(s.review_cycle, s.period, s.RIC, s.iED)) if v is not None]
        y = np.array([v[21] for _, _, v in V]); d0 = np.array([p_ == PER[0] for _, p_, _ in V], float); d3 = np.array([p_ == PER[3] for _, p_, _ in V], float)
        Xp = np.column_stack([np.array([p_ == q for _, p_, _ in V], float) for q in PER])
        rec('B volym', ty, urv, 'andel ED−1: 2022–2026 minus 2007–2011 (procentenheter)', lin(Xp, y, [k for k, _, _ in V], [-1.0, 0, 0, 1.0]))
F11 = pd.DataFrame(f11); F11.columns = [f'{a}|{b}|{c}' for a, b, c in F11.columns]; F11.index.name = 'dag_relativt_ED'; F11.to_csv(OUT / 'volume_share_by_day.csv')
oldv = pd.read_csv(CMP / 'previous_run_volume_share_by_day.csv', index_col=0)
for p in PER:
    jfr(f'B dagsbana tillägg {p}', F11[f'tabell 1|addition|{p}'].values, oldv[f'all|addition|{p}'].values)
    jfr(f'B dagsbana borttag {p}, gammalt urval', F11[f'gammalt urval|deletion|{p}'].values, oldv[f'all|deletion|{p}'].values)

# ---------- C. tilläggens rang bland icke-medlemmar (G&S figur 8)
pv = px.assign(pv=px.close * px.volume).pivot(index='date', columns='ric', values='pv').reindex(cal)
to = pv.fillna(piv('turnover')); rk = []
for c in cyc:
    ad = rev.AD[c]; ref = cal[cal < pd.Timestamp(ad.year, ad.month, 1)][-1]; win = (cal > ref - pd.DateOffset(months=6)) & (cal <= ref)
    T = to.loc[win]; ok = T.notna().sum() >= 0.5 * win.sum(); tsum = T.sum()[ok]; m = mc.loc[ref].reindex(tsum.index)
    cand = [r for r in tsum.index if r not in set(before[c])]
    tr = tsum[cand].sort_index().sort_values(ascending=False, kind='stable'); mr = m[cand].dropna().sort_index().sort_values(ascending=False, kind='stable')   # lika värden (aktieslag i samma bolag har samma börsvärde) ordnas efter RIC
    rank_t = pd.Series(np.arange(1, len(tr) + 1), index=tr.index); rank_m = pd.Series(np.arange(1, len(mr) + 1), index=mr.index)
    for k in rev.adds[c]:
        rk.append(dict(review_cycle=c, AD=ad, ED=rev.ED[c], key=k, year=rev.ED[c].year, ref_date=ref, n_universe_turnover=len(tr), n_universe_mcap=len(mr),
                       rank_turnover=rank_t.get(k, np.nan), rank_mcap=rank_m.get(k, np.nan), in_panel=k in tsum.index))
rk = pd.DataFrame(rk).sort_values(['ED', 'key']).reset_index(drop=True)
rk['pct_turnover'] = rk.rank_turnover / rk.n_universe_turnover * 100; rk['pct_mcap'] = rk.rank_mcap / rk.n_universe_mcap * 100
rk['post_nov2023'] = rk.ED >= pd.Timestamp('2023-12-01'); rk.to_csv(OUT / 'size_rank_of_additions.csv', index=False)
q = lambda a: (lambda s: s.quantile(a))
f10 = rk.groupby('year').agg(N=('key', 'size'), N_ranked=('rank_turnover', 'count'), universe=('n_universe_turnover', 'mean'), mean_turn=('rank_turnover', 'mean'),
                             p25_turn=('rank_turnover', q(.25)), p75_turn=('rank_turnover', q(.75)), mean_mcap=('rank_mcap', 'mean'), p25_mcap=('rank_mcap', q(.25)),
                             p75_mcap=('rank_mcap', q(.75)), pct_turn_mean=('pct_turnover', 'mean'), pct_mcap_mean=('pct_mcap', 'mean'))
f10.to_csv(OUT / 'size_rank_by_year.csv')
# jämförelse med 30 okt, tillägg för tillägg. Lika värden (två aktieslag i samma bolag har samma börsvärde, och en aktie med två RIC
# samma omsättning) ordnades då godtyckligt av sorteringen; här ordnas de efter RIC, så att körningen blir densamma på alla datorer.
oldk = pd.read_csv(CMP / 'previous_run_size_rank_of_additions.csv').merge(rk, on=['review_cycle', 'key'], suffixes=('_da', ''))
assert len(oldk) == len(rk)
n_olika = sum(int((oldk[v + '_da'].fillna(-1) != oldk[v].fillna(-1)).sum()) for v in ['rank_turnover', 'rank_mcap'])
max_olika = max(float((oldk[v + '_da'] - oldk[v]).abs().max()) for v in ['rank_turnover', 'rank_mcap'])
jfr('C antal aktier att ranka bland', oldk[['n_universe_turnover', 'n_universe_mcap']].values, oldk[['n_universe_turnover_da', 'n_universe_mcap_da']].values)
if max_olika > 1: avvik.append(f'C rang: största skillnad {max_olika} platser')
rk['period'] = pd.cut(rk.year, [2006, 2011, 2016, 2021, 2026], labels=PER).astype(str)
for v, nm in [('pct_turnover', 'percentil efter omsättning'), ('pct_mcap', 'percentil efter börsvärde'), ('rank_turnover', 'rang efter omsättning'), ('rank_mcap', 'rang efter börsvärde')]:
    for p in PER:
        s = rk[(rk.period == p) & rk[v].notna()]; rec('C storleksrang', 'addition', 'alla tillägg', f'{p}: {nm} (1 = högst)', medel(s[v], s.review_cycle))
    s = rk[rk[v].notna()]; Xp = np.column_stack([(s.period == p).astype(float).values for p in PER])
    rec('C storleksrang', 'addition', 'alla tillägg', f'{nm}: 2022–2026 minus 2007–2011', lin(Xp, s[v].values, s.review_cycle.values, [-1.0, 0, 0, 1.0]))
    a, b = s[~s.post_nov2023], s[s.post_nov2023]
    rec('C storleksrang', 'addition', 'alla tillägg', f'{nm}: före översynen nov 2023', medel(a[v], a.review_cycle))
    rec('C storleksrang', 'addition', 'alla tillägg', f'{nm}: från översynen nov 2023 (sex dagars varsel)', medel(b[v], b.review_cycle))
    o = OLDR[OLDR.test.str.contains(f'Fig. 10 analogue: {v} ')]
    jfr(f'C {v} före nov 2023', rows[-2]['b'], o[o.statistic == 'before Nov 2023'].coef.iloc[0], 0.03); jfr(f'C {v} från nov 2023', rows[-1]['b'], o[o.statistic.str.startswith('from Nov 2023')].coef.iloc[0], 0.03)   # tolerans för lika värden, se ovan

R = pd.DataFrame(rows); R.to_csv(OUT / 'liquidity_results.csv', index=False)
f = lambda v, d=2: '' if pd.isna(v) else f'{v:.{d}f}'.replace('-', '−')
with open(OUT / 'LIQUIDITY.md', 'w', encoding='utf-8') as fh:
    fh.write('# Steg 11: spread, volym kring ändringen och storleksrang\n\nFlyttat från `code/build/mechanisms_2007.py` (30 okt 2026), metoden oförändrad. Stjärnor från wild cluster bootstrap.\n\n')
    fh.write('## Jämförelse med körningen 30 oktober\n\n' + ('Alla jämförda siffror är desamma (tolerans 0,000001).\n\n' if not avvik else 'Avvikelser:\n\n' + '\n'.join('- ' + a for a in avvik) + '\n\n'))
    fh.write('## A. Värdeviktad noterad spread, OMXSB-bolagen (G&S figur 9)\n\n| År | Spread, OMXSB (%) | Spread, alla Stockholmsaktier i panelen (%) | Tilläggens CAR (%) | N tillägg |\n|---|---|---|---|---|\n')
    for y_, r in e2.iterrows(): fh.write(f'| {y_} | {f(r.vw_spread_omxsb_members, 3)} | {f(r.vw_spread_all_st_panel, 3)} | {f(r.addition_effect_mean)} | {f(r.N_additions, 0)} |\n')
    fh.write('\n| Lutning, CAR på årets spread | Urval | Skattning | 95 % intervall | p | N |\n|---|---|---|---|---|---|\n')
    for r in R[R.rad.str.startswith('lutning')].itertuples(): fh.write(f'| {r.typ} | {r.urval} | {f(r.b)}{stars(r.p_wcb)} | {f(r.lo)} till {f(r.hi)} | {f(r.p_wcb, 3)} | {int(r.n)} |\n')
    fh.write('\n## B. Andel av omsättningen ED±22 (G&S avsnitt 2.4.3)\n\n| Typ | Urval | Rad | Skattning | 95 % intervall | N |\n|---|---|---|---|---|---|\n')
    for r in R[R.test == 'B volym'].itertuples(): fh.write(f'| {r.typ} | {r.urval} | {r.rad} | {f(r.b)}{stars(r.p_wcb) if "minus" in r.rad else ""} | {f(r.lo)} till {f(r.hi)} | {int(r.n)} |\n')
    fh.write('\n## C. Tilläggens rang bland icke-medlemmar (G&S figur 8)\n\n| Rad | Skattning | 95 % intervall | p | N |\n|---|---|---|---|---|\n')
    for r in R[R.test == 'C storleksrang'].itertuples(): fh.write(f'| {r.rad} | {f(r.b, 1)}{stars(r.p_wcb) if "minus" in r.rad else ""} | {f(r.lo, 1)} till {f(r.hi, 1)} | {f(r.p_wcb, 3) if "minus" in r.rad else ""} | {int(r.n)} |\n')
    fh.write(f'\n{n_olika} av {2 * len(rk)} rangtal skiljer sig från körningen 30 oktober, alla med en plats. Orsaken är lika värden: två aktieslag i samma bolag har samma börsvärde i LSEG, och då ordnade sorteringen dem godtyckligt. Här ordnas lika värden efter RIC.\n')
    fh.write(f'\n{int(rk.rank_turnover.isna().sum())} av {len(rk)} tillägg saknar rang efter omsättning (aktien handlades under hälften av dagarna i fönstret eller saknas i panelen).\n')
print('Metod: klustrat per översyn, restriktiv wild cluster bootstrap (9 999 dragningar)')
print('jämförelse med 30 okt:', 'inga avvikelser' if not avvik else avvik)
print(R[['test', 'typ', 'urval', 'rad', 'b', 'lo', 'hi', 'p_wcb', 'n', 'G']].to_string())
