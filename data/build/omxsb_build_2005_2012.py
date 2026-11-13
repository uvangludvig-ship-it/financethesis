#!/usr/bin/env python3
"""
omxsb_build_2005_2012.py - regenerate omxsb_changes_2005_2012.csv from the SOURCES table below.

Backward extension of omxsb_build.py (2013-2026). Same columns, same vocabulary, same rule:
every row is traceable to one entry in SOURCES (one entry per review release), and
additions and deletions are typed in exactly as the release lists them. Nothing is
inferred from index membership snapshots or from the LSEG index feed.

Schedule note (differs from 2013-2026): until the January 2009 review the index was
revised by OMX AB / Stockholmsborsen with new portfolios effective on the first
trading day of JANUARY and JULY (Swedish exchange notices "Ny sammansattning av OMX
Stockholm Benchmark index", numbered Aktier/Avista nnn/yy). From the May 2009 review
NASDAQ OMX moved to the June/December schedule. The review effective 2 Jan 2009 is
therefore labelled 2009JAN so that it does not clash with 2009H1 (effective 1 Jun 2009).
review_cycle = half-year of the EFFECTIVE date (2007H2 = effective 2 Jul 2007,
2008H1 = effective 2 Jan 2008), as in the 2013-2026 file where H1 = June, H2 = December.

Usage:
    python3 omxsb_build_2005_2012.py                 # writes data/input/omxsb/omxsb_changes_2005_2012.csv
    python3 omxsb_build_2005_2012.py --include-reversed
    python3 omxsb_build_2005_2012.py --summary
    python3 omxsb_build_2005_2012.py --check         # chain check, also joined with the 2013-2026 file

Verification levels (same as omxsb_build.py):
    VERIFIED  - lists read from the exchange's own release text (GlobeNewswire/Hugin copy of
                the OMX market notice incl. its PDF attachment, Nasdaq OMX release on
                GlobeNewswire, ir.nasdaq.com, or a verbatim republication on mondovisione.com).
    SECONDARY - lists read from a newswire report only (none in this file).
"""
import argparse
import csv
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from omxsb_build import COLUMNS, trading_days_between  # noqa: E402  (shared calendar + columns)

OUT_CSV = os.path.join(HERE, "..", "..", "data", "input", "omxsb", "omxsb_changes_2005_2012.csv")
PREV_CSV = os.path.join(HERE, "..", "..", "data", "input", "omxsb", "omxsb_changes_2013_2026.csv")

# ----------------------------------------------------------------------------
# SOURCES: one entry per review. Items are (company_as_written, ticker, isin) or
# (company_as_written, ticker, isin, per-item note). ISINs are given only by the
# OMX-era notices (2007-2008); the Nasdaq OMX releases 2009-2012 do not give them.
# Announcement times: GlobeNewswire shows US Eastern time; CET/CEST = ET + 6 h.
# ----------------------------------------------------------------------------

GNW = "https://www.globenewswire.com"

