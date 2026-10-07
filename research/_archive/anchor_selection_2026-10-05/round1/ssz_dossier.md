# Dossier for candidate (A): Sialm, Starks and Zhang (2015) as the anchor

Prepared 4 October 2026 (round 1). Paper: Clemens Sialm, Laura T. Starks and Hanjiang Zhang, "Defined Contribution Pension Plans: Sticky or Discerning Money?", Journal of Finance 70(2), April 2015, pp. 805-838 (SSZ below).

Conventions. "p." is the journal page. The PDF (JSTOR, 35 pages) has a cover page, so PDF page = journal page minus 803. "txt line" is a line in `scratchpad/ssz.txt`. Tables that are garbled in the text were read from rendered page images in `round1/ssz_work/pages/` (`p-NN.png`; rotated tables `rot-NN.png`). All code and derived data are in `scratchpad/anchor_final/round1/ssz_work/` (file list in the appendix). Every Swedish number below comes from those scripts. Labels: **VERIFIED** (checked against the source cited), **JUDGEMENT** (my reasoning), **NOT VERIFIED** (could not confirm).

Blind-analysis rule used for the power work: the regressions behind every MDE printed only N, cluster counts, standard errors and MDEs (2.8 x SE). No point estimate of any replication or extension coefficient was printed or inspected. Two descriptive moments were seen because they enter the power arithmetic: flow standard deviations and the PPM-ratio distribution (section 3.6). I report them as such.

---

## 0. Bottom line

- The four claims in the brief are all **VERIFIED** (section 1.5). The prior memo's claim that "SSZ's sponsor table (VIII) cannot be replicated at all in Sweden, because PPM reallocations are mechanical" (`claude/anchor_decision_cookson_vs_ssz.md`, section 1 item 3) is wrong on the paper's own terms. SSZ's sponsor flow, eq. (4), p. 812, is built mechanically: a deletion books -100% of that plan's assets, and an addition books the fund's whole assets at t. An FTN column can be built the same way from the public files. N = 81 fund decisions in 6 rounds (sections 4.3 and 5).
- The data support the replication. "Handel, netto" is the month's net SEK flow into the PPM holding (median absolute gap to the asset identity 0.015 to 0.030% of assets, 2018 to 2025). Within-fund PPM and non-PPM flows exist for 199 SEK-currency equity funds monthly (8,033 fund-months, 2019 to 2023) and for 160 funds annually (635 fund-years). The PPM ratio distribution is almost identical to SSZ's DC ratio. Mean, quartile 1, median, quartile 3: 25.3 / 8.2 / 18.1 / 37.9%, against SSZ's 25.38 / 8.50 / 19.85 / 35.52% (Table I, p. 813).
- Power splits in two:
  - The pre-2024 replication is powered. For the Table III difference (PPM minus non-PPM), the linear-rank MDE is 0.110 per year (annual) and 0.0059 per month (monthly). SSZ's own estimates imply a gap of about -0.20 per year.
  - The FTN extension is marginal. The sponsor-flow slope on rank has MDE 0.655, against an average sponsor slope of 0.674 implied by SSZ's Table VIII. SSZ's piecewise form cannot be estimated on FTN (MDE 1.4 to 5.4).
- Verdict, detailed in section 7: (A) is the strongest of the candidates on table-level replicability and on power for the replication. It also contains Cookson's one powered test, the selection regression, as its Table VIII column. Its weakness is that the policy-relevant part rests on 81 decisions in 6 rounds and is only powered against effects at least as large as SSZ's US sponsors.

---

## 1. The paper, section by section (VERIFIED unless marked)

### 1.1 Data and definitions (Section I, pp. 810-813)

- **Sources.**
  - Pensions & Investments (P&I) annual surveys of DC assets by fund, 1997 to 2010. Each survey reports Dec 31 of the prior year, so the data cover 1996 to 2009 (p. 810; txt lines 326-338; p. 812 txt lines 483-485).
  - CRSP survivor-bias-free mutual fund data. Funds with less than $5m in the previous month are excluded. Share classes are aggregated to the fund (p. 810, txt lines 339-352).
  - Form 11-K plan filings from Pool, Sialm and Stefanescu (p. 811, txt lines 388-394).
  - Sample: domestic equity funds only, at least 80% in common stock, index funds included (fn 16, txt lines 366-370).
- **Flows.**
  - DC Flow, eq. (1): [DC_t - DC_{t-1}(1+R)] / [DC_{t-1}(1+R)].
  - NonDC Flow, eq. (2): the same with total assets minus DC assets.
  - Plan Flow, eq. (3): aggregated over the 11-K plans.
  - Plan Sponsor Flow, eq. (4): [sum over additions of Assets_{p,f,t} - sum over deletions of Assets_{p,f,t-1}(1+R)] / [sum over p of Assets_{p,f,t-1}(1+R)].
  - Plan Participant Flow, eq. (5): Plan Flow minus Sponsor Flow.
  - Source: PDF pp. 8-9 images, journal pp. 811-812. Plan flow is computed only if at least one 11-K plan offered the fund in the prior year (p. 811-812).
- **Footnote 18 (p. 812, txt lines 492-500).** Sponsors also shape participant flows (closures, defaults, competing additions). Their sponsor-flow measure "likely underestimates the influence of sponsors and overestimates the influence of participants."
- **Sample (p. 812).** 1,078 distinct equity funds, 5,808 fund-years, 1996 to 2009. The intro says flows are compared "from 1997 to 2010" (p. 807, txt lines 159-160), meaning the survey years.
- **Winsorizing.** Flows are winsorized at the 2.5% level (p. 814, txt lines 575-576).

### 1.2 Table-by-table record

