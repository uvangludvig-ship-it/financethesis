import csv

OUT = "/tmp/claude-0/-home-claude/5b447583-b5ae-51ff-a30e-274749b6d7af/scratchpad/t2/omx/omxs30_changes_2005_2026.csv"

cols = ["event_id", "effective_date", "announcement_date", "company", "ticker", "isin", "type",
        "reason", "review_cycle", "source_url", "source_type", "verification", "notes"]

# Source URL shorthands
WIKI_SV = "https://sv.wikipedia.org/wiki/OMXS30"
GU2024 = "https://gupea.ub.gu.se/server/api/core/bitstreams/0b648e49-f901-46b6-a85c-30a62db4fa39/content"
SSE2013 = "http://arc.hhs.se/download.aspx?MediumId=1971"
NQ_2009 = "https://ir.nasdaq.com/news-releases/news-release-details/semi-annual-review-omx-stockholm-30-index-and-launch-new-omx"
NQ_2009_SV = "https://www.globenewswire.com/news-release/2009/06/03/126063/0/sv/Halv%C3%A5rsrevidering-av-OMX-Stockholm-30-Index-och-lansering-av.html"
NQ_2015 = "https://mondovisione.com/media-and-resources/news/semi-annual-review-of-the-omx-stockholm-30-index-the-new-portfolio-of-the-omx-1-2015124/"
NQ_2016 = "https://www.globenewswire.com/news-release/2016/12/07/895672/0/en/semi-annual-review-of-the-omx-stockholm-30-index.html"
NQ_2017 = "https://www.globenewswire.com/news-release/2017/06/09/1011926/0/en/semi-annual-review-of-the-omx-stockholm-30-index.html"
NQ_2020 = "https://view.news.eu.nasdaq.com/view?id=b783a55ac05d00eb1bb15ecaa5e077250&lang=en"
NQ_2022 = "https://mondovisione.com/media-and-resources/news/nasdaq-announces-semi-annual-changes-to-the-omx-stockholm-30-index-3-2022622/"
NQ_2022D = "https://www.nasdaq.com/press-release/nasdaq-announces-semi-annual-changes-to-the-omx-stockholm-30-index-2022-12-22"
NQ_2024 = "https://view.news.eu.nasdaq.com/view?id=bd35e114a5cc4ef5961fd79c4c85eb122&lang=en"
NQ_2025 = "https://view.news.eu.nasdaq.com/view?id=bcac945d48982875d4ea084d072e73269&lang=en"
SCANIA_DELIST = "https://www.globenewswire.com/news-release/2014/05/21/638110/0/en/Delisting-from-NASDAQ-OMX-Stockholm-of-Scania-AB-79-14.html"
REALTID_2018 = "https://www.realtid.se/fingerprint-ut-och-hexagon-in-i-omxs30/"
PA_2021 = "https://www.privataaffarer.se/placeringar/aktier/sinch-tar-securitas-plats-i-omxs30/"
PA_2022 = "https://www.privataaffarer.se/sbb-in-i-omxs30/"
SWMA_CAPIQ = "https://www.marketscreener.com/quote/stock/SWEDISH-MATCH-AB-PUBL-6492173/news/Swedish-Match-AB-OM-SWMA-dropped-from-OMX-Stockholm-30-Index-42353100/"
OM_CISION = "https://news.cision.com/se/old-mutual"

rows = []
n = 0

def add(eff, ann, company, ticker, isin, typ, reason, cycle, url, stype, ver, notes):
    global n
    n += 1
    rows.append([f"E{n:03d}", eff, ann, company, ticker, isin, typ, reason, cycle, url, stype, ver, notes])

# ---- 2006: Skandia -> Old Mutual (merger replacement), dates not found ----
add("", "", "Skandia Forsakrings AB (Skandia)", "SDIA", "", "deletion",
    "merger (acquired by Old Mutual plc; offer declared unconditional 26 Jan 2006, completed Feb 2006)", "off-cycle",
    OM_CISION, "company press releases (Old Mutual) + sv.wikipedia OMXS30 table (Old Mutual listed as member excluded 2006-07-03)",
    "UNVERIFIED",
    "Inferred: Old Mutual plc appears as an OMXS30 member removed at the July 2006 review, so it must have replaced Skandia under the take-over replacement rule, most likely Feb-Mar 2006. No Nasdaq/OMX notice or press report with the exact date was found; dates left blank. Treat as merger event (G&S-type samples normally exclude).")
