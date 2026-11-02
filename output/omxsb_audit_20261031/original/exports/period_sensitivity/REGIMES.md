# Announcement-timing regimes and the Nov 2023 change to an exact six-day lead

Announcement-timing regimes: did the index effect change after Nov 2023, when the announcement lead became
exactly six trading days under the rulebook? Regimes (from omxsb_notes.md section 4): intraday releases 2007-2012
(lead 7-17); pre-open 08:30 releases 2013-2020 (lead 14-17); after-close releases May 2021-May 2023 (lead 7-8);
after-close, exactly six trading days, Nov 2023-2026. Mean CAR per regime and the difference between the last two,
with HC1, CR1 (clustered on announcement date) and wild cluster bootstrap p. Writes period_sensitivity/REGIMES.md.

Cell: mean CAR % against .OMXSBGI, stars HC1 p, (HC1 SE) [CR1 SE] {wild cluster bootstrap p} N events G reviews.

## Additions

| Window | R1 intraday release, lead 7–17 (2007–2012) | R2 pre-open 08:30, lead 14–17 (2013–2020) | R3 after close, lead 7–8 (May 2021–May 2023) | R4 after close, exactly 6 (Nov 2023–2026) | R4 − R3 | R4 − R2 |
|---|---|---|---|---|---|---|
| Announcement [AD−1, AD+1] | 1.28** (0.53) [0.67] {0.175} N=48 G=11 | 0.30 (0.56) [1.04] {0.877} N=108 G=16 | 0.48 (0.95) [1.02] {0.660} N=53 G=5 | 2.11** (0.96) [0.40] {0.016} N=51 G=6 | 1.63 (1.35) [1.04] {0.168} N=104 G=11 | 1.81 (1.11) [1.10] {0.165} N=159 G=22 |
| Effective [ED−1, ED+1] | 0.65 (0.70) [1.04] {0.543} N=47 G=11 | 0.29 (0.45) [0.68] {0.675} N=107 G=16 | -0.59 (0.79) [0.62] {0.380} N=53 G=5 | -0.11 (1.05) [0.73] {0.894} N=51 G=6 | 0.48 (1.31) [0.91] {0.655} N=104 G=11 | -0.39 (1.14) [0.96] {0.707} N=158 G=22 |
| Total [AD−1, ED+1] | 5.80*** (1.35) [2.52] {0.042} N=45 G=11 | 2.32** (1.06) [1.08] {0.046} N=107 G=16 | 0.46 (1.11) [0.80] {0.594} N=53 G=5 | 2.46 (1.67) [0.64] {0.019} N=51 G=6 | 1.99 (2.00) [0.98] {0.103} N=104 G=11 | 0.14 (1.97) [1.23] {0.909} N=158 G=22 |

## Deletions

| Window | R1 intraday release, lead 7–17 (2007–2012) | R2 pre-open 08:30, lead 14–17 (2013–2020) | R3 after close, lead 7–8 (May 2021–May 2023) | R4 after close, exactly 6 (Nov 2023–2026) | R4 − R3 | R4 − R2 |
|---|---|---|---|---|---|---|
| Announcement [AD−1, AD+1] | -0.31 (0.71) [0.92] {0.771} N=58 G=11 | -1.86*** (0.46) [0.44] {0.001} N=75 G=16 | -1.93*** (0.68) [1.17] {0.177} N=47 G=5 | -0.15 (0.43) [0.39] {0.716} N=46 G=6 | 1.78** (0.81) [1.17] {0.216} N=93 G=11 | 1.71*** (0.63) [0.57] {0.012} N=121 G=22 |
| Effective [ED−1, ED+1] | 0.23 (0.73) [1.03] {0.826} N=58 G=11 | 0.01 (0.59) [0.81] {0.996} N=75 G=16 | -0.34 (0.63) [0.74] {0.743} N=47 G=5 | -1.82*** (0.54) [0.80] {0.021} N=46 G=6 | -1.48* (0.83) [1.04] {0.223} N=93 G=11 | -1.83** (0.80) [1.10] {0.145} N=121 G=22 |
| Total [AD−1, ED+1] | -3.01** (1.35) [2.86] {0.364} N=58 G=11 | -2.21* (1.23) [1.53] {0.168} N=74 G=16 | -1.63* (0.85) [1.58] {0.411} N=47 G=5 | -2.33*** (0.86) [1.43] {0.143} N=46 G=6 | -0.70 (1.21) [2.03] {0.762} N=93 G=11 | -0.11 (1.50) [2.03] {0.961} N=120 G=22 |

