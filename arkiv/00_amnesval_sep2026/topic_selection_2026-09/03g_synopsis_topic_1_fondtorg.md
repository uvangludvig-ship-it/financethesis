# Synopsis draft, Topic 1 (tutor-suggested, Klug): The Swedish Fund Selection Agency and the Mutual Fund Market

> **Arbetsanteckning (tas bort före inlämning).** Utkast 9 september 2026.
> Bygger på ämne K i `05_fem_alternativ.md` och red-team i
> `agent_reports/19_redteam_K.md` (fakta verifierade mot Fondtorgsnämndens
> rapporter, Pensionsmyndighetens månadsstatistik och FI:s innehavsdata
> 7 sep 2026). Handledarföreslaget ämne: får bara vara ett av de två.
> Handledarens egna referenser (Berk & Green 2004 JPE; Leippold & Rueegg
> 2020 RoF) är inlagda som mekanism-ankare. Skriv om med egna ord, läs
> ankarartiklarna i fulltext, logga AI-användning.

**Authors:** [Full name], [Full name]
**Preferred tutor, if any:** Michael Klug

---

## Topic 1: Forced Flows and Price Pressure: The Swedish Fund Selection Agency's Procurements 2024–2026

### 1. Tentative research question

*When the Swedish Fund Selection Agency (Fondtorgsnämnden) closes a
category of premium-pension funds to non-selected managers and tens of
billions of kronor are moved from de-listed funds to procured funds on an
administrative timetable, do the stocks that must be sold fall and the
stocks that must be bought rise, and do prices revert once the flow is
complete?*

Fondtorgsnämnden was created in 2022 to replace the open premium-pension
fund platform with procured categories. Each procurement designates a
handful of winners; all other funds in the category become non-selectable
and are wound down, with savers' capital moved to a procured fund unless
they choose otherwise. Between 2024 and 2026 this has produced a sequence
of large, dated, involuntary flows: Europe active (SEK 11 billion, 2024),
global index and Europe index (SEK 58 billion, 2024–2025), Nordic active
and Nordic small cap (SEK 18 billion, 2025), Sweden active (SEK 92 billion,
about 25 de-listed funds closed one per week from November 2025 to April
2026), Sweden passive (SEK 59 billion, 2025) and Sweden small cap (SEK 34
billion, 180,000 savers, nine de-listed funds from 18 August 2026).

The economic mechanism is price pressure from non-fundamental demand
(Coval and Stafford, 2007; Lou, 2012): if arbitrage capital is limited,
forced sales push prices below fundamentals and forced purchases above,
followed by reversal. The competing view, in the spirit of Berk and Green
(2004), is that fund flows respond to and reveal skill and that capital
markets absorb flows without lasting price effects; Koijen and Yogo (2019)
quantify how inelastic demand must be for flows to move prices. The
Swedish setting is unusual because the timing and size of the flow are set
by an agency, not by investors reacting to returns, which removes the main
identification problem in the flow literature (Wardlaw, 2020).

A zero result is informative: it would show that the Swedish small- and
mid-cap market absorbs tens of billions of forced trading without
measurable price impact, which speaks directly to Leippold and Rueegg's
(2020) question of how competitive and rational the fund market is, and to
whether procurement-based platform design has hidden costs for savers.

### 2. Closest literature and intended contribution

**Coval and Stafford (2007, JFE), "Asset fire sales (and purchases) in
equity markets".** Question: do mutual funds' flow-driven trades move
stock prices? Data: U.S. fund holdings and flows, 1980–2004. Method:
identify stocks heavily sold by funds in extreme outflow and bought by
funds in extreme inflow; event-time abnormal returns and reversal. Result:
pressure stocks fall (rise) and revert over the following quarters. *We
replicate* the pressure measure and event-time return design. *We extend*
by using flows whose timing and size are administratively determined, so
that pressure is not confounded with the information in investor
redemptions.

