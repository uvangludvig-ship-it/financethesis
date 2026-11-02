# Runda 11: Greenwood och Sammon (2025) fullt ut, med multiplikatorn M

Deklarerad 2 november 2026, skriven 19:23–19:35 CET (klockslag avlästa med `date`). Filen ändras inte efter att den lagts på Ludvigs dator. Tillägg skrivs i `runda11_tillagg.md`, utfall i `runda11_resultat/`.

**Källa.** Greenwood, R. och M. Sammon (2025), "The Disappearing Index Effect", Journal of Finance 80(2): 657–698, den publicerade versionen i Harvards arkiv (dash.harvard.edu). Avsnitts-, tabell- och ekvationsnummer nedan är artikelns.

**Redan känt före deklarationen.** T24 (medel-CAR och medel-D per period, tillägg och borttag), kontrollen för senare splittar (`runda9_resultat/T24_kontroll_split.csv`), E1 (Ludvigs tabell 2 med andra kontroller), att D inom en översyn bara korrelerar 0,38 med fri flytande andel (2017–26). Inget av det som skattas nedan har räknats.

## Gemensamt

- **Händelser:** OMXSB-tillägg och borttag i `output/omxsb_replication_2007/events_car.csv` med kurser i fönstren. Borttag som flaggas i `mechanisms/step1_deletion_flags.csv` (avnotering, bud, ändrat antal aktier) utesluts via `event_id`.
- **Perioder** (år för AD): 2007–11, 2012–16, 2017–21, 2022–26.
- **CAR:** överavkastning mot .OMXSBGI, summerad. Totalt fönster [AD−1, ED+1] (G&S "total effect"). Långt fönster [AD−20, ED+1] (G&S avsnitt 2.4). Tecken vänt för borttag i allt som rör M.
- **D (efterfrågechocken):** OMXSB-indexfondernas nettoköp ur LSEG (`data/runda8_fondagare.csv.gz`), samma regel som runda 9: fonder som rapporterar både före AD (inom 120 dagar) och efter ED (inom 45 dagar), saknat innehav = 0. I procent av aktieslagets historiska aktieantal dagen för ED ur hela panelen. Tecken vänt för borttag.
- **Senare splittar:** LSEG:s innehav är justerade för senare splittar, men aktieantalet är historiskt. En händelse flaggas om kvoten (bolagets mcap / summan av de noterade aktieslagens aktier) / justerad kurs skiljer sig mer än en faktor 1,4 mellan ED och sista dagen i panelen, eller om kvoten inte går att räkna. **Primärt används bara händelser utan flagga.** Känslighet: alla händelser.
- **Kontroller (G&S tabell 2), demeanade inom urvalet:**
  - onormal omsättning: aktieslagets omsättning i kronor / dess börsvärde, medel över de 21 handelsdagarna före AD, minus samma kvot värdeviktat över alla aktier på huvudlistan;
  - storlek: aktieslagets börsvärde dagen före AD / summan för OMXSB-medlemmarna (före översynen), i procent;
  - arbitragerisk (Wurgler och Zhuravskaya): residualvariansen från dagsavkastning på .OMXSBGI, [AD−250, AD−2], minst 100 dagar;
  - analytiker: antal vinstprognoser (FY1) i senaste månaden före AD (`data/runda8_analytiker.csv.gz`); saknas värdet men aktien finns i datan räknas 0.
  - Aktieslagets börsvärde = bolagets `mcap` × slagets andel av aktierna i bolagets noterade slag (regeln från 6c).
- **Inferens:** klustrat på översyn, 95 % intervall med t(G−1), p från restriktiv wild cluster bootstrap (Rademacher om G ≥ 12, annars Webb), 9 999 dragningar, frö 20261102. MDE = (t.975 + t.80) × SE.

## Steg 0 (datakedja, inga utfall)

Spärr: medel-D per period för tillägg, alla händelser, ska återskapa T24 (0,10 / 0,29 / 0,79 / 0,90) med högst 0,03 i avvikelse. Annars stopp och felsökning före steg 1. Steg 0 visar också antal händelser, andel med D, andel flaggade för split och täckning för varje kontroll.

## Test

**A. Tabell 2, sammansättning (beskrivande replikation).** CAR (totalt fönster) på periodkonstanter utan konstant, med och utan de fyra kontrollerna. Tillägg och borttag var för sig, alla händelser (D behövs inte). Redovisa periodkonstanterna, skillnaden 2007–11 minus 2022–26 med intervall, och kontrollernas koefficienter.

**B. Tabell 4, uppgång före beskedet (beskrivande).** CAR [AD−n, AD−1] för n = 10, 20, 50 och 100, per period, tillägg och borttag. Medel med klustrat intervall.

**C. Tabell 5, M per period (beskrivande).** M_p = medel-CAR_p / medel-D_p, totalt och långt fönster, tillägg och borttag. Elasticitet = −1/M. Intervall från bootstrap över översyner inom perioden. Primärt utan splittflaggade händelser, känslighet med alla.

