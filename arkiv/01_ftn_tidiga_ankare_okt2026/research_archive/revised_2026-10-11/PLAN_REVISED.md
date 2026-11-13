# PLAN_REVISED: FTN as a demand shock

**Written 11 October 2026.** Proposal for a thesis with Fondtorgsnämnden at the centre. It is built on the data in `financethesis_ny/data`, on the 5 October anchor contest in `financethesis_ny/research/_archive`, and on eight feasibility runs made on 10 and 11 October (reports in `evidence/`). Nothing in `financethesis_ny` has been changed or deleted. If the authors adopt this plan, `PLAN.md` in the old folder should be marked superseded.

Authors: Alexander Fox and Ludvig Pauli Uväng. Tutor: Michael Klug. Course BE451. Deadline Mon 7 Dec 2026, 10:00.

> Course rule: AI may not write thesis text. Everything here is design, data and numbers. The thesis prose is the authors' own.

---

## 1. The question

**When the state moves pension money between funds, what happens to the prices of the stocks those funds hold, and who pays for the move?**

Fondtorgsnämnden removes losing funds from the premium-pension platform and moves savers' capital, by default, to the winners. The savers do not react: 94 per cent of the capital in removed funds is moved by default (6 per cent of savers choose themselves), and the 2019 purge shows the same (97 per cent default, 313 funds, SEK 80 bn). The flows are therefore large, dated, and unrelated to any information about the stocks. Pensionsmyndigheten redeems 100 per cent of its units in a removed fund on a single day, and its stake is 20 to 44 per cent of the fund's NAV for the big losers. The removed fund must sell a fifth to nearly half of its portfolio that day; the winners buy with a lag. This is the cleanest flow-induced-trading shock available in any Nordic market, and it is the tutor's own field (demand curves, index inclusion, microstructure).

**Working title.** "Forced flows: stock prices and fund investors when Fondtorgsnämnden moves the premium pension"

## 2. Anchor and partners

| Paper | Role |
|---|---|
| **Lou (2012), "A Flow-Based Explanation for Return Predictability", RFS 25(12), 3457-3489** | Anchor. Flow-induced trading (FIT) by mutual funds moves contemporaneous stock returns and reverses later. Replicated on Swedish data independent of FTN |
| **Wardlaw (2020), "Measuring Mutual Fund Flow Pressure as Shock to Stock Returns", JF 75(6), 3221-3243** | Recency partner and measurement rule: build the pressure measure from holdings and flows, never from prices |
| Da, Larrain, Sialm and Tessada (2018), RFS 31(10), 3720-3755 | Closest setting: mandated pension reallocations in Chile. Their Table 11 cross-section is the template for the FTN table. Already fully dossiered in the old folder |
| Pavlova and Sikorskaya (2023), "Benchmarking Intensity", RFS 36(3), 859-903 | Index-round module: the Swedish index round moved SEK 38 bn between funds tracking different indices (OMXS30 and SBX out, SIX SRI and Solactive ESG screens in) |
| Coval and Stafford (2007), JFE 86(2), 479-512; Edelen (1999), JFE 53(3), 439-466 | Fund-level exit cost: forced liquidation and the cost borne by remaining investors |
| Sialm, Starks and Zhang (2015), JF; Dahlquist and Martinez (2015), EFM | Why the flows are exogenous: pension money is sticky, the sponsor moves it. One motivating table, not the design |
| Cronqvist, Thaler and Yu (2018), AEA P&P; Dahlquist, Martinez and Söderlind (2017), RFS | PPM background; large coordinated PPM flows hurt fund NAVs |

Verify page numbers of Lou and Wardlaw against the journal PDFs before citing (the feasibility agent checked existence and journal, not pages).

## 3. Why this beats the 5 October choice (SSZ as anchor)

The judge on 5 October scored SSZ at 66/90 and the price-pressure design (Da et al.) at 53. The three reasons it lost were: no execution event had happened, one small round carried the result, and the replication was method-level only. All three have changed.

1. **Execution events exist now.** Swedish active moved SEK 15.7 bn out of 18 losers in January and February 2026 (51 and 34 per cent of award capital). Swedish index has moved in about ten monthly tranches since October 2025, including Avanza Zero (22.1 bn to 2.7 bn). Nordic active moved in June 2025. Swedish small cap is moving now (closed 18 Aug, choice deadline 25 Sep 2026). Loser redemptions are single-day, 100 per cent of PPM units.
2. **Several rounds, three dose levels.** Swedish small cap: sd of net pressure 0.56 to 0.73 pp of market cap. Swedish active: 0.25 to 0.35 pp across about 200 stocks, 10 to 18 names above 0.5 pp, sell-side execution dated. Swedish index: 0.05 to 0.09 pp, sign predictable from the index screens, which makes it a low-dose placebo. Nordic active and Global index: placebo-strength. The result no longer rests on ten micro caps.
3. **Table-level replication on independent data.** Lou's FIT table is replicated on Swedish stocks 2018 to 2025 from FI quarterly holdings and Morningstar flows, about 27,000 stock-quarters, with no FTN event in it. The FTN rounds then enter the same regression as an exogenous instrument.
4. **Topic and tutor.** FTN is the shock, not a side column. Klug's listed interests are demand curves, index investment and microstructure.
5. **The flows are the largest uninformed institutional trades ever documented in Sweden**: SEK 75 bn moved so far, 2019 purge another 80 bn. No published paper uses them.