**Lou (2012, RFS), "A flow-based explanation for return predictability".**
Question: can expected flow-induced trading predict returns? Data: U.S.
holdings and flows. Method: flow-induced trading measure at the stock
level, scaled by shares outstanding; predictive regressions and reversal.
Result: predicted flow trading forecasts returns and subsequent
reversal. *We replicate* the stock-level flow-induced trading measure,
computed as de-listed funds' holdings times capital to be moved, net of
the procured winners' expected purchases, scaled by average daily volume.
*We extend* to a setting where the winners' portfolios are known in
advance, so net rather than gross demand can be measured.

**Dahlquist, Martinez and Söderlind (2017, RFS), "Individual investor
activity and performance".** Question: how do Swedish premium-pension
savers choose and switch funds? Data: the full premium-pension register.
Method: performance and activity of individual savers. Result: most
savers are passive; active savers earn higher returns. *We use* their
description of saver inertia to justify that capital in de-listed funds
is moved mechanically rather than reallocated by savers, which is what
makes the flow exogenous to stock fundamentals.

**Berk and Green (2004, JPE)** provide the rational benchmark in which flows
chase skill and returns do not persist; **Leippold and Rueegg (2020,
Review of Finance)** test competition and rationality in the fund market;
**Koijen and Yogo (2019, JPE)** give the demand-system framework for
translating flows into price effects; **Wardlaw (2020, JF)** shows how
mechanical flow measures can be contaminated by returns and dictates our
measure; **Greenwood and Sammon (2025, JF)** document that the index
inclusion effect has disappeared, which frames whether forced demand still
moves prices today. The 2015 Per Hiller thesis on fund-flow risk is the
closest prior student work.

> Relative to Coval and Stafford (2007) and Lou (2012), we replicate the
> flow-induced price pressure design on stocks held by de-listed
> premium-pension funds and extend it by exploiting that Fondtorgsnämnden
> fixes both the size and the weekly timing of the flow, allowing us to
> test whether forced, pre-announced demand moves Swedish stock prices
> and how quickly prices revert.

### 3. Data and feasibility

- **Fund holdings:** Finansinspektionen's quarterly "Fondinnehav" files,
  2018Q4–2026Q2, public XML, fund × ISIN × market value (Swedish-domiciled
  funds only; 2026Q2 published 20 August 2026). Morningstar via the Swedish
  House of Finance for daily NAV, total net assets and flows per share
  class, used to reconstruct the weekly closure tranches.
- **Premium-pension flows:** Pensionsmyndigheten's monthly fund statistics
  (market value and net trading per fund), the fund list with closure
  dates and status, and Fondtorgsnämnden's award decisions (bidders,
  winners, capital per category, closure schedule).
- **Stock data:** FinBas or LSEG via SHoF for daily prices, volume, bid
  and ask for Nasdaq Stockholm and First North; index membership for
  controls.
- **Unit of observation:** stock × closure tranche (event) and stock ×
  day. **Geography:** Sweden. **Period:** 2024–2026, main sample the
  completed Sweden active wave (November 2025–April 2026); the Sweden small
  cap wave (from August 2026) as an out-of-sample test.
- **Outcomes:** cumulative abnormal returns around tranche dates, reversal
  over 1–3 months, abnormal volume and bid-ask spreads.
- **Treatment:** net flow-induced demand per stock = (de-listed funds'
  holdings × capital moved) − (new winners' holdings weights × capital
  received), scaled by average daily volume; gross demand for volume and
  spread tests.
- **Controls:** size, book-to-market, momentum, liquidity; stocks with
  similar characteristics not held by premium-pension funds.
- **Expected sample:** about 25 de-listed funds and 10 winners in the
  Sweden active wave, several hundred stocks, weekly tranches over six
  months, giving several hundred fund–stock–tranche observations;
  pooled with the 2024–2025 waves for power.
- **Access verified:** FI and Pensionsmyndigheten files downloaded 7
  September 2026; a closed-fund outflow is visible in the monthly data
  (Storebrand Sverige, SEK −3.9 billion, January 2026). SHoF Morningstar
  and FinBas access to be confirmed in week 1.
