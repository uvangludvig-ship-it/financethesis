# Runda 6: förutsägbarhet (T19), dos-respons (T20), ägare vid borttag (T21)

Deklarerad 2 november 2026, 10:40 CET. Inget i dessa test har körts. Inga avkastningar, volymer eller ägarutfall för urvalen nedan har setts. Kända sedan tidigare: nettoköpens medel per typ (1,17 % tillägg, 0,84 % borttag), regelns träffsäkerhet per översyn (`T6_traffsakerhet.csv`) och T13:s skattningar över [AD−1, ED+1].

Alla test redovisas i repot oavsett utfall.

## Gemensamt

- Avkastning: överavkastning mot .OMXSBGI, summerad över fönstret (som i runda 2–3, `wsum`).
- Regression: utfall på testvariabel, uppgång [AD−100, AD−1], log börsvärde dagen före AD och fasta effekter per översyn. Klustrat på översyn. 95 % intervall med t(G−1); p från restriktiv wild cluster bootstrap (Rademacher om G ≥ 12, annars Webb).
- MDE = (t.975 + t.80) × SE.
- Steg 1 (styrka) visar bara N, G, SE och MDE. Steg 2 körs bara för test som klarar sitt villkor. Ett test som stoppas redovisas med MDE.

## T19. Förutsägbarhet

**Fråga.** Prisar marknaden in tillägg som går att förutse med Nasdaqs regel innan beskedet?

**Urval.** Samma konstruktion som T13 (`runda3.py`): per översyn 2008H1–2026H1, Nasdaq-regeln beräknad med data fram till referensdagen före beskedet. Tillägg (event = 1) och icke-medlemmar som inte lades till, inte bland de 30 % minst omsatta och antingen valda av regeln eller med kumulativ andel ≤ 95 % (event = 0). Samma uteslutningar som T13.

**Utfall.** Beskedsreaktion CAR [AD, AD+1].

**T19a (primär).** Bland tillägg: CAR [AD, AD+1] på dummyn "regeln valde" med kontroller ovan. Förutsägelse vid förväntan: b < 0, eftersom en förutsägbar del redan är i priset.

**T19b (primär).** Bland icke-tillagda: CAR [AD, AD+1] på dummyn "regeln valde". Förutsägelse vid förväntan: b < 0, eftersom aktier som marknaden räknade med föll när de inte valdes.

**Sekundärt.**
- T19a och T19b före respektive efter 2017.
- T19a med utfall CAR [AD, ED+1].
- T19c: bland tillägg, CAR [AD−20, AD−1] på "regeln valde", med uppgång [AD−100, AD−21] i stället för [AD−100, AD−1] som kontroll. Förväntan förutsäger b > 0.
- T19d: bland tillägg, onormal log volym [AD−10, AD−1] (medel av log volym minus medel över [AD−120, AD−21]) på "regeln valde". Förväntan förutsäger b > 0.

**Styrkevillkor (steg 1).** T19a körs om MDE ≤ 1,5 procentenheter; T19b om MDE ≤ 0,5. Motivering: med en total effekt kring 3 % och en skillnad i sannolikhet på cirka 0,4 mellan valda och ej valda är skillnaden i beskedsreaktion cirka 1,2. För de icke tillagda är sannolikheten lägre och effekten per aktie mindre.

**Tolkning, bestämd i förväg.**
- Övre gräns under 0 i T19a eller T19b: marknaden förväntar sig delar av tilläggen. Förutsägbarhet finns.
- Intervallet innehåller 0 och MDE klarar villkoret: förväntan större än MDE går att utesluta; mindre kan inte uteslutas.
- Skillnaden före och efter 2017 är sekundär och redovisas med intervall. Den avgör inte om förutsägbarheten har ökat om intervallet för skillnaden innehåller 0.

## T20. Dos-respons: pris mot indexfondernas köp

**Fråga.** Rör sig priset mer vid händelser där indexfonderna köper eller säljer mer?

**Urval.** Tillägg och borttag 2019–2026 med status ok i `nettokop_events.csv`.

**Testvariabel.** Nettoköp, alla indexfamiljer (`netto_alla_index`), i procent av aktieslagets aktier. Sekundärt: nettoköp i dagars omsättning (nettoköp × aktier / medelvolym [AD−120, AD−21]), och bara OMXSB-familjen.

