"""Bounded public-source probe. No credentials, cookies, or browser session.
Official documented endpoint only; an authentication refusal is not bypassed.
No return outcomes or price-change calculations.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json

O = Path(__file__).resolve().parent
(O / 'sources').mkdir(exist_ok=True)
URLS = {
 'giw_spec.pdf': 'https://www.nasdaq.com/docs/GIW_WebService_Spec.pdf',
 'daily_proforma_guide.pdf': 'https://indexes.nasdaq.com/docs/GIW%20Web%20Services%20API%20-%20Daily%20Pro%20Forma%20Guide%202.pdf',
 'giw_navigation.pdf': 'https://indexes.nasdaq.com/docs/Tips%20to%20Navigate%20Your%20New%20Global%20Index%20Watch%20Access.pdf',
 'omxsb_methodology_current.pdf': 'https://indexes.nasdaq.com/docs/Methodology_OMXSB.pdf',
 'release_2023H2.html': 'https://view.news.eu.nasdaq.com/view?id=be007a57f33d4d52541bfc529d8b21f55&lang=en',
 'omxsbpi_weighting.html': 'https://indexes.nasdaq.com/Index/Weighting/OMXSBPI',
 'pilot_20231130_EOD.txt': 'https://indexes.nasdaqomx.com/reports2/UFFWeighting.ashx?IndexSymbol=OMXSBPI&Date=2023-11-30&Type=pipe&FileType=EOD',
 'pilot_20231201_SOD.txt': 'https://indexes.nasdaqomx.com/reports2/UFFWeighting.ashx?IndexSymbol=OMXSBPI&Date=2023-12-01&Type=pipe&FileType=SOD',
}
def one(item):
    name,url=item
    row={'file':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authenticated':False}
    try:
        try:
            r=urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=25)
        except HTTPError as e:
            r=e
        body=r.read();row.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
        (O/'sources'/name).write_bytes(body)
        if 'pdf' not in name:
            text=body.decode('utf8','replace')
            row['authentication_words']={s:s.lower()in text.lower()for s in ['Invalid username','Invalid password','login','Log in','Unauthorized','Access Denied']}
            if name.startswith('pilot_'):row['body_excerpt']=text[:600]
    except Exception as e:
        row['error']=type(e).__name__+': '+str(e)
    return row
with ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(one,URLS.items()))
(O/'PUBLIC_SOURCE_ATTEMPTS.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
