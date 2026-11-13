import csv, sys, re, collections, statistics as st, math
funds_csv, hold_csv, ev_csv = sys.argv[1:4]
F=list(csv.DictReader(open(funds_csv))); H=list(csv.DictReader(open(hold_csv))); E=list(csv.DictReader(open(ev_csv)))
def fl(x):
    try: return float(str(x).replace(',','.'))
    except: return None
meta={(r['quarter'],r['fund_id']):r for r in F}
omxsb=re.compile(r'stockholm benchmark|omxsb',re.I)
idxname=re.compile(r'index|indeks|access|passiv|zero|xact|exponering',re.I)
def is_other_index(m):
    bm=m['benchmark'] or ''; name=m['fund_name'] or ''; ar=fl(m['active_risk'])
    if omxsb.search(bm): return False
    passive=(ar is not None and ar<1.5) or bool(idxname.search(name))
    return passive
hold=collections.defaultdict(float)
for h in H:
    a=fl(h['antal'])
    if a is not None: hold[(h['quarter'],h['fund_id'],h['isin'])]+=a
byqi=collections.defaultdict(list)
for (q,f,i),a in hold.items(): byqi[(q,i)].append((f,a))
names=collections.Counter()
res={'addition':[], 'deletion':[]}
for e in E:
    S=fl(e['shares_qa']);
    if not S: continue
    isins=[s for s in re.split(r'[;,| ]+',e['isins']) if s]
    def tot(q):
        t=0
        for i in isins:
            for f,a in byqi.get((q,i),[]):
                m=meta.get((q,f))
                if m and is_other_index(m):
                    t+=a
                    if a>0: names[m['fund_name']]+=1
        return t
    b=tot(e['qb']); a=tot(e['qa'])
    res[e['type']].append((e['AD'],100*b/S,100*a/S,100*(a-b)/S,e['company']))
for ty,rows in res.items():
    rev=collections.defaultdict(list)
    for ad,b,a,d,c in rows: rev[ad].append(d)
    rm=[st.mean(v) for v in rev.values()]
    m=st.mean(rm); se=st.stdev(rm)/math.sqrt(len(rm))
    pre=[b for _,b,_,_,_ in rows]
    print(f"{ty}: n {len(rows)}, reviews {len(rm)} | other index funds' holding before: mean {st.mean(pre):.3f}% median {st.median(pre):.3f}% | change {m:+.3f}% (t {m/se:.2f}) | events with holding before>0.05%: {sum(1 for p in pre if p>0.05)}")
    big=sorted(rows,key=lambda r:r[3])[:4] if ty=='addition' else sorted(rows,key=lambda r:-r[3])[:4]
    for r in big: print('   ',r[0],r[4][:28],f'before {r[1]:.3f}% after {r[2]:.3f}% change {r[3]:+.3f}%')
print('most common other index funds:',[n for n,_ in names.most_common(12)])
