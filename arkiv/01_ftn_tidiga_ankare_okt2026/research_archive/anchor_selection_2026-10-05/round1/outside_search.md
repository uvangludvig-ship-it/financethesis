# Outside search: is there an anchor better than (A) SSZ 2015, (B) Cookson et al. 2021, (C) Da et al. 2018?

Prepared 5 October 2026 (round 1, resumed run). The earlier runs left `round1/outside_src/` empty, so everything below was re-collected in this run. Benchmark read first: `round1/ssz_dossier.md` sections 0, 2, 5, 7.

Labels: **VERIFIED** = checked in this run against the source named (journal page, RePEc/IDEAS record, publisher page, author CV, or our own files). **NOT VERIFIED** = could not confirm. **JUDGEMENT** = my reasoning. No point estimate of any thesis regression was computed or inspected. The only new numbers computed here are counts and analytic MDEs (section 5).

Access limits met in this run (so readers know what was and was not checked): data.mendeley.com (container proxy: CONNECT 403; WebFetch on the public API: 403), riksrevisionen.se (CONNECT 403; WebFetch robots timeout), nber.org and academic.oup.com (CONNECT 403, from the proxy status log). Abstracts and citations were therefore taken from IDEAS/RePEc, publisher landing pages, author CVs and accepted manuscripts.

---

## 0. Bottom line

1. **No outside candidate beats all three of A, B and C.** None beats A at all on the combined criteria.
2. The structural reason is the same for every outside paper. Any test that needs FTN variation runs into the same constraints: 81 sponsor decisions in 6 rounds, a median dose of 6% of AUM, short post-periods, and noisy outside-PPM flows. So an outside anchor can only win through a better powered, FTN-independent replication (criterion 2) **plus** a closer question (criterion 1). On data we already hold, only two outside papers clear criterion 2:
   - Cooper, Halling and Yang (2021 RoF). Its question fits worse than A's, and its FTN headline is mechanical inside PPM and unpowered outside PPM.
   - Tran and Wang (2023 JFE). The part of it that can be run on our data is A's Table III data under a different specification.
3. **Best outside candidates, in order:**
   - Cooper, Halling and Yang (2021 RoF), a fee-dispersion design.
   - Armstrong, Genc and Verbeek (2019 MS), on Morningstar analyst ratings. Its replication data are not in our files.
   - Jenkinson, Jones and Martinez (2016 JF), on consultant recommendations. It is dominated by B, the same authors' newer platform paper.
   - Tran and Wang (2023 JFE). This is a partner for A, not a rival.
4. **Useful by-products for the chosen design (JUDGEMENT):**
   - Use Tran and Wang (2023) and Kronlund et al. (2021) as A's recency partners.
   - Add a CHY-style residual fee-dispersion panel to A's Table I. Fee data are monthly from 2006 (section 2.1).
   - Run a JJM/Cookson-style bid-level selection table: 290 bids, 75 winners, analytic MDE about 0.07 in win probability per SD (section 5).
   - Use Johansson, Sabbatucci and Tamoni (2025 RoF) tradable factors for any performance table. That paper is by the examiner.
   - Note that Riksrevisionen has an ongoing audit of FTN. This matters for novelty and as a source.

---

## 1. Search coverage (what was checked)

| Group | Item | Status in this run |
|---|---|---|
| Pension menus and flows | Tran and Wang 2023 JFE; replication package | Citation and abstract VERIFIED; package contents NOT VERIFIED (blocked), section 3.4 |
| | Kronlund, Pool, Sialm, Stefanescu 2021 JFE | VERIFIED (RePEc) |
| | Christoffersen and Simutin 2017 RFS | Citation VERIFIED in SSZ dossier §2.2; not re-fetched |
| | Chalmers and Reuter 2020 JFE | VERIFIED (RePEc) |
| | Egan, Ge and Tang 2022 RFS | VERIFIED (abstract; volume not shown) |
| | Bhattacharya, Illanes and Padi 2025 Econometrica | VERIFIED (RePEc) |
| | Choukhmane 2025 AER | VERIFIED (RePEc) |
| | Cohen and Schmidt 2009 JF | Citation VERIFIED via RePEc handle v64y2009i5p2125-2151; content not re-read |
| | 2020-2026 menu, mapping and fee papers | Badoer, Costello and James 2020 JFE (VERIFIED); Pool, Sialm and Stefanescu 2026 MS revenue sharing (VERIFIED, Sialm CV); no top-journal paper on post-deletion "mapping" found |
| Gatekeepers | Kaniel and Parham 2017 JFE | VERIFIED (RePEc) |
| | Hartzmark and Sussman 2019 JF | Citation VERIFIED (RePEc handle v74y2019i6p2789-2837) |
| | Ben-David, Li, Rossi and Song 2022 RFS | Citation VERIFIED (RePEc handle v35y2022i4p1723-1774) |
| | Evans and Sun 2021 RFS | Citation VERIFIED (RePEc handle v34y2021i1p67-107) |
| | Goyal, Wahal and Yavuz 2024 JFQA | VERIFIED (Cambridge page) |
| | Jenkinson, Jones and Martinez 2016 JF | VERIFIED (accepted manuscript; JF pages 2333-2369) |
| | Armstrong, Genc and Verbeek 2019 MS | VERIFIED (abstract, pages 2310-2327, DOI 10.1287/mnsc.2017.2884) |
| | Public agency selection: YFYS, UK VfM and charge cap, Chile, Mexico, Israel | No top-journal empirical paper found (section 4) |
| Fees | Hortaçsu and Syverson 2004 QJE | Not re-verified (NBER w9728 only); fails recency anyway |
| | Cooper, Halling and Yang 2021 RoF | Local text read (`cooper_halling_yang_2021.txt`) |
| | Fee spillovers from negotiated or platform fees to retail classes | No top-journal paper found |
| Price pressure | Sabbatucci, Tamoni and Xiao WP | Status VERIFIED as unpublished (Inquire Europe page) |
| | Hartzmark and Solomon | **Published:** "Market-Wide Predictable Price Pressure", AER 115(9), 2025, 3171-3213 (VERIFIED, RePEc) |
| Swedish PPM | Dahlquist, Martinez and Söderlind 2017 RFS | VERIFIED (DOI 10.1093/rfs/hhw093, from p. 866) |
| | Dahlquist, Setty and Vestman 2018 JF | VERIFIED (pp. 1893-1936) |
| | Cronqvist, Thaler and Yu 2018 | AEA P&P, DOI 10.1257/pandp.20181096 (VERIFIED) |
| | Cronqvist and Thaler 2004 | NOT re-verified |
| | Anderson and Robinson 2022 RoF | VERIFIED: "Financial Literacy in the Age of Green Investment", RoF 26(6), 1551-1584 (Anderson CV 2025). Not about FTN. |
| | FTN work 2024-2026 | Riksrevisionen ongoing audit (section 4); Kinnerud and Lorentzon (AEJ: Applied) |
| Open search | | Hong, Lu and Pan 2025 MS; Greenwood and Sammon 2025 JF; Johansson, Sabbatucci and Tamoni 2025 RoF |

