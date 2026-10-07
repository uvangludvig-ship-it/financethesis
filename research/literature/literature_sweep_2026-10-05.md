# Wide literature sweep: does anything beat SSZ (2015)?

Run 5 October 2026, evening, after the anchor decision. It supplements `round1/outside_search.md`, which assessed about 35 papers chosen from known strands. Coverage: OpenAlex, Scopus, EconLit and Semantic Scholar, about 9,500 records in total.

## Most important finding: Dahlquist and Martinez (2015) already ran a version of the headline test

**Dahlquist, M. and Martinez, J. V. (2015), "Investor Inattention: A Hidden Cost of Choice in Pension Plans?", European Financial Management 21(1), 1-19.** Doi 10.1111/j.1468-036X.2013.12008.x. Published version read in full (EBSCO PDF; JEL G11, G23, H55); it matches the EFMA 2012 working paper. Table 2 is on p. 11 (N = 8,663 per system). Detailed notes: `research/literature/dahlquist_martinez_2015_notes.md`.

- **Data:** Swedish premium pension, October 2000 to July 2008, **quarterly**. 263 equity funds (230 in March 2008), all offered both in the PPS and in the retail market; the default fund is excluded. Only pension assets managed by investors themselves (96%). Pension TNA and returns come from the PPM. Retail data come from Finansinspektionen and Svensk Fondstatistik (quarterly only). Returns are net of fees and adjusted for PPM rebates.
- **Flow measures:**
  - absolute SEK flow, TNA_t - TNA_{t-1}(1+R_t);
  - "relative" flow = absolute flow / **total assets of the whole market** (retail or PPS), so it measures market share, not SSZ's flow over the fund's own TNA.
  - Flow over own TNA was tried; it is described as noisy and "intermediate", and not tabulated.
- **Specification (Table 2):** Flow_it = α_t + β·Rank_{i,t-1} + γ·(log TNA × contribution-quarter dummy) + δ'(log TNA, one-year volatility, [lagged flow]) + ε. The rank is the raw one-year return rank, 0-1. Retail and pension equations are estimated jointly as a system, with pairwise bootstrap standard errors (1,000 replications).
- **Results:**

| System | Retail β | Pension β | Test of equality |
|---|---|---|---|
| I (absolute) | 0.064*** (0.014) | 0.007 (0.009) | rejected; bootstrap: pension exceeds retail in about 1% of draws |
| II (absolute, lagged flow) | 0.043*** | 0.001 | rejected |
| III (relative) | 0.023*** (0.005) | 0.003 (0.012) | **Wald p = 0.123; bootstrap 0.067** |
| IV (relative, lagged flow) | 0.018*** | 0.003 | **Wald p = 0.254; bootstrap 0.133** |

- In market-share terms the pension-versus-retail gap is **not statistically significant**. The pension coefficient is imprecise (SE 0.012); the authors rely on the economic size (6-8 times).
- **Tables 3-5:**
  - Pension money holds more in the bottom decile (9.18% vs 6.88%) and keeps flowing in (adjusted flow gap -1.89 pp).
  - Pension money holds more in the subsequent worst performers.
  - The aggregate alpha gap of 0.43-0.51% a year is not significant.
- **Policy proposal:** an automatic "back to the default" clause. They do not propose a curated menu.
- **Not in the paper:** plan sponsors, SSZ, or any menu curation.
- **None of the nine anchor reports cite it** (checked by text search of the anchor-contest reports, now in `research/_archive/anchor_selection_2026-10-05/`).

### What it means for the frozen design

1. **Novelty.** "PPM money is less performance-sensitive than other money in the same funds" is already published for 2000-2008, though only significantly in SEK terms, not in the market-share specification. It cannot be the headline claim on its own. The contribution has to be one of these:
   - the first test with SSZ's fund-level flow definition and enough power to separate the two coefficients (D&M's pension SE of 0.012 could not);
   - whether the gap survives 15 years and the 2019-2022 fund-market reforms (2020-2023);
   - SSZ's sponsor attribution (Sweden as the no-sponsor counterpart to SSZ's US DC money);
   - the FTN sponsor column.
