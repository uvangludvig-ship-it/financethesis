"""Greenwood & Sammon (2025) tests of the five explanations for the disappearing index effect, on OMXSB 2007-2026.

Reads the event file of the 2007 replication (events_car.csv), the LSEG daily panel, the change lists, the
81-name constituent table of 2009-05-11, the deletion reasons and the hand-built tracker AUM table, and writes
output/omxsb_replication_2007/mechanisms/ (RESULTS.md, numbers_mechanisms.json, figures as png + csv, tables as csv).
Inference functions (ols, wcb, cell, diffcell) are taken from code/notebooks/replication_omxsb_2007.ipynb.
No return is computed around an FTN date; only OMXSB events are used.
"""
import os, re, json, warnings
import numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT0 = os.path.join(REPO, "output", "omxsb_replication_2007")
OUT = os.path.join(OUT0, "mechanisms")
D = os.path.join(REPO, "data", "raw", "lseg", "panel_2005_2026")
EV = os.path.join(REPO, "data", "input", "omxsb")
os.makedirs(OUT, exist_ok=True)
PER = ["2007–2012", "2013–2017", "2018–2020", "2021–2023", "2024–2026"]
BINS = [2006, 2012, 2017, 2020, 2023, 2026]
STYLE = {"font.family": "serif", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "lines.linewidth": 1.4, "figure.dpi": 150, "savefig.bbox": "tight", "axes.unicode_minus": False}
plt.rcParams.update(STYLE)
PAL = ["#B0B0B0", "#000000", "#000000", "#6E6E6E", "#1F4E79"]
LS = [dict(color=PAL[0], linestyle="-"), dict(color=PAL[1], linestyle="-"), dict(color=PAL[2], linestyle="--"), dict(color=PAL[3], linestyle="-"), dict(color=PAL[4], linestyle="-.")]
NUM, ROWS, PROBLEMS = {}, [], []

# ---------- inference functions from the notebook ----------
nb = json.load(open(os.path.join(REPO, "code", "notebooks", "replication_omxsb_2007.ipynb")))
src = next("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code" and "def wcb(" in "".join(c["source"]))
ns = {"np": np, "pd": pd, "stats": stats, "PER": PER}
exec(src.split("rows = []")[0], ns)
ols, wcb, cell, diffcell = ns["ols"], ns["wcb"], ns["cell"], ns["diffcell"]

def coef_table(y, X, g, names, seed=0):
    """OLS with HC1, CR1 and wild cluster bootstrap p per coefficient (no constant unless included in X)."""
    y = np.asarray(y, float); X = np.asarray(X, float); g = np.asarray(g)
    b, e, Vh, Vc, G, gs, XtXi = ols(y, X, g)
    n, k = X.shape
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    out = []
    for j, nm in enumerate(names):
        r = np.zeros(k); r[j] = 1.0
        t, pw, _ = wcb(y, X, g, r, seed=seed + j)
        th, tc = b[j] / np.sqrt(Vh[j, j]), b[j] / np.sqrt(Vc[j, j])
        out.append(dict(var=nm, coef=b[j], se_hc1=np.sqrt(Vh[j, j]), p_hc1=2 * stats.norm.sf(abs(th)), se_cr1=np.sqrt(Vc[j, j]), p_cr1=2 * stats.t.sf(abs(tc), G - 1), p_wcb=pw, N=n, G=G, r2=r2))
    return pd.DataFrame(out)

def add_row(expl, test, sample, stat, c, same, sentence, **kw):
    ROWS.append(dict(explanation=expl, test=test, sample=sample, statistic=stat, coef=c.get("coef", c.get("mean")), se_hc1=c.get("se_hc1"), se_cr1=c.get("se_cr1"), p_hc1=c.get("p_hc1"), p_cr1=c.get("p_cr1"), p_wcb=c.get("p_wcb"), N=c.get("N"), G=c.get("G"), same_as_gs=same, what_it_shows=sentence, **kw))

# ---------- data ----------
ev = pd.read_csv(os.path.join(OUT0, "events_car.csv"), parse_dates=["AD", "ED", "announcement_date", "effective_date"])
assert len(ev) == 487, len(ev)
px = pd.read_parquet(os.path.join(D, "stocks_daily_2005.parquet"))
px["date"] = pd.to_datetime(px.date).astype("datetime64[ns]")
ix = pd.read_csv(os.path.join(D, "indices_daily (1).csv"), parse_dates=["date"])
cal = pd.DatetimeIndex(ix.loc[(ix.ric == ".OMXSBGI") & ix.close.notna(), "date"].sort_values().unique())
pend = px.date.max()
px = px[px.date.isin(cal) & px.ric.str.contains(r"\.ST", regex=True)].sort_values(["ric", "date"]).reset_index(drop=True)
last_date = px.groupby("ric").date.max()
pos = pd.Series(np.arange(len(cal)), index=cal)
ev["iAD"] = ev.AD.map(pos).astype(int)
ev["iED"] = ev.ED.map(pos).astype(int)
ev["adx"] = ev.AD.dt.strftime("%Y-%m-%d")
ev["year"] = ev.ED.dt.year
rm = ix.pivot(index="date", columns="ric", values="close").reindex(cal).pct_change() * 100
mkt = rm[".OMXSBGI"]
NUM["n_st_rics_in_panel"] = int(px.ric.nunique())
NUM["n_st_stocks_with_close_per_year"] = {int(y): int(v) for y, v in px[px.close.notna()].groupby(px.date.dt.year).ric.nunique().items()}

def rser(ric):
    g = px[px.ric == ric].set_index("date")
    r = g.totret.fillna(g.close.pct_change() * 100)
    return r.reindex(cal[(cal >= g.index.min()) & (cal <= g.index.max())])
RICS = ev.RIC.unique()
AR = pd.DataFrame({r: rser(r) for r in RICS}).reindex(cal).sub(mkt, axis=0)
def wsum(ric, a, b):
    s = AR[ric].iloc[a:b + 1]
    return np.nan if s.isna().any() else s.sum()

# ---------- Step 1: flags on deletions ----------
rs = pd.read_csv(os.path.join(EV, "deletion_reasons_2007_2026.csv"))
ev = ev.merge(rs[["event_id", "deletion_reason"]], on="event_id", how="left")
isdel = ev.type == "deletion"
i100 = np.minimum(ev.iED + 100, len(cal) - 1)
ev["last_px"] = ev.RIC.map(last_date)
ev["flag_delist"] = isdel & (ev.last_px < cal[i100].values) & (ev.last_px < pend)
ev["flag_offer"] = isdel & ev.deletion_reason.isin(["public_offer", "merger_or_acquirer", "delisting_application"])
sh = px.pivot(index="date", columns="ric", values="shares").reindex(cal)
def share_jump(ric, i):
    s = sh[ric]
    a = s.iloc[i:i + 6].dropna()
    b = s.iloc[max(i + 50, 0):i + 101].dropna()
    if a.empty or b.empty:
        return np.nan
    return b.iloc[-1] / a.iloc[0] - 1
ev["share_chg"] = [share_jump(r, i) if d else np.nan for r, i, d in zip(ev.RIC, ev.iED, isdel)]
ev["flag_shares"] = isdel & (ev.share_chg.abs() > 0.10)
ev["flagged"] = ev.flag_delist | ev.flag_offer | ev.flag_shares
NUM["step1"] = dict(deletions=int(isdel.sum()), flag_delist_100td=int(ev.flag_delist.sum()), flag_offer=int(ev.flag_offer.sum()), flag_shares_10pct=int(ev.flag_shares.sum()), flag_shares_increase=int((isdel & (ev.share_chg > 0.10)).sum()), flag_shares_decrease=int((isdel & (ev.share_chg < -0.10)).sum()), shares_missing=int((isdel & ev.share_chg.isna()).sum()), flagged_any=int(ev.flagged.sum()), flagged_by_period={p: int(ev[(ev.period == p)].flagged.sum()) for p in PER})
ev[isdel][["event_id", "company", "RIC", "period", "AD", "ED", "tot", "deletion_reason", "last_px", "share_chg", "flag_delist", "flag_offer", "flag_shares", "flagged"]].to_csv(os.path.join(OUT, "step1_deletion_flags.csv"), index=False)
def SMP():
    return {"all": ev, "clean": ev[~ev.flagged]}
