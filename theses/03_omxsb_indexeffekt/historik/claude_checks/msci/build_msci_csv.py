import csv

dates = {
 "2017-02": ("2017-02-09", "2017-02-28"),
 "2017-05": ("2017-05-15", "2017-05-31"),
 "2017-08": ("2017-08-10", "2017-08-31"),
 "2017-11": ("2017-11-13", "2017-11-30"),
 "2018-02": ("2018-02-12", "2018-02-28"),
 "2018-05": ("2018-05-14", "2018-05-31"),
 "2018-08": ("2018-08-13", "2018-08-31"),
 "2018-11": ("2018-11-13", "2018-11-30"),
 "2019-02": ("2019-02-11", "2019-02-28"),
 "2019-05": ("2019-05-13", "2019-05-28"),
 "2019-08": ("2019-08-07", "2019-08-27"),
 "2019-11": ("2019-11-07", "2019-11-26"),
 "2020-02": ("2020-02-12", "2020-02-28"),
 "2020-05": ("2020-05-12", "2020-05-29"),
 "2020-08": ("2020-08-12", "2020-08-31"),
 "2020-11": ("2020-11-10", "2020-11-30"),
 "2021-02": ("2021-02-09", "2021-02-26"),
 "2021-05": ("2021-05-11", "2021-05-27"),
 "2021-08": ("2021-08-11", "2021-08-31"),
 "2021-11": ("2021-11-11", "2021-11-30"),
}

PB = "section spans page break; columns assigned via Sweden summary count ({a} add/{d} del)"

