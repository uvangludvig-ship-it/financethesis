**FTN anchor: evidence of data availability, checked 4 October 2026**

I ignored the previous anchor’s `data/` directory. All data inspected here were newly downloaded from official public sources into [sources/](sources/). This audit verifies source files and a limited historical match, not an estimated thesis result or complete panel.

**Availability verdict**

| Required ingredient | Evidence obtained | Status |
|---|---|---|
| FTN award dates and selected funds | Official procurement reports; first Europe report downloaded and read | Public and verified |
| Admission/implementation context | Pensionsmyndigheten’s implementation page | Public; exact fund-level transfer dates still need their own event records |
| PPM identifiers, holdings, returns and fees | June/August 2026 and December 2023/March–June 2024 workbooks downloaded and parsed | Public and verified; schema and precision vary by vintage |
| Daily historical fund prices | 2024 annual workbook downloaded and parsed | Public and verified for PPM funds; raw prices are not distribution-adjusted |
| Total fund assets | FI quarterly XML archives for 2023Q4, 2024Q1, 2024Q2 and 2026Q2 downloaded and parsed | Public and verified for Swedish UCITS; not the full international fund universe |
| Broad monthly assets and estimated flows | SHoF Morningstar catalogue and field definitions inspected | Dataset exists; group’s licensed access, historical completeness and usable export not verified |
| Exact original Cookson UK platform data | Paper/FCA documentation inspected | Confidential; no open replication dataset established |
| Complete qualified-loser identities and scores | First public FTN report checked | Counts are public; complete identity/score information needed for the preferred comparison is not established |

**The public files genuinely join**

