"""Generate the Swedish decision memo, gap ledger and reproducible run instructions."""
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'output/omxsb_audit_20261031'
r=pd.read_csv(A/'result_table.csv')
def result(question,typ,period='2022–2026',window=None):
    z=r[r.question.eq(question)&r.type.eq(typ)&r.period.eq(period)]
    if window:z=z[z.window.eq(window)]
    t=z.iloc[0]
    return f"{t.estimate:.2f} [{t.ci_low:.2f}; {t.ci_high:.2f}], N={int(t.N)}, G={int(t.independent_reviews)}"

gaps=[]
def gap(cat,var,period,source,access,license,sample,blocks,action):
    gaps.append(dict(category=cat,variable=var,period=period,source=source,access_verified=access,
                     license=license,actual_sample=sample,blocked_test=blocks,next_action=action))
gap('A','Dagliga totalavkastningar, OMXSBGI, stängningskurser, volym, bid/ask, shares och mcap','event 2007H2–2026H1; panelens faktiska datum 1991-11-01–2026-10-26',
    'data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet; indices_daily (1).csv','Läsbart, LFS-SHA stämmer; 4 340 104 rader, 1 928 RIC','LSEG; befintlig lokal licensdata, ingen ny distributionsrätt verifierad','hela filen läst',
    'Inget hinder för marknadsjusterad huvudreplikation; tvärsnitt/universum och variabelhistorik är ofullständiga','Använd parquet; csv.gz har verifierat CRC-fel')
gap('A','FI-fondinnehav och rapportmetadata','2018Q4–2026Q2','data/raw/fi/*.zip; data/derived/fi/fi_holdings_long.csv.gz',
    '31 zipfiler; 20 630 XML lästa; 3 064 860 innehavsrader avstämda; 886 fonder med innehav','Offentliga FI-rapporter; ingen vidare licensbedömning','hela lokala historiken läst',
    'Täcker svenska värdepappersfonder, inte alla institutioner','Använd rapportinventeringen inklusive tomma rapporter; håll saknat och noll isär')
gap('A','Annonseringsdatum, effektiva datum, förändringslistor, ankarlista 2009 och tracker-AUM','39 översyner 2007–2026',
    'data/input/omxsb/','Filer lästa; 536 förändringar; tracker_aum.csv finns','Sammanställda offentliga uppgifter; underliggande källor per rad','lokala filer',
    'Listor är inte komplett datumgiltigt medlemskap eller säkert realtidsuniversum','Behåll källstatus och separera beskedsdatum från första handelsreaktion')
gap('A','Instrumentlista, bransch/supersektor, listade aktier och 12-månadersomsättning','februari 2020; publicerad 2020-03-23 13:08:10 CET',
    'https://attachment.news.eu.nasdaq.com/a8cb43b3dac4a07770fd3957b8858b42a','XLS hämtad och blad läst; 387 Stockholm-instrument','Publik fil; historisk produktlicens och vidareanvändning inte utredda','nasdaq_202002.xls',
    'Verifierar formatet, inte oktoberpiloter eller full kandidatpopulation','Stock-filter räcker inte: tio preferensnamn märkta Stock; free float saknas')
gap('B','Föregående månad och föregående tolv hela månader','alla 487 händelser',
    'notebook cell 24 och mechanisms E1','rättat och omkört','intern kod','before/after-exporter','Framtida handel i förklaringsvariabel','AD.to_period(M)-1; volatilitet från ym_pre−11 till ym_pre')
gap('B','Samstämmig estimand och osäkerhet; ägaridentitet på samma urval','253 händelser 2019–2026, 15 översyner',
    'omxsb_audit_helpers.py; ownership_common_sample.csv','rättat och omkört','intern kod','event_fund_reporting.csv.gz','Felaktiga E5b-standardfel och medianbokföring','Årsmedianer med översynsbootstrap inom år; additiva medel separat')
gap('B','Fondernas rapportnärvaro och rapporterat jämförelseindex vid kvartalsslut','2018Q4–2026Q2',
    'fi_raw_report_inventory.csv; tracker_quarter_metadata.csv','konstruerat, men mandattext bevisar inte indexreplikering','FI','hela historiken av rapportmetadata',
    'Tidskonstant handelsklassificering får inte likställas med historiskt tracker-mandat','Granska övergångar och tomma rapporter; separera ex post-klassificering från mandat')
