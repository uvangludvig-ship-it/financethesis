import csv
rows = []
def add(review, seg, change, names, ann, eff, status="ok", note=""):
    if isinstance(names, str):
        names = [names]
    for n in names:
        rows.append([review, seg, change, n, ann, eff, status, note])

NOSEC = "no MSCI SWEDEN INDEX section; Sweden absent from summary table"
# 2007-02
add("2007-02","ST","none","","2007-02-13","2007-02-28",note=NOSEC)
add("2007-02","SC","","","","","not_found","fetch failed (client_error) on www.msci.com and app2.msci.com")
# 2007-05
add("2007-05","ST","deletion","TELELOGIC","2007-05-03","2007-05-31",note="Additions: None")
n="section titled MSCI SWEDEN SMALL CAP INDEX; columns merged in text; assigned by line order (left=Additions) and summary count SWEDEN 4 5"
add("2007-05","SC","addition",["AARHUSKARLSHAMN","AXIS COMMUNICATIONS","BIOVITRUM","SECURITAS DIRECT B"],"2007-05-03","2007-05-31",note=n)
add("2007-05","SC","deletion",["AXFOOD","JM","KUNGSLEDEN","PEAB B","TRELLEBORG B"],"2007-05-03","2007-05-31",note=n)
# 2007-08
add("2007-08","ST","none","","2007-08-16","2007-08-31",note=NOSEC)
add("2007-08","SC","none","","2007-08-16","2007-08-31",note="no Sweden section; summary table shows Sweden 0 added 0 deleted")
# 2007-11
add("2007-11","ST","addition",["INVESTOR B","MILLICOM INT'L CELLULAR","SWEDBANK"],"2007-11-05","2007-11-30",note="Deletions: None; summary SWEDEN 3 0")
add("2007-11","SC","addition",["ACTIVE BIOTECH","AXFOOD","BE GROUP","BILIA A","CASTELLUM","ENIRO","FABEGE","GANT COMPANY","HEMTEX","HEXAGON B","HOGANAS B","HQ","HUFVUDSTADEN A","INDUTRADE","JM","KAPPAHL HOLDING","KINNEVIK INVESTMENT B","KUNGSLEDEN","LBI INTERNATIONAL","LINDAB INTERNATIONAL","MEDA","MEKONOMEN","NCC B","NOBIA","OMX AB","ORIFLAME COSMETICS SDR","PA RESOURCES","PEAB B","RATOS B","REZIDOR HOTEL GROUP","RNB RETAIL AND BRANDS","SAAB B","SECURITAS SYSTEMS B","TRADEDOUBLER","TRELLEBORG B","VOSTOK GAS SDR","VOSTOK NAFTA INV. SDR"],"2007-11-05","2007-11-30",note="section titled MSCI SWEDEN SMALL CAP INDEX; Deletions: None; summary SWEDEN 37 0")
# 2008-02
add("2008-02","ST","deletion","SAS","2008-02-13","2008-02-29",note="Additions: None")
add("2008-02","SC","addition","SAS","2008-02-13","2008-02-29",note="section titled MSCI SWEDEN SMALL CAP INDEX; Deletions: None")
# 2008-05
add("2008-05","ST","deletion",["AXFOOD","BILLERUD","CASTELLUM","D. CARNEGIE & CO","ELEKTA B","ENIRO","FABEGE","HOGANAS B","KUNGSLEDEN","NOBIA","ORIFLAME COSMETICS SDR","SECURITAS SYSTEMS B","TRELLEBORG B","VOLVO A","WIHLBORGS FASTIGHETER"],"2008-05-06","2008-05-30",note="Additions: None; summary SWEDEN 0 15")
n="section titled MSCI SWEDEN SMALL CAP INDEX; page break (p6/p7) between column header and names; all names on p7; assigned by line order and summary count SWEDEN 6 3"
add("2008-05","SC","addition",["BETSSON B","BLACK EARTH FARMING SDR","BURE EQUITY","EAST CAPITAL EXPLORER","NEONET","SYSTEMAIR"],"2008-05-06","2008-05-30",note=n)
add("2008-05","SC","deletion",["CISION","CONCORDIA MARITIME B","ROTTNEROS"],"2008-05-06","2008-05-30",note=n)
# 2008-08
add("2008-08","ST","none","","2008-08-13","2008-08-29",note=NOSEC)
add("2008-08","SC","none","","2008-08-13","2008-08-29",note=NOSEC)
# 2008-11
add("2008-11","ST","addition","VOLVO A","2008-11-11","2008-11-25",note="summary SWEDEN 1 1; left=Additions")
add("2008-11","ST","deletion","BOLIDEN","2008-11-11","2008-11-25",note="summary SWEDEN 1 1; left=Additions")
n="column headers misaligned in text extraction; assigned from summary count SWEDEN 1 6 and alphabetical order of Deletions column"
add("2008-11","SC","addition","BOLIDEN","2008-11-11","2008-11-25",note=n)
add("2008-11","SC","deletion",["ACTIVE BIOTECH","BILIA A","BIOVITRUM","MICRONIC LASER SYSTEMS","SECTRA B","SYSTEMAIR"],"2008-11-11","2008-11-25",note=n)
# 2009-02
add("2009-02","ST","none","","2009-02-11","2009-02-27",note=NOSEC)
add("2009-02","SC","none","","2009-02-11","2009-02-27",note=NOSEC)
# 2009-05
add("2009-05","ST","deletion","MTG MODERN TIMES GROUP B","2009-05-13","2009-05-29",note="Additions: None; summary SWEDEN 0 1")
n="section spans page break (p9/p10); assigned by summary count SWEDEN 11 1"
add("2009-05","SC","addition",["BIOINVENT INTL","BJOERN BORG","EOS RUSSIA","HIQ INTERNATIONAL","IFS IND & FIN SYSTEMS B","MTG MODERN TIMES GROUP B","NET ENTERTAINMENT NE B","NET INSIGHT B","ORC SOFTWARE","ORESUND INVESTMENT","TRICORONA"],"2009-05-13","2009-05-29",note=n)
add("2009-05","SC","deletion","LBI INTERNATIONAL","2009-05-13","2009-05-29",note=n)
# 2009-08
add("2009-08","ST","none","","2009-08-12","2009-08-31",note=NOSEC)
add("2009-08","SC","none","","2009-08-12","2009-08-31",note=NOSEC)
# 2009-11
add("2009-11","ST","none","","2009-11-11","2009-11-30",note=NOSEC)
add("2009-11","SC","addition",["BIOGAIA B","DIAMYD MEDICAL B","LUNDBERGS B"],"2009-11-11","2009-11-30",note="Deletions: None; summary SWEDEN 3 0")
# 2010-02
add("2010-02","ST","addition",["KINNEVIK INVESTMENT B","RATOS B"],"2010-02-10","2010-02-26",note="Deletions: None; summary SWEDEN 2 0")
add("2010-02","SC","deletion",["KINNEVIK INVESTMENT B","RATOS B"],"2010-02-10","2010-02-26",note="Additions: None")
# 2010-05
n="summary SWEDEN 2 2; left=Additions"
add("2010-05","ST","addition",["BOLIDEN","MTG MODERN TIMES GROUP B"],"2010-05-11","2010-05-26",note=n)
add("2010-05","ST","deletion",["LUNDIN PETROLEUM","VOLVO A"],"2010-05-11","2010-05-26",note=n)
n="summary SWEDEN 8 2; left=Additions"
add("2010-05","SC","addition",["ACTIVE BIOTECH","B&B TOOLS B","BILIA A","BIOVITRUM","LUNDIN PETROLEUM","MEDIVIR B","PROFFICE B","TRANSCOM WORLDWIDE B"],"2010-05-11","2010-05-26",note=n)
add("2010-05","SC","deletion",["BOLIDEN","MTG MODERN TIMES GROUP B"],"2010-05-11","2010-05-26",note=n)
# 2010-08
add("2010-08","ST","addition","HEXAGON B","2010-08-17","2010-08-31",note="Deletions: None")
add("2010-08","SC","deletion","HEXAGON B","2010-08-17","2010-08-31",note="Additions: None")
# 2010-11
n="page footer (p4) between column header and the single names line; summary SWEDEN 1 1; left=Additions (same convention as other 1/1 sections in this document)"
add("2010-11","ST","addition","INDUSTRIVARDEN C","2010-11-10","2010-11-30",note=n)
add("2010-11","ST","deletion","SSAB SVENSKT STAL B","2010-11-10","2010-11-30",note=n)
n="columns merged in text; assigned by line order (left=Additions) and summary count SWEDEN 2 1"
add("2010-11","SC","addition",["BYGGMAX GROUP","DUNI"],"2010-11-10","2010-11-30",note=n)
add("2010-11","SC","deletion","HQ","2010-11-10","2010-11-30",note=n)
# 2011-02
add("2011-02","ST","none","","2011-02-10","2011-02-28",note=NOSEC)
add("2011-02","SC","none","","2011-02-10","2011-02-28",note=NOSEC)
# 2011-05
add("2011-05","ST","none","","2011-05-16","2011-05-31",note=NOSEC)
add("2011-05","SC","addition",["FASTIGHETS AB BALDER B","MICRONIC MYDATA","NORDIC MINES AB","UNIBET GROUP SDR"],"2011-05-16","2011-05-31",note="Deletions: None; summary SWEDEN 4 0")
# 2011-08
add("2011-08","ST","none","","2011-08-16","2011-08-31",note=NOSEC)
add("2011-08","SC","none","","2011-08-16","2011-08-31",note=NOSEC)
# 2011-11
add("2011-11","ST","addition","LUNDIN PETROLEUM","2011-11-15","2011-11-30",note="Deletions: None")
n="summary SWEDEN 1 4; left=Additions"
add("2011-11","SC","addition","NCC A","2011-11-15","2011-11-30",note=n)
add("2011-11","SC","deletion",["DIAMYD MEDICAL B","LUNDIN PETROLEUM","RNB RETAIL AND BRANDS","TRANSCOM WORLDWIDE B"],"2011-11-15","2011-11-30",note=n)

with open("./lists_2007_2011.csv","w",newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["review","segment","change","security","announcement_date","effective_date","status","note"])
    w.writerows(rows)
print(len(rows))