**Utfall.** CAR [AD−1, ED+1] (som `tot_gi`).

**T20 (primär).** Utfallet på nettoköp, med kontroller ovan och fasta effekter per översyn × typ. Lutningen skattas alltså inom tillägg och inom borttag. Förutsägelse vid efterfrågan: b > 0.

**Styrkevillkor.** Körs om MDE ≤ 1,8 (beskrivande pris per köpt procent).

**Tolkning, bestämd i förväg.** Undre gräns över 0: större köp hänger ihop med större prisrörelse inom samma typ och översyn. Det är förenligt med efterfrågan men inget bevis, eftersom nettoköpet beror på fritt flytande andel, som kan hänga ihop med likviditet. Kvartalsmätningen gör nettoköpet brusigt, vilket drar b mot 0.

## T21. Ägaruppdelning vid borttag

Samma beskrivande uppdelning som `agar_kontroll/agar_omxsb.py`, för borttag mot nästan borttagna 2019–2026. Ingen styrkekontroll; beskrivande.

## Utfall

**Datakälla.** `stocks_daily_2005.parquet` kan inte läsas i Claude-miljön (pyarrow saknas, paketregistret nås inte). `stocks_daily_2005.csv.gz` i repot är trasig: gzip-kontrollen misslyckas (CRC- och längdfel), både här och på Ludvigs dator (md5 53de3aa6…). Därför körs T19a, T19c, T19d och T20 på `data/panel_utdrag.csv.gz` (186 aktier). Utdraget täcker alla tillägg och alla T20-händelser men bara 35 % av de icke tillagda, så T19b väntar på hela panelen. Tilläggens regelflagga, uppgång och storlek tas direkt från `runda3_resultat/T13_events.csv`, det vill säga exakt T13:s urval.

**Steg 0, 2 nov ca 10:42.** Utdraget ger CAR [AD−1, ED+1] för alla 237 tillägg med största avvikelse 0,0 mot runda 3. Godkänt.

**Steg 1, 2 nov ca 10:44.** Bara N, G, SE och MDE visade.
- T19a: N 237 (118 valda av regeln), G 37, SE 0,744, MDE 2,14 > 1,5. **Stoppad.**
- T20: N 204, G 15, SE 1,061, MDE 3,20 > 1,8. **Stoppad.**
- Sekundära test följer sitt primära test och skattas inte (T19a [AD, ED+1], T19c, T19d, T19a per period; alla T20-varianter). Regeln ändras inte i efterhand.

**Läsning.** Med 237 tillägg kan en skillnad i beskedsreaktion mellan förutsägbara och oförutsägbara tillägg bara upptäckas om den är över cirka 2 procentenheter. Dos-respons-testet saknar precision eftersom nettoköpen mäts kvartalsvis och bara 15 översyner finns. Båda frågorna lämnas öppna.

**T21, beskrivande** (`agar_kontroll/runda6_t21.py`). 96 borttag, 564 nästan borttagna, 15 översyner. Förlorade ägare per borttag relativt kontrollerna:
- alla fonder −10,8 (−14,1 till −7,5);
- OMXSB i jämförelseindex −10,9 (−13,0 till −8,9), varav utan "index" i namnet −6,5 och med aktiv risk över 1,5 −1,8 (−3,1 till −0,4);
- utan OMXSB i jämförelseindex +0,1 (−1,7 till 1,9);
- fondbolag −1,2 (−1,8 till −0,6).

Vid borttag försvinner ägare bara bland fonder med OMXSB i jämförelseindex. Bland övriga fonder syns ingen förändring. Vid tillägg tillkom däremot +3,3 (1,8 till 4,7) ägare utanför OMXSB-fonderna.

## Tillägg 10:46: T19e, tillägg och borttag sammantaget

Deklarerat efter att T19a stoppats för låg precision. Inga skattningar för T19a har setts. Syftet är bara större urval.

