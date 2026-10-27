# Dossier for candidate (B): Cookson, Jenkinson, Jones and Martinez (2021) as the anchor

Prepared 5 October 2026 (round 1, resumed run). Paper: Gordon Cookson, Tim Jenkinson, Howard Jones and Jose Vicente Martinez, "Best Buys and Own Brands: Investment Platforms' Recommendations of Mutual Funds", Review of Financial Studies 34(1), January 2021, pp. 227-263, DOI 10.1093/rfs/hhaa057 (CJJM below).

Conventions.
- "p." is the printed page of the accepted manuscript (`research/anchor_review/sources/cookson_et_al_accepted_2019.pdf`, dated December 2019, SSRN 3024128). PDF page = printed page + 1. "txt L" is a line in `cookson_et_al_accepted_2019.txt`. Table 6 and Figure 1 are images; I read them from `cookson_work/t6-41.png` and `f1-45.png`.
- All Swedish numbers come from scripts in `scratchpad/anchor_final/round1/cookson_work/` (file list in the appendix).
- Labels: **VERIFIED** (checked against the cited source), **JUDGEMENT** (my reasoning), **NOT VERIFIED** (could not confirm).
- Blind rule: the power scripts print N, standard errors, MDEs (2.8 x SE) and dispersion moments only. No winner-minus-loser point estimate, selection coefficient or flow effect was printed or inspected.

---

## 0. Bottom line

- **Factual questions, all resolved (VERIFIED, section 1.4).**
  - The listing flow effect is 0.16% of total fund AUM per month (1.92% annualized, t = 5.42) in the full sample (Table 6, column 3, p. 40). After the ban it is 0.06% per month (t = 1.91, column 11).
  - The "about 1% of AUM per year" figure comes from an earlier, different version: FCA Occasional Paper No. 30 (August 2017), which used annual flows and Roman-numbered Tables I to X.
  - Deletion outflows last about two months: R+1 and R+2 in Figure 1A (p. 44), with only R+2 clearly below zero. They are gone by R+3, and the figure stops at R+4.
  - The performance split is by agreement with Morningstar analysts (Table 7 Panel B), not by affiliation. Affiliation and revenue share are descriptors in Panel C.
  - The tables are 1 to 8 and the figures 1 to 2. Internet Appendix tables IA.4, IA.6 and IA.7 are cited.
  - The published abstract matches the manuscript's. The published table contents are NOT VERIFIED (paywall).
- **Samples (section 2).**
  - P(win | bid): 290 bids, 75 winners, 11 rounds. Returns are available today for 142 bids (58 winners, 11 rounds).
  - P(win | qualified): 217 qualified bids. Qualified losers are identifiable only in the three Swedish rounds, where FTN reports that every bid met the requirements: 57 bids, 25 winners, 32 qualified losers; 49 have returns.
  - Elsewhere, 110 of 183 named losers qualified, but FTN does not publish which ones.
- **Power (section 5), MDE = 2.8 x SE, against CJJM's magnitudes.**
  - (i) Selection: a winner-minus-loser percentile gap of 15.0 points (1-year return) or 15.3 (3-year), against CJJM's 6.7 and 14.9 points (Table 4). Powered against a CJJM-sized 3-year gap only.
  - (ii) Outside-PPM flows: 3.5 to 4.7% of TNA over 3 months and 6.3 to 9.0% over 6 months, against CJJM-implied 0.48% and 0.96%. Not powered, by a factor of about 7 to 10.
  - (iii) Performance: 3.5% per year pooled, against CJJM's 0.60 to 0.94% per year. Not powered.
  - New: the savers' own (non-mechanical) PPM exits from removed funds between award and removal have MDE 0.8 to 1.5% of PPM capital in the first month (N 50 to 74 funds). That is powered against active-exit shares of a few percent.
- **Verdict (section 7, JUDGEMENT).**
  - (B) is the better fit for the FTN question: a gatekeeper's list, its selection, and voluntary versus default money. It is recent (RFS 2021), and it gives two clean powered pieces, the Table 5 selection model conditional on bidding and the Table 8 fee decomposition, plus one powered behavioural flow column inside Table 6.
  - (B) is weaker than (A) on replication. No CJJM table can be reproduced on comparable data (the FCA data are confidential), and CJJM's headline variables (affiliation, revenue sharing) have no FTN counterpart.
  - (B) fails if the examiner reads "replication" as reproducing the anchor's main exercise in comparable data, or if voluntary flows turn out to happen only inside the transfer month.

---

## 1. The paper: every equation, table and figure (VERIFIED unless marked)

### 1.1 Setting and data (Section 2, pp. 6-12)

- **Platforms.** Three UK direct-to-consumer platforms with a combined share above 50% of D2C assets under administration (p. 9, txt L495-511). Data were obtained by the FCA; platform identities are anonymous.
- **Data and unit.** Monthly data for 2006-2015. The unit is fund by platform. Share classes are aggregated into a "bundled" or "clean" group per fund (p. 10, txt L561-577; fn 9).
- **Sample.** Equity, fixed income, asset allocation and alternatives, GBP share classes, live and dead funds (pp. 10-11).
- **Affiliation and availability.** A fund is affiliated if it shares "branding name" or "advisor" with the platform (p. 11, txt L627-633). A fund is "available" on a platform if it has a revenue-share agreement and/or within-platform flows within three months (p. 11, txt L613-625).
- **RDR.** The ban on commission sharing applied to new business from 6 April 2014; the platforms switched to clean classes between February and April 2014; the sunset was April 2016 (p. 7, txt L407-425).
- **Recommendation criteria** stated by the platforms: past performance, risk, charges, process and manager tenure (p. 8, txt L448-452).

### 1.2 Equations

