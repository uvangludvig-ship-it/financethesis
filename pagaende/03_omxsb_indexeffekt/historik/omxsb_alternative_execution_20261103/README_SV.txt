ALTERNATIVA DATAKÄLLOR — GENOMFÖRD PILOT 3 NOVEMBER 2026
Teknisk arbets-/granskningsanteckning, inte uppsatstext.

Vad den här omgången gör
Prövar konkret om den inloggade LSEG-appen och SHoF ger nya mätningar för OMXSB. Omgången ändrar inte tidigare replikationsresultat, tolkar inte saknade data som noll och öppnar inga FTN-utfall. Äldre dagliga kursresultat var redan kända; detta är en explorativ källpilot, inte blind förhandsregistrering.

1. Indexkorgar: medlemskap fungerar, vikt-/aktieantalsdata återstår
Desktopanslutningen fungerade utan ny appnyckel eller plattformsinloggning. Den gamla kandidatkoden .OMXSB kunde inte lösas. LSEG:s instrumentsökning identifierade .OMXSBPI som det okappade prisindexet. Originalförsöken och identifieringsrättelsen är bevarade.
Historiska listor 30 november och 1 december 2023 ger 105 respektive 104 giltiga medlemmar. Sex tillägg och sju borttag stämmer mot den implementerade listan efter uppdateringen 29 november: JM finns båda dagarna, Karnov saknas båda dagarna. Detta är en faktisk källkontroll, inte en ny priseffekt.
Historiska Weight percent och Index Shares är tomma i den rättade huvudpiloten och i sju ytterligare dokumenterade frågor. Tomma strängar är missing, inte nollvikter. Inget tvångsköp har räknats från dessa svar. Kontot gav inget entydigt behörighetsfel; den exakta orsaken är inte fastställd. Produktbeskrivningar eller fungerande medlemslistor bevisar inte tillgång till viktserier.
Två ytterligare kontrollfrågor på dagens S&P500 och det kappade OMXSB gav också medlemslistor men tomma vikt-/IndexShares-fält. Vi har alltså ingen positiv fältkontroll och kan inte tillskriva luckan just OMXSB:s historiska innehåll. Dessa index ersätter aldrig huvudindexet. Detaljer: index_sources/DESKTOP_UPDATE_SV.txt, FIELD_CONTROL_ADDENDUM_SV.txt och READY_REQUEST.txt.

2. Stängningsauktionen: två individuella kontraster har räknats
Urvalet låstes på metadata före nya HFT-prisutfall: första giltiga tillägg och borttag i 2019H1 respektive 2023H2. Det blev Bilia, Atrium Ljungberg, Camurus och AFRY. Primära datum är handelsdagen före indexets ikraftträdande och samma akties fasta jämförelsedag sex börsdagar före ikraftträdandet. Inga aktier byts ut på grund av utfall eller dataluckor.
SHoF:s Bilia-export i full rekonstruktion har 5483 rader. Transaktionsexporten har exakt samma 862 transaktionsrader, utan extra stängningsobservationer. Båda slutar före auktionen. Det betyder att dessa levererade filer saknar auktionen; det bevisar inte att produktens hela databas avsiktligt utesluter den.
LSEG:s dokumenterade CLS_AUC-fält avser slutpriset i stängningsauktionen. Det finns för båda fasta datum för Camurus och AFRY 2023, men saknas för båda datum för Bilia och Atrium Ljungberg 2019. CLS_AUCVOL finns för samma fyra 2023-observationer. Vanligt dagspris får inte ersätta saknat auktionspris. Fem separata minutfrågor gav inga rader för de aktuella historiska datumen.
Fyra SHoF-orderböcker har därför hämtats för de redan valda 2023-datumen. De innehåller unika, giltiga sista köp-/säljkurser strax före 17:25. Nyhetsbrevet med indexbeskedet den 23 november publicerades efter stängning. Jämförelse av auktion till nästa morgon skulle därför innehålla beskedseffekten och används inte som primärt test.
Det enda primära måttet är skillnaden i auktionspris relativt sista giltiga mittkursen före auktionen, omviktningsdag minus jämförelsedag. Borttagets tecken vänds. Det är ett beskrivande mått på ovanligt prisavstånd vid auktionen, inte bevis på indexfondens handelspris, arbitragevinst, nettoorder eller kausal prispåverkan.
2019-fallen behålls som NA. Inget genomsnitt över bara två 2023-fall, inga p-värden och ingen populationsslutsats tillåts av pilotens specifikation. Ett generellt resultat kräver ett i förväg avgränsat större urval och oberoende jämförelsedagar/kontroller.

