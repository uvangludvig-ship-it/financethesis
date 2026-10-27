# Synopsis draft, pair A + B, condensed to 1–2 pages per topic (7 September 2026)

> Condensed from `03_synopsis_draft.md` to meet the 1–2 pages per topic
> requirement. Same rules: rewrite in your own words, verify references,
> log AI use.

**Authors:** [Full name], [Full name]
**Preferred tutor, if any:** [Alvin Chen / Valentin Schubert / No preference]

---

## Topic 1: Buy, Decentralise, Grow? Parent Type and the Financing of Acquired Swedish Private Firms

**Tentative research question.** *When a Swedish private firm is acquired,
does the type of its new parent, a private-equity-backed platform, a
private equity fund, a listed decentralised serial acquirer, or an
independent strategic buyer, determine whether the target's financial
constraints are relieved and growth follows?*

Roughly 1,000 private Swedish firms change owner in a recorded transaction
each year. In our Capital IQ extract for 2025–2026, 38 percent of these
acquisitions were add-ons by private-equity-owned platforms, 12 percent
direct fund acquisitions, 8 percent by listed strategic buyers including
serial acquirers such as Lifco and Indutrade, and 42 percent by other
strategic buyers. Existing Swedish evidence (Olsson and Tåg, 2025; Kärnä
and Myers, 2025) compares PE-owned firms with firms never acquired, so it
cannot separate the effect of the owner type from the effect of the
ownership change. The mechanism is the financing synergy of Erel, Jang,
and Weisbach (2015): access to a parent's internal capital market lowers
cash holdings and the sensitivity of investment to cash flow and raises
investment and employment. The competing hypothesis is that growth requires
active integration (Eliason, Heebsh, McDevitt, and Roberts, 2020), so a
decentralised parent shows no growth beyond selection. A zero difference
across parent types is informative: post-deal growth would then reflect
which firms get bought, not who buys them.

**Closest literature and contribution.** Erel, Jang, and Weisbach (2015,
JF) study 5,187 acquisitions of mostly private European targets 2001–2008
with matched before/after comparisons and find lower cash, higher
investment and lower cash-flow sensitivities after the deal, most for small
and constrained targets; we replicate this baseline on Swedish targets
2015–2023. Boucly, Sraer, and Thesmar (2011, JFE) find that French
private-to-private LBOs raise sales by 12 percent and employment by 18
percent in a matched difference-in-differences; we replicate the design
and separate fund buyouts from platform add-ons. Cohn, Hotchkiss, and
Towery (2022, Review of Finance) show with US tax returns that PE targets
are either weakly profitable or growth-constrained and that value comes
from relaxing constraints; we use their ex-ante constraint classification
to discriminate selection from treatment. Bernstein, Lerner, and Mezzanotti
(2019, RFS) and Olsson and Tåg (2025, JF) anchor the crisis and Swedish
register dimensions; Callaway and Sant'Anna (2021, Journal of Econometrics)
provide the estimator. Relative to Erel et al. and Boucly et al., we
compare four parent types on the same target population, allowing us to
test whether financing synergies require integration or also arise under
decentralised ownership. Our contribution is threefold: a hand-built
dataset classifying about 6,000 acquired Swedish firms into four parent
types; a test of financing synergy against integration on the same
population; and the first evidence on targets of decentralised serial
acquirers, the model that the new Competition Act amendment (2026:580, in
force 1 August 2026) and the Riksbank's 2025 private equity review both
single out. Benchmark: Boucly et al. report employment growth of 18
percent; our minimum detectable effect is around 1–1.5 percentage points
per year.

**Data and feasibility.** Deals from our Capital IQ screen (56,455 DACH and
Nordic transactions 2015–2026; 2025–2026 exported, remaining years in
progress), with parent type from buyer type, company type and sponsor
status. Outcomes from Serrano (all Swedish limited companies since 1997:
accounts, employees, group parent, bankruptcy; SWAMID access). Board birth
years from Retriever for a succession subsample. Unit: firm-year, deals
2015–2023, accounts 2011–2024. Expected sample: 8,000–9,000 Swedish private
targets, about 6,000 matched to organisation numbers, and 30,000 matched
controls. Serrano variable list and a 50-firm name-match test are
scheduled this week. Fallback: use Serrano's own group-parent changes as
the universe of ownership changes and Capital IQ only to classify the
parent.

