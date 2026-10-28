# OMXS30 index-change event list, Jan 2005 to Oct 2026: notes

Companion to `omxs30_changes_2005_2026.csv` (48 event rows). Built 11 Oct 2026 for a Greenwood and Sammon (2025, JF, "The Disappearing Index Effect") style replication on the Swedish OMXS30.

## 1. What is in the CSV

48 rows = 24 additions + 24 deletions.

| Verification | Rows | Meaning |
|---|---|---|
| VERIFIED | 27 | Nasdaq / NASDAQ OMX press release or exchange notice read directly (ir.nasdaq.com, GlobeNewswire, view.news.eu.nasdaq.com, nasdaq.com, or a verbatim Mondo Visione / finanznachrichten reproduction of the release) |
| SECONDARY | 19 | Swedish press (SvD, DI, Privata Affarer, Affarsvarlden, Realtid, Placera), sv.wikipedia's sourced change table, or thesis appendices built from Nasdaq data |
| UNVERIFIED | 2 | Skandia out / Old Mutual in (early 2006 merger replacement): inferred, dates left blank |

Events by effective year: 2006: 4 (+2 undated 2006 merger rows), 2007: 4, 2008: 2, 2009: 4, 2014: 2, 2016: 2, 2017: 3, 2018: 3, 2021: 4, 2022: 3, 2023: 1, 2024: 2, 2025: 12. Zero events in 2005, 2010, 2011, 2012, 2013, 2015, 2019, 2020, and (so far) 2026.

Columns: event_id, effective_date (first trading day the new composition applies), announcement_date (date of the Nasdaq release or, when only press is available, the press report date), company, ticker (Nasdaq Stockholm short name), isin (only where I am confident of the ISIN valid at the event; otherwise blank), type, reason, review_cycle, source_url, source_type, verification, notes.

Reason categories used: semi-annual review (36 rows), merger / acquisition (Skandia 2006, Swedish Match 2022), merger replacement (Old Mutual 2006), delisting after takeover (Scania 2014), liquidation (Vostok Gas 2009), spin-off (Essity 2017). For a G&S-style sample of review-driven changes, drop E001, E002, E013, E017, E023, E033 (6 rows), leaving 42 review-driven events (21 additions, 21 deletions, of which 12 + 12 come from the single July 2025 methodology reset).

## 2. Review register (every semi-annual review 2005 to 2026)

"No change (V)" = a Nasdaq release stating no change was read. "No change (inferred)" = no release found, but verified constituent lists before and after are identical (or two independent thesis event lists built from Nasdaq data show nothing).

