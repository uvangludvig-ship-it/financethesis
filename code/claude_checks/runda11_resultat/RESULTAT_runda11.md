# Runda 11: resultat (G&S fullt ut, multiplikatorn M)

Deklaration: `runda11_deklaration.md` (sparad 19:23:35). Tillägg och körtider: `runda11_tillagg.md`. Kod: `runda11.py`. Data: `runda11_resultat/` (`runda11_resultat.csv` med alla skattningar, `handelser.csv` per händelse, `G_figur1_figur5.csv`, `I_figur7.csv`, `F_nyemissioner_urval.csv`). Figurerna finns som data, inte som bilder.

Steg 0 godkänt (T24 återskapat, största avvikelse 0,022). Steg 1: H11a och H11b körs enligt deklarationen; T30 klarar inte styrkevillkoret (MDE 3,8–8,2 mot 2) och redovisas bara som lutning.

## Huvudresultat

1. **M har fallit kraftigt** (H11a). Tillägg, totalt fönster, med kontroller: M från 199 (2007–11) till 2,3 (2022–26). Skillnad 197 (58 till 336), wild bootstrap p 0,055. Intervallet utesluter 0, men p ligger strax över 0,05. Nivån 2007–11 bygger på 11 tillägg och ett D på 0,05 % och är mycket osäker. Med alla händelser (känslighet): 82 till 1,7.
2. **I dag ligger Sverige mellan USA på 2000-talet och 2010-talet.** M 2022–26 med kontroller 2,3 (0,8 till 3,8), elasticitet cirka −0,4. G&S: M med kontroller 0,7 för 2010-talet, elasticitet −1,44 till −2,72 för 2010-talet och −0,17 till −0,28 för 2000-talet. Den svenska marknaden tar emot indexköpen ungefär tre gånger sämre än den amerikanska gör i dag. Beskrivande: olika marknader, perioder och mått på D.
3. **Säljarna finns utanför fonderna** (tabell 7, H11c). Vid tillägg 2017–26 köper alla fonder tillsammans 1,25 % av aktierna: OMXSB-indexfonderna 0,77 och övriga passiva fonder 0,60. Aktiva fonder ändrar inte sitt innehav: −0,13 (−0,41 till 0,16), p 0,38. Aktierna kommer alltså från investerare utanför fonderna, till exempel direktägande hushåll, utländska investerare och försäkringsbolag. I USA tar andra institutioner emot köpen (G&S tabell 7). Vid borttag 2022–26 säljer även aktiva fonder: 0,50 (0,10 till 0,90).
4. **Den indexkopplade efterfrågan är större än D.** Övriga passiva fonder (blandfonder som följer OMXSB, andra indexfonder) köper nästan lika mycket som OMXSB-indexfonderna. Räknat på all passiv efterfrågan blir M 2022–26 cirka 1,7 i stället för 2,7 (2,28 / (0,86 + 0,48); räkneexempel, inte deklarerat).
5. **I långt fönster har M inte fallit sedan 2017** (H11b). Med kontroller: 5,8 (2017–21) och 6,5 (2022–26), mot 4,4 och 2,3 i totalt fönster. 2007–11 mot 2022–26: 163 (−3 till 329), p 0,13, inte visat. Enligt läsningen bestämd i förväg är fallet mindre i långt fönster, vilket är förenligt med att en del av effekten har flyttats till före beskedet. Det är inte visat.
6. **Sammansättning och nyemissioner förklarar inte nedgången.** Med G&S kontroller blir skillnaden 2007–11 mot 2022–26 större, inte mindre: 8,5 (3,4 till 13,6) mot 7,0 utan kontroller. Tillägg ökar inte antalet aktier mer än jämförbara bolag: 0,5 procentenheter (−1,7 till 2,7).
7. **Per händelse syns inget samband mellan köp och prisrörelse** (figur 3): R² 0,004 för tillägg och 0,02 för borttag, som hos G&S. T30 saknar styrka.

