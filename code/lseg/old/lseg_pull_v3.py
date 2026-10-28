"""
lseg_pull_v3.py  --  thesis 2 stock panel from LSEG Workspace CodeBook.

One notebook cell per '# %% CELL' block. Run them in order. After any kernel restart, rerun CELL 0 first.
Files to upload next to this notebook: omxsb_changes_2013_2026.csv, isin_list_lseg_v2.csv

Design choices (why this version should not fail like the last one):
  * Universe comes from LSEG Search with delisted instruments included (RICs ending in ^Xyy),
    not from a screen of active stocks.
  * One instrument per history call, resumable, every failure logged to failures.csv.
  * Field names and filter syntax are tested first; whatever fails is dropped or swapped, and printed.
  * Daily call budget so the API quota is never exceeded silently.
"""

# %% CELL 0  --  session, helpers, smoke tests (rerun after every restart)
import os, re, time, json, difflib, shutil
import pandas as pd
try:
    import lseg.data as ld
except ImportError:
    import refinitiv.data as ld

OUT = "thesis_data"
os.makedirs(f"{OUT}/daily", exist_ok=True)
START = "2012-01-01"
END = pd.Timestamp.today().strftime("%Y-%m-%d")
MAX_CALLS = 9000                      # daily API quota is about 10,000 requests
CALLS = {"n": 0}

def api(fn, *a, **k):
    CALLS["n"] += 1
    if CALLS["n"] > MAX_CALLS:
        raise RuntimeError("budget: daily call budget reached, rerun tomorrow (everything resumes)")
    r = fn(*a, **k)
    time.sleep(0.25)
    return r

def search(filter_, select, top=10000, query=None):
    kw = dict(view=ld.discovery.Views.EQUITY_QUOTES, filter=filter_, select=select, top=top)
    if query: kw["query"] = query
    return api(ld.discovery.search, **kw)

ld.open_session()

# 0a. which history fields work on this account? (tested on Volvo B, one week)
CANDIDATES = ["TR.PriceClose", "TR.TotalReturn", "TR.Volume", "TR.CompanyMarketCap",
              "TR.SharesOutstanding", "TR.Turnover"]
FIELDS = []
for f in CANDIDATES:
    try:
        t = api(ld.get_history, universe="VOLVb.ST", fields=[f],
                start="2024-06-03", end="2024-06-07", interval="daily")
        ok = t is not None and len(t) > 0 and t.notna().any().any()
        print(f"{f:24s}", "OK" if ok else "EMPTY")
        if ok: FIELDS.append(f)
    except Exception as e:
        print(f"{f:24s} FAIL: {str(e)[:100]}")
if "TR.TotalReturn" not in FIELDS:
    try:
        t = api(ld.get_history, universe="VOLVb.ST", fields=["TR.TotalReturn1D"],
                start="2024-06-03", end="2024-06-07", interval="daily")
        if len(t): FIELDS.append("TR.TotalReturn1D"); print("TR.TotalReturn1D       OK")
    except Exception as e:
        print("TR.TotalReturn1D FAIL:", str(e)[:100])
print("\nFIELDS to use:", FIELDS)
assert "TR.PriceClose" in FIELDS, "TR.PriceClose failed: stop and send Claude the output above"

# 0b. does Search accept the field list, and does it return delisted stocks?
SEL_FULL = "RIC,DTSubjectName,IssueISIN,ExchangeCode,ExchangeName,RCSAssetCategoryLeaf,RetireDate,PrimaryRIC,TickerSymbol"
SEL_MIN = "RIC,DTSubjectName,IssueISIN,ExchangeCode,RetireDate"
SEL = SEL_FULL
try:
    search("ExchangeCode eq 'STO'", SEL_FULL, top=3)
except Exception as e:
    print("full select failed, using minimal select:", str(e)[:100]); SEL = SEL_MIN

INACTIVE_CLAUSE = None
for clause in ["IsActive eq false", "AssetState eq 'DC'"]:
    try:
        s = search(f"ExchangeCode eq 'STO' and {clause}", SEL, top=5, query="Klovern")
        print(f"\ninactive clause '{clause}': {len(s)} rows"); print(s.to_string())
        if len(s): INACTIVE_CLAUSE = clause; break
    except Exception as e:
        print(f"clause '{clause}' FAIL:", str(e)[:100])
print("\nINACTIVE_CLAUSE =", INACTIVE_CLAUSE, "(None means Search could not return delisted stocks: tell Claude)")
json.dump({"FIELDS": FIELDS, "SEL": SEL, "INACTIVE_CLAUSE": INACTIVE_CLAUSE}, open(f"{OUT}/config.json", "w"))
# SEND CLAUDE everything this cell printed.


