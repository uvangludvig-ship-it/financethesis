"""Public issuer documents only; no account, cookie, or licensed-data access."""
from pathlib import Path
import urllib.request, json, hashlib, datetime, io
from pypdf import PdfReader
O = Path(__file__).resolve().parent
sources = {
    'SEB_dividends_2021_alternate.pdf': 'https://seb.se/globalassets/fondutdelningar-maj-2021.pdf',
    'SEB_class_letter_2017.pdf': 'https://sebgroup.com/globalassets/adobe/seb_ethical_beta_fund_kundbrev_bilaga.pdf',
}
rows = []
for name, url in sources.items():
    row = dict(file=name, source_url=url, retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), public_document=True, fulltext_republication_allowed=False)
    try:
        with urllib.request.urlopen(url, timeout=25) as response:
            raw = response.read()
            row.update(status=response.status, final_url=response.url)
        assert raw.startswith(b'%PDF'), 'Not PDF'
        (O / name).write_bytes(raw)
        reader = PdfReader(io.BytesIO(raw))
        row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), pages=len(reader.pages))
        row['relevant_pdf_pages'] = [i + 1 for i, p in enumerate(reader.pages) if 'SE0001696857' in p.extract_text()]
    except Exception as error:
        row['error'] = str(error)
    rows.append(row)
    print(name, row.get('status'), row.get('relevant_pdf_pages'), row.get('error'))
(O / 'SUPPLEMENTAL_PUBLIC_DOCUMENTS.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
