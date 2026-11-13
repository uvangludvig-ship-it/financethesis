# Synopsis draft, Topic 5 (tutor-suggested): Tokenization and the Future of Financial Markets

> **Arbetsanteckning (tas bort före inlämning).** Utkast 9 september 2026, skrivet
> enligt kursens synopsismall (fråga, litteratur, data, metod, tremånadersplan,
> referenser). Detta är ett handledarföreslaget ämne och räknas därför som det
> enda tillåtna "tutor-inspired topic"; det andra ämnet i inlämningen måste
> vara ett eget. Skriv om varje stycke med egna ord, kontrollera varje referens
> mot tidskriftens sida och logga AI-användningen enligt kursens regler.
> Verifierade fakta i utkastet: Lehar & Parlour JF 2025 (80:321–374);
> Hautsch, Scheuch & Voigt RoF 2024 (28:1345–1381); Capponi & Jia RFS 2025
> (38:3040–3085); Chiu & Koeppl RFS 2019 (32:1716–1753); Sockin & Xiong JF
> 2023 (78:247–299); xStocks lanserades 30 juni 2025 (Backed/Kraken, Solana);
> Ondo Global Markets lanserades september 2025; Ondo öppnade 24/7
> mint/redeem för sex tokens (SPYon, QQQon, CRCLon, NVDAon, TSLAon, GOOGLon)
> den 25 juni 2026; Krakens historiska OHLCVT-data är gratis (kvartalsvisa
> zip-filer, 1-minutsupplösning); Dune har en officiell xStocks-dashboard.
> Cong, Landsman, Rabetti, Zhang & Zhao, "Tokenized Stocks" (SSRN, dec 2025)
> är närmaste working paper och måste läsas i fulltext före första
> handledarmötet.

**Authors:** [Full name], [Full name]
**Preferred tutor, if any:** [Name or "No preference"]

---

## Topic 2: One Share, Two Ledgers: Price Discovery, Arbitrage and 24/7 Trading in Tokenized U.S. Equities

### 1. Tentative research question

*When the same U.S. share trades both on Nasdaq/NYSE and as a blockchain
token on centralized crypto exchanges and decentralized exchanges (DEXs),
where does price discovery take place, how large and persistent are the
deviations between the token and the underlying share, and do token prices
formed while the stock market is closed carry information about the next
opening price?*

Tokenized equities moved from concept to live markets in mid-2025. Backed
Finance's xStocks launched on 30 June 2025 on Solana and trade on Kraken,
Bybit and on-chain automated market makers (Raydium, Jupiter); Robinhood
launched stock tokens for European clients the same week; Ondo Global
Markets launched over 100 tokenized U.S. stocks in September 2025. By early
2026 xStocks alone reported more than USD 25 billion in cumulative
transaction volume and over 80,000 on-chain holders. Each token is backed
one-for-one by a share held with a custodian, can be minted and redeemed
at net asset value only by KYC-cleared participants above a minimum size,
and trades around the clock even though the underlying market is open
6.5 hours a day.

This is an unusually clean laboratory for the questions the topic
description raises. The same cash flow claim trades on a limit order book
that closes at 16:00 ET, on a centralized crypto exchange and on an
on-chain automated market maker, with different settlement (T+1 versus
block finality), different access rules and different trading hours.
Finance theory gives two competing predictions. Under the "wrapper" view,
tokens are a pass-through claim: arbitrage against the primary market
should keep deviations near zero during U.S. hours and token trading
outside those hours should add little information, as Barclay and
Hendershott (2003) find for thin after-hours trading. Under the "limits to
arbitrage" view, gated redemption, settlement latency, gas fees and
crypto-market risk (Hautsch, Scheuch and Voigt, 2024; Makarov and Schoar,
2020; Capponi and Jia, 2025) allow deviations to open and persist,
especially when the underlying market is closed, and the size of those
deviations measures how much of the promised efficiency gain is actually
realized (Chiu and Koeppl, 2019; Adrian, 2026; OECD, 2025).

