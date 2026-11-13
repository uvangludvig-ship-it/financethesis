"""Extract downloaded AP holdings with provenance, source-date checks and RIC review flags.

Run with --out pointing at a new directory. Requires Poppler pdftotext.
Original PDFs and event files are never changed.
"""
import argparse, collections, csv, datetime as dt, difflib, hashlib, json, pathlib, re, subprocess, unicodedata
from decimal import Decimal

ROOT=pathlib.Path(__file__).resolve().parents[2]
RAW=ROOT/'data/raw/ap'
META=RAW/'_collection_20261031'
ISIN=r'[A-Z]{2}[A-Z0-9]{9}[0-9]'
N=r'-?(?:\d{1,3}(?: \d{3})+|\d+)(?:,\d+)?'

def number(s, english=False):
    s=s.strip().replace('−','-').replace(' ','').replace('\u00a0','')
    return Decimal(s.replace(',','' if english else '.'))

def asof(text):
    head=text[:500]
    verbal=re.search(r'(30|31)\s+(Jun\w*|Dec\w*)\s+(20\d\d)',head,re.I)
    if verbal:return f'{verbal[3]}-{"06" if verbal[2].lower().startswith("jun") else "12"}-{verbal[1]}'
    m=re.search(r'(20\d\d)-(\d\d)-(\d\d)',head)
    if m:return m.group()
    m=re.search(r'(30|31)\s+(Jun\w*|Dec\w*)\s+(20\d\d)',head,re.I)
    if m:return f'{m[3]}-{"06" if m[2].lower().startswith("jun") else "12"}-{m[1]}'
    raise ValueError('No source date: '+head[:100])

def write_csv(path,rows,fields=None):
    with path.open('x',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields or list(rows[0]))
        writer.writeheader();writer.writerows(rows)

