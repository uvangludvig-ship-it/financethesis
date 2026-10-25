# The thesis in plain words

**Working title:** Pre-announced, uninformed, and large: the price of moving the premium pension

Planning document, 25 October 2026. It replaces `Thesis_in_plain_words.docx` (12 Oct). It says what the thesis is, what each section must contain, which papers go where and what we take from each, how every table is built, what we expect to find, and who does what. No result exists yet. Where a number about our own results appears, it is what we expect, not what we found. All thesis text is written by the two of us; this document is a map, not a draft.

Companions: `01_DESIGN.md` (the pre-analysis plan with equations), `thesis2_method.tex` (the same with the data table and the honest assessment), `outline/thesis2_outline.md` (page budget, what each prize winner did per section, the trap per section), `literature/literature_verified.md` (66 papers with verification flags and magnitudes), `../PLAN.md` and `../STEPS.md` (division of labour, gates, dates).

---

## 1. The thesis in one paragraph

Since 2024 a new agency, Fondtorgsnämnden (FTN), decides by procurement which funds stay on the premium-pension platform. When a fund loses, Pensionsmyndigheten takes the savers' money out of it and puts it into a winner. Savers rarely act (about 94 per cent of the money moves by default), so the move is mechanical. The agency often owns 20 to 44 per cent of a losing fund and redeems it in one to three chunks (tranches) of 5 to 11 per cent of the fund, spread over two or three weeks. The fund must sell stocks to pay. So on dates known months in advance, for reasons that have nothing to do with the companies, specific Swedish stocks get sold in amounts that can reach tens of per cent of a normal day's trading. We ask three things: do those stocks fall on the selling days and bounce back after; does part of the move happen before the selling days (because traders see it coming); and who loses, the savers who are moved or the investors who stay in the losing fund. Then we put a SEK figure on the cost of a round and set it against what the round saves in fees (the agency's figure is SEK 178m a year platform-wide; cite the source when writing). The replication part does the same kind of measurement on a flow the market has had years to learn, OMXSB index reconstitutions, following Greenwood and Sammon (2025).

**One sentence for the abstract, to be filled with numbers:** on FTN tranche days, stocks fall by X basis points per unit of forced sale over daily volume and recover Y per cent of it within 20 days; the index effect on OMXSB is Z; funds without swing pricing lose W basis points on tranche days and funds with it do not; a round's price cost equals N months of its fee saving.

---

## 2. Why these flows are special, and what is new

Three properties make the FTN flow a clean experiment, and we must convince the reader of each in section 2 of the thesis:

1. **Uninformed.** FTN picks funds on fees, quality and sustainability. Nothing in the award depends on the stocks the funds hold. So the selling carries no news about the companies.
2. **Pre-announced.** The award is public months before the money moves, and the saver letter gives a second public date. Anyone can see the sale coming.
3. **Large.** The redeemed share of a losing fund is 20 to 44 per cent, and the dose per stock (forced sale divided by average daily volume) reaches tens of per cent in small caps.

What is new: nobody has measured FTN's executions. The data exist (FTN reports, Pensionsmyndigheten monthly files, Morningstar daily fund data through SHoF, FI quarterly holdings, Datastream prices). And the flow has three dated steps, award, letter, tranche, which lets us separate "the market positions early" from "the market absorbs on the day". No index reconstitution offers that, and no reconstitution has a fund-level side (who paid) at all.

What the thesis does not do: it does not judge whether FTN picks good funds. That needs years of returns after the awards. It stays out.

---

## 3. The anchor paper and how we copy it

**Greenwood and Sammon (2025), "The Disappearing Index Effect", Journal of Finance 80(2), 657-698.**

What they ask: why did the S&P 500 index effect vanish while index assets exploded? What they do: an event study of every S&P 500 addition and deletion 1980-2020, with three windows (announcement, effective day, and announcement to effective), by decade. Their numbers (NBER WP 30748, Table 2; the JF abstract revises them slightly, check against the published table): additions earned 3.4 per cent in the 1980s, 7.6 in the 1990s, 5.2 in the 2000s and 0.8 in the 2010s over the full window; deletions lost 4.6, 16.6, 12.3 and 0.6. The 2010s numbers are indistinguishable from zero. They test five explanations and conclude that two carry most of it: index migrations (stocks moving up from the MidCap, where passive money already held them) and a general rise in the market's capacity to supply liquidity on the day (other institutions now sell to the trackers). Increased predictability of additions "cannot be ruled out".

What we copy exactly, and say so in the text: the three windows; market-adjusted returns as the main measure (no factor model; the four-factor version is a robustness row); a table with additions and deletions in rows and sub-periods in columns, with N per cell; a regression of the announcement-to-effective return on expected tracker demand scaled by ADV; and a figure of tracker assets against the yearly effect ("the disappearing picture"). Our version: OMXSB, the Nasdaq Stockholm benchmark index of about 100 stocks, reviewed twice a year, 394 events over 27 reviews from June 2013 to June 2026 (222 additions, 172 deletions; 325 read from Nasdaq's own releases, 69 from newswires). Tracker assets grew from about SEK 15bn to 120bn inside the sample, and the announcement lead fell from 14-17 trading days to 6 from November 2023. Sub-periods: 2013-17, 2018-20, 2021-23, 2024-26.

What the replication can show: whether a small market with rising tracker demand shows the same disappearance. Either answer is a finding. If the Swedish effect did not disappear, we say which of their explanations does not apply here, using only what Table 2 shows.

Why it is the right anchor for an FTN thesis: their open question is whether the effect died because markets got liquid in general or because arbitrageurs learned this one flow. FTN is the same kind of flow, in the same market and years, that nobody has learned yet. If the index effect is gone (Table 2) but the FTN effect is there (Table 3), general liquidity cannot be the whole story. That contrast is the sentence that goes in the abstract and the conclusion.

---

## 4. The literature: what we read, what we take, how we differ

### 4.1 How to do the literature work (Ludvig, weeks 1 to 2)

1. Read the anchor in full, twice: once for the story, once with a pen for the exact windows, filters, table layout and the numbers we will print beside ours.
2. For each paper we will cite (target 25 to 30 of the 66 in `literature_verified.md`), write a card of four lines in `literature/cards.md`: the question; the data and identification; the one magnitude we may quote; the sentence saying how we use it or how we differ. If the card has no fourth line, the paper is not cited.
3. Verify every bibliographic record against the publisher's page before it enters `references.bib`. Entries flagged [M] in `literature_verified.md` (Almgren et al. 2005, Frazzini-Israel-Moskowitz 2018, Coval-Stafford DOI, Christoffersen et al.) are not cited until checked; a magnitude recalled from memory is never printed.
4. The related-literature text is one run-in paragraph under one page at the end of the introduction, three strands, two or three papers each, and for each strand one sentence "we differ in that ...". The course slides say it is not a review of the literature, and no prize winner exceeded a page.
5. If we borrow a table layout or the exposure measure from an SSE winner (the 2020 leveraged-ETF thesis for volatility scaling and date clustering, the 2021 invariance thesis for the Kyle-Obizhaeva form), cite it; the course treats uncited borrowing of table formats as plagiarism.
6. Every quoted magnitude in the thesis carries the table or page it came from, so the number audit in week 5 can trace it.

### 4.2 Strand A: the index effect and its decline (anchor strand)

- **Shleifer (1986, JF)** and **Harris and Gurel (1986, JF)**: the first S&P 500 inclusion studies. Both find about +3 per cent at inclusion; Shleifer reads it as a permanent shift (demand curves slope down), Harris and Gurel as temporary pressure that reverses in about two weeks. We cite them for the two readings our Table 3 will choose between. Magnitudes are [M]; check before quoting.
- **Kaul, Mehrotra and Morck (2000, JF)**: the 1996 TSE 300 float redefinition, pre-announced, no information, no change in rights: +2.3 per cent in the event week, no reversal. The cleanest pre-announced pure demand shock in the literature, and the closest analogue to FTN's flow. One sentence in the motivation.
- **Greenwood (2005, JFE)**: the Nikkei 225 redefinition; the theory of risk-averse arbitrageurs absorbing a known flow with a price path that moves at announcement, again at execution, and then reverses. This is our equation (1). Cite for the path, do not derive it.
- **Chang, Hong and Liskovich (2015, RFS)**: Russell 1000/2000 cutoffs as a regression discontinuity; demand from index funds moves prices. Cite in the strand sentence.
- **Greenwood and Sammon (2025, JF)**: the anchor, section 3 above.
- How we differ: our flow is larger relative to holdings than any reconstitution, has three dated steps, and has a fund-level incidence side. And it is new, so the learning that killed the US index effect has not happened.

### 4.3 Strand B: price pressure from fund flows (method strand)

- **Coval and Stafford (2007, JFE)**: funds with extreme outflows sell their holdings; commonly held stocks drop and recover over 12-18 months; because flows are predictable, front-running is possible. Cite for the pressure-and-reversal template and for the front-running idea behind H3.
- **Lou (2012, RFS)**: flow-induced trading built as fund flow times portfolio weight, aggregated to the stock. Our dose (equation 3) is this construction with the agency's redemption as the flow. Cite as the template.
- **Wardlaw (2020, JF)**: the standard flow-pressure measure is mechanically tied to the stock's own return in the flow quarter; once removed, the effect shrinks. We avoid the critique by construction: holdings from the last report before the letter, prices from before the event, and a flow fixed by the award rather than by returns. Say so in one sentence in the method section.
- **Da, Larrain, Sialm and Tessada (2018, RFS)**: Chilean pension savers following an adviser's switch recommendations moved USD 1-5bn at a time, 10-20 per cent of fund assets, forcing managers to trade about 10 per cent of their equity book within days in a market with about USD 205m of daily turnover. Price pressure of about 1.06 per cent on day 1, 1.22 by day 3, fully reversed within 15 days (NBER WP tables 5-7; check table numbers against the RFS version). This is the closest published analogue: coordinated, uninformed, huge relative to volume, small market. Our Table 3 and Figure 3 follow its event-day CAR, reversal and cross-section. Difference: their flow was advice-driven and noisy in timing; ours is executed by a state agency on administrative dates.
- **Hartzmark and Solomon (2025, AER)**: predictable dividend cash flows move the whole market; price multiplier about 1.9. Cite for "a pre-announced flow moves prices even at market level" and as a benchmark multiplier.
- **Sabbatucci, Tamoni and Xiao (2023, SSRN 4322784)**: the examiner's own working paper: shifts of 401(k) plan assets from active to passive funds move stock prices through fund holdings. Cite in the motivation; the exact claims must be read from the current version before anything is quoted.
- How we differ: a flow executed by an agency on dated tranches, a dose built from administrative facts, and a measured split between anticipation and execution.

### 4.4 Strand C: theory, kept to four ideas

- **Duffie (2010, JF presidential address)**: slow-moving capital. Prices concede to a known flow and recover as capital arrives. Equation (1), with Greenwood (2005).
- **Brunnermeier and Pedersen (2005, JF)**: predatory trading. Traders who know a forced sale is coming sell first and buy back after, so the price overshoots on the day and the recovery exceeds the day's move. This is the competing story in H3.
- **Grossman and Miller (1988, JF)** and **Admati and Pfleiderer (1991, RFS)**: liquidity provision and sunshine trading. A pre-announced uninformed trade attracts liquidity, so the day's move is smaller than an unannounced one. Third story in H3, one sentence.
- **Wurgler and Zhuravskaya (2002, J. Business)**: the drop is larger for stocks without close substitutes. Gives one cross-sectional prediction: the dose effect should rise with idiosyncratic volatility. Use it in Table 7 or in the Table 3 controls, not as a hypothesis.
- Koijen and Yogo (2019) and Gabaix and Koijen (2021) on inelastic markets: one sentence of motivation if space allows, otherwise out.
- Rule from the winners: one equation per idea, intuition in plain sentences, derivation cited. Eight numbered equations in the whole thesis, no more.

### 4.5 Strand D: how big should the drop be (the square-root law)

- **Kyle and Obizhaeva (2016, Econometrica)**, **Toth et al. (2011, Phys. Rev. X)**, **Bouchaud et al. (2018, CUP textbook)**: the expected impact of a large order is Y times daily volatility times the square root of (order size over daily volume), with Y around 0.5 to 1. This is equation (2) and the source of our pre-committed Y = 0.7. It gives a predicted drop for every stock and tranche day before we look at a single price.
- **Zarinelli et al. (2015)**: for very large orders impact flattens below the square root. Our biggest doses sit there, so we report the square-root prediction as an upper bound.
- **Almgren and Chriss (2001, J. Risk)**: optimal liquidation trades off expected cost against variance; selling in tranches lowers temporary impact. This is the theory behind the agency's own "we stagger large funds so that sales do not move prices", and the frame for the policy sentence in the conclusion.
- Almgren et al. (2005) and Frazzini et al. (2018) are [M]: cite only after the records are checked.
- How we use it: the coefficient beta in Table 3 is the realised drop divided by the square-root prediction. Beta near 1 means the market treated the state's sale like any other big order; near 0 means it absorbed it at no price cost; above 1 means something extra (predation). Beta not equal to 1 is a finding, not a failure, provided the minimum detectable effect is stated.

### 4.6 Strand E: who pays (incidence)

- **Edelen (1999, JFE)**: flow-driven trading costs the fund about 1.5-2 per cent of assets a year [M], paid by all holders. The baseline "stayers pay" statement.
- **Greene and Hodges (2002, JFE)**: the NAV-dilution accounting. Our equation (6) is this accounting on one day.
- **Chen, Goldstein and Jiang (2010, JFE)**: in illiquid funds redemptions hurt stayers more, which creates a first-mover advantage. Why swing pricing exists.
- **Jin, Kacperczyk, Kahraman and Suntheim (2022, RFS)**: UK bond funds; swing pricing's dilution adjustment averages about 33 bp (full swing) and offsets stress outflows almost one for one. Our Table 5 contrast (funds with and without swing pricing on the same tranche days) is their design on Swedish equity funds. Difference: our redemption is executed by the state, so the first-mover game is between the agency and the stayers.
- **Capponi, Glasserman and Weber (2020, Management Science)** and **Lewrick and Schanz (2017, BIS WP)**: what a swing factor must look like for a 20-44 per cent redemption; evidence that swing funds' returns hold up in stress. One sentence each.
- **Dahlquist, Martinez and Söderlind (2017, RFS)**: PPM daily data; fund-level flow impact on fund returns. The one Swedish paper that measured flows hitting fund NAVs. Cite in the method for Table 5 and in the Swedish strand.
- How we differ: a dated, state-executed redemption of a known share, in funds where swing pricing was legal only from July 2023, which gives a before-and-after inside the same country (the 2019 purge had no swing pricing by law).

### 4.7 Strand F: the statistics we lean on

- **Boehmer, Musumeci and Poulsen (1991)** for the standardised event test; **Kolari and Pynnönen (2010, RFS)** for the correction when many stocks react on the same day (our case: 200 stock-events share a handful of tranche days); **Petersen (2009, RFS)** for clustering by date; **Young (2019, QJE)** for randomisation inference with few clusters; **Kothari and Warner (2007)** and **MacKinlay (1997)** as the event-study references. One sentence in the method section and one line in each caption. No paragraph explaining OLS.

### 4.8 Strand G: the Swedish premium pension (context, short)

- **Cronqvist and Thaler (2004, AER P&P)** and **Cronqvist, Thaler and Yu (2018, AEA P&P)**: the 2000 launch and the inertia since; the menu, not the saver, decides where money sits. This is why only the state can move these positions and why the move is uninformed.
- **Dahlquist and Martinez (2015, EFM)**: PPM money is less responsive to performance than retail money in the same funds (2000-2008). Context for "savers do not react".
- **Kinnerud and Lorentzon (2026, AEJ: Applied)**: letters do not move most savers even when search costs are removed. The state's rationale for procuring the menu.
- **Sialm, Starks and Zhang (2015, JF)**, **Pool, Sialm and Stefanescu (2016, JF)**, **Keim and Mitchell (2018, JPEF)**: sponsors' menu changes, not participants, drive large flows; menu removals are not information about the stocks; what happens to money when a menu is cut. Two sentences in the institutional section.
- Institutional sources (not papers): SOU 2019:44, prop. 2021/22:179, lag (2022:759) and (2022:760), FTN's procurement reports and award decisions, Pensionsmyndigheten's avslutsprocess document and fee-saving figure, FI (2025) on fees, RiR 2018:32, the Riksrevisionen audit opened June 2026 (check in November). Every date in the thesis has one of these as its source.

### 4.9 The three strands of the related-literature paragraph

(i) Index effect and its decline: Shleifer; Harris and Gurel; Chang, Hong and Liskovich; Greenwood and Sammon. We differ: a new, larger, three-step flow in the same market. (ii) Flow-induced pressure and slow capital: Coval and Stafford; Lou; Da et al.; Greenwood; Duffie; Brunnermeier and Pedersen. We differ: administrative dates and a dose built before any price is seen. (iii) The premium pension and who pays: Cronqvist and Thaler; Dahlquist, Martinez and Söderlind; Jin et al. We differ: the first measurement of the reform's executions and of their incidence.

---

## 5. Section by section: what to write, who writes it

Page budget 33 of 40, everything after the title page counts. Owner in brackets. Each section's trap is from the outline; read it before writing the section.

**0. Title and abstract (1 page) [L, last].** Title plus a subtitle naming the two settings. Abstract of at most 180 words with five numbers: the OMXSB effect by sub-period, the FTN pressure coefficient and reversal, the incidence result, the cost against the fee saving. Trap: an abstract that says what we did instead of what we found.

**1. Introduction (3 pages) plus related literature (under 1 page) [L, week 3].** Paragraph by paragraph: the fact with numbers (money moved, largest redemption as share of fund and as days of volume in the most exposed stock); the anchor and the replication in two sentences with our number; why the extension is not "the same thing in Sweden" (larger, three steps, fund side); the results in numbers; what we do not claim (causality for anticipation, welfare, scaling to larger rounds); three numbered contributions and a roadmap. Trap: a literature review, and modesty about the FTN part, which is the contribution.

**2. Institutional background (2.5 pages) [L, week 1].** 2.1 OMXSB: review cycle, notice, effective date, which funds track it and their assets over time, what a tracker must do on the day. 2.2 FTN step by step with a date source for each step: procurement notice, bids, award (with standstill and appeals, note the frozen global active round, Förvaltningsrätten 4909-26), fund agreements, saver letter and deadline, what happens to non-choosers, execution in tranches, fee savings. 2.3 Why the flow is uninformed, pre-announced and large, one paragraph each. Figure 1: one round's timeline with one losing fund's capital dropping on its tranche days. Appendix Table A1: every round. Trap: a history of the premium pension since 2000; vagueness about where the money went (without the destination the net dose is wrong by construction).

**3. Theory and hypotheses (3 pages) [L, week 2; equations from 01_DESIGN.md].** Equation (1), the price path under slow-moving capital, with the predatory and sunshine stories in one paragraph each; equation (2), the square-root benchmark; the four hypotheses as numbered blocks, each with sign, test and table. Figure 3 panel A is the schematic path. Trap: deriving Greenwood or Duffie; a hypothesis that needs two tables.

**4. Data (3 pages) [L writes, A supplies every count].** Source by source with N and period: OMXSB events; FTN rounds and losers; PPM monthly capital; tranche days from daily fund units; FI holdings; swing-pricing status; prices and volume from Datastream. 4.3 defines the dose, equation (3): minus the sum over losers of redeemed share times fund assets times portfolio weight, plus the money arriving in winners times their weights, divided by the stock's average daily volume. Table 1: panel A rounds, panel B the dose distribution (mean, median, p90, max, share above 0.1 days of ADV, top ten stock-events), panel C stock characteristics by dose tercile. Figure 2: tracker assets against the yearly OMXSB effect, and the dose distribution. Trap: stale holdings (use the report before the letter and the one after execution, and treat the difference as H3 evidence); overlap of an OMXSB review within 30 days of a tranche (flag, exclude in robustness).

**5. Methodology (2.5 pages) [L writes, A checks every line against the code].** Equation (4), the replication regression; equation (5), the FTN regression with returns scaled by the stock's own volatility so the coefficient reads in volatility units per day of ADV, converted to basis points for the median stock in every paragraph; equation (6), the fund-level incidence regression; the inference paragraph (cluster by tranche day, wild cluster bootstrap, Kolari-Pynnönen, randomisation within round); equation (7), the minimum detectable effect, printed next to the square-root prediction for the median and p90 dose; equation (8), the cost arithmetic. Trap: choosing a window after seeing data; clustering by stock when 200 stock-events share five dates.

**6. Results (9 pages) [A runs and writes the one sentence per table; L writes the prose].** 6.1 Table 2 and Figure 2, the replication, compared with the anchor's decade numbers sentence by sentence (2 pages). 6.2 Table 3 and Figure 3, pressure and reversal: coefficient to basis points for the median and p90 stock-event, fraction reversed by day 20 and 60, beta against the square-root prediction, and the index-effect magnitude at equal dose (3.5 pages). 6.3 Table 4, the share of the total move in each window (award, anticipation, execution, reversal), plus the holdings change between the pre-letter and post-execution reports as direct evidence of early selling (1.5 pages). 6.4 Table 5 and Figure 4, who paid, in basis points of the fund and SEK per remaining saver (2 pages). 6.5 Table 6, cost per round against the fee saving, and one paragraph on what the comparison means (a transfer to liquidity providers is a cost to savers, not a deadweight loss; the fee saving recurs, the cost does not) (1.5 pages). Trap: reading t-statistics instead of magnitudes; burying a replication that disagrees with the anchor.

**7. Robustness (1.5 pages) [A].** Table 7, one row per named threat: placebo tranche dates (shifted a quarter, and random); exclude stock-events within 30 days of an OMXSB review; dose from the pre-letter versus the post-execution report; ADV window 20, 60, 120 days and market-adjusted versus four-factor; drop the largest round, drop the largest stock-event, winsorise. Everything else in one sentence pointing to Appendix A3. Trap: a laundry list.

**8. Conclusion (1.5 pages) [L, last, with `research/reference/conclusions_winners_vs_nonwinners.md` open].** Paragraph 1: the three numbers and the cost. Paragraph 2: what it says about pre-announced uninformed flows in a small market, against the anchor. Paragraph 3: the limits before the examiner lists them (anticipation cannot be pinned on a trader type; the concession is partly a transfer; few tranche dates make clustered inference the binding constraint; may not scale to larger rounds). Paragraph 4, only if the stock result is null: the minimum detectable effect and what the data rule out, then what the fund-level evidence still shows. Paragraph 5: two next steps (intraday data; the next rounds as an out-of-sample test). Trap: policy over-reach. Keep the recommendation to execution mechanics (staggering, in-kind transfer, swing pricing), where the evidence bears.

**Appendix (3 pages).** A1 procurement calendar with a source per date (a contribution on its own); A2 variable definitions; A3 the remaining checks; A4 the AI disclosure from `AI_LOG.md`.

---

## 6. The tables and figures: how each is built

| Exhibit | What it shows | Inputs | Script | Expect |
|---|---|---|---|---|
| Table 1 | Rounds, money moved, dose distribution, stock characteristics by dose tercile | FTN reports, PPM panel, FI holdings, prices | `pressure.py`, a small table script | Descriptive |
| Table 2 | OMXSB additions and deletions: abnormal return by window and sub-period; regression on demand over ADV | `omxsb_changes_2013_2026.csv`, prices, tracker AUM by year | `replication_omxsb.py` | Small, weaker in recent years; a volume spike on the effective day |
| Figure 2 | Tracker assets against the yearly effect; dose distribution | same | same | The "disappearing picture", Swedish version |
| Table 3 | Abnormal return on tranche days against the dose; reversal windows; gross and net dose | dose file, prices, tranche days | `ftn_eventstudy.py` (gated) | Little in large caps (tiny doses); a clear drop and recovery in small caps |
| Figure 3 | Panel A schematic path; panel B average CAR from award to exec+60, top versus bottom dose tercile, 90 per cent bands | same | same | A dip at the tranche, recovery after |
| Table 4 | Share of the total move in each window; holdings change pre-letter to post-execution | same plus two FI reports | same | Little at award; some early selling by the managers |
| Table 5 | Fund NAV minus benchmark on tranche days, with and without swing pricing | Reinvestments (NAV), fund master (benchmark), swing status, redeemed share | `dilution.py` (gated) | Funds without swing pricing lose a few bp per tranche day; funds with it do not. Worked example: SEB Sverige Expanderad (swing) sold 15 and 19 Jan 2026, same weeks as Öhman, Lannebo and Prior & Nilsson (no swing) |
| Figure 4 | Scatter of the tranche-day NAV excess return against r/(1 - r), marker by swing status | same | same | Two clouds |
| Table 6 | Per round: money moved, predicted cost (Y = 0.5 and 1), realised cost with bands, split stayers/movers, break-even months of fee saving | Tables 3 and 5 | small script | A number the policy debate lacks |
| Table 7 | Robustness rows for the Table 3 and Table 5 coefficients | all | the two gated scripts with flags | Nothing on placebo dates |
| Figure 1 | Timeline of one round with one losing fund's capital | `exit_days`, FTN dates | small script | Illustration |

Every table is written by its script as a `.tex` fragment into `output/tables/` and `\input` into the text. Nobody types a number.

---

## 7. The data, item by item

| What | Source | Status 25 Oct | Who |
|---|---|---|---|
| 394 OMXSB events 2013-2026, 48 OMXS30 events 2005-2026 | Nasdaq releases, newswires | Done, verified against prices | A |
| FTN rounds, dates, winners, losers, bids, fees | 11 FTN reports | Done (`data/derived/ftn_2026-10-11/`) | A |
| PPM capital, savers, net trade, fees per fund-month 2018-2026 | Pensionsmyndigheten monthly files | Done (`data/panel/`) | A |
| Tranche days and redeemed share per losing fund | Morningstar daily units via SHoF | Done for about 30 of the 78 losing-fund entries to 30 Sep; the method note counts 73 funds, reconcile the two counts; refresh to 31 Oct in week 2 | A, L requests the refresh |
| Sale orders for the largest Swedish losers (Avanza Zero, Storebrand Sverige, LF Sverige Vision, Handelsbanken Sverige, Nordea Swedish Stars and others with month-end-only data) | Pensionsmyndigheten, offentlighetsprincipen | Request not sent | L |
| Holdings of each losing fund | FI quarterly holdings | 4 of 12 quarters; 13 zips to download (links in `03_DATA.md` B) | A |
| Swing-pricing status and adoption date | Fund rules, annual reports | 11 yes, 38 no, 29 unknown (mostly Luxembourg) | L fills gaps if time |
| Daily price, total return, volume | Datastream pull of 15 Oct, wide, names only | On disk, not yet in the code's format; MV, NOSH, indices and a code row to pull (`data/prices/README.md`) | A |
| Swedish factors | SHoF Fama-French page | Not pulled; robustness only | A |
| Fund NAV and benchmark | Morningstar reinvested prices, fund master | Done; opened only after unblinding | A |

Holdings gap to state in the text: only Swedish-domiciled funds report to FI; nine foreign-domiciled losers need semi-annual reports or Morningstar holdings through SHoF; until then they are out of the dose, which biases the dose down, not up.

---

## 8. The method in plain words

**Abnormal return.** The stock's return minus the market's (OMXSPI or OMXSGI) that day, as the anchor does. A four-factor version with Swedish factors is a robustness row.

**The dose.** For each stock and tranche day: how much the losing funds had to sell in that stock (redeemed share times fund assets times the fund's weight in the stock) minus what the winners bought (spread over the month's trading days), divided by the stock's average daily volume. A dose of 0.5 means the forced net sale equals half a normal day's trading. Built from holdings before the letter and prices before the event, so it is fixed before anything happens (the Wardlaw point).

**The main regression.** Abnormal return on the tranche day, scaled by the stock's own volatility, against the dose. The coefficient is read in two ways: in basis points for the median and the p90 stock-event, and as beta, the realised move divided by the square-root prediction. Then the same for the reversal windows (day 2 to 20 and 21 to 60), and for the award and anticipation windows (Table 4).

**Who paid.** On a tranche day the fund's NAV return minus its benchmark, against r/(1 - r) where r is the redeemed share, separately for funds with and without swing pricing. The coefficient for funds without is the realised dilution rate; it should match the stock-level cost applied to the fund's sold portfolio.

**Inference.** The shock is by date, so we cluster by tranche day, not by stock. With few dates we also report wild-cluster bootstrap p-values and a randomisation test that reshuffles doses within a round and asks how often an equally strong result appears. The Kolari-Pynnönen correction handles many stocks reacting on the same day. Stated once in the text and once in each caption.

**Power.** Before any FTN result, the minimum detectable effect at the 5 per cent level and 80 per cent power, from the spread of window returns among unexposed stocks and the effective number of independent observations after clustering, printed next to the square-root prediction for the median and p90 dose. If the MDE exceeds the predicted effect for the median stock, we say so and the headline test is on high-dose stock-events. No prize winner did this; the course asks for it.

**Unblinding.** `replication_omxsb.py` runs now and touches no FTN date. `ftn_eventstudy.py` and `dilution.py` stay switched off until Klug has agreed the specifications and the date is written into `03_DATA.md` section E. Anything run afterwards that is not in `01_DESIGN.md` is labelled exploratory.

---

## 9. What we expect, and how the conclusion reads in each case

1. **Most likely:** prices drop and recover in small caps; large caps show nothing visible because their doses are tiny; stayers in funds without swing pricing pay a few basis points per tranche day; the index effect on OMXSB is small and has fallen. The conclusion gives the SEK cost per round against the fee saving and recommends execution mechanics: staggering, swing pricing, in-kind transfers.
2. **Effect only in small caps, nothing else:** same conclusion with the large-cap null stated with its MDE.
3. **Nothing anywhere:** the conclusion states the MDE, what sizes of impact the data rule out, and what the fund-level and anticipation evidence still shows. The 2024 prize winner won with a null on every outcome, explained by the institution.

In all three: one sentence per claim with our number, the benchmark and the bound; "associated with", never "caused", unless the design earns it.

---

## 10. Order of work and who does what

Dates and gates: `../STEPS.md`. Division of labour and working rules: `../PLAN.md` sections 6 and 7. In one line each:

- **Alexander:** repo private and pushed; the stock panel into the code's format; Table 2; FI zips, dose, power; after sign-off Tables 3 to 7 and the figures; one script per exhibit; clean-machine run; the replication package.
- **Ludvig:** Klug (method note, sign-off meeting in the week of 2 Nov, Friday three-liners); Pensionsmyndigheten request; SHoF refresh request; literature cards and the related-literature paragraph; sections 2, 3, 4, 5 in that order, then 6 from Alexander's table sentences, then 1, 8, abstract; the AI log and appendix; references and format.
- **Both:** Friday swap (A reads text for claims without a table cell; L reads code for a choice not in the PAP); three lines in `STATUS.md` each evening.

Full draft to Klug Fri 20 Nov. Submission-ready Fri 4 Dec. Hard deadline Mon 7 Dec, 10:00.
