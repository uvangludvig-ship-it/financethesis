# Synopsis draft, alternative pair H + G (working document, 7 September 2026)

> Same rules as `03_synopsis_draft.md`: rewrite in your own words, verify
> every reference against the journal page, log AI use. 1–2 pages per topic.

**Authors:** [Full name], [Full name]
**Preferred tutor, if any:** [Alvin Chen / Laszlo Sajtos / No preference]

---

## Topic 1: What Does the Threat of a Profit Cap Cost? Political Uncertainty and Sweden's Private Welfare Firms, 2016–2026

### 1. Tentative research question

*How did Sweden's private welfare firms respond to the threat of a statutory
profit cap, in investment, payouts, entry and exit, and ownership changes,
and did the response reverse when the threat was removed?*

Between November 2016 and June 2018 every private provider of tax-financed
schooling, social care and personal assistance in Sweden operated under a
credible legislative threat. The Reepalu inquiry (SOU 2016:78, 8 November
2016) proposed to cap operating profit at the government borrowing rate
plus seven percentage points times operating capital; the government's
bill (prop. 2017/18:159, 19 March 2018) adopted the cap; the Riksdag
rejected it on 7 June 2018. The threat returned with a directive for a
school sector "without profit motive" (dir. 2022:102, 30 June 2022), an
inquiry (SOU 2025:37, 8 April 2025), a bill restricting value transfers in
the school sector (prop. 2025/26:292, 25 June 2026, in force 1 July 2027),
and the general election of 13 September 2026 in which profit caps are a
campaign issue. Private providers deliver a substantial share of Swedish
schooling and social care [insert SCB/Skolverket share, verify], and many
of the largest are owned by private equity, so the question is
economically first-order and, to our knowledge, unstudied at the firm
level.

The mechanism is the real-option value of waiting under political
uncertainty (Julio and Yook, 2012; Jens, 2017): firms postpone irreversible
investment until the policy is resolved. A profit cap adds a second,
sharper prediction: capital retained inside a capped firm is worth less, so
owners should accelerate dividends and group contributions while the cap
is pending and reverse after 7 June 2018. The competing hypothesis is that
markets and owners assigned the proposal a low probability, since it
lacked a parliamentary majority, so nothing happened. A null is therefore
informative: it measures how much a politically salient but legislatively
weak threat actually costs.

### 2. Closest literature and intended contribution

**Julio and Yook (2012, JF).** Question: does political uncertainty reduce
corporate investment? Data: 48 countries, national elections 1980–2005,
firm-level investment. Method: election-year indicators in investment
regressions with firm and year effects; heterogeneity by election
closeness. Result: firms reduce investment expenditures by an average of
4.8 percent in election years relative to non-election years, and the
effect is consistent with delaying investment until uncertainty is
resolved. *We replicate* the event-window design on a
single, well-dated policy threat. *We extend* by identifying the treated
group within one country and by adding payout and ownership outcomes.

**Jens (2017, JFE).** Question: is the effect causal? Data: US firms and
gubernatorial elections. Method: difference-in-differences exploiting
staggered election timing, with placebo tests. Result: investment declines
before elections, particularly close ones, and rebounds after. *We
replicate* the placebo logic: healthcare providers (SNI 86), excluded from
the bill, serve as a within-sector control.

**Kelly, Pástor, and Veronesi (2016, JF).** Political uncertainty is priced
in option markets around elections and summits. *We use* the theory to
derive the payout prediction and, for the four listed welfare firms
(Attendo, Humana, AcadeMedia, Ambea), an illustrative event study.

**Bonaime, Gulen, and Ion (2018, JFE).** Policy uncertainty reduces merger
activity and lengthens completion. *We use* this for the ownership-change
outcome: sales of welfare firms, including to private equity, around the
threat.

> Relative to Julio and Yook (2012) and Jens (2017), we replicate the
> political-uncertainty investment design on a single legislative threat
> that hit an identifiable set of Swedish private firms, allowing us to test
> both the investment channel and the payout channel with a within-sector
> placebo.

Our contribution is threefold. First, we provide the first firm-level
evidence on how a sector-specific profit-cap threat affects investment,
using the full population of Swedish private welfare firms [N to be
inserted after the Serrano count, expected several thousand treated
firms]. Second, we test the real-option channel against the payout
channel, which make opposite predictions for dividends and group
contributions, and use private-equity ownership as a mechanism split.
Third, we hand-code the four legislative dates, the bill's sector scope
and the ownership type of the largest welfare groups from annual reports,
which lets us build a within-sector placebo that election-based designs
cannot. Benchmark: Julio and Yook (2012) find a 4.8 percent investment
reduction in election years; with our sample size and firm-clustered
errors the minimum detectable effect on investment/assets will be well
below that, so a null is a rejection of the election-based magnitude in
our setting.

### 3. Data and feasibility