What is weaker than SSZ: power on the stock-level test is moderate and depends on true effect sizes; the holdings panel takes two to three weeks to build; FI holdings cover Swedish-registered funds only (85 per cent of loser capital in Swedish active, 95 per cent in Swedish index).

## 4. Specification (to be frozen in the PAP before any return is opened)

### 4.1 Pressure measure
For stock i, fund f, event e:
- sell_i = sum over losers of w_fi × C_f, where w_fi is the loser's portfolio weight in the last FI quarter before the move and C_f its PPM capital at award (or at the redemption day).
- buy_i = sum over winners of w_fi × A_f, A_f the winner's actual PPM inflow in the execution window.
- **Net pressure** FIP_i,e = (buy_i − sell_i) / market cap_i, in pp, market cap ten trading days before the event.
- **Sell-side pressure** SELL_i,e = sell_i / market cap_i: the clean instrument, since the redemption day is known and mechanical while winners buy at their discretion.
Holdings from FI quarterly VPFO files (parser in `data/agentP/scripts/`), company level (A and B shares summed), Stockholm-listed stocks with a market cap. Da et al. eq. (1) and Wardlaw's holdings-based construction.

### 4.2 Replication (Lou 2012)
Stock-quarter panel of Stockholm-listed stocks 2018Q1 to 2025Q2. FIT_i,t = sum over all Swedish-registered equity funds of (shares held × fund flow / TNA) / shares outstanding, flows from Morningstar monthly TNA and returns (SSZ eq. 1), holdings from FI. Tables: FIT-decile sorted contemporaneous quarterly returns and returns over the next four quarters (reversal), and Fama-MacBeth regressions of returns on FIT with size, book-to-market and momentum controls. Print Lou's numbers alongside. No FTN event is in this sample.

### 4.3 Headline (the FTN cross-section, Da et al. Table 11 form)
CAR_i,e[0, +k] = a_e + b × FIP_i,e + controls + u, for k = 1, 3, 5, 10, 20, 60 trading days from the redemption day (sell side) or the first winner tranche (buy side). Event fixed effects, standard errors clustered by event, randomisation inference by permuting FIP within event. Separate rows for SELL_i,e. Rounds: Swedish small cap (high dose), Swedish active (medium), Swedish index (low dose, predictable sign), Nordic active (placebo). Benchmark: return minus OMXSPI, and minus a size-matched portfolio. Pre-registered reading: b at day 3 compared with Da et al.'s 3.61 (SE 1.53) and with the elasticity-implied 2.2; reversal by day 20 to 60.

### 4.4 Exit cost (fund level)
For each removed fund: daily NAV return minus category benchmark on the redemption day and days +1 to +5, when Pensionsmyndigheten redeems 100 per cent of its units (20 to 44 per cent of NAV for the large losers). N = 67 FTN losers plus the 2019 purge funds with FI holdings, plus Avanza Zero's tranches. Regress the five-day shortfall on PPM share of NAV and portfolio illiquidity. Question: is the liquidation cost borne by the remaining (non-PPM) investors, or pushed back to PPM through adjusted NAV (swing pricing)? Daily fund NAVs are already on disk (SHoF RIPS daily files).

### 4.5 Power (rough, assumptions stated; refine in the PAP with FinBas volatilities)
- Stock-level, five-day CAR, daily idiosyncratic sd 2.5 per cent small caps and 1.8 per cent large caps. Swedish small cap alone: MDE about 1.6 to 2.1 CAR per pp of FIP. Swedish active alone: about 2.7. Pooled with event fixed effects: about 1.4. Against Da et al.'s 3.6 and the elasticity-implied 2.2, power is adequate on the pooled sample and marginal round by round. Sell-side-only variants have roughly half the dispersion, so MDE doubles: label them as bounds.
- Fund-level exit cost: daily tracking sd 0.3 per cent for active Swedish funds, five-day 0.7 per cent, N = 67: MDE about 0.25 per cent over five days. A liquidation of 30 per cent of NAV at a 0.5 to 1 per cent round-trip cost implies 0.15 to 0.3. Borderline; the 2019 sample roughly doubles N.
- All numbers above are blind: no stock or fund return has been looked at around any FTN date.

