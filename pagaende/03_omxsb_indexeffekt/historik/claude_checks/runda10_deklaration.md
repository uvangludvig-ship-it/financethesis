# Runda 10: OMXS30 mot OMXSB (T28) och kostnaden för indexsparare (T29)

Deklarerad 2 november 2026, 17:58 CET (filtid). Inget i T28 eller T29 har körts. OMXS30-händelsernas avkastningar och nettoköp har inte setts. Tilläggens CAR per period för OMXSB är kända (T24). T19b och T19e körs i samma runda men är deklarerade sedan tidigare (`runda6_deklaration.md`, 10:40 och 10:46).

Alla test redovisas i repot oavsett utfall.

Datakälla för priser: `stocks_daily_2005.parquet`, sparad som `runda2_indata/panel_full.csv.gz` av Ludvig 2 nov 17:53 (gzip-kontroll godkänd).

## Gemensamt

- Avkastning: överavkastning mot .OMXSBGI, summerad över fönstret (`wsum`, runda 3).
- Inferens: klustrat på besked (översyn för OMXSB, beskedsdatum för OMXS30), 95 % intervall med t(G−1), p från restriktiv wild cluster bootstrap (Rademacher om G ≥ 12, annars Webb).
- MDE = (t.975 + t.80) × SE.

## T28. OMXS30 mot OMXSB

**Fråga.** Hur stor är prisreaktionen vid OMXS30-ändringar, och hur stor är den per köpt procent jämfört med OMXSB?

**Varför.** OMXS30-fonderna äger lite. Om OMXS30-tillägg ger lika stor eller större reaktion med mindre köp, talar det mot att köpen ensamma driver priset. Ett OMXS30-inträde ändrar dock flera saker samtidigt (synlighet, derivat, investerarkrets), så skillnaden är skillnaden mellan två paket. Den går inte att döpa om till uppmärksamhet (se `output/omxsb_attention_dd_20261102/DD.txt`, avsnitt 3).

**Urval.**
- OMXS30: de 38 händelserna i `runda8_input.csv`. E040 (Industrivärden C) utesluts, eftersom Nasdaqs original anger A-aktien (`identifier_discrepancies.txt`). E036 och E046 behålls: avvikelsen gäller ISIN, inte vilket aktieslag som handlas.
- En OMXS30-händelse utesluts om samma RIC har en OMXSB-händelse vars fönster [AD−1, ED+1] överlappar.
- OMXSB: tilläggen och borttagen i `output/omxsb_replication_2007/events_car.csv` (samma som T24 och T13).

**Utfall.** CAR [AD−1, ED+1], tecken vänt för borttag. Tillägg och borttag slås ihop.

**Primär skattning.** Utfallet på dummyn "OMXS30" i det sammanslagna urvalet, utan övriga kontroller. Klustrat på beskedsdatum.

**Styrkevillkor (steg 1).** Skillnaden skattas om MDE ≤ 3 procentenheter. Motivering: OMXSB-effekten efter 2017 är cirka 2 till 3 %. En skillnad mindre än så är inte meningsfull att tolka. Klarar testet inte villkoret redovisas bara medel med intervall för var och en, och ingen jämförelse dras.

**Beskrivande, oavsett steg 1.**
- Medel-CAR med intervall för OMXS30-tillägg och OMXS30-borttag var för sig.
- OMXS30-fondernas nettoköp i procent av aktierna (LSEG, samma regel som runda 9: rapporterande fonder, saknat = 0), och pris per köpt procent = medel-CAR / medelnettoköp. Ställs bredvid T24.

**Tolkning, bestämd i förväg.**
- Skillnaden innehåller 0 och MDE klarar villkoret: en skillnad större än MDE går att utesluta.
- Större pris per köpt procent i OMXS30: köpen ensamma räcker inte för att förklara OMXS30-reaktionen. Det är förenligt med uppmärksamhet, derivatanknytning eller andra skillnader, och avgör inte vilken.
- Inget resultat här skattar uppmärksamhetens andel av priset.

