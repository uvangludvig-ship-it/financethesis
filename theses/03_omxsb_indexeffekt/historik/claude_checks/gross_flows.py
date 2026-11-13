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
def tracker(m):
    bm=m['benchmark'] or ''; name=m['fund_name'] or ''; ar=fl(m['active_risk'])
    single=bool(swe.search(bm)) and not comp.search(bm.replace('Sweden','').replace('Sverige',''))
    return single and bool(omxsb.search(bm)) and ((ar is not None and ar<1.5) or bool(idxname.search(name)))
hold=collections.defaultdict(float)
for h in H:
    a=fl(h['antal'])
    if a is not None: hold[(h['quarter'],h['fund_id'],h['isin'])]+=a
rows=[]
for e in E:
    if e['type']!='addition': continue
    S=fl(e['shares_qa']); 
    if not S: continue
    isins=[s for s in re.split(r'[;,| ]+',e['isins']) if s]
    qb,qa=e['qb'],e['qa']
    funds=set(f for (q,f,i) in hold if i in isins and q in (qb,qa))
    gb=gs=0.0; nb=ns=0; tr=0.0
    for f in funds:
        b=sum(hold.get((qb,f,i),0) for i in isins); a=sum(hold.get((qa,f,i),0) for i in isins)
        m=meta.get((qb,f)) or meta.get((qa,f))
        d=a-b
        if m and tracker(m): tr+=d; continue
        if d>0: gb+=d; nb+=1
        elif d<0: gs+=-d; ns+=1
    rows.append(dict(AD=e['AD'],tracker=100*tr/S,gross_buy=100*gb/S,gross_sell=100*gs/S,n_buy=nb,n_sell=ns,car=fl(e['tot'])))
def revmean(k):
    by=collections.defaultdict(list)
    for r in rows:
        if r[k] is not None: by[r['AD']].append(r[k])
    return st.mean(st.mean(v) for v in by.values())
print('Additions N=',len(rows))
for k in ['tracker','gross_buy','gross_sell','n_buy','n_sell','car']:
    print(f"  {k:10s} event-mean {st.mean(r[k] for r in rows if r[k] is not None):7.3f} | review-mean {revmean(k):7.3f}")
share_events_with_sellers=sum(1 for r in rows if r['n_sell']>0)/len(rows)
print('  share of additions where at least one non-tracker fund sold:',round(share_events_with_sellers,2))
print('  gross selling as % of tracker buying (review means):',round(revmean('gross_sell')/revmean('tracker'),2))
print('  M event-means:',round(st.mean(r['car'] for r in rows)/st.mean(r['tracker'] for r in rows),2),'| M review-means:',round(revmean('car')/revmean('tracker'),2))
