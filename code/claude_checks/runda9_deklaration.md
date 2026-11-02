# Runda 9: indexköp 2007–2026, utländska fonder, migrationer och professionell bevakning (LSEG)

Deklarerad 2 november 2026, 17:45 CET. Data: `runda8_fondagare.csv.gz` (LSEG/Lipper fondägare per händelse, före AD och 45 dagar efter ED), `runda8_analytiker.csv.gz` (antal vinstprognoser i konsensus, FY1, per månad). Sedda hittills: bara täckning (antal fonder per händelse, rapportdatum, länder, fondtyper) och att vissa fondnamn finns. Inga innehavsförändringar, inga analytikerförändringar och inga avkastningar för dessa urval är räknade.

## Fonddefinitioner (bestämda före beräkning)

Fonder identifieras på namn i LSEG (`Fund Name`), eftersom LSEG bara visar innehavet i händelseaktien och inte hela portföljen.

- **OMXSB-indexfonder:** Nordea Sverige Passiv; Swedbank Robur Access Sverige; Swedbank Robur Access Edge Sweden; Nordnet Indexfond Sverige och Nordnet Sverige Index; Öhman Marknad Sverige (inte "Bred"); Nordea Inst Aktiefonden Sverige; iShares OMX Stockholm Capped UCITS ETF; XACT Sverige / XACT OMXSB fram till och med 2018 (följer SIX från senast 2018Q4 enligt FI); Länsförsäkringar Sverige Index från 2025-06-16; Storebrand Sverige från 2025-10-01.
- **OMXSB-blandfonder:** Nordeas generationsfonder, Swedbank Robur Access Mix, KPA Blandfond, Nordea Donationsmedelsfond, Länsförsäkringar Sparmål från 2025-06-16. Redovisas separat, eftersom bara den svenska aktiedelen följer OMXSB.
- **OMXS30-fonder:** XACT OMXS30 (även ESG), Avanza Zero till och med 2025-06, Aktiespararna Topp Sverige.
- **Småbolagsindexfonder:** namn med Småbolag/Small Cap och Index/XACT/ETF/PLUS.
- **Övriga passiva:** Fund Type "Exchange-Traded Fund" eller namn med Index/Passive/Tracker som inte hör till grupperna ovan, svenska och utländska.

## Mått per händelse

- Nettoköp = (summa aktier hos gruppens fonder efter) − (summa före), i procent av aktieslagets aktier vid ED (`panel_utdrag`, `shares`). Tecken vänt för borttag.
- **Huvudmått:** bara fonder som finns i båda ögonblicksbilderna (stabila). Sekundärt: alla fonder.
- Innehav vars rapportdatum ligger mer än 120 dagar före ögonblicksbilden räknas inte.

## Steg 0: kontroll mot FI (2019–2026)

För händelser med data i både LSEG och FI (`nettokop_v2_events.csv`): korrelation och medelskillnad mellan LSEG:s nettoköp för svenska OMXSB-indexfonder och FI:s `netto_OMXSB_ny`. **Godkänt** om korrelationen är minst 0,6 och medelskillnaden högst 0,3 procentenheter. Annars används LSEG bara beskrivande och med förbehåll.

## T24. Indexköp och pris per köpt procent över tid (beskrivande, huvudresultat för kedja 2)

- Nettoköp för OMXSB-indexfonder per tillägg och borttag, per period 2007–11, 2012–16, 2017–21, 2022–26, med 95 % intervall (medel per översyn, t(G−1)).
- Pris per köpt procent = medel CAR [AD−1, ED+1] (`tot_gi`) delat med medel nettoköp, per period. Intervall med bootstrap över översyner (9 999 dragningar).
- **Tolkning, bestämd i förväg:** om nettoköpen är lika stora eller större efter 2017 än 2007–2011 medan CAR har fallit, har priset per köpt procent fallit. Det är förenligt med likviditetsförklaringen och talar emot att effekten krympt för att köpen krympt. Om nettoköpen var större tidigt, förklarar mindre köp en del av nedgången.