---

## 2. Serious candidates (full template)

Ratings are High / Medium / Low on the brief's six criteria (JUDGEMENT). "A, B, C" refer to the brief's candidates.

### 2.1 Cooper, Halling and Yang (2021), "The Persistence of Fee Dispersion among Mutual Funds", Review of Finance

**Citation and source.**
- Local text: `/mnt/user-data/uploads/financethesis_ny/research/anchor_review/sources/cooper_halling_yang_2021.txt`. This is the May 2020 version; the journal volume and pages were not re-checked in this run.
- Halling is at SSE/SHoF (line 23).

**Exact question (VERIFIED, lines 104-108).** "The first is to determine which viewpoint — fees matter to investors or fees do not matter — is on average evident in the data. The second goal, conditional on finding that fees do matter, is to examine the competitiveness of the mutual fund markets via an examination of mutual fund pricing."

**Design and tables (VERIFIED from the text).**
- Data: CRSP Mutual Fund Database equity funds (line 351), 1980-2017 (lines 151, 226), with share-class data and institutional classes from 1999 (line 381).
- Table I: summary statistics.
- Table II: annual net-of-fee alphas regressed on fees and controls (line 487).
- Table III: fee regressions for S&P 500 index funds, all index funds, all active funds and large funds (lines 555-558).
- Table IV: residual fee dispersion, with 25-75 and 10-90 spreads (lines 699, 814-817).
- Table V: extended expense models (line 778).
- Table VI: Berk-van Binsbergen gross and net value added, and misallocated capital (lines 926-1093).
- Abstract (lines 50-55): a "strong negative association between net-of-fee fund performance and fees", dispersion that is "economically large, robust, persistent, and pervasive", and total value lost of USD 125bn.

**Replication availability.**
- No public package found. The original needs CRSP (WRDS access for this group is NOT VERIFIED).
- A Swedish different-data replication is feasible on data in hand (VERIFIED in this run from `data/pa_panel_raw.pkl`): `fee_net` and `fee_gross` exist monthly for essentially all PPM funds.
  - 2006: 7,567 of 8,328 rows.
  - 2007-2010 and 2012-2023: 99% or more of rows.
  - 2011: only 3,212 of 9,496 rows (a gap to repair).
  - 2019-2023: 490 to 802 funds per year.
  - Morningstar fee snapshots: `audit/fees.pkl`, 347,401 rows, by share class and prospectus date.
  - Returns for Table II: SHoF `tri_sek`, 2018 onward only. The PPM-file returns are integer-rounded (SSZ dossier, risk 5).

**How FTN enters its tables (JUDGEMENT).**
- Table III gets a "procured" indicator and an "FTN-procured fee" column.
- Table IV becomes a category-by-month residual-dispersion panel, before and after each round's admission month, with not-yet-procured categories as controls.
- Table II/VI compares the net alpha of winners and removed funds before and after.
- The PPM data separate the fund's gross fee from the fee net of the PPM rebate. That lets the thesis show what PPM's pre-2024 rebate model already did to dispersion, before FTN replaced it.

**Power on our data (JUDGEMENT).**
- Fees are observed without sampling error at the fund-month level. Dispersion statistics are therefore precise, and the replication is powered.
- The FTN headline inside PPM is mechanical: procured fees are contract terms. It is "powered" but uninformative.
- The non-mechanical versions are weak:
  - Spillover to the same funds' fees outside PPM: list-fee changes are rare and lumpy, and there are 81 decisions.
  - Competitive response of not-yet-procured funds: plausible, but bidders quote a separate procured fee, so the list fee need not move.
- I did not estimate MDEs for these. **NOT VERIFIED.**

**Feasibility.** High. The data are in hand and the fee-panel code is straightforward. The 2011 gap and the definitions of fee_net and fee_gross must be checked against the file headers.

**Biggest risk.** The examiner reads the FTN extension as "procurement lowered procured fees", which is true by construction. The non-mechanical spillover is the interesting part and is likely underpowered.
- Mitigation: headline the pre-2024 Swedish replication ("did PPM's rebate model compress dispersion; is residual dispersion persistent among near-identical index funds?"). Report FTN as a bounded descriptive column.
- This only reduces the risk; it does not solve it.

