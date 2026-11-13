# Indexeffekten på OMXSB: struktur och förlängning

Version 1 november 2026. Ersätter tidigare strukturdokument.

## Beslutet i korthet

- **Replikation:** G&S på OMXSB 2007–2026, inklusive deras fyra förklaringar. I stort sett klar.
- **Förlängning, del 1 (huvudtest):** faller priset tillbaka efter indexfondernas handelsdag? Det motsvarar G&S figur 9, nu för Sverige, på alla cirka 490 händelser.
- **Förlängning, del 2 (det nya):** tvillingaktier. När bara ett av ett bolags två aktieslag (A och B) byter indexstatus, används systeraktien som jämförelse. Den har samma bolag, samma utdelning och samma nyheter, men får inga indexköp.
- **Struket:** förutsägbarhet före beskedet, regeländringen 2021 som bevis, slutauktionen, fonders indexbyten och blankning (motiv längst ned).

## Frågan

Hur tillfällig och aktieslagsspecifik är den svenska indexeffekten?

Frågan är formulerad efter vad testen faktiskt kan visa. De kan visa om prisrörelsen går tillbaka och om den är koncentrerad till det aktieslag som indexfonderna handlar. De kan inte visa vilka handlare som jämnar ut den.

## X, Y och Z

**X (G&S):** Indexeffekten för S&P 500 har nästan försvunnit. G&S förklarar det främst med migration mellan index och med att marknaden bättre kan möta indexfondernas handel. Prismultiplikatorn för tillägg föll från 6,75 till 0,37. Aktier med nära substitut utsätts för mindre prispress, enligt Wurgler och Zhuravskaya som G&S citerar. På 1990- och 2000-talet föll priset delvis tillbaka efter inträdet, men på 2010-talet nästan inte alls.

**Y (Sverige):**
1. Effekten finns kvar (+2,5 % för tillägg 2017–2026), så det finns en prisrörelse att följa efter handelsdagen.
2. Många bolag har två noterade aktieslag med samma kassaflöden. Nasdaq bedömer varje aktieslag för sig: alla slag är valbara, och ofta ingår bara det ena i OMXSB.
3. FI:s fondinnehav per ISIN visar att indexfonderna i regel bara äger det aktieslag som ingår i indexet.

**Z:** Om effekten är tillfällig, och om den är koncentrerad till det aktieslag som indexfonderna handlar, jämfört med ett systerslag med samma rätt till utdelning. En ensam aktie kan stiga och falla av bolagsnyheter. Om det indexerade slaget rör sig relativt systerslaget och sedan går tillbaka blir förklaringen med tillfälligt efterfrågetryck mer trovärdig. Det kan prisreaktionen ensam inte visa.

## Kapitel

1. **Inledning.** G&S gåta, att effekten finns kvar i Sverige, frågan och svaret.
2. **Institutionell bakgrund.** OMXSB:s regler, urval per aktieslag, svenska A- och B-aktier, indexfonder, översynskalendern och kortare väntetid från maj 2021.
3. **Data.** LSEG-panelen, Nasdaqs ändringslistor och FI:s fondinnehav.
4. **Replikation.** G&S tabeller för OMXSB, multiplikator och elasticitet. Därefter G&S fyra förklaringar: sammansättning, migration, förutsägbarhet och likviditet.
5. **Priset efter handelsdagen** (del 1).
6. **Tvillingaktier** (del 2).
7. **Slutsats.** Siffrorna jämförs med G&S siffror i samma mening.

## Del 1: priset efter handelsdagen

- **Vad som mäts:** CAR från beskedet till 100 dagar efter, i samma form som G&S figur 9, och de förhandsspecificerade fönstren efter handelsdagen.
- **Varför:** det är G&S eget mått på om effekten var tillfällig. Det går att göra på alla händelser, så styrkan är god.
- **Tolkning:**
  - Faller priset tillbaka var effekten ett tillfälligt prisryck, som i USA på 1990- och 2000-talet.
  - Ligger det kvar är den bestående, som i USA på 2010-talet men på en högre nivå.

**Förhandsspecifikation:**
- **Urval:** alla 487 tillägg och borttag 2007–2026 (39 översyner).
- **Primärt mått:** CAR [ED, ED+10].
- **Sekundärt:** CAR [ED, ED+20] och andelen av uppgången [AD, ED−1] som går tillbaka.
- **Test:** tvåsidigt teckenbytestest på översynsmedel och wild cluster bootstrap per översyn, α 0,05. Femårsperioder redovisas sekundärt.
- **Öppen redovisning:** del 1 är en vidareutveckling av tidigare analyser, inte ett okört test.
  - Repot har redan testat CAR [ED+2, ED+100] (`mechanisms/RESULTS.md`). Tillägg 2007–11: −3,27 %, 2012–16: −1,30 %, 2017–21: −1,52 % (alla inte signifikanta). 2022–26: −4,86 % (p cirka 0,055). Inga signifikanta värden för borttag.
  - Även repots figur med medelvärden efter ED (`fig_09_car_effective.csv`) sågs innan specifikationen skrevs.
  - Det nya är de kortare fönstren direkt efter handelsdagen och återgångsandelen.