## Tabeller

**Tabell 5, M per period** (primärt: händelser utan senare split; intervall från bootstrap över översyner)

| | Fönster | 2007–11 | 2012–16 | 2017–21 | 2022–26 |
|---|---|---|---|---|---|
| Tillägg | totalt | 196,7 (58,6 till 1118,1) | −9,2 (−35,7 till 4,5) | 5,1 (1,5 till 11,3) | 2,7 (0,7 till 4,8) |
| Tillägg | långt | 147,7 (−69,4 till 680,0) | −4,4 (−50,9 till 25,6) | 7,2 (2,3 till 14,0) | 7,5 (3,2 till 12,2) |
| Tillägg | CAR / D (totalt) | 8,4 / 0,04 (N 11) | −1,9 / 0,21 (N 27) | 3,3 / 0,65 (N 58) | 2,3 / 0,86 (N 78) |
| Borttag | totalt | 22,9 (−10,5 till 981,2) | 13,9 (−19,5 till 93,2) | 0,4 (−7,9 till 6,2) | 1,7 (−0,0 till 3,0) |
| Borttag | långt | 36,8 (−1,1 till 744,0) | 27,1 (−26,0 till 127,7) | −1,1 (−10,1 till 13,0) | 2,9 (−3,1 till 6,7) |
| Borttag | CAR / D (totalt) | 3,1 / 0,13 (N 10) | 2,1 / 0,15 (N 25) | 0,2 / 0,52 (N 40) | 1,7 / 1,00 (N 68) |

**Tabell 6, M med och utan kontroller** (klustrat på översyn, 95 % intervall)

| | Fönster | Kontroller | M 2007–11 | M 2012–16 | M 2017–21 | M 2022–26 | M 2007–11 − M 2022–26, p |
|---|---|---|---|---|---|---|---|
| Tillägg | totalt | nej | 196,7 (62,0 till 331,5) | −9,2 (−25,4 till 6,9) | 5,1 (0,4 till 9,7) | 2,7 (0,2 till 5,1) | 194 (59 till 329), p 0,068 |
| Tillägg | totalt | ja | 199,2 (60,2 till 338,1) | −3,9 (−19,1 till 11,3) | 4,4 (−0,7 till 9,4) | 2,3 (0,8 till 3,8) | 197 (58 till 336), p 0,055 |
| Tillägg | långt | nej | 147,7 (−7,7 till 303,0) | −4,4 (−37,0 till 28,2) | 7,2 (1,5 till 12,9) | 7,5 (2,6 till 12,4) | 140 (−15 till 296), p 0,132 |
| Tillägg | långt | ja | 169,4 (3,3 till 335,5) | 10,8 (−18,1 till 39,7) | 5,8 (−0,7 till 12,2) | 6,5 (3,7 till 9,4) | 163 (−3 till 329), p 0,126 |
| Borttag | totalt | nej | 22,9 (−14,1 till 59,9) | 13,9 (−34,2 till 62,1) | 0,4 (−7,0 till 7,8) | 1,7 (−0,4 till 3,7) | 21 (−16 till 58), p 0,282 |
| Borttag | totalt | ja | 20,2 (−14,2 till 54,6) | 9,8 (−37,2 till 56,9) | −0,0 (−6,9 till 6,9) | 1,8 (−0,4 till 4,0) | 18 (−16 till 53), p 0,311 |
| Borttag | långt | nej | 36,8 (−4,2 till 77,7) | 27,1 (−38,8 till 93,1) | −1,1 (−13,2 till 11,0) | 2,9 (−2,5 till 8,3) | 34 (−7 till 75), p 0,160 |
| Borttag | långt | ja | 14,1 (−24,8 till 53,0) | 26,5 (−34,7 till 87,6) | 6,3 (−4,0 till 16,7) | 1,5 (−4,1 till 7,1) | 13 (−27 till 52), p 0,557 |

