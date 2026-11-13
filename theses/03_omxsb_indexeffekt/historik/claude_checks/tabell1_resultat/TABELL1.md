# Tabell 1, rättad: stjärnor från wild cluster bootstrap per översyn

CAR i procent mot OMXSBGI, totalavkastning, 95 % intervall klustrat per översyn (t med G−1). Stjärnor: * p<0,10, ** p<0,05, *** p<0,01 från restriktiv wild cluster bootstrap (Rademacher om G≥12, annars Webb; 9 999 dragningar). Källa: tabell1.py, CAR från common.py som återskapar Luddes tot exakt.

## Panel A: Tillägg

| Fönster | 2007–2011 | 2012–2016 | 2017–2021 | 2022–2026 |
|---|---|---|---|---|
| Besked [AD−1, AD+1] | 0.96 (-0.98 till 2.90) | 1.87** (0.09 till 3.65) | -0.16 (-2.90 till 2.59) | 1.20 (-0.42 till 2.83) |
| Ändring [ED−1, ED+1] | 1.16 (-1.69 till 4.01) | -0.73 (-2.86 till 1.40) | 0.38 (-1.23 till 1.98) | -0.09 (-1.31 till 1.13) |
| Totalt [AD−1, ED+1] | 8.52** (2.92 till 14.12) | 0.25 (-3.87 till 4.36) | 2.85*** (1.00 till 4.70) | 1.50* (-0.20 till 3.20) |
| Händelser | 33 | 54 | 82 | 87 |
| Översyner | 9 | 10 | 10 | 9 |
| p, klustrat | 0.008 | 0.894 | 0.007 | 0.076 |
| p, wild bootstrap | 0.027 | 0.908 | 0.005 | 0.062 |

## Panel B: Borttag

| Fönster | 2007–2011 | 2012–2016 | 2017–2021 | 2022–2026 |
|---|---|---|---|---|
| Besked [AD−1, AD+1] | 0.02 (-3.12 till 3.16) | -1.69** (-2.78 till -0.61) | -1.97** (-3.35 till -0.59) | -0.65 (-2.19 till 0.89) |
| Ändring [ED−1, ED+1] | -0.17 (-3.76 till 3.42) | -0.79 (-3.67 till 2.10) | 0.86 (-0.40 till 2.12) | -1.26 (-2.84 till 0.31) |
| Totalt [AD−1, ED+1] | -6.69*** (-10.60 till -2.79) | -2.45 (-10.18 till 5.29) | -0.57 (-3.77 till 2.63) | -1.52 (-4.09 till 1.05) |
| Händelser | 38 | 47 | 63 | 77 |
| Översyner | 9 | 10 | 10 | 9 |
| p, klustrat | 0.004 | 0.493 | 0.698 | 0.210 |
| p, wild bootstrap | 0.003 | 0.518 | 0.698 | 0.268 |

## Panel C: sammanslagna perioder, totalt fönster

| Typ | Urval | Händelser | Översyner | Effekt | p, wild bootstrap |
|---|---|---|---|---|---|
| addition | 2007–16 | 87 | 19 | 3.39* (-0.30 till 7.08) | 0.066 |
| addition | 2017–26 | 169 | 19 | 2.15*** (1.00 till 3.30) | 0.001 |
| addition | 2010–20 (G&S kalenderår) | 135 | 21 | 2.41** (0.26 till 4.56) | 0.028 |
| addition | 2011–20 | 130 | 20 | 1.99* (-0.04 till 4.02) | 0.054 |
| addition | efter brottet juni 2010 | 234 | 31 | 1.75*** (0.52 till 2.97) | 0.007 |
| addition | 2007 till juni 2010 | 22 | 7 | 11.37** (5.86 till 16.88) | 0.014 |
| deletion | 2007–16 | 85 | 19 | -4.34 (-9.20 till 0.51) | 0.105 |
| deletion | 2017–26 | 140 | 19 | -1.09 (-2.90 till 0.71) | 0.241 |
| deletion | 2010–20 (G&S kalenderår) | 111 | 22 | -1.40 (-4.49 till 1.70) | 0.376 |
| deletion | 2011–20 | 104 | 20 | -1.07 (-4.21 till 2.06) | 0.503 |
| deletion | efter brottet juni 2010 | 201 | 32 | -1.46 (-3.34 till 0.42) | 0.138 |
| deletion | 2007 till juni 2010 | 24 | 6 | -9.55** (-14.98 till -4.11) | 0.011 |

