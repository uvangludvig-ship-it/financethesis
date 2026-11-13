"""Append source-gated pre-2007 OMXSB events without altering the existing replication.

The workbook and normalized price supplements remain local/private. See the locked
SPECIFICATION.txt for the estimands, exclusions and interpretation of provisional dates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy import stats

REPO = Path(__file__).resolve().parents[3]
OLD_EVENTS = Path("data/input/omxsb/omxsb_events_with_ric_2007_2026.csv")
OLD_RESULTS = Path("output/omxsb_replication_2007/events_car.csv")
OLD_PANEL = Path("data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet")
OLD_INDEX = Path("data/raw/lseg/panel_2005_2026/indices_daily (1).csv")
EARLY_DATES = {"2003-01-02", "2003-07-01", "2004-01-02", "2004-07-01",
               "2005-01-03", "2005-07-01", "2006-01-02", "2006-07-03"}
PERIODS = ["2002–2006", "2007–2011", "2012–2016", "2017–2021", "2022–2026"]
PRICE_COLUMNS = ["ric", "date", "close", "totret", "volume", "bid", "ask"]
WINDOWS = {"eff": (-1, 1), "post10": (0, 10), "post20": (0, 20),
           "post60": (0, 60), "post100": (0, 100)}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                   allow_nan=False, default=str) + "\n")


def truth(value):
    return str(value).strip().lower() in {"true", "1", "yes"}


def read_workbook(path):
    book = load_workbook(path, read_only=True, data_only=True)
    sheet = book["L&J"]
    assert [c.value for c in sheet[4]] == ["Status", "Issuer", "Code", "Date"]
    records = []
    for row, (status, issuer, ric, date) in enumerate(sheet.iter_rows(min_row=5, values_only=True), 5):
        if status is None:
            continue
        assert status in {"Joiner", "Leaver"} and isinstance(date, datetime)
        if date.year >= 2007:
            continue
        date = date.strftime("%Y-%m-%d")
        category = ("initial_basket" if date == "2002-08-12" else
                    "scheduled_candidate" if date in EARLY_DATES else "other_change")
        records.append(dict(event_id=f"OMXSB-HIST-LJ-{row:04d}", workbook_row=row,
                            company=issuer, RIC=re.sub(r"\s*\(expired\)\s*$", "", str(ric).strip(), flags=re.I),
                            type={"Joiner": "addition", "Leaver": "deletion"}[status],
                            vendor_date=date, effective_date=date, announcement_date="",
                            review_cycle="HIST-" + date, category=category,
                            source_reference=f"L&J!A{row}:D{row}", source_url="",
                            event_verified=False, ed_verified=False, ad_verified=False,
                            source_conflict=False))
    book.close()
    result = pd.DataFrame(records)
    assert result.event_id.is_unique
    assert not result.duplicated(["RIC", "type", "vendor_date"]).any()
    return result


def apply_verification(early, path):
    if not path:
        return early
    overlay = pd.read_csv(path, dtype=str).fillna("")
    assert not overlay.workbook_row.duplicated().any(), "Duplicate event verification"
    result = early.set_index("workbook_row", drop=False).copy()
    for row in overlay.to_dict("records"):
        key = int(row["workbook_row"])
        assert key in result.index, f"Unknown source row {key}"
        for col in ["event_verified", "ed_verified", "ad_verified", "source_conflict"]:
            result.at[key, col] = truth(row.get(col, False))
        for col in ["effective_date", "announcement_date", "source_url"]:
            if row.get(col):
                result.at[key, col] = row[col]
        if result.at[key, "event_verified"] or result.at[key, "ed_verified"]:
            assert result.at[key, "source_url"], "Verified event needs source URL"
        if result.at[key, "ad_verified"]:
            assert result.at[key, "announcement_date"] and result.at[key, "source_url"]
        if result.at[key, "announcement_date"]:
            assert pd.Timestamp(result.at[key, "announcement_date"]) <= pd.Timestamp(result.at[key, "effective_date"])
        assert pd.Timestamp(result.at[key, "effective_date"]).year in range(2002, 2007)
    result["review_cycle"] = "HIST-" + result.effective_date
    return result.reset_index(drop=True)


def merge_supplement(existing, paths, columns):
    """Supplement absent cells only; existing nonmissing cells always have priority."""
    result = existing[columns].copy()
    result["date"] = pd.to_datetime(result.date).dt.normalize()
    assert not result.duplicated(["ric", "date"]).any()
    result = result.set_index(["ric", "date"])
    value_cols = list(result.columns)
    for c in value_cols:
        result[c + "_source"] = pd.Series("existing", index=result.index).where(result[c].notna())
    overlaps = []
    for path in paths:
        extra = pd.read_csv(path)
        extra["date"] = pd.to_datetime(extra.date).dt.normalize()
        assert extra.date.between("2001-01-01", "2007-01-19").all(), "Supplement outside fixed early-history bounds"
        for c in columns:
            if c not in extra:
                extra[c] = np.nan
        assert not extra.duplicated(["ric", "date"]).any(), f"Duplicate source cells: {path}"
        extra = extra[columns].set_index(["ric", "date"])
        common = result.index.intersection(extra.index)
        overlap = {"file": str(path), "overlapping_security_days": len(common)}
        for c in value_cols:
            a, b = result.loc[common, c], extra.loc[common, c]
            both = a.notna() & b.notna()
            overlap[c + "_nonmatching_nonmissing"] = int((both & ~np.isclose(
                pd.to_numeric(a, errors="coerce"), pd.to_numeric(b, errors="coerce"),
                rtol=1e-8, atol=1e-10, equal_nan=True)).sum())
        overlaps.append(overlap)
        for c in value_cols:
            extra[c + "_source"] = pd.Series(str(path), index=extra.index).where(extra[c].notna())
        # A level seam is usable only after direct overlap validation, never by rebasing.
        # Twenty shared values must all agree; otherwise source labels stay different.
        compatibility = []
        for ric in common.get_level_values("ric").unique():
            keys = common[common.get_level_values("ric") == ric]
            for c in value_cols:
                a, b = result.loc[keys, c], extra.loc[keys, c]
                both = a.notna() & b.notna()
                sources = result.loc[keys[both], c + "_source"].dropna().unique()
                same = bool(both.sum() >= 20 and len(sources) == 1 and np.isclose(
                    a[both].to_numpy(float), b[both].to_numpy(float), rtol=1e-8, atol=1e-10).all())
                compatibility.append(dict(ric=ric, field=c, overlap_values=int(both.sum()), compatible=same))
                if same:
                    mask = (extra.index.get_level_values("ric") == ric) & extra[c].notna()
                    extra.loc[mask, c + "_source"] = sources[0]
        overlap["source_compatibility"] = compatibility
        result = result.combine_first(extra)
    return result.reset_index().sort_values(["ric", "date"]), overlaps


def complete_window(series, position, lo, hi):
    a, b = position + lo, position + hi
    if a < 0 or b >= len(series):
        return np.nan
    values = series.iloc[a:b + 1].to_numpy(dtype=float)
    if len(values) != hi - lo + 1 or not np.isfinite(values).all():
        return np.nan
    return float(values.sum())


def prepare_series(panel, index):
    benchmark = index.loc[index.ric.eq(".OMXSBGI") & index.close.notna()].sort_values("date")
    assert not benchmark.date.duplicated().any()
    # Use the union to expose a missing benchmark session, not silently remove it.
    cal = pd.DatetimeIndex(sorted(index.loc[index.ric.isin([".OMXSBGI", ".OMXSPI"]) & index.close.notna(), "date"].unique()))
    assert cal.is_monotonic_increasing
    benchmark = benchmark.set_index("date").reindex(cal)
    market = benchmark.close.pct_change(fill_method=None) * 100
    if "close_source" in benchmark:
        market = market.where(benchmark.close_source.eq(benchmark.close_source.shift(1)))
    series = {}
    for ric, rows in panel.groupby("ric", sort=False):
        rows = rows.set_index("date").sort_index()
        aligned = rows.reindex(cal)
        close = pd.to_numeric(aligned.close, errors="coerce").where(lambda x: x > 0)
        price_ret = close.pct_change(fill_method=None) * 100
        if "close_source" in aligned:
            price_ret = price_ret.where(aligned.close_source.eq(aligned.close_source.shift(1)))
        total = pd.to_numeric(aligned.totret, errors="coerce")
        ret = total.combine_first(price_ret)
        # Do not infer a return when there is no valid price at either endpoint.
        ret = ret.where(close.notna() & close.shift(1).notna())
        aligned["ar"] = ret - market
        aligned["price_fallback"] = (total.isna() & price_ret.notna()).astype(int)
        aligned["close"] = close
        series[ric] = aligned
    return cal, series


def measure(event, cal, series, modern=False):
    record = {k: event.get(k, "") for k in ["event_id", "type", "review_cycle"]}
    ed = pd.Timestamp(event["ED"] if modern else event["effective_date"])
    record["year"] = ed.year
    record["period"] = PERIODS[min(max((ed.year - 2002) // 5, 0), 4)]
    record.update(coverage_100_calendar=False, exact_calendar_date=False, price_series=False,
                  missing_reason="", fallback_days_0_100=0)
    for metric in list(WINDOWS) + ["ann", "tot", "volume_share_edm1", "spread_edm1"]:
        record[metric] = np.nan
    ric = event["RIC"]
    if ric not in series:
        record["missing_reason"] = "no_price_series"
        return record, None
    record["price_series"] = True
    if ed not in cal:
        record["missing_reason"] = "ED_not_in_observed_benchmark_calendar"
        return record, None
    record["exact_calendar_date"] = True
    s = series[ric]
    p = cal.get_loc(ed)
    valid_dates = s.index[s.close.notna()]
    # A fixed source filter, never describe failure as verified listing/delisting.
    span_ok = (len(valid_dates) > 0 and valid_dates.min() <= ed - pd.Timedelta(days=100)
               and valid_dates.max() >= ed + pd.Timedelta(days=100))
    record["coverage_100_calendar"] = bool(span_ok)
    if not modern and not span_ok:
        record["missing_reason"] = "insufficient_price_span_for_100_calendar_day_filter"
        return record, None
    for name, (lo, hi) in WINDOWS.items():
        record[name] = complete_window(s.ar, p, lo, hi)
        record[name + "_fallback_days"] = (int(s.price_fallback.iloc[p+lo:p+hi+1].sum())
                                             if np.isfinite(record[name]) else np.nan)
    ad = event.get("AD", "") if modern else event.get("announcement_date", "")
    ad_ok = modern or (truth(event.get("event_verified")) and truth(event.get("ed_verified"))
                       and truth(event.get("ad_verified")) and not truth(event.get("source_conflict")))
    if ad_ok and pd.notna(ad) and ad and pd.Timestamp(ad) in cal:
        a = cal.get_loc(pd.Timestamp(ad))
        if a <= p:
            record["ann"] = complete_window(s.ar, a, -1, 1)
            record["tot"] = complete_window(s.ar, a, -1, p - a + 1)
            for metric, b in [("ann", a+1), ("tot", p+1)]:
                record[metric + "_fallback_days"] = (int(s.price_fallback.iloc[a-1:b+1].sum())
                                                       if np.isfinite(record[metric]) else np.nan)
    if p >= 22 and p + 22 < len(cal):
        volume = pd.to_numeric(s.volume.iloc[p - 22:p + 23], errors="coerce")
        same_volume_source = "volume_source" not in s or s.volume_source.iloc[p-22:p+23].nunique(dropna=False) == 1
        if same_volume_source and np.isfinite(volume).all() and (volume >= 0).all() and volume.sum() > 0:
            record["volume_share_edm1"] = float(100 * volume.iloc[21] / volume.sum())
    if p >= 1:
        bid, ask = s.iloc[p - 1][["bid", "ask"]]
        same_quote_source = ("bid_source" not in s or s.iloc[p-1].bid_source == s.iloc[p-1].ask_source)
        if same_quote_source and np.isfinite(bid) and np.isfinite(ask) and ask >= bid > 0:
            spread = 200 * (ask - bid) / (ask + bid)
            if spread <= 20:
                record["spread_edm1"] = float(spread)
    record["fallback_days_0_100"] = int(s.price_fallback.iloc[p:p + 101].sum())
    path = None
    if np.isfinite(record["post100"]):
        path = np.r_[0., s.ar.iloc[p:p + 101].cumsum().to_numpy(float)]
    if not np.isfinite(record["eff"]):
        record["missing_reason"] = "incomplete_effective_return_window"
    return record, path


def summarize(frame, metrics):
    result = []
    for metric in metrics:
        for period in PERIODS + ["All"]:
            subset = frame if period == "All" else frame.loc[frame.period.eq(period)]
            for typ in ["addition", "deletion"]:
                group = subset.loc[subset.type.eq(typ)].dropna(subset=[metric])
                means = group.groupby("review_cycle")[metric].mean()
                g = len(means)
                se = means.std(ddof=1) / np.sqrt(g) if g >= 2 else np.nan
                center = means.mean()
                margin = stats.t.ppf(.975, g - 1) * se if g >= 2 else np.nan
                result.append(dict(period=period, type=typ, metric=metric, events=len(group), reviews=g,
                                   mean_event=group[metric].mean(), mean_review=center,
                                   se_review=se, ci_low=center-margin, ci_high=center+margin))
    return pd.DataFrame(result)


def replay_legacy(panel, index, old):
    """Reproduce historical notebook arithmetic, separately from new strict coverage rules."""
    cal = pd.DatetimeIndex(index.loc[index.ric.eq(".OMXSBGI") & index.close.notna(), "date"].sort_values().unique())
    market = index.loc[index.ric.eq(".OMXSBGI")].set_index("date").close.reindex(cal).pct_change(fill_method=None) * 100
    series = {}
    for ric, rows in panel.loc[panel.ric.isin(old.RIC)].groupby("ric"):
        rows = rows.loc[rows.date.isin(cal)].set_index("date").sort_index()
        series[ric] = rows.totret.fillna(rows.close.pct_change(fill_method=None) * 100).reindex(cal) - market
    out = []
    for event in old.to_dict("records"):
        a, e = cal.get_loc(pd.Timestamp(event["AD"])), cal.get_loc(pd.Timestamp(event["ED"]))
        for metric, lo, hi in [("ann", a-1, a+1), ("eff", e-1, e+1), ("tot", a-1, e+1)]:
            value = complete_window(series[event["RIC"]], 0, lo, hi)
            reference = event[metric]
            equal = (pd.isna(value) and pd.isna(reference)) or np.isclose(value, reference, rtol=1e-10, atol=1e-9)
            out.append(dict(event_id=event["event_id"], metric=metric, recomputed=value,
                            stored=reference, equal=bool(equal), difference=value-reference))
    return pd.DataFrame(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO)
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--verification", type=Path)
    parser.add_argument("--price-supplement", type=Path, action="append", default=[])
    parser.add_argument("--index-supplement", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo_root
    out = args.output or repo / "output/omxsb_history_extension_20261103"
    assert not (out/"RUN_LOCK.json").exists(), "Use a fresh versioned output directory; never overwrite an outcome run"
    private = out / "private"
    private.mkdir(parents=True, exist_ok=True)
    inputs = [repo/p for p in [OLD_EVENTS, OLD_RESULTS, OLD_PANEL, OLD_INDEX]] + [args.workbook]
    inputs += args.price_supplement + args.index_supplement + ([args.verification] if args.verification else [])
    hashes_before = {str(p): sha(p) for p in inputs}
    dump(out/"RUN_LOCK.json", dict(locked_utc=datetime.now(timezone.utc).isoformat(),
                                  inputs=hashes_before, script_sha256=sha(Path(__file__)),
                                  specification_sha256=sha(out/"SPECIFICATION.txt") if (out/"SPECIFICATION.txt").exists() else None,
                                  note="Operational lock, not an external preregistration; no new outcome has yet been computed in this run"))
    original = pd.read_csv(repo/OLD_EVENTS, dtype=str).fillna("")
    old = pd.read_csv(repo/OLD_RESULTS)
    early = apply_verification(read_workbook(args.workbook), args.verification)
    early.to_csv(private/"early_source_ledger.csv", index=False)
    # Preserve modern raw columns/values; older raw vendor history is not publicly redistributed.
    modern_catalog = original.assign(category="legacy_2007_2026", source_reference="existing_verified_census")
    catalog = pd.concat([modern_catalog, early], ignore_index=True)
    catalog.to_csv(private/"omxsb_history_catalog_2002_2026.csv", index=False)
    pd.testing.assert_frame_equal(catalog.iloc[:len(original)][original.columns].reset_index(drop=True), original)
    assert not catalog.event_id.duplicated().any()
    candidates = early.loc[early.category.eq("scheduled_candidate") & ~early.source_conflict].copy()
    rics = sorted(set(old.RIC.dropna()) | set(candidates.RIC))
    old_panel = pd.read_parquet(repo/OLD_PANEL, columns=PRICE_COLUMNS, filters=[("ric", "in", rics)])
    old_panel["date"] = pd.to_datetime(old_panel.date).dt.normalize()
    old_index = pd.read_csv(repo/OLD_INDEX, usecols=["ric", "date", "close"], parse_dates=["date"])
    replay = replay_legacy(old_panel, old_index, old)
    replay.to_csv(out/"BASELINE_REPLAY.csv", index=False)
    assert replay.equal.all(), "Legacy arithmetic failed; do not publish extended outcomes"
    panel, overlap = merge_supplement(old_panel, args.price_supplement, PRICE_COLUMNS)
    index, ioverlap = merge_supplement(old_index, args.index_supplement, ["ric", "date", "close"])
    dump(out/"SUPPLEMENT_OVERLAP.json", {"stocks": overlap, "indices": ioverlap, "existing_values_preserved": True})
    cal, series = prepare_series(panel, index)
    gi_dates = set(index.loc[index.ric.eq(".OMXSBGI") & index.close.notna(), "date"])
    pd.DataFrame({"date": sorted(set(cal)-gi_dates), "reason": "OMXSPI_session_missing_OMXSBGI_level"}).to_csv(
        out/"BENCHMARK_MISSING_SESSIONS.csv", index=False)
    rows, paths = [], []
    for is_modern, events in [(True, old), (False, candidates)]:
        for event in events.to_dict("records"):
            record, path = measure(event, cal, series, modern=is_modern)
            record["source_group"] = ("legacy" if is_modern else "primary_verified" if
                truth(event["event_verified"]) and truth(event["ed_verified"]) else "vendor_provisional")
            record["source_reference"] = event.get("source_reference", "")
            record["has_verified_AD"] = is_modern or truth(event.get("ad_verified", False))
            if is_modern:
                # Main AD/ED estimates keep the exact previously exported observation/return definition.
                for metric in ["ann", "eff", "tot"]:
                    record[metric] = event[metric]
            rows.append(record)
            if path is not None:
                paths.extend(dict(event_id=record["event_id"], type=record["type"], period=record["period"],
                                  review_cycle=record["review_cycle"], source_group=record["source_group"],
                                  tau=tau, car=car) for tau, car in zip(range(-1,101), path))
    measured = pd.DataFrame(rows)
    measured.to_csv(out/"EVENT_METRICS.csv", index=False)
    old_subset = measured[measured.source_group.eq("legacy")].set_index("event_id")
    for metric in ["ann", "eff", "tot"]:
        pd.testing.assert_series_equal(old_subset[metric], old.set_index("event_id")[metric], check_names=False)
    metrics = list(WINDOWS) + ["ann", "tot", "volume_share_edm1", "spread_edm1"]
    sets = {"BASELINE": measured.source_group.eq("legacy"),
            "VERIFIED_EXTENDED": ~measured.source_group.eq("vendor_provisional"),
            "PROVISIONAL_EARLY_ONLY": measured.source_group.eq("vendor_provisional"),
            "VERIFIED_EARLY_ONLY": measured.source_group.eq("primary_verified"),
            "PROVISIONAL_COMBINED": pd.Series(True, index=measured.index)}
    for label, mask in sets.items():
        summarize(measured.loc[mask], metrics).to_csv(out/f"{label}_SUMMARY.csv", index=False)
    if paths:
        paths = pd.DataFrame(paths)
        paths.to_csv(out/"BALANCED_ED_PATHS.csv", index=False)
        keys = ["source_group", "period", "type", "tau"]
        path_summary = paths.groupby(keys).agg(
            mean_car_event=("car", "mean"), events=("event_id", "nunique"), reviews=("review_cycle", "nunique"))
        path_summary["mean_car_review"] = paths.groupby(keys+["review_cycle"]).car.mean().groupby(keys).mean()
        path_summary.reset_index().to_csv(out/"BALANCED_ED_PATH_SUMMARY.csv", index=False)
    coverage = measured.loc[~measured.source_group.eq("legacy")].groupby(["year", "type", "source_group"]).agg(
        candidates=("event_id", "size"), price_series=("price_series", "sum"),
        complete_ed=("eff", "count"), complete_post10=("post10", "count"),
        complete_post100=("post100", "count"), complete_total=("tot", "count"),
        complete_volume=("volume_share_edm1", "count"), valid_spread=("spread_edm1", "count")
    ).reset_index()
    coverage.to_csv(out/"EARLY_TEST_COVERAGE.csv", index=False)
    early.groupby(["category", "vendor_date", "type"]).size().rename("source_rows").reset_index().to_csv(
        out/"EARLY_SOURCE_COUNTS.csv", index=False)
    old_rows_preserved = len(old_subset) == len(old)
    hashes_after = {str(p): sha(p) for p in inputs}
    assert hashes_before == hashes_after, "An input changed while executing"
    report = dict(created_utc=datetime.now(timezone.utc).isoformat(), original_input_rows=len(original),
                  original_result_rows=len(old), original_rows_preserved=old_rows_preserved,
                  original_car_replay_pass=bool(replay.equal.all()), replay_values=len(replay),
                  initial_basket_excluded=int(early.category.eq("initial_basket").sum()),
                  other_early_changes_excluded=int(early.category.eq("other_change").sum()),
                  scheduled_candidates=len(candidates), candidate_reviews=candidates.review_cycle.nunique(),
                  verified_early_events=int(measured.source_group.eq("primary_verified").sum()),
                  verified_early_with_eff=int(measured.loc[measured.source_group.eq("primary_verified"), "eff"].notna().sum()),
                  early_with_eff=int(measured.loc[~measured.source_group.eq("legacy"), "eff"].notna().sum()),
                  early_with_total=int(measured.loc[~measured.source_group.eq("legacy"), "tot"].notna().sum()),
                  source_inputs=hashes_before, script_sha256=sha(Path(__file__)),
                  specification_sha256=sha(out/"SPECIFICATION.txt") if (out/"SPECIFICATION.txt").exists() else None,
                  no_announcement_imputation=True, no_FTN_analysis=True,
                  caveats=["2002 is a source snapshot, not 79 addition events",
                           "Provisional workbook-date outcomes are separate from the verified main extension",
                           "Original ann/eff/tot retained exactly; new other windows use strict complete-session rules",
                           "BASELINE_SUMMARY review-t intervals are a new summary, not the legacy notebook CR1/WCB inference",
                           "Review-mean t intervals are nominal exploratory intervals, not multiplicity-adjusted",
                           "No historical ownership, migration or demand inferred from membership alone"])
    dump(out/"RUN_MANIFEST.json", report)
    print(json.dumps({k:v for k,v in report.items() if k not in {"source_inputs", "caveats"}}, indent=2))


if __name__ == "__main__":
    main()
