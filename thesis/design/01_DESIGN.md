# 01. Design: theory, measures, estimation, inference, power

Written 12 Oct 2026 as the pre-analysis plan for thesis 2. Everything here is fixed before any return around an FTN date is computed. Section numbers follow `outline/thesis2_outline.md`. Equations are numbered as they will be in the thesis. Students write the prose; this file gives them the mathematics and the specifications to write about.

## 1. The object

A regulator-driven, pre-announced, uninformed demand shock, observed at three levels:

- stock level: forced net sales and purchases by funds, dated to tranche days, with a dose that varies across stocks for reasons unrelated to the stocks (the losers' prior portfolio weights times the agency's stake);
- fund level: a redemption of 5 to 11 per cent of a fund's assets per tranche day, 15 to 44 per cent in total, where the cost is borne either by the remaining holders (NAV dilution) or by the redeemer (swing pricing);
- market level: the same mechanism as an index reconstitution, which is the anchor's object, so the reconstitution sample calibrates what a learned flow does in this market.

What the data established on 11 and 12 Oct 2026 (files in `data/`):

- Execution is in tranches, not one day. Where daily fund data exist (about 30 of 78 losers), the agency's redemptions show up as one to three days of 5 to 11 per cent of fund assets each, within two to three weeks: SEB Sverige Expanderad 15 and 19 Jan 2026 (7.1, 6.4 per cent); Ohman Sverige 13 and 20 Jan 2026 (9.9, 10.6); Lannebo Sverige 23 and 30 Jan 2026 (5.3, 5.3); Prior & Nilsson 16, 23, 29 Jan 2026 (5.2, 5.8, 5.5); Danske Sverige 15 and 22 Jan 2026. In the 2024 European round it was one day per fund (19 Jun 2024 for four funds, 26 Jun 2024 for SEB Europafond at 21.5 per cent and Templeton at 38.7 per cent of units). No loser had a single day of 5 per cent or more outflow in the year before award. The day of each tranche is the event; the dose per stock-day is the sum over funds redeemed that day. Pensionsmyndigheten says it staggers large funds "so that sales do not move market prices": the agency itself believes in H2.
- The index-effect replication moves from OMXS30 (42 usable events, 1 to 2 per cent of market cap in trackers) to OMXSB (394 events 2013 to 2026, 325 read from Nasdaq releases; tracker assets from about SEK 15bn in 2016 to about 120bn in 2026). Announcement lead was 14 to 17 trading days to 2020 and 6 trading days from Nov 2023, a within-sample change in the anticipation window that the anchor's logic predicts should matter.
- Swing pricing at exit: 11 losers yes, 38 no, 29 unknown (mostly Luxembourg). Adoption dates: SEB 14 Mar 2025, Storebrand 1 Sep 2025, Nordea Sweden before May 2024, Lannebo bond funds only. All 2019 Swedish losers no, by law.

## 3. Theory (three pages in the thesis, eight equations here, the students choose four)

### 3.1 A pre-announced uninformed flow and slow-moving capital

Consider one stock. Fundamental value is a martingale; set it to zero without loss. At date 0 the agency announces that it will sell $u > 0$ shares at date $T$ (for purchases, flip signs). Liquidity is supplied by risk-averse arbitrageurs with CARA utility, aggregate risk tolerance $\tau$, who hold the stock's residual supply $x_t$ against return variance $\sigma^2$ per period. In a static Grossman and Miller (1988) market the price concession required to hold $x$ for one period is

$$p_t = -\frac{\sigma^2}{\tau}\, x_t . \tag{1}$$

If every arbitrageur were present at $T$, the sale would be absorbed at the concession $\sigma^2 u / \tau$ and the price would recover as the position was unwound. Duffie (2010) adds the feature that matters here: only a fraction of capital is attentive at any date, and capital arrives at rate $\kappa$ after the shock. The price path is then

$$p_t = -\,\lambda\, u\, e^{-\kappa (t - T)}\quad\text{for } t \ge T, \qquad \lambda = \frac{\sigma^2}{\tau_T}, \tag{2}$$

