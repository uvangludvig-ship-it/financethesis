import pandas as pd, glob, re, warnings, os
warnings.filterwarnings("ignore")
import os
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
ROOT=REPO+"/data/raw/ppm"
files=sorted(f for f in glob.glob(ROOT+"/*/*/*.xlsm") if re.search(r"20(1[89]|2[0-6])-\d\d-\d\d", f))
def sheet(xl, name, hdr_key):
    df=xl.parse(name, header=None)
    col0=df[0].astype(str)
    i=col0[col0.str.fullmatch(r"\d{6}(\.0)?")].index.min()
    # header row = row containing 'Fondnummer'
    h=None
    for k in range(i-1, i-6, -1):
        if "Fondnummer" in [str(x) for x in df.iloc[k]]: h=k; break
    cols=[str(x).strip() for x in df.iloc[h]]
    body=df.iloc[h+1:].copy(); body.columns=cols
    body=body[body["Fondnummer"].astype(str).str.fullmatch(r"\d+(\.0)?")]
    return body, cols
rows=[]
for f in files:
    d=re.search(r"(20\d\d-\d\d-\d\d)", f).group(1)
    xl=pd.ExcelFile(f, engine="openpyxl")
    a,ca=sheet(xl,"Fondval & marknadsvärde","Fondnummer")
    # positions: Fondnummer, Fondnamn, K,M,Total(val), K,M,Total(MV), Handel netto, Fondkategori, Fondtyp, Förvaltare, Svensk/Utländsk, Upphandlad?
    base=a.iloc[:, :12].copy()
    base.columns=["fondnr","fondnamn","val_k","val_m","val_tot","mv_k","mv_m","mv_tot","handel_netto","kategori","fondtyp","forvaltare"]
    rest=a.iloc[:, 12:]
    def pick(vals):
        for j in range(rest.shape[1]):
            v=set(rest.iloc[:,j].dropna().astype(str).str.strip())
            if v and v<=set(vals): return rest.iloc[:,j].values
        return None
    base["svensk"]=pick({"Svensk","Utländsk"})
    base["forvaltning"]=pick({"Aktiv","Passiv"})
    u=pick({"Upphandlad","Ja"})
    base["upphandlad"]=u
    a=base
    b,cb=sheet(xl,"Fondstatistik","Fondnummer")
    keep={"Fondnummer":"fondnr","I år":"ret_ytd","1 mån.":"ret_1m","12 mån.":"ret_12m","36 mån.":"ret_36m","Netto":"fee_net","Brutto (TER)":"fee_gross","ISIN-kod":"isin","Startdatum":"startdatum","valuta":"valuta"}
    b=b[[c for c in b.columns if c in keep]].rename(columns=keep)
    b=b.loc[:,~b.columns.duplicated()]
    m=a.merge(b,on="fondnr",how="left")
    m["date"]=d
    rows.append(m)
    print(d, len(a), len(b), "upph col" , "upphandlad" in a.columns, flush=True)
p=pd.concat(rows, ignore_index=True)
p["fondnr"]=p["fondnr"].astype(str).str.replace(r"\.0$","",regex=True)
for c in ["val_tot","mv_tot","handel_netto","ret_1m","ret_12m","ret_36m","fee_net","fee_gross"]:
    p[c]=pd.to_numeric(p[c],errors="coerce")
p.to_csv(REPO+"/data/derived/ppm/ppm_panel_2018_2026.csv",index=False)
print(p.shape, p.date.nunique(), p.fondnr.nunique())
print(p.upphandlad.value_counts(dropna=False).head())
