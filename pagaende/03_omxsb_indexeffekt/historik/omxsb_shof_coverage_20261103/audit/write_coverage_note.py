from pathlib import Path
import pandas as pd,json,hashlib,datetime
O=Path(__file__).resolve().parent
R=pd.read_csv(O/'remaining_fund_gap_ranking_B.csv',dtype={'fund_id':str});D=pd.read_csv(O/'event_role_endpoint_coverage.csv');E=pd.read_csv(O/'fund_review_source_eligibility_ABC.csv',dtype={'fund_id':str});X=pd.read_csv(O/'remaining_fund_review_gaps_B.csv',dtype={'fund_id':str})
notes={
'51670':'Mixed shareclass currencies. From2020H2 onward inspected windows have25positivecapital/TRI endpoints; allSEKscreen alone fails. Need actualdatedFX/classcurrency validation; earlier2019history also short.',
'51318':'Mixed currencies plus classstart/missingclass history in earlier windows. In2022H2–2023H2 allother inspectedmonthlychecks pass; FX/datedactiveclass handling is a concrete source task, not yet approved eligibility.',
'51545':'2019source begins2018; later failures are one capitalreconciliation endpoint in25. Retrieve/reconcile actual dated TNA for that month; no automatic tolerance relaxation.',
'51313':'One capitalreconciliation endpoint fails in2022H1–2023H2; rawdate/identity check needed (oldminimum classsum/fundTNA≈0.8435), not assumed rounding.',
'51381':'No monthly source observations for mappedFundId in inspectedwindows. DirectrawSHoFretrieval is a bounded source test; availability unproved.',
'60908':'Earlierfuture/newclass presence and latercapitalreconciliation gaps. Check datedactiveclassunion and actual rawTNA dates; retain all sourcefailures.',
'60087':'Rawpilot nowavailable. A-classTRIstarts2023-10; B haslonghistory but is not substituted. VendorfundNF has14missingdates. Root checking NAV/dividends/splits separately.',
'60730':'Mixedcurrencies plus oldunconvertedclasssum fails; actual FX and datedactiveclasses required before economicuse.',
'51449':'Mixedcurrencies and earlierclasscapital/TRI missingness. Datedclassstarts plus rawsource/FX check; not just dropminorclasses.',
'51734':'Olderclasssum/fundTNA reconciliation and2017history gaps; laterwindows passA. ActualdatedrawTNA check targeted at earlierwindows.',
'51776':'OldsourcehasmissingclassTNA and laterfundTNA/reconciliation problems; retrieve datedrawclasscapital/identity before interpreting.',
'54155':'No previousmonthly source observations on mappedFundId; possible rawsource retrieval target, unproved.',
'60824':'Rawpilot confirms TRIonlyfrom2023-10; classNFcomplete2023H2 is a separate route. September2022fundTNA is dated8days beforeclassTNA; no silentfund/classsubstitution.',
'51204':'Mixedcurrencies and someclassTRI missing; requires actualclasscoverage plus FX, not summingcurrencyamounts.',
'51541':'Earlierclasscapital/TRI missing despite oneSEKclassavailable; verify actualclassinceptions/history. Laterwindows already passA.',
'51482':'Rawpilotavailable. NOKclasses and2022-05inceptions require a separatelylocked datedactiveunion/FX rule; D not applied.',
'60302':'Rawpilotavailable.2022newclasschangesstrictclasslist; no silentgatechange. Absent fromfixedoriginalfundpopulation2019H2/2020H2.'}
top=R[(R.scope=='event_role')&(R['rank']<=15)].copy();top['source_repair_note']=top.fund_id.map(notes).fillna('See per-review source flags; no promised repair.');top.to_csv(O/'PRIORITY_REPAIR_TARGETS.csv',index=False)
# Identities are metadata only, not newsource requests or neweconomic sample selection.
master=pd.read_excel('/Users/ludviguvang/dev/financethesis/data/raw/shof/fundmaster.xlsx',usecols=['performanceid','secid','fundid','ISIN','currencyid','inceptiondate','obsoletedate','shareclasslegalname']).drop_duplicates('performanceid')
fi=E[E.fund_id.isin(top.fund_id)][['fund_id','fundid']].dropna().drop_duplicates();idmap=fi.merge(master,on='fundid').merge(top[['fund_id','rank','fund_name','source_repair_note']],on='fund_id');idmap.to_csv(O/'PRIORITY_REPAIR_CLASS_IDENTIFIERS.csv',index=False)
rows=[]
for sc in ['A','B','C']:
 d=D[D.scenario.eq(sc)];ev=d[d.role.eq('event')];rows.append({'scenario':sc,'allcells_mean_pct':100*d.coverage_fraction.mean(),'allcells_pooled_SEK_pct':100*d.covered_SEK_at_q1price.sum()/d.denominator_SEK_at_q1price.sum(),'event_q0_mean_pct':100*ev[ev.endpoint.eq('q0')].coverage_fraction.mean(),'event_q1_mean_pct':100*ev[ev.endpoint.eq('q1')].coverage_fraction.mean()})
pd.DataFrame(rows).to_csv(O/'HEADLINE_COVERAGE_TABLE.csv',index=False)
v=[]
for sc in ['V_fundNF','V_classNF']:
 d=D[(D.scenario==sc)&(D.review=='2023H2')];v.append(dict(route=sc,review='2023H2',events=d.event_id.nunique(),eligible_funds_per_event_min=int(d.eligible_funds.min()),eligible_funds_per_event_max=int(d.eligible_funds.max()),allcells_mean_pct=100*d.coverage_fraction.mean(),pooled_SEK_pct=100*d.covered_SEK_at_q1price.sum()/d.denominator_SEK_at_q1price.sum(),interpretation='Separate vendor-estimated NFsourceavailability only; no mixing intoABC or claim of economicusability.'))
