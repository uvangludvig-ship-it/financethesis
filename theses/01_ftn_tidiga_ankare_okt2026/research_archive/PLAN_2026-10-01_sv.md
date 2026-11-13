# PLAN.md: BE451-uppsatsen om Fondtorgsnämnden

Senast uppdaterad 1 oktober 2026. Deadlines enligt kursen: slutuppsats i Canvas och replikationspaket (zip) till Anneli Sandbladh **7 december kl. 10.00**, presentation och opposition **före 12 december**, definitiv version i Publish Thesis **18 december kl. 18.00**. Halvtidsmöte i november på handledarens datum.

## 1. Forskningsfrågan

**Does selection by a public fund procurement agency move private money? Evidence from Sweden's premium pension procurements.**

Operativt: får fonder som Fondtorgsnämnden väljer nettoinflöden från investerare utanför premiepensionen, jämfört med de fonder som lade anbud och förlorade, och tappar bortvalda fonder pengar utanför PPM utöver den mekaniska överflyttningen?

Varför den frågan: den är intressant oavsett utfall. Ja betyder att en statlig myndighets val styr privat kapital (certifiering). Nej betyder att effekten stannar inne på plattformen, i linje med Berk och Green (2004) där investerare reagerar på avgifter och avkastning, inte på stämplar. Mekanismen (information mot pris) går att skilja åt eftersom detaljistavgiften utanför PPM inte ändras av upphandlingen. Ingen akademisk studie av reformen finns ännu.

Skriv om frågan i era egna ord innan den går till handledaren. Kursen förbjuder AI-skriven uppsatstext.

## 2. Ankaret och replikationen

**Sialm, Starks & Zhang (2015), "Defined Contribution Pension Plans: Sticky or Discerning Money?", Journal of Finance 70(2), 805–838.**

De delar varje fonds flöden i pensionspengar (DC) och övriga pengar (icke-DC), visar att DC-flöden är mer prestationskänsliga (Tabell III: DC Low 1,194, Mid 0,236, High 1,776 mot icke-DC 0,328, 0,284, 0,487), och visar med 11-K-data att känsligheten kommer från sponsorernas menyändringar, inte från deltagarna (Tabell VIII). DC-flöden förutsäger inte framtida avkastning, icke-DC-flöden förutsäger sämre avkastning (Tabell IX).

PPM mot icke-PPM är samma uppdelning. Tre saker vi kan göra som de inte kunde: vi observerar flöden (nettohandel per fond och månad) i stället för att imputera dem ur årliga tillgångar; vi observerar sponsorns hela beslutsmängd (alla anbudsgivare, kvalificerade, intervjuade, vinnare, datum); och Sverige bytte regim inom samma system, från öppet fondtorg till kuraterad meny, kategori för kategori från 2024.

Replikation tabell för tabell:

| SSZ | Svensk motsvarighet |
|---|---|
| Ekv. 1–2, flödesdefinitioner | PPM-flöde = nettohandel / MV föregående period (eller deras formel med MV och avkastning); icke-PPM-flöde = Morningstar-flöde för fonden (alla andelsklasser) minus PPM-flöde, matchat på ISIN |
| Tabell II, volatilitet och autokorrelation | Samma, årsdata och månadsdata 2001–2026 |
| Tabell III, Sirri-Tufano PPM mot icke-PPM | Rank föregående år bland alla aktiefonder sålda i Sverige; samma kontroller; om omsättning saknas i Morningstar: kör med och utan och skriv ut skillnaden |
| Tabell IV, alternativa benchmark | Morningstar-kategori; Carhart med SHoF:s svenska faktorer (Sverigefonder) och Frenchs globala (övriga) |
| Tabell V, delperioder | Före och efter 2024, per kategori i takt med upphandlingarna |
| Tabell VII, in- och utträde | Fonders in- och utträde ur fondtorget |
| Tabell VIII, sponsor mot deltagare | Sponsorflöde = flöden i tilldelnings- och avvecklingsmånader; deltagarflöde = resten |
| Tabell IX, förutsägbarhet | Framtida kategorijusterad avkastning och alfa på PPM-flöde, icke-PPM-flöde och en indikator för FTN-val |

