# Referee report on candidate (C): Da, Larrain, Sialm and Tessada (2018 RFS) as anchor

Referee role: examiner (SSE, retirement plans and stock demand). Target: `round1/da_dossier.md`. Prepared 5 October 2026.
My scripts and outputs are in `scratchpad/anchor_final/round2/refC/` (`chk1.py` to `chk4.py`, `rerun_netting.txt`). Labels: **CONFIRMED**, **CORRECTED** (right number given), **UNVERIFIABLE**. Judgements are marked JUDGEMENT.

## 0. Verdict

1. **The arithmetic is sound.** Every netting statistic I recomputed from `fi26q1_smallcap_vectors.psv` matches the dossier to the third decimal. The DLST magnitudes are cited correctly. The "2.5% within eight days" correction is right.
2. **The design has a gap the dossier understates (FATAL as framed).** The only powered test, the award window, is an *announcement* test that DLST never runs. DLST's own test, at *execution*, is the transfer window, and the dossier rates it underpowered (MDE 4 to 8). The power benchmarks b = 2.2 and 3.6 are execution-time multipliers for pressure that DLST show reverses within about ten days. For pricing at the award they are an upper bound, not a central value.
3. **The headline rests on one fund's portfolio.** Meds Apotek alone carries 41% of the squared net FIP in S1, with leverage 0.41 on the slope. Edge's Q1 and Q2 weights correlate only 0.39. On Q2 holdings the Edge-robust residual sd is 0.509 pp, and with Edge not deploying it is 0.49. "Passes narrowly" should read "sits at the 0.5 bar".
4. **Power is overstated.** The dossier assumes the same 2.5% daily volatility for every stock, but the FIP is concentrated in micro-caps. Under size-dependent volatility the award-window MDE is 2.5 to 3.0 (S1) and 3.0 to 3.5 (S6), not 2.1 and 2.7.
5. **Section 3.3 misses the obvious replication.** DLST's headline Table 6 (and Table 8) can be replicated on DLST's own public Chilean index data through LSEG Workspace, which the course offers. That repairs the replication standard. It does not repair point 2.
6. **Recommendation.** (C) should not be the anchor. At most it is one pre-registered extension figure inside (A): the award-window cross-section, with S6 as the primary scenario. Re-scored rubric: 43 of 90 (48%) as the dossier stands, 53 of 90 (59%) at best after the fixes, against (A)'s 69 (77%).

---

## 1. Verification of load-bearing claims (19 checked)