| Eq. (page) | Specification | Notes |
|---|---|---|
| **(1)** (p. 14, txt L777-807) | Logit: Prob(ACT_{p,f,t} = 1) = Λ(AFF_{p,f,t-1} β_AFF + RS_{p,f,t-1} β_RS + Z_{p,f,t-1} β_Z), where ACT is ADD (addition) or DEL (deletion) in month t | Z: pro-rated total cost over a 5-year holding period; 1- and 3-year performance percentiles on platform-specific returns in excess of Morningstar category benchmarks; turnover; log size; age; return sd; Morningstar 5-star dummy; Gold dummy; Gold/Silver/Bronze dummy; style x year FE. Separate logits for additions and deletions, for the full, pre-RDR and post-RDR samples. RS is dropped post-RDR. z-scores clustered by fund (p. 15, txt L824-832). Initial listings excluded (fn 13). |
| **Steady state** (p. 15; Appendix eqs. A.1-A.12, pp. 31-32) | Long-run share recommended = P_ADD / (P_ADD + P_DEL) (A.8). Favoritism means this share is larger for affiliated funds (A.9). A sufficient condition is β_AFF(add) ≥ 0 and β_AFF(del) ≤ 0, one of them strictly (Proposition 2) | Used to turn Table 5 into 14.56% vs 3.90% (pp. 16-17) |
| **(2)** (p. 20, txt L1128-1144) | Flow_{p,f,t} = REC_{p,f,t-1} β_REC + RS_{p,f,t-1} β_RS + Z_{p,f,t-1} β + ε, monthly | Flow is either the platform-specific GBP flow or the percentage flow = platform GBP flow / the fund's total net assets at the end of the previous year (pp. 19-20, txt L1107-1118; Table 6 caption). Fund-platform FE and calendar-year FE. GBP regressions use the TNA level; percentage regressions drop funds below GBP 10m TNA. t-statistics clustered by fund. A variant adds REC x AFF and REC x RS. |
| **Figure 1 specification** (p. 44 caption) | Eq. (2) for percentage flows plus leads and lags: R-4 to R-1 (before addition), R(F) to R(F+2) (first three months), RR (rest of listing), R(L-2) to R(L) (last three months), R+1 to R+4 (after deletion) | Panels B and C interact with affiliation and revenue |
| **Performance** (pp. 24-25, txt L1355-1410) | Three methods: (1) EW excess return over the Morningstar benchmark, recommended vs non-recommended, platform by platform; (2) within-category matching (160 level-2 categories); (3) one-factor alphas on category benchmarks, fund-by-fund residuals (Gerakos, Linnainmaa and Morse 2016) | Holding period "as long as listed" or five years from listing. Platform-specific net returns, assuming GBP 50,000 per account. Newey-West (2 lags) for the portfolio tests. |

### 1.3 Tables and figures

| Item (page) | Content | Sample / N | Headline numbers |
|---|---|---|---|
| **Table 1** (p. 36) | Platforms, funds, recommendations by year | 2006-2015 | 1,595 funds per platform on average, 45.2% of available funds, 74.9% of AUM; 111 recommended per platform (7.2%), falling from 11.5% (2006) to 3.5% (2015) |
| **Table 2** (p. 36) | Funds in platform vs not | Monthly obs | Age 12.63 vs 6.10 years; size GBP 0.25bn vs 0.08bn; 5-star share 12.77% vs 4.42%; fees 1.58 vs 1.52% (all differences p < 0.01, except turnover p = 0.09) |
| **Table 3** (p. 37) | By asset category | Per year | Equity 1,015 funds and 82 recommended per platform; fixed income 215/15; asset allocation 310/11; alternatives 55/3 |
| **Table 4** (p. 38) | Recommended vs not | 20,461 vs 309,714 platform-fund-months (pre-RDR 16,642 / 214,882; post 3,819 / 94,832) | Affiliated 3.79 vs 1.98% [0.03]; platform revenue 0.59 vs 0.54%; size GBP 1.09bn vs 0.21bn; fees 1.46 vs 1.56%; 5-star 30.94 vs 11.56%; Gold 18.04 vs 1.41%; Gold/Silver/Bronze 60.31 vs 14.00%; **prior 1-year percentile 55.76 vs 49.06 (gap 6.70); prior 3-year 63.44 vs 48.52 (gap 14.92)**, all p < 0.01 |
| **Table 5** (p. 39) | Eq. (1) logits | Additions: 100,474 / 66,090 / 34,017 obs. Deletions: 8,308 / 5,895 / 2,354 (all / pre / post) | Additions, affiliated: 1.15 (2.87)***, 0.75 (1.40), 2.95 (3.96)***. Deletions, affiliated: -0.57 (-1.17), 0.19 (0.37), -2.47 (-2.14)**. Additions, platform revenue: 1.92 (4.68)***, pre 2.32 (5.79)***. Additions: 5-star 1.27 (5.05)***; fees -0.99 (-2.47)**; 1-year percentile -0.54 (-1.32); 3-year 0.31 (0.63). Deletions: 1-year -0.62 (-2.07)**; 3-year -0.93 (-2.67)***; Gold/Silver/Bronze -0.52 (-2.27)**. Average marginal effect of affiliation on additions 0.0020 per month; deletions -0.0088 (all), -0.0290 (post). Pseudo-R² 0.07-0.17. Text: affiliated addition probability 0.0031 vs 0.0011; steady state 14.56% vs 3.90% (pp. 16-17) |
| **Table 6** (p. 40) | Eq. (2) | Columns 1-2: 107,459; 3-4: 95,896; 5-6: 72,089; 7-8: 64,353; 9-10: 35,405; 11-12: 31,560 | **Recommendation list:** GBP flows (1) 0.86 (5.13)***, (2) 0.80 (3.93)***; **percentage flows (3) 0.16 (5.42)***, (4) 0.14 (2.63)***.** Pre-RDR: (5) 0.75 (3.88)***, (6) 1.14 (4.20)***, (7) 0.11 (3.16)***, (8) 0.10 (1.40). Post-RDR: (9) 0.25 (1.52), (10) 0.31 (1.83)*, **(11) 0.06 (1.91)***, (12) 0.08 (2.71)***. Rec x affiliated: -0.85 (-3.69)*** (2), -0.21 (-3.34)*** (4). Rec x revenue insignificant. Morningstar Gold and Gold/Silver/Bronze: no significant direct effect (e.g., (3): -0.02 (-0.66), 0.01 (0.76)). R² 0.01-0.03 |
| **Figure 1** (p. 44) | Event-time marginal effects, % flows | Same as (2) | Read from the figure, so approximate. Leads R-4 to R-1 about +0.09, +0.10, +0.09, +0.06, with 95% CIs above zero. R(F) to R(F+2) about +0.23, +0.24, +0.22; RR about +0.19; R(L-2) to R(L) about +0.15, +0.13, +0.17. **R+1 about -0.10 (CI includes 0); R+2 about -0.17 (CI about -0.29 to -0.05); R+3 about -0.02 and R+4 about -0.04 (CIs include or touch 0).** Panel C: high-revenue funds R+1 about -0.43 |
| **Table 7A** (p. 41) | Recommended vs non-recommended performance, % per year | Portfolio tests, Newey-West | Listed holding period. Recommended 0.08% (0.11) vs non-recommended -0.86% over benchmark. **Recommended minus non-recommended: 0.94% (3.75)*** (vs benchmark), 0.60% (2.88)*** (within category), 0.80% (3.49)*** (one-factor alpha).** Five-year holding: 0.83, 0.48, 0.63. Pre-RDR 0.88 / 0.61 / 0.85; post-RDR 1.29 / 0.63 / 0.72 |
| **Table 7B** (p. 42) | Split by **agreement with Morningstar**: platform and Morningstar; platform only; Morningstar only | One-factor alphas, within category | Listed, all. Platform and Morningstar (Gold/Silver/Bronze) 1.29% (5.80)***; Gold 1.77% (4.30)***. **Platform but not Morningstar 0.34% (0.71).** Morningstar but not platform 0.70% (3.25)***, Gold 1.36% (2.78)***. Post-RDR platform-only 0.81% (2.17)** |
| **Table 7C** (p. 42) | Affiliation and revenue across the 7B groups | Panel, clustered by fund | Platform-only picks: affiliated 5.44% vs 1.66% for non-recommended, difference 3.78 (2.89)***; revenue difference 0.09 (8.41)***. Morningstar picks: affiliation difference -0.08 (-0.17) |
| **Table 8** (p. 43) | Fees and platform revenue around RDR, % per year | Clustered by fund | (A) All funds: fees -0.33, revenue -0.18, difference -0.15; all UK funds -0.17. (B) Same funds before and after: -0.26 / -0.16 / -0.10 / -0.11. (C) Funds only after vs only before: -0.55 / -0.23 / -0.32 / -0.37. (B) - (C) = 0.29 / 0.07. All p < 0.01 |
| **Figure 2** (p. 45) | Fees and platform revenue over time, 2006-2015 | Year-end | Illustration; pre-RDR 2006-2013, post 2014-2015 |
| **Internet Appendix** (cited) | IA.4: Morningstar analysts' additions/deletions, with no affiliation or rebate effect (p. 19, txt L1062-1066). IA.6, IA.7: within-style ranks and fund-time FE for flows (fn 21) | | **NOT VERIFIED**: IA not in hand |