Kör replikationen på årsdata först, som de, och visa månadsdata som robusthet.

## 3. Utvidgningen

Den sitter inuti SSZ:s Tabell VIII och IX, inte vid sidan av dem.

1. **Vad väljer sponsorn på?** P(vinst | anbud) på prestationsrank, avgift, storlek, svensk/utländsk, bankägd. Beslutsmängden är observerad (rapporterna), vilket Pool, Sialm & Stefanescu (2016) och SSZ saknade.
2. **Reagerar icke-PPM-pengarna?** Icke-PPM-flöde för vinnare mot kvalificerade förlorare runt tilldelningsdatum. Tvåvägs fixed effects (fond, kategori × månad), kluster på fond, wild cluster bootstrap, förtrendsplot, placebo i kategorier som ännu inte upphandlats, dos-respons i PPM-andel av fondens kapital. Det mekaniska sponsorflödet är borträknat per konstruktion eftersom utfallet är icke-PPM.
3. **Väljer sponsorn rätt?** SSZ:s Tabell IX med FTN-valet som regressor, med uttalad minsta detekterbara effekt (kort efterperiod).

Mot examinatorns lista (slide 10) uppfyller detta tre kriterier: nytt dataset, ny tillämpning (offentlig upphandling), samma metod på ny fråga (spillover).

Sekundärt test om tid finns: Allra- och Falcon-avregistreringarna 2017–2019 som förtest av sponsorkanalen före reformen.

## 4. Data (verifierat 1 oktober 2026)

**Fondtorgsnämnden, upphandlingsrapporter.** https://www.ftn.se/marknadsdialog/upphandlingsrapporter.html. Elva avslutade upphandlingar med tilldelningsdatum: aktiva Europafonder 25 mars 2024; globalt index och Europaindex 31 oktober 2024; aktiva nordiska stor/medel och nordiska småbolag 19 februari 2025; aktiva svenska stor/medel och passiva svenska 27 augusti 2025; aktiva globala 24 februari 2026; europeiska småbolag och svenska småbolag 28 maj 2026; globala teknologifonder 22 september 2026. Varje rapport ger alla anbudsgivare med namn, kvalificerade, intervjuade, vinnare med ISIN och upphandlad avgift, fondlistan i kategorin före upphandlingen, kapital och sparare, avgifter före och efter, annonseringsdatum och anbudsfrist, fördelningsregel för flyttat kapital. Vikter: kvalitet 75 procent, kostnad 25.

**Pensionsmyndigheten, månadsstatistik om premiepensionens fonder.** https://www.pensionsmyndigheten.se/statistik-och-rapporter/statistik/statistik-for-premiepension (2025–2026) och https://www.pensionsmyndigheten.se/statistik-och-rapporter/statistik/statistik-for-premiepension/aldre-manadsstatistik-premiepension (2001–2024, 288 filer). En Excelfil per månad. Fliken "Fondval & marknadsvärde": fondnummer, fondnamn, antal fondval (kvinnor, män, totalt), marknadsvärde, "Handel, netto", fondkategori, fondtyp, förvaltare, aktiv/passiv, svensk/utländsk, flagga "Upphandlad fond". Fliken "Fondstatistik": avkastning 1–60 månader, avgift netto (efter rabatt) och brutto (TER), risk, Sharpe, startdatum, ISIN. Äldre filer har annat format; räkna med två parsers. Kontrollera definitionen av "Handel, netto" i fliken "Beskrivning av mått".

**SHoF Fund Data Morningstar.** https://www.houseoffinance.se/data-center/shof-fund-data-morningstar/. Över 9 000 fonder till salu i Norden, dagliga kurser, daglig TNA och nettoflöde per fond och andelsklass, avgiftsfil, historik till 1970. Tillgång kräver att SSE har Morningstar Direct, vilket tidigare uppsatser tyder på. Mejla SHoF och biblioteket vecka 1.