gap('B','CAPM-residualvarians och skattad marknadsmodell','2007–2026 där skattningsfönster finns',
    'befintliga aktie- och marknadsavkastningar','kan konstrueras; inte körd i granskningen','LSEG lokalt','avkastningsdata verifierade',
    'WZ-liknande kontroll och marknadsmodellrobusthet; inte huvudreplikationen','Förbestäm skattningsfönster och minsta täckning före körning')
gap('B','Tre använda splitfaktorer','Lagercrantz okt 2020, Addnode maj 2022, Heba maj 2022',
    'split_source_verification.csv','3:1, 4:1, 2:1 bekräftade mot emittenter','Offentliga emittentmeddelanden','primärkällornas text läst',
    'Dessa tre faktorer stämmer; detta verifierar inte alla historiska justeringar','Länka datum och aktieslag; särskilj faktorverifiering från full ISIN-validering')
gap('B','Pilotmål och lokal pristäckning','oktoberreferenser 2019 och 2024',
    'candidate_pilot_targets.csv; OMXSB-listor','29 förändringar, två översyner; 27 efter huvudurvalets filter','lokala data','målrader, ingen officiell oktoberkandidatfil',
    'Kan kontrollera pipeline, inte skatta ett trovärdigt pilotavkastningstest','Hämta oktoberfiler innan kandidatmatchning; inga nya avkastningstest i piloten')
gap('C','Fullständigt historiskt kandidatuniversum och historiska instrumenttyper','oktober 2019 och oktober 2024 först; därefter referensmånader 2007–2026',
    'Nasdaq Equity Trading by Company and Instrument; OMXSPI-historik','okänd för målmånaderna; arkivsida gav timeout/anslutningsfel','Publik månadsfil möjlig; komplett arkiv/licens okänd','februari 2020 ja; oktober 2019/2024 nej',
    'Urvalsjusterad förbeskedsanalys och ärlig realtidsprognos','Begär eller hämta exakt två oktoberfiler; kontrollera publiceringstid och avlistade instrument')
gap('C','Datumgiltiga OMXSB/OMXSPI-medlemmar, corporate-action-inträden och fem saknade översyner','jan 2005–jan 2007 samt mellan översyner 2007–2026',
    'Nasdaq index notices, corporate-action notices, historiska constituent-filer','delvis; full historik okänd','Historiska indexprodukter kan vara licensierade; tillgång okänd','2009-06-01 ankarlista och förändringar ja; komplett historik nej',
    'Historiskt icke-medlemsuniversum, indexkapitalisering och exakta transitionskedjor','Verifiera Nokia, Loomis och sex rapporterade kedjebrott; fyll inte med bakåtblickande antaganden')
gap('C','Officiell Nasdaq-omsättning över tolv månader samt historiskt ICB','samma referensdatum, pilot oktober 2019/2024',
    'Nasdaq instrumentstatistik, historiska ICB-versioner','feb 2020 fält verifierade; övriga datum okända','Nasdaq/FTSE ICB-villkor; historisk åtkomst okänd','ett februari-XLS ja',
    'Exakt regelrekonstruktion; sex månader close×volume är en annan variabel','Behåll officiella SEK-definitioner och historiska branschklassificeringar')
gap('C','Free-float-faktor och free-float-kapitalisering per giltighetsdatum','pilot oktober 2019/2024; därefter 2007–2026',
    'Nasdaq indexfiler eller LSEG historisk free float','okänd; saknas i verifierad Nasdaq-provfil','Sannolikt index-/dataleverantörslicens; lokal behörighet ej verifierad','nej',
    '85%-urval inom supersektor och korrekt mekanisk efterfrågan/indexvikt','Begär daterat prov på 10–20 pilotinstrument och publiceringstid')
gap('C','Historisk instrumentkedja: ISIN, aktieslag, datum, split-/inlösen-/BTA-faktorer','2007–2026; särskilt 259 FI-händelser 2019–2026',
    'Nasdaq/emittentnotiser; LSEG historiska instrumentidentiteter','statisk matchning och namnförslag finns; full giltighet okänd','Offentliga notiser; LSEG historik beror på licens','tre splitkällor ja; full korsreferens nej',
    'Exakta fondkvantiteter och jämförbara aktieslagsnämnare','Granska 11 namnflaggor och BTA-länkar; dagens ISIN är inte ett historiskt facit')
