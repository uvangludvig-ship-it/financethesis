"""Independent sampled/full source comparison. No price or volume outcomes.

Only fixed five instrument-days; extra range days listed and never compared.
Numeric quote/transaction cells used solely for equality, never exported.
"""
import argparse
from collections import Counter,defaultdict
import csv
from datetime import datetime,timezone
from decimal import Decimal,InvalidOperation
import gzip,hashlib,io,json
from pathlib import Path
import zipfile

FIXED=[('SE0009921588','2019-05-31','1793732319625'),
 ('SE0007692850','2023-11-23','1793733524718'),('SE0007692850','2023-11-30','1793733549086'),
 ('SE0005999836','2023-11-23','1793733618890'),('SE0005999836','2023-11-30','1793733672616')]
TOP=['bidpx1','askpx1','bidsz1','asksz1']
DEPTH=TOP+['bidpx2','askpx2','bidsz2','asksz2']
MISSING={'','n/a','na','null','none','nan'}
TOL=Decimal('1e-10')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    blob=path.read_bytes()
    if blob[:2]==b'\x1f\x8b':members=[gzip.decompress(blob)]
    elif blob[:2]==b'PK':
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            assert z.testzip() is None
            members=[z.read(n) for n in z.namelist() if n.lower().endswith('.csv')]
    else:members=[blob]
    rows=[];schema=None
    for member in members:
        reader=csv.DictReader(io.StringIO(member.decode('utf-8-sig')),delimiter=';')
        if schema is None:schema=reader.fieldnames
        assert schema==reader.fieldnames
        for r in reader:
            assert None not in r
            rows.append(r)
    return schema,rows


def number(value):
    if value.strip().lower() in MISSING:return None
    result=Decimal(value)
    return result if result.is_finite() else None


def eq(a,b,fields):
    for field in fields:
        x,y=number(a[field]),number(b[field])
        if x is None or y is None:
            if not(x is None and y is None):return False
        elif abs(x-y)>TOL:return False
    return True


def nanos(text):
    h,m,s=text.split(':')
    return int((Decimal(h)*3600+Decimal(m)*60+Decimal(s))*10**9)


def valid(r):
    values=[number(r[f]) for f in TOP]
    return r['status']=='T' and all(v is not None and v>0 for v in values) and values[0]<=values[1]


