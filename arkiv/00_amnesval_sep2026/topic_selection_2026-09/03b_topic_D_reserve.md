# Reservämne D (ej i synopsisen): utdelningssäsong och klientel

Flyttat ur synopsisutkastet 6 sep 2026 efter granskning (prispotential 5/10, 7–8 om ledd av prispress). Behålls som reserv om ämne B faller på Serranos kommunvariabel.

## Topic 2: One Month, All the Dividends: Price Pressure and Clienteles in Sweden's Compressed Dividend Season

*(Revised after adversarial review: the price-pressure test leads, the tax-clientele test is a secondary chapter with a pre-stated informative null.)*

### 1. Tentative research question

*When almost all of a market's dividends go ex within a few weeks, does
dividend-seeking demand generate a larger dividend month premium than in
the US, or does the simultaneous supply of dividend-paying stocks absorb
it? And does the premium respond to monetary policy and to the tax status
of the marginal investor?*

Hartzmark and Solomon (2013) show that US stocks earn about 40 basis
points of abnormal return in months when a dividend is expected, driven by
price pressure from dividend-seeking investors before the ex-day and
reversal afterwards. US dividends are quarterly and spread across the year.
Sweden is the opposite case: most listed firms pay once a year, the annual
general meeting must be held within six months of the fiscal year-end
(Aktiebolagslagen 7:10), and ex-dates cluster in April and May with yields
per event of three to four percent. Two mechanisms make opposite
predictions. If the premium reflects concentrated, inattentive demand for
dividend income, it should be larger in Sweden and increase with the
fraction of the market going ex in the same week. If dividend-seeking
investors substitute across payers, crowding should weaken the price
pressure per stock. The policy rate was negative from February 2015 to
December 2019, the condition under which investors "reach for income"
(Daniel, Garlappi, and Xiao, 2021; Jiang and Sun, 2020), and since 2012
retail investors hold shares in ISK accounts that make dividends and
capital gains tax-neutral, with tax-free allowances of SEK 150,000 from
2025 and SEK 300,000 from 2026. The classical clientele model (Elton and
Gruber, 1970; Michaely, 1991; Graham, Michaely, and Roberts, 2003)
predicts that the ex-day price drop and ex-day trading volume in
retail-heavy stocks respond to that change. A zero effect in the clientele
test is informative: it would show that tax-neutral institutions set
Swedish ex-day prices and that any premium is attention-driven rather than
tax-driven.

### 2. Closest literature and intended contribution

**Hartzmark and Solomon (2013, JFE).** Question: do expected dividend
months carry a return premium? Data: CRSP 1927–2011. Method: predicted
dividend month from dividends 3, 6 or 12 months earlier; Fama–MacBeth and
calendar-time portfolios. Result: ≈ 40 bp per month abnormal return in
predicted dividend months, pre-ex run-up and post-ex reversal, consistent
with price pressure. *We replicate* the monthly and daily decomposition on
Swedish stocks 2000–2026. *We extend* by testing whether the premium is
weaker when many ex-days cluster (substitution) or stronger under negative
rates.

**Daniel, Garlappi, and Xiao (2021, JF)** and **Jiang and Sun (2020,
JME).** Question: does expansionary monetary policy push income-seeking
investors into dividend-paying stocks? Data: US fund flows, household
holdings and returns. Result: low rates raise demand for and prices of
high-dividend stocks ("reaching for income"). *We use* the Swedish
negative-rate period 2015–2019 as a regime split for the premium.
Hartzmark and Solomon (2019, JF) provide the behavioural foundation
(investors treat dividends as free income).

**Graham, Michaely, and Roberts (2003, JF)** and **Michaely (1991, JF).**
Ex-day price-drop ratios respond to tax reform (TRA 1986) and to
microstructure (decimalisation); tax clienteles and short-term traders
both matter. *We replicate* the price-drop-ratio design around a tax
change, here the diffusion of ISK and the 2025/2026 allowance steps, using
the pre-reform cross-section of retail ownership as treatment intensity.

**Rantapuska (2008, JFE).** Finnish investor-level data: ex-day trading is
dominated by domestic investors with a tax preference for dividends;
foreign investors sell before the ex-day. *We use* the same Nordic
institutional logic (30 percent withholding tax for foreign holders) to
predict heterogeneity by foreign ownership share.

Prior student work to cite and position against: Peltomäki (2019, Aalto
MSc) finds a dividend month premium in the Nordics that is larger for
illiquid stocks and smaller under high foreign ownership; Swedish ex-day
drop-ratio theses exist in numbers, none tied to a shock or to ownership
data.

> Relative to Hartzmark and Solomon (2013), we replicate the dividend
> month premium in a market where the entire dividend season is compressed
> into a few weeks, allowing us to test whether price pressure scales with
> concentrated demand or is absorbed by simultaneous supply, and, relative
> to Graham, Michaely, and Roberts (2003), whether the ex-day response of
> retail-heavy stocks changes as tax-neutral ISK accounts spread.

### 3. Data and feasibility

- **Prices and dividends:** FinBas (Swedish House of Finance), daily prices
  and corporate actions for Nasdaq Stockholm and First North; confirm the
  ex-date field at first login, otherwise LSEG Workspace (library workshop
  15 September).
- **Ownership:** Modular Finance Holdings (library workshop 11 September):
  retail, institutional, insider and foreign ownership shares per stock.
- **Rates and ISK statistics:** Riksbank policy rate; Skatteverket/SCB for
  ISK account counts and household equity held via ISK.
