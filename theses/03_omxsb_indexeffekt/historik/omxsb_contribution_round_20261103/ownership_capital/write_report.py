from pathlib import Path
import pandas as pd,json,hashlib,datetime
O=Path(__file__).resolve().parent;R=Path('/Users/ludviguvang/dev/financethesis');a=pd.read_csv(O/'summary.csv');c=pd.read_csv(O/'same_support_counts_capital.csv');b=pd.read_csv(O/'addition_benchmark_components.csv');v=json.load(open(O/'validation.json'));iv=json.load(open(O/'independent_validation.json'));raw=json.load(open(O/'raw_control_validation.json'));support=pd.read_csv(O/'fund_support.csv');gate=pd.read_csv(O/'event_feasibility_gate.csv');sg=pd.read_csv(O/'security_feasibility_gate.csv')
def get(metric,group='ALL',ty='addition'):return a[a.type.eq(ty)&a.group.eq(group)&a.metric.eq(metric)].iloc[0]
def fmt(r):return f"{r.mean_pp:+.4f} [{r.ci95_low:+.4f}; {r.ci95_high:+.4f}]"
p=get('matched_new_minus_preexisting');n=get('matched_new');old=get('matched_preexisting');net=get('matched_total');idx=c[c.type.eq('addition')&c.group.eq('OMXSB_index_named')].iloc[0];oth=c[c.type.eq('addition')&c.group.eq('OMXSB_other_named')].iloc[0]
lines=[
'OMXSB: NYA FONDÄGARE OCH KAPITALMÄNGD — NY GENOMFÖRD UPPDELNING',
'3 november 2026. Tekniskt forsknings- och beslutsunderlag, INTE uppsatstext.',
'',
'KORT SVENSK LÄSNING',
f'På {v["additions"]} tillägg och {v["reviews"]} översyner är ökningen av observerade nettopositioner jämfört med tre fasta kontroller {fmt(net)} procentenheter av bolagsvärdet. Nytillkomna fondpositioner bidrar {fmt(n)}. Tidigare ägare tillsammans bidrar {fmt(old)}. Det positiva matchade nettot ligger alltså i nya positioner i detta urval; tidigare ägares bidrag är osäkert och har negativ punktskattning.',
f'Det enda primära kontrastmåttet, nya minus tidigare ägares bidrag, är {fmt(p)} procentenheter. Intervallet behåller samvariationen mellan delarna. Det är nominellt och explorativt efter tidigare kända projektresultat.',
f'En konkret mätkonsekvens: på exakt samma stöd ger OMXSB-fonder med indexindikerande namn {idx["count"]:+.3f} ägare och {idx.pp:+.4f} kapitalenheter, medan OMXSB-fonder med andra namn ger {oth["count"]:+.3f} ägare och {oth.pp:+.4f}. Gruppen med fler extra fondnamn har alltså mindre extra normaliserat kapital. Fondantal och belopp rangordnar dessa grupper olika. Namnen är inte en verifierad aktiv/passiv-klassificering.',
'',
'VAD SOM ÄR NYTT, OCH VAD SOM REDAN FANNS',
'Tidigare demand/build_panel.py hade redan positive_from_zero_pp och positive_from_existing_pp för13 kandidatfonder. För gamla frysta112tillägg var dessa0.950921 och0.070111 av totalt1.021032 positiva fondnetton; signerad nettomängd1.018987. Det var ingen kontrolljusterad all-fond-uppdelning. Den analysen redovisas som tidigare arbete, inte som ny upptäckt.',
'Denna nya beräkning omfattar den stabila, rapporterande fondpopulationen och ursprungliga tre kontrollaktier, samt alla tre additiva delar: nya, kvarvarande och utträdande positioner. Ingen metodprioritet eller global nyhetsclaim görs. Parallell litteraturgranskning har identifierat Pavlova–Sikorskaya och van der Beck som nära tidigare arbeten; se källnot nedan.',
'',
'ADDITIV BOKFÖRING, TILLÄGG',
'Enhet: procentenheter av hela emittentens aktiemarknadsvärde, samma slutkurs för före- och efterantal.',
'Komponent                       Händelse       Medel3kontroller      Skillnad',
]
for key,label in [('new','Nya ägare'),('continuing','Kvarvarande ägare'),('exiting','Utträdande ägare'),('total','Samtliga')]:
 lines.append(f'{label:30s} {get("event_"+key).mean_pp:+.6f}       {get("control_"+key).mean_pp:+.6f}          {get("matched_"+key).mean_pp:+.6f}')
