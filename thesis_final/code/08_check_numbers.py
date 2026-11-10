# Jämför huvudsiffrorna med det skripten skrev. Skriver OK eller FEL per rad, och antal FEL sist.
# Körs från thesis_final efter alla steg: python3 code/08_check_numbers.py
# Tolerans: 0,001 för skattningar och analytiska intervall, 0,005 för bootstrapintervall (testinversion, 9 nov). För p från wild bootstrap 0,0005, eftersom en
# dragning av 9 999 kan hamna olika på olika datorer (sett i tabell1 panel E, två rader, ingen stjärna ändras).
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RES = ROOT / 'results'
import json, sys
import pandas as pd

T1 = pd.read_csv(RES / 'effect' / 'tabell1_lang.csv')
R13 = pd.read_csv(RES / 'fund_demand' / 'omrakning_resultat.csv')
F1 = pd.read_csv(RES / 'fund_demand' / 'figur1_skikt.csv')
KJ = json.load(open(RES / 'fund_demand' / 'kontroller.json'))
FI = pd.read_csv(RES / 'fi_check' / 'fi_m_kontroll.csv')
C14 = pd.read_csv(RES / 'msci_overlap' / 'resultat_car.csv')
M14 = pd.read_csv(RES / 'msci_overlap' / 'resultat_m.csv')
O14 = pd.read_csv(RES / 'msci_overlap' / 'overlapp_handelser.csv')
MDE = pd.read_csv(RES / 'mde' / 'mde.csv')


def rad(df, **k):
    m = df
    for a, b in k.items():
        m = m[m[a] == b]
    if len(m) == 0:
        raise KeyError(k)
    return m.iloc[0]


fel = 0
TOL_IV = 0.005   # bootstrapintervall: kanten hamnar där p passerar 0,05, så en annan dragning flyttar den något


def koll(namn, varde, vantat, tol=0.001):
    global fel
    ok = abs(float(varde) - vantat) <= tol
    fel += not ok
    print(f"{'OK ' if ok else 'FEL'}  {namn:<62} {float(varde):>9.4f}   väntat {vantat:>9.4f}")


def iv(r, lo_b, hi_b, lo_a, hi_a):
    # bootstrapintervall (testinversion, satt 9 nov 2026) och det analytiska CR1-intervallet som gällde före 9 nov
    koll('  undre, bootstrap', r.lo, lo_b, TOL_IV); koll('  övre, bootstrap', r.hi, hi_b, TOL_IV)
    koll('  undre, analytiskt (CR1)', r.lo_cr1, lo_a); koll('  övre, analytiskt (CR1)', r.hi_cr1, hi_a)


# tabell1.py
r = rad(T1, panel='A/B', typ='addition', fönster='tot', urval='2007–2011')
koll('Tillägg 2007–11, totalt fönster', r.b, 8.5229); iv(r, 2.4561, 14.7431, 2.9227, 14.1230)
koll('Tillägg 2017–21, totalt fönster', rad(T1, panel='A/B', typ='addition', fönster='tot', urval='2017–2021').b, 2.8475)
r = rad(T1, panel='A/B', typ='addition', fönster='tot', urval='2022–2026')
koll('Tillägg 2022–26, totalt fönster', r.b, 1.4976); koll('  p wild bootstrap', r.p_wcb, 0.0620, 0.0005)
r = rad(T1, panel='C', typ='addition', urval='2017–26')
koll('Tillägg 2017–26', r.b, 2.1526); iv(r, 1.0118, 3.3872, 1.0026, 3.3026)
r = rad(T1, panel='D', typ='addition', urval='2022–26 minus 2007–11')
koll('Fall 2007–11 till 2022–26', r.b, -7.0252); koll('  p wild bootstrap', r.p_wcb, 0.0285, 0.0005)
r = rad(T1, panel='D', typ='addition', urval='2022–26 minus 2017–21')
koll('2022–26 minus 2017–21', r.b, -1.3498); iv(r, -3.8780, 0.9782, -3.5020, 0.8023)
koll('Decennier, 2017–26 minus 2007–16', rad(T1, panel='D', typ='addition', urval='2017–26 minus 2007–16 (decennier)').b, -1.2353)
r = T1[(T1.panel == 'D') & (T1.typ == 'addition') & T1.urval.str.startswith('efter minus före brottet')].iloc[0]
koll('Brottet juni 2010', r.b, -9.6276); koll('  p wild bootstrap', r.p_wcb, 0.0061, 0.0005)
koll('Borttag 2007–11, totalt fönster', rad(T1, panel='A/B', typ='deletion', fönster='tot', urval='2007–2011').b, -6.1563)
r = rad(T1, panel='C', typ='deletion', urval='2017–26')
koll('Borttag 2017–26', r.b, -1.0382); iv(r, -2.8811, 0.8954, -2.8574, 0.7810)
koll('Borttag, beskedet 2012–16', rad(T1, panel='A/B', typ='deletion', fönster='ann', urval='2012–2016').b, -1.7091)
koll('Borttag, beskedet 2017–21', rad(T1, panel='A/B', typ='deletion', fönster='ann', urval='2017–2021').b, -2.0941)
# urvalsregeln 10 nov 2026 (G&S): 10 borttag ute ur CAR-tabellerna; panel R är det gamla urvalet
r = rad(T1, panel='D', typ='deletion', urval='2022–26 minus 2007–11'); koll('Borttag, fall 2007–11 till 2022–26', r.b, 4.6230); koll('  p wild bootstrap', r.p_wcb, 0.0392, 0.0005)
koll('Borttag i tabell 1 (händelser, totalt fönster)', T1[(T1.panel == 'A/B') & (T1.typ == 'deletion') & (T1.fönster == 'tot')].n.sum(), 215, 0)
koll('Gammalt urval, borttag 2007–11 (robusthet)', rad(T1, panel='R (gammalt urval, alla borttag)', typ='deletion', urval='2007–2011').b, -6.6939)

