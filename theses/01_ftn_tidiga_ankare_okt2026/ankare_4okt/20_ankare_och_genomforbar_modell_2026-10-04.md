# FTN: val av ankare och en genomförbar huvudanalys

4 oktober 2026. Forsknings- och metodunderlag, inte text för inlämning. Ersätter den preliminära rangordningen i rapport 19. PLAN.md och synopsis har inte ändrats.

**Förtydligande 5 oktober 2026:** Rekommendationen av JJM nedan ska inte behandlas som ett låst metodankare för en kausal FTN-studie. JJM är nära urvals-/flödesfrågan, men dess regressionsupplägg ger inte i sig identifikation av FTN-vinstens effekt. SSZ är stöd för flödesmätning, kapitaluppdelning och sponsormekanismen. FTN-frågan behålls; huvudankaret avgörs först mot en trovärdig jämförelsedesign. Hartzmark–Sussman (2019) är en kandidat att pröva, inte en ny färdig vinnare i rangordningen. Deras ratinglansering och tröskeljämförelser kräver andra antaganden än FTN:s urval. FTN:s globalrapport 2026 anger en tilldelning till de 14 högst poängsatta anbuden, men även intervjuavdrag och prisrevideringar; identifierade slutpoäng och fullständig tilldelningsregel måste verifieras innan en lokal tröskeldesign kan rekommenderas.

## 1. Mitt val och dess gräns

**För frågan i PLAN.md rekommenderar jag Jenkinson, Jones & Martinez (2016), _Picking Winners? Investment Consultants’ Recommendations of Fund Managers_, Journal of Finance 71(5), 2333–2370, som huvudankare.** Huvudkopplingen är artikelns flödesanalys: professionellt urval av förvaltare → efterföljande kapitalflöden, utöver vad tidigare prestation och observerbara fondkarakteristika förklarar. Vårt eget tillägg blir att skilja kapital på den berörda pensionsplattformen från kapital utanför den.

Detta är mitt bäst motiverade val bland granskade kandidater, inte ett bevis för att det är bäst i hela litteraturen. Jag har inte verifierat en publicerad artikel som samtidigt har offentlig fondupphandling, samma pensionssystem, externa fondflöden, tillgängliga originaldata och direkt överförbar kausal identifikation. Den begränsningen försvinner inte genom ett nytt artikelnamn.

**Forskningsfråga för denna design:** Hur förändras nettoflöden utanför premiepensionen för FTN-utvalda fonder relativt jämförbara anbudsgivare som inte väljs?

Möjlig arbetstitel: _Does Public Fund Selection Reallocate Capital Beyond the Pension Platform?_

Den bredare synopsisen gäller FTN:s påverkan på fondmarknaden, inklusive avgifter och utbud. Här väljs flöden som huvudutfall. ”Utanför PPM” betyder inte automatiskt svenska hushålls pengar: internationella fondtotaler omfattar även utländska och institutionella investerare. Utan geografisk ägaruppdelning ska frågan och slutsatserna avse kapital utanför PPM.

## 2. Vad jag kontrollerat i huvudartikeln

