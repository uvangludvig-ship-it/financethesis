"""Two-review OMXSB candidate DATA pilot. No return, prediction or significance tests.

python omxsb_candidate_pilot.py --repo /absolute/financethesis --out /absolute/new/output \
    --source-dir /absolute/staging
Use --download to retrieve the explicitly listed public original sources.
Never modifies repository raw data, older audit outputs or manifests.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, re, shutil, urllib.request
from pathlib import Path
import pandas as pd

SPECS = [
 dict(month='2019-10', cycle='2019H2', suffix='xls', header=5, cap=18, shares=17,
      turnover=56, turnover_start='2018-11-01', ref='2019-10-31',
      published='2019-11-07 15:46:21+01:00', ad='2019-11-11 08:30:00+01:00',
      attachment='https://attachment.news.eu.nasdaq.com/abbfc1693d740f6912416ede1e22ad437',
      notice='https://view.news.eu.nasdaq.com/view?id=b70fd0ca29c6359152cf8fec406373bb3&lang=en'),
 dict(month='2024-10', cycle='2024H2', suffix='xlsx', header=6, cap=17, shares=16,
      turnover=47, turnover_start='2023-11-01', ref='2024-10-31',
      published='2024-11-04 09:23:45+01:00', ad='2024-11-22 18:00:00+01:00',
      attachment='https://attachment.news.eu.nasdaq.com/ac38287f46eb72fdb59bc9310e3251cb9',
      notice='https://view.news.eu.nasdaq.com/view?id=b831680b404482150ad4af5b0771d33ba&lang=en')]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(v): return re.sub(r'[^A-Z0-9]','',str(v).upper())
def fetch(url, path):
    with urllib.request.urlopen(url,timeout=30) as r:
        data=r.read()
    path.write_bytes(data)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--source-dir',type=Path)
    ap.add_argument('--download',action='store_true');args=ap.parse_args()
    repo=args.repo.resolve();out=args.out.resolve();sources=out/'sources';sources.mkdir(parents=True,exist_ok=True)
    audit=repo/'output/omxsb_audit_20261031'
    input_files=[audit/'candidate_pilot_targets.csv',audit/'corrected/mechanisms/omxsb_membership_by_review.csv',
                 audit/'corrected/mechanisms/membership_inconsistencies.csv',
                 repo/'data/raw/lseg/panel_2005_2026/stocks_static_2005.csv',
                 repo/'data/raw/lseg/panel_2012_2026/stocks_static.csv']
    before={str(p.relative_to(repo)):sha(p) for p in input_files}
    targets=pd.read_csv(input_files[0],keep_default_na=False)
    membership=pd.read_csv(input_files[1]);issues=pd.read_csv(input_files[2])
    static=pd.concat([pd.read_csv(p)[['ric','IssueISIN']] for p in input_files[3:]],ignore_index=True).dropna().drop_duplicates()
    static_map=static.groupby('IssueISIN')['ric'].agg(lambda x:';'.join(sorted(set(x)))).to_dict()
    all_candidates=[];event_rows=[];summary=[];manifest=[];field_rows=[]
    for spec in SPECS:
        ym=spec['month'].replace('-',''); fn=f'nasdaq_{ym}.{spec["suffix"]}'
        for filename,url in [(fn,spec['attachment']),(f'notice_{ym}.html',spec['notice'])]:
            dest=sources/filename
            if args.source_dir and (args.source_dir/filename).exists():
                if (args.source_dir/filename).resolve()!=dest.resolve():shutil.copy2(args.source_dir/filename,dest)
            elif not dest.exists() and args.download: fetch(url,dest)
            if not dest.exists():raise FileNotFoundError(f'Missing {dest}; use --source-dir or --download')
            manifest.append(dict(file=str(dest.relative_to(out)),url=url,bytes=dest.stat().st_size,sha256=sha(dest),
                                 public_access='Downloaded without authentication',license='No redistribution licence established'))
        f=pd.ExcelFile(sources/fn);x=pd.read_excel(f,sheet_name='Instrument Trading Details',header=None)
        headers=x.iloc[spec['header']]
        assert headers.iloc[0]=='Instrument' and headers.iloc[3]=='ISIN'
        assert norm(headers.iloc[spec['cap']])=='MARKETCAP'
        assert norm(headers.iloc[spec['turnover']])=='TOTALNTURNOVER' or norm(headers.iloc[spec['turnover']])=='TOTALTURNOVER'
        assert 'October '+spec['ref'][:4] in str(x.iloc[0,3])
        expected_period=('November 2018 - October 2019' if ym=='201910' else 'November 2023 - October 2024')
        assert any(expected_period in str(v) for v in x.iloc[:spec['header']].values.ravel())
        assert not any('float' in str(v).lower() for v in x.iloc[:spec['header']+1].values.ravel())
        notice=(sources/f'notice_{ym}.html').read_text()
        expected_pub=spec['published'][:19]
        assert expected_pub in notice, f'Publication time absent from original notice {ym}'
        assert spec['attachment'] in notice, 'Downloaded attachment must be linked by its original notice'
        cols={0:'name_as_reported',1:'company_code',2:'orderbook_code',3:'isin_as_reported',4:'instrument_type',5:'segment',
              6:'industry_as_reported',7:'supersector_as_reported',13:'currency',14:'location',15:'delisted_date',
              spec['shares']:'shares_listed',spec['cap']:'market_cap_local',spec['turnover']:'on_exchange_turnover_12m_local'}
        c=x.iloc[spec['header']+1:].rename(columns=cols)[list(cols.values())].copy()
        c['source_excel_row']=c.index+1;c=c[c.location.eq('STO') & c.isin_as_reported.notna()].copy()
        assert not c.isin_as_reported.duplicated().any()
        for col in ['shares_listed','market_cap_local','on_exchange_turnover_12m_local']:
            c[col]=pd.to_numeric(c[col],errors='coerce')
        c['delisted_date']=pd.to_datetime(c.delisted_date,errors='coerce')
        c['reference_date']=spec['ref'];c['review_cycle']=spec['cycle'];c['publication_timestamp']=spec['published']
        c['turnover_start']=spec['turnover_start'];c['turnover_end']=spec['ref']
        c['source_url']=spec['attachment'];c['source_sheet']='Instrument Trading Details'
        c['stock_type']=c.instrument_type.eq('Stock')
        c['listed_at_month_end']=c.delisted_date.isna() | (c.delisted_date>pd.Timestamp(spec['ref']))
        c['preference_name_flag']=c.name_as_reported.str.contains('pref',case=False,na=False)
        c['preliminary_ordinary_stock_screen']=c.stock_type & c.listed_at_month_end & ~c.preference_name_flag
        c['final_omxspi_eligibility_verified']=False
        c['eligibility_status']='Stock/end-month/pref-name screen only; dominance, security type and historical methodology unresolved'
        c['free_float_available']=False;c['official_omxsb_membership_verified']=False
        c['static_isin_ric_candidates']=c.isin_as_reported.map(static_map).fillna('')
        c['static_ric_count']=c.static_isin_ric_candidates.map(lambda z:len(z.split(';')) if z else 0)
        c['ric_historical_identity_verified']=False
        prior=membership[pd.to_datetime(membership.ED)<=pd.Timestamp(spec['ref'])].sort_values('ED').iloc[-1]
        members=set(prior.members_after.split(';'))
        c['membership_chain_asof']=prior.ED
        c['provisional_member_from_static_link']=c.static_isin_ric_candidates.map(lambda z:any(r in members for r in z.split(';')) if z else pd.NA)
        c['membership_status']='Existing reconstructed chain only; no official reference-date constituent file'
        c['data_available_at_reference_close']=False
        c['data_available_before_announcement']=pd.Timestamp(spec['published'])<pd.Timestamp(spec['ad'])
        c['earliest_verified_file_availability']=spec['published']
        c['_symbol']=c.orderbook_code.map(norm)
        ev=targets[targets.review_cycle.eq(spec['cycle'])]
        for _,e in ev.iterrows():
            matches=c[c._symbol.eq(norm(e.ticker))]
            row=e.to_dict();row.update(event_notice_url=e.source_url,reference_date=spec['ref'],publication_timestamp=spec['published'],
                announcement_timestamp=spec['ad'],source_url=spec['attachment'],matching_method='Exact normalized event ticker to dated Nasdaq orderbook code',
                matching_candidates=len(matches),free_float_available=False,official_membership_file_available=False,
                official_candidate_file_verified=True,historical_identifier_link_verified=False,
                status='Dated Nasdaq instrument file and exact ticker/name identity verified; full eligibility, float and historical RIC chain unresolved',
                ric_historical_identity_verified=False,
                file_public_before_announcement=bool(pd.Timestamp(spec['published'])<pd.Timestamp(spec['ad'])))
            if len(matches)==1:
                m=matches.iloc[0]
                assert norm(e.company)==norm(m.name_as_reported), f'Target name conflict: {e.event_id}'
                for k in ['name_as_reported','orderbook_code','isin_as_reported','source_excel_row','instrument_type','listed_at_month_end',
                          'industry_as_reported','supersector_as_reported','shares_listed','market_cap_local','on_exchange_turnover_12m_local',
                          'static_isin_ric_candidates','preliminary_ordinary_stock_screen']:
                    row[k]=m[k]
                row['nasdaq_reference_identity_verified']=True
                row['event_ric_in_static_isin_candidates']=e.RIC in m.static_isin_ric_candidates.split(';')
                row['provisional_chain_pre_member']=e.RIC in members
                row['expected_pre_member_from_event_type']=e.type=='deletion'
                row['provisional_chain_consistent_with_type']=(e.RIC in members)==(e.type=='deletion')
            else:row['nasdaq_reference_identity_verified']=False
            event_rows.append(row)
        filt=c.preliminary_ordinary_stock_screen
        summary.append(dict(review_cycle=spec['cycle'],stockholm_instruments=len(c),instrument_types=c.instrument_type.value_counts().to_dict(),
             listed_stock_count=int((c.stock_type&c.listed_at_month_end).sum()),preference_name_stock_count=int((c.stock_type&c.preference_name_flag).sum()),
             preliminary_ordinary_stock_count=int(filt.sum()),
             stock_screen_missing_market_cap=int(c.loc[filt,'market_cap_local'].isna().sum()),
             stock_screen_missing_turnover=int(c.loc[filt,'on_exchange_turnover_12m_local'].isna().sum()),
             stock_screen_missing_supersector=int(c.loc[filt,'supersector_as_reported'].isna().sum()),
             stock_screen_static_isin_any_match=int((filt & c.static_ric_count.gt(0)).sum()),
             stock_screen_static_isin_unique_match=int((filt & c.static_ric_count.eq(1)).sum()),
             targets=len(ev),nasdaq_target_ticker_matches=sum(r['nasdaq_reference_identity_verified'] for r in event_rows if r['review_cycle']==spec['cycle']),
             published_at=spec['published'],reference_date=spec['ref'],announcement_at=spec['ad'],
             publication_before_announcement=True,free_float_available=False,official_membership_available=False,
             earliest_forecast_information=spec['published'],period_coverage='Two pilot reviews only; no full-history coverage inference'))
        for field,status,detail in [
            ('historical_main_market_instruments','verified','Includes securities listed at month end or delisted during month'),
            ('instrument_types_and_ISIN','verified','Original dated Nasdaq row; not a full historical RIC link'),
            ('official_on_exchange_12m_turnover','verified',expected_period+'; local currency; OTC separate/omitted'),
            ('ICB_supersector','verified_as_reported','Contemporaneous source codes; taxonomy version differs; no cross-year harmonisation'),
            ('listed_shares_and_market_cap','verified_as_reported','Month-end listed shares times reference price; not free-float capital'),
            ('free_float','missing','No float column in instrument sheet; licensed/date-correct source required'),
            ('complete_OMXSPI_eligible_universe','not_verified','Main-market screen is not official OMXSPI membership or full eligibility'),
            ('official_OMXSB_members_at_reference','not_verified','Local reconstructed membership is explicitly provisional'),
            ('publication_timestamp','verified',spec['published']+'; after reference date, before announcement'),
            ('historical_rule_version','partial','March2018 v2.4 primary located; exact amendments through both pilot dates not fully established'),
            ('distribution_licence','not_verified','Public download is not blanket redistribution permission; ICB restrictions in primary methodology')]:
            field_rows.append(dict(review_cycle=spec['cycle'],field=field,status=status,detail=detail))
        all_candidates.append(c.drop(columns='_symbol'))
    candidates=pd.concat(all_candidates,ignore_index=True);events=pd.DataFrame(event_rows)
    assert len(events)==29 and events.event_id.nunique()==29
    assert events.nasdaq_reference_identity_verified.all()
    candidates.to_csv(out/'candidate_instrument_ledger.csv',index=False)
    events.to_csv(out/'event_target_coverage.csv',index=False)
    pd.DataFrame(field_rows).to_csv(out/'field_availability.csv',index=False)
    candidates[~candidates.preliminary_ordinary_stock_screen].to_csv(out/'excluded_instruments_screen_only.csv',index=False)
    candidates[candidates.preliminary_ordinary_stock_screen & candidates.static_ric_count.ne(1)].to_csv(out/'static_identity_gaps.csv',index=False)
    events[~events.event_ric_in_static_isin_candidates].to_csv(out/'event_static_identifier_conflicts.csv',index=False)
    examples=[]
    for _,e in events[~events.event_ric_in_static_isin_candidates].iterrows():
        examples.append(dict(event_id=e.event_id,ric=e.RIC,nasdaq_reference_isin=e.isin_as_reported,
                             static_isins=';'.join(sorted(set(static.loc[static.ric.eq(e.RIC),'IssueISIN']))),
                             status='Different dated/source identities; do not infer a missing price series or substitute today\'s ISIN'))
    pd.DataFrame(examples).to_csv(out/'event_historical_vs_static_isin.csv',index=False)
    issues.to_csv(out/'existing_membership_chain_issues_unresolved.csv',index=False)
    after={str(p.relative_to(repo)):sha(p) for p in input_files};assert before==after
    result=dict(run_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),repo=str(repo),source_retrieval_date='2026-10-31',
        pandas_version=pd.__version__,reviews=summary,
        target_total=29,target_dated_nasdaq_identity_matches=29,
        source_input_hashes=before,original_inputs_unchanged=True,
        hard_limits=['No returns computed','No forecasts or model probabilities computed','No matching within AD-100 outcome window',
        'Reference values do not establish availability at reference close','Full historical price linkage not established',
        'Membership and float still block exact rule replication'])
    (out/'pilot_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (out/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2));print('OUTPUT',out)
if __name__=='__main__':main()