**SHoF Fama-French-faktorer** för Sverige: https://www.houseoffinance.se/data-center/fama-french-factors/. Globala faktorer från Kenneth Frenchs bibliotek.

### Så används datan

En primärkälla per variabel, en andra källa för validering på ett delurval, aldrig två källor blandade i samma variabel.

| Variabel | Primärkälla | Validering / reserv |
|---|---|---|
| PPM-flöde, PPM-kapital, antal sparare | Pensionsmyndighetens månadsfil ("Handel, netto", marknadsvärde, fondval) | Fondens MV-förändring minus avkastning (SSZ ekv. 1) |
| Totalt fondkapital och totalt nettoflöde per fond | SHoF Morningstar (daglig TNA och nettoflöde per andelsklass, summerat till fond och månad) | Lipper-fondflöden i LSEG Workspace på ett delurval |
| Icke-PPM-flöde | Totalt nettoflöde minus PPM-nettohandel, i SEK, fondnivå | Samma på enbart PPM:s andelsklass (ISIN i PM-filen) |
| Avkastning och prestationsrank | Morningstar NAV total return i SEK; rank föregående 12 månader bland alla aktiefonder sålda i Sverige | PM-filens 12-månadersavkastning för plattformsfonder |
| Avgift | PM-filens brutto-TER (plattformsfonder); Morningstars avgiftsfil (alla) | Lipper |
| Familjestorlek, ålder, kategori | Morningstar (branding name, startdatum, Morningstar-kategori) | PM-filens förvaltare och kategori |
| Omsättning | Morningstar om fältet finns, annars Lipper; saknas båda: utelämna och skriv ut | |
| Volatilitet, kategoriflöde | Beräknas ur månadsavkastning och kategorisummor | |
| Valutakurser (EUR, USD till SEK, månadsslut) | Riksbanken | LSEG Workspace |
| Benchmarkindex (MSCI Europe NR, MSCI World NR, OMXSBGI m.fl., i SEK) | LSEG Workspace | Morningstar |
| Faktorer | SHoF (Sverige), Kenneth French (globalt) | |
| Behandling: anbudsgivare, vinnare, datum, befintliga fonder | FTN:s upphandlingsrapporter | Tilldelningsbesluten på e-Avrop; begär utvärderingslistor från FTN (offentlig handling) |
| ISIN för förlorande anbudsgivare | LSEG Workspace (sök på fondnamn) | Morningstar |

Regler: rådata sparas orört med nedladdningsdatum; alla transformationer i kod; flöden winsoriseras vid 2,5 procent som i SSZ; aktiefonder är huvudurvalet (alla upphandlade kategorier är aktiekategorier); valutor konverteras vid månadsslut; PM-filen är per månadsslut, Morningstar summeras till samma datum. Rapporterna namnger alla anbudsgivare men inte alltid vilka som kvalificerade sig; den listan begärs ut från Fondtorgsnämnden i vecka 1, med "alla förlorande anbudsgivare" som reservkontroll.

## 5. Uppsatsens form

Målbild 25–35 sidor, sju tabeller och tre figurer i huvudtexten, resten i appendix.

| Nr | Innehåll | SSZ |
|---|---|---|
| Tabell 1 | Beskrivande statistik 2001–2026 och de elva upphandlingarna | Tabell I |
| Tabell 2 | Volatilitet och autokorrelation, PPM mot icke-PPM | Tabell II |
| Tabell 3 | Styckvis linjär flödes-prestationsregression, PPM mot icke-PPM, med SSZ:s koefficienter i egen kolumn | Tabell III |
| Figur 1 | Flödes-prestationskurvan, PPM mot icke-PPM | Figur 1–2 |
| Tabell 4 | Före och efter reformen, per kategori | Tabell V |
| Tabell 5 | Vad förutsäger vinst i upphandlingen | Tabell VIII:s logik |
| Figur 2 | Event study: icke-PPM-flöden, vinnare mot kvalificerade förlorare, med förtrend | ny |
| Tabell 6 | DiD-estimat med placebo och bootstrap; huvudresultatet | ny |
| Tabell 7 | Förutsägbarhet med FTN-val | Tabell IX |
| Figur 3 | Dos-respons mot PPM-andel av kapital | ny |