| Item (page) | Dependent variable | Regressors | FE / SE | Frequency, sample, N | Headline numbers |
|---|---|---|---|---|---|
| **Table I** (p. 813) | Summary statistics | none | none | Annual, 1996 to 2009, N = 5,808 | DC ratio mean 25.38%, quartile 1 8.50, median 19.85, quartile 3 35.52; DC flow mean 32.00% (sd 119.34); non-DC flow 6.65% (sd 44.37); plan sponsor flow mean 9.68 (sd 74.12); participant flow 12.59 (sd 25.88). Panel B: correlations. |
| **Table II** (p. 815) | Fund-lifetime sd and AR(1) of annual DC and non-DC flows, pooled | DC indicator, initial log size, log family size, log age, expense ratio, turnover (demeaned), DC x controls | Caption gives no clustering ("Standard errors are reported in parentheses") | Cross-section of funds with at least 5 annual flows (fn 19); N 1,032 (cols 1, 4) and 987 (cols 2-3, 5-6) | DC indicator, sd: 0.522*** (0.033), 0.212*** (0.031), 0.310*** (0.031). DC indicator, AR(1): -0.138*** (0.026), -0.127*** (0.034), -0.114*** (0.041). Text on p. 816: the DC sd exceeds non-DC by 21.2 to 52.2% per year. |
| **Figure 1** (p. 818) | Flows by 100 percentile groups of prior-year return, DC vs non-DC, covariates at means | eq. (7) | none | Annual | p. 819: middle 10% get DC +23.7% vs non-DC +2.1%; bottom decile DC -8.3% vs non-DC -11.8%; top decile DC +53.6% vs non-DC +17.9% (txt lines 859-875). |
| **Table III** (p. 820, PDF p. 17) | DC flow, non-DC flow, and their difference | Low, Mid, High (eq. 8, Sirri and Tufano) of the prior 1-year or prior 5-year return percentile across all sample equity funds; log DC size, log non-DC size, log family size, log age, expense ratio, turnover, volatility, style flow (eq. 6) | Time FE; SEs clustered by fund | Annual; N 3,851 (1-year), 3,249 (5-year) | 1-year, DC: 1.194*** (0.377), 0.236*** (0.086), 1.776*** (0.497). Non-DC: 0.328** (0.142), 0.284*** (0.037), 0.487*** (0.180). Difference: 0.866** (0.374), -0.049 (0.090), 1.289*** (0.476). 5-year, DC: 0.845**, 0.421***, 0.619*. Non-DC: 0.096, 0.281***, 0.102. |
| **Figure 2** (p. 821) | Piecewise fit from Table III | none | none | none | Illustration only |
| **Table IV** (p. 823, PDF p. 20 rotated) | As in Table III, with alternative benchmarks | Rank within objective code; within 9 holdings-based styles; on Carhart alpha (prior year, weekly) | Time FE; cluster fund | N 3,851 / 3,780 / 3,408 | DC Low/Mid/High, objective-adjusted: 1.040***, 0.237***, 1.736***; style-adjusted: 1.219***, 0.189*, 1.390***; Carhart: 0.927**, 0.138, 1.625***. Non-DC objective-adjusted: 0.379**, 0.273***, 0.504***. Non-DC style: 0.088, 0.275***, 0.415**. Non-DC Carhart: 0.073, 0.281***, 0.290. |
| **Table V** (p. 825, PDF p. 22) | Table III by subperiod | Same | Time FE; cluster fund | 1996-2002: N 1,759; 2003-2009: N 2,092 | 1996-2002, DC: 0.660 (0.630), 0.416***, 2.484***. Non-DC: 0.318, 0.333***, 1.234***. 2003-2009, DC: 1.546***, 0.120, 1.296**. Non-DC: 0.410**, 0.259***, -0.031. The low-quintile DC sensitivity appears only after 2003 (p. 824, txt lines 1290-1295). |
| **Table VI** (pp. 826-827, PDF pp. 23-24) | Table III plus Low/Mid/High interacted with demeaned log DC size, log non-DC size and log age | Same | Time FE; cluster fund | N 3,851 | Size model, DC: 0.970***, 0.258***, 1.492***. Age model, DC: 1.147***, 0.252***, 1.639***. No interaction significant at 5% (p. 824, txt lines 1306-1309). |
| **Table VII** (p. 829) | Multinomial logit: exit from or entry to the P&I list | Performance, log fund size, log family size, log age, expenses, turnover, volatility, style flow | Time FE; cluster fund | N 5,006 | Exit: performance -0.958*** (0.221). Entry: 0.485** (0.203) (txt lines 1827-1857). This is a sample-selection check, not a menu test (p. 828). |
| **Figure 3** (p. 830) | Sponsor vs participant flows by 100 percentile groups, 11-K | none | none | Annual | Sensitivity comes mostly from sponsors; participant flows are "only weakly related" (p. 830). |
| **Table VIII** (p. 831, PDF p. 28 rotated) | Total plan flow, sponsor flow, participant flow (eqs. 3-5) | Low/Mid/High of prior-year rank; log plan size, log fund size, log family size, log age, expense ratio, turnover, volatility, style flow | Time FE; cluster fund (p. 832) | P&I sample N 2,815; full 11-K sample N 8,268 | P&I, total: 1.046*** (0.399), 0.465*** (0.091), 1.584*** (0.482). Sponsor: 1.050*** (0.376), 0.310*** (0.083), 1.389*** (0.427). Participant: -0.004 (0.111), 0.156*** (0.024), 0.194 (0.136). 11-K, total: 0.773***, 0.516***, 0.744**. Sponsor: 0.786***, 0.380***, 0.718**. Participant: -0.013, 0.135***, 0.026. |
| **Table IX** (p. 834, PDF p. 31 rotated; eq. 9 p. 833) | Next year's performance: raw, objective-adjusted, style-adjusted, CAPM, FF3, Carhart | DC flow_{t-1}, non-DC flow_{t-1}, return over past year, log size, log family size, log age, expense ratio, turnover, DC ratio | Year FE; cluster fund | Annual; N 4,116 / 4,075 / 3,999 / 4,009 / 4,009 / 4,009 | DC flow: -0.262 (0.163), -0.260 (0.160), -0.091 (0.133), -0.176 (0.144), 0.114 (0.128), -0.011 (0.121). Non-DC flow: -1.567*** (0.455), -1.102** (0.436), -0.815** (0.351), -1.261*** (0.405), -0.657** (0.286), -0.948*** (0.276). F-test p-values (DC = non-DC): 0.009, 0.074, 0.059, 0.016, 0.024, 0.004. |

Units. Flows enter as fractions: "A 10-percentile increase ... increases the DC flows by 11.9%" (p. 820) equals 0.1 x 1.194. The Table IX performance unit is not stated; the text says "raw fund return per month" (p. 833). I treat it as percent per month. **NOT VERIFIED** beyond that inference.

### 1.3 Section IV mechanism text (pp. 829-832)

"when plan sponsors terminate an investment option, the assets in that option are usually mapped to a replacement option" (p. 829, txt lines 1876-1879). Sponsor flows are those "associated with the appearance or disappearance of an investment option on plan menus" (p. 829-830). The P&I sample is weighted toward large funds, so the 11-K columns are "more muted" (p. 832, fn 29).

### 1.4 Conclusions (p. 835)

DC money is "less sticky and more discerning" because sponsors delete poor performers and add good ones. DC flows do not predict performance, while non-DC flows predict it negatively. The authors read this as sponsors keeping participants out of the "dumb money crowd" (txt lines 2408-2432).

### 1.5 The four claims to verify

