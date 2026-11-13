# Synopsis draft (working document, v1, 6 September 2026)

> **Hur detta ska användas.** Detta är ett strukturerat arbetsunderlag som
> följer kursens synopsismall punkt för punkt. Skriv om varje stycke med
> egna ord innan inlämning, kontrollera varje referens mot tidskriftens sida
> och logga AI-användningen (verktyg, datum, syfte) enligt kursens regler.
> Målformat: 1–2 sidor per ämne, PDF, `BScThesis_Surname1_Surname2.pdf`.

**Authors:** [Full name], [Full name]
**Preferred tutor, if any:** Topic 1 fits Alvin Chen or Laszlo Sajtos; Topic 2 fits Valentin Schubert. [State one name or "No preference".]

---

## Topic 1: Buy, Decentralise, Grow? Parent Type and the Financing of Acquired Swedish Private Firms

### 1. Tentative research question

*When a Swedish private firm is acquired, does the type of its new parent, a
private-equity-backed buy-and-build platform, a private equity fund
directly, a listed decentralised serial acquirer, or an independent
strategic buyer, determine whether the target's financial constraints are
relieved and growth follows?*

Acquisitions of private firms are the bulk of M&A activity but the smallest
part of the evidence (Netter, Stegemoller, and Wintoki, 2011). Sweden is an
unusually rich laboratory: roughly 1,000 private Swedish firms change owner
in a recorded transaction every year, and the buyer population is
dominated by two organisational models that the literature has not
compared. In our own S&P Capital IQ extract for 2025–2026, 38 percent of
acquisitions of Swedish private targets were add-ons by private-equity-owned
platforms, 12 percent were direct fund acquisitions, 8 percent were by
listed strategic buyers (including the decentralised serial acquirers such
as Lifco, Indutrade, Addtech, and Lagercrantz), and 42 percent were by other
strategic buyers. Existing work on Swedish buyouts (Olsson and Tåg, 2025;
Riksbank, 2025) compares PE-owned firms with firms that were not acquired
at all, so it cannot say whether the *owner type* or the *ownership change*
drives post-deal outcomes.

The economic mechanism is the financing synergy of Erel, Jang, and Weisbach
(2015): an acquisition gives a constrained private firm access to the
parent's internal capital market, so cash holdings fall, the sensitivity of
investment to cash flow falls, and investment and employment rise. The
competing hypothesis is governance and integration: growth requires active
restructuring and centralised functions (Eliason, Heebsh, McDevitt, and
Roberts, 2020), so a decentralised parent that leaves the target alone
should show no growth beyond selection. The question stays interesting if
the estimate is zero: if targets of all parent types evolve identically
after matching, post-deal growth reflects which firms get bought, not who
buys them, which speaks directly to the premium at which serial acquirers
trade and to the policy debate on private equity.

### 2. Closest literature and intended contribution

**Erel, Jang, and Weisbach (2015, JF).** Question: do acquisitions relieve
targets' financial constraints? Data: 5,187 acquisitions of mostly private
European targets, 2001–2008, target accounts from Amadeus. Method:
before/after comparison of cash holdings, cash-flow sensitivity of cash and
investment, with matched controls. Result: post-acquisition cash falls,
investment rises, sensitivities fall, most for small and constrained
targets. *We replicate* the baseline specification on Swedish targets
2015–2023 using Serrano. *We extend* by classifying the acquirer into four
parent types and estimating whether the relief differs by type.

**Boucly, Sraer, and Thesmar (2011, JFE).** Question: do LBOs of private
firms generate growth? Data: 839 French LBOs 1994–2004, matched DiD on
accounting data. Result: sales +12 percent, employment +18 percent, assets
+12 percent, concentrated in private-to-private deals and credit-constrained
industries. *We replicate* the matched-DiD design and the private-to-private
focus. *We extend* by separating fund-level buyouts from platform add-ons,
which now dominate PE activity in Swedish SMEs.