Format enligt syllabus och introföreläsningen: intro 2–4 sidor som förhandsvisar siffrorna och listar bidraget; related literature under en sida (SSZ; Pool, Sialm & Stefanescu 2016 JF; Cookson, Jenkinson, Jones & Martinez 2021 RFS; Jenkinson, Jones & Martinez 2016 JF; Dahlquist, Martinez & Söderlind 2017 RFS; Berk & Green 2004 JPE; Sirri & Tufano 1998 JF; Sabbatucci, Tamoni & Xiao 2026 WP); ingen innehållsförteckning; ingen pedagogisk förklaring av OLS eller DiD; självbärande tabellrubriker; 12 punkter, enkelt radavstånd, officiell framsida; AI-appendix; replikationspaket med README.

## 6. Vecka för vecka

**Vecka 1, 1–7 oktober: go eller no-go.**
- Ladda ner alla månadsfiler från Pensionsmyndigheten och de elva upphandlingsrapporterna.
- Mejla SHoF och biblioteket om tillgång till fonddatat.
- Bekräfta definitionen av "Handel, netto".
- Matcha ISIN för de 35 anbudsgivarna i Europarundan mot Morningstar. Går 30 av 35 så kör vi.
- Skriv forskningsfrågan i egna ord och skicka till handledaren med beslutsfrågan: icke-PPM-flöden eller överlevnad som huvudutfall?
- Starta AI-loggen (verktyg, datum, syfte, vad som ändrades).

**Vecka 2–3, 8–21 oktober: panelen.**
- Fond × månad från Pensionsmyndigheten: fondnummer, ISIN, MV, sparare, nettohandel, avgifter, kategori, upphandlad-flagga.
- Morningstar: TNA och flöden per andelsklass aggregerat till fondnivå, avkastning, avgifter, familj, startdatum.
- PPM-flöde och icke-PPM-flöde enligt SSZ ekv. 1–2, årsdata först.
- Behandlingsfil från rapporterna: per kategori alla anbudsgivare, kvalificerade, intervjuade, vinnare, befintliga fonder, annonseringsdatum, tilldelningsdatum, avvecklingsmånad.
- Rådata orört, varje transformation dokumenterad. Replikationspaketet byggs från dag ett.

**Vecka 4, 22–28 oktober: rådata talar.**
- Tre figurer före någon regression: SSZ:s Figur 1 på svenska data; råa icke-PPM-flöden för vinnare och kvalificerade förlorare månad för månad runt varje tilldelning; samma för avvecklade fonder.
- Beslut: syns inget i flödena blir överlevnad och storlek huvudutfall. Beslutet tas här, inte efter regressionerna.
- Figurerna till handledaren.

**Vecka 5–6, 29 oktober–11 november: replikationen.**
- Tabell 2, 3 och 4 i SSZ:s exakta form, kolumn med deras siffror bredvid våra.
- Omsättning med och utan.
- Replikationen fryses innan utvidgningen börjar.

**Vecka 7, 12–18 november: utvidgningen.**
- Tabell 5, Figur 2, Tabell 6, Tabell 7, Figur 3.
- Balanstabell vinnare mot kvalificerade förlorare före tilldelning.
- Wild cluster bootstrap, minsta detekterbara effekt, placebo.
- Halvtidsmötet: ta med Tabell 3, Figur 2 och Tabell 6, inget annat.

