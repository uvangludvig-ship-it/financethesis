# Runda 2, deklarerad 2026-11-01 20:09 CET, innan något av testen körs

Syfte: lösa de tre svagheterna i version 4. (1) Jämförelsen med nästan tillagda bygger bara på storlek. (2) Den kvarvarande effekten på cirka 1,7 % saknar förklaring. (3) Tvillingurvalet är litet.

Allt här är robusthet eller explorativt. Huvudresultatet (T5, tillägg efter 2017) ändras inte av dessa test; de redovisas bredvid.

## Gemensamt

- Som i `robusthet_deklaration.md`: onormal avkastning mot .OMXSBGI, dagsavkastning över 1 000 % satt till saknad, "efter" = AD 2017–2026, kluster på översyn, 95 % intervall med t(G−1), restriktiv wild cluster bootstrap för regressionskoefficienter, frö 20261101.
- Regressionen "som T5" = CAR = b·Händelse + c·uppgång [AD−100, AD−1] + d·log börsvärde + fasta effekter per översyn.

## T6. Nasdaqs urvalsregel (svaghet 1)

Regeln enligt Nasdaqs metod för OMXSB: de 10 % mest omsatta (minst 25) väljs; de 30 % minst omsatta är aldrig valbara; övriga väljs per ICB-supersektor i ordning efter fritt flytande börsvärde tills minst 85 % av supersektorns fritt flytande börsvärde är täckt.

- Referensdag: sista handelsdagen i april (juni-översyner) respektive oktober (december-översyner); för 2009JAN sista handelsdagen i november 2008.
- Omsättning: summan av volym × stängningskurs över sex kalendermånader fram till referensdagen.
- Börsvärde vid referensdagen, multiplicerat med andel fritt flytande om LSEG ger historisk eller aktuell andel; annars helt börsvärde.
- Universum: aktier med kurs på referensdagen. Om LSEG ger marknadsplats tas bara huvudlistan (XSTO) med.
- Supersektor: ICB-supersektor från LSEG om den finns, annars TRBC-sektor, annars ingen sektorindelning (då 85 % av hela marknaden).
- En rad per bolag och aktieslag; regeln tillämpas per aktieslag som hos Nasdaq.
- **Träffsäkerhet** (redovisas först): andel av de verkliga tilläggen som regeln väljer, andel av de verkliga medlemmarna efter översynen som regeln väljer, och antal aktier regeln väljer som inte lades till.
- **Nästan valda:** icke-medlemmar som inte läggs till, inte är bland de 30 % minst omsatta, och vars kumulativa andel av supersektorns fritt flytande börsvärde (inklusive aktien själv) ligger högst 10 procentenheter över gränsen på 85 %, eller som regeln väljer men som inte lades till.
- **Test:** som T5, med log omsättning som extra kontroll, tillägg mot nästan valda. Primärt: tillägg efter 2017, [AD−1, ED+1]. Sekundärt: före 2017.
- **Tolkning bestämd i förväg:** om b har undre gräns över 0 håller huvudresultatet även mot regelns nästan valda. Är träffsäkerheten för tillägg under 50 % redovisas testet, men vägs lätt.

## T7. Håller effekten över tid? (svaghet 2)

- Som T5 (samma nästan tillagda), men med CAR [AD−1, ED+20], [AD−1, ED+60] och [AD−1, ED+100]. Tillägg och borttag, före och efter 2017.
- **Tolkning:** b vid ED+100 minst hälften av b vid ED+1 (≥ 0,84) med undre gräns över 0 betyder att effekten består. b vid ED+100 nära 0 eller negativt betyder att den går tillbaka, alltså långsamt tryck. Annars går det inte att avgöra.

## T8. Likviditet (svaghet 2)

- Mått: relativ spread (sälj − köp) / mittkurs, och omsättning (volym / antal aktier i slaget). Median per aktie över före-fönstret [AD−120, AD−21] och efter-fönstret [ED+20, ED+120]. Förändring = log(efter) − log(före).
- **T8a, tvillingar** (39 slutliga händelser): skillnad i förändring, indexslag minus systerslag, med tecknet vänt för borttag. Medel, 95 % intervall och teckenbyte över bolag. Dessutom förändringen för varje slag för sig.
- **T8b, tillägg mot nästan tillagda** (som T5): regression av förändringen på Händelse + uppgång + log börsvärde + fasta effekter per översyn.
- **Tolkning:** blir indexslaget lättare att handla än systerslaget, medan priserna rör sig lika, förklarar likviditet i just det värdepappret inte prisökningen. Förbättras båda slagen lika, eller tilläggen mot de nästan tillagda, är likviditet på bolagsnivå en kandidat.