### 1.4 The five factual questions

1. **Listing flow effect: 0.16% per month, not "about 1% per year". VERIFIED.**
   - Table 6 col. (3): 0.16 (t = 5.42), full sample. Col. (11): 0.06 (t = 1.91), post-RDR. Intro p. 4 (txt L223-227) and p. 21 (txt L1175-1181): "0.16% (1.92% once annualized) of the overall assets managed by that mutual fund".
   - The denominator is the fund's total AUM; the flow is through one platform. Fn 22 (p. 21): with 15-20% platform shares, "if all the platforms were to recommend a mutual fund that would result in a 9.6% to 13.8% asset flow once annualized".
   - **Manuscript inconsistency:** the text on p. 21 cites "column (4)", but 0.16 is in column (3). Column (4) is 0.14 with the interactions. Cite column (3).
   - **Source of "1% per year":** FCA Occasional Paper No. 30 (August 2017), an earlier annual-frequency version. It says the fund "experiences an average inflow of GBP5.9 million, equating to 1% of the total assets under management" per year, and numbers its tables I to X (fetched from fca.org.uk via WebFetch, 5 Oct 2026). That version is not the RFS paper.
2. **Duration of deletion outflows: about two months. VERIFIED from Figure 1A, approximate reading.**
   - R+1 (about -0.10) is not significant; R+2 (about -0.17) is significant; R+3 and R+4 are near zero. The figure covers only four months after removal.
   - Text p. 21 (txt L1189-1193): "Net flows then experience a significant drop, even compared to pre-recommendation levels, when the fund is removed".
   - There is no multi-year outflow evidence in the paper.
3. **Performance split: by agreement with Morningstar analysts (Table 7B). VERIFIED.**
   - Affiliation enters only as the descriptive Panel C: platform-only picks lean own-brand and high-revenue.
   - Platform-only picks do not outperform in the full and pre-RDR samples (0.34%, t = 0.71). Post-RDR they do (0.81%, t = 2.17; pp. 26-27, txt L1463-1477).
4. **Table numbers: Tables 1 to 8 (Arabic), Figures 1 to 2. VERIFIED.** Listing logit = Table 5; flows = Table 6; performance = Table 7; fees = Table 8. There are no Tables IX or X; those are FCA OP30 numbering.
5. **Published RFS version vs manuscript.**
   - VERIFIED from the ORA record (ora.ox.ac.uk, uuid:84450809...) and a SUFE newsletter reprint:
     - accepted 28 January 2020, published online 20 May 2020, RFS 34(1) 227-263;
     - the published abstract is the manuscript's with copyedits ("on-line" to "online", "U.K." to "United Kingdom").
   - **NOT VERIFIED:** published table contents and page numbers (OUP returned 403 to the container; WebFetch saw only the header). Our file is dated December 2019, one month before acceptance, so the numbers are probably final. Check the published PDF on the SSE network before citing published page numbers.

### 1.5 What CJJM conclude (pp. 29-30)

Platforms favour own-brand and high-commission funds. Investors discount own-brand recommendations, but not high-commission ones (which are unobservable). Recommended funds beat non-recommended ones, but only picks that agree with Morningstar add value before the ban. RDR cut costs, mostly by replacing expensive funds.

---

## 2. Bidders and the true samples

### 2.1 Round table (`cookson_work/bidders.csv`, finalised this run)

Verified against §5.3-5.5 of each FTN report (`scratchpad/ftn_txt/`).

Corrections made this run:
- Sweden active `fee_before_pct` changed from 0.303 to **0.309**. The report's §6.2 says "0,309 procent ... 0,154 procent". All other fees match.
- Global index: 11 qualified, all 11 called to interview, and 1 withdrew when interviews began (L713-715), so 10 were interviewed. The withdrawer is counted as a qualified loser.
- New columns added: named losers, qualified losers identified, qualified share of losers, identifiability, and a verification note. The old file is in `bidders_v0_backup.csv`.