## T29. Kostnaden för indexsparare

**Fråga.** Hur mycket betalar OMXSB-indexfonderna per år för att köpa tillägg efter beskedet och sälja borttag efter beskedet?

**Metod.** Petajisto (2011), "The Index Premium and Its Hidden Cost for Index Funds", Journal of Empirical Finance 18(2): 271–288. Kostnaden är indexets omsättning vid ändringar gånger prispremien mellan besked och genomförande. Petajisto får 21 till 28 punkter per år för S&P 500 och 38 till 77 för Russell 2000.

**Mått.**
- Vikt w: aktiens fritt flytande börsvärde dagen före AD delat med summan för alla medlemmar efter översynen (tillägg) eller före översynen (borttag). Fritt flytande andel som i runda 3 (`lseg_freefloat_hist.csv`, annars `lseg_klassificering.csv`, annars 100 %).
- Premie: CAR [AD−1, ED−1], till stängningen då fonderna handlar. Tecken vänt för borttag.
- Kostnad per översyn = Σ w × premie. Kostnad per år = summan av årets översyner, i punkter av fondförmögenheten.
- I kronor: kostnad per år × OMXSB-fondernas förmögenhet i december samma år (`data/shof/tracker_aum_shof.csv`, kolumnen `shof_inkl_xact_omxsb_mdkr`, samma fondgrupp som runda 9).

**Sekundärt.** Premien med CAR [AD−1, ED+1] minus medel-CAR för nästan valda i samma översyn (`runda3_resultat/T13_events.csv`, event = 0). Det tar bort den del som också syns hos jämförbara aktier.

**Redovisning.** Medel per år och period (2007–11, 2012–16, 2017–21, 2022–26) med 95 % intervall från bootstrap över översyner inom perioden (9 999 dragningar, frö 20261102). Beskrivande; ingen styrkekontroll och inget test.

**Tolkning, bestämd i förväg.**
- Måttet är det pris fonderna betalar utöver priset före beskedet, om hela premien beror på deras köp. Med kontrollerna (sekundärt) blir det en mindre och försiktigare siffra.
- Kostnaden är en överföring till dem som säljer till fonderna. Det är inte en uppmätt förlust i avkastning, och den säger inget om fonderna borde handla annorlunda.

## Tillägg cirka 18:02, före körning av T28 och T29

Inga T28- eller T29-utfall har setts. T19b och T19e har körts (se `runda6_deklaration.md`).

- OMXSB-borttag som flaggas i `output/omxsb_replication_2007/mechanisms/step1_deletion_flags.csv` (avnotering, bud eller ändrat antal aktier) utesluts i både T28 och T29, som i T19e. Kursen vid ett bud beror på budet, inte på indexet.
- T29 sekundärt: borttag justeras med medel-CAR [AD−1, ED+1] för nästan borttagna i samma översyn (`runda2_resultat/T5urval_T7_T8b_events.csv`, type = deletion, event = 0). Tillägg justeras som deklarerat med `runda3_resultat/T13_events.csv`.
- T29 i kronor: för 2026 finns ingen decembersiffra; senaste månaden i `tracker_aum_shof.csv` används.
- Medlemmar före den första översynen (2007H2) saknas i medlemslistan. Där används medlemmarna efter översynen, minus tilläggen, plus borttagen.

## Tillägg cirka 18:05, före körning av T29: fel i SHoF-serien

När indata till T29 kontrollerades visade sig `tracker_aum_shof.csv` ha luckor. Serien byggdes utan skript och använde bara `tnafund`, som saknas för Swedbank Robur Access Sverige och Access Edge Sweden från januari 2025 till augusti 2026 och för Nordnet Indexfond Sverige ESG från 2023. Där sattes förmögenheten till 0. December 2025 blev därför 116 miljarder; rätt nivå är cirka 181.

