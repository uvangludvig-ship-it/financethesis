"""Independent stdlib reconstruction; never imports producer functions.

Use original q1 cohort/weights, prior F35 raw quantities and independently
rebuilt fund/report masks. Public output contains aggregates and hashes only.
"""
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone, date
import argparse, csv, gzip, hashlib, json, math

P=Path(__file__).resolve().parent
CHAT=P.parents[2]
REPO=Path('/Users/ludviguvang/dev/financethesis')
G=CHAT/'work/omxsb_scaled_round_20261103/independent_design/retention'
PROD=CHAT/'work/omxsb_shof_continue_20261104/next_test'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    op=gzip.open if p.suffix=='.gz' else open
    with op(p,'rt',newline='') as f: return list(csv.DictReader(f))
def boolean(x):
    assert str(x).lower() in ('true','false'),str(x)
    return str(x).lower()=='true'
def number(x):
    try: return float(x)
    except (ValueError,TypeError): return math.nan
def group(rows,key):
    out=defaultdict(list)
    for r in rows: out[key(r)].append(r)
    return out
def singleton(rows,key):
    out={key(r):r for r in rows}
    assert len(out)==len(rows),'duplicate source key'
    return out
def capped_units(q1,q2,factor):
    assert math.isfinite(q1) and q1>0 and math.isfinite(q2) and q2>=0
    assert math.isfinite(factor) and factor>0
    return min(q1,q2/factor)
