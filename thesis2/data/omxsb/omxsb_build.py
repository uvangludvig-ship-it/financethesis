#!/usr/bin/env python3
"""
omxsb_build.py - regenerate omxsb_changes_2013_2026.csv from the SOURCES table below.

Every row in the CSV is traceable to one entry in SOURCES (one entry per Nasdaq
review release or, where no release could be read, per secondary report).
Nothing is inferred: additions and deletions are typed in exactly as the
release (or the secondary report) lists them.

Usage:
    python3 omxsb_build.py                 # writes omxsb_changes_2013_2026.csv next to this file
    python3 omxsb_build.py --include-reversed
                                           # also emits changes that were announced and then
                                           # reversed before the effective date (type suffix "_reversed")
    python3 omxsb_build.py --summary       # prints counts per review and the announcement lead

Verification levels:
    VERIFIED  - lists read from the Nasdaq release text (GlobeNewswire, view.news.eu.nasdaq.com,
                nasdaq.com, or a verbatim republication of the release on mondovisione.com /
                loomis.us / finanznachrichten.de). The source_url points at the copy that was read.
    SECONDARY - lists read from a Swedish newswire report (Finwire via Placera, Nyhetsbyran
                Direkt via Aktiespararna/EFN, Swedbank Aktiellt) because the Nasdaq release
                itself could not be fetched. Tickers for SECONDARY rows were assigned by the
                builder from Nasdaq Stockholm ticker conventions and are flagged in `notes`.
"""
import argparse
import csv
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(HERE, "omxsb_changes_2013_2026.csv")

# ----------------------------------------------------------------------------
# Swedish trading calendar (Nasdaq Stockholm closed days) for lead calculation
# ----------------------------------------------------------------------------

