import os, sys, re
import numpy as np, pandas as pd

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EV = os.path.join(REPO, "data", "input", "omxsb")
D = os.path.join(REPO, "data", "raw", "lseg", "panel_2005_2026")
OUT = os.path.join(REPO, "theses", "03_omxsb_indexeffekt", "historik", "omxsb_replication_2007")  # flyttad 13 nov 2026 från output/omxsb_replication_2007
os.makedirs(OUT, exist_ok=True)
COLS = ["event_id", "effective_date", "announcement_date", "company", "ticker", "isin", "type", "review_cycle", "source_url", "verification", "notes"]

log_lines = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log_lines.append(s)

e1 = pd.read_csv(os.path.join(EV, "omxsb_changes_2005_2012.csv"))
e2 = pd.read_csv(os.path.join(EV, "omxsb_changes_2013_2026.csv"))
assert list(e1.columns) == COLS and list(e2.columns) == COLS
ev = pd.concat([e1, e2], ignore_index=True)
ev = ev.sort_values(["effective_date", "event_id"], kind="stable").reset_index(drop=True)
assert len(ev) == 536 and ev.event_id.is_unique
ev.to_csv(os.path.join(EV, "omxsb_changes_2007_2026.csv"), index=False)
log(f"omxsb_changes_2007_2026.csv: {len(ev)} events, {ev.review_cycle.nunique()} reviews, {ev.effective_date.min()} to {ev.effective_date.max()}")

uni = pd.read_csv(os.path.join(D, "td_universe.csv"))
uni["RIC"] = uni["RIC"].astype(str)
st = pd.read_csv(os.path.join(D, "stocks_static_2005.csv"))
st["RIC"] = st["ric"].astype(str)
px = pd.read_parquet(os.path.join(D, "stocks_daily_2005.parquet"), columns=["ric", "date", "close"])
px["date"] = pd.to_datetime(px.date)
span = px.groupby("ric").date.agg(px_first="min", px_last="max")
cand = pd.concat([uni[["RIC", "DTSubjectName", "IssueISIN", "RetireDate"]], st[["RIC", "DTSubjectName", "IssueISIN", "RetireDate"]]], ignore_index=True)
cand = cand.sort_values("DTSubjectName", na_position="last").drop_duplicates("RIC", keep="first").reset_index(drop=True)
cand = cand.merge(span, left_on="RIC", right_index=True, how="left")
cand["RetireDate"] = pd.to_datetime(cand.RetireDate, errors="coerce")
log(f"candidate RICs: {len(cand)} (universe {uni.RIC.nunique()}, static {st.RIC.nunique()}), {cand.px_first.notna().sum()} with prices in the parquet")

def ric_base(t):
    p = str(t).strip().split()
    return p[0] + "".join(x.lower() for x in p[1:])
def norm(s):
    s = pd.Series([str(s)]).str.replace(r"\(publ\)|\bAB\b|\bser\.?\b|\bSDB\b|\bplc\b|,|\.", " ", regex=True, case=False)
    return " ".join(s.iloc[0].lower().split())
def sim(a, b):
    A, B = set(a.split()), set(b.split())
    return len(A & B) / max(1, len(A | B))
cand["base"] = cand.RIC.str.replace(r"\.ST(\^.*)?$", "", regex=True)
cand["nname"] = cand.DTSubjectName.map(lambda x: norm(x) if pd.notna(x) else "")

known = pd.read_csv(os.path.join(EV, "omxsb_events_with_ric.csv"))
kmap = known.drop_duplicates("ticker").set_index("ticker")[["RIC", "company"]]
old = ev[ev.effective_date < "2013-01-01"].copy()
new = ev[ev.effective_date >= "2013-01-01"].copy()
assert len(old) == 142 and len(new) == 394

def alive_at(hit, ed):
    a = hit[(hit.RetireDate.isna() | (hit.RetireDate >= ed)) & (hit.px_first.isna() | (hit.px_first <= ed))]
    return a if len(a) else hit

rows = []
for tk, grp in old.groupby("ticker", sort=False):
    name, base = grp.company.iloc[0], ric_base(tk)
    ed = pd.to_datetime(grp.effective_date).max()
    if tk in kmap.index:
        r = cand[cand.RIC == kmap.RIC[tk]]
        rows.append(dict(ticker=tk, company=name, ric_base=base, RIC=kmap.RIC[tk], matched_name=r.DTSubjectName.iloc[0] if len(r) else None, how="known", n_candidates=1, known_company=kmap.company[tk]))
        continue
    hit, how = cand[cand.base == base], "ticker"
    if hit.empty:
        hit = cand[cand.base.str.lower() == base.lower()]
    if hit.empty:
        sc = cand.nname.map(lambda x: sim(norm(name), x) if x else 0.0)
        hit, how = cand[sc >= 0.5].assign(score=sc[sc >= 0.5]).sort_values("score", ascending=False).head(3), "name"
    n = len(hit)
    if len(hit) > 1:
        hit = alive_at(hit, ed)
        if len(hit) > 1:
            hit = hit.sort_values("RetireDate", na_position="last").head(1)
    rows.append(dict(ticker=tk, company=name, ric_base=base, RIC=hit.RIC.iloc[0] if len(hit) else None, matched_name=hit.DTSubjectName.iloc[0] if len(hit) else None, how=how if len(hit) else "UNMATCHED", n_candidates=n, known_company=None))
