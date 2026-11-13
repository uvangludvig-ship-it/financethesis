# OMXSB: aktuell arbetsstruktur och evidensstatus

Rättad 1 november 2026 efter kod- och tolkningsgranskning. Detta är en arbetsplan för författarna, inte uppsatstext. Föregående version är bevarad i `archive/robusthet_repair_20261101/thesis/design/OMXSB_struktur.md`.

## Fråga och logiskt flöde

Hur robust är den observerade prisreaktionen kring OMXSB-byten mot jämförelser med andra aktier, och hur tillfällig och aktieslagsspecifik är den?

1. **Replikation:** beskriv svenska prisreaktioner med G&S:s mått. Marknadsjusterad avkastning är ett uppmätt utfall, inte ensam identifiering av indexbytets kausala effekt.
2. **Kontrolljämförelse:** jämför eventaktierna med andra aktier med liknande tidigare avkastning och storlek. Redovisa balans, täckning, vikter och osäkerhet. Detta är den aktuella huvudsakliga fördjupningen.
3. **Tidsprofil:** undersök hur mycket av rörelsen som går tillbaka inom uttryckliga fönster. Ett osäkert kortsiktigt återgångstest bevisar inte permanent effekt.
4. **A/B:** undersök relativ prisrörelse mellan eventaktien och en verifierad systeraktie. Redovisa båda prisbanorna. Systern kan påverkas av samma indexefterfrågan; den är inte automatiskt obehandlad.
5. **Tolkning:** avgränsa vad dessa jämförelser kan stödja. Ingen additiv uppdelning i urval, köptryck och bolagseffekt och ingen slutsats att migration förklarar landskillnaden följer av testerna ensamma.

## Ankare och extra observation

**X:** G&S dokumenterar en kraftigt minskad amerikansk prisreaktion och undersöker flera förklaringar, bland annat nettning genom migration och lägre prisrespons per efterfrågeförändring.

**Y:** Den svenska studien jämför den vanliga eventavkastningen med andra aktier och, i ett separat mindre urval, med systeraktieslag. Extra jämförelser behöver inte vara unika för Sverige, men måste tillföra information relativt det första testet.

**Z:** Bedöm robustheten hos den uppmätta svenska reaktionen och begränsa dess relativa aktieslagskomponent. Det är inte ett test som säkert väljer mellan migration, uppmärksamhet och spridd indexefterfrågan.

## Vad som faktiskt är körbart och verifierat

| Del | Status |
|---|---|
| G&S-replikation | Tidigare körd; använd korrigerad audit och rätt tidsfönster/urval när resultat citeras. |
| T2: bred panelmatchning | Rättad kod i `code/build/robusthet_hela.py`. Skattning, intervall och bootstrap väger samma översynsmedel. Matchning använder endast uppgifter före utfallsstart. Aktuella siffror genereras i `output/omxsb_robusthet_20261101/results.csv`. |
| T5: storleks-/medlemsproxy | Tidigare +1,68 kan återskapas från sparade rader, men gruppen är inte verifierat nästan invalda. Den rättade koden använder en uttrycklig spärr vid olösta medlemsidentifierare; se körningsstatus. Ingen spärr eller saknad skattning får kallas ekonomisk noll. |
| Kort återgång ED till ED+10/20 | Uppgifter finns i konversationen, men tillhörande aktuell kod, eventfil och full resultatkedja har inte följt med det granskade robusthetspaketet. Därför inte verifierat resultat här. Äldre ED+2 till ED+100 är ett annat test. |
| Ny A/B-prisanalys och multiplikator 0,57 | Ingen tillhörande verifierad körning i robusthetspaketet. Äldre explorativ parpilot har redan lästs; den får inte presenteras som ny blind analys. |
| A/B-förstasteg 0,74 | Summan finns i äldre importerad fil men beräkningskedjan är inte validerad. Nuvarande `twin_first_stage.py` skriver kontrollstatus och NA tills nödvändiga underlag är verifierade. |
| Migration | Inte färdigreplikerad. |

Det aktuella resultatdokumentet är `output/omxsb_robusthet_20261101/RESULTAT.md`, med en kopia i repots `RESULTAT_2026-11-01.md`. Rättelsespecifikationen är `ROBUSTHET_RATTELSE_20261101.md`. Detaljerade tolkningsgränser finns i `OMXSB_TOLKNINGSREGLER.md`.

