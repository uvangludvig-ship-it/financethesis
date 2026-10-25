# 00. Is thesis 2 the best thesis? What the deep research found (11 to 12 Oct 2026)

The brief: assume thesis 2 (forced flows, Greenwood and Sammon anchor) and test whether it holds up, find the data, find the papers, start the code, and build the structure of a prize-level paper. This file is the verdict. The evidence is in the rest of the folder.

## The verdict in five lines

1. The design survives the blind referee's five new objections (file 08) with data, not argument: four are closed, one is reduced to a known risk with a date. Details below.
2. The replication leg is stronger than any earlier version of this plan assumed: 394 OMXSB events, 325 read from Nasdaq releases, with tracker assets growing eightfold inside the sample. That is a real test of the anchor's mechanism, not a decorative replication.
3. The execution events are visible in the data and look exactly like what a price-pressure study needs: one to three days per fund of 5 to 11 per cent of assets each, clustered in a two to three week window, and nothing like it in the year before. Dates found for about 30 of 78 losers; the rest need one email to Pensionsmyndigheten.
4. The incidence table can be built: swing-pricing status is known for 49 of 78 losers, with adoption dates, and the 2019 purge supplies 38 Swedish no-swing funds by law.
5. Two things are needed from you before anything else can run: the stock-price panel (LSEG or FinBas) and ten FI holdings files. Both are click-and-download tasks with exact instructions in `03_DATA.md`. Nothing in the design depends on data that does not exist.

## The referee's objections, re-examined with tonight's data

| objection (file 08) | what was found | status |
|---|---|---|
| Calendar: exec+40 for the small-cap round lands after 7 Dec | Humle's first tranche was 24 Sep 2026; the other small-cap losers with daily data (Carnegie, Spiltan, Lannebo x2, Skandia) show no tranche yet in data ending 30 Sep. The design pre-commits to a 20-day reversal window for that round, and the small-cap row is added last (week 5). The earlier rounds carry the 40-day window | reduced to a known risk; the SHoF data must be refreshed in November |
| Where the fund trades: a manager warned two weeks earlier sells over [letter, exec], so a 7-day window is wrong and the MDE triples | The tranche structure answers this. A fund redeemed 10 per cent on a Thursday must deliver cash within days; it cannot have sold that 10 per cent two weeks earlier without holding cash, which the FI holdings before and after will show. The event is the tranche day, the window is [-1, +1] per tranche plus the round window; the pre-tranche drift is H3, measured, not assumed away. Power is recomputed on that basis in `01_DESIGN.md` section 5.4 | closed |
| Netting: winners bought in the same months losers sold, so sell-side pressure overstates the net shock threefold | Net and sell-side doses are both reported with equal weight (equation 6). Winners' purchases are dated to the month and spread across its trading days; losers' sales are dated to the day. On a tranche day the sell leg is concentrated and the buy leg is diffuse, which is why the day-level design has power the month-level design lacked | closed by design |
| The OMXS30 replication cannot show the anchor's result: trackers hold too little, 20 to 30 events per sub-period | Confirmed for OMXS30 (42 usable events, trackers 1 to 2 per cent of cap). Replaced by OMXSB: 394 events, 5 to 15 per review, 27 of 28 reviews covered, trackers from SEK 15bn to 120bn, announcement lead changing from 15 to 6 trading days inside the sample | closed |
| Fan-out: two anchors, five tables, three figures, a cost-benefit, on the grader's own question | The outline (`outline/thesis2_outline.md`) budgets 33 pages with 7 tables and 4 figures; the cost-benefit is one table or one paragraph (to be decided with Klug); Lou and Jin et al. are method references, not second anchors. The grader's working paper is cited in the motivation, which is the right place for it | reduced |

The motivated-reasoning items in file 08 section 3 are corrected in the design: "one pre-announced day" is now "one to three tranche days per fund, read from daily units"; the appeal-round fact is used for saver inertia only; one pre-registered prediction per table; the index round is called a low-dose treated group.

## Why it is the best thesis, now with evidence rather than taste

- The object is new and the data to measure it exist. Nothing has been published on Fondtorgsnamnden or the 2019 purge (literature search, `literature/literature_verified.md`, weak evidence of absence but consistent across sources).
- Identification is institutional, not statistical. The dose per stock is the losers' old portfolio weights times the agency's stake; the dates are administrative; the flow is 94 per cent default. The 2024 prize winner won with a weaker version of this argument.
- The anchor fits like a glove. Greenwood and Sammon ask why a pre-announced uninformed flow stopped moving prices. OMXSB gives the Swedish version of their time series. FTN gives the counterfactual: the same kind of flow, not yet learned, with a dose per stock-day that reaches tens of per cent of daily volume in small caps.
- It has a theory section with closed forms (slow-moving capital path, square-root impact benchmark, dilution identity) that produces a parameter with an external benchmark ($\beta = 1$ in equation 9), which is rarer in BSc theses than another regression table.
- It has a second result that stands on its own: who paid. For index losers the power is almost noiseless (tracking error 3 to 5 bp against 20 to 30 bp of cumulated dilution).
- It fits both readers. Klug: index investing and demand curves. Sabbatucci: a working paper on retirement-plan menu shifts moving stock prices, cross-sectional event studies, tradable factor models (his RoF 2025 paper is the fallback factor model here).
- It fits the winner pattern on every dimension listed in file 02, and adds the one thing none of the 25 winners did: a written minimum detectable effect, before unblinding.

## What could still sink it, honestly

- Data arrival. If the stock panel is not on disk by 17 Oct, the Friday gate says thesis 1. The LSEG pull is a half-day job with the instructions in `03_DATA.md`.
- Execution days for the largest Swedish losers (Avanza Zero, Storebrand Sverige, LF Sverige Vision, Handelsbanken Sverige, Nordea Swedish Stars) are not in the Morningstar daily file (monthly only). One email to Pensionsmyndigheten (draft in `03_DATA.md`) or a reading of the fund companies' own daily AUM pages. Without them the index round is month-dated, which is acceptable for a low-dose group, and the Swedish active round loses three of its eighteen funds.
- The square-root law may not hold for a one-day sale by a fund that has to deliver cash; then $\beta \ne 1$ is the finding and the thesis must interpret it. That is a result, not a failure, provided the MDE is stated.
- Pensionsmyndigheten's staggering policy means the per-tranche dose is smaller than the stake; power comes from the small-cap round and from pooling. If the small-cap tranches slip to November, the thesis is written on Swedish active, Nordic active and the 2024 European round, with small cap as a last-week addition.

## Decision rule for Friday 17 Oct (unchanged from file 08, with tonight's state)

1. Stock panel on disk: not yet (your task, `03_DATA.md` section A).
2. Counted index-change list: done, 394 OMXSB plus 48 OMXS30 events, in `data/omxsb/`.
3. Execution days visible in daily data: yes for about 30 losers (`data/exit_days/exit_days_by_loser.csv`); the small-cap round's first tranche is 24 Sep 2026, inside the window that fits before the deadline.

Two of three gates are met tonight. The third is yours.