G&S, USA: tillägg 1990-talet 7,4 %; tillägg 2010-talet under 1 %, inte skild från noll; borttag 2010–2020 −0,6 %.

## Panel D: har effekten minskat? Totalt fönster

| Typ | Test | Skattning | Intervall | p, klustrat | p, wild bootstrap | Översyner |
|---|---|---|---|---|---|---|
| addition | 2022–26 minus 2007–11 | -7.03 | -11.97 till -2.08 | 0.007 | 0.029 | 38 |
| addition | 2022–26 minus 2017–21 | -1.35 | -3.50 till 0.80 | 0.212 | 0.250 | 38 |
| addition | 2017–26 minus 2007–16 (decennier) | -1.24 | -4.92 till 2.45 | 0.501 | 0.502 | 38 |
| addition | trend per år (ingen periodindelning) | -0.28 | -0.60 till 0.05 | 0.091 | 0.117 | 38 |
| addition | efter minus före brottet juni 2010 (brottet från Luddes T4, inte sökt här) | -9.63 | -14.09 till -5.17 | 0.000 | 0.006 | 38 |
| addition | F-test lika medel i fyra perioder | 3.40 |  | 0.028 |  | 38 |
| deletion | 2022–26 minus 2007–11 | 5.17 | 1.23 till 9.12 | 0.012 | 0.015 | 38 |
| deletion | 2022–26 minus 2017–21 | -0.95 | -4.47 till 2.57 | 0.587 | 0.616 | 38 |
| deletion | 2017–26 minus 2007–16 (decennier) | 3.25 | -1.69 till 8.20 | 0.190 | 0.260 | 38 |
| deletion | trend per år (ingen periodindelning) | 0.23 | -0.15 till 0.61 | 0.230 | 0.279 | 38 |
| deletion | efter minus före brottet juni 2010 (brottet från Luddes T4, inte sökt här) | 8.09 | 3.70 till 12.48 | 0.001 | 0.008 | 38 |
| deletion | F-test lika medel i fyra perioder | 3.14 |  | 0.037 |  | 38 |

## Panel E: tillägg från varje startår till 2026, totalt fönster

| Från | Händelser | Översyner | Effekt | p, wild bootstrap |
|---|---|---|---|---|
| från 2008 | 254 | 37 | 2.53*** (1.12 till 3.95) | 0.000 |
| från 2009 | 248 | 35 | 2.42*** (1.00 till 3.84) | 0.000 |
| från 2010 | 239 | 32 | 1.99*** (0.69 till 3.29) | 0.003 |
| från 2011 | 234 | 31 | 1.75*** (0.52 till 2.97) | 0.006 |
| från 2012 | 223 | 29 | 1.69*** (0.46 till 2.92) | 0.008 |
| från 2013 | 211 | 27 | 1.88*** (0.61 till 3.16) | 0.003 |
| från 2014 | 203 | 25 | 1.61*** (0.40 till 2.82) | 0.009 |
| från 2015 | 196 | 23 | 1.95*** (0.83 till 3.07) | 0.002 |
| från 2016 | 185 | 21 | 1.82*** (0.68 till 2.95) | 0.003 |
| från 2017 | 169 | 19 | 2.15*** (1.00 till 3.30) | 0.001 |
| från 2018 | 154 | 17 | 1.76*** (0.73 till 2.79) | 0.003 |
| från 2019 | 139 | 15 | 1.83*** (0.74 till 2.92) | 0.003 |
| från 2020 | 129 | 13 | 1.64*** (0.50 till 2.79) | 0.010 |
| från 2021 | 104 | 11 | 1.44** (0.07 till 2.81) | 0.035 |
| från 2022 | 87 | 9 | 1.50* (-0.20 till 3.20) | 0.069 |
| från 2023 | 58 | 7 | 1.88* (-0.17 till 3.92) | 0.068 |
