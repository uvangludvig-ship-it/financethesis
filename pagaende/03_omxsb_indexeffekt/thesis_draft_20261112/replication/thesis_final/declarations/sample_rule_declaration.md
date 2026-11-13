# Deklaration: samma urvalsregel i alla tabeller (G&S filter) och samma händelser med och utan kontroller

Skriven 2026-11-10 17:21 CET, innan körningen. Beslutad av Alexander 17:18.

## Bakgrund

1. Tabell 1 (steg 01) hade med 19 borttag som tabell 2 och D/M-tabellerna uteslöt (`omxsb_deletion_flags_2007_2026.csv`, ur Ludvigs `mechanisms_2007.py`).
2. Regressionerna med kontroller kördes på färre händelser än de utan.

## Vad som redan var sett

- Steg 10 (17:12 samma dag) och runda 11: utan alla 19 var borttagens fall 2007–11 till 2022–26 −4,06 (p 0,09), mot 5,17 (p 0,015) i tabell 1.
- Listan över de 19 med CAR per händelse. Fem av de tio med bud eller fusion ligger i 2007–11 och har negativ CAR.

Ändringen gjordes med vetskap om att borttagens resultat kunde bli svagare. Skälet är regeln i förlagan, inte utfallet.

## Regel 1: urval

Greenwood och Sammon utesluter bolag som noterats, köpts upp eller avnoterats inom 100 dagar, och bolag som själva är köpare. Här:

- Notering och avnotering inom 100 dagar var redan borttagna i replikeringen (`listed_100`, `delisted_100`).
- Nytt i tabell 1 och alla andra CAR-tabeller: borttag där `flag_offer` eller `flag_delist` är sann utesluts (10 borttag). Orsaken till borttaget är uppköpsbud, fusion eller köpare, eller avnoteringsansökan, eller så avnoterades aktien inom 100 handelsdagar efter ED. Närmaste motsvarighet till G&S regel, inte en exakt kopia: flaggan bygger på orsaken till borttaget.
- De 9 borttag som bara har `flag_shares` (aktieantalet ändrat mer än 10 % mellan ED och ED+100) är kvar i CAR-tabellerna och utesluts som förut där D används (steg 02).
- Begränsning: för tillägg finns ingen motsvarande flagga. Regeln tillämpas bara på borttag.

Berörda steg: 01 (via `returns.py`), 05, 09, 10, årstabellen och figur 2 (årsmedel räknas i 01 ur händelserna). Steg 02 och 03 ändras inte.

## Regel 2: samma händelser

- Tabell 2 (steg 10): utan kontroller på hela urvalet (= tabell 1), med kontroller på händelser med alla fyra kontroller, och utan kontroller på exakt de händelserna.
- M (steg 10): regressionen i tabell 6 utan kontroller också på de händelser som har alla kontroller. Steg 02 rörs inte.

## Läsning, bestämd i förväg

- Det nya urvalet är huvudspec. Det gamla (alla borttag med) redovisas som robusthetsrad (panel R i `tabell1_lang.csv`).
- Är borttagens fall 2007–11 till 2022–26 inte signifikant på 5 % skrivs att det inte kan påvisas på 5 %.
- Byter någon skillnad i M tecken eller stjärnnivå på samma händelser skrivs det ut.
- Kontrollsiffrorna i `08_check_numbers.py` uppdateras för borttag; alla andra ska vara oförändrade.
