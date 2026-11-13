# Rättelser 3 november 2026

**Detta dokument gäller före `RESULTAT_2026-11-02.md` och `runda11_resultat/RESULTAT_runda11.md` där de skiljer sig.** Plan: `rattelser_2026-11-03_plan.md` (skriven 15:21:30, innan något kördes). Kod: `rattelser_2026-11-03.py`, körd 15:22. Data: `rattelser_2026-11-03_resultat/`. Allt är explorativt: resultaten från runda 11 och den andra chattens granskning (commit 2eedada) var kända.

## 1. Vad som nu gäller

| Påstående | Tidigare | Nu |
|---|---|---|
| M i dag | 2–5 | **Oförändrat.** 2017–26: 2,3–5,1 i totalt fönster, 6–7,5 i långt fönster. |
| M föll från cirka 200 till 2 | p 0,055 | **Inte visat.** Med rättat D bygger 2007–11 på 6 tillägg: M cirka 96 (−27 till 247); skillnaden mot i dag p 0,18 utan och p 0,39 med kontroller. |
| M var mycket högre tidigt | – | **Sannolikt, men osäkert.** Med förväntat D från SHoF (33 tillägg): M 2007–11 cirka 129 (57 till 224), troligen för högt (avsnitt 3). |
| Indexköpen växte 10–20 gånger | T24, LSEG | **Fondernas ägarandel av indexet växte från 0,06 % (2007) till 1,3 % (2025–26) enligt SHoF.** LSEG:s tidiga köp är för dåligt mätta för att ge en egen siffra. |
| T29: 125 miljoner kronor per år | uppmätt kostnad | **Villkorat räkneexempel**, cirka 90–100 miljoner per år 2022–25 (avsnitt 5). |
| Säljarna finns utanför fonderna | runda 11 | Oförändrat, 2017–26, där D är väl mätt. |

## 2. D, indexfondernas köp

**Felet.** När ingen OMXSB-indexfond rapporterade kring en händelse blev köpen 0. Då blir D för litet och M för stort.

**Rättelse.** D sätts till saknat när ingen OMXSB-indexfond rapporterar både före AD (inom 120 dagar) och efter ED (inom 45 dagar). Rapporterar en sådan fond men äger inte aktien är D = 0 som förut. Det gäller 5 tillägg och 3 borttag, alla 2007–11; övriga perioder påverkas inte.

**Kvar, går inte att rätta:** fonderna klassas efter dagens namn i LSEG. Kontroll mot FI-innehaven finns bara för 2019–26 (korrelation 0,91, runda 9). Händelser där aktien senare splittats är fortfarande uteslutna.

## 3. M per period, tillägg, totalt fönster [AD−1, ED+1]

Intervall från bootstrap över översyner, med alla dragningar.

| Mått på D | 2007–11 | 2012–16 | 2017–21 | 2022–26 |
|---|---|---|---|---|
| LSEG, rättat D | 96 (−27 till 247), N 6 | −9 (−36 till 5), N 27 | 5,1 (1,6 till 11,4), N 58 | 2,7 (0,7 till 4,8), N 78 |
| LSEG, som runda 11 | 197 (58 till 1 252), N 11 | −9 (−35 till 5), N 27 | 5,1 (1,5 till 11,5), N 58 | 2,7 (0,7 till 4,7), N 78 |
| Förväntat D (SHoF) | 129 (57 till 224), N 33 | 1,0 (−13 till 16), N 54 | 7,0 (3,9 till 12,8), N 82 | 2,2 (0,4 till 4,0), N 87 |

- **Förväntat D** = aktiens fria flytande andel × OMXSB-fondernas ägarandel av indexet samma år. Det beror inte på LSEG:s rapporter, så alla tillägg kan användas.
- Förväntat D blir troligen för litet, eftersom indexets börsvärde är för stort: några utländska bolag (AstraZeneca, ABB, Sampo, Stora Enso) räknas med hela sitt globala börsvärde. För 2017–26, där båda måtten finns, är förväntat D 20–40 % lägre än LSEG:s. Rättat för det blir M 2007–11 med SHoF cirka 80–100.
- Fonder som följer index internt, till exempel pensionsbolag, saknas i båda källorna.

**Läsning.** M var sannolikt mycket högre 2007–11 än i dag, troligen 50–200, men nivån är osäker. Med rättat LSEG-D är skillnaden inte statistiskt säkerställd. I dag är M 2–5 i totalt fönster. **Använd inte "M föll från 200 till 2" i uppsatsen.**