**Tabell 7, nettoförändring i procent av aktierna** (primärt; tecken vänt för borttag, så positivt = i indexfondernas riktning)

| | Period | OMXSB-indexfonder (D) | Övriga passiva | Aktiva fonder | Alla fonder |
|---|---|---|---|---|---|
| Tillägg | 2007–11 (N 11) | 0,04 (−0,01 till 0,09) | −0,03 (−0,36 till 0,29) | 0,67 (−0,39 till 1,73) | 0,68 (−0,58 till 1,94) |
| Tillägg | 2012–16 (N 27) | 0,21 (0,10 till 0,32) | 0,45 (0,26 till 0,65) | 0,02 (−0,93 till 0,97) | 0,69 (−0,49 till 1,86) |
| Tillägg | 2017–21 (N 58) | 0,65 (0,53 till 0,77) | 0,77 (0,64 till 0,91) | −0,37 (−0,82 till 0,08) | 1,06 (0,59 till 1,53) |
| Tillägg | 2022–26 (N 78) | 0,86 (0,57 till 1,15) | 0,48 (0,22 till 0,74) | 0,05 (−0,32 till 0,42) | 1,39 (0,64 till 2,14) |
| Tillägg | 2017–26 (N 136) | 0,77 (0,61 till 0,93) | 0,60 (0,44 till 0,77) | −0,13 (−0,41 till 0,16) | 1,25 (0,82 till 1,68) |
| Borttag | 2007–11 (N 10) | 0,13 (−0,12 till 0,39) | 0,10 (−0,09 till 0,28) | −1,20 (−4,38 till 1,99) | −0,97 (−3,78 till 1,85) |
| Borttag | 2012–16 (N 25) | 0,15 (0,04 till 0,26) | 0,22 (0,05 till 0,39) | 0,72 (−1,19 till 2,63) | 1,09 (−0,83 till 3,00) |
| Borttag | 2017–21 (N 41) | 0,52 (0,37 till 0,67) | 0,26 (0,08 till 0,44) | 0,10 (−0,96 till 1,16) | 0,88 (−0,36 till 2,12) |
| Borttag | 2022–26 (N 68) | 1,00 (0,65 till 1,36) | 0,04 (−0,11 till 0,19) | 0,50 (0,10 till 0,90) | 1,54 (1,03 till 2,05) |
| Borttag | 2017–26 (N 109) | 0,82 (0,57 till 1,06) | 0,12 (−0,00 till 0,24) | 0,35 (−0,09 till 0,79) | 1,29 (0,75 till 1,83) |

H11c (aktiva fonder, tillägg 2017–26): −0,13 (−0,41 till 0,16), p 0,382.

**Tabell 2, sammansättning** (CAR totalt fönster på periodkonstanter, klustrat)

| | Kontroller | 2007–11 | 2012–16 | 2017–21 | 2022–26 | 2007–11 − 2022–26, p |
|---|---|---|---|---|---|---|
| Tillägg | nej (N 256) | 8,52 (3,79 till 13,25) | 0,25 (−3,31 till 3,81) | 2,85 (1,24 till 4,45) | 1,50 (0,06 till 2,93) | 7,03 (2,08 till 11,97), p 0,032 |
| Tillägg | ja (N 237) | 10,12 (5,09 till 15,16) | 0,55 (−3,01 till 4,11) | 2,33 (0,38 till 4,29) | 1,60 (0,68 till 2,53) | 8,52 (3,39 till 13,65), p 0,024 |
| Borttag | nej (N 206) | −5,88 (−9,81 till −1,96) | −1,75 (−7,73 till 4,22) | −0,45 (−3,44 till 2,54) | −1,82 (−3,86 till 0,21) | −4,06 (−8,48 till 0,36), p 0,083 |
| Borttag | ja (N 185) | −6,23 (−11,03 till −1,43) | −1,42 (−7,61 till 4,76) | −0,29 (−3,35 till 2,77) | −1,95 (−4,02 till 0,12) | −4,28 (−9,44 till 0,88), p 0,121 |

