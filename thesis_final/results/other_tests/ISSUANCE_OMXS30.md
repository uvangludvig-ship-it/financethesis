# Steg 12: nyemissioner och OMXS30

Flyttat från `runda11.py` (del F) och `runda10.py` (T28), körda 2 nov 2026, metoden oförändrad.

## Jämförelse med körningen 2 november

Alla jämförda siffror är desamma.

## A. Nyemissioner: förändring i log antal aktier, AD−5 till ED+60 (G&S avsnitt 2.4.3)

| Rad | Medel (%) | 95 % intervall | p | N | Andel över 1 % | Andel över 5 % |
|---|---|---|---|---|---|---|
| tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter) | 0.57 | −0.47 till 1.65 | 0.284 | 2586 |  |  |
| andel med ökning över 1 %: tillägg minus nästan tillagda, fasta effekter per översyn (procentenheter) | 5.77** | 0.27 till 11.24 | 0.042 | 2586 |  |  |
| andel med ökning över 5 %: tillägg minus nästan tillagda, fasta effekter per översyn (procentenheter) | 3.67* | −0.51 till 8.19 | 0.091 | 2586 |  |  |
| tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter), gräns 1,4 utan matchning | 1.01* | −0.04 till 2.09 | 0.059 | 2586 |  |  |
| tillägg minus nästan tillagda, 2007–26, fasta effekter per översyn (procentenheter), utan splitjustering | 0.50 | −1.58 till 2.73 | 0.695 | 2586 |  |  |
| 2007–11: nästan tillagda, medel (%) | 1.55 |  |  | 354 | 0.08 | 0.04 |
| 2007–11: nästan tillagda, medel (%), utan splitjustering | 1.26 |  |  | 354 | 0.09 | 0.05 |
| 2007–11: tillägg, medel (%) | 0.69 |  |  | 27 | 0.11 | 0.07 |
| 2007–11: tillägg, medel (%), utan splitjustering | 0.69 |  |  | 27 | 0.11 | 0.07 |
| 2012–16: nästan tillagda, medel (%) | 0.34 |  |  | 410 | 0.07 | 0.02 |
| 2012–16: nästan tillagda, medel (%), utan splitjustering | 2.14 |  |  | 410 | 0.09 | 0.04 |
| 2012–16: tillägg, medel (%) | 2.92 |  |  | 47 | 0.15 | 0.11 |
| 2012–16: tillägg, medel (%), utan splitjustering | 2.92 |  |  | 47 | 0.15 | 0.11 |
| 2017–21: nästan tillagda, medel (%) | 1.74 |  |  | 878 | 0.11 | 0.07 |
| 2017–21: nästan tillagda, medel (%), utan splitjustering | 3.60 |  |  | 878 | 0.13 | 0.09 |
| 2017–21: tillägg, medel (%) | 2.40 |  |  | 78 | 0.24 | 0.14 |
| 2017–21: tillägg, medel (%), utan splitjustering | 3.29 |  |  | 78 | 0.26 | 0.15 |
| 2022–26: nästan tillagda, medel (%) | 0.74 |  |  | 712 | 0.08 | 0.04 |
| 2022–26: nästan tillagda, medel (%), utan splitjustering | 1.49 |  |  | 712 | 0.09 | 0.05 |
| 2022–26: tillägg, medel (%) | 0.43 |  |  | 80 | 0.06 | 0.01 |
| 2022–26: tillägg, medel (%), utan splitjustering | 3.03 |  |  | 80 | 0.10 | 0.05 |

Splitjusterade rader: 48 av 2586 (|ln k| > ln 1,4 och faktorn förklarar aktieändringen inom 10 %); med gränsen 1,4 ensam: 61. Rader med |dlog| > 30 före justering: 71, efter: 23.

### De 20 största |dlog_just| (kontrollera mot pressmeddelanden)

