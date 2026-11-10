# Steg 11: spread, volym kring ändringen och storleksrang

Flyttat från `code/build/mechanisms_2007.py` (30 okt 2026), metoden oförändrad. Stjärnor från wild cluster bootstrap.

## Jämförelse med körningen 30 oktober

Alla jämförda siffror är desamma (tolerans 0,000001).

## A. Värdeviktad noterad spread, OMXSB-bolagen (G&S figur 9)

| År | Spread, OMXSB (%) | Spread, alla Stockholmsaktier i panelen (%) | Tilläggens CAR (%) | N tillägg |
|---|---|---|---|---|
| 2007 | 0.270 | 0.790 | 7.39 | 2 |
| 2008 | 0.357 | 1.280 | 7.27 | 6 |
| 2009 | 0.303 | 1.497 | 13.87 | 9 |
| 2010 | 0.233 | 1.722 | 13.39 | 5 |
| 2011 | 0.138 | 0.477 | 2.82 | 11 |
| 2012 | 0.129 | 0.424 | −1.70 | 12 |
| 2013 | 0.098 | 0.363 | 8.85 | 8 |
| 2014 | 0.083 | 0.264 | −7.91 | 7 |
| 2015 | 0.093 | 0.238 | 4.19 | 11 |
| 2016 | 0.100 | 0.236 | −1.73 | 16 |
| 2017 | 0.095 | 0.190 | 6.15 | 15 |
| 2018 | 0.079 | 0.191 | 1.16 | 15 |
| 2019 | 0.084 | 0.172 | 4.23 | 10 |
| 2020 | 0.098 | 0.202 | 2.48 | 25 |
| 2021 | 0.076 | 0.168 | 1.16 | 17 |
| 2022 | 0.082 | 0.193 | 0.74 | 29 |
| 2023 | 0.074 | 0.152 | −0.87 | 13 |
| 2024 | 0.072 | 0.149 | 2.34 | 17 |
| 2025 | 0.079 | 0.214 | 1.61 | 17 |
| 2026 | 0.087 | 0.187 | 4.82 | 11 |

| Lutning, CAR på årets spread | Urval | Skattning | 95 % intervall | p | N |
|---|---|---|---|---|---|
| addition | tabell 1 | 39.64*** | 16.35 till 79.54 | 0.007 | 256 |
| deletion | tabell 1 | −26.09* | −52.85 till 4.75 | 0.069 | 215 |
| deletion | gammalt urval | −29.14** | −51.38 till −9.20 | 0.018 | 225 |

## B. Andel av omsättningen ED±22 (G&S avsnitt 2.4.3)

| Typ | Urval | Rad | Skattning | 95 % intervall | N |
|---|---|---|---|---|---|
| addition | tabell 1 | 2007–2011: andel av omsättningen ED±22 som handlas ED−1 (%) | 9.44 | 6.46 till 11.13 | 37 |
| addition | tabell 1 | 2007–2011: andel av omsättningen ED±22 som handlas ED (%) | 4.93 | 2.62 till 7.71 | 37 |
| addition | tabell 1 | 2012–2016: andel av omsättningen ED±22 som handlas ED−1 (%) | 12.59 | 9.54 till 16.88 | 54 |
| addition | tabell 1 | 2012–2016: andel av omsättningen ED±22 som handlas ED (%) | 2.60 | 2.09 till 3.19 | 54 |
| addition | tabell 1 | 2017–2021: andel av omsättningen ED±22 som handlas ED−1 (%) | 12.62 | 10.96 till 14.80 | 83 |
| addition | tabell 1 | 2017–2021: andel av omsättningen ED±22 som handlas ED (%) | 2.38 | 2.04 till 2.66 | 83 |
| addition | tabell 1 | 2022–2026: andel av omsättningen ED±22 som handlas ED−1 (%) | 15.24 | 13.64 till 17.81 | 87 |
| addition | tabell 1 | 2022–2026: andel av omsättningen ED±22 som handlas ED (%) | 2.56 | 2.20 till 2.91 | 87 |
| addition | tabell 1 | andel ED−1: 2022–2026 minus 2007–2011 (procentenheter) | 5.79*** | 3.30 till 8.84 | 261 |
| deletion | tabell 1 | 2007–2011: andel av omsättningen ED±22 som handlas ED−1 (%) | 8.75 | 7.00 till 10.15 | 33 |
| deletion | tabell 1 | 2007–2011: andel av omsättningen ED±22 som handlas ED (%) | 3.46 | 2.21 till 5.39 | 33 |
| deletion | tabell 1 | 2012–2016: andel av omsättningen ED±22 som handlas ED−1 (%) | 10.33 | 7.85 till 12.11 | 46 |
| deletion | tabell 1 | 2012–2016: andel av omsättningen ED±22 som handlas ED (%) | 2.68 | 2.14 till 3.52 | 46 |
| deletion | tabell 1 | 2017–2021: andel av omsättningen ED±22 som handlas ED−1 (%) | 12.58 | 10.13 till 15.22 | 62 |
| deletion | tabell 1 | 2017–2021: andel av omsättningen ED±22 som handlas ED (%) | 2.39 | 2.11 till 2.73 | 62 |
| deletion | tabell 1 | 2022–2026: andel av omsättningen ED±22 som handlas ED−1 (%) | 14.52 | 12.37 till 16.94 | 75 |
| deletion | tabell 1 | 2022–2026: andel av omsättningen ED±22 som handlas ED (%) | 2.67 | 2.24 till 3.07 | 75 |
| deletion | tabell 1 | andel ED−1: 2022–2026 minus 2007–2011 (procentenheter) | 5.76*** | 3.26 till 8.38 | 216 |
| deletion | gammalt urval | 2007–2011: andel av omsättningen ED±22 som handlas ED−1 (%) | 9.01 | 7.26 till 10.78 | 38 |
| deletion | gammalt urval | 2007–2011: andel av omsättningen ED±22 som handlas ED (%) | 3.42 | 2.32 till 5.00 | 38 |
| deletion | gammalt urval | 2012–2016: andel av omsättningen ED±22 som handlas ED−1 (%) | 10.18 | 7.43 till 12.04 | 47 |
| deletion | gammalt urval | 2012–2016: andel av omsättningen ED±22 som handlas ED (%) | 2.69 | 2.16 till 3.50 | 47 |
| deletion | gammalt urval | 2017–2021: andel av omsättningen ED±22 som handlas ED−1 (%) | 12.82 | 10.17 till 15.54 | 64 |
| deletion | gammalt urval | 2017–2021: andel av omsättningen ED±22 som handlas ED (%) | 2.44 | 2.14 till 2.81 | 64 |
| deletion | gammalt urval | 2022–2026: andel av omsättningen ED±22 som handlas ED−1 (%) | 14.44 | 12.52 till 16.56 | 77 |
| deletion | gammalt urval | 2022–2026: andel av omsättningen ED±22 som handlas ED (%) | 2.67 | 2.25 till 3.05 | 77 |
| deletion | gammalt urval | andel ED−1: 2022–2026 minus 2007–2011 (procentenheter) | 5.43*** | 2.97 till 7.88 | 226 |