## T9. Ägarbredd, uppmärksamhet (svaghet 2)

- FI-innehav 2018Q4–2026Q2. Antal svenska fonder (Fond_institutnummer) som äger aktieslaget (ISIN, Antal > 0) vid sista kvartalsslutet före AD och första kvartalsslutet minst 20 handelsdagar efter ED.
- Två mått: alla fonder, och fonder vars namn inte innehåller "index", "indexnära", "exponering", "ETF" eller "XACT" (gemener och versaler).
- Förändring = log(1 + efter) − log(1 + före). Test som T5 (tillägg mot nästan tillagda), 2019–2026.
- **Tolkning:** fler nya ägare bland icke-indexfonder för tilläggen än för de nästan tillagda passar med uppmärksamhet. Ingen skillnad talar emot.

## T10. Aktiva fonders köp (svaghet 2)

- Händelser 2019–2026 med FI-data (`events_car.csv`: `activebuy`, `nt`). CAR [AD−1, ED+1] = a + b·activebuy + c·nt, tillägg och borttag separat, kluster på översyn.
- **Tolkning:** positiv och signifikant b passar med efterfrågan från aktiva fonder som jämför sig med index. Annars talar det emot.

## T11. Tvillingar i OMXS30 (svaghet 3)

- OMXS30-ändringar från `omxs30_changes_2005_2026.csv` med känt beskedsdatum, där bolaget har ett annat aktieslag med andel handelsdagar ≥ 0,90 över [AD−60, ED+20]. Uteslut: Stora Enso, avknoppning (Essity), D-aktier (SBB), bud eller kontrollstrid i fönstret (Scania 2007, MAN:s bud).
- Kandidater: Holmen B 2007, SSAB A 2007, MTG B 2009 och 2016, Kinnevik B 2014 och 2025, SSAB A 2021, Epiroc A 2025, Industrivärden C 2025, Atlas Copco B 2025, Electrolux B 2025.
- Spread som i tvillingtestet, [AD−1, ED+1], tecken vänt för borttag. Inferens med placebofönster som i `twin_run.py`.
- Redovisas separat och sammanslaget med de 39 OMXSB-händelserna.
- **Tolkning:** som tvillingtestet. Sammanslaget ger det en övre gräns med fler händelser.

## Tillägg 20:11 CET, innan T6 körts

- Referensdag för T6 efter när ändringen gäller: januari → sista handelsdagen i november året innan; juni → april; juli → maj; december → oktober.
- Aktier som saknar sektor från LSEG läggs i en egen grupp "okänd", där 85 %-regeln tillämpas för sig. Andelen börsvärde utan sektor redovisas per översyn.

## Tillägg 20:15 CET: testkörning och resultat som redan körts

- T8a (likviditet, tvillingar) och T10 (aktiva fonder) är körda här efter deklarationen 20:09 (`runda2_lokalt_har.py`, `runda2_har_results.csv`). I T8a saknas köp- och säljkurser för systerslag som hämtats separat från LSEG (NCC A, Sweco A, Bonava A, Ratos A).
- Koden för T6, T7, T8b, T9 och T11 testkördes på utdraget med 186 aktier för att kontrollera att den går igenom. Siffrorna från testkörningen har setts. Utdraget är inte det deklarerade urvalet (T6 får där en universum på cirka 140 aktier och T9 saknar FI-data). Det är körningen på hela panelen som gäller.

## Tillägg 20:29 CET: ändrade tolkningsregler, innan något körs på hela panelen

T8a och T10 är redan körda och har setts. Ändringen nedan är metodologisk och gäller alla test i runda 2.

