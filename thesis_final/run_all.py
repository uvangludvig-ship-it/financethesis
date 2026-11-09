# Kör hela kedjan från data/ till results/ och kontrollerar huvudsiffrorna.
# Öppna mappen thesis_final i VS Code och kör den här filen (Run Python File), eller i terminalen:
#   python3 run_all.py
# Kräver Python 3.13 med pandas 3.0, numpy 2.5, scipy 1.18 och python-docx 1.2. Tar cirka tre minuter.
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
    ('07_word_tables.py', 'Word-tabellerna'),
]
if Path('results').exists():
    shutil.rmtree('results')
for fil, namn in STEG:
    t0 = time.time()
    print(f'{fil}: {namn} ...', end=' ', flush=True)
    r = subprocess.run([PY, f'code/{fil}'], capture_output=True, text=True)
    if r.returncode:
        print('FEL')
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f'Stopp vid {fil}')
    print(f'klar ({time.time() - t0:.0f} s)')

r = subprocess.run([PY, 'code/08_check_numbers.py'], capture_output=True, text=True)
Path('results/check.txt').write_text(r.stdout + r.stderr, encoding='utf-8')
print((r.stdout.strip().splitlines() or ['inget utfall'])[-1])
print('Resultaten ligger i', ROOT / 'results')
sys.exit(r.returncode)
