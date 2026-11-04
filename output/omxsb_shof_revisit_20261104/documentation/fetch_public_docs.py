"""Bounded public documentation retrieval; no data portal/account requests."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
OUT = HERE / "private_sources"
URLS = {
    "reconstructed_current": "https://www.houseoffinance.se/data-center/nasdaq-hft/reconstructed-order-book/",
    "nmq_current": "https://www.houseoffinance.se/data-center/nasdaq-hft/nordic-market-quality/",
    "hft_current": "https://www.houseoffinance.se/data-center/nasdaq-hft/",
    "nmq_interview_2023": "https://www.houseoffinance.se/outreach/data-center-news/2023/discover-the-nordic-market-quality-database-making-financial-markets-research-more-feasible/",
    "nmq_archive_lookup": "https://archive.org/wayback/available?url=https%3A%2F%2Fwww.houseoffinance.se%2FMQ_metrics.pdf&timestamp=20230101",
    "nmq_hhs_archive_lookup": "https://archive.org/wayback/available?url=https%3A%2F%2Fwww.hhs.se%2FMQ_metrics.pdf&timestamp=20230101",
    "itch_2020": "https://www.nasdaq.com/docs/2020/04/03/Nordic-Equity-TotalView---ITCH-3.03.5.pdf",
    "itch_2024": "https://www.nasdaq.com/docs/2024/10/10/Nordic-Equity-TotalView-ITCH-3.04.1.pdf",
}

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            h=dict(attrs).get("href", "")
            if any(x in h.lower() for x in ["data.houseoffinance", "metrics", "documentation", "ticker", "timeserie"]):
                self.links.append(h)

def fetch(item):
    name,url=item
    r={"id":name,"requested_url":url,"retrieved_utc":datetime.now(timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=22) as f:
            body=f.read(); r.update(status=f.status,final_url=f.url,content_type=f.headers.get("Content-Type"))
        (OUT/(name+".bin")).write_bytes(body)
        r.update(bytes=len(body),sha256=sha256(body).hexdigest(),private_path="private_sources/"+name+".bin")
        if "html" in (r["content_type"] or ""):
            p=Links();p.feed(body.decode("utf-8",errors="replace"));r["public_page_links"]=sorted(set(p.links))
        if "lookup" in name:
            r["archive_response"]=json.loads(body)
    except Exception as e:
        r["error"]=str(e)
    return r

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(fetch,URLS.items()))
    (HERE/"PUBLIC_FETCH_LOG.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))
