# Ämnesval för synopsis — rankad shortlist (6 september 2026)

Syfte: hitta två ämnen till synopsisen (deadline 9 sep kl. 13.00) med
realistisk chans att vinna Per Hiller- eller Staffan Viotti-priset.

Underlag: nio parallella litteratursökningar (Google Scholar, Crossref,
OpenAlex, SSRN, NBER, förlagssidor, Riksbanken, FI, riksdagen), ett
feasibility-test på vår egen CapIQ-export (6 914 deals 2025–2026) samt en
genomgång av alla 25 tidigare prisvinnare. Alla "kärnreferenser" nedan är
verifierade mot tidskrift/volym om inget annat anges. Citeringstal är
ungefärliga.

---

## 1. Vad som faktiskt vinner (25 vinnare 2011–2024)

- **21 av 25 replikerar en namngiven topptidskriftsartikel** och utvidgar den.
  Sedan 2019: 11 av 11.
- **13 av 25 använder svenska/nordiska data.** Den vanligaste pitchen är
  "Sverige/Norden ger ett renare test än USA-originalet" (12 av 25).
- **Kvasi-experimentell identifikation i 8 av 25** (DiD, RD, IV, chock), event
  study i 5, panel-FE vanligast.
- **Unika eller handbyggda data i ~14 av 25** (data på begäran från myndighet
  eller bolag, tickdata, handinsamling).
- **Nollresultat vinner:** 7 av 25 har null/motsägelse som huvudresultat, och 4
  av de senaste 6 vinnarna motsäger sin ankarartikel.
- **Formen:** ~25 sidor huvudtext, kursiverad forskningsfråga i intro,
  "our contribution is threefold"-stycke, magnituder i abstract, egen
  robusthetssektion, placebo.
- Viotti-priset går nästan alltid till marknader/asset pricing/makrofinans;
  Hiller-priset är bredare och premierar naturliga experiment i corporate
  finance.

Fullständig analys: se avsnitt 7.

---

## 2. Feasibility-fakta som styr valet

**CapIQ-exporten (DACH + Norden, 2025–2026, 6 914 deals):**

| Variabel | Täckning |
|---|---|
| Köpartyp (strategisk/finansiell) | 92 % |
| Target privat bolag | 71 % |
| Target sponsor-status (PE-ägd/ej) | ~50 % |
| Deal value | 18 % |
| Target LTM-omsättning | 17 % |
| **EV/EBITDA** | **2,8 %** |
| Premie (noterade targets) | 2,3 % |
| Rådgivare till target/säljare | 14 % |

Slutsats: **allt som bygger på multiplar för privata bolag är för tunt**
(kanske 1 500 observationer på tolv år, skevt urval). Det slår ut idéerna
"PE- vs strategiska multiplar efter räntechocken 2022", "rådgivarens fixed
effects på pris" och "succession discount" som rena prisstudier. Däremot är
CapIQ utmärkt för att identifiera **vilka svenska bolag som förvärvades, när
och av vem** (1 375 svenska targets per år), vilket kan kopplas till Serrano
för utfall före och efter affären.

**Serrano (SHoF):** bokslut för alla svenska AB sedan 1997, SCB-företagsdata,
konkurs, koncernregister från Bisnode. Åtkomst via SWAMID för SSE-studenter.
Variabellistan ligger bakom inloggning: **verifiera dag 1 att säteskommun,
antal anställda, räntekostnader, utdelning och koncernmoder finns.**

**Åtkomst som kursen ger (enligt `course_context/README.md`):** WRDS
(Compustat, CRSP, klasskod 5414d36b), S&P Capital IQ (workshop 8 sep),
**Modular Finance Holdings** (workshop 11 sep: ägardata per nordiskt noterat
bolag, inklusive retail-, institutions- och insiderandel), LSEG Workspace
(workshop 15 sep), SHoF Data Center (Serrano, FinBas) och bibliotekets
databaser (bland annat Retriever Business).

**Övrig fri data som verifierats:** Riksbankens SWEA-API (räntor 1985–),
Riksbankens innehav per ISIN och auktionsdata (2012–2026), Riksbankens
event-study-databas (WP 445, 269 penningpolitiska händelser 2004–2024,
nedladdningsbar), FI:s insyns- och blankningsregister, jkpfactors.com
(faktorer för SWE/NOR/DNK/FIN), ECB EA-MPD.