# (review, segment) -> (additions, deletions, note for all rows, per-name notes)
data = {
 ("2017-05","SC"): (["AHLSELL","BUFAB","CHERRY B","HANSA MEDICAL","LEOVEGAS","PARADOX INTERACTIVE","VICTORIA PARK B","VOLATI"],
                    ["CONCENTRIC","LIFCO B"], "summary count SWEDEN 8 2 matches", {}),
 ("2017-11","SC"): (["BIOTAGE","MUNTERS GROUP B"],
                    ["DUNI","KAMBI GROUP","MAGNOLIA BOSTAD","TETHYS OIL"], "summary count SWEDEN 2 4 matches", {}),
 ("2018-02","SC"): ([], ["ARCAM"], "summary count SWEDEN 0 1 matches", {}),
 ("2018-05","ST"): ([], ["GETINGE B"], "", {"GETINGE B": "added to SC same review"}),
 ("2018-05","SC"): (["GETINGE B","ONCOPEPTIDES AB","STILLFRONT GROUP","STORYTEL B","TROAX GROUP"],
                    ["BERGMAN & BEVING B","FINGERPRINT CARDS B","GUNNEBO","KAPPAHL"],
                    "page break between heading and names; summary count SWEDEN 5 4 matches", {"GETINGE B": "deleted from ST same review"}),
 ("2018-11","SC"): (["CELLAVISION AB","FORTNOX","KAMBI GROUP","KARO PHARMA"],
                    ["BYGGMAX GROUP","ITAB SHOP CONCEPT","STARBREEZE B"], "summary count SWEDEN 4 3 matches", {}),
 ("2019-05","SC"): (["ACANDO B","BOOZT","CLIMEON B","FINGERPRINT CARDS B","LIFCO B","SAGAX D","THQ NORDIC B","XVIVO PERFUSION"],
                    ["ELANDERS","VICTORIA PARK B"], "summary count SWEDEN 8 2 matches", {}),
 ("2019-11","SC"): (["AMBEA AB","ATRIUM LJUNGBERG B","BEIJER REF","BIOARCTIC B","CATENA","JOHN MATTSON","POWERCELL SWEDEN","SAMHALLSBYGGNADSBOLAGE D"],
                    ["CATENA MEDIA","HALDEX","PROBI AB","VOLATI"], "summary count SWEDEN 8 4 matches",
                    {"SAMHALLSBYGGNADSBOLAGE D": "name truncated as printed (Samhallsbyggnadsbolaget i Norden D)"}),
 ("2020-05","ST"): (["EQT AB","EVOLUTION GAMING GROUP","LATOUR INVESTMENT B","NIBE INDUSTRIER B","SCA B"],
                    ["MILLICOM INTL CELL SDR"], "summary count SWEDEN 5 1 matches",
                    {"EVOLUTION GAMING GROUP":"deleted from SC same review","NIBE INDUSTRIER B":"deleted from SC same review","SCA B":"deleted from SC same review","MILLICOM INTL CELL SDR":"added to SC same review"}),
 ("2020-05","SC"): (["ADDTECH","CELLINK B","CIBUS NORDIC REAL ESTATE","COOR SERVICE MGMT","CREADES","DUNI","HMS NETWORKS AB","INSTALCO","KFAST HOLDING B","MILLICOM INTL CELL SDR","MIPS","SEDANA MEDICAL AB","SINCH"],
                    ["CLIMEON B","ELTEL","EVOLUTION GAMING GROUP","HOIST FINANCE","HUMANA AB","NEW WAVE GROUP B","NIBE INDUSTRIER B","RAYSEARCH LABORATORIES B","SCA B"],
                    "columns run together in text; split checked vs summary count SWEDEN 13 9", {}),
 ("2020-11","ST"): (["FASTIGHETS AB BALDER B","INDUSTRIVARDEN A"], [], "summary count SWEDEN 2 0 matches",
                    {"FASTIGHETS AB BALDER B":"deleted from SC same review"}),
 ("2020-11","SC"): (["BACTIGUARD HOLDING B","BETTER COLLECTIVE","BHG GROUP","BONESUPPORT HOLDING","CALLIDITAS THERAPEUTICS","CANTARGIA","GARO","IMMUNOVIA","INVISIO","KNOW IT AB","LIME TECHNOLOGIES","PLATZER FASTIGHETER B","SDIPTECH B","SVOLDER B"],
                    ["FASTIGHETS AB BALDER B"],
                    "page break between heading and names; assigned via summary count SWEDEN 14 1",
                    {"FASTIGHETS AB BALDER B":"page break between heading and names; assigned via summary count SWEDEN 14 1; consistent with ST addition same review"}),
 ("2021-05","ST"): (["EMBRACER GROUP B","SINCH","VOLVO A"], [], "summary count SWEDEN 3 0 matches",
                    {"EMBRACER GROUP B":"deleted from SC same review","SINCH":"deleted from SC same review"}),
 ("2021-05","SC"): (["BEIJER ALMA","CINT GROUP","DESENIO GROUP","ENAD GLOBAL 7","FAGERHULT","HEXATRONIC GROUP","IMPLANTICA A SDR","NEW WAVE GROUP B","NORDNET","RENEWCELL","SAGAX B","SWEDENCARE"],
                    ["CANTARGIA","EMBRACER GROUP B","IMMUNOVIA","JOHN MATTSON","SINCH"],
                    "section spans page break (p7-8); assigned via summary count SWEDEN 12 5",
                    {"EMBRACER GROUP B":"section spans page break; assigned via summary count SWEDEN 12 5; consistent with ST addition same review",
                     "SINCH":"section spans page break; assigned via summary count SWEDEN 12 5; consistent with ST addition same review"}),
 ("2021-11","ST"): (["GETINGE B","INVESTOR A","LIFCO B","SAGAX B"], [], "summary count SWEDEN 4 0 matches",
                    {"GETINGE B":"deleted from SC same review","LIFCO B":"deleted from SC same review","SAGAX B":"deleted from SC same review"}),
 ("2021-11","SC"): (["HEMNET GROUP","HUMBLE GROUP","OX2","RVRC HOLDING","SECTRA B","SURGICAL SCIENCE SWEDEN","VESTUM","VIMIAN GROUP","VITEC SOFTWARE GROUP","VNV GLOBAL","VOLATI"],
                    ["BONESUPPORT HOLDING","ENAD GLOBAL 7","GETINGE B","LIFCO B","ONCOPEPTIDES AB","SAGAX B","SAGAX D","SCANDI STANDARD"],
                    "summary count SWEDEN 11 8 matches",
                    {"GETINGE B":"added to ST same review","LIFCO B":"added to ST same review","SAGAX B":"added to ST same review"}),
}

rows = []
for review, (ann, eff) in dates.items():
    for seg in ("ST", "SC"):
        key = (review, seg)
        if key not in data:
            rows.append([review, seg, "none", "", ann, eff, "ok", "no MSCI SWEDEN INDEX section in public list"])
            continue
        adds, dels, note, per = data[key]
        for change, names in (("addition", adds), ("deletion", dels)):
            for n in names:
                rows.append([review, seg, change, n, ann, eff, "ok", per.get(n, note)])

with open("./lists_2017_2021.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["review","segment","change","security","announcement_date","effective_date","status","note"])
    w.writerows(rows)
print(len(rows))