print("Step 1:", NUM["step1"])

# ---------- membership reconstruction ----------
ch = pd.read_csv(os.path.join(EV, "omxsb_events_with_ric_2007_2026.csv"), parse_dates=["effective_date", "announcement_date"])
cons = pd.read_csv(os.path.join(EV, "omxsb_constituents_2009_06_01.csv"), dtype=str).fillna("")
ALIAS_T = {"TWW SDB": "TWW SDB B", "NOKIA SEK": "NOKI SEK", "NOKI SEK": "NOKI SEK"}
TICK_RIC = {"CYBE": "CYBC.ST^A16", "KAUP SEK": "KAUP.ST^L08", "CSN": "CISI.ST^H14", "RABT B": "VSSABb.ST", "WSIB SDB": "AOILsdb.ST^L13", "NOKI SEK": "NOKIA.ST", "HAKN": "ICAA.ST^A22", "TWW SDB B": "TWWsdbb.ST^K14", "AWP": "ARISE.ST^A26", "BVT": "SOBIV.ST"}
def key_of(ric, ticker):
    t = ALIAS_T.get(str(ticker).strip(), str(ticker).strip())
    if isinstance(ric, str) and ric:
        if ric == "NOKIsdb.ST^E07":
            return "NOKIA.ST"
        return ric
    return TICK_RIC.get(t, "T:" + t)
ch["key"] = [key_of(r, t) for r, t in zip(ch.RIC, ch.ticker)]
cons["key"] = [key_of(r, t) for r, t in zip(cons.RIC, cons.ticker)]
ch["ED"] = ch.effective_date.map(lambda d: cal[cal.searchsorted(d)])
ch["AD"] = ch.announcement_date.map(lambda d: cal[cal.searchsorted(d)])
rev = ch.groupby("review_cycle").agg(ED=("ED", "first"), AD=("AD", "first")).sort_values("ED")
rev["adds"] = [set(ch[(ch.review_cycle == c) & (ch.type == "addition")].key) for c in rev.index]
rev["dels"] = [set(ch[(ch.review_cycle == c) & (ch.type == "deletion")].key) for c in rev.index]
cyc = list(rev.index)
i0 = cyc.index("2009H1")
after = {cyc[i0]: set(cons.key)}
incons = []
for i in range(i0 + 1, len(cyc)):
    S = set(after[cyc[i - 1]])
    for k in rev.dels[cyc[i]]:
        if k not in S:
            incons.append((cyc[i], "deleted but not a member", k))
    for k in rev.adds[cyc[i]]:
        if k in S:
            incons.append((cyc[i], "added but already a member", k))
    after[cyc[i]] = (S - rev.dels[cyc[i]]) | rev.adds[cyc[i]]
for i in range(i0, 0, -1):
    S = set(after[cyc[i]])
    for k in rev.adds[cyc[i]]:
        if k not in S:
            incons.append((cyc[i], "added but not in the set after the review (backward chain)", k))
    for k in rev.dels[cyc[i]]:
        if k in S:
            incons.append((cyc[i], "deleted but still in the set after the review (backward chain)", k))
    after[cyc[i - 1]] = (S - rev.adds[cyc[i]]) | rev.dels[cyc[i]]
before = {cyc[0]: (after[cyc[0]] - rev.adds[cyc[0]]) | rev.dels[cyc[0]]}
for i in range(1, len(cyc)):
    before[cyc[i]] = after[cyc[i - 1]]
pd.DataFrame(incons, columns=["review_cycle", "problem", "key"]).to_csv(os.path.join(OUT, "membership_inconsistencies.csv"), index=False)
mc = px.pivot(index="date", columns="ric", values="mcap").reindex(cal)
no_mcap = [r for r in mc.columns if mc[r].notna().sum() == 0]
cs = (px.assign(cs=px.close * px.shares)).pivot(index="date", columns="ric", values="cs").reindex(cal)
mc[no_mcap] = cs[no_mcap]
NUM["mcap_filled_from_close_x_shares"] = dict(n_rics_without_mcap=len(no_mcap), n_rics_filled=int(cs[no_mcap].notna().any().sum()), examples=[r for r in no_mcap if cs[r].notna().any()][:15])
def stem(r):
    return re.sub(r"(sdb)?[abcr]?\.ST.*$", "", r)
# are mcaps company-level (identical across share classes)?
pairs = []
for c in ["2010H1", "2015H1", "2020H1", "2025H1"]:
    d = cal[pos[rev.AD[c]] - 1]
    row = mc.loc[d].dropna()
    st_ = pd.Series(row.index.map(stem), index=row.index)
    for s_, grp in row.groupby(st_):
        if len(grp) >= 2:
            pairs.append(grp.max() / grp.min() - 1)
NUM["mcap_dual_class_median_ratio_minus_1"] = float(np.median(pairs)) if pairs else None
DEDUP = bool(pairs) and np.median(pairs) < 0.02
NUM["mcap_company_level_dedup"] = DEDUP
def alive(k, d):
    return (not k.startswith("T:")) and k in mc.columns and last_date.get(k, pd.Timestamp("1900-01-01")) >= cal[max(pos[d] - 10, 0)]
def total_mcap(members, d):
    rics = [k for k in members if alive(k, d)]
    v = mc.loc[d, rics].dropna()
    if DEDUP:
        v = v.groupby(v.index.map(stem)).max()
    return v.sum(), len(rics), int(v.shape[0])
top100 = mc.apply(lambda r: r.nlargest(100).sum(), axis=1)
cov, missing_members = [], []
for c in cyc:
    d = cal[pos[rev.AD[c]] - 1]
    tm, nric, nmc = total_mcap(before[c], d)
    dead = [k for k in before[c] if (not k.startswith("T:")) and k in mc.columns and not alive(k, d)]
    live = [k for k in before[c] if k not in dead]
    miss = [k for k in live if k.startswith("T:") or k not in mc.columns or pd.isna(mc.at[d, k])]
    missing_members.append(dict(review_cycle=c, n_missing=len(miss), missing=";".join(sorted(miss)), n_exited_delisted=len(dead), exited=";".join(sorted(dead))))
    cov.append(dict(review_cycle=c, AD=rev.AD[c].date(), ED=rev.ED[c].date(), n_members_before=len(live), n_exited_delisted=len(dead), n_with_ric=nric, n_with_mcap_ADm1=nmc, share_found=nmc / len(live), total_omxsb_mcap_bn=tm / 1e9, top100_mcap_bn=top100[d] / 1e9, n_members_after=len(after[c])))
cov = pd.DataFrame(cov)
pd.DataFrame(missing_members).to_csv(os.path.join(OUT, "membership_missing_mcap_by_review.csv"), index=False)
cov.to_csv(os.path.join(OUT, "membership_coverage_by_review.csv"), index=False)
pd.DataFrame({"review_cycle": cyc, "ED": [rev.ED[c].date() for c in cyc], "n_after": [len(after[c]) for c in cyc], "members_after": [";".join(sorted(after[c])) for c in cyc]}).to_csv(os.path.join(OUT, "omxsb_membership_by_review.csv"), index=False)
NUM["membership"] = dict(n_inconsistencies=len(incons), inconsistencies=[f"{a}: {b} ({k})" for a, b, k in incons], share_found_mean=float(cov.share_found.mean()), share_found_min=float(cov.share_found.min()), share_found_by_review={r.review_cycle: round(r.share_found, 3) for r in cov.itertuples()}, n_members_range=[int(cov.n_members_before.min()), int(cov.n_members_before.max())], total_mcap_over_top100_median=float((cov.total_omxsb_mcap_bn / cov.top100_mcap_bn).median()))
print("membership coverage mean", cov.share_found.mean(), "min", cov.share_found.min(), "inconsistencies", len(incons))
cyc_of = dict(zip(ch.event_id, ch.review_cycle))
ev["cycle"] = ev.event_id.map(cyc_of)
TOT = dict(zip(cov.review_cycle, cov.total_omxsb_mcap_bn * 1e9))
TOP = dict(zip(cov.review_cycle, cov.top100_mcap_bn * 1e9))
def members_on(d):
    c = [k for k in cyc if rev.ED[k] <= d]
    return after[c[-1]] if c else before[cyc[0]]

