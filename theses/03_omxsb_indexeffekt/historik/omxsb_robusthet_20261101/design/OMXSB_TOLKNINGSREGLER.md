# Tolkningsregler efter rättelsen

Teknisk arbetsanteckning 1 november 2026. Ingen uppsatstext.

| Påstående | Status och korrekt avgränsning |
|---|---|
| En tredjedel urval, två tredjedelar kausal indexeffekt | Inte identifierat. Rå CAR minus regressionskoefficient är ingen kausal dekomposition; urval, vikter och antaganden måste redovisas. |
| Köptrycket är noll eftersom A och B stiger lika | Fel inferens. Efterfrågan kan spridas mellan aktieslagen. En osäker skillnad är inte heller bevis på likhet. |
| Multiplikatorn är högst 0,57 | Ingen tillhörande verifierad kod/resultatkälla i det levererade paketet. Ska inte användas. En relativ aktieslagskvot är dessutom inte samma estimand som total prisrespons. |
| Den kvarvarande effekten beror på uppmärksamhet | Oprövad mekanism. Gemensamma nyheter, efterfrågespridning, benchmarkhandel och urval kan inte särskiljas av A/B ensamt. |
| Ingen kort återgång innebär permanent effekt | Fel. Endast återgång inom det observerade fönstret kan begränsas, med konfidensintervall och samma händelseurval. |
| Sverige saknar migration | Inte färdigtestat. Avsaknad av en identisk S&P-indexfamilj visar inte att alla motverkande indexflöden saknas. |
| 58 användbara tvillinghändelser | 58 kandidater i den importerade listan; vissa noteringsdatum och externa identifierare är antagna. Slutligt validerat urval är inte fastställt. |
| Förstasteget 0,74 visar att systern inte handlas | Medlet går att summera ur den äldre filen, men fast fondpopulation, fullständiga rapporter, historiska ISIN, splitjustering och klassnämnare är inte färdigvaliderade. Kinnevik A hade ett konkret felaktigt ISIN. |
| Alla tester skrevs innan några utfall sågs | Fel. Tidigare pilotutfall och prisbanor var kända. Rättelsespecifikationen redovisar detta uttryckligen. |
| T5:s stora kontroller är nästan invalda | Inte verifierat. Storleksurvalet rekonstruerar inte Nasdaq-reglerna eller historisk behörighet. Saknade identifierare får inte bli icke-medlemskap. |
| Inga nya tester får ändra slutsatsen | Fel arbetsregel. Begränsa omotiverad resultatsökning, men genomför nödvändiga rättelser och specificerade kontroller oavsett utfall. |

G&S:s avkastningsmått och efterfrågemultiplikator avser inte definitionsmässigt enbart kortvarig avvikelse mellan två aktieslag. Kopplingen till ankaret ska göras på samma mätobjekt, tidsfönster och urval.

Säkra uppgifter om vad som faktiskt körts hämtas ur `output/omxsb_robusthet_20261101/RESULTAT.md` och dess manifest. Äldre arbetsmaterial ligger kvar som historik och ska inte blandas in som resultat från den korrigerade körningen.