**Cohn, Hotchkiss, and Towery (2022, Review of Finance).** Question: where
does value come from in PE buyouts of private firms? Data: US corporate tax
returns 1995–2009. Result: targets are either weakly profitable or
profitable but growth-constrained; value comes from relaxing constraints
and operating improvement, not financial engineering; 41 percent do
add-ons. *We use* their ex-ante constraint classification as a heterogeneity
test that discriminates between selection and treatment.

**Eliason, Heebsh, McDevitt, and Roberts (2020, QJE).** Question: how do
acquisitions by large chains change acquired units? Data: US dialysis
facilities. Result: acquired facilities adopt the chain's practices, replace
skilled staff and raise throughput. *We borrow* the roll-up framing to
formulate the integration hypothesis for platform add-ons versus
decentralised serial acquirers.

**Bernstein, Lerner, and Mezzanotti (2019, RFS)** (PE-owned UK firms
invested more than matched firms in 2008 because sponsors supplied
liquidity) and **Olsson and Tåg (2025, JF)** (Swedish register evidence on
buyouts) anchor the Swedish and crisis dimensions; **Fuller, Netter, and
Stegemoller (2002, JF)** anchors serial acquirers; **Callaway and Sant'Anna
(2021, Journal of Econometrics)** provides the staggered-DiD estimator.
Non-core prior work we position against: Kärnä and Myers (2025, Economics
Letters; Serrano + PitchBook DiD on Swedish LBOs, leverage and interest
costs) and El Ghoul, Gong, and Guedhami (2024, RIBF; mechanisms behind
Erel et al. on Orbis data).

> Relative to Erel, Jang, and Weisbach (2015) and Boucly, Sraer, and
> Thesmar (2011), we replicate the constraint-relief design on the universe
> of Swedish private targets and extend it by comparing four parent types
> on the same target population, allowing us to test whether financing
> synergies require active integration or also arise under decentralised
> ownership.

### 3. Data and feasibility

- **Deal data:** S&P Capital IQ, own saved screen "Thesis MA DACH Nordics
  2015+" (56,455 transactions; 2025–2026 already exported, 2015–2024 being
  exported at 2–3 years per day). Swedish private targets ≈ 1,000 per year.
  Acquirer type from buyer type, buyer company type and buyer sponsor
  status ("Current Sponsor" identifies platform add-ons); verified
  manually on a random subsample.
- **Outcomes:** Serrano (Swedish House of Finance): annual accounts for all
  Swedish limited companies since 1997, employees, industry, group parent,
  bankruptcy. Access through SWAMID. Variables to confirm at first login:
  interest expense, group receivables/payables, appropriations, municipality.
- **Owner age (heterogeneity subsample):** board members' birth years from
  Retriever Business/Bolagsverket for targets.
- **Unit of observation:** firm-year. **Geography:** Sweden. **Period:**
  deals 2015–2023, accounts 2011–2024 (event window t−4 to t+3).
- **Outcomes:** cash/assets, investment/assets, sales growth, employment
  growth, leverage, interest expense/debt, exit (bankruptcy, merger into
  parent). **Treatment:** completed change-of-control acquisition, by parent
  type. **Controls:** size, age, 5-digit SNI × year, county, pre-period
  growth, profitability, leverage, cash.
- **Expected sample:** ≈ 8,000–9,000 Swedish private targets 2015–2023;
  with a 65–70 percent match to organisation numbers ≈ 6,000 treated firms
  and ≈ 30,000 matched controls (5:1).
- **Access verified?** Capital IQ: yes (export in hand, library workshop 8
  Sep). Serrano: SSE access, first login and variable list this week.
  Retriever: library access, export test this week.
- **Cleaning/merging:** Capital IQ name → organisation number (Capital IQ
  carries it for many Swedish firms; fuzzy match plus manual check for the
  rest); event year = first full fiscal year after closing; drop broken
  fiscal years.
- **Main data risks and fallback:** match rate below 50 percent, or missing
  group/merger identifiers in Serrano. Fallback: use Serrano's own
  group-parent changes as the universe of ownership changes and Capital IQ
  only to classify the parent; the constraint-relief question can still be
  answered.