# ---------- E1: composition (Table 3) ----------
px["ym"] = px.date.dt.to_period("M")
mon = px.groupby(["ric", "ym"]).agg(vol=("volume", "sum"), nvol=("volume", "count"), shares=("shares", "last"), mcap=("mcap", "last")).reset_index()
mon = mon[(mon.nvol > 0) & (mon.shares > 0)]
mon["turn"] = mon.vol / mon.shares * 100
TURN_CAP = 300.0
NUM["e1_turn_stock_months_dropped_above_cap"] = dict(cap_pct_per_month=TURN_CAP, n_dropped=int((mon.turn > TURN_CAP).sum()), n_total=int(len(mon)), examples=mon[mon.turn > TURN_CAP].sort_values("turn", ascending=False).head(8).assign(ym=lambda d: d.ym.astype(str))[["ric", "ym", "turn"]].round(0).to_dict("records"))
mon = mon[mon.turn <= TURN_CAP]
mk = mon.dropna(subset=["mcap"]).groupby("ym").apply(lambda g: np.average(g.turn, weights=g.mcap)).rename("mturn")
mon = mon.merge(mk, on="ym")
mon["xturn"] = mon.turn - mon.mturn
ev["ym_pre"] = (ev.AD - pd.offsets.MonthBegin(1)).dt.to_period("M")
ev = ev.drop(columns=[c for c in ["turn", "size", "vol"] if c in ev.columns])
ev = ev.merge(mon[["ric", "ym", "xturn"]].rename(columns={"ric": "RIC", "ym": "ym_pre", "xturn": "turn"}), on=["RIC", "ym_pre"], how="left")
ev["mcap_pre"] = [mc.at[cal[i - 1], r] for r, i in zip(ev.RIC, ev.iAD)]
ev["size"] = ev.mcap_pre / ev.cycle.map(TOT) * 100
ev["size_top100"] = ev.mcap_pre / ev.cycle.map(TOP) * 100
sqm = (AR ** 2).groupby(AR.index.to_period("M")).sum(min_count=1)
def vol12(ric, ym):
    s = sqm.loc[ym - 12:ym - 1, ric]
    return np.nan if s.isna().any() or len(s) < 12 else s.mean()
ev["vol"] = [vol12(r, y) for r, y in zip(ev.RIC, ev.ym_pre)]
NUM["e1_controls_missing"] = {c: int(ev[c].isna().sum()) for c in ["turn", "size", "vol"]}
NUM["e1_mean_size_pct_by_type"] = ev.groupby("type")["size"].mean().round(4).to_dict()
e1 = []
for typ in ["addition", "deletion"]:
    for smp, s in SMP().items():
        s = s[(s.type == typ)].dropna(subset=["tot", "turn", "size", "vol"])
        for variant in ["uncentred", "demeaned"]:
            C = s[["turn", "size", "vol"]].copy()
            if variant == "demeaned":
                C = C - C.mean()
            X = pd.concat([C, pd.get_dummies(s.period).reindex(columns=PER).astype(float)], axis=1)
            t = coef_table(s.tot, X, s.adx, list(X.columns))
            t.insert(0, "variant", variant); t.insert(0, "sample", smp); t.insert(0, "type", typ)
            e1.append(t)
            if variant == "uncentred" or smp == "all":
                for r in t.itertuples():
                    add_row("E1 composition", f"Table 3 eq. (4), {typ}s, {variant}", smp, r.var, r._asdict(), "same spec; universe/era deviate" if variant == "uncentred" else "deviates (HBS/JF demean the controls)", f"Coefficient on {r.var} in the regression of the total return on turnover, size, volatility and five era dummies without a constant, {typ}s, {smp} sample.")
        if smp == "all" or typ == "deletion":
            pass
e1 = pd.concat(e1)
e1.to_csv(os.path.join(OUT, "e1_table3_long.csv"), index=False)
# fallback with top-100 size for comparison
e1b = []
for typ in ["addition", "deletion"]:
    s = ev[(ev.type == typ)].dropna(subset=["tot", "turn", "size_top100", "vol"])
    X = pd.concat([s[["turn", "size_top100", "vol"]], pd.get_dummies(s.period).reindex(columns=PER).astype(float)], axis=1)
    t = coef_table(s.tot, X, s.adx, list(X.columns)); t.insert(0, "type", typ); e1b.append(t)
pd.concat(e1b).to_csv(os.path.join(OUT, "e1_table3_size_top100.csv"), index=False)
NUM["e1"] = {f"{r.type}_{r.sample}_{r.variant}_{r.var}": dict(coef=round(r.coef, 4), se_hc1=round(r.se_hc1, 4), se_cr1=round(r.se_cr1, 4), p_hc1=round(r.p_hc1, 4), p_wcb=round(r.p_wcb, 4), N=int(r.N), G=int(r.G), r2=round(r.r2, 4)) for r in e1.itertuples()}
print(e1[(e1["sample"] == "all") & (e1.variant == "uncentred")][["type", "var", "coef", "se_hc1", "se_cr1", "p_hc1", "N", "G", "r2"]].round(3).to_string())

# ---------- E2: average liquidity (Fig. 4) ----------
bw = px.pivot(index="date", columns="ric", values="bid").reindex(cal)
aw = px.pivot(index="date", columns="ric", values="ask").reindex(cal)
rsp = ((aw - bw) / ((aw + bw) / 2) * 100).where((bw > 0) & (aw >= bw))
rsp = rsp.where(rsp <= 20)
NUM["e2_spread_obs_dropped_above_20pct"] = int((((aw - bw) / ((aw + bw) / 2) * 100).where((bw > 0) & (aw >= bw)) > 20).sum().sum())
w = mc.where(rsp.notna())
vw_all = (rsp * w).sum(axis=1) / w.sum(axis=1)
vw_mem = pd.Series(np.nan, index=cal)
for i, c in enumerate(cyc):
    lo = rev.ED[c]
    hi = rev.ED[cyc[i + 1]] if i + 1 < len(cyc) else cal[-1] + pd.Timedelta(days=1)
    if i == 0:
        lo0 = cal[0]
        rics = [k for k in before[c] if k in rsp.columns]
        m = (cal >= lo0) & (cal < lo)
        vw_mem[m] = ((rsp.loc[m, rics] * w.loc[m, rics]).sum(axis=1) / w.loc[m, rics].sum(axis=1)).values
    rics = [k for k in after[c] if k in rsp.columns]
    m = (cal >= lo) & (cal < hi)
    vw_mem[m] = ((rsp.loc[m, rics] * w.loc[m, rics]).sum(axis=1) / w.loc[m, rics].sum(axis=1)).values
