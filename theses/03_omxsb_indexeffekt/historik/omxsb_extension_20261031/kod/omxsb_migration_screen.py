#!/usr/bin/env python3
"""Bounded cross-index screen; immutable repository inputs, local saved primary extracts.

Uses only stdlib. No regressions, downloads, or edits to source inputs. An ordinary-list
difference is a candidate transition, not proof of membership immediately before ED.
"""
import argparse, csv, datetime as dt, hashlib, json, re, unicodedata, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

def norm(s):
    return re.sub('[^A-Z0-9]', '', unicodedata.normalize('NFKD', s.upper()).encode('ascii','ignore').decode())

def write_csv(p, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for row in rows for k in row))
    with p.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields);w.writeheader();w.writerows(rows)

def source_block(p, contains):
    blocks=[b.lstrip() for b in p.read_text().split('--------------------------------------------------------------------------------')]
    b=next(b for b in blocks if contains in b.split('\n')[0])
    return re.sub(r'^L\d+: ?', '', b, flags=re.M)

def names_from(b, multi=False):
    if multi:
        b=b.split('### Solactive ISS ESG Screened Sweden Small Cap Tradable Index:')[1]
    marker=re.search(r'In the ordinary (?:rebalance|adjustment).*?effective open[^\n]*:\s*\n', b)
    if not marker: raise ValueError('composition marker missing')
    lines=b[marker.end():].splitlines(); names=[]
    for l in lines:
        l=l.strip()
        if not l: continue
        if l.startswith(('*','Index name','#','©','【')): break
        names.append(l.upper())
    assert 95<=len(names)<=101, (len(names),names[-3:])
    assert len(set(names))==len(names)
    return names

