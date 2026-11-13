"""Read NMQ identities/dates/header only; no numerical market-quality outcomes."""
from pathlib import Path
import zipfile,csv,io,json,hashlib

RAW=Path('/Users/ludviguvang/dev/financethesis/data/raw/shof/Reinvestments/hft_pilot_20261103/NASDAQ_micromeasures_1793733197232.zip')
OUT=Path(__file__).resolve().parent
members=[]
with zipfile.ZipFile(RAW) as z:
    assert z.testzip() is None
    for name in z.namelist():
        with z.open(name) as f:
            text=io.TextIOWrapper(f,encoding='utf-8-sig').read()
        dialect=csv.Sniffer().sniff(text[:65536],delimiters=',;\t|')
        reader=csv.DictReader(io.StringIO(text),dialect=dialect)
        header=reader.fieldnames
        metadata=[{k:r[k] for k in ['Stock','Date']} for r in reader]
        members.append({'member':name,'rows':len(metadata),'metadata':metadata,
            'explicit_auction_named_headers':[c for c in header if any(w in c.lower() for w in ['auction','uncross','close'])]})
result={'source_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest(),'source_only':True,
 'numerical_metric_values_used_for_analysis':False,'members':members,
 'conclusion':'No explicit auction/uncross/closing-price field in this delivered schema. Aggregate min/mean/max prices are not auction prices and will not substitute for the locked primary.',
 'UI_range_note':'Root observed authenticated query UI ending2021-06-30; this raw one-week file is not itself proof of full product range, and no2023NMQcoverage is claimed.'}
(OUT/'NMQ_SOURCE_NOTE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