| Round | Bids | Winners | Named losers | Qualified losers | Identifiable? | Fee before → after (%) | Change (bp) |
|---|---|---|---|---|---|---|---|
| Europe active 2024 | 35 | 6 | 29 | 6 | No (23 rejected, unnamed) | 0.48 → 0.21 | -27.0 |
| Europe index 2024 | 12 | 4 | 8 | 6 | No | 0.135 → 0.046 | -8.9 |
| Global index 2024 | 18 | 6 | 12 | 5 | No | 0.143 → 0.046 | -9.7 |
| Nordic large/mid 2025 | 17 | 4 | 13 | 11 | No (2 rejected) | 0.326 → 0.204 | -12.2 |
| Nordic small 2025 | 10 | 4 | 6 | 5 | No (1 rejected) | 0.515 → 0.244 | -27.1 |
| **Sweden active 2025** | 22 | 10 | 12 | 12 | **Yes**: "Alla inkomna anbud uppfyllde kraven" (L714) | 0.309 → 0.154 | -15.5 |
| **Sweden passive 2025** | 16 | 5 | 11 | 11 | **Yes**: "Alla anbud uppfyllde kraven" (L674-676) | 0.129 → 0.039 | -9.0 |
| Global active 2026 (under appeal) | 99 | 14 | 85 | 55 | No (20 rejected, 10 withdrawn, L1288) | 0.371 → 0.186 | -18.5 |
| Europe small 2026 | 15 | 4 | 11 | 8 | No | 0.398 → 0.321 | -7.7 |
| **Sweden small 2026** | 19 | 10 | 9 | 9 | **Yes**: "Samtliga 19 anbud uppfyllde de obligatoriska kraven" (§5.3) | 0.339 → 0.197 | -14.2 |
| Technology 2026 | 27 | 8 | 19 | 14 | No | 0.396 → 0.194 | -20.2 |
| **Total** | **290** | **75** | **215** | **142** | **32 identified** | | |

- Every bidder is named (manager and fund) in §5.2 of each report.
- Losers' status (rejected, qualified, interviewed), losers' scores and losers' bid prices are not linked to names.
- The 2026 reports print anonymous dots with the price and quality scores of evaluated bids. They cannot be linked to identities.
- ISINs are published for winners only.

### 2.2 Can losers' qualification be identified? (VERIFIED)

- **Fully, in three rounds:** Sweden active 2025, Sweden passive 2025 and Sweden small 2026. FTN states that every bid met the requirements, so every named loser is a qualified loser: 57 bids, 25 winners, 32 qualified losers.
- **Not otherwise.** In the other 8 rounds, 110 of 183 named losers qualified, but the reports do not say which ones. The qualified share of named losers ranges from 21% (Europe active) to 85% (Nordic large/mid).
- **The rejection counts per round are known.** That supports bounds (section 6, risk 6), not point identification.

### 2.3 Matching bids to Morningstar and SHoF (`cookson_power.py` writes `bids_long_final.csv`)

| Group | Bids | Morningstar fundid | SHoF return id | 12-month return | 36-month return |
|---|---|---|---|---|---|
| Winners | 75 | 72 | 62 | 58 | 57 |
| Losers, PPM incumbents | 66 | 66 | 65 | 65 | 63 |
| Losers, not in PPM | 149 | 82 | 19 | 19 | 19 |
| **Total** | **290** | **220** | **146** | **142** | **139** |

- **Matching methods** (`shof_map.py`): ISIN for 127 bids; token-Jaccard name match at 0.95 or above for 97. Inspected by hand.
- **Four doubtful name matches set to missing:** Carnegie Small & Micro Cap; Indecap Guide Sverige Småbolag; Nordea 2 Global Responsible Enhanced Equity; FTGF ClearBridge Global Growth Leaders.
- 38 weak and 28 unmatched names remain, almost all non-PPM losers.
- **Bottleneck:** returns exist for only 19 of 149 non-PPM losers, because the SHoF download covered PPM-related ids only.

### 2.4 The true samples

| Estimand | Population | Identified today | With returns today |
|---|---|---|---|
| P(win \| bid), CJJM eq. (1) analog | 290 bids, 75 winners, 11 rounds | 290 | 142 (58 winners, 11 rounds); 110 (52 winners, 10 rounds) excluding the appealed global active round |
| P(win \| qualified) | 217 (75 winners + 142 qualified losers) | 57 (25 winners + 32 losers, 3 rounds) | 49 (23 winners) |
| Winners vs qualified losers | 75 vs 142 | 25 vs 32 (3 Swedish rounds) | 23 winners / 26 losers with 12-month returns |
| Bid vs did not bid (CJJM Table 2 analog) | Incumbent funds in procured categories (SSZ `ftn_cross_section.csv`, 108 PPM fund numbers, R1-R4 and R6) | Of 66 removed PPM classes (R1-R4): **38 bid and lost, 26 never bid, 2 belong to funds that won with another class** (`ssz_cross_section_fundlevel.csv`) | |

---

## 3. Mapping CJJM to the Swedish data

### 3.1 Table by table

| CJJM exhibit | Swedish counterpart | N available now | Status |
|---|---|---|---|
| Table 1 / 3 (descriptives) | Round table: bids, qualified, winners, capital, fees (2.1) | 11 rounds | Adaptation, complete |
| Table 2 (offered vs not) | Incumbents that bid vs did not bid | 66 removed + 21 incumbent winners (R1-R4); +12 R6 losers still listed in Aug 2026 | Adaptation |
| Table 4 (recommended vs not) | Winners vs losers vs non-bidders: returns, fees, size, age, risk | 142 bids with returns | Adaptation. Morningstar stars and Medalist ratings are **not in the data** (no rating fields in `fundmaster.pkl` or `shof_field_definitions.txt`) |
| Table 5, eq. (1) | Cross-sectional logit/LPM of win on lagged covariates, round FE | 142 (all bids), 49 (all-qualified rounds) | Adaptation. One decision per fund-round, not a monthly hazard. **AFF and RS have no FTN counterpart**: FTN is unconflicted, like CJJM's Morningstar benchmark (IA.4) |
| Table 6, eq. (2), inside PPM, transfer months | Rule-based transfers (equal split up to the level of other winners; incumbents keep their capital; defaults) | All rounds | **Mechanical; not CJJM's object.** Report as the dose only |
| Table 6, inside PPM, voluntary windows | (a) Removed funds' PPM net trading between award and removal; (b) winners' PPM net trading from transfer month + 2 onward | (a) 74 of 78 losers (50 with PPM capital of at least SEK 100m); (b) 32 winners, 7 rounds | **Behavioural adaptation of eq. (2) and Figure 1** |
| Table 6, outside PPM | (Fund TNA flow − PPM net trading) / lagged TNA, SEK-currency funds | 3-month window: 27 winners / 38 losers, 10 rounds. 6-month window: 16 / 24, 8 rounds | Extension column (CJJM only observe platform flows) |
| Table 7A | Within-round (= within-category) winner-minus-loser returns, calendar time, SHoF `tri_sek` | 11 rounds; post-award months to Sep 2026: 0 (technology) to 30 (Europe active) | Adaptation |
| Table 7B/C | FTN picks vs Morningstar Medalist picks | 0 (no ratings in hand) | Not possible without Medalist/star history |
| Table 8 | Category fee before/after (A); same funds: incumbent winners' old fee vs procured fee (B); replacement: removed funds vs new winners (C) | 11 rounds (A, from FTN reports); B and C from PPM `Fondstatistik` fees and FTN procured fees (75 winners in `winners.csv`) | **Adaptation, exact (no sampling error in A)** |