# %% CELL 1  --  universe: every Swedish share, active and delisted, alive at some point since 2012
cfg = json.load(open(f"{OUT}/config.json")); SEL = cfg["SEL"]; INACTIVE_CLAUSE = cfg["INACTIVE_CLAUSE"]
CATS = ["RCSAssetCategoryLeaf eq 'Ordinary Share'", "RCSAssetCategoryLeaf eq 'Depository Receipt'"]
frames, used = [], None
for base in ["RCSExchangeCountryLeaf eq 'Sweden'", "ExchangeCountry eq 'SWE'", "ExchangeCode eq 'STO'"]:
    try:
        for cat in CATS:
            a = search(f"{base} and {cat}", SEL); frames.append(a.assign(active_flag=True))
            if len(a) >= 10000: print("WARNING: active search hit the 10,000 cap for", cat)
            if INACTIVE_CLAUSE:
                i = search(f"{base} and {cat} and {INACTIVE_CLAUSE}", SEL); frames.append(i.assign(active_flag=False))
                if len(i) >= 10000: print("WARNING: inactive search hit the 10,000 cap for", cat)
            print(f"{base} | {cat[-20:]}: active {len(a)}, inactive {len(i) if INACTIVE_CLAUSE else 'n/a'}")
        used = base; break
    except Exception as e:
        print("filter failed:", base, "->", str(e)[:120]); frames = []
assert frames, "no universe filter worked: send Claude the output"
uni = pd.concat(frames, ignore_index=True).drop_duplicates("RIC")
uni["RIC"] = uni["RIC"].astype(str)
print("\nRIC suffixes before filtering:", uni["RIC"].str.extract(r"\.([A-Za-z]+)")[0].value_counts().head(12).to_dict())
uni = uni[uni["RIC"].str.contains(r"\.ST(\^|$)", regex=True)]          # Nasdaq Stockholm and First North
if "RetireDate" in uni:
    rd_ = pd.to_datetime(uni["RetireDate"], errors="coerce")
    uni = uni[rd_.isna() | (rd_ >= "2012-01-01")]                       # drop stocks that died before our window
uni.to_csv(f"{OUT}/universe.csv", index=False)
print(f"\nuniverse: {len(uni)} RICs, of which {uni['RIC'].str.contains(chr(94)).sum()} delisted (^). filter used: {used}")
print(uni.head(8).to_string())
# SEND CLAUDE: the counts and the suffix list.


# %% CELL 2  --  resolve the fund-holdings ISIN list (so stocks the losers own are covered even if CELL 1 missed them)
INCLUDE_TIER2 = False   # True also pulls the non-Nordic stocks held by the European-round losers
L = pd.read_csv("isin_list_lseg_v2.csv")
if not INCLUDE_TIER2: L = L[L["tier"] == 1]
isins = L["isin"].astype(str).str.strip()
isins = sorted({i for i in isins if re.fullmatch(r"[A-Z]{2}[A-Z0-9]{10}", i)})
res = []
for k in range(0, len(isins), 50):
    chunk = ",".join(f"'{x}'" for x in isins[k:k + 50])
    clauses = [""] + ([f" and {INACTIVE_CLAUSE}"] if INACTIVE_CLAUSE else [])
    for extra in clauses:
        try:
            res.append(search(f"IssueISIN in ({chunk}){extra}", SEL, top=2000))
        except Exception as e:
            print("isin chunk", k, "FAIL:", str(e)[:100])
isin_res = pd.concat(res, ignore_index=True).drop_duplicates("RIC") if res else pd.DataFrame(columns=["RIC", "IssueISIN"])
HOME = {"SE": r"\.ST(\^|$)", "DK": r"\.CO(\^|$)", "FI": r"\.HE(\^|$)", "NO": r"\.OL(\^|$)"}
def is_home(row):
    pat = HOME.get(str(row["IssueISIN"])[:2])
    return bool(re.search(pat, str(row["RIC"]))) if pat else True
if len(isin_res):
    isin_res = isin_res[isin_res.apply(is_home, axis=1)]
isin_res.to_csv(f"{OUT}/isin_resolved.csv", index=False)
found = set(isin_res["IssueISIN"]) if len(isin_res) else set()
print(f"ISINs in list: {len(isins)} | resolved to a home-exchange share: {len(found)} | unresolved: {len(set(isins) - found)}")
print("(unresolved ones are mostly bonds, fund units and foreign stocks; that is expected)")


# %% CELL 3  --  map the 394 OMXSB events to RICs, delisted included
uni = pd.read_csv(f"{OUT}/universe.csv"); uni["RIC"] = uni["RIC"].astype(str)
ev = pd.read_csv("omxsb_changes_2013_2026.csv")
def ric_base(t):
    p = str(t).strip().split()
    return p[0] + "".join(x.lower() for x in p[1:])      # 'BALD B' -> 'BALDb', 'ALIV SDB' -> 'ALIVsdb'