### 4. Empirical method

- **Baseline:** event-study difference-in-differences with firm and
  industry-by-year fixed effects, estimated with the Callaway and Sant'Anna
  (2021) estimator using matched never-treated and not-yet-treated
  controls; coefficients for k = −4,…,+3 relative to the deal year, by
  parent type. Investment-cash-flow sensitivity: regress investment/assets
  on cash flow/assets, a post indicator, their interaction, and the triple
  interaction with parent type.
- **Identification logic:** conditional on matching and pre-trends, the
  post-deal change relative to controls measures the treatment effect on
  the type of firm that gets bought. The *difference* between parent types
  is the headline, because selection on expected growth is common to all
  acquirers and partly cancels.
- **Key assumptions:** parallel pre-trends by parent type; no differential
  accounting changes that mimic constraint relief.
- **Threats:** (i) selection on expected growth: report pre-trends, use
  Cohn-style ex-ante constraint splits (effects concentrated in constrained
  targets are hard to explain by positive selection); (ii) accounting
  artefacts after group inclusion: use EBIT before appropriations, track
  intra-group receivables and debt as mechanisms rather than noise;
  (iii) attrition through merger into the parent, which is more common for
  integrating strategics: track merger codes, report attrition by parent
  type, bound with Lee bounds, keep the headline window at three years;
  (iv) reverse causality from growth to acquisition: addressed by matching
  on pre-period growth and by the placebo below.
- **Robustness/placebo:** announced-but-withdrawn deals (if n ≥ 50),
  randomised event dates, alternative matching, succession-driven subsample
  (oldest board member ≥ 62, no younger family member) where the seller's
  motive is plausibly unrelated to prospects.
- **Power:** with ≈ 6,000 treated firms and firm-clustered errors, the
  minimum detectable effect on annual employment growth is on the order of
  1–1.5 percentage points, well below the magnitudes in Boucly et al.
- **Software and skills:** Python or Stata; staggered DiD (`csdid`/`did`),
  matching, fuzzy name matching.

### 5. Three-month scope

- **Minimal viable analysis:** Erel et al. replication on Swedish targets,
  PE versus non-PE parents.
- **Meaningful extension:** four parent types, constraint heterogeneity,
  mechanism tables (intra-group financing, leverage), succession subsample.
- **First data test:** Serrano variable list and a 50-firm name match this
  week; export one more Capital IQ year.
- **Main failure mode:** low match rate or unresolved accounting artefacts
  in the strategic-buyer arm.
- **Fallback:** Serrano-only ownership-change study of constraint relief
  with parent classified from Serrano, dropping the strategic arm if
  attrition cannot be bounded.

### References — Topic 1

Bernstein, Shai, Josh Lerner, and Filippo Mezzanotti, 2019, Private equity and financial fragility during the crisis, *Review of Financial Studies* 32, 1309–1373.

Boucly, Quentin, David Sraer, and David Thesmar, 2011, Growth LBOs, *Journal of Financial Economics* 102, 432–453.

Callaway, Brantly, and Pedro H. C. Sant'Anna, 2021, Difference-in-differences with multiple time periods, *Journal of Econometrics* 225, 200–230.

Cohn, Jonathan B., Edith S. Hotchkiss, and Erin M. Towery, 2022, Sources of value creation in private equity buyouts of private firms, *Review of Finance* 26, 257–285.

Eliason, Paul J., Benjamin Heebsh, Ryan C. McDevitt, and James W. Roberts, 2020, How acquisitions affect firm behavior and performance: Evidence from the dialysis industry, *Quarterly Journal of Economics* 135, 221–267.

Erel, Isil, Yeejin Jang, and Michael S. Weisbach, 2015, Do acquisitions relieve target firms' financial constraints?, *Journal of Finance* 70, 289–328.

Fuller, Kathleen, Jeffry Netter, and Mike Stegemoller, 2002, What do returns to acquiring firms tell us? Evidence from firms that make many acquisitions, *Journal of Finance* 57, 1763–1793.

