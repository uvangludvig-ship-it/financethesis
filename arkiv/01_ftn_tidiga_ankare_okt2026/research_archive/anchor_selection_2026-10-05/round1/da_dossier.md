# Dossier for candidate (C): Da, Larrain, Sialm and Tessada (2018) as the anchor

Prepared 5 October 2026 (round 1, third run; the first two were cut off). Paper: Zhi Da, Borja Larrain, Clemens Sialm and José Tessada, "Destabilizing Financial Advice: Evidence from Pension Fund Reallocations", Review of Financial Studies 31(10), 2018, pp. 3720-3755 (DLST below).

Conventions. "p." is the RFS page. The full text was read from the typeset RFS PDF on Zhi Da's Notre Dame page (36 pages; PDF page k = RFS page 3719 + k). Verbatim numbers with page references are in `da_work/paper/dlst_2018_key_numbers.txt`. All Swedish numbers come from scripts in `scratchpad/anchor_final/round1/da_work/` (list in the appendix). Labels: **VERIFIED** (checked against the cited source or reproduced by the cited script), **JUDGEMENT** (my reasoning), **NOT VERIFIED**.

Blind-analysis rule. No stock return, CAR or price was downloaded or looked at. Everything below is built from holdings, PPM capital and market capitalisations only.

---

## 0. Bottom line

- **The go/no-go number.** On pre-award holdings (FI 2026Q1, 31 March 2026) and exact market caps, the cross-sectional sd of net flow-induced pressure (net FIP, % of market cap) in the Swedish small-cap round is **0.75 pp; after partialling out log market cap it is 0.73 pp** (174 Swedish-listed stocks, base scenario S1). That clears the pre-committed 0.5 pp bar. It does not clear the 1 pp bar. **VERIFIED** (`netting_q1.py`, `log_netting_q1.txt`).
- **Netting does not destroy the shock in market-cap units.** In SEK, winners and losers overlap (corr of buy and sell 0.50; sd(net)/sd(gross) = 0.58). The overlap sits in large liquid names (Nordnet, Beijer Ref, Addtech, AAK). In % of market cap, buy and sell are slightly negatively correlated (-0.14), so sd(net FIP)/sd(gross FIP) = 1.13. The earlier fear that net would be a third of gross is wrong for this round. **VERIFIED.**
- **The number is fragile in the tail.** The top ten stocks carry 70% of the squared net FIP. Without them the sd is 0.43 pp. The largest positive values come from one small new winner, Aktiespararna Småbolag Edge (AUM SEK 545m), which under the allocation rule receives about SEK 1.56bn, 2.9 times its size, and is assumed to scale its micro-cap book pro rata. If Edge instead invests like the other three covered winners (S6), the residual sd is **0.56 pp**: still above 0.5, barely. **VERIFIED** (numbers); the pro-rata assumption is **JUDGEMENT**.
- **Power.** Award window (days -2 to +5, daily idiosyncratic sd 2.5%, no cross-sectional inflation): SE 0.73, **MDE 2.1% CAR per 1 pp of net FIP** (S1); 2.7 (S6); 3.5 without the top ten. Against plausible multipliers of 1.4 to 3.6 (DLST: elasticity -0.45 implies about 2.2; DLST Table 11 day-3 slope 3.61), power is 48 to 100% in S1 and 30 to 96% in S6. The transfer-window test has MDE 3.7 to 8 and is a labelled first look only.
- **The paper.** DLST is a 15-event (22 in the expanded sample) study of Chilean advice-driven switches between equity fund A and bond fund E, 2011 to 2014. The published effect is **1.06% on day 1 (SE 0.29), 1.22% by day 3, 0.33% by day 10** (Table 6, p. 3736), not "about 2.5% within eight days". The 2.5% figure is the May 2015 draft's raw-index number (peak 2.45% on day 8). **VERIFIED.**
- **Replication.** Only the cross-sectional table (Table 11 Panel A and B), the placebos (Table 7 in spirit), the fund-response table (Table 13, quarterly) and the descriptive tables carry over. DLST's headline aggregate tables (6, 8, 9) have no Swedish counterpart, because the FTN shock nets to about zero in aggregate. No part can be replicated on independent (non-FTN) Swedish data in nine weeks: the December placement is about a tenth of the size and confounded by December seasonality; the 2011 PPM mass-switching had no published event dates; the 2019 purge has no public capital mapping. **VERIFIED** (sizes) and **JUDGEMENT** (feasibility).
- **Verdict.** (C) passes its own go/no-go rule, narrowly and on the tail. It is a defensible thesis with a powered award-date test on one event. Against SSZ (A) it is weaker on the course's "replication" standard (method-level, single event, no data-level replication) and stronger on novelty and on fit with Klug's index-inclusion expertise. My ranking: (A) remains the safer anchor; (C) is a GO only as an explicitly single-event, Table 11-style study and only if Klug accepts a method-level replication (section 6).

---

## 1. The paper (VERIFIED unless marked)

### 1.1 Design

