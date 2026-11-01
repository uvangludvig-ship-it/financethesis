"""Twin-share feasibility: OMXSB events 2007-2026 for companies with >1 listed share class on Nasdaq Stockholm.
Read-only on the repo; writes /home/claude/agent_scratch/twin_events.csv (+ summary prints).
Usage: python3 -I twin_events.py <repo_root>
"""
import re, sys
import numpy as np
import pandas as pd

R = sys.argv[1]
OUT = "/home/claude/agent_scratch/"
s05 = pd.read_csv(R + "/data/raw/lseg/panel_2005_2026/stocks_static_2005.csv")
s12 = pd.read_csv(R + "/data/raw/lseg/panel_2012_2026/stocks_static.csv")
tu = pd.read_csv(R + "/data/raw/lseg/panel_2005_2026/td_universe.csv").rename(columns={"RIC": "ric"})
ev = pd.read_csv(R + "/data/input/omxsb/omxsb_events_with_ric_2007_2026.csv")
car = pd.read_csv(R + "/output/omxsb_replication_2007/events_car.csv")
mem = pd.read_csv(R + "/output/omxsb_replication_2007/mechanisms/omxsb_membership_by_review.csv")
nt = pd.read_csv(R + "/output/omxsb_replication_2007/nettrading_omxsb.csv")

# ---------- event keys exactly as in code/build/mechanisms_2007.py ----------
ALIAS_T = {"TWW SDB": "TWW SDB B", "NOKIA SEK": "NOKI SEK", "NOKI SEK": "NOKI SEK"}
TICK_RIC = {"CYBE": "CYBC.ST^A16", "KAUP SEK": "KAUP.ST^L08", "CSN": "CISI.ST^H14", "RABT B": "VSSABb.ST", "WSIB SDB": "AOILsdb.ST^L13",
            "NOKI SEK": "NOKIA.ST", "HAKN": "ICAA.ST^A22", "TWW SDB B": "TWWsdbb.ST^K14", "AWP": "ARISE.ST^A26", "BVT": "SOBIV.ST"}
def key_of(ric, ticker):
    t = ALIAS_T.get(str(ticker).strip(), str(ticker).strip())
    if isinstance(ric, str) and ric:
        return "NOKIA.ST" if ric == "NOKIsdb.ST^E07" else ric
    return TICK_RIC.get(t, "T:" + t)
ev["key"] = [key_of(r, t) for r, t in zip(ev.RIC, ev.ticker)]

# ---------- membership before/after each review ----------
mem = mem.sort_values("ED").reset_index(drop=True)
after = {c: set(m.split(";")) for c, m in zip(mem.review_cycle, mem.members_after)}
cyc = list(mem.review_cycle)
adds = {c: set(ev[(ev.review_cycle == c) & (ev.type == "addition")].key) for c in cyc}
dels = {c: set(ev[(ev.review_cycle == c) & (ev.type == "deletion")].key) for c in cyc}
before = {cyc[0]: (after[cyc[0]] - adds[cyc[0]]) | dels[cyc[0]]}
for i in range(1, len(cyc)):
    before[cyc[i]] = after[cyc[i - 1]]

# ---------- universe of Stockholm share lines ----------
ORD = {"", "a", "b", "c", "r", "sdb", "sdba", "sdbb"}          # ordinary classes / ordinary SDR classes
PREFLIKE = {"d", "pref", "prefb"}                              # preference-like (fixed dividend), not true twins
def parse(ric):
    if ric.startswith("T:"):
        m = re.match(r"^T:(\S+)\s+([A-Z])$", ric)
        return (m.group(1), m.group(2).lower()) if m else (ric[2:].split()[0], "")
    m = re.match(r"^([A-Z0-9_]+?)([a-z]*)\.ST(\^[A-L]\d\d)?$", ric)
    return (m.group(1), m.group(2)) if m else (None, None)