Ny serie: `shof_aum.py` → `data/shof/tracker_aum_shof_v2.csv`. Dagsvärde = `tnafund`, annars summan av `tnaclass` för fondens andelsklasser samma dag; månadsvärde = senaste dagsvärde inom 92 dagar före månadens slut. T29 i kronor använder kolumnen `inkl_xact_omxsb_mdkr` i v2. Den första filen ligger kvar oförändrad.

Kvarvarande lucka: Nordnet Indexfond Sverige ESG saknas i SHoF från mitten av 2026 och i december 2022.

OMXSB-borttagen i T28 och T29 utesluts via `event_id` i flaggfilen (inte via RIC som i T19e), så att bara de flaggade händelserna faller bort.

## Tillägg cirka 18:08, efter steg 0 och före steg 1 och 2

Steg 0 visar bara urval och datakedja, inga utfall.

- **T28-urval:** 36 OMXS30-händelser (19 tillägg, 17 borttag) på 15 beskedsdatum. Utöver E040 utesluts E010 (Stora Enso R, borttag 2007), som överlappar en OMXSB-händelse för samma aktie. OMXSB: 462 händelser.
- **T29, vikter:** panelens `mcap` gäller hela bolaget, inte aktieslaget (samma värde för A och B). Vikten räknas därför som kurs × aktieslagets antal aktier × fritt flytande andel. Bolagets `mcap` används bara om inget annat aktieslag har kurs. Två till sex medlemmar per översyn saknar ändå värde, främst Skanska B och Tele2 B (aktier saknas i panelen), Millicom och Nordea 2007–2009. Summan i nämnaren blir då något för liten, och kostnaden något för stor. Felet är uppskattningsvis några procent av kostnaden, mer 2007–2009.
- 468 händelser; 6 saknar vikt och 6 saknar premie.

## Utfall (2 nov 18:09 till 18:28, filtider)

**T28, steg 1.** N 498 (36 OMXS30), G 54 (15 OMXS30-datum), SE 1,28, MDE 3,66 > 3. **Stoppad.** Skillnaden mellan OMXS30 och OMXSB skattas inte och ingen jämförelse dras.

**T28, beskrivande** (`T28_resultat.csv`, `T28_omxs30_nettokop.csv`). CAR [AD−1, ED+1], tecken vänt för borttag:
- OMXS30-tillägg +0,21 (−2,46 till +2,88), N 19, G 14; OMXS30-borttag +0,69 (−3,82 till +5,21), N 17, G 12; alla OMXS30 +0,44 (−2,03 till +2,91).
- OMXSB-tillägg +2,57 (1,16 till 3,98), N 256; OMXSB-borttag +2,03 (0,18 till 3,88), N 206; alla OMXSB +2,33 (1,07 till 3,60).
- OMXS30-fondernas nettoköp: 0,22 % av aktierna vid tillägg och 0,13 % vid borttag (alla 36 har fonddata). Pris per köpt procent: 1,0 vid tillägg. Vid borttag (5,5) är kvoten meningslös, eftersom CAR-intervallet är mycket brett.
- Läsning: ingen prisreaktion är påvisad vid OMXS30-ändringar. Intervallet når cirka 3 %, så en reaktion lika stor som OMXSB:s går inte att utesluta.

**T29, första körningen av steg 2 (18:11), felaktig.** Två aktier fick orimliga vikter: Eniro 42 % och Fingerprint B 32 % av indexet. Orsaken är panelens aktieantal för dessa bolag, som inte stämmer med kursen (bolagen har gjort stora nyemissioner och sammanläggningar). Kostnaden blev 405 punkter per år 2012–16 och −50 punkter 2017–21. Resultaten ligger kvar i `runda10_resultat/forsta_korningen/`.

**Rättelse cirka 18:13 (andra körningen 18:15, också felaktig).** Regeln "ett aktieslag kan inte vara värt mer än bolaget" tog bort Eniro och Fingerprint, men grundfelet kvarstod. Resultaten ligger i `runda10_resultat/andra_korningen/`.