def norm(s):
    s = re.sub(r"\(publ\)|\bAB\b|\bser\.?\b|\bSDB\b|\bplc\b|,|\.", " ", str(s), flags=re.I)
    return re.sub(r"\s+", " ", s).strip().lower()
uni["base"] = uni["RIC"].str.replace(r"\.ST(\^.*)?$", "", regex=True)
uni["nname"] = uni["DTSubjectName"].map(norm)
rows = []
for tk, grp in ev.groupby("ticker"):
    name, base = grp["company"].iloc[0], ric_base(tk)
    hit, how = uni[uni["base"] == base], "ticker"
    if hit.empty: hit = uni[uni["base"].str.lower() == base.lower()]
    if hit.empty:
        cands = difflib.get_close_matches(norm(name), uni["nname"].tolist(), n=3, cutoff=0.75)
        hit, how = uni[uni["nname"].isin(cands)], "name"
    if len(hit) > 1:                                      # several listings: keep the one alive at the event
        ed = pd.to_datetime(grp["effective_date"], errors="coerce").max()
        rd_ = pd.to_datetime(hit["RetireDate"], errors="coerce") if "RetireDate" in hit else pd.Series(pd.NaT, index=hit.index)
        alive = hit[rd_.isna() | (rd_ >= ed)]
        hit = alive if len(alive) else hit
    rows.append({"ticker": tk, "company": name, "ric_base": base,
                 "RIC": hit["RIC"].iloc[0] if len(hit) else None,
                 "matched_name": hit["DTSubjectName"].iloc[0] if len(hit) else None,
                 "how": how if len(hit) else "UNMATCHED", "n_candidates": len(hit)})
omx = pd.DataFrame(rows); omx.to_csv(f"{OUT}/omxsb_ric_map.csv", index=False)
print(omx["how"].value_counts().to_dict())
print("\nUNMATCHED: type the RIC by hand into omxsb_ric_map.csv (Workspace search box: company name; delisted RICs end in ^):")
print(omx[omx["how"] == "UNMATCHED"][["ticker", "company"]].to_string())
print("\nMatched by NAME, check these:")
print(omx[omx["how"] == "name"][["ticker", "company", "RIC", "matched_name"]].to_string())
# SEND CLAUDE: this output. Fix UNMATCHED rows in the csv before CELL 4 (or leave them, they are listed again in CELL 7).


# %% CELL 4  --  final download list
uni = pd.read_csv(f"{OUT}/universe.csv")
isin_res = pd.read_csv(f"{OUT}/isin_resolved.csv") if os.path.exists(f"{OUT}/isin_resolved.csv") else pd.DataFrame()
omx = pd.read_csv(f"{OUT}/omxsb_ric_map.csv")
rics = set(uni["RIC"].dropna().astype(str)) | set(isin_res.get("RIC", pd.Series(dtype=str)).dropna().astype(str)) \
       | set(omx["RIC"].dropna().astype(str))
rics = sorted(r for r in rics if r and r != "nan")
json.dump(rics, open(f"{OUT}/rics_final.json", "w"))
print(len(rics), "RICs to download;", sum("^" in r for r in rics), "delisted")


# %% CELL 5  --  daily history, one RIC per call, resumable (rerun until 'to download' is 0)
cfg = json.load(open(f"{OUT}/config.json")); FIELDS = cfg["FIELDS"]
rics = json.load(open(f"{OUT}/rics_final.json"))
def fname(r): return f"{OUT}/daily/{re.sub(r'[^A-Za-z0-9.]', '_', r)}.csv"
def pull(r):
    err = ""
    try:
        h = api(ld.get_history, universe=r, fields=FIELDS, start=START, end=END, interval="daily")
        if h is not None and len(h): h = h.copy(); h["source"] = "tr"; return h
        err = "tr empty"
    except Exception as e:
        err = "tr: " + str(e)[:120]
    try:                                                   # fallback: pricing endpoint (close, volume, turnover)
        h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        if h is not None and len(h): h = h.copy(); h["source"] = "pricing"; return h
        err += " | pricing empty"
    except Exception as e:
        err += " | pricing: " + str(e)[:120]
    raise RuntimeError(err)

todo = [r for r in rics if not os.path.exists(fname(r))]
print(len(todo), "to download,", len(rics) - len(todo), "already on disk")
fails = []
for n, r in enumerate(todo, 1):
    try:
        h = pull(r); h["ric"] = r; h.to_csv(fname(r))
    except RuntimeError as e:
        if "budget" in str(e): print("STOP:", e); break
        fails.append({"RIC": r, "error": str(e)})
    if n % 100 == 0: print(f"{n}/{len(todo)} done, {len(fails)} failed, {CALLS['n']} API calls this session")