Att Holdings ingår stärker ämne D (retail-ägarandel per aktie som
behandlingsintensitet i ISK-testet) och gör ägar-/efterfrågebaserade
asset pricing-ämnen (Klugs område) fullt genomförbara.

---

## 3. Rankad shortlist

### Tier 1 — rekommenderas till synopsisen

#### A. Förvärv av svenska privata SME: låser nytt ägande upp tillväxt, och för vem?
*(Klose-nära. Corporate finance. Hiller-spår.)*

- **Forskningsfråga:** Lättar förvärv finansiella restriktioner i svenska
  privata målbolag, och skiljer sig effekten mellan PE-köpare, strategiska
  köpare och nordiska serieförvärvare (Lifco, Indutrade, Addtech m.fl.)? Är
  effekten störst i successionsdrivna affärer (ägare 60+)?
- **Ankare (verifierade):**
  - Erel, Jang & Weisbach (2015), "Do Acquisitions Relieve Target Firms'
    Financial Constraints?", *JF* 70(1), 289–328. 5 187 europeiska privata
    targets 2001–2008 (Amadeus): kassa faller, investeringar ökar efter
    förvärv, mest för små/restringerade bolag.
  - Boucly, Sraer & Thesmar (2011), "Growth LBOs", *JFE* 102(2), 432–453.
    839 franska LBO:er, matchad DiD: försäljning +12 %, anställda +18 %.
  - Cohn, Hotchkiss & Towery (2022), "Sources of Value Creation in Private
    Equity Buyouts of Private Firms", *Review of Finance* 26(2), 257–285.
  - Bernstein, Lerner & Mezzanotti (2019), "Private Equity and Financial
    Fragility during the Crisis", *RFS* 32(4), 1309–1373.
  - Smith, Yagan, Zidar & Zwick (2019), "Capitalists in the Twenty-First
    Century", *QJE* 134(4), 1675–1745 (ägarens icke-överförbara humankapital).
  - Jenter & Lewellen (2015), "CEO Preferences and Acquisitions", *JF* 70(6),
    2813–2852 (försäljningssannolikhet hoppar vid vd-ålder 65).
  - Olsson & Tåg (2025), "What Is the Cost of Privatization for Workers?",
    *JF* 80(4), 2107–2151 (svenska registerdata i JF, metodmall).
  - Bennedsen, Nielsen, Pérez-González & Wolfenzon (2007), *QJE* 122(2),
    647–691 (succession, danska register).
