# Trend tests: bin-free and for every equidistant period length

Bin-free (do not depend on how years are grouped):
  T1  OLS of the event CAR on calendar time (years since 2007, effective date), SE clustered on announcement
      date (CR1), p from t(G-1), and the wild cluster bootstrap p with the null imposed.
  T2  Review-level: mean CAR per review (38 reviews) regressed on time, HC1 p; and Spearman rank correlation
      between review date and review mean.
  T3  Mann-Kendall: Kendall's tau between event time and CAR, normal-approximation p (events treated as
      independent, so this ignores the clustering and is reported as a descriptive test).
  T4  Sup-Wald test for a single break in the mean at an unknown review boundary (at least 5 reviews on each
      side), Wald with CR1 variance, p from the wild cluster bootstrap under the no-break null (999 draws).
Per period length L in {1, 2, 4, 5, 10}:
  P1  OLS of the CAR on the period index (slope per period; also per year), CR1 and wild bootstrap p.
  P2  Jonckheere-Terpstra test for an ordered alternative across the periods (computed as Kendall's tau between
      the period index and the CAR; identical ordering statistic), normal-approximation p.
  P3  Spearman between the period index and the period mean (k points).
  P4  Sup-Wald break test with the break restricted to the period boundaries (at least 5 reviews on each side, as in T4), wild cluster bootstrap p.
Reads output/omxsb_replication_2007/events_car.csv; writes period_sensitivity/TREND_TESTS.md and .csv.

Sample: 487 OMXSB events 2007–2026 (`events_car.csv`), CAR in percent against .OMXSBGI. Stat = slope, tau, rho or sup-Wald; p = analytical p (CR1 t for OLS, normal for tau and HC1, exact/approx for Spearman); p_boot = wild cluster bootstrap with the null imposed. A negative slope for additions and a positive one for deletions means the effect shrinks.

## Total [AD−1, ED+1]

**Additions**

| Length | Test | Stat | SE | p | p_boot | per year | N | G |
|---|---|---|---|---|---|---|---|---|
| bin-free | T1 OLS on calendar time (per year) | -0.287 | 0.158 | 0.078 | 0.101 |  | 256 | 38 |
| bin-free | T2a review means on time (per year), HC1 | -0.298 | 0.161 | 0.064 |  |  | 38 | 38 |
| bin-free | T2b Spearman, review date vs review mean | -0.259 |  | 0.117 |  |  | 38 | 38 |
| bin-free | T3 Mann-Kendall tau, event time vs CAR (no clustering) | -0.121 |  | 0.004 |  |  | 256 | 38 |
| bin-free | T4 sup-Wald single break (break after 2010-06-01 review; pre 11.37, post 1.75) | 19.139 |  |  | 0.014 |  | 256 | 38 |
| 1 | P1 OLS on period index (slope per period) | -0.278 | 0.160 | 0.091 | 0.112 | -0.278 | 256 | 38 |
| 1 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.120 |  | 0.005 |  |  | 256 | 38 |
| 1 | P3 Spearman, period index vs period mean | -0.439 |  | 0.053 |  |  | 20 | 20 |
| 1 | P4 sup-Wald break at a period boundary (break before 2011; pre 11.37, post 1.75) | 19.139 |  |  | 0.015 |  | 256 | 38 |
| 2 | P1 OLS on period index (slope per period) | -0.511 | 0.323 | 0.122 | 0.147 | -0.255 | 256 | 38 |
| 2 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.115 |  | 0.009 |  |  | 256 | 38 |
| 2 | P3 Spearman, period index vs period mean | -0.285 |  | 0.425 |  |  | 10 | 10 |
| 2 | P4 sup-Wald break at a period boundary (break before 2011; pre 11.37, post 1.75) | 19.139 |  |  | 0.015 |  | 256 | 38 |
| 4 | P1 OLS on period index (slope per period) | -1.185 | 0.675 | 0.087 | 0.123 | -0.296 | 256 | 38 |
| 4 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.124 |  | 0.007 |  |  | 256 | 38 |
| 4 | P3 Spearman, period index vs period mean | -0.300 |  | 0.624 |  |  | 5 | 5 |
| 4 | P4 sup-Wald break at a period boundary (break before 2011; pre 11.37, post 1.75) | 19.139 |  |  | 0.006 |  | 256 | 38 |
| 5 | P1 OLS on period index (slope per period) | -1.343 | 0.768 | 0.089 | 0.114 | -0.269 | 256 | 38 |
| 5 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.121 |  | 0.011 |  |  | 256 | 38 |
| 5 | P3 Spearman, period index vs period mean | -0.400 |  | 0.600 |  |  | 4 | 4 |
| 5 | P4 sup-Wald break at a period boundary (break before 2012; pre 8.52, post 1.69) | 8.095 |  |  | 0.046 |  | 256 | 38 |
| 10 | P1 OLS on period index (slope per period) | -1.235 | 1.819 | 0.501 | 0.508 | -0.124 | 256 | 38 |
| 10 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.052 |  | 0.314 |  |  | 256 | 38 |
| 10 | P4 sup-Wald break at a period boundary (break before 2017; pre 3.39, post 2.15) | 0.461 |  |  | 0.527 |  | 256 | 38 |

