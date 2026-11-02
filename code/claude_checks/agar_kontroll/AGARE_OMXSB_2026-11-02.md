# Vilka fonder blir nya ägare efter tillägg (2 november 2026)

Beskrivande uppdelning av T9. Inte ett deklarerat test. Kod: `agar_omxsb.py`, körs från `code/claude_checks`.

## Bakgrund

En annan chatt rapporterade att ökningen i antal fondägare efter tillägg främst kommer från fonder med OMXSB i jämförelseindexet (118 tillägg: +9,9 fonder, varav 8,5 OMXSB-anknutna; +2,1 fondbolag). Koden fanns inte i repot. Här är den omräknad på vår data.

## Metod

- Urval, kvartal och regression som T9 och T14 (`runda4.py`): tillägg 2019–2026 mot nästan tillagda, kontroll för uppgång [AD−100, AD−1], log börsvärde och översyn. Klustrat på översyn, 95 % intervall med t(G−1).
- Utfall: förändring i antal fonder som äger aktieslaget, kvartalet före AD till första kvartalet minst 20 handelsdagar efter ED.
- Fonden klassas efter sin rad i `fi_all_funds_klass.csv` samma kvartal. "OMXSB i jämförelseindex": `jmf` innehåller stockholm benchmark, omxsb eller sbx.

## Resultat

108 tillägg med data, 1 009 kontroller, 15 översyner. Nya ägare per tillägg relativt kontrollerna:

| Fondgrupp | Skattning (95 % intervall) |
|---|---|
| Alla fonder | +15,4 (12,7 till 18,1) |
| OMXSB i jämförelseindex | +12,1 (10,5 till 13,8) |
| varav utan "index" i namnet | +7,7 (5,9 till 9,5) |
| varav utan "index" i namnet och inte bred indexfond | +2,1 (0,8 till 3,4) |
| varav aktiv risk över 1,5 | +2,7 (1,1 till 4,2) |
| Utan OMXSB i jämförelseindex | +3,3 (1,8 till 4,7) |
| Fondbolag, alla fonder | +2,1 (1,8 till 2,5) |

Skillnaden mot den andra chatten (108 mot 118 tillägg, +15,4 mot +9,9) kan inte förklaras utan deras kod. Riktningen, andelen OMXSB-fonder (79 mot 86 %) och antalet fondbolag stämmer.

## Vilka fonderna är

`nya_B_agare.csv` listar varje ny ägare med OMXSB i jämförelseindex. De utan "index" i namnet är främst Nordeas generationsfonder (50-tal till 90-tal, Senior), Institutionella Aktiefonden Sverige, Nordeas donationsfonder och KPA Blandfond. Deras svenska aktiedel följer OMXSB, och aktiv risk är låg eller saknas. Ett fondbolag med många sådana fonder räknas som många ägare men fattar ett beslut.

## Läsning

- Ökningen i antal fondägare efter tillägg är till cirka 80 % fonder med OMXSB i jämförelseindex, främst passiva fonder och blandfonder vars svenska aktiedel följer indexet. Räknat i fondbolag är ökningen cirka två.
- Rättelse av T9: "fler ägare även utan indexfonder" (+0,38) byggde på ett namnfilter som missar dessa fonder. Ökningen är mest passiva pengar, inte tecken på bredare uppmärksamhet.
- Nettoköpsmåttet (`nettokop.py`, 1,17 %) klassar fonder efter jämförelseindex och räknar redan med dessa fonder. Mängden köp ändras inte.
- Om aktiva OMXSB-fonder reagerar mer än aktiva fonder som jämför sig med hela börsen är fortfarande obesvarat (T14, stoppad för låg precision).
- Uppdelningen säger inget om hur mycket av prisuppgången ägarna orsakar.