**Vecka 8, 19–25 november: robusthet och text.**
- Robusthet: SSZ Tabell IV-varianter, månadsdata, leave-one-round-out, Callaway-Sant'Anna som märkt utvidgning.
- Introduktionen klar, related literature klar.

**Vecka 9, 26 november–2 december: hela manuset.**
- Data och metod, resultat, diskussion, slutsats.
- AI-appendix ur loggen.
- Replikationspaket: rådata, kod som skapar varje tabell och figur, datadictionary, README med körordning.

**Vecka 10, 3–7 december: läs som examinatorn.**
- Byt uppsats med varandra. Stryk allt som förklarar standardmetod, allt som är textbook, varje mening som låter genererad.
- Varje källa i texten finns i listan och tvärtom; ankarförfattarna rättstavade; siffrorna i intron stämmer med tabellerna.
- Inlämning 7 december kl. 10: Canvas och zip till Anneli Sandbladh.

**Efter 7 december:** presentation och opposition före 12 december; endast mindre korrigeringar; Publish Thesis senast 18 december kl. 18.

## 7. Arbetsdelning

Två spår som möts vecka 4. Dataspår: Pensionsmyndighetens filer, Morningstar, ISIN-matchning, flödesdefinitioner, panelen, replikationspaketet. Händelsespår: upphandlingsrapporterna, behandlingsfilen, balanstabellen, litteraturen, introduktionen. Den som bygger panelen skriver inte intron.

## 8. Beslutspunkter

- Vecka 1: ISIN-matchning och SHoF-tillgång. Faller de: Tabell 2–5 och 7 går att göra helt på Pensionsmyndighetens data (sponsorsidan av SSZ), och överlevnad/storlek blir utfall.
- Vecka 4: huvudutfall flöden eller överlevnad, utifrån råfigurerna.
- Vecka 7: är DiD-estimatet noll, skriv nollan som resultat med mekanism och styrka. Byt inte fråga.

## 9. Vad examinatorn graderar på (verifierade citat ur syllabus och introföreläsning)

- "I grade the theses, not the tutors." Kriterier: useful, correct, relevant, contribution, independence.
- "Standard for BSc thesis: replication and extension of a (recent) published paper in a top journal ... The extension needs to be meaningful. Avoid default option of applying the question to Nordic countries unless meaningful."
- "Replication is just the first step to finding something new & interesting, it is a guarantee of solid foundations."
- "A robust research question is a question that is interesting independently of the results."
- "Do not chase 'statistical significance'."
- "Minimum detectable effect: check the power of your test."
- "Simpler is better! ... If you cannot justify why you use a complicated method, do not use it."
- "Introduction (2-4 pages) ... Intro = self contained summary of paper. Related Literature (<1 page) ... It is not a review of the literature!"
- "NO to tables of contents; YES to table captions that are detailed."
- "Do not write it as a student project with a table of contents, a complete literature review, off-topic digressions, and pedagogic explanation of standard methodology."
- "You can make use of AI but you must submit an AI-appendix ... do not use AI to directly write part of your thesis ... AI has a very distinctive and often very convoluted writing style."

## 10. Det som får uppsatsen att tappa

Fler än sju tabeller i huvudtexten. Ett tillägg utanför SSZ:s form. En introduktion utan siffror. Att kalla tilldelningen exogen i stället för "vald bland dem som var goda nog att lägga anbud". Att stryka en kontrollvariabel utan att säga det. Inferens på sex vinnare utan bootstrap. Text som låter genererad.

## 11. Underlag i repot

- `non_winners/analysis/ANALYSIS_winners_vs_nonwinners.md`: vad som skiljer de 25 vinnarna från de 635 övriga.
- `old_winners/text/2024_per_hiller_the_smooth_transition.txt`: mallen för en reformstudie med nollresultat.
- `course_context/`: syllabus, introföreläsning, handledarlista, ekonometrimodul.
- `synopsis/BScThesis_Fox_Pauli_Uvang.pdf`: inlämnad synopsis.