**Deletions**

| Length | Test | Stat | SE | p | p_boot | per year | N | G |
|---|---|---|---|---|---|---|---|---|
| bin-free | T1 OLS on calendar time (per year) | 0.222 | 0.186 | 0.240 | 0.295 |  | 225 | 38 |
| bin-free | T2a review means on time (per year), HC1 | 0.519 | 0.144 | 0.000 |  |  | 38 | 38 |
| bin-free | T2b Spearman, review date vs review mean | 0.468 |  | 0.003 |  |  | 38 | 38 |
| bin-free | T3 Mann-Kendall tau, event time vs CAR (no clustering) | 0.051 |  | 0.261 |  |  | 225 | 38 |
| bin-free | T4 sup-Wald single break (break after 2010-06-01 review; pre -9.55, post -1.46) | 13.947 |  |  | 0.030 |  | 225 | 38 |
| 1 | P1 OLS on period index (slope per period) | 0.231 | 0.189 | 0.230 | 0.283 | 0.231 | 225 | 38 |
| 1 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.054 |  | 0.236 |  |  | 225 | 38 |
| 1 | P3 Spearman, period index vs period mean | 0.450 |  | 0.047 |  |  | 20 | 20 |
| 1 | P4 sup-Wald break at a period boundary (break before 2010; pre -8.74, post -1.66) | 11.084 |  |  | 0.080 |  | 225 | 38 |
| 2 | P1 OLS on period index (slope per period) | 0.460 | 0.398 | 0.255 | 0.316 | 0.230 | 225 | 38 |
| 2 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.057 |  | 0.223 |  |  | 225 | 38 |
| 2 | P3 Spearman, period index vs period mean | 0.358 |  | 0.310 |  |  | 10 | 10 |
| 2 | P4 sup-Wald break at a period boundary (break before 2011; pre -8.11, post -1.50) | 8.953 |  |  | 0.080 |  | 225 | 38 |
| 4 | P1 OLS on period index (slope per period) | 1.189 | 0.749 | 0.121 | 0.153 | 0.297 | 225 | 38 |
| 4 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.093 |  | 0.058 |  |  | 225 | 38 |
| 4 | P3 Spearman, period index vs period mean | 0.800 |  | 0.104 |  |  | 5 | 5 |
| 4 | P4 sup-Wald break at a period boundary (break before 2011; pre -8.11, post -1.50) | 8.953 |  |  | 0.056 |  | 225 | 38 |
| 5 | P1 OLS on period index (slope per period) | 1.500 | 0.770 | 0.059 | 0.070 | 0.300 | 225 | 38 |
| 5 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.106 |  | 0.035 |  |  | 225 | 38 |
| 5 | P3 Spearman, period index vs period mean | 0.800 |  | 0.200 |  |  | 4 | 4 |
| 5 | P4 sup-Wald break at a period boundary (break before 2012; pre -6.69, post -1.43) | 7.690 |  |  | 0.043 |  | 225 | 38 |
| 10 | P1 OLS on period index (slope per period) | 3.254 | 2.439 | 0.190 | 0.262 | 0.325 | 225 | 38 |
| 10 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.117 |  | 0.033 |  |  | 225 | 38 |
| 10 | P4 sup-Wald break at a period boundary (break before 2017; pre -4.34, post -1.09) | 1.780 |  |  | 0.264 |  | 225 | 38 |

## Announcement [AD−1, AD+1]

**Additions**

