# T18: tvillingaktier vid MSCI-ändringar

Deklarerad 2 november 2026, 09:30 CET. Inga kurser, avkastningar eller volymer för dessa händelser har setts. Underlaget hittills är bara MSCI:s ändringslistor.

## Varför

A/B-testet på OMXSB kan inte skilja köptryck från en effekt på hela bolaget. Indexfonderna köper bara 0,2–0,8 % av aktierna, så den förväntade skillnaden mellan aktieslagen är mindre än vad testet kan upptäcka. MSCI-ändringar handlas av globala indexfonder och ETF:er, och tidigare studier hittar 3–5 % kursrörelse vid MSCI-tillägg i utvecklade marknader. MSCI bedömer varje aktieslag för sig: att ett slag tas med eller tas bort påverkar inte automatiskt bolagets andra slag (MSCI, Select Summary of GIMI Methodology, april 2010).

## Kända resultat före testet

- OMXSB-tvillingar, rensade: +0,33 (−0,47 till 1,16), 39 händelser i 13 bolag.
- OMXSB-tvillingar där bara indexslaget köps (T15): +0,70 (−0,85 till 2,38), 18 händelser i 8 bolag.
- OMXS30-tvillingar (T11): +1,01 (−0,89 till 2,73), 7 händelser.

## Underlag

- MSCI:s publika ändringslistor för MSCI Sweden (Standard, `STPublicList`) och MSCI Sweden Small Cap (`SCPublicList`), februari 2007 till augusti 2026, hämtade 2 november 09:17–09:28. 79 av 80 listor hittades (småbolagslistan för februari 2007 saknas). Samlade i `msci_sweden_changes_2007_2026.csv`, 523 ändringar.
- Kandidater: `msci_tvilling_kandidater.csv`, 41 händelser där ett aktieslag ändras och bolagets andra slag är noterat i Stockholm men inte ändras i samma översyn. 26 gäller MSCI Standard och 15 MSCI Small Cap.
- Kurser: LSEG, dagliga stängningskurser, totalavkastning och volym för båda aktieslagen, 2006–2026 (`msci_lseg_CodeBook.ipynb`).

## Händelsedatum

- AD: tillkännagivandedagen på listan. MSCI publicerar efter stängning i Europa, så första reaktionen kan komma AD+1.
- ED: första handelsdagen efter den dag som anges som "as of the close of". Indexfonderna handlar vid stängning dagen före ED. Det motsvarar definitionen för OMXSB.

## Uteslutningar, beslutade innan kurserna ses

1. Systerslagets MSCI-status går inte att fastställa från listorna (Klövern A 2015).
2. Bolaget har en OMXSB- eller OMXS30-ändring, i något aktieslag, vars fönster [AD−1, ED+1] överlappar MSCI-händelsens fönster.
3. Rensningsreglerna R1–R4 från `ab_deklaration.md`, oförändrade: samma källa för båda slagen (R1), toppar som går tillbaka (R2), ojusterade bolagshändelser (R3) och stillastående systerslag, mer än hälften av dagarna utan prisändring i [AD−60, ED+20] (R4).
4. Färre än 20 placebofönster.

## Mått

Skillnaden i logavkastning mellan det ändrade aktieslaget och systerslaget, [AD−1, ED+1], med tecknet vänt för borttag (även flytt från Standard till Small Cap). Totalavkastning där den finns, annars pris, enligt samma regel som A/B-revisionen.

## Skattningar

- **Primär:** medel över MSCI Standard-händelserna.
- Sekundära: Standard-händelser där systerslaget ligger utanför MSCI; Small Cap-händelser; alla händelser.
- Inferens: placebofönster för samma bolag, samma längd, start inom ±45 dagar från AD:s dag på året under andra år, utan överlapp med bolagets andra index-händelser (MSCI, OMXSB, OMXS30) ±60/20 dagar. Intervall och p som i A/B-revisionen.