- Urval: tillägg som i T19a samt borttag 2008H1–2026H1, där "förutsägbart borttag" betyder att regeln inte valde aktien vid översynen. Kräver hela panelen, eftersom regeln ska beräknas för medlemmarna.
- Utfall: beskedsreaktion CAR [AD, AD+1], tecken vänt för borttag.
- Skattning: utfallet på dummyn "förutsägbar" med uppgång (tecken vänt för borttag), log börsvärde och fasta effekter per översyn × typ. Klustrat på översyn.
- Förväntan förutsäger b < 0. Styrkevillkor: MDE ≤ 1,5, samma som T19a.
- Tolkning som T19a.
- Tillägg 10:48, före körning: borttag som Ludvigs steg 1 flaggar (`output/omxsb_replication_2007/mechanisms/step1_deletion_flags.csv`, flagged = True: avnotering, bud eller ändrat antal aktier, 19 av 226) utesluts. Annars blandas uppköpsborttag, med egen kursreaktion, in bland de oförutsägbara.

## Utfall, hela panelen (2 nov 17:59 till 18:01)

Data: `runda2_indata/panel_full.csv.gz`, det vill säga `stocks_daily_2005.parquet` sparad som csv av Ludvig 17:53. Gzip-kontrollen godkänd.

- **Steg 0.** T13 återskapat exakt: +1,701 (0,657 till 2,746), N 985, G 19. Godkänt.
- **Steg 1.** T19b: N 1 461 (855 valda av regeln), G 38, SE 0,196, MDE 0,565 > 0,5. **Stoppad.** T19e: N 417 (237 tillägg, 180 borttag; 230 förutsägbara), G 38, SE 0,505, MDE 1,45 ≤ 1,5. Godkänd. Villkoren ändras inte i efterhand.
- **Steg 2.** T19e: −0,481 (−1,505 till +0,543), p 0,335.
- **Läsning enligt förhandsregeln.** Intervallet innehåller 0 och MDE klarar villkoret. En skillnad i beskedsreaktion på mer än cirka 1,5 procentenheter mellan förutsägbara och oförutsägbara händelser går att utesluta. En mindre förväntan går inte att utesluta. Punktskattningen har det tecken som förväntan förutsäger.
- T19b:s sekundära test skattas inte. Medel per grupp finns i `runda6_resultat/T19_medel.csv` (beskrivande, ingen inferens).

## Rättelse 2 nov cirka 18:20: börsvärdet i Nasdaq-regeln (runda 2, 3 och 6)

Panelens kurs är justerad för senare splittar och sammanläggningar, medan aktieantalet är historiskt. Regeln räknade börsvärdet som kurs × aktier och fick därför fel värde för alla bolag som senare ändrat antalet aktier (Investor 2018: en fjärdedel av rätt värde). Rättat i `runda2.py`, `runda3.py` och `runda6.py`: bolagets `mcap` (ojusterat) × aktieslagets andel av aktierna i bolagets noterade aktieslag. Den gamla raden står kvar som kommentar. Omkört på hela panelen till `runda2_resultat_v2/`, `runda3_resultat_v2/` och `runda6_resultat_v2/`; de gamla mapparna är orörda.

- Regelns träffsäkerhet (T6) blir bättre: efter 2017 väljer den 61 % av tilläggen (förut 54 %), före 2017 44 % (förut 38 %).
- T13 efter 2017: +1,30 (0,22 till 2,38), p 0,026, N 1 055 (förut +1,70, N 985).
- T19b steg 1: N 1 571, SE 0,201, MDE 0,577 > 0,5. Fortfarande stoppad.
- T19e steg 1: N 415, SE 0,460, MDE 1,32 ≤ 1,5. Godkänd. Steg 2: **−0,364 (−1,296 till +0,567), p 0,400**.
- Läsningen står kvar: en skillnad över cirka 1,3 procentenheter mellan förutsägbara och oförutsägbara händelser kan uteslutas; en mindre kan inte uteslutas. Steg 0 i `runda6_resultat_v2/` säger STOPP eftersom jämförelsevärdet (+1,701) gäller den gamla regeln; det nya värdet stämmer med `runda3_resultat_v2`.

## Rättelse av klockslag (2 nov 18:40)

Klockslagen i den här filen skrev jag efter uppskattning, inte efter klockan, och flera ligger senare än filernas faktiska tider. Ordningen är rätt beskriven, men klockslagen bevisar den inte. Filtider: utdragets resultat sparades 10:42 och deklarationen ändrades senast 10:46, före kvällens tillägg. Hela panelen kördes 17:59 till 18:01 och den rättade regeln 18:22 till 18:25.
