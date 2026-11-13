"""
tvilling_data.py  --  allt Claude behöver för del 1 (återgång) och del 2 (tvillingaktier).
DEL 1 körs lokalt i repo-mappen (financethesis/). DEL 2 körs i LSEG Workspace CodeBook.
Resultat: två filer som laddas upp till Claude:
  panel_utdrag.csv.gz        (från DEL 1)
  tvilling_priser_lseg.csv   (från DEL 2)
"""

TWIN_RICS = ['BONAVa.ST', 'BONAVb.ST', 'COREa.ST', 'COREb.ST', 'HUSQa.ST', 'HUSQb.ST', 'IFSa.ST^J16', 'IFSb.ST^J16',
             'INDUa.ST', 'INDUc.ST', 'KINVa.ST', 'KINVb.ST', 'KLOVa.ST^G21', 'KLOVb.ST^G21', 'NCCa.ST', 'NCCb.ST',
             'RATOa.ST', 'RATOb.ST', 'SAGAa.ST', 'SAGAb.ST', 'SCAa.ST', 'SCAb.ST', 'SSABa.ST', 'SSABb.ST',
             'STEa.ST', 'STEr.ST', 'SWECa.ST', 'SWECb.ST', 'TWWsdba.ST^K14', 'TWWsdbb.ST^K14', 'VOLVa.ST', 'VOLVb.ST',
             'VPLAYa.ST', 'VPLAYb.ST']

# %% DEL 1  --  lokalt: plocka ut alla händelseaktier + tvillingarna ur panelen (någon minut)
import pandas as pd
ev = pd.read_csv("output/omxsb_replication_2007/events_car.csv")
RICS = sorted(set(ev["RIC"].dropna().astype(str)) | set(TWIN_RICS))
p = pd.read_parquet("data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet")
print("kolumner i panelen:", p.columns.tolist())
ric_col = [c for c in p.columns if c.lower() in ("ric", "instrument")][0]
sub = p[p[ric_col].isin(RICS)]
sub.to_csv("panel_utdrag.csv.gz", index=False)
print("sparat:", len(sub), "rader,", sub[ric_col].nunique(), "av", len(RICS), "aktieslag")
print("tvillingar som saknas i panelen:", sorted(set(TWIN_RICS) - set(sub[ric_col].unique())))
# SKICKA TILL CLAUDE: panel_utdrag.csv.gz och de två utskrifterna ovan.

# %% DEL 2  --  i LSEG CodeBook: hämta de tvillingar som saknas i panelen
# Fyll i SAKNAS med listan från DEL 1. Väntat: NCCa.ST, RATOa.ST, SWECa.ST, BONAVa.ST.
# (STEa.ST behövs inte: Stora Enso utesluts.)
try:
    import lseg.data as ld
except Exception:
    import refinitiv.data as ld
ld.open_session()
SAKNAS = ["NCCa.ST", "RATOa.ST", "SWECa.ST", "BONAVa.ST"]
FIELDS = ["TR.PriceClose", "TR.Volume", "TR.TotalReturn1D"]
out = []
for r in SAKNAS:
    try:
        h = ld.get_history(universe=r, fields=FIELDS, start="2006-01-01", end="2026-10-31", interval="daily")
        h = h.reset_index(); h["ric"] = r
        out.append(h)
        print(r, "OK", len(h), "dagar, från", h.iloc[0, 0], "till", h.iloc[-1, 0])
    except Exception as e:
        print(r, "FEL", str(e)[:120])
pd.concat(out, ignore_index=True).to_csv("tvilling_priser_lseg.csv", index=False)
# SKICKA TILL CLAUDE: tvilling_priser_lseg.csv och utskriften ovan.
# Ger en RIC "FEL": skriv bolagets namn, så letar vi rätt RIC (t.ex. med ^ för avnoterade).
