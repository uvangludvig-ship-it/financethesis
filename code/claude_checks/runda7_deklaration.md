# Runda 7: varför stiger priset? (T22 hopptest, T23 asymmetri)

Deklarerad 2 november 2026, 13:55 CET.

## Tre förklaringar och vad de förutsäger

| | Fondernas köp | Uppmärksamhet | Urval |
|---|---|---|---|
| När priset rör sig | Vid beskedet (köpen förutses) och dagen före ändringen (köpen sker) | Vid beskedet | Jämnt över tiden, som en fortsatt trend |
| Efter ändringen | Tillfälligt tryck går tillbaka; varaktig efterfrågan består | Består | Trenden fortsätter |
| Borttag | Spegelbild av tillägg | Svagare och kortare än tillägg: man glömmer inte ett bolag man lärt känna (Chen, Noronha och Singal 2004) | Spegelbild |
| Ägare | Indexfonder | Fler ägare också utanför indexfonderna | Inget särskilt |
| Två aktieslag | Det köpta slaget stiger mer, om inte arbitrage jämnar ut | Båda slagen | Båda slagen |

Redan kända resultat som bär på tabellen: återgång efter ändringen före 2017 men inte efter (Del 1); kontrollgrupper med jämförbar uppgång och jämförbar ställning enligt Nasdaqs regel (T12, T13); tvillingarna (T15, T18); ingen ökning i omsättning efter tillägg (T8b); ägaruppdelningen (avsnitt 4 i RESULTAT_2026-11-02).

## T22. Hopptest mot urval (deklarerat innan något setts)

**Fråga.** Kommer överavkastningen på de dagar då något händer, eller jämnt fördelad som en trend?

**Data.** `data/panel_utdrag.csv.gz`, som täcker alla OMXSB-händelser i `events_car.csv`. Daglig överavkastning mot .OMXSBGI. Borttag som Ludvigs steg 1 flaggar utesluts.

**Mått per händelse.** Händelsedagar H = {AD, AD+1, ED−1}. Övriga dagar = [AD−20, ED+20] utom H. J = medel av överavkastningen på H minus medel på övriga dagar. Krav: värde på alla dagar i H och på minst 80 % av övriga dagar.

**Förutsägelse.** Rent urval (en trend som ändå skulle ha fortsatt) ger J = 0. Händelsedriven effekt ger J > 0 för tillägg och J < 0 för borttag.

**Primärt.** Tillägg efter 2017 (AD ≥ 2017-01-01): medel av J, skattat som konstant, klustrat på översyn, p från wild cluster bootstrap.

**Sekundärt.** Borttag efter 2017; tillägg före 2017; J uppdelat på beskedsdagarna {AD, AD+1} och handelsdagen {ED−1}; genomsnittlig överavkastning per händelsedag (profil, beskrivande).

**Styrkevillkor (steg 1, bara N, G, SE, MDE).** Primärt körs om MDE ≤ 0,5 procentenheter per dag. Motivering: en effekt på cirka 2 % fördelad på tre händelsedagar är cirka 0,7 per dag.

**Tolkning, bestämd i förväg.** Undre gräns över 0: överavkastningen är koncentrerad till händelsedagarna och kan inte vara enbart en fortsatt trend. Det talar emot urval som enda förklaring men skiljer inte köp från uppmärksamhet. Intervall som innehåller 0: urval kan inte avvisas med detta test.

**Begränsning.** Om Nasdaqs val i sig avslöjar något om bolaget, är det en effekt av beskedet och syns på AD. Testet skiljer inte det från uppmärksamhet.

## T23. Asymmetri mellan tillägg och borttag (explorativt)

Komponenterna är redan sedda: tillägg efter 2017 mot nästan tillagda vid ED+20 +2,24, borttag −0,70 (runda 2); fondägare utanför OMXSB-fonderna +3,3 vid tillägg och +0,1 vid borttag (ägaruppdelningen). Testet är därför explorativt och redovisas så.

- **T23a.** Summan b_tillägg + b_borttag för CAR [AD−1, ED+20] och [AD−1, ED+1], med samma urval och kontroller som runda 2 (`T5urval_T7_T8b_events.csv`, efter 2017). Skattas i en regression med typspecifika kontroller och fasta effekter per översyn × typ. Klustrat på översyn. Summa över 0 betyder att tilläggens effekt är större eller varaktigare än borttagens, vilket uppmärksamhetsförklaringen förutsäger.
- **T23b.** Summan av effekterna på antal fondägare utanför OMXSB-fonderna, tillägg plus borttag, med standardfel från de två skattningarna (oberoende urval). Symmetrisk efterfrågan ger summan 0.

**Tolkning.** Asymmetri är förenlig med uppmärksamhet men bevisar den inte. Borttag kan också ha andra orsaker (svaga bolag, köpare som väntar ut säljtrycket).

## Utfall (körd 2 november ca 14:00)

**Steg 1.** T22: N 170, G 19, SE 0,112, MDE 0,33 ≤ 0,5. Godkänt.

**T22, överavkastning per dag på händelsedagarna {AD, AD+1, ED−1} minus övriga dagar i [AD−20, ED+20]:**

| | J (95 % intervall) | p | N | Händelsedagar | Övriga dagar |
|---|---|---|---|---|---|
| **Tillägg efter 2017 (primär)** | **+0,43 (0,20 till 0,67)** | **0,003** | 170 | +0,51 | +0,08 |
| Borttag efter 2017 | −0,42 (−0,69 till −0,14) | 0,003 | 131 | −0,43 | −0,01 |
| Tillägg före 2017 | +0,92 (0,31 till 1,52) | 0,005 | 89 | +0,93 | +0,01 |

Uppdelat, efter 2017:

| | Beskedet {AD, AD+1} | Handelsdagen {ED−1} |
|---|---|---|
| Tillägg | +0,48 (0,03 till 0,94) | +0,33 (−0,41 till 1,07) |
| Borttag | −0,69 (−1,11 till −0,27) | +0,13 (−0,59 till 0,86) |

**Enligt regeln bestämd i förväg:** undre gränsen ligger över 0. Överavkastningen är koncentrerad till händelsedagarna, främst beskedet, och kan inte vara enbart en fortsatt trend. Det talar emot urval som enda förklaring. Det skiljer inte köp från uppmärksamhet. Efter 2017 syns inget säkert hopp på handelsdagen. Profilen per dag finns i `runda7_resultat/T22_profil.csv`.

**T23, explorativt (komponenterna sedda i förväg):**
- T23a, summan b_tillägg + b_borttag: [AD−1, ED+1] +0,11 (−1,63 till 1,85); [AD−1, ED+20] +1,54 (−0,79 till 3,86). Ingen säker asymmetri i priset.
- T23b, fondägare utanför OMXSB-fonderna: +3,39 (1,06 till 5,71). Tillägg ger cirka tre nya ägare utanför OMXSB-fonderna; borttag tar inte bort några. Förenligt med uppmärksamhet, men litet och explorativt.