e2 = pd.DataFrame({"vw_spread_omxsb_members": vw_mem.groupby(cal.year).mean(), "vw_spread_all_st_panel": vw_all.groupby(cal.year).mean(), "n_members_with_quote": rsp.notna().sum(axis=1).groupby(cal.year).mean()})
e2 = e2.loc[2007:2026]
ya = ev[ev.type == "addition"].groupby("year").tot.agg(addition_effect_mean="mean", N_additions="count")
yd = ev[ev.type == "deletion"].groupby("year").tot.agg(deletion_effect_mean="mean", N_deletions="count")
ydc = ev[(ev.type == "deletion") & ~ev.flagged].groupby("year").tot.agg(deletion_effect_mean_clean="mean")
e2 = e2.join(ya).join(yd).join(ydc)
e2.index.name = "year"
e2.to_csv(os.path.join(OUT, "e2_spread_by_year.csv"))
fig, ax = plt.subplots(figsize=(6.3, 3.6))
ax.plot(e2.index, e2.vw_spread_omxsb_members, color=PAL[1], marker="o", markersize=3, label="VW relative quoted spread, OMXSB constituents (%)")
ax.plot(e2.index, e2.vw_spread_all_st_panel, color=PAL[3], linestyle="--", label="VW relative quoted spread, all .ST stocks in panel (%)")
ax.set_ylabel("Relative quoted spread (%)"); ax.set_xlabel("Year")
ax2 = ax.twinx(); ax2.spines["right"].set_visible(True)
ax2.bar(e2.index, e2.addition_effect_mean, color=PAL[4], alpha=0.35, label="Mean total return of additions (%)")
ax2.axhline(0, color=PAL[0], linewidth=0.6)
ax2.set_ylabel("Addition effect, mean CAR AD−1 to ED+1 (%)")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
fig.legend(h1 + h2, l1 + l2, loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=1, fontsize=8)
fig.savefig(os.path.join(OUT, "fig_e2_spread_vs_addition_effect.png"), dpi=300); plt.close(fig)
NUM["e2"] = dict(spread_members_2007=round(float(e2.vw_spread_omxsb_members.get(2007, np.nan)), 4), spread_members_2016=round(float(e2.vw_spread_omxsb_members.get(2016, np.nan)), 4), spread_members_2025=round(float(e2.vw_spread_omxsb_members.get(2025, np.nan)), 4), spread_all_2007=round(float(e2.vw_spread_all_st_panel.get(2007, np.nan)), 4), spread_all_2025=round(float(e2.vw_spread_all_st_panel.get(2025, np.nan)), 4))
# correlation of yearly addition effect with yearly spread (descriptive)
cc = e2[["vw_spread_omxsb_members", "addition_effect_mean"]].dropna()
NUM["e2_corr_spread_addition_effect_by_year"] = round(float(cc.corr().iloc[0, 1]), 3)
yy = ev[ev.type == "addition"].merge(e2[["vw_spread_omxsb_members"]], left_on="year", right_index=True).dropna(subset=["tot", "vw_spread_omxsb_members"])
t = coef_table(yy.tot, np.column_stack([np.ones(len(yy)), yy.vw_spread_omxsb_members]), yy.adx, ["const", "spread"])
add_row("E2 average liquidity", "Fig. 4 analogue: total return of additions on the yearly VW quoted spread of OMXSB constituents", "all", "slope on spread (%)", t.iloc[1].to_dict(), "deviates (quoted closing spread, not effective spread; our regression, G&S only plot)", "Slope of the event-level total return of additions on the value-weighted relative quoted spread of the constituents in the event year.")

# ---------- E3: migrations ----------
o30 = pd.read_csv(os.path.join(EV, "omxs30_changes_2005_2026.csv"), parse_dates=["effective_date"])
def normt(t):
    return re.sub(r"\s+", " ", str(t).upper().strip())
o30["tk"] = o30.ticker.map(normt)
o30 = o30.dropna(subset=["effective_date"]).sort_values("effective_date")
def omxs30_member(tk, d):
    """Membership status of ticker tk in OMXS30 on date d, inferred from the change list only: unknown (None) for
    tickers that never appear in the list; before the first listed event, a deletion implies membership and an
    addition implies non-membership."""
    g = o30[o30.tk == tk]
    if g.empty:
        return None
    st = g.iloc[0].type == "deletion"
    for r in g.itertuples():
        if r.effective_date <= d:
            st = r.type == "addition"
    return st
ch["tk"] = ch.ticker.map(normt)
ch["omxs30_member_at_AD"] = [omxs30_member(t, d) for t, d in zip(ch.tk, ch.AD)]
e3 = ch[ch.omxs30_member_at_AD.notna()][["event_id", "effective_date", "company", "ticker", "type", "omxs30_member_at_AD"]]
e3.to_csv(os.path.join(OUT, "e3_omxsb_events_vs_omxs30_membership.csv"), index=False)
mem = ch[ch.omxs30_member_at_AD == True]
NUM["e3"] = dict(n_omxsb_events_with_ticker_in_omxs30_list=int(ch.omxs30_member_at_AD.notna().sum()), n_additions_of_omxs30_members=int((mem.type == "addition").sum()), additions_of_omxs30_members=(mem[mem.type == "addition"].event_id + " " + mem[mem.type == "addition"].company).tolist(), n_deletions_of_omxs30_members=int((mem.type == "deletion").sum()), deletions_of_omxs30_members=(mem[mem.type == "deletion"].event_id + " " + mem[mem.type == "deletion"].company).tolist(), note="membership inferred from the OMXS30 change list only; tickers never in that list have unknown status")

# ---------- E4: predictability ----------
def cum_paths(idx, lo, hi, zero_at=None):
    paths = []
    for r, i in idx:
        s = AR[r].iloc[i + lo:i + hi + 1]
        if len(s) == hi - lo + 1 and not s.isna().any():
            c = s.cumsum().values
            if zero_at is not None:
                c = c - c[zero_at]
            paths.append(c)
    return np.array(paths)
def car_fig(anchor, lo, hi, zero_at, name, xlabel, ylabel):
    data = {}
    for smp, s0 in SMP().items():
        fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0), sharey=True)
        x = np.arange(lo, hi + 1)
        for ax, typ in zip(axs, ["addition", "deletion"]):
            for p, ls in zip(PER, LS):
                s = s0[(s0.type == typ) & (s0.period == p)]
                P = cum_paths(zip(s.RIC, s[anchor]), lo, hi, zero_at)
                ax.plot(x, P.mean(0), label=f"{p} (N = {len(P)})", **ls)
                data[(smp, typ, p)] = pd.Series(P.mean(0), index=x)
            ax.axvline(0, color=PAL[3], linewidth=0.8, linestyle=":"); ax.axhline(0, color=PAL[0], linewidth=0.6, zorder=0)
            ax.text(0.02, 0.97, typ.capitalize() + "s", transform=ax.transAxes, va="top")
        axs[0].set_ylabel(ylabel); fig.supxlabel(xlabel, fontsize=10, y=-0.04)
        h, l = axs[0].get_legend_handles_labels()
        fig.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=8)
        fig.savefig(os.path.join(OUT, f"{name}_{smp}.png"), dpi=300); plt.close(fig)
    data = pd.DataFrame(data); data.columns = [f"{a}|{b}|{c}" for a, b, c in data.columns]
    data.to_csv(os.path.join(OUT, name + ".csv"))
    return data
f8 = car_fig("iAD", -100, 10, 110, "fig_e4a_car_announcement", "Trading days relative to announcement date", "Mean CAR, normalised to zero at AD+10 (%)")
f9 = car_fig("iED", -1, 100, 0, "fig_e4b_car_effective", "Trading days relative to effective date", "Mean CAR from ED−1 (%)")
for smp, s0 in SMP().items():
    for typ in ["addition", "deletion"]:
        if smp == "clean" and typ == "addition":
            continue
        s = s0[s0.type == typ]
        for lo, hi, lab in [(-100, -1, "CAR [AD−100, AD−1]"), (-20, -1, "CAR [AD−20, AD−1]")]:
            y = pd.Series([wsum(r, a + lo, a + hi) for r, a in zip(s.RIC, s.iAD)], index=s.index)
            for p in PER:
                c = cell(y[s.period == p], s.adx[s.period == p])
                add_row("E4 predictability", f"Fig. 8 / HBS Table 4: pre-announcement {lab}, {typ}s", smp, p, c, "same", f"Mean cumulative abnormal return of {typ}s over {lab} in {p}, {smp} sample.")
                NUM[f"e4a_{typ}_{smp}_{lab}_{p}"] = round(c["mean"], 3)
        y = pd.Series([wsum(r, e + 2, e + 100) for r, e in zip(s.RIC, s.iED)], index=s.index)
        for p in PER:
            c = cell(y[s.period == p], s.adx[s.period == p])
            add_row("E4 predictability", f"Fig. 9: post-event CAR [ED+2, ED+100], {typ}s", smp, p, c, "deviates (anchored at ED, not AD)", f"Mean cumulative abnormal return of {typ}s from two days after the effective date to 100 days after it in {p}, {smp} sample.")
            NUM[f"e4b_post_{typ}_{smp}_{p}"] = round(c["mean"], 3)

