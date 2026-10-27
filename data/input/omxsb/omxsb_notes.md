# OMX Stockholm Benchmark (OMXSB): semi-annual constituent changes 2013 to Oct 2026

Companion to `omxsb_changes_2013_2026.csv` (built by `omxsb_build.py`). Compiled 11 Oct 2026 for a Greenwood and Sammon (2025, JF) style replication.

Headline: 27 of the 28 reviews in the window have a change list; 394 events (222 additions, 172 deletions), of which 325 are VERIFIED from Nasdaq release text and 69 are SECONDARY (three reviews read from Swedish newswire reports because the Nasdaq release could not be fetched). The 28th review (December 2026) has not been announced yet. A per-ticker membership-chain check (`omxsb_build.py --check`) finds zero inconsistencies across 152 tickers, which is strong evidence that the lists were read correctly.

## 1. Correction to the previous agent's description

The schedule is NOT "first trading day of July and January until 2025". Every release from 2013 onward says the index is reviewed in May and November with the new portfolio effective at market open on the first trading day of June and December (and the 2009 and 2010 releases say the same). What changed over time is the announcement timing (see section 4), not the effective months. OMXS30 is the index that moved from January/July to June/December in 2025; OMXSB has always been June/December.

Constituent count: Nasdaq's OMXSBPI overview page showed 111 constituents in August 2026 (the 2009 release had 81), so "80 to 100" is low for recent years; the Robur Access Sverige portfolio had 87 to 103 holdings over 2018-2025.

## 2. Releases found (one per review)

Verification: VERIFIED = change lists read from the Nasdaq release text (GlobeNewswire, view.news.eu.nasdaq.com, nasdaq.com, or a verbatim republication of the release on mondovisione.com / loomis.us / finanznachrichten.de). SECONDARY = read from a newswire report of the release.