Netter, Jeffry, Mike Stegemoller, and M. Babajide Wintoki, 2011, Implications of data screens on merger and acquisition analysis: A large sample study of mergers and acquisitions from 1992 to 2009, *Review of Financial Studies* 24, 2316–2357.

Olsson, Martin, and Joacim Tåg, 2025, What is the cost of privatization for workers?, *Journal of Finance* 80, 2107–2151.

Non-core, cited for positioning only: Kärnä, Anders, and Samantha Myers, 2025, Plundered or profitably pumped-up? The effects of private equity takeover, *Economics Letters* 247, 112054; Andersson, Mathias, Anders Kärnä, and Samantha Myers, 2025, Private equity in Sweden: A financial stability perspective, Sveriges Riksbank Staff Memo, https://www.riksbank.se.

---

## Topic 2: Powerless? Corporate Liquidity and the 2022 Electricity Shock in Southern Sweden

### 1. Tentative research question

*When electricity prices in bidding zones SE3 and SE4 rose to more than twice
the level in SE1 and SE2 during 2022, did cash buffers and credit access
determine which private firms cut investment and employment, and did the
2023 electricity support to firms act as constraint relief or as a cash
windfall?*

Sweden has been divided into four electricity bidding zones since November
2011. Transmission bottlenecks between the hydro-rich north and the
gas-price-linked south turned the 2022 energy crisis into a within-country
natural experiment: Nord Pool annual average prices were 63 and 66 öre per
kWh in SE1 and SE2 but 137 and 162 öre in SE3 and SE4, against 43, 43, 67
and 82 öre in 2021 and 46, 46, 59 and 80 öre in 2023. Firms in the south
with the same industry, size and age as firms in the north faced a large,
temporary, plausibly exogenous cost shock. In 2023 the government paid
electricity support to firms only in SE3 (50 öre per kWh) and SE4 (79 öre
per kWh), based on consumption between October 2021 and September 2022,
capped at SEK 20 million per group and credited to the tax account
between June and December 2023 (SFS 2023:233; roughly SEK 29 billion
expected).

The finance question is how a negative cash-flow shock transmits to real
decisions. In the financing-frictions view (Fazzari-type sensitivities;
Brown, Gustafson, and Ivanov, 2021), firms with thin cash and credit cannot
smooth the shock and cut investment and jobs, while unconstrained firms
borrow or draw down cash; a later cash injection then restores investment
in constrained firms. In the pass-through view, effects scale with
electricity intensity regardless of balance sheets because firms raise
prices, and a windfall raises cash and dividends rather than investment
(Blanchard, López-de-Silanes, and Shleifer, 1994). A null on the
financial-constraint interaction is informative: it would mean the shock
was absorbed through prices, not balance sheets, and that the support
was largely a transfer.

### 2. Closest literature and intended contribution

**Bartram, Hou, and Kim (2022, JFE).** Question: do financially constrained
firms respond differently to a regional energy-cost regulation? Data: US
plants and firms around California's cap-and-trade programme. Method:
difference-in-differences with financial-constraint interactions and
spillovers to plants elsewhere. Result: constrained firms shift activity
out of the regulated region and reduce output; unconstrained firms do not.
*We replicate* the regional-shock-by-constraint design with Swedish
bidding zones as the regional variation. *We extend* with a shock that is
a market price rather than a regulation, with the full population of
private SMEs, and with a subsequent cash injection.

**Brown, Gustafson, and Ivanov (2021, JF).** Question: how do firms weather
cash-flow shocks? Data: US firms hit by unusually severe winter weather,
matched to credit-line data. Method: difference-in-differences using
weather shocks. Result: firms draw on credit lines; constrained firms
without lines cut investment. *We replicate* the logic that the response
to a transitory cash-flow shock reveals financing frictions; Serrano gives
cash, bank debt and trade credit for every Swedish limited company.

**Blanchard, López-de-Silanes, and Shleifer (1994, JFE).** Question: what do
firms do with cash windfalls? Result: windfalls unrelated to investment
opportunities are largely retained or paid out, not invested. *We use* the
2023 support payment, whose size depends on zone and past consumption
rather than on 2023 opportunities, as a windfall test.

