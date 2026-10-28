"""
lseg_pull_v4.py  --  thesis 2 stock panel from LSEG Workspace CodeBook.

CodeBook blocks os, shutil, glob and other filesystem modules, so this version uses only pandas
and the LSEG library. All output is written as flat files in the notebook folder, prefixed td_.
Run one cell at a time, in order. After any kernel restart, rerun CELL 0 first.
Upload next to this notebook: omxsb_changes_2013_2026.csv, isin_list_lseg_v2.csv
"""

# %% CELL 0  --  session, helpers, smoke tests (rerun after every restart)
import pandas as pd
try:
    import lseg.data as ld
except Exception:
    import refinitiv.data as ld
try:
    import time
    def pause(s): time.sleep(s)
except Exception:
    def pause(s): pass

START = "2012-01-01"
END = pd.Timestamp.today().strftime("%Y-%m-%d")
MAX_CALLS = 9000                      # daily API quota is about 10,000 requests
CALLS = {"n": 0}

def api(fn, *a, **k):
    CALLS["n"] += 1
    if CALLS["n"] > MAX_CALLS:
        raise RuntimeError("budget: daily call budget reached, rerun tomorrow (everything resumes)")
    r = fn(*a, **k)
    pause(0.25)
    return r

def search(filter_, select, top=10000, query=None):
    kw = dict(view=ld.discovery.Views.EQUITY_QUOTES, filter=filter_, select=select, top=top)
    if query: kw["query"] = query
    return api(ld.discovery.search, **kw)

def exists(path):
    try:
        pd.read_csv(path, nrows=0); return True
    except Exception:
        return False

def save_cfg(d): pd.DataFrame([d]).to_csv("td_cfg.csv", index=False)
def load_cfg():
    c = pd.read_csv("td_cfg.csv").iloc[0].to_dict()
    c["FIELDS"] = str(c["FIELDS"]).split("|")
    c["INACTIVE_CLAUSE"] = None if pd.isna(c["INACTIVE_CLAUSE"]) else str(c["INACTIVE_CLAUSE"])
    return c

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
        print(f + " " * (24 - len(f)), "OK" if ok else "EMPTY")
        if ok: FIELDS.append(f)
    except Exception as e:
        print(f + " " * (24 - len(f)), "FAIL:", str(e)[:100])
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
        s = search("ExchangeCode eq 'STO' and " + clause, SEL, top=5, query="Klovern")
        print("\ninactive clause '" + clause + "':", len(s), "rows"); print(s.to_string())
        if len(s): INACTIVE_CLAUSE = clause; break
    except Exception as e:
        print("clause '" + clause + "' FAIL:", str(e)[:100])
print("\nINACTIVE_CLAUSE =", INACTIVE_CLAUSE, "(None means Search could not return delisted stocks: tell Claude)")
save_cfg({"FIELDS": "|".join(FIELDS), "SEL": SEL, "INACTIVE_CLAUSE": INACTIVE_CLAUSE})
# SEND CLAUDE everything this cell printed.


# %% CELL 1  --  universe: every Swedish share, active and delisted, alive at some point since 2012
cfg = load_cfg(); SEL = cfg["SEL"]; INACTIVE_CLAUSE = cfg["INACTIVE_CLAUSE"]
CATS = ["RCSAssetCategoryLeaf eq 'Ordinary Share'", "RCSAssetCategoryLeaf eq 'Depository Receipt'"]
frames, used = [], None
for base in ["RCSExchangeCountryLeaf eq 'Sweden'", "ExchangeCountry eq 'SWE'", "ExchangeCode eq 'STO'"]:
    try:
        for cat in CATS:
            a = search(base + " and " + cat, SEL); frames.append(a.assign(active_flag=True))
            if len(a) >= 10000: print("WARNING: active search hit the 10,000 cap for", cat)
            n_i = "n/a"
            if INACTIVE_CLAUSE:
                i = search(base + " and " + cat + " and " + INACTIVE_CLAUSE, SEL); frames.append(i.assign(active_flag=False))
                n_i = len(i)
                if len(i) >= 10000: print("WARNING: inactive search hit the 10,000 cap for", cat)
            print(base, "|", cat[-20:], ": active", len(a), ", inactive", n_i)
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
uni.to_csv("td_universe.csv", index=False)
n_del = int(uni["RIC"].str.contains(chr(94)).sum())
print("\nuniverse:", len(uni), "RICs, of which", n_del, "delisted (^). filter used:", used)
print(uni.head(8).to_string())
# SEND CLAUDE: the counts and the suffix list.