- **Unit:** stock-month (premium) and ex-day event (price-drop ratio).
  **Period:** 2000–2026. **Expected sample:** ≈ 300–400 dividend payers per
  year, ≈ 6,000–7,000 ex-day events.
- **Access verified?** FinBas and Holdings are course resources; ex-date
  field and Holdings history depth to be confirmed this week.
- **Risks and fallback:** missing ex-dates in FinBas (fallback LSEG);
  Holdings history too short (fallback: annual-report ownership tables and
  Euroclear aggregates).

### 4. Empirical method

- **Baseline (premium):** Fama–MacBeth regressions of monthly returns on a
  predicted-dividend-month dummy with size, book-to-market and momentum
  controls; calendar-time long–short portfolios; daily decomposition into
  pre-ex run-up and post-ex reversal.
- **Crowding test:** abnormal return in the ex-day week regressed on the
  share of market capitalisation going ex in the same week, with stock and
  year fixed effects; heterogeneity by foreign and retail ownership from
  Holdings; regime split for negative policy rates.
- **Clientele test (secondary):** ex-day price-drop ratio (P_cum − P_ex)/D
  and abnormal ex-day volume regressed on lagged retail ownership share
  interacted with ISK diffusion and the 2025/2026 allowance steps, with
  firm and season fixed effects and controls for dividend yield, tick
  size, liquidity and foreign share; run in Mid Cap, Small Cap and First
  North where retail holds 30–60 percent.
- **Identification:** the crowding measure varies within stock across
  years for reasons unrelated to the stock (other firms' AGM dates); the
  ISK steps are market-wide time shocks with cross-sectional intensity
  from pre-determined retail ownership, so the comparison is across stocks
  within the same season and macro conditions cancel. **Threats:** the
  marginal investor in large caps is institutional or foreign (restrict
  the clientele test to smaller segments; the null is informative),
  concurrent shocks in spring 2025 (within-season cross-section, 2026
  season, placebo on non-dividend stocks), few independent seasons
  (cluster by season; use volume, which is far better powered than the
  drop ratio), price discreteness (control tick size as in Graham et
  al.), tax-neutral institutional arbitrage (predicts a ratio near one
  regardless; test where arbitrage is costly: illiquid, high-yield stocks).
- **Power:** ≈ 6,000–7,000 ex-day events over ≈ 25 seasons for the
  premium and crowding tests; the ISK step test has two post-shock seasons
  and is presented as suggestive, with volume as the primary outcome.
- **Software:** Python or Stata; standard asset-pricing toolkit.

### 5. Three-month scope

- **MVP:** Hartzmark and Solomon (2013) replication on Sweden with the
  season-concentration figure (share of ex-dates and dividend cash by week,
  Sweden vs US).
- **Extension:** crowding test, negative-rate regime, ISK clientele test
  with volume.
- **First test:** FinBas ex-date field and a Holdings export for ten stocks.
- **Failure mode:** no reliable ex-dates or ownership history.
- **Fallback:** premium and rate-regime tests only, using LSEG data.

### References — Topic 2

Daniel, Kent, Lorenzo Garlappi, and Kairong Xiao, 2021, Monetary policy and reaching for income, *Journal of Finance* 76, 1145–1193.

Elton, Edwin J., and Martin J. Gruber, 1970, Marginal stockholder tax rates and the clientele effect, *Review of Economics and Statistics* 52, 68–74.

Graham, John R., Roni Michaely, and Michael R. Roberts, 2003, Do price discreteness and transactions costs affect stock returns? Comparing ex-dividend pricing before and after decimalization, *Journal of Finance* 58, 2611–2636.

Hartzmark, Samuel M., and David H. Solomon, 2013, The dividend month premium, *Journal of Financial Economics* 109, 640–660.

Hartzmark, Samuel M., and David H. Solomon, 2019, The dividend disconnect, *Journal of Finance* 74, 2153–2199.

Jiang, Hao, and Zheng Sun, 2020, Reaching for dividends, *Journal of Monetary Economics* 115, 321–338.

Michaely, Roni, 1991, Ex-dividend day stock price behavior: The case of the 1986 Tax Reform Act, *Journal of Finance* 46, 845–859.

Rantapuska, Elias, 2008, Ex-dividend day trading: Who, how, and why? Evidence from the Finnish market, *Journal of Financial Economics* 88, 355–374.

---


## Tillägg 7 sep: nytt kärnankare för D

Kontoghiorghes, Alexander P., 2024, Do personal taxes affect investment
decisions and stock returns?, *Journal of Financial Economics* 162, 103927.
När AIM-aktier 2013 blev tillåtna i skattefria ISA-konton i Storbritannien
föll deras överavkastning med den effektiva skatten, och bolagen ökade
utdelning och investeringar. Det är den direkta mallen för ISK:
fribeloppet 2025/2026 som steg i skattefrihet, med hushållsägarandel
(Holdings) som behandlingsintensitet, och utfall i avkastning, utdelning
och investeringar, inte bara ex-dagen. Även Hackethal, Hanspal, Hartzmark &
Bräuer (2025, *RFS*, advance) om "free dividends" och Müller-Dethard,
Reinhardt & Weber (2025, *RoF* 29, 1467–1495) om kontostruktur och
återinvestering av utdelning. Med dessa ankare stiger D:s rubrikpoäng, men
huvudinvändningen kvarstår: två säsonger efter fribeloppet och ett troligt
nollresultat i ex-dagstestet.