### 4.6 Exhibits (five, fixed)

| Exhibit | Content |
|---|---|
| **Table 1** | Panel A: the FTN rounds (bids, winners, removals, capital, fee before and after; from `data/bids_long.csv` and `data/ftn_category_fees.csv`). Panel B: who moved the money: default versus own choice, FTN rounds and the 2019 purge side by side (`data/agentA`, `data/agent2019`). This is the exogeneity argument |
| **Table 2** | Replication of Lou (2012) on Swedish stock-quarters 2018 to 2025, Lou's coefficients alongside |
| **Table 3 (headline)** | CAR on FIP and on SELL by horizon, rounds pooled and separately, randomisation inference, reversal rows |
| **Figure 1** | Event-time cumulative abnormal returns, top versus bottom FIP tercile, days −10 to +60, Swedish small cap and Swedish active, with the index round as the flat line |
| **Table 4** | Exit cost: removed funds' abnormal NAV return around the single-day redemption, FTN and 2019 |

Secondary (one paragraph each, no new exhibit): the winners' forced inflows (doses 5 to 35 per cent of TNA, MDE ten times the plausible effect: descriptive only); fees (PPM fee falls at contract start, retail TER unchanged for every winner); bids (winners are cheaper, larger, more often incumbents and Swedish). SSZ's 2020 to 2023 flow-sensitivity test is dropped, or kept as an appendix figure if time allows.

### 4.7 Pre-committed reading
- b significantly positive at days 1 to 5 and reverting by day 60: prices are moved by uninformed government flows, as in Chile; report b relative to 3.6 and 2.2.
- b positive but not reverting: demand curves slope down permanently (Pavlova and Sikorskaya reading); say so, do not call it mispricing.
- b indistinguishable from zero with the pooled MDE of about 1.4: report the bound; Swedish large caps absorbed SEK 16 bn without measurable pressure.
- Index round: predicted signs (Saab and Evolution net sold under ESG screens; mid caps net bought) but low dose; a placebo unless the sign pattern is significant.
- Exit cost: a negative abnormal NAV return on the redemption day means remaining investors paid; zero means the fund pre-positioned or swing-priced.

## 5. Data

### 5.1 In hand (built 10 and 11 October, in `data/`)
- `ppm_panel_2018_2026.csv`: PPM fund-month panel, 104 months, capital, savers by sex, net trade, fees, ISIN, Upphandlad flag; parser `build_ppm_2018.py`.
- `bids_long.csv`: all 290 bids across 11 rounds, winners, incumbents, announce and award dates; `unmatched_for_lseg.csv` (144 bids without returns).
- `agentA/`: round membership (winners, losers, capital), default-versus-voluntary decomposition per loser.
- `agent2019/`: the 2019 purge: 313 funds, destinations (AP7 versus sibling fund), decomposition.
- `agentP/`: FI holdings parsed for 2023Q4, 2024Q1, 2024Q2, 2026Q2; per-stock net demand and FIP for Swedish active and Swedish index; index benchmarks of all index funds; execution windows by month; FI fund mapping.
- `agentDRS/`: forced-inflow doses per winner and power sketch.
- `crosswalk_ppm_shof.csv`: PPM ISIN to Morningstar fundid (99.6 per cent matched).
- SHoF Morningstar daily TNA and RIPS 2018 to 2026 (in `financethesis_ny/data`).

### 5.2 To get (all public or already licensed; see `DATA_TODO.md`)
1. FI quarterly holdings zips not on disk: 2024Q3, 2024Q4, 2025Q1, 2025Q2, 2025Q3, 2025Q4, 2026Q1 (URL pattern in `DATA_TODO.md`), plus 2018Q1 to 2023Q3 for the Lou replication (24 files). Each is one click.
2. Daily stock prices, volumes, shares outstanding and market caps for all Stockholm-listed stocks 2018 to 2026: FinBas via SHoF (preferred) or LSEG.
3. Redemption days per removed fund: read off the daily SHoF TNA series (the day fund TNA drops by the PPM stake). Cross-check with Pensionsmyndigheten letters where available.
4. Holdings for the non-Swedish-registered losers and winners (Odin Sverige, Danske SICAV Sverige, SEB 3 Sweden Equity, Evli Sverige Aktieindex, the Nordic SICAVs): LSEG or Morningstar holdings; otherwise bound the result with and without them.
5. Monthly fund flows for the replication: already derivable from SHoF TNA and returns.