- **Styrka:** 487 händelser ger inte 487 oberoende observationer. Händelser i samma översyn sker samtidigt, därför klustras inferensen på översyn (39). Långa efterfönster tappar händelser genom avnoteringar.

## Del 2: tvillingaktier

### Hur det fungerar, med ett exempel

SSAB har A- och B-aktier. Under 2023–2026 låg B i OMXSB hela tiden, medan A gick in och ut vartannat halvår.

När A läggs till köper indexfonderna A men inte B. Det syns i FI-datan: 2025H1 köpte indexfonderna SSAB A för 0,67 % av A-aktierna.

Man räknar skillnaden i avkastning mellan A och B, dag för dag:
- **Före beskedet** ska skillnaden vara nära noll.
- **Om indexköpen pressar upp A men inte B** öppnar sig en skillnad.
- **Om skillnaden sedan krymper** var trycket tillfälligt. Det visar inte vilken handel som stängde den: A kan falla tillbaka, eller B kan stiga ikapp. Därför redovisas båda aktiernas prisbanor, inte bara skillnaden.
- Måttet är förändringen i det normala prisgapet. Aktieslagen behöver inte kosta lika mycket, eftersom rösträtt, likviditet och omvandlingsrätt skiljer sig.

### Första steget i FI-datan (2019–2026, 24 händelser)

- Indexfondernas innehav i det aktieslag som byter status ändras i snitt med 0,74 % av aktieslagets aktier, i rätt riktning.
- **Systeraktien utanför indexet:** indexfonderna äger ingenting eller nästan ingenting av den, före och efter (högst 0,23 miljoner aktier, i SSAB A). Indexköpen träffar bara det ena slaget.
- **Systeraktien också i indexet** (SSAB, Volvo, Industrivärden): innehavet i systeraktien rör sig också. Det beror sannolikt på fondflöden under kvartalet. FI-datan är kvartalsvis.
- Skript: `twin_first_stage.py`.

### Urval

- 58 användbara händelser (27 tillägg, 31 borttag) i 29 översyner och 17 bolag, enligt den nya genomgången.
- Med kurser som redan finns i repot är det 39–42 händelser i 11–12 bolag. Resten kräver LSEG-hämtning av NCC A, Ratos A, Sweco A och Bonava A.
- **Ska stämmas av:** Codex tidigare pilot hade 34 parhändelser i 8 bolag, varav 11 i 4 bolag där systeraktien låg utanför indexet. Skillnaden mot de 58 kan bero på olika krav på kursdata och noteringsdatum. Den låsta händelselistan ska förklara varje skillnad.
- Efter planerade uteslutningar (Stora Enso 6 händelser, systeraktier med för lite handel, fönster kring bud och fusioner) återstår cirka 45–50.
- Koncentrationen är hög: SSAB står för 12 händelser.
- I 24 händelser ingår systeraktien i indexet både före och efter. I 34 står den utanför.

### Vad varje utfall betyder

| Utfall | Tolkning |
|---|---|
| Skillnaden öppnar sig och stängs efter handelsdagen | Tillfälligt prisryck som handeln mellan tvillingarna inte genast tar bort. Gränser för arbitrage även mellan nästan identiska aktier |
| Skillnaden öppnar sig och består | Prisryck eller likviditetspremie. Går inte att skilja åt, så förändringen i likviditet redovisas |
| Ingen skillnad, båda aktierna rör sig lika | Antingen sprids efterfrågan helt till systeraktien, eller så är det bolagsnyheter. Går inte att avgöra, och det sägs i förväg |
| Brus | Styrkan räckte inte. Redovisas som begränsning med den minsta effekt som datan kan upptäcka |

**Styrka:** granskarens uppskattning är att datan kan upptäcka en skillnad på cirka 1,4 procentenheter, med tillägg och borttag sammanslagna. Det ska räknas om på placebofönster innan några händelsefönster öppnas.

### Förhandsspecifikation

Dateras och skickas till handledaren innan någon avkastning räknas.

**Händelser:** ett ordinarie aktieslag (A, B, C eller R) byter OMXSB-status, och systerslaget är noterat och oförändrat i samma översyn. Preferensaktier och D-aktier räknas inte som tvillingar.

**Uteslutningar:**
- Stora Enso, eftersom huvudnoteringen är i Helsingfors.
- Systerslag som handlas färre än 90 % av dagarna i [AD−60, ED+20].
- Händelser inom ±60 dagar från bud, fusion, blockaffär eller återköp i ett av slagen, till exempel Klövern och Corem 2021.
- Händelser där något av slagen samtidigt byter status i OMXS30.

**Utfall:**
- **Primärt:** skillnaden i avkastning över [AD−1, ED+1], med tecknet vänt för borttag, och tillägg och borttag sammanslagna.
- **Medprimärt:** återgång över [ED, ED+20].
- **Sekundärt:** [AD−1, AD+1], [AD+2, ED−2] och [ED−1, ED+1], med Holm-korrektion.
- **Placebo:** [AD−60, AD−21] och [AD−20, AD−2].