## Steg 1: första steget och styrka, innan skattningen visas

Koden skriver först:
- **Första steget:** onormal omsättning på dagen före ED (log volym mot medianen i [ED−60, ED−21]), det ändrade slaget minus systerslaget, med intervall. Det visar om handeln vid MSCI-ändringen faktiskt hamnar i det ändrade slaget.
- **Styrka:** minsta upptäckbara effekt för den primära skattningen, från placebofördelningen (80 % styrka, 5 % nivå).

Testet körs bara om:
- minst 15 Standard-händelser finns kvar efter uteslutningarna;
- första stegets undre gräns ligger över 0;
- minsta upptäckbara effekt är högst 2,0 procentenheter, det vill säga 60 % av en typisk MSCI-tilläggseffekt i utvecklade marknader (cirka 3,4 %).

Annars stopp, och skattningen visas inte.

## Tolkning

- Undre gräns över 0: prisrörelsen är koncentrerad till det aktieslag som indexfonderna handlar. Det talar för köptryck som inte fullt sprids mellan aktieslagen.
- Intervall nära 0 med liten övre gräns, samtidigt som båda slagen rör sig mot marknaden: rörelsen delas mellan aktieslagen. Det är förenligt med en effekt på hela bolaget eller med arbitrage mellan slagen, och testet skiljer inte dessa åt.
- Båda slagens rörelse mot marknaden redovisas för sig.
- Ett intervall som innehåller 0 betyder "inte påvisat", inte "uteslutet".

## Utfall, 2 november 10:05–10:06 CET

Kurser: `indata/msci_tvilling_priser.csv` (första hämtningen) och `indata/msci_tvilling_priser_2.csv` (komplettering för sex A-aktier utan kurs i första hämtningen). Steg 0 (bara antal per uteslutning) kördes före kompletteringen.

**Urval:** 24 Standard-händelser i 12 bolag och 13 Small Cap-händelser kvar. Uteslutna: MTG B 2009-05 (överlapp med OMXSB), MTG B 2010-05 (kurs saknas i fönstret), Klövern A 2015-05 (systerstatus okänd), IFS B 2009-05 (R3).

**Steg 1, godkänt:**
- Första steget: onormal log-omsättning dagen före ED, ändrat slag minus systerslag, +2,47 (1,92 till 3,01), N 24. Omsättningen i det ändrade slaget är alltså cirka 12 gånger den normala, relativt systerslaget.
- Minsta upptäckbara effekt 1,84 procentenheter (gräns 2,0).

**Steg 2:**

| Urval | N (bolag) | Ändrat slag minus systerslag | p |
|---|---|---|---|
| **Standard (primär)** | **24 (12)** | **+0,21 (−1,14 till 1,53)** | **0,56** |
| Standard, systerslaget utanför MSCI | 15 (10) | −0,29 (−2,34 till 1,81) | 0,93 |
| Small Cap | 13 (9) | −2,33 (−4,23 till −0,04) | 0,037 |
| Alla | 37 (18) | −0,68 (−1,73 till 0,59) | 0,26 |

Standard, mot marknaden (tecken vänt för borttag): ändrat slag +1,52 %, systerslaget +1,31 %.

**Upptäckt efter att resultaten setts (redovisas, ändrar inte de deklarerade skattningarna):** Small Cap-skattningen drivs av två händelser med dataproblem. Hufvudstaden C saknar kurs nästan hela 2007; R4 räknar bara dagar med kurs, så en serie som nästan helt saknar kurs fångas inte av regeln. Transcom B 2011-11 har en skillnad på −23 procentenheter, troligen en bolagshändelse som R3 inte fångar eftersom rörelsen sprids över flera dagar. Utan de två: +0,25 (11 händelser), beskrivande. Standard-händelserna påverkas inte: alla har kurs i fönstret och högst 33 % stillastående dagar.