def compare(full,sampled):
    minute=60*10**9;cut=(17*3600+25*60)*10**9
    full_times=[nanos(r['time']) for r in full]
    sample_times=[nanos(r['time']) for r in sampled]
    full_reversals=sum(b<a for a,b in zip(full_times,full_times[1:]))
    sample_reversals=sum(b<a for a,b in zip(sample_times,sample_times[1:]))
    assert full_reversals==0 and sample_reversals==0,'Chronology must be established before last-row comparison'
    fbin=defaultdict(list);sbin=defaultdict(list)
    for row in full:fbin[nanos(row['time'])//minute].append(row)
    for row in sampled:sbin[nanos(row['time'])//minute].append(row)
    assert all(len(v)==1 for v in sbin.values())
    time_groups=defaultdict(list)
    for row in full:time_groups[nanos(row['time'])].append(row)
    signature=lambda row:tuple(number(row[field]) for field in TOP)
    conflicting_times=[key for key,rows in time_groups.items() if len({signature(r) for r in rows})>1]
    terminal_bin_ambiguities=[]
    for key,rows in fbin.items():
        maximum=max(nanos(r['time']) for r in rows)
        tied=[r for r in rows if nanos(r['time'])==maximum]
        if len({signature(r) for r in tied})>1:
            terminal_bin_ambiguities.append(dict(minute_label=f'{key//60:02d}:{key%60:02d}:00',
                full_last_timestamp=tied[0]['time'],tied_rows=len(tied),distinct_top4_states=len({signature(r) for r in tied})))
    fullT={key:[r for r in rows if r['status']=='T'] for key,rows in fbin.items() if any(r['status']=='T' for r in rows)}
    sampledT={key:rows[0] for key,rows in sbin.items() if rows[0]['status']=='T'}
    nonT=[]
    for key in sorted(set(fullT)-set(sampledT)):
        if key in sbin:
            nonT.append(dict(sampled_time=sbin[key][0]['time'],sampled_status=sbin[key][0]['status'],
                full_final_status=fbin[key][-1]['status'],full_final_top4_equal=eq(sbin[key][0],fbin[key][-1],TOP)))
    common=sorted(set(fbin)&set(sbin))
    matches={fields:0 for fields in ['top4','depth8','txpx','txsz','status','identity']}
    for key in common:
        last=fbin[key][-1];actual=sbin[key][0]
        matches['top4']+=eq(actual,last,TOP)
        matches['depth8']+=eq(actual,last,DEPTH)
        matches['txpx']+=eq(actual,last,['txpx'])
        matches['txsz']+=eq(actual,last,['txsz'])
        matches['status']+=actual['status']==last['status']
        matches['identity']+=all(actual[c]==last[c] for c in ['isin','date','symbol','market','currency','instrumentid'])
    # This tests the original terminal state, never computes a midpoint or premium.
    fvalid=[r for r in full if valid(r) and cut-minute<=nanos(r['time'])<cut]
    assert fvalid
    finaltime=max(nanos(r['time']) for r in fvalid)
    finalrows=[r for r in fvalid if nanos(r['time'])==finaltime]
    assert all(eq(finalrows[0],r,TOP) for r in finalrows)
    skey=(cut-1)//minute
    endpoint=sbin.get(skey,[])
    terminal_ok=len(endpoint)==1 and valid(endpoint[0]) and eq(endpoint[0],finalrows[0],TOP)
    return dict(full_rows=len(full),sampled_rows=len(sampled),
        identity={c:sorted({r[c] for r in sampled}) for c in ['isin','date','symbol','market','currency','instrumentid']},
        sample_first_time=min(r['time'] for r in sampled),sample_last_time=max(r['time'] for r in sampled),
        ordering_check=dict(full_nonmonotonic_transitions=full_reversals,sample_nonmonotonic_transitions=sample_reversals,
            full_exact_duplicate_extra_rows=len(full)-len({tuple(r.items()) for r in full}),
            full_duplicate_timestamp_extra_rows=len(full)-len(time_groups),
            full_conflicting_top4_same_timestamp_groups=len(conflicting_times),
            sampled_duplicate_timestamp_extra_rows=len(sampled)-len(set(sample_times)),
            full_minute_final_timestamp_conflicting_top4_groups=len(terminal_bin_ambiguities),
            full_minute_final_timestamp_conflicts=terminal_bin_ambiguities,
            every_full_minute_has_unique_chronologically_last_top4_state=not terminal_bin_ambiguities,
            final_preauction_valid_timestamp_rows=len(finalrows),
            final_preauction_top4_state_unique=True),
        sampled_status_counts=dict(Counter(r['status'] for r in sampled)),
        full_nonempty_minute_bins=len(fbin),sampled_minute_bins=len(sbin),
        exact_one_sample_for_every_nonempty_full_minute=set(fbin)==set(sbin),
        full_nonempty_bins_missing_sample=len(set(fbin)-set(sbin)),
        sampled_bins_without_any_full_update=len(set(sbin)-set(fbin)),
        sampled_empty_full_bins=[sbin[k][0]['time'] for k in sorted(set(sbin)-set(fbin))],
        all_sample_times_are_minute_start_labels=all(nanos(r['time'])%minute==0 for r in sampled),
        original_update_timestamps_preserved=sum(any(r['time']==s['time'] for r in fbin[k]) for k,ss in sbin.items() for s in ss if k in fbin),
        sample_matches_final_full_row_in_same_minute=dict(compared_bins=len(common),equal_counts=matches),
        full_minutes_containing_T_updates=len(fullT),sampled_T_minutes=len(sampledT),
        full_T_minutes_missing_sampled_T=len(set(fullT)-set(sampledT)),
        full_T_minutes_missing_any_sample=len(set(fullT)-set(sbin)),
        sampled_T_minutes_without_full_T_update=len(set(sampledT)-set(fullT)),
        full_T_minutes_ending_nonT_and_sampled_nonT=nonT,
        terminal_four_field_state_reproduced=terminal_ok,
        full_final_valid_update_time=finalrows[0]['time'],
        full_final_valid_update_age_seconds=str(Decimal(cut-finaltime)/Decimal(10**9)),
        final_label=endpoint[0]['time'] if endpoint else None,
        terminal_bin_contains_observed_actual_update=bool(fbin.get(skey)),
        pilot_freshness_proven_from_fullbook=bool(terminal_ok and 0<cut-finaltime<=minute),
        sample_label_alone_is_original_update_time=False,
        original_final_update_is_unique_four_field_state=True,
        full_rows_17_25_plus=sum(nanos(r['time'])>=cut for r in full),
        sampled_rows_17_25_plus=sum(nanos(r['time'])>=cut for r in sampled),
        sampled_closing_L_rows=sum(r['status']=='L' for r in sampled),
        sampled_closing_cross_third_C_rows=sum(len(r['status'])==3 and r['status'][2]=='C' for r in sampled),
        source_only=True,no_quote_levels_or_economic_outcomes_exported=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=Path('/Users/ludviguvang/dev/financethesis'))
    parser.add_argument('--input',type=Path,nargs='+',required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    allrows=[];schema=[]
    for p in args.input:
        columns,rows=load(p);allrows.extend(rows);schema.append(dict(file=str(p),columns=columns,rows=len(rows),sha256=sha(p)))
    checks=[];full_hashes={}
    for isin,date,identifier in FIXED:
        sampled=[r for r in allrows if r['isin']==isin and r['date']==date]
        if not sampled:
            checks.append(dict(ISIN=isin,date=date,status='not_yet_delivered_fixed_day'));continue
        path=args.repo_root/'data/raw/shof/Reinvestments/hft_pilot_20261103'/f'NASDAQ_2nd_level_orderbook_{identifier}.csv.zip'
        _,full=load(path);full_hashes[str(path)]=sha(path)
        assert {r['isin'] for r in full}=={isin} and {r['date'] for r in full}=={date}
        assert {r['market'] for r in sampled}=={'XSTO'} and {r['currency'] for r in sampled}=={'SEK'}
        checks.append(dict(ISIN=isin,date=date,status='source_compared',**compare(full,sampled)))
    selected={(i,d) for i,d,_ in FIXED}
    ignored=sorted({(r['isin'],r['date']) for r in allrows}-selected)
    out=dict(created_utc=datetime.now(timezone.utc).isoformat(),source_only=True,script_sha256=sha(Path(__file__)),
        sampled_inputs=schema,full_source_hashes=full_hashes,fixed_checks=checks,ignored_extra_days=ignored,
        tolerance='absolute1e-10 fixed in predeclared source spec; Decimal comparison',
        no_new_returns_or_auction_premiums=True,
        all_five_terminal_states_reproduced=all(c.get('terminal_four_field_state_reproduced',False) for c in checks),
        all_five_no_empty_bin_generation=all(c.get('sampled_bins_without_any_full_update',1)==0 for c in checks),
        scope_limit='Matched fixed-day source evidence, not universal software documentation or broad historical outcome authorization')
    args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['all_five_terminal_states_reproduced','all_five_no_empty_bin_generation','ignored_extra_days']},indent=2))


if __name__=='__main__':main()
