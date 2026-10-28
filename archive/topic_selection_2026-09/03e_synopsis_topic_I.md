# Synopsis draft, Topic I (to pair with Topic 1 = H from `03c_synopsis_draft_H_G.md`), 7 September 2026

> Same rules: rewrite in your own words, verify references, log AI use.
> Target 1–2 pages.

## Topic 2: Do Taxes Depress or Stimulate Borrowing? Sweden's 2019 Corporate Tax Cut and Interest Deduction Limit in the Full Population of Private Firms

### 1. Tentative research question

*When Sweden cut the corporate tax rate and simultaneously capped interest
deductibility on 1 January 2019, did private firms borrow less, as the
trade-off theory of the tax shield predicts, or more, as the productivity
channel of Ivanov, Pettit, and Whited (2026) predicts, and does the answer
differ between firms that lost deductions and firms that only gained a
lower rate?*

The reform (prop. 2017/18:245) contained two treatments with opposite
predictions under the standard theory. The corporate tax rate fell from 22
to 21.4 percent in 2019 and to 20.6 percent in 2021, lowering the value of
the interest tax shield for every firm. At the same time, net interest
expense became deductible only up to 30 percent of taxable EBITDA, with a
simplification rule allowing SEK 5 million of net interest per group of
associated companies regardless. Trade-off theory (Heider and Ljungqvist,
2015) predicts lower leverage from both. Ivanov, Pettit, and Whited (2026)
find the opposite for small US private firms: after tax cuts, higher
after-tax cash flows move default further away, credit spreads fall, and
leverage rises. Sanati and Beyhaghi (2025) use the USD 25 million
exemption in the 2017 US reform in a regression discontinuity and find that
losing the deduction lowers debt and investment, with no equity
substitution. Sweden lets us run both tests in one population: all limited
companies, with the SEK 5 million simplification rule as a kink in marginal tax treatment and
the rate cut as a common shock whose bite varies with pre-reform taxable
profits. A null on both margins is informative: it would mean that Swedish
private-firm capital structure is not tax-driven at the elasticities
estimated in the US literature.

### 2. Closest literature and intended contribution

**Ivanov, Pettit, and Whited (2026, REStud).** Question: do corporate
taxes depress borrowing? Data: US private firms and state tax changes.
Method: difference-in-differences with a structural interpretation.
Result: leverage rises after tax cuts for small private firms because
lower taxes raise capital productivity and lower credit spreads. *We
replicate* the tax-cut response on Swedish private firms with the 2019 and
2021 rate steps. *We extend* by adding the simultaneous deduction cap,
which the US setting lacks at the same time.

**Sanati and Beyhaghi (2025, RFS).** Question: what happens when the tax
benefit of debt is removed? Data: US firms around the USD 25 million
gross-receipts exemption of the 2017 reform. Method: regression
discontinuity. Result: debt and investment fall; equity does not replace
debt. *We replicate* the discontinuity design at Sweden's SEK 5 million
net-interest threshold, measured per group of associated companies.

**Heider and Ljungqvist (2015, JFE).** Question: how tax-sensitive is
leverage? Data: US state corporate tax changes. Result: a one percentage
point tax increase raises leverage by about 0.4 percentage points;
responses are asymmetric. *We use* their elasticity as the benchmark for
the minimum detectable effect.

**Brok (2026, JFQA; 2024, Review of Finance).** Tax avoidance acts as a
non-debt tax shield that crowds out the debt tax shield (2026); corporate
group structure creates additional leverage incentives because parents can
deduct subsidiary losses (2024). Both imply tax effects on debt are a
group-level phenomenon. *We use* Serrano's group identifiers to measure the
threshold per group and to test whether groups reallocate interest across
entities to stay under the cap.

> Relative to Ivanov, Pettit, and Whited (2026) and Sanati and Beyhaghi
> (2025), we replicate both designs in one reform and one population of
> all Swedish limited companies, allowing us to test the trade-off and
> productivity channels against each other with a threshold that binds at
> the group level.