The downloaded 2026Q2 FI archive contains 726 XML files, 677 with a reported fund-asset value. The June PPM workbook contains 374 six-digit fund records in `Fondstatistik`. An exact unique ISIN match joins 179 of those records to FI, including 25 marked procured by PPM. This is a conservative mechanical match, not comprehensive parent-fund coverage. Both the unmatched records and multiple share classes require further investigation. [FI archive index](https://www.fi.se/sv/vara-register/fondinnehav-per-kvartal/); [PPM monthly statistics](https://www.pensionsmyndigheten.se/statistik-och-rapporter/statistik/statistik-for-premiepension).

Two concrete observations on 30 June 2026 are:

| Fund | ISIN | FI total assets, SEK | PPM assets, SEK | Workbook locations |
|---|---|---:|---:|---|
| AMF Aktiefond Europa | SE0000739153 | 13,935,664,326 | 6,447,324,644 | `Fondstatistik` row 52; `Fondval & marknadsvärde` row 72 |
| Swedbank Robur Europafond A | SE0000539454 | 9,977,188,083 | 1,222,753,970 | `Fondstatistik` row 167; `Fondval & marknadsvärde` row 153 |

Values are rounded to SEK here; full cached precision and archive member names are in [public_data_audit.json](public_data_audit.json). The difference between total and PPM assets is an outside-PPM **asset stock**, not a net flow. For Swedbank, the PPM label is a share class while FI reports the parent fund: do not use that class’s return as the whole portfolio return without reconciliation.

FI’s `UtanAndelsklasser` flag identifies 65 of the matched records as funds reported without share classes. Only **seven** of those are marked procured in the June snapshot. That is a useful clean subset for measurement checks, but too small to assert adequate statistical power. The flag must be checked in each historical period; neither current status nor current fund names establish historical comparability.

**Historical availability was tested, not just assumed from a download menu**

For AMF Aktiefond Europa, an actual winner in the first Europe procurement, the same ISIN matches before and after the 25 March 2024 award:

| Reporting date | FI fund assets, SEK | PPM assets, SEK | Historical PPM amount row |
|---|---:|---:|---:|
| 31 December 2023 | 7,891,537,544 | 3,215,319,747 | 86 |
| 31 March 2024 | 8,388,903,071 | 3,477,181,392 | 87 |
| 30 June 2024 | 8,511,620,198 | 3,522,959,982 | 264 |

The 2024 price workbook supplies 251 price observations for that PPM number. Its last observations before the first two quarter ends are 28 March, NAV SEK 349.06, and 28 June, NAV SEK 353.67. These are file-level checks, not estimates of a reform effect. A three-date, one-fund check cannot establish full panel availability or identification. [Machine-readable historical probe](historical_public_probe.json); [historical PPM workbook archive](https://www.pensionsmyndigheten.se/statistik-och-rapporter/statistik/statistik-for-premiepension/aldre-manadsstatistik-premiepension).

There is an important parsing trap: the ISIN field is column R in these 2023–2024 workbooks and column S in June 2026. The older displayed/cached return fields can also be heavily rounded. A production pipeline must use header mappings and precise underlying NAV/total-return data, not hard-coded 2026 column positions or rounded three-month returns.

**How outside flows could be constructed**

Let total portfolio assets be A, the sum of all PPM holdings in that portfolio be P, and outside assets be O = A − P, in the same currency and at the same valuation date. For a verified single-class, accumulating portfolio with return R, a conventional residual estimate is:

    estimated outside flow_t = O_t − O_(t−1) × (1 + R_t)

This is an approximation to flow based on period-end stocks. Within-period transaction timing, distributions, mergers and valuation-date differences matter. For multiple classes, use properly aggregated class-specific assets and returns or a reliable parent-level estimated-flow series. Do not assume all classes have the PPM class’s fee, currency or net return.

A second route subtracts PPM flows in currency units from a same-scope provider estimate of total fund flows. This requires understanding the PPM `Handel, netto` field’s interval and transaction scope. Its heading and values are present in the downloaded files, but the inspected `Beskrivning av mått` sheet does not define that scope. The review has therefore **not certified this as a complete observed PPM net-subscription measure**. Reconcile it against holdings, returns and known transactions before using the subtraction. Mixed observed/estimated components can generate spurious outside flows during large administrative transfers.

PPM assets include valuation effects. Changes in the number of savers are not subscriptions in SEK. Fee rebates and reinvestments must be handled consistently. FI management fees and PPM TER are different measures; a difference between them is not automatically the procurement discount. Outside-PPM assets can include institutions, foreign investors, other pension arrangements and insurance wrappers. The defensible label is **outside-PPM capital**, not “Swedish private retail savings.”

**The preferred licensed route is documented**

An additional public check downloaded SHoF’s [fund identity master](https://www.houseoffinance.se/globalassets/shof/data-center/shof-fund-data-morningstar/fundmaster.zip). It maps AMF Europa’s ISIN to `secid F0GBR04K9U`, `fundid FSGBR05332` and `performanceid 0P00000K17`. This confirms a concrete bridge from the public PPM/FI observation into Morningstar identifiers. The master’s snapshot assets and trailing returns do not supply the required historical monthly panel. The valuations access page did not expose usable data in this session. [Reproducible identity check](shof_master_probe.json).

SHoF advertises historical Morningstar coverage of over 9,000 funds available for sale in the Nordic countries. Its eligibility statement includes students whose institution has a Morningstar Direct subscription. That is more useful than assuming that a terminal restriction on one Morningstar product applies to every SHoF dataset, but it still does not prove this group has working access. [SHoF dataset and access terms](https://www.houseoffinance.se/data-center/shof-fund-data-morningstar/).

The downloaded [field definitions](sources/shof_field_definitions.pdf) distinguish `secid`, `fundid` and `performanceid`, class/fund assets (`tnaclass`, `tnafund`) and class/fund estimated net flows (`netflowclass`, `netflowfund`). A parent-fund value can repeat across share-class rows; summing it would double-count. Currency and valuation timing must be harmonized. A “daily” field listing does not guarantee genuinely daily reporting for every fund. The source definitions describe net flows as estimates derived from assets and returns, not a transaction register.

Before adopting the monthly design, export the identity master, asset/flow histories, distribution-adjusted returns and relevant fees for selected and comparison funds. Check dead funds, reporting gaps, suspicious repeated values, all PPM share classes and parent-level scope. Compare at least two early procurements and reconcile a known transfer. Freeze the sample on measurement and eligibility criteria before looking at treatment estimates.

**The event calendar limits what is estimable today**

The live FTN page lists the following award cohorts as of this review. Search-engine snippets were older than the live page, so the live chronology is used. [FTN reports](https://www.ftn.se/marknadsdialog/upphandlingsrapporter.html).

| Award date | Categories | Admission month/status reported by PPM |
|---|---|---|
| 25 March 2024 | Europe active | June 2024 |
| 31 October 2024 | Europe index; global index | February 2025; March 2025 |
| 19 February 2025 | Nordic large/mid; Nordic small | April 2025 |
| 27 August 2025 | Sweden active; Sweden passive | December 2025; October 2025 |
| 24 February 2026 | Global active | Reported under appeal, awaiting decision |
| 28 May 2026 | Europe small; Sweden small | July 2026; August 2026 |
| 22 September 2026 | Global technology active | Do not infer implementation from the award |

Admission information comes from [Pensionsmyndigheten](https://www.pensionsmyndigheten.se/forsta-din-pension/valj-och-byt-fonder/upphandlat-fondtorg). These months are not verified actual transfer dates. Build a separate event ledger for notifications and transfers. Technology has no post-award observation in the latest August monthly file downloaded here. The eleven categories occur on seven award dates; the 2024–2025 core has seven categories on four dates. Correlated decisions and short follow-up must enter the power assessment.

**What the audit establishes**

The public institutional and measurement inputs exist and can be joined; historical matching works for a real selected fund. A narrow public-only quarterly analysis is technically plausible subject to return and scope checks. The broader monthly outside-flow design has a credible documented data source, but access and coverage remain unverified. No candidate should be advertised as fully data-safe until those distinctions are resolved. This is the specific remaining constraint on the recommended anchor, rather than a vague request to “find data later.”
