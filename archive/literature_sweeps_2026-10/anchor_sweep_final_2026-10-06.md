# Final anchor sweep (6 October 2026): does anything beat SSZ?

**Verdict: no. Sialm, Starks and Zhang (2015, JF) stays the anchor. The anchor question is closed. Do not reopen it.**

## Method

- Six parallel research agents each covered one FTN area, all using one shared brief and rubric:
  1. sponsors and menus;
  2. public procurement and tenders;
  3. gatekeepers and ratings;
  4. fees and buyer power;
  5. forced reallocation and price pressure;
  6. PPM, the Nordics and novelty.
- About 300 distinct queries in total, on Firecrawl first and WebSearch as a fallback.
- Agent 1 also followed the OpenAlex citation trails of every paper citing SSZ (207) and every paper citing Pool-Sialm-Stefanescu 2016 or Kronlund et al. 2021 (131).
- Rubric, 0-3 on each of six criteria: question fit, top journal and recent, replicable on our data, power, extension inside the anchor's tables, fit to tutor and examiner. **SSZ scores 14/18.**
- **Coverage limits:**
  - Firecrawl hit rate limits (HTTP 429) and is low on credits.
  - The shared WebSearch budget ran out near the end.
  - Thinnest coverage: Norway, Denmark and Finland; some Latin America follow-ups; 2024-2026 working papers on gatekeepers.
  - The six areas overlapped heavily, and every agent independently reached the same verdict.

## Finalists, with an adversarial check against SSZ

| Paper | Score | Why it does not beat SSZ |
|---|---|---|
| Bjerksund, Døskeland, Sjuve & Ørpetveit (2026), "Forced to be Active: Evidence from a Regulation Intervention", *Management Science* 72(5), 4341-4358 (verified on RePEc) | 12 | **Wrong question.** A regulator's action against closet indexers, not a sponsor that selects funds and moves capital. As an FTN transplant, "winning a tender" is an endogenous treatment (winners are chosen on quality and fees), unlike their exogenous intervention. With about 75 treated funds and 6-30 months of post-period, the headline would be weaker than SSZ's (MDE 0.10). |
| Goyal & Wahal (2008), *JF* 63(4), 1805-1847 | 9-11 | The most FTN-shaped question: does a selector hire better managers than it fires? But it is 18 years old, and the post-selection return test cannot be powered on FTN (about 75 winners, short post-periods). Its pre-selection side is already our Table 3. |
| Del Guercio & Tkac (2002), *JFQA* 37(4), 523-557 | 11 | Conceptual ancestor of SSZ: flows from pension clients versus retail. Old, and its pension side is separately managed accounts, not the same funds. SSZ supersedes it. |
| Brown, Gredil, Kantak & Ramadorai (2023), *RFS* 36(8), 3071-3121 | 10 | Selected versus non-selected candidates (FTN-shaped and recent), but built on one allocator's proprietary due-diligence log. Only the returns table transplants, and it is underpowered. |
| van Binsbergen, Kim & Kim, *JFQA* (forthcoming, online Oct 2025) | 10 | Scale and capital allocation. Not the FTN question; its fund-level estimates need long series. |
| Ben-David, Li, Rossi & Song (2022), *RFS* 35(6), 2790-2838; Gantchev, Giannetti & Li (2024), *JFE* 155; Ceccarelli, Ramelli & Wagner (2024), *RoF* 28(1); Jones & Martinez (2017), *JFQA* 52(6) | 10 | Certification and ratings mechanisms. Wrong question or not replicable on our data. |

**Fatal-flaw summary:**
- No published paper from 2016 or later combines all three of these:
  - an FTN-shaped question (a public or institutional selector moving pension money);
  - a top journal;
  - table-level transplantability to our data with a powered headline.
- Every paper that tests selection quality fails on power, because FTN's sample is small.
- SSZ's headline is powered: its MDE is 0.10 against benchmarks of ±0.17-0.185.

## Novelty (the FTN area is unclaimed)

- **No academic paper on FTN exists.** We searched journals, working papers and BSc/MSc theses (DiVA, LUP, GUPEA) as well as SNS, Ratio, Timbro and Fores. The latest PPM thesis on DiVA, Sener & Ärleskog (2026, Linköping), compares active and passive funds with AP7 and is not about FTN.
- **The PPM versus non-PPM flow test for 2009-2026 has not been done.** Dahlquist & Martinez cover 2000-2008, and Engström & Westerberg about 2000-2002.
- **FTN's own follow-up** (as reported by European Pensions, 18 March 2026; the FTN source report was not located):
  - procured European index funds returned +0.29 pp in their first year (4.85% vs 4.56%);
  - active European equity funds returned about +1.5 pp;
  - FTN expects about +0.5 pp a year platform-wide.
  - These are raw before/after numbers with no counterfactual, no risk adjustment and no flows. Cite them, and position the thesis as the first benchmarked evaluation.