# %% CELL 2  --  resolve the fund-holdings ISIN list (safety net for stocks the losers own)
cfg = load_cfg(); SEL = cfg["SEL"]; INACTIVE_CLAUSE = cfg["INACTIVE_CLAUSE"]
INCLUDE_TIER2 = False   # True also pulls the non-Nordic stocks held by the European-round losers
L = pd.read_csv("isin_list_lseg_v2.csv")
if not INCLUDE_TIER2: L = L[L["tier"] == 1]
isins = L["isin"].astype(str).str.strip()
isins = sorted(set(isins[isins.str.match(r"^[A-Z]{2}[A-Z0-9]{10}$")]))
res = []
clauses = [""] + ([" and " + INACTIVE_CLAUSE] if INACTIVE_CLAUSE else [])
for k in range(0, len(isins), 50):
    chunk = ",".join("'" + x + "'" for x in isins[k:k + 50])
    for extra in clauses:
        try:
            res.append(search("IssueISIN in (" + chunk + ")" + extra, SEL, top=2000))
        except Exception as e:
            print("isin chunk", k, "FAIL:", str(e)[:100])
isin_res = pd.concat(res, ignore_index=True).drop_duplicates("RIC") if res else pd.DataFrame(columns=["RIC", "IssueISIN"])
if len(isin_res):
    home = pd.Series("", index=isin_res.index)
    pref = isin_res["IssueISIN"].astype(str).str[:2]
    pat = pref.map({"SE": r"\.ST(\^|$)", "DK": r"\.CO(\^|$)", "FI": r"\.HE(\^|$)", "NO": r"\.OL(\^|$)"})
    keep = pd.Series(True, index=isin_res.index)
    for p in pat.dropna().unique():
        m = pat == p
        keep[m] = isin_res.loc[m, "RIC"].astype(str).str.contains(p, regex=True)
    isin_res = isin_res[keep]
isin_res.to_csv("td_isin_resolved.csv", index=False)
found = set(isin_res["IssueISIN"]) if len(isin_res) else set()
print("ISINs in list:", len(isins), "| resolved to a home-exchange share:", len(found), "| unresolved:", len(set(isins) - found))
print("(unresolved ones are mostly bonds and fund units; that is expected)")


# %% CELL 3  --  map the 394 OMXSB events to RICs, delisted included
uni = pd.read_csv("td_universe.csv"); uni["RIC"] = uni["RIC"].astype(str)
ev = pd.read_csv("omxsb_changes_2013_2026.csv")
def ric_base(t):
    p = str(t).strip().split()
    return p[0] + "".join(x.lower() for x in p[1:])      # 'BALD B' -> 'BALDb', 'ALIV SDB' -> 'ALIVsdb'
def norm(s):
    s = pd.Series([str(s)]).str.replace(r"\(publ\)|\bAB\b|\bser\.?\b|\bSDB\b|\bplc\b|,|\.", " ", regex=True, case=False)
    return " ".join(s.iloc[0].lower().split())
def sim(a, b):
    A, B = set(a.split()), set(b.split())
    return len(A & B) / max(1, len(A | B))
uni["base"] = uni["RIC"].str.replace(r"\.ST(\^.*)?$", "", regex=True)
uni["nname"] = uni["DTSubjectName"].map(norm)
rows = []
for tk, grp in ev.groupby("ticker"):
    name, base = grp["company"].iloc[0], ric_base(tk)
    hit, how = uni[uni["base"] == base], "ticker"
    if hit.empty: hit = uni[uni["base"].str.lower() == base.lower()]
    if hit.empty:
        sc = uni["nname"].map(lambda x: sim(norm(name), x))
        hit, how = uni[sc >= 0.5].assign(score=sc[sc >= 0.5]).sort_values("score", ascending=False).head(3), "name"
    if len(hit) > 1:                                      # several listings: keep the one alive at the event
        ed = pd.to_datetime(grp["effective_date"], errors="coerce").max()
        rd_ = pd.to_datetime(hit["RetireDate"], errors="coerce") if "RetireDate" in hit else pd.Series(pd.NaT, index=hit.index)
        alive = hit[rd_.isna() | (rd_ >= ed)]
        hit = alive if len(alive) else hit
    rows.append({"ticker": tk, "company": name, "ric_base": base,
                 "RIC": hit["RIC"].iloc[0] if len(hit) else None,
                 "matched_name": hit["DTSubjectName"].iloc[0] if len(hit) else None,
                 "how": how if len(hit) else "UNMATCHED", "n_candidates": len(hit)})
