# Revised plan (v2): SSZ anchor with Dahlquist and Martinez (2015) as the Swedish predecessor

Written 5 October 2026, late evening. This revises `FINAL_anchor_decision_2026-10-05.md` after the wide literature sweep (OpenAlex, Scopus, EconLit and Semantic Scholar, about 9,500 records; see `round3/outside_search_wide_2026-10-05.md`). Everything in the final decision still holds unless this file changes it. No thesis coefficient has been opened.

## 1. What changed and why

The sweep found **Dahlquist and Martinez (2015), "Investor Inattention: A Hidden Cost of Choice in Pension Plans?", European Financial Management 21(1), 1-19** (full text in `round3/dahlquist_martinez_2015_EFM.pdf`, notes in `round3/dahlquist_martinez_2015_notes.md`). None of the nine anchor reports cite it.

D&M run the comparison our headline test makes, on the same system: premium-pension money against retail money in the same 263 Swedish equity funds, quarterly, October 2000 to July 2008 (Table 2, p. 11, N = 8,663). Pension money barely reacts to last year's return rank. In SEK terms the gap is significant (Wald p < 0.001). In market-share terms it is not (p = 0.123 and 0.254), because the pension coefficient is imprecise (0.003, SE 0.012).

Three consequences:

1. **The direction of the headline result is not new.** The thesis cannot claim it.
2. **What remains open is still the thesis.** Nobody has a powered test with fund-level flows, the post-reform period (2020-2023), the sponsor interpretation, or the FTN column.
3. **The thesis gets a Swedish predecessor.** That answers risk S1 ("SSZ on Swedish data, off Klug's topic") better than any framing could.

The anchor stays SSZ (2015, JF). D&M is not a top-tier journal and has no sponsor or FTN dimension, so it enters as the direct predecessor and a second replication target.

## 2. Framing

**Working title (unchanged):** "Did the Premium Pension Need a Sponsor? Sticky Money before Fondtorgsnämnden"

**The three-step story:**
- SSZ: US pension money is *more* performance-sensitive than the other money in the same funds, and they credit plan sponsors, who drop bad funds.
- D&M: Swedish premium-pension money, with no sponsor, was *less* sensitive in 2000-2008.
- FTN: in 2024 Sweden got a sponsor. Was the gap still there just before, and how did the new sponsor choose?

**Contribution sentence (draft for the introduction):**
> Dahlquist and Martinez (2015) show that premium-pension money responded far less to past returns than retail money in the same funds in 2000-2008, although the gap is imprecise once flows are scaled by market size. We ask whether that gap survived the reforms of 2019-2022, estimate it with fund-level flows that have the power to separate the two groups, and read it through Sialm, Starks and Zhang's sponsor attribution, in the last years before Fondtorgsnämnden became the system's sponsor.

**Literature roles:**

| Paper | Role |
|---|---|
| Sialm, Starks and Zhang (2015, JF) | Anchor: specification, sponsor attribution, Tables I, III, VIII, IX |
| Dahlquist and Martinez (2015, EFM) | Swedish predecessor; robustness specification; conditional replication |
| Fricke, Jank and Wilke (2026, RFS) | Recency partner: clientele sensitivities within the same fund-quarter; sharpens S2 |
| Tran and Wang (2023, JFE); Kronlund, Pool, Sialm and Stefanescu (2021, JFE) | Recency partners (unchanged) |
| Evans and Fahlenbrach (2012, RFS; 2007 WP) | Mechanism: "market governance" vs "traditional governance" by a sponsor |
| Keim and Mitchell (2018, JPEF) | What a sponsor's removal round does to savers (closest analogue to an FTN round) |
| Koh and Mitchell (2010); Kavourakis and Tanewski (2026) | Public bodies curating or grading pension funds (Singapore, Australia) |
| Cookson, Jenkinson, Jones and Martinez (2021, RFS); Jenkinson, Jones and Martinez (2016, JF) | Gatekeeper selection, for Table 3 |

## 3. Specification changes

The headline test is **unchanged**: SSZ Table III difference, annual flow-years 2020-2023, linear percentile rank of prior-year SHoF return, year fixed effects, clustered by fund, Δ = β_PPM − β_nonPPM.

**Added, pre-registered before any coefficient is opened:**

1. **D&M robustness rows in Table 2.**
   - Quarterly, 2020Q1-2023Q4.
   - Absolute SEK flow and market-share flow, D&M eqs. (1)-(3).
   - Rank on one-year return, new-pension-money term (log TNA × contribution-quarter dummy), log TNA, one-year volatility, quarter intercepts.
   - PPM and non-PPM equations estimated as a system with pairwise bootstrap standard errors (1,000 replications).
   - Report D&M's 2000-2008 Systems I and III beside ours.
   - The PPM quarterly flow comes from summed monthly "Handel, netto". Non-PPM is SHoF TNA minus PPM capital.
