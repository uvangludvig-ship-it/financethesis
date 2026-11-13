# Deklaration: splitfaktor för Lipper-innehav

Låst tid från kommandot `date`: **2026-11-05 08:17:00 CET (+0100)**.

Denna fil ska committas innan LSEG-kurser hämtas, k beräknas eller nya kontrollresultat öppnas. Tidigare projektresultat är kända. Hittills har endast kod, scheman, antal och datum/identifierare granskats: 468 händelser, 150 med `split=True`, 318 med `split=False`. Inga nya faktorer eller FI-jämförelser har beräknats.

## Avgränsning

Endast tre filer skapas i `code/claude_checks/splitfaktor/`: denna deklaration, `splitfaktor_events.csv` och `kontroll.md`. Andra repofiler ändras inte, inklusive gamla resultat, fondklassning och AI-logg (användarens uttryckliga filbegränsning gäller). Ingen ny avkastning, multiplikator, hypotesvariant eller ny fondklassning körs. Teknisk kod och leverantörssvar får hållas i en privat temporär katalog utanför repot och refereras med hash i kontrollrapporten.

## Fryst underlag och datum

Alla 468 rader i `handelser_rattade.csv` behålls, i samma ordning. Använd dess `event_id`, `RIC`, `ED`, `sh_ed` och redan bestämda splitflagga. Det gamla fältet `k` i händelsefilen är inte denna nya faktor. Inga manuella RIC-ersättningar eller urvalsändringar.

Lipperfilen innehåller två `asof` per händelse, en för `snap=fore` och en för `snap=efter`. **Leveransens `asof` är det unika datumet för `snap=efter`**, det vill säga efter-snapshoten (normalt ED+45 kalenderdagar). Saknat eller motstridigt datum ger saknad faktor; inget datum antas. Före-datumet sparas i arbetsunderlaget för källtolkning men är inte en alternativ slutpunkt.

Viktig källbegränsning: `asof` är det historiska datumet för innehavsförfrågan. Det är inte därmed bevisat att `Fund Shares Held (Adjusted)` uttrycks i just det datumets aktieenheter. Om innehaven i stället är justerade till hämtningstidpunkten kan den föreslagna kvoten vara otillräcklig. Vi byter inte tyst till dagens datum eller senare aktieantal för att få godkända kontroller.

## LSEG-källa och beräkning

Hämta samma instruments `TR.ClosePrice(Adjusted=0)`, `TR.ClosePrice(Adjusted=1)` och prisdatum, i samma valuta, via LSEG Workspace. Använd inte `TR.PriceClose` med en justeringsparameter som fältet inte stöder. Hämta dagliga observationer från sju kalenderdagar före varje måldatum till måldatum. Använd sista gemensamma positiva ojusterade/justerade stängningskurs med samma faktiska prisdatum, på eller före måldatum och högst sju kalenderdagar gammal. Detta hanterar helger; framtida observationer och olika datum i kvotens två priser tillåts inte. Saknade eller motstridiga prispar blir saknade, aldrig 0 eller 1. Dokumentera faktisk kursdag och ursprungligt svar i kontrollunderlaget.

`r(t) = ojusterad stängningskurs(t) / justerad stängningskurs(t)`

`k = r(ED) / r(asof_efter)`

`sh_ed_adj = sh_ed * k`

Ingen avrundning till en förväntad splitkvot. Varken marknadsvärde/aktieantal eller totalavkastningsindex används som ersättning för det direkta prisparet. En 4:1-split mellan ED och asof ska ge k nära 4. En split efter båda datumen kan däremot finnas i båda prisernas justeringsfaktorer och då ta ut sig i kvoten; detta är en begränsning som ska synliggöras, inte ändras efter resultat.

För kontrollens D behålls samma täljare, rapportfilter, fondklassning och riktning som i rättelsefilens `D_ny`: `D_adj = D_ny / k`. Det är algebraiskt samma innehavsförändring dividerad med `sh_ed_adj`. Saknat `D_ny` förblir saknat. Denna uppgift rättar endast den föreslagna enhetsskalningen.