Publiceringen är verifierad hos [Wiley](https://doi.org/10.1111/jofi.12289). Den fulltext vars metod jag har läst och vars ekvation jag har kontrollerat visuellt är [författarversionen från september 2014](https://www.stat.berkeley.edu/users/aldous/157/Papers/jenkinson.pdf), märkt Journal of Finance forthcoming. Hänvisningarna nedan avser **den versionens** tryckta sidnummer, inte slutversionens paginering. Jag har inte kunnat jämföra hela publicerade slutversionen sida för sida.

På s. 19–22, ekvationerna (2)–(4), definieras flöden och huvudregression. Tabell IV, s. 44, visar sex specifikationer. Ekvation (4), med förenklad notation, är:

`Flow_it = year_FE_t + β ΔRecommendations_i,t−1 + γ PastPerformance_i,t−1 + δ Controls_i,t−1 + ε_it`.

Det är årsdata, en poolad regression med årseffekter; den verifierade specifikationen har **inte fondfixa effekter**. Standardfelen klustras på investeringsprodukt. Rekommendationsförändringen är förändringen i antalet rekommendationer, skalad med maximalt möjligt antal rekommendationer. Prestation mäts som kategorirelativa rangmått för avkastning och trefaktoralfa; kontroller omfattar storlek och volatilitet. Tabellens not beskriver benchmarkrelativ avkastning, medan löptexten benämner ettårig bruttoavkastning; slutversion/dataanvisning måste avgöra exakt reproduktion. Procentflödet skalas med föregående års kapital. Storlek loggas i procentflödesregressionen. Volatilitet bygger på föregående två år. Författarversionen winsoriserar procentflöden vid 95:e percentilen.

Tabell IV:s kolumner I/IV använder förändrade rekommendationer; II/V lägger till rekommendationernas nivå; III/VI delar upp positiva och negativa förändringar. Därmed kan modellen skilja en ny rekommendation från att redan vara rekommenderad. Framtida avkastning är en separat analys i artikeln och behöver inte bli en stor del av vår uppsats.

En faktisk originalreplikation kräver författarnas rekommendations- och produktdata, bland annat från Greenwich Associates, eVestment och Informa. Ingen nedladdningsbar komplett originaldatabas har verifierats här. Tillämpning av modellen på FTN är en **metodreplikation med anpassningar**, inte en återskapad amerikansk tabell. Det måste stå tydligt i uppsatsens metod och replikationspaket.

## 3. Varför detta val framför övriga huvudkandidater

| Artikel | Styrka för vår fråga | Avgörande avvikelse / roll |
|---|---|---|
| **Jenkinson–Jones–Martinez 2016, JF** | Professionellt, delvis kvalitativt förvaltarurval; explicit flödesregression kontrollerad för historisk prestation. | Årlig rekommendationsintensitet, inte svensk kontraktstilldelning. Bäst sammanhållen huvudmodell, men inte färdig FTN-identifikation. |
| [Del Guercio–Tkac 2008, JFQA](https://doi.org/10.1017/S0022109000014393) | Tydliga ratinghändelser och abnormalflöden. | Formelbaserade stjärnändringar och individuella normalflödesprognoser ligger längre från upphandlingsurvalet. Bra kompletterande eventanalys; 2001-versionen är läst, inte slutversionens hela metod. |
| [Cookson m.fl. 2021, RFS](https://doi.org/10.1093/rfs/hhaa057) | Mycket nära rekommendationer och fondförsäljning på plattformar. | Plattformsspecifika flöden och variation mellan flera plattformar; FTN-frågan gäller även kapital utanför plattformen. Stark närliggande referens, inte obrukbar. |
| [Sialm–Starks–Zhang 2015, JF](https://doi.org/10.1111/jofi.12232) | Pensions-/övrigt kapital i samma fond. | Huvudrelationen är prestationskänslighet och sponsorns roll, inte besked om kontraktsvinst. Använd för kapitaluppdelningen. |
| [Hartzmark–Sussman 2019, JF](https://doi.org/10.1111/jofi.12841) | Ratinginformation och flöden, tydligt empiriskt upplägg. | Ratinglansering och ratinggränser ger annan identifikation. FTN ändrar även fondens ekonomiska villkor. |
| [Kaniel–Parham 2017, JFE](https://doi.org/10.1016/j.jfineco.2016.11.003) | Listplacering, synlighet, flöden och jämförelse kring listgräns. | Kan bli ett starkare ankare för en **annan, lokal tröskeldesign**, om FTN-poäng och tilldelningsregel medger den. Detta är inte verifierat. |
| [Goyal–Wahal 2008, JF](https://doi.org/10.1111/j.1540-6261.2008.01375.x) | Mycket nära institutionellt anlitande/uppsägning av förvaltare och före/efter-prestation. | Bäst för frågan om FTN väljer bättre förvaltning; den korta efterperioden begränsar detta. Inte ankare för externa flöden. |

Jag prövade även nyare spår. [Goyal, Wahal & Yavuz, Choosing Investment Managers, JFQA 2024](https://doi.org/10.1017/S0022109023001072) fokuserar på kontakter och anlitande, inte externa flöden. [Cookson m.fl., Virtual Reality?, juli 2021-version](https://ora.ox.ac.uk/objects/uuid%3A707022d9-e93c-49c7-8b25-348f845d96f7/files/shq37vp22s) gäller konsulters egna prestationspåståenden. [Parwada & Tan, Unwanted Attention?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5736217) är särskilt relevant för nominerade förlorare och negativa reaktioner, men är verifierad som working paper/preprint, inte som publicerad i kursens angivna tidskrifter. Dessa tre är screenade på sammanfattning/inledning, inte fullständigt metodgranskade. Working paperets viktiga invändning är att en positiv vinnare–förlorare-skillnad kan drivas av förlorarnas utflöden.

Rapport 19 dokumenterar ytterligare kandidater om pensionsauktioner, avgiftsinformation och fondtvillingar. Fler referenser ersätter inte ett fungerande huvudtest.

## 4. Exakt vad som återanvänds och vad som ändras

| Del | Original | Vår tillämpning | Klassificering |
|---|---|---|---|
| Ekonomisk relation | Bedömarrekommendation → kommande flöde, givet prestation | FTN-urval → kommande flöde, givet prestation | Samma grundrelation |
| Enhet | Investeringsprodukt–år | Fondportfölj–månad, knuten till upphandling | Motiverad ändring för beskedens timing |
| Utfallsdefinition | Kapitalförändring rensad för avkastning, i belopp och andel | Samma flödesbegrepp; total-, PPM- och icke-PPM-komponent | Återanvändning + huvudextension |
| Urvalsvariabel | Förändring i rekommendationsandel | Tilldelning vid ett dokumenterat besked | Anpassning; inte samma behandling |
| Förhandskontroller | Avkastnings-/alfarank, storlek, volatilitet | Motsvarande mått före besked inom relevant fondkategori | Nära återanvändning där data finns |
| Dynamik | Årsförändring och rekommendationsnivå | Månadsspecifika reaktioner före/efter besked | Egen extension |
| Jämförelse | Rekommendationsvariation mellan produkter | Vinnare mot kvalificerade, kvarstående förlorande anbud | Egen jämförelsedesign |
| Inferens | Produktklustrade standardfel | Hänsyn till fondfamilj och gemensamma upphandlingsbesked | Måste omprövas, inte kopieras |

**Viktig kodningsfråga:** en befintlig PPM-fond som vinner har fått ett nytt positivt FTN-besked trots att dess tillgänglighet är oförändrad. `ΔPPM-tillgänglighet` skulle felaktigt ge noll behandling. En ny anbudsgivare som förlorar har däremot inte blivit borttagen från PPM. Behåll därför både `award` och `incumbent_before_award` som separata variabler; kalla inte alla förlorare ”avregistrerade”.

## 5. Huvudanalys som faktiskt besvarar frågan

### A. Bygg rätt flöde

För samma fondportfölj, valuta och månad:

`ExternalFlow_it = TotalFlow_it − PPMFlow_it`.

Subtraktionen sker i kronor. Om ett relativt externt flöde behövs:

`ExternalRate_it = ExternalFlow_it / (TotalAssets_i,t−1 − PPMAssets_i,t−1)`.

För huvudtabellens tre komponenter föreslås också en gemensam, förutbestämd kapitalbas `B_iq = TotalAssets` vid månadsslutet före beskedet. Då kan total-, PPM- och externflöden alla uttryckas i procent av `B_iq`. Med identiskt urval, regressorer och vikter blir totalflödets regressionskoefficient exakt summan av komponenternas koefficienter. Separat winsorisering av de tre utfallen skulle bryta denna identitet; validera och flagga avvikande observationer gemensamt och redovisa känslighet.

Skilj denna dekomposition från extern tillväxttakt med extern kapitalbas. Ett stort PPM-inflöde får inte mekaniskt ändra nämnaren och därmed se ut som ett nytt beteende utanför PPM.

### B. Gör först en transparent tabell nära ankaret

En observation per fond och upphandling. Skatta för en på förhand vald horisont, exempelvis de sex hela månaderna efter beskedsmånaden:

`CumFlow_iq(1:6)/B_iq = round_FE_q + β Winner_iq + γ Performance_iq,pre + δ Controls_iq,pre + ε_iq`.

Kör **samma regression och samma urval** för totalflöde, PPM-flöde och externt flöde. Prestationsrang beräknas inom jämförbar kategori, inte mellan alla aktiefonder. Storlek och tvåårig volatilitet mäts före beskedet. Lägg preflöden till som en uttrycklig egen robusthet, inte som något originalet redan innehåller. Använd nettotalavkastning om detta är det tillgängliga måttet, men redovisa avvikelsen från originalets brutto-/benchmarkmått.

Detta är en anpassning av ekvation (4), inte identisk replikation. β är i denna tabell en **villkorad flödesskillnad**, inte automatiskt en kausal effekt. FTN kan ha valt egenskaper som också förutsäger framtida externa flöden.

### C. Lägg tidsdimensionen till samma huvudtest

Bygg separata eventpaneler för varje upphandling, med fond–upphandlingseffekter och upphandling–kalendermånadseffekter:

`y_iqt = fund_round_FE_iq + round_month_FE_qt + Σ[k ≠ −1] β_qk Winner_iq × 1[t−T_q=k] + ε_iqt`.

Här är `y` det externa nettoflödet i andel av den frysta kapitalbasen. Referensmånad är −1; visa exempelvis −12 till +6. Behåll beskedsmånaden som en separat, delvis behandlad månad. Redovisa kohortspecifika effekter och aggregera med förutbestämda vikter, exempelvis lika vikt per upphandling. En sådan viktning svarar på genomsnittlig effekt över upphandlingar; fond- och kapitalviktning svarar på andra frågor och redovisas separat.

För ett sammanfattande före/efter-estimat kan samma panel användas med `Winner × Post`, med lika långa för- och efterfönster. Förhandskarakteristika som är konstanta absorberas av fond–upphandlingseffekterna; de ska inte läggas in en gång till som identifierade nivåeffekter. Vid behov används på förhand valda interaktioner med tid eller ett motiverat matchat urval.

Detta är en **egen dynamisk extension**, inte JJM:s specifikation. Kausal tolkning kräver att vinnarnas och förlorarnas externa flöden annars skulle ha utvecklats jämförbart, och att relevanta skillnader i andra samtidiga händelser hanteras. Förtrender är diagnostik, inte bevis. Lägg inte rutinmässigt in efterbehandlad avgift, storlek, prestation eller laggat externt flöde: de kan vara delar av den effekt man försöker mäta.

### D. Tolka vinnare och förlorare korrekt

En positiv β visar att vinnare utvecklas bättre relativt förlorare. Den visar inte ensam om vinnare får extra inflöden, förlorare får extra utflöden eller båda. Absoluta effekter för båda grupperna kräver en tredje trovärdig referens, exempelvis förhandsmatchade icke-anbudsgivare. Dessa är självselekterade och kan också påverkas av reformen; redovisa analysen som mer antagandekänslig. Lägg inte bara in både vinnare och förlorare mot en gemensam kategori–månadseffekt i ett urval som endast består av dessa två grupper: deras separata gemensamma nivåförskjutningar är då inte identifierade.

En extern flödesreaktion är evidens för att urvalet har betydelse utanför plattformen. Den isolerar inte en ren kvalitetsstämpel. Marknadsföring, skalfördelar, förväntad fondöverlevnad, ändrade avgifter och framtida likviditet kan också påverkas. Besked före faktiska kapitalflyttar ger en användbar timingkontroll, men förväntningar på kapitalflytten kan påverka investerare direkt.

## 6. Kontrollgruppen: ett faktiskt problem i FTN-materialet

[Första upphandlingsrapporten, mars 2024](https://www.ftn.se/download/18.7a22cebb18e5fb3c04d3486/1711311108882/FTN%20upphandlingsrapport%2025%20mars%202024%20sve.pdf), s. 19–21: 35 anbud, 12 kvalificerade, tio intervjuade och sex vinnare. En kvalificerad anbudsgivare drog tillbaka sitt anbud och en nådde inte erforderlig poängnivå inför intervjun. Därför är ”29 förlorare” inte en lämplig automatisk huvudkontroll. De namngivna anbuden och de aggregerade processantalen ger heller inte en fullständig identifierad lista över kvalificerade förlorare.

[Globala aktiva fonder, februari 2026](https://www.ftn.se/download/18.6b5a53e019c4795fa8c93ab/1771597818829/FTN%20upphandlingsrapport%20Global%20Aktiv%20SE.pdf), s. 25 och 30–31: 99 anbud, tio återkallade, 20 förkastade, 69 utvärderade; 14 fonder från tolv förvaltare vann. Räkna inte tolv vinnande förvaltare som tolv fondobservationer. Kontrollera dessutom om flera anbud eller nya andelsklasser avser samma ekonomiska portfölj.

Huvudurvalet bör vara vinnare och kvalificerade kvarstående förlorare i samma upphandling. Finalister är en ytterligare jämförelse om identiteter och regler kan verifieras; de är fortfarande inte slumpmässigt valda. Återkallade och diskvalificerade anbud kodas separat. Saknade statusuppgifter får inte fyllas i genom gissning.

## 7. Datakontroll som faktiskt är gjord

Lokal kontroll av filstruktur, fält och ett sent PPM-blad; inte en färdig sammanfogad panel:

| Källa | Verifierat | Återstår |
|---|---|---|
| `data/fundmaster.xlsx`, blad fundmaster | 80 258 datarader; fond-ID, andelsklass-ID, ISIN, valuta, tillgängliga försäljningsländer samt kapital-/avkastningssnapshot | Ingen månatlig TNA-/flödespanel i denna fil. Rader är inte unika fonder. |
| `data/FEES.txt` | 347 401 avgiftsrader; bl.a. avgiftstyp, prospektdatum, enhet och avgift | Inte verifierat som fullständig historisk avgiftspanel. Olika datum mellan fonder bevisar inte historik inom fond. |
| PPM augusti 2026 | Fondval & marknadsvärde!A23:O23 innehåller fondnummer, kapital, Handel netto, kategori och upphandlad-flagga; Fondstatistik innehåller ISIN | Validera periodisering och fullständig avregistreringsmånad; borttagna fonder måste följas, inte bara de kvarvarande. Ingen definition av Handel netto hittades i bladet Beskrivning av mått. |
| FTN:s rapporter | Beskedsdatum, anbud och vinnare i kontrollerade rapporter | Kvalificeringsstatus per förlorare, faktiska implementationsdatum och eventuella fond-/klassbyten |
| [SHoF Valuations](https://www.houseoffinance.se/data-center/shof-fund-data-morningstar/valuations-daily-tna-and-net-flow-by-fund-and-fund-share-class/) | Officiellt dataset med TNA/flöden på klass- och fondnivå | Denna historik har inte återfunnits i lokala datafiler; tillgång och faktisk fond-/datumtäckning återstår att kontrollera. |

[SHoF:s fältdefinition, s. 4 och 21–23](https://www.houseoffinance.se/globalassets/shof/data-center/shof-fund-data-morningstar/field-definition_shof-fund-data-1.pdf) visar att `netflowclass` och `netflowfund` är **estimerade** flöden. `performanceid` kan finnas flera gånger för samma andelsklass i olika valutor; `secid` identifierar andelsklass och `fundid` fondportfölj. Summera inte upprepade fondtotaler eller olika valutaversioner. Dokumentationen är dessutom inkonsekvent i valutabenämningen för `netflowfund` jämfört med `tnafund`; valuta ska verifieras mot faktisk export innan subtraktion.

Föredra en verifierad fondtotal per fond/datum. Om andelsklasser måste summeras: en rad per verklig klass, inga dubbla performance streams, gemensam valuta och fullständig klasstäckning. Konvertera dagliga flöden med relevant dagskurs innan månadssummering; en månadsslutskurs på alla månadens kassaflöden är en approximation. PPM-avkastning efter särskild rabatt är inte automatiskt samma avkastning som fondens NAV.

Validera identiteten på några vinnare och förlorare kring faktiska flyttar. Ett stort PPM-inflöde kan via mätfel i Morningstar skapa ett falskt externt residualflöde. Kontrollera fusioner, klassbyten och rapporteringsfördröjningar; jämför kortare och längre flödesfönster. Välj inte fönster utifrån signifikans.

## 8. Tidsfönster och inferens: vad siffrorna medger nu

[FTN:s rapportförteckning](https://www.ftn.se/marknadsdialog/upphandlingsrapporter.html) visar elva upphandlingar på sju olika tilldelningsdatum fram till september 2026. Flera kategorier beslutas samma dag. De är inte elva uppenbart oberoende experiment.

Med slutmånad augusti 2026 och sex **hela** efterföljande månader (+1 till +6) kan aktiva Europa mars 2024, två aktiva Nordenkategorier februari 2025, aktiv Sverige augusti 2025 och aktiv Global februari 2026 principiellt ingå: **fem aktiva upphandlingar på fyra beskedsdatum**, före ytterligare bortfall från datatäckning. Småbolagsbeskeden i maj 2026 har bara juni–augusti, tre hela eftermånader. Teknologibeskedet i september ligger efter den lokala PPM-filens senaste månad. Tolvmånadersanalys begränsar urvalet ytterligare. Kortare horisonter kan använda fler kohorter, men redovisa då att sammansättningen förändras; visa även ett konstant kohorturval.

För nära koppling till JJM:s aktiva förvaltarurval föreslås aktiva fonder som huvudpopulation och passiva upphandlingar som en separat, förutbestämd utvidgning. Detta förbättrar jämförbarheten men minskar underlaget. Det är en verklig avvägning.

Rapportera effekter per upphandling, konfidensintervall, lämna-en-upphandling-ut och gärna lämna-ett-beskedsdatum-ut. Beroende mellan samma fondfamiljs produkter behöver också hanteras. Produktklustring från originalet är otillräcklig som enda motivering. Wild cluster bootstrap löser inte automatiskt få och beroende beslut. Permutation av vinnaretiketter är inte exakt randomiseringsinferens när vinnarna väljs efter kvalitet. Inferensmetod och detekterbar effekt måste bedömas med det faktiska urvalet innan stora kausala slutsatser utlovas.

## 9. Vad vi ska ta från de gamla vinnarna

Tre kontrollerade exempel:

* [Bank Stock Returns and Monetary Policy Surprises, 2020](../old_winners/text/2020_staffan_viotti_bank_stock_returns_and_monetary_policy_surprises.txt): återanvänder English m.fl.:s relation mellan oväntad penningpolitik och bankavkastning, börjar med originalperiod och för över samma test till 2012–2019. Tim- till dagsdata är en redovisad avvikelse. Originalförfattarnas datahjälp anges uttryckligen.
* [Changing Patterns over the FOMC Cycle, 2023](../old_winners/text/2023_per_hiller_changing_patterns_over_the_fomc_cycle.txt): samma kalenderdefinitioner och centrala avkastningstest som Cieslak m.fl.; ny period och prövning av mekanismen. Att ett äldre resultat inte återkommer är ett forskningsresultat.
* [The Smooth Transition, 2024](../old_winners/text/2024_per_hiller_the_smooth_transition.txt): Ahern–Dittmars event- och IV-upplägg förs till fransk kvotering; institutionella skillnader motiverar jämförelsen. Att en metod tidigare använts gör dock inte dess antaganden självklara i den nya miljön.

Det gemensamma är ett igenkännbart huvudtest, en motiverad förändring och en slutsats som kan jämföras med ankaret. För FTN blir förändringen **vilka pengar som reagerar på ett professionellt urval**. Undvik att lägga flera SSZ-tabeller före en fristående FTN-regression som egentligen besvarar frågan.

De granskade uppsatserna utanför vinnararkivet ger exempel på svag koppling mellan teoretiskt begrepp och mätt utfall, ändrad fråga utan ändrat ankare och alltför breda analyser; se rapport 18. De bevisar inte varför någon inte vann. Avsaknad i vår vinnarsamling är inte heller säkert samma sak som frånvaro av alla utmärkelser. Använd kvalitetskriterierna, inte en påstådd vinnarprediktion.

## 10. Ett fokuserat uppsatspaket

Följande är ett designförslag, inte en kursregel om antal tabeller:

1. **Urvalstabell:** upphandling, processdatum, anbud, kvalificerade, vinnare, datatäckning; fullständigt flödesschema för bortfall.
2. **Jämförbarhetstabell:** förhandsavkastning, storlek, avgift, PPM-andel och externa flöden för vinnare och kontrollfonder.
3. **Ankartabell:** JJM-inspirerat urvals-/flödessamband med exakt redovisade metodskillnader. Originalets rapporterade resultat får visas separat, men inte kallas egen replikation.
4. **Huvudtabell:** samma modell och urval för total-, PPM- och externflöden; kronor och tydligt definierad skalning. Externt flöde är primärt utfall.
5. **Eventfigur:** externa flödesdifferenser före och efter besked, med kohorttäckning per horisont och separat markerad implementering.
6. **Känslighet:** alternativa rimliga kontroller, bortfall av en upphandling/beskedsdag i taget och noggrant validerad flödesmätning. En prioriterad mekanismanalys kan vara reaktion före kapitalflytt, med dess begränsade tolkning.

Detta ger ett sammanhängande test även vid nollresultat. Ange en ekonomiskt relevant minsta effekt och rapportera vad intervallet faktiskt utesluter. Ett brett intervall betyder otillräcklig precision; det visar inte att investerare ignorerar FTN. En positiv reaktion visar heller inte irrationellt beteende. Berk–Green innebär inte att rationella investerare alltid ska ignorera informativa kvalitetsbesked.

## 11. Beslut som bör tas före stora regressioner

**Jag skulle arbeta vidare med JJM som huvudankare och ovanstående flödesdekomposition som extension.** Det är en starkare koppling mellan ankare och fråga än PLAN.md:s nuvarande stora prestationskänslighetsreplikation följd av ett separat huvudtest.

Lås däremot inte löftet om en nästan exakt originalreplikation: originaldata är inte verifierat tillgängliga. Lås inte heller en ren certifieringseffekt: FTN:s tilldelning ändrar fler ekonomiska förutsättningar än information. Den återstående genomförbarhetskontrollen är konkret: identifierade kvalificerade förlorare, månatliga totala flöden/TNA för samma portföljer och tillräcklig jämförbar för-/efterhistorik. Inga effekter har skattats i detta underlag.

Om kursens önskade replikationsnivå i praktiken kräver en återskapad originaltabell med originaldata måste just den delen säkras innan denna design utlovas. Annars ska arbetet beskrivas korrekt som ny tillämpning och extension av en publicerad flödesmodell. Det kan vara en bra uppsats, men är en annan ambitionsnivå än vinnaruppsatsen som fick originaldata direkt från forskarna.