**Rättelse cirka 18:16 (slutlig).** Panelens kurs är justerad för senare splittar och sammanläggningar, medan aktieantalet är historiskt. Kurs × aktier blir därför fel för alla bolag som senare ändrat antalet aktier: Investor 2018 får en fjärdedel av sitt rätta värde, Eniro 2013 750 gånger för mycket. Nu används bolagets `mcap` (ojusterat) × aktieslagets andel av aktierna i bolagets noterade aktieslag samma dag. Största vikten är då 2,5 % (Stora Enso R). Regeln beror inte på premierna. Samma fel fanns i Nasdaq-regeln i runda 2, 3 och 6; se `runda6_deklaration.md` och `RESULTAT_2026-11-02.md`, avsnitt 6c. T29:s sekundära premie använder därför kontrollerna från den rättade runda 3 (`runda3_resultat_v2/T13_events.csv`).

**T29, slutlig** (`T29_primär.csv`, `T29_sekundär.csv`). Kostnad per år i punkter av OMXSB-fondernas förmögenhet, 95 % intervall från bootstrap över översyner:

| Period | Omsättning, % per år | Primär, punkter | Sekundär, punkter | Primär, mkr per år |
|---|---|---|---|---|
| 2007–11 | 2,1 | 16,1 (9,5 till 22,7) | 11,4 (6,3 till 16,5) | 5 (2 till 7) |
| 2012–16 | 4,0 | 7,2 (−3,2 till 19,3) | 4,0 (−2,9 till 10,6) | 25 (0 till 61) |
| 2017–21 | 6,1 | 5,3 (−7,1 till 15,7) | 1,9 (−6,5 till 9,4) | 45 (−5 till 99) |
| 2022–26 | 5,9 | 10,6 (7,1 till 14,4) | 12,0 (6,6 till 18,5) | 125 (71 till 203) |

- Läsning: kostnaden ligger på 2 till 16 punkter per år. Petajisto (2011) fick 21 till 28 punkter för S&P 500 och 38 till 77 för Russell 2000. Intervallen 2012–21 innehåller 0.
- I kronor växer kostnaden med fondförmögenheten, från cirka 5 miljoner per år 2007–11 till cirka 125 miljoner per år 2022–26.
- Kostnaden är en överföring till dem som säljer till fonderna, inte en uppmätt förlust i avkastning.

**T28, tillägg 18:24: aktieantal i LSEG-innehaven.** LSEG:s "Fund Shares Held (Adjusted)" verkar vara justerat för senare splittar (men inte för nyemissioner), medan panelens aktieantal är historiskt. Belägg: Indutrade 2020 (split 3:1 senare) har LSEG-köp 2,5 gånger högre än FI-köp i förhållande till övriga händelser, medan aktier med senare nyemissioner (Intrum, SAS, Bonava) inte avviker (`runda9_resultat/T24_split_per_handelse.csv`). För aktier som senare splittats blir köpt andel därför för stor. 5 av 19 OMXS30-tillägg gäller sådana aktier och 3 saknar uppgift. Utan dem: nettoköp 0,11 % av aktierna och CAR −0,15 (N 11). Kvoten pris per köpt procent är meningslös när CAR ligger nära 0. Se `T28_omxs30_nettokop_split.csv`.

## Rättelse av klockslag (2 nov 18:40)

Klockslagen i den här filen skrev jag efter uppskattning, inte efter klockan, och flera ligger senare än filernas faktiska tider. Ordningen är rätt beskriven, men klockslagen bevisar den inte. I denna fil är klockslagen nu rättade efter filtiderna i Claude-miljön (deklarationen 17:58, T28 steg 1 18:09, T29-körningarna 18:11, 18:15 och 18:28, omkörningen av runda 2, 3 och 6 18:22 till 18:25). Där filtid saknas står "cirka".
