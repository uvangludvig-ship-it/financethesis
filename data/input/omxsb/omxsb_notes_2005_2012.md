# OMX Stockholm Benchmark (OMXSB): semi-annual constituent changes 2005 to 2012

Companion to `omxsb_changes_2005_2012.csv` (built by `code/build/omxsb_build_2005_2012.py`, which imports the trading calendar and column list from `omxsb_build.py`). Compiled 27 Oct 2026 as the backward extension of `omxsb_changes_2013_2026.csv` / `omxsb_notes.md`; same columns, same vocabulary, same rule (nothing inferred from membership snapshots or from the LSEG index feed).

Headline: 12 of the 17 reviews whose effective date falls in 2005-2012 have a change list; 142 events (62 additions, 80 deletions), all VERIFIED from the exchange's own release text. The five earliest reviews (effective Jan 2005, Jul 2005, Jan 2006, Jul 2006, Jan 2007) could not be found anywhere online (section 3). The membership chain is consistent within 2005-2012 and across the join with the 2013-2026 file except for one name, Nokia (section 4).

## 1. Correction to the task description: the schedule was January/July until January 2009

The task assumed June/December reviews throughout. That is only true from the May 2009 review onward. Every OMX-era notice found says the new composition applies "för första/andra halvåret" and takes effect on the first trading day of January or July:

| Notice | Date | Effective |
|---|---|---|
| Aktier 175/07 (corr. 183/07) | 2007-06-12 (2007-06-25) | Mon 2 Jul 2007 |
| Aktier 287/07 | 2007-12-14 | Wed 2 Jan 2008 |
| Aktier 142/08 (update 148/08) | 2008-06-11 (2008-06-16) | Tue 1 Jul 2008 |
| Aktier 293/08 (corr. 294/08) | 2008-12-11 | Fri 2 Jan 2009 |

Nasdaq OMX then held a review in May 2009 effective 1 Jun 2009 and from there on the June/December cycle described in `omxsb_notes.md` section 1. So 2009 had two reviews five months apart (2 Jan and 1 Jun). The window 2005-01-01 to 2012-12-31 therefore contains 17 reviews, not 16: Jan 2005, Jul 2005, Jan 2006, Jul 2006, Jan 2007, Jul 2007, Jan 2008, Jul 2008, Jan 2009, Jun 2009, Dec 2009, Jun 2010, Dec 2010, Jun 2011, Dec 2011, Jun 2012, Dec 2012.

Naming in the CSV: `review_cycle` is the half-year of the effective date, as in the 2013-2026 file (there H1 = June, H2 = December). So 2007H2 = effective 2 Jul 2007, 2008H1 = effective 2 Jan 2008, 2008H2 = effective 1 Jul 2008. The review effective 2 Jan 2009 is labelled **2009JAN** (event ids `OMXSB-2009JAN-nn`) because 2009H1 is taken by the June 2009 review. Anything that groups on `review_cycle` must treat 2009JAN as a separate review.

Index history, for context: the index was launched by Stockholmsbörsen as SBX (Stockholmsbörsens Benchmarkindex; base 100 at 1995-12-30; XACT SBX ETF listed 2 Jun 2003, Cision c80505) and renamed OMX Stockholm Benchmark on 3 Oct 2005 when OMX harmonised its index names (Cision c161338, 22 Aug 2005). The OMX description sheet (omxgroup.com/digitalAssets/8489_OMXSBenchmark_swe.pdf, via Wayback) says 80 to 100 constituents, free-float weighted, with a capped UCITS version OMXSBCAP. The Nov 2010 release puts assets tracking the index at about SEK 160 bn.

## 2. Releases found (one per review)

Verification: VERIFIED = change lists read from the exchange's own release text: for 2007-2008 the OMX/Nasdaq OMX Stockholm market notice on Hugin/GlobeNewswire together with its PDF attachment (which carries name, ticker, ISIN and GICS code); for 2009-2012 the Nasdaq OMX press release on GlobeNewswire, cross-read against ir.nasdaq.com or the verbatim Mondo Visione copy. Every list was read from two independent copies where two existed (all of 2009H1 to 2012H2); all matched.

