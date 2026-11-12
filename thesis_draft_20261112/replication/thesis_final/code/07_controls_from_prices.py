# Steg 07: kontrollvariablerna i G&S tabell 2, räknade ur kurserna för varje händelse. Flyttat hit från
# code/claude_checks/runda11.py (2 nov 2026), definitionerna oförändrade. Deklaration: declarations/step11_13_declaration.md.
#   k_oms      onormal omsättning: aktieslagets dagliga omsättning i procent av dess börsvärde, medel över [AD−21, AD−1],
#              minus samma mått för hela huvudmarknaden. Minst 10 dagar krävs.
#   k_storlek  relativ storlek: aktieslagets börsvärde i procent av OMXSB-medlemmarnas sammanlagda börsvärde, dagen före AD.
#   k_wz       arbitragerisk (Wurgler och Zhuravskaya): residualvariansen i en regression av dagsavkastningen på OMXSBGI
#              över [AD−250, AD−2]. Minst 100 dagar krävs.
#   k_ana      analytiker: antal vinstprognoser i konsensus månaden före AD (0 om bolaget finns i LSEG:s fil men saknar värde).
# Aktieslagets börsvärde = bolagets börsvärde × aktieslagets andel av aktierna i de noterade aktieslagen (LSEG:s mcap gäller bolaget).
# Runda 11 räknade kontrollerna för 468 händelser; de 19 då flaggade borttagen fick inga. Här räknas alla 487. De 468 ska bli
# desamma som i data/events/omxsb_changes_corrected_2007_2026.csv; avvikelser skrivs ut.
# Steget ändrar ingen tabell: steg 10 läser fortfarande kontrollerna ur filen från runda 11. Om de 9 borttagen med bara ändrat
# aktieantal ska in i tabell 2 med kontroller avgör författarna; värdena finns då i results/controls/controls_by_event.csv.
# Körs från thesis_final: python3 code/07_controls_from_prices.py
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
OUT = RES / 'controls'

SRC = ROOT / 'code' / '01_effect_table.py'
g = {'__file__': str(SRC), '__name__': 'steg07'}
exec(compile(SRC.read_text(encoding='utf-8').split('\nrows = []')[0], str(SRC), 'exec'), g)
np, pd, cal, pos, mkt, GS_UTE = g['np'], g['pd'], g['cal'], g['pos'], g['mkt'], g['GS_UTE']
exec(open(ROOT / 'code' / 'panel_runda3.py', encoding='utf-8').read())   # px, RET, CLOSE, mc, SH, TV, root
os.makedirs(OUT, exist_ok=True)
KC = ['k_oms', 'k_storlek', 'k_wz', 'k_ana']

E = g['ev_alla'].copy(); E['iA'] = E.AD.map(pos).astype(int); E['iE'] = E.ED.map(pos).astype(int)
rev = E.groupby('review_cycle').agg(AD=('AD', 'first')).sort_values('AD').reset_index(); rev['k'] = np.arange(len(rev))
E['k'] = E.review_cycle.map(dict(zip(rev.review_cycle, rev.k))); cyc = list(rev.review_cycle)
MV = pd.read_csv(DATA / 'index' / 'omxsb_members_by_review_verified.csv')
MED = {c: set(d[d.status == 'medlem'].ric) for c, d in MV.groupby('review_after')}
KL = pd.read_csv(DATA / 'controls' / 'stock_classification_lseg.csv'); MIC = dict(zip(KL.ric, KL.marknad.astype(str)))
def not_main(r): return MIC.get(r, 'nan') in ('SSME', 'ONSE')   # Spotlight och NGM räknas inte till huvudmarknaden

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

MAIN = [c for c in TV.columns if not not_main(c)]
mcr = mc[[c for c in MAIN if c in mc]].T.groupby(lambda c: root(c)).max().T   # ett börsvärde per bolag
mkt_turn = TV[MAIN].sum(axis=1, min_count=1) / mcr.sum(axis=1, min_count=1) * 100
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
A8 = pd.read_csv(DATA / 'controls' / 'analyst_estimates_monthly.csv.gz', low_memory=False)
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

# jämförelse med runda 11
K11 = pd.read_csv(DATA / 'events' / 'omxsb_changes_corrected_2007_2026.csv')[['event_id'] + KC]
J = E[['event_id'] + KC].merge(K11, on='event_id', how='left', suffixes=('', '_r11'), indicator=True)
E['kalla'] = np.where(J._merge.values == 'both', 'runda 11 (2 nov), räknad om här', 'ny 10 nov (borttag som var flaggat i runda 11)')
B = J[J._merge == 'both']; avvik = []
for c in KC:
    a, b = B[c].to_numpy(float), B[c + '_r11'].to_numpy(float)
    olika = ~np.isclose(a, b, rtol=1e-9, atol=1e-9, equal_nan=True)
    if olika.any(): avvik.append(f'{c}: {int(olika.sum())} av {len(B)} händelser skiljer sig, största skillnad {np.nanmax(np.abs(a - b)[olika]):.6g}')
E[['event_id', 'type', 'company', 'RIC', 'AD', 'ED', 'review_cycle'] + KC + ['kalla']].to_csv(OUT / 'controls_by_event.csv', index=False)
ny = E[E.kalla.str.startswith('ny')]
with open(OUT / 'CONTROLS.md', 'w', encoding='utf-8') as fh:
    fh.write('# Steg 07: kontrollvariablerna räknade ur kurserna\n\n')
    fh.write(f'{len(E)} händelser. {len(B)} hade kontroller från runda 11 (2 nov). ' + ('De blir desamma här (tolerans 0,000000001).\n\n' if not avvik else 'Avvikelser mot runda 11:\n\n' + '\n'.join('- ' + a for a in avvik) + '\n\n'))
    fh.write('| Kontroll | Händelser med värde | därav nya |\n|---|---|---|\n')
    for c in KC: fh.write(f'| {c} | {int(E[c].notna().sum())} | {int(ny[c].notna().sum())} |\n')
    fh.write(f'\n## De {len(ny)} borttag som får kontroller först nu\n\n| Händelse | Bolag | I tabell 1 | ' + ' | '.join(KC) + ' |\n|---|---|---|' + '---|' * 4 + '\n')
    for r in ny.sort_values('ED').itertuples():
        fh.write(f'| {r.event_id} | {r.company} | {"nej (G&S regel)" if r.event_id in GS_UTE else "ja"} | ' + ' | '.join('' if pd.isna(getattr(r, c)) else f'{getattr(r, c):.3f}' for c in KC) + ' |\n')
print('Metod: beskrivande (kontrollvariabler per händelse), ingen inferens')
print('jämförelse med runda 11:', 'inga avvikelser' if not avvik else avvik)
print({c: int(E[c].notna().sum()) for c in KC}, '| nya:', len(ny), {c: int(ny[c].notna().sum()) for c in KC})
print(ny[['event_id', 'company'] + KC].to_string())