- **Riksrevisionen audit "Ett upphandlat fondtorg för premiepensionen":**
  - decided 2 June 2026 and announced 5 June 2026; still ongoing; no publication date set (checked 6 October);
  - it audits FTN, Pensionsmyndigheten and Regeringskansliet on how efficient and fast the transition is (only about a third of platform assets had been procured by May 2026);
  - it does not cover flows or selection quality, so it does not pre-empt the thesis;
  - **re-check the audit page in November:** https://www.riksrevisionen.se/granskningar/pagaende-granskningar/ett-upphandlat-fondtorg-for-premiepensionen.html
- **Earlier audit:** RiR 2018:32, "Förvaltningen av premiepensionssystemet – kostnadseffektivitet för spararnas bästa?" The government's reply is skr. 2018/19:80. It works as motivation.
- **Correction:** the title of SOU 2019:44 is "Ett bättre premiepensionssystem".

## What changes in the design: nothing

The agents proposed five additions. Each is checked against `PLAN.md` (five exhibits, the drop list):

| Suggestion | Decision |
|---|---|
| Goyal & Wahal-style pre-selection comparison of winners, losing bidders and removed funds | **Already in Table 3** (stage 1 and stage 2 on past returns). Cite Goyal & Wahal as the design ancestor. |
| Barr & Diamond (2020) hypothesis: procurement "weeds out" bad funds better than it picks high performers | **Adopt as framing only.** It gives Table 3 a falsifiable reading: compare return dependence at stage 1 (who stays or leaves) with stage 2 (who wins). Write it into the PAP before any coefficient is opened. |
| Post-selection returns of winners versus losers | **Not added.** It is the dropped FTN-period Table IX and is underpowered. |
| Fee spillover to winners' non-PPM share classes (FI 2025 report; Evans, Gómez & Zambrana) | **Not added.** FTN-period non-PPM spillovers are on the drop list. One sentence of future research, citing the FI report. |
| Tran & Wang split of flows into FTN-moved and saver-driven | **Not applicable.** The headline sample, 2020-2023, predates FTN's capital moves. |
| Bjerksund-style difference-in-differences of fees, active share and alpha after winning | **Not added.** It would be a sixth exhibit and its power is low. |

## New references worth citing (pick within the 20-30 budget)

**Closest to the design:**
- Del Guercio & Tkac (2002), *JFQA* 37(4), 523-557: pension versus retail flow-performance, the ancestor of SSZ.
- Goyal & Wahal (2008), *JF* 63(4), 1805-1847: sponsors hire after good returns, with no excess return afterwards. Design ancestor for Table 3.
- Brown, Gredil, Kantak & Ramadorai (2023), *RFS* 36(8), 3071-3121: a recent test of selected versus non-selected candidates.
- Barr & Diamond (2020), *Refining the choice architecture in the Swedish Premium Pension*, response to SOU 2019:44 (MIT PDF): the screening-versus-picking hypothesis.

**Swedish and PPM:**
- Engström & Westerberg (2004), SSE/EFI WP 555: the first PPM flow paper (about 2000-2002).
- Hagen, Malisa & Post (2023), *Review of Behavioral Finance* 15(5), 694-708: PPM inertia during COVID, using the same Pensionsmyndigheten data.
- Bjerksund, Døskeland, Sjuve & Ørpetveit (2026), *MS* 72(5), 4341-4358: a Scandinavian authority intervening in fund quality.
- Finansinspektionen (28 Nov 2025), *Avgifter och distribution på den svenska fondmarknaden* (FI dnr 25-35134):
  - PPM equity-fund fees are about 0.2%, against about 1.0% outside PPM;
  - PPM holds 36% of Swedish households' fund holdings;
  - no fee spillover to funds outside PPM.

**Institutional chain:**
- Finansdepartementet promemoria (Dec 2017);
- Dir. 2018:57;
- SOU 2019:44, "Ett bättre premiepensionssystem";
- Prop. 2021/22:179;
- Lag (2022:759) om Fondtorgsnämnden and Lag (2022:760) om upphandling av fonder till premiepensionens fondtorg;
- RiR 2018:32;
- the 2026 Riksrevisionen audit;
- FTN's results as reported by European Pensions (18 Mar 2026).

**Background only, if space allows:**
- Begenau & Siriwardane (2024), *JF* 79(2), 1199-1247: the same fund charges buyers different fees depending on their bargaining power;
- Reuter & Zitzewitz (2021), *RoF* 25(5), 1395-1432: size and performance;
- Greenwood & Sammon (2025), *JF* 80(2), 657-698: pre-announced demand is anticipated, which supports dropping the price-pressure design;
- Sabbatucci, Tamoni & Xiao, SSRN 4322784 (the examiner's paper; unpublished).

The agents' full reports (search logs and per-paper rubric scores) were returned in the 6 October session. This file is their consolidated outcome.