- **Cleaning/merging:** ISIN mapping across FI, Morningstar and FinBas;
  foreign-domiciled winners (e.g. a Danske SICAV fund) missing from FI
  holdings, proxied from fund reports; tranche dates inferred from daily
  TNA drops.
- **Main risks and fallback:** managers trade ahead of the tranches,
  attenuating tranche-day effects (fallback: use award and de-listing
  announcement dates as events); overlap between winners' and losers'
  portfolios nets demand to zero (this is itself a finding); the small cap
  wave is ongoing and may not complete within the thesis period (main
  results rest on completed waves).

### 4. Empirical method

- **Baseline:** event study of daily abnormal returns (market and
  characteristic-adjusted) for stock *i* around tranche *t*, regressed on
  net flow-induced demand with stock and tranche fixed effects; standard
  errors clustered by stock and week.
- **Identification:** the agency decides which funds close and when, and
  savers are largely inert, so the timing and quantity of trading in a
  given stock are determined by the fund's past holdings, not by news
  about the stock. Winner selection is not random, but selection affects
  which stocks are traded, not when or how much; stocks held by both losers
  and winners provide within-event variation in net demand.
- **Key assumptions:** holdings at the last quarter-end approximate what
  is sold; arbitrageurs do not fully front-run the announced schedule.
- **Threats:** information in losers' portfolios (the reversal test is the
  main defence, following Coval and Stafford); pre-trading by managers
  (test announcement dates and the pre-period); confounding market
  events (staggered tranche timing across funds and stocks); return
  contamination of the flow measure (Wardlaw, 2020; we use quantities, not
  values).
- **Robustness and placebos:** placebo tranche dates in quarters without
  closures; stocks with zero premium-pension ownership; heterogeneity by
  liquidity and by portfolio overlap; gross versus net demand for volume
  and spreads.
- **Power:** pooled waves give hundreds of fund–stock–tranche
  observations; the Sweden active wave alone gives roughly 25 funds × 20
  weekly tranches.
- **Software and skills:** Python or R, standard event-study and panel
  regression code; parsing FI XML files.

### 5. Three-month scope

- **Minimal viable analysis:** Sweden active wave, net demand per stock,
  event-study returns around tranches and reversal.
- **Meaningful extension:** all completed waves pooled; small cap wave as
  live out-of-sample test; volume and spread effects; heterogeneity by
  overlap and liquidity.
- **First data test (week 1):** parse FI 2025Q3 holdings for the 25
  de-listed Sweden active funds, compute net demand per stock, and plot
  abnormal returns around the first three tranches in November 2025.
- **Main failure risk:** tranche dates cannot be reconstructed from
  Morningstar data.
- **Fallback:** monthly event windows from Pensionsmyndigheten's net
  trading data and announcement-date event studies, which still test the
  price-pressure hypothesis.

### References — Topic 1

Berk, J. B., and Green, R. C. (2004). Mutual fund flows and performance
in rational markets. *Journal of Political Economy*, 112(6), 1269–1295.

Coval, J., and Stafford, E. (2007). Asset fire sales (and purchases) in
equity markets. *Journal of Financial Economics*, 86(2), 479–512.

Dahlquist, M., Martinez, J. V., and Söderlind, P. (2017). Individual
investor activity and performance. *Review of Financial Studies*, 30(3),
866–899.

Greenwood, R., and Sammon, M. (2025). The disappearing index effect.
*Journal of Finance*, 80(2), 657–698.

Koijen, R. S. J., and Yogo, M. (2019). A demand system approach to asset
pricing. *Journal of Political Economy*, 127(4), 1475–1515.

Leippold, M., and Rueegg, R. (2020). How rational and competitive is the
market for mutual funds? *Review of Finance*, 24(3), 579–613.

Lou, D. (2012). A flow-based explanation for return predictability.
*Review of Financial Studies*, 25(12), 3457–3489.

Wardlaw, M. (2020). Measuring mutual fund flow pressure as shock to stock
returns. *Journal of Finance*, 75(6), 3221–3243.