where $\tau_T$ is the risk tolerance of the capital present on the execution day. Three predictions follow and each is one table: an execution-day drop proportional to $u$ scaled by the liquidity available ($\lambda u$); a reversal with half-life $\ln 2 / \kappa$; and, because the flow is announced at 0, an announcement-day component $p_0 = -\lambda_0 u$ where $\lambda_0 \le \lambda$ reflects how much capital can pre-position between 0 and $T$. Greenwood (2005) and Greenwood and Sammon (2025) are this model applied to index demand: as more capital learned to pre-position and the flow became predictable, $\lambda_0$ rose, $\lambda$ fell, and the total $\lambda_0 + \lambda$ fell toward zero. The FTN flow is the same object with $u / \text{ADV}$ far larger and no arbitrage community yet formed.

### 3.2 Predatory trading

Brunnermeier and Pedersen (2005): if strategic traders know the date and size of a forced sale, they sell ahead of it and buy back after, so the price overshoots at $T$ and the reversal exceeds the execution-day move. The slow-capital model and the predatory model differ in one observable: under slow capital the pre-execution drift is gradual and the execution-day move is at most the remaining concession; under predation the pre-execution drift and the execution move have the same sign and the post-execution recovery is larger than the execution move. Admati and Pfleiderer (1991): pre-announcement ("sunshine trading") lowers the cost when liquidity suppliers can coordinate, which is the opposite prediction and the one Pensionsmyndigheten's staggering policy presupposes. H3 is the horse race.

### 3.3 Square-root benchmark for expected impact

The empirical market-impact literature (Almgren, Thum, Hauptmann and Li 2005; Toth et al. 2011; Bouchaud et al. 2018; Kyle and Obizhaeva 2016 for the invariance version the 2021 winner used) finds that the peak impact of a metaorder of $Q$ shares executed over a period in which $V$ shares trade is

$$\mathbb{E}\!\left[\frac{\Delta P}{P}\right] = Y\,\sigma_d \sqrt{\frac{Q}{V}}, \qquad Y \in [0.5, 1], \tag{3}$$

with $\sigma_d$ the stock's daily volatility. Equation (3) gives, for every stock and tranche day, a predicted impact that uses no FTN returns. Two uses: ex ante, the power calculation (section 5.4); ex post, Table 3 regresses realised abnormal returns on the predicted impact and tests $\beta = 1$ (the state's trade was absorbed like any metaorder), $\beta > 1$ (predation or thinner liquidity than normal) or $\beta < 1$ (sunshine absorption). This is a sharper test than a coefficient on dose alone, because it carries an external benchmark.

### 3.4 Incidence

A fund with assets $A$ receives a redemption of a fraction $r$ at the unswung NAV. It sells $rA$ of its portfolio at a proportional cost $c$ (impact plus half-spread, which equation (3) predicts). The cost falls on the holders who remain, whose wealth is $(1-r)A$:

$$\text{dilution} = \frac{c\, r}{1 - r}. \tag{4}$$

With $r = 0.10$ per tranche and $c = 0.5$ per cent, the stayers lose 5.6 bp on the day; with $r = 0.44$ in one day and $c = 1$ per cent, 79 bp. Under swing pricing with factor $s$ applied when net outflow exceeds the threshold, the redeemer receives $(1-s)$ NAV and the dilution is $(c - s)\, r / (1-r)$: zero if $s = c$, negative (a transfer to stayers) if $s > c$. The Swedish rule since July 2023 caps $s$ at the maximum stated in the fund rules (SEB 1 per cent, Storebrand 2 per cent, Nordea 1.75 per cent) and requires the applied factor to be disclosed in the annual report, which gives $s$ directly for the yes-funds.

### 3.5 Hypotheses (one table each)

H1, replication. Around OMXSB reconstitutions, additions earn positive and deletions negative abnormal returns from announcement to effective date; in the cross-section the effect increases in expected tracker demand scaled by ADV; whether it declines over 2013 to 2026 as tracker assets grew eightfold is the sub-question. Table 2.

