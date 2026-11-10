# Steg 12: nyemissioner och OMXS30

Flyttat från `runda11.py` (del F) och `runda10.py` (T28), körda 2 nov 2026, metoden oförändrad.

## Jämförelse med körningen 2 november

Alla jämförda siffror är desamma.

## A. Nyemissioner: förändring i log antal aktier, AD−5 till ED+60 (G&S avsnitt 2.4.3)

| Rad | Medel (%) | 95 % intervall | p | N | Andel över 1 % | Andel över 5 % |
|---|---|---|---|---|---|---|
| tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter) | 0.50 | −1.61 till 2.76 | 0.688 | 2586 |  |  |
| 2007–11: nästan tillagda, medel (%) | 1.26 |  |  | 354 | 0.09 | 0.05 |
| 2007–11: tillägg, medel (%) | 0.69 |  |  | 27 | 0.11 | 0.07 |
| 2012–16: nästan tillagda, medel (%) | 2.14 |  |  | 410 | 0.09 | 0.04 |
| 2012–16: tillägg, medel (%) | 2.92 |  |  | 47 | 0.15 | 0.11 |
| 2017–21: nästan tillagda, medel (%) | 3.60 |  |  | 878 | 0.13 | 0.09 |
| 2017–21: tillägg, medel (%) | 3.29 |  |  | 78 | 0.26 | 0.15 |
| 2022–26: nästan tillagda, medel (%) | 1.49 |  |  | 712 | 0.09 | 0.05 |
| 2022–26: tillägg, medel (%) | 3.03 |  |  | 80 | 0.10 | 0.05 |

## B. OMXS30 jämfört med OMXSB (G&S tabell 8)

| Urval | Rad | Medel | 95 % intervall | N | Kluster |
|---|---|---|---|---|---|
| tabell 1 (10 borttag ute) | OMXS30, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.21 | −2.65 till 3.25 | 19 | 14 |
| tabell 1 (10 borttag ute) | OMXS30, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.69 | −3.34 till 7.16 | 17 | 12 |
| tabell 1 (10 borttag ute) | OMXS30, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.44 | −2.03 till 3.83 | 36 | 15 |
| tabell 1 (10 borttag ute) | OMXSB, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.57 | 1.20 till 4.03 | 256 | 38 |
| tabell 1 (10 borttag ute) | OMXSB, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.13 | 0.11 till 4.11 | 215 | 38 |
| tabell 1 (10 borttag ute) | OMXSB, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.37 | 1.06 till 3.73 | 471 | 39 |
| tabell 1 (10 borttag ute) | styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3 | 3.67 |  | 507 | 54 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.21 | −2.58 till 3.39 | 19 | 14 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.69 | −3.45 till 7.05 | 17 | 12 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.44 | −1.96 till 3.86 | 36 | 15 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.57 | 1.22 till 4.00 | 256 | 38 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.03 | 0.07 till 3.94 | 206 | 38 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.33 | 1.04 till 3.64 | 462 | 39 |
| som 2 nov (19 flaggade borttag ute) | styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3 | 3.66 |  | 498 | 54 |

Styrkan räcker inte för att testa skillnaden mellan indexen (MDE över gränsen 3 procentenheter). Därför redovisas bara medelvärden.