# E4c: rank of additions among non-constituents at the reference date
pv = (px.assign(pv=px.close * px.volume)).pivot(index="date", columns="ric", values="pv").reindex(cal)
to = pv.fillna(px.pivot(index="date", columns="ric", values="turnover").reindex(cal))
rk = []
for c in cyc:
    ad = rev.AD[c]
    ref = cal[cal < pd.Timestamp(ad.year, ad.month, 1)][-1]
    lo = ref - pd.DateOffset(months=6)
    win = (cal > lo) & (cal <= ref)
    T = to.loc[win]
    ok = T.notna().sum() >= 0.5 * win.sum()
    tsum = T.sum()[ok]
    m = mc.loc[ref].reindex(tsum.index)
    mem = set(before[c])
    cand = [r for r in tsum.index if r not in mem]
    tr = tsum[cand].sort_values(ascending=False)
    mr = m[cand].dropna().sort_values(ascending=False)
    rank_t = pd.Series(np.arange(1, len(tr) + 1), index=tr.index)
    rank_m = pd.Series(np.arange(1, len(mr) + 1), index=mr.index)
    for k in rev.adds[c]:
        rk.append(dict(review_cycle=c, AD=ad, ED=rev.ED[c], key=k, year=rev.ED[c].year, ref_date=ref, n_universe_turnover=len(tr), n_universe_mcap=len(mr), rank_turnover=rank_t.get(k, np.nan), rank_mcap=rank_m.get(k, np.nan), in_panel=k in tsum.index))
rk = pd.DataFrame(rk)
rk["pct_turnover"] = rk.rank_turnover / rk.n_universe_turnover * 100
rk["pct_mcap"] = rk.rank_mcap / rk.n_universe_mcap * 100
rk["post_nov2023"] = rk.ED >= pd.Timestamp("2023-12-01")
rk.to_csv(os.path.join(OUT, "e4c_rank_of_additions.csv"), index=False)
NUM["e4c_additions_without_rank"] = int(rk.rank_turnover.isna().sum())
f10 = rk.groupby("year").agg(N=("key", "size"), N_ranked=("rank_turnover", "count"), universe=("n_universe_turnover", "mean"), mean_turn=("rank_turnover", "mean"), p25_turn=("rank_turnover", lambda x: x.quantile(.25)), p75_turn=("rank_turnover", lambda x: x.quantile(.75)), mean_mcap=("rank_mcap", "mean"), p25_mcap=("rank_mcap", lambda x: x.quantile(.25)), p75_mcap=("rank_mcap", lambda x: x.quantile(.75)), pct_turn_mean=("pct_turnover", "mean"), pct_mcap_mean=("pct_mcap", "mean"))
f10.to_csv(os.path.join(OUT, "fig_e4c_rank.csv"))
for v, nm in [("turn", "6-month SEK turnover"), ("mcap", "market cap")]:
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.fill_between(f10.index, f10[f"p25_{v}"], f10[f"p75_{v}"], color=PAL[3], alpha=0.25, linewidth=0, label="Interquartile range")
    ax.plot(f10.index, f10[f"mean_{v}"], color=PAL[1], marker="o", markersize=3.5, label="Mean rank")
    ax.plot(f10.index, f10.universe, color=PAL[0], linestyle=":", label="Number of non-constituents in panel")
    ax.axvline(2023.5, color=PAL[4], linewidth=0.8, linestyle="--")
    ax.set_xlabel("Year of effective date"); ax.set_ylabel(f"Rank among non-constituents by {nm} (1 = highest)")
    ax.legend(loc="upper left", fontsize=8)
    fig.savefig(os.path.join(OUT, f"fig_e4c_rank_{v}.png"), dpi=300); plt.close(fig)
cyc_ad = dict(zip(rev.index, rev.AD.dt.strftime("%Y-%m-%d")))
rk["adx"] = rk.review_cycle.map(cyc_ad)
for v in ["pct_turnover", "pct_mcap", "rank_turnover", "rank_mcap"]:
    a = rk[~rk.post_nov2023]; b = rk[rk.post_nov2023]
    ca, cb = cell(a[v], a.adx), cell(b[v], b.adx)
    d = diffcell(rk[v], rk.adx, rk.post_nov2023.values.astype(float))
    add_row("E4 predictability", f"Fig. 10 analogue: {v} of added stocks among non-constituents", "all", "before Nov 2023", ca, "deviates (turnover selection rule; panel universe)" if "turn" in v else "deviates (panel universe; mcap is G&S's variable)", f"Mean {v} of added stocks at the reference date for reviews before the November 2023 review.")
    add_row("E4 predictability", f"Fig. 10 analogue: {v} of added stocks among non-constituents", "all", "from Nov 2023 (6-day lead)", cb, "our addition", f"Mean {v} of added stocks for reviews from November 2023, when the announcement lead fell to six trading days.")
    add_row("E4 predictability", f"Fig. 10 analogue: {v} of added stocks among non-constituents", "all", "difference after − before", d, "our addition", f"Difference in mean {v} between reviews from November 2023 and earlier reviews.")
    NUM[f"e4c_{v}_before"] = round(ca["mean"], 2); NUM[f"e4c_{v}_after"] = round(cb["mean"], 2); NUM[f"e4c_{v}_diff_p_hc1"] = round(d["p_hc1"], 3)

# ---------- E5a: volume share (Fig. 11) ----------
vo = px.pivot(index="date", columns="ric", values="volume").reindex(cal)
def vshare(ric, i):
    s = vo[ric].iloc[i - 22:i + 23]
    if len(s) < 45 or s.isna().all():
        return None
    s = s.fillna(0.0)
    return s.values / s.sum() * 100 if s.sum() > 0 else None
f11 = {}
for smp, s0 in SMP().items():
    fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0), sharey=True)
    x = np.arange(-22, 23)
    for ax, typ in zip(axs, ["addition", "deletion"]):
        for p, ls in zip(PER, LS):
            s = s0[(s0.type == typ) & (s0.period == p)]
            V = [(ix_, v) for ix_, v in ((j, vshare(r, i)) for j, r, i in zip(s.index, s.RIC, s.iED)) if v is not None]
            P = np.array([v for _, v in V]); idx = [j for j, _ in V]
            m = P.mean(0)
            ax.plot(x, m, label=f"{p} (N = {len(P)})", **ls)
            f11[(smp, typ, p)] = pd.Series(m, index=x)
            if smp == "all" or typ == "deletion":
                for off, lab in [(21, "ED−1"), (22, "ED")]:
                    c = cell(P[:, off], s.loc[idx, "adx"])
                    add_row("E5 event liquidity", f"Fig. 11: share of ED±22 volume traded on {lab}, {typ}s", smp, p, c, "same (ED−1 is the day the index funds trade, at the close before the change takes effect)" if off == 21 else "same", f"Mean share of the 45-day volume around the effective date that is traded on {lab}, {typ}s, {p}, {smp} sample.")
                    NUM[f"e5a_{lab}_share_{typ}_{smp}_{p}"] = round(c["mean"], 2)
        ax.axvline(0, color=PAL[3], linewidth=0.8, linestyle=":")
        ax.text(0.02, 0.97, typ.capitalize() + "s", transform=ax.transAxes, va="top")
    axs[0].set_ylabel("Share of 45-day volume (%)"); fig.supxlabel("Trading days relative to effective date", fontsize=10, y=-0.04)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=8)
    fig.savefig(os.path.join(OUT, f"fig_e5a_volume_{smp}.png"), dpi=300); plt.close(fig)
f11 = pd.DataFrame(f11); f11.columns = [f"{a}|{b}|{c}" for a, b, c in f11.columns]; f11.to_csv(os.path.join(OUT, "fig_e5a_volume.csv"))