| Length | Test | Stat | SE | p | p_boot | per year | N | G |
|---|---|---|---|---|---|---|---|---|
| bin-free | T1 OLS on calendar time (per year) | -0.039 | 0.076 | 0.606 | 0.610 |  | 260 | 38 |
| bin-free | T2a review means on time (per year), HC1 | 0.016 | 0.080 | 0.836 |  |  | 38 | 38 |
| bin-free | T2b Spearman, review date vs review mean | 0.143 |  | 0.390 |  |  | 38 | 38 |
| bin-free | T3 Mann-Kendall tau, event time vs CAR (no clustering) | -0.006 |  | 0.886 |  |  | 260 | 38 |
| bin-free | T4 sup-Wald single break (break after 2023-12-01 review; pre 0.59, post 2.24) | 5.309 |  |  | 0.304 |  | 260 | 38 |
| 1 | P1 OLS on period index (slope per period) | -0.035 | 0.076 | 0.652 | 0.655 | -0.035 | 260 | 38 |
| 1 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.001 |  | 0.981 |  |  | 260 | 38 |
| 1 | P3 Spearman, period index vs period mean | 0.045 |  | 0.850 |  |  | 20 | 20 |
| 1 | P4 sup-Wald break at a period boundary (break before 2024; pre 0.59, post 2.24) | 5.309 |  |  | 0.234 |  | 260 | 38 |
| 2 | P1 OLS on period index (slope per period) | -0.051 | 0.145 | 0.729 | 0.726 | -0.025 | 260 | 38 |
| 2 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.006 |  | 0.895 |  |  | 260 | 38 |
| 2 | P3 Spearman, period index vs period mean | -0.006 |  | 0.987 |  |  | 10 | 10 |
| 2 | P4 sup-Wald break at a period boundary (break before 2015; pre 1.92, post 0.54) | 2.296 |  |  | 0.541 |  | 260 | 38 |
| 4 | P1 OLS on period index (slope per period) | -0.267 | 0.338 | 0.435 | 0.449 | -0.067 | 260 | 38 |
| 4 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.019 |  | 0.679 |  |  | 260 | 38 |
| 4 | P3 Spearman, period index vs period mean | 0.000 |  | 1.000 |  |  | 5 | 5 |
| 4 | P4 sup-Wald break at a period boundary (break before 2015; pre 1.92, post 0.54) | 2.296 |  |  | 0.497 |  | 260 | 38 |
| 5 | P1 OLS on period index (slope per period) | -0.112 | 0.344 | 0.747 | 0.748 | -0.022 | 260 | 38 |
| 5 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.015 |  | 0.748 |  |  | 260 | 38 |
| 5 | P3 Spearman, period index vs period mean | 0.000 |  | 1.000 |  |  | 4 | 4 |
| 5 | P4 sup-Wald break at a period boundary (break before 2017; pre 1.51, post 0.54) | 1.122 |  |  | 0.757 |  | 260 | 38 |
| 10 | P1 OLS on period index (slope per period) | -0.966 | 0.912 | 0.296 | 0.328 | -0.097 | 260 | 38 |
| 10 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.037 |  | 0.462 |  |  | 260 | 38 |
| 10 | P4 sup-Wald break at a period boundary (break before 2017; pre 1.51, post 0.54) | 1.122 |  |  | 0.322 |  | 260 | 38 |

**Deletions**