# runda 13 (omrakning_fondklassning.py)
r = rad(R13, tabell=5, typ='addition', skikt='D_V', fonster='y_tot', period='2017–26')
koll('D_V tillägg 2017–26 (% av aktierna)', r.D, 0.8723)
koll('M_V tillägg 2017–26', r.M, 3.1104); koll('  undre', r.lo, 1.4450); koll('  övre', r.hi, 5.1431)
koll('D_V tillägg 2007–11', rad(R13, tabell=5, typ='addition', skikt='D_V', fonster='y_tot', period='2007–11').D, 0.1034)
r = rad(R13, tabell=6, typ='addition', skikt='D_V', fonster='y_tot', period='M 2007–11 − M 2022–26')
koll('M 2007–11 minus M 2022–26, p', r.p, 0.1140, 0.0005)
r = rad(R13, tabell=7, typ='addition', period='2017–26', grupp='alla_fonder')
# 9 nov: efter-rader rapporterade före ED räknas som 0 (fond som sålt allt). Före: 1,2044 [0,7630, 1,6457]; aktiva −0,1505.
koll('Alla fonder, köp vid tillägg 2017–26', r.b, 1.1923); koll('  undre', r.lo, 0.7585); koll('  övre', r.hi, 1.6261)
r = rad(R13, tabell=7, typ='addition', period='2017–26', grupp='aktiva')
koll('Aktiva fonder, köp vid tillägg 2017–26', r.b, -0.1624); iv(r, -0.4694, 0.1565, -0.4683, 0.1434)
koll('Ägarandel V 2007 (%)', rad(F1, ar=2007).agarandel_V_pct, 0.0600)
koll('Ägarandel V 2025 (%)', rad(F1, ar=2025).agarandel_V_pct, 1.1360)
koll('Korrelation D_V mot FI', KJ['fi_jamforelse']['D_V']['korr'], 0.809)
koll('Uteslutna fond-händelser (grupp-byte)', KJ['uteslutna_mandatbyten'], 93, 0)

# fi_m_kontroll.py (inte deklarerad)
r = FI[(FI.typ == 'addition') & (FI.splittade == False)].iloc[0]
koll('M med FI:s D, tillägg utan split', r.M_FI, 2.1229); koll('  undre', r.lo_FI, 0.8711); koll('  övre', r.hi_FI, 3.7867)

# runda 14
koll('Händelser som överlappar MSCI', len(O14), 29, 0)
r = rad(C14, typ='addition', urval='2017–26', variant='utan överlapp')
koll('Tillägg 2017–26 utan MSCI-överlapp', r.b, 1.4573); iv(r, 0.4968, 2.4735, 0.4823, 2.4323)
koll('  p wild bootstrap', r.p, 0.0073, 0.0005)
koll('Tillägg 2022–26 utan MSCI-överlapp', rad(C14, typ='addition', urval='2022–26', variant='utan överlapp').b, 0.7258)
koll('Överlappande tillägg 2017–26, medel (beskrivande)', rad(C14, typ='addition', urval='2017–26', variant='bara överlapp (beskrivande)').b, 11.2487)
r = rad(M14, typ='addition', urval='2017–26', variant='utan överlapp')
koll('M_V 2017–26 utan MSCI-överlapp', r.M, 2.2815); koll('  undre', r.lo, 0.9805); koll('  övre', r.hi, 3.9690)

# mde.py
for test, v in [('2022–26 minus 2017–21', 3.057), ('2017–26 minus 2007–16 (decennier)', 5.234),
                ('M 2017–21 minus M 2022–26', 5.751)]:
    koll(f'MDE {test}', rad(MDE, test=test).mde, v)