m = pd.DataFrame(rows)
log("")
log("mapping of the 2007-2012 tickers:", m.how.value_counts().to_dict())
log("")
log("Reused from omxsb_events_with_ric.csv (ticker, company 2007-2012, RIC, company 2013-2026, LSEG name):")
log(m[m.how == "known"][["ticker", "company", "RIC", "known_company", "matched_name"]].to_string(index=False))
log("")
log("Matched by ticker (ticker, company, RIC, LSEG name):")
log(m[m.how == "ticker"][["ticker", "company", "RIC", "matched_name"]].to_string(index=False))
log("")
log("Matched by NAME, check these (ticker, company, RIC, LSEG name, RetireDate, first and last price date, last effective date of the ticker):")
nm = m[m.how == "name"].merge(cand[["RIC", "RetireDate", "px_first", "px_last"]], on="RIC", how="left").merge(old.groupby("ticker").effective_date.max().rename("last_ED"), on="ticker")
log(nm[["ticker", "company", "RIC", "matched_name", "RetireDate", "px_first", "px_last", "last_ED"]].to_string(index=False) if len(nm) else "none")
log("")
log("UNMATCHED (RIC left empty; nearest candidates by name similarity are listed for manual review only and are not used):")
um = m[m.how == "UNMATCHED"]
for r in um.itertuples():
    sc = cand.nname.map(lambda x: sim(norm(r.company), x) if x else 0.0)
    near = cand[sc > 0].assign(score=sc[sc > 0]).sort_values("score", ascending=False).head(3)
    log(f"  {r.ticker:10s} {r.company:40s} nearest: " + ("; ".join(f"{a} ({b}, {c:.2f})" for a, b, c in zip(near.RIC, near.DTSubjectName, near.score)) if len(near) else "none"))
if not len(um):
    log("none")

isin_chk = old.drop_duplicates("ticker")[["ticker", "isin"]].merge(m[["ticker", "RIC"]], on="ticker").merge(cand[["RIC", "IssueISIN"]], on="RIC", how="left")
isin_chk = isin_chk[isin_chk["isin"].notna() & isin_chk.IssueISIN.notna()]
bad = isin_chk[isin_chk["isin"] != isin_chk.IssueISIN]
log("")
log(f"ISIN diagnostic (not used for matching): {len(isin_chk)} tickers with an ISIN in both the event list and LSEG, {len(bad)} disagree")
if len(bad):
    log(bad.to_string(index=False))

old = old.merge(m[["ticker", "RIC"]], on="ticker", how="left")
new = new.merge(known[["event_id", "RIC"]], on="event_id", how="left")
assert new.RIC.notna().all()
allv = pd.concat([old, new], ignore_index=True).sort_values(["effective_date", "event_id"], kind="stable").reset_index(drop=True)
ad = pd.to_datetime(allv.announcement_date)
ed = pd.to_datetime(allv.effective_date)
sub = px[px.ric.isin(set(allv.RIC.dropna()))]
cov = []
for k in range(len(allv)):
    if pd.isna(allv.RIC[k]):
        cov.append(0)
        continue
    d = sub[(sub.ric == allv.RIC[k]) & (sub.date >= ad[k] - pd.Timedelta(days=3)) & (sub.date <= ed[k] + pd.Timedelta(days=3))]
    cov.append(int(d.close.notna().sum()))
allv["days_with_price"] = cov
allv = allv[COLS + ["RIC", "days_with_price"]]
allv.to_csv(os.path.join(EV, "omxsb_events_with_ric_2007_2026.csv"), index=False)
ok = allv.days_with_price >= 10
log("")
log(f"OMXSB coverage on stocks_daily_2005.parquet: {int(ok.sum())} of {len(allv)} events have at least 10 days with a close between AD-3 and ED+3")
log(f"  2007-2012: {int(ok[allv.effective_date < '2013-01-01'].sum())} of {int((allv.effective_date < '2013-01-01').sum())}; 2013-2026: {int(ok[allv.effective_date >= '2013-01-01'].sum())} of {int((allv.effective_date >= '2013-01-01').sum())}")
fail = allv[~ok][["event_id", "company", "ticker", "RIC", "effective_date", "days_with_price"]]
fail.to_csv(os.path.join(OUT, "coverage_failures.csv"), index=False)
log("Coverage failures:")
log(fail.to_string(index=False) if len(fail) else "none")
chg = allv.merge(known[["event_id", "days_with_price"]].rename(columns={"days_with_price": "days_old"}), on="event_id")
chg = chg[chg.days_with_price != chg.days_old]
log("")
log(f"2013-2026 events whose days_with_price differs from omxsb_events_with_ric.csv (2012 pull): {len(chg)}")
if len(chg):
    log(chg[["event_id", "company", "RIC", "days_old", "days_with_price"]].to_string(index=False))
with open(os.path.join(OUT, "mapping_review.txt"), "w") as f:
    f.write("\n".join(log_lines) + "\n")