1. **Table III**, DC 1.194 / 0.236 / 1.776 and non-DC 0.328 / 0.284 / 0.487: **VERIFIED**. p. 820, 1-year columns; PDF p. 17 image; txt lines 926-931.
2. **Table VIII**, P&I sponsor Low 1.050 and High 1.389, participant Low -0.004 and High 0.194: **VERIFIED**. p. 831, PDF p. 28 image. Note: the participant Mid of 0.156*** (0.024) is significant, so participants are not fully inert in the middle range.
3. **Footnote 6**, "When a fund is replaced, the plan assets are typically transferred to the new fund": **VERIFIED** verbatim. p. 807, fn 6, txt lines 195-197; PDF p. 4 image. The preceding sentence: 43% of plan sponsors in a Deloitte (2011) survey replaced at least one fund for poor performance within the year.
4. **Table IX**, DC flows do not predict returns and non-DC flows predict them negatively: **VERIFIED**. All six DC coefficients are insignificant; all six non-DC coefficients are negative and significant at 5% or better (p. 834). Text p. 833, txt lines 2197-2206.

Page note: the brief's "Table III p. 16, Table VIII p. 27, Table IX p. 30" are PDF page numbers minus one. The tables sit on PDF pp. 17, 28 and 31 (journal pp. 820, 831, 834).

---

## 2. Literature since SSZ

### 2.1 Tran and Wang (2023), JFE 148(1), 69-90, "Barking up the wrong tree: Return-chasing in 401(k) plans"

- **VERIFIED** citation and abstract via IDEAS / RePEc and ScienceDirect.
  - Data: hand-collected Form 11-K data, "1,551 public firms from 1993 to 2016".
  - Finding: "83% of investors in our sample hold only 39% of total assets and follow a return-chasing strategy", while wealthier investors follow CAPM alpha.
- **VERIFIED** (from the ScienceDirect page through the fetch tool; exact page not visible): "To tease out the effect of menu change, we decompose fund flows into sponsor flows and participant flows following Sialm et al. (2015) and re-examine the flow-performance relation both at the fund level and plan level." Per the same page, sponsor flows respond to CAPM alpha and Morningstar ratings.
  - This is direct evidence that SSZ's decomposition is live in a 2023 top-3 journal paper.
  - It also supplies the recent anchor partner the course's recency rule wants.
- **Replication package.** Mendeley Data, DOI 10.17632/8tyd2z7xgr.1, "Code and data for 'Barking Up The Wrong Tree'", contributor Pingle Wang, published 14 Feb 2023, version 1. The description is "code and data used for the paper"; a `readme.txt` with "detailed steps to reproduce the results" is listed.
  - **NOT VERIFIED:** the file tree, the size, and whether CRSP or Morningstar inputs are included. The page is JavaScript-rendered; the Mendeley API returned 403 (container egress policy and fetch tool); SSRN returned 429.
  - Judgement on whether a student could re-run their tables: unknown. The 11-K holdings are public filings, but fund returns, alphas and Morningstar ratings almost surely come from licensed CRSP or Morningstar data. WRDS access for this group is unverified (brief section 3).
  - This does not matter for (A): the thesis replicates SSZ on Swedish data and needs neither the US files nor this package. Open it once on the SSE network, read `readme.txt`, and cite it as the template for the replication folder.

### 2.2 Other papers to check

- **Pool, Sialm and Stefanescu (2016)**, JF 71(4), 1779-1812, "It Pays to Set the Menu". Citation **VERIFIED** (RePEc author page).
  - Content via NBER WP 18764 summary, numbers **NOT VERIFIED** against the published version: 11-K data 1998-2009, about 2,645 plans.
  - Trustee-affiliated funds are less likely to be deleted after poor performance. The WP summary gives a deletion coefficient of -0.140 on Trustee Fund and +0.247 on LowRank x Trustee.
  - It decomposes extensive-margin (menu) and intensive-margin (participant) flows.
  - Relevance: it is the source of SSZ's 11-K decomposition, and it shows that sponsor selection can be conflicted. FTN is a non-conflicted public sponsor, so the conflict dimension has no FTN counterpart. Do not invent one.
- **Christoffersen and Simutin (2017)**, RFS 30(8), 2596-2620, "On the Demand for High-Beta Stocks". Citation **VERIFIED** (IDEAS URL); content from the CBS accepted manuscript via the fetch tool.
  - Uses the same P&I DC survey, 2003-2013 holdings, 4,603 fund-years.
  - Funds with more sponsor-monitored DC assets tilt to high-beta stocks to beat benchmarks.
  - It cites SSZ: "larger fund size, lower expenses and higher relative performance are of first order economic importance to determine DC flows."
  - Relevance: a consequence of sponsor monitoring for managers. It could motivate one sentence on whether FTN winners change risk, but that is not a thesis table.
- **Kronlund, Pool, Sialm and Stefanescu (2021)**, JFE 141(2), 644-668, "Out of Sight No More?". Citation **VERIFIED** (RePEc).
  - Content via NBER WP 27573 summary, **NOT VERIFIED** against the published version.
  - A US regime change: the 2012 DOL participant fee-disclosure rule 404(a)(5).
  - Plan-by-fund fixed effects; participants become more fee-sensitive and more sensitive to 1-year returns.
  - Sponsor deletions do not change around the reform.
  - Relevance: the closest published "SSZ decomposition around a regime change." It changes participant information, while FTN changes the sponsor. That is a clean contrast for the related-literature paragraph.
- **Da, Larrain, Sialm and Tessada (2018)**, RFS 31(10), 3720-3755 (Chile). Citation **VERIFIED** (RePEc). Pension reallocations driven by advice; a price-pressure paper, not the DC/non-DC decomposition.
- **Outside the US, regime changes.**
  - I listed SSZ's 158 citing records (Semantic Scholar API, citations of DOI 10.1111/jofi.12232) and checked the plausible ones.
  - **Israel:** Arbaa and Varon (2019/2020), International Journal of Managerial Finance 16(3), 334-356, flow-performance in provident funds. Per the RePEc abstract, no sponsor/participant split.
  - **Australia:** superannuation switching and choice-legislation papers (e.g., Financial Services Review 2015) study member switching; the decomposition is not shown in the titles or abstracts I saw. Australia's 2021 "Your Future, Your Super" performance test is a close institutional analogue to FTN (a regulator tests products, failing products must notify members). The results I found are practitioner and APRA sources and a UTS honours thesis, not top-journal papers. **NOT VERIFIED** that no academic paper applies SSZ there.
  - **UK:** NAO and TPR reports on DC regulation only.
  - **Chile:** DLST above.
  - Judgement: I found no published paper that applies SSZ's DC/non-DC or sponsor/participant decomposition outside the US or around a sponsor-side regime change. This is a bounded search result, not proof of absence.
- **SSZ on Swedish PPM or FTN.**
  - No paper found in web searches (English and Swedish).
  - "Sticky or Discerning" or "Sialm ... Starks" appears in none of the 635 non-winner or 25 winner thesis texts (Grep over `financethesis/non_winners/text` and `old_winners`). "Sialm" alone appears in 10 non-winner texts, none citing SSZ by that pattern.
  - Swedish PPM inertia papers exist (Cronqvist and Thaler 2004; Dahlquist, Martinez and Söderlind 2017 RFS, cited in the synopsis), but none use the DC/non-DC decomposition. The earlier memo reports that "Fondtorgsnämnd" appears in zero of the 635 thesis texts; I did not re-run that.
  - **NOT VERIFIED:** a DiVA search for spring-2026 bachelor theses. Do it before writing a novelty sentence.