gap('C','Fondöverlåtelser, fusioner, upplösningar och fullständigt datumgiltigt tracker-mandat','2018Q4–2026Q2 och tidigare trackers 2007–2018',
    'FI-fondregister, fondårsberättelser, kundbrev och fondbolagsnotiser','kvartalsmetadata finns; full händelsehistorik okänd','Offentliga fondrapporter; eventuell Morningstar-licens ej verifierad','LF-byte 16 juni 2025 ja; två ISIN/ID-konflikter lokalt',
    'Skilja handel från fondöverföring och korrekt OMXSB-tied passive demand','Granska rapportinträden/utträden och fond-ID; benchmark är inte ensamt mandatbevis')
gap('C','Ägargrupper utanför svenska värdepappersfonder: utländska fonder, direkta pensioner, försäkring, hushåll, övriga institutioner','eventkvartal 2019–2026; lång historik 2007–2018',
    'Euroclear/ägarregister, Morningstar eller annan ägardatabas, förvaltarrapporter','FI täcker inte komplett ägarpopulation; AP1–AP4-filer tillkom parallellt i data/raw/ap och är inte verifierade i denna audit','Ofta licens; behörighet och omfattning okända','AP-filer finns nu lokalt men innehåll/historik är inte granskat; inget verifierat heltäckande ägarprov',
    'Full marknadsbalans och identifiering av vem som absorberar efterfrågan','Begär prov med aktieslag, datum och ägarkategori; residualen får inte döpas till utländska ägare')
gap('C','Justerade emissioner, återköp, inlösen, optionsinlösen, ersättningsaktier, konverteringar och treasury shares','händelsekvartal 2007–2026',
    'Emittenternas kapitalförändringsnotiser/årsrapporter; LSEG corporate actions','aktieantal finns; full klassificering och justeringshistorik okända','Offentlig bolagsdata eller LSEG-licens','tre splits ja; komplett utbudshistorik nej',
    'Sammon–Shim-utbudstest och kausal tolkning av ändrat aktieantal','Bygg aktieslagsbalans före aggregering till bolag; ett aktieantalssteg är inte automatiskt en emission')
gap('C','Historiska korta nettopositioner med LEI/ISIN och rapporteringströskel','2012–2026 möjlig registerperiod; 2007–2011 ej täckt av verifierad källa',
    'https://www.fi.se/sv/vara-register/blankningsregistret/','webbsidan läst; historisk bulkfil och full periodtäckning ej verifierade','Publikt register; exportåtkomst okänd','registersida ja, historisk datafil nej',
    'Blankningskanal; inte total marknadsblankning','Publik namngiven historik är tröskelbegränsad (0,5%); noll offentlig position är inte noll blankning')
gap('C','Motsatta faktiska indexövergångar och trackerflöde på båda sidor','2007–2026, datum för varje övergång',
    'Nasdaq/andra indexleverantörer och berörda fonders daterade mandat/AUM','okänd; noll verifierade migrationshändelser i paketet','Indexhistoria/AUM kan kräva licens','OMXS30-förändringslista ja; motsatt övergång med två trackers nej',
    'G&S-migrationstest','Kräv utträde ur index A och inträde i B samt relevant trackerexponering; överlapp räcker inte')
gap('C','Effektiva spreadar, intradagsorder och implementation shortfall','2007–2026 eller förbestämd delperiod',
    'Nasdaq tickdata/LSEG Tick History; mäklar- eller exekveringsdata','okänd','Marknadsdata-/mäklarlicens krävs sannolikt','nej, endast closing bid/ask lokalt',
    'Exakt G&S-likviditetsreplikation och faktisk exekveringskostnad','Begär prov på två översyner och kontrollera quote-/trade-tidsstämplar')
gap('C','Svenska dagliga faktorer och analytikertäckning','2007–2026',
    'SHoF/SweFin factors; LSEG I/B/E/S historisk täckning','factors_daily.csv saknas lokalt; extern åtkomst okänd','Kontrollera faktorvillkor respektive I/B/E/S-licens','nej',
    'Kompletterande faktormodell och full senare G&S-kontrolluppsättning; hindrar inte beta-ett-replikationen','Hämta först om vald robusthet behöver dem; SHoF Valuations/Reinvestments behövs inte här och har inte kontrollerats')
pd.DataFrame(gaps).to_csv(A/'data_gaps.csv',index=False)
(A/'DATALUCKOR.md').write_text('# Dataluckor och verifierad tillgång\n\nA = finns och läst. B = konstruerbart/rättat med lokala data. C = extern källa eller ännu overifierad tillgång. '
    'Frånvaro i FI är inte frånvaro på marknaden. Provfil betyder faktisk läsning, inte en manifestpost.\n\n'+pd.DataFrame(gaps).to_markdown(index=False)+'\n')

