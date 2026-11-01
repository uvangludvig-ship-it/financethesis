import csv, sys, re, math, random, statistics as st, collections
funds_csv, hold_csv, ev_csv = sys.argv[1:4]
F = list(csv.DictReader(open(funds_csv)))
H = list(csv.DictReader(open(hold_csv)))
E = list(csv.DictReader(open(ev_csv)))
def fl(x):
    try: return float(str(x).replace(',','.'))
    except: return None
meta = {(r['quarter'], r['fund_id']): r for r in F}
comp = re.compile(r'msci|omrx|bond|world|acwi|ftse|bloomberg|hfrx|t-bill|t-bond|stoxx|nordic|norden|vinx|europe|global|ränte|obligation', re.I)
swe = re.compile(r'stockholm benchmark|omxsb|six portfolio|six return|sixrx|morningstar sweden|solactive sweden|msci sweden|omx stockholm|sweden|sverige', re.I)
omxsb = re.compile(r'stockholm benchmark|omxsb', re.I)
idxname = re.compile(r'index|access|indexnära|passiv|zero|exponering', re.I)
def classify(m):
    bm = m['benchmark'] or ''; name = m['fund_name'] or ''; ar = fl(m['active_risk'])
    single_swe = bool(swe.search(bm)) and not comp.search(bm.replace('Sweden','').replace('Sverige',''))
    strict = single_swe and bool(omxsb.search(bm)) and ((ar is not None and ar < 1.5) or bool(idxname.search(name)))
    broad = single_swe and ((ar is not None and ar < 1.5) or bool(idxname.search(name)))
    return strict, broad
cls = {k: classify(m) for k, m in meta.items()}
hold = collections.defaultdict(float)  # (q, fund, isin) -> antal
for h in H:
    a = fl(h['antal'])
    if a is not None: hold[(h['quarter'], h['fund_id'], h['isin'])] += a
byqi = collections.defaultdict(list)
for (q,f,i),a in hold.items(): byqi[(q,i)].append((f,a))
out=[]
for e in E:
    isins=[s for s in re.split(r'[;,| ]+',e['isins']) if s]
    qb,qa=e['qb'],e['qa']; S=fl(e['shares_qa']); fac=fl(e['f']) or 1.0
    if not S: continue
    tot={'all_b':0,'all_a':0,'s_b':0,'s_a':0,'b_b':0,'b_a':0}
    for i in isins:
        for q,side in ((qb,'b'),(qa,'a')):
            for f,a in byqi.get((q,i),[]):
                # classification ex ante: use fund's status at qb (if missing, at q)
                c = cls.get((qb,f)) or cls.get((q,f)) or (False,False)
                aa = a*(fac if side=='b' else 1.0)
                tot['all_'+side]+=aa
                if c[0]: tot['s_'+side]+=aa
                if c[1]: tot['b_'+side]+=aa
    r=dict(event=e['event_id'],type=e['type'],AD=e['AD'],tot=fl(e['tot']),
           repo_all_b=fl(e['all_b']),repo_all_a=fl(e['all_a']),repo_nt=fl(e['nt']),repo_act=fl(e['activebuy']),
           dF=100*(tot['all_a']-tot['all_b'])/S,
           nt_strict=100*(tot['s_a']-tot['s_b'])/S, nt_broad=100*(tot['b_a']-tot['b_b'])/S,
           all_b=tot['all_b'],all_a=tot['all_a'])
    r['act_strict']=r['dF']-r['nt_strict']; r['act_broad']=r['dF']-r['nt_broad']
    out.append(r)
# validation vs repo totals
dev=[abs(r['all_b']-r['repo_all_b'])/max(r['repo_all_b'],1) for r in out if r['repo_all_b'] is not None]
dev2=[abs(r['all_a']-r['repo_all_a'])/max(r['repo_all_a'],1) for r in out if r['repo_all_a'] is not None]
print('events',len(out),'| all-fund holdings vs repo: median rel dev before',round(st.median(dev),4),'after',round(st.median(dev2),4),'| share within 1%:',round(sum(d<0.01 for d in dev)/len(dev),3),round(sum(d<0.01 for d in dev2)/len(dev2),3))
random.seed(7)
def review_test(rows,k):
    by=collections.defaultdict(list)
    for r in rows:
        if r[k] is not None: by[r['AD']].append(r[k])
    m=[st.mean(v) for v in by.values()]; G=len(m); mu=st.mean(m); se=st.stdev(m)/math.sqrt(G)
    B=20000; c=sum(1 for _ in range(B) if abs(st.mean(x*random.choice((-1,1)) for x in m))>=abs(mu))
    return f"{mu:+.3f} (se {se:.3f}, t {mu/se:+.2f}, p {c/B:.4f}, {sum(x>0 for x in m)}/{G}>0)"
for typ in ['addition','deletion']:
    rows=[r for r in out if r['type']==typ]
    print(f"\n{typ.upper()} N={len(rows)}")
    for k,lab in [('dF','All Swedish funds (classification-free)'),('repo_nt','Index funds, repo classification'),('repo_act','Active funds, repo classification'),
                  ('nt_strict','Index funds, STRICT (OMXSB trackers, ex ante)'),('act_strict','Everyone else, STRICT'),
                  ('nt_broad','Index funds, BROAD (any single Swedish index, ex ante)'),('act_broad','Everyone else, BROAD'),('tot','CAR total window')]:
        print(f"  {lab:55s} {review_test(rows,k)}")
# who are the strict index funds (2024Q2) for sanity
print('\nSTRICT index funds at 2024-06-30:')
for (q,f),c in cls.items():
    if q=='2024-06-30' and c[0]: print('  ',meta[(q,f)]['fund_name'],'|',meta[(q,f)]['benchmark'][:50],'| AR',meta[(q,f)]['active_risk'])
print('BROAD-only (not strict) at 2024-06-30:')
for (q,f),c in cls.items():
    if q=='2024-06-30' and c[1] and not c[0]: print('  ',meta[(q,f)]['fund_name'],'|',meta[(q,f)]['benchmark'][:50],'| AR',meta[(q,f)]['active_risk'])
csv.DictWriter(open('data/fi_check/recomputed_events.csv','w',newline=''),fieldnames=list(out[0].keys())).writerows([dict(zip(out[0].keys(),out[0].keys()))]+out)