# ---------- E5b: trackers vs all funds (Table 4) ----------
nt = pd.read_csv(os.path.join(OUT0, "nettrading_omxsb.csv"), parse_dates=["AD", "ED"])
nt = nt.merge(ev[["event_id", "flagged", "adx"]], on="event_id", how="left")
nt["year"] = nt.ED.dt.year
t4 = []
for smp, s0 in [("all", nt), ("clean", nt[~nt.flagged.fillna(False)])]:
    m = s0.groupby(["type", "year"])[["nt", "instbuy", "activebuy"]].median()
    m["N"] = s0.groupby(["type", "year"]).size()
    ew = m.groupby(level=0)[["nt", "instbuy", "activebuy"]].mean(); ew["N"] = m.groupby(level=0).N.sum()
    ew.index = pd.MultiIndex.from_tuples([(t, "EW mean of yearly medians") for t in ew.index])
    m = pd.concat([m, ew]); m.insert(0, "sample", smp); t4.append(m)
    for typ in ["addition", "deletion"]:
        if smp == "clean" and typ == "addition":
            continue
        s = s0[s0.type == typ]
        for v, lab in [("nt", "OMXSB trackers"), ("instbuy", "all FI funds"), ("activebuy", "non-tracker funds")]:
            c = cell(s[v], s.adx); c["mean"] = float(ew.loc[(typ, "EW mean of yearly medians"), v])
            add_row("E5 event liquidity", f"Table 4: net trading by {lab} (% of shares), {typ}s, 2019-2026", smp, "EW mean of yearly medians (SE from pooled mean)", c, "deviates (FI funds, not 13F; 2007-2018 missing)", f"Equal-weighted mean of the yearly medians of net trading by {lab} from the quarter before to the quarter after the {typ}, 2019-2026, {smp} sample; the standard errors refer to the pooled mean.")
            NUM[f"e5b_{v}_{typ}_{smp}_ew_mean_of_medians"] = round(c["mean"], 3)
pd.concat(t4).to_csv(os.path.join(OUT, "e5b_table4_medians_by_year.csv"))

# ---------- Demand: Fig. 3 ----------
fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0), sharey=True)
for ax, typ in zip(axs, ["addition", "deletion"]):
    for smp, s0 in [("all", nt), ("clean", nt[~nt.flagged.fillna(False)])]:
        if smp == "clean" and typ == "addition":
            continue
        s = s0[(s0.type == typ)].dropna(subset=["nt", "tot"])
        t = coef_table(s.tot, np.column_stack([np.ones(len(s)), s.nt]), s.adx, ["const", "nt"])
        r = t.iloc[1].to_dict()
        add_row("Demand (Fig. 3)", f"total return on net trading by OMXSB trackers, {typ}s, 2019-2026", smp, "slope on nt (% of shares)", r, "same", f"Slope of the event-level total return on net buying by index trackers in percent of shares outstanding, {typ}s, {smp} sample; R² = {r['r2']:.3f}.")
        NUM[f"fig3_slope_{typ}_{smp}"] = round(r["coef"], 3); NUM[f"fig3_r2_{typ}_{smp}"] = round(r["r2"], 4)
        if smp == "all":
            ax.scatter(s.nt, s.tot, s=12, facecolors="none", edgecolors=PAL[1], linewidths=0.6)
            xs = np.linspace(s.nt.min(), s.nt.max(), 50); ax.plot(xs, t.coef[0] + t.coef[1] * xs, color=PAL[1])
            ax.text(0.02, 0.97, typ.capitalize() + "s", transform=ax.transAxes, va="top")
            ax.text(0.02, 0.88, f"slope = {r['coef']:.2f} ({r['se_hc1']:.2f}) [{r['se_cr1']:.2f}]\nR² = {r['r2']:.3f}, N = {int(r['N'])}", transform=ax.transAxes, va="top", fontsize=8)
    ax.axhline(0, color=PAL[0], linewidth=0.6, zorder=0)
axs[0].set_ylabel("CAR, AD−1 to ED+1 (%)"); fig.supxlabel("Net trading by OMXSB index funds (% of shares outstanding)", fontsize=10, y=-0.04)
fig.savefig(os.path.join(OUT, "fig_d_fig3_nettrading.png"), dpi=300); plt.close(fig)
nt[["event_id", "type", "year", "nt", "tot", "flagged"]].to_csv(os.path.join(OUT, "fig_d_fig3_nettrading.csv"), index=False)

# expected demand for all years from tracker AUM
aum = pd.read_csv(os.path.join(EV, "tracker_aum.csv"), parse_dates=["date"])
fp = aum[aum.kind == "fund_point"].copy()
daily = pd.DataFrame(index=cal)
for f, g in fp.groupby("fund"):
    s = g.set_index("date").aum_sek_bn.sort_index()
    d = s.reindex(cal.union(s.index)).interpolate(method="time").ffill().reindex(cal)
    d[cal < s.index.min()] = np.nan
    daily[f] = d
fund_sum = daily.sum(axis=1, min_count=1)
fs = fund_sum.dropna()
ff = fs.index[fs.index >= pd.Timestamp("2018-12-31")][0]
summ = aum[aum.kind == "summary_point"].set_index("date").aum_sek_bn.sort_index()
pts = pd.concat([summ[summ.index < ff], pd.Series({ff: fs[ff]})]).sort_index()
early = pts.reindex(cal.union(pts.index)).interpolate(method="time").reindex(cal)
series = fund_sum.copy()
series[cal < ff] = early[cal < ff]
series[cal < pts.index.min()] = pts.iloc[0]
NUM["aum_construction"] = f"fund-level points (Robur Access Sverige, Nordnet Sverige Index, LF Sverige Index from 2025-06-16) interpolated linearly in time and summed from {ff.date()}; before that, linear interpolation from the notes' summary point (SEK {pts.iloc[0]} bn at {pts.index[0].date()}) to the fund sum at {ff.date()} (SEK {fs[ff]:.1f} bn); held flat at SEK {pts.iloc[0]} bn before {pts.index[0].date()} (assumption)"
series.rename("tracker_aum_sek_bn").to_csv(os.path.join(OUT, "tracker_aum_daily_interpolated.csv"))
NUM["aum"] = {str(d.date()): round(float(series[d]), 2) for d in [cal[cal.searchsorted(pd.Timestamp(y, 6, 1))] for y in [2007, 2012, 2016, 2019, 2022, 2025, 2026]]}
ev["aum_bn"] = series.reindex(cal[ev.iAD - 1]).values
ev["demand_mcap_pct"] = ev.aum_bn * 1e9 / ev.cycle.map(TOT) * 100
ev["adv_sek"] = [to[r].iloc[i - 60:i - 10].mean() if to[r].iloc[i - 60:i - 10].count() >= 25 else np.nan for r, i in zip(ev.RIC, ev.iAD)]
ev["demand_adv_days"] = ev.aum_bn * 1e9 * (ev.mcap_pre / ev.cycle.map(TOT)) / ev.adv_sek
ev["pre2019"] = ev.ED < pd.Timestamp("2019-01-01")
dem = []
for typ in ["addition", "deletion"]:
    for win, lab in [(ev.pre2019, "2007-2018"), (ev.ED.notna(), "2007-2026")]:
        for smp, s0 in SMP().items():
            if smp == "clean" and typ == "addition":
                continue
            for v, vl in [("demand_mcap_pct", "expected demand, % of mcap (= AUM / total OMXSB mcap)"), ("demand_adv_days", "expected demand in days of ADV")]:
                s = s0[(s0.type == typ) & win.loc[s0.index]].dropna(subset=["tot", v])
                if len(s) < 10:
                    continue
                t = coef_table(s.tot, np.column_stack([np.ones(len(s)), s[v]]), s.adx, ["const", v])
                r = t.iloc[1].to_dict(); r.update(type=typ, window=lab, sample=smp, var=v); dem.append(r)
                add_row("Demand (Fig. 3)", f"total return on {vl}, {typ}s, {lab}", smp, "slope", r, "deviates (expected demand from tracker AUM, not realised net trading)", f"Slope of the event-level total return on {vl}, {typ}s, {lab}, {smp} sample; R² = {r['r2']:.3f}; the %-of-mcap measure is identical for all stocks in a review, so the slope is identified from variation across reviews only.")
                NUM[f"demand_{v}_{typ}_{lab}_{smp}_slope"] = round(r["coef"], 4)
pd.DataFrame(dem).to_csv(os.path.join(OUT, "fig_d_expected_demand_long.csv"), index=False)
fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0), sharey=True)
for ax, typ in zip(axs, ["addition", "deletion"]):
    s = ev[(ev.type == typ)].dropna(subset=["tot", "demand_adv_days"])
    ax.scatter(s.demand_adv_days, s.tot, s=12, facecolors="none", edgecolors=PAL[1], linewidths=0.6)
    ax.set_xscale("log"); ax.axhline(0, color=PAL[0], linewidth=0.6, zorder=0)
    ax.text(0.02, 0.97, typ.capitalize() + "s", transform=ax.transAxes, va="top")