u = pd.DataFrame({"ric": sorted(set(s05.ric) | set(s12.ric) | set(tu.ric) | set(ev.key))})
u[["root", "cls"]] = pd.DataFrame(u.ric.map(parse).tolist(), index=u.index)
u = u[u.root.notna() & u.cls.isin(ORD | PREFLIKE)].copy()
u["source"] = "repo"
# sister classes listed on Nasdaq Stockholm but ABSENT from every repo file (external knowledge, flagged, not verifiable in repo)
EXTRA = [("NCCa.ST", "NCC", "a", None), ("RATOa.ST", "RATO", "a", None), ("SWECa.ST", "SWEC", "a", None),
         ("BONAVa.ST", "BONAV", "a", "2016-06-09"), ("STEa.ST", "STE", "a", None)]
u = pd.concat([u, pd.DataFrame([dict(ric=r, root=o, cls=c, source="external_not_in_repo", ext_start=s) for r, o, c, s in EXTRA])], ignore_index=True)
# T:STE A (membership key for Stora Enso A) is the same line as STEa.ST
u = u[u.ric != "T:STE A"]

def suffix_end(ric):
    m = re.search(r"\^([A-L])(\d\d)$", ric)
    if not m:
        return pd.NaT
    yy = int(m.group(2)); y = 1900 + yy if yy >= 80 else 2000 + yy
    return pd.Timestamp(year=y, month="ABCDEFGHIJKL".index(m.group(1)) + 1, day=1) + pd.offsets.MonthEnd(0)

S12 = s12.set_index("ric"); S05 = s05.set_index("ric")
def interval(row):
    r = row.ric
    start, start_note, end = pd.NaT, "", pd.NaT
    if r in S12.index:
        fd, ld = pd.Timestamp(S12.at[r, "first_date"]), pd.Timestamp(S12.at[r, "last_date"])
        if fd > pd.Timestamp("2012-01-04"):
            start, start_note = fd, "s12_first_date"
        else:
            start, start_note = pd.NaT, "listed_by_2012-01_start_unknown"
        if ld < pd.Timestamp("2026-10-01"):
            end = ld
    else:
        start_note = "not_in_s12_start_unknown"
    if row.source != "repo" and isinstance(row.get("ext_start"), str):
        start, start_note = pd.Timestamp(row.ext_start), "external"
    rd = S05.at[r, "RetireDate"] if r in S05.index else np.nan
    if isinstance(rd, str):
        end = min(end, pd.Timestamp(rd)) if pd.notna(end) else pd.Timestamp(rd)
    if pd.isna(end):
        end = suffix_end(r)
    return pd.Series(dict(start=start, start_note=start_note, end=end))
u = pd.concat([u, u.apply(interval, axis=1)], axis=1)
u["n_days_s05"] = u.ric.map(S05.n_days)     # padded panel: ~5,613 for almost every RIC (uninformative)
u["n_days_s12"] = u.ric.map(S12.n_days)     # days with a price in 2012-01..2026-10 (informative)
def bdays(a, b):
    return np.busday_count(a.date(), b.date()) if pd.notna(a) and pd.notna(b) else np.nan
u["s12_first"] = u.ric.map(S12.first_date); u["s12_last"] = u.ric.map(S12.last_date)
u["trade_day_share_s12"] = [n / bdays(pd.Timestamp(f), pd.Timestamp(l)) if pd.notna(n) and bdays(pd.Timestamp(f), pd.Timestamp(l)) > 0 else np.nan
                            for n, f, l in zip(u.n_days_s12, u.s12_first, u.s12_last)]

# turnover of a line, only where the line has its own event in events_car (G&S 'turn' at that event)
car["key"] = [key_of(r, t) for r, t in zip(car.RIC, car.ticker)]
car["ADt"] = pd.to_datetime(car.AD)

# ---------- events ----------
ev["AD"] = pd.to_datetime(ev.announcement_date); ev["ED"] = pd.to_datetime(ev.effective_date)
ev[["root", "cls"]] = pd.DataFrame(ev.key.map(parse).tolist(), index=ev.index)
ev.loc[ev.key == "T:STE A", ["root", "cls"]] = ["STE", "a"]
y = ev.ED.dt.year
ev["period5"] = np.select([y <= 2011, y <= 2016, y <= 2021], ["2007-11", "2012-16", "2017-21"], "2022-26")
ev["in_car_sample"] = ev.event_id.isin(car.event_id)
ev["in_nettrading_259"] = ev.event_id.isin(nt.event_id)
ev["n_isin_fi"] = ev.event_id.map(car.set_index("event_id").n_isin)