Our contribution is threefold. First, the first evidence on Sweden's 2019
reform for the full private-firm population [N to be inserted after the
Serrano count]. Second, a horse race between two channels with opposite
signs in the same data. Third, a hand-built group-level net-interest
variable that assigns the SEK 5 million threshold correctly, which
firm-level data cannot. Benchmark: Heider and Ljungqvist's elasticity
implies a leverage change of roughly 0.6 percentage points for the 1.4
point rate cut; our minimum detectable effect will be well below that.

### 3. Data and feasibility

- **Firm data:** Serrano, all Swedish limited companies 2013–2024: debt,
  interest expense, tax expense, EBITDA, investment, dividends, group
  parent and intra-group balances. SWAMID access; interest, tax and group
  fields to be confirmed at first login this week.
- **Treatment variables:** (i) rate cut: pre-reform effective tax
  payments/assets (loss-making firms untreated); (ii) cap: net interest
  expense 2017–2018 above versus below SEK 5 million, aggregated within
  groups of associated companies; (iii) a third treatment for rental
  housing firms (12 percent primary deduction).
- **Sample:** hundreds of thousands of firms; the cap binds for a few
  thousand, mainly real estate and PE-owned firms.
- **Access verified?** Serrano is a course resource; law text verified.
- **Risks and fallback:** concurrent 2019 rules (hybrid and CFC rules)
  affect large multinationals (exclude); interest rates were near zero
  2019–2021 and rose in 2022 (industry-by-year effects, dose design);
  anticipation after the bill of 3 May 2018 (check 2018). Fallback: rate
  cut only.

### 4. Empirical method

- **Baseline (rate cut):** difference-in-differences of leverage,
  new borrowing, interest expense/debt and investment on pre-reform tax
  exposure × post-2019 and post-2021 indicators, with firm and
  industry-by-year fixed effects.
- **Baseline (cap):** regression discontinuity in group net interest at
  SEK 5 million and bunching analysis, plus difference-in-differences for
  firms bound by the 30 percent EBITDA rule versus unbound.
- **Identification:** the law fixes both the rate path and the threshold;
  within industry and year, firms with different pre-reform tax exposure
  or net interest faced the same macro conditions.
- **Threats and mitigations:** manipulation at the threshold (bunching is
  itself a finding; use pre-reform net interest); intra-group reallocation
  (group aggregation, Brok test); rate cycle (industry-by-year effects;
  placebo in 2016–2018).
- **Power:** population data; minimum detectable effect on leverage well
  below 0.5 percentage points.
- **Software:** Python or Stata; panel fixed effects, RD.

### 5. Three-month scope

- **MVP:** rate-cut difference-in-differences with tax-exposure dose.
- **Extension:** threshold RD, bunching, group channel, rental housing.
- **First test:** Serrano interest, tax and group fields; count of groups
  above SEK 5 million.
- **Failure mode:** group aggregation infeasible. **Fallback:** firm-level
  threshold with attenuation caveat.

### References — Topic 2

Brok, Peter, 2024, Debt and taxes: The role of corporate group structure, *Review of Finance* 28, 2051–2082.

Brok, Peter, 2026, Debt and taxes: The role of tax avoidance, *Journal of Financial and Quantitative Analysis* 61, 2007–2032.

Heider, Florian, and Alexander Ljungqvist, 2015, As certain as debt and taxes: Estimating the tax sensitivity of leverage from state tax changes, *Journal of Financial Economics* 118, 684–712.

Ivanov, Ivan T., Luke Pettit, and Toni M. Whited, 2026, Taxes depress corporate borrowing: Evidence from private firms, *Review of Economic Studies* 93, 2715–2749.

Sanati, Ali, and Mehdi Beyhaghi, 2025, How does removing the tax benefits of debt affect firms? Evidence from the 2017 U.S. tax reform, *Review of Financial Studies*, advance access, https://doi.org/10.1093/rfs/hhaf041.

Sveriges riksdag, 2018, Nya skatteregler för företagssektorn, prop. 2017/18:245, https://www.riksdagen.se.
