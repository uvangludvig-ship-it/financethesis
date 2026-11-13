# Table 2, old (2013–2026, 27 reviews) versus new (2007–2026, 39 reviews)

Cells: mean CAR in percent against .OMXSBGI, stars from the HC1 p-value, HC1 standard error in parentheses, standard error clustered on announcement date in brackets, wild cluster bootstrap p-value in braces, N events. Last − previous is the last period minus the second-to-last. The F-test is the cluster-robust test of equal means across the periods of the table, p-value from F(k−1, G−1).

## New run: code/notebooks/replication_omxsb_2007.ipynb on data/raw/lseg/panel_2005_2026 (487 events, 39 reviews, 4 periods)

| Type | Window | 2007–2011 | 2012–2016 | 2017–2021 | 2022–2026 | Last − previous | F, equal means |
|---|---|---|---|---|---|---|---|
| Additions | Announcement window [AD−1, AD+1] | 0.96 (0.66) [0.84] {0.405} N=36 | 1.87*** (0.63) [0.79] {0.040} N=54 | -0.16 (0.63) [1.21] {0.985} N=83 | 1.20 (0.79) [0.70] {0.123} N=87 | 1.36 (1.01) [1.37] {0.473} N=170 | 0.73 (p = 0.540; G = 38) |
| Additions | Effective window [ED−1, ED+1] | 1.16 (0.88) [1.23] {0.357} N=35 | -0.73 (0.71) [0.94] {0.520} N=54 | 0.38 (0.42) [0.71] {0.615} N=82 | -0.09 (0.76) [0.53] {0.866} N=87 | -0.47 (0.87) [0.86] {0.608} N=169 | 0.64 (p = 0.596; G = 38) |
| Additions | Total window [AD−1, ED+1] | 8.52*** (1.48) [2.43] {0.025} N=33 | 0.25 (1.38) [1.82] {0.904} N=54 | 2.85*** (1.09) [0.82] {0.004} N=82 | 1.50 (1.17) [0.74] {0.070} N=87 | -1.35 (1.60) [1.07] {0.241} N=169 | 3.40 (p = 0.028; G = 38) |
| Deletions | Announcement window [AD−1, AD+1] | 0.02 (0.98) [1.36] {0.988} N=38 | -1.69*** (0.54) [0.48] {0.014} N=47 | -1.97*** (0.52) [0.61] {0.010} N=64 | -0.65 (0.44) [0.67] {0.395} N=77 | 1.32* (0.68) [0.88] {0.182} N=141 | 1.28 (p = 0.295; G = 38) |
| Deletions | Effective window [ED−1, ED+1] | -0.17 (1.06) [1.56] {0.914} N=38 | -0.79 (0.80) [1.28] {0.622} N=47 | 0.86* (0.48) [0.56] {0.147} N=64 | -1.26*** (0.45) [0.68] {0.125} N=77 | -2.12*** (0.66) [0.86] {0.026} N=141 | 2.20 (p = 0.104; G = 38) |
| Deletions | Total window [AD−1, ED+1] | -6.69*** (1.59) [1.69] {0.004} N=38 | -2.45 (1.66) [3.42] {0.530} N=47 | -0.57 (1.03) [1.41] {0.693} N=63 | -1.52** (0.68) [1.11] {0.266} N=77 | -0.95 (1.23) [1.76] {0.614} N=140 | 3.14 (p = 0.037; G = 38) |

## Original run: code/notebooks/replication_omxsb.ipynb on data/raw/lseg/panel_2012_2026 (380 events, 27 reviews, 4 periods)