**Colmer, Martin, Muûls, and Wagner (2024, REStud)** (firm-level effects of
carbon pricing in the EU ETS) and **Ivanov, Kruttli, and Watugala (2024,
RFS)** (bank lending responses to cap-and-trade) anchor the identification
of energy-cost shocks at the firm level; **Känzig (2021, AER)** anchors the
macro transmission of energy price shocks. **Almeida, Campello, and
Weisbach (2004, JF)** provides the cash-flow sensitivity of cash as a
constraint measure. Non-core prior work we position against: Bălașa and
Pollitt (2026, EPRG working paper; descriptive study of Swedish zonal prices
and industrial relocation, which explicitly calls for firm-level evidence)
and Bijnens, Hutchinson, Konings, and Saint-Guilhem (2024, working paper;
Belgian electricity prices, financial constraints and employment before
the crisis).

> Relative to Bartram, Hou, and Kim (2022) and Brown, Gustafson, and
> Ivanov (2021), we replicate the constraint-amplification design on a
> within-country price shock covering all Swedish private firms, and
> extend it with a zone-specific cash injection that lets us separate
> constraint relief from windfall effects.

### 3. Data and feasibility

- **Firm data:** Serrano (Swedish House of Finance): annual accounts,
  employees, industry, group structure and bankruptcy for all Swedish
  limited companies, 2015–2024 (FY2024 in the December 2025 update).
  Access through SWAMID. To confirm at first login: municipality of
  registered office and an establishment-count or group flag.
- **Exposure:** Nord Pool annual and monthly zone prices (public);
  municipality-to-zone mapping (public; a few municipalities straddle a
  border and are dropped); SCB electricity use per unit of value added by
  industry (table EN0301) as electricity intensity.
- **Support:** SFS 2023:233 terms; the overlapping national scheme for
  energy-intensive firms administered by Energimyndigheten (not
  zone-restricted) is netted out by excluding eligible energy-intensive
  industries or controlling for them.
- **Unit:** firm-year. **Period:** 2015–2024. **Sample:** single-unit
  private firms with at least five employees, outside groups, which limits
  registered-office mismeasurement; ≈ 100,000 firms.
- **Outcomes:** cash/assets, net debt, trade payables, interest coverage,
  dividends, shareholder contributions, investment/assets, employment
  growth, exit (bankruptcy, reconstruction). **Treatment intensity:** zone
  price × industry electricity intensity, continuous from mid-2021.
  **Constraint measures (pre-determined, 2020):** cash/assets, leverage,
  age, size.
- **Access verified?** Serrano: SSE licence, variable list this week. Zone
  prices and SCB tables: public, already located.
- **Main data risks and fallback:** no municipality variable in Serrano
  (fallback: Retriever Business postal address for a stratified sample);
  firm-level support amounts are tax-secret and unobservable (support is
  therefore imputed from zone and consumption, and the windfall test uses
  SE4 versus SE3 intensity in 2023–2024 as a secondary analysis).

### 4. Empirical method

- **Baseline:** event-study difference-in-differences with firm and
  industry-by-year fixed effects and municipality fixed effects, where the
  treatment is continuous exposure (zone price × electricity intensity)
  interacted with year indicators 2016–2024; triple interaction with
  pre-determined constraint measures.
- **Identification logic:** within industry and year, firms in the south
  faced higher input prices for reasons set by interconnector capacity and
  continental gas prices, not by local demand; the constraint interaction
  compares firms with the same exposure but different balance sheets.
- **Key assumptions:** parallel trends by zone within industry
  (event-study pre-period 2015–2020); no differential non-energy shock in
  the south correlated with balance sheets.