- **Replikation:** Erel m.fl.:s före/efter-design på svenska privata targets
  2015–2023 (CapIQ → orgnr → Serrano), matchade icke-förvärvade kontroller,
  staggered DiD (Callaway–Sant'Anna). Utfall: kassa, investeringar,
  cash-flow-känslighet, anställda, skuld, konkurs.
- **Extension och mekanism:** (i) tre köpartyper på samma målpopulation, vilket
  ingen kärnartikel gjort (litteraturen jämför PE mot "ingen affär");
  (ii) ägarens ålder från Bolagsverket/Retriever: successionsdrivna affärer
  testar två motsatta hypoteser: underinvestering före affären (→ större
  lyft) mot icke-överförbart humankapital (→ mindre lyft). Nollresultat är
  informativt i båda riktningarna.
- **Placebo:** affärer som annonserades men aldrig fullbordades (CapIQ-status).
- **Luckor i litteraturen (verifierade):** ingen kärnartikel om pris eller
  utfall beroende på säljarens ålder/successionsmotiv; ingen om nordiska
  serieförvärvare; nästan ingen kärnforskning om M&A i Norden/DACH efter 2004.
- **Prior art att citera:** Kärnä & Myers (2025), *Economics Letters* (Serrano
  + PitchBook DiD på svenska LBO:er); Andric, Genedy & Nordqvist (2026, SSE
  white paper) om arvsskattens avskaffande.
- **Data:** CapIQ (egen screen, 2015–2024 återstår att exportera), Serrano,
  Retriever Business/Bolagsverket för styrelseledamöters födelseår.
- **Risker:** namnmatchning CapIQ → organisationsnummer (räkna med 60–75 %
  träff, Serranos koncernregister kan användas som andra källa för
  ägarbyten); Serranos eftersläpning (senaste bokslut 2024); att handsamla
  ägarålder tar tid, gör det för ett delurval.
- **Tutor-fit:** Alvin Chen (corporate, labor and finance), Laszlo Sajtos.

#### B. Elpriskrisen 2022 per elområde och elstödet till företag
*(Skarpaste svenska naturliga experimentet. Corporate finance. Hiller-spår.)*

- **Forskningsfråga:** Hur absorberar privata företag en stor, kvasi-exogen
  kostnadschock, och förstärker finansiella restriktioner effekten på
  investeringar, sysselsättning och överlevnad? Fungerade elstödet 2023 som
  en likviditetsinjektion?
- **Institutionell variation:** Sverige delades i fyra elområden 2011.
  Under 2022 var spotpriset i SE3/SE4 flerfaldigt högre än i SE1/SE2
  (**verifiera årsmedel mot Nord Pool/Ei**). Elstöd till företag
  (förordning 2023:233) gick **bara** till SE3 (50 öre/kWh) och SE4
  (79 öre/kWh), tak 20 mnkr per koncern, ~17,5 mdkr utbetalt 2023.
- **Ankare (verifierade):**
  - Bartram, Hou & Kim (2022), "Real effects of climate policy: Financial
    constraints and spillovers", *JFE* 143(2), 668–696.
  - Brown, Gustafson & Ivanov (2021), "Weathering Cash Flow Shocks", *JF*
    76(4), 1731–1772.
  - Colmer, Martin, Muûls & Wagner (2024), "Does Pricing Carbon Mitigate
    Climate Change? Firm-Level Evidence from the EU ETS", *REStud*.
  - Ivanov, Kruttli & Watugala (2023), "Banking on Carbon", *RFS* 37(5).
  - Känzig (2021), "The Macroeconomic Effects of Oil Supply News", *AER*
    111(4), 1092–1125.
- **Identifikation:** trippeldifferens elområde × branschens elintensitet
  (SCB) × efter 2021, med bransch×år- och kommun-FE; gränsdesign med kommuner
  längs SE2/SE3- och SE3/SE4-gränsen; heterogenitet efter förutbestämd kassa,
  skuld och ålder; bunching kring 20 mnkr-taket i elstödet; DiD SE4 vs SE3
  vs SE2 på 2023–2024-utfall.
- **Mekanism:** finansiella restriktioner som förstärkare av reala chocker
  (Brown m.fl.). Noll: effektiv riskdelning/hedging bland SME, och att
  elstödet saknade likviditetsmotiv.
- **Data:** Serrano (kräver säteskommun, verifiera), Nord Pool/Ei-priser,
  SCB energianvändning per bransch. Allt finns, ingen extern begäran.
- **Risker:** säte ≠ produktionsort (använd enkoncernbolag/små bolag);
  fastprisavtal observeras inte (intention-to-treat); SE4 = Skåne kan skilja
  sig strukturellt (lång pre-period 2012–2021 hjälper).
- **Tutor-fit:** Valentin Schubert (climate finance, environmental economics),
  Laszlo Sajtos.

### Tier 1-alternativ (lika starka, välj efter smak och tutor)

#### C. Riksbankens företagsobligationsköp 2020–2022
*(Financial intermediation/marknader. Viotti-spår.)*

- Program med publika auktionsdata per ISIN, skarp behandlingsregel (SEK,
  icke-finansiellt, investment grade, begränsad löptid) och koppling till
  fastighetsbolagens obligationskris 2022–2023.
- Ankare: Todorov (2020), *JFE* 135; Grosse-Rueschkamp, Steffen & Streitz
  (2019), *JFE* 133; Arce, Gimeno & Mayordomo (2021), *Review of Finance* 25;
  Haddad, Moreira & Muir (2021), *RFS* 34; Boyarchenko, Kovner & Shachar
  (2022), *JFE* 144.
- Design: DiD berättigade vs icke-berättigade emittenter, event study kring
  tillkännagivande och första auktioner, BBB-/BB+-gräns, Serrano för
  realeffekter och "capital structure channel" (bank → obligation).
- Risk: liten emittentgrupp (~50–80 bolag). Verifiera programkriterier och
  datum mot Riksbankens sidor. Tutor-fit: Schubert.

#### D. Utdelningsmånadspremien och ISK-klientel i Sveriges komprimerade vårsäsong
*(Asset pricing. Viotti-spår. Låg datarisk.)*

- Sverige är extremfallet: nästan alla ex-dagar på sex veckor, minusränta
  2015–2019, och ISK (skatteneutralt mellan utdelning och kursvinst) som växt
  sedan 2012, med fribelopp 150 tkr 2025 och 300 tkr 2026.
- Ankare: Hartzmark & Solomon (2013), *JFE* 109(3), 640–660; Hartzmark &
  Solomon (2019), "The Dividend Disconnect", *JF* 74(5); Rantapuska (2008),
  *JFE* 88(2) (finska ex-dagar); Graham, Michaely & Roberts (2003), *JF* 58(6);
  Michaely (1991), *JF* 46(3); Jacob & Michaely (2017), *RFS* 30(9).
- Tre mekanismtest: substitution (koncentrerad säsong), "reaching for
  dividends" vid låg ränta, skatteklientel (ex-dagens prisfallskvot mot 1
  när ISK-andelen växer; DiD över aktier efter retail-ägarandel från
  Holdings, som kursen ger åtkomst till).