- **Setting** (pp. 3724-3726). Chilean DC pension system; each AFP offers funds A (riskiest) to E (bonds). A and E are not default options. Assets (US$bn, Table 1, p. 3725): A 28.0, B 27.9, C 60.6, D 22.4, E 14.1. Chilean equity weight: A 16.9%, E 1.1%. Cash: A 2.9%, E 16.4%.
- **What moves, and between which funds.** Felices y Forrados (FyF), an advisory firm charging about US$20 a year, e-mails switch recommendations after the close. Savers move whole balances between fund A (equity) and fund E (bonds) (p. 3727). Switches take effect at t+4, priced at t+2, with a 5%-of-assets daily cap, first come first served (p. 3726), which creates a rush to switch.
- **Events** (Table 2, p. 3727). 22 recommendations, 27 July 2011 to 18 March 2015. Recommendations 1 to 15 (to 24 January 2014) involve only funds A and E and are the main sample. Recommendations 16 to 22 are partial (weights 0.25 or 0.5) and enter only the "expanded" column of Table 9.
- **Size.** Monthly flows of US$1 to 4bn in recommendation months; up to 10% of the equity funds and 20% of the bond fund (pp. 3731-3732). A US$2.5bn flow implies about US$395m of domestic equity trading against US$205m daily market volume (p. 3732).
- **Windows.** Event day 0 is the sending date (after the close). Aggregate CARs over days 1 to 10 (Table 6). Calendar-time regressions on day dummies 1 to 5, January 2010 to February 2014 (Tables 8 to 10). Cross-section: cumulative returns and turnover to event days 1 to 5 (Table 11). Monthly volatility (Table 12, 48 months). Monthly cash holdings (Table 13, 36 months).
- **Benchmark.** IPSA minus the MSCI World index in pesos (p. 3734). Without the adjustment the day-1 effect is 0.63% (fn 14, p. 3734).

### 1.2 Tables and magnitudes (units as printed)

| Table | Content | Key numbers |
|---|---|---|
| 1 (p. 3725) | Five fund classes | see 1.1 |
| 2 (p. 3727) | 22 recommendations | dates; weights ±1, ±0.5, ±0.25 |
| 3 (p. 3729) | Logit of recommendation on lagged returns | equity return week -1: 73.42 (t 2.71) for E to A; pseudo R2 0.08 to 0.16; N 323 and 441 days |
| 4 (p. 3730) | FyF vs contrarian returns (% per day) | all 15 periods: 0.020 (t 0.901); FyF wins 8 of 15 |
| 5 (p. 3733) | Modelo (young) AFP | switch to A: +4.0% flow to A, +7.8% more at Modelo |
| 6 (p. 3736) | Aggregate equity CAR (SE) | day 1 1.06% (0.29); day 2 1.12% (0.34); day 3 1.22% (0.53); day 4 1.06% (0.65, n.s.); day 5 0.58% (0.58); day 8 0.97% (0.65); day 10 0.33% (0.90). Bonds: day 10 -0.22% (0.15) |
| elasticity (p. 3736) | Wurgler-Zhuravskaya back-of-envelope | Δq = 2 × 16.9% / 70 = 0.48%; elasticity -0.48/1.06 = **-0.45** |
| 7 (p. 3738) | Placebos | Panel A: 16 probit-chosen dates 2003-2006, all n.s.; Panel B: MSCI World and Barclays Global Aggregate on the actual dates, n.s. |
| 8 (p. 3739) | Calendar-time day dummies | day 1: raw 0.63% (0.25), adjusted 1.05% (0.29), with controls 0.77% (0.22); CUM[1-3] adjusted 1.21% (p 0.014); CUM[1-5] 0.57% (p 0.375) |
| 9 (p. 3741) | Subsamples | day 1: first 7 recs 0.45% (0.33); last 8 1.01% (0.30); buy 1.06% (0.33); sell 0.48% (0.31); all 22 recs 0.44% (0.20) |
| 10 (p. 3742) | Log volume by broker type | retail-with-retail day 1 +17.6% (SE 8.5); CUM[1-3] +52.8% (p 0.005); institution-with-institution day 4 and 5 +15%, n.s. |
| 11 (p. 3744) | Cross-section on FIP (event FE, SE clustered by event) | Panel A CAR: day 1 0.714 (0.603), day 2 1.355 (1.186), **day 3 3.613 (1.534)**, day 4 2.573 (1.468), day 5 0.911 (1.555); N 512 to 569 stock-events. Panel B turnover on abs(FIP): day 3 0.665 (0.271), day 5 1.002 (0.358). Panel C retail turnover |
| 12 (p. 3745) | Monthly volatility on abs(FIP) | 1.506 (0.368) to 0.613 (0.359); 48 cross-sections |
| 13 (p. 3748) | Monthly cash holdings, 36 obs | fund A: FyF recommendation +0.497 pp (0.213); trend +0.043 pp/month; fund E trend +0.477 pp/month |

FIP definition (eq. 1, p. 3743): FIP_i,t = FLOW_A,t × w_i,t-1 / MKTCAP_i,t-1, with A funds aggregated across AFPs and weights from the previous month's holdings. The Table 11 coefficient is a return per unit of FIP: 1 pp of market cap in fund demand moves the day-3 return by 3.6 pp.

### 1.3 The "about 2.5% within eight days, then reversal" claim: wrong for the published paper

