# Tabell 1, rättad: intervall och stjärnor från wild cluster bootstrap per översyn

CAR i procent mot OMXSBGI, totalavkastning. **BOOTSTRAP:** 95 % intervall i parentes = alla värden som restriktiv wild cluster bootstrap per översyn inte förkastar på 5 % (testinversion). Stjärnor: * p<0,10, ** p<0,05, *** p<0,01 från samma bootstrap och samma dragningar (Rademacher om G≥12, annars Webb; 9 999 dragningar), så intervall och stjärnor stämmer alltid överens. **ANALYTISKT (jämförelse):** raderna märkta klustrat = CR1-standardfel per översyn, t med G−1. Källa: 01_effect_table.py, CAR från returns.py som återskapar replikeringens tot exakt.

## Panel A: Tillägg

| Fönster | 2007–2011 | 2012–2016 | 2017–2021 | 2022–2026 |
|---|---|---|---|---|
| Besked [AD−1, AD+1] | 0.96 (-0.82 till 2.98) | 1.87** (0.07 till 3.93) | -0.16 (-3.05 till 1.88) | 1.20 (-0.39 till 2.68) |
| Ändring [ED−1, ED+1] | 1.16 (-1.74 till 4.00) | -0.73 (-2.96 till 1.70) | 0.38 (-1.45 till 1.84) | -0.09 (-1.17 till 1.25) |
| Totalt [AD−1, ED+1] | 8.52** (2.46 till 14.74) | 0.25 (-3.73 till 5.30) | 2.85*** (1.26 till 5.20) | 1.50* (-0.10 till 3.22) |
| Händelser | 33 | 54 | 82 | 87 |
| Översyner | 9 | 10 | 10 | 9 |
| Intervall totalt, klustrat (analytiskt) | 2.92 till 14.12 | -3.87 till 4.36 | 1.00 till 4.70 | -0.20 till 3.20 |
| p totalt, klustrat (analytiskt) | 0.008 | 0.894 | 0.007 | 0.076 |
| p totalt, wild bootstrap | 0.027 | 0.908 | 0.005 | 0.062 |

## Panel B: Borttag

| Fönster | 2007–2011 | 2012–2016 | 2017–2021 | 2022–2026 |
|---|---|---|---|---|
| Besked [AD−1, AD+1] | -0.77 (-3.65 till 1.84) | -1.71** (-3.24 till -0.86) | -2.09** (-3.66 till -0.58) | -0.71 (-2.27 till 0.94) |
| Ändring [ED−1, ED+1] | -0.09 (-4.72 till 3.65) | -0.85 (-6.55 till 0.86) | 0.89 (-0.26 till 2.22) | -1.23 (-2.90 till 0.40) |
| Totalt [AD−1, ED+1] | -6.16*** (-11.41 till -2.10) | -2.47 (-14.42 till 3.60) | -0.43 (-3.43 till 3.02) | -1.53 (-4.24 till 0.89) |
| Händelser | 33 | 46 | 61 | 75 |
| Översyner | 9 | 10 | 10 | 9 |
| Intervall totalt, klustrat (analytiskt) | -10.46 till -1.85 | -10.40 till 5.46 | -3.63 till 2.77 | -4.12 till 1.05 |
| p totalt, klustrat (analytiskt) | 0.011 | 0.499 | 0.768 | 0.209 |
| p totalt, wild bootstrap | 0.007 | 0.522 | 0.759 | 0.279 |

## Panel C: sammanslagna perioder, totalt fönster

| Typ | Urval | Händelser | Översyner | Effekt (bootstrapintervall) | Intervall, klustrat (analytiskt) | p, wild bootstrap |
|---|---|---|---|---|---|---|
| addition | 2007–16 | 87 | 19 | 3.39* (-0.25 till 7.53) | -0.30 till 7.08 | 0.066 |
| addition | 2017–26 | 169 | 19 | 2.15*** (1.01 till 3.39) | 1.00 till 3.30 | 0.001 |
| addition | 2010–20 (G&S kalenderår) | 135 | 21 | 2.41** (0.31 till 4.65) | 0.26 till 4.56 | 0.028 |
| addition | 2011–20 | 130 | 20 | 1.99* (-0.06 till 4.09) | -0.04 till 4.02 | 0.054 |
| addition | efter brottet juni 2010 | 234 | 31 | 1.75*** (0.55 till 2.98) | 0.52 till 2.97 | 0.007 |
| addition | 2007 till juni 2010 | 22 | 7 | 11.37** (6.04 till 17.89) | 5.86 till 16.88 | 0.014 |
| deletion | 2007–16 | 79 | 19 | -4.01 (-9.48 till 1.32) | -9.07 till 1.06 | 0.155 |
| deletion | 2017–26 | 136 | 19 | -1.04 (-2.88 till 0.90) | -2.86 till 0.78 | 0.267 |
| deletion | 2010–20 (G&S kalenderår) | 108 | 22 | -1.35 (-4.87 till 1.79) | -4.51 till 1.81 | 0.402 |
| deletion | 2011–20 | 102 | 20 | -1.04 (-4.72 till 2.14) | -4.23 till 2.15 | 0.520 |
| deletion | efter brottet juni 2010 | 196 | 32 | -1.43 (-3.45 till 0.57) | -3.34 till 0.48 | 0.152 |
| deletion | 2007 till juni 2010 | 19 | 6 | -9.36** (-18.42 till -4.64) | -16.00 till -2.72 | 0.029 |