- Data: FinBas för kurser och utdelningar, Holdings för ägarandelar.
  Risk: få oberoende säsonger (klustra per år).
  Tutor-fit: Michael Klug. Examinatorns forskning ligger i asset pricing.

#### E. Vilken centralbank driver svenska räntor och aktier?
*(Makrofinans. Viotti-spår. Samma stil som 2023 års vinnare.)*

- Ankare: Hillenbrand (2025), *RFS* 38(4), 981–1013; Brusa, Savor & Wilson
  (2020), *Review of Finance* 24(2); Lucca & Moench (2015), *JF* 70(1);
  Savor & Wilson (2014), *JFE* 113(2); Cieslak, Morse & Vissing-Jørgensen
  (2019), *JF* 74(5).
- Test: koncentreras den sekulära nedgången i svenska 10-årsräntor (och
  vändningen 2022–2026) i fönster kring FOMC, ECB eller Riksbanken? Bär
  Riksbanksdagar en aktiepremie? All data gratis (SWEA, FinBas, EA-MPD).
- Risk: få Riksbanksmöten, överlappande fönster. Tutor-fit: Klug.

### Tier 2 — bra reserver

- **F. Räntechocken 2022–2023 och kassaflödeskanalen hos SME med rörlig
  ränta.** Ottonello & Winberry (2020), *Econometrica* 88(6); Ippolito,
  Ozdagli & Perez-Orive (2018), *JME* 95; Gürkaynak, Karasoy-Can & Lee (2022),
  *JF* 77(4); Greenwald, Krainer & Paul (2025), *JF* 80(6). Riksbankens
  event-study-databas ger överraskningar. Svagare identifikation (årsdata,
  sammanfaller med elprischocken).
- **G. Kvoteringshotet 2016–2017** (Ds 2016:32 i sept 2016, riksdagens
  avslag jan 2017): två motsatta chocker på samma bolag. Ahern & Dittmar
  (2012), *QJE* 127(1); Adams & Ferreira (2009), *JFE* 94(2); Bertrand m.fl.
  (2019), *REStud* 86(1). Billigt och exakt, men ämnet är "beprövat"
  (2011 och 2024 års vinnare).
- **H. FI:s insynsregister + Listing Act-tröskeln.** Cohen, Malloy &
  Pomorski (2012), *JF* 67; Akbas, Jiang & Koch (2020), *JF* 75; Jank,
  Roling & Smajlbegovic (2021), *JFE* 139. Fri data, men insiderstudier är
  vanliga; vinkeln måste vara regeländringen.
- **I. Minimikapitalets sänkningar 2010 och 2020.** Hombert, Schoar, Sraer &
  Thesmar (2020), *JF* 75(3); Andersen & Nielsen (2012), *RFS* 25(12).
  Robust men lågt "wow".

### Avråds (och varför)