### 3.2 Real moments of outside-PPM flows, monthly, 2018-2023

Definition: (imputed TNA flow − PPM `nt`) / TNA_{t-1}, in percent. Funds with SEK fund currency only. Lagged TNA must be at least SEK 100m (CJJM drop funds below GBP 10m). Winsorized at 1%/99%.

| Sample (script) | Funds | Fund-months (AR(1) sample) | sd | Within-fund sd | Within AR(1) | Mean |
|---|---|---|---|---|---|---|
| All SEK PPM funds (`moments.py`, PPM-fund level) | 355 | 16,905 | 3.12 | 3.00 | 0.149 | 0.07 |
| same, excluding December | 355 | 14,257 | 3.08 | 2.95 | 0.139 | 0.10 |
| SEK equity-type PPM funds | 217 | 10,204 | 3.00 | 2.88 | 0.152 | -0.03 |
| FTN bidder funds (SEK) | 98 | 4,978 | 2.25 | 2.11 | 0.155 | 0.16 |
| FTN winner funds (SEK) | 42 | 2,386 | 2.16 | 2.02 | 0.105 | 0.07 |
| FTN bidder funds, Morningstar-fund level incl. non-PPM months (`cookson_power.py`) | 118 | 7,112 | 2.97 | 2.83 | 0.159 | not printed |
| Cumulative 3-month / 6-month outside flow, bidder funds | 118 | | median within-fund sd 4.00 / 5.97 | | | |

- Unwinsorized sd is about 11% per month, so the tails are fat (mergers, launches).
- 60% of bidder fund-months have monthly TNA only (`ndays` of 2 or less); this is why flows are imputed from TNA.
- The median PPM share of fund TNA is 0.16 overall, 0.23 for bidders and 0.30 for winners.
- **Agreement with the SSZ dossier:** its monthly non-PPM flow sd of 2.83% (normalized by non-PPM assets) matches ours.
- **Comparison with the pressure test:** it assumed sd 3 to 5% and AR(1) 0.3. The real figures are sd 2.0 to 3.1% and AR(1) 0.10 to 0.16.

---

## 4. The strongest Cookson-anchored thesis

### 4.1 One question

**How much of a public fund list's effect on savers' money comes from savers acting on it voluntarily, rather than from the default transfer?**

JUDGEMENT on why this question is interesting whatever the answer:
- CJJM's 0.16% per month is purely voluntary: UK investors are free to ignore the list. FTN lets the same list effect be split into a default part and a voluntary part.
- A large voluntary response means certification by an unconflicted gatekeeper persuades.
- A zero voluntary response means FTN's reallocation is all inertia. That would be the first list setting where the influence CJJM document is fully mechanical, consistent with PPM inertia (Cronqvist and Thaler 2004; Dahlquist, Martinez and Söderlind 2017 RFS).
- What FTN selects on (Table 5 analog) defines what is being certified. Fees (Table 8) give the price side.

### 4.2 Adaptation tables (labelled "adaptation", never "replication")

