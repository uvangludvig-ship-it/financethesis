SHoF-källprovet efter inloggningen, 3 november 2026
Teknisk arbetsanteckning. Inte uppsatstext. Inga nya ekonomiska utfall beräknade.

Hämtningen är genomförd

De två förutbestämda utdragen för 20 andelsklasser i fem fonder, 2017-01-01–2023-12-31, har hämtats från SHoF/Morningstar: Re-invested Prices och Valuations. Originalen är lokalt sparade i gitignorerade rådatamappar. Avkastningsindexfilen innehåller 22 872 rader och kapitalfilen 17 923. Båda arkiven klarar integritetskontrollen, saknar oväntade identifierare/datum och har inga dubbletter per klass/datum/avkastningstyp. Alla levererade avkastningsindex är typ 1, totalavkastning. Detaljer och SHA256 finns i ROOT_SOURCE_VERIFICATION.json.

Det konkreta framsteget

För var och en av fem fonder och tio översyner 2019–2023 kontrollerades 25 månadsändpunkter före annonseringen, underlag för 24 historiska månadsintervall. Med de äldre utdragen fanns en representativ SEK-klass med både kapital och avkastningsindex i 8 av 50 fond/översyn-kombinationer. De nya utdragen ger 39 av 50. Den strängare kontrollen, som också kräver underlag för alla då aktiva andelsklasser, klaras av 23 av 50. Dessa är datatäckningsmått, inte antal oberoende händelser eller en styrkeberäkning.

Fond (FI-id)                                Representativ klass   Alla aktiva klasser
SEB Sverigefond Småbolag Chans/Risk (51331)       0 -> 10/10              10/10
Storebrand Sverige (51482)                      8 -> 10/10               6/10
SEB Sverige Indexfond (60087)                    0 ->  9/10               0/10
SEB Sverige Indexnära (60302)                    0 -> 10/10               7/10
Swedbank Robur Access Sverige (60824)            0 ->  0/10               0/10

Detta betyder att bristen i de gamla månadsutdragen delvis gick att reparera genom en ny hämtning. Det betyder ännu inte att hela aktiepopulationen har tillräcklig täckning eller att riskfrågan går att besvara precist. Både källvalidatorn och en oberoende kontroll återger dessa antal.

Vad som återstår i underlagen

- Access Sveriges totalavkastningsserie börjar fortfarande först oktober 2023 i det begärda utdraget. Det är inte reparerat.
- SEB Sverige Indexfond (60087) har lång historik i B-klassen men inte A-klassen. En representativ klass får inte obemärkt ersätta hela fonden; kapital, klassavgifter och historik måste behandlas konsekvent.
- Storebrand har nytillkomna klasser och NOK-klasser. Samma valuta och korrekt klasshantering krävs före summering.
- Morningstars färdigberäknade nettokapitalflöden finns i betydligt större omfattning än de äldre utdragen antydde. De är en separat möjlig källa, även när ett avkastningsindex saknas. Men vissa dagar saknas, och upprepade fondvärden får inte summeras en gång per andelsklass. Saknat flöde har inte ersatts med noll. Den separata källkontrollen redovisar både exakt likhet och avrundning; mycket små skillnader mellan kopior är inte i sig ekonomiska motsägelser.
- Både leverantörens flödesfält och ett flöde beräknat från kapital och avkastning är skattningar. De är inte observerade betalningar eller börsorder.
- Dagens fondregister bevisar inte fullständig historisk klass-, valuta- eller fusionskontinuitet. Sista datarad är heller inte automatiskt bevis på samma underliggande värderingsdag.

Beslut och kvarvarande fråga

Källprovet gav en verklig datavinst, men inte ett nytt uppsatsresultat. Det tidigare generella datastoppet måste därför beskrivas som partiellt reparerat. Ingen statistisk klarteckenbedömning ges här.

Nästa nödvändiga steg är att använda endast validerade källor för att mäta täckningen av fondkapital i de redan låsta händelse- och kontrollaktierna. Först om den täckningen och precisionen räcker är ett nytt ekonomiskt test motiverat. Fonder med tillgängliga data får inte väljas efter vilken riskskillnad de ger, och saknade ägare får inte räknas som riskfria.

Frågan för det testet är om den observerade ökningen av fondägandet sprider exponeringen mot kunduttag eller samlar den hos fonder vars flöden rör sig tillsammans. Det är en fråga om en möjlig konsekvens av ändrat ägande. Det skulle inte i sig förklara indexaktiens prisuppgång, bevisa faktisk tvångsförsäljning eller visa att aktiens realiserade prisrisk förändras.

Inga nya aktieavkastningar, fondavkastningar, flöden eller kovarianser har beräknats i detta källprov. Inga FTN-utfall har öppnats. Tidigare forskningsresultat och negativa kontroller är oförändrade. Teknisk förhandsdeklaration, källmetadata, begränsningar och kontrollkod finns i audit/. Hela tidigare designgranskningen ligger kvar i output/omxsb_design_frontier_20261103; dess uppgift om väntande inloggning beskriver läget före denna hämtning.