The question stays interesting if the estimate is zero. Deviations of zero
and no off-hours information would show that tokenization, as currently
implemented, changes the venue but not the price process, which would
weaken the case that 24/7 tokenized trading improves price discovery.
Large and persistent deviations would show that the benefits depend on who
may access the primary market and how fast settlement is, which is
directly relevant to the regulatory debate on tokenized securities.

### 2. Closest literature and intended contribution

**Gagnon and Karolyi (2010, JFE), "Multi-market trading and arbitrage".**
Question: how large are price deviations between cross-listed shares (ADRs)
and their home-market shares, and what explains them? Data: 506
cross-listed pairs from 35 countries, daily synchronous prices. Method:
parity deviations, their distribution and persistence, regressed on
holding costs, illiquidity and short-sale constraints. Result: deviations
are small on average but fat-tailed and larger when arbitrage is costly.
*We replicate* their parity-deviation design on token–share pairs. *We
extend* by exploiting that the "second market" here never closes, so the
deviation can be measured separately when the primary market is open and
when it is closed.

**Barclay and Hendershott (2003, RFS), "Price discovery and trading after
hours".** Question: is thin after-hours trading informative? Data: Nasdaq
trades and quotes including pre- and post-market sessions. Method: weighted
price contribution and variance ratios across periods. Result: after-hours
trades are few but each carries more information than a trade during the
day; prices are less efficient after hours. *We replicate* the weighted
price contribution for token trading between 16:00 ET and the next 09:30 ET
and over weekends. *We extend* by testing whether the token's weekend
return predicts the underlying's Friday-close-to-Monday-open return, with
slope one as the benchmark for full informativeness.

**Hasbrouck (1995, JF), "One security, many markets".** Question: which
market impounds information first when one asset trades in several places?
Data: NYSE-listed stocks traded on regional exchanges. Method: vector error
correction model and information shares. Result: the NYSE dominated price
discovery. *We replicate* the information-share method at one-minute
frequency during overlapping hours for token versus Nasdaq. *We extend* by
comparing a centralized crypto exchange and an on-chain AMM for the same
token, following Lehar and Parlour (2025) on AMM price formation.

**Hautsch, Scheuch and Voigt (2024, Review of Finance), "Building trust
takes time".** Question: why do Bitcoin prices differ across exchanges?
Data: Bitcoin network data and order books from several exchanges. Method:
relate cross-exchange price gaps to settlement latency and default risk.
Result: gaps widen when settlement is slow and are smaller across
low-default-risk exchanges. *We use* their settlement-latency measure of
limits to arbitrage as an explanatory variable for token–share deviations.

**Makarov and Schoar (2020, JFE)** document persistent cross-exchange
crypto arbitrage spreads tied to capital-flow frictions; **Capponi and Jia
(2025, RFS)** show that arbitrage rents on DEXs flow largely to validators;
**Chiu and Koeppl (2019, RFS)** model when blockchain settlement improves on
existing systems; **Yermack (2017, Review of Finance)** sets out the
governance and record-keeping consequences of on-chain ownership;
**O'Hara and Ye (2011, JFE)** provide the benchmark for how fragmentation
across venues affects market quality. The closest recent work is Cong,
Landsman, Rabetti, Zhang and Zhao (2025, working paper), who provide a first
empirical description of price discovery in tokenized stocks; we position
against their descriptive results and add the event-based design below.

> Relative to Gagnon and Karolyi (2010) and Barclay and Hendershott
> (2003), we replicate the parity-deviation and after-hours price
> discovery designs on tokenized U.S. equities and extend them by using
> Ondo's 25 June 2026 opening of 24/7 minting and redemption for six tokens
> as a natural experiment, allowing us to test whether access to the primary
> market, rather than trading hours themselves, is what keeps a tokenized
> asset priced like its underlying share.