2. **Replication opportunity.** D&M is a Swedish, same-data, table-level target by an SSE/SHoF author. If quarterly retail TNA from before 2018 can be obtained (SHoF request, risk S3), the thesis can replicate D&M's Table 2 (Systems I-IV) for 2001-2008 on the same PPM files and then extend it to 2020-2023. That is a stronger replication than SSZ-on-Swedish-data, and it answers risk S1, because the thesis would be built on a Swedish predecessor.
3. **Framing.** The natural story becomes reconciling the two papers:
   - US DC money is *more* performance-sensitive than other money, attributed to sponsors (SSZ);
   - Swedish sponsor-free DC money is *less* sensitive (D&M);
   - FTN now adds a sponsor.

   The working title still fits. Evans and Fahlenbrach supply the mechanism language: "market governance" (investors leaving) against "traditional governance" (sponsors replacing options). Keim and Mitchell (2018) show what a sponsor's removal round does to savers.
4. **Pre-registration.** H_noSponsor now has a Swedish prior: a pension/retail sensitivity ratio of about 0.13 (0.003/0.023) in market-share flows. Converted to SSZ-style fund-level annual units (×230 funds, ×4 quarters) it implies a gap of about −0.18 per year, close to the frozen −0.17 (see `PLAN.md` §4.2). This is a calibration only; no thesis coefficient is opened.
5. **Anchor choice.** D&M does not replace SSZ as the anchor: EFM is not a top-tier journal, and it has no sponsor or FTN dimension. It enters as the direct predecessor and second replication target. Raise it with Klug together with the A/B question.

## Method

- **Google Scholar:** SSZ related articles (16 papers). Scholar then blocked the network for "unusual traffic".
- **OpenAlex:** 3,154 works.
  - Forward citations of SSZ, Tran-Wang, Cookson et al., Da et al., Kronlund et al. and Pool-Sialm-Stefanescu 2016.
  - 40 question-based keyword searches.
  - Topic filters across 14 top finance and economics journals, 2017-2026.
  - SSRN and NBER working papers, 2022-2026.
  - 591 topic-relevant by title; about 45 read at abstract level.
- **Scopus** (SSE login): 988 records, 807 topic-relevant.
  - 11 structured concept searches.
  - Forward citations of SSZ (104 in Scopus), TW, CK, DA, KPSS, PSS16, Zalewska and Wong-Tsang.
  - About 15 further abstracts read.
- **EconLit with Full Text** (SSE login, EBSCO): 1,840 records from 8 searches, including the JEL G23 descriptor × flows, performance sensitivity and switching. 484 screened by title; about 13 abstracts read.
- **Semantic Scholar** (API): 3,544 records.
  - 14 FTN-area keyword searches (2,089 hits) plus seed-based recommendations.
  - 1,006 screened by title; about 25 abstracts read. See the section below.
- **Full text read:** D&M (2015), published version. Keim and Mitchell (NBER w21854) read at abstract level only, since the PDF did not render in the browser.
- **Not done:** Swedish-language searches (DiVA, Riksrevisionen); other full texts.

## Verdict

No paper beats SSZ as the anchor. D&M (2015) changes the novelty claim and adds a Swedish replication target (see above). By the last of the four databases, new finds had dropped to a few close analogues per area, so the search is close to saturated.

## Other new papers worth using (SSZ question)