omx = pd.DataFrame(rows); omx.to_csv("td_omxsb_map.csv", index=False)
print(omx["how"].value_counts().to_dict())
print("\nUNMATCHED: type the RIC by hand into td_omxsb_map.csv (Workspace search box: company name; delisted RICs end in ^):")
print(omx[omx["how"] == "UNMATCHED"][["ticker", "company"]].to_string())
print("\nMatched by NAME, check these:")
print(omx[omx["how"] == "name"][["ticker", "company", "RIC", "matched_name"]].to_string())
# SEND CLAUDE: this output.


# %% CELL 4  --  final download list
uni = pd.read_csv("td_universe.csv")
isin_res = pd.read_csv("td_isin_resolved.csv") if exists("td_isin_resolved.csv") else pd.DataFrame()
omx = pd.read_csv("td_omxsb_map.csv")
rics = set(uni["RIC"].dropna().astype(str)) | set(isin_res.get("RIC", pd.Series(dtype=str)).dropna().astype(str)) \
       | set(omx["RIC"].dropna().astype(str))
rics = sorted(r for r in rics if r and r != "nan")
pd.DataFrame({"ric": rics}).to_csv("td_rics_final.csv", index=False)
print(len(rics), "RICs to download;", sum("^" in r for r in rics), "delisted")


# %% CELL 5  --  daily history, one RIC per call, resumable (rerun until 'to download' is 0)
cfg = load_cfg(); FIELDS = cfg["FIELDS"]
rics = pd.read_csv("td_rics_final.csv")["ric"].astype(str).tolist()
done = set(pd.read_csv("td_done.csv")["ric"].astype(str)) if exists("td_done.csv") else set()
CHUNK = 250                                            # 250 stocks per output file
def pull(r):
    err = ""
    try:
        h = api(ld.get_history, universe=r, fields=FIELDS, start=START, end=END, interval="daily")
        if h is not None and len(h): return h.copy(), "tr"
        err = "tr empty"
    except Exception as e:
        err = "tr: " + str(e)[:120]
    try:                                               # fallback: pricing endpoint (close, volume, turnover)
        h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        if h is not None and len(h): return h.copy(), "pricing"
        err += " | pricing empty"
    except Exception as e:
        err += " | pricing: " + str(e)[:120]
    raise RuntimeError(err)

