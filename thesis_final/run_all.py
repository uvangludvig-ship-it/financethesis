# Kör hela kedjan från data/ till results/ och kontrollerar huvudsiffrorna.
# Öppna mappen thesis_final i VS Code och kör den här filen (Run Python File), eller i terminalen:
#   python3 run_all.py
# Kräver Python 3.13 med pandas 3.0, numpy 2.5, scipy 1.18, python-docx 1.2 och matplotlib 3.11. Tar cirka tio minuter.
# Sista raden "0 FEL" betyder samma siffror som i testet 9 november 2026.
import csv, hashlib, os, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
PY = sys.executable

# 0. Indata: samma filer som i testet?
rader = list(csv.DictReader(open('data/FILES.csv', encoding='utf-8')))
fel = [r['file'] for r in rader if not (Path('data') / r['file']).exists()
       or hashlib.md5((Path('data') / r['file']).read_bytes()).hexdigest() != r['md5']]
print(f'Indata: {len(rader) - len(fel)} av {len(rader)} filer stämmer')
for f in fel:
    print('  annan eller saknas:', f)
if fel:
    sys.exit('Stopp: indata skiljer sig från testet. Se data/FILES.csv.')

STEG = [
    ('01_effect_table.py', 'Effekten per period, år och decennium'),
    ('02_fund_demand.py', 'Fondernas köp (D), priset per köpt procent (M), vem som köper'),
    ('03_fund_demand_fi_check.py', 'M med FI:s D (kontroll)'),
    ('04_msci_overlap_match.py', 'Vilka händelser som sammanfaller med MSCI'),
    ('05_msci_overlap_results.py', 'Effekt och M med och utan MSCI-överlapp'),
    ('06_mde.py', 'Minsta påvisbara effekt'),
    ('07_controls_from_prices.py', 'Kontrollvariablerna i G&S tabell 2 räknade ur kurserna (ändrar ingen tabell)'),
    ('09_news_screen.py', 'Robusthet: utan händelser med egen bolagsnyhet i fönstret'),
    ('10_composition_runup.py', 'G&S tabell 2 och 4 (metod 5.3 och 5.4) och M på samma händelser'),
    ('11_liquidity_and_selection.py', 'G&S figur 9 (spread), volym kring ändringen och figur 8 (storleksrang)'),
    ('12_issuance_and_omxs30.py', 'G&S nyemissioner och tabell 8 (OMXS30)'),
    ('13_extreme_values.py', 'Robusthet: extremvärden (winsorisering, utan |CAR| > 20, utan Sivers, median) och M utan nyhetshändelserna'),
    ('14_near_additions_control.py', 'Tillägg och borttag mot nästan tillagda (T5v)'),
    ('15_reversal.py', 'Återgång efter ändringen'),
    ('16_twins.py', 'Tvillingar: indexslaget mot systerslaget'),
]
# Word-tabeller och figurer, en fil per tabell eller figur, i Greenwood och Sammons ordning
STEG += [(f'output/{f.name}', f.stem) for f in sorted((ROOT / 'code' / 'output').glob('[0-9][0-9]_*.py'))]
if Path('results').exists():   # allt byggs om; bara README.md (beskrivningen av mappen, committad) får stå kvar
    for p in Path('results').iterdir():
        if p.name != 'README.md':
            shutil.rmtree(p) if p.is_dir() else p.unlink()
for fil, namn in STEG:
    t0 = time.time()
    print(f'{fil}: {namn} ...', end=' ', flush=True)
    r = subprocess.run([PY, f'code/{fil}'], capture_output=True, text=True)
    if r.returncode:
        print('FEL')
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f'Stopp vid {fil}')
    print(f'klar ({time.time() - t0:.0f} s)')
    (ROOT / 'results' / 'logs').mkdir(parents=True, exist_ok=True)
    (ROOT / 'results' / 'logs' / Path(fil).name.replace('.py', '.txt')).write_text(r.stdout + r.stderr, encoding='utf-8')
    for rad in dict.fromkeys(l for l in r.stdout.splitlines() if l.startswith('Metod')):
        print('    ' + rad)

r = subprocess.run([PY, 'code/08_check_numbers.py'], capture_output=True, text=True)
Path('results/check.txt').write_text(r.stdout + r.stderr, encoding='utf-8')
print((r.stdout.strip().splitlines() or ['inget utfall'])[-1])
print('Resultaten ligger i', ROOT / 'results', '(hela utskriften per steg i results/logs/)')
sys.exit(r.returncode)