- The 2015 draft ("Price Pressure from Coordinated Noise Trading", May 2015, www7.uc.cl) used raw IPSA returns and a 15-day window. Its abstract says "large price pressure of almost 2.5%". Its p. 12 says the pressure "peaks at 2.45% on day 8". **VERIFIED** (text extracted in the browser). The t-statistic of 2.17 comes from a WebFetch summary only: **NOT VERIFIED**.
- The RFS version: about 1% on day 1, 1.22% by day 3, insignificant from day 4, 0.33% by day 10 (Table 6). The text says the response is "around 1% during the first three days ... and reverts within five days" (p. 3721) and "remains relatively stable for the subsequent eight days and reverts almost completely within ten days. The statistical significance disappears by the fifth day" (p. 3734). Correct citation: 1.06% on day 1, 1.22% by day 3, reversal by days 5 to 10.
- The project doc `claude/final_design_and_plan.md` already states the RFS numbers correctly (1.06%, SE 0.29; 1.22%; 0.33%; -0.45; Table 11 3.61, SE 1.53; day -1 0.64% excluded). All of those are **VERIFIED** here.

### 1.4 Are the data public?

Partly (Appendix, p. 3751). Public: SAFP (regulator) daily share values, monthly holdings, demographics and AUM; monthly flows computed from them (fn 19); recommendation dates from FyF's website; index data (MSCI, LVA, Central Bank). Commercial: Economatica (prices, accounting), Bloomberg. Not public: the daily switch counts in Figure 1 ("administrative records that are not publicly available", p. 3722) and the broker-level transaction data from the Santiago Stock Exchange (Tables 10, 11C).

### 1.5 What DLST's own question is

Their Section 3 question (do large uninformative pension flows move prices, and in proportion to FIP) is the thesis question. Their title question (does advice destabilise markets) is not; FTN is a mandated reallocation, not advice. **JUDGEMENT.**

---

## 2. Netting (the decisive deliverable)

### 2.1 Assumptions, stated

| Item | Choice | Source / status |
|---|---|---|
| Event | Swedish small cap, award 28 May 2026 | briefing; FTN report |
| Holdings date | **FI 2026Q1 (31 March 2026), pre-award**; FI 2026Q2 (30 June 2026) as comparison | FI zip `Fondinnehav_2026Q1_2026-08-16 17.42.zip`, all 16 funds report Kvartalsslut 2026-03-31 (**VERIFIED**). Parsed in the browser pane with `fi_inbrowser_extract.js`; per-stock vectors in `fi26q1_smallcap_vectors.psv` |
| Weight | market value / fund AUM, transferable securities only, duplicate ISIN lines summed | same |
| PPM capital | PPM market value per fund at 31 Mar 2026 (base) and 31 Aug 2026 (closest to transfer) | `audit/pa_panel_2023_2026.csv` |
| Losers | 9 funds: 7 Swedish-domiciled (Spiltan 2.15bn, Carnegie 1.97bn, Lannebo SCO 0.78bn, LF Småbolag Sverige 0.70bn, Lannebo Micro 0.69bn, Skandia 0.33bn, Humle 0.04bn at 31 Mar) plus Evli Sverige Småbolag (0.61bn) and C WorldWide Sweden Small Cap (0.53bn), not in the FI register | **VERIFIED** (capital); ISINs as in `netting_smallcap.py` |
| Allocation rule | Capital from deregistered funds is split equally across procured funds; incumbents keep their capital and are topped up only to the common level (FTN Sverige småbolag report, section 3.7, `ftn_txt/... Sverige småbolag.txt` lines 752-765). With T = SEK 7.81bn and the smallest incumbent (D&G Småbolag) at 3.23bn > T/5, only the five new winners receive, T/5 = 1.56bn each | rule text **VERIFIED**; the water-filling reading is **JUDGEMENT** (the binding rules are in the procurement instructions, not read) |
| New winners | Aktiespararna Småbolag Edge, Cliens Småbolag, Nordea Småbolagsfond Sverige, SEB Sverigefond Småbolag (in FI) and Danske Invest SICAV Sverige Småbolag (not in FI) | |
| Default acceptance | 1.0 (base) and 0.85 (S2, S4): the buy side is scaled; losers sell everything either way | reported 85 to 95% (briefing): **NOT VERIFIED** for this round |
| Market cap | Exact company-level market caps from stockanalysis.com (`__data.json`, read 5 Oct 2026) | `mcap/stockanalysis_sto_20261005_exact.psv`. Post-award date: a Wardlaw-type concern. Use FinBas caps at day -10 in the thesis |
| Universe for FIP | Stockholm-listed stocks with a matched cap: 174 of 188 held stocks; they carry 96.7% of gross SEK | foreign-listed names (Tomra, Nordic Semiconductor, Puuilo, Hiab, ChemoMetec, Össur) and Plejd excluded |
| Controls | log market cap only | B/M, momentum, Amihud need FinBas: **not done** |

### 2.2 Results, Swedish small cap (FI 2026Q1 holdings)

Columns: S1 covered funds, acceptance 1.0; S2 acceptance 0.85; S3 imputed full coverage (Danske invests like the average covered new winner, buy × 5/4; Evli and C WorldWide sell like the average covered loser, sell × T/covered); S4 = S3 with acceptance 0.85; S5 sell side only; S6 Edge invests like the average of the other three covered winners. Capital at 31 March 2026 (T = 7.81bn). Source `log_netting_q1.txt`.