rows = []
for _, e in ev.iterrows():
    if e.root is None:
        continue
    sis = u[(u.root == e.root) & (u.ric != e.key) & (u.cls != e.cls)]
    for _, s in sis.iterrows():
        aliases = {s.ric, "T:" + s.root + " " + s.cls.upper()}
        # listing status on AD
        if pd.notna(s.end) and s.end < e.AD:
            listed = "no_delisted_before_AD"
        elif pd.notna(s.start) and s.start > e.AD:
            listed = "no_not_yet_listed"
        elif pd.notna(s.start):
            listed = "yes"
        elif aliases & (before[e.review_cycle] | after[e.review_cycle]):
            listed = "yes_omxsb_member"
        elif s.start_note.startswith("listed_by_2012") and e.AD >= pd.Timestamp("2012-01-02"):
            listed = "yes"
        else:
            listed = "assumed_start_unknown"
        same_rev = ev[(ev.review_cycle == e.review_cycle) & (ev.root == s.root) & (ev.cls == s.cls)]
        own = car[car.key == s.ric]
        own_turn, own_turn_date = (np.nan, None)
        if len(own):
            j = (own.ADt - e.AD).abs().idxmin(); own_turn, own_turn_date = own.at[j, "turn"], own.at[j, "AD"]
        rows.append(dict(
            event_id=e.event_id, review_cycle=e.review_cycle, AD=e.AD.date(), ED=e.ED.date(), period5=e.period5, type=e.type,
            company=e.company, ticker=e.ticker, event_key=e.key, class_changed=e.cls.upper() if e.cls else "(none)",
            sister_ric=s.ric, sister_class=s.cls.upper() if s.cls else "(none)",
            sister_kind=("same_class_other_form" if {s.cls, e.cls} == {"", "sdb"} else "ordinary") if s.cls in ORD else "preference_like",
            sister_source=s.source, sister_start=s.start.date() if pd.notna(s.start) else None, sister_start_note=s.start_note,
            sister_end=s.end.date() if pd.notna(s.end) else None, sister_listed_on_AD=listed,
            sister_changed_same_review=(same_rev.type.iloc[0] if len(same_rev) else ""),
            sister_member_before=bool(aliases & before[e.review_cycle]), sister_member_after=bool(aliases & after[e.review_cycle]),
            sister_n_days_s05_padded=s.n_days_s05, sister_n_days_s12=s.n_days_s12, sister_trade_day_share_s12=s.trade_day_share_s12,
            sister_excess_turn_at_own_event=own_turn, sister_own_event_AD=own_turn_date,
            event_in_car_sample=e.in_car_sample, event_tot_car=car.set_index("event_id").tot.get(e.event_id, np.nan),
            event_in_nettrading_259=e.in_nettrading_259, event_n_isin_fi=e.n_isin_fi))