| Effective | Announced | Outcome | Lead (trading days) | Evidence |
|---|---|---|---|---|
| 2005-01-03 | ? | No change (inferred) | | Norin & Parksjo 2013 (Nasdaq OMX lists 1987-2012) and Frantzich & Nilson 2024 list no 2004-05 events |
| 2005-07-01 | ? | No change (inferred) | | same |
| 2006-01-02 | ? | No change (inferred; SSE thesis shows "Fabege 03/01/2006", see below) | | same |
| 2006-07-03 | 2006-06-30? / 06-03? | Boliden, Vostok Nafta in; Fabege, Old Mutual out | approx 1 | sv.wikipedia (DI 2006-06-30), theses |
| 2007-01-02 | 2006-12-27 | Scania B in; Holmen B out | 2 to 3 | SvD 2006-12-27 |
| 2007-07-02 | 2007-06-26 | SSAB A in; Stora Enso R out | 4 | Frantzich & Nilson; DI 2007-06-29 |
| 2008-01-02 | 2007-12-06 | Lundin Petroleum in; Autoliv out | 17 | Privata Affarer 2007-12-06 |
| 2008-07-01 | ? | No change (inferred) | | list reconciliation Jan 2008 to Jan 2009 |
| 2009-01-02 | 2008-12-22 | Vostok Gas out (liquidation), no replacement | 6 | SvD 2008-12-22 |
| 2009-07-01 | 2009-06-03 | Getinge B, MTG B in; Eniro out | 20 | NASDAQ OMX release (V) |
| 2010-01-04 | 2009-12-02 | No change (V) | 22 | ir.nasdaq.com |
| 2010-07-01 | ? | No change (inferred) | | Jan 2010 list = Jan 2011 list |
| 2011-01-03 | 2010-12-02 | No change (V) | 20 | GlobeNewswire / EQS |
| 2011-07-01 | 2011-06-07 | No change (V) | 17 | ir.nasdaq.com |
| 2012-01-02 | ? | No change (inferred) | | Jan 2011 list = Jan 2014 list |
| 2012-07-02 | ? | No change (inferred) | | same |
| 2013-01-02 | ? | No change (inferred) | | same |
| 2013-07-01 | ? | No change (inferred) | | same |
| 2014-01-02 | 2013-12-05 | No change (V) | 18 | EQS reproduction |
| (2014-06-05) | 2014-05-21 | Scania B out (delisting) | 10 | Nasdaq delisting notice 79/14 |
| 2014-07-01 | 2014-06-05 | Kinnevik B in (no deletion) | 17 | Affarsvarlden, thesis |
| 2015-01-02 | 2014-12-04 | No change (V) | 18 | GlobeNewswire |
| 2015-07-01 | ? | No change (inferred) | | Jan 2015 list minus MTG plus Fingerprint = Jul 2016 list |
| 2016-01-04 | 2015-12-04 | Fingerprint B in; MTG B out | 20 | Nasdaq release (V, Mondo Visione) |
| 2016-07-01 | 2016-06-13 | No change (V) | 13 | Markets Media reproduction |
| 2017-01-02 | 2016-12-07 | Autoliv in; Nokia out | 17 | GlobeNewswire (V) |
| (2017-06-12) | 2017-06-09 | Essity B in (spin-off, extra constituent) | 1 | Nasdaq release footnote (V) |
| 2017-07-03 | 2017-06-09 | No change (V) | 16 | GlobeNewswire |
| 2018-01-02 | 2017-12-07 | Lundin Petroleum out (no addition) | 16 | DI 2017-12-07 |
| 2018-07-02 | 2018-06-07 | Hexagon B in; Fingerprint B out | 16 | Realtid, Placera |
| 2019-01-02 | 2018-12-07 | No change (V) | 15 | GlobeNewswire |
| 2019-07-01 | 2019-06-11 | No change (V) | 14 | view.news.eu.nasdaq.com |
| 2020-01-02 | ? | No change (inferred) | | Jul 2019 list = Jul 2020 list |
| 2020-07-01 | 2020-06-09 | No change (V) | 16 | finanznachrichten reproduction |
| 2021-01-04 | 2020-12-10 | Evolution in; SSAB A out | 15 | Nasdaq release (V) |
| 2021-07-01 | 2021-06-22 | Sinch in; Securitas B out | 7 | Privata Affarer / Direkt |
| 2022-01-03 | 2021-12-22 | No change (V) | 6 | view.news.eu.nasdaq.com |
| 2022-07-01 | 2022-06-22 | SBB B in; Skanska B out | 7 | Nasdaq release (V, Mondo Visione) |
| (2022-11-18) | 2022-11-16 | Swedish Match out (PMI takeover) | 2 | Capital IQ item, DI |
| 2023-01-02 | 2022-12-22 | NIBE B in (no deletion) | 4 | nasdaq.com (V) |
| 2023-07-03 | ? | No change (inferred) | | Jan 2023 list = Jan 2024 list |
| 2024-01-02 | 2023-12-20 | No change (V) | 5 | finanznachrichten reproduction |
| 2024-07-01 | 2024-06-20 | Saab B in; Autoliv out | 7 | Nasdaq release (V) |
| 2025-01-02 | 2024-12-18 | No change (V) | 7 | Nasdaq release (V) |
| 2025-07-01 | 2025-06-23 | 6 in, 6 out (new methodology) | 6 | Nasdaq release (V) |
| 2025-12-01 | 2025-11-21 | No change (V) | 6 | Mondo Visione reproduction |
| 2026-06-01 | 2026-05-22 | No change (V) | 6 | Mondo Visione reproduction |
| 2026-12-01 | due 2026-11-20 | pending | 6 | per methodology |

Lead-time regimes visible in the data: (a) 2006 to mid-2007, 1 to 4 trading days; (b) Dec 2007 to 2020, roughly 3 to 4 weeks (announcement in the first ten days of June/December); (c) June 2021 to Dec 2024, roughly 1 to 2 weeks (announcement around the 18th to 22nd); (d) from June 2025, exactly 6 trading days by rule. Note for the replication: announcement and effective dates are almost never on the same day, but in regime (a) the gap is so short that announcement-window and effective-window returns overlap.