| Statistic | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| Sell, covered equities (SEK bn) | 6.53 | 6.53 | 7.65 | 7.65 | 6.53 | 6.53 |
| Buy (SEK bn) | 6.12 | 5.20 | 7.65 | 6.50 | 0 | 6.14 |
| corr(buy, sell), SEK | 0.50 | 0.50 | 0.50 | 0.50 | | 0.47 |
| **sd(net)/sd(gross), SEK** | **0.58** | 0.58 | 0.58 | 0.58 | 1 | 0.62 |
| Share of gross SEK volume that nets out | 0.53 | 0.52 | 0.52 | 0.52 | 0 | 0.45 |
| **Top-10 share of squared net SEK** | **0.44** | 0.42 | 0.45 | 0.43 | 0.42 | 0.47 |
| corr(buy FIP, sell FIP) | -0.14 | -0.14 | -0.14 | -0.14 | | -0.10 |
| sd(net FIP)/sd(gross FIP) | 1.13 | 1.14 | 1.13 | 1.14 | 1 | 1.11 |
| **sd net FIP (pp of mcap)** | **0.75** | 0.67 | 0.92 | 0.82 | 0.37 | 0.56 |
| **Residual sd after log mcap (pp)** | **0.73** | 0.66 | 0.90 | 0.81 | 0.37 | **0.56** |
| sd, winsorised 1/99 | 0.60 | 0.55 | 0.73 | 0.66 | 0.36 | 0.54 |
| sd, excluding top-10 abs(FIP) | 0.43 | 0.40 | 0.51 | 0.48 | 0.24 | 0.40 |
| Top-10 share of squared net FIP | 0.70 | 0.67 | 0.71 | 0.68 | 0.57 | 0.52 |
| Stocks with abs(net FIP) ≥ 0.5 / ≥ 1 pp | 47 / 15 | 44 / 14 | 56 / 21 | 57 / 19 | 33 / 8 | 45 / 15 |
| min / max net FIP (pp) | -1.64 / 6.39 | -1.64 / 5.43 | -1.92 / 7.99 | -1.92 / 6.79 | -1.90 / 0 | -1.64 / 2.57 |

With capital at 31 August 2026 (T = 8.41bn) every FIP statistic is 6 to 10% larger (S1 residual sd 0.80, S6 0.62). **VERIFIED.**

**Largest net-demand stocks by FIP** (S1, March capital):

| Stock | Mcap SEK bn | Sell SEK m | Buy SEK m | Net FIP pp | Who |
|---|---|---|---|---|---|
| Meds Apotek | 0.44 | 0 | 27.8 | +6.39 | Edge only |
| Devyser Diagnostics | 0.93 | 0 | 21.7 | +2.34 | Edge only |
| Vertiseit | 2.13 | 0 | 47.2 | +2.21 | Edge, Nordea |
| CAG Group | 0.64 | 0 | 12.4 | +1.93 | Nordea |
| Ovzon | 3.81 | 62.6 | 0 | -1.64 | Carnegie |
| MedCap | 7.66 | 123.0 | 0 | -1.61 | Spiltan (114m), LF |
| Bergman & Beving | 7.14 | 111.0 | 0 | -1.55 | Spiltan |
| Ferroamp | 0.27 | 0 | 4.1 | +1.52 | Nordea |
| Coor | 4.56 | 0 | 65.3 | +1.43 | Nordea, Edge |
| Arla Plast | 0.77 | 0 | 11.0 | +1.43 | Nordea |
| Lime Technologies | 3.26 | 61.7 | 16.4 | -1.39 | Spiltan, LF / Cliens |
| Humana | 3.40 | 0 | 44.0 | +1.30 | Edge |

**Largest by net SEK:** Bufab -184m (-0.67 pp), Sweco +148m (+0.32), AAK +144m (+0.30), NCAB -135m (-0.81), Sectra +135m (+0.24), OEM +131m (+0.52), MedCap -123m (-1.61), AQ Group +117m (+0.53), Hoist Finance -116m (-0.67), Balder +112m (+0.21), Bergman & Beving -111m (-1.55). **VERIFIED.**

Cross-checks. MedCap's sell of SEK 123m is Spiltan 5.31% × 2.15bn = 114m plus LF 1.24% × 0.70bn = 9m; the project doc cites Placera's 144m for MedCap at Spiltan's later capital. **VERIFIED** (arithmetic from `fi26q1_smallcap_vectors.psv`).

### 2.3 Coverage of the missing foreign-domiciled funds

- Sell side: FI covers 7 of 9 losers, SEK 6.67bn of 7.81bn (85%) at 31 March; 7.51 of 8.41bn (89%) at 31 August. Missing: Evli Sverige Småbolag (0.61bn March, 0.32bn August; it had +0.41bn net trading in March and -0.47bn in June 2026) and C WorldWide Sweden Small Cap (0.53 / 0.57bn). **VERIFIED** (`pa_panel`).
- Buy side: FI covers 4 of 5 new winners. Danske Invest SICAV Sverige Småbolag (LU1857272469) receives one fifth of the inflow and is missing.
- Bounds: S3/S4 impute the missing funds at the average covered weights. They raise the FIP sd by about 23%. The truth lies between S1 and S3 if the missing funds hold similar stocks. **Solution:** Danske's factsheet (top holdings, date stated), Morningstar holdings via SHoF for all three. This reduces the gap; it does not close it unless full holdings are obtained.

### 2.4 Pre-trading diagnostic (Q1 versus Q2 holdings)

