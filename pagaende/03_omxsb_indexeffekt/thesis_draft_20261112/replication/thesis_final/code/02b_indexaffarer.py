# Indexaffärstestet (Greenwood och Sammons regel): en fond räknas som indexföljare om den gör minst hälften av indexaffärerna.
# För varje fond och händelse där fonden rapporterar högst 120 dagar före AD och högst 45 dagar efter ED (samma regel som i 02):
#   före  = summa aktier i snap 'fore', efter = summa aktier i snap 'efter' med rapport >= ED (saknat innehav = 0)
#   indexaffär: tillägg före = 0 och efter > 0; borttag före > 0 och efter = 0
#   generös:    tillägg efter > före;            borttag efter < före
# Händelser: de 468 i results/fund_demand/handelser_omraknade.csv (körs efter 02). År = beskedsåret (ar), som i 02.
# ALIAS, grupp() och rapport_i() kommer ur 02_fund_demand.py (huvudet körs, inga resultat i 02 ändras).
# Körs från thesis_final: python3 code/02b_indexaffarer.py
import sys
from pathlib import Path
SRC = Path(__file__).resolve().parent / '02_fund_demand.py'
sys.argv = [str(SRC)]   # huvudkörningen (INKL av)
exec(compile(SRC.read_text(encoding='utf-8').split('\n# ---------- nettoköp per händelse')[0], str(SRC), 'exec'))
assert callable(grupp) and callable(rapport_i) and ALIAS

EV = pd.read_csv(RES / 'fund_demand' / 'handelser_omraknade.csv', parse_dates=['AD', 'ED'])
assert len(EV) == 468, len(EV)
G0 = F[~F.gammal & F.aktier.notna()]   # som i 02: rader högst 120 dagar gamla, med antal aktier
H = G0[G0.event_id.isin(EV.event_id)]
FORE = H[H.snap == 'fore'].groupby(['event_id', 'fond']).aktier.sum()
EFTER = H[(H.snap == 'efter') & (H.rapport >= H.ED)].groupby(['event_id', 'fond']).aktier.sum()
rad = []
for e in EV.itertuples():
    a0, a1, b1 = e.AD - pd.Timedelta(days=120), e.AD - pd.Timedelta(days=1), e.ED + pd.Timedelta(days=45)
    for f in RD:
        if rapport_i(f, a0, a1, sista=True) is None or rapport_i(f, e.ED, b1) is None: continue
        fo, ef = FORE.get((e.event_id, f), 0.0), EFTER.get((e.event_id, f), 0.0)
        if e.type == 'addition': ia, ge = fo == 0 and ef > 0, ef > fo
        else: ia, ge = fo > 0 and ef == 0, ef < fo
        rad.append(dict(fond=f, ar=e.ar, event_id=e.event_id, indexaffar=ia, generos=ge))
R = pd.DataFrame(rad)
U = (R.groupby(['fond', 'ar']).agg(antal_handelser=('event_id', 'size'), indexaffarer=('indexaffar', 'sum'), generosa=('generos', 'sum'))
     .reset_index().rename(columns={'ar': 'år'}))
U['andel_indexaffarer'] = U.indexaffarer / U.antal_handelser
U.to_csv(RES / 'fund_demand' / 'indexaffarer_fond_ar.csv', index=False)
print(f'{len(U)} fond-år, {U.fond.nunique()} fonder, {len(R)} fond-händelser')

# kontroll mot uppgiften (11 nov 2026)
KONTROLL = [('XACT Sverige (UCITS ETF)', 2012, 32, 32, None), ('Swedbank Robur Access Mix', 2025, 29, 24, None), ('Storebrand Sverige', 2025, 29, 7, 26)]
fel = 0
for f, ar, n, ia, ge in KONTROLL:
    r = U[(U.fond == f) & (U['år'] == ar)]
    got = (int(r.antal_handelser.iloc[0]), int(r.indexaffarer.iloc[0]), int(r.generosa.iloc[0])) if len(r) else None
    ok = got is not None and got[0] == n and got[1] == ia and (ge is None or got[2] == ge)
    fel += not ok
    print(f"{'OK ' if ok else 'FEL'} {f} {ar}: {got[1] if got else '–'} av {got[0] if got else '–'} indexaffärer, generösa {got[2] if got else '–'}"
          f" (ska vara {ia} av {n}{'' if ge is None else f', generösa {ge}'})")
if fel: sys.exit(f'Stopp: {fel} kontroller stämmer inte')
print('Metod: beskrivande räkning, ingen inferens')