| Length | Test | Stat | SE | p | p_boot | per year | N | G |
|---|---|---|---|---|---|---|---|---|
| bin-free | T1 OLS on calendar time (per year) | -0.032 | 0.080 | 0.686 | 0.766 |  | 226 | 38 |
| bin-free | T2a review means on time (per year), HC1 | -0.033 | 0.071 | 0.646 |  |  | 38 | 38 |
| bin-free | T2b Spearman, review date vs review mean | -0.010 |  | 0.955 |  |  | 38 | 38 |
| bin-free | T3 Mann-Kendall tau, event time vs CAR (no clustering) | 0.005 |  | 0.917 |  |  | 226 | 38 |
| bin-free | T4 sup-Wald single break (break after 2022-12-01 review; pre -1.57, post 0.22) | 7.934 |  |  | 0.093 |  | 226 | 38 |
| 1 | P1 OLS on period index (slope per period) | -0.027 | 0.078 | 0.731 | 0.790 | -0.027 | 226 | 38 |
| 1 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.006 |  | 0.893 |  |  | 226 | 38 |
| 1 | P3 Spearman, period index vs period mean | -0.101 |  | 0.673 |  |  | 20 | 20 |
| 1 | P4 sup-Wald break at a period boundary (break before 2023; pre -1.57, post 0.22) | 7.934 |  |  | 0.060 |  | 226 | 38 |
| 2 | P1 OLS on period index (slope per period) | -0.041 | 0.154 | 0.791 | 0.831 | -0.021 | 226 | 38 |
| 2 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.007 |  | 0.874 |  |  | 226 | 38 |
| 2 | P3 Spearman, period index vs period mean | -0.079 |  | 0.829 |  |  | 10 | 10 |
| 2 | P4 sup-Wald break at a period boundary (break before 2023; pre -1.57, post 0.22) | 7.934 |  |  | 0.037 |  | 226 | 38 |
| 4 | P1 OLS on period index (slope per period) | -0.018 | 0.344 | 0.959 | 0.971 | -0.004 | 226 | 38 |
| 4 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.030 |  | 0.540 |  |  | 226 | 38 |
| 4 | P3 Spearman, period index vs period mean | -0.300 |  | 0.624 |  |  | 5 | 5 |
| 4 | P4 sup-Wald break at a period boundary (break before 2023; pre -1.57, post 0.22) | 7.934 |  |  | 0.022 |  | 226 | 38 |
| 5 | P1 OLS on period index (slope per period) | -0.090 | 0.430 | 0.835 | 0.864 | -0.018 | 226 | 38 |
| 5 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.011 |  | 0.821 |  |  | 226 | 38 |
| 5 | P3 Spearman, period index vs period mean | -0.400 |  | 0.600 |  |  | 4 | 4 |
| 5 | P4 sup-Wald break at a period boundary (break before 2012; pre 0.02, post -1.36) | 1.040 |  |  | 0.655 |  | 226 | 38 |
| 10 | P1 OLS on period index (slope per period) | -0.323 | 0.817 | 0.695 | 0.727 | -0.032 | 226 | 38 |
| 10 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.010 |  | 0.849 |  |  | 226 | 38 |
| 10 | P4 sup-Wald break at a period boundary (break before 2017; pre -0.93, post -1.25) | 0.156 |  |  | 0.730 |  | 226 | 38 |

## Effective [ED−1, ED+1]

**Additions**

| Length | Test | Stat | SE | p | p_boot | per year | N | G |
|---|---|---|---|---|---|---|---|---|
| bin-free | T1 OLS on calendar time (per year) | -0.041 | 0.076 | 0.591 | 0.595 |  | 258 | 38 |
| bin-free | T2a review means on time (per year), HC1 | -0.159 | 0.124 | 0.199 |  |  | 38 | 38 |
| bin-free | T2b Spearman, review date vs review mean | -0.176 |  | 0.289 |  |  | 38 | 38 |
| bin-free | T3 Mann-Kendall tau, event time vs CAR (no clustering) | -0.048 |  | 0.253 |  |  | 258 | 38 |
| bin-free | T4 sup-Wald single break (break after 2010-06-01 review; pre 3.06, post -0.21) | 14.720 |  |  | 0.021 |  | 258 | 38 |
| 1 | P1 OLS on period index (slope per period) | -0.035 | 0.077 | 0.653 | 0.660 | -0.035 | 258 | 38 |
| 1 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.048 |  | 0.262 |  |  | 258 | 38 |
| 1 | P3 Spearman, period index vs period mean | -0.278 |  | 0.235 |  |  | 20 | 20 |
| 1 | P4 sup-Wald break at a period boundary (break before 2011; pre 3.06, post -0.21) | 14.720 |  |  | 0.022 |  | 258 | 38 |
| 2 | P1 OLS on period index (slope per period) | -0.076 | 0.154 | 0.627 | 0.630 | -0.038 | 258 | 38 |
| 2 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.055 |  | 0.212 |  |  | 258 | 38 |
| 2 | P3 Spearman, period index vs period mean | -0.127 |  | 0.726 |  |  | 10 | 10 |
| 2 | P4 sup-Wald break at a period boundary (break before 2011; pre 3.06, post -0.21) | 14.720 |  |  | 0.022 |  | 258 | 38 |
| 4 | P1 OLS on period index (slope per period) | -0.114 | 0.323 | 0.725 | 0.727 | -0.029 | 258 | 38 |
| 4 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.039 |  | 0.403 |  |  | 258 | 38 |
| 4 | P3 Spearman, period index vs period mean | -0.100 |  | 0.873 |  |  | 5 | 5 |
| 4 | P4 sup-Wald break at a period boundary (break before 2011; pre 3.06, post -0.21) | 14.720 |  |  | 0.019 |  | 258 | 38 |
| 5 | P1 OLS on period index (slope per period) | -0.168 | 0.374 | 0.655 | 0.663 | -0.034 | 258 | 38 |
| 5 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.045 |  | 0.338 |  |  | 258 | 38 |
| 5 | P3 Spearman, period index vs period mean | -0.400 |  | 0.600 |  |  | 4 | 4 |
| 5 | P4 sup-Wald break at a period boundary (break before 2012; pre 1.16, post -0.07) | 0.973 |  |  | 0.708 |  | 258 | 38 |
| 10 | P1 OLS on period index (slope per period) | 0.122 | 0.870 | 0.889 | 0.891 | 0.012 | 258 | 38 |
| 10 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | 0.010 |  | 0.846 |  |  | 258 | 38 |
| 10 | P4 sup-Wald break at a period boundary (break before 2017; pre 0.01, post 0.14) | 0.020 |  |  | 0.905 |  | 258 | 38 |