---

## 3. Mapping SSZ to the Swedish data, with real counts

### 3.1 Coverage of the Pensionsmyndigheten files, by year

Source: full header scan of all 307 files, `coverage_scan.json` from `scan_headers.py`, and the parsed panel `ppm_panel_all.csv` from `build_panel.py` (205,937 fund-month rows).

| Years | Market value | Handel, netto | ISIN | Returns in the file | Fees |
|---|---|---|---|---|---|
| 2001-2005 | yes (stored as text with decimal comma, parsed) | no | no | none | no |
| 2006-2011 | yes | no | no | calendar-year returns, YTD and 5-year average | yes |
| 2012-Aug 2017 | yes | no | no | YTD, 3, 6, 12, 36, 60 months | yes |
| Sep 2017-Aug 2026 | yes | yes | yes (Fondstatistik "ISIN-kod") | adds "1 mån." | yes |

- Missing files and sheets: June 2006 has no file; Jan and Aug 2006 have no market-value sheet.
- Market-value sums are not comparable across 2005-2006. The total jumps from SEK 164.8bn in Oct 2006 to 232.3bn in Nov 2006, and falls from 192.4 to 159.5bn between Dec 2005 and Feb 2006. So the 2006 annual flow (median 19%) is unusable; start the annual PPM series in 2007 or 2008.
- **Returns in the PPM files are integer-rounded percent in every vintage.** For example, the Dec 2018 "1 mån." values are -8, -7, -6, -6; 100% of 2012-2025 values are integers, except the 2009 column. Monthly flows therefore cannot be built from file returns. Annual flows can: a 0.5 pp return error moves a flow by about 0.5% of assets, against a flow sd of about 32%. Returns for 2018 onward come from SHoF `tri_sek`.
- Fund counts: 589 (2001) rising to 920 (2015), then 891 (2018), 802 (2019), 530 (2020), 403 (2026).
- 2019 has 348 exits holding SEK 60.9bn of PPM capital, mostly Mar to Jul 2019 (the re-registration under prop. 2017/18:247). Some large exit months (2008, 2009 and 2011, the last with SEK 223bn) are almost surely renumbering or default-fund reorganisation, not removals. **NOT VERIFIED**; an identity map is needed before using pre-2017 exits.

### 3.2 What "Handel, netto" measures (VERIFIED)

`validate_nt.py`, rows in `nt_validation_rows.csv`. The file holds no definition of the field, so I tested it against the asset identity mv_t - mv_{t-1}(1+R_t), with R the SEK total return of the PPM share class from SHoF.

| Sample | N | Funds | Correlation | Median gap (% of lagged PPM assets) | 90th-percentile gap |
|---|---|---|---|---|---|
| All months | 42,418 | 687 | 0.997 | 0.065 | 0.92 |
| Excluding December | 39,100 | 687 | 0.999 | 0.060 | 0.92 |

- For holdings above SEK 200m, the median gap is 0.015 to 0.030% in every year 2018-2025, and 0.504% in 2026. The 2026 gap is a SHoF data issue: aggregate implied flows swing SEK +36.6bn and -25.7bn in Feb and Mar 2026.
- December gaps are 0.062% median; the December placement is in `nt` (aggregate +47 to +51bn every December).
- The AP7 funds do not satisfy the identity. AP7 Aktiefond in Dec 2025 shows `nt` SEK 32.8bn against an implied 0.77bn, presumably internal Såfa flows. Exclude them, as SSZ exclude non-equity.
- Conclusion: from Sep 2017, `nt` is the month's net SEK flow into the PPM holding (subscriptions minus redemptions, switches, placements and transfers). It is better than eq. (1), because the file returns are rounded. Before Sep 2017, PPM flows must use eq. (1), annual only.

### 3.3 Non-PPM flows (SSZ eq. 2)

`link_shof.py`, `ppm_shof_flows.csv`. PPM ISINs are matched to Morningstar `performanceid` through `fundmaster.pkl`: 52,495 of 56,328 ISIN-months.

- Coverage by year: tri_sek returns 83-90% and SHoF TNA 87-96% in 2019-2023; SHoF starts Jan 2018.
- Definitions: non-PPM assets NP = `tnafund` - PPM market value; non-PPM flow = [NP_t - NP_{t-1}(1+R)] / [NP_{t-1}(1+R)].
- Two restrictions:
  - Only funds with `ccy_fund == 'SEK'`, about 55-64% of linked PPM fund-months, because `tnafund` is in fund currency and no FX series is in hand. Domiciles of the SEK equity funds: SWE 206, LUX 41, NOR 32, FIN 15.
  - Flows are imputed from TNA and returns, as the brief's CAUTION requires; the Morningstar net-flow field is not used.
- TNA gaps: 39 of 759 linked funds have TNA in under half of the 2019-2023 months (SEK 32.5bn of SEK 988bn average PPM capital), mainly Öhman, Espiria, Danske and Allianz.

### 3.4 Reconciliation in transfer months (VERIFIED, `reconcile.py`, `reconcile_winners.csv`)

Sample: FTN-flagged SEK-currency funds, taking each fund's largest-`nt` month after 2024 with `nt` above SEK 300m. That gives 23 funds; 19 have SHoF TNA. Four Swedbank Robur winners lack TNA in their transfer month.

| Fund, month | PPM nt (SEK m) | Implied total fund flow (SEK m) | Non-PPM residual as % of PPM nt |
|---|---|---|---|
| Skandia Global Exponering A, Apr 2025 | 3,227 | 3,175 | -1.6 |
| Cliens Sverige, Jan 2026 | 1,637 | 1,551 | -5.3 |
| Handelsbanken Sverige Index Criteria, Nov 2025 | 2,867 | 2,995 | +4.5 |
| Handelsbanken Sverige Selektiv, Jan 2026 | 1,584 | 1,704 | +7.6 |
| Swedbank Robur Europafond A, Jun 2024 | 684 | 695 | +1.7 |
| AMF Aktiefond Europa, Mar 2025 | 1,387 | 1,961 | +41.4 |
| SEB Sverigefond, Feb 2026 | 2,308 | 1,039 | -55.0 |
| Handelsbanken Sverige 100 Index Criteria, Nov 2025 | 1,641 | 787 | -52.0 |
| Handelsbanken Europa Index Criteria, Mar 2025 | 647 | 3,066 | +374 |