2. **A D&M benchmark in Table 1.** Their Table 1 shares (PPS share of sample equity assets, 113.7 / (113.7 + 356.2)) next to ours.
3. **Recalibrated hypotheses** (section 4).
4. **Conditional appendix: replicating D&M Table 2 for 2001-2008.** Only if quarterly non-PPM fund assets for 2000-2008 arrive by the 1 November data freeze (SHoF, Svensk Fondstatistik via Fondbolagen, or FI). Otherwise it is dropped and the thesis says why in one sentence.

**Definitional difference to state.** D&M's retail assets come from Svensk Fondstatistik and cover only Swedish investors (their footnote 4). Our non-PPM money is total fund assets minus PPM capital, so it also includes foreign investors, occupational and unit-linked money, and funds of funds. Fricke, Jank and Wilke (2026) show funds of funds are the most performance-sensitive clientele. This raises β_nonPPM mechanically and pushes Δ negative regardless of any sponsor effect. It belongs in the S2 discussion, with the funds-of-funds robustness check and the holder-type request.

**Exhibit count stays five.** The D&M material goes inside Tables 1 and 2 and the appendix. No new table.

## 4. Hypotheses after recalibration (calibration only, no thesis data)

Converting D&M's market-share coefficients into SSZ-style fund-level annual units is rough. Multiply by the number of sample funds (230) to move from share of market assets to share of an average fund's assets, then by 4 to annualise. That gives:
- pension about 0.028 per unit rank per year;
- retail about 0.21;
- **an implied Δ of about −0.18 per year**, with a pension standard error of about 0.11.

This is close to the frozen point prediction for H_noSponsor (about −0.17 raw). The pre-analysis plan therefore keeps:
- **H_noSponsor:** Δ ≤ 0, point prediction about −0.17 raw (now cross-checked against D&M at about −0.18).
- **H_US:** Δ = +0.185 (SSZ OLS-equivalent); **H_US scaled:** Δ = +0.075.

The equal-size approximation ignores that D&M's sample is tilted to large funds, so treat −0.18 as an order of magnitude. Write the conversion and its caveat into the PAP.

**Pre-committed reading** (unchanged, with one addition):
- If the CI upper bound is below 0.075: reject the US pattern at Swedish scale.
- If the CI lower bound is above 0: a sponsor is not necessary.
- Otherwise: report the bound.
- A negative Δ is "consistent with SSZ's participants and with D&M's 2000-2008 evidence, not unique to the sponsor channel".
- **New:** a Δ near zero or positive means the 2000-2008 gap has closed. That is reported as a change since D&M, not as a failure.

## 5. Risks, updated

| # | Risk | Change |
|---|---|---|
| S1 | Read as "SSZ on Swedish data", off topic | **Reduced further:** the thesis now extends a Swedish paper by an SSE author on the same data |
| S2 | Non-PPM money is not non-DC | **Sharpened** by FJW (2026) and the D&M definitional difference. Add the funds-of-funds robustness check; keep the holder-type request |
| 16 | Novelty | **Changed:** the direction of the PPM gap is published (D&M). Novelty now rests on power, period, sponsor reading and the FTN column. DiVA and Riksrevisionen checks still pending |
| new | Specification search | Adding D&M rows after seeing results would look like fishing. **Solution:** they are in the PAP before any coefficient is opened |
| new | Scope creep | The 2001-2008 replication is conditional on data by 1 November and limited to the appendix |

All other risks and solutions in `FINAL_anchor_decision_2026-10-05.md` §5 stand.

## 6. Message to Klug (draft)

> Hi Michael,
>
> Before we freeze our pre-analysis plan we'd like your view on two things.
>
> First, the A/B choice. A: test Sialm, Starks and Zhang's sponsor attribution on premium-pension data for 2020-2023 (MDE about 0.10 per year against their +0.185), with FTN's first selections as a bounded "new sponsor" column. B: a pure FTN selection study without a replication, whose main test only detects near-perfect return-based selection. We lean towards A. Are you fine with narrowing the synopsis's fee and supply promises to descriptive statistics?
>
> Second, we found Dahlquist and Martinez (2015, EFM), which compares PPM and retail flows in the same funds for 2000-2008. We plan to treat it as our direct predecessor: their specification goes in as a robustness row on our period, and we replicate their main table for 2001-2008 if SHoF can give us pre-2018 fund assets. Our contribution would then be a powered test after the reforms, read through the sponsor lens, just before FTN. Does that framing work for you? Do you think Magnus Dahlquist would be open to a short comment on the plan?
>
> We'll send the timestamped plan as soon as it's frozen.
>
> Best,
> Alexander and Ludvig

## 7. What stays exactly as frozen

Sample rules (SEK equity funds; AP7 and merger-recipient fund-years dropped; flow-year 2019 dropped). SHoF ranks. Year fixed effects; fund clustering. Table 3 two-stage bid-level design with randomisation inference. Table 4 (SSZ Table IX). The drop list. No causal "introduction of a sponsor" language. Each claim states our number, the benchmark and the bound in one sentence.