**Inferens:**
- Randomisering mot placebofönster för varje par, med samma längd och årstid men utan händelse.
- Både medel per händelse och medel per bolag (17 bolag).
- Ett bolag i taget utelämnas.

**Explorativt:**
- Aktieslag som går att omvandla, till exempel Volvo, SCA och Stora Enso (A till B eller R), jämfört med slag utan omvandlingsrätt.
- Resultat med och utan Volvo.

## Data

| Behövs | Läge |
|---|---|
| Dagskurser och volym för indexerade aktier och de flesta systeraktier | LSEG-panelen hos Ludvig |
| Dagskurser för NCC A, Ratos A, Sweco A och Bonava A | Hämtas från LSEG. Ungefär 10 minuter |
| FI-innehav per ISIN 2018Q4–2026Q2 | Finns, och första steget är kört |
| Bolagsordningar: omvandlingsrätt per bolag och datum | Hämtas från bolagens webbplatser |
| Bud, fusioner och blockaffärer | Nasdaqs bolagshändelser, pressmeddelanden och repots fil över skäl till borttag |
| OMXS30-ändringar | Finns i repot |

## Risker och hur de hanteras

- **Litet urval och hög koncentration:** förhandsspecifikation, placebobaserad inferens, ett bolag i taget utelämnat och den minsta upptäckbara effekten redovisad.
- **Indexet väljer det mest omsatta slaget**, ibland efter en händelse som påverkar röstpremien: placebofönster före beskedet och uteslutning kring bud och blockaffärer.
- **Likviditetspremie kontra prisryck:** återgången efter handelsdagen är det rena måttet och är därför medprimär.
- **Del 2 förklarar inte varför effekten försvann i USA.** Den testar mekanismen med substitut som G&S citerar och skrivs fram så.
- **Tidsrisk:** är del 2 inte klar senast 20 november flyttas den till en bilaga.

## Nyhetsvärde

- Ingen tidigare studie har, så långt vi har sökt, använt systeraktien som jämförelse vid indexändringar.
- De närmaste är:
  - Betzer, van den Bongard och Goergen (2017): sammanslagning av aktieslag och indexmedlemskap i Tyskland.
  - Froot och Dabora (1999): tvillingaktier som Royal Dutch/Shell.
  - Neumann (2003) och Ødegaard (2007): prisskillnader mellan aktieslag i Danmark och Norge.
- Svenska studier av OMXSB och OMXS30 har inte använt aktieslag.
- Del 1 är beprövad metod. Det nya är svensk evidens där effekten finns kvar.

## Struket och varför

- **Förutsägbarhet före beskedet:** G&S ger den "only a limited role". Den kräver dessutom fritt handlat börsvärde, sektorer och historiska regelversioner som inte finns.
- **Regeländringen 2021 som bevis:** resultatet håller inte för olika startår. Två av tretton startår ger p under 0,05.
- **Slutauktionen:** SHoF:s orderboksdata finns men täckning och fält är obekräftade, och prisrörelsen i Sverige sker inte på handelsdagen.
- **Fonders indexbyten:** få händelser, okända handelsdagar och ESG-uteslutningar som kan bära information.
- **Blankning:** FI:s historik täcker bara positioner över 0,5 %. Samlade positioner finns bara som ögonblicksbild sedan 2022.

## Tidsplan

| Datum | Steg |
|---|---|
| Mån 2 nov | Förhandsspecifikationen till Klug. Ludvig börjar del 1. LSEG-hämtning av fyra systerslag |
| Fre 6 nov | Del 1 klar. Händelselistan för del 2 låst |
| Fre 20 nov | Del 2 klar, annars bilaga |
| Från 3 nov | Replikationskapitlet skrivs parallellt |
| Mån 7 dec 10:00 | Inlämning |

## Källor

- Greenwood, R. och Sammon, M. (2025). The Disappearing Index Effect. *Journal of Finance*. HBS Working Paper 23-025 för multiplikatorer och förklaringar. NBER Working Paper 30748, figur 9, för återgång per decennium.
- Wurgler, J. och Zhuravskaya, E. (2002). Does Arbitrage Flatten Demand Curves for Stocks? *Journal of Business*.
- Betzer, A., van den Bongard, I. och Goergen, M. (2017). *Journal of International Financial Markets, Institutions and Money* 49.
- Froot, K. och Dabora, E. (1999). *Journal of Financial Economics*.
- Neumann, R. (2003). *European Financial Management* 9(3). Ødegaard, B. A. (2007). *Journal of Banking and Finance* 31(12).
- Nasdaq. OMX Stockholm Benchmark Index Methodology. Nordic All-Share Methodology.
- Repo: `output/omxsb_replication_2007/`. Arbetsfiler: `twin_events.csv`, `twin_first_stage.py`, `analyser_claude.zip`.