- Across the 19 funds, the median |residual| is 34.6% of the PPM transfer, or 2.0% of non-PPM assets. The pre-2024 monthly non-PPM flow sd is 2.83%, so in transfer months the subtraction adds error of roughly 0.7 sd.
- AMF Aktiefond Europa matches the brief: TNA SEK 9,816m in Feb 2025 and 11,190m in Mar 2025, PPM `nt` +1,387m. But it implies SEK +574m of simultaneous non-PPM inflow.
- Judgement: the subtraction works for some funds and fails for others in transfer months, probably because of timing and other platforms moving in step. Pre-2024 there are no FTN transfers, so the replication is not exposed. Any FTN-period non-PPM column is exposed.

### 3.5 FTN events in the panel (`ftn_rounds.py`, `ftn_cross_section.csv`)

Incumbent funds in each procured category, taken at the month before the award:

| Round | Removed | Incumbent winners | Comment |
|---|---|---|---|
| R1 Europe active | 22 | 1 | Others are new share classes |
| R2 Europe index | 2 | 4 | |
| R2 Global index | 8 | 3 | |
| R3 Nordic, incl. small | 9 | 6 | The PPM category "Norden" holds both |
| R4 Sweden active | 18 | 4 | |
| R4 Sweden passive | 7 | 3 | |
| R6 Europe small, Sweden small | 0 | 7 | 12 losers still listed in Aug 2026; transfers not yet done |

- Removed funds held SEK 74.0bn of PPM capital before their awards.
- **Removal months (VERIFIED from fund disappearance):**
  - R1: May-Jun 2024.
  - R2 Europe index: Feb 2025.
  - R2 Global index: Mar 2025.
  - R3: May-Jun 2025.
  - R4 Sweden active: Oct 2025 to Mar 2026, spread out.
  - R4 Sweden passive: Oct-Nov 2025.
- **Allocation rule (VERIFIED, FTN report of 25 Mar 2024, section 3.7, report pp. 11-12, txt lines 417-425; the same sentence is in all 11 reports):**
  - Capital from removed funds "fördelas lika mellan de upphandlade fonderna, dock med vissa undantag". Incumbent winners "behåller befintligt kapital" and receive capital only "upp till samma nivå som övriga upphandlade fonder".
  - So the winner's dose is an equalization formula that falls with the winner's own prior PPM capital. Example: AMF Aktiefond Europa, an incumbent with SEK 3.3bn, received nothing in the R1 window (Jun-Aug 2024 `nt` -28.6m).
  - Its +1.39bn in Mar 2025 is unexplained by R1. **NOT VERIFIED** source. This is the case for asking Pensionsmyndigheten for the transfer ledger.
- **Scoring rule (VERIFIED, same report, section 3.5, txt lines 272-278 and 310-360).**
  - Mandatory: at least 3 consecutive years in the same strategy within the last 5.
  - Award criteria: quality 75% (investment philosophy, process, manager resources, "Investeringsresultat", administration and risk control) and cost 25%.
  - The reports print each winner's 3-year Sharpe ratio and information ratio (e.g., txt lines 1111-1115).
  - Past performance is therefore one of five quality subcriteria, not the score.

### 3.6 Counts actually obtained, and table-by-table feasibility

| SSZ exhibit | Swedish version | Years | N actually available | Status |
|---|---|---|---|---|
| Table I | PPM ratio, sizes, fees, flows | 2019-2023 annual (joint sample) | 651 fund-years, 163 funds | Replicable. Fact already seen: PPM ratio mean 25.3%, quartiles 8.2 / 18.1 / 37.9 (SSZ 25.38 / 8.50 / 19.85 / 35.52). Winsorized annual flow mean (sd): PPM 0.073 (0.321), non-PPM 0.007 (0.179); SSZ 32.0 (119.3) and 6.65 (44.4) in % (Table I). |
| Table II | sd and AR(1) of PPM vs non-PPM flows | 2019-2023 annual (5 flows each) | 96 funds (192 moments). Monthly robustness: 133 funds with at least 36 months | Replicable but thin; SSZ have 1,032 moments (about 516 funds, inferred) |
| Table II, PPM side only | | 2007-2023 annual | 755 funds with 5 or more annual flows (all asset classes); equity 493 | Replicable with no non-PPM comparison before 2019 |
| Table III | PPM vs non-PPM vs difference | 2019-2023 annual; Feb 2019-Dec 2023 monthly | Annual N 635 (160 funds, 5 years). Monthly N 8,033 (199 funds, 59 months) | **Replicable** |
| Table III, PPM column only | | 2008-2023 annual | N 5,728 equity fund-years, 751 funds | Replicable (integer-rounded file returns for ranks) |
| Table IV | Rank within PPM category | same | same | Replicable; holdings-based styles not available |
| Table V | Subperiods | PPM-only 2008-2015 vs 2016-2023; joint too short to split | | Partly |
| Table VI | Size and age interactions | same | same | Replicable |
| Table VII | Exit and entry logit | PPM exits by month 2001-2026 (`ppm_panel_all.csv`) | All exits observed; 2019 and FTN removals are their own events | Replicable as "platform exit"; needs an identity map before 2017 |
| Table VIII | P&I and 11-K sponsor/participant split | Not replicable before 2024 (no sponsor, which is the point). FTN column 2024-2026 | N 81 (62 removed, 19 incumbent winners, 6 rounds) | **Extension** |
| Table IX | Perf_t on PPM and non-PPM flows_{t-1} | flows 2019-2023, performance 2020-2024 | N 631, 157 funds, 5 years | **Replicable** |
| Figures 1-3 | | same samples | | Replicable; Figure 3 only as the FTN column |

Exhibits that cannot be replicated: Table IV's holdings-based style ranks (FI holdings cover Swedish-domiciled funds only, a few quarters downloaded); Table IV's Carhart alpha from weekly returns (monthly is possible); the P&I and 11-K columns of Table VIII for any pre-2024 Swedish period; any non-PPM series before 2018, unless SHoF supplies the older history it says it holds.

---

## 4. The reframed thesis

### 4.1 Research question (one sentence)

When a public sponsor that deletes and adds funds is introduced into a pension system where only participants chose, does pension money stop being sticky and become discerning, as Sialm, Starks and Zhang attribute to US plan sponsors?

JUDGEMENT on why it is interesting whatever the result:
- If PPM money was performance-insensitive before 2024 and FTN's selection loads on performance, SSZ's sponsor mechanism is confirmed by switching it on.
- If FTN selects mainly on process and cost, so that sponsor flows do not load on past returns, a public sponsor disciplines on something other than returns. That separates "sponsor presence" from "return-chasing by sponsors", which SSZ cannot separate.

### 4.2 Replication tables (participants only, before 2024)