**Deletions**

| Length | Test | Stat | SE | p | p_boot | per year | N | G |
|---|---|---|---|---|---|---|---|---|
| bin-free | T1 OLS on calendar time (per year) | -0.055 | 0.098 | 0.579 | 0.605 |  | 226 | 38 |
| bin-free | T2a review means on time (per year), HC1 | 0.038 | 0.086 | 0.663 |  |  | 38 | 38 |
| bin-free | T2b Spearman, review date vs review mean | 0.032 |  | 0.847 |  |  | 38 | 38 |
| bin-free | T3 Mann-Kendall tau, event time vs CAR (no clustering) | -0.091 |  | 0.046 |  |  | 226 | 38 |
| bin-free | T4 sup-Wald single break (break after 2023-12-01 review; pre -0.03, post -2.05) | 4.519 |  |  | 0.454 |  | 226 | 38 |
| 1 | P1 OLS on period index (slope per period) | -0.052 | 0.099 | 0.607 | 0.631 | -0.052 | 226 | 38 |
| 1 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.090 |  | 0.051 |  |  | 226 | 38 |
| 1 | P3 Spearman, period index vs period mean | 0.003 |  | 0.990 |  |  | 20 | 20 |
| 1 | P4 sup-Wald break at a period boundary (break before 2024; pre -0.03, post -2.05) | 4.519 |  |  | 0.411 |  | 226 | 38 |
| 2 | P1 OLS on period index (slope per period) | -0.083 | 0.196 | 0.674 | 0.690 | -0.041 | 226 | 38 |
| 2 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.082 |  | 0.080 |  |  | 226 | 38 |
| 2 | P3 Spearman, period index vs period mean | -0.055 |  | 0.881 |  |  | 10 | 10 |
| 2 | P4 sup-Wald break at a period boundary (break before 2023; pre -0.03, post -1.45) | 2.524 |  |  | 0.509 |  | 226 | 38 |
| 4 | P1 OLS on period index (slope per period) | -0.076 | 0.407 | 0.853 | 0.860 | -0.019 | 226 | 38 |
| 4 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.063 |  | 0.199 |  |  | 226 | 38 |
| 4 | P3 Spearman, period index vs period mean | 0.000 |  | 1.000 |  |  | 5 | 5 |
| 4 | P4 sup-Wald break at a period boundary (break before 2023; pre -0.03, post -1.45) | 2.524 |  |  | 0.447 |  | 226 | 38 |
| 5 | P1 OLS on period index (slope per period) | -0.243 | 0.479 | 0.615 | 0.637 | -0.049 | 226 | 38 |
| 5 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.080 |  | 0.109 |  |  | 226 | 38 |
| 5 | P3 Spearman, period index vs period mean | -0.400 |  | 0.600 |  |  | 4 | 4 |
| 5 | P4 sup-Wald break at a period boundary (break before 2022; pre 0.08, post -1.26) | 2.394 |  |  | 0.357 |  | 226 | 38 |
| 10 | P1 OLS on period index (slope per period) | 0.212 | 1.065 | 0.843 | 0.849 | 0.021 | 226 | 38 |
| 10 | P2 Jonckheere-Terpstra (Kendall tau, period index vs CAR) | -0.014 |  | 0.790 |  |  | 226 | 38 |
| 10 | P4 sup-Wald break at a period boundary (break before 2017; pre -0.51, post -0.30) | 0.040 |  |  | 0.840 |  | 226 | 38 |