**Ratings.** (1) Medium. (2) High. (3) Medium-High. (4) High: RoF 2021, about 5 years old. (5) High: "fees" is in Klug's prompt and the synopsis promised fees on and off the platform. (6) Low-Medium: the informative test is the spillover, which is unpowered.

**Versus A, B, C (JUDGEMENT).**
- **vs A:** Equal on criterion 2: both have pre-2024 Swedish replications, and CHY's is even easier. Worse on criterion 1: CHY's question is fee dispersion, not who allocates money. Worse on criterion 6: A's FTN column, sponsor flow on rank, has an MDE of 0.655 against an SSZ-sized effect of 0.674 (SSZ dossier §5); CHY's FTN column is either mechanical or unpowered. **A wins.**
- **vs B:** Better on criterion 2: B's replication is FTN-dependent. Worse on criterion 1: B asks the selection-and-demand question directly.
- **vs C:** Better on criteria 2 and 5. Worse on fit to Klug's own research, which is price elasticities and index inclusion.
- **Best use:** as a Table I panel inside A (fees on and off the platform), not as the anchor.

### 2.2 Jenkinson, Jones and Martinez (2016), "Picking Winners? Investment Consultants' Recommendations of Fund Managers", Journal of Finance (2016), pp. 2333-2369

**Citation and source.**
- Pages from the SUFE academic newsletter record; volume 71 by year (issue not verified).
- Accepted manuscript: https://www.stat.berkeley.edu/~aldous/157/Papers/jenkinson.pdf

**Exact question (VERIFIED, abstract).** "we analyze the factors that drive consultants' recommendations, what impact these recommendations have on flows, and how well the recommended funds perform."

**Design and magnitudes (VERIFIED from the accepted manuscript via the fetch tool; table numbers are from that version).**
- Data: Greenwich Associates survey, 1999-2011, with eVestment and IIS data. On average 1,919 products a year, 21% recommended, 29 consultants a year.
- Table III (Poisson, determinants of recommendations): soft factors dominate past performance. Moving soft investment factors from the bottom to the top percentile adds +5.78 recommendations; return rank adds +0.56.
- Table IV: going from zero to full recommendation adds about USD 2.4bn of flows (t = 2.75), or 29% growth (t = 4.35).
- Table V: equal-weighted net three-factor alpha is 0.39% for recommended products and 1.36% for others; the difference is -0.97%. Value-weighted, there is no significant difference.

**Replication availability.** None. Greenwich and eVestment data are proprietary. There is no Swedish gatekeeper dataset before 2024.

**How FTN enters.** Very naturally:
- Table III becomes a bid-level P(win) regression on past performance, fees and size, alongside FTN's own quality score.
- Table IV becomes winner inflows (mechanical inside PPM; outside PPM as in B).
- Table V becomes winners versus removed funds after the award.

**Power on our data.**
- Selection table: about 0.07 per SD at bid level (section 5; analytic).
- Performance table: MDE 2.5-4.3 pp per year (SSZ dossier §5, `ftn_t9_power.py`).
- Flows outside PPM: MDE 6-7% of non-PPM assets over six months (SSZ dossier §5).

**Feasibility.** High for the FTN tables. There is no replication.

**Biggest risk.** No table-level replication outside FTN. This fails the course standard unless the "FTN as different data" reading is accepted, which is the same issue B has.

**Ratings.** (1) High. (2) Low. (3) High. (4) Medium-High (JF 2016). (5) Medium-High. (6) Low-Medium.

**Versus A, B, C.**
- **vs B:** Strictly dominated. B, by the same three authors plus Cookson, is newer (2021 RFS), is about a retail platform (closer to FTN), and has the same three-table structure.
- **vs A:** Loses on criteria 2 and 6.
- **vs C:** Better question fit; worse on Klug's expertise.
- **Best use:** cite as the institutional-gatekeeper precedent for B's or A's selection table.

### 2.3 Armstrong, Genc and Verbeek (2019), "Going for Gold: An Analysis of Morningstar Analyst Ratings", Management Science, pp. 2310-2327