report=f'''# OMXSB granskningsrapport 31 oktober 2026

Analys- och kodunderlag, inte uppsatstext. **Huvudavkastningarna reproduceras. Underlaget visar en mindre indexeffekt än i början av perioden, men avgör inte varför. Det stöder varken att effekten säkert är noll i dag eller att förhandspositionering eller en viss säljargrupp har identifierats.**

## Version och vad som faktiskt körts

Lokal HEAD och kontrollerad `origin HEAD`: `b886f5b744f797a6c1252f0e41fe2b740591c8c3`. Arbetskopian var ren vid start. Ändringarna i detta granskningspaket är lokala och inte publicerade. Originalexporter och originalkod är frysta under `original/`, med SHA256 i `original_sha256.json`. Den befintliga katalogen `output/omxsb_replication_2007/` är lämnad orörd. Under arbetet tillkom separat `collect_ap_fi_20261031.py`, `parse_ap_20261031.py` och `data/raw/ap/` med AP1–AP4-mappar. De har inte skapats, ändrats eller analyserats här; deras variabler och historik är ännu overifierade i detta underlag.

Alla notebookens kodceller samt mekanismskriptet, periodkänsligheten och trendtesten har körts från läsbara indata, både med fryst originalkod (`baseline/`) och rättad kod (`corrected/`). Körloggar och `run_complete.json` dokumenterar detta. Köraren exekverar notebookcellerna i ordning utan Jupyter-kernel och omdirigerar bara exportvägarna. Befintliga 2013–2026-exporter används enbart till den äldre jämförelsen. Den separata `deletions_clean_table.py` har lästs och dess regler jämförts; dess äldre exporter är inte märkta som omkörda. Ingen FTN-avkastning har beräknats.

Efter sortering på händelsenyckel stämmer 56 av 64 jämförbara CSV-exporter numeriskt och textuellt. I återstående åtta skiljer endast bootstrap-p-värden: högst 0,0001 i huvudtabellen, men upp till 0,1684 i ettårstabeller med mycket få översyner. Orsaken är strikt flyttalsjämförelse av teoretiskt lika teststatistikor, inte ändrade avkastningar eller andra slumpfrön. Osorterade mängder gav dessutom olika radordning i rang- och medlemsfiler, men samma nyckelkopplade data. `baseline_comparison.csv` och detaljfilen visar varje avvikelse. Den rättade bootstrapen räknar numeriska likheter som likheter och har kontrollerats för skalinvarians.

Parquetfilen har 4 340 104 lästa rader och 1 928 RIC, utan duplicerade RIC-datum; dess SHA motsvarar LFS-objektet. Det är inte samma sak som 2 117 rader i statiktabellen eller ett komplett historiskt börsuniversum. Den parallella gzipfilens LFS-hash stämmer också, **men själva gzipinnehållet har CRC-fel**. FI-filen är läsbar: 3 064 860 rader, 886 fonder med innehav, 31 kvartal 2018Q4–2026Q2. Alla 20 630 rå-XML har parsats och senaste rapporters radantal stämmer exakt mot den härledda filen. 1 306 senaste rapporter har inga instrument; dessa verifieras inte därmed som ekonomiska nollinnehav. `input_inventory.csv` skiljer manifest, LFS-pekare, hash och läsbarhet. Rådata har inte ändrats.

## Vad resultaten stödjer

Tabellen nedan använder 95-procentiga intervall med CR1 klustrad på beskedsdatum och t(G−1). G avser oberoende översynsdatum, inte antalet aktier. Fulla enheter, fönster, källfiler och begränsningar per fråga finns i [resultattabellen](RESULTATTABELL.md) och [CSV-filen](result_table.csv).

| Fråga | Inval | Utträden |
|---|---|---|
| Totalfönster AD−1:ED+1, 2007–2011 (%) | {result('Indexeffekt','addition','2007–2011','AD−1:ED+1')} | {result('Indexeffekt','deletion','2007–2011','AD−1:ED+1')} |
| Samma fönster, 2022–2026 (%) | {result('Indexeffekt','addition',window='AD−1:ED+1')} | {result('Indexeffekt','deletion',window='AD−1:ED+1')} |
| Före besked AD−100:AD−1, 2022–2026 (%) | {result('Förbeskedsavkastning','addition',window='AD−100:AD−1')} | {result('Förbeskedsavkastning','deletion',window='AD−100:AD−1')} |
| Före besked AD−20:AD−1, 2022–2026 (%) | {result('Förbeskedsavkastning','addition',window='AD−20:AD−1')} | {result('Förbeskedsavkastning','deletion',window='AD−20:AD−1')} |
| Andel 45-dagarsvolym på ED−1, 2022–2026 (%) | {result('Volymkoncentration','addition',window='ED−1 / ED±22')} | {result('Volymkoncentration','deletion',window='ED−1 / ED±22')} |

536 källhändelser blir 505 med tillräcklig pristäckning och 487 efter befintligt noterings-/avnoteringsfilter. 481 har komplett totalfönster: 256 inval och 225 utträden, vardera 38 översyner och tillsammans 39. Perioderna omfattar 10/10/10/9 källöversyner, men ett visst utfall och händelseslag kan ha färre. Inga händelser har tagits bort på grund av extrema eller obekväma avkastningar.

De sista periodernas totalmedel är +1,50% och −1,52%; båda klusterintervallen omfattar noll och ekonomiskt märkbara effekter. Skillnaden sista minus första period är −7,03 procentenheter för inval och +5,17 för utträden. En direkt gemensamt klustrad jämförelse mellan inval och utträden 2022–2026 ger 3,02 pp [−1,14; 7,18]. Olika separat signifikans är alltså inget skillnadstest. Totalfönstrets längd ändras dessutom med beskedsregimen; de fasta AD- och ED-fönstren visas separat. De befintliga brott- och trendtesten är reproducerade, men granskningen använder inte valet mellan deras specifikationer för att hitta signifikans.

Den stora AD−100-avkastningen kvarstår, medan AD−20 är betydligt osäkrare. Detta är förenligt med flera förklaringar: urval efter omsättning/storlek, tidigare bolagsnyheter, momentum och förhandspositionering. Rangmåtten löser inte frågan: de använder ett efterhandsselekterat LSEG-universum och sex månaders pris×volym i stället för officiell tolvmånadersomsättning. Ett starkt långfönster är därför ingen identifierad anticiperingseffekt.

Kompositionskontrollen förklarar inte bort tidsförändringen i den körda proxy-modellen. På samma kompletta urval är sista-minus-första −7,60 pp utan och −7,90 med kontroller för inval; +5,45 respektive +5,02 för utträden. Senaste periodens effekt vid typens genomsnittliga kontroller är +1,24 och −1,39%. Detta är inte den fulla senare G&S-modellen: medlemskap och kapitalisering är approximationer, volatilitet ersätter deras residualrisk och analytikertäckning saknas. Ocentrerade periodkoefficienter beskriver nollvärden på kontrollerna och får inte läsas som genomsnittliga effekter.

Den rekonstruerade medlemsportföljens värdeviktade slutnoterade relativa spread faller från 0,270% år 2007 till 0,079% år 2025. Detta är en deskriptiv proxy, inte effektiv spread eller implementation shortfall. Vikter påverkas av bolags-/aktieslagsnivå och medlemskedjan. Ökad volymkoncentration på ED−1 visar när handeln sker, inte dess riktning, motpart eller kostnad. Samband mellan årsmedelspread och eventavkastning bevisar ingen likviditetsmekanism.

## Bekräftade rättelser och deras effekt

| Rättelse | Före | Efter och slutsats |
|---|---|---|
| Föregående månad | Alla 487 händelser fick annonseringsmånaden genom `AD−MonthBegin(1)` | `AD.to_period('M')−1` i notebook och byggskript. Volatilitetens kodintervall blir ym_pre−11:ym_pre för att bevara samma tolv historiska månader. Volatilitet, CAR och förbeskeds-CAR är oförändrade. |
| Komposition efter datumrättelsen | Centrerad sista-periodkoefficient +1,534 / −1,299 | +1,237 / −1,390; tidsförändringen kvarstår. Rangmåttet i notebooken får också rätt referensmånad. |
| E5b osäkerhet | Medel av årsmedianer kombinerades med poolat medelvärdes SE/p | Samma medel av årsmedianer med bootstrap av hela översyner inom år; poolade medel och deras CR1 redovisas separat. Inga gamla p-värden återanvänds. |
| Rapporteringsinträde/utträde | Hela fonders rapportbortfall kunde bli handel | Jämför samma fonder med icke-tom rapport i båda kvartalen. 131 event ändras i alla/övriga FI, inget i tracker-nettot. Fullständig portföljöverföringshistorik saknas fortfarande. |
| Bootstrap och N | Strikta flyttalsties; F-rad räknade även saknade utfall | Stabil tie-hantering; N räknar giltiga utfall. Huvudskattningar ändras inte. |
| Täckningsetiketter | Deduplicerade bolag dividerades med antal medlemsaktieslag; spreadkolumnen sade medlemmar men räknade panelaktier | Samma enhet i täckningskvoten och korrekt panelkolumnnamn; kapitaliseringssumman och avkastningar ändras inte. |

Efter rapportparning är gemensamma poolade medel (% av efterkvartalets LSEG-aktier) tracker/övriga/alla FI **1,031 + 0,225 = 1,257** vid inval och **−1,030 − 0,125 = −1,155** vid utträden, med N=137/116 och G=15. Före parning var övriga FI +0,212/−0,185. Identiteten stämmer per event med maximalt avrundningsfel under 10⁻¹⁵. Årsmedianerna blir tracker/alla/övriga +1,052/+1,126/+0,151 respektive −1,048/−1,058/−0,049; **dessa medianer ska inte summeras**. Bootstrapintervallen har begränsat stöd eftersom de betingar på åtta observerade år med en eller två översyner per år. Varken medlen eller medianerna identifierar enskilda affärers motparter.

## Kvarstående mätfrågor

Fondgrupperna är ex post-handelsklassificerade, inte verifierade OMXSB-mandat under hela perioden. FI-metadata visar att LF Sverige var OMXSB-relaterad före bytet 2022, hade Morningstar under mellanperioden och återgick till Custom OMXSB 2025. Det senare bytet den 16 juni 2025 bekräftas i [fondbolagets halvårsredogörelse, tryckt sida 153](https://mb.cision.com/Main/152/4222567/3624909.pdf). En äldre notis om att LF aldrig följde OMXSB före 2025 är alltså för grov. Nordnet byter rapporterad benchmark från SBX till ESG-variant mellan 2022Q1 och Q2. Rapporterade benchmarktexter och två möjliga ISIN/fond-ID-konflikter finns i paketet; de är granskningsflaggor, inte automatiskt bekräftade överlåtelser.

Tre splitfaktorer (Lagercrantz 3, Addnode 4, Heba 2) stämmer mot emittentkällor i `split_source_verification.csv`. Det verifierar inte alla namnmatchningar: 11 event har namn-/aktieslagsflaggor och flera alias avser BTA eller inlöseninstrument. 28 FI-pris/mcap-per-aktie-avvikelser finns; flera förklaras av att mcap är bolagsvärde medan shares avser aktieslag, så dessa flaggor är **inte** ett exklusionsurval. För Volvo, SSAB och Atlas Copco är A/B-mcap identiska under samtliga 5 610 jämförda dagar och aktieantalen skiljer sig. Mekanismskriptet deduplicerar redan kapitalisering med en RIC-stamheuristik; notebookens top-100-proxy gör det inte. Full historisk issuer-/aktieslagslänk behövs innan samtliga storleksmått och utbudsbalanser kan betraktas som verifierade.

Medlemskedjan saknar fem tidiga översyner och dokumenterade inträden mellan ordinarie översyner. Sex kedjebrott rapporteras; ett uteblivet inträde får inte uppfinnas. Avnoteringsfiltret använder 100 kalenderdagar i notebooken och mekanismflaggningen 100 handelsdagar. Det separata skälsbaserade filtret flaggar 20 utträden, mekanismskriptet 19; de skiljer sig i nio event. Africa Oil 2018H1 saknar rad i skälsfilen. Alla finns kvar i huvudanalysen. Ändrade aktieantal är granskningssignaler, inte verifierade emissioner/återköp.

## Fem kodavsnitt och fyra breda G&S-förklaringar

| G&S-fråga | Kod | Replikationsstatus |
|---|---|---|
| Sammansättning | E1 | Svensk proxy-regression; datumfel rättat. Senare G&S har centrerade kontroller, residualrisk och analytikertäckning. |
| Migration | E3 | **Ej replikerad.** OMXS30-överlapp är inte en motsatt indexövergång; noll verifierade migrationspar med berörda trackers. Detta säger inget om huruvida sådana data finns på marknaden. |
| Förutsägbarhet/förhandspositionering | E4 | Avkastningsfönstren följer äldre G&S-konventioner. Kandidatrang är en ersättningsvariabel; efterfönstret har annan förankring än äldre figur. |
| Likviditet | E2 och E5 | E2 ersätter effektiv spread med slutnoterad spread; shortfall saknas. E5a replikerar volymandelens beräkning. E5b ersätter 13F-institutioner med FI-fonder och har nu samstämmig inferens. |

Kartläggningen gäller versionsskillnaderna dokumenterade i [författarnas HBS-arbetsartikel](https://www.hbs.edu/ris/Publication%20Files/23-025_563e45c6-df92-4d9c-ae05-608d4d0acab1.pdf). JF-publiceringen är verifierad via [Harvards post](https://dash.harvard.edu/entities/publication/2cc676bd-c8da-40e7-b112-3ecc8644e687); fulltextsfilen gav HTTP 429 i denna granskning. Därför används inte formuleringen ”exakt JF-replikation” för hela paketet. Avkastningarna är marknadsjusterade med beta ett. En skattad marknadsmodell är en möjlig robusthet, inte ett krav för ankarmetoden. Prisreaktion/nettohandel och dess invers är deskriptiva kvoter här, inte kausala elasticiteter.

## Datagrind och rangordning av högst två fördjupningar

Nasdaq-provet för februari 2020 är läst: 387 Stockholm-instrument, 384 märkta Stock, varav tio preferensnamn. Endast 256 instrument matchar någon statisk LSEG-ISIN, vilket varken bevisar att resten saknar prisdata eller validerar de matchade historiska länkarna. Filen saknar free float. [Publiceringstiden 23 mars](https://view.news.eu.nasdaq.com/view?id=b7a3dee62469c86b8de72dddaef274d3d&lang=en) ligger efter referensmånaden. Oktober 2019/2024-filerna kunde inte hämtas i den avgränsade arkivkontrollen; deras åtkomst är okänd. Pilotmålen är 13 respektive 16 förändringar (6/7 och 9/7 inval/utträden); 11 respektive 16 finns i huvudprisurvalet. Piloten har två översyner och ska kontrollera data, inte avkastningssignifikans.

**1. Urvalsjusterad förbeskedsavkastning.** Ekonomisk fråga: finns en extra prisrörelse före beskedet utöver den rörelse som följer av att index väljer stora och omsatta värdepapper? Närmast G&S:s förutsägbarhetsavsnitt, som också skiljer ex post-kursuppgång från verklig förutsägbarhet. Det tillför en kontrollgrupp som den befintliga replikationen saknar. **Villkorat förstaval**, inte ett redan godkänt avkastningstest: två officiella oktoberfiler, giltigt medlemskap, identifierarlänkar, historisk ICB och ett free-float-prov måste först verifieras. Den lokala långfönsteravkastningen finns för 243 inval och 216 utträden; det användbara matchade antalet är ännu okänt och högst 39 översyner. Begränsa sedan till en förbestämd period och ett huvudfönster, med samtidiga icke-valda kandidater från hela universumet. Urvalströsklar i flera dimensioner, bolagsnyheter och historiska regelbyten gör kausal tolkning svår. Ett nollresultat skulle minska stödet för en extra förbeskedspremie efter observerbar urvalsjustering, inte bevisa att ingen positionerat sig. En retrospektiv kontroll kräver korrekta historiska referensvärden; en prognos kräver dessutom att varje uppgift faktiskt var offentlig före beskedet.

**2. Svenska fonders absorption av trackerflöden på verifierade rapportpar.** Ekonomisk fråga: säljer andra svenska värdepappersfonder systematiskt när datumgiltiga OMXSB-trackers köper, och vice versa? Närmast G&S:s ägarjämförelse och Sammon–Shim, *Who Clears the Market When Passive Investors Trade?* ([RFS-publiceringspost 2026](https://doi.org/10.1093/rfs/hhag032); [läst arbetsversion 2024](https://jhfinance.web.unc.edu/wp-content/uploads/sites/12369/2024/11/Who-Clears-the-Market-When-Passive-Investors-Trade.pdf)). Det finns 259 event med kvartalspar, 253 med användbar nämnare (137/116) och endast 15 oberoende översyner. Datainsatsen börjar med 14 handelsklassificerade fonders mandathistorik, identifierarflaggor, rapportbyten och datumgiltiga aktieslagsnämnare. Slutligt säkert N är ännu okänt. En full svensk Sammon–Shim-replikation kräver dessutom justerat aktieutbud, blankning och ägare utanför FI och är därför inte verifierat genomförbar. Ett nollresultat för svenska fonders nettomotstånd utesluter inte absorption utanför FI, intrakvartalshandel eller låg precision. Kvartalsnetto ger aldrig transaktionsmotpart.

Prioriteringen bygger på obesvarad fråga och identifieringsvärde, inte p-värden. Om kandidatpiloten fallerar kan den avgränsade fondfrågan prioriteras efter mätgranskningen; inget spår är låst nu. Migration rangordnas inte som genomförbar utan faktiska övergångar. [Dataluckelistan](DATALUCKOR.md) separerar A/B/C med variabel, period, källa, licensstatus, prov och hindrat test. Svenska faktorer blockerar bara en kompletterande faktormodell. SHoF Valuations/Reinvestments behövs inte för detta uppdrag och har därför inte kontrollerats.

Reproduktion: [KORNING.md](KORNING.md). Alla filer och deras hash finns i `artifact_inventory.csv`; nya datafiler registreras i `data/MANIFEST.md`. AI-användningen är loggad i `thesis/AI_LOG.md`.
'''
(A/'GRANSKNING.md').write_text(report)

