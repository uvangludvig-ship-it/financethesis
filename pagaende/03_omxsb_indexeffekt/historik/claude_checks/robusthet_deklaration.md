# Robusthetstest, deklarerade 2026-11-01 19:06 CET, innan de körs

Görs efter att del 1, del 2 och tilläggsanalyserna A–D setts. Redovisas som robusthet, inte som förhandsspecificerade huvudtest.

## Gemensamt

- Onormal avkastning mot .OMXSBGI (`common.py`). Fönster [AD−1, ED+1] om inget annat sägs.
- Period: "före" = AD 2007–2016 (20 översyner), "efter" = AD 2017–2026 (19 översyner).
- Inferens: medel per översyn med teckenbyte (20 000 dragningar) och wild cluster bootstrap på översyn (9 999 dragningar, Rademacher om G ≥ 12, annars Webb). Frö 20261101.
- Tecken: +1 för tillägg, −1 för borttag, där det står "signerad".

## T1. Pseudohändelser

- För varje verklig händelse i översyn k: samma aktie med AD och ED från översyn k−1 ("före") och k+1 ("efter").
- Tas bort om aktien har en verklig händelse i pseudoöversynen eller saknar avkastning i fönstret.
- Mått: CAR [AD−1, ED+1] med pseudodatum, per typ, period och riktning. Dessutom parvis skillnad verklig minus pseudo-före, klustrad på den verkliga översynen.
- **Primärt:** tillägg efter 2017, pseudo-före.
- **Tolkning bestämd i förväg:** är pseudo-före minst hälften av den verkliga effekten (≥ 1,25 %) och signifikant på 5 %, förklarar momentum en stor del. Är den nära noll och skillnaden verklig minus pseudo signifikant, är effekten knuten till händelsen.

## T2. Matchad kontroll

- Pool: panelens 186 aktier. Hela LSEG-panelen ligger i Git LFS och är inte tillgänglig här, så testet körs om lokalt på hela panelen med samma skript.
- Kandidater för händelse i översyn k: inga verkliga händelser i översyn k−1, k eller k+1; inte samma bolag (samma rot i RIC); komplett avkastning över [AD−100, ED+1]; börsvärde (bolagsnivå) finns på eller före AD−1.
- Matchningsvariabler: uppgång = marknadsjusterad CAR [AD−100, AD−1], storlek = log börsvärde vid AD−1. Båda standardiseras inom översynen (händelser och kandidater). Närmaste granne efter euklidiskt avstånd, med återläggning.
- Mått: händelsens CAR minus kontrollens CAR, båda [AD−1, ED+1].
- **Primärt:** tillägg efter 2017, en kontroll. **Robusthet:** medel av tre närmaste kontroller; borttag; perioden före.

## T3. Asymmetri mellan tillägg och borttag

- Signerad CAR s = tecken × CAR.
- Per period: s = a + b·Tillägg. b = tilläggseffekt minus borttagseffekt i absoluta termer.
- Hela perioden: s = a + b·Tillägg + c·Efter + d·Tillägg×Efter. d = om asymmetrin ändrades.
- Kluster på översyn. p-värde från wild cluster bootstrap med nollhypotesen påtvingad (restriktiva residualer).
- **Primärt:** b efter 2017, [AD−1, ED+1]. **Sekundärt:** d; samma sak för [ED, ED+20]; Mid Cap som jämförelseindex.

## T4. Multiplikator för indexslaget med samma urval i täljare och nämnare

- Urval: de 39 slutliga tvillinghändelserna som också har FI-data. Det är 19 händelser 2019–2026. De övriga 5 av FI:s 24 föll bort på de i förväg låsta reglerna.
- Efterfrågan d = tecken × indexfondernas förändring i indexslaget, % av slagets aktier (`twin_first_stage_output.csv`).
- Spread y = signerad skillnad indexslag minus systerslag, [AD−1, ED+1].
- **Primärt:** M = medel(y) / medel(d). 95 % intervall från bootstrap över bolag (10 000 dragningar, percentil).
- **Sekundärt:** y = α + β·d, kluster på bolag, wild bootstrap (Webb om färre än 12 bolag).
- **Beskrivande:** indexslagets CAR mot marknaden delat med d.

# Tillägg 2026-11-01 19:23 CET, innan de körs: T2 på hela panelen och T5 nästan tillagda

Körs lokalt av Ludvig med `robusthet_hela_panelen.ipynb` på `stocks_daily_2005.parquet`. Gemensamma regler som ovan. Varje skattning redovisas med 95 % intervall (klustrat medel per översyn ± t(G−1) · SE).

## T2-hela. Matchad kontroll på hela panelen

Exakt som T2, men poolen är alla aktier i hela panelen i stället för 186.

## T5. Nästan tillagda aktier

- Medlemmar före översyn k: `members_after` för översyn k−1 i `output/omxsb_replication_2007/mechanisms/omxsb_membership_by_review.csv`. Medlemmar som bara finns som ticker (T:) kopplas till RIC via `TickerSymbol` i `td_universe.csv`.
- Kandidater i översyn k: aktier som inte är medlemmar före k och inte läggs till i k. Samma uteslutningar som T2: ingen verklig händelse i k−1, k eller k+1; inte samma bolag som en händelseaktie i k; komplett avkastning över [AD−100, ED+1]; börsvärde vid AD−1. En rad per bolag: aktieslaget med högst handelsvärde över [AD−120, AD−1].
- **Nästan tillagd:** kandidat vars börsvärde vid AD−1 är minst lika stort som det minsta tillägget i samma översyn.
- **Primärt:** tillägg efter 2017. Tillägg och nästan tillagda i samma regression: CAR [AD−1, ED+1] = b·Tillägg + c·uppgång [AD−100, AD−1] + d·log börsvärde + fasta effekter per översyn. Kluster på översyn, restriktiv wild cluster bootstrap för b.
- **Sekundärt:** skillnaden tillägg minus nästan tillagda per översyn (teckenbyte, wild bootstrap); perioden före 2017; borttag, där nästan borttagna är medlemmar före k som inte tas bort och vars börsvärde är högst lika stort som det största borttaget i översynen.
- **Tolkning bestämd i förväg:** övre gränsen för b under 1,25 (halva den råa effekten) betyder att det mesta är urval. Nedre gränsen över 0 betyder att en indexeffekt finns kvar. Annars går det inte att avgöra.

## Tillägg 19:26 CET: datafel

En testkörning av koden på utdraget med 186 aktier (för att kontrollera att T2-hela återskapar T2 exakt, vilket den gör) visade dagsavkastningar på miljontals procent för Eniro 2005–2008, ett justeringsfel i LSEG-panelen. Regel: en dagsavkastning över 1 000 % sätts till saknad. Testkörningen gav också siffror för T5 på utdraget. De har setts, men utdraget är inte det deklarerade urvalet. Det är hela panelen som gäller.