T = pd.DataFrame(rows)
T["sister_listed"] = T.sister_listed_on_AD.str.startswith("yes") | (T.sister_listed_on_AD == "assumed_start_unknown")
T["usable_pair"] = T.sister_listed & (T.sister_changed_same_review == "") & (T.sister_kind == "ordinary")
# event-level
g = T.groupby("event_id")
E = ev.set_index("event_id").loc[g.size().index, ["review_cycle", "period5", "type", "company", "key", "root", "in_car_sample", "in_nettrading_259", "n_isin_fi"]]
E["any_ord_sister_listed"] = g.apply(lambda d: (d.sister_listed & (d.sister_kind == "ordinary")).any())
E["any_ord_sister_listed_repo"] = g.apply(lambda d: (d.sister_listed & (d.sister_kind == "ordinary") & (d.sister_source == "repo")).any())
E["only_pref_sister"] = g.apply(lambda d: not (d.sister_listed & (d.sister_kind == "ordinary")).any() and (d.sister_listed & (d.sister_kind != "ordinary")).any())
E["sister_changed_same_review"] = g.apply(lambda d: (d.sister_listed & (d.sister_kind == "ordinary") & (d.sister_changed_same_review != "")).any())
E["usable"] = g.apply(lambda d: d.usable_pair.any())
E["usable_repo_only"] = g.apply(lambda d: (d.usable_pair & (d.sister_source == "repo")).any())
E["usable_verified_listing"] = g.apply(lambda d: (d.usable_pair & d.sister_listed_on_AD.str.startswith("yes") & (d.sister_source == "repo")).any())
E["sister_in_index_both_sides"] = g.apply(lambda d: (d.usable_pair & d.sister_member_before & d.sister_member_after).any())
E["sister_out_of_index_both_sides"] = g.apply(lambda d: (d.usable_pair & ~d.sister_member_before & ~d.sister_member_after).any())
T["event_usable"] = T.event_id.map(E.usable)
T.sort_values(["AD", "event_id", "sister_ric"]).to_csv(OUT + "twin_events.csv", index=False)
E.to_csv(OUT + "twin_events_eventlevel.csv")

def summ(d, lab):
    print(f"\n== {lab}: events {len(d)}, reviews {d.review_cycle.nunique()}, companies {d.root.nunique()}")
    print(pd.crosstab(d.period5, d.type, margins=True))
multi = E[E.any_ord_sister_listed]
print("events in list:", len(ev), "| events with any same-root line (any status):", len(E))
print("events whose company has >=1 ORDINARY sister listed on AD:", len(multi), "(repo-only:", int(E.any_ord_sister_listed_repo.sum()), ")")
print("  of which sister changed in same review (excluded):", int(multi.sister_changed_same_review.sum()), "; events with both a changed and an unchanged sister:", int((multi.sister_changed_same_review & multi.usable).sum()))
print("events with only preference-like sister (D/pref):", int(E.only_pref_sister.sum()))
U = E[E.usable]
summ(U, "USABLE (incl. external sisters)")
summ(E[E.usable_repo_only], "USABLE, repo-derived sisters only")
summ(E[E.usable_verified_listing], "USABLE, sister in repo AND listing verified from repo (s12 dates or OMXSB membership)")
print("usable: sister in OMXSB before&after:", int(U.sister_in_index_both_sides.sum()), "| sister outside OMXSB before&after:", int(U.sister_out_of_index_both_sides.sum()))
print(pd.crosstab(U.sister_in_index_both_sides, U.type))
print("excluded (sister changed same review):"); print(E[E.sister_changed_same_review][["review_cycle","company","type","usable"]].to_string())
summ(U[U.in_car_sample], "USABLE and in the 487-event CAR sample")
print("\nusable by company:"); print(U.groupby("root").agg(n=("type", "size"), add=("type", lambda x: (x == "addition").sum()), first=("review_cycle", "min"), last=("review_cycle", "max")).sort_values("n", ascending=False).to_string())
# consistency with FI n_isin>1 flag in 2019-2026 (259 net-trading events)
n259 = ev[ev.in_nettrading_259].set_index("event_id")
flag_fi = n259.n_isin_fi > 1
mine = n259.index.isin(E[E.any_ord_sister_listed | E.only_pref_sister].index)
print("\n259 net-trading events: n_isin>1 (FI name match):", int(flag_fi.sum()), "| mine (any listed sister, ord or pref):", int(mine.sum()),
      "| mine ordinary:", int(n259.index.isin(E[E.any_ord_sister_listed].index).sum()), "| both:", int((flag_fi & mine).sum()))
x = n259.assign(fi=flag_fi, mine=mine)
print("FI-flagged but no listed sister:", x[x.fi & ~x.mine][["company", "n_isin_fi"]].to_string())
print("listed sister but not FI-flagged:", x[~x.fi & x.mine][["company", "n_isin_fi"]].to_string())