At constant March capital, the stock-level vectors built from 31 March and 30 June holdings correlate 0.954 (sell), 0.967 (buy) and 0.946 (net); covered sell totals are 6.53bn (Q1) and 6.52bn (Q2). Losers had not visibly rebalanced away from their names by 30 June, one month after the award. **VERIFIED** (`netting_q1.py`). Market-value weights also move with prices, so this is a weak test. Share counts would be better, and July to September trading is not observable before FI publishes 2026Q3 (the 2026Q2 file is dated 21 September 2026, so Q3 will likely appear after 7 December: **JUDGEMENT** from the file names).

### 2.5 Placebo vector

The five capped incumbents' holdings, scaled like an inflow of T, give a pseudo-FIP with sd 0.28 pp and correlation -0.06 with net FIP. The incumbents-only placebo therefore has power of its own and is not a copy of the treatment. **VERIFIED.**

### 2.6 Reconciliation with the earlier run (FI 2026Q2, transcribed caps)

The earlier run (`netting_fip.py`, Q2 holdings, market caps transcribed by a summariser model) gave sd 0.51 pp (S1) and a residual of 0.51. The transcription had errors (Volvo Car 55.3 vs exact 42.0bn; Yubico 7.7 vs 9.9bn; Viscaria 6.1 vs 7.8bn) and left 28 holdings unmatched, among them Meds Apotek, CAG, Ferroamp, Precio and Malmbergs, the micro-caps that now drive the tail. The move from 0.51 to 0.75 comes mostly from matching those caps, not from the holdings date (Q1 and Q2 vectors correlate 0.95). **VERIFIED** for the inputs; the attribution is **JUDGEMENT**.

### 2.7 Swedish active large/mid round (award 27 August 2025)

