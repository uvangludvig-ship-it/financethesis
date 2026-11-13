# Steg 15: återgång efter ändringen

Port av `del1.py` med `lin()`. Medel i procent; borttag med eget tecken.

## Jämförelse med del1.py (tillägg och alla borttag)

Alla jämförda siffror är desamma (händelsemedel, medel per översyn, N och kluster).

## Resultat

| Typ | Urval | Period | Mått | Medel | 95 % intervall | p | N | Översyner |
|---|---|---|---|---|---|---|---|---|
| addition | alla | all | CAR [ED, ED+10] | −1.42** | −2.68 till −0.21 | 0.019 | 260 | 38 |
| addition | alla | all | CAR [ED, ED+20] | −0.65 | −2.23 till 0.90 | 0.429 | 257 | 38 |
| addition | alla | all | Uppgång [AD, ED−1] | 3.64*** | 2.16 till 5.14 | 0.000 | 257 | 38 |
| addition | alla | 2007–2011 | CAR [ED, ED+10] | −5.33*** | −8.29 till −2.91 | 0.002 | 37 | 9 |
| addition | alla | 2007–2011 | CAR [ED, ED+20] | −6.51*** | −11.62 till −2.86 | 0.003 | 34 | 9 |
| addition | alla | 2007–2011 | Uppgång [AD, ED−1] | 11.03*** | 5.18 till 17.08 | 0.004 | 34 | 9 |
| addition | alla | 2012–2016 | CAR [ED, ED+10] | −3.52*** | −7.07 till −1.44 | 0.007 | 54 | 10 |
| addition | alla | 2012–2016 | CAR [ED, ED+20] | −1.71 | −5.03 till 0.86 | 0.195 | 54 | 10 |
| addition | alla | 2012–2016 | Uppgång [AD, ED−1] | 1.00 | −2.18 till 5.18 | 0.503 | 54 | 10 |
| addition | alla | 2017–2021 | CAR [ED, ED+10] | −0.44 | −1.79 till 0.79 | 0.464 | 82 | 10 |
| addition | alla | 2017–2021 | CAR [ED, ED+20] | 1.85 | −1.16 till 4.93 | 0.303 | 82 | 10 |
| addition | alla | 2017–2021 | Uppgång [AD, ED−1] | 4.29*** | 1.78 till 6.15 | 0.003 | 82 | 10 |
| addition | alla | 2022–2026 | CAR [ED, ED+10] | 0.63 | −1.69 till 2.85 | 0.538 | 87 | 9 |
| addition | alla | 2022–2026 | CAR [ED, ED+20] | −0.06 | −1.27 till 1.09 | 0.913 | 87 | 9 |
| addition | alla | 2022–2026 | Uppgång [AD, ED−1] | 1.78** | 0.57 till 3.06 | 0.012 | 87 | 9 |
| deletion | utan de 10 (G&S regel) | all | CAR [ED, ED+10] | −0.65 | −2.55 till 1.32 | 0.490 | 216 | 38 |
| deletion | utan de 10 (G&S regel) | all | CAR [ED, ED+20] | 0.12 | −1.81 till 2.20 | 0.904 | 215 | 38 |
| deletion | utan de 10 (G&S regel) | all | Uppgång [AD, ED−1] | −2.28** | −4.14 till −0.50 | 0.013 | 215 | 38 |
| deletion | utan de 10 (G&S regel) | 2007–2011 | CAR [ED, ED+10] | 4.11 | −3.11 till 11.89 | 0.267 | 33 | 9 |
| deletion | utan de 10 (G&S regel) | 2007–2011 | CAR [ED, ED+20] | 5.31* | −1.21 till 11.26 | 0.091 | 33 | 9 |
| deletion | utan de 10 (G&S regel) | 2007–2011 | Uppgång [AD, ED−1] | −8.63*** | −15.79 till −3.49 | 0.002 | 33 | 9 |
| deletion | utan de 10 (G&S regel) | 2012–2016 | CAR [ED, ED+10] | −2.02 | −8.10 till 2.14 | 0.374 | 46 | 10 |
| deletion | utan de 10 (G&S regel) | 2012–2016 | CAR [ED, ED+20] | −2.01 | −3.99 till 2.68 | 0.352 | 45 | 10 |
| deletion | utan de 10 (G&S regel) | 2012–2016 | Uppgång [AD, ED−1] | −2.15 | −12.04 till 2.98 | 0.525 | 46 | 10 |
| deletion | utan de 10 (G&S regel) | 2017–2021 | CAR [ED, ED+10] | −1.09 | −4.80 till 2.35 | 0.620 | 62 | 10 |
| deletion | utan de 10 (G&S regel) | 2017–2021 | CAR [ED, ED+20] | 0.19 | −3.58 till 3.87 | 0.896 | 62 | 10 |
| deletion | utan de 10 (G&S regel) | 2017–2021 | Uppgång [AD, ED−1] | −0.30 | −2.52 till 2.48 | 0.793 | 61 | 10 |
| deletion | utan de 10 (G&S regel) | 2022–2026 | CAR [ED, ED+10] | −1.55 | −4.95 till 1.57 | 0.370 | 75 | 9 |
| deletion | utan de 10 (G&S regel) | 2022–2026 | CAR [ED, ED+20] | −0.95 | −4.06 till 2.18 | 0.517 | 75 | 9 |
| deletion | utan de 10 (G&S regel) | 2022–2026 | Uppgång [AD, ED−1] | −1.17* | −2.72 till 0.08 | 0.073 | 75 | 9 |
| deletion | alla | all | CAR [ED, ED+10] | −0.62 | −2.53 till 1.38 | 0.512 | 226 | 38 |
| deletion | alla | all | CAR [ED, ED+20] | 0.13 | −1.78 till 2.16 | 0.893 | 225 | 38 |
| deletion | alla | all | Uppgång [AD, ED−1] | −2.54*** | −4.45 till −0.68 | 0.008 | 225 | 38 |
| deletion | alla | 2007–2011 | CAR [ED, ED+10] | 4.05 | −2.09 till 10.73 | 0.203 | 38 | 9 |
| deletion | alla | 2007–2011 | CAR [ED, ED+20] | 4.85* | −0.40 till 9.41 | 0.066 | 38 | 9 |
| deletion | alla | 2007–2011 | Uppgång [AD, ED−1] | −9.35*** | −15.23 till −4.54 | 0.002 | 38 | 9 |
| deletion | alla | 2012–2016 | CAR [ED, ED+10] | −1.95 | −7.68 till 1.94 | 0.387 | 47 | 10 |
| deletion | alla | 2012–2016 | CAR [ED, ED+20] | −1.87 | −3.97 till 2.65 | 0.400 | 46 | 10 |
| deletion | alla | 2012–2016 | Uppgång [AD, ED−1] | −2.20 | −11.07 till 2.89 | 0.503 | 47 | 10 |
| deletion | alla | 2017–2021 | CAR [ED, ED+10] | −1.34 | −5.41 till 2.27 | 0.610 | 64 | 10 |
| deletion | alla | 2017–2021 | CAR [ED, ED+20] | −0.01 | −4.08 till 3.93 | 0.995 | 64 | 10 |
| deletion | alla | 2017–2021 | Uppgång [AD, ED−1] | −0.38 | −2.54 till 2.29 | 0.730 | 63 | 10 |
| deletion | alla | 2022–2026 | CAR [ED, ED+10] | −1.53 | −4.87 till 1.60 | 0.371 | 77 | 9 |
| deletion | alla | 2022–2026 | CAR [ED, ED+20] | −0.89 | −3.96 till 2.23 | 0.530 | 77 | 9 |
| deletion | alla | 2022–2026 | Uppgång [AD, ED−1] | −1.17 | −2.74 till 0.23 | 0.135 | 77 | 9 |

## Återgångsandel över 20 dagar (−CAR [ED, ED+20] / uppgång [AD, ED−1])

- addition, alla: 17 % (N 255)
- deletion, utan de 10 (G&S regel): 7 % (N 214)
- deletion, alla: 7 % (N 224)