add("", "", "Old Mutual plc", "OM", "GB0007389926", "addition",
    "merger replacement (acquirer of Skandia, secondary listing on Stockholmsborsen)", "off-cycle",
    OM_CISION, "company press releases (Old Mutual) + sv.wikipedia OMXS30 table",
    "UNVERIFIED",
    "See E001. Old Mutual was then removed at the July 2006 review (E006). Exact inclusion date not found; left blank.")

# ---- July 2006 review (effective 2006-07-03) ----
j06_note = ("Announcement date unresolved: Frantzich & Nilson (2024, Gothenburg) appendix gives 2006-06-03 (a Saturday, probably a keying error); "
            "sv.wikipedia cites DI market report of 2006-06-30. Lead time in 2006-07 appears to have been only days. Norin & Parksjo (2013, SSE) appendix lists "
            "Boliden and Vostok Nafta inclusions effective 03/07/2006 but Fabege exclusion effective 03/01/2006 (possible day/month slip).")
add("2006-07-03", "", "Boliden AB", "BOL", "", "addition", "semi-annual review", "2006-07",
    WIKI_SV, "sv.wikipedia (citing Dagens Industri 2006-06-30) + two thesis event lists (Gothenburg 2024, SSE 2013)", "SECONDARY", j06_note)
add("2006-07-03", "", "Vostok Nafta Investment Ltd SDB (renamed Vostok Gas Ltd 24 May 2007)", "", "", "addition", "semi-annual review", "2006-07",
    WIKI_SV, "sv.wikipedia (citing DI 2006-06-30) + thesis lists", "SECONDARY", j06_note + " Company renamed Vostok Gas in May 2007 (not an index event).")
add("2006-07-03", "", "Fabege AB ser. B (ex-Drott/Wihlborgs)", "FABG B", "", "deletion", "semi-annual review", "2006-07",
    WIKI_SV, "sv.wikipedia (citing DI 2006-06-30) + thesis lists", "SECONDARY", j06_note)
add("2006-07-03", "", "Old Mutual plc", "OM", "GB0007389926", "deletion", "semi-annual review (low Stockholm turnover after Skandia takeover)", "2006-07",
    WIKI_SV, "sv.wikipedia (citing DI 2006-06-30)", "SECONDARY", "Not in the two thesis lists (they drop merger-related names). " + j06_note)

# ---- Jan 2007 review (effective 2007-01-02) ----
j07_note = "Announcement date: Svenska Dagbladet article 'Scanias B-aktie ar inne' dated 2006-12-27 (cited by sv.wikipedia); Frantzich & Nilson give 2006-12-26 (a Swedish holiday). Lead of only 2-3 trading days."
add("2007-01-02", "2006-12-27", "Scania AB ser. B", "SCV B", "SE0000308280", "addition", "semi-annual review", "2007-01",
    WIKI_SV, "sv.wikipedia (citing SvD 2006-12-27) + thesis lists", "SECONDARY", j07_note)
add("2007-01-02", "2006-12-27", "Holmen AB ser. B", "HOLM B", "SE0000109290", "deletion", "semi-annual review", "2007-01",
    WIKI_SV, "sv.wikipedia (citing SvD 2006-12-27) + thesis lists", "SECONDARY", j07_note)

# ---- July 2007 review (effective 2007-07-02) ----
j07b = "Announcement date 2007-06-26 per Frantzich & Nilson (2024) appendix; sv.wikipedia cites DI market report of 2007-06-29. Short lead (about 4 trading days)."
add("2007-07-02", "2007-06-26", "SSAB AB ser. A", "SSAB A", "SE0000171100", "addition", "semi-annual review", "2007-07",
    WIKI_SV, "sv.wikipedia (citing DI 2007-06-29) + thesis lists", "SECONDARY", j07b)
add("2007-07-02", "2007-06-26", "Stora Enso Oyj ser. R", "STE R", "FI0009005961", "deletion", "semi-annual review", "2007-07",
    WIKI_SV, "sv.wikipedia (citing DI 2007-06-29) + thesis lists", "SECONDARY", j07b)