SOURCES = [
    dict(
        cycle="2007H2", announced="2007-06-12", announce_time="12:29 CEST (during trading)", effective="2007-07-02",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2007/06/12/116558/0/sv/avista-ny-sammans%c3%a4ttning-av-omx-stockholm-benchmark-index-175-07.html",
        source_note="Stockholmsborsen AB market notice Aktier 175/07 'Ny sammansattning av OMX Stockholm Benchmark index' (Hugin/GlobeNewswire, PDF attachment wkr0001.pdf fileId=195221); lists identical in the correction 183/07 of 2007-06-25 (TWW SDB B was missing from the Excel attachment and stays in the index; PDF .../2007/06/25/116692/0/sv/files/193995/0/wkr0001.pdf)",
        adds=[("Ängpanneföreningen, AB ser. B", "ANGP B", "SE0000115578"), ("Boss Media AB", "BOSS", "SE0000488850"),
              ("Kaupthing Bank", "KAUP SEK", "IS0000001469"), ("PA Resources", "PAR SEK", "SE0000818569"),
              ("Tanganyika Oil Company Ltd. SDB", "TYKS SDB", "SE0001134537"), ("West Siberian Resources Ltd", "WSIB SDB", "SE0000739286")],
        dels=[("Broström AB ser. B", "BRO B", "SE0000254880"), ("Husqvarna AB ser. A", "HUSQ A", "SE0001662222"),
              ("ReadSoft AB ser. B", "RSOF B", "SE0000479107"), ("SECTRA AB ser B", "SECT B", "SE0000408189"),
              ("Stora Enso Oyj ser. A", "STE A", "FI0009007603"), ("Stora Enso Oyj ser. R", "STE R", "FI0009007611"),
              ("Wihlborgs Fastighteter AB", "WIHL", "SE0001413600", "name misspelt in the notice (Wihlborgs Fastigheter AB)")],
    ),
    dict(
        cycle="2008H1", announced="2007-12-14", announce_time="12:00 CET (during trading)", effective="2008-01-02",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2007/12/14/118048/0/sv/avista-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-287-07.html",
        source_note="OMX Nordic Exchange Stockholm market notice Aktier 287/07 'Ny sammansattning av OMX Stockholm Benchmark index' (Hugin/GlobeNewswire, PDF attachment wkr0001.pdf fileId=176761); English version 'Equities: New composition of OMX Stockholm Benchmark index (287/07)' id 118047",
        adds=[("Cybercom Group Europe AB", "CYBE", "SE0000702169"), ("Husqvarna AB ser. A", "HUSQ A", "SE0001662222"),
              ("Svenska Cellulosa AB SCA ser. A", "SCA A", "SE0000171886")],
        dels=[("AarhusKarlshamn AB", "AAK", "SE0001493776"), ("Cision AB", "CSN", "SE0000291486"),
              ("NOCOM AB ser. B", "NOCM B", "SE0000373128"), ("Sigma AB ser. B", "SIGM B", "SE0000835217")],
    ),
    dict(
        cycle="2008H2", announced="2008-06-11", announce_time="13:00 CEST (during trading)", effective="2008-07-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2008/06/11/119843/0/sv/avista-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-142-08.html",
        source_note="OMX Nordic Exchange Stockholm market notice Aktier 142/08 'Ny sammansattning av OMX Stockholm Benchmark index' (Hugin/GlobeNewswire, PDF attachment .../2008/06/11/119843/0/sv/files/154957/0/wkr0003.pdf); lists identical in the update 148/08 of 2008-06-16 (number of shares for IBS B; .../2008/06/16/119887/0/sv/files/154582/0/wkr0003.pdf)",
        adds=[("AarhusKarlshamn AB", "AAK", "SE0001493776"), ("AddNode AB ser. B", "ANOD B", "SE0000472268"),
              ("Betsson AB ser. B", "BETS B", "SE0000102378"), ("Connecta AB", "CNTA", "SE0001161530"),
              ("Cision AB", "CSN", "SE0000291486"), ("Atrium Ljungberg AB ser. B", "LJGR B", "SE0000191827"),
              ("Wihlborgs Fastigheter AB", "WIHL", "SE0001413600")],
        dels=[("Gunnebo AB", "GUNN", "SE0000195570"), ("HEXPOL AB ser. B", "HPOL B", "SE0002452623"),
              ("Lundin Mining Corporation SDB", "LUMI SDB", "SE0001134529"), ("Nobia AB", "NOBI", "SE0000949331")],
    ),
    dict(
        cycle="2009JAN", announced="2008-12-11", announce_time="09:30 CET (during trading); correction 12:35 CET", effective="2009-01-02",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2008/12/11/121680/0/sv/avista-korrigering-ny-sammans%C3%A4ttning-av-omx-stockholm-benchmark-index-294-08.html",
        source_note="NASDAQ OMX Stockholm market notice Aktier 293/08 'Ny sammansattning av OMX Stockholm Benchmark index' (.../2008/12/11/121676/0/sv/files/136223/0/wkr0003.pdf) as corrected the same day by 294/08 (PDF fileId=136174): Stora Enso A and Sigma B are NOT included; last review on the January/July schedule",
        adds=[("Rederi AB Transatlantic ser. B", "RABT B", "SE0000143521"), ("Tricorona AB", "TRIC", "SE0001493693")],
        dels=[("AarhusKarlshamn AB", "AAK", "SE0001493776"), ("D. Carnegie & Co AB", "CAR", "SE0000798829"),
              ("Cision AB", "CSN", "SE0000291486"), ("Hexagon AB ser. B", "HEXA B", "SE0000103699"),
              ("Husqvarna AB ser. A", "HUSQ A", "SE0001662222"), ("Loomis AB ser. B", "LOOM B", "SE0002683557"),
              ("Öresund, Investment AB", "ORES", "SE0000115610"), ("PA Resources", "PAR SEK", "SE0000818569"),
              ("Semcon AB", "SEMC", "SE0000379497"), ("Teleca AB ser. B", "TELC B", "SE0000366254"),
              ("Transcom WorldWide S.A SDB ser. B", "TWW SDB B", "SE0000818031"), ("Vostok Gas Ltd. SDB", "VGAS SDB", "SE0000367823")],
        reversed_adds=[("Sigma AB ser. B", "SIGM B", "SE0000835217", "announced in 293/08 2008-12-11 09:30 CET, withdrawn by correction 294/08 the same day 12:35 CET"),
                       ("Stora Enso Oyj ser. A", "STE A", "FI0009007603", "announced in 293/08 2008-12-11 09:30 CET, withdrawn by correction 294/08 the same day 12:35 CET")],
    ),
    dict(
        cycle="2009H1", announced="2009-05-11", announce_time="16:14 CEST (during trading)", effective="2009-06-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2009/05/11/2584/0/da/New-OMX-Stockholm-Benchmark-portfolio-selected.html",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (GlobeNewswire, with the full 81-name constituent table); identical on https://ir.nasdaq.com/news-releases/news-release-details/new-omx-stockholm-benchmark-portfolio-selected and in the Swedish version (.../2584/0/sv/); first review on the June/December schedule",
        adds=[("Loomis AB", "LOOM B", ""), ("Net Entertainment NE AB", "NET B", ""), ("PA Resources", "PAR SEK", ""),
              ("Transcom WorldWide S.A", "TWW SDB B", "")],
        dels=[("Cybercom Group Europe", "CYBE", ""), ("Nokia", "NOKI SEK", ""), ("Rederi AB Transatlantic", "RABT B", "")],
    ),
    dict(
        cycle="2009H2", announced="2009-11-09", announce_time="13:00 CET (during trading)", effective="2009-12-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2009/11/09/142934/0/en/new-omx-stockholm-benchmark-portfolio-selected.html",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark portfolio selected' (GlobeNewswire); identical on Mondo Visione https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-stoc-2011124/",
        adds=[("AarhusKarlshamn AB", "AAK", ""), ("Cybercom Group Europe AB", "CYBE", ""), ("Hexagon AB", "HEXA B", ""),
              ("Proffice AB", "PROE B", ""), ("Investment AB Öresund", "ORES", "")],
        dels=[("Addnode AB", "ANOD B", ""), ("LBI International AB", "LBI", ""), ("Tricorona AB", "TRIC", "")],
    ),
    dict(
        cycle="2010H1", announced="2010-05-07", announce_time="14:30 CEST (during trading)", effective="2010-06-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2010/05/07/167938/0/en/new-omx-stockholm-benchmark-portfolio-selected.html",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark Portfolio Selected' (GlobeNewswire); identical in the release PDF on https://ir.nasdaq.com/static-files/1cfd8887-6154-4b78-8585-a94e64e30582",
        adds=[("Active Biotech AB", "ACTI", ""), ("Arise Windpower", "AWP", ""), ("Biovitrum AB", "BVT", ""), ("Gunnebo AB", "GUNN", ""),
              ("Höganäs AB ser. B", "HOGA B", ""), ("Klövern AB", "KLOV", ""), ("Lundin Mining Corporation SDB", "LUMI SDB", ""),
              ("Proact IT Group AB", "PACT", "")],
        dels=[("AarhusKarlshamn AB", "AAK", ""), ("Hexagon AB ser. B", "HEXA B", ""), ("PA Resources", "PAR SEK", ""),
              ("Transcom WorldWide S.A SDB ser. B", "TWW SDB", "", "ticker printed as TWW SDB (TWW SDB B in the 2009 releases)")],
    ),
    dict(
        cycle="2010H2", announced="2010-11-08", announce_time="14:30 CET (during trading)", effective="2010-12-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2010/11/08/189068/0/en/new-omx-stockholm-benchmark-portfolio-selected.html",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark Portfolio Selected' (GlobeNewswire); identical on Mondo Visione https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-2011124/",
        adds=[("Rederi AB TransAtlantic", "RABT B", "")],
        dels=[("Höganäs AB", "HOGA B", ""), ("Millicom International Cellular S.A.", "MIC SDB", ""),
              ("Investment AB Öresund", "ORES", ""), ("Proffice AB", "PROE B", "")],
    ),
    dict(
        cycle="2011H1", announced="2011-05-09", announce_time="09:00 CEST (at the open)", effective="2011-06-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2011/05/09/214538/0/en/new-omx-stockholm-benchmark-portfolio-selected.html",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark Portfolio Selected' (GlobeNewswire); identical on https://ir.nasdaq.com/news-releases/news-release-details/new-omx-stockholm-benchmark-portfolio-selected-2",
        adds=[("Addnode AB", "ANOD B", ""), ("Etrion Corporation", "ETX", ""), ("Hexagon AB", "HEXA B", ""), ("Höganäs AB", "HOGA B", ""),
              ("Medivir AB", "MVIR B", ""), ("Millicom International Cellular", "MIC SDB", ""), ("Proffice AB", "PROE B", "")],
        dels=[("CDON Group AB", "CDON", ""), ("Cybercom Group AB", "CYBE", ""), ("Enea AB", "ENEA", ""), ("Eniro AB", "ENRO", ""),
              ("Gunnebo AB", "GUNN", ""), ("Nokia Corporation", "NOKI SEK", ""), ("Svenska Cellulosa AB SCA ser A.", "SCA A", ""),
              ("Swedish Orphan Biovitrum AB", "SOBI", "")],
    ),
    dict(
        cycle="2011H2", announced="2011-11-10", announce_time="09:30 CET (during trading)", effective="2011-12-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2011/11/10/237112/0/en/new-omx-stockholm-benchmark-portfolio-selected.html",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark Portfolio Selected' (GlobeNewswire); identical on Mondo Visione https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-1-20111110/",
        adds=[("Nobia AB", "NOBI", ""), ("Opcon AB", "OPCO", ""), ("ReadSoft AB ser. B", "RSOF B", ""),
              ("Svenska Cellulosa AB SCA ser. A.", "SCA A", ""), ("Sigma AB ser. B", "SIGM B", "")],
        dels=[("Active Biotech AB", "ACTI", ""), ("EnQuest Plc", "ENQ", ""), ("Medivir AB ser. B", "MVIR B", ""),
              ("Rezidor Hotel Group AB", "REZT", ""), ("SSAB AB ser. B", "SSAB B", "")],
    ),
    dict(
        cycle="2012H1", announced="2012-05-07", announce_time="13:20 CEST (during trading)", effective="2012-06-01",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2012/05/07/262074/0/en/new-composition-of-omx-stockholm-benchmark-index.html",
        source_note="NASDAQ OMX Index Operations notice 'New composition of OMX Stockholm Benchmark Index' (GlobeNewswire, PDF attachment 2012-05-07_OMXSB-Review.pdf); same counts (11 in, 24 out) reported by Dagens industri 2012-05-07 'De kastas ut fran toppindex'",
        adds=[("AarhusKarlshamn AB", "AAK", ""), ("Billerud AB", "BILL", ""), ("Cloetta AB ser. B", "CLA B", ""),
              ("Fastighets AB Balder ser. B", "BALD B", ""), ("HEXPOL AB ser. B", "HPOL B", ""), ("Mekonomen AB", "MEKO", ""),
              ("NCC AB ser. B", "NCC B", ""), ("NIBE Industrier AB ser. B", "NIBE B", ""), ("Rezidor Hotel Group AB", "REZT", ""),
              ("Stora Enso Oyj ser. R", "STE R", ""), ("Trigon Agri A/S", "TAGR", "")],
        dels=[("Acando AB ser. B", "ACAN B", ""), ("Addnode AB ser. B", "ANOD B", ""), ("Axfood AB", "AXFO", ""), ("Connecta AB", "CNTA", ""),
              ("Hakon Invest AB", "HAKN", ""), ("HiQ International AB", "HIQ", ""), ("Industrial & Financial Systems AB ser. B", "IFS B", ""),
              ("Klövern AB", "KLOV", ""), ("Know IT AB", "KNOW", ""), ("Loomis AB ser. B", "LOOM B", ""), ("Nobia AB", "NOBI", ""),
              ("Opcon AB", "OPCO", ""), ("Oriflame Cosmetics S.A, SDB", "ORI SDB", ""), ("Proact IT Group AB", "PACT", ""),
              ("Proffice AB ser. B", "PROE B", ""), ("ReadSoft AB ser. B", "RSOF B", ""), ("Rederi AB Transatlantic ser. B", "RABT B", ""),
              ("SAS AB", "SAS", ""), ("Securitas AB ser. B", "SECU B", ""), ("Sigma AB ser. B", "SIGM B", ""),
              ("Svenska Cellulosa AB SCA ser. A", "SCA A", ""), ("Tieto Corporation", "TIEN", ""), ("TradeDoubler AB", "TRAD", ""),
              ("ÅF AB ser. B", "AF B", "")],
    ),
    dict(
        cycle="2012H2", announced="2012-11-09", announce_time="09:00 CET (at the open)", effective="2012-12-03",
        verification="VERIFIED",
        source_url=GNW + "/news-release/2012/11/09/503912/0/en/new-omx-stockholm-benchmark-portfolio-selected.html",
        source_note="Nasdaq OMX release 'New OMX Stockholm Benchmark Portfolio Selected' (GlobeNewswire); identical on Mondo Visione https://mondovisione.com/media-and-resources/news/new-omx-stockholm-benchmark-portfolio-selected-the-new-portfolio-of-the-omx-st-3-2012119/",
        adds=[("Black Earth Farming Ltd. SDB", "BEF SDB", ""), ("Klövern AB", "KLOV", ""), ("Nokia Corporation", "NOKI SEK", "")],
        dels=[("Fastighets AB Balder ser. B", "BALD B", ""), ("Trigon Agri A/S", "TAGR", "")],
    ),
]