axs[0].set_ylabel("CAR, AD−1 to ED+1 (%)"); fig.supxlabel("Expected tracker demand, days of ADV (log scale)", fontsize=10, y=-0.04)
fig.savefig(os.path.join(OUT, "fig_d_expected_demand_adv.png"), dpi=300); plt.close(fig)
ev[["event_id", "company", "type", "period", "cycle", "AD", "ED", "tot", "flagged", "turn", "size", "size_top100", "vol", "aum_bn", "demand_mcap_pct", "adv_sek", "demand_adv_days", "nt"]].to_csv(os.path.join(OUT, "events_mechanisms.csv"), index=False)
NUM["demand_mcap_pct_by_period_mean"] = ev.groupby("period").demand_mcap_pct.mean().round(3).to_dict()

# ---------- outputs ----------
R = pd.DataFrame(ROWS)
R.to_csv(os.path.join(OUT, "results_table_long.csv"), index=False)
with open(os.path.join(OUT, "numbers_mechanisms.json"), "w") as f:
    json.dump(dict(sorted(NUM.items())), f, indent=2, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("rows", len(R)); print("done")

# ---------- RESULTS.md ----------
def f(x, d=2):
    return "" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{d}f}"
def row_md(r):
    return f"| {r.explanation} | {r.test} | {r['sample']} | {r.statistic} | {f(r.coef, 3)} | {f(r.se_hc1, 3)} | {f(r.se_cr1, 3)} | {f(r.p_hc1, 3)} | {f(r.p_cr1, 3)} | {f(r.p_wcb, 3)} | {int(r.N) if pd.notna(r.N) else ''} | {int(r.G) if pd.notna(r.G) else ''} | {r.same_as_gs} | {r.what_it_shows} |"
