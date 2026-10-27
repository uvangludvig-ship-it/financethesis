# Metodankare för FTN: fördjupad prövning

Datum: 4 oktober 2026. Beslutsunderlag, inte uppsatstext. Detta reviderar rekommendationen i rapport 18. PLAN.md och synopsis har inte ändrats.

## Bedömning

Invändningen mot den tidigare rekommendationen är befogad. Ämneslikhet och en gemensam regressionstyp räcker inte. Ett huvudankare bör ge er ett återanvändbart huvudtest: samma ekonomiska utfall, jämförbar observationsenhet, tydlig händelse, begriplig jämförelse och en tabell som går att ställa bredvid originalets.

**För frågan om flöden utanför PPM är Del Guercio & Tkac (2008), Star Power, min främsta metodkandidat efter denna genomgång.** Det är ett villkorat val, inte ett verifierat optimalt ankare. Slutversionens metod och faktisk datatäckning måste kontrolleras innan det låses. Cookson passar fortfarande som närliggande forskning; SSZ kan stödja kanaluppdelningen. De behöver inte vara uppsatsens huvudankare.

**För frågan om FTN väljer bättre förvaltning är Goyal & Wahal (2008) mer direkt.** Deras huvudtabeller kan överföras nära, men FTN:s korta efterperiod gör den inriktningen svagare praktiskt just nu.

Er synopsis omfattar avgifter, utbud och flöden. Jag har inte funnit en artikel som erbjuder en nära replikation av samtliga delar samtidigt. Det är därför nödvändigt att välja ett huvudutfall. Frågan i PLAN.md om externa flöden är en möjlig avgränsning, inte hela det ursprungliga ämnet.

## Vinnarna: vad betyder nära metod?

Följande bygger på lästa introduktions-, metod- och resultatavsnitt. Tillsammans med den tidigare granskningen omfattar detta åtta vinnare, inte samtliga 25 i arkivet. Det är inte en statistisk studie av vad som orsakar ett uppsatspris.

| Vinnaruppsats | Vad som faktiskt återanvänds | Vad som förändras |
|---|---|---|
| Changing Patterns over the FOMC Cycle, 2023 | Cieslak–Morse–Vissing-Jorgensens kalenderdefinitioner och centrala avkastningsregression. Tabell I jämför originalperiod och ny period. | Testar om mönstret kvarstår efter 2016 och undersöker förändringar i den föreslagna mekanismen. |
| Bank Stock Returns and Monetary Policy Surprises, 2020 | English m.fl.: grundregression med penningpolitiska överraskningar, avkastning och bankkarakteristika. Originalperioden återkommer före extensionen. | Efterkrisperiod 2012–2019. Timdata byts till dagsdata; skillnaden och svagare resultat redovisas. |
| Owning the Wave, 2022 | Baek m.fl.: krisavkastning förklaras med ägarstruktur före krisen; modeller med endast branschkontroller respektive både företags- och branschkontroller. | Annan kris och miljö samt utvidgad ägarklassificering. |
| The Smooth Transition, 2024 | Ahern–Dittmar: annonseringsstudie, IV-upplägg och Tobin's Q. | Frankrikes kvotering jämförs med originalets norska miljö. |

Källor: [FOMC](../old_winners/text/2023_per_hiller_changing_patterns_over_the_fomc_cycle.txt), [banker](../old_winners/text/2020_staffan_viotti_bank_stock_returns_and_monetary_policy_surprises.txt), [ägande](../old_winners/text/2022_staffan_viotti_owning_the_wave.txt), [kvotering](../old_winners/text/2024_per_hiller_the_smooth_transition.txt).

Ja: dessa exempel ligger betydligt närmare sina original än att bara låna ordet DiD. Men metodöverföringen är inte alltid exakt. Exempelvis använder In the Eye of a Pandemic en närliggande intradagsmetod från Busse–Green med nya händelser och förklaringsvariabler. Vinnarsamlingen innehåller också uppsatser med flera metodkällor. Vi bör inte uppfinna en regel att varje vinnare kopierar en enda artikel, eller kopiera deras starkaste kausala formuleringar okritiskt.

Den användbara ribban för er är: **vilken huvudtabell replikerar vi, och vilken tydligt avgränsad ändring gör vår extension?**

## Kandidater efter djupare läsning

### Del Guercio & Tkac (2008): närmast flödesfrågan

