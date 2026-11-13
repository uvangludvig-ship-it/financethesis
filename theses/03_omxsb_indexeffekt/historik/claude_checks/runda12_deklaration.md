# Runda 12: förväntat D mot uppmätt D, och ett kalibrerat tidigt M

Skriven 2026-11-03 17:13:09 CET (tid från `date` på datorn). Ska committas till git innan något räknas. Explorativt.

## Varför
Uppmätt D (LSEG, rättat 3 nov) finns bara i 4 av 9 tidiga översyner (2009H1, 2009H2, 2011H1, 2011H2). I de andra fem rapporterade ingen OMXSB-indexfond. XACT OMXSB:s rapporter för 2007–2011 finns inte på nätet.

## Kraftkontroll, gjord före körningen och bara på redan kända tal
- Med de 4 översynerna är redan CAR osäker: medel av översynsmedel 7,8 (−8,2 till 23,8; t med 3 frihetsgrader, 18 tillägg). Med alla 9 översyner: 8,0 (2,4 till 13,5; 33 tillägg). Inget rättat D i de 4 översynerna kan alltså ge ett tidigt M skilt från noll. Därför rättar vi inte de 12 split-händelserna.
- Matchade tillägg (utan split, både D_ny och D_shof finns): 2007–11: 6 (4 översyner); 2012–16: 27 (8); 2017–21: 58 (10); 2022–26: 78 (9).
- Redan kända resultat som jag har sett: M med förväntat D 2007–11 = 129 (57 till 224) och periodmedel för båda D-måtten på olika urval (`rattelser_2026-11-03_resultat/M_per_period.csv`). Kvoten mellan måtten på matchade händelser är inte räknad.

## Data
`rattelser_2026-11-03_resultat/handelser_rattade.csv`, bara tillägg. D_ny = uppmätt D (saknat utan rapporterande indexfond). D_shof = fri flytande andel × fondernas ägarandel av indexet (SHoF). Fönster y_tot. Inga nya data, ingen ändrad regel.

## Mått
- R_p = medel(D_ny) / medel(D_shof) på matchade tillägg i period p. Intervall: översyner dras med återläggning (som `kvot_ci`), B = 9999, frö 20261103, percentil 2,5 och 97,5.
- Kalibrerat tidigt M: M_kal = M_shof(2007–11) / R(2012–16). M_shof på alla tillägg 2007–11 med y_tot och D_shof (33 tillägg, 9 översyner). Översyner dras oberoende i de två perioderna.

## Huvudtest (H12)
M_kal − M_LSEG(2022–26), där M_LSEG(2022–26) är rättat M utan split (2,65 i M_per_period.csv). Översyner dras oberoende i de tre urvalen. Ett intervall över noll betyder att M är högre tidigt med det kalibrerade måttet. Innehåller intervallet noll är fallet inte visat och inte uteslutet.

## Sekundärt
- R för 2007–11 (6 tillägg), 2017–21, 2022–26 och alla perioder.
- M_kal med R från 2007–11 i stället för 2012–16.
- Samma sak i fönstret y_lang.
- Beskrivande: korrelation mellan log D_ny och log D_shof på matchade tillägg.

## Antaganden och gränser
- Förhållandet mellan uppmätt och förväntat D antas vara detsamma 2007–11 som 2012–16. Fondmixen ändrades (XACT OMXSB dominerade tidigt), så det är ett antagande.
- D_shof är beräknat, inte observerat.
- Detta ersätter inte huvudmåttet från 3 nov. Det rättade LSEG-M för 2007–11 (95,7; −27 till 247) förblir huvudmåttet och redovisas först.
- M visar samband, inte orsak. Ett tidigt M runt 100 är svårt att tolka eftersom D är nästan noll.
- Detta är tredje sättet att skatta det tidiga M (LSEG, långt fönster, SHoF). Alla tre redovisas.