H2, pressure and reversal. On FTN tranche days, abnormal returns are decreasing in the forced net sale scaled by ADV, with $\beta$ on the square-root prediction of order one, and the move reverses within 20 trading days. Table 3, Figure 3.

H3, anticipation. Part of the move happens between award, letter and the first tranche. Under predation the pre-tranche drift has the sign of the sale and the recovery exceeds the tranche-day move; under slow capital the drift is gradual and recovery slow; under sunshine trading the tranche-day move is smaller than equation (3) predicts. Table 4.

H4, incidence. On tranche days, losing funds without swing pricing show NAV returns below benchmark by about $c r / (1 - r)$; funds with swing pricing do not. Table 5.

Table 6 (cost-benefit) is arithmetic on H2 and H4.

## 4. Measures

### 4.1 Exposure

For stock $i$, fund $j$, tranche day $e$: the agency redeems a fraction $\rho_{je}$ of fund $j$'s assets $A_j$ (read from daily TNA and units, `data/exit_days/`). The fund's weight in $i$ is $w_{ij}$ from the last FI quarterly holdings report before the saver letter. Expected forced sale in SEK:

$$S_{ie} = \sum_{j \in \text{losers}} \rho_{je}\, A_j\, w_{ij}. \tag{5}$$

Destination purchases $B_{ie} = \sum_{k} m_{ke} w_{ik}$ with $m_{ke}$ the money arriving in winner $k$ around $e$ (from the PPM panel; winners buy at their own pace, so $B$ is dated to the month and spread evenly over its trading days in the main specification, with a zero-$B$ version as robustness). Net $F_{ie} = B_{ie} - S_{ie}$. Scaled dose in days of volume:

$$x_{ie} = \frac{F_{ie}}{P_i\, \text{ADV}_i}, \qquad \text{ADV}_i = \text{mean daily SEK volume over } [e-60, e-11]. \tag{6}$$

Both $x$ (net) and $x^S = -S/(P\,\text{ADV})$ (sell side) are reported with equal weight, as the blind referee required (file 08). Predicted impact from equation (3): $\hat\pi_{ie} = Y \sigma_{d,i} \sqrt{|x_{ie}|}\,\text{sign}(x_{ie})$ with $Y = 0.7$ and $\sigma_{d,i}$ from $[e-250, e-11]$.

Holdings staleness: the FI report after execution gives $w^{\text{post}}_{ij}$. The difference $w_{ij} - w^{\text{post}}_{ij}$ relative to $\rho_j$ shows whether the manager sold ahead (evidence for H3), and the pre-letter report is the instrument for the realised sale in a 2SLS version (Table 7).

### 4.2 Abnormal returns

Daily returns from LSEG or FinBas, dividends and corporate actions adjusted. Expected return from a four-factor model with Swedish factors (SHoF FinBas factors; fallback: Johansson, Sabbatucci and Tamoni 2025 tradable factors, which the grader built) estimated over $[-250, -31]$ relative to the first event day:

$$AR_{it} = R_{it} - \hat\alpha_i - \hat\beta_i' f_t, \qquad CAR_i[a,b] = \sum_{t=a}^{b} AR_{it}. \tag{7}$$

Standardised $SCAR_i = CAR_i / \hat\sigma_i \sqrt{b - a + 1}$ for the BMP test. Windows: replication $[\text{ann}, \text{eff}]$ and $[\text{eff}+1, \text{eff}+20]$ (with $\text{ann}$ being the announcement day itself before May 2021, when releases came pre-open, and the next trading day from May 2021); FTN award $[-1, +5]$, letter $[-1, +5]$, tranche $[-1, +1]$ per tranche and $[\text{first tranche}-1, \text{last tranche}+1]$ per round, reversal $[\text{last}+2, \text{last}+20]$ and $[+21, +40]$ where the calendar allows (small cap: 20 days only, pre-committed).

## 5. Estimation and inference

### 5.1 Replication (Table 2, Figure 2)