| Cycle | Announced (CET/CEST) | Effective | Adds | Dels | Verif. | Source read |
|---|---|---|---|---|---|---|
| 2007H2 | 2007-06-12 12:29 | 2007-07-02 | 6 | 7 | VERIFIED | https://www.globenewswire.com/news-release/2007/06/12/116558/0/sv/avista-ny-sammans%c3%a4ttning-av-omx-stockholm-benchmark-index-175-07.html (PDF fileId=195221); correction 183/07 2007-06-25 https://www.globenewswire.com/news-release/2007/06/25/116692/0/sv/files/193995/0/wkr0001.pdf |
| 2008H1 | 2007-12-14 12:00 | 2008-01-02 | 3 | 4 | VERIFIED | https://www.globenewswire.com/news-release/2007/12/14/118048/0/sv/avista-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-287-07.html (PDF fileId=176761); English 118047 |
| 2008H2 | 2008-06-11 13:00 | 2008-07-01 | 7 | 4 | VERIFIED | https://www.globenewswire.com/news-release/2008/06/11/119843/0/sv/files/154957/0/wkr0003.pdf ; update 148/08 2008-06-16 https://www.globenewswire.com/news-release/2008/06/16/119887/0/sv/files/154582/0/wkr0003.pdf |
| 2009JAN | 2008-12-11 09:30 (corr. 12:35) | 2009-01-02 | 2 | 12 | VERIFIED | 293/08 https://www.globenewswire.com/news-release/2008/12/11/121676/0/sv/files/136223/0/wkr0003.pdf ; correction 294/08 https://www.globenewswire.com/news-release/2008/12/11/121680/0/sv/avista-korrigering-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-294-08.html (PDF fileId=136174) |
| 2009H1 | 2009-05-11 16:14 | 2009-06-01 | 4 | 3 | VERIFIED | https://www.globenewswire.com/news-release/2009/05/11/2584/0/da/New-OMX-Stockholm-Benchmark-portfolio-selected.html (with 81-name constituent table); https://ir.nasdaq.com/news-releases/news-release-details/new-omx-stockholm-benchmark-portfolio-selected |
| 2009H2 | 2009-11-09 13:00 | 2009-12-01 | 5 | 3 | VERIFIED | https://www.globenewswire.com/news-release/2009/11/09/142934/0/en/new-omx-stockholm-benchmark-portfolio-selected.html ; Mondo Visione …-omx-stoc-2011124/ |
| 2010H1 | 2010-05-07 14:30 | 2010-06-01 | 8 | 4 | VERIFIED | https://www.globenewswire.com/news-release/2010/05/07/167938/0/en/new-omx-stockholm-benchmark-portfolio-selected.html ; https://ir.nasdaq.com/static-files/1cfd8887-6154-4b78-8585-a94e64e30582 |
| 2010H2 | 2010-11-08 14:30 | 2010-12-01 | 1 | 4 | VERIFIED | https://www.globenewswire.com/news-release/2010/11/08/189068/0/en/new-omx-stockholm-benchmark-portfolio-selected.html ; Mondo Visione …-selected-2011124/ |
| 2011H1 | 2011-05-09 09:00 | 2011-06-01 | 7 | 8 | VERIFIED | https://www.globenewswire.com/news-release/2011/05/09/214538/0/en/new-omx-stockholm-benchmark-portfolio-selected.html ; https://ir.nasdaq.com/news-releases/news-release-details/new-omx-stockholm-benchmark-portfolio-selected-2 |
| 2011H2 | 2011-11-10 09:30 | 2011-12-01 | 5 | 5 | VERIFIED | https://www.globenewswire.com/news-release/2011/11/10/237112/0/en/new-omx-stockholm-benchmark-portfolio-selected.html ; Mondo Visione …-omx-st-1-20111110/ |
| 2012H1 | 2012-05-07 13:20 | 2012-06-01 | 11 | 24 | VERIFIED | https://www.globenewswire.com/news-release/2012/05/07/262074/0/en/new-composition-of-omx-stockholm-benchmark-index.html (PDF 2012-05-07_OMXSB-Review.pdf); counts confirmed by Dagens industri 2012-05-07 https://www.di.se/artiklar/2012/5/7/de-kastas-ut-fran-toppindex/ |
| 2012H2 | 2012-11-09 09:00 | 2012-12-03 | 3 | 2 | VERIFIED | https://www.globenewswire.com/news-release/2012/11/09/503912/0/en/new-omx-stockholm-benchmark-portfolio-selected.html ; Mondo Visione …-omx-st-3-2012119/ |

