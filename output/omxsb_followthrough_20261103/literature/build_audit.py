"""Source/claim metadata only. Never imports or reads event outcomes."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json

P = Path(__file__).resolve().parent
WORK = P.parents[1]
spec = P.parent / 'design/PRIMARY_SPEC.txt'
sources = [
 dict(id='HG1986', authors='Lawrence Harris; Eitan Gurel', year=1986,
 title='Price and Volume Effects Associated with Changes in the S&P 500 List: New Evidence for the Existence of Price Pressures',
 url='https://doi.org/10.1111/j.1540-6261.1986.tb04550.x',
 fulltext_url='https://static1.squarespace.com/static/5e6033a4ea02d801f37e15bb/t/5f6246a2d40a936b59607e69/1600276134797/harris_gurel_sp500_jf.pdf',
 read='Scanned original visually inspected: printed pp.817–823 and 825–827; focus §II.A pp.818–819 Table I and §II.C pp.825–826 Table V.',
 local_pdf=str(P/'private/harris_gurel.pdf'),
 evidence='Daily and multi-day market-adjusted share-volume ratios use an eight-week preceding baseline; Table V tracks pre/post daily and weekly activity. A short spike and longer activity are already separate objects.',
 difference='Our measure is gross SEK value, matched fixed peers, 45 sessions, and an additive split; these are local design choices rather than a new abnormal-volume concept.',
 limitation='Does not trace identical orders shifted between days; its price-pressure interpretation is not identification for our sample.'),
 dict(id='GS2023_2024', authors='Robin Greenwood; Marco Sammon', year=2025,
 title='The Disappearing Index Effect',
 url='https://doi.org/10.1111/jofi.13410',
 fulltext_url='https://marcosammon.com/images/greenwood_sammon.pdf',
 read='June2023 author manuscript §2.4.3 pp.25–26 and Figure11 (PDF index46); March2024 Harvard-deposited manuscript p.25 coordination subsection.',
 local_pdf=str(P/'private/greenwood_sammon_draft.pdf'),
 evidence='2023 manuscript normalises each day by total ±22-day volume; reported concentration rises over decades. The 2024 manuscript retains concentration discussion citing Chinco–Sammon, without the same Figure11.',
 difference='An external-baseline 45-day level is not mechanically fixed by normalisation to window total. It addresses an interpretive gap in the local E5 replication.',
 limitation='Exact Figure11 citation applies only to June2023 version. Final published PDF was not obtained; do not assert identical figure numbering or language.'),
 dict(id='CHANG2025', authors='Xin Chang; Jiang Luo; Jiaxin Peng; Shuoge Qian; Choon Wee Tan', year=2025,
 title='Index-tracking rigidity and arbitrage opportunities in MSCI index reconstitutions',
 url='https://doi.org/10.1016/j.pacfin.2025.102900',
 fulltext_url='https://www.sciencedirect.com/science/article/pii/S0927538X25002379',
 read='Publisher abstract, introduction and Daily analysis section snippet retrieved through web search. Full paper tables not read.',
 local_pdf=None,
 evidence='Across 56 MSCI markets 2006–2023, introduction reports AD+1 and ED−1 abnormal-turnover spikes and final-minute shares of ED−1 volume of 41% for additions and 49.8% for deletions.',
 difference='Our daily accounting contains no minute-level or lending evidence and cannot inherit their investor-rigidity interpretation.',
 limitation='Access to excerpts does not establish absence of cumulative volume tests elsewhere in the full paper.'),
 dict(id='DFA2025', authors='Kaitlin Hendrix; Jerry Liu; Trey Roberts', year=2025,
 title='Measuring the Costs of Index Reconstitution: Evidence Outside the US',
 url='https://www.dimensional.com/chmedia/407991/source/measuring-the-costs-of-index-reconstitution-evidence-outside-the-us.pdf',
 fulltext_url='https://www.dimensional.com/chmedia/407991/source/measuring-the-costs-of-index-reconstitution-evidence-outside-the-us.pdf',
 read='Printed pp.6–8, Volume Pressure/Intraday Volume Pressure, Exhibits3–4; p.9 conclusion.',
 local_pdf=None,
 evidence='Daily USD trading-value multiples versus t−20 are plotted over t−20:t+20. Intraday multiples compare corresponding 15-minute intervals against a preceding average.',
 difference='Our total uses a 50-session baseline and matched peers with fixed common support; the plotted spike itself is already known.',
 limitation='Primary practitioner research by asset manager, not peer-reviewed independent evidence; its trading-cost claims are not demonstrated by our gross-value test.'),
]
for s in sources:
    p=s['local_pdf']
    s['sha256']=hashlib.sha256(Path(p).read_bytes()).hexdigest() if p else None

def dump(name,v):
    (P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
dump('SOURCE_LEDGER.json',sources)
fields=['id','authors','year','title','read','evidence','difference','limitation','url']
with (P/'CLOSEST_PAPERS.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    w.writerows({k:r[k] for k in fields} for r in sources)
harvard=WORK/'deep_audit/greenwood_sammon_harvard.pdf'
dump('AUDIT_SCOPE.json',dict(
 created_utc=datetime.now(timezone.utc).isoformat(),
 no_new_outcome_calculations=True,
 no_new_outcome_estimates_read=True,
 no_design_changes_recommended=True,
 input_spec_path=str(spec),input_spec_sha256=hashlib.sha256(spec.read_bytes()).hexdigest(),
 local_harvard_version_path=str(harvard),local_harvard_version_sha256=hashlib.sha256(harvard.read_bytes()).hexdigest(),
 harvard_deposit_url='https://dash.harvard.edu/entities/publication/2cc676bd-c8da-40e7-b112-3ecc8644e687',
 harvard_document_titlepage_version='March 2024 manuscript, with repository cover citing 2025 publication',
 current_harvard_download_attempt='HTTP429; already existing local primary-source PDF and text used instead',
 population='Parent-specified source-complete65 additions, originating in70 ownership-covered additions2019–2023;3frozen peers;10reviews expected',
 primary='45sessions ED−22..ED+22 minus own baseline, event minus3peer mean; total only; ED−1/other44 descriptive identity',
 baseline='50sessions ending at min(AD−12, ED−23), from read PRIMARY_SPEC',
 local_result_exposure='Initial keyword search returned limitation strings in PRIMARY_RESULT.json and code, not numeric estimates. No result file or result values opened.',
 search_scope='Four closest primary documents; bounded targeted check, not systematic novelty review',
 decision='USEFUL_LOCAL_COMPLEMENT_NOT_NEW_GENERAL_MECHANISM_OR_METHOD',
))
dump('READ_LOG.json',dict(
 queries=['index reconstitution trading volume displacement trading across days index implementation volume Madhavan',
 'Greenwood Sammon disappearing index effect trading volume reconstitution turnover paper pdf',
 'Harris Gurel 1986 price volume changes S&P500 pdf volume normal20days',
 'Index-tracking rigidity volume pdf', 'Harris Gurel cumulative volume'],
 failed_access=['Publisher direct MSCI page HTTP403; indexed publisher introduction available', 'Harvard fresh PDF download HTTP429; local deposited manuscript read'],
 raw_private_files='PDFs and rendered source pages stay in private; never part of public allowlist',
 no_world_novelty_claim=True,
))
print(json.dumps({'papers':len(sources),'decision':'local complement; no new test'}))