def extract(job):
    path=ROOT/job['local_path']; fund=job['fund']
    text=subprocess.check_output(['pdftotext','-layout',str(path),'-'],text=True)
    date=asof(text)
    if not date.endswith(('06-30','12-31')):
        return [],[],dict(fond=fund,datum=date,kallfil=job['local_path'],status='excluded_wrong_date',rows=0,source_total_sek='',extracted_total_sek='',difference_sek='')
    rows=[]; rejects=[]; total=None; parent=''; parent_index=None; active=False; ended=False
    control_method='text'
    if fund=='AP4' and date=='2026-06-30':
        # This PDF's section headings/total are vector outlines, absent from pdftotext.
        # Visually verified on original page 3: SUMMA SVENSKA AKTIER, NOTERADE 144 755 MSEK.
        text='\f'.join(text.split('\f')[:3]);total=Decimal('144755000000');control_method='visual_original_PDF_page_3'
    scale=1_000 if fund!='AP4' else (1 if '(kr)' in text[:150].lower() else 1_000_000)
    for page,part in enumerate(text.split('\f'),1):
        for lineno,line in enumerate(part.splitlines(),1):
            s=line.strip(); parsed=None; isin=''; source_isin=''; ticker=''; selection='fund_swedish_equity_list'; excluded=''; aggregate=False
            if not s:continue
            if fund=='AP1':
                if not s.startswith('Equity '):continue
                m=re.match(r'^Equity\s+(.*?)\s+([\d,]+)\s+([\d,]+)(?:\s+('+ISIN+r'))?\s*$',s)
                if m:
                    name,value,shares,isin=m.groups();isin=isin or '';parsed=(name,number(shares,True),number(value,True));selection='SE_ISIN_or_swedish_list_crosscheck'
            elif fund=='AP2':
                m=re.match(r'^(.*?)\s+('+ISIN+r')\s+([A-Z]{2})\s+('+N+r')\s{2,}('+N+r')(?:\s|$)',s)
                if m:
                    name,isin,country,shares,value=m.groups();parsed=(name,number(shares),number(value))
                elif not re.search(ISIN,s):continue
            elif fund=='AP3':
                if 'Security name' in text[:600]:
                    m=re.match(r'^(.*?)\s+(\S+\s+S[SF])\s+Equity\s+SEK\s+([\d,.]+)\s+([\d,.]+)\s+('+ISIN+r')\s*$',s)
                    if m:
                        name,ticker,shares,value,isin=m.groups();parsed=(name,number(shares,True),number(value,True))
                    elif not re.search(r'\bEquity\s+SEK\b',s):continue
                else:
                    english=date>='2024-12-31'
                    numeric=r'[\d,.]+' if english else N
                    m=re.match(r'^SEK\s+(?:/EQUITY/SHARE-LISTED/EQ|EQUITY|EQ)\s+(.*?)\s+('+numeric+r')\s{2,}('+numeric+r')\s+.*?('+ISIN+r')\s*$',s)
                    if m:
                        name,shares,value,isin=m.groups();parsed=(name,number(shares,english),number(value,english))
                    elif not re.match(r'^SEK\s+(?:/EQUITY/SHARE-LISTED/EQ|EQUITY|EQ)\s',s):continue
            elif fund=='AP4':
                modern=date>='2020-12-31'
                if modern:
                    if ended:continue
                    if re.match(r'Summa svenska aktier',s,re.I):
                        vals=re.findall(N,s);total=number(vals[-1])*scale if vals else None; ended=True;continue
                    if re.search(r'(?:UTLÄNDSKA AKTIER|Utländska aktier)',s):ended=True;continue
                    # Land SE is the source's Swedish market classification (not ISIN domicile).
                    modern_n=r'(?:'+N+r'|\d+\.\d+)'
                    m=re.match(r'^(.*?)\s+SE\s+('+modern_n+r')\s{2,}('+N+r')\s+('+ISIN+r'(?:/\d+)?|-)(?:\s+(.*))?$',s)
                    if m:
                        name,shares,value,isin,tail=m.groups();parsed=(name,number(shares),number(value)); ticker=' '.join((tail or '').split()[:2]); selection='source_country_SE'
                        if '/' in isin:source_isin=isin;isin='';aggregate=True
                        if isin=='-':isin=''
                    elif not re.search(r'\sSE\s+\d',s):continue
                else:
                    if re.match(r'^Sverige\s+Antal',s):active=True;continue
                    if s.startswith('Summa verkligt värde noterade aktier Sverige'):
                        total=number(s.split('Sverige')[-1])*scale;active=False;continue
                    if not active:continue
                    m=re.match(r'^(.*?)\s+('+N+r')\s{2,}('+N+r')(?:\s+(.*))?$',s)
                    if m:
                        name,shares,value,tail=m.groups(); tail=tail or ''
                        tick=re.search(r'\S+:(?:SS|SF)',tail)
                        if not tick:
                            if name.lower().startswith(('summa','page','noterade','sverige')):continue
                            parent=name;parent_index=len(rows);aggregate=True
                        ticker=tick.group() if tick else '';name=name.strip()
                        if re.fullmatch(r'A|B|C|D|Pref|Preferens|Stam|Aktier|Rätter',name,re.I):
                            name=re.sub(r'\s+[ABCD]$','',parent)+' '+name
                            if parent_index is not None:rows[parent_index]['excluded']='aggregate_parent_with_share_class_children'
                        parsed=(name,number(shares),number(value));selection='source_Sverige_section'
                    elif not re.search(r':S[SF]\b',s):continue
            if parsed:
                name,shares,value=parsed
                # Subscription rights, warrants and ETFs are not shares.
                if re.search(r'\b(?:RTS|RIGHTS?|WARRANTS?|ETF|ETFS)\b|\b(?:BTA|BTR|TR)\b',name,re.I):excluded='non_share_instrument'
                if 'Rätter' in name or re.search(r'(?:BTA|BTR|TR)(?:[: ]S[SF])',ticker):excluded='non_share_instrument'
                if 'proventus capital' in name.lower() or 'debenture' in name.lower():excluded='private_credit_fund_or_debenture_not_listed_share'
                rows.append(dict(fond=fund,datum=date,bolagsnamn=name.strip(),ISIN=isin,antal_aktier=str(shares),marknadsvarde=str(value*scale),kallfil=job['local_path'],kallsida=page,kallrad=lineno,kallurl=job['url'],kallticker=ticker,kall_ISIN=source_isin or isin,samlat_aktieslag=str(aggregate).lower(),kallenhet='SEK' if scale==1 else ('TSEK' if scale==1000 else 'MSEK'),urvalsgrund=selection,excluded=excluded))
            else:rejects.append(dict(fond=fund,datum=date,kallfil=job['local_path'],sida=page,rad=lineno,text=s))
    gross=sum(Decimal(r['marknadsvarde']) for r in rows if r['excluded']!='aggregate_parent_with_share_class_children')
    return rows,rejects,dict(fond=fund,datum=date,kallfil=job['local_path'],status='parsed' if not rejects else 'parse_review',rows=len(rows),source_total_sek=str(total) if total is not None else '',extracted_total_sek=str(gross),difference_sek=str(gross-total) if total is not None else '',control_method=control_method)