### 3. Data and feasibility

- **Token prices, centralized venue:** Kraken publishes free historical
  OHLCVT files at 1-minute resolution for every pair, updated quarterly;
  xStocks pairs (e.g. TSLAx/USD) are included from June 2025. Ondo tokens
  (e.g. TSLAon) trade on Coinbase and other venues with public APIs;
  CoinGecko provides cross-venue minute data.
- **Token prices, on-chain:** Dune Analytics (SQL over decoded Solana and
  Ethereum data, free tier) with the official xStocks dashboard as
  starting point; Raydium/Jupiter swaps give trade-level prices, pool depth
  and fees; Ondo tokens on Ethereum, BNB Chain and Solana.
- **Underlying shares:** 1-minute trades and quotes including pre- and
  post-market sessions from Polygon.io (student subscription) or Refinitiv
  Tick History via the Swedish House of Finance if available; daily CRSP
  prices and corporate actions for adjustments. For SPY and QQQ tokens,
  E-mini S&P 500 and Nasdaq-100 futures give a near-continuous overnight
  benchmark.
- **Frictions:** Solana and Ethereum gas fees and block times (public
  RPC/Dune), BTC realized volatility (Kraken data), stablecoin USDC/USDT
  deviations from par.
- **Unit of observation:** token–venue–minute; aggregated to token–day and
  token–weekend for the event analysis. **Geography:** U.S. underlying,
  global token venues. **Period:** 30 June 2025 to the latest available
  quarter, roughly 15 months.
- **Outcomes:** log parity deviation, its half-life, information shares,
  weighted price contribution, off-hours predictive slope, quoted and
  effective spreads (Corwin–Schultz estimator where quotes are missing).
- **Expected sample:** about 60 xStocks and 100 Ondo tokens; roughly 100
  tokens with both a Kraken/Coinbase series and a DEX series; several
  million minute observations; 6 treated tokens in the event design.
- **Access verified:** Kraken download page and Dune xStocks dashboard
  confirmed public on 9 September 2026; Polygon.io pricing and SHoF tick
  data access to be confirmed in week 1.
- **Cleaning/merging:** time-zone alignment to ET, ticker mapping
  token→CUSIP, adjustment for splits and for dividends that Backed
  reinvests into the token (drift versus the cash-dividend share price),
  removal of pairs with zero volume days.
- **Main risks and fallback:** free-tier Dune limits (fallback: Kraken
  centralized data only); intraday underlying data cost (fallback: daily
  closes and the official pre/post-market prints); small treated group in
  the event design (fallback: descriptive before/after with permutation
  inference).

### 4. Empirical method

- **Baseline:** for token *i*, venue *v*, minute *t*,
  d_ivt = ln P^token_ivt − ln P^ref_it, where P^ref is the Nasdaq midquote
  when the market is open and the last close (or futures-implied price for
  ETF tokens) when it is closed. We report the distribution, an AR(1)
  half-life, and regress |d| on a market-closed dummy, hours since close,
  gas fees, pool depth, BTC volatility, stablecoin deviations and token
  fixed effects, with standard errors clustered by token and day.
- **Price discovery:** Hasbrouck (1995) information shares and Gonzalo–
  Granger component shares from a VECM of token and Nasdaq prices during
  09:30–16:00 ET; Barclay–Hendershott weighted price contribution for
  off-hours periods; regression of the underlying's overnight/weekend
  return on the token's off-hours return.
- **Identification (event):** difference-in-differences around 25 June
  2026. Treated: the six Ondo tokens that gained 24/7 mint/redeem.
  Controls: other Ondo tokens still on 24/5 access and xStocks on the same
  underlyings (TSLAx, NVDAx, GOOGLx, SPYx, QQQx). Outcome: weekend |d|,
  weekend spread and weekend informativeness. Key assumption: parallel
  trends in weekend deviations before the event, checked with event-time
  plots and a placebo date. Threat: the six tokens were chosen because they
  are the most liquid; we control for pre-event volume and use the xStocks
  twin of each treated token as the tightest comparison.