### 5.3 Requests (send this week)
- Pensionsmyndigheten: redemption dates per removed fund for all FTN rounds and the 2019 purge; counts of own choice versus default per round (Table 1B).
- FTN: bid deadlines per round and per-bid qualification status (Table 1A).
- SHoF: confirm FinBas access and whether Morningstar holdings are in the licence.

## 6. Risks

| # | Risk | Mitigation |
|---|---|---|
| S1 | True price effect is smaller than Chile's and the pooled test is underpowered | Pre-registered bound reading; sell-side instrument; fund-level exit-cost test as the second powered result; 2019 sample |
| S2 | FI holdings miss foreign-registered funds (15 per cent of Swedish active loser capital; Odin Sverige alone 1.95 bn) | Bound with imputed holdings; LSEG holdings for the few large ones |
| S3 | Redemption days cannot be dated exactly | Daily SHoF TNA drops; monthly execution windows as fallback with a wider CAR window; request to Pensionsmyndigheten |
| S4 | Winners' buying is spread over months, so buy-side pressure is diluted | Treat the sell side as the instrument; the buy side is a secondary row |
| S5 | Swedish small cap executes in October and November 2026, close to the freeze | Daily stock data are available at once; set the freeze at 20 November for this round; the other rounds stand on their own |
| S6 | Building the FI holdings panel 2018 to 2026 for the replication takes time | Parser exists; 34 zips; the replication can run on 2021 to 2025 if time is short |
| S7 | Examiner reads it as "Da et al. again" | The anchor is Lou's general mechanism, replicated on independent Swedish data; FTN is the identification, with Da et al. as the setting precedent |
| S8 | Klug prefers the flow-sensitivity design he was told about | Put the choice to him this week with both designs on one page; this plan has his topic in the title and his field in the method |

## 7. Calendar (eight weeks)

| Week | Alexander (data, code, exhibits) | Ludvig (literature, institutions, text) | Gate |
|---|---|---|---|
| 12 to 18 Oct | Download FI zips; FinBas pull; parse all quarters; date redemption days from daily TNA; build FIT panel | Read Lou, Wardlaw, Da et al. (one page each); institutional section on FTN and the exit process; send the three requests | Klug's answer; PAP drafted |
| 19 to 25 Oct | Table 2 (replication); FIP for all rounds; power recomputed with FinBas volatilities | PAP written with Alexander; literature section | PAP frozen and timestamped, Fri 24 Oct |
| 26 Oct to 1 Nov | Table 3 and Figure 1 on executed rounds; Table 4 exit cost | Data section; Table 1 | Headline run |
| 2 to 8 Nov | Robustness rows; 2019 sample; index-round module | Results drafted from the tables | Full draft to Klug Mon 9 Nov |
| 9 to 15 Nov | Swedish small cap execution data in; rerun Table 3 pooled | Introduction, conclusion | |
| 16 to 22 Nov | Freeze Fri 20 Nov; replication package | Outside reader; number audit | Submission-ready Fri 27 Nov |
| 23 Nov to 7 Dec | Buffer; presentation | AI appendix; references | Submit Mon 7 Dec 10:00 |

## 8. Message to Klug (edit freely)

> Hi Michael,
>
> We have re-planned the thesis so that Fondtorgsnämnden is the identification rather than a side table, and would like your view before we freeze the pre-analysis plan.
>
> Design: FTN's removals force Pensionsmyndigheten to redeem 100% of its units in each losing fund on one day (20 to 44% of the fund's NAV for the large ones), and savers do not react (94% of capital is moved by default). We use these dated, uninformed flows as a flow-induced-trading shock to Swedish stocks, in the spirit of Lou (2012 RFS) and Wardlaw (2020 JF), with Da et al. (2018 RFS) on Chilean pension reallocations as the closest setting. Replication: Lou's FIT tables on Swedish stocks 2018 to 2025 from FI holdings and Morningstar flows, independent of FTN. Extension: the cross-section of CARs on FTN net pressure across the Swedish active, Swedish index and Swedish small-cap rounds (dose 0.07 to 0.7 pp of market cap), plus the NAV cost borne by the removed funds' remaining investors on the redemption day.
>
> Rough blind power: pooled MDE about 1.4% CAR per pp of pressure against Da et al.'s 3.6. The earlier flow-sensitivity design (SSZ 2015) becomes an appendix.
>
> Would you be comfortable with this as the main design, and does the Lou/Wardlaw replication meet the course's replication standard in your reading?
>
> Best,
> Alexander and Ludvig

## 9. Rules carried over
1. No coefficient on any FTN event is opened before the PAP is frozen and timestamped.
2. Every claim gives the estimate, the benchmark (Lou, Da et al.) and the bound in one sentence.
3. Five exhibits. Something new replaces something.
4. Raw data untouched; every transformation in code; AI log kept from today.