Det konkreta pilotutfallet, efter passerade källkontroller
Camurus (tillägg): auktionspriset ligger 0,7522 procent UNDER sista giltiga mittkurs före auktionen på omviktningsdagen. På jämförelsedagen ligger det 0,0454 procent över. Primär signerad differens: -79,7637 baspunkter.
AFRY (borttag): auktionspriset ligger 0,2349 procent UNDER motsvarande mittkurs på omviktningsdagen. På jämförelsedagen ligger det 0,0786 procent över. Efter det förbestämda teckenbytet för borttag är primär differens +31,3480 baspunkter.
En baspunkt är 0,01 procentenhet. Positiv signerad differens betyder högre pris för tillägg eller lägre för borttag jämfört med den fasta jämförelsedagen. De två händelserna ger motsatta tecken. Detta stöder inte ett gemensamt mönster av indextryck i piloten, och det varken bevisar eller utesluter indexhandel som orsak. Observationerna är båda från samma översyn.
Exakta värden, kvarstående NA och källkontroller finns i hft_audit/INDIVIDUAL_AUCTION_CONTRASTS.csv och FINAL_SOURCE_GATE_SUMMARY.json. Ingen efterföljande återgång, faktisk fondaffär eller auktionsvolymseffekt har skattats här.

Öppen redovisning av källmetodändring
SHoF:s ursprungliga dokumentationslänk var trasig. En arkiverad version från oktober 2020 återfanns och definierar handelsfaser, men anger inte tidszonen. Före beräkning av auktionspremier skrevs därför auction_source/CLOCK_METHOD_AMENDMENT.json: endast lokal Stockholmsklocka och UTC får jämföras mot dokumenterade öppningsfaser och kontinuerliga handelstider. Det är en explicit metadata-inferens som ersätter det ursprungliga kravet på en uttrycklig leverantörsetikett. Den gamla regeln beskrivs inte i efterhand som uppfylld. Aktier, datum, sista60sekundersfönster och ekonomiskt mått ändras inte. SHoF:s 2023-fasdata bedöms mot Nasdaq2023-modellen; den modellen bevisar inte ensam 2019 års regler.

Nordic Market Quality och ägardata
Ett separat NMQ-uttag för Bilias fasta vecka innehåller två filer med fyra handelsdagar. Det ger ingen explicit auktionspriskolumn; min-/medel-/maxpris får inte användas som ersättning. Formuläret anger slutdatum juni2021, så dagens produktgränssnitt täcker inte 2023-piloten.
Nio offentliga issueroriginal verifierar viktiga klass- och utdelningsuppgifter för Robur/SEB. Detta stärker källkedjan men fyller inte Roburs saknade kapitaldatum och verifierar inte oberoende alla ex-/återinvesteringsdagar. Tidigare täckningsflaggor är oförändrade. Holdings produkt och universitetsväg finns; faktisk HHS-behörighet och historisk studentexport är fortfarande inte verifierade. Se ownership_sources/REPORT_SV.txt.

Filer, rådata och kontroll
ACQUISITION_LEDGER.json registrerar sju oförändrade SHoF-original. Dessa ligger privat under data/raw/shof/Reinvestments/hft_pilot_20261103/. LSEG-svaren ligger lokalt i respektive index_sources/private och auction_source/private; mapparna är ignorerade av Git. Inga numeriska råserier, fulltexter, inloggningsuppgifter eller mejlinnehåll publiceras. Automatiska leveransmeddelanden har använts för hämtning; inga manuella mejl skickades.
Den publika filkontrollen körs med python3 verify_package.py i denna katalog. independent/verify.py gör separat kontroll från de licensierade originalen; läs dess --help och använd en ny outputfil. Den kräver att originalen finns lokalt och att sökvägar anges vid flytt till annan dator. API-hämtningsskripten kräver lseg-data2.1.1 och en legitim inloggad desktop-session. De ska inte köras för enbart kontroll av frysta resultat.

Vad detta ännu inte visar
Två individuella auktionsfall kan belägga att ett nytt mått går att konstruera. De kan inte avgöra varför den genomsnittliga indexeffekten finns kvar, om den består efter20dagar, vem som säljer eller om en viss uppsatsdesign vinner ett pris. Frånvaro av auktionsdata2019 är ingen ekonomisk frånvaro av effekt.