old = pd.read_csv(f"{OUT}/failures.csv") if os.path.exists(f"{OUT}/failures.csv") else pd.DataFrame()
pd.concat([old, pd.DataFrame(fails)]).drop_duplicates("RIC", keep="last").to_csv(f"{OUT}/failures.csv", index=False) if (len(old) or fails) else None
print("finished this run. failures so far:", len(fails), "(failures.csv)")


# %% CELL 6  --  indices
IDX = [".OMXSPI", ".OMXSGI", ".OMXS30", ".OMXS30GI", ".OMXSB", ".OMXSBGI", ".OMXSBCAPGI", ".SIXRX", ".SIXPRX"]
for r in IDX:
    try:
        try:
            h = api(ld.get_history, universe=r, fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        except Exception:
            h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        h["ric"] = r; h.to_csv(f"{OUT}/index_{r.strip('.')}.csv")
        print(f"{r:14s} {len(h):5d} rows  {str(h.index.min())[:10]} to {str(h.index.max())[:10]}")
    except Exception as e:
        print(f"{r:14s} FAILED: {str(e)[:100]}")
# Must have: .OMXSGI (market total return) or .OMXSPI, and .OMXSBGI or .OMXSB. Tell Claude which failed.


# %% CELL 7  --  combine, static table, coverage check against the OMXSB events
def canon(c):
    cl = str(c).lower()
    if c == "TRDPRC_1" or "price close" in cl: return "close"
    if c == "ACVOL_UNS" or cl == "volume": return "volume"
    if "total return" in cl: return "totret"
    if "market cap" in cl: return "mcap"
    if "shares" in cl: return "shares"
    if c == "TRNOVR_UNS" or "turnover" in cl: return "turnover"
    return c
parts = []
for f in sorted(os.listdir(f"{OUT}/daily")):
    d = pd.read_csv(f"{OUT}/daily/{f}", index_col=0, parse_dates=True); d.index.name = "date"
    d = d.rename(columns=canon); d = d.loc[:, ~d.columns.duplicated()]
    parts.append(d.reset_index())
daily = pd.concat(parts, ignore_index=True)
keep = [c for c in ["ric", "date", "close", "totret", "volume", "mcap", "shares", "turnover", "source"] if c in daily]
daily = daily[keep].sort_values(["ric", "date"]); daily.to_csv(f"{OUT}/stocks_daily.csv", index=False)
uni = pd.read_csv(f"{OUT}/universe.csv").rename(columns={"RIC": "ric"})
static = (daily.groupby("ric").agg(first_date=("date", "min"), last_date=("date", "max"), n_days=("date", "size"))
          .reset_index().merge(uni[[c for c in ["ric", "DTSubjectName", "IssueISIN", "RetireDate", "ExchangeCode"] if c in uni]], on="ric", how="left"))
static.to_csv(f"{OUT}/stocks_static.csv", index=False)
print("stocks_daily:", daily.shape, "| columns:", keep)
print("rows by source:", daily["source"].value_counts().to_dict() if "source" in daily else "n/a")
print("latest date in data:", daily["date"].max())

omx = pd.read_csv(f"{OUT}/omxsb_ric_map.csv")
ev = pd.read_csv("omxsb_changes_2013_2026.csv").merge(omx[["ticker", "RIC"]], on="ticker", how="left")
ad = pd.to_datetime(ev["announcement_date"], errors="coerce"); ed = pd.to_datetime(ev["effective_date"], errors="coerce")
cov = []
for k in range(len(ev)):
    d = daily[(daily["ric"] == ev.loc[k, "RIC"]) & (daily["date"] >= ad[k] - pd.Timedelta(days=3)) & (daily["date"] <= ed[k] + pd.Timedelta(days=3))]
    cov.append(int(d["close"].notna().sum()) if "close" in d else 0)
ev["days_with_price"] = cov
print(f"\nOMXSB coverage: {(ev['days_with_price'] >= 10).sum()} of {len(ev)} events have prices from announcement to effective day")
print(ev[ev["days_with_price"] < 10][["event_id", "company", "ticker", "RIC", "days_with_price"]].to_string())
# SEND CLAUDE: the coverage line and the list under it.


# %% CELL 8  --  zip everything for download
shutil.make_archive("thesis_data", "zip", OUT)
print("thesis_data.zip is ready. Right-click it in the CodeBook file browser -> Download,")
print("then unzip into ~/Documents/financethesis_fresh/thesis2/data/prices/")
