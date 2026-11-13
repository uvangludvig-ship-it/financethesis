"""Build source-only institutional note. No security prices or economic outcomes."""
from pathlib import Path
import csv
import hashlib
import json
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REVIEW_INPUT = ROOT / 'omxsb_history_extension_20261103/sources/REVIEW_VERIFICATION.csv'

def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def write_csv(name, rows):
    with (HERE / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def source(id, title, url, locator, supported, not_supported, quote=''):
    return dict(source_id=id, title=title, url=url, locator=locator,
                supported=supported, not_supported=not_supported, short_quote=quote,
                read_method='web primary source text', raw_body_sha256=None)

S = [
 source('S01', 'Stockholmsbörsen: XACT SBX – en ny börshandlad fond noteras, 2 juni 2003',
 'https://news.cision.com/se/stockholmsborsen/r/xact-sbx---en-ny-borshandlad-fond-noteras,c80505',
 'Press release body; publication shown 2003-06-02 10:17 CET by archive',
 'XACT SBX listed that day; SBX launched 12 April 2001; base 30 December 1995 = 100; semiannual revisions; 80–100 liquid shares.',
 'Does not establish first ever SBX passive demand, exact seed capital, an unanticipated shock, or historical ADs.',
 'SBX-index lanserades den 12 april 2001'),
 source('S02', 'MSCI/NOREX: new GICS classification and benchmark indices, 27 November 2000',
 'https://www.msci.com/eqb/pressreleases/archive/20001127_pr.pdf',
 'One-page original release, paragraphs 5–6',
 'Free-float investability was an original design feature. Stockholm GICS adoption scheduled 5 January 2001. Benchmark launch was then planned for February 2001.',
 'The announced February plan is not evidence of actual February SBX launch. Later exchange source S01 states actual 12 April 2001.',
 'new benchmark indices, which take into account free float'),
 source('S03', 'Sjunde AP-fonden: Årsredovisning 2002, del 2',
 'https://www.ap7.se/app/uploads/2017/04/ap7_arsredovisning_2002_del2.pdf',
 'Printed pp.4/10: allocation by style; pp.5/11: benchmark switch; pp.8/14: audit dated 13 February 2003. PDF zero-based pages 5/11, 6/12, 9/15.',
 'Pre-ETF Swedish index-management sleeves and explicit SBX transition in both funds.',
 'Style allocation is not total-fund weight, exact replication, review orders or dated tracker AUM.',
 'SBX Stockholmsbörsens benchmarkindex (från och med den 1 augusti 2002)'),
 source('S04', 'Andra AP-fonden: Årsredovisning 2002',
 'https://ap2.se/wp-content/uploads/2021/03/arsredovisning-2002.pdf',
 'Printed pp.20–21 (PDF zero-based 21–22), Swedish equities discussion and Swedish SIXRX/SBX mandate table; p.44 (PDF45) style split.',
 'Benchmark switch in autumn 2002: 70% Swedish equity reference SBX, remainder OSX/CSX. Internal portfolio 1 is labelled passive under combined SIXRX/SBX mandates; SEB and Carlson are active.',
 'Combined annual SIXRX/SBX label does not date every mandate switch or quantify pure SBX replication capital. Active benchmarked mandates must not be counted as strict passive.',
 'Portfölj 1 (passiv)'),
 source('S05', 'OMX Exchanges: Gemensam global branschklassificering för alla NOREX-börser, 19 January 2005',
 'https://news.cision.com/se/omx-exchanges/r/gemensam-global-branschklassificering-for-alla-norex-borser,c132347',
 'Press release body',
 'Stockholm, Oslo and Copenhagen had used GICS since 2001; 2005 expansion concerns Helsinki, Iceland and Baltic exchanges.',
 'Not a new Stockholm classification regime starting in 2005, and not a documented SBX selection-rule break.'),
 source('S06', 'OMX Exchanges: OMX harmoniserar indexnamn, 22 August 2005',
 'https://news.cision.com/se/omx-exchanges/r/omx-harmoniserar-indexnamn,c161338',
 'Opening paragraph and benchmark name paragraph',
 'Stockholm benchmark renamed OMXSB effective 3 October 2005. Narrative also mentions ongoing rule and calculation-system harmonisation.',
 'Does not date a specific change in SBX constituent selection, buffers, turnover thresholds, free-float bands or cap treatment. Do not code rename as a methodology shock.'),
 source('S07', 'OMHEX: sale of XACT Fonder to Svenska Handelsbanken, 16 June 2004',
 'https://news.cision.com/omhex/r/omhex-sells-xact-fonder-to-svenska-handelsbanken,e107255',
 'Opening paragraph',
 'Announced ownership transfer of XACT Fonder, which managed XACT OMX and XACT SBX, effective 30 June 2004.',
 'Not an index methodology change; no documented exogenous demand increase or date-specific index purchase quantity.'),
 source('S08', 'OMX annual report 2004',
 'https://ir.nasdaq.com/static-files/f21b62a2-ac7f-48f0-831a-1d83ee47b933',
 'PDF zero-based p.54, Integration work related to merger of OM and HEX. Text font encoding corrupts numerical page label.',
 'September 2004 integration included harmonisation of trading rules and Stockholm/Helsinki opening hours.',
 'This passage does not specify precise before/after clock times or support assuming a constant intraday market model over the sample.'),
 source('S09', 'OMX Stockholm: Avista, ny sammansättning av OMX Stockholm Benchmark index (175/07), 12 June 2007',
 'https://www.globenewswire.com/news-release/2007/06/12/116558/0/sv/avista-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-175-07.html',
 'Original review notice body',
 'New composition effective 2 July 2007, with dated announcement. This is a confirmed historical January/July-era review.',
 'Does not verify any of the eight earlier workbook candidate dates or their issuer lists.'),
 source('S10', 'Nasdaq OMX: New OMX Stockholm Benchmark portfolio selected, 11 May 2009',
 'https://www.globenewswire.com/news-release/2009/05/11/2584/0/da/New-OMX-Stockholm-Benchmark-portfolio-selected.html',
 'Original review press release body',
 'Composition effective 1 June 2009, showing a later June effective date rather than the older July example.',
 'One notice alone is not a complete rule change log. The local verified review calendar documents January 2009 followed by June 2009.'),
]

for s in S:
    assert len(s['short_quote'].split()) <= 25
write_json('SOURCE_LEDGER.json', S)

rows = list(csv.DictReader(REVIEW_INPUT.open()))
assert len(rows) == 8
pre = [r for r in rows if r['candidate_effective_date'] < '2003-06-02']
post = [r for r in rows if r['candidate_effective_date'] > '2003-06-02']
count = lambda rr: sum(int(r['candidate_additions']) + int(r['candidate_deletions']) for r in rr)
assert (len(pre), count(pre), len(post), count(post)) == (1, 9, 7, 48)
write_json('FEASIBILITY.json', dict(
    generated_utc=datetime.now(timezone.utc).isoformat(),
    decision='CONTEXT_ONLY_NOT_CAUSAL_ETF_BREAK',
    candidate_pre_reviews=len(pre), candidate_pre_events=count(pre),
    candidate_post_reviews=len(post), candidate_post_events=count(post),
    source_verified_early_reviews=sum(r['review_verified'].lower() == 'true' for r in rows),
    all_counts_are_candidate_metadata_not_independent_policy_replications=True,
    seed_date='2002-08-12', seed_rows=79, seed_rows_are_additions=False,
    all_early_ADs_missing=True, new_study_outcomes_retrieved_or_computed=False,
    inference='One candidate pre-review cannot identify a secular pretrend or supply independent repeated pre-launch review variation. More stocks do not create more institutional launches.',
    missing=['Original review AD/ED/issuer notices', 'Dated complete tracker AUM and basket demand', 'Contemporaneous complete index methodology versions', 'Comparable price/auction measurement where relevant'],
))
write_json('INPUT_LEDGER.json', dict(
    review_metadata_path=str(REVIEW_INPUT),
    review_metadata_sha256=hashlib.sha256(REVIEW_INPUT.read_bytes()).hexdigest(),
    source_workbook_sha256='555fce1ee8d7a82965fa178d01db179a531d0813d7946a06d919154b56a41316',
    workbook_used_only_indirectly_via_previous_frozen_metadata=True,
    previous_sources_package='work/omxsb_history_extension_20261103/sources',
    main_repo_plan_read_only='/Users/ludviguvang/dev/financethesis/PLAN.md',
    main_repo_calendar_read_only='/Users/ludviguvang/dev/financethesis/data/input/omxsb/omxsb_notes_2005_2012.md',
))

timeline = [
 ('1995-12-30','day','index_base','Retrospective SBX base date, not live publication or selection event','S01','No pre-launch event inference'),
 ('2000-11-27','day','advance_method_announcement','MSCI/NOREX announces free-float benchmarks; February 2001 intended launch','S02','Planned date superseded by later actual-launch evidence'),
 ('2001-01-05','day_planned','classification','Announced Stockholm GICS/industry-index adoption; 2005 release confirms use since 2001','S02;S05','Exact implementation day not independently reverified'),
 ('2001-04-12','day','live_launch','Actual SBX index launch stated by exchange in 2003','S01','Not 1995 backcast date'),
 ('2002-08-01','day','investor_benchmark','AP7 Swedish equity benchmark switches SIX-RXA to SBX; index-managed sleeve documented for 2002','S03','Ethical exclusions; not all Swedish assets are passive'),
 ('2002','autumn','investor_benchmark','AP2 Swedish reference changes to SBX/OSX/CSX; passive and active mandates coexist','S04','No invented exact day'),
 ('2003-06-02','day','ETF_listing','XACT SBX listing','S01','New listed channel, not first proven SBX index demand'),
 ('2004-06-30','day_announced','provider_ownership','XACT Fonder ownership transfer to Handelsbanken announced','S07','Not selection-rule change or observed demand dose'),
 ('2004-09','month','market_structure','Trading-rule and Stockholm/Helsinki opening-hours harmonisation','S08','No precise intraday clock rule inferred'),
 ('2005-01-19','day','classification_announcement','GICS extension to remaining NOREX exchanges announced; Stockholm already GICS','S05','Not Stockholm 2005 GICS adoption'),
 ('2005-10-03','day','index_rename','SBX becomes OMXSB under harmonised index names','S06','No verified simultaneous SBX selection-rule shock'),
 ('2007-07-02','day','verified_review_ED','Confirmed half-year review; AD 12 June 2007','S09','Cannot fill earlier ADs'),
 ('2009-06-01','day','later_schedule_comparator','Confirmed June effective date, after old January/July era','S10;local_calendar','Outside 2001–07; included only for later-measurement comparison'),
]
write_csv('TIMELINE.csv', [dict(zip(['date_or_period','precision','event_type','fact','source_ids','limitation'],r)) for r in timeline])
investors = [
 ('AP7 Premiesparfonden','2002','index_managed_sleeve_with_exclusions','Documented before ETF; see S03 and report','S03','No full-replication assumption or review-order quantities'),
 ('AP7 Premievalsfonden','2002','index_managed_sleeve_with_exclusions','Documented before ETF; see S03 and report','S03','Same manager; not independent institutional adoption'),
 ('AP2 internal portfolio 1','2002','passive_under_combined_annual_SIXRX_SBX_label','Passive table label and autumn overall SBX transition','S04','Exact internal mandate switch date and pure SBX capital not separated'),
 ('AP2 SEB/Carlson Swedish mandates','2002','active_benchmarked','SBX reference and active management designation','S04','Do not classify as strict passive merely because benchmark is SBX'),
 ('Robur Mix Indexfond / later Indexfond Sverige','before_2003_06_02','UNVERIFIED_SBX_MANDATE','Bounded primary-source search did not establish contemporaneous SBX mandate or exact pre-launch strategy','','Fund existence or later name is insufficient; no historical passive SBX flag'),
 ('XACT SBX','2003-06-02','ETF_tracking_SBX','Exchange confirms listing and index-tracking objective','S01','Launch AUM, seed basket execution and net incremental demand not established'),
]
write_csv('INVESTOR_EVIDENCE.csv', [dict(zip(['institution_or_fund','dated_scope','classification','evidence','source_ids','limitation'],r)) for r in investors])

write_json('DECISION_TABLE.json', [
 dict(use='Institutional history',status='GO',meaning='SBX was live from 2001, used institutionally before its dedicated ETF, and later renamed OMXSB.',claim_limit='No causal price or liquidity effect.'),
 dict(use='Extend the same event description to early SBX years',status='CONDITIONAL',meaning='Potentially documents whether later index patterns also appear in the early live era.',requirements='Original AD/ED/issuer validation and comparable measurement under the existing design; no new outcome test authorised here.',claim_limit='An era comparison is not an ETF treatment estimate.'),
 dict(use='Natural experiment at XACT launch',status='REJECT_WITH_CURRENT_DATA',meaning='One candidate pre-review, prior index management, no measured incremental dose, and time-varying market institutions.',claim_limit='A positive result would not isolate ETF causation; a null would not prove no ETF effect.'),
])

write_json('SEARCH_LOG.json', dict(
    method='Bounded public primary-source search, source text reads and existing source-calendar metadata only. No authenticated service or contact.',
    representative_queries=[
      '"SBX" "passiv" "2002" "AP"', 'site:ap7.se "2002" "SBX"',
      'site:ap7.se "arsredovisning_2002"', 'site:ap7.se "årsredovisning" "2002" "Sverige" "25"',
      '"Roburs Mix Indexfond" "SBX"', 'site:news.cision.com "Roburs Mix Indexfond" "2002"',
      'site:swedbank.com "Mix Indexfond" "2002"', '"SBX" "Robur" "2001"',
      '"Stockholmsbörsen" "nya index" "2001"', '"SBX" "index" "free float" "2001"',
      '"NOREX" "Global Industry Classification" "2005"', '"OMXSB" "2006" "rules" "changed"',
      '"XACT SBX" "2003" "Maj"', '"OMHEX sells XACT Fonder to Svenska Handelsbanken"',
    ],
    unresolved=['Robur pre-June-2003 SBX replication mandate', 'Complete 2001–07 SBX rule-change history', 'Earliest advance announcement of XACT SBX and actual launch capital'],
    absence_interpretation='Search non-result is not evidence that a fund or historical rule change did not exist.',
))
print(json.dumps({'metadata_only': True, 'pre': [len(pre), count(pre)], 'post': [len(post), count(post)]}))
