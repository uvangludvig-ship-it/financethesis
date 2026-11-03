# Rättelser 3 november: plan, skriven 15:21:30 CET (klockslag från `date`) innan något körts

Explorativt: alla resultat i runda 11 och den andra chattens granskning (commit 2eedada) är kända. Syftet är att rätta mätfel, inte att söka nya utfall.

**D (indexfondernas köp).**
1. D sätts till saknat, inte 0, när ingen OMXSB-indexfond rapporterar både före AD (inom 120 dagar) och efter ED (inom 45 dagar), räknat över alla fondens rapporter. Rapporterar minst en sådan fond, och den inte äger aktien, är D = 0 som förut.
2. Händelser där aktien senare splittats utesluts som i runda 11.
3. Klassningen efter dagens fondnamn går inte att rätta före 2019. Den redovisas som begränsning.

**M.** Tabell 5 och 6 i runda 11 räknas om med rättat D. Intervallen för M per period tar med alla bootstrapdragningar: om medel-D ≤ 0 i en dragning räknas M som oändligt, så att intervallet blir obegränsat i stället för att dragningen tas bort. Inga nya test.

**Kontroll mot SHoF.** Förväntat D = aktiens fria flytande andel × OMXSB-fondernas ägarandel av indexet (SHoF-förmögenhet / indexets börsvärde, `runda11_resultat/G_figur1_figur5.csv`, samma år). M räknas också med förväntat D, per period, på samma händelser. Förbehåll: indexets börsvärde är för stort, eftersom några utländska bolag räknas med hela det globala börsvärdet, så förväntat D blir för litet och M för stort.

**T29.** Inga nya beräkningar. Redovisas som villkorat räkneexempel med siffrorna från den andra chattens granskning (`output/omxsb_execution_followup_20261102/cost_audit/REPORT.txt`).

**Dokument.** Allt samlas i `RATTELSER_2026-11-03.md`, som gäller före äldre dokument där de skiljer sig.