## T25. Utländska fonder

Nettoköp för utländska OMXSB-fonder (iShares OMX Stockholm Capped) och för övriga passiva fonder, svenska och utländska, per period. Beskrivande. Frågan är om jämförelsen med USA (1,2 % mot 2,3 %) ändras när utländska fonder räknas med.

## T26. Migrationer 2007–2026

Nettoköp för småbolagsindexfonder vid OMXSB-tillägg, per period. Beskrivande. Negativa värden betyder att de säljer, alltså migration.

## T27. Professionell bevakning (test)

- Utfall: förändring i log(1 + antal vinstprognoser), medel över månad +3 till +6 efter ED minus medel över månad −6 till −1 före AD. Saknat värde betyder ingen prognos och sätts till 0, om aktien har värden någon gång i panelen; annars utesluts den.
- Urval: tillägg och borttag mot nästan tillagda och nästan borttagna (`T5urval_T7_T8b_events.csv`), efter 2017 primärt, före 2017 sekundärt. Regression som T9: händelsedummy, uppgång, log börsvärde, fasta effekter per översyn, klustrat på översyn, wild cluster bootstrap.
- Styrka (steg 1, bara SE och MDE): körs om MDE ≤ 0,15 i log, ungefär 15 % fler prognoser.
- **Tolkning, bestämd i förväg:** undre gräns över 0 för tillägg: inträdet följs av fler prognoser i konsensus än för jämförbara aktier, det vill säga bredare professionell bevakning. Intervall som innehåller 0 med godkänd styrka: en ökning större än MDE kan uteslutas. Det utesluter inte ökad uppmärksamhet i andra kanaler, och testet avgör inte köp mot uppmärksamhet som orsak till priset.

## Tillägg 17:50, före beräkning

- Namnen i LSEG är skrivna utan å, ä och ö. Öhman Marknad Sverige heter "Lannebo Marknad Sverige" (inte "... Bred", som följer hela börsen), Nordea Inst Aktiefonden heter "Nordea Inst Aktief Sverige", Nordnet-fonden "Nordnet Sverige Index". Övriga passiva fonder med oklart index (till exempel Danske Invest Index Sweden Restricted) räknas till "övriga passiva".
- Sekundärt mått (utöver 120-dagarsregeln): före-rapporten ska vara daterad före AD och efter-rapporten på eller efter ED.

## Steg 0, första körningen (17:55): ej godkänd, definitionsfel

- Korrelation mot FI 0,57, medelskillnad −0,68. Tillägg: LSEG 0,06 mot FI 1,10 (korrelation 0,28). Borttag: 0,85 mot 1,12 (korrelation 0,95).
- **Orsak, mekanisk:** "stabila fonder" krävde att fonden ägde aktien både före och efter. Vid tillägg äger indexfonderna inte aktien före, och LSEG listar bara fonder som äger aktien. Fonderna som köper föll alltså bort per definition. Felet ligger i definitionen, inte i datan.

## Rättelse 17:58, före omräkning

- **Primärt mått:** alla fonder i gruppen som rapporterar till LSEG både före AD och efter ED, i någon av de hämtade aktierna. En sådan fond som saknas i en ögonblicksbild för just denna aktie räknas som innehav 0 där. Fonder utan rapport i någon av perioderna räknas inte (de fanns inte eller rapporterade inte).
- Steg 0 körs om med samma gränser (korrelation minst 0,6, medelskillnad högst 0,3). Underkänns det igen används LSEG bara beskrivande.

## Utfall (2 november 18:00–18:20)

