# Dahlquist and Martinez (2015): notes for the thesis

**Citation:** Dahlquist, M. and Martinez, J. V. (2015). Investor Inattention: A Hidden Cost of Choice in Pension Plans? *European Financial Management* 21(1), 1-19. doi 10.1111/j.1468-036X.2013.12008.x. First published online 29 May 2013. Working paper: EFMA 2012, paper 0095. JEL G11, G23, H55.

Read from the published PDF (`research/literature/papers/dahlquist_martinez_2015_EFM.pdf`). Page numbers refer to the journal.

## Question
Are premium-pension investors less attentive than retail investors in the same funds, and does that cost them? Attention is measured by the flow-performance sensitivity (pp. 2, 9).

## Data (pp. 6-8)
- **Pension side:** monthly PPS assets and returns per fund from the PPM, October 2000 to July 2008. Funds that were later closed are included. Only assets managed by investors themselves (96% of the PPS). The default fund is excluded because it is not sold to retail investors.
- **Retail side:** quarterly, from Finansinspektionen and Svensk Fondstatistik. Footnote 4: Svensk Fondstatistik assets cover **Swedish investors only**, pension and retail.
- **Returns:** from the PPM and Fondbolagens Förening. Net of fees, adjusted for the PPM fee rebates (0.53% average fee after rebate for active savers in 2007; 0.14% default; 0.16% administration fee).
- **Sample:** equity funds with at least one year of returns. 263 funds; 230 at March 2008, covering 86% of PPS equity assets and 58% of retail equity assets (Table 1, p. 8). Footnote 5: foreign-domiciled funds are lost for lack of retail data.

## Specification (pp. 9-10)
- Absolute flow (eq. 1): TNA_t − TNA_{t−1}(1 + R_t), SEK.
- Relative flow (eq. 2): absolute flow / **total assets of the whole market** (retail or PPS), in %.
- Flow over the fund's own TNA was tried; it gave "intermediate" results and is not tabulated (p. 9).
- Regression (eq. 3), quarterly: Flow = α_t + β·Performance_{t−1} + γ·NewPensionMoney_{t−1} + δ'Controls_{t−1} + ε.
  - Performance: rank of the raw one-year return, 0-1.
  - NewPensionMoney: log TNA × contribution-quarter dummy.
  - Controls: log TNA, one-year volatility; Systems II and IV add lagged flow.
- Retail and pension equations are estimated jointly as a system, with pairwise bootstrap standard errors (1,000 replications) that allow for heteroscedasticity and serial correlation.

## Table 2 (p. 11), N = 8,663 per system

| | I Retail | I Pension | II Retail | II Pension | III Retail | III Pension | IV Retail | IV Pension |
|---|---|---|---|---|---|---|---|---|
| Ranking | 0.064*** (0.014) | 0.007 (0.009) | 0.043*** (0.012) | 0.001 (0.008) | 0.023*** (0.005) | 0.003 (0.012) | 0.018*** (0.004) | 0.003 (0.012) |
| New pension money | | 4.394*** | | 5.029*** | | 8.205*** | | 8.587*** |
| Wald p (equal β) | <0.001 | | <0.001 | | **0.123** | | **0.254** | |
| Bootstrap percentile | <0.001 | | <0.001 | | 0.067 | | 0.133 | |

Panel A (I, II) is absolute flows in SEK billions; Panel B (III, IV) is relative flows in %. Risk-adjusted rankings give similar results (p. 12, not tabulated). Lagged flows shrink the gap (p. 12).

## Other results
- **Table 3 (p. 13):**
  - Bottom decile holds 9.18% of pension assets vs 6.88% of retail.
  - Pension flows into the bottom decile are +5.92% vs −0.74% for retail; adjusted gap −1.89 pp (SE 0.87).
- **Table 4 (p. 14):** pension investors hold more of the *subsequent* worst performers (10.47% vs 8.50%).
- **Table 5 (p. 15):** retail beats pension by 0.43-0.51% a year in alpha, not significant. Footnote 8: the realised difference is close to zero because PPM fee rebates offset the poorer choices. Fund momentum: top minus bottom quintile 8.7-8.9% alpha, significant.
- **Robur Contura** (section 2): about 90% retail in 2000; more than 60% PPS by 2009. 14% of active choosers still held it in 2009.

## Their explanation and policy idea
Pension investors are involuntary, keep the money in a separate mental account and are less sophisticated (p. 17). The default fund protects most inattentive savers (p. 16). They propose a "back to the default" clause for inactive savers (p. 17). They do not discuss plan sponsors, SSZ or a curated menu.

**Footnote 11 (p. 16), worth quoting in the thesis:** besides the fee reduction mechanism, they list as a protective feature "the mingling of pension and non-pension assets in the same funds", where inattentive pension investors may benefit from the market pressure of attentive investors. They also note that specialised advisers/account managers had emerged but were unstudied. That is the pre-2011 robot-switching market. Footnote 9 cites Cohen and Schmidt (2009) on less sensitive trustee flows in 401(k) plans.

## How the thesis uses it
1. **Predecessor:** cite it as the first evidence of the PPM gap; the contribution sentence builds on it.
2. **Robustness rows:** their specification on 2020Q1-2023Q4, Systems I and III at minimum, their 2000-2008 numbers beside ours.
3. **Calibration:** their market-share coefficients, converted to fund-level annual units (×230 funds, ×4 quarters), imply a pension-minus-retail gap of about −0.18 per year (pension SE about 0.11). The equal-size approximation is rough.
4. **Conditional replication** of Table 2 for 2001-2008 if quarterly non-PPM assets for that period arrive by 1 November.
5. **Differences to state:**
   - their retail = Swedish investors only, while our non-PPM = everyone else, including funds of funds;
   - their flows are scaled by market, ours by fund;
   - their period is the launch era, before the 2011 robot-switching rules and the 2019-2022 reforms.