## Kontrollanalysen

- Utfallet behåller replikationens `[AD−1, ED+1]`. Matchningsuppgifterna slutar AD−2 och överlappar inte utfallet.
- Tidigare avkastning omfattar 100 handelsdagar. Börsvärde hämtas senast AD−2.
- T2 matchar på tidigare avkastning och logaritmerat börsvärde. En och tre kontroller redovisas, utan att välja efter p-värde.
- Valda kontrollaktier ersätts inte för att deras senare utfall saknas. Bortfallet sparas.
- Kontrollpoolen är den tillgängliga panelen, inte en verifierad historisk OMXSB-kandidatcensus. Huvudlistebehörighet och exakt Nasdaq-urval kräver mer än aktuell börskod, storlek eller en .ST-identifierare.
- T5 är en beskrivande proxy och får inte användas som gränsexperiment eller som marknadens förhandsförväntan.
- Förhandsuppgången kan själv innehålla väntade indexköp. Matchningen avgränsar därför ett senare fönster och behöver inte mäta hela effekten av kommande medlemskap.
- Alla tester är explorativa rättelser efter att tidigare resultat setts. Specificerade känslighetsanalyser och nödvändiga rättelser får ändra slutsatsen.

## A/B: användbart men avgränsat

En positiv relativ rörelse kan vara förenlig med att efterfrågan påverkar aktieslagen olika. En liten, precist skattad skillnad kan begränsa den relativa komponenten. En osäker skillnad är inte bevisad noll.

Om båda aktieslagen rör sig lika kan det bero på gemensamma nyheter eller att indexefterfrågan sprids mellan aktieslagen. Det visar inte att köptrycket är borta eller att uppmärksamhet är mekanismen. En relativ multiplikator kan inte ersätta G&S:s totala efterfrågemultiplikator.

Den importerade listans 58 rader är **kandidater**. Vissa noteringsstarter och externa systermappningar är antagna. Slutligt urval måste styrkas med historisk notering, rättigheter, korrekta identifierare, likviditet, corporate actions och övriga indexbyten. Antal prisrader ersätter inte antal oberoende bolag och översyner.

FI:s kvartalsinnehav är inte order på indexdagen. En riktig nolla kräver rätt instrument och en fullständig rapport från samma daterade fondpopulation på båda sidor. Kinnevik A efter juni 2024 hade ett konkret gammalt ISIN i den importerade koden. Det korrigerade identifierarledet gör inte automatiskt resten av förstasteget giltigt.

## Tidsprofil och statistiska påståenden

- Skilj indexets ikraftträdandedag från sista stängningen före ikraftträdandet och faktisk fondhandel. Kvartalsdata daterar inte en stängningsauktion.
- Ange vilken version och vilket fönster av G&S som jämförs. Figurnummer skiljer mellan arbetsversioner.
- Kort och långt återgångsfönster har olika tolkning och kan ha olika urval. Jämför samma event när en återgångsandel beräknas.
- Skillnaden mellan en signifikant period och en insignifikant period är inte ett test av periodskillnaden.
- Ett konfidensintervall, inte bara ett p-värde, behövs för att utesluta en ekonomiskt viktig återgång eller relativ prisskillnad.

## Originalitet och genomförbarhet

Inget påstående görs att A/B, indexprognoser eller innehavsdata bara finns i Sverige. Inget försthetsanspråk görs för systeraktier som indexjämförelse. Ett möjligt bidrag är en systematisk och transparent OMXSB-prövning med rätt identifierade begränsningar.

Befintliga prisfiler för fler systeraktier behöver granskas per event; filernas existens innebär inte verifierad täckning. Datagap ersätts inte med antaganden om noteringsdatum, nollinnehav eller framtida datatillgång. FTN-spåret öppnas inte i denna rättelse.

## Föreslagen redovisningsordning för författarna

Replikation → kontrolljämförelse → tidsprofil → A/B med validerad täckning → samlad tolkning. Delar med otillräckligt underlag redovisas som begränsade eller ofullständiga. Resultaten avgör slutsatsen; ingen önskad berättelse väljs i förväg.
