from pathlib import Path
import urllib.request, hashlib, json, subprocess
from concurrent.futures import ThreadPoolExecutor

O = Path(__file__).resolve().parent
sources = {
    'SPP_2018': 'https://www.storebrandfonder.se/globalassets/dokument/finansiell-information/arsberattelse-2018.pdf',
    'SPP_2019': 'https://www.spp.se/globalassets/om-spp/finansiell-information/arsberattelser-och-halvarsredogorelser-for-storebrand-fonder/spp_fonder_arsberattelse-2019.pdf',
    'LF_2018': 'https://mb.cision.com/Main/152/2777443/1017671.pdf',
    'LF_2019': 'https://mb.cision.com/Main/152/3078055/1221768.pdf',
}

def get(item):
    name, url = item
    p = O / (name + '.pdf')
    if not p.exists():
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                blob = response.read()
            assert blob.startswith(b'%PDF'), name
            p.write_bytes(blob)
        except Exception as exc:
            return {'id': name, 'url': url, 'download_error': str(exc), 'reading_route': 'web tool indexed primary PDF; not downloaded'}
    subprocess.run(['/opt/homebrew/bin/pdftotext', '-layout', str(p), str(p.with_suffix('.txt'))], check=True)
    return {'id': name, 'url': url, 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(get, sources.items()))
(O / 'source_manifest.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