Announcement times are the GlobeNewswire timestamps (US Eastern) converted to Stockholm time (+6 h). Lead in trading days (announcement to effective, Stockholm calendar, `--summary`): 13, 8, 13, 11, 14, 16, 16, 17, 17, 15, 18, 16.

The May 2012 review was published as an Index Operations notice ("New composition of OMX Stockholm Benchmark Index", organisation "Index" on GlobeNewswire), not as a press release, and is by far the largest reconstitution in the window (11 in, 24 out; the index shrank from about 85 to about 72 names). A Cision release by Trigon Agri (2012-05-31) confirms its addition effective 1 Jun 2012.

## 3. Reviews not found (5) and what was tried

| Review | Effective | Expected notice |
|---|---|---|
| 2005H1 | 2005-01-03 | Stockholmsbörsen, "Ny sammansättning av SBX" (index still named SBX), Dec 2004 |
| 2005H2 | 2005-07-01 | Stockholmsbörsen, SBX, Jun 2005 |
| 2006H1 | 2006-01-02 | OMX / Stockholmsbörsen, "Ny sammansättning av OMX Stockholm Benchmark index", Dec 2005 |
| 2006H2 | 2006-07-03 | same, Jun 2006 |
| 2007H1 | 2007-01-02 | same, Dec 2006 |