*Star Power: The Effect of Morningstar Ratings on Mutual Fund Flow*, JFQA 43(4), 907–936. [Publicerad artikel](https://doi.org/10.1017/S0022109000014393).

Artikeln undersöker fondflöden runt ratingförändringar. I den öppna arbetsversionens metodavsnitt III.B skattas normalflöde separat per fond med kategoriflöde, föregående avkastning och föregående flöde. Faktiskt minus förväntat flöde ger abnormalflöde. Tabell IV behandlar ratingförändringar, Figur 3 ekonomiska storlekar och Tabell V heterogenitet. Där används skattningsmånader −14 till −3 och uppföljning upp till sex månader.

**Versionsgräns:** dessa detaljhänvisningar gäller 2001 års arbetsversion, inte verifierade tabellnummer i 2008 års slutversion. Slutversionens publiceringsuppgifter och övergripande metod är kontrollerade, men dess fulltext var inte åtkomlig. [Öppen originalversion](https://fraser.stlouisfed.org/docs/historical/frbatl/wp/frbatl_wp_2001-15.pdf); [lokal text](../tmp/anchor_audit/star_power_2001.txt).

Min föreslagna FTN-fråga:

> Hur förändras fonders nettoflöden utanför premiepensionen kring offentliggörandet av FTN:s upphandlingsbeslut, och skiljer sig reaktionen mellan utvalda fonder och befintliga PPM-fonder som inte blir kvar?

Detta behåller ert tema och gör efterfrågan utanför PPM till huvudutfall. Det kräver inga individkonton. Det testar inte direkt förtroende, kvalitet eller svenska hushålls beteende: kapital utanför PPM kan även komma från institutioner och utlandet.

| Del i er studie | Konkret genomförande |
|---|---|
| Replikation | Om historiska Morningstar-ratingar finns: kör först ratinghändelsetestet på samma svenska fonddataset. Detta är en metodreplikation i ny miljö, inte en reproduktion av originalets amerikanska resultat. |
| FTN-extension | Ersätt ratinghändelsen med FTN-beslutet. Separera befintliga vinnare, nytillkomna vinnare och befintliga fonder som inte blir kvar. |
| Huvudutfall | Nettoflöde utanför PPM, mätt i kronor och i relation till relevant förutbestämt kapital. |
| Huvudfigur | Genomsnittligt abnormalflöde före och efter beskedet, med osäkerhet och separat visning av de olika grupperna. |
| Huvudtabell | Förregistrerade fönster, exempelvis annonseringsmånad, 0–2 och 0–5 månader; endast kohorter med full uppföljning i respektive kolumn. |
| Viktig extension | Jämför reaktionen vid beskedet med reaktionen vid faktisk kapitalöverföring. Redovisa PPM-flödet separat. |

Detta är mer direkt överförbart än en allmän pensionsflödesregression. Men FTN förändrar också fondtillgång, kapitalbas, avgifter och marknadsföringsmöjligheter. Även externa flöden kan reagera på dessa förändringar. Därför är ett abnormalflöde kring beslutet **inte automatiskt en identifierad kausal certifieringseffekt**.

Ett enkelt egenformulerat redovisningsmått är:

`abnormalflöde_utanför_PPM = observerat_flöde_utanför_PPM − modellens_förväntade_flöde_utanför_PPM`.

Det är ett mått relativt en modell. Ett negativt värde behöver inte innebära nettoutflöde.

### Goyal & Wahal (2008): tydligast för urvalets kvalitet

*The Selection and Termination of Investment Management Firms by Plan Sponsors*, JF 63(4), 1805–1847. [Publicerad artikel](https://doi.org/10.1111/j.1540-6261.2008.01375.x), [läst original-PDF](https://fwpwealth.com/wp-content/uploads/2020/10/Goyal-and-Wahal-JF-2008.pdf).

Tabell IV jämför benchmarkjusterad avkastning, informationskvoter och kalenderalfa före och efter anlitande på ett-, två- och treårshorisonter. Tabell IX gäller avslutade mandat. Avsnitt V jämför verkliga byten med att behålla den tidigare förvaltaren; författarna undviker att okritiskt jämföra alla anlitade med alla avskedade.

En svensk motsvarighet vore: **Ger FTN:s nya fondurval bättre nettoavkastning än ett i förväg definierat alternativ att behålla det gamla urvalet?** Koppla faktisk mottagarfond till avvecklad fond där en sådan överföring är dokumenterad; hitta inte på en-till-en-par. Skilj bruttoförvaltning från spararnas avkastning efter PPM-avgifter.

Här finns ett nära återanvändbart huvudtest. Problemet är tidsperioden: 2024–2026 års upphandlingar ger ännu inte tre års uppföljning. Ett kort och gemensamt börsförlopp ger svag grund för slutsatser om urvalsskicklighet. Därför väljer jag inte detta som huvudspår idag trots den starka konceptuella och metodmässiga kopplingen.

### Badoer, Costello & James (2020): bättre för en fråga om avgiftskänslighet

*I Can See Clearly Now: The Impact of Disclosure Requirements on 401(k) Fees*, JFE 136(2), 471–489. [Publicerad artikel](https://www.sciencedirect.com/science/article/pii/S0304405X19302466), [läst konferensversion december 2018](https://www.aeaweb.org/conference/2019/preliminary/paper/d5hen8Hr).

I arbetsversionens Tabell 6 jämförs månatliga flöden efter informationsreformen över två dimensioner: pensions-/retailandelar och avgiftsnivå. Nyckeltermen är `Post × Fee × R Class`. Tabell 7 prövar alternativa reformår. Avgiften avser bland annat amerikanska 12b-1-avgifter, inte svensk PPM-rabatt.

Det går att formulera en FTN-extension om ändrad avgiftskänslighet mellan kapital inom och utanför PPM. Men prisinformation och obligatoriska fondbyten är olika behandlingar. En överföring från borttagna dyra fonder till billigare vinnare kan mekaniskt skapa det sökta resultatet. Utan separation av flyttkapital blir beteendetolkningen missvisande. Detta är således ett alternativ för en annan huvudfråga, inte ett överlägset ankare för externa flöden efter urval.

### Kronlund, Pool, Sialm & Stefanescu (2021): tydligt men fel huvudutfall

*Out of Sight No More? The Effect of Fee Disclosures on 401(k) Investment Allocations*, JFE 141(2), 644–668. [Publicerad artikel](https://www.sciencedirect.com/science/article/pii/S0304405X21001355), [läst Fed-version](https://www.federalreserve.gov/econres/feds/files/2020078pap.pdf).

Fed-versionens ekvation 7 och Tabell 3 testar om flödens samband med avgifter ändras efter reformen. Dataenheten är fond–pensionsplan–år. Författarna exkluderar nytillagda och borttagna fonder för att fokusera på deltagarnas val, och använder variation över många planer.

Just det urvalet tar bort en central del av FTN-händelsen. Ni har heller inte motsvarande variation över många oberoende pensionsplaner. Metoden är explicit, men den svarar inte på er urvalsfråga utan en väsentlig omformulering.

### Hartzmark & Sussman (2019): viktig metodjämförelse, ingen automatisk identifikation

*Do Investors Value Sustainability? A Natural Experiment Examining Ranking and Fund Flows*, JF 74, 2789–2837. [Artikel](https://doi.org/10.1111/jofi.12841), [läst marsversion 2019](https://www.ecgi.global/sites/default/files/working_papers/documents/finalhartzmarksussman2.pdf).

Arbetsversionens Tabell 3 använder flödesregressioner med ratingkategorier och kategori×månadseffekter; Tabell 4 använder regression discontinuity vid ratinggränser. Artikeln är alltså inte bara en RD-studie. Den gemensamma lanseringen av synliga ratings och deras koppling till redan tillgänglig information är också viktig för argumentet.

Ni kan efterlikna flödesfigurer och panelregressioner. Ni kan inte därmed låna artikelns kausala tolkning. FTN:s beslut är både urval och en ändring av ekonomiska villkor. En RD kräver dessutom verifierad tilldelningsregel, poäng, tillräckligt många närliggande anbud samt stöd för jämförbarhet och frånvaro av manipulation. Några fonder precis över och under en rangordningsgräns räcker inte.

## Ytterligare sökspår och varför de inte vann

Detta är screening, inte påståenden om fullständig läsning av varje artikel.

| Kandidat och kontrollerad källa | Varför inte huvudankare nu? |
|---|---|
| [Harrison, Parada-Contzen & Villena (2023), pensionsauktioner i Chile](https://pure.uai.cl/en/publications/can-auctions-increase-competition-in-the-pension-funds-market-the/) | Stark institutionell träff: avgifter, konkurrens och pensionsupphandling. Författarsammanfattning/förlagstext kontrollerad; full metod inte verifierad. Journal of Policy Modeling finns inte på kursens angivna lista. Bra bakgrundskandidat. |
| [Kurach, Kuśmierczyk & Papla (2019), Can Auctions Help Reduce Mandatory Pension Fund Fees?](https://doi.org/10.1017/S1474747217000440) | Originalet använder laboratorieexperiment. Metoden går inte att återanvända med er historiska fondpanel. Tidskriften finns inte på listan. |
| [Hong, Lu & Pan, Fintech Platforms and Mutual Fund Distribution](https://pubsonline.informs.org/doi/10.1287/mnsc.2022.01966) | Staggerad plattformsanslutning är relevant, men utfallet är framför allt prestationsjagande. Förlagets abstract kontrollerat; full metod inte färdiggranskad. Management Science finns inte på den lokala kurslistan. |
| [Evans & Fahlenbrach (2012), Retail–Institutional Fund Twins](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1907149) | Intressant för avgiftsspillover från institutionell övervakning. Abstract kontrollerat; full metod inte åtkomlig. Separata tvillingportföljer är inte samma sak som PPM- och övriga ägare i samma fond. |
| [Cohen & Schmidt (2009), Attracting Flows by Attracting Big Clients](https://doi.org/10.1111/j.1540-6261.2009.01496.x) | Stor pensionskund och fondflöden är relevant. Abstract kontrollerat. Paperets bredare konflikt- och portföljtest ger inte en verifierad färdig design för externa FTN-flöden. |
| [Kaniel & Parham (2017), WSJ Category Kings](https://www.sciencedirect.com/science/article/pii/S0304405X16302008) | Nära för synlighet och fondfamiljsspillover. Förlagstext kontrollerad. Jämförelser vid en listgräns kräver en motsvarande trovärdig gräns i FTN. |
| [Ferraz, Finan & Szerman, Procuring Firm Growth](https://sites.google.com/site/claudferraz/research) | Offentlig kontraktsvinst och tillväxt utanför ursprunglig affär är relevant. Författarens sida anger fortfarande working paper/under revision; ingen godkänd tidskrift verifierad. Företags- och auktionsdata skiljer sig dessutom väsentligt från fondpanelen. |

Tidskriftskravet bygger på [course_context/README.md](../course_context/README.md), avsnitt Litteraturregler. Det säger något om kursens angivna centrala referenser, inte om artiklarnas allmänna kvalitet. En artikel utanför listan kan fortfarande bidra till bakgrunden.

## Vad måste fungera innan ett ankare låses?

1. **Fondidentiteten:** totalfond eller andelsklass måste vara samma ekonomiska enhet i Morningstar och PPM. Summera inte fondtotaler en gång per andelsklass. Samordna valuta, datum, fusioner och redovisade flöden.
2. **Externa flöden:** subtrahera PPM-flöde i kronor från motsvarande totalflöde i kronor. Subtrahera inte två procentsatser med olika kapitalbas. Kontrollera att fondbyten inte skapar bokföringsartefakter i denna differens.
3. **Händelsen:** dokumentera besked, genomförande, överklaganden och förhandsinformation separat. Fond som inte lämnat anbud är inte samma sak som fond som förlorat efter utvärdering.
4. **Oberoende jämförelse:** kategoriaggregat som inkluderar alla behandlade fonder kan absorbera själva reformeffekten. Välj jämförelsefonder före utfallsläsningen och pröva rimliga alternativ. Matchning gör inte urvalet slumpmässigt.
5. **Dynamik:** en normalflödesmodell som under efterperioden använder observerade eftersläpande flöden kan absorbera delar av en tidigare reaktion. Skilj ett villkorat abnormalflöde från den totala kumulativa effekten; dokumentera prognosmetoden.
6. **Osäkerhet:** många fondmånader är inte många oberoende upphandlingar. Gemensamma beslut och kategoriavkastningar skapar beroende. Visa resultat per upphandling och känslighet när en upphandling i taget tas bort. Få kluster kan göra även bootstrap osäker.
7. **Replikationsnivå:** kontrollera slutversionen innan ekvationer eller tabeller kallas exakt replikerade. Om ratinghistorik saknas är FTN-studien en metodtillämpning, inte en separat replikation av Morningstar-resultatet.

Nästa konkreta arbetsprodukt bör vara en liten datamatris för tidiga upphandlingar: fond-ID, status, beskedsdatum, implementeringsdatum, minst ett års förhistorik och sex månaders efterdata där sådan finns, samt matchat PPM- och totalflöde. Jag har inte gjort det datatestet i denna litteraturgranskning, så faktisk åtkomst och täckning är fortfarande öppna frågor.

**Beslutsregel:** börja med Star Power om externa flöden är huvudfrågan och datatestet fungerar. Om ni prioriterar avgifter eller urvalskvalitet, välj och formulera den frågan först; byt inte bara artikelnamnet över en oförändrad design. Inget av de undersökta alternativen är ännu ett verifierat nära-exakt och datamässigt färdigt FTN-ankare.