# ---- Jan 2008 review (effective 2008-01-02) ----
j08 = "Announcement 2007-12-06: Privata Affarer 'Lundin in i finrummet' 6 Dec 2007 (cited by sv.wikipedia) and Frantzich & Nilson appendix. From this review on, the lead was roughly 3-4 weeks."
add("2008-01-02", "2007-12-06", "Lundin Petroleum AB", "LUPE", "SE0000825820", "addition", "semi-annual review", "2008-01",
    "https://www.privataaffarer.se/alla-nyheter/nyheter/lundin-in-i-finrummet-75051/", "Privata Affarer 2007-12-06 (via sv.wikipedia) + thesis lists", "SECONDARY", j08)
add("2008-01-02", "2007-12-06", "Autoliv Inc. SDB", "ALIV SDB", "SE0000382335", "deletion", "semi-annual review", "2008-01",
    "https://www.privataaffarer.se/alla-nyheter/nyheter/lundin-in-i-finrummet-75051/", "Privata Affarer 2007-12-06 (via sv.wikipedia) + thesis lists", "SECONDARY", j08)

# ---- Jan 2009: Vostok Gas out ----
add("2009-01-02", "2008-12-22", "Vostok Gas Ltd SDB", "VGAS SDB", "", "deletion",
    "liquidation/delisting (EGM Dec 2008 approved liquidation and distribution of Gazprom ADRs); removed at the Jan 2009 review date with no replacement", "2009-01",
    "https://www.svd.se/a/3506c472-65c9-3ad6-8299-df05d8c7bdd6/vostok-gas-bort-fran-omxs-30", "Svenska Dagbladet 2008-12-22 (cited by sv.wikipedia); en.wikipedia Vostok Gas", "SECONDARY",
    "Index ran with 29 members from 2 Jan 2009 to 30 Jun 2009 (the July 2009 review then added two and removed one). Not a pure review event; classify as delisting.")

# ---- July 2009 review ----
add("2009-07-01", "2009-06-03", "Getinge AB ser. B", "GETI B", "SE0000202624", "addition", "semi-annual review", "2009-07",
    NQ_2009, "NASDAQ OMX press release 2009-06-03 (ir.nasdaq.com; Swedish version on GlobeNewswire)", "VERIFIED", "Swedish release: " + NQ_2009_SV)
add("2009-07-01", "2009-06-03", "Modern Times Group MTG AB ser. B", "MTG B", "SE0000412371", "addition", "semi-annual review", "2009-07",
    NQ_2009, "NASDAQ OMX press release 2009-06-03", "VERIFIED", "")
add("2009-07-01", "2009-06-03", "Eniro AB", "ENRO", "", "deletion", "semi-annual review", "2009-07",
    NQ_2009, "NASDAQ OMX press release 2009-06-03", "VERIFIED", "")

# ---- 2014: Scania delisting, Kinnevik in ----
add("2014-06-05", "2014-05-21", "Scania AB ser. B", "SCV B", "SE0000308280", "deletion",
    "delisting after Volkswagen takeover and squeeze-out (last trading day 5 June 2014)", "off-cycle",
    SCANIA_DELIST, "Nasdaq Stockholm delisting notice 79/14 (2014-05-21) + sv.wikipedia (citing Privata Affarer 2014-05-21)", "SECONDARY",
    "The delisting notice is verified; the index-removal date (2014-06-05) is from sv.wikipedia. No replacement until the July 2014 review.")
add("2014-07-01", "2014-06-05", "Kinnevik AB ser. B (Investment AB Kinnevik)", "KINV B", "", "addition", "semi-annual review (fills vacancy left by Scania)", "2014-07",
    "https://www.affarsvarlden.se/artikel/stenbeck-bolag-tar-plats-pa-omxs30-6774320", "Affarsvarlden 2014-06-05 (via sv.wikipedia) + Frantzich & Nilson appendix; constituent list of Nasdaq release 2014-12-04 confirms membership", "SECONDARY",
    "Nasdaq release of 2014-06-05 exists but was not retrieved. The Dec 2014 Nasdaq release lists Kinnevik among constituents (https://www.globenewswire.com/news-release/2014/12/04/688561/0/en/SEMI-ANNUAL-REVIEW-OF-THE-OMX-STOCKHOLM-30-INDEX.html).")

# ---- Jan 2016 ----
add("2016-01-04", "2015-12-04", "Fingerprint Cards AB ser. B", "FING B", "", "addition", "semi-annual review", "2016-01",
    NQ_2015, "Nasdaq press release 2015-12-04 (Mondo Visione reproduction)", "VERIFIED", "")
add("2016-01-04", "2015-12-04", "Modern Times Group MTG AB ser. B", "MTG B", "SE0000412371", "deletion", "semi-annual review", "2016-01",
    NQ_2015, "Nasdaq press release 2015-12-04 (Mondo Visione reproduction)", "VERIFIED", "")