- **Firm data:** Serrano (all Swedish limited companies), 2012–2024:
  investment, dividends, group contributions, cash, employees, entry, exit,
  group parent. SWAMID access; dividend, appropriation and deregistration
  fields to be confirmed at first login this week.
- **Treated:** SNI 85 (education), 87–88 (care, personal assistance).
  **Placebo:** SNI 86 (health care), excluded from the bill. **Controls:**
  matched private service firms. Listed firms from LSEG or FinBas.
- **Expected sample:** several thousand treated firms, tens of thousands of
  controls.
- **Risks and fallback:** owner and management screening rules from
  1 January 2019 (main window 2016–2018; SNI 85 separated from 87–88); the
  2022–2026 episode coincides with the rate shock (matching, SNI 86
  placebo); the listed sample is small and Ambea bid for Humana on 29 June
  2026 (event study illustrative only).

### 4. Empirical method

- **Baseline:** event-study difference-in-differences with firm and
  industry-by-year fixed effects around 8 November 2016, 19 March 2018 and
  7 June 2018; outcomes investment/assets, dividends/equity, group
  contributions, employment growth, exit, ownership change.
- **Identification:** the treated set is defined by the bill's own scope;
  SNI 86 shares public financing and demand structure but was excluded;
  matched service firms absorb aggregate shocks.
- **Mechanism:** private-equity-owned versus other treated firms (shorter
  horizon, higher leverage); firms with profits above the proposed cap
  versus below (bite of the cap).
- **Placebo/robustness:** SNI 86, pre-2016 pseudo-events, exclusion of
  asylum accommodation (SNI 87.9), alternative matching. Software: Python or
  Stata.

### 5. Three-month scope

- **MVP:** 2014–2020 DiD on investment and payouts with SNI 86 placebo.
- **Extension:** 2022–2026 school episode, PE mechanism, listed event study.
- **First test:** Serrano dividend and appropriation fields.
- **Failure mode:** treated definition too coarse. **Fallback:** restrict to
  firms with public-sector revenue share above a threshold using SCB
  procurement data or company descriptions.

### References — Topic 1

Bonaime, Alice, Huseyin Gulen, and Mihai Ion, 2018, Does policy uncertainty affect mergers and acquisitions?, *Journal of Financial Economics* 129, 531–558.

Jens, Candace E., 2017, Political uncertainty and investment: Causal evidence from U.S. gubernatorial elections, *Journal of Financial Economics* 124, 563–579.

Julio, Brandon, and Youngsuk Yook, 2012, Political uncertainty and corporate investment cycles, *Journal of Finance* 67, 45–83.

Kelly, Bryan, Ľuboš Pástor, and Pietro Veronesi, 2016, The price of political uncertainty: Theory and evidence from the option market, *Journal of Finance* 71, 2417–2480.

---

## Topic 2: Consolidation Below the Radar: Private Equity Roll-Ups and Market Power in Swedish Local Service Markets

### 1. Tentative research question

*When private-equity-backed platforms acquire small competitors in a local
service market, do the margins of the remaining independent firms rise or
fall, and do entry and exit change?*

Since 2015 private-equity-backed platforms have acquired hundreds of small
Swedish firms in fragmented local service industries: dental and
veterinary clinics, electrical and plumbing installers, accounting firms,
physiotherapy and elderly care. In our Capital IQ extract for 2025–2026,
platform add-ons are the single largest acquisition channel for Swedish
private targets (38 percent). Each deal is far below the merger-control
thresholds in the Competition Act (combined Swedish turnover above SEK 1
billion and at least two parties above SEK 200 million), so the resulting
local concentration has never been reviewed. On 1 August 2026 a new law
(2026:580) gave the Competition Authority the power to call in deals below
the thresholds and to order serial acquirers to pre-notify all deals, citing
small and local markets. Whether the problem the law targets exists is an
open empirical question; we found no firm-level study of it in Sweden or
Europe.

The market-power hypothesis (Kepler, Naiker, and Stewart, 2023; Cunningham,
Ederer, and Ma, 2021) predicts that consolidation raises prices and margins
for all local providers, including independents that were not acquired.
The efficiency hypothesis (Eliason, Heebsh, McDevitt, and Roberts, 2020)
predicts that platforms lower costs, squeeze independents' margins and
push them out. A null implies that local service markets are contestable
and that the 2026 law addresses a problem that did not materialise.

### 2. Closest literature and intended contribution

**Kepler, Naiker, and Stewart (2023, JF).** Question: do acquisitions
structured to avoid antitrust review reduce competition? Data: US deals
around the Hart–Scott–Rodino thresholds. Method: bunching below thresholds
and product-market outcomes. Result: below-threshold acquisitions of rivals
reduce competition and raise markups. *We replicate* the "unreviewed
consolidation" question in a setting where every deal is unreviewed by
construction. *We extend* from acquirers to the rivals left behind.

**Cunningham, Ederer, and Ma (2021, JPE).** Acquisitions below notification
thresholds shut down competing projects; 5–7 percent of pharma deals are
"killer". *We borrow* the focus on competitive effects invisible to
regulators.

