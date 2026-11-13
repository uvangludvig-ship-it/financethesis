import csv, sys, re, math, random, statistics as st, collections
funds_csv, hold_csv, ev_csv = sys.argv[1:4]
F=list(csv.DictReader(open(funds_csv))); H=list(csv.DictReader(open(hold_csv))); E=list(csv.DictReader(open(ev_csv)))
def fl(x):
    try: return float(str(x).replace(',','.'))
    except: return None
meta={(r['quarter'],r['fund_id']):r for r in F}
comp=re.compile(r'msci|omrx|bond|world|acwi|ftse|bloomberg|hfrx|t-bill|t-bond|stoxx|nordic|norden|vinx|europe|global',re.I)
swe=re.compile(r'stockholm benchmark|omxsb|six portfolio|six return|sixrx|morningstar sweden|solactive sweden|msci sweden|omx stockholm|sweden|sverige',re.I)
omxsb=re.compile(r'stockholm benchmark|omxsb',re.I)
idxname=re.compile(r'index|access|indexnära|passiv|zero|exponering',re.I)
def grp(m):
    bm=m['benchmark'] or ''; name=m['fund_name'] or ''; ar=fl(m['active_risk'])
    single=bool(swe.search(bm)) and not comp.search(bm.replace('Sweden','').replace('Sverige',''))
    if single and omxsb.search(bm) and ((ar is not None and ar<1.5) or idxname.search(name)): return 'tracker'
    if omxsb.search(bm): return 'bench_omxsb'      # active or balanced funds with OMXSB in benchmark
    if swe.search(bm) and not comp.search(bm.replace('Sweden','').replace('Sverige','')): return 'other_swe_single'  # SIX/other Swedish single-index funds (active or passive)
    return 'other'
G={k:grp(m) for k,m in meta.items()}
hold=collections.defaultdict(float)
for h in H:
    a=fl(h['antal'])
    if a is not None: hold[(h['quarter'],h['fund_id'],h['isin'])]+=a
byqi=collections.defaultdict(list)
for (q,f,i),a in hold.items(): byqi[(q,i)].append((f,a))
groups=['tracker','bench_omxsb','other_swe_single','other']
out=[]
for e in E:
    S=fl(e['shares_qa'])
    if not S: continue
    isins=[s for s in re.split(r'[;,| ]+',e['isins']) if s]
    d={g:0.0 for g in groups}
    for i in isins:
        for q,sgn in ((e['qb'],-1),(e['qa'],1)):
            for f,a in byqi.get((q,i),[]):
                g=G.get((e['qb'],f)) or G.get((q,f)) or 'other'
                d[g]+=sgn*a
    r={'type':e['type'],'AD':e['AD']}; r.update({g:100*d[g]/S for g in groups}); out.append(r)
random.seed(3)
def rt(rows,k):
    by=collections.defaultdict(list)
    for r in rows: by[r['AD']].append(r[k])
    m=[st.mean(v) for v in by.values()]; Gn=len(m); mu=st.mean(m); se=st.stdev(m)/math.sqrt(Gn)
    c=sum(1 for _ in range(20000) if abs(st.mean(x*random.choice((-1,1)) for x in m))>=abs(mu))
    return f"{mu:+.3f} (se {se:.3f}, p {c/20000:.3f}, {sum(x>0 for x in m)}/{Gn}>0)"
labels={'tracker':'OMXSB trackers','bench_omxsb':'Active/balanced funds benchmarked to OMXSB','other_swe_single':'Other single-Swedish-index funds (SIX etc.)','other':'All other funds'}
for typ in ['addition','deletion']:
    rows=[r for r in out if r['type']==typ]; print(typ.upper(),len(rows))
    for g in groups: print(f"  {labels[g]:48s} {rt(rows,g)}")