**Empirical method.** Event-study difference-in-differences with firm and
industry-by-year fixed effects, Callaway–Sant'Anna estimator with matched
never-treated and not-yet-treated controls, coefficients for years −4 to
+3 by parent type; investment–cash-flow sensitivity with post and
parent-type interactions. The headline is the difference between parent
types, since selection on expected growth is common to all acquirers.
Threats and mitigations: selection on growth (pre-trends, constraint
splits); accounting artefacts after group inclusion (EBIT before
appropriations, intra-group items treated as mechanisms); attrition through
merger into the parent (tracked, reported by parent type, Lee bounds);
placebo on withdrawn deals and randomised event dates. With about 6,000
treated firms the minimum detectable effect on employment growth is around
1–1.5 percentage points.

**Three-month scope.** MVP: Erel et al. replication, PE versus non-PE.
Extension: four parent types, constraint heterogeneity, mechanism tables.
Main failure mode: low match rate. Fallback: Serrano-only ownership-change
study.

**References.** Bernstein, Shai, Josh Lerner, and Filippo Mezzanotti, 2019, Private equity and financial fragility during the crisis, *Review of Financial Studies* 32, 1309–1373. · Boucly, Quentin, David Sraer, and David Thesmar, 2011, Growth LBOs, *Journal of Financial Economics* 102, 432–453. · Callaway, Brantly, and Pedro H. C. Sant'Anna, 2021, Difference-in-differences with multiple time periods, *Journal of Econometrics* 225, 200–230. · Cohn, Jonathan B., Edith S. Hotchkiss, and Erin M. Towery, 2022, Sources of value creation in private equity buyouts of private firms, *Review of Finance* 26, 257–285. · Eliason, Paul J., Benjamin Heebsh, Ryan C. McDevitt, and James W. Roberts, 2020, How acquisitions affect firm behavior and performance: Evidence from the dialysis industry, *Quarterly Journal of Economics* 135, 221–267. · Erel, Isil, Yeejin Jang, and Michael S. Weisbach, 2015, Do acquisitions relieve target firms' financial constraints?, *Journal of Finance* 70, 289–328. · Olsson, Martin, and Joacim Tåg, 2025, What is the cost of privatization for workers?, *Journal of Finance* 80, 2107–2151. · Kärnä, Anders, and Samantha Myers, 2025, Plundered or profitably pumped-up? The effects of private equity takeover, *Economics Letters* 247, 112054 (non-core, positioning).

---

## Topic 2: Powerless? Corporate Liquidity and the 2022 Electricity Shock in Southern Sweden

**Tentative research question.** *When electricity prices in bidding zones
SE3 and SE4 rose to more than twice the level in SE1 and SE2 during 2022,
did cash buffers and credit access determine which private firms cut
investment and employment, and did the 2023 electricity support to firms
act as constraint relief or as a cash windfall?*

Sweden has four bidding zones since 2011. Nord Pool annual averages were
63 and 66 öre per kWh in SE1 and SE2 but 137 and 162 öre in SE3 and SE4 in
2022, against 43, 43, 67 and 82 öre in 2021 and 46, 46, 59 and 80 öre in
2023. In 2023 the government paid support to firms only in SE3 (50 öre per
kWh) and SE4 (79 öre per kWh) on consumption between October 2021 and
September 2022, capped at SEK 20 million per group (SFS 2023:233). In the
financing-frictions view, firms with thin cash and credit cannot smooth a
transitory cost shock and cut investment and jobs, and a later cash
injection restores investment in constrained firms. In the pass-through
view, effects scale with electricity intensity regardless of balance sheets
and a windfall raises cash and dividends rather than investment (Blanchard,
López-de-Silanes, and Shleifer, 1994). A null on the constraint interaction
is informative: the shock was absorbed through prices, not balance sheets,
and the support was a transfer.

