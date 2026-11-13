import csv, sys, re, collections, statistics as st
funds_csv, hold_csv, ev_csv = sys.argv[1:4]
F=list(csv.DictReader(open(funds_csv))); H=list(csv.DictReader(open(hold_csv))); E=list(csv.DictReader(open(ev_csv)))
def fl(x):
    try: return float(str(x).replace(',','.'))
    except: return None
filed=collections.defaultdict(set)   # quarter -> set of fund_ids that filed with >0 instruments
for r in F:
    if (fl(r['n_instr']) or 0)>0: filed[r['quarter']].add(r['fund_id'])
hold=collections.defaultdict(float)
for h in H:
    a=fl(h['antal'])
    if a is not None: hold[(h['quarter'],h['fund_id'],h['isin'])]+=a
tot_sell=tot_sell_dropout=tot_buy=tot_buy_dropin=0.0; n=0
by=collections.defaultdict(lambda:[0,0,0,0])
for e in E:
    if e['type']!='addition': continue
    S=fl(e['shares_qa'])
    if not S: continue
    isins=[s for s in re.split(r'[;,| ]+',e['isins']) if s]; qb,qa=e['qb'],e['qa']
    funds=set(f for (q,f,i) in hold if i in isins and q in (qb,qa))
    s=sd=b=bd=0.0
    for f in funds:
        bh=sum(hold.get((qb,f,i),0) for i in isins); ah=sum(hold.get((qa,f,i),0) for i in isins); d=ah-bh
        if d<0:
            s+=-d
            if f not in filed[qa]: sd+=-d
        elif d>0:
            b+=d
            if f not in filed[qb]: bd+=d
    by[e['AD']][0]+=100*s/S; by[e['AD']][1]+=100*sd/S; by[e['AD']][2]+=100*b/S; by[e['AD']][3]+=100*bd/S
    n+=1; tot_sell+=100*s/S; tot_sell_dropout+=100*sd/S; tot_buy+=100*b/S; tot_buy_dropin+=100*bd/S
print('additions',n)
print(f'gross selling (all funds) mean {tot_sell/n:.3f}% ; of which fund did NOT file at qa (dropout) {tot_sell_dropout/n:.3f}% -> share {tot_sell_dropout/tot_sell:.0%}')
print(f'gross buying  (all funds) mean {tot_buy/n:.3f}% ; of which fund did NOT file at qb (new/drop-in) {tot_buy_dropin/n:.3f}% -> share {tot_buy_dropin/tot_buy:.0%}')