**Steg 0, efter rättelsen:** korrelation LSEG mot FI 0,91 (tillägg 0,85, borttag 0,95). Medel LSEG 0,85 mot FI 1,11, skillnad −0,26. Godkänt. LSEG ligger något lägre, eftersom några svenska fonder saknas där (till exempel Nordeas generationsfonder, som här ligger under blandfonder, och KPA). Samma utfall med kravet på rapportdatum.

**T24, indexköp och pris per köpt procent** (`runda9_resultat/T24_resultat.csv`). Medel per översyn med 95 % intervall; kvoten med bootstrap över översyner.

| Tillägg | Indexköp, OMXSB-indexfonder | Med blandfonder | CAR [AD−1, ED+1] | Pris per köpt procent |
|---|---|---|---|---|
| 2007–11 (29 händelser, 7 översyner) | 0,10 (−0,01 till 0,21) | 0,20 | 9,23 (2,31 till 16,15) | 80 (29 till 331) |
| 2012–16 (51, 10) | 0,29 (0,17 till 0,42) | 0,33 | −0,67 (−5,43 till 4,10) | – |
| 2017–21 (80, 10) | 0,79 (0,62 till 0,95) | 0,94 | 3,06 (1,13 till 4,98) | 3,1 (1,4 till 6,1) |
| 2022–26 (86, 9) | 0,90 (0,63 till 1,16) | 1,10 | 1,55 (0,01 till 3,09) | 1,8 (0,4 till 3,3) |

Borttag: indexsälj 0,08, 0,18, 0,60, 0,97; CAR −7,76, −7,91, −0,29, −1,25.

**Enligt regeln bestämd i förväg:** indexköpen är större efter 2017 än 2007–2011 medan CAR har fallit. Priset per köpt procent har alltså fallit, och effekten har inte krympt för att köpen krympt. Det är förenligt med likviditetsförklaringen.

**Förbehåll (inte deklarerat, men nödvändigt för läsningen):** 2007–2011 köpte de indexfonder som syns i LSEG bara cirka 0,1 % av aktierna. Det är svårt att se hur så små köp ensamma skulle ge 9 %. Den tidiga effekten drevs troligen till stor del av något annat än de uppmätta indexköpen. LSEG:s täckning är också sämre tidigt (färre fonder, rapporter i median 70 dagar gamla före beskedet), så köpen kan vara något underskattade.

**T25, utländska och övriga passiva fonder** (`T25_T26_resultat.csv`): iShares OMX Stockholm Capped köper 0,06 % vid tillägg 2017–2026. Övriga passiva fonder (andra index): utländska +0,2 vid tillägg 2012–2026, svenska +0,3 till +0,6 vid tillägg 2012–2021. Jämförelsen med USA bygger på indexspecifik efterfrågan och påverkas inte: OMXSB-index- och blandfonder 0,94–1,10 % mot G&S 2,3 %.

**T26, migrationer:** småbolagsindexfonderna handlar 0,00 % vid tillägg i alla fyra perioder. Svenska småbolagsindexfonder finns i LSEG först från 2016, så före dess fanns i praktiken ingen sådan efterfrågan att ta ut.

**T27, professionell bevakning** (`T27_resultat.csv`). Steg 1: N 1 684, G 19, SE 0,036, MDE 0,107 ≤ 0,15, godkänt; 95 % av tilläggen har data.
- Tillägg efter 2017 (primär): +0,027 (−0,049 till 0,103), p 0,47.
- Borttag efter 2017: +0,010 (−0,083 till 0,103), p 0,82.
- Tillägg före 2017 (sekundär): +0,128 (−0,006 till 0,261), p 0,068.

**Enligt regeln bestämd i förväg:** efter 2017 följs inträdet inte av fler vinstprognoser i konsensus än för jämförbara aktier. En ökning större än cirka 11 % kan uteslutas. Det utesluter inte ökad uppmärksamhet i andra kanaler och avgör inte köp mot uppmärksamhet som prisorsak. Före 2017 pekar skattningen mot en ökning, men intervallet innehåller 0.