def easter(year):
    """Anonymous Gregorian algorithm."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(year, month, day)


def midsummer_eve(year):
    # Friday between 19 and 25 June
    d = dt.date(year, 6, 19)
    while d.weekday() != 4:
        d += dt.timedelta(days=1)
    return d


def stockholm_holidays(year):
    e = easter(year)
    hol = {
        dt.date(year, 1, 1), dt.date(year, 1, 6),
        e - dt.timedelta(days=2), e + dt.timedelta(days=1),
        dt.date(year, 5, 1), e + dt.timedelta(days=39),
        dt.date(year, 6, 6), midsummer_eve(year),
        dt.date(year, 12, 24), dt.date(year, 12, 25), dt.date(year, 12, 26),
        dt.date(year, 12, 31),
    }
    return hol


def is_trading_day(d):
    return d.weekday() < 5 and d not in stockholm_holidays(d.year)


def trading_days_between(announce, effective):
    """Number of trading days strictly after `announce` and strictly before `effective`,
    plus 1 (so that T-6 convention: announcement on the 6th trading day before the
    effective date gives 6). Equivalently: count of trading days in (announce, effective]."""
    n = 0
    d = announce + dt.timedelta(days=1)
    while d <= effective:
        if is_trading_day(d):
            n += 1
        d += dt.timedelta(days=1)
    return n


# ----------------------------------------------------------------------------
# SOURCES: one entry per review. Lists copied from the release / report.
# Each add/del item is (company_as_written, ticker). ISINs are never given in
# the 2013-2026 releases, so the CSV isin column is left blank.
# ----------------------------------------------------------------------------

SOURCES = [
    dict(
        cycle="2013H1", announced="2013-05-08", announce_time="08:30 CET (pre-open)", effective="2013-06-03",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/nasdaq-omx-nordic-new-omx-stockholm-benchmark-portfolio-selected-the-new-port-201358/",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (Mondo Visione verbatim copy)",
        adds=[("Fastighets AB Balder ser. B", "BALD B"), ("SAS AB", "SAS")],
        dels=[("Black Earth Farming Ltd. SDB", "BEF SDB"), ("Etrion Corporation", "ETX"), ("Klövern AB", "KLOV"),
              ("Lundbergföretagen AB, L E ser. B", "LUND B"), ("SkiStar AB ser. B", "SKIS B")],
    ),
    dict(
        cycle="2013H2", announced="2013-11-07", announce_time="08:30 CET (pre-open)", effective="2013-12-02",
        verification="VERIFIED",
        source_url="https://www.globenewswire.com/news-release/2013/11/07/587625/0/en/NEW-OMX-STOCKHOLM-BENCHMARK-PORTFOLIO-SELECTED.html",
        source_note="Nasdaq OMX release on GlobeNewswire; Mondo Visione copy at .../new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-4-2013117/",
        adds=[("Axis AB", "AXIS"), ("EnQuest PLC", "ENQ"), ("Eniro AB", "ENRO"), ("Etrion Corporation", "ETX"),
              ("Swedish Orphan Biovitrum", "SOBI"), ("Trelleborg AB Ser B", "TREL B")],
        dels=[("Arise AB", "ARISE")],
    ),
    dict(
        cycle="2014H1", announced="2014-05-08", announce_time="08:30 CET (pre-open)", effective="2014-06-02",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-5-201458/",
        source_note="Nasdaq OMX release (Mondo Visione verbatim copy)",
        adds=[("Arise AB", "ARISE"), ("Hemfosa Fastigheter AB", "HEMF")],
        dels=[("AXIS AB", "AXIS"), ("SAS AB", "SAS")],
    ),
    dict(
        cycle="2014H2", announced="2014-11-10", announce_time="08:30 CET (pre-open)", effective="2014-12-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-6-20141110/",
        source_note="Nasdaq OMX release (Mondo Visione verbatim copy)",
        adds=[("Africa Oil Corp.", "AOI"), ("Klövern AB", "KLOV"), ("Lundbergföretagen AB, L E ser. B", "LUND B"),
              ("SSAB AB ser. B", "SSAB B"), ("Scandi Standard AB", "SCST"), ("Tethys Oil AB", "TETY")],
        dels=[("EnQuest PLC", "ENQ"), ("Eniro AB", "ENRO"), ("Ratos AB ser. B", "RATO B"), ("Stora Enso Oyj ser. R", "STE R")],
    ),
    dict(
        cycle="2015H1", announced="2015-05-07", announce_time="08:30 CET (pre-open)", effective="2015-06-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-7-201557/",
        source_note="Nasdaq release (Mondo Visione verbatim copy); lists re-read verbatim in a second fetch",
        adds=[("Haldex AB", "HLDX"), ("Sagax AB B", "SAGA B"), ("Securitas AB ser. B", "SECU B"), ("Stora Enso Oyj ser. R", "STE R")],
        dels=[("Arise AB", "ARISE"), ("Klövern AB Ser. A", "KLOV A"), ("Lundin Mining Corporation SDB", "LUMI SDB"),
              ("Mekonomen AB", "MEKO"), ("Scandi Standard AB", "SCST"), ("Tethys Oil AB", "TETY"), ("Volvo, AB ser. A", "VOLV A")],
    ),
    dict(
        cycle="2015H2", announced="2015-11-10", announce_time="08:30 CET (pre-open)", effective="2015-12-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-8-20151110/",
        source_note="Nasdaq release (Mondo Visione copy); identical lists on https://www.loomis.us/resources/press-releases-news/omx-stockholm-benchmark-portfolio-selected",
        adds=[("Fingerprint Cards AB ser. B", "FING B"), ("Klövern AB Ser. B", "KLOV B"), ("Loomis AB ser. B", "LOOM B"),
              ("Mekonomen AB", "MEKO"), ("Pandox AB ser. B", "PNDX B"), ("SAAB AB ser. B", "SAAB B"), ("Volvo, AB ser. A", "VOLV A")],
        dels=[("Haldex AB", "HLDX"), ("Nokia Corporation", "NOKIA SEK"), ("Rezidor Hotel Group AB", "REZT")],
    ),
    dict(
        cycle="2016H1", announced="2016-05-10", announce_time="08:30 CET (pre-open)", effective="2016-06-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-9-2016510/",
        source_note="Nasdaq release (Mondo Visione verbatim copy)",
        adds=[("ATTENDO AB", "ATT"), ("ICA Gruppen", "ICA"), ("Latour, Investmentab. ser. B", "LATO B"), ("Recipharm AB ser. B", "RECI B"),
              ("SAS AB", "SAS"), ("Thule Group AB", "THULE"), ("Vitrolife AB", "VITR")],
        dels=[("Etrion Corporation", "ETX")],
    ),
    dict(
        cycle="2016H2", announced="2016-11-10", announce_time="08:30 CET (pre-open)", effective="2016-12-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-20161110/",
        source_note="Nasdaq release (Mondo Visione verbatim copy)",
        adds=[("Ahlsell AB", "AHSL"), ("BioGaia AB ser. B", "BIOG B"), ("Bonava AB ser. B", "BONAV B"), ("Capio AB", "CAPIO"),
              ("DOMETIC GROUP AB", "DOM"), ("Granges AB", "GRNG"), ("Melker Schorling AB", "MELK"),
              ("RaySearch Laboratories AB ser. B", "RAY B"), ("Rezidor Hotel Group AB", "REZT"), ("Scandic Hotels Group AB", "SHOT")],
        dels=[("Loomis AB ser. B", "LOOM B"), ("Mekonomen AB", "MEKO"), ("SAS AB", "SAS"), ("Thule Group AB", "THULE")],
    ),
    dict(
        cycle="2017H1", announced="2017-05-09", announce_time="08:30 CET (pre-open)", effective="2017-06-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-1-201759/",
        source_note="Nasdaq release 9 May 2017 (Mondo Visione copy). Correction 17 May 2017: SAAB B stays in the index (https://mondovisione.com/media-and-resources/news/correction-new-omx-stockholm-benchmark-portfolio-selected-2017517/)",
        adds=[("Ambea AB", "AMBEA"), ("Axfood AB", "AXFO"), ("D. Carnegie & Co AB B", "DCAR B"), ("Hansa Medical AB", "HMED"),
              ("Mekonomen AB", "MEKO"), ("Peab AB ser. B", "PEAB B"), ("SkiStar AB ser. B", "SKIS B")],
        dels=[("Ahlsell AB", "AHSL"), ("Klovern AB Ser. B", "KLOV B"), ("Melker Schorling AB", "MELK"), ("Rezidor Hotel Group AB", "REZT")],
        reversed_dels=[("SAAB AB ser. B", "SAAB B", "announced 2017-05-09, withdrawn by correction 2017-05-17")],
    ),
    dict(
        cycle="2017H2", announced="2017-11-10", announce_time="08:30 CET (pre-open)", effective="2017-12-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-2-20171110/",
        source_note="Nasdaq release (Mondo Visione copy); same lists in Nyhetsbyran Direkt via Aktiespararna/Placera 2017-11-10",
        adds=[("Ahlsell AB", "AHSL"), ("Biotage AB", "BIOT"), ("CellaVision AB", "CEVI"), ("Catena Media P.L.C", "CTM"),
              ("Evolution Gaming Group AB", "EVO"), ("Karo Pharma AB", "KARO"), ("Klovern AB Ser. B", "KLOV B"),
              ("Medicover AB ser. B", "MCOV B"), ("SAS AB", "SAS")],
        dels=[("Ambea AB", "AMBEA"), ("D. Carnegie & Co AB B", "DCAR B"), ("Mekonomen AB", "MEKO"), ("SAAB AB ser. B", "SAAB B"),
              ("SkiStar AB ser. B", "SKIS B")],
    ),
    dict(
        cycle="2018H1", announced="2018-05-08", announce_time="08:30 CET (pre-open)", effective="2018-06-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-3-201858/",
        source_note="Nasdaq release (Mondo Visione verbatim copy)",
        adds=[("AddLife AB ser. B", "ALIF B"), ("Arjo AB ser. B", "ARJO B"), ("Bilia AB ser. A", "BILI A"), ("D. Carnegie & Co AB B", "DCAR B"),
              ("LeoVegas AB", "LEO"), ("Thule Group AB", "THULE")],
        dels=[("Africa Oil Corp.", "AOI"), ("Latour, Investmentab. ser. B", "LATO B"), ("NCC AB ser. B", "NCC B"),
              ("RaySearch Laboratories AB ser. B", "RAY B"), ("Sagax AB B", "SAGA B"), ("Stora Enso Oyj ser. R", "STE R")],
    ),
    dict(
        cycle="2018H2", announced="2018-11-12", announce_time="08:30 CET (pre-open)", effective="2018-12-03",
        verification="VERIFIED",
        source_url="https://www.globenewswire.com/news-release/2018/11/12/1649397/0/en/New-OMX-Stockholm-Benchmark-Portfolio-Selected.html",
        source_note="Nasdaq release on GlobeNewswire; Mondo Visione copy .../new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-4-20181112/",
        adds=[("Epiroc AB ser. A", "EPI A"), ("Epiroc AB ser. B", "EPI B"), ("Latour, Investment ab. ser. B", "LATO B"), ("SAAB AB ser. B", "SAAB B"),
              ("Sagax AB B", "SAGA B"), ("SECTRA AB ser B", "SECT B"), ("SkiStar AB ser. B", "SKIS B"), ("Stora Enso Oyj ser. R", "STE R"),
              ("Tethys Oil AB", "TETY"), ("Veoneer Inc. SDB", "VNE SDB")],
        dels=[("Bilia AB ser. A", "BILI A"), ("Fingerprint Cards AB ser. B", "FING B"), ("Klovern AB Ser. B", "KLOV B"),
              ("Lundbergforetagen AB, L E ser. B", "LUND B"), ("Medicover AB ser. B", "MCOV B"), ("Thule Group AB", "THULE")],
    ),
    dict(
        cycle="2019H1", announced="2019-05-13", announce_time="08:30 CET (pre-open)", effective="2019-06-03",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-5-2019513/",
        source_note="Nasdaq release (Mondo Visione copy); same lists in Realtid 2019-05-14 (https://www.realtid.se/forandringar-i-omx-stockholm-benchmark-index/)",
        adds=[("Bilia AB ser. A", "BILI A"), ("International Petroleum Corporation", "IPCO"), ("Klovern AB Ser. B", "KLOV B"),
              ("Lundbergforetagen AB, L E ser. B", "LUND B"), ("Nordic Entertainment Group ser. B", "NENT B"), ("Nyfosa AB", "NYF")],
        dels=[("Atrium Ljungberg AB ser. B", "ATRLJ B"), ("Bonava AB ser. B", "BONAV B"), ("Catena Media P.L.C", "CTM"), ("Intrum AB", "INTRUM"),
              ("Karo Pharma AB", "KARO"), ("LeoVegas AB", "LEO"), ("SAS AB", "SAS"), ("Tethys Oil AB", "TETY")],
    ),
    dict(
        cycle="2019H2", announced="2019-11-11", announce_time="08:30 CET (pre-open)", effective="2019-12-02",
        verification="VERIFIED",
        source_url="https://www.nasdaq.com/press-release/new-omx-stockholm-benchmark-portfolio-selected-2019-11-11",
        source_note="Nasdaq release on nasdaq.com; Mondo Visione copy .../new-omx-stockholm-benchmark-portfolio-selected-new-portfolio-of-the-omx-stockh-6-20191111/",
        adds=[("Atrium Ljungberg AB ser. B", "ATRLJ B"), ("Catena AB", "CATE"), ("EQT AB", "EQT"), ("Fingerprint Cards AB ser. B", "FING B"),
              ("Loomis AB ser. B", "LOOM B"), ("SWECO AB ser. B", "SWEC B")],
        dels=[("Bilia AB ser. A", "BILI A"), ("Hembla AB ser. B", "HEM B"), ("International Petroleum Corporation", "IPCO"),
              ("Latour, Investmentab. ser. B", "LATO B"), ("Peab AB ser. B", "PEAB B"), ("SSAB AB ser. A", "SSAB A"),
              ("Millicom International Cellular S.A. SDB", "TIGO SDB")],
    ),
    dict(
        cycle="2020H1", announced="2020-05-14", announce_time="08:30 CEST (pre-open)", effective="2020-06-01",
        verification="VERIFIED",
        source_url="https://view.news.eu.nasdaq.com/view?id=bdf4cc2c820c3b12852b88ca0c810b60f&lang=en",
        source_note="Nasdaq release 'Nasdaq Selects New OMX Stockholm Benchmark Portfolio' on view.news.eu.nasdaq.com",
        adds=[("Indutrade AB", "INDT"), ("Lifco AB ser. B", "LIFCO B"), ("Oncopeptides AB", "ONCO"), ("Medicover AB ser. B", "MCOV B"),
              ("Arise AB", "ARISE"), ("Samhällsbyggnadsbo. i Norden AB ser. B", "SBB B")],
        dels=[("Atrium Ljungberg AB ser. B", "ATRLJ B"), ("Hansa Biopharma AB", "HNSA"), ("Loomis AB ser. B", "LOOM B"),
              ("SAAB AB ser. B", "SAAB B"), ("Scandic Hotels Group AB", "SHOT")],
    ),
    dict(
        cycle="2020H2", announced="2020-11-10", announce_time="morning (pre-open, per Aktiellt)", effective="2020-12-01",
        verification="SECONDARY",
        source_url="https://www.swedbank-aktiellt.se/2020/november/manga_forandringar_i_omxsb-indexet.csp",
        source_note="Swedbank Aktiellt 2020-11-10 10:42 'Manga forandringar i OMXSB-indexet' reporting the Nasdaq release of the same morning; Nasdaq release itself not retrievable (nasdaq.com rate-limited, not on Mondo Visione)",
        tickers_assigned=True,
        adds=[("Academedia", "ACAD"), ("ÅF Pöyry", "AF B"), ("BHG Group", "BHG"), ("Bilia", "BILI A"), ("Bravida", "BRAV"), ("Camurus", "CAMX"),
              ("Cellink", "CLNK B"), ("Eolus Vind", "EOLU B"), ("Hansa Biopharma", "HNSA"), ("Lagercrantz Group", "LAGR B"), ("Millicom", "TIGO SDB"),
              ("Mips", "MIPS"), ("Mycronic", "MYCR"), ("Nobia", "NOBI"), ("Peab", "PEAB B"), ("Sinch", "SINCH"), ("Thule", "THULE"),
              ("Vitec", "VIT B"), ("Xvivo Perfusion", "XVIVO")],
        dels=[("Axfood", "AXFO"), ("Lifco", "LIFCO B"), ("Cellavision", "CEVI"), ("Skistar", "SKIS B"), ("Cloetta", "CLA B"),
              ("SSAB, serie B", "SSAB B"), ("Fingerprint Cards", "FING B"), ("Volvo, serie A", "VOLV A")],
    ),
    dict(
        cycle="2021H1", announced="2021-05-21", announce_time="evening (after close, per Finwire)", effective="2021-06-01",
        verification="SECONDARY",
        source_url="https://www.placera.se/placera/telegram/2021/05/24/academedia-nasdaq-justerar-om-i-omx-stockholm-benchmark-index-oms.html",
        source_note="Finwire telegram (first sent Friday evening 2021-05-21, re-sent 2021-05-24) via Placera; also borsvarlden.com 2021-05-21 16:34 UTC. Nasdaq release not retrievable (nasdaq.com rate-limited)",
        tickers_assigned=True,
        adds=[("Addnode", "ANOD B"), ("Bonava B", "BONAV B"), ("Etrion", "ETX"), ("Fingerprint Cards", "FING B"), ("Hemnet", "HEM"),
              ("International Petroleum", "IPCO"), ("Latour", "LATO B"), ("Nordnet", "SAVE"), ("SSAB B", "SSAB B")],
        dels=[("Academedia", "ACAD"), ("Attendo", "ATT"), ("Betsson", "BETS B"), ("Industrivärden A", "INDU A"), ("Stora Enso R", "STE R")],
    ),
    dict(
        cycle="2021H2", announced="2021-11-23", announce_time="18:00 CET (after close)", effective="2021-12-01",
        verification="VERIFIED",
        source_url="https://view.news.eu.nasdaq.com/view?id=b147597c4972dde112c64e62f434f296b&lang=en",
        source_note="Nasdaq release on view.news.eu.nasdaq.com; same lists on finanznachrichten.de (54569570) and Dagens Bors 2021-11-24",
        adds=[("Addtech AB ser. B", "ADDT B"), ("Lifco AB Ser. B", "LIFCO B"), ("Africa Oil Corp.", "AOI"), ("Mekonomen AB", "MEKO"),
              ("Cibus Nordic Real Estate AB", "CIBUS"), ("Stillfront Group AB", "SF"), ("Cint Group AB", "CINT"),
              ("Storskogen Group AB ser. B", "STOR B"), ("CTEK AB", "CTEK"), ("Troax Group AB", "TROAX"), ("Dios AB", "DIOS"),
              ("Truecaller AB ser. B", "TRUE B")],
        dels=[("Addnode Group AB ser. B", "ANOD B"), ("Lundbergforetagen AB, L E ser. B", "LUND B"), ("Camurus AB", "CAMX"), ("Nobia AB", "NOBI"),
              ("Eolus Vind AB, ser. B", "EOLU B"), ("Oncopeptides AB", "ONCO"), ("Etrion Corporation", "ETX"), ("Nordnet AB", "SAVE"),
              ("Hemnet Group AB", "HEM"), ("Millicom International Cellular", "TIGO SDB"), ("Hansa Biopharma AB", "HNSA"),
              ("Xvivo Perfusion AB", "XVIVO")],
    ),
    dict(
        cycle="2022H1", announced="2022-05-23", announce_time="18:00 CEST (after close)", effective="2022-06-01",
        verification="VERIFIED",
        source_url="https://www.nasdaq.com/press-release/nasdaq-announces-semi-annual-changes-to-the-omx-stockholm-benchmark-index-2022-05-23",
        source_note="Nasdaq release on nasdaq.com; also finanznachrichten.de (56120676)",
        adds=[("Addnode Group AB ser. B", "ANOD B"), ("Axfood AB", "AXFO"), ("Fortnox AB", "FNOX"), ("Heba Fastighets AB ser. B", "HEBA B"),
              ("Industrivärden, AB ser. A", "INDU A"), ("Karnov Group AB", "KAR"), ("Lindab International AB", "LIAB"),
              ("Lundbergföretagen AB, L E ser. B", "LUND B"), ("New Wave Group AB ser. B", "NEWA B"), ("OX2 AB", "OX2"),
              ("Volvo Car AB ser. B", "VOLCAR B")],
        dels=[("AFRY AB", "AFRY"), ("BICO Group AB", "BICO"), ("Bonava AB ser. B", "BONAV B"), ("Bravida Holding AB", "BRAV"), ("CTEK AB", "CTEK"),
              ("Fingerprint Cards AB ser. B", "FING B"), ("Medicover AB ser. B", "MCOV B"), ("Mekonomen AB", "MEKO"), ("Mycronic AB", "MYCR"),
              ("Storskogen Group AB ser. B", "STOR B"), ("Troax Group AB", "TROAX")],
    ),
    dict(
        cycle="2022H2", announced="2022-11-21", announce_time="18:00 CET (after close); Finwire report next morning", effective="2022-12-01",
        verification="SECONDARY",
        source_url="https://www.placera.se/telegram/nasdaq-justerar-om-i-omx-stockholm-benchmark-index-2022-11-22",
        source_note="Finwire telegram 2022-11-22 via Placera. Announcement date from the Nasdaq release link tweeted 2022-11-21 19:05 CET (x.com/ekkalundin/status/1594753946479902725). Nasdaq release not retrievable (nasdaq.com rate-limited, Mondo Visione copy not indexed)",
        tickers_assigned=True,
        adds=[("AFRY", "AFRY"), ("Atrium Ljungberg", "ATRLJ B"), ("Beijer Ref", "BEIJ B"), ("BioArctic", "BIOA B"), ("Boozt", "BOOZT"),
              ("Bravida", "BRAV"), ("Camurus", "CAMX"), ("CTEK", "CTEK"), ("Eolus Vind", "EOLU B"), ("Hemnet", "HEM"), ("Hexatronic", "HTRO"),
              ("Medicover", "MCOV B"), ("Mycronic", "MYCR"), ("Platzer", "PLAZ B"), ("Saab", "SAAB B"), ("Solid Försäkring", "SFAB"),
              ("Tethys Oil", "TETY"), ("Volvo A", "VOLV A")],
        dels=[("Addtech", "ADDT B"), ("BHG Group", "BHG"), ("BioGaia", "BIOG B"), ("Corem", "CORE B"), ("Heba", "HEBA B"), ("Latour", "LATO B"),
              ("Lindab", "LIAB"), ("Lifco", "LIFCO B"), ("Peab", "PEAB B"), ("Truecaller", "TRUE B")],
    ),
    dict(
        cycle="2023H1", announced="2023-05-23", announce_time="18:00 CEST (after close)", effective="2023-06-01",
        verification="VERIFIED",
        source_url="https://view.news.eu.nasdaq.com/view?id=be1e3832f84b20bb2b14416bc14f0c439&lang=en",
        source_note="Nasdaq release on view.news.eu.nasdaq.com; identical on finanznachrichten.de (59160570)",
        adds=[("Addtech AB ser. B", "ADDT B"), ("BioGaia AB ser. B", "BIOG B"), ("Embracer Group AB ser. B", "EMBRAC B"), ("Lifco AB ser. B", "LIFCO B"),
              ("Sampo Plc SDB", "SAMPO SDB"), ("SSAB AB ser. A", "SSAB A"), ("Millicom International Cellular S.A. SDB", "TIGO SDB")],
        dels=[("Biotage AB", "BIOT"), ("Camurus AB", "CAMX"), ("Cibus Nordic Real Estate AB", "CIBUS"), ("Cint Group AB", "CINT"), ("CTEK AB", "CTEK"),
              ("Hexatronic Group AB", "HTRO"), ("Karnov Group AB", "KAR"), ("Lundbergföretagen AB, L E ser. B", "LUND B"),
              ("Securitas AB ser. B", "SECU B"), ("Volvo, AB ser. A", "VOLV A")],
    ),
    dict(
        cycle="2023H2", announced="2023-11-23", announce_time="18:00 CET (after close)", effective="2023-12-01",
        verification="VERIFIED",
        source_url="https://view.news.eu.nasdaq.com/view?id=be007a57f33d4d52541bfc529d8b21f55&lang=en",
        source_note="Nasdaq release 23 Nov 2023; UPDATE 29 Nov 2023 (finanznachrichten.de 60793469): JM stays in the index, Karnov not added. Final lists exclude the two reversed items",
        adds=[("Camurus AB", "CAMX", "release prints ticker as 'CMAX' (sic); Nasdaq ticker is CAMX"), ("Munters Group AB", "MTRS"), ("Cibus Nordic Real Estate AB", "CIBUS"), ("NCAB Group AB", "NCAB"),
              ("Securitas AB ser. B", "SECU B"), ("Lundbergföretagen AB, L E ser. B", "LUND B")],
        dels=[("AFRY AB", "AFRY"), ("Boozt AB", "BOOZT"), ("Addnode Group AB ser. B", "ANOD B"), ("Arjo AB ser. B", "ARJO B"),
              ("Platzer Fastigheter Holding AB ser. B", "PLAZ B"), ("Beijer Ref AB ser. B", "BEIJ B"), ("SSAB AB ser. A", "SSAB A")],
        reversed_adds=[("Karnov Group AB", "KAR", "announced 2023-11-23, withdrawn by UPDATE 2023-11-29")],
        reversed_dels=[("JM AB", "JM", "announced 2023-11-23, withdrawn by UPDATE 2023-11-29")],
    ),
    dict(
        cycle="2024H1", announced="2024-05-24", announce_time="18:00 CEST (after close)", effective="2024-06-03",
        verification="VERIFIED",
        source_url="https://view.news.eu.nasdaq.com/view?id=b465a30d4561f8f31f15763b0f6dc7ae6&lang=en",
        source_note="Nasdaq release on view.news.eu.nasdaq.com; Mondo Visione copy .../nasdaq-announces-semi-annual-changes-to-omx-stockholm-benchmark-index-2-2024524/",
        adds=[("Addnode Group AB ser. B", "ANOD B"), ("AFRY AB", "AFRY"), ("Biotage AB", "BIOT"), ("Bonesupport Holding AB", "BONEX"), ("Boozt AB", "BOOZT"),
              ("Lindab International AB", "LIAB"), ("SSAB AB ser. A", "SSAB A"), ("VBG Group AB ser. B", "VBG B")],
        dels=[("BioArctic AB ser. B", "BIOA B"), ("BioGaia AB ser. B", "BIOG B"), ("Bravida Holding AB", "BRAV"), ("Lundbergföretagen AB, L E ser. B", "LUND B"),
              ("NCAB Group AB", "NCAB"), ("Securitas AB ser. B", "SECU B"), ("Stillfront Group AB", "SF"), ("Tethys Oil AB", "TETY")],
    ),
    dict(
        cycle="2024H2", announced="2024-11-22", announce_time="18:00 CET (after close)", effective="2024-12-02",
        verification="VERIFIED",
        source_url="https://view.news.eu.nasdaq.com/view?id=b8d5c1243d98f7e08a9438dd230a204e7&lang=en",
        source_note="Nasdaq release on view.news.eu.nasdaq.com; also nasdaq.com (…-2024-11-22), Mondo Visione (…-3-20241122), Finwire/EFN 2024-11-25",
        adds=[("Alleima AB", "ALLEI"), ("Beijer Ref AB ser. B", "BEIJ B"), ("Betsson AB ser. B", "BETS B"), ("Bravida Holding AB", "BRAV"),
              ("Clas Ohlson AB ser. B", "CLAS B"), ("MEKO AB", "MEKO"), ("NP3 Fastigheter AB", "NP3"), ("Securitas AB ser. B", "SECU B"),
              ("Xvivo Perfusion AB", "XVIVO")],
        dels=[("AFRY AB", "AFRY"), ("Biotage AB", "BIOT"), ("Kinnevik AB ser. B", "KINV B"), ("Solid Försäkringsaktiebolag", "SFAB"),
              ("SSAB AB ser. A", "SSAB A"), ("Millicom International Cellular S.A. SDB", "TIGO SDB"), ("VBG GROUP AB ser. B", "VBG B")],
    ),
    dict(
        cycle="2025H1", announced="2025-05-22", announce_time="18:00 CEST (after close)", effective="2025-06-02",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/nasdaq-announces-semi-annual-changes-to-omx-stockholm-benchmark-index-2025522/",
        source_note="Nasdaq release (Mondo Visione verbatim copy); same lists Finwire/MarketScreener 2025-05-23",
        adds=[("AFRY AB", "AFRY"), ("Asker Healthcare Group AB", "ASKER"), ("BioGaia AB ser. B", "BIOG B"), ("NCC AB ser. B", "NCC B"), ("Rusta AB", "RUSTA"),
              ("Solid Försäkringsaktiebolag", "SFAB"), ("Swedish Logistic Property AB ser. B", "SLP B"), ("SSAB AB ser. A", "SSAB A"),
              ("Synsam AB", "SYNSAM"), ("Truecaller AB ser. B", "TRUE B")],
        dels=[("Beijer Ref AB ser. B", "BEIJ B"), ("Boozt AB", "BOOZT"), ("Fortnox AB", "FNOX"), ("Gränges AB", "GRNG"), ("Lindab International AB", "LIAB")],
    ),
    dict(
        cycle="2025H2", announced="2025-11-21", announce_time="18:00 CET (after close)", effective="2025-12-01",
        verification="VERIFIED",
        source_url="https://mondovisione.com/media-and-resources/news/nasdaq-announces-semi-annual-changes-to-omx-stockholm-benchmark-index-20251121/",
        source_note="Nasdaq release (Mondo Visione verbatim copy); same lists Finwire/MarketScreener 2025-11-24",
        adds=[("AcadeMedia AB", "ACAD"), ("BioArctic AB ser. B", "BIOA B"), ("Boozt AB", "BOOZT"), ("Cloetta AB ser. B", "CLA B"), ("Gränges AB", "GRNG"),
              ("Platzer Fastigheter Holding AB ser. B", "PLAZ B"), ("Scandic Hotels Group AB", "SHOT"), ("VBG GROUP AB ser. B", "VBG B")],
        dels=[("Arise AB", "ARISE"), ("BioGaia AB ser. B", "BIOG B"), ("Bravida Holding AB", "BRAV"), ("MEKO AB", "MEKO"), ("Rusta AB", "RUSTA"),
              ("Solid Försäkringsaktiebolag", "SFAB"), ("SSAB AB ser. A", "SSAB A"), ("Truecaller AB ser. B", "TRUE B"), ("Xvivo Perfusion AB", "XVIVO")],
    ),
    dict(
        cycle="2026H1", announced="2026-05-22", announce_time="18:00 CEST (after close)", effective="2026-06-01",
        verification="VERIFIED",
        source_url="https://view.news.eu.nasdaq.com/view?id=b49024270d6eeb2f3f1ae80c5fea1dae7&lang=en",
        source_note="Nasdaq release on view.news.eu.nasdaq.com; identical on Mondo Visione (…-2026522) and Finwire/Borsvarlden 2026-05-25",
        adds=[("Attendo AB", "ATT"), ("Beijer Ref AB ser. B", "BEIJ B"), ("Bravida Holding AB", "BRAV"), ("Hacksaw AB", "HACK"),
              ("Intea Fastigheter AB ser. B", "INTEA B"), ("Lundin Gold Inc.", "LUG"), ("Maha Capital AB", "MAHA A"), ("NCAB Group AB", "NCAB"),
              ("Solid Försäkringsaktiebolag", "SFAB"), ("Sivers Semiconductors AB", "SIVE"), ("SSAB AB ser. A", "SSAB A")],
        dels=[("AcadeMedia AB", "ACAD"), ("AFRY AB", "AFRY"), ("Addnode Group AB ser. B", "ANOD B"), ("Billerud Aktiebolag", "BILL"),
              ("Eolus Aktiebolag ser. B", "EOLU B"), ("Indutrade AB", "INDT"), ("NCC AB ser. B", "NCC B"), ("Norion Bank AB", "NORION"),
              ("Sampo Plc A", "SAMPO SEK"), ("Samhällsbyggnadsbo. i Norden AB ser. B", "SBB B"), ("Vitec Software Group AB ser. B", "VIT B"),
              ("Vitrolife AB", "VITR")],
    ),
]

# Reviews in the 2013-2026 window with no release and no reliable secondary source.
MISSING = [
    ("2026H2", "reference date 2026-10-30; announcement expected 2026-11-20 (6th trading day before 2026-12-01); not yet announced as of 2026-10-11"),
]

COLUMNS = ["event_id", "effective_date", "announcement_date", "company", "ticker", "isin", "type",
           "review_cycle", "source_url", "verification", "notes"]


def build_rows(include_reversed=False):
    rows = []
    for src in sorted(SOURCES, key=lambda s: s["effective"]):
        base_note = src["source_note"]
        if src.get("tickers_assigned"):
            base_note += "; ticker assigned by builder (not in source)"
        base_note += "; announcement " + src["announce_time"]
        seq = 0

        def unpack(item, typ):
            # items are (company, ticker) or (company, ticker, per-item note)
            if len(item) == 3:
                return (item[0], item[1], typ, item[2])
            return (item[0], item[1], typ, "")

        items = [unpack(x, "addition") for x in src["adds"]] + [unpack(x, "deletion") for x in src["dels"]]
        if include_reversed:
            items += [(c, t, "addition_reversed", n) for c, t, n in src.get("reversed_adds", [])]
            items += [(c, t, "deletion_reversed", n) for c, t, n in src.get("reversed_dels", [])]
        for company, ticker, typ, extra in items:
            seq += 1
            note = base_note + ("; " + extra if extra else "")
            rows.append({
                "event_id": f"OMXSB-{src['cycle']}-{seq:02d}",
                "effective_date": src["effective"],
                "announcement_date": src["announced"],
                "company": company,
                "ticker": ticker,
                "isin": "",
                "type": typ,
                "review_cycle": src["cycle"],
                "source_url": src["source_url"],
                "verification": src["verification"],
                "notes": note,
            })
    return rows


def summary():
    print(f"{'cycle':8} {'announced':11} {'effective':11} {'lead_td':7} {'adds':5} {'dels':5} {'verif':10}")
    tot_a = tot_d = 0
    nver = 0
    for src in sorted(SOURCES, key=lambda s: s["effective"]):
        a = dt.date.fromisoformat(src["announced"])
        e = dt.date.fromisoformat(src["effective"])
        lead = trading_days_between(a, e)
        na, nd = len(src["adds"]), len(src["dels"])
        tot_a += na
        tot_d += nd
        if src["verification"] == "VERIFIED":
            nver += na + nd
        print(f"{src['cycle']:8} {src['announced']:11} {src['effective']:11} {lead:7d} {na:5d} {nd:5d} {src['verification']:10}")
    print(f"total reviews={len(SOURCES)} additions={tot_a} deletions={tot_d} events={tot_a + tot_d} verified={nver}")
    for cyc, why in MISSING:
        print(f"missing: {cyc}: {why}")


def check(rows):
    """Membership-chain check: for each ticker, additions and deletions must alternate
    (a name cannot be added twice without a deletion in between, or deleted twice without
    an addition). A name whose first event is a deletion was in the index before 2013.
    Any violation points at a misread list and is printed."""
    by = {}
    for r in rows:
        if r["type"] not in ("addition", "deletion"):
            continue
        by.setdefault(r["ticker"], []).append((r["effective_date"], r["type"], r["review_cycle"]))
    problems = []
    for t, ev in by.items():
        state = None
        for d, typ, c in sorted(ev):
            if typ == "addition" and state == "in":
                problems.append((t, "added while already in", d, c))
            if typ == "deletion" and state == "out":
                problems.append((t, "deleted while already out", d, c))
            state = "in" if typ == "addition" else "out"
    print(f"chain check: {len(by)} tickers, {len(problems)} problems")
    for p in problems:
        print("  ", p)
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-reversed", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out", default=OUT_CSV)
    args = ap.parse_args()
    rows = build_rows(include_reversed=args.include_reversed)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {args.out}")
    if args.summary:
        summary()
    if args.check:
        check(rows)


if __name__ == "__main__":
    main()
