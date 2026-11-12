# Siffror som ändras: fondlistan efter G&S regel och huvudmåttet C (11 november 2026)

Jämförelse cell för cell mellan results/tables/all_tables.docx före (commit 98ff7e0) och efter. Alla p-värden och intervall är
omräknade (run_all.py, 0 FEL). Tabellerna 1–4, 9, 11–13, A4 och CAR-delarna av tabell 10 och A5 är oförändrade: bytet rör bara
fondmåtten. Uppsatstexten ligger inte i repot, så siffror i löptexten måste stämmas av mot listan nedan.

## Huvudsiffror

| | Före (D_V) | Efter (D_C) |
|---|---|---|
| M tillägg 2017–21 | 3.29 [1.00, 6.87] | 2.97 [0.95, 6.20] |
| M tillägg 2022–26 | 2.94 [0.80, 5.37] | 2.35 [0.60, 4.32] |
| M tillägg 2017–26 | 3.11 [1.44, 5.14] | 2.63 [1.24, 4.31] |
| M borttag 2017–26 | 1.21 [−1.00, 2.80] | 1.01 [−0.79, 2.35] |
| D̄ tillägg 2017–26 (% av aktierna) | 0.87 | 1.03 |
| D̄ borttag 2017–26 | −0.92 | −1.11 |
| M tillägg 2017–26 utan MSCI-överlapp | 2.28 [0.98, 3.97] | 1.92 [0.83, 3.37] |
| M tillägg 2017–26 utan egen bolagsnyhet | 2.27 [1.03, 3.83] | 1.92 [0.87, 3.26] |
| p, M 2007–11 − M 2022–26 (tillägg) | 0.114 | 0.138 |
| Aktiva fonder, tillägg 2017–26 | −0.16 [−0.47, 0.16] | −0.24 [−0.52, 0.05], p 0.103 |
| Alla fonder, tillägg 2017–26 | 1.19 [0.76, 1.63] | 1.19 [0.75, 1.62] |
| Ägarandel december 2025 (%) | 1.14 (V) | 1.63 (C) |
| Förmögenhet 2025-12, mdkr | V 152.85 (C fanns, men ej huvudmått) | C 219.16 |
| MDE, M 2017–21 minus M 2022–26 | 5.75 | 4.94 |
| Korrelation LSEG-D mot FI | 0.809 (D_V) | 0.842 (D_C) |
| Fond-händelser uteslutna för gruppbyte | 93 | 222 (+129: LF Sparmål, sex fonder, blir C 2025-06-16) |

Tabell 5 har en ny panel C (M med B och V), och tabell 7 visar C med B, varianter och blandfonder som delrader.
Figur 1 och 3 ritar nu D_C; figur 4 har samma tre linjer, men C är huvudmåttet.

## Tabell 8: splitjusterat aktieantal (declarations/issuance_split_declaration.md, med tillägget samma kväll)

| Tillägg minus nästan tillagda | Före (rådata) | Efter (split = faktorn förklarar aktieändringen inom 10 %) |
|---|---|---|
| Ändring i aktieantal (pp) | 0.50 [−1.63, 2.76], p 0.70 | 0.57 [−0.47, 1.65], p 0.28 |
| Andel med ökning > 1 %, skillnad (pp) | – | 5.77** [0.27, 11.24], p 0.042 |
| Andel med ökning > 5 %, skillnad (pp) | – | 3.67* [−0.51, 8.19], p 0.091 |
| Känslighet: gränsen 1,4 utan matchning | – | 1.01* [−0.04, 2.09], p 0.059 |

