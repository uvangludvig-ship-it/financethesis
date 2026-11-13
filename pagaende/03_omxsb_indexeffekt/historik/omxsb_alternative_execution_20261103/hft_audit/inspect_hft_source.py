"""Source-only inventory of SHoF CSV/ZIP exports. No price/volume outcomes.

Example: python inspect_hft_source.py private.zip --out source_inventory.json
Explicit --categorical COLUMN may inspect documented message/phase/status labels;
never pass a numerical price, quantity or investor identifier as categorical.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, csv, gzip, hashlib, io, json, zipfile
from collections import Counter
from contextlib import contextmanager

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

@contextmanager
def members(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            bad=z.testzip()
            if bad: raise ValueError(f'ZIP CRC failure in {bad}')
            found=[n for n in z.namelist() if not n.endswith('/')]
            yield [(n,lambda n=n:z.open(n,'r')) for n in found]
    else:
        with path.open('rb') as check: magic=check.read(2)
        op=(lambda:gzip.open(path,'rb')) if magic==b'\x1f\x8b' else (lambda:path.open('rb'))
        yield [(path.name,op)]

def inspect(path, categories):
    out={'created_utc':datetime.now(timezone.utc).isoformat(),'path':str(path.resolve()),
         'sha256':sha(path),'bytes':path.stat().st_size,'source_only':True,
         'computed_price_volume_return_outcomes':False,'members':[]}
    with members(path) as mm:
        for name,op in mm:
            m={'member':name}
            with op() as raw:
                f=io.TextIOWrapper(raw,encoding='utf-8-sig',errors='strict',newline='')
                sample=f.read(65536)
            try:dialect=csv.Sniffer().sniff(sample,delimiters=',;\t|')
            except csv.Error: dialect=csv.excel
            with op() as raw:
                f=io.TextIOWrapper(raw,encoding='utf-8-sig',errors='strict',newline='')
                reader=csv.reader(f,dialect)
                header=next(reader)
                if len(header)!=len(set(header)): raise ValueError('Duplicate header labels')
                missing=Counter(); cats={c:Counter() for c in categories if c in header}
                idx={c:header.index(c) for c in cats}
                hashes=set(); n=0;dup=0; malformed=0
                for row in reader:
                    n+=1
                    if len(row)!=len(header):
                        malformed+=1
                        continue
                    for col,v in zip(header,row):
                        if v.strip().lower() in ('','na','n/a','nan','null','none'):missing[col]+=1
                    digest=hashlib.blake2b(json.dumps(row,separators=(',',':')).encode(),digest_size=16).digest()
                    if digest in hashes:dup+=1
                    hashes.add(digest)
                    for c,values in cats.items():values[row[idx[c]]]+=1
                m.update(delimiter=dialect.delimiter,columns=header,row_count=n,
                         malformed_rows=malformed,exact_duplicate_rows=dup,
                         missing_count={c:missing[c] for c in header},
                         explicit_categorical_counts={c:dict(v) for c,v in cats.items() if len(v)<=100},
                         categorical_omitted_high_cardinality=[c for c,v in cats.items() if len(v)>100])
            out['members'].append(m)
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('input',type=Path);a.add_argument('--out',type=Path,required=True)
    a.add_argument('--categorical',action='append',default=[])
    x=a.parse_args()
    if x.out.exists(): raise FileExistsError('Preserve earlier inventory; choose a new output name')
    result=inspect(x.input,x.categorical)
    x.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'source_sha256':result['sha256'],'members':[
        {k:m[k] for k in ['member','columns','row_count','malformed_rows','exact_duplicate_rows']}
        for m in result['members']]},ensure_ascii=False))

if __name__=='__main__':main()
