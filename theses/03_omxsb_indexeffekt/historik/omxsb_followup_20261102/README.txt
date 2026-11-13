PORTABEL OMKÖRNING AV FYRA REDAN LÅSTA OMXSB-UPPFÖLJNINGAR
2026-11-02

Denna mapp innehåller sparade resultat, originalarkiv, låsta underlag och en kontrollerad replay. Analyskoden ligger i code/build/omxsb_followup_20261102 med samma fyra underkataloger. Anpassningarna ändrar enbart repo-/utdatasökvägar och importer. Inga ekonomiska definitioner, fondgrupper, horisonter, vikter, inferensval eller urval har ändrats.

Kör från repots rot med den Pythonmiljö som har requirements_replay.txt installerad:

python code/build/omxsb_followup_20261102/replay.py

Alternativt, från valfri arbetskatalog:

python /sökväg/till/repot/code/build/omxsb_followup_20261102/replay.py --repo /sökväg/till/repot --output /sökväg/till/repot/output/omxsb_followup_20261102

Alla enskilda skript stödjer också OMXSB_REPO och OMXSB_FOLLOWUP_OUTPUT. Om dessa inte anges härleds repot från kodens placering och output blir repot/output/omxsb_followup_20261102. Outputmappen måste innehålla de medföljande låsta filerna och originalarkivet. Replay ska inte köras mot en tom resultatmapp.

Replayordning
1 comparison_rebuild_20261102/run.py
2 comparison_rebuild_20261102/independent_audit.py
3 volume_measurement_20261102/run.py
4 volume_measurement_20261102/independent_audit.py
5 volume_measurement_20261102/unit_venue_audit/audit.py
6 retention_followup_20261102/quantity.py
7 retention_followup_20261102/validate.py
8 deletion_exposure_20261102/freeze_and_run.py
9 deletion_exposure_20261102/verify_raw.py

Retentionens quantity_gate_frozen.csv och gate_frozen_summary.json återanvänds. Deletionens gate_event_ledger.csv, GATE_PROTOCOL.txt och ANALYSIS_LOCK.json återanvänds. Replay skapar ingen ny deklaration, kör inte om grindspecifikationen och ändrar inte ursprunglig tidsstämpel eller event-ID-lista. Gate-/finalize-skripten finns portabilitetsanpassade i kodmappen för spårbarhet, men ingår INTE i replay. Kör dem inte över denna låsta resultatmapp som del av en reproduktion.

Vad som valideras
Replay kontrollerar först SHA256 för43 befintliga indata-/beroendefiler och för hela originalarkivet. Saknad eller ändrad källa stoppar körningen före nya resultat. Därefter körs nio beräknings-/granskningssteg.22CSV-filer och4JSON-filer jämförs med originalversionerna: samma rader, kolumner, strängar och numeriska resultat inom rtol=atol=1e−10. Den enda avsiktligt ändrade CSV-kolumnen är den fysiska filvägen till Nasdaqs källarbetsbok i unit_venue_audit; filnamn och källhash måste fortfarande stämma. Alla sex lås-/protokollfiler ska vara byte-identiska före/efter.

Vid stagingreplay reproducerades alla26 vetenskapliga resultatfiler;21 av22CSV var dessutom byte-identiska. Den återstående CSV-filens skillnad var enbart flyttad källfilväg. Alla nio steg avslutades utan fel och de89 originalarkivfilerna förblev oförändrade. Ny repo-replay sparar sin faktiska körstatus i replay_execution.json och sin fulla jämförelse i replay_comparison.json. Loggar ligger i replay_logs/.

Källversioner och hashar
archived_original_work/ innehåller en exakt kopia av de ursprungliga fyra work-mapparna, inklusive ursprungliga skript, samtliga låsta ledger, deklarationer, resultat, tidigare försök och hashfiler. Filinnehållet är låst genom ARCHIVE_SHA256.json och filerna är skrivskyddade. Importera eller kör inte arkivskripten: deras historiska absoluta sökvägar har medvetet inte ändrats. Aktiv kod finns endast under code/build.
De aktiva resultatmapparna behåller de ursprungliga låsta ledger/protokollen. Omkörda hash-/valideringsfiler får nya fysiska sökvägar och kodhashar för den portabla versionen; de gamla finns alltid oförändrade i originalarkivet. path_only_code_changes.json redovisar diff och original/portabel kodhash för varje anpassat skript. INPUT_SHA256.json använder repo-relativa källvägar. PORTABILITY_LOG.json och requirements_replay.txt beskriver miljön.

Indata och portabilitetsgräns
Detta är portabelt inom det kompletta lokala repot, inte en fristående datahämtare. De befintliga raw LSEG-panelerna, FI-extrakten, de tidigare OMXSB-analysmapparna och Nasdaqs historiska Excel-filer måste finnas på de repo-relativa platser som anges i INPUT_SHA256.json. Inga nätverksanrop, API-nycklar eller nya datahämtningar behövs. Ett rent Git-klonat repo eller en användarzip som saknar stora/ignorerade datakällor kan därför inte köra hela replay utan att dessa tillförs. Programmet ska då stoppa tydligt, inte fylla saknade data.
Historiska absoluta sökvägar kan finnas i frysta ledger/proveniensfält och originalrapporter. De är bevarade källuppgifter, inte operativa inläsningsberoenden. Aktiv kod innehåller inga användarspecifika /Users-sökvägar eller chat-work-inputs.

Tolkning
Paketeringen ändrar inte slutsatsernas begränsningar. Volym är inte passivt ägande eller komplett handelsplatstäckning. Kvartalsnetto är inte daghandel. Retentionen gäller rapporterad positionsstorlek fram tillED+79–86, inte flödesrensad handel eller observerat innehav tillED100. Avkastning per observerad efterfrågan och deletionsexponeringslutningar är inte automatiskt kausala elasticiteter. Se respektive analysrapport och oberoende audit för fulla gränser.