**Citation and source.** DOI 10.1287/mnsc.2017.2884 (VERIFIED: SUFE record and Erasmus repository, https://repub.eur.nl/pub/113161).

**Exact question (VERIFIED, abstract).** Do Morningstar's "qualitative, forward-looking analyst ratings" attract flows and predict performance? Published findings: "relatively higher flows to funds receiving higher ratings" and "investors would have earned significantly higher returns ... by investing in funds with the highest analyst conviction."
- **Caution:** a CXO Advisory summary of an earlier version (ratings September 2011 to December 2012, performance to June 2013) reports no outperformance. The published sample and tables are **NOT VERIFIED**. Cite only the published abstract.

**Why it is interesting (JUDGEMENT).** FTN's score is 75% quality, judged qualitatively on organisation, process and team, much like Morningstar's pillar-based analyst rating. The thesis question "does a qualitative expert assessment pick better funds, and does money follow it?" is AGV's question, with FTN as a public-sector analyst.

**Replication availability.**
- No package.
- A Swedish pre-2024 replication would need the history of Morningstar Analyst Ratings for Swedish-sold funds. **VERIFIED absent from our files:** `fundmaster.pkl` (57 columns), `fees.pkl` (12 columns) and the SHoF field definitions have no rating, star, medal or analyst field.
- Whether SHoF can export rating histories is **NOT VERIFIED**.
- From general knowledge, NOT VERIFIED in this run: Morningstar replaced the Analyst Rating with the Medalist Rating around 2021-2023, which would break the series.

**How FTN enters.**
- An FTN-award column in AGV's flow and performance tables.
- A new concordance table: P(FTN win) on Morningstar rating among bidders, i.e. does FTN add information beyond Morningstar?

**Power.**
- The concordance table is at bid level (about 0.07-0.11 per SD; section 5).
- Performance is the same as in 2.2 (unpowered).
- Replication power: unknown without the data.

**Feasibility.** Low until the rating history is confirmed, then Medium.

**Biggest risk.** The data do not exist in usable form.
- Mitigation: ask SHoF this week whether Morningstar Direct rating histories (Analyst/Medalist, stars) can be exported for SEK funds from 2011.
- This fully solves the risk if yes; if no, the candidate dies.

**Ratings.** (1) Medium-High. (2) Low as things stand (High if the data appear). (3) Medium-High. (4) Medium-High (MS 2019). (5) Medium. (6) Low-Medium.

**Versus A, B, C.**
- **vs B:** Better than B only if the ratings exist, because the replication would then be pre-2024.
- **vs A:** Never better than A on present evidence.
- **vs C:** Better on question fit; worse on data.
- **Best use:** a robustness control (Morningstar rating) in B's or A's selection table, if SHoF can supply it.

### 2.4 Tran and Wang (2023), "Barking up the wrong tree: Return-chasing in 401(k) plans", JFE 148(1), 69-90

**Citation.** VERIFIED in SSZ dossier §2.1. In this run, ScienceDirect (https://www.sciencedirect.com/science/article/abs/pii/S0304405X23000314) and SSRN 3502862 (77 pages) confirmed the abstract and the "hand-collection ... from annual Form 11-K filings", 1,551 firms, 1993-2016.

**Exact question (VERIFIED, abstract).** Why do "fund flows respond to returns at the plan level but to CAPM alpha at the aggregated fund level"? Answer: 83% of investors, holding 39% of assets, chase returns; wealthier and more literate investors follow CAPM alpha.

**Replication package (criterion asked explicitly).**
- VERIFIED: Mendeley Data, "Code and data for 'Barking Up The Wrong Tree: Return-chasing in 401(k) Plans'", DOI 10.17632/8tyd2z7xgr.1, contributor Pingle Wang, published 14 February 2023. Description: "The directory contains code and data used for the paper". A `readme.txt` with "detailed steps to reproduce the results" is referenced.
- **NOT VERIFIED:** the file tree, sizes, and whether CRSP, Morningstar or factor inputs are included. Attempts this run:
  - container curl to the dataset page and the public API: CONNECT 403;
  - WebFetch on `public-api/datasets/8tyd2z7xgr` and `/files?folder_id=root&version=1`: 403;
  - WebFetch on the landing page: description only;
  - search for the DOI string: no mirror;
  - Wang's site (https://wangpingle.com/): no data links;
  - the ScienceDirect fetch: no data-availability statement visible.
- JUDGEMENT: the hand-collected 11-K panel is probably included (it is their own data). CRSP fund returns and Morningstar ratings are licensed and probably not redistributed. So re-running the tables would likely require WRDS. Whether the tables can be re-run without licensed data is unknown.
- Solution: download `readme.txt` from a normal browser on the SSE network (a 2-minute task for the user), or email the author (address on his site).

**How FTN enters.** As a horse race of FTN selection on raw return versus CAPM alpha versus fees. This is A's Table VIII column with a different right-hand side.

**Power.**
- Replication of the PPM flow-performance horse race: powered (8,033 fund-months, 2019-2023; SSZ dossier §5).
- FTN horse race: about A's MDE (0.655 on rank; LPM 0.436 worst-to-best).

**Ratings.** (1) Medium-Low: the thesis question is not wealth-driven return-chasing. (2) Medium: Swedish replication of the flow-performance part is feasible; the package is unknown. (3) Medium. (4) High. (5) Medium-High. (6) Medium-Low.

**Versus A, B, C.**
- **vs A:** A variant of A without SSZ's sponsor-versus-participant framing, which is the part FTN actually changes. As a partner it fixes A's recency weakness (risk 2 in the SSZ dossier), and it shows that the SSZ decomposition is live in a 2023 JFE paper. **A plus TW is better than TW alone.**

### 2.5 Kronlund, Pool, Sialm and Stefanescu (2021), "Out of sight no more? The effect of fee disclosures on 401(k) investment allocations", JFE 141(2), 644-668

**Citation.** VERIFIED (RePEc).

**Exact question (VERIFIED, abstract).** Did the 2012 fee- and performance-disclosure mandate change participants' choices? "participants became significantly more attentive to expense ratios and short-term performance after the reform."

**Design.** A regime change with plan-by-fund panels (11-K and plan data).

**Replication.** Not feasible in nine weeks. The data are hand-collected 11-K; no package was found.

**FTN fit.** A dated regime change, but one that changes participants' information, not the existence of a sponsor. A Swedish analogue is "do PPM savers' flow sensitivities change after FTN?" The SSZ dossier's regime column has MDE 0.042-0.046 per month, against 0.008 for the same categories in 2019-2023 (`regime_power.py`). That is unpowered.

**Ratings.** (1) Medium-Low. (2) Low. (3) Medium. (4) High. (5) Medium. (6) Low.

**Versus A.** A cites it as the closest published "SSZ decomposition around a regime change" (SSZ dossier §2.2). Not a rival.

### 2.6 Kaniel and Parham (2017), "WSJ Category Kings - The impact of media attention on consumer and mutual fund investment decisions", JFE 123(2), 337-356

**Citation.** VERIFIED (RePEc).

**Question and design (VERIFIED, abstract).** A regression discontinuity around the WSJ "Category Kings" cutoff: a "31% local average increase in quarterly capital flows" to listed funds against near-misses, about seven times the performance-only flow effect, with spillovers to the same family.

**FTN fit.** Certification of winners, which is B's outside-PPM question with a discontinuity design.

**Power (VERIFIED input, JUDGEMENT conclusion).** FTN's reports leave very few near-misses. Example from the brief: Europe active 2024 had 35 submissions, 10 fully evaluated and 6 winners, so about 4 near-misses. An RD across 6 rounds has perhaps 25-40 near-cutoff funds, too few. The Swedish outcome (outside-PPM flows) is also noisy (median residual 35%).

**Replication.** Needs hand-collected WSJ lists and CRSP; no Swedish analogue.

**Ratings.** (1) Medium. (2) Low. (3) Low-Medium. (4) High. (5) Medium. (6) Low.

### 2.7 Hartzmark and Solomon (2025), "Market-Wide Predictable Price Pressure", AER 115(9), 3171-3213

**Status.** VERIFIED: the NBER WP "Predictable Price Pressure" (w30688, 2022) is published in the AER under this title.

**Abstract (VERIFIED).** Predictable dividend-reinvestment flows forecast aggregate market returns, with a "market-level price multiplier of 1.9", and the pattern holds internationally.

**Replication.** AEA supplementary materials are listed (aeaweb.org/articles/materials/23797 and 23798). Contents and data licensing are **NOT VERIFIED**.

**FTN fit (JUDGEMENT).** FTN transfers are predictable, uninformed flows, which matches Klug's front-running and index-reconstitution work and the examiner's STX working paper. But the published paper is market-level. FTN flows net largely within category (removed funds sell, winners buy similar stocks), so market-level FTN demand is close to zero. The stock-level version is C's design. HS strengthens C's motivation and offers a pre-FTN replication (a market-level dividend-day test on Swedish data). It does not fix C's FTN power.

**Ratings.** (1) Medium (for a price-pressure thesis). (2) Medium: the package exists; Swedish dividend data access NOT VERIFIED. (3) Low. (4) High. (5) Medium-Low: drifts from "effects of FTN on funds and savers". (6) Low.

**Versus C.** A possible recency partner for C, not a replacement.

---

## 3. Candidates screened out (one line each, with the verified reason)

| Paper | Verified content | Why not an anchor (JUDGEMENT) |
|---|---|---|
| Goyal, Wahal and Yavuz (2024), "Choosing Investment Managers", JFQA 59(8), 3531-3563 | Connected managers are more likely to be hired; connections give no higher post-hiring returns | The question is connections. FTN is a non-conflicted public procurer with no counterpart. Mercer-type data are proprietary. The hire/fire performance structure (Goyal and Wahal 2008 JF 63(4) 1805-1847) is useful for the performance table only. |
| Chalmers and Reuter (2020), JFE 138(2), 366-387 | Oregon ORP: brokers removed and TDFs added; new participants move to TDFs | A plan-design change, but it needs individual administrative data. PPM individual data are not obtainable in nine weeks. |
| Egan, Ge and Tang (2022), RFS (pages from 5334) | Variable annuities: after the 2016 DOL fiduciary proposal, sales of high-expense products fell 52% | Broker conflicts; no FTN mapping |
| Bhattacharya, Illanes and Padi (2025), Econometrica 93(4), 1449-1480 | State fiduciary duty raises risk-adjusted returns 25 bp and reduces entry 16% | Advice market, structural; no mapping |
| Choukhmane (2025), AER 115(11), 3749-3787 | Auto-enrolment effects fade by 36 months; switching cost about USD 250 | Savings defaults, not fund selection |
| Cohen and Schmidt (2009), JF 64(5), 2125-2151 | (content not re-read) Trustee fund families | Conflict channel absent in FTN |
| Christoffersen and Simutin (2017), RFS 30(8) | Sponsor-monitored funds tilt to high beta (SSZ dossier) | At most a secondary risk-taking test; underpowered post-period |
| Badoer, Costello and James (2020), JFE 136(2), 471-489 | The 2012 disclosure shifted indirect to direct fees, cut fees for small plans, and created retirement share classes | Fees regime change; Form 5500/Schedule C data heavy; FTN fees are contractual |
| Pool, Sialm and Stefanescu (2026), "Mutual Fund Revenue Sharing in 401(k) Plans", MS 72(7), 5698-5722 (Sialm CV) | Revenue sharing | No FTN counterpart |
| Hartzmark and Sussman (2019), JF 74(6), 2789-2837 | Morningstar globes and flows | Sustainability question; no globe history in our data; SHoF data start in 2018 |
| Ben-David, Li, Rossi and Song (2022), RFS 35(4), 1723-1774 | Flows follow Morningstar stars, not alpha | No star history in our files (VERIFIED, section 2.3); FTN part reduces to A's horse race |
| Evans and Sun (2021), RFS 34(1), 67-107 | Morningstar methodology change | US-only design; no FTN mapping |
| Hong, Lu and Pan (2025), "Fintech Platforms and Mutual Fund Distribution", MS 71(1), 488-517 | Staggered entry onto Chinese fintech platforms raises performance chasing; managers take more risk | Platform entry, not removal by a procurer; Chinese data |
| Greenwood and Sammon (2025), "The Disappearing Index Effect", JF 80(2), 657-698 (RePEc handle) | (content not re-read) | Stock-index inclusion; relevant only to C's framing |
| Hortaçsu and Syverson (2004), QJE | Search costs and fee dispersion in S&P 500 funds (NBER w9728) | 22 years old: fails "recent"; CHY supersedes it |
| Sabbatucci, Tamoni and Xiao (WP) | VERIFIED unpublished. Per the Inquire Europe summary, which is secondary and has no page reference: BrightScope Beacon data; 401(k) passive share about 40% of equity assets by 2020; a 10% rise in 401(k) demand raises prices 3.5-4% | Fails criterion 4. The examiner's own paper, so cite it in A's motivation (sponsor-driven shifts) and in C's. |
| Johansson, Sabbatucci and Tamoni (2025), "Tradable Risk Factors for Institutional and Retail Investors", RoF 29(1), 103-139 | Tradable factors from funds and ETFs; implementation shortfall 2-4% a year | A measurement tool, not an anchor. Use it to benchmark winners versus removed funds in any performance table: examiner fit. |
| Dahlquist, Martinez and Söderlind (2017), RFS (DOI 10.1093/rfs/hhw093) | Active PPM investors outperform; extreme outflows hurt NAVs; advisors coordinate flows | Individual PPM data; cite it for "performance after large flows" |
| Dahlquist, Setty and Vestman (2018), JF, 1893-1936 | Default fund asset allocation | Calibration of the AP7 design; not FTN |
| Cronqvist, Thaler and Yu (2018), AEA P&P | Inertia in the default | P&P, not a full paper; motivates the 85-95% default acceptance |
| Anderson and Robinson (2022), RoF 26(6), 1551-1584 | Green investment and literacy | Off-topic. Their SHoF WP "Who Feels the Nudge?" uses PPM-linked survey data (individual level). |
| Kinnerud and Lorentzon, "Dominated pension investments: the role of search frictions and unawareness", AEJ: Applied (DOI 10.1257/app.20240153; abstract via AEA 2023 programme) | Field experiment in the Swedish pension system: letters about dominated high-fee index funds; awareness and search costs explain "at most 45 percent" of dominated choices | Very close to FTN's index rounds, which removed high-fee index funds. Individual experimental data, and AEJ: Applied is not on the brief's journal list. Cite it in the index-round discussion. |

---

## 4. Public agencies that select, certify or delist funds (the brief's open question)

- **Australia, Your Future Your Super performance test.**
  - Found: APRA results pages, Treasury consultations (2024), the Grattan Institute submission "The superannuation performance test is performing" (2024), and a Climateworks briefing (2025).
  - **No peer-reviewed top-journal paper found** in two extended searches.
  - JUDGEMENT: the closest institutional analogue (a regulator tests products; failures must notify members), but there is no anchor.
- **UK value-for-money regime and charge cap.** Only FCA, consumer-panel and DWP survey material; no top-journal paper found.
- **Chile.** "Can auctions increase competition in the pension funds market? The Chilean experience", Journal of Policy Modeling 45(5), 2023, 975-993 (RePEc handle). Not a top journal.
- **Mexico.** Hastings, Hortaçsu and Syverson (2017), Econometrica (Nov 2017), on sales force and competition. It is about demand elasticity, not procurement. Pages NOT VERIFIED.
- **Israel.**
  - The 2016 default-fund tender: press coverage only (Haaretz).
  - Hamdani, Kandel, Mugerman and Yafeh, "Incentive Fees and Competition in Pension Funds", Journal of Law, Finance, and Accounting 2(1), 2017, 49-86: not top, and not about tenders.
- **Sweden, 2024-2026.**
  - Riksrevisionen has an **ongoing audit, "Ett upphandlat fondtorg för premiepensionen"** (title VERIFIED in search results; the page itself is blocked here).
  - Per News55 (1 October 2026, secondary): it examines whether FTN and Pensionsmyndigheten created conditions for an efficient transition. It studies "two completed and well-documented procurements" on site. As of May 2026 only one-third of fund assets had been procured. Publication date NOT VERIFIED.
  - JUDGEMENT: no academic paper on FTN found. The audit is both a novelty risk, since it may publish before 7 December, and a citable source. Check its status before writing the contribution paragraph.

Bounded conclusion: I found **no published top-journal paper in which a regulator or public agency selects, procures, certifies or delists funds**. FTN is close to unique as a setting, which helps novelty but means no anchor asks exactly the FTN question.

---

## 5. Power numbers used above

From the SSZ dossier §5 (VERIFIED there; not re-run):
- FTN sponsor-flow slope: MDE 0.655 (N = 81).
- Selection LPM: 0.436 from worst to best rank.
- FTN performance: 2.5-4.3 pp per year.
- Non-PPM spillover: 6-7% over six months.
- Regime column: 0.042-0.046 per month.
- PPM replication: Table III linear 0.0059 per month.

New in this run:
- **Bid counts (VERIFIED, `round1/cookson_work/bids_long.csv`):** 290 bids in 11 rounds, 75 winners, 108 PPM incumbents. 147 bids are matched to SHoF, 62 of them winners. The global active round (99 bids) is under appeal (brief).
- **Bid-level selection MDE (JUDGEMENT, analytic):** linear probability model, one standardized regressor, MDE = 2.8 x sqrt(p(1-p)/N).
  - All bids: p = 0.259, N = 290, MDE = **0.072** change in win probability per SD.
  - SHoF-matched: p = 0.422, N = 147, MDE = **0.114** per SD.
  - Round fixed effects and clustering by round (11 clusters) will raise these. Treat them as lower bounds; randomization inference within round is the honest test.
  - This is the one FTN-side test that every gatekeeper anchor (JJM, AGV, Cookson) shares, and it is better powered than the 81-decision version because it uses all bidders.
- **Fee data coverage (VERIFIED, `data/pa_panel_raw.pkl`):** fee_net and fee_gross are monthly from 2006 to 2026, with 2011 partial (table in section 2.1).

---

## 6. Ranked top five overall (A, B, C included)

1. **(A) SSZ 2015 JF, with Tran and Wang 2023 JFE and Kronlund et al. 2021 JFE as recency partners.**
   - The only design with a powered, FTN-independent table-level replication: Table III linear MDE 0.110 per year against an implied gap of about -0.20; Table IX is powered.
   - It puts FTN inside the anchor's own table (Table VIII sponsor column) and asks a question FTN genuinely changes (a sponsor is introduced into a participant-only system).
   - Additions from this search: TW and KPSS for recency; a CHY-style fee-dispersion panel in Table I; JSZ tradable factors in Table IX.
   - Weakness unchanged: the FTN column is powered only against SSZ-sized sponsor sensitivity.
2. **(B) Cookson et al. 2021 RFS.**
   - Best question fit for "what does FTN select on and does money follow outside PPM".
   - Its powered test (selection) improves at bid level (MDE about 0.07 per SD).
   - Loses to A because its replication needs FTN itself and its demand test is unpowered (8-12% power in the earlier analysis).
3. **Cooper, Halling and Yang 2021 RoF.**
   - The best outside candidate: a pre-2024 replication on fee data in hand, an SSE co-author, and "fees" in Klug's prompt.
   - Loses to A and B on question fit, and its FTN headline is mechanical.
   - Better used inside A than as the anchor.
4. **(C) Da et al. 2018 RFS.**
   - Fits Klug's expertise and the examiner's working paper, and Hartzmark and Solomon (AER 2025) now gives it a published, recent partner.
   - The brief's concerns stand (netting, few events, no FTN-independent replication, drift from the prompt).
   - **This rank is conditional on the C dossier's netting result, which I did not inspect.**
5. **Armstrong, Genc and Verbeek 2019 MS.**
   - Strong conceptual fit (FTN as a qualitative analyst rating).
   - Viable only if SHoF can export Morningstar rating histories for SEK funds. That is unverified and possibly broken by Morningstar's switch to the Medalist rating.
   - Jenkinson, Jones and Martinez 2016 JF would be sixth: same structure as B, older, no replication.

---

## 7. Does any outside candidate beat all three?

**No.**
- **Cooper, Halling and Yang** beats B and C on criterion 2, but loses to A on criteria 1, 3 and 6.
- **Armstrong, Genc and Verbeek** could beat B on criterion 2 only if the rating data materialise. Even then it ties A at best on criterion 2 and loses on criterion 6, because its FTN performance table has the same 2.5-4.3 pp MDE.
- **Jenkinson, Jones and Martinez** is dominated by B.
- **Tran and Wang** is a component of A.
- **Kaniel and Parham** and **Hartzmark and Solomon** fail criterion 3 or 6 on FTN's numbers.

Since no outside paper wins, no full outside design is given. What would change the verdict:

1. **SHoF confirms Morningstar Analyst/Medalist rating histories for SEK funds from about 2011.** AGV then becomes a genuine rival to B: a pre-2024 replication, with FTN as a second qualitative rater. Next step: email SHoF data support this week. One reply decides it.
2. **The Tran-Wang `readme.txt` shows the full input data (including returns) are bundled.** An original-data replication of TW would then be possible, and TW plus a PPM horse race could rival A on criterion 2 (original-data replication is rare and valued). Next step: download the readme on the SSE network. Even then, TW's question fits worse than A's, so I expect it to stay a partner.
3. **Riksrevisionen publishes before the thesis.** This does not change the anchor, but the novelty paragraph and the FTN facts should then cite the audit.

---

## 8. Risks from this search, with solutions

| Risk | Solution | Fully solves or reduces |
|---|---|---|
| The Tran-Wang package is unread, so the claim "TW is a replicable recency partner" is unsupported | Cite TW only for using SSZ's decomposition (VERIFIED in the SSZ dossier); read the readme on the SSE network before claiming anything about re-running it | Fully solves the claim risk |
| Riksrevisionen may pre-empt descriptive FTN findings | Check the audit page before submission; frame the thesis contribution as estimates inside SSZ/Cookson tables, which an audit will not produce | Reduces |
| The published AGV results differ from the working-paper summary | Cite only the published abstract; do not quote the WP sample | Fully solves |
| Using CHY inside A adds scope | Limit it to one Table I panel (residual fee dispersion, PPM rebate model, procured fees); no new regressions | Fully solves scope creep |
| The bid-level selection MDE is analytic, not estimated, and ignores round clustering | Re-compute with round FE and randomization inference within round before relying on it; report it as a bounded test | Reduces |
| The fee_net and fee_gross definitions are unverified against file headers; 2011 coverage is a third | Read the "Fondstatistik" headers for one file per format vintage; impute 2011 from Morningstar `fees.pkl` or drop 2011 | Fully solves if the headers are clear |

---

## Sources (URLs used in this run)

- Tran and Wang: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X23000314); [Mendeley dataset](https://data.mendeley.com/datasets/8tyd2z7xgr); [P. Wang site](https://wangpingle.com/); [SSRN 3502862](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3502862)
- [Kronlund et al. 2021 (RePEc)](https://ideas.repec.org/a/eee/jfinec/v141y2021i2p644-668.html)
- [Chalmers and Reuter 2020 (RePEc)](https://ideas.repec.org/a/eee/jfinec/v138y2020i2p366-387.html)
- [Egan, Ge and Tang (SUFE record)](https://academicnewsletter.sufe.edu.cn/info/352020)
- [Bhattacharya, Illanes and Padi 2025 (RePEc)](https://ideas.repec.org/a/wly/emetrp/v93y2025i4p1449-1480.html)
- [Choukhmane 2025 (RePEc)](https://ideas.repec.org/a/aea/aecrev/v115y2025i11p3749-87.html)
- [Badoer, Costello and James 2020 (RePEc)](https://ideas.repec.org/a/eee/jfinec/v136y2020i2p471-489.html)
- [Sialm CV](https://faculty.mccombs.utexas.edu/clemens.sialm/CV-SIALM.pdf)
- [Kaniel and Parham 2017 (RePEc)](https://ideas.repec.org/a/eee/jfinec/v123y2017i2p337-356.html)
- [Hartzmark and Sussman 2019 (RePEc)](https://ideas.repec.org/a/bla/jfinan/v74y2019i6p2789-2837.html)
- [Ben-David et al. 2022 (RePEc)](https://ideas.repec.org:443/a/oup/rfinst/v35y2022i4p1723-1774..html)
- [Evans and Sun 2021 (RePEc)](https://ideas.repec.org/a/oup/rfinst/v34y2021i1p67-107..html)
- [Goyal, Wahal and Yavuz 2024 (Cambridge)](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/choosing-investment-managers/8E120D8C640A293B2E50917A51305BF5)
- Jenkinson, Jones and Martinez: [accepted manuscript](https://www.stat.berkeley.edu/~aldous/157/Papers/jenkinson.pdf); [SUFE record](https://academicnewsletter.sufe.edu.cn/info/359798)
- Armstrong, Genc and Verbeek: [SUFE record](https://academicnewsletter.sufe.edu.cn/info/391636); [Erasmus repository](https://repub.eur.nl/pub/113161); [CXO summary of an earlier version](https://www.cxoadvisory.com/investing-expertise/usefulness-of-morningstars-qualitative-fund-ratings)
- Hartzmark and Solomon: [AER 2025 (RePEc)](https://ideas.repec.org/a/aea/aecrev/v115y2025i9p3171-3213.html); [NBER WP record](https://ideas.repec.org/p/nbr/nberwo/30688.html)
- [Sabbatucci, Tamoni and Xiao (Inquire Europe)](https://www.inquire-europe.org/news/in-case-you-missed-it-shifting-from-active-to-passive-how-retirement-plans-impact-equity-prices/)
- Johansson, Sabbatucci and Tamoni: [RoF 2025 (RePEc)](https://ideas.repec.org/a/oup/revfin/v29y2025i1p103-139..html); [Sabbatucci, SHoF page](https://www.houseoffinance.se/about/people/people-container/riccardo-sabbatucci)
- [Greenwood and Sammon 2025 (RePEc)](https://ideas.repec.org/a/bla/jfinan/v80y2025i2p657-698.html)
- [Hong, Lu and Pan 2025 (RePEc)](https://ideas.repec.org/a/inm/ormnsc/v71y2025i1p488-517.html)
- [Dahlquist, Martinez and Söderlind 2017 (SUFE record)](https://academicnewsletter.sufe.edu.cn/info/353457)
- [Dahlquist, Setty and Vestman 2018 (SUFE record)](https://academicnewsletter.sufe.edu.cn/info/359460)
- [Cronqvist, Thaler and Yu 2018 (AEA)](https://www.aeaweb.org/articles?id=10.1257%2Fpandp.20181096)
- Anderson: [CV 2025](https://www.hhs.se/contentassets/cd1c63605f424a96b47bbcdec1dc6e96/cv_anders_anderson_2025.pdf); ["Who Feels the Nudge?" (NBER w25061)](https://www.nber.org/system/files/working_papers/w25061/revisions/w25061.rev0.pdf)
- Kinnerud and Lorentzon: [AEA 2023 programme](https://www.aeaweb.org/conference/2023/program/paper/8eQRSDE4); [DOI record](https://www.citedrive.com/en/discovery/dominated-pension-investments-the-role-of-search-frictions-and-unawareness/)
- Riksrevisionen: [audit page (blocked here)](https://www.riksrevisionen.se/granskningar/pagaende-granskningar/ett-upphandlat-fondtorg-for-premiepensionen.html); [News55, 1 Oct 2026](https://www.news55.se/privatekonomi/riksrevisionen-granskar-ppm-pension-forsamrad-overblick/)
- YFYS: [Grattan 2024 submission](https://grattan.edu.au/wp-content/uploads/2024/05/Grattan-2024-Submission-to-the-Treasury-review-of-the-YFYS-performance-test.pdf); [Treasury consultation](https://treasury.gov.au/consultation/c2024-471223)
- [Chile auctions, JPolMod 2023 (RePEc)](https://ideas.repec.org/a/eee/jpolmo/v45y2023i5p975-993.html)
- [Hastings, Hortaçsu and Syverson, Econometrica 2017](https://www.econometricsociety.org/publications/econometrica/2017/11/01/sales-force-and-competition-financial-product-markets-case)
- [Hamdani et al. (RePEc)](https://ideas.repec.org/p/cpr/ceprdp/10911.html)
- Local: `cooper_halling_yang_2021.txt`, `round1/ssz_dossier.md`, `round1/cookson_work/bids_long.csv`, `data/pa_panel_raw.pkl`, `audit/fundmaster.pkl`, `audit/fees.pkl`, `shof_field_definitions.txt`
