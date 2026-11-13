TRE FÄRDIGA TILLÄGGSANALYSER – PORTABEL OMKÖRNING
Datum: 2026-11-02

Omfattning
Endast följande tre redan genomförda analyser ingår:
  mandate_upgrade_20261102
  owner_concentration_stability_20261102
  retention_scaling_feasibility_20261102

Detta är ett tillägg till det befintliga paketet omxsb_followup_20261102.
Inga tidigare kataloger, originalarkiv, lås eller körskript ersätts. Den nya
205-observationsanalysen för volym ingår inte. Inga ekonomiska definitioner,
fönster, urval, fondklasser eller estimatorer har ändrats vid porteringen.

Installation
Kopiera de fyra NYA underkatalogerna från staging/code/build/omxsb_followup_20261102
till motsvarande code/build/omxsb_followup_20261102 i repot:
  additions_20261102 och de tre analysnamnen ovan.
Kopiera samma fyra nya underkataloger från staging/output/omxsb_followup_20261102
till output/omxsb_followup_20261102 i repot. Kopiera inte över befintliga kataloger.
Första paketets code- och output-kataloger samt de ursprungliga datakällorna
måste redan finnas. INPUT_SHA256.json kontrollerar 17 sådana repoindata.

Kör från valfri katalog, efter kopiering:
  python /sökväg/till/repo/code/build/omxsb_followup_20261102/additions_20261102/replay.py --repo /sökväg/till/repo

Alternativt kan --output peka på en separat output/omxsb_followup_20261102
dit samtliga fyra nya output-kataloger först kopierats. Äldre sekundärindata
(mandatkatalog, volymmått och ursprunglig positionsretention) läses ändå från
det valda repots första paket, inte från den separata output-katalogen.

De sex stegen, i ordning
1. mandate_upgrade_20261102/aggregate.py
2. mandate_upgrade_20261102/independent_audit.py
3. owner_concentration_stability_20261102/run.py
4. owner_concentration_stability_20261102/independent_audit.py
5. retention_scaling_feasibility_20261102/relative_retention.py
6. retention_scaling_feasibility_20261102/validate.py

Alla sex är porteringar med endast ändrade sökvägar/importer. Det första
paketets befintliga, main-skyddade Fieller- och oberoende kvotfunktioner
importeras; deras analyser körs inte. Ingen datakälla hämtas via nätet.

Låsta underlag och arkiv
output/omxsb_followup_20261102/additions_20261102/archived_original_work
bevarar samtliga 59 originalfiler från de tre arbetskatalogerna, inklusive
ursprunglig kod, råa PDF-filer, läsanteckningar, beslut, urval och resultat.
Aktiv körbar kod ligger under code; aktiva tabeller och underlag under output.
Originalkod i arkivet är dokumentation, inte en alternativ körväg.

Retention körs från de redan låsta kärnkorgarna och valideringsgrinden.
select_core.py och gate_core.py körs aldrig i denna replay. Deras original
ligger kvar i arkivet. Originalens hashmanifest behålls byte för byte;
portabilitetsadaptern kontrollerar frysta data i den aktiva output-katalogen
och ursprunglig urvalskod i originalarkivet. Den skriver inte om manifesten.

Mandatberäkningen använder den frysta upgraded_fund_review_evidence.csv.
fetch.py finns endast i originalarkivet och ingår inte i omkörningen.
source_manifest.json anger fortfarande HTTP 403 för SPP:s PDF-källor 2018
och 2019: tidigare läsning skedde via webbsökningens indexerade primärkälla,
och dessa PDF-filer finns inte lokalt. Två LF-årsrapporter finns lokalt.
Porteringen ger alltså inte starkare källstöd än det ursprungliga arbetet.

Kontroller och loggar
I den nya output-katalogen additions_20261102 finns:
  ARCHIVE_SHA256.json        alla 59 ursprungliga filer
  LOCK_SHA256.json           18 oföränderliga aktiva beslut/underlag
  INPUT_SHA256.json          17 repoindata och befintliga hjälpfunktioner
  SECONDARY_PATH_EQUIVALENCE.json  fem gamla/nya indatavägar, identiska bytes
  PATH_ONLY.diff och PATH_ONLY_CHANGES.json  varje ändring i de sex skripten
  replay_logs/              separat logg för varje steg
  replay_execution.json     exekveringsstatus
  replay_comparison.json    jämförelse med arkiverade originalresultat
  EXISTING_ARCHIVE_CHECK.json  separat kontroll av det första originalarkivet
  ENVIRONMENT.json          faktiskt använd paketmiljö

Omkörningen stoppar om indatakontrollerna, arkivet eller något lås avviker.
Efter sex steg jämförs alla 14 genererade vetenskapliga CSV-tabeller och tre
oberoende audit-JSON-filer med originalen. CSV-jämförelsen kontrollerar exakt
radordning, kolumner, text och numeriska värden med atol=rtol=1e-10. JSON:s
vetenskapliga fält måste vara exakt lika. Endast input_hashes och repots
absoluta sökväg i källproveniens undantas från vetenskaplig JSON-jämförelse.
Alla indata och lås kontrolleras även efter körningen.

Verifierat stagingresultat
Sex steg passerade. Alla 14 tabeller hade numerisk avvikelse 0; 13 var helt
byteidentiska. Den komprimerade tabellens gzip-huvud ändrades, medan samtliga
dekomprimerade värden var exakt desamma. Tre audit-JSON-filers vetenskapliga
innehåll reproducerades exakt. Alla 59 originalfiler och 18 lås var intakta.
Genererade hashrapporter visar med avsikt de nya kod-/output-sökvägarna.

Tolkning
Detta verifierar portering och reproduktion av befintliga analyser. Det gör
inte fondklassificeringens kontinuitetsantaganden säkra, kvartalsnettoköp till
daglig handel, ägarantal till kapital eller portföljrelativ retention till
observerade nettokapitalflöden. De befintliga rapporternas begränsningar gäller.

Miljö
requirements.txt är en oförändrad kopia av det första paketets versionslista.
Miljön använd vid verifiering: Python i /tmp/omxsb-audit-venv, med versioner
registrerade i ENVIRONMENT.json. Omkörningen kräver ingen internetanslutning.