Periodcellerna (medel %, rådata → splitjusterat): 2007–11 tillägg: 0.69 → 0.69; 2007–11 nästan tillagda: 1.26 → 1.55; 2012–16 tillägg: 2.92 → 2.92; 2012–16 nästan tillagda: 2.14 → 0.34; 2017–21 tillägg: 3.29 → 2.40; 2017–21 nästan tillagda: 3.60 → 1.74; 2022–26 tillägg: 3.03 → 0.43; 2022–26 nästan tillagda: 1.49 → 0.74.
Med full justering (alla rader) blir skillnaden 0.99 (p 0.044), som i den utforskande körningen. NCAB 2021H2 och Cherry 2017H1
räknas med rådata (faktorn förklarar inte aktieändringen inom 10 %) och bör kontrolleras mot pressmeddelanden.

## Känslighetskörningen (INKL)

Efter ändringarna har fondlistan inga obelagda följare (loggen: "obelagda som INTE ingår: 0"), så INKL ger samma siffror som
huvudkörningen. Den används inte i någon tabell, figur eller annan kod i thesis_final: run_all.py kör bara huvudkörningen, och
argumentet inkl_obelagda finns bara i 02_fund_demand.py. Om uppsatstexten nämner en känslighetskörning med obelagda fonder
(t.ex. Nordea Generationsfond, Stiftelsefonden, Sparmål, Öhman 2009–2011) ska den meningen strykas eller skrivas om: de fonderna
ingår nu i huvudmåttet.

## Alla ändrade celler