pd.DataFrame(v).to_csv(O/'SEPARATE_VENDOR_NF_2023H2_COVERAGE.csv',index=False)
note='''Kapitaltäckning efter SHoF-pilot — 3 november 2026
Tekniskt beslutsunderlag, inte uppsatstext. Inga fondavkastningar, flöden, kovarianser eller riskutfall har beräknats.

Samma 135 händelser före 2024 (70 inträden, 65 utträden), 10 omviktningar och tre ursprungliga kontrollaktier behålls. Varje händelse har samma fondpopulation i alla fyra aktier och båda kvartalsändpunkterna. Källkraven bestämmer vilka fonder som är täckta oberoende av om de äger just aktien.

A återskapar det tidigare preliminära källurvalet exakt: 5 089 fond/omviktningsrader och 1 080 kapitaltäckningsceller stämmer fält för fält. En separat kapitalberäkning avviker högst 2,22e-16 i täckningsandel.
B uppdaterar bara fem pilotfonders historiker med den strikta all-aktiva-klasser/25-ändpunktsgrinden. Ingen representativ B-klass ersätter en hel fond. Av pilotens 23 godkända fond/omviktningshistoriker finns 21 i ursprunglig rapportpopulation: 60302 saknas där 2019H2 och 2020H2 och förs därför inte in.
C visar endast kapital som täcks av de nya rågranskade pilotfondernas godkända historiker, med samma ursprungliga nämnare. Rågranskning är inte fullständig ekonomisk eller historisk identitetscertifiering.

                         A       B       C
Medel över alla celler    32,45%  37,69%   5,24%
Kapitalvägt över celler   34,21%  39,14%   4,93%
Eventaktier q0, medel     31,31%  37,49%   6,18%
Eventaktier q1, medel     31,04%  37,55%   6,50%

B innebär en verklig men begränsad förbättring. Bara en av 135 händelser når minst 50% i samtliga åtta celler; ingen når 75% eller 90%. I A och C når ingen händelse 50% i alla celler. Den enda B-händelsen är utträdet OMXSB-2021H2-21, med minsta täckning 51,25%. Gränserna är deskriptiva; de anger varken statistisk styrka eller klartecken för en riskanalys.

De största kvarvarande luckorna i eventaktierna, kapitalviktat inom den fasta designen:
51670 Lannebo Småbolag: 5,49% av hela nämnarens kapital.
51318 Handelsbanken Svenska Småbolag: 5,09%.
51545 Swedbank Robur Småbolagsfond Sverige: 2,99%.
51313 Didner & Gerge Aktiefond: 2,76%.
De första två har betydande valutaklassproblem; 51545 och 51313 har senare fönster där en kapitalavstämningsmånad faller. Det är konkreta källuppgifter, inte bevis att de kan repareras. Full rangordning, tidigare källsteg och aktuella klass-ID finns i PRIORITY_REPAIR_TARGETS.csv och PRIORITY_REPAIR_CLASS_IDENTIFIERS.csv. Piloter som redan hämtats markeras särskilt så att gamla nollrader inte misstolkas som fortsatt helt saknade rådata.

Kapitalvikter: inom varje aktie är andel av aktieantalet samma som kapitalandel vid ett gemensamt pris. För kapitalvägning mellan aktier värderas båda ändpunkterna till respektive akties gemensamma q1-pris från FI, med tidigare validerad splitjustering av q0-antal. Ingen prisavkastning har beräknats. Samma kontrollaktie kan återkomma i flera händelser; summan är därför designens värderade exponeringar, inte unikt fondkapital eller marknadens förmögenhet. Ingen cell har saknad nämnare i denna beräkning; koden behåller sådana celler som NA om de förekommer. Noll täckt kapital betyder att ingen kvalificerad källa täcker innehavet, inte att fondflödet är noll.

Vendor-NF redovisas separat endast som källtäckning 2023H2: fond-NF för 51331, respektive klass-NF för 51331 och 60824. Fälten är leverantörsestimat och blandas inte med TNA/TRI-vägen i A/B/C. Se SEPARATE_VENDOR_NF_2023H2_COVERAGE.csv. Klassidentitet, kalender, kapitalavstämning och ekonomisk användbarhet återstår även vid komplett närvaro.

En föreslagen förbättrad regel för daterade klassinträden och valuta kan senare ändra källurvalet. Ingen sådan D-variant har tillämpats här. Tidigare strikta gränser, negativa fynd och källa för varje uppdatering behålls. Inga nya ekonomiska utfall eller efterhandsval av händelser har gjorts.
'''
(O/'REPORT_SV.txt').write_text(note)
(O/'README_REPLAY.txt').write_text('Run original unchanged source_feasibility.py, then update_capital_coverage.py, then write_coverage_note.py. Python: /Users/ludviguvang/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3. Requires pandas,numpy,openpyxl. Repository and prior audits read-only. Source-data paths and hashes in SOURCE_FEASIBILITY_LOCK.json and COVERAGE_UPDATE_LOCK.json. Only this folder receives outputs. Common fundpopulations preserved; no economic outcomes. Keep A/B/C separate from vendor-NF appendix and from any later D rule. Source flags for nonpilot funds remain provisional. Private raw licensed values are not copied to publication.\n')
print(pd.DataFrame(rows).to_string(index=False));print(pd.DataFrame(v).to_string(index=False));print('Report and repair target metadata complete.')