Kontrollernas koefficienter (med kontroller):

| | Onormal omsättning | Relativ storlek | Arbitragerisk | Analytiker |
|---|---|---|---|---|
| Tillägg | 6,23 (2,41 till 10,06), p 0,17 | 2,34 (−0,61 till 5,28), p 0,07 | −0,09 (−0,18 till 0,00), p 0,19 | −0,23 (−0,62 till 0,16), p 0,28 |
| Borttag | −0,68 (−1,62 till 0,26), p 0,15 | −2,48 (−8,71 till 3,76), p 0,44 | 0,09 (−0,20 till 0,38), p 0,54 | 0,25 (−0,08 till 0,58), p 0,12 |

**Tabell 4, uppgång före beskedet** (CAR [AD−n, AD−1], medel)

| | Period | n = 10 | n = 20 | n = 50 | n = 100 |
|---|---|---|---|---|---|
| Tillägg | 2007–11 | 0,2 (−2,7 till 3,0) | 0,3 (−6,5 till 7,1) | 3,2 (−3,0 till 9,4) | 12,1 (3,6 till 20,6) |
| Tillägg | 2012–16 | 2,8 (−0,2 till 5,7) | 4,1 (−0,5 till 8,7) | 7,0 (−3,7 till 17,7) | 18,1 (8,0 till 28,1) |
| Tillägg | 2017–21 | 1,1 (−0,7 till 2,8) | 0,6 (−2,6 till 3,8) | 2,0 (−0,1 till 4,1) | 11,8 (5,6 till 18,1) |
| Tillägg | 2022–26 | 0,1 (−2,7 till 2,9) | 2,9 (−0,2 till 6,1) | 12,3 (2,3 till 22,4) | 18,9 (8,7 till 29,1) |
| Borttag | 2007–11 | −2,8 (−7,9 till 2,2) | −6,0 (−11,8 till −0,2) | −10,0 (−17,8 till −2,3) | −18,5 (−31,2 till −5,8) |
| Borttag | 2012–16 | −2,2 (−7,8 till 3,4) | −3,5 (−8,5 till 1,5) | −5,5 (−11,8 till 0,8) | −5,8 (−13,5 till 1,8) |
| Borttag | 2017–21 | 1,5 (−3,0 till 6,1) | 0,2 (−6,4 till 6,8) | −7,1 (−14,1 till −0,1) | −11,2 (−22,0 till −0,4) |
| Borttag | 2022–26 | 0,8 (−1,4 till 2,9) | −0,9 (−5,7 till 3,8) | −8,6 (−15,1 till −2,1) | −21,1 (−30,6 till −11,7) |

**Nyemissioner:** förändring i bolagets aktieantal AD−5 till ED+60, tillägg minus nästan tillagda i samma översyn: 0,50 (−1,72 till 2,73) procent, p 0,70 (N 2586).

| Period | Tillägg: medel, andel > 5 % | Nästan tillagda: medel, andel > 5 % |
|---|---|---|
| 2007–11 | 0,7 %, 7 % (N 27) | 1,3 %, 5 % (N 354) |
| 2012–16 | 2,9 %, 11 % (N 47) | 2,1 %, 4 % (N 410) |
| 2017–21 | 3,3 %, 15 % (N 78) | 3,6 %, 9 % (N 878) |
| 2022–26 | 3,0 %, 5 % (N 80) | 1,5 %, 5 % (N 712) |

**Figur 3 och T30, CAR på D per händelse:**