# Reviews in the 2005-2012 window for which no release or report could be found.
MISSING = [
    ("2005H1 (effective 2005-01-03)", "SBX-era Stockholmsborsen notice; not on Cision, Hugin/GlobeNewswire, Wayback or in indexed press"),
    ("2005H2 (effective 2005-07-01)", "SBX-era Stockholmsborsen notice; not on Cision, Hugin/GlobeNewswire, Wayback or in indexed press"),
    ("2006H1 (effective 2006-01-02)", "OMX Stockholm Benchmark notice; not on Cision, Hugin/GlobeNewswire, mynewsdesk, Wayback or in indexed press"),
    ("2006H2 (effective 2006-07-03)", "OMX notice; not on Cision, Hugin/GlobeNewswire, mynewsdesk, Wayback or in indexed press"),
    ("2007H1 (effective 2007-01-02)", "OMX notice of Dec 2006; Hugin/GlobeNewswire archive for OMX Stockholm starts Jan 2007; not on mynewsdesk, Wayback or in indexed press"),
]


def build_rows(include_reversed=False):
    rows = []
    for src in sorted(SOURCES, key=lambda s: s["effective"]):
        base_note = src["source_note"] + "; announcement " + src["announce_time"]
        seq = 0

        def unpack(item, typ):
            if len(item) == 4:
                return (item[0], item[1], item[2], typ, item[3])
            return (item[0], item[1], item[2], typ, "")

        items = [unpack(x, "addition") for x in src["adds"]] + [unpack(x, "deletion") for x in src["dels"]]
        if include_reversed:
            items += [unpack(x, "addition_reversed") for x in src.get("reversed_adds", [])]
            items += [unpack(x, "deletion_reversed") for x in src.get("reversed_dels", [])]
        for company, ticker, isin, typ, extra in items:
            seq += 1
            note = base_note + ("; " + extra if extra else "")
            rows.append({
                "event_id": f"OMXSB-{src['cycle']}-{seq:02d}",
                "effective_date": src["effective"],
                "announcement_date": src["announced"],
                "company": company,
                "ticker": ticker,
                "isin": isin,
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
    for src in sorted(SOURCES, key=lambda s: s["effective"]):
        a = dt.date.fromisoformat(src["announced"])
        e = dt.date.fromisoformat(src["effective"])
        lead = trading_days_between(a, e)
        na, nd = len(src["adds"]), len(src["dels"])
        tot_a += na
        tot_d += nd
        print(f"{src['cycle']:8} {src['announced']:11} {src['effective']:11} {lead:7d} {na:5d} {nd:5d} {src['verification']:10}")
    print(f"total reviews={len(SOURCES)} additions={tot_a} deletions={tot_d} events={tot_a + tot_d}")
    for cyc, why in MISSING:
        print(f"missing: {cyc}: {why}")


# Ticker spellings that differ between releases for the same security (used only by --check).
TICKER_ALIASES = {"TWW SDB": "TWW SDB B", "NOKIA SEK": "NOKI SEK"}


def check(rows, joined=None):
    """Membership-chain check (same as omxsb_build.check). With joined=rows of the 2013-2026
    file the chain runs across both files."""
    allrows = list(rows) + list(joined or [])
    by = {}
    for r in allrows:
        if r["type"] not in ("addition", "deletion"):
            continue
        t = TICKER_ALIASES.get(r["ticker"], r["ticker"])
        by.setdefault(t, []).append((r["effective_date"], r["type"], r["review_cycle"]))
    problems = []
    for t, ev in by.items():
        state = None
        for d, typ, c in sorted(ev):
            if typ == "addition" and state == "in":
                problems.append((t, "added while already in", d, c))
            if typ == "deletion" and state == "out":
                problems.append((t, "deleted while already out", d, c))
            state = "in" if typ == "addition" else "out"
    print(f"chain check ({'2005-2026 joined' if joined else '2005-2012 only'}): {len(by)} tickers, {len(problems)} problems")
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
        if os.path.exists(PREV_CSV):
            with open(PREV_CSV, newline="", encoding="utf-8") as f:
                prev = list(csv.DictReader(f))
            check(rows, joined=prev)


if __name__ == "__main__":
    main()