Tried, without result:
- Hugin/GlobeNewswire: keyword searches "Stockholm Benchmark", "Benchmark", "SBX" with date filters covering 2005-01-01 to 2007-03-01, and the organisation feed "Nasdaq Stockholm AB" filtered to 2005-2006. The archive of OMX Stockholm market notices on GlobeNewswire begins on 8 Jan 2007 (Meda rights-issue adjustment, 2/07); nothing from 2005-2006 exists there. Dec 2006 is not covered even though the 22 Jan 2007 notices refer to the then-current composition.
- Cision: newsrooms `news.cision.com/se/omx-exchanges` (2004-2006) and `news.cision.com/se/stockholmsborsen` (2001-2004) scanned page by page; they hold press releases only (index-name harmonisation 2005-08-22, monthly statistics, XACT SBX listing 2003), no composition notices. The Cision full-text search returns nothing for "Stockholm Benchmark" + "sammansättning".
- mynewsdesk `nasdaqomx` pressroom, which holds OMX market notices from late 2006 (e.g. 298/06 of 2006-12-06 on Home Properties): the pressroom listing and search pages return 404 today; only items that are indexed by search engines or in the Wayback Machine are reachable, and none of them is a composition notice.
- Wayback Machine (CDX API, intermittently "temporarily offline" during the session): omxgroup.com market-notice listing pages from Oct 2006 to Jan 2007 are archived but the lists were loaded by JavaScript from an un-archived endpoint; the archived notice pages (`.../marketnotices/Article/?msgId=...`) start at msgId 160778 captured 2007-03-15, i.e. 2007 notices only; stockholmsborsen.se captures end in 2004 and omxgroup.com/stockholmsborsen/borsmeddelanden returned 404 already in Dec 2004. The Wayback Machine does hold the "Morning Weight Report for OMXSBPI at 2007-01-02.xls" (omxgroup.com/digitalAssets/15824_...), i.e. the constituent list after the Jan 2007 review, but no list before it, so it cannot give the change list and was not used (the file's rule is: no inference from membership snapshots).
- Swedish press: Firecrawl and web searches on di.se (article archive 2005-2006 is indexed), svd.se, affarsvarlden.se, privataaffarer.se, aktiespararna.se, e24, placera for "Benchmark"/"SBX"/"benchmarkindex" with "nya bolag", "sammansättning", "halvåret" in 2005-2006. The only hits are a 26 Sep 2006 DI note on a Securitas start price in OMXSB and a 2017 DI column about an "SBX update"; no report of a review.
- Nasdaq IR (`ir.nasdaq.com`) starts with the May 2009 release; `-3`/`-4` suffixes do not exist (the two detail pages are May 2009 and May 2011; the 2010 release is a static-files PDF only).
- Mondo Visione's index covers Nov 2009 onward for this release family.

Next steps if these five are needed: (1) ask Nasdaq Index Operations (index@nasdaq.com, +46 8 405 62 96) for the market notices 2004-2006 on the SBX/OMXSB composition; they are numbered Aktier nnn/yy and were kept in the exchange's notice archive; (2) Retriever/Mediearkivet (DI, TT, Direkt) for mid-June and mid-December 2004-2006; (3) Handelsbanken (XACT SBX/OMXSB) annual reports 2005-2006 as a membership cross-check only.

## 4. Caveats for the event study

- Announcement timing differs from 2013-2026: every release in 2007-2012 came out during trading hours, between 09:00 and 16:14 Stockholm time (OMX-era notices around midday; Nasdaq OMX 2009-2010 at 13:00-16:14; 2011-2012 at 09:00-09:30 or 13:20). The announcement-day return therefore contains only part of the reaction (none of it for the 16:14 release of 11 May 2009 if the market is slow). From May 2013 the releases moved to 08:30, pre-open (see `omxsb_notes.md` section 4).
- Announced-then-reversed changes (excluded from the CSV by default, emitted with `--include-reversed` as `addition_reversed`): Sigma AB ser. B (SIGM B) and Stora Enso Oyj ser. A (STE A) were listed as additions in 293/08 at 09:30 on 11 Dec 2008 and withdrawn by 294/08 at 12:35 the same day.
- Corrections that did not change the lists: 183/07 (25 Jun 2007, TWW SDB B had been left out of the Excel constituent file; it stayed in the index) and 148/08 (16 Jun 2008, number of shares for IBS B).
- Nokia (NOKI SEK) is the one chain problem, within this file and in the join with 2013-2026: it is removed effective 1 Jun 2009 (the May 2009 constituent table of 81 names does not contain it) and removed again effective 1 Jun 2011, but no release in between (Nov 2009, May 2010, Nov 2010) lists it as an addition. Nokia must have re-entered between Jun 2009 and Jun 2011 outside the published add lists (or one release is incomplete). Not resolved; the two deletion rows are kept as the releases state them and the `--check` output flags it. Both the later addition (Dec 2012, `NOKI SEK`) and deletion (Dec 2015, printed `NOKIA SEK` in the 2013-2026 file) are consistent.
- Ticker spelling follows the release: Transcom is `TWW SDB B` in 2009 (Jan and Jun) and `TWW SDB` in the May 2010 deletion; Nokia is `NOKI SEK` here and `NOKIA SEK` in Dec 2015. `--check` maps these aliases. Wihlborgs is misspelt "Wihlborgs Fastighteter AB" in the June 2007 notice (kept as written, flagged in `notes`).
- Loomis (LOOM B) is deleted on 2 Jan 2009 without a prior recorded addition: it was spun off from Securitas on 9 Dec 2008 and entered OMXSB through that corporate action, not through a review; it was re-added at the June 2009 review. Names deleted before any recorded addition (e.g. HUSQ A, STE R, GUNN, HEXA B, MIC SDB, REZT, SSAB B, AXFO, SECU B, SAS) were members before July 2007 or entered through corporate actions.
- Company names are as printed: Swedish-form names with "ser. B" in the 2007-2008 notices, Nasdaq's shorter English forms from 2009. ISINs are filled only where the source prints them (the 2007-2008 notices); the Nasdaq OMX releases 2009-2012 do not give ISINs, so those rows have an empty `isin` as in the 2013-2026 file.
- Counts per review are small in 2007-2011 (7 to 15) and the index had 81 names in June 2009, 86 in June 2011 and 85 in December 2011 per the releases.

## 5. Fetch notes

- GlobeNewswire pages and PDF attachments were readable through Firecrawl (direct curl returns 403); the attachment URLs `Attachment/DownloadAttachment?articleid=...&fileId=...` and `/files/<id>/0/wkr000n.pdf` are stable. The GlobeNewswire keyword search with a date range (`/en/search/keyword/<kw>/date/[YYYY-MM-DD TO YYYY-MM-DD]`) works and was the way the 2007-2008 notices were located.
- ir.nasdaq.com returns 403 to the plain fetch tool but is readable through Firecrawl.
- Internet Archive services were offline for parts of the session; the CDX API answered intermittently.
- Firecrawl's per-minute rate limit was hit once; nothing was lost.