Assumptions: FI 2025Q2 holdings (30 June 2025, pre-award; all 23 funds report that date, **VERIFIED**); PPM capital at 31 July 2025; 18 losers (T = 21.10bn), of which 4 foreign-domiciled are missing (LU0424681269 0.04bn, LU1349495116 0.42bn, NO0008000023 1.96bn, LU0047322432 0.77bn: 15% of T); water-filling level L = (T + Carnegie Sverigefond's 2.86bn)/7 = 3.42bn for each of 6 new winners and a 0.56bn top-up to Carnegie; incumbents above L (AMF 27.5bn, D&G 27.5bn, Folksam LO 12.0bn) receive nothing; the sixth new winner (LU2352402031, 3.42bn) is missing. Bond lines (FRNs) dropped. Vectors in `fi25q2_largemid_vectors.psv`.

| Statistic | Covered | Imputed full coverage |
|---|---|---|
| Sell / buy, SEK bn | 17.29 / 17.22 | 20.36 / 20.55 |
| corr(buy, sell), SEK | 0.83 | 0.83 |
| sd(net)/sd(gross), SEK | **0.32** | 0.32 |
| Top-10 share of squared net SEK | 0.60 | 0.60 |
| sd net FIP (pp) | 0.41 | 0.48 |
| Residual sd after log mcap | **0.39** | **0.46** |
| sd excl. top-10 | 0.27 | 0.32 |
| Top-10 share of squared net FIP | 0.59 | 0.59 |
| abs(FIP) ≥ 0.5 / ≥ 1 pp | 24 / 6 | 34 / 13 |

Largest abs(FIP): Lammhults (-2.32, SEK 4.9m on a 0.21bn cap), Lime (+1.58), Garo (-1.36), Balco (-1.15), Truecaller (-1.13, -80m), Afry (+1.10, +128m), Troax (-0.94), Addnode (+0.93), AddLife (+0.92, +190m), Sweco (+0.84, +386m). **VERIFIED** (after correcting five wrong fuzzy matches, e.g. Ericsson matched to Betsson).

Judgement on weight quality: **moderate for the award test, poor for the transfer test.** The holdings are 58 days before the award, which is good. But the transfers happened in January and February 2026 (losers' net trading -8.86bn in January and -6.86bn in February 2026; winners and Carnegie +10.06bn and +8.06bn: **VERIFIED**, `pa_panel`), so the weights are seven months stale at execution; 15% of loser capital and one sixth of the new-winner inflow are missing; and the residual sd fails the 0.5 bar in both columns. This round can serve only as a second, weak event (pooled), not as a stand-alone test. FI 2025Q4 holdings (31 December 2025) exist and should be used for the transfer window.

---

## 3. Mapping DLST's tables to Sweden

### 3.1 Events

| Round | Award | Execution | Usable Swedish-stock FIP | Status |
|---|---|---|---|---|
| Sweden small cap | 28 May 2026 | after 31 Aug 2026 (losers still held 8.41bn at end-August: **VERIFIED**); late September to October per project doc (**NOT VERIFIED** here) | residual sd 0.56 to 0.90 pp | headline |
| Sweden active large/mid | 27 Aug 2025 | Jan-Feb 2026 (**VERIFIED**) | 0.39 to 0.46 pp | weak second event |
| Nordic small cap, Nordic large/mid | 19 Feb 2025 | about mid-May 2025 (project doc) | not computed; losers Aktia and Fondita are Finnish, not in FI | NOT VERIFIED |
| Sweden passive | 27 Aug 2025 | Oct 2025 | index funds hold the same index: net demand near zero | no cross-section |
| Europe small cap | 28 May 2026 (same day) | Jul 2026 | near-zero Swedish FIP | same-date confound check only |

So DLST's 15 events become one strong event, one weak event and possibly one more. DLST's Table 11 used 512 to 569 stock-events over 15 events with SEs clustered by event; the Swedish headline is about 174 stocks on one date.

### 3.2 Table-by-table

| DLST | Estimable in Sweden? | Swedish analogue, N | No counterpart / deviation |
|---|---|---|---|
| T1 fund classes | Yes | 9 losers, 5 new winners, 5 incumbents: PPM and total AUM, fee, domicile | one category, not five risk classes |
| T2 event list | Yes | award, closure, letters, deadline, detected transfer date per fund; about 3 rounds | |
| F1 daily switches | Partly | daily TNA of losers (SHoF Morningstar, Avanza) | flows, not people |
| T3 determinants | Partly | logit/LPM of winning on fee and past returns (10 of 19 bids in this round) | selection, not timing |
| T4 strategy returns | No | | advice informativeness has no analogue |
| F2 monthly flows | Yes | PPM `nt` per fund, monthly | |
| T5 young investors | Partly | first stage: realised outflow on rule outflow; savers by gender in PPM files | no age data |
| F3, T6 aggregate CAR | **No** | net aggregate demand is about zero by construction (S3: sell 7.65bn, buy 7.65bn) | replaced by a long-short portfolio sorted on net FIP |
| T7 placebos | Yes | frozen FIP vector on non-event windows (randomisation inference); incumbents' pseudo-FIP (sd 0.28, corr -0.06); Europe small-cap award on the same day | not probit-chosen dates |
| T8 calendar-time | Partly | daily long-short return on event-day dummies with SHoF factors | 1 to 2 events |
| T9 subsamples | Partly | net buyers vs net sellers; liquidity terciles; second event | within one event |
| T10 broker volume | No | total turnover only (FinBas) | no public broker IDs |
| **T11 cross-section** | **Yes (A, B); No (C)** | **CAR and turnover on net FIP, about 174 stocks, award window and transfer window side by side** | one event; inference by randomisation, not by event clusters |
| T12 volatility | Partly | monthly volatility on abs(FIP), award and transfer months | few treated months |
| T13 fund response | Partly | losers' and winners' cash (`Likvida_medel`) in FI quarters, incumbents as control | quarterly; one or two quarters |

### 3.3 Can any part be replicated on data independent of FTN?

1. **PPM advisor mass-switching before the ban.** The ban on mass fund switches took effect on 1 December 2011; about 75% of 2011 switches were robot-driven mass switches; about 700,000 savers used such services; one example moved SEK 300m for 65,000 savers over two days (Pensionsmyndigheten, "Effekter av massfondbytesstoppet", 19 Sep 2012, pp. 1, 4, 13, 16, per a WebFetch summary: **NOT VERIFIED** verbatim). This is the closest Swedish analogue to FyF. But event dates and fund-level daily flows are not published (the report has weekly totals only after the stop), and Swedish stock-level fund holdings for 2010-2011 are not in the FI register as downloaded. **Not feasible by 7 December** without a Pensionsmyndigheten data delivery. Worth one request; not a plan.
2. **The 2019 purge into AP7 Såfa.** Funds leaving PPM in 2019: 330 exits with about SEK 61bn at their last observation, concentrated in February to May 2019; Swedish-equity categories SEK 15.2bn, of which 7.0bn is Swedbank Robur Sverigefond MEGA, likely a share-class merger with no net demand (`ppm_panel_all.csv`: **VERIFIED** counts; the merger reading is **JUDGEMENT**). Which capital went to Såfa and which to merger targets requires fund-by-fund deregistration letters. The shock is one-sided and staggered. **Not viable as a replication in time**; possibly a robustness event.
3. **December placements.** Every December about SEK 40 to 52bn is placed (all-fund December `nt`: 51.6bn in 2018, 40.5 in 2019, 41.7 in 2020, 42.0 in 2021, 44.3 in 2022, 47.4 in 2023, 49.8 in 2024, 51.3 in 2025: **VERIFIED**, `ppm_panel_all.csv`). Into the Swedish small-cap category, December net trading is only SEK 0.06 to 1.06bn a year (2018-2025) on 21 to 56bn of capital, against about 7.8bn moved by the FTN round. The FIP would be roughly a tenth of FTN's, one-sided, inside a month with known seasonality (tax-loss selling, window dressing), and the placement day within December is not verified. Seven events (2019-2025, FI holdings) would not offset a tenfold smaller dispersion. **Not viable as a powered replication; usable as a placebo-style descriptive.**

Conclusion: no independent replication is feasible. The thesis replicates DLST's method (Table 11), not its data. **JUDGEMENT.**

---

## 4. MDEs (2.8 × SE), recomputed from the netting numbers

Formula: SE = c × σ_CAR / (sd_resid(FIP) × √(N - 2)), σ_CAR = σ_daily × √(days), MDE = 2.8 × SE, power = Φ(b/SE - 1.96). Assumptions: σ_daily = 2.5% for Swedish small caps (assumption, **NOT VERIFIED**; needs FinBas); N = 174 (168 for large/mid); c = 1.0 or 1.3 (inflation for residual cross-correlation on a single date, assumption); b = multiplier in % CAR per 1 pp of net FIP. Code `mde.py`.

| Test | FIP scenario | SE | MDE | Power at b = 0.7 / 1.4 / 2.2 / 3.6 |
|---|---|---|---|---|
| Award, days -2 to +5 (8 d), c = 1.0 | S1 (0.734) | 0.73 | **2.06** | 0.16 / 0.48 / 0.85 / 1.00 |
| | S1, August capital (0.801) | 0.67 | 1.88 | 0.18 / 0.55 / 0.90 / 1.00 |
| | S6 Edge-robust (0.558) | 0.97 | **2.71** | 0.11 / 0.30 / 0.62 / 0.96 |
| | S1 winsorised (0.598) | 0.90 | 2.52 | 0.12 / 0.34 / 0.68 / 0.98 |
| | S1 without top 10 (0.426) | 1.27 | 3.54 | 0.08 / 0.20 / 0.41 / 0.81 |
| | Large/mid 2025 (0.389) | 1.41 | 3.95 | 0.07 / 0.17 / 0.34 / 0.72 |
| Award, days -5 to +5 (11 d), c = 1.3 | S1 | 1.12 | 3.14 | 0.09 / 0.24 / 0.50 / 0.90 |
| | S6 | 1.47 | 4.12 | 0.07 / 0.16 / 0.32 / 0.69 |
| Transfer, 30 d, c = 1.0 | S1 | 1.42 | 3.98 | 0.07 / 0.16 / 0.34 / 0.72 |
| | S6 | 1.87 | 5.24 | 0.06 / 0.11 / 0.22 / 0.49 |
| Transfer, 42 d, c = 1.3 | S1 | 2.19 | 6.13 | 0.05 / 0.09 / 0.17 / 0.38 |
| | S6 | 2.88 | 8.06 | 0.04 / 0.07 / 0.12 / 0.24 |

Benchmarks for b: DLST aggregate elasticity -0.45 implies b ≈ 2.2 (p. 3736); DLST Table 11 day-3 slope 3.61, day-1 0.71 (p. 3744); Chang, Hong and Liskovich elasticities -0.46 to -1.5 imply 0.7 to 2.2 (as cited in the pressure test, **NOT VERIFIED** here). Two caveats (JUDGEMENT): at the award only the expected part of the eventual impact should be priced, so the relevant b may be a fraction of the full multiplier; and the award was partly anticipated (Placera published an at-risk list on 26 May 2026), so the window must open before day 0. The single-event SE (0.73 to 0.97) is about half of DLST's own day-3 SE (1.53 on 15 events), because the Swedish FIP dispersion per event is large. A pooled two-event design adds the large/mid round: √(9.6² + 5.0²) ≈ 10.9 in the denominator instead of 9.6, MDE about 1.8 in S1 (JUDGEMENT arithmetic).

Compared with the pressure test's design D: its MDE of 1.1 to 2.1 "on gross FIT" assumed a FIT sd of 1 pp; its feared 6.3 "if net is a third of gross" does not apply, because net FIP is not smaller than gross FIP.

---

## 5. Risks, each with a solution

| Risk | Evidence | Solution | Solves or reduces |
|---|---|---|---|
| **Netting** | Measured: SEK netting is real (sd ratio 0.58), but in market-cap units net ≥ gross (1.13). The tail depends on Edge's pro-rata scaling and on the water-filling reading of the allocation rule | Report S1 and S6 side by side as pre-registered; add realised-flow FIP from daily TNA for the transfer window; read the procurement instructions for the binding rule | Reduces |
| **Pre-trading** | Q1 vs Q2 vectors correlate 0.95; no July-September holdings before December | Award test as headline (pre-trading cannot precede the award's information, only anticipation); measure anticipation from 26 May; transfer test recast as "was anything left"; losers' monthly top-10 factsheets for July-September | Reduces |
| **Holdings coverage** | 15% of sell capital (Evli, C WorldWide) and one fifth of buy (Danske) missing | S1/S3 bounds; Danske factsheet; SHoF Morningstar holdings request | Reduces; solves only with full foreign holdings |
| **Market-cap date** | Caps are from 5 October 2026, after the award | FinBas caps at day -10 (Wardlaw), free float from LSEG | Solves |
| **Single event** | One date, 174 dependent CARs | Randomisation inference: rerun with the frozen FIP vector on every non-overlapping window 2015-2025; leave-one-stock-out and top-10-excluded estimates; incumbents' pseudo-FIP; second event (large/mid 2025) pooled | Reduces; cannot solve |
| **Timing of transfer data vs 7 December** | PPM August 2026 file was in the repository on 2 October and the September file was not (directory listing: **VERIFIED**), so the lag exceeds one month; the October file will arrive mid- to late November (**NOT VERIFIED**) | Date transfers from daily fund capital (Avanza fund-guide endpoint; SHoF Morningstar daily TNA); keep the award as headline and the transfer as a labelled first look | Fully for the headline; reduces for the transfer test |
| **Expert bar** (course: "replication and extension of a (recent) published paper in a top journal") | DLST's headline aggregate tables cannot be replicated; data-level replication impossible | Frame as replication of DLST Table 11 (and T7, T13) on a new uninformative shock; report numbers beside 0.71, 3.61 and -0.45; state the deviations in one table | Reduces |
| **Pandering perception** | Examiner (Sabbatucci) works on retirement-plan reallocations repricing stocks; tutor (Klug) on index inclusions | Cite each once as framing; justify the design by the netting and MDE numbers, which are computed blind | Reduces |
| **Drift from Klug's prompt** | Prompt lists "market efficiency", so price pressure is in scope; the synopsis promised fees, fund supply, saver behaviour and post-inflow performance | Table 1 keeps fees and default acceptance as descriptives; ask Klug for explicit sign-off at the 9 October meeting with this number | Solves if Klug agrees; otherwise reduces |
| **Anticipation of the award** | Placera's 26 May list; bids known earlier | Window from day -5; surprise-weighted FIP from a P(win) model on fees and past returns (Klug chapter 3 logic) | Reduces |

---

## 6. Verdict on (C), compared with the SSZ dossier

**Go/no-go status: GO on the pre-committed rule, narrowly.** Residual net-FIP sd is 0.73 pp (S1) and 0.56 pp (S6, Edge-robust), above 0.5; 0.43 pp without the ten largest names; never above 1 pp except in the imputed-coverage scenarios (0.90). The award-window MDE is 2.1 (S1) to 2.7 (S6) per pp, inside the range of plausible multipliers. The transfer window is underpowered.

**Strengths (JUDGEMENT).** A real, dated, informationless, pre-announced demand shock; the netting worry is resolved in the design's favour; the per-event precision is about twice DLST's own; the question is squarely "market efficiency" in Klug's prompt and in his index-inclusion expertise; the answer is interesting whether the slope is zero or not.

**Weaknesses (JUDGEMENT).**
1. It is one event. Everything rests on about 20 to 40 stocks with abs(FIP) above 0.5 to 1 pp, and the largest values come from one small fund's assumed behaviour.
2. The replication is method-level. DLST's aggregate headline (Tables 6, 8, 9) has no counterpart; Tables 4 and 10 have none either; no independent Swedish replication is feasible in nine weeks (section 3.3).
3. Inputs still to be secured before 9 October: FinBas daily returns, caps and turnover; the foreign funds' holdings; the binding allocation rule.

**Against SSZ (A).** The SSZ dossier finds the pre-2024 replication of Tables I, II, III, VI, VII and IX powered (Table III MDE 0.110 per year against an implied gap of about 0.20) on data identical in structure to SSZ's, with the FTN extension marginal (MDE 0.655 against an implied 0.674). (A) therefore satisfies the course's "replication" standard at table level and puts the risk in the extension. (C) puts the risk in the headline: a single-event cross-section with 30 to 85% power at plausible effects, and only a method-level replication. On the briefing's evidence about what wins (anchor question equals thesis question, table-level replication, dated reform, numbers compared with the anchor's), (A) scores higher on replication and calibration; (C) scores higher on the dated, reform-based design and on novelty.

**Recommendation.** Keep (A) as the anchor. (C) is a GO only if (i) Klug accepts a Table 11-level replication of DLST as the "replication", (ii) S6 is pre-registered alongside S1, and (iii) FinBas data are confirmed this week. A middle option worth raising with Klug: (A) as anchor, with the (C) award-window cross-section as one powered extension figure, which is what the pressure test's fallback already envisaged.

---

## Appendix: files (all in `scratchpad/anchor_final/round1/da_work/`)

| File | What it is |
|---|---|
| `paper/dlst_2018_key_numbers.txt` | Verbatim DLST numbers with RFS pages; 2015 draft figures |
| `fi_inbrowser_extract.js` | ZIP and XML reader used in the browser pane on fi.se (FI 2026Q1, 2025Q2) |
| `fi26q1_smallcap_vectors.psv` | Per-stock loser sales (March and August capital), new-winner weight sums, incumbents' weight sums, FI 2026Q1 |
| `fi25q2_largemid_vectors.psv` | Per-stock sales and purchases, Sweden active round, FI 2025Q2 |
| `mcap/stockanalysis_sto_20261005_exact.psv` | Exact market caps, 630 Stockholm stocks (≥ SEK 185m plus one) |
| `netting_q1.py` → `log_netting_q1.txt`, `stock_netFIP_q1_smallcap.csv`, `stock_netFIP_q2_2025_largemid.csv` | Go/no-go statistics, scenarios S1-S6, Q1 vs Q2, placebo, large/mid |
| `mde.py` | MDE and power table |
| `parse_fi.py`, `netting_smallcap.py`, `netting_fip.py`, `netting_largemid.py`, `trades_*`, `stock_net_*` | Earlier runs on FI 2026Q2 (small cap) and 2024Q2/2026Q2 (large/mid) holdings with transcribed caps; superseded except as the Q2 comparison |
| `mcap/isin_mcap_smallcap_fixed.csv`, `mcap/match.py`, `mcap/fix_smallcap.py` | ISIN-to-symbol matches (values superseded by the exact file) |

Sources: DLST RFS PDF https://academicweb.nd.edu/~zda/Pension.pdf ; 2015 draft https://www7.uc.cl/economia/finance_uc/docs/conferences/9th/LARRAIN_DLST_2015.pdf ; NBER WP 22161 https://www.nber.org/papers/w22161 ; FI holdings https://www.fi.se/sv/vara-register/fondinnehav-per-kvartal/ ; stockanalysis https://stockanalysis.com/list/nasdaq-stockholm/ ; Pensionsmyndigheten, Effekter av massfondbytesstoppet (2012) https://www.pensionsmyndigheten.se/content/dam/pensionsmyndigheten/blanketter---broschyrer---faktablad/publikationer/svar-p%C3%A5-regeringsuppdrag/2012/Effekter%2Bav%2Bmassfondbytesstoppet%2B120919.pdf