def main():
    a=argparse.ArgumentParser();a.add_argument('--repo',required=True);a.add_argument('--source-dir',required=True);a.add_argument('--output',required=True)
    args=a.parse_args();R=Path(args.repo);S=Path(args.source_dir);O=Path(args.output);O.mkdir(parents=True,exist_ok=True)
    specs=[
      ('2023-06-01','2023-05-10','web_2023h1_2024h1.txt','1st-june-2023/',True),
      ('2023-12-01','2023-11-13','web_main_domain.txt','1st-december-2023/',False),
      ('2024-06-03','2024-05-10','search_2023_2024.txt','3rd-june-2024/',False),
      ('2024-12-02','2024-11-08','web_main_domain.txt','2nd-december-2024/',False),
      ('2025-06-02','2025-05-21','web_2025h1.txt','2nd-june-2025/',False),
      ('2025-12-01','2025-11-19','web_5.txt','announcements/55260',False)]
    snapshots=[]; bydate={}; sourcerows=[]
    for date,ad,fn,match,multi in specs:
        b=source_block(S/fn,match);names=names_from(b,multi)
        url=re.search(r'\((https://[^)]+)\)',b.split('\n')[0]).group(1)
        bydate[date]=names
        sourcerows.append(dict(effective_open=date,announced=ad,count=len(names),url=url,extract=fn,retrieved='2026-10-31',access='web_tool_cached_primary_extract; direct_HTML_returned_404'))
        snapshots += [dict(effective_open=date,solactive_name=n,source_url=url) for n in names]
    write_csv(O/'solactive_snapshots.csv',snapshots);write_csv(O/'source_register.csv',sourcerows)
    changes=[]
    dates=sorted(bydate)
    for prev,date in zip(dates,dates[1:]):
        for typ,names in [('addition',set(bydate[date])-set(bydate[prev])),('deletion',set(bydate[prev])-set(bydate[date]))]:
            changes += [dict(previous_snapshot=prev,effective_open_candidate=date,solactive_name=n,type=typ,status='adjacent_ordinary_snapshot_difference; offcycle_not_fully_excluded') for n in sorted(names)]
    write_csv(O/'solactive_snapshot_differences.csv',changes)
    sb=list(csv.DictReader(open(R/'data/input/omxsb/omxsb_changes_2007_2026.csv')))
    cars={x['event_id']:x for x in csv.DictReader(open(R/'output/omxsb_audit_20261031/corrected/events_car.csv'))}
    # Conservative issuer screening only. The two positive candidates receive exact ISIN validation below.
    aliases={'BEIJER':'BEIJER REF','SWEDISH':'SWEDISH LOGISTIC','SAMHALLSBYGGNADSBO':'SAMHALLSBYGGNADSBOLAGET','LUNDBERGFORETAGEN':'L E LUNDBERGFORETAGEN'}
    screen=[]; candidates=[]
    for e in sb:
        if e['effective_date'] not in dates[1:]:continue
        date=e['effective_date'];prev=dates[dates.index(date)-1]
        tok=unicodedata.normalize('NFKD',e['company'].upper()).encode('ascii','ignore').decode().split()[0].strip(',.')
        pref=aliases.get(tok,tok)
        matches=[n for n in set(bydate[prev]+bydate[date]) if norm(n).startswith(norm(pref))]
        if len(matches)>1:
            # Names unchanged except capitalization are already uppercased; remaining ambiguity is retained.
            raise ValueError(('ambiguous issuer screen',e['company'],matches))
        n=matches[0] if matches else ''
        before=n in bydate[prev];after=n in bydate[date]
        kind='addition' if after and not before else 'deletion' if before and not after else 'unchanged_or_absent'
        same_class=not(e['ticker']=='SSAB A' and 'ORD B' in n)
        opposed=same_class and kind in ('addition','deletion') and kind!=e['type']
        row=dict(event_id=e['event_id'],effective_date=date,ticker=e['ticker'],omxsb_type=e['type'],solactive_name=n,previous_snapshot=prev,member_previous=before,member_current=after,solactive_change_candidate=kind,same_share_class_screen=same_class,opposed_candidate=opposed)
        screen.append(row)
        if opposed:candidates.append(row)
    assert {(x['ticker'],x['effective_date']) for x in candidates}=={('ANOD B','2023-12-01'),('VBG B','2024-12-02')}, candidates
    write_csv(O/'omxsb_solactive_event_screen.csv',screen)
    # Separate OMXS30 exercise: all dated input rows, exact ticker or nonempty ISIN;
    # ±5 days is the anchor rule, ±190 is a diagnostic only, never a migration definition.
    om=list(csv.DictReader(open(R/'data/input/omxsb/omxs30_changes_2005_2026.csv')));pairs=[]
    for e in sb:
      for j in om:
        if not j['effective_date']:continue
        same=norm(e['ticker'])==norm(j['ticker']) or bool(e['isin'] and e['isin']==j['isin'])
        if not same:continue
        gap=(dt.date.fromisoformat(j['effective_date'])-dt.date.fromisoformat(e['effective_date'])).days
        if abs(gap)>190:continue
        pairs.append(dict(event_id=e['event_id'],ticker=e['ticker'],omxsb_date=e['effective_date'],omxs30_date=j['effective_date'],gap_calendar_days=gap,omxsb_type=e['type'],omxs30_type=j['type'],opposed=e['type']!=j['type'],anchor_timing=abs(gap)<=5,other_verification=j['verification'],source_url=j['source_url']))
    write_csv(O/'omxs30_matching_diagnostics.csv',pairs)
    # Parse original FI report envelopes, latest report per fund-quarter; retain individual position rows.
    inv=list(csv.DictReader(open(R/'output/omxsb_audit_20261031/fi_raw_report_inventory.csv')))
    fund=[x for x in inv if x['fund']=='60817']; latest={}
    for x in fund:
        if x['quarter'] not in latest or x['published_file']>latest[x['quarter']]['published_file']:latest[x['quarter']]=x
    finrows=[];metadata=[];totals=defaultdict(float);isin_by_ticker={'ANOD B':'SE0017885767','VBG B':'SE0000115107'}
    for quarter,x in sorted(latest.items()):
        with zipfile.ZipFile(R/'data/raw/fi'/x['zip']) as z:raw=z.read(x['file'])
        t=ET.fromstring(raw)
        for n in t.iter():n.tag=n.tag.split('}')[-1]
        def tx(tag):
            n=next(t.iter(tag),None);return n.text.strip() if n is not None and n.text else ''
        ninst=sum(1 for _ in t.iter('FinansielltInstrument'))
        metadata.append(dict(quarter=quarter,fund='60817',fund_name=tx('Fond_namn'),benchmark=' | '.join(n.text.strip() for n in t.iter('Jämförelseindex') if n.text and n.text.strip()),aum_sek=tx('Fondförmögenhet'),n_positions=ninst,zip=x['zip'],xml=x['file'],xml_sha256=hashlib.sha256(raw).hexdigest()))
        for n in t.iter('FinansielltInstrument'):
            d={k.tag:(k.text or '').strip() for k in n}
            if d.get('ISIN-kod_instrument') in isin_by_ticker.values():
                isin=d['ISIN-kod_instrument'];qty=float(d['Antal']);totals[(quarter,isin)]+=qty
                finrows.append(dict(quarter=quarter,isin=isin,name=d['Instrumentnamn'],shares=qty,mv_sek=d.get('Marknadsvärde_instrument'),asset_type=d.get('Tillgångsslag_enligt_LVF_5_kap'),zip=x['zip'],xml=x['file']))
        if quarter in ('2023-09-30','2023-12-31','2024-09-30','2024-12-31'):
            (O/'source_xml').mkdir(exist_ok=True);(O/'source_xml'/f'XACT_60817_{quarter}.xml').write_bytes(raw)
    write_csv(O/'xact_fund_quarter_metadata.csv',metadata);write_csv(O/'xact_candidate_raw_positions.csv',finrows)
    tracker_ids={x['Fond_institutnummer'] for x in csv.DictReader(open(R/'output/omxsb_audit_20261031/tracker_quarter_metadata.csv'))}
    assert len(tracker_ids)==14 and '60817' not in tracker_ids
    indexed_inventory={}
    for x in inv:
        key=(x['fund'],x['quarter'])
        if key not in indexed_inventory or x['published_file']>indexed_inventory[key]['published_file']:indexed_inventory[key]=x
    tracker_raw=[];output=[]
    for e in candidates:
        c=cars[e['event_id']];isin=isin_by_ticker[e['ticker']]
        assert c['IssueISIN']==isin
        qb,qa=c['qb'],c['qa'];assert qb in latest and qa in latest
        b,a=totals[qb,isin],totals[qa,isin];delta=a-b
        old=float(c['idx_b']);new=float(c['idx_a']);decline=old-new
        rawqty={qb:0.,qa:0.};nordea={qb:0.,qa:0.};nordea_bench={}
        for fid in sorted(tracker_ids):
            if not all((fid,q) in indexed_inventory for q in (qb,qa)):continue
            for q in (qb,qa):
                source=indexed_inventory[fid,q]
                with zipfile.ZipFile(R/'data/raw/fi'/source['zip']) as z:raw=z.read(source['file'])
                t=ET.fromstring(raw)
                for n in t.iter():n.tag=n.tag.split('}')[-1]
                qty=0.
                for n in t.iter('FinansielltInstrument'):
                    d={k.tag:(k.text or '').strip() for k in n}
                    if d.get('ISIN-kod_instrument')==isin:qty+=float(d['Antal'])
                bench=' | '.join(n.text.strip() for n in t.iter('Jämförelseindex') if n.text and n.text.strip())
                rawqty[q]+=qty
                tracker_raw.append(dict(event_id=e['event_id'],fund=fid,quarter=q,isin=isin,shares=qty,benchmark=bench,zip=source['zip'],xml=source['file'],xml_sha256=hashlib.sha256(raw).hexdigest()))
                if fid=='60293':nordea[q]=qty;nordea_bench[q]=bench
        assert abs(rawqty[qb]-old)<.01 and abs(rawqty[qa]-new)<.01, ('raw tracker mismatch',e,rawqty,old,new)
        nordea_decline=nordea[qb]-nordea[qa]
        output.append(dict(**e,isin=isin,quarter_before=qb,quarter_after=qa,xact_shares_before=b,xact_shares_after=a,xact_change_shares=delta,xact_offset_of_repository_tracker_decline_pct=100*delta/decline,repository_tracker_shares_before=old,repository_tracker_shares_after=new,raw_xml_tracker_reconciles=True,tracker_group_warning='14-fund ex-post trading classifier; not all true OMXSB mandates',nordea_60293_before_shares=nordea[qb],nordea_60293_after_shares=nordea[qa],nordea_60293_benchmark_before=nordea_bench[qb],nordea_60293_benchmark_after=nordea_bench[qa],xact_offset_of_nordea_60293_decline_pct=100*delta/nordea_decline if nordea_decline>0 else None,xact_aum_before_sek=next(m['aum_sek'] for m in metadata if m['quarter']==qb),xact_aum_after_sek=next(m['aum_sek'] for m in metadata if m['quarter']==qa),ann_car_pct=c['ann'],eff_car_pct=c['eff'],total_car_pct=c['tot'],return_status='existing frozen audit output; no new regression; timing convention not re-estimated',strict_migration_verified=False,identification_status='same-security opposing adjacent ordinary-list changes; exact pre-ED membership/offcycle audit incomplete'))
    write_csv(O/'migration_candidate_measurement.csv',output)
    write_csv(O/'tracker_candidate_raw_xml_aggregates.csv',tracker_raw)
    summary=dict(solactive_snapshot_counts={k:len(v) for k,v in bydate.items()},solactive_review_intervals=len(dates)-1,solactive_snapshot_differences=len(changes),omxsb_events_screened=len(screen),opposing_candidate_events=len(candidates),fully_verified_daily_membership_migrations=0,omxs30_input_rows=len(om),omxs30_dated_rows=sum(bool(x['effective_date']) for x in om),omxs30_near_pairs=len(pairs),omxs30_opposing_within5=sum(x['opposed'] and x['anchor_timing'] for x in pairs),xact_quarters=len(metadata),xact_candidate_raw_positions=len(finrows),inference='descriptive ownership accounting only; two candidates do not identify price attenuation')
    (O/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    hashes=[]
    for p in sorted(S.glob('*.txt'))+[R/'data/input/omxsb/omxsb_changes_2007_2026.csv',R/'data/input/omxsb/omxs30_changes_2005_2026.csv',R/'output/omxsb_audit_20261031/corrected/events_car.csv',R/'output/omxsb_audit_20261031/fi_raw_report_inventory.csv']:
        hashes.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    write_csv(O/'input_hashes.csv',hashes)
    print(json.dumps(summary,indent=2));print(json.dumps(output,indent=2))

if __name__=='__main__':main()