**Eliason, Heebsh, McDevitt, and Roberts (2020, QJE).** Chains transfer
their practices to acquired dialysis facilities. *We replicate* the
facility-level event study for acquired units and add non-acquired rivals.

**Gupta, Howell, Yannelis, and Gupta (2024, RFS)** anchors the
welfare-sector concern (nursing homes); **Aggarwal and Baxamusa (2025,
JFQA)** provides recent evidence on stealth mergers.

> Relative to Kepler, Naiker, and Stewart (2023) and Eliason et al. (2020),
> we measure the effect of unreviewed roll-ups on the rivals that remain,
> using the full population of Swedish firms, allowing us to distinguish
> market power from efficiency in markets the new 2026 law targets.

Our contribution is threefold. First, we build the first universe of
private-equity add-on acquisitions in Swedish local service markets from
Serrano group-parent changes and Capital IQ sponsor data [N to be inserted;
our 2025–2026 extract alone contains 370 platform add-ons of Swedish
private targets]. Second, we test market power against efficiency on the
firms that were not acquired, which neither Kepler et al. nor Eliason et
al. observe. Third, we add clinic-level dental prices from TLV, so that for
one industry the price channel is observed directly. Benchmark: Kepler,
Naiker, and Stewart (2023) report higher markups after below-threshold
acquisitions of rivals; with hundreds of treated local markets per
industry, our minimum detectable effect on independents' operating margins
is on the order of one percentage point, so a null rejects a market-power
effect of that size.

### 3. Data and feasibility

- **Firm data:** Serrano: accounts, SNI, registered municipality, group
  parent changes (the universe of add-ons), deregistration reason;
  platforms identified from Capital IQ sponsor status. Dental prices per
  clinic from TLV's Tandpriskollen (export to be verified).
- **Unit:** firm-year and market-year (municipality or functional region ×
  industry), 2012–2024; single-establishment firms in five to six service
  industries; thousands of local markets. Municipality and deregistration
  fields to be confirmed at first Serrano login this week.
- **Risks and fallback:** registered office differs from operating site
  (single-establishment firms); acquired units merged into platform
  entities (code mergers separately; main outcomes on independents);
  Capital IQ misses small add-ons (Serrano parent changes as universe).
  Fallback: dental and installation only.

### 4. Empirical method

- **Baseline:** stacked difference-in-differences at the market level,
  treatment = first platform acquisition in the market, dose = platform
  share of market turnover; Callaway and Sant'Anna estimator; outcomes for
  remaining independents: operating margin, sales, wage cost per employee,
  exit (bankruptcy versus merger), entry; for acquired units: margin,
  employment, prices where available.
- **Identification:** matched control markets on pre-trends in growth and
  margins; timing of platform entry driven by the platform's national
  roll-out rather than local conditions (instrument: platform founding year
  × distance to its first acquisition).
- **Threats:** market definition (municipality, FA region, radius;
  robustness); reverse causality (matching, instrument); selection of
  independents that later get acquired (exclude within three years).
  Software: Python or Stata with geographic mapping.

### 5. Three-month scope

- **MVP:** dental and installation, municipality DiD on independents'
  margins and exit.
- **Extension:** dental prices, dose–response, further industries.
- **First test:** Serrano municipality and parent-change fields; count of
  platform add-ons per industry.
- **Failure mode:** no reliable location. **Fallback:** industry-level
  concentration without geography (weaker), or switch to topic A.

### References — Topic 2

Aggarwal, Rajesh K., and Mufaddal Baxamusa, 2025, Stealth mergers and investment outcomes, *Journal of Financial and Quantitative Analysis* 60, 2060–2087.

Cunningham, Colleen, Florian Ederer, and Song Ma, 2021, Killer acquisitions, *Journal of Political Economy* 129, 649–702.

Eliason, Paul J., Benjamin Heebsh, Ryan C. McDevitt, and James W. Roberts, 2020, How acquisitions affect firm behavior and performance: Evidence from the dialysis industry, *Quarterly Journal of Economics* 135, 221–267.

Gupta, Atul, Sabrina T. Howell, Constantine Yannelis, and Abhinav Gupta, 2024, Owner incentives and performance in healthcare: Private equity investment in nursing homes, *Review of Financial Studies* 37, 1029–1077.

Kepler, John D., Vic Naiker, and Christopher R. Stewart, 2023, Stealth acquisitions and product market competition, *Journal of Finance* 78, 2837–2900.

Non-core, cited for positioning only: Stiebale, Joel, and Florian Szücs, 2022, Mergers and market power: Evidence from rivals' responses in European markets, *RAND Journal of Economics* 53, 678–702; Wollmann, Thomas G., 2019, Stealth consolidation: Evidence from an amendment to the Hart-Scott-Rodino Act, *American Economic Review: Insights* 1, 77–94.
