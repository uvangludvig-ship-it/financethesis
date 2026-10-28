# Table 2, old (2013–2026, 27 reviews) versus new (2007–2026, 39 reviews)

Cells: mean CAR in percent against .OMXSBGI, stars from the HC1 p-value, HC1 standard error in parentheses, standard error clustered on announcement date in brackets, wild cluster bootstrap p-value in braces, N events. Last − previous is the last period minus the second-to-last. The F-test is the cluster-robust test of equal means across the periods of the table, p-value from F(k−1, G−1).

## New run: code/notebooks/replication_omxsb_2007.ipynb on data/raw/lseg/panel_2005_2026 (487 events, 39 reviews, 5 periods)

| Type | Window | 2007–2012 | 2013–2017 | 2018–2020 | 2021–2023 | 2024–2026 | Last − previous | F, equal means |
|---|---|---|---|---|---|---|---|---|
| Additions | Announcement window [AD−1, AD+1] | 1.32** (0.52) [0.64] {0.135} N=49 | 1.78*** (0.64) [0.75] {0.024} N=57 | -1.35 (0.89) [1.57] {0.926} N=51 | 0.55 (0.86) [0.90] {0.540} N=59 | 2.24** (1.09) [0.43] {0.027} N=45 | 1.68 (1.38) [0.96] {0.120} N=104 | 2.12 (p = 0.098; G = 38) |
| Additions | Effective window [ED−1, ED+1] | 0.66 (0.68) [1.02] {0.527} N=49 | -0.93 (0.72) [0.96] {0.393} N=57 | 1.75*** (0.46) [0.30] {0.003} N=51 | -0.60 (0.73) [0.55] {0.332} N=59 | -0.03 (1.17) [0.83] {0.968} N=45 | 0.57 (1.38) [0.94] {0.636} N=104 | 5.81 (p = 0.001; G = 38) |
| Additions | Total window [AD−1, ED+1] | 6.18*** (1.34) [2.39] {0.029} N=49 | 2.21 (1.43) [1.95] {0.280} N=57 | 2.35 (1.56) [0.87] {0.044} N=51 | 0.51 (1.01) [0.71] {0.519} N=59 | 2.67 (1.88) [0.68] {0.030} N=45 | 2.16 (2.13) [0.94] {0.056} N=104 | 2.42 (p = 0.066; G = 38) |
| Deletions | Announcement window [AD−1, AD+1] | -0.31 (0.71) [0.92] {0.771} N=58 | -1.88*** (0.54) [0.49] {0.004} N=36 | -1.84** (0.73) [0.77] {0.056} N=39 | -1.67*** (0.61) [1.04] {0.180} N=54 | -0.19 (0.47) [0.46] {0.703} N=39 | 1.48* (0.77) [1.10] {0.240} N=93 | 2.36 (p = 0.071; G = 38) |
| Deletions | Effective window [ED−1, ED+1] | 0.23 (0.73) [1.03] {0.826} N=58 | -1.07 (1.00) [1.44] {0.683} N=36 | 1.00 (0.63) [0.76] {0.236} N=39 | -0.37 (0.56) [0.63] {0.664} N=54 | -2.05*** (0.61) [0.90] {0.032} N=39 | -1.68** (0.82) [1.04] {0.174} N=93 | 2.14 (p = 0.096; G = 38) |
| Deletions | Total window [AD−1, ED+1] | -3.01** (1.35) [2.86] {0.364} N=58 | -5.49*** (1.79) [2.19] {0.009} N=36 | 1.08 (1.51) [1.74] {0.574} N=39 | -1.45* (0.81) [1.36] {0.406} N=54 | -2.69*** (0.90) [1.63] {0.163} N=39 | -1.24 (1.21) [2.02] {0.618} N=93 | 1.69 (p = 0.173; G = 38) |

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

F_original and p_original are from the original run (four periods, 2012 panel); F_old and p_old are the same four-period test on the 2013–2026 events of the new run (2005 panel); F_new and p_new use all five periods. G is the number of announcement-date clusters.

| type | window | F_original | p_original | G_original | F_old | p_old | G_old | reviews_old | F_new | p_new | G_new | reviews_new |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| addition | ann | 2.669 | 0.068 | 27 | 2.669 | 0.068 | 27 | 27 | 2.119 | 0.098 | 38 | 38 |
| addition | eff | 7.581 | 0.001 | 27 | 7.639 | 0.001 | 27 | 27 | 5.809 | 0.001 | 38 | 38 |
| addition | tot | 2.070 | 0.129 | 27 | 2.074 | 0.128 | 27 | 27 | 2.420 | 0.066 | 38 | 38 |
| deletion | ann | 2.859 | 0.056 | 27 | 2.859 | 0.056 | 27 | 27 | 2.361 | 0.071 | 38 | 38 |
| deletion | eff | 2.707 | 0.066 | 27 | 2.707 | 0.066 | 27 | 27 | 2.136 | 0.096 | 38 | 38 |
| deletion | tot | 2.187 | 0.114 | 27 | 2.165 | 0.116 | 27 | 27 | 1.690 | 0.173 | 38 | 38 |

## Trend test

OLS of the total-window CAR [AD−1, ED+1] on the period index (0 for the first period of the sample, 1 for the next, and so on), one observation per event, standard error clustered on announcement date (CR1), p-value from t(G−1), and the wild cluster bootstrap p-value with the null imposed (9,999 draws, Webb weights if G < 12, Rademacher otherwise). Old uses the four periods 2013–2026 (index 0 = 2013–2017) on the new run; new adds 2007–2012 as index 0 (five periods). The slope is the change in the mean CAR per period in percentage points.

| type | sample | slope | se_cr1 | p_cr1 | p_wcb | N | G | n_periods | reviews | first | last |
|---|---|---|---|---|---|---|---|---|---|---|---|
| addition | old: 2013-2026, four periods | -0.109 | 0.658 | 0.870 | 0.872 | 212 | 27 | 4 | 27 | 2013–2017 | 2024–2026 |
| addition | new: 2007-2026, five periods | -0.906 | 0.555 | 0.111 | 0.124 | 261 | 38 | 5 | 38 | 2007–2012 | 2024–2026 |
| deletion | old: 2013-2026, four periods | 0.538 | 0.878 | 0.546 | 0.574 | 168 | 27 | 4 | 27 | 2013–2017 | 2024–2026 |
| deletion | new: 2007-2026, five periods | 0.447 | 0.748 | 0.553 | 0.634 | 226 | 38 | 5 | 38 | 2007–2012 | 2024–2026 |