| # | Dossier claim | My check | Status |
|---|---|---|---|
| 1 | Design: Chilean funds A (equity) to E (bonds); 22 recommendations; first 15 (A and E only, 27 Jul 2011 to 24 Jan 2014) are the main sample; switches effective t+4, priced at t+2, 5% daily cap | WebFetch of Pension.pdf (Table 2 text, p. 3726) | CONFIRMED |
| 2 | Table 6: 1.06% (0.29) day 1, 1.22% day 3, 0.33% day 10; 10-day window | WebFetch, Table 6 all ten days match `dlst_2018_key_numbers.txt` | CONFIRMED |
| 3 | Elasticity -0.45 = -0.48/1.06, with Δq = 2 × 16.9% / 70 | CONFIRMED. Note that "70" is the US$70bn **free float**. The implied b ≈ 2.2 is per pp of free float, not per pp of market cap as in the FIP | CONFIRMED (units caveat) |
| 4 | Table 11 Panel A: 0.714 (0.603) day 1, 3.613 (1.534) day 3; N 512 to 569; event FE; SE clustered by event | WebFetch. **Omitted by the dossier:** the controls are ln market cap, B/M and momentum (Panel B adds turnover). FIP units are not stated in the paper; reading "1 pp FIP gives 3.6 pp CAR" requires the same units on both sides | CONFIRMED; units UNVERIFIABLE |
| 5 | "About 2.5% within eight days" is wrong for the RFS paper | May 2015 draft: "almost 2.5%"; "peaks at 2.45% on day 8 with a t-statistic of 2.17"; raw IPSA; 15-day window. The RFS paper has no such number | CONFIRMED (the dossier's correction is right) |
| 6 | Table 8: day 1 adjusted 1.05%; CUM[1-3] 1.21% (p 0.014) | Two WebFetch summaries disagree (one gives CUM[1-3] 1.00%, p 0.0128) | UNVERIFIABLE (not load-bearing) |
| 7 | Allocation rule: equal split; incumbents keep their capital and are topped up only to the common level | FTN report §3.7 (lines 753-773): capital "fördelas lika mellan upphandlade fonder", incumbents "behåller ... sitt befintliga kapital" and are topped up "upp till samma nivå som övriga upphandlade fonder". This round: 5 new winners (Edge, Cliens, Danske, Nordea, SEB, all "(Ny)") receive T/5 = SEK 1.562bn each (March capital) or 1.682bn (August). The 5 incumbents (AMF, D&G, Handelsbanken, Lannebo Småbolag, Swedbank Robur; smallest D&G 3.230bn) receive nothing. **Ex-post check (new):** in the Sweden active round the new winners went from about 0.01bn to 3.05 to 3.36bn by end-March 2026, against a predicted 3.42bn. Carnegie Sverigefond took +0.61bn net, against a predicted 0.56 top-up. AMF, D&G and Folksam took about zero (`pa_panel_2023_2026.csv`) | CONFIRMED (text and realised behaviour); binding instructions still unread |
| 8 | T = 7.81bn (31 Mar), 8.41bn (31 Aug); FI covers 6.67bn (85%) and 7.51bn (89%) of the sell side; buy side 4 of 5 | Summed the 9 losers in `pa_panel`: 7.811 and 8.409bn. Evli + C WorldWide = 1.140bn (14.6%) and 0.896bn (10.7%). Danske missing | CONFIRMED |
| 9 | sd(net)/sd(gross) in SEK 0.58; corr(buy, sell) 0.50; top-10 share of squared net SEK 0.44 | Own code `chk2.py`: 0.580, 0.499, 0.437 | CONFIRMED |
| 10 | Residual net-FIP sd 0.73 pp (S1), 0.56 pp (S6); 0.43 pp without the top ten; top-10 share 0.70; sd(net FIP)/sd(gross FIP) 1.13 | `chk2.py`: 0.734, 0.558, 0.426, 0.700. Ratio 1.133 (rerun of `netting_q1.py`, reproduced exactly) | CONFIRMED |
| 11 | The tail comes from Edge's assumed pro-rata scaling | **Worse than stated.** Meds Apotek (all of its buying is Edge's) is 41.4% of the squared S1 net FIP, leverage 0.41. A 10% idiosyncratic move in Meds shifts the slope by 0.64 per pp, about 0.9 SE. Three of the top four FIP stocks are bought wholly or mostly by Edge. Variants: drop Meds only, 0.572; drop the 10 names only Edge buys, 0.538; Edge buys nothing (S7), **0.490**; Edge capped at 2% of market cap per stock, 0.578; Edge half pro-rata and half average, 0.586. Edge's Q1 and Q2 weights correlate **0.39** (Meds 1.78% falls to 1.01%; new names Upsales, SHT, Norion, Octave, SSAB). On full FI 2026Q2 holdings: S1 0.750, with the tail stock switching to **Upsales (+6.79 pp)**; S6 **0.509** (`chk3.py`) | CORRECTED (fragility larger) |
| 12 | Q1 and Q2 vectors correlate 0.954 / 0.967 / 0.946 | CONFIRMED in SEK. **In FIP units, which is what the test uses, the Pearson correlation is 0.745** (Spearman 0.92; 17 of the top 20 overlap) | CORRECTED (interpretation) |
| 13 | Market-cap matching: 174 of 188 stocks, 96.7% of gross SEK; exact caps | Gross share CONFIRMED (0.967). Lowest-similarity matches checked by hand: Nyfosa → ALTRA is correct (renamed Altra Fastigheter, press release 13 May 2026). Errors: (a) Fasadgruppen's interim-share line (SE0028000232) is a separate observation at the full company cap, so double-counted; (b) TF Bank is mapped to a "TFBANK / Avarda Bank" row at 11.48bn while an "AVARDA" row shows 12.79bn (duplicate source row); (c) Plejd (sell SEK 40m) and Neola Medical (Edge buy SEK 7.7m, a micro-cap) are excluded, though both could carry FIP of 1 pp or more; (d) the caps are from **5 Oct 2026, after the event**, so the FIP vector already contains post-award prices. Quality is good on names and poor on dating | CORRECTED (minor errors; dating flaw) |
| 14 | MDE, award window [-2,+5]: 2.06 (S1), 2.71 (S6) per pp | Arithmetic CONFIRMED (`mde.py`). With size-dependent volatility, σ_i = 2.5% × (mcap/3bn)^-β clipped to 1.2 to 6%, and White SEs (`chk4.py`): **S1 2.52 / 2.70 / 3.04 and S6 2.99 / 3.14 / 3.46 for β = 0.2 / 0.25 / 0.33**. Power at b = 2.2: 53 to 68% (S1) and 43 to 54% (S6). At b = 1.4: 20 to 34%. The volatility model is my assumption (NOT VERIFIED; it needs LSEG or FinBas) | CORRECTED |
| 15 | The transfer window is underpowered (MDE 3.7 to 8) | CONFIRMED for 30 to 42-day windows. **But** if tranche dates are pinned from daily TNA, a 5-day execution window gives MDE 1.63 (S1) and 2.14 (S6) with one tranche, or 2.30 and 3.02 with two half-tranches. The Sweden active round moved in two monthly tranches (Jan and Feb 2026: new winners about +1.5bn, then +1.3bn each) | CORRECTED (fixable) |
| 16 | Large/mid 2025 residual sd 0.39 (covered) and 0.46 (imputed) | Rerun reproduces 0.389 and 0.461 | CONFIRMED |
| 17 | "Placera published an at-risk list on 26 May" | The 26 May article ranks stocks by total Swedish fund ownership and says plainly that most of those funds are not on the PPM platform. It names no at-risk fund. The 27 May article (Mats Olsson): 93% of PPM-scaled capital is on the main list, 46% in mid caps, and hedge funds may act on the announcement | CORRECTED |
| 18 | December placements are about a tenth of FTN's size: December `nt` 51.6 / 40.5 / 41.7 / 42.0 / 44.3 / 47.4 / 49.8 / 51.3bn (2018-2025); Swedish small-cap December net 0.06 to 1.06bn | `ppm_panel_all.csv` | CONFIRMED |
| 19 | No transfer by 31 Aug 2026; FI 2026Q3 "likely after 7 December" | No transfer by 31 Aug CONFIRMED: the new winners hold 0.000 to 0.029bn; Evli fell from 0.83 to 0.36bn in June (an own-fund event). On the Q3 timing: FI 2026Q2 manager files are stamped 2 Jul to 21 Sep, 35 of 47 by 21 Jul, and every relevant manager (Spiltan, Carnegie, Lannebo, Cicero, Cliens, LF, Skandia, Atle) by 6 Aug, with SEB and Nordea on 17 and 19 Aug. Q3 files are therefore likely by mid-November (JUDGEMENT) | CORRECTED (judgement) |

