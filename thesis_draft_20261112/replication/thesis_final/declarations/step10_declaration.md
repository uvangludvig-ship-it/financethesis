# Deklaration: steg 10 (metod 5.3 och 5.4)

Skriven 2026-11-10 17:11 CET, innan körningen.

`code/10_composition_runup.py` återskapar runda 11 A (G&S tabell 2, metod 5.3) och runda 11 B (G&S tabell 4, metod 5.4) ur `data/events/omxsb_changes_corrected_2007_2026.csv` (468 händelser, utan de 19 flaggade borttagen, som i runda 11). Kontrollerna `k_oms`, `k_storlek`, `k_wz`, `k_ana` och fönstren `car_tot`, `pre10` till `pre100` tas som de står i filen (räknade i runda 11). Inferens som tabell 1: klustrat per översyn, restriktiv wild cluster bootstrap med 9 999 dragningar, intervall genom testinversion; CR1-intervall bredvid.

Utfall: (1) tabell 2 utan och med de fyra centrerade kontrollerna, skillnaden 2007–11 minus 2022–26 och kontrollernas koefficienter; (2) ny rad: utan kontroller på samma händelser som med kontroller, eftersom metodtexten 5.3 kräver samma händelser; (3) tabell 4, CAR [AD−n, AD−1] för n = 10, 20, 50, 100 per period och typ.

Kontroll: skattningarna ska vara identiska med runda 11, CR1-intervallen likaså; p kan skilja i tredje decimalen.

Läsning: faller skillnaden 2007–11 minus 2022–26 för tillägg under 5 procentenheter eller blir den osignifikant på 10 % i rad (2), skrivs det ut. Huvudtabellerna ändras inte.

## Tillägg 2026-11-10 17:21, före omkörningen

Urvalet i steg 10 följer nu `sample_rule_declaration.md`: samma händelser som tabell 1 (10 borttag ute enligt G&S regel), perioder efter ändringsåret, och fönstren före beskedet räknas i skriptet ur kurserna. Kontrollerna hämtas som förut ur den rättade händelsefilen. Tillkommer: M-regressionen utan kontroller på samma händelser som med, och kursbanan AD−100 till AD+14 (G&S figur 7, runda 11 I). Kontroll: tilläggens siffror ska vara identiska med runda 11.