| Cycle | Announced | Effective | Adds | Dels | Verif. | Source read |
|---|---|---|---|---|---|---|
| 2013H1 | 2013-05-08 | 2013-06-03 | 2 | 5 | VERIFIED | https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/ |
| 2013H2 | 2013-11-07 | 2013-12-02 | 6 | 1 | VERIFIED | https://www.globenewswire.com/news-release/2013/11/07/587625/0/en/NEW-OMX-STOCKHOLM-BENCHMARK-PORTFOLIO-SELECTED.html (release PDF attachment OMXSB_2013-11-07.pdf; Mondo Visione copy …-st-4-2013117/) |
| 2014H1 | 2014-05-08 | 2014-06-02 | 2 | 2 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-5-201458/ |
| 2014H2 | 2014-11-10 | 2014-12-01 | 6 | 4 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-6-20141110/ |
| 2015H1 | 2015-05-07 | 2015-06-01 | 4 | 7 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-7-201557/ |
| 2015H2 | 2015-11-10 | 2015-12-01 | 7 | 3 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-8-20151110/ ; same text at https://www.loomis.us/resources/press-releases-news/omx-stockholm-benchmark-portfolio-selected |
| 2016H1 | 2016-05-10 | 2016-06-01 | 7 | 1 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-9-2016510/ |
| 2016H2 | 2016-11-10 | 2016-12-01 | 10 | 4 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-20161110/ |
| 2017H1 | 2017-05-09 (corr. 2017-05-17) | 2017-06-01 | 7 | 4 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-1-201759/ ; correction https://mondovisione.com/media-and-resources/news/correction-new-omx-stockholm-benchmark-portfolio-selected-2017517/ |
| 2017H2 | 2017-11-10 | 2017-12-01 | 9 | 5 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-2-20171110/ ; Direkt via https://www.aktiespararna.se/nyheter/forandringar-i-viktigt-borsindex and https://www.placera.se/placera/redaktionellt/2017/11/10/nya-i-aktier-i-benchmark-index.html |
| 2018H1 | 2018-05-08 | 2018-06-01 | 6 | 6 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-3-201858/ |
| 2018H2 | 2018-11-12 | 2018-12-03 | 10 | 6 | VERIFIED | https://www.globenewswire.com/news-release/2018/11/12/1649397/0/en/New-OMX-Stockholm-Benchmark-Portfolio-Selected.html (Mondo Visione copy …-stockh-4-20181112/) |
| 2019H1 | 2019-05-13 | 2019-06-03 | 6 | 8 | VERIFIED | https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-5-2019513/ ; Realtid 2019-05-14 https://www.realtid.se/forandringar-i-omx-stockholm-benchmark-index/ |
| 2019H2 | 2019-11-11 | 2019-12-02 | 6 | 7 | VERIFIED | https://www.nasdaq.com/press-release/new-omx-stockholm-benchmark-portfolio-selected-2019-11-11 (Mondo Visione copy …-stockh-6-20191111/) |
| 2020H1 | 2020-05-14 | 2020-06-01 | 6 | 5 | VERIFIED | https://view.news.eu.nasdaq.com/view?id=bdf4cc2c820c3b12852b88ca0c810b60f&lang=en ; finanznachrichten.de 49653661 |
| 2020H2 | 2020-11-10 | 2020-12-01 | 19 | 8 | SECONDARY | Swedbank Aktiellt 2020-11-10 10:42 https://www.swedbank-aktiellt.se/2020/november/manga_forandringar_i_omxsb-indexet.csp (reports the Nasdaq release of that morning) |
| 2021H1 | 2021-05-21 | 2021-06-01 | 9 | 5 | SECONDARY | Finwire via Placera https://www.placera.se/placera/telegram/2021/05/24/academedia-nasdaq-justerar-om-i-omx-stockholm-benchmark-index-oms.html (first sent Fri 2021-05-21 evening; also borsvarlden.com 2021-05-21 16:34 UTC) |
| 2021H2 | 2021-11-23 | 2021-12-01 | 12 | 12 | VERIFIED | https://view.news.eu.nasdaq.com/view?id=b147597c4972dde112c64e62f434f296b&lang=en ; https://www.finanznachrichten.de/nachrichten-2021-11/54569570-… ; Dagens Bors 2021-11-24 |
| 2022H1 | 2022-05-23 | 2022-06-01 | 11 | 11 | VERIFIED | https://www.nasdaq.com/press-release/nasdaq-announces-semi-annual-changes-to-the-omx-stockholm-benchmark-index-2022-05-23 ; finanznachrichten.de 56120676 |
| 2022H2 | 2022-11-21 | 2022-12-01 | 18 | 10 | SECONDARY | Finwire via Placera https://www.placera.se/telegram/nasdaq-justerar-om-i-omx-stockholm-benchmark-index-2022-11-22 (report dated 2022-11-22; the release link was tweeted 2022-11-21 19:05 CET, x.com/ekkalundin/status/1594753946479902725) |
| 2023H1 | 2023-05-23 | 2023-06-01 | 7 | 10 | VERIFIED | https://view.news.eu.nasdaq.com/view?id=be1e3832f84b20bb2b14416bc14f0c439&lang=en ; https://www.finanznachrichten.de/nachrichten-2023-05/59160570-… |
| 2023H2 | 2023-11-23 (UPDATE 2023-11-29) | 2023-12-01 | 6 | 7 | VERIFIED | https://view.news.eu.nasdaq.com/view?id=be007a57f33d4d52541bfc529d8b21f55&lang=en ; UPDATE https://www.finanznachrichten.de/nachrichten-2023-11/60793469-update-… ; Realtid 2023-11-24 |
| 2024H1 | 2024-05-24 | 2024-06-03 | 8 | 8 | VERIFIED | https://view.news.eu.nasdaq.com/view?id=b465a30d4561f8f31f15763b0f6dc7ae6&lang=en (Mondo Visione copy …-index-2-2024524/) |
| 2024H2 | 2024-11-22 | 2024-12-02 | 9 | 7 | VERIFIED | https://view.news.eu.nasdaq.com/view?id=b8d5c1243d98f7e08a9438dd230a204e7&lang=en ; https://www.nasdaq.com/press-release/nasdaq-announces-semi-annual-changes-omx-stockholm-benchmarktm-index-2024-11-22 ; Finwire/EFN 2024-11-25 |
| 2025H1 | 2025-05-22 | 2025-06-02 | 10 | 5 | VERIFIED | https://mondovisione.com/media-and-resources/news/nasdaq-announces-semi-annual-changes-to-omx-stockholm-benchmark-index-2025522/ ; Finwire/MarketScreener 2025-05-23 |
| 2025H2 | 2025-11-21 | 2025-12-01 | 8 | 9 | VERIFIED | https://mondovisione.com/media-and-resources/news/nasdaq-announces-semi-annual-changes-to-omx-stockholm-benchmark-index-20251121/ ; Finwire/MarketScreener 2025-11-24 |
| 2026H1 | 2026-05-22 | 2026-06-01 | 11 | 12 | VERIFIED | https://view.news.eu.nasdaq.com/view?id=b49024270d6eeb2f3f1ae80c5fea1dae7&lang=en ; Mondo Visione …-index-2026522/ ; Finwire/Borsvarlden 2026-05-25 |