## Kontroller och stoppregel

Beräkna först faktorer för alla händelser som källan medger och redovisa samtliga saknade rader. Utvärdera därefter kontrollerna i ordning; vid första underkända eller ej verifierbara kontroll stoppas fortsatt ekonomisk analys och senare kontroller märks ej genomförda. Inga utfall eller gränser ändras efteråt.

1. **Osplittade:** för alla beräkningsbara händelser med befintlig `split=False` krävs `abs(k-1) <= 0.01`. En procent är den här i förväg låsta tolkningen av ungefär 1. Redovisa N, median, min/max och alla avvikelser. Bristande täckning redovisas separat och ger inget påstående om att samtliga 468 är rättade.
2. **FI:** länka på exakt RIC och review, kontrollera unik nyckel och samma tillägg/borttag. Använd endast FI `status=ok`, ED under 2019–2026, befintlig `split=True`, ändliga `D_ny`, k och `netto_OMXSB_ny`. Beräkna eventviktad Pearsonkorrelation samt den signerade medelskillnaden `mean(D_adj - netto_OMXSB_ny)`, i procentenheter. Godkänt endast om korrelationen är minst 0.8 och absolut medelskillnad högst 0.3. Minst tre par och icke-konstanta serier behövs för en meningsfull korrelation. Redovisa även antal och motsvarande osplittade jämförelse som diagnostik, utan att byta krav eller primärt urval.
3. **Tre största k:** välj de tre händelserna med högst ändlig k, fallande k och därefter event_id alfabetiskt. Inget byte till mer gynnsamma fall. Kontrollera produkten av fysiska split-/sammanläggningsvillkor mellan de faktiskt använda prisdatumen mot bolags- eller Nasdaq-original. Kräv relativ avvikelse högst 1 procent. Om de tre avser samma bolag anges detta; annan kapitalhändelse eller saknad primärkälla är inte verifierad fysisk split.

Underkänd kontroll betyder STOPP, inte att de 150 händelserna får återinföras. CSV levereras ändå med observerade faktorer och tomma värden där de saknas, tillsammans med tydlig underkänd status i kontrollrapporten. Ingen M/CAR-analys eller ändring i huvudresultat.

## Leverans

CSV-kolumner exakt: `event_id,RIC,ED,asof,k,sh_ed,sh_ed_adj`.

`kontroll.md` redovisar deklarationscommit, körtid, källfält/parametrar, datatäckning, genomförda kontrollmått, saknade/underkända händelser och slutstatus. Den ska skilja matematiskt beräknad kvot från verifierad enhetskorrigering av Lippers innehav. Oförändrade indata kontrolleras med SHA256.

## Frysta indatahashar

- `code/claude_checks/data/runda8_fondagare.csv.gz`: `67ec3e7dd87f8eea512ae911a6301a1819981021fb6fa768b4a121502e14e1d6`
- `code/claude_checks/rattelser_2026-11-03_resultat/handelser_rattade.csv`: `05d301dad399bfad98c348ac8cfe1df8eacd2c1725989cb2d465c01a8c1701f1`
- `code/claude_checks/nettokop_v2_events.csv`: `1173c25be1d3ed4f31b911531a206bcca8b72b9210b6f50d459f746a37cd394c`
- `code/claude_checks/runda9.py`: `8f717281116f7c1b5624b60ac594e0e84f4bd4c0638392bbdb0bb6209176e484`
- `code/claude_checks/rattelser_2026-11-03.py`: `5f9fd2c5bdea9b8749c2c398fed6a80a8ec8f2ef30c2a00ab3ce2cd1d7f114a9`

## Fältdokumentation läst före beräkning

- LSEG Developer Community: https://community.developers.lseg.com/discussion/121346/query-prices-adjustes-and-unadjusted-for-time-series/p1
- LSEG:s exempel på splitjusterade respektive ojusterade priser: https://community.developers.lseg.com/discussion/89791/does-anybody-know-how-to-download-adjusted-and-not-adjusted-price-for-equity-with-and-without-di/p1