| Paper | What it shows | Use |
|---|---|---|
| Fricke, Jank and Wilke (2026), "Mutual Fund Clienteles", RFS, doi 10.1093/rfs/hhag019 | Flow-performance sensitivity differs by investor sector within the same fund-quarter; households least sensitive, investment funds most | Top-tier recency partner for the headline test. Sharpens risk S2: fund-of-funds money inside non-PPM flows is the most sensitive clientele and pushes Δ negative. Data confidential (SHS-S). |
| Jank (2010), "Are there disadvantaged clienteles in mutual funds?", working paper | German sector data: households chase performance but show status-quo bias; financial corporations chase strongly | Earlier version of the FJW evidence; clientele split. |
| Evans and Fahlenbrach (2007), "Do Funds Need Governance? Evidence from Variable Annuity-Mutual Fund Twins", working paper (CRR WP 2007-20; SFI RP 11-31; unpublished) | Same funds inside variable annuities vs retail: annuity money is less sensitive to performance and fees; annuity sponsors compensate by adding options and replacing advisers | **Conceptually the closest paper to "did the premium pension need a sponsor".** Mechanism language. |
| Evans and Fahlenbrach (2012), "Institutional Investors and Mutual Fund Governance: Evidence from Retail-Institutional Fund Twins", RFS 25(12), 3530-3571 | Institutional co-investors monitor and improve the retail twin | Citable top-journal version of the monitoring-on-behalf-of-passive-investors idea. |
| Sialm, Starks and Zhang (2018), Journal of Investment Management | Practitioner summary of SSZ 2015 | Cite alongside SSZ. |
| Brown and Van Harlow (2012), IJPAM | Options chosen by sponsors beat non-plan funds by up to 120 bp a year (30,000 plans) | Benchmark for whether FTN's selections beat the funds it removed. |
| James and Karceski (2006), JBF | Institutional funds with weaker investor oversight underperform | Monitoring motivation. |
| Karlsson, Massa, Simonov and Madrian (2007); Palme, Sundén and Söderlind (2005/2007); Engström and Westerberg (2003); Hedesström et al. (2005/2007) | Early PPM choice studies | Background on PPM menu and choice. |
| Keswani and Stolin (2012), Journal of Financial Research | Flow-performance sensitivity differs across seven UK distribution channels for the same funds | Supports the within-fund design. |
| Koh and Mitchell (2010), Pensions | Singapore CPF board admits funds by criteria; included managers outperform excluded | Closest analogue to FTN admission/removal (government-curated menu). |
| Tang, Mitchell, Mottola and Utkus (2010), JPubE | Sponsors build efficient menus; participants undo it | Sponsor-versus-participant split. |
| Goldreich and Halaburda (2013), Management Science | Menu-setters differ in ability; larger 401(k) menus are worse | Motivation for FTN shrinking the menu. |
| Zalewska (2021), Management Science 68(7) | UK DC funds with third-party oversight earn 0.96-1.67 pp more and charge 0.7 pp less | Oversight matters for outcomes. |
| Kavourakis and Tanewski (2026), Accounting and Finance 66(2) | Failing Australia's regulator performance test cuts net flows by 9 pp of assets | Closest published analogue to FTN grading funds. |
| Wong and Tsang (2016), Contemporary Economic Policy 35(2) | Hong Kong MPF: removing employer-restricted menus raised flow-performance sensitivity | Mirror image of the thesis. |
| García, Reñé and Agudo (2015); Cheong, Sung and Kang (2019) | Pension funds vs investment funds flow-performance (Spain; Korea) | International comparisons for Table 2. |
| Gutierrez Cortez, Ivashina and Salomão (2025), NBER w33693 | Chile and Peru DC switching is performance-sensitive | Recency. |
| Barahona (2025), working paper | Fee-insensitivity explained by intermediaries' standard of care | Fee side of Table 1 panel B. |
| Dannhauser and Pontiff (2026), RFS; Bessembinder et al. (2026), RFS; Broman and Lovelace (2026), EFM | Current flow-performance evidence; U-shape | Literature review; tail-contrast test. |
| Florentsen et al. (2022), RoF; Bjerksund et al. (2025), MS | Nordic distributor steering; Scandinavian regulator intervention | Nordic context. |
| Luco (2019), AEJ: Micro | Chile switching costs and fees | Inertia context. |

## Semantic Scholar sweep across all FTN areas (not only SSZ)

Semantic Scholar API, run in the browser. **14 keyword searches**, one per FTN area, 2000-2026, economics and business: procurement and auctions; regulator performance tests; menus; fund removal; fund closures and mergers; negotiated fees and scale; fee competition; price pressure from mechanical flows; defaults and inertia in national DC systems; supply-side entry; gatekeepers and ratings; flow-performance; ESG exclusion; manager selection.
- 2,089 hits.
- Plus seed-based recommendations from four seed sets, which gave 3,544 records in total. The recommendations were mostly off-topic 2026 noise.
- After filters, 1,006 titles were screened and about 25 abstracts read.