- **Table I:** summary statistics, with SSZ's Table I numbers in a side column.
- **Table II:** sd and AR(1), PPM vs non-PPM, annual 2019-2023 (96 funds). PPM-only moments for 2007-2023 as a panel B.
- **Table III:**
  - Joint annual 2019-2023 and joint monthly 2019-2023, PPM, non-PPM and difference.
  - Panel B: PPM only, 2008-2023.
  - Columns follow SSZ, except that family size and turnover are absent from the data in hand.
  - Pre-specify one linear-rank difference as the headline replication test, with the piecewise form as the SSZ-faithful display.
- **Table IX:** annual, raw and category-adjusted performance. The CAPM and multi-factor versions need Swedish/global factors (SHoF factors; **NOT VERIFIED** for global funds).

### 4.3 The extension inside SSZ's tables

1. **Table VIII, FTN column.**
   - Sponsor flow per SSZ eq. (4): removed fund = -1 in the removal month; incumbent winner = transferred capital over the round's transfer window divided by PPM capital before the window. New share classes and new entrants are excluded, as eq. (4) is undefined without t-1 holdings (pp. 811-812).
   - Participant flow = PPM flow minus sponsor flow over award-to-transfer+2 months. This captures active choosers leaving removed funds before removal, and savers choosing winners.
   - Rank: the 12-month SEK return percentile within round at the pre-award month (SHoF). A 36-month rank as robustness, since FTN reports 3-year ratios.
   - Report two pieces: selection (a linear probability model of win on rank, which is Cookson's selection test inside SSZ's table), and dose (the rule-implied transfer).
   - Sample now: N 81. It rises to about 100 when R6 transfers appear in the Sep and Oct 2026 files (**NOT VERIFIED** release dates).
2. **Table III, regime column.** Monthly PPM flows in procured equity categories, Feb 2024 to Aug 2026 (N 2,611 fund-months, 131 funds), with the removal month booked at -1, against the same categories in 2019-2023.
   - This column shares the same 81 decisions with the Table VIII column, so it is not independent evidence. Present it as the "total DC flow" counterpart, like SSZ's column 1 of Table VIII.
   - Do not winsorize the -1 rows. They are 2.2% of rows, and SSZ's 2.5% winsorizing would clip them (checked in `regime_power.py`).
3. **Table IX with the FTN selection.** Post-award category-adjusted mean monthly return of winners minus removed funds, within round. Removed funds stay observable in SHoF after leaving PPM. Read against SSZ's Berk and Green interpretation.

### 4.4 Predicted signs, with reasoning (JUDGEMENT, written before any estimate)

| Estimate | Predicted sign | Reasoning |
|---|---|---|
| Table III difference, pre-2024, Low and High | Negative, about -0.3 per year | SSZ attribute DC sensitivity to sponsors (Table VIII). With no sponsor, PPM should look like SSZ's participant column (-0.004 / 0.156 / 0.194) against a non-DC-like non-PPM column (0.328 / 0.284 / 0.487). Implied differences: about -0.33 / -0.13 / -0.29. As a linear slope over the full rank range: participants 0.132, non-DC 0.333, difference about -0.20. |
| Table III, PPM-only 2008-2023 vs SSZ DC | Much smaller than 1.194 / 0.236 / 1.776 | Same reasoning |
| Table II DC indicator for sd (with size controls) | Ambiguous | SSZ's higher DC volatility is sponsor-driven. But PPM flows also contain the December placement and third-party switching services (not verified), and the PPM base is small: median PPM ratio 18%. The raw annual sd is already higher for PPM (0.32 vs 0.18). Pre-commit: a positive indicator after size controls means a sponsor is not necessary for DC volatility. |
| Table II DC indicator for AR(1) | Positive (stickier) | Inertia plus pro-rata December placements |
| Table VIII FTN column, Low | Positive | Removals (-1) should sit in the low tail if "Investeringsresultat" and the 3-year Sharpe/IR matter |
| Table VIII FTN column, High | Flat, possibly negative | The equalization rule gives large incumbents (often past winners) little or nothing |
| Table VIII FTN participant column | Small and positive | SSZ participant Mid 0.156 |
| Table IX, pre-2024 | PPM flow coefficient about 0; non-PPM negative | SSZ Table IX |
| Table IX, FTN selection | About 0 for gross returns | Berk and Green; selection on process and cost. The fee cut shows up only in PPM-class net returns, not in SHoF share-class returns. |

### 4.5 "FTN sponsor flows are mechanical": the objection and the answer

1. **SSZ's sponsor flows are mechanical too, by construction.**
   - Eq. (4) books a deletion as -Assets_{p,f,t-1}(1+R), all of that plan's money in the fund, and an addition as the fund's whole assets at t (p. 812).
   - SSZ state that deleted options' assets are "usually mapped to a replacement option" (p. 829) and "typically transferred to the new fund" (fn 6, p. 807).
   - The economics is in which fund the sponsor deletes or adds; the dollar amount follows from the plan's holdings.
2. **The FTN column measures the same thing:** the performance loading of the sponsor's decision rule (win, or remove). With one sponsor, the "flow-performance slope" is a revealed loading of FTN's scoring rule on past returns. That is informative, because the rule is 75% quality including track record and 25% cost (section 3.5).
3. **What really differs.**
   - SSZ aggregate many independent plan decisions per fund, so sponsor flow is continuous. PPM has one sponsor, so sponsor flow is -1 or a rule-set dose, and inference comes from 81 decisions in 6 rounds, not thousands of plan-years.
   - FTN's dose is formula-driven (equalization) in a way US mappings are not. Hence the selection/dose split in 4.3, which removes the dose mechanics from the selection estimate.
4. **The non-mechanical parts are measurable separately:** pre-removal exits by active choosers, default acceptance, and non-PPM flows.

---

## 5. Power (MDE = 2.8 x SE, 5% two-sided, 80% power)

Assumptions:
- Real samples as in section 3.6, SEK-currency equity funds.
- Flows winsorized at 2.5% per tail, except sponsor -1 values.
- Time fixed effects; one-way fund-clustered SEs (CR1, `olslib.py`); FTN cross-section with round FE and HC1 SEs.
- Controls are as SSZ's, except that family size and turnover are omitted.
- Annualizing monthly coefficients by multiplying by 12 is an approximation that assumes the response to the trailing-12-month rank is spread evenly over the year.