- PE- vs strategiska **multiplar** efter räntechocken 2022, rådgivarens
  fixed effects på **pris**, succession discount som **prisstudie**: EV/EBITDA
  finns för ~3 % av dealsen.
- Blankningströskeln 0,1 %: positioner under 0,5 % är konfidentiella.
- 3:12-reformen 2026: bokslut finns först 2027.
- PFOF-förbudet: ingen retail-orderdata.
- Tullchocken 2025: närmaste metodartiklar ligger i *JIE*, inte på listan.
- LLM som **prediktor** av avkastning: fortfarande working-paper-territorium;
  LLM som **mätinstrument med validering** (Li m.fl. 2026, *RFS* 39(1)) är
  däremot acceptabelt som modul i ämne A.

---

## 4a. Slutlig ranking 7 sep kväll: se `05_fem_alternativ.md` (sju kandidater; rekommendation H + I, reserv J)

Efter en andra idérunda utan Klose-krav och två ytterligare verifierade
kandidater (F granskningslagar, G lokal konsolidering, H vinster i
välfärden) är rekommendationen **ämne 1 = H, ämne 2 = G**, med F som
reserv om Serrano saknar kommun. Poäng (orig/ident/genomf/pris): H 7/7/8/8,
G 8/6/6/9, F 8/6/7/8, A 7/5/6/7, B 7/5/6/6. Avsnitt 4 nedan är den
tidigare rekommendationen (A + B) och behålls som historik.

## 4. Tidigare rekommendation (6 sep, efter red-team av A, B, D)

Tre kandidater granskades adversariellt (tidigare uppsatser via OpenAlex/
DiVA/LUP, scoop-risk, identifikation, institutionella fakta). Betyg 1–10:

| Ämne | Originalitet | Identifikation | Genomförbarhet | Prispotential |
|---|---:|---:|---:|---:|
| A. Förvärv av svenska SME efter ägartyp | 7 | 5 | 6 | 7 |
| B. Elprischocken 2022 per elområde | 7 | 5 | 6 | 6 (8 som likviditetsuppsats) |
| D. Utdelningssäsong och ISK | 6 | 4 | 7 | 5 (7–8 om ledd av prispress) |

**Rekommendation: Ämne 1 = A, ämne 2 = B.** D behålls som dokumenterad
reserv i `03b_topic_D_reserve.md`.

Skälen: (i) B har högst prispotential av kandidaterna till ämne 2 när den
skrivs som en uppsats om företagslikviditet (kassa, skuld, leverantörs-
skulder, utdelning) snarare än regional energiekonomi; (ii) luckan är
bekräftad: Bălașa & Pollitt (2026, Cambridge EPRG, med SSE-koppling) är
enbart deskriptiv och efterlyser firm-nivådata, och ingen europeisk
företagsstödsordning har en kausal firm-nivåutvärdering; (iii) D:s
ISK-del förväntas ge ett nollresultat och en nordisk H&S-replikation finns
redan (Peltomäki 2019, Aalto). Nackdelen med A + B är att båda bygger på
Serrano och DiD; det kompenseras av att frågorna, chockerna och
litteraturerna är helt olika.

Verifierade fakta för B (Nord Pool, årsmedel öre/kWh SE1/SE2/SE3/SE4):
2021 43/43/67/82; 2022 63/66/137/162; 2023 46/46/59/80. Gapet öppnade
mitten av 2021 och stängde nov–dec 2022, så behandlingen är kontinuerlig,
inte en "efter 2021"-dummy. Elstöd till företag (SFS 2023:233): SE3 50 och
SE4 79 öre/kWh på förbrukning okt 2021–sep 2022, tak 20 mnkr per koncern,
ansökan 30 maj–25 sep 2023, förväntat ~29 mdkr. Stödet är sekretessbelagt
på företagsnivå, så det måste imputeras; bunching vid taket har ingen
styrka. Ett överlappande nationellt stöd till elintensiva företag måste
räknas bort.

Viktiga justeringar av A efter granskningen: ägarens ålder är inte ett
instrument utan en heterogenitetsdimension; huvudresultatet är skillnaden
mellan ägartyper (difference-in-DiD); bokföringsartefakter efter koncern-
inträde (koncernbidrag, fusion in i moderbolaget) måste hanteras explicit.
Tidigare arbete att positionera mot: Kärnä & Myers (2025, Economics
Letters), El Ghoul, Gong & Guedhami (2024, RIBF).