todo = [(k, r) for k, r in enumerate(rics) if r not in done]
print(len(todo), "to download,", len(done), "already on disk")
fails, n_ok = [], 0
for n, (k, r) in enumerate(todo, 1):
    try:
        h, src = pull(r)
        h.index.name = "date"; h = h.reset_index(); h.columns = [str(c) for c in h.columns]
        h["ric"] = r; h["source"] = src
        f = "td_%s_%03d.csv" % ("daily" if src == "tr" else "pricing", k // CHUNK)
        h.to_csv(f, mode="a", index=False, header=not exists(f))
        pd.DataFrame({"ric": [r]}).to_csv("td_done.csv", mode="a", index=False, header=not exists("td_done.csv"))
        n_ok += 1
    except RuntimeError as e:
        if "budget" in str(e): print("STOP:", e); break
        fails.append({"ric": r, "error": str(e)})
    if n % 100 == 0: print(n, "/", len(todo), "done,", len(fails), "failed,", CALLS["n"], "API calls this session")
if fails:
    pd.DataFrame(fails).to_csv("td_failures.csv", mode="a", index=False, header=not exists("td_failures.csv"))
print("finished this run:", n_ok, "downloaded,", len(fails), "failed (td_failures.csv)")


# %% CELL 6  --  indices
IDX = [".OMXSPI", ".OMXSGI", ".OMXS30", ".OMXS30GI", ".OMXSB", ".OMXSBGI", ".OMXSBCAPGI", ".SIXRX", ".SIXPRX"]
parts = []
for r in IDX:
    try:
        try:
            h = api(ld.get_history, universe=r, fields=["TR.PriceClose"], start=START, end=END, interval="daily")
        except Exception:
            h = api(ld.get_history, universe=r, start=START, end=END, interval="daily")
        h.index.name = "date"; h = h.reset_index(); h.columns = [str(c) for c in h.columns]
        col = [c for c in h.columns if c != "date"][0]
        parts.append(pd.DataFrame({"ric": r, "date": h["date"], "close": h[col]}))
        print(r + " " * (14 - len(r)), len(h), "rows ", str(h["date"].min())[:10], "to", str(h["date"].max())[:10])
    except Exception as e:
        print(r + " " * (14 - len(r)), "FAILED:", str(e)[:100])
if parts: pd.concat(parts).to_csv("indices_daily.csv", index=False)
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
rics = pd.read_csv("td_rics_final.csv")["ric"].astype(str).tolist()
n_files = len(rics) // 250 + 1
parts = []
for kind in ["daily", "pricing"]:
    for k in range(n_files):
        f = "td_%s_%03d.csv" % (kind, k)
        if not exists(f): continue
        d = pd.read_csv(f, low_memory=False).rename(columns=canon)
        d = d.loc[:, ~d.columns.duplicated()]
        keep = [c for c in ["ric", "date", "close", "totret", "volume", "mcap", "shares", "turnover", "source"] if c in d]
        parts.append(d[keep])
daily = pd.concat(parts, ignore_index=True)
daily["date"] = pd.to_datetime(daily["date"], errors="coerce")
daily = daily.sort_values(["ric", "date"])
daily.to_csv("stocks_daily.csv.gz", index=False, compression="gzip")
uni = pd.read_csv("td_universe.csv").rename(columns={"RIC": "ric"})
static = (daily.groupby("ric").agg(first_date=("date", "min"), last_date=("date", "max"), n_days=("date", "size")).reset_index()
          .merge(uni[[c for c in ["ric", "DTSubjectName", "IssueISIN", "RetireDate", "ExchangeCode"] if c in uni]], on="ric", how="left"))
static.to_csv("stocks_static.csv", index=False)
print("stocks_daily:", daily.shape, "| columns:", list(daily.columns))
print("rows by source:", daily["source"].value_counts().to_dict() if "source" in daily else "n/a")
print("latest date in data:", daily["date"].max())

omx = pd.read_csv("td_omxsb_map.csv")
ev = pd.read_csv("omxsb_changes_2013_2026.csv").merge(omx[["ticker", "RIC"]], on="ticker", how="left")
ad = pd.to_datetime(ev["announcement_date"], errors="coerce"); ed = pd.to_datetime(ev["effective_date"], errors="coerce")
sub = daily[daily["ric"].isin(set(ev["RIC"].dropna()))]
cov = []
for k in range(len(ev)):
    d = sub[(sub["ric"] == ev.loc[k, "RIC"]) & (sub["date"] >= ad[k] - pd.Timedelta(days=3)) & (sub["date"] <= ed[k] + pd.Timedelta(days=3))]
    cov.append(int(d["close"].notna().sum()) if "close" in d else 0)
ev["days_with_price"] = cov
print("\nOMXSB coverage:", int((ev["days_with_price"] >= 10).sum()), "of", len(ev), "events have prices from announcement to effective day")
print(ev[ev["days_with_price"] < 10][["event_id", "company", "ticker", "RIC", "days_with_price"]].to_string())
# SEND CLAUDE: the coverage line and the list under it.


# %% CELL 8  --  files to download
print("Download these from the file browser (right-click -> Download) into")
print("~/Documents/financethesis_fresh/thesis2/data/prices/ :")
for f in ["stocks_daily.csv.gz", "stocks_static.csv", "indices_daily.csv", "td_omxsb_map.csv", "td_universe.csv", "td_failures.csv"]:
    print("  ", f, "(exists)" if exists(f) else "(missing)")