1. **T1 (CJJM T1/T3):** rounds, bids, qualified, winners, capital, fee before and after (section 2.1).
2. **T2 (CJJM T2):** incumbents that bid vs did not bid (38 bid and lost, 26 never bid, 2 won through another class, plus incumbent winners); size, age, fee, returns.
3. **T3 (CJJM T4):** winners vs losers vs non-bidders, with CJJM's 1- and 3-year percentile gaps (6.70, 14.92) printed beside ours.
4. **T4 (CJJM T5, eq. 1):** P(win | bid), logit and LPM, round FE, covariates as in CJJM's Z (fees, 1- and 3-year percentiles, log size, age, return sd), plus incumbency. Panel B: P(win | qualified) in the three all-qualified rounds.
5. **T5 (CJJM T6, eq. 2, and Figure 1):** event-time PPM flows, month-adjusted.
   - Losers, award to removal (voluntary exits; CJJM's R+1, R+2).
   - Winners, transfer + 2 to + 7 (CJJM's RR).
   - Transfer months shown separately as the mechanical dose.
   - Leads (-4 to -1) as in Figure 1.
6. **T6 (CJJM T7A):** within-round winner-minus-loser returns, calendar time, reported as a bounded result with its MDE.
7. **T7 (CJJM T8):** fees, rows A (category), B (same funds) and C (replacements), beside CJJM's -0.33 / -0.26 / -0.55.

### 4.3 The extension inside CJJM's tables

- **Table 6 gets three columns where CJJM have one:**
  - PPM voluntary;
  - PPM mechanical (dose);
  - outside PPM (spillover to money that never sees the list).
- **Table 5 gets the bid margin:** CJJM condition on "available on platform" (Table 2), and FTN adds the fund's own decision to bid.
- **Covariates:** none of CJJM's conflict variables exist here. The "affiliation" column becomes a falsification: incumbency or Swedish bank-group manager should not predict winning for an unconflicted gatekeeper, the counterpart of CJJM's IA.4 result for Morningstar.

### 4.4 Predicted signs (JUDGEMENT, written before any estimate)

| Estimate | Sign | Reasoning |
|---|---|---|
| T4: 3-year percentile | + | FTN prints winners' 3-year Sharpe and information ratios; "Investeringsresultat" is a quality subcriterion. CJJM Table 4 gap is +14.9 |
| T4: 1-year percentile | about 0 | CJJM additions: -0.54 (n.s.) once 5-star is controlled |
| T4: current fee | − | Cost is 25% of the score, and the current fee correlates with the bid price |
| T4: log size, age | + | Manager resources and the 3-year track-record requirement |
| T4: incumbency, bank-group manager | 0 | No conflict; falsification |
| T5: losers' PPM flow, award to removal | − | Letters and active choice; reported default acceptance 85-95% (brief; NOT VERIFIED) implies 5-15% active choosers, some acting early. CJJM R+1 and R+2 negative |
| T5: removed non-bidders vs bid-and-lost | Same sign and size | Savers see "removed", not why |
| T5: winners, transfer + 2 onward | + | Listing (CJJM RR about +0.19), but inflated by the menu shrinking to winners (risk 4) |
| T5: leads before award | 0 or + | CJJM leads are positive (+0.06 to +0.10); FTN may pick funds with momentum flows |
| T5: outside PPM | about 0 | Outside investors do not see the PPM list. CJJM: Morningstar ratings have no direct effect on platform flows (Table 6, col. 3) |
| T6: winners minus losers | about 0 gross | Berk and Green; selection on process and cost; the fee cut accrues to the PPM class only |
| T7: fees | − in all rows; B smaller than C in active categories | CJJM's B (-0.26) is smaller than C (-0.55); replacements are cheaper share classes |

### 4.5 Handling the three structural problems

- **Mechanical PPM flows.** Flows are never measured in transfer months. Removal and transfer months (`nt` at or below -60% of PPM capital) are dropped. Voluntary flows are measured only:
  - between award and removal for losers;
  - from transfer + 2 for winners.
  The dose is reported separately, like SSZ's sponsor flow. A Pensionsmyndigheten ledger by transaction type would turn this from a window design into a direct split.
- **No list before 2024.** There is no pre-2024 replication of a list effect, and I do not pretend otherwise. The 2018-2023 panel is used as:
  - the placebo distribution: the same statistics at award dates shifted back 24, 36 and 48 months give the SEs in section 5 and support randomization inference;
  - the pre-period for the event-time leads.
  The 2019 re-registration is not used; the pressure test's reasons to drop it stand.
- **Unidentifiable qualified losers.**
  - The headline estimand is P(win | bid), which needs no qualification status.
  - Winners vs qualified losers runs on the three all-qualified rounds (25 vs 32).
  - Elsewhere, trimming bounds use the known number of rejected bids per round (2.1).
  - A request under offentlighetsprincipen for per-bid status and scores.

---

## 5. Minimum detectable effects (2.8 x SE, real data)

Scripts: `cookson_power.py`, `ppm_pretransfer_power.py`, `post_transfer_power.py`. SEs are HC1 with round FE (cross-sections), or come from placebo distributions. Power against CJJM is computed as Φ(effect/SE − 1.96).

| Test | N | SE | MDE | CJJM magnitude | Approximate power vs CJJM |
|---|---|---|---|---|---|
| **(i) Selection: winner-minus-loser 3-year percentile gap**, all bids | 139 (57 winners, 11 rounds) | 5.5 pts | **15.3 pts** | Table 4: 14.92 pts | about 77% |
| (i) same, 1-year percentile | 142 (58 winners) | 5.4 pts | **15.0 pts** | Table 4: 6.70 pts | about 24% |
| (i) LPM, worst-to-best change in P(win), 1-year | 142 | 0.141 | 0.40 | Table 5 is a monthly hazard, not comparable | |
| (i) PPM-incumbent bids only, 3-year gap | 102 (39 winners) | 6.9 | 19.3 | 14.92 | about 58% |
| (i) Excluding global active (appeal), 3-year gap | 107 (51 winners) | 6.1 | 17.0 | 14.92 | about 69% |
| (i) All-qualified rounds, P(win \| qualified), 3-year gap | 46 (22 winners, 3 rounds) | 9.0 | 25.2 | 14.92 | about 38% |
| **(ii) Outside-PPM flow, 3 months, DiD (post − pre)**, placebo cross-sections | 104 (47-49 winners, 11 rounds) | 1.25-1.29 | **3.5-3.6% of TNA** | 0.16 x 3 = 0.48% (full); 0.18% (post-RDR) | about 6%; about 5% |
| (ii) same, at the real available N | 58-65 (27 winners) | 1.67 | **about 4.7%** | 0.48% | about 5-6% |
| (ii) 3 months, post only (no pre-window) | 104 | 0.88-1.02 | 2.5-2.9% | 0.48% | about 7% |
| **(ii) Outside-PPM flow, 6 months, DiD** | 94-99 (41-47 winners) | 2.24-2.62 | **6.3-7.3%** | 0.96% (full); 0.36% (post-RDR) | about 6% |
| (ii) same, at the real available N | 30-40 (14-16 winners) | 3.22 | **about 9.0%** | 0.96% | about 5% |
| **(iii) Performance: pooled calendar-time winner-minus-loser** | 11 rounds, T = 30 months | 0.106% per month (1.27% per year) | **0.30% per month = 3.5% per year** | Table 7A: 0.60 (within category), 0.80 (alpha), 0.94 (vs benchmark) % per year | about 7-11% |
| (iii) single rounds with at least 13 post months | 4-12 winners vs 2-12 losers | | 3.0-9.1% per year | same | below 10% |
| **(iv) Voluntary PPM exits from removed funds, award + 1 month** | 50 losers (PPM capital ≥ SEK 100m) / 74 (≥ SEK 10m) | 0.28 / 0.54 | **0.77 / 1.51% of PPM capital** | CJJM R+1 and R+2: -0.10 and -0.17% of fund AUM per platform. Scaled by a 15-20% platform share this is about -1.4 to -1.8% of platform capital over two months (JUDGEMENT: rough conversion; CJJM do not report the platform's share of each fund's AUM, so this borrows fn 22's market shares) | about 95% (≥ SEK 100m sample) or 46% (≥ SEK 10m) for an early-exit effect of 1% of PPM capital |
| (iv) same, award + 2 months | 50 / 74 | 0.47 / 0.80 | 1.32 / 2.23% | as above | about 89% / 47% for a 1.5% effect |
| **(v) Winners' PPM flow, transfer + 2 to + 7, month-adjusted** | 32 winners, 7 rounds | 0.24% per month | **0.67% per month of PPM capital** | CJJM RR about +0.19% of fund AUM per platform; about 1.0-1.3% of platform capital (same rough JUDGEMENT conversion) | high if the conversion holds; inflated by the menu effect |
| (vi) Fees (T7, row A) | 11 categories | none (population) | n/a | -33 bp (A), -26 (B), -55 (C) | exact: -7.7 to -27.1 bp per category |

Notes:
- (ii) excludes nothing in transfer months. The SSZ reconciliation (median |residual| 34.6% of the PPM transfer, `ssz_work/reconcile_winners.csv`) means real SEs in transfer months are larger still.
- (iii) assumes independent rounds, which understates the SE if rounds co-move.
- (iv) and (v) month-adjust by subtracting the cross-sectional median PPM flow, which absorbs the pro-rata December placement. The placebo sd is 1.95 to 4.62% (1 month).
- Summary: **powered** are (i) against a CJJM-sized 3-year gap, (iv), probably (v), and (vi). **Not powered** are (ii) and (iii), which are bounded nulls at best.

---

## 6. Risks and solutions

| # | Risk | Solution | Fully solves or reduces? |
|---|---|---|---|
| 1 | **No table is reproducible on CJJM's data** (FCA, confidential, platforms anonymous; p. 9). The course standard is "replication and extension" and "replicating the main quantitative exercise" (course_intro.txt L142, L272). | Reproduce CJJM's specifications exactly (eq. 1 covariates, eq. 2 with fund FE and time FE, Figure 1 leads and lags, the Table 8 A/B/C decomposition) on FTN data, labelled as adaptations, and print CJJM's numbers in a side column. The course lists "different dataset, application" as extensions (L148). | Reduces. It cannot be fully solved. |
| 2 | **Main exercise (Table 6) has no clean counterpart:** inside PPM is mechanical; outside PPM is unpowered (MDE 8-10 times CJJM). | Use voluntary windows (section 4.5) as the Table 6 headline; outside PPM is a bounded column. | Reduces |
| 3 | **CJJM's headline variables (affiliation, revenue share) have no FTN counterpart**, so the "own brands" result cannot be tested. | Turn it into a falsification (incumbency or bank-group manager should be 0); the FTN analog is CJJM's Morningstar benchmark (IA.4). | Reduces |
| 4 | **Menu effect:** after removal, the category menu is the winners, so any active chooser in the category must pick a winner; post-transfer inflows are partly mechanical. | Report winners' share of the category's voluntary inflow against their capital share; compare with non-procured categories in the same months; make (iv), the loser exits, the headline. | Reduces |
| 5 | **No list before 2024.** | Placebo dates from 2018-2023 for inference (randomization inference); event-time leads; no claim of a pre-2024 list replication. | Reduces |
| 6 | **Qualified losers are unidentified in 8 of 11 rounds.** | (a) Headline P(win \| bid). (b) Three all-qualified rounds for P(win \| qualified). (c) Lee-type trimming bounds: in round r, drop the k_r most and least favourable losers, with k_r = rejected bids (2.1). (d) Request per-bid status and scores from FTN under offentlighetsprincipen. Secrecy under OSL 19:3 should lapse after the award decision; NOT VERIFIED that FTN releases scores. | Fully solves if (d) is granted; otherwise reduces |
| 7 | **Returns missing for non-PPM losers** (19 of 149) plus 66 weak or unmatched names and 4 doubtful matches set to missing, which bias the bid sample toward PPM incumbents. | Request SHoF series for the 82 matched non-PPM loser fundids; match the remaining names by ISIN from fund websites or prospectuses. | Fully solves coverage for matched funds; reduces overall |
| 8 | **CJJM covariates missing:** Morningstar stars and Medalist ratings (not in hand); losers' bid prices (not published). | Request historical ratings from SHoF / Morningstar Direct; use the current share-class fee as a proxy for the bid price, and say so. | Reduces (fully for ratings if delivered) |
| 9 | **Outside-PPM measurement:** SEK-only (`tnafund` is in fund currency); TNA-only Swedish funds; reconciliation error in transfer months. | Riksbank FX for non-SEK funds; an award-to-admission window with no transfers; FI quarterly fund assets as a check. | Reduces |
| 10 | **Performance unpowered** (MDE 3.5% per year vs 0.60-0.94). | One table, written as a bounded null with its MDE. | Reduces (the honest presentation is fully solved; the power is not) |
| 11 | **Few independent events:** 11 rounds, 7 award dates. | Round FE; leave-one-round-out; permutation of winner labels within round; report results round by round. | Reduces |
| 12 | **Global active award under appeal** (99 bids, a third of the sample). | Main tables include it as decided; robustness without it (3-year gap MDE 17.0). | Reduces |
| 13 | **Pre-trends:** CJJM's own leads are positive; FTN may select on flows. | Leads in T5; pre-award flows as a T4 covariate; DiD rather than post-only. | Reduces |
| 14 | **Share-class vs fund identity:** winners often enter with new share classes; 2 of 66 removed classes (SEK 0.78bn of 74.0bn) belong to funds that won. | Use the Morningstar fundid as the unit, as CJJM aggregate share classes (p. 10). | Fully solves |
| 15 | **Timing of savers' choices unverified:** whether early choosers' switches execute before removal; the 85-95% default figure. | Check Pensionsmyndigheten saver letters and press releases; request the transaction-type ledger. | Fully solves with the ledger; reduces otherwise |
| 16 | **December placement** inside some windows (Europe and global index: award 31 Oct, window Nov-Dec). | Month-median adjustment (used in section 5); drop December as robustness. | Reduces |
| 17 | **Data calendar:** R6 transfers after Aug 2026; the October file lands about mid-November. | Build on R1-R4 now; R6 losers' pre-removal windows (Jun-Jul 2026) are already observed; R6 transfers are an add-on. | Reduces |
| 18 | **Specification search / multiple tests.** | Pre-register the predicted-sign table (4.4) and one headline per block; blind power work as here. | Reduces |
| 19 | **Manuscript inconsistency** (0.16 cited as column 4, but it is in column 3). | Cite Table 6, column (3); note it. | Fully solves |
| 20 | **Published version unchecked.** | Download the RFS PDF on the SSE network; confirm the tables match and record the published page numbers. | Fully solves |
| 21 | **"Avoid applying the question to Nordic countries unless meaningful"** (L147). | The extension (voluntary vs default split of a list effect) needs a list with a default transfer, which the UK setting lacks. | Reduces (examiner's judgement) |

---

## 7. Verdict

### 7.1 Comparison with the SSZ dossier (`round1/ssz_dossier.md`)

**Agreements (checked against its files):**
- Performance MDE of 2.5-4.3 pp per year (mine: 3.5).
- 6-month spillover MDE of 6-7% (mine: 6.3-9.0%).
- Monthly non-PPM flow sd of 2.83% (mine: within-fund sd 2.83 for bidders).
- `nt` measures PPM net flow; transfer-month reconciliation is poor.

**Disagreements:**
1. **SSZ's selection LPM conditions on incumbency, not on bidding.** Its "FTN selection: P(win) on rank" (N 81: 62 removed, 19 incumbent winners) treats every removed fund as a loser. At fund level, 26 of 66 removed classes never bid (`ssz_cross_section_fundlevel.csv`). That LPM estimates P(bid) x P(win | bid), not FTN's rule. CJJM's structure (Table 2: availability; Table 5: additions given availability) separates the two. Bid-level MDE today: 0.40 (N 142), against SSZ's 0.436 (N 81).
2. **Two "removed" share classes belong to funds that won with another class** (abrdn European Sustainable Equity; SEB Sweden Equity Fund C; SEK 0.78bn). At fund level they are winners. Small, but it changes their sponsor flow from -1.
3. **SSZ cites "Cookson's listing effect is 0.16% per month (prior memo; not re-verified here)".** Now verified (Table 6, column 3), with the column-4 citation error noted.
4. **The SSZ dossier says N = 81 incumbents** (from `ftn_sponsor_sample.csv` after dropping missing returns). Its own `ftn_cross_section.csv` has 87 in R1-R4 (66 removed + 21 winners). This is consistent, not an error; I note it for the record.

**Shared resource:** SSZ's "participant flow over award-to-transfer + 2" is the same object as my test (iv). Either anchor can carry it; CJJM's Figure 1 is the natural display for it.

### 7.2 How strong is (B)? (JUDGEMENT)

On the brief's criteria:
1. **Anchor question equals thesis question:** yes, more directly than (A). CJJM ask what a list selects on, how it moves money and whether it adds value; FTN is a list.
2. **Table-level replication:** weak. Every table is an adaptation, CJJM's data are confidential, and their two conflict variables are absent. (A) can reproduce SSZ Tables III and IX on pre-2024 PPM data with powered linear MDEs. On this criterion (A) wins clearly.
3. **Dated reform with treatment and control:** yes. Dated awards, winners and losers within category, placebo dates, and a voluntary/mechanical split that CJJM cannot make.
4. **Extension inside the anchor's tables:** yes. Table 6 columns (voluntary, mechanical, outside), the Table 5 bid margin, and the Table 8 A/B/C fee rows.
5. **Numbers comparable to the anchor's:** for selection (percentile gaps), fees (bp) and event-time flow profiles, yes. For outside flows and performance, only as bounded nulls.

Powered core: selection against a CJJM-sized 3-year gap (about 77% power), voluntary loser exits (MDE 0.8-1.5% of PPM capital in month 1), probably winners' post-transfer flows (0.67% per month), and fees (exact). That is a thesis with three to four informative tables, which is more than the pressure test credited to (B) ("selection logit and fees" only).

**Overall:** (B) is a credible final anchor and the better match to Klug's prompt (selection design, investor behaviour) and to his index-inclusion work (a list inclusion is an index inclusion). It is weaker than (A) on the course's "replication on solid ground" criterion. My ranking: (B) ahead on fit and policy payoff, (A) ahead on replicability; close overall. The deciding question for Klug is whether a pure adaptation counts as the replication.

### 7.3 What would make (B) fail

- **The examiner requires a reproduction of the anchor's main exercise on comparable data.** CJJM cannot be reproduced; SSZ can.
- **Savers act only at the transfer date.** If active choices execute inside the transfer month, test (iv) is a null that cannot be separated from the dose without the ledger. The voluntary/default split then rests on a ledger that may not come.
- **FTN's selection is unrelated to observable covariates**, so T4 is a null with MDE 15 points. That is interesting ("certification on unobservables"), but it leaves the thesis with fees as its only clear positive result.
- **Neither SHoF data for non-PPM losers nor FTN bid status arrive.** The selection sample stays at 142 bids, tilted to PPM incumbents. P(win | qualified) stays at 3 rounds (MDE 25 points).
- **The global active appeal overturns the award**, removing a third of the bids.

---

## Appendix: files (in `scratchpad/anchor_final/round1/cookson_work/` unless noted)

- `bidders.csv`: round table, finalised this run (backup `bidders_v0_backup.csv`). `winners.csv`: 75 winners with ISIN and procured fee. `bids_raw.json`, `parse_bids.py`, `parse_winners.py`: extraction from the FTN §5.2 bidder lists.
- `bids_long.csv`: 290 bids with PPM and Morningstar matching (`match_bids*.py`, `shof_map.py`; `match_out*.txt` logs). `bids_long_final.csv`: adds qualification status, doubtful-match flags, SHoF performanceId and 12/36-month returns and within-round percentiles.
- `ppm_panel_2018_2023.csv` (`parse_ppm_2018_2023.py`) plus `scratchpad/audit/pa_panel_2023_2026.csv` feed `build_panel.py`, which writes `ppm_shof_panel.pkl` (PPM fund-months 2018-2026 linked to SHoF TNA and returns, imputed flows).
- `moments.py` writes `moments.pkl`: outside-PPM flow moments (section 3.2).
- `cookson_power.py`: sample counts, selection, outside-flow and performance MDEs.
- `ppm_pretransfer_power.py`: voluntary loser exits (iv); the size-threshold variants were run with the `sed` substitution recorded in section 5.
- `post_transfer_power.py`: winners' post-transfer flows (v).
- `ssz_cross_section_fundlevel.csv`: SSZ's `ftn_cross_section.csv` with Morningstar fundid and bid status added.
- `t6-41.png`, `f1-45.png`: CJJM Table 6 and Figure 1 page images.
- External sources consulted:
  - ORA record uuid:84450809-3da8-4c6a-bfc1-0f41ac780b71 (accepted manuscript, dates);
  - academic.oup.com/rfs/article/34/1/227/5841239 (metadata only; PDF blocked);
  - FCA Occasional Paper No. 30 (fca.org.uk/publication/occasional-papers/occasional-paper-30.pdf, August 2017);
  - academicnewsletter.sufe.edu.cn/info/352223 (published abstract).