def mean(xs): return math.fsum(xs)/len(xs)
def table(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def write(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def tests():
    assert (capped_units(100,0,1)+capped_units(100,200,1))/200==.5
    assert capped_units(100,200,2)==100
    assert capped_units(25,10,1)+capped_units(75,30,1)==40
    assert mean([mean([0,1]),mean([1])])==.75
    try: capped_units(1,-1,1)
    except AssertionError: pass
    else: raise AssertionError('negative quantity accepted')
    return 5

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();O=a.output
    assert not O.exists(),'Use a new directory; preserve first run.'
    assert (PROD/'outcomes/PRIMARY_RESULT.json').exists(),'Await frozen producer result.'
    assert tests()==5
    paths={
      'cohort':REPO/'output/omxsb_contribution_round_20261103/ownership_capital/normalized_fund_role_contributions.csv.gz',
      'roles':G/'FROZEN_ROLES.csv','event_gate':G/'EVENT_SOURCE_GATE.csv',
      'eligible':G/'ELIGIBLE_FUNDS.csv','fund_support':G/'FUND_REPORT_SUPPORT.csv.gz',
      'invalid_units':G/'INVALID_FUND_UNITS.csv','security_gate':G/'SECURITY_SOURCE_GATE.csv',
      'raw':G/'private/RAW_RELEVANT_POSITIONS.csv.gz','scaling':G/'private/SCALING_INPUTS.csv',
      'report_metadata':REPO/'output/omxsb_open_questions_20261102/demand_quarter/raw_fund_report_metadata.csv',
      'actions':REPO/'output/omxsb_extension_20261031/ownership/corporate_action_sources.csv',
      'source_precision':PROD/'EVENT_ONLY_SOURCE_PRECISION.json',
      'producer_design':PROD/'DESIGN_LOCK.json','producer_execution':PROD/'outcomes/EXECUTION_LOCK.json',
      'independent_code':Path(__file__), 'audit_spec':P/'AUDIT_SPEC.txt'}
    O.mkdir(parents=True)
    lock={'started_utc':datetime.now(timezone.utc).isoformat(),'producer_functions_imported':False,
          'formula_chosen_before_input_read':True,'synthetic_checks':5,
          'inputs':{k:{'path':str(v),'sha256':sha(v)} for k,v in paths.items()}}
    write(O/'INPUT_LOCK.json',lock)
    dlock=json.loads(paths['producer_design'].read_text())
    for own,other in [('cohort','q1_ledger'),('raw','raw_positions'),('scaling','scaling_inputs'),('roles','FROZEN_ROLES.csv'),('event_gate','EVENT_SOURCE_GATE.csv'),('eligible','ELIGIBLE_FUNDS.csv'),('security_gate','SECURITY_SOURCE_GATE.csv')]:
        assert paths[own].resolve()==Path(dlock['inputs'][other]['path']).resolve()
        assert sha(paths[own])==dlock['inputs'][other]['sha256']

    D=[r for r in read(paths['cohort']) if r['type']=='addition' and r['review']<'2024']
    singleton(D,lambda r:(r['event_id'],r['role'],r['fund_id']))
    byevent=group(D,lambda r:r['event_id'])
    assert len(byevent)==70 and len({r['review'] for r in D})==10
    for eid,rs in byevent.items():
        byrole=group(rs,lambda r:r['role']);assert set(byrole)=={'event','c1','c2','c3'}
        assert all({r['fund_id'] for r in v}=={r['fund_id'] for r in byrole['event']} for v in byrole.values())
    N=[r for r in D if r['role']=='event' and r['component']=='new']
    assert len(N)==737 and all(math.isfinite(number(r['pp'])) and number(r['pp'])>0 for r in N)
    Nby=group(N,lambda r:r['event_id'])
    S=read(paths['roles']);Sby=group(S,lambda r:r['event_id'])
    assert len(S)==280 and set(Sby)==set(byevent)
    E=singleton(read(paths['event_gate']),lambda r:r['event_id'])
    SG=singleton(read(paths['security_gate']),lambda r:(r['review'],r['ric']))
    scale=singleton(read(paths['scaling']),lambda r:(r['review'],r['ric']))
    F=read(paths['eligible']);singleton(F,lambda r:(r['event_id'],r['fund_id']))
    eligible=group(F,lambda r:r['event_id'])
    support=group(read(paths['fund_support']),lambda r:r['event_id'])
    invalid=read(paths['invalid_units'])
    meta=singleton(read(paths['report_metadata']),lambda r:(r['Fond_institutnummer'],r['Kvartalsslut']))
    ca=read(paths['actions'])
    verified_funds={};good=set();report_checks=0
    for eid,rs in Sby.items():
        assert len(rs)==4 and {r['role'] for r in rs}=={'event','c1','c2','c3'}
        x=rs[0];dates=[x[k] for k in ('q0','q1','q2')]
        assert all([r[k] for k in ('q0','q1','q2')]==dates for r in rs)
        assert len(set(dates))==3 and dates==sorted(dates)
        bad={r['fund_id'] for r in invalid if r['review']==x['review'] and r['ric'] in {s['ric'] for s in rs}}
        base={r['fund_id'] for r in byevent[eid] if r['role']=='event'}
        expected=set()
        for fid in base:
            reports=[meta.get((fid,q)) for q in dates]
            ok=all(r is not None and number(r['actual_instrument_rows'])>0 and r['fund_isin'].strip().lower() not in ('','nan','none') for r in reports)
            if ok: ok=len({r['fund_isin'] for r in reports})==1
            if ok and fid not in bad: expected.add(fid)
        actual={r['fund_id'] for r in eligible.get(eid,[])}
        assert expected==actual,'eligible fund mismatch'
        assert {r['fund_id'] for r in support[eid] if boolean(r['eligible'])}==actual
        verified_funds[eid]=actual;report_checks+=len(actual)*3
        pass_set=all(boolean(SG[(r['review'],r['ric'])]['gate_pass']) for r in rs) and bool(actual)
        assert pass_set==boolean(E[eid]['gate_pass'])
        if pass_set:
            good.add(eid)
            for r in rs:
                g=SG[(r['review'],r['ric'])]
                assert boolean(g['q0_same_actual_LSEG_date']) and g['q0_LSEG_close_date']==g['q0_LSEG_mcap_date']
    assert len(good)==59

    # Keep source rows private in memory only. No copied fund/quantity ledger.
    raw=group(read(paths['raw']),lambda r:(r['isin'],r['fund_id'],r['quarter']))
    def quantity(aliases,fid,quarter):
        rr=[r for isin in aliases for r in raw.get((isin,fid,quarter),[])]
        vv=[number(r['qty']) for r in rr]
        duplicate=len({tuple(sorted(r.items())) for r in rr})<len(rr)
        valid=all(math.isfinite(v) and v>=0 for v in vv)
        return (math.fsum(vv) if valid else math.nan),len(rr),duplicate

    out=[];source_supported=actual_supported=verified_absences=observed_zero=unexpected=0
    cohort_checks=0;split_nonunit=0
    for eid,entries in sorted(Nby.items()):
        x=next(s for s in Sby[eid] if s['role']=='event')
        aliases=x['aliases'].split(';');assert all(aliases)
        factor=number(scale[(x['review'],x['ric'])]['factor12'])
        factor_from_dates=math.prod(number(z['factor']) for z in ca if z['RIC']==x['ric'] and z['kind']=='ordinary_split' and x['q1']<z['action_date'][:10]<=x['q2'])
        if eid in good:
            assert math.isfinite(factor) and factor>0
            assert abs(factor-number(SG[(x['review'],x['ric'])]['factor12']))<1e-12
            assert abs(factor-factor_from_dates)<1e-12
            split_nonunit+=int(abs(factor-1)>1e-12)
        denom=[];overlap=[];unknown=[];source_unknown=[];ratios=[];ns=na=nv=nz=nu=0
        for r in entries:
            fid=r['fund_id'];q0,_,du0=quantity(aliases,fid,x['q0']);q1,_,du1=quantity(aliases,fid,x['q1'])
            assert not du0 and not du1,'original duplicate rows require adjudication'
            assert math.isfinite(q0) and q0==0 and math.isfinite(q1) and q1>0,'original cohort inconsistency'
            cohort_checks+=1;denom.append(q1);ratios.append(number(r['pp'])/q1)
            originally_known=eid in good and fid in verified_funds[eid]
            if not originally_known:
                unknown.append(q1);source_unknown.append(q1);continue
            ns+=1
            q2,n,dup=quantity(aliases,fid,x['q2'])
            if dup or not math.isfinite(q2) or q2<0:
                unknown.append(q1);nu+=1;continue
            # Report existence/stable fund ISIN was independently established above.
            na+=1;nv+=int(n==0);nz+=int(n>0 and q2==0)
            overlap.append(capped_units(q1,q2,factor))
        assert max(abs(v/ratios[0]-1) for v in ratios)<1e-9,'q1 ledger not proportional to original quantity'
        total=math.fsum(denom);lo=math.fsum(overlap)/total;wid=math.fsum(unknown)/total;hi=lo+wid
        basewidth=math.fsum(source_unknown)/total
        assert 0<=lo<=hi<=1+1e-12
        source_supported+=ns;actual_supported+=na;verified_absences+=nv;observed_zero+=nz;unexpected+=nu
        out.append({'event_id':eid,'review':x['review'],'q0':x['q0'],'q1':x['q1'],'q2':x['q2'],
                    'original_new_positions':len(entries),'source_supported_positions':ns,'supported_positions':na,
                    'verified_report_absences':nv,'observed_zero_quantity_positions':nz,'unexpected_q2_failures':nu,
                    'lower_fraction':lo,'upper_fraction':hi,'width_fraction':wid,'source_only_width_fraction':basewidth})
    reviews=[]
    for rv,ee in sorted(group(out,lambda r:r['review']).items()):
        reviews.append({'review':rv,'events':len(ee),'lower_fraction':mean([r['lower_fraction'] for r in ee]),
                        'upper_fraction':mean([r['upper_fraction'] for r in ee]),'width_fraction':mean([r['width_fraction'] for r in ee]),
                        'source_only_width_fraction':mean([r['source_only_width_fraction'] for r in ee])})
    assert len(out)==70 and len(reviews)==10 and cohort_checks==737 and source_supported==617
    full=sum(r['source_supported_positions']==r['original_new_positions'] for r in out)
    whole=sum(r['source_supported_positions']==0 for r in out)
    assert (full,70-full-whole,whole)==(57,2,11)
    prewidth=json.loads(paths['source_precision'].read_text())['event_only_equal_review_bound_width_pp']
    assert abs(100*mean([r['source_only_width_fraction'] for r in reviews])-prewidth)<1e-10
    result={'completed_utc':datetime.now(timezone.utc).isoformat(),'events':70,'reviews':10,'original_positions':737,
            'source_supported_positions':source_supported,'supported_positions':actual_supported,'fully_source_supported_events':full,
            'partly_source_supported_events':70-full-whole,'wholly_source_unsupported_events':whole,
            'lower_percent':100*mean([r['lower_fraction'] for r in reviews]),'upper_percent':100*mean([r['upper_fraction'] for r in reviews]),
            'width_percentage_points':100*mean([r['width_fraction'] for r in reviews]),
            'source_only_width_percentage_points':prewidth,'unexpected_q2_source_failures':unexpected,
            'verified_complete_report_absences':verified_absences,'explicit_reported_zero_quantity_positions':observed_zero,
            'independently_rebuilt_report_cells':report_checks,'source_pass_events':len(good),'nonunit_split_event_factors':split_nonunit,
            'original_cohort_checks':cohort_checks,'fund_sets_independently_reproduced':True,'q1_quantity_weight_equivalence_checked_all_positions':True,
            'capped_per_fund':True,'producer_functions_imported':False,'producer_private_audit_used':False,
            'raw_fund_values_exported':False,'peer_statistics_computed':False,'sampling_CI_or_pvalue_computed':False,
            'measure':'Descriptive endpoint overlap; conservative missing-source bounds, not continuous holding or causal effect'}
    table(O/'INDEPENDENT_EVENT_BOUNDS.csv',out);table(O/'INDEPENDENT_REVIEW_BOUNDS.csv',reviews)
    write(O/'INDEPENDENT_RESULT.json',result)

    # Only now open the producer aggregates for comparison.
    pe=singleton(read(PROD/'outcomes/EVENT_BOUNDS.csv'),lambda r:r['event_id'])
    pr=singleton(read(PROD/'outcomes/REVIEW_BOUNDS.csv'),lambda r:r['review'])
    pj=json.loads((PROD/'outcomes/PRIMARY_RESULT.json').read_text())
    em=max(abs(r[k]-number(pe[r['event_id']][k])) for r in out for k in ('lower_fraction','upper_fraction','width_fraction'))
    rm=max(abs(r[k]-number(pr[r['review']][k])) for r in reviews for k in ('lower_fraction','upper_fraction','width_fraction'))
    am=max(abs(result[k]-pj[k]) for k in ('lower_percent','upper_percent','width_percentage_points'))
    assert em<1e-10 and rm<1e-10 and am<1e-10
    assert actual_supported==pj['supported_positions'] and unexpected==pj['unexpected_q2_source_failures']
    comp={'status':'PASS','max_event_fraction_difference':em,'max_review_fraction_difference':rm,'max_aggregate_percentage_point_difference':am,
          'producer_aggregate_hashes':{n:sha(PROD/'outcomes'/n) for n in ['PRIMARY_RESULT.json','EVENT_BOUNDS.csv','REVIEW_BOUNDS.csv']},
          'all_input_hashes_unchanged':all(sha(Path(v['path']))==v['sha256'] for v in lock['inputs'].values())}
    assert comp['all_input_hashes_unchanged'];write(O/'COMPARISON.json',comp)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(comp,indent=2))

if __name__=='__main__':main()