- Tillägg, utan kontroller, 2007–26: lutning 1,23 (−2,33 till 4,78), p 0,50, N 174, R² 0,004.
- Tillägg, fasta effekter per översyn och kontroller, från 2007: lutning 0,65 (−5,03 till 6,32), N 165, MDE 8,0 (styrkan räcker inte, inget p-värde).
- Tillägg, fasta effekter per översyn och kontroller, från 2017: lutning 0,58 (−5,22 till 6,38), N 132, MDE 8,2 (styrkan räcker inte, inget p-värde).
- Borttag, utan kontroller, 2007–26: lutning 1,89 (−0,50 till 4,28), p 0,26, N 143, R² 0,021.
- Borttag, fasta effekter per översyn och kontroller, från 2007: lutning 2,89 (−0,09 till 5,86), N 133, MDE 4,2 (styrkan räcker inte, inget p-värde).
- Borttag, fasta effekter per översyn och kontroller, från 2017: lutning 2,42 (−0,28 till 5,13), N 101, MDE 3,8 (styrkan räcker inte, inget p-värde).

**Figur 1 och G&S figur 5:** medel-D per år och OMXSB-fondernas ägarandel (förmögenhet i december / indexets börsvärde vid årets sista översyn)

| År | D tillägg | D borttag | Fonder, mdkr | Index, mdkr | Ägarandel |
|---|---|---|---|---|---|
| 2007 | 0,00 | 0,00 | 3 | 4675 | 0,06 % |
| 2010 | 0,00 | 0,08 | 5 | 3948 | 0,12 % |
| 2013 | 0,13 | 0,17 | 10 | 4810 | 0,20 % |
| 2016 | 0,26 | 0,44 | 30 | 5879 | 0,52 % |
| 2019 | 0,70 | 0,68 | 45 | 7617 | 0,59 % |
| 2022 | 0,57 | 0,68 | 65 | 10459 | 0,62 % |
| 2025 | 1,20 | 1,26 | 181 | 13456 | 1,35 % |
| 2026 | 1,22 | 1,63 | 192 | 14903 | 1,29 % |

## Jämförelse med G&S (publicerade versionen)

| | USA (G&S) | Sverige (runda 11) |
|---|---|---|
| M, tillägg, totalt fönster, tidigt → sent | 6,75 → 0,37 (slutet av 1990-talet → 2010-talet) | 197 → 2,7 (2007–11 → 2022–26) |
| M med kontroller | 6,6 → 0,7 | 199 → 2,3 |
| M, långt fönster, med kontroller | 8,7 → 1,7 | 169 → 6,5 |
| Elasticitet i dag | −1,44 till −2,72 | cirka −0,4 |
| Indexfondernas ägarandel | cirka 7 % av börsvärdet | 1,3 % (2025–26) |
| Vem tar emot köpen | Andra institutioner (13F); aktiva fonder cirka 0 | Investerare utanför fonderna; aktiva fonder cirka 0 |
| Uppgång [AD−100, AD−1], tillägg | 9,6 % → 18,7 % | 12,1 % → 18,9 % |
| Sammansättning | Förklarar lite | Förklarar inget |
| Nyemissioner | Ingen större roll | Ingen skillnad mot kontroller |
| Köp mot prisrörelse per händelse | Inget stabilt samband (R² 2–6 %) | Inget samband (R² 0,4–2 %) |

## Förbehåll

- M är en kvot. Den utgår från att hela prisrörelsen beror på köpen. Beror en del på uppmärksamhet blir M för högt.
- D 2007–11 är litet och sämre täckt i LSEG; M_2007–11 är därför mycket osäkert.
- Händelser där aktien senare splittats är uteslutna (87 tillägg, 63 borttag), eftersom LSEG:s innehav är justerade för splittar men aktieantalet är historiskt.
- Utländska bolag noterade även i Stockholm (AstraZeneca, ABB) räknas med hela bolagets börsvärde. Om Nasdaq bara räknar aktierna noterade i Stockholm blir indexets börsvärde för stort och ägarandelen för låg. Det påverkar figur 5 och storlekskontrollen, inte M.
- Onormal omsättning har ett extremvärde (33,7 % per dag). Kontrollens koefficient vid tillägg (6,2, p 0,17) ska inte tolkas.
- LSEG täcker fonder, inte alla institutioner. "Utanför fonderna" betyder alla andra ägare.
