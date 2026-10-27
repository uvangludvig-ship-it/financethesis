"""
lseg_codebook_pull_v2.py: targeted stock panel for thesis 2, run inside LSEG Workspace CodeBook.

Pulls ONE instrument per request (small requests do not hit API limits), resumes where it stopped,
and logs every failure to failures.csv instead of silently dropping it.

Upload lseg_input.csv into the same CodeBook folder as this file before running.
Run the steps one cell at a time, in order. Send Claude the printed output of each step.
"""
import os, time, json
import pandas as pd
try:
    import lseg.data as ld
except ImportError:                      # older CodeBook images
    import refinitiv.data as ld

OUT = "thesis_data"
os.makedirs(f"{OUT}/daily", exist_ok=True)
START, END = "2012-01-01", pd.Timestamp.today().strftime("%Y-%m-%d")
ld.open_session()

# ===================================================================== STEP 0: does anything work?
t = ld.get_history(universe="VOLVb.ST", fields=["TR.PriceClose", "TR.Volume"],
                   start="2024-06-03", end="2024-06-07", interval="daily")
print(t)
# Expect 5 rows with price and volume. If this fails, stop and send Claude the error.

# ===================================================================== STEP 1: resolve every id to a RIC
inp = pd.read_csv("lseg_input.csv")
rows = []
# 1a. ISINs -> RIC, name, status (one call per 100 ISINs)
isins = inp.loc[inp.id_type == "ISIN", "id"].tolist()
for k in range(0, len(isins), 100):
    try:
        d = ld.get_data(universe=isins[k:k+100],
                        fields=["TR.RIC", "TR.CommonName", "TR.ISIN", "TR.InstrumentIsActive",
                                "TR.ExchangeMarketIdCode", "TR.InstrumentType"])
        rows.append(d)
    except Exception as e:
        print("isin batch", k, e)
    time.sleep(0.5)
# 1b. guessed RICs for OMXSB names (delisted ones will fail here and are retried in 1c)
rics_guess = inp.loc[inp.id_type == "RIC", "id"].tolist()
try:
    d = ld.get_data(universe=rics_guess,
                    fields=["TR.RIC", "TR.CommonName", "TR.ISIN", "TR.InstrumentIsActive", "TR.ExchangeMarketIdCode"])
    rows.append(d)
except Exception as e:
    print("ric batch", e)
res = pd.concat(rows, ignore_index=True)
res.to_csv(f"{OUT}/resolved.csv", index=False)

# 1c. OMXSB names whose guessed RIC did not resolve: search by company name, active AND inactive
ok_names = set(res.get("Company Common Name", pd.Series(dtype=str)).dropna())
missing = inp[(inp.id_type == "RIC")]
missing = missing[~missing.id.isin(res.loc[res.get("RIC", pd.Series(dtype=str)).notna(), "Instrument"])]
found = []
for _, r in missing.iterrows():
    try:
        s = ld.discovery.search(query=r["name"], top=3,
                                filter="ExchangeCode eq 'STO' and AssetCategory eq 'ORD'",
                                select="RIC,DTSubjectName,IssueISIN,ExchangeName,RetireDate")
        if len(s):
            s["query"] = r["name"]; found.append(s.head(1))
    except Exception as e:
        print("search", r["name"], e)
    time.sleep(0.3)
if found:
    pd.concat(found).to_csv(f"{OUT}/omxsb_search_hits.csv", index=False)
print("resolved rows:", len(res), "| OMXSB searched:", len(missing), "| search hits:", sum(len(f) for f in found))
# Send Claude these three numbers and the first rows of omxsb_search_hits.csv.

# ===================================================================== STEP 2: build the final RIC list
ric_col = "RIC" if "RIC" in res.columns else res.columns[1]
rics = set(res[ric_col].dropna().astype(str))
if found:
    rics |= set(pd.concat(found)["RIC"].dropna().astype(str))
rics = sorted(r for r in rics if r.endswith(".ST") or ".ST^" in r)   # Stockholm listings only
json.dump(rics, open(f"{OUT}/rics.json", "w"))
print(len(rics), "Stockholm RICs to download")

# ===================================================================== STEP 3: daily history, one RIC per call
FIELDS = ["TR.PriceClose", "TR.TotalReturn", "TR.Volume", "TR.CompanyMarketCap", "TR.SharesOutstanding"]
fails = []
for n, r in enumerate(rics):
    path = f"{OUT}/daily/{r.replace('^', '_')}.csv"
    if os.path.exists(path):
        continue
    for attempt in range(3):
        try:
            h = ld.get_history(universe=r, fields=FIELDS, start=START, end=END, interval="daily")
            h.to_csv(path); break
        except Exception as e:
            if attempt == 2: fails.append({"ric": r, "error": str(e)[:200]})
            time.sleep(3)
    time.sleep(0.25)
    if n % 50 == 0: print("done", n, "of", len(rics))
pd.DataFrame(fails).to_csv(f"{OUT}/failures.csv", index=False)
print("finished; failures:", len(fails))

# ===================================================================== STEP 4: static fields (listing and delisting dates)
st = []
for k in range(0, len(rics), 100):
    try:
        st.append(ld.get_data(universe=rics[k:k+100],
                              fields=["TR.CommonName", "TR.ISIN", "TR.FirstTradeDate", "TR.RetireDate",
                                      "TR.TRBCEconomicSector", "TR.FreeFloatPct"]))
    except Exception as e:
        print("static", k, e)
pd.concat(st).to_csv(f"{OUT}/stocks_static.csv", index=False)

# ===================================================================== STEP 5: indices
for r in [".OMXSPI", ".SIXRX", ".OMXSBGI", ".OMXSB", ".OMXS30"]:
    try:
        h = ld.get_history(universe=r, fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        h.to_csv(f"{OUT}/index_{r.strip('.')}.csv"); print(r, len(h))
    except Exception as e:
        print(r, "failed:", str(e)[:120])

ld.close_session()
print("Download the folder", OUT)