| Test (script) | N | SE | MDE | SSZ comparison |
|---|---|---|---|---|
| Table III difference, annual 2019-2023, piecewise (`table3_power.py`) | 635 fund-years, 160 funds, 5 years | Low 0.369, Mid 0.064, High 0.233 | 1.03, 0.18, 0.65 | SSZ difference: 0.866 (0.374), -0.049 (0.090), 1.289 (0.476). Our SEs equal or beat SSZ's. Implied PPM gap about -0.33 / -0.13 / -0.29: not detectable segment by segment. |
| Table III difference, annual, linear rank (`table3_linear_power.py`) | 635 | 0.039 | **0.110** | Implied gap about -0.20: powered |
| Table III difference, monthly 2019-2023, piecewise | 8,033 fund-months, 199 funds, 59 months | 0.011, 0.003, 0.014 per month (x12: 0.13, 0.04, 0.17) | 0.031, 0.009, 0.040 per month (x12: 0.37, 0.10, 0.47) | Mid powered against -0.13; Low and High borderline |
| Table III difference, monthly, linear | 8,033 | 0.0021 per month | **0.0059 per month** (about 0.071 per year) | Powered |
| Table III PPM-only, annual 2008-2023 (`ppm_only_power.py`) | 5,728 fund-years, 751 funds | 0.130, 0.026, 0.113 | 0.36, 0.07, 0.32 | SSZ DC 1.194 / 0.236 / 1.776 (SEs 0.377 / 0.086 / 0.497): distinguishable from SSZ's DC column in all segments; from SSZ's participant column only at Mid |
| Table II DC indicator, annual (96 funds) | 192 moments | sd 0.019; AR(1) 0.062 | 0.053; **0.174** | SSZ 0.522 (0.033); -0.138 (0.026). The AR(1) test is underpowered. |
| Table II, monthly (133 funds) | 266 moments | sd 0.001; AR(1) 0.026 | 0.004; 0.074 | Not comparable to annual moments |
| **FTN sponsor flow (Table VIII column), linear rank** (`ftn_power.py`) | 81 (62 removed, 19 incumbent winners, 6 rounds) | 0.234 | **0.655** | Average sponsor slope implied by SSZ Table VIII: 0.2 x 1.050 + 0.6 x 0.310 + 0.2 x 1.389 = 0.674. MDE is about equal to SSZ's effect, so roughly 80% power only against an SSZ-sized sponsor. |
| FTN sponsor flow, piecewise | 81 | 1.92, 0.49, 1.08 | 5.4, 1.4, 3.0 | SSZ 1.050 / 0.310 / 1.389: not estimable meaningfully |
| FTN selection: P(win) on rank, linear probability model | 81 | 0.156 | 0.436 (worst-to-best change in win probability) | Detects only strong selection on returns |
| Regime column, monthly linear (`regime_power.py`) | 2,611 fund-months, 131 funds | 0.015-0.017 | 0.042-0.046 per month | Same categories 2019-2023: MDE 0.008 |
| Table IX annual, raw (`table9_power.py`) | 631 fund-years, 157 funds | PPM 0.135; non-PPM 0.225; difference 0.269 | 0.38; 0.63; 0.75 | SSZ DC -0.262 (0.163); non-DC -1.567 (0.455): a non-DC effect of SSZ size is detectable |
| Table IX annual, category-adjusted | 631 | 0.092; 0.116; 0.140 | 0.26; 0.33; 0.39 | SSZ objective-adjusted: DC -0.260 (0.160); non-DC -1.102 (0.436) |
| Table IX, FTN selection (`ftn_t9_power.py`, pre-award dispersion only) | 21 incumbent (+17 new) winners vs 66 removed | 0.074-0.129 pp per month | 0.21-0.36 pp per month = **2.5-4.3 pp per year** | Only very large selection alpha detectable: a bounded null at best |
| Non-PPM spillover, 6 months after award (SEK funds) | 17-29 winners vs 38 removed | 0.021-0.025 | 6-7% of non-PPM assets over 6 months (about 1.0-1.2% per month) | Cookson's listing effect is 0.16% per month (prior memo; not re-verified here): not powered |

Summary:
- **Powered:** the pre-2024 Table III replication in linear form, and the Table IX replication.
- **Marginal:** the FTN sponsor-flow slope, powered only against SSZ-sized effects.
- **Not powered:** Table II AR(1) (annual), any piecewise FTN estimate, FTN-period performance, and non-PPM spillovers.

---

## 6. Risks and solutions

