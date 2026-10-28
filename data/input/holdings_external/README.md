# holdings_external: full portfolio holdings for 11 PPM funds that do not report to Finansinspektionen

Built 2026-10-27 from the fund companies' own published documents (annual and
semi-annual reports, monthly reports, fund web pages), with the Wayback Machine
used to recover web pages and files as they stood at the time. One file:
`holdings_external.csv`, one row per instrument per fund per requested as-of date
(753 rows). Columns: fund, isin_fund, as_of_requested, as_of_actual,
instrument_name, instrument_isin (always blank: none of the sources print ISINs),
weight_pct, market_value, currency, source_url, retrieved_at.

Conventions
- `as_of_requested` is the month-end asked for; `as_of_actual` is the date of the
  document actually used. When the exact month-end is not published, the nearest
  published full-holdings date BEFORE the requested date is used, so both
  requested dates can map to the same document.
- `weight_pct` is the weight in per cent of fund net assets as printed by the
  source. `market_value` is in the currency given in `currency` (the reporting
  currency of the document, not the instrument's trading currency). Odin,
  Delphi and DNB report in NOK; the Odin and Storebrand reports print NOK 1000
  and have been multiplied by 1000. C WorldWide, Danske Invest and Evli report
  in SEK. Holberg and SEB rows have weights only (no market values published).
- Cash rows are kept where the source lists them (Odin Norden "CASH").
- Instrument names are exactly as printed by the source (so the same stock can be
  spelled differently across funds, e.g. "Atlas Copco A", "Atlas Copco AB ser. B").
- Sources marked "last resort" below are not fund-company documents.

## Per fund

### C WorldWide Sweden 1A (LU0424681269)  -- FULL on both dates
- 2025-07-31 -> 2025-06-30: 30 holdings (96.39 % of NAV, rest cash). C WorldWide
  semi-annual report 30 June 2025, "Securities portfolio", SEK.
  https://cww.lu/media/5ccpzdde/docrep-o00001790-00000000-0000-2025-06-30-sr-en-0000.pdf
  (link recovered from the Wayback copy of https://cww.lu/downloads/semi-annual-reports/
  dated 2025-11-06; the PDF is still live on cww.lu).
- 2025-12-31 -> 2025-12-31: 31 holdings (97.51 %). C WorldWide annual report
  31 December 2025. https://www.cww.lu/media/5aipz1pl/cww-fcp-signed-annual-report-31122025.pdf
- Monthly fact sheets on cww.lu give top 10 only; not used.

### C WorldWide Sweden Small Cap 1A (LU0424682077)  -- FULL on both dates
- 2026-04-30 -> 2025-12-31: 26 holdings (97.97 %). Annual report 31 Dec 2025 (same
  PDF as above). Nothing is published between 31 Dec 2025 and 30 Jun 2026.
- 2026-08-31 -> 2026-06-30: 26 holdings (97.89 %). C WorldWide semi-annual report
  30 June 2026. https://www.cww.lu/media/5ccpzdde/c-worldwide-sar2026.pdf
- The 30 June 2025 semi-annual also has this fund (27 holdings) but it is not
  needed for the requested dates.

### Danske Invest SICAV Sverige SI (LU1349495116)  -- FULL on both dates
- 2025-07-31 -> 2025-06-30: 28 holdings (99.95 %). Danske Invest SICAV unaudited
  semi-annual report 30 June 2025, "Sverige - Statement of Investments", SEK.
  https://www.danskeinvest.lu/docs/diluen_semi-annual-report_danske_invest_sicav_2025.pdf
- 2025-12-31 -> 2025-12-31: 28 holdings (100.14 %). Danske Invest SICAV annual
  report 31 Dec 2025. https://www.danskeinvest.lu/docs/diluen_annualreport_2025_sicav.pdf
- The figures are for the whole sub-fund (all share classes), as for every
  Luxembourg/Norwegian/Finnish report used here.

### Odin Sverige C (NO0008000023)  -- FULL on both dates
- 2025-07-31 -> 2025-06-30: 30 holdings (98.4 %). Odin semi-annual report 2025,
  "ODIN Sverige - Portfolio Composition as of 30/06/2025", NOK (NOK 1000 x 1000).
  https://odinfond.no/wp-content/uploads/2025/09/EN-Semi-Annual-Report-2025-FINAL.pdf
- 2025-12-31 -> 2025-12-31: 27 holdings (98.7 %). Odin annual report 2025,
  "Portfolio Composition as at 31/12/2025".
  https://odinfond.no/wp-content/uploads/2026/04/en_annual_report_2025_eur_Odin_mutual-funds-1.pdf
- Odin's fund pages (odinfonder.se / odinfond.no) show the full portfolio with
  weights and NOK market values updated monthly; Wayback copies of the Sverige
  page exist for 2025-07-07 (30.06.2025) and 2026-01-15 (31.12.2025), i.e. the
  same dates as the reports, so the reports were used.

### SEB Sweden Equity Fund C (LU0047322432)  -- TOP 25 ONLY (not full), one date
- 2025-07-31 -> 2025-06-30 and 2025-10-31 -> 2025-06-30: the 25 largest holdings
  (88.8 % of NAV; the fund had 37 holdings) as shown on Nordnet's fund page
  ("Exponering uppdaterad 2025-06-30", data from Morningstar), Wayback copy
  2025-07-16. LAST RESORT, not a fund-company document.
  http://web.archive.org/web/20250716075618/https://www.nordnet.se/fonder/lista/seb-sweden-equity-c-sek-41c6c381
  Cross-check: Pensionsmyndigheten's fund page (Wayback 2025-07-12) shows the same
  top 10 for "Innehav 2025-06-30" (Investor 9.7, Volvo 7.8, Swedbank 6.3, Hexagon
  5.3, Atlas Copco 4.9, Nordea 4.9, AstraZeneca 4.7, SEB 4.3, Beijer Ref 3.7,
  Epiroc 3.4).
- Not found: the full SEB Fund 1 (Luxembourg) semi-annual report 30 June 2025 /
  annual report 31 Dec 2025 with the SEB Sweden Equity Fund schedule of
  investments. Tried: sebgroup.com SEB Funds AB "legal information" page (only
  the management company's own annual reports, e.g.
  https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/1E8D570B7871010BC1258DD8002AFBE2/$FILE/SEB_Funds_AB_Annual_Report_2025_ENG.pdf,
  no fund holdings); sebgroup.lu fund pages (gated, no document links);
  seb.se/fondbolaget (redirects, no links); swissfunddata.ch SEB Fund 1 semi-annual
  30 June 2025 (https://swissfunddata.ch/sfdpub/docs/sar-200464-20250901-en.pdf,
  Swiss-registered sub-funds only, Sweden Equity not included); factsheetslive.com
  SEB Fund 1 annual report 31 Dec 2025 and semi-annual 30 June 2026 (German-
  registered sub-funds only, Sweden Equity not included); Avanza and Nordnet
  document links (KID only); Morningstar and FT holdings pages (blocked).
  No Wayback copy of any distributor page exists between 2025-07-16 and
  2026-01-19 (the 2026-01-19 Nordnet copy is as of 2025-12-31, after the second
  requested date), so 2025-06-30 is the nearest available date for both.

### Evli Sverige Aktieindex B (FI4000058821)  -- FULL, one document for both dates
- 2025-07-31 -> 2024-12-30 and 2025-11-30 -> 2024-12-30: 29 holdings (96.78 %;
  OMXS30 future with zero value dropped). Evli mutual funds annual report 2024,
  "Evli Sweden Equity Index Fund - Portfolio report 30.12.2024", SEK; recovered
  from the Wayback copy (2025-08-10) of the annual-report URL, which Evli
  overwrites every year.
  http://web.archive.org/web/20250810014002/https://content.evli.com/fund/pdf/Annual_report_and_financial_statements_Evli_mutual_funds.pdf
- Not found: the semi-annual review 30 June 2025 (Evli overwrites
  Semi_annual_review_Evli_mutual_funds.pdf each year; no Wayback copy; Finnish and
  Swedish file-name variants return 404) and any monthly full-holdings list (the
  monthly report has top 10 only). The annual report 2025 (30.12.2025, live URL
  https://content.evli.com/fund/pdf/Annual_report_and_financial_statements_Evli_mutual_funds.pdf)
  has full holdings but is after both requested dates and is not in the CSV.
  The fund was renamed Evli Atlas Sweden Enhanced Index on 2026-09-28.

### Evli Sverige Smabolag (FI0008813142)  -- FULL, one document for both dates
- 2026-04-30 -> 2025-12-30 and 2026-08-31 -> 2025-12-30: 39 holdings (96.47 %).
  Evli mutual funds annual report 2025, "Evli Swedish Small Cap Fund - Portfolio
  report 30.12.2025", SEK (weights as printed).
  https://content.evli.com/fund/pdf/Annual_report_and_financial_statements_Evli_mutual_funds.pdf
- Not found: full holdings at 30 June 2026. Evli's semi-annual review 2026
  (https://content.evli.com/fund/pdf/Semi_annual_review_Evli_mutual_funds.pdf)
  contains only portfolio structure and the 10 largest investments for this fund,
  and the monthly report likewise top 10.

### Odin Norden C (NO0008000155)  -- FULL on both dates (exact for the first)
- 2025-01-31 -> 2025-01-31: 41 holdings + cash (100.0 %). Odin's own fund page
  "Full portefolje 31.01.2025" (weights and NOK market values), Wayback copy
  2025-02-12. http://web.archive.org/web/20250212194051/https://odinfond.no/fond/odin-norden-c-nok/
- 2025-05-31 -> 2025-03-31: 41 holdings + cash (100.0 %). Same page, "Full
  portefolje 31.03.2025", Wayback copy 2025-04-26.
  http://web.archive.org/web/20250426074908/https://odinfond.no/fond/odin-norden-c-nok/
  No Wayback copy shows 30.04.2025 or 31.05.2025; the next copy (2025-08-06) is
  30.06.2025, which is also in the Odin semi-annual report 2025.
- Odin annual report 2024 (31.12.2024) also has the full portfolio; not needed.

### DNB Gront Skifte Norden S (NO0010875438)  -- FULL, one document for both dates
- 2025-01-31 -> 2024-12-31 and 2025-05-31 -> 2024-12-31: 66 holdings (99.18 %).
  DNB Asset Management "Aarsrapport for fondene 2024", DNB Gront Skifte Norden,
  Note 7 Verdipapirportefolje, NOK (whole fund, all share classes).
  https://s3.eu-north-1.amazonaws.com/dnb-asset-management/legal-documents/ANNUALREPORT-NO-NO-NO0010337421_2025-08-07-130354_srut.pdf
  (linked as "Aarsrapport 2024 for DNB Asset Managements norskregistrerte fond" on
  https://dnbam.com/vare-fond/juridiske-dokumenter).
- Not found: a monthly full-holdings list for Jan-May 2025. DNB publishes a
  monthly "Fondbeholdning" PDF (https://documents.anevis-solutions.com/dnb/FUNDHOLDINGS-NO-NO-NO0010102866.pdf,
  full list with weights) but only the current month; the only Wayback copy is
  2025-08-19. The half-year report 2025 (30.06.2025) is after the second date.
  Pensionsmyndigheten's page (Wayback 2025-06-19) has top 10 at 2025-03-31 only.

### Holberg Norden (NO0010072945)  -- FULL on one date, TOP 20 on the other
- 2025-01-31 -> 2024-12-31: 23 holdings = the whole portfolio (98.7 %, rest cash),
  weights only. Holberg monthly report December 2024, "Nokkeltall for fondets
  investeringer".
  https://cdn.prod.website-files.com/6448e908ec910c7805ca1aa7/677d12ad12e90791920de8e5_M%C3%A5nedsrapport%20Holberg%20Norden%20-%20Desember%202024.pdf
  The January 2025 monthly report could not be located (Holberg's CDN file names
  carry an unguessable hash; search engines and the Wayback CDX index only
  return the December 2024, February 2025, May 2025 and June 2025 reports).
- 2025-05-31 -> 2025-05-31: TOP 20 only (91.8 %), weights only. Holberg monthly
  report May 2025, "Nokkeltall for fondets storste investeringer" (from 2025 the
  table is limited to the 20 largest).
  https://cdn.prod.website-files.com/6448e908ec910c7805ca1aa7/684009537e72beb4e7c84351_M%C3%A5nedsrapport%20Holberg%20Norden%20-%20Mai%202025.pdf
- Holberg's annual report 2024 / half-year report 2025 were not found online
  (holberg.no fund page links only prospectus, KID and the latest monthly report).

### Delphi Nordic (NO0010039670)  -- FULL, one document for both dates
- 2025-01-31 -> 2024-12-31 and 2025-05-31 -> 2024-12-31: 41 holdings (98.50 %).
  Storebrand Asset Management "Aarsrapport 2024, Verdipapirfond forvaltet av
  Storebrand Asset Management AS", Delphi Nordic Portefoljeoversikt 31.12.2024,
  NOK (NOK 1000 x 1000).
  https://www.storebrandam.com/globalassets/storebrand-asset-management/documents/reports/annual-reports-mutual-funds-norwegian/arsrapport-for-verdipapirfondene-2024.pdf
- Not found: monthly full holdings for Jan-May 2025. Storebrand's monthly fund
  report (api.storebrand.no ... documentType=MONTHLY_FUND_REPORT) lists only the
  10 largest holdings; the storebrand.no fund page shows the full list but only
  for the current month and has no Wayback copies; storebrandam.com and
  delphifunds.com are gated behind a country/investor selector. The half-year
  report 2025 (30.06.2025) is after the second date.

## Summary
Funds with full holdings at two distinct dates: 5 (C WorldWide Sweden, C WorldWide
Sweden Small Cap, Danske Invest Sverige, Odin Sverige, Odin Norden). Funds with
full holdings from one document that is the nearest date before both requested
dates: 4 (DNB Gront Skifte Norden, Delphi Nordic, Evli Sverige Aktieindex, Evli
Sverige Smabolag). Full on one date and top 20 on the other: 1 (Holberg Norden).
Top 25 only, from a distributor page: 1 (SEB Sweden Equity Fund). Nothing: 0.

Documents downloaded during the build (not kept in the repo): Danske Invest
SICAV AR 2025 and SAR 2025; C WorldWide AR 2025, SAR 2025, SAR 2026; Odin AR 2024,
AR 2025, SAR 2025; Storebrand fund AR 2024; DNB fund AR 2024 and AR 2025 (fund
level); Evli AR 2024 (Wayback), AR 2025, SAR 2026; Holberg Norden monthly reports
Dec 2024, Feb 2025, May 2025, Sep 2026; SEB Fund 1 reports from swissfunddata and
factsheetslive (no Sweden Equity sub-fund). All were parsed with pdftotext
-layout and regular expressions; parsed totals were checked against the
"Total" lines of each report.
