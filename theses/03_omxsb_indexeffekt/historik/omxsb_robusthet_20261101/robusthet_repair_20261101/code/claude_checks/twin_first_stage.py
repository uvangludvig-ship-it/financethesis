import pandas as pd, re, zipfile, glob, os, xml.etree.ElementTree as ET, collections
R='/home/claude/uvangludvig-ship-it/financethesis'
tw=pd.read_csv('/home/claude/agent_scratch/twin_events.csv'); tw=tw[(tw.usable_pair==True)]
tw['AD']=pd.to_datetime(tw.AD); tw=tw[tw.AD>='2019-01-01']
st=pd.read_csv(f'{R}/data/raw/lseg/panel_2005_2026/stocks_static_2005.csv')
isin=dict(zip(st.ric,st.IssueISIN))
nt=pd.read_csv(f'{R}/output/omxsb_replication_2007/nettrading_omxsb.csv')
evinfo=nt.set_index('event_id')[['isins','qb','qa','shares_qa']]
tw=tw.join(evinfo,on='event_id')
tw['sister_isin']=tw.sister_ric.map(isin)
MAN={('SSAB','A'):'SE0000171100',('SSAB','B'):'SE0000120669',('VOLV','A'):'SE0000115420',('VOLV','B'):'SE0000115446',
     ('INDU','A'):'SE0000190126',('INDU','C'):'SE0000107203',('KLOV','A'):'SE0006593901',('CORE','A'):'SE0010714279',
     ('KINV','A'):'SE0015810239',('NCC','A'):'SE0000118952'}
import re as _re
def _root(r): return _re.match(r'([A-Z]+?)[a-z]?\.ST',str(r)).group(1) if _re.match(r'([A-Z]+?)[a-z]?\.ST',str(r)) else ''
tw['sister_isin']=[MAN.get((_root(r),c),i) for r,c,i in zip(tw.sister_ric,tw.sister_class,tw.sister_isin)]
# tracker fund ids per quarter (same rule as split_others.py)
f=pd.read_csv('/home/claude/fi_check/parsed/funds.csv')
f['ar']=pd.to_numeric(f.active_risk.astype(str).str.replace(',','.'),errors='coerce')
comp=re.compile(r'msci|omrx|bond|world|acwi|ftse|bloomberg|t-bill|t-bond|stoxx|nordic|norden|vinx|europe|global',re.I)
omx=re.compile(r'stockholm benchmark|omxsb',re.I); swe=re.compile(r'stockholm benchmark|omxsb|six|sweden|sverige|omx stockholm',re.I)
idxn=re.compile(r'index|access|indexnära|passiv|zero|exponering',re.I)
def is_tracker(r):
    bm=r.benchmark if isinstance(r.benchmark,str) else ''; nm=r.fund_name if isinstance(r.fund_name,str) else ''
    single=bool(swe.search(bm)) and not comp.search(bm.replace('Sweden','').replace('Sverige',''))
    return single and bool(omx.search(bm)) and ((r.ar==r.ar and r.ar<1.5) or bool(idxn.search(nm)))
f['tracker']=f.apply(is_tracker,axis=1)
trk={q:set(g.fund_id.astype(str)) for q,g in f[f.tracker].groupby('quarter')}
NS='{http://schemas.fi.se/publika/vardepappersfonder/20200331}'
zips={re.search(r'(\d{4}Q\d)',z).group(1):z for z in glob.glob(f'{R}/data/raw/fi/Fondinnehav_*.zip')}
def qlab(d): d=pd.Timestamp(d); return f'{d.year}Q{(d.month-1)//3+1}'
want=collections.defaultdict(set)
for _,r in tw.iterrows():
    for q in [r.qb,r.qa]:
        if isinstance(q,str): want[qlab(q)] |= {s for s in re.split(r'[;,| ]+',str(r.isins)) if s} | ({r.sister_isin} if isinstance(r.sister_isin,str) else set())
hold=collections.defaultdict(float)
for q,isins in want.items():
    if q not in zips: continue
    z=zipfile.ZipFile(zips[q]); qd=[k for k in trk if qlab(k)==q]; ids=trk[qd[0]] if qd else set()
    for n in z.namelist():
        if not n.lower().endswith('.xml'): continue
        try: root=ET.fromstring(z.read(n))
        except Exception: continue
        fe=root.find('.//'+NS+'Fond_institutnummer')
        if fe is None or (fe.text or '').strip() not in ids: continue
        for it in root.iter(NS+'FinansielltInstrument'):
            i=it.find(NS+'ISIN-kod_instrument'); a=it.find(NS+'Antal')
            if i is not None and i.text in isins and a is not None and a.text:
                hold[(q,i.text)]+=float(a.text.replace(',','.'))
rows=[]
for _,r in tw.iterrows():
    if not isinstance(r.qb,str): continue
    qb,qa=qlab(r.qb),qlab(r.qa)
    ev=[s for s in re.split(r'[;,| ]+',str(r.isins)) if s]
    e_b=sum(hold[(qb,i)] for i in ev); e_a=sum(hold[(qa,i)] for i in ev)
    s_b=hold[(qb,r.sister_isin)]; s_a=hold[(qa,r.sister_isin)]
    rows.append(dict(review=r.review_cycle,company=r.company,type=r.type,cls=r.class_changed,sister=r.sister_class,
        sister_in_idx=bool(r.sister_member_before and r.sister_member_after),
        event_class_chg_pct=100*(e_a-e_b)/r.shares_qa if r.shares_qa==r.shares_qa else None,
        event_class_chg_mn=(e_a-e_b)/1e6, sister_chg_mn=(s_a-s_b)/1e6, sister_hold_before_mn=s_b/1e6))
out=pd.DataFrame(rows); out.to_csv('/home/claude/scripts/twin_first_stage_output.csv',index=False)
pd.set_option('display.width',200)
print(out.round(3).to_string(index=False))