- **Threats:** (i) registered office differs from production site (single-
  unit firms; measurement error biases toward zero); (ii) fixed-price
  contracts and hedging unobserved (intention-to-treat; heterogeneity by
  2022 gross-margin change as realised exposure); (iii) SE4 is Skåne and
  may differ structurally (continuous exposure rather than zone dummies;
  border-municipality subsample along SE2/SE3 and SE3/SE4); (iv) the 2022
  rate hikes interact with leverage in the same way as the energy shock
  (run the constraint interaction as a placebo in SE1/SE2, where there was
  no energy shock but the same rate cycle); (v) the north–south gap opened
  in mid-2021 and closed in November–December 2022 (use monthly prices to
  build annual exposure rather than a post-2021 dummy); (vi) support
  anticipated from December 2022 (timing tests).
- **Planned robustness/placebo:** SE1/SE2 placebo, pre-2021 placebo years,
  border municipalities, alternative intensity measures, exclusion of
  energy-intensive industries covered by the national scheme.
- **Power:** ≈ 100,000 firms and a shock of 70–100 öre per kWh give ample
  power for the main effect; the constraint interaction and the windfall
  test are reported with municipality-clustered errors.
- **Software and skills:** Python or Stata; panel fixed effects, event
  studies, geographic mapping of municipalities to zones.

### 5. Three-month scope

- **Minimal viable analysis:** zone-by-intensity event study 2016–2024 on
  investment, employment and cash, with constraint heterogeneity.
- **Meaningful extension:** balance-sheet transmission (debt, payables,
  dividends) and the 2023 windfall chapter (SE4 versus SE3).
- **First data test:** Serrano municipality and establishment variables;
  build the municipality-to-zone map; pull Nord Pool monthly prices.
- **Main failure mode:** no reliable firm location.
- **Fallback:** industry-intensity-only design without zones (weaker), or
  switch to the reserve topic on dividend seasons documented separately.

### References — Topic 2

Almeida, Heitor, Murillo Campello, and Michael S. Weisbach, 2004, The cash flow sensitivity of cash, *Journal of Finance* 59, 1777–1804.

Bartram, Söhnke M., Kewei Hou, and Sehoon Kim, 2022, Real effects of climate policy: Financial constraints and spillovers, *Journal of Financial Economics* 143, 668–696.

Blanchard, Olivier Jean, Florencio López-de-Silanes, and Andrei Shleifer, 1994, What do firms do with cash windfalls?, *Journal of Financial Economics* 36, 337–360.

Brown, James R., Matthew T. Gustafson, and Ivan T. Ivanov, 2021, Weathering cash flow shocks, *Journal of Finance* 76, 1731–1772.

Colmer, Jonathan, Ralf Martin, Mirabelle Muûls, and Ulrich J. Wagner, 2024, Does pricing carbon mitigate climate change? Firm-level evidence from the European Union emissions trading system, *Review of Economic Studies* 92, 1625–1660.

Ivanov, Ivan T., Mathias S. Kruttli, and Sumudu W. Watugala, 2024, Banking on carbon: Corporate lending and cap-and-trade policy, *Review of Financial Studies* 37, 1640–1684.

Känzig, Diego R., 2021, The macroeconomic effects of oil supply news: Evidence from OPEC announcements, *American Economic Review* 111, 1092–1125.

Non-core, cited for positioning only: Bălașa, Alexandru, and Michael G. Pollitt, 2026, Have zonal electricity prices in Sweden caused industrial (re)locations?, EPRG Working Paper 2602, University of Cambridge; Bijnens, Gert, John Hutchinson, Jozef Konings, and Arthur Saint-Guilhem, 2024, The interplay between green policy, electricity prices, financial constraints and jobs, working paper (SSRN 4832157); Sveriges Riksdag, 2023, Förordning (2023:233) om elstöd till företag.


---

### Kontroll före inlämning

- [ ] Varje referens kontrollerad mot tidskriftens sida (volym, sidor).
- [ ] Minst tre kärnreferenser per ämne, inga huvudreferenser utanför listan.
- [ ] Datatester genomförda och resultaten inskrivna (matchningsgrad,
      Serrano-variabler, FinBas ex-dagar, Holdings-historik).
- [ ] Texten omskriven med egna ord; AI-logg sparad.
- [ ] 1–2 sidor per ämne; namn och önskad tutor överst; rätt filnamn.