| # | Risk | Solution | Fully solves or reduces? |
|---|---|---|---|
| 1 | **Question fit** (rival review: SSZ "do[es] not directly supply the outside-platform selection question"). | Change the question, not the anchor: SSZ's own question (sticky or discerning; sponsors or participants) with variation in whether a sponsor exists. The outside-platform question becomes one stated, underpowered column (section 5). | Reduces. A reader who wants Cookson's question will still prefer Cookson. |
| 2 | **Recency** (2015). | The course says "Read recent papers (<15 years)" (course_intro.txt, slide 11, line 165), and SSZ is 11 years old. Pair it with Tran and Wang (2023 JFE), who use SSZ's decomposition, and KPSS (2021 JFE). | Fully solves the rule; reduces perception. |
| 3 | **"No sponsor before 2024" is not exactly true:** 2019 re-registration (348 exits, SEK 60.9bn, capital to AP7 Såfa per earlier memo; not re-verified), misconduct deregistrations in 2017-18, mergers, third-party switching services (**NOT VERIFIED**). | Drop exit-year observations from the participant sample (SSZ's exits are censored too, Table VII). Show 2019 as a separate "rule-based deletion" placebo column. Flag mergers by ISIN continuity. Check DMS (2017) for switching services. | Reduces |
| 4 | **Non-PPM measurement:** SEK-only restriction, TNA gaps (39 of 759 funds), poor transfer-month reconciliation (median residual 35% of the transfer). | Use non-PPM flows only before 2024 and outside transfer months. Use FI quarterly total assets as an independent check. Treat any FTN-period non-PPM result as bounded. | Fully solves the replication; reduces for the extension |
| 5 | **File returns are integer-rounded; no non-PPM data before 2018.** | `nt` plus SHoF `tri_sek` from 2018. Ask SHoF for pre-2018 history (the brief says SHoF holds it) and Pensionsmyndigheten for the daily NAV archive (precedent: earlier SSE theses got NAVs from 2000, per the prior memo). | Fully solves if delivered; otherwise the replication is 2019-2023 joint plus 2008-2023 PPM-only |
| 6 | **FTN column power** (MDE 0.655, about equal to SSZ's 0.674). | Pre-register the linear form; add R6 when its transfers appear (N to about 100); add the 36-month rank. | Reduces |
| 7 | **Few independent events** (6 rounds, 5 award dates). | Round fixed effects; results round by round; leave-one-round-out; randomization inference permuting ranks within round. | Reduces (inference becomes honest; the information content does not grow) |
| 8 | **"Mechanical" objection.** | Section 4.5: SSZ's eq. (4) is equally mechanical; estimate selection separately from dose. | Fully solves conceptually |
| 9 | **The equalization rule drives winner doses** (incumbents keep their capital), so a High-segment slope may reflect the rule, not FTN preference. | Rule-implied dose computed from pre-award capital; report selection and dose separately. | Fully solves interpretation |
| 10 | **Transfer timing and composition:** default vs active; the December placement inside the R4 window (Nov 2025-Apr 2026); unexplained AMF Europa inflow in Mar 2025. | Ask Pensionsmyndigheten for a ledger per fund and date by transaction type. Otherwise use abnormal `nt` = `nt` minus the fund's pre-period flow rate and its December-placement share. | Fully solves with the ledger; reduces without it |
| 11 | **Table II comparability:** 5 annual observations, AR(1) MDE 0.174 above SSZ's 0.138; monthly moments not comparable. | Report annual as the replication and monthly as robustness. Claim nothing from AR(1) unless precisely estimated. | Reduces |
| 12 | **Framing risk:** the raw PPM annual flow sd (0.32) already exceeds non-PPM (0.18), so the naive "sticky" Table II prediction may fail. | Pre-commit the interpretation (section 4.4); the size control is SSZ's own explanation (p. 816). | Reduces |
| 13 | **Tutor and examiner fit.** Klug works on index inclusions (closer to Cookson or price pressure); his prompt lists "investor behaviour or market efficiency" and "selection design", which (A) covers. Sabbatucci's April 2026 working paper is about retirement-plan menu shifts, the sponsor channel. Several recent winners name Adrien d'Avernas as examiner (brief). | Bring Klug the A-or-B choice with the power table above. | Reduces |
| 14 | **Synopsis promises** (fees on and off the platform, supply, active vs default, performance after inflows). | Active vs default becomes the participant/sponsor columns; performance after inflows becomes Table IX. Fees and supply go descriptively in Table I. Tell Klug the scope narrowed. | Reduces |
| 15 | **Fund identity:** renumbering, mergers, very large non-FTN "exits" (2008-2011). | ISIN map after 2017; names and manual checks for large exits before 2017; Morningstar master has no merger link (brief). | Reduces |
| 16 | **Tran-Wang package not inspected.** | Not needed for (A). Open it on the SSE network as the replication-folder template. | Fully solves the dependency |
| 17 | **Rival review: "Remove the assumption that all decision-month flows are sponsor decisions ... Aggregate monthly observations do not identify those actors."** | The sponsor flow is event-defined (deregistration = -1; winner inflow inside the transfer window under the published rule), the same identification SSZ use with annual menus, with the same caveat as fn 18. The ledger (row 10) removes the rest. | Reduces; fully solves with the ledger |
| 18 | **Rival review: "Detailed original pension data are another access problem."** | Irrelevant: like Cookson, (A) is a different-dataset replication, which the course allows ("different dataset, time, application", slide 10). | Fully solves |
| 19 | **Course warning against "applying the question to Nordic countries unless meaningful."** | The Swedish setting changes the mechanism: no sponsor before 2024, then a sponsor is introduced. That variation does not exist in SSZ's US sample. | Reduces (it is a judgement the examiner must accept) |
| 20 | **Data calendar:** R6 transfers after Aug 2026; the global active round under appeal. | Design around the 6 completed rounds; R6 is an add-on. | Reduces |

---

## 7. Verdict

**On the brief's criteria (JUDGEMENT):**

1. **Anchor question equals thesis question:** yes, in the reframed form. The thesis asks SSZ's question where the sponsor's presence varies.
2. **Table-level replication:** yes, and more completely than for Cookson.
   - Tables I, II, III, IV (partly), VI, VII and IX are replicable on real Swedish data with the N above.
   - The joint PPM/non-PPM decomposition is exactly SSZ's DC/non-DC object.
   - The PPM ratio distribution reproduces SSZ's DC ratio almost exactly.
3. **Dated reform with treatment and control:** partly. FTN rounds are dated and pre-2024 PPM plus non-procured categories serve as controls, but the extension is a cross-section of 81 decisions, not a powered DiD.
4. **Extension inside the anchor's tables:** yes. Table VIII column, Table III regime column, Table IX FTN.
5. **Numbers comparable to the anchor's:** yes. Same units and specification, and SEs comparable to or smaller than SSZ's in Tables III and IX.
6. **Calibration:** predicted signs written before estimation (section 4.4).

**How strong overall.** Strong on replicability, power for the replication, and the fit between mechanism and institution: introducing a sponsor is what SSZ's theory is about. The design also contains the powered half of candidate (B), the selection regression (the linear probability model of win on rank), inside SSZ's Table VIII. Moderate on policy payoff, since the part Klug and the FTN debate care about rests on 81 decisions with MDE about equal to SSZ-sized effects. Weak on outside-platform spillovers, which this design should not headline.

**What would make (A) fail:**
- **The examiner reads the powered part as "SSZ on Swedish data".** The defense is the sponsor switch; if it is not accepted, the extension carries too little weight.
- **FTN's selection is roughly orthogonal to past returns.** This is plausible given a process-heavy quality score and 25% cost. The FTN column is then a null. With MDE 0.655 it still excludes SSZ-sized sponsor sensitivity, but cannot say more. That is acceptable only if written as a bounded result.
- **The transfer ledger is unavailable and the winner-dose puzzles (AMF Europa) cannot be resolved.** The dose half of the Table VIII column then becomes unreliable; the selection half survives.
- **The pre-2024 "no sponsor" premise is undermined** by the 2019 re-registration or switching services in a way that cannot be separated. Mitigated by exclusions and placebo columns, but a referee can press on it.
- **SHoF pre-2018 history and the NAV archive never arrive.** The joint replication stays at 5 annual cross-sections (2019-2023), where Table II AR(1) is underpowered.

---

## Appendix: files (all in `scratchpad/anchor_final/round1/ssz_work/`)

- `pages/`: SSZ page renders (`p-NN.png`; `rot-20, 22, 23, 24, 28, 31.png` for the rotated Tables IV, V, VI, VIII, IX).
- `scan_headers.py` writes `coverage_scan.json`: full header scan of all 307 files.
- `build_panel.py` writes `ppm_panel_all.csv`: fund-month panel, Jan 2001-Aug 2026.
- `link_shof.py` writes `ppm_shof_monthly.csv`: PPM to Morningstar link with returns and TNA.
- `validate_nt.py` writes `nt_validation_rows.csv`: test of "Handel, netto".
- `reconcile.py` writes `ppm_shof_flows.csv` and `reconcile_winners.csv`: non-PPM flows and the transfer-month reconciliation.
- `ftn_rounds.py` writes `ftn_cross_section.csv`; `ftn_power.py` writes `ftn_sponsor_sample.csv`: FTN cross-section and sponsor-flow MDEs.
- `table3_power.py` writes `t3_monthly_sample.csv` and `t3_annual_sample.csv`; `table3_linear_power.py`.
- `ppm_annual_counts.py` writes `ppm_annual_flows.csv`; `ppm_only_power.py`.
- `table9_power.py`, `ftn_t9_power.py`, `regime_power.py`.
- `olslib.py`: OLS with HC1 and fund-clustered SEs (statsmodels is unavailable in the container).