G&S, USA: tillägg 1990-talet 7,4 %; tillägg 2010-talet under 1 %, inte skild från noll; borttag 2010–2020 −0,6 %.

## Panel D: har effekten minskat? Totalt fönster

| Typ | Test | Skattning | Intervall, bootstrap | Intervall, klustrat (analytiskt) | p, klustrat (analytiskt) | p, wild bootstrap | Översyner |
|---|---|---|---|---|---|---|---|
| addition | 2022–26 minus 2007–11 | -7.03 | -13.10 till -1.10 | -11.97 till -2.08 | 0.007 | 0.029 | 38 |
| addition | 2022–26 minus 2017–21 | -1.35 | -3.88 till 0.98 | -3.50 till 0.80 | 0.212 | 0.250 | 38 |
| addition | 2017–26 minus 2007–16 (decennier) | -1.24 | -5.26 till 2.54 | -4.92 till 2.45 | 0.501 | 0.502 | 38 |
| addition | trend per år (ingen periodindelning) | -0.28 | -0.64 till 0.08 | -0.60 till 0.05 | 0.091 | 0.117 | 38 |
| addition | efter minus före brottet juni 2010 (brottet från Luddes T4, inte sökt här) | -9.63 | -16.32 till -4.40 | -14.09 till -5.17 | 0.000 | 0.006 | 38 |
| addition | F-test lika medel i fyra perioder | 3.40 |  |  | 0.028 |  | 38 |
| deletion | 2022–26 minus 2007–11 | 4.62 | 0.25 till 9.81 | 0.38 till 8.87 | 0.034 | 0.039 | 38 |
| deletion | 2022–26 minus 2017–21 | -1.10 | -5.11 till 2.70 | -4.63 till 2.43 | 0.530 | 0.564 | 38 |
| deletion | 2017–26 minus 2007–16 (decennier) | 2.97 | -2.94 till 8.60 | -2.16 till 8.10 | 0.248 | 0.328 | 38 |
| deletion | trend per år (ingen periodindelning) | 0.19 | -0.29 till 0.64 | -0.21 till 0.59 | 0.344 | 0.400 | 38 |
| deletion | efter minus före brottet juni 2010 (brottet från Luddes T4, inte sökt här) | 7.93 | 2.51 till 17.54 | 2.72 till 13.14 | 0.004 | 0.020 | 38 |
| deletion | F-test lika medel i fyra perioder | 2.29 |  |  | 0.094 |  | 38 |

## Panel E: tillägg från varje startår till 2026, totalt fönster

| Från | Händelser | Översyner | Effekt (bootstrapintervall) | p, wild bootstrap |
|---|---|---|---|---|
| från 2008 | 254 | 37 | 2.53*** (1.14 till 3.99) | 0.000 |
| från 2009 | 248 | 35 | 2.42*** (1.04 till 3.87) | 0.000 |
| från 2010 | 239 | 32 | 1.99*** (0.72 till 3.31) | 0.003 |
| från 2011 | 234 | 31 | 1.75*** (0.53 till 2.97) | 0.006 |
| från 2012 | 223 | 29 | 1.69*** (0.48 till 2.94) | 0.008 |
| från 2013 | 211 | 27 | 1.88*** (0.63 till 3.20) | 0.003 |
| från 2014 | 203 | 25 | 1.61*** (0.40 till 2.85) | 0.009 |
| från 2015 | 196 | 23 | 1.95*** (0.87 till 3.13) | 0.002 |
| från 2016 | 185 | 21 | 1.82*** (0.69 till 3.02) | 0.003 |
| från 2017 | 169 | 19 | 2.15*** (1.02 till 3.39) | 0.001 |
| från 2018 | 154 | 17 | 1.76*** (0.72 till 2.86) | 0.003 |
| från 2019 | 139 | 15 | 1.83*** (0.75 till 3.03) | 0.003 |
| från 2020 | 129 | 13 | 1.64*** (0.49 till 2.85) | 0.010 |
| från 2021 | 104 | 11 | 1.44** (0.12 till 2.87) | 0.035 |
| från 2022 | 87 | 9 | 1.50* (-0.11 till 3.23) | 0.069 |
| från 2023 | 58 | 7 | 1.88* (-0.20 till 3.77) | 0.068 |

F-testet i panel D (lika medel i fyra perioder) är analytiskt: Wald med CR1, p från F(3, G−1), ingen bootstrap.
