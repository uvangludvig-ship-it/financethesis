# Steg 12: nyemissioner och OMXS30

Flyttat från `runda11.py` (del F) och `runda10.py` (T28), körda 2 nov 2026, metoden oförändrad.

## Jämförelse med körningen 2 november

Alla jämförda siffror är desamma.

## A. Nyemissioner: förändring i log antal aktier, AD−5 till ED+60 (G&S avsnitt 2.4.3)

| Rad | Medel (%) | 95 % intervall | p | N | Andel över 1 % | Andel över 5 % |
|---|---|---|---|---|---|---|
| tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter) | 1.01* | −0.05 till 2.11 | 0.063 | 2586 |  |  |
| andel med ökning över 1 %: tillägg minus nästan tillagda, fasta effekter per översyn (procentenheter) | 5.84** | 0.34 till 11.30 | 0.039 | 2586 |  |  |
| andel med ökning över 5 %: tillägg minus nästan tillagda, fasta effekter per översyn (procentenheter) | 3.72* | −0.46 till 8.27 | 0.086 | 2586 |  |  |
| tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter), utan splitjustering | 0.50 | −1.63 till 2.76 | 0.701 | 2586 |  |  |
| 2007–11: nästan tillagda, medel (%) | 0.58 |  |  | 354 | 0.08 | 0.04 |
| 2007–11: nästan tillagda, medel (%), utan splitjustering | 1.26 |  |  | 354 | 0.09 | 0.05 |
| 2007–11: tillägg, medel (%) | 0.69 |  |  | 27 | 0.11 | 0.07 |
| 2007–11: tillägg, medel (%), utan splitjustering | 0.69 |  |  | 27 | 0.11 | 0.07 |
| 2012–16: nästan tillagda, medel (%) | 0.29 |  |  | 410 | 0.07 | 0.02 |
| 2012–16: nästan tillagda, medel (%), utan splitjustering | 2.14 |  |  | 410 | 0.09 | 0.04 |
| 2012–16: tillägg, medel (%) | 2.92 |  |  | 47 | 0.15 | 0.11 |
| 2012–16: tillägg, medel (%), utan splitjustering | 2.92 |  |  | 47 | 0.15 | 0.11 |
| 2017–21: nästan tillagda, medel (%) | 1.26 |  |  | 878 | 0.11 | 0.07 |
| 2017–21: nästan tillagda, medel (%), utan splitjustering | 3.60 |  |  | 878 | 0.13 | 0.09 |
| 2017–21: tillägg, medel (%) | 2.40 |  |  | 78 | 0.24 | 0.14 |
| 2017–21: tillägg, medel (%), utan splitjustering | 3.29 |  |  | 78 | 0.26 | 0.15 |
| 2022–26: nästan tillagda, medel (%) | 0.41 |  |  | 712 | 0.08 | 0.04 |
| 2022–26: nästan tillagda, medel (%), utan splitjustering | 1.49 |  |  | 712 | 0.09 | 0.05 |
| 2022–26: tillägg, medel (%) | 0.43 |  |  | 80 | 0.06 | 0.01 |
| 2022–26: tillägg, medel (%), utan splitjustering | 3.03 |  |  | 80 | 0.10 | 0.05 |

Splitjusterade rader: 61 av 2586 (|ln(faktor(b)/faktor(a))| > ln 1,4). Rader med |dlog| > 30 före justering: 71, efter: 25.

### De 20 största |dlog_just| (kontrollera mot pressmeddelanden)

| Bolag (RIC) | Översyn | Grupp | dlog utan justering | dlog_just | justerad |
|---|---|---|---|---|---|
| INTRUM.ST | 2026H1 | nästan tillagd | 315.82 | 154.36 | ja |
| COREb.ST | 2021H1 | nästan tillagd | 113.01 | 113.01 | nej |
| HLDX.ST^I22 | 2011H1 | nästan tillagd | 69.74 | −111.46 | ja |
| ORES.ST | 2011H2 | nästan tillagd | −77.58 | −77.58 | nej |
| VOLO.ST | 2026H1 | nästan tillagd | 0.00 | −73.38 | ja |
| SOBIV.ST | 2009H2 | nästan tillagd | 142.49 | 73.32 | ja |
| ISOFOL.ST | 2021H1 | nästan tillagd | 66.14 | 66.14 | nej |
| XANOb.ST | 2014H1 | nästan tillagd | 0.00 | −61.85 | ja |
| SBBd.ST | 2019H2 | nästan tillagd | 60.05 | 60.05 | nej |
| BURE.ST | 2009H2 | nästan tillagd | 57.69 | 57.69 | nej |
| SFAST.ST | 2021H1 | nästan tillagd | 1.43 | 56.87 | ja |
| EG7.ST | 2020H2 | nästan tillagd | 54.57 | 54.57 | nej |
| PEABb.ST | 2009JAN | nästan tillagd | 54.07 | 54.07 | nej |
| KAHL.ST^J19 | 2011H2 | nästan tillagd | 109.86 | 53.71 | ja |
| BEFsdb.ST^L17 | 2012H2 | tillägg | 51.08 | 51.08 | nej |
| ETRN.ST^A22 | 2013H2 | tillägg | 48.01 | 48.01 | nej |
| SAGAd.ST | 2019H1 | nästan tillagd | 47.53 | 47.53 | nej |
| TIETOS.ST | 2019H2 | nästan tillagd | 46.96 | 46.96 | nej |
| ICAA.ST^A22 | 2013H1 | nästan tillagd | 41.43 | 41.43 | nej |
| NYOR.ST | 2009H2 | nästan tillagd | 40.55 | 40.55 | nej |

## B. OMXS30 jämfört med OMXSB (G&S tabell 8)

| Urval | Rad | Medel | 95 % intervall | N | Kluster |
|---|---|---|---|---|---|
| tabell 1 (10 borttag ute) | OMXS30, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.21 | −2.66 till 3.22 | 19 | 14 |
| tabell 1 (10 borttag ute) | OMXS30, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.69 | −3.45 till 7.29 | 17 | 12 |
| tabell 1 (10 borttag ute) | OMXS30, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.44 | −1.96 till 3.85 | 36 | 15 |
| tabell 1 (10 borttag ute) | OMXSB, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.57 | 1.19 till 4.01 | 256 | 38 |
| tabell 1 (10 borttag ute) | OMXSB, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.13 | 0.16 till 4.10 | 215 | 38 |
| tabell 1 (10 borttag ute) | OMXSB, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.37 | 1.10 till 3.67 | 471 | 39 |
| tabell 1 (10 borttag ute) | styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3 | 3.67 |  | 507 | 54 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.21 | −2.59 till 3.22 | 19 | 14 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.69 | −3.35 till 7.13 | 17 | 12 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.44 | −1.98 till 3.76 | 36 | 15 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.57 | 1.20 till 4.04 | 256 | 38 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.03 | 0.08 till 3.92 | 206 | 38 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.33 | 1.04 till 3.63 | 462 | 39 |
| som 2 nov (19 flaggade borttag ute) | styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3 | 3.66 |  | 498 | 54 |

Styrkan räcker inte för att testa skillnaden mellan indexen (MDE över gränsen 3 procentenheter). Därför redovisas bara medelvärden.