## 3. Index rules on review timing and announcement lead

### 3.1 Old regime (1986 to 30 June 2025): turnover-ranked "30 most traded"

Source: "Rules for the Construction and Maintenance of the OMX Stockholm 30 Index", version 1.5, 8 Dec 2014 (copy at https://docplayer.net/251049-Rules-for-the-construction-and-maintenance-of-the-omx-stockholm-30-index.html); the same substance appears in Nasdaq's 2025 consultation paper (https://indexes.nasdaqomx.com/docs/OMXS30%20Index%20Consultation.pdf).

- Selection: the 30 shares with the highest SEK turnover on Nasdaq Stockholm over a six-month Control Period "starting seven months before the review date", i.e. Dec to May for the July review and Jun to Nov for the January review. Data cut-off: last trading day of May / November.
- Buffer rule: an incumbent is removed only if it ranks outside the top 45 by turnover; a non-member enters only if it ranks within the top 15. Replacements pair the lowest-ranked incumbent with the highest-ranked outsider.
- Effective: "after the close of the last trading day of June and December", i.e. at the open of the first trading day of July / January.
- Announcement: section 6 of the rulebook: periodic composition changes are announced "no less than one (1) week prior to implementation"; corporate-action-driven changes "where possible no later than two business days before the ex-day". Rule amendments normally announced three months ahead.
- Between reviews: mergers/takeovers: removal the day after the shareholder vote or expected tender expiry (or on written consent) and the Index Calculator may decide on a replacement; bankruptcy: removal as soon as practicable; low liquidity exclusion needs Index Ombudsman approval with two trading days' notice. Fast entry for very large new listings (expected market value at least 5% of the index, high liquidity) as an extra share, normally on the second trading day of listing. Spin-offs: handled case by case (Essity 2017 was added as an extra 31st constituent; Epiroc 2018, Veoneer 2018, Electrolux Professional 2020 were not).
- Weighting: full market-cap weighting (no free-float adjustment, no cap), multiple share classes of one company allowed (Atlas Copco A and B both in).
- Practice versus rule: as the register above shows, Nasdaq announced 3 to 4 weeks ahead in 2008-2020 and 1 to 2 weeks ahead in 2021-2024; in 2006-2007 the lead was only days (consistent with the rule only having a one-week floor).

### 3.2 New methodology from 1 July 2025 (announced 5 May 2025 after a consultation that closed 28 Feb 2025)

Sources: Nasdaq release 5 May 2025 (https://view.news.eu.nasdaq.com/view?id=bcafef084bdc14cf1924ea6036b3d705a&lang=en); OMX Stockholm 30 Index Methodology (https://indexes.nasdaqomx.com/docs/Methodology_OMXS30.pdf), changelog entries 7/1/2025 and 12/1/2025; consultation follow-up on the schedule (https://indexes.nasdaqomx.com/docs/OMXS30%20Index%20Consultation%20Follow%20up_Final%202.pdf and ..._Summary_Of_Responses_And_Conclusion.pdf).

- Selection: eligible universe = OMXSPI constituents with 6-month average daily traded value of at least SEK 50m (the consultation proposed SEK 10m; final rule SEK 50m). Companies ranked by free-float market cap (all share classes combined for ranking). Top 20 selected outright; incumbents ranked 21 to 35 retained; remaining seats filled in rank order from the top 30. One security per company (incumbent class kept; otherwise the class with the highest 6-month ADVT). 15% single-name cap applied only at the semi-annual rebalance. Modified free-float cap weighting.
- Schedule in the first new-regime review (effective 1 Jul 2025): reference date last trading day of May; announcement after close on the sixth trading day prior (23 Jun 2025).
- Schedule from the second new-regime review: after the August 2025 consultation Nasdaq moved the reference dates to the last trading day of April and October, with the reconstitution and rebalance "effective at market open on the first trading day in June and December" and the announcement "after the close on the sixth trading day prior to the Reconstitution effective date" (methodology changelog dated 12/1/2025). Consequence: there was no January 2026 review; the cycle is now 1 Dec 2025, 1 Jun 2026, 1 Dec 2026, and so on, aligned with OMXSB.
- Between reviews: removed securities "are not replaced" except in certain merger situations (Corporate Actions and Events Manual); fast entry for new listings whose combined free-float cap at the end of day 2 of trading would rank in the top 20 of the index, with at least five trading days' notice; the index may temporarily exceed 30 names.
- Pricing: VWAP for added/deleted names was discontinued in favour of last sale price (release of 5 May 2025), although the OMXS60 methodology still says replacements go in at VWAP.

### 3.3 Implication for the event study

Three regimes of announcement lead (days, weeks, exactly six trading days) and one regime change in selection criterion (turnover to free-float cap) that produced a single 12-name reset in July 2025. The July 2025 names were widely anticipated (Handelsbanken and Bloomberg published candidate lists in May/June 2025; Placera 19 Jun 2025), so pre-announcement run-ups are likely for that batch.

## 4. Index trackers: who tracks OMXS30 versus broader Swedish indices

Fund sizes are fondformogenhet as shown on borskollen.se or xact.se (latest reported quarter, mostly 2026 Q2); treat as approximate.

| Fund | Index tracked | AUM (SEK bn) | Source |
|---|---|---|---|
| Avanza Zero | SIX30 Return Index (SIX30RX): same 30 constituents as OMXS30, total return; informationsbroschyr says composition "revideras i januari och juli" (not yet updated for the June/Dec cycle) | 66.3 (2026 Q2); 59 in Jun 2025 | https://www.borskollen.se/fond/avanza-zero ; https://investors.avanza.se/files/Avanza_fonder/Informationsbroschyr/informationsbroschyr_avanza-zero_2026-05-04.pdf ; Placera 2025-06-19 |
| XACT OMXS30 ESG (UCITS ETF), formerly XACT OMXS30 | OMX Stockholm 30 ESG Responsible Index (OMXS30ESG): OMXS30 constituents screened for ESG exclusions, so it holds a subset of OMXS30 (29 names in 2025) | 16.1 to 16.7 | https://www.xact.se/en/Products ; https://www.borskollen.se/fond/xact-omxs30-esg-ucits-etf |
| XACT Bull, Bull 2, Bear, Bear 2 | OMXS30 / OMXS30GI leveraged (plus/minus 150%, 200%) | 0.6 + 1.8 + 0.15 + 0.3 = about 2.9 (notional exposure roughly 1.5 to 2x) | https://www.xact.se/en/Products |
| Nordnet Indexfond Sverige (Nordnet Sverige Index) | OMX Stockholm Benchmark ESG Responsible Index (OMXSBESG), a screened version of OMXSB (about 80-90 names) | 14.8 | https://www.borskollen.se/fond/nordnet-sverige-index ; https://www.nordnet.se/fonder/lista/nordnet-sverige-index-sek-aa7a9014 |
| Handelsbanken Sverige Index Criteria | SIX Sweden SRI Gross Index (a screened SIXPRX-type broad index) | 85.3 | https://www.borskollen.se/fond/handelsbanken-sverige-index-criteria |
| SEB Sverige Indexfond | SIX Sweden Sustainability (Return) Index, broad | 27.6 | https://www.borskollen.se/fond/seb-sverige-indexfond |
| Swedbank Robur Access Sverige | OMX Stockholm Benchmark Cap GI (OMXSBCAPGI); in 2018 it tracked OMXSBGI | 52.4 (2026 Q1) | https://www.borskollen.se/fond/swedbank-robur-access-sverige ; petrusko 2018-03-21 |
| Lansforsakringar Sverige Indexnara | Custom OMX Stockholm Benchmark Index since 16 Jun 2025 (before: Morningstar Sweden Large-Mid PAB Select) | not retrieved | https://www.lansforsakringar.se/49d715/globalassets/aa-global/dokument/ovrigt/fondhandelser/2025/kundbrev-lf-16-06-2025.pdf |
| XACT Sverige (ex XACT OMXSB) | SIX Sweden ESG Selection Index GI | 3.9 | https://www.xact.se/en/Products |

Summary: only Avanza Zero (via SIX30RX), XACT OMXS30 ESG and the XACT leveraged ETFs are mechanically tied to OMXS30 membership, roughly SEK 83 to 86bn in 2026 (about SEK 75bn in mid-2025). The large bank index funds (Handelsbanken, Swedbank Robur, SEB, Lansforsakringar, Nordnet) track OMXSB or SIX broad-market families (80 to 300 names), so an OMXS30 change does not force them to trade; they are, however, exposed to OMXSB reviews, which matters for the secondary sample in section 5. Nasdaq's OMXS30 derivatives (futures and options, the most traded equity-index derivatives in the Nordics) and structured products add further indexed demand that is not captured by fund AUM.

Share of index market cap: Nasdaq's public factsheet (https://indexes.nasdaqomx.com/docs/FS_OMXS30.pdf, 30 Sep 2026) does not publish the aggregate market value and the Global Index Watch weighting page requires a login, so I could not source a figure. Order-of-magnitude estimate only: the 30 constituents' full market cap is in the region of SEK 7 to 8 trillion and the free-float adjusted figure around SEK 5 to 6 trillion (my own rough estimate, not sourced), which puts OMXS30-tied passive holdings at roughly 1 to 2 percent of free-float cap. That is small by S&P 500 standards (G&S report index-fund ownership of the S&P 500 rising from about 2% in 1990 to 16-18% in the 2010s), which is itself a useful framing for the Swedish replication. If an exact figure is needed, Nasdaq GIW (free registration) shows constituent market values, and SIX/Modular Finance publish SIX30RX constituent caps.

## 5. OMXSB and OMXS60 as a larger-N secondary sample

OMX Stockholm Benchmark (OMXSB, launched Nov 2008; FRED series starts 17 Nov 2008): 80 to 100 constituents, selected by 12-month turnover (top 10%, minimum 25 names) and then by free-float cap within each ICB supersector until 85% coverage; bottom-30%-turnover names are removed and not replaced. Reviewed semi-annually with reference dates last trading day of April/October, announcement after close on the sixth trading day before, effective first trading day of June/December (same schedule OMXS30 adopted in Dec 2025). Methodology: https://indexes.nasdaqomx.com/docs/Methodology_OMXSB.pdf.

Change lists are obtainable the same way as for OMXS30:
- 2013-2019: GlobeNewswire / Nasdaq releases titled "New OMX Stockholm Benchmark portfolio selected" (e.g. https://www.globenewswire.com/news-release/2013/11/07/587625/0/en/NEW-OMX-STOCKHOLM-BENCHMARK-PORTFOLIO-SELECTED.html, Dec 2013: 6 in, 1 out; https://www.globenewswire.com/news-release/2018/11/12/1649397/0/en/new-omx-stockholm-benchmark-portfolio-selected.html; Mondo Visione carries May 2015, Nov 2015, May 2016, May 2019 copies).
- 2020 onward: "Nasdaq announces semi-annual changes to the OMX Stockholm Benchmark Index" on view.news.eu.nasdaq.com and Mondo Visione (e.g. 23 May 2023: 7 in, 10 out, https://view.news.eu.nasdaq.com/view?id=be1e3832f84b20bb2b14416bc14f0c439&lang=en; 21 Nov 2025 copy on mondovisione.com).
- Typical review produces 5 to 15 changes, so 2009-2026 should yield roughly 150 to 300 events, versus 48 for OMXS30. Caveat: OMXSB additions include many mid-caps with thin trading, and the tracking money is a different set of funds (Swedbank Robur Access Sverige, Nordnet Indexfond Sverige via OMXSBESG, Lansforsakringar since 2025).

OMX Stockholm 60 (OMXS60, launched 1 Jul 2009, base 100 at 30 Dec 2005, still calculated as of 9 Oct 2026): defined as OMXS30 plus OMXS30 NEXT (the next 30 by the OMXS30 rules), so its changes are the union of OMXS30 changes and OMXS30NEXT changes. Nasdaq does not appear to issue public press releases for OMXS30NEXT reviews; its changes are posted on Global Index Watch (login) only, so a public OMXS60 change list is harder to assemble than OMXSB. Methodology: https://indexes.nasdaqomx.com/docs/Methodology_OMXS60.pdf. Note OMXS30 NEXT membership changes are partly mechanical consequences of OMXS30 changes (a name leaving OMXS30 often drops into NEXT), which complicates event classification.

Also worth knowing: OMX Nordic 40 (OMXN40) and OMX Copenhagen 25 / OMX Helsinki 25 have the same release format; Carlsson & Bladh (2019) and Metsola (2020) pooled OMXS30 with OMXH25/OMXC20/OMXC25 to get N of 80 to 170.

## 6. Prior studies of the OMXS30 index effect

No journal article specifically on OMXS30 index changes was found. Student theses (all event studies with market-model abnormal returns):

1. Norin, C. and Parksjo, D. (2013), "Fundamentals or Frictions: The Effects of Equity Indices on the Swedish Stock Market", MSc thesis, Stockholm School of Economics (tutor Kenth Skogsvik), http://arc.hhs.se/download.aspx?MediumId=1971. OMXS30 constituent lists 1987-2012 from Nasdaq OMX; final sample 38 inclusions, 26 exclusions (1992-2009, mergers/spin-offs/name changes removed). Headline: inclusions show a significant announcement-day abnormal return of +1.4% (CAPM, t = 3.0; +1.2% FF3F) and CAR(-7,0) around announcement of +4.6%, with partial reversal (CAR(-7,+7) = +4.0%); around the effective date nothing is significant (AR(0) = +0.2%, CAR(-7,0) = +1.6%, n.s.), and long-window CAR(-30,+60) = +0.5% n.s. Volume on the day before the effective date is 2.08x normal (t = 3.05). Exclusions mirror this with a significant post-announcement drift. The appendix (Table A1) is a complete 1992-2009 event list with effective dates and is reproduced in `dl/sse_norin_parksjo_2013.md`.
2. Frantzich, A. and Nilson, A. (2024), "The Impact of OMXS30 Index Revisions Announcements on Stock Returns and Volume", BSc thesis, University of Gothenburg (supervisor Jian Hua Zhang), https://gupea.ub.gu.se/server/api/core/bitstreams/0b648e49-f901-46b6-a85c-30a62db4fa39/content. 37 inclusions and 29 exclusions, announcements 1995-2024, window -5 to +5 around the announcement, estimation -280 to -30. Headline: abnormal returns essentially insignificant (event-day AR +0.1% inclusions, +0.8% exclusions; only day -3 for inclusions significant at -1.3%); abnormal volume significant for both, peaking at day +3 (+83% inclusions, +79% exclusions); cumulative abnormal volume 21 to 31% over the windows tested. Appendix lists announcement dates 1995-2024 (used here; contains one error, Securitas placed in 2022 instead of 2021).
3. Carlsson, C. and Bladh, O. (2019), "Investigating the Price and Volume Effects following Changes on OMX Nordic Indices", MSc Finance thesis, Lund University (supervisor Frederik Lundtofte), https://lup.lub.lu.se/luur/download?func=downloadFile&recordOId=8987640&fileOId=8987641. OMXH25, OMXC20, OMXS30 1999-2018; OMXS30 contributes 16 inclusions and 13 exclusions; windows around the effective date only. Headline: no significant AAR/CAAR; event-date CAAR about +1% (inclusions) and -2% (exclusions) reversing within five days; abnormal volume on ED-1 of 32 to 39% (1% level); price effects visible in 1999-2008 but essentially absent in 2009-2018, which is a Nordic analogue of the G&S "disappearing" result.
4. Metsola, J. (2020), "The index effect: evidence from the Nordics", MSc thesis, University of Oulu, https://oulurepo.oulu.fi/handle/10024/15816. OMXH25, OMXS30, OMXC25/C20, Jan 2009 to Jan 2020, 80 events pooled. Headline: index effect "rather negligible"; temporary price and volume effects concentrated before the effective date; permanent volume effects, no permanent return effects. No OMXS30-specific magnitudes in the abstract.
5. Not retrievable in this session (DiVA/CORE blocked), listed for follow-up: "Indexeffektens inverkan pa reviderade aktier i OMXS30" (DiVA diva2:1775736, c. 2023); "The Index Effect in the Nordic Markets: Examining Returns ..." (DiVA diva2:1963940, c. 2025); "Indexeffekten: en studie gjord pa Nasdaq OMXS30 och OMXH25" (DiVA diva2:721619, c. 2014); "Kostnader for indexfonder vid revidering av OMXS30?" (DiVA diva2:1452558, c. 2020); "Inkluderingar och exkluderingar i OMXS30 och dess paverkan pa aktiers avkastning pa kort och lang sikt" (CORE 387516989); Blomstrand and Safstrand (2010), cited as an OMXS30 index-effect study in van de Wetering (2022, Erasmus); a CBS master thesis on Nordic index revisions (research-api.cbs.dk, 879434).

Overall picture from the Swedish work: announcement-window effects of about +1 to +1.5% for additions pre-2013, little or nothing on the effective date, and nothing significant in post-2009 samples. That is consistent with the G&S narrative and gives a benchmark magnitude.

## 7. Gaps, caveats and pages I could not read

Gaps in the event list:
- 2005 (both reviews) and Jan 2006: no Nasdaq/OMX release found; "no change" rests on two thesis event lists. A possible 2005 technical substitution (old Fabege, ex-Drott, taken over by Wihlborgs, which then renamed itself Fabege) is not in any source and is not included.
- Skandia out / Old Mutual in (early 2006): dates unknown, rows E001-E002 left undated.
- July 2006 announcement date unresolved (2006-06-30 versus 2006-06-03); the SSE thesis dates Fabege's exclusion 3 Jan 2006 while two other sources say 3 Jul 2006.
- Several "no change" reviews (Jul 2008, Jul 2010, Jan/Jul 2012, Jan/Jul 2013, Jul 2015, Jan 2020, Jul 2023) are inferred from identical verified constituent lists rather than from a release.
- Announcement dates for 2006-2008, Jan 2009, Jun 2014, Dec 2017, Jun 2018, Jun 2021 and Nov 2022 come from press reports, not from the release itself.
- ISINs are given only where I am confident they were valid at the event date (several names changed ISIN after later splits or redemptions); blank otherwise.
- Technical events deliberately not listed as rows: Vostok Nafta renamed Vostok Gas (May 2007); ForeningsSparbanken renamed Swedbank (2006); TeliaSonera renamed Telia Company (2016); Nordea Bank AB replaced by Nordea Bank Abp on redomiciliation (1 Oct 2018, new ISIN); Autoliv's Veoneer spin-off (2018), Atlas Copco's Epiroc spin-off (2018), Electrolux Professional spin-off (2020): the spun-off companies were not added.

Pages that could not be read (for the record): nasdaq.com press releases of 2018-06-07, 2021-06-22 and 2022-06-22 (WebFetch rate-limited, 429); business.nasdaq.com release of 2017-12-07; di.se and svd.se (blocked); web.archive.org (blocked); diva-portal.org PDFs and gupea record pages (robots/bot protection); privataaffarer.se was readable only through Firecrawl, whose account is low on credits; Nasdaq GIW corporate-actions and weighting pages require a login.

## 8. Key source URLs

- Methodology (current): https://indexes.nasdaqomx.com/docs/Methodology_OMXS30.pdf
- Old rulebook v1.5 (Dec 2014): https://docplayer.net/251049-Rules-for-the-construction-and-maintenance-of-the-omx-stockholm-30-index.html
- 2025 consultation and follow-ups: https://indexes.nasdaqomx.com/docs/OMXS30%20Index%20Consultation.pdf ; https://indexes.nasdaqomx.com/docs/OMXS30%20Index%20Consultation%20Follow%20up_Final%202.pdf ; https://indexes.nasdaqomx.com/docs/OMXS30_Consultation_Follow_Up_Reconstitution_And_Rebalance_Schedule_Summary_Of_Responses_And_Conclusion.pdf
- Methodology change release 5 May 2025: https://view.news.eu.nasdaq.com/view?id=bcafef084bdc14cf1924ea6036b3d705a&lang=en
- Review releases read: 2009-06-03 (ir.nasdaq.com), 2009-12-02 (ir.nasdaq.com), 2010-12-02 (GlobeNewswire), 2011-06-07 (ir.nasdaq.com), 2013-12-05 (eqs-news), 2014-12-04 (GlobeNewswire), 2015-12-04 (mondovisione), 2016-06-13 (marketsmedia), 2016-12-07 (GlobeNewswire), 2017-06-09 (GlobeNewswire), 2018-12-07 (GlobeNewswire), 2019-06-11 (view.news.eu.nasdaq.com), 2020-06-09 (finanznachrichten), 2020-12-10 (view.news.eu.nasdaq.com), 2021-12-22 (view.news.eu.nasdaq.com), 2022-06-22 (mondovisione), 2022-12-22 (nasdaq.com), 2023-12-20 (finanznachrichten), 2024-06-20 (view.news.eu.nasdaq.com), 2024-12-18 (view.news.eu.nasdaq.com), 2025-06-23 (view.news.eu.nasdaq.com), 2025-11-21 (mondovisione), 2026-05-22 (mondovisione).
- sv.wikipedia OMXS30 change table with its press citations: https://sv.wikipedia.org/wiki/OMXS30 (the English page has no history table).
- Avanza blog on the July 2025 reset: https://blogg.avanza.se/nya-omxs30-bolagen-som-aker-in-och-ut/