**D. Tabell 6, M med kontroller (G&S ekvation 6).** CAR_i = Σ_p M_p · (1{i i period p} · D̄_p) + kontroller + fel, utan konstant, där D̄_p är periodens medel-D. Fyra kolumner per typ: totalt och långt fönster, med och utan kontroller. M_p:s intervall = periodkoefficientens intervall / D̄_p (D̄_p behandlas som givet, som hos G&S).

- **Primär hypotes H11a:** M har fallit. H0: M_2007–11 = M_2022–26, det vill säga den linjära restriktionen b_1 · D̄_4 − b_4 · D̄_1 = 0 på periodkoefficienterna, tillägg, totalt fönster, med kontroller. Förväntan enligt G&S: M_2007–11 > M_2022–26.
- **H11b:** samma i det långa fönstret.
- **Sekundärt:** borttag; M_2017–21 mot M_2022–26 (de två perioder där D mäts väl).
- **Tolkning, bestämd i förväg:**
  - Fallet i M är en beskrivning av hur pris och köp hänger ihop över tid, inte en skattad orsak. D före 2012 är mycket litet och sämre täckt, så M_2007–11 är osäkert. Det redovisas.
  - Om M faller i totalt fönster men klart mindre i långt fönster har en del av effekten flyttats till före beskedet (förväntan). Om fallet är lika stort i båda: inget tecken på flytt.
  - Jämförelse med G&S (tillägg, M från 6,75 till 0,37; med kontroller 6,6 till 0,7; långt fönster med kontroller 8,7 till 1,7) är beskrivande: olika marknad, perioder och mått på D.

**E. Tabell 7, vem tar emot köpen (beskrivande).** Nettoförändring i procent av aktierna per fondgrupp ur LSEG, samma regel som D: OMXSB-indexfonder, övriga passiva (OMXSB-blandfonder, OMXS30, småbolagsindex, övriga passiva svenska och utländska), aktiva fonder ("ej passiv" i runda 9) och alla fonder. Per period, tillägg och borttag, primärt utan splittflaggade händelser.

- **Sekundär hypotes H11c:** aktiva fonders nettoförändring vid tillägg 2017–26. G&S: cirka 0. Vår läsning, bestämd i förväg: under 0 = aktiva fonder säljer till indexfonderna; över 0 = de köper också, efterfrågan är större än D och M är för högt; intervall som innehåller 0 = ingen säker förändring.
- Skillnaden indexfonder minus alla fonder är det som köps från investerare utanför fonderna.

**F. Nyemissioner (G&S avsnitt 2.4.3, beskrivande).** Förändring i bolagets totala historiska aktieantal (summa över noterade slag), log, från AD−5 till ED+60, tillägg mot nästan tillagda i samma översyn (`runda2_resultat_v2/T5urval_T7_T8b_events.csv`), och andel med ökning över 1 % och över 5 %. Per period.

**G. Figur 1 och G&S figur 5 (beskrivande).** Medel-D per år för tillägg och borttag. Indexfondernas ägarandel: OMXSB-fondernas förmögenhet i december (`data/shof/tracker_aum_shof_v2.csv`, `inkl_xact_omxsb_mdkr`) / OMXSB-medlemmarnas samlade börsvärde vid årets sista översyn.

**H. Figur 3 och T30, prisrörelse mot D per händelse.**
- Som G&S: CAR på D utan kontroller, tillägg och borttag, alla perioder; lutning och R².
- T30: samma med fasta effekter per översyn och de fyra kontrollerna, 2007–26 och 2017–26.
- Styrkevillkor för T30: MDE ≤ 2 (ungefär M i 2017–26 enligt T24). Klarar det inte villkoret redovisas bara lutningen utan p-värde.
- **Tolkning, bestämd i förväg:** inom en översyn varierar D i teorin bara med fri flytande andel, och i datan korrelerar de bara 0,38, så det mesta är brus som drar lutningen mot 0. En undre gräns över 0 vore förenlig med att köpen driver priset. Ett intervall som innehåller 0 säger nästan ingenting, och tolkas inte som att köpen saknar betydelse.

**I. Figur 7, kursbanan (beskrivande).** Medel-CAR dag för dag från AD−100 till AD+14, per period, tillägg och borttag.

## Steg 1 (styrka, bara N, G, SE och MDE)

För H11a, H11b, H11c och T30. H11a och H11b körs oavsett (förväntad styrka är hög eftersom D_2007–11 är litet); MDE redovisas. H11c är beskrivande med intervall. T30 enligt villkoret ovan.

## Rapportering

Allt redovisas oavsett utfall, i `runda11_resultat/` och i `RESULTAT_2026-11-02.md`. Ändringar efter denna fil skrivs med klockslag (`date`) i `runda11_tillagg.md`.