$$CAR_i[\text{ann},\text{eff}] = a + b\, \text{Add}_i + \gamma\, \text{Add}_i \times \frac{\text{TrackerAUM}_t \, \hat w_i}{P_i \text{ADV}_i} + \delta_t + \varepsilon_i, \tag{8}$$

by addition and deletion, by sub-period (four equal five-year periods of effective dates, 2007-2011, 2012-2016, 2017-2021, 2022-2026, the analogue of the anchor's four decades; changed 30 Oct 2026 from the earlier unequal cut 2007-2012, 2013-2017, 2018-2020, 2021-2023, 2024-2026, whose bins had no common rationale and made the per-period trend slope ill-defined; the announcement-lead regimes, intraday to 2012, pre-open 2013-2020, after-close from May 2021, are handled per event by moving AD to the next trading day, not by the period cut), and against tracker assets. Report mean CARs by sub-period beside Greenwood and Sammon's decade means (additions 3.4, 7.6, 5.2, 0.8 per cent; deletions -4.6, -16.6, -12.3, -0.6 per cent for the 1980s to 2010s, NBER WP Table 2) in one sentence of text, as the 2016 and 2024 winners did. Post-effective reversal $[\text{eff}+1, \text{eff}+20]$ in the same table.

### 5.2 FTN pressure (Table 3, Figure 3)

Unit: stock $\times$ tranche day (about 2,000 stock-days in Swedish active alone; most with small dose, which is the variation). Main specification:

$$CAR_{ie}[-1,+1] = \alpha_r + \beta\, \hat\pi_{ie} + \theta' Z_{ie} + \varepsilon_{ie}, \tag{9}$$

with round fixed effects $\alpha_r$, $Z$ = log market cap, past 12-month return, Amihud illiquidity, book-to-market, industry (ICB supersector) dummies. Test $\beta = 0$ and $\beta = 1$. Second column: dose $x_{ie}$ instead of $\hat\pi$. Third column: sell side only. Fourth: round-level windows $[\text{first}-1, \text{last}+1]$ with the cumulative dose. Reversal: same regressors on $CAR[\text{last}+2, \text{last}+20]$; the pressure story requires $\beta_{\text{rev}} \approx -\beta$.

Swedish index round: same equations, reported in its own row. The dose is 0.02 per cent of cap per tranche with predictable sign, so the pre-registered prediction is $\beta$ indistinguishable from zero with a confidence band that excludes the active-round estimate. It is a low-dose treated group, not a placebo, and will be called that.

### 5.3 Inference

Three things, all reported:

1. Standard errors clustered by tranche day (the common shock within a day), with the wild cluster bootstrap (Cameron, Gelbach and Miller 2008) because there are about 25 clusters across rounds.
2. Kolari and Pynnonen (2010) adjusted BMP statistic for the mean $SCAR$ on tranche days, which corrects for cross-sectional correlation of abnormal returns on a common event day; and a calendar-time portfolio (long low-dose, short high-dose stocks on tranche days) with Newey-West errors as the second check.
3. Randomisation inference: reassign $\hat\pi_{ie}$ across stocks within the same tranche day 2,000 times and report the share of placebo $|\beta|$ exceeding the estimate (Young 2019). This answers the common-shock objection that permutation within round does not, because the day is held fixed.

### 5.4 Power, computed before unblinding (`code/power.py` recomputes with the actual ADV)

Minimum detectable slope at 80 per cent power and 5 per cent size: $\text{MDE}_\beta = 2.8\, \sigma_{CAR} / (\sigma_x \sqrt{N})$.

- Tranche-day windows $[-1,+1]$: $\sigma_{CAR} \approx 3$ per cent for large caps (daily idiosyncratic volatility 1.7 per cent), 5 per cent for small caps. $N$: Swedish active about 200 names $\times$ 10 tranche days; small cap about 150 names $\times$ 4 to 6 tranche days (Oct 2026); Nordic active about 150 names $\times$ 3 days; the index round about 400 names $\times$ 10 days. Dose per stock-day: a 10 per cent tranche of a SEK 2bn fund is SEK 200m across 50 names, SEK 4m per name, which is 0.5 to 2 per cent of ADV for a large cap and 10 to 80 per cent for a small cap. Equation (3) then predicts impacts of 0.1 to 0.2 per cent for large caps (undetectable per day, detectable only in the round window) and 1 to 3 per cent for small caps (detectable per day).
- Round windows: Swedish active cumulative sell pressure 0.15 to 0.35 per cent of cap, which for cap/ADV around 500 is 0.75 to 1.75 days of volume spread over three weeks; equation (3) predicts about 1.2 per cent total. With $N = 200$, $\sigma_{CAR}$ over 15 days about 6 per cent, $\sigma_x \approx 0.6$ days: $\text{MDE}_\beta \approx 2.8 \times 6 / (0.6 \times 14) = 2.0$ per cent per day of volume, against a square-root prediction of about 1 per cent per day at $x = 1$. Borderline alone. Small cap: $N = 150$, $\sigma_{CAR} = 8$, $\sigma_x \approx 3$ days: MDE about 0.6 per cent per day against a prediction of 2 to 3 per cent. Well powered. Pooled with round fixed effects: adequate.
- Mean effect on the predicted-impact scale ($\beta = 1$ test): the standard error of $\hat\beta$ in equation (9) with $N \approx 2{,}500$ stock-days and $\sigma_{\hat\pi} \approx 0.5$ per cent is about $3 / (0.5 \times 50) = 0.12$, so $\beta = 1$ versus $\beta = 0$ is an eight-standard-error distinction if the law holds. This is the headline power statement for the thesis.
- Incidence (Table 5): index losers' daily tracking error 3 to 5 bp; predicted dilution per tranche $c r / (1-r)$ with $r = 0.08$, $c = 0.3$ per cent: 2.6 bp per tranche, 20 to 30 bp cumulated over ten tranches. With about 8 funds and 10 tranche days, the standard error of the mean daily effect is about 0.5 bp. Active losers: daily noise 30 to 50 bp against a benchmark; predicted 5 to 8 bp per tranche; with 18 funds and 2 to 3 tranches each the standard error is about 7 bp: underpowered on its own, reported beside the index result and pooled with the 2019 purge.

Every table reports its MDE in the note. The 2024 prize winner's null was accepted because the paper said what it could not detect; this thesis says it in advance.

## 6. Cost-benefit (Table 6)

Transition cost of round $r$ borne by moved savers: $\sum_{i,e} \hat\beta\, \hat\pi_{ie}\, S_{ie}$ (realised impact times SEK sold), plus the same for purchases. Borne by stayers: $\sum_j \text{dilution}_j (1 - r_j) A_j$ for non-swing funds. Benefit: the round's fee saving from file 06 fact 4 (178 MSEK a year across executed rounds; Swedish active 79, Swedish index 30). Report cost in SEK and in years of fee savings, with a band from the confidence intervals of $\hat\beta$ and the dilution estimate. Compare the agency's actual schedule (one to three tranches) with the Almgren and Chriss (2000) cost of spreading the same quantity over $n$ days under equation (3), which scales as $n^{-1/2}$: this quantifies what the staggering policy saved and is one paragraph.

## 7. Robustness (Table 7)

Placebo dates (same stocks, tranche days shifted by 30 and 60 trading days); OMXSB reconstitutions within 30 days of a tranche (flag and drop); holdings staleness (pre-letter versus post-execution weights; 2SLS); ADV window and volatility window; factor model (market model, 4-factor, grader's tradable factors); winsorising at 1 and 99; excluding the five largest-dose names; the 2024 European round as a one-day-per-fund sample.

## 8. What is pre-committed and what is left open

Pre-committed: windows, dose definitions, $Y = 0.7$, factor model, clustering unit, the four hypotheses with their tables, 20-day reversal for the small-cap round, index round reported as low-dose treated. Left open and to be settled with Klug on 17 Oct: whether the replication uses OMXSB alone or OMXSB plus OMXS30; whether the 2019 purge enters Table 5 as a pooled sample or an appendix; whether the cost-benefit is a table or a paragraph.