instructions='''# Reproducera OMXSB granskningen

Kör från reporoten på Python 3.14.7 (miljön som användes). `requirements.lock` låser de faktiskt installerade versionerna. Paketen kan installeras i annan Python-version endast om motsvarande versioner stöds. Inga FTN-skript ingår.

```sh
python3 -m venv /tmp/omxsb-audit-venv
/tmp/omxsb-audit-venv/bin/pip install -r output/omxsb_audit_20261031/requirements.lock
git lfs pull
export MPLBACKEND=Agg
export MPLCONFIGDIR=/tmp/omxsb-audit-matplotlib
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_inputs.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_fi_raw.py
/tmp/omxsb-audit-venv/bin/python code/build/test_omxsb_audit.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_run.py baseline --periods
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_run.py corrected --periods
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_candidates.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_results.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_report.py
/tmp/omxsb-audit-venv/bin/python code/build/audit_omxsb_finalize.py
```

`git lfs pull` hämtar objekt men verifierar inte att deras interna format är oskadat. Inputskriptet läser parquet och FI, testar zip/CRC och jämför LFS-hash. CRC-felet i stocks_daily_2005.csv.gz är känt och ska kvarstå som dokumenterat fel; analysen använder parquet. Inputskriptet skriver en status per fil, så läs inventeringen och stoppa analysen om andra nödvändiga indata är oläsbara.

Baseline använder koden och exporterna från den frysta committen b886f5b744f797a6c1252f0e41fe2b740591c8c3. Om snapshoten saknas återskapas den från git-objekten i just den committen, inte från aktuell korrigerad kod. Alla kodceller körs; ingen cachad notebookutdata återanvänds. Endast exportvägarna omdirigeras. Mekanism-, period- och trendskript körs efter notebooken. Originalets filordning från Python-mängder kan variera; jämförelsen sorterar på nyckel. Baseline behåller det ursprungliga bootstrap-tieproblemet av reproduktionsskäl.

`corrected/` är den korrigerade analysen. Äldre exporter i `output/omxsb_replication_2007/` och originalsnapshoten ändras inte. Notebookens gamla inbäddade outputs är rensade för att undvika att de visas som om de hörde till rättad kod; fulla körloggar och nya exporter levereras. Vanlig interaktiv körning av notebooken skriver fortfarande till den äldre standardkatalogen, så använd audit-köraren för bevarad jämförelse.

Nasdaq-provfilen finns i paketet. För oberoende nyhämtning:

```sh
curl -L --fail 'https://attachment.news.eu.nasdaq.com/a8cb43b3dac4a07770fd3957b8858b42a' -o /tmp/nasdaq_202002.xls
shasum -a 256 /tmp/nasdaq_202002.xls
```

Förväntad SHA256: b7cd6b69eae58b19d5ff465dfa0afbaa0fa30da49aa091492b7790eeb753860a. Filen är publicerad 23 mars 2020. Oktoberfilerna ingår inte. `candidate_pilot_targets.csv` listar bara mål för framtida kontroll och kör inga nya avkastningstest.

De tre splitkällorna i split_source_verification.csv och licens-/åtkomststatus i data_gaps.csv är manuellt verifierad dokumentation från 31 oktober 2026. De återskapas inte genom analyskörningen. Full extern historisk datatäckning, fondöverföringar och mandat är uttryckligen inte verifierade.
'''
(A/'KORNING.md').write_text(instructions)
print('report, data gaps and run instructions written')