Also checked by rerun only (not independent): the placebo pseudo-FIP (sd 0.276, corr -0.059); August-capital S1 0.801 and S6 0.615; MedCap's SEK 123m (consistent with Q2 weights Spiltan 5.20% and LF 1.35% against Q1's 5.31% and 1.24%). The same-day Europe small-cap award (category SEK 5.5bn, FTN report line 55) has a Swedish FIP the dossier calls "near zero" but **never computed**: NOT VERIFIED.

---

## 2. Design attacks and classified issues

| ID | Issue | Class | Fix | Solves? |
|---|---|---|---|---|
| **F1** | **The anchor and the test do not match.** DLST estimate execution-time pressure (Table 11 days 1 to 5 after flows that settle at t+4) that reverses (Table 6 day 10: 0.33%, n.s.). The award reveals flows *months ahead*. Under DLST's own results, a market with working arbitrage should price close to none of the transient component at the award. It prices only a permanent demand-curve effect (Shleifer and Greenwood-type), or front-running if arbitrage is limited, and DLST estimate neither. So b = 2.2 or 3.6 is not the award-window benchmark. The powered test is not DLST's, and DLST's test (execution) is unpowered in the dossier's design. Replicating "at Table 11 level" is really applying Table 11's specification to a different treatment timing | **FATAL as framed** | (a) Make Table 11 two-window: announcement [-2,+5] and execution [-1,+3] around each **tranche date** dated from daily TNA (SHoF `tnafund` for Danske, Evli and C WorldWide; daily NAV times units for Swedish funds), giving MDE 1.6 to 3.0 (I-15). (b) Benchmark the award window on announcement-then-reversal evidence: Greenwood (2005, JFE 75(3) 607-649, Nikkei 225 redefinition; citation VERIFIED via RePEc, content from memory and NOT VERIFIED). Say explicitly that DLST's multiplier bounds award plus execution together. (c) Pool the Sweden active execution tranches (Jan and Feb 2026; needs FI 2025Q4) | **Partly.** Fully only if small-cap tranche dates are identified and fall before about 15 November |
| S1 | **Course replication standard.** A Table 11 run on FTN data is the extension, not a replication. The course asks for "replicating the main quantitative exercise of a key paper" (course_intro p. 17); DLST's main exercise is Tables 6 and 8. Section 3.3 looks only for *Swedish* independent data and misses DLST's own public inputs: the 15 dates (Table 2), IPSA, MSCI World in CLP and the Central Bank of Chile exchange rate | SERIOUS | Replicate Table 6 (days 1 to 10, IPSA minus MSCI World in CLP, sign-flipped) and Table 8 column 2 (day dummies, Jan 2010 to Feb 2014) with LSEG Workspace, which has a course workshop on 15 Sep (syllabus line 82). Print the result beside 1.06 (0.29). Optional: Table 11 on SAFP monthly fund-A holdings, which DLST's appendix (p. 3751) says are public. Effort: 3 to 5 days for Table 6/8 (JUDGEMENT); IPSA and MSCI CLP coverage in LSEG NOT VERIFIED | **Largely.** The aggregate tables become a data-level replication; Table 11 stays method-level without SAFP data |
| S2 | **Tail dependence on Edge** (I-11): one stock, one fund, one quarter's weights | SERIOUS | Pre-register **S6 as the primary scenario** and S1 as a sensitivity; Huber or winsorised-FIP slope; leave-one-stock-out band; report S7 (0.49) honestly; use FI Q3 holdings (30 Sep, pre-transfer) for the execution test | Reduces |
| S3 | **Power overstated** (I-14): homoskedastic σ, c = 1, and b taken from the execution literature | SERIOUS | Estimate σ_i from LSEG returns for 2024-2025 *before* the event window is opened; compute MDE with White SEs and the RI null; state the bound a null can exclude (about 3 per pp, which is roughly DLST's day-3 point estimate and no lower) | Reduces (it measures the problem; it does not create power) |
| S4 | **A single event with cross-sectional dependence.** Randomisation inference (RI) with a frozen FIP vector over historical windows is a valid exact test of the sharp null if event and placebo windows are exchangeable. It absorbs the unconditional covariance between FIP and style. It does not absorb an event-specific style shock (Edge growth micro-caps against Spiltan's industrials during 28 May to 4 Jun 2026). It needs history for recent listings (Asmodee, Apotea, Norion, Octave). It must exclude windows near other FTN events and December placements. It typically *lowers* power when correlations are positive | SERIOUS | Studentised slope as the RI statistic; returns scaled by trailing volatility; DLST's controls (ln mcap, B/M, momentum) plus industry FE; windows from 2015 to 2025, excluding FTN dates and Decembers; minimum two years of history, otherwise flagged | Reduces; a single draw of the common shock cannot be fixed |
| S5 | **Information content of the award.** On fundamentals the award is information-free: FTN scores process and fees, not holdings. But (i) all 14 incumbents had been at risk since 29 Apr 2025, so only the identities are news; (ii) the market was primed on the channel (Placera 26 and 27 May, I-17); (iii) the award may trigger non-PPM redemptions at losers and certification inflows at winners, extra unmeasured FIP; (iv) the 10-day standstill and appeal risk (FTN §3.6) make day-0 news probabilistic | SERIOUS (iii); MINOR (i, ii, iv) | Incumbents' pseudo-FIP placebo (already built, corr -0.06) tests a "winner-portfolio signal"; measure losers' and winners' non-PPM flows over the window from daily TNA; check e-Avrop for any överprövning in this round; a fee-based P(win) surprise weight only as a robustness check | Reduces |
| S6 | **Expert bar and pandering.** The examiner's own working paper is on retirement-plan reallocations repricing equities; the tutor's thesis is on index-inclusion elasticities. A single-event, 174-stock cross-section whose slope is 41% one stock will be read against the examiner's own standard | SERIOUS | Cite each once; claim a bounded multiplier, not an elasticity; make leave-one-out and S6 the headline; no demand-system language | Reduces |
| S7 | **Drift from the synopsis.** The synopsis promises fees on and off platform, fund supply, default versus active choice and post-inflow performance. (C) tests none of them. "Market efficiency" is in Klug's prompt, not in the synopsis | SERIOUS (process) | Written sign-off from Klug at the 9 October meeting; keep fees and default acceptance as Table 1 descriptives | Solves if Klug agrees |
| S8 | **Missing data, and timing against 7 December.** Daily returns, turnover and shares outstanding (FinBas or LSEG); Danske, Evli and C WorldWide holdings; FI 2025Q4 (for large/mid execution) and 2026Q3; tranche dates. If the small-cap transfer lands in late October, the execution window closes in November, which is tight but feasible | SERIOUS | Use LSEG now for returns, caps and shares outstanding (low risk); download FI 2025Q4 and Q3 when published; date tranches from daily TNA; Danske factsheet or SHoF holdings; freeze the award-window analysis by 1 November | Reduces; the foreign holdings remain partial (S1 to S3 bounds) |
| M1 | **Post-event caps.** Caps from 5 Oct 2026 put post-award prices into the FIP. That compromises the "blind" claim and makes the FIP endogenous to the outcome | MINOR (now), SERIOUS if kept | FIP = (PPM capital / fund AUM) × (fund's shares / shares outstanding), using FI `shares` and LSEG shares outstanding at day -10. This is price-free | Solves |
| M2 | Matching errors (I-13 a to c) | MINOR | Sum share lines by company; resolve TF Bank / Avarda; add Plejd and Neola caps (First North, Spotlight) | Solves |
| M3 | Controls: log market cap only, while DLST Table 11 uses ln mcap, B/M and momentum | MINOR | Add DLST's set, plus Amihud | Solves |
| M4 | "Per-event precision about twice DLST's" compares an *assumed* homoskedastic SE on an 8-day window with DLST's *estimated*, event-clustered SE on a 3-day window | MINOR | Delete the claim | Solves |
| M5 | Same-day Europe small-cap award: Swedish FIP not computed | MINOR | Compute from Swedish-domiciled Europe small-cap funds' FI holdings and add it to net FIP | Solves for covered funds |
| M6 | With acceptance at 0.85, opt-outs plausibly go to the same-category incumbents, which contaminates the zero-flow incumbents placebo | MINOR | Check incumbents' `nt` in the transfer month; scale the placebo accordingly | Solves |
| M7 | The Q1-to-Q2 "pre-trading" check is weight drift, not pre-trading, and SEK correlations hide FIP-unit instability (I-12) | MINOR | Q3 (30 Sep) holdings and losers' cash share before the transfer | Largely solves |
| M8 | The "residual sd ≥ 0.5 pp" go/no-go bar is not a power criterion | MINOR | Replace it with a pre-registered MDE against a stated b range | Solves |

**Section 3.3 evaluated.** The dossier is right that the 2011 mass-switch ban (no event dates, no holdings), the 2019 purge (staggered, one-sided, capital mapping missing; AP7 Såfa also holds Swedish equity, so even that flow partly nets) and December placements (FIP about a tenth of FTN's, one-sided, December seasonality) give **no powered Swedish replication**. Its conclusion "no independent replication is feasible" is **CORRECTED**: DLST's own public Chilean inputs allow a data-level replication of Tables 6 and 8 in days (S1). One extra point: other FTN rounds' execution tranches (Sweden active Jan and Feb 2026; Nordic May 2025) add events but are not independent of FTN.

---

## 3. Re-score on the winners-audit rubric

| # | Criterion (weight) | Audit's C | As the dossier stands, with my corrections | Best version after fixes | Reason |
|---|---|---:|---:|---:|---|
| 1 | Same-question anchor (2) | 4 | 3 | 3 | DLST's question is execution-time pressure; the headline is an announcement test (F1) |
| 2 | Table-level replication (3) | 1 | 1 | 3 | No replication now; Chilean Table 6/8 at data level after S1 |
| 3 | Extension inside the anchor's specification (2) | 2 | 2 | 3 | Table 11 specification with DLST controls, split into announcement and execution |
| 4 | One headline question (2) | 4 | 4 | 4 | |
| 5 | Informative result (powered or bounded) (3) | 1 | 2 | 2 | A power analysis now exists, but corrected MDE 2.5 to 3.5 against plausible b ≤ 2.2 |
| 6 | Identification from the institution (2) | 3 | 3 | 3 | Dated, mechanical rule confirmed ex post; one event |
| 7 | Avoids non-winner failure modes (2) | 2 | 2 | 3 | 5202-type window fishing is avoided only if pre-registered |
| 8 | Institutional or unique data (1) | 2 | 3 | 3 | FI Q1, Q2 and Q4 holdings, FTN reports, PPM files |
| 9 | Fit with the tutor's prompt (1) | 3 | 3 | 3 | "Market efficiency" is in the prompt; drift from the synopsis |
| | **Total (max 90)** | 41 (46%) | **43 (48%)** | **53 (59%)** | (A) 69 (77%); (B) 48 (53%) |
| | Equal weights (max 45) | 22 | 23 (51%) | 27 (60%) | (A) 34 (76%) |

Even fully fixed, (C) stays 16 points behind (A). It closes the gap only on criterion 2, and only by adding a Chilean replication that does not touch FTN at all.

---

## 4. The best version of (C), and where it belongs (one page)

**Question.** Do mandated, information-free pension reallocations move individual stock prices in proportion to net flow-induced pressure, first when they are announced and then when they are executed?

**Replication (on DLST's own data).** Table 6 (aggregate IPSA minus MSCI World in CLP, days 1 to 10, the 15 Table 2 dates) and Table 8 column 2 (calendar-time day dummies, Jan 2010 to Feb 2014), from LSEG Workspace. Report the result beside 1.06% (0.29), 1.22% and 0.33%. Table 11 on SAFP holdings only if the data arrive by 20 October.

**Extension (Sweden small cap, award 28 May 2026).**
- Net FIP from FI 2026Q1 share counts over pre-award shares outstanding (price-free), plus the same-day Europe small-cap round.
- The water-filling allocation, which held ex post in the Sweden active round: SEK 1.56bn to each new winner, nothing to incumbents.
- **S6 primary**, S1 and S3 as bounds. Leave-one-stock-out and Huber slopes reported in the main table.
- DLST Table 11 specification: CAR on net FIP; controls ln mcap, B/M, momentum and Amihud; industry FE. Two windows:
  - announcement [-2,+5];
  - execution [-1,+3] around each transfer tranche dated from daily TNA, with Q3 holdings.
- Inference by studentised randomisation over 2015-2025 windows, excluding FTN and December dates. Incumbents' zero-flow placebo. A second execution event from the Sweden active round (Jan and Feb 2026 tranches, FI 2025Q4), pooled.

**Calibrated claims.** Corrected MDE is about 2.5 to 3.5 per pp for the announcement window and about 1.6 to 3.0 for a tranche-dated execution window. So a null excludes DLST's day-3 point estimate (3.6), not its aggregate implied multiplier (about 2.2). Any positive slope must survive dropping the top-FIP stock and holding under S6. Benchmark the announcement window against announcement-then-reversal evidence (Greenwood 2005), not against DLST's execution multipliers.

**Cost.** About 4 to 5 weeks of the 9 remaining (JUDGEMENT). The critical path is the small-cap transfer date: if it falls after about 15 November, the execution half is only a labelled first look.

**Should (C) be the anchor?** **No.** Even in its best version, the powered half (announcement) is not DLST's design, the DLST-matched half (execution) depends on a transfer date not yet observed, and the estimate rests on a handful of micro-caps bought by one fund of SEK 0.5 to 0.7bn. (A) already has a powered, table-level, same-data replication.

**Use inside (A):** one pre-registered extension figure. The award-window cross-section of CAR on net FIP (S6 primary, leave-one-out band, RI p-value), framed as the price consequence of the sponsor's flows. Add the execution window only if the tranche dates fall before mid-November. Do not import a second replication: the Chilean tables would make (A) a two-anchor thesis, and that is the fan-out risk the winners audit flags (criterion 7).

---

### Files
- `round2/refC/chk1.py`: ISIN-to-cap match audit (duplicates, name similarity, unmatched holdings).
- `round2/refC/chk2.py`: independent netting statistics; Edge variants S6 to S9; leverage.
- `round2/refC/chk3.py`: FI 2026Q2 recomputation with exact caps; Edge Q1 against Q2.
- `round2/refC/chk4.py`: heteroskedastic MDE.
- `round2/refC/rerun_netting.txt`: rerun of `netting_q1.py`, identical to the log.

Sources: DLST RFS PDF https://academicweb.nd.edu/~zda/Pension.pdf ; 2015 draft https://www7.uc.cl/economia/finance_uc/docs/conferences/9th/LARRAIN_DLST_2015.pdf ; NBER w22161 (April 2016, "Coordinated Noise Trading") https://www.nber.org/papers/w22161 ; Placera 26 May 2026 https://www.placera.se/nyheter/pensionsrisk-i-smabolagen-har-ager-svenska-fonder-mest-2026-05-26 ; Placera 27 May 2026 https://placera.se/nyheter/har-ligger-den-dolda-risken-i-fondtorgets-miljardbeslut-2026-05-27 ; Nyfosa rename https://www.placera.se/pressmeddelanden/nyfosa-nyfosa-changes-name-to-altra-fastigheter-20260513 ; Greenwood (2005) citation https://ideas.repec.org/a/eee/jfinec/v75y2005i3p607-649.html ; FTN Sverige småbolag report (`ftn_txt/`), lines 50-125, 753-773, 833-867, 957-1012.