lines += [
'En positiv matchad utträdesdel betyder mindre avveckling än hos kontrollerna. Det betyder inte att utträdande fonder köper. Nya+fortsatta+utträdande summerar exakt till totalen; signerade andelar kan därför överstiga100%. Ingen andelskvot används som huvudresultat.',
'',
'BENCHMARKUPPDELNING, ENBART BESKRIVANDE',
]
for group in ['OMXSB_index_named','OMXSB_other_named','broad_H','other_broad_Sweden','other_or_unknown']:
 lines.append(f'{group}: nya {get("matched_new",group).mean_pp:+.6f}; kvarvarande {get("matched_continuing",group).mean_pp:+.6f}; utträdande {get("matched_exiting",group).mean_pp:+.6f}; netto {get("matched_total",group).mean_pp:+.6f}.')
lines += [
'OMXSB-familjens nettobidrag överstiger totalnettot eftersom övriga grupper tillsammans har negativt bidrag. Detta är en summa av observerade komponenter, inte familjens andel av orsakad prisrörelse.',
'',
'BORTTAG, FÖRDEKLARERAT BESKRIVANDE',
f'{v["deletions"]} borttag,14översyner. Matchat netto {fmt(get("matched_total",ty="deletion"))}. Nya {get("matched_new",ty="deletion").mean_pp:+.6f}, kvarvarande {get("matched_continuing",ty="deletion").mean_pp:+.6f}, utträdande {get("matched_exiting",ty="deletion").mean_pp:+.6f}. Detta är en spegelbeskrivning, inte en andra vald primär hypotes.',
'',
'URVAL, ENHETER OCH RAPPORTSTÖD',
'Gamla219ägarevent korsades med tidigare216validerade kapitalhändelser:204gemensamma,111tillägg/93borttag. Kontrollerna saknade tidigare motsvarande kapitalgrind. Ny kontrollgrind utesluter19hela jämförelser på olösta enheter/ISIN, gamla uppgifter, få oberoende nominella prisrapporter eller oförenligt klassvärde.185återstår:98tillägg/87borttag. Kontroller byts aldrig ut. Fullt utfall från alla grindscreeningar finns i event_feasibility_gate.csv/security_feasibility_gate.csv.',
'För händelseaktien används den tidigare granskade råa FI-slutkursen och samma bolagsvärde exakt. Kontrollaktier kräver minst3fondrapporter inom1% av nominellt SEK-medianpris i båda kvartal, positivt historiskt TR-bolagsvärde högst7dagar gammalt, rimlig aktieslagsvärde/bolagsvärde-kvot, verifierad klassidentitet, samt oförändrat accepterat ISIN-set eller dokumenterad fysisk split. Prisdiagnostik större än3% utan daterad upplösning stoppar jämförelsen. Prisrelationen härleder aldrig ensam en splitfaktor. Detta är stöd från identifierare och två datakällor, inte en uttömmande leverantörslogg över samtliga bolagshändelser.',
'Varför preliminärt184blev185: OMXSB-2024H2-03(Betsson) hade redan en validerad aktieslagsnämnare i den tidigare kapitalgrinden. Den första generiska rawshares-kontrollen gav felaktigt klassvärde större än bolagsvärde. Före utfallen återställdes den tidigare granskade nämnarkontrollen enligt den daterade grindändringen; pris,bolagsvärde,kontroller och kapitalformel ändrades inte. Därför98tillägg i sluturvalet,inte preliminära97. En senare rent kosmetisk rättelse av tomma skälceller ändrade inga urval eller resultat; originalfil/hash sparas.',
'Kontrollens shares används bara som konservativ omöjlighetskontroll, inte som estimandets nämnare. Giltiga poster kan därmed ha fallit bort om en ej verifierad shares-override behövts. Samtliga behållna kontrollers klassvärde/bolagsvärde ligger0.306–1.020; små kvoter är huvudsakligen olika aktieslag, inte ett ändrat kapitalmått.',
f'Exakt samma fonder finns i alla4roller per händelse: {int(support.retained_funds.min())}–{int(support.retained_funds.max())}, median{support.retained_funds.median():.0f}. Totalt{v["fund_role_rows"]}fond×händelse×roll-rader. Dubbel fond-ISIN, ändrad fondidentitet/benchmark och tidigare namn-/instrumentambiguitet ärvs från det gamla urvalet; extra kvantitets-/enhetsfel utesluts symmetriskt.',
'Kontrollen hittade fond61031at2020Q4 med0faktiska instrumentrader trots positivt gammalt n_instr. Fonden uteslöts därför från23hela fond×händelsejämförelser, alla4roller. En ytterligare fond×händelse uteslöts på pris-/enhetsfel. Den kända mottagarfusionen51437i2022H1 var redan utanför stabila fondpanelen; explicit kontroll kvarstår. Inga saknade rapporter blir noll. Ny ägare betyder0före/positiv efter i full rapport, inte första ägandet någonsin.',
'',
'FORMEL OCH OSÄKERHET',
'delta_q=q1-splitfaktor*q0. Komponentvärde=100*delta_q*gemensam rå FI-kurs1/bolagsvärde1. Nya:q0=0,q1>0; kvarvarande:q0>0,q1>0; utträde:q0>0,q1=0. Alla fonder summeras inom roll, sedan händelse minus medelc1,c2,c3. Händelser väger lika inom översyn och14översyner väger lika. Standardfel och t13-intervall beräknas på reviewmedel. component_covariance.csv visar full kovarians för delarna.',
'Gruppernas tabeller är additiv beskrivning. summary.csv behåller även stödintervall för transparens; endast is_primary=True är primär kontrast. Inga p-värden, klassificeringssökningar, kontrollersättningar eller leave-company-out-tester har gjorts. De69bolagens bidrag redovisas fullständigt i all_company_contributions.csv, utan vald utelämningsvariant.',
'',
'KONTROLLRÄKNING OCH RÅKÄLLOR',
f'{v["prior_event_quantity_checks"]}händelse×fond-par stämmer exakt med den tidigare enhetsvaliderade kvartalsledgern; råkvantitetsfel={v["max_prior_event_quantity_error"]:.1f}, kapitalfel={v["max_prior_event_pp_error"]:.1f}. {v["raw_ownership_status_checks"]}positiv-/noll-statuskontroller mot FI-långfilen passerar.',
f'En separat kodväg summerar råa antal per komponent FÖRE värdering och reproducerar{iv["event_component_rows_checked"]}händelse×grupp-rader, största skillnad{max(iv["max_event_component_error_pp"].values()):.2g}procentenheter. Primär standardavvikelse för medlet{iv["primary_SE_reproduced_from_joint_covariance"]:.8f}återskapas ur gemensam kovarians. Detta är oberoende aritmetik/kodväg, inte separat datainsamling.',
f'Direkt XML-kontroll av{raw["raw_reports"]}fullrapporter för två fasta fonder över alla{raw["distinct_control_security_quarters"]}behållna kontrollaktie×review-par reproducerar{raw["endpoints"]}endpoints, inklusive{raw["zero_endpoints"]}nollor, med0kvantitetsfel. raw_control_report_map.csv pekar ut ZIP och XML-medlem/hash. Råinmatningskartans filer och roller finns i raw_input_map.csv.',
'',
'BEGRÄNSNINGAR OCH BIDRAGETS NIVÅ',
'Kvartalets nettopositioner är inte faktiska börsorder, bruttoköp eller handel på indexdagen. Fondflöden, aktiva omplaceringar, nyemissioner, transfereringar och mellanliggande rundresor ingår. Ett aktieslag/depåbevis mäts relativt hela bolagets kapital; byte till ett annat aktieslag kan ändra måttet utan ändrad total bolagsexponering. Slutkurs/nämnare kan vara endogena. FI-fonder är inte hela investerarmarknaden, och samma fondbolag kan ha flera beslutsfattare. Kontrollerna är matchade, inte slumpmässiga; några är redan indexmedlemmar och frånvaro i medlemskedjan bevisar inte icke-medlemskap.',
'Färre jämförelser och extra supportkrav innebär att kapitaltabellen inte kan klistras ihop med det gamla219-eventresultatet utan samma-urvalstabellen. Små14kluster och potentiellt beroende mellan översyner begränsar intervallen. Resultaten är explorativa efter många äldre analyser och intervallen är inte korrigerade för hela forskningsprocessens val.',
'För en struktur kring mätning och konsekvenser är det användbara steget: färre/fler fondnamn säger inte hur mycket exponering som ändras; den nya bokföringen visar både vem som börjar äga och hur stora deras observerade nettopositioner är. Detta kan stärka ett avgränsat svenskt empiriskt bidrag. Det identifierar inte orsaken till prisreaktionen och lovar ingen uppsatsvinst.',
'',
'LITTERATURGRÄNS (parallellt verifierade läspass, inte ny fulltextgranskning här)',
'Pavlova–Sikorskaya2022, §4.1/Table5: https://www.sikorskaya.net/files/Pavlova_and_Sikorskaya_2022.pdf',
'Philippe van der Beck, Flow-Driven ESG Returns, Nov2022, tryckta s30–31/AppendixB.3s61: https://memento.epfl.ch/public/upload/files/VanderBeckPaper.pdf . Nollpositionsinträden/utträden kontra kvarvarande positioner är en tidigare använd uppdelning.',
'',
'TID, FEL OCH REPLAY',
'Initial design14:08:36UTC; kapital-/kontrollgrindens avgränsning14:12:58; rapportstödskorrigering14:16:07 efter avbruten råavstämning men före aggregat. Slutlig primär låsning14:16:48UTC; första färdiga ekonomiska aggregat14:16:59. Separat aritmetik klar14:21:02. Efter kända primärutfall låstes same-support-count/bolagsbokföring14:21:41. Inget av detta kallas blind förregistrering.',
'failed_first_run.log och first_run_lock.json bevarar rapportgrindsfelet. failed_verifier_id_parse.log bevarar en separat granskningskod som först läste sträng-ID som flyttal; rättad typning ändrade inga huvudresultat. run_before_ledger_export.py är originalkod vid huvudlåset; run.py lägger endast till fond-ID/ledgerexport och bevarar låset på replay. Varken rådata, repo, uppsatstext eller FTN-utfall har ändrats/öppnats. AI-ändamål och datum dokumenteras här; repoägaren måste föra den ordinarie AI-loggen.',
'',
'Kör lokalt: python gate.py; python run.py; python verify.py; python raw_control_check.py; python descriptive.py; python write_report.py. requirements.txt anger miljön. FINANCETHESIS_REPO stöds i huvudskripten; hjälpskripten har den dokumenterade lokala reposökvägen. Kopiera inte .venv, rå LSEG-data eller FI-arkiv i en publik leverans. Normaliserade härledda tabeller och skript ligger här; licensvillkor gäller fortfarande för underliggande LSEG-källa.',
]
(O/'REPORT.txt').write_text('\n'.join(lines)+'\n')
# Explicit dependency map: inherited intermediates are not passed off as newly re-extracted raw data.
entries=[
 ('FI raw original reports','data/raw/fi/Fondinnehav_*.zip','Public regulator source; dated2019Q1–2025Q4 full XML; exact direct-check members in raw_control_report_map.csv','Antal,ISIN,Valuta,Marknadsvärde,Fond_institutnummer,Kvartalsslut','Original source; no full raw archive copied'),
 ('FI standardized positions','data/derived/fi/fi_holdings_long.csv.gz','Inherited canonical long file; earlier repository raw audit plus new control XML checks','Raw reported quantities; common after-price from SEK value/quantity consensus','Read only; raw fund portfolios not copied'),
 ('LSEG company capitalization','data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet','Inherited historical panel,source=tr; same TR.CompanyMarketCap measure as prior validated quantity work','ric,date,close,mcap,shares,source; no returns/volume used','Licensed; raw prices/market caps not delivered'),
 ('Historical security identities','output/omxsb_mechanism_frontier_20261102/ownership/security_role_gate.csv','Previously Nasdaq-backed class identity/alias mapping; fixedthreecontrols','event_id,review,role,ric,aliases,q0,q1,source_url','Derived input'),
 ('Stable report/fund support','output/omxsb_mechanism_frontier_20261102/ownership/decomp_fund_roles.csv.gz','Prior quality-screened stable fund ID/ISIN/benchmark ledger','event_id,role,fund_id,group,own_before,own_after','Derived input; not sufficient alone for full-report proof'),
 ('Fund benchmark and company metadata','output/omxsb_mechanism_frontier_20261102/ownership/decomp_fund_groups.csv','Prior pre-quarter benchmark grouping and legal company name','review,fund_id,group,company,q0,q1','Derived input; no active/passive reclassification'),
 ('Raw full report metadata','output/omxsb_open_questions_20261102/demand_quarter/raw_fund_report_metadata.csv','Earlier raw-derived actual instrument count; used directly to exclude empty reports','Fond_institutnummer,Kvartalsslut,actual_instrument_rows','Derived support input'),
 ('Prior event quantity gate','output/omxsb_open_questions_20261102/demand_quarter/events_locked.csv','Previously validated216eventquarterunits','event_id,RIC,review_cycle,factor','Derived inherited event gate'),
 ('Canonical event capitalization','output/omxsb_open_questions_20261102/demand/denominator_audit.csv','Prior event rawFIprice/companymcap/classcapital audit','fi_price,mcap,class_value_fraction','Derived event audit; exact reproduction asserted'),
 ('Prior event quantities','output/omxsb_open_questions_20261102/demand_quarter/fund_event_quarter_changes.csv.gz','Previously validated rawFIevent quantities','before_quantity,after_quantity,delta_company_pp','Validation only; new controls rebuilt separately'),
 ('Dated corporate-action evidence','output/omxsb_extension_20261031/ownership/corporate_action_sources.csv','Primary issuer/Nasdaq sources retained in source column','RIC,action_date,factor,kind,source','No new factor inferred from price ratio'),
 ('Original XML member locator','output/omxsb_audit_20261031/fi_raw_report_inventory.csv','Previous envelope audit selects latest reported fund-quarter XML','zip,file,fund,quarter,published_file,n_instruments','Source map; direct XML reading in newrawcheck'),
 ('Previous ownership event gate','output/omxsb_mechanism_frontier_20261102/ownership/decomp_coverage.csv','Earlier219common support comparisonIDs','event_id,kept','No rematch'),
]
rows=[]
for label,rel,role,fields,license_note in entries:
 p=R/rel;rows.append(dict(input=label,absolute_path=str(p),purpose_and_provenance=role,fields=fields,distribution_note=license_note,sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'see raw_archive_hashes.csv'))
pd.DataFrame(rows).to_csv(O/'raw_input_map.csv',index=False)
rawmap=pd.read_csv(O/'raw_control_report_map.csv');pd.DataFrame([dict(path=p,sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for p in sorted(rawmap.raw_zip.unique())]).to_csv(O/'raw_archive_hashes.csv',index=False)
files=[p for p in O.iterdir() if p.is_file() and p.name!='OUTPUT_SHA256.json'];(O/'OUTPUT_SHA256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2))
print('REPORT.txt,raw_input_map.csv,raw_archive_hashes.csv,OUTPUT_SHA256.json written')