Inget av ämnena kommer från handledarnas lista, så regeln "högst ett
tutor-inspirerat ämne" är oproblematisk. Synopsisutkast:
`03_synopsis_draft.md`.

---

## 5. Vanliga referensfel att undvika (verifierade)

Synopsisen underkänns om huvudreferenserna ligger utanför listan. Dessa
"kända" artiklar är **inte** i godkända tidskrifter:

- Alstadsæter, Jacob & Michaely (2017) → *Journal of Public Economics*, inte
  JFE. Använd Jacob & Michaely (2017), *RFS*.
- Cloyne, Ferreira, Froemel & Surico (2023) → *JEEA*, inte REStud.
- Boissel & Matray (2022, *AER*) → **tillbakadragen**.
- Song, Wei & Zhou (2013) "Boutique investment banks" → *JCF*.
- Agrawal m.fl. (2013) "Common advisers" → *J. Law & Economics*.
- Davis m.fl. (2025) PE-uppföljning → *Management Science*.
- Chen, Pelger & Zhu (2024) → *Management Science*.
- Greenland m.fl. (2024) och Huang m.fl. (2023) om tullar → *JIE*.
- Kim, Muhn & Nikolaev (LLM-artiklar) → working papers, delvis tillbakadragna.
- Gabaix & Koijen "Inelastic markets" → fortfarande working paper.
- Eisfeldt m.fl. "Generative AI and firm values" → "forthcoming JF", ingen
  volym ännu.

Rätta tidskrifter: Boone & Mulherin (2007) är *JF* 62(2); Cieslak, Morse &
Vissing-Jørgensen (2019) är *JF* 74(5); Ellul, Pagano & Panunzi (2010) är
*AER*; Malenko & Malenko (2015) är *JFE* 117(3); Hillenbrand (2025) är *RFS*
38(4).

---

## 6. Att göra före onsdag 9 sep kl. 13.00

**Söndag–måndag: datatester (krävs för att synopsisen ska vara trovärdig)**

1. Logga in på data.houseoffinance.se/serrano via SWAMID. Ladda ner
   variabellistan. Bekräfta: säteskommun, antal anställda, räntekostnader,
   utdelning, koncernmoder, SNI, senaste bokslutsår.
2. CapIQ: kör screenen för ett år till (t.ex. 2019) och exportera. Räkna
   svenska privata targets med köpartyp. Testa namnmatchning mot Serrano på
   50 bolag (andel träff).
3. Retriever Business (via biblioteket): kontrollera att styrelseledamöters
   födelseår går att exportera för ett urval targets.
4. Om D väljs: kontrollera i FinBas att ex-dagar/utdelningsbelopp finns som
   fält (annars Datastream).
5. Om B väljs: hämta årsmedelspot per elområde 2019–2023 från Nord Pool/Ei
   och elstödets villkor (förordning 2023:233).

**Måndag–tisdag: skriv synopsisen enligt `course_context/SYNOPSIS_TEMPLATE.md`**

- Per ämne 1–2 sidor: kursiverad forskningsfråga, mekanism, varför Sverige,
  minst tre kärnreferenser med volym/sidor, exakt vad som replikeras och vad
  som utvidgas, data med bekräftad åtkomst och förväntat N, baseline-
  specifikation, hot mot identifikationen, placebo, tre månaders scope,
  fallback.
- Namn och önskad tutor överst. Filnamn `BScThesis_Efternamn1_Efternamn2.pdf`.

**Fortsätt parallellt:** exportera CapIQ 2015–2024 (2–3 år per dag) enligt
`~/dev/capiq-transactions/export_log.md`.

---

## 7. Källfiler

Agentrapporterna (kompakta sammanfattningar) ligger i sessionens scratchpad
under `reports/`. Vinnaruppsatsernas extraherade text och introduktioner
ligger i scratchpad under `winners_txt/` och `intros/`. Kurskrav:
`course_context/README.md`, `course_context/SYNOPSIS_TEMPLATE.md`.
