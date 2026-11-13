# Runda 5: T15, T16, T17

Deklarerad 1 november 2026, 23:22 CET. Inget i dessa test har körts. Bara urvalsuppgifter har setts: antal händelser per grupp, väntetid per översyn och antal ESG-indexfonder per kvartal. Inga avkastningar.

Rättelse av det som sades i chatten 23:12: väntetiden mellan besked och ändring kortades från maj 2021 (översyn 2021H1), inte från november 2023. Den var 14–17 handelsdagar till och med 2020H2 (2020H1: 11) och 6–8 dagar från 2021H1.

## Kända resultat före dessa test

- Tvillingar, rensade (A/B-revisionen 21:42): indexslag minus systerslag [AD−1, ED+1] +0,33 (−0,47 till 1,16), 39 händelser i 13 bolag. Explorativt, med gamla serier: systerslaget utanför index (minst ena sidan) +0,70 (p 0,37, 18 händelser); i index +0,01 (21 händelser).
- Tillägg efter 2017 mot nästan tillagda (T5v): +1,53 (0,36 till 2,69).
- Första steget v2: indexfonderna köper i median 0,2–0,8 % av indexslaget. Rena indexfonder faller till 2 från slutet av 2022, när flera byter till ESG-varianter av OMXSB.
- T14 stoppade på styrkekontrollen.

## T15. A/B-gränsen på rätt urval

**Urval.** De rensade tvillinghändelserna (`ab_revision_events.csv`, status ok, minst 20 placebofönster) där systerslaget inte ingår i OMXSB varken före eller efter översynen. Där köper indexfonderna bara indexslaget. Det är 18 händelser i 8 bolag.

**Mått och inferens.** Samma som A/B-revisionen: indexslag minus systerslag, [AD−1, ED+1], tecken vänt för borttag. Intervall och p från placebofönster (samma bolag, ±45 dagar från AD:s dag på året, andra år).

**Redovisas oavsett utfall:**
- medel och 95 % intervall;
- övre gränsen som andel av indexslagets egen rörelse mot marknaden i samma händelser;
- sekundärt: samma för händelser från 2017 (9 händelser).

**Tolkning.** Övre gränsen är den största skillnad mellan aktieslagen som är förenlig med datan. Den avgör inte mekanismen.

## T16. ESG-bytet

**Idé.** Från slutet av 2022 följer de flesta indexfonderna ESG-varianter av OMXSB. Ett tillägg som inte kommer med i ESG-varianten köps bara av de få rena OMXSB-fonderna. Om köptryck driver priset bör sådana tillägg stiga mindre. Om urval, information eller uppmärksamhet driver priset finns ingen skillnad.

**Urval.** Tillägg med AD från 2022-11-01 (`T5urval_T7_T8b_events.csv`, event = 1). Tillägg utan FI-kvartal efter ändringen faller bort.

**Klassning, med FI-data.** ESG-indexfonder: bred enligt första steget, jämförelseindex i OMXSB-familjen och med ESG, Responsible, Sustainability, hållbar, custom, Paris eller climate i jämförelseindex. För varje tillägg: andelen ESG-indexfonder (som finns kvartalet efter) som äger aktieslaget kvartalet efter ändringen.
- Utanför ESG-varianten: andel under 0,2.
- Inom: andel minst 0,5.
- Däremellan: utesluts och antalet redovisas.

**Utfall och skattning.** CAR [AD−1, ED+1] mot marknaden. Regression på en dummy för "utanför", uppgång [AD−100, AD−1], log börsvärde och fasta effekter per översyn. Klustrat på översyn, restriktiv wild cluster bootstrap (Webb-vikter när översynerna är färre än 12), intervall med t(G−1).

**Styrkekontroll, innan skattningen visas.** Koden skriver bara antal händelser per grupp, antal översyner och MDE = (t(0,975; G−1) + t(0,80; G−1)) × SE. Testet körs bara om:
- minst 8 tillägg utanför, i minst 4 översyner; och
- MDE ≤ 1,5 procentenheter (ungefär huvudeffekten mot nästan tillagda, alltså den skillnad som väntas om ESG-fonderna står för det mesta av köpen och köpen driver priset).

Annars stopp, och skattningen visas inte.

**Tolkning om testet körs.** Undre gräns över 0 för "inom minus utanför": förenligt med köptryck. Ett intervall som innehåller 0 betyder "inte påvisat". ESG-uteslutning hänger ihop med bransch, och branschchocker i översynsfönstret tas inte bort av fasta effekter per översyn.

## T17. Kortare väntetid från 2021

**Idé.** Om arbitragörer tar emot indexfondernas köp och bär risk mellan besked och ändring, bör ersättningen, och därmed prisrörelsen, minska när väntetiden kortas från cirka 15 till 6–8 handelsdagar. Om urval eller information driver priset påverkar väntetiden inte rörelsen.

**Urval.** Samma som T5v efter 2017: tillägg och nästan tillagda (`T5urval_T7_T8b_events.csv`). Kort väntetid: AD från 2021-05-01 (översyn 2021H1 och senare). Lång: 2017H1–2020H2.

**Utfall och skattning.** CAR [AD−1, ED+1]. Regression som T5v plus interaktionen händelse × kort väntetid. Koefficienten för interaktionen är testet. Klustrat på översyn, wild cluster bootstrap.

**Styrkekontroll, innan skattningen visas.** Koden skriver bara SE och MDE för interaktionen. Testet körs bara om MDE ≤ 0,92 procentenheter. Gränsen är den minskning som väntas om hela effekten efter 2017 (1,53) vore riskersättning proportionell mot väntetiden, som kortats med cirka 60 %.

**Tolkning om testet körs.** Interaktion med övre gräns under 0: förenligt med riskburen prispress. Andra förändringar över tid (likviditet, ESG-bytet) sammanfaller med brytpunkten och kan inte skiljas ut.

## Körning

T15 körs direkt. T16 och T17 körs i två steg: först styrkekontrollen, sedan skattningen bara om den är godkänd. Ingen testkörning.

## Utfall av körningen, 23:25 CET

- **T15:** systerslaget utanför index båda sidor, 18 händelser i 8 bolag: +0,70 (−0,85 till 2,38), p 0,33. Indexslaget mot marknaden i samma händelser +5,24 (gamla serier, används som skala). Övre gränsen motsvarar 45 % av indexslagets rörelse. Från 2017, 9 händelser i 5 bolag: +0,42 (−2,17 till 3,22); övre gränsen är lika stor som hela rörelsen (3,12), alltså inte informativ.
- **T16 stoppade:** 11 tillägg utanför ESG-varianten i 5 översyner, 33 inom, 22 mellan (uteslutna), 3 utan FI-kvartal. MDE 10,7 procentenheter mot gränsen 1,5. Ingen skattning.
- **T17 stoppade:** 96 tillägg med kort väntetid, 63 med lång, 19 översyner. MDE 3,26 procentenheter mot gränsen 0,92. Ingen skattning.

## Tillägg 23:35 CET

- Väntetiden kortades i två steg: till 7–8 handelsdagar i maj 2021 och till exakt sex dagar från november 2023. Båda stämmer med repots `REGIMES.md`.
- `REGIMES.md` (30 oktober) jämför rå CAR per regim och borde ha listats som känt resultat i T17. T17 stoppade i styrkekontrollen innan någon skattning gjordes.