# ---- Jan 2017 ----
add("2017-01-02", "2016-12-07", "Autoliv Inc. SDB", "ALIV SDB", "SE0000382335", "addition", "semi-annual review", "2017-01",
    NQ_2016, "Nasdaq press release 2016-12-07 (GlobeNewswire)", "VERIFIED", "")
add("2017-01-02", "2016-12-07", "Nokia Corporation", "NOKIA SEK", "FI0009000681", "deletion", "semi-annual review", "2017-01",
    NQ_2016, "Nasdaq press release 2016-12-07 (GlobeNewswire)", "VERIFIED", "")

# ---- June 2017 Essity spin-off ----
add("2017-06-12", "2017-06-09", "Essity AB ser. B", "ESSITY B", "SE0009922164", "addition",
    "spin-off (distributed by SCA; listed 15 Jun 2017; added as extra constituent, index temporarily 31 names)", "off-cycle",
    NQ_2017, "Nasdaq press release 2017-06-09 (footnote: 'Essity AB ser. B will be added to the OMXS30 index on June 12th, 2017')", "VERIFIED",
    "Announcement date given is the public press release; the GIW index notice may have been earlier. Essity first trading day was 15 June 2017; the release states index addition on 12 June (when-issued/pre-listing). Check price data availability.")

# ---- Jan 2018 ----
add("2018-01-02", "2017-12-07", "Lundin Petroleum AB", "LUPE", "SE0000825820", "deletion", "semi-annual review (no addition; index back from 31 to 30 names)", "2018-01",
    "https://www.di.se/nyheter/lundin-petroleum-petas-fran-omxs30/", "Dagens Industri 2017-12-07 (via sv.wikipedia) + Frantzich & Nilson appendix", "SECONDARY",
    "Nasdaq release of 2017-12-07 exists (business.nasdaq.com/mediacenter/pressreleases/1654602) but could not be fetched.")

# ---- July 2018 ----
add("2018-07-02", "2018-06-07", "Hexagon AB ser. B", "HEXA B", "SE0000103699", "addition", "semi-annual review", "2018-07",
    REALTID_2018, "Realtid 2018-06-07 + Placera telegram 2018-06-07 (via sv.wikipedia) + Frantzich & Nilson appendix", "SECONDARY",
    "Nasdaq release of 2018-06-07 exists (nasdaq.com) but the fetch was rate-limited.")
add("2018-07-02", "2018-06-07", "Fingerprint Cards AB ser. B", "FING B", "", "deletion", "semi-annual review", "2018-07",
    REALTID_2018, "Realtid 2018-06-07 + Placera telegram 2018-06-07 + Frantzich & Nilson appendix", "SECONDARY", "")

# ---- Jan 2021 ----
add("2021-01-04", "2020-12-10", "Evolution Gaming Group AB (now Evolution AB)", "EVO", "SE0012673267", "addition", "semi-annual review", "2021-01",
    NQ_2020, "Nasdaq press release 2020-12-10 (view.news.eu.nasdaq.com)", "VERIFIED", "Release contains a typo ('January 04, 2020'); effective date is Monday 4 Jan 2021.")
add("2021-01-04", "2020-12-10", "SSAB AB ser. A", "SSAB A", "SE0000171100", "deletion", "semi-annual review", "2021-01",
    NQ_2020, "Nasdaq press release 2020-12-10", "VERIFIED", "")

# ---- July 2021 ----
add("2021-07-01", "2021-06-22", "Sinch AB", "SINCH", "", "addition", "semi-annual review", "2021-07",
    PA_2021, "Privata Affarer / Nyhetsbyran Direkt 2021-06-22 quoting Nasdaq press release; Frantzich & Nilson appendix", "SECONDARY",
    "Nasdaq release of 2021-06-22 (nasdaq.com/press-release/...2021-06-22) could not be fetched (rate-limited).")
add("2021-07-01", "2021-06-22", "Securitas AB ser. B", "SECU B", "SE0000163594", "deletion", "semi-annual review", "2021-07",
    PA_2021, "Privata Affarer / Direkt 2021-06-22; DI 2021-06-23 (via sv.wikipedia)", "SECONDARY", "Frantzich & Nilson wrongly list Securitas under the June 2022 announcement.")