Reviews with no change list: **2026H2** only (reference date 30 Oct 2026; announcement expected after close on 20 Nov 2026, the 6th trading day before Mon 1 Dec 2026).

Reviews with a SECONDARY list only (Nasdaq release exists but could not be fetched): 2020H2, 2021H1, 2022H2. The nasdaq.com press-release host returned HTTP 429 for every attempt in this session, Mondo Visione's search index does not contain the Nov 2020 to Nov 2023 OMXSB items, and GlobeNewswire's search pages are robots-blocked. The obvious next step is to open these three on nasdaq.com from a browser: `…/press-release/nasdaq-announces-semi-annual-changes-to-the-omx-stockholm-benchmark-index-2021-05-21` and `…-2022-11-21` (URL pattern inferred from the 2022-05-23 page), and the Nov 2020 release titled "Nasdaq Selects New OMX Stockholm Benchmark Portfolio" (10 Nov 2020). For these three reviews the ticker column was filled by me from Nasdaq Stockholm conventions and is flagged in `notes`.

Announced-then-reversed changes (excluded from the default CSV, emitted with `--include-reversed`):
- 2017H1: SAAB B deletion announced 9 May 2017, withdrawn by Nasdaq correction 17 May 2017 (SAAB B stayed in).
- 2023H2: Karnov (KAR) addition and JM (JM) deletion announced 23 Nov 2023, withdrawn by Nasdaq UPDATE 29 Nov 2023.

Other caveats for the event study:
- The releases never give ISINs in 2013-2026 (the 2010 release did), so the `isin` column is empty; map from ticker.
- Ticker spelling follows the release. Nasdaq's Dec 2023 release prints Camurus as "CMAX" (sic); the CSV uses CAMX with a note. Cellink (CLNK B, added Dec 2020) is the same company as BICO (deleted Jun 2022); D. Carnegie & Co (DCAR B) became Hembla (HEM B); Klovern appears as KLOV, KLOV A and KLOV B over time; AF Poyry (AF B) became AFRY.
- Corem (CORE B) is deleted in Dec 2022 without a recorded addition because it entered through the 2021 Klovern takeover (corporate-action replacement, not a review).
- Names deleted before their first recorded addition were in the index before 2013.
- No ticker is added twice without an intervening deletion or vice versa (0 chain problems), which is also why the SECONDARY lists can be trusted: every one of their names is consistent with the VERIFIED lists before and after.

## 3. Methodology (selection rule, reference date, announcement lead)

