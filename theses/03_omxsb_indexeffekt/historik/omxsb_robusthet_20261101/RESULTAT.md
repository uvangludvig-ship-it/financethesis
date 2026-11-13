# OMXSB: korrigerad kontrollanalys, version 5

Teknisk resultatrapport, inte uppsatstext. Genererad 2026-11-01T20:00:33.597373+01:00

## Vad denna körning kan säga

T2 är bred panelmatchning på tidigare avkastning och storlek. T5 är en explorativ storleks-/medlemsproxy, inte verifierade nästan tillagda aktier. Historisk huvudlistebehörighet och fullständig medlemskedja är inte säkrade. Alla skattningar är associationer under respektive jämförelse, inte en kausal uppdelning av indexeffekten.

Tidigare resultat var kända före rättelsen. Alla varianter nedan redovisas; ingen väljs för sitt p-värde. T-intervall och wild-bootstrap-p kommer från olika inferensmetoder men avser samma skattning. P-värden är nominella och explorativa.

T5-status: not_estimable_membership_unresolved. 38 av 38 granskade översyner spärras av olösta medlemsuppgifter. Om inga återstår kan ingen T5-regression skattas; detta är ett datastopp, INTE ett nollresultat. Den tidigare +1,68-regressionen kan återskapas från gamla sparade rader, men dess kontrollgrupp är inte här validerad som historiskt behöriga icke-medlemmar.

## Resultat (procentenheter)

| Test | Typ | Period | Variant | Skattning | 95% t-intervall | p teckenbyte | p wild | N | Översyner | Status |
|---|---|---|---|---:|---|---:|---:|---:|---:|---|
| T2_panel_match | addition | before2017 | diff1 | 4.773 | [-0.016, 9.561] | 0.051 | 0.051 | 79 | 19 | ok |
| T2_panel_match | addition | before2017 | diff3 | 4.614 | [0.697, 8.531] | 0.024 | 0.023 | 76 | 19 | ok |
| T5_exploratory_proxy | addition | before2017 | proxy_all | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |
| T5_exploratory_proxy | addition | before2017 | proxy_common_support | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |
| T2_panel_match | addition | since2017 | diff1 | 2.069 | [0.109, 4.030] | 0.040 | 0.038 | 157 | 19 | ok |
| T2_panel_match | addition | since2017 | diff3 | 1.605 | [0.079, 3.131] | 0.036 | 0.034 | 156 | 19 | ok |
| T5_exploratory_proxy | addition | since2017 | proxy_all | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |
| T5_exploratory_proxy | addition | since2017 | proxy_common_support | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |
| T2_panel_match | deletion | before2017 | diff1 | -4.727 | [-8.460, -0.994] | 0.015 | 0.015 | 79 | 18 | ok |
| T2_panel_match | deletion | before2017 | diff3 | -6.686 | [-10.550, -2.822] | 0.002 | 0.002 | 76 | 18 | ok |
| T5_exploratory_proxy | deletion | before2017 | proxy_all | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |
| T5_exploratory_proxy | deletion | before2017 | proxy_common_support | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |
| T2_panel_match | deletion | since2017 | diff1 | -0.849 | [-2.226, 0.527] | 0.207 | 0.205 | 132 | 19 | ok |
| T2_panel_match | deletion | since2017 | diff3 | -0.939 | [-1.995, 0.117] | 0.081 | 0.080 | 132 | 19 | ok |
| T5_exploratory_proxy | deletion | since2017 | proxy_all | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |
| T5_exploratory_proxy | deletion | since2017 | proxy_common_support | saknas | [saknas, saknas] | saknas | saknas | 0 | 0 | blocked_unresolved_historical_membership |

T2 och rader med review_difference väger varje översyn lika. T5-regressionen är pooled OLS med översynsfasta effekter och klustrad inferens. Dessa estimand ska inte blandas. N i review_difference är antal översynsskillnader; se sparade analysrader för aktieantal.

## Rättelser som genomförts

- Matchningsdata slutar AD−2; utfallet börjar AD−1. Tidigare avkastning omfattar fortfarande 100 handelsdagar.
- Samma reviewviktning i T2:s skattning, intervall, teckenbyte och bootstrap.
- Kontrollval görs innan kontrollens framtida avkastning läses. Saknade utfall ersätts inte med nästa kontroll.
- Nästa översyns händelser används inte för att välja kontrollpoolen. Full händelsecensus används för samma och föregående översyn; olösta identifierare exporteras.
- Tre kontroller betyder tre olika emittentproxyer. Alla matchningar, distanser och balansfält sparas.
- T5 redovisas som proxy. Översyner med olösta medlems-tickers hoppas över i denna proxy; övrig kedjeosäkerhet kvarstår. Båda jämförelsegrupper måste finnas i en översyn.
- Samma T5-urval används i regression och reviewdifferens. Gemensamt stöd redovisas separat och ersätter inte huvudvarianten.
- Simuleringstest hanterar numeriska likheter och ger inte p=0 genom ett begränsat antal dragningar.

## Vad som inte är visat

- Skillnaden mellan rå och justerad avkastning är inte en identifierad andel orsakad av urval.
- Lika A/B-avkastning utesluter inte köptryck som sprids mellan aktieslagen. Relativ A/B-multiplikator är inte total efterfrågeelasticitet.
- Uppgifterna 0,57 och den senare korta återgångskörningen har inte källverifierats i detta paket. A/B-kodens äldre förstasteg har identifierar- och rapporttäckningsproblem; 0,74 ska inte användas som validerat förstasteg.
- Ingen säkerställd återgång under ett ändligt fönster bevisar inte permanent effekt.
- Frånvaro av migration, uppmärksamhet som mekanism och varför Sverige skiljer sig från USA identifieras inte här.

## Kvarstående begränsningar

Panelen är det tillgängliga prisunderlaget, inte en historiskt verifierad census av behöriga OMXSB-kandidater. RIC-stammar är emittentproxyer. Medlemskedjan har kända luckor. Prisavkastning används där totalavkastning saknas, enligt den tidigare replikationen; bolagshändelser måste därför fortsatt beaktas. Komplett utfallsfönster krävs och bortfall kan vara selektivt. Förhandsuppgång kan själv innehålla förväntad indexefterfrågan, så matchning på den skattar inte nödvändigtvis hela effekten av kommande indexmedlemskap. En gemensam stödrange bevisar inte balans eller kausalitet.

Balans, valda kontroller, utfallsbortfall och exakta tidsgränser finns i CSV-filerna. Avkastningar runt FTN har inte beräknats. Originalfiler finns i archive/robusthet_repair_20261101/.

## Körning

python code/build/robusthet_hela.py

Beroenden: numpy, pandas, scipy, pyarrow. Notebooken anropar samma källkod; inga kopierade regressionsfunktioner.
