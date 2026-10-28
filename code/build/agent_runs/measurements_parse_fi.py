"""Parse FI VPFO quarterly holdings XML files into two CSVs:
  out/fi_funds_<q>.csv    one row per fund (name, ISIN, institutnr, quarter, NAV, benchmark)
  out/fi_holdings_<q>.csv one row per (fund, instrument ISIN) aggregated across lots
Usage: python -I parse_fi.py <data_root> <out_dir> <quarter_tag>...
"""
import sys, os, csv, glob
import xml.etree.ElementTree as ET

NS = {"v": "http://schemas.fi.se/publika/vardepappersfonder/20200331"}

def txt(el, path):
    x = el.find(path, NS)
    if x is None or x.text is None:
        return ""
    return x.text.strip()

def fnum(s):
    try:
        return float(s)
    except Exception:
        return float("nan")

def parse_file(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return None, None, f"parse error {e}"
    root = tree.getroot()
    q = txt(root, "v:Rapportinformation/v:Kvartalsslut")
    fb = txt(root, "v:Bolagsinformation/v:Fondbolag_namn")
    fi = root.find("v:Fondinformation", NS)
    if fi is None:
        return None, None, "no Fondinformation"
    fund = {
        "quarter_end": q,
        "fondbolag": fb,
        "fund_instnr": txt(fi, "v:Fond_institutnummer"),
        "fund_isin": txt(fi, "v:Fond_ISIN-kod"),
        "fund_name": txt(fi, "v:Fond_namn"),
        "nav_sek": txt(fi, "v:Fondförmögenhet"),
        "cash_sek": txt(fi, "v:Likvida_medel"),
        "active_risk": txt(fi, "v:Aktiv_risk"),
        "benchmark": " | ".join(
            (x.text or "").strip() for x in fi.findall("v:Jämförelseindex/v:Jämförelseindex", NS)
        ),
        "file": os.path.basename(path).encode("utf-8", "replace").decode("utf-8", "replace"),
    }
    hold = {}
    for ins in fi.findall("v:FinansiellaInstrument/v:FinansielltInstrument", NS):
        isin = txt(ins, "v:ISIN-kod_instrument")
        name = txt(ins, "v:Instrumentnamn")
        key = isin if isin else "NOISIN:" + name
        mv = fnum(txt(ins, "v:Marknadsvärde_instrument"))
        n = fnum(txt(ins, "v:Antal"))
        sh = fnum(txt(ins, "v:Andel_av_fondförmögenhet_instrument"))
        px = fnum(txt(ins, "v:Kurs_som_använts_vid_värdering_av_instrumentet"))
        fx = fnum(txt(ins, "v:Valutakurs_instrument"))
        d = hold.setdefault(key, {
            "isin": isin, "name": name,
            "asset_class": txt(ins, "v:Tillgångsslag_enligt_LVF_5_kap"),
            "country": txt(ins, "v:Landkod_Emittent"),
            "ccy": txt(ins, "v:Valuta"),
            "sector": txt(ins, "v:Bransch/v:Bransch_namn_instrument"),
            "mv_sek": 0.0, "shares": 0.0, "weight_pct": 0.0, "price": px, "fx": fx,
        })
        if mv == mv:
            d["mv_sek"] += mv
        if n == n:
            d["shares"] += n
        if sh == sh:
            d["weight_pct"] += sh
    return fund, hold, ""

def main():
    data_root, out_dir = sys.argv[1], sys.argv[2]
    tags = sys.argv[3:]
    for tag in tags:
        files = glob.glob(os.path.join(data_root, f"fi_{tag}", "**", "*.xml"), recursive=True)
        funds, rows, errs = [], [], []
        for p in sorted(files):
            fund, hold, err = parse_file(p)
            if fund is None:
                errs.append((p, err)); continue
            fund["n_holdings"] = len(hold)
            funds.append(fund)
            for k, d in hold.items():
                rows.append({"fund_instnr": fund["fund_instnr"], "fund_isin": fund["fund_isin"],
                             "fund_name": fund["fund_name"], "quarter_end": fund["quarter_end"],
                             "nav_sek": fund["nav_sek"], **d})
        with open(os.path.join(out_dir, f"fi_funds_{tag}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(funds[0].keys())); w.writeheader(); w.writerows(funds)
        with open(os.path.join(out_dir, f"fi_holdings_{tag}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        print(tag, "funds", len(funds), "holding rows", len(rows), "errors", len(errs))
        for e in errs[:10]:
            print("  ERR", e)

if __name__ == "__main__":
    main()