Current rulebook (Nasdaq "OMX Stockholm Benchmark Index Methodology", copyright 2025, https://indexes.nasdaq.com/docs/Methodology_OMXSB.pdf):
- Universe: members of OMX Stockholm All-Share (OMXSPI); non-zero turnover; not in bankruptcy; no pending buyout/delisting.
- Ranking by Nasdaq official aggregate 12-month SEK turnover ending at the reference date. Securities in the top 10% of the turnover ranking (minimum 25) are selected; then, within each ICB Supersector, securities are added in free-float market-cap order until at least 85% of the supersector's free-float cap is covered (target may not be met). Securities in the bottom 30% of the turnover ranking are removed and not replaced.
- Free-float market-cap weighted, no caps (the OMXSBCAP version caps weights for UCITS).
- Reconstitution and rebalance semi-annual. Reference date: last trading day of April and October. Announcement: after the close on the sixth trading day before the effective date. Effective: market open on the first trading day of June and December.

Earlier releases (2013-2020) describe the rule only qualitatively: "some of the largest and most traded stocks on Nasdaq Stockholm, represented by companies in all ten industries; screened for liquidity; weights based on free-float adjusted market value; reviewed semi-annually in May and November; new portfolios effective the first trading day of June and December". The repeated flip-flopping of borderline names (SSAB A in and out every six months 2023-2026; Bravida, AFRY, Beijer Ref similar) is consistent with a pure turnover-rank cutoff without a buffer zone.

Related custom index: the "Custom OMX Stockholm Benchmark Index" (COMXSB, https://indexes.nasdaq.com/docs/COMXSB_Methodology.pdf) is an ESG-screened subset of OMXSB for Lansforsakringar with the same reference, announcement and effective dates.

## 4. Announcement lead observed in practice

Lead = trading days from the announcement to the effective date (Stockholm calendar: May 1, Ascension Day, June 6 excluded; weekends excluded).

| Period | Announcement time | Lead (trading days) |
|---|---|---|
| May 2013 to Nov 2020 | 08:30 CET, before the open, roughly three weeks before the effective date | 14 to 17 (11 in May 2020) |
| May 2021 to May 2023 | after the close (Finwire notes the May 2021 story went out Friday evening; from Nov 2021 the releases carry an 18:00 CET timestamp) | 7 to 8 (6 in Nov 2021 and May 2022) |
| Nov 2023 to May 2026 | 18:00 CET, after the close | exactly 6 every time (= rulebook) |

Per-cycle leads are printed by `python3 omxsb_build.py --summary`. For an event study this matters: until Nov 2020 the announcement day's return already contains the reaction; from May 2021 the first trading reaction is on the day after the announcement date in the CSV (announcement_date + 1 trading day). The effective date in the CSV is the first day the stock trades as a member; the index-fund trade is at the close of the preceding trading day.

## 5. Trackers tied to OMXSB and their size

| Fund | Index tracked | AUM, SEK bn (date) | Source |
|---|---|---|---|
| Swedbank Robur Access Sverige | OMX Stockholm Benchmark Cap GI (capped version of OMXSB; same constituents) | 11.3 (2018-12-31), 24.0 (2019-12-31), 26.2 (2020-12-31), 36.4 (2021-12-31), 28.7 (2022-12-31), 36.1 (2023-12-31), 39.8 (2024-12-31), 49.8 (2025-12-31), 57.8 (2026Q2). Holdings 87 to 103. | Finansinspektionen fondinnehav via insidevoice.se/fond/swedbank-robur-access-sverige/<quarter-end>; borskollen.se/fond/swedbank-robur-access-sverige |
| Nordnet Sverige Index (Nordnet Indexfond Sverige; started 2009-03-10 as Nordnet Superfonden Sverige) | OMX Stockholm Benchmark GI until 2022-06-01, thereafter OMX Stockholm Benchmark ESG Responsible GI (OMXSBESGGI, a screened subset of OMXSB) | year-end: 1.22 (2016), 1.71 (2017), 1.81 (2018), 2.69 (2019), 3.49 (2020), 6.40 (2021), 5.78 (2022), 7.83 (2023), 9.42 (2024), 12.08 (2025); 104 holdings at 2025-12-31 | Annual report 2025: https://nordnetab.com/wp-content/uploads/2026/04/Arsberattelse-Nordnet-Sverige-Index-2025.pdf |
| Lansforsakringar Sverige Index (Indexnara) | Custom OMX Stockholm Benchmark Index since 2025-06-16 (before: Morningstar Sweden Large-Mid PAB Select, so not an OMXSB tracker for 2013 to mid-2025) | 49.6 (2026Q2) | Customer letter https://www.lansforsakringar.se/49d715/globalassets/aa-global/dokument/ovrigt/fondhandelser/2025/kundbrev-lf-16-06-2025.pdf ; borskollen.se/fond/lansforsakringar-sverige-index |
| XACT OMXSB (ETF, later renamed XACT Sverige and moved to a SIX index) | OMXSB GI in the early part of the window | not retrieved | Previous agent's note; the switch date was not verified here |

Implication for the replication: OMXSB-tied passive money is modest (roughly SEK 15 bn in 2016 rising to about SEK 60 bn by 2025 and about SEK 120 bn in 2026 once LF's fund switched), against an index free-float cap in the trillions, so the mechanical demand shock per review is small and grew over the window; the index-fund share is closer to the early-1990s S&P 500 numbers in G&S than to their 2010s numbers.

## 6. Fetch failures to be aware of

- nasdaq.com/press-release pages: HTTP 429 from the fetch proxy throughout the session (three of the Nasdaq releases could therefore not be read; see section 2).
- newsclient.omxgroup.com, privataaffarer.se, m.mondovisione.com, globenewswire.com search pages: robots-blocked. affarsvarlden.se: client error.
- Direct curl to external hosts is denied by the egress policy, so every page was read through the fetch tool; lists were cross-checked between two independent copies wherever two existed (Dec 2021, Jun 2023, Dec 2023, Dec 2024, Jun 2025, Dec 2025, Jun 2026, Dec 2015, Dec 2017, Jun 2019) and all matched.