| Bolag (RIC) | Översyn | Grupp | dlog utan justering | dlog_just | justerad |
|---|---|---|---|---|---|
| INTRUM.ST | 2026H1 | nästan tillagd | 315.82 | 315.82 | nej |
| NCAB.ST | 2021H2 | nästan tillagd | 230.26 | 230.26 | nej |
| CHERb.ST^E19 | 2017H1 | nästan tillagd | 180.44 | 180.44 | nej |
| SOBIV.ST | 2009H2 | nästan tillagd | 142.49 | 142.49 | nej |
| COREb.ST | 2021H1 | nästan tillagd | 113.01 | 113.01 | nej |
| KAHL.ST^J19 | 2011H2 | nästan tillagd | 109.86 | 109.86 | nej |
| ORES.ST | 2011H2 | nästan tillagd | −77.58 | −77.58 | nej |
| HLDX.ST^I22 | 2011H1 | nästan tillagd | 69.74 | 69.74 | nej |
| COALA.ST^D24 | 2008H2 | nästan tillagd | 69.31 | 69.31 | nej |
| ISOFOL.ST | 2021H1 | nästan tillagd | 66.14 | 66.14 | nej |
| SBBd.ST | 2019H2 | nästan tillagd | 60.05 | 60.05 | nej |
| BURE.ST | 2009H2 | nästan tillagd | 57.69 | 57.69 | nej |
| EG7.ST | 2020H2 | nästan tillagd | 54.57 | 54.57 | nej |
| PEABb.ST | 2009JAN | nästan tillagd | 54.07 | 54.07 | nej |
| BEFsdb.ST^L17 | 2012H2 | tillägg | 51.08 | 51.08 | nej |
| ETRN.ST^A22 | 2013H2 | tillägg | 48.01 | 48.01 | nej |
| SAGAd.ST | 2019H1 | nästan tillagd | 47.53 | 47.53 | nej |
| SAGAa.ST | 2019H1 | nästan tillagd | 47.53 | 47.53 | nej |
| TIETOS.ST | 2019H2 | nästan tillagd | 46.96 | 46.96 | nej |
| ICAA.ST^A22 | 2013H1 | nästan tillagd | 41.43 | 41.43 | nej |

### Över gränsen 1,4 men inte justerade (faktorn förklarar inte aktieändringen; kontrollera för hand)

| Bolag (RIC) | Översyn | Grupp | dlog (räknas) | 100·ln k | dlog med gränsen 1,4 |
|---|---|---|---|---|---|
| INTRUM.ST | 2026H1 | nästan tillagd | 315.82 | −161.46 | 154.36 |
| NCAB.ST | 2021H2 | nästan tillagd | 230.26 | −219.84 | 10.42 |
| CHERb.ST^E19 | 2017H1 | nästan tillagd | 180.44 | −161.97 | 18.47 |
| SOBIV.ST | 2009H2 | nästan tillagd | 142.49 | −69.18 | 73.32 |
| KAHL.ST^J19 | 2011H2 | nästan tillagd | 109.86 | −56.15 | 53.71 |
| HLDX.ST^I22 | 2011H1 | nästan tillagd | 69.74 | −181.20 | −111.46 |
| COALA.ST^D24 | 2008H2 | nästan tillagd | 69.31 | −37.12 | 32.19 |
| SAGAa.ST | 2019H1 | nästan tillagd | 47.53 | −60.93 | −13.40 |
| SFAST.ST | 2021H1 | nästan tillagd | 1.43 | 55.44 | 56.87 |
| BERGb.ST | 2017H1 | nästan tillagd | 0.05 | −37.71 | −37.66 |
| ACANb.ST^E19 | 2014H1 | nästan tillagd | 0.00 | 38.54 | 38.54 |
| XANOb.ST | 2014H1 | nästan tillagd | 0.00 | −61.85 | −61.85 |
| VOLO.ST | 2026H1 | nästan tillagd | 0.00 | −73.38 | −73.38 |

## B. OMXS30 jämfört med OMXSB (G&S tabell 8)

| Urval | Rad | Medel | 95 % intervall | N | Kluster |
|---|---|---|---|---|---|
| tabell 1 (10 borttag ute) | OMXS30, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.21 | −2.59 till 3.27 | 19 | 14 |
| tabell 1 (10 borttag ute) | OMXS30, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.69 | −3.35 till 7.16 | 17 | 12 |
| tabell 1 (10 borttag ute) | OMXS30, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.44 | −1.99 till 3.83 | 36 | 15 |
| tabell 1 (10 borttag ute) | OMXSB, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.57 | 1.19 till 4.01 | 256 | 38 |
| tabell 1 (10 borttag ute) | OMXSB, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.13 | 0.14 till 4.11 | 215 | 38 |
| tabell 1 (10 borttag ute) | OMXSB, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.37 | 1.09 till 3.70 | 471 | 39 |
| tabell 1 (10 borttag ute) | styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3 | 3.67 |  | 507 | 54 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.21 | −2.61 till 3.20 | 19 | 14 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.69 | −3.37 till 7.32 | 17 | 12 |
| som 2 nov (19 flaggade borttag ute) | OMXS30, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 0.44 | −2.01 till 3.82 | 36 | 15 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, addition: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.57 | 1.20 till 4.04 | 256 | 38 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, deletion: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.03 | 0.08 till 3.95 | 206 | 38 |
| som 2 nov (19 flaggade borttag ute) | OMXSB, alla: CAR [AD−1, ED+1], tecken vänt för borttag (%) | 2.33 | 1.03 till 3.67 | 462 | 39 |
| som 2 nov (19 flaggade borttag ute) | styrka för skillnaden OMXS30 minus OMXSB: MDE (procentenheter), gräns 3 | 3.66 |  | 498 | 54 |

Styrkan räcker inte för att testa skillnaden mellan indexen (MDE över gränsen 3 procentenheter). Därför redovisas bara medelvärden.