- Tabell 5, Baseline window [AD−1, ED+1] | 2007–11, kol. 3 (D̄): 0.10 → 0.15
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–11, kol. 4 (M): 84.97 → 57.87
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–11, kol. 7 (D̄): −0.20 → −0.26
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–11, kol. 8 (M): −0.93 → −0.72
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–11 (intervall), kol. 4 (M): [13.05, 196.38] → [7.06, 166.30]
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–11 (intervall), kol. 8 (M): [−58.86, 31.41] → [−58.86, 15.72]
- Tabell 5, Baseline window [AD−1, ED+1] | 2012–16, kol. 3 (D̄): 0.42 → 0.52
- Tabell 5, Baseline window [AD−1, ED+1] | 2012–16, kol. 4 (M): −4.67 → −3.76
- Tabell 5, Baseline window [AD−1, ED+1] | 2012–16, kol. 7 (D̄): −0.33 → −0.48
- Tabell 5, Baseline window [AD−1, ED+1] | 2012–16, kol. 8 (M): 6.28 → 4.36
- Tabell 5, Baseline window [AD−1, ED+1] | 2012–16 (intervall), kol. 4 (M): [−19.22, 2.20] → [−15.89, 1.65]
- Tabell 5, Baseline window [AD−1, ED+1] | 2012–16 (intervall), kol. 8 (M): [−9.76, 37.14] → [−5.32, 31.71]
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–21, kol. 3 (D̄): 1.00 → 1.11
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–21, kol. 4 (M): 3.29 → 2.97
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–21, kol. 7 (D̄): −0.91 → −0.99
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–21, kol. 8 (M): 0.22 → 0.20
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–21 (intervall), kol. 4 (M): [1.00, 6.87] → [0.95, 6.20]
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–21 (intervall), kol. 8 (M): [−4.52, 3.49] → [−4.10, 3.26]
- Tabell 5, Baseline window [AD−1, ED+1] | 2022–26, kol. 3 (D̄): 0.78 → 0.97
- Tabell 5, Baseline window [AD−1, ED+1] | 2022–26, kol. 4 (M): 2.94 → 2.35
- Tabell 5, Baseline window [AD−1, ED+1] | 2022–26, kol. 7 (D̄): −0.93 → −1.18
- Tabell 5, Baseline window [AD−1, ED+1] | 2022–26, kol. 8 (M): 1.78 → 1.41
- Tabell 5, Baseline window [AD−1, ED+1] | 2022–26 (intervall), kol. 4 (M): [0.80, 5.37] → [0.60, 4.32]
- Tabell 5, Baseline window [AD−1, ED+1] | 2022–26 (intervall), kol. 8 (M): [0.00, 3.18] → [0.00, 2.54]
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–16, kol. 3 (D̄): 0.34 → 0.43
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–16, kol. 4 (M): 1.49 → 1.18
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–16, kol. 7 (D̄): −0.30 → −0.43
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–16, kol. 8 (M): 5.23 → 3.68
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–16 (intervall), kol. 4 (M): [−9.99, 17.50] → [−7.54, 13.46]
- Tabell 5, Baseline window [AD−1, ED+1] | 2007–16 (intervall), kol. 8 (M): [−9.27, 28.01] → [−5.32, 23.42]
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–26, kol. 3 (D̄): 0.87 → 1.03
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–26, kol. 4 (M): 3.11 → 2.63
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–26, kol. 7 (D̄): −0.92 → −1.11
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–26, kol. 8 (M): 1.21 → 1.01
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–26 (intervall), kol. 4 (M): [1.44, 5.14] → [1.24, 4.31]
- Tabell 5, Baseline window [AD−1, ED+1] | 2017–26 (intervall), kol. 8 (M): [−1.00, 2.80] → [−0.79, 2.35]
- Tabell 5, Extended window [AD−20, ED+1] | 2007–11, kol. 3 (D̄): 0.10 → 0.15
- Tabell 5, Extended window [AD−20, ED+1] | 2007–11, kol. 4 (M): 89.32 → 60.83
- Tabell 5, Extended window [AD−20, ED+1] | 2007–11, kol. 7 (D̄): −0.20 → −0.26
- Tabell 5, Extended window [AD−20, ED+1] | 2007–11, kol. 8 (M): 16.75 → 12.98
- Tabell 5, Extended window [AD−20, ED+1] | 2007–11 (intervall), kol. 4 (M): [60.57, 157.61] → [46.61, 113.31]
- Tabell 5, Extended window [AD−20, ED+1] | 2007–11 (intervall), kol. 8 (M): [−46.06, 100.06] → [−46.06, 50.08]
- Tabell 5, Extended window [AD−20, ED+1] | 2012–16, kol. 3 (D̄): 0.42 → 0.52
- Tabell 5, Extended window [AD−20, ED+1] | 2012–16, kol. 4 (M): −2.26 → −1.82
- Tabell 5, Extended window [AD−20, ED+1] | 2012–16, kol. 7 (D̄): −0.33 → −0.48
- Tabell 5, Extended window [AD−20, ED+1] | 2012–16, kol. 8 (M): 12.22 → 8.49
- Tabell 5, Extended window [AD−20, ED+1] | 2012–16 (intervall), kol. 4 (M): [−26.51, 14.25] → [−20.78, 10.16]
- Tabell 5, Extended window [AD−20, ED+1] | 2012–16 (intervall), kol. 8 (M): [−10.35, 55.79] → [−8.15, 41.13]
- Tabell 5, Extended window [AD−20, ED+1] | 2017–21, kol. 3 (D̄): 1.00 → 1.11
- Tabell 5, Extended window [AD−20, ED+1] | 2017–21, kol. 4 (M): 4.69 → 4.24
- Tabell 5, Extended window [AD−20, ED+1] | 2017–21, kol. 7 (D̄): −0.91 → −0.99
- Tabell 5, Extended window [AD−20, ED+1] | 2017–21, kol. 8 (M): −0.62 → −0.57
- Tabell 5, Extended window [AD−20, ED+1] | 2017–21 (intervall), kol. 4 (M): [1.39, 9.11] → [1.22, 8.30]
- Tabell 5, Extended window [AD−20, ED+1] | 2017–21 (intervall), kol. 8 (M): [−6.34, 6.16] → [−5.94, 5.70]
- Tabell 5, Extended window [AD−20, ED+1] | 2022–26, kol. 3 (D̄): 0.79 → 0.99
- Tabell 5, Extended window [AD−20, ED+1] | 2022–26, kol. 4 (M): 8.34 → 6.66
- Tabell 5, Extended window [AD−20, ED+1] | 2022–26, kol. 7 (D̄): −0.94 → −1.19
- Tabell 5, Extended window [AD−20, ED+1] | 2022–26, kol. 8 (M): 3.09 → 2.44
- Tabell 5, Extended window [AD−20, ED+1] | 2022–26 (intervall), kol. 4 (M): [3.80, 13.27] → [3.06, 10.73]
- Tabell 5, Extended window [AD−20, ED+1] | 2022–26 (intervall), kol. 8 (M): [−3.26, 7.30] → [−2.46, 5.83]
- Tabell 5, Extended window [AD−20, ED+1] | 2007–16, kol. 3 (D̄): 0.34 → 0.43
- Tabell 5, Extended window [AD−20, ED+1] | 2007–16, kol. 4 (M): 4.03 → 3.21
- Tabell 5, Extended window [AD−20, ED+1] | 2007–16, kol. 7 (D̄): −0.30 → −0.43
- Tabell 5, Extended window [AD−20, ED+1] | 2007–16, kol. 8 (M): 12.88 → 9.09
- Tabell 5, Extended window [AD−20, ED+1] | 2007–16 (intervall), kol. 4 (M): [−14.10, 26.28] → [−11.67, 19.26]
- Tabell 5, Extended window [AD−20, ED+1] | 2007–16 (intervall), kol. 8 (M): [−7.41, 47.67] → [−5.10, 37.15]
- Tabell 5, Extended window [AD−20, ED+1] | 2017–26, kol. 3 (D̄): 0.88 → 1.04
- Tabell 5, Extended window [AD−20, ED+1] | 2017–26, kol. 4 (M): 6.54 → 5.54
- Tabell 5, Extended window [AD−20, ED+1] | 2017–26, kol. 7 (D̄): −0.93 → −1.12
- Tabell 5, Extended window [AD−20, ED+1] | 2017–26, kol. 8 (M): 1.74 → 1.45
- Tabell 5, Extended window [AD−20, ED+1] | 2017–26 (intervall), kol. 4 (M): [3.51, 10.11] → [2.98, 8.48]
- Tabell 5, Extended window [AD−20, ED+1] | 2017–26 (intervall), kol. 8 (M): [−2.96, 5.59] → [−2.35, 4.61]
- Tabell 5 table1: ny tabell (14 rader)
- Tabell 6,  | M, 2007–11, kol. 1 (No controls): 84.97 → 57.87
- Tabell 6,  | M, 2007–11, kol. 2 (Controls): 79.68 → 54.85
- Tabell 6,  | M, 2007–11, kol. 3 (No controls): −0.93 → −0.72
- Tabell 6,  | M, 2007–11, kol. 4 (Controls): 2.17 → 1.68
- Tabell 6,  | M, 2007–11 (intervall), kol. 1 (No controls): [11.98, 157.95] → [8.16, 107.57]
- Tabell 6,  | M, 2007–11 (intervall), kol. 2 (Controls): [2.94, 156.41] → [2.03, 107.67]
- Tabell 6,  | M, 2007–11 (intervall), kol. 3 (No controls): [−16.84, 14.98] → [−13.05, 11.61]
- Tabell 6,  | M, 2007–11 (intervall), kol. 4 (Controls): [−12.48, 16.81] → [−9.67, 13.03]
- Tabell 6,  | M, 2012–16, kol. 1 (No controls): −4.67 → −3.76
- Tabell 6,  | M, 2012–16, kol. 2 (Controls): −1.96 → −1.57
- Tabell 6,  | M, 2012–16, kol. 3 (No controls): 6.28 → 4.36
- Tabell 6,  | M, 2012–16, kol. 4 (Controls): 4.49 → 3.10
- Tabell 6,  | M, 2012–16 (intervall), kol. 1 (No controls): [−12.91, 3.57] → [−10.40, 2.88]
- Tabell 6,  | M, 2012–16 (intervall), kol. 2 (Controls): [−9.55, 5.63] → [−7.64, 4.50]
- Tabell 6,  | M, 2012–16 (intervall), kol. 3 (No controls): [−15.51, 28.07] → [−10.77, 19.49]
- Tabell 6,  | M, 2012–16 (intervall), kol. 4 (Controls): [−16.87, 25.84] → [−11.64, 17.83]
- Tabell 6,  | M, 2017–21, kol. 1 (No controls): 3.29 → 2.97
- Tabell 6,  | M, 2017–21, kol. 2 (Controls): 2.88 → 2.60
- Tabell 6,  | M, 2017–21, kol. 3 (No controls): 0.22 → 0.20
- Tabell 6,  | M, 2017–21 (intervall), kol. 1 (No controls): [0.27, 6.31] → [0.24, 5.71]
- Tabell 6,  | M, 2017–21 (intervall), kol. 2 (Controls): [−0.40, 6.16] → [−0.36, 5.57]
- Tabell 6,  | M, 2017–21 (intervall), kol. 3 (No controls): [−4.04, 4.47] → [−3.71, 4.11]
- Tabell 6,  | M, 2017–21 (intervall), kol. 4 (Controls): [−3.96, 3.92] → [−3.63, 3.59]
- Tabell 6,  | M, 2022–26, kol. 1 (No controls): 2.94 → 2.35
- Tabell 6,  | M, 2022–26, kol. 2 (Controls): 2.57 → 2.05
- Tabell 6,  | M, 2022–26, kol. 3 (No controls): 1.78 → 1.41
- Tabell 6,  | M, 2022–26, kol. 4 (Controls): 1.93 → 1.52
- Tabell 6,  | M, 2022–26 (intervall), kol. 1 (No controls): [0.24, 5.65] → [0.19, 4.50]
- Tabell 6,  | M, 2022–26 (intervall), kol. 2 (Controls): [0.92, 4.21] → [0.74, 3.36]
- Tabell 6,  | M, 2022–26 (intervall), kol. 3 (No controls): [−0.46, 4.02] → [−0.36, 3.18]
- Tabell 6,  | M, 2022–26 (intervall), kol. 4 (Controls): [−0.47, 4.33] → [−0.37, 3.42]
- Tabell 6, Differences | 2007–11 − 2022–26, kol. 1 (No controls): 82.03 → 55.52
- Tabell 6, Differences | 2007–11 − 2022–26, kol. 2 (Controls): 77.11 → 52.80
- Tabell 6, Differences | 2007–11 − 2022–26, kol. 3 (No controls): −2.71 → −2.13
- Tabell 6, Differences | 2007–11 − 2022–26, kol. 4 (Controls): 0.24 → 0.16
- Tabell 6, Differences | 2007–11 − 2022–26 (intervall), kol. 1 (No controls): [−42.16, 140.25] → [−29.09, 95.35]
- Tabell 6, Differences | 2007–11 − 2022–26 (intervall), kol. 2 (Controls): [−∞, 587.77] → [−∞, 266.27]
- Tabell 6, Differences | 2012–16 − 2022–26, kol. 1 (No controls): −7.61* → −6.11*
- Tabell 6, Differences | 2012–16 − 2022–26, kol. 2 (Controls): −4.53 → −3.61
- Tabell 6, Differences | 2012–16 − 2022–26, kol. 3 (No controls): 4.50 → 2.95
- Tabell 6, Differences | 2012–16 − 2022–26, kol. 4 (Controls): 2.56 → 1.57
- Tabell 6, Differences | 2012–16 − 2022–26 (intervall), kol. 1 (No controls): [−18.81, 1.16] → [−15.21, 1.02]
- Tabell 6, Differences | 2012–16 − 2022–26 (intervall), kol. 2 (Controls): [−14.24, 4.34] → [−11.34, 3.30]
- Tabell 6, Differences | 2012–16 − 2022–26 (intervall), kol. 3 (No controls): [−14.44, 53.57] → [−10.35, 37.02]
- Tabell 6, Differences | 2012–16 − 2022–26 (intervall), kol. 4 (Controls): [−14.14, 48.72] → [−10.13, 33.47]
- Tabell 6, Differences | 2017–21 − 2022–26, kol. 1 (No controls): 0.35 → 0.63
- Tabell 6, Differences | 2017–21 − 2022–26, kol. 2 (Controls): 0.31 → 0.56
- Tabell 6, Differences | 2017–21 − 2022–26, kol. 3 (No controls): −1.57 → −1.21
- Tabell 6, Differences | 2017–21 − 2022–26, kol. 4 (Controls): −1.95 → −1.54
- Tabell 6, Differences | 2017–21 − 2022–26 (intervall), kol. 1 (No controls): [−4.13, 5.08] → [−3.16, 4.78]
- Tabell 6, Differences | 2017–21 − 2022–26 (intervall), kol. 2 (Controls): [−3.61, 5.02] → [−2.88, 4.79]
- Tabell 6, Differences | 2017–21 − 2022–26 (intervall), kol. 3 (No controls): [−7.37, 3.37] → [−6.78, 3.10]
- Tabell 6, Differences | 2017–21 − 2022–26 (intervall), kol. 4 (Controls): [−7.67, 2.96] → [−6.56, 2.83]
- Tabell 7, Panel A. Additions: net buying | OMXSB index trackers (C) (rad): ny rad: 0.15 · 0.52 · 1.11 · 0.97 · 1.03
- Tabell 7, Panel A. Additions: net buying | OMXSB index trackers (C) (intervall): ny rad: [0.04, 0.26] · [0.28, 0.75] · [0.96, 1.25] · [0.65, 1.29] · [0.85, 1.21]
- Tabell 7, Panel A. Additions: net buying |   Pure index funds (B) (rad): ny rad: 0.10 · 0.37 · 0.92 · 0.41 · 0.63
- Tabell 7, Panel A. Additions: net buying |   Pure index funds (B) (intervall): ny rad: [0.06, 0.15] · [0.18, 0.56] · [0.81, 1.03] · [0.30, 0.51] · [0.47, 0.78]
- Tabell 7, Panel A. Additions: net buying |   Tracker variants (rad): ny rad: 0.05 · 0.12 · 0.10 · 0.37 · 0.26
- Tabell 7, Panel A. Additions: net buying |   Tracker variants (intervall): ny rad: [−0.04, 0.14] · [0.06, 0.19] · [0.04, 0.16] · [0.18, 0.56] · [0.14, 0.38]
- Tabell 7, Panel A. Additions: net buying |   Balanced funds, OMXSB share (rad): ny rad: 0.00 · 0.02 · 0.09 · 0.20 · 0.15
- Tabell 7, Panel A. Additions: net buying |   Balanced funds, OMXSB share (intervall): ny rad: [0.00, 0.00] · [−0.01, 0.06] · [0.07, 0.11] · [0.13, 0.27] · [0.10, 0.20]
- Tabell 7, Panel B. Deletions: net selling | OMXSB index trackers (C) (rad): ny rad: 0.26 · 0.48 · 0.98 · 1.18 · 1.11
- Tabell 7, Panel B. Deletions: net selling | OMXSB index trackers (C) (intervall): ny rad: [−0.31, 0.83] · [0.19, 0.76] · [0.87, 1.10] · [0.82, 1.54] · [0.89, 1.32]
- Tabell 7, Panel B. Deletions: net selling |   Pure index funds (B) (rad): ny rad: 0.20 · 0.31 · 0.83 · 0.52 · 0.64
- Tabell 7, Panel B. Deletions: net selling |   Pure index funds (B) (intervall): ny rad: [−0.27, 0.68] · [0.09, 0.53] · [0.72, 0.94] · [0.38, 0.65] · [0.52, 0.75]
- Tabell 7, Panel B. Deletions: net selling |   Tracker variants (rad): ny rad: 0.06 · 0.16 · 0.08 · 0.42 · 0.29
- Tabell 7, Panel B. Deletions: net selling |   Tracker variants (intervall): ny rad: [−0.06, 0.17] · [0.01, 0.31] · [0.05, 0.12] · [0.18, 0.65] · [0.13, 0.45]
- Tabell 7, Panel B. Deletions: net selling |   Balanced funds, OMXSB share (rad): ny rad: 0.00 · 0.01 · 0.07 · 0.25 · 0.18
- Tabell 7, Panel B. Deletions: net selling |   Balanced funds, OMXSB share (intervall): ny rad: [0.00, 0.00] · [−0.02, 0.04] · [0.06, 0.09] · [0.16, 0.33] · [0.11, 0.25]
- Tabell 10,  | Additions, 2017–21, all events, kol. 3 (D̄ (%)): 1.00 → 1.11
- Tabell 10,  | Additions, 2017–21, all events, kol. 4 (M): 3.29 → 2.97
- Tabell 10,  | Additions, 2017–21, all events (intervall), kol. 4 (M): [0.98, 6.85] → [0.90, 6.20]
- Tabell 10,  | Additions, 2017–21, excluding overlap, kol. 3 (D̄ (%)): 1.01 → 1.11
- Tabell 10,  | Additions, 2017–21, excluding overlap, kol. 4 (M): 2.60 → 2.35
- Tabell 10,  | Additions, 2017–21, excluding overlap (intervall), kol. 4 (M): [0.60, 5.27] → [0.55, 4.75]
- Tabell 10,  | Additions, 2022–26, all events, kol. 3 (D̄ (%)): 0.78 → 0.97
- Tabell 10,  | Additions, 2022–26, all events, kol. 4 (M): 2.94 → 2.35
- Tabell 10,  | Additions, 2022–26, all events (intervall), kol. 4 (M): [0.80, 5.31] → [0.63, 4.28]
- Tabell 10,  | Additions, 2022–26, excluding overlap, kol. 3 (D̄ (%)): 0.74 → 0.94
- Tabell 10,  | Additions, 2022–26, excluding overlap, kol. 4 (M): 1.98 → 1.56
- Tabell 10,  | Additions, 2022–26, excluding overlap (intervall), kol. 4 (M): [0.64, 3.98] → [0.50, 3.21]
- Tabell 10,  | Additions, 2017–26, all events, kol. 3 (D̄ (%)): 0.87 → 1.03
- Tabell 10,  | Additions, 2017–26, all events, kol. 4 (M): 3.11 → 2.63
- Tabell 10,  | Additions, 2017–26, all events (intervall), kol. 4 (M): [1.48, 5.13] → [1.26, 4.37]
- Tabell 10,  | Additions, 2017–26, excluding overlap, kol. 3 (D̄ (%)): 0.85 → 1.01
- Tabell 10,  | Additions, 2017–26, excluding overlap, kol. 4 (M): 2.28 → 1.92
- Tabell 10,  | Additions, 2017–26, excluding overlap (intervall), kol. 4 (M): [0.98, 3.97] → [0.83, 3.37]
- Tabell 10,  | Deletions, 2017–21, all events, kol. 3 (D̄ (%)): −0.91 → −0.99
- Tabell 10,  | Deletions, 2017–21, all events, kol. 4 (M): 0.22 → 0.20
- Tabell 10,  | Deletions, 2017–21, all events (intervall), kol. 4 (M): [−4.56, 3.53] → [−4.18, 3.26]
- Tabell 10,  | Deletions, 2022–26, all events, kol. 3 (D̄ (%)): −0.93 → −1.18
- Tabell 10,  | Deletions, 2022–26, all events, kol. 4 (M): 1.78 → 1.41
- Tabell 10,  | Deletions, 2022–26, all events (intervall), kol. 4 (M): [0.00, 3.19] → [0.00, 2.55]
- Tabell 10,  | Deletions, 2017–26, all events, kol. 3 (D̄ (%)): −0.92 → −1.11
- Tabell 10,  | Deletions, 2017–26, all events, kol. 4 (M): 1.21 → 1.01
- Tabell 10,  | Deletions, 2017–26, all events (intervall), kol. 4 (M): [−1.02, 2.80] → [−0.86, 2.36]
- Tabell 10,  | Deletions, 2017–26, excluding overlap, kol. 3 (D̄ (%)): −0.91 → −1.10
- Tabell 10,  | Deletions, 2017–26, excluding overlap, kol. 4 (M): 0.78 → 0.64
- Tabell 10,  | Deletions, 2017–26, excluding overlap (intervall), kol. 4 (M): [−1.46, 2.40] → [−1.23, 1.99]
- Tabell 12,  |  (intervall), kol. 1 (Run-up
[AD, ED−1]
- Tabell 12,  |  (intervall), kol. 2 (CAR
[ED, ED+10]
- Tabell 12,  |  (intervall), kol. 3 (CAR
[ED, ED+20]
- Tabell 12,  |  (intervall), kol. 4 (Run-up
[AD, ED−1]
- Tabell 12,  |  (intervall), kol. 5 (CAR
[ED, ED+10]
- Tabell 12,  |  (intervall), kol. 6 (CAR
[ED, ED+20]
- Tabell A2,  | Change in M for additions, 2017–21 minus 2022–26, kol. 2 (SE): 1.988 → 1.707
- Tabell A2,  | Change in M for additions, 2017–21 minus 2022–26, kol. 4 (MDE): 5.75 → 4.94
- Tabell A3,  | Additions, excl. split events, kol. 6 (D̄ (%)): 0.88 → 1.05
- Tabell A3,  | Additions, excl. split events, kol. 7 (M): 2.75 → 2.30
- Tabell A3,  | Additions, excl. split events (intervall), kol. 7 (M): [1.10, 5.04] → [0.93, 4.15]
- Tabell A3,  | Deletions, excl. split events, kol. 6 (D̄ (%)): −0.94 → −1.15
- Tabell A3,  | Deletions, excl. split events, kol. 7 (M): 1.12 → 0.92
- Tabell A3,  | Deletions, excl. split events (intervall), kol. 7 (M): [−1.51, 2.83] → [−1.24, 2.33]
- Tabell A5,  | 2017–21, kol. 1 (M): 3.29 → 2.97
- Tabell A5,  | 2017–21, kol. 3 (M): 2.88 → 2.61
- Tabell A5,  | 2017–21 (intervall), kol. 1 (M): [1.00, 6.77] → [0.91, 6.08]
- Tabell A5,  | 2017–21 (intervall), kol. 3 (M): [0.94, 5.52] → [0.85, 4.95]
- Tabell A5,  | 2022–26, kol. 1 (M): 2.94 → 2.35
- Tabell A5,  | 2022–26, kol. 3 (M): 1.70 → 1.36
- Tabell A5,  | 2022–26 (intervall), kol. 1 (M): [0.78, 5.31] → [0.61, 4.28]
- Tabell A5,  | 2022–26 (intervall), kol. 3 (M): [0.20, 3.65] → [0.16, 2.97]
- Tabell A5,  | 2017–26, kol. 1 (M): 3.11 → 2.63
- Tabell A5,  | 2017–26, kol. 3 (M): 2.27 → 1.92
- Tabell A5,  | 2017–26 (intervall), kol. 1 (M): [1.47, 5.13] → [1.25, 4.34]
- Tabell A5,  | 2017–26 (intervall), kol. 3 (M): [1.03, 3.83] → [0.87, 3.26]