# ---- July 2022 ----
add("2022-07-01", "2022-06-22", "Samhallsbyggnadsbolaget i Norden AB ser. B (SBB)", "SBB B", "SE0009554454", "addition", "semi-annual review", "2022-07",
    NQ_2022, "Nasdaq press release 2022-06-22 (Mondo Visione reproduction); Privata Affarer 2022-06-23", "VERIFIED", "")
add("2022-07-01", "2022-06-22", "Skanska AB ser. B", "SKA B", "SE0000113250", "deletion", "semi-annual review", "2022-07",
    NQ_2022, "Nasdaq press release 2022-06-22 (Mondo Visione reproduction); Privata Affarer 2022-06-23", "VERIFIED", "")

# ---- Nov 2022 Swedish Match ----
add("2022-11-18", "2022-11-16", "Swedish Match AB", "SWMA", "SE0000310336", "deletion",
    "acquisition by Philip Morris International (offer unconditional 7 Nov 2022; PMI above 90% late Nov; delisted Dec 2022); no replacement until Jan 2023 review", "off-cycle",
    SWMA_CAPIQ, "S&P Capital IQ item 2022-11-16 'removed from OMX Stockholm 30 Index' (MarketScreener) + sv.wikipedia (citing DI 2022-11-21) for the 2022-11-18 effective date", "SECONDARY",
    "Nasdaq GIW notice not retrieved; effective date 2022-11-18 is from sv.wikipedia. Index ran with 29 names until 2 Jan 2023.")

# ---- Jan 2023 ----
add("2023-01-02", "2022-12-22", "NIBE Industrier AB ser. B", "NIBE B", "SE0015988019", "addition", "semi-annual review (fills vacancy left by Swedish Match)", "2023-01",
    NQ_2022D, "Nasdaq press release 2022-12-22 (nasdaq.com); Placera 2022-12-23", "VERIFIED", "No deletion at this review.")

# ---- July 2024 ----
add("2024-07-01", "2024-06-20", "Saab AB ser. B", "SAAB B", "SE0000112385", "addition", "semi-annual review", "2024-07",
    NQ_2024, "Nasdaq press release 2024-06-20 (view.news.eu.nasdaq.com)", "VERIFIED", "")
add("2024-07-01", "2024-06-20", "Autoliv Inc. SDB", "ALIV SDB", "SE0000382335", "deletion", "semi-annual review", "2024-07",
    NQ_2024, "Nasdaq press release 2024-06-20", "VERIFIED", "")

# ---- July 2025 (new methodology) ----
r25 = "semi-annual review; first reconstitution under the free-float methodology effective 1 Jul 2025 (methodology change announced 5 May 2025)"
for comp, tic, isin in [("Addtech AB ser. B", "ADDT B", "SE0014781795"), ("Epiroc AB ser. A", "EPI A", "SE0015658109"),
                        ("EQT AB", "EQT", "SE0012853455"), ("Industrivarden AB ser. C", "INDU C", "SE0000190126"),
                        ("Lifco AB ser. B", "LIFCO B", "SE0015949201"), ("Skanska AB ser. B", "SKA B", "SE0000113250")]:
    add("2025-07-01", "2025-06-23", comp, tic, isin, "addition", r25, "2025-07", NQ_2025,
        "Nasdaq press release 2025-06-23 (view.news.eu.nasdaq.com; also Mondo Visione, Placera, Avanza blog)", "VERIFIED", "")
for comp, tic, isin, extra in [("Atlas Copco AB ser. B", "ATCO B", "SE0017486897", "Removed because only one share class per company is allowed under the new methodology; Atlas Copco A stays."),
                               ("Electrolux AB ser. B", "ELUX B", "SE0016589188", ""), ("Getinge AB ser. B", "GETI B", "SE0000202624", ""),
                               ("Kinnevik AB ser. B", "KINV B", "SE0015810247", ""), ("Samhallsbyggnadsbolaget i Norden AB ser. B (SBB)", "SBB B", "SE0009554454", ""),
                               ("Sinch AB", "SINCH", "", "")]:
    add("2025-07-01", "2025-06-23", comp, tic, isin, "deletion", r25, "2025-07", NQ_2025,
        "Nasdaq press release 2025-06-23", "VERIFIED", extra)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(cols)
    w.writerows(rows)

print(len(rows), "rows written")
from collections import Counter
print(Counter(r[11] for r in rows))
print(Counter(r[1][:4] for r in rows))
print(Counter(r[6] for r in rows))