## C. Tilläggens rang bland icke-medlemmar (G&S figur 8)

| Rad | Skattning | 95 % intervall | p | N |
|---|---|---|---|---|
| 2007–2011: percentil efter omsättning (1 = högst) | 15.8 | 11.0 till 21.3 |  | 45 |
| 2012–2016: percentil efter omsättning (1 = högst) | 9.8 | 6.0 till 15.0 |  | 55 |
| 2017–2021: percentil efter omsättning (1 = högst) | 7.1 | 5.7 till 8.1 |  | 83 |
| 2022–2026: percentil efter omsättning (1 = högst) | 6.5 | 4.6 till 7.9 |  | 87 |
| percentil efter omsättning: 2022–2026 minus 2007–2011 | −9.3*** | −14.7 till −4.6 | 0.001 | 270 |
| percentil efter omsättning: före översynen nov 2023 | 9.5 | 7.8 till 11.2 |  | 219 |
| percentil efter omsättning: från översynen nov 2023 (sex dagars varsel) | 6.5 | 3.3 till 9.1 |  | 51 |
| 2007–2011: percentil efter börsvärde (1 = högst) | 22.6 | 18.8 till 27.5 |  | 43 |
| 2012–2016: percentil efter börsvärde (1 = högst) | 11.9 | 9.2 till 15.0 |  | 55 |
| 2017–2021: percentil efter börsvärde (1 = högst) | 10.1 | 8.0 till 12.3 |  | 82 |
| 2022–2026: percentil efter börsvärde (1 = högst) | 8.6 | 6.3 till 10.4 |  | 86 |
| percentil efter börsvärde: 2022–2026 minus 2007–2011 | −14.0*** | −18.9 till −9.9 | 0.000 | 266 |
| percentil efter börsvärde: före översynen nov 2023 | 12.7 | 10.7 till 15.0 |  | 215 |
| percentil efter börsvärde: från översynen nov 2023 (sex dagars varsel) | 8.9 | 6.5 till 11.1 |  | 51 |
| 2007–2011: rang efter omsättning (1 = högst) | 53.0 | 37.0 till 71.5 |  | 45 |
| 2012–2016: rang efter omsättning (1 = högst) | 35.9 | 23.7 till 52.0 |  | 55 |
| 2017–2021: rang efter omsättning (1 = högst) | 40.6 | 31.2 till 47.8 |  | 83 |
| 2022–2026: rang efter omsättning (1 = högst) | 43.1 | 30.5 till 52.4 |  | 87 |
| rang efter omsättning: 2022–2026 minus 2007–2011 | −9.9 | −29.5 till 8.0 | 0.261 | 270 |
| rang efter omsättning: före översynen nov 2023 | 42.9 | 36.7 till 48.8 |  | 219 |
| rang efter omsättning: från översynen nov 2023 (sex dagars varsel) | 40.9 | 22.8 till 56.9 |  | 51 |
| 2007–2011: rang efter börsvärde (1 = högst) | 60.5 | 49.5 till 72.7 |  | 43 |
| 2012–2016: rang efter börsvärde (1 = högst) | 40.6 | 32.7 till 49.6 |  | 55 |
| 2017–2021: rang efter börsvärde (1 = högst) | 56.1 | 43.2 till 68.3 |  | 82 |
| 2022–2026: rang efter börsvärde (1 = högst) | 54.2 | 40.6 till 65.7 |  | 86 |
| rang efter börsvärde: 2022–2026 minus 2007–2011 | −6.3 | −22.2 till 8.9 | 0.401 | 266 |
| rang efter börsvärde: före översynen nov 2023 | 52.9 | 45.9 till 59.7 |  | 215 |
| rang efter börsvärde: från översynen nov 2023 (sex dagars varsel) | 53.4 | 40.4 till 66.0 |  | 51 |

9 av 568 rangtal skiljer sig från körningen 30 oktober, alla med en plats. Orsaken är lika värden: två aktieslag i samma bolag har samma börsvärde i LSEG, och då ordnade sorteringen dem godtyckligt. Här ordnas lika värden efter RIC.

14 av 284 tillägg saknar rang efter omsättning (aktien handlades under hälften av dagarna i fönstret eller saknas i panelen).
