SHoF: slutlig käll- och kapitaltäckning, 3 november 2026
Tekniskt arbetsunderlag. Inte uppsatstext eller ett nytt ekonomiskt resultat.

BESKED
Den nya fondhistoriken räcker till en avgränsad grupp fonder, men ännu inte till
en trovärdig huvudslutsats om hur OMXSB-tillägg förändrar hela ägarbasens risk
för samtidiga fonduttag. Jag rekommenderar därför inte att göra detta till
uppsatsens huvudförlängning på det nuvarande underlaget.

Det är ett beslut om denna design och datatäckning, inte ett påstående om att
den ekonomiska frågan saknar intresse eller att de befintliga resultaten faller.
En senare beskrivning av endast den täckta fondgruppen är möjlig om den har ett
eget tydligt syfte. Den löser inte frågan om varför aktiekursen steg.

VAD SOM GJORDES
Efter inloggningen hämtades de saknade SHoF-källorna och granskades på faktisk
värderingsdag, exakt fond/andelsklass, valuta, utdelningsunderlag och avstämning
mellan klasskapital och fondkapital. Totalt 178 fonder rådatagranskades.
Först fem pilotfonder, sedan tio stora kvarvarande luckor och slutligen 163
fonder vars äldre preliminära flaggor behövde kontrolleras. Detta är en riktad
källtäckningsundersökning, inte ett slumpmässigt urval av svenska fonder.

Ingen ny fondavkastning, uppskattat nettoflöde, kovarians, aktierisk eller FTN-
avkastning beräknades. Inga ekonomiska fönster valdes efter deras resultat.
Specifikationerna gjordes efter redan kända ägarresultat; detta är inte en
registrerad blind studie. Ändrade källregler och rättelser finns kvar som historik.

De många mejlen var SHoF:s automatiska leveransbesked för de separata frågorna,
även den fråga som inte gav några rader. Inga personliga mejl skickades. Alla
planerade hämtningar i denna omgång är färdiga.

SLUTLIG TÄCKNING F
Samma fasta 135 händelser (70 tillägg, 65 borttag), tio översyner 2019–2023,
samma tre kontrollaktier och samma fondpopulation vid båda kvartalsändpunkterna.
Åtta celler per händelse: fyra aktier gånger två tidpunkter.

                                         Levererad TRI    Även villkorad NAV
Genomsnittlig celltäckning                    51,71%              55,91%
Täckning viktad med FI-fondkapital             51,34%              54,35%
Händelser med >=50% i alla åtta celler         13/135              30/135
Händelser med >=75% i alla åtta celler          0/135               0/135

Nämnaren är de observerade FI-fondernas innehav i den redan frysta populationen.
Den är inte hela bolagets värde, alla svenska ägare eller utländska investerare.
50/75/90-procentsnivåerna är beskrivande diagnostik, inte styrkekrav eller en
automatiskt godkänd forskningsdesign. 56 äldre godkända fond/översynspar underkändes
vid rådatakontrollen. F använder ingen äldre månadsflagga som reserv.

TÄCKER DET JUST DE NYA ÄGARNA?
Den frågan kontrollerades separat efter F, före några riskutfall. För de 70
tilläggen täcker levererad TRI 29,81% av de nytillkomna bruttopositionerna;
den villkorade NAV-varianten når 49,01%. Här viktas först händelser lika inom
översyn och sedan översyner lika. Positionerna mäts i procentenheter av respektive
bolags värde; detta är inte ett gemensamt mått på kronor eller observerade köp.

Om varje händelses täckningsandel i stället räknas ut först blir medeltäckningen
26,94% respektive 45,10%. Dessa två beräkningssätt besvarar olika viktade frågor.
Kontrollerna redovisas separat; ingen kvot med nettoskillnaden mot kontroller
används som nämnare. De ursprungliga ägarresultaten ändras inte av denna kontroll.

Detta är den viktigaste begränsningen för den tänkta förlängningen: den grupp
vars nytillkomst vi ville studera har sämre täckning än den befintliga ägarbasen.
Det går inte att anta att saknade fonders flödesrisk liknar de observerades.
Okända varianser och samvariationer kan förstärka eller motverka resultatet för
den täckta gruppen. Ett smalt intervall inom gruppen löser inte den luckan.

VAD SOM FORTFARANDE ÄR VILLKORAT
TRI är leverantörens återinvesterade prisserie. NAV-varianten bygger på särskilda
utdelnings-/splitantaganden och är inte certifierad totalavkastning. Nuvarande
klassregister certifierar inte alla historiska klasser; ECB:s referensfixing är
inte nödvändigtvis fondens värderingskurs. Saknat underlag blir aldrig noll.
Kapital minus avkastningsjusterat tidigare kapital skulle senare vara ett
uppskattat fondflöde, inte observerade betalningar eller aktieorder.

VERIFIERING OCH FILER
- audit/REPORT_F_FINAL_SV.txt och FINAL_SOURCE_DECISION_SCOPE.json: slutbesked.
- audit/F_*: slutlig kapitaltäckning utan äldre reservflaggor.
- audit/NEW_POSITION_*: separat täckning av nytillkomna bruttopositioner.
- audit/FINAL_A_TO_F_COVERAGE_COMPARISON.csv: alla bevarade mellanversioner.
- source_method/: daterade regler, kod, källflaggor och separat kontroll.
- provenance/SOURCE_ACQUISITIONS.json: sex nya originalarkivs namn och SHA256;
  tom splitfråga redovisas. De tidigare två pilotarkiven finns i föregående paket.
- provenance/ECB_FX_SOURCE.json och ECB_FX_SEK_201612_202312.csv: offentlig FX-källa.
- precision/: metodgranskarens förslag, inte utförd pilot eller godkänt styrketest.
- verify_published.py: oberoende aritmetisk rekonstruktion av F och nya positioner.

Från reporoten: python3 output/omxsb_shof_coverage_20261103/verify_published.py
Det kräver bara Python-standardbiblioteket och det redan publicerade normaliserade
ägarregistret i output/omxsb_contribution_round_20261103/ownership_capital/.
Det kontrollerar beräkningarna, inte råkällornas fullständighet eller kausalitet.

De ursprungliga rådataskripten är oförändrade proveniensversioner, med lokala
arbetsvägar och licensierade beroenden i sina INPUT/LOCK-filer. De är inte en
portabel enkommandokörning från detta paket. Full rådatareplikation kräver separat
behörighet och samma indata. Kör inte deras skrivande steg i det frysta paketet.
Licensierade råserier, fulltexter, mejlinnehåll och inloggningsuppgifter ingår inte.