What it adds, by FTN area:

| FTN area | New papers | Use |
|---|---|---|
| **Removing funds from a menu** | **Keim and Mitchell (2018), "Simplifying choices in defined contribution retirement plan design: a case study", JPEF (NBER w21854)**: a large employer deleted nearly half the plan's funds; participants who were moved ended up in funds with lower turnover and expense ratios (about $9,400 saved per participant over 20 years) and held less equity and lower factor risk. Also Benz (2018) on a T. Rowe Price fund closure changing retirement savers' portfolios. | **The closest published analogue to an FTN removal round.** Benchmark for what happens to savers' money and fees when a menu-setter removes funds; motivates Table 1 panel B and any removed-fund outcome table. |
| **Limiting providers / procurement** | Clark and Richardson (2010), "Who's Watching the Door? How Controlling Provider Access Can Improve K-12 Teacher Retirement Outcomes" (US 403(b) vendor limits); Illanes (2016), "Switching Costs in Pension Plan Choice" (Chile); Uyen (2016), Economía y Sociedad, on Latin American fee auctions (fees fall, effect on competition ambiguous); Kurach et al. (2019) and the Chile auction papers. | Procurement analogues; motivation for FTN's fee goal. |
| **Fee competition and spillover** | Wahal and Wang (2011), "Competition Among Mutual Funds", JFE (incumbents cut fees when overlapping new funds enter); Khorana and Servaes (2012), RoF; Dyck and Pomorski (2011), "Is Bigger Better? Size and Performance in Pension Plan Management" (scale lowers costs); Betermier, Schumacher and Shahrad (2023), RAPS (fund proliferation deters entry). | Theory and evidence for whether FTN's procured fees spill over to the same funds outside PPM. Only a descriptive Table 1 item under the frozen design. |
| **Price pressure from mechanical reallocations** | Ceballos and Romero (2020, SSRN): advisory-triggered Chilean pension switches move government bond prices persistently (a Da et al. analogue in bonds); Brzeszczyński, Bohl and Serwa (2018), JPEF: Polish ZUS-to-OFE transfers give temporary price pressure; Lou (2012), JF; Chen, Noronha and Singal (2006), FAJ (index changes). | Relevant only to candidate C (dropped). Cite in one sentence if transfer timing is discussed. |
| **Regulator ratings and tests** | Watson et al. (2016), "Australian superannuation fund product ratings and performance", AJM; Kavourakis and Tanewski (2026). | Background for FTN as a public rater. |
| **Clienteles and flow-performance** | Jank (2010) confirmed as the most-cited clientele paper (126 citations); retail vs institutional flow-performance (FRL 2017; TEL 2019); Clark-Murphy, Gerrans and Speelman (2009), Australian superannuation return chasing. | Supports the within-fund design. |

Nothing in these areas beats SSZ as the anchor or gives a powered FTN test. The FTN-side literature is thin, international and mostly in field journals, which supports FTN's novelty.

## Novelty (FTN)

No academic paper on Fondtorgsnämnden was found in OpenAlex, Scopus, EconLit, Semantic Scholar or by web search of DiVA. Riksrevisionen's audit is still the main FTN novelty risk. The PPM-versus-retail flow sensitivity result is **not** novel as a direction (D&M 2015), but has not been shown significantly in relative terms or after 2008.

## Follow-ups

1. Decide whether to replicate D&M Table 2 (Systems I-IV) for 2001-2008. It needs quarterly retail TNA from before 2018 (Finansinspektionen, Svensk Fondstatistik or SHoF).
2. Done: H_noSponsor cross-checked against D&M (about −0.18 vs −0.17). Write the conversion and its caveat into the PAP.
3. Read in full: Keim and Mitchell (2018, JPEF), Fricke-Jank-Wilke (2026), Evans and Fahlenbrach (2007 WP and 2012 RFS).
4. Swedish-language searches: DiVA directly; Riksrevisionen audit status.
5. Unassessed SSRN items: Loseto 2023; de Vries et al. 2023; Gropper 2023; Andonov, Bonetti and Stefanescu 2022/2025.