**Closest literature and contribution.** Bartram, Hou, and Kim (2022, JFE)
show with California's cap-and-trade programme that financially constrained
firms shift activity out of the regulated region while unconstrained firms
do not; we replicate the regional-shock-by-constraint design with bidding
zones as the regional variation and extend it to a market price shock, the
full population of private SMEs, and a subsequent cash injection. Brown,
Gustafson, and Ivanov (2021, JF) show that firms hit by severe weather draw
on credit lines while constrained firms without lines cut investment; we
replicate the logic that responses to transitory cash-flow shocks reveal
financing frictions. Blanchard, López-de-Silanes, and Shleifer (1994, JFE)
find that cash windfalls unrelated to opportunities are retained or paid
out; we use the 2023 support as a windfall test. Colmer, Martin, Muûls,
and Wagner (2024, REStud), Ivanov, Kruttli, and Watugala (2024, RFS) and
Känzig (2021, AER) anchor firm-level and macro identification of energy
cost shocks; Almeida, Campello, and Weisbach (2004, JF) provide the
constraint measure. Bălașa and Pollitt (2026, working paper) study Swedish
zonal prices descriptively and call for firm-level evidence. Our
contribution is threefold: a firm-level exposure measure built from
monthly zone prices and industry electricity intensity for about 100,000
firms; a test of financing frictions against pass-through with a placebo
in the untreated north; and the first evaluation of the 2023 support to
firms, whose design is under review as the bidding-zone configuration is
being reassessed [insert date of the Svenska kraftnät/ENTSO-E decision].
Benchmark: Bartram, Hou, and Kim (2022) find output shifts concentrated in
constrained firms; with our sample the minimum detectable difference in
investment between constrained and unconstrained firms is below one
percentage point of assets.

**Data and feasibility.** Serrano 2015–2024 for all Swedish limited
companies (municipality of registered office and establishment count to
confirm at first login); Nord Pool monthly zone prices; SCB electricity
use per unit of value added by industry; municipality-to-zone mapping.
Sample: single-unit private firms with at least five employees outside
groups, about 100,000 firms. Outcomes: cash, net debt, trade payables,
interest coverage, dividends, shareholder contributions, investment,
employment, exit. Support amounts are tax-secret at the firm level, so the
windfall test uses SE4 versus SE3 intensity in 2023–2024. Fallback:
Retriever postal addresses, or an industry-intensity design without zones.

**Empirical method.** Event-study difference-in-differences with firm,
industry-by-year and municipality fixed effects; treatment is continuous
exposure, zone price times industry electricity intensity, interacted with
year indicators 2016–2024 and with pre-determined constraint measures
(cash, leverage, age at 2020). Identification: within industry and year,
southern firms faced higher input prices set by interconnector capacity and
continental gas prices. Threats and mitigations: registered office versus
plant (single-unit firms); unobserved hedging (intention-to-treat;
heterogeneity by 2022 gross-margin change); SE4 structural differences
(continuous exposure, border municipalities); rate hikes interacting with
leverage (run the constraint interaction as a placebo in SE1/SE2); the gap
opened mid-2021 and closed in late 2022 (monthly prices). Power is ample
with 100,000 firms; errors clustered by municipality.

**Three-month scope.** MVP: zone-by-intensity event study with constraint
heterogeneity. Extension: balance-sheet transmission and the 2023 windfall
chapter. Main failure mode: no reliable firm location.

**References.** Almeida, Heitor, Murillo Campello, and Michael S. Weisbach, 2004, The cash flow sensitivity of cash, *Journal of Finance* 59, 1777–1804. · Bartram, Söhnke M., Kewei Hou, and Sehoon Kim, 2022, Real effects of climate policy: Financial constraints and spillovers, *Journal of Financial Economics* 143, 668–696. · Blanchard, Olivier Jean, Florencio López-de-Silanes, and Andrei Shleifer, 1994, What do firms do with cash windfalls?, *Journal of Financial Economics* 36, 337–360. · Brown, James R., Matthew T. Gustafson, and Ivan T. Ivanov, 2021, Weathering cash flow shocks, *Journal of Finance* 76, 1731–1772. · Colmer, Jonathan, Ralf Martin, Mirabelle Muûls, and Ulrich J. Wagner, 2024, Does pricing carbon mitigate climate change? Firm-level evidence from the European Union emissions trading system, *Review of Economic Studies* 92, 1625–1660. · Ivanov, Ivan T., Mathias S. Kruttli, and Sumudu W. Watugala, 2024, Banking on carbon: Corporate lending and cap-and-trade policy, *Review of Financial Studies* 37, 1640–1684. · Känzig, Diego R., 2021, The macroeconomic effects of oil supply news: Evidence from OPEC announcements, *American Economic Review* 111, 1092–1125.