| Type | Window | 2013–2017 | 2018–2020 | 2021–2023 | 2024–2026 | Last − previous | F, equal means |
|---|---|---|---|---|---|---|---|
| Additions | Announcement window [AD−1, AD+1] | 1.78*** (0.64) [0.75] {0.024} N=57 | -1.35 (0.89) [1.57] {0.926} N=51 | 0.55 (0.86) [0.90] {0.540} N=59 | 2.24** (1.09) [0.43] {0.027} N=45 | 1.68 (1.38) [0.96] {0.120} N=104 | 2.67 (p = 0.068; G = 27) |
| Additions | Effective window [ED−1, ED+1] | -0.93 (0.72) [0.96] {0.393} N=57 | 1.73*** (0.45) [0.30] {0.004} N=51 | -0.60 (0.73) [0.55] {0.332} N=59 | -0.03 (1.17) [0.83] {0.968} N=45 | 0.57 (1.38) [0.94] {0.636} N=104 | 7.58 (p = 0.001; G = 27) |
| Additions | Total window [AD−1, ED+1] | 2.21 (1.43) [1.95] {0.280} N=57 | 2.35 (1.56) [0.88] {0.045} N=51 | 0.51 (1.01) [0.71] {0.519} N=59 | 2.67 (1.88) [0.68] {0.030} N=45 | 2.16 (2.13) [0.94] {0.056} N=104 | 2.07 (p = 0.129; G = 27) |
| Deletions | Announcement window [AD−1, AD+1] | -1.88*** (0.54) [0.49] {0.004} N=36 | -1.84** (0.73) [0.77] {0.056} N=39 | -1.67*** (0.61) [1.04] {0.180} N=54 | -0.19 (0.47) [0.46] {0.703} N=39 | 1.48* (0.77) [1.10] {0.240} N=93 | 2.86 (p = 0.056; G = 27) |
| Deletions | Effective window [ED−1, ED+1] | -1.07 (1.00) [1.44] {0.683} N=36 | 1.00 (0.63) [0.76] {0.236} N=39 | -0.37 (0.56) [0.63] {0.664} N=54 | -2.05*** (0.61) [0.90] {0.032} N=39 | -1.68** (0.82) [1.04] {0.174} N=93 | 2.71 (p = 0.066; G = 27) |
| Deletions | Total window [AD−1, ED+1] | -5.49*** (1.79) [2.19] {0.009} N=36 | 1.13 (1.52) [1.76] {0.560} N=39 | -1.45* (0.81) [1.36] {0.406} N=54 | -2.69*** (0.90) [1.63] {0.163} N=39 | -1.24 (1.21) [2.02] {0.618} N=93 | 2.19 (p = 0.114; G = 27) |

## F-test for equal period means, old versus new

F_original and p_original are from the original run (its four periods 2013–2017, 2018–2020, 2021–2023, 2024–2026, 2012 panel); F_old and p_old are the same four-period test on the 2013–2026 events of the new run (2005 panel); F_new and p_new use the four equal five-year periods of the new run (2007–2011, 2012–2016, 2017–2021, 2022–2026). G is the number of announcement-date clusters.

| type | window | F_original | p_original | G_original | F_old | p_old | G_old | reviews_old | F_new | p_new | G_new | reviews_new |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| addition | ann | 2.669 | 0.068 | 27 | 2.669 | 0.068 | 27 | 27 | 0.731 | 0.540 | 38 | 38 |
| addition | eff | 7.581 | 0.001 | 27 | 7.135 | 0.001 | 27 | 27 | 0.637 | 0.596 | 38 | 38 |
| addition | tot | 2.070 | 0.129 | 27 | 2.130 | 0.121 | 27 | 27 | 3.404 | 0.028 | 38 | 38 |
| deletion | ann | 2.859 | 0.056 | 27 | 2.859 | 0.056 | 27 | 27 | 1.281 | 0.295 | 38 | 38 |
| deletion | eff | 2.707 | 0.066 | 27 | 2.707 | 0.066 | 27 | 27 | 2.204 | 0.104 | 38 | 38 |
| deletion | tot | 2.187 | 0.114 | 27 | 2.021 | 0.136 | 27 | 27 | 3.140 | 0.037 | 38 | 38 |

## Trend test

OLS of the total-window CAR [AD−1, ED+1] on the period index (0 for the first period of the sample, 1 for the next, and so on), one observation per event, standard error clustered on announcement date (CR1), p-value from t(G−1), and the wild cluster bootstrap p-value with the null imposed (9,999 draws, Webb weights if G < 12, Rademacher otherwise). Old uses the original run's four periods 2013–2026 (index 0 = 2013–2017, unequal in length) on the new run's events; new uses the four equal five-year periods 2007–2026 (index 0 = 2007–2011), so its slope is the change in the mean CAR per five years in percentage points.

| type | sample | slope | se_cr1 | p_cr1 | p_wcb | N | G | n_periods | reviews | first | last |
|---|---|---|---|---|---|---|---|---|---|---|---|
| addition | old: 2013-2026, the original run's four periods | -0.115 | 0.659 | 0.863 | 0.866 | 211 | 27 | 4 | 27 | 2013–2017 | 2024–2026 |
| addition | new: 2007-2026, four equal five-year periods | -1.343 | 0.768 | 0.089 | 0.114 | 256 | 38 | 4 | 38 | 2007–2011 | 2022–2026 |
| deletion | old: 2013-2026, the original run's four periods | 0.570 | 0.875 | 0.520 | 0.552 | 167 | 27 | 4 | 27 | 2013–2017 | 2024–2026 |
| deletion | new: 2007-2026, four equal five-year periods | 1.500 | 0.770 | 0.059 | 0.070 | 225 | 38 | 4 | 38 | 2007–2011 | 2022–2026 |