- Ett insignifikant samband utesluter inte en förklaring. En förklaring räknas som begränsad bara om konfidensintervallets gräns ligger under en i förväg angiven storlek. Varje test redovisas med skattning och 95 % intervall. Formuleringar av typen "talar emot" i T8–T10 stryks.
- Lika avkastning för A- och B-aktien utesluter inte köptryck, eftersom påverkan kan spridas mellan aktieslagen. Tvillingtestet mäter bara den del som är specifik för indexslaget. T8a- och T11-tolkningarna ändras därefter.
- Före T5, T6, T7, T8b och T9 körs om ska medlemslistan vara verifierad: alla nycklar kopplade till RIC, RIC-byten hanterade och noll brott i medlemskedjan. Annars stoppar koden.
- T6 körs i två steg. Först redovisas träffsäkerheten, och jämförelsen körs bara om den har setts och godkänts.
- T9 kräver en ISIN-koppling som gäller vid varje kvartal, inte dagens ISIN.

## Tillägg 21:21 CET: verifierad kontrollgrupp och datakällor, före körning på hela panelen

**Redan kända resultat som specifikationen nedan skrivs med vetskap om:**
- T5 (gamla medlemslistan, utan First North-filter): tillägg efter 2017 +1,68 (0,57 till 2,80); per översyn +1,70. Beskrivande känslighet: utan de 48 misstänkta raderna +1,71; utan First North +1,70; bara huvudlistan +1,53.
- T2-hela: +1,27 (−1,18 till 3,72) med en kontroll; +1,33 (−0,27 till 2,93) med tre. Korrigerad matchning enligt Ludvigs körning: +1,6 till 2,1 (inte granskad här).
- T7 på utdraget med 186 aktier (inte det deklarerade urvalet): tilläggens försprång mot nästan tillagda +1,33 vid ED+1, +2,09 vid ED+20, −1,06 vid ED+60, −1,98 vid ED+100, alla med breda intervall.
- T6 på utdraget: träffsäkerhet för tillägg 0,28–0,34 utan bransch och fritt flytande; inte meningsfullt med 140 aktier i universumet.

**Medlemskap.** `medlemskap_verifierad.csv` ersätter `resolve()`. Den bygger på medlemskedjan med två tickerkopplingar (Nordea → NDASE.ST, Tieto → TIETOS.ST) och dokumenterade rättelser för Nokia, EnQuest, CDON, Corem B, Collector/Norion och Sampo; se `medlemskap.py`. Efter rättelserna: 0 olösta nycklar och 0 brott i kedjan. Status "osäker" (exakt inträde okänt) utesluts ur alla kontrollgrupper.

**Kontrollgrupper (T5, T6, T7, T8b, T9).** Utesluts:
- medlemmar och osäkra före översynen;
- First North och liknande marknader (LSEG-marknadsplats SSME eller ONSE).

Aktier utan känd marknadsplats (avnoterade) behålls, men andelen redovisas. Känslighet: bara huvudlistan (XSTO).

**T6, data.** ICB-supersektor (TR.ICBSupersectorCode), annars TRBC-sektor, annars "okänd". Andel fritt flytande från historiken per referensdag, annars aktuell, annars 100 %. NDASE.ST och TIETOS.ST läggs till universumet med kurs och volym från LSEG och börsvärde per månad. Månadsraderna saknar datum; de 250 raderna antas vara januari 2006 till oktober 2026 i ordning. T6 körs i två steg: först bara träffsäkerheten. Jämförelsen körs separat när träffsäkerheten har setts.

**T9, ISIN.** Ett ISIN används för en händelse bara om det finns i FI-data senast i kvartalet före. Annars utesluts aktien ur T9 för den händelsen.

**Tolkning, alla test.** Skattning med 95 % intervall. Ett intervall som innehåller 0 betyder "inte påvisat", inte "uteslutet".

## Tillägg 21:41 CET: testkörning av den rättade koden

Den rättade koden testkördes på utdraget med 186 aktier och, för T9, på ett FI-utdrag som bara innehåller en del av fonderna och aktierna (`/home/claude/fi_check/parsed/holdings.csv`). Det sågs att T9 i testet gav en större ökning i antal ägande fonder för tillägg än för nästan tillagda (cirka 0,35–0,40 i log-punkter). Testet är inte giltigt eftersom FI-utdraget saknar de flesta kontrollaktier. Det är körningen på hela panelen och hela FI-filen som gäller.
