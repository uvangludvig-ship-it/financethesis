# Runda 4: T14, vilka fonder blir nya ägare

Deklarerad 1 november 2026, 22:55 CET. Inget i detta test har körts. Inga ägarutfall per fondgrupp har setts.

## Fråga

Efter ett tillägg äger fler svenska fonder aktien (T9). Kommer ökningen från fonder vars jämförelseindex ändras vid tillägget, eller också från fonder vars jämförelseindex inte ändras?

## Två tolkningar och vad de förutsäger

- **Jämförelseindex.** Aktiva fonder som jämför sig med OMXSB får aktien i sitt jämförelseindex vid tillägget och har skäl att köpa. Fonder som jämför sig med hela börsen (SIX Portfolio Return Index, SIXRX, OMXSGI, OMXSPI) hade redan aktien i sitt index. För dem ändras inget. Förutsägelse: ökningen finns i grupp B, inte i grupp H.
- **Något som inte går via jämförelseindex** (uppmärksamhet, likviditet, bevakning). Förutsägelse: ökning också i grupp H.
- Båda kan gälla samtidigt.

## Kända resultat före detta test

- T9 (runda 2, hela FI-filen, 2019–2026), förändring i log(1 + antal fonder som äger aktien), tillägg minus nästan tillagda: alla fonder +0,35 (0,28 till 0,41); utan indexfonder (namnfilter) +0,38 (0,30 till 0,47). Borttag: −0,22 (−0,33 till −0,10) och −0,29 (−0,43 till −0,14).
- Första steget v2: indexfonderna köper i median 0,2–0,8 % av indexslagets aktier.
- T10: pris mot fondernas köp har breda intervall.
- Antal fonder per kvartal (räknat 22:48 ur `fi_all_funds_klass.csv`, inga utfall): ungefär 10 rena aktiva fonder med OMXSB som jämförelseindex och ungefär 30 rena med hela börsen, därtill blandfonder.

## Data och urval

- FI-innehav 2018Q4–2026Q2, alla 31 kvartal (`fi_all_holdings.pkl`, `fi_all_funds_klass.csv`).
- Urval som T9: tillägg och borttag samt nästan tillagda och nästan borttagna från runda 2 (`T5urval_T7_T8b_events.csv`), AD från 2019-01-01.
- ISIN från `td_universe.csv` och `stocks_static_2005.csv` som i T9. Ett ISIN används bara om det finns i FI senast kvartalet före.
- Kvartal före: sista kvartalsslut före AD. Kvartal efter: första kvartalsslut minst 20 handelsdagar efter ED.

## Steg 0: kontroll av datakedjan

T9 körs om med samma definitioner på den här FI-inläsningen. Skattningarna för tillägg (alla fonder, utan indexfonder) ska ligga inom ±0,03 från de kända (+0,35 och +0,38). Annars stopp: datakedjan skiljer sig från runda 2.

## Fondgrupper

Bestäms per händelse vid kvartalet före. Villkor för båda grupperna:
- fonden finns i FI både kvartalet före och kvartalet efter;
- fonden äger kvartalet före minst 10 olika värdepapper med ISIN som börjar på SE (Antal > 0);
- fonden är inte indexfond: inte "bred" enligt första steget, och namnet innehåller inte index, indexnära, exponering, etf, xact, passiv eller access.

Grupper:
- **B:** jämförelseindex innehåller OMXSB-familjen (stockholm benchmark, omxsb, sbx).
- **H:** jämförelseindex innehåller hela börsen (SIX Portfolio Return, SIXPRX, SIXRX, SIX Return, OMXSGI, OMXSPI, all share) och inte OMXSB-familjen.

## Utfall

För varje aktie och grupp g: Δandel_g = andelen fonder i g som äger aktieslaget kvartalet efter minus andelen kvartalet före, i procentenheter. Nämnaren är de fonder som uppfyller villkoren ovan.

## Skattning

Samma regression som T9: utfallet på en händelsedummy, uppgång [AD−100, AD−1], log börsvärde och fasta effekter per översyn. Klustrat på översyn. p från restriktiv wild cluster bootstrap, 95 % intervall med t(G−1).

Skattningar, tillägg 2019–2026:
- **E_H** (primär): tillägg minus nästan tillagda, utfall Δandel_H.
- **E_D** (primär): utfall Δandel_B − Δandel_H per aktie, tillägg minus nästan tillagda.
- E_B: utfall Δandel_B.
- E_BH: utfall Δandel bland alla fonder i B och H. Motsvarar det kända T9-resultatet och används som skala.

Borttag skattas på samma sätt och redovisas som sekundärt.

## Steg 1: styrkekontroll innan skattningarna visas

Koden skriver först bara standardfel och minsta upptäckbara effekt för E_H och E_D, MDE = (t(0,975; G−1) + t(0,80; G−1)) × SE, samt E_BH.

Testet räknas som informativt om båda gäller:
- MDE för E_D ≤ E_BH, alltså kan testet upptäcka en skillnad mellan grupperna lika stor som hela ökningen;
- MDE för E_H ≤ 0,5 × E_BH, alltså kan testet upptäcka om fonderna i H står för minst halva ökningen.

Om villkoren inte uppfylls stoppar koden. E_H, E_B och E_D skrivs inte ut, och fördjupningen väljs bort.

## Tolkning, tillägg

- E_H med undre gräns över 0: fonder vars jämförelseindex inte ändras blir också ägare. Ökningen i antal ägare kan då inte helt förklaras av jämförelseindex.
- E_D med undre gräns över 0: fonder med OMXSB som jämförelseindex blir ägare i större utsträckning. Det är förenligt med efterfrågan från jämförelseindex.
- Ett intervall som innehåller 0 betyder "inte påvisat", inte "uteslutet".
- Testet gäller ägande, inte pris. Det säger vilka fonder som blir ägare, inte varför priset stiger.

## Känslighet, efter de primära skattningarna

- Bara fonder med ett enda jämförelseindex.
- Utfall i antal: förändring i log(1 + antal fonder i g).

## Kända svagheter

- Jämförelseindex i FI är fondens egen uppgift och kan vara fel.
- Grupp B är liten.
- Kvartalsdata: köp syns bara som innehav vid kvartalsslut.
- Fonder i H kan köpa av andra skäl som hör ihop med tillägget. Ett positivt E_H betyder "inte via jämförelseindex", inte bevisad uppmärksamhet.

## Körning

Ingen testkörning. Koden körs en gång på hela underlaget i ordningen steg 0, steg 1, steg 2. Om ett steg stoppar redovisas det.

## Utfall av körningen, 22:56 CET

- Steg 0 godkänt: T9 återskapat, tillägg +0,345 (alla fonder) och +0,385 (utan indexfonder), mot kända +0,35 och +0,38.
- Steg 1 stoppade: MDE för E_D 5,01 procentenheter mot gränsen E_BH = 3,23. MDE för E_H 1,02 mot gränsen 1,61. Båda villkoren krävdes. E_H, E_B och E_D har inte skattats. Regeln ändras inte i efterhand.