def normalize(name):
    s=unicodedata.normalize('NFKD',name.casefold());s=''.join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r'\b(?:aktiebolaget|aktiebolag|ab|publ|ser|series|class|shares|shs|ord|plc|ltd|limited|inc|corporation|corp)\b',' ',s)
    s=re.sub(r'[^a-z0-9]+',' ',s)
    return ' '.join(s.split())

def base_name(name):return re.sub(r'\s+[abcd]$','',normalize(name))

def match_rows(rows):
    events=list(csv.DictReader((ROOT/'data/input/omxsb/omxsb_events_with_ric_2007_2026.csv').open()))
    byisin=collections.defaultdict(list);byname=collections.defaultdict(list);bybase=collections.defaultdict(list)
    event_rics=collections.defaultdict(list)
    for e in events:
        if e['isin']:byisin[e['isin']].append(e)
        byname[normalize(e['company'])].append(e);bybase[base_name(e['company'])].append(e)
        if e['RIC']:event_rics[e['RIC']].append(e)
    # Local LSEG security metadata supplies identifiers for event rows with a blank ISIN.
    static_byisin=collections.defaultdict(list)
    for rel in ('data/raw/lseg/panel_2012_2026/stocks_static.csv','data/raw/lseg/panel_2005_2026/stocks_static_2005.csv'):
        for sec in csv.DictReader((ROOT/rel).open(encoding='utf-8-sig')):
            if sec.get('IssueISIN') and sec.get('ric') in event_rics:
                static_byisin[sec['IssueISIN']]+=event_rics[sec['ric']]
    for r in rows:
        candidates=[];method='unmatched';uncertain=True;ric=''
        if r['ISIN'] and r['ISIN'] in byisin:
            candidates=byisin[r['ISIN']];method='exact_isin'
        elif r['ISIN'] and r['ISIN'] in static_byisin:
            candidates=static_byisin[r['ISIN']];method='exact_isin_via_local_LSEG_event_RIC'
        elif normalize(r['bolagsnamn']) in byname:
            candidates=byname[normalize(r['bolagsnamn'])];method='normalized_name'
        elif base_name(r['bolagsnamn']) in bybase:
            candidates=bybase[base_name(r['bolagsnamn'])];method='company_name_share_class_review'
        else:
            near=difflib.get_close_matches(normalize(r['bolagsnamn']),byname,n=3,cutoff=.75)
            candidates=[e for n in near for e in byname[n]]
            if candidates:method='fuzzy_suggestion_only'
        rics=sorted({e['RIC'] for e in candidates if e['RIC']})
        conflicting_isin=bool(not method.startswith('exact_isin') and r['ISIN'] and candidates and all(e['isin'] and e['isin']!=r['ISIN'] for e in candidates))
        # No automatic fuzzy or share-class inference. Exact identifiers/names must resolve to one RIC.
        if len(rics)==1 and (method.startswith('exact_isin') or method=='normalized_name') and not conflicting_isin and r['samlat_aktieslag']!='true':
            ric=rics[0];uncertain=not method.startswith('exact_isin')
        if conflicting_isin:method+=';source_event_isin_conflict'
        r.update(RIC=ric,matchningsmetod=method,osaker_matchning=str(uncertain).lower(),RIC_kandidater='|'.join(rics),event_bolagsnamn='|'.join(sorted({e['company'] for e in candidates})),event_ISIN='|'.join(sorted({e['isin'] for e in candidates if e['isin']})))
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args();out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=False)
    jobs=json.loads((META/'download_manifest.json').read_text())
    rows=[];rejects=[];checks=[]
    for job in jobs:
        if job['fund'] in ('AP2','AP3') and not re.search('svenska aktier',job['text'],re.I):continue
        got,bad,check=extract(job);rows+=got;rejects+=bad;checks.append(check)
    # AP1 has no market field. Crosscheck foreign ISINs against contemporary Swedish
    # holdings of AP2/AP3/AP4; retain explicit provenance for this inferred classification.
    # Primary issuer references for these exceptions are in classification_sources.csv.
    foreign_market_isins={'LU1778762911','US2575592033','CA76131D1033','US7311054099'}
    for r in rows:
        if r['ISIN'] in foreign_market_isins and not r['excluded']:r['excluded']='foreign_listing_in_source_Swedish_portfolio'
    domestic={(r['datum'],r['ISIN']) for r in rows if r['fond']!='AP1' and r['ISIN'] and not r['excluded']}
    for r in rows:
        if r['fond']=='AP1':
            if r['ISIN'].startswith('SE'):r['urvalsgrund']='AP1_SE_ISIN'
            elif (r['datum'],r['ISIN']) in domestic:r['urvalsgrund']='AP1_same_date_ISIN_in_other_AP_swedish_list_market_unverified'
            elif not r['excluded']:r['excluded']='not_identified_as_swedish'
    excluded=[r for r in rows if r['excluded']];rows=[r for r in rows if not r['excluded']]
    rows=match_rows(rows);rows.sort(key=lambda r:(r['fond'],r['datum'],r['bolagsnamn'],r['ISIN']))
    for r in rows:
        flags=[]
        if not r['ISIN']:flags.append('source_ISIN_missing_or_combined')
        if r['samlat_aktieslag']=='true':flags.append('share_classes_not_separable')
        if Decimal(r['marknadsvarde'])==0:flags.append('zero_source_value_listing_not_independently_verified')
        if r['urvalsgrund'].startswith('AP1_same'):flags.append('AP1_market_inferred_from_same_ISIN')
        if r['osaker_matchning']=='true':flags.append('RIC_requires_review_or_unmatched')
        r['datakvalitetsflaggor']='|'.join(flags)
    base=['fond','datum','bolagsnamn','ISIN','antal_aktier','marknadsvarde']
    labels={'antal_aktier':'antal aktier','marknadsvarde':'marknadsvärde'}
    write_csv(out/'ap_svenska_aktier_2013_2026.csv',[{labels.get(k,k):r[k] for k in base} for r in rows],[labels.get(k,k) for k in base])
    write_csv(out/'ap_svenska_aktier_med_ric.csv',rows)
    write_csv(out/'matchningar_att_granska.csv',[r for r in rows if r['osaker_matchning']=='true'],list(rows[0]))
    write_csv(out/'parse_rejections.csv',rejects,['fond','datum','kallfil','sida','rad','text'])
    write_csv(out/'source_checks.csv',checks,['fond','datum','kallfil','status','rows','source_total_sek','extracted_total_sek','difference_sek','control_method'])
    write_csv(out/'excluded_rows.csv',excluded,list(excluded[0]))
    print(json.dumps({'rows':len(rows),'source_checks':len(checks),'parse_rejections':len(rejects),'fund_rows':dict(collections.Counter(r['fond'] for r in rows)),'match_methods':dict(collections.Counter(r['matchningsmetod'] for r in rows))},indent=2))

if __name__=='__main__':main()