**Tabell 6 med rättat D, tillägg** (`tabell6_rattad.csv`):
- Totalt fönster med kontroller: M 2007–11 80 (−43 till 203), 2022–26 2,3 (0,9 till 3,8); skillnad 77 (−45 till 200), p 0,39.
- Långt fönster med kontroller: 136 (96 till 175) och 6,6 (3,7 till 9,5); skillnad 129 (88 till 169), p 0,10.
- 2017–21 mot 2022–26: ingen skillnad i något fönster.

**Borttag:** med rättat D bygger 2007–11 på 7 borttag och M blir cirka −1; med SHoF 92 (35 till 200). För borttag går det inte att säga något om förändringen.

## 4. Indexfondernas ägarandel (oberoende av LSEG)

OMXSB-fondernas förmögenhet i december (SHoF) / indexets börsvärde vid årets sista översyn:

| 2007 | 2010 | 2013 | 2016 | 2019 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| 0,06 % | 0,12 % | 0,20 % | 0,52 % | 0,59 % | 0,62 % | 1,35 % |

Ägarandelen har vuxit ungefär 20 gånger. Nivåerna är troligen något för låga (samma förbehåll om indexets börsvärde), men tillväxten påverkas lite.

## 5. T29, kostnaden för indexsparare

Inga nya beräkningar. Den andra chattens granskning (`output/omxsb_execution_followup_20261102/cost_audit/REPORT.txt`) återskapade T29 exakt och visade tre problem:
1. **Vikterna är osäkra.** Medlemslistan innehåller avnoterade bolag, Skanska B och Tele2 B saknar data, och utländska bolag räknas med globalt börsvärde (Sampo 180–250 gånger, Stora Enso 7–12 gånger det som är noterat i Stockholm).
2. **Fondförmögenheten var fel daterad.** December samma år användes även för besked i maj.
3. **Tolkningen.** Räkningen förutsätter att hela premien mellan besked och handelsdag beror på fonderna och hade gått att undvika. Den andra chattens handelstest visar att aktierna efter beskedet inte steg säkert mer än jämförbara aktier: +0,83 (−0,41 till 2,07).

**Så ska T29 redovisas:** som ett villkorat räkneexempel. Om vikterna stämmer och hela premien beror på fonderna, blir kostnaden 10,3 baspunkter per år 2022–25, det vill säga 103 kronor per 100 000 kronor, eller cirka 89 miljoner kronor per år med fondförmögenheten före beskedet (9,4 baspunkter i snitt 2008–25). Om halva premien beror på fonderna halveras beloppen. Det är ingen uppmätt förlust och ingen statistisk gräns.

## 6. Den andra chattens nya test (commit 2eedada)

Köp aktien dagen efter beskedet, behåll den till dagen före genomförandet:
- tillägg 2017–25: +2,31 (1,09 till 3,54) mot börsindex, 165 tillägg;
- samma 143 tillägg mot våra kontrollaktier: +0,83 (−0,41 till 2,07); 2021–25: +0,24 (−1,01 till 1,49).

Läsning: priset anpassar sig vid beskedet. Efteråt finns ingen säker extra uppgång som är unik för indexaktierna. Det passar med T22.

Samma granskning följde två fasta fonder (Storebrand Sverige och Robur Access Sverige) i FI 2019–25: deras köp vid tillägg var oförändrade, 0,432 % mot 0,429 % av bolagsvärdet.

## 7. Formuleringar som ska undvikas

| Undvik | Skriv i stället |
|---|---|
| Indexfonderna köpte nästan inget 2007–11, så de drev inte den tidiga effekten | Fondernas ägarandel var liten (cirka 0,1 %), men köpen per händelse är osäkert mätta; om de drev den tidiga effekten går inte att avgöra |
| M föll från 200 till 2 | M var sannolikt mycket högre tidigt; i dag är M 2–5 |
| Nästan alla nya fondägare är OMXSB-fonder | Cirka 78 % av de nya fondägarna |
| Aktieslagen rör sig lika | Aktieslagen rör sig ungefär lika; en effekt bara i det köpta slaget på 3–5 % kan uteslutas |
| Fonderna köper på handelsdagen | Fonderna köper mellan besked och genomförande; omsättningen samlas dagen före genomförandet |
| Kursen stiger 2–5 % per köpt procent | M, kvoten mellan kursrörelse och köp, är 2–5 |
| Indexsparare betalar 125 miljoner per år | Ett villkorat räkneexempel ger cirka 90 miljoner per år 2022–25 |
| Effekten finns kvar eftersom migrationer saknas | Migrationer saknas, vilket är förenligt med att effekten finns kvar |

## Filer

- `rattelser_2026-11-03_plan.md`, `rattelser_2026-11-03.py`, `rattelser_2026-11-03_logg.txt`
- `rattelser_2026-11-03_resultat/`: `M_per_period.csv` (alla mått, fönster och perioder, tillägg och borttag), `tabell6_rattad.csv`, `handelser_rattade.csv`
