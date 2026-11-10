# Deklaration: händelser med egen bolagsnyhet i fönstret

Skriven 2026-11-09 20:50 CET, innan någon av de 24 händelserna utom Sivers Semiconductors sökts igenom efter nyheter. Sivers är kontrollerad: avtal med GlobalFoundries 2 juni 2026 (ED+1), blankarrapport 1 juni, kvartalsrapport 29 maj.

## Varför

En enskild händelse får inte tas bort för att den är stor. Det giltiga skälet i en eventstudie är att fönstret innehåller en nyhet om bolaget som inte har med indexet att göra. Regeln gäller alla händelser lika, åt båda hållen.

## Urval

De 24 händelser där |CAR [AD−1, ED+1]| > 20 % (`data/events/omxsb_changes_with_car_2007_2026.csv`, kolumnen `tot`). De listas i `data/events/news_screen_extreme_events.csv`. Övriga 457 händelser gås inte igenom; det redovisas som en begränsning.

## Regel

En händelse räknas som förorenad (`contaminated = ja`) om bolaget självt, eller en part i en transaktion med bolaget, offentliggjort något av följande med datum från AD−1 till och med ED+1:
- delårsrapport, bokslutskommuniké eller vinstvarning,
- bud, förvärv, avyttring, fusion eller avnotering,
- nyemission, återköp eller annan kapitalåtgärd,
- större avtal, order, myndighetsbeslut eller studieresultat,
- en offentlig blankarrapport eller utredning om bolaget.

Nyheter om hela branschen eller marknaden (till exempel oljepriset) räknas inte. Nyheten om själva indexändringen räknas inte. Går det inte att avgöra: `oklart`, och händelsen behålls.

Källor: bolagets egna pressmeddelanden (Cision, MFN, GlobeNewswire, bolagets webbplats) och finanspress. Varje bedömning noteras med datum, rubrik, kategori och länk.

## Vad som räknas

`code/09_news_screen.py`: samma inferens som tabell 1 (klustrat per översyn, wild cluster bootstrap, frö 20261103) för tillägg och borttag 2007–11, 2017–21, 2022–26, 2017–26 och skillnaderna 2022–26 minus 2007–11 och 2022–26 minus 2017–21, med och utan de förorenade händelserna.

## Läsning, bestämd nu

- Huvudtabellen ändras inte. Resultatet redovisas som en kolumn i robusthetstabellen ("utan händelser med egen bolagsnyhet i fönstret").
- Ändras stjärnnivån för något test jämfört med tabell 1 skrivs det ut i robusthetskapitlet.