- **Threats and robustness:** stale reference prices (use futures for
  ETFs); wash trading on DEXs (drop trades below a size floor, replicate
  on Kraken only); corporate action mis-adjustment (exclude event windows);
  venue outages (drop days with gaps). Placebo: apply the same off-hours
  test to the ETF tokens where a liquid futures benchmark exists, where
  deviations should be smallest.
- **Power:** with minute data the parity and information-share estimates
  are precise; the event design has few treated units, so inference uses
  token-level clustering and randomization over token assignments.
- **Software and skills:** Python (pandas, statsmodels) or R, SQL on Dune,
  standard VECM/information-share code; skills covered in the econometrics
  courses of the programme.

### 5. Three-month scope

- **Minimal viable analysis:** parity deviations and their determinants for
  xStocks on Kraken versus Nasdaq, open versus closed hours, plus the
  weekend-return predictive regression. This alone answers the research
  question.
- **Meaningful extension:** information shares across Nasdaq, Kraken and
  the Solana AMM; the Ondo 24/7 mint/redeem event study.
- **First data test (week 1):** download the Kraken 2025 Q3 OHLCVT archive,
  extract TSLAx/USD and NVDAx/USD, align with Nasdaq 1-minute data for one
  month, and plot the deviation over a full week including the weekend.
- **Main failure risk:** DEX data proves too noisy or too expensive to
  clean within the timeframe.
- **Fallback:** a centralized-venue-only study of deviations and off-hours
  informativeness, which still tests the wrapper versus limits-to-arbitrage
  views.

### References — Topic 2

Adrian, T. (2026). *Tokenized Finance*. IMF Notes No. 2026/001. Washington,
DC: International Monetary Fund.

Barclay, M. J., and Hendershott, T. (2003). Price discovery and trading
after hours. *Review of Financial Studies*, 16(4), 1041–1073.

Capponi, A., and Jia, R. (2025). Liquidity provision on blockchain-based
decentralized exchanges. *Review of Financial Studies*, 38(10), 3040–3085.

Chiu, J., and Koeppl, T. V. (2019). Blockchain-based settlement for asset
trading. *Review of Financial Studies*, 32(5), 1716–1753.

Cong, L. W., Landsman, W. R., Rabetti, D., Zhang, C., and Zhao, W. (2025).
Tokenized stocks. Working paper, SSRN 5937314.

Gagnon, L., and Karolyi, G. A. (2010). Multi-market trading and arbitrage.
*Journal of Financial Economics*, 97(1), 53–80.

Hasbrouck, J. (1995). One security, many markets: Determining the
contributions to price discovery. *Journal of Finance*, 50(4), 1175–1199.

Hautsch, N., Scheuch, C., and Voigt, S. (2024). Building trust takes time:
Limits to arbitrage for blockchain-based assets. *Review of Finance*,
28(4), 1345–1381.

Lehar, A., and Parlour, C. A. (2025). Decentralized exchange: The Uniswap
automated market maker. *Journal of Finance*, 80(1), 321–374.

Makarov, I., and Schoar, A. (2020). Trading and arbitrage in cryptocurrency
markets. *Journal of Financial Economics*, 135(2), 293–319.

O'Hara, M., and Ye, M. (2011). Is market fragmentation harming market
quality? *Journal of Financial Economics*, 100(3), 459–474.

Organisation for Economic Co-operation and Development. (2025).
*Tokenisation of assets and distributed ledger technologies in financial
markets*. Paris: OECD Publishing. https://doi.org/10.1787/40e7f217-en

Sockin, M., and Xiong, W. (2023). Decentralization through tokenization.
*Journal of Finance*, 78(1), 247–299.

Yermack, D. (2017). Corporate governance and blockchains. *Review of
Finance*, 21(1), 7–31.