for typ, test, v in [('addition', '2017–26', 1.622), ('addition', '2022–26', 2.353), ('deletion', '2017–26', 2.566)]:
    koll(f'MDE {typ} {test}', rad(MDE, typ=typ, test=test).mde, v)

# steg 07, 11 och 12 (10 nov): G&S-test flyttade hit från körningarna 30 okt och 2 nov. Punktskattningarna ska vara desamma som då.
SP = pd.read_csv(RES / 'liquidity' / 'spread_by_year.csv')
LQ = pd.read_csv(RES / 'liquidity' / 'liquidity_results.csv')
OT = pd.read_csv(RES / 'other_tests' / 'issuance_omxs30_results.csv')
KO = pd.read_csv(RES / 'controls' / 'controls_by_event.csv')
koll('Spread OMXSB-bolagen 2007 (%)', rad(SP, year=2007).vw_spread_omxsb_members, 0.2701, 0.0001)
koll('Spread OMXSB-bolagen 2025 (%)', rad(SP, year=2025).vw_spread_omxsb_members, 0.0790, 0.0001)
koll('Tilläggens CAR på årets spread, lutning', rad(LQ, test='A spread', typ='addition', urval='tabell 1').b, 39.6428)
koll('Andel av omsättningen ED−1, tillägg 2007–11 (%)', rad(LQ, typ='addition', rad='2007–2011: andel av omsättningen ED±22 som handlas ED−1 (%)').b, 9.4441)
koll('Andel av omsättningen ED−1, tillägg 2022–26 (%)', rad(LQ, typ='addition', rad='2022–2026: andel av omsättningen ED±22 som handlas ED−1 (%)').b, 15.2364)
koll('Andel ED−1, borttag 2022–26, gammalt urval (%)', rad(LQ, typ='deletion', urval='gammalt urval', rad='2022–2026: andel av omsättningen ED±22 som handlas ED−1 (%)').b, 14.4356)
koll('Tilläggens percentil efter omsättning 2007–11', rad(LQ, rad='2007–2011: percentil efter omsättning (1 = högst)').b, 15.7881)
koll('Tilläggens percentil efter omsättning 2022–26', rad(LQ, rad='2022–2026: percentil efter omsättning (1 = högst)').b, 6.5008)
r = rad(OT, rad='tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter)')
koll('Nyemissioner, tillägg minus nästan tillagda', r.b, 0.5018); koll('  antal aktier i jämförelsen', r.n, 2586, 0)
koll('OMXS30, tillägg, CAR (%)', rad(OT, urval='tabell 1 (10 borttag ute)', rad='OMXS30, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%)').b, 0.2105)
koll('OMXS30, alla, CAR med vänt tecken för borttag (%)', rad(OT, urval='tabell 1 (10 borttag ute)', rad='OMXS30, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%)').b, 0.4388)
koll('OMXS30 minus OMXSB, MDE som 2 nov', rad(OT, urval='som 2 nov (19 flaggade borttag ute)', rad='styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3').b, 3.6642)
koll('Händelser med alla fyra kontroller', int(KO[['k_oms', 'k_storlek', 'k_wz', 'k_ana']].notna().all(axis=1).sum()), 440, 0)
koll('Kontroller: händelser från runda 11 som räknats om', int(KO.kalla.str.startswith('runda 11').sum()), 468, 0)
for fil in ['liquidity/LIQUIDITY.md', 'other_tests/ISSUANCE_OMXS30.md', 'controls/CONTROLS.md']:
    txt = (RES / fil).read_text(encoding='utf-8')
    koll(f'{fil}: avvikelser mot den gamla körningen', int('Avvikelser' in txt), 0, 0)

# intervall och p från samma bootstrap ska alltid stämma: p < 0,05 precis när 0 ligger utanför intervallet
for namn, df, pc in [('tabell1', T1, 'p_wcb'), ('runda 13', R13, 'p'), ('runda 14', C14, 'p')]:
    d = df[df.ci_metod.astype(str).str.startswith('95 % intervall: invertering')]
    n_fel = int(((d[pc] < .05) != ((d.lo > 0) | (d.hi < 0))).sum())
    koll(f'{namn}: bootstrapintervall som inte stämmer med p ({len(d)} rader)', n_fel, 0, 0)
for namn, df in [('tabell1', T1), ('runda 13', R13), ('runda 14 CAR', C14), ('runda 14 M', M14), ('FI-kontroll', FI), ('MDE', MDE)]:
    kol = 'metod' if 'metod' in df else 'ci_metod'
    koll(f'{namn}: rader utan metodtext', int(df[kol].isna().sum()), 0, 0)

print(f'\n{fel} FEL')
sys.exit(1 if fel else 0)