s1 = NUM["step1"]; mb = NUM["membership"]
L = ["# Results: Greenwood & Sammon's five explanations on OMXSB 2007-2026", "",
     f"Produced by `code/build/mechanisms_2007.py` on {pd.Timestamp.today().date()} from `output/omxsb_replication_2007/events_car.csv` (487 events, `tot` = CAR in percent over [AD−1, ED+1] against .OMXSBGI), `nettrading_omxsb.csv`, the LSEG panel `data/raw/lseg/panel_2005_2026/`, the change lists, `data/input/omxsb/omxsb_constituents_2009_06_01.csv` and `data/input/omxsb/tracker_aum.csv`. Plan and source comparison: `PLAN.md`. All numbers in `numbers_mechanisms.json`; the long table in `results_table_long.csv`.", "",
     "Inference: HC1 standard errors as in G&S; CR1 clustered on announcement date and wild cluster bootstrap p-values (Webb weights when G < 12, Rademacher otherwise, 9,999 draws, null imposed) are our additions. `sample` = all events, or `clean` = without the deletions flagged in step 1 (additions never flagged).", "",
     "## Step 1: flagged deletions (our cleaning, not G&S)", "",
     f"Of {s1['deletions']} deletions in the sample: (i) delisted within 100 trading days after ED: {s1['flag_delist_100td']} (the listing/delisting filter of the notebook already removed stocks delisted within 100 calendar days); (ii) public offer, merger/acquirer or delisting application in `deletion_reasons_2007_2026.csv`: {s1['flag_offer']}; (iii) shares outstanding changed by more than 10% between ED and ED+100 trading days: {s1['flag_shares_10pct']} ({s1['flag_shares_increase']} increases, {s1['flag_shares_decrease']} decrease; `shares` missing for {s1['shares_missing']} deletions, which are not flagged). Flagged by any criterion: {s1['flagged_any']}, by period " + ", ".join(f"{k} {v}" for k, v in s1["flagged_by_period"].items()) + ". List: `step1_deletion_flags.csv`. One deletion in the sample is not in the reasons file (226 vs 225).", "",
     "## Constituent reconstruction", "",
     f"The 81-name table of the 2009-05-11 release (effective 2009-06-01) is chained forward and backward through the 39 reviews with the change lists. Keys are LSEG RICs where the event or constituent has one, otherwise the ticker. Inconsistencies found ({mb['n_inconsistencies']}): " + "; ".join(mb["inconsistencies"]) + ". These are stocks deleted at a review without a recorded addition: Nokia (the known chain gap), and CDON, EnQuest, Corem, Norion and Sampo, which entered the index through corporate actions (spin-offs, mergers, fast entry) that are not in the review lists. Members that stop trading (acquired or delisted) are treated as having left the index on their last price date; they are counted separately (`n_exited_delisted` in `membership_coverage_by_review.csv`).", "",
     f"Coverage: {mb['n_members_range'][0]} to {mb['n_members_range'][1]} live members per review; the share of members with a market cap in the panel on AD−1 is {mb['share_found_min']:.2f} at worst (2007H2) and {mb['share_found_mean']:.2f} on average, rising from about 0.82 in 2007 to about 0.93 in 2026 (`membership_coverage_by_review.csv`; the missing names per review are in `membership_missing_mcap_by_review.csv`: Nordea, Tieto and TradeDoubler have no RIC in the panel, Millicom has no market cap, and Skanska B and Tele2 B have no `mcap` field and are filled with close × shares outstanding). The LSEG `mcap` is company-level (identical across share classes: median ratio across A/B pairs {NUM['mcap_dual_class_median_ratio_minus_1']:.3f}), so each company is counted once in the OMXSB total. The reconstructed total is {mb['total_mcap_over_top100_median']:.2f} of the top-100 .ST sum at the median review, so the notebook's top-100 proxy overstates the denominator (it also counts dual-class companies twice, since both share classes carry the company-level mcap); the E1 regression with the top-100 size is in `e1_table3_size_top100.csv`.", "",
     "## E3 Migrations: not replicated", "",
     f"G&S's migration test needs a second index with dedicated passive money on the other side of the move (S&P MidCap 400 ↔ S&P 500). In Sweden the index funds tied to Nasdaq Stockholm indices track OMXS30 (XACT OMXS30, Avanza Zero) and OMXSB (section 5 of `omxsb_notes.md`); there is no Nasdaq mid- or small-cap index change list with dedicated trackers in the repo, and OMXS30 is by construction the 30 most traded stocks, which OMXSB (top 10% by turnover, 70-110 names) also contains. A move between the two therefore cannot generate offsetting selling or buying by the other index's trackers: an OMXSB addition of an OMXS30 member means OMXS30 trackers keep holding, not sell. Checking OMXS30 membership at the announcement date from `omxs30_changes_2005_2026.csv` (status only known for tickers that appear in that list): {NUM['e3']['n_additions_of_omxs30_members']} OMXSB addition of a current OMXS30 member ({', '.join(NUM['e3']['additions_of_omxs30_members'])}) and {NUM['e3']['n_deletions_of_omxs30_members']} OMXSB deletions of OMXS30 members ({', '.join(NUM['e3']['deletions_of_omxs30_members'])}); none is a migration in the G&S sense. No proxy was built (`e3_omxsb_events_vs_omxs30_membership.csv`).", "",
     "## E2: what is and is not available", "",
     f"We have closing quoted bid and ask (relative quoted spread), not effective spreads from trade data, and no implementation-shortfall series (G&S Fig. 5 / HBS Fig. 9 green line): that part is not replicated. The value-weighted relative quoted spread of OMXSB constituents falls from {NUM['e2']['spread_members_2007']:.2f}% (2007) to {NUM['e2']['spread_members_2016']:.2f}% (2016) and {NUM['e2']['spread_members_2025']:.2f}% (2025); across all .ST stocks in the panel from {NUM['e2']['spread_all_2007']:.2f}% to {NUM['e2']['spread_all_2025']:.2f}% (`e2_spread_by_year.csv`, `fig_e2_spread_vs_addition_effect.png`). The correlation of the yearly spread with the yearly mean addition effect is {NUM['e2_corr_spread_addition_effect_by_year']:.2f} (20 years). Stock-days with a relative spread above 20% ({NUM['e2_spread_obs_dropped_above_20pct']}) are dropped as quote errors.", "",
     "## E4c: selection variable", "",
     f"Nasdaq's methodology (\"OMX Stockholm Benchmark Index Methodology\", © 2025, https://indexes.nasdaq.com/docs/Methodology_OMXSB.pdf, fetched) ranks the OMXSPI universe by 12-month SEK turnover, selects the top 10% (minimum 25), then adds by free-float market cap within ICB supersectors to 85% coverage and removes the bottom 30% by turnover; reference dates are the last trading day of April and October and the announcement is after the close on the sixth trading day before the effective date. G&S rank by market cap because S&P selects on it; we rank non-constituents by 6-month SEK turnover (price × volume) ending at the reference date (taken as the last trading day of the month before the announcement month) and, as a second version, by market cap. The universe is the panel, not all of Nasdaq Stockholm, and it grows from about 330 to 700 non-constituents over the window, so percentile ranks are reported next to raw ranks. {NUM['e4c_additions_without_rank']} of the 270 additions in the change lists have no rank (no price data in the window).", "",
     "## Demand measures", "",
     f"For 2019-2026 the realised net trading by OMXSB trackers (`nt`) is used as in G&S Fig. 3. For 2007-2018 (no FI holdings) the expected demand is tracker AUM × index weight / market cap, which with weight = mcap / total OMXSB mcap collapses to AUM / total OMXSB mcap and is identical for every stock in a review; and AUM × weight / ADV, with ADV the mean of close × volume over the 50 trading days ending 11 days before AD. Tracker AUM: {NUM['aum_construction']}; interpolated series in `tracker_aum_daily_interpolated.csv`; values at review dates: " + ", ".join(f"{k} SEK {v} bn" for k, v in NUM["aum"].items()) + ". Mean expected demand in % of market cap by period: " + ", ".join(f"{k} {v:.2f}%" for k, v in NUM["demand_mcap_pct_by_period_mean"].items()) + ". The Nov 2010 Nasdaq OMX release's 'about SEK 160 bn tracking the index' is a different concept (benchmarked assets) and is not used.", "",
     "## Table", "",
     "| Explanation | Test | Sample | Statistic | Coef. | SE HC1 | SE CR1 | p HC1 | p CR1 | p WCB | N | Clusters | Same as G&S / deviates | What it shows |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
L += [row_md(r) for _, r in R.iterrows()]
L += ["", "Units: `tot` and all CARs in percent; turnover in percent of shares outstanding traded in the month (stock minus cap-weighted panel average); size in percent of total OMXSB market cap; volatility in percent² (12-month mean of the monthly sum of squared daily abnormal returns); net trading in percent of shares outstanding; expected demand in percent of market cap or in days of ADV; ranks with 1 = highest.", "",
      "## Figures and data files", "",
      "| File | Content |", "|---|---|",
      "| `fig_e2_spread_vs_addition_effect.png`, `e2_spread_by_year.csv` | E2: yearly VW relative quoted spread (constituents and panel) with the yearly mean addition effect |",
      "| `fig_e4a_car_announcement_{all,clean}.png`, `fig_e4a_car_announcement.csv` | E4: mean CAR from AD−100 to AD+10 by period, normalised at AD+10 (G&S Fig. 8) |",
      "| `fig_e4b_car_effective_{all,clean}.png`, `fig_e4b_car_effective.csv` | E4: mean CAR from ED−1 to ED+100 by period, normalised at ED−1 (G&S Fig. 9, anchored at ED) |",
      "| `fig_e4c_rank_{turn,mcap}.png`, `fig_e4c_rank.csv`, `e4c_rank_of_additions.csv` | E4: mean, p25, p75 rank of added stocks among non-constituents by year (G&S Fig. 10); dashed line = November 2023 review |",
      "| `fig_e5a_volume_{all,clean}.png`, `fig_e5a_volume.csv` | E5: share of ED±22 volume by day and period (G&S Fig. 11) |",
      "| `e5b_table4_medians_by_year.csv` | E5: yearly medians of net trading by trackers, all FI funds and non-trackers, 2019-2026 (G&S Table 4) |",
      "| `fig_d_fig3_nettrading.png`, `fig_d_fig3_nettrading.csv` | Demand: total return against net tracker trading, 2019-2026 (G&S Fig. 3) |",
      "| `fig_d_expected_demand_adv.png`, `fig_d_expected_demand_long.csv` | Demand: total return against expected demand in days of ADV, all years |",
      "| `e1_table3_long.csv`, `e1_table3_size_top100.csv` | E1: all coefficients, both samples, uncentred and demeaned, and the top-100 size variant |",
      "| `events_mechanisms.csv` | event-level variables used here |",
      "| `omxsb_membership_by_review.csv`, `membership_coverage_by_review.csv`, `membership_missing_mcap_by_review.csv`, `membership_inconsistencies.csv` | reconstruction |",
      "| `step1_deletion_flags.csv` | step 1 flags |", "",
      "## Problems flagged", ""]
tcap = NUM["e1_turn_stock_months_dropped_above_cap"]
P = [
    f"Universe: the LSEG panel holds OMXSB constituents 2013-2026, the FTN losers' holdings and the mapped 2007-2012 constituents (about 330 to 800 .ST stocks with prices per year), not all of Nasdaq Stockholm. Everything that requires 'all non-constituents' or 'all listed shares' (E1 market turnover, E2 panel spread, E4c ranks) uses this panel.",
    f"Membership chain: six deletions without a recorded addition (Nokia plus five corporate-action entries), the five reviews Jan 2005 to Jan 2007 are missing so the backward chain stops at the July 2007 review, and corporate-action exits are detected only through the last price date. Coverage of the OMXSB market-cap total is 82% to 93% of members.",
    f"`shares` is sparse before 2009 (2% of stock-days 2004-2006, 70% in 2007), so turnover is missing for {NUM['e1_controls_missing']['turn']} events and the step-1 share-jump flag cannot be evaluated for {s1['shares_missing']} deletions. {tcap['n_dropped']} of {tcap['n_total']} stock-months with monthly turnover above {tcap['cap_pct_per_month']:.0f}% of shares outstanding (a unit mismatch between LSEG-adjusted volume and shares, e.g. Cloetta 2008-12) are dropped before the cap-weighted market average; without this cap the market average is dominated by one stock in 2008-11.",
    f"E1 N: {NUM['e1']['addition_all_uncentred_turn']['N']} of 261 additions and {NUM['e1']['deletion_all_uncentred_turn']['N']} of 226 deletions have all three controls.",
    "E2: closing quoted spreads, not effective spreads; no implementation shortfall. G&S's figure is descriptive; the regression row is ours.",
    "E3: no migration test is possible (see above).",
    "E4b is anchored at ED−1 rather than at AD−1 as in G&S Fig. 9 (the notebook's convention).",
    "E4c: OMXSB selects on turnover, G&S on market cap; the reference date before 2025 is assumed to be the last trading day of the month before the announcement month; 14 additions have no rank.",
    "E5b and Fig. 3: FI fund holdings exist only from 2018Q4, so 2007-2018 has no realised net trading and no 13F-type institutional ownership; FI covers Swedish mutual funds, not all institutions.",
    "Expected demand 2007-2018 rests on a hand-built AUM series: fund points only from 2016 (Nordnet) and 2018 (Robur), the notes' 'roughly SEK 15 bn in 2016' before that, and a flat SEK 15 bn assumption for 2007-2016; XACT OMXSB's AUM was not retrieved. The %-of-mcap measure varies only across reviews (23 clusters in 2007-2018), so its slope is a time-series regression with few effective observations.",
    "The JF version could not be fetched (HTTP 403); the HBS working paper was used for the later conventions (demeaned controls, extra controls WZ and analyst coverage, which we cannot build).",
    "One deletion in the events file (226) is not in `deletion_reasons_2007_2026.csv` (225); it is treated as review_only.",
]
L += [f"- {p}" for p in P]
open(os.path.join(OUT, "RESULTS.md"), "w").write("\n".join(L) + "\n")
print("RESULTS.md written")
